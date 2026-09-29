"""AU101 Lab 13 starter: subtitle timing and directional sound cues.

Run the tests from the repository root with:

    .venv/bin/python courses/AU101-audio-for-games/labs/lab13-starter/test_subtitles.py

Run this file on its own to print the timing report for dialogue.csv:

    .venv/bin/python courses/AU101-audio-for-games/labs/lab13-starter/subtitles.py

Standard library only. Every function marked TODO raises NotImplementedError.
The model is the one in lectures/w13-accessibility-subtitles-and-visual-sound-cues.md:

    n        characters in the subtitle, counting spaces and punctuation
    L        length of the voice clip in seconds
    g        gap in seconds from the end of this clip to the start of the next line
    R        reading limit in characters per second (CPS)
    d_min    minimum time any subtitle stays on screen

    required display time   d = max(d_min, n / R)
    hold after the voice    h = max(0, d - L)
    the line fits if        h <= g
    longest text that fits  n_max = floor(R * (L + g))
"""
import csv
import math
from pathlib import Path

TOL = 1e-9          # tolerance for float comparisons
MAX_LINE = 42       # characters per subtitle row
MAX_ROWS = 2        # rows per subtitle event


def load_dialogue(path):
    """Read dialogue.csv into a list of dicts with float start and voice_len.

    Adds 'gap': seconds from the end of this line's voice to the start of the
    next line. The last line's gap is float('inf').
    """
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({"id": r["id"], "speaker": r["speaker"], "text": r["text"],
                         "start": float(r["start"]), "voice_len": float(r["voice_len"])})
    rows.sort(key=lambda r: r["start"])
    for a, b in zip(rows, rows[1:]):
        a["gap"] = b["start"] - (a["start"] + a["voice_len"])
    if rows:
        rows[-1]["gap"] = float("inf")
    return rows


def char_count(text):
    """Characters the player has to read. Spaces and punctuation count."""
    return len(text.strip())


# ---------------------------------------------------------------------------
# Part A. Timing one line
# ---------------------------------------------------------------------------

def required_duration(n, reading_cps, d_min):
    """Seconds a subtitle of n characters must stay up for a reader at reading_cps."""
    raise NotImplementedError("TODO: d = max(d_min, n / R)")


def unread_fraction(n, voice_len, reading_cps):
    """Fraction of the text a reader has NOT reached if the subtitle vanishes when the voice ends.

    A reader at R characters per second has read R * L characters after L seconds.
    Return a number between 0 and 1.
    """
    raise NotImplementedError("TODO: max(0, 1 - R * L / n)")


def time_line(text, voice_len, gap, reading_cps, d_min):
    """Return a dict describing one line under the hold-after-voice policy.

    Keys:
      n        characters
      cps      n / voice_len (the rate the voice forces if the subtitle ends with the voice)
      need     required_duration(...)
      hold     max(0, need - voice_len)
      fits     True if hold <= gap (use TOL)
      n_max    floor(R * (voice_len + gap)), or None if gap is infinite
    """
    raise NotImplementedError("TODO")


# ---------------------------------------------------------------------------
# Part B. Layout: two rows of 42 characters
# ---------------------------------------------------------------------------

def wrap(text, max_line=MAX_LINE):
    """Greedy word wrap. Return a list of rows, each at most max_line characters.

    Break only at spaces. A single word longer than max_line goes on its own row.
    """
    raise NotImplementedError("TODO")


def needs_split(text, max_line=MAX_LINE, max_rows=MAX_ROWS):
    """True if the text does not fit in max_rows rows of max_line characters."""
    raise NotImplementedError("TODO")


# ---------------------------------------------------------------------------
# Part C. Directional cues for sounds
# ---------------------------------------------------------------------------

def relative_bearing(listener, facing_deg, source):
    """Angle of the source relative to where the listener faces, in degrees.

    Coordinates are (x, y) with +y forward on the map ("north") and +x to the
    right ("east"). Headings are compass style: 0 = +y, 90 = +x, clockwise.
    Return a value in (-180, 180]. Positive means the source is to the right.
    """
    raise NotImplementedError("TODO: atan2(dx, dy), subtract facing, wrap")


def cue_arrow(listener, facing_deg, source, fov_deg=90.0, behind_deg=135.0):
    """Caption direction marker for a sound.

    ""  if the source is on screen: |rel| <= fov_deg / 2
    "v" if the source is behind:    |rel| >= behind_deg
    "<" if it is off screen to the left, ">" if to the right.
    """
    raise NotImplementedError("TODO")


def sector(rel_deg, k=8):
    """Index of the radial-indicator wedge for a relative bearing.

    Wedge 0 is centred straight ahead, indices increase clockwise, k wedges in total.
    Use round(rel / (360 / k)) mod k. Python's round() sends halves to the even
    number; that is acceptable here.
    """
    raise NotImplementedError("TODO")


def report(path, reading_cps=17.0, d_min=1.0):
    """Print the timing table for a dialogue file."""
    print(f"R = {reading_cps:g} CPS, d_min = {d_min:g} s")
    print(f"{'id':>4} {'n':>4} {'L':>5} {'gap':>5} {'cps':>6} {'hold':>5} {'fits':>5} {'split':>5}")
    for r in load_dialogue(path):
        t = time_line(r["text"], r["voice_len"], r["gap"], reading_cps, d_min)
        gap = "end" if math.isinf(r["gap"]) else f"{r['gap']:.1f}"
        print(f"{r['id']:>4} {t['n']:>4} {r['voice_len']:>5.1f} {gap:>5} {t['cps']:>6.1f} "
              f"{t['hold']:>5.2f} {str(t['fits']):>5} {str(needs_split(r['text'])):>5}")


if __name__ == "__main__":
    try:
        report(Path(__file__).with_name("dialogue.csv"))
    except NotImplementedError as e:
        print(f"\nNot finished yet: {e}. Run test_subtitles.py to see which parts are left.")
