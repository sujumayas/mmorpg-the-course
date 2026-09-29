"""GD201 Lab 08: clue reliability from playtest data.

Run:    python story_reliability.py
Check:  python check_lab08.py

Fill in every function marked TODO. The docstrings define what each returns.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "watchtower_playtest.csv"
CLUES = ["well", "sickbay", "order", "bags"]

# Candidate places for clues in the chapel level (Part D): (slot name, notice chance).
CHAPEL_SLOTS = [
    ("door_lever", 0.95), ("altar", 0.8), ("nave_left", 0.5), ("nave_right", 0.5),
    ("bell_rope", 0.5), ("crypt", 0.25), ("vestry", 0.25), ("porch_behind", 0.1),
]


def p_all(ps):
    """Chance that every clue is noticed (independent clues)."""
    raise NotImplementedError  # TODO Part A


def p_any(ps):
    """Chance that at least one clue is noticed (independent clues)."""
    raise NotImplementedError  # TODO Part A


def p_at_least(ps, k):
    """Chance that at least k clues are noticed. k = 0 gives 1.0; k > len(ps) gives 0.0."""
    raise NotImplementedError  # TODO Part A


def load_log(path=LOG):
    """Rows of the playtest CSV as a list of dicts, with the clue columns and
    said_beat converted to int."""
    raise NotImplementedError  # TODO Part B


def estimate_p(rows, clue):
    """Fraction of testers who noticed this clue."""
    raise NotImplementedError  # TODO Part B


def observed_rate(rows, clues, k):
    """Fraction of testers who noticed at least k of the given clues."""
    raise NotImplementedError  # TODO Part B


def plan_clues(slots, k, target):
    """Smallest set of slots whose p_at_least(..., k) >= target.
    Among sets of that size, pick the one with the highest rate. If rates tie
    (within 1e-9), pick the alphabetically first sorted list of names.
    Return (sorted list of slot names, rate), or (None, 0.0) if no set reaches the target."""
    raise NotImplementedError  # TODO Part C


if __name__ == "__main__":
    try:
        rows = load_log()
        ps = [estimate_p(rows, c) for c in CLUES]
        print("Estimated p:", {c: round(p, 3) for c, p in zip(CLUES, ps)})
        for k in range(1, len(CLUES) + 1):
            print(f"k={k}: predicted {p_at_least(ps, k):.3f}  observed {observed_rate(rows, CLUES, k):.3f}")
        for k in (1, 2):
            names, rate = plan_clues(CHAPEL_SLOTS, k, 0.9)
            print(f"Chapel plan, k={k}, target 0.9: {names} -> {rate:.3f}")
    except NotImplementedError:
        print("Not implemented yet. Fill in the TODO functions, then run check_lab08.py.")
