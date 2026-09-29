#!/usr/bin/env python3
"""PR201 lab 06: check a sprint 2 plan. Standard library only.

Usage: python check_sprint_plan.py forecast.csv backlog.csv [--tolerance 0.10]

Model (PR201 week 6, section 4):
  f        = s1_done_estimate_h / s1_useful_h        (yesterday's weather, week 5's focus factor)
  forecast = f * s2_useful_h
  q        = s1_stories_done / s1_stories_committed  (rough per-story finish rate)
  P(chain) = q ** k                                  (k = stories marked on_chain)

Rules checked:
  1. Committed hours (above_line = y) are at most forecast * (1 + tolerance).
  2. Every committed story's dependencies are committed too, or 'sprint1' (already done).
  3. The chain (on_chain = y) is non-empty, fully committed and closed: every dependency of a
     chain story is another chain story or 'sprint1'.
  4. Every committed story has an owner and acceptance criteria.
  5. The committed stories cover every loop role in required_roles (the sprint goal's loop).
  6. The forecast file has a sprint goal.
Prints PASS or NOT READY and exits 1 when anything fails.
"""
import argparse
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def deps(row):
    return [d.strip() for d in row["depends_on"].replace(",", ";").split(";") if d.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("forecast")
    ap.add_argument("backlog")
    ap.add_argument("--tolerance", type=float, default=0.10)
    a = ap.parse_args()
    kv = {r["key"]: r["value"] for r in read(a.forecast)}
    rows = read(a.backlog)
    problems = []

    f = float(kv["s1_done_estimate_h"]) / float(kv["s1_useful_h"])
    forecast = f * float(kv["s2_useful_h"])
    q = float(kv["s1_stories_done"]) / float(kv["s1_stories_committed"])
    print(f"focus f = {f:.3f}   forecast = {forecast:.1f} estimated hours   per-story q = {q:.2f}")

    ids = {r["id"] for r in rows}
    above = [r for r in rows if r["above_line"].strip().lower() == "y"]
    above_ids = {r["id"] for r in above}
    committed = sum(float(r["estimate_h"]) for r in above)
    print(f"committed = {committed:.1f} h across {len(above)} stories")
    if committed > forecast * (1 + a.tolerance):
        problems.append(f"committed {committed:.1f} h exceeds forecast {forecast:.1f} h by more than {a.tolerance:.0%}")

    for r in above:
        for d in deps(r):
            if d == "sprint1":
                continue
            if d not in ids:
                problems.append(f"{r['id']} depends on unknown story {d}")
            elif d not in above_ids:
                problems.append(f"{r['id']} is committed but its dependency {d} is below the line")
        if not r["owner"].strip():
            problems.append(f"{r['id']} has no owner")
        if not r["acceptance"].strip():
            problems.append(f"{r['id']} has no acceptance criteria")

    chain = [r for r in rows if r["on_chain"].strip().lower() == "y"]
    chain_ids = {r["id"] for r in chain}
    if not chain:
        problems.append("no stories marked on_chain = y")
    for r in chain:
        if r["id"] not in above_ids:
            problems.append(f"chain story {r['id']} is below the line")
        for d in deps(r):
            if d != "sprint1" and d not in chain_ids:
                problems.append(f"chain story {r['id']} depends on {d}, which is not on the chain")
    k = len(chain)
    print(f"chain: {', '.join(sorted(chain_ids)) or '-'}   k = {k}   P(chain) = q^k = {q ** k:.2f}")

    need = [x.strip() for x in kv.get("required_roles", "").split(";") if x.strip()]
    have = {r.get("loop_role", "").strip() for r in above}
    missing = [x for x in need if x not in have]
    if not need:
        problems.append("forecast.csv has no required_roles")
    elif missing:
        problems.append("the committed stories do not form the loop; missing roles: " + ", ".join(missing))

    if not kv.get("sprint_goal", "").strip():
        problems.append("forecast.csv has no sprint_goal")

    if problems:
        for p in problems:
            print("  -", p)
        print("NOT READY")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
