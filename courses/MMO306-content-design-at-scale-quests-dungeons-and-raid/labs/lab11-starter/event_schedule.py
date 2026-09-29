"""MMO306 Lab 11 starter: the event clock.

Fill in every function marked TODO. Standard library only.

    python event_schedule.py                        # prints the lecture table once done
    python -m unittest test_event_schedule.py       # all tests fail until you write the code

Symbols follow the week 11 lecture. All times are in minutes.
    N  daily players who want the event
    S  session length (one session per player per day)
    W  join window: minutes after a start in which a player can still join
    T  interval between starts
"""
import csv
import random

DAY = 1440


def reach(T, S, W):
    """Share of daily players whose session catches at least one start: min(1, (S + W) / T)."""
    raise NotImplementedError("TODO: reach")


def crowd(N, T, S, W):
    """Players at one occurrence with a once-per-day reward: N * min(S + W, T) / 1440."""
    raise NotImplementedError("TODO: crowd")


def n_crit(n_min, S, W):
    """Smallest N for which some interval gives a crowd of at least n_min."""
    raise NotImplementedError("TODO: n_crit")


def kill_time(n, H0, h, d):
    """Seconds to kill a boss with health H0 + h * n when n players each deal d DPS."""
    raise NotImplementedError("TODO: kill_time")


def load_hourly_weights(path):
    """Read online_by_hour.csv (columns hour, share_of_session_starts).

    Return a list of 24 floats, index = hour, normalised to sum to 1.
    """
    raise NotImplementedError("TODO: load_hourly_weights")


def simulate(N, S, W, T, days=10, seed=11, hourly_weights=None):
    """Simulate `days` days. Each day each of N players starts one session of
    length S. The start minute is uniform over the day, or, if hourly_weights
    is given, pick the hour with those weights and then a uniform minute
    inside it. Use one random.Random(seed) for everything.

    Occurrences start at 0, T, 2T, ... (minutes since day 0 began, running
    across days). A player whose session starts at s catches an occurrence
    at t if s - W <= t <= s + S. With a once-per-day reward they attend only
    the FIRST occurrence they catch.

    Return a dict:
        "reach":          attendances / (N * days)
        "mean_crowd":     total attendances / number of occurrences in the run
        "crowd_by_start": {minute of day of each start: mean attendance per day}
                          for example {0: ..., 360: ..., 720: ..., 1080: ...} when T = 360
    """
    raise NotImplementedError("TODO: simulate")


if __name__ == "__main__":
    try:
        for T in (30, 60, 105, 120, 180, 360, 1440):
            print(f"every {T:4d} min  reach {reach(T, 90, 15):5.1%}  crowd {crowd(3000, T, 90, 15):6.1f}")
        r = simulate(3000, 90, 15, 360)
        print("simulated T=360:", round(r["reach"], 3), round(r["mean_crowd"], 1))
    except NotImplementedError as e:
        print("not done yet:", e)
