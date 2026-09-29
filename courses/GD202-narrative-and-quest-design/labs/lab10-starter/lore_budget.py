"""GD202 Lab 10: lore budget planner.

Standard library only. Fill in the TODO functions, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab10-starter/test_lore_budget.py

Once the tests pass, score a delivery plan:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab10-starter/lore_budget.py sample_plan.csv

The model (week 10 lecture, section 2): before each sentence a reader keeps
going with chance s, so sentence k is read with chance s**k.

A plan file is a CSV with columns: piece, channel, sentences, find_chance, tier
(tier is need, nice or fans). Every row is one piece of lore placed in the game.
"""
import csv
import os
import sys


def expected_read(n, s):
    """TODO 1. Expected number of sentences read from an n-sentence text.
    E(n) = s + s**2 + ... + s**n. Return 0.0 when n == 0. Must also work for
    s == 1.0 (everyone reads everything)."""
    raise NotImplementedError("expected_read() is yours to write")


def completion(n, s):
    """TODO 2. Share of readers who reach the last sentence, s**n."""
    raise NotImplementedError("completion() is yours to write")


def fit_s(reached_last, players, n):
    """TODO 3. Estimate s from a playtest: `reached_last` of `players` testers
    reached sentence n. Return (reached_last / players) ** (1 / n)."""
    raise NotImplementedError("fit_s() is yours to write")


def plan_value(pieces, s):
    """TODO 4. `pieces` is a list of (sentences, find_chance) pairs.
    Return the expected sentences read, sum of find_chance * E(sentences)."""
    raise NotImplementedError("plan_value() is yours to write")


def break_even_f(total, k, s):
    """TODO 5. Split `total` sentences into k equal pieces (k divides total).
    Return the find chance f* at which the split equals one forced wall:
    E(total) / (k * E(total / k))."""
    raise NotImplementedError("break_even_f() is yours to write")


def best_split(total, f, s):
    """TODO 6. Among the divisors k of `total`, return the k whose split plan
    (k pieces, all with find chance f, except k == 1 which is a forced wall
    with find chance 1.0) gives the most sentences read. On a tie, return the
    smallest k (fewer pieces cost less to build)."""
    raise NotImplementedError("best_split() is yours to write")


# ---- Provided: reading a plan file and printing a report --------------------

def load_plan(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["sentences"] = int(r["sentences"])
        r["find_chance"] = float(r["find_chance"])
    return rows


def report(rows, s):
    total = sum(r["sentences"] for r in rows)
    wall = expected_read(total, s)
    value = plan_value([(r["sentences"], r["find_chance"]) for r in rows], s)
    print(f"{'piece':<22}{'channel':<16}{'sent':>5}{'find':>7}{'E(n)':>7}{'f*E':>7}  tier")
    for r in rows:
        e = expected_read(r["sentences"], s)
        print(f"{r['piece']:<22}{r['channel']:<16}{r['sentences']:>5}{r['find_chance']:>7.2f}"
              f"{e:>7.2f}{r['find_chance'] * e:>7.2f}  {r['tier']}")
    need = [r for r in rows if r["tier"] == "need"]
    forced = all(r["find_chance"] >= 1.0 for r in need)
    print(f"\ns = {s:.3f}, {total} sentences in all")
    print(f"one forced wall of {total}: {wall:.2f} sentences read")
    print(f"this plan:              {value:.2f} sentences read ({value / wall:.2f}x the wall)")
    print(f"need-to-know tier forced (find chance 1.0): {'yes' if forced else 'NO'}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "sample_plan.csv")
    if not os.path.isabs(path) and not os.path.exists(path):
        path = os.path.join(here, path)
    s = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    report(load_plan(path), s)
