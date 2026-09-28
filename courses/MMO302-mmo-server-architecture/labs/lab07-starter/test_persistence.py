"""MMO302 lab 07 tests. Run with: python -m unittest test_persistence.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from persistence import Database, EventLog, WriteBehindStore, apply, run, ROW_BYTES


class TestWriteBehind(unittest.TestCase):
    def test_coalesces_repeated_changes(self):
        db = Database()
        s = WriteBehindStore(db, flush_ms=1000)
        for t in (10, 20, 30):
            s.add("ayla", "gold", 5, t)
        s.add("ayla", "xp", 100, 40)
        s.tick(1000)
        self.assertEqual(db.commits, 1)                    # one commit per dirty player
        self.assertEqual(db.bytes, 2 * ROW_BYTES)          # two distinct rows
        self.assertEqual(db.rows[("ayla", "gold")], 15)

    def test_crash_loses_only_unflushed(self):
        db = Database()
        s = WriteBehindStore(db, flush_ms=1000)
        s.add("ayla", "gold", 5, 100)
        s.tick(1000)
        s.add("ayla", "gold", 7, 1200)
        s.add("bren", "xp", 3, 1300)
        self.assertEqual(s.oldest_dirty_age(1500), 300)
        self.assertEqual(s.crash(), 2)
        self.assertEqual(s.memory[("ayla", "gold")], 5)

    def test_commit_rate_matches_lecture(self):
        r = run("write-behind", players=200, flush_ms=10_000)
        self.assertAlmostEqual(r["commits"] / 120, 200 / 10, delta=1.0)   # N / F


class TestEventLog(unittest.TestCase):
    def test_group_commit_and_recovery(self):
        db = Database()
        log = EventLog(db, group_ms=10, snapshot_ms=100)
        log.append(("ayla", "gold", 50), 1)
        log.append(("ayla", "gold", -20), 2)
        log.tick(10)                                     # one commit for two events
        self.assertEqual(db.commits, 1)
        log.tick(100)                                    # snapshot covers both
        log.append(("bren", "xp", 80), 101)
        log.tick(110)
        log.append(("bren", "xp", 5), 111)               # still pending at crash
        state, replayed, lost = log.crash_and_recover()
        self.assertEqual(state, {"ayla": {"gold": 30}, "bren": {"xp": 80}})
        self.assertEqual((replayed, lost), (1, 1))

    def test_snapshot_plus_tail_equals_full_replay(self):
        db = Database()
        log = EventLog(db, group_ms=10, snapshot_ms=50)
        for t in range(1, 300):
            log.append((t % 7, "gold", t), t)
            log.tick(t)
        state, _, _ = log.crash_and_recover()
        full = {}
        for e in log.durable:
            apply(full, e)
        self.assertEqual(state, full)

    def test_replay_matches_lecture(self):
        r = run("event log", players=200, crash_ms=90_000, snapshot_ms=60_000)
        self.assertAlmostEqual(r["replayed"], 200 * 0.5 * 30, delta=300)   # N x c x (t mod K)
        self.assertLessEqual(r["lost"], 10)


if __name__ == "__main__":
    unittest.main()
