# MA102 · Lab 06: Crit simulator versus the binomial

**Week:** 6 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 06, Binomial distribution: crits over a fight](../lectures/w06-binomial-crits-over-a-fight.md)

## Objective

Simulate thousands of fights, check the results against the binomial formula, and measure how the spread of the observed crit rate depends on fight length. Then use the binomial to answer a live-ops question about player complaints. The simulation code you write here is the starting point for the Monte Carlo lab in week 11.

## Starter materials

- Python 3 with the standard library (`random`, `math`), or a spreadsheet with `RAND()` and `BINOM.DIST` (Excel, LibreOffice) or `BINOMDIST` (Google Sheets).
- A fixed random seed: use `random.seed(6)` in Python so results can be reproduced and graded.
- The complaint log summary below.

> **Live-ops note: the Duelist class.** The Duelist has a 25% crit chance on every attack. A typical arena duel lasts 6 Duelist attacks; a typical dungeon boss lasts 120. Last week, 40,000 arena duels and 5,000 boss fights were logged. The forum has a thread titled "Crits are broken in arena" with 312 replies. The community manager asks: is something wrong, or is this how 25% behaves?

## Steps

1. **Formula table.** Write a function `binom_pmf(n, k, p)` using `math.comb`. For the lecture's champion (n = 8, p = 0.10) print P(K = 0) through P(K = 4). Check: 0.4305, 0.3826, 0.1488, 0.0331, 0.0046.
2. **Simulate one fight.** Write `simulate_fight(n, p)` that rolls `n` independent attacks and returns the crit count.
3. **Simulate many.** Run 10,000 fights for the champion. Tabulate the proportion of fights with 0, 1, 2, 3 and 4 or more crits. Put the simulated and formula values side by side with the difference.
4. **How big should the differences be?** A simulated proportion over 10,000 fights has standard deviation `√(P(1 − P) / 10,000)`, where `P` is the true probability. Compute this for each row of step 3. Are all your differences within two of these standard deviations? Report any that are not.
5. **Rate spread versus fight length.** For p = 0.25 and n in {6, 12, 25, 50, 120, 250}, simulate 5,000 fights each and record the observed crit rate `k / n` of each fight. Report the standard deviation of the observed rates and compare with `√(p(1 − p) / n)`. Plot both against `n` on one chart.
6. **The Duelist.** Using the formula (not simulation), compute for the arena (n = 6) and the boss (n = 120): P(no crits), P(observed rate ≥ 50%), and P(observed rate ≤ 10%). Multiply each by the logged number of fights to get expected counts per week.
7. **Break it on purpose.** Modify `simulate_fight` so the crit chance rises by 0.05 after every non-crit and resets to 0.10 after a crit. Simulate 10,000 six-attack fights. Report the mean crit count and P(no crits), and compare them with the binomial's. You have built a crude pseudo-random system; week 10 shows how to tune it so the mean matches exactly.

## Deliverable

Your script or sheet, the step-3 comparison table with the step-4 check, the step-5 chart, and a 300-word reply to the community manager using the step-6 counts. The reply must say how many arena duels last week should have had zero Duelist crits, whether 312 replies is consistent with that, and one design option if the team wants fewer dry duels, citing your step-7 result.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Formula and simulation | PMF matches check values; simulation seeded and reproducible | Minor mismatch or seed missing | Formula or simulation wrong | 25% |
| Agreement check | Every row compared with the correct standard deviation, outliers discussed | Comparison present, standard deviation missing | Missing | 15% |
| Rate spread study | Simulated SDs within 10% of theory at every n, chart labeled | Chart present, one n off or unlabeled | Missing | 20% |
| Duelist analysis | All six probabilities and weekly counts correct | One or two wrong | Several wrong | 20% |
| Reply and step 7 | Uses counts, answers the question directly, proposes one option backed by the step-7 numbers | Answers without counts or without step 7 | Missing | 20% |
