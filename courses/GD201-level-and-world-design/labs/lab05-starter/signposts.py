"""GD201 Lab 05: signpost models, playtest fitting and route redesign. Standard library only.

Model (lecture week 5, section 2):
  one group      P(find) = 1 - (1 - p)^n
  a route        P(find) = 1 - product of (1 - p_i) over the signposts on it
  several groups P(find) = sum over groups of share_g x (group's P(find))

A group is a (share, p) pair, where share is the fraction of players in that group.
A route is a list of signposts. Each signpost is a dict mapping a group name to that
group's notice chance, for example {"scanner": 0.5, "tunneler": 0.05}.

Fill in the TODOs, then run `python check_lab05.py`. Run `python signposts.py` for a report.
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).parent

SUBTLE = {"scanner": 0.5, "tunneler": 0.05}   # a scuffed handhold, a broken railing
LOUD = {"scanner": 0.9, "tunneler": 0.9}      # paint, a strong light, a companion's line
SAMPLE_ROUTE = [SUBTLE] * 6
LECTURE_GROUPS = {"scanner": 0.7, "tunneler": 0.3}


def find_chance(p, n):
    """Chance that one player with notice chance p finds the route past n signposts."""
    # TODO: complement rule.
    raise NotImplementedError("find_chance")


def signposts_needed(p, target):
    """Smallest whole number of signposts at notice chance p giving P(find) >= target."""
    # TODO: ceil(ln(1 - target) / ln(1 - p)). Guard against float error just above an integer.
    raise NotImplementedError("signposts_needed")


def mixture(n, groups):
    """P(find) for n identical signposts and a list of (share, p) groups."""
    # TODO: sum of share x find_chance(p, n).
    raise NotImplementedError("mixture")


def route_find(route, shares):
    """P(find) for a route (list of signpost dicts) and {group: share}."""
    # TODO: for each group, 1 - product of (1 - signpost[group]); weight by share and add.
    raise NotImplementedError("route_find")


def lost_by_group(route, shares):
    """{group: share of all LOST players who belong to that group}. Values add to 1."""
    # TODO: lost in group g = share_g x product of (1 - p). Normalize by the total lost.
    raise NotImplementedError("lost_by_group")


def load_log(path=HERE / "playtest_log.csv"):
    """Return {tester: {signpost: 0 or 1}}. Provided for you."""
    log = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            log.setdefault(row["tester"], {})[row["signpost"]] = int(row["noticed"])
    return log


def signpost_rates(log):
    """{signpost: share of testers who noticed it}."""
    # TODO
    raise NotImplementedError("signpost_rates")


def tester_rates(log):
    """{tester: share of signposts that tester noticed}."""
    # TODO
    raise NotImplementedError("tester_rates")


def fit_two_groups(log, cut=0.5):
    """Split testers at `cut` (rate >= cut is a scanner). Return
    {"scanner": (share, mean rate), "tunneler": (share, mean rate)}.
    The mean rate is the pooled share of signposts noticed by the group's testers."""
    # TODO
    raise NotImplementedError("fit_two_groups")


def simulate(route, shares, players=10_000, seed=1):
    """Monte Carlo check of route_find. Each player draws a group by share, then walks the
    route and notices each signpost with that group's chance. Return the share who notice
    at least one. Use random.Random(seed) so the result is repeatable."""
    # TODO
    raise NotImplementedError("simulate")


def report():
    log = load_log()
    fit = fit_two_groups(log)
    shares = {g: s for g, (s, _) in fit.items()}
    print("signpost rates:", {k: round(v, 3) for k, v in signpost_rates(log).items()})
    print("fitted groups:", {g: (round(s, 3), round(p, 3)) for g, (s, p) in fit.items()})
    route = [{g: p for g, (_, p) in fit.items()}] * 6
    print(f"fitted route, 6 signposts: P(find) = {route_find(route, shares):.1%}")
    print(f"lecture groups, sample route: P(find) = {route_find(SAMPLE_ROUTE, LECTURE_GROUPS):.1%}")
    print(f"simulated: {simulate(SAMPLE_ROUTE, LECTURE_GROUPS):.1%}")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not finished yet: {e} is still a TODO. Run check_lab to see what passes.")
