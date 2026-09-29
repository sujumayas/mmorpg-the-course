"""Tests for Lab 08, from the week 8 lecture.
Run with `python test_elo.py` or `pytest test_elo.py`."""
import random

from elo import (calibration, expected, make_players, play_round, settled_sd,
                 time_constant, update, k_rule_flat)


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_expected():
    assert near(expected(1500, 1500), 0.5)
    assert near(expected(1900, 1500), 10 / 11)
    assert round(expected(1700, 1500), 3) == 0.760
    assert near(expected(1500, 1700) + expected(1700, 1500), 1)


def test_lecture_table():
    a, b = update(2300, 1500, 1, 32)
    assert round(a - 2300, 1) == 0.3 and near(a - 2300, 1500 - b)
    a, b = update(2300, 1500, 0, 32)
    assert round(2300 - a, 1) == 31.7
    a, b = update(1700, 1700, 1, 32)
    assert near(a, 1716) and near(b, 1684)


def test_unequal_k_injects_points():
    a, b = update(1500, 1500, 1, 40, 10)
    assert near(a, 1520) and near(b, 1495)


def test_speed_and_noise():
    assert round(time_constant(32), 1) == 21.7
    assert round(time_constant(10), 1) == 69.5
    assert round(settled_sd(32), 1) == 52.7
    assert round(settled_sd(16), 1) == 37.3


def test_calibration_buckets():
    records = [(0.55, 1), (0.55, 0), (0.75, 1), (0.75, 1), (0.75, 0), (0.75, 1), (1.0, 1)]
    out = calibration(records)
    assert out[0][:3] == (0.5, 0.6, 2) and near(out[0][4], 0.5)
    assert out[1][:3] == (0.7, 0.8, 4) and near(out[1][3], 0.75) and near(out[1][4], 0.75)
    assert out[2][:3] == (0.9, 1.0, 1)


def test_ladder_is_zero_sum_with_flat_k():
    players = make_players(100, seed=3)
    rng = random.Random(4)
    for _ in range(20):
        play_round(players, k_rule_flat(24), rng)
    assert near(sum(p["rating"] for p in players), 100 * 1500, 1e-6)


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
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    raise SystemExit(1 if failed else 0)
