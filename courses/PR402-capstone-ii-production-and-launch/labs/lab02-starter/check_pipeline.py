#!/usr/bin/env python3
"""PR402 lab 02: content pipeline throughput, bottleneck and WIP.

Usage: python check_pipeline.py pipeline.csv params.csv

Model (PR402 week 2, section 4):
  m_s = hours_per_week / hours_per_item     capacity of stage s, items per week
  X   = min m_s                             throughput; the argmin is the bottleneck
  W   = wip_limit / X                       Little's law lead time, weeks
  N   = floor(X * weeks_to_content_lock)    items finished by content lock
Rules: every stage has an owner and a source for hours_per_item; W <= 2 weeks;
       if N * minutes_per_item < target_minutes, gap_decision must say what closes the gap.
"""
import csv
import math
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    stages = read(sys.argv[1])
    params = {r["key"]: r["value"].strip() for r in read(sys.argv[2])}
    problems = []

    cap = {}
    for s in stages:
        h, k = float(s["hours_per_week"]), float(s["hours_per_item"])
        cap[s["stage"]] = h / k
        print(f"{s['stage']:<10} {s['owner']:<16} {h:5g} h/wk / {k:4g} h/item = {h / k:5.2f} items/wk")
        if not s["owner"].strip():
            problems.append(f"{s['stage']}: no owner")
        if not s["source"].strip():
            problems.append(f"{s['stage']}: no source for hours_per_item (timed item, log, estimate)")

    x = min(cap.values())
    neck = min(cap, key=cap.get)
    weeks = float(params["weeks_to_content_lock"])
    wip = float(params["wip_limit"])
    mins = float(params["minutes_per_item"])
    target = float(params["target_minutes"])
    lead = wip / x
    n = math.floor(x * weeks + 1e-9)
    print(f"bottleneck {neck}, throughput X = {x:.2f} items/wk")
    print(f"WIP {wip:g} -> lead time W = {lead:.1f} weeks")
    print(f"forecast {n} items by content lock = {n * mins:g} minutes (target {target:g})")

    if lead > 2 + 1e-9:
        problems.append(f"lead time {lead:.1f} weeks is over 2; lower the WIP limit to {math.floor(2 * x)} or less")
    if n * mins < target and not params.get("gap_decision"):
        problems.append(f"forecast is {target - n * mins:g} minutes short and gap_decision is empty")

    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
