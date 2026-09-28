"""DB201 Lab 02 checker: constraint tests, then blob-vs-rows measurements.

Run from this folder:
    python check_schema.py              # uses schema.sql
    python check_schema.py my.sql       # uses another file
    python check_schema.py --tests-only

Python 3.10+, standard library only (sqlite3 with JSON support, SQLite 3.38+).
"""
import json
import os
import random
import sqlite3
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# (description, SQL, should_succeed). Each case runs on a fresh copy of a small base world.
BASE = """
INSERT INTO item_types (type_id, name, rarity, max_stack, vendor_price) VALUES
  (1, 'Minor Healing Potion', 'common', 20, 5),
  (2, 'Emberfang Sword', 'rare', 1, 400),
  (3, 'Copper Ore', 'common', 50, 1);
INSERT INTO characters (character_id, name, class, level, gold) VALUES
  (10, 'Aria', 'warrior', 12, 500),
  (11, 'Bram', 'mage', 9, 300);
INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity, durability) VALUES
  (100, 1, 10, 0, 0, 12, NULL),
  (101, 2, 10, 0, 1, 1, 80);
INSERT INTO item_affixes (item_id, stat, value) VALUES (101, 'fire_damage', 14);
"""

CASES = [
    ("insert a new item in a free slot",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (102, 3, 10, 0, 2, 7)", True),
    ("reject an item whose type does not exist",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (103, 999, 10, 0, 3, 1)", False),
    ("reject an item owned by a character who does not exist",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (104, 3, 999, 0, 3, 1)", False),
    ("reject a stack of zero",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (105, 3, 10, 0, 4, 0)", False),
    ("reject two items in the same owner/bag/slot",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (106, 3, 10, 0, 0, 1)", False),
    ("allow the same bag/slot for a different owner",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (107, 3, 11, 0, 0, 1)", True),
    ("reject a duplicate character name",
     "INSERT INTO characters (character_id, name, class) VALUES (12, 'Aria', 'rogue')", False),
    ("reject a character with no class",
     "INSERT INTO characters (character_id, name, class) VALUES (13, 'Cyra', NULL)", False),
    ("reject negative gold",
     "UPDATE characters SET gold = -1 WHERE character_id = 11", False),
    ("reject the same stat twice on one item",
     "INSERT INTO item_affixes (item_id, stat, value) VALUES (101, 'fire_damage', 3)", False),
    ("reject deleting an item type that items still use",
     "DELETE FROM item_types WHERE type_id = 2", False),
    ("allow an item with no durability (stackables)",
     "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity, durability) VALUES (108, 1, 11, 0, 1, 3, NULL)", True),
]

STRETCH = ("stretch: reject a stack larger than its type's max_stack",
           "INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity) VALUES (109, 1, 11, 0, 2, 21)", False)


def fresh(schema_sql, path=":memory:"):
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(schema_sql)
    return con


def run_case(schema_sql, sql, want_ok):
    con = fresh(schema_sql)
    con.executescript(BASE)
    try:
        con.execute(sql)
        con.commit()
        got_ok = True
    except sqlite3.IntegrityError:
        got_ok = False
    finally:
        con.close()
    return got_ok == want_ok


def tests(schema_sql):
    passed = 0
    try:
        fresh(schema_sql).executescript(BASE)
    except sqlite3.Error as e:
        print(f"Schema or base data failed to load: {e}")
        return False
    for desc, sql, want in CASES:
        ok = run_case(schema_sql, sql, want)
        passed += ok
        print(f"  {'OK  ' if ok else 'FAIL'} {desc}")
    desc, sql, want = STRETCH
    print(f"  {'OK  ' if run_case(schema_sql, sql, want) else 'no  '} {desc}")
    print(f"{passed}/{len(CASES)} required tests pass")
    return passed == len(CASES)


# ---------------------------------------------------------------------------
# Part C: measure blob vs rows on a generated world
# ---------------------------------------------------------------------------

N_CHARS, ITEMS_PER_CHAR, N_TYPES, TARGET_TYPE = 2000, 150, 800, 42


def world(seed=201):
    rng = random.Random(seed)
    types = [(t, f"Item Type {t:04d}", rng.choice(["common", "common", "uncommon", "rare"]),
              rng.choice([1, 20, 50, 250]), rng.randint(1, 500)) for t in range(1, N_TYPES + 1)]
    chars = [(c, f"Hero{c:05d}", rng.choice(["warrior", "mage", "rogue", "cleric"]),
              rng.randint(1, 60), rng.randint(0, 20000)) for c in range(1, N_CHARS + 1)]
    items, iid = [], 1
    for c in range(1, N_CHARS + 1):
        for s in range(ITEMS_PER_CHAR):
            t = rng.randint(1, N_TYPES)
            cap = types[t - 1][3]
            qty = rng.randint(1, cap)
            dur = rng.randint(1, 100) if cap == 1 else None
            items.append((iid, t, c, s // 30, s % 30, qty, dur))
            iid += 1
    return types, chars, items


def measure(schema_sql):
    types, chars, items = world()
    with tempfile.TemporaryDirectory(prefix="db201-lab02-") as d:
        rows_path, blob_path = os.path.join(d, "rows.db"), os.path.join(d, "blob.db")
        con = fresh(schema_sql, rows_path)
        con.executemany("INSERT INTO item_types (type_id, name, rarity, max_stack, vendor_price) VALUES (?,?,?,?,?)", types)
        con.executemany("INSERT INTO characters (character_id, name, class, level, gold) VALUES (?,?,?,?,?)", chars)
        con.executemany("INSERT INTO items (item_id, type_id, owner_id, bag, slot, quantity, durability) "
                        "VALUES (?,?,?,?,?,?,?)", items)
        con.commit()

        blob = sqlite3.connect(blob_path)
        blob.execute("CREATE TABLE character_blob (character_id INTEGER PRIMARY KEY, inventory TEXT NOT NULL)")
        by_owner = {}
        for (iid, t, c, bag, slot, q, dur) in items:
            by_owner.setdefault(c, []).append({"item_id": iid, "type_id": t, "bag": bag, "slot": slot, "qty": q})
        blob.executemany("INSERT INTO character_blob VALUES (?, ?)",
                         [(c, json.dumps(v)) for c, v in by_owner.items()])
        blob.commit()
        avg_blob = blob.execute("SELECT avg(length(inventory)) FROM character_blob").fetchone()[0]

        def timed(con, sql, reps=5):
            best = None
            for _ in range(reps):
                t0 = time.perf_counter()
                r = con.execute(sql).fetchone()[0]
                dt = time.perf_counter() - t0
                best = dt if best is None or dt < best else best
            return r, best * 1000

        q_rows = f"SELECT sum(quantity) FROM items WHERE type_id = {TARGET_TYPE}"
        q_blob = (f"SELECT sum(json_extract(j.value, '$.qty')) FROM character_blob b, "
                  f"json_each(b.inventory) j WHERE json_extract(j.value, '$.type_id') = {TARGET_TYPE}")
        r1, t1 = timed(con, q_rows)
        r2, t2 = timed(blob, q_blob)
        plan = " / ".join(row[3] for row in con.execute("EXPLAIN QUERY PLAN " + q_rows))
        con.close()
        blob.close()
        print()
        print(f"World: {N_CHARS:,} characters x {ITEMS_PER_CHAR} items = {len(items):,} item rows, {N_TYPES} types")
        print(f"  rows.db size: {os.path.getsize(rows_path) / 1e6:.1f} MB   blob.db size: {os.path.getsize(blob_path) / 1e6:.1f} MB")
        print(f"  average inventory blob: {avg_blob:,.0f} bytes")
        print(f"  'how many of type {TARGET_TYPE} exist?'  rows: {r1} in {t1:.2f} ms   blob: {r2} in {t2:.2f} ms")
        print(f"  rows plan: {plan}")
        print(f"  moving one item rewrites: rows ~1 row;  blob 2 x {avg_blob:,.0f} bytes")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = args[0] if args else os.path.join(HERE, "schema.sql")
    with open(path) as f:
        schema = f.read()
    ok = tests(schema)
    if ok and "--tests-only" not in sys.argv:
        measure(schema)
    sys.exit(0 if ok else 1)
