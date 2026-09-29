"""Tests for Lab 04. Values come from the week 4 lecture.
Run with `python test_ladder.py` or `pytest test_ladder.py`."""
import math

from ladder import (creep_for_landing, gap_exp, gap_linear, ladder, landing, load_tracks,
                    max_width, ranks_at, survival)

S = load_tracks()


def close(a, b, tol=0.005):
    return abs(a - b) <= tol


def test_ladders():
    assert ladder(S["midnight_s1"]) == (220, 289)
    assert ladder(S["midnight_s2"]) == (266, 334)
    assert ladder(S["tww_s2"]) == (610, 678)
    assert ladder(S["tww_s3"]) == (655, 723)


def test_veteran_4():
    assert ranks_at(289, S["midnight_s2"]) == ["Veteran 4"]
    assert "Veteran 4" in ranks_at(678, S["tww_s3"])
    assert ranks_at(250, S["midnight_s1"]) == ["Champion 2", "Veteran 6"]


def test_landing_table():
    assert close(landing(237, 266, 69), -0.42)
    assert close(landing(263, 266, 69), -0.04)
    assert close(landing(276, 266, 69), 0.14)
    assert close(landing(289, 266, 69), 0.33)
    assert close(landing(678, 655, 68), 0.34)


def test_survival():
    assert [survival(i, 220, 46) for i in (237, 250, 263, 276, 289)] == [0, 0, 0, 1, 1]
    assert survival(289, 220, 23) == 3
    assert survival(289, 220, 0) == math.inf


def test_gaps():
    assert close(gap_exp(23, 0.01), 1.26)
    assert close(gap_exp(46, 0.01), 1.58)
    assert close(gap_exp(69, 0.01), 1.99)
    assert close(gap_linear(289, 220), 1.28)
    assert close(gap_linear(159, 146), 1.0757, 0.0005)


def test_design_inverses():
    assert close(creep_for_landing(1 / 3, 69), 46)
    assert close(max_width(2, 0.01), 69.66, 0.01)


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
    raise SystemExit(1 if failed else 0)
