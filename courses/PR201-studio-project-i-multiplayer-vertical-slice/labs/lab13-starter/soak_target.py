#!/usr/bin/env python3
"""PR201 lab 13: showcase reliability target and soak progress. Standard library only.

Usage: python soak_target.py soak_plan.csv soak_log.csv

Model (PR201 week 13, section 3):
  lambda_max = -ln(R) / S                     largest tolerable crash rate per server-hour
  T_needed   = factor(k) / lambda_max         factor = exact 95% Poisson upper bound for k crashes
                                              (2.996, 4.744, 6.296, 7.754 for k = 0..3)
Only log rows for the current build (the plan's build_tag) count. k is the crashes on that build.
PASS when the logged hours reach T_needed. ON TRACK when logged plus booked hours reach it.
The plan must record R and the date it was set, on or before the first soak on this build.
"""
import csv
import sys
from datetime import date
from math import exp, factorial, log


def upper_count(k, conf=0.95):
    """95% upper bound on a Poisson mean after seeing k events, by bisection."""
    lo, hi = 0.0, 50.0
    for _ in range(100):
        mid = (lo + hi) / 2
        cdf = sum(exp(-mid) * mid ** i / factorial(i) for i in range(k + 1))
        lo, hi = (mid, hi) if cdf > 1 - conf else (lo, mid)
    return lo


FACTOR = [upper_count(k) for k in range(4)]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = []
    with open(sys.argv[1], newline="") as f:
        plan = {r["key"].strip(): r["value"].strip() for r in csv.DictReader(f)}
    for k in ("S", "R", "R_set_on", "build_tag", "booked_hours"):
        if not plan.get(k):
            problems.append(f"plan: {k} missing")
    if problems:
        for p in problems:
            print("FAIL:", p)
        print("NOT READY")
        sys.exit(1)
    S, R, booked = float(plan["S"]), float(plan["R"]), float(plan["booked_hours"])
    tag = plan["build_tag"]
    with open(sys.argv[2], newline="") as f:
        log_rows = [r for r in csv.DictReader(f) if r["date"].strip()]
    rows = [r for r in log_rows if r["build_tag"].strip() == tag]
    hours = sum(float(r["hours"]) for r in rows)
    k = sum(int(r["crashes"]) for r in rows)
    lam = -log(R) / S
    print(f"S = {S} h, R = {R}, lambda_max = {lam:.4f} per hour")
    if k >= len(FACTOR):
        problems.append(f"{k} crashes on {tag}: fix the crashes and soak a new build")
        needed = float("inf")
    else:
        needed = FACTOR[k] / lam
    print(f"build {tag}: {hours:.1f} h logged, {k} crash(es), {needed:.1f} h needed, {booked:.1f} h booked")
    if rows:
        first = min(date.fromisoformat(r["date"].strip()) for r in rows)
        if date.fromisoformat(plan["R_set_on"]) > first:
            problems.append("R was set after the first soak on this build")
    for r in rows:
        if not r["route_version"].strip():
            problems.append(f"log {r['date']}: route_version missing")
    for p in problems:
        print("FAIL:", p)
    if problems:
        print("NOT READY")
        sys.exit(1)
    if hours >= needed:
        print("PASS")
    elif hours + booked >= needed:
        print(f"ON TRACK: {needed - hours:.1f} h still to run")
    else:
        print(f"NOT READY: short by {needed - hours - booked:.1f} h even with booked nights")
        sys.exit(1)


if __name__ == "__main__":
    main()
