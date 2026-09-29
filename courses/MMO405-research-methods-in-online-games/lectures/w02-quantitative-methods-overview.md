# MMO405 · Week 02 — Quantitative Methods Overview

**Why this matters:** Online games hand you samples that most researchers only dream of. With 40,000 players, almost any difference is statistically significant, so "significant" stops telling you anything about whether the difference matters. This week you learn to decide in advance how big an effect has to be before you care, and to read every quantitative study by its design and its effect size, not its p-value.

**You will be able to:**
- Place a quantitative study on a map of designs (cross-sectional, panel, experiment, natural experiment, trace data) and state the strongest claim each design supports.
- Compute a standardized effect size and its confidence interval, and classify a result into one of four verdicts using a smallest effect size of interest.
- Convert between `d`, `r` and `R²`, and explain a small effect in plain terms with the probability of superiority.
- Critique a published result from an online game by separating statistical significance, effect size and design.

**Before class:** Lakens, "Equivalence Tests: A Practical Primer for t Tests, Correlations, and Meta-Analyses" (2017), sections 1 to 3. Vuorre, Johannes, Magnusson and Przybylski (2022), sections 1 and 2 and figure 4. Drachen, Gagné and Seif El-Nasr, "Sampling for Game User Research," in *Game Analytics* (2013), pp. 143-167.

**Prerequisites from earlier courses:** [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error and confidence intervals). [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (z statistic, p-value, power). [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (minimum detectable effect, clustering). [MMO308 week 6, A/B testing statistics and pitfalls](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (peeking and multiple looks). [Week 1 of this course](w01-research-questions-in-game-studies.md) (claim types and the selection term).

**Interactive:** [examples/w02-significant-vs-meaningful.html](../examples/w02-significant-vs-meaningful.html). Keep it open during section 2.

---

## 1. A map of quantitative designs

Week 1 sorted questions by claim type. This week sorts the designs that answer them. The **design** of a study is what you vary, whom you measure, and when. It fixes the strongest claim you can make before you collect a single number. Statistics can only tell you how precise that claim is.

| Design | What happens | Strongest claim | Online-game example |
|---|---|---|---|
| Cross-sectional survey | Many people answer once | Descriptive, associational | Williams, Yee and Caplan (2008), 7,000 EverQuest II players on who plays and how much |
| Linked survey and telemetry, one wave | Survey answers joined to logged play for the same players | Associational, with a better behaviour measure | Johannes, Vuorre and Przybylski (2021), *Plants vs. Zombies* and *Animal Crossing* |
| Panel (longitudinal) | The same people measured several times | Associational within people over time; causal under stated assumptions | Vuorre et al. (2022), 38,935 players of seven games over six weeks |
| Randomized experiment | The researcher assigns conditions by chance | Causal | A studio A/B test (MMO308 weeks 5 and 6) |
| Natural experiment | Something outside the study assigns conditions nearly at random | Causal, if the "nearly" holds | Egami et al. (2024), console lotteries in Japan |
| Trace-data analysis | Logs or public records, no contact with players | Descriptive, associational | Ducheneaut et al. (2006), World of Warcraft census data (MMO305 week 2) |

Three distinctions do most of the work in this table.

- **Who assigns the condition.** If players choose (joining a guild, playing more), you have week 1's selection term. If a coin, a hash of the player ID or a retailer's lottery chooses, you don't.
- **Between people or within people.** A cross-sectional study compares different players with each other. A panel can compare each player with their own past. Vuorre et al. chose a within-person model for exactly this reason, because comparing a player with themselves removes stable differences between players.
- **Designed or found data.** A survey is designed: you chose every question. Telemetry is found: the studio logged it for its own purposes and you inherit its choices. Week 3 is about what that costs you.

### Levels of measurement

Every variable in your data has a level, and the level decides which summaries make sense.

- **Nominal**: categories with no order. Class, faction, server.
- **Ordinal**: ordered categories without equal spacing. Guild rank, a 5-point "how satisfied are you" item, league tier.
- **Interval**: equal spacing, no true zero. Rare in games. A standardized scale score is usually treated as interval.
- **Ratio**: equal spacing and a true zero. Hours played, gold earned, deaths per hour.

You can average hours played. You should hesitate before averaging guild ranks, because the gap from Member to Officer need not equal the gap from Officer to Leader. Week 4 returns to this for survey items, where many 5-point items are summed into a scale that behaves roughly like an interval measure.

## 2. Worked example: significant is not the same as big

### The hook: one hour a day, one ninth of a noticeable change

Vuorre and colleagues linked six weeks of play logs from seven publishers (*Animal Crossing: New Horizons*, *Apex Legends*, *EVE Online*, *Forza Horizon 4*, *Gran Turismo Sport*, *Outriders* and *The Crew 2*) with three waves of well-being surveys, 38,935 players in all. Before looking at the result, they fixed how large a change in well-being a person could actually notice, using an estimate from Anvari and Lakens (2021) that asked people to rate whether they felt different.

Their estimate was that one extra hour of play per day went with a change of about 0.03 units on their well-being scale. The noticeable threshold was about 0.26 units. So an average player would have to play about ten extra hours **per day** before the change would be noticeable, and the model put a 99% probability on the one-hour effect being too small to notice.

The year before, the same team had reported, from *Plants vs. Zombies: Battle for Neighborville* and *Animal Crossing* data, a positive and statistically significant association between logged play and well-being. Play time explained about 1% of the variance in well-being in each game (`R² = 0.01`). The paper's title called play "positively correlated with well-being." That was true. The question this section answers is whether it was big.

### The model

Compare two groups on a continuous outcome, such as a well-being score, with `n` players in each group.

```
d       = (mean_B − mean_A) / s          standardized difference (Cohen's d)
SE(d)  ≈ sqrt(2 / n)                     for small d and equal groups
95% CI  = d ± 1.96 × SE(d)               "is it different from zero?"
90% CI  = d ± 1.645 × SE(d)              "is it smaller than the SESOI?"
```

- `s` is the standard deviation of the outcome within groups. Dividing by it puts every outcome on one scale: "how many standard deviations apart are the group means?"
- `SE(d)` is the standard error you met in MA102 week 13, for a difference of two means measured in standard-deviation units. It shrinks with `sqrt(n)`, and `d` itself does not.
- The **SESOI** (smallest effect size of interest), written `Δ` (capital delta), is the smallest effect you would care about. You choose it **before** seeing the data, from what players could notice, what a design change is worth, or what theory predicts.

Two tests use the two intervals.

- The usual **significance test** from MA102 week 14 asks whether the 95% interval excludes zero.
- An **equivalence test** asks whether the 90% interval lies entirely inside `(−Δ, +Δ)`. If it does, the effect is smaller than anything you care about. Lakens (2017) explains why 90% goes with a 5% error rate here: the equivalence test is two one-sided tests, one at each bound, each at 5%. The procedure is called TOST.

Together they give **four verdicts**:

| Differs from 0? | Inside ±Δ? | Verdict |
|---|---|---|
| Yes | No | **Meaningful effect.** Real and big enough to matter. |
| No | Yes | **No meaningful effect.** Any effect is too small to care about. |
| Yes | Yes | **Real but trivial.** It exists, and it doesn't matter. |
| No | No | **Inconclusive.** You need more data. |

MA102 week 14 has the two-verdict version: significant or not. The equivalence test adds the second column, which is what lets you say "no meaningful effect" instead of the weaker "we found nothing."

### Numbers you can check

Suppose every study below observes the same difference, `d = 0.05`, with a SESOI of `Δ = 0.20`. Only the sample size changes. The last row is a larger effect for contrast.

| Observed d | n per group | SE(d) | p | 95% CI | 90% CI | Verdict |
|---|---|---|---|---|---|---|
| 0.05 | 100 | 0.1414 | 0.72 | −0.227 to +0.327 | −0.183 to +0.283 | Inconclusive |
| 0.05 | 1,000 | 0.0447 | 0.26 | −0.038 to +0.138 | −0.024 to +0.124 | No meaningful effect |
| 0.05 | 10,000 | 0.0141 | 0.00041 | +0.022 to +0.078 | +0.027 to +0.073 | Real but trivial |
| 0.05 | 100,000 | 0.0045 | < 10⁻²⁸ | +0.041 to +0.059 | +0.043 to +0.057 | Real but trivial |
| 0.30 | 1,000 | 0.0447 | 2 × 10⁻¹¹ | +0.212 to +0.388 | +0.226 to +0.374 | Meaningful effect |

Read down the first four rows. The effect never changes. The p-value falls from 0.72 to below 10⁻²⁸, and the verdict goes from "we can't tell" to "no effect worth caring about" to "real but trivial." A study of 100,000 players and a study of 1,000 reach the same practical conclusion. The larger one just says it with more decimal places.

The code below prints the table. It runs as shown with `.venv/bin/python`.

```python
# Four verdicts for an observed standardized difference d with n players per group.
from math import erf, sqrt

def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))

def verdict(d, n, sesoi):
    se = sqrt(2 / n)
    p = 2 * (1 - phi(abs(d) / se))
    lo95, hi95 = d - 1.96 * se, d + 1.96 * se      # for "different from zero?"
    lo90, hi90 = d - 1.645 * se, d + 1.645 * se    # for "smaller than the SESOI?"
    different = lo95 > 0 or hi95 < 0
    equivalent = -sesoi < lo90 and hi90 < sesoi
    label = {(True, False): "meaningful", (False, True): "no meaningful effect",
             (True, True): "real but trivial", (False, False): "inconclusive"}
    return se, p, (lo95, hi95), label[(different, equivalent)]

for d, n in [(0.05, 100), (0.05, 1_000), (0.05, 10_000), (0.05, 100_000), (0.30, 1_000)]:
    se, p, (lo, hi), v = verdict(d, n, sesoi=0.20)
    ptxt = f"{p:.2g}" if p > 1e-15 else "<1e-15"
    print(f"d={d:.2f} n={n:>7,}  SE={se:.4f}  p={ptxt}  95% CI [{lo:+.3f}, {hi:+.3f}]  {v}")
```

Output:

```
d=0.05 n=    100  SE=0.1414  p=0.72  95% CI [-0.227, +0.327]  inconclusive
d=0.05 n=  1,000  SE=0.0447  p=0.26  95% CI [-0.038, +0.138]  no meaningful effect
d=0.05 n= 10,000  SE=0.0141  p=0.00041  95% CI [+0.022, +0.078]  real but trivial
d=0.05 n=100,000  SE=0.0045  p=<1e-15  95% CI [+0.041, +0.059]  real but trivial
d=0.30 n=  1,000  SE=0.0447  p=2e-11  95% CI [+0.212, +0.388]  meaningful
```

(The exact p at 100,000 is about 5 × 10⁻²⁹. Floating-point arithmetic cannot compute `1 − Φ(z)` that small, so the code prints a floor.)

### What "d = 0.05" looks like

A standardized difference is hard to feel. Two translations help.

- **Probability of superiority.** Pick one player at random from each group. The chance that the player from the higher group scores higher is `Φ(d / √2)`. At `d = 0.05` that is 51.4%, barely better than a coin flip. At `d = 0.2` it is 55.6%, and at `d = 0.5` it is 63.8%.
- **Variance explained.** For two equal groups, `r = d / sqrt(d² + 4)`. At `d = 0.05`, `r = 0.025` and `R² = 0.0006`, so group membership explains 0.06% of the variation in the outcome. At `d = 0.2`, `R² ≈ 0.01`, the size of the Johannes et al. association.

### A visual you can move

Open [`examples/w02-significant-vs-meaningful.html`](../examples/w02-significant-vs-meaningful.html). The left view plots the 95% and 90% intervals on a number line with zero and the `±Δ` band shaded, plus the p-value in large type. The right view draws the two groups' distributions as overlapping bell curves, with the probability of superiority below.

Set `d = 0.05` and drag the sample size from 100 to 100,000. On the left, the interval shrinks to a sliver, moves off zero and the p-value collapses, and the verdict label changes three times. On the right, **nothing moves**. The two curves were almost on top of each other at 100 players and they still are at 100,000. Sample size changes how sure you are. It does not change what the players experience. Then drag `d` to 0.3 and watch the right view separate.

### Cross-context recognition

Rewrite each of these as "effect size, interval, SESOI" and the same judgment applies.

**EverQuest II, gender and hours (Williams, Yee and Caplan 2008).** Women in the sample played 29.31 hours a week and men 25.03, a difference the authors reported as `t = 7.33`, `p < .001`, `d = .18`. Highly significant. In our terms it is small: the probability of superiority is about 55%, so a randomly chosen woman out-played a randomly chosen man only slightly more often than not. It still mattered to the paper's argument, because the stereotype predicted a difference in the **other** direction. The sign carried the finding, and the size was modest. Whether a difference is meaningful depends on the question.

**Game time and well-being (Johannes et al. 2021).** With each extra 10 hours of play in two weeks, well-being rose by between 0.02 and 0.18 standard deviations in *Plants vs. Zombies* and between 0.03 and 0.09 in *Animal Crossing* (95% intervals). The authors did the SESOI reasoning after the fact. They noted that people may perceive changes of about a third of a standard deviation on a similar measure, which would take roughly three and a half hours of play in their data. Their follow-up (Vuorre et al. 2022) fixed the SESOI in advance.

**Console lotteries (Egami et al. 2024).** Winning a Switch lottery reduced psychological distress by about 0.18 standard deviations, with a 95% interval of 0.13 to 0.24. That is similar in size to the EverQuest II gender gap, and it came from a design that supports a causal claim. Same `d`, different claim type. Keep the two axes separate.

**A/B tests (MMO308 week 5).** The minimum detectable effect you computed there is the SESOI's twin. The SESOI says what you care about. The MDE says what your sample can see. Plan the sample so that `MDE ≤ Δ`. A 5,000-player test that cannot detect anything smaller than 8 points of retention is useless for a feature you expect to move retention by 2.

### Eyes-open design judgment

- **Choose the SESOI before the data.** Afterwards, every threshold looks like an argument for the result you got. Sources for a SESOI include what players can perceive (anchor-based, as in Vuorre et al.), what the effect is worth to the studio (a retention change that pays for the feature), and what competing theories predict.
- **With big data, the equivalence test is the interesting one.** In a telemetry study of 50,000 players, "significant" is almost guaranteed for any non-zero effect. The useful question is whether the interval sits inside or outside `±Δ`.
- **Prefer natural units when your reader has them.** Vuorre et al. reported unstandardized effects, "units of well-being per hour of play," because hours are something players and policymakers understand. A designer understands "0.4 more dungeon runs per week" better than "d = 0.12."
- **A SESOI is not a license to ignore small effects everywhere.** A 0.05 SD effect applied to millions of players, or repeated every day for years, can matter in total even when no single player notices it. Say which scale your SESOI refers to: the individual, the population, or the business.

### Check yourself (worked example)

1. A study of 400 players per group finds `d = 0.15` with `Δ = 0.20`. Compute the 95% and 90% intervals and give the verdict.
2. How many players per group would make the interval for `d = 0.15` narrow enough to classify it as "real but trivial" or "meaningful"? Explain why neither may happen.
3. Convert `d = 0.18` to `r` and to probability of superiority.

<details>
<summary>Answers</summary>

1. `SE = sqrt(2/400) = 0.0707`. 95% CI `0.15 ± 0.139 = 0.011 to 0.289`, which excludes 0. 90% CI `0.15 ± 0.116 = 0.034 to 0.266`, which crosses 0.20. Differs from zero, not inside `±Δ`, so the verdict is "meaningful" by the table. But the interval includes values below Δ, so a careful report says the effect is real and may or may not reach the SESOI.
2. For "real but trivial" the upper 90% bound must fall below 0.20: `0.15 + 1.645 × sqrt(2/n) < 0.20` gives `n > 2,165`. If the true effect is 0.15, a large study will converge on "real but trivial." If the true effect is above 0.20, it converges on "meaningful." An effect sitting close to Δ needs a very large sample to classify either way.
3. `r = 0.18 / sqrt(0.0324 + 4) = 0.0896`. Probability of superiority `Φ(0.18 / 1.414) = Φ(0.127) ≈ 0.551`.

</details>

## 3. Effect sizes you will meet

Papers report effects in many forms. Learn to translate them into one another and into something a designer can use.

| Measure | Meaning | Typical use | Convert |
|---|---|---|---|
| Difference in means (natural units) | "Guild members play 3.1 more hours a week" | Anything with a meaningful unit | — |
| Cohen's `d` | Difference in standard deviations | Scales, scores, comparisons across studies | `d = 2r / sqrt(1 − r²)` |
| Pearson `r` | Strength of linear association, −1 to 1 | Two continuous variables | `r = d / sqrt(d² + 4)` (equal groups) |
| `R²` | Share of variance explained | Regression summaries | `R² = r²` for one predictor |
| Risk difference | Difference in rates, in percentage points | Retention, conversion, churn | — |
| Risk ratio / odds ratio | Ratio of rates or odds | Rare events (bans, purchases) | Depends on the base rate |

Two warnings. First, "percentage points" and "percent" are different. Retention going from 20% to 22% is +2 points and +10%. Papers and dashboards mix them up often, so always say which one you mean. Second, Cohen's labels of 0.2 "small," 0.5 "medium" and 0.8 "large" were offered as a fallback for when nothing better is known. They are not a SESOI. In well-being research 0.2 may be meaningful. In a studio's retention test, 0.2 SD would be enormous.

### Uncertainty in the effect size itself

Every effect size needs an interval. For a correlation, the standard route is Fisher's transformation: `z = atanh(r)`, with standard error `1 / sqrt(n − 3)`. Build the interval on `z` and convert back with `tanh`. For `r = 0.10` and `n = 2,500`, `z = 0.1003 ± 1.96 × 0.0200`, which converts back to `0.061 to 0.139`. You will implement this in the lab.

## 4. Units, nesting and generalization

### Players inside groups

Players in online games are rarely independent. They sit inside guilds, servers, parties and matches, and players in the same group influence each other. MMO308 week 5 showed what this does to an A/B test: the **design effect** shrinks your effective sample toward the number of groups, not players. The same applies to observational research. A study of 10,000 players from 40 guilds has much less information about guild-level questions than 10,000 suggests. Before you compute a standard error, ask what the independent units are.

### Many games, not one

Vuorre et al. treated their seven games as a sample from the wider population of games. They estimated the effect separately in each game and then combined the estimates with a random-effects meta-analysis, a model that expects the true effect to differ somewhat from game to game. This matters for the claim. A result from one MMO is a result about that MMO. To say something about MMOs, you need several, and you need to report how much they disagree.

### Samples that answer the survey

Response rates in linked telemetry studies are low. Johannes et al. had about 0.21% of invited *Plants vs. Zombies* players and 1.75% of *Animal Crossing* players finish their survey. Vuorre et al.'s first-wave response ranged from 0.1% to 3.0% across games. Whoever answers is a selected group. UX201 week 12 and MMO308 week 10 covered who answers surveys and how to weight for it. For research, the rule is to state the response rate, compare responders to non-responders on anything the logs let you see, and phrase conclusions about the population you actually reached.

## 5. Researcher choices and preregistration

Between raw data and a published number sit dozens of choices: which sessions to drop, how to define an active player, which covariates to adjust for, which outcome to lead with. Each is defensible. Taken together, they give a researcher room to find a significant result in data with no real effect. MMO308 week 6 showed one version, peeking at an A/B test until it crosses the line. Choosing among outcomes and exclusions is the same problem spread over more choices.

The main defense is **preregistration**: writing the hypotheses, the SESOI, the exclusions and the analysis plan in a time-stamped public document before seeing the data. It does not forbid exploration. It marks which analyses were planned and which came later, so readers can weigh them differently.

Johannes et al. (2021) is an honest example of the other path. The authors wrote that their study was exploratory and that they made data-processing and analysis decisions without specifying them in advance. That statement does not make the paper wrong. It tells you to treat its effect sizes as leads for a planned study, which is how the 2022 follow-up treated them.

## In-class activity (25 minutes)

Groups of three. Each group receives three one-paragraph study summaries (from the instructor's set, drawn from recent game-research papers and studio blog posts).

1. **Place it (5 min).** Put each study on the section 1 design map and write its strongest supportable claim type.
2. **Size it (10 min).** For each, find or compute the effect size, convert it to probability of superiority, and write one plain-language sentence a designer would understand.
3. **Judge it (10 min).** Propose a SESOI for each question and justify it in one sentence. Using the reported interval, give the four-verdict classification. Where the paper's own conclusion is stronger than your verdict, write the sentence you would change.

Expected output: a 3 × 4 table (design, effect, SESOI, verdict) and at most three rewritten conclusion sentences.

## Common misconceptions

- **"p < 0.001 means a big effect."** The p-value mixes effect size and sample size. With 100,000 players per group, `d = 0.05` gives `p` below 10⁻²⁸ and a coin-flip probability of superiority.
- **"Not significant means no effect."** It means the interval includes zero. Only an equivalence test against a stated SESOI supports "no meaningful effect." At `n = 100` per group, the first row of the table cannot rule out effects as large as 0.33.
- **"Cohen's small, medium and large tell me what matters."** They were a fallback. Your SESOI comes from what players perceive or what the outcome is worth.
- **"More players means a better study."** More players shrink the interval around whatever the design measures, including its selection term. A 40,000-player cross-sectional study is precise about an association, not about a cause.

## Check yourself

1. For each, name the design and the strongest claim: (a) a studio emails 100,000 players, 1,500 answer a satisfaction survey, and the answers are compared with their logged spending; (b) a region receives a feature two months late because of localization, and its players' retention is compared with other regions; (c) a researcher reads six months of a game's public forum posts and counts complaint topics.
2. A telemetry study reports that players who use voice chat have well-being scores `d = 0.08` higher, 95% CI 0.05 to 0.11, `n = 18,000` in total. With `Δ = 0.15`, what is the verdict? Rewrite the headline "Voice chat boosts well-being" so it matches the evidence.
3. A correlation of `r = 0.10` is observed among 2,500 players. Compute the 95% interval with Fisher's `z`. Does it rule out `r = 0.15`?
4. Your team plans a 2,000-player study (1,000 per group) and sets `Δ = 0.10`. Can it ever return "no meaningful effect"? Show the arithmetic.

<details>
<summary>Answers</summary>

1. (a) Linked survey and telemetry, one wave; associational, with a selected sample of about 1.5%. (b) Natural experiment; causal if the late region is otherwise comparable, which you must argue. (c) Trace-data analysis of public text; descriptive.
2. The 90% interval is about 0.055 to 0.105, inside ±0.15, and the 95% interval excludes 0. Verdict "real but trivial" relative to your SESOI, and associational only. A fair headline: "Voice-chat users report slightly higher well-being; the difference is small and may reflect who chooses voice chat."
3. `z = atanh(0.10) = 0.1003`, `SE = 1/sqrt(2,497) = 0.0200`, interval `0.0611 to 0.1395` in z, which converts back to `r = 0.061 to 0.139`. The upper end is below 0.15, so yes, at the 95% level.
4. `SE = sqrt(2/1000) = 0.0447`, so the 90% half-width is `1.645 × 0.0447 = 0.0736`. The whole interval (width 0.147) fits inside (−0.10, +0.10) only if the observed `d` falls between −0.026 and +0.026. It can happen, but only when the observed effect is very close to zero. To make "no meaningful effect" a realistic outcome for a small true effect, plan a larger sample.

</details>

## Lab / assignment hook

[Lab 02, effect sizes and the four verdicts](../labs/lab02.md). You implement `d`, its intervals, the equivalence test and Fisher's `z` interval, run them on an invented dataset of 6,000 players from three servers, and write a 300-word results paragraph that a designer and a reviewer would both accept.

## Sources

- Vuorre, M., Johannes, N., Magnusson, K. & Przybylski, A. K. (2022). "Time spent playing video games is unlikely to impact well-being." *Royal Society Open Science* 9(7), 220411. https://doi.org/10.1098/rsos.220411. Seven games and publishers; 38,935 players; one hour per day ≈ 0.03 units; about 10 extra hours per day to notice (0.26 units); 99% probability too small to notice; unstandardized effects; games treated as a sample, random-effects meta-analysis; first-wave response 0.1% to 3.0% (data collected May to September 2021).
- Johannes, N., Vuorre, M. & Przybylski, A. K. (2021). "Video game play is positively correlated with well-being." *Royal Society Open Science* 8(2), 202049. https://doi.org/10.1098/rsos.202049. `R² = 0.01` in both games; 0.02-0.18 and 0.03-0.09 SD per 10 hours; about 3.5 hours for a perceivable change; response rates 0.21% and 1.75%; the statement that the study was exploratory.
- Anvari, F. & Lakens, D. (2021). "Using anchor-based methods to determine the smallest effect size of interest." *Journal of Experimental Social Psychology* 96, 104159. https://doi.org/10.1016/j.jesp.2021.104159.
- Lakens, D. (2017). "Equivalence Tests: A Practical Primer for t Tests, Correlations, and Meta-Analyses." *Social Psychological and Personality Science* 8(4), 355-362. https://doi.org/10.1177/1948550617697177. TOST, the 90% interval, and the four outcomes of combining significance and equivalence tests.
- Williams, D., Yee, N. & Caplan, S. E. (2008). "Who plays, how much, and why? Debunking the stereotypical gamer profile." *Journal of Computer-Mediated Communication* 13(4), 993-1018. https://doi.org/10.1111/j.1083-6101.2008.00428.x. EverQuest II; women 29.31 and men 25.03 hours per week, `t = 7.33`, `df = 6,722`, `d = .18` (p. 1002).
- Egami, H., Rahman, M. S., Yamamoto, T., Egami, C. & Wakabayashi, T. (2024). "Causal effect of video gaming on mental well-being in Japan 2020-2022." *Nature Human Behaviour* 8(10), 1943-1956. https://doi.org/10.1038/s41562-024-01948-y. Switch lottery effect on distress 0.18 s.d., 95% CI 0.13-0.24 (regression estimate).
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*, 407-416. https://doi.org/10.1145/1124772.1124834. Named here only as an example of trace-data design; details in MMO305 week 2.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum. The small, medium and large conventions and their intended use as a fallback.
- Drachen, A., Gagné, A. & Seif El-Nasr, M. (2013). "Sampling for Game User Research." In Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.), *Game Analytics*, pp. 143-167. Springer. https://doi.org/10.1007/978-1-4471-4769-5_9.

## Interactive spec: examples/w02-significant-vs-meaningful.html

**The one insight.** Growing the sample shrinks the interval and the p-value, and it changes nothing about how far apart the two groups of players are. Significance measures certainty. The effect size measures difference.

**Layout.** Two linked views side by side on desktop, stacked on mobile (interval view on top). A verdict badge sits between them.

- **Left view, "How sure are we?"** A horizontal number line for `d` from −0.5 to +0.8. Zero marked with a solid line. The band `(−Δ, +Δ)` shaded as "too small to matter." The 95% interval drawn as a thin bar with end caps and the 90% interval as a thicker bar on top, both centered on the observed `d` (a dot). Above the line, the p-value in large type, formatted to two significant figures while `p ≥ 10⁻⁴` (`0.72`, `0.00041`), as `m × 10⁻ᵏ` with a one-digit mantissa below that (`2 × 10⁻¹¹`), and as the upper bound `< 10⁻ᵏ` with `k = floor(−log10(p))` only when `z > 8`, where `log10 p` comes from the asymptotic normal tail below so it never shows 0. SE is shown to four decimals.
- **Right view, "What players experience."** Two normal density curves with SD 1, means 0 and `d`, drawn as outlines with 30% fill. Below them, "A random player from group B beats one from group A X% of the time," with X = probability of superiority to one decimal, and `r` and `R²` shown to three and four decimals.
- **Verdict badge.** One of the four verdicts from the lecture, with its row of the two-by-two table highlighted in a small inline table.

**Controls.**

| Control | Range | Step | Default | Scale |
|---|---|---|---|---|
| Observed effect `d` | −0.30 to +0.60 | 0.01 | 0.05 | linear |
| Players per group `n` | 20 to 200,000 | — | 100 | log slider; snap points at 100, 1,000, 10,000, 100,000 |
| SESOI `Δ` | 0.05 to 0.50 | 0.01 | 0.20 | linear |

Buttons: "Lecture rows" cycles through the five rows of the lecture table; "Reset." All controls keyboard accessible with visible numeric readouts.

**Formulas.**

```
SE = sqrt(2 / n)
z = |d| / SE ;  p = 2 × (1 − Φ(z))
for z > 8 use log10 p ≈ log10(2) + log10(φ(z)/z) where φ(z) = exp(−z²/2)/sqrt(2π)
CI95 = d ± 1.96 SE ;  CI90 = d ± 1.645 SE
different  = CI95 excludes 0
equivalent = −Δ < CI90.low and CI90.high < Δ
PS = Φ(d / sqrt(2))
r = d / sqrt(d² + 4) ;  R² = r²
```

Φ via an erfc approximation with small relative error in the tail, such as the Chebyshev form in Numerical Recipes (fractional error below 1.2 × 10⁻⁷). Abramowitz and Stegun 7.1.26 has a small absolute error but cannot resolve `p = 2 × 10⁻¹¹`.

**Test values** (Δ = 0.20).

| d | n | SE | p | CI95 | Verdict | PS |
|---|---|---|---|---|---|---|
| 0.05 | 100 | 0.1414 | 0.72 | −0.227 to +0.327 | Inconclusive | 51.4% |
| 0.05 | 1,000 | 0.0447 | 0.26 | −0.038 to +0.138 | No meaningful effect | 51.4% |
| 0.05 | 10,000 | 0.0141 | 0.00041 | +0.022 to +0.078 | Real but trivial | 51.4% |
| 0.05 | 100,000 | 0.0045 | < 10⁻²⁸ | +0.041 to +0.059 | Real but trivial | 51.4% |
| 0.30 | 1,000 | 0.0447 | 2 × 10⁻¹¹ | +0.212 to +0.388 | Meaningful | 58.4% |
| 0.15 | 400 | 0.0707 | 0.034 | +0.011 to +0.289 | Meaningful (interval crosses Δ; show the note "may be below SESOI") | 54.2% |

Show the note in the last row whenever the verdict is "meaningful" but CI90 includes values inside `±Δ`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The two curves use different line styles (solid and dashed) as well as color. A visually hidden live region announces the verdict and p-value when they change. Reduced motion: no transitions on the curves.
