"""MMO407 lab 04 tests. Run with: python -m unittest test_rebuild_model.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from rebuild_model import (REF, crossover_m, old_game_gap, patch_months,
                           players_after, rebuild_months)

G, F, T_R = REF["G"], REF["F"], REF["T_r"]


class TestLectureTable(unittest.TestCase):
    def test_patch(self):
        self.assertAlmostEqual(patch_months(G, 0.1, 3, F), 36.0)
        self.assertAlmostEqual(patch_months(G, 0.5, 1.5, F), 37.5)
        self.assertAlmostEqual(patch_months(G, 0.5, 4, F), 75.0)
        self.assertAlmostEqual(patch_months(400, 0.3, 2, 10), 52.0)

    def test_rebuild(self):
        self.assertAlmostEqual(rebuild_months(G, 0.1, F, T_R), 51.0)
        self.assertAlmostEqual(rebuild_months(G, 0.5, F, T_R), 39.0)
        self.assertAlmostEqual(rebuild_months(G, 0.5, F, T_R, 0.25), 47.0)
        self.assertAlmostEqual(rebuild_months(G, 0.5, F, T_R, 0.25, 0.5), 43.0)
        # carry-over can never make the content gap negative
        self.assertAlmostEqual(rebuild_months(100, 0.9, 10, 10, 0.5, 1.0), 20.0)

    def test_crossover(self):
        self.assertAlmostEqual(crossover_m(G, 0.5, F, T_R), 1.6)
        self.assertAlmostEqual(crossover_m(G, 0.1, F, T_R), 8.0)
        self.assertAlmostEqual(crossover_m(250, 0.4, 10, 18), 1.8)


class TestPlayers(unittest.TestCase):
    def test_old_game_gap(self):
        self.assertAlmostEqual(old_game_gap(0, G, 0.5, 4, F, 0.25), 300.0)
        self.assertAlmostEqual(old_game_gap(12, G, 0.5, 4, F, 0.25), 288.0)
        self.assertAlmostEqual(old_game_gap(12, G, 0.5, 4, F, 0.0), 300.0)
        self.assertAlmostEqual(old_game_gap(10_000, G, 0.5, 4, F, 0.25), 0.0)

    def test_players_after(self):
        full_gap = lambda t: G
        self.assertAlmostEqual(players_after(100_000, 10, full_gap, G), 100_000 * 0.93 ** 10,
                               places=6)
        no_gap = lambda t: 0.0
        self.assertAlmostEqual(players_after(50_000, 3, no_gap, G, base=0.1, k=0.5),
                               50_000 * 0.9 ** 3, places=6)
        falling = lambda t: G * (1 - t / 4)
        expected = 1000 * (1 - 0.07) * (1 - 0.0575) * (1 - 0.045) * (1 - 0.0325)
        self.assertAlmostEqual(players_after(1000, 4, falling, G), expected, places=9)


if __name__ == "__main__":
    unittest.main()
