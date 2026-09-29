"""MMO404 lab 09 starter: meshing a crowd, and authority with epochs.

    python test_mesh.py                  # checks your functions against the week 9 lecture
    python mesh.py --table               # section 2's table
    python mesh.py --curves out.csv      # crowd and spread capacity for k = 1..1024
    python mesh.py --pause               # section 3's paused-server scenario

Implement every function and method marked TODO. The model is in the week 9 lecture,
sections 2 and 3. Standard library only.
"""
import csv
import sys

C_P = 20e-6      # CPU s per owned player per tick
C_I = 2e-6       # CPU s per interacting ordered pair per tick
C_G = 4e-6       # CPU s per ghost per tick
BUDGET = 0.050   # usable CPU s per tick
KS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]


def tick_ms(n, k):
    """Crowd mode: c_p*n/k + c_i*n*n/k + c_g*n*(1 - 1/k), in milliseconds. TODO."""
    raise NotImplementedError("tick_ms")


def capacity(k):
    """Crowd mode: the positive root of (c_i/k) N^2 + (c_p/k + c_g(1 - 1/k)) N - BUDGET = 0.
    Return a float. TODO."""
    raise NotImplementedError("capacity")


def servers_for(n, k_max=100_000):
    """Fewest k (integer) with tick_ms(n, k) <= 50, or None if none up to k_max. TODO."""
    raise NotImplementedError("servers_for")


def ghost_updates(n, k):
    """Crowd mode: ghost updates the replication layer delivers per tick, n*(k - 1). TODO."""
    raise NotImplementedError("ghost_updates")


def spread_tick_ms(n, k, m=30):
    """Spread mode: each player interacts with min(n, m) others; each server ghosts
    min(n*(1 - 1/k), 2*m) players.
    c_p*n/k + c_i*(n/k)*min(n, m) + c_g*ghosts, in milliseconds. TODO."""
    raise NotImplementedError("spread_tick_ms")


def spread_capacity(k, m=30):
    """Spread mode: largest n (float, to 0.01) with spread_tick_ms(n, k, m) <= 50.
    Bisection on [1, 1e6]. TODO."""
    raise NotImplementedError("spread_capacity")


class AuthorityTable:
    """The replication layer's record of who owns each entity, with epochs as fencing tokens."""

    def __init__(self):
        self.records = {}   # entity -> {"owner": str, "epoch": int, "state": object}
        self.log = []       # strings, one per event, for your report

    def grant(self, entity, server):
        """Make `server` the owner of `entity` and return the new epoch.
        The first grant for an entity is epoch 1; every later grant adds 1.
        Keep the entity's current state. TODO."""
        raise NotImplementedError("grant")

    def write(self, entity, server, epoch, state):
        """Accept the write (store state, return True) only if `server` is the recorded
        owner and `epoch` equals the recorded epoch. Otherwise return False.
        Append a line to self.log either way. TODO."""
        raise NotImplementedError("write")

    def owner(self, entity):
        """Recorded owner of entity, or None. TODO."""
        raise NotImplementedError("owner")

    def state(self, entity):
        """Last accepted state of entity, or None. TODO."""
        raise NotImplementedError("state")


def pause_scenario():
    """Section 3's table: A pauses, B takes over, A's late write must be rejected. Given."""
    t = AuthorityTable()
    for _ in range(7):
        e = t.grant(12, "A")          # epochs 1..7, as if authority had moved back and forth
    t.write(12, "A", e, {"hp": 100})
    a_epoch = e                       # A pauses holding epoch 7
    b_epoch = t.grant(12, "B")        # epoch 8
    t.write(12, "B", b_epoch, {"hp": 80})
    late = t.write(12, "A", a_epoch, {"hp": 100})
    return t, late


def table():
    print(" k   crowd   vs k=1   tick at 1,000   ghost updates per tick")
    for k in (1, 2, 4, 16, 64, 256):
        n = capacity(k)
        print(f"{k:3d}  {n:6.0f}   {n / capacity(1):5.2f}x   {tick_ms(1000, k):9.1f} ms"
              f"   {ghost_updates(n, k):12,.0f}")


def curves(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["k", "crowd_capacity", "spread_capacity"])
        for k in KS:
            w.writerow([k, round(capacity(k), 1), round(spread_capacity(k), 1)])
    print("wrote", path)


if __name__ == "__main__":
    if "--table" in sys.argv:
        table()
    elif "--curves" in sys.argv:
        curves(sys.argv[sys.argv.index("--curves") + 1])
    elif "--pause" in sys.argv:
        t, late = pause_scenario()
        print("\n".join(t.log))
        print("late write accepted?", late, "| final state", t.state(12), "| owner", t.owner(12))
    else:
        print(__doc__)
