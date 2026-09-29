#!/usr/bin/env python3
"""PR401 lab 02: comparables ranges and launch audience. Standard library only.

Usage: python check_comps.py comps.csv audience.csv [--m-low 38] [--m-high 58] [--phi 0.5] [--fee 0.30]

Model (PR401 week 2, sections 2 and 4):
  owners = reviews * m          gross = owners * price * phi          net = gross * (1 - fee)
  D      = 24 * ccu_peak / (q * h_day)
Rows marked 'paid' are estimated. 'paid_plus_offsite' rows are estimated as a lower bound,
because buyers outside Steam leave no Steam review. 'free' and 'subscription' rows are listed but
not estimated.
PASS when there are 2 to 4 comps, every row has a date and a reason, at least one row is
marked small_or_failed = yes, at least two rows are estimable, and audience.csv is complete.
"""
import argparse
import csv
import sys

MODELS = {"paid", "free", "subscription", "paid_plus_offsite"}


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("comps")
    ap.add_argument("audience")
    ap.add_argument("--m-low", type=float, default=38)
    ap.add_argument("--m-high", type=float, default=58)
    ap.add_argument("--phi", type=float, default=0.5)
    ap.add_argument("--fee", type=float, default=0.30)
    a = ap.parse_args()
    comps, problems = read(a.comps), []
    if not 2 <= len(comps) <= 4:
        problems.append(f"{len(comps)} comps (need 2 to 4)")
    print(f"{'game':<32}{'owners low':>12}{'owners high':>13}{'net low $M':>12}{'net high $M':>13}")
    estimable = 0
    for r in comps:
        g = r["game"].strip()
        for col in ("reviews_date", "reason"):
            if not r.get(col, "").strip():
                problems.append(f"{g}: missing {col}")
        bm = r.get("business_model", "").strip()
        if bm not in MODELS:
            problems.append(f"{g}: business_model must be one of {sorted(MODELS)}")
            continue
        if bm not in ("paid", "paid_plus_offsite"):
            print(f"{g:<32}{'not estimable (' + bm + ')':>50}")
            continue
        estimable += 1
        R, price = float(r["reviews"]), float(r["price_usd"])
        lo, hi = R * a.m_low, R * a.m_high
        k = price * a.phi * (1 - a.fee) / 1e6
        note = "  (Steam only: lower bound)" if bm == "paid_plus_offsite" else ""
        print(f"{g:<32}{lo:>12,.0f}{hi:>13,.0f}{lo * k:>12.2f}{hi * k:>13.2f}{note}")
    if estimable < 2:
        problems.append("fewer than two comps can be estimated with the review multiplier")
    if not any(r.get("small_or_failed", "").strip() == "yes" for r in comps):
        problems.append("no comp is marked small_or_failed = yes")
    aud = {r["key"].strip(): r["value"].strip() for r in read(a.audience)}
    try:
        peak, q, h = float(aud["ccu_peak"]), float(aud["q"]), float(aud["h_day"])
        D = 24 * peak / (q * h)
        print(f"\nlaunch audience: peak {peak:.0f}, q {q}, h_day {h} -> average CCU {peak / q:.1f}, daily players D = {D:.0f}")
        if aud.get("D_claimed") and abs(float(aud["D_claimed"]) - D) > 1:
            problems.append(f"D_claimed {aud['D_claimed']} does not match computed {D:.0f}")
    except (KeyError, ValueError):
        problems.append("audience.csv needs numeric ccu_peak, q and h_day")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
