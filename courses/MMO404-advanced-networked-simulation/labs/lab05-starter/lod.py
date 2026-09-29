"""MMO404 Lab 05: error-driven updates and a token-bucket shaper.

    python lod.py --check                  # tests your functions against the week 5 lecture
    python lod.py --hub hub.csv            # seeded 300-entity hub, boss spawns at t = 30 s
    python lod.py --hub hub.csv --shaped   # the same, through a 96 kbit/s shaper
    python lod.py --hub hub.csv --budget 48   # through a shaper of any rate, in kbit/s

Implement every function marked TODO. The model is in the week 5 lecture, sections 2 and 4.
Standard library only.
"""
import csv
import math
import random
import sys

TICK = 0.05          # seconds per tick (20 Hz)
UPDATE_BYTES = 20    # bytes per full update


def smooth_interval(eps, a):
    """Seconds between error-driven updates for smooth motion: sqrt(2 eps / a).
    Return float('inf') when a == 0. TODO."""
    raise NotImplementedError


def guess(sent_pos, sent_vel, dt):
    """Dead-reckoned position dt seconds after an update: pos + vel * dt (2D tuples). TODO."""
    raise NotImplementedError


def needs_update(true_pos, sent_pos, sent_vel, dt, eps):
    """True when the client's guess is more than eps metres from the true position. TODO."""
    raise NotImplementedError


class Shaper:
    """Token bucket with a priority queue that keeps at most one waiting update per entity."""

    def __init__(self, rate, depth):
        self.rate, self.depth = rate, depth
        self.tokens = depth
        self.waiting = {}            # entity id -> (priority, bytes)

    def offer(self, eid, prio, nbytes):
        """Queue an update. A newer update for the same entity replaces the waiting one. TODO."""
        raise NotImplementedError

    def tick(self, dt=TICK):
        """Add rate * dt tokens (capped at depth), then send waiting updates in descending
        priority (ties by lower id) while the next one fits in the tokens. Return the list
        of entity ids sent. TODO."""
        raise NotImplementedError

    def backlog(self):
        return sum(b for _, b in self.waiting.values())


# ---------------------------------------------------------------- hub (given)

BANDS = [("near", 30, 10.0), ("mid", 90, 40.0), ("far", 180, 100.0)]
TIERS = {"near": (1, 20), "mid": (4, 12), "far": (20, 6)}   # every N ticks (20, 5, 1 Hz), bytes
THETA = math.radians(1.0)


def make_hub(seed=5):
    rng = random.Random(seed)
    ents = []
    for band, count, d in BANDS:
        for _ in range(count):
            a = rng.uniform(0, 2 * math.pi)
            ents.append({"band": band, "d": d, "x": d * math.cos(a), "y": d * math.sin(a),
                         "hx": d * math.cos(a), "hy": d * math.sin(a),
                         "h": rng.uniform(0, 2 * math.pi), "speed": 0.0, "turn": 0.0})
    return ents


def behave(ents, rng, t, boss_at):
    """Before boss_at, half the crowd idles and walkers change input about once a second.
    After it, everyone runs and changes input about three times a second. Given."""
    panic = t >= boss_at
    for i, e in enumerate(ents):
        moving = panic or i % 2 == 0
        changes = 3.0 if panic else 1.0
        if not moving:
            e["speed"], e["turn"] = 0.0, 0.0
            continue
        if e["speed"] == 0.0 or rng.random() < changes * TICK:
            e["speed"] = rng.choice([0.0, 3.5, 3.5, 6.0]) if not panic else rng.choice([3.5, 6.0])
            e["turn"] = rng.uniform(-1.5, 1.5) if panic else rng.uniform(-0.6, 0.6)
        if math.hypot(e["x"] - e["hx"], e["y"] - e["hy"]) > 10:
            e["h"] = math.atan2(e["hy"] - e["y"], e["hx"] - e["x"])
        e["h"] += e["turn"] * TICK
        e["x"] += e["speed"] * TICK * math.cos(e["h"])
        e["y"] += e["speed"] * TICK * math.sin(e["h"])


def run_hub(policy, seconds=60, boss_at=30, shaped=False, budget_kbps=96, depth=4000, seed=5):
    """Returns one row per second: bytes sent, mean and max angular error (degrees),
    and shaper backlog. policy is 'tiers' or 'error'. Given, but it calls your code."""
    rng = random.Random(seed + 1)
    ents = make_hub(seed)
    sent = [((e["x"], e["y"]), (0.0, 0.0), 0.0) for e in ents]   # pos, vel, time
    shaper = Shaper(budget_kbps * 1000 / 8, depth) if shaped else None
    rows, sec_bytes, errs = [], 0, []

    def size(i):
        return TIERS[ents[i]["band"]][1] if policy == "tiers" else UPDATE_BYTES

    ticks = int(seconds / TICK)
    for k in range(1, ticks + 1):
        t = k * TICK
        behave(ents, rng, t, boss_at)
        want = []
        for i, e in enumerate(ents):
            pos = (e["x"], e["y"])
            if policy == "tiers":
                due = k % TIERS[e["band"]][0] == 0
            else:
                p, v, ts = sent[i]
                due = needs_update(pos, p, v, t - ts, THETA * e["d"]) or t - ts >= 5.0
            if due:
                want.append(i)
        if shaper:
            for i in want:
                shaper.offer(i, 10.0 / ents[i]["d"], size(i))
            want = shaper.tick()
        for i in want:
            e = ents[i]
            vel = (e["speed"] * math.cos(e["h"]), e["speed"] * math.sin(e["h"]))
            sent[i] = ((e["x"], e["y"]), vel, t)
            sec_bytes += size(i)
        for i, e in enumerate(ents):
            p, v, ts = sent[i]
            g = guess(p, v, t - ts)
            errs.append(math.degrees(math.hypot(e["x"] - g[0], e["y"] - g[1]) / e["d"]))
        if k % 20 == 0:
            rows.append({"second": k // 20, "policy": policy, "shaped": shaped,
                         "kbps": round(sec_bytes * 8 / 1000, 1),
                         "mean_err_deg": round(sum(errs) / len(errs), 3),
                         "max_err_deg": round(max(errs), 2),
                         "backlog_bytes": shaper.backlog() if shaper else 0})
            sec_bytes, errs = 0, []
    return rows


# ---------------------------------------------------------------- checks

def close(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


def check():
    assert close(smooth_interval(0.1745, 2.0), 0.4177), "smooth_interval near band"
    assert smooth_interval(1.0, 0.0) == float("inf"), "no acceleration, no updates"
    assert guess((1.0, 2.0), (3.0, -1.0), 0.5) == (2.5, 1.5), "guess"
    assert needs_update((0.0, 0.3), (0.0, 0.0), (0.0, 0.0), 1.0, 0.2), "needs_update true"
    assert not needs_update((1.0, 0.0), (0.0, 0.0), (2.0, 0.0), 0.5, 0.2), "needs_update false"
    # dead reckoning on a circle: v = 5, R = 10, eps = 0.1 -> interval 0.283 s
    v, R, eps, dt = 5.0, 10.0, 0.1, 0.001
    w, t, sends = v / R, 0.0, 0
    sp, sv, ts = (R, 0.0), (0.0, v), 0.0
    while t < 30.0:
        t += dt
        pos = (R * math.cos(w * t), R * math.sin(w * t))
        if needs_update(pos, sp, sv, t - ts, eps):
            sends += 1
            sp, sv, ts = pos, (-v * math.sin(w * t), v * math.cos(w * t)), t
    assert abs(30.0 / sends - smooth_interval(eps, v * v / R)) < 0.005, "circle interval"
    # shaper: the lecture's burst, 12,000 B/s, depth 2,000, steady 340 B per tick
    s = Shaper(12_000, 2_000)
    s.offer(1, 5.0, 300)
    s.offer(1, 5.0, 100)
    assert s.backlog() == 100, "a newer update replaces the waiting one"
    s.offer(2, 9.0, 1_950)
    assert s.tick() == [2], "highest priority first, stop when the next does not fit"
    assert s.tick() == [1], "the waiting update goes on the next tick"
    print("all checks passed")


def hub(path, shaped, budget):
    rows = (run_hub("tiers", shaped=shaped, budget_kbps=budget)
            + run_hub("error", shaped=shaped, budget_kbps=budget))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for pol in ("tiers", "error"):
        for lo, hi, label in ((5, 30, "quiet"), (35, 60, "panic")):
            rs = [r for r in rows if r["policy"] == pol and lo <= r["second"] < hi]
            kb = sum(r["kbps"] for r in rs) / len(rs)
            me = sum(r["mean_err_deg"] for r in rs) / len(rs)
            mx = max(r["max_err_deg"] for r in rs)
            print(f"{pol:6s} {label:6s} {kb:7.1f} kbit/s  mean error {me:5.2f} deg  worst {mx:6.2f} deg")
    print(f"wrote {path}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--check":
        check()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--hub":
        budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 96.0
        hub(sys.argv[2], "--shaped" in sys.argv or "--budget" in sys.argv, budget)
    else:
        print(__doc__)
