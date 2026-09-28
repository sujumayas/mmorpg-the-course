"""MMO302 lab 09 tests. Run with: python -m unittest test_login_service.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from login_service import TicketService, World, estimate_wait, evening


class TestQueue(unittest.TestCase):
    def test_matches_lecture_evening(self):
        log = evening()
        self.assertEqual([log[t] for t in (0, 60, 120, 180, 240, 360)],
                         [20, 1220, 2420, 3585, 2685, 885])
        self.assertEqual(next(t for t, q in enumerate(log) if t > 180 and q == 0), 419)

    def test_estimate(self):
        self.assertEqual(estimate_wait(1500, 3000, 120), 60)
        self.assertAlmostEqual(estimate_wait(2000, 5000, 150), 60)

    def test_reconnects_go_first(self):
        w = World(cap=1000, session_min=100)      # 10 logouts per minute
        w.arrive(50)
        w.reconnect(8)
        self.assertAlmostEqual(w.step(), 10)
        self.assertAlmostEqual(w.priority, 0)
        self.assertAlmostEqual(w.queue, 48)

    def test_abandonment_shrinks_queue(self):
        w = World(cap=1000, session_min=100, abandon_min=10)
        w.arrive(110)
        w.step()                                   # 10 admitted, then 10% of 100 leave
        self.assertAlmostEqual(w.queue, 90)


class TestTickets(unittest.TestCase):
    def setUp(self):
        self.svc = TicketService(b"test-secret", ttl=60)
        self.t = self.svc.issue(40213, "world-3", now=1000, ticket_id="abc")

    def test_accept_once_then_replay(self):
        self.assertEqual(self.svc.verify(self.t, "world-3", 1030), "accept 40213")
        self.assertEqual(self.svc.verify(self.t, "world-3", 1031), "reject: replayed")

    def test_rejections(self):
        self.assertEqual(self.svc.verify(self.t, "world-3", 1061), "reject: expired")
        self.assertEqual(self.svc.verify(self.t, "world-5", 1030), "reject: wrong world")
        self.assertEqual(self.svc.verify(self.t.replace("40213", "1"), "world-3", 1030), "reject: forged")
        self.assertEqual(self.svc.verify("abc|40213", "world-3", 1030), "reject: malformed")

    def test_used_ids_are_forgotten_after_expiry(self):
        self.svc.verify(self.t, "world-3", 1030)
        later = self.svc.issue(7, "world-3", now=2000, ticket_id="def")
        self.svc.verify(later, "world-3", 2001)
        self.assertNotIn("abc", self.svc.used)


if __name__ == "__main__":
    unittest.main()
