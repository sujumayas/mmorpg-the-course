"""Tests for Lab 03. Values come from the week 3 lecture and packs.csv.
Run with ../../../../.venv/bin/python test_pulls.py (or pytest)."""
import math

from pulls import (BASE, best_pull, clear_minutes, kill_time, load_packs, pull_works, route,
                   survive_time)

P = {k: v for k, v in BASE.items() if k != "walk"}


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_times():
    assert close(kill_time(8, 1000, 50, 20), 20.0)
    assert close(kill_time(8, 1000, 50, 5), 32.0)
    assert close(kill_time(50, 1000, 50, None), 20.0)
    assert close(survive_time(8, 30, 150, 3200), 3200 / 90)
    assert survive_time(5, 30, 150, 3200) == math.inf
    assert pull_works(10, **P)
    assert not pull_works(11, **P)
    assert not pull_works(9, **{**P, "cap": 5})


def test_clear_table():
    assert close(clear_minutes(120, 1, **BASE), 60.0)
    assert close(clear_minutes(120, 8, **BASE), 7.5)
    assert close(clear_minutes(120, 8, **{**BASE, "cap": 5}), 10.5)
    assert clear_minutes(120, 12, **BASE) is None


def test_best_pull():
    assert best_pull(120) == (10, 6.0)
    n, m = best_pull(120, cap=5)
    assert n == 8 and close(m, 10.5)
    n, m = best_pull(120, scale=1.08 ** 5)
    assert n == 5 and close(round(m, 1), 15.8)
    n, m = best_pull(120, scale=1.08 ** 10)
    assert n == 3 and close(round(m, 1), 35.5)
    assert best_pull(120, Q=210) == (12, 5.0)
    assert best_pull(120, B=10, Q=0) is None


def test_route():
    packs = load_packs()
    secs, names = route(packs, 30, **P)
    assert names == ["crypt_stair", "entry_guards", "hall_left", "library_a", "library_b"]
    assert close(secs, 185.0)
    # Harder-hitting trash makes the 8-enemy crypt pull unsafe, so the route changes.
    secs, names = route(packs, 30, **{**P, "d": 45})
    assert names == ["hall_left", "hall_right", "library_a", "library_b", "side_vault"]
    assert close(secs, 205.0)
    assert route(packs, 500, **P) is None


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
