"""CS202 Lab 06: sequence numbers, acks, and redundant inputs over a lossy link.

    python reliability.py --check                    # tests against the week 6 lecture
    python reliability.py --table                    # the lecture's section 2 table, by formula
    python reliability.py --sim --p 0.05 --q 0.5 --k 3
                                                     # one hour of 60 Hz inputs, simulated

The model is the week 6 lecture. Standard library only.
"""
import argparse
import random
import struct

HEADER = struct.Struct("!HHI")   # sequence, ack, ack_bits: 8 bytes, network byte order


# ---------------------------------------------------------------- sequence numbers

def seq_greater_than(a, b):
    """True if 16-bit sequence number a is newer than b, allowing for wraparound
    (65535 is followed by 0). Half the number space counts as 'ahead'. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- acks

class AckTracker:
    """Receiver side. Remembers which recent packets arrived and writes the ack fields
    for the next outgoing header: `ack` is the newest sequence received, and bit n of
    `ack_bits` (n = 0..31) is set if packet ack - 1 - n was received."""

    def __init__(self):
        self.received = set()
        self.newest = None

    def on_receive(self, seq):
        """TODO: record seq; update self.newest using seq_greater_than."""
        raise NotImplementedError

    def ack_fields(self):
        """TODO: return (ack, ack_bits). Sequence arithmetic is modulo 65536."""
        raise NotImplementedError


def acked_by(ack, ack_bits):
    """Sender side: the set of sequence numbers one header acknowledges (up to 33). TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- loss and redundancy

def p_input_lost(p, k, q=None):
    """Chance that all k consecutive copies of an input are lost.
    Independent loss (q is None): p ** k. Bursty loss: p * q ** (k - 1). TODO."""
    raise NotImplementedError


def loss_pattern(n, p, q, seed=7):
    """n booleans, True = packet lost. Long-run loss rate p; after a loss, the next
    packet is lost with probability q (q = p gives independent loss). This is the
    week 2 bursty model. Given, do not change."""
    rng = random.Random(seed)
    r = p if q == p else p * (1 - q) / (1 - p)   # P(lost | previous arrived)
    out, prev = [], False
    for _ in range(n):
        prev = rng.random() < (q if prev else r)
        out.append(prev)
    return out


def simulate_redundancy(lost, k):
    """Input i is sent in packets i, i + 1, ..., i + k - 1 (one packet per tick).
    `lost` has at least len(inputs) + k - 1 entries. For each input return the index j
    (0 .. k - 1) of the first copy that arrived, or None if every copy was lost.
    Return that list for the first len(lost) - k + 1 inputs. TODO."""
    raise NotImplementedError


def packet_bytes(k, input_bytes=4, udp_ip=28):
    """Size of one input packet on the wire: headers + our 8-byte header + k inputs."""
    return udp_ip + HEADER.size + k * input_bytes


# ---------------------------------------------------------------- report

def table():
    per_hour = 60 * 3600
    print(f"{'loss':>5} {'copies':>6} {'P(input lost)':>14} {'lost per hour':>14} {'packet':>7} {'kbit/s':>7}")
    for p in (0.01, 0.05, 0.10, 0.20):
        for k in (1, 2, 3):
            pl = p_input_lost(p, k)
            print(f"{p:>5.0%} {k:>6} {pl:>14.2e} {pl * per_hour:>14,.1f} "
                  f"{packet_bytes(k):>6}B {packet_bytes(k) * 60 * 8 / 1000:>7.2f}")


def sim(p, q, k, n=60 * 3600, seed=7):
    lost = loss_pattern(n + k - 1, p, q, seed)
    first = simulate_redundancy(lost, k)
    missed = sum(1 for f in first if f is None)
    late = [f for f in first if f]
    print(f"p={p} q={q} k={k}: {n:,} inputs, measured packet loss {sum(lost[:n]) / n:.2%}")
    print(f"  inputs lost: {missed:,} (formula: {p_input_lost(p, k, None if q == p else q) * n:,.1f})")
    print(f"  inputs saved by a later copy: {len(late):,}")


def check():
    tests = []

    def t(name, got, want, tol=1e-12):
        ok = got == want if not isinstance(want, float) else abs(got - want) <= tol
        tests.append((name, ok, got, want))

    try:
        t("5 > 3", seq_greater_than(5, 3), True)
        t("2 > 65534 (wrapped)", seq_greater_than(2, 65534), True)
        t("65534 > 2", seq_greater_than(65534, 2), False)
        t("40000 > 5000", seq_greater_than(40000, 5000), False)
        a = AckTracker()
        for s in (65533, 65534, 0, 1, 3):          # 65535 and 2 were lost
            a.on_receive(s)
        ack, bits = a.ack_fields()
        t("ack after wrap", ack, 3)
        t("ack_bits", bits, 0b110110)
        t("acked_by", acked_by(ack, bits), {3, 1, 0, 65534, 65533})
        t("header size", HEADER.size, 8)
        t("P lost p=5% k=3", p_input_lost(0.05, 3), 0.05 ** 3)
        t("P lost bursty p=5% q=0.5 k=3", p_input_lost(0.05, 3, 0.5), 0.0125)
        lost = [False, True, True, False, True, True, True, False]
        t("redundancy k=2", simulate_redundancy(lost, 2), [0, None, 1, 0, None, None, 1])
        t("redundancy k=3", simulate_redundancy(lost, 3), [0, 2, 1, 0, None, 2])
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
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--sim", action="store_true")
    ap.add_argument("--p", type=float, default=0.05)
    ap.add_argument("--q", type=float, default=None, help="burstiness; default = p (independent)")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    if a.table:
        table()
    elif a.sim:
        sim(a.p, a.p if a.q is None else a.q, a.k, seed=a.seed)
    else:
        check()
