"""MA201 Lab 13 tests. Run `python test_lab13.py` (or `pytest test_lab13.py`).
On the untouched starter every test fails."""
import math

from aim import (intercept_time, aim_point, launch_angles, ballistic_intercept,
                 dodge_budget, simulate_duel)


def near(a, b, tol=1e-3):
    return a is not None and abs(a - b) < tol


def test_crossing_target():
    assert near(intercept_time((1000, 0), (0, 400), 1100), 0.97590)
    p = aim_point((1000, 0), (0, 400), 1100)
    assert p is not None and near(p[0], 1000.0, 0.1) and near(p[1], 390.4, 0.1)


def test_radial_targets():
    assert near(intercept_time((1000, 0), (-400, 0), 1100), 2 / 3)
    assert near(intercept_time((1000, 0), (400, 0), 1100), 1000 / 700)


def test_equal_speeds():
    assert near(intercept_time((20, 0), (-10, 0), 10), 1.0)     # closing: t = -c/b
    assert intercept_time((20, 0), (10, 0), 10) is None          # leaving at equal speed


def test_slow_shot():
    assert near(intercept_time((20, 0), (-12, 0), 10), 20 / 22)  # closing: first root
    assert intercept_time((20, 0), (12, 0), 10) is None          # fleeing and faster


def test_cast_delay():
    t = intercept_time((1000, 0), (0, 345), 2000, delay=0.25)
    assert near(t, 0.51722)
    p = aim_point((1000, 0), (0, 345), 2000, delay=0.25)
    assert p is not None and near(p[1], 264.69, 0.05)


def test_launch_angles():
    a = launch_angles(60, 0, 40)
    assert a is not None and near(a[0], 10.792, 0.01) and near(a[1], 79.208, 0.01)
    b = launch_angles(30, 30, 40)
    assert b is not None and near(b[0], 50.92, 0.02)
    assert launch_angles(200, 0, 40) is None                    # past s^2/g = 163 m


def test_ballistic_intercept():
    r = ballistic_intercept((60.0, 0.0, 0.0), (0.0, 0.0, 0.0), 40.0)
    assert r is not None and near(r[0], 1.527, 0.002)
    t, v = r
    assert near(math.degrees(math.atan2(v[1], v[0])), 10.79, 0.02)
    assert near(math.sqrt(sum(c * c for c in v)), 40.0, 1e-3)
    t, v = ballistic_intercept((60.0, 0.0, 0.0), (0.0, 0.0, 5.0), 40.0)
    assert near(t, 1.540, 0.002) and near(math.degrees(math.atan2(v[2], v[0])), 7.31, 0.02)


def test_dodge_budget():
    assert near(dodge_budget(345, 0.51722, 0.25, 0.25), 178.44, 0.05)
    assert near(dodge_budget(6, 0.5, 0.0, 0.25), 1.5)


def test_duel_straight_runners():
    exact = simulate_duel("exact", 25.0, shots=200)
    body = simulate_duel("body", 25.0, shots=200)
    assert exact > 0.97 and exact > body + 0.3


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for test in TESTS:
        try:
            test()
            passed += 1
            print(f"PASS {test.__name__}")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {test.__name__}: {type(e).__name__} {e}")
    print(f"{passed}/{len(TESTS)} tests passed")
