# MMO306 · Lab 04: The enrage line

**Week:** 4, encounter mechanics ([lecture](../lectures/w04-encounter-mechanics-tank-and-spank-to-dance-fights.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the encounter designs (40%). The calculator is reused in labs 05 and 06 and in the final dungeon.

## Objective

Finish a small encounter calculator that turns a boss (health, enrage, mechanics) and a group (paper DPS, execution factor) into uptime, hidden health and kill time, with both the lecture's average model and its tick simulation. Then use it to tune three bosses to three stated design goals.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python 3.10 or later.

- [`encounter.py`](lab04-starter/encounter.py) defines `Boss` and `Group` dataclasses, the lecture's Quakemaw, Stitchgut and groups A and B, and eight functions marked TODO: `tax`, `uptime`, `kill_time`, `passes`, `hidden_health`, `required_paper_dps`, `simulate` and `max_deaths`.
- [`test_encounter.py`](lab04-starter/test_encounter.py) checks the lecture's numbers: Quakemaw tax 0.2; kill times 287.5 / 313.6 s on Stitchgut and 306.4 / 284.1 s on Quakemaw; hidden health 6,250,000 for group B; simulated kill 282.3 s for group B; and that one death at 60 s pushes group B to 301.1 s, past the enrage. Run it with `python test_encounter.py`. Every test fails on the starter.
- The [interactive](../examples/w04-enrage-line.html) for spot checks.

## Steps

1. **Average model.** Implement `tax`, `uptime`, `kill_time`, `passes`, `hidden_health` and `required_paper_dps`. Clamp uptime at 0, and return `None` for a kill time when uptime is 0.
2. **Simulation.** Implement `simulate` with integer ticks of 0.1 s, exactly as in lecture section 3. Deaths are given as `(time, count)`, and each dead damage dealer removes `1 / dps_players` of paper DPS from that tick on.
3. **Deaths budget.** Implement `max_deaths(boss, group, when_s)`. Run the tests until all pass.
4. **Boss 1, the gear check.** Design a boss with at most one mechanic (tax at most 0.05) and a 360 s enrage that group A clears with 5 to 15 s spare and group B fails. Report `H`, the mechanic, and both kill times.
5. **Boss 2, the execution check.** Design a boss with three mechanics and a 360 s enrage that group B clears and group A fails, in both the average model and the simulation. Make sure no two mechanic windows overlap for group A (show the schedule for the first 120 s). Report the tax, hidden health for both groups and the tax at which group A would start clearing.
6. **Boss 3, the one-death boss.** Using group B, tune `H` so the group clears with exactly one death at the halfway point of the enrage and fails with two. Report `H` and the three simulated kill times (0, 1 and 2 deaths).
7. **Average versus simulation.** For boss 2, list the gap between the average-model and simulated kill times for both groups, and explain where it comes from (first-cast delay, partial last cycle, or overlap).

## Deliverable

`encounter.py` with all tests passing, and a design memo of at most 600 words with the three boss tables, the schedule from step 5 and the explanation from step 7. Add one paragraph on which of the three bosses you would place first in a raid and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Calculator correctness | All tests pass; code readable and uses integer ticks | Tests pass, code hard to follow | Tests fail | 30% |
| Boss 1 and boss 2 | Both meet their goals in both models, numbers shown | One goal met, or only in one model | Goals not met | 25% |
| Boss 3 | Exactly one death allowed, all three runs reported | Death budget off by one | Missing | 15% |
| Model comparison | Gap measured and traced to its cause | Gap measured, cause guessed | Missing | 15% |
| Design memo | Ordering argued from what each boss tests | Ordering stated without reasons | Missing | 15% |
