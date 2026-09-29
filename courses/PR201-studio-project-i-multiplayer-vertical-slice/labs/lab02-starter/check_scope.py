#!/usr/bin/env python3
"""PR201 lab 02: rank features, place the cut line, check pillar support. Standard library only.

Usage: python check_scope.py features.csv [--plannable 312] [--useful 445.5] [--min-support 2] [--greedy]

Model (PR201 week 2, section 2):
  density_f = (number of pillars f supports) / hours_f
  rank non-must features by density, highest first, and keep them while the running total fits
  in plannable - must_hours. Then every pillar needs support >= min_support among kept features,
  and m_max = useful / must_hours must be >= 2.
With --greedy the script proposes tiers. Without it, it checks the tiers you wrote:
tier is must, should (kept) or cut. Every cut row needs a player_loses entry.
"""
import argparse
import csv
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("features")
    ap.add_argument("--plannable", type=float, default=312)
    ap.add_argument("--useful", type=float, default=445.5)
    ap.add_argument("--min-support", type=int, default=2)
    ap.add_argument("--greedy", action="store_true")
    a = ap.parse_args()
    with open(a.features, newline="") as f:
        rows = list(csv.DictReader(f))
    pillars = [k for k in rows[0] if k.startswith("P") and k[1:].isdigit()]
    must = [r for r in rows if r["tier"].strip() == "must"]
    must_h = sum(float(r["hours"]) for r in must)
    room = a.plannable - must_h
    rest = [r for r in rows if r["tier"].strip() != "must"]
    for r in rest:
        r["v"] = sum(int(r[p]) for p in pillars)
        r["d"] = r["v"] / float(r["hours"])
    problems = []
    if a.greedy:
        total = 0.0
        for r in sorted(rest, key=lambda r: -r["d"]):
            h = float(r["hours"])
            if r["v"] > 0 and total + h <= room:
                r["tier"] = "should"
                total += h
            else:
                r["tier"] = "cut"
    kept = [r for r in rest if r["tier"].strip() == "should"]
    kept_h = sum(float(r["hours"]) for r in kept)
    print(f"must {must_h:.0f} h, room {room:.0f} h, should {kept_h:.0f} h, slack {room - kept_h:.0f} h")
    print(f"{'id':<5}{'hours':>6}{'pillars':>8}{'density':>9}  tier")
    for r in sorted(rest, key=lambda r: -r["d"]):
        print(f"{r['id']:<5}{float(r['hours']):6.0f}{r['v']:8d}{r['d']:9.4f}  {r['tier']}")
    if kept_h > room + 1e-9:
        problems.append(f"should tier {kept_h:.0f} h exceeds room {room:.0f} h")
    for p in pillars:
        s = sum(int(r[p]) for r in kept)
        tag = "unsupported" if s == 0 else "fragile" if s < a.min_support else "ok"
        print(f"support({p}) = {s}  {tag}")
        if s < a.min_support:
            problems.append(f"pillar {p} has support {s} < {a.min_support}")
    m_max = a.useful / must_h if must_h else 0
    print(f"m_max = {a.useful:.1f} / {must_h:.0f} = {m_max:.2f}")
    if m_max < 2:
        problems.append("m_max < 2: the must tier is too large for a first-time team")
    for r in rest:
        if r["tier"].strip() not in ("should", "cut"):
            problems.append(f"{r['id']}: tier must be must, should or cut")
        if r["tier"].strip() == "cut" and not r["player_loses"].strip():
            problems.append(f"{r['id']}: cut row needs a player_loses entry")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
