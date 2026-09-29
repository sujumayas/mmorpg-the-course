"""MMO407 lab 14: launch readiness review.

A scorecard is a dict  name -> (weight, gate), where gate is None for "no minimum".
A plan is a dict       name -> score in [0, 1], or None for "no evidence" (scores 0).
Standard library only. Run the tests from inside lab14-starter/ with:
    python -m unittest test_readiness.py
"""
from math import prod

# The lecture's section 2 scorecard and plans. Invented teaching values.
LECTURE_CRITERIA = {"capacity": (3, 0.7), "beta exposure": (2, None),
                    "restore drill": (2, 0.7), "kill switches": (2, 0.7),
                    "player comms": (2, None), "low-end platform": (1, 0.7)}
_NAMES = list(LECTURE_CRITERIA)
LECTURE_PLANS = {"A": dict(zip(_NAMES, [1.0, 1.0, 1.0, 1.0, 1.0, 0.0])),
                 "B": dict(zip(_NAMES, [0.85] * 6)),
                 "C": dict(zip(_NAMES, [0.9, 0.7, 0.9, 0.9, 0.9, 0.9]))}


def score_of(plan, name):
    """A criterion's score, with missing evidence (None or absent) as 0."""
    s = plan.get(name)
    return 0.0 if s is None else s


def weighted_score(criteria, plan):
    """S = sum(w * s) / sum(w)."""
    # TODO 1
    raise NotImplementedError("TODO 1")


def geometric_score(criteria, plan):
    """G = product of s ** (w / W). Any zero score with positive weight gives 0."""
    # TODO 2: watch out for 0 ** x, which is fine in Python for x > 0.
    raise NotImplementedError("TODO 2")


def failed_gates(criteria, plan):
    """Names of gated criteria whose score is below the gate, in scorecard order."""
    # TODO 3
    raise NotImplementedError("TODO 3")


def verdict(criteria, plan, rule="gated", threshold=0.8, tol=1e-9):
    """'go' or 'no-go' under the rule 'average', 'geometric' or 'gated'."""
    if rule == "average":
        ok = weighted_score(criteria, plan) >= threshold - tol
    elif rule == "geometric":
        ok = geometric_score(criteria, plan) >= threshold - tol
    elif rule == "gated":
        ok = not failed_gates(criteria, plan) and weighted_score(criteria, plan) >= threshold - tol
    else:
        raise ValueError(rule)
    return "go" if ok else "no-go"


def smallest_fix(criteria, plan, threshold=0.8):
    """The smallest total score increase that turns the plan into 'go' under the
    gated rule. Returns {name: new score} for the criteria that change.

    Step 1: raise every failed gate exactly to its gate value.
    Step 2: if S is still below threshold, add the missing weighted points to
    the criteria with the largest weight first (ties in scorecard order),
    raising each at most to 1.0. Return None if even all 1.0 cannot reach it.
    """
    # TODO 4
    raise NotImplementedError("TODO 4")


def print_lecture_table():
    for name, plan in LECTURE_PLANS.items():
        print(f"plan {name}: average {weighted_score(LECTURE_CRITERIA, plan):.3f}  "
              f"geometric {geometric_score(LECTURE_CRITERIA, plan):.3f}  "
              f"failed gates: {', '.join(failed_gates(LECTURE_CRITERIA, plan)) or 'none'}")


if __name__ == "__main__":
    try:
        print_lecture_table()
    except NotImplementedError as e:
        print(f"{e} is not done yet. Run the tests to see what is missing.")
