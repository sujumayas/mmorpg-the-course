# MMO405 · Exam bank: quiz, practice and oral-check questions

MMO405 has no written exam. The grade comes from the research proposal (20%, [proposal-brief.md](proposal-brief.md)), the methods labs (30%, [methods-labs-brief.md](methods-labs-brief.md)) and the final research paper (50%, [paper-brief.md](paper-brief.md)). This bank does three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Oral check.** The 10-minute oral check on the final paper draws on questions in this style. The examiner rewrites them with the numbers from your own study.

Every question is tagged with the week it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **analysis**: read a small dataset or a study summary and reach a conclusion that needs a number.
- **explain**: say why a model or a study behaves as it does, with a number or a named mechanism as evidence.
- **critique**: find what is wrong with a claim or a plan and say how to fix it.

All numbers are invented unless a question names a study. Every study fact used here comes from the lecture of the tagged week, which cites its source and date. Every numeric answer was recomputed in Python from the lecture's own model, and the three code snippets below run as shown with `.venv/bin/python`. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: Research questions in game studies

Model: `observed gap = causal effect + selection term`, with `selection term = (r_H − r_L) × (s_T − s_U)` when the effect is the same for both kinds of player. [Lecture](../lectures/w01-research-questions-in-game-studies.md).

1. *Week 1 · compute.* An invented server has 2,000 new players: 600 high-commitment and 1,400 low-commitment. High-commitment players join a guild 80% of the time and low-commitment players 25% of the time. Without a guild, 30-day retention is 75% for high-commitment and 35% for low-commitment players. Guilds have no causal effect. Compute (a) the number of each kind in and out of guilds, (b) 30-day retention for guild members and non-members, (c) the observed gap, and (d) `s_T`, `s_U` and the selection term.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Retention 58.1% against 39.1%, a gap of 19.0 points, all of it selection.

(a) Guild members: `600 × 0.80 = 480` high and `1,400 × 0.25 = 350` low, 830 in all. Non-members: 120 high and 1,050 low, 1,170 in all.

(b) Guild: `(480 × 0.75 + 350 × 0.35) / 830 = (360 + 122.5) / 830 = 58.1%`. No guild: `(120 × 0.75 + 1,050 × 0.35) / 1,170 = (90 + 367.5) / 1,170 = 39.1%`.

(c) `58.1 − 39.1 = 19.0` points.

(d) `s_T = 480 / 830 = 0.578` and `s_U = 120 / 1,170 = 0.103`. Selection `= (0.75 − 0.35) × (0.578 − 0.103) = 0.40 × 0.475 = 0.190`, the whole gap.
</details>

2. *Week 1 · compute.* Same server as question 1, but now guilds burn players out: a guild lowers each player's 30-day retention by 8 points (`δ = −0.08`). (a) What gap does the dashboard show? (b) How negative would `δ` have to be before the dashboard showed no gap at all?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) +11.0 points. (b) `δ = −0.190`, a 19-point harm.

(a) The selection term does not depend on `δ`, so it stays at +19.0 points. The gap is `δ + selection = −8.0 + 19.0 = +11.0` points. Check directly: guild retention is `(480 × 0.67 + 350 × 0.27) / 830 = 50.1%`, non-members stay at 39.1%, gap 11.0.

(b) The gap is zero when `δ = −0.190`. No clamping is needed, since `0.35 − 0.19 = 0.16` is still a valid rate. A dashboard reading "guild members retain slightly better" is compatible with guilds that cost up to 19 points of retention.
</details>

3. *Week 1 · analysis.* A studio stratifies its 1,700 new accounts by week-one play time. Counts and 30-day retention:

| Band | In guild (n, retained) | No guild (n, retained) |
|---|---|---|
| Low | 100, 30 | 700, 196 |
| Mid | 200, 110 | 300, 150 |
| High | 300, 225 | 100, 70 |

Compute the pooled (dashboard) gap, the gap inside each band, and the stratified gap weighted by band size. How much of the dashboard gap is selection on week-one play time, and what can the stratified number still not tell you?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Dashboard gap 23.0 points; stratified gap 3.6 points; about 19.4 points are selection on the measured proxy.

Pooled: guild `365 / 600 = 60.8%`, no guild `416 / 1,100 = 37.8%`, gap 23.0 points.

Inside bands: low `30% − 28% = 2` points, mid `55% − 50% = 5`, high `75% − 70% = 5`.

Weighted by band size (800, 500 and 400 of 1,700): `(800 × 2 + 500 × 5 + 400 × 5) / 1,700 = 6,100 / 1,700 = 3.6` points.

So `23.0 − 3.6 = 19.4` points of the dashboard gap come from guild members being concentrated in the high band. The 3.6 points are still not a causal effect. Stratification removes only the selection that runs through week-one play time. Anything the bands miss, such as having friends who already play, stays in the estimate (lecture section 2, "Stratification only fixes what you measured").
</details>

4. *Week 1 · critique.* A patch note says: "Players who use the new in-game calendar raid twice as often, so the calendar is driving raid participation." (a) Name the claim type the data support and the claim type the sentence makes. (b) Write the two brackets of the selection term for this case and the sign you expect for each. (c) Propose one design that would separate the calendar's effect from selection, and say what it assumes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Associational data, causal claim; both brackets positive; a randomized encouragement or a staggered rollout.

(a) The data compare calendar users with non-users, so they support an associational claim. "Driving" is causal.

(b) `r_H − r_L`: players already organized into raid groups raid more with or without the calendar, so positive. `s_T − s_U`: those organized players are the ones who adopt a scheduling tool, so positive. The product is positive, and it may account for most of the "twice as often".

(c) Randomize an encouragement, such as a calendar tutorial prompt shown to a random half of new raiders, and compare raid participation between the prompted and unprompted halves. It assumes the prompt affects raiding only through calendar use. A staggered regional rollout with a DiD comparison (week 5) also works, and it assumes parallel trends between regions.
</details>

---

## Week 2: Quantitative methods overview

Model: `SE(d) ≈ sqrt(2/n)`, 95% interval for "different from zero", 90% interval inside `±Δ` for "too small to matter", four verdicts. [Lecture](../lectures/w02-quantitative-methods-overview.md).

5. *Week 2 · compute.* A linked survey finds that players who use voice chat score `d = 0.12` higher on a well-being scale, with 1,500 players per group. Compute `SE(d)`, the 95% and 90% intervals, and the verdict (a) with a SESOI of `Δ = 0.20` and (b) with `Δ = 0.05`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** SE 0.0365; 95% CI 0.048 to 0.192; 90% CI 0.060 to 0.180. (a) Real but trivial. (b) Meaningful.

`SE = sqrt(2 / 1,500) = 0.0365`. 95%: `0.12 ± 1.96 × 0.0365 = 0.048 to 0.192`, which excludes zero. 90%: `0.12 ± 1.645 × 0.0365 = 0.060 to 0.180`.

(a) The 90% interval sits inside `(−0.20, +0.20)` and the 95% interval excludes zero: real but trivial.

(b) The 90% interval is not inside `(−0.05, +0.05)`, and its lower end, 0.060, is above 0.05, so the whole interval lies above the SESOI: meaningful. The same data give opposite practical verdicts because the SESOI changed. That is why the SESOI must be fixed before the analysis.
</details>

6. *Week 2 · compute.* A study observes `d = 0.05` with `Δ = 0.20`. What is the smallest number of players per group at which the four-verdict rule returns "real but trivial"? Which of the two conditions is the binding one?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3,074 per group; the "different from zero" condition binds.

"Real but trivial" needs both conditions.

- 95% interval excludes zero: `0.05 > 1.96 × sqrt(2/n)`, so `n > 2 × (1.96 / 0.05)² = 3,073.3`, which means 3,074.
- 90% interval below 0.20: `0.05 + 1.645 × sqrt(2/n) < 0.20`, so `n > 2 × (1.645 / 0.15)² = 240.5`, which means 241.

The first condition binds. At `n = 3,074` the 95% lower bound is `0.05 − 1.96 × 0.02551 = 0.00001`, just above zero. Between 241 and 3,073 per group the same `d = 0.05` is "no meaningful effect", and below 241 it is inconclusive.
</details>

7. *Week 2 · compute.* (a) Convert `d = 0.30` (two equal groups) to `r`, `R²` and the probability of superiority. (b) A paper reports `r = 0.20` between weekly raid hours and a belonging score. What standardized difference `d` does that correspond to?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `r = 0.148`, `R² = 0.022`, probability of superiority 58.4%. (b) `d = 0.41`.

(a) `r = 0.30 / sqrt(0.09 + 4) = 0.30 / 2.022 = 0.148`. `R² = 0.022`, so group membership explains 2.2% of the variance. Probability of superiority `Φ(0.30 / 1.414) = Φ(0.212) = 0.584`.

(b) `d = 2r / sqrt(1 − r²) = 0.40 / sqrt(0.96) = 0.408`.
</details>

8. *Week 2 · compute.* A study of 400 players finds `r = 0.15` between days in a guild and a loneliness score (reverse-scored). Compute the 95% interval with Fisher's `z`. Does it rule out `r = 0.30`? Does it rule out `r = 0.05`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.053 to 0.244. It rules out both, the second only just.

`z = atanh(0.15) = 0.1511`, `SE = 1 / sqrt(400 − 3) = 0.0502`. Interval on `z`: `0.1511 ± 1.96 × 0.0502 = 0.0528 to 0.2495`. Back-transformed with `tanh`: 0.053 to 0.244.

0.30 is above the upper end, so it is ruled out. 0.05 sits just below the lower end, 0.053, so it is ruled out at the 95% level, but only just. A report should say the data are compatible with anything from a very small to a modest association.
</details>

9. *Week 2 · critique.* A studio blog post says: "Our new tutorial raised 30-day retention by 15% (from 20% to 23%, p < .001, 8,000 players in 40 guild-recruitment cohorts). That is a small effect by Cohen's standards, so we will not keep it." Find three problems in this sentence and fix each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Percent versus points, Cohen's labels used as a SESOI, and the wrong independent unit.

- 20% to 23% is +3 percentage points and +15% relative. Say which one you mean, and prefer points for retention (lecture section 3).
- Cohen's small, medium and large are a fallback, not a SESOI. For a studio, a 3-point retention lift may be worth a lot. Set the SESOI from what the change is worth (lecture section 2, "Choose the SESOI before the data").
- If players were assigned or recruited in 40 cohorts, the independent units are closer to 40 than 8,000 (design effect, lecture section 4). The p-value computed on 8,000 players is too small. Recompute with cohort as the cluster, or say that the interval is too narrow.
</details>

---

## Week 3: Telemetry as research data

Model: `S = X + b + e`, `r(S, Y) = r(X, Y) × r(S, X)`, corrected `r = r(S, Y) / r(S, X)`; players needed `n = ((1.96 + 0.8416) / atanh(r))² + 3`. [Lecture](../lectures/w03-telemetry-as-research-data.md).

10. *Week 3 · compute.* In a sample like yours, self-reported weekly play correlates with logged play at `r = 0.45`. A survey-only study reports `r = 0.09` between self-reported play and a stress score (assume the stress score is perfectly reliable and the recall error is random). (a) Estimate the log-based correlation. (b) How many players would each design need for 80% power at the 5% level: the self-report design at `r = 0.09`, and a log design at your corrected value?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.20. (b) About 967 players with self-reports against 194 with logs, five times as many.

(a) `0.09 / 0.45 = 0.20`.

(b) `atanh(0.09) = 0.0902`, so `n = (2.8016 / 0.0902)² + 3 = 966.8`, round up to 967. `atanh(0.20) = 0.2027`, so `n = (2.8016 / 0.2027)² + 3 = 194.0`, round up to 194. The ratio is 967 / 194 = 5.0.
</details>

11. *Week 3 · compute.* Logged play has an SD of 8 hours a fortnight (variance 64). Players' recall adds random noise with an SD of 10 hours and a constant overestimate of 2 hours. (a) What is the reliability `ρ` of the self-report and its correlation with the logs? (b) If the true correlation between logged play and well-being is 0.25, what will a self-report study observe? (c) What does the 2-hour overestimate do to the mean and to the correlation?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `ρ = 0.390`, `r(S, X) = 0.625`. (b) 0.156. (c) The mean rises by 2 hours; the correlation is unchanged.

(a) `ρ = 64 / (64 + 100) = 0.390`, `r(S, X) = sqrt(0.390) = 0.625`.

(b) `0.25 × 0.625 = 0.156`.

(c) Bias `b` shifts every answer by the same amount. Means move by 2 hours, and correlations, which ignore constant shifts, do not change (lecture section 2, "Bias moves means. Noise hides relationships.").
</details>

12. *Week 3 · compute.* One invented player's evening: login at 18:00; activity events every minute or two from 18:00 to 18:50; no events from 18:50 to 19:12; activity from 19:12 to 20:00; no events from 20:00 to 20:35; activity from 20:35 to 20:45; no events until logout at 21:30. Compute hours played under (a) login to logout, (b) an activity rule where gaps over 30 minutes end a session, (c) gaps over 15 minutes, and (d) gaps over 45 minutes (logout does not count as activity). What is the ratio of the largest to the smallest answer?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.50 h, (b) 2.17 h, (c) 1.80 h, (d) 2.75 h. Ratio 1.94.

(a) 18:00 to 21:30 is 210 minutes, 3.50 h.

(b) The 22-minute gap does not end a session, and the 35-minute gap does. Sessions 18:00 to 20:00 (120 min) and 20:35 to 20:45 (10 min): 130 min, 2.17 h.

(c) Both gaps end sessions. Sessions of 50, 48 and 10 minutes: 108 min, 1.80 h.

(d) Neither gap ends a session. 18:00 to 20:45 is 165 min, 2.75 h. The 45 idle minutes before logout are excluded because logout is not activity.

`3.50 / 1.80 = 1.94`. The rule choice nearly doubles this player's evening, more than the lecture's 1.76, because of the long idle stretch before logout.
</details>

13. *Week 3 · explain.* For each cleaning rule, say which way it moves mean weekly play time and one other consequence for a study of heavy play. (a) Drop accounts that average more than 16 hours a day. (b) Treat accounts with no events in the window as missing rather than zero. (c) Sample "current players" from those who logged in yesterday.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

(a) Lowers the mean. It removes likely bots and farmers, and also removes the heaviest human players if any exist, so a study of heavy play must report how many accounts it dropped and check the result with a cap instead of a drop.

(b) Raises the mean, because zeros leave the data. The finding then describes active players only, which is what Vuorre and colleagues stated for their 38,935 players. The method section must say so.

(c) Raises the mean. It is length-biased and survivor-biased: heavy, long-tenure players are more likely to have logged in yesterday, and players who left are absent. Any retention claim from this sample describes those who stayed.
</details>

---

## Week 4: Survey design and validated scales

Model: `α = k/(k − 1) × (1 − Σσ²_i / σ²_X)`; standardized `α = k r̄ / (1 + (k − 1) r̄)`; `r̄ = α / (k − (k − 1)α)`. [Lecture](../lectures/w04-survey-design-and-validated-scales.md).

14. *Week 4 · compute.* A 4-item "raid pressure" scale has item variances 1.2, 1.0, 1.1 and 0.9 in your sample. The variance of the summed score is 10.4. Compute Cronbach's alpha.

<details>
<summary>Answer and worked solution</summary>

**Answer:** α = 0.795.

`Σσ²_i = 4.2`. `α = 4/3 × (1 − 4.2 / 10.4) = 1.333 × 0.596 = 0.795`.

Check the logic: if the items were unrelated, the total's variance would be 4.2 and alpha would be 0. The total's variance is 2.5 times larger, so the items move together.
</details>

15. *Week 4 · compute.* A 5-item scale has an average inter-item correlation of 0.35. (a) What is its standardized alpha? (b) Holding `r̄` fixed, how many items would reach α = 0.85? (c) Is adding those items a good idea in an in-game survey?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.729. (b) 11 items. (c) Usually not.

(a) `5 × 0.35 / (1 + 4 × 0.35) = 1.75 / 2.40 = 0.729`.

(b) Solve `k × 0.35 / (1 + (k − 1) × 0.35) = 0.85`: `k = 0.85 × 0.65 / (0.35 × 0.15) = 10.5`, so 11 items.

(c) Six extra items raise alpha by length alone and cost completions. Near-duplicate items also narrow what the scale measures (lecture, "Don't pad a scale to raise alpha"). A 5-item scale at 0.73 is often the better trade in a live game. Report the alpha and let readers judge.
</details>

16. *Week 4 · compute.* A student's 8-item "guild commitment" scale has two groups of 4 items. Items within a group correlate at 0.55, and items in different groups correlate at 0.05. (a) Count within-group and between-group pairs and compute `r̄`. (b) Compute alpha for the whole scale and for each 4-item group. (c) What would you report?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12 within, 16 between, `r̄ = 0.264`. (b) Whole scale 0.742; each group 0.830. (c) Two scores.

(a) Within: `2 × C(4, 2) = 12`. Between: `4 × 4 = 16`. Total pairs `C(8, 2) = 28`. `r̄ = (12 × 0.55 + 16 × 0.05) / 28 = 7.4 / 28 = 0.264`.

(b) Whole: `8 × 0.264 / (1 + 7 × 0.264) = 2.114 / 2.850 = 0.742`. Each group: `4 × 0.55 / (1 + 3 × 0.55) = 2.2 / 2.65 = 0.830`.

(c) The whole scale passes the usual 0.70 line, yet it is two nearly separate constructs. Each half is more reliable than the whole. Report two 4-item scores with their own alphas and show the correlation matrix.
</details>

17. *Week 4 · compute.* A published 6-item scale reports α = 0.78. (a) What is its average inter-item correlation? (b) What alpha should you expect from a 3-item short form built from items like these? (c) From a 12-item version?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.371. (b) 0.639. (c) 0.876.

(a) `r̄ = 0.78 / (6 − 5 × 0.78) = 0.78 / 2.10 = 0.371`.

(b) `3 × 0.371 / (1 + 2 × 0.371) = 1.114 / 1.743 = 0.639`.

(c) `12 × 0.371 / (1 + 11 × 0.371) = 4.457 / 5.086 = 0.876`.

The short form falls below 0.70 without any change in the items. If you shorten a scale, report the alpha you got in your own sample.
</details>

18. *Week 4 · analysis.* On a 1-to-5 agreement scale, item 7 of your survey reads "I would leave my guild if a better one invited me." Its corrected item-total correlation is −0.31, and alpha rises from 0.62 to 0.79 if it is deleted. (a) What is the most likely cause? (b) What is item 7's recoded value for a respondent who answered 2? (c) Should you simply delete the item?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) An unrecoded reverse item. (b) 4. (c) No, recode it first.

(a) Agreeing with item 7 means less commitment, so it is reverse-worded. A negative item-total correlation almost always means a forgotten reversal (lecture section 4).

(b) `recoded = lo + hi − raw = 1 + 5 − 2 = 4`.

(c) Recode it and recompute. Deleting it would raise alpha and silently change the scale. If it still correlates weakly after recoding, check whether respondents misread the reversed wording before you drop it, and report any deletion.
</details>

---

## Week 5: Experiments and quasi-experiments

Model: `δ = (Y_T,post − Y_T,pre) − (Y_C,post − Y_C,pre)`, valid under parallel trends; placebo DiD on pre-period windows. [Lecture](../lectures/w05-experiments-and-quasi-experiments.md).

19. *Week 5 · compute.* A studio switches on a new report tool on its APAC servers only. Verbal-abuse reports per 1,000 matches: APAC before 8.4, after 7.1; EU (no change) before 8.0, after 7.9. Compute the naive before-and-after change on APAC and the DiD estimate. Which threat to internal validity does the EU comparison address, and which assumption does it add?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Naive −1.3; DiD −1.2 reports per 1,000 matches.

Naive: `7.1 − 8.4 = −1.3`. DiD: `(7.1 − 8.4) − (7.9 − 8.0) = −1.3 + 0.1 = −1.2`.

The EU series absorbs history (anything else that happened to both regions, such as a season change) and maturation. It adds the parallel-trends assumption: without the tool, APAC reports would have fallen by the same 0.1 as the EU's. Show the weekly pre-period lines for both regions to support it.
</details>

20. *Week 5 · compute.* An invented MMO applies a playtime rule to minors, who are 8% of accounts. Heavy-play share, in percent: minors before 5.0, after 3.8; adults before 2.5, after 3.1 (an expansion launched the same week). (a) What does pooled telemetry show, including the odds ratio? (b) What is the DiD estimate? (c) Under parallel trends, where would minors have been without the rule?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2.70% to 3.16%, +0.46 points, odds ratio 1.17. (b) −1.8 points. (c) 5.6%.

(a) Before: `0.08 × 5.0 + 0.92 × 2.5 = 2.70`. After: `0.08 × 3.8 + 0.92 × 3.1 = 3.156`. Change +0.456 points. Odds ratio `(0.03156 / 0.96844) / (0.0270 / 0.9730) = 1.17`.

(b) `(3.8 − 5.0) − (3.1 − 2.5) = −1.2 − 0.6 = −1.8` points.

(c) Minors would have risen by the adults' +0.6 to 5.6%. The rule took them to 3.8%, a cut of about a third, while the pooled figure rose. This is the dilution the lecture's analyst 1 cannot see.
</details>

21. *Week 5 · analysis.* A DiD uses four-week window means. Minors: early-pre 4.0, pre 4.6, post 4.4. Adults: early-pre 3.0, pre 3.2, post 3.9. (a) Compute the DiD and the placebo DiD. (b) What does the placebo tell you, and what would the effect be if the pre-period difference in trends had continued unchanged? (c) How should you report it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) DiD −0.9; placebo +0.4. (b) Trends were not parallel; about −1.3 under a continuing linear gap. (c) Report both and do not present −0.9 as the effect.

(a) DiD: `(4.4 − 4.6) − (3.9 − 3.2) = −0.2 − 0.7 = −0.9`. Placebo: `(4.6 − 4.0) − (3.2 − 3.0) = 0.6 − 0.2 = +0.4`.

(b) Minors were already rising 0.4 points faster per four-week step than adults. The windows are one step apart, so DiD = effect + 0.4 if that gap continued, giving an effect of about `−0.9 − 0.4 = −1.3`. That correction rests on a new assumption (a linear, continuing trend gap), which is why it is not a fix.

(c) Report the DiD, the placebo and the weekly plot. Say that parallel trends fail, that the effect is probably larger than −0.9 in magnitude but uncertain, and look for a comparison group whose placebo is near zero, or use a comparative ITS that models each group's trend (lecture section 3).
</details>

22. *Week 5 · analysis.* A studio gives a "Gold" badge at 1,500 rating and wants to estimate its effect on next-season play with a regression discontinuity. Finishing ratings near the cutoff: 1,490 to 1,494, 410 players; 1,495 to 1,499, 390; 1,500 to 1,504, 980; 1,505 to 1,509, 430. What do these counts show, and what does it do to the RD estimate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Bunching just above the cutoff; the RD estimate is likely biased upward.

The bins either side of the first and last are about 400 players each, so a smooth distribution would put about 400 in 1,500 to 1,504. There are 980, roughly 580 extra, and the bin just below has slightly fewer than its neighbours. Players pushed themselves over 1,500. Those just above are more motivated than those just below, so comparing them mixes the badge's effect with motivation, probably overstating it. Report the histogram, and look for a cutoff players cannot see or cannot aim for (lecture section 4).
</details>

23. *Week 5 · explain.* Name the main threat to internal validity in each before-and-after claim. (a) Toxicity reports on the three worst servers fell 30% a month after moderators were added there. (b) Average session length jumped 12% on the day a client update changed how disconnects are logged. (c) Satisfaction rose after a difficulty patch, measured among players still active a month later. (d) Logins rose the week the guild finder launched, which was also the week of a holiday event.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Regression to the mean. (b) Instrumentation. (c) Attrition. (d) History.

(a) The servers were chosen because they were extreme, and extreme months drift back. Compare with equally bad servers that got no moderators.

(b) The measurement changed on the same day as the outcome.

(c) Frustrated players left, so the remaining sample is happier regardless of the patch.

(d) The holiday event raised logins too. A comparison series without the finder, or randomized rollout, separates the two.
</details>

---

## Week 6: Qualitative methods: interviews

Model: `p_o = (a + d)/n`, `p_e = p_A p_B + (1 − p_A)(1 − p_B)`, `κ = (p_o − p_e)/(1 − p_e)`, `p_pos = 2a/(2a + b + c)`, `p_neg = 2d/(2d + b + c)`, `PABAK = 2p_o − 1`. [Lecture](../lectures/w06-qualitative-methods-interviews.md).

24. *Week 6 · compute.* Two coders code 100 interview excerpts for "mentions being carried". Table: `a = 12` (both yes), `b = 6` (A yes, B no), `c = 4` (A no, B yes), `d = 78`. Compute `p_o`, each coder's yes rate, `p_e`, κ, `p_pos`, `p_neg` and PABAK.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p_o = 0.90`, `p_e = 0.718`, κ = 0.65, `p_pos = 0.71`, `p_neg = 0.94`, PABAK 0.80.

`p_o = 90/100 = 0.90`. `p_A = 18/100 = 0.18`, `p_B = 16/100 = 0.16`. `p_e = 0.18 × 0.16 + 0.82 × 0.84 = 0.0288 + 0.6888 = 0.7176`. `κ = (0.90 − 0.7176) / 0.2824 = 0.646`. `p_pos = 24 / 34 = 0.706`. `p_neg = 156 / 166 = 0.940`. `PABAK = 2 × 0.90 − 1 = 0.80`.

Agreement on the absent cases is high. Agreement on the positive cases, which carry the finding, is 0.71.
</details>

25. *Week 6 · compute.* Two coders each mark 15% of 100 excerpts "yes" for a code and agree on 90 excerpts, with the 10 disagreements split 5 and 5. Build the 2 × 2 table and compute `p_e`, κ, `p_pos` and PABAK. Compare with the same agreement at 50% prevalence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Table 10, 5, 5, 80. `p_e = 0.745`, κ = 0.61, `p_pos = 0.67`, PABAK 0.80. At 50%, κ = 0.80 and `p_pos = 0.90`.

Each coder says yes 15 times, 5 of them in disagreement, so `a = 10`, `b = c = 5`, `d = 80`.

`p_e = 0.15² + 0.85² = 0.0225 + 0.7225 = 0.745`. `κ = (0.90 − 0.745) / 0.255 = 0.608`. `p_pos = 20 / 30 = 0.667`. PABAK = 0.80, the same as at any prevalence.

At 50% prevalence `p_e = 0.5`, `κ = 0.80`, `p_pos = 0.90` (lecture table). The same 90% agreement means much weaker agreement on the positive cases when the code is rarer.
</details>

26. *Week 6 · compute.* You want κ = 0.70 on a code both coders mark "yes" for 20% of excerpts. What observed agreement do you need? What agreement gives κ = 0.70 at 50% prevalence?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 90.4% at 20% prevalence; 85% at 50%.

At 20%: `p_e = 0.2² + 0.8² = 0.68`. `0.70 = (p_o − 0.68) / 0.32` gives `p_o = 0.68 + 0.224 = 0.904`.

At 50%: `p_e = 0.5`, so `p_o = 0.5 + 0.70 × 0.5 = 0.85`.
</details>

27. *Week 6 · compute.* Coder A marks 70% of 200 excerpts "yes" for a code and coder B marks 60%. They agree on 85%. Find the four cells (in counts), then `p_e`, κ, `p_pos` and `p_neg`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a = 115`, `b = 25`, `c = 5`, `d = 55`. `p_e = 0.54`, κ = 0.67, `p_pos = 0.88`, `p_neg = 0.79`.

As shares: `b − c = p_A − p_B = 0.10` and `b + c = 1 − 0.85 = 0.15`, so `b = 0.125`, `c = 0.025`, `a = 0.70 − 0.125 = 0.575`, `d = 1 − 0.575 − 0.125 − 0.025 = 0.275`. Times 200: 115, 25, 5, 55.

`p_e = 0.70 × 0.60 + 0.30 × 0.40 = 0.42 + 0.12 = 0.54`. `κ = (0.85 − 0.54) / 0.46 = 0.674`. `p_pos = 230 / 260 = 0.885`. `p_neg = 110 / 140 = 0.786`.

Here the common category is "yes", so the weaker specific agreement is on "no". The coders' different yes rates (the bias paradox) also appear in `b` being five times `c`.
</details>

28. *Week 6 · critique.* A proposal says: "We will interview 15 members of one raiding guild, recruited by the guild leader, about why people get benched. Two coders will code all transcripts and we will report κ averaged across our 20 codes. Quotes will use players' character names so readers can follow the story." Find three problems and fix each.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Recruitment bias.** The leader will pass the call to members they trust, and benched players, the people most affected, are least likely to hear it. Add a second route to former and benched members that the leader does not see, and name the bias in the limitations.
- **Averaged kappa.** An average over 20 codes hides the rare codes that fail. Report the 2 × 2 table, κ, `p_pos` and `p_neg` per code, and build the reliability set so each reported code has enough positive cases. Also decide whether IRR fits at all: if the analysis is reflexive and interpretive, show rigor with an audit trail instead.
- **Character names.** They are identifying, since players search them and armory pages link them to histories. Use one pseudonym per person, do not report character, guild or server names, and paraphrase distinctive quotes.
</details>

---

## Week 7: Ethnography and participant observation

Model: continuous `p`; scan samples unbiased at any `T`; one-zero `E[p_10] = n(T + b)/L`, bias factor `1 + T/b` when bouts do not share blocks. [Lecture](../lectures/w07-ethnography-and-participant-observation.md).

29. *Week 7 · compute.* A focal player spends 5 bouts of 4 minutes each at the auction house during a 150-minute session, far apart. With `T = 10`, what do continuous recording, the long-run average of a scan sample and the expected one-zero score report? What is the bias factor?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Continuous 13.3%; scan average 13.3%; one-zero 46.7%; factor 3.5.

`p = 20 / 150 = 13.3%`. The scan's expected value is `p` at any interval. `E[p_10] = 5 × (10 + 4) / 150 = 70 / 150 = 46.7%`. Bias factor `1 + 10/4 = 3.5`, and `13.3% × 3.5 = 46.7%`.
</details>

30. *Week 7 · compute.* One focal character in a 150-minute session is "in conversation" during minutes 2-10, 40-44, 71-80 and 118-122 (end minute excluded). With `T = 10`, compute the continuous share, the scan at offset 0, the scan averaged over offsets 0 to 9, and the one-zero score. Compare the one-zero score with the formula `n(T + b)/L` using the mean bout length, and explain the difference.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Continuous 16.7%; scan 13.3%; scan average 16.7%; one-zero 33.3%; formula 43.3%.

Bouts of 8, 4, 9 and 4 minutes total 25 of 150, so `p = 16.7%`. Scan points 0, 10, ..., 140: only 40 and 120 fall inside a bout (minute 10 and minute 80 are end points, which are excluded), so 2 of 15 = 13.3%. Averaged over offsets it returns to 16.7%. One-zero blocks touched: 0-10, 40-50, 70-80, 110-120 and 120-130, so 5 of 15 = 33.3%, twice the truth.

The formula with `b = 6.25` gives `4 × 16.25 / 150 = 43.3%`. It is an average over where bouts fall on the grid. In this evening three of the four bouts happen to sit inside one block each, and only the last one straddles a boundary, so this draw comes in below the average. The code below checks all five numbers.

```python
BOUTS = [(2, 10), (40, 44), (71, 80), (118, 122)]
L, T = 150, 10

def scan(offset):
    points = range(offset, L, T)
    return sum(any(s <= t < e for s, e in BOUTS) for t in points) / len(points)

blocks = [(b, b + T) for b in range(0, L, T)]
one_zero = sum(any(s < b1 and e > b0 for s, e in BOUTS) for b0, b1 in blocks) / len(blocks)
b = sum(e - s for s, e in BOUTS) / len(BOUTS)
print(f"continuous {sum(e - s for s, e in BOUTS) / L:.1%}  scan {scan(0):.1%}  "
      f"scan avg {sum(scan(o) for o in range(T)) / T:.1%}  one-zero {one_zero:.1%}  "
      f"formula {len(BOUTS) * (T + b) / L:.1%}")
```

Output:

```
continuous 16.7%  scan 13.3%  scan avg 16.7%  one-zero 33.3%  formula 43.3%
```
</details>

31. *Week 7 · compute.* A tiny game has two players over a 30-day month. Player A plays 2 hours every day. Player B plays 20 minutes on one day. (a) Compute average DAU, MAU and stickiness (DAU/MAU). (b) Compute each player's share of the month's total play time. (c) Which of these numbers are one-zero scores, and what does that explain?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) DAU 1.03, MAU 2, stickiness 0.52. (b) A 99.4%, B 0.6%. (c) DAU and MAU are one-zero scores.

(a) A is active on 30 days and B on 1, so average DAU `= 31 / 30 = 1.033`. MAU = 2. Stickiness `= 1.033 / 2 = 0.517`.

(b) A plays 3,600 minutes and B 20, so A has `3,600 / 3,620 = 99.4%` of play time.

(c) MAU is a one-zero score with a 30-day block, and DAU one with a 1-day block. B's 20 minutes count as a full touch in MAU, half the base, while contributing 0.6% of play. This is the `1 + T/b` effect with a very long block and a very short bout, and it is why a stream of short-session "tourists" drags stickiness down.
</details>

32. *Week 7 · critique.* A classmate plans to join a roleplay guild for six weeks, tell no one they are researching, record the guild's voice channel with a bot, and quote members' in-character lines verbatim "because they are fictional anyway." Name Gold's role for this plan and three changes that would make it acceptable for a student project.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Complete participant. Changes: open role, no voice recording without consent, pseudonymize and paraphrase.

- Take an open role (participant-as-observer): a profile note and a message to the guild leader, with ethics approval before starting. Hidden roles need a justification a student project rarely has.
- Do not record the voice channel. It is not a public space under the AoIR context test, a bot may breach the terms of service, and recording needs explicit consent. Take jottings and same-day notes instead.
- In-character lines are still identifying. Characters, guilds and servers can be searched, and exact quotes can be traced. Pseudonymize all three and paraphrase.
</details>

---

## Week 8: Mixed methods

Model: `Δ_r = Δ_ℓ + (b_A − b_B)`, where `b_g` is group `g`'s mean of reported minus logged hours. [Lecture](../lectures/w08-mixed-methods.md).

33. *Week 8 · compute.* Survey answers linked to logs, hours per week. Veterans report 18.0 and log 20.5. New players report 15.5 and log 16.0. (a) Compute the survey gap, the log gap, each group's bias and the bias gap, and check the identity. (b) What share of the logged gap does the survey show? (c) How large a bias gap would make the survey reverse the direction?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `Δ_r = 2.5`, `Δ_ℓ = 4.5`, `b_vet = −2.5`, `b_new = −0.5`, bias gap −2.0. (b) 56%. (c) Any bias gap below −4.5.

(a) `Δ_r = 18.0 − 15.5 = 2.5`. `Δ_ℓ = 20.5 − 16.0 = 4.5`. Biases −2.5 and −0.5, gap −2.0. Identity: `4.5 + (−2.0) = 2.5`.

(b) `2.5 / 4.5 = 56%`.

(c) The survey gap is `4.5 + (b_vet − b_new)`, which turns negative once the bias gap is below −4.5 hours.
</details>

34. *Week 8 · compute.* Group A logs 20 hours a week and under-reports by 15% of its logged hours. Group B logs 16 hours and under-reports by 5%. Compute each group's reported mean, the survey gap, and the share of the true gap it shows.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A reports 17.0, B 15.2; survey gap 1.8 against a true 4.0, 45%.

A: `20 × 0.85 = 17.0`, bias −3.0. B: `16 × 0.95 = 15.2`, bias −0.8. `Δ_r = 1.8`, `Δ_ℓ = 4.0`, bias gap −2.2, and `4.0 − 2.2 = 1.8`. Share `1.8 / 4.0 = 45%`.

Compare this with the lecture's check-yourself question 2: equal proportional under-reporting only shrinks a gap, while unequal under-reporting can shrink it much more or reverse it.
</details>

35. *Week 8 · analysis.* Apply the lecture's connecting rule (the two largest under-reporters in each group plus the most accurate reporter, ties broken by id) to this linked table. Hours are reported / logged.

| Id | Group | Reported | Logged |
|---|---|---|---|
| N1 | New | 10 | 14 |
| N2 | New | 22 | 20 |
| N3 | New | 8 | 9 |
| N4 | New | 15 | 19 |
| V1 | Veteran | 20 | 26 |
| V2 | Veteran | 30 | 31 |
| V3 | Veteran | 12 | 17 |
| V4 | Veteran | 25 | 25 |

Whom do you interview, and why is N2 a useful case even though the rule does not select them?

<details>
<summary>Answer and worked solution</summary>

**Answer:** New: N1, N4 and N3. Veterans: V1, V3 and V4.

Discrepancies `d = reported − logged`: N1 −4, N2 +2, N3 −1, N4 −4; V1 −6, V2 −1, V3 −5, V4 0.

New players: the two most negative are N1 and N4, tied at −4, taken in id order. The most accurate is N3 (`|d| = 1`). Veterans: V1 (−6) and V3 (−5), and V4 (`d = 0`) as the accurate case.

N2 is the only over-reporter. The rule has no slot for over-reporting, so if over-reporting is a phenomenon of interest (for example, counting forum or Discord time as play), write a second rule for it before looking at names.
</details>

36. *Week 8 · explain.* A study surveys 2,000 players about why they quit raiding, then interviews 12 players chosen from survey respondents whose answers contradicted their logs. (a) Write the design in Morse notation and name it. (b) Name the integration method. (c) The survey says 41% quit because of schedule, and 8 of 12 interviewees mention schedule. Is reporting this as "confirmation" enough? What would you check?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `QUAN → qual`, explanatory sequential. (b) Connecting. (c) Not without checks.

(c) The interviewees were chosen for contradicting their logs, so they are not a sample of quitters, and 8 of 12 is not a prevalence. Check that both strands asked about the same construct ("schedule" as a reason versus schedule mentioned at all), who each strand reached, and whether the interviews add a mechanism. If they explain how schedule works rather than repeating that it matters, the fit is expansion.
</details>

---

## Week 9: Social network analysis of guilds

Model: degree `deg(v)/(n − 1)`, strength (sum of hours), betweenness normalised by `(n − 1)(n − 2)/2`, eigenvector by repeated neighbour sums. [Lecture](../lectures/w09-social-network-analysis-of-guilds.md).

37. *Week 9 · compute.* A 7-member guild has these co-play ties (hours in a month): Ari-Bex 4, Ari-Cal 6, Bex-Cal 5, Cal-Dov 2, Dov-Eli 3, Eli-Fen 8, Eli-Gus 7, Fen-Gus 9. Compute each member's degree centrality and strength, and the raw and normalised betweenness of Cal, Dov and Eli. Who has the lowest strength and the highest betweenness?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Dov has the lowest strength (5 hours) and the highest betweenness (raw 9, normalised 0.600).

Degree: Cal and Eli `3/6 = 0.50`; everyone else `2/6 = 0.33`. Strength: Ari 10, Bex 9, Cal 13, Dov 5, Eli 18, Fen 17, Gus 16.

The graph is two triangles joined by the path Cal-Dov-Eli. Dov lies on every shortest path between {Ari, Bex, Cal} and {Eli, Fen, Gus}: `3 × 3 = 9` pairs. Cal lies on the paths from Ari and Bex to Dov, Eli, Fen and Gus: `2 × 4 = 8`. Eli, by symmetry, 8. Normalised by `6 × 5 / 2 = 15`: Dov 0.600, Cal and Eli 0.533. Everyone else 0.

```python
from collections import deque
from itertools import combinations

TIES = [("Ari", "Bex", 4), ("Ari", "Cal", 6), ("Bex", "Cal", 5), ("Cal", "Dov", 2),
        ("Dov", "Eli", 3), ("Eli", "Fen", 8), ("Eli", "Gus", 7), ("Fen", "Gus", 9)]

def graph(ties, min_hours=0):
    adj = {p: set() for a, b, _ in ties for p in (a, b)}
    for a, b, h in ties:
        if h >= min_hours:
            adj[a].add(b)
            adj[b].add(a)
    return adj

def bfs(adj, s):
    dist, paths, q = {s: 0}, {s: 1}, deque([s])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w], paths[w] = dist[v] + 1, 0
                q.append(w)
            if dist[w] == dist[v] + 1:
                paths[w] += paths[v]
    return dist, paths

def betweenness(adj):
    sp = {v: bfs(adj, v) for v in adj}
    score = dict.fromkeys(adj, 0.0)
    for s, t in combinations(adj, 2):
        ds, ps = sp[s]
        if t not in ds:
            continue
        dt, pt = sp[t]
        for v in adj:
            if v not in (s, t) and v in ds and v in dt and ds[v] + dt[v] == ds[t]:
                score[v] += ps[v] * pt[v] / ps[t]
    return score

for threshold in (0, 3):
    btw = betweenness(graph(TIES, threshold))
    print(threshold, {v: round(x, 1) for v, x in btw.items() if x})
```

Output:

```
0 {'Cal': 8.0, 'Dov': 9.0, 'Eli': 8.0}
3 {'Eli': 2.0}
```
</details>

38. *Week 9 · compute.* In question 37's guild, the researcher sets a minimum of 3 hours for a tie. (a) Which tie disappears, and what happens to the network? (b) What are the new raw betweenness scores? (c) What does this say about reporting Dov as "the guild's broker"?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Cal-Dov (2 hours) goes, and the guild splits in two. (b) Eli 2, everyone else 0. (c) The finding does not survive a plausible threshold.

(a) Only Cal-Dov is below 3 hours. {Ari, Bex, Cal} becomes its own component, and Dov becomes a leaf attached to Eli.

(b) Pairs in different components have no path and add nothing. In the {Dov, Eli, Fen, Gus} component, Eli lies on Dov-Fen and Dov-Gus, raw 2. Dov falls from 9 to 0. The snippet in question 37 prints both thresholds.

(c) Dov's brokerage rests on one 2-hour tie. Report it at two or three thresholds (lecture section 3) and say that the "bridge" is a single weak tie, which may itself be the finding: the two halves barely play together.
</details>

39. *Week 9 · analysis.* In the lecture's 10-member guild, raise the tie threshold from 0 to 3 hours. (a) Which tie is removed? (b) Kest's raw betweenness rises from 2.67 to 8.00 (normalised 0.074 to 0.222). Explain why, in one or two sentences. (c) What does this change suggest about how you should report Kest's role?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Rowan-Mira (2 hours). (b) Rowan becomes a leaf hanging off Kest. (c) Report it as a threshold artefact.

(a) Rowan-Mira is the only tie under 3 hours. Rowan-Kest (3 hours) survives.

(b) With Rowan tied only to Kest, every shortest path from Rowan to the other 8 members runs through Kest: 8 pairs, raw 8.00, and `8 / 36 = 0.222`. Tamsin's raw score also rises, from 18.83 to 23.5, because Rowan's routes to the casual group, which used to run through Mira, now run through Kest and Tamsin.

(c) Kest's jump comes from routing an inactive guild master, not from bridging groups of active players. Report the sensitivity table and say which conclusions hold across thresholds (Tamsin at the top) and which do not (Kest's rank).
</details>

40. *Week 9 · analysis.* Four members of a 30-member guild, with rank and centralities computed from one month of co-play:

| Member | Rank | Degree | Strength (h) | Betweenness | Eigenvector |
|---|---|---|---|---|---|
| Wren | Guild master | 0.07 | 6 | 0.00 | 0.11 |
| Osk | Officer | 0.31 | 140 | 0.02 | 0.83 |
| Lio | Member | 0.21 | 38 | 0.29 | 0.40 |
| Fae | Member | 0.55 | 120 | 0.18 | 1.00 |

Match each member to one of the lecture's section 4 patterns, and say whom you would interview first to learn how the guild is led, and why.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Wren, absent guild master; Osk, officer inside one clique; Lio, bridge nobody named; Fae, raid leader without a title.

Wren has high rank and low scores everywhere. Osk has high strength but betweenness near zero. Lio has modest degree and the highest betweenness. Fae tops degree and eigenvector with high strength and member rank.

Interview Wren first. The question is about leadership, and Wren's work, if any, is invisible in co-play: it may run through recruitment, the bank or Discord (lecture section 2, "Rank tells you who holds permissions"). Fae second, as the likely working leader. Lio is the member whose departure could split the guild, which is worth a later interview.
</details>

41. *Week 9 · explain.* A student's ethics form for a guild network study says "all names will be removed, so the data are anonymous." Give two reasons that is not enough, and the protection each calls for.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Structural re-identification.** In a small guild, the only member tied to both halves is identifiable to anyone in the guild, with or without a name. Report structure in aggregate, or suppress or merge unique positions.
- **Third parties.** Every tie records information about two people, and many never consented. State how non-participants' data are handled (aggregate or pseudonymised only) and what will and will not be shared with the guild's leaders, since a list of "peripheral members" can change how people are treated.
</details>

---

## Week 10: Ethics and IRB

Model: `q = tπ + (1 − t)/2`, `π̂ = (q̂ − (1 − t)/2)/t`, `SE = sqrt(q(1 − q)/n)/t`, `ε = ln((1 + t)/(1 − t))`. [Lecture](../lectures/w10-ethics-and-irb.md).

42. *Week 10 · compute.* A randomized response survey uses `t = 0.7` and gets 1,050 "yes" answers from 3,000 respondents. Estimate `π`, its standard error and a 95% interval.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `π̂ = 0.286`, SE 0.0124, 95% interval 0.261 to 0.310.

`q̂ = 1,050 / 3,000 = 0.35`. `π̂ = (0.35 − 0.15) / 0.7 = 0.286`. `SE = sqrt(0.35 × 0.65 / 3,000) / 0.7 = 0.00871 / 0.7 = 0.0124`. Interval `0.286 ± 0.024`.
</details>

43. *Week 10 · compute.* With `t = 0.6` and a true share `π = 0.15`: (a) what are the odds factor and `ε`? (b) What share of answers will be "yes"? (c) What is P(bought given "yes") and P(bought given "no")? (d) Check (c) against the odds factor.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Factor 4, `ε = ln 4 = 1.39`. (b) `q = 0.29`. (c) 41.4% and 4.2%. (d) Posterior odds are 4 times prior odds.

(a) `(1 + 0.6) / (1 − 0.6) = 4`; `ε = 1.386`.

(b) `0.6 × 0.15 + 0.2 = 0.29`.

(c) A buyer says yes with probability `0.6 + 0.2 = 0.8`. P(bought given yes) `= 0.15 × 0.8 / 0.29 = 0.414`. P(bought given no) `= 0.15 × 0.2 / 0.71 = 0.042`.

(d) Prior odds `0.15 / 0.85 = 0.176`. Posterior odds after "yes" `0.414 / 0.586 = 0.706`, which is `4 × 0.176`.
</details>

44. *Week 10 · compute.* You plan a randomized response survey about botting with `t = 0.5` and a planning value of `π = 0.08`. How many respondents give a 95% margin of ±3 points? How many would an honestly answered direct question need, and what is the ratio?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3,516 against 315, about 11 times as many.

`q = 0.5 × 0.08 + 0.25 = 0.29`. Need `1.96 × sqrt(q(1 − q)/n) / t ≤ 0.03`, so `n ≥ (1.96 / 0.03)² × 0.29 × 0.71 / 0.25 = 4,268.4 × 0.8236 = 3,515.5`, round up to 3,516. Direct: `4,268.4 × 0.08 × 0.92 = 314.2`, round up to 315. Ratio 11.2.
</details>

45. *Week 10 · compute.* True share `π = 0.12`. Asked directly, only 60% of buyers admit it; non-buyers always say no. Randomized response uses `t = 0.5`. With `n = 1,000` per method: (a) compute each method's centre, standard error and root-mean-square error. (b) At what sample size does randomized response first have the smaller RMSE?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Direct: centre 0.072, SE 0.0082, bias −0.048, RMSE 0.0487. Randomized: centre 0.12, SE 0.0293, RMSE 0.0293. (b) 343 respondents per method.

(a) Direct centre `0.6 × 0.12 = 0.072`, `SE = sqrt(0.072 × 0.928 / 1,000) = 0.0082`, RMSE `sqrt(0.048² + 0.0082²) = 0.0487`. Randomized: `q = 0.06 + 0.25 = 0.31`, `SE = sqrt(0.31 × 0.69 / 1,000) / 0.5 = 0.0293`, and it is unbiased if players follow the instructions.

(b) Solve `sqrt(0.31 × 0.69 / n) / 0.5 < sqrt(0.048² + 0.072 × 0.928 / n)` by stepping `n`: the first `n` where it holds is 343. Below that, the direct question's small variance wins despite its bias. Above it, randomized response wins by more every time `n` grows, because the direct RMSE can never fall below 0.048.
</details>

46. *Week 10 · analysis.* Using the Common Rule's categories as the lecture presents them, give the most likely review level for each plan and the fact that decides it. (a) Counting class picks from a game's public aggregate statistics page. (b) An anonymous online survey of adult players about their favourite zone. (c) Recorded voice interviews with 10 adult raid leaders about loot disputes, quoted under pseudonyms. (d) A survey of 14- to 17-year-old players about bullying in voice chat.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Not human-subjects research. (b) Exempt under (d)(2). (c) Expedited. (d) Full board.

(a) No interaction and no identifiable private information (§46.102(e)(1)). Many institutions still want a short determination form.

(b) A survey with answers recorded so people cannot be identified fits §46.104(d)(2)(i). The institution confirms the exemption.

(c) Voice recordings are identifiable, so (d)(2)(i) fails, and loot disputes could affect reputations, so (d)(2)(ii) is doubtful. Minimal risk points to expedited review. Not recording would move it toward exempt.

(d) Minors, and a sensitive topic. Under Subpart D the survey exemption does not apply to children (§46.104(b)(3)), and bullying may be more than minimal risk. Expect full review with parental permission and assent.
</details>

---

## Week 11: Writing and presenting research

Model: a mean of `n × L` integer answers lies on a grid of step `1/(n × L)`; the check has no power once `n × L ≥ 10^D`. [Lecture](../lectures/w11-writing-and-presenting-research.md).

47. *Week 11 · compute.* Run GRIM on each mean (two decimals, rounding half up). (a) 3.72 from 28 players on one 1-to-5 item. (b) 2.64 from 25 players on a two-item scale scored as the item mean. (c) 4.18 from 60 players on a two-item scale. Give the matching sum or the nearest possible values.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Impossible; neighbours 3.71 (sum 104) and 3.75 (105). (b) Possible, sum 132. (c) Untestable.

(a) `3.72 × 28 = 104.16`. `104 / 28 = 3.714` rounds to 3.71; `105 / 28 = 3.750`. No sum gives 3.72.

(b) `n × L = 50`. `2.64 × 50 = 132`, and `132 / 50 = 2.640`.

(c) `n × L = 120`, above 100, so every two-decimal value is possible and GRIM cannot find anything.
</details>

48. *Week 11 · analysis.* A table reports raid enjoyment on one 1-to-5 item: officers `n = 8`, mean 4.25; members `n = 20`, mean 3.60; all participants `n = 28`, mean 3.72. Check the three means individually and against each other. What is the most likely error, and how would you word a query to the authors?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Officers and members pass GRIM; the overall mean fails GRIM and should be 3.79.

Officers: `34 / 8 = 4.25`, possible. Members: `72 / 20 = 3.60`, possible. Overall: impossible for `n = 28` (question 47a). The subgroups imply a total of `34 + 72 = 106` and `106 / 28 = 3.786`, which would be reported as 3.79.

Most likely a typo or a mean computed on a different `n`, for example before or after an exclusion. A query leads with the checkable facts: "The overall mean of 3.72 for 28 participants cannot arise from integer responses, and the subgroup means imply 3.79. Could you confirm the analyzed `n` and the overall mean?" No speculation about motive.
</details>

49. *Week 11 · compute.* Check two claims from fan sites. (a) "A 47.5% win rate over 55 ranked matches." (b) "A 2.5% drop rate from 120 kills."

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Impossible; the nearest values are 47.3% (26 wins) and 49.1% (27). (b) Possible, 3 drops.

(a) `26 / 55 = 47.27%` and `27 / 55 = 49.09%`. Win rates over 55 matches move in steps of 1.82 points, and none rounds to 47.5%. Either the count or the rate is wrong.

(b) `3 / 120 = 2.50%`.
</details>

50. *Week 11 · critique.* Rewrite this results sentence to the lecture's standard, and list what you need from the analysis to do it: "Players in the mentor condition felt significantly more connected to their guild (p = .02)."

<details>
<summary>Answer and worked solution</summary>

**Answer:** Direction, size in natural units, interval, then statistics with the analyzed `n`.

A model sentence: "Players assigned a mentor scored higher on the 5-item guild belonging scale than players without one (M = 3.84 vs 3.61 on a 1-to-5 scale, difference 0.23, 95% CI [0.04, 0.42], d = 0.24, n = 140 and 138)." The numbers here are placeholders that must come from your own results.

You need both group means and `n`, the difference with its interval, the SD or a standardized effect, the scale's item count and response range (so readers can run GRIM), and whether the comparison was planned. Replace "felt connected" with the name of the measure, and match the verb to the design: "caused" only if mentoring was randomized.
</details>

---

## Week 12: Peer review

Model: committee scores `S = Q + E` with reliability `ρ`; accept precision `P(both)/a`; inconsistency `2(a − P(both))`; Spearman-Brown `ρ_k = kρ₁/(1 + (k − 1)ρ₁)`. [Lecture](../lectures/w12-peer-review.md).

51. *Week 12 · compute.* A venue with 300 submissions accepts 25%. If committee scores were pure noise (`ρ = 0`), how many papers would two independent committees both accept, how many would they disagree on, and what is the accept precision?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 19 both accept, about 113 disagreements, precision 0.25.

Both accept `0.25 × 0.25 × 300 = 18.75`. Disagreements `2 × 0.25 × 0.75 × 300 = 112.5`. Precision equals `a`, 0.25.
</details>

52. *Week 12 · compute.* A single reviewer's score has reliability 0.25. (a) What is the reliability of the mean of 4 reviewers? (b) How many reviewers are needed for 0.60? (c) For 0.80?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.571. (b) 5 (4.5 rounded up). (c) 12.

(a) `4 × 0.25 / (1 + 3 × 0.25) = 1.0 / 1.75 = 0.571`.

(b) `k = ρ(1 − ρ₁) / (ρ₁(1 − ρ)) = 0.6 × 0.75 / (0.25 × 0.4) = 4.5`, so 5.

(c) `0.8 × 0.75 / (0.25 × 0.2) = 12`.
</details>

53. *Week 12 · compute.* Using the lecture's bivariate normal model, compute the accept precision and inconsistency for (a) 4 reviewers of reliability 0.25 each at 20% acceptance, and (b) a committee reliability of 0.60 at 20% and at 40% acceptance. What does (b) say about selectivity?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Precision 0.478, inconsistency 0.209. (b) 0.496 at 20% and 0.644 at 40%. More selectivity means a more arbitrary accepted list.

(a) `ρ = 0.571` from question 52. At `a = 0.20`, `P(both) = 0.0956`, precision `0.0956 / 0.20 = 0.478`, inconsistency `2 × (0.20 − 0.0956) = 0.209`. Fewer than half of the accepted papers would survive a rerun.

(b) At `ρ = 0.60`: 20% gives precision 0.496 and inconsistency 0.202; 40% gives 0.644 and 0.285. Inconsistency rises with `a`, because more papers sit near the cutoff, but precision falls as the venue gets more selective, which is the NeurIPS 2021 point.

```python
from statistics import NormalDist

N = NormalDist()

def both_accept(a, rho, steps=2000):
    z = N.inv_cdf(1 - a)
    lo, hi = z, 8.0
    h = (hi - lo) / steps
    total = 0.0
    for i in range(steps + 1):
        x = lo + i * h
        w = 1 if i in (0, steps) else (4 if i % 2 else 2)
        total += w * N.pdf(x) * (1 - N.cdf((z - rho * x) / (1 - rho * rho) ** 0.5))
    return total * h / 3

for rho, a in [(4 * 0.25 / (1 + 3 * 0.25), 0.20), (0.60, 0.20), (0.60, 0.40)]:
    b = both_accept(a, rho)
    print(f"rho={rho:.3f} a={a:.2f} precision={b / a:.3f} inconsistency={2 * (a - b):.3f}")
```

Output:

```
rho=0.571 a=0.20 precision=0.478 inconsistency=0.209
rho=0.600 a=0.20 precision=0.496 inconsistency=0.202
rho=0.600 a=0.40 precision=0.644 inconsistency=0.285
```
</details>

54. *Week 12 · critique.* Rewrite each review comment so the authors can act on it and the editor can check it. (a) "The sample is biased." (b) "The network analysis is unconvincing." (c) "I work part-time as a community manager for the game studied, but I can be objective." Where does (c) belong?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

(a) "Participants were recruited from the guild's Discord (method, paragraph 2), but the discussion generalizes to all players of the game. Please restrict the claims to the recruited population, or compare the sample's play-time distribution with the game's public figures and discuss the difference."

(b) "Section 4 reports betweenness at one tie threshold (1 hour) for one month. Please report the top five members at thresholds of 1, 3 and 5 hours and for a second month, and say which conclusions hold across all of them."

(c) This is a conflict of interest. It goes to the editor before you read further, not in the review to the authors, and the editor decides whether you review (COPE: declare, and let the editor decide).
</details>

---

## Week 13: Replication

Model: `SE = sqrt(2/n)`, `power = 1 − Φ(1.96 − δ/SE)`, `E[published d̂] = δ + SE × φ(a)/(1 − Φ(a))`; `d33 = (1.96 − 0.440) × SE_original`. [Lecture](../lectures/w13-replication.md).

55. *Week 13 · compute.* A literature studies a true effect of `δ = 0.30` with 40 players per group, and only significant positive results are published. Compute the standard error, power, mean published effect and exaggeration ratio.

<details>
<summary>Answer and worked solution</summary>

**Answer:** SE 0.224, power 26.8%, mean published `d` 0.575, exaggeration 1.92.

`SE = sqrt(2/40) = 0.224`. `δ/SE = 1.342`, so `a = 1.96 − 1.342 = 0.618`. Power `= 1 − Φ(0.618) = 0.268`. `φ(0.618) = 0.330`, so `E = 0.30 + 0.224 × 0.330 / 0.268 = 0.575`. `0.575 / 0.30 = 1.92`.

A replication should expect about half the published effect.
</details>

56. *Week 13 · compute.* An original study (40 per group) reports `d = 0.55`. A replication (200 per group) finds `d = 0.15`. Apply the lecture's five criteria, with `Δ = 0.20` for equivalence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Significance no; interval capture no; small telescopes: the effect is too small for the original; equivalence inconclusive; pooled 0.217 [0.038, 0.396].

`SE_o = 0.224`, `SE_r = sqrt(2/200) = 0.100`.

- Significance: `z = 0.15 / 0.100 = 1.50`, `p = 0.134`. Not significant.
- Interval capture: `0.15 ± 0.196 = −0.046 to 0.346`. 0.55 is outside.
- Small telescopes: `d33 = 1.520 × 0.224 = 0.340`. `z = (0.15 − 0.340) / 0.100 = −1.90`, one-sided `p = 0.029`. The replication is significantly below `d33`: the original was too small a telescope for whatever effect exists.
- Equivalence: 90% interval `0.15 ± 0.1645 = −0.015 to 0.315`, not inside ±0.20. The effect is not shown to be negligible.
- Pooling: weights `1/0.05 = 20` and `1/0.01 = 100`; `(0.55 × 20 + 0.15 × 100) / 120 = 0.217`, `SE = 1 / sqrt(120) = 0.091`, interval 0.038 to 0.396. This carries any exaggeration in the original into the result.
</details>

57. *Week 13 · compute.* You will replicate question 56's original. (a) What sample does Simonsohn's rule of thumb give? (b) If you plan instead to detect a discounted effect of 0.15 with 80% power (two-sided, α = .05), how many per group do you need? (c) Which plan answers which question?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 100 per group. (b) 698 per group. (c) The first tests the original's claim; the second tests whether a small effect exists.

(a) `2.5 × 40 = 100`.

(b) `n = 2 × ((1.96 + 0.8416) / 0.15)² = 697.7`, round up to 698.

(c) 100 per group gives about 78% power to show the effect is below `d33` if it is really zero, which answers "could the original have seen it?" Only the 698-per-group plan can tell a small real effect from none.
</details>

58. *Week 13 · analysis.* An original telemetry study with 500 players per group found `d = 0.25` for a matchmaking feature. A replication after the matchmaking system was rebuilt finds `d = 0.08`. (a) What was the original's power for an effect of 0.25? (b) If the true effect had always been 0.08, what average published effect would the filter predict at `n = 500`, and how unusual would 0.25 be? (c) Which explanation fits better?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 97.7%. (b) 0.161; an estimate of 0.25 or more would appear in about 1.5% of published studies. (c) The world changed.

(a) `SE = sqrt(2/500) = 0.0632`, `0.25 / 0.0632 = 3.95`, power `1 − Φ(1.96 − 3.95) = 0.977`. The filter has almost nothing to remove at this size.

(b) With `δ = 0.08`: `a = 1.96 − 1.265 = 0.695`, power 0.243, `E = 0.08 + 0.0632 × φ(0.695) / 0.243 = 0.161`. The chance of `d̂ ≥ 0.25` is `1 − Φ((0.25 − 0.08) / 0.0632) = 0.0036`, which is 1.5% of the 24.3% that get published.

(c) The filter does not explain a drop from 0.25 to 0.08 in a study this large. The rebuilt matchmaking is the better candidate. Compare the two samples' descriptive statistics (queue times, match quality, player mix) and describe the rebuild in the paper, as in lab 13's S10 case.
</details>

---

## Week 14: Research presentations

Model: for two independent means with the same standard error `s`, `z = distance / (sqrt(2) × s)`; paired: `SE_diff = SD × sqrt(2(1 − ρ)) / sqrt(n)`. [Lecture](../lectures/w14-research-presentations.md).

59. *Week 14 · compute.* Two independent group means, same SE. What p-value is implied by (a) SE bars with a gap of half an arm between them, and (b) 95% intervals that overlap by a quarter of an arm?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `p = 0.077`. (b) `p = 0.015`.

(a) The bars end one arm from each mean, so a half-arm gap puts the means `1 + 0.5 + 1 = 2.5` SE apart. `z = 2.5 / 1.414 = 1.77`, `p = 0.077`. It looks separate and is not significant.

(b) Each arm is `1.96s`. Overlap of `0.25 × 1.96s` puts the means `2 × 1.96s − 0.49s = 3.43s` apart. `z = 3.43 / 1.414 = 2.43`, `p = 0.015`. It looks overlapping and is significant.
</details>

60. *Week 14 · compute.* A slide compares weekly dungeon runs on two servers: 12.0 and 13.1 runs, SD 6 on each, 150 players per server. (a) Describe what 95% CI bars and SE bars would show (overlap or gap, in runs). (b) Compute `z` and `p`. (c) Write a slide title that states the evidence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) CIs overlap by 0.82 runs; SE bars have a gap of 0.12 runs. (b) `z = 1.59`, `p = 0.11`. (c) A title with the difference and its interval.

(a) `s = 6 / sqrt(150) = 0.490`. CI arms `0.960`: overlap `2 × 0.960 − 1.1 = 0.82` runs, 0.85 of an arm. SE arms 0.490: gap `1.1 − 0.98 = 0.12` runs.

(b) `z = 1.1 / (1.414 × 0.490) = 1.59`, `p = 0.112`. The SE picture invites "different", and the test does not support it.

(c) For example: "Server B players ran 1.1 more dungeons a week (95% CI −0.26 to 2.46); the data cannot tell the servers apart." The interval is `1.1 ± 1.96 × 0.693`.
</details>

61. *Week 14 · compute.* The same 225 players are measured before and after a patch. Mean raid clear time falls by 1.2 minutes; the SD in each week is 15 minutes; the correlation between a player's two weeks is 0.9. (a) Compute the paired test. (b) What would an analysis that treated the weeks as independent groups report? (c) Above what correlation is the change significant at `p < .05`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `z = 2.68`, `p = 0.0073`. (b) `z = 0.85`, `p = 0.40`. (c) `ρ > 0.813`.

(a) `SD_change = 15 × sqrt(2 × 0.1) = 6.71`, `SE = 6.71 / 15 = 0.447`, `z = 1.2 / 0.447 = 2.68`, `p = 0.0073`.

(b) `SE_diff = sqrt(2) × 15 / 15 = 1.414`, `z = 0.85`, `p = 0.40`. The overlapping weekly bars are irrelevant to a within-player change.

(c) Need `SE < 1.2 / 1.96 = 0.612`. Since `SE = sqrt(2(1 − ρ))` here, `2(1 − ρ) < 0.375`, so `ρ > 0.813`.
</details>

62. *Week 14 · compute.* A talk says: "Mentoring raised guild joining by 4.0 points for new players (SE 1.5) and 1.5 points for returning players (SE 1.5), so it only works for new players." Compute each group's `p` and the test of the difference between groups. What should the speaker have said?

<details>
<summary>Answer and worked solution</summary>

**Answer:** New players `p = 0.0077`; returning `p = 0.32`; difference 2.5 points, SE 2.12, `z = 1.18`, `p = 0.24`.

New: `z = 4.0 / 1.5 = 2.67`, `p = 0.0077`. Returning: `z = 1.0`, `p = 0.32`. Difference: `SE = sqrt(1.5² + 1.5²) = 2.12`, `z = 2.5 / 2.12 = 1.18`, `p = 0.24`.

The speaker should say that mentoring raised joining overall, and that the study cannot tell whether the effect differs between new and returning players. Plot the difference between groups with its interval (Gelman and Stern's point).
</details>
