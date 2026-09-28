# MA102 · Lab 05: Swing and overkill

**Week:** 5 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 05, Variance and standard deviation: 'swingy' designs](../lectures/w05-variance-and-swingy-designs.md)

## Objective

Measure how much damage spread costs or gains a weapon near health thresholds. You will compute per-hit variance, the exact distribution of hits-to-kill across a range of enemy HP, and a plot that shows where a swingy weapon beats a steady one with the same average.

## Starter materials

- Your Lab 04 spreadsheet, or a new sheet or Python 3 script.
- The two weapons from the lecture: Steady Blade (20 per hit) and Gambler's Axe (16 per hit, 25% crit, ×2).
- A short list of enemy HP values from a real zone design, given below.

> **Zone brief: the Ember Flats.** Enemy health values: rat 32, scout 60, raider 96, brute 112, champion 180, elite 300. The design goal is that no single-target weapon kills any common enemy (rat to brute) more than 10% slower on average than any other weapon with the same expected DPS.

## Steps

1. **Per-hit spread.** For both weapons compute mean, variance, standard deviation and coefficient of variation per hit, using both `Σ (x − μ)² P(x)` and `E[X²] − μ²`. Check: Axe variance 48, SD 6.93, CV 0.346.
2. **Hits-to-kill, by hand.** For the Axe against 100 HP, reproduce the lecture's table: P(T = 4) = 0.0508, P(T = 5) = 0.3164, P(T = 6) = 0.4548, P(T = 7) = 0.1780, E[T] = 5.76.
3. **Hits-to-kill, general.** Build a sheet or function that returns `P(T = n)` for any HP `H`, base `b`, crit chance `c` and multiplier `m`. Use `P(T ≤ n) = Σ over k of C(n, k) c^k (1 − c)^(n − k) × [b(n + k(m − 1)) ≥ H]`. Check against the lecture: H = 32 gives E[T] = 1.75; H = 96 gives E[T] = 4.96; H = 112 gives E[T] = 5.76.
4. **Sweep.** Compute E[T] for both weapons for every HP from 20 to 200. Plot both on one chart (the Blade is a staircase). Shade or list the HP values where the Axe kills faster.
5. **The zone brief.** For each Ember Flats enemy, report both weapons' E[T] and the percentage difference. Which enemies violate the design goal?
6. **Fix it two ways.** Propose (a) one change to the Axe's crit chance and multiplier that keeps the mean at 20 and brings every common enemy within 10%, and (b) one change to enemy HP values instead. Recompute and show both fixes work. Use the lecture's "same mean, different spread" table to guide (a).
7. **Long fights.** For the elite (300 HP), compute the CV of total damage after the expected number of hits for both weapons. Explain in two sentences why the elite does not violate the goal while the raider might.

## Deliverable

The sheet or script, the step-4 chart, a step-5 table, and a 250-word note to the zone designer recommending fix (a) or fix (b), with the numbers that justify it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Per-hit statistics | Both methods, all four statistics correct for both weapons | One statistic wrong or one method missing | Several wrong | 15% |
| Hits-to-kill model | General model matches all four check values | Matches the 100-HP case only | Does not match | 30% |
| Sweep chart | Both curves correct, crossing regions identified | Chart correct, regions not identified | Missing or wrong | 20% |
| Brief and fixes | Violations identified; both fixes verified numerically | One fix verified | No verified fix | 20% |
| Note | Recommends one fix with numbers and names its cost | Recommendation without numbers | Missing | 15% |
