"""Lab 11 tests. Run with `python3 test_season_sim.py` (or pytest).
Every test fails on the starter and passes once the TODOs are done."""
import random
import sys
from season_sim import (elo_update, soft_reset, play_round, mean_abs_error,
                        lopsided_share, run_season)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_elo_update():
    a, b = elo_update(1500, 1500, 1.0, 32)
    assert close(a, 1516) and close(b, 1484)
    a, b = elo_update(1700, 1500, 0.0, 20)          # upset: favourite loses
    assert close(a + b, 3200)                       # zero-sum
    assert close(a, 1700 - 20 / (1 + 10 ** (-0.5)))


def test_soft_reset():
    assert soft_reset([1100, 1500, 2100], 0.5, 1500) == [1300, 1500, 1800]
    assert soft_reset([1900], 0.0, 1500) == [1500]
    original = [1600.0]
    soft_reset(original, 0.5, 1500)
    assert original == [1600.0]                     # returns a new list


def test_metrics():
    assert close(mean_abs_error([1, 2], [2, 4]), 1.5)
    true = [1000, 1150, 1500, 1800]
    assert close(lopsided_share([(0, 1), (2, 3)], true), 0.5)
    assert close(lopsided_share([(0, 1), (2, 3)], true, gap=100), 1.0)


def test_play_round():
    rng = random.Random(7)
    true = [rng.gauss(1500, 200) for _ in range(100)]
    shown = [1500.0 + i for i in range(100)]
    before = sum(shown)
    pairs = play_round(true, shown, 32, rng)
    seen = [i for p in pairs for i in p]
    assert len(pairs) == 50 and sorted(seen) == list(range(100))
    assert close(sum(shown), before, 1e-6)          # Elo is zero-sum
    assert shown != [1500.0 + i for i in range(100)]


def test_season_shape():
    hard = run_season(alpha=0.0, players=400, warmup=200, rounds=100, seed=2)
    light = run_season(alpha=0.8, players=400, warmup=200, rounds=100, seed=2)
    assert len(hard) == 101 and hard[0][2] is None
    assert hard[0][1] > 2 * light[0][1]             # hard reset starts far worse
    assert hard[100][1] < 0.5 * hard[0][1]          # and recovers
    assert hard[1][2] > light[1][2]                 # more lopsided games early


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:
                failed += 1
                print(f"FAIL {name}: {type(e).__name__} {e}")
    sys.exit(1 if failed else 0)
