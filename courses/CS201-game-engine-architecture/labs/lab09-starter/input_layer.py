"""CS201 Lab 09: an event-built input layer.

Fill in every function marked TODO. Each docstring says exactly what
check_lab09.py expects. Standard library only, Python 3.10 or later.
Times are integer microseconds throughout, so no float comparisons are needed.
"""
import csv
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    time_us: int
    kind: str            # "down", "up", "move" or "focus_lost"
    key: str = ""        # for down/up
    dx: int = 0          # for move
    dy: int = 0


def load_session(path):
    """Provided: read session.csv into a list of Events, in file order."""
    events = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            t, kind, data = int(row["time_us"]), row["kind"], row["data"]
            if kind == "move":
                dx, dy = (int(v) for v in data.split())
                events.append(Event(t, kind, dx=dx, dy=dy))
            else:
                events.append(Event(t, kind, key=data))
    return events


def sampled_presses(events, frame_us, duration_us=30_000_000):
    """Provided: the WRONG way, for comparison.

    Samples the held state of every key at t = 0, frame_us, 2*frame_us, ...
    and counts a press whenever a key is held at a sample but was not held at
    the previous sample (CS101 week 8's edge detection). Returns {key: count}.
    """
    held, counts, i = set(), {}, 0
    prev = set()
    for sample in range(0, duration_us + 1, frame_us):
        while i < len(events) and events[i].time_us <= sample:
            e = events[i]
            if e.kind == "down":
                held.add(e.key)
            elif e.kind == "up":
                held.discard(e.key)
            i += 1
        for k in held - prev:
            counts[k] = counts.get(k, 0) + 1
        prev = set(held)
    return counts


# ---------------------------------------------------------------------------
# Part A: the frame summary (lecture section 3)
# ---------------------------------------------------------------------------

class InputFrame:
    """Per-frame input state built from events.

    held(key)         True if the key is down after the last applied event
    presses(key)      number of "down" events for key since begin_frame()
    releases(key)     number of "up" events for key since begin_frame()
    just_pressed(key) presses(key) > 0
    mouse             (dx, dy) summed over all "move" events since begin_frame()

    A "focus_lost" event releases every held key: for each held key, count a
    release and mark it not held.
    """

    def __init__(self):
        self._held = set()
        self._presses = {}
        self._releases = {}
        self.mouse = (0, 0)

    def begin_frame(self):
        """Clear per-frame counts and mouse motion. Keep held keys."""
        raise NotImplementedError("TODO A1: begin_frame")

    def apply(self, event):
        raise NotImplementedError("TODO A2: apply")

    def held(self, key):
        return key in self._held

    def presses(self, key):
        return self._presses.get(key, 0)

    def releases(self, key):
        return self._releases.get(key, 0)

    def just_pressed(self, key):
        return self.presses(key) > 0


def event_presses(events, frame_us):
    """Run frames at t = 0, frame_us, 2*frame_us, ... until every event has
    been applied. At the start of each frame, call begin_frame() and then apply
    every event with time_us <= the frame's start time that has not been
    applied yet (so the frame at t = frame_us sees everything that happened in
    (0, frame_us]). Events are sorted by time. Sum presses(key) over all frames
    and return {key: total}.

    Must return the same totals for any frame_us, because no event is lost.
    """
    raise NotImplementedError("TODO A3: event_presses")


# ---------------------------------------------------------------------------
# Part B: action maps with rebinding
# ---------------------------------------------------------------------------

class ActionMap:
    """Maps physical keys to action names for one context.

    `bindings` is a dict action -> list of keys, as loaded from a data file,
    for example {"jump": ["space", "j"], "attack": ["k"]}.
    """

    def __init__(self, bindings):
        self.bindings = {a: list(keys) for a, keys in bindings.items()}

    def action_for(self, key):
        """The action bound to key, or None. If two actions claim the same key,
        raise ValueError naming both actions (a map must be unambiguous)."""
        raise NotImplementedError("TODO B1: action_for")

    def rebind(self, action, old_key, new_key):
        """Replace old_key with new_key in action's list. If new_key is already
        bound to a DIFFERENT action, remove it from that action first (the
        new binding wins), and return the name of the action that lost it, or
        None if nothing lost a key. Unknown action or old_key: ValueError."""
        raise NotImplementedError("TODO B2: rebind")


# ---------------------------------------------------------------------------
# Part C: the context stack with press ownership
# ---------------------------------------------------------------------------

class Context:
    """A handler on the input stack. Provided, do not change."""

    def __init__(self, name, action_map, eats_everything=False):
        self.name = name
        self.map = action_map
        self.eats_everything = eats_everything
        self.held = set()        # actions (or raw keys, if unbound) this context thinks are held
        self.log = []            # (kind, action or key) in the order received

    def wants(self, key):
        return self.eats_everything or self.map.action_for(key) is not None

    def handle(self, kind, key):
        name = self.map.action_for(key) or key
        self.log.append((kind, name))
        if kind == "down":
            self.held.add(name)
        else:
            self.held.discard(name)


class Router:
    """Routes down/up events to the top context that wants them.

    stack[-1] is the top. Rules the checker tests:
    - A "down" goes to the topmost context that wants the key. That context
      becomes the key's owner. If nobody wants it, it is dropped.
    - An "up" goes to the key's owner (press ownership), whatever is on top
      now, and clears the ownership. An up for a key with no owner is dropped.
    - focus_lost(): send an "up" to the owner of every owned key, in
      alphabetical key order, and clear all ownership.
    - pop(): before removing the top context, send an "up" to it for every key
      it owns (alphabetical order), and clear those ownerships.
    """

    def __init__(self):
        self.stack = []
        self.owner = {}

    def push(self, ctx):
        self.stack.append(ctx)

    def pop(self):
        raise NotImplementedError("TODO C1: pop")

    def route(self, kind, key):
        raise NotImplementedError("TODO C2: route")

    def focus_lost(self):
        raise NotImplementedError("TODO C3: focus_lost")
