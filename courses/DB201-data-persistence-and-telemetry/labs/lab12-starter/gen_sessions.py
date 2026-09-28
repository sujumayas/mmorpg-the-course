"""DB201 Lab 12: generate accounts.csv and sessions.csv (deterministic, seed 1212).

Run:  python gen_sessions.py

accounts.csv  account_id, person_id, install_day (YYYY-MM-DD, UTC), utc_offset_hours
sessions.csv  account_id, start_utc (ISO 8601), minutes

60 days of play, 2026-03-01 to 2026-04-29 (UTC). About 3,000 accounts owned by about
2,850 people: some people run a second account (an "alt"). Play probability falls with
account age, the way real retention curves do. About one session in ten is shorter
than 5 minutes (a login to check mail, a crash, a queue that never popped).

Standard library only.
"""
import csv
import math
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
START = date(2026, 3, 1)
DAYS = 60
ACCOUNTS = 3000
OFFSETS = [-8, -7, -5, -4, -3, 0, 1, 2, 3, 8, 9]


def generate(seed=1212):
    rng = random.Random(seed)
    accounts = []
    person = 0
    for a in range(1, ACCOUNTS + 1):
        if a > 1 and rng.random() < 0.05:
            owner = accounts[-1][1]            # alt of the previous account's owner
            install = accounts[-1][2] + timedelta(days=rng.randint(0, 3))
            offset = accounts[-1][3]
        else:
            person += 1
            owner = person
            # more installs early (launch spike), then a steady trickle
            install = START + timedelta(days=min(DAYS - 1, int(rng.expovariate(1 / 12))))
            offset = rng.choice(OFFSETS)
        accounts.append((a, owner, install, offset))

    sessions = []
    for a, owner, install, offset in accounts:
        engagement = rng.choice([0.35, 0.6, 0.9])        # casual, regular, devoted
        for d in range((START + timedelta(days=DAYS) - install).days):
            day = install + timedelta(days=d)
            p = 1.0 if d == 0 else engagement * (0.25 + 0.75 * math.exp(-d / 10))
            if rng.random() > p:
                continue
            for _ in range(1 if rng.random() < 0.8 else 2):
                local_hour = rng.choice([7, 12, 17, 18, 19, 20, 21, 22, 23])
                local = datetime(day.year, day.month, day.day, local_hour, rng.randint(0, 59))
                start = (local - timedelta(hours=offset)).replace(tzinfo=timezone.utc)
                minutes = rng.randint(1, 4) if rng.random() < 0.1 else int(rng.lognormvariate(3.7, 0.6))
                if start.date() < START + timedelta(days=DAYS):
                    sessions.append((a, start.strftime("%Y-%m-%dT%H:%M:%SZ"), max(1, minutes)))
    sessions.sort(key=lambda s: s[1])
    return accounts, sessions


def main():
    accounts, sessions = generate()
    with open(HERE / "accounts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "person_id", "install_day", "utc_offset_hours"])
        for a, p, d, o in accounts:
            w.writerow([a, p, d.isoformat(), o])
    with open(HERE / "sessions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "start_utc", "minutes"])
        w.writerows(sessions)
    print(f"wrote {len(accounts):,} accounts ({len({a[1] for a in accounts}):,} people) "
          f"and {len(sessions):,} sessions")


if __name__ == "__main__":
    main()
