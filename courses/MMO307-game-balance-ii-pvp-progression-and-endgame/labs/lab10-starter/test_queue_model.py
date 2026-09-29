"""Lab 10 tests. Run with `python3 test_queue_model.py` (or pytest).
Every test fails on the starter and passes once the TODOs are done."""
import sys
from queue_model import (share_in_window, mean_wait, mean_favourite_score,
                         match_pool, simulate_queue, summarise)


def close(a, b, tol):
    return abs(a - b) <= tol


def test_share_in_window():
    assert close(share_in_window(1500, 50), 0.1974, 1e-4)
    assert close(share_in_window(2100, 100), 0.0060, 1e-4)


def test_mean_wait():
    assert close(mean_wait(1500, 50), 25.3, 0.1)
    assert close(mean_wait(2100, 100), 836.5, 0.5)
    # Doubling the arrival rate halves the wait.
    assert close(mean_wait(1500, 50, lam=24), 25.33 / 2, 0.05)


def test_mean_favourite_score():
    assert close(mean_favourite_score(1500, 50), 0.536, 0.001)
    assert close(mean_favourite_score(2100, 200), 0.678, 0.001)


def test_match_pool_rule():
    m, rest = match_pool([(1500, 0), (1540, 0), (1700, 0)], 0, 50, 5, 400)
    assert m == [(40, 0, 0)] and rest == [(1700, 0)]
    m, rest = match_pool([(1600, 0), (1500, 0)], 0, 50, 5, 400)
    assert m == [] and len(rest) == 2
    m, rest = match_pool([(1600, 0), (1500, 0)], 10, 50, 5, 400)
    assert m == [(100, 10, 10)] and rest == []


def test_simulation_is_sane():
    matches = simulate_queue(seconds=1800, seed=3)
    assert len(matches) > 100
    assert all(g <= 400 for g, _, _ in matches)
    wait, gap, fav = summarise(matches)
    assert wait < 60 and 0.5 < fav < 0.7


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:          # NotImplementedError counts as a fail
                failed += 1
                print(f"FAIL {name}: {type(e).__name__} {e}")
    sys.exit(1 if failed else 0)
