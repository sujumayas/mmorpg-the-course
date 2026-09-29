"""Tests for AR101 Lab 05. Values come from the week 5 lecture.
Run with `.venv/bin/python test_palette.py`. Exit code is 0 only if all pass."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from palette import (check_palette, even_ramp, harmony, hex_to_rgb, lerp, lerp_hue,
                     lightness, ramp)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def same_colors(got, want):
    """Hex lists equal within 1 per channel (float rounding at .5 may differ)."""
    return len(got) == len(want) and all(
        max(abs(a - b) for a, b in zip(hex_to_rgb(g), hex_to_rgb(w))) <= 1
        for g, w in zip(got, want))


def test_lerp_hue():
    assert close(lerp_hue(350, 30, 0.5), 10)
    assert close(lerp_hue(30, 350, 0.25), 20)
    assert close(lerp_hue(200, 60, 0.5), 130)
    assert close(lerp_hue(160, 80, 0.25), 140)
    assert close(lerp_hue(10, 10, 0.7), 10)
    assert 0 <= lerp_hue(350, 30, 0.25) < 360


def test_ramp_lecture_table():
    assert same_colors(ramp(120, 120, 60, 60, 20, 90, 5), ["143314", "266026", "388c38", "4ab94a", "5ce65c"])
    assert same_colors(ramp(160, 80, 70, 45, 20, 90, 5), ["1c332b", "29603b", "2a8c2a", "72b94f", "c3e67e"])


def test_ramp_check_yourself():
    assert same_colors(ramp(350, 40, 80, 55, 25, 95, 4), ["401d23", "7b2d23", "b76734", "f2c66d"])
    assert same_colors(ramp(250, 190, 60, 40, 15, 85, 4), ["191726", "2e3662", "49739d", "82cad9"])


def test_harmony():
    assert harmony(20, "monochromatic") == [20]
    assert harmony(20, "analogous") == [350, 20, 50]
    assert harmony(20, "complementary") == [20, 200]
    assert harmony(20, "split") == [20, 170, 230]
    assert harmony(20, "triadic") == [20, 140, 260]
    assert harmony(20, "tetradic") == [20, 110, 200, 290]
    assert harmony(200, "split") == [200, 350, 50]


def test_even_ramp():
    hexes = even_ramp(160, 80, 70, 45, 20, 85, 5)
    assert len(hexes) == 5
    for i, h in enumerate(hexes):
        target = lerp(20, 85, i / 4)
        assert abs(lightness(*hex_to_rgb(h)) - target) < 0.6, (i, h)


def test_even_ramp_lowers_saturation_when_needed():
    # A blue ramp cannot reach L* 80 at S = 60; the top step must lose saturation.
    hexes = even_ramp(250, 220, 60, 60, 20, 80, 3)
    assert abs(lightness(*hex_to_rgb(hexes[-1])) - 80) < 0.6


def test_checker_on_broken_zone():
    problems = check_palette(os.path.join(HERE, "broken_zone.hex"))
    text = "\n".join(problems)
    assert "ramp stone: step 2" in text           # 4a4852 -> 56545e is too small a rise
    assert "reserved 4dbf4d: hue within" in text  # reserved green inside the moss hues
    assert "17 unique" not in text


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
