"""Generator for Lab 10. Do not edit. Run it to rebuild the data files:

    ../../../../.venv/bin/python make_survey.py

It simulates one week of a fictional MMO with 60,000 active players, then:
- an in-game survey shown to players who are online at random moments
  (chance of being asked proportional to hours played that week),
- a quest bug that leaves some players stuck, reported through two channels.

Files written:
    survey.csv          one row per respondent: player_id, segment, hours_7d, sessions_7d, approve
    forum_accounts.txt  accounts that posted in the bug thread, one per line
    reporter_accounts.txt  accounts that used the in-game bug reporter
    stuck_accounts.txt  accounts the telemetry shows stuck on the quest (the ground truth)
    stuck_telemetry.csv player_id and hours_7d for every stuck account
"""
import csv
import random

SEED = 10
N_PLAYERS = 60_000
EXPECTED_RESPONDENTS = 3_000

# segment: (share of players, mean hours per week, mean sessions per week, base approval)
SEGMENTS = {
    "casual": (0.62, 2.5, 2.0, 0.72),
    "regular": (0.28, 9.0, 5.0, 0.52),
    "hardcore": (0.10, 26.0, 11.0, 0.22),
}


def make_players(rng):
    players = []
    names = list(SEGMENTS)
    cum = []
    total = 0.0
    for s in names:
        total += SEGMENTS[s][0]
        cum.append(total)
    for i in range(N_PLAYERS):
        u = rng.random()
        seg = names[next(k for k, c in enumerate(cum) if u <= c)]
        _, mh, ms, base = SEGMENTS[seg]
        hours = round(max(0.5, rng.gammavariate(4.0, mh / 4.0)), 1)
        sessions = max(1, round(rng.gammavariate(3.0, ms / 3.0)))
        # within a segment, heavier players approve a little less
        p = min(0.95, max(0.05, base - 0.004 * (hours - mh)))
        approve = 1 if rng.random() < p else 0
        players.append(dict(player_id=f"a{i + 1:05d}", segment=seg, hours_7d=hours,
                            sessions_7d=sessions, approve=approve))
    return players


def online_now_sample(players, n, rng):
    """Each player is asked independently with chance c * hours (Poisson sampling), so the
    chance of being asked is exactly proportional to hours. c is set so about n are asked.
    Everyone asked answers (nonresponse is UX201's problem, not this lab's)."""
    c = n / sum(p["hours_7d"] for p in players)
    return [p for p in players if rng.random() < min(1.0, c * p["hours_7d"])]


def bug_channels(players, rng):
    # Some players got stuck on the quest; heavier players more often.
    stuck = [p for p in players if rng.random() < min(0.9, 0.02 + 0.006 * p["hours_7d"])]
    forum, reporter = [], []
    for p in stuck:
        engaged = min(1.0, p["hours_7d"] / 30.0)
        if rng.random() < 0.03 + 0.25 * engaged:
            forum.append(p["player_id"])
        if rng.random() < 0.08 + 0.30 * engaged:
            reporter.append(p["player_id"])
    return stuck, forum, reporter


def main():
    rng = random.Random(SEED)
    players = make_players(rng)
    sample = online_now_sample(players, EXPECTED_RESPONDENTS, rng)
    with open("survey.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["player_id", "segment", "hours_7d", "sessions_7d", "approve"])
        w.writeheader()
        for p in sorted(sample, key=lambda p: p["player_id"]):
            w.writerow(p)
    stuck_players, forum, reporter = bug_channels(players, rng)
    stuck = [p["player_id"] for p in stuck_players]
    with open("stuck_telemetry.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["player_id", "hours_7d"])
        for p in sorted(stuck_players, key=lambda p: p["player_id"]):
            w.writerow([p["player_id"], p["hours_7d"]])
    for name, ids in (("stuck_accounts.txt", stuck), ("forum_accounts.txt", forum),
                      ("reporter_accounts.txt", reporter)):
        with open(name, "w") as f:
            f.write("\n".join(sorted(ids)) + "\n")
    truth = sum(p["approve"] for p in players) / len(players)
    print(f"players {len(players)}, respondents {len(sample)}, true approval {truth:.4f}")
    print(f"stuck {len(stuck)}, forum {len(forum)}, reporter {len(reporter)}, "
          f"both {len(set(forum) & set(reporter))}")


if __name__ == "__main__":
    main()
