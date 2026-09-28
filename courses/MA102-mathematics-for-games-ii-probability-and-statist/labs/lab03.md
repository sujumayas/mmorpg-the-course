# MA102 · Lab 03: The drop-rate calculator

**Week:** 3 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 03, Complement rule: chance of at least one drop](../lectures/w03-complement-rule-chance-of-at-least-one-drop.md)

## Objective

Build a calculator that turns a drop rate into the waits players actually experience (median, mean, 95th and 99th percentile), check it against a large simulation, and use it to set drop rates for a boss from tail targets.

## Starter materials

- A spreadsheet, or Python 3 with the standard library.
- The producer brief below.

> **Producer brief: the Sunken Warden.** The Sunken Warden is a weekly-lockout boss. Each character can kill it once a week. It has three rare drops, rolled independently on each kill:
> - *Tidecaller's Band* (ring): 95% of characters who kill the boss every week should have it within 12 weeks.
> - *Drowned Standard* (cosmetic banner): half of weekly killers should have it within 26 weeks. We are fine with a long tail.
> - *Reins of the Leviathan* (mount): prestige item. No more than 20% of weekly killers should have it after one year (52 weeks). But we do not want more than 1 in 100 still dry after three years.
> The live game has 150,000 characters killing the Warden every week.

## Steps

1. **Calculator.** Build a sheet or script that takes `p` and returns `P(at least one in n)` for any `n`, and the waits for 50%, 95% and 99% using `ceil(ln(1 − q) / ln(1 − p))`, plus the mean `1/p`. Check it against the lecture's table for `p = 1/100` (69, 100, 299, 459) and `p = 1/512` (355, 512, 1,533, 2,356).
2. **Rules of thumb.** Add columns for `0.7/p`, `3/p` and `4.6/p`. For `p` from 0.1% to 20%, plot the relative error of each rule of thumb against the exact value. At what `p` does the 95% rule first err by more than 5%?
3. **Simulation check.** Simulate 100,000 players for `p = 1%`. For each, record the kill of their first drop. Compute the observed median, mean, 95th and 99th percentile, and compare with step 1. Report the differences.
4. **Solve the brief, ring and banner.** For each of the first two items, solve for `p` with `p = 1 − (1 − q)^(1/n)`. Report `p` as a percentage and as "1 in X".
5. **Solve the brief, mount.** The mount has two constraints. Write them as two inequalities on `p`. Find the range of `p` that satisfies both, or show that none does. If none does, propose the smallest change to the brief that makes it possible, and explain it in one sentence.
6. **Population numbers.** For each item and your chosen `p`, compute how many of the 150,000 characters are still dry after 12, 52 and 156 weeks.
7. **Different rates, one kill.** With your three rates, compute the chance that a single kill drops at least one of the three items.

## Deliverable

The calculator (sheet or script), a plot for step 2, the step-3 comparison table, and a one-page response to the producer with the three drop rates, the population table from step 6, and your step-5 argument.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Calculator correctness | Matches all eight check values; rounding up handled | One check value off by rounding | Several wrong | 25% |
| Rule-of-thumb analysis | Error plot correct, threshold `p` found and explained | Plot present, threshold missing | Missing | 15% |
| Simulation check | Observed percentiles within 1% of theory, differences discussed | Simulation run, discussion thin | Missing | 15% |
| Solving the brief | Ring and banner rates correct; mount constraints written as inequalities and resolved correctly | Rates correct, mount reasoning incomplete | Rates wrong | 30% |
| Communication | Response uses population numbers and names the trade-off for each item | Numbers present, trade-offs missing | No response to the producer | 15% |
