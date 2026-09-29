"""MMO405 Lab 04: writes survey.csv, synthetic answers from 400 players to a
10-item guild scale on a 1-7 agreement scale. Seed 404. Standard library only.

Run:  python gen_survey.py
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 400
SEED = 404
# Items g1-g5 are driven by one hidden trait, g6-g10 by another.
# Some items are worded in reverse (agreeing means less of the trait).
REVERSED = {4, 9}


def clamp(x):
    return max(1, min(7, int(round(x))))


def main():
    rng = random.Random(SEED)
    rows = []
    for pid in range(1, N + 1):
        a = rng.gauss(0, 1)
        b = 0.15 * a + (1 - 0.15 ** 2) ** 0.5 * rng.gauss(0, 1)
        answers = []
        for i in range(1, 11):
            trait = a if i <= 5 else b
            x = 4 + 1.2 * trait + 1.0 * rng.gauss(0, 1)
            if i in REVERSED:
                x = 8 - x
            answers.append(clamp(x))
        rows.append([pid] + answers)
    with open(HERE / "survey.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["player"] + [f"g{i}" for i in range(1, 11)])
        w.writerows(rows)
    print(f"wrote survey.csv: {N} players, 10 items")


if __name__ == "__main__":
    main()
