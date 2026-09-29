"""Lab 08: canon fit.

Fill in every function marked TODO. Run the tests with
    ../../../../.venv/bin/python test_canon_fit.py
from this folder (or with pytest). All tests fail until you implement the functions.

Symbols follow the week 8 lecture:
    ps       list of take rates p_i, the share of players who chose the canon option
    honored  indices (0-based) of choices the expansion honors; they contradict nobody
    types    list of (weight, [p per choice]) for a population of player types;
             weights sum to 1, and within a type choices are independent
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fit(ps, honored=()):
    """Product of p_i over canonized (not honored) choices. 1.0 if none are canonized."""
    raise NotImplementedError("TODO")


def expected_contradictions(ps, honored=()):
    """Sum of (1 - p_i) over canonized choices."""
    raise NotImplementedError("TODO")


def distribution(ps, honored=()):
    """Poisson binomial: list d where d[k] = P(contradicted on exactly k canonized choices).

    Length is (number of canonized choices + 1). Build it one choice at a time with
    d'[k] = d[k] * p + d[k - 1] * (1 - p).
    """
    raise NotImplementedError("TODO")


def dissonance_bits(ps, honored=()):
    """Sum of -log2(p_i) over canonized choices."""
    raise NotImplementedError("TODO")


def best_honor_set(ps, budget):
    """Indices of the `budget` choices with the smallest p_i, as a sorted tuple.

    Break ties by lower index first.
    """
    raise NotImplementedError("TODO")


def take_rates(types):
    """Population take rate per choice: sum over types of weight * p."""
    raise NotImplementedError("TODO")


def mixture_distribution(types, honored=()):
    """Weighted sum of each type's distribution()."""
    raise NotImplementedError("TODO")


def mixture_fit(types, honored=()):
    """Share of the whole population contradicted on no canonized choice."""
    raise NotImplementedError("TODO")


def per_type_expected(types, honored=()):
    """List of expected contradictions for each type, in the order given."""
    raise NotImplementedError("TODO")


def load_choices(path=HERE / "choices.csv"):
    """Return a list of (choice, p) tuples from the CSV, with p as a float."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    rows = load_choices()
    ps = [p for _, p in rows]
    print(f"fit {fit(ps):.3f}  E {expected_contradictions(ps):.2f}  bits {dissonance_bits(ps):.2f}")
    print("distribution", " ".join(f"{100 * x:.1f}%" for x in distribution(ps)))
    h = best_honor_set(ps, 2)
    print("honor", [rows[i][0] for i in h], f"fit {fit(ps, h):.3f}")
