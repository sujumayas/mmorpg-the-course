"""CS202 Lab 05: a bit writer, a bit reader, and a player state that fits in 14 bytes.

    python bitpack.py --check        # tests your code against the week 5 lecture
    python bitpack.py --demo         # packs the lecture's player state and prints the sizes
    python bitpack.py --fuzz 10000   # feeds random bytes to the reader; it must never crash

The model is the week 5 lecture, sections 2 and 3. Standard library only.
"""
import argparse
import math
import random
import struct


# ---------------------------------------------------------------- how many bits?

def bits_for_count(count):
    """Bits needed to tell `count` different values apart: ceil(log2(count)).
    One value needs 0 bits. TODO."""
    raise NotImplementedError


def steps(lo, hi, precision, wraps=False):
    """Number of distinct values when [lo, hi] is cut into steps of `precision`.
    A closed range includes both ends, so it has (hi - lo) / precision + 1 values.
    An angle that wraps (hi is the same place as lo) has (hi - lo) / precision values.
    Round (hi - lo) / precision to the nearest integer before adding. TODO."""
    raise NotImplementedError


def quantize(x, lo, hi, precision, wraps=False):
    """Map a real value to an integer 0 .. steps - 1. Clamp to [lo, hi] first, or for
    a wrapping value take it modulo (hi - lo). Round to the nearest step. TODO."""
    raise NotImplementedError


def dequantize(q, lo, precision):
    """The inverse: the real value an integer step stands for."""
    return lo + q * precision


# ---------------------------------------------------------------- the bit stream

class BitWriter:
    """Appends unsigned integers of any width from 0 to 32 bits, least significant bit
    first, into a growing bytearray. write(v, n) must reject v < 0 or v >= 2**n."""

    def __init__(self):
        self.buf = bytearray()
        self.nbits = 0

    def write(self, value, nbits):
        """TODO: write the low `nbits` bits of value. Hint: loop bit by bit first; make
        it fast later only if you need to."""
        raise NotImplementedError

    def write_bool(self, b):
        self.write(1 if b else 0, 1)

    def getvalue(self):
        return bytes(self.buf)


class ReadError(Exception):
    """Raised when a packet is shorter than the reader asked for or holds a bad value."""


class BitReader:
    """Reads what BitWriter wrote. Never trusts the packet: reading past the end raises
    ReadError, it does not return garbage or crash with IndexError."""

    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read(self, nbits):
        """TODO: return the next `nbits` bits as an unsigned integer."""
        raise NotImplementedError

    def read_bool(self):
        return self.read(1) == 1


# ---------------------------------------------------------------- the player state

# name, lo, hi, precision, wraps. These are the lecture's section 2 choices.
FIELDS = [
    ("x", 0.0, 512.0, 0.01, False),
    ("y", 0.0, 512.0, 0.01, False),
    ("z", 0.0, 64.0, 0.01, False),
    ("yaw", 0.0, 360.0, 360 / 1024, True),
    ("pitch", -90.0, 90.0, 180 / 511, False),
    ("vx", -20.0, 20.0, 0.05, False),
    ("vy", -20.0, 20.0, 0.05, False),
    ("vz", -20.0, 20.0, 0.05, False),
    ("health", 0, 100, 1, False),
    ("state", 0, 4, 1, False),
]
FLAGS = ["crouching", "firing", "reloading", "sprinting"]
NAIVE = struct.Struct("<3f2f3fii4?")   # what a first attempt sends: 44 bytes


def field_bits(f):
    _, lo, hi, prec, wraps = f
    return bits_for_count(steps(lo, hi, prec, wraps))


def pack_state(state):
    """TODO: write every field in FIELDS order with quantize + field_bits, then the four
    flags as single bits. Return bytes."""
    raise NotImplementedError


def unpack_state(data):
    """TODO: the inverse of pack_state. Must raise ReadError, not crash, on a short or
    malformed packet. Any field whose integer is >= its steps() count (for example a
    `state` above 4 or an x above 51,200) is malformed."""
    raise NotImplementedError


SAMPLE = {"x": 123.456, "y": 400.004, "z": 12.5, "yaw": 271.3, "pitch": -12.0,
          "vx": 5.43, "vy": -0.02, "vz": 0.0, "health": 87, "state": 2,
          "crouching": False, "firing": True, "reloading": False, "sprinting": True}


def demo():
    total = sum(field_bits(f) for f in FIELDS) + len(FLAGS)
    for f in FIELDS:
        print(f"  {f[0]:<7} {field_bits(f):>2} bits   max error {f[3] / 2:.4g}")
    print(f"  flags   {len(FLAGS):>2} bits")
    packed = pack_state(SAMPLE)
    print(f"total {total} bits -> {len(packed)} bytes (naive struct: {NAIVE.size} bytes)")
    back = unpack_state(packed)
    for k in FIELDS:
        print(f"  {k[0]:<7} sent {SAMPLE[k[0]]:>9} got {back[k[0]]:>12.5f}")


def fuzz(n, seed=5):
    rng = random.Random(seed)
    counts = {"ok": 0, "ReadError": 0}
    for _ in range(n):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 20)))
        try:
            unpack_state(data)
            counts["ok"] += 1
        except ReadError:
            counts["ReadError"] += 1
    print(f"{n} random packets: {counts['ok']} decoded, {counts['ReadError']} rejected, 0 crashes")


def check():
    tests = []

    def t(name, got, want, tol=1e-9):
        ok = got == want if not isinstance(want, float) else abs(got - want) <= tol
        tests.append((name, ok, got, want))

    try:
        t("bits_for_count(1001)", bits_for_count(1001), 10)
        t("bits_for_count(1024)", bits_for_count(1024), 10)
        t("bits_for_count(1025)", bits_for_count(1025), 11)
        t("steps x (0..512 at 1 cm)", steps(0, 512, 0.01), 51201)
        t("bits x", field_bits(FIELDS[0]), 16)
        t("bits z", field_bits(FIELDS[2]), 13)
        t("bits yaw (wraps)", field_bits(FIELDS[3]), 10)
        t("bits yaw if you forget it wraps", bits_for_count(steps(0, 360, 360 / 1024)), 11)
        t("bits for Fiedler's z in [0, 32) at 1/512 m", bits_for_count(32 * 512), 14)
        t("quantize 123.456", quantize(123.456, 0, 512, 0.01), 12346)
        t("quantize clamps", quantize(600, 0, 512, 0.01), 51200)
        t("quantize yaw 359.9 wraps to 0", quantize(359.9, 0, 360, 360 / 1024, True), 0)
        w = BitWriter()
        w.write(5, 3)
        w.write(1, 1)
        w.write(300, 9)
        t("writer bytes", w.getvalue(), bytes([0xCD, 0x12]))
        r = BitReader(w.getvalue())
        t("reader round trip", (r.read(3), r.read(1), r.read(9)), (5, 1, 300))
        try:
            BitReader(b"\x01").read(9)
            t("read past end raises ReadError", False, True)
        except ReadError:
            t("read past end raises ReadError", True, True)
        packed = pack_state(SAMPLE)
        t("packed size", len(packed), 14)
        back = unpack_state(packed)
        t("x error <= 5 mm", abs(back["x"] - SAMPLE["x"]) <= 0.005 + 1e-9, True)
        t("flags survive", (back["firing"], back["sprinting"], back["crouching"]), (True, True, False))
    except NotImplementedError:
        print("some functions still raise NotImplementedError; finish the TODOs")
        return
    bad = [x for x in tests if not x[1]]
    for name, ok, got, want in bad:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
    print("all checks passed" if not bad else f"{len(bad)} of {len(tests)} checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fuzz", type=int, default=0)
    a = ap.parse_args()
    if a.demo:
        demo()
    elif a.fuzz:
        fuzz(a.fuzz)
    else:
        check()
