"""Writes owners.csv: season play time (hours) of 5,000 battle pass owners.

    python gen_owners.py

Seed 405. Play time is lognormal with median 38 hours and log-spread 0.75,
plus a small group of 150 owners who stop playing in the first week
(0.5 to 3 hours). Do not edit; the checker expects this exact file.
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    rng = random.Random(405)
    rows = []
    for i in range(4850):
        rows.append((i, round(rng.lognormvariate(math.log(38), 0.75), 2)))
    for i in range(4850, 5000):
        rows.append((i, round(rng.uniform(0.5, 3.0), 2)))
    rng.shuffle(rows)
    with open(HERE / "owners.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["owner_id", "season_hours"])
        w.writerows(rows)
    print(f"wrote {len(rows)} owners to owners.csv")


if __name__ == "__main__":
    main()
