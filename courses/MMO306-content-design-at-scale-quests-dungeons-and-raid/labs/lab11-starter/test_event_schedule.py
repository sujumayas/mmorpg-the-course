"""Tests for Lab 11. Run:  python -m unittest test_event_schedule.py

Every test fails on the starter and passes on a correct solution.
Expected values come from the week 11 lecture (N = 3,000, S = 90, W = 15).
"""
import os
import unittest

import event_schedule as e

HERE = os.path.dirname(os.path.abspath(__file__))


class TestFormulas(unittest.TestCase):
    def test_reach(self):
        self.assertAlmostEqual(e.reach(60, 90, 15), 1.0)
        self.assertAlmostEqual(e.reach(105, 90, 15), 1.0)
        self.assertAlmostEqual(e.reach(180, 90, 15), 105 / 180)
        self.assertAlmostEqual(e.reach(1440, 90, 15), 105 / 1440)

    def test_crowd(self):
        self.assertAlmostEqual(e.crowd(3000, 30, 90, 15), 62.5)
        self.assertAlmostEqual(e.crowd(3000, 60, 90, 15), 125.0)
        for T in (105, 180, 360, 1440):
            self.assertAlmostEqual(e.crowd(3000, T, 90, 15), 218.75)

    def test_n_crit(self):
        self.assertAlmostEqual(e.n_crit(40, 90, 15), 548.571, places=3)
        self.assertAlmostEqual(e.n_crit(30, 45, 15), 720.0)

    def test_kill_time(self):
        self.assertAlmostEqual(e.kill_time(10, 200_000, 60_000, 500), 160.0)
        self.assertAlmostEqual(e.kill_time(40, 200_000, 60_000, 500), 130.0)
        self.assertAlmostEqual(e.kill_time(150, 200_000, 60_000, 500), 122.667, places=3)


class TestSimulation(unittest.TestCase):
    def test_uniform_matches_formulas(self):
        r = e.simulate(3000, 90, 15, 360, days=10, seed=11)
        self.assertAlmostEqual(r["reach"], 105 / 360, delta=0.01)
        self.assertAlmostEqual(r["mean_crowd"], 218.75, delta=6)

    def test_below_knee_everyone_reaches(self):
        r = e.simulate(2000, 90, 15, 60, days=5, seed=3)
        self.assertAlmostEqual(r["reach"], 1.0, delta=0.001)
        self.assertAlmostEqual(r["mean_crowd"], 2000 * 60 / 1440, delta=4)

    def test_crowd_by_start_keys(self):
        r = e.simulate(500, 90, 15, 360, days=2, seed=5)
        self.assertEqual(sorted(r["crowd_by_start"]), [0, 360, 720, 1080])

    def test_prime_time_changes_crowds(self):
        w = e.load_hourly_weights(os.path.join(HERE, "online_by_hour.csv"))
        self.assertEqual(len(w), 24)
        self.assertAlmostEqual(sum(w), 1.0)
        r = e.simulate(3000, 90, 15, 240, days=10, seed=8, hourly_weights=w)
        by = r["crowd_by_start"]
        # the 20:00 occurrence draws far more than the 04:00 one
        self.assertGreater(by[1200], 3 * by[240])
        # reach doesn't depend on when sessions start, only on T, S and W
        self.assertAlmostEqual(r["reach"], 105 / 240, delta=0.02)


if __name__ == "__main__":
    unittest.main()
