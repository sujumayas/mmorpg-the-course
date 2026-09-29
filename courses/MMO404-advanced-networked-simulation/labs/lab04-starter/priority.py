"""MMO404 Lab 04: a replication priority allocator.

    python priority.py --check                 # tests your functions against the week 4 lecture
    python priority.py --scene out.csv         # runs the seeded 400-entity scene under three falloffs
    python priority.py --scene out.csv --speed # the same, with the speed term in the priority

Implement every function marked TODO. The model is in the week 4 lecture, sections 2 and 3.
Standard library only.
"""
import csv
import math
import random
import sys

D0 = 10.0      # metres; the falloff is flat inside this distance
TICK = 0.05    # seconds per tick (20 Hz)


def falloff(d, kind="inverse", d0=D0):
    """Distance term f(d). kind is 'inverse' (d0 / max(d, d0)), 'square' (that value squared)
    or 'flat' (always 1). TODO."""
    raise NotImplementedError


def priority(weight, d, kind="inverse", d0=D0):
    """p = weight * f(d). TODO."""
    raise NotImplementedError


def priority_speed(weight, d, speed, kind="inverse", d0=D0, v0=3.0):
    """Lecture section 3: p = weight * f(d) * (1 + speed / v0). The viewer is standing
    still in this lab, so relative speed is the entity's own speed. TODO."""
    raise NotImplementedError


def fair_rates(prios, budget):
    """Water-filling. Return (rates, lam) with rate_i = min(1, lam * p_i) and sum(rates) == budget.
    Entities with priority 0 get rate 0. If budget >= number of positive priorities, every
    positive entity gets rate 1 and lam is float('inf'). TODO."""
    raise NotImplementedError


class Accumulator:
    """Priority accumulator (CS202 week 13, section 4; MMO404 week 4, section 3)."""

    def __init__(self, n):
        self.acc = [0.0] * n

    def pick(self, prios, budget):
        """Add each priority to its running total, choose the `budget` largest totals
        (ties broken by lower index), reset the chosen totals to 0 and return their
        indices in the order chosen. TODO."""
        raise NotImplementedError


# ---------------------------------------------------------------- scene (given)

CLASSES = {  # name: (count, weight, speed m/s, ring radius m)
    "target": (1, 4.0, 7.0, 10.0),
    "party": (8, 2.0, 7.0, 12.0),
    "enemies": (40, 2.0, 7.0, 25.0),
    "npcs": (120, 1.0, 3.0, 45.0),
    "far players": (100, 2.0, 7.0, 75.0),
    "loot": (131, 0.5, 0.0, 60.0),
}


def make_scene(seed=4):
    """400 entities around a viewer at the origin. Each has a class, a position and a
    heading. Given."""
    rng = random.Random(seed)
    ents = []
    for name, (count, w, v, ring) in CLASSES.items():
        for _ in range(count):
            r = max(2.0, rng.gauss(ring, ring * 0.25))
            a = rng.uniform(0, 2 * math.pi)
            x, y = r * math.cos(a), r * math.sin(a)
            ents.append({"cls": name, "w": w, "v": v, "x": x, "y": y, "hx": x, "hy": y,
                         "h": rng.uniform(0, 2 * math.pi)})
    return ents


def step(ents, rng):
    """Move every entity one tick. Headings wander, and anyone more than 8 m from
    home turns back toward it, so the crowd keeps its shape. Given."""
    for e in ents:
        if math.hypot(e["x"] - e["hx"], e["y"] - e["hy"]) > 8.0:
            e["h"] = math.atan2(e["hy"] - e["y"], e["hx"] - e["x"])
        e["h"] += rng.gauss(0, 0.2)
        e["x"] += e["v"] * TICK * math.cos(e["h"])
        e["y"] += e["v"] * TICK * math.sin(e["h"])


def run_scene(kind, budget=20, ticks=1000, seed=4, use_speed=False):
    """Run the scene with the accumulator. Returns per-class mean interval (ticks) and
    mean angular error (degrees) between the client's last received position and the
    true position. Given, but it calls your functions."""
    rng = random.Random(seed + 1)
    ents = make_scene(seed)
    seen = [(e["x"], e["y"]) for e in ents]
    last = [0] * len(ents)
    gaps = {c: [] for c in CLASSES}
    err = {c: [] for c in CLASSES}
    accum = Accumulator(len(ents))
    for t in range(1, ticks + 1):
        step(ents, rng)
        if use_speed:
            prios = [priority_speed(e["w"], math.hypot(e["x"], e["y"]), e["v"], kind) for e in ents]
        else:
            prios = [priority(e["w"], math.hypot(e["x"], e["y"]), kind) for e in ents]
        for i in accum.pick(prios, budget):
            gaps[ents[i]["cls"]].append(t - last[i])
            last[i] = t
            seen[i] = (ents[i]["x"], ents[i]["y"])
        if t > 100:
            for i, e in enumerate(ents):
                d = max(math.hypot(e["x"], e["y"]), 1.0)
                drift = math.hypot(e["x"] - seen[i][0], e["y"] - seen[i][1])
                err[e["cls"]].append(math.degrees(drift / d))
    out = {}
    for c in CLASSES:
        g = gaps[c]
        out[c] = (sum(g) / len(g) if g else float("inf"), sum(err[c]) / len(err[c]))
    return out


# ---------------------------------------------------------------- checks

def close(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


def check():
    assert close(falloff(5), 1.0) and close(falloff(40), 0.25), "falloff inverse"
    assert close(falloff(40, "square"), 0.0625), "falloff square"
    assert close(falloff(500, "flat"), 1.0), "falloff flat"
    assert close(priority(2, 80), 0.25), "priority"
    assert close(priority_speed(2, 20, 6), 3.0) and close(priority_speed(1, 5, 0), 1.0), "priority_speed"
    # lecture section 2 table
    groups = [(1, 4, 10), (8, 2, 10), (16, 2, 20), (32, 1, 40), (64, 2, 80), (128, 0.5, 80)]
    prios = []
    for count, w, d in groups:
        prios += [priority(w, d)] * count
    rates, lam = fair_rates(prios, 20)
    assert close(lam, 19 / 64), f"lambda {lam}"
    assert close(rates[0], 1.0) and close(rates[1], 0.59375), "target and party rates"
    assert close(sum(rates), 20), "rates must sum to the budget"
    # check-yourself question 1
    r2, lam2 = fair_rates([3] * 4 + [0.5] * 40, 12)
    assert close(lam2, 0.4) and close(r2[-1], 0.2), "check-yourself 1"
    r3, lam3 = fair_rates([1, 0, 2], 5)
    assert r3 == [1.0, 0.0, 1.0] and lam3 == float("inf"), "budget larger than the set"
    # accumulator, lecture section 3
    acc = Accumulator(len(prios))
    sends = [0] * len(prios)
    for _ in range(2000):
        for i in acc.pick(prios, 20):
            sends[i] += 1
    assert sends[0] >= 1990, "the target is sent on almost every tick"
    assert 990 <= sends[1] <= 1010, "party members about every 2 ticks"
    assert 2000 * 20 == sum(sends), "every slot is used"
    acc2 = Accumulator(3)
    assert acc2.pick([1, 1, 1], 2) == [0, 1], "ties go to the lower index"
    assert acc2.pick([1, 1, 1], 2) == [2, 0], "the waiting entity wins next"
    print("all checks passed")


def scene(path, use_speed=False):
    rows = []
    for kind in ("inverse", "square", "flat"):
        res = run_scene(kind, use_speed=use_speed)
        for c, (gap, ang) in res.items():
            rows.append({"falloff": kind, "speed_term": use_speed, "class": c, "interval_ticks": round(gap, 2),
                         "angle_deg": round(ang, 2)})
            print(f"{kind:8s} {c:12s} every {gap:6.2f} ticks  error {ang:5.2f} deg")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--check":
        check()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--scene":
        scene(sys.argv[2], use_speed="--speed" in sys.argv)
    else:
        print(__doc__)
