"""Tests for AR101 Lab 04. Values come from the week 4 lecture tables.
Run with `.venv/bin/python test_color_tools.py`. Exit code is 0 only if all pass."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_tools import (HERE, hex_to_rgb, hsv_to_rgb, lightness, load_hex_file,
                         match_value, nearest_value, rgb_to_hsv, swap)


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def same_colors(got, want):
    """Hex lists equal within 1 per channel (float rounding at .5 may differ)."""
    return len(got) == len(want) and all(
        max(abs(a - b) for a, b in zip(hex_to_rgb(g), hex_to_rgb(w))) <= 1
        for g, w in zip(got, want))


def test_hex():
    assert hex_to_rgb("#FF004D") == (255, 0, 77)
    assert hex_to_rgb(" 5f574f ") == (95, 87, 79)


def test_rgb_to_hsv():
    for rgb, hue in {(255, 0, 0): 0, (255, 255, 0): 60, (0, 255, 0): 120,
                     (0, 255, 255): 180, (0, 0, 255): 240, (255, 0, 255): 300}.items():
        h, s, v = rgb_to_hsv(*rgb)
        assert close(h, hue) and close(s, 100) and close(v, 100), rgb
    h, s, v = rgb_to_hsv(51, 102, 153)
    assert close(h, 210) and close(s, 66.67, 0.01) and close(v, 60)
    h, s, v = rgb_to_hsv(95, 87, 79)
    assert close(h, 30) and close(s, 16.84, 0.01) and close(v, 37.25, 0.01)
    h, s, v = rgb_to_hsv(255, 0, 77)            # hue near 360 must wrap
    assert close(h, 341.88, 0.01)
    assert rgb_to_hsv(0, 0, 0) == (0, 0, 0)
    h, s, _ = rgb_to_hsv(128, 128, 128)
    assert h == 0 and s == 0


def test_hsv_to_rgb():
    assert hsv_to_rgb(240, 60, 75) == (77, 77, 191)     # hand check in section 2
    assert hsv_to_rgb(210, 66.67, 60) == (51, 102, 153)
    assert hsv_to_rgb(360 + 120, 70, 25) == (19, 64, 19)
    assert hsv_to_rgb(-120, 100, 100) == (0, 0, 255)


def test_round_trip():
    for rgb in [(19, 64, 19), (255, 0, 77), (95, 87, 79), (220, 220, 255)]:
        assert hsv_to_rgb(*rgb_to_hsv(*rgb)) == rgb


def test_naive_swap_matches_lecture():
    slime = load_hex_file(os.path.join(HERE, "slime.hex"))
    assert same_colors(swap(slime, 120, keep_value=False), ["131340", "2d2d80", "4d4dbf", "9d9df2"])
    assert same_colors(swap(slime, 240, keep_value=False), ["401313", "802d2d", "bf4d4d", "f29d9d"])


def test_match_value():
    s, v = match_value(23.2, 240, 70)            # dark step: V rises, S kept
    assert close(s, 70) and abs(v - 53.5) < 0.3
    s, v = match_value(69.0, 240, 60)            # base step: hits the ceiling
    assert close(v, 100) and abs(s - 37.8) < 0.3
    s, v = match_value(45, 0, 80)                # check yourself 3, red
    assert close(s, 80) and abs(v - 79.8) < 0.3
    s, v = match_value(45, 240, 80)              # check yourself 3, blue
    assert close(v, 100) and abs(s - 68.8) < 0.3


def test_keep_value_swap():
    slime = load_hex_file(os.path.join(HERE, "slime.hex"))
    for rotation in (120, 240):
        new = swap(slime, rotation)
        for a, b in zip(slime, new):
            la, lb = lightness(*hex_to_rgb(a)), lightness(*hex_to_rgb(b))
            assert abs(la - lb) < 0.6, (rotation, a, b, la, lb)
    assert swap(["808080"], 90) == ["808080"]


def test_nearest_value():
    pico8 = load_hex_file(os.path.join(HERE, "pico8.hex"))
    assert nearest_value("ff004d", pico8) == "83769c"    # L* 53.8 -> 52.0
    assert nearest_value("29adff", pico8) == "ff77a8"    # L* 67.7 -> 67.5
    assert nearest_value("000000", pico8) == "1d2b53"


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e} is not written yet")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    sys.exit(1 if failed else 0)
