"""Tests for Lab 10. Run:  python -m unittest test_ugc_rewards.py

Every test fails on the starter (the functions raise NotImplementedError)
and passes on a correct solution. The expected values come from the
week 10 lecture.
"""
import unittest

import ugc_rewards as u


class TestModel(unittest.TestCase):
    def test_harmonic(self):
        self.assertAlmostEqual(u.harmonic(1), 1.0)
        self.assertAlmostEqual(u.harmonic(10), 2.928968, places=5)

    def test_expected_best_matches_lecture(self):
        for n, want in [(1, 1.100), (10, 1.293), (100, 1.519),
                        (1_000, 1.749), (10_000, 1.979), (100_000, 2.209)]:
            self.assertAlmostEqual(u.expected_best(n, 0.10), want, places=3)

    def test_levers(self):
        self.assertAlmostEqual(u.expected_best(10_000, 0.02), 1.196, places=3)
        self.assertAlmostEqual(u.expected_best(50, 0.10), 1.450, places=3)
        self.assertAlmostEqual(u.expected_best(10_000, 0.10, cap=1.2), 1.2)
        # a cap above the expected best does nothing
        self.assertAlmostEqual(u.expected_best(10, 0.10, cap=1.5), 1.293, places=3)

    def test_inflow(self):
        self.assertAlmostEqual(u.inflow_multiplier(0.3, 1.979), 1.2937, places=4)
        self.assertAlmostEqual(u.inflow_multiplier(0.0, 3.0), 1.0)


class TestSimulation(unittest.TestCase):
    def test_simulation_agrees_with_formula(self):
        sim = u.simulate_best(1_000, 0.10, trials=1_000, seed=1)
        self.assertAlmostEqual(sim, 1.749, delta=0.02)

    def test_uniform_tail_is_bounded(self):
        # Uniform overpay on [0, 2m]: the best of n has mean 1 + 2m * n / (n + 1)
        sim = u.simulate_best(200, 0.10, trials=1_000, seed=2, dist="uniform")
        self.assertAlmostEqual(sim, 1 + 0.2 * 200 / 201, delta=0.005)
        self.assertLess(sim, 1.2)

    def test_seed_is_reproducible(self):
        a = u.simulate_best(50, 0.10, trials=100, seed=7)
        b = u.simulate_best(50, 0.10, trials=100, seed=7)
        self.assertEqual(a, b)


class TestFunnel(unittest.TestCase):
    def test_lecture_funnel(self):
        counts = u.funnel(5_000, [0.6, 0.3, 0.4])
        self.assertEqual(len(counts), 3)
        for got, want in zip(counts, [3_000, 900, 360]):
            self.assertAlmostEqual(got, want)

    def test_check_yourself_funnel(self):
        self.assertAlmostEqual(u.funnel(8_000, [0.5, 0.25, 0.5])[-1], 500)

    def test_largest_pool(self):
        # lecture check-yourself 3: m = 0.08, best must stay at or under 1.3
        self.assertEqual(u.largest_pool(0.08, 1.3), 23)
        self.assertEqual(u.largest_pool(0.10, 1.1), 1)


if __name__ == "__main__":
    unittest.main()
