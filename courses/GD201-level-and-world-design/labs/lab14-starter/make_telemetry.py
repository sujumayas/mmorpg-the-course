"""Makes telemetry.csv for GD201 Lab 14: a synthetic playtest of an invented 40 x 20 m level.

You don't need to edit this file. Read TRUE_DANGER after you have made your heatmaps and
compare: which regions did your maps find, and which did they miss or exaggerate?

Players start at the spawn room (west), follow one of three routes east to the exit,
and are sampled once per second. Each second spent in a region carries that region's
chance of dying. A run ends at the exit or at a death. Each tester plays several runs.
"""
import csv
import random

# region name: (x0, y0, x1, y1) in metres, and the chance of dying per second inside it
TRUE_DANGER = {
    "spawn room":  ((0, 6, 6, 14), 0.002),
    "corridor":    ((6, 8, 26, 12), 0.012),
    "sniper yard": ((14, 12, 26, 20), 0.070),
    "vent":        ((10, 0, 30, 4), 0.050),
    "bridge":      ((26, 8, 34, 12), 0.030),
    "exit hall":   ((34, 6, 40, 14), 0.004),
}
ROUTES = {  # waypoints (x, y); how often testers pick each route
    "main":  ([(3, 10), (26, 10), (34, 10), (39, 10)], 0.70),
    "yard":  ([(3, 10), (14, 10), (18, 16), (24, 16), (26, 10), (34, 10), (39, 10)], 0.25),
    "vent":  ([(3, 10), (8, 10), (10, 2), (30, 2), (34, 10), (39, 10)], 0.05),
}
SPEED = 2.0  # metres per second, a cautious playtest pace


def danger_at(x, y):
    for (x0, y0, x1, y1), p in TRUE_DANGER.values():
        if x0 <= x < x1 and y0 <= y < y1:
            return p
    return 0.01


def samples(waypoints):
    """Positions once per second along the waypoints."""
    x, y = waypoints[0]
    yield x, y
    for tx, ty in waypoints[1:]:
        while True:
            dx, dy = tx - x, ty - y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= SPEED:
                x, y = tx, ty
                break
            x, y = x + SPEED * dx / dist, y + SPEED * dy / dist
            yield x, y
        yield x, y


def main(testers=30, runs=4, seed=13, path="telemetry.csv"):
    rng = random.Random(seed)
    names, weights = zip(*[(n, w) for n, (_, w) in ROUTES.items()])
    with open(path, "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["player", "run", "t", "kind", "x", "y"])
        for p in range(testers):
            for r in range(runs):
                route = rng.choices(names, weights)[0]
                for t, (x, y) in enumerate(samples(ROUTES[route][0])):
                    x += rng.uniform(-0.8, 0.8)
                    y += rng.uniform(-0.8, 0.8)
                    x, y = min(max(x, 0), 39.9), min(max(y, 0), 19.9)
                    out.writerow([f"p{p:02d}", r, t, "pos", f"{x:.2f}", f"{y:.2f}"])
                    if rng.random() < danger_at(x, y):
                        out.writerow([f"p{p:02d}", r, t, "death", f"{x:.2f}", f"{y:.2f}"])
                        break


if __name__ == "__main__":
    main()
    print("wrote telemetry.csv")
