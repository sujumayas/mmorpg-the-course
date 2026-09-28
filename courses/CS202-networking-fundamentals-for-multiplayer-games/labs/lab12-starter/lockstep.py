"""CS202 Lab 12: deterministic lockstep. Part A times the turns; part B hunts a desync.

    python lockstep.py --check                     # tests part A and runs the desync test
    python lockstep.py --timing --turn 200 --k 2   # effective turn length for a set of latencies
    python lockstep.py --sync --turns 300          # two peers, same commands, compare checksums

The model is the week 12 lecture. Commands issued during turn n run at the start of turn n + k.
Each peer runs the whole simulation; only commands cross the network. Standard library only.
"""
import argparse
import random
import struct
import zlib

# ================================================================ part A: timing

def execution_delay(issue_ms, turn_ms, k):
    """Milliseconds from issuing a command at time issue_ms to its execution at the start of
    turn floor(issue_ms / turn_ms) + k. TODO."""
    raise NotImplementedError("TODO")


def simulate_turns(turn_ms, k, latency, turns=241, jitter=0.0, seed=12):
    """Start times of each turn when every peer must hear from every other peer before it may
    start turn n. Commands for turn n are sent at the END of turn n - k. latency[i][j] is the
    one-way latency from peer i to peer j in ms; jitter adds U(0, jitter) to each message.
    Returns the list of start times. TODO: fill in the max(...) rule from the lecture."""
    raise NotImplementedError("TODO")


def effective_turn(start):
    """Average turn length over the last 120 turns (skips the warm-up)."""
    h = len(start) - 121
    return (start[-1] - start[h]) / (len(start) - 1 - h)


# ================================================================ part B: the desync hunt

class Unit:
    def __init__(self, uid, owner, x, y):
        self.uid, self.owner = uid, owner
        self.x, self.y = x, y              # millimetres, integers
        self.dest = None
        self.hp = 1000                     # tenths of a hit point, integer
        self.target = None


class Peer:
    """One machine's copy of the whole game. local_player is the player sitting at it."""

    def __init__(self, local_player, seed=2026):
        self.local_player = local_player
        self.rng = random.Random(seed)            # shared: same seed on every peer
        self.cosmetic_rng = random.Random()       # local only, never affects the game
        self.units = [Unit(u, u // 6, 1000 * (u % 6), 0 if u < 6 else 20000) for u in range(12)]
        self.turn = 0

    def apply(self, commands):
        """Apply this turn's commands in the order this peer received them."""
        reserved = set()
        for cmd in commands:
            u = self.units[cmd["unit"]]
            if cmd["kind"] == "move":
                tile = (cmd["x"] // 1000, cmd["y"] // 1000)
                while tile in reserved:            # two units cannot claim the same tile
                    tile = (tile[0] + 1, tile[1])
                reserved.add(tile)
                u.dest = (tile[0] * 1000, tile[1] * 1000)
            elif cmd["kind"] == "attack":
                u.target = cmd["target"]

    def step(self):
        for u in self.units:
            if u.hp <= 0:
                continue
            if u.dest:
                for axis in ("x", "y"):
                    d = u.dest[0 if axis == "x" else 1] - getattr(u, axis)
                    setattr(u, axis, getattr(u, axis) + max(-300, min(300, d)))
                if (u.x, u.y) == u.dest:
                    u.dest = None
                if u.owner == self.local_player:
                    self.rng.random()    # pick a footstep sound for my own units
            if u.target is not None:
                t = self.units[u.target]
                if t.hp > 0 and abs(t.x - u.x) + abs(t.y - u.y) <= 8000:
                    if self.rng.random() < 0.75:    # 75% chance to hit, shared RNG
                        t.hp -= 73
        self.turn += 1

    def checksum(self):
        """CRC-32 of everything that matters: turn, and each unit's id, x, y, hp.
        Pack integers with struct so the bytes are identical on every machine. TODO."""
        raise NotImplementedError("TODO")


def script(turns, seed=7):
    """The same random-but-fixed command script for both players."""
    rng = random.Random(seed)
    out, seq = [], 0
    for n in range(turns):
        cmds = []
        for player in (0, 1):
            for _ in range(rng.choice([0, 0, 1, 2])):
                unit = player * 6 + rng.randrange(6)
                if rng.random() < 0.6:
                    x, y = rng.randrange(0, 12000), rng.randrange(4000, 16000)
                    if rng.random() < 0.3:
                        x, y = 6000, 10000          # both sides fight over the centre tile
                    cmds.append({"player": player, "seq": seq, "unit": unit, "kind": "move",
                                 "x": x, "y": y})
                else:
                    cmds.append({"player": player, "seq": seq, "unit": unit, "kind": "attack",
                                 "target": (1 - player) * 6 + rng.randrange(6)})
                seq += 1
        out.append(cmds)
    return out


def run_sync(turns=300, verbose=True):
    """Both peers run the same script. Each receives its own commands first (local), then the
    other player's (network), as real peers would. Returns the first turn whose checksums differ,
    or None."""
    peers = [Peer(0), Peer(1)]
    for n, cmds in enumerate(script(turns)):
        for p in peers:
            mine = [c for c in cmds if c["player"] == p.local_player]
            theirs = [c for c in cmds if c["player"] != p.local_player]
            p.apply(mine + theirs)
            p.step()
        a, b = peers[0].checksum(), peers[1].checksum()
        if a != b:
            if verbose:
                print(f"DESYNC at turn {n}: {a:08x} vs {b:08x}")
                for ua, ub in zip(peers[0].units, peers[1].units):
                    if (ua.x, ua.y, ua.hp) != (ub.x, ub.y, ub.hp):
                        print(f"  unit {ua.uid}: peer0 {(ua.x, ua.y, ua.hp)}  peer1 {(ub.x, ub.y, ub.hp)}")
            return n
    if verbose:
        print(f"in sync for {turns} turns, final checksum {peers[0].checksum():08x}")
    return None


def check():
    ok = True

    def eq(label, got, want, tol=1e-6):
        nonlocal ok
        good = got == want if want is None or isinstance(want, bool) else abs(got - want) <= tol
        print(("pass " if good else "FAIL ") + f"{label}: got {got}, want {want}")
        ok &= good

    eq("delay: issued at 1000 ms, T 200, k 2", execution_delay(1000, 200, 2), 400)
    eq("delay: issued at 1150 ms", execution_delay(1150, 200, 2), 250)
    eq("delay: issued at 1199 ms", execution_delay(1199, 200, 2), 201)
    lat = lambda L: [[0, L], [L, 0]]
    eq("T_eff, L 150", effective_turn(simulate_turns(200, 2, lat(150))), 200)
    eq("T_eff, L 250", effective_turn(simulate_turns(200, 2, lat(250))), 225)
    eq("T_eff, L 400", effective_turn(simulate_turns(200, 2, lat(400))), 300)
    eq("T_eff, L 400, k 3", effective_turn(simulate_turns(200, 3, lat(400))), 200)
    p = Peer(0)
    c0 = p.checksum()
    eq("checksum is repeatable", p.checksum() == c0, True)
    p.units[3].hp -= 1
    eq("checksum sees one tenth of a hit point", p.checksum() != c0, True)
    eq("two peers stay in sync for 300 turns", run_sync(300, verbose=False), None)
    print("all checks passed" if ok else "some checks FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--timing", action="store_true")
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--turn", type=float, default=200)
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--jitter", type=float, default=0)
    ap.add_argument("--turns", type=int, default=300)
    a = ap.parse_args()
    if a.check:
        raise SystemExit(0 if check() else 1)
    if a.timing:
        print(f"T = {a.turn:.0f} ms, k = {a.k}, jitter = {a.jitter:.0f} ms")
        print(f"{'worst one-way':>13} {'effective turn':>15} {'mean input delay':>17}")
        for L in (50, 150, 200, 250, 400):
            t = effective_turn(simulate_turns(a.turn, a.k, [[0, L], [L, 0]], jitter=a.jitter))
            print(f"{L:>11}ms {t:>13.1f}ms {(a.k - 0.5) * t:>15.1f}ms")
    if a.sync:
        run_sync(a.turns)


if __name__ == "__main__":
    main()
