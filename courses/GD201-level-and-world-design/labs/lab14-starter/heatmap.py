"""GD201 Lab 14: death heatmaps that don't lie.

telemetry.csv has one row per event: player, run, t (seconds), kind ('pos' or 'death'), x, y
(metres). Every row, including a death, is also a position sample. The level is 40 x 20 m.
See lecture week 14, section 2.

Run `python heatmap.py` to print three maps of the sample playtest.
"""
import csv

WIDTH, HEIGHT = 40, 20


def load_events(path="telemetry.csv"):
    """List of dicts with keys player (str), run (int), t (int), kind (str), x and y (float)."""
    with open(path, newline="") as f:
        return [{"player": r["player"], "run": int(r["run"]), "t": int(r["t"]),
                 "kind": r["kind"], "x": float(r["x"]), "y": float(r["y"])}
                for r in csv.DictReader(f)]


def cell_of(x, y, size):
    """The (column, row) of the square cell of side `size` metres containing (x, y)."""
    # TODO
    raise NotImplementedError("cell_of")


def count_deaths(events, size):
    """Dict cell -> number of 'death' events in that cell."""
    # TODO
    raise NotImplementedError("count_deaths")


def count_visits(events, size):
    """Dict cell -> number of visits.

    Walk each (player, run) in the order the events appear. A visit starts at the first
    event of the run and every time the event's cell differs from the previous event's cell.
    """
    # TODO
    raise NotImplementedError("count_visits")


def heat(d, v, r_bar, k):
    """Shrunk death rate per visit: (d + k * r_bar) / (v + k)."""
    # TODO
    raise NotImplementedError("heat")


def heat_map(events, size, k):
    """Dict cell -> heat for every visited cell. r_bar is total deaths / total visits."""
    # TODO: use count_deaths, count_visits and heat.
    raise NotImplementedError("heat_map")


def top_cells(values, n):
    """The n cells with the highest value, highest first; break ties by the smaller cell."""
    # TODO
    raise NotImplementedError("top_cells")


def render(values, size, title):
    """Print a text map, north at the top. '.' = no data, then 0-9 by value / max value."""
    cols, rows = WIDTH // size, HEIGHT // size
    top = max(values.values()) or 1
    print(title)
    for row in reversed(range(rows)):
        line = ""
        for col in range(cols):
            val = values.get((col, row))
            line += "." if val is None else str(min(9, int(10 * val / top)))
        print("  " + line)


def report(size=4, k=20):
    ev = load_events()
    deaths, visits = count_deaths(ev, size), count_visits(ev, size)
    raw = {c: deaths.get(c, 0) / v for c, v in visits.items()}
    render({c: float(deaths.get(c, 0)) for c in visits}, size, "death count")
    render(raw, size, "raw rate (k = 0)")
    render(heat_map(ev, size, k), size, f"shrunk rate (k = {k})")
    for name, m in (("count", deaths), ("raw", raw), ("shrunk", heat_map(ev, size, k))):
        print(f"top 3 by {name}: {top_cells(m, 3)}")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}(). Fill in the TODOs, then run check_lab14.py.")
