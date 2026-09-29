"""MA201 Lab 14 starter: precision budget and a determinism harness.

Standard library only. Python's float is a double (binary64). `f32` rounds a
double to the nearest float32, which lets you emulate float32 arithmetic:
adding two float32 values in double is exact at game magnitudes, so
f32(a + b) gives the same bits as a float32 addition.

Six functions are stubs (marked TODO). As shipped they return 0 or None, so
the file runs and prints a table of zeros. Fill them in using lecture
sections 1 to 5, then run `python test_lab14.py`.

    python precision.py                  # walker table and arena divergence
    python precision.py --speed 0.5 --hz 30
"""
import argparse
import math
import struct
import zlib


def f32(x):
    """Round a Python float (a double) to the nearest float32."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ------------------------------------------------------------- your code
def gap32(x):
    """Spacing between float32 x (x != 0) and the next float32 away from zero."""
    # TODO: 2 ** (floor(log2 |x|) - 23)
    return 0.0


def walk_speed(x0, v, dt, ticks=60, rep="f32"):
    """Average speed of a walker starting at x0 metres, moving v m/s for
    `ticks` ticks of length dt, when positions are stored as
    rep = "f32" (float32 metres), "f64" (double metres) or "mm" (integer mm,
    each tick adds round(v * dt * 1000) mm)."""
    # TODO: simulate the ticks in the chosen representation, return
    # (final - start) / (ticks * dt) in metres per second.
    return 0.0


def freeze_distance(v, dt):
    """Smallest power of two 2**e (metres) at which a float32 walker moving
    v * dt per tick can no longer move (the gap exceeds 2 * v * dt)."""
    # TODO
    return 0.0


def float_clock(hours, ticks, dt):
    """A float32 clock starts at `hours` of uptime and adds f32(dt) `ticks`
    times. Return how many seconds it advanced (as a double)."""
    # TODO
    return 0.0


def state_hash(state):
    """CRC32 of the exact bits of a tuple of floats, packed little-endian as
    doubles. Two states hash equal only if every bit matches."""
    # TODO: struct.pack("<" + "d" * len(state), *state), then zlib.crc32.
    return 0


def first_divergence(hashes_a, hashes_b):
    """Index of the first tick whose hashes differ, or None if none differ."""
    # TODO
    return None


# ------------------------------------------------------------- given
def arena_run(ticks, fused, dt=1 / 120):
    """The lecture's section 5 arena. Returns the state (x, y, vx, vy) after
    every tick, as a list of length `ticks`."""
    x, y, vx, vy = 0.1, -0.8, math.cos(0.3), math.sin(0.3)
    states = []
    for _ in range(ticks):
        x, y = x + vx * dt, y + vy * dt
        if abs(x) > 1:
            vx, x = -vx, math.copysign(2, x) - x
        if abs(y) > 1:
            vy, y = -vy, math.copysign(2, y) - y
        d = math.hypot(x, y)
        if d < 0.5:
            nx, ny = x / d, y / d
            dot = vx * nx + vy * ny
            if fused:
                vx, vy = math.fma(-2 * dot, nx, vx), math.fma(-2 * dot, ny, vy)
            else:
                vx, vy = vx - 2 * dot * nx, vy - 2 * dot * ny
            x, y = nx * (1 - d), ny * (1 - d)
        states.append((x, y, vx, vy))
    return states


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speed", type=float, default=1.4)
    ap.add_argument("--hz", type=float, default=60.0)
    args = ap.parse_args()
    dt = 1 / args.hz

    print(f"Walker at {args.speed} m/s, {args.hz:g} Hz")
    print("   distance     gap32      f32 speed   f64 speed   mm speed")
    for x0 in [1, 10_000, 100_000, 200_000, 300_000, 600_000, 30_000_000]:
        print(f"{x0:>11,} m  {gap32(x0):9.3g}   {walk_speed(x0, args.speed, dt):9.3f}"
              f"   {walk_speed(x0, args.speed, dt, rep='f64'):9.3f}"
              f"   {walk_speed(x0, args.speed, dt, rep='mm'):8.3f}")
    print(f"Freeze distance: {freeze_distance(args.speed, dt):,.0f} m")

    ticks = 120 * 60
    a = [state_hash(s) for s in arena_run(ticks, fused=False)]
    b = [state_hash(s) for s in arena_run(ticks, fused=True)]
    print(f"Arena: first divergent tick {first_divergence(a, b)} of {ticks}")


if __name__ == "__main__":
    main()
