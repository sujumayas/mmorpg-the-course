"""MMO404 Lab 02, part B: what does a seam cost, and how wide should the hysteresis band be?

    python seam.py --check          # tests your functions against the week 2 lecture
    python seam.py --sweep out.csv  # handoffs, ghosts and cost for w = 0..60 m

The walker simulation is given. You write the ownership rule and the cost model.
The model is in the week 2 lecture, section 2. Standard library only.
"""
import csv
import math
import random
import sys

E_H = 1.0      # CPU milliseconds per handoff, both servers together
C_G = 0.003    # CPU milliseconds per ghost per tick
TICK_HZ = 10
R = 100.0      # AOI radius, metres
L = 500.0      # border length, metres
BAND = 200.0   # the simulation covers |x| <= BAND on both sides of the border


def update_owner(x, on_b, w):
    """Ownership after this tick. on_b is True if server B (east, x > 0) owns the player.
    Move to B only when x > w/2, back to A only when x < -w/2.
    Return (new_on_b, changed). TODO."""
    raise NotImplementedError


def ghost_count(rho, length, radius, w):
    """Entities mirrored across the seam, both directions: 2 * rho * length * (radius + w). TODO."""
    raise NotImplementedError


def seam_cost_ms_per_s(handoffs_per_s, ghosts, e_h=E_H, c_g=C_G, tick_hz=TICK_HZ):
    """CPU milliseconds per second spent on the seam: handoffs * e_h + ghosts * tick_hz * c_g. TODO."""
    raise NotImplementedError


def handoffs_per_s(w, travellers=100, dwellers=300, band=BAND, dt=0.1, seconds=300, seed=4):
    """Given. Travellers walk straight across at 5 m/s and rarely turn back. Dwellers mill
    around a fixed spot with a 4 m spread (a fight, a vendor, a resource node)."""
    rng = random.Random(seed)
    tx = [rng.uniform(-band, band) for _ in range(travellers)]
    tv = [rng.choice((-5.0, 5.0)) for _ in range(travellers)]
    anchors = [rng.uniform(-band, band) for _ in range(dwellers)]
    dx = anchors[:]
    on_b = [x > 0 for x in tx + dx]
    count = 0
    for _ in range(int(seconds / dt)):
        for i in range(travellers):
            if rng.random() < 0.05 * dt:
                tv[i] = -tv[i]
            tx[i] += tv[i] * dt
            if abs(tx[i]) > band:
                tv[i] = -tv[i]
        for i in range(dwellers):
            dx[i] += 0.5 * (anchors[i] - dx[i]) * dt + 4.0 * math.sqrt(dt) * rng.gauss(0, 1)
        for i, x in enumerate(tx + dx):
            on_b[i], changed = update_owner(x, on_b[i], w)
            count += changed
    return count / seconds


def density(travellers=100, dwellers=300, band=BAND, length=L):
    return (travellers + dwellers) / (2 * band * length)


def check():
    assert update_owner(0.5, False, 0.0) == (True, True)
    assert update_owner(0.5, False, 2.0) == (False, False)
    assert update_owner(-0.5, True, 2.0) == (True, False)
    assert update_owner(-1.5, True, 2.0) == (False, True)
    rho = density()
    assert abs(rho - 0.002) < 1e-12
    assert abs(ghost_count(rho, L, R, 0) - 200) < 1e-9
    assert abs(ghost_count(rho, L, R, 20) - 240) < 1e-9
    assert abs(seam_cost_ms_per_s(9.25, 200) - 15.25) < 1e-9
    for w, want in ((0, 9.25), (10, 1.62), (40, 0.94)):
        got = handoffs_per_s(w)
        assert abs(got - want) < 0.01, f"handoffs_per_s({w}) = {got:.2f}, lecture says {want}"
    print("all checks passed")


def sweep(path):
    rho = density()
    with open(path, "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["w", "handoffs_per_s", "ghosts", "cost_ms_per_s"])
        for w in (0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60):
            h = handoffs_per_s(w)
            g = ghost_count(rho, L, R, w)
            out.writerow([w, round(h, 2), round(g, 1), round(seam_cost_ms_per_s(h, g), 2)])
    print("wrote", path)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--sweep" in sys.argv:
        sweep(sys.argv[sys.argv.index("--sweep") + 1])
    else:
        print(__doc__)
