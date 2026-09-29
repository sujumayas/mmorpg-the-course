"""Tests for Lab 01. Values come from the week 1 lecture.
Run with `python3 test_ghosts.py` or `pytest test_ghosts.py`."""
from ghosts import (DOWN, LEFT, LEVEL_1, LEVEL_5_UP, LEVELS_2_TO_4, RIGHT, UP,
                    ahead, choose_direction, mode_at, scatter_seconds, target)

ALL = {UP, LEFT, DOWN, RIGHT}
CLYDE_CORNER = (0, 30)


def test_ahead():
    assert ahead((14, 20), RIGHT, 4) == (18, 20)
    assert ahead((14, 20), DOWN, 2) == (14, 22)
    assert ahead((14, 20), UP, 4) == (10, 16)            # the overflow bug
    assert ahead((14, 20), UP, 4, bug=False) == (14, 16)


def test_lecture_board_facing_up():
    pac, b = (14, 20), (20, 14)
    assert target("blinky", pac, UP, b, b, None) == (14, 20)
    assert target("pinky", pac, UP, (2, 2), b, None) == (10, 16)
    assert target("inky", pac, UP, (18, 18), b, None) == (4, 22)
    assert target("clyde", pac, UP, (10, 24), b, CLYDE_CORNER) == CLYDE_CORNER


def test_lecture_board_facing_right():
    pac, b = (14, 20), (20, 14)
    assert target("pinky", pac, RIGHT, (2, 2), b, None) == (18, 20)
    assert target("inky", pac, RIGHT, (18, 18), b, None) == (12, 26)


def test_bug_off():
    assert target("inky", (14, 20), UP, (18, 18), (20, 14), None, bug=False) == (8, 22)


def test_check_yourself_targets():
    pac, b = (10, 12), (14, 8)
    assert target("pinky", pac, LEFT, (0, 0), b, None) == (6, 12)
    assert target("inky", pac, LEFT, (0, 0), b, None) == (2, 16)
    assert target("clyde", pac, LEFT, (4, 18), b, CLYDE_CORNER) == pac        # 72
    assert target("clyde", pac, LEFT, (5, 16), b, CLYDE_CORNER) == CLYDE_CORNER  # 41


def test_turn_rule_tie_goes_up():
    assert choose_direction((5, 5), RIGHT, ALL, (9, 1)) == UP


def test_turn_rule_never_reverses():
    # Heading left: right is the reverse even though it points at the target.
    assert choose_direction((7, 5), LEFT, ALL, (10, 2)) == UP
    # Target straight behind: right is barred, so down (170) beats left (196).
    assert choose_direction((7, 5), LEFT, {LEFT, RIGHT, DOWN}, (20, 5)) == DOWN


def test_turn_rule_dead_end_reverses():
    assert choose_direction((3, 3), UP, {DOWN}, (0, 0)) == DOWN


def test_mode_at():
    assert mode_at(0, LEVEL_1) == "scatter"
    assert mode_at(6.99, LEVEL_1) == "scatter"
    assert mode_at(7, LEVEL_1) == "chase"
    assert mode_at(27.5, LEVEL_1) == "scatter"
    assert mode_at(84, LEVEL_1) == "chase"
    assert mode_at(10_000, LEVEL_1) == "chase"


def test_scatter_seconds():
    assert abs(scatter_seconds(LEVEL_1, 60) - 19) < 1e-9
    assert abs(scatter_seconds(LEVEL_1, 180) - 24) < 1e-9
    assert abs(scatter_seconds(LEVELS_2_TO_4, 180) - 19) < 1e-9
    assert abs(scatter_seconds(LEVEL_5_UP, 55) - 15) < 1e-9


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
    print(f"\n{failed} test(s) not passing" if failed else "\nall tests pass")
    raise SystemExit(1 if failed else 0)
