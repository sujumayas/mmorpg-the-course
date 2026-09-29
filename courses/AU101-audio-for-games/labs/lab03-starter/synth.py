"""AU101 Lab 03 starter: a tiny sound-effect synthesiser. Standard library only.

The model is week 3, section 3:

    f(t) = f0 * 2**(slide * t), times 2**(jump / 12) from t_jump onward
    level(t) = t / A during the attack, 1 - (t - A) / D during the decay, then 0
    phase accumulator: phase += f / rate each sample, wrapped into [0, 1)

Fill in the four TODO functions, then run the tests from the repository root:

    .venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab03-starter

Render the lecture's presets to WAV files:

    .venv/bin/python courses/AU101-audio-for-games/labs/lab03-starter/synth.py out/
"""
import json
import math
import os
import random
import sys
import wave
from dataclasses import dataclass, asdict

RATE = 48000
WAVES = ("sine", "square", "sawtooth", "triangle", "noise")


@dataclass
class Sfx:
    wave: str = "square"
    f0: float = 440.0       # start frequency, Hz
    slide: float = 0.0      # octaves per second, signed
    jump: int = 0           # semitones, signed; 0 means no jump
    t_jump: float = 0.0     # seconds after the start
    attack: float = 0.005   # seconds
    decay: float = 0.2      # seconds
    gain: float = 0.5       # peak amplitude, keep <= 0.5 to leave headroom
    seed: int = 1           # for noise, so renders are repeatable

    @property
    def length(self):
        return self.attack + self.decay


PRESETS = {
    "coin":  Sfx("square",   1000,  0.0, 5, 0.06, 0.005, 0.25),
    "jump":  Sfx("square",    300,  2.0, 0, 0.00, 0.010, 0.20),
    "laser": Sfx("sawtooth", 1200, -4.0, 0, 0.00, 0.002, 0.25),
    "hurt":  Sfx("square",    400, -3.0, 0, 0.00, 0.002, 0.20),
}


def freq_at(t, sfx):
    """TODO 1. Frequency in Hz at time t (seconds) for this sound.
    Apply the jump only when sfx.jump != 0 and t >= sfx.t_jump."""
    raise NotImplementedError("freq_at() is yours to write")


def envelope(t, attack, decay):
    """TODO 2. The two-stage linear envelope, between 0 and 1.
    An attack of 0 means the level starts at 1 immediately.
    Outside 0 <= t < attack + decay the level is 0."""
    raise NotImplementedError("envelope() is yours to write")


def wave_value(kind, phase, rng):
    """TODO 3. One sample of the waveform at `phase` in [0, 1).
    sine: sin(2*pi*phase); square: 1 if phase < 0.5 else -1;
    sawtooth: 2*phase - 1; triangle: 1 - 4*abs(phase - 0.5);
    noise: rng.uniform(-1, 1) (ignore phase). Unknown kinds raise ValueError."""
    raise NotImplementedError("wave_value() is yours to write")


def render(sfx, rate=RATE):
    """TODO 4. Return a list of round(sfx.length * rate) float samples.
    For sample i, t = i / rate. Compute the sample from the CURRENT phase,
    then advance the phase by freq_at(t, sfx) / rate and wrap it into [0, 1).
    Start with phase 0 and rng = random.Random(sfx.seed).
    Each sample is sfx.gain * envelope(t, ...) * wave_value(...)."""
    raise NotImplementedError("render() is yours to write")


def write_wav(path, samples, rate=RATE):
    """Write mono 24-bit PCM. Provided."""
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(3)
        w.setframerate(rate)
        top = 2**23 - 1
        w.writeframes(b"".join(int(round(max(-1.0, min(1.0, s)) * top))
                               .to_bytes(3, "little", signed=True) for s in samples))


def load_sfx(path):
    """Read a JSON file of {"name": {field: value, ...}} into {"name": Sfx}."""
    with open(path) as f:
        return {name: Sfx(**fields) for name, fields in json.load(f).items()}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    sounds = load_sfx(sys.argv[2]) if len(sys.argv) > 2 else PRESETS
    os.makedirs(out, exist_ok=True)
    for name, sfx in sounds.items():
        samples = render(sfx)
        write_wav(os.path.join(out, f"{name}.wav"), samples)
        print(f"{name:<8} {sfx.f0:7.1f} -> {freq_at(sfx.length, sfx):7.1f} Hz  "
              f"{len(samples):6d} samples  {json.dumps(asdict(sfx))}")
