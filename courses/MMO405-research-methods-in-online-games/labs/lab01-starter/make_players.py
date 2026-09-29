"""Writes players.csv, the invented 2,000-account log for MMO405 lab 01.
Run: python make_players.py   (already run once; the CSV ships with the starter)

Counts are exact by construction, so every answer in the lab has one right value.
Columns: account_id, week1_band (low/mid/high hours played in week one),
in_guild_d7 (1 if in a guild on day 7), active_d30 (1 if any session on days 28-30).
"""
import csv
import random

# band: (accounts, in guild, retained among guild, retained among no guild)
PLAN = {
    "low": (1000, 100, 25, 180),
    "mid": (600, 240, 120, 162),
    "high": (400, 320, 256, 60),
}


def build():
    rows = []
    for band, (n, g, kept_g, kept_u) in PLAN.items():
        u = n - g
        rows += [(band, 1, 1)] * kept_g + [(band, 1, 0)] * (g - kept_g)
        rows += [(band, 0, 1)] * kept_u + [(band, 0, 0)] * (u - kept_u)
    random.Random(405).shuffle(rows)
    return [{"account_id": f"A{i:05d}", "week1_band": b, "in_guild_d7": g, "active_d30": a}
            for i, (b, g, a) in enumerate(rows, start=1)]


if __name__ == "__main__":
    with open("players.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["account_id", "week1_band", "in_guild_d7", "active_d30"])
        w.writeheader()
        w.writerows(build())
    print("wrote players.csv")
