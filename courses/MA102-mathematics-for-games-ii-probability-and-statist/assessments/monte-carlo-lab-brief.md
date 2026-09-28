# MA102 · Monte Carlo lab brief

**Weight:** 20% of the course grade.
**Work:** individual.
**Assigned:** week 11. **Due:** start of week 13.
**Lab handout:** [Lab 11, Monte Carlo lab](../labs/lab11.md). **Lecture:** [Week 11, Monte Carlo simulation](../lectures/w11-monte-carlo-simulation.md).

## The task

You build a Monte Carlo simulation of a raid boss's loot system with a personal pity counter, prove that it follows the rules before you trust it, report every estimate with a margin of error, and use it to answer a producer's question that has no convenient formula. The full rules are in [`raid_config.json`](../labs/lab11-starter/raid_config.json) and summarized in the lab handout: 10 players, 2 drops per kill from a weighted table of 8 items (weights 20, 20, 15, 15, 10, 10, 5, 5), one needed item per player, satisfied players removed from eligibility, and a guarantee on the 12th kill without the item.

This is the course's only graded simulation project. It tests the week 11 skills directly and draws on the weighted tables of week 9 and the pity counters of week 10.

## Deliverables

1. **Notebook or script** (`lab11-<name>.ipynb` or `lab11-<name>.py`, built on the [lab 11 starter](../labs/lab11-starter/README.md)), runnable top to bottom with the seeds given in the handout. A grader will run it from a fresh start. It must finish in under 10 minutes on a lab machine.
2. **Report** (`lab11-<name>.pdf`), at most 800 words plus tables. It contains, in this order:
   - The validation table and the two edge tests (lab steps 1 and 2).
   - The main results table with 95% margins, and the precision calculation (steps 3 and 4).
   - The pity 12 versus 16 comparison and a recommendation (step 5).
   - One paragraph on model error versus sampling error, using your deliberate bug (step 6).
3. **Honesty note**, three lines at the top of the report: which lab 07 and lab 10 code you reused, anyone you discussed methods with, and any part that does not run.

## Reference values the grader checks

These come from exact formulas. Your simulation must reproduce them within its own margin.

| Check | Exact value | Source |
|---|---|---|
| One player, weight 1 of 20, one drop per kill, no pity: P(item within 10 kills) | `1 − 0.95^10 = 0.4013` | week 3 complement rule |
| Same case with pity at 12: mean kills | `(1 − 0.95^12)/0.05 = 9.19` | week 10 hard pity |

A validation interval that misses its exact value is a bug until proven otherwise. Find it before you run step 3.

## Milestones

| When | Milestone | What you show | Consequence |
|---|---|---|---|
| Week 11 lab session | Validation checkpoint | `trial_raid` in the one-player configuration and a 1,000-trial table that covers 0.4013 | Required. Feedback on the spot. |
| End of week 12 | Pilot run posted | A 2,000-trial pilot of the full raid with the SD of kills-to-completion, and your planned trial count from the precision budget | Required. Missing it costs 5 points. |
| Start of week 13 | Submission | Notebook and report | Late rules below |

The pilot milestone exists because the most common failure in this lab is running a million trials of a simulation with a rules bug. A 2,000-trial pilot with an honest validation catches that in minutes.

## Rubric

100 points, matching the five criteria in the lab handout. Each criterion has point bands.

| Criterion | Points | Excellent | Adequate | Weak |
|---|---|---|---|---|
| Validation | 25 | **22 to 25.** Known case reproduced at 1,000, 10,000 and 100,000 trials, every interval covers 0.4013, pity mean matches 9.19 within its margin, both edge tests explained (what bug each would catch) | **13 to 21.** Validation at one or two sizes, or edge tests run but not explained | **0 to 12.** No validation, or an interval misses the exact value and the report does not notice |
| Simulation correctness | 25 | **22 to 25.** `trial_raid` follows every rule in the config (two drops, weights, removal of satisfied players, personal pity reset), seeded, reruns identically | **13 to 21.** One rule wrong or one seed missing, results otherwise sensible | **0 to 12.** Does not run, or several rules wrong |
| Uncertainty reporting | 20 | **18 to 20.** Every estimate has a 95% margin, median and 90th percentile reported as a spread over 20 seeds, precision budget computed from the pilot SD with `n = (1.96 × s / 0.1)²` | **10 to 17.** Margins on some estimates only, or the budget uses a guessed SD | **0 to 9.** Point estimates with no margins |
| Design recommendation | 20 | **18 to 20.** Pity 12 and 16 compared on mean, 90th percentile and pity share, each difference judged against the combined margins, recommendation follows from the numbers and names the cost | **10 to 17.** Comparison made, but differences not judged against margins, or the recommendation does not follow | **0 to 9.** Missing or unsupported |
| Report clarity | 10 | **9 to 10.** Under 800 words, tables first, model error and sampling error clearly separated using the step 6 bug | **5 to 8.** Understandable but long, or vague on the two kinds of error | **0 to 4.** Hard to follow |

## How the grader marks

1. Run the notebook or script from a fresh start. Any step that fails costs the dependent criterion its Excellent band.
2. Read `trial_raid` against the config, rule by rule.
3. Compare the validation table with the reference values.
4. Rerun step 5 with a different seed. Your conclusion should survive; the numbers should move by about your stated margins.

## Rules

- **Late work** loses 10 points per day, up to three days. The problem-set extension cannot be used here.
- **Seeds.** Use the seeds in the handout. Results that only appear with an undisclosed seed score as unreproducible.
- **Collaboration.** You may discuss methods and debugging strategies. Code and reports are your own.
- **Reuse.** Reusing your own lab 07 and lab 10 code is expected. Declare it in the honesty note.
