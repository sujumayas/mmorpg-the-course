"""MMO305 Lab 01 starter: load the server network and measure reach.

Standard library only. Run from this folder:  python3 netlib.py

You write:
  - ei_index(edges, guild_of)
  - find_brokers(players, edges)
The loaders and reach() are done for you.
"""
import csv
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load():
    """Return (players, guild_of, edges). edges is a list of (a, b) tuples."""
    guild_of = {}
    with open(HERE / "players.csv", newline="") as f:
        for row in csv.DictReader(f):
            guild_of[row["player"]] = row["guild"]
    players = list(guild_of)
    edges = []
    with open(HERE / "server-ties.csv", newline="") as f:
        for row in csv.DictReader(f):
            edges.append((row["a"], row["b"]))
    return players, guild_of, edges


def reach(players, edges, removed=()):
    """Return (connected_pairs, all_pairs, average_steps) among players not in `removed`.

    connected_pairs counts unordered pairs joined by some path.
    average_steps is the mean shortest-path length over connected pairs.
    """
    removed = set(removed)
    alive = [p for p in players if p not in removed]
    adj = {p: set() for p in alive}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)
    connected = 0
    total_steps = 0
    for s in alive:
        dist = {s: 0}
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        for t in alive:
            if t > s and t in dist:
                connected += 1
                total_steps += dist[t]
    all_pairs = len(alive) * (len(alive) - 1) // 2
    avg = total_steps / connected if connected else float("nan")
    return connected, all_pairs, avg


def ei_index(edges, guild_of):
    """TODO: return (I, E, (E - I) / (E + I))."""
    raise NotImplementedError


def find_brokers(players, edges):
    """TODO: return a list of (player, connected_pairs_after, all_pairs_after)
    for every player whose removal leaves some remaining pair disconnected."""
    raise NotImplementedError


if __name__ == "__main__":
    players, guild_of, edges = load()
    c, p, avg = reach(players, edges)
    print(f"{len(players)} players, {len(edges)} ties")
    print(f"reach {c} of {p} ({c / p:.1%}), average steps {avg:.2f}")
