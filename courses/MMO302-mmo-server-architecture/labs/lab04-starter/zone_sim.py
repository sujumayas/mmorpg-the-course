"""MMO302 lab 04: zone servers and handoff (week 4 lecture).

Run:
    python zone_sim.py --table          # formula table for the lecture's shard
    python zone_sim.py --simulate 4     # random-walk shard on a 4 x 4 grid, measured vs predicted
    python zone_sim.py --idle           # 40 idle players on a border, handoffs vs hysteresis band

Standard library only. Fill in every function marked TODO, then run test_zone_sim.py.
"""
import argparse
import math
import random


# ---------------------------------------------------------------- the model

def handoff_rate(n, world, speed, g):
    """Predicted handoffs per second, both directions: (2/pi) * rho * v * L,
    with rho = n / world**2 and L = 2 * world * (g - 1)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def ghost_fraction(world, radius, g):
    """Share of evenly spread players within `radius` of a border: 2 * R * L / world**2."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def busiest_zone(n, f, g):
    """Players in the busiest zone when a fraction f of n sits in one city inside one zone
    and the rest are spread evenly over g*g zones: f*n + (1 - f)*n / g**2."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


# ---------------------------------------------------------------- ownership

def zone_of(x, y, world, g):
    """(column, row) of the zone containing the point. Provided."""
    size = world / g
    return (min(int(x // size), g - 1), min(int(y // size), g - 1))


def next_owner(owner, x, y, world, g, h):
    """Return the zone that should own an entity at (x, y) whose current owner is `owner`.

    Hysteresis rule from the lecture: keep the current owner while the entity is inside the
    owner's zone grown by h/2 metres on every side. Once it leaves that grown square, the
    owner becomes the zone that contains the point. With h = 0 this is plain zone_of."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


# ---------------------------------------------------------------- simulations (provided)

def simulate(n, world, speed, g, h=0.0, seconds=600, seed=1, turn_p=0.02):
    """Random walk on a torus, one step per simulated second. Returns measured handoffs/s.
    Moves that wrap around the world edge are not counted (they are not real borders)."""
    rnd = random.Random(seed)
    xs = [rnd.random() * world for _ in range(n)]
    ys = [rnd.random() * world for _ in range(n)]
    th = [rnd.random() * 2 * math.pi for _ in range(n)]
    own = [zone_of(xs[i], ys[i], world, g) for i in range(n)]
    handoffs = 0
    for _ in range(seconds):
        for i in range(n):
            if rnd.random() < turn_p:
                th[i] = rnd.random() * 2 * math.pi
            nx = xs[i] + speed * math.cos(th[i])
            ny = ys[i] + speed * math.sin(th[i])
            wrapped = not (0 <= nx < world and 0 <= ny < world)
            nx %= world
            ny %= world
            xs[i], ys[i] = nx, ny
            if wrapped:
                own[i] = zone_of(nx, ny, world, g)
                continue
            new = next_owner(own[i], nx, ny, world, g, h)
            if new != own[i]:
                # count each border line crossed (a diagonal corner step crosses two)
                handoffs += abs(new[0] - own[i][0]) + abs(new[1] - own[i][1])
                own[i] = new
    return handoffs / seconds


def idle_crowd(h, n=40, seconds=36000, checks_per_second=1, sigma=0.5, half=5.0, seed=7):
    """n players wander within +-half metres of the border x = 0 (zones -1 and 0 on a line).
    sigma is the random-walk step per second; with more checks per second the step per check
    shrinks by sqrt(checks). Returns handoffs per second."""
    rnd = random.Random(seed)
    step = sigma / math.sqrt(checks_per_second)
    world, g = 2 * half, 2        # map [-half, half) onto a 2-zone line [0, 2*half)
    xs = [rnd.uniform(-half, half) for _ in range(n)]
    own = [zone_of(x + half, 0.0, world, g) for x in xs]
    handoffs = 0
    for _ in range(seconds * checks_per_second):
        for i in range(n):
            x = xs[i] + rnd.gauss(0, step)
            if x > half:
                x = 2 * half - x
            if x < -half:
                x = -2 * half - x
            x = max(-half, min(half - 1e-9, x))
            xs[i] = x
            new = next_owner(own[i], x + half, 0.0, world, g, h)
            if new != own[i]:
                handoffs += 1
                own[i] = new
    return handoffs / seconds


# ---------------------------------------------------------------- the handoff protocol

class ZoneServer:
    """One zone server's view of ownership. Messages are tuples:
        ("HANDOFF", pid, seq, state, src, dst)
        ("ACK", pid, seq, src, dst)
    The Network class below delivers them. Invariant to keep: at every moment, at most one
    server has `owns(pid)` true."""

    def __init__(self, name):
        self.name = name
        self.owned = {}      # pid -> state dict, for entities this server holds
        self.leaving = {}    # pid -> seq of the handoff in flight
        self.last_seq = {}   # pid -> highest seq this server has seen or issued
        self.ghosts = set()

    def owns(self, pid):
        """True if this server may simulate pid now (holds it and is not handing it off)."""
        return pid in self.owned and pid not in self.leaving

    def spawn(self, pid, state):
        """Provided: create a player here (login)."""
        self.owned[pid] = dict(state)
        self.last_seq[pid] = 0

    def start_handoff(self, pid, dst):
        """Begin handing pid to server name `dst`. Only an owner may start, and only one
        handoff per entity may be in flight. Return the HANDOFF message, or None if refused.
        Use seq = last_seq[pid] + 1, record it in last_seq and in leaving."""
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError

    def on_message(self, msg):
        """Handle one message. Return a reply message or None.
        HANDOFF: reject (return None) if seq <= last_seq for pid; otherwise take ownership,
                 record the seq, drop any ghost of pid, and reply with an ACK.
        ACK:     if pid is leaving with exactly this seq, release it: remove it from owned
                 and leaving and keep it as a ghost. Otherwise ignore."""
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError


class Network:
    """Provided: a list of servers and a queue of messages you deliver by hand, in any order,
    so tests can lose, duplicate and reorder messages."""

    def __init__(self, *servers):
        self.servers = {s.name: s for s in servers}
        self.queue = []

    def send(self, msg):
        if msg is not None:
            self.queue.append(msg)

    def deliver(self, index=0):
        msg = self.queue.pop(index)
        dst = msg[-1]
        self.send(self.servers[dst].on_message(msg))

    def owners(self, pid):
        return [n for n, s in self.servers.items() if s.owns(pid)]


# ---------------------------------------------------------------- command line

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--simulate", type=int, metavar="G")
    ap.add_argument("--idle", action="store_true")
    args = ap.parse_args()
    n, world, v, r = 3000, 6000, 2.0, 100
    if args.table:
        print("g  zones  per-zone  handoffs/s  ghosts  busiest(f=0.4)")
        for g in (1, 2, 3, 4, 6, 8):
            print(f"{g:<2} {g*g:>5} {n/g**2:>9.0f} {handoff_rate(n, world, v, g):>11.2f} "
                  f"{ghost_fraction(world, r, g):>7.1%} {int(busiest_zone(n, 0.4, g) + 0.5):>10}")
    if args.simulate:
        g = args.simulate
        got = simulate(n, world, v, g, seconds=300)
        print(f"g={g}: measured {got:.2f}/s, predicted {handoff_rate(n, world, v, g):.2f}/s")
    if args.idle:
        for h in (0, 1, 2, 4, 8):
            print(f"h={h} m: {idle_crowd(h):.2f}/s at 1 check/s")


if __name__ == "__main__":
    main()
