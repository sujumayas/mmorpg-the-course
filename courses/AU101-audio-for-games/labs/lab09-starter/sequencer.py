"""AU101 Lab 09: a quantized music director (horizontal re-sequencing and stingers).

Run:   python sequencer.py          (prints the schedule for the demo fight)
Test:  python -m unittest test_sequencer -v

Fill in every function marked TODO. The docstrings define what each returns.
Time is in seconds from the moment the music started. Beat 0 is at t = 0.
"""
import math

BPM = 120
BEATS_PER_BAR = 4

# How many beats each sync unit spans. "immediate" means no waiting.
UNIT_BEATS = {"immediate": 0, "beat": 1, "bar": BEATS_PER_BAR, "phrase": 4 * BEATS_PER_BAR}

# Part B: your transition matrix. (from_state, to_state) -> sync unit.
# Any pair not listed uses DEFAULT_UNIT.
DEFAULT_UNIT = "bar"
TRANSITIONS = {
    ("explore", "combat"): "bar",
    ("explore", "boss"): "beat",
    ("combat", "explore"): "phrase",
    ("combat", "victory"): "beat",
    ("combat", "boss"): "bar",
    ("boss", "victory"): "beat",
    ("victory", "explore"): "phrase",
}


def unit_seconds(unit, bpm=BPM):
    """Length of one sync unit in seconds. "immediate" is 0."""
    return UNIT_BEATS[unit] * 60 / bpm


def next_sync(t, unit, bpm=BPM):
    """Earliest sync point at or after time t. A request that lands exactly on a
    boundary is served at that boundary. "immediate" returns t.
    Use a small tolerance (1e-9) so float noise does not skip a boundary."""
    # TODO (Part A, step 2)
    raise NotImplementedError


def expected_wait(unit, bpm=BPM):
    """Average wait if requests arrive at uniformly random times: half a unit."""
    return unit_seconds(unit, bpm) / 2


class Director:
    """Holds the current music state and at most one pending switch."""

    def __init__(self, state, transitions=None, bpm=BPM):
        self.state = state
        self.transitions = TRANSITIONS if transitions is None else transitions
        self.bpm = bpm
        self.pending = None          # (switch_time, target_state) or None
        self.log = []                # entries: (time, "switch", from, to) or (time, "stinger", name)

    def unit_for(self, src, dst):
        return self.transitions.get((src, dst), DEFAULT_UNIT)

    def request(self, t, target):
        """The game asks for music state `target` at time t.
        - If target is the current state, cancel any pending switch.
        - Otherwise set pending to (next_sync(t, unit), target), where unit comes
          from the transition (current state -> target). A newer request always
          replaces an older pending one."""
        # TODO (Part A, step 4)
        raise NotImplementedError

    def stinger(self, t, name):
        """Schedule a stinger on the next beat at or after t and log it as
        (time, "stinger", name). Stingers never change the state."""
        # TODO (Part A, step 5)
        raise NotImplementedError

    def advance(self, t):
        """Perform the pending switch if its time is at or before t."""
        if self.pending and self.pending[0] <= t:
            when, target = self.pending
            self.log.append((when, "switch", self.state, target))
            self.state = target
            self.pending = None


def run(events, start_state="explore", transitions=None, bpm=BPM):
    """events: list of (time, kind, value), kind "state" or "stinger".
    Returns the director's log sorted by time."""
    d = Director(start_state, transitions, bpm)
    for t, kind, value in sorted(events, key=lambda e: e[0]):
        d.advance(t)
        if kind == "state":
            d.request(t, value)
        elif kind == "stinger":
            d.stinger(t, value)
    d.advance(math.inf)
    return sorted(d.log, key=lambda e: e[0])


DEMO = [
    (3.3, "state", "combat"),      # enemy spots the player
    (3.3, "stinger", "spotted"),
    (9.1, "stinger", "crit"),
    (12.2, "state", "explore"),    # enemy loses track...
    (13.0, "state", "combat"),     # ...and finds the player again before the switch
    (20.6, "state", "victory"),
    (21.0, "state", "explore"),
]


def main():
    try:
        for unit in ("beat", "bar", "phrase"):
            print(f"{unit:<7} length {unit_seconds(unit):5.2f} s  expected wait {expected_wait(unit):5.2f} s")
        print()
        for entry in run(DEMO):
            print(f"{entry[0]:7.2f}  " + "  ".join(str(x) for x in entry[1:]))
    except NotImplementedError:
        print("Some functions are still TODO. Run the tests to see which.")


if __name__ == "__main__":
    main()
