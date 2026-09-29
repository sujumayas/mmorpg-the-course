"""GD201 Lab 03: intensity graphs.

Time is split into steps of STEP seconds. E is a list of threat per step. Intensity follows
    I[k] = d * I[k-1] + E[k],  with I = 0 before the first step.
See lecture week 3, section 2.

Run `python intensity.py` for a report on the lecture's three designs and the sample beat chart.
"""
import math

STEP = 10  # seconds per step

# The Flooded Mill beat chart from lecture week 3, section 3: (name, duration in seconds, threat per step).
SAMPLE_BEATS = [
    ("dock", 40, 0),
    ("water wheel", 60, 5),
    ("sluice", 50, 15),
    ("mill loft", 40, 0),
    ("gear room", 70, 20),
    ("stairwell", 20, 0),
    ("rooftop", 60, 25),
]


def intensity_curve(E, d=0.5):
    """Return the list of I values, one per step."""
    # TODO: one line of arithmetic per step.
    raise NotImplementedError("intensity_curve")


def measure(curve, peak=35, calm=10, step=STEP):
    """Return a dict with keys max, peak_s, calm_s, peaks (see the lecture for definitions)."""
    # TODO: count steps above peak and below calm; a new peak starts when the previous step was below peak.
    raise NotImplementedError("measure")


def director(steps, full=20, peak=35, relax=3, d=0.5):
    """Return the E list produced by the lecture's Director rule."""
    # TODO: send full unless resting; after a step with threat that reaches peak, rest for relax steps.
    raise NotImplementedError("director")


def events_from_beats(beats, step=STEP):
    """Turn (name, duration_s, threat_per_step) rows into one E list.

    Each beat lasts ceil(duration_s / step) steps, all with the beat's threat.
    """
    # TODO: repeat each beat's threat for ceil(duration / step) steps.
    raise NotImplementedError("events_from_beats")


def half_life(d, step=STEP):
    """Seconds for intensity to halve with no new threat."""
    # TODO: solve d ** (t / step) = 0.5 for t.
    raise NotImplementedError("half_life")


def report():
    designs = {
        "A drip": [10] * 18,
        "B wave": [0, 5, 10, 15, 20, 30, 40, 0, 0, 0, 0, 5, 10, 15, 30, 0, 0, 0],
        "C director": director(18),
        "Flooded Mill": events_from_beats(SAMPLE_BEATS),
    }
    print(f"d = 0.5, half-life {half_life(0.5):.0f} s")
    for name, E in designs.items():
        m = measure(intensity_curve(E))
        print(f"{name:12s} steps {len(E):2d} total {sum(E):4d} max {m['max']:5.1f} "
              f"peak {m['peak_s']:3d} s calm {m['calm_s']:3d} s peaks {m['peaks']}")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}(). Fill in the TODOs, then run check_lab03.py.")
