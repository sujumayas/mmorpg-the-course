"""Tests for AU101 Lab 05. Run: python test_lab05.py
Each test prints PASS or FAIL. NotImplementedError counts as FAIL."""
import os
import tempfile
import wave
from fractions import Fraction as F

import timing as t


def test_reset_times():
    r = t.reset_times(800, 60, 5)
    assert r[0] == 0
    assert all(isinstance(x, F) for x in r)
    assert r[1] == F(5, 60)                        # 4.5 frames rounds up to 5
    assert r[4] == F(20, 60)
    assert t.reset_times(600, 144, 2)[1] == F(15, 144)
    assert t.reset_times(600, 60, 3) == [0, F(1, 10), F(2, 10)]   # exact fit


def test_carry_times():
    c = t.carry_times(800, 60, 5)
    assert c == [0, F(5, 60), F(9, 60), F(14, 60), F(18, 60)]
    # the float trap from the lecture: shot 3 of 600 rpm at 30 fps is exactly frame 9
    assert t.carry_times(600, 30, 4)[3] == F(9, 30)
    assert t.carry_times(800, 144, 6)[5] == F(54, 144)


def test_audio_clock_times():
    a = t.audio_clock_times(800, 4, F(1, 20))
    assert a == [F(1, 20), F(1, 20) + F(3, 40), F(1, 20) + F(6, 40), F(1, 20) + F(9, 40)]


def test_snap_to_chunks():
    c = F(512, 48000)
    snapped = t.snap_to_chunks(t.carry_times(800, 60, 4), 512)
    assert snapped[0] == 0
    assert snapped[1] == 8 * c                     # 83.3 ms -> 85.33 ms
    assert all(s % c == 0 for s in snapped)
    assert t.snap_to_chunks([c * 3], 512) == [c * 3]   # on a boundary: unchanged


def test_measuring():
    assert t.gaps_ms(t.carry_times(800, 60, 5)) == [83.3, 66.7, 83.3, 66.7]
    assert t.gaps_ms(t.audio_clock_times(800, 3, F(0))) == [75.0, 75.0]
    assert abs(t.average_rpm(t.reset_times(800, 60, 10)) - 720.0) < 1e-9
    assert abs(t.average_rpm(t.carry_times(800, 60, 16)) - 794.1176470588) < 1e-6
    assert abs(t.average_rpm(t.reset_times(600, 144, 10)) - 576.0) < 1e-9
    intended = [k * F(3, 40) for k in range(5)]
    assert abs(t.worst_error_ms(intended, t.carry_times(800, 60, 5)) - 8.3333333) < 1e-6
    assert abs(t.worst_error_ms(intended, t.reset_times(800, 60, 5)) - 33.3333333) < 1e-6


def test_distance_steps():
    steps = t.distance_steps([3] * 120, 60, F(3, 4))  # 3 m/s, 0.75 m stride, 2 s
    # after frame i the character has walked (i + 1) / 20 m, so the first step is frame 14
    assert steps == [14, 29, 44, 59, 74, 89, 104, 119]
    fast = t.distance_steps([6] * 120, 60, F(3, 4))
    assert len(fast) == 16                          # double speed, double rate
    stop = t.distance_steps([3] * 30 + [0] * 90, 60, F(3, 4))
    assert len(stop) == 2                           # no steps while standing still


def test_render():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "c.wav")
        t.render_clicks(t.audio_clock_times(800, 3, F(0)), path)
        with wave.open(path) as w:
            assert w.getframerate() == 48000
            assert w.getnframes() == 7200 + int(0.025 * 48000)   # last click at 150 ms


TESTS = [test_reset_times, test_carry_times, test_audio_clock_times, test_snap_to_chunks,
         test_measuring, test_distance_steps, test_render]

if __name__ == "__main__":
    passed = 0
    for fn in TESTS:
        try:
            fn()
            print("PASS", fn.__name__)
            passed += 1
        except Exception as e:  # noqa: BLE001 - report every failure kind
            print("FAIL", fn.__name__, "-", type(e).__name__, e)
    print(f"{passed}/{len(TESTS)} tests passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
