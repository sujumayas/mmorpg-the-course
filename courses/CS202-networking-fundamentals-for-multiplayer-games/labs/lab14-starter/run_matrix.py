"""CS202 Lab 14: run the toy client under every network profile and several seeds.

    python run_matrix.py                               # all profiles, 10 seeds, 60 s each
    python run_matrix.py --seeds 20 --seconds 120
    python run_matrix.py --repro evening_wifi 4        # replay one run and explain the failure
    python run_matrix.py --profiles my_profiles.json

A run fails if the client throws an exception, if its server_tick ever goes backwards,
if the drawn entity moves more than
TELEPORT_M in one frame (its real speed allows about 0.1 m per frame), or if it is drawn
more than MAX_ERROR_M from where the server says it was at the render time. The offline
simulation knows the truth, which a live test never does.
Standard library only.
"""
import argparse
import json
import math
import os

from conditioner import Conditioner, burst_lengths, reorder_count
from toy_client import INTERP_MS, SEND_HZ, Client, Snapshot, server_position

FRAME_HZ = 60
TELEPORT_M = 2.0
MAX_ERROR_M = 1.0
HERE = os.path.dirname(os.path.abspath(__file__))


def run_once(profile, seed, seconds, verbose=False):
    """Simulate one run. Returns (first_failure_s or None, note, stats)."""
    sends = [i * 1000.0 / SEND_HZ for i in range(int(seconds * SEND_HZ))]
    cond = Conditioner(profile["delay_ms"], profile["jitter_ms"], profile["p"], profile["q"],
                       profile.get("dup", 0.0), seed)
    arrivals, lost = cond.run(sends)
    stats = {"lost": sum(lost), "longest_burst": max(burst_lengths(lost), default=0),
             "reordered": reorder_count([s for _, s in arrivals])}
    client, last_pos, last_tick, j = Client(), None, -1, 0
    base = profile["delay_ms"]            # assume clocks are synced to the base delay
    for f in range(int(seconds * FRAME_HZ)):
        now = f * 1000.0 / FRAME_HZ
        while j < len(arrivals) and arrivals[j][0] <= now:
            seq = arrivals[j][1]
            client.on_receive(Snapshot(seq, sends[seq], server_position(sends[seq])))
            j += 1
            if client.server_tick < last_tick:
                return now / 1000, (f"server_tick went back from {last_tick} to "
                                    f"{client.server_tick}"), stats
            last_tick = client.server_tick
        render = now - base - INTERP_MS
        try:
            pos = client.sample(render)
        except Exception as e:  # a crash is a failure too
            return now / 1000, f"{type(e).__name__}: {e} (branch {client.branch})", stats
        if pos is None:
            continue
        if last_pos is not None:
            step = math.dist(pos, last_pos)
            if step > TELEPORT_M:
                recent = [s for t, s in arrivals[max(0, j - 6):j]]
                note = (f"moved {step:.1f} m in one frame, branch {client.branch}, "
                        f"last arrivals (seq) {recent}")
                return now / 1000, note, stats
        err = math.dist(pos, server_position(render))
        if err > MAX_ERROR_M:
            return now / 1000, f"drawn {err:.2f} m from the truth, branch {client.branch}", stats
        last_pos = pos
    return None, "", stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", default=os.path.join(HERE, "profiles.json"))
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--repro", nargs=2, metavar=("PROFILE", "SEED"))
    a = ap.parse_args()
    with open(a.profiles) as fh:
        profiles = json.load(fh)
    if a.repro:
        name, seed = a.repro[0], int(a.repro[1])
        t, note, stats = run_once(profiles[name], seed, a.seconds)
        print(f"{name} seed {seed}: lost {stats['lost']}, longest burst {stats['longest_burst']}, "
              f"reordered {stats['reordered']}")
        print(f"first failure at {t:.2f} s: {note}" if t is not None else "no failure")
        return
    print(f"{'profile':<18}{'seeds':>6}{'fails':>6}{'first failure (s)':>19}  replay")
    for name, prof in profiles.items():
        fails = []
        for seed in range(1, a.seeds + 1):
            t, _, _ = run_once(prof, seed, a.seconds)
            if t is not None:
                fails.append((t, seed))
        if fails:
            t, seed = min(fails)
            print(f"{name:<18}{a.seeds:>6}{len(fails):>6}{t:>19.1f}  "
                  f"python run_matrix.py --repro {name} {seed}")
        else:
            print(f"{name:<18}{a.seeds:>6}{0:>6}{'-':>19}")


if __name__ == "__main__":
    main()
