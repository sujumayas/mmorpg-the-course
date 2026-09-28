"""MMO302 lab 11 tests. Run with: python -m unittest test_bots.py
All fail on the starter and pass once the three TODO functions work."""
import random
import unittest

from bots import find_knee, percentile, poisson_schedule


class TestPercentile(unittest.TestCase):
    def test_ma102_rule(self):
        xs = [15, 1, 3, 7, 9, 12, 5, 20, 2, 11]
        self.assertAlmostEqual(percentile(xs, 0.5), 8.0)
        self.assertAlmostEqual(percentile(xs, 0.9), 15.5)
        self.assertAlmostEqual(percentile(xs, 0.0), 1.0)
        self.assertAlmostEqual(percentile(xs, 1.0), 20.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            percentile([], 0.5)


class TestSchedule(unittest.TestCase):
    def test_rate_and_range(self):
        times = poisson_schedule(0.5, 20_000, random.Random(7))
        self.assertEqual(times, sorted(times))
        self.assertTrue(0 < times[0] and times[-1] < 20_000)
        self.assertLess(abs(len(times) - 10_000), 300)       # 0.5/s for 20,000 s

    def test_deterministic(self):
        a = poisson_schedule(2.0, 10, random.Random(3))
        b = poisson_schedule(2.0, 10, random.Random(3))
        self.assertEqual(a, b)


class TestKnee(unittest.TestCase):
    def test_lecture_numbers(self):
        rows = [(200, 11.5), (500, 18.4), (800, 46.1), (900, 92.1), (950, 184.2)]
        self.assertEqual(find_knee(rows, 100), 900)
        self.assertEqual(find_knee(rows, 50), 800)
        self.assertIsNone(find_knee(rows, 10))

    def test_noisy_dip_does_not_count(self):
        rows = [(100, 20), (200, 150), (300, 60)]
        self.assertEqual(find_knee(rows, 100), 100)


if __name__ == "__main__":
    unittest.main()
