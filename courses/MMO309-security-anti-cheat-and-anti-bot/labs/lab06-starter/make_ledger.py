"""Writes bots.csv: a synthetic ban log for 2,000 bot accounts (seed 309).

The numbers are invented for practice and do not come from any real game.
Each account is created on a day from 0 to 89. Detection finds it after a geometric number
of days (daily chance 0.15). The studio bans in weekly waves: a detected account is banned
on the first wave day (days 7, 14, 21, ...) strictly after its detection day.
The log ends on day 120. Accounts not detected by then have empty detected/banned cells,
and accounts detected but not yet banned have an empty banned cell.
"""
import csv
import random
from pathlib import Path

END_DAY = 120
WAVE = 7
TRUE_D = 0.15


def main(path=Path(__file__).resolve().parent / "bots.csv"):
    rng = random.Random(309)
    rows = []
    for i in range(2000):
        created = rng.randrange(0, 90)
        k = 1
        while rng.random() >= TRUE_D:
            k += 1
        detected = created + k
        banned = (detected // WAVE + 1) * WAVE
        rows.append({
            "account": f"bot{i:04d}",
            "created_day": created,
            "detected_day": detected if detected <= END_DAY else "",
            "banned_day": banned if banned <= END_DAY and detected <= END_DAY else "",
        })
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path


if __name__ == "__main__":
    print("wrote", main())
