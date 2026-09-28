"""MMO303 Lab 13 starter: event-driven Monte Carlo combat simulator.

It runs as shipped, but every class deals zero damage until you complete
`apply_action`. Standard library only.

    python3 sim.py --class Duelist --seed 1 --iterations 1000 --fight-length 60
"""
import argparse
import heapq
import json
import math
import os
import random
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))


def load_classes(path=os.path.join(HERE, "classes.yaml")):
    """classes.yaml is JSON-style YAML, so json can read it."""
    with open(path) as f:
        data = json.load(f)
    data.pop("_note", None)
    return data


@dataclass
class Action:
    name: str
    cast_time: float


@dataclass
class Actor:
    name: str
    spec: dict                      # one entry from classes.yaml
    rng: random.Random              # one stream per actor
    damage: float = 0.0
    state: dict = field(default_factory=dict)   # buffs, charges, cooldowns


def choose_action(actor, t):
    """TODO step 4: the Ritualist uses Rite at 4 charges. Everyone else hits."""
    return Action("Hit", actor.spec["cast_time"])


def apply_action(actor, action, t, rng):
    """TODO step 1: add base damage, roll a crit with rng.random().
    TODO step 3: Frenzy proc, its 6 s duration and 10 s internal cooldown.
    TODO step 4: Ritualist charges and Rite."""
    pass


def run_fight(actors, fight_length, rng):
    queue = [(0.0, i, "ready") for i in range(len(actors))]
    heapq.heapify(queue)
    while queue:
        t, i, kind = heapq.heappop(queue)
        if t >= fight_length:
            break
        actor = actors[i]
        if kind == "ready":
            action = choose_action(actor, t)
            apply_action(actor, action, t, actor.rng)
            heapq.heappush(queue, (t + action.cast_time, i, "ready"))
        # TODO: handle buff expiry, proc cooldowns
    return {a.name: a.damage / fight_length for a in actors}


def simulate(class_name, fight_length, iterations, seed, spec=None):
    """Run `iterations` fights of one class. Return (mean DPS, sample SD, SE)."""
    spec = spec or load_classes()[class_name]
    master = random.Random(seed)
    results = []
    for _ in range(iterations):
        actor = Actor(class_name, spec, random.Random(master.random()))
        results.append(run_fight([actor], fight_length, actor.rng)[class_name])
    n = len(results)
    mean = sum(results) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in results) / (n - 1)) if n > 1 else 0.0
    return mean, sd, sd / math.sqrt(n)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--class", dest="cls", default="Duelist")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--iterations", type=int, default=1000)
    ap.add_argument("--fight-length", type=float, default=60.0)
    args = ap.parse_args()
    mean, sd, se = simulate(args.cls, args.fight_length, args.iterations, args.seed)
    print(f"{args.cls}: mean {mean:.2f} DPS, SD {sd:.2f}, SE {se:.3f} "
          f"(seed {args.seed}, {args.iterations} fights of {args.fight_length:g} s)")
