"""MMO402 Lab 10 starter: audit four pacing rules over a player population.

Usage:  python lab10-starter.py            # runs the self-test, then the audit
        python lab10-starter.py --csv out.csv

Units: experience is measured in percent of a level. A session is (day, start_hour,
length_hours), day 0 = Monday ... 6 = Sunday. The simulation runs hour by hour for
WEEKS weeks and reports the last week, so rested pools reach a steady state.

Rules (lecture week 10, section 2):
  flat     every played hour earns B.
  rested   offline hours add A to a pool capped at CAP; a played hour earns
           B + min(pool, B) and the bonus is removed from the pool.
  fatigue  within one calendar day: hours 0-3 earn B, hours 3-5 earn B/2, later 0.
  daily    every played hour earns B, plus D on the first played hour of each day.
  weekly   (you design it in Part C) every played hour earns B, plus a weekly bonus.

Pure standard library. Python 3.8+.
"""
import csv
import random
import sys

B = 10.0        # base experience per hour (percent of a level)
A = 0.625       # rested accrual per offline hour (WoW: 10% per 16 h in an inn)
CAP = 150.0     # rested cap (WoW: 150% of a level)
D = 10.0        # daily reward
WEEKS = 6


def sessions_for(days, hours):
    """Evening sessions at 18:00, or 10:00 if longer than 6 hours."""
    start = 18 if hours <= 6 else 10
    return [(d, start, hours) for d in days]


def played_hours(sessions):
    """Set of (day, hour) cells that are played in one week."""
    cells = set()
    for day, start, length in sessions:
        for h in range(start, start + length):
            cells.add((day + h // 24, h % 24))
    return cells


def simulate(sessions, rule):
    played = played_hours(sessions)
    pool = 0.0
    week_total = 0.0
    for w in range(WEEKS):
        week_total = 0.0
        for day in range(7):
            hours_today = 0
            for hour in range(24):
                if (day, hour) in played:
                    gain = rule_gain(rule, hours_today, pool)
                    if rule == "rested":
                        pool -= gain - B        # bonus comes out of the pool
                    hours_today += 1
                    week_total += gain
                else:
                    pool = min(CAP, pool + A)
    return week_total


def rule_gain(rule, hours_today, pool):
    if rule == "flat":
        return B
    if rule == "rested":
        # TODO Part A: return B plus the rested bonus.
        raise NotImplementedError("rested")
    if rule == "fatigue":
        # TODO Part A: 1x for the first 3 hours today, 0.5x until 5, then 0.
        raise NotImplementedError("fatigue")
    if rule == "daily":
        # TODO Part A: B, plus D on the first played hour of the day.
        raise NotImplementedError("daily")
    raise ValueError(rule)


LECTURE = {
    "light":   (sessions_for([5, 6], 2),        {"flat": 40, "rested": 80, "fatigue": 40, "daily": 60}),
    "daily":   (sessions_for(range(7), 2),      {"flat": 140, "rested": 236.25, "fatigue": 140, "daily": 210}),
    "weekend": (sessions_for([5, 6], 7),        {"flat": 140, "rested": 236.25, "fatigue": 80, "daily": 160}),
    "binge":   (sessions_for([6], 14),          {"flat": 140, "rested": 236.25, "fatigue": 40, "daily": 150}),
}


def self_test(rules=("flat", "rested", "fatigue", "daily")):
    ok = True
    for name, (sess, expected) in LECTURE.items():
        for rule in rules:
            try:
                got = simulate(sess, rule)
            except NotImplementedError:
                print(f"  {name:8s} {rule:8s} not implemented yet")
                ok = False
                continue
            flag = "ok" if abs(got - expected[rule]) < 1e-6 else "MISMATCH"
            ok &= flag == "ok"
            print(f"  {name:8s} {rule:8s} {got:8.2f}  expected {expected[rule]:8.2f}  {flag}")
    return ok


def population(n=500, seed=402):
    """Synthetic schedules. Four archetypes with random variation.

    Shares: 30% evening regulars, 30% weekenders, 25% irregulars, 15% marathoners.
    Returns a list of (player_id, archetype, sessions).
    """
    rng = random.Random(seed)
    players = []
    for pid in range(n):
        r = rng.random()
        if r < 0.30:
            arche = "regular"
            days = sorted(rng.sample(range(7), rng.randint(4, 7)))
            sess = sessions_for(days, rng.randint(1, 3))
        elif r < 0.60:
            arche = "weekender"
            days = [5, 6] if rng.random() < 0.7 else [4, 5, 6]
            sess = sessions_for(days, rng.randint(3, 8))
        elif r < 0.85:
            arche = "irregular"
            days = sorted(rng.sample(range(7), rng.randint(1, 4)))
            sess = [(d, rng.choice([12, 18, 20]), rng.randint(1, 4)) for d in days]
        else:
            arche = "marathon"
            days = sorted(rng.sample(range(7), rng.randint(1, 2)))
            sess = sessions_for(days, rng.randint(9, 14))
        players.append((pid, arche, sess))
    return players


def audit(players, rules=("flat", "rested", "fatigue", "daily")):
    rows = []
    for pid, arche, sess in players:
        hours = sum(length for _, _, length in sess)
        row = {"player": pid, "archetype": arche, "hours": hours, "days": len(sess)}
        for rule in rules:
            row[rule] = simulate(sess, rule)
        rows.append(row)
    return rows


if __name__ == "__main__":
    print("Self-test against the lecture table:")
    if not self_test():
        print("Finish Part A before running the audit.")
        sys.exit(1)
    rows = audit(population())
    # TODO Part B: summarize rows by archetype (mean experience per hour for each rule,
    # and each rule's total as a ratio of flat).
    if "--csv" in sys.argv:
        path = sys.argv[sys.argv.index("--csv") + 1]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {len(rows)} rows to {path}")
