# MMO305 · Lab 05: DKP simulator

**Assigned:** week 5. **Due:** start of week 6. **Weight:** part of the final design project component (50% of the course); the loot rule you design here can be reused in the final project.
**Lecture:** [Week 5, raiding as organization: roles, attendance, loot rules (DKP)](../lectures/w05-raiding-as-organization-dkp.md). **Interactive:** `examples/w05-dkp-simulator.html`, for checking your first two tasks.

## Objective

Build a simulator for earned-spent and zero-sum DKP, reproduce the lecture's numbers, then extend it with gear groups and use it to design and defend a loot rule for a fictional raid. By the end you should be able to predict, before simulating, which members a loot rule favours, and prove it with a run.

## Starter materials

**Tool.** Python 3 (standard library only) or a spreadsheet. Python is recommended for task 4. Spreadsheet users should lay out one row per night and one column per raider balance.

**Starter code.** Copy this into `dkp.py`. It runs as given and prints nothing useful until you fill in the three `TODO` lines.

```python
import random

def run_season(system, roster, attendance, k, price, e, nights,
               joins=None, leaves=None, seed=0, wants=None, drops=None):
    """Simulate one season of fixed-price DKP.

    system      'es' (earned-spent) or 'zs' (zero-sum)
    roster      list of raider names, in tie-break order
    attendance  dict name -> probability of attending a night (1.0 = always)
    k, price, e items per night, fixed item price, earning per night (es only)
    joins       dict name -> first night active (default 1)
    leaves      dict name -> first night no longer active
    wants       dict name -> gear group (task 3); None means everyone wants everything
    drops       function(night, rng) -> list of k gear groups (task 3)
    Returns balances, items received and first-item night for each raider.
    """
    rng = random.Random(seed)
    joins, leaves = joins or {}, leaves or {}
    bal = {}; items = {n: 0 for n in roster}; first = {}
    for night in range(1, nights + 1):
        active = [n for n in roster
                  if joins.get(n, 1) <= night < leaves.get(n, 10**9)]
        for n in active:
            bal.setdefault(n, 0.0)
        present = [n for n in active if rng.random() < attendance.get(n, 1.0)]
        if not present:
            continue
        for n in present:
            bal[n] += 0  # TODO 1: earning for 'es' and for 'zs'
        groups = drops(night, rng) if drops else [None] * k
        taken = set()
        for g in groups:
            eligible = [n for n in present if n not in taken
                        and (wants is None or g is None or wants[n] == g)]
            if not eligible:
                continue
            winner = eligible[0]  # TODO 2: highest balance, ties to roster order
            taken.add(winner)
            # TODO 3: charge the winner and record the item and first-item night
    return bal, items, first
```

**The raid for task 4.** "Lanternwatch" (the fictional guild from lab 04, now recovered) has a roster of 14 for a 10-player raid. Two items drop per night, each for one armor group. Each night's two drops are drawn independently with probabilities plate 0.30, mail 0.25, leather 0.25, cloth 0.20.

| Raider | Armor group | Attendance | Joins at night |
|---|---|---|---|
| Aster | plate | 1.00 | 1 |
| Bram | plate | 0.95 | 1 |
| Cato | plate | 0.60 | 1 |
| Dara | mail | 1.00 | 1 |
| Eryn | mail | 0.90 | 1 |
| Fenn | mail | 0.50 | 1 |
| Gale | leather | 1.00 | 1 |
| Hollis | leather | 0.85 | 1 |
| Ines | leather | 0.85 | 1 |
| Jory | leather | 0.60 | 1 |
| Kest | cloth | 1.00 | 1 |
| Lio | cloth | 0.90 | 1 |
| Mave | cloth | 0.95 | 25 |
| Nox | plate | 0.95 | 25 |

When more than 10 raiders would attend, only the first 10 in roster order raid that night and the rest are benched. Mave and Nox are recruits who join at night 25. The season is 60 nights.

## Steps

1. **Fill in the TODOs** and reproduce the lecture's four-raider hand table (both systems, nights 1 to 8) and the newcomer result (first item on night 18 under earned-spent with `e = 20`, night 12 under zero-sum). Paste your output.
2. **Reproduce the inflation table.** With `n = 10`, `k = 2`, `P = 50`, a newcomer replacing a veteran at night 21 and `e` in {5, 10, 20, 30}, report the newcomer's first-item night and compare it with `n/k + T(ρ − 1)(n − 1)/n`. Explain any difference of more than one night.
3. **Add gear groups.** Use the `wants` and `drops` arguments. Show with one run that a raider in a small armor group gears faster than one in a large group at equal attendance, and explain why in two sentences.
4. **Design a loot rule for Lanternwatch.** Add the bench rule (first 10 in roster order raid) and choose a system, earning rule, price and any extras you want (bench pay, a cap, weekly decay). Run at least 500 seasons with different seeds. Report for each raider: mean items by night 60, and mean first-item night. Report for Mave and Nox separately.
5. **Compare against a baseline.** Run plain earned-spent with `e = 20`, `P = 50` on the same roster and seeds. Put the two result tables side by side.
6. **Defend it.** Write a 400-word memo to Lanternwatch's officers recommending your rule. It must state `ρ` for your rule, name who gains and who loses compared with the baseline, and say how your rule affects the guild's recruitment `R` and churn `c` from week 4.

## Deliverable

`dkp.py` (or the spreadsheet), a results document with the outputs of steps 1 to 5 in tables, and the memo from step 6.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Correct simulator | 20 | Both systems implemented; hand table and newcomer nights reproduced exactly | Reproduces one system only | Does not reproduce the lecture |
| Inflation table and formula | 15 | All four rows reported, compared with the formula, differences explained | Rows reported without comparison | Missing |
| Gear groups | 15 | Working groups; small-versus-large group effect shown and explained | Shown but not explained | Missing |
| Lanternwatch design runs | 20 | 500+ seasons, per-raider means, recruits reported separately, bench rule applied | Fewer seasons or missing recruits | Single run only |
| Baseline comparison | 10 | Same seeds, side-by-side table | Different seeds or incomplete table | Missing |
| Memo | 20 | States `ρ`, names winners and losers with numbers, links to `R` and `c` | Recommendation without numbers or without the week 4 link | Missing |
