"""MMO308 Lab 02 data generator. Writes two files next to this script:

activity.csv  one row per active player per day: day (0-89), player_id
payments.csv  one row per purchase: day, player_id, amount (USD)

The game is invented. Days 0-29 are month 1, 30-59 month 2, 60-89 month 3.
A free weekend ran on days 40 and 41. Seed 2026. Standard library only.
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 2026
DAYS = 90
FREE_WEEKEND = (40, 41)


def main():
    rng = random.Random(SEED)
    players = []          # [player_id, kind, p, first_day, last_day]
    pid = 0

    def add(kind, p, first):
        nonlocal pid
        pid += 1
        # regulars quit with a small daily hazard; others stop after their visit(s)
        last = first
        while last < DAYS - 1 and rng.random() > 0.004:
            last += 1
        players.append([f"P{pid:06d}", kind, p, first, last])

    for _ in range(6_000):
        add("regular", rng.choice([0.15, 0.30, 0.50, 0.80]), 0)
    for day in range(1, DAYS):
        for _ in range(30):
            add("regular", rng.choice([0.15, 0.30, 0.50, 0.80]), day)
        for _ in range(20):
            add("drifter", 0.0, day)
    for _ in range(4_000):
        add("weekend", 0.0, FREE_WEEKEND[0])

    with open(HERE / "activity.csv", "w", newline="") as fa, \
         open(HERE / "payments.csv", "w", newline="") as fp:
        wa, wp = csv.writer(fa), csv.writer(fp)
        wa.writerow(["day", "player_id"])
        wp.writerow(["day", "player_id", "amount"])
        for player_id, kind, p, first, last in players:
            if kind == "regular":
                days = [d for d in range(first, last + 1) if d == first or rng.random() < p]
                pay_p = 0.03
            elif kind == "drifter":
                days = [first]
                pay_p = 0.005
            else:
                days = sorted(rng.sample(FREE_WEEKEND, rng.choice([1, 1, 2])))
                if rng.random() < 0.10:  # a few stay on as light players
                    days += [d for d in range(42, DAYS) if rng.random() < 0.10]
                pay_p = 0.01
            for d in days:
                wa.writerow([d, player_id])
                if rng.random() < pay_p:
                    wp.writerow([d, player_id, rng.choice([4.99, 4.99, 9.99, 9.99, 19.99, 49.99])])
    print(f"wrote activity.csv and payments.csv for {len(players):,} players")


if __name__ == "__main__":
    main()
