"""MMO302 lab 08: a dupe-proof item service.

SQLite stands in for PostgreSQL; the SQL carries over with small changes
(noted in the lab sheet). Standard library only.
Run the tests with:  python -m unittest test_item_service.py
"""
import random
import sqlite3


class Crash(Exception):
    """Raised to simulate the server process dying mid-operation."""


SCHEMA = """
CREATE TABLE wallet (owner TEXT PRIMARY KEY, gold INTEGER NOT NULL CHECK (gold >= 0));
CREATE TABLE item (item_id INTEGER PRIMARY KEY, owner TEXT NOT NULL);
CREATE TABLE ledger (kind TEXT NOT NULL, amount INTEGER NOT NULL);  -- 'mint' or 'destroy'
CREATE TABLE applied_op (op_id TEXT PRIMARY KEY, result TEXT NOT NULL);
"""


def open_world(players=("ayla", "bren", "cato", "dara"), gold_each=1000, items_each=5):
    """A fresh in-memory world. Every starting coin and item is minted in the ledger. Provided."""
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.executescript(SCHEMA)
    next_id = 1
    for p in players:
        db.execute("INSERT INTO wallet VALUES (?, ?)", (p, gold_each))
        db.execute("INSERT INTO ledger VALUES ('mint', ?)", (gold_each,))
        for _ in range(items_each):
            db.execute("INSERT INTO item VALUES (?, ?)", (next_id, p))
            next_id += 1
    return db


def gold(db, owner):
    return db.execute("SELECT gold FROM wallet WHERE owner = ?", (owner,)).fetchone()[0]


def transfer_gold_buggy(db, op_id, src, dst, amount, crash=False):
    """The shipped version: give first, take second, two separate writes,
    no idempotency. Provided so you can reproduce the dupe."""
    if gold(db, src) < amount:
        return "insufficient"
    db.execute("UPDATE wallet SET gold = gold + ? WHERE owner = ?", (amount, dst))
    if crash:
        raise Crash()
    db.execute("UPDATE wallet SET gold = gold - ? WHERE owner = ?", (amount, src))
    return "ok"


def transfer_gold(db, op_id, src, dst, amount, crash=False):
    """Atomic and idempotent. Returns "ok", "insufficient", or the first
    result followed by " (replayed)" when op_id has been seen before.
    If crash is True, raise Crash after the first write, leaving no trace."""
    # TODO 1: one transaction. Record op_id in applied_op first (a duplicate
    # means replay the stored result). Refuse overdrafts (the CHECK constraint
    # raises sqlite3.IntegrityError; roll back and record "insufficient").
    # Simulate the crash between the two wallet updates and roll back.
    raise NotImplementedError("TODO 1")


def move_item(db, op_id, item_id, from_owner, to_owner):
    """Move one unique item. Returns "ok", "not owner", or a replayed result."""
    # TODO 2: one transaction; op_id recorded as in transfer_gold; the move is
    # a conditional UPDATE that only succeeds if from_owner still owns it.
    raise NotImplementedError("TODO 2")


def audit(db):
    """Returns {"gold_drift": actual - (minted - destroyed), "items": count}."""
    # TODO 3: sum every container that holds gold (here only wallets) and
    # compare with the ledger. Count item rows.
    raise NotImplementedError("TODO 3")


def stress(transfer, ops=10_000, crash_rate=0.01, lost_reply_rate=0.02, seed=7):
    """Random gold transfers with crashes and client retries. Provided.
    A crash makes the client retry with the SAME op_id. A lost reply after
    success also makes the client retry with the same op_id."""
    rng = random.Random(seed)
    db = open_world()
    players = ["ayla", "bren", "cato", "dara"]
    for n in range(ops):
        src, dst = rng.sample(players, 2)
        amount = rng.randint(1, 50)
        op_id = f"op-{n}"
        try:
            transfer(db, op_id, src, dst, amount, crash=rng.random() < crash_rate)
        except Crash:
            if db.in_transaction:
                db.execute("ROLLBACK")
            transfer(db, op_id, src, dst, amount)          # retry after the crash
            continue
        if rng.random() < lost_reply_rate:
            transfer(db, op_id, src, dst, amount)          # retry after a lost reply
    return db


if __name__ == "__main__":
    try:
        for name, fn in [("buggy", transfer_gold_buggy), ("yours", transfer_gold)]:
            print(f"{name:6}", audit(stress(fn)))
    except NotImplementedError as e:
        print(f"not run yet: {e} is still a stub. Fill in the TODOs, then run the tests.")
