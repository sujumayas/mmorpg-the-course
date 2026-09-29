"""MMO307 Lab 07 starter: split tuning between PvE and PvP.
Standard library only. Fill in the TODOs, then run
    .venv/bin/python test_split_tuning.py      (from this folder)
or pytest.

Model from the week 7 lecture:
    PvE DPS = s + B / C
    PvP TTK = max(0, h*H - p*B) / (q*s)
s = sustained DPS, B = burst per cooldown, C = cooldown (s), H = target EHP,
p = PvP burst multiplier, q = PvP sustain multiplier, h = global PvP health multiplier.
"""

H = 30_000
C = 60
PVE_TARGET = 1_100
PVE_TOLERANCE = 0.03          # +-3% of the target
TTK_BAND = (15.0, 22.0)       # seconds, inclusive

# Six invented classes: name -> (s, B). The first three are from the lecture.
ROSTER = {
    "Duelist":   (900, 12_000),
    "Ravager":   (700, 24_000),
    "Channeler": (1_050, 3_000),
    "Assassin":  (600, 30_000),
    "Warden":    (1_000, 6_000),
    "Stormcaller": (820, 16_800),
}


def pve_dps(s, B):
    """TODO step 1. Throughput over a long fight."""
    raise NotImplementedError("pve_dps is yours to write")


def pvp_ttk(s, B, p=1.0, q=1.0, h=1.0):
    """TODO step 1. Time to kill the standard target, opening with the burst."""
    raise NotImplementedError("pvp_ttk is yours to write")


def clone(D, T):
    """TODO step 2. Return (s, B) that hits PvE DPS D and PvP TTK T exactly."""
    raise NotImplementedError("clone is yours to write")


def burst_multiplier(s, B, T):
    """TODO step 3. The p that puts this class at TTK T (q = h = 1)."""
    raise NotImplementedError("burst_multiplier is yours to write")


def sustain_multiplier(s, B, T):
    """TODO step 3. The q that puts this class at TTK T (p = h = 1)."""
    raise NotImplementedError("sustain_multiplier is yours to write")


def audit(roster, splits=None, h=1.0):
    """TODO step 4. Return a dict name -> list of problems, where a problem is
    the string "pve" if PvE DPS is outside the tolerance band, and "pvp" if TTK
    is outside TTK_BAND. splits maps name -> {"p": ..., "q": ...}; missing
    entries mean 1.0. A class with no problems maps to an empty list."""
    raise NotImplementedError("audit is yours to write")


if __name__ == "__main__":
    try:
        for name, (s, B) in ROSTER.items():
            print(f"{name:12} PvE {pve_dps(s, B):7.1f}  TTK {pvp_ttk(s, B):5.1f} s")
    except NotImplementedError as e:
        print("TODO:", e)
