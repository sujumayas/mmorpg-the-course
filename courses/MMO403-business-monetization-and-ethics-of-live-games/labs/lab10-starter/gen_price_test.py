"""MMO403 Lab 10: player-level results of a three-arm price test.

Run:  python gen_price_test.py     (writes price_test.csv, seed 1129)

The test: the new-player starter bundle, normally $4.99, shown at one of three
prices. Arms are assigned 1/3 each by hashed account id. Each row is one exposed
player: their arm, the bundle price they saw, whether they bought the bundle within
14 days, and what they spent on the rest of the store in the same 14 days.
Do not read below main() until step 5 of the lab.
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 1129
PLAYERS = 36_000
ARMS = {"A": 4.99, "B": 6.99, "C": 3.99}
NEXT_BUNDLE = 9.99


def main(seed=SEED, write=True):
    rng = random.Random(seed)
    rows = []
    for i in range(PLAYERS):
        arm = "ABC"[rng.randrange(3)]
        price = ARMS[arm]
        conv = 0.05 - 0.005 * (price - 4.99)
        bought = rng.random() < conv
        # The next bundle: some of its buyers are pulled forward into a cheap starter bundle.
        p_next = {"A": 0.030, "B": 0.031, "C": 0.024}[arm]
        other = NEXT_BUNDLE if rng.random() < p_next else 0.0
        if rng.random() < 0.004:                 # a few players buy a lot of currency
            other += rng.choice([19.99, 49.99, 99.99])
        rows.append((f"p{i:05d}", arm, price, int(bought), round(other, 2)))
    if write:
        with open(HERE / "price_test.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(("player", "arm", "price", "bought", "other_spend"))
            w.writerows(rows)
        print(f"{len(rows)} players written to price_test.csv")
    return rows


if __name__ == "__main__":
    main()
