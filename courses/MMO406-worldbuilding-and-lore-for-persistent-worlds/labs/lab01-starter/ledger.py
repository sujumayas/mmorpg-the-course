"""MMO406 Lab 01 starter: the tension ledger. Standard library only.

A bible is a JSON file with a consumption rate "c" and a list of "tensions".
Each tension has "id", "kind" ("plot" or "structural"), "who", "wants" and
"blocked_by". Structural tensions also carry "g" (plot tensions spawned per
expansion) and should carry "system" (the game system that renews them).

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_ledger.py

Run the audit on a bible:

    ../../../../.venv/bin/python ledger.py coastal.json
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
UNLIMITED = None  # returned by full_expansions when refill >= consumption


def load(path):
    """Read a bible JSON file (given)."""
    with open(path) as f:
        return json.load(f)


def refill(bible):
    """TODO: return R = the sum of g over structural tensions, as a Fraction.

    Hint: Fraction(str(0.5)) == Fraction(1, 2). Plot tensions contribute 0.
    """
    raise NotImplementedError


def launch_stock(bible):
    """TODO: return P0 = the number of plot tensions that are real tensions.

    A tension counts only if both "wants" and "blocked_by" are non-empty.
    """
    raise NotImplementedError


def simulate(P0, c, R, horizon=12):
    """TODO: return a list of (stock_at_start, full) for expansions 1..horizon.

    An expansion is full if stock >= c; then stock = stock - c + R.
    Otherwise it is short and stock = stock + R (nothing consumed).
    """
    raise NotImplementedError


def full_expansions(P0, c, R):
    """TODO: closed form from the lecture.

    0 if P0 < c; UNLIMITED if R >= c; else floor((P0 - c) / (c - R)) + 1.
    """
    raise NotImplementedError


def problems(bible):
    """TODO: return a sorted list of problem strings, one per issue:

    - "<id>: not a tension (missing want or block)" if wants or blocked_by is empty
    - "<id>: structural but not tied to a system" if kind is structural and
      "system" is missing or empty
    """
    raise NotImplementedError


def audit(bible):
    """Summary used by the report (given, relies on your functions)."""
    P0, R, c = launch_stock(bible), refill(bible), Fraction(bible["c"])
    N = full_expansions(P0, c, R)
    return {"P0": P0, "R": R, "c": c, "d": c - R, "N": N, "problems": problems(bible)}


def report(bible):
    a = audit(bible)
    n = "unlimited" if a["N"] is UNLIMITED else a["N"]
    print(f"{bible['name']}")
    print(f"  P0 = {a['P0']}, c = {a['c']}, R = {float(a['R']):g}, d = {float(a['d']):g}, N = {n}")
    for stock, full in simulate(a["P0"], a["c"], a["R"]):
        print(f"  {float(stock):6.2f}  {'full' if full else 'SHORT'}")
    for p in a["problems"]:
        print("  problem:", p)


if __name__ == "__main__":
    report(load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "coastal.json")))
