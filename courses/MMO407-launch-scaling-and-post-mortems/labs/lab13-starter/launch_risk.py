"""MMO407 lab 13: launch risk register, tail and mitigation budget.

Losses are in thousands of player-hours (k ph). Standard library only.
Run the tests from inside lab13-starter/ with:  python -m unittest test_launch_risk.py
"""
from itertools import combinations, product

# The lecture's section 2 register and mitigations. Invented teaching values.
# A risk is name -> (p, impact). A fix is name -> (risk it changes, new (p, impact)).
LECTURE_RISKS = {"queues": (0.80, 50), "auth": (0.40, 75),
                 "dupe": (0.05, 500), "data loss": (0.02, 1000)}
LECTURE_FIXES = {"M1": ("queues", (0.20, 50)), "M2": ("auth", (0.10, 75)),
                 "M3": ("dupe", (0.05, 60)), "M4": ("data loss", (0.02, 100))}
LECTURE_D = 300


def loss_distribution(risks):
    """Exact distribution of the week's total loss for independent risks.

    Returns a dict {total loss: probability}. List all 2**n combinations of
    risks firing or not; combinations with the same total are added together.
    """
    # TODO 1: loop over product((0, 1), repeat=len(risks)); multiply p or 1 - p;
    # add the impacts of the risks that fired; accumulate into the dict.
    raise NotImplementedError("TODO 1")


def expected_loss(dist):
    """Mean of a distribution {loss: probability}."""
    return sum(loss * p for loss, p in dist.items())


def exceedance(dist, x):
    """P(L > x): strictly greater than x."""
    # TODO 2: sum the probabilities of every loss above x.
    raise NotImplementedError("TODO 2")


def apply_fixes(risks, fixes, chosen):
    """A copy of `risks` with each chosen fix's new (p, impact) applied."""
    out = dict(risks)
    for name in chosen:
        risk, new = fixes[name]
        out[risk] = new
    return out


def choose(risks, fixes, budget, D, rule="expected", B=0.0, max_p=0.0):
    """Best set of exactly `budget` fixes, as a sorted tuple of names.

    rule "expected":    lowest expected loss.
    rule "penalty":     lowest expected loss + B * P(L > D).
    rule "limit":       lowest expected loss among sets with P(L > D) <= max_p
                        (return None if no set qualifies).
    Break ties by the alphabetical order of the tuple.
    """
    # TODO 3: try every combination of `budget` fixes (itertools.combinations
    # over sorted names), score it by the rule, and return the best.
    raise NotImplementedError("TODO 3")


def scenario_distribution(risks, s, forced):
    """Distribution when a hidden cause with probability s fires every risk in
    `forced` together. Outside the scenario, each forced risk's probability
    becomes (p - s) / (1 - s), clamped at 0, so its overall rate is unchanged.
    Returns {loss: probability}, mixing the two cases with weights s and 1 - s.
    """
    # TODO 4: build the "inside" register (forced risks at p = 1) and the
    # "outside" register (adjusted p), get both distributions, and mix them.
    raise NotImplementedError("TODO 4")


def print_lecture_table():
    print("plan      E[loss]  P(>300)")
    for plan in [()] + list(combinations(sorted(LECTURE_FIXES), 2)):
        dist = loss_distribution(apply_fixes(LECTURE_RISKS, LECTURE_FIXES, plan))
        label = "+".join(plan) or "none"
        print(f"{label:9} {expected_loss(dist):7.1f}  {exceedance(dist, LECTURE_D):7.3f}")


if __name__ == "__main__":
    try:
        print_lecture_table()
    except NotImplementedError as e:
        print(f"{e} is not done yet. Run the tests to see what is missing.")
