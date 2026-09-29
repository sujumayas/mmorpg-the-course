"""MA201 Lab 09 tests. Run `python test_lab09.py` (or `pytest test_lab09.py`).
Numbers come from the week 9 lecture. On the untouched starter every test fails."""
from narrow import (aabb_aabb, aabb_sphere, make_box, projection_radius, sat_obb,
                    sphere_sphere)

A = make_box((0, 0), 2, 1, 0)


def close(a, b, tol=1e-4):
    return all(abs(x - y) < tol for x, y in zip(a, b))


def test_sphere_sphere_lecture():
    n, d = sphere_sphere((0, 0, 0), 1.0, (1.2, 0.9, 0.0), 0.8)
    assert close(n, (0.8, 0.6, 0.0)) and abs(d - 0.3) < 1e-9
    n, d = sphere_sphere((0, 0, 0), 1.0, (1.2, 0.9, 0.8), 0.8)
    assert close(n, (0.7059, 0.5294, 0.4706)) and abs(d - 0.1) < 1e-9


def test_sphere_sphere_miss_and_coincident():
    assert sphere_sphere((1, 2, 2), 1.5, (3, 3, 4), 1.5) is None     # touching only
    n, d = sphere_sphere((0, 0, 0), 1.0, (0, 0, 0), 1.0)
    assert n == (0, 1, 0) and abs(d - 2.0) < 1e-9


def test_aabb_aabb():
    n, d = aabb_aabb((0, 0, 0), (1, 1, 1), (1.5, 0.2, -1.8), (1, 1, 1))
    assert close(n, (0, 0, -1)) and abs(d - 0.2) < 1e-9
    assert aabb_aabb((0, 0, 0), (1, 1, 1), (2.5, 0, 0), (1, 1, 1)) is None


def test_aabb_sphere():
    n, d = aabb_sphere((0, 0, 0), (1, 1, 1), (1.6, 1.8, 0.0), 1.1)
    assert close(n, (0.6, 0.8, 0.0)) and abs(d - 0.1) < 1e-9


def test_projection_radius():
    b = make_box((0, 0), 1, 1, 45)
    assert abs(projection_radius(b, (1.0, 0.0)) - 1.4142) < 1e-4
    assert abs(projection_radius(A, (0.70710678, 0.70710678)) - 2.1213) < 1e-4
    c = make_box((0, 0), 2, 1, 30)
    assert abs(projection_radius(c, (1.0, 0.0)) - 2.2321) < 1e-4


def test_case1_separated():
    assert sat_obb(A, make_box((3.0, 1.5), 1, 1, 45)) is None
    assert sat_obb(A, make_box((2.8, 1.4), 1, 1, 45)) is not None


def test_case2_mtv():
    n, d = sat_obb(A, make_box((2.8, 1.4), 1, 1, 45))
    assert close(n, (0.7071, 0.7071)) and abs(d - 0.1515) < 1e-4


def test_mtv_points_from_a_to_b():
    n, d = sat_obb(A, make_box((-2.8, -1.4), 1, 1, 45))
    assert close(n, (-0.7071, -0.7071)) and abs(d - 0.1515) < 1e-4


def test_activity_boxes():
    a = make_box((0, 0), 3, 1, 0)
    n, d = sat_obb(a, make_box((3.5, 1.8), 1, 0.5, 30))
    assert close(n, (0.0, 1.0)) and abs(d - 0.1330) < 1e-4
    assert sat_obb(a, make_box((3.5, 2.0), 1, 0.5, 30)) is None


def test_resolving_by_mtv_leaves_zero_overlap():
    b = make_box((2.8, 1.4), 1, 1, 45)
    n, d = sat_obb(A, b)
    moved = make_box((2.8 + n[0] * d, 1.4 + n[1] * d), 1, 1, 45)
    assert sat_obb(A, make_box((moved["c"][0] + 1e-6, moved["c"][1] + 1e-6), 1, 1, 45)) is None
    back = make_box((moved["c"][0] - 1e-3, moved["c"][1] - 1e-3), 1, 1, 45)
    assert sat_obb(A, back) is not None


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"PASS {name}")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__} {e}")
    print(f"{passed}/{len(tests)} tests passed")
