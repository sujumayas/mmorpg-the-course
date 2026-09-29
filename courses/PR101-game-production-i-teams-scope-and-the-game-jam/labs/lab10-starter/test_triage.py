import os
import unittest

import triage

HERE = os.path.dirname(os.path.abspath(__file__))


class PriorityTests(unittest.TestCase):
    def test_matrix_matches_lecture(self):
        expected = {
            (1, "always"): 1, (1, "often"): 1, (1, "rare"): 2,
            (2, "always"): 1, (2, "often"): 2, (2, "rare"): 3,
            (3, "always"): 2, (3, "often"): 3, (3, "rare"): 4,
            (4, "always"): 3, (4, "often"): 4, (4, "rare"): 4,
        }
        for (sev, freq), p in expected.items():
            with self.subTest(severity=sev, frequency=freq):
                self.assertEqual(triage.priority(sev, freq), p)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            triage.priority(0, "always")
        with self.assertRaises(ValueError):
            triage.priority(2, "sometimes")


class BacklogTests(unittest.TestCase):
    def test_find_rates_round_half_up(self):
        self.assertEqual(triage.find_rates(20, 0.8, 10),
                         [20, 16, 13, 10, 8, 7, 5, 4, 3, 3])
        self.assertEqual(triage.find_rates(13, 0.5, 2), [13, 7])

    def test_lecture_table(self):
        found = triage.find_rates(20, 0.8, 20)
        b = triage.backlog(30, found, 8)
        self.assertEqual(len(b), 20)
        self.assertEqual([round(x) for x in b[:10]],
                         [42, 50, 55, 57, 57, 56, 53, 49, 44, 39])
        self.assertEqual(triage.peak_days(b), [4, 5])
        self.assertEqual(triage.zero_day(b), 16)

    def test_regressions(self):
        found = triage.find_rates(20, 0.8, 30)
        b = triage.backlog(30, found, 8, r=0.25)
        self.assertAlmostEqual(b[5], 66.0)
        self.assertEqual(triage.peak_days(b), [6])
        self.assertEqual(triage.zero_day(b), 21)

    def test_never_fixes_more_than_exist(self):
        b = triage.backlog(2, [1, 0, 0], 10)
        self.assertEqual(b, [0.0, 0.0, 0.0])

    def test_check_yourself_question_one(self):
        b = triage.backlog(12, [10, 8, 6, 4], 7)
        self.assertEqual([round(x) for x in b], [15, 16, 15, 12])
        self.assertEqual(triage.zero_day(b), None)


class EstimateTests(unittest.TestCase):
    def test_lincoln_petersen(self):
        a = set(range(1, 25))           # 24 bugs
        b = set(range(13, 31))          # 18 bugs, 12 shared
        self.assertAlmostEqual(triage.lincoln_petersen(a, b), 36.0)

    def test_duplicates_count_once(self):
        self.assertAlmostEqual(
            triage.lincoln_petersen([1, 1, 2, 3], [2, 3, 3, 4]), 4.5)

    def test_no_overlap_raises(self):
        with self.assertRaises(ValueError):
            triage.lincoln_petersen({1, 2}, {3, 4})


class BlockerTests(unittest.TestCase):
    def test_sample_file(self):
        bugs = triage.load_bugs(os.path.join(HERE, "bugs_sample.csv"))
        self.assertEqual(triage.ship_blockers(bugs),
                         ["B-001", "B-004", "B-007", "B-011"])


if __name__ == "__main__":
    unittest.main()
