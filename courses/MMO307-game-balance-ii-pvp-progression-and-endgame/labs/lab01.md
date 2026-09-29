# MMO307 · Lab 01: Gear chase simulator

**Week:** 1, the endgame problem ([lecture](../lectures/w01-the-endgame-problem.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%). The simulator is reused in week 6 (catch-up) and week 11 (seasons).

## Objective

Build a small simulator that answers "when is a player done?" for four reward systems: random drops, a choice of `m`, tokens and a hybrid of drops and tokens. Then use it to design the gear chase for one content tier so that it fits a 14-week calendar and keeps the upgrade chance per run above a floor you choose.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`gear_chase.py`](lab01-starter/gear_chase.py), a skeleton with six functions to fill in: `upgrade_chance`, `expected_runs`, `finish_cdf`, `percentile_run`, `token_runs` and `simulate_hybrid`. Each docstring states the rule from the lecture.
- [`test_gear_chase.py`](lab01-starter/test_gear_chase.py), tests built from the lecture's numbers. Examples: 29.29 expected runs for `S = 10`; median, 90th and 99th percentile finish runs of 27, 44 and 66; 14.78 runs with a choice of 3; a token set of 30 runs; a hybrid with `d = 0.25` and `q = 8` whose median lands between runs 38 and 42. Run `python test_gear_chase.py`. Every test prints `TODO` on the starter.
- The [interactive](../examples/w01-upgrade-decay.html) for spot checks.

## Steps

1. **Closed forms.** Implement `upgrade_chance` and `expected_runs`. Check `expected_runs(10)` against the lecture's table by hand for the first three rows.
2. **Exact distribution.** Implement `finish_cdf` as a Markov chain over `k`, the number of filled slots. Keep a list of probabilities of length `S + 1` and update it once per run. Use it for `percentile_run`.
3. **Tokens and hybrid.** Implement `token_runs` and `simulate_hybrid`. Use `random.Random(seed)` so your results are reproducible.
4. **Tests.** Run the tests until all pass.
5. **Upgrade rate.** Add a function that returns the expected upgrade chance on each run `n`, for random drops and for a choice of `m` (use the same Markov chain: sum `P(K_n = k) × p(k)`). For the hybrid, estimate it from the simulation as the share of players who gain at least one slot on run `n`. Plot all four systems on one chart for `S = 10` (matplotlib, or paste into a spreadsheet).
6. **Design task.** A tier lasts 16 weeks. The set has `S = 12` slots. Your median player runs the content 3 times a week, a light player once, a heavy player 12 times. Design a system (any of the four, with any cap) that meets all of these:
   - the median player finishes between weeks 13 and 15;
   - no more than 10% of median players are still missing a slot at week 16;
   - the expected upgrade chance per run stays at or above 20% until the median player is done;
   - the heavy player does not finish before week 8.
   Report the parameters and the finish weeks for light, median and heavy players.
7. **Sensitivity.** Change `S` from 12 to 14 (a new slot type is added mid-tier) without changing anything else. Which of your four targets break first, and by how much?

## Deliverable

Your completed `gear_chase.py` with passing tests, the step 5 chart, and a report of at most 600 words. The report gives your step 6 design with its numbers, the step 7 result and one paragraph on which player (light, median, heavy or unlucky) your design treats worst.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Simulator correctness | All provided tests pass; code readable, no hard-coded answers | Tests pass but functions duplicate logic or hard-code `S` | Tests fail | 30% |
| Upgrade-rate chart | Four systems on one chart, axes labelled, crossings of the 20% floor marked | Chart present, one system missing or unlabelled | Missing | 15% |
| Design task | All four targets met, numbers shown for three player types | Three of four targets met, trade-off explained | Fewer than three targets met | 30% |
| Sensitivity | Identifies which target breaks first with numbers, proposes a fix | Identifies the break without numbers | Missing | 15% |
| Report | Clear, within length, names the worst-treated player with evidence | Clear but thin on evidence | Hard to follow or over length | 10% |
