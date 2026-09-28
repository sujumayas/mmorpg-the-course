# MMO303 · Lab 12: Measuring stat weights with a noisy simulator

**Week:** 12 ([lecture](../lectures/w12-stat-weights-and-theorycrafting.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual.
**Counts toward:** problem sets (30% of the course grade).

## Objective

Measure stat weights the way SimulationCraft does, by running a randomized fight with and without extra stat points. Compare the measured weights with the lecture's exact formula, estimate the noise, and find how large a delta and how many simulated fights you need before you can trust a ranking.

## Starter materials

- [`lab12-starter.py`](lab12-starter.py): a Python 3 skeleton (standard library only) for a single-target fight. It defines a `Char` with power, crit rating, haste rating, crit multiplier and an optional crit cap, the lecture's closed-form `expected_dps`, a `fight(char, seconds, rng)` stub, a `run` helper that reuses a seed for common random numbers, and a helper for mean and standard error. Run it first: it prints the exact weights (0.192 and 0.238) you will compare against.
- The [stat weights interactive](../examples/w12-stat-weights.html) for checking the peak.
- The lecture's class rules: 5% base crit, 0% base haste, 40 rating per 1%, crits deal `m` times damage, base damage per second equals power.
- Python 3 (`numpy` optional), or a spreadsheet using `RAND()` (slower but accepted).

## Steps

### Part A: build the randomized fight (40 min)

1. Implement `fight`. The character attacks once every `1 / (1 + h)` seconds for a 300-second fight. Each attack deals `power` damage, times `m` if a random draw is below `c`. Return total damage divided by 300.
2. Run 1,000 fights at 1,000 power, 1,000 crit rating, 200 haste rating, `m = 2`. The mean should be close to the lecture's 1,365 DPS. Report mean and standard error. (Small bias from whole attack counts is expected; explain it in one sentence.)

### Part B: finite-difference weights (30 min)

3. Using the same random seed sequence for the base run and each changed run (common random numbers), measure the gain from +100 power, +100 crit rating and +100 haste rating. Normalize by the power gain.
4. Compare with the exact weights 0.192 (crit) and 0.238 (haste). Report the difference.
5. Repeat step 3 with independent random seeds for each run. Report how much larger the error becomes and explain why common random numbers help.

### Part C: how much simulation is enough? (35 min)

6. With independent seeds, measure the crit and haste weights 30 times each for every combination of delta (25, 100, 400) and fights per run (100, 1,000). Record the standard deviation of each weight across the 30 repeats.
7. For each combination, decide whether you can say "haste is worth more than crit" with confidence (the gap of 0.046 should exceed about twice the combined standard deviation). Present a table.
8. Turn on the lecture's crit cap at 30% and repeat the delta-400 measurement at 950 crit rating. Explain why the measured crit weight is wrong in a way that a smaller delta would not be.

### Part D: find the peak (15 min)

9. Using your simulator, find the best split of 1,200 rating for `m = 2` and for `m = 2.5` by trying splits in steps of 50. Compare with the lecture (500 and about 1,167 crit rating).

## Deliverable

- The completed script, runnable, with its outputs.
- A 2-page PDF with the Part A result, the Part B comparison, the Part C table with your confidence decisions, the Part C cap explanation and the Part D peaks. End with a 150-word note to a designer: what delta and iteration count would you set as the team's default for internal stat-weight sims, and why?

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Randomized fight (Part A) | Mean within 1% of 1,365 with standard error reported and the bias explained | Runs but mean or error missing | Does not run | 20 |
| Finite-difference weights (Part B) | Weights within 0.02 of exact with common random numbers; independent-seed comparison explained | Weights measured, explanation weak | Missing | 25 |
| Noise study (Part C) | Full table, correct confidence decisions, cap effect explained with the delta range | Table incomplete or decisions not justified | Missing | 30 |
| Peak search (Part D) | Both peaks found and compared with the lecture | One peak found | Missing | 10 |
| Designer note | Specific numbers with a reason tied to the Part C table | Numbers without reasons | Missing | 15 |
| **Total** | | | | **100** |
