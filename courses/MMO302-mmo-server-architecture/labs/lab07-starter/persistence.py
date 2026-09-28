"""MMO302 lab 07: persistence strategies under crash.

Time is in integer milliseconds so no float comparisons creep in.
Standard library only. Run the tests with:  python -m unittest test_persistence.py
"""
import random

ROW_BYTES = 120     # bytes in one changed row or one event (lecture's s)


def apply(state, event):
    """Apply one event (player, field, delta) to a state dict. Provided."""
    player, fld, delta = event
    row = state.setdefault(player, {})
    row[fld] = row.get(fld, 0) + delta
    return state


class Database:
    """The system of record. Provided. Counts commits and bytes."""

    def __init__(self):
        self.rows = {}          # (player, field) -> value
        self.commits = 0
        self.bytes = 0

    def commit(self, writes, size_bytes):
        self.rows.update(writes)
        self.commits += 1
        self.bytes += size_bytes


class WriteBehindStore:
    """Changes live in memory; dirty rows are flushed every flush_ms.

    One flush writes each dirty player's dirty rows as ONE commit, so repeated
    changes to the same row inside a window are coalesced.
    """

    def __init__(self, db, flush_ms):
        self.db = db
        self.flush_ms = flush_ms
        self.memory = {}                 # (player, field) -> value
        self.dirty = {}                  # player -> set of fields
        self.unflushed_changes = 0       # changes made since the last flush
        self.first_dirty_ms = None       # time of the oldest unflushed change
        self.next_flush = flush_ms

    def add(self, player, fld, delta, now):
        # TODO 1: update memory, mark (player, fld) dirty, count the change,
        # and remember when the oldest unflushed change happened.
        raise NotImplementedError("TODO 1")

    def flush(self):
        # TODO 2: one db.commit per dirty player, containing only that
        # player's dirty rows, size = rows x ROW_BYTES. Then clear the dirty marks.
        raise NotImplementedError("TODO 2")

    def tick(self, now):
        if now >= self.next_flush:
            self.flush()
            self.next_flush += self.flush_ms

    def oldest_dirty_age(self, now):
        return 0 if self.first_dirty_ms is None else now - self.first_dirty_ms

    def crash(self):
        """The process dies. Returns the number of changes lost."""
        # TODO 3: memory is gone. Rebuild memory from the database and
        # report how many changes never reached it.
        raise NotImplementedError("TODO 3")


class EventLog:
    """Append-only log with group commit and periodic snapshots."""

    def __init__(self, db, group_ms, snapshot_ms):
        self.db = db
        self.group_ms = group_ms
        self.snapshot_ms = snapshot_ms
        self.pending = []           # appended, not yet committed
        self.durable = []           # committed events, in order
        self.snapshot = ({}, 0)     # (state, number of durable events it covers)
        self.next_commit = group_ms
        self.next_snapshot = snapshot_ms

    def append(self, event, now):
        self.pending.append(event)

    def tick(self, now):
        # TODO 4: at each group-commit boundary, commit all pending events as
        # ONE db.commit (size = events x ROW_BYTES) and move them to durable.
        # Skip the commit if nothing is pending. At each snapshot boundary,
        # snapshot the state of all durable events.
        raise NotImplementedError("TODO 4")

    def crash_and_recover(self):
        """Returns (state, events_replayed, events_lost)."""
        # TODO 5: pending events are lost. Start from a copy of the snapshot
        # and replay the durable events it does not cover.
        raise NotImplementedError("TODO 5")


def run(strategy, players=200, rate=0.5, duration_ms=120_000, crash_ms=None,
        flush_ms=10_000, group_ms=10, snapshot_ms=60_000, seed=1):
    """Simulate a shard in 10 ms steps. Each player makes a change with
    probability rate x 0.01 per step, on one of 3 fields. Returns a dict with
    commits, bytes, changes, lost, replayed. Provided."""
    rng = random.Random(seed)
    db = Database()
    store = WriteBehindStore(db, flush_ms) if strategy == "write-behind" else EventLog(db, group_ms, snapshot_ms)
    changes = lost = replayed = 0
    end = duration_ms if crash_ms is None else crash_ms
    for now in range(10, end + 1, 10):
        for p in range(players):
            if rng.random() < rate * 0.01:
                changes += 1
                fld = rng.choice(["gold", "xp", "rep"])
                if strategy == "write-behind":
                    store.add(p, fld, 1, now)
                else:
                    store.append((p, fld, 1), now)
        store.tick(now)
    if crash_ms is not None:
        if strategy == "write-behind":
            lost = store.crash()
        else:
            _, replayed, lost = store.crash_and_recover()
    return {"commits": db.commits, "bytes": db.bytes, "changes": changes,
            "lost": lost, "replayed": replayed}


def report():
    for s in ["write-behind", "event log"]:
        r = run(s)
        secs = 120
        print(f"{s:12} commits/s {r['commits']/secs:7.1f}  kB/s {r['bytes']/secs/1000:6.1f}  changes/s {r['changes']/secs:6.1f}")
    r = run("event log", crash_ms=90_000)
    print("event log crash at 90 s: replayed", r["replayed"], "lost", r["lost"])
    r = run("write-behind", crash_ms=95_000)
    print("write-behind crash at 95 s: lost", r["lost"])


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"not run yet: {e} is still a stub. Fill in the TODOs, then run the tests.")
