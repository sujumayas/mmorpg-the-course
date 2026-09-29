"""GD201 Lab 10: errand costs, shortcuts and gate slack.

A zone is a weighted, undirected graph stored as an edge list of (a, b, metres).
One node is the hub. Every other node is a destination. See lecture week 10.

Run `python hubs.py` to print a report for the sample zone.
"""
import heapq

# The sample zone: a river valley laid out as a chain from the town (the hub).
SAMPLE_ZONE = [
    ("town", "mill", 120),
    ("mill", "ford", 90),
    ("ford", "orchard", 150),
    ("orchard", "quarry", 110),
    ("quarry", "ruins", 130),
    ("ruins", "tower", 100),
    ("tower", "cave", 140),
]
SAMPLE_HUB = "town"

# Shortcuts the art team says they can build, with their lengths in metres.
CANDIDATE_SHORTCUTS = [
    ("town", "orchard", 260),
    ("town", "ruins", 380),
    ("town", "cave", 420),
    ("mill", "quarry", 250),
    ("ford", "tower", 300),
]

# A gated hub: tokens per spoke, in the order spokes open, and the gate before each.
# Spoke 0 is open from the start, so its gate is 0. The last entry is the final door.
SAMPLE_SPOKES = [10, 10, 10, 10, 10]
SAMPLE_GATES = [0, 5, 15, 25, 35, 40]


def build(edges):
    """Adjacency dict {node: [(neighbour, metres), ...]} from an edge list. Given."""
    g = {}
    for a, b, w in edges:
        g.setdefault(a, []).append((b, w))
        g.setdefault(b, []).append((a, w))
    return g


def shortest(g, start):
    """Dijkstra: shortest distance in metres from start to every reachable node. Given."""
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist


def errand_cost(edges, hub):
    """Mean round trip in metres from the hub to each destination and back:
    E = (2 / n) x sum of shortest(hub, i) over destinations i."""
    # TODO Part A
    raise NotImplementedError("errand_cost")


def pairwise_cost(edges, hub):
    """Mean shortest distance in metres between two different destinations (hub excluded).
    Average over unordered pairs."""
    # TODO Part A
    raise NotImplementedError("pairwise_cost")


def best_shortcut(edges, hub, candidates):
    """Try adding each candidate edge on its own. Return (candidate, new_E) for the one that
    gives the lowest errand cost. Break ties by the order of the candidate list."""
    # TODO Part B
    raise NotImplementedError("best_shortcut")


def gate_slack(spokes, gates):
    """Slack at each gate after the first: available / required, where available is the sum of
    tokens in the spokes open before that gate. Gate k (k >= 1) opens spoke k; the final entry
    in `gates` is the final door, and every spoke is open before it.
    Return a list of floats, one per gate from gates[1] onward."""
    # TODO Part C
    raise NotImplementedError("gate_slack")


def main():
    for name, fn in [
        ("errand cost E", lambda: errand_cost(SAMPLE_ZONE, SAMPLE_HUB)),
        ("pairwise mean", lambda: pairwise_cost(SAMPLE_ZONE, SAMPLE_HUB)),
        ("best shortcut", lambda: best_shortcut(SAMPLE_ZONE, SAMPLE_HUB, CANDIDATE_SHORTCUTS)),
        ("gate slack", lambda: gate_slack(SAMPLE_SPOKES, SAMPLE_GATES)),
    ]:
        try:
            print(f"{name}: {fn()}")
        except NotImplementedError as e:
            print(f"{name}: not implemented yet ({e})")


if __name__ == "__main__":
    main()
