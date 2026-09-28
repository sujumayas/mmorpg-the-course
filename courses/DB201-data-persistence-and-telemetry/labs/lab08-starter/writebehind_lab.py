"""DB201 Lab 08 starter: a write-behind cache over SQLite, measured against the model.

Run:
    python writebehind_lab.py --check      # correctness tests only
    python writebehind_lab.py              # tests, then the flush-interval table
    python writebehind_lab.py --players 5000 --rate 2 --seconds 60

Python 3.10+, standard library only.
You edit the two methods marked TODO in WriteBehindCache: take_dirty and flush.

Time here is simulated: the script does not sleep. Changes arrive as a Poisson
process at rate u per player, and a flush runs every T simulated seconds. Every
flush really writes to SQLite, so the row counts are real.

PostgreSQL note: the upsert below (INSERT ... ON CONFLICT ... DO UPDATE ... WHERE)
is valid PostgreSQL too, with %s or $1 placeholders. For big batches in PostgreSQL,
send one statement with unnest() arrays or COPY into a staging table, because some
drivers' executemany still makes one round trip per row.
"""
import argparse
import math
import random
import sqlite3
import sys

SCHEMA = """
CREATE TABLE IF NOT EXISTS char_state (
    id      INTEGER PRIMARY KEY,
    x       REAL    NOT NULL,
    hp      INTEGER NOT NULL,
    xp      INTEGER NOT NULL,
    version INTEGER NOT NULL
)
"""

UPSERT = """
INSERT INTO char_state (id, x, hp, xp, version) VALUES (?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    x = excluded.x, hp = excluded.hp, xp = excluded.xp, version = excluded.version
WHERE excluded.version > char_state.version
"""


def new_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(SCHEMA)
    return conn


class WriteBehindCache:
    """In-memory state per character, a dirty set, and a flusher.

    self.state[pid] = {"x": float, "hp": int, "xp": int, "version": int}
    self.dirty      = set of pids changed since they were last taken for a flush
    self.rows_written counts rows sent to the database over the cache's life.
    """

    def __init__(self):
        self.state = {}
        self.dirty = set()
        self.rows_written = 0
        self.flushes = 0

    def update(self, pid, **changes):
        s = self.state.setdefault(pid, {"x": 0.0, "hp": 100, "xp": 0, "version": 0})
        for k, v in changes.items():
            s[k] = v
        s["version"] += 1
        self.dirty.add(pid)

    def take_dirty(self):
        """TODO (Part A): return a list of (id, x, hp, xp, version) rows for every
        dirty pid, and leave self.dirty empty.

        Swap, don't iterate: replace self.dirty with a new empty set *first*, then
        build rows from the old set. Snapshot the values (copy them into the tuple)
        so that later updates cannot change a row that is about to be written.
        """
        raise NotImplementedError("take_dirty")

    def flush(self, conn):
        """TODO (Part A): write every dirty row with UPSERT in ONE transaction.

        Use take_dirty(), then conn.executemany(UPSERT, rows) inside `with conn:`.
        Add len(rows) to self.rows_written, add 1 to self.flushes if rows were
        written, and return the number of rows.
        """
        raise NotImplementedError("flush")

    def crash(self):
        """The game server dies: everything in memory is gone."""
        self.state.clear()
        self.dirty.clear()


# ---------------------------------------------------------------------------
# The model from the lecture
# ---------------------------------------------------------------------------


def model_writes_per_s(n, u, T):
    if T <= 0:
        return n * u
    return n * (1 - math.exp(-u * T)) / T


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------


def simulate(n, u, T, seconds, seed=1, crash_at=None):
    """Run n players for `seconds` of simulated time with flush interval T.

    T == 0 means write-through: flush after every change.
    If crash_at is set, the cache crashes at that time and the function returns
    what was lost. Returns a dict of measurements.
    """
    rng = random.Random(seed)
    conn = new_db()
    cache = WriteBehindCache()
    total_rate = n * u
    t = 0.0
    next_flush = T if T > 0 else float("inf")
    last_flush_t = 0.0
    changes = 0
    changes_since_flush = 0
    end = seconds if crash_at is None else crash_at
    while True:
        t += rng.expovariate(total_rate)
        while next_flush <= min(t, end):
            cache.flush(conn)
            last_flush_t = next_flush
            changes_since_flush = 0
            next_flush += T
        if t > end:
            break
        pid = rng.randrange(n)
        s = cache.state.get(pid)
        xp = (s["xp"] if s else 0) + 1
        cache.update(pid, x=rng.random() * 1000, hp=rng.randrange(1, 101), xp=xp)
        changes += 1
        changes_since_flush += 1
        if T == 0:
            cache.flush(conn)
            last_flush_t = t
            changes_since_flush = 0
    result = {
        "changes": changes,
        "rows": cache.rows_written,
        "rows_per_s": cache.rows_written / end,
        "model_per_s": model_writes_per_s(n, u, T),
    }
    if crash_at is not None:
        in_memory_xp = sum(s["xp"] for s in cache.state.values())
        cache.crash()
        stored_xp = conn.execute("SELECT COALESCE(SUM(xp), 0) FROM char_state").fetchone()[0]
        result.update(
            lost_changes=changes_since_flush,
            lost_seconds=crash_at - last_flush_t,
            lost_xp=in_memory_xp - stored_xp,
        )
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def run_checks():
    conn = new_db()
    c = WriteBehindCache()
    for i in range(10):
        c.update(1, x=float(i), hp=100 - i, xp=i)
    c.update(2, x=5.0, hp=50, xp=7)
    assert c.flush(conn) == 2, "ten changes to one player plus one to another should coalesce to 2 rows"
    assert c.dirty == set(), "flush must leave the dirty set empty"
    assert conn.execute("SELECT x, hp, xp, version FROM char_state WHERE id=1").fetchone() == (9.0, 91, 9, 10)
    assert c.flush(conn) == 0, "a flush with nothing dirty writes nothing"
    print("Part A ok: coalescing and dirty tracking")

    rows = c.take_dirty()
    assert rows == [], "nothing dirty after a flush"
    c.update(1, xp=100)
    rows = c.take_dirty()
    c.update(1, xp=200)          # arrives during the flush
    assert 1 in c.dirty, "a change during a flush must be dirty again"
    assert rows[0][3] == 100, "the taken row must be a snapshot, not a live reference"
    with conn:
        conn.executemany(UPSERT, rows)
    c.flush(conn)
    assert conn.execute("SELECT xp FROM char_state WHERE id=1").fetchone()[0] == 200
    print("Part A ok: take_dirty swaps and snapshots")

    stale = [(1, 0.0, 1, 1, 3)]  # version 3 is older than what is stored
    with conn:
        conn.executemany(UPSERT, stale)
    assert conn.execute("SELECT xp FROM char_state WHERE id=1").fetchone()[0] == 200, \
        "the version guard must reject an older row"
    print("Part A ok: version guard rejects stale writes")

    r = simulate(200, 2, 5, 60, seed=4)
    assert abs(r["rows_per_s"] - r["model_per_s"]) / r["model_per_s"] < 0.1, r
    print(f"Part B ok: simulated {r['rows_per_s']:.1f} rows/s vs model {r['model_per_s']:.1f}")


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


def run_table(n, u, seconds):
    print(f"\nN={n}, u={u}/s, {seconds} simulated seconds")
    print(f"{'T (s)':>8} {'rows/s':>10} {'model':>10} {'cut %':>7}")
    base = n * u
    for T in (0, 0.1, 0.5, 1, 2, 5, 10, 30):
        r = simulate(n, u, T, seconds, seed=11)
        cut = 100 * (1 - r["rows_per_s"] / base)
        label = "through" if T == 0 else f"{T:g}"
        print(f"{label:>8} {r['rows_per_s']:>10.1f} {r['model_per_s']:>10.1f} {cut:>7.1f}")

    print(f"\nCrash test: 200 crashes at random times, T = 5 s, N={min(n, 500)}")
    rng = random.Random(99)
    lost_s, lost_c = [], []
    for k in range(200):
        crash_at = rng.uniform(5, 60)
        r = simulate(min(n, 500), u, 5, 60, seed=1000 + k, crash_at=crash_at)
        lost_s.append(r["lost_seconds"])
        lost_c.append(r["lost_changes"])
    print(f"mean seconds lost {sum(lost_s) / len(lost_s):.2f} (model T/2 = 2.5), worst {max(lost_s):.2f} (model T = 5)")
    print(f"mean changes lost {sum(lost_c) / len(lost_c):.0f} across the shard")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--players", type=int, default=2000)
    ap.add_argument("--rate", type=float, default=2.0)
    ap.add_argument("--seconds", type=float, default=30.0)
    args = ap.parse_args()
    try:
        run_checks()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}. Finish the TODOs, then run again.")
        sys.exit(1)
    if not args.check:
        run_table(args.players, args.rate, args.seconds)


if __name__ == "__main__":
    main()
