# MMO308 · Week 07 — Segmentation

**Why this matters:** Every live-game KPI is an average over different kinds of players. When the mix of players changes, the average moves even if nobody's behavior changed, and teams have cut good features and shipped bad ones because they read a mix change as a quality change. This week you learn to split a number into segments, tell a mix effect from a real change, and choose segments that stand up to the statistics you learned in MA102.

**You will be able to:**
- Compute an overall rate as a weighted mean of segment rates, and decompose a change in it into a mix effect and a rate effect.
- Recognize the same mix-versus-rate structure in a price index, an admissions table and a retention dashboard.
- Design a segmentation scheme from attributes known before a change, and compute the margin of error each segment can support.
- Critique a segment-level A/B readout for multiple comparisons and for segments defined after the treatment.

**Before class:** Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics* (2013), the chapter on game data mining (Drachen et al.), the sections on clustering players. Skim the Wikipedia article "Simpson's paradox", the sections on UC Berkeley admissions and the kidney stone study. Reread your DB201 week 12 notes on KPI definitions.

**Prerequisites from earlier courses:** [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (DAU, Dn retention, cohorts, and the idea that a KPI is a definition). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the margin of error of a rate). [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives and multiple comparisons). [MMO304 week 12, economic telemetry](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (price indices). Retention cohorts come from [MMO308 week 3](w03-cohorts-and-retention-curves.md) and A/B statistics from [week 6](w06-ab-testing-statistics-and-pitfalls.md).

**Interactive:** [w07-segment-mix.html](../examples/w07-segment-mix.html). Keep it open during section 2.

---

## 1. One number, many kinds of player

A **segment** is a group of players defined by a rule, such as "accounts created on mobile" or "players who have spent money at least once". **Segmentation** is the act of splitting a population into segments so you can read a metric for each group separately. A good scheme is **exhaustive** (every player lands in some segment) and **exclusive** (no player lands in two). Without both properties, the segment numbers will not add back up to the total, and you lose the ability to explain the total.

Almost every KPI you met in DB201 is a rate or an average: D7 retention, conversion to payer, ARPDAU, median session length. Any rate over a population is a **weighted mean** of the same rate over its segments, with each segment weighted by its share of the population. That is arithmetic, not a modeling choice. It follows that a rate can move for two different reasons:

1. **The rates inside segments changed.** Players of some kind started behaving differently.
2. **The weights changed.** The population now has more of one kind of player and fewer of another.

The first is usually what the team wants to know about, because it responds to design. The second often comes from outside the game: a marketing campaign, a new platform, a store feature, a free weekend, a price change. Both show up as the same line going down on the dashboard.

Live teams segment along a handful of axes. Each one answers a different question.

| Axis | Example segments | Question it answers |
|---|---|---|
| Acquisition | organic, paid ad, referral; account type (free, paid) | Did the kind of player arriving change? |
| Platform and region | PC, console, mobile; NA, EU, Asia | Is a problem technical or local? |
| Lifecycle | new (under 7 days), established, veteran, returning | Is this about onboarding or about endgame? |
| Value | non-payer, low, mid, high spender | Who does a price or store change affect? |
| Behavior | mostly PvP, mostly crafting, mostly social | Which part of the game does a change touch? |

The first four are **rule-based**: a line of SQL puts each player in a segment. The last one is often built by clustering, which section 3 covers. Start with rules. They are cheap, stable and easy to explain in a meeting.

## 2. Worked example: every segment got better, the total got worse

### The hook

On 29 August 2015, ArenaNet made the core game of Guild Wars 2 free to play. Before that date, every new account had bought the game. After it, anyone could make an account for nothing. ArenaNet did not treat the two kinds of account alike. Free accounts had rate-limited map chat and could whisper only friends and players on the same map. They could not mail coins or items, and they could use only a restricted list of items on the Trading Post. The Guild Wars 2 Wiki records the stated aim as keeping malicious users from disrupting the game and encouraging players to buy it.

In other words, the studio segmented its players by account type on day one and wrote the segments into the game rules. Now think about what that change does to a dashboard. The people who make a free account on a whim are not the same people who paid for a box. If the free players stay at a lower rate, and there are suddenly many more of them, then "D7 retention of new accounts" will fall on the week the game goes free. It will fall even if the game got better for everyone.

Did the game get worse, or did the players change? You cannot answer that from the total. You can answer it from the segments.

The numbers below are invented for a game like this one. ArenaNet has not published retention by account type, and nothing here depends on its real values.

### The model

Split the population into segments `s`. For each period:

```
overall rate  M = Σ_s  w_s × m_s
```

- `w_s` is segment `s`'s **share** of the population (its count divided by the total), so the shares add to 1.
- `m_s` is the rate inside segment `s`, for example its D7 retention.
- `M` is the overall rate, the number on the dashboard.

Now compare a "before" period (subscript 0) with an "after" period (subscript 1). The change in the overall rate splits exactly into two parts:

```
ΔM = M1 − M0
   = Σ_s (w1_s − w0_s) × m0_s     mix effect:  new shares, old rates
   + Σ_s  w1_s × (m1_s − m0_s)    rate effect: new shares, rate changes
```

The **mix effect** is how much the total would have moved if every segment kept its old rate and only the shares changed. The **rate effect** is what remains: how much the segments themselves changed, weighted by how big they are now. Add the two lines and the cross terms cancel, so the split is exact. Every point of change lands in one bucket or the other.

### Numbers you can check

Two weeks of new accounts, one before the free-to-play switch and one after.

| Segment | Week 0 new accounts | Week 0 D7 | Week 1 new accounts | Week 1 D7 |
|---|---|---|---|---|
| Paid | 9,000 | 40% | 6,000 | 42% |
| Free | 1,000 | 15% | 24,000 | 18% |
| **All** | 10,000 | **37.5%** | 30,000 | **22.8%** |

Both segments improved. Paid went from 40% to 42%, free from 15% to 18%. The total dropped 14.7 points.

Check the totals by hand. Week 0 retained `9,000 × 0.40 + 1,000 × 0.15 = 3,600 + 150 = 3,750` players out of 10,000, which is 37.5%. Week 1 retained `6,000 × 0.42 + 24,000 × 0.18 = 2,520 + 4,320 = 6,840` out of 30,000, which is 22.8%.

Now the shares. In week 0, paid is `w0 = 0.9` and free is `0.1`. In week 1, paid is `w1 = 0.2` and free is `0.8`.

```
mix effect  = (0.2 − 0.9) × 0.40 + (0.8 − 0.1) × 0.15
            = −0.280 + 0.105 = −0.175
rate effect = 0.2 × (0.42 − 0.40) + 0.8 × (0.18 − 0.15)
            = 0.004 + 0.024 = +0.028
total       = −0.175 + 0.028 = −0.147
```

The mix shift cost 17.5 points. The segments improving earned 2.8 points back. The team that read only the total would have hunted for a bug in onboarding. The team that read the split would have seen an onboarding that was working slightly better for both kinds of player, and an audience that changed.

Look at one more column before you move on. Retained players went from 3,750 to 6,840, up 82%. The rate fell and the count rose. Which of those matters depends on the decision. A server-capacity planner cares about the count. A designer judging the tutorial cares about the segment rates. Nobody should be making a decision from the blended rate alone.

Here is the same computation as code. It runs as shown with `.venv/bin/python`.

```python
before = {"paid": (9_000, 0.40), "free": (1_000, 0.15)}
after = {"paid": (6_000, 0.42), "free": (24_000, 0.18)}

def shares(groups):
    total = sum(n for n, _ in groups.values())
    return {s: (n / total, m) for s, (n, m) in groups.items()}

def overall(groups):
    return sum(w * m for w, m in shares(groups).values())

def decompose(before, after):
    b, a = shares(before), shares(after)
    mix = sum((a[s][0] - b[s][0]) * b[s][1] for s in b)
    rate = sum(a[s][0] * (a[s][1] - b[s][1]) for s in b)
    return mix, rate

print(f"overall before {overall(before):.3f}, after {overall(after):.3f}")
mix, rate = decompose(before, after)
print(f"mix effect {mix:+.3f}, rate effect {rate:+.3f}, total {mix + rate:+.3f}")
```

Output:

```
overall before 0.375, after 0.228
mix effect -0.175, rate effect +0.028, total -0.147
```

One honest caveat about the split. The formula above measures the mix effect at the old rates and the rate effect at the new shares. You can also do it the other way round: mix at the new rates, rate at the old shares. That gives a mix effect of `−0.168` and a rate effect of `+0.021`. Same total, slightly different split. When the two orderings disagree a lot, report the average of the two (analysts call this the midpoint or Shapley split) and say which you used. When they agree, as here, either ordering tells the same story.

### The visual

Open `examples/w07-segment-mix.html`. The left view is one bar: overall D7 for week 0 and week 1, the number your dashboard shows. The right view shows each segment's D7 as a bar whose width is its share of players. The overall rate is the area of those bars, so you can see it as a weighted mean.

Drag the "free share in week 1" slider from 10% up to 80%. The segment bars on the right do not change height at all. They only change width. The overall bar on the left falls steadily. Then leave the share alone and drag the segment rates. Now the right view changes height and the left moves much less. Below both views, a waterfall chart splits the change into a mix bar and a rate bar with exact values. The picture to keep is that one view can fall while the other rises.

### Cross-game recognition

**EVE Online's price indices (MMO304 week 12).** In MMO304 you saw that the average transaction price in a game market can double while no item changed price, because players bought more of the expensive items. That is a mix effect on prices. A Laspeyres price index holds the basket fixed and lets only prices move, which is exactly our rate effect with the old weights. CCP's Monthly Economic Report publishes indices instead of average prices for this reason. Write the average price as `Σ w_s × p_s`, where `w_s` is item `s`'s share of units sold, and you have this lecture's formula with prices in place of retention.

**UC Berkeley graduate admissions, fall 1973.** Men were admitted at 44% of 8,442 applications and women at 35% of 4,321. Bickel, Hammel and O'Connell (1975) broke the numbers out by department and found no pattern of bias against women inside departments; if anything, the department rates slightly favored women. Women had applied more often to departments that admitted a small share of all applicants. Segments are departments, `w_s` is the share of each sex's applications going to each department, and `m_s` is the department's admission rate. The gap in the total was a mix effect.

**The kidney stone study (Charig et al., 1986).** Treatment A succeeded more often than treatment B for small stones (93% against 87%) and for large stones (73% against 69%). Overall, B looked better (83% against 78%), because doctors had given A the harder, large-stone cases. When the segment mix differs between the two things you are comparing, the totals can point the wrong way. Statisticians call this reversal **Simpson's paradox**. Our GW2-style example is the time-series version of it. Instead of comparing two treatments, you compare a week with the week before.

Three contexts, one identity. A total is a weighted mean of segments. Before you explain a change in the total, split it into what the weights did and what the segments did.

### Eyes-open design judgment

- **Always ship a total with its segment table.** A retention tile without the account-type split is an invitation to misread a marketing success as a design failure. Put the split one click away, on the same dashboard.
- **Pick the segment axis that matches the suspected cause.** If you changed acquisition, split by acquisition source. If you changed the tutorial, split by platform and new-versus-returning, because the tutorial can break on one client. A mix analysis only finds the mix shifts along the axis you chose.
- **Mix changes can be the goal.** Going free to play was a deliberate choice to change the mix, so a lower blended retention was the expected price for more players. Judge the change against the question the studio asked. Here that is "did we gain retained players?" (yes, 3,750 to 6,840) and "did any segment get worse?" (no).
- **Watch for rates that move because the mix inside a segment moved.** "Free" is itself a mix: the week-1 free players include curious visitors a paid game never saw. The free segment's rate could fall while the game improved. Split further when a segment is large and not uniform, and stop when segments get too small to measure (section 3).

## 3. Choosing segments that hold up

### Define segments before the thing you are measuring

The most common segmentation error is defining a segment by something that happened after the change you are studying. Suppose the team adds guilds to the new-player experience and reports: "players who joined a guild in their first week retained at 60%, players who didn't retained at 25%, so guilds more than double retention." The segment "joined a guild in week one" is defined by behavior that happened after the player chose to keep playing for a while. Players who were already going to stay are the ones who have time to join guilds. The gap could be mostly selection.

The rule is simple. **Segment by attributes that were fixed before the treatment**: account type at creation, install date, platform, region, acquisition source, spend tier as of the day before the change. Attributes measured after the change are outcomes. You may study them, but you cannot use them to split a comparison and call the result an effect. MA102 week 14 called this the missing-control problem. Segmenting on an outcome is one of the easiest ways to create it.

### Size: every segment has an error bar

A segment rate is a sample rate, and MA102 week 13 gave you its 95% margin of error, about `1.96 × sqrt(m(1 − m) / n)`. Apply it before you trust a segment row.

| Segment | n | D7 | 95% margin |
|---|---|---|---|
| Free, week 1 (from section 2) | 24,000 | 18% | ±0.5 points |
| Free, week 0 | 1,000 | 15% | ±2.2 points |
| A region and platform cell | 300 | 30% | ±5.2 points |

The week-0 free segment's margin is about as large as the 3-point improvement we credited it with. With only 1,000 players before the switch, you should say "free retention held or rose slightly", not "rose 3 points". In the smallest cell, a 5-point swing from one week to the next is noise. When you split a population many ways, the cells get small quickly: 5 regions times 3 platforms times 4 spend tiers is 60 cells. The practical rule is to split along one axis at a time, and to merge cells until the margin is smaller than the change you would act on.

### Clusters: segments you discover instead of define

Sometimes you do not know the right rule, and you want the data to suggest groups. **Clustering** algorithms such as k-means take a table of per-player features (hours per week, share of time in PvP, share in crafting, guild size, spend) and group players whose feature vectors are close together. Drachen, Canossa and Yannakakis (2009) grouped Tomb Raider: Underworld players this way from gameplay telemetry, and Drachen and colleagues (2012) extended the approach to large commercial datasets. The *Game Analytics* reading describes the method.

Clusters are useful for discovery and risky as dashboard segments, for three reasons.

- **They move.** Re-run k-means next month and players change clusters because the features changed, not because the players did. A cluster label is an outcome, which breaks the rule above if you use it to split an experiment.
- **They depend on your choices.** The number of clusters, the features and how you scale them decide the answer. Two analysts can get different "player types" from the same data.
- **They invite personality stories.** In [MMO301 week 9](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w09-motivation-research-beyond-bartle-yee.md) you saw that Yee's survey data found motivation components that most players mix, rather than clean types, and [UX201 week 6](../../UX201-game-ux-and-player-psychology/lectures/w06-player-motivation-models.md) showed how a questionnaire's design can manufacture types. A cluster called "the socializers" is a region of a feature space, not a kind of person.

Use clusters to find a rule, then write the rule down and use the rule. "Over half of play time in PvP during the player's first 14 days" is a rule you can compute on any day, audit, and hold fixed across a test.

### A worked scheme

A reasonable first scheme for a mid-size MMO dashboard looks like this. Each row is a rule, evaluated on the player's state at the start of the reporting period.

| Axis | Segments | Rule |
|---|---|---|
| Tenure | new, established, veteran, returning | days since account creation under 7, 7 to 89, 90 or more; returning if absent 30 or more days before this session |
| Account | free, paid, subscriber | account flags at period start |
| Spend | non-payer, payer | lifetime spend above zero at period start |
| Platform | PC, console | client of first session in the period |

Four axes, 2 to 4 segments each, one axis at a time on the dashboard. This is deliberately boring. Boring segments are the ones that still mean the same thing next year.

## 4. Segments in experiments and targeting

### Reading an A/B test by segment

When a test result comes back flat, someone will ask to "look at it by segment". Sometimes a change really does help one group and hurt another, which is called a **heterogeneous treatment effect**. More often, a segment that "won" is noise. MMO308 week 6 treats the statistics in depth. The core arithmetic is the complement rule from [MA102 week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). If you test 10 independent segments at a 5% false-positive rate each, the chance that at least one "wins" by luck is `1 − 0.95^10 ≈ 0.40`. Four times in ten, a change with no effect at all produces a winning segment.

Three habits keep segment readouts honest:

- **Name the segments before the test starts,** in the test plan, with a reason for each. A segment you picked after seeing the results is a hypothesis for the next test, not a finding.
- **Use pre-treatment segments only,** for the reason in section 3.
- **Check that randomization balanced the segments.** If group B got 55% free accounts and group A got 45%, the overall comparison already contains a mix effect. Compare within segments and combine using a common set of weights.

### Targeting segments in a shared world

Segments are also for acting: showing a returning-player offer, tuning an event for new players, adjusting a store for one region. In a single-player mobile game, one segment rarely sees another segment's treatment. In an MMO, players stand in the same town and read the same forums. A discount shown only to lapsed players is visible to the loyal players who paid full price the week before. GW2's free-account limits worked partly because they were public, stated and applied by rule to everyone in the segment.

When you target a segment, write down what players outside it will see and whether they would consider it fair. [MMO403 week 10](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w10-pricing-experiments.md) covers the ethics of price targeting. For now, keep one test: could you explain the rule on the official forum without embarrassment?

## In-class activity (25 minutes)

In groups of three. You receive this table for a game's Day-1 conversion to a first purchase, before and after a store redesign that shipped the same week as a large console launch.

| Segment | Before: players | Before: conversion | After: players | After: conversion |
|---|---|---|---|---|
| PC | 20,000 | 4.0% | 22,000 | 4.4% |
| Console | 5,000 | 1.0% | 30,000 | 1.1% |

1. Compute the overall conversion before and after.
2. Decompose the change into mix and rate effects, both orderings.
3. Compute the 95% margin of error for each segment rate.
4. Write a three-sentence note to the producer: did the store redesign work, and on which platform can you say so with confidence?

Expected output: overall 3.40% before and 2.50% after. With old rates, the mix effect is −1.13 points and the rate effect +0.23 points. With new rates, −1.24 and +0.34. PC's margins are about ±0.27 points in both weeks, so its 0.4-point gain is real but small. Console's margins are ±0.28 and ±0.12 points, larger than its 0.1-point change. Your note should say the drop is a mix effect from the console launch, the redesign probably helped a little on PC, and its effect on console is unknown.

## Common misconceptions

- **"If every segment improved, the total must improve."** Only if the shares stayed the same. A shift toward a lower-rate segment can pull the total down while every segment rises.
- **"A falling rate means fewer successes."** In section 2 retention fell from 37.5% to 22.8% while retained players rose 82%. Check the counts.
- **"More segments means more insight."** Every split shrinks `n` and widens the margin. Past a point you are reading noise with confidence.
- **"Players who used the feature retained better, so the feature works."** Segmenting on a behavior after the change mixes the feature's effect with who chose to use it. Use a pre-treatment segment or a randomized test.

## Check yourself

1. Before a patch, segment A is 50% of players at 30% retention, segment B is 50% at 10%. After the patch, A is 25% at 32% and B is 75% at 12%. Compute the overall rate before and after, and the mix and rate effects (old-rate ordering).
2. A test is read across 8 pre-registered segments at a 5% false-positive rate each. The change does nothing. What is the chance at least one segment shows a "significant" win?
3. A segment of 250 players has D7 of 24%. Next week it reads 28%. Should the dashboard highlight the change? Show the margin.
4. A producer says, "Clusters from last month show 'explorers' retain best, so let's split next month's A/B test by explorer cluster." Give two problems with that plan.

<details>
<summary>Answers</summary>

1. Before `0.5 × 0.30 + 0.5 × 0.10 = 0.20`. After `0.25 × 0.32 + 0.75 × 0.12 = 0.08 + 0.09 = 0.17`. Mix `(0.25 − 0.5) × 0.30 + (0.75 − 0.5) × 0.10 = −0.075 + 0.025 = −0.05`. Rate `0.25 × 0.02 + 0.75 × 0.02 = +0.02`. Total `−0.03`, which matches `0.17 − 0.20`.
2. `1 − 0.95^8 ≈ 0.34`, about one test in three.
3. Margin `1.96 × sqrt(0.24 × 0.76 / 250) ≈ 0.053`, about ±5.3 points. A 4-point change is inside the margin, so no highlight. Merge the segment with a neighbor or wait for more data.
4. Cluster membership is computed from behavior, so it can change during the test and may be affected by the treatment (a post-treatment segment). And the cluster depends on the analyst's choices of features and cluster count, so "explorer" may not be stable from month to month. Convert the cluster into a fixed rule measured before the test starts.

</details>

## Lab / assignment hook

[Lab 07, segment the retention drop](../labs/lab07.md). You get two weeks of new-player records with account type, region and D7 retention, and a starter module with the decomposition left to write. Deliverable: passing tests, a decomposition along two axes, and a 300-word memo that separates the mix effect from one real regression hidden inside a segment.

## Sources

- Guild Wars 2 Wiki, "Free to play" (accessed September 2026). Core game free since 29 August 2015; free-account limits on map chat, whispers, mail and the Trading Post; stated intent to prevent disruption and encourage purchase.
- Bickel, P. J., Hammel, E. A. & O'Connell, J. W. (1975). "Sex Bias in Graduate Admissions: Data from Berkeley." *Science* 187(4175), 398-404. Fall 1973 figures (44% of 8,442 men, 35% of 4,321 women), as summarized in Wikipedia, "Simpson's paradox".
- Charig, C. R., Webb, D. R., Payne, S. R. & Wickham, J. E. A. (1986). "Comparison of treatment of renal calculi by open surgery, percutaneous nephrolithotomy, and extracorporeal shockwave lithotripsy." *BMJ* 292, 879-882. Success rates by stone size, as summarized in Wikipedia, "Simpson's paradox".
- CCP Games, EVE Online Monthly Economic Report (current series). Consumer and producer price indices; see MMO304 week 12 for the full treatment.
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Chapter on game data mining and player clustering.
- Drachen, A., Canossa, A. & Yannakakis, G. N. (2009). "Player modeling using self-organization in Tomb Raider: Underworld." *IEEE Symposium on Computational Intelligence and Games (CIG 2009)*, Milan.
- Drachen, A., Sifa, R., Bauckhage, C. & Thurau, C. (2012). "Guns, swords and data: Clustering of player behavior in computer games in the wild." *IEEE Conference on Computational Intelligence and Games (CIG 2012)*, Granada. doi:10.1109/CIG.2012.6374152.

## Interactive spec: examples/w07-segment-mix.html

**The one insight.** A total is a weighted mean of segments. Changing only the weights moves the total while every segment stays the same or improves, and a waterfall splits the change exactly into a mix part and a rate part.

**Layout.** Two linked views side by side at 1280px, stacked at 390px. Left: "What the dashboard shows", two bars (week 0, week 1) of overall rate, values printed on top. Right: "What the segments did", a variable-width bar chart per week. Each segment is a bar whose width is its share of the week's players and whose height is its rate, paid and free side by side, with the overall rate drawn as a dashed horizontal line across each week's group. The dashed line's height equals the area-weighted mean of the bars. Below both, a waterfall: week-0 overall, mix effect bar, rate effect bar, week-1 overall.

**Controls (all update instantly).**
- Week 0 free share `w0_free`, 0% to 90%, default 10%.
- Week 1 free share `w1_free`, 0% to 90%, default 80%.
- Four rate sliders, 0% to 60% in 0.5-point steps: `m0_paid` 40, `m0_free` 15, `m1_paid` 42, `m1_free` 18.
- Week totals: `N0 = 10,000`, `N1 = 30,000`, editable number inputs.
- Ordering toggle: "old rates" (default), "new rates", "midpoint".
- Reset button restores defaults.

**Formulas.**
- `w_paid = 1 − w_free` in each week. `M0 = w0_paid × m0_paid + w0_free × m0_free`; `M1` likewise.
- Old-rate ordering: `mix = Σ (w1 − w0) × m0`, `rate = Σ w1 × (m1 − m0)`.
- New-rate ordering: `mix = Σ (w1 − w0) × m1`, `rate = Σ w0 × (m1 − m0)`.
- Midpoint: average of the two orderings' mix values, and of their rate values.
- Retained counts: `R = N × M`; show `R0`, `R1` and the percent change under the chart.

**Readouts.** Next to the views, print `M0`, `M1`, `ΔM`, mix, rate (three decimals and as points), `R0`, `R1`. Print a warning line "Every segment improved, the total fell" whenever both segment rates rose and `ΔM < 0`.

**Test values.**
- Defaults, old-rate ordering: `M0 = 0.375`, `M1 = 0.228`, mix `−0.175`, rate `+0.028`, `ΔM = −0.147`, `R0 = 3,750`, `R1 = 6,840` (+82.4%).
- Defaults, new-rate ordering: mix `−0.168`, rate `+0.021`. Midpoint: mix `−0.1715`, rate `+0.0245`.
- `w1_free = 10%` with default rates: `M1 = 0.396`, mix `0`, rate `+0.021`.
- Check-yourself question 1 (relabel segments A and B by setting `w0_free = 50%`, `w1_free = 75%`, `m0_paid = 30`, `m0_free = 10`, `m1_paid = 32`, `m1_free = 12`): `M0 = 0.20`, `M1 = 0.17`, mix `−0.05`, rate `+0.02`.

**Accessibility and style.** Sliders are native range inputs with visible labels and numeric outputs; the waterfall bars carry text values. Colors from `templates/interactive-tokens.css`; paid and free differ by pattern as well as color. No game art or logos.
