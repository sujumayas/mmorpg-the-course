"""MMO309 Lab 13: pricing a bounty table.

The model (lecture week 13, section 2):
    exploit value    E_x = v / h - q * L
    bounty needed    B*  = max(0, E_x / a)
    studio cost      C_x = d / h + R
    double dip       E_dd = v * k + (1 - p) * a * B - p * L

Symbols: v = finder's real-money value per day, h = daily detection chance,
q = chance the exploiter is identified, L = finder's loss if identified,
a = chance a report is accepted and paid, d = studio harm per day,
R = one-time incident cost, k = days a double-dipper uses the bug first,
p = chance your logs reveal that prior use, B = the bounty paid.

Fill in every function marked TODO. Run `python test_bounty.py` to check.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent


def load_classes(path=HERE / "exploit_classes.csv"):
    """Read the exploit classes into a list of dicts with float fields."""
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({"name": r["name"], **{k: float(r[k]) for k in "v q L a d R".split()}})
    return rows


def exploit_value(v, h, q, L):
    """TODO: expected dollars from using the exploit until it is patched."""
    raise NotImplementedError


def bounty_needed(v, h, q, L, a):
    """TODO: smallest bounty that makes reporting at least as good as exploiting. Never negative."""
    raise NotImplementedError


def studio_cost(d, h, R):
    """TODO: expected cost to the studio if the exploit runs until detection."""
    raise NotImplementedError


def double_dip_value(v, k, p, a, B, L):
    """TODO: expected value of using the bug for k days and then reporting it."""
    raise NotImplementedError


def round_up(x, step=50):
    """Round x up to the next multiple of step (payouts are quoted in $50 steps)."""
    return step * math.ceil(x / step)


def price_table(rows, mean_detection_days, floor=100):
    """TODO: return one dict per exploit class with keys
    name, b_star, payout, studio_cost, share.
    payout = max(floor, round_up(b_star)); share = payout / studio_cost.
    Use h = 1 / mean_detection_days.
    """
    raise NotImplementedError


def longest_affordable_detection(rows, cap, max_days=365):
    """TODO: the largest whole number of mean detection days D (1..max_days) for which
    every class has b_star <= cap. Return 0 if even D = 1 is unaffordable.
    """
    raise NotImplementedError


if __name__ == "__main__":
    rows = load_classes()
    print(f"{'class':<24}{'B*':>9}{'payout':>9}{'C_x':>10}{'share':>8}")
    for r in price_table(rows, mean_detection_days=10):
        print(f"{r['name']:<24}{r['b_star']:>9,.0f}{r['payout']:>9,}{r['studio_cost']:>10,.0f}{r['share']:>8.1%}")
    print("longest affordable mean detection at a $5,000 cap:",
          longest_affordable_detection(rows, cap=5000), "days")
