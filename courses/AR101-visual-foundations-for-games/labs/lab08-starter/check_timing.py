"""AR101 Lab 08: check a pair of timing sheets (light and heavy) for one set of drawings.

    .venv/bin/python check_timing.py light.csv heavy.csv

Each CSV has the header  drawing,hold_ticks,phase  and one row per drawing, in
play order. phase is windup, active or recovery. Ticks are 1/60 s.

The brief's rules, checked here:
  1. Both sheets list the same drawings in the same order (same art, new timing).
  2. Holds are whole numbers from 1 to 60. Phases run windup -> active -> recovery,
     each present at least once, never going backwards.
  3. The light sheet totals 15 to 30 ticks.
  4. The heavy windup is at least twice the light windup.
  5. The heavy recovery is longer than the light recovery.
  6. The heavy active phase is no longer than the light active phase + 2 ticks
     (weight must come from windup and recovery, not from a longer hit).
Prints a summary and exits 0 if every rule passes, 1 otherwise.
"""
import csv
import sys

ORDER = {"windup": 0, "active": 1, "recovery": 2}


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    sheet = []
    for n, row in enumerate(rows, start=2):
        try:
            hold = int(row["hold_ticks"])
        except (KeyError, ValueError):
            raise SystemExit(f"{path} line {n}: hold_ticks must be a whole number")
        phase = row.get("phase", "").strip().lower()
        if phase not in ORDER:
            raise SystemExit(f"{path} line {n}: phase must be windup, active or recovery")
        sheet.append((row["drawing"].strip(), hold, phase))
    return sheet


def summary(sheet):
    sums = {"windup": 0, "active": 0, "recovery": 0}
    for _, hold, phase in sheet:
        sums[phase] += hold
    total = sum(sums.values())
    return sums, total


def check(light, heavy):
    problems = []
    if [d for d, _, _ in light] != [d for d, _, _ in heavy]:
        problems.append("rule 1: the two sheets must list the same drawings in the same order")
    for name, sheet in (("light", light), ("heavy", heavy)):
        if any(not 1 <= h <= 60 for _, h, _ in sheet):
            problems.append(f"rule 2: {name} has a hold outside 1-60 ticks")
        seq = [ORDER[p] for _, _, p in sheet]
        if seq != sorted(seq) or set(seq) != {0, 1, 2}:
            problems.append(f"rule 2: {name} phases must run windup, active, recovery, each at least once")
    ls, lt = summary(light)
    hs, _ = summary(heavy)
    if not 15 <= lt <= 30:
        problems.append(f"rule 3: light total is {lt} ticks, needs 15-30")
    if hs["windup"] < 2 * ls["windup"]:
        problems.append(f"rule 4: heavy windup {hs['windup']} < 2 x light windup {ls['windup']}")
    if hs["recovery"] <= ls["recovery"]:
        problems.append(f"rule 5: heavy recovery {hs['recovery']} is not longer than light {ls['recovery']}")
    if hs["active"] > ls["active"] + 2:
        problems.append(f"rule 6: heavy active {hs['active']} > light active {ls['active']} + 2")
    return problems


def report(name, sheet):
    sums, total = summary(sheet)
    print(f"{name:6} total {total:3} ticks = {total * 1000 / 60:6.1f} ms   "
          f"windup {sums['windup']}  active {sums['active']}  recovery {sums['recovery']}")
    t = 0
    for drawing, hold, phase in sheet:
        print(f"         tick {t:3}  {drawing:<12} hold {hold:2}  {phase}")
        t += hold


def main(argv):
    if len(argv) != 3:
        raise SystemExit(__doc__)
    light, heavy = load(argv[1]), load(argv[2])
    report("light", light)
    report("heavy", heavy)
    problems = check(light, heavy)
    for p in problems:
        print("FAIL", p)
    print("ALL RULES PASS" if not problems else f"{len(problems)} rule(s) failed")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
