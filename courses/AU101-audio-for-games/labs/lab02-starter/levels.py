"""AU101 Lab 02 starter: level measurements for foley takes. Standard library only.

Samples are floats in [-1.0, 1.0), where 1.0 is full scale (0 dBFS).
Fill in the three TODO functions, then run the tests from the repository root:

    .venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab02-starter

`read_wav` is provided and handles 16-bit and 24-bit PCM WAV files.
"""
import math
import wave

SILENCE_DBFS = -200.0   # what to return for a block of exact zeros


def read_wav(path):
    """Return (samples, rate, bits, channels). Multi-channel files are mixed to
    mono by averaging, so every function below receives one list of floats."""
    with wave.open(str(path), "rb") as w:
        channels, width, rate, frames = (w.getnchannels(), w.getsampwidth(),
                                         w.getframerate(), w.getnframes())
        raw = w.readframes(frames)
    if width not in (2, 3):
        raise ValueError(f"{path}: {8 * width}-bit files are not supported; use 16 or 24")
    full = float(1 << (8 * width - 1))
    values = [int.from_bytes(raw[i:i + width], "little", signed=True) / full
              for i in range(0, len(raw), width)]
    mono = [sum(values[i:i + channels]) / channels for i in range(0, len(values), channels)]
    return mono, rate, 8 * width, channels


def amplitude_to_dbfs(a):
    """20 * log10(a), with exact silence mapped to SILENCE_DBFS."""
    return 20 * math.log10(a) if a > 0 else SILENCE_DBFS


def peak_dbfs(samples):
    """TODO 1. The largest absolute sample value, in dBFS.
    A sine wave with amplitude 0.5 peaks at about -6.02 dBFS."""
    raise NotImplementedError("peak_dbfs() is yours to write")


def rms_dbfs(samples):
    """TODO 2. Root-mean-square level in dBFS: sqrt(mean of squares), then
    amplitude_to_dbfs. A full-scale sine wave measures about -3.01 dBFS.
    An empty list or all zeros returns SILENCE_DBFS."""
    raise NotImplementedError("rms_dbfs() is yours to write")


def noise_floor_dbfs(samples, rate, window_ms=50):
    """TODO 3. The quietest window of the recording, in dBFS RMS.
    Split the samples into consecutive, non-overlapping windows of
    window_ms milliseconds (drop a final partial window unless it is the only
    one), measure each window with rms_dbfs, and return the minimum."""
    raise NotImplementedError("noise_floor_dbfs() is yours to write")


def clipped_runs(samples, threshold=0.999, run=3):
    """Count places where `run` or more consecutive samples have an absolute
    value >= threshold. One such run is enough to call a take clipped.
    Provided, so you can see how the checker defines clipping."""
    count, streak = 0, 0
    for s in samples:
        if abs(s) >= threshold:
            streak += 1
            if streak == run:
                count += 1
        else:
            streak = 0
    return count
