"""Tests for AU101 Lab 04. Run: python test_lab04.py
Each test prints PASS or FAIL. NotImplementedError counts as FAIL."""
import os
import random
import tempfile
import wave
from collections import Counter

import variation as v

TOL = 1e-6


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def test_semitones_and_decibels():
    assert close(v.semitones_to_ratio(12), 2.0)
    assert close(v.semitones_to_ratio(-12), 0.5)
    assert close(v.semitones_to_ratio(0), 1.0)
    assert close(v.semitones_to_ratio(1), 1.0594631, 1e-6)
    assert close(v.db_to_gain(0), 1.0)
    assert close(v.db_to_gain(-6), 0.5011872, 1e-6)
    assert close(v.db_to_gain(20), 10.0)


def test_repeat_chance():
    assert close(v.repeat_chance([1]), 1.0)
    assert close(v.repeat_chance([1] * 32), 1 / 32)
    heretic = Counter(a - b for a in range(8) for b in range(8))
    assert close(v.repeat_chance(list(heretic.values())), 344 / 4096)
    assert close(v.repeat_chance([3, 1, 1, 1, 1]), 13 / 49)
    assert close(v.repeat_chance([2, 2]), 0.5)          # scale does not matter
    assert close(v.repeat_chance([6, 1, 1, 1, 1, 1]), 41 / 121)


def test_burst_repeat_probability():
    assert close(v.burst_repeat_probability(1.0, 10), 1.0)
    assert close(v.burst_repeat_probability(0.0, 10), 0.0)
    assert close(v.burst_repeat_probability(1 / 32, 10), 0.2485407, 1e-6)
    assert close(v.burst_repeat_probability(0.5, 1), 0.0)   # no pairs
    assert close(v.burst_repeat_probability(0.5, 0), 0.0)
    assert close(v.burst_repeat_probability(1 / 9, 6), 0.4450710, 1e-6)


def test_no_repeat_picker():
    rng = random.Random(1)
    p = v.NoRepeatPicker(4, no_repeat=True)
    picks = [p.pick(rng) for _ in range(2000)]
    assert set(picks) == {0, 1, 2, 3}
    assert all(a != b for a, b in zip(picks, picks[1:]))
    one = v.NoRepeatPicker(1, no_repeat=True)
    assert [one.pick(rng) for _ in range(5)] == [0] * 5
    free = v.NoRepeatPicker(2, no_repeat=False)
    picks = [free.pick(rng) for _ in range(400)]
    assert any(a == b for a, b in zip(picks, picks[1:]))  # repeats allowed


def test_plan_burst_ranges():
    rng = random.Random(7)
    plan = v.plan_burst([4, 3, 2], 50, 1.5, 3.0, rng, no_repeat=True)
    assert len(plan) == 50
    for shot in plan:
        assert len(shot.variants) == 3
        assert 0 <= shot.variants[0] < 4 and 0 <= shot.variants[1] < 3
        assert 0 <= shot.variants[2] < 2
        assert -1.5 <= shot.semitones <= 1.5
        assert -3.0 <= shot.gain_db <= 0.0
    for layer in range(3):
        seq = [s.variants[layer] for s in plan]
        assert all(a != b for a, b in zip(seq, seq[1:]))


def test_plan_burst_reproducible_and_machine_gun():
    a = v.plan_burst([4, 4, 4], 10, 1.0, 2.0, random.Random(99), no_repeat=True)
    b = v.plan_burst([4, 4, 4], 10, 1.0, 2.0, random.Random(99), no_repeat=True)
    assert a == b
    same = v.plan_burst([1], 10, 0.0, 0.0, random.Random(5))
    assert all(s == v.Shot((0,), 0.0, 0.0) for s in same)
    # the draw order in the docstring: variants, then pitch, then gain
    rng = random.Random(3)
    first = v.plan_burst([4], 1, 2.0, 2.0, rng)[0]
    ref = random.Random(3)
    variant = ref.randrange(4)
    pitch = ref.uniform(-2.0, 2.0)
    gain = ref.uniform(-2.0, 0.0)
    assert first == v.Shot((variant,), pitch, gain)


def test_render_length():
    layers = [[[0.5] * 1000], [[0.25] * 3000]]
    plan = [v.Shot((0, 0), 0.0, 0.0), v.Shot((0, 0), 12.0, -6.0)]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.wav")
        n = v.render(plan, layers, path, interval=0.1)
        with wave.open(path) as w:
            assert w.getnframes() == n
    # shot 2 starts at 4410; at double speed its 3000-sample layer lasts 1500 samples
    assert n == 4410 + 1500


TESTS = [test_semitones_and_decibels, test_repeat_chance, test_burst_repeat_probability,
         test_no_repeat_picker, test_plan_burst_ranges,
         test_plan_burst_reproducible_and_machine_gun, test_render_length]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print("PASS", t.__name__)
            passed += 1
        except Exception as e:  # noqa: BLE001 - report every failure kind
            print("FAIL", t.__name__, "-", type(e).__name__, e)
    print(f"{passed}/{len(TESTS)} tests passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
