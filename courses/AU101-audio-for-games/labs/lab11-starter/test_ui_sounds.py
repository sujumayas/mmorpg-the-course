"""Tests for AU101 Lab 11. Values come from the week 11 lecture.
Run with `python3 test_ui_sounds.py` (or pytest)."""
import os
import tempfile
import wave

from ui_sounds import (MAJOR, SR, concat, estimate_freq, ladder_semitones, peak_db,
                       render, semitone_ratio, streak_steps, write_wav)


def test_semitone_ratio():
    assert abs(semitone_ratio(12) - 2.0) < 1e-9
    assert abs(semitone_ratio(7) - 1.4983) < 1e-4
    assert abs(semitone_ratio(-12) - 0.5) < 1e-9


def test_ladder_table():
    freqs = [round(523.25 * semitone_ratio(ladder_semitones(n)), 2) for n in range(1, 9)]
    assert freqs == [523.25, 587.33, 659.25, 698.45, 783.99, 880.0, 987.76, 1046.5]


def test_ladder_modes():
    assert [ladder_semitones(n, MAJOR, "cap") for n in (8, 9, 12)] == [12, 12, 12]
    assert [ladder_semitones(n, MAJOR, "wrap") for n in (8, 9, 10)] == [12, 0, 2]
    assert [ladder_semitones(n, MAJOR, "same") for n in (1, 5, 9)] == [0, 0, 0]


def test_streak_reset():
    assert streak_steps([0, 0.3, 0.6, 1.5, 1.7], 0.5) == [1, 2, 3, 1, 2]
    assert streak_steps([0, 0.5, 1.0], 0.5) == [1, 2, 3]      # equal gap keeps it
    assert streak_steps([], 0.5) == []


def test_render_length_and_peak():
    s = render(440, 440, 0.1, peak=-12)
    assert len(s) == 4800
    assert abs(peak_db(s) - (-12)) < 0.01
    assert abs(s[0]) < 1e-3                                      # starts silent


def test_render_pitch():
    s = render(440, 440, 0.25, peak=-6)
    assert abs(estimate_freq(s) - 440) / 440 < 0.01


def test_sweep_direction():
    up = render(600, 1200, 0.2)
    half = len(up) // 2
    assert estimate_freq(up[:half]) < estimate_freq(up[half:])
    down = render(1200, 600, 0.2)
    assert estimate_freq(down[:half]) > estimate_freq(down[half:])


def test_concat_and_wav():
    a = render(500, 500, 0.05)
    joined = concat(a, a, gap=0.02)
    assert len(joined) == 2 * len(a) + 960
    path = os.path.join(tempfile.mkdtemp(), "t.wav")
    write_wav(path, joined)
    with wave.open(path) as w:
        assert w.getnframes() == len(joined) and w.getframerate() == SR


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
