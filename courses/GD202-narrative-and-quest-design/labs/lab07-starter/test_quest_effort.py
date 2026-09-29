"""Tests for Lab 07. Values come from the week 7 lecture's tables.
Run with ../../../../.venv/bin/python test_quest_effort.py (or pytest)."""
from quest_effort import (expected_kills, load_quests, percentile_kills,
                          prob_done_by, same_mean_designs, sd_kills)

TOL = 1e-9


def test_mean_and_sd():
    assert abs(expected_kills(10, 0.5) - 20) < TOL
    assert abs(expected_kills(1, 0.05) - 20) < TOL
    assert abs(sd_kills(10, 0.5) - 4.47213595) < 1e-6
    assert abs(sd_kills(1, 0.05) - 19.49358869) < 1e-6
    assert sd_kills(20, 1.0) == 0


def test_prob_done_by():
    assert prob_done_by(9, 10, 0.5) == 0.0
    assert abs(prob_done_by(10, 10, 0.5) - 0.5 ** 10) < TOL
    assert abs(prob_done_by(1, 1, 0.05) - 0.05) < TOL
    # a lone 5% drop: chance of still waiting after 40 kills is 0.95^40
    assert abs((1 - prob_done_by(40, 1, 0.05)) - 0.95 ** 40) < TOL
    assert abs(prob_done_by(20, 20, 1.0) - 1.0) < TOL


def test_percentiles_table():
    # (n, p): (median, P90, P99) from the lecture's same-mean table
    table = {
        (1, 0.05): (14, 45, 90),
        (2, 0.10): (17, 38, 64),
        (5, 0.25): (19, 30, 43),
        (10, 0.50): (19, 26, 33),
        (20, 1.00): (20, 20, 20),
    }
    for (n, p), want in table.items():
        got = tuple(percentile_kills(n, p, q) for q in (0.5, 0.9, 0.99))
        assert got == want, f"{(n, p)}: got {got}, want {want}"


def test_same_mean_designs():
    got = same_mean_designs(20, [1, 2, 5, 10, 20, 40])
    assert [n for n, _ in got] == [1, 2, 5, 10, 20]
    assert all(abs(p - n / 20) < TOL for n, p in got)


def test_bad_arguments():
    for bad in [(10, 0), (10, 1.5), (0, 0.5)]:
        try:
            expected_kills(*bad)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")


def test_quests_csv():
    qs = load_quests()
    assert len(qs) == 5
    tusks = next(q for q in qs if q["name"].startswith("Boar"))
    assert abs(expected_kills(tusks["n"], tusks["p"]) - 32) < TOL


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
