"""MMO405 Lab 08: writes survey.csv and telemetry.csv (seed 808).

telemetry.csv  one row per account: account_id, logged_total_h, logged_active_h
               (hours per week over the last 8 weeks; "active" excludes stretches
               of 10+ minutes with no input, which the server flags as idle)
survey.csv     one row per respondent: account_id, cohort (veteran/new),
               reported_h (answer to "In a typical week, how many hours do you play?")

Some survey ids have no telemetry row (typed wrongly or deleted accounts), and
most accounts in telemetry did not answer the survey.
Run:  python gen_data.py
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    rng = random.Random(808)
    tele, survey = [], []
    for i in range(1, 1201):
        aid = f"A{i:04d}"
        veteran = rng.random() < 0.45
        total = round(rng.gammavariate(2.2, 7.0 if veteran else 5.0), 1)
        idle_share = rng.uniform(0.15, 0.40) if veteran else rng.uniform(0.02, 0.15)
        active = round(total * (1 - idle_share), 1)
        tele.append((aid, total, active))
        if rng.random() < 0.25:
            under = rng.uniform(0.0, 0.35) if veteran else rng.uniform(-0.05, 0.12)
            reported = max(0, round(total * (1 - under) + rng.gauss(0, 1.5)))
            survey.append((aid, "veteran" if veteran else "new", reported))
    for j in range(8):
        survey.append((f"A{9000 + j}", rng.choice(["veteran", "new"]), rng.randint(2, 40)))
    rng.shuffle(survey)
    with open(HERE / "telemetry.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "logged_total_h", "logged_active_h"])
        w.writerows(tele)
    with open(HERE / "survey.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "cohort", "reported_h"])
        w.writerows(survey)
    print(f"wrote telemetry.csv ({len(tele)} accounts) and survey.csv ({len(survey)} responses)")


if __name__ == "__main__":
    main()
