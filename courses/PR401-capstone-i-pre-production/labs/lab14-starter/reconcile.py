#!/usr/bin/env python3
"""PR401 lab 14: replan production from the slice's measured unit costs. Standard library only.

Usage: python reconcile.py team.csv backlog.csv replan.csv

team.csv and backlog.csv are your lab 11 files (raw estimates, scaled by plan_ratio).
replan.csv  id,unit_type,u1,first_n,units,lr,measured_units,note
            id          the backlog item whose estimate the measurement replaces
            u1          measured per-unit ACTUAL hours of the first unit (one-time removed)
            first_n     unit number of the first production unit (2 if the slice made unit 1)
            units       production units planned
            lr          learning rate you plan with (1.0 = flat)
            measured_units  units of this type built so far at the quality bar

Replaced items use sum(u1 * n**log2(lr)) for n = first_n .. first_n + units - 1, in actual
hours (not scaled by plan_ratio, because u1 is already an actual). Prints each replaced
item at the planned rate and flat, the cumulative load per discipline at each milestone,
then PASS or NOT READY. Exits 1 when anything fails.
"""
import csv
import math
import sys

MILESTONES = ["S1", "S2", "S3", "S4"]
WEEKS_TO = {"S1": 1, "S2": 2, "S3": 3, "S4": 8}


def read(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def curve(u1, first, units, lr):
    b = math.log2(lr)
    return sum(u1 * n ** b for n in range(first, first + units))


def main(team_path, backlog_path, replan_path):
    problems = []
    team = {}
    for r in read(team_path):
        weekly = float(r["people"]) * float(r["hours_per_week"]) * float(r["focus_factor"])
        absent = float(r.get("absence_hours") or 0) * float(r["focus_factor"])
        team[r["discipline"]] = (weekly, absent, float(r["plan_ratio"]))
    items = {r["id"]: r for r in read(backlog_path)}
    replaced = {}
    print(f"{'id':<5}{'type':<12}{'old plan':>9}{'at lr':>8}{'flat':>8}  lr")
    for r in read(replan_path):
        rid = r["id"]
        if rid not in items:
            problems.append(f"replan {rid}: no such backlog item")
            continue
        u1, first, units = float(r["u1"]), int(r["first_n"]), int(r["units"])
        lr, measured = float(r["lr"]), int(r.get("measured_units") or 0)
        if not 0.5 <= lr <= 1.0:
            problems.append(f"replan {rid}: lr {lr} outside 0.5-1.0")
            continue
        if lr < 0.9 and measured < 2 and not r.get("note"):
            problems.append(f"replan {rid}: lr {lr} below 0.9 with fewer than 2 measured units needs a note with evidence")
        item = items[rid]
        old = float(item["hours"]) * team[item["discipline"]][2]
        new = curve(u1, first, units, lr)
        replaced[rid] = new
        print(f"{rid:<5}{r['unit_type']:<12}{old:>9.1f}{new:>8.1f}{curve(u1, first, units, 1.0):>8.1f}  {lr}")
    demand = {d: {m: 0.0 for m in MILESTONES} for d in team}
    for rid, it in items.items():
        d, m = it["discipline"], it["milestone"]
        if d not in team or m not in MILESTONES:
            problems.append(f"{rid}: unknown discipline or milestone")
            continue
        demand[d][m] += replaced.get(rid, float(it["hours"]) * team[d][2])
    print(f"{'discipline':<22}" + "".join(f"{'load@' + m:>9}" for m in MILESTONES))
    for d, (weekly, absent, _R) in team.items():
        cum, row = 0.0, []
        for m in MILESTONES:
            cum += demand[d][m]
            cap = weekly * WEEKS_TO[m] - absent * WEEKS_TO[m] / WEEKS_TO["S4"]
            load = cum / cap if cap > 0 else (float("inf") if cum else 0.0)
            row.append(load)
            if load > 1.0 + 1e-9:
                problems.append(f"{d}: cumulative load {load:.2f} at {m} (above 1.0)")
        print(f"{d:<22}" + "".join(f"{x:>9.2f}" for x in row))
    for p in dict.fromkeys(problems):
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
