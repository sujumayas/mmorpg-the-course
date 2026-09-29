"""MMO405 lab 01 tests. Run with: python -m unittest test_selection_audit.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from selection_audit import load_players, observed_gap, selection_term, stratified_gap


def lecture_server(delta):
    """The lecture's invented 1,000-player server as rows (400 high, 600 low)."""
    rows = []
    for band, n, join, base in (("high", 400, 300, 0.70), ("low", 600, 120, 0.30)):
        kept_g = round(join * (base + delta))
        kept_u = round((n - join) * base)
        rows += [{"week1_band": band, "in_guild_d7": 1, "active_d30": 1}] * kept_g
        rows += [{"week1_band": band, "in_guild_d7": 1, "active_d30": 0}] * (join - kept_g)
        rows += [{"week1_band": band, "in_guild_d7": 0, "active_d30": 1}] * kept_u
        rows += [{"week1_band": band, "in_guild_d7": 0, "active_d30": 0}] * (n - join - kept_u)
    return rows


class TestObserved(unittest.TestCase):
    def test_lecture_table(self):
        g, u, gap = observed_gap(lecture_server(0.0))
        self.assertAlmostEqual(g, 246 / 420, places=9)
        self.assertAlmostEqual(u, 214 / 580, places=9)
        self.assertAlmostEqual(gap, 246 / 420 - 214 / 580, places=9)

    def test_lab_data(self):
        g, u, gap = observed_gap(load_players())
        self.assertAlmostEqual(g, 401 / 660, places=9)
        self.assertAlmostEqual(u, 402 / 1340, places=9)


class TestStratified(unittest.TestCase):
    def test_lecture_zero_effect(self):
        per, overall = stratified_gap(lecture_server(0.0))
        self.assertAlmostEqual(per["high"], 0.0, places=9)
        self.assertAlmostEqual(per["low"], 0.0, places=9)
        self.assertAlmostEqual(overall, 0.0, places=9)

    def test_lecture_five_points(self):
        _, overall = stratified_gap(lecture_server(0.05))
        self.assertAlmostEqual(overall, 0.05, places=9)

    def test_lab_data(self):
        per, overall = stratified_gap(load_players())
        self.assertEqual(set(per), {"low", "mid", "high"})
        self.assertAlmostEqual(overall, 0.05, places=9)

    def test_skips_one_sided_stratum(self):
        rows = lecture_server(0.0) + [{"week1_band": "bots", "in_guild_d7": 1, "active_d30": 1}] * 50
        per, overall = stratified_gap(rows)
        self.assertNotIn("bots", per)
        self.assertAlmostEqual(overall, 0.0, places=9)


class TestSelection(unittest.TestCase):
    def test_lecture_value(self):
        self.assertAlmostEqual(selection_term(0.70, 0.30, 300 / 420, 100 / 580),
                               0.40 * (300 / 420 - 100 / 580), places=12)

    def test_zero_when_no_sorting(self):
        self.assertEqual(selection_term(0.9, 0.1, 0.5, 0.5), 0.0)


if __name__ == "__main__":
    unittest.main()
