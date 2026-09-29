"""AU101 Lab 08: vertical layering driven by an intensity parameter.

Run:    python layers.py                 (prints the gain table)
        python layers.py render out.wav  (renders 32 s of layered music)
Test:   python -m unittest test_layers -v

Fill in every function marked TODO. The docstrings define what each returns.
All music here is generated from sine waves and noise, so there is nothing to license.
"""
import math
import random
import struct
import sys
import wave

SR = 22050            # samples per second
BPM = 120
BEAT = 60 / BPM       # 0.5 s
BAR = 4 * BEAT        # 2 s, 4/4 time
LOOP_BARS = 4         # every stem is exactly 4 bars (8 s) long

# (name, threshold a, fade width w). a = None means "always on" (the bed).
STEMS = [
    ("pad", None, None),
    ("drums", 0.2, 0.2),
    ("bass", 0.45, 0.2),
    ("lead", 0.7, 0.2),
]


def stem_gain(x, a, w):
    """Linear ramp: 0 below a, 1 at or above a + w, straight line between.
    If a is None the stem is the bed and always returns 1.0."""
    # TODO (Part A, step 2)
    raise NotImplementedError


def equal_power(r):
    """Reshape a 0..1 ramp value so that a fade keeps power steady: sin(r * pi / 2)."""
    return math.sin(max(0.0, min(1.0, r)) * math.pi / 2)


def level_db(gains):
    """Loudness of the sum, in dB relative to one stem at full gain, assuming
    equally loud, uncorrelated stems: 10 * log10(sum of squared gains).
    Return -inf if every gain is 0."""
    # TODO (Part A, step 4)
    raise NotImplementedError


def smooth(current, target, up_rate, down_rate, dt):
    """Move current toward target by at most up_rate * dt when rising and
    down_rate * dt when falling. Never overshoot the target."""
    # TODO (Part B, step 6)
    raise NotImplementedError


# ---------- synthesis (complete; no changes needed) ----------

A_MINOR = [220.0, 261.63, 329.63]          # A3 C4 E4
CHORDS = [A_MINOR, [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [164.81, 207.65, 246.94]]
BASS_ROOTS = [110.0, 87.31, 98.0, 82.41]    # A2 F2 G2 E2
LEAD = [440.0, 523.25, 587.33, 659.26, 587.33, 523.25, 493.88, 440.0]


def _stem_sample(name, t, rng_noise):
    """One sample of one stem at loop time t (0 <= t < 8 s)."""
    bar = int(t // BAR) % LOOP_BARS
    tb = t % BEAT                          # time since the last beat
    if name == "pad":
        return 0.12 * sum(math.sin(2 * math.pi * f * t) for f in CHORDS[bar])
    if name == "drums":
        kick = math.sin(2 * math.pi * (50 + 60 * math.exp(-tb * 30)) * tb) * math.exp(-tb * 12)
        te = t % (BEAT / 2)
        hat = rng_noise * math.exp(-te * 60) * 0.25
        return 0.45 * kick + hat
    if name == "bass":
        te = t % (BEAT / 2)
        f = BASS_ROOTS[bar] * (2 if int(t / (BEAT / 2)) % 4 == 3 else 1)
        env = math.exp(-te * 6)
        return 0.3 * env * sum(math.sin(2 * math.pi * f * k * t) / k for k in (1, 2, 3))
    if name == "lead":
        step = int(t / BEAT) % len(LEAD)
        env = min(1.0, tb * 40) * math.exp(-tb * 3)
        f = LEAD[step]
        return 0.18 * env * (math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * 3 * f * t))
    raise ValueError(name)


def render(intensity_at, seconds, path, sr=SR, up_rate=0.5, down_rate=0.1):
    """Render the four stems, all sample-aligned from t = 0, mixed by the
    smoothed intensity. intensity_at(t) returns the game's target intensity."""
    rng = random.Random(8)
    x = intensity_at(0.0)
    dt = 1 / sr
    frames = bytearray()
    peak = 0.0
    for n in range(int(seconds * sr)):
        t = n * dt
        x = smooth(x, intensity_at(t), up_rate, down_rate, dt)
        lt = t % (LOOP_BARS * BAR)
        noise = rng.uniform(-1, 1)
        s = 0.0
        for name, a, w in STEMS:
            g = stem_gain(x, a, w)
            if g > 0:
                s += g * _stem_sample(name, lt, noise)
        s *= 0.5                           # master trim: 6 dB of headroom for all four stems
        peak = max(peak, abs(s))
        frames += struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767))
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(bytes(frames))
    return peak


def demo_intensity(t):
    """A fight: calm for 8 s, enemies spot you, the fight peaks, then it ends."""
    if t < 8:
        return 0.1
    if t < 12:
        return 0.55
    if t < 22:
        return 1.0
    return 0.0


def main():
    try:
        print(f"{'x':>5} " + " ".join(f"{n:>6}" for n, _, _ in STEMS) + f" {'level dB':>9}")
        for x in (0.0, 0.25, 0.3, 0.5, 0.6, 0.8, 0.9, 1.0):
            gs = [stem_gain(x, a, w) for _, a, w in STEMS]
            print(f"{x:>5.2f} " + " ".join(f"{g:>6.2f}" for g in gs) + f" {level_db(gs):>9.2f}")
        if len(sys.argv) >= 3 and sys.argv[1] == "render":
            peak = render(demo_intensity, 32, sys.argv[2])
            print(f"wrote {sys.argv[2]}, peak {peak:.2f} (1.00 = full scale)")
    except NotImplementedError:
        print("Some functions are still TODO. Run the tests to see which.")


if __name__ == "__main__":
    main()
