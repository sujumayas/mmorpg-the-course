"""MMO302 lab 08 tests. Run with: python -m unittest test_item_service.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from item_service import (Crash, audit, gold, move_item, open_world, stress,
                          transfer_gold, transfer_gold_buggy)


class TestAudit(unittest.TestCase):
    def test_fresh_world_balances(self):
        self.assertEqual(audit(open_world()), {"gold_drift": 0, "items": 20})

    def test_buggy_transfer_shows_drift(self):
        drift = audit(stress(transfer_gold_buggy))["gold_drift"]
        self.assertGreater(drift, 0)       # the dupe you are asked to reproduce


class TestTransfer(unittest.TestCase):
    def test_retry_is_replayed(self):
        db = open_world()
        self.assertEqual(transfer_gold(db, "t1", "ayla", "bren", 300), "ok")
        self.assertEqual(transfer_gold(db, "t1", "ayla", "bren", 300), "ok (replayed)")
        self.assertEqual((gold(db, "ayla"), gold(db, "bren")), (700, 1300))

    def test_crash_leaves_no_trace_and_retry_works(self):
        db = open_world()
        with self.assertRaises(Crash):
            transfer_gold(db, "t2", "ayla", "bren", 100, crash=True)
        self.assertEqual((gold(db, "ayla"), gold(db, "bren")), (1000, 1000))
        self.assertEqual(transfer_gold(db, "t2", "ayla", "bren", 100), "ok")
        self.assertEqual(audit(db)["gold_drift"], 0)

    def test_overdraft_refused(self):
        db = open_world()
        self.assertEqual(transfer_gold(db, "t3", "ayla", "bren", 5000), "insufficient")
        self.assertEqual(transfer_gold(db, "t3", "ayla", "bren", 5000), "insufficient (replayed)")
        self.assertEqual(gold(db, "ayla"), 1000)

    def test_stress_has_zero_drift(self):
        self.assertEqual(audit(stress(transfer_gold))["gold_drift"], 0)


class TestMoveItem(unittest.TestCase):
    def test_only_owner_can_move(self):
        db = open_world()
        self.assertEqual(move_item(db, "m1", 1, "ayla", "bren"), "ok")
        self.assertEqual(move_item(db, "m2", 1, "ayla", "cato"), "not owner")
        self.assertEqual(move_item(db, "m1", 1, "ayla", "bren"), "ok (replayed)")
        self.assertEqual(audit(db)["items"], 20)


if __name__ == "__main__":
    unittest.main()
