"""MMO309 Lab 03: a lag-tolerant movement validator and the detector built on it.

    python movement_validator.py --check          # test your functions against the lecture
    python movement_validator.py --table          # the week 3 lecture's section 2 table
    python movement_validator.py --tune --L 250 --precision 0.9
                                                  # choose k on the supplied session log

The model is the week 3 lecture. Times in ms, distances in metres. Standard library only.
A server tick is TICK_MS. The honest client sends one position per tick; packets take
LATENCY_MS; a lag spike of J ms holds every packet sent during it and releases them together.
"""
import argparse
import math
import random

TICK_MS = 50
SPEED = 6.0                               # legal run speed, m/s
STEP = SPEED * TICK_MS / 1000             # 0.3 m per tick
LATENCY_MS = 40
MAX_RISE = 1.3                            # metres above the last ground contact
MAX_AIR_TICKS = 30                        # 1.5 s airborne before descent is required
MIN_FALL = 0.3                            # metres per tick of descent required after that
BLINK_M = 5.0                             # distance of one blink by a cheater


# ------------------------------------------------------------------ part A: the two checks

def rate_allowed(tol):
    """Rate check: the distance allowed in one tick is one step times (1 + tol). TODO."""
    raise NotImplementedError


def credit_allowed(now_ms, last_ok_ms, lag_tol_ms):
    """Credit check: SPEED times the server time since the last accepted claim,
    capped at TICK_MS + lag_tol_ms. Return metres. TODO."""
    raise NotImplementedError


def simulate(spike_ms, check, param, ticks=60, spike_start=1000):
    """One honest client through one lag spike. check is "rate" (param = tol) or
    "credit" (param = L in ms). Returns (violations, metres pulled back).
    Written for you; it calls your two functions above."""
    arrivals = []
    for k in range(ticks):
        sent = k * TICK_MS
        held = spike_start <= sent < spike_start + spike_ms
        arrivals.append(((spike_start + spike_ms if held else sent) + LATENCY_MS, (k + 1) * STEP))
    accepted, last_ok, violations, pulled = 0.0, 0, 0, 0.0
    for i in range(1, ticks + 3):
        now = i * TICK_MS
        batch = [pos for t, pos in arrivals if now - TICK_MS < t <= now]
        if not batch:
            continue
        d = batch[-1] - pulled - accepted
        allowed = rate_allowed(param) if check == "rate" else credit_allowed(now, last_ok, param)
        if d > allowed + 1e-9:
            violations += 1
            pulled += d - allowed
            d = allowed
        accepted, last_ok = accepted + d, now
    return violations, pulled


def min_setting(spike_ms, check):
    """Smallest setting with zero honest violations for this spike.
    rate: search tol from 0 to 20 in steps of 0.1 and return it as a float.
    credit: search L from 0 to 1000 ms in steps of 10 and return it as an int. TODO."""
    raise NotImplementedError


# ------------------------------------------------------------------ part B: gravity

def gravity_violations(z, grounded):
    """z[i] is the claimed height at tick i; grounded[i] is True when the server's own
    collision says the player stands on something. Return the list of tick indices that
    break either rule:
      1. rise: z[i] is more than MAX_RISE above the height at the last grounded tick;
      2. stall: the player has been airborne for more than MAX_AIR_TICKS consecutive ticks
         and z fell by less than MIN_FALL since the previous tick.
    Tick 0 is always grounded. TODO."""
    raise NotImplementedError


def jump(v0=5.0, ticks=40, start_z=0.0, floor_z=0.0):
    """Heights of an honest jump (or a fall when v0 = 0) under 9.8 m/s^2 gravity,
    landing on floor_z. Written for you."""
    z, grounded = [start_z], [True]
    for i in range(1, ticks):
        t = i * TICK_MS / 1000
        h = start_z + v0 * t - 4.9 * t * t
        z.append(max(h, floor_z))
        grounded.append(h <= floor_z)
    return z, grounded


# ------------------------------------------------------------------ part C: detection

def make_log(players=10000, days=7, cheat_share=0.01, seed=309):
    """The supplied session log, generated the same way every time. Each row is one
    player-day: (player, day, is_cheater, spikes, blinks). spikes is a list of lag-spike
    lengths in ms (count ~ Poisson(6), length ~ exponential, mean 100 ms). blinks is the
    number of 5 m teleports (0 for honest players, ~ Poisson(5) for cheaters).
    Written for you."""
    rng = random.Random(seed)

    def poisson(lam):
        limit, k, p = math.exp(-lam), 0, 1.0
        while True:
            p *= rng.random()
            if p <= limit:
                return k
            k += 1

    rows = []
    for p in range(players):
        cheater = rng.random() < cheat_share
        for d in range(days):
            spikes = [rng.expovariate(1 / 100) for _ in range(poisson(6))]
            blinks = poisson(5) if cheater else 0
            rows.append((p, d, cheater, spikes, blinks))
    return rows


def violations(row, lag_tol_ms):
    """Violations one player-day produces under the credit check with lag tolerance L:
    every spike longer than L, plus every blink if BLINK_M is more than the largest
    jump SPEED * (TICK_MS + L) / 1000. TODO."""
    raise NotImplementedError


def flag_stats(log, lag_tol_ms, k, window_days=1):
    """Flag a player when their violations summed over the first window_days days reach k.
    Count per player (not per day). Return (tp, fp, fn, tn). TODO."""
    raise NotImplementedError


def best_k(log, lag_tol_ms, min_precision, window_days=1):
    """The smallest k from 1 to 60 whose precision tp / (tp + fp) is at least
    min_precision (a k that flags nobody does not count). Return (k, precision, recall),
    or None if no k qualifies. TODO."""
    raise NotImplementedError


# ------------------------------------------------------------------ checks and reports

def check():
    log = make_log()
    z_jump, g_jump = jump()
    z_fall, g_fall = jump(v0=0.0, ticks=50, start_z=20.0)
    z_fly = [0.0] + [0.2 * i for i in range(1, 12)]
    z_hover = jump(ticks=12)[0] + [1.2 - 0.02 * i for i in range(1, 40)]
    tests = [
        ("rate allowed, tol 0.5", lambda: round(rate_allowed(0.5), 6), 0.45),
        ("credit allowed, long gap capped", lambda: round(credit_allowed(2000, 1000, 250), 6), 1.8),
        ("credit allowed, one tick", lambda: round(credit_allowed(1050, 1000, 250), 6), 0.3),
        ("min tol for 250 ms", lambda: min_setting(250, "rate"), 5.0),
        ("min L for each spike", lambda: [min_setting(j, "credit") for j in (50, 100, 250, 500)],
         [50, 100, 250, 500]),
        ("500 ms spike at L = 250", lambda: tuple(round(x, 6) for x in simulate(500, "credit", 250)),
         (1, 1.5)),
        ("honest jump passes", lambda: gravity_violations(z_jump, g_jump), []),
        ("cliff fall passes", lambda: gravity_violations(z_fall, g_fall), []),
        ("fly hack caught at tick 7", lambda: gravity_violations(z_fly, [True] + [False] * 11)[:1], [7]),
        ("hover hack caught at tick 31", lambda: gravity_violations(z_hover, [True] + [False] * 50)[:1],
         [31]),
        ("honest violations in the log, L = 250", lambda: sum(violations(r, 250) for r in log if not r[2]), 34231),
        ("cheater violations in the log, L = 800", lambda: sum(violations(r, 800) for r in log if r[2]), 1),
        ("one-day stats, L = 250, k = 3", lambda: flag_stats(log, 250, 3), (92, 136, 5, 9767)),
        ("best k, one day, 90%", lambda: best_k(log, 250, 0.9)[0], 5),
        ("best k, seven days, 99%", lambda: best_k(log, 250, 0.99, 7)[0], 13),
    ]
    failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
        except NotImplementedError:
            got = "not implemented yet"
        except TypeError as exc:
            got = f"error: {exc}"
        if got != expected:
            failed += 1
            print(f"FAIL {name}: expected {expected}, got {got}")
        else:
            print(f"ok   {name}")
    print("all checks passed" if not failed else f"{failed} check(s) failed")
    return failed == 0


def table():
    for j in (50, 100, 250, 500):
        tol, lag = min_setting(j, "rate"), min_setting(j, "credit")
        print(f"spike {j:3} ms | rate: tol {tol:5.0%}, cheater {SPEED * (1 + tol):2.0f} m/s"
              f" | credit: L {lag:3} ms, largest jump {SPEED * (TICK_MS + lag) / 1000:.1f} m")


def tune(lag_tol_ms, min_precision):
    log = make_log()
    for window in (1, 7):
        print(f"window {window} day(s), L = {lag_tol_ms} ms")
        for k in range(1, 16):
            tp, fp, fn, tn = flag_stats(log, lag_tol_ms, k, window)
            prec = tp / (tp + fp) if tp + fp else float("nan")
            print(f"  k={k:2}  tp {tp:3}  fp {fp:5}  fn {fn:3}  precision {prec:6.1%}  recall {tp / (tp + fn):6.1%}")
        print("  best:", best_k(log, lag_tol_ms, min_precision, window))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--tune", action="store_true")
    ap.add_argument("--L", type=int, default=250)
    ap.add_argument("--precision", type=float, default=0.9)
    args = ap.parse_args()
    if args.table:
        table()
    elif args.tune:
        tune(args.L, args.precision)
    else:
        raise SystemExit(0 if check() else 1)
