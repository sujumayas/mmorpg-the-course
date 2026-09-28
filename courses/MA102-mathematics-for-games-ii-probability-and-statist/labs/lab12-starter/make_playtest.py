"""Instructor script: regenerates playtest_w12.csv (seed 12).

    python make_playtest.py

40 testers of a fictional dungeon, 20 new and 20 returning. Synthetic data
with three planted features the lab asks students to find:
  - t18 idled 41 minutes mid-run (long clear time, high minutes_idle).
  - t29 got lost (long clear time, low minutes_idle, many deaths).
  - Ratings split into two groups. New players mostly rate 5 to 6,
    returning players mostly 3 to 4, with a few crossovers.
One rating is missing (t08 skipped the survey). Change SEED or the planted
rows to make a fresh dataset for a new offering.
"""
import csv

from mulberry32 import Mulberry32

SEED = 12
rng = Mulberry32(SEED)


def randint(lo, hi):
    return lo + int(rng.random() * (hi - lo + 1))


def skewed_minutes(center, spread):
    # Sum of three uniforms, shifted, then a small right tail.
    u = rng.random() + rng.random() + rng.random() - 1.5
    tail = spread * (rng.random() ** 4) * 2
    return round(center + spread * u + tail)


rows = []
for i in range(40):
    tid = f"t{i + 1:02d}"
    new = i % 2 == 0
    clear = skewed_minutes(24 if new else 20, 5)
    deaths = 0
    while rng.random() < (0.72 if new else 0.55):
        deaths += 1
    deaths = min(deaths, 8)
    idle = randint(0, 4)
    reached = "yes" if rng.random() < (0.80 if new else 0.95) else "no"
    beat = "yes" if reached == "yes" and rng.random() < (0.60 if new else 0.85) else "no"
    if new:
        rating = 6 if rng.random() < 0.45 else (5 if rng.random() < 0.8 else 4)
    else:
        rating = 3 if rng.random() < 0.45 else (4 if rng.random() < 0.8 else 5)
    rows.append([tid, "new" if new else "returning", clear, deaths, idle, reached, beat, rating])

# Planted rows.
rows[17][2:5] = [66, 3, 41]      # t18: idle outlier, a returning player who went AFK
rows[17][5:7] = ["yes", "yes"]  # t18 came back and finished
rows[28][2:5] = [57, 11, 1]      # t29: lost, a new player who kept dying and wandering
rows[28][5:8] = ["no", "no", 7]
rows[7][7] = ""                  # t08: skipped the rating question

with open("playtest_w12.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tester_id", "experience", "clear_minutes", "deaths", "minutes_idle",
                "reached_boss", "beat_boss", "difficulty_rating"])
    w.writerows(rows)
