"""UX201 Lab 11 starter: WCAG contrast ratio and required backplate opacity.

Usage:
    python contrast.py measurements.csv

The CSV has one row per measurement with columns:
    screen, element, text_hex, background_hex, size
size is "standard" or "large" (XAG 102: large = 52 px at 1080p on console,
36 px at 1080p on PC). Pick text_hex from the text fill and background_hex
from the LIGHTEST (for light text) or DARKEST (for dark text) background
pixel directly behind the text, as XAG 102 asks.

For each row the script prints both luminances, the contrast ratio, pass/fail
against the XAG thresholds, and the black-box opacity needed to reach the
standard threshold (linear-light model from the week 11 lecture; real engines
that blend in sRGB space will look darker, so treat it as conservative).
"""
import csv
import sys


def lin(c8):
    c = c8 / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_str):
    h = hex_str.strip().lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def alpha_needed(l_text, l_bg, target):
    """Opacity of a black box so that text lighter than the boxed background
    reaches `target`. Returns None when the text is darker than the
    background (a black box would make things worse; use a light box)."""
    limit = (l_text + 0.05) / target - 0.05
    if l_bg <= limit:
        return 0.0
    if limit <= 0:
        return None
    return 1 - limit / l_bg


def main(path):
    print(f"{'screen':<14}{'element':<18}{'L text':>8}{'L bg':>8}{'ratio':>8}"
          f"{'need':>7}{'pass':>6}{'box a':>8}")
    for r in csv.DictReader(open(path, newline="")):
        lt, lb = luminance(r["text_hex"]), luminance(r["background_hex"])
        c = ratio(lt, lb)
        need = 3.0 if r["size"].strip() == "large" else 4.5
        a = alpha_needed(lt, lb, need) if lt > lb else None
        a_txt = "-" if a is None else f"{a:.2f}"
        print(f"{r['screen']:<14}{r['element']:<18}{lt:8.3f}{lb:8.3f}{c:8.2f}"
              f"{need:7.1f}{('yes' if c >= need else 'NO'):>6}{a_txt:>8}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "measurements.csv")
