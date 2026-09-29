"""AU101 Lab 10 starter: an HDR mix window, a ducker and a voice allocator.

Standard library only. Run the tests with

    python3 test_mixer.py

Every function below raises NotImplementedError until you write it. The
docstrings give the exact rules from the week 10 lecture. Levels are in dB,
times in seconds, rates in dB per second.
"""
import math
from dataclasses import dataclass


def db_sum(levels):
    """Level of several uncorrelated sounds played together.

    L_total = 10 * log10(sum(10 ** (L_i / 10))). Return float('-inf') for an
    empty list.
    """
    raise NotImplementedError("db_sum")


def hdr_target(active_levels, threshold):
    """Where the top of the HDR window wants to be right now.

    The loudest active level, but never below the threshold.
    """
    raise NotImplementedError("hdr_target")


def hdr_step(top_prev, active_levels, threshold, release, dt):
    """Move the window top for one time step.

    Attack is instant: if the target is at or above top_prev, jump to it.
    Release is limited: otherwise fall by at most release * dt, and never
    below the target.
    """
    raise NotImplementedError("hdr_step")


def hdr_output(level, top, window):
    """Output level in dBFS for one sound, or None if it falls below the window.

    out = level - top. The sound is audible when out >= -window.
    """
    raise NotImplementedError("hdr_output")


def duck_step(gain_prev, key_active, depth, attack_time, release_time, dt):
    """One step of a sidechain ducker, gain in dB (0 = no ducking).

    When the key (for example dialogue) is active, the gain moves toward
    -depth at depth / attack_time dB per second. When it is not, the gain moves
    back toward 0 at depth / release_time dB per second. Never overshoot.
    """
    raise NotImplementedError("duck_step")


@dataclass
class Request:
    name: str
    priority: float      # 1 (lowest) to 100 (highest), before distance offset
    distance: float      # metres from the listener
    start_time: float    # when it started; smaller = older


def effective_priority(priority, offset, distance, max_distance):
    """Priority after a linear distance offset.

    No offset at distance 0, the full offset at max_distance and beyond.
    offset is a positive number that is subtracted.
    """
    raise NotImplementedError("effective_priority")


def allocate(requests, limit, offset, max_distance, keep="oldest"):
    """Choose which requests get a real voice.

    Sort by effective priority, highest first. Among equal priorities keep
    the oldest (smallest start_time) when keep == "oldest", or the newest when
    keep == "newest". Return the names of the first `limit` requests, in that
    order.
    """
    raise NotImplementedError("allocate")


def run_scene(events, threshold, window, release, dt, t_end):
    """Simulate the lecture's scene and return a list of rows.

    events: list of (name, level, t_on, t_off). A sound is active when
    t_on <= t <= t_off (both ends included, so the release starts at t_off).
    Start with top = threshold and step with hdr_step.
    Each row is (t, top, {name: output or None}) for every active sound,
    sampled at t = 0, dt, 2*dt, ... while t <= t_end (use integer ticks).
    """
    raise NotImplementedError("run_scene")


# The lecture's scene. Levels in dB on an arbitrary in-game scale.
SCENE = [
    ("gunfire", 20, -1.0, 99.0),
    ("footsteps", 0, -1.0, 99.0),
    ("birds", -15, -1.0, 99.0),
    ("wind", -25, -1.0, 99.0),
    ("explosion", 45, 0.0, 0.5),
]

if __name__ == "__main__":
    try:
        for t, top, outs in run_scene(SCENE, threshold=0, window=48,
                                      release=20, dt=0.05, t_end=2.0):
            if round(t / 0.05) % 5 == 0:
                cells = ", ".join(f"{k} {'culled' if v is None else f'{v:+.0f}'}"
                                  for k, v in outs.items())
                print(f"t={t:4.2f}s top={top:5.1f}  {cells}")
    except NotImplementedError as e:
        print("Not written yet:", e)
