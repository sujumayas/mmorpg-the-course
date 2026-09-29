"""Lab 14 tests. Run with `pytest test_ladder.py` or `python test_ladder.py`.
All tests fail on the starter and pass on a correct solution."""
from ladder import (class_win_rate, elo_update, expected_score, representation,
                    simulate_ladder, top_share, window_win_rate)

TOL = 1e-4


def test_expected_score():
    assert abs(expected_score(1500, 1500) - 0.5) < TOL
    assert abs(expected_score(1600, 1500) - 0.6401) < TOL
    assert abs(expected_score(1500, 1600) + expected_score(1600, 1500) - 1) < 1e-12


def test_elo_update_is_zero_sum():
    a, b = elo_update(1500, 1500, 1.0, k=24)
    assert abs(a - 1512) < TOL and abs(b - 1488) < TOL
    a, b = elo_update(1600, 1500, 0.0, k=32)
    assert abs((a + b) - 3100) < 1e-9
    assert abs(a - (1600 - 32 * 0.6401)) < 1e-2


def test_class_win_rate_lecture_table():
    assert abs(class_win_rate(60, 0.0) - 0.5855) < TOL
    assert abs(class_win_rate(60, 0.5) - 0.5431) < TOL
    assert abs(class_win_rate(60, 1.0) - 0.5) < TOL


def test_top_share_lecture_table():
    assert abs(top_share(0, 200, 0.001) - 0.001) < 1e-9
    assert abs(top_share(60, 200, 0.001) - 0.002634) < 1e-5
    assert abs(top_share(60, 200, 0.10) - 0.16316) < 1e-4


def test_simulated_ladder_hides_the_advantage():
    # A mid-season patch gives the class +60; each main's rating is per class (f = 1).
    res = simulate_ladder(n_players=2000, rounds=200, delta=60, f=1.0, seed=7)
    early = window_win_rate(res, 0, 10)
    late = window_win_rate(res, 150, 200)
    assert early > 0.55, early           # before ratings absorb the advantage
    assert abs(late - 0.5) < 0.02, late  # after they do
    assert representation(res, 0.10) > 1.25


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:
                failed += 1
                print(f"FAIL {name}: {type(exc).__name__} {exc}")
    raise SystemExit(1 if failed else 0)
