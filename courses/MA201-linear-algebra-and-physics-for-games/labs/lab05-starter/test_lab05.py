"""Tests for Lab 05. Run: python test_lab05.py"""
import math
import os
import sys
import traceback

import quat as Q

HERE = os.path.dirname(os.path.abspath(__file__))


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def vclose(u, v, tol=1e-4):
    return all(close(p, q, tol) for p, q in zip(u, v))


def test_axis_angle():
    q = Q.from_axis_angle((0, 2, 0), 90)
    assert vclose(q, (0.70711, 0, 0.70711, 0))
    axis, deg = Q.to_axis_angle((0.92388, 0, 0, 0.38268))
    assert close(deg, 45, 1e-3) and vclose(axis, (0, 0, 1))


def test_normalize():
    assert vclose(Q.normalize((2, 0, 0, 0)), (1, 0, 0, 0))
    assert close(math.sqrt(Q.dot(*(Q.normalize((1, 2, 3, 4)),) * 2)), 1)


def test_rotate_matches_matrix():
    assert vclose(Q.rotate(Q.from_axis_angle(Q.UP, 90), (1, 0, 0)), (0, 0, -1))
    assert vclose(Q.rotate(Q.from_axis_angle(Q.RIGHT, 90), (0, 0, -1)), (0, 1, 0))


def test_order():
    yaw, pitch = Q.from_axis_angle(Q.UP, 90), Q.from_axis_angle(Q.RIGHT, 90)
    assert vclose(Q.rotate(Q.mul(yaw, pitch), (0, 0, -1)), (0, 1, 0))
    assert vclose(Q.rotate(Q.mul(pitch, yaw), (0, 0, -1)), (-1, 0, 0))


def test_gimbal_lock():
    a = Q.from_euler_yxz(30, 90, 0)
    b = Q.from_euler_yxz(0, 90, -30)
    assert vclose(a, (0.68301, 0.68301, 0.18301, -0.18301))
    assert close(Q.turn_between(a, b), 0, 1e-3)


def test_turn_between_double_cover():
    a, b = Q.from_axis_angle(Q.UP, 170), Q.from_axis_angle(Q.UP, -170)
    assert close(Q.turn_between(a, b), 20, 1e-3)
    assert close(Q.turn_between(a, tuple(-c for c in a)), 0, 1e-3)


def test_slerp_long_and_short():
    a, b = Q.from_axis_angle(Q.UP, 170), Q.from_axis_angle(Q.UP, -170)
    naive = [round(Q.yaw_of(Q.slerp(a, b, t, False)), 1) for t in (0.25, 0.5, 0.75)]
    short = [round(Q.yaw_of(Q.slerp(a, b, t)), 1) for t in (0.25, 0.5, 0.75)]
    assert naive == [85.0, 0.0, -85.0], naive
    assert [abs(s) for s in short] == [175.0, 180.0, 175.0], short


def test_slerp_identical():
    a = Q.from_axis_angle(Q.UP, 45)
    assert vclose(Q.slerp(a, a, 0.3), a)
    assert close(Q.yaw_of(Q.slerp(a, Q.from_axis_angle(Q.UP, 405), 0.5)), 45, 1e-3)


def test_nlerp():
    a, b = Q.from_axis_angle(Q.UP, 0), Q.from_axis_angle(Q.UP, 120)
    assert close(Q.yaw_of(Q.nlerp(a, b, 0.25)), 27.8, 0.05)


def test_long_way_segments_small():
    neg = lambda q: tuple(-c for c in q)
    keys = [(0.0, Q.from_axis_angle(Q.UP, 10)), (0.5, neg(Q.from_axis_angle(Q.UP, 30))),
            (1.0, neg(Q.from_axis_angle(Q.UP, 50))), (1.5, Q.from_axis_angle(Q.UP, 70))]
    assert Q.long_way_segments(keys) == [0, 2]


def test_replay_file():
    keys = Q.load_keys(os.path.join(HERE, "turret_keys.csv"))
    bad = Q.long_way_segments(keys)
    assert len(bad) >= 1
    assert Q.max_yaw_step(keys, 60, shortest=True) < 2.0
    assert Q.max_yaw_step(keys, 60, shortest=False) > 5.0


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
