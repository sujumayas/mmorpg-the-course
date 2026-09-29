"""Tests for AR101 Lab 03. Values come from the week 3 lecture, section 2.
Run with `python3 test_silhouette.py` or `pytest test_silhouette.py`."""
import os
import sys

from silhouette_test import downsample, iou, load_mask, normalize, worst_pairs

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = {n: load_mask(os.path.join(HERE, "sprites", n + ".txt"))
       for n in ("knight", "mage", "cleric", "rogue")}


def roster():
    return {n: normalize(m) for n, (m, w, h) in RAW.items()}


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_pixel_counts():
    assert {n: len(m) for n, (m, w, h) in RAW.items()} == {
        "knight": 91, "mage": 98, "cleric": 74, "rogue": 74}


def test_iou_basics():
    a = {(0, 0), (1, 0)}
    assert iou(a, a) == 1.0
    assert iou(a, {(5, 5)}) == 0.0
    assert close(iou(a, {(1, 0), (2, 0)}), 1 / 3)
    assert iou(set(), set()) == 1.0


def test_lecture_table():
    ROSTER = roster()
    assert close(iou(ROSTER["cleric"], ROSTER["rogue"]), 70 / 78)
    assert close(iou(ROSTER["knight"], ROSTER["mage"]), 70 / 119)
    assert close(iou(ROSTER["knight"], ROSTER["rogue"]), 70 / 95)
    assert close(iou(ROSTER["mage"], ROSTER["cleric"]), 74 / 98)


def test_normalize_moves_feet_to_origin():
    n = roster()["rogue"]
    assert max(y for _, y in n) == 0
    feet = [x for x, y in n if y == 0]
    assert (min(feet) + max(feet)) // 2 == 0


def test_normalize_ignores_position():
    shifted = {(x + 7, y + 3) for x, y in RAW["rogue"][0]}
    assert close(iou(normalize(shifted), roster()["cleric"]), 70 / 78)


def test_downsample():
    m, w, h = RAW["rogue"]
    half = downsample(m, w, h, 2)
    assert len(half) == 20                       # the dagger is gone
    m, w, h = RAW["knight"]
    assert len(downsample(m, w, h, 2)) == 26
    assert downsample({(0, 0), (1, 1)}, 2, 2, 2) == {(0, 0)}   # exactly half counts
    assert downsample({(0, 0)}, 2, 2, 2) == set()


def test_worst_pairs():
    ROSTER = roster()
    bad = worst_pairs(ROSTER, 0.80)
    assert [(a, b) for a, b, _ in bad] == [("cleric", "rogue")]
    assert close(bad[0][2], 70 / 78)
    bad = worst_pairs(ROSTER, 0.73)
    assert [(a, b) for a, b, _ in bad] == [
        ("cleric", "rogue"), ("cleric", "mage"), ("cleric", "knight"), ("knight", "rogue")]


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
