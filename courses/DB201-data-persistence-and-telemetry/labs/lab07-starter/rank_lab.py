"""DB201 Lab 07 starter: what rank am I? SQL counting versus a skip list with spans.

Run:
    python rank_lab.py --check            # correctness tests only (small board)
    python rank_lab.py                    # tests, then the timing table (200,000 players)
    python rank_lab.py --players 1000000  # bigger board, slower to build

Python 3.10+, standard library only (sqlite3 ships with Python).
You edit the three functions marked TODO: rank_sql, SkipList.zrevrank, build_snapshot.

PostgreSQL note: the SQL here runs unchanged on PostgreSQL (use %s or $1 placeholders
instead of ?). PostgreSQL's index-only scan does more work per entry than SQLite's
covering-index scan, so expect a larger cost per entry there, with the same shape.
"""
import argparse
import math
import random
import sqlite3
import sys
import time

# ---------------------------------------------------------------------------
# The board
# ---------------------------------------------------------------------------


def build_db(n_players, seed=7):
    """Create an in-memory board with unique scores and an index on score.

    Scores are unique so that "rank = players with a higher score + 1" is exact.
    Returns the connection.
    """
    rng = random.Random(seed)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE players (id INTEGER PRIMARY KEY, score INTEGER NOT NULL)")
    scores = rng.sample(range(1_000_000_000), n_players)
    conn.executemany("INSERT INTO players VALUES (?, ?)", enumerate(scores, start=1))
    conn.execute("CREATE INDEX ix_players_score ON players(score)")
    conn.commit()
    return conn


def rank_sql(conn, player_id):
    """TODO (Part A): return the 1-based rank of player_id (rank 1 = highest score).

    Use one SQL statement that counts players with a strictly higher score.
    Check with EXPLAIN QUERY PLAN that SQLite uses ix_players_score as a covering index.
    """
    raise NotImplementedError("rank_sql")


# ---------------------------------------------------------------------------
# A sorted set: skip list with spans plus a hash table (the Redis design)
# ---------------------------------------------------------------------------

MAX_LEVEL = 32
P = 0.25  # chance a node is promoted one more level


class Node:
    __slots__ = ("key", "member", "forward", "span")

    def __init__(self, key, member, level):
        self.key = key            # sort key: (-score, member), smallest first = rank 1
        self.member = member
        self.forward = [None] * level
        self.span = [0] * level   # how many rank positions forward[i] jumps over


class SkipList:
    """Members ordered by score descending, ties by member ascending.

    self.scores is the hash-table half: member -> score, O(1).
    self.head is a sentinel node with MAX_LEVEL lanes.
    """

    def __init__(self, seed=0):
        self.rng = random.Random(seed)
        self.head = Node(None, None, MAX_LEVEL)
        self.level = 1
        self.length = 0
        self.scores = {}
        self.last_steps = 0  # set by zrevrank: nodes visited in the last lookup

    def _random_level(self):
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < P:
            lvl += 1
        return lvl

    def zadd(self, member, score):
        """Insert a new member (updating an existing member is not needed in this lab)."""
        if member in self.scores:
            raise ValueError("member already present; this lab only inserts")
        key = (-score, member)
        update = [None] * MAX_LEVEL
        rank = [0] * MAX_LEVEL
        x = self.head
        for i in range(self.level - 1, -1, -1):
            rank[i] = 0 if i == self.level - 1 else rank[i + 1]
            while x.forward[i] is not None and x.forward[i].key < key:
                rank[i] += x.span[i]
                x = x.forward[i]
            update[i] = x
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                rank[i] = 0
                update[i] = self.head
                self.head.span[i] = self.length
            self.level = lvl
        node = Node(key, member, lvl)
        for i in range(lvl):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
            node.span[i] = update[i].span[i] - (rank[0] - rank[i])
            update[i].span[i] = (rank[0] - rank[i]) + 1
        for i in range(lvl, self.level):
            update[i].span[i] += 1
        self.length += 1
        self.scores[member] = score

    def zrevrank(self, member):
        """TODO (Part B): return the 1-based rank of member, or None if absent.

        Look up the score in self.scores, build the target key (-score, member),
        then walk from the top lane down. On each lane, move forward while the next
        node's key is <= the target, adding that lane's span to a running total.
        When you land on the member, the running total is its rank.
        Count every forward move in self.last_steps (reset it at the start).
        Expected cost: a small multiple of log2(N) steps for every member.
        """
        raise NotImplementedError("zrevrank")


# ---------------------------------------------------------------------------
# Rank snapshot table (the SQL alternative)
# ---------------------------------------------------------------------------


def build_snapshot(conn):
    """TODO (Part C): (re)build rank_snapshot(id INTEGER PRIMARY KEY, rnk INTEGER).

    Use a window function: RANK() OVER (ORDER BY score DESC).
    Drop and recreate the table, fill it in one INSERT ... SELECT, commit.
    SQLite 3.25+ and every supported PostgreSQL have window functions.
    """
    raise NotImplementedError("build_snapshot")


def rank_snapshot(conn, player_id):
    row = conn.execute("SELECT rnk FROM rank_snapshot WHERE id = ?", (player_id,)).fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def run_checks():
    conn = build_db(2_000, seed=3)
    rows = conn.execute("SELECT id, score FROM players").fetchall()
    truth = {pid: r for r, (pid, _) in enumerate(sorted(rows, key=lambda t: -t[1]), start=1)}
    sample = random.Random(5).sample(list(truth), 200)

    for pid in sample:
        got = rank_sql(conn, pid)
        assert got == truth[pid], f"rank_sql({pid}) = {got}, expected {truth[pid]}"
    print("Part A ok: rank_sql matches brute force on 200 players")

    sl = SkipList(seed=1)
    for pid, score in rows:
        sl.zadd(pid, score)
    worst = 0
    for pid in sample:
        got = sl.zrevrank(pid)
        assert got == truth[pid], f"zrevrank({pid}) = {got}, expected {truth[pid]}"
        worst = max(worst, sl.last_steps)
    assert sl.zrevrank(-1) is None, "absent member should give None"
    assert worst <= 8 * math.log2(len(rows)), f"too many steps ({worst}); are you using the upper lanes?"
    print(f"Part B ok: zrevrank matches brute force; worst lookup {worst} steps for N={len(rows)}")

    build_snapshot(conn)
    for pid in sample:
        got = rank_snapshot(conn, pid)
        assert got == truth[pid], f"rank_snapshot({pid}) = {got}, expected {truth[pid]}"
    print("Part C ok: snapshot ranks match brute force")


# ---------------------------------------------------------------------------
# Timing table
# ---------------------------------------------------------------------------


def time_call(fn, repeats):
    t0 = time.perf_counter()
    for _ in range(repeats):
        fn()
    return (time.perf_counter() - t0) / repeats


def run_bench(n):
    print(f"\nBuilding a board of {n:,} players ...")
    conn = build_db(n)
    by_rank = [pid for (pid,) in conn.execute("SELECT id FROM players ORDER BY score DESC")]
    sl = SkipList(seed=1)
    t0 = time.perf_counter()
    for pid, score in conn.execute("SELECT id, score FROM players"):
        sl.zadd(pid, score)
    print(f"Skip list built in {time.perf_counter() - t0:.1f} s")
    t0 = time.perf_counter()
    build_snapshot(conn)
    snap_build = time.perf_counter() - t0

    ranks = [r for r in (10, 1_000, 10_000, n // 10, n // 2, n - 1) if 1 <= r <= n]
    print(f"\n{'rank':>10} {'SQL ms':>10} {'ns/entry':>9} {'skip steps':>11} {'skip us':>9} {'snapshot us':>12}")
    for r in ranks:
        pid = by_rank[r - 1]
        reps = 20 if r > 10_000 else 200
        t_sql = time_call(lambda: rank_sql(conn, pid), reps)
        t_skip = time_call(lambda: sl.zrevrank(pid), 2_000)
        steps = sl.last_steps
        t_snap = time_call(lambda: rank_snapshot(conn, pid), 2_000)
        per_entry = t_sql / max(r - 1, 1) * 1e9
        print(f"{r:>10,} {t_sql * 1e3:>10.3f} {per_entry:>9.1f} {steps:>11} {t_skip * 1e6:>9.2f} {t_snap * 1e6:>12.2f}")
    print(f"\nSnapshot rebuild for {n:,} players: {snap_build:.2f} s")
    print("Record this table in RESULTS.md. The Python skip list is far slower per step than")
    print("Redis's C code; compare step counts, not microseconds, with the lecture's model.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run tests only")
    ap.add_argument("--players", type=int, default=200_000)
    args = ap.parse_args()
    try:
        run_checks()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}. Finish the TODOs, then run again.")
        sys.exit(1)
    if not args.check:
        run_bench(args.players)


if __name__ == "__main__":
    main()
