"""Writes events.csv and survey.csv, the invented data for MMO405 lab 03.
Run: python make_log.py   (already run once; both CSVs ship with the starter)

events.csv  account_id, minute (minutes since Monday 00:00 of the study week), type
            type is login, activity or logout.
survey.csv  account_id, reported_hours (the player's answer to "how many hours did you
            play this week?"), satisfaction (1-7).
Values are drawn once with a fixed seed and stored, so the CSVs, not this script, are the
lab's data. Three accounts are bots.
"""
import csv
import random

WEEK = 7 * 24 * 60


def one_session(rng, start):
    """Events for one sitting: login, bursts of activity with idle gaps, logout."""
    ev = [(start, "login")]
    t = start + rng.randint(0, 5)
    for _ in range(rng.randint(1, 4)):                 # activity bursts
        end = t + rng.randint(15, 70)
        while t <= end:
            ev.append((t, "activity"))
            t += rng.randint(1, 4)
        t += rng.choice([rng.randint(5, 12), rng.randint(12, 40)])   # idle gap
    ev.append((t + rng.randint(0, 45), "logout"))
    return ev


def build(seed=4053, players=300, bots=3):
    rng = random.Random(seed)
    events, survey = [], []
    for i in range(1, players + 1):
        acc = f"C{i:04d}"
        mine = []
        for _ in range(rng.choice([0, 1, 2, 3, 4, 5, 6, 8, 10])):
            start = rng.randint(0, WEEK - 400)
            if all(abs(start - s) > 400 for s, _ in mine if _ == "login"):
                mine += one_session(rng, start)
        events += [(acc, m, k) for m, k in mine]
        active = sum(1 for _, k in mine if k == "activity") * 2.5 / 60   # rough true hours
        said = max(0.0, active * rng.uniform(0.6, 1.8) + rng.gauss(2.0, 9.0))
        sat = round(4 + 0.6 * (active - 6) / 5 + rng.gauss(0, 1.3))
        survey.append((acc, round(said * 2) / 2, min(7, max(1, sat))))
    for j in range(1, bots + 1):
        acc = f"B{j:04d}"
        for day in range(7):
            t = day * 1440 + rng.randint(0, 120)
            events.append((acc, t, "login"))
            end = t + 20 * 60
            while t <= end:
                events.append((acc, t, "activity"))
                t += 5
            events.append((acc, t, "logout"))
    rng.shuffle(events)                                  # logs arrive out of order
    return events, survey


if __name__ == "__main__":
    events, survey = build()
    with open("events.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "minute", "type"])
        w.writerows(events)
    with open("survey.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "reported_hours", "satisfaction"])
        w.writerows(survey)
    print(f"wrote events.csv ({len(events)} rows) and survey.csv ({len(survey)} rows)")
