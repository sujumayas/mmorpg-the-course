"""Generate the validation scores for MMO309 Lab 08.

Run:  python make_scores.py
Writes scores.csv: one row per account with a detector score in [0, 1] and the
reviewed label (1 = bot, 0 = human). Synthetic and seeded; no real game data.
"""
import csv
import math
import random
from pathlib import Path

SEED = 3098
N = 20_000
PREVALENCE = 0.03
HERE = Path(__file__).resolve().parent


def main():
    rng = random.Random(SEED)
    rows = []
    for i in range(N):
        is_bot = rng.random() < PREVALENCE
        z = rng.gauss(2.8, 1.1) if is_bot else rng.gauss(0.0, 1.0)
        score = 1 / (1 + math.exp(-(z - 3.0)))
        rows.append((f"V{i:05d}", round(score, 4), int(is_bot)))
    with open(HERE / "scores.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "score", "label"])
        w.writerows(rows)
    print(f"wrote {N} rows to scores.csv, {sum(r[2] for r in rows)} bots")


if __name__ == "__main__":
    main()
