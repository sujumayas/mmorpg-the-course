"""Tests for MMO406 Lab 04. Values come from the week 4 lecture and lab04.md.
Run with `.venv/bin/python test_lore_clock.py` (from any folder) or pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lore_clock import check_timeline, clock_summary, world_year  # noqa: E402
from thornmere import ERAS, EVENTS, PEOPLE  # noqa: E402

TOL = 1e-9


def close(a, b):
    return abs(a - b) < TOL


def test_world_year_policies():
    assert close(world_year(10, 1200, 0), 1200)
    assert close(world_year(10, 1200, 0.25), 1202.5)
    assert close(world_year(10, 1200, 1), 1210)
    assert close(world_year(10, 1200, 0, 3, 2.5), 1212)


def test_jumps_count_whole_expansions_only():
    # Just before the second expansion (T = 2.5) only one jump has happened.
    assert close(world_year(4.9, 0, 0, 3, 2.5), 3)
    assert close(world_year(5.0, 0, 0, 3, 2.5), 6)


def test_lecture_table():
    rows = {
        (0, 0, None): (0, 60, 16),
        (0.25, 0, None): (2.5, 24, 18.5),
        (1, 0, None): (10, 6, 26),
        (0, 3, 2.5): (12, 5, 28),
    }
    for (r, J, T), (span, density, age) in rows.items():
        s = clock_summary(10, 1200, r, J, T, E=6, a0=16)
        assert close(s["span"], span) and close(s["gap"], span)
        assert close(s["density"], density) and close(s["age"], age)


def test_check_yourself_question():
    s = clock_summary(9, 400, 0.5, 2, 3, E=8, a0=30)
    assert close(s["span"], 10.5)
    assert close(s["age"], 40.5)
    assert abs(s["density"] - 72 / 10.5) < 1e-9


def test_sample_timeline_finds_planted_problems():
    assert check_timeline(EVENTS, PEOPLE, ERAS) == [
        ("E04", "OUTSIDE_ERA"),
        ("E06", "AFTER_DEATH"),
        ("E09", "BEFORE_BIRTH"),
        ("E10", "UNKNOWN_PERSON"),
    ]


def test_edges():
    people = {"A": (100, 150), "B": (120, None)}
    eras = {"X": (100, 200)}
    ok = [
        {"id": "a", "year": 100, "era": "X", "participants": ["A"]},   # birth year is fine
        {"id": "b", "year": 150, "era": "X", "participants": ["A"]},   # death year is fine
        {"id": "c", "year": 200, "era": "X", "participants": ["B"]},   # living, era end inclusive
    ]
    assert check_timeline(ok, people, eras) == []
    bad = [{"id": "d", "year": 90, "era": "Nope", "participants": ["A", "B"]}]
    assert check_timeline(bad, people, eras) == [
        ("d", "BEFORE_BIRTH"), ("d", "BEFORE_BIRTH"), ("d", "OUTSIDE_ERA"),
    ]


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
