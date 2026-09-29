"""MMO308 Lab 04: funnels and churn from an event log.

Run:  python gen_log.py        # once, writes the three CSV files
      python funnel.py         # prints your results
      python check_lab04.py    # PASS / FAIL / TODO per function

Fill in every function that raises NotImplementedError. Use only the
standard library. Days are integers; day 0 is launch day.

Data (loaded for you by load()):
    players   dict  player_id -> (install_day, cadence)
    sessions  dict  player_id -> sorted list of days with a session
    chapters  dict  player_id -> {chapter: day completed}
"""
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
AS_OF = 119          # the day you are analysing on; later days are the future
STEPS = 8            # story chapters


def load():
    players, sessions, chapters = {}, defaultdict(list), defaultdict(dict)
    with open(HERE / "players.csv") as f:
        for r in csv.DictReader(f):
            players[int(r["player_id"])] = (int(r["install_day"]), r["cadence"])
    with open(HERE / "sessions.csv") as f:
        for r in csv.DictReader(f):
            sessions[int(r["player_id"])].append(int(r["day"]))
    with open(HERE / "chapters.csv") as f:
        for r in csv.DictReader(f):
            chapters[int(r["player_id"])][int(r["chapter"])] = int(r["day"])
    for days in sessions.values():
        days.sort()
    return players, dict(sessions), dict(chapters)


def step_conversions(counts):
    """counts[0] is the number at the top, counts[k] the number reaching step k.
    Return [counts[1]/counts[0], counts[2]/counts[1], ...] (length len(counts) - 1).
    If a denominator is 0, use 0.0 for that ratio."""
    raise NotImplementedError


def snapshot_funnel(players, chapters, as_of=AS_OF, steps=STEPS):
    """Open, unboxed snapshot, as a dashboard or Steam would show it on day as_of.
    Top of the funnel: every player with install_day <= as_of.
    Return (n_top, shares) where shares[k-1] is the share of n_top who completed
    chapter k on a day <= as_of, for k = 1..steps."""
    raise NotImplementedError


def cohort_funnel(players, chapters, window, as_of=AS_OF, steps=STEPS):
    """Closed, time-boxed cohort funnel.
    Eligible: players with install_day <= as_of - window (they have all had
    `window` days). A player counts at step k only if they completed chapters
    1..k, each on a day <= install_day + window.
    Return (n_eligible, shares) with shares[k-1] for k = 1..steps."""
    raise NotImplementedError


def churned(players, sessions, W, as_of=AS_OF):
    """Set of player_ids labelled churned on day as_of with inactivity window W:
    installed on or before as_of - W, and no session in the days
    as_of - W + 1 .. as_of (so their last session up to as_of is <= as_of - W)."""
    raise NotImplementedError


def false_churn_share(players, sessions, W, as_of=AS_OF, horizon=60, cadence=None):
    """Among players labelled churned on as_of with window W (optionally only those
    with the given cadence), the share who have at least one session in the days
    as_of + 1 .. as_of + horizon. Return 0.0 if nobody is labelled."""
    raise NotImplementedError


def main():
    players, sessions, chapters = load()
    for name, fn in (("snapshot", lambda: snapshot_funnel(players, chapters)),
                     ("cohort, 30-day box", lambda: cohort_funnel(players, chapters, 30)),
                     ("cohort, 60-day box", lambda: cohort_funnel(players, chapters, 60))):
        try:
            n, shares = fn()
            conv = step_conversions([1.0] + shares)
            print(f"{name:>20}  n={n:>5}  " + " ".join(f"{s:6.1%}" for s in shares))
            print(f"{'step conversion':>20}  {'':7}  " + " ".join(f"{c:6.1%}" for c in conv))
        except NotImplementedError:
            print(f"{name:>20}  TODO")
    for W in (3, 7, 14, 30):
        try:
            row = [false_churn_share(players, sessions, W, cadence=c)
                   for c in ("daily", "regular", "occasional", None)]
            print(f"W={W:>2}  false churn  daily {row[0]:.1%}  regular {row[1]:.1%}  "
                  f"occasional {row[2]:.1%}  all {row[3]:.1%}")
        except NotImplementedError:
            print(f"W={W:>2}  TODO")


if __name__ == "__main__":
    main()
