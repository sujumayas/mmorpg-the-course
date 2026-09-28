"""CS101 Lab 08: input you can trust.

Standard-library Python 3.10+. Run the tests with:  python test_lab08.py

Part A (you write): edge detection, the two-timer jump model in seconds and in
frames, and approach().
Part B (done for you): scenario runners that replay one jump attempt frame by
frame, and a loader for attempts.csv.
Part C (you run): the experiments on the lab sheet.
"""
import csv
from pathlib import Path

BIG = 999.0

# ---------------------------------------------------------------- Part A ---

def edges(held):
    """Given a list of booleans (held or not, one per frame), return a pair of
    lists (just_pressed, just_released), same length. Before frame 0 the
    button counts as not held."""
    raise NotImplementedError


class JumpInput:
    """Coyote time and jump buffer, both in SECONDS (lecture section 3)."""

    def __init__(self, coyote=0.1, buffer=0.1):
        self.coyote = coyote
        self.buffer = buffer
        self.was_held = False
        self.since_ground = BIG
        self.since_press = BIG

    def update(self, held, grounded, dt):
        """Advance one frame. Return True if the character jumps this frame.
        since_ground is 0 on grounded frames, else grows by dt.
        since_press is 0 on just-pressed frames, else grows by dt.
        Jump when since_ground <= coyote and since_press <= buffer, then set
        both timers to BIG so one press gives one jump."""
        raise NotImplementedError


class JumpInputFrames:
    """The same model, but the windows are whole FRAMES and the timers count
    frames instead of seconds. dt is accepted and ignored."""

    def __init__(self, coyote_frames=6, buffer_frames=6):
        self.coyote = coyote_frames
        self.buffer = buffer_frames
        self.was_held = False
        self.since_ground = 10**9
        self.since_press = 10**9

    def update(self, held, grounded, dt):
        raise NotImplementedError


def approach(value, target, max_step):
    """Move value toward target by at most max_step (>= 0). Never overshoot."""
    raise NotImplementedError


def frames_to_top_speed(max_speed, accel, fps):
    """Start at speed 0 and call approach(speed, max_speed, accel / fps) once
    per frame. Return how many frames until speed == max_speed."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part B ---

def run_ledge(jumper, fps, press_after, frames=60):
    """Character leaves the ground after frame 0. Jump is pressed (and then
    held) from the first frame k with k*dt >= press_after. press_after may be
    negative (pressed while still on the ground; then frames before 0 are
    simulated too). Returns the time in seconds at which the jump fired, or
    None if the character fell."""
    dt = 1 / fps
    start = min(0, int(press_after * fps) - 2)
    for k in range(start, frames):
        t = k * dt
        grounded = k <= 0
        held = t >= press_after - 1e-9
        if jumper.update(held, grounded, dt):
            return round(t, 6)
    return None


def run_landing(jumper, fps, press_before_landing, frames=60):
    """Character is airborne and lands on frame 0. Jump is pressed (and held)
    from the first frame k with k*dt >= offset, where offset is negative for
    an early press. Returns the fire time or None."""
    dt = 1 / fps
    offset = press_before_landing
    start = min(-round(0.5 * fps), int(offset * fps) - 2)
    for k in range(start, frames):
        t = k * dt
        grounded = k >= 0
        held = t >= offset - 1e-9
        if jumper.update(held, grounded, dt):
            return round(t, 6)
    return None


def load_attempts(path=Path(__file__).with_name("attempts.csv")):
    """Return a list of (attempt, kind, offset_seconds) from attempts.csv."""
    with open(path, newline="") as f:
        return [(int(r["attempt"]), r["kind"], float(r["press_offset_s"]))
                for r in csv.DictReader(f)]


# ---------------------------------------------------------------- Part C ---

if __name__ == "__main__":
    attempts = load_attempts()
    for label, make in [("strict", lambda: JumpInput(0.0, 0.0)),
                        ("C=B=0.1 s", lambda: JumpInput(0.1, 0.1))]:
        ok = 0
        for _, kind, off in attempts:
            run = run_ledge if kind == "ledge" else run_landing
            ok += run(make(), 60, off) is not None
        print(f"{label:10s} {ok}/{len(attempts)} attempts jumped at 60 fps")
