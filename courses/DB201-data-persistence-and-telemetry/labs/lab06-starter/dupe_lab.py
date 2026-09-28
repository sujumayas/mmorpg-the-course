"""DB201 Lab 06 starter: reproduce the trade dupe, then make it impossible.

Run from this folder:
    python dupe_lab.py                 # all 20 interleavings for every handler, then a stress test
    python dupe_lab.py --order 121212  # step through one interleaving and print each state
    python dupe_lab.py --stress 2000   # threaded stress test with 2,000 attack attempts

Python 3.10+, standard library only (sqlite3, threading).

The world: character 1 (the giver) owns one sword, item instance 5001. Two trades run at
once: trade 1 gives the sword to character 2, trade 2 gives it to character 3. A correct
server ends with exactly one sword. The naive handler below does not.

An interleaving is a string of '1' and '2' saying which trade takes its next step, for
example "112122". Each handler is a generator that yields after every database step, so
the scheduler can pause it there. That is exactly what a busy server does to real requests.
"""
import argparse
import itertools
import json
import os
import random
import sqlite3
import tempfile
import threading
import time

SWORD = 5001
GIVER, RECEIVER_1, RECEIVER_2 = 1, 2, 3

SCHEMA = """
CREATE TABLE characters (
  character_id INTEGER PRIMARY KEY,
  name         TEXT NOT NULL
);
-- Blob model: one JSON list of item instance ids per character (Lab 02, Part D).
CREATE TABLE inventories (
  character_id INTEGER PRIMARY KEY REFERENCES characters(character_id),
  items        TEXT NOT NULL,
  version      INTEGER NOT NULL DEFAULT 0
);
-- Row model: one row per item instance (the Lab 02 reference schema, trimmed).
CREATE TABLE items (
  item_id  INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL REFERENCES characters(character_id)
);
"""


WAIT = "wait"  # a handler yields this when it could not get a lock; the scheduler retries later


def make_world(path):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path, isolation_level=None)  # autocommit: every statement commits
    con.executescript(SCHEMA)
    for cid, name in [(GIVER, "Giver"), (RECEIVER_1, "Bram"), (RECEIVER_2, "Cyra")]:
        con.execute("INSERT INTO characters VALUES (?, ?)", (cid, name))
        items = [SWORD] if cid == GIVER else []
        con.execute("INSERT INTO inventories (character_id, items) VALUES (?, ?)",
                    (cid, json.dumps(items)))
    con.execute("INSERT INTO items VALUES (?, ?)", (SWORD, GIVER))
    con.close()


def connect(path):
    # timeout=0: a locked database raises immediately instead of waiting, so the
    # deterministic scheduler can see the lock and run the other trade instead.
    con = sqlite3.connect(path, isolation_level=None, timeout=0, check_same_thread=False)
    return con


def load(con, cid):
    return json.loads(con.execute(
        "SELECT items FROM inventories WHERE character_id = ?", (cid,)).fetchone()[0])


def save(con, cid, items):
    con.execute("UPDATE inventories SET items = ? WHERE character_id = ?",
                (json.dumps(items), cid))


def copies_in_blobs(con):
    return sum(load(con, cid).count(SWORD) for cid in (GIVER, RECEIVER_1, RECEIVER_2))


def copies_in_rows(con):
    return con.execute("SELECT COUNT(*) FROM items WHERE item_id = ?", (SWORD,)).fetchone()[0]


# ---------------------------------------------------------------------------
# The naive handler: read, give, take. Three steps, no transaction.
# ---------------------------------------------------------------------------
def naive_trade(con, receiver):
    inv = load(con, GIVER)                 # step 1: read the giver's inventory
    if SWORD not in inv:
        return "rejected"
    yield "read"
    got = load(con, receiver)              # step 2: give (read-modify-write the receiver)
    save(con, receiver, got + [SWORD])
    yield "give"
    inv.remove(SWORD)                      # step 3: take (write back the copy read in step 1)
    save(con, GIVER, inv)
    yield "take"
    return "done"


# ---------------------------------------------------------------------------
# TODO Part B: three fixes. Each must keep the same three yields (or fewer) so the
# scheduler can still interleave them, and each must end with exactly one sword.
# ---------------------------------------------------------------------------
def conditional_trade(con, receiver):
    """TODO B1 (row model): move the sword with ONE statement,
        UPDATE items SET owner_id = ? WHERE item_id = ? AND owner_id = ?
    and use cursor.rowcount to decide between "done" and "rejected".
    Yield once after the statement. Count copies with copies_in_rows()."""
    raise NotImplementedError("conditional_trade")
    yield  # keeps this a generator


def locked_trade(con, receiver):
    """TODO B2 (blob model): wrap the naive steps in BEGIN IMMEDIATE ... COMMIT.
    If BEGIN IMMEDIATE raises sqlite3.OperationalError (database is locked), yield WAIT
    and try again, in a loop, so the scheduler can run the other trade meanwhile. In PostgreSQL you would write
    SELECT ... FOR UPDATE on the giver's row instead (see lecture section 4)."""
    raise NotImplementedError("locked_trade")
    yield


def versioned_trade(con, receiver):
    """TODO B3 (blob model, optimistic): read the giver's items AND version in step 1.
    Take before give, and make the take conditional:
        UPDATE inventories SET items = ?, version = version + 1
        WHERE character_id = ? AND version = ?
    If rowcount is 0 someone else changed the giver first: return "conflict" without
    giving anything."""
    raise NotImplementedError("versioned_trade")
    yield


# ---------------------------------------------------------------------------
# The deterministic scheduler
# ---------------------------------------------------------------------------
def run_interleaving(handler, order, path, counter, verbose=False):
    """Run two trades following `order`. Returns (copies, outcome1, outcome2)."""
    make_world(path)
    cons = {"1": connect(path), "2": connect(path)}
    gens = {"1": handler(cons["1"], RECEIVER_1), "2": handler(cons["2"], RECEIVER_2)}
    out = {"1": None, "2": None}
    pending = list(order)
    stalls = 0
    while any(v is None for v in out.values()):
        if pending:
            who = pending.pop(0)
        else:                             # order used up: finish whoever is left
            who = "1" if out["1"] is None else "2"
        if out[who] is not None:          # that trade already finished; skip its turn
            continue
        try:
            step = next(gens[who])
        except StopIteration as stop:
            out[who] = stop.value or "done"
            continue
        if step == WAIT:
            # Blocked on a lock: give this turn back and let the other trade move.
            pending.append(who)
            other = "2" if who == "1" else "1"
            if other in pending:
                pending.remove(other)
            pending.insert(0, other)
            stalls += 1
            if stalls > 50:
                raise RuntimeError("both trades keep waiting: deadlock?")
            continue
        stalls = 0
        if verbose:
            print(f"  trade {who}: {step:<6} -> {state(cons[who])}")
    copies = counter(cons["1"])
    for c in cons.values():
        c.close()
    return copies, out["1"], out["2"]


def state(con):
    inv = {cid: load(con, cid) for cid in (GIVER, RECEIVER_1, RECEIVER_2)}
    return f"giver {inv[GIVER]}  bram {inv[RECEIVER_1]}  cyra {inv[RECEIVER_2]}"


def all_orders():
    """The 20 ways to interleave two 3-step trades: choose where trade 1's steps go."""
    for pos in itertools.combinations(range(6), 3):
        yield "".join("1" if i in pos else "2" for i in range(6))


def table(handler, counter, path):
    dupes = 0
    for order in all_orders():
        copies, o1, o2 = run_interleaving(handler, order, path, counter)
        dupes += copies > 1
        flag = "DUPE" if copies > 1 else ("LOST" if copies == 0 else "ok")
        print(f"  {order}  copies={copies}  trade1={o1:<9} trade2={o2:<9} {flag}")
    print(f"  -> {dupes} of 20 interleavings duplicate the sword")
    return dupes


# ---------------------------------------------------------------------------
# Threaded stress test: real threads, real timing
# ---------------------------------------------------------------------------
def stress(handler, counter, attempts, path, jitter_ms=3.0, work_ms=0.5, seed=6):
    """Fire both trades at nearly the same moment `attempts` times.
    Each trade starts after a random delay in [0, jitter_ms] and pauses work_ms
    between steps (standing in for server work and network round trips).
    Returns the fraction of attempts that produced a dupe."""
    run_interleaving(handler, "111222", path, counter)  # raises NotImplementedError for TODOs
    rng = random.Random(seed)
    dupes = 0
    for _ in range(attempts):
        make_world(path)
        delays = [rng.uniform(0, jitter_ms) / 1000 for _ in range(2)]

        def worker(receiver, delay):
            con = connect(path)
            con.execute("PRAGMA busy_timeout = 2000")  # real servers wait for locks
            time.sleep(delay)
            gen = handler(con, receiver)
            while True:
                try:
                    step = next(gen)
                except StopIteration:
                    break
                time.sleep(0.0005 if step == WAIT else work_ms / 1000)
            con.close()

        ts = [threading.Thread(target=worker, args=(r, d))
              for r, d in zip((RECEIVER_1, RECEIVER_2), delays)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        con = connect(path)
        dupes += counter(con) > 1
        con.close()
    return dupes / attempts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", help="one interleaving to trace, e.g. 121212")
    ap.add_argument("--stress", type=int, default=300)
    args = ap.parse_args()
    path = os.path.join(tempfile.mkdtemp(prefix="db201_lab06_"), "world.db")

    if args.order:
        print(f"naive_trade, order {args.order}")
        copies, o1, o2 = run_interleaving(naive_trade, args.order, path, copies_in_blobs,
                                          verbose=True)
        print(f"copies of the sword: {copies}")
        return

    handlers = [("naive_trade", naive_trade, copies_in_blobs),
                ("conditional_trade", conditional_trade, copies_in_rows),
                ("locked_trade", locked_trade, copies_in_blobs),
                ("versioned_trade", versioned_trade, copies_in_blobs)]
    for name, h, counter in handlers:
        print(f"\n== {name}: all interleavings")
        try:
            table(h, counter, path)
        except NotImplementedError:
            print("  TODO")
    print(f"\n== threaded stress test, {args.stress} attempts")
    for name, h, counter in handlers:
        try:
            rate = stress(h, counter, args.stress, path)
            print(f"  {name:<18} dupe rate {rate:.1%}")
        except NotImplementedError:
            print(f"  {name:<18} TODO")


if __name__ == "__main__":
    main()
