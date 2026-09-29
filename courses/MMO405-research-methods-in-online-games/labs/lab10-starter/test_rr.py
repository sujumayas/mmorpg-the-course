"""MMO405 lab 10 tests. Run with: python -m unittest test_rr.py
Every test fails on the starter and passes once the TODOs are done."""
import math
import unittest

from rr import epsilon, estimate, load_responses, n_for_margin, p_yes, posterior


class TestModel(unittest.TestCase):
    def test_p_yes_lecture(self):
        self.assertAlmostEqual(p_yes(0.10, 0.5), 0.30, places=12)
        self.assertAlmostEqual(p_yes(0.10, 1.0), 0.10, places=12)
        self.assertAlmostEqual(p_yes(0.37, 0.0), 0.50, places=12)

    def test_estimate_lecture(self):
        pi_hat, se = estimate(1200, 4000, 0.5)
        self.assertAlmostEqual(pi_hat, 0.10, places=12)
        self.assertAlmostEqual(se, math.sqrt(0.3 * 0.7 / 4000) / 0.5, places=12)

    def test_estimate_round_trip(self):
        for pi in (0.02, 0.2, 0.45):
            for t in (0.25, 0.6, 1.0):
                n = 10_000
                pi_hat, _ = estimate(p_yes(pi, t) * n, n, t)
                self.assertAlmostEqual(pi_hat, pi, places=9)

    def test_epsilon(self):
        self.assertAlmostEqual(epsilon(0.5), math.log(3), places=12)
        self.assertAlmostEqual(epsilon(1 / 3), math.log(2), places=12)
        self.assertEqual(epsilon(1.0), math.inf)

    def test_posterior_lecture(self):
        self.assertAlmostEqual(posterior(0.10, 0.5, 1), 0.25, places=12)
        self.assertAlmostEqual(posterior(0.10, 0.5, 0), 0.025 / 0.70, places=12)
        self.assertAlmostEqual(posterior(0.10, 1.0, 1), 1.0, places=12)

    def test_posterior_odds_factor(self):
        for prior in (0.05, 0.3):
            for t in (0.25, 0.75):
                post = posterior(prior, t, 1)
                factor = (post / (1 - post)) / (prior / (1 - prior))
                self.assertAlmostEqual(factor, (1 + t) / (1 - t), places=9)

    def test_n_for_margin(self):
        self.assertEqual(n_for_margin(0.02, 0.05, 0.75), 2324)
        n = n_for_margin(0.04, 0.10, 0.5)
        q = 0.30
        self.assertLessEqual(1.959963984540054 * math.sqrt(q * (1 - q) / n) / 0.5, 0.04)
        self.assertGreater(1.959963984540054 * math.sqrt(q * (1 - q) / (n - 1)) / 0.5, 0.04)


class TestData(unittest.TestCase):
    def test_file_estimates(self):
        data = load_responses()
        yes_d, n_d, t_d = data["direct"]
        yes_r, n_r, t_r = data["rr"]
        d_hat, _ = estimate(yes_d, n_d, t_d)
        r_hat, r_se = estimate(yes_r, n_r, t_r)
        self.assertAlmostEqual(d_hat, yes_d / n_d, places=12)
        self.assertAlmostEqual(r_hat, (yes_r / n_r - 0.25) / 0.5, places=12)
        self.assertGreater(r_se, 2 * math.sqrt(d_hat * (1 - d_hat) / n_d))


if __name__ == "__main__":
    unittest.main()
