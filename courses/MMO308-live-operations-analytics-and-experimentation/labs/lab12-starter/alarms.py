"""Lab 12: faucet alarms.

Fill in the five functions marked TODO (lecture week 12, sections 2 and 4).
Days are 1-based in the CSV; lists in this file are 0-based, so day d is index d - 1.
Standard-library Python 3 only.

    ../../../../.venv/bin/python alarms.py
"""
import csv
import statistics

SERIES = ["mob_loot", "quest_reward", "repair", "auction_fee", "residual"]


def read_economy(path="economy.csv"):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    data = {s: [float(r[s]) for r in rows] for s in SERIES}
    data["active_players"] = [int(r["active_players"]) for r in rows]
    data["weekday"] = [r["weekday"] for r in rows]
    return data


def read_events(path="events.csv"):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def weekday_baseline(values, i, weeks=4, skip=frozenset()):
    """Mean of values[i - 7], values[i - 14], ... over `weeks` earlier same weekdays.

    Indices in `skip` (planned events, known incidents) are left out; if that leaves
    fewer than `weeks` values, go further back until you have `weeks` or run out.
    Raise ValueError if there is no earlier same weekday at all.
    """
    # TODO
    raise NotImplementedError


def robust_sigma(residuals):
    """1.4826 times the median absolute deviation from the median."""
    # TODO
    raise NotImplementedError


def spike_alarms(z, limit=3.0):
    """Indices where z > limit."""
    # TODO
    raise NotImplementedError


def cusum(z, k=0.5, h=5.0, direction=1):
    """One-sided CUSUM. direction=1 watches for rises, -1 for falls (the mirror score).

    Returns (scores, first_alarm) where scores[i] is S after index i and first_alarm is
    the first index with S > h, or None. S starts at 0 and never goes below 0.
    """
    # TODO
    raise NotImplementedError


def zscores(values, baselines, sigma):
    """(value - baseline) / sigma for each pair; None where the baseline is None."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    data = read_economy()
    x = data["mob_loot"]
    base = [weekday_baseline(x, i) if i >= 28 else None for i in range(len(x))]
    sigma = robust_sigma([x[i] - base[i] for i in range(28, 56)])
    z = zscores(x, base, sigma)
    watched = [v for v in z[56:]]
    scores, first = cusum(watched)
    print(f"mob_loot raw: sigma {sigma:.2f}, first CUSUM alarm on day {None if first is None else first + 57}")
    print("This naive pipeline ignores events, patches and player counts. Steps 3 to 6 fix that.")
