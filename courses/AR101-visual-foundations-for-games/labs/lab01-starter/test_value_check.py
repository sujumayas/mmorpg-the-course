"""Tests for AR101 Lab 01. Values come from the week 1 lecture.
Run with `python3 test_value_check.py` or `pytest test_value_check.py`."""
import sys

from value_check import band, check_scene, lightness, srgb_to_linear

TOL = 0.05


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def test_linear_channel():
    assert srgb_to_linear(0) == 0
    assert close(srgb_to_linear(255), 1.0, 1e-9)
    assert close(srgb_to_linear(10), 0.0030353, 1e-6)      # low branch
    assert close(srgb_to_linear(128), 0.2158605, 1e-6)     # power branch


def test_lightness_primaries():
    assert close(lightness((0, 0, 0)), 0.0)
    assert close(lightness((255, 255, 255)), 100.0)
    assert close(lightness((255, 0, 0)), 53.24)
    assert close(lightness((0, 255, 0)), 87.74)
    assert close(lightness((0, 0, 255)), 32.30)


def test_red_equals_mid_gray():
    red, gray = lightness((255, 0, 0)), lightness((128, 128, 128))
    assert close(gray, 53.59)
    assert abs(red - gray) < 0.5


def test_band():
    assert band(0, 4) == 0
    assert band(24.9, 4) == 0
    assert band(25, 4) == 1
    assert band(53.6, 4) == 2
    assert band(100, 4) == 3
    assert band(50, 3) == 1


def test_check_scene():
    colors = {"floor": (128, 128, 128), "potion": (255, 0, 0),
              "pale": (255, 160, 160), "dark": (60, 60, 60)}
    pairs = [("potion", "floor"), ("pale", "floor"), ("potion", "dark")]
    fails = check_scene(colors, pairs, 20)
    assert [(f, g) for f, g, _ in fails] == [("potion", "floor")]
    assert close(fails[0][2], 0.35, 0.05)
    fails = check_scene(colors, pairs, 25)
    assert [(f, g) for f, g, _ in fails] == [("potion", "floor"), ("pale", "floor")]


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
