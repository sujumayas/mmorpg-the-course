"""CS202 Lab 11: server-side lag compensation (rewind hit detection).

    python rewind.py --check                  # tests your functions against the lecture
    python rewind.py --accuracy               # hit rate with and without rewind, by shooter RTT
    python rewind.py --cover --cap 1000       # how long after reaching cover a victim can die

The model is the week 11 lecture, section 2. Top-down 2D, metres and milliseconds. The shooter
stands at (0, 0) and looks up the +y axis. The target is a circle of radius 0.3 m at y = 10.
The server records the target every tick; a shot arrives with the shooter's RTT and interpolation
delay, and the server decides hit or miss. Standard library only.
"""
import argparse
import math
from collections import deque

TICK_MS = 1000 / 60    # 60 Hz server tick, as in weeks 8 to 10
RADIUS = 0.3
SPEED = 6.0
TARGET_Y = 10.0


# ---------------------------------------------------------------- your code

class History:
    """Ring buffer of (t_ms, (x, y)) for one player, oldest first."""

    def __init__(self, max_unlag_ms=1000, tick_ms=TICK_MS):
        self.records = deque(maxlen=round(max_unlag_ms / tick_ms) + 1)

    def record(self, t_ms, pos):
        self.records.append((t_ms, pos))

    def position_at(self, t_ms):
        """Position at time t_ms, interpolated between the two records that bracket it.
        Clamp to the oldest record if t_ms is older than the buffer, and to the newest if
        t_ms is in the future. TODO."""
        raise NotImplementedError("TODO")


def ray_hits_circle(origin, direction, center, radius):
    """True if the ray from origin along direction (any length) passes within radius of
    center, in front of the origin. Use the dot product. TODO."""
    raise NotImplementedError("TODO")


def rewind_time(arrival_ms, rtt_ms, interp_ms, max_unlag_ms):
    """Server time the shooter was looking at: arrival minus (RTT + interpolation delay),
    but never more than max_unlag_ms in the past. TODO."""
    raise NotImplementedError("TODO")


def server_hit(history, arrival_ms, aim_point, rtt_ms, interp_ms, lag_comp=True,
               max_unlag_ms=1000):
    """Decide a shot that reaches the server at arrival_ms, aimed from (0, 0) at aim_point.
    With lag_comp, test against the rewound position; without, against the newest record."""
    t = rewind_time(arrival_ms, rtt_ms, interp_ms, max_unlag_ms) if lag_comp else arrival_ms
    return ray_hits_circle((0.0, 0.0), aim_point, history.position_at(t), RADIUS)


# ---------------------------------------------------------------- the harness (given)

def strafe_x(t):
    """Target strafes between x = -2.1 and +2.1 m at 6 m/s, reversing every 700 ms."""
    phase = t % 1400
    x = SPEED * phase / 1000 if phase < 700 else 4.2 - SPEED * (phase - 700) / 1000
    return x - 2.1


def fill(history, path, t_end):
    t = 0
    while t <= t_end:
        history.record(t, (path(t), TARGET_Y))
        t += TICK_MS


def accuracy(rtt, interp=100, lag_comp=True, cap=1000, shots=200):
    """The shooter aims at exactly what their screen shows, every 70 ms, and never leads."""
    hits = 0
    for k in range(shots):
        fire = 2000 + 70 * k                        # server clock when the shooter clicks
        view = fire - rtt / 2 - interp              # what the shooter's screen shows
        arrival = fire + rtt / 2
        h = History(max(cap, 1000) + 1000)
        fill(h, strafe_x, arrival)
        aim = (strafe_x(view), TARGET_Y)
        hits += server_hit(h, arrival, aim, rtt, interp, lag_comp, cap)
    return hits / shots


def cover_window(shooter_rtt, victim_rtt=40, interp=100, cap=1000):
    """Victim runs right at 6 m/s from x = -2. A wall hides everything at x > 0, so the victim
    is fully hidden once the circle's centre passes x = 0.3. The shooter fires on the last frame
    their screen shows a sliver, 1 ms before the centre reaches x = 0.3, aiming 5 mm left of the
    wall edge.
    Returns how long the victim's own screen showed them fully behind cover before the kill
    reached them, or None if the server rejects the shot."""
    run = lambda t: -2.0 + SPEED * t / 1000
    t_hidden = (2.0 + 0.3) / SPEED * 1000           # server time the centre reaches x = 0.3
    view = t_hidden - 1                             # shooter's screen: centre at x = 0.294
    fire = view + shooter_rtt / 2 + interp
    arrival = fire + shooter_rtt / 2
    h = History(max(cap, 1000) + 1000)
    fill(h, run, arrival + TICK_MS)
    if not server_hit(h, arrival, (-0.005, TARGET_Y), shooter_rtt, interp, True, cap):
        return None
    victim_screen_hidden = t_hidden - victim_rtt / 2  # the victim's prediction runs ahead
    death_seen = arrival + victim_rtt / 2
    return death_seen - victim_screen_hidden


def check():
    ok = True

    def eq(label, got, want, tol=1e-6):
        nonlocal ok
        good = got == want if isinstance(want, (bool, type(None))) else abs(got - want) <= tol
        print(("pass " if good else "FAIL ") + f"{label}: got {got}, want {want}")
        ok &= good

    h = History(1000)
    for t, x in [(0, 0.0), (50, 0.3), (100, 0.6)]:
        h.record(t, (x, 10.0))
    eq("position_at(75).x", h.position_at(75)[0], 0.45)
    eq("position_at(-500) clamps to oldest", h.position_at(-500)[0], 0.0)
    eq("position_at(900) clamps to newest", h.position_at(900)[0], 0.6)
    eq("capacity at 1 s and 60 Hz ticks", h.records.maxlen, 61)
    eq("ray straight at the centre", ray_hits_circle((0, 0), (0, 1), (0, 10), 0.3), True)
    eq("ray 0.29 m off", ray_hits_circle((0, 0), (0, 1), (0.29, 10), 0.3), True)
    eq("ray 1.5 m off (the lecture's lead)", ray_hits_circle((0, 0), (0, 1), (1.5, 10), 0.3), False)
    eq("target behind the shooter", ray_hits_circle((0, 0), (0, 1), (0, -10), 0.3), False)
    eq("rewind at 150 ms RTT, 100 ms interp", rewind_time(5000, 150, 100, 1000), 4750)
    eq("rewind capped at 200 ms", rewind_time(5000, 150, 100, 200), 4800)
    eq("accuracy with rewind, 150 ms", accuracy(150, lag_comp=True), 1.0)
    eq("cover window, shooter 150 ms, victim 40 ms", round(cover_window(150), 3), 289.0)
    eq("cover window rejected by a 200 ms cap", cover_window(150, cap=200), None)
    print("all checks passed" if ok else "some checks FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--accuracy", action="store_true")
    ap.add_argument("--cover", action="store_true")
    ap.add_argument("--interp", type=float, default=100)
    ap.add_argument("--cap", type=float, default=1000)
    ap.add_argument("--victim-rtt", type=float, default=40)
    a = ap.parse_args()
    if a.check:
        raise SystemExit(0 if check() else 1)
    rtts = [0, 50, 100, 150, 250, 400]
    if a.accuracy:
        print(f"{'RTT':>5} {'with rewind':>12} {'without':>8}")
        for r in rtts:
            print(f"{r:>5} {accuracy(r, a.interp, True, a.cap):>12.0%} "
                  f"{accuracy(r, a.interp, False, a.cap):>8.0%}")
    if a.cover:
        print(f"{'shooter RTT':>11} {'victim behind cover for':>24}")
        for r in rtts:
            w = cover_window(r, a.victim_rtt, a.interp, a.cap)
            print(f"{r:>11} {'shot rejected' if w is None else f'{w:.0f} ms':>24}")


if __name__ == "__main__":
    main()
