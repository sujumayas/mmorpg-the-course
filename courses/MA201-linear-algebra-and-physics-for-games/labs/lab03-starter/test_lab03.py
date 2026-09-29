"""Tests for Lab 03. Run from this folder: python test_lab03.py"""
import math
import os
import sys
import traceback

from xform import Xform, Scene

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 1e-3


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def vclose(a, b, tol=TOL):
    return all(close(x, y, tol) for x, y in zip(a, b))


def scene():
    return Scene(os.path.join(HERE, "scene.csv"))


def test_point_and_vector():
    T = Xform.trs(5, 2, 90)
    assert vclose(T.point((3, 1)), (4, 5))
    assert vclose(T.vector((3, 1)), (-1, 3))


def test_compose_ship_crane_hook():
    ship, crane, hook = Xform.trs(100, 50, 90, 2, 2), Xform.trs(3, 0, 30), Xform.trs(4, 0)
    assert vclose((ship * crane).t, (100, 56))
    hw = ship * crane * hook
    assert vclose(hw.t, (96, 62.928))
    assert vclose((ship * (crane * hook)).t, hw.t)   # associativity


def test_inverse_round_trip():
    T = Xform.trs(-3, 7, 37, 1.5, 0.5)
    for p in [(0, 0), (4, -2), (10, 10)]:
        assert vclose(T.inverse().point(T.point(p)), p)
    try:
        Xform(((1, 2), (2, 4)), (0, 0)).inverse()
        assert False, "singular basis must raise ValueError"
    except ValueError:
        pass


def test_guard_local():
    s = scene()
    assert vclose(s.to_local("Guard", (14, 9)), (5.464, 1.464))
    assert s.describe("Guard", (14, 9)) == ("ahead", "left")
    assert s.describe("Guard", (6, 5)) == ("behind", "left")
    assert s.describe("Guard", (6, 1)) == ("behind", "right")


def test_hook_local():
    s = scene()
    assert vclose(s.world("Hook").t, (96, 62.928))
    local = s.to_local("Hook", (97, 66))
    assert vclose(local, (1.080, -1.201))
    assert vclose(s.world("Hook").point(local), (97, 66))


def test_shear_table():
    S = Xform.trs(0, 0, 0, 2, 1)
    for deg, want in [(0, 90.0), (15, 110.56), (30, 123.0), (45, 126.87), (90, 90.0)]:
        W = S * Xform.trs(0, 0, deg)
        assert close(W.corner_angle(), want, 0.01), (deg, W.corner_angle())
        assert close(W.det(), 2.0)
    assert close((Xform.trs(0, 0, 0, 3, 1) * Xform.trs(0, 0, 45)).corner_angle(), 143.13, 0.01)


def test_normal_inverse_transpose():
    S = Xform.trs(0, 0, 0, 2, 1)
    n = S.normal((-math.sqrt(0.5), math.sqrt(0.5)))
    assert vclose(n, (-1 / math.sqrt(5), 2 / math.sqrt(5)))
    R = Xform.trs(0, 0, 30)
    assert vclose(R.normal((1, 0)), R.vector((1, 0)))


def test_transpose_shortcut_only_for_rotations():
    R = Xform.trs(4, 1, 50)
    assert vclose(R.transpose_inverse().point((2, 2)), R.inverse().point((2, 2)))
    s = scene()
    lantern = s.world("Lantern")
    full = lantern.inverse().point((3, 2))
    fast = lantern.transpose_inverse().point((3, 2))
    assert math.dist(full, fast) > 0.1


def test_audit():
    s = scene()
    assert s.audit() == ["Crate", "Flag", "Lamp", "Lantern", "Sign"]
    assert s.audit(tol_deg=40) == ["Flag"]


TESTS = [f for k, f in dict(globals()).items() if k.startswith("test_")]

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
