"""Checker for MMO309 Lab 04. Run:  python check_lab04.py

Every test injects a failure at each point (0 = no failure, 1, 2, 3), simulates the
process dying (open transactions roll back), retries once with the same request id,
and then checks conservation and exactly-once behaviour.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mailbox as M  # noqa: E402

failures = 0
total = 0


def check(name, fn):
    global failures, total
    total += 1
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not implemented yet ({exc})"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures += 1


def with_retry(db, handler, crash_at, *args):
    try:
        return handler(db, *args, crash_at=crash_at)
    except M.Crash:
        if db.in_transaction:
            db.execute("ROLLBACK")      # the process died: uncommitted work is gone
        return handler(db, *args, crash_at=0)


def mails(db):
    return db.execute("SELECT sender, recipient, gold, collected FROM mail ORDER BY id").fetchall()


def held(db):
    purses = db.execute("SELECT SUM(gold) FROM players").fetchone()[0]
    unclaimed = db.execute("SELECT COALESCE(SUM(gold), 0) FROM mail WHERE collected=0").fetchone()[0]
    return purses + unclaimed


def t_send(k):
    def run():
        db = M.new_world()
        reply = with_retry(db, M.send_mail, k, "req-1", "ana", "bo", 100)
        state = f"reply={reply} ana={M.gold(db, 'ana')} mails={mails(db)} held={held(db)}"
        ok = (reply == "sent" and M.gold(db, "ana") == 400
              and mails(db) == [("ana", "bo", 100, 0)] and held(db) == 500)
        return ok, state
    return run


def t_collect(k):
    def run():
        db = M.new_world()
        M.send_mail(db, "req-1", "ana", "bo", 100)
        reply = with_retry(db, M.collect_mail, k, "req-2", "bo", 1)
        state = f"reply={reply} bo={M.gold(db, 'bo')} mails={mails(db)} held={held(db)}"
        ok = (reply == "collected" and M.gold(db, "bo") == 100
              and mails(db) == [("ana", "bo", 100, 1)] and held(db) == 500)
        return ok, state
    return run


def t_replay():
    db = M.new_world()
    first = M.send_mail(db, "req-1", "ana", "bo", 100)
    again = M.send_mail(db, "req-1", "ana", "bo", 100)
    ok = first == again == "sent" and M.gold(db, "ana") == 400 and len(mails(db)) == 1
    return ok, f"replies={first},{again} ana={M.gold(db, 'ana')} mails={len(mails(db))}"


def t_new_request():
    db = M.new_world()
    M.send_mail(db, "req-1", "ana", "bo", 100)
    M.send_mail(db, "req-2", "ana", "bo", 100)
    ok = M.gold(db, "ana") == 300 and len(mails(db)) == 2
    return ok, f"ana={M.gold(db, 'ana')} mails={len(mails(db))}"


def t_overdraft():
    db = M.new_world()
    reply = M.send_mail(db, "req-1", "ana", "bo", 600)
    ok = reply == "refused" and M.gold(db, "ana") == 500 and mails(db) == []
    return ok, f"reply={reply} ana={M.gold(db, 'ana')} mails={len(mails(db))}"


def t_double_collect():
    db = M.new_world()
    M.send_mail(db, "req-1", "ana", "bo", 100)
    first = M.collect_mail(db, "req-2", "bo", 1)
    second = M.collect_mail(db, "req-3", "bo", 1)
    ok = first == "collected" and second == "nothing" and M.gold(db, "bo") == 100
    return ok, f"replies={first},{second} bo={M.gold(db, 'bo')}"


def t_wrong_recipient():
    db = M.new_world()
    M.send_mail(db, "req-1", "ana", "bo", 100)
    reply = M.collect_mail(db, "req-2", "cy", 1)
    ok = reply == "nothing" and M.gold(db, "cy") == 0
    return ok, f"reply={reply} cy={M.gold(db, 'cy')}"


def t_audit_clean():
    db = M.new_world()
    M.send_mail(db, "req-1", "ana", "bo", 100)          # 100 sits in uncollected mail
    a = M.audit(db)
    return a == {"held": 500, "created": 500, "residual": 0}, f"audit={a}"


def t_audit_catches():
    db = M.new_world()
    db.execute("UPDATE players SET gold = gold + 250 WHERE name='cy'")   # an off-the-books dupe
    a = M.audit(db)
    return a == {"held": 750, "created": 500, "residual": 250}, f"audit={a}"


if __name__ == "__main__":
    for k in (0, 1, 2, 3):
        check(f"send survives failure at point {k}", t_send(k))
    for k in (0, 1, 2, 3):
        check(f"collect survives failure at point {k}", t_collect(k))
    check("replayed request changes nothing", t_replay)
    check("a new request id is a new send", t_new_request)
    check("overdraft is refused", t_overdraft)
    check("a mail is collected once", t_double_collect)
    check("only the recipient can collect", t_wrong_recipient)
    check("audit balances with gold in the mail", t_audit_clean)
    check("audit finds 250 gold created off the books", t_audit_catches)
    print(f"\n{total - failures} of {total} checks pass.")
    sys.exit(1 if failures else 0)
