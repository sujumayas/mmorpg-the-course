"""DB201 Lab 12 checker. Recomputes every KPI from the CSV files in plain Python
(no SQL) and compares with the answers in kpi.db produced by kpis.py.

Run:  python check_lab12.py
"""
import csv
import sqlite3
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import kpis

HERE = Path(__file__).resolve().parent
TOL = 1e-6


def reference():
    acc = {}
    with open(HERE / "accounts.csv") as f:
        for r in csv.DictReader(f):
            acc[int(r["account_id"])] = (int(r["person_id"]), r["install_day"], int(r["utc_offset_hours"]))
    days = defaultdict(lambda: defaultdict(set))   # kind -> day -> set of ids
    active = defaultdict(set)                       # utc day -> accounts
    with open(HERE / "sessions.csv") as f:
        for r in csv.DictReader(f):
            a = int(r["account_id"])
            t = datetime.strptime(r["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
            d = t.date().isoformat()
            local = (t + timedelta(hours=acc[a][2])).date().isoformat()
            days["dau_utc"][d].add(a)
            active[d].add(a)
            if int(r["minutes"]) >= 5:
                days["dau_5min"][d].add(a)
            days["dau_local"][local].add(a)
            days["dau_person"][d].add(acc[a][0])
    ref = {k: [(d, len(s)) for d, s in sorted(v.items())] for k, v in days.items()}

    last = date.fromisoformat(kpis.LAST_DAY)
    window = [(last - timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    mau = len(set().union(*(active[d] for d in window)))
    avg = sum(len(active[d]) for d in window) / 30
    ref["mau_last30"] = [(mau,)]
    ref["stickiness_last30"] = [(avg, mau, avg / mau)]

    cohorts = defaultdict(list)
    for a, (_, inst, _) in acc.items():
        cohorts[inst].append(a)
    ret = []
    for inst in sorted(cohorts):
        d0 = date.fromisoformat(inst)
        if d0 + timedelta(days=7) > last:
            continue
        c = cohorts[inst]
        d1 = sum(a in active[(d0 + timedelta(days=1)).isoformat()] for a in c) / len(c)
        d7 = sum(a in active[(d0 + timedelta(days=7)).isoformat()] for a in c) / len(c)
        ret.append((inst, len(c), d1, d7))
    ref["retention"] = ret
    return ref


def same(a, b):
    if len(a) != len(b):
        return False
    for ra, rb in zip(a, b):
        if len(ra) != len(rb):
            return False
        for x, y in zip(ra, rb):
            if isinstance(y, float) or isinstance(x, float):
                if x is None or abs(float(x) - float(y)) > TOL:
                    return False
            elif x != y:
                return False
    return True


def main():
    con = sqlite3.connect(":memory:")
    kpis.load(con)
    ref = reference()
    ok = True
    for name, sql in kpis.QUERIES.items():
        if sql is None:
            print(f"TODO {name}")
            ok = False
            continue
        rows = [tuple(r) for r in con.execute(sql).fetchall()]
        if same(rows, ref[name]):
            print(f"PASS {name}")
        else:
            ok = False
            print(f"FAIL {name}: got {rows[:2]}... expected {ref[name][:2]}...")
    s = ref["stickiness_last30"][0]
    print(f"\nreference: MAU {s[1]:,}, mean DAU {s[0]:.1f}, stickiness {s[2]:.3f}; "
          f"sum of the 30 DAUs {s[0] * 30:,.0f} (not the MAU)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
