"""Tests for Lab 08. Values come from the week 8 lecture.
Run with `python3 test_utility.py` or `pytest test_utility.py`."""
from utility import (LECTURE_HP, attack_desire, choose, crossover, logistic, piecewise, power,
                     replay, score)

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) < tol


def test_power():
    assert close(power(0.5, 1), 0.5)
    assert close(power(0.5, 2), 0.25)
    assert close(power(0.8, 3), 0.512)
    assert close(power(1.7, 2), 1.0)          # inputs are clamped to [0, 1]


def test_logistic():
    assert close(logistic(0.5), 0.5)
    assert close(logistic(0.7, mid=0.5, steep=10), 1 / (1 + 2.718281828459045 ** -2), 1e-12)
    assert logistic(0.0) < 0.01 and logistic(1.0) > 0.99


def test_piecewise_hunger_curve():
    hunger = [(0.0, 0.0), (0.4, 0.1), (0.7, 0.3), (1.0, 1.0)]
    assert close(piecewise(0.2, hunger), 0.05)
    assert close(piecewise(0.55, hunger), 0.2)
    assert close(piecewise(0.85, hunger), 0.65)
    assert close(piecewise(1.5, hunger), 1.0)


def test_product_and_geomean():
    two = [lambda: 0.8, lambda: 0.8]
    five = [lambda: 0.9] * 5
    assert close(score(two), 0.64)
    assert close(score(five), 0.59049)
    assert close(score(two, "geomean"), 0.8)
    assert close(score(five, "geomean"), 0.9)


def test_zero_disqualifies_and_stops():
    calls = []
    def expensive():
        calls.append(1)
        return 0.9
    assert score([lambda: 0.0, expensive]) == 0.0
    assert calls == []                         # the expensive check never ran


def test_choose_with_bonus():
    assert choose({"attack": 0.6, "drink": 0.64}, "attack", 0.0) == "drink"
    assert choose({"attack": 0.6, "drink": 0.64}, "attack", 0.1) == "attack"   # 0.66 > 0.64
    assert choose({"attack": 0.6, "drink": 0.6}, "drink", 0.0) == "drink"      # tie keeps current


def test_crossovers():
    assert close(crossover(1), 0.4)
    assert close(crossover(2), 0.2254033307585166)
    assert close(crossover(3), 0.156567, 1e-6)
    assert close(crossover(2, attack_desire(0.5)), 0.133975, 1e-6)
    assert close(crossover(2, attack_desire(0.1)), 0.067262, 1e-6)


def test_lecture_replay_no_bonus():
    choices, switches, done = replay(LECTURE_HP, bonus=0.0)
    assert "".join(c[0] for c in choices) == "aadaddadadaa"
    assert switches == 8 and done is None


def test_lecture_replay_bonus():
    choices, switches, done = replay(LECTURE_HP, bonus=0.1)
    assert "".join(c[0] for c in choices) == "aaaaadddddda"
    assert switches == 2 and done == 8


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
    print(f"\n{failed} test(s) not passing" if failed else "\nall tests pass")
    raise SystemExit(1 if failed else 0)
