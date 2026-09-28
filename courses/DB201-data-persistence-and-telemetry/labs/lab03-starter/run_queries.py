"""DB201 Lab 03 checker: runs queries/qNN.sql against game.db and compares results.

Run:  python run_queries.py          # all queries
      python run_queries.py 6        # only q06
The expected answers are computed in plain Python from the generator, not from SQL,
so a query that "looks right" but double counts will fail.
"""
import os
import sqlite3
import sys
from collections import Counter, defaultdict

import build_db

HERE = os.path.dirname(os.path.abspath(__file__))
QDIR = os.path.join(HERE, "queries")


def expected():
    types, chars, items, quests = build_db.generate()
    tmap = {t[0]: t for t in types}
    cmap = {c[0]: c for c in chars}
    exp = {}

    n_by_class = Counter(c[2] for c in chars)
    exp[1] = sorted(n_by_class.items(), key=lambda kv: (-kv[1], kv[0]))

    exp[2] = sorted(((c[1], c[4]) for c in chars), key=lambda r: (-r[1], r[0]))[:5]

    qty_by_rarity = Counter()
    for it in items:
        qty_by_rarity[tmap[it[1]][2]] += it[5]
    exp[3] = sorted(qty_by_rarity.items())

    owners = {it[2] for it in items}
    exp[4] = [(sum(1 for c in chars if c[0] not in owners),)]

    gold = Counter()
    for c in chars:
        gold[c[2]] += c[4]
    exp[5] = sorted(gold.items())

    item_rows, quest_rows = Counter(), Counter()
    for it in items:
        item_rows[cmap[it[2]][2]] += 1
    for q in quests:
        quest_rows[cmap[q[0]][2]] += 1
    exp[6] = sorted((k, gold[k], item_rows[k], quest_rows[k]) for k in gold)

    value = Counter()
    for it in items:
        value[cmap[it[2]][1]] += it[5] * tmap[it[1]][4]
    exp[7] = sorted(value.items(), key=lambda r: (-r[1], r[0]))[:5]

    levels = defaultdict(list)
    for c in chars:
        levels[c[2]].append(c[3])
    exp[8] = sorted((k, round(sum(v) / len(v), 1)) for k, v in levels.items() if len(v) > 250)
    return exp


def normalize(rows):
    return [tuple(round(x, 1) if isinstance(x, float) else x for x in r) for r in rows]


def main():
    if not os.path.exists(build_db.DB_PATH):
        build_db.build()
    only = {int(a) for a in sys.argv[1:]}
    exp = expected()
    con = sqlite3.connect(build_db.DB_PATH)
    passed = 0
    for n in sorted(exp):
        if only and n not in only:
            continue
        path = os.path.join(QDIR, f"q{n:02d}.sql")
        sql = open(path).read() if os.path.exists(path) else ""
        body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--")).strip()
        if not body:
            print(f"q{n:02d}  TODO")
            continue
        try:
            got = normalize(con.execute(body).fetchall())
        except sqlite3.Error as e:
            print(f"q{n:02d}  ERROR {e}")
            continue
        want = normalize(exp[n])
        if got == want:
            passed += 1
            print(f"q{n:02d}  OK")
        else:
            print(f"q{n:02d}  FAIL")
            print(f"      want (first 5): {want[:5]}")
            print(f"      got  (first 5): {got[:5]}")
    total = len(only) if only else len(exp)
    print(f"{passed}/{total} queries correct")
    return passed == total


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
