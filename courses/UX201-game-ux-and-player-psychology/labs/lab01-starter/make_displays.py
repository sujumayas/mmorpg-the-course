#!/usr/bin/env python3
"""UX201 Lab 01 starter: generate visual search displays and a trial sheet.

Standard library only. Run:
    python3 make_displays.py --out displays --seed 7

Creates, in the output folder:
  - one SVG per trial (open full screen in a browser, one at a time)
  - trials.csv: the randomised trial order, with an empty rt_ms and answer column
    for you to fill in during the session
  - key.csv: which display has the target and where (keep it away from the participant)

Design: 2 modes (popout, conjunction) x 4 set sizes (4, 8, 16, 32)
x target present/absent x --reps repetitions (default 3) = 48 trials.

popout:      target = accent circle; distractors = neutral circles
conjunction: target = accent circle; distractors = accent squares and neutral circles
"""
import argparse
import csv
import os
import random

W, H = 1200, 800
CELL = 90          # grid cell size in px; items are jittered inside a cell
R = 24             # item radius / half-size in px
ACCENT = "#d9480f"
NEUTRAL = "#868e96"
BG = "#ffffff"
SET_SIZES = [4, 8, 16, 32]
MODES = ["popout", "conjunction"]


def shape(kind, colour, x, y):
    if kind == "circle":
        return f'<circle cx="{x}" cy="{y}" r="{R}" fill="{colour}"/>'
    return (f'<rect x="{x - R}" y="{y - R}" width="{2 * R}" height="{2 * R}" '
            f'fill="{colour}"/>')


def positions(n, rng):
    cols, rows = W // CELL, H // CELL
    cells = rng.sample([(c, r) for c in range(cols) for r in range(rows)], n)
    jitter = (CELL - 2 * R) // 2 - 4
    return [(c * CELL + CELL // 2 + rng.randint(-jitter, jitter),
             r * CELL + CELL // 2 + rng.randint(-jitter, jitter)) for c, r in cells]


def display(mode, n, present, rng):
    pos = positions(n, rng)
    items = []
    target_at = None
    for i, (x, y) in enumerate(pos):
        if present and i == 0:
            items.append(("circle", ACCENT, x, y))
            target_at = (x, y)
        elif mode == "popout":
            items.append(("circle", NEUTRAL, x, y))
        else:
            items.append(("square", ACCENT, x, y) if rng.random() < 0.5
                         else ("circle", NEUTRAL, x, y))
    rng.shuffle(items)
    body = "\n".join(shape(k, c, x, y) for k, c, x, y in items)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{BG}"/>'
           f'\n{body}\n</svg>\n')
    return svg, target_at


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="displays")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--reps", type=int, default=3)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    os.makedirs(args.out, exist_ok=True)

    trials = [(m, n, p) for m in MODES for n in SET_SIZES for p in (True, False)
              for _ in range(args.reps)]
    rng.shuffle(trials)

    with open(os.path.join(args.out, "trials.csv"), "w", newline="") as f, \
         open(os.path.join(args.out, "key.csv"), "w", newline="") as k:
        tw, kw = csv.writer(f), csv.writer(k)
        tw.writerow(["trial", "file", "mode", "set_size", "rt_ms", "answer", "notes"])
        kw.writerow(["trial", "file", "present", "target_x", "target_y"])
        for i, (m, n, p) in enumerate(trials, 1):
            name = f"t{i:02d}.svg"
            svg, at = display(m, n, p, rng)
            with open(os.path.join(args.out, name), "w") as s:
                s.write(svg)
            tw.writerow([i, name, m, n, "", "", ""])
            kw.writerow([i, name, int(p), at[0] if at else "", at[1] if at else ""])
    print(f"Wrote {len(trials)} displays, trials.csv and key.csv to {args.out}/")


if __name__ == "__main__":
    main()
