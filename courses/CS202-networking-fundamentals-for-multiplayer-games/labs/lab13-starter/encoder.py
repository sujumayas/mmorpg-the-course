"""CS202 Lab 13: measure real bytes per entity.

    python encoder.py          # prints bytes per entity at full and quantized precision

`encode_full` is given. You write `encode_quantized` and `decode_quantized` (TODO) so that
the round trip loses at most the stated precision. Standard library only.
"""
import math
import random
import struct

MAP = 1024.0  # metres, map is MAP x MAP x 64 high

# id uint16, x y z float32, yaw float32, vx vy vz float32, health uint16, anim uint8, flags uint8
FULL = struct.Struct("!H3ff3fHBB")
# id uint16, x y uint16 (1/64 m), z uint16 (1/1024 m), yaw uint8 (360/256 deg),
# vx vy vz int8 (0.25 m/s, clamped), health uint8 (0..255), anim uint8
QUANT = struct.Struct("!H3HB3bBB")


def encode_full(e):
    return FULL.pack(e["id"], e["x"], e["y"], e["z"], e["yaw"], *e["vel"], e["hp"], e["anim"], e["flags"])


def _q(v, lo, hi, steps):
    v = min(max(v, lo), hi)
    return int(round((v - lo) / (hi - lo) * steps))


def encode_quantized(e):
    """Pack e with QUANT. x, y in 0..MAP on a 1/64 m grid; z in 0..64 on a 1/1024 m grid;
    yaw in degrees 0..360 to 0..255; each velocity component to round(v * 4) clamped to
    -128..127; hp clamped to 0..255. TODO."""
    raise NotImplementedError


def decode_quantized(data):
    """Inverse of encode_quantized. TODO."""
    raise NotImplementedError


def random_entity(rng, i):
    return {"id": i, "x": rng.uniform(0, MAP - 1), "y": rng.uniform(0, MAP - 1), "z": rng.uniform(0, 60),
            "yaw": rng.uniform(0, 360), "vel": tuple(rng.uniform(-8, 8) for _ in range(3)),
            "hp": rng.randint(0, 200), "anim": rng.randint(0, 40), "flags": 0}


def main():
    rng = random.Random(13)
    ents = [random_entity(rng, i) for i in range(1000)]
    full = len(encode_full(ents[0]))
    quant = len(encode_quantized(ents[0]))
    worst_pos = worst_yaw = worst_vel = 0.0
    for e in ents:
        d = decode_quantized(encode_quantized(e))
        worst_pos = max(worst_pos, math.dist((e["x"], e["y"]), (d["x"], d["y"])))
        dyaw = abs((e["yaw"] - d["yaw"] + 180) % 360 - 180)
        worst_yaw = max(worst_yaw, dyaw)
        worst_vel = max(worst_vel, max(abs(a - b) for a, b in zip(e["vel"], d["vel"])))
    print(f"full precision: {full} bytes per entity")
    print(f"quantized:      {quant} bytes per entity")
    print(f"worst error: position {worst_pos * 100:.2f} cm, yaw {worst_yaw:.2f} deg, velocity {worst_vel:.3f} m/s")
    ok = full == 34 and quant == 14 and worst_pos <= 0.0111 and worst_yaw <= 0.71 and worst_vel <= 0.126
    print("all checks passed" if ok else "check your quantizer")


if __name__ == "__main__":
    main()
