"""Tests for Lab 01. Run from this folder: python test_lab01.py"""
import math
import os
import sys
import traceback

import vec3 as v

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 1e-3


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def vclose(a, b, tol=TOL):
    return all(close(x, y, tol) for x, y in zip(a, b))


def test_cross_basics():
    assert vclose(v.cross((1, 0, 0), (0, 1, 0)), (0, 0, 1))
    assert vclose(v.cross((0, 1, 0), (0, 0, 1)), (1, 0, 0))
    assert vclose(v.cross((2, 1, 0), (1, 3, 2)), (2, -4, 5))
    assert vclose(v.cross((1, 2, 3), (4, 5, 6)), (-3, 6, -3))


def test_cross_properties():
    a, b = (1.5, -2.0, 0.5), (0.25, 4.0, -3.0)
    c = v.cross(a, b)
    assert close(v.dot(c, a), 0) and close(v.dot(c, b), 0)
    assert vclose(v.cross(b, a), v.scale(c, -1))
    assert vclose(v.cross(a, a), (0, 0, 0))


def test_normalize_guard():
    assert vclose(v.normalize((3, 0, 4)), (0.6, 0, 0.8))
    assert v.normalize((0, 0, 0)) is None
    assert v.normalize((1e-12, 0, 0)) is None


def test_ramp_normal_and_area():
    n = v.triangle_normal((0, 0, 0), (0, 0, 1), (4, 3, 0))
    assert vclose(n, (-0.6, 0.8, 0))
    assert close(v.triangle_area((0, 0, 0), (0, 0, 1), (4, 3, 0)), 2.5)
    assert v.triangle_normal((1, 0, 1), (2, 0, 2), (3, 0, 3)) is None
    assert close(v.triangle_area((1, 0, 0), (0, 1, 0), (0, 0, 1)), math.sqrt(3) / 2)


def test_lecture_table():
    n11 = v.triangle_normal((0, 0, 0), (0, 0, 1), (1, 1, 0))
    assert (v.classify(n11, "ue5"), v.classify(n11, "ue3"), v.classify(n11, "godot47")) == ("wall", "floor", "floor")
    n = v.triangle_normal((0, 0, 0), (0, 0, 1), (1, 1.01, 0))
    assert (v.classify(n, "ue5"), v.classify(n, "ue3"), v.classify(n, "godot47")) == ("wall", "floor", "floor")
    n = v.triangle_normal((0, 0, 0), (0, 0, 1), (5, 6, 0))
    assert (v.classify(n, "ue5"), v.classify(n, "ue3"), v.classify(n, "godot47")) == ("wall", "wall", "wall")
    n = v.triangle_normal((0, 0, 0), (0, 0, 1), (4, 1, 0))
    assert v.classify(n, "ue5") == "floor"


def test_flipped_winding_is_ceiling_in_godot():
    n = v.triangle_normal((0, 0, 0), (1, 1, 0), (0, 0, 1))
    assert vclose(n, (0.7071, -0.7071, 0))
    assert v.classify(n, "godot47") == "ceiling"
    assert v.classify(n, "ue5") == "wall"


def test_custom_up():
    # Z-up world (Unreal): a 1:1 ramp rising along x, normal (-0.7071, 0, 0.7071).
    n = v.normalize((-1, 0, 1))
    assert v.classify(n, "ue5", up=(0, 0, 1)) == "wall"
    assert v.classify(n, "ue3", up=(0, 0, 1)) == "floor"
    assert v.classify((0, 0, 1), "ue5", up=(0, 0, 1)) == "floor"


def test_side_by_engine():
    assert close(v.side((0, 0, -1), (1, 0, 0), (0, 1, 0)), -1)   # Godot: right is negative
    assert close(v.side((0, 0, 1), (1, 0, 0), (0, 1, 0)), 1)     # Unity: right is positive
    assert close(v.side((1, 0, 0), (0, 1, 0), (0, 0, 1)), 1)     # Unreal: right is positive
    assert close(v.side((0, 0, 1), (-3, 0, 4), (0, 1, 0)), -3)   # check-yourself 3


def test_level_areas():
    tris = v.load_level(os.path.join(HERE, "level.csv"))
    assert len(tris) == 18
    g = v.area_by_class(tris, "godot47")
    assert set(g) == {"floor", "wall", "ceiling", "degenerate"}
    assert close(g["floor"], 100 + 2 * math.hypot(4, 1) + 2 * 5 + 2 * math.hypot(2, 2) + 2 * math.hypot(2, 2.02), 1e-2)
    assert close(g["ceiling"], 100 + math.hypot(2, 2), 1e-2)
    assert close(g["wall"], 30 + 2 * math.hypot(5, 6), 1e-2)
    assert close(g["degenerate"], 0)
    u = v.area_by_class(tris, "ue5")
    assert close(u["floor"], g["floor"] - 2 * math.hypot(2, 2) - 2 * math.hypot(2, 2.02), 1e-2)
    assert close(u["ceiling"], 0)


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
