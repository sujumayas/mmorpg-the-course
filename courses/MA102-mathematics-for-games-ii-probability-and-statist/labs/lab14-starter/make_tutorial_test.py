"""Instructor script: regenerates tutorial_test.csv (seed 14).

4,800 new players, random 50/50 assignment. True completion rates:
A 40%, B 44% overall; mobile players complete about 6 points less often.
day1_return depends on completion. Change the constants to make a new cohort.
"""
import csv

from mulberry32 import Mulberry32

rng = Mulberry32(14)
BASE = {"A": 0.40, "B": 0.44}
with open("tutorial_test.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["player_id", "group", "completed_tutorial", "day1_return", "sessions_day1", "platform"])
    for i in range(4800):
        group = "A" if rng.random() < 0.5 else "B"
        platform = "mobile" if rng.random() < 0.55 else "pc"
        p = BASE[group] + (-0.03 if platform == "mobile" else 0.037)
        done = rng.bernoulli(p)
        back = rng.bernoulli(0.45 if done else 0.25)
        sessions = 0
        if back or rng.random() < 0.8:
            sessions = 1
            while rng.random() < (0.55 if done else 0.35):
                sessions += 1
        w.writerow([f"u{i + 1:05d}", group, done, back, sessions, platform])
