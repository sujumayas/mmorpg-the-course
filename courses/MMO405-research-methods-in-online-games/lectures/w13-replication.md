# MMO405 · Week 13 — Replication

**Why this matters:** Your final paper will cite effects from earlier studies, and some of them are too big. That happens without anyone cheating. When journals and conferences mostly print results that cross `p < .05`, the printed effects from small studies come out inflated, and the next study to try the same thing finds less. This week you learn to predict how much less, to judge whether a replication "worked," and to plan one that can give a clear answer.

**You will be able to:**
- Compute the power of a study and the average effect a significance filter lets through, and explain why a replication of a small study should expect a smaller effect.
- Apply five replication criteria (significance, interval capture, small telescopes, equivalence, pooling) to one original and one replication, and explain why they disagree.
- Plan the sample size of a replication from the original study's sample size, and write a preregistration for it.
- Critique a replication of an online-game study for what changed between the two studies: the game version, the population, the platform and the measures.

**Before class:** Open Science Collaboration, "Estimating the reproducibility of psychological science" (2015), read the abstract, the introduction and the section on effect sizes (the free author copy is linked in Sources). Zendle and Cairns (2019), "Loot boxes are again linked to problem gambling: Results of a replication study," *PLOS ONE*, read the introduction and discussion (open access). Skim Hilgard, Engelhardt and Rouder (2017), the abstract and the general discussion.

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (power, false positives). [MMO308 week 6, A/B testing statistics and pitfalls](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (early winners overstate the effect, which is the same mechanism as this week's filter). [Week 2 of this course](w02-quantitative-methods-overview.md) (Cohen's `d`, `SE(d) = sqrt(2/n)`, the SESOI `Δ` and the equivalence test). [Week 5 of this course](w05-experiments-and-quasi-experiments.md) (threats to validity).

**Interactive:** [examples/w13-significance-filter.html](../examples/w13-significance-filter.html). Keep it open during section 2.

---

## 1. What a replication is

A **replication** is a new study that tests the same claim as an earlier one, with new data. It sits next to three related ideas, and people mix them up.

- **Reproduction** (or computational reproducibility): the same data and the same code give the same numbers. No new players, no new data. If a paper fails this, the problem is in the analysis, not the world.
- **Close replication** (also called direct): new participants, and as many of the original procedures, measures and analyses as you can keep. The question is "does the effect show up again when we do what they did?"
- **Conceptual replication**: new participants and deliberately different measures or procedures that should capture the same construct. The question is "does the claim hold beyond the specific setup?"
- **Robustness check**: the original data, analysed with other reasonable choices (another exclusion rule, another outcome definition). Week 2's section on researcher choices is the reason this matters.

No replication is exact. Time passes, the sample changes, the lab or the platform changes. Online games add a problem most sciences don't have. **The object of study itself changes.** A study run on a game in 2021 and repeated in 2026 is studying a game that has been patched dozens of times, whose population has turned over, and whose players now know things (build guides, meta strategies, community norms) that the first sample did not. When a replication in a live game finds less, there are always two stories. Either the first result was inflated, or the world moved. This lecture gives you a way to tell them apart.

### Why this became a field

In 2015 the Open Science Collaboration, 270 authors coordinated by the Center for Open Science, published close replications of 100 studies from three psychology journals, using high-powered designs and the original materials where they could get them. Their headline numbers:

- 97% of the original studies had reported a significant result. 36% of the replications did.
- The mean effect size, expressed as a correlation, fell from 0.403 in the originals to 0.197 in the replications. Replication effects were about half the size.
- 47% of original effect sizes fell inside the 95% interval of the replication.
- 39% of the effects were subjectively rated as replicated by the replication teams.

Two things in that list matter for this week. First, the effects shrank on average, even for studies that "replicated." Second, the criteria gave different answers (36%, 47%, 39%), because they ask different questions. Section 2 explains the shrinkage. Section 3 explains the disagreement.

## 2. Worked example: why replications come in smaller

### The hook: two game findings, two fates

In 2010, Anderson and colleagues published a large meta-analysis in *Psychological Bulletin* concluding that violent video games increase aggressive thoughts, feelings and behaviour, and argued that publication bias in that literature was small. In 2017, Hilgard, Engelhardt and Rouder reanalysed the same studies with a wider set of bias-detection methods. They found substantial publication bias in the experimental studies of aggressive affect and behaviour. After adjusting for it, the estimated effect of violent games on aggressive behaviour in experiments was very small. Experiments that met the original authors' own quality criteria showed more signs of bias, not larger effects. Two years later, Przybylski and Weinstein ran a preregistered study of 1,004 British 14- and 15-year-olds and their carers, published as a registered report, and found no evidence that recent violent game play was linked to carer-rated aggression.

Now the other case. In 2018, Zendle and Cairns surveyed 7,422 gamers recruited through Reddit and found that loot box spending was linked to problem gambling severity, with an effect size of `η² = 0.054`. In 2019 they repeated the study with 1,172 gamers recruited on Amazon Mechanical Turk, a different platform with a different population. The replication found `η² = 0.051`. The authors noted that both the direction and the size lined up closely with the first study.

Why did one literature shrink and the other hold? The model below says you could have predicted much of the difference from one number per study: its power.

### The model

Imagine a true effect `δ` (a standardized difference, week 2's `d`). Many research teams study it, each with `n` players per group. Each team's estimate `d̂` scatters around `δ` with the standard error from week 2:

```
SE    = sqrt(2 / n)                         standard error of d with n per group
power = 1 − Φ(1.96 − δ/SE)                  chance a study finds d̂ > 1.96·SE
a     = 1.96 − δ/SE                         the publication cut-off, in SE units from δ
E[published d̂] = δ + SE × φ(a) / (1 − Φ(a))   mean of the studies that pass the filter
exaggeration = E[published d̂] / δ
```

- `Φ` is the standard normal cumulative distribution and `φ` its density, both from MA102.
- The **significance filter** is the rule "a study reaches print only if its estimate is significant in the predicted direction." Real publishing is not that strict, but it leans that way.
- **Power** is the share of studies that pass the filter, which MA102 week 14 defined as the chance of detecting a true effect.
- The last formula is the mean of a normal distribution cut off below at `1.96·SE`. You don't need to derive it. Its meaning is simple: if only the top slice of the scatter gets printed, the printed average sits above the truth, and the smaller the slice, the further above.
- The **exaggeration ratio** (Gelman and Carlin call it the type M error) says how many times too big the published average is.

A replication has no filter. It gets printed whatever it finds. So its expected estimate is `δ`, and the gap between the original and the replication is, on average, the exaggeration.

### Numbers you can check

Set the true effect at `δ = 0.20`, a size that week 2 showed is common in game and well-being research. Vary the sample.

| n per group | SE | Power | Mean published d | Exaggeration |
|---|---|---|---|---|
| 20 | 0.316 | 9.2% | 0.767 | 3.84× |
| 50 | 0.200 | 16.9% | 0.499 | 2.49× |
| 100 | 0.141 | 29.3% | 0.366 | 1.83× |
| 200 | 0.100 | 51.6% | 0.277 | 1.39× |
| 400 | 0.071 | 80.7% | 0.224 | 1.12× |
| 1,000 | 0.045 | 99.4% | 0.201 | 1.00× |

Check the `n = 50` row by hand. `SE = sqrt(2/50) = 0.2`, so `δ/SE = 1` and `a = 0.96`. `Φ(0.96) ≈ 0.831`, so power is about 16.9%. `φ(0.96) ≈ 0.252`, and `0.252 / 0.169 ≈ 1.49`. The published mean is `0.20 + 0.2 × 1.49 ≈ 0.499`. A literature of 50-per-group studies of a real 0.2 effect prints an average of about 0.5, a "medium" effect by Cohen's labels, and a careful replication will find a quarter of a standard deviation less.

Look at the middle of the table. An exaggeration of 2, the Open Science Collaboration's halving, falls between the `n = 50` and `n = 100` rows. Solving the model for it gives originals with about 25% power (24% for their exact ratio, 0.403 / 0.197 = 2.05). At 17% power, the `n = 50` row, the model predicts shrinkage by 2.5 times, more than they saw. Now look at the bottom. When the original study had high power, almost every run passes the filter, so the filter has nothing to select, and the published average is honest. The loot box study had 7,422 respondents. Its power to detect an effect of the size it found was close to 100%, so there was little room for inflation, and the replication found the same size. That is the prediction in one sentence: **the smaller the original's power, the more its replication should shrink.**

The code prints the table, then checks the `n = 50` row by brute force. Both run as shown with `.venv/bin/python`.

```python
# The significance filter: what a literature that publishes only "significant" results reports.
from math import erf, exp, pi, sqrt

def phi(z):            # standard normal cumulative distribution
    return 0.5 * (1 + erf(z / sqrt(2)))

def pdf(z):            # standard normal density
    return exp(-z * z / 2) / sqrt(2 * pi)

def filtered(delta, n):
    se = sqrt(2 / n)
    a = 1.96 - delta / se              # the cut-off, in SE units from the true effect
    power = 1 - phi(a)
    published = delta + se * pdf(a) / (1 - phi(a))
    return se, power, published

print(" n/group     SE   power  mean published d  exaggeration")
for n in [20, 50, 100, 200, 400, 1000]:
    se, power, pub = filtered(0.20, n)
    print(f"{n:>8,}  {se:.3f}  {power:5.1%}  {pub:16.3f}  {pub / 0.20:11.2f}x")
```

Output:

```
 n/group     SE   power  mean published d  exaggeration
      20  0.316   9.2%             0.767         3.84x
      50  0.200  16.9%             0.499         2.49x
     100  0.141  29.3%             0.366         1.83x
     200  0.100  51.6%             0.277         1.39x
     400  0.071  80.7%             0.224         1.12x
   1,000  0.045  99.4%             0.201         1.00x
```

```python
# Check the formula by brute force: run 20,000 studies of 50 players per group, publish the significant ones.
import random
from math import sqrt

random.seed(13)
delta, n = 0.20, 50
se = sqrt(2 / n)
runs = [random.gauss(delta, se) for _ in range(20_000)]
published = [d for d in runs if d > 1.96 * se]
print(f"published {len(published):,} of 20,000 ({len(published) / 20_000:.1%})")
print(f"mean published d = {sum(published) / len(published):.3f}")
```

Output:

```
published 3,414 of 20,000 (17.1%)
mean published d = 0.498
```

The simulation agrees with the formula to within its own noise: 17.1% against 16.9%, and 0.498 against 0.499.

### A visual you can move

Open [`examples/w13-significance-filter.html`](../examples/w13-significance-filter.html). The left view, "Every study that was run," shows 200 simulated studies as dots on a number line of `d̂`. A vertical line marks the significance cut-off `1.96·SE`. Dots to the right of it are filled (published), dots to the left are hollow (in the file drawer). A marker shows the true `δ` and another the mean of the filled dots. The right view, "What the next study finds," shows the published mean as a bar, the replication's expected estimate `δ` as a second bar, and the replication's 95% interval.

Start at `δ = 0.2` and `n = 50`. On the left, the filled dots form a small cluster far to the right of the true effect. On the right, the published bar is two and a half times the replication bar. Now drag `n` up to 400. The cut-off line slides left past most of the dots, nearly all of them fill, the published mean falls onto `δ`, and the two bars on the right become equal. The data did not get more honest. The filter stopped having anything to throw away. Then set `δ = 0` and `n = 50`. About 2.5% of dots still pass the one-sided filter, and their mean sits near 0.47. A literature built from those would report a "medium" effect of nothing.

### Cross-context recognition

Rewrite each case as "power of the original, filter, expected shrinkage," and it is the same idea.

**Violent games experiments (Hilgard et al. 2017).** Many of the laboratory experiments in the 2010 meta-analysis were small. Small studies plus a literature that favoured significant results is the top of the table. Bias adjustments of the kind Hilgard and colleagues applied are statistical ways of subtracting the filter. One family, meta-regression methods such as PET-PEESE (Stanley and Doucouliagos 2014), regresses each study's effect on its standard error and reads off what a study with zero standard error would find. The cross-sectional correlations looked largely unbiased in their reanalysis, which is what the bottom of the table predicts for studies that are larger or less filtered.

**Loot boxes and problem gambling (Zendle and Cairns 2018, 2019).** A 7,422-person original leaves the filter nothing to do. The replication moved to a different platform with a different population and a sample one sixth the size, and the effect held (`η² = 0.054` then `0.051`). This was also a partly conceptual replication, because the people changed. A result that survives a change of population is stronger evidence than one that survives only a repeat on the same forum.

**Early-stopped A/B tests (MMO308 week 6).** A live-ops team that stops a test on the first day it turns green has applied a significance filter to its own experiment. The effect at the stopping point is biased upward for the same reason as the table's middle rows, and the launched feature "underperforms" its test. Same mechanism, different room.

**The research literature of the 2010s.** The Open Science Collaboration's halving (0.403 to 0.197) is what the model predicts for originals with power around 25%. The real originals varied in power and in true effect, so this is a consistency check, not an estimate. It shows that the filter alone can produce shrinkage of the size they saw, without any fraud.

### Eyes-open design judgment

- **Discount small published effects before you use them.** When you plan a study from a published effect, ask the original's power. If it was low, plan for an effect about half the size or less. Planning from the published number is how the next underpowered study gets run.
- **A shrinking effect is not proof that the original was wrong.** In the `n = 50` row, the true effect is 0.2, and it is real. The replication will find something near 0.2, which is smaller than 0.5 and not zero. "Smaller" and "absent" are different verdicts. Section 3 separates them.
- **In a live game, check whether the world moved.** The filter predicts shrinkage in proportion to the original's low power. A patch, a population change or a platform change predicts differences that are unrelated to power, and often shows up in the descriptive statistics (session length, class mix, spend distribution) before it shows up in the effect. Report those descriptives for both samples side by side.
- **Big data does not save you from the filter.** It saves each individual study from it. A literature of large telemetry studies can still be filtered if researchers try many outcomes and report the one that worked. That is week 2's researcher-choices problem, and preregistration is its fix.

### Check yourself (worked example)

1. A study of 100 players per group finds `d = 0.40, p = .005`. If the true effect were 0.20, what was its power, and what published effect would you expect on average from studies like it?
2. You want to replicate it. What effect should you plan for, and roughly how many players per group give 80% power for that effect in a two-sided test at `α = .05`?
3. Why does raising the original's sample size make the exaggeration ratio fall toward 1, even though the true effect never changes?

<details>
<summary>Answers</summary>

1. From the table, power 29.3% and mean published `d` 0.366. The observed 0.40 is in line with a true 0.2 that passed the filter.
2. Plan for 0.2 or less. `n ≈ 2 × ((1.96 + 0.8416) / 0.2)² = 2 × 196.2 = 392.4`, so 393 per group, about 400.
3. The filter only raises the average by dropping the studies below the cut-off. With high power there are almost none below the cut-off, so the published set is almost the whole set, and its average is `δ`.

</details>

## 3. Did it replicate? Five criteria that disagree

Take one invented case that matches the table. A 2021 study of an MMO's onboarding quest (the original) reported `d = 0.48` in 30-day guild membership between players who got a mentor NPC and players who didn't, with 50 players per group (`SE = 0.2`, `p = .016`). In 2025 a team repeats it with 250 per group (`SE = 0.089`) and finds `d = 0.12`. Did it replicate? Five criteria in use today give five answers.

| Criterion | Question it asks | Computation | Answer |
|---|---|---|---|
| 1. Significance and sign | Did the replication also reach `p < .05` in the same direction? | `z = 0.12 / 0.089 = 1.34`, `p = .18` | No |
| 2. Interval capture | Is the original estimate inside the replication's 95% interval? | `0.12 ± 0.175 = −0.055 to +0.295` | No, 0.48 is outside |
| 3. Small telescopes | Is the replication smaller than an effect the original could have seen? | `d33 = 0.304`, one-sided `p = .020` | Yes, the effect is too small for the original to have detected |
| 4. Equivalence (week 2) | Is the effect inside `±Δ` with `Δ = 0.20`? | 90% interval `−0.027 to +0.267` | Not inside, so not shown to be negligible |
| 5. Pooling | What do both studies say together? | weighted mean `0.180`, `p = .027` | A small positive effect |

Each criterion needs a line of explanation.

**Significance and sign** is the most common and the weakest. A replication can fail it because the effect is absent or because the replication was too small. It can pass it with an effect a tenth the original's size. It treats `p = .049` and `p = .051` as opposite results.

**Interval capture** asks whether the original's number is plausible given the replication. It fails here because 0.48 is implausible, which the filter predicted. It says nothing about whether the effect exists.

**Small telescopes** (Simonsohn 2015) asks a sharper question: is the effect big enough that the original study could have seen it? Define `d33` as the effect size that would have given the original 33% power, a study that was unlikely but not hopeless to detect it:

```
d33 = (1.96 − z_0.67) × SE_original = (1.96 − 0.440) × 0.2 = 0.304
```

Then test whether the replication estimate is significantly below `d33` (one-sided): `z = (0.12 − 0.304) / 0.089 = −2.06`, `p = .020`. The verdict is that the original study was a telescope too small to see whatever effect exists. That does not say the effect is zero. It says the original's evidence could not have been about an effect this size. Note the result in our invented world: the true effect is 0.2, and small telescopes correctly says the original study could not have found it reliably.

**Equivalence** is week 2's test, and it asks whether the effect is too small to matter by your SESOI. Here it is inconclusive, because the interval still reaches 0.267. The replication cannot rule out an effect that matters.

**Pooling** combines both estimates, weighted by precision (`1/SE²`: 25 for the original, 125 for the replication), into `0.180 ± 0.160`. This is the right move only if you believe the original is unbiased. If the original passed a filter, pooling carries its exaggeration into the combined number. The Open Science Collaboration reported that 68% of effects were significant after combining original and replication, and they said explicitly that this figure assumes no bias in the originals.

The disagreement is the lesson. **"Did it replicate?" is five questions.** In your paper, state which one you are asking, and report the replication's effect size and interval so a reader can apply the others.

### Planning a replication that can answer

Small telescopes also gives a planning rule. If the true effect were zero, how big must the replication be to reject `d33` with 80% power? With the normal approximation:

```
SE_rep = d33 / (1.645 + 0.842)        one-sided α = .05, power .80
n_rep / n_original = (2.487 / 1.520)² ≈ 2.7
```

Simonsohn's rule of thumb is about 2.5 times the original sample. At 125 per group (2.5 × 50), the replication has about 78% power to reject `d33` if the effect is zero. Our 250-per-group replication had about 96%. If you want the replication to detect the effect itself, plan instead from a discounted effect, as in question 2 above, which here needs about 400 per group.

## 4. Doing a replication in an online game

### Decide what must stay the same

Write down, before anything else, what the original's claim was, and which features of the original are part of that claim. For the loot box studies, the claim was about a link between spending and gambling problems among gamers, so the measure of problem gambling had to stay the same and the recruitment platform did not. For a study about a specific raid mechanic, the mechanic is the claim, and a patch that changed it makes a close replication impossible. Then you are running a conceptual replication and should say so.

The usual checklist, adapted to online games:

- **Game version.** Record the patch or build for both studies. If the relevant system changed, describe the change in the methods.
- **Population.** Region, server type, account age, and how players were recruited. A Reddit sample and an MTurk sample differ in who plays what and how much.
- **Measures.** Use the same instrument, in the same language version, scored the same way. Week 4 showed how easily a scale's structure differs between samples. Check the structure again in yours.
- **Telemetry definitions.** "Active," "session" and "guild member" are definitions in someone's code. Week 3 covered how they drift. Get the original definitions in writing.
- **Analysis.** Run the original analysis exactly, then your preferred analysis, and report both.

### Preregister, and consider a registered report

Preregistration (week 2) matters more for a replication than for an original, because the replication's value is that the reader knows its analysis was fixed in advance. A **registered report** goes further. The journal reviews the introduction and methods before the data exist and commits to publishing the result whatever it is. That removes the filter at the level of the journal. Przybylski and Weinstein's violent games study was published this way in *Royal Society Open Science*. A registered report is the direct answer to this week's model, because a study accepted before its results cannot be selected for them.

### Contact the original authors

Ask for materials, code, exact item wording and any unreported details. Most researchers help. Record what you asked and what you received, and say in the paper which differences remain. Treat the original authors as colleagues who know things about the study you don't, not as defendants.

### Data you cannot share

Reproduction needs the data, and telemetry often cannot leave the studio. Telemetry tied to player accounts is usually personal data under the EU's GDPR and similar laws, the studio's agreement with you may forbid sharing, and your consent forms (week 10) may not have asked players about sharing. Options that keep a study checkable:

- Share the **analysis code** with a small **synthetic dataset** that has the same columns and similar distributions, so a reader can run every step.
- Share **aggregates** that are enough to recompute the key numbers (group means, SDs, counts per cell).
- Arrange **controlled access**: the data stay with the studio or a data archive, and a named replicator can apply to use them.
- Ask for consent to share de-identified data at the start, in the consent form, not afterwards.

Whatever you choose, say it in a data availability statement. "Data available on request" with no route to actually get them is not a plan.

## In-class activity (25 minutes)

Groups of three. Each group gets one invented original study summary (effect size, sample size, recruitment, game version) and one replication summary from the instructor's set.

1. **Predict (5 min).** From the original's sample size alone, estimate its power for a true effect half its published size, and read off the expected exaggeration from the table or the interactive.
2. **Judge (10 min).** Apply all five criteria from section 3 to the pair. Put the answers in a five-row table.
3. **Explain (10 min).** List every difference between the two studies (version, population, platform, measure, analysis). Decide whether the gap between the effects is better explained by the filter or by a change in the world, and write two sentences defending your choice.

Expected output: the five-row table and the two sentences. Two groups with the same pair compare verdicts at the end.

## Common misconceptions

- **"A failed replication means the original was fraud or error."** The filter inflates honest small studies. In the `n = 50` row of the table, an honest original with a real effect reports 2.5 times the truth on average.
- **"The replication didn't reach significance, so the effect is zero."** Non-significance can mean an underpowered replication. Small telescopes and equivalence tests are how you say something stronger, and they need planned sample sizes.
- **"If the replication is significant, the original is confirmed."** A significant replication at a quarter of the original's size contradicts the original's size. Report both numbers.
- **"Pooling original and replication gives the best estimate."** Only if the original was not filtered. If it was, the pooled estimate inherits the inflation.

## Check yourself

1. An original study with 30 players per group reports `d = 0.62`. Compute `d33` for it. A replication with 150 per group finds `d = 0.10`. Apply the small-telescopes test.
2. A replication of a 2019 MMO study finds the same direction but one third of the effect. The original had 200 players per group. Between 2019 and the replication, the game's matchmaking was rebuilt. Using the table, how much shrinkage would the filter predict for a true effect of 0.2, and what does that suggest about the matchmaking change?
3. Your team has 12 months of telemetry that a studio will not let you publish. Write a data availability statement that lets a reviewer reproduce your main table.
4. Two replications of the same original report `d = 0.18 (95% CI 0.02 to 0.34)` and `d = 0.08 (95% CI −0.08 to 0.24)`. A blog post says "one replicated and one failed." Rewrite that sentence so it matches the evidence.

<details>
<summary>Answers</summary>

1. `SE_o = sqrt(2/30) = 0.258`, so `d33 = 1.520 × 0.258 = 0.392`. `SE_r = sqrt(2/150) = 0.115`. `z = (0.10 − 0.392) / 0.115 = −2.53`, one-sided `p ≈ .006`. The replication rejects `d33`: the original was too small a telescope to have detected an effect of the size that exists, if one does.
2. At 200 per group the table predicts about 1.39× inflation, so a replication should find roughly 70% of the original. Finding a third is much more shrinkage than the filter explains, so the change in the world (the matchmaking rebuild) is a serious candidate. Compare descriptive statistics of the two samples and describe the matchmaking change in the paper.
3. One good answer: "The telemetry belongs to [studio] and cannot be shared under our data agreement. We publish the analysis code, a synthetic dataset of 5,000 rows with the same columns and matched marginal distributions, and the cell counts, means and standard deviations needed to recompute Table 2. Qualified researchers may apply to [studio] for controlled access under the same agreement." It must name what is shared and how access works.
4. The two intervals overlap heavily and both include values around 0.1 to 0.2. A fair sentence: "Two replications found smaller effects than the original (0.18 and 0.08). Their intervals overlap, so they do not disagree with each other; together they point to a small effect, well below the original estimate."

</details>

## Lab / assignment hook

[Lab 13, a replication audit](../labs/lab13.md). You implement the power, filter and five-criteria functions, run them on 12 invented original and replication pairs from game research, and write a one-page replication plan for one study you cite in your final paper, with the sample size from section 3 and a preregistration outline.

## Sources

- Open Science Collaboration (2015). "Estimating the reproducibility of psychological science." *Science* 349(6251), aac4716. https://doi.org/10.1126/science.aac4716. Author copy: https://research.rug.nl/files/87923937/PSYCHOLOGY._Estimating_the_reproducibility_of_psychological_science.pdf. 100 replications from three journals; 97% vs 36% significant; mean effect r 0.403 (SD 0.188) vs 0.197 (SD 0.257); 47% of original effects inside the replication 95% CI; 39% subjectively replicated; 68% significant after combining, assuming no bias.
- Zendle, D. & Cairns, P. (2018). "Video game loot boxes are linked to problem gambling: Results of a large-scale survey." *PLOS ONE* 13(11), e0206767. https://doi.org/10.1371/journal.pone.0206767. N = 7,422, recruited through gaming subreddits; η² = 0.054.
- Zendle, D. & Cairns, P. (2019). "Loot boxes are again linked to problem gambling: Results of a replication study." *PLOS ONE* 14(3), e0213194. https://doi.org/10.1371/journal.pone.0213194. N = 1,172 on Amazon Mechanical Turk; η² = 0.051; effect sizes described as closely aligned with the original.
- Anderson, C. A., Shibuya, A., Ihori, N., Swing, E. L., Bushman, B. J., Sakamoto, A., Rothstein, H. R. & Saleem, M. (2010). "Violent video game effects on aggression, empathy, and prosocial behavior in Eastern and Western countries: A meta-analytic review." *Psychological Bulletin* 136(2), 151-173. https://doi.org/10.1037/a0018251.
- Hilgard, J., Engelhardt, C. R. & Rouder, J. N. (2017). "Overstated evidence for short-term effects of violent games on affect and behavior: A reanalysis of Anderson et al. (2010)." *Psychological Bulletin* 143(7), 757-774. https://doi.org/10.1037/bul0000074. Substantial publication bias in experiments; very small adjusted effect on aggressive behaviour; cross-sectional correlations largely unbiased; best-practice experiments showed more signs of bias.
- Przybylski, A. K. & Weinstein, N. (2019). "Violent video game engagement is not associated with adolescents' aggressive behaviour: evidence from a registered report." *Royal Society Open Science* 6(2), 171474. https://doi.org/10.1098/rsos.171474. n = 1,004 adolescents aged 14-15 and their carers; preregistered analysis; no support for the predicted relationship.
- Simonsohn, U. (2015). "Small Telescopes: Detectability and the Evaluation of Replication Results." *Psychological Science* 26(5), 559-569. https://doi.org/10.1177/0956797614567341. `d33`, the one-sided test against it, and the rule of thumb in the section "Replication sample size = 2.5 × original sample size" (if the true effect is zero, 2.5 times the original sample gives about 80% power to reject `d33`). Checked against the OnlineFirst PDF (23 March 2015) archived by the Internet Archive from datacolada.org, September 2026.
- Gelman, A. & Carlin, J. (2014). "Beyond Power Calculations: Assessing Type S (Sign) and Type M (Magnitude) Errors." *Perspectives on Psychological Science* 9(6), 641-651. https://doi.org/10.1177/1745691614551642. The exaggeration ratio (type M error).
- Stanley, T. D. & Doucouliagos, H. (2014). "Meta-regression approximations to reduce publication selection bias." *Research Synthesis Methods* 5(1), 60-78. https://doi.org/10.1002/jrsm.1095. PET-PEESE meta-regression adjustment for publication selection.

## Interactive spec: examples/w13-significance-filter.html

**The one insight.** When only significant results get printed, small studies of a real effect print an average that is several times too big, and a replication finds the truth. Raising the original's sample size removes the gap, because the filter then has nothing to throw away.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view on top). A summary strip above both shows power, mean published `d`, and exaggeration ratio in large type.

- **Left view, "Every study that was run."** A horizontal number line for `d̂` from −0.6 to +1.2, ticks every 0.2. 200 simulated studies drawn as dots in a beeswarm (or jittered strip) above the line. A vertical line at `c = 1.96·SE` labelled "significant". Dots with `d̂ > c` filled in the accent color ("published"); others hollow grey ("file drawer"). A triangle marker below the axis at the true `δ` ("truth") and a second marker at the mean of the filled dots ("published average"). Counter: "published k of 200".
- **Right view, "What the next study finds."** Two horizontal bars on a shared axis from 0 to 1.2: "published average" (analytic `E[published d̂]`, not the simulated mean) and "replication expects" (= `δ`). Below them, the replication's 95% interval `δ ± 1.96·sqrt(2/n_rep)` as a bar with end caps, and the replication's power to detect `δ` (two-sided) as a percentage.
- Under the right view, a sentence that updates: "A replication with n_rep per group should find about X, which is Y% of the published average."

**Controls.**

| Control | Range | Step | Default | Scale |
|---|---|---|---|---|
| True effect `δ` | 0.00 to 0.60 | 0.01 | 0.20 | linear |
| Original players per group `n` | 10 to 2,000 | — | 50 | log slider; snap points at 20, 50, 100, 200, 400, 1,000 |
| Replication players per group `n_rep` | 10 to 5,000 | — | 250 | log slider |

Buttons: "Lecture rows" cycles `n` through 20, 50, 100, 200, 400, 1,000 with `δ = 0.20`; "New draw" re-samples the 200 dots with a new seed; "Null effect" sets `δ = 0`; "Reset". All controls keyboard accessible with numeric readouts. Respect `prefers-reduced-motion` (no dot animation, instant redraw).

**Formulas.**

```
SE    = sqrt(2 / n)
c     = 1.96 × SE
a     = 1.96 − δ / SE
power = 1 − Φ(a)
E_pub = δ + SE × φ(a) / (1 − Φ(a))
exaggeration = E_pub / δ         (show "∞" or "no true effect" when δ = 0)
dots: d̂_i = δ + SE × z_i, z_i standard normal from a seeded PRNG (e.g. mulberry32 + Box-Muller)
SE_rep = sqrt(2 / n_rep); rep interval = δ ± 1.96 × SE_rep
rep power (two-sided) = 1 − Φ(1.96 − δ/SE_rep) + Φ(−1.96 − δ/SE_rep)
```

Use an accurate `Φ` (for example the Abramowitz-Stegun 26.2.17 approximation or an erf series) and compute `1 − Φ(a)` directly as the upper tail for large `a`, so power near 0 does not become exactly 0 and `E_pub` stays finite. For `δ = 0` show `E_pub` and label exaggeration "no true effect."

**Test values** (δ = 0.20; these must match the lecture table to the shown decimals).

| n | SE | power | E_pub | exaggeration |
|---|---|---|---|---|
| 20 | 0.316 | 9.2% | 0.767 | 3.84× |
| 50 | 0.200 | 16.9% | 0.499 | 2.49× |
| 100 | 0.141 | 29.3% | 0.366 | 1.83× |
| 200 | 0.100 | 51.6% | 0.277 | 1.39× |
| 400 | 0.071 | 80.7% | 0.224 | 1.12× |
| 1,000 | 0.045 | 99.4% | 0.201 | 1.00× |

Extra checks. `δ = 0, n = 50`: power 2.5%, `E_pub = 0.468` (`0.2 × φ(1.96) / (1 − Φ(1.96)) = 0.2 × 0.05844 / 0.02500 = 0.46757`). `δ = 0.20, n_rep = 250`: replication interval 0.025 to 0.375, replication power 60.9%.

**Palette and accessibility.** Use `templates/interactive-tokens.css` inline. Filled vs hollow dots must differ by shape fill, not only color. Every number in the summary strip is live text, not canvas pixels, so students can copy it.
