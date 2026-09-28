# MA102 · Lab 02: Streak detective

**Week:** 2 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 02, Independent events: the gambler's fallacy in loot](../lectures/w02-independent-events-and-the-gamblers-fallacy.md)

## Objective

Simulate three randomness systems that share the same long-run success rate, measure how their droughts differ, and use conditional probability to test a kill log for accidental dependence between two events.

## Starter materials

- Python 3 with the standard library (`random`, `collections`, `csv`), or a spreadsheet if you prefer. Plotting with any tool you like (spreadsheet chart, matplotlib if already installed, or a hand-drawn chart from printed numbers).
- Starter function signatures to implement:

```python
def independent(p, n, rng):   # list of n booleans, each True with chance p
def bag(N, n, rng):           # one winner per N tickets, refill when empty
def streak_bonus(p, b, n, rng):  # chance p + b*k after k failures, capped at 1
def longest_drought(history): # longest run of False
def next_after_k(histories, k):  # observed success rate right after exactly k failures
```

- A kill log, `kills.csv`, supplied by your instructor, with columns `kill, crit, gem` for 20,000 kills. It was produced by one of two versions of the hit handler. The correct version rolls `crit = r1 < 0.20` and `gem = r2 < 0.05` with separate random numbers. The buggy version reuses `r1` for both. You are not told which. Your job is to detect it. (Instructors: generate one log per lab group with a different seed and version, and keep the key.)

## Steps

1. **Implement the three systems.** Use a seeded `random.Random(seed)` so your results are reproducible. Test each with `p = 0.1` (bag of 10, streak bonus `b = 0.05`) over 1,000,000 attempts and confirm the long-run success rate. Record it. Note that the streak-bonus system will have a higher long-run rate than `p`; report by how much.
2. **Match the rates.** Adjust the streak-bonus base chance until its long-run rate is 10% within 0.1 percentage points. Record the base chance you found.
3. **Droughts.** Simulate 10,000 players with 200 attempts each under each system. Plot a histogram of each player's longest drought. Report the mean and maximum for each system, and compare the bag maximum with the theoretical `2N − 2`.
4. **The gambler's question.** For k = 0, 5, 10, 15, 20, compute the observed chance of success right after exactly k failures, for each system. Put the results in a table next to the theory from the lecture (`p` for independent, `1/(N − j)` for the bag, `p + b × k` for the streak bonus). Explain any row where observation and theory differ by more than 2 percentage points.
5. **Coin runs.** Simulate 100,000 sequences of 100 fair flips. Report the fraction that contains a run of at least 5, 6, 7 and 8 identical results. Compare with 97.2%, 80.7%, 54.2%, 31.5%.
6. **Detective work.** From `kills.csv`, compute `P(gem)`, `P(gem | crit)` and `P(gem | no crit)`. Decide whether the log came from the independent code or the buggy code, and justify it with the numbers.
7. **Recommendation.** A designer wants a 4% chance for a crafting "masterwork" and says players must never fail more than 60 times in a row. Choose a system and its parameters, and show from your simulation that it meets the rule while keeping the 4% long-run rate.

## Deliverable

A report of at most 4 pages (PDF or Markdown) with the drought histograms, the step-4 table, the step-5 comparison, your step-6 verdict with the three conditional probabilities, and the step-7 recommendation. Attach your code or spreadsheet.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correct simulations | All three systems correct and seeded; long-run rates reported; step 2 base chance found | One system has a small bug, noted | Systems wrong or unseeded with no rates | 25% |
| Drought analysis | Histograms labelled, means and maxima reported, bag maximum matches theory | Histograms present with incomplete numbers | Missing | 20% |
| Conditional probability table | Observed vs theory for all k, discrepancies explained | Table complete, no explanation | Missing or wrong conditioning | 20% |
| Dependence detection | Correct verdict supported by all three conditional probabilities | Correct verdict with partial evidence | Wrong or unsupported verdict | 20% |
| Design recommendation | Meets both constraints, shown with simulation output | Meets one constraint | No evidence | 15% |
