"""MMO404 Lab 02, part A: a handoff protocol that never duplicates or loses an input.

    python handoff.py --check     # runs the protocol tests
    python handoff.py --trace     # prints one handoff, message by message

Two servers, A (west, x < 0) and B (east, x > 0), share a border at x = 0. One player
walks back and forth across it. The client sends one numbered input per tick. A gateway
routes each input to whichever server it believes owns the player. Messages between
servers take `delay` ticks. Your job is the four handlers marked TODO.

The rules you must keep (the tests check all of them):
  1. At most one server is AUTHORITATIVE for the player at any moment.
  2. Every input is applied exactly once, in sequence order, by whichever server owns it.
  3. The player's final position equals the sum of all inputs.
Standard library only.
"""
import random
import sys

AUTHORITATIVE, TRANSFERRING, GHOST, ABSENT = "authoritative", "transferring", "ghost", "absent"


def wants_handoff(x, side, w):
    """Should the owner on `side` ('A' is west, 'B' is east) hand the player over?
    Hysteresis band of width w centred on the border. TODO."""
    raise NotImplementedError


class Server:
    def __init__(self, name, net, gateway, w):
        self.name, self.net, self.gateway, self.w = name, net, gateway, w
        self.role = ABSENT
        self.x = 0.0          # player position as this server knows it
        self.next_seq = 0     # next input sequence number to apply
        self.pending = {}     # seq -> dx, inputs that arrived early
        self.buffer = {}      # seq -> dx, inputs held while TRANSFERRING
        self.applied = []     # log of applied seqs (the tests read it)

    def other(self):
        return "B" if self.name == "A" else "A"

    def _apply_in_order(self):
        while self.next_seq in self.pending:
            self.x += self.pending.pop(self.next_seq)
            self.applied.append(self.next_seq)
            self.next_seq += 1

    def on_input(self, seq, dx):
        """An input arrived from the gateway or was forwarded by the other server. TODO.
        AUTHORITATIVE: apply inputs strictly in seq order (hold early ones in pending).
        TRANSFERRING: hold the input in self.buffer; the new owner will get it later.
        GHOST or ABSENT: this server must not apply it. Send it to the other server."""
        raise NotImplementedError

    def end_of_tick(self):
        """Called once per tick after inputs. If AUTHORITATIVE and wants_handoff says so,
        start a handoff: send ("transfer", x, next_seq, pending) to the other server,
        and become TRANSFERRING. TODO."""
        raise NotImplementedError

    def on_message(self, msg):
        """Handle a server-to-server message. TODO.
        ("transfer", x, next_seq, pending): install the state, become AUTHORITATIVE,
            point the gateway here, apply what you can, reply ("ack",).
        ("ack",): send every buffered input to the other server as ("input", seq, dx),
            clear the buffer, become GHOST.
        ("input", seq, dx): treat exactly like on_input."""
        raise NotImplementedError


# ---------------------------------------------------------------- given harness below

class Net:
    """Server-to-server link. Each message arrives `delay` ticks after it is sent."""
    def __init__(self, delay):
        self.delay, self.t, self.queue = delay, 0, []

    def send(self, to, msg):
        self.queue.append((self.t + self.delay, len(self.queue), to, msg))

    def due(self):
        now = [m for m in self.queue if m[0] <= self.t]
        self.queue = [m for m in self.queue if m[0] > self.t]
        return sorted(now)


class Gateway:
    def __init__(self):
        self.route = "A"


def run(inputs, w, delay, trace=False):
    net, gw = Net(delay), Gateway()
    servers = {"A": Server("A", net, gw, w), "B": Server("B", net, gw, w)}
    servers["A"].role = AUTHORITATIVE
    servers["A"].x = -1.0
    worst = 0
    handoffs = 0
    for seq, dx in enumerate(inputs + [0.0] * (4 * delay + 4)):
        net.t = seq
        for _, _, to, msg in net.due():
            if trace:
                print(f"t={seq:3d}  {to} <- {msg[0]}")
            if msg[0] == "transfer":
                handoffs += 1
            servers[to].on_message(msg)
        if seq < len(inputs):
            servers[gw.route].on_input(seq, dx)
        for s in servers.values():
            s.end_of_tick()
        owners = sum(s.role == AUTHORITATIVE for s in servers.values())
        worst = max(worst, owners)
    applied = sorted(servers["A"].applied + servers["B"].applied)
    owner = [s for s in servers.values() if s.role == AUTHORITATIVE]
    return worst, applied, owner, handoffs


def walk(n, seed):
    """A player dithering near the border: steps of -1..+1 m with a slight drift."""
    rng = random.Random(seed)
    return [round(rng.uniform(-1.0, 1.0) + (0.05 if (i // 200) % 2 == 0 else -0.05), 3)
            for i in range(n)]


def check():
    for delay in (1, 2, 3):
        for w in (0.0, 4.0):
            for seed in range(5):
                inputs = walk(600, seed)
                worst, applied, owner, handoffs = run(inputs, w, delay)
                assert worst <= 1, f"two owners at once (delay {delay}, w {w}, seed {seed})"
                assert applied == list(range(len(inputs))), \
                    f"inputs lost, duplicated or out of order (delay {delay}, w {w}, seed {seed})"
                assert len(owner) == 1, "the player ended with no owner"
                assert abs(owner[0].x - (-1.0 + sum(inputs))) < 1e-6, "final position is wrong"
                assert handoffs > 0, "the walk never crossed the border; check end_of_tick"
    assert wants_handoff(0.1, "A", 0.0) and not wants_handoff(0.1, "A", 4.0)
    assert wants_handoff(-2.5, "B", 4.0) and not wants_handoff(-1.5, "B", 4.0)
    print("all checks passed")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--trace" in sys.argv:
        run([0.6, 0.6, 0.6, 0.6, 0.6, 0.0, 0.0], 0.0, 2, trace=True)
    else:
        print(__doc__)
