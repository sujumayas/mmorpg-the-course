"""Tests for MMO406 Lab 01. Values come from the week 1 lecture.
Run with `python test_ledger.py` or `pytest test_ledger.py`."""
import os
from fractions import Fraction

from ledger import (UNLIMITED, audit, full_expansions, launch_stock, load,
                    problems, refill, simulate)

HERE = os.path.dirname(os.path.abspath(__file__))


def test_lecture_table():
    # P0 = 12, c = 3, R = 0..3 (section 2 table)
    assert full_expansions(12, 3, 0) == 4
    assert full_expansions(12, 3, 1) == 5
    assert full_expansions(12, 3, 2) == 10
    assert full_expansions(12, 3, 3) is UNLIMITED
    assert full_expansions(2, 3, 1) == 0


def test_check_yourself():
    R = Fraction(3, 2)
    assert full_expansions(20, 4, R) == 7
    assert full_expansions(28, 4, R) == 10
    assert full_expansions(20, 4, Fraction(5, 2)) == 11


def test_simulate_matches_table():
    rows = simulate(12, 3, 1, horizon=7)
    assert [s for s, _ in rows] == [12, 10, 8, 6, 4, 2, 3]
    assert [f for _, f in rows] == [True] * 5 + [False, True]


def test_simulate_agrees_with_closed_form():
    for P0 in range(0, 25):
        for c in range(1, 6):
            for R in [Fraction(k, 2) for k in range(0, 2 * c)]:
                rows = simulate(P0, c, R, horizon=60)
                n = 0
                for _, full in rows:
                    if not full:
                        break
                    n += 1
                assert n == full_expansions(P0, c, R), (P0, c, R)


def test_coastal_audit():
    a = audit(load(os.path.join(HERE, "coastal.json")))
    assert a["P0"] == 10
    assert a["R"] == Fraction(3, 2)
    assert a["N"] == 5
    assert a["problems"] == []


def test_broken_bible():
    b = load(os.path.join(HERE, "broken.json"))
    assert launch_stock(b) == 1
    assert refill(b) == Fraction(3, 2)
    assert problems(b) == [
        "history: not a tension (missing want or block)",
        "pass: structural but not tied to a system",
    ]
    assert full_expansions(launch_stock(b), 2, refill(b)) == 0


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
