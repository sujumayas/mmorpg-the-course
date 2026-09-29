"""MMO405 lab 03 tests. Run with: python -m unittest test_telemetry.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from telemetry import corrected_r, hours_by_account, load_events, load_survey, sessionize


def lecture_evening():
    """The lecture's invented evening: login 19:00, activity 19:00-19:40 and 20:05-20:50, logout 21:30."""
    ev = [(1140, "login")]
    ev += [(m, "activity") for m in range(1140, 1181, 2)]
    ev += [(m, "activity") for m in range(1205, 1251, 5)]
    ev.append((1290, "logout"))
    return ev


class TestSessionize(unittest.TestCase):
    def test_lecture_rules(self):
        self.assertEqual(sessionize(lecture_evening(), 10), [(1140, 1180), (1205, 1250)])
        self.assertEqual(sessionize(lecture_evening(), 30), [(1140, 1250)])

    def test_ignores_login_logout_and_edges(self):
        ev = [(0, "login"), (5, "activity"), (15, "activity"), (26, "activity"), (90, "logout")]
        self.assertEqual(sessionize(ev, 10), [(5, 15), (26, 26)])
        self.assertEqual(sessionize(ev, 11), [(5, 26)])
        self.assertEqual(sessionize([(0, "login"), (60, "logout")], 10), [])


class TestHours(unittest.TestCase):
    def test_lecture_evening_hours(self):
        h10 = hours_by_account({"x": lecture_evening()}, 10)
        h30 = hours_by_account({"x": lecture_evening()}, 30)
        self.assertAlmostEqual(h10["x"], 85 / 60, places=12)
        self.assertAlmostEqual(h30["x"], 110 / 60, places=12)

    def test_zeros_for_silent_accounts(self):
        h = hours_by_account({"x": lecture_evening()}, 10, accounts=["x", "y"])
        self.assertEqual(h["y"], 0.0)

    def test_lab_data(self):
        ev, players = load_events(), sorted(load_survey())
        self.assertAlmostEqual(sum(hours_by_account(ev, 10, players).values()), 1876.0333, places=3)
        self.assertAlmostEqual(sum(hours_by_account(ev, 30, players).values()), 2147.1833, places=3)
        allh = hours_by_account(ev, 30)
        self.assertEqual(len(allh), 273)
        self.assertAlmostEqual(allh["B0001"], 140.0, places=9)


class TestCorrection(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(corrected_r(0.2, 0.5), 0.4, places=12)
        self.assertAlmostEqual(corrected_r(0.2, 0.5, rel_y=0.64), 0.5, places=12)


if __name__ == "__main__":
    unittest.main()
