"""CS203 Lab 10 starter: an awareness meter and path-based hearing.

Run:   python perception.py      prints the tuning table for the two routes
Check: python check_lab10.py     exits 0 only when your work is complete

You edit the five functions and one method marked TODO. Everything else is
provided. Time runs in whole ticks of DT seconds, so tests never depend on
floating-point luck.
"""
from collections import deque

DT = 0.1                         # seconds per AI tick
T_NEAR, T_FAR, RANGE = 1.0, 4.0, 20.0
SUSPICIOUS_ON, SUSPICIOUS_OFF, ALERT = 0.5, 0.3, 1.0
EPS = 1e-9


def detect_time(d, light=1.0):
    """Seconds of unbroken sight to fill the meter from 0 to 1.

    T = (T_NEAR + (T_FAR - T_NEAR) * min(d, RANGE) / RANGE) / light
    Return float('inf') when light <= 0.
    """
    raise NotImplementedError("detect_time")  # TODO


def break_even(d, light=1.0, forget=6.0):
    """Largest exposure share e / (e + h) that never fills the meter: T / (T + F)."""
    raise NotImplementedError("break_even")  # TODO


class Awareness:
    """One NPC's awareness of one target.

    meter: float in [0, 1]
    state: "unaware", "suspicious" or "alert"

    Rules for update():
      sensed:     meter += DT / detect_time(d, light), capped at 1
      not sensed: meter -= DT / forget, floored at 0
      then state transitions, in this order:
        meter >= ALERT - EPS                       -> "alert"
        state == "alert" and meter <= EPS          -> "unaware"   (lost the target)
        state == "unaware" and meter >= 0.5 - EPS  -> "suspicious"
        state == "suspicious" and meter < 0.3      -> "unaware"
      An alert NPC stays alert until the meter drains to 0.
    """

    def __init__(self, forget=6.0):
        self.forget = forget
        self.meter = 0.0
        self.state = "unaware"

    def update(self, sensed, d, light=1.0):
        """Advance one tick and return the new state."""
        raise NotImplementedError("Awareness.update")  # TODO


def simulate(route, forget=6.0):
    """route: list of (seconds, sensed, distance, light) segments, run once in order.

    Returns (first_alert_time or None, list of (time, state) state changes).
    Provided: uses your Awareness.update.
    """
    npc, t, changes, first_alert = Awareness(forget), 0, [], None
    for seconds, sensed, d, light in route:
        for _ in range(round(seconds / DT)):
            t += 1
            before = npc.state
            after = npc.update(sensed, d, light)
            if after != before:
                changes.append((round(t * DT, 1), after))
                if after == "alert" and first_alert is None:
                    first_alert = round(t * DT, 1)
    return first_alert, changes


def load_grid(text):
    """Grid of 1 m cells: '.' open, '#' wall. Returns a list of strings."""
    return [row for row in text.splitlines() if row.strip()]


def path_distance(grid, a, b):
    """Shortest 4-way walking distance in cells from a to b, (row, col) tuples.

    Use breadth-first search (every step costs 1). Walls '#' block.
    Return None if b cannot be reached.
    """
    raise NotImplementedError("path_distance")  # TODO


def heard(radius, distance, offscreen_far=False):
    """True if a sound of this radius reaches a listener at this path distance.

    Off-screen listeners that are far away hear at half radius (Blacklist rule).
    distance None means no path, so never heard.
    """
    raise NotImplementedError("heard")  # TODO


# Two routes past the same guard. Segments: (seconds, sensed, distance m, light)
CAREFUL = [(1.0, True, 12, 1.0), (3.0, False, 12, 1.0)] * 4 + [(4.0, True, 18, 0.5)]
CARELESS = [(2.0, True, 12, 1.0), (1.0, False, 12, 1.0)] * 4 + [(4.0, True, 18, 0.5)]

if __name__ == "__main__":
    print(f"{'F (s)':>6} {'careful':>10} {'careless':>10}")
    for forget in (2, 4, 6, 8, 12, 20):
        try:
            c, _ = simulate(CAREFUL, forget)
            r, _ = simulate(CARELESS, forget)
            show = lambda x: "safe" if x is None else f"{x:.1f} s"
            print(f"{forget:>6} {show(c):>10} {show(r):>10}")
        except NotImplementedError as exc:
            print(f"{forget:>6} {'-':>10} {'-':>10}   ({exc} not written yet)")
            break
