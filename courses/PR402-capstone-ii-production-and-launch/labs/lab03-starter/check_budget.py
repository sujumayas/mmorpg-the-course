#!/usr/bin/env python3
"""PR402 lab 03: concurrent players, fleet size and the semester hosting budget.

Usage: python check_budget.py demand.csv budget.csv [--reserve 0.10]

Model (PR402 week 3, sections 3 and 4):
  DAU        = signups * launch_day_share
  avg CCU    = DAU * session_hours / 24
  peak       = avg CCU * peak_ratio;  launch peak = peak * launch_spike
  servers    = ceil(launch peak / (knee_per_zone_server * utilization))
  line cost  = dollars_per_hour * hours_per_week * weeks + fixed_dollars
Rules: zone_servers_launch >= servers; a staging line exists; every line outside production
       runs fewer than 168 hours a week; total <= grant * (1 - reserve); every demand input
       has a source.
"""
import argparse
import csv
import math
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("demand")
    ap.add_argument("budget")
    ap.add_argument("--reserve", type=float, default=0.10)
    a = ap.parse_args()
    rows = read(a.demand)
    d = {r["key"]: float(r["value"]) for r in rows}
    problems = [f"demand input {r['key']} has no source" for r in rows
                if r["key"] != "zone_servers_launch" and not r["source"].strip()]

    dau = d["signups"] * d["launch_day_share"]
    avg = dau * d["session_hours"] / 24
    peak = avg * d["peak_ratio"]
    launch = peak * d["launch_spike"]
    usable = d["knee_per_zone_server"] * d["utilization"]
    need = math.ceil(launch / usable - 1e-9)
    print(f"DAU {dau:.0f}  avg CCU {avg:.1f}  evening peak {peak:.1f}  launch peak {launch:.1f}")
    print(f"usable per zone server {usable:.0f} -> zone servers needed at launch {need}")
    if d["zone_servers_launch"] < need:
        problems.append(f"launch plan has {d['zone_servers_launch']:g} zone servers, needs {need}")

    total = 0.0
    envs = set()
    for b in read(a.budget):
        cost = (float(b["dollars_per_hour"]) * float(b["hours_per_week"]) * float(b["weeks"])
                + float(b["fixed_dollars"]))
        total += cost
        envs.add(b["environment"])
        print(f"  {b['line']:<32} {b['environment']:<11} {cost:8.2f}")
        if b["environment"] != "production" and float(b["hours_per_week"]) >= 168:
            problems.append(f"{b['line']}: {b['environment']} runs all week; schedule it")
    cap = d["grant_dollars"] * (1 - a.reserve)
    print(f"total {total:.2f}  grant {d['grant_dollars']:g}  limit with {a.reserve:.0%} reserve {cap:.2f}")
    if "staging" not in envs:
        problems.append("no staging environment in the budget")
    if total > cap + 1e-9:
        problems.append(f"total {total:.2f} is over the limit {cap:.2f} by {total - cap:.2f}")

    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
