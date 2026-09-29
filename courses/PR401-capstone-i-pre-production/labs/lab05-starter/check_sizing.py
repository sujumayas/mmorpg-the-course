#!/usr/bin/env python3
"""PR401 lab 05: how many testers settle a question? Standard library only.

Usage: python check_sizing.py sizing.csv [--z 1.96]

One row per prototype 2 question. kind = discovery or decision.
  discovery: P(seen) = 1 - (1 - lam)^n                     reports the n for 85% and the chance at n_planned
  decision:  n0 = z^2 p (1 - p) / (p - t)^2,  DE = 1 + (k - 1) rho,  n = ceil(n0 * DE)
             groups = ceil(n / k),  observer_hours = groups * s * o
PASS when every row is complete, decision rows plan at least n testers (or give a
reason in note), sequential rows have a stop_rule, and the planned observer hours of all
rows fit within the budget row.
"""
import argparse
import csv
import math
import sys


def f(r, k):
    return float(r[k])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sizing")
    ap.add_argument("--z", type=float, default=1.96)
    a = ap.parse_args()
    problems, hours, budget = [], 0.0, None
    with open(a.sizing, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        q, kind = r["id"].strip(), r["kind"].strip()
        try:
            if kind == "budget":
                budget = f(r, "hours_available")
                continue
            if kind == "discovery":
                lam, n = f(r, "lam"), f(r, "n_planned")
                n85 = math.ceil(math.log(0.15) / math.log(1 - lam))
                print(f"{q}: discovery, lam {lam:.2f}: P(seen) at n={n:.0f} is {1 - (1 - lam) ** n:.1%}; 85% needs n = {n85}")
                hours += math.ceil(n / f(r, "k")) * f(r, "s") * f(r, "o")
                continue
            if kind != "decision":
                problems.append(f"{q}: kind must be discovery, decision or budget")
                continue
            p, t, k, rho = f(r, "p"), f(r, "t"), f(r, "k"), f(r, "rho")
        except (KeyError, ValueError):
            problems.append(f"{q}: missing or non-numeric values")
            continue
        if abs(p - t) < 1e-9:
            problems.append(f"{q}: p equals t; no finite sample decides it")
            continue
        n0 = a.z ** 2 * p * (1 - p) / (p - t) ** 2
        de = 1 + (k - 1) * rho
        n = math.ceil(n0 * de - 1e-9)
        groups = math.ceil(n / k)
        planned = float(r.get("n_planned") or 0)
        g_planned = math.ceil(planned / k) if planned else groups
        oh = g_planned * f(r, "s") * f(r, "o")
        hours += oh
        print(f"{q}: decision p={p} t={t} k={k:g} rho={rho}: n0 {n0:.1f}, DE {de:.2f}, n {n}, groups {groups}, "
              f"planned {planned:.0f} testers in {g_planned} groups = {oh:g} observer h")
        if planned < n and not r.get("note", "").strip():
            problems.append(f"{q}: plans {planned:.0f} testers, sizing needs {n}; give a reason in note")
        if r.get("sequential", "").strip() == "yes" and not r.get("stop_rule", "").strip():
            problems.append(f"{q}: sequential test with no stop_rule")
    if budget is None:
        problems.append("no budget row")
    else:
        print(f"observer hours planned {hours:g} of {budget:g} available")
        if hours > budget + 1e-9:
            problems.append(f"planned observer hours {hours:g} exceed budget {budget:g}")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
