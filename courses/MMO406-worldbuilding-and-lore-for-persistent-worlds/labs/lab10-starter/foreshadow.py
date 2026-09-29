"""MMO406 Lab 10: how far ahead to foreshadow.

Run:   .venv/bin/python foreshadow.py thornmere_plan.json
Tests: .venv/bin/python test_foreshadow.py   (or pytest)

Model (week 10 lecture, section 2):
    s     = 1 - rho                          chance a plan survives one cycle
    E(d)  = s**d * v * d - (1 - s**d) * D    expected value of lead time d
    d*    = max(0, -1/ln(s) - D/v)           continuous best lead time

d is the lead time in expansion cycles: payoff expansion minus planted expansion.
v is the exposure value per cycle, D the broken-promise cost, rho the
plan-change rate per cycle.

A plan file (see thornmere_plan.json) holds rho, v, a map from hook type to D,
and a list of hooks with id, text, type, planted and payoff (expansion numbers,
0 = launch).
"""
import json
import math
import sys

TIE = 1e-9  # values closer than this count as a tie


def expected_value(d, v, D, rho):
    """Return E(d)."""
    raise NotImplementedError("expected_value")


def best_horizon(v, D, rho):
    """Return the continuous best lead time d*, floored at 0."""
    raise NotImplementedError("best_horizon")


def best_whole(v, D, rho, d_max=10):
    """Return (d, E) for the whole-number d in 0..d_max with the highest E(d).
    On a tie (within TIE) return the lowest d."""
    raise NotImplementedError("best_whole")


def audit(plan):
    """Audit every hook in a plan. Return a list of dicts sorted by hook id:

        {"id", "d", "D", "E", "d_star", "status", "negative"}

    status is "too early" if d > d_star + 1, "too late" if d < d_star - 1,
    otherwise "ok". negative is True when E < 0.

    Raise ValueError if rho is not strictly between 0 and 1, if v <= 0,
    if a hook's type is not in plan["D"], or if a hook's payoff comes
    before its planting.
    """
    raise NotImplementedError("audit")


def report(plan):
    rows = audit(plan)
    print(f"{plan.get('world', 'plan')}: rho={plan['rho']}, v={plan['v']}")
    print(f"{'id':<4} {'type':<10} {'d':>2} {'d*':>6} {'E(d)':>7}  status")
    types = {h["id"]: h["type"] for h in plan["hooks"]}
    for r in rows:
        flag = "  (negative)" if r["negative"] else ""
        print(f"{r['id']:<4} {types[r['id']]:<10} {r['d']:>2} {r['d_star']:>6.2f} "
              f"{r['E']:>7.2f}  {r['status']}{flag}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "thornmere_plan.json"
    with open(path) as f:
        plan = json.load(f)
    try:
        report(plan)
    except NotImplementedError as e:
        print(f"TODO: implement {e}")
        sys.exit(1)
