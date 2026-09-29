"""MMO406 Lab 06 starter: myth outcomes and fact-matrix audits.

Standard library only. Fill in the three TODO functions, then run the tests:

    .venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab06-starter/test_myth.py

Model (week 6, section 2). Each of k independent accounts tells a fact truly
(chance p), distorts it (chance q) or stays silent (1 - p - q).

    unrecoverable  fewer than 2 true tellings
    settled        2+ true tellings and no distortion
    answerable     2+ true tellings and 1+ distortion

Fact matrices (see sample_matrix.csv) have one row per fact and one column per
account. A cell is "T" (true), "" (silent) or "D:<label>" (a distortion; two
cells with the same label tell the same false version).
"""
import csv


def outcomes(k, p, q):
    """TODO 1. Return (settled, answerable, unrecoverable) as expected shares.
    Clamp a tiny negative answerable share (float round-off) to 0.0."""
    raise NotImplementedError("outcomes() is yours to write")


def classify_row(cells):
    """TODO 2. Classify one row of cells from INDEPENDENT accounts.

    Return one of 'settled', 'answerable', 'unrecoverable', 'false_consensus'.
    'false_consensus' wins over everything else: it means some distortion
    label appears in 2 or more cells, so a false version looks confirmed."""
    raise NotImplementedError("classify_row() is yours to write")


def audit(rows, accounts, copies=None):
    """TODO 3. Classify every fact, first dropping dependent accounts.

    rows:     list of dicts as read by load_matrix (keys 'fact' + account names)
    accounts: list of account column names
    copies:   dict {copy_name: source_name}; a copy is not an independent
              witness, so its column is ignored when copies is given.
    Return a dict {fact: classification} and do not modify `rows`."""
    raise NotImplementedError("audit() is yours to write")


def load_matrix(path):
    """Read a fact-matrix CSV. Returns (rows, accounts)."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
        accounts = [c for c in reader.fieldnames if c != "fact"]
    return rows, accounts


def summary(classes):
    """Count classifications, in a fixed order."""
    order = ["settled", "answerable", "unrecoverable", "false_consensus"]
    return {c: sum(1 for v in classes.values() if v == c) for c in order}


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    rows, accounts = load_matrix(os.path.join(here, "sample_matrix.csv"))
    print("as written:     ", summary(audit(rows, accounts)))
    print("copy removed:   ", summary(audit(rows, accounts, {"codex_translation": "temple_codex"})))
    for k in range(1, 7):
        print(k, [round(x, 3) for x in outcomes(k, 0.4, 0.2)])
