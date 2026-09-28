"""MMO302 lab 12 tests. Run with: python -m unittest test_tidi.py"""
import unittest

from tidi import dilation, simulate, work


class TestModel(unittest.TestCase):
    def test_lecture_table(self):
        self.assertAlmostEqual(work(1000), 1.30)
        self.assertAlmostEqual(work(3000), 9.90)
        self.assertAlmostEqual(dilation(500), 1.0)
        self.assertAlmostEqual(dilation(1000), 1 / 1.3)
        self.assertAlmostEqual(dilation(3500), 0.1)


class TestSimulate(unittest.TestCase):
    def test_tidi_keeps_up_below_floor(self):
        r = simulate([2000] * 100, "tidi")
        self.assertEqual(r["real_s"], 100)
        self.assertAlmostEqual(r["game_s"], 100 / 4.6)
        self.assertAlmostEqual(r["max_backlog"], 0.0)
        self.assertAlmostEqual(r["max_delay"], 4.6)

    def test_no_tidi_backlog_grows(self):
        r = simulate([3000] * 60, "none")
        self.assertAlmostEqual(r["game_s"], 60)
        self.assertAlmostEqual(r["end_backlog"], 60 * 8.9)
        self.assertAlmostEqual(r["max_delay"], 60 * 8.9 + 1)

    def test_floor_overload(self):
        r = simulate([3500] * 10, "tidi")
        self.assertAlmostEqual(r["end_backlog"], 10 * 0.33)


if __name__ == "__main__":
    unittest.main()
