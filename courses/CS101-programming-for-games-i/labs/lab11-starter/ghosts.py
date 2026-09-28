"""CS101 Lab 11 starter, part 1: the ghost mode machine (model of Pac-Man level 1).

Python 3.10+, standard library only. Fill in the functions marked TODO.
Rules (lecture 11, section 2):
  1. Schedule: scatter 7, chase 20, scatter 7, chase 20, scatter 5, chase 20, scatter 5, chase forever.
  2. A power pellet switches to "frightened" for `seconds`. While frightened, the schedule
     clock does NOT advance. When fright ends, return to SCHEDULE[phase] mode.
  3. Leaving "scatter" or "chase" for any mode adds one reversal. Leaving "frightened" does not.
"""

SCHEDULE = [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20),
            ("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", None)]


def new_ghost():
    """Given, do not change."""
    return {"mode": "scatter", "phase": 0, "phase_time": 0.0,
            "fright_left": 0.0, "reversals": 0}


def change_mode(ghost, new_mode):
    """The ONLY place that assigns ghost["mode"]. Apply rule 3 here."""
    raise NotImplementedError("TODO")


def update(ghost, dt):
    """Advance the machine by dt seconds. Carry leftover time into the next phase
    (phase_time -= duration), do not reset it to zero."""
    raise NotImplementedError("TODO")


def eat_power_pellet(ghost, seconds=6.0):
    """Enter frightened mode for `seconds`. Eating one while already frightened
    restarts the countdown and must NOT add a reversal."""
    raise NotImplementedError("TODO")


def run(pellets=(), until=100.0, dt=1 / 60, fright=6.0):
    """Given. Simulate from 0 to `until` seconds with pellets eaten at the listed times.
    Returns a list of (time, new_mode, reversals_so_far) for every mode change."""
    ghost = new_ghost()
    pending = sorted(pellets)
    log = []
    last = ghost["mode"]
    for i in range(1, int(round(until / dt)) + 1):
        t = i * dt
        update(ghost, dt)
        if pending and t >= pending[0] - 1e-9:
            eat_power_pellet(ghost, fright)
            pending.pop(0)
        if ghost["mode"] != last:
            log.append((round(t, 2), ghost["mode"], ghost["reversals"]))
            last = ghost["mode"]
    return log


if __name__ == "__main__":
    for row in run():
        print(row)
