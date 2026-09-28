<!-- generated-stub: safe to overwrite -->
# MA102 — Mathematics for Games II: Probability and Statistics

Year 1, semester 2 · 4 credits · Prerequisites: MA101

Loot, crits, drop rates, matchmaking and A/B tests all run on probability. This course makes randomness designable.

## Learning outcomes

- Compute probabilities of compound events (drops, crits, combos)
- Use expected value and variance to compare designs
- Model 'until success' processes with the geometric distribution
- Design pseudo-random and pity systems with controlled variance
- Read basic statistics from playtest data

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Probability basics: sample spaces and events | [lecture](lectures/w01-sample-spaces-and-events.md) | [advantage-grid](examples/w01-advantage-grid.html) |
| 2 | Independent events: the gambler's fallacy in loot | [lecture](lectures/w02-independent-events-and-the-gamblers-fallacy.md) | [dry-streaks](examples/w02-dry-streaks.html) |
| 3 | Complement rule: chance of at least one drop | [lecture](lectures/w03-complement-rule-chance-of-at-least-one-drop.md) | [drop-curve](examples/w03-drop-curve.html) |
| 4 | Expected value: comparing weapons | [lecture](lectures/w04-expected-value-comparing-weapons.md) | [expected-dps](examples/w04-expected-dps.html) |
| 5 | Variance and standard deviation: 'swingy' designs | [lecture](lectures/w05-variance-and-swingy-designs.md) | [swing-meter](examples/w05-swing-meter.html) |
| 6 | Binomial distribution: crits over a fight | [lecture](lectures/w06-binomial-crits-over-a-fight.md) | [crit-binomial](examples/w06-crit-binomial.html) |
| 7 | Geometric distribution: kills until the drop | [lecture](lectures/w07-geometric-distribution-kills-until-the-drop.md) | [kills-until-drop](examples/w07-kills-until-drop.html) |
| 8 | Dice sums and the normal curve (2d6 vs 1d12) | [lecture](lectures/w08-dice-sums-and-the-normal-curve.md) | [dice-shapes](examples/w08-dice-shapes.html) |
| 9 | Weighted tables and loot table design | [lecture](lectures/w09-weighted-tables-and-loot-table-design.md) | [loot-weights](examples/w09-loot-weights.html) |
| 10 | Pseudo-random distribution and pity timers | [lecture](lectures/w10-pseudo-random-distribution-and-pity-timers.md) | [gacha-pity](examples/w10-gacha-pity.html) · [prd-streaks](examples/w10-prd-streaks.html) |
| 11 | Monte Carlo simulation | [lecture](lectures/w11-monte-carlo-simulation.md) | [monte-carlo-mulligan](examples/w11-monte-carlo-mulligan.html) |
| 12 | Descriptive statistics for playtests | [lecture](lectures/w12-descriptive-statistics-for-playtests.md) | [playtest-spread](examples/w12-playtest-spread.html) |
| 13 | Sampling, confidence and why n=5 lies | [lecture](lectures/w13-sampling-confidence-and-why-n5-lies.md) | [sampling-intervals](examples/w13-sampling-intervals.html) |
| 14 | Intro to hypothesis testing (A/B) | [lecture](lectures/w14-intro-to-hypothesis-testing-ab.md) | [ab-test-simulator](examples/w14-ab-test-simulator.html) |
| 15 | Final exam + loot system design | [assessments](#assessment-materials) | — |

## Signature worked examples

- 1% drop rate: after 100 kills only ~63% of players have it — and 1 in 20 still lacks it after ~300 kills
- Dota 2 pseudo-random distribution: same average crit rate, far lower streakiness (verify C constants)
- Gacha pity: soft/hard pity changes the expected pulls (Genshin hard pity at 90; verify soft-pity rates)
- 2d6 vs 1d12: same range, completely different feel

## Readings

- Schreiber — Game Balance Concepts (blog course), levels 4-5
- Schreiber & Romero — Game Balance (2021), ch. on probability

## Assessment

Problem sets (35%), Monte Carlo lab (20%), loot design (20%), final (25%)
