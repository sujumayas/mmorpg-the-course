"""GD201 Lab 11: zone population planner.

The neighbour model from lecture week 11:
    at a camp:    N_camp = f * P / H - 1
    in the open:  N_open = (1 - f) * P * pi * r^2 / A

Part A implements the formulas, Part B a Monte Carlo placement that tests them,
Part C measures what uneven camp choice does. Standard library only.

Run `python crowd.py` to print a report for the teaching zone.
"""
import math
import random

TEACHING_ZONE = {"A": 1_000_000, "H": 8, "f": 0.6, "r": 40}


def camp_neighbours(P, H, f):
    """Others seen by a player at a camp: f * P / H - 1."""
    # TODO Part A
    raise NotImplementedError("camp_neighbours")


def open_neighbours(P, f, r, A):
    """Others seen by a player in the open: (1 - f) * P * pi * r^2 / A."""
    # TODO Part A
    raise NotImplementedError("open_neighbours")


def capacity(H, f, n_min, n_max):
    """Comfortable range (P_min, P_max): P_min = H(n_min + 1) / f as a float,
    P_max = floor(H(n_max + 1) / f) as an int."""
    # TODO Part A
    raise NotImplementedError("capacity")


def copies_needed(P, P_max):
    """ceiling(P / P_max), and at least 1."""
    # TODO Part A
    raise NotImplementedError("copies_needed")


def toroidal_distance(a, b, side):
    """Distance between points a and b on a square of this side length whose edges wrap
    around (leaving the right edge brings you in at the left). Removes edge effects. Given."""
    dx = abs(a[0] - b[0]); dy = abs(a[1] - b[1])
    dx = min(dx, side - dx); dy = min(dy, side - dy)
    return math.hypot(dx, dy)


def simulate(P, H, f, r, A, camp_radius=15.0, trials=20, seed=1, random_camps=False):
    """Monte Carlo test of the model. For each trial:
      - m = round(f * P) players go to camps. If random_camps is False, player i goes to camp
        i % H (even split). If True, each picks a camp uniformly at random.
        Each camp player stands at a uniform random point in a disc of camp_radius.
      - The other P - m players stand at uniform random points in a square of area A.
      - camp count: for each camp player, the number of OTHER players at the SAME camp
        within r (ordinary distance).
      - open count: for each open player, the number of OTHER open players within r,
        using toroidal_distance.
    Return (mean camp count, mean open count), averaged over every player in every trial.
    Use random.Random(seed) so results repeat."""
    # TODO Part B (and Part C for random_camps=True)
    raise NotImplementedError("simulate")


def main():
    z = TEACHING_ZONE
    for P in (100, 400, 1000):
        try:
            print(P, round(camp_neighbours(P, z["H"], z["f"]), 2),
                  round(open_neighbours(P, z["f"], z["r"], z["A"]), 2))
        except NotImplementedError as e:
            print(P, f"not implemented yet ({e})")
    try:
        print("capacity", capacity(z["H"], z["f"], 2, 10))
        print("simulate P=400", simulate(400, z["H"], z["f"], z["r"], z["A"]))
    except NotImplementedError as e:
        print(f"not implemented yet ({e})")


if __name__ == "__main__":
    main()
