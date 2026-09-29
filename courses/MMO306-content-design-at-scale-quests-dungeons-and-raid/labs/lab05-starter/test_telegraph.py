"""Tests for Lab 05. Values come from the week 5 lecture and reaction_times.csv.
Run with `python test_telegraph.py` (or `pytest test_telegraph.py` if you have pytest)."""
from telegraph import (expected_misses, fit_normal, load_times, p_clean, p_empirical,
                       p_normal, required_empirical, required_normal, shift)

TIMES = load_times()


def close(a, b, tol):
    return a is not None and abs(a - b) <= tol


def test_fit():
    mu, sd = fit_normal(TIMES)
    assert len(TIMES) == 400
    assert close(mu, 698.26, 0.01)
    assert close(sd, 153.58, 0.01)


def test_lecture_values():
    assert close(p_normal(1000, 700, 150), 0.97725, 1e-5)
    assert close(p_clean(0.97725, 20, 5), 0.100, 0.001)
    assert close(p_clean(p_normal(1100, 700, 150), 20, 5), 0.681, 0.001)
    assert close(expected_misses(p_normal(1000, 700, 150), 20, 5), 2.275, 0.001)
    assert close(required_normal(0.95, 20, 5, 700, 150), 1192.5, 0.5)
    assert close(required_normal(0.95, 1, 5, 700, 150), 1047.9, 0.5)


def test_empirical_tail_is_heavier():
    mu, sd = fit_normal(TIMES)
    assert p_empirical(1200, TIMES) == 0.99
    assert p_empirical(1000, TIMES) == 0.955
    assert close(p_clean(p_normal(1200, mu, sd), 20, 5), 0.947, 0.002)
    assert close(p_clean(p_empirical(1200, TIMES), 20, 5), 0.366, 0.001)


def test_required_empirical():
    assert required_empirical(0.95, 1, 5, TIMES) == 1170
    assert required_empirical(0.5, 20, 1, TIMES) == 1043
    # 100 trials need p* = 0.99949: only the slowest of the 400 samples qualifies.
    assert required_empirical(0.95, 20, 5, TIMES) == max(TIMES) == 1456


def test_shift():
    moved = shift(TIMES, 170)
    assert moved[0] == TIMES[0] + 170 and len(moved) == len(TIMES)
    assert p_empirical(1370, moved) == p_empirical(1200, TIMES)


if __name__ == "__main__":
    import sys
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
    print(f"{failed} test(s) not passing")
    sys.exit(1 if failed else 0)
