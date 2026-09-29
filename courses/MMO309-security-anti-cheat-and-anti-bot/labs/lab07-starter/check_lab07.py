"""Checker for MMO309 Lab 07. Run:  python check_lab07.py

Part 1 tests each feature on hand-computable inputs.
Part 2 runs your features and flag() over the 150 synthetic accounts.
"""
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import features as F  # noqa: E402

COUNTS = ["kills", "loots", "moves", "chats", "trades", "crafts"]
failures = 0


def check(name, fn):
    global failures
    try:
        ok, detail = fn()
    except NotImplementedError:
        ok, detail = False, "not implemented yet"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures += 1


def close(a, b, tol=1e-6):
    return a is not None and abs(a - b) <= tol


def t_slack():
    v = F.slack_cv([1100, 900, 1100, 900], [0, 0, 0, 0])
    w = F.slack_cv([1600, 1520, 1580, 1500], [1500] * 4)
    ok = close(v, 0.1) and close(w, statistics.pstdev([100, 20, 80, 0]) / 50)
    return ok, f"got {v} and {w}, expected 0.1 and {statistics.pstdev([100, 20, 80, 0]) / 50:.6f}"


def t_hours():
    rows = [dict(day=0, hour=5, kills=1, loots=0, moves=0, chats=0, trades=0, crafts=0),
            dict(day=0, hour=5, kills=0, loots=0, moves=3, chats=0, trades=0, crafts=0),
            dict(day=1, hour=5, kills=0, loots=0, moves=0, chats=0, trades=0, crafts=0),
            dict(day=1, hour=6, kills=0, loots=0, moves=0, chats=2, trades=0, crafts=0)]
    v = F.active_hours_per_day(rows, days=2)
    return close(v, 1.0), f"got {v}, expected 1.0 (two active slots over two days)"


def t_cosine():
    a = F.cosine([1, 0, 0], [0, 1, 0])
    b = F.cosine([3, 4, 0], [6, 8, 0])
    c = F.cosine([0, 0, 0], [1, 2, 3])
    return close(a, 0.0) and close(b, 1.0) and close(c, 0.0), f"got {a}, {b}, {c}"


def t_selfsim():
    v = F.self_similarity([[1, 0], [0, 1], [1, 1]])
    expected = (0 + 2 * (1 / math.sqrt(2))) / 3
    one = F.self_similarity([[5, 5]])
    capped = F.self_similarity([[1, 0]] * 40 + [[0, 1]] * 10)
    ok = close(v, expected) and close(one, 1.0) and close(capped, 1.0)
    return ok, f"got {v}, {one}, {capped}; expected {expected:.6f}, 1.0, 1.0"


def load():
    if not (HERE / "labels.csv").exists():
        import make_logs
        make_logs.main()
    gaps, cds = defaultdict(list), defaultdict(list)
    with open(HERE / "intervals.csv") as f:
        for r in csv.DictReader(f):
            gaps[r["account_id"]].append(float(r["gap_ms"]))
            cds[r["account_id"]].append(float(r["cooldown_ms"]))
    hours = defaultdict(list)
    with open(HERE / "hours.csv") as f:
        for r in csv.DictReader(f):
            row = {k: int(v) for k, v in r.items() if k != "account_id"}
            hours[r["account_id"]].append(row)
    with open(HERE / "labels.csv") as f:
        labels = {r["account_id"]: (r["label"], r["kind"]) for r in csv.DictReader(f)}
    return gaps, cds, hours, labels


def t_end_to_end():
    gaps, cds, hours, labels = load()
    tp = fp = fn = 0
    by_kind = defaultdict(lambda: [0, 0])
    for acc, (label, kind) in labels.items():
        rows = sorted(hours[acc], key=lambda r: (r["day"], r["hour"]))
        feats = {
            "raw_cv": statistics.pstdev(gaps[acc]) / statistics.mean(gaps[acc]),
            "slack_cv": F.slack_cv(gaps[acc], cds[acc]),
            "hours_per_day": F.active_hours_per_day(rows),
            "self_similarity": F.self_similarity([[r[c] for c in COUNTS] for r in rows]),
        }
        flagged = bool(F.flag(feats))
        by_kind[kind][0] += flagged
        by_kind[kind][1] += 1
        tp += flagged and label == "bot"
        fp += flagged and label == "human"
        fn += (not flagged) and label == "bot"
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn)
    table = ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(by_kind.items()))
    print(f"       flagged by kind: {table}")
    ok = precision >= 0.95 and recall >= 0.90 and by_kind["rotation"][0] == 0
    return ok, f"precision {precision:.3f}, recall {recall:.3f} (need >= 0.95, >= 0.90, 0 rotation humans)"


check("slack_cv", t_slack)
check("active_hours_per_day", t_hours)
check("cosine", t_cosine)
check("self_similarity", t_selfsim)
check("end-to-end rule", t_end_to_end)
print("ALL PASS" if failures == 0 else f"{failures} check(s) failing")
sys.exit(1 if failures else 0)
