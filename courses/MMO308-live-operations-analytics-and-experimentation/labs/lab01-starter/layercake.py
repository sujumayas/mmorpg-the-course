"""MMO308 Lab 01: the layer cake.

Weekly active players (WAU) of a live game are a stack of install cohorts:

    WAU(t) = sum over s <= t of installs[s] * R(t - s)

with the two-type retention curve from the week 1 lecture:

    R(a) = w * qs**a + (1 - w) * qt**a

  w   share of each cohort who are "stayers"
  qs  weekly survival of a stayer
  qt  weekly survival of a "tourist"

Fill in every function marked TODO, then run `python test_layercake.py`.
Standard-library Python 3.10+ only.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The lecture's reference game.
BASE = {"w": 0.30, "qs": 0.90, "qt": 0.30}


def retention(a, w, qs, qt):
    """Share of a cohort active in week a after install (a = 0 is the install week)."""
    raise NotImplementedError("retention: implement R(a)")


def lifetime(w, qs, qt):
    """Expected active weeks per install, L = sum of R(a) for a = 0, 1, 2, ...
    Use the closed form, not a long loop."""
    raise NotImplementedError("lifetime: closed form of the sum of R(a)")


def plateau(ongoing, w, qs, qt):
    """Steady-state WAU when every week brings `ongoing` installs."""
    raise NotImplementedError("plateau: installs per week times lifetime")


def layers(installs, w, qs, qt):
    """Return a list of rows, one per week t = 0 .. len(installs) - 1.
    Row t is a list of the contribution of every cohort s <= t:
    [installs[0] * R(t), installs[1] * R(t - 1), ..., installs[t] * R(0)]."""
    raise NotImplementedError("layers: one row per week, one entry per cohort")


def wau_series(installs, w, qs, qt):
    """Total WAU per week: the sum of each row of layers()."""
    raise NotImplementedError("wau_series: sum the layers")


def launch_share(installs, t, w, qs, qt):
    """Share of WAU in week t that comes from the launch cohort (s = 0)."""
    raise NotImplementedError("launch_share: launch layer divided by the total")


# ---------------------------------------------------------------- provided

def launch_installs(weeks, launch=200_000, ongoing=10_000):
    """The lecture's install pattern: one big launch week, then a steady trickle."""
    return [launch] + [ongoing] * (weeks - 1)


def load_steam(path=HERE / "steam_monthly.csv"):
    """Monthly average concurrent players from SteamCharts (see lab01.md for the source).
    Returns {game: [(month, avg_players), ...]} in date order."""
    out = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            out.setdefault(row["game"], []).append((row["month"], int(row["avg_players"])))
    return out


def write_layers_csv(installs, path, w, qs, qt, bands=(0, 1, 5, 13, 27)):
    """Write a CSV you can plot as a stacked area: launch cohort, then cohorts
    grouped into bands by install week. Uses your layers()."""
    rows = layers(installs, w, qs, qt)
    edges = list(bands) + [10**9]
    names = [f"cohorts_{a}_{b - 1}" if b < 10**9 else f"cohorts_{a}_plus"
             for a, b in zip(edges, edges[1:])]
    names[0] = "launch"
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["week"] + names + ["total"])
        for t, row in enumerate(rows):
            sums = [sum(row[a:min(b, t + 1)]) for a, b in zip(edges, edges[1:])]
            wr.writerow([t] + [round(x) for x in sums] + [round(sum(row))])


if __name__ == "__main__":
    inst = launch_installs(53)
    series = wau_series(inst, **BASE)
    for t in (0, 1, 2, 4, 8, 12, 26, 52):
        print(f"week {t:2d}  WAU {series[t]:9,.0f}  launch share {launch_share(inst, t, **BASE):6.1%}")
    print(f"lifetime L = {lifetime(**BASE):.3f} weeks, plateau = {plateau(10_000, **BASE):,.0f}")
    write_layers_csv(inst, HERE / "layers.csv", **BASE)
    print("wrote layers.csv")
