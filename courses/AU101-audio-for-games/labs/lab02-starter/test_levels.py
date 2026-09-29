"""Tests for levels.py. They fail on the starter and pass on a correct solution.

    .venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab02-starter
"""
import math
import os
import sys
import tempfile
import unittest
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import levels  # noqa: E402

RATE = 48000


def sine(amp, freq=1000, seconds=0.1):
    return [amp * math.sin(2 * math.pi * freq * i / RATE) for i in range(int(RATE * seconds))]


class PeakAndRms(unittest.TestCase):
    def test_peak_half_scale(self):
        self.assertAlmostEqual(levels.peak_dbfs(sine(0.5)), -6.02, places=2)

    def test_peak_uses_absolute_value(self):
        self.assertAlmostEqual(levels.peak_dbfs([0.0, -0.1, 0.05]), -20.0, places=6)

    def test_peak_of_silence(self):
        self.assertEqual(levels.peak_dbfs([0.0] * 10), levels.SILENCE_DBFS)

    def test_rms_full_scale_sine(self):
        self.assertAlmostEqual(levels.rms_dbfs(sine(1.0)), -3.01, places=2)

    def test_rms_constant(self):
        self.assertAlmostEqual(levels.rms_dbfs([0.1] * 100), -20.0, places=6)

    def test_rms_empty_and_zero(self):
        self.assertEqual(levels.rms_dbfs([]), levels.SILENCE_DBFS)
        self.assertEqual(levels.rms_dbfs([0.0] * 50), levels.SILENCE_DBFS)


class NoiseFloor(unittest.TestCase):
    def test_quietest_window(self):
        # 100 ms at 0.1 (-20 dBFS RMS), then 100 ms at 0.001 (-60 dBFS RMS)
        samples = [0.1] * 4800 + [0.001] * 4800
        self.assertAlmostEqual(levels.noise_floor_dbfs(samples, RATE), -60.0, places=6)

    def test_windows_do_not_overlap_loud_part(self):
        # 50 ms windows: the loud burst sits entirely in the first window
        samples = [0.5] * 2400 + [0.01] * 2400 + [0.01] * 2400
        self.assertAlmostEqual(levels.noise_floor_dbfs(samples, RATE), -40.0, places=6)

    def test_partial_tail_ignored(self):
        samples = [0.01] * 2400 + [0.0] * 100
        self.assertAlmostEqual(levels.noise_floor_dbfs(samples, RATE), -40.0, places=6)

    def test_short_file_is_one_window(self):
        self.assertAlmostEqual(levels.noise_floor_dbfs([0.1] * 100, RATE), -20.0, places=6)


class ReadWav(unittest.TestCase):
    def test_24_bit_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.wav")
            with wave.open(path, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(3)
                w.setframerate(RATE)
                w.writeframes(b"".join(int(v * 2**23).to_bytes(3, "little", signed=True)
                                       for v in (0.5, -0.25, 0.0)))
            samples, rate, bits, ch = levels.read_wav(path)
            self.assertEqual((rate, bits, ch), (RATE, 24, 1))
            self.assertAlmostEqual(levels.peak_dbfs(samples), -6.0206, places=3)


if __name__ == "__main__":
    unittest.main()
