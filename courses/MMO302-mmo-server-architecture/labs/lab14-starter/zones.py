"""MMO302 Lab 14: one hour of recorded tick times (ms) for 12 zones at 20 Hz.

Do not edit. The data are generated deterministically so everyone gets the same numbers.
Each zone has its own character; part of the lab is finding out which is which.
"""
HZ = 20
TICKS = 60 * 60 * HZ          # one hour
ZONES = ["meadow-01", "hills-02", "forge-03", "crypt-04", "market-05", "coast-06",
         "harbor-07", "keep-08", "marsh-09", "arena-10", "docks-11", "spire-12"]


def _lcg(seed):
    state = seed
    while True:
        state = (1103515245 * state + 12345) % 2**31
        yield state / 2**31


def zone_ticks(name):
    i = ZONES.index(name)
    rnd = _lcg(1000 + i)
    base = 14 + i % 5                      # ordinary zones: 14-18 ms typical
    if name == "forge-03":
        base = 36                          # busy zone: high mean, but under budget
    out = []
    t = 0
    while t < TICKS:
        v = base + int(next(rnd) * 9) - 4  # base-4 .. base+4
        if name == "harbor-07" and t % 1500 == 700:
            out.extend([120, 118, 125, 121])   # clustered GC pauses
            t += 4
            continue
        if name == "docks-11" and 30_000 <= t < 30_006:
            v = 95                              # one short burst during a world event
        if next(rnd) < 0.0002:
            v = 70                              # rare isolated hitch, every zone
        out.append(v)
        t += 1
    return out[:TICKS]


def all_zones():
    return {z: zone_ticks(z) for z in ZONES}
