"""MMO405 Lab 08: link a survey to telemetry and integrate it with interviews.

Run:  python gen_data.py        # once, writes survey.csv and telemetry.csv
      python linkage.py         # prints the analysis once your functions work
      python check_lab08.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
A linked row is a dict with keys: account_id, cohort, reported_h,
logged_total_h, logged_active_h (numbers as floats).
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEASURES = ("logged_total_h", "logged_active_h")


def load(name):
    with open(HERE / name, newline="") as f:
        return list(csv.DictReader(f))


def link(survey, telemetry):
    """Inner-join survey rows to telemetry rows on account_id.
    Return (linked, unmatched): linked is a list of dicts as described in the
    module docstring, in the order of the survey file; unmatched is the sorted
    list of survey account_ids with no telemetry row."""
    raise NotImplementedError


def discrepancy(row, measure="logged_total_h"):
    """d = reported_h minus the chosen logged measure."""
    raise NotImplementedError


def group_summary(linked, measure="logged_total_h"):
    """Return {cohort: (mean reported, mean logged, mean discrepancy, n)}."""
    raise NotImplementedError


def decompose(summary, a="veteran", b="new"):
    """Return (survey_gap, log_gap, bias_gap) for group a minus group b, where
    survey_gap = log_gap + bias_gap."""
    raise NotImplementedError


def select_cases(linked, measure="logged_total_h", k_under=4, k_accurate=2):
    """Connecting rule, applied within each cohort.
    Under-reporters: the k_under rows with the most negative discrepancy
    (sort by (d, account_id) ascending).
    Accurate reporters: then the k_accurate rows, not already chosen, with the
    smallest |d| (sort by (|d|, account_id) ascending).
    Return {cohort: {"under": [ids], "accurate": [ids]}}."""
    raise NotImplementedError


def theme_table(selected, interviews):
    """Statistics-by-themes joint display.
    interviews is a list of dicts with keys account_id and themes, where themes
    is a ';'-separated string of theme codes. Use only interviews whose
    account_id was selected. Strata are f"{cohort}-{kind}" with kind "under" or
    "accurate". Count participants (not mentions) per theme per stratum.
    Return {theme: {stratum: count}} including zero counts for every stratum."""
    raise NotImplementedError


def main():
    linked, unmatched = link(load("survey.csv"), load("telemetry.csv"))
    print(f"linked {len(linked)} respondents; unmatched ids: {', '.join(unmatched)}")
    for m in MEASURES:
        s = group_summary(linked, m)
        for c in sorted(s):
            r, l, d, n = s[c]
            print(f"  {m:16} {c:8} n={n:3} reported {r:5.2f} logged {l:5.2f} bias {d:+.2f}")
        g_r, g_l, g_b = decompose(s)
        print(f"  {m:16} survey gap {g_r:+.2f} = log gap {g_l:+.2f} + bias gap {g_b:+.2f}")
    sel = select_cases(linked)
    print("selected:", sel)
    table = theme_table(sel, load("interviews.csv"))
    strata = sorted({k for row in table.values() for k in row})
    print(f"{'theme':22}" + "".join(f"{s:>18}" for s in strata))
    for theme in sorted(table):
        print(f"{theme:22}" + "".join(f"{table[theme][s]:>18}" for s in strata))


if __name__ == "__main__":
    main()
