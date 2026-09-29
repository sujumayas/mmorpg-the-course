"""MMO407 lab 02 tests. Run with: python -m unittest test_launch_queue.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from launch_queue import (alive_on_day30, peak, queue_at, simulate,
                          smallest_worlds, wait_at_back)


class TestLectureLaunch(unittest.TestCase):
    def test_ten_worlds(self):
        log = simulate(10, 4000, 100, 160)
        self.assertAlmostEqual(queue_at(log, 1), 2700, delta=0.5)
        self.assertAlmostEqual(queue_at(log, 3), 4500, delta=0.5)
        self.assertEqual(peak(log)[1], 180)
        self.assertEqual(next(t + 1 for t in range(180, 720) if log[t] < 0.5), 630)
        self.assertAlmostEqual(wait_at_back(queue_at(log, 3), 4000, 160), 180)

    def test_fifteen_worlds_and_layers(self):
        self.assertAlmostEqual(queue_at(simulate(15, 4000, 100, 160), 3), 750, delta=0.5)
        self.assertAlmostEqual(queue_at(simulate(10, 6000, 150, 160), 3), 1125, delta=0.5)


class TestSessionModels(unittest.TestCase):
    def test_first_minute_logouts(self):
        self.assertAlmostEqual(queue_at(simulate(10, 4000, 100, 160, model="first"), 3), 4059, delta=1)

    def test_fixed_length(self):
        log = simulate(10, 4000, 100, 160, model="fixed")
        self.assertAlmostEqual(queue_at(log, 3), 6000, delta=0.5)
        q, m = peak(log)
        self.assertAlmostEqual(q, 7200, delta=0.5)
        self.assertEqual(m, 160)


class TestPlanning(unittest.TestCase):
    def test_day30(self):
        self.assertEqual(alive_on_day30(30000, 10, 2500), (3000, True))
        self.assertEqual(alive_on_day30(30000, 15, 2500), (2000, False))

    def test_smallest_worlds(self):
        self.assertEqual(smallest_worlds(30, 3, 4000, 100, 160), 15)
        self.assertEqual(smallest_worlds(180, 3, 4000, 100, 160), 10)


if __name__ == "__main__":
    unittest.main()
