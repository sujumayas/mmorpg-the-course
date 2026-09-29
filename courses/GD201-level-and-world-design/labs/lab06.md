# GD201 · Lab 06: Chokepoint simulator and three-lane arena

**Week:** 6, combat spaces with cover, lanes and chokepoints ([lecture](../lectures/w06-combat-spaces-cover-lanes-chokepoints.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** part of the blockouts assessment (40%). The arena is one of the blockouts you submit.

## Objective

Build a tick simulator for open-field and chokepoint fights, confirm it against the square law and the chokepoint law, and use it to tune a three-lane greybox arena. The goal is an arena where a coordinated push on one lane succeeds if the defenders rotate late and fails if they rotate on time.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`choke_sim.py`](lab06-starter/choke_sim.py), with empty functions `kill_rate`, `square_law`, `choke_losses`, `fall_time`, `fight`, `cover_factor` and `weakest_lane`, plus a `report()` that prints the lecture's table once they work.
- [`check_lab06.py`](lab06-starter/check_lab06.py), 17 checks from the lecture's numbers: 30 against 10 in the open leaves 28.28; a two-wide gate costs 25 and lasts 50 s; a one-wide gate leaves 6.40 defenders; half cover at a four-wide gate leaves 11.94 attackers; the 4/3/3 lane split falls in 15 s. All fail on the starter. Do not edit it.
- The [interactive](../examples/w06-chokepoint-law.html) for spot checks.

## Steps

1. **Closed forms.** Implement `kill_rate`, `square_law`, `choke_losses`, `fall_time` and `cover_factor`.
2. **Simulator.** Implement `fight` exactly as its docstring says. Both updates in a tick must use the counts from the start of that tick. Run `python check_lab06.py` until all 17 checks pass.
3. **Where the formula breaks.** For 10 defenders at `w = 2` with equal fighters, run `fight` for every attacker count from 20 to 40. Plot attackers left against `A₀`, with the closed-form line `A₀ − 25` on the same axes. Mark where the two diverge and explain why, using the formula's validity condition.
4. **Lanes.** Implement `weakest_lane`. Then, for 12 defenders on a map with three `w = 2` lanes, list every split (such as 6/3/3 or 4/4/4) and its weakest-lane fall time. Which split maximizes the time the defenders buy? What rotation time does that split tolerate?
5. **Build the arena.** Greybox a three-lane arena in the course engine for 6 against 6. Give each lane one chokepoint, and at least one lane half cover at its choke. Measure each choke's width in characters abreast using the course's character collision width, and each rotation route's length. Use a movement speed of 6 m/s unless your engine's metrics say otherwise.
6. **Tune.** Using your measured widths and routes, and a 10-second time-to-kill, adjust the geometry (not the numbers) until two conditions hold for an even 2/2/2 defender split: (a) the weakest lane falls in more time than the fastest rotation into it, and (b) it falls in less time than the slowest rotation into it. Report the widths, route lengths, fall times and rotation times before and after.
7. **Playtest.** Run at least three 6-against-6 rounds (or 3-against-3 with halved numbers) in which attackers commit to one lane. Record which lane was attacked, when defenders started rotating and who won. Compare with the model's prediction and explain one difference.

## Deliverable

Your completed `choke_sim.py` with all checks passing, the plot from step 3, the split table from step 4, a top-down screenshot of your arena with widths and route lengths labeled, and a report of at most 700 words covering steps 3, 4, 6 and 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Simulator correctness | All 17 checks pass; tick order correct | 13-16 checks pass | Fewer than 13 | 25% |
| Validity analysis | Divergence located and explained with `A₀ ≥ losses + w` | Plot correct, explanation thin | Missing | 15% |
| Lane splits | All splits listed, best split and tolerated rotation time found | Partial list or no rotation time | Missing | 15% |
| Arena and tuning | Measured widths and routes; both tuning conditions met by geometry changes | One condition met, or tuned by changing numbers | Not tuned | 30% |
| Playtest comparison | Three rounds recorded, prediction compared, one difference explained | Fewer rounds or no explanation | Missing | 15% |
