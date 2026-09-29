"""MMO407 lab 08: battle escalation model.

One step is one real minute. Pilot counts are whole numbers; game progress
is a float. Cost constants are MMO302 week 12's invented teaching values.
Standard library only. Run the tests from inside lab08-starter/ with:
    python -m unittest test_battle_loop.py
"""

A_COST, B_COST, FLOOR = 0.0003, 0.000001, 0.1


def work(n):
    """CPU-seconds to simulate one game-second with n pilots."""
    return A_COST * n + B_COST * n * n


def speed(n, C=1.0, floor=FLOOR):
    """Game speed f = clamp(C / W(n), floor, 1)."""
    return max(floor, min(1.0, C / work(n)))


def battle(n0=1000, r=20, G=60, pool=6000, C=1.0, deadline=None,
           dilate=True, floor=FLOOR):
    """Run one fight. Returns a dict with keys:
        "T"            real minutes until the fight ends
        "n_end"        pilots in the system when it ends
        "pilot_hours"  sum of n over every minute, divided by 60
        "game"         game-minutes done when it ends
        "floor_min"    real minutes spent at the floor (speed == floor)
        "decided"      True if game >= G, False if the deadline stopped it
    Each minute, in this order: add speed(n) to game (or 1.0 if not dilate),
    add n to the pilot-minute total, count the minute, then
    n = min(pool, n + r). Stop when game >= G or when t reaches deadline.
    """
    # TODO 1: follow the docstring
    raise NotImplementedError("TODO 1")


def fit_rate(timeline):
    """Estimate the arrival rate r (pilots per minute) from a list of
    (minute, pilots) observations, as the least-squares slope of pilots
    against minutes. Needs at least two points."""
    # TODO 2: slope = sum((x - mx)(y - my)) / sum((x - mx)^2)
    raise NotImplementedError("TODO 2")


def objective_for_length(target, **kw):
    """Smallest whole G (1 to 600) whose fight lasts at least `target`
    real minutes, with the other parameters from kw. None if none does."""
    # TODO 3: search G = 1, 2, ... using battle()
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    for label, kw in [("no dilation needed", {"dilate": False}),
                      ("lecture battle", {}),
                      ("half the arrivals", {"r": 10}),
                      ("node twice as fast", {"C": 2.0})]:
        b = battle(**kw)
        print(f"{label:20s} {b['T']:4d} min {b['n_end']:5d} pilots "
              f"{b['pilot_hours']:7,.0f} pilot-hours")
