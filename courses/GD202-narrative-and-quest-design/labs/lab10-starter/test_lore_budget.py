"""Tests for GD202 Lab 10. Values come from the week 10 lecture, section 2.
Run with `.venv/bin/python test_lore_budget.py` (from any folder) or pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lore_budget import (best_split, break_even_f, completion, expected_read,  # noqa: E402
                         fit_s, plan_value)

TOL = 0.005


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def test_expected_read():
    assert close(expected_read(1, 0.8), 0.80)
    assert close(expected_read(3, 0.8), 1.952)
    assert close(expected_read(5, 0.8), 2.689)
    assert close(expected_read(20, 0.8), 3.954)
    assert close(expected_read(5, 0.7), 1.941)
    assert expected_read(0, 0.8) == 0.0
    assert close(expected_read(7, 1.0), 7.0), "s = 1 means every sentence is read"


def test_completion():
    assert close(completion(3, 0.8), 0.512)
    assert close(completion(20, 0.8), 0.0115, 0.0005)


def test_fit_s():
    assert close(fit_s(15, 50, 6), 0.818)
    assert close(fit_s(40, 100, 4), 0.795)


def test_plan_value():
    s = 0.8
    assert close(plan_value([(20, 1.0)], s), 3.954)
    assert close(plan_value([(5, 0.6)] * 4, s), 6.454)
    assert close(plan_value([(1, 0.6)] * 20, s), 9.60)
    mixed = [(2, 1.0)] + [(1, 0.6)] * 18
    assert close(plan_value(mixed, s), 10.08)
    assert close(plan_value([(0, 0.9)], s), 0.0), "a wordless piece reads zero sentences"


def test_break_even_f():
    assert close(break_even_f(20, 4, 0.8), 0.367)
    assert close(break_even_f(20, 20, 0.8), 0.247)
    assert close(break_even_f(12, 6, 0.8), 0.431)


def test_best_split():
    assert best_split(20, 0.6, 0.8) == 20
    assert best_split(20, 0.2, 0.8) == 1, "below every f*, the forced wall wins"
    assert best_split(12, 0.5, 0.8) == 12
    assert best_split(6, 1.0, 0.8) == 6


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
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
