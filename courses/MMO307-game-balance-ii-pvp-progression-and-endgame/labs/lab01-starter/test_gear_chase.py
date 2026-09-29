"""Tests for MMO307 Lab 01. Values come from the week 1 lecture.
Run with `python test_gear_chase.py` (or pytest if you have it)."""
import statistics

from gear_chase import (expected_runs, finish_cdf, percentile_run,
                        simulate_hybrid, token_runs, upgrade_chance)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_upgrade_chance():
    assert close(upgrade_chance(0, 10), 1.0)
    assert close(upgrade_chance(9, 10), 0.1)
    assert close(upgrade_chance(9, 10, m=3), 0.271)
    assert close(upgrade_chance(8, 10, m=3), 0.488)


def test_expected_runs():
    assert close(expected_runs(10), 29.2896825, 1e-5)
    assert close(expected_runs(10, 3), 14.7848454, 1e-5)
    assert close(expected_runs(10, 9), 10.84, 0.01)
    assert close(expected_runs(12), 37.24, 0.01)


def test_cdf_shape():
    cdf = finish_cdf(10, n_max=100)
    assert len(cdf) == 100
    assert all(cdf[i] <= cdf[i + 1] + 1e-15 for i in range(99))
    assert cdf[8] == 0.0          # cannot finish 10 slots in 9 runs
    assert cdf[9] > 0.0           # can finish in exactly 10
    assert close(cdf[29], 0.6291, 1e-4)


def test_percentiles():
    assert [percentile_run(10, x) for x in (0.5, 0.9, 0.99)] == [27, 44, 66]


def test_tokens():
    assert token_runs(10, 3, 1) == 30
    assert token_runs(12, 5, 2) == 30
    assert token_runs(10, 4, 1) == 40
    assert token_runs(5, 3, 2) == 8   # 7.5 runs rounds up


def test_hybrid_bounds():
    runs = simulate_hybrid(10, 3, 1, players=4_000)
    assert len(runs) == 4_000
    assert max(runs) <= 30            # tokens alone would finish by run 30
    assert statistics.mean(runs) < 29.29   # faster than drops alone
    assert 11 <= statistics.median(runs) <= 13


def test_hybrid_rare_drops():
    runs = sorted(simulate_hybrid(10, 8, 1, d=0.25, players=10_000))
    assert 38 <= runs[len(runs) // 2] <= 42
    assert 46 <= runs[int(0.9 * len(runs))] <= 50
    assert max(runs) <= 80


def test_hybrid_reproducible():
    assert simulate_hybrid(10, 5, 1, players=200, seed=3) == simulate_hybrid(10, 5, 1, players=200, seed=3)


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
