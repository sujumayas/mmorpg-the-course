"""DB201 Lab 05 starter: split saves, real crashes, and what durability costs.

Run from this folder:
    python acid_lab.py split          # Part A: Monte Carlo of independent per-character saves
    python acid_lab.py crash          # Part B: kill a process in the middle of a trade
    python acid_lab.py commit         # Part C: commits per second under three settings
    python acid_lab.py                # all three

Python 3.10+, standard library only. You edit the functions marked TODO.
"""
import os
import random
import sqlite3
import subprocess
import sys
import tempfile
import time

HERE = os.path.abspath(__file__)

# ---------------------------------------------------------------------------
# Part A: the split save
# ---------------------------------------------------------------------------


def split_save_trial(rng, T, horizon):
    """One trade and one crash under independent per-character saves.

    Character A (giver) and character B (receiver) are each saved every T seconds,
    with independent random phases in [0, T). A trade happens at time 0. The server
    crashes at a time drawn uniformly from [0, horizon). After the crash each character
    is restored from its own last save.

    Returns "dupe" (B's save includes the trade, A's does not), "loss" (A's does, B's
    does not), "ok" (both or neither include it).
    """
    crash = rng.uniform(0, horizon)
    # the first save of each character after the trade happens at its phase
    a_saved = rng.uniform(0, T) < crash
    b_saved = rng.uniform(0, T) < crash
    if b_saved and not a_saved:
        return "dupe"
    if a_saved and not b_saved:
        return "loss"
    return "ok"


def split_save_rates(T, horizon, n=200_000, seed=5):
    rng = random.Random(seed)
    counts = {"dupe": 0, "loss": 0, "ok": 0}
    for _ in range(n):
        counts[split_save_trial(rng, T, horizon)] += 1
    return {k: v / n for k, v in counts.items()}


def split_save_formula(d_over_T):
    """TODO (Part A): the lecture's closed form. For a crash d seconds after the trade,
    with p = min(d / T, 1), return P(dupe). (P(loss) is the same by symmetry.)"""
    raise NotImplementedError("split_save_formula")


def part_a():
    print("== Part A: split saves (T = 300 s)")
    for horizon in (30, 150, 300, 600, 3000):
        r = split_save_rates(300, horizon)
        print(f"  crash within {horizon:>5} s of the trade: dupe {r['dupe']:.3f}  "
              f"loss {r['loss']:.3f}  ok {r['ok']:.3f}")
    try:
        for d in (0.1, 0.5, 0.9, 1.5):
            print(f"  formula P(dupe) at d/T = {d}: {split_save_formula(d):.3f}")
    except NotImplementedError:
        print("  split_save_formula(): TODO")


# ---------------------------------------------------------------------------
# Part B: a real crash in the middle of a trade
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE characters (
  character_id INTEGER PRIMARY KEY,
  gold INTEGER NOT NULL CHECK (gold >= 0)
);
CREATE TABLE items (
  item_id  INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL REFERENCES characters(character_id)
);
"""


def make_world(path):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO characters VALUES (?, ?)", [(1, 0), (2, 500)])
    con.execute("INSERT INTO items VALUES (5001, 1)")  # character 1 sells a sword
    con.commit()
    con.close()


def trade_worker(path, mode):
    """Runs in a child process. Sells sword 5001 from character 1 to character 2 for
    500 gold, and dies with os._exit (no cleanup, no commit) after the second write.

    mode "autocommit": every statement commits on its own.
    mode "transaction": all four writes sit inside one transaction.
    """
    con = sqlite3.connect(path, isolation_level=None)
    if mode == "transaction":
        con.execute("BEGIN")
    con.execute("UPDATE characters SET gold = gold - 500 WHERE character_id = 2")
    con.execute("UPDATE characters SET gold = gold + 500 WHERE character_id = 1")
    os._exit(1)  # the crash: power cut, kill -9, segfault in the zone server
    con.execute("UPDATE items SET owner_id = 2 WHERE item_id = 5001")  # never runs
    con.execute("COMMIT")


def audit(path):
    """TODO (Part B): return a dict with total gold, the sword's owner, and a verdict:
    "consistent" if either nothing happened (gold 0/500, owner 1) or the whole trade
    happened (gold 500/0, owner 2), otherwise "HALF A TRADE"."""
    raise NotImplementedError("audit")


def part_b():
    print("\n== Part B: kill the process between the gold writes and the item write")
    path = os.path.join(tempfile.mkdtemp(prefix="db201_lab05_"), "world.db")
    for mode in ("autocommit", "transaction"):
        make_world(path)
        subprocess.run([sys.executable, HERE, "_worker", path, mode])
        con = sqlite3.connect(path)  # opening the file runs SQLite's recovery
        gold = dict(con.execute("SELECT character_id, gold FROM characters"))
        owner = con.execute("SELECT owner_id FROM items WHERE item_id = 5001").fetchone()[0]
        con.close()
        print(f"  {mode:<12} after restart: gold {gold}  sword owner {owner}")
        try:
            print(f"  {'':<12} audit: {audit(path)}")
        except NotImplementedError:
            print(f"  {'':<12} audit(): TODO")


# ---------------------------------------------------------------------------
# Part C: what durability costs
# ---------------------------------------------------------------------------
def commit_rate(path, n_trades, synchronous, batch):
    """Commit n_trades small trades, `batch` trades per transaction.
    synchronous is SQLite's PRAGMA synchronous: "FULL" waits for the disk on every
    commit (like PostgreSQL's synchronous_commit = on); "OFF" hands data to the OS and
    moves on (closer to synchronous_commit = off, but see the lecture for why it is weaker).
    Returns trades per second."""
    make_world(path)
    con = sqlite3.connect(path, isolation_level=None)
    con.execute("PRAGMA journal_mode = WAL")
    con.execute(f"PRAGMA synchronous = {synchronous}")
    # macOS only: a plain fsync() there does not force the drive to flush its cache,
    # so without this SQLite's FULL is not really waiting for durable storage.
    # Other systems ignore the pragma.
    con.execute("PRAGMA fullfsync = ON")
    con.execute("UPDATE characters SET gold = 1000000000 WHERE character_id = 2")
    t0 = time.perf_counter()
    done = 0
    while done < n_trades:
        con.execute("BEGIN")
        for _ in range(min(batch, n_trades - done)):
            con.execute("UPDATE characters SET gold = gold - 1 WHERE character_id = 2")
            con.execute("UPDATE characters SET gold = gold + 1 WHERE character_id = 1")
            done += 1
        con.execute("COMMIT")
    dt = time.perf_counter() - t0
    con.close()
    return n_trades / dt


def part_c():
    print("\n== Part C: trades per second")
    path = os.path.join(tempfile.mkdtemp(prefix="db201_lab05_"), "rate.db")
    for sync, batch in (("FULL", 1), ("FULL", 10), ("FULL", 100), ("OFF", 1)):
        r = commit_rate(path, 500 if sync == "FULL" else 5000, sync, batch)
        print(f"  synchronous={sync:<4} batch={batch:<3}  {r:>10,.0f} trades/s  "
              f"({1000 / r * batch:.3f} ms per commit)")
    # TODO (Part C): add a row for batch=1000 and explain in lab05.md why the
    # per-commit time stays roughly flat while trades per second grows.


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "_worker":
        trade_worker(sys.argv[2], sys.argv[3])
    else:
        which = sys.argv[1] if len(sys.argv) > 1 else "all"
        if which in ("split", "all"):
            part_a()
        if which in ("crash", "all"):
            part_b()
        if which in ("commit", "all"):
            part_c()
