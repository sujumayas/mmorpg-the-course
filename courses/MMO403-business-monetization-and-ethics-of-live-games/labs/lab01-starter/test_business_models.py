"""Tests for Lab 01. Values come from the week 1 lecture, section 2.
Run with `python3 test_business_models.py` or `pytest test_business_models.py`."""
from business_models import (Model, contribution, crossover_month, load_models,
                             months_active, retention_value)

M = load_models()
TOL = 1.0  # dollars


def test_months_active():
    assert months_active(0.8, 0) == 0
    assert abs(months_active(0.8, 1) - 1.0) < 1e-12
    assert abs(months_active(0.8, 3) - 2.44) < 1e-12
    assert abs(months_active(0.8, 36) - 4.99837) < 1e-4
    assert abs(months_active(1.0, 5) - 5.0) < 1e-12


def test_lecture_table_r080():
    # Contribution in $ millions at T = 1, 3, 12, 36 (lecture table, r = 0.80).
    expected = {
        "box": (11.90, 11.76, 11.53, 11.50),
        "subscription": (5.45, 7.54, 10.75, 11.25),
        "free-to-play": (1.50, 3.66, 6.98, 7.50),
        "hybrid": (8.25, 9.33, 10.99, 11.25),
    }
    for name, row in expected.items():
        for T, v in zip((1, 3, 12, 36), row):
            assert abs(contribution(M[name], 0.80, T) / 1e6 - v) < 0.006, (name, T)


def test_exact_values():
    assert abs(contribution(M["box"], 0.80, 1) - 11_900_000) < TOL
    assert abs(contribution(M["subscription"], 0.80, 1) - 5_450_000) < TOL
    assert abs(contribution(M["free-to-play"], 0.80, 3) - 3_660_000) < TOL


def test_retention_flips_the_ranking():
    at = lambda r: {n: contribution(m, r, 36) for n, m in M.items()}
    low, high = at(0.70), at(0.90)
    assert max(low, key=low.get) == "box"
    assert max(high, key=high.get) == "subscription"


def test_crossover():
    # Subscription never catches the box at r = 0.80 within 36 months...
    assert crossover_month(M["box"], M["subscription"], 0.80, horizon=36) is None
    # ...but does at r = 0.90.
    t = crossover_month(M["box"], M["subscription"], 0.90)
    assert t == 7
    # A model that already leads returns 1.
    assert crossover_month(M["free-to-play"], M["box"], 0.80) == 1


def test_retention_value_signs():
    assert retention_value(M["box"], 0.80) < 0
    assert abs(retention_value(M["subscription"], 0.80) - 380_100) < 500
    assert abs(retention_value(M["free-to-play"], 0.80) - 393_200) < 500


def test_cost_matters():
    free = Model("free", 1.0, 0.0, 0.40)
    assert contribution(free, 0.8, 12) < 0  # revenue per month below the cost to serve


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
