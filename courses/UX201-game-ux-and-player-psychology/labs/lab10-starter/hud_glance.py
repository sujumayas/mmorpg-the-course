"""UX201 Lab 10 starter: price HUD checks with the week 10 glance-cost model.

Usage:
    python hud_glance.py hud_elements.csv

The CSV has one row per HUD element with columns:
    element, x_frac, y_frac, checks_per_min
x_frac and y_frac are the element's centre as a fraction of screen width and
height measured from the TOP-LEFT corner (0..1). Measure them on a screenshot.

The script prints theta, time per check and look-away share for each element
on every setup in SETUPS. Edit SETUPS and the model constants to match the
screens and players you tested. All constants are teaching values from the
lecture; replace them with your own measurements where you have them.
"""
import csv
import math
import sys

L_MS = 200.0        # saccade latency
F_MS = 250.0        # fixation to read the element
THETA_F = 2.5       # reading radius in degrees
SACC_A, SACC_B = 20.0, 2.5   # saccade duration = A + B * theta (ms)

# name: (diagonal inches, viewing distance cm), all 16:9
SETUPS = {
    "PC 24in @ 60cm": (24, 60),
    "TV 55in @ 250cm": (55, 250),
    "Handheld 7in @ 35cm": (7, 35),
}


def screen_cm(diag_in):
    k = diag_in * 2.54 / math.hypot(16, 9)
    return 16 * k, 9 * k


def theta_deg(x_frac, y_frac, diag_in, dist_cm, cx=0.5, cy=0.5):
    w, h = screen_cm(diag_in)
    d = math.hypot((x_frac - cx) * w, (y_frac - cy) * h)
    return math.degrees(math.atan(d / dist_cm))


def glance_ms(theta):
    if theta <= THETA_F:
        return F_MS
    return 2 * (L_MS + SACC_A + SACC_B * theta) + F_MS


def main(path):
    rows = list(csv.DictReader(open(path, newline="")))
    for setup, (diag, dist) in SETUPS.items():
        print(f"\n== {setup}")
        print(f"{'element':<20}{'theta':>8}{'T ms':>9}{'f/min':>7}{'E %':>7}")
        total = 0.0
        for r in rows:
            th = theta_deg(float(r["x_frac"]), float(r["y_frac"]), diag, dist)
            t = glance_ms(th)
            f = float(r["checks_per_min"])
            e = f * t / 60000
            total += e
            print(f"{r['element']:<20}{th:8.1f}{t:9.0f}{f:7.1f}{100*e:7.1f}")
        print(f"{'total look-away':<44}{100*total:7.1f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "hud_elements.csv")
