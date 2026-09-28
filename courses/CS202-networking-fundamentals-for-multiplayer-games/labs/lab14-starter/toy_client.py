"""CS202 Lab 14: a toy snapshot-interpolation client with bugs in it.

The server moves one entity around a circle and sends a snapshot 30 times per second.
The client draws the entity INTERP_MS (120 ms) in the past, interpolating between the two
snapshots around that time. If no newer snapshot has arrived yet (the buffer ran dry),
it extrapolates from the last two, for at most EXTRAP_CAP_MS, then holds still.

This file is written the way a first version often is. It passes every test on a
perfect network. Your job in Lab 14 is to find out what it does on a bad one.
"""
import bisect
import math

SEND_HZ = 30
INTERP_MS = 120.0     # three 30 Hz intervals plus 20 ms for jitter
EXTRAP_CAP_MS = 250.0
RADIUS = 20.0          # metres
SPEED = 6.0            # metres per second


def server_position(t_ms):
    """Where the entity really is at server time t_ms."""
    angle = SPEED / RADIUS * t_ms / 1000.0
    return (RADIUS * math.cos(angle), RADIUS * math.sin(angle))


class Snapshot:
    def __init__(self, seq, t_ms, pos):
        self.seq, self.t, self.pos = seq, t_ms, pos


class Client:
    def __init__(self):
        self.snaps = []        # snapshots sorted by server time
        self.times = []        # their server times, for bisect
        self.server_tick = -1  # newest server tick the client knows about (HUD, clock sync)
        self.branch = None     # "interp", "extrap", "hold" or "wait", for debugging

    def on_receive(self, snap):
        i = bisect.bisect_right(self.times, snap.t)
        self.snaps.insert(i, snap)
        self.times.insert(i, snap.t)
        self.server_tick = snap.seq

    def sample(self, render_ms):
        """Position to draw for server time render_ms, or None before two snapshots exist."""
        if len(self.snaps) < 2:
            self.branch = "wait"
            return None
        i = bisect.bisect_right(self.times, render_ms)
        if 0 < i < len(self.snaps):
            a, b = self.snaps[i - 1], self.snaps[i]
            alpha = (render_ms - a.t) / (b.t - a.t)
            self.branch = "interp"
            return lerp(a.pos, b.pos, alpha)
        if i == 0:
            self.branch = "hold"
            return self.snaps[0].pos
        # buffer ran dry: extrapolate from the last two snapshots
        prev, last = self.snaps[-2], self.snaps[-1]
        ahead = min(render_ms - last.t, EXTRAP_CAP_MS)
        vel = ((last.pos[0] - prev.pos[0]) / (last.t - prev.t),
               (last.pos[1] - prev.pos[1]) / (last.t - prev.t))   # metres per ms
        self.branch = "extrap"
        return (last.pos[0] + vel[0] * ahead * 1000, last.pos[1] + vel[1] * ahead * 1000)


def lerp(p, q, a):
    return (p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a)
