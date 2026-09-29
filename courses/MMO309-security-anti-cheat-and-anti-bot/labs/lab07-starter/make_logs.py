"""Generate the synthetic telemetry for MMO309 Lab 07.

Run:  python make_logs.py
Writes intervals.csv, hours.csv and labels.csv next to this file.
Everything is synthetic and seeded, so every student gets the same data.
No real game or player data is involved.
"""
import csv
import math
import random
from pathlib import Path

SEED = 309
DAYS = 7
GCD = 1500           # ms, global cooldown for rotation-style play
N_GAPS = 200         # action intervals sampled per account
HERE = Path(__file__).resolve().parent

# Activity modes: [kills, loots, moves, chats, trades, crafts] per hour
MODES = {
    "combat":   [55, 50, 110, 3, 0, 0],
    "social":   [2, 1, 25, 45, 2, 0],
    "crafting": [0, 0, 15, 4, 3, 40],
    "trading":  [0, 0, 20, 10, 25, 2],
    "questing": [25, 20, 160, 5, 1, 1],
}

# (label, kind, count)
POPULATION = [
    ("human", "casual", 60),
    ("human", "rotation", 30),
    ("human", "grinder", 26),
    ("human", "fisher", 4),
    ("bot", "naive", 8),
    ("bot", "rotation_bot", 7),
    ("bot", "mimic", 8),
    ("bot", "part_time_mimic", 7),
]


def lognormal(rng, median, shape):
    return median * math.exp(rng.gauss(0, shape))


def gaps_for(rng, kind):
    """Return (gap_ms, cooldown_ms) pairs for one account."""
    out = []
    for _ in range(N_GAPS):
        if kind == "casual":
            out.append((lognormal(rng, 900, 0.6), 0))
        elif kind == "rotation":
            out.append((GCD + lognormal(rng, 150, 0.7), GCD))
        elif kind == "grinder":
            out.append((lognormal(rng, 700, 0.5), 0))
        elif kind == "naive":
            out.append((1000 + rng.uniform(-100, 100), 0))
        elif kind == "rotation_bot":
            out.append((GCD + 60 + rng.uniform(-20, 20), GCD))
        else:  # fisher, mimic and part_time_mimic use casual human timing
            out.append((lognormal(rng, 900, 0.6), 0))
    return out


def hours_per_day(rng, kind):
    if kind in ("naive", "rotation_bot", "mimic"):
        return rng.randint(20, 23)
    if kind == "part_time_mimic":
        return rng.randint(7, 10)
    if kind == "fisher":
        return rng.randint(2, 5)
    if kind == "grinder":
        return rng.randint(9, 14)
    return rng.randint(1, 5)


def vector_for(rng, kind):
    """One hour of activity counts."""
    if kind in ("naive", "rotation_bot", "mimic", "part_time_mimic"):
        base = MODES["combat"]
        return [max(0, round(v * rng.uniform(0.95, 1.05))) for v in base]
    if kind == "fisher":
        # one repetitive activity: loot from a fishing spot, a little chat
        return [0, round(40 * rng.uniform(0.85, 1.15)), round(rng.uniform(2, 8)),
                round(rng.uniform(0, 6)), 0, 0]
    if kind == "grinder":
        mode = "combat" if rng.random() < 0.6 else rng.choice(list(MODES))
    else:
        mode = rng.choice(list(MODES))
    base = MODES[mode]
    return [max(0, round(v * rng.uniform(0.4, 1.6) + rng.uniform(0, 4))) for v in base]


def main():
    rng = random.Random(SEED)
    accounts = []
    for label, kind, count in POPULATION:
        accounts += [(label, kind)] * count
    rng.shuffle(accounts)

    with open(HERE / "intervals.csv", "w", newline="") as fi, \
         open(HERE / "hours.csv", "w", newline="") as fh, \
         open(HERE / "labels.csv", "w", newline="") as fl:
        wi, wh, wl = csv.writer(fi), csv.writer(fh), csv.writer(fl)
        wi.writerow(["account_id", "gap_ms", "cooldown_ms"])
        wh.writerow(["account_id", "day", "hour", "kills", "loots", "moves",
                     "chats", "trades", "crafts"])
        wl.writerow(["account_id", "label", "kind"])
        for i, (label, kind) in enumerate(accounts):
            acc = f"A{i:03d}"
            wl.writerow([acc, label, kind])
            for gap, cd in gaps_for(rng, kind):
                wi.writerow([acc, round(gap, 1), cd])
            for day in range(DAYS):
                n = hours_per_day(rng, kind)
                start = rng.randint(0, 24 - n) if n < 24 else 0
                for hour in range(start, start + n):
                    wh.writerow([acc, day, hour] + vector_for(rng, kind))
    print(f"wrote {len(accounts)} accounts to intervals.csv, hours.csv, labels.csv")


if __name__ == "__main__":
    main()
