#!/usr/bin/env python3
"""PR201 lab 03: rank technical risks and choose spikes. Standard library only.

Usage: python check_risks.py risks.csv [--budget 20]

Model (PR201 week 3, section 2):
  exposure  RE     = p * loss_h                      expected hours lost (Boehm's risk exposure)
  reduction dRE    = (p - p_after) * loss_h          hours of exposure a spike removes
  net value        = dRE - spike_h                   worth doing if > 0
  return           = net / spike_h                   rank spikes by this, highest first
Spikes are chosen in rank order while their hours fit in the budget. Negative-net risks are accepted.
"""
import argparse
import csv
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("risks")
    ap.add_argument("--budget", type=float, default=20)
    a = ap.parse_args()
    with open(a.risks, newline="") as f:
        rows = list(csv.DictReader(f))
    problems = []
    for r in rows:
        r["p"], r["p_after"] = float(r["p"]), float(r["p_after"])
        r["L"], r["s"] = float(r["loss_h"]), float(r["spike_h"])
        r["RE"] = r["p"] * r["L"]
        r["dRE"] = (r["p"] - r["p_after"]) * r["L"]
        r["net"] = r["dRE"] - r["s"]
        r["ret"] = r["net"] / r["s"] if r["s"] else 0
        if not 0 <= r["p_after"] <= r["p"] <= 1:
            problems.append(f"{r['id']}: need 0 <= p_after <= p <= 1")
        if not r["owner"].strip():
            problems.append(f"{r['id']}: no owner")
        if not r["spike_question"].strip().endswith("?"):
            problems.append(f"{r['id']}: spike_question must be a yes/no question")
    used = 0.0
    print(f"{'id':<4}{'RE':>6}{'dRE':>6}{'spike':>6}{'net':>7}{'return':>8}  decision")
    for r in sorted(rows, key=lambda r: -r["ret"]):
        if r["net"] <= 0:
            d = "accept (spike costs more than it saves)"
        elif used + r["s"] <= a.budget:
            used += r["s"]
            d = "SPIKE in sprint 1"
        else:
            d = "over budget: spike in sprint 2 or rethink"
        print(f"{r['id']:<4}{r['RE']:6.1f}{r['dRE']:6.1f}{r['s']:6.0f}{r['net']:7.2f}{r['ret']:8.2f}  {d}")
    print(f"total exposure {sum(r['RE'] for r in rows):.1f} h, spike hours used {used:.0f} of {a.budget:.0f}")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
