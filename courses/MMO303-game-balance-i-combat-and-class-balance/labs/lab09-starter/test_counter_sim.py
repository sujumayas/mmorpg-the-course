"""Tests for Lab 09, from the week 9 lecture's Knight buff (70/60/60).
Run with `python3 test_counter_sim.py` or `pytest test_counter_sim.py`."""
from counter_sim import (expected_margins, load_winrates, margins_from_winrates,
                         run, stable_mix3, step, triangle_winrates, win_rates)

THIRD = [1 / 3] * 3
def buff():
    return margins_from_winrates(triangle_winrates(0.70, 0.60, 0.60))


def pct(xs):
    return [round(100 * x, 1) for x in xs]


def test_antisymmetric():
    for M in (buff(), margins_from_winrates(load_winrates()[1])):
        n = len(M)
        assert all(abs(M[i][j] + M[j][i]) < 1e-9 for i in range(n) for j in range(n))


def test_stable_mix():
    assert pct(stable_mix3(0.4, 0.2, 0.2)) == [25.0, 50.0, 25.0]
    k, m, r = stable_mix3(0.4, 0.2, 0.2)
    assert all(abs(e) < 1e-9 for e in expected_margins([k, m, r], buff()))


def test_week1_win_rates():
    assert pct(win_rates(THIRD, buff())) == [53.3, 50.0, 46.7]


def test_one_step():
    assert pct(step(THIRD, buff(), eta=1.0)) == [35.6, 33.3, 31.1]


def test_run_length_and_sum():
    path = run(THIRD, buff(), weeks=30)
    assert len(path) == 31
    assert all(abs(sum(s) - 1) < 1e-9 for s in path)


def test_five_class_regular_tournament():
    names, W = load_winrates()
    M = margins_from_winrates(W)
    assert all(abs(e) < 1e-9 for e in expected_margins([0.2] * 5, M))


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
