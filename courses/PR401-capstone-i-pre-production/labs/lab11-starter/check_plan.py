#!/usr/bin/env python3
"""PR401 lab 11: production plan checker. Standard library only.

Usage: python check_plan.py team.csv backlog.csv

team.csv    discipline,people,hours_per_week,focus_factor,absence_hours,plan_ratio
            (focus_factor and plan_ratio are the measured week 6 values)
backlog.csv id,item,discipline,owner,milestone,hours,depends_on
            hours are raw estimates; the checker multiplies them by plan_ratio.
            milestone is one of S1, S2, S3, S4 (PR402 weeks 1, 2, 3 and 4-8).
            depends_on lists ids separated by ';' (may be empty).

Prints capacity and cumulative load per discipline at each milestone,
then PASS or NOT READY. Exits 1 when anything fails.
"""
import csv
import sys

MILESTONES = ["S1", "S2", "S3", "S4"]
WEEKS_TO = {"S1": 1, "S2": 2, "S3": 3, "S4": 8}   # cumulative PR402 weeks
W = WEEKS_TO["S4"]


def read(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main(team_path, backlog_path):
    problems = []
    team = {}
    for r in read(team_path):
        d = r["discipline"]
        n, h, f = float(r["people"]), float(r["hours_per_week"]), float(r["focus_factor"])
        absent = float(r.get("absence_hours") or 0)
        R = float(r["plan_ratio"])
        if not 0 < f <= 1:
            problems.append(f"{d}: focus_factor {f} must be between 0 and 1")
        if R < 1:
            problems.append(f"{d}: plan_ratio {R} below 1.0; estimates rarely run early as a whole")
        team[d] = (n * h * f, absent * f, R)
    items = read(backlog_path)
    ids = {r["id"]: r for r in items}
    demand = {d: {m: 0.0 for m in MILESTONES} for d in team}
    for r in items:
        rid = r["id"]
        for field in ("item", "discipline", "owner", "milestone", "hours"):
            if not r.get(field):
                problems.append(f"{rid}: missing {field}")
        if r.get("discipline") and r["discipline"] not in team:
            problems.append(f"{rid}: discipline '{r['discipline']}' not in team.csv")
            continue
        if r.get("milestone") not in MILESTONES:
            problems.append(f"{rid}: milestone must be one of {MILESTONES}")
            continue
        try:
            demand[r["discipline"]][r["milestone"]] += float(r["hours"]) * team[r["discipline"]][2]
        except ValueError:
            problems.append(f"{rid}: hours is not a number")
        for dep in filter(None, (x.strip() for x in r.get("depends_on", "").split(";"))):
            if dep not in ids:
                problems.append(f"{rid}: depends on unknown id {dep}")
            elif MILESTONES.index(ids[dep].get("milestone", "S4") if ids[dep].get("milestone") in MILESTONES else "S4") > MILESTONES.index(r["milestone"]):
                problems.append(f"{rid} ({r['milestone']}) depends on {dep} ({ids[dep]['milestone']}), scheduled later")
    print(f"{'discipline':<22}{'capacity':>9}  " + "  ".join(f"{'load@' + m:>8}" for m in MILESTONES))
    team_c = team_d = 0.0
    worst = (0, None)
    for d, (weekly, absent, _R) in team.items():
        row, cum = [], 0.0
        for m in MILESTONES:
            cum += demand[d][m]
            cap = weekly * WEEKS_TO[m] - absent * WEEKS_TO[m] / W
            load = cum / cap if cap > 0 else float("inf") if cum else 0.0
            row.append(load)
            if load > 1.0 + 1e-9:
                problems.append(f"{d}: cumulative load {load:.2f} at {m} (above 1.0)")
        cap_total = weekly * W - absent
        team_c += cap_total
        team_d += cum
        if row[-1] > worst[0]:
            worst = (row[-1], d)
        print(f"{d:<22}{cap_total:>9.1f}  " + "  ".join(f"{x:>8.2f}" for x in row))
    print(f"team load {team_d / team_c:.2f}  (hides the constraint; don't plan with it)")
    print(f"constraint: {worst[1]} at {worst[0]:.2f}, needs {worst[0] * W:.1f} of {W} weeks")
    for p in dict.fromkeys(problems):
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
