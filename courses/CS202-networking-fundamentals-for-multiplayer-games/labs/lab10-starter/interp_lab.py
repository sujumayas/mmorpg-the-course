"""CS202 Lab 10: an entity interpolation buffer, tested under latency, jitter and loss.

    python interp_lab.py --check                      # tests your functions against the lecture
    python interp_lab.py --delay 100                  # one run, default network
    python interp_lab.py --sweep --loss 0.05 --jitter 20   # table of delays 0..200 ms

The model is the week 10 lecture, sections 2 and 3. Times are in milliseconds, positions in
metres. The server sends a snapshot of one strafing player every 50 ms. The client draws
60 frames per second at render time t_r = client_time - latency - delay. Standard library only.
"""
import argparse
import random

SPEED = 6.0          # m/s, the strafing player's speed (week 8's walking speed)
STRAFE_MS = 700      # the player reverses direction every 700 ms
SNAP_MS = 50         # 20 snapshots per second
FRAME_MS = 1000 / 60


def true_x(t):
    """Where the strafing player really was at server time t (a triangle wave, 0 to 4.2 m)."""
    phase = t % (2 * STRAFE_MS)
    if phase < STRAFE_MS:
        return SPEED * phase / 1000
    return SPEED * STRAFE_MS / 1000 - SPEED * (phase - STRAFE_MS) / 1000


# ---------------------------------------------------------------- your code

def lerp(a, b, alpha):
    """Linear interpolation: a at alpha = 0, b at alpha = 1. TODO."""
    raise NotImplementedError("TODO")


def lerp_angle(a, b, alpha):
    """Interpolate between two headings in degrees along the SHORTER arc.
    Result in [0, 360). lerp_angle(350, 10, 0.5) is 0, not 180. TODO."""
    raise NotImplementedError("TODO")


class InterpolationBuffer:
    """Holds (server_time, x) snapshots in arrival order and answers "where to draw"."""

    def __init__(self, max_extrap_ms=250):
        self.snaps = []                  # list of (t, x), kept sorted by t
        self.max_extrap_ms = max_extrap_ms

    def add(self, t, x):
        """Insert a snapshot. Keep self.snaps sorted by t; ignore a duplicate t."""
        if any(s[0] == t for s in self.snaps):
            return
        self.snaps.append((t, x))
        self.snaps.sort()

    def sample(self, t_r):
        """Return (x, mode) for render time t_r. TODO.

        mode "interp": two snapshots bracket t_r (t_a <= t_r <= t_b); lerp between them.
        mode "extrap": t_r is later than the newest snapshot and there are at least two;
                       continue the newest pair's velocity for at most max_extrap_ms,
                       then hold that extrapolated position.
        mode "hold":   t_r is earlier than the oldest snapshot, or only one snapshot exists;
                       draw the nearest snapshot you have.
        Return (None, "empty") if there are no snapshots.
        """
        raise NotImplementedError("TODO")

    def prune(self, t_r):
        """Drop snapshots that can never be used again: keep the newest one at or before t_r
        and everything after it. Keeps the buffer small."""
        older = [i for i, (t, _) in enumerate(self.snaps) if t <= t_r]
        if len(older) > 1:
            del self.snaps[:older[-1]]


def render_time(client_ms, latency_ms, delay_ms):
    """The server time to draw at this client frame. TODO."""
    raise NotImplementedError("TODO")


# ---------------------------------------------------------------- the harness (given)

def run(delay, latency=75, jitter=0.0, loss=0.0, seed=10, seconds=20, max_extrap=250):
    """Simulate one client and return a dict of metrics."""
    rng = random.Random(seed)
    arrivals = []
    for k in range(int(seconds * 1000 / SNAP_MS) + 1):
        t = k * SNAP_MS
        if rng.random() < loss:
            continue
        arrivals.append((t + latency + rng.uniform(0, jitter), t))
    arrivals.sort()
    buf = InterpolationBuffer(max_extrap)
    modes = {"interp": 0, "extrap": 0, "hold": 0, "empty": 0}
    errs, pops, prev = [], 0, None
    i, frame = 0, 0
    while True:
        now = 500 + frame * FRAME_MS
        if now > seconds * 1000:
            break
        while i < len(arrivals) and arrivals[i][0] <= now:
            buf.add(arrivals[i][1], true_x(arrivals[i][1]))
            i += 1
        t_r = render_time(now, latency, delay)
        x, mode = buf.sample(t_r)
        buf.prune(t_r - 1000)
        modes[mode] += 1
        if x is not None:
            errs.append(abs(x - true_x(max(t_r, 0))))
            if prev is not None and abs(x - prev) > 2 * SPEED * FRAME_MS / 1000:
                pops += 1
            prev = x
        frame += 1
    n = sum(modes.values())
    return {
        "delay": delay,
        "interp": modes["interp"] / n,
        "extrap": modes["extrap"] / n,
        "mean_err": sum(errs) / len(errs),
        "max_err": max(errs),
        "pops": pops,
        "age": latency + delay,
    }


def print_rows(rows):
    print(f"{'delay':>6} {'interp':>7} {'extrap':>7} {'mean err':>9} {'max err':>8} {'pops':>5} {'age':>5}")
    for r in rows:
        print(f"{r['delay']:>6} {r['interp']:>7.1%} {r['extrap']:>7.1%} {r['mean_err']:>8.3f}m "
              f"{r['max_err']:>7.3f}m {r['pops']:>5} {r['age']:>4}ms")


def check():
    ok = True

    def eq(label, got, want, tol=1e-6):
        nonlocal ok
        good = (got == want) if isinstance(want, str) else abs(got - want) <= tol
        print(("pass " if good else "FAIL ") + f"{label}: got {got}, want {want}")
        ok &= good

    eq("lerp(4.0, 4.3, 0.5)", lerp(4.0, 4.3, 0.5), 4.15)
    eq("lerp_angle(350, 10, 0.5)", lerp_angle(350, 10, 0.5), 0.0)
    eq("lerp_angle(10, 350, 0.25)", lerp_angle(10, 350, 0.25), 5.0)
    eq("lerp_angle(90, 180, 0.5)", lerp_angle(90, 180, 0.5), 135.0)
    eq("render_time(1225, 75, 100)", render_time(1225, 75, 100), 1050)
    # The lecture's table: snapshots 1000 and 1050 received, 1100 lost, 1150 still in flight.
    b = InterpolationBuffer()
    b.add(1000, 4.0)
    b.add(1050, 4.3)
    x, m = b.sample(1025)
    eq("interp at 1025", round(x, 3), 4.15, 1e-9); eq("mode at 1025", m, "interp")
    x, m = b.sample(1095)
    eq("extrap at 1095", round(x, 3), 4.57, 1e-9); eq("mode at 1095", m, "extrap")
    x, m = b.sample(975)
    eq("hold at 975", x, 4.0); eq("mode at 975", m, "hold")
    x, m = b.sample(1050 + 400)
    eq("extrapolation capped at 250 ms", round(x, 3), 5.8, 1e-9)
    b.add(1150, 4.3)
    x, m = b.sample(1100)
    eq("interp across the lost snapshot", round(x, 3), 4.3, 1e-9); eq("mode at 1100", m, "interp")
    r = run(100)
    eq("clean network, 100 ms: all frames interpolated", r["interp"], 1.0)
    eq("clean network, 100 ms: max error", round(r["max_err"], 9), 0.0)
    r = run(0)
    eq("clean network, 0 ms: all frames extrapolated", r["extrap"], 1.0)
    print("all checks passed" if ok else "some checks FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--delay", type=float, default=100)
    ap.add_argument("--latency", type=float, default=75)
    ap.add_argument("--jitter", type=float, default=0)
    ap.add_argument("--loss", type=float, default=0)
    ap.add_argument("--seed", type=int, default=10)
    a = ap.parse_args()
    if a.check:
        raise SystemExit(0 if check() else 1)
    delays = [0, 25, 50, 75, 100, 150, 200] if a.sweep else [a.delay]
    print_rows([run(d, a.latency, a.jitter, a.loss, a.seed) for d in delays])


if __name__ == "__main__":
    main()
