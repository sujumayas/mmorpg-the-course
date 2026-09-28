"""DB201 Lab 11 checker. Recomputes the expected answers from events.ndjson in plain
Python and compares them with telemetry.db.

Run:  python check_lab11.py
"""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def expected(path):
    seen = set()
    deaths = Counter()
    late = 0
    lines = 0
    for line in open(path):
        lines += 1
        e = json.loads(line)
        if e["event_id"] in seen:
            continue
        seen.add(e["event_id"])
        if e["received_at"][:10] > e["event_time"][:10]:
            late += 1
        if e["event_name"] == "player_died":
            deaths[(e["event_time"][:10], e["properties"]["zone_id"])] += 1
    return lines, len(seen), deaths, late


def main():
    db, landing = HERE / "telemetry.db", HERE / "events.ndjson"
    if not (db.exists() and landing.exists()):
        raise SystemExit("Run make_events.py and pipeline.py first.")
    lines, unique, deaths, late = expected(landing)
    con = sqlite3.connect(db)
    ok = True

    rows = con.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0]
    if rows == unique:
        print(f"PASS raw_events has {rows:,} rows ({lines - unique:,} duplicate lines skipped)")
    else:
        ok = False
        print(f"FAIL raw_events has {rows:,} rows, expected {unique:,}. "
              f"{rows - unique:,} extra rows are retried events (TODO 1).")

    got = {(d, z): n for d, z, n in con.execute("SELECT event_day, zone_id, deaths FROM daily_zone_deaths")}
    if got == dict(deaths):
        print(f"PASS daily_zone_deaths matches ({len(got)} rows)")
    else:
        ok = False
        wrong = sum(1 for k in set(got) | set(deaths) if got.get(k) != deaths.get(k))
        print(f"FAIL daily_zone_deaths: {wrong} of {len(deaths)} (day, zone) cells differ (TODO 2)")

    idx = [r[1] for r in con.execute("PRAGMA index_list('raw_events')")]
    print(("INFO " if idx else "TODO ") + f"indexes on raw_events: {idx or 'none yet (TODO 3)'}")
    print(f"INFO expected late-arriving events (after dedupe): {late:,}. Compare with your TODO 4 answer.")
    con.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
