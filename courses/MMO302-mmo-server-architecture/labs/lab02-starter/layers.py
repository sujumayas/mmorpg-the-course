"""MMO302 lab 02: assigning players to layers (week 2 lecture, section 2).

Run:
    python layers.py                 # compare both policies at L = 20, cap 180
    python layers.py --layers 10 --cap 330

Standard library only. Every random choice uses mulberry32, so results are
identical on every machine (and match the week 3 interactive's generator).
"""
import argparse
from collections import Counter, defaultdict


def mulberry32(seed):
    """Deterministic uniform [0, 1) generator, same as the JavaScript original."""
    a = seed & 0xFFFFFFFF

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def make_population(n=3000, guilded_share=0.6, seed=302):
    """Return (arrival_order, guild_of). guild_of[p] is a guild id or None.
    The first guilded_share of player ids are cut into guilds of 5 to 25
    members; the rest are solo. Arrival order is a Fisher-Yates shuffle."""
    rnd = mulberry32(seed)
    guild_of = [None] * n
    limit = int(n * guilded_share)
    p, gid = 0, 0
    while p < limit:
        size = 5 + int(rnd() * 21)
        for q in range(p, min(p + size, limit)):
            guild_of[q] = gid
        p += size
        gid += 1
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = int(rnd() * (i + 1))
        order[i], order[j] = order[j], order[i]
    return order, guild_of


def assign_random(order, guild_of, layers, cap, seed=7):
    """Each arriving player picks a uniformly random layer that has room.
    Draw r = rnd(); open = sorted list of layers with load < cap;
    choose open[int(r * len(open))]. Returns layer_of (dict player -> layer)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def assign_guild(order, guild_of, layers, cap):
    """Guild-aware placement. If the player has a guild with members already
    placed, pick the layer holding the most of them that still has room
    (ties: lowest layer index). Otherwise, or if none of those layers has
    room, pick the least-loaded layer (ties: lowest index)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def cohesion(layer_of, guild_of):
    """Share of same-guild pairs of players who are on the same layer."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


# ---- provided below this line -------------------------------------------

def quest_time(layer_of, share=0.10, spawns=30, respawn=60, q=2.0, kills=10):
    """Average quest time (minutes) over all players, per the lecture's model,
    with each layer's contention computed from its own population."""
    supply = spawns * 60 / respawn
    loads = Counter(layer_of.values())
    total = 0.0
    for layer, n in loads.items():
        rate = min(q, supply / (share * n)) if n else q
        total += n * kills / rate
    return total / len(layer_of)


def report(name, layer_of, guild_of):
    loads = Counter(layer_of.values())
    meet = sum(loads[layer_of[p]] - 1 for p in layer_of) / len(layer_of)
    print(f"{name:>7}: largest layer {max(loads.values()):>4}, smallest {min(loads.values()):>4}, "
          f"cohesion {cohesion(layer_of, guild_of):6.1%}, avg quest {quest_time(layer_of):5.2f} min, "
          f"avg meetable {meet:6.1f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", type=int, default=20)
    ap.add_argument("--cap", type=int, default=180)
    ap.add_argument("--players", type=int, default=3000)
    a = ap.parse_args()
    order, guild_of = make_population(a.players)
    report("random", assign_random(order, guild_of, a.layers, a.cap), guild_of)
    report("guild", assign_guild(order, guild_of, a.layers, a.cap), guild_of)
