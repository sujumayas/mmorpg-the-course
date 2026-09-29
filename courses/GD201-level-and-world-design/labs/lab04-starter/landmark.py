"""GD201 Lab 04: landmark legibility audit. Standard library only.

Model (lecture week 4, sections 2 and 3):
  vertical FOV    V = 2 atan(tan(H/2) / aspect)
  screen fraction f = h / (2 d tan(V/2))
  legible range   d_max = h / (2 f_min tan(V/2)), capped at the fog distance if there is fog
  luminance       WCAG 2.1 relative luminance of an 8-bit sRGB color
  contrast ratio  (L_lighter + 0.05) / (L_darker + 0.05)

Angles are in degrees. Distances and heights are in meters. Distance between two map points is the
straight-line distance on the ground plane (ignore eye height).

Fill in the TODOs, then run `python check_lab04.py`. Run `python landmark.py` for a report.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent


def vertical_fov(h_fov_deg, aspect=16 / 9):
    """Vertical field of view in degrees from a horizontal one."""
    # TODO: V = 2 atan(tan(H/2) / aspect). Work in radians inside, return degrees.
    raise NotImplementedError("vertical_fov")


def screen_fraction(height, distance, v_fov_deg):
    """Share of the screen height a landmark of `height` fills at `distance`."""
    # TODO: f = h / (2 d tan(V/2))
    raise NotImplementedError("screen_fraction")


def max_distance(height, f_min, v_fov_deg, fog=None):
    """Largest distance at which the landmark is still legible. Cap at `fog` when it is given."""
    # TODO: d_max = h / (2 f_min tan(V/2)), then min(d_max, fog) if fog is not None.
    raise NotImplementedError("max_distance")


def required_height(distance, f_min, v_fov_deg):
    """Smallest landmark height that is legible from `distance`."""
    # TODO: invert the screen-fraction formula.
    raise NotImplementedError("required_height")


def relative_luminance(rgb):
    """WCAG 2.1 relative luminance of an (r, g, b) tuple of 0-255 integers."""
    # TODO: divide each channel by 255, linearize (<= 0.04045 -> c / 12.92,
    # else ((c + 0.055) / 1.055) ** 2.4), then 0.2126 R + 0.7152 G + 0.0722 B.
    raise NotImplementedError("relative_luminance")


def contrast_ratio(rgb_a, rgb_b):
    """WCAG contrast ratio between two colors, always >= 1."""
    # TODO: (lighter + 0.05) / (darker + 0.05)
    raise NotImplementedError("contrast_ratio")


def load_zone(path=HERE / "zone.csv"):
    """Return (landmarks, starts). Each landmark is a dict with name, x, y, height, rgb.
    Each start is a dict with name, x, y. Provided for you."""
    landmarks, starts = [], []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            point = {"name": row["name"], "x": float(row["x"]), "y": float(row["y"])}
            if row["kind"] == "landmark":
                point["height"] = float(row["height"])
                point["rgb"] = (int(row["r"]), int(row["g"]), int(row["b"]))
                landmarks.append(point)
            else:
                starts.append(point)
    return landmarks, starts


def legibility_matrix(landmarks, starts, v_fov_deg, f_min, fog=None):
    """Return {start name: [names of landmarks legible from that start, in landmark order]}.

    A landmark is legible from a start when the ground distance between them is at most the
    landmark's max_distance (with fog applied).
    """
    # TODO: use math.dist or math.hypot for the distance.
    raise NotImplementedError("legibility_matrix")


def report(h_fov=90, f_min=0.02, fog=None, sky=(170, 190, 215)):
    v = vertical_fov(h_fov)
    landmarks, starts = load_zone()
    print(f"H = {h_fov} deg, V = {v:.1f} deg, f_min = {f_min:.1%}, fog = {fog}")
    for lm in landmarks:
        print(f"  {lm['name']:<14} h = {lm['height']:>4.0f} m  d_max = {max_distance(lm['height'], f_min, v, fog):6.0f} m"
              f"  contrast vs sky = {contrast_ratio(lm['rgb'], sky):.2f}")
    for start, seen in legibility_matrix(landmarks, starts, v, f_min, fog).items():
        print(f"  from {start:<12} sees: {', '.join(seen) if seen else 'NOTHING'}")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not finished yet: {e} is still a TODO. Run check_lab to see what passes.")
