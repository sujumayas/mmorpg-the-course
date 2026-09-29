"""MMO403 Lab 09 starter: the spending curve of a live game.

Standard library only. Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab09-starter/test_spend.py
from the repository root. Formulas are the week 9 lecture's.

spend_month.csv holds one synthetic month: 20,000 accounts, spend in US dollars.
It is invented data, generated for this lab, not any game's telemetry.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).with_name("spend_month.csv")


def load(path=DATA):
    """Return the list of monthly spends (floats), one per account. Provided."""
    with open(path, newline="") as fh:
        return [float(r["spend_usd"]) for r in csv.DictReader(fh)]


def payer_rate(spends):
    """Share of accounts with spend > 0. TODO"""
    raise NotImplementedError


def gini(xs):
    """Gini coefficient with the sorted formula from the lecture:
    sum((2i - n - 1) * x_i) / (n * total), i = 1..n on the ascending list.
    Return 0.0 if the total is 0. TODO"""
    raise NotImplementedError


def lorenz(xs):
    """Lorenz points [(0.0, 0.0), (1/n, L1), ..., (1.0, 1.0)] on the ascending list. TODO"""
    raise NotImplementedError


def top_share(xs, q):
    """Share of the total held by the top k = round(q * n) values. TODO"""
    raise NotImplementedError


def gini_identity(spends):
    """(1 - p) + p * gini(payers), where payers are the spends > 0. TODO"""
    raise NotImplementedError


def alpha_from_top_share(q, share):
    """Pareto alpha such that q ** (1 - 1/alpha) == share. TODO"""
    raise NotImplementedError


def pareto_top_share(q, alpha):
    """Model top share q ** (1 - 1/alpha). TODO"""
    raise NotImplementedError


def cap_effect(xs, cap):
    """Apply a cap to a list of payer spends. Return (share of payers with
    spend > cap, share of revenue lost), where the loss is sum(max(0, x - cap))
    over the total. TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    s = load()
    pay = [x for x in s if x > 0]
    print("payer rate", payer_rate(s))
    print("G_pay", round(gini(pay), 3), "G_all", round(gini(s), 3))
    for q in (0.01, 0.1):
        print("top", q, "of payers", round(top_share(pay, q), 3))
