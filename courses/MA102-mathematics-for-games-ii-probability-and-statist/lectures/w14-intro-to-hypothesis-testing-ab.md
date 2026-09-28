# MA102 · Week 14 — Intro to hypothesis testing (A/B)

**Why this matters:** Sooner or later someone on your team will say "the new version is better, look at the numbers." Sometimes it is. Often the numbers are noise, and a studio that ships noise as insight spends months tuning in circles. This week you learn the test that separates a real improvement from a lucky week.

**You will be able to:**
- Compute a two-proportion z-test and a p-value for an A/B test on a rate such as tutorial completion or purchase conversion.
- Explain what a p-value, a significance level and a false positive are, and predict how often an A/A test "wins".
- Calculate the sample size an A/B test needs to detect a given effect with 80% power.
- Critique an experiment design for missing controls, multiple comparisons, peeking and player interference.

**Before class:** OpenIntro Statistics (4th ed.), section 5.3 (hypothesis testing) and section 6.2 (difference of two proportions); Kohavi, R. & Thomke, S. (2017), "The Surprising Power of Online Experiments," *Harvard Business Review*.

**Prerequisites from earlier courses:** MA102 week 13, [Sampling, confidence and why n=5 lies](w13-sampling-confidence-and-why-n5-lies.md), and week 8, [Dice sums and the normal curve](w08-dice-sums-and-the-normal-curve.md). Week 3 (complement rule) is listed in the [MA102 syllabus](../syllabus.md). Solving for a variable under a square root, from the [MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md).

**Interactive:** [A/B test simulator](../examples/w14-ab-test-simulator.html) (built from the spec at the end of this lecture). Keep it open during sections 2 and 4.

---

## 1. From "how sure is this number?" to "is B better than A?"

Last week you put an error bar on one rate. This week you compare two. The questions designers actually ask are comparisons. Does the new tutorial keep more players? Does the redesigned shop sell more? Does the nerfed boss get cleared more often?

The tool for these questions is the **A/B test**, also called a controlled experiment. Its parts:

- The **control** (A) is the current version.
- The **variant** or **treatment** (B) is the change you want to evaluate.
- The **metric** is the number you judge them by, decided before the test starts. This week we stick to rates: completion, conversion, retention on day 1.
- **Random assignment** means each player is put in A or B by a coin flip the player cannot influence.

Random assignment is what makes an A/B test different from "we changed it and numbers went up." If you change the tutorial on Monday and completion rises on Tuesday, the rise might come from the change, or from a weekend influx of new players, or a streamer who sent you an audience, or a server outage last week that dragged the baseline down. When the coin decides who gets which version, all those other causes hit A and B equally. The only systematic difference left between the groups is your change. Any remaining difference is either your effect or chance.

This week's math answers one question. **Is the difference between A and B bigger than chance alone would usually produce?**

## 2. Worked example: did the change really work?

### The hook: the discount that cost sales

Before SimCity launched in March 2013, EA's Maxis team tested its pre-order web page using the Optimizely platform. The original page showed a large promotional banner offering a discount on a future purchase to anyone who pre-ordered. Everyone expected the offer to help. The team tested variants that placed and styled the offer differently, plus one with no offer at all.

The version with no offer produced 43.4% more purchases. The banner had pushed the buy button down the page, and removing it did more than any discount. The team's shared intuition was wrong, and only a randomized comparison could show it.

Now turn that around. Suppose your own shop test shows a 10% lift. Is that real, or did B get a luckier batch of visitors? The SimCity case study reports the lift but not the visitor counts, so as published you cannot check it. By the end of this section you will know what you would need to check.

### The model

A/B test on a rate. Group A has `n_A` players and `k_A` successes. Group B has `n_B` and `k_B`.

```
p̂_A = k_A / n_A        p̂_B = k_B / n_B        (observed rates)
p̂   = (k_A + k_B) / (n_A + n_B)                (pooled rate)
SE  = sqrt( p̂ (1 − p̂) × (1/n_A + 1/n_B) )      (standard error of the difference)
z   = (p̂_B − p̂_A) / SE                          (test statistic)
```

Decision rule at the usual 5% significance level: if `|z| > 1.96`, call the difference **statistically significant**.

What each piece means:

- The **null hypothesis** `H₀` is the boring explanation: A and B have the same true rate, and any observed difference is chance. The **alternative** `H₁` is that the true rates differ.
- The **pooled rate** `p̂` is our best estimate of the shared rate if `H₀` is true. We pool because the test asks "how would the difference behave if there were no real effect?"
- `SE` is how much the difference `p̂_B − p̂_A` typically wobbles under `H₀`. It is last week's standard error, applied to two groups. Variances add, so both `1/n` terms appear.
- `z` measures the observed difference in units of that wobble. A `z` of 2 means "the gap is twice the size chance usually makes".
- The **p-value** is the probability, if `H₀` were true, of seeing a gap at least this large in either direction. For a z-test, `p = 2 × (1 − Φ(|z|))`, where `Φ` is the normal curve's cumulative probability from week 8.
- The **significance level** `α` (alpha) is the false-alarm rate you accept, chosen in advance. `α = 0.05` gives the 1.96 threshold.

### Numbers you can check

Your studio tests a new tutorial. The old one has a 40% completion rate. The new one is truly better, at 44%. Here is what the test reports at different sizes, each time with observed rates landing exactly on 40% and 44%:

| Players per group | A completes | B completes | SE | `z` | p-value | Verdict at α = 0.05 |
|---|---|---|---|---|---|---|
| 10 | 4 (40%) | 6 (60%)* | 0.2236 | 0.89 | 0.37 | Not significant |
| 100 | 40 | 44 | 0.0698 | 0.57 | 0.57 | Not significant |
| 1,000 | 400 | 440 | 0.0221 | 1.81 | 0.070 | Not significant |
| 2,000 | 800 | 880 | 0.0156 | 2.56 | 0.010 | Significant |
| 10,000 | 4,000 | 4,400 | 0.0070 | 5.73 | < 0.0001 | Significant |

\* With 10 players, 44% is impossible to observe, so the row shows a typical playtest outcome, 4 versus 6. The observed gap there is 20 points, five times the true gap, and it is still nowhere near significant.

Check the 1,000 row by hand. Pooled `p̂ = 840/2000 = 0.42`. `0.42 × 0.58 = 0.2436`. `1/1000 + 1/1000 = 0.002`. `SE = sqrt(0.2436 × 0.002) = sqrt(0.000487) = 0.0221`. `z = 0.04 / 0.0221 = 1.81`. That is below 1.96, so not significant, even though the effect is real.

Read the table as one story. **The effect never changed. Only the sample did.** "Not significant" does not mean "no effect". It means "this test could not tell". The 10-player playtest, the kind a small team runs, has no chance of detecting a 4-point improvement. Its verdict is decided by luck.

### A visual you can move

Open `examples/w14-ab-test-simulator.html`. It runs 1,000 simulated A/B tests at once.

The left view is the **null world**. Set the true lift to 0 (A and B identical, an **A/A test**). The histogram of `z` values is a bell centered on zero, and the shaded tails beyond ±1.96 hold about 5% of the tests. Those tests "found" an improvement that does not exist. Run it again. It is always about 50 in 1,000. That is what `α = 0.05` means.

The right view is the **power curve**, the chance the test detects a real effect, plotted against players per group. Set the true lift to 4 points on a 40% baseline and slide `n` from 100 to 5,000. At 1,000 per group the marker sits at about 44%. Most tests of a genuinely better tutorial come back "not significant". The curve crosses 80% near 2,400 per group.

The two views together carry the lesson. A test that is too small does not protect you from false wins (those stay at 5%), but it hides most of the true ones.

### Cross-game recognition

Rewrite each case as "two rates, two sample sizes, compute `z`".

**SimCity pre-order page (EA/Maxis, 2013).** Two conversion rates, `k_A/n_A` visitors who bought with the banner and `k_B/n_B` without it. The published 43.4% is a relative lift, `(p̂_B − p̂_A) / p̂_A`. To judge it you need the visitor counts, which the case study does not give. It does say the team sent all site traffic into the test to get answers fast. That is the right instinct. At the high traffic of a major launch, even a 5% relative lift on a small conversion rate becomes detectable.

**League of Legends cross-team chat (Riot Games).** Riot's player-behavior lead, Jeffrey Lin, described switching cross-team "/all" chat from on by default to opt-in. Over the following two weeks Riot reported negative chat down 32.7% and positive chat up 34.5%, while the share of games with any cross-team chat barely moved (about 54% to 53%). As described, this was a before-and-after comparison across the whole game, not a randomized split. Put it in the A/B frame and a question appears. Was anything else different in those two weeks? A before-and-after design cannot rule out patches, events or seasonal change. With League's volume, `n` is not the problem, since millions of games make the random error tiny. The design is the risk. A randomized split would have removed it. Note the contrast. SimCity had the control group and did not publish `n`. Riot had huge `n` and, as described, no control group. A trustworthy result needs both.

**Web search (Bing).** Kohavi and Thomke describe a small change to how Bing displayed ad headlines. The idea sat in a backlog for months until an engineer ran an A/B test. It raised revenue by 12%, which they report was worth over $100 million a year in the US. It is the same test on the same kind of rate (clicks per visit), at a scale where a lift of a fraction of a percent is detectable. Kohavi's wider point matches the SimCity story. Experienced teams are poor at predicting which ideas will win, which is why they test.

One idea underneath all three. Compare two rates, measure the gap in units of its standard error, and only trust the gap if randomization made the groups comparable.

### Eyes-open design judgment

The z-test is simple. Designing an experiment worth running is not. Decide these deliberately.

- **Pick the metric and the threshold before you look.** If you choose after seeing the data, you will find a metric that "won". Write down the metric, `α`, and `n` in the test plan.
- **Size the test for the effect you care about.** If a 1-point lift in retention is worth shipping, you need a test that can see 1 point. If you can only afford a small test, admit it will only catch large effects.
- **"Not significant" is not "no effect".** At low power, a null result is a shrug. Report the confidence interval for the difference alongside the verdict. For the 1,000-player row, the 95% interval for the lift is −0.3 to +8.3 points. The effect may be nothing, or it may be large.
- **Randomization is what earns causality.** If you cannot randomize (a whole-server economy change, a global chat change), you are doing a before-and-after study. It can still be useful, but say so, and look for other explanations.
- **Practical significance is a separate call.** With 10 million players, a 0.1-point change can be highly significant and not worth the maintenance cost. Statistics tells you an effect is real. Design judgment tells you if it matters.

### Check yourself (worked example)

1. Store test: A converts 150 of 5,000 visitors, B converts 190 of 5,000. Compute `z`. Is it significant at α = 0.05? What is the relative lift?
2. Your 20-player playtest has 7 of 10 completing the new tutorial and 5 of 10 the old one. A teammate says "40% relative improvement, ship it". Respond with a number.

<details>
<summary>Answers</summary>

1. Pooled `p̂ = 340/10000 = 0.034`. `SE = sqrt(0.034 × 0.966 × 0.0004) = sqrt(0.00001314) = 0.003625`. Gap `0.038 − 0.030 = 0.008`. `z = 0.008 / 0.003625 = 2.21`, above 1.96, so significant (p ≈ 0.027). Relative lift `0.008 / 0.030 = 26.7%`.
2. Pooled `p̂ = 0.6`. `SE = sqrt(0.6 × 0.4 × 0.2) = 0.219`. Gap 0.2, so `z = 0.91`, p ≈ 0.36. A gap this large happens by chance more than a third of the time with no real effect. The playtest cannot distinguish the tutorials. Use it to find problems, then run a real test.

</details>

## 3. False positives, false negatives, and what a p-value is not

Every test can go wrong in two ways.

| | Truly no effect | Truly an effect |
|---|---|---|
| Test says significant | **False positive** (Type I error), rate `α` | Correct detection, rate = **power** |
| Test says not significant | Correct | **False negative** (Type II error), rate `1 − power` |

You choose `α` directly. You control power only through sample size, the size of the effect, and the noise of the metric.

**What a p-value means.** "If the variants were truly identical, a gap at least this large would appear with probability p." A p-value of 0.03 says the data would be surprising under `H₀`.

**What a p-value does not mean.** It is not the probability that B is no better. It is not the probability the result will replicate. It is not the size of the effect. A p-value of 0.001 on a 0.1-point lift and a p-value of 0.04 on a 10-point lift tell you different things, and the second may matter much more.

**The A/A test.** Before trusting an experiment system, split players into two groups that get the identical game and run a "test". About 5% of A/A tests should come out significant at `α = 0.05`. If your system reports far more, something is broken, for example uneven assignment or players counted in both groups. Large experimentation teams run A/A tests routinely for exactly this reason.

### Multiple comparisons

Suppose you test one change and measure 20 metrics: day-1 retention, day-7 retention, session length, purchases, chat messages, and so on. Even if the change does nothing, each metric has a 5% false-positive chance. The chance at least one "wins" is the complement rule from week 3:

```
P(at least one false positive in 20) = 1 − 0.95^20 ≈ 0.64
```

Nearly two in three useless changes will produce a headline. The same happens when you test 10 variants against one control (`1 − 0.95^10 ≈ 0.40`). The fixes are to pick one primary metric in advance, or to demand a stricter threshold per comparison. The simplest stricter threshold is the **Bonferroni correction**, which divides `α` by the number of comparisons, so 20 metrics each need `p < 0.0025`.

## 4. Power and sample size

The **power** of a test is the probability it detects an effect of a given size. The convention is to design for 80% power at `α = 0.05`. The sample size per group for comparing two rates is:

```
n per group = (z_α + z_β)² × ( p_A(1 − p_A) + p_B(1 − p_B) ) / d²

z_α = 1.96 (two-sided, α = 0.05)     z_β = 0.84 (80% power)     d = p_B − p_A
```

`(1.96 + 0.84)² ≈ 7.85`. A quick version, often called **Lehr's rule**, is `n ≈ 16 × p(1 − p) / d²` per group, with `p` the baseline rate.

For the tutorial example (baseline 40%):

| True lift `d` | `n` per group (exact formula) | Lehr's rule |
|---|---|---|
| 10 points (40% → 50%) | 385 | 384 |
| 4 points (40% → 44%) | 2,387 | 2,400 |
| 2 points (40% → 42%) | 9,490 | 9,600 |

The `d²` in the denominator makes small effects expensive. Halving the effect you want to detect multiplies the test size by four, the same square-root law as last week.

And power at a fixed size, for the 4-point lift:

| `n` per group | 100 | 500 | 1,000 | 2,000 | 2,400 | 5,000 |
|---|---|---|---|---|---|---|
| Power | 8.8% | 25.0% | 44.2% | 72.7% | 80.2% | 98.2% |

This is what the right view of the interactive draws. An underpowered test is a coin flip you paid for.

For a small studio this has a hard consequence. If your game has 300 new players a week, a test that needs 2,400 per group takes 16 weeks. You will either test only large changes, accept lower power, or pick a metric with more signal. That is a design decision, and it should be made on purpose.

### Peeking

A tempting habit is to watch the dashboard and stop the test the first day `|z|` crosses 1.96. Each look is another chance for noise to cross the line, so the real false-positive rate climbs well above 5%. Fix the sample size in advance and look once, or use methods built for repeated looks. The live-ops course MMO308 (week 6, "A/B testing: statistics and pitfalls", see the [MMO308 syllabus](../../MMO308-live-operations-analytics-and-experimentation/syllabus.md)) builds a simulation of exactly this problem.

## 5. What makes A/B testing hard in an MMO

The z-test assumes each player's outcome is independent of which group other players are in. In single-player games and web shops, that is roughly true. Online worlds break it in ways you should expect.

- **Interference between players.** If group B gets a cheaper crafting recipe and sells on the same auction house as group A, B's change moves A's prices. Players in the same guild or party share outcomes. Randomize by server, guild or region when players interact, and accept that you now have fewer, larger units, so your effective `n` is the number of servers, not players.
- **Fairness and visibility.** Players compare notes. A visible difference in price or power between groups becomes a forum thread within hours. Some tests (drop rates, competitive balance) may be unethical or unacceptable to run on paying players. Test on things players do not compete over, or test on a public test server and say so.
- **Novelty and learning.** A new UI often gets a short burst of clicks because it is new, then fades. Run long enough to see the lasting effect, which usually means at least a full week to cover weekday and weekend players.
- **Wrong unit of analysis.** If you randomize by player but count sessions, a few heavy players dominate one group. Count at the level you randomized.

## In-class activity (25 minutes)

Materials: one coin per pair, the shared class spreadsheet, the interactive on the projector.

1. **A/A test by hand (10 min).** Each pair flips a coin 30 times for "version A" and 30 times for "version B". Heads is a "completion". Both versions are the same coin, so there is no real effect. Compute `z` for B versus A. Enter it in the sheet.
2. **Count false wins (5 min).** The instructor plots all pairs' `z` values as a dot plot with lines at ±1.96. With about 20 pairs, expect roughly one false win. Did the class get about that many?
3. **Plan a real test (10 min).** Your game's day-1 retention is 35%. The team wants to know if a new onboarding flow raises it to 38%. Using the power formula, compute `n` per group. If you get 400 new players per day, how many days does the test take? Propose one change to the plan that shortens it, and state its cost.

Expected output: a class dot plot with about 5% of `z` values beyond ±1.96, and for step 3 about 4,040 players per group (Lehr's rule with `p = 0.35`, `d = 0.03`), so about 8,080 players in total, or about 20 days at 400 new players per day.

## Common misconceptions

- **"p = 0.03 means a 97% chance B is better."** The p-value is computed assuming no effect. It tells you how surprising the data are under that assumption, not the probability of a hypothesis.
- **"Not significant means the change does nothing."** It often means the test was too small. Check power, and report the interval for the difference.
- **"Significant means important."** With enough players, a trivial difference becomes significant. Look at the effect size and ask if it is worth shipping.
- **"We saw it go up after the patch, so the patch did it."** Without a randomized control, anything that changed at the same time is a rival explanation.

## Check yourself

1. An A/B test of a new daily-login reward shows day-7 retention of 20.0% (A, 3,000 players) and 21.5% (B, 3,000 players). Compute `z` and state the verdict at α = 0.05.
2. A producer runs one test with 15 metrics and celebrates that "match length" improved with p = 0.04. What is the chance at least one of 15 metrics comes out significant when nothing changed? What threshold would Bonferroni require?
3. Your baseline purchase rate is 5%. You want 80% power to detect a rise to 6%. Estimate `n` per group with Lehr's rule. With 2,000 visitors a day, how long is the test?
4. A designer proposes testing a 20% cheaper potion in half of the players on each server of your MMO. Name two problems and one better design.

<details>
<summary>Answers</summary>

1. Pooled `p̂ = 0.2075`. `SE = sqrt(0.2075 × 0.7925 × (2/3000)) = sqrt(0.0001096) = 0.01047`. `z = 0.015 / 0.01047 = 1.43`. Not significant (p ≈ 0.15). The lift may be real, but this test cannot tell.
2. `1 − 0.95^15 ≈ 0.54`. More likely than not. Bonferroni requires `p < 0.05/15 ≈ 0.0033`, so p = 0.04 does not pass.
3. `n ≈ 16 × 0.05 × 0.95 / 0.01² = 7,600` per group, 15,200 total, so about 7.6 days. Run a full 8 days, or better 14, to cover two weekly cycles.
4. Players in both groups share each server's market, so cheap potions from B leak into A (interference), and players will notice the price difference and complain (fairness). Better: randomize whole servers, or test on a public test realm, and accept a smaller effective `n`.

</details>

## Lab / assignment hook

**Lab 14: Analyze an A/B test, and design one** ([labs/lab14.md](../labs/lab14.md)). You analyze a simulated tutorial experiment, run 1,000 A/A tests to confirm the 5% false-positive rate, and write a one-page test plan with metric, `α`, power and duration for a change to your loot-design project. The plan feeds the final loot-system design assessment.

## Sources

- Optimizely customer case study, "Electronic Arts optimizes SimCity game launch for pre-order revenue", and TechCrunch, "Optimizely Explains How It Boosted SimCity Pre-Order Revenue" (14 June 2013). SimCity (2013) pre-order page test, the no-offer variant with 43.4% more purchases, traffic sent to the test. No visitor counts or significance figures are published.
- Lin, J. (2015). "The first online player behavior experiment at Riot Games." LinkedIn article, 20 April 2015. League of Legends cross-team chat made opt-in; over two weeks negative chat down 32.7%, neutral down 1.9%, positive up 34.5%, games with cross-team chat about 54% to 53%. Described by Lin as Riot's first player-behavior experiment; the article does not give the exact date of the test. Riot later removed cross-team chat entirely (patch 11.21, 2021), reported by PC Gamer.
- Kohavi, R. & Thomke, S. (2017). "The Surprising Power of Online Experiments." *Harvard Business Review*, September-October 2017. Bing headline test, 12% revenue increase, reported worth over $100 million a year.
- Kohavi, R., Tang, D. & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*. Cambridge University Press. A/A tests, peeking, interference.
- van Belle, G. (2008). *Statistical Rules of Thumb*, 2nd ed. Wiley. Lehr's `16/Δ²` sample-size rule.
- Diez, D., Çetinkaya-Rundel, M. & Barr, C. (2019). *OpenIntro Statistics*, 4th ed., sections 5.3 and 6.2.
- All test statistics, p-values and power values in this lecture were computed by the author from the formulas given.

## Interactive spec: examples/w14-ab-test-simulator.html

**The one insight.** Tests that are too small keep false wins at 5% but miss most real improvements. With the lift at zero, the student sees about 5% of tests "win" anyway. With a real 4-point lift at 1,000 players per group, the student sees that most tests still come back "not significant".

**Layout.** Two linked views side by side on desktop, stacked on mobile.

- **Left view, "1,000 experiments".** Histogram of the `z` statistic from 1,000 simulated A/B tests at the current settings. Bins of width 0.25 from −5 to +8 (clamp the rest into the end bins and label them). Vertical lines at −1.96 and +1.96; bars beyond them in the accent color. Overlay the standard normal curve (null distribution) as a thin line, scaled to the histogram. Header: "Significant: X of 1,000". When lift = 0, add the subtitle "every one of these is a false positive".
- **Right view, "Power vs players per group".** x axis: `n` per group, log scale 10 to 20,000. y axis: power 0% to 100%, dashed guide at 80%. Plot the analytic power curve for the current baseline and lift. A marker at the current `n` shows the analytic power, and a second hollow marker shows the simulated fraction significant from the left view. When lift = 0, the curve is flat at 5%.
- **Readout row** under both views with exact numbers: baseline `p_A`, true `p_B`, `n` per group, SE under `H₀` (pooled, using the true rates), analytic power, simulated significant fraction, and the `n` per group needed for 80% power.
- **One-test panel** (collapsible, open by default on desktop): shows the first simulated experiment in full, `k_A of n`, `k_B of n`, pooled rate, SE, `z`, p-value and verdict, so students can check the arithmetic.

**Controls (all keyboard accessible, update immediately).**
- Baseline rate `p_A`: slider 1% to 90%, step 1%, default 40%.
- True lift `d` in percentage points: slider −10 to +15, step 0.5, default +4.
- Players per group `n`: stepped slider over [10, 20, 50, 100, 200, 500, 1000, 2000, 2400, 5000, 10000, 20000], default 1000.
- `α`: toggle 0.05 / 0.01 (thresholds 1.96 / 2.576), default 0.05.
- Button "Run 1,000 new experiments". Checkbox "Fixed seed" (default on, seeded PRNG such as mulberry32 with seed 14).
- Presets: "A/A test" (d = 0), "Playtest" (n = 10), "Tutorial test" (p_A = 40%, d = 4, n = 1000), "Well powered" (same, n = 2400).

**Formulas.**
- Simulate `k_A ~ Binomial(n, p_A)`, `k_B ~ Binomial(n, p_A + d)`. For `n ≤ 1000`, sum uniform draws. For larger `n`, a normal approximation to the binomial with continuity correction is acceptable; state this in a footnote.
- Pooled `p̂ = (k_A + k_B) / 2n`, `SE = sqrt(p̂(1 − p̂) × 2/n)`, `z = (k_B/n − k_A/n) / SE`. If `SE = 0` (both groups all 0 or all 1), set `z = 0`.
- p-value `= 2 × (1 − Φ(|z|))`, with Φ from a standard erf approximation (Abramowitz-Stegun 7.1.26 is fine).
- Analytic power: `SE₁ = sqrt(p_A(1 − p_A)/n + p_B(1 − p_B)/n)`, `power = Φ(d/SE₁ − z_α) + Φ(−d/SE₁ − z_α)`.
- Required `n` for 80% power: `n = (z_α + 0.8416)² × (p_A(1 − p_A) + p_B(1 − p_B)) / d²`, rounded up.

**Test values (the build must reproduce these).**
- `k_A = 400, k_B = 440, n = 1000`: pooled 0.42, SE 0.02207, z 1.812, p 0.070.
- `k_A = 800, k_B = 880, n = 2000`: SE 0.01561, z 2.563, p 0.0104.
- `k_A = 4, k_B = 6, n = 10`: SE 0.2236, z 0.894, p 0.371.
- Analytic power, `p_A = 0.40, d = 0.04`: n = 100 → 8.8%; 500 → 25.0%; 1000 → 44.2%; 2000 → 72.7%; 2400 → 80.2%; 5000 → 98.2%.
- Required `n` at 80% power, `p_A = 0.40`: d = 0.10 → 385; d = 0.04 → 2,387; d = 0.02 → 9,490.
- With d = 0 and any `n ≥ 100`, the simulated significant fraction over 1,000 runs should fall between 3.5% and 6.5% nearly always.

**First screen.** Tutorial test preset (p_A = 40%, d = +4, n = 1000, α = 0.05, fixed seed). The left histogram shows fewer than half of the bars past 1.96, and the right marker sits near 44% power, below the 80% guide.
