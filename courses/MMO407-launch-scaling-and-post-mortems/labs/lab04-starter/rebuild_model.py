"""MMO407 lab 04: patch or rebuild. Standard-library Python 3.10+.

Model from the week 4 lecture (units: fix-units = one month of healthy-code work).

  T_patch   = G * (phi * m + 1 - phi) / F
  build     = T_r / (1 - s)
  carried   = c * s * F * build
  T_rebuild = build + max(0, (1 - phi) * G - carried) / F
  m*        = T_r * F / (phi * G)

Fill in every function marked TODO, then run:  python -m unittest test_rebuild_model.py
"""

# The lecture's reference studio (invented teaching values).
REF = {"G": 300, "F": 10, "T_r": 24}


def patch_months(G, phi, m, F):
    """TODO 1. Months to close the whole gap by patching the old code."""
    raise NotImplementedError("patch_months")


def rebuild_months(G, phi, F, T_r, s=0.0, c=0.0):
    """TODO 2. Months to relaunch on a new foundation, with share s of the team
    kept on the old game and share c of their work carried over."""
    raise NotImplementedError("rebuild_months")


def crossover_m(G, phi, F, T_r):
    """TODO 3. The structural penalty at which both paths take equally long (s = 0)."""
    raise NotImplementedError("crossover_m")


def old_game_gap(t, G, phi, m, F, s):
    """TODO 4. Gap players of the OLD game see at month t during a rebuild.
    The share s of the team patches it at the old-code price, so the gap falls by
    s * F / (phi * m + 1 - phi) units per month. Never below 0."""
    raise NotImplementedError("old_game_gap")


def players_after(P0, months, gap_at, G, base=0.02, k=0.05):
    """TODO 5. Players left after `months` months if each month a share
    base + k * gap_at(t) / G leaves, for t = 0, 1, ..., months - 1.
    gap_at is a function of the month."""
    raise NotImplementedError("players_after")


# ---- helpers (provided) -----------------------------------------------------

def patch_gap(t, G, phi, m, F):
    """Gap on the patch path at month t (linear, as in the lecture's interactive)."""
    return G * max(0.0, 1 - t / patch_months(G, phi, m, F))


def print_lecture_table():
    for label, phi, m in [("A, surface problems", 0.1, 3), ("B, deep but cheap", 0.5, 1.5),
                          ("C, deep and taxing", 0.5, 4)]:
        p = patch_months(REF["G"], phi, m, REF["F"])
        r = rebuild_months(REF["G"], phi, REF["F"], REF["T_r"])
        mstar = crossover_m(REF["G"], phi, REF["F"], REF["T_r"])
        print(f"{label:22} patch {p:5.1f}  rebuild {r:5.1f}  m* {mstar:4.2f}")
    for s, c in [(0, 0), (0.25, 0), (0.25, 0.5)]:
        print(f"C with s={s:.2f}, c={c:.1f}: rebuild "
              f"{rebuild_months(REF['G'], 0.5, REF['F'], REF['T_r'], s, c):5.1f} months")


if __name__ == "__main__":
    print_lecture_table()
