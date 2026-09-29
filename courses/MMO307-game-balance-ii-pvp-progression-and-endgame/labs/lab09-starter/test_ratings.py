"""Tests for Lab 09, from the week 9 lecture.
Run with `python test_ratings.py` or `pytest test_ratings.py`."""
from ratings import (MU, SIGMA, c_for_reset, g, glicko_expected, glicko_update,
                     rd_after_idle, trueskill_rate, win_probability)


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_g_and_expected():
    assert round(g(30), 4) == 0.9955
    assert round(g(300), 4) == 0.7242
    assert round(glicko_expected(1500, 1400, 30), 3) == 0.639


def test_glickman_example():
    r, rd = glicko_update(1500, 200, [(1400, 30, 1), (1550, 100, 0), (1700, 300, 0)])
    assert round(r) == 1464
    assert round(rd, 1) == 151.4


def test_effective_k_table():
    r, rd = glicko_update(1500, 350, [(1500, 50, 1)])
    assert round(r - 1500, 1) == 175.0 and round(rd, 1) == 248.1
    r, rd = glicko_update(1500, 100, [(1500, 50, 1)])
    assert round(r - 1500, 1) == 26.3 and round(rd, 1) == 96.2


def test_no_games():
    assert glicko_update(1600, 80, []) == (1600, 80)


def test_idle_growth():
    assert round(rd_after_idle(50, 63.2, 1), 1) == 80.6
    assert round(rd_after_idle(50, 63.2, 5), 1) == 149.9
    assert rd_after_idle(50, 63.2, 40) == 350
    assert round(c_for_reset(50, 30), 1) == 63.2
    assert round(c_for_reset(40, 24), 1) == 71.0


def test_trueskill_1v1_matches_library():
    (a,), (b,) = trueskill_rate([(MU, SIGMA)], [(MU, SIGMA)], 0.10)
    assert round(a[0], 3) == 29.396 and round(a[1], 3) == 7.171
    assert round(b[0], 3) == 20.604 and round(b[1], 3) == 7.171
    (a,), _ = trueskill_rate([(MU, SIGMA)], [(MU, SIGMA)])
    assert round(a[0], 3) == 29.205


def test_trueskill_teams():
    vet, rival, new = (30.0, 2.0), (28.0, 2.0), (MU, SIGMA)
    up, down = trueskill_rate([vet, vet, new], [rival] * 3)
    assert round(up[0][0] - 30, 2) == 0.22
    assert round(up[2][0] - 25, 2) == 3.76
    assert round(up[2][1], 2) == 7.35
    assert round(28 - down[0][0], 2) == 0.22


def test_win_probability():
    assert near(win_probability([(MU, SIGMA)], [(MU, SIGMA)]), 0.5)
    p = win_probability([(30, 2), (30, 2), (MU, SIGMA)], [(28, 2)] * 3)
    assert round(p, 3) == 0.529
    assert near(p + win_probability([(28, 2)] * 3, [(30, 2), (30, 2), (MU, SIGMA)]), 1)


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
