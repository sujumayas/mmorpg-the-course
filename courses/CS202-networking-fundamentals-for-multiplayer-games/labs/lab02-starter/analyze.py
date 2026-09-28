"""CS202 Lab 02: turn a ping log into the numbers a netcode programmer needs.

    python analyze.py --check            # tests your functions on sample_run.csv
    python analyze.py run.csv            # reports on your own run

Implement every function marked TODO. The formulas are in the week 2 lecture, section 2.
Standard library only (statistics, csv, math).
"""
import csv
import math
import statistics
import sys


def load(path):
    """Return (sent_count, rows) where rows are dicts for echoed packets, in seq order."""
    rows, sent = [], 0
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            sent += 1
            if r["rtt_ms"]:
                rows.append({"seq": int(r["seq"]), "rtt": float(r["rtt_ms"]),
                             "order": int(r["arrival_order"])})
    rows.sort(key=lambda r: r["seq"])
    return sent, rows


def loss_rate(sent, rows):
    """Fraction of sent packets with no echo. TODO."""
    raise NotImplementedError


def reordered(rows):
    """Number of echoed packets that arrived after a packet with a higher seq. TODO.
    Hint: walk the rows from the highest seq down to the lowest, keeping the lowest
    arrival 'order' seen so far. A packet is reordered if its own 'order' is greater than
    that minimum. Test it on a tiny hand-made list first."""
    raise NotImplementedError


def percentile(values, p):
    """Inclusive linear-interpolation percentile, p in [0, 1] (the MA102 week 12 rule).
    Sort; h = (n - 1) * p; interpolate between sorted[floor(h)] and sorted[ceil(h)]. TODO."""
    raise NotImplementedError


def rfc3550_jitter(rtts):
    """Smoothed jitter: J starts at 0; for each consecutive pair, D = r[i] - r[i-1],
    J = J + (|D| - J) / 16. Return the final J. TODO."""
    raise NotImplementedError


def late_fraction(extra, buffer_ms):
    """Fraction of packets whose extra delay (rtt - min rtt) is greater than buffer_ms. TODO."""
    raise NotImplementedError


def buffer_for(extra, target_late):
    """Smallest buffer B, chosen from the observed extra delays, with
    late_fraction(extra, B) <= target_late. TODO."""
    raise NotImplementedError


def report(path):
    sent, rows = load(path)
    rtts = [r["rtt"] for r in rows]
    base = min(rtts)
    extra = [x - base for x in rtts]
    print(f"file {path}: sent {sent}, echoed {len(rows)}")
    print(f"loss            {loss_rate(sent, rows) * 100:.2f}%")
    print(f"reordered       {reordered(rows)}")
    print(f"RTT min         {base:.2f} ms")
    print(f"RTT mean        {statistics.mean(rtts):.2f} ms")
    print(f"RTT median      {percentile(rtts, 0.5):.2f} ms")
    print(f"RTT P95         {percentile(rtts, 0.95):.2f} ms")
    print(f"RTT SD          {statistics.stdev(rtts):.2f} ms (sample, n - 1)")
    print(f"RFC 3550 jitter {rfc3550_jitter(rtts):.2f} ms")
    for target in (0.10, 0.05, 0.01):
        b = buffer_for(extra, target)
        print(f"buffer for <= {target:.0%} late: {b:.1f} ms above min "
              f"(actual late {late_fraction(extra, b):.1%})")
    return sent, rows, rtts, extra


def check():
    sent, rows, rtts, extra = report("sample_run.csv")
    expect = {
        "loss": (loss_rate(sent, rows), 1 / 21),
        "reordered": (reordered(rows), 1),
        "mean": (statistics.mean(rtts), 45.85),
        "median": (percentile(rtts, 0.5), 42.0),
        "p95": (percentile(rtts, 0.95), 59.85),
        "sd": (statistics.stdev(rtts), 12.57),
        "jitter": (rfc3550_jitter(rtts), 8.18),
        "late@5": (late_fraction(extra, 5), 0.15),
        "buf10%": (buffer_for(extra, 0.10), 16.0),
        "buf5%": (buffer_for(extra, 0.05), 18.0),
    }
    bad = [k for k, (got, want) in expect.items() if not math.isclose(got, want, abs_tol=0.01)]
    print("all checks passed" if not bad else f"check these: {bad}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--check":
        report(sys.argv[1])
    else:
        check()
