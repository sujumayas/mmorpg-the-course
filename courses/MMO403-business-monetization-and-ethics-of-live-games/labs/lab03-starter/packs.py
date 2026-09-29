"""MMO403 Lab 03 starter: premium currency pack audit. Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_packs.py        (or: pytest test_packs.py)

The model is the one from the week 3 lecture, section 2. Prices are in integer cents so
that comparisons are exact.

    cash to buy an item   C(c, b) = min over pack counts n_i of  sum n_i x p_i
                                    subject to  b + sum n_i x q_i >= c
    leftover              L = b + sum n_i x q_i - c
    reference price       c x p_1 / q_1   (the smallest pack's rate, no bulk discount)

q_i is the currency in pack i, p_i its price in cents, c the item price in currency and
b the balance the player already holds.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# The lecture's invented store: (currency in pack, price in cents), smallest first.
PACKS = [(1_000, 999), (2_800, 2_499), (5_000, 3_999), (13_500, 9_999)]


def load_packs(path):
    """Return [(coins, cents), ...] sorted by coins from a CSV with columns coins,cents."""
    with open(path, newline="") as f:
        return sorted((int(r["coins"]), int(r["cents"])) for r in csv.DictReader(f))


def cheapest_cover(packs, c, balance=0):
    """TODO step 1. Return (cents, counts, leftover) for the cheapest way to hold at least c
    currency, starting from balance. counts is a tuple with one count per pack, in the
    order given. Break ties in cents by the larger leftover (more currency for the same
    money). If balance >= c, return (0, all zeros, balance - c).

    Hint: this is an unbounded knapsack "cover" problem. A dynamic program over currency
    amounts from 0 to c - balance + the largest pack works well."""
    raise NotImplementedError("cheapest_cover() is yours to write")


def reference_cents(packs, c):
    """TODO step 2. The item's price in money at the smallest pack's rate, rounded to the
    nearest cent (half up). This is the 'no quantity discount' price in the lecture."""
    raise NotImplementedError("reference_cents() is yours to write")


def audit(packs, prices):
    """TODO step 3. For each item price c in prices, starting from a zero balance, return a
    dict with keys: price, cents, leftover, reference, markup (cents / reference, as a
    float). Return the rows in the order of prices."""
    raise NotImplementedError("audit() is yours to write")


def sequence(packs, prices, balance=0):
    """TODO step 4. A player buys the items in prices one after another, each time buying
    the cheapest cover for the next item from their current balance. Return
    (total cents spent, final balance)."""
    raise NotImplementedError("sequence() is yours to write")


if __name__ == "__main__":
    for row in audit(PACKS, [800, 1_200, 1_500, 2_000, 2_800]):
        print(row)
