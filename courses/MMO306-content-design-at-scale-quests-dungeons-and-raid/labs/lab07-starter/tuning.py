"""MMO306 Lab 07 starter: tuning an encounter from logs.

Fill in every function marked TODO. Standard library only.
Run the checks with:   python test_lab07.py
Run the report with:   python tuning.py
"""
import csv
import math
from collections import Counter
from statistics import NormalDist

ENRAGE_T = 400            # seconds, the Warden's hard enrage
BOSS_H = 440_000_000      # the Warden's health on Mythic
STD = NormalDist()        # STD.cdf(z) is Phi(z), STD.inv_cdf(p) is its inverse


def read_pulls(path):
    """Read an encounter log and return one dict per pull, in pull order:
        {"pull": int, "length": float, "damage": int, "dps": float,
         "kill": bool, "first_death": str or None, "deaths": Counter}
    `length` is the t of ENCOUNTER_END. `kill` is True when its amount is 1.
    `damage` sums DAMAGE amounts. `first_death` is the ability on the first
    DEATH line of the pull (lines are already in time order).
    """
    raise NotImplementedError("TODO: read_pulls")


def wipe_causes(pulls, enrage_t=ENRAGE_T):
    """Classify every wipe (kill is False). A wipe whose length is at least
    enrage_t counts as "Enrage". Any other wipe counts under its first_death.
    Return a dict {cause: share of wipes}, shares summing to 1.
    """
    raise NotImplementedError("TODO: wipe_causes")


def deaths_per_100(path):
    """Deaths per 100 exposures for each ability that has CAST lines.
    Exposures = sum of CAST amounts (players targeted) for that ability.
    Deaths = number of DEATH lines with that ability. Return {ability: rate}.
    """
    raise NotImplementedError("TODO: deaths_per_100")


def survival(pulls, t):
    """Share of pulls whose length is at least t seconds."""
    raise NotImplementedError("TODO: survival")


def kill_rate(dps_values, h, t=ENRAGE_T):
    """Share of groups whose DPS is at least h / t."""
    raise NotImplementedError("TODO: kill_rate")


def fit_lognormal(dps_values):
    """Return (m, sigma): m = exp(mean of ln D), sigma = population std dev of ln D."""
    raise NotImplementedError("TODO: fit_lognormal")


def model_kill_rate(h, m, sigma, t=ENRAGE_T):
    """K = 1 - Phi(ln(h / (t m)) / sigma)."""
    raise NotImplementedError("TODO: model_kill_rate")


def health_for_target(k_target, m, sigma, t=ENRAGE_T):
    """Boss health that gives kill rate k_target in the model."""
    raise NotImplementedError("TODO: health_for_target")


def weighted_kill_rate(rows, h, upload_rate, t=ENRAGE_T):
    """rows: list of (dps, uploaded) with uploaded 0 or 1.
    Use only uploaded rows, weight each by 1 / upload_rate(dps), and return
    the weighted share with dps >= h / t.
    """
    raise NotImplementedError("TODO: weighted_kill_rate")


def load_best_pulls(path):
    """Return a list of (best_dps, uploaded) tuples from best_pulls.csv."""
    with open(path, newline="") as f:
        return [(int(r["best_dps"]), int(r["uploaded"])) for r in csv.DictReader(f)]


def report():
    pulls = read_pulls("encounter_log.csv")
    print(f"{len(pulls)} pulls, {sum(p['kill'] for p in pulls)} kill(s)")
    for cause, share in sorted(wipe_causes(pulls).items(), key=lambda kv: -kv[1]):
        print(f"  wipe cause {cause:14} {share:6.1%}")
    for a, rate in deaths_per_100("encounter_log.csv").items():
        print(f"  {a:14} {rate:5.2f} deaths per 100 exposures")
    print("  survival at 100/200/300/400 s:",
          [round(survival(pulls, s), 3) for s in (100, 200, 300, 400)])
    rows = load_best_pulls("best_pulls.csv")
    everyone = [d for d, _ in rows]
    logged = [d for d, up in rows if up]
    m, s = fit_lognormal(everyone)
    print(f"population: K={kill_rate(everyone, BOSS_H):.3f}  m={m:,.0f} sigma={s:.4f}"
          f"  model K={model_kill_rate(BOSS_H, m, s):.3f}")
    ml, sl = fit_lognormal(logged)
    print(f"logged only: K={kill_rate(logged, BOSS_H):.3f}  m={ml:,.0f} sigma={sl:.4f}")
    print(f"health for 35% (population fit): {health_for_target(0.35, m, s):,.0f}")


if __name__ == "__main__":
    report()
