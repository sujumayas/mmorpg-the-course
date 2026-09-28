"""CS101 Lab 10 starter: collision toolkit.

Python 3.10+, standard library only. Fill in every function marked TODO.
Boxes are dicts {"x", "y", "w", "h"} with (x, y) the top-left corner and y pointing down.
Circles are dicts {"cx", "cy", "r"}.
Run the tests with:  python test_lab10.py
"""


def edges(box):
    """Return (left, right, top, bottom). Given, do not change."""
    return box["x"], box["x"] + box["w"], box["y"], box["y"] + box["h"]


def aabb_overlap(a, b):
    """True if boxes a and b overlap. Touching edges do NOT count (strict rule).
    Use exactly the four comparisons from the lecture, in the lecture's order."""
    raise NotImplementedError("TODO")


def circle_overlap(a, b):
    """True if circles a and b overlap (strict). No square roots."""
    raise NotImplementedError("TODO")


def clamp(v, lo, hi):
    """Given, do not change."""
    return max(lo, min(v, hi))


def circle_box_overlap(c, box):
    """True if circle c overlaps box (strict). Use the nearest point on the box."""
    raise NotImplementedError("TODO")


def overlap_depth(a, b):
    """Return (ox, oy), the overlap on each axis. Values <= 0 mean no overlap on that axis."""
    raise NotImplementedError("TODO")


def push_out(a, b):
    """Return a NEW box: a moved along the axis of smaller overlap, away from b's center,
    so that a and b touch but no longer overlap. If they don't overlap, return a copy of a.
    On a tie (ox == oy) push along y."""
    raise NotImplementedError("TODO")


def bullet_hits_wall(speed, fps, wall_x=200, wall_t=16, bullet_size=4, substeps=1,
                     start_x=10, seconds=1.0):
    """Simulate a bullet flying right along y = 0 at `speed` px/s.

    The bullet is a box of side `bullet_size` whose left edge starts at start_x.
    The wall is a box from wall_x to wall_x + wall_t, very tall.
    Each frame lasts 1/fps seconds and is split into `substeps` equal moves;
    after EACH move, test the bullet against the wall with aabb_overlap.
    Return the time (seconds, float) of the first hit, or None if it never hits.

    The loop below is complete except for the TODO line."""
    bullet = {"x": start_x, "y": 0, "w": bullet_size, "h": bullet_size}
    wall = {"x": wall_x, "y": -1000, "w": wall_t, "h": 2000}
    dt = 1.0 / fps
    frames = int(round(seconds * fps))
    for frame in range(1, frames + 1):
        for step in range(1, substeps + 1):
            bullet["x"] += speed * dt / substeps
            # TODO: if the bullet overlaps the wall, return the time of this substep
            #       (frame - 1) * dt + step * dt / substeps
    return None


if __name__ == "__main__":
    player = {"x": 100, "y": 100, "w": 32, "h": 48}
    print("A overlaps:", aabb_overlap(player, {"x": 120, "y": 130, "w": 32, "h": 32}), "(want True)")
    for fps in (120, 60, 30, 20):
        print(f"{fps:>3} fps, 900 px/s, 16 px wall:", bullet_hits_wall(900, fps))
