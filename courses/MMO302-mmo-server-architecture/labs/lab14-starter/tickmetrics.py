"""MMO302 Lab 14: tick telemetry. Implement every function marked TODO.

The lecture (week 14, sections 2, 3 and 6) gives every formula you need.
"""
import math

BOUNDS = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 250]  # ms, bucket upper edges


def nearest_rank(values, q):
    """Smallest value with at least a fraction q of the data at or below it."""
    raise NotImplementedError("TODO step 1")


class TickHistogram:
    """Per-bucket (not cumulative) counts: counts[i] is the number of observations in
    (BOUNDS[i-1], BOUNDS[i]]; counts[-1] is the overflow bucket (> BOUNDS[-1])."""

    def __init__(self, bounds=BOUNDS):
        self.bounds = list(bounds)
        self.counts = [0] * (len(self.bounds) + 1)
        self.total = 0
        self.sum = 0.0

    def observe(self, ms):
        raise NotImplementedError("TODO step 2")

    def merge(self, other):
        """Return a new histogram holding both sets of observations."""
        raise NotImplementedError("TODO step 2")

    def count_over(self, bound):
        """Exact number of observations > bound. bound must be one of the edges."""
        raise NotImplementedError("TODO step 2")

    def quantile(self, q):
        """Estimate by linear interpolation inside the bucket that holds rank q * total.
        The first bucket starts at 0. If the rank falls in the overflow bucket return BOUNDS[-1]."""
        raise NotImplementedError("TODO step 2")


def stalls_per_minute(p, hz):
    raise NotImplementedError("TODO step 3")


def share_of_seconds_with_stall(p, hz):
    raise NotImplementedError("TODO step 3")


def stall_alert(ticks_by_zone, hz=20, budget=50, max_per_min=2, window_min=5):
    """Return the sorted list of zones where some rolling window of window_min minutes
    contains more than max_per_min * window_min ticks over budget."""
    raise NotImplementedError("TODO step 4")


if __name__ == "__main__":
    import zones
    data = zones.all_zones()
    for z, ticks in data.items():
        h = TickHistogram()
        for t in ticks:
            h.observe(t)
        p = h.count_over(50) / h.total
        print(f"{z:10} mean {h.sum / h.total:5.1f}  p99 {h.quantile(0.99):5.1f}  "
              f"p99.9 {nearest_rank(ticks, 0.999):4}  stalls/min {stalls_per_minute(p, zones.HZ):5.2f}")
    print("alert:", stall_alert(data))
