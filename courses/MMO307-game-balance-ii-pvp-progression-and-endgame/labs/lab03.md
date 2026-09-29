# MMO307 · Lab 03: Horizontal reward track

**Week:** 3, horizontal progression ([lecture](../lectures/w03-horizontal-progression.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%). The segment mixes you estimate here return in week 7 (split tuning) and week 14 (measuring balance).

## Objective

Estimate the content mix of two player segments from a play log, compute what each horizontal reward is worth to each segment, and tune a reward track (bonus size, rotation and gates) so that every segment has enough rewards worth chasing while the power gap stays under a limit.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`play_log.csv`](lab03-starter/play_log.csv), a synthetic week of play for 16 players in two segments (`raider` and `pvp`). Each row is a 10-minute block in one of six situations: `boss_heavy`, `trash_heavy`, `armored`, `swarm`, `vertical_zone`, `arena`. The data is invented for the lab.
- [`horizontal.py`](lab03-starter/horizontal.py), a skeleton with a working `load_log` and nine functions to fill in: `estimate_mix`, `zipf`, `rotate`, `values`, `n_eff`, `gap_ceiling`, `tools_worth_chasing`, `gate_share` and `gate_marginals`.
- [`test_horizontal.py`](lab03-starter/test_horizontal.py), tests from the lecture's numbers (Zipf values 12.24% to 2.04%, `N_eff = 4.02`, `G_max = 1.158`, the rotation table, gate marginals 0, 33.3, 66.7) and from the log (raider mix 0.40, 0.25, 0.15, 0.10, 0.06, 0.04). Run `python test_horizontal.py`. On the starter only the loading test passes.
- The [interactive](../examples/w03-situation-weights.html) for spot checks (use the Custom mix).

## Steps

1. **Implement and test.** Fill in the nine functions and run the tests until all pass.
2. **Two segments.** Print each segment's mix, `N_eff`, and each tool's value at `b = 0.3`. Put both segments in one table. Which tools does each segment consider worth chasing at `u = 4%`?
3. **Design task.** You may choose one bonus size `b` (0.05 to 1.0) for all six tools and one rotation strength `λ` (0 to 1) applied to both segments. Meet all three targets:
   - each segment has at least 4 tools with value at or above `u = 4%`;
   - `G_max` is at most 1.25 for each segment;
   - `b` is as small as possible among designs meeting the first two (smaller bonuses are easier to balance).
   Search a grid (step 0.05 for both) and report the chosen `(b, λ)` with every segment's numbers.
4. **Gates.** Turn the `arena` tool into a gate for PvP players (they cannot play rated arena without it) and leave it a bonus for raiders. Explain in two sentences what this does to the PvP players' chase, using the marginal-value shape from lecture section 4. Then design a small gate system of your own. Write an activity list for `gate_share` with three or four counters and mixed requirement sizes, so that the first counter a player earns opens at least 20% of activities and at least one activity still needs every counter. Report the list and the marginal value of each counter in the order you expect players to earn them.
5. **Content change.** A new raid shifts raiders' play so that `armored` rises to 35% and the other five situations shrink in proportion. Recompute the raider values under your step 3 design. Which tool becomes best-in-slot for raiders? Does any target from step 3 break?

## Deliverable

Your completed `horizontal.py` with passing tests, and a design note of at most 600 words with the step 2 table, your step 3 design and grid-search evidence, your step 4 gate system, and the step 5 result with one recommendation.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All tests pass; functions reused rather than duplicated | Tests pass, some duplication | Tests fail | 25% |
| Segment analysis | Mixes, `N_eff` and values correct for both segments, chase lists correct | One segment incomplete | Numbers wrong | 20% |
| Design task | All targets met, smallest `b` found with grid evidence | Targets met but `b` not minimal or evidence missing | Targets not met | 25% |
| Gates | Correct marginal-shape explanation and a valid gate design meeting the 20% rule | Explanation or design only | Missing | 15% |
| Content change and note | Best-in-slot tool identified with numbers, broken targets named, sensible recommendation | Tool identified, no recommendation | Missing | 15% |
