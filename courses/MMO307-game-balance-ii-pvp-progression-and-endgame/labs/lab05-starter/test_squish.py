"""Tests for Lab 05. Values come from the week 5 lecture.
Run with `python test_squish.py` or `pytest test_squish.py`."""
import math

from squish import (armor_mitigation, compensation, dot_tick, dynamic_range, floored_damage,
                    headroom, hits_to_kill, load_eras, power_law, scale_error, squish,
                    time_to_die, uniform_divisor_range)

HEALTH = [2_000, 20_000, 200_000, 2_000_000]
DIVISORS = [2, 10, 50, 200]


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_dynamic_range():
    assert close(dynamic_range(HEALTH), 1000)
    assert uniform_divisor_range(HEALTH, 1_000, 10_000) is None
    assert uniform_divisor_range([300, 9_000_000], 100, 50_000) is None
    lo, hi = uniform_divisor_range([5_000, 40_000], 100, 1_000)
    assert close(lo, 40) and close(hi, 50)


def test_lecture_table():
    assert squish(HEALTH, DIVISORS) == [1_000, 2_000, 4_000, 10_000]
    assert compensation(DIVISORS) == [100, 20, 4, 1]
    new_hit = 400_000 / DIVISORS[-1]
    before = [hits_to_kill(v, 400_000) for v in HEALTH]
    after = [hits_to_kill(v, new_hit) for v in squish(HEALTH, DIVISORS)]
    assert before == [1, 1, 1, 5]
    assert after == [1, 1, 2, 5]
    assert hits_to_kill(2_000, 2_000) == 1


def test_power_law():
    new = power_law(HEALTH, 10_000, 1 / 3)
    assert [round(x) for x in new] == [1_000, 2_154, 4_642, 10_000]


def test_headroom():
    assert close(headroom(40, 1.8), 6.276, 0.001)
    assert close(headroom(5, 5 ** (1 / 3.3)), 3.3, 1e-9)


def test_scale_error():
    # Divisive armor is safe only if K is squished with armor.
    assert close(scale_error(armor_mitigation, (1_000, 1_000), 25, degree=0), 0)
    assert close(armor_mitigation(1_000 / 25, 1_000), 1 / 26)
    assert scale_error(armor_mitigation, (1_000, 1_000), 25, degree=0, scaled=[True, False]) < -0.9
    # The floor of 5 is a constant: attack 120, defense 100, squish by 10.
    assert close(scale_error(floored_damage, (120, 100), 10), 1.5)
    # Time to die is a ratio of two squished values.
    assert close(scale_error(time_to_die, (30_000, 5_000), 25, degree=0), 0)
    # Rounding: a 7-damage tick squished by 20 rounds to zero.
    assert dot_tick(7 / 20, 1) == 0


def test_eras_file():
    eras = load_eras()
    assert len(eras) == 6
    assert eras[-1]["creature_health"] == 4_000_000


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
