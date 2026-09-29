"""Lab 10: who answered the survey?

Fill in the five functions marked TODO. The model is in the week 10 lecture, section 2
(inverse-probability weights and effective sample size) and section 3 (capture-recapture).
Standard-library Python 3 only. Run this file to print the results table:

    ../../../../.venv/bin/python feedback.py
"""
import csv


def read_survey(path="survey.csv"):
    """Return a list of dicts with float hours_7d, int sessions_7d and int approve."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(dict(player_id=r["player_id"], segment=r["segment"],
                             hours_7d=float(r["hours_7d"]), sessions_7d=int(r["sessions_7d"]),
                             approve=int(r["approve"])))
    return rows


def read_ids(path):
    with open(path) as f:
        return {line.strip() for line in f if line.strip()}


def raw_share(rows):
    """Unweighted share of respondents with approve == 1."""
    # TODO
    raise NotImplementedError


def ipw_share(rows, pi_column="hours_7d"):
    """Inverse-probability weighted share: sum(w * y) / sum(w) with w = 1 / row[pi_column].

    pi_column names the telemetry field the chance of being asked is proportional to.
    """
    # TODO
    raise NotImplementedError


def kish_neff(weights):
    """Kish effective sample size: (sum w)^2 / sum(w^2)."""
    # TODO
    raise NotImplementedError


def lincoln_petersen(a, b):
    """Estimated population from two sets of account ids: |a| * |b| / |a & b|.

    Raise ValueError if the sets do not overlap.
    """
    # TODO
    raise NotImplementedError


def chapman(a, b):
    """Small-overlap corrected estimate: (|a| + 1)(|b| + 1) / (|a & b| + 1) - 1."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    rows = read_survey()
    print(f"respondents {len(rows)}")
    print(f"raw approval               {raw_share(rows):.1%}")
    print(f"weighted by 1/hours        {ipw_share(rows, 'hours_7d'):.1%}")
    print(f"weighted by 1/sessions     {ipw_share(rows, 'sessions_7d'):.1%}")
    print(f"effective sample (1/hours) {kish_neff([1 / r['hours_7d'] for r in rows]):.0f}")
    forum, reporter = read_ids("forum_accounts.txt"), read_ids("reporter_accounts.txt")
    stuck = read_ids("stuck_accounts.txt")
    print(f"forum {len(forum)}, reporter {len(reporter)}, both {len(forum & reporter)}")
    print(f"Lincoln-Petersen {lincoln_petersen(forum, reporter):.0f}, "
          f"Chapman {chapman(forum, reporter):.0f}, telemetry count {len(stuck)}")
