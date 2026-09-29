"""Tests for Lab 09. Values come from the week 9 lecture's recurrence table.
Run with ../../../../.venv/bin/python test_rival.py (or pytest)."""
from rival import campaign, expected_wait, p_meet, p_rematch_within, simulate, weight_for

TOL = 1e-4


def test_table():
    # (R, w): (P, within 5, within 10, wait)
    table = {
        (20, 1): (0.05, 0.2262, 0.4013, 20.0),
        (20, 5): (0.2083, 0.6890, 0.9033, 4.8),
        (20, 10): (0.3448, 0.8793, 0.9854, 2.9),
        (3, 1): (0.3333, 0.8683, 0.9827, 3.0),
        (200, 1): (0.005, 0.0248, 0.0489, 200.0),
        (200, 50): (0.2008, 0.6740, 0.8937, 4.98),
    }
    for (R, w), (p, w5, w10, wait) in table.items():
        assert abs(p_meet(R, w) - p) < TOL, (R, w)
        assert abs(p_rematch_within(5, R, w) - w5) < TOL, (R, w)
        assert abs(p_rematch_within(10, R, w) - w10) < TOL, (R, w)
        assert abs(expected_wait(R, w) - wait) < 0.01, (R, w)
    assert p_rematch_within(0, 20, 5) == 0.0


def test_weight_for():
    assert weight_for(20, 5, 0.5) == 3
    assert weight_for(200, 5, 0.5) == 30
    assert weight_for(3, 5, 0.5) == 1


def test_bad_arguments():
    for bad in [(0, 1), (20, 0), (20, -2)]:
        try:
            p_meet(*bad)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")


def test_simulate_matches_formula():
    for R, w in [(20, 1), (20, 10), (200, 50)]:
        got = simulate(R, w, 5, 20_000, seed=1)
        assert abs(got - p_rematch_within(5, R, w)) < 0.015, (R, w, got)


def test_campaign_rules():
    log, ranks = campaign(20, 10, 60, 0.7, seed=3)
    assert len(log) == 60 and len(ranks) == 20
    losses = sum(not e["player_won"] for e in log)
    assert sum(ranks) == 20 + losses          # each loss promotes one character
    beaten_by = set()
    for e in log:
        assert e["rematch"] == (e["who"] in beaten_by)
        if not e["player_won"]:
            beaten_by.add(e["who"])
    # same seed, same story
    assert campaign(20, 10, 60, 0.7, seed=3) == (log, ranks)


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
