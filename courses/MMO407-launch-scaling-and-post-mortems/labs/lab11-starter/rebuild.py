"""MMO407 lab 11: the rebuild clock for a fan emulator.

Standard library only. Times are in weeks unless a name says years.
Run from inside lab11-starter/:
    python rebuild.py                    # prints the report (fails until the TODOs are done)
    python -m unittest test_rebuild.py
"""
import csv
from pathlib import Path

# The lecture's section 2 project. Invented teaching values.
LECTURE = dict(behaviours=1_500, w=60, g=4, per_week=200)
HOURS_PORT = 3


def rebuild_hours(behaviours, w, g, q, w_evidence=None):
    """Volunteer-hours to rebuild everything.

    Evidence-backed behaviours (share q) cost `w_evidence` hours each
    (default: w). Behaviours without evidence cost g * w hours each.
    Note that g multiplies the ORIGINAL w, so a protocol document that
    lowers w_evidence does not make guessing cheaper.
    """
    # TODO 1: behaviours * (q * w_evidence + (1 - q) * g * w)
    raise NotImplementedError("TODO 1")


def rebuild_weeks(behaviours, w, g, q, per_week, w_evidence=None):
    return rebuild_hours(behaviours, w, g, q, w_evidence) / per_week


def completeness(t, behaviours, w, g, q, per_week):
    """Share of the game rebuilt after t weeks (evidence-backed behaviours first).

    Up to the kink t_q = behaviours*q*w/per_week the curve climbs at
    per_week/(behaviours*w) per week; after it, g times slower. Never above 1.
    """
    # TODO 2: the piecewise curve from the lecture's interactive spec
    raise NotImplementedError("TODO 2")


def slope(history, start_week, end_week):
    """Average completeness gained per week between two weeks of a history.

    `history` is a list of (week, completeness) pairs; both weeks must appear in it.
    """
    points = dict(history)
    return (points[end_week] - points[start_week]) / (end_week - start_week)


def find_kink(history):
    """Return the week after which the slope drops most sharply.

    Compare, at each interior point, the slope from the previous point with the
    slope to the next point, and return the week where their ratio is largest.
    """
    # TODO 3: loop over interior points of the (sorted) history
    raise NotImplementedError("TODO 3")


def fit(history):
    """Estimate (q, g) from a history: q is the completeness at the kink,
    g is the slope before the kink divided by the slope after it."""
    history = sorted(history)
    kink = find_kink(history)
    weeks = [wk for wk, _ in history]
    before = slope(history, weeks[0], kink)
    after = slope(history, kink, weeks[-1])
    return dict(history)[kink], before / after


def load_history(path=Path(__file__).with_name("project_history.csv")):
    with open(path, newline="") as f:
        return [(int(r["week"]), float(r["completeness"])) for r in csv.DictReader(f)]


if __name__ == "__main__":
    L = LECTURE
    for q in (1.0, 0.9, 0.8, 0.6, 0.4):
        wk = rebuild_weeks(q=q, **L)
        print(f"evidence {q:4.0%}  weeks {wk:6.0f}  years {wk / 52:5.1f}")
    print(f"source released  weeks {L['behaviours'] * HOURS_PORT / L['per_week']:6.1f}")
    for t in (0, 180, 360, 540, 720):
        print(f"week {t:3}  rebuilt {completeness(t, q=0.8, **L):6.1%}")
    q_hat, g_hat = fit(load_history())
    print(f"history fit: kink at q = {q_hat:.2f}, g = {g_hat:.1f}")
