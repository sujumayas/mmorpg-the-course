"""DB201 Lab 11: a three-stage telemetry pipeline in SQLite.

    events.ndjson  --load-->  raw_events  --rollup-->  daily_zone_deaths  --query-->  answers

Run:  python make_events.py      # once, writes events.ndjson
      python pipeline.py         # loads, rolls up, runs and times the queries
      python check_lab11.py      # compares your telemetry.db with the expected answers

Search for "TODO". There are four. The starter runs as-is, but gives wrong answers
until you fix TODO 1 and write TODO 2.

PostgreSQL notes are marked "PG:". The lab uses SQLite so it runs anywhere.
"""
import json
import sqlite3
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "telemetry.db"
LANDING = HERE / "events.ndjson"

RAW_SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_events (
    event_id    TEXT NOT NULL,      -- TODO 1: this column should make retries harmless
    event_name  TEXT NOT NULL,
    event_time  TEXT NOT NULL,      -- client clock, ISO 8601 UTC
    received_at TEXT NOT NULL,      -- collector clock, ISO 8601 UTC
    event_day   TEXT NOT NULL,      -- first 10 chars of event_time: the day the event HAPPENED
    player_id   INTEGER NOT NULL,
    session_id  TEXT NOT NULL,
    build_id    INTEGER NOT NULL,
    properties  TEXT NOT NULL       -- JSON. PG: use jsonb and the ->> operator
);
"""
# PG: CREATE TABLE raw_events (...) PARTITION BY RANGE (event_time);
#     with one partition per day, and a BRIN index on received_at.


def load(con, path=LANDING, batch_size=5000):
    """Stage 1: copy the landing file into raw_events. Returns (lines read, rows in table)."""
    con.executescript(RAW_SCHEMA)
    sql = """INSERT INTO raw_events
             (event_id, event_name, event_time, received_at, event_day,
              player_id, session_id, build_id, properties)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    # TODO 1 (continued): change the INSERT so a second copy of the same event_id is skipped.
    # SQLite: INSERT OR IGNORE, or INSERT ... ON CONFLICT (event_id) DO NOTHING.
    # PG:     INSERT ... ON CONFLICT (event_id) DO NOTHING (needs a unique constraint).
    lines = 0
    buf = []
    with open(path) as f:
        for line in f:
            e = json.loads(line)
            lines += 1
            buf.append((e["event_id"], e["event_name"], e["event_time"], e["received_at"],
                        e["event_time"][:10], e["player_id"], e["session_id"], e["build_id"],
                        json.dumps(e["properties"], separators=(",", ":"))))
            if len(buf) >= batch_size:
                con.executemany(sql, buf)
                buf.clear()
    if buf:
        con.executemany(sql, buf)
    con.commit()
    rows = con.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0]
    return lines, rows


def build_rollup(con):
    """Stage 2: one row per (event_day, zone_id) with the number of deaths.

    TODO 2: replace the body with SQL that creates daily_zone_deaths(event_day, zone_id, deaths)
    from raw_events where event_name = 'player_died'. The zone is inside the JSON:
    json_extract(properties, '$.zone_id')   (PG: (properties->>'zone_id')::int)
    Make it safe to run twice: drop and recreate, or delete and reinsert.
    """
    con.executescript("""
        DROP TABLE IF EXISTS daily_zone_deaths;
        CREATE TABLE daily_zone_deaths (event_day TEXT, zone_id INTEGER, deaths INTEGER,
                                        PRIMARY KEY (event_day, zone_id));
    """)
    con.commit()


RAW_QUERY = """
SELECT COUNT(*) FROM raw_events
WHERE event_name = 'player_died'
  AND event_day = ?
  AND json_extract(properties, '$.zone_id') = ?
"""
ROLLUP_QUERY = "SELECT COALESCE(SUM(deaths), 0) FROM daily_zone_deaths WHERE event_day = ? AND zone_id = ?"


def timed(con, sql, params, repeat=5):
    """Run a query `repeat` times; return (answer, best time in milliseconds)."""
    best = float("inf")
    ans = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        ans = con.execute(sql, params).fetchone()[0]
        best = min(best, time.perf_counter() - t0)
    return ans, best * 1000


def main():
    if not LANDING.exists():
        raise SystemExit("events.ndjson not found. Run: python make_events.py")
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)

    t0 = time.perf_counter()
    lines, rows = load(con)
    print(f"load: {lines:,} lines -> {rows:,} rows in {time.perf_counter() - t0:.1f} s "
          f"({lines - rows:,} duplicates skipped)")

    t0 = time.perf_counter()
    build_rollup(con)
    n = con.execute("SELECT COUNT(*) FROM daily_zone_deaths").fetchone()[0]
    print(f"rollup: {n} rows in {time.perf_counter() - t0:.2f} s")

    params = ("2026-03-05", 7)
    a1, ms1 = timed(con, RAW_QUERY, params)
    a2, ms2 = timed(con, ROLLUP_QUERY, params)
    print(f"deaths in zone 7 on 2026-03-05: raw scan {a1} in {ms1:.2f} ms, rollup {a2} in {ms2:.3f} ms")
    print("plan (raw):   ", [r[-1] for r in con.execute("EXPLAIN QUERY PLAN " + RAW_QUERY, params)])
    print("plan (rollup):", [r[-1] for r in con.execute("EXPLAIN QUERY PLAN " + ROLLUP_QUERY, params)])

    # TODO 3: add an index that lets RAW_QUERY skip most of the table, for example on
    # (event_name, event_day). Re-run and record rows touched (EXPLAIN QUERY PLAN) and time.
    # PG: EXPLAIN (ANALYZE, BUFFERS) shows rows and pages actually read.

    # TODO 4: late arrivals. Count events whose received_at day is later than event_day.
    # Then answer in your report: if the rollup for 2026-03-05 was built at 00:05 on 03-06,
    # how many deaths for that day was it missing? (Hint: compare received_at with that time.)

    con.close()


if __name__ == "__main__":
    main()
