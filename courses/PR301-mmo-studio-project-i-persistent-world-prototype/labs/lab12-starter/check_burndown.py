#!/usr/bin/env python3
"""PR301 lab 12: check the sprint 5 burn-down, the day-3 cut and the encounter numbers.
Standard library only.

Usage: python check_burndown.py backlog.csv burndown.csv encounter.csv pulls.csv

Model (PR301 week 12, sections 3 to 5):
  r_avg    = (commit + added so far - remaining) / t
  r_recent = (remaining at t-2 - remaining at t + added on days t-1 and t) / 2
  cut_needed = max(0, remaining - min(r_avg, r_recent) x (5 - t)), with t = 3
  Items with status "cut" must be marked minimum = no and must save at least cut_needed.
  (A replacement item, status "remaining" with a note starting "replaces", adds its hours back.)
  Encounter: H must be within 1% of D x T_target x u; the sheet's D_min must match H / (T_enrage x u).
  Pulls: every row needs a build id and a question.
"""
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    problems = []
    items = read(sys.argv[1])
    commit = sum(float(r["hours"]) for r in items if r["planned"].strip().lower() == "yes")
    days = {int(r["day"]): r for r in read(sys.argv[2])}
    t = 3
    if not all(d in days and days[d]["remaining"].strip() for d in range(0, t + 1)):
        sys.exit("burndown.csv needs remaining for days 0 to 3")
    R = {d: float(days[d]["remaining"]) for d in range(0, t + 1)}
    add = {d: float(days[d]["added"] or 0) for d in range(0, t + 1)}
    if abs(R[0] - commit) > 1e-9:
        problems.append(f"day 0 remaining {R[0]:g} differs from planned commit {commit:g}")
    r_avg = (commit + sum(add.values()) - R[t]) / t
    r_rec = (R[t - 2] - R[t] + add[t - 1] + add[t]) / 2
    left_avg, left_rec = R[t] - r_avg * (5 - t), R[t] - r_rec * (5 - t)
    need = max(0.0, left_avg, left_rec)
    print(f"commit {commit:g}  r_avg {r_avg:.2f}  r_recent {r_rec:.2f}")
    print(f"projected left: average {left_avg:.2f}, recent {left_rec:.2f}  cut needed {need:.2f}")
    cut = sum(float(r["hours"]) for r in items if r["status"].strip().lower() == "cut")
    back = sum(float(r["hours"]) for r in items
               if r["note"].strip().lower().startswith("replaces"))
    saved = cut - back
    print(f"cut {cut:g}, replacements {back:g}, saved {saved:g}")
    if saved + 1e-9 < need:
        problems.append(f"saved {saved:g} hours, need at least {need:.2f}")
    for r in items:
        if r["status"].strip().lower() == "cut" and r["minimum"].strip().lower() != "no":
            problems.append(f"{r['id']}: cut, but marked minimum = {r['minimum']}")
    e = {r["key"].strip(): float(r["value"]) for r in read(sys.argv[3]) if r["value"].strip()}
    for k in ("D", "u", "T_target", "H", "T_enrage", "D_min"):
        if k not in e:
            problems.append(f"encounter.csv: missing {k}")
    if all(k in e for k in ("D", "u", "T_target", "H", "T_enrage", "D_min")):
        H_model = e["D"] * e["T_target"] * e["u"]
        D_min = e["H"] / (e["T_enrage"] * e["u"])
        T = e["H"] / (e["D"] * e["u"])
        print(f"H model {H_model:.0f} (sheet {e['H']:.0f})  kill time {T:.1f} s  "
              f"margin {e['T_enrage'] / T - 1:.1%}  D_min {D_min:.1f} = {D_min / e['D']:.0%} of D")
        if abs(e["H"] - H_model) > 0.01 * H_model:
            problems.append("H is more than 1% away from D x T_target x u")
        if abs(e["D_min"] - D_min) > 0.5:
            problems.append(f"D_min on the sheet should be {D_min:.1f}")
    pulls = read(sys.argv[4])
    for i, p in enumerate(pulls, 1):
        if not p["build"].strip() or not p["question"].strip():
            problems.append(f"pull {i}: needs a build id and a question")
    print(f"{len(pulls)} pulls logged")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
