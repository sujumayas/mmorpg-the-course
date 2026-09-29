"""Tests for Lab 04. Run: python test_lab04.py"""
import math
import sys
import traceback

import camera as c

TOL = 1e-3


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def test_translate_point_and_direction():
    T = c.translate(3, 0, -2)
    assert [round(x, 6) for x in c.apply(T, c.point(1, 1, 1))] == [4, 1, -1, 1]
    assert [round(x, 6) for x in c.apply(T, c.direction(1, 1, 1))] == [1, 1, 1, 0]


def test_order_matters():
    M = c.mat_mul(c.translate(5, 0, 0), c.rot_y(90))
    r = c.apply(M, c.point(1, 0, 0))
    assert close(r[0], 5) and close(r[2], -1)
    W = c.mat_mul(c.rot_y(90), c.translate(5, 0, 0))
    r = c.apply(W, c.point(1, 0, 0))
    assert close(r[0], 0) and close(r[2], -6)


def test_scale():
    r = c.apply(c.scale(2, 3, 4), c.point(1, 1, 1))
    assert [round(x, 6) for x in r] == [2, 3, 4, 1]


def test_rigid_inverse():
    C = c.mat_mul(c.translate(0, 2, 10), c.rot_y(30))
    Vm = c.rigid_inverse(C)
    I = c.mat_mul(Vm, C)
    for i in range(4):
        for j in range(4):
            assert close(I[i][j], 1.0 if i == j else 0.0, 1e-9)
    tree = c.apply(c.rigid_inverse(c.translate(0, 2, 10)), c.point(0, 2, 0))
    assert [round(x, 6) for x in tree] == [0, 0, -10, 1]


def test_perspective_lecture_point():
    P = c.perspective(75, 16 / 9, 0.05, 4000)
    clip = c.apply(P, [2, 1, -10, 1])
    assert close(clip[3], 10)
    assert close(clip[0] / clip[3], 0.1466) and close(clip[1] / clip[3], 0.1303)


def test_project_pixels():
    P = c.perspective(75, 16 / 9, 0.05, 4000)
    px, py, z = c.project(P, c.identity(), (2, 1, -10), 1920, 1080)
    assert close(px, 1100.7, 0.1) and close(py, 469.6, 0.1) and close(z, 0.99, 1e-3)
    P60 = c.perspective(60, 16 / 9, 0.1, 100)
    px, py, _ = c.project(P60, c.identity(), (-3, 0, -12), 1920, 1080)
    assert close(px, 726.2, 0.1) and close(py, 540, 0.1)


def test_project_culls():
    P = c.perspective(75, 16 / 9, 0.05, 4000)
    V = c.identity()
    assert c.project(P, V, (0, 0, 5), 1920, 1080) is None       # behind camera
    assert c.project(P, V, (100, 0, -10), 1920, 1080) is None   # far to the right
    assert c.project(P, V, (0, 0, -5000), 1920, 1080) is None   # beyond far plane


def test_fov_table():
    assert close(c.hfov_from_vfov(75, 16 / 9), 107.51, 0.01)
    assert close(c.hfov_from_vfov(75, 21 / 9), 121.63, 0.01)
    assert close(c.hfov_from_vfov(70, 16 / 9), 102.45, 0.01)
    assert close(c.vfov_from_hfov(107.51, 16 / 9), 75, 0.01)


def test_conventions():
    assert close(c.vfov_from_setting(75, "vertical", 16 / 9), 75)
    assert close(c.vfov_from_setting(75, "horizontal43", 16 / 9), 59.84, 0.01)
    assert close(c.vfov_from_setting(90, "horizontal43", 21 / 9), 73.74, 0.01)
    v = c.vfov_from_setting(100, "horizontal", 16 / 9)
    assert close(c.hfov_from_vfov(v, 16 / 9), 100)


def test_depth():
    assert close(c.z_ndc(0.05, 0.05, 4000), -1, 1e-9)
    assert close(c.z_ndc(0.1, 0.05, 4000), 0, 1e-4)
    assert close(c.z_ndc(4000, 0.05, 4000), 1, 1e-9)
    s300 = c.depth_step(300, 0.05, 4000)
    assert 0.1 < s300 < 0.3, s300
    assert close(c.depth_step(300, 0.1, 4000) * 2, s300, s300 * 0.01)


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
