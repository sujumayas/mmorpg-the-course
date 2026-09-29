# MMO405 · Week 14 — Research Presentations

**Why this matters:** Next week you hand in your paper, and this week you present it. Many more people will see your results slide than will read your methods section, and they will judge your finding from it in about ten seconds. If the slide shows error bars without saying which kind, a large share of your audience, including experienced researchers, will read your result backwards. This week you learn to build a talk around one claim and to draw a results figure that can't be misread.

**You will be able to:**
- Compute the p-value implied by the gap between two error bars, for standard-error bars and for 95% confidence intervals, and predict how an audience will misread each.
- Explain why overlapping bars say nothing about a within-player (paired) comparison, and compute the correct test from the correlation between periods.
- Design a results slide that shows the difference you are claiming, with its interval, in natural units, labelled so it cannot be misread.
- Plan a 12-minute research talk and a poster around one claim, and prepare the people-related parts (quotes, screenshots, network figures) so they meet your ethics approval.

**Before class:** Cumming and Finch, "Inference by Eye: Confidence Intervals and How to Read Pictures of Data" (2005), *American Psychologist* 60(2), 170-180, read the rules of eye and the figures. Belia, Fidler, Williams and Cumming (2005), "Researchers Misunderstand Confidence Intervals and Standard Error Bars," read the method and results. Association of Internet Researchers, *Internet Research: Ethical Guidelines 3.0* (2020), section 3.1.2 on informed consent, including its footnotes on publishing quotes (pp. 10-11).

**Prerequisites from earlier courses:** [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error and the 95% interval). [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (the z test for a difference). [UX201 week 14, UX research reporting](../../UX201-game-ux-and-player-psychology/lectures/w14-ux-research-reporting.md) (reporting to a team that must act; this week is the research-audience counterpart). [UX201 week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) (color and contrast). [Week 2 of this course](w02-quantitative-methods-overview.md) (effect sizes, SESOI and the four verdicts). [Week 10 of this course](w10-ethics-and-irb.md) (what your approval covers).

**Interactive:** [examples/w14-error-bar-reading.html](../examples/w14-error-bar-reading.html). Keep it open during section 2.

---

## 1. A talk is one argument

A paper can hold three findings, a long related-work section and four robustness checks. A 12-minute talk can hold one claim and the evidence for it. Everything else is backup slides for questions. Before you open slide software, write the claim as one sentence in the form your week 1 question card supports: descriptive, associational, causal or interpretive. "Guild officers are not the most central members of their guilds' chat networks" is a claim. "Guild social structure" is a topic, and a talk built on a topic turns into a tour of your data.

A plan that works for most 12-minute slots:

| Minutes | Part | What the audience should leave with |
|---|---|---|
| 0-1.5 | Hook and question | Why this question, in this game, now. One concrete observation. |
| 1.5-3.5 | What was known | Two or three prior findings and the gap. Not a literature list. |
| 3.5-6 | What you did | Design, sample, measures. The design decides the claim type, so say it out loud. |
| 6-10 | What you found | The main result figure, then at most one supporting figure or quote set. |
| 10-11.5 | What it means and what it doesn't | Claim type, limitations, the one alternative explanation you can't rule out. |
| 11.5-12 | Take-away | The claim sentence again, word for word. |

### Slide titles are claims

Write each slide title as a full sentence that states what the slide shows. "Officers ranked 4th of 12 in betweenness on average" tells the audience what to look for in the figure below. "Results" tells them nothing. Garner and Alley (2013) call this the assertion-evidence approach, a sentence headline supported by visual evidence rather than bullet lists, and make the case that it improves audience comprehension. Treat it as a reasonable default, not a law. The test is simple: if someone photographs only your slide titles, they should be able to reconstruct your argument.

### Know your room

An academic audience wants to know whether the design supports the claim, so spend your time on the design and the limitations. A studio audience wants to know what to change, so spend it on effect sizes in natural units and on what would be different in the game. UX201 week 14 covered that second room in detail. You will present to the first, and your paper will be read by both.

## 2. Worked example: two pictures of the same result

### The hook

In 2005, Belia, Fidler, Williams and Cumming invited authors of articles in psychology, behavioural neuroscience and medicine journals to a website. Each saw a figure of two group means with error bars and was asked to drag one mean until the two were just significantly different at `p < .05`. The bars were either 95% confidence intervals or standard-error bars. 473 researchers took part. The authors concluded that many leading researchers had severe misconceptions about how error bars relate to significance, did not tell confidence intervals and SE bars apart well, and did not appreciate that the rules change when the two means come from the same people measured twice.

Those are the people who will review your paper. The audience at your talk is unlikely to do better. So the question for this section is exact: for a given picture, what p-value does it imply?

### The model

Two independent groups with means `m₁` and `m₂` and the same standard error `s` for each mean (week 2 and MA102 week 13: `s = SD / sqrt(n)`). The error bars you might draw have different **arms** (half-lengths):

```
SE bar arm       = s
95% CI arm       = 1.96 × s             (large samples; slightly wider with small n)
SD bar arm       = SD = s × sqrt(n)     (describes spread of players, not precision)

SE of the difference = sqrt(s² + s²) = sqrt(2) × s
z = (m₂ − m₁) / (sqrt(2) × s)
p = 2 × (1 − Φ(|z|))
```

The key is the `sqrt(2)`. Each mean is uncertain, but the difference is not twice as uncertain, only 1.41 times as uncertain. So two 95% intervals can overlap and the difference can still be significant. Measure the distance between the means in units of `s`, and the picture gives you the p-value.

### Numbers you can check

| Picture | Means apart (in s) | z | p |
|---|---|---|---|
| SE bars overlap by one arm | 1.00 | 0.71 | 0.48 |
| SE bars just touch | 2.00 | 1.41 | 0.157 |
| SE bars with a gap of one SE | 3.00 | 2.12 | 0.034 |
| 95% CI arm reaches the other mean | 1.96 | 1.39 | 0.166 |
| 95% CIs overlap by half an arm | 2.94 | 2.08 | 0.038 |
| 95% CIs just touch | 3.92 | 2.77 | 0.0056 |

Two rows are the traps. **SE bars that just touch are not significant** (`p ≈ .16`), and people read them as "separate, so different." **95% intervals that just touch are strongly significant** (`p ≈ .006`), and people read them as "barely different." The picture that looks like `p = .05` differs by a factor of about 28 in p between the two bar types.

The exact line for `p = .05` sits at 2.77 standard errors: 95% intervals overlapping by 0.59 of an arm, or SE bars with a gap of 0.77 SE. Cumming and Finch turned these into rules of eye for independent means with groups of about 10 or more: 95% intervals overlapping by about half an arm is roughly `p = .05`, and just touching is roughly `p = .01`. For SE bars, a gap of about one arm is roughly `p = .05`. The table is the same idea computed with the normal approximation.

Now a slide. Your study compares weekly raid hours on two servers, 100 players each, SD 4.0 hours. Server A averages 6.0 hours and server B 7.2. Each mean has `s = 0.4` hours. With 95% intervals, A spans 5.22 to 6.78 and B spans 6.42 to 7.98. They overlap by 0.37 hours. The audience sees overlap and thinks "no difference." With SE bars, A spans 5.6 to 6.4 and B spans 6.8 to 7.6, with a clear gap. The audience sees separation and thinks "different." The data are the same in both pictures, and the test is `z = 1.2 / 0.566 = 2.12`, `p = .034`: the third row of the table.

The code prints the table and the slide case. It runs as shown with `.venv/bin/python`.

```python
# What p-value does a picture of two error bars imply? Two independent means, same SE.
from math import sqrt
from statistics import NormalDist

Z = NormalDist()

def p_from_distance(distance_in_se):
    """Two-sided p for two independent means `distance_in_se` standard errors apart."""
    z = distance_in_se / sqrt(2)          # SE of a difference is sqrt(2) x SE of one mean
    return 2 * (1 - Z.cdf(z))

layouts = [
    ("SE bars overlap by one arm",          1.0),
    ("SE bars just touch",                  2.0),
    ("SE bars, gap of one SE",              3.0),
    ("95% CI reaches the other mean",       1.96),
    ("95% CIs overlap by half an arm",      1.5 * 1.96),
    ("95% CIs just touch",                  2 * 1.96),
]
for name, dist in layouts:
    print(f"{name:<34} means {dist:4.2f} SE apart   p = {p_from_distance(dist):.4f}")

d05 = Z.inv_cdf(0.975) * sqrt(2)
print(f"p = .05 needs the means {d05:.2f} SE apart: "
      f"95% CIs overlap by {2 - d05 / 1.96:.2f} of an arm, SE bars have a gap of {d05 - 2:.2f} SE")
```

Output:

```
SE bars overlap by one arm         means 1.00 SE apart   p = 0.4795
SE bars just touch                 means 2.00 SE apart   p = 0.1573
SE bars, gap of one SE             means 3.00 SE apart   p = 0.0339
95% CI reaches the other mean      means 1.96 SE apart   p = 0.1658
95% CIs overlap by half an arm     means 2.94 SE apart   p = 0.0376
95% CIs just touch                 means 3.92 SE apart   p = 0.0056
p = .05 needs the means 2.77 SE apart: 95% CIs overlap by 0.59 of an arm, SE bars have a gap of 0.77 SE
```

### A visual you can move

Open [`examples/w14-error-bar-reading.html`](../examples/w14-error-bar-reading.html). The left view, "What the slide shows," draws two server means with error bars. A toggle switches the bars between SD, SE and 95% CI. The right view, "What the test says," draws the difference `m₂ − m₁` with its own 95% interval on a line with zero marked, and prints `z` and `p`.

Start with the slide case and 95% intervals. The left view shows two overlapping bars. The right view shows a difference interval that clears zero. Flip the toggle to SE: the left view now shows a gap, and the right view **does not change at all**, because the test never depended on the bars you drew. Flip to SD bars and the left view shows two huge overlapping bars, which is a correct picture of how much players vary and says nothing about the means. Drag server B's mean until the right view reads `p = .05` and look at what the left view shows in each mode. Then switch on paired mode (below).

### Cross-context recognition

**The same players before and after a patch.** You measure raid clear time for the same 400 players in the week before and the week after a patch. The mean falls from 42.0 to 40.5 minutes, and the SD in each week is 20 minutes, so each week's 95% interval has an arm of 1.96 minutes and the two intervals overlap almost completely. But the players are the same. Fast groups stay fast and slow groups stay slow, so the two weeks correlate strongly. With a correlation of 0.9 between a player's two weeks, the SD of each player's change is `20 × sqrt(2 × (1 − 0.9)) = 8.94` minutes, its SE is `8.94 / sqrt(400) = 0.447`, and `z = 1.5 / 0.447 = 3.35`, `p = .0008`. The overlapping bars were irrelevant. This is Belia et al.'s third finding: for repeated measures, the bars on each mean cannot tell you about the difference. **Plot the change itself**, with its interval. In the interactive, paired mode adds a correlation slider and shows the difference interval shrinking as the correlation rises while the left view stays the same.

**One A/B test, two regions.** A retention test shows a lift of 3.0 points in the EU (SE 1.2, `p = .012`) and 1.2 points in North America (SE 1.2, `p = .32`). The slide says "works in the EU, not in NA." But the difference between regions is 1.8 points with SE `sqrt(1.2² + 1.2²) = 1.70`, so `z = 1.06`, `p = .29`. Gelman and Stern's title states the rule: the difference between "significant" and "not significant" is not itself statistically significant. If your claim is about a difference between groups, test and plot that difference. MMO308 week 7 gave you the segment-size version of this warning.

**Win rates with error bars.** [MMO307 week 14](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md) puts error bars on class win rates. The same arithmetic applies when you compare two classes, with one change: two classes that meet each other in the same matches are not independent groups, which is the paired problem in another form.

**Forest plots.** A figure with one row per game, server or study, each a point and interval, and a combined estimate at the bottom, is a forest plot. Week 2 described Vuorre et al.'s per-game estimates combined by meta-analysis, and week 13's pooled estimate is the two-row version. A forest plot works because each row's interval is about one quantity, the effect, not about two means that the viewer must mentally subtract.

### Eyes-open design judgment

- **Draw the quantity you claim.** If the claim is a difference, the difference and its interval belong on the slide. Group means with bars can stay as context, but the interval on the difference is the evidence.
- **Always label the bars.** "Error bars: 95% CI" in the caption or the legend, every time. An unlabelled bar can be misread by a factor of 28 in p.
- **Prefer 95% intervals to SE bars for inference.** SE bars look more impressive because they are shorter. That is the problem. If a field's convention is SE, label them and consider adding the difference interval.
- **SD bars describe players, not precision.** Use them when your point is how much players vary, and say so. Don't use them to suggest a difference is or isn't real.
- **Show the data when groups are small.** With 12 interviewees scored on a scale, or 20 guilds, plot every point. A bar with an interval hides the two outliers that drive the mean.
- **Put the SESOI on the plot.** Week 2's band of `±Δ` turns the reader's question from "is it different from zero?" into "is it big enough to matter?", which is the one your audience cares about.

### Check yourself (worked example)

1. A slide shows two independent group means with SE bars that overlap by half an arm. Roughly what is p?
2. Two 95% intervals on independent means have arms of 0.5 and overlap by 0.25. Is the difference significant at `p < .05`?
3. In the patch example, what correlation between weeks would make the change not significant at `p < .05`?

<details>
<summary>Answers</summary>

1. The means are 1.5 SE apart. `z = 1.5 / 1.414 = 1.06`, `p ≈ .29`.
2. Arm 0.5 means `s = 0.5 / 1.96 = 0.255`. Overlap 0.25 means the means are `1.0 − 0.25 = 0.75` apart, which is `0.75 / 0.255 = 2.94` SE. That is half an arm of overlap, `p ≈ .038`. Yes, just.
3. Need `SE_change > 1.5 / 1.96 = 0.765`, so `SD_change > 15.3`, so `20 × sqrt(2(1 − ρ)) > 15.3`, `1 − ρ > 0.293`, `ρ < 0.71`. With a correlation below about 0.7 the change would not reach significance.

</details>

## 3. A results slide that can't be misread

Put the section 2 rules together into one checklist for your main figure.

1. **Title is the claim**, with the number: "Officers were less central than their guilds' most central member in 17 of 20 guilds."
2. **One quantity per axis, in natural units.** Hours per week, retention points, members. Standardized effects go in the caption for readers who want them.
3. **The interval is labelled** in the legend, with the level (95%) and the method if it is not the usual one (bootstrap, Wilson).
4. **The comparison is drawn**, not left to subtraction.
5. **n is on the slide**: players, guilds, sessions. The unit of analysis from week 2's section on nesting goes next to it.
6. **The SESOI or a reference line** where one exists.
7. **Readable at the back of the room.** Axis text at least as large as body text, direct labels instead of a legend where possible, and a palette that survives color-vision deficiency. UX201 week 11 has the contrast rules. Don't rely on red against green.

### Qualitative results on a slide

An interpretive claim needs its own evidence figure. A theme with three short quotes, each tagged with a pseudonym and role ("Rowan, raid leader, 4 years"), makes a better slide than a word cloud. Include the quote that complicates the theme, as week 6 asked you to in the paper. Put the count of participants who expressed the theme only if your analysis actually counted, and say what the count means. "9 of 14 interviewees" is a description of your sample, not an estimate for the population.

## 4. Presenting people

Your ethics approval (week 10) covers what you publish, and a talk is publication. Slides are photographed, recorded and posted, and a poster sits in a hall for a day. Weeks 6, 7 and 9 set the rules for pseudonymizing players, characters, guilds and network positions in your paper. Three problems are specific to presenting.

**Screenshots carry names.** A screenshot of a guild roster, a chat window or a raid frame shows character names, guild tags, server names and often chat from people who are not participants. Crop or redraw it. A redrawn schematic of the UI with pseudonyms is usually clearer anyway.

**Verbatim quotes can be searched.** A distinctive sentence from a public forum or a Discord channel can be pasted into a search engine and traced to its author in seconds. The AoIR guidelines discuss exactly this risk, re-identification through a string search, and describe one response: ask for consent to publish a specific quote at the dissemination stage, which is practical when only a handful of quotes are involved. Another response is to transform quotes or build composites from several participants. The same guidelines record an important counterpoint: altering or erasing someone's words to protect them is not automatically the ethical choice, and some people want their words and names kept. Which route you take must match your approved protocol. If your protocol says "paraphrase public chat," a verbatim quote on a slide breaks it.

**Network figures identify positions.** Week 9 showed that the only member bridging two halves of a small guild is identifiable to anyone in that guild. On a projected slide, that person may be in the audience's Discord. Show structure at the level your approval allows, and merge or suppress unique positions.

## 5. Posters, questions and limitations

### Posters

A poster is read standing, in under a minute, by someone deciding whether to talk to you. The title is the claim. The main figure is the largest thing on the page. Methods fit in a small box: design, sample, measures, claim type. Put the limitation you would want to hear about in a visible place, because it starts better conversations than a hidden one. Bring a one-page handout or a link to your preregistration and materials.

### Questions

Three habits help.

- **Repeat the question** so the room and the recording hear it, and so you have a few seconds to think.
- **Answer with the design.** "Did you control for play time?" is often a question about claim type. If your claim is associational, say so: "No, and this is an association. Play time is one of the variables that could explain it. The panel design in my future work would address that."
- **Say "I don't know"** when you don't, and say what would answer it. A made-up answer on the spot is the talk version of the researcher choices from week 2.

### Limitations that do work

"The sample was small" is not a limitation, it is a disclaimer. A useful limitation names the alternative explanation and its likely direction: "Players who answered the survey played about 40% more hours than those who didn't, so our estimate of guild satisfaction probably describes more committed players." If your study is a replication (week 13), say which features changed from the original, especially the game version.

## In-class activity (25 minutes)

Work in pairs with your own final-paper results.

1. **Draw it twice (10 min).** Sketch your main result figure as you currently have it. Then redraw it following the section 3 checklist. If your claim is a difference, the redrawn figure must show the difference and its interval.
2. **Swap and read (10 min).** Give your partner only the redrawn figure and your slide title. They write, without asking you, what the claim is, what the interval is, the implied p-value range, and one thing they cannot tell from the figure.
3. **Fix (5 min).** Compare their reading with your intended claim. Change the figure or title until the two match.

Expected output: before and after sketches, your partner's written reading, and a one-line note of what you changed.

## Common misconceptions

- **"If the error bars overlap, the difference isn't significant."** For 95% intervals on independent means, overlap of up to about half an arm is still `p < .05`. For paired data, overlap tells you nothing.
- **"If the error bars don't overlap, the difference is significant."** For SE bars that just touch, `p ≈ .16`.
- **"Significant in one group and not in the other means the groups differ."** Test the difference. In the two-region example, `p = .012` and `p = .32` give a between-region difference with `p = .29`.
- **"Changing a player's name on the slide is enough."** Screenshots, verbatim quotes and network positions all identify people. Your approved protocol decides what can be shown.

## Check yourself

1. Your slide shows two independent server means, 5.0 and 5.9 hours, each with SE 0.35. Draw the bars in your head as SE bars and as 95% CIs. Describe what each shows and compute the p-value of the difference.
2. A talk reports: "Mentoring raised guild joining by 8 points for new players (p = .01) and 3 points for returning players (p = .30), so it only works for new players." Both SEs are 3 points. What should the speaker have said?
3. You want to show a quote from a public forum thread that supports your main theme. Your ethics approval says forum text will be paraphrased. List two ways to present the evidence without breaking the approval.
4. Write a limitations sentence for a study that linked a survey (response rate 2%) to telemetry and found that guild members report higher well-being.

<details>
<summary>Answers</summary>

1. The means are `0.9 / 0.35 = 2.57` SE apart. SE bars (arms 0.35) leave a gap of 0.2 hours, so they look clearly separate. 95% CIs (arms 0.686) overlap by 0.47 hours, about 0.69 of an arm, so they look overlapping. `z = 0.9 / (0.35 × 1.414) = 1.82`, `p ≈ .069`. Neither picture should be read as "significant," and the SE picture invites exactly that misreading.
2. The difference between groups is 5 points with SE `sqrt(9 + 9) = 4.24`, `z = 1.18`, `p ≈ .24`. The speaker should say mentoring raised joining overall and that the study cannot tell whether the effect differs between new and returning players, and show the difference with its interval.
3. Paraphrase the quote on the slide and say it is a paraphrase. Or present the theme with several paraphrased excerpts and the count of posts coded to it. (A verbatim quote would need an amendment to the approval, and consent from the author if the protocol requires it.)
4. For example: "Only 2% of invited players answered, and responders may differ from non-responders in ways linked to both guild membership and well-being; the association may not hold for the wider player base and does not show that guilds raise well-being."

</details>

## Lab / assignment hook

[Lab 14, results figure audit and presentation](../labs/lab14.md). You implement the error-bar and difference functions from section 2, audit six invented results slides with them, redraw your own main figure to the section 3 checklist, and give your 12-minute research presentation with a peer review of two classmates' talks. Your slides and figure feed directly into the final paper due in week 15.

## Sources

- Belia, S., Fidler, F., Williams, J. & Cumming, G. (2005). "Researchers Misunderstand Confidence Intervals and Standard Error Bars." *Psychological Methods* 10(4), 389-396. https://doi.org/10.1037/1082-989X.10.4.389. Authors of journal articles in psychology, behavioural neuroscience and medicine; web task of adjusting two means to just-significant; 473 respondents; misconceptions about CIs vs SE bars and about repeated-measures designs.
- Cumming, G. & Finch, S. (2005). "Inference by Eye: Confidence Intervals and How to Read Pictures of Data." *American Psychologist* 60(2), 170-180. https://doi.org/10.1037/0003-066X.60.2.170. Seven rules of eye, including the overlap rules for 95% CIs and the gap rules for SE bars on independent means, and the warning about repeated measures.
- Gelman, A. & Stern, H. (2006). "The Difference Between 'Significant' and 'Not Significant' is not Itself Statistically Significant." *The American Statistician* 60(4), 328-331. https://doi.org/10.1198/000313006X152649.
- Garner, J. K. & Alley, M. P. (2013). "How the design of presentation slides affects audience comprehension: A case for the assertion-evidence approach." *International Journal of Engineering Education* 29(6), 1564-1579. Metadata checked via OpenAlex (September 2026); the lecture uses only the claim stated in the title.
- franzke, a. s., Bechmann, A., Zimmer, M., Ess, C. & the Association of Internet Researchers (2020). *Internet Research: Ethical Guidelines 3.0*. https://aoir.org/reports/ethics3.pdf. Section 3.1.2 and its footnotes: quotes identifiable through string search, consent at the dissemination stage, transforming quotes or using composites, and the point that altering someone's words without consent is not automatically ethical.
- Vuorre, M., Johannes, N., Magnusson, K. & Przybylski, A. K. (2022). "Time spent playing video games is unlikely to impact well-being." *Royal Society Open Science* 9(7), 220411. https://doi.org/10.1098/rsos.220411. Per-game estimates combined by meta-analysis (details in week 2).

## Interactive spec: examples/w14-error-bar-reading.html

**The one insight.** The bars you draw change what the audience sees and never change what the test says. Switching between SD, SE and 95% CI bars rearranges the left picture from "overlap" to "gap," while the difference interval on the right stays exactly where it is. In paired mode, the left picture stays fixed while the correlation moves the right one.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view on top).

- **Left view, "What the slide shows."** Vertical axis "weekly raid hours" in independent mode (the slide case) and "raid clear time (minutes)" in paired mode (the patch case), with every readout using the same unit (auto-range to include all bars, with padding). Two points at x positions "Server A" and "Server B" (in paired mode, "Week before" and "Week after"), each with the selected bar type drawn as a vertical line with end caps. When bars overlap, shade the overlap region lightly and print "overlap: X hours (Y of an arm)"; when they don't, print "gap: X hours". A caption under the plot always states the bar type, for example "Error bars: 95% CI".
- **Right view, "What the test says."** A horizontal number line for the difference `m₂ − m₁` (auto-range symmetric around 0 to include the interval). Zero marked. The difference as a dot with its 95% interval as a thick bar. Large-type readouts: `difference`, `SE of difference`, `z`, `p` (format `0.034`, and `< 0.0001` below that). A verdict line: "significant at .05" or "not significant at .05".
- **Below both, a readout row**: means apart in units of `s`, and the matching row of the lecture table highlighted when the layout is within 0.02 `s` of a table row.

**Controls.**

| Control | Range | Step | Default |
|---|---|---|---|
| Mean A `m₁` | 0 to 60 | 0.1 | 6.0 |
| Mean B `m₂` | 0 to 60 | 0.1 | 7.2 |
| SD of players | 0.5 to 30 | 0.1 | 4.0 |
| Players per group `n` | 5 to 2,000 | 1 | 100 |
| Bar type | SD / SE / 95% CI | toggle | 95% CI |
| Paired mode | off / on | toggle | off |
| Correlation `ρ` (paired mode only) | 0 to 0.99 | 0.01 | 0.9 |

Buttons: "Slide case" (6.0, 7.2, SD 4, n 100, independent), "Patch case" (42.0, 40.5, SD 20, n 400, paired, ρ 0.9), "Find p = .05" (moves `m₂` so that `p = .05` for the current settings), "Reset". All controls keyboard accessible with numeric readouts. Respect `prefers-reduced-motion`.

**Formulas.**

```
s = SD / sqrt(n)                          SE of one mean
arm: SD mode = SD; SE mode = s; CI mode = 1.96 × s
independent: SE_diff = sqrt(2) × s
paired:      SE_diff = SD × sqrt(2 × (1 − ρ)) / sqrt(n)
z = (m₂ − m₁) / SE_diff
p = 2 × (1 − Φ(|z|))
difference interval = (m₂ − m₁) ± 1.96 × SE_diff
means apart in s = |m₂ − m₁| / s
overlap = (arm₁ + arm₂) − |m₂ − m₁|   (positive = overlap, negative = gap)
```

The left view uses the same `s` in both modes. In paired mode, the left bars stay the per-week bars (they do not depend on `ρ`); only the right view changes. Use the large-sample 1.96 throughout, as the lecture does.

**Test values.**

| Case | Expected |
|---|---|
| Slide case, CI mode | A 5.216 to 6.784; B 6.416 to 7.984; overlap 0.368 hours (0.47 of an arm); z = 2.12; p = 0.034 |
| Slide case, SE mode | A 5.6 to 6.4; B 6.8 to 7.6; gap 0.4 hours; z and p unchanged |
| Patch case | per-week CI arm 1.96; SE_diff 0.447; z = −3.35; p = 0.0008 |
| Patch case, ρ = 0 | SE_diff 1.414; z = −1.06; p = 0.29 |
| m₁ = 0, m₂ = 3.92, SD 10, n 100 (CIs just touch) | z = 2.77; p = 0.0056 |
| m₁ = 0, m₂ = 2.0, SD 10, n 100 (SE bars just touch) | z = 1.41; p = 0.157 |

**Palette and accessibility.** Use `templates/interactive-tokens.css` inline. Server A and B differ by marker shape (circle, square) as well as color. Readouts are live text so students can copy them into the lecture table.
