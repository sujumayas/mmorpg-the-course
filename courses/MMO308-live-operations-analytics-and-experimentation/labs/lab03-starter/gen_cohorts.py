"""MMO308 Lab 03 data generator. Writes two files next to this script:

installs.csv  player_id, install_day      (days 0-89)
activity.csv  day, player_id              (one row per active player per day, days 0-89)

The game is invented. About 500 players install every day. Hidden in the data
are three changes of the kinds described in the week 3 lecture. Your job is to
find their dates and types from the data, so do not read the SECRET block below
until you have written your answers. Seed 303. Standard library only.
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 303
DAYS = 90
QS, QT, PLAY = 0.985, 0.30, 0.9   # stayer and tourist daily survival; alive players play 90% of days

# ---- SECRET: the planted effects (read only after step 5 of the lab) ----
BREAK_DAY, W_NORMAL, W_BROKEN = 31, 0.25, 0.15
OUTAGE_DAY, OUTAGE_KEEP = 52, 0.35
ENDGAME_DAY, QS_AFTER = 70, 0.97
# --------------------------------------------------------------------------


def main():
    rng = random.Random(SEED)
    pid = 0
    with open(HERE / "installs.csv", "w", newline="") as fi, \
         open(HERE / "activity.csv", "w", newline="") as fa:
        wi, wa = csv.writer(fi), csv.writer(fa)
        wi.writerow(["player_id", "install_day"])
        wa.writerow(["day", "player_id"])
        for c in range(DAYS):
            for _ in range(rng.randint(460, 540)):
                pid += 1
                name = f"P{pid:06d}"
                wi.writerow([name, c])
                wa.writerow([c, name])
                w = W_BROKEN if c >= BREAK_DAY else W_NORMAL
                stayer = rng.random() < w
                for t in range(c + 1, DAYS):
                    q = (QS_AFTER if t > ENDGAME_DAY else QS) if stayer else QT
                    if rng.random() >= q:
                        break                      # left the game for good
                    keep = OUTAGE_KEEP if t == OUTAGE_DAY else 1.0
                    if rng.random() < PLAY * keep:
                        wa.writerow([t, name])
    print(f"wrote installs.csv and activity.csv for {pid:,} players")


if __name__ == "__main__":
    main()
