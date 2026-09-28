"""DB201 Lab 04 starter: scans, B-tree indexes and query plans in SQLite.

Run from this folder:
    python index_lab.py                  # 10,000 characters x ~120 items (about 1.2M rows)
    python index_lab.py --chars 2000     # smaller world for slow laptops
    python index_lab.py --clustered      # insert each character's items together

Python 3.10+, standard library only. The database is rebuilt in a temp file each run.
You edit the functions marked TODO (Parts C and D of lab04.md).
"""
import argparse
import math
import os
import random
import sqlite3
import statistics
import tempfile
import time

ITEMS_PER_CHAR = 120   # the lecture's k: average items a character owns
N_TYPES = 400          # item types; type 7 is made common on purpose (the "potion")
POTION_TYPE = 7
POTION_SHARE = 0.08    # 8% of all item rows are potions

SCHEMA = """
CREATE TABLE items (
  item_id    INTEGER PRIMARY KEY,
  type_id    INTEGER NOT NULL,
  owner_id   INTEGER NOT NULL,
  bag        INTEGER NOT NULL,
  slot       INTEGER NOT NULL,
  quantity   INTEGER NOT NULL,
  durability INTEGER,
  note       TEXT            -- padding so a row is roughly 100 bytes, like the lecture's model
);
"""
# Note: the Lab 02/03 schema has UNIQUE (owner_id, bag, slot). That constraint quietly
# builds an index whose first column is owner_id. We leave it out here so you can see
# the table without any index first.


def build(path, n_chars, clustered, seed=404):
    rng = random.Random(seed)
    rows = []
    for c in range(1, n_chars + 1):
        for s in range(ITEMS_PER_CHAR):
            t = POTION_TYPE if rng.random() < POTION_SHARE else rng.randint(1, N_TYPES)
            rows.append([t, c, s // 24, s % 24, rng.randint(1, 20), rng.randint(1, 100)])
    if not clustered:
        # Items arrive over months of play: shuffle so one character's items are spread
        # across the whole table, as they are in a live game.
        rng.shuffle(rows)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    pad = "x" * 60
    con.executemany(
        "INSERT INTO items (type_id, owner_id, bag, slot, quantity, durability, note) "
        "VALUES (?,?,?,?,?,?,?)",
        (r + [pad] for r in rows),
    )
    con.commit()
    return con


def pages(con):
    page_size = con.execute("PRAGMA page_size").fetchone()[0]
    page_count = con.execute("PRAGMA page_count").fetchone()[0]
    return page_size, page_count


def plan(con, sql, args=()):
    """Return the EXPLAIN QUERY PLAN detail lines as one string."""
    rows = con.execute("EXPLAIN QUERY PLAN " + sql, args).fetchall()
    return " | ".join(r[-1] for r in rows)


def time_queries(con, sql, arg_list, repeat=3):
    """Median milliseconds per query over arg_list, best of `repeat` passes."""
    best = math.inf
    for _ in range(repeat):
        t0 = time.perf_counter()
        for a in arg_list:
            con.execute(sql, a).fetchall()
        best = min(best, (time.perf_counter() - t0) / len(arg_list))
    return best * 1000


def btree_height(n_rows, fanout):
    """The lecture's model: h = ceil(log_f(N)), at least 1."""
    return max(1, math.ceil(math.log(n_rows) / math.log(fanout)))


def model_pages(n_rows, k, rows_per_page, fanout, scattered=True):
    """Pages read by a full scan and by an index lookup that returns k rows."""
    seq = math.ceil(n_rows / rows_per_page)
    heap = k if scattered else math.ceil(k / rows_per_page)
    return seq, btree_height(n_rows, fanout) + heap


# ---------------------------------------------------------------------------
# TODO Part C: selectivity. Return the fraction of rows each query returns.
# ---------------------------------------------------------------------------
def selectivity(con, where_sql, args=()):
    """TODO: return rows matching `where_sql` divided by all rows in items."""
    raise NotImplementedError("selectivity")


# ---------------------------------------------------------------------------
# TODO Part D: the write cost of indexes.
# ---------------------------------------------------------------------------
def insert_rate(con, n_rows=20000, seed=9):
    """TODO: insert n_rows new items in ONE transaction and return rows per second.
    Use the same column mix as build(). Roll the transaction back afterwards
    (con.rollback()) so the table size does not drift between measurements."""
    raise NotImplementedError("insert_rate")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chars", type=int, default=10000)
    ap.add_argument("--clustered", action="store_true")
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="db201_lab04_")
    path = os.path.join(tmp, "items.db")
    t0 = time.perf_counter()
    con = build(path, args.chars, args.clustered)
    n = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    ps, pc = pages(con)
    print(f"built {n:,} rows in {time.perf_counter() - t0:.1f} s  "
          f"(page size {ps} B, {pc:,} pages, {n / pc:.1f} rows/page, "
          f"{'clustered' if args.clustered else 'scattered'})")

    rng = random.Random(1)
    owners = [(rng.randint(1, args.chars),) for _ in range(40)]
    q_owner = "SELECT * FROM items WHERE owner_id = ?"
    q_potion = "SELECT * FROM items WHERE type_id = ?"

    print("\n-- Part A: no index")
    print("plan:", plan(con, q_owner, owners[0]))
    ms_scan = time_queries(con, q_owner, owners[:10], repeat=2)
    print(f"owner lookup: {ms_scan:.2f} ms per query")

    print("\n-- Part B: CREATE INDEX idx_items_owner ON items(owner_id)")
    t0 = time.perf_counter()
    con.execute("CREATE INDEX idx_items_owner ON items(owner_id)")
    print(f"index built in {time.perf_counter() - t0:.2f} s; file now {pages(con)[1]:,} pages")
    print("plan:", plan(con, q_owner, owners[0]))
    ms_idx = time_queries(con, q_owner, owners)
    print(f"owner lookup: {ms_idx:.3f} ms per query  (speed-up x{ms_scan / ms_idx:,.0f})")

    rpp = n / pc
    for fanout in (400,):
        seq, idx = model_pages(n, ITEMS_PER_CHAR, rpp, fanout)
        print(f"model (f={fanout}): scan reads {seq:,} pages, index reads {idx:,} pages "
              f"(h={btree_height(n, fanout)})")

    print("\n-- Part C: a low-selectivity query (all potions)")
    con.execute("CREATE INDEX idx_items_type ON items(type_id)")
    print("plan with index:   ", plan(con, q_potion, (POTION_TYPE,)))
    ms_type_idx = time_queries(con, q_potion, [(POTION_TYPE,)], repeat=3)
    print("plan forced scan:  ", plan(con, "SELECT * FROM items NOT INDEXED WHERE type_id = ?",
                                        (POTION_TYPE,)))
    ms_type_scan = time_queries(con, "SELECT * FROM items NOT INDEXED WHERE type_id = ?",
                                [(POTION_TYPE,)], repeat=3)
    print(f"potions via index: {ms_type_idx:.1f} ms   via scan: {ms_type_scan:.1f} ms")
    try:
        print(f"selectivity owner: {selectivity(con, 'owner_id = ?', owners[0]):.5%}   "
              f"potion: {selectivity(con, 'type_id = ?', (POTION_TYPE,)):.2%}")
    except NotImplementedError:
        print("selectivity(): TODO")

    print("\n-- Part D: what indexes cost on insert")
    try:
        with_two = insert_rate(con)
        con.execute("DROP INDEX idx_items_type")
        con.execute("DROP INDEX idx_items_owner")
        with_none = insert_rate(con)
        print(f"inserts/s with 0 extra indexes: {with_none:,.0f}   with 2: {with_two:,.0f}")
    except NotImplementedError:
        print("insert_rate(): TODO")

    con.close()


if __name__ == "__main__":
    main()
