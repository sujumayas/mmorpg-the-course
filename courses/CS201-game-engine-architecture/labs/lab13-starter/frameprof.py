"""CS201 Lab 13 starter: a small frame profiler and the numbers that go with it.

Run `python frameprof.py` to profile one simulated frame and a two-second capture.
Parts you have not written yet print a dash. The provided parts are:

- FakeClock and Profiler: scoped timing that records (name, tid, depth, start_us, end_us).
- simulated_frame(): the lecture's frame, profiled on a main thread and a render thread.
- capture(): 120 frames of per-thread totals from a simulated level, with hitches.

You write the six functions marked TODO. Profiler events are in integer microseconds;
the overhead and sampling functions work in nanoseconds, as in the lecture.
"""
from contextlib import contextmanager
import json

MAIN, RENDER = 1, 2  # thread ids used by the simulation


class FakeClock:
    """A clock you advance by hand, so every run prints the same numbers."""

    def __init__(self, start=0):
        self.now = start

    def __call__(self):
        return self.now

    def work(self, us):
        self.now += us


class Profiler:
    """Scoped instrumentation. One Profiler per thread, sharing a list of events."""

    def __init__(self, clock, tid=MAIN, events=None):
        self.clock = clock
        self.tid = tid
        self.events = [] if events is None else events
        self.depth = 0

    @contextmanager
    def scope(self, name):
        start = self.clock()
        self.depth += 1
        try:
            yield
        finally:
            self.depth -= 1
            self.events.append((name, self.tid, self.depth, start, self.clock()))


# The lecture's frame after the render-thread split (section 2), in microseconds.
GAME_WORK = [("input", 400, []),
             ("gameplay", 3_600, [("scripts", 2_700), ("triggers", 900)]),
             ("ai", 2_000, []),
             ("physics", 3_000, [("broadphase", 900), ("solver", 1_500)]),
             ("animation", 2_200, []),
             ("audio", 500, []),
             ("ui", 1_000, [])]
RENDER_WORK = [("render_submit", 4_100, [("cull", 1_300), ("draw_calls", 2_800)])]


def _run(prof, clock, work):
    with prof.scope("frame"):
        for name, total, children in work:
            with prof.scope(name):
                own = total - sum(us for _, us in children)
                clock.work(own)
                for child, us in children:
                    with prof.scope(child):
                        clock.work(us)


def simulated_frame():
    """Profile one frame on two threads. Returns the shared event list."""
    events = []
    main_clock, render_clock = FakeClock(), FakeClock()
    _run(Profiler(main_clock, MAIN, events), main_clock, GAME_WORK)
    _run(Profiler(render_clock, RENDER, events), render_clock, RENDER_WORK)
    return events


def capture(frames=120):
    """Per-frame thread totals (us) for a level that streams a chunk every 40 frames."""
    rows = []
    for f in range(frames):
        game = 12_700 + (f % 7) * 150          # small frame-to-frame noise
        gpu = 11_000 + (f % 5) * 200
        if f % 40 == 39:                        # streaming hitch on the game thread
            game += 21_000
        rows.append({"game": game, "render": 4_100, "gpu": gpu})
    return rows


# ---------------------------------------------------------------- TODO 1
def self_times(events):
    """Return {name: self_us} summed over all events with that name.

    Self time = inclusive time minus the inclusive time of direct children
    (same tid, depth + 1, starting and ending inside the parent).
    """
    raise NotImplementedError("self_times")


# ---------------------------------------------------------------- TODO 2
def correct_overhead(measured_ns, calls, overhead_ns):
    """Remove instrumentation overhead: {name: measured - calls * overhead}, never below 0.

    measured_ns and calls are dicts keyed by function name. Use the lecture's model
    measured = true + n * o. Return integer or float ns exactly as the arithmetic gives.
    """
    raise NotImplementedError("correct_overhead")


# ---------------------------------------------------------------- TODO 3
def frames_needed(t_ns, rate_hz, error_pct):
    """Frames of capture a sampling profiler needs to measure a function to +-error_pct.

    The function takes t_ns per frame; the sampler takes rate_hz samples per second
    of running time. It needs k = 1 / e**2 samples in the function, e = error_pct / 100.
    Return the smallest whole number of frames. Use integer arithmetic (no floats).
    """
    raise NotImplementedError("frames_needed")


# ---------------------------------------------------------------- TODO 4
def bottleneck(threads):
    """Given {"game": us, "render": us, "gpu": us}, return (name, us) of the slowest."""
    raise NotImplementedError("bottleneck")


# ---------------------------------------------------------------- TODO 5
def percentile(values, p):
    """Nearest-rank percentile: sort, then take item ceil(p/100 * n) (1-based)."""
    raise NotImplementedError("percentile")


# ---------------------------------------------------------------- TODO 6
def to_trace(events, pid=1):
    """Convert events to a Chrome JSON trace: a list of B and E dicts.

    Each dict has name, ph ("B" or "E"), ts (us), pid and tid. Group by tid, then
    order by ts within a thread. When several events share a ts, every E comes before every B; among Bs the outer
    scope (smaller depth) comes first; among Es the inner scope comes first.
    """
    raise NotImplementedError("to_trace")


def _try(fn, *args):
    try:
        return fn(*args)
    except NotImplementedError:
        return None


if __name__ == "__main__":
    ev = simulated_frame()
    st = _try(self_times, ev)
    print("self time per scope (us):", "-" if st is None else st)
    rows = capture()
    game = [r["game"] for r in rows]
    worst = max(rows, key=lambda r: r["game"])
    print("slowest thread in the worst frame:", _try(bottleneck, worst) or "-")
    print("p50 / p99 game thread (us):", _try(percentile, game, 50) or "-",
          "/", _try(percentile, game, 99) or "-")
    deep = {"update_transform": 2_200_000, "vec_normalize": 2_400_000}
    calls = {"update_transform": 20_000, "vec_normalize": 40_000}
    print("deep profile corrected for 50 ns scopes (ns):", _try(correct_overhead, deep, calls, 50) or "-")
    print("frames to measure vec_normalize to +-10% at 8 kHz:", _try(frames_needed, 400_000, 8_000, 10) or "-")
    trace = _try(to_trace, ev)
    if trace is not None:
        with open("frame_trace.json", "w") as fh:
            json.dump(trace, fh, indent=1)
        print(f"wrote frame_trace.json with {len(trace)} events; open it at ui.perfetto.dev")
    else:
        print("trace: -")
