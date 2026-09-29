"""Tests for Lab 06. Run: python test_lab06.py"""
import math
import os
import sys
import traceback

import kinematics as K

HERE = os.path.dirname(os.path.abspath(__file__))


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def test_differences_lecture():
    xs = [200 * math.sin(math.pi * t / 2) for t in (0.4, 0.5, 0.6)]
    assert close(K.forward_diff(xs, 0.1)[1], 203.82)
    assert close(K.central_diff(xs, 0.1)[0], 221.23)
    assert close(K.second_diff(xs, 0.1)[0], -348.23)
    assert len(K.forward_diff(xs, 0.1)) == 2 and len(K.central_diff(xs, 0.1)) == 1


def test_differences_drone():
    xs, ys = [10.0, 12.0, 14.4], [4.0, 4.5, 4.8]
    assert close(K.central_diff(xs, 0.1)[0], 22) and close(K.central_diff(ys, 0.1)[0], 4)
    assert close(K.second_diff(xs, 0.1)[0], 40) and close(K.second_diff(ys, 0.1)[0], -20)


def test_launch_modes():
    assert K.launch_velocity("add", (150.0, 0.0)) == (150.0, 400.0)
    assert K.launch_velocity("nothing", (150.0, 0.0)) == (0.0, 400.0)
    assert K.launch_velocity("add", (0.0, -100.0)) == (0.0, 300.0)
    assert K.launch_velocity("upward", (0.0, -100.0)) == (0.0, 400.0)
    assert K.launch_velocity("upward", (0.0, 100.0)) == (0.0, 500.0)


def test_launch_caps():
    assert K.launch_velocity("upward", (600.0, 300.0), cap_x=250, cap_up=130) == (250.0, 530.0)
    assert K.launch_velocity("upward", (-600.0, -50.0), cap_x=250, cap_up=130) == (-250.0, 400.0)


def test_relative_landing_tables():
    t, dx = K.relative_landing((150.0, 400.0), (150.0, 0.0))
    assert close(t, 0.816, 1e-3) and close(dx, 0.0)
    t, dx = K.relative_landing((0.0, 400.0), (150.0, 0.0))
    assert close(dx, -122.4)
    t, dx = K.relative_landing((0.0, 400.0), (0.0, 100.0))
    assert close(t, 0.612, 1e-3)
    t, dx = K.relative_landing((0.0, 400.0), (0.0, -100.0))
    assert close(t, 1.020, 1e-3)


def test_relative_landing_cart():
    t, dx = K.relative_landing((100.0, 400.0), (100.0, 0.0), (200.0, 0.0))
    assert close(dx, -66.6)
    assert K.relative_landing((0.0, 50.0), (0.0, 100.0)) == (None, None)


def test_rotating_platform():
    v = K.point_velocity((0.0, 0.5, 0.0), (4.0, 0.0, 0.0))
    assert all(close(p, q, 1e-9) for p, q in zip(v, (0.0, 0.0, -2.0)))
    assert close(K.centripetal(1.0, 3.0), 3.0, 1e-9)


def test_find_jumps():
    log = K.load_log(os.path.join(HERE, "platform_log.csv"))
    idx = K.find_jumps(log)
    assert [round(log["t"][i], 2) for i in idx] == [0.5, 2.0], idx


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            passed += 1
            print(f"PASS {t.__name__}")
        except NotImplementedError:
            print(f"TODO {t.__name__}")
        except Exception:
            print(f"FAIL {t.__name__}")
            traceback.print_exc(limit=1)
    print(f"{passed}/{len(TESTS)} tests passed")
    sys.exit(0 if passed == len(TESTS) else 1)
