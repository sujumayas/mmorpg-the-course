"""MMO309 Lab 04: the mailbox under fire.

A tiny mail system. Players send gold as a mail attachment; the recipient collects it later.
The two handlers below are written the naive way. Your job:

  1. Run check_lab04.py and read which failure points break (steps 1-2 of the lab).
  2. Rewrite send_mail and collect_mail so that every failure point is safe:
     one transaction, a conditional update that cannot go negative, and an idempotency key
     stored in the `done` table in the same transaction.
  3. Implement audit(db).

Rules for the rewrite:
  - Keep calling crash_point(crash_at, 1), (crash_at, 2) and (crash_at, 3) in that order:
    1 after the first check, 2 after the first write, 3 after the work is committed and
    before the reply is returned. The checker uses them to inject failures.
  - Do not catch Crash. The checker simulates the process dying: it rolls back any open
    transaction and retries your handler once with the same request id.
"""
import sqlite3


class Crash(Exception):
    """The server process dies here. Only committed writes survive."""


def crash_point(crash_at, k):
    if crash_at == k:
        raise Crash(f"injected failure at point {k}")


def new_world():
    db = sqlite3.connect(":memory:", isolation_level=None)  # autocommit unless you BEGIN
    db.executescript("""
        CREATE TABLE players (name TEXT PRIMARY KEY, gold INTEGER NOT NULL);
        CREATE TABLE mail (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, recipient TEXT,
                           gold INTEGER NOT NULL, collected INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, amount INTEGER);
        CREATE TABLE done (req_id TEXT PRIMARY KEY, reply TEXT);
        INSERT INTO players VALUES ('ana', 500), ('bo', 0), ('cy', 0);
        INSERT INTO ledger (kind, amount) VALUES ('grant', 500);
    """)
    return db


def gold(db, name):
    return db.execute("SELECT gold FROM players WHERE name=?", (name,)).fetchone()[0]


# ---------------------------------------------------------------- naive handlers

def send_mail(db, req_id, sender, recipient, amount, crash_at=0):
    """Attach `amount` gold from sender to a new mail for recipient.
    Returns "sent" or "refused"."""
    balance = gold(db, sender)
    if balance < amount:
        return "refused"
    crash_point(crash_at, 1)
    db.execute("INSERT INTO mail (sender, recipient, gold) VALUES (?, ?, ?)",
               (sender, recipient, amount))
    crash_point(crash_at, 2)
    db.execute("UPDATE players SET gold=? WHERE name=?", (balance - amount, sender))
    crash_point(crash_at, 3)
    return "sent"


def collect_mail(db, req_id, recipient, mail_id, crash_at=0):
    """Move a mail's gold into the recipient's purse. Returns "collected" or "nothing"."""
    row = db.execute("SELECT gold, collected FROM mail WHERE id=? AND recipient=?",
                     (mail_id, recipient)).fetchone()
    if row is None or row[1]:
        return "nothing"
    crash_point(crash_at, 1)
    db.execute("UPDATE players SET gold = gold + ? WHERE name=?", (row[0], recipient))
    crash_point(crash_at, 2)
    db.execute("UPDATE mail SET collected=1 WHERE id=?", (mail_id,))
    crash_point(crash_at, 3)
    return "collected"


# ---------------------------------------------------------------- audit

def audit(db):
    """Conservation check. Return a dict with three integers:
      "held":     gold in all purses plus gold in uncollected mail
      "created":  total of all 'grant' rows in the ledger (the only faucet in this lab)
      "residual": held - created  (0 when no gold was created or destroyed off the books)
    """
    raise NotImplementedError("step 5: implement audit(db)")
