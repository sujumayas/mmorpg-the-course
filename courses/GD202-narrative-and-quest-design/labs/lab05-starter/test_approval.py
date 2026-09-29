"""Tests for GD202 Lab 05. Values come from the week 5 lecture and lab05.md.
Run with `.venv/bin/python test_approval.py` (from any folder) or pytest."""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from approval import ODA, Event, closed_form, mean, prob_at_least, walk_distribution  # noqa: E402

SYM = [Event(f"e{i}", +5, -5) for i in range(20)]


def test_lecture_value_exact():
    d = walk_distribution(SYM, F(1, 2))
    assert prob_at_least(d, 50) == F(21_700, 1_048_576)


def test_matches_closed_form():
    for p in (0.6, 0.7, 0.75, 0.8, 0.9):
        d = walk_distribution(SYM, p)
        assert abs(prob_at_least(d, 50) - closed_form(20, 5, 50, p)) < 1e-12


def test_distribution_sums_to_one():
    d = walk_distribution(ODA, F(3, 5))
    assert sum(d.values()) == 1


def test_mean():
    assert abs(mean(walk_distribution(SYM, 0.7)) - 40) < 1e-9
    # Asymmetric event: +10 or -5 at p = 0.5 has mean +2.5.
    assert mean(walk_distribution([Event("x", 10, -5)], F(1, 2))) == F(5, 2)


def test_clamp_three_big_steps():
    big = [Event(f"b{i}", +50, -50) for i in range(3)]
    d = walk_distribution(big, F(1, 2), lo=-100, hi=100)
    assert d == {100: F(1, 8), 50: F(3, 8), -50: F(3, 8), -100: F(1, 8)}
    free = walk_distribution(big, F(1, 2))
    assert free == {150: F(1, 8), 50: F(3, 8), -50: F(3, 8), -150: F(1, 8)}


def test_order_matters_with_cap():
    up, down = Event("up", 60, 60), Event("down", -20, -20)
    early = walk_distribution([up, up, down], 1, lo=-100, hi=100)
    late = walk_distribution([down, up, up], 1, lo=-100, hi=100)
    assert early == {80: 1} and late == {100: 1}


def test_per_event_persona():
    evs = [Event("a", 10, -10), Event("b", 10, -10)]
    d = walk_distribution(evs, [F(1), F(1, 2)])
    assert d == {20: F(1, 2), 0: F(1, 2)}


def test_oda_indifferent_player():
    d = walk_distribution(ODA, F(1, 2))
    # Each event contributes (agree + disagree) / 2 at p = 1/2; for ODA these sum to -5.
    assert mean(d) == -5


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError:
                failed += 1
                print(f"FAIL {name}")
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
