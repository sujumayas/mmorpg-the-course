"""MMO404 Lab 06, part B: find a desync.

    python lockstep.py --check     # runs two "machines" and compares checksums every tick
    python lockstep.py --machine   # (used by --check) runs one machine, prints one checksum per tick

Each machine is a separate Python process started with a different PYTHONHASHSEED, the way
two players' computers would differ. Both run the same commands from the same start.
The simulation below has a determinism bug. Find it with first_divergence, then fix it.
Standard library only.
"""
import hashlib
import os
import struct
import subprocess
import sys

TICKS = 200


def simulate():
    """A 300-unit skirmish in two fleets. Returns one checksum per tick."""
    hp = {f"red{i:03d}": 100.0 for i in range(150)}
    hp.update({f"blue{i:03d}": 100.0 for i in range(150)})
    power = {name: 0.7 + (int(name[-3:]) % 7) * 0.13 for name in hp}
    dealt = {"red": 0.0, "blue": 0.0}          # damage meter shown on the battle report
    sums = []
    for t in range(TICKS):
        alive = {name for name, h in hp.items() if h > 0}
        volley = {"red": 0.0, "blue": 0.0}
        for name in alive:                     # each alive unit fires at the other fleet
            side = "red" if name.startswith("red") else "blue"
            volley[side] += power[name] * (1.0 + (t % 5) * 0.1)
        dealt["red"] += volley["red"]
        dealt["blue"] += volley["blue"]
        for name in alive:                     # damage is shared across the target fleet
            side = "red" if name.startswith("red") else "blue"
            enemy = "blue" if side == "red" else "red"
            share = sum(1 for n in alive if n.startswith(side))
            hp[name] -= volley[enemy] / share * 0.05
        state = struct.pack(f"{len(hp) + 2}d", *(hp[k] for k in sorted(hp)), dealt["red"], dealt["blue"])
        sums.append(hashlib.sha1(state).hexdigest()[:10])
    return sums


def first_divergence(a, b):
    """Index of the first tick where the two checksum lists differ, or None if they never do. TODO."""
    raise NotImplementedError


def run_machine(seed):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    out = subprocess.run([sys.executable, __file__, "--machine"], capture_output=True,
                         text=True, env=env, check=True)
    return out.stdout.split()


def check():
    assert first_divergence(["a", "b", "c"], ["a", "x", "c"]) == 1, "first_divergence"
    assert first_divergence(["a"], ["a"]) is None, "no divergence"
    a, b = run_machine(1), run_machine(2)
    tick = first_divergence(a, b)
    assert tick is None, f"machines desync at tick {tick}: checksums {a[tick]} vs {b[tick]}"
    print("all checks passed")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--machine":
        print("\n".join(simulate()))
    elif len(sys.argv) >= 2 and sys.argv[1] == "--check":
        check()
    else:
        print(__doc__)
