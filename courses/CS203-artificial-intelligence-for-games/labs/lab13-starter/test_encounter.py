"""Checks for CS203 Lab 13. Run from this folder: python test_encounter.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys
from fractions import Fraction as F

import encounter as e

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"TODO: {exc} not written yet"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def windows():
    got = e.phase_windows(e.WARDEN, 4_400, "hp")
    want = [(0, F(600, 11)), (F(600, 11), F(1050, 11)), (F(1050, 11), F(1500, 11))]
    if got != want:
        return False, f"hp at 4,400: got {got}"
    got = e.phase_windows(e.WARDEN, 4_400, "time")
    want = [(0, 120), (120, 210), (210, None)]
    if got != want:
        return False, f"time at 4,400: got {got}"
    got = e.phase_windows(e.WARDEN, 6_000, "guard")
    want = [(0, 40), (40, 85), (85, 115)]
    return got == want, f"guard at 6,000: got {got}, want {want}"


def casts():
    tests = [((0, 40, 15, 25, 1000), [15]), ((0, 41, 15, 25, 1000), [15, 40]),
             ((100, None, 15, 25, 160), [115, 140]), ((0, 39, 40, 40, 1000), []),
             ((F(1), F(41), 40, 40, 1000), [])]
    for args, want in tests:
        got = e.cast_times(*args)
        if list(got) != want:
            return False, f"cast_times{args}: got {got}, want {want}"
    return True, ""


LECTURE = {  # dps: (hp counts, time counts) from the lecture's table
    2_000: ([3, 2, 3], [3, 2, 3]), 3_200: ([2, 1, 2], [3, 1, 0]),
    4_400: ([1, 1, 2], [3, 0, 0]), 4_600: ([1, 0, 1], [3, 0, 0]),
    6_000: ([1, 0, 1], [2, 0, 0]),
}


def lecture_table():
    for dps, (hp, tm) in LECTURE.items():
        for mode, want in (("hp", hp), ("time", tm)):
            got = e.counts(e.WARDEN, e.run(e.WARDEN, dps, mode))
            if got != want:
                return False, f"{mode} at {dps}: got {got}, want {want}"
    r = e.run(e.WARDEN, 4_400, "hp")
    first_meteor = [t for t, _, n in r["events"] if n == "Meteor"]
    if first_meteor != [F(600, 11) + 40]:
        return False, f"Meteor at 4,400 should be at 94.5 s, got {first_meteor}"
    return True, ""


def enrage():
    r = e.run(e.WARDEN, 1_600, "hp")
    if r["outcome"] != "enrage" or r["end"] != 360:
        return False, f"1,600 DPS should enrage at 360, got {r['outcome']} at {r['end']}"
    if e.counts(e.WARDEN, r) != [3, 2, 4]:
        return False, f"casts before the enrage: got {e.counts(e.WARDEN, r)}, want [3, 2, 4]"
    if any(t >= 360 for t, _, _ in r["events"]):
        return False, "an event happens at or after the enrage"
    r = e.run(e.WARDEN, 2_000, "time")
    return (r["outcome"], r["end"]) == ("kill", 300), f"2,000 time mode: {r['outcome']} at {r['end']}"


def thresholds():
    if e.skip_threshold(e.WARDEN, "P2", "Meteor") != 4_500:
        return False, "Meteor threshold should be 4,500"
    if e.skip_threshold(e.FOUNDRY, "Merged", "Crucible") != 4_000:
        return False, "Crucible threshold should be 4,000"
    at = e.counts(e.WARDEN, e.run(e.WARDEN, 4_500, "hp"))[1]
    below = e.counts(e.WARDEN, e.run(e.WARDEN, 4_499, "hp"))[1]
    return (at, below) == (0, 1), f"Meteor casts at 4,500 and 4,499: got {at}, {below}; want 0, 1"


def guard():
    r = e.run(e.WARDEN, 6_000, "guard")
    if (e.counts(e.WARDEN, r), r["end"]) != ([1, 1, 1], 115):
        return False, f"guard at 6,000: got {e.counts(e.WARDEN, r)} ending at {r['end']}"
    for dps in (2_000, 3_200):
        a, b = e.run(e.WARDEN, dps, "guard"), e.run(e.WARDEN, dps, "hp")
        if a != b:
            return False, f"guard and hp should agree at {dps} DPS"
    return True, ""


def foundry():
    r = e.run(e.FOUNDRY, 4_000, "guard")
    want_counts, want_end = [4, 1, 3, 1], 110
    if (e.counts(e.FOUNDRY, r), r["end"]) != (want_counts, want_end):
        return False, f"Foundry guard at 4,000: got {e.counts(e.FOUNDRY, r)} ending at {r['end']}"
    times = [t for t, _, _ in r["events"]]
    if times != sorted(times):
        return False, "events are not sorted by time"
    return r["events"][:3] == [(10, "Split", "Hammer"), (22, "Split", "Hammer"),
                               (30, "Split", "Bellows")], f"first events: {r['events'][:3]}"


check("step 1: phase windows for hp, time and guard", windows)
check("step 2: cast times", casts)
check("step 3: the lecture's table, both modes", lecture_table)
check("step 3: enrage cuts the fight at 360 s", enrage)
check("step 4: skip thresholds are exact", thresholds)
check("step 5: guard keeps one Meteor at 6,000 DPS", guard)
check("step 5: works on a second boss", foundry)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
