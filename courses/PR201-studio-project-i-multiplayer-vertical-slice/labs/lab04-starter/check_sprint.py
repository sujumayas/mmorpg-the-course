#!/usr/bin/env python3
"""PR201 lab 04: check a sprint plan and forecast from the daily log. Standard library only.

Usage: python check_sprint.py availability.csv backlog.csv [daily.csv] [--day 6] [--weeks 2]
       [--c 0.25] [--focus 0.7] [--max-task 4] [--days 10]

Model (PR201 week 4, section 2):
  limit_i  = focus * (hours_available_i - c * (n - 1) * weeks)   per-person commitment limit
  limit    = sum of limit_i
  done[d]  = scope[d] - remaining[d]                             burn-up
  burn-down forecast at day k: remaining[k] - (remaining[0] - remaining[k]) / k * (days - k)
  burn-up forecast at day k:   scope[k] - done[k] - done[k] / k * (days - k)
"""
import argparse
import csv
import sys


def read(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("availability")
    ap.add_argument("backlog")
    ap.add_argument("daily", nargs="?")
    ap.add_argument("--day", type=int, default=6)
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--weeks", type=float, default=2)
    ap.add_argument("--c", type=float, default=0.25)
    ap.add_argument("--focus", type=float, default=0.7)
    ap.add_argument("--max-task", type=float, default=4)
    a = ap.parse_args()
    avail, tasks = read(a.availability), read(a.backlog)
    n = len(avail)
    problems = []
    lim = {m["member"]: a.focus * (float(m["hours_available"]) - a.c * (n - 1) * a.weeks) for m in avail}
    load = {m: 0.0 for m in lim}
    for t in tasks:
        e = float(t["estimate_h"])
        if e > a.max_task:
            problems.append(f"{t['id']}: {e:g} h is over {a.max_task:g} h, split it")
        if t["owner"] not in lim:
            problems.append(f"{t['id']}: owner '{t['owner']}' not in availability")
        else:
            load[t["owner"]] += e
        if not t["acceptance"].strip():
            problems.append(f"{t['id']}: no acceptance test")
        if t["goal"].strip() not in ("y", "n"):
            problems.append(f"{t['id']}: goal must be y or n")
    print(f"{'member':<8}{'limit':>7}{'load':>7}")
    for m in lim:
        flag = "  <- over" if load[m] > lim[m] + 1e-9 else ""
        print(f"{m:<8}{lim[m]:7.2f}{load[m]:7.1f}{flag}")
        if flag:
            problems.append(f"{m} committed {load[m]:g} h over limit {lim[m]:.2f}")
    tl, tc = sum(lim.values()), sum(load.values())
    goal_h = sum(float(t["estimate_h"]) for t in tasks if t["goal"].strip() == "y")
    print(f"team limit {tl:.2f} h, committed {tc:g} h, sprint-goal tasks {goal_h:g} h")
    if tc > tl + 1e-9:
        problems.append("team commitment over limit")
    if a.daily:
        rows = read(a.daily)
        print(f"{'day':>4}{'remain':>8}{'scope':>7}{'done':>6}")
        for r in rows:
            rem, sc = float(r["remaining_h"]), float(r["scope_h"])
            print(f"{int(r['day']):4d}{rem:8g}{sc:7g}{sc - rem:6g}")
        k = a.day
        r0, rk = float(rows[0]["remaining_h"]), float(rows[k]["remaining_h"])
        sk = float(rows[k]["scope_h"])
        dk = sk - rk
        bd = rk - (r0 - rk) / k * (a.days - k)
        bu = sk - dk - dk / k * (a.days - k)
        print(f"at day {k}: burn-down slope {(r0 - rk) / k:.3f} h/day -> {bd:.1f} h left at day {a.days}")
        print(f"at day {k}: burn-up rate {dk / k:.3f} h/day -> {bu:.1f} h left at day {a.days} (if scope holds)")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
