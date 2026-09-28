"""DB201 Lab 13 starter: retention windows, erasure requests, and deleted bytes that stay on disk.

Run from this folder:
    python privacy_lab.py                 # build both stores, run every part, print the tables
    python privacy_lab.py --players 1000  # smaller world for slow laptops
    python privacy_lab.py --check         # correctness tests for your TODO functions only

Python 3.10+, standard library only. Databases are rebuilt in a temp folder each run.
You edit the functions marked TODO (Parts C, D and E of lab13.md).

The telemetry store keeps one table per day (events_d000, events_d001, ...). That is how you
fake PostgreSQL's declarative partitioning in SQLite: dropping a day is DROP TABLE, not DELETE.
"""
import argparse
import os
import random
import secrets
import sqlite3
import tempfile
import time

EVENT_TYPES = ["login", "logout", "quest_accept", "quest_done", "kill", "loot",
               "craft", "trade", "chat", "death", "level_up", "shop_buy"]

ACCOUNT_SCHEMA = """
CREATE TABLE accounts (
  player_id    INTEGER PRIMARY KEY,
  email        TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  country      TEXT NOT NULL
);
"""

# The pseudonymous store adds one mapping table. Events never see player_id or email.
PSEUDO_SCHEMA = """
CREATE TABLE pseudonyms (
  player_id    INTEGER PRIMARY KEY REFERENCES accounts(player_id),
  telemetry_id TEXT NOT NULL UNIQUE      -- random, not derived from player_id
);
"""


def day_table(d):
    return f"events_d{d:03d}"


def build(path, mode, n_players, n_days, events_per_day, active_share, seed=13):
    """Build one store. mode is 'naive' (events carry player_id and display_name)
    or 'pseudo' (events carry only a random telemetry_id)."""
    rng = random.Random(seed)
    con = sqlite3.connect(path)
    con.executescript(ACCOUNT_SCHEMA)
    if mode == "pseudo":
        con.executescript(PSEUDO_SCHEMA)
    names = []
    for p in range(1, n_players + 1):
        name = f"Hero{p:05d}"
        names.append(name)
        con.execute("INSERT INTO accounts VALUES (?,?,?,?)",
                    (p, f"player{p:05d}@example.com", name, rng.choice(["DE", "FR", "ES", "PE", "US"])))
        if mode == "pseudo":
            # secrets.token_hex is fine for a lab. The point: nothing links it to player_id
            # except this one row.
            con.execute("INSERT INTO pseudonyms VALUES (?,?)", (p, secrets.token_hex(8)))
    tid = {}
    if mode == "pseudo":
        tid = dict(con.execute("SELECT player_id, telemetry_id FROM pseudonyms"))
    for d in range(n_days):
        t = day_table(d)
        if mode == "naive":
            con.execute(f"CREATE TABLE {t} (ts INTEGER, player_id INTEGER, display_name TEXT,"
                        f" type TEXT, value INTEGER)")
        else:
            con.execute(f"CREATE TABLE {t} (ts INTEGER, telemetry_id TEXT, type TEXT, value INTEGER)")
        rows = []
        for p in range(1, n_players + 1):
            if rng.random() > active_share:
                continue
            for _ in range(events_per_day):
                ts = d * 86400 + rng.randrange(86400)
                typ = rng.choice(EVENT_TYPES)
                val = rng.randrange(1000)
                if mode == "naive":
                    rows.append((ts, p, names[p - 1], typ, val))
                else:
                    rows.append((ts, tid[p], typ, val))
        q = "?,?,?,?,?" if mode == "naive" else "?,?,?,?"
        con.executemany(f"INSERT INTO {t} VALUES ({q})", rows)
    con.commit()
    return con


def day_tables(con):
    return [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'events_d%' ORDER BY name")]


def total_rows(con):
    return sum(con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in day_tables(con))


# ---------------------------------------------------------------------------
# Part B (given): two erasure strategies on the naive store
# ---------------------------------------------------------------------------

def erase_by_scan(con, player_id):
    """Strategy A. No index on player_id: every day table is scanned in full.
    Returns (rows_examined, rows_deleted)."""
    examined = deleted = 0
    for t in day_tables(con):
        examined += con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        deleted += con.execute(f"DELETE FROM {t} WHERE player_id = ?", (player_id,)).rowcount
    con.execute("DELETE FROM accounts WHERE player_id = ?", (player_id,))
    con.commit()
    return examined, deleted


def add_player_indexes(con):
    for t in day_tables(con):
        con.execute(f"CREATE INDEX IF NOT EXISTS ix_{t}_player ON {t}(player_id)")
    con.commit()


def erase_by_index(con, player_id):
    """Strategy B. With an index per day table, SQLite visits only the matching rows.
    Returns (rows_examined, rows_deleted); examined ~= deleted here."""
    deleted = 0
    for t in day_tables(con):
        deleted += con.execute(f"DELETE FROM {t} WHERE player_id = ?", (player_id,)).rowcount
    con.execute("DELETE FROM accounts WHERE player_id = ?", (player_id,))
    con.commit()
    return deleted, deleted


# ---------------------------------------------------------------------------
# Part C (TODO): erasure in the pseudonymous store
# ---------------------------------------------------------------------------

def erase_pseudonymous(con, player_id):
    """Strategy C. Erase the account and break the link from telemetry to the player.

    TODO:
      1. Delete the player's row from pseudonyms (this is the only link).
      2. Delete the player's row from accounts.
      3. Commit, and return (rows_examined, rows_deleted) counting only rows you touched.
    Do NOT touch any events_d table. Explain in your memo why that is (or is not) enough.
    """
    raise NotImplementedError("Part C")


# ---------------------------------------------------------------------------
# Part D (TODO): the retention job
# ---------------------------------------------------------------------------

def enforce_retention(con, today, keep_days):
    """Drop every day table older than keep_days, counting back from `today`.

    A table events_dNNN is expired when NNN <= today - keep_days.
    Use DROP TABLE, not DELETE. Return the list of dropped table names.

    TODO: implement. Hint: day_tables(con) and int(name[-3:]).
    """
    raise NotImplementedError("Part D")


# ---------------------------------------------------------------------------
# Part E (TODO): a subject access export (GDPR Article 15)
# ---------------------------------------------------------------------------

def export_subject(con, player_id):
    """Return a dict with everything this store holds about player_id:
        {"account": {...}, "event_count": int, "events_by_type": {type: count}}
    It must work on BOTH stores. In the pseudonymous store, look up the telemetry_id first.
    If the player was erased, return {"account": None, "event_count": 0, "events_by_type": {}}
    for the naive store. For the pseudonymous store after erasure you cannot find the events
    any more: that is the point. Return the same empty shape.

    TODO: implement.
    """
    raise NotImplementedError("Part E")


# ---------------------------------------------------------------------------
# Part F (given): do deleted bytes leave the file?
# ---------------------------------------------------------------------------

def bytes_on_disk(path, needle):
    with open(path, "rb") as f:
        return f.read().count(needle.encode())


def forensic_demo(tmp, n_players, n_days):
    path = os.path.join(tmp, "DB201_forensic.db")
    con = build(path, "naive", n_players, n_days, events_per_day=20, active_share=0.5)
    pid = 7
    email = f"player{pid:05d}@example.com"
    name = f"Hero{pid:05d}"
    print(f"\nPart F. Player {pid}: '{email}' and '{name}' in the file")
    print(f"  before erasure : email x{bytes_on_disk(path, email)}, name x{bytes_on_disk(path, name)}")
    erase_by_scan(con, pid)
    print(f"  after DELETE   : email x{bytes_on_disk(path, email)}, name x{bytes_on_disk(path, name)}")
    con.execute("VACUUM")
    con.close()
    print(f"  after VACUUM   : email x{bytes_on_disk(path, email)}, name x{bytes_on_disk(path, name)}")


# ---------------------------------------------------------------------------
# Tests and driver
# ---------------------------------------------------------------------------

def check(tmp):
    ok = True
    con = build(os.path.join(tmp, "DB201_chk_pseudo.db"), "pseudo", 50, 10, 5, 1.0)
    before = total_rows(con)
    try:
        ex, de = erase_pseudonymous(con, 3)
        linked = con.execute("SELECT COUNT(*) FROM pseudonyms WHERE player_id=3").fetchone()[0]
        acct = con.execute("SELECT COUNT(*) FROM accounts WHERE player_id=3").fetchone()[0]
        assert linked == 0 and acct == 0, "mapping or account row still present"
        assert total_rows(con) == before, "Part C must not touch event tables"
        assert ex <= 4, f"examined {ex} rows; should be a handful"
        print("  Part C ok")
    except NotImplementedError:
        print("  Part C not done"); ok = False
    try:
        dropped = enforce_retention(con, today=9, keep_days=3)
        assert dropped == [day_table(d) for d in range(0, 7)], dropped
        assert day_tables(con) == [day_table(d) for d in range(7, 10)]
        print("  Part D ok")
    except NotImplementedError:
        print("  Part D not done"); ok = False
    try:
        naive = build(os.path.join(tmp, "DB201_chk_naive.db"), "naive", 50, 3, 5, 1.0)
        e = export_subject(naive, 4)
        assert e["account"]["email"] == "player00004@example.com"
        assert e["event_count"] == 15 and sum(e["events_by_type"].values()) == 15
        p = export_subject(con, 5)
        assert p["event_count"] == 15, p["event_count"]
        erased = export_subject(con, 3)
        assert erased == {"account": None, "event_count": 0, "events_by_type": {}}
        print("  Part E ok")
    except NotImplementedError:
        print("  Part E not done"); ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=int, default=2000)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--events", type=int, default=40, help="events per active player per day")
    ap.add_argument("--active", type=float, default=0.4, help="share of players active each day")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="DB201_lab13_") as tmp:
        print("Tests:")
        passed = check(tmp)
        if a.check:
            raise SystemExit(0 if passed else 1)

        print(f"\nBuilding stores: {a.players} players, {a.days} days, "
              f"{a.events} events/active player/day, {a.active:.0%} active per day")
        naive = build(os.path.join(tmp, "DB201_naive.db"), "naive", a.players, a.days, a.events, a.active)
        pseudo = build(os.path.join(tmp, "DB201_pseudo.db"), "pseudo", a.players, a.days, a.events, a.active)
        n = total_rows(naive)
        print(f"  rows per store: {n:,}  (model: players x active x events x days = "
              f"{a.players * a.active * a.events * a.days:,.0f})")
        for label, path in (("naive", "DB201_naive.db"), ("pseudo", "DB201_pseudo.db")):
            print(f"  {label:6s} file size: {os.path.getsize(os.path.join(tmp, path)) / 1e6:6.1f} MB")

        print("\nErasure of 5 players (Parts B and C)")
        print(f"  {'strategy':<22}{'rows examined':>16}{'rows deleted':>14}{'ms/request':>12}")
        victims = [11, 222, 333, 444, 555]
        t0 = time.perf_counter(); ex = de = 0
        for v in victims[:5]:
            e, d = erase_by_scan(naive, v); ex += e; de += d
        ms = (time.perf_counter() - t0) * 1000 / 5
        print(f"  {'A scan every day':<22}{ex // 5:>16,}{de // 5:>14,}{ms:>12.1f}")
        t0 = time.perf_counter(); add_player_indexes(naive)
        print(f"  (building the player_id indexes took {(time.perf_counter() - t0) * 1000:.0f} ms, "
              f"file now {os.path.getsize(os.path.join(tmp, 'DB201_naive.db')) / 1e6:.1f} MB)")
        t0 = time.perf_counter(); ex = de = 0
        for v in [12, 223, 334, 445, 556]:
            e, d = erase_by_index(naive, v); ex += e; de += d
        ms = (time.perf_counter() - t0) * 1000 / 5
        print(f"  {'B index on player_id':<22}{ex // 5:>16,}{de // 5:>14,}{ms:>12.1f}")
        try:
            t0 = time.perf_counter(); ex = de = 0
            for v in victims:
                e, d = erase_pseudonymous(pseudo, v); ex += e; de += d
            ms = (time.perf_counter() - t0) * 1000 / 5
            print(f"  {'C drop the pseudonym':<22}{ex // 5:>16,}{de // 5:>14,}{ms:>12.1f}")
        except NotImplementedError:
            print("  C drop the pseudonym   (Part C not done)")

        try:
            t0 = time.perf_counter()
            dropped = enforce_retention(pseudo, today=a.days - 1, keep_days=7)
            print(f"\nPart D. Retention 7 days: dropped {len(dropped)} tables in "
                  f"{(time.perf_counter() - t0) * 1000:.1f} ms, {total_rows(pseudo):,} rows remain")
        except NotImplementedError:
            print("\nPart D not done")

        forensic_demo(tmp, min(a.players, 500), 5)


if __name__ == "__main__":
    main()
