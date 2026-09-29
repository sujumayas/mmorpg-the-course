"""MMO405 Lab 09: a guild network from census snapshots, and its centralities.

Run:  python gen_census.py      # once, writes census.csv
      python sna.py             # prints the centrality table once your functions work
      python check_lab09.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
A census row is a dict with keys snapshot, day, minute, character, guild, zone,
grouped (all strings, as csv.DictReader returns them).
A tie key is a tuple (a, b) of two character names with a < b.
An adjacency is a dict {member: set of neighbours} that includes every member,
even members with no ties.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
CITIES = {"Capital", "Harbor"}
INTERVAL = 10  # minutes between snapshots


def load(name):
    with open(HERE / name, newline="") as f:
        return list(csv.DictReader(f))


def members(rows, guild):
    """Sorted list of every character seen at least once in the guild."""
    raise NotImplementedError


def build_ties(rows, guild, cities=CITIES, interval=INTERVAL):
    """Ducheneaut-style co-activity ties. Two members of `guild` are tied in a
    snapshot when both are grouped ("y"), in the same zone, and the zone is not
    a city. Return {(a, b): minutes}, where minutes = interval x the number of
    snapshots in which the pair was tied."""
    raise NotImplementedError


def graph(ties, nodes, min_minutes=0):
    """Adjacency over all `nodes`, keeping ties with minutes >= min_minutes."""
    raise NotImplementedError


def degree_centrality(adj):
    """{v: deg(v) / (n - 1)} with n = len(adj)."""
    raise NotImplementedError


def strength(adj, ties):
    """{v: total minutes on v's ties that are present in adj}."""
    raise NotImplementedError


def betweenness(adj):
    """Normalised betweenness. For every unordered pair {s, t} of other members
    with t reachable from s, add sigma_sv * sigma_vt / sigma_st to v whenever
    dist(s, v) + dist(v, t) = dist(s, t). Divide by (n - 1)(n - 2) / 2."""
    raise NotImplementedError


def eigenvector(adj, rounds=200):
    """Start every score at 1. Each round set y(v) = x(v) + sum of neighbours' x,
    then divide every y by the largest y. Return the scores after `rounds`."""
    raise NotImplementedError


def top_by_threshold(ties, nodes, thresholds, measure):
    """For each threshold, build the graph with that min_minutes, compute
    `measure` (a function of adj), and return {threshold: member with the
    highest score}, breaking ties alphabetically."""
    raise NotImplementedError


def main():
    rows = load("census.csv")
    nodes = members(rows, "Lanternfall")
    ties = build_ties(rows, "Lanternfall")
    rank = {r["character"]: r["rank"] for r in load("ranks.csv")}
    adj = graph(ties, nodes)
    deg, st, btw, eig = degree_centrality(adj), strength(adj, ties), betweenness(adj), eigenvector(adj)
    print(f"{len(nodes)} members, {len(ties)} ties")
    print(f"{'member':8} {'rank':13} {'degree':>6} {'minutes':>7} {'betw':>6} {'eig':>5}")
    for v in sorted(nodes, key=lambda v: (-btw[v], v)):
        print(f"{v:8} {rank.get(v, '?'):13} {deg[v]:6.2f} {st[v]:7} {btw[v]:6.3f} {eig[v]:5.2f}")
    for name, fn in (("betweenness", betweenness), ("degree", degree_centrality)):
        print(name, top_by_threshold(ties, nodes, [0, 100, 400], fn))


if __name__ == "__main__":
    main()
