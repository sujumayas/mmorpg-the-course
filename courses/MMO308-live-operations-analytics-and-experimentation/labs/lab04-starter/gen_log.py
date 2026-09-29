"""MMO308 Lab 04: generate a simulated story-progress and session log.

Run:  python gen_log.py      (writes players.csv, sessions.csv, chapters.csv)

The game launched on day 0. Players install between day 0 and day 119.
The log runs to day 179, so days 120-179 are "the future" you use to check
churn labels made on day 119. Seed 404: everyone gets the same files.
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 404
N_PLAYERS = 6000
LAST_DAY = 179
AS_OF = 119
CHAPTERS = 8
CADENCE = {"daily": 0.5, "regular": 0.3, "occasional": 0.1}   # daily return chance
MIX = [("daily", 0.40), ("regular", 0.35), ("occasional", 0.25)]
P_PROGRESS = [0.60, 0.40, 0.20, 0.40, 0.40, 0.40, 0.40, 0.40]  # per session, chapter k+1
H_QUIT = 0.03                                                    # per session


def pick(rng, mix):
    r = rng.random()
    for name, w in mix:
        if r < w:
            return name
        r -= w
    return mix[-1][0]


def main():
    rng = random.Random(SEED)
    players, sessions, chapters = [], [], []
    for pid in range(1, N_PLAYERS + 1):
        if rng.random() < 0.25:
            install = int(rng.random() * 7)            # launch week
        else:
            install = int(rng.random() * (AS_OF + 1))
        cadence = pick(rng, MIX)
        players.append((pid, install, cadence))
        a = CADENCE[cadence]
        done = 0
        for day in range(install, LAST_DAY + 1):
            if day > install and rng.random() >= a:
                continue
            sessions.append((pid, day))
            if done < CHAPTERS and rng.random() < P_PROGRESS[done]:
                done += 1
                chapters.append((pid, done, day))
            if rng.random() < H_QUIT:
                break
    for name, header, rows in (("players.csv", ("player_id", "install_day", "cadence"), players),
                               ("sessions.csv", ("player_id", "day"), sessions),
                               ("chapters.csv", ("player_id", "chapter", "day"), chapters)):
        with open(HERE / name, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
    print(f"{len(players)} players, {len(sessions)} sessions, {len(chapters)} chapter completions")


if __name__ == "__main__":
    main()
