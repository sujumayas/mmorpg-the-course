"""DB201 Lab 09 starter: add item durability to a live item table, and measure the stalls.

Run:
    python migration_lab.py --check                 # correctness tests only (small table)
    python migration_lab.py                         # tests, then the experiment table
    python migration_lab.py --rows 1000000 --duty 0.5

Python 3.10+, standard library only.
You edit the two functions marked TODO: backfill_batched and fit_rate_and_overhead.

What happens: the script builds an item table in a temporary SQLite file, runs the
expand step (ADD COLUMN), starts a "game" thread that updates random items at a fixed
rate and records how long each write waits, then runs a backfill. It reports total
backfill time and the game's worst and 99th-percentile wait.

SQLite versus PostgreSQL: SQLite allows one writer for the whole database at a time,
so a running batch blocks every game write. PostgreSQL locks only the rows a batch has
updated, so only game writes to those rows wait. The stall for a write that does
collide is the same in both: up to one batch's running time, b / r.
"""
import argparse
import os
import random
import sqlite3
import statistics
import sys
import tempfile
import threading
import time

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------


def connect(path, timeout=120):
    conn = sqlite3.connect(path, timeout=timeout, isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=FULL")  # every commit waits for the disk, like PostgreSQL
    return conn


def build_db(path, rows, seed=1):
    rng = random.Random(seed)
    conn = connect(path)
    conn.execute("CREATE TABLE item_def (id INTEGER PRIMARY KEY, max_durability INTEGER NOT NULL)")
    conn.executemany("INSERT INTO item_def VALUES (?, ?)",
                     [(d, rng.choice([40, 60, 80, 100, 120])) for d in range(1, 501)])
    conn.execute("""CREATE TABLE item_instance (
        id INTEGER PRIMARY KEY, def_id INTEGER NOT NULL, owner_id INTEGER NOT NULL, slot INTEGER NOT NULL,
        affixes TEXT NOT NULL)""")
    conn.execute("CREATE INDEX ix_item_owner ON item_instance(owner_id)")
    conn.execute("BEGIN")
    affix = '{"affixes":[{"stat":"str","v":12},{"stat":"crit","v":3}],"crafted_by":null,"bound":false}'
    conn.executemany("INSERT INTO item_instance VALUES (?, ?, ?, ?, ?)",
                     ((i, rng.randrange(1, 501), rng.randrange(1, rows // 200 + 2), rng.randrange(60), affix)
                      for i in range(1, rows + 1)))
    conn.execute("COMMIT")
    return conn


def expand(conn):
    """Migration 0042: metadata-only in SQLite and in PostgreSQL 11+."""
    conn.execute("ALTER TABLE item_instance ADD COLUMN durability INTEGER")
    conn.execute("CREATE TABLE IF NOT EXISTS backfill_progress (job TEXT PRIMARY KEY, last_id INTEGER NOT NULL)")


def backfill_one_statement(conn):
    """The obvious version: one UPDATE for the whole table. Returns [running time]."""
    t0 = time.perf_counter()
    conn.execute("""UPDATE item_instance SET durability = d.max_durability
                    FROM item_def d WHERE d.id = item_instance.def_id AND item_instance.durability IS NULL""")
    return [time.perf_counter() - t0]


def backfill_batched(conn, batch, duty, job="durability"):
    """TODO (Part A): fill durability in batches of `batch` ids, keeping the duty cycle.

    Requirements:
    - Resume: read last_id from backfill_progress for `job` (0 if absent).
    - Walk primary-key ranges: lo = last_id + 1, hi = lo + batch - 1, until lo > max(id).
    - Each batch is ONE transaction: BEGIN IMMEDIATE; the UPDATE ... FROM item_def
      restricted to `id BETWEEN lo AND hi AND durability IS NULL`; an upsert of
      (job, hi) into backfill_progress; COMMIT.
    - Time each batch's BEGIN..COMMIT with time.perf_counter() and append it to a list.
    - After each batch, sleep run_time * (1 / duty - 1) so the job runs `duty` of the time.
    - Return the list of per-batch running times.
    """
    raise NotImplementedError("backfill_batched")


def fit_rate_and_overhead(points):
    """TODO (Part C): fit t_batch = b / r + o by least squares.

    points is a list of (batch_size, mean_batch_seconds). Fit a straight line
    t = slope * b + intercept, then return (r, o) with r = 1 / slope, o = intercept.
    Use statistics.linear_regression (Python 3.10+) or write the two formulas yourself.
    """
    raise NotImplementedError("fit_rate_and_overhead")


# ---------------------------------------------------------------------------
# The game: a writer thread that measures its own waits
# ---------------------------------------------------------------------------


class GameWriter(threading.Thread):
    def __init__(self, path, rows, rate_per_s, seed=2):
        super().__init__(daemon=True)
        # timeout=0: we poll the lock ourselves every 0.2 ms. SQLite's built-in busy
        # handler sleeps in growing steps up to 100 ms, which would hide the real stall.
        self.conn = connect(path, timeout=0)
        self.rows = rows
        self.interval = 1.0 / rate_per_s
        self.rng = random.Random(seed)
        self.waits = []
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            item = self.rng.randrange(1, self.rows + 1)
            t0 = time.perf_counter()
            while True:
                try:
                    self.conn.execute("UPDATE item_instance SET owner_id = owner_id + 1 WHERE id = ?", (item,))
                    break
                except sqlite3.OperationalError as e:
                    if "locked" not in str(e) and "busy" not in str(e):
                        raise
                    time.sleep(0.0002)
            self.waits.append(time.perf_counter() - t0)
            time.sleep(self.interval)

    def stop(self):
        self.stop_flag.set()
        self.join()
        self.conn.close()


def run_experiment(rows, batch, duty, game_rate=200, seed=1):
    """batch=None runs the one-statement backfill. Returns a dict of measurements."""
    with tempfile.TemporaryDirectory(prefix="DB201_lab09_") as d:
        path = os.path.join(d, "items.db")
        conn = build_db(path, rows, seed)
        expand(conn)
        game = GameWriter(path, rows, game_rate)
        game.start()
        time.sleep(0.3)  # let the game warm up
        t0 = time.perf_counter()
        runs = backfill_one_statement(conn) if batch is None else backfill_batched(conn, batch, duty)
        total = time.perf_counter() - t0
        time.sleep(0.3)
        game.stop()
        missing = conn.execute("SELECT COUNT(*) FROM item_instance WHERE durability IS NULL").fetchone()[0]
        conn.close()
    waits = sorted(game.waits)
    p99 = waits[int(0.99 * (len(waits) - 1))] if waits else 0.0
    return {"batch": batch or rows, "batches": len(runs), "total_s": total,
            "mean_batch_s": statistics.fmean(runs), "max_wait_s": max(waits, default=0.0),
            "p99_wait_s": p99, "game_writes": len(waits), "missing": missing}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def run_checks():
    with tempfile.TemporaryDirectory(prefix="DB201_lab09_check_") as d:
        path = os.path.join(d, "items.db")
        conn = build_db(path, 5_000, seed=3)
        expand(conn)
        # Pre-fill a few rows as "v42 already wrote durability": the backfill must not overwrite them.
        conn.execute("UPDATE item_instance SET durability = 7 WHERE id IN (10, 20, 30)")
        runs = backfill_batched(conn, 700, duty=1.0)
        assert len(runs) == 8, f"5,000 rows in batches of 700 should take 8 batches, got {len(runs)}"
        missing = conn.execute("SELECT COUNT(*) FROM item_instance WHERE durability IS NULL").fetchone()[0]
        assert missing == 0, f"{missing} rows still NULL"
        wrong = conn.execute("""SELECT COUNT(*) FROM item_instance i JOIN item_def d ON d.id = i.def_id
                                WHERE i.durability <> d.max_durability AND i.id NOT IN (10, 20, 30)""").fetchone()[0]
        assert wrong == 0, f"{wrong} rows have the wrong durability"
        kept = conn.execute("SELECT COUNT(*) FROM item_instance WHERE id IN (10,20,30) AND durability = 7").fetchone()[0]
        assert kept == 3, "the backfill overwrote values that new code had already written"
        last = conn.execute("SELECT last_id FROM backfill_progress WHERE job='durability'").fetchone()
        assert last and last[0] >= 5_000, "progress must record the last finished id"
        assert backfill_batched(conn, 700, duty=1.0) == [], "a finished job must resume and do nothing"
        print("Part A ok: batches, idempotence, resume")

        t0 = time.perf_counter()
        conn.execute("DELETE FROM backfill_progress")
        conn.execute("UPDATE item_instance SET durability = NULL")
        runs = backfill_batched(conn, 1_000, duty=0.5)
        elapsed = time.perf_counter() - t0
        assert elapsed >= 1.7 * sum(runs), "duty 0.5 should roughly double the running time"
        print("Part A ok: duty cycle pauses")
        conn.close()

    r, o = fit_rate_and_overhead([(100, 0.003), (1_000, 0.012), (10_000, 0.102)])
    assert abs(r - 100_000) / 100_000 < 0.01 and abs(o - 0.002) < 1e-4, (r, o)
    print("Part C ok: fit recovers r = 100,000 rows/s and o = 2 ms on synthetic data")


# ---------------------------------------------------------------------------
# Experiment table
# ---------------------------------------------------------------------------


def run_table(rows, duty):
    print(f"\nItem table of {rows:,} rows, duty cycle {duty}, game writing 200 items/s")
    print(f"{'batch':>10} {'batches':>8} {'total s':>9} {'batch ms':>9} {'max wait ms':>12} {'p99 ms':>8}")
    points = []
    for batch in (None, 100_000, 10_000, 1_000, 100):
        if batch is not None and batch >= rows:
            continue
        res = run_experiment(rows, batch, duty if batch else 1.0)
        assert res["missing"] == 0
        if batch is not None:
            points.append((batch, res["mean_batch_s"]))
        label = "one stmt" if batch is None else f"{batch:,}"
        print(f"{label:>10} {res['batches']:>8,} {res['total_s']:>9.2f} {res['mean_batch_s'] * 1e3:>9.2f} "
              f"{res['max_wait_s'] * 1e3:>12.1f} {res['p99_wait_s'] * 1e3:>8.2f}")
    r, o = fit_rate_and_overhead(points)
    print(f"\nFitted r = {r:,.0f} rows/s, o = {o * 1e3:.2f} ms per batch")
    print("Model check: longest stall should be about b / r; total about (N/b)(b/r + o)/d.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--rows", type=int, default=1_000_000)
    ap.add_argument("--duty", type=float, default=0.5)
    args = ap.parse_args()
    try:
        run_checks()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}. Finish the TODOs, then run again.")
        sys.exit(1)
    if not args.check:
        run_table(args.rows, args.duty)


if __name__ == "__main__":
    main()
