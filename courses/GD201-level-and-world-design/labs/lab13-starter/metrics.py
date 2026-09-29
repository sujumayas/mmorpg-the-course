"""GD201 Lab 13: jump reach and a metrics audit.

Units are whatever your game uses (Quake units in the sample). See lecture week 13, section 2.

A metrics sheet is a dict:
    v0     launch speed of the jump (units/s, upward)
    g      gravity (units/s^2)
    v      horizontal run speed (units/s)
    w      width of the collision box (units)
    step   maximum step height (units)

A jump is a dict with a name, the gap (edge to edge, units) and dy, the height of the far
ledge's top above the take-off floor (negative when it is lower). A gap of 0 means the
player only has to get up (or down) a ledge that starts right at their feet.

Run `python metrics.py` to print an audit of the sample route.
"""
from math import sqrt

QUAKE_RUN = {"v0": 270, "g": 800, "v": 320, "w": 32, "step": 18}

SAMPLE_ROUTE = [
    {"name": "crate hop",      "gap": 0,   "dy": 16},
    {"name": "crate climb",    "gap": 0,   "dy": 40},
    {"name": "pit",            "gap": 180, "dy": 0},
    {"name": "broken bridge",  "gap": 230, "dy": 0},
    {"name": "ledge up",       "gap": 120, "dy": 32},
    {"name": "high ledge",     "gap": 100, "dy": 44},
    {"name": "drop across",    "gap": 240, "dy": -64},
    {"name": "tower top",      "gap": 40,  "dy": 60},
]


def jump_height(v0, g):
    """Apex height h = v0^2 / (2 g)."""
    # TODO
    raise NotImplementedError("jump_height")


def time_to_apex(v0, g):
    """Time to apex t_h = v0 / g."""
    # TODO
    raise NotImplementedError("time_to_apex")


def max_gap(dy, m):
    """Widest clearable gap G(dy) = v t_h (1 + sqrt(1 - dy/h)) + w for the metrics sheet m.

    Return None when dy > h (the ledge is above the apex).
    """
    # TODO: use jump_height and time_to_apex.
    raise NotImplementedError("max_gap")


def classify(jump, m, gap_margin=0.8, height_margin=0.9):
    """Return one of 'walk', 'comfortable', 'skill', 'impossible'.

    walk:        gap == 0 and dy <= step
    impossible:  dy > h, or gap > G(dy)
    skill:       gap > gap_margin * G(dy), or dy > height_margin * h
    comfortable: everything else
    """
    # TODO
    raise NotImplementedError("classify")


def audit(route, m, gap_margin=0.8, height_margin=0.9):
    """List of (name, verdict, percent) for each jump in the route.

    percent is 100 * gap / G(dy), rounded to one decimal, or None when G(dy) is None.
    """
    # TODO: call max_gap and classify for each jump.
    raise NotImplementedError("audit")


def report():
    m = QUAKE_RUN
    print(f"h = {jump_height(m['v0'], m['g']):.2f}, t_h = {time_to_apex(m['v0'], m['g']):.4f}")
    for name, verdict, pct in audit(SAMPLE_ROUTE, m):
        shown = "   —  " if pct is None else f"{pct:5.1f}%"
        print(f"{name:15s} {shown}  {verdict}")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}(). Fill in the TODOs, then run check_lab13.py.")
