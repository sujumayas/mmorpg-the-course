# MA102 · Week 13 — Sampling, confidence and why n=5 lies

**Why this matters:** Every number you measure from players is a sample. Four of five playtesters beat your boss, a wiki says a mount drops 1% of the time, a forum post claims a shiny rate. Each of these is a guess with an error bar that nobody wrote down, and this week you learn to write it down before you act on it.

**You will be able to:**
- Compute the standard error and a 95% confidence interval for a rate measured from a sample.
- Explain why the simple interval fails at small samples and compute the Wilson interval and the rule-of-three bound instead.
- Calculate the sample size needed to measure a rate to a chosen precision, including rare drop rates.
- Critique a playtest or community statistic for sample size and for sampling bias.

**Before class:** Schreiber, *Game Balance Concepts*, Level 5 ("Probability and Randomness Gone Horribly Wrong"); OpenIntro Statistics (4th ed.), sections 5.1 and 5.2 on point estimates and confidence intervals for a proportion.

**Prerequisites from earlier courses:** MA102 weeks 3, 6 and 12 in the [MA102 syllabus](../syllabus.md) (complement rule, binomial distribution, descriptive statistics), plus [week 5 on variance](w05-variance-and-swingy-designs.md) and [week 8 on the normal curve](w08-dice-sums-and-the-normal-curve.md). Square roots and reading curves from MA101, see the [MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md).

**Interactive:** [w13-sampling-intervals.html](../examples/w13-sampling-intervals.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Samples, populations and the number you wish you had

Start with vocabulary. You will use these words for the rest of your career, so pin them down now.

- The **population** is everyone or everything you care about. All players who will ever fight your boss. Every kill of a monster that can drop a mount.
- A **parameter** is a number that describes the population. The true clear rate of the boss. The true drop rate programmed into the loot table. You usually cannot see it.
- A **sample** is the part of the population you actually observed. The five people in Tuesday's playtest. The 300 kills logged by a fan site.
- A **statistic** is a number computed from the sample. "4 of 5 cleared it, so 80%."

The whole of this week is one idea. **A statistic is a parameter plus noise, and the size of the noise depends on how big the sample is.** Your job is to estimate how big the noise is, so you know how much to trust the statistic.

In week 6 you met the binomial distribution. If the true clear rate is `p` and you watch `n` independent attempts, the number of clears `k` is binomial. That means the sample rate `p̂ = k/n` (read "p-hat", the hat marks an estimate) is itself a random variable. Run the same five-player playtest twice with different people and you get different answers, even though your boss did not change.

Here is what that looks like when the true clear rate is 60% and you test five players. The table lists every possible outcome and how often it happens, using the binomial formula `C(5,k) × 0.6^k × 0.4^(5−k)`.

| Clears out of 5 | Measured rate `p̂` | Probability |
|---|---|---|
| 0 | 0% | 1.0% |
| 1 | 20% | 7.7% |
| 2 | 40% | 23.0% |
| 3 | 60% | 34.6% |
| 4 | 80% | 25.9% |
| 5 | 100% | 7.8% |

Two things jump out. First, five testers can only ever report six values, in steps of 20 points. You cannot measure 60% more precisely than "somewhere between 40 and 80" with that ruler. Second, the right answer (60%) comes up only about a third of the time. One time in three, the playtest reports 80% or 100% and your team concludes the boss is easy. One time in four it reports 40% or less and someone nerfs a boss that was fine.

That is the headline. **n=5 does not lie because players are unreliable. It lies because the ruler is coarse and the noise is as large as the effect you care about.**

## 2. Worked example: how sure is a measured rate?

### The hook: a whole community measured it, and still had to revise

Pokémon GO never published its base shiny rate, the chance that a wild Pokémon appears in its rare alternate colors. The Silph Road, a volunteer research group, crowd-sourced encounter logs from players and in 2018 estimated the base rate at about 1 in 450. That number became common knowledge. Players quoted it, calculators used it.

Then, with a larger and cleaner dataset, the same group reported that the evidence fit a base rate near 1 in 500 or 1 in 512 better, and they said their 2018 figure had likely been biased. A community of thousands, pooling data for years, was off by roughly 12%.

So here is the puzzle. If thousands of players could not pin down a rate to better than about 10%, what does your five-person playtest tell you about your boss? And how many kills does a fan site need before its "1.2% drop rate" means anything?

### The model

For a rate measured from `n` independent trials with `k` successes:

```
p̂  = k / n                                   (the measured rate)
SE = sqrt( p̂ × (1 − p̂) / n )                 (standard error)
95% confidence interval = p̂ ± 1.96 × SE
```

- `n` is the sample size: players tested, kills logged, encounters seen.
- `k` is the count of successes: clears, drops, shinies.
- `p̂` is your estimate of the true rate `p`.
- `SE` is the **standard error**, the typical distance between `p̂` and `p` if you repeated the whole study many times. It is the standard deviation (week 5) of the statistic, not of the players.
- `1.96` comes from the normal curve (week 8). About 95% of a normal distribution lies within 1.96 standard deviations of its center.
- `1.96 × SE` is the **margin of error**.

A **95% confidence interval** is a range built by a recipe that captures the true rate in 95% of studies. Read it as a statement about the recipe: "if every team in the world ran this playtest and built this interval, 95 of every 100 intervals would contain the true clear rate." You never know whether yours is one of the 95 or one of the 5.

Look at the `n` in the denominator under the square root. That square root is the whole story of sample size. To halve the margin of error you need **four times** the data. To cut it by ten you need a hundred times the data.

### Numbers you can check

Suppose the team keeps seeing an 80% clear rate as they test more people. Here is what each sample size actually supports. The "simple" column uses the formula above. The "Wilson" column uses a better formula for small samples, which section 3 explains.

| Sample | `p̂` | SE | Simple 95% interval | Wilson 95% interval |
|---|---|---|---|---|
| 4 of 5 | 80% | 17.9 pts | 44.9% to 115.1% | 37.6% to 96.4% |
| 16 of 20 | 80% | 8.9 pts | 62.5% to 97.5% | 58.4% to 91.9% |
| 80 of 100 | 80% | 4.0 pts | 72.2% to 87.8% | 71.1% to 86.7% |
| 800 of 1,000 | 80% | 1.3 pts | 77.5% to 82.5% | 77.4% to 82.4% |

Check the first row by hand. `0.8 × 0.2 = 0.16`. `0.16 / 5 = 0.032`. `sqrt(0.032) = 0.179`. `1.96 × 0.179 = 0.351`. So `0.80 ± 0.35`, which runs past 100%.

That upper end of 115% is your first clue that the simple formula is broken at `n = 5`. A clear rate cannot exceed 100%. We fix that in section 3. For now, read the Wilson column. **Four of five testers beating your boss is consistent with a true clear rate anywhere from about 38% to 96%.** That range covers "brutal" and "trivial". The playtest told you almost nothing about difficulty.

At 1,000 players the interval is 5 points wide. Now you can make a tuning decision.

### A visual you can move

Open `examples/w13-sampling-intervals.html`. The left panel shows one playtest, the kind your team actually runs, with its single interval. It looks authoritative. The right panel runs the same playtest 100 times against the same true rate and stacks all 100 intervals. The intervals that miss the true rate turn orange.

Set the true rate to 60% and `n` to 5. Switch the method to "simple". Count the orange bars on the right. About 16 in 100 miss, not 5, because the simple formula is wrong at this size. Switch to Wilson and the misses drop to about 1 in 100, while every bar stays wide. Now drag `n` to 100. The bars shrink to a quarter of their old width and both methods agree.

The left panel is what you see in a meeting. The right panel is what is really going on.

### Cross-game recognition

The same formula runs under very different surfaces. Your skill is to rewrite each case as "`k` out of `n`, so the margin is about `1.96 × sqrt(p(1−p)/n)`".

**Pokémon GO shiny rates.** Rewrite the Silph Road question. Telling 1 in 450 (`p = 0.00222`) apart from 1 in 512 (`p = 0.00195`) means resolving a difference of 0.00027. For a 95% margin of half that difference, solve `1.96 × sqrt(p(1−p)/n) = 0.000135` with `p ≈ 0.00195`:

```
n = 1.96² × 0.00195 × 0.998 / 0.000135² ≈ 410,000 encounters
```

That is why an estimate from a very large community still wobbled. Rare events need enormous samples. Even ±10% relative precision on a 1-in-450 rate needs about 170,000 encounters.

**Nielsen's "test with five users".** In 2000, usability researcher Jakob Nielsen argued that five test users find about 85% of an interface's usability problems. That sounds like it contradicts this lecture. It does not, because it answers a different question. His model is the complement rule from week 3. If each problem is hit by a given user with probability `L = 0.31`, the chance at least one of five users hits it is `1 − (1 − 0.31)^5 = 0.84`. That is discovery, "does this problem exist?" His own group later wrote that five users are fine for finding problems and misleading for measuring rates, and recommended well over 30 participants for numbers. Same five people, two questions, two verdicts. Use n=5 to find what is broken. Never use it to report a percentage.

**Opinion polls.** A national poll of about 1,000 people reports "±3 points". Plug in the worst case `p = 0.5`: `1.96 × sqrt(0.25/1000) = 0.031`. Same formula, same square root. Note what is missing. The population of the country does not appear anywhere. A poll of 1,000 is as precise for a small country as for a large one, and a fan-site sample of 1,000 kills is as precise for a niche boss as for a popular one.

### Eyes-open design judgment

Confidence intervals do not tell you what to do. They tell you how much you know. Decide these things deliberately.

- **Decide the precision before you collect.** If a clear rate between 50% and 70% would lead to the same tuning decision, a ±10-point margin is enough and you need about 100 players. If you are choosing between a 1% and a 1.5% drop rate, you need tens of thousands of kills. Pick `n` from the decision, not from the calendar.
- **Small playtests are for discovery.** Five players are excellent at showing you that a door is hard to find. They are useless for telling you what fraction of players will find it. Report what you saw ("3 of 5 missed the door"), never a percentage with no interval.
- **Show the interval in the report.** "80% (38% to 96%, n = 5)" stops a meeting from overreacting. "80%" starts one.
- **Precision is not accuracy.** A huge sample from the wrong people gives a tight interval around the wrong number. Section 5 returns to this.

### Check yourself (worked example)

1. A fan site logs 2,000 kills of a raid boss and records 24 drops of a rare mount. Compute `p̂`, SE and the simple 95% interval. Is the site entitled to claim "the drop rate is 1%"?
2. You want to measure a tutorial completion rate near 70% to within ±4 points. About how many players do you need?

<details>
<summary>Answers</summary>

1. `p̂ = 24/2000 = 0.012`. `SE = sqrt(0.012 × 0.988 / 2000) = 0.00243`. Interval `0.012 ± 0.0048`, so 0.72% to 1.68%. The data are consistent with 1%, but also with 1.5%. "About 1%, give or take half a percent" is the honest claim.
2. `n = 1.96² × 0.7 × 0.3 / 0.04² = 3.8416 × 0.21 / 0.0016 ≈ 505` players.

</details>

## 3. Why the simple interval breaks, and what to use instead

The simple formula (statisticians call it the **Wald interval**) assumes the distribution of `p̂` is a smooth bell curve centered on the truth. That is fine when you expect at least about 10 successes and 10 failures. At `n = 5` the distribution is six spikes (look back at the table in section 1), and near 0% or 100% it is lopsided. Three failures follow.

1. **It spills past 0% and 100%.** You saw 4 of 5 give an upper bound of 115%.
2. **It collapses to zero width at the extremes.** If 5 of 5 testers clear the boss, `p̂ = 1`, so `p̂(1 − p̂) = 0` and the interval is "100% to 100%". The formula claims certainty exactly when you know least.
3. **It misses far more than 5% of the time.** The table below gives the true coverage, the fraction of studies whose interval really contains `p`. These are exact binomial calculations, not simulations.

| True rate | `n` | Simple (Wald) coverage | Wilson coverage |
|---|---|---|---|
| 60% | 5 | 83.5% | 99.0% |
| 80% | 5 | 66.6% | 94.2% |
| 5% | 20 | 63.9% | 92.5% |
| 2% | 100 | 86.6% | 94.9% |
| 60% | 100 | 94.8% | 94.8% |
| 2% | 1,000 | 95.0% | 94.7% |

The simple interval is dangerous at small `n` and at rare rates, which is exactly where game designers use it most (playtests and drop rates). Agresti and Coull made this point in a well-known 1998 paper, arguing that a slightly different formula beats the textbook one.

### The Wilson interval

The **Wilson score interval** fixes these failures. It looks worse on paper and is easy in a spreadsheet:

```
center    = ( p̂ + z²/(2n) ) / ( 1 + z²/n )
halfwidth = z × sqrt( p̂(1 − p̂)/n + z²/(4n²) ) / ( 1 + z²/n )
interval  = center ± halfwidth,     with z = 1.96
```

Two things happen. The center is pulled toward 50%, so 4 of 5 gets a center near 67% instead of 80%. And the `z²/(4n²)` term keeps the width above zero even when `k = 0` or `k = n`. For 5 of 5 clears, Wilson gives 56.6% to 100%. For 0 of 5, it gives 0% to 43.4%.

A shortcut worth memorizing, the **Agresti-Coull "plus four" rule**: add two successes and two failures, then use the simple formula. For 4 of 5 you compute with 6 of 9, which gives `0.667 ± 0.308`. That is close to Wilson and you can do it in your head.

Use Wilson (or plus four) by default. When `n` is large and the rate is not extreme, all three agree, so you lose nothing.

### Zero drops: the rule of three

Drop rates bring a special case. You kill a boss 100 times and see no drop. What can you say?

The simple interval says "0% to 0%", which is absurd. Go back to the complement rule. If the true rate is `p`, the chance of seeing zero drops in `n` kills is `(1 − p)^n`. Find the rate `p` for which a dry streak of `n` would happen only 5% of the time:

```
(1 − p)^n = 0.05
n × ln(1 − p) = ln(0.05) ≈ −3.0
p ≈ 3 / n            (because ln(1 − p) ≈ −p for small p)
```

This is the **rule of three**. After `n` trials with zero successes, the 95% upper bound on the rate is about `3/n`. After 100 dry kills, the drop rate is plausibly anything up to 3%. After 300, up to 1%. It is the week 3 signature example read backwards. There you learned that one player in twenty still lacks a 1% drop after about 300 kills. Here, 300 dry kills is exactly the point where a 1% rate starts to look unlikely.

## 4. Planning a sample size

Turn the margin formula around and solve for `n`:

```
n = z² × p(1 − p) / m²          (m = margin of error you want, z = 1.96)
```

If you do not know `p`, use `p = 0.5`, the worst case, which gives the handy rule **`n ≈ 1 / m²`**.

| Margin wanted | `n` at worst case `p = 0.5` |
|---|---|
| ±20 points | 25 |
| ±10 points | 97 |
| ±5 points | 385 |
| ±3 points | 1,068 |
| ±1 point | 9,604 |

For rare events, absolute margins mislead. A ±1-point margin on a 1% drop rate is useless, since it spans 0% to 2%. Think in **relative** precision instead. To measure a rate `p` to within ±`r` of itself (for example ±20% of the rate):

```
n ≈ 3.84 × (1 − p) / (p × r²)
```

For a 1% drop rate at ±20% relative precision (0.8% to 1.2%), `n ≈ 3.84 × 0.99 / (0.01 × 0.04) ≈ 9,500` kills. For a 0.1% drop, multiply by ten. When you read a claimed rate for a very rare item, ask how many kills stand behind it. If the answer is a few hundred, the number is a rumor.

## 5. Bias: the error that sample size cannot fix

Everything above handles **random error**, the wobble that shrinks as `n` grows. There is a second kind. **Sampling bias** is error from sampling the wrong way, and it does not shrink at all. Collect a million biased observations and you get a very tight interval around the wrong answer.

Where bias comes from in games:

- **Self-selection.** Players who log their drops to a fan site are not typical. Players who got a rare drop are more excited to report it. The Silph Road noted that its early shiny data had likely been biased, and a larger sample would not have fixed that alone. Better collection did.
- **Convenience samples.** Your playtesters are classmates, friends, or the QA team. They play more games than your audience and know your genre. Their clear rate overstates the public's.
- **Survivorship.** Measuring the clear rate of a raid from players who reached the raid ignores everyone who quit before. Measuring satisfaction among players still subscribed ignores those who left.
- **Non-independence.** The formulas assume independent trials. Five testers who watch each other play are not five independent samples. A guild that farms a boss together shares strategy, so their clear rates move together.

The practical rule: before you ask "is `n` big enough?", ask "would a bigger `n` of these same people give me the right answer?" If not, fix who you sample first.

## In-class activity (25 minutes)

Materials: one six-sided die per pair, the shared class spreadsheet (one row per pair), the interactive on a projector.

The "boss" drops loot on a roll of 6, so the true drop rate is `1/6 ≈ 16.7%`. Pretend nobody knows that.

1. Each pair rolls 20 times and records the number of 6s (`k`).
2. Compute `p̂`, the simple interval and the Wilson interval (or the plus-four shortcut). Enter them in your row.
3. When every pair has entered data, the instructor sorts the rows and draws each interval as a bar with a vertical line at 16.7%. Count how many of the simple intervals and how many of the Wilson intervals miss.
4. Pool all the class rolls into one big sample. Compute the interval again. How much narrower is it? Does its width match the `sqrt(n)` prediction?
5. Discussion (5 minutes). One pair rolled an unusual result. Should their interval be thrown out? Why not?

Expected output: a class chart of 15 to 25 intervals, a count of misses for each method (Wilson should miss about one in twenty, simple at `n = 20` noticeably more), and one pooled estimate close to 16.7%.

## Common misconceptions

- **"A 95% interval means there is a 95% chance the true rate is inside it."** The 95% belongs to the method, not to your particular interval. Across many studies, 95% of intervals built this way capture the truth. For everyday design decisions the loose reading does little harm, but it breaks down when people cherry-pick the one interval they like from many.
- **"We need to sample a percentage of the player base."** Precision depends on `n`, not on `n` divided by the population. A thousand players give about ±3 points whether your game has ten thousand players or ten million.
- **"Five testers is useless."** Five testers are excellent at discovery, as Nielsen's model shows. They are useless for measuring rates. Match the sample to the question.
- **"More data fixes everything."** More data fixes random error. It does nothing for bias, and it makes biased results look more convincing.

## Check yourself

1. A designer reports "our new dungeon has a 90% completion rate" from 9 of 10 playtesters. Compute the Wilson 95% interval (or use plus four). Write the one-sentence version of this result you would put in a report.
2. You killed a boss 60 times with no drop. What is the rule-of-three upper bound on the drop rate? The wiki says the rate is 5%. How surprised should you be?
3. A survey of 400 players finds 55% want a harder mode. Your producer says "that's a majority". Compute the 95% interval and respond.
4. Your margin on a clear rate is ±8 points with 150 players. Roughly how many players would you need for ±4 points? For ±2?

<details>
<summary>Answers</summary>

1. Plus four: 11 of 14, `p̂ = 0.786`, `SE = sqrt(0.786 × 0.214 / 14) = 0.110`, interval about 57% to 100% (Wilson gives 59.6% to 98.2%). Report: "9 of 10 playtesters completed it; the true completion rate could be anywhere from about 60% to 98%."
2. `3 / 60 = 5%`. The chance of 60 dry kills at a true 5% rate is `0.95^60 ≈ 0.046`. That is unusual, about a 1 in 22 streak, but it happens to thousands of players in a large game. Be mildly suspicious, not certain the wiki is wrong.
3. `SE = sqrt(0.55 × 0.45 / 400) = 0.0249`, margin `0.049`, interval 50.1% to 59.9%. The data barely exclude 50%. "Probably a slight majority" is fair, "a clear majority" is not. And check who answered the survey.
4. The margin scales as `1/sqrt(n)`. Halving the margin needs 4× the players, so 600 for ±4 and 2,400 for ±2.

</details>

## Lab / assignment hook

**Lab 13: How many kills until you trust a drop rate?** ([labs/lab13.md](../labs/lab13.md)). You simulate drop logs from a loot table with a hidden rate, compute simple and Wilson intervals at growing sample sizes, measure their real coverage, and write a one-page guideline for your team on reporting rates from playtests. It counts toward the problem-set grade and uses the Monte Carlo skills from week 11.

## Sources

- The Silph Road research group, reported by Bleeding Cool (T. Dwyer, "The Startling Truth About the Shiny Rate in Pokémon GO", March 2021), and Bleeding Cool, "What Is The Shiny Rate For Wild Spawns In Pokémon GO?". The 2018 crowd-sourced estimate of about 1 in 450, the later analysis favoring about 1 in 500 or 1 in 512, and the researchers' note that the earlier figure was likely biased. Pokémon GO, 2018 to 2021 era. The rate is not officially published by Niantic, so treat these as community estimates.
- Nielsen, J. (2000). "Why You Only Need to Test with 5 Users." Nielsen Norman Group. Model `1 − (1 − L)^n` with `L = 31%`, five users finding about 85% of problems.
- Nielsen Norman Group, "Why 5 Participants Are Okay in a Qualitative Study, but Not in a Quantitative One." The distinction between finding problems and measuring metrics, and the recommendation of more than 30 (preferably 40 or more) participants for quantitative studies.
- Agresti, A. & Coull, B. A. (1998). "Approximate is better than 'exact' for interval estimation of binomial proportions." *The American Statistician* 52(2), 119-126. Poor coverage of the Wald interval, the add-two-successes-and-two-failures adjustment.
- Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference." *Journal of the American Statistical Association* 22, 209-212. The score interval.
- Hanley, J. A. & Lippman-Hand, A. (1983). "If nothing goes wrong, is everything all right? Interpreting zero numerators." *JAMA* 249(13), 1743-1745. The rule of three.
- Diez, D., Çetinkaya-Rundel, M. & Barr, C. (2019). *OpenIntro Statistics*, 4th ed., chapter 5.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 5, "Probability and Randomness Gone Horribly Wrong." gamebalanceconcepts.wordpress.com.
- All interval and coverage values in this lecture were computed by the author from the binomial distribution and can be reproduced with the formulas given.

## Interactive spec: examples/w13-sampling-intervals.html

**The one insight.** A single small-sample result looks precise, but repeating the same study shows how widely it scatters, and the simple interval misses far more often than it claims at small `n`. The student should see a column of 100 intervals and count the misses without reading any text.

**Layout.** Two linked views side by side on desktop, stacked on mobile (single study on top).

- **Left view, "Your playtest".** One simulated study. Large text shows `k of n`, `p̂` as a percent, and the interval as "low% to high%". Below it, a horizontal 0% to 100% axis with the interval drawn as a bar, a dot at `p̂`, and a vertical dashed line at the true rate. Bar is neutral color if it contains the truth, orange accent if it misses. If the simple interval exceeds [0, 1], draw the overflow part hatched and label it "impossible values" (do not clamp silently).
- **Right view, "100 teams ran the same playtest".** 100 horizontal bars stacked vertically, each one study's interval on the same 0% to 100% axis, with the same dashed truth line. Misses in orange. Header shows "Missed the truth: X of 100 (method promises 5)". Under it, a small histogram of the 100 `p̂` values, which at `n = 5` shows only six spikes.
- Below both views, a readout row with exact numbers: true `p`, `n`, SE for the left study, margin, and the exact theoretical coverage of the current method at the current `p` and `n` (computed by summing binomial probabilities, not simulated).

**Controls (all keyboard accessible, change the picture immediately).**
- True rate `p`, slider 1% to 99%, step 1%, default 60%.
- Sample size `n`, stepped slider over [5, 10, 20, 50, 100, 400, 1000], default 5.
- Method toggle: "Simple (Wald)" / "Wilson", default Simple.
- Button "Run 100 more teams" redraws the right view with fresh random samples. Button "New playtest" redraws the left view only.
- A "Fixed seed" checkbox (default on) using a seeded PRNG (for example mulberry32 with seed 13) so the first screen is identical for every student and matches the lecture.
- Preset buttons: "4 of 5 cleared" (sets p = 80%, n = 5, and forces the left study to k = 4), "Rare drop" (p = 2%, n = 100), "Poll" (p = 50%, n = 1000).

**Formulas.**
- Sample: `k = number of U < p` for `n` uniform draws.
- Wald: `p̂ ± 1.96 × sqrt(p̂(1 − p̂)/n)`.
- Wilson: `center = (p̂ + z²/(2n)) / (1 + z²/n)`, `half = z × sqrt(p̂(1 − p̂)/n + z²/(4n²)) / (1 + z²/n)`, `z = 1.96`.
- Exact coverage: `sum over k = 0..n of C(n,k) p^k (1−p)^(n−k)` for each `k` whose interval contains `p`. Use log-gamma or iterative binomial terms so `n = 1000` does not overflow.

**Test values (the build must reproduce these).**
- `k = 4, n = 5`: Wald 44.9% to 115.1%; Wilson 37.6% to 96.4%.
- `k = 16, n = 20`: Wald 62.5% to 97.5%; Wilson 58.4% to 91.9%.
- `k = 800, n = 1000`: Wald 77.5% to 82.5%; Wilson 77.4% to 82.4%.
- `k = 5, n = 5`: Wald 100% to 100% (zero width, flag it); Wilson 56.6% to 100%.
- Exact coverage, `p = 0.6, n = 5`: Wald 83.5%, Wilson 99.0%. `p = 0.8, n = 5`: Wald 66.6%, Wilson 94.2%. `p = 0.05, n = 20`: Wald 63.9%, Wilson 92.5%. `p = 0.6, n = 100`: both 94.8%.

**First screen.** p = 60%, n = 5, method Simple, fixed seed. The right view already shows 100 intervals with roughly 16 orange misses, so the failure is visible before any interaction.
