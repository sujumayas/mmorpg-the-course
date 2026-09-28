"""DB201 Lab 12: compute live-game KPIs in SQL.

Run:  python gen_sessions.py     # once, writes accounts.csv and sessions.csv
      python kpis.py             # loads kpi.db, runs every query in QUERIES, writes out/*.csv
      python check_lab12.py      # compares your answers with a plain-Python reference

Fill in every query marked TODO. Each query must return exactly the columns named
in its comment, in that order. The first query is done for you as a pattern.

Useful SQLite date functions (all times in the data are UTC):
    date(start_utc)                               -> '2026-03-05'   the UTC calendar day
    date(start_utc, utc_offset_hours || ' hours') -> the player's local calendar day
    date('2026-03-05', '+7 days')                 -> '2026-03-12'
PG equivalents: (start_utc AT TIME ZONE 'UTC')::date, start_utc + make_interval(hours => off),
and install_day + 7.
"""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "kpi.db"
OUT = HERE / "out"
LAST_DAY = "2026-04-29"          # the last day in the data

QUERIES = {
    # (day, dau): accounts with at least one session starting on that UTC day.
    "dau_utc": """
        SELECT date(start_utc) AS day, COUNT(DISTINCT account_id) AS dau
        FROM sessions
        GROUP BY day ORDER BY day
    """,

    # TODO (day, dau): as dau_utc, but only sessions of 5 minutes or more count.
    "dau_5min": None,

    # TODO (day, dau): as dau_utc, but the day is the player's LOCAL calendar day.
    # Join accounts to get utc_offset_hours.
    "dau_local": None,

    # TODO (day, dau): as dau_utc, but count people (person_id), not accounts.
    "dau_person": None,

    # TODO (mau): one row. Distinct accounts with a session on any UTC day in the
    # 30 days ending LAST_DAY, inclusive (2026-03-31 to 2026-04-29).
    "mau_last30": None,

    # TODO (avg_dau, mau, stickiness): one row. avg_dau is the mean of the 30 daily
    # dau_utc values in the same window; stickiness = avg_dau / mau.
    "stickiness_last30": None,

    # TODO (install_day, cohort, d1, d7): one row per install day that has a full 7 days
    # of data after it. cohort = accounts installed that day. d1 = fraction of the cohort
    # with a session on install_day + 1 (UTC). d7 likewise for install_day + 7.
    "retention": None,
}


def load(con):
    con.executescript("""
        DROP TABLE IF EXISTS accounts; DROP TABLE IF EXISTS sessions;
        CREATE TABLE accounts (account_id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL,
                               install_day TEXT NOT NULL, utc_offset_hours INTEGER NOT NULL);
        CREATE TABLE sessions (account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                               start_utc TEXT NOT NULL, minutes INTEGER NOT NULL);
        CREATE INDEX ix_sessions_start ON sessions(start_utc);
    """)
    with open(HERE / "accounts.csv") as f:
        con.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                        [(int(r["account_id"]), int(r["person_id"]), r["install_day"],
                          int(r["utc_offset_hours"])) for r in csv.DictReader(f)])
    with open(HERE / "sessions.csv") as f:
        con.executemany("INSERT INTO sessions VALUES (?, ?, ?)",
                        [(int(r["account_id"]), r["start_utc"], int(r["minutes"]))
                         for r in csv.DictReader(f)])
    con.commit()


def run(con):
    """Run every query; return {name: (column names, rows)} for the ones written so far."""
    results = {}
    for name, sql in QUERIES.items():
        if sql is None:
            print(f"  {name:18} TODO")
            continue
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        results[name] = (cols, rows)
        preview = rows[0] if len(rows) == 1 else f"{len(rows)} rows, first {rows[0] if rows else None}"
        print(f"  {name:18} {preview}")
    return results


def main():
    if not (HERE / "sessions.csv").exists():
        raise SystemExit("sessions.csv not found. Run: python gen_sessions.py")
    con = sqlite3.connect(DB)
    load(con)
    results = run(con)
    OUT.mkdir(exist_ok=True)
    for name, (cols, rows) in results.items():
        with open(OUT / f"{name}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
    print(f"wrote {len(results)} CSV files to {OUT}")
    con.close()


if __name__ == "__main__":
    main()
