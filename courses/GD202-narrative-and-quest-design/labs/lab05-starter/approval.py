"""GD202 Lab 05 starter: exact approval distributions for a companion.

Standard library only. Fill in the three TODO functions, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab05-starter/test_approval.py

Model (week 5, section 2): at each event the player agrees with probability p
(approval moves by agree_step) or disagrees (approval moves by disagree_step).
Events are independent. With a clamp, approval is clipped to [lo, hi] after
every step, which makes the order of events matter.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import ceil, comb


@dataclass
class Event:
    name: str
    agree_step: int      # step when the player picks what the companion prefers, e.g. +5
    disagree_step: int   # e.g. -5 (0 if the companion does not care either way)


def closed_form(n, s, T, p):
    """The lecture's formula: P(A >= T) for n symmetric events of size s, no clamp."""
    k_min = max(0, ceil((n + T / s) / 2))
    return sum(comb(n, k) * p**k * (1 - p)**(n - k) for k in range(k_min, n + 1))


def walk_distribution(events, p, start=0, lo=None, hi=None):
    """TODO 1. Return a dict {approval value: probability} after all events.

    `p` is either one probability used for every event, or a list with one
    probability per event (a persona that agrees more on some topics).
    Start from {start: 1}. For each event, move each value by agree_step with
    probability p_i and by disagree_step with probability 1 - p_i, then clamp
    to [lo, hi] if those are not None. Merge equal values by adding their
    probabilities. Works with floats or fractions.Fraction."""
    raise NotImplementedError("walk_distribution() is yours to write")


def prob_at_least(dist, T):
    """TODO 2. Return the total probability of values >= T in `dist`."""
    raise NotImplementedError("prob_at_least() is yours to write")


def mean(dist):
    """TODO 3. Return the expected approval of `dist`."""
    raise NotImplementedError("mean() is yours to write")


# Oda, the invented companion from lecture section 1, with ten events.
# agree_step is what happens when the player picks the option Oda prefers.
ODA = [
    Event("the ferryman's debt", +5, -5),
    Event("orphans ask for free food", +5, -5),
    Event("a locked side door", +5, -1),
    Event("the captured informant", +5, -10),
    Event("the magistrate's order", +5, -10),
    Event("the captured deckhand", +10, -10),
    Event("a small bribe", +1, -1),
    Event("the smuggler's ledger", +5, -5),
    Event("the toll bridge", +1, -5),
    Event("the mutiny", +10, -10),
]


if __name__ == "__main__":
    try:
        d = walk_distribution(ODA, 0.5)
        print(f"Oda, p = 0.5: mean {float(mean(d)):+.1f}, P(A >= 30) = {float(prob_at_least(d, 30)):.1%}")
    except NotImplementedError as e:
        raise SystemExit(f"Not finished yet: {e}. Run test_approval.py to see what is left.")
