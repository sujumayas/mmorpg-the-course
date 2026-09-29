"""Generator for Lab 12. Do not edit. Rebuild the data with:

    ../../../../.venv/bin/python make_faucet.py

168 days (24 weeks, day 1 is a Monday) of one server's economy, in millions of gold:
    mob_loot, quest_reward   faucets, scale with active players, weekly cycle
    repair, auction_fee      sinks, scale with active players, weekly cycle
    residual                 snapshot supply minus ledger-predicted supply (should be about 0)
    active_players           distinct players that day

events.csv lists what the team planned and announced. Anything else in the data was not planned.
"""
import csv
import random

SEED = 12
DAYS = 168
WEEK = [1.00, 0.97, 1.00, 1.02, 1.10, 1.30, 1.25]  # Mon..Sun activity multiplier
PER_PLAYER = {"mob_loot": 1.00, "quest_reward": 0.60, "repair": 0.70, "auction_fee": 0.45}  # thousand gold/player/day
NOISE = {"mob_loot": 0.025, "quest_reward": 0.025, "repair": 0.025, "auction_fee": 0.03}  # relative sd

PLANNED = [  # day, series, multiplier, note
    (62, "mob_loot", 1.8, "Double gold weekend (Sat)"),
    (63, "mob_loot", 1.8, "Double gold weekend (Sun)"),
    (85, "quest_reward", 1.06, "Patch 2.3: quest rewards +6% from this day on"),
    (155, "all", None, "Expansion launch: new players expected"),
]


def main():
    rng = random.Random(SEED)
    rows = []
    for day in range(1, DAYS + 1):
        wd = (day - 1) % 7
        players = 40_000 * (1 + 0.0004 * day)
        if day >= 155:
            players *= 1.25
        players = round(players * (0.97 + 0.06 * WEEK[wd] / 1.3))
        row = dict(day=day, weekday="Mon Tue Wed Thu Fri Sat Sun".split()[wd], active_players=players)
        for s, pp in PER_PLAYER.items():
            mean = players * pp * WEEK[wd] / 1000
            if s == "mob_loot" and day in (62, 63):
                mean *= 1.8
            if s == "quest_reward" and day >= 85:
                mean *= 1.06
            if s == "mob_loot" and day >= 120:          # unplanned: slow dupe via mob loot
                mean += 1.2
            if s == "repair" and day >= 100:            # unplanned: some repairs stopped charging
                mean *= 0.955
            row[s] = round(rng.gauss(mean, NOISE[s] * mean), 2)
        resid = rng.gauss(0, 0.15)
        if day == 140:                                   # unplanned: one-day item-to-gold exploit
            resid += 6.0
        row["residual"] = round(resid, 2)
        rows.append(row)
    cols = ["day", "weekday", "active_players", "mob_loot", "quest_reward", "repair", "auction_fee", "residual"]
    with open("economy.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open("events.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day", "series", "expected_multiplier", "note"])
        for d, s, m, note in PLANNED:
            w.writerow([d, s, "" if m is None else m, note])
    print(f"wrote {len(rows)} days")


if __name__ == "__main__":
    main()
