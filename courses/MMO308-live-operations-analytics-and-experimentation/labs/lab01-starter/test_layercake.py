"""Tests for MMO308 Lab 01. Values come from the week 1 lecture.
Run with `python test_layercake.py` (or pytest, if you have it)."""
from layercake import (BASE, launch_installs, launch_share, layers, lifetime,
                       plateau, retention, wau_series)

TOL = 1e-6


def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_retention_table():
    expected = [1.0, 0.48, 0.306, 0.2376, 0.2025]
    for a, r in enumerate(expected):
        assert close(retention(a, **BASE), r), (a, retention(a, **BASE), r)


def test_lifetime_closed_form():
    assert close(lifetime(**BASE), 4.0)
    assert close(lifetime(0.36, 0.90, 0.30), 3.6 + 0.64 / 0.7)
    assert close(lifetime(0.30, 0.92, 0.30), 4.75)
    long_sum = sum(retention(a, 0.2, 0.95, 0.5) for a in range(3000))
    assert close(lifetime(0.2, 0.95, 0.5), long_sum, 1e-9)


def test_plateau():
    assert close(plateau(10_000, **BASE), 40_000)
    assert close(plateau(12_000, **BASE), 48_000)


def test_layers_shape():
    rows = layers([5, 7, 11], **BASE)
    assert [len(r) for r in rows] == [1, 2, 3]
    assert close(rows[2][0], 5 * 0.306)   # launch cohort, age 2
    assert close(rows[2][1], 7 * 0.48)    # second cohort, age 1
    assert close(rows[2][2], 11 * 1.0)    # newest cohort, install week


def test_wau_series_lecture_values():
    s = wau_series(launch_installs(53), **BASE)
    assert round(s[0]) == 200_000
    assert round(s[1]) == 106_000
    assert round(s[2]) == 76_000
    assert round(s[12]) == 48_473
    assert round(s[26]) == 41_938
    assert round(s[52]) == 40_125


def test_launch_share():
    inst = launch_installs(27)
    assert close(launch_share(inst, 0, **BASE), 1.0)
    assert abs(launch_share(inst, 8, **BASE) - 0.488) < 0.001
    assert abs(launch_share(inst, 26, **BASE) - 0.092) < 0.001


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
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    raise SystemExit(1 if failed else 0)
