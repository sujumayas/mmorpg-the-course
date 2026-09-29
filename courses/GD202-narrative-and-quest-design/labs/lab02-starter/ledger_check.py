"""GD202 Lab 02 helper: check a flag ledger and report the week 2 cost numbers.

Usage (from this folder):
    ../../../../.venv/bin/python ledger_check.py flag_ledger.csv BASE_WORDS

BASE_WORDS is the word count one player reads in your scene (the shared text
plus one version of each variant). The ledger has one row per flag write or
read. For a read, extra_words is the words you wrote for the other option(s)
at that point, so the ledger's extra_words total is W - V from the lecture.
"""
import csv
import sys
from collections import defaultdict


def check(rows, base_words):
    writes, reads = defaultdict(list), defaultdict(list)
    for r in rows:
        (writes if r["kind"] == "write" else reads)[r["flag"]].append(r)
    problems = []
    for flag in sorted(writes):
        if not reads[flag]:
            problems.append(f"flag '{flag}' is written but never read (a broken promise)")
    for flag in sorted(reads):
        if not writes[flag]:
            problems.append(f"flag '{flag}' is read but never written (a bug)")
        for r in reads[flag]:
            first_write = min((int(w["scene"]) for w in writes[flag]), default=None)
            if first_write is not None and int(r["scene"]) <= first_write:
                problems.append(f"flag '{flag}' is read in scene {r['scene']} before it is written")
    extra = sum(int(r["extra_words"] or 0) for r in rows)
    acks = sum(len(v) for f, v in reads.items() if writes[f])
    heavy = sum(1 for f, v in reads.items() if writes[f] for r in v if r["weight"] == "heavy")
    written = base_words + extra
    return {
        "W": written,
        "V": base_words,
        "share_seen": base_words / written,
        "extra": extra,
        "R": acks,
        "heavy": heavy,
        "extra_per_ack": extra / acks if acks else None,
        "problems": problems,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "flag_ledger.csv"
    base = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    with open(path, newline="") as f:
        result = check(list(csv.DictReader(f)), base)
    print(f"W = {result['W']:,}  V = {result['V']:,}  V/W = {result['share_seen']:.1%}")
    print(f"extra = {result['extra']:,}  R = {result['R']} (heavy {result['heavy']})", end="")
    if result["extra_per_ack"] is not None:
        print(f"  extra per acknowledgement = {result['extra_per_ack']:,.0f}")
    else:
        print()
    for p in result["problems"]:
        print("PROBLEM:", p)
