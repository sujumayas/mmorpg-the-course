"""AU101 Lab 06: generate seamless procedural engine loops.

Usage:  python make_loops.py 1000 2000 4000
Writes engine_<rpm>.wav for each RPM (48 kHz, mono, 16-bit, about 2 s) and prints
the exact RPM each loop represents after rounding to a whole number of cycles.

The model engine is a four-cylinder four-stroke: it fires twice per revolution, so
the firing frequency is F = rpm / 60 * 2 Hz. The tone is harmonics 1-12 of F with
amplitudes 1/k and fixed phases, a slow amplitude wobble, and a little noise.
Standard library only. No recorded audio is used.
"""
import math
import random
import struct
import sys
import wave

SAMPLE_RATE = 48000
TARGET_SECONDS = 2.0


def engine_loop(rpm, seed=6):
    f = rpm / 60 * 2
    cycles = max(1, round(TARGET_SECONDS * f))
    n = round(cycles * SAMPLE_RATE / f)
    f_exact = cycles * SAMPLE_RATE / n            # whole cycles in n samples
    wobble_cycles = max(1, round(3 * n / SAMPLE_RATE))
    rng = random.Random(seed)
    phases = [rng.uniform(0, 2 * math.pi) for _ in range(12)]
    noise = [rng.uniform(-1, 1) for _ in range(n)]
    out = []
    lp = 0.0
    a = math.exp(-2 * math.pi * 2500 / SAMPLE_RATE)
    for i in range(n):
        x = 0.0
        for k in range(1, 13):
            if k * f_exact < SAMPLE_RATE / 2:
                x += math.sin(2 * math.pi * k * cycles * i / n + phases[k - 1]) / k
        x *= 1 + 0.1 * math.sin(2 * math.pi * wobble_cycles * i / n)
        x += 0.12 * noise[i]
        lp = (1 - a) * x + a * lp                  # gentle low-pass
        out.append(lp)
    peak = max(abs(s) for s in out) or 1.0
    return [s / peak * 0.7 for s in out], f_exact * 30


def write_wav(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * 32767)) for s in samples))


def main(args):
    if not args:
        print(__doc__)
        return 1
    for arg in args:
        rpm = float(arg)
        samples, exact = engine_loop(rpm)
        name = f"engine_{int(round(rpm))}.wav"
        write_wav(name, samples)
        print(f"{name}: {len(samples) / SAMPLE_RATE:.3f} s, represents {exact:.2f} rpm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
