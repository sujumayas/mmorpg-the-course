"""Tests for MMO406 Lab 02. Values come from the week 2 lecture.
Run with `python test_regions.py` or `pytest test_regions.py`."""
import os
from fractions import Fraction

from regions import (combo_coverage, load, local_share, makeable_anywhere,
                     makeable_here, predator_ratio)

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = load(os.path.join(HERE, "albion.json"))
BOOK = load(os.path.join(HERE, "recipes.json"))["recipes"]


def test_lecture_table():
    assert [local_share(5, 3, k) for k in (1, 2, 3)] == [Fraction(3, 5), Fraction(3, 10), Fraction(1, 10)]
    assert local_share(5, 4, 2) == Fraction(3, 5)
    assert local_share(5, 4, 3) == Fraction(2, 5)
    assert local_share(5, 2, 3) == 0
    assert local_share(5, 5, 3) == 1


def test_check_yourself():
    assert local_share(6, 4, 2) == Fraction(2, 5)
    assert local_share(6, 4, 3) == Fraction(1, 5)
    assert local_share(6, 3, 3) == Fraction(1, 20)


def test_albion_coverage():
    types, regions = WORLD["types"], WORLD["regions"]
    assert combo_coverage(types, regions, 1) == (5, 5)
    assert combo_coverage(types, regions, 2) == (10, 10)
    assert combo_coverage(types, regions, 3) == (5, 10)


def test_forest_recipes():
    here = makeable_here(WORLD["regions"]["Forest"], BOOK)
    assert here == ["leather cap", "saddle", "staff"]


def test_anywhere():
    anywhere = makeable_anywhere(WORLD["regions"], BOOK)
    assert "war banner" not in anywhere
    assert "siege frame" in anywhere
    assert len(anywhere) == 11


def test_swamp_spawns():
    spawns = load(os.path.join(HERE, "spawns.json"))["spawns"]
    assert predator_ratio(spawns) == 36


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
