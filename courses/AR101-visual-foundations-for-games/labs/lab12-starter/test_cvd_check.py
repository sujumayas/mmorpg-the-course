"""Tests for AR101 Lab 12. Numbers come from the week 12 lecture.
Run with `python test_cvd_check.py` or `pytest test_cvd_check.py`."""
import sys

from cvd_check import audit, contrast_ratio, lightness, simulate

FLOOR, RED, GREEN = (96, 112, 72), (200, 48, 40), (64, 168, 72)


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def test_simulate_normal_is_identity():
    assert simulate(RED, "normal") == RED


def test_simulate_lecture_table():
    assert simulate(FLOOR, "protan") == (116, 107, 69)
    assert simulate(RED, "protan") == (95, 85, 37)
    assert simulate(RED, "deutan") == (133, 118, 33)
    assert simulate(GREEN, "deutan") == (158, 144, 79)
    assert simulate(RED, "tritan") == (220, 0, 48)


def test_simulate_clips():
    # pure blue under tritanopia pushes red below zero before clipping
    r, g, b = simulate((0, 0, 255), "tritan")
    assert r == 0 and 0 <= g <= 255 and 0 <= b <= 255


def test_contrast_ratio():
    assert close(contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0)
    assert close(contrast_ratio((255, 255, 255), (0, 0, 0)), 21.0)
    assert close(contrast_ratio((32, 16, 16), FLOOR), 3.42, 0.01)
    assert close(contrast_ratio(RED, RED), 1.0)


def test_audit_rows_and_values():
    rows = audit({"floor": FLOOR, "red": RED}, [("red", "floor")])
    assert [r[2] for r in rows] == ["normal", "protan", "deutan", "tritan"]
    # simulate() rounds to whole sRGB values, so allow 0.2 from the lecture's table
    for row, want in zip(rows, [0.0, 9.0, 4.8, 1.5]):
        assert close(row[3], want, 0.2)
    assert not any(r[5] for r in rows)


def test_audit_fixed_design_passes():
    colors = {"floor": FLOOR, "rim": (32, 16, 16), "fill": (255, 176, 48)}
    rows = audit(colors, [("rim", "floor"), ("fill", "floor")])
    assert len(rows) == 8 and all(r[5] for r in rows)
    for row, want in zip(rows[:4], [3.42, 3.50, 3.36, 3.39]):
        assert close(row[4], want, 0.02)
    assert close(lightness(simulate((255, 176, 48), "deutan")), 80.1, 0.2)


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
    sys.exit(1 if failed else 0)
