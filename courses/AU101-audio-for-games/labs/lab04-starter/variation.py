"""AU101 Lab 04: the variation engine.

Standard-library Python 3.10+. Run `python variation.py` to render two WAV files
once Part A and Part B are done. Run `python test_lab04.py` to check your work.

Part A: the model from lecture section 2 (pure functions, no randomness inside).
Part B: picking and planning (randomness comes in through an `rng` argument).
Part C: synthesis and rendering. Provided; read it, you will change the sound in step 6.
"""
import math
import random
import struct
import wave
from dataclasses import dataclass

SAMPLE_RATE = 44100


# ---------------------------------------------------------------- Part A: the model

def semitones_to_ratio(semitones):
    """Playback-rate multiplier for a pitch shift in semitones: 2 ** (s / 12).
    semitones_to_ratio(12) == 2.0, semitones_to_ratio(-12) == 0.5."""
    raise NotImplementedError


def db_to_gain(db):
    """Amplitude multiplier for a level change in decibels: 10 ** (dB / 20).
    db_to_gain(0) == 1.0, db_to_gain(-6) is about 0.501."""
    raise NotImplementedError


def repeat_chance(weights):
    """Chance that two plays in a row give the same outcome.
    `weights` are non-negative numbers, one per outcome (they need not sum to 1).
    R = sum of (w / total) ** 2. repeat_chance([1, 1, 1, 1]) == 0.25."""
    raise NotImplementedError


def burst_repeat_probability(r, shots):
    """Chance of at least one exact repeat between neighbours in a burst of `shots`
    plays, when each neighbouring pair repeats with probability r.
    A burst of 0 or 1 shots has no pairs, so the answer is 0."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part B: picking and planning

class NoRepeatPicker:
    """Picks an index in range(n). If no_repeat is True and n >= 2, never returns
    the same index twice in a row (reroll until different). With n == 1 it always
    returns 0. Randomness comes only from the rng passed to pick()."""

    def __init__(self, n, no_repeat=True):
        self.n = n
        self.no_repeat = no_repeat
        self.last = None

    def pick(self, rng):
        raise NotImplementedError


@dataclass
class Shot:
    variants: tuple      # one variant index per layer, e.g. (2, 0, 3)
    semitones: float     # pitch offset applied to the whole shot
    gain_db: float       # level offset, always <= 0


def plan_burst(layer_sizes, shots, pitch_range, vol_drop_db, rng, no_repeat=False):
    """Return a list of `shots` Shot objects.

    layer_sizes: number of variants per layer, e.g. [4, 4, 4].
    pitch_range: each shot's pitch is uniform in [-pitch_range, +pitch_range].
    vol_drop_db: each shot's gain is uniform in [-vol_drop_db, 0] (downward only).
    no_repeat:   use one NoRepeatPicker per layer with this setting.

    Draw in this order for every shot, so results are reproducible:
    each layer's variant (layer 0 first), then pitch, then gain.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- Part C: synthesis (provided)

def _noise(seed, n):
    g = random.Random(seed)
    return [g.uniform(-1.0, 1.0) for _ in range(n)]


def _one_pole_lowpass(x, cutoff):
    a = math.exp(-2 * math.pi * cutoff / SAMPLE_RATE)
    y, out = 0.0, []
    for s in x:
        y = (1 - a) * s + a * y
        out.append(y)
    return out


def _highpass(x, cutoff):
    low = _one_pole_lowpass(x, cutoff)
    return [s - l for s, l in zip(x, low)]


def _decay(x, tau):
    return [s * math.exp(-i / (tau * SAMPLE_RATE)) for i, s in enumerate(x)]


def make_layers():
    """Three layers x four variants, all generated from seeds. Returns a list of
    layers, each a list of variant sample lists (floats in about -1..1)."""
    transient, body, tail = [], [], []
    for v in range(4):
        n = int(0.03 * SAMPLE_RATE)
        transient.append(_decay(_highpass(_noise(11 + v, n), 2000 + 400 * v), 0.004))
        n = int(0.15 * SAMPLE_RATE)
        f0, phase, sweep = 140 + 20 * v, 0.0, []
        for i in range(n):
            t = i / SAMPLE_RATE
            f = 50 + (f0 - 50) * math.exp(-t / 0.03)
            phase += 2 * math.pi * f / SAMPLE_RATE
            sweep.append(math.sin(phase))
        grit = _one_pole_lowpass(_noise(21 + v, n), 800)
        body.append(_decay([s + 0.25 * g for s, g in zip(sweep, grit)], 0.04))
        n = int(0.6 * SAMPLE_RATE)
        band = _highpass(_one_pole_lowpass(_noise(31 + v, n), 500 + 100 * v), 300)
        tail.append([0.35 * s for s in _decay(band, 0.15)])
    return [transient, body, tail]


def _resample(x, ratio):
    """Play x at `ratio` times normal speed (pitch and length change together)."""
    out, pos = [], 0.0
    last = len(x) - 1
    while pos < last:
        i = int(pos)
        frac = pos - i
        out.append(x[i] * (1 - frac) + x[i + 1] * frac)
        pos += ratio
    return out


def render(plan, layers, path, interval=4 / 35):
    """Mix the planned shots, `interval` seconds apart, into a 16-bit mono WAV.
    Uses layer k's variant plan[j].variants[k] for every layer the shot names.
    Returns the number of sample frames written."""
    starts = [round(j * interval * SAMPLE_RATE) for j in range(len(plan))]
    voices = []
    for start, shot in zip(starts, plan):
        ratio = semitones_to_ratio(shot.semitones)
        gain = db_to_gain(shot.gain_db)
        for layer, v in zip(layers, shot.variants):
            voices.append((start, [gain * s for s in _resample(layer[v], ratio)]))
    length = max(start + len(samples) for start, samples in voices)
    mix = [0.0] * length
    for start, samples in voices:
        for i, s in enumerate(samples):
            mix[start + i] += s
    peak = max(1e-9, max(abs(s) for s in mix))
    scale = 0.9 / peak
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * scale * 32767)) for s in mix))
    return length


def main():
    rng = random.Random(4)
    layers = make_layers()
    same = plan_burst([1], 10, 0.0, 0.0, rng)
    body_only = [layers[1]]
    render(same, body_only, "same_x10.wav")
    varied = plan_burst([4, 4, 4], 10, 1.0, 2.0, rng, no_repeat=True)
    render(varied, layers, "layered.wav")
    print("wrote same_x10.wav and layered.wav")
    print(f"R, same sample:       {repeat_chance([1]):.4f}")
    print(f"R, 3 layers x 4 each: {repeat_chance([1] * 4) ** 3:.4f}")


if __name__ == "__main__":
    main()
