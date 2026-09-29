"""Tests for GD202 Lab 06. Values come from the week 6 lecture and lab06.md.
Run with `.venv/bin/python test_quest_board.py` (from any folder) or pytest."""
import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quest_board import (Quest, decay_percent, load_board, minutes, paid_xp,  # noqa: E402
                         rate, required_listed_xp)

BOARD = {q.name: q for q in load_board()}
WOLVES, OGRE = BOARD["Wolves at the mill"], BOARD["The ogre's tithe"]
LETTER, BONES, CAVE = BOARD["Letter to the ferryman"], BOARD["Old bones"], BOARD["Smuggler's cave"]


def close(a, b, tol=0.05):
    return abs(a - b) < tol


def test_decay_table():
    assert [decay_percent(d) for d in range(-3, 13)] == \
        [100] * 9 + [80, 60, 40, 20, 10, 10, 10]


def test_paid_xp_level_20():
    assert [paid_xp(q, 20) for q in (WOLVES, OGRE, LETTER, BONES, CAVE)] == [1800, 4200, 900, 800, 3000]


def test_paid_xp_rounding():
    q = Quest("odd", 10, 1234, 1, 1)
    assert paid_xp(q, 16) == 985    # 1234 x 0.8 = 987.2 -> 985
    assert paid_xp(q, 20) == 125    # 123.4 -> 125
    assert paid_xp(Quest("half", 10, 1225, 1, 1), 20) == 125  # 122.5 rounds up


def test_rates_level_20():
    assert close(rate(OGRE, 20), 182.6)
    assert close(rate(BONES, 20), 100.0)
    assert close(rate(CAVE, 20), 214.3)
    assert close(rate(LETTER, 20), 225.0)


def test_level_17_and_25():
    assert close(rate(BONES, 17), 250.0)
    assert paid_xp(WOLVES, 25) == 1440 and close(rate(WOLVES, 25), 180.0)
    assert paid_xp(LETTER, 25) == 540


def test_mount():
    assert close(minutes(OGRE, 0.5), 18.5)
    assert close(rate(OGRE, 20, 0.5), 227.0)


def test_complication_tax():
    collapsed = replace(CAVE, complication=4)
    assert minutes(collapsed) == 18
    assert close(rate(collapsed, 20), 166.7)
    assert required_listed_xp(collapsed, 20, 200) == 3600


def test_required_with_decay():
    assert required_listed_xp(OGRE, 20, 200) == 4600
    # Smuggler's cave at level 27 (60%) must pay 200 x 14 = 2,800. 4,665 x 0.6 = 2,799,
    # which rounds to 2,800, so 4,665 is enough; 4,660 pays 2,795 and is not.
    assert required_listed_xp(CAVE, 27, 200) == 4665


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
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
