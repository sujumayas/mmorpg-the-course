"""CS101 lab 13, part B: a seeded enemy spawner with a safe radius.

Run:   python spawner.py      (prints a text map of 40 spawns)

Arena is W x H pixels. The player stands at (px, py). An enemy must not
appear within SAFE_RADIUS pixels of the player. We use rejection sampling:
pick a uniform random point, throw it away if it is too close, try again,
and give up after MAX_ATTEMPTS so a bad arena can never freeze the game.
"""
import math
import random

W, H = 800, 600
SAFE_RADIUS = 150
MAX_ATTEMPTS = 20

# Weighted spawn table: (enemy kind, weight). Weights need not sum to 100.
SPAWN_TABLE = [("grunt", 70), ("runner", 25), ("brute", 5)]


def random_point(rng):
    """A uniform random point inside the arena."""
    return rng.uniform(0, W), rng.uniform(0, H)


def spawn_position(rng, px, py, safe=SAFE_RADIUS, attempts=MAX_ATTEMPTS):
    """Return (x, y, tries) for a point at least `safe` px from (px, py).

    Returns (None, None, attempts) if every attempt landed too close.

    TODO (step 6): loop up to `attempts` times. Draw a point with
    random_point(rng). Compare the SQUARED distance with safe * safe
    (no square root needed). Return the first point that is far enough,
    together with the number of tries it took (1 for the first try).
    """
    x, y = random_point(rng)  # TODO: fallback ignores the safe radius
    return x, y, 1


def pick_kind(rng, table=SPAWN_TABLE):
    """Pick an enemy kind using the weights in `table`."""
    kinds = [k for k, _ in table]
    weights = [w for _, w in table]
    return rng.choices(kinds, weights=weights, k=1)[0]


def text_map(points, px, py, cols=40, rows=15):
    """Draw spawns as '*' and the player as '@' on a small character grid."""
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for x, y in points:
        grid[min(rows - 1, int(y / H * rows))][min(cols - 1, int(x / W * cols))] = "*"
    grid[int(py / H * rows)][int(px / W * cols)] = "@"
    return "\n".join("".join(r) for r in grid)


def demo(seed=7, n=40, px=W / 2, py=H / 2):
    rng = random.Random(seed)
    points, tries, kinds = [], [], {}
    for _ in range(n):
        x, y, t = spawn_position(rng, px, py)
        tries.append(t)
        if x is not None:
            points.append((x, y))
            k = pick_kind(rng)
            kinds[k] = kinds.get(k, 0) + 1
    too_close = sum(math.hypot(x - px, y - py) < SAFE_RADIUS for x, y in points)
    print(text_map(points, px, py))
    print(f"spawned {len(points)}, too close: {too_close}, "
          f"mean tries {sum(tries) / len(tries):.2f}, kinds {kinds}")


if __name__ == "__main__":
    demo()
