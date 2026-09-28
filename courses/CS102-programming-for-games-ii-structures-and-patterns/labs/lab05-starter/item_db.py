"""CS102 Lab 05 starter: an item database, three ways.

Run:  python item_db.py           (runs the benchmarks; dict parts print TODO until you write them)
      python item_db.py --check   (runs the correctness checks only)

The game data is synthetic: N item definitions with integer ids, a name and a price.
Your job (see lab05.md):
  1. Implement DictItemDB.get and DictItemDB.add so they run in O(1) average time.
  2. Implement load_unique_set, the set-based version of load_unique_list.
  3. Fill in the table in lab05.md from the benchmark output.
"""
import random
import sys
import time

FRAME_MS = 1000.0 / 60.0          # 16.67 ms at 60 frames per second


def make_items(n, seed=5):
    """Return n item records (id, name, price) with ids shuffled so order tells you nothing."""
    rng = random.Random(seed)
    ids = list(range(100_000, 100_000 + n))
    rng.shuffle(ids)
    return [(item_id, f"item_{item_id}", rng.randint(1, 5000)) for item_id in ids]


class ListItemDB:
    """Items kept in a Python list. get() scans from the front: O(n)."""

    def __init__(self):
        self.items = []

    def add(self, record):
        self.items.append(record)

    def get(self, item_id):
        for record in self.items:
            if record[0] == item_id:
                return record
        return None


class DictItemDB:
    """Items kept in a dict keyed by id. TODO: make get() and add() O(1) on average."""

    def __init__(self):
        self.by_id = {}

    def add(self, record):
        raise NotImplementedError("TODO: store record under its id")

    def get(self, item_id):
        raise NotImplementedError("TODO: return the record for item_id, or None")


def load_unique_list(records):
    """Keep the first copy of each id. Checks every id seen so far: O(n^2) in total.

    This is the shape of the duplicate check behind GTA Online's slow load (lecture week 5).
    """
    seen = []
    kept = []
    for record in records:
        if record[0] not in seen:        # linear scan of everything loaded so far
            seen.append(record[0])
            kept.append(record)
    return kept


def load_unique_set(records):
    """TODO: same result as load_unique_list, but O(n) in total. Use a set for `seen`."""
    raise NotImplementedError("TODO: set-based duplicate check")


def per_lookup_us(db, queries):
    t0 = time.perf_counter()
    for q in queries:
        db.get(q)
    return (time.perf_counter() - t0) / len(queries) * 1e6


def check():
    items = make_items(500)
    ldb, ddb = ListItemDB(), DictItemDB()
    ok = True
    try:
        for r in items:
            ldb.add(r)
            ddb.add(r)
        for r in items[:50]:
            assert ddb.get(r[0]) == ldb.get(r[0]) == r
        assert ddb.get(-1) is None
        print("DictItemDB: OK")
    except NotImplementedError as e:
        print("DictItemDB:", e)
        ok = False
    dup = items + items[:100]
    random.Random(2).shuffle(dup)
    try:
        assert load_unique_set(dup) == load_unique_list(dup)
        print("load_unique_set: OK")
    except NotImplementedError as e:
        print("load_unique_set:", e)
        ok = False
    return ok


def bench(lookups_per_frame=250):
    print(f"\nLookups per frame: {lookups_per_frame}. Frame budget {FRAME_MS:.2f} ms.")
    print(f"{'n':>7} {'list us/lookup':>15} {'list ms/frame':>14} {'dict us/lookup':>15} {'dict ms/frame':>14}")
    rng = random.Random(9)
    for n in (100, 1_000, 10_000, 100_000):
        items = make_items(n)
        queries = [items[rng.randrange(n)][0] for _ in range(300)]
        ldb = ListItemDB()
        for r in items:
            ldb.add(r)
        lu = per_lookup_us(ldb, queries)
        try:
            ddb = DictItemDB()
            for r in items:
                ddb.add(r)
            du = per_lookup_us(ddb, queries * 20)
            dcol = f"{du:>15.3f} {du * lookups_per_frame / 1000:>14.3f}"
        except NotImplementedError:
            dcol = f"{'TODO':>15} {'TODO':>14}"
        print(f"{n:>7,} {lu:>15.2f} {lu * lookups_per_frame / 1000:>14.2f} {dcol}")

    print("\nDuplicate check while loading (every id unique, as in the GTA Online case)")
    print(f"{'n':>7} {'list ms':>10} {'set ms':>10}")
    for n in (1_000, 5_000, 20_000):
        items = make_items(n)
        t0 = time.perf_counter()
        load_unique_list(items)
        tl = (time.perf_counter() - t0) * 1000
        try:
            t0 = time.perf_counter()
            load_unique_set(items)
            ts = f"{(time.perf_counter() - t0) * 1000:>10.2f}"
        except NotImplementedError:
            ts = f"{'TODO':>10}"
        print(f"{n:>7,} {tl:>10.1f} {ts}")


if __name__ == "__main__":
    check()
    if "--check" not in sys.argv:
        bench()
