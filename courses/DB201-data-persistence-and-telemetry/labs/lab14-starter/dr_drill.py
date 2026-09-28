"""DB201 Lab 14 starter: a disaster-recovery drill with base backups and an archived log.

Run from this folder:
    python dr_drill.py                         # default drill: base every 600 s, archive every 60 s
    python dr_drill.py --base 1800 --archive 5 # try other policies
    python dr_drill.py --check                 # tests for your TODO functions only

Python 3.10+, standard library only. Files live in a temp folder that is deleted afterwards.
You edit the functions marked TODO (Parts B, C and D of lab14.md).

How the pieces map to PostgreSQL:
  game.db                    -> the live cluster (data directory)
  base_<t>.db (backup API)   -> pg_basebackup output
  archive/seg_<n>.log        -> archived WAL segments (archive_command, archive_timeout)
  the in-memory `pending`    -> the current WAL segment, not yet archived
  restore + replay           -> restore_command + recovery_target_time
The log here is logical (one line per game transaction). Real WAL is physical (page changes),
which is why a WAL archive only replays onto a base backup from the same major version.
"""
import argparse
import json
import os
import random
import sqlite3
import tempfile
import time

N_CHARS = 500
START_GOLD = 1000

SCHEMA = """
CREATE TABLE characters (char_id INTEGER PRIMARY KEY, gold INTEGER NOT NULL CHECK (gold >= 0));
CREATE TABLE items (item_id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL, type_id INTEGER NOT NULL);
CREATE TABLE meta (k TEXT PRIMARY KEY, v INTEGER NOT NULL);
"""


# ---------------------------------------------------------------------------
# Part A (given): the game, its transactions, and the log
# ---------------------------------------------------------------------------

def new_db(path):
    con = sqlite3.connect(path, isolation_level=None)
    # Lab shortcut: no fsync per commit, so the drill runs in seconds. A real server keeps
    # synchronous on (week 1); durability here comes from the archived log instead.
    con.execute("PRAGMA synchronous = OFF")
    con.executescript(SCHEMA)
    con.execute("BEGIN")
    con.executemany("INSERT INTO characters VALUES (?, ?)",
                    [(c, START_GOLD) for c in range(1, N_CHARS + 1)])
    con.execute("INSERT INTO meta VALUES ('last_txn', 0), ('clock', 0), ('next_item', 1)")
    con.execute("COMMIT")
    return con


def apply_op(con, op):
    """Apply one logical transaction. Deterministic, so replay gives the same state.
    Every transaction also records its txn id and game clock in meta, so a backup
    knows exactly which point of the log it contains (its 'LSN')."""
    con.execute("BEGIN")
    kind = op["kind"]
    if kind == "loot":
        con.execute("INSERT INTO items VALUES (?, ?, ?)", (op["item"], op["char"], op["type"]))
        con.execute("UPDATE meta SET v = ? WHERE k = 'next_item'", (op["item"] + 1,))
    elif kind == "trade":   # item moves a -> b, gold moves b -> a
        con.execute("UPDATE items SET owner_id = ? WHERE item_id = ?", (op["b"], op["item"]))
        con.execute("UPDATE characters SET gold = gold - ? WHERE char_id = ?", (op["price"], op["b"]))
        con.execute("UPDATE characters SET gold = gold + ? WHERE char_id = ?", (op["price"], op["a"]))
    elif kind == "vendor":  # item destroyed, gold created (a faucet)
        con.execute("DELETE FROM items WHERE item_id = ?", (op["item"],))
        con.execute("UPDATE characters SET gold = gold + ? WHERE char_id = ?", (op["price"], op["a"]))
    elif kind == "gm_wipe":  # the operator mistake: a script without a WHERE clause
        con.execute("UPDATE characters SET gold = 0")
    con.execute("UPDATE meta SET v = ? WHERE k = 'last_txn'", (op["txn"],))
    con.execute("UPDATE meta SET v = ? WHERE k = 'clock'", (op["t"],))
    con.execute("COMMIT")


def gen_op(con, rng, txn, t):
    """Pick a plausible transaction given the current state."""
    r = rng.random()
    if r < 0.5:
        nxt = con.execute("SELECT v FROM meta WHERE k = 'next_item'").fetchone()[0]
        return {"txn": txn, "t": t, "kind": "loot", "item": nxt,
                "char": rng.randint(1, N_CHARS), "type": rng.randint(1, 400)}
    n_items = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if n_items == 0:
        return None
    # Python's seeded rng, not SQL RANDOM(), so every run of the drill is identical.
    item, owner = con.execute("SELECT item_id, owner_id FROM items ORDER BY item_id LIMIT 1 OFFSET ?",
                              (rng.randrange(n_items),)).fetchone()
    if r < 0.8:
        buyer = rng.randint(1, N_CHARS)
        gold = con.execute("SELECT gold FROM characters WHERE char_id = ?", (buyer,)).fetchone()[0]
        price = min(gold, rng.randint(1, 50))
        if buyer == owner or price == 0:
            return None
        return {"txn": txn, "t": t, "kind": "trade", "item": item, "a": owner, "b": buyer, "price": price}
    return {"txn": txn, "t": t, "kind": "vendor", "item": item, "a": owner, "price": rng.randint(1, 10)}


def state_fingerprint(con):
    """A few numbers that must match between the live database and a correct restore."""
    gold = con.execute("SELECT SUM(gold) FROM characters").fetchone()[0]
    items = con.execute("SELECT COUNT(*), COALESCE(SUM(item_id), 0) FROM items").fetchone()
    last = con.execute("SELECT v FROM meta WHERE k = 'last_txn'").fetchone()[0]
    clock = con.execute("SELECT v FROM meta WHERE k = 'clock'").fetchone()[0]
    return {"gold": gold, "items": items[0], "item_id_sum": items[1], "last_txn": last, "clock": clock}


class Server:
    """Runs the game, takes base backups and archives the log on a schedule."""

    def __init__(self, folder, base_every, archive_every, tps, seed=14):
        self.folder = folder
        self.archive_dir = os.path.join(folder, "archive")
        os.makedirs(self.archive_dir, exist_ok=True)
        self.live_path = os.path.join(folder, "game.db")
        self.con = new_db(self.live_path)
        self.rng = random.Random(seed)
        self.base_every, self.archive_every, self.tps = base_every, archive_every, tps
        self.txn, self.t = 0, 0
        self.pending = []          # log records not yet archived (lost in a disaster)
        self.segments = 0
        self.bases = []            # list of (clock, path)
        self.history = {}          # clock -> fingerprint, for checking restores
        self.take_base_backup()

    def take_base_backup(self):
        path = os.path.join(self.folder, f"base_{self.t:07d}.db")
        dst = sqlite3.connect(path)
        self.con.backup(dst)       # SQLite online backup API: consistent copy of a live db
        dst.close()
        self.bases.append((self.t, path))

    def archive_segment(self):
        if not self.pending:
            return
        path = os.path.join(self.archive_dir, f"seg_{self.segments:06d}.log")
        with open(path, "w") as f:
            for op in self.pending:
                f.write(json.dumps(op) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.segments += 1
        self.pending = []

    def run(self, seconds, gm_wipe_at=None):
        for _ in range(seconds):
            self.t += 1
            for _ in range(self.tps):
                op = gen_op(self.con, self.rng, self.txn + 1, self.t)
                if op is None:
                    continue
                self.txn += 1
                apply_op(self.con, op)
                self.pending.append(op)
            if gm_wipe_at == self.t:
                self.txn += 1
                op = {"txn": self.txn, "t": self.t, "kind": "gm_wipe"}
                apply_op(self.con, op)
                self.pending.append(op)
            self.history[self.t] = state_fingerprint(self.con)
            if self.t % self.archive_every == 0:
                self.archive_segment()
            if self.t % self.base_every == 0:
                self.take_base_backup()

    def disaster(self):
        """The disk holding game.db is gone. Unarchived log records are gone with it."""
        self.con.close()
        os.remove(self.live_path)
        lost = len(self.pending)
        self.pending = []
        return lost


def read_archive(archive_dir):
    """Yield every archived log record in order."""
    for name in sorted(os.listdir(archive_dir)):
        with open(os.path.join(archive_dir, name)) as f:
            for line in f:
                yield json.loads(line)


# ---------------------------------------------------------------------------
# Part B (TODO): point-in-time restore
# ---------------------------------------------------------------------------

def restore_to(bases, archive_dir, target_t, out_path):
    """Rebuild the database as it was at the END of game second `target_t`.

    bases:       list of (clock, path) base backups, oldest first
    archive_dir: folder of archived log segments
    target_t:    replay only records with op["t"] <= target_t (None = everything archived)
    out_path:    where to write the restored database

    Steps (this is what PostgreSQL does with restore_command and recovery_target_time):
      1. Pick the newest base backup whose clock <= target_t (or the newest overall if None).
      2. Copy it to out_path with the SQLite backup API (src.backup(dst)), never by editing it.
      3. Read its meta 'last_txn'. Replay every archived record with txn > last_txn and
         t <= target_t, in order, using apply_op.
      4. Return a dict: {"base_clock": ..., "replayed": number of records applied,
                         "fingerprint": state_fingerprint(restored connection)}
    Close your connections before returning.
    Speed hint: run PRAGMA synchronous = OFF on the restored copy while replaying (a crash
    mid-restore just means you restart the restore), then set it back to FULL.
    """
    raise NotImplementedError("Part B")


# ---------------------------------------------------------------------------
# Part C (TODO): a backup you have not restored is not a backup
# ---------------------------------------------------------------------------

def verify_base_backup(path):
    """Open the backup read-only and prove it is usable. Return a list of problems (empty = ok).

    Check at least:
      - PRAGMA integrity_check returns 'ok'
      - the three tables exist and characters has N_CHARS rows
      - meta has last_txn and clock
    Do not raise on a bad file; report it. An empty or truncated file must produce problems.
    Hint: sqlite3.connect(f"file:{path}?mode=ro", uri=True), and catch sqlite3.DatabaseError.
    """
    raise NotImplementedError("Part C")


# ---------------------------------------------------------------------------
# Part D (TODO): the RPO/RTO model from lecture
# ---------------------------------------------------------------------------

def model(db_gb, restore_mb_s, wal_gb_per_h, replay_gb_per_h, base_every_h, archive_every_s):
    """Return worst-case and average RPO (seconds) and RTO (hours) for the lecture's model.

        rpo_worst_s = archive_every_s                  rpo_avg_s = archive_every_s / 2
        t_copy_h    = db_gb * 1000 / restore_mb_s / 3600
        t_replay_worst_h = wal_gb_per_h * base_every_h / replay_gb_per_h
        rto_worst_h = t_copy_h + t_replay_worst_h      rto_avg_h = t_copy_h + t_replay_worst_h / 2

    TODO: implement and return a dict with those six keys.
    """
    raise NotImplementedError("Part D")


# ---------------------------------------------------------------------------
# Tests and driver
# ---------------------------------------------------------------------------

def check(tmp):
    ok = True
    srv = Server(os.path.join(tmp, "chk"), base_every=50, archive_every=10, tps=5)
    srv.run(125)
    truth_100 = srv.history[100]
    truth_120 = srv.history[120]
    srv.disaster()
    try:
        r = restore_to(srv.bases, srv.archive_dir, 100, os.path.join(tmp, "chk_r100.db"))
        assert r["fingerprint"] == truth_100, (r["fingerprint"], truth_100)
        assert r["base_clock"] == 100 and r["replayed"] == 0
        r = restore_to(srv.bases, srv.archive_dir, None, os.path.join(tmp, "chk_rall.db"))
        assert r["fingerprint"] == truth_120, "restore to end should reach the last archived second (120)"
        print("  Part B ok")
    except NotImplementedError:
        print("  Part B not done"); ok = False
    try:
        assert verify_base_backup(srv.bases[-1][1]) == []
        bad = os.path.join(tmp, "chk_bad.db")
        open(bad, "wb").close()
        assert verify_base_backup(bad), "an empty file must fail verification"
        with open(srv.bases[-1][1], "rb") as f:
            head = f.read(4096)
        trunc = os.path.join(tmp, "chk_trunc.db")
        with open(trunc, "wb") as f:
            f.write(head)
        assert verify_base_backup(trunc), "a truncated file must fail verification"
        print("  Part C ok")
    except NotImplementedError:
        print("  Part C not done"); ok = False
    try:
        m = model(400, 250, 10, 100, 24, 60)
        assert abs(m["rto_worst_h"] - (400 * 1000 / 250 / 3600 + 2.4)) < 1e-9
        assert m["rpo_worst_s"] == 60 and m["rpo_avg_s"] == 30
        print("  Part D ok")
    except NotImplementedError:
        print("  Part D not done"); ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=int, default=600, help="seconds between base backups")
    ap.add_argument("--archive", type=int, default=60, help="seconds between archived log segments")
    ap.add_argument("--tps", type=int, default=20, help="game transactions per second")
    ap.add_argument("--seconds", type=int, default=1500, help="game seconds before the disaster")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="DB201_lab14_") as tmp:
        print("Tests:")
        passed = check(tmp)
        if a.check:
            raise SystemExit(0 if passed else 1)

        print(f"\nDrill 1: disk loss. base every {a.base} s, archive every {a.archive} s, "
              f"{a.tps} txn/s, disaster at t={a.seconds + 37}")
        srv = Server(os.path.join(tmp, "d1"), a.base, a.archive, a.tps)
        srv.run(a.seconds + 37)   # the disaster lands mid-segment on purpose
        truth = srv.history[srv.t]
        lost = srv.disaster()
        print(f"  live state at failure: {truth}")
        print(f"  base backups: {len(srv.bases)}, archived segments: {srv.segments}, "
              f"unarchived records lost: {lost}")
        try:
            t0 = time.perf_counter()
            r = restore_to(srv.bases, srv.archive_dir, None, os.path.join(tmp, "d1_restored.db"))
            wall = time.perf_counter() - t0
            f = r["fingerprint"]
            print(f"  restored from base at t={r['base_clock']}, replayed {r['replayed']} records "
                  f"in {wall * 1000:.0f} ms")
            print(f"  restored state: {f}")
            print(f"  RPO this drill: {srv.t - f['clock']} game seconds, "
                  f"{truth['last_txn'] - f['last_txn']} transactions")
        except NotImplementedError:
            print("  Part B not done: cannot restore")

        print("\nDrill 2: operator mistake. A GM script zeroes every character's gold at t=700.")
        srv2 = Server(os.path.join(tmp, "d2"), a.base, a.archive, a.tps, seed=41)
        srv2.run(900, gm_wipe_at=700)
        srv2.archive_segment()
        print(f"  gold now: {srv2.history[900]['gold']:,} (before the script: {srv2.history[699]['gold']:,})")
        try:
            r = restore_to(srv2.bases, srv2.archive_dir, 699, os.path.join(tmp, "d2_pitr.db"))
            print(f"  PITR to t=699: gold {r['fingerprint']['gold']:,}, matches history: "
                  f"{r['fingerprint'] == srv2.history[699]}")
            print("  Every transaction from t=700 to t=900 is now gone from this copy. "
                  "Part E asks what you do about them.")
        except NotImplementedError:
            print("  Part B not done: cannot do point-in-time recovery")

        try:
            print("\nPart C. Verifying every base backup of drill 1:")
            bad = sum(1 for _, p in srv.bases if verify_base_backup(p))
            print(f"  {len(srv.bases) - bad} ok, {bad} with problems")
        except NotImplementedError:
            print("  Part C not done")


if __name__ == "__main__":
    main()
