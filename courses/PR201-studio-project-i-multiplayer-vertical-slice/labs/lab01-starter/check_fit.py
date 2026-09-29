#!/usr/bin/env python3
"""PR201 lab 01: does a pitch fit the team? Standard library only.

Usage: python check_fit.py team.csv pitch_demand.csv [--weeks 11] [--c 0.25] [--buffer 0.3]

Model (PR201 week 1, section 2):
  useful_i = (hours_per_week_i - c * (n - 1)) * weeks     coordination from the PR101 channel model
  supply_d = sum over members whose primary is d of (1 - buffer) * useful_i
  load_d   = demand_d / supply_d
  the pitch fits when max_d load_d <= 1 AND every discipline has a primary and a backup
"""
import argparse
import csv
import sys

DISCIPLINES = ["code", "design", "art", "audio", "production"]


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def supply(team, weeks, c, buffer):
    n = len(team)
    out = {d: 0.0 for d in DISCIPLINES}
    for m in team:
        useful = (float(m["hours_per_week"]) - c * (n - 1)) * weeks
        out[m["primary"].strip()] += (1 - buffer) * useful
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("team")
    ap.add_argument("demand")
    ap.add_argument("--weeks", type=float, default=11)
    ap.add_argument("--c", type=float, default=0.25)
    ap.add_argument("--buffer", type=float, default=0.3)
    a = ap.parse_args()
    team, demand = read(a.team), read(a.demand)
    problems = []
    for m in team:
        for col in ("primary", "backup"):
            if m[col].strip() not in DISCIPLINES:
                problems.append(f"{m['member']}: unknown {col} '{m[col]}'")
        if m["primary"].strip() == m["backup"].strip():
            problems.append(f"{m['member']}: backup must differ from primary")
    for d in DISCIPLINES:
        if not any(m["primary"].strip() == d for m in team):
            problems.append(f"no primary for {d}")
        if not any(m["backup"].strip() == d for m in team):
            problems.append(f"no backup for {d} (bus factor 1)")
    sup = supply(team, a.weeks, a.c, a.buffer)
    need = {r["discipline"].strip(): float(r["hours"]) for r in demand}
    print(f"{'discipline':<11}{'supply':>8}{'demand':>8}{'load':>7}")
    worst = 0.0
    for d in DISCIPLINES:
        s, q = sup[d], need.get(d, 0.0)
        load = q / s if s else float("inf") if q else 0.0
        worst = max(worst, load)
        flag = "  <- over" if load > 1 else ""
        print(f"{d:<11}{s:8.1f}{q:8.1f}{load:7.2f}{flag}")
    ts, tq = sum(sup.values()), sum(need.values())
    print(f"{'total':<11}{ts:8.1f}{tq:8.1f}{tq / ts:7.2f}")
    print(f"max load {worst:.2f}")
    if worst > 1:
        problems.append(f"max load {worst:.2f} > 1: cut or move work in the bottleneck discipline")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
