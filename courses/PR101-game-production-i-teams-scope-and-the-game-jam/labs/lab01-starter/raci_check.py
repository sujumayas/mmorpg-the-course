"""PR101 Lab 01 checker for a RACI matrix and a coverage matrix.

Usage:
    python raci_check.py raci.csv coverage.csv

raci.csv:     first column 'deliverable', one column per person.
              Cells are A, R, A/R, C, I or empty.
coverage.csv: columns 'skill', 'critical' (yes/no), then one column per person.
              A person cell is 'yes' if that person can do the skill at a usable level.

Errors (make the check fail):
  - a RACI row without exactly one A (A/R counts as an A)
  - a RACI row with no R (A/R counts as an R)
  - an unknown RACI letter
  - a skill nobody covers (bus factor 0)
  - a critical skill with bus factor 1
  - the people in the two files differ
Warnings (reported, do not fail):
  - a person who is A on more than half the rows (possible bottleneck)
  - a non-critical skill with bus factor 1
Exit code 0 when there are no errors, 1 otherwise.
"""
import csv
import sys

VALID = {"A", "R", "A/R", "C", "I", ""}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
    return [h.strip() for h in header], [[c.strip() for c in r] for r in body]


def check_raci(header, body):
    errors, warnings = [], []
    people = header[1:]
    a_count = {p: 0 for p in people}
    for row in body:
        name, cells = row[0], row[1:]
        cells = [c.upper() for c in cells] + [""] * (len(people) - len(cells))
        bad = [c for c in cells if c not in VALID]
        if bad:
            errors.append(f"RACI '{name}': unknown letter(s) {bad}")
        n_a = sum(c in ("A", "A/R") for c in cells)
        n_r = sum(c in ("R", "A/R") for c in cells)
        if n_a != 1:
            errors.append(f"RACI '{name}': {n_a} A's (need exactly 1)")
        if n_r == 0:
            errors.append(f"RACI '{name}': nobody is R")
        for p, c in zip(people, cells):
            if c in ("A", "A/R"):
                a_count[p] += 1
    for p, n in a_count.items():
        if n > len(body) / 2:
            warnings.append(f"RACI: {p} is A on {n} of {len(body)} rows (bottleneck?)")
    return people, errors, warnings


def check_coverage(header, body):
    errors, warnings = [], []
    people = header[2:]
    for row in body:
        skill, critical = row[0], row[1].lower() == "yes"
        cells = row[2:] + [""] * (len(people) - len(row[2:]))
        bus = sum(c.lower() == "yes" for c in cells)
        if bus == 0:
            errors.append(f"coverage '{skill}': nobody covers it (bus factor 0)")
        elif bus == 1 and critical:
            errors.append(f"coverage '{skill}': critical skill with bus factor 1")
        elif bus == 1:
            warnings.append(f"coverage '{skill}': bus factor 1")
    return people, errors, warnings


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    p1, e1, w1 = check_raci(*load(argv[1]))
    p2, e2, w2 = check_coverage(*load(argv[2]))
    errors, warnings = e1 + e2, w1 + w2
    if sorted(p1) != sorted(p2):
        errors.append(f"people differ: RACI {p1} vs coverage {p2}")
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR  ", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
