"""AU101 Lab 02: check a folder of foley WAV files against the session spec.

Usage (from the repository root):

    .venv/bin/python courses/AU101-audio-for-games/labs/lab02-starter/check_foley.py path/to/folder

Needs your finished levels.py. Prints one line per file and exits with
status 1 if anything fails. The spec is in labs/lab02.md.
"""
import re
import sys
from pathlib import Path

from levels import clipped_runs, noise_floor_dbfs, peak_dbfs, read_wav

NAME = re.compile(r"^(?P<cat>[A-Z]{4}[A-Za-z]{2,5})_(?P<desc>[a-z0-9-]+)_(?P<who>[A-Z]{2,3})_(?P<n>\d{2})\.wav$")
RATE, BITS = 48000, 24
PEAK_MIN, PEAK_MAX = -20.0, -1.0     # dBFS: loud enough, never near clipping
MIN_SNR = 40.0                       # dB between the take's peak and the room tone floor
ROOM_TONE_CAT = "AMBRoom"


def check_folder(folder):
    files = sorted(Path(folder).glob("*.wav"))
    problems, rows = [], []
    room = [f for f in files if f.name.startswith(ROOM_TONE_CAT + "_")]
    floor = None
    if not room:
        problems.append(f"no room tone file (name it {ROOM_TONE_CAT}_room-tone_XX_01.wav)")
    for f in files:
        m = NAME.match(f.name)
        if not m:
            problems.append(f"{f.name}: name does not match CatID_description_initials_NN.wav")
            continue
        samples, rate, bits, channels = read_wav(f)
        seconds = len(samples) / rate
        peak = peak_dbfs(samples)
        issues = []
        if rate != RATE:
            issues.append(f"rate {rate} (need {RATE})")
        if bits != BITS:
            issues.append(f"{bits}-bit (need {BITS})")
        if channels != 1 and m["cat"] != ROOM_TONE_CAT:
            issues.append("stereo (effects must be mono)")
        if clipped_runs(samples):
            issues.append("clipped")
        if m["cat"] == ROOM_TONE_CAT:
            floor = noise_floor_dbfs(samples, rate)
            if seconds < 20:
                issues.append(f"room tone only {seconds:.1f} s (need 20)")
        elif not PEAK_MIN <= peak <= PEAK_MAX:
            issues.append(f"peak {peak:.1f} dBFS outside {PEAK_MIN} to {PEAK_MAX}")
        rows.append((f.name, seconds, peak, issues))
        problems += [f"{f.name}: {i}" for i in issues]
    effects = [r for r in rows if not r[0].startswith(ROOM_TONE_CAT)]
    if len(effects) < 11:
        problems.append(f"only {len(effects)} effect files (need 11 plus room tone)")
    for name, seconds, peak, issues in rows:
        snr = "" if floor is None or name.startswith(ROOM_TONE_CAT) else f"  SNR {peak - floor:5.1f} dB"
        print(f"{'FAIL' if issues else 'ok  '} {name:<40} {seconds:5.2f} s  peak {peak:6.1f} dBFS{snr}")
        if snr and peak - floor < MIN_SNR:
            problems.append(f"{name}: SNR {peak - floor:.1f} dB below {MIN_SNR}")
    if floor is not None:
        print(f"room tone floor: {floor:.1f} dBFS")
    for p in problems:
        print("  -", p)
    return not problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(0 if check_folder(sys.argv[1]) else 1)
