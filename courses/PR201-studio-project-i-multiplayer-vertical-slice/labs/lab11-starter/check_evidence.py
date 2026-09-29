#!/usr/bin/env python3
"""PR201 lab 11: check the playtest evidence table and the telemetry count checks. Standard library only.

Usage: python check_evidence.py evidence.csv counts.csv

Model (PR201 week 11, section 3):
  Wilson 95% interval for k of n. Rule "above:t" means act if the whole interval is above t,
  leave if the whole interval is at or below t, otherwise can't decide. Rule "below:t" is the mirror.
evidence.csv needs unit (player, party or session), k, n, rule, and your verdict
(act, leave or cant_decide). Every "act" row needs a cluster_note saying which sessions the
events came from. counts.csv lists each count check with two numbers that should match;
a mismatch needs a note explaining it.
"""
import csv
import sys
from math import sqrt


def wilson(k, n, z=1.96):
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, center - half), min(1.0, center + half)


def verdict(lo, hi, rule):
    side, t = rule.split(":")
    t = float(t)
    if side == "above":
        return "act" if lo > t else "leave" if hi <= t else "cant_decide"
    return "act" if hi < t else "leave" if lo >= t else "cant_decide"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = []
    with open(sys.argv[1], newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"{'id':<4}{'unit':<8}{'k/n':>7}  {'Wilson 95%':<17}{'model':<12}yours")
    for r in rows:
        rid = r["id"]
        try:
            k, n = int(r["k"]), int(r["n"])
        except ValueError:
            problems.append(f"{rid}: k and n must be whole numbers")
            continue
        if r["unit"].strip() not in ("player", "party", "session"):
            problems.append(f"{rid}: unit must be player, party or session")
        if not r["rule"].strip() or ":" not in r["rule"]:
            problems.append(f"{rid}: rule must look like above:0.05 or below:0.70")
            continue
        lo, hi = wilson(k, n)
        model = verdict(lo, hi, r["rule"].strip())
        yours = r["verdict"].strip()
        print(f"{rid:<4}{r['unit']:<8}{k:>3}/{n:<3}  [{lo:5.1%}, {hi:5.1%}]  {model:<12}{yours or '-'}")
        if yours != model:
            problems.append(f"{rid}: verdict '{yours}' but the interval gives '{model}'")
        if model == "act" and not r["cluster_note"].strip():
            problems.append(f"{rid}: an act row needs a cluster_note")
    with open(sys.argv[2], newline="") as f:
        for c in csv.DictReader(f):
            a, b = c["value_a"].strip(), c["value_b"].strip()
            if not a or not b:
                problems.append(f"count check '{c['check']}': both values are required")
            elif a != b and not c["note"].strip():
                problems.append(f"count check '{c['check']}': {a} vs {b} needs a note")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
