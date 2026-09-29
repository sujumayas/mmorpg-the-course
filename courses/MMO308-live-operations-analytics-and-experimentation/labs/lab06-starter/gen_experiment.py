"""MMO308 Lab 06: a 14-day experiment log, one row per day.

Run:  python gen_experiment.py     (writes experiment_daily.csv)

The test: a new crafting-station screen (B) against the old one (A), 50/50 by
hashed account id. Primary metric: crafted an item within 3 days of first
exposure. Each row gives that day's newly exposed players per arm and how many
of them converted. (What else is going on in this data is for you to find.)
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 735
DAYS = 14
ARRIVALS = 3000        # newly assigned players per day, both arms together
RATE = 0.30            # true conversion, the same in both arms
CRASH = 0.043          # B only: chance the client crashes before exposure is logged,
                       # for players who were not going to convert anyway


def main(seed=SEED, write=True):
    rng = random.Random(seed)
    rows = []
    for day in range(1, DAYS + 1):
        na = nb = ka = kb = 0
        for _ in range(ARRIVALS):
            if rng.random() < 0.5:
                na += 1
                ka += rng.random() < RATE
            else:
                converts = rng.random() < RATE
                crashed = (not converts) and rng.random() < CRASH
                if crashed:
                    continue                # never logged: missing from B
                nb += 1
                kb += converts
        rows.append((day, na, ka, nb, kb))
    if write:
        with open(HERE / "experiment_daily.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(("day", "n_a", "conv_a", "n_b", "conv_b"))
            w.writerows(rows)
        print(f"{DAYS} days written")
    return rows


if __name__ == "__main__":
    main()
