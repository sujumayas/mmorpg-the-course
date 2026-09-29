"""Tests for GD202 Lab 12. Values come from the week 12 lecture, section 2.
Run with `.venv/bin/python test_variation.py` (from any folder) or pytest."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from variation import (Cycle, NoRepeatBag, Once, RandomPick, ShuffleBag,  # noqa: E402
                       Stopping, count_back_to_back, first_repeat, lines_needed,
                       p_any_repeat, plays)


def test_deterministic_rules():
    assert plays(Stopping(3), 6) == [0, 1, 2, 2, 2, 2]
    assert plays(Once(3), 5) == [0, 1, 2, None, None]
    assert plays(Cycle(3), 7) == [0, 1, 2, 0, 1, 2, 0]


def test_random_pick():
    seq = plays(RandomPick(4, random.Random(7)), 2000)
    assert set(seq) == {0, 1, 2, 3}
    for v in range(4):
        assert 400 < seq.count(v) < 600, "picks should be roughly uniform"


def test_shuffle_bag_blocks():
    seq = plays(ShuffleBag(5, random.Random(3)), 50)
    for start in range(0, 50, 5):
        assert sorted(seq[start:start + 5]) == [0, 1, 2, 3, 4], "each bag is a permutation"
    orders = {tuple(seq[s:s + 5]) for s in range(0, 50, 5)}
    assert len(orders) > 1, "the bag must be reshuffled"


def test_no_repeat_bag():
    seq = plays(NoRepeatBag(3, random.Random(11)), 3000)
    assert count_back_to_back(seq) == 0
    for start in range(0, 3000, 3):
        assert sorted(seq[start:start + 3]) == [0, 1, 2]


def test_counters():
    assert count_back_to_back([1, 1, 2, 2, 2, 3]) == 3
    assert count_back_to_back([0, None, None, 1]) == 0
    assert first_repeat([3, 1, 3]) == 3
    assert first_repeat([0, 1, 2, 3]) is None
    assert first_repeat([2, 2]) == 2


def test_formulas():
    assert abs(p_any_repeat(5, 3) - 0.52) < 1e-9
    assert abs(p_any_repeat(10, 4) - 0.496) < 1e-9
    assert p_any_repeat(5, 1) == 0.0
    assert p_any_repeat(3, 4) == 1.0
    assert lines_needed(5, 0.9) == 97
    assert lines_needed(4, 0.9) == 59
    assert lines_needed(5, 0.5) == 17


def test_measured_matches_model():
    # Lecture section 2: over 100 plays with n = 5, random gives 99/5 = 19.8
    # back-to-back repeats on average and a shuffle bag gives 19 x 1/5 = 3.8.
    rng = random.Random(2026)
    rand = sum(count_back_to_back(plays(RandomPick(5, rng), 100)) for _ in range(2000)) / 2000
    bag = sum(count_back_to_back(plays(ShuffleBag(5, rng), 100)) for _ in range(2000)) / 2000
    assert abs(rand - 19.8) < 0.5, rand
    assert abs(bag - 3.8) < 0.3, bag


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
