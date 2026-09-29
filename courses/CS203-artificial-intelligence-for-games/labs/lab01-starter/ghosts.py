"""CS203 Lab 01 starter: ghost brains. Standard library only.

Fill in the TODO functions, then run the tests:

    ../../../../.venv/bin/python test_ghosts.py      (or: python3 test_ghosts.py)

Then run this file to watch the maze simulation:

    python3 ghosts.py

Coordinates follow the week 1 lecture: a tile is (x, y), x grows to the right,
y grows DOWNWARD. Directions are unit steps.
"""

UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)
ORDER = [UP, LEFT, DOWN, RIGHT]          # tie-break order for the turn rule

# Published arcade schedules (Pittman, "The Pac-Man Dossier"). Even indices are
# scatter, odd indices are chase; after the list, chase forever.
LEVEL_1 = [7, 20, 7, 20, 5, 20, 5]
LEVELS_2_TO_4 = [7, 20, 7, 20, 5, 1033, 1 / 60]
LEVEL_5_UP = [5, 20, 5, 20, 5, 1037, 1 / 60]


# ---------------------------------------------------------------- your code

def ahead(tile, facing, n, bug=True):
    """TODO step 1. Return the tile n steps ahead of `tile` in direction `facing`.
    If bug is True and facing is UP, reproduce the arcade overflow bug:
    n up AND n left."""
    raise NotImplementedError("ahead() is yours to write")


def target(name, pac, facing, ghost, blinky, corner, bug=True):
    """TODO step 2. Return the chase-mode target tile of ghost `name`
    ("blinky", "pinky", "inky" or "clyde").
    pac: Pac-Man's tile; facing: his direction; ghost: this ghost's tile;
    blinky: Blinky's tile (Inky needs it); corner: this ghost's scatter corner
    (Clyde needs it). Clyde chases when his squared distance to Pac-Man is
    >= 64 and retreats to his corner otherwise. Do not use a square root."""
    raise NotImplementedError("target() is yours to write")


def choose_direction(tile, heading, open_dirs, goal):
    """TODO step 3. The turn rule. Among the directions in open_dirs, excluding
    the reverse of heading, return the one whose next tile has the smallest
    squared distance to goal. Break ties in ORDER (up, left, down, right).
    If the reverse is the only open direction, return the reverse."""
    raise NotImplementedError("choose_direction() is yours to write")


def mode_at(t, schedule):
    """TODO step 4. Return "scatter" or "chase" at t seconds into the level."""
    raise NotImplementedError("mode_at() is yours to write")


def scatter_seconds(schedule, window):
    """TODO step 4. Seconds of scatter in the first `window` seconds, counted
    frame by frame at 60 Hz (a frame at time f/60 counts if mode_at says scatter)."""
    raise NotImplementedError("scatter_seconds() is yours to write")


# ------------------------------------------------ provided: maze simulation

W, H = 25, 29                            # x 0..24, y 0..28


def is_open(x, y):
    """Lattice maze from the lecture's interactive: walls where x and y are both odd."""
    return 0 <= x < W and 0 <= y < H and not (x % 2 == 1 and y % 2 == 1)


def open_dirs(tile):
    return {d for d in ORDER if is_open(tile[0] + d[0], tile[1] + d[1])}


CORNERS = {"blinky": (24, -2), "pinky": (0, -2), "inky": (24, 30), "clyde": (0, 30)}


def pac_route():
    """Pac-Man loops the outer ring clockwise, one tile per step."""
    ring = [(x, 0) for x in range(W)] + [(W - 1, y) for y in range(1, H)]
    ring += [(x, H - 1) for x in range(W - 2, -1, -1)] + [(0, y) for y in range(H - 2, 0, -1)]
    return ring


def spacing(ghosts):
    """Mean Manhattan distance over the 6 pairs of ghosts."""
    g = list(ghosts.values())
    pairs = [(a, b) for i, a in enumerate(g) for b in g[i + 1:]]
    return sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in pairs) / len(pairs)


def bunched(ghosts):
    """True if all four ghosts fit in a box whose width + height is at most 6 tiles."""
    xs = [p[0] for p in ghosts.values()]
    ys = [p[1] for p in ghosts.values()]
    return (max(xs) - min(xs)) + (max(ys) - min(ys)) <= 6


def simulate(steps=800, personalities=True, schedule=LEVEL_1, seconds_per_step=0.25):
    """Run the ghosts on the lattice while Pac-Man loops the outer ring.
    Returns (mean spacing, fraction of steps bunched), measured in chase mode only."""
    ring = pac_route()
    ghosts = {"blinky": (12, 14), "pinky": (12, 12), "inky": (10, 14), "clyde": (14, 14)}
    heading = {name: LEFT for name in ghosts}
    last_mode, chase_steps, total_spacing, total_bunched = None, 0, 0.0, 0
    for step in range(steps):
        pac, nxt = ring[step % len(ring)], ring[(step + 1) % len(ring)]
        facing = (nxt[0] - pac[0], nxt[1] - pac[1])
        mode = mode_at(step * seconds_per_step, schedule)
        reverse_now = last_mode is not None and mode != last_mode
        last_mode = mode
        for name, tile in ghosts.items():
            if mode == "scatter":
                goal = CORNERS[name]
            else:
                who = name if personalities else "blinky"
                goal = target(who, pac, facing, tile, ghosts["blinky"], CORNERS[name])
            h = heading[name]
            if reverse_now:
                d = (-h[0], -h[1])
            else:
                d = choose_direction(tile, h, open_dirs(tile), goal)
            heading[name] = d
            ghosts[name] = (tile[0] + d[0], tile[1] + d[1])
        if mode == "chase":
            chase_steps += 1
            total_spacing += spacing(ghosts)
            total_bunched += bunched(ghosts)
    return total_spacing / chase_steps, total_bunched / chase_steps


if __name__ == "__main__":
    for p in (True, False):
        label = "four personalities" if p else "four Blinkys      "
        s, b = simulate(personalities=p)
        print(f"{label}: mean spacing {s:.2f} tiles, bunched {b:.0%} of chase steps")
