"""MMO405 lab 01: observed gap, stratified gap and the selection term.

Python 3, standard library only. Fill in the three TODOs, then run
    python -m unittest test_selection_audit.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly prints the report once the TODOs are done.
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent


def load_players(path=HERE / "players.csv"):
    """Return a list of dicts with ints for the 0/1 columns."""
    with open(path, newline="") as f:
        return [{"account_id": r["account_id"], "week1_band": r["week1_band"],
                 "in_guild_d7": int(r["in_guild_d7"]), "active_d30": int(r["active_d30"])}
                for r in csv.DictReader(f)]


def retention(rows):
    """Share of rows with active_d30 == 1. Returns None for an empty list."""
    if not rows:
        return None
    return sum(r["active_d30"] for r in rows) / len(rows)


def observed_gap(rows):
    """TODO 1. Return (retention of guild members, retention of non-members, gap).

    Guild members have in_guild_d7 == 1. gap = first minus second.
    """
    raise NotImplementedError("TODO 1")


def stratified_gap(rows, by="week1_band"):
    """TODO 2. Compare like with like.

    Split rows by the value of column `by`. In each stratum compute the gap
    (guild retention minus non-guild retention). Return (per_stratum, overall) where
    per_stratum maps stratum value -> gap, and overall is the average of the stratum
    gaps weighted by each stratum's share of ALL rows. Skip a stratum that has no
    guild members or no non-members, and renormalize the weights over the rest.
    """
    raise NotImplementedError("TODO 2")


def selection_term(r_h, r_l, s_t, s_u):
    """TODO 3. The lecture's two-kind selection term (r_H - r_L) * (s_T - s_U)."""
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    rows = load_players()
    g, u, gap = observed_gap(rows)
    per, overall = stratified_gap(rows)
    print(f"accounts: {len(rows)}")
    print(f"guild {g:.1%}  no guild {u:.1%}  observed gap {gap:+.1%}")
    for band in ("low", "mid", "high"):
        print(f"  {band:>4}: within-band gap {per[band]:+.1%}")
    print(f"stratified gap {overall:+.1%}   share of observed gap that is selection "
          f"{(gap - overall) / gap:.0%}")
