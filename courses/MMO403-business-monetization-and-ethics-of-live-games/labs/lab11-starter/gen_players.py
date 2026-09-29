"""MMO403 Lab 11: a player population for a subscription MMO considering a token.

Run:  python gen_players.py     (writes players.csv, seed 1111)

Each row is one active or recently lapsed player. wtp_usd is the most they would pay
in cash for a month of subscription. gold_per_month is the gold they earn in a month
of normal play. The two are drawn so that players with more time (more gold) tend to
have less spare cash, which is the population a token is designed for.
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 1111
PLAYERS = 50_000


def main(seed=SEED, write=True):
    rng = random.Random(seed)
    rows = []
    for i in range(PLAYERS):
        time_rich = rng.gauss(0, 1)                      # hidden trait
        wtp = math.exp(rng.gauss(2.75 - 0.35 * time_rich, 0.45))
        gold = math.exp(rng.gauss(11.0 + 0.8 * time_rich, 0.6))
        rows.append((f"p{i:05d}", round(wtp, 2), int(gold)))
    if write:
        with open(HERE / "players.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(("player", "wtp_usd", "gold_per_month"))
            w.writerows(rows)
        print(f"{len(rows)} players written to players.csv")
    return rows


if __name__ == "__main__":
    main()
