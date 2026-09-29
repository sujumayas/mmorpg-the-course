"""MMO307 Lab 06 starter: catch-up simulator. Standard library only.

Fill in every function that raises NotImplementedError, then run the tests:

    python test_catchup.py        (or: pytest test_catchup.py)

Notation follows the week 6 lecture: L is the weekly allowance, j the weeks a
player missed, v the player's speed (what they would earn per week with no cap),
N the currency needed to finish, w the week number (weeks are 1, 2, 3, ...).
"""
import math
import random
from dataclasses import dataclass


@dataclass
class Rule:
    L: float                 # weekly allowance
    rolling: bool = True     # True: unused allowance carries forward; False: weekly cap
    head_start: float = 0    # extra allowance available from week 1 (rolling only)
    raise_at: int = None     # after this week, the allowance grows by L2 per week
    L2: float = None
    remove_at: int = None    # after this week, there is no cap at all


def allowance(w, rule):
    """Rolling rule: the most a player may have earned in total by the end of week w.
    Include head_start, a raise after raise_at, and return math.inf after remove_at.
    (For a weekly rule this is not used by simulate; return rule.L * w.)"""
    raise NotImplementedError("allowance() is yours to write")


def simulate(rule, j, v, N, weeks):
    """Return a list totals[0..weeks], the currency a player has at the end of each week.
    totals[0] = 0. The player plays from week j + 1 on and would earn v per week uncapped.
    Weekly rule: each played week earns min(v, weekly limit), where the weekly limit is L,
    or L2 after raise_at, or unlimited after remove_at.
    Rolling rule: each played week earns min(v, allowance(w) - total).
    Totals never exceed N."""
    raise NotImplementedError("simulate() is yours to write")


def finish_week(totals, N):
    """First week whose end-of-week total reaches N, or None."""
    raise NotImplementedError("finish_week() is yours to write")


def catch_up_week(j, v, L):
    """w* = v j / (v - L) for a rolling cap; math.inf when v <= L."""
    raise NotImplementedError("catch_up_week() is yours to write")


def free_window(N, L, v):
    """J_free = N / L - N / v, floored at 0."""
    raise NotImplementedError("free_window() is yours to write")


def population(n, seed, max_join, speeds):
    """Return n players as (j, v) pairs: j uniform on 0..max_join, v chosen uniformly from
    `speeds`. Use random.Random(seed) so results are reproducible."""
    raise NotImplementedError("population() is yours to write")


if __name__ == "__main__":
    rule = Rule(L=750)
    try:
        totals = simulate(rule, 6, 1_500, 9_000, 14)
        print("rolling cap, j = 6, v = 1,500:", [round(t) for t in totals])
    except NotImplementedError:
        print("Write allowance() and simulate(), then run this file again.")
