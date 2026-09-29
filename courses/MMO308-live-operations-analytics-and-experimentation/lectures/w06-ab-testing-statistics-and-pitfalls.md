# MMO308 · Week 06 — A/B testing: statistics and pitfalls

**Why this matters:** Once a test is live, its dashboard updates every hour and everyone on the team can see it. The single most common way a live team ships a false win is by watching that dashboard and stopping the day it turns green. This week you measure exactly how bad that habit is, learn stopping rules that let you look safely, and learn the checks that catch a broken test before you believe its result.

**You will be able to:**
- Simulate an A/A test checked `K` times and compute its real false-positive rate.
- Apply Pocock and O'Brien-Fleming stopping boundaries, and compare their error rate, power and average test length.
- Run a sample ratio mismatch check with a chi-square test and name causes of mismatch specific to online games.
- Critique a revenue or engagement readout for whale-driven noise and novelty effects.

**Before class:** Johari, R., Koomen, P., Pekelis, L. & Walsh, D. (2017), "Peeking at A/B Tests: Why It Matters, and What to Do About It", KDD 2017; the long version is free on arXiv as "Always Valid Inference" (1512.04922), read section 1 and look at figure 1. Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments*, chapter 17 (the statistics behind online controlled experiments) and the chapter on sample ratio mismatch.

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (z-test, p-value, `α`, power, A/A tests, multiple comparisons, and the brief warning about peeking this week expands). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (how many trials a simulated rate needs). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (means and heavy tails). [MMO308 week 5, A/B testing design](w05-ab-testing-design.md) (the plan, the unit, hashing and exposure logging). Reading results by segment is MMO308 week 7, [segmentation](w07-segmentation.md).

**Interactive:** [w06-peeking-simulator.html](../examples/w06-peeking-simulator.html). Keep it open during section 2.

---

## 1. From one look to many

MA102 week 14 analysed a test once, at the end. That is how the z-test's 5% false-positive rate was derived. It assumes you decide the sample size first, collect it, and compute `z` one time.

Live teams do not work like that. The experiment dashboard recomputes `z` or a "chance to beat control" every hour. The producer checks it at standup. After three days B is ahead with `p = 0.03`, and someone asks why you are still waiting. Each check is a new chance for noise to cross the line, and a test stopped at its first crossing is a different test from the one the 5% came with.

This week's signature example measures the cost. MA102's lab 14 had you peek every 200 players and see the rate go up. Here you will see how it grows with the number of looks, why most of those early "wins" would have gone away, and what to do instead.

## 2. Worked example: peeking at an A/B test inflates false positives

### The hook

Figure 1 of the "Always Valid Inference" paper shows a real dashboard from a large commercial A/B testing platform. The test plotted is an A/A test, both arms identical. The dashboard's "chance to beat baseline" line wanders over the days and rises above the 95% significance threshold. Anyone watching would have declared a winner between two copies of the same page. All three authors of that paper worked at or advised Optimizely when the work was done, the platform EA's Maxis team used for the SimCity pre-order tests you met in MA102 week 14. The paper reports that its fix, always-valid p-values, was implemented in a large commercial platform and used to analyse hundreds of thousands of experiments.

If an identical A/A test can cross the line, how often will your two-week crafting test cross it by chance if you check it every morning?

### The model

Under the null hypothesis (no real effect), split a test into `K` equal batches of data and look after each batch. Each batch adds an independent standard-normal amount to a running total. The z-statistic after look `k` is the running total divided by `√k`:

```
S_k = X_1 + X_2 + ... + X_k        each X_i ~ Normal(0, 1), independent
z_k = S_k / sqrt(k)                 the z you would compute at look k
Naive rule: stop and declare a winner at the first k with |z_k| > 1.96
```

- `K` is the number of looks. `K = 1` is MA102's single analysis.
- Each `z_k` on its own has exactly a 5% chance of passing 1.96. That is why each individual look "looks" fine.
- The looks are correlated, since `z_k` shares most of its data with `z_(k−1)`. But they are not identical, so every look adds a little extra chance of a crossing.

The **real false-positive rate** is `P(|z_k| > 1.96 for at least one k ≤ K)`. For `K = 1` it is 5%. For `K > 1` there is no neat closed form, which is exactly the situation MA102 week 11 prepared you for. Simulate it.

### Numbers you can check

```python
import math
import random

def false_positive_rate(looks, sims=100_000, bound=1.96, seed=6):
    """Share of A/A tests declared significant when checked `looks` times,
    equally spaced, stopping at the first |z| > bound."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(sims):
        total = 0.0
        for k in range(1, looks + 1):
            total += rng.gauss(0, 1)          # one batch of data under no effect
            if abs(total / math.sqrt(k)) > bound:
                hits += 1
                break
    return hits / sims

for looks in (1, 2, 5, 14, 30):
    print(f"{looks:>3} looks: {false_positive_rate(looks):.1%}")
```

Output:

```
  1 looks: 5.1%
  2 looks: 8.4%
  5 looks: 14.2%
 14 looks: 22.1%
 30 looks: 28.0%
```

A run of one million simulated tests per row gives the same picture with less noise.

| Looks `K` | Real false-positive rate | Multiple of the promised 5% |
|---|---|---|
| 1 | 5.0% | 1.0× |
| 2 | 8.3% | 1.7× |
| 5 | 14.2% | 2.8× |
| 10 | 19.3% | 3.9× |
| 14 (daily, two weeks) | 22.0% | 4.4× |
| 20 | 24.8% | 5.0× |
| 30 (daily, a month) | 28.0% | 5.6× |
| 100 | 37.4% | 7.5× |

Check the first row by hand. With one look, the rule is MA102's rule, 5%. The rest you check by running the code, as MA102 week 11 taught you. The 1969 paper by Armitage, McPherson and Rowe computed these values for clinical trials without a computer simulation, and their numbers agree with this table.

A two-week test read every morning does not have a 5% false-positive rate. It has 22%. Run five such A/A tests and you should expect one of them to "win".

There is a second number worth knowing. Of the simulated A/A tests with 14 looks that crossed 1.96 at some point, only 23% were still past it at the last look. The other 77% crossed, then drifted back. Every one of those would have been shipped by a team that stopped at the first green day, and would have shown no effect in the weeks after.

### A visual you can move

Open `examples/w06-peeking-simulator.html`. The left view draws 40 simulated A/A tests as z-paths across the looks, inside a shaded band from −1.96 to +1.96. A path that leaves the band is drawn in the accent color, with a dot where a peeking team would have stopped. The right view is the false-positive rate against the number of looks, from 1,000 fresh simulations per point, with the 5% line drawn across.

Set looks to 1. The paths are single dots and about 2 of the 40 fall outside the band. Slide looks to 14. Paths wander, and with the fixed seed 6 of the 40 escape (the long-run share is 22%, about 9 in 40, so press "New 40 paths" a few times) at some point, most of them early and most of them drifting back inside by the end. The right-hand curve climbs and keeps climbing. Now switch the boundary from "1.96 every look" to "O'Brien-Fleming". The band becomes a funnel, very wide at the first look and narrowing to about 2.1 at the last. The escapes drop back to about 2 in 40, and the curve on the right goes flat at 5%.

### Cross-game recognition

The same structure, a statistic checked repeatedly against a fixed threshold, appears wherever results arrive over time.

**Clinical trials.** Drug trials check accumulating results at planned interim analyses, because stopping a trial early can save lives if a drug clearly works or clearly harms. Armitage's 1969 paper showed the inflated error rate. Stuart Pocock (1977) and Peter O'Brien with Thomas Fleming (1979) then published the stopping boundaries in section 3, which are still standard. Game teams face the same pull. A clearly winning variant that you keep testing costs revenue each day.

**Web experimentation platforms.** The "Always Valid Inference" paper documents the same problem in a commercial platform whose users, in the authors' description, routinely monitor tests continuously and stop when they see significance. The platform's response was a method that stays valid however often you look. In the model's terms, it replaces the fixed 1.96 with a boundary that widens enough to absorb any number of looks.

**A live-ops standup.** Your test plan says 14 days. The dashboard is on the wall. Each morning's glance is a look, `K = 14`, whether or not anyone intends to stop. The standup is a clinical trial's interim analysis with no stopping rule written down.

**Your own lab.** MA102 lab 14 step 4 peeked every 200 players on a 2,400-player test, `K = 12`. You should have measured about 21%, which sits in this table between 10 and 14 looks.

### Eyes-open design judgment

- **Looking is not the sin. Stopping on a naive look is.** Watch guardrails every hour, since a crash spike in B must stop the test. Just do not stop for a win unless your rule was built for repeated looks.
- **Choose between three honest options.** Fix the sample size and read the primary metric once. Or plan `K` interim looks with a group-sequential boundary. Or use an always-valid method designed for continuous monitoring. Write which one in the plan from week 5.
- **Early stopping costs something.** Sequential rules buy speed with power, or with a larger maximum sample. Section 3 puts numbers on the trade.
- **Early winners overstate the effect.** A test stopped at its first crossing stopped because noise happened to push in the winning direction. Even when the effect is real, its size at the stopping point is biased upward. Expect it to shrink after launch.

## 3. Stopping rules that survive looking

A **group-sequential design** fixes in advance how many looks `K` there will be and a boundary `b_k` for each. You stop at look `k` if `|z_k| > b_k`. The boundaries are chosen so the overall false-positive rate is exactly `α`.

- **Pocock boundary.** The same threshold at every look, raised above 1.96. For `K = 5` and `α = 0.05` it is 2.413. For `K = 14` it is 2.615.
- **O'Brien-Fleming boundary.** A threshold that starts very high and falls: `b_k = c × √(K / k)`. For `K = 5`, `c = 2.040`, so the boundaries are 4.562, 3.226, 2.634, 2.281 and 2.040. Early looks almost never stop the test. The final look is nearly the ordinary 1.96.
- **Bonferroni per look.** Test each look at `α / K`. For `K = 5` that is a threshold of 2.576 at every look. It is valid but wasteful, since it treats the looks as independent when they are strongly correlated. Its real false-positive rate is only 3.3%, not 5%.

All of these values can be found by simulation with the code above. Replace the fixed `bound` with a list of boundaries and search for the constant that brings the rate to 5%. The published tables for Pocock and O'Brien-Fleming agree with the simulated ones to the third decimal.

What do they cost? Take a test sized, as in MA102, for 80% power at a single final look, and use the same maximum sample for each rule. With a real effect of that size:

| Rule (`K = 5`) | Real false-positive rate | Power | Average share of the planned sample used |
|---|---|---|---|
| One look at the end | 5.0% | 80.0% | 100% |
| 1.96 at every look (peeking) | 14.2% | 84.9% | 58% |
| Pocock, 2.413 | 5.0% | 70.9% | 71% |
| O'Brien-Fleming | 5.0% | 78.9% | 80% |
| Bonferroni, 2.576 | 3.3% | 64.8% | 75% |

The peeking row looks attractive. It has the most power and is the fastest. That is the trap. Its power is bought with almost three times the false-positive rate.

Among the honest rules, O'Brien-Fleming gives up only one point of power and saves 20% of the sample on average when the effect is real. That is why it is the usual default. Pocock stops sooner when effects are large, but loses nine points of power unless you raise the maximum sample. Bonferroni is dominated. Use it only when you cannot compute anything better.

**Always-valid methods** go further and let you look after every player with no `K` fixed in advance. The price is a wider boundary at any given moment, so each individual look is less sensitive than a fixed-horizon test at that same sample size. The "Always Valid Inference" paper gives one such method and its trade-offs. For a live team whose members will look anyway, it is the honest choice.

## 4. Check the split before the result

Your plan said 50/50. If the arms come back 50,500 against 49,500, is that chance? Test it before reading anything else. A **sample ratio mismatch** (SRM) is a split that differs from the planned ratio by more than chance allows. The test is the chi-square goodness-of-fit test with one degree of freedom:

```
expected E = N × planned share for each arm
chi² = Σ (observed − E)² / E
p = erfc( sqrt(chi² / 2) )          (the chi-square tail with 1 degree of freedom)
```

For 50,500 against 49,500, `E = 50,000` for each arm, `chi² = 500²/50,000 + 500²/50,000 = 10.0`, and `p = 0.0016`. A split this uneven happens by chance less than twice in a thousand. For 50,150 against 49,850, `chi² = 0.9` and `p = 0.34`, which is ordinary noise.

Fabijan and colleagues (KDD 2019), drawing on experiments at four software companies across more than 25 products, compare an SRM to a fever. It is a symptom shared by many different data problems, and ignoring it without finding the cause can make a bad change look good. Treat a test with an SRM as unreadable until you know why. An SRM means some players are missing from one arm, and missing players are rarely random. Causes that show up in games:

- **B crashes before exposure is logged.** If the new client code crashes during loading, the players who crashed never send their `experiment_exposure` event. B loses exactly the players with the worst experience, and its metrics look better than they are.
- **Bots and farm accounts.** Automated accounts that follow fixed scripts may trigger the change in one arm and not the other, or be removed by anti-cheat at different rates.
- **Assignment and login disagree.** The web shop hashes the account id, the game server hashes the character id. A player with three characters counts once in one place and three times in another.
- **Triggering only in one arm.** If B shows a new button that counts as the trigger, and A has no button, B's triggered group includes curious clickers A never counts. Week 5's rule, a trigger that happens the same way in both arms, prevents this.

Run the SRM check first, on every test, automatically. It is one line of arithmetic.

## 5. Metrics that lie even when the split is fine

### Whales

Revenue per player is the metric studios care about and the hardest one to test. Spending in most free-to-play games is highly concentrated. A small share of players, often called **whales**, account for a large share of revenue ([MMO403 week 9](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w09-whales-and-spending-distributions.md) studies the spending distribution in detail). For testing, this means the mean is dominated by a handful of players, and its standard error is huge (MA102 week 12 on means and heavy tails).

A made-up but typical case. Each arm has 10,000 players. A earns $19,000, B earns $22,000, so revenue per player is $1.90 against $2.20, a 16% lift. One player in B spent $4,000. Remove that one player and B's revenue per player is $18,000 / 9,999 = $1.80, below A. The whole "lift" was one person, who was assigned to B by a coin flip.

Three standard defenses, each with a cost.

- **Cap (winsorize) each player's spend** at, say, the 99.9th percentile of last month's spenders. Capping the $4,000 player at $500 gives B $18,500, or $1.85. The variance falls sharply. The metric is now "capped revenue", and a change that works only on whales becomes invisible.
- **Split the metric in two.** Test conversion (share who pay anything) as one rate and spend per payer as another. Conversion is a rate, so MA102's z-test applies directly. Spend per payer is still heavy-tailed, but you now know which part moved.
- **Run longer.** Heavy tails need large samples. Kohavi and colleagues recommend estimating the variance from past data before the test and sizing for it. Lehr's rule from MA102 applies with the metric's own variance in place of `p(1 − p)`.

### Novelty and learning

A changed interface gets clicked because it is new. A changed reward gets chased for a few days, then treated as normal. The effect on day 1 of exposure is often larger, or smaller, than on day 14.

Check it by plotting the treatment effect by days since each player's first exposure, not by calendar day. Here is an illustrative pattern for a new daily-quest board:

| Days since first exposure | 1 | 3 | 7 | 14 |
|---|---|---|---|---|
| Lift in quests completed per player | +4.0 | +2.0 | +0.8 | +0.5 |

A test that stopped after three days would see mostly first-, second- and third-day players and report a lift four to eight times the lasting one. If the curve is still falling at the end of the test, the honest statement is "at least +0.5, still declining". The opposite pattern also occurs. A complex new crafting interface may lose on day 1 while players learn it and win by week 2. A short test would kill a good change.

This is another reason the week 5 plan runs whole weeks and keeps a long-term holdout for large changes.

### Everything at once

MA102 week 14 showed that testing 20 metrics gives a 64% chance of at least one false win. Peeking multiplies with it. A test with 5 metrics read daily for two weeks has 70 chances to cross 1.96. The primary metric from your week 5 plan, read at its planned looks with its planned boundary, is the only result that carries its stated error rate. Everything else is a lead for the next test. Week 7 applies the same rule to results split by player segment.

## In-class activity (25 minutes)

In groups of three with one laptop, the code from section 2 and the interactive.

1. **Your team's real error rate (8 min).** Your studio runs every test for 21 days and the dashboard is checked each weekday, 15 looks in all. Adapt the code to find the real false-positive rate. If the studio runs 30 tests a year where the change truly does nothing, how many false wins should it expect?
2. **Find a boundary (10 min).** Change the code to use a constant boundary `b` at every look and search (by trial and error or bisection) for the `b` that gives 5% for `K = 15`. Compare with the interactive's Pocock value.
3. **Read a broken test (7 min).** A test assigned 50/50 reports 61,200 players in A and 60,100 in B. B's day-1 retention is 1.2 points higher, `p = 0.01`. Run the SRM check. What would you tell the producer, and what would you look at first?

Expected output: about 22.5% for 15 looks (your simulated value will vary by about half a point), so roughly 7 false wins a year instead of 1.5. A Pocock constant near 2.63 (the exact value is 2.626). For step 3, `chi² ≈ 9.98`, `p ≈ 0.0016`, so do not read the retention result. B is missing about 550 players relative to an even split, and a client crash or a missing exposure event in B is the first suspect.

## Common misconceptions

- **"Each look has a 5% error rate, so looking often is fine."** Each look does. The chance that at least one look crosses grows with every look, to 22% for 14 daily looks.
- **"If it's significant now, more data will only confirm it."** Under no effect, most early crossings drift back. Only 23% of 14-look A/A crossings were still significant at the end.
- **"A sequential test is always slower."** With a real effect, O'Brien-Fleming used 80% of the planned sample on average, for one point of power.
- **"A small split imbalance is harmless."** A 1% imbalance on 100,000 players is `p = 0.0016`. It signals missing players, and missing players are rarely random.

## Check yourself

1. A team runs an A/A test for 10 days and checks it every day with the naive rule. Using the table, what is the chance it reports a winner? If they instead check only on day 5 and day 10, about what is it?
2. For `K = 4` looks, the O'Brien-Fleming constant is 2.024. Compute the four boundaries. Would `z = 2.5` at the second look stop the test?
3. A 90/10 ramped test (90% A) has 90,450 players in A and 9,550 in B. Run the SRM check.
4. A test on revenue per player shows B ahead by 12% with `p = 0.04`. The top spender in B spent 300 times the median payer. Name two analyses you would run before believing the result.

<details>
<summary>Answers</summary>

1. About 19.3% with 10 looks. With 2 looks, about 8.3%.
2. `b_k = 2.024 × √(4/k)`: 4.048, 2.862, 2.337, 2.024. At look 2 the boundary is 2.862, so `z = 2.5` does not stop the test.
3. `N = 100,000`, expected 90,000 and 10,000. `chi² = 450²/90,000 + 450²/10,000 = 2.25 + 20.25 = 22.5`, `p ≈ 2 × 10⁻⁶`. Serious mismatch. Find the cause before reading any metric.
4. Recompute with that player removed, or with spend capped at a pre-set percentile. Split the metric into payer conversion and spend per payer, and test conversion as a rate. Also run the SRM check, and confirm revenue was the pre-registered primary metric and was read at its planned look.

</details>

## Lab / assignment hook

[Lab 06, peeking, boundaries and a broken split](../labs/lab06.md). You simulate the false-positive rate of peeking for any number of looks, find Pocock and O'Brien-Fleming boundaries by simulation, and then analyse a 14-day experiment log day by day: you will see it cross 1.96 early, apply a proper boundary, and find the sample ratio mismatch hiding in it. The write-up is the analysis half of the A/B report assessment.

## Sources

- Johari, R., Pekelis, L. & Walsh, D. J. (2015, revised 2019). "Always Valid Inference: Bringing Sequential Analysis to A/B Testing." arXiv:1512.04922. Figure 1, an A/A test on a large commercial platform's dashboard crossing the 95% threshold under continuous monitoring; users continuously monitor tests; the method implemented in a commercial platform and used on hundreds of thousands of experiments; author affiliations with Optimizely, Inc. Read September 2026.
- Johari, R., Koomen, P., Pekelis, L. & Walsh, D. (2017). "Peeking at A/B Tests: Why It Matters, and What to Do About It." *Proceedings of KDD 2017*, doi:10.1145/3097983.3097992.
- Armitage, P., McPherson, C. K. & Rowe, B. C. (1969). "Repeated Significance Tests on Accumulating Data." *Journal of the Royal Statistical Society, Series A*, 132(2), 235-244.
- Pocock, S. J. (1977). "Group Sequential Methods in the Design and Analysis of Clinical Trials." *Biometrika*, 64(2), 191-199.
- O'Brien, P. C. & Fleming, T. R. (1979). "A Multiple Testing Procedure for Clinical Trials." *Biometrics*, 35(3), 549-556.
- Jennison, C. & Turnbull, B. W. (2000). *Group Sequential Methods with Applications to Clinical Trials*. Chapman & Hall/CRC. Chapter 2 tables of Pocock and O'Brien-Fleming constants.
- Fabijan, A., Gupchup, J., Gupta, S., Omhover, J., Qin, W., Vermeer, L. & Dmitriev, P. (2019). "Diagnosing Sample Ratio Mismatch in Online Controlled Experiments." *Proceedings of KDD 2019*, 2156-2164, doi:10.1145/3292500.3330722. Abstract read via OpenAlex, September 2026: experience from four software companies and over 25 products; SRM as a symptom of many data-quality issues.
- Kohavi, R., Tang, D. & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*. Cambridge University Press. Chapter 17 on the statistics of online experiments; sample ratio mismatch; capping heavy-tailed metrics; novelty and primacy effects.
- MA102 week 14 for the SimCity pre-order test on Optimizely (Optimizely case study and TechCrunch, June 2013).
- The false-positive tables, boundaries, power and sample-use figures, crossing statistics and SRM values were computed by the author: the code shown, and a NumPy run of one million simulated tests per setting (seed-fixed). The whale and novelty numbers are illustrative.

## Interactive spec: examples/w06-peeking-simulator.html

**The one insight.** Checking an A/A test repeatedly and stopping at the first `|z| > 1.96` turns a 5% false-positive rate into 22% for 14 looks. A boundary designed for repeated looks brings it back to 5%. The student sees paths escape a fixed band and then sees the same paths stay inside a funnel-shaped one.

**Layout.** Two linked views side by side on desktop, stacked on mobile.

- **Left view, "40 experiments, looked at K times".** x axis: look number 1 to K. y axis: z from −5 to +5. Shaded acceptance region between the current boundaries (`±1.96` flat, `±Pocock` flat, or the O'Brien-Fleming funnel). Draw 40 paths `z_k` as thin lines. A path that crosses the boundary is drawn in the accent color up to its first crossing, with a filled dot there, and faint afterward (so the student sees it drift back). Header: "Stopped as winners: X of 40".
- **Right view, "Real false-positive rate".** x axis: looks 1 to 50 (log). y axis: 0% to 45%. Line of the simulated rate for the current boundary type (2,000 simulations per K, computed once per boundary change, cached), a dashed horizontal line at 5%, and a marker at the current K with its value. Show the reference values from the test table as small ticks.
- **Readout row.** K, boundary type, the boundary values at each look (list, 3 decimals; truncate to first 5 and last with "..." when K > 8), simulated false-positive rate at K (from 20,000 simulations when the student presses "Run 20,000"), and, when the effect toggle is on, power and average share of the planned sample used.

**Controls (keyboard accessible, update immediately).**
- Looks `K`: stepped slider [1, 2, 3, 5, 10, 14, 20, 30, 50], default 14.
- Boundary: radio "1.96 every look (peeking)" / "Pocock" / "O'Brien-Fleming" / "Bonferroni α/K". Default peeking.
- True effect: toggle "None (A/A)" / "Sized for 80% power at the end" (drift: add `θ/√K` to each batch with `θ = 2.8016`). Default none.
- Buttons: "New 40 paths", "Run 20,000". Checkbox "Fixed seed" (default on, mulberry32, seed 6).

**Formulas.**
- Batch increments `X_i ~ Normal(0,1) + θ/√K` (θ = 0 under A/A), from Box-Muller on the seeded PRNG. `S_k = Σ_{i≤k} X_i`, `z_k = S_k/√k`.
- Stop at the first `k` with `|z_k| > b_k`.
- Peeking: `b_k = 1.96`. Bonferroni: `b_k = Φ⁻¹(1 − 0.025/K)` (use a rational approximation for the normal quantile, for example Acklam's).
- Pocock and O'Brien-Fleming: precomputed constants (do not solve in the browser). Pocock `c_P`: K=1 1.960, 2 2.178, 3 2.289, 5 2.413, 10 2.555, 14 2.615, 20 2.672, 30 2.731, 50 2.797. O'Brien-Fleming `c_O` with `b_k = c_O·√(K/k)`: K=1 1.960, 2 1.977, 3 2.004, 5 2.040, 10 2.087, 14 2.107, 20 2.126, 30 2.145, 50 2.165. These were computed by numerical integration of the crossing probabilities and checked against 10⁶ simulated A/A tests per K; the K ≤ 10 values match the published tables (Jennison & Turnbull 2000, chapter 2).
- Power (effect on): share of runs that stop. Average sample used: mean over runs of (stopping look / K), with runs that never stop counted as 1.

**Test values (1,000,000 simulations; the build's 20,000-run button should land within ±0.5 points).**
- Peeking false-positive rate: K=1 5.0%, 2 8.3%, 5 14.2%, 10 19.3%, 14 22.0%, 20 24.8%, 30 28.0%, 100 37.4%.
- K = 5: Pocock 2.413; O'Brien-Fleming boundaries 4.562, 3.226, 2.634, 2.281, 2.040; Bonferroni 2.576 with real rate 3.3%.
- K = 5, effect on: one look power 80.0%; peeking 84.9% power, 58% sample; Pocock 70.9%, 71%; O'Brien-Fleming 78.9%, 80%; Bonferroni 64.8%, 75%.
- K = 14: Pocock 2.615; O'Brien-Fleming c 2.107, first boundary 7.882, last 2.107.
- K = 14, A/A, peeking: of runs that ever cross, 23% are past 1.96 at the last look.

**First screen.** K = 14, peeking, A/A, fixed seed. With seed 6, 6 of the 40 paths are highlighted with stop dots (the long-run average is about 9), most in the first five looks, and the right-hand marker reads about 22% above the 5% line.
