"""MMO309 Lab 14: response scorecard.

Model (lecture week 14, section 2). One attack cycle has three durations in days:
    detect  days from the attack going live to a signal you trust
    act     days from that signal to your action
    down    days from your action until the attack is live again
    live    = detect + act
    uptime  = live / (live + down)          (1.0 when down == 0)
Money, per year, with h = harm per live day, K = studio cost, C = honest-player cost:
    harm_left = 365 * h * uptime
    saving    = 365 * h - harm_left - K - C
A day of attacker downtime is worth live / down days of faster detection (inf when down == 0).
Lawsuit break-even: h >= L / (365 * (u_before - u_after)); inf if uptime does not fall.

Multi-year (this lab). K_first is paid in year 1 and K_later in every later year; C and the
harm are paid every year. Over n years:
    saving_n = n * (365 * h - harm_left - C) - K_first - (n - 1) * K_later

Fill in every function marked TODO. Run `python test_scorecard.py` to check.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent


def load(path=HERE / "levers.json"):
    """Return the parsed levers.json as a dict."""
    return json.loads(Path(path).read_text())


def uptime(detect, act, down, **_):
    """TODO: share of the year the attack is live."""
    raise NotImplementedError


def one_year(lever, h):
    """TODO: return (uptime, harm_left, saving) for one year, using K_first as K."""
    raise NotImplementedError


def day_worth(detect, act, down, **_):
    """TODO: how many days of faster detection one day of downtime is worth."""
    raise NotImplementedError


def lawsuit_breakeven(L, u_before, u_after):
    """TODO: the smallest h at which the lawsuit pays."""
    raise NotImplementedError


def saving_over(lever, h, years):
    """TODO: total saving over `years` years with K_first then K_later."""
    raise NotImplementedError


def rank(levers, h, years):
    """TODO: lever names sorted by saving_over, largest first. Ties keep file order."""
    raise NotImplementedError


if __name__ == "__main__":
    data = load()
    for game, g in data["games"].items():
        for years in (1, 3):
            best = rank(data["levers"], g["h"], years)[0]
            print(f"{game:<12} {years}y best: {best:<19} "
                  f"saving ${saving_over(data['levers'][best], g['h'], years):,.0f}")
    print("lawsuit pays when h >=", round(lawsuit_breakeven(**data["lawsuit"])))
