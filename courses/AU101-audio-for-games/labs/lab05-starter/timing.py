"""AU101 Lab 05: trigger timing.

Standard-library Python 3.10+. Run `python timing.py` once Part A is done to render
three click tracks. Run `python test_lab05.py` to check your work.

All times are fractions.Fraction seconds. Use Fraction arithmetic everywhere:
floats make ceil() wrong at exact frame boundaries (lecture section 2).

Part A: the three trigger strategies and the mix-chunk grid.
Part B: measuring (gaps, average rate, worst error).
Part C: footsteps by distance.
Part D: rendering (provided).
"""
import math
import struct
import wave
from fractions import Fraction

SAMPLE_RATE = 48000


# ---------------------------------------------------------------- Part A: strategies

def period(rpm):
    """Seconds between shots for a weapon firing `rpm` rounds per minute."""
    return Fraction(60, rpm)


def reset_times(rpm, fps, shots):
    """Reset cooldown: every gap is ceil(T / frame) whole frames.
    Returns `shots` start times, the first at 0."""
    raise NotImplementedError


def carry_times(rpm, fps, shots):
    """Carry cooldown: shot k plays on the first frame boundary at or after k * T."""
    raise NotImplementedError


def audio_clock_times(rpm, shots, lookahead):
    """Audio-clock scheduling: shot k plays at lookahead + k * T.
    `lookahead` is a Fraction of a second."""
    raise NotImplementedError


def snap_to_chunks(times, chunk, sample_rate=SAMPLE_RATE):
    """The mixer starts sounds only at chunk boundaries: round every time UP to the
    next multiple of chunk / sample_rate seconds (a time exactly on a boundary stays)."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part B: measuring

def gaps_ms(times):
    """Gaps between consecutive times, in milliseconds, as floats rounded to 1 decimal."""
    raise NotImplementedError


def average_rpm(times):
    """Average rate over the burst: (number of gaps) shots per (last - first) seconds,
    in rounds per minute, as a float. Needs at least 2 times."""
    raise NotImplementedError


def worst_error_ms(intended, actual):
    """Largest |actual - intended| over matching pairs, in ms, as a float.
    For audio-clock times, subtract the lookahead first if you want the rhythm error only."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part C: footsteps

def distance_steps(speeds, fps, stride):
    """Footsteps by distance (the accumulator from CS101 week 9, in metres).

    speeds: one speed in m/s per frame (numbers or Fractions).
    Each frame: walked += speed * (1 / fps); while walked >= stride: record a step
    at this frame's index and subtract stride.
    Returns the list of frame indices with a step (an index appears twice if two
    steps land in one frame)."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part D: rendering (provided)

def _click():
    n = int(0.025 * SAMPLE_RATE)
    return [math.sin(2 * math.pi * 2000 * i / SAMPLE_RATE) * math.exp(-i / (0.005 * SAMPLE_RATE))
            for i in range(n)]


def render_clicks(times, path):
    """Write a mono 16-bit WAV with one click at each time (Fraction seconds)."""
    click = _click()
    starts = [round(t * SAMPLE_RATE) for t in times]
    mix = [0.0] * (max(starts) + len(click))
    for s in starts:
        for i, c in enumerate(click):
            mix[s + i] += c
    peak = max(abs(x) for x in mix) or 1.0
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(struct.pack("<h", int(0.8 * x / peak * 32767)) for x in mix))


def main():
    rpm, fps, shots = 800, 30, 24
    tracks = {
        "reset_30fps.wav": reset_times(rpm, fps, shots),
        "carry_30fps.wav": carry_times(rpm, fps, shots),
        "audio_clock.wav": audio_clock_times(rpm, shots, Fraction(1, 20)),
    }
    for name, times in tracks.items():
        render_clicks(times, name)
        print(f"{name:<16} {average_rpm(times):7.1f} rpm  gaps {gaps_ms(times)[:6]} ...")


if __name__ == "__main__":
    main()
