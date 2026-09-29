#!/usr/bin/env python3
"""PR402 lab 01: capacity to alpha and content lock under an ops tax.

Usage: python check_capacity.py history.csv plan.csv backlog.csv [--band 0.2]

Model (PR402 week 1, section 4):
  r   = done points / available hours           (PR401 slice sprints)
  c_w = r * H_w * (1 - t_w)                     t_w = measured tax if given, else planned
  F   = sum c_w over feature weeks, C = sum c_w over content weeks
Rules: kept points <= budget in each phase; trigger points cover the gap between the budget
       and its low value, budget * (1 - band); every cut or trigger row has a pillar check;
       taxes >= 0.1 in feature weeks and >= 0.3 in content weeks.
"""
import argparse
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("history")
    ap.add_argument("plan")
    ap.add_argument("backlog")
    ap.add_argument("--band", type=float, default=0.2)
    a = ap.parse_args()
    hist, plan, items = read(a.history), read(a.plan), read(a.backlog)
    problems = []

    pts = sum(float(h["done_points"]) for h in hist)
    hrs = sum(float(h["available_hours"]) for h in hist)
    r = pts / hrs
    print(f"rate r = {pts:g} / {hrs:g} = {r:.3f} points per hour")

    budget = {"feature": 0.0, "content": 0.0}
    for w in plan:
        measured = w["measured_tax"].strip()
        t = float(measured) if measured else float(w["planned_tax"])
        floor = 0.1 if w["phase"] == "feature" else 0.3
        if t < floor:
            problems.append(f"week {w['week']}: tax {t:.2f} below {floor} for a {w['phase']} week")
        c = r * float(w["available_hours"]) * (1 - t)
        budget[w["phase"]] += c
        src = "measured" if measured else "planned"
        print(f"week {w['week']:>2} {w['phase']:<8} tax {t:.2f} ({src})  backlog points {c:5.1f}")

    for phase in ("feature", "content"):
        rows = [i for i in items if i["type"] == phase]
        keep = sum(float(i["points"]) for i in rows if i["decision"] == "keep")
        trig = sum(float(i["points"]) for i in rows if i["decision"] == "trigger")
        cut = sum(float(i["points"]) for i in rows if i["decision"] == "cut")
        b = budget[phase]
        low = b * (1 - a.band)
        print(f"{phase:<8} budget {b:5.1f} (low {low:5.1f})  keep {keep:g}  trigger {trig:g}  cut {cut:g}")
        if keep > b + 0.05:
            problems.append(f"{phase}: kept {keep:g} points exceed budget {b:.1f}")
        if trig + 0.05 < min(keep, b) - low:
            problems.append(f"{phase}: trigger items {trig:g} do not cover budget - low = {b - low:.1f}")
    for i in items:
        if i["decision"] not in ("keep", "trigger", "cut"):
            problems.append(f"{i['id']}: decision must be keep, trigger or cut")
        if i["decision"] in ("trigger", "cut") and not i["pillar_check"].strip():
            problems.append(f"{i['id']}: {i['decision']} without a pillar check")

    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
