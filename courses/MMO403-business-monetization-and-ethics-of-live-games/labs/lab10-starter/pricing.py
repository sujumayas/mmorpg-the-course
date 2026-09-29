"""MMO403 Lab 10: pricing functions. Fill in every function that raises NotImplementedError.

Run:  python gen_price_test.py   # once, writes price_test.csv
      python pricing.py          # prints the readout
      python check_lab10.py      # PASS / FAIL / TODO per function

Standard library only.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
Z_ALPHA = 1.96      # two-sided 5%
Z_POWER = 0.8416    # 80% power


def rpe(price, conversion):
    """Revenue per exposed player for one item at one price."""
    raise NotImplementedError


def breakeven_conversion(p0, c0, p1):
    """Conversion that price p1 must reach to earn the same revenue per exposed player as (p0, c0)."""
    raise NotImplementedError


def arc_elasticity(p0, c0, p1, c1):
    """Midpoint (arc) elasticity: (change in c / mean c) / (change in p / mean p)."""
    raise NotImplementedError


def n_per_arm_rate(c0, c1):
    """Players per arm to detect c0 vs c1: (Z_ALPHA + Z_POWER)^2 * (c0(1-c0) + c1(1-c1)) / (c1 - c0)^2."""
    raise NotImplementedError


def n_per_arm_revenue(p0, c0, p1, c1):
    """Players per arm to detect a difference in revenue per exposed player for a single item.
    Each player's revenue is p with probability c, else 0, so its variance is p^2 c (1 - c)."""
    raise NotImplementedError


def welch_z(a, b):
    """z statistic for mean(b) - mean(a), unpooled: diff / sqrt(var_a/n_a + var_b/n_b),
    with sample variances using n - 1. Return 0.0 if the standard error is 0."""
    raise NotImplementedError


def cap_values(values, cap):
    """Winsorize: return a new list with every value above cap replaced by cap (MMO308 week 6)."""
    raise NotImplementedError


def summarize(rows):
    """rows: dicts with keys arm, price (float), bought (int), other_spend (float).
    Return {arm: {"n", "buyers", "conversion", "rpe", "store_rpe"}}, where rpe is bundle
    revenue per exposed player and store_rpe adds other_spend (whole-store revenue per exposed player)."""
    raise NotImplementedError


def load_rows():
    with open(HERE / "price_test.csv") as f:
        return [{"arm": r["arm"], "price": float(r["price"]), "bought": int(r["bought"]),
                 "other_spend": float(r["other_spend"])} for r in csv.DictReader(f)]


def main():
    try:
        rows = load_rows()
        s = summarize(rows)
        price = {r["arm"]: r["price"] for r in rows}
        a = s["A"]
        print("arm  price     n  buyers   conv    rpe  store_rpe  breakeven  elasticity")
        for arm, v in s.items():
            be = breakeven_conversion(price["A"], a["conversion"], price[arm])
            el = 0.0 if arm == "A" else arc_elasticity(price["A"], a["conversion"], price[arm], v["conversion"])
            print(f"{arm}   {price[arm]:5.2f} {v['n']:6d} {v['buyers']:6d}  {v['conversion']:.3%} "
                  f"{v['rpe']:.4f}  {v['store_rpe']:.4f}     {be:.3%}     {el:+.2f}")
        for arm in ("B", "C"):
            rev = lambda arm_: [r["price"] * r["bought"] for r in rows if r["arm"] == arm_]
            store = lambda arm_: [r["price"] * r["bought"] + r["other_spend"] for r in rows if r["arm"] == arm_]
            conv = lambda arm_: [r["bought"] for r in rows if r["arm"] == arm_]
            capped = lambda arm_: cap_values(store(arm_), 20.0)
            print(f"{arm} vs A: z(conversion) {welch_z(conv('A'), conv(arm)):+.2f}  "
                  f"z(bundle rpe) {welch_z(rev('A'), rev(arm)):+.2f}  z(store rpe) {welch_z(store('A'), store(arm)):+.2f}  "
                  f"z(store rpe capped at $20) {welch_z(capped('A'), capped(arm)):+.2f}")
        print(f"players per arm, A vs B: conversion {n_per_arm_rate(0.05, 0.04):,.0f}, "
              f"revenue {n_per_arm_revenue(4.99, 0.05, 6.99, 0.04):,.0f}")
    except NotImplementedError:
        print("TODO: finish the functions, then rerun")


if __name__ == "__main__":
    main()
