#!/usr/bin/env python3
"""UX201 Lab 03 starter: estimate challenge ratios from a playtest log and apply the strain rule.

Standard library only. Run:
    python3 flow_strain.py flow_log.csv            # uses Q = 3, band 0.8-1.25
    python3 flow_strain.py flow_log.csv --q 5 --intended 2

Input CSV columns (one row per tester per level attempted):
    tester, level, deaths, cleared, minutes, rating, stopped_here
    - deaths: deaths or failed attempts on this level
    - cleared: 1 if the tester cleared the level, 0 if they stopped on it
    - minutes: time spent on the level
    - rating: post-level answer, one of easy / right / hard (may be blank)
    - stopped_here: 1 if the tester stopped or asked to stop during/after this level

Model (UX201 week 3, section 3):
    R_hat = deaths / intended     (intended = deaths per clear the designer wants; default 1)
    zone  = bored if R_hat < lo, anxious if R_hat > hi, else flow
    strain: +1 outside the band, else max(0, strain - 1); predicted quit when strain reaches Q
A level the tester did not clear is counted as anxious regardless of deaths.
"""
import argparse
import csv
import math
from collections import defaultdict


def zone(r, lo, hi):
    if r < lo:
        return "bored"
    if r > hi:
        return "anxious"
    return "flow"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--q", type=int, default=3)
    ap.add_argument("--lo", type=float, default=0.8)
    ap.add_argument("--hi", type=float, default=1.25)
    ap.add_argument("--intended", type=float, default=1.0)
    a = ap.parse_args()

    rows = defaultdict(list)
    with open(a.log, newline="") as f:
        for r in csv.DictReader(f):
            rows[r["tester"]].append(r)

    per_level = defaultdict(list)
    print(f"Q = {a.q}, band {a.lo}-{a.hi}, intended deaths per clear = {a.intended}\n")
    for tester, rs in rows.items():
        rs.sort(key=lambda r: int(r["level"]))
        strain, predicted, actual = 0, None, None
        print(f"{tester}")
        print("  level  deaths  R_hat  zone     strain  rating  stopped")
        for r in rs:
            lvl, d = int(r["level"]), int(r["deaths"])
            cleared = r["cleared"].strip() == "1"
            rh = d / a.intended
            z = zone(rh, a.lo, a.hi) if cleared else "anxious"
            strain = strain + 1 if z != "flow" else max(0, strain - 1)
            if strain >= a.q and predicted is None:
                predicted = lvl
            if r.get("stopped_here", "").strip() == "1" and actual is None:
                actual = lvl
            per_level[lvl].append(d)
            print(f"  {lvl:5d}  {d:6d}  {rh:5.2f}  {z:8s} {strain:6d}  "
                  f"{r.get('rating', ''):6s}  {'yes' if r.get('stopped_here', '').strip() == '1' else ''}")
        print(f"  predicted quit after level: {predicted or 'none'}; "
              f"actually stopped at level: {actual or 'none'}\n")

    print("Per-level pooled estimate (testers who reached the level)")
    print("  level  n  mean_deaths  R_hat  approx_SE")
    for lvl in sorted(per_level):
        ds = per_level[lvl]
        m = sum(ds) / len(ds)
        rh = m / a.intended
        p = 1 / (1 + rh)
        se = math.sqrt(1 - p) / p / math.sqrt(len(ds)) / a.intended
        print(f"  {lvl:5d}  {len(ds)}  {m:11.2f}  {rh:5.2f}  {se:9.2f}")


if __name__ == "__main__":
    main()
