"""AU101 Lab 11 starter: render a UI sound family to WAV files.

Standard library only (math, struct, wave). Run the tests with

    python3 test_ui_sounds.py

and, once they pass, render your family with

    python3 ui_sounds.py

Functions marked TODO raise NotImplementedError until you write them.
`estimate_freq`, `peak_db` and `write_wav` are finished tools you can use.
"""
import math
import struct
import wave

SR = 48_000                               # samples per second
MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]        # semitone offsets of a major scale


# ---------------------------------------------------------------- TODO part A
def semitone_ratio(s):
    """Frequency (or playback-rate) ratio for s semitones: 2 ** (s / 12)."""
    raise NotImplementedError("semitone_ratio")


def ladder_semitones(n, scale=MAJOR, mode="cap"):
    """Semitone offset for the n-th hit of a streak (n starts at 1).

    mode "cap":  stay on the top step once the scale runs out.
    mode "wrap": start again from the bottom step (n = len(scale) + 1 -> scale[0]).
    mode "same": always 0 (the control condition).
    """
    raise NotImplementedError("ladder_semitones")


def streak_steps(times, reset_gap):
    """Step number for each event time. A gap strictly longer than
    reset_gap seconds since the previous event resets the streak to 1.

    streak_steps([0, 0.3, 0.6, 1.5, 1.7], 0.5) == [1, 2, 3, 1, 2]
    """
    raise NotImplementedError("streak_steps")


# ---------------------------------------------------------------- TODO part B
def render(f_start, f_end, dur, peak=-12.0, attack=0.005, release_frac=0.3, sr=SR):
    """A sine sweep from f_start to f_end Hz lasting dur seconds.

    - Exactly round(dur * sr) samples.
    - Frequency moves linearly from f_start to f_end; accumulate phase
      (phase += 2*pi*f/sr each sample) so the sweep has no clicks.
    - Envelope: linear rise over `attack` seconds, linear fall over the last
      release_frac * dur seconds, 1.0 in between.
    - Scale the result so its largest absolute sample is exactly
      10 ** (peak / 20) (peak in dBFS).
    Returns a list of floats in [-1, 1].
    """
    raise NotImplementedError("render")


def concat(*parts, gap=0.0, sr=SR):
    """Join sounds end to end with `gap` seconds of silence between them."""
    raise NotImplementedError("concat")


# ---------------------------------------------------------------- tools (done)
def peak_db(samples):
    """Largest absolute sample in dBFS."""
    m = max(abs(x) for x in samples)
    return 20 * math.log10(m) if m > 0 else float("-inf")


def estimate_freq(samples, sr=SR):
    """Average frequency from upward zero crossings (good for clean sines)."""
    ups = [i for i in range(1, len(samples)) if samples[i - 1] < 0 <= samples[i]]
    if len(ups) < 2:
        return 0.0
    return (len(ups) - 1) * sr / (ups[-1] - ups[0])


def write_wav(path, samples, sr=SR):
    """Write mono 16-bit PCM."""
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767))
                               for x in samples))


# ---------------------------------------------------------------- your family
# Part C: replace these placeholders with your own design and justify each
# row in your spec sheet. (f_start, f_end, dur, peak)
FAMILY = {
    "hover":   (1200, 1200, 0.03, -30),
    "click":   (900, 900, 0.06, -20),
    "confirm": (660, 990, 0.12, -14),
    "cancel":  (660, 440, 0.12, -14),
    "error":   (330, 311, 0.20, -12),
}

if __name__ == "__main__":
    try:
        for name, (a, b, d, p) in FAMILY.items():
            s = render(a, b, d, p)
            write_wav(f"{name}.wav", s)
            print(f"{name:8s} {len(s) / SR * 1000:5.0f} ms  peak {peak_db(s):6.1f} dBFS")
        streak = concat(*[render(523.25 * semitone_ratio(ladder_semitones(n)),
                                 523.25 * semitone_ratio(ladder_semitones(n)), 0.12, -14)
                          for n in range(1, 9)], gap=0.08)
        write_wav("streak.wav", streak)
        print("streak.wav written")
    except NotImplementedError as e:
        print("Not written yet:", e)
