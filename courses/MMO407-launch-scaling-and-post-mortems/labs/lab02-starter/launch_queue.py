"""MMO407 lab 02: launch queue planner.

Time is in whole minutes. Rates are players per minute. Counts are floats,
because the model is a fluid one (averages), as in the lecture.
Standard library only. Run the tests from inside lab02-starter/ with:
    python -m unittest test_launch_queue.py
"""
import math

# The lecture's section 2 launch: (end minute, players per minute across the game).
LECTURE_DEMAND = [(60, 1200), (180, 400), (math.inf, 150)]


def demand_at(schedule, t):
    """Players per minute arriving across the whole game at minute t."""
    for end, rate in schedule:
        if t < end:
            return rate
    return schedule[-1][1]


def simulate(worlds, cap, entry, session_min, schedule=LECTURE_DEMAND,
             model="full", minutes=720):
    """Queue length for ONE world after each minute of a fresh launch.

    Each minute t: arrivals demand/worlds join the queue; logouts happen
    according to `model`; then admit = min(queue, entry, cap - online).
    Models:
      "full"  - once the world is full (online >= cap), cap/session_min leave per minute
      "first" - online/session_min leave every minute from the start
      "fixed" - everyone stays exactly session_min minutes (admitted at t leave at t + session_min)
    Returns a list: log[t] is the queue after minute t (log[179] is hour 3).
    """
    # TODO 1: follow the docstring minute by minute; keep an `admitted` list for the fixed model
    raise NotImplementedError("TODO 1")


def queue_at(log, hour):
    """Queue at the end of hour `hour` (hour 3 is log[179])."""
    return log[60 * hour - 1]


def peak(log):
    """(peak queue, minute it happens) with minutes counted from 1."""
    t = max(range(len(log)), key=lambda i: log[i])
    return log[t], t + 1


def wait_at_back(queue, cap, session_min):
    """Minutes the last player in `queue` waits at a full world."""
    return queue / (cap / session_min)


def alive_on_day30(forecast_peak, worlds, threshold):
    """(players per world at the day-30 peak, True if at or above threshold)."""
    # TODO 2: players per world = forecast / worlds; compare with the threshold
    raise NotImplementedError("TODO 2")


def smallest_worlds(max_wait, hour, cap, entry, session_min,
                    schedule=LECTURE_DEMAND, limit=100):
    """Fewest worlds whose back-of-queue wait at `hour` is at most `max_wait`."""
    # TODO 3: try w = 1, 2, ... and return the first whose wait at the back is <= max_wait
    raise NotImplementedError("TODO 3")


def print_lecture_table():
    for w in (10, 15, 20):
        log = simulate(w, 4000, 100, 160)
        q, m = peak(log)
        print(f"{w} worlds: at 3 h {queue_at(log, 3):6.0f}, peak {q:6.0f} at minute {m}")


if __name__ == "__main__":
    try:
        print_lecture_table()
    except NotImplementedError as e:
        print(f"{e} is not done yet. Run the tests to see what is missing.")
