"""MMO302 lab 10 tests. Run with: python -m unittest test_chat_router.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from chat_router import Router, TokenBucket, predicted_deliveries, shard_name, simulate


class TestTokenBucket(unittest.TestCase):
    def test_lecture_sequence(self):
        # Same numbers as the lecture: burst of 3, one token per 5 s.
        b = TokenBucket(capacity=3, rate=0.2)
        got = [b.allow(t) for t in [0.0, 0.5, 1.0, 1.5, 2.0, 6.0, 7.0, 12.0]]
        self.assertEqual(got, [True, True, True, False, False, True, False, True])

    def test_never_above_capacity(self):
        b = TokenBucket(capacity=2, rate=1.0)
        self.assertEqual([b.allow(1000.0) for _ in range(3)], [True, True, False])


class TestRouter(unittest.TestCase):
    def test_fanout_excludes_sender(self):
        r = Router()
        for m in ["a", "b", "c", "d"]:
            r.subscribe(m, "guild")
        self.assertEqual(r.publish("a", "guild", 0.0), 3)
        self.assertEqual((r.accepted, r.deliveries), (1, 3))

    def test_rate_limit_counts_drops(self):
        r = Router(burst=2, refill_per_s=0.0)
        r.subscribe("a", "zone")
        r.subscribe("b", "zone")
        sent = [r.publish("a", "zone", t) for t in [0.0, 0.1, 0.2]]
        self.assertEqual(sent, [1, 1, 0])
        self.assertEqual((r.accepted, r.dropped, r.deliveries), (2, 1, 2))

    def test_non_member_cannot_post(self):
        r = Router()
        r.subscribe("a", "zone")
        self.assertEqual(r.publish("x", "zone", 0.0), 0)
        self.assertEqual((r.accepted, r.dropped, r.deliveries), (0, 0, 0))


class TestSharding(unittest.TestCase):
    def test_k1_is_unchanged(self):
        self.assertEqual(shard_name("trade", "p7", 1), "trade")

    def test_stable_and_balanced(self):
        names = [shard_name("trade", f"p{i}", 4) for i in range(4000)]
        self.assertEqual(names, [shard_name("trade", f"p{i}", 4) for i in range(4000)])
        counts = {n: names.count(n) for n in set(names)}
        self.assertEqual(sorted(counts), ["trade#0", "trade#1", "trade#2", "trade#3"])
        self.assertTrue(all(800 <= c <= 1200 for c in counts.values()), counts)


class TestSimulation(unittest.TestCase):
    def test_matches_model_within_10_percent(self):
        q = 0.05 / 60
        got, dropped = simulate(1000, q, seconds=1200, limit=False)
        want = predicted_deliveries(1000, q)
        self.assertEqual(dropped, 0.0)
        self.assertLess(abs(got - want) / want, 0.10, (got, want))

    def test_split_divides_load(self):
        q = 0.05 / 60
        one, _ = simulate(1000, q, seconds=1200, k=1, limit=False)
        four, _ = simulate(1000, q, seconds=1200, k=4, limit=False)
        self.assertLess(abs(one / four - 4) / 4, 0.15, (one, four))


if __name__ == "__main__":
    unittest.main()
