#!/usr/bin/env python3
"""PR201 lab 05: velocity-based forecast to a milestone, and a check that cuts close the gap.

Usage: python forecast.py sprint_result.csv plan.csv --remaining 120 [--band 0.2] [--cuts cuts.csv]

Model (PR201 week 5, section 2):
  focus f     = done_estimate / useful_capacity             (estimate-hours finished per useful hour)
  ratio r     = done_actual / done_estimate                 (how long an estimated hour really took)
  forecast    = f * sum of planned useful capacity           (mid)
  band        = forecast * (1 - band) .. forecast * (1 + band)
  gap         = remaining - forecast
  the plan passes when the 'now' cuts close the mid gap and now + trigger cuts close the low gap
"""
import argparse
import csv
import sys


def read(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("plan")
    ap.add_argument("--remaining", type=float, required=True)
    ap.add_argument("--band", type=float, default=0.2)
    ap.add_argument("--cuts")
    a = ap.parse_args()
    res, plan = read(a.result), read(a.plan)
    cap = sum(float(r["useful_capacity_h"]) for r in res)
    done_e = sum(float(r["done_estimate_h"]) for r in res)
    done_a = sum(float(r["done_actual_h"]) for r in res)
    f, r = done_e / cap, done_a / done_e
    future = sum(float(p["useful_capacity_h"]) for p in plan)
    mid = f * future
    lo, hi = mid * (1 - a.band), mid * (1 + a.band)
    print(f"focus f = {done_e:g} / {cap:g} = {f:.3f}   estimate ratio r = {done_a:g} / {done_e:g} = {r:.2f}")
    for p in plan:
        c = float(p["useful_capacity_h"])
        print(f"sprint {p['sprint']}: capacity {c:g} h -> forecast {f * c:.1f} estimate-h")
    print(f"naive (capacity) view: {future:g} h available vs {a.remaining:g} h remaining")
    print(f"forecast low {lo:.1f}  mid {mid:.1f}  high {hi:.1f}")
    gaps = {k: a.remaining - v for k, v in (("low", lo), ("mid", mid), ("high", hi))}
    print("gap " + "  ".join(f"{k} {v:.1f}" for k, v in gaps.items()))
    problems = []
    if a.cuts:
        cuts = read(a.cuts)
        now = sum(float(c["hours"]) for c in cuts if c["when"].strip() == "now")
        trig = sum(float(c["hours"]) for c in cuts if c["when"].strip().startswith("trigger"))
        print(f"cuts now {now:g} h, trigger cuts {trig:g} h")
        if now < gaps["mid"]:
            problems.append(f"'now' cuts {now:g} h do not close the mid gap {gaps['mid']:.1f} h")
        if now + trig < gaps["low"]:
            problems.append(f"now + trigger cuts {now + trig:g} h do not close the low gap {gaps['low']:.1f} h")
        for c in cuts:
            if not c["pillar_check"].strip():
                problems.append(f"{c['id']}: no pillar check")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
