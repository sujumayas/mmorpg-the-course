#!/usr/bin/env python3
"""PR301 lab 04: is the login path done? Standard library only.

Usage: python check_soak.py soak.csv [--threshold 0.01] [--z 1.96]

soak.csv has one row per test condition: condition, attempts, failures.
Model (PR301 week 4, section 2):
  zero failures:   upper bound = -ln(0.05) / n  (the rule of three, about 3 / n)
  any failures:    upper bound = Wilson 95% upper limit for failures / n
  A condition is DONE when its upper bound is at or below the threshold.
  attempts needed for zero failures to prove the threshold: ceil(-ln(0.05) / threshold)
"""
import argparse
import csv
import math
import sys


def wilson_upper(x, n, z):
    p = x / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre + half


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("soak")
    ap.add_argument("--threshold", type=float, default=0.01)
    ap.add_argument("--z", type=float, default=1.96)
    a = ap.parse_args()
    with open(a.soak, newline="") as f:
        rows = [r for r in csv.DictReader(f)]
    if not rows:
        print("NOT READY: no rows")
        sys.exit(1)
    need = math.ceil(-math.log(0.05) / a.threshold)
    print(f"Threshold {a.threshold:.2%}. Zero failures prove it after {need} attempts.")
    print(f"{'condition':<22}{'n':>6}{'fail':>6}{'upper 95%':>11}  verdict")
    ok = True
    for r in rows:
        n, x = int(r["attempts"]), int(r["failures"])
        if n <= 0 or x < 0 or x > n:
            print(f"{r['condition']:<22} bad counts")
            ok = False
            continue
        up = -math.log(0.05) / n if x == 0 else wilson_upper(x, n, a.z)
        done = up <= a.threshold
        ok = ok and done
        print(f"{r['condition']:<22}{n:>6}{x:>6}{up:>11.2%}  {'DONE' if done else 'NOT DONE'}")
    print("PASS" if ok else "NOT READY")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
