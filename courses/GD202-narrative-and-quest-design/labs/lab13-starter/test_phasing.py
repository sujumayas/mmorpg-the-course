"""Lab 13 tests. Run with `python test_phasing.py` or `pytest test_phasing.py`.
Every test fails on the starter and passes on a correct phasing.py."""
import json
import os

from phasing import (effective_phases, expected_visible, per_phase_visible,
                     phase_shares, visible_share)

HERE = os.path.dirname(os.path.abspath(__file__))


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def test_visible_share_lecture_cases():
    assert close(visible_share([1.0]), 1.0)
    assert close(visible_share([0.5, 0.5]), 0.5)
    assert close(visible_share([0.30, 0.25, 0.20, 0.15, 0.10]), 0.225)
    assert close(visible_share({"base": 0.9, "after": 0.1}), 0.82)


def test_expected_visible_and_effective():
    assert close(expected_visible([0.9, 0.1], 41), 32.8)
    assert close(effective_phases([0.30, 0.25, 0.20, 0.15, 0.10]), 1 / 0.225)


def test_linear_chain():
    chain = [{"sets_phase": None}, {"sets_phase": "x"}]
    shares = phase_shares(chain, [0.5, 0.3, 0.2])
    assert set(shares) == {"base", "x"}
    assert close(shares["base"], 0.8) and close(shares["x"], 0.2)


def test_choice_multiplies_later_phases():
    chain = [{"sets_phase": {"a": 0.5, "b": 0.5}}, {"sets_phase": "z"}]
    shares = phase_shares(chain, [0.4, 0.4, 0.2])
    assert close(shares["base"], 0.4)
    assert close(shares["a"], 0.2) and close(shares["b"], 0.2)
    assert close(shares["a+z"], 0.1) and close(shares["b+z"], 0.1)


def test_saltmarsh():
    zone = load("saltmarsh.json")
    shares = phase_shares(zone["chain"], zone["funnel"])
    expected = {
        "base": 0.40, "flooded": 0.30,
        "flooded+dam_blown": 0.06, "flooded+dam_repaired": 0.04,
        "flooded+dam_blown+knight_dead": 0.12,
        "flooded+dam_repaired+knight_dead": 0.08,
    }
    assert set(shares) == set(expected)
    for k, v in expected.items():
        assert close(shares[k], v), k
    assert close(visible_share(shares), 0.276)
    assert close(expected_visible(shares, 41), 11.04)
    seen = per_phase_visible(shares, 41)
    assert close(seen["flooded+dam_blown+knight_dead"], 4.8)


def test_zero_shares_dropped():
    chain = [{"sets_phase": "x"}]
    shares = phase_shares(chain, [1.0, 0.0])
    assert shares == {"base": 1.0}


def test_bad_input_raises():
    chain = [{"sets_phase": None}]
    for funnel in ([0.5, 0.4], [1.0], [1.2, -0.2]):
        try:
            phase_shares(chain, funnel)
        except ValueError:
            continue
        raise AssertionError(f"no ValueError for funnel {funnel}")
    try:
        phase_shares([{"sets_phase": {"a": 0.7, "b": 0.2}}], [0.5, 0.5])
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError for choice fractions summing to 0.9")


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:  # NotImplementedError counts as a failure
                failed += 1
                print(f"FAIL {name}: {type(e).__name__} {e}")
    sys.exit(1 if failed else 0)
