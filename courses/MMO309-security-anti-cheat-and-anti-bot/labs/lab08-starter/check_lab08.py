"""Checker for MMO309 Lab 08. Run:  python check_lab08.py"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import detect as D  # noqa: E402

failures = 0


def check(name, fn):
    global failures
    try:
        ok, detail = fn()
    except NotImplementedError:
        ok, detail = False, "not implemented yet"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures += 1


def close(a, b, tol=1e-9):
    return a is not None and abs(a - b) <= tol


S = [0.95, 0.90, 0.80, 0.70, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]
L = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0]


def t_confusion():
    got = D.confusion(S, L, 0.70)
    return tuple(got) == (3, 1, 1, 5), f"got {got}, expected (3, 1, 1, 5)"


def t_pr():
    p, r = D.precision_recall(S, L, 0.70)
    p0, r0 = D.precision_recall(S, L, 0.99)
    return close(p, 0.75) and close(r, 0.75) and close(p0, 1.0) and close(r0, 0.0), \
        f"got ({p}, {r}) and ({p0}, {r0})"


def t_thr():
    a = D.threshold_for_precision(S, L, 0.75)
    b = D.threshold_for_precision(S, L, 1.0)
    return a == 0.70 and b == 0.90, f"got {a} and {b}, expected 0.7 and 0.9"


def t_cost():
    c = D.expected_cost(S, L, 0.70, c_fp=100, c_fn=10)
    return close(c, 110), f"got {c}, expected 110"


def t_prev():
    p = D.precision_at_prevalence(0.95, 0.01, 0.02)
    return close(p, 0.019 / (0.019 + 0.0098)), f"got {p}, expected {0.019 / 0.0288:.6f}"


def t_band():
    b = D.review_band(S, 0.90, 3)
    c = D.review_band(S, 0.90, 0)
    return b == 0.60 and c == 0.90, f"got {b} and {c}, expected 0.6 and 0.9"


def load():
    if not (HERE / "scores.csv").exists():
        import make_scores
        make_scores.main()
    with open(HERE / "scores.csv") as f:
        rows = list(csv.DictReader(f))
    return [float(r["score"]) for r in rows], [int(r["label"]) for r in rows]


def t_dataset():
    s, l = load()
    t = D.threshold_for_precision(s, l, 0.99)
    p, r = D.precision_recall(s, l, t)
    band = D.review_band(s, t, 400)
    n_band = sum(band <= x < t for x in s)
    ok = (t is not None and abs(t - 0.7407) < 1e-9 and p >= 0.99
          and abs(band - 0.3661) < 1e-9 and n_band <= 400)
    return ok, (f"auto-ban threshold {t} (precision {p:.3f}, recall {r:.3f}); "
                f"review band starts at {band} with {n_band} cases")


check("confusion", t_confusion)
check("precision_recall", t_pr)
check("threshold_for_precision", t_thr)
check("expected_cost", t_cost)
check("precision_at_prevalence", t_prev)
check("review_band", t_band)
check("dataset thresholds", t_dataset)
print("ALL PASS" if failures == 0 else f"{failures} check(s) failing")
sys.exit(1 if failures else 0)
