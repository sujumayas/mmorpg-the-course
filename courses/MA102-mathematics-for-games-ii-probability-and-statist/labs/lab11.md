# MA102 · Lab 11: Monte Carlo lab

Assigned in week 11 ([lecture](../lectures/w11-monte-carlo-simulation.md)). Due at the start of week 13. This is the graded Monte Carlo lab, worth 20% of the course.

## Objective

Build a validated Monte Carlo simulation of a loot system with bad-luck protection, report every estimate with a margin of error, and answer design questions that have no convenient closed form.

## Starter materials

- `lab11_starter.ipynb` (on the course page). A Python 3 notebook with numpy and matplotlib, a helper `estimate(trial, n, seed)` that returns `p̂` (or `x̄`) with its 95% margin, and a stub `trial_raid(rng, config)` to fill in.
- `raid_config.json`. The loot rules for a fictional 10-player raid boss: two items drop per kill from a weighted table of 8 items (weights 20, 20, 15, 15, 10, 10, 5, 5), each player needs one specific item, a player who already has their item is removed from eligibility, and a personal pity counter guarantees a player's item after 12 kills without it.
- Your lab 07 and lab 10 code.
- The week 11 interactive, `examples/w11-monte-carlo-mulligan.html`, as a reference for convergence plots.

## Steps

1. **Validate on a known case (required before anything else).** Configure the raid as one player, one item with weight 1 out of a total of 20, one drop per kill and no pity. The chance of having the item within 10 kills is `1 − 0.95^10 ≈ 0.4013`. Run 1,000, 10,000 and 100,000 trials with seed 1111. Show a table of `p̂ ± margin` and confirm each interval covers 0.4013. Then turn on pity at 12 and confirm your simulated mean kills matches the exact `(1 − 0.95^12) / 0.05 ≈ 9.19`.
2. **Edge tests.** Run two cases where you know the answer without any math (for example, every item has the same weight and there are as many drops as players). Explain what each test protects against.
3. **Main simulation.** With the full `raid_config.json`, estimate:
   - the mean and median number of kills until all 10 players have their item;
   - the 90th percentile of that number;
   - the share of players whose item came from the pity counter.
   Report each with a 95% margin (for the median and percentile, run the whole simulation with 20 different seeds and report the spread).
4. **Precision budget.** Choose the number of trials so that the mean kills is known to within ±0.1. Show the calculation from a pilot run's SD.
5. **Design question.** The producer asks whether raising the pity from 12 to 16 kills saves enough rare-item value to be worth the extra frustration. Simulate both. Report the change in mean kills to full completion, the change in the 90th percentile, and the change in the share of pity-awarded items. Say whether the differences are larger than the margins.
6. **Break it on purpose.** Introduce one deliberate rules bug (for example, forget to remove satisfied players from eligibility). Report how much each statistic moves and whether your step 1 validation would have caught it. If not, write a new validation test that would.

## Deliverable

The notebook, plus a report of at most 800 words with:

- The validation table and edge tests (steps 1 and 2).
- The main results table with margins (step 3) and the precision calculation (step 4).
- A recommendation on pity 12 versus 16 with numbers (step 5).
- A short paragraph on model error versus sampling error, using your bug from step 6 as the example.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Validation | Known case reproduced at three sample sizes with intervals covering the exact value; pity mean matched; edge tests explained | Validation done at one size or edge tests unexplained | No validation | 25% |
| Simulation correctness | `trial_raid` follows every rule in the config, seeded and reproducible | One rule wrong or unseeded | Does not run or several rules wrong | 25% |
| Uncertainty reporting | Every estimate has a margin; percentile spread from multiple seeds; precision budget computed correctly | Margins on some estimates only | No margins | 20% |
| Design recommendation | Pity comparison uses margins to judge whether differences are real, recommendation follows from numbers | Comparison made without margins | Missing or unsupported | 20% |
| Report clarity | Under 800 words, tables first, clear distinction between model and sampling error | Understandable but long or vague on error | Hard to follow | 10% |
