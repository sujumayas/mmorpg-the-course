# MMO308 · Lab 09: Rollout planner

**Week:** 9, patch management and hotfixes ([lecture](../lectures/w09-patch-management-and-hotfixes.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

Implement the lecture's staged-rollout model, check it against a Monte Carlo simulation, use it to choose stage plans under a time budget, and triage a queue of six bugs with the hotfix rule. Finish with a one-page rollout policy a small MMO team could adopt.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Standard-library Python 3.12 or later (the repository's `.venv` has 3.13).

- [`rollout.py`](lab09-starter/rollout.py): stubs for `reach_probs`, `expected_harm`, `simulate_rollout`, `canary_size`, `rollout_hours`, `best_plan` and `hotfix_decision`, and a loader for the bug queue.
- [`bugs.csv`](lab09-starter/bugs.csv): six invented bugs with harm per hour, hours to the next scheduled patch, restart minutes, concurrent players, hotfix risk and the harm if the hotfix goes wrong.
- [`test_rollout.py`](lab09-starter/test_rollout.py): eight tests from the lecture's tables and the bug queue. All eight fail on the starter.

```
.venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab09-starter/test_rollout.py
```

- The staged-rollout interactive, `examples/w09-staged-rollout.html`, for spot checks.

## Steps

### Part A: the model (45 min)

1. **Reach and harm.** Implement `reach_probs` and `expected_harm`. The tests check the lecture's values: 100 for a big bang, 4.3 for 1% → 10% → 100% at `d = 1`, 20.5 at `d = 0.2`.
2. **Simulate.** Implement `simulate_rollout` with `rng.binomialvariate`, as the docstring describes. The test compares the mean of 4,000 simulated rollouts with the formula, allowing four standard errors (MA102 week 11). Then run 20,000 simulations yourself for the `d = 0.2` plan and report the median and the 95th percentile of players hit. Why is the mean a poor summary here?
3. **Canary size.** Implement `canary_size` and confirm the rule of three: 14,978 players to catch a one-in-5,000 bug at `d = 1`.

### Part B: planning (40 min)

4. **Time budget.** Implement `rollout_hours` and `best_plan`. With 4-hour soaks, find the best plan among the test's four candidates for budgets of 0, 8 and 16 hours.
5. **Build your own candidates.** Generate every plan with 2 to 5 stages whose shares come from {0.5%, 1%, 2%, 5%, 10%, 25%, 50%, 100%}. For `N = 200,000`, `p = 1/2,000`, `d = 0.5` and 4-hour soaks, plot the lowest achievable expected harm against the time budget from 0 to 16 hours. Where does another stage stop being worth four hours?
6. **Robustness.** Take your best 8-hour plan from step 5 and compute its expected harm for `p` from 1 in 100,000 to 1 in 100. Compare it with the big bang in a table like the lecture's. Which bug rates does your plan handle worst?

### Part C: triage (25 min)

7. **Hotfix rule.** Implement `hotfix_decision` and run it on `bugs.csv`. The test checks the six decisions.
8. **Sensitivity.** For each bug, find the restart length in minutes at which the decision flips. Which bugs would flip if your hotfixes needed no restart at all?
9. **Beyond the formula.** Bug B5 is an active exploit. Say what the formula leaves out for it, and what you would do in the first ten minutes (week 13's revert-first logic and a kill switch).

## Deliverable

Your `rollout.py` with all tests passing, the chart from step 5, and a one-page rollout policy for a 200,000-player MMO. It must give default stage sizes and soak time with their expected harm at `d = 0.5`, the smallest bug rate the canary is meant to catch, a detection target, and the hotfix rule with its break-even harm rate under your restart time.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All eight tests pass; simulation is independent of the formula | Tests pass with shortcuts | Tests fail | 25% |
| Simulation insight | Median and 95th percentile reported, with a clear reason why the mean misleads | Numbers without interpretation | Missing | 15% |
| Planning | Full plan search, chart and robustness table correct; the point where stages stop paying is identified | Search partial or chart unclear | No search | 25% |
| Triage | Six decisions, flip points computed, exploit case reasoned beyond the formula | Decisions only | Decisions wrong | 15% |
| Policy | Every required number present, justified from the model, one page | Some numbers missing | Not actionable | 20% |
