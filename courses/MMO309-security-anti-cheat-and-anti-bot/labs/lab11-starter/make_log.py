"""MMO309 Lab 11: incident log generator. Do not edit.

incident_log(seed=11) returns the item log of a new dupe, as your ledger would show it
T_OBS = 4 hours after the exploit began. One row per duplicated serial:
    (serial, hour_left, destination)
hour_left is the hour the item left the ring (None if it is still in the ring's accounts),
destination is "bought" (now in an honest player's bag) or "gone" (vendored or crafted),
or None while the item is still held. The true k and b are hidden in this file; estimate
them from the rows, not by reading the constants.
"""
import random

T_OBS = 4.0
_D, _K, _B = 20_000, 0.15, 0.7


def incident_log(seed=11):
    rng = random.Random(seed)
    rows = []
    for serial in range(_D):
        t = rng.expovariate(_K)
        if t < T_OBS:
            dest = "bought" if rng.random() < _B else "gone"
            rows.append((serial, round(t, 4), dest))
        else:
            rows.append((serial, None, None))
    return rows
