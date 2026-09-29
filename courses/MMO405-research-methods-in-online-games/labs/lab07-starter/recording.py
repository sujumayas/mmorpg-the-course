"""MMO405 Lab 07: three recording rules for the same observation.

Run:  python gen_focal.py       # once, writes focal_log.csv
      python recording.py       # prints the comparison table once your functions work
      python check_lab07.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
A bout is a (start, end) pair of minutes with start < end; the behaviour is "on"
at time t when start <= t < end. Sessions run from minute 0 to minute L.
"""
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = 180


def continuous_share(bouts, L):
    """True share of the session spent in the behaviour: total bout minutes / L."""
    raise NotImplementedError


def scan_share(bouts, L, T, offset=0):
    """Instantaneous sampling at t = offset, offset + T, ... while t < L.
    Return the share of sample points at which the behaviour is on."""
    raise NotImplementedError


def scan_average(bouts, L, T):
    """Mean of scan_share over every integer offset 0, 1, ..., T - 1."""
    raise NotImplementedError


def one_zero_share(bouts, L, T):
    """One-zero sampling. Cut [0, L) into blocks [kT, (k+1)T) for k = 0, 1, ...
    while kT < L (the last block may be cut short by L). A block scores 1 if any
    bout overlaps it, meaning start < block_end and end > block_start.
    Return the share of blocks that score 1."""
    raise NotImplementedError


def one_zero_expected(n, b, T, L):
    """Lecture formula for the expected one-zero score of n bouts of length b,
    assuming no two bouts share a block: min(1, n * (T + b) / L)."""
    raise NotImplementedError


def bias_factor(b, T):
    """Predicted one-zero overstatement for bouts of length b: 1 + T / b."""
    raise NotImplementedError


def load_log(path=HERE / "focal_log.csv"):
    """Return {focal_id: [(start, end), ...]} from focal_log.csv."""
    out = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            out[row["focal_id"]].append((int(row["start_min"]), int(row["end_min"])))
    return dict(out)


def main():
    log = load_log()
    print(f"{'focal':5} {'bouts':>5} {'mean b':>6} {'true':>6} {'scan15':>7} "
          f"{'1-0 15':>7} {'formula':>7} {'obs x':>6} {'pred x':>6}")
    for fid, bouts in log.items():
        n = len(bouts)
        b = sum(e - s for s, e in bouts) / n
        p = continuous_share(bouts, L)
        p10 = one_zero_share(bouts, L, 15)
        print(f"{fid:5} {n:5} {b:6.1f} {p:6.1%} {scan_average(bouts, L, 15):7.1%} "
              f"{p10:7.1%} {one_zero_expected(n, b, 15, L):7.1%} "
              f"{p10 / p:6.2f} {bias_factor(b, 15):6.2f}")


if __name__ == "__main__":
    main()
