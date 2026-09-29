"""Tests for synth.py. They fail on the starter and pass on a correct solution.

    .venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab03-starter
"""
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth  # noqa: E402
from synth import PRESETS, Sfx  # noqa: E402


class Frequency(unittest.TestCase):
    def test_lecture_end_frequencies(self):
        expected = {"coin": 1334.8, "jump": 401.4, "laser": 596.7, "hurt": 262.8}
        for name, f_end in expected.items():
            sfx = PRESETS[name]
            self.assertAlmostEqual(synth.freq_at(sfx.length, sfx), f_end, places=1, msg=name)

    def test_jump_only_after_t_jump(self):
        coin = PRESETS["coin"]
        self.assertAlmostEqual(synth.freq_at(0.059, coin), 1000.0, places=6)
        self.assertAlmostEqual(synth.freq_at(0.06, coin), 1000 * 2 ** (5 / 12), places=6)

    def test_one_octave(self):
        self.assertAlmostEqual(synth.freq_at(0.2, Sfx(f0=1600, slide=-5)), 800.0, places=6)


class Envelope(unittest.TestCase):
    def test_shape(self):
        env = synth.envelope
        self.assertAlmostEqual(env(0.0, 0.01, 0.1), 0.0)
        self.assertAlmostEqual(env(0.005, 0.01, 0.1), 0.5)
        self.assertAlmostEqual(env(0.01, 0.01, 0.1), 1.0)
        self.assertAlmostEqual(env(0.06, 0.01, 0.1), 0.5)
        self.assertEqual(env(0.11, 0.01, 0.1), 0.0)
        self.assertEqual(env(-0.001, 0.01, 0.1), 0.0)

    def test_zero_attack_starts_at_full(self):
        self.assertAlmostEqual(synth.envelope(0.0, 0.0, 0.1), 1.0)


class Waves(unittest.TestCase):
    def test_values(self):
        rng = random.Random(0)
        w = synth.wave_value
        self.assertAlmostEqual(w("sine", 0.25, rng), 1.0)
        self.assertEqual(w("square", 0.49, rng), 1)
        self.assertEqual(w("square", 0.5, rng), -1)
        self.assertAlmostEqual(w("sawtooth", 0.75, rng), 0.5)
        self.assertAlmostEqual(w("triangle", 0.5, rng), 1.0)
        self.assertAlmostEqual(w("triangle", 0.0, rng), -1.0)
        self.assertTrue(-1 <= w("noise", 0.3, rng) <= 1)

    def test_unknown_wave(self):
        with self.assertRaises(ValueError):
            synth.wave_value("organ", 0.1, random.Random(0))


class Render(unittest.TestCase):
    def test_lengths_match_lecture(self):
        expected = {"coin": 12240, "jump": 10080, "laser": 12096, "hurt": 9696}
        for name, n in expected.items():
            self.assertEqual(len(synth.render(PRESETS[name])), n, msg=name)

    def test_peak_respects_gain(self):
        samples = synth.render(PRESETS["hurt"])
        self.assertLessEqual(max(abs(s) for s in samples), 0.5 + 1e-9)
        self.assertGreater(max(abs(s) for s in samples), 0.45)

    def test_phase_accumulates_frequency(self):
        # A 1,200 Hz square at 48 kHz has a 40-sample period: 20 high, 20 low.
        sfx = Sfx("square", 1200, 0, 0, 0, 0.0, 0.01, gain=1.0)
        s = synth.render(sfx)
        signs = [1 if v > 0 else -1 for v in s[:80] if v != 0]
        changes = sum(1 for a, b in zip(signs, signs[1:]) if a != b)
        self.assertEqual(changes, 3)

    def test_sliding_tone_has_no_phase_jumps(self):
        # With a phase accumulator a sine never jumps by more than 2*pi*f/rate per sample.
        sfx = Sfx("sine", 2000, -4.0, 0, 0, 0.0, 0.25, gain=1.0)
        s = synth.render(sfx)
        env = [synth.envelope(i / synth.RATE, 0.0, 0.25) for i in range(len(s))]
        raw = [v / e for v, e in zip(s, env) if e > 0.05]
        limit = 2 * math.pi * 2000 / synth.RATE + 1e-6
        self.assertLess(max(abs(b - a) for a, b in zip(raw, raw[1:])), limit)

    def test_noise_is_repeatable(self):
        sfx = Sfx("noise", 100, 0, 0, 0, 0.001, 0.05, seed=7)
        self.assertEqual(synth.render(sfx), synth.render(sfx))


if __name__ == "__main__":
    unittest.main()
