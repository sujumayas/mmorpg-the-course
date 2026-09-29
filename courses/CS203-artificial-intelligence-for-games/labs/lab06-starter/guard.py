"""CS203 Lab 06 starter: a guard NPC as a table-driven state machine.

The world calls machine.step(inputs) once per AI tick (10 ticks per second).
inputs is a dict:
    sees      True if the guard can see the player this tick
    seen_ago  ticks since the guard last saw the player (0 while visible)
    dist      distance to the player's last known position, in meters

Run:   python guard.py            prints the state timeline for each trace
Check: python check_lab06.py      exits 0 only when your work is complete

Part A: finish Machine.step().  Part B: fix GUARD_TRANSITIONS and MIN_DWELL
so the guard meets the behaviour requirements in the lab handout.
"""
import math
import sys


class Transition:
    def __init__(self, src, dst, guard, interrupt=False):
        self.src, self.dst, self.guard, self.interrupt = src, dst, guard, interrupt


class Machine:
    def __init__(self, start, transitions, min_dwell=None, on_enter=None, on_exit=None):
        self.state = start
        self.transitions = transitions
        self.min_dwell = min_dwell or {}
        self.on_enter = on_enter or (lambda state: None)
        self.on_exit = on_exit or (lambda state: None)
        self.tick = 0
        self.time_in_state = 0
        self.log = []            # (tick, src, dst) for every transition

    def step(self, inputs):
        """TODO Part A. Advance the machine by one tick.

        1. Look at the transitions whose src is the current state, in list order.
        2. A transition may fire only if its guard(inputs, self) is true AND
           (it is an interrupt OR time_in_state >= min_dwell for the current state,
           default 0).
        3. The first one that may fire wins. Call on_exit(src), then on_enter(dst),
           append (tick, src, dst) to log, switch state, set time_in_state to 0.
           At most one transition per tick.
        4. Finally, whether or not anything fired, add 1 to time_in_state and
           to tick. Return the current state.
        """
        raise NotImplementedError("write Machine.step() in Part A")


# ------------------------------------------------------------ the guard (Part B)

ATTACK_RANGE = 2.0

# This first draft is what a designer wrote in five minutes. Every rule uses a
# single threshold and nothing has a minimum dwell. Run the traces and watch it.
GUARD_TRANSITIONS = [
    Transition("PATROL", "CHASE",  lambda i, m: i["sees"]),
    Transition("CHASE",  "ATTACK", lambda i, m: i["sees"] and i["dist"] <= ATTACK_RANGE),
    Transition("CHASE",  "SEARCH", lambda i, m: i["seen_ago"] > 0),
    Transition("ATTACK", "SEARCH", lambda i, m: i["seen_ago"] > 0),
    Transition("ATTACK", "CHASE",  lambda i, m: i["dist"] > ATTACK_RANGE),
    Transition("SEARCH", "CHASE",  lambda i, m: i["sees"]),
    Transition("SEARCH", "PATROL", lambda i, m: m.time_in_state >= 1),
]

MIN_DWELL = {}


def make_guard():
    return Machine("PATROL", GUARD_TRANSITIONS, MIN_DWELL)


# ------------------------------------------------------------ test traces


def with_memory(frames):
    """Fill in seen_ago from the sees flags."""
    seen_ago = 10_000
    for f in frames:
        seen_ago = 0 if f["sees"] else seen_ago + 1
        f["seen_ago"] = seen_ago
    return frames


def strafe_trace(ticks=300):
    """The player circle-strafes at the edge of attack range, ducking behind
    a pillar for 2 ticks out of every 17."""
    frames = []
    for t in range(ticks):
        dist = ATTACK_RANGE + 0.6 * math.sin(t * 0.9) + 0.3 * math.sin(t * 2.3)
        frames.append({"sees": t % 17 not in (15, 16), "dist": round(dist, 3)})
    return with_memory(frames)


def approach_trace():
    """Unseen for 10 ticks, then walks straight at the guard from 10 m at
    0.25 m per tick and stops at 1 m."""
    frames = []
    for t in range(80):
        if t < 10:
            frames.append({"sees": False, "dist": 10.0})
        else:
            frames.append({"sees": True, "dist": max(1.0, 10.0 - 0.25 * (t - 10))})
    return with_memory(frames)


def escape_trace():
    """Seen at 6 m for 60 ticks, then gone for good (the player hid)."""
    frames = [{"sees": t < 60, "dist": 6.0} for t in range(220)]
    return with_memory(frames)


def juke_trace():
    """In melee at 1.5 m from the start, dashes out to 4 m on ticks 4-6,
    comes back, then really leaves (5 m) from tick 25 on."""
    frames = []
    for t in range(40):
        dist = 4.0 if 4 <= t <= 6 else (5.0 if t >= 25 else 1.5)
        frames.append({"sees": True, "dist": dist})
    return with_memory(frames)


def run(machine, frames):
    return [machine.step(f) for f in frames]


def timeline(states):
    """Compress a list of states into 'STATE xN' runs."""
    out, prev, n = [], None, 0
    for s in states + [None]:
        if s == prev:
            n += 1
            continue
        if prev is not None:
            out.append(f"{prev} x{n}")
        prev, n = s, 1
    return ", ".join(out)


def main():
    for name, trace in [("strafe", strafe_trace()), ("approach", approach_trace()),
                        ("escape", escape_trace()),
                        ("juke", juke_trace())]:
        guard = make_guard()
        try:
            states = run(guard, trace)
        except NotImplementedError as exc:
            print(f"{name}: not finished ({exc})")
            continue
        print(f"{name}: {len(guard.log)} transitions")
        print("   ", timeline(states))
    return 0


if __name__ == "__main__":
    sys.exit(main())
