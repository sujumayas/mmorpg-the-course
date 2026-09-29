"""Tests for MMO403 Lab 14. Values come from the week 14 lecture (money in $ millions).
Run with `python3 test_stage_gate.py` (or `pytest test_stage_gate.py`) from this folder."""
from stage_gate import (best_stage1, breakeven_f, ev_all_in, ev_gated, founder_share,
                        kill_rate, load_options, post_money, posterior_hit, pre_money)

TOL = 1e-9
P, V, C1, C2 = 0.25, 60, 2, 18


def close(a, b, tol=TOL):
    return abs(a - b) < tol


def test_all_in_and_perfect_gate():
    assert close(ev_all_in(P, V, C1, C2), -5.0)
    assert close(ev_gated(P, V, C1, C2, 1.0, 0.0), 8.5)
    # A signal that always says go carries no information: a rational funder stops, EV = -C1.
    assert close(ev_gated(P, V, C1, C2, 1.0, 1.0), -2.0)


def test_realistic_gates_table():
    for f, ev, k in [(0.0, 6.4, 0.80), (0.2, 3.7, 0.65), (0.4, 1.0, 0.50), (0.6, -1.7, 0.35)]:
        assert close(ev_gated(P, V, C1, C2, 0.8, f), ev), f
        assert close(kill_rate(P, 0.8, f), k), f


def test_never_continue_at_a_loss():
    # With V below C2 nobody should pay for stage 2: the EV is just -C1.
    assert close(ev_gated(0.5, 10, 2, 18, 0.9, 0.1), -2.0)


def test_posterior():
    assert close(posterior_hit(P, 0.8, 0.2), 0.2 / 0.35)
    assert close(posterior_hit(P, 0.9, 0.1), 0.75)
    assert posterior_hit(0.0, 0.8, 0.0) is None


def test_breakeven():
    assert close(breakeven_f(P, V, C1, C2, 0.8), 6.4 / 13.5)
    assert close(breakeven_f(0.2, 80, 3, 20, 0.75), 0.375)     # check-yourself question 2
    assert breakeven_f(0.05, 20, 5, 18, 0.8) == 0.0              # clamped
    assert breakeven_f(0.5, 200, 1, 5, 1.0) == 1.0               # clamped


def test_best_stage1():
    opts = load_options()
    design, ev = best_stage1(opts, P, V, C2)
    assert design == "soft launch" and close(ev, 4.1)
    opts[2]["c1"] = 6
    design, ev = best_stage1(opts, P, V, C2)
    assert design == "vertical slice" and close(ev, 3.7)


def test_valuation():
    assert close(post_money(46, 0.10), 460)                      # Cloud Imperium, Dec 2018
    assert close(pre_money(46, 0.10), 414)
    assert close(post_money(5, 0.20), 25) and close(post_money(30, 0.30), 100)


def test_dilution():
    assert close(founder_share([]), 1.0)
    assert close(founder_share([0.25, 0.25]), 0.5625)
    assert close(founder_share([0.2, 0.3]), 0.56)
    assert close(founder_share([20 / 26]), 6 / 26)


if __name__ == "__main__":
    import sys
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print("FAIL", t.__name__, "-", type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
