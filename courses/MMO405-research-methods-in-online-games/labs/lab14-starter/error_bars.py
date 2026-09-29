"""MMO405 lab 14: what a results slide implies, and whether its claim holds.

Python 3, standard library only. Fill in the three TODOs, then run
    python -m unittest test_error_bars.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly audits slides.json once the TODOs are done.

Conventions (lecture week 14): large-sample normal approximation, 95% CI arm = 1.96 x SE,
two-sided tests at alpha = .05.
"""
import json
from math import sqrt
from pathlib import Path
from statistics import NormalDist

HERE = Path(__file__).parent
Z = NormalDist()


def load_slides(path=HERE / "slides.json"):
    with open(path) as f:
        return json.load(f)


def two_sided_p(z):
    return 2 * (1 - Z.cdf(abs(z)))


def se_from_bar(arm, bar, n=None):
    """TODO 1. Recover the standard error of a mean from one bar's arm (half-length).

    bar is "SE", "CI95" or "SD". An SD arm needs n (players in that group):
    SE = SD / sqrt(n). Raise ValueError for an unknown bar type, or for "SD" without n.
    """
    raise NotImplementedError("TODO 1")


def diff_test(m1, s1, m2, s2, paired=False, rho=0.0):
    """TODO 2. Test m2 - m1, where s1 and s2 are the standard errors of the two means.

    Independent: SE_diff = sqrt(s1^2 + s2^2).
    Paired (the same players measured twice, correlation rho between their two scores):
    SE_diff = sqrt(s1^2 + s2^2 - 2 * rho * s1 * s2).
    Return (diff, se_diff, z, p).
    """
    raise NotImplementedError("TODO 2")


def audit_slide(slide):
    """TODO 3. Audit one slide dict from slides.json. Return a dict with keys:

    "p"          two-sided p of the comparison the claim is about.
    "significant" p < 0.05.
    "looks"      for kind "two_groups": "overlap" if the drawn bars overlap
                 (sum of arms > distance between means), else "gap".
                 For kind "two_effects": "one significant, one not" if exactly one
                 effect has p < .05, else "both same".
    "supported"  True if the claim matches the test: claim "different" needs
                 significant, claim "no difference" needs not significant. (This is the
                 weak two-verdict reading; your write-up should use week 2's four verdicts.)

    two_groups: recover each mean's SE with se_from_bar (use slide["n"] for SD bars),
    then diff_test with slide["paired"] and slide["rho"] (None means 0).
    two_effects: the claim is about the DIFFERENCE between the two effects; test it as
    independent with diff_test(effect1, se1, effect2, se2).
    """
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    for s in load_slides():
        a = audit_slide(s)
        print(f"{s['id']}: {s['title']}")
        print(f"    looks: {a['looks']:<24} p = {a['p']:.4f}   claim '{s['claim']}' "
              f"{'supported' if a['supported'] else 'NOT supported'}")
