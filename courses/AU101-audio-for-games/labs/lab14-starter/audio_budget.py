"""AU101 Lab 14 starter: an audio memory, CPU and streaming budget.

Run the tests from the repository root with:

    .venv/bin/python courses/AU101-audio-for-games/labs/lab14-starter/test_audio_budget.py

Run this file on its own to evaluate every plan in level_assets.csv:

    .venv/bin/python courses/AU101-audio-for-games/labs/lab14-starter/audio_budget.py [plan_file.csv]

Standard library only. The model is the one in
lectures/w14-optimization-voices-memory-streaming.md. Units: bytes, seconds,
and CPU as a percentage of one core. 1 MB = 1,000,000 bytes.

    PCM bytes          P = rate * (bits / 8) * channels * seconds * count
    on disk            P / r            (r = compression ratio of the codec)
    resident memory    P                 load = decompress   (decoded when the level loads)
                       P / r             load = compressed   (decoded while it plays)
                       voices * S        load = stream       (S = buffer per playing stream)
    CPU at the peak    voices * (MIX + DECODE[codec played])
                       a decompressed sound plays as PCM, whatever it was stored as
    stream read rate   voices * rate * (bits / 8) * channels / r    (stream groups only)
"""
import csv
import math
import sys
from pathlib import Path

# Compression ratios from the Unity 6 manual (AudioClip import settings):
# ADPCM about 3.5x smaller than PCM, Vorbis about 10x. Real Vorbis ratios depend on the quality setting.
RATIO = {"pcm": 1.0, "adpcm": 3.5, "vorbis": 10.0}

# Unity 6 manual: a streaming clip has an overhead of about 200 KB even with no audio loaded.
STREAM_BUFFER = 200_000

# CPU costs per real voice, in % of one core. INVENTED for this course's imaginary
# mid-range phone. Only their order (PCM < ADPCM < Vorbis) comes from engine docs.
# Measure your own platform with a profiler before trusting any number like these.
MIX = 0.10
DECODE = {"pcm": 0.0, "adpcm": 0.05, "vorbis": 0.40}

LOADS = {"decompress", "compressed", "stream"}
TOL = 1e-9


def load_groups(path):
    """Read an asset plan CSV into a dict: plan name -> list of group dicts."""
    plans = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            g = {"name": r["group"], "count": int(r["count"]), "seconds": float(r["seconds"]),
                 "channels": int(r["channels"]), "rate": int(r["rate"]), "bits": int(r["bits"]),
                 "codec": r["codec"].strip().lower(), "load": r["load"].strip().lower(),
                 "voices": int(r["peak_voices"])}
            if g["codec"] not in RATIO or g["load"] not in LOADS:
                raise ValueError(f"bad codec or load type in row {r}")
            plans.setdefault(r["plan"], []).append(g)
    return plans


# ---------------------------------------------------------------------------
# Part A. Bytes
# ---------------------------------------------------------------------------

def pcm_bytes(rate, bits, channels, seconds):
    """Uncompressed size of one sound."""
    raise NotImplementedError("TODO: rate * bits / 8 * channels * seconds")


def group_pcm_bytes(g):
    """Uncompressed size of every sound in a group."""
    raise NotImplementedError("TODO")


def disk_bytes(g):
    """Size of the group in the game's package."""
    raise NotImplementedError("TODO")


def resident_bytes(g):
    """Memory the group occupies while the level runs, by load type."""
    raise NotImplementedError("TODO")


# ---------------------------------------------------------------------------
# Part B. CPU and streaming
# ---------------------------------------------------------------------------

def played_codec(g):
    """The codec the mixer has to decode at play time."""
    raise NotImplementedError("TODO: a decompressed group plays as PCM")


def cpu_percent(g):
    """CPU for the group at its peak number of voices."""
    raise NotImplementedError("TODO")


def stream_read_rate(g):
    """Bytes per second read from disk for the group (0 unless it streams)."""
    raise NotImplementedError("TODO")


def max_real_voices(cpu_budget, codec):
    """How many voices of one codec fit in a CPU budget (whole voices only)."""
    raise NotImplementedError("TODO: floor(budget / (MIX + DECODE[codec]))")


# ---------------------------------------------------------------------------
# Part C. Whole plan
# ---------------------------------------------------------------------------

def evaluate(groups, mem_budget, cpu_budget):
    """Totals for a plan.

    Return a dict with keys: memory, disk, cpu, read_rate, voices,
    fits_memory, fits_cpu (use TOL in the comparisons).
    """
    raise NotImplementedError("TODO")


def main(path, mem_budget=32_000_000, cpu_budget=8.0):
    for name, groups in load_groups(path).items():
        e = evaluate(groups, mem_budget, cpu_budget)
        verdict = "FITS" if e["fits_memory"] and e["fits_cpu"] else "OVER"
        print(f"{name:<28} mem {e['memory'] / 1e6:7.2f} MB  disk {e['disk'] / 1e6:7.2f} MB  "
              f"cpu {e['cpu']:5.2f}%  read {e['read_rate'] / 1e3:6.1f} KB/s  "
              f"voices {e['voices']:3d}  {verdict}")


if __name__ == "__main__":
    plan_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("level_assets.csv")
    try:
        main(plan_file)
    except NotImplementedError as e:
        print(f"Not finished yet: {e}. Run test_audio_budget.py to see which parts are left.")
