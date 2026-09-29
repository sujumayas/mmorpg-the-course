#!/usr/bin/env python3
"""PR201 lab 08: check a sprint 3 content budget against XP, time and hours. Standard library only.

Usage: python check_content_budget.py unit_cost.csv curve.csv capacity.csv plan.csv

Model (PR201 week 8, sections 3 and 4). Every hour is an estimated hour.
  f          = done_estimate_h / useful_h_done                 focus over the sprints so far
  forecast   = floor(f * useful_h)                             yesterday's weather, whole hours
  r_content  = sum(actual_h) / sum(estimate_h)                 from the room built in sprint 2
  k          = r_content / team_ratio                          content overrun beyond the team's
  XP needed  = sum(xp_to_next) over the curve rows              (reach the level after the last row)
  XP supply  = sum(packs) * xp_per_pack + sum(extra_xp)
  minutes    = sum(minutes)
  hours      = k * sum(estimate_h) over items that are not 'existing'
  capacity   = forecast - bug_reserve_h - systems_h            (both at their estimates)
Balances:
  XP     supply >= needed
  time   |minutes - target| <= tolerance * target
  hours  hours <= capacity
Prints PASS when all three hold, otherwise NOT READY, and exits 1.
"""
import csv
import math
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    unit, curve, cap, plan = (read(p) for p in sys.argv[1:])
    kv = {r["key"]: float(r["value"]) for r in cap}

    est = sum(float(r["estimate_h"]) for r in unit)
    act = sum(float(r["actual_h"]) for r in unit)
    r_content = act / est
    k = r_content / kv["team_ratio"]
    f = kv["done_estimate_h"] / kv["useful_h_done"]
    forecast = math.floor(f * kv["useful_h"] + 1e-9)
    print(f"unit cost: estimate {est:g} h, actual {act:g} h, content ratio {r_content:.2f}")
    print(f"team ratio {kv['team_ratio']:.2f}, content factor k = {k:.2f}")
    print(f"focus f = {f:.3f}, forecast = {f:.3f} x {kv['useful_h']:g} = {f * kv['useful_h']:.1f}, "
          f"planned as {forecast} estimate-hours")

    need = sum(float(r["xp_to_next"]) for r in curve)
    target_level = max(int(r["level"]) for r in curve) + 1
    packs = sum(int(r["packs"]) for r in plan)
    supply = packs * kv["xp_per_pack"] + sum(float(r["extra_xp"]) for r in plan)
    minutes = sum(float(r["minutes"]) for r in plan)
    hours = k * sum(float(r["estimate_h"]) for r in plan if r["kind"].strip() != "existing")
    capacity = forecast - kv["bug_reserve_h"] - kv["systems_h"]
    target, tol = kv["target_minutes"], kv["time_tolerance"]

    print(f"\n{'item':<32}{'kind':<10}{'planned h':>10}{'packs':>7}{'min':>6}")
    for r in plan:
        h = 0.0 if r["kind"].strip() == "existing" else float(r["estimate_h"]) * k
        print(f"{r['item']:<32}{r['kind']:<10}{h:>10.1f}{int(r['packs']):>7}{float(r['minutes']):>6g}")

    checks = [
        ("XP", supply >= need, f"supply {supply:g} XP vs {need:g} needed for level {target_level}"),
        ("time", abs(minutes - target) <= tol * target + 1e-9, f"{minutes:g} min vs target {target:g} (+/- {tol:.0%})"),
        ("hours", hours <= capacity + 1e-9, f"{hours:.1f} estimate-h vs content capacity {capacity:g} estimate-h"),
    ]
    print()
    for name, ok, msg in checks:
        print(f"{name:<6} {'holds' if ok else 'FAILS'}  {msg}")
    if all(ok for _, ok, _ in checks):
        print("PASS")
    else:
        print("NOT READY")
        sys.exit(1)


if __name__ == "__main__":
    main()
