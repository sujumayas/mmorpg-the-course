"""MA201 Lab 12 starter: a grid raycaster and a hitscan check.

Run:   python raycast.py          renders the lecture map as text, then the maze
Check: python check_lab12.py      exits 0 only when your work is complete

You write the five functions marked TODO. Maps are lists of strings, '#' is a
wall, row index y grows downward, cell (cx, cy) covers cx <= x < cx + 1.
"""
import math

LECTURE_MAP = [
    "########",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "########",
]

MAZE = [
    "################",
    "#......#.......#",
    "#.##...#..###..#",
    "#.#....#....#..#",
    "#.#..###....#..#",
    "#..............#",
    "####..#####..###",
    "#.....#........#",
    "#..#..#..####..#",
    "#..#.....#.....#",
    "#..####..#..#..#",
    "#.......##..#..#",
    "#..#........#..#",
    "#..#..####.....#",
    "#.....#........#",
    "################",
]

# The server map for Part C. Pillars are single wall cells.
ARENA = [
    "############",
    "#..........#",
    "#..#.......#",
    "#..........#",
    "#.....#....#",
    "#..........#",
    "#........#.#",
    "#..........#",
    "############",
]


def is_wall(grid, cx, cy):
    """Cells outside the map count as walls, so rays always stop."""
    if cy < 0 or cy >= len(grid) or cx < 0 or cx >= len(grid[cy]):
        return True
    return grid[cy][cx] == "#"


# ---------------------------------------------------------------- TODO: yours

def grid_walk(grid, ox, oy, dx, dy, t_max=math.inf):
    """First wall along the ray from (ox, oy) with unit direction (dx, dy).

    Return (t, (cx, cy), side) where side is "x" if the ray crossed a vertical
    line (x = integer) to enter the wall cell and "y" otherwise, or None if no
    wall is entered with t <= t_max. Exact ties (t_max_x == t_max_y) go to y.
    Use math.inf for t_delta and t_max on an axis where the direction is 0.
    """
    raise NotImplementedError("grid_walk")  # TODO


def column_heights(grid, ox, oy, view_deg, fov_deg, n, perp=True, h=240.0):
    """Heights of n wall columns. Ray i is at view + fov * (i / (n - 1) - 0.5)
    degrees. Height = h / distance, where distance is t_perp = t cos(a - view)
    if perp else t. A ray that hits nothing gives height 0."""
    raise NotImplementedError("column_heights")  # TODO


def ray_sphere(o, d, c, radius):
    """First t >= 0 where o + t d (d unit, 3D tuples) meets the sphere, else None.
    If the origin is inside, return 0.0."""
    raise NotImplementedError("ray_sphere")  # TODO


def ray_aabb(o, d, lo, hi):
    """Slab test. First t >= 0 where the ray enters the box, else None.
    If the origin is inside, return 0.0. Handle d[axis] == 0 without dividing."""
    raise NotImplementedError("ray_aabb")  # TODO


def can_see(grid, a, b):
    """Exact line of sight between points a and b: False if the segment from a
    to b enters any wall cell (walk the cells, don't sample). A segment that
    passes exactly through the shared corner of two diagonal wall cells is
    blocked."""
    raise NotImplementedError("can_see")  # TODO


# ---------------------------------------------------------------- provided

def sampled_can_see(grid, a, b, per_cell=4):
    """The old server check: sample every 1/per_cell of a cell. Has a bug class."""
    (ax, ay), (bx, by) = a, b
    n = max(1, math.ceil(per_cell * max(abs(bx - ax), abs(by - ay))))
    for i in range(n + 1):
        x, y = ax + (bx - ax) * i / n, ay + (by - ay) * i / n
        if is_wall(grid, int(x), int(y)):
            return False
    return True


SHADES = " .:-=+*#%@"


def render(grid, ox, oy, view_deg, fov_deg=60, cols=64, rows=20, perp=True):
    heights = column_heights(grid, ox, oy, view_deg, fov_deg, cols, perp, h=rows * 2.0)
    lines = []
    for r in range(rows):
        row = ""
        for hgt in heights:
            half = min(hgt, rows) / 2
            inside = abs(r + 0.5 - rows / 2) <= half
            shade = SHADES[min(len(SHADES) - 1, int(hgt / 3))] if inside else " "
            row += shade
        lines.append(row)
    return "\n".join(lines)


if __name__ == "__main__":
    try:
        print("lecture map, correction off:")
        print(render(LECTURE_MAP, 2.5, 4.5, 0, perp=False))
        print("lecture map, correction on:")
        print(render(LECTURE_MAP, 2.5, 4.5, 0, perp=True))
        print("maze:")
        print(render(MAZE, 1.5, 1.5, 30))
    except NotImplementedError as exc:
        print(f"-- {exc} not written yet")
