# MMO405 · Week 11 — Writing and Presenting Research

**Why this matters:** A study nobody can read, check or repeat does not count, however good the data. Your final grade in this course is a paper, and your week 14 grade is a talk. Both are judged by readers who will spend a few minutes on your abstract and a few seconds on each figure. This week is about making those minutes carry the right claim, in numbers a reader can check.

**You will be able to:**
- Compute whether a reported mean of integer data is possible given its sample size and number of items (the GRIM test), and say when the check has no power.
- Draft each section of an empirical paper about an online game (abstract, introduction, method, results, discussion) to the standard a reviewer in the field expects.
- Report a quantitative result with its effect size and interval, and a qualitative finding with its evidence, in a form another researcher could check.
- Critique the reporting of a published game study for completeness and internal consistency.

**Before class:** Appelbaum et al., "Journal Article Reporting Standards for Quantitative Research in Psychology" (2018), tables 1 and 2 (the reporting checklist), about 30 minutes. Brown and Heathers, "The GRIM Test" (2017), pp. 363-366. Pick one empirical paper from the last two years of *Game Studies* or the CHI PLAY issue of *Proceedings of the ACM on Human-Computer Interaction* and bring it to class.

**Prerequisites from earlier courses:** [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (what a confidence interval is). [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (the test for a difference). [UX201 week 14, UX research reporting](../../UX201-game-ux-and-player-psychology/lectures/w14-ux-research-reporting.md) (writing one finding and a report a team will act on; this week is the academic counterpart). Earlier in this course, [week 2](w02-quantitative-methods-overview.md) (effect sizes and preregistration) and [week 8](w08-mixed-methods.md) (joint displays).

**Interactive:** [GRIM consistency check](../examples/w11-grim-check.html). Keep it open during section 2.

---

## 1. Who reads a paper, and how

UX201 week 14 taught you to write a report for a team that must decide something by Friday. A research paper has a different reader. It is a reviewer who has to judge whether your claim follows from your evidence, and later a researcher who wants to build on it or check it. Both read in the same order. Title, abstract, figures, then the method if the figures surprise them, and the full text only if they are still interested.

That order sets three rules for the rest of this lecture.

- **The abstract must contain the result.** Not "we examine the relation between guild membership and retention" but the direction, the size and the uncertainty.
- **Every figure must stand alone.** A reader who sees only the figure and its caption should be able to say what was compared, in whom, and how sure the authors are.
- **The method must be complete enough to repeat.** Week 13 is about replication. A study whose method section omits the tie threshold in a guild network or the sessionization rule for telemetry cannot be replicated, because nobody knows what to repeat.

Behind all three sits a fourth rule that readers rarely state and always assume: the numbers agree with each other. The worked example shows how easily they don't.

## 2. Worked example: the mean that cannot exist

### The hook

A game-studies paper reports a player survey. Twenty-eight raiders rated "I enjoy our guild's raid nights" on a 1-to-5 scale, and the table gives a mean of 3.47. It looks like any other number in any other table. It is impossible. (The paper is invented. The problem is not.)

Each of the 28 answers is a whole number, so their sum is a whole number, and the mean is that sum divided by 28. A sum of 97 gives 3.464, which rounds to 3.46. A sum of 98 gives 3.500. No sum gives 3.47. Something in the table is wrong: the mean, the `n`, the number of items, or the rounding.

In 2017 Nick Brown and James Heathers turned this observation into a published check, the **GRIM test** (granularity-related inconsistency of means). They applied it to recent articles in leading psychology journals. Of the 71 articles they could test, 36 appeared to contain at least one impossible mean, and 16 contained several. They asked for the data behind 21 of them and received it for 9. In every one of those 9 they confirmed at least one reporting error, and three articles needed extensive corrections.

Those papers had passed peer review. Nobody had checked the arithmetic, because the numbers did not look wrong. This section is about writing numbers that readers can check, and checking your own before anyone else does.

### The model

Suppose each of `n` participants gives `L` whole-number answers, and you report the mean of all `n × L` answers (for a one-item question `L = 1`; for a scale scored as the mean of its items, `L` is the number of items, as in week 4). The sum of the answers is a whole number `k`. So every possible mean has the form

```
mean = k / (n × L)          for some whole number k
```

The possible means sit on a grid with step `1 / (n × L)`, the **granularity**. A mean reported to `D` decimal places is consistent if at least one grid value rounds to it.

How often can a random reported value pass? With two decimals there are 100 reported values per scale point, and there are `n × L` grid values per scale point. So when `n × L < 100`,

```
share of two-decimal values that are possible ≈ n × L / 100
```

With `n = 28` and one item, only 28% of the values between 3.00 and 4.00 can occur. When `n × L` reaches 100, the grid is finer than the reporting, every value is possible, and the test can no longer find anything.

### Numbers you can check

```python
def grim(mean, n, items=1, decimals=2):
    """Can a mean of n people's integer answers (items per person) round to `mean`?"""
    total = n * items                        # number of integer answers summed
    scale = 10 ** decimals
    target = round(mean * scale)             # the reported mean as an integer
    k0 = (target * total) // scale           # candidate sums near mean * total
    for k in range(k0 - 1, k0 + 3):
        shown = (2 * k * scale + total) // (2 * total)   # k / total, rounded half up
        if shown == target:
            return True, k
    return False, None

cases = [(3.47, 28, 1), (3.46, 28, 1), (3.47, 28, 4), (2.15, 45, 1), (4.12, 60, 1), (4.12, 150, 1)]
for m, n, L in cases:
    ok, k = grim(m, n, L)
    share = min(1.0, n * L / 100)
    print(f"mean {m:.2f}  n={n:3d}  items={L}  step={1 / (n * L):.4f}  "
          f"possible share={share:4.0%}  consistent={ok}  sum={k}")
```

Output:

```
mean 3.47  n= 28  items=1  step=0.0357  possible share= 28%  consistent=False  sum=None
mean 3.46  n= 28  items=1  step=0.0357  possible share= 28%  consistent=True  sum=97
mean 3.47  n= 28  items=4  step=0.0089  possible share=100%  consistent=True  sum=389
mean 2.15  n= 45  items=1  step=0.0222  possible share= 45%  consistent=False  sum=None
mean 4.12  n= 60  items=1  step=0.0167  possible share= 60%  consistent=True  sum=247
mean 4.12  n=150  items=1  step=0.0067  possible share=100%  consistent=True  sum=618
```

The code works in whole numbers to avoid floating-point rounding surprises. `shown` is `k / total` rounded half up to `D` decimals, computed without division error.

| Reported mean | `n` | Items `L` | Grid step | Share of 2-decimal values possible | Consistent? |
|---|---|---|---|---|---|
| 3.47 | 28 | 1 | 0.0357 | 28% | No |
| 3.46 | 28 | 1 | 0.0357 | 28% | Yes (sum 97) |
| 3.47 | 28 | 4 | 0.0089 | 100% | Yes (sum 389), and uninformative |
| 2.15 | 45 | 1 | 0.0222 | 45% | No |
| 4.12 | 60 | 1 | 0.0167 | 60% | Yes (sum 247) |
| 4.12 | 150 | 1 | 0.0067 | 100% | Yes, and uninformative |

Check two rows by hand. For 2.15 with `n = 45`: `2.15 × 45 = 96.75`, so try sums 96 and 97. `96 / 45 = 2.133` and `97 / 45 = 2.156`, which round to 2.13 and 2.16. Neither is 2.15. For 3.47 with four items: `3.47 × 112 = 388.6`, and `389 / 112 = 3.4732`, which rounds to 3.47. The same mean is impossible for a single item and fine for a four-item scale, which is why a paper must say how many items went into each mean.

### What an inconsistent mean usually means

Brown and Heathers stress that a failed check is a question, not an accusation. The common causes are mundane: a typo; an `n` that changed after exclusions while the table kept the old one; a mean computed on a subgroup; a scale averaged differently from what the method describes; rounding by truncation instead of to the nearest value. Several of those are errors in the **writing**, not the analysis. The data were fine, and the paper described them wrongly. That is the lesson for your own paper. Every number you report is a claim a reader can test against the others.

### A visual you can move

Open the interactive. The left view, **"What the table says"**, is a number line around the reported mean, with a tick at every possible value `k / (n × L)` and a band for the rounding interval of the reported value. When a tick falls in the band, the mean is possible and the band turns solid. Otherwise it is hatched. Drag `n` from 28 up to 30 and watch the ticks slide until one lands in the band. The right view, **"How much the check can see"**, plots the share of two-decimal values that are possible against `n × L`, the line `min(1, nL/100)`, with a dot at the current setting. Slide the number of items from 1 to 4 and watch the dot hit 100%, where the check goes blind.

### Cross-context recognition

**statcheck (psychology, 1985 to 2013).** Michèle Nuijten and colleagues wrote software that reads the test statistics in a paper, such as `t(58) = 2.10`, recomputes the p-value, and compares it with the reported one. Across more than 250,000 p-values in eight psychology journals, half of the papers contained at least one p-value inconsistent with its statistic, and one in eight contained a gross inconsistency that may have changed the conclusion. Gross errors were more common among values reported as significant. In our terms, the test statistic and its degrees of freedom define the only p-value that can exist, just as `n` defines the only means that can exist.

**Drop rates and win rates.** A fan site reports a "1.3% drop rate from 50 kills". With 50 kills the observed rate must be a multiple of 2%: 0%, 2%, 4% and so on. A stats page shows "53.7% win rate over 40 matches". With 40 matches, win rates move in steps of 2.5 points: 52.5%, 55.0%. Both numbers are impossible for the stated `n`. Either the count is wrong or the rate came from different data. MA102 week 13 showed you how uncertain such rates are. GRIM shows that some of them are not even possible.

**Your own tables.** The most common GRIM failure in student papers is an `n` that silently changes. You report 312 respondents in the method, drop 19 who failed an attention check, and compute means on 293, while the table still says 312. Report the analyzed `n` next to every mean, and say how many items each scale mean uses.

The three share one principle: numbers in a paper constrain each other, so any reader can recompute one from the others.

### Eyes-open design judgment

- **Report what makes checking possible.** Give `n` for every mean, the number of items per scale, the rounding, and means to two decimals. Hiding `n` does not make a paper safer. It makes it unverifiable, and reviewers notice.
- **Run the checks on yourself.** Before you submit, run GRIM on every mean of integer data and recompute every p-value from its statistic. Nuijten and colleagues suggest a "co-pilot model", in which a co-author checks the numbers independently. In this course your peer reviewer (week 12) is your co-pilot.
- **Share data and code when you can.** The strongest check is the one Brown and Heathers could do for only 9 of 21 papers: rerun the analysis. Week 13 discusses what you can share when the data belong to a studio.
- **Know the test's limits.** GRIM needs integer data, small `n × L` and known rounding. It says nothing about means of continuous measures such as minutes played, and it cannot show a consistent mean is correct. A passed check is weak evidence. A failed check is a good reason to ask.
- **Ask, don't accuse.** If you find an impossible mean in someone else's paper, write to the authors or raise it through the editor. Week 12 covers how reviewers phrase such concerns.

### Check yourself (worked example)

1. A survey of 36 players reports a mean of 2.78 on one 1-to-7 item. Is it possible?
2. The same paper reports a four-item scale mean of 5.13 for those 36 players. Can GRIM test it? Why?
3. A patch-balance post says a class won "61.4% of 57 ranked matches". Check it.

<details>
<summary>Answers</summary>

1. `2.78 × 36 = 100.08`. `100 / 36 = 2.778`, which rounds to 2.78. Possible.
2. `n × L = 144`, above 100, so every two-decimal value is possible and GRIM cannot find anything. You would need the sum of squares or the SD for a stronger check.
3. `0.614 × 57 = 35.0`, and `35 / 57 = 0.6140`, which rounds to 61.4%. Consistent.

</details>

## 3. The empirical paper, section by section

Most empirical papers in game research use some form of **IMRaD**: introduction, method, results and discussion, after a title and abstract. Humanities-leaning venues such as *Game Studies*, the open-access journal published since 2001, often use argument-led structures instead. The jobs below still have to be done somewhere.

### Title and abstract

The title names the population, the phenomenon and, if you can, the finding. "Guild membership and 30-day retention in a fantasy MMORPG: evidence from 12,000 new accounts" is better than "Guilds and players".

A good empirical abstract, 150 to 250 words, answers five questions in five to seven sentences. What problem? What did you do, with whom and how many? What did you find, with an effect size and interval? What does it mean? What can it not tell you? Write it last. Then check that every number in it appears, identically, in the results.

### Introduction

The introduction makes one argument. The question matters (to players, designers or theory), prior work has not answered it for a stated reason, and here is what this study does about it. It ends with the research question or hypotheses in the form of your week 1 question card. If you preregistered (week 2), cite the registration here.

Two faults are common in student drafts. The literature review becomes a list of papers rather than a line of reasoning toward the gap. And the introduction promises a causal answer that the design, as week 5 showed you, cannot give. Match your verbs to your claim type. "Is associated with" for associations, "caused" only for randomized or strong quasi-experimental designs.

### Method

Write the method so another team could repeat the study without emailing you. The APA Journal Article Reporting Standards (JARS, Appelbaum et al., 2018) give a checklist that most quantitative venues accept, whether or not they use APA style. For a study of an online game, reviewers will look for these in particular:

- **Game and version.** Name the game, the servers or regions, the patch or season, and the dates of data collection. MMOs change every few weeks, and a result from one patch may not hold on the next.
- **Participants and sampling.** How players were recruited, inclusion and exclusion rules, the number who started and finished, and why each person was dropped. A flow diagram helps.
- **Measures.** For each scale, the source, any changes and its reliability in your sample (week 4). For each telemetry variable, the exact rule that produced it (week 3), such as the sessionization threshold.
- **Procedure and design.** What participants did, in what order, and how conditions were assigned (week 5).
- **Analysis.** The model, the software and version, and how you handled missing data and outliers. Say which analyses were planned and which were exploratory.
- **Ethics.** Which board approved the study, with its reference number, how consent was obtained, and any waiver (week 10). Many venues now require this statement.

For qualitative and ethnographic work, the method covers the same ground in other terms: site and its boundaries, your role, how long you were there, how you recorded, how you coded and who else coded (weeks 6 and 7).

### Results

Report results in the order of your questions. For each, give the descriptive numbers first, then the test. A good result sentence names the direction, the size and the uncertainty in plain words, then gives the statistics in parentheses:

> New players on flow B played longer first sessions than those on flow A (M = 48.0 vs 42.0 minutes, difference 6.0 minutes, 95% CI [0.5, 11.5], d = 0.21).

That sentence lets a reader check your arithmetic, judge whether 6 minutes matters (week 2) and see that the interval runs from almost nothing to a sizable effect. It does not say "significantly" and let the reader guess how much.

Qualitative results report themes with their evidence. Give each theme a claim, then the observations behind it, with short pseudonymized quotes and how many participants they came from (week 6). Say where cases disagreed. In mixed-methods papers, put the joint display from week 8 here.

### Discussion

Start with the answer to the research question in one paragraph. Then relate it to prior work, where it agrees and where it does not. Give the limitations that affect the claim: the sample that cannot speak for all players, the unmeasured confounder, the single patch. Generic limitations ("further research is needed") use space without telling the reader anything. End with implications for designers or theory that follow from your evidence, and no further.

### Where game research is published

The main peer-reviewed venues for work like yours include the DiGRA conference (the Digital Games Research Association, founded in 2003, which has run its conference annually since 2014), CHI PLAY (whose full papers now appear in a CHI PLAY issue of *Proceedings of the ACM on Human-Computer Interaction*), the *Foundations of Digital Games* conference, and journals such as *Game Studies* and *Games and Culture*. Read three papers from your target venue before you write, and copy its structure and tone. Week 12 covers what happens after you submit.

## 4. Figures and tables

A figure is a claim with evidence attached. Before you draw one, write the sentence it supports. Then check the figure against it.

- **One figure, one comparison.** If a reader must compare bars across panels to see your point, rearrange the panels.
- **Label axes with units and the population.** "First-session minutes (new accounts, patch 4.2)".
- **The caption is a paragraph, not a label.** It says what is plotted, what any bars are, the `n` in each group, and the one thing to notice. [Week 14](w14-research-presentations.md) shows how badly readers misjudge error bars whose type is not stated, and how to draw a comparison so it cannot be misread.
- **Show the data when `n` is small.** Weissgerber and colleagues reviewed 703 physiology papers and found that most showed continuous data as bar or line graphs, which hide very different distributions behind the same bar. For small studies, plot every point.
- **Tables are for exact numbers.** Put descriptive statistics and model coefficients in tables, with `n` for each row. That is what lets a reader run section 2's checks. Put comparisons and trends in figures. Don't give the same numbers in both.
- **Color is not the only code.** About 8% of men of Northern European ancestry have a congenital color vision deficiency ([UX201 week 11](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md)). Use shape, pattern or labels as well.

## 5. Before you submit

Most errors that reviewers and readers find could have been found by the authors in an afternoon. Run this pass on the full draft, ideally with a co-author or your week 12 peer reviewer.

1. **The abstract test.** Cover everything but the abstract. Can a classmate state the finding, its size and its main limit? If not, rewrite the abstract.
2. **The number audit.** List every number in the abstract and check it against the results. Check every `n` against the participant flow. Run GRIM on every mean of integer data and recompute each p-value from its statistic.
3. **The replication test.** Give the method section to someone who has not seen your data and ask what they would need to redo the study. Everything they ask for goes in the paper or the supplement.
4. **The claim test.** Underline every verb that states a relation ("increases", "is associated with", "drives"). Does each match the design (week 5)?
5. **The ethics test.** Search the paper for character names, guild names, server names and verbatim chat. Each must be covered by your approval or removed (week 10).

The talk that presents the paper is the subject of [week 14](w14-research-presentations.md). Write the paper first. A clear abstract is most of a clear talk.

## In-class activity (25 minutes)

Pairs. Use the paper you brought.

1. **Abstract audit (7 min).** Mark the five questions in the abstract (problem, method, finding with size, meaning, limits). Which are missing?
2. **Number audit (10 min).** Find every table of means from integer data (Likert-type items, counts). For each, note `n` and the number of items, and run GRIM by hand or with section 2's code for at least five means. Recompute one p-value from its reported statistic if the paper gives one (MA102 week 14). Record what you could not check because a number was missing.
3. **Rewrite (8 min).** Rewrite one result sentence in the form "direction, size, interval in words, then statistics in parentheses". If the paper does not report enough to do this, list exactly what is missing.

Expected output: an abstract checklist, a number-audit table (mean, `n`, items, consistent or not or untestable), and one rewritten sentence or a list of missing numbers. If you find an inconsistency, draft a two-sentence query you would send to the authors.

## Common misconceptions

- **"If a number passed peer review, it has been checked."** Reviewers rarely recompute. Brown and Heathers found apparent impossible means in about half of the testable articles in leading journals.
- **"An impossible mean means fraud."** Usually it means a typo, a changed `n`, a subgroup or a rounding choice. Treat it as a question.
- **"Leaving out `n` and item counts keeps the table clean."** It makes the table unverifiable. Report the analyzed `n` for every mean.
- **"The abstract should make readers want to read the paper, so leave out the numbers."** Many readers stop at the abstract. If the finding is not there, they leave with only the topic.

## Check yourself

1. A paper reports that 22 players rated a dungeon at a mean of 4.05 on a single 1-to-5 item. Is that possible? What is the nearest possible reported mean on each side?
2. For how large an `n` does GRIM stop working on a single item reported to two decimals? To three decimals?
3. A method says 120 players took part, a table reports a mean of 3.18 on one item "for all participants", and the results mention excluding 9 speeders. Which `n` values would you test, and what would each result tell you?
4. A method section says, "We collected data from active players of a popular MMO." List four things a reviewer will ask for.
5. Rewrite this result sentence: "Guild members retained significantly better (p < .001)."

<details>
<summary>Answers</summary>

1. `4.05 × 22 = 89.1`. `89 / 22 = 4.0455`, which rounds to 4.05, so it is possible. If the authors truncated instead of rounding, 4.0455 would show as 4.04, which is why you check the rounding convention before flagging anything. The neighbors are `88/22 = 4.00` and `90/22 = 4.09`.
2. At `n = 100` every two-decimal value is possible. At three decimals, at `n = 1,000`.
3. Test `n = 120` and `n = 111`. `3.18 × 120 = 381.6`, and `382/120 = 3.183`, so it passes at 120. `3.18 × 111 = 352.98`, and `353/111 = 3.180`, so it also passes at 111. Both pass, so this mean cannot tell you which `n` was used. You would ask the authors, and check other means in the same table.
4. Which game, servers and patch; dates; how players were recruited and what counted as "active"; how many started and finished; the exact measures and how they were derived; ethics approval.
5. For example: "New accounts that joined a guild in week one were more likely to be active at day 30 (61% vs 30%, difference 31 points, 95% CI [27, 35], n = 12,040); this is an association, and week-one play time explains part of it (see table 3)." The numbers must come from your results.

</details>

## Lab / assignment hook

[Lab 11, from output to page](../labs/lab11.md). You write a GRIM checker and a p-value recomputer, audit the tables of an invented game-study manuscript, then write the results paragraph and 200-word abstract for your own project's main finding and run section 5's pre-submission pass on them. The results and abstract rubric is the one used for your final paper.

## Sources

- Brown, N. J. L. & Heathers, J. A. J. (2017). "The GRIM Test: A Simple Technique Detects Numerous Anomalies in the Reporting of Results in Psychology." *Social Psychological and Personality Science* 8(4), 363-369 (online October 2016). https://doi.org/10.1177/1948550616673876. 260 articles screened, 71 testable, 36 with at least one inconsistent mean, 16 with several; data requested for 21, received for 9, errors confirmed in all 9, three needing extensive correction.
- Nuijten, M. B., Hartgerink, C. H. J., van Assen, M. A. L. M., Epskamp, S. & Wicherts, J. M. (2016). "The prevalence of statistical reporting errors in psychology (1985-2013)." *Behavior Research Methods* 48(4), 1205-1226. https://doi.org/10.3758/s13428-015-0664-2. Over 250,000 p-values in eight journals; half of papers with at least one inconsistency; one in eight with a gross inconsistency; the co-pilot model.
- Weissgerber, T. L., Milic, N. M., Winham, S. J. & Garovic, V. D. (2015). "Beyond Bar and Line Graphs: Time for a New Data Presentation Paradigm." *PLOS Biology* 13(4), e1002128. https://doi.org/10.1371/journal.pbio.1002128. Review of 703 physiology papers.
- Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M. & Rao, S. M. (2018). "Journal Article Reporting Standards for Quantitative Research in Psychology: The APA Publications and Communications Board Task Force Report." *American Psychologist* 73(1), 3-25. https://doi.org/10.1037/amp0000191
- Game Studies, gamestudies.org (accessed September 2026). Open-access journal of computer game research; volume 26 in 2026, so volume 1 in 2001.
- Wikipedia, "Digital Games Research Association" (accessed September 2026). Founded 2003 in Finland; annual conference since 2014.
- Crossref records for *Proceedings of the ACM on Human-Computer Interaction*, CHI PLAY issues (for example "PACMHCI V8, CHI PLAY, October 2024 Editorial", https://doi.org/10.1145/3677053).
- The raid survey, the drop-rate and win-rate claims, and all other numbers in the examples are invented for teaching.

## Interactive spec: examples/w11-grim-check.html

**The one insight.** A mean of whole-number answers can only take values on a grid with step `1/(n × L)`. When that grid is coarser than the reported decimals, many reported means are impossible, and anyone can see it. When `n × L` passes `10^D`, every value becomes possible and the check goes blind.

**Layout.** Controls on top at 390px, on the left at 1280px. Two panels side by side at 1280px, stacked at 390px: "What the table says" and "How much the check can see". A readout underneath.

**Controls (keyboard operable, with visible values).**
- Reported mean `M`: number input, default 3.47, step 0.01 (or 0.001 when decimals = 3).
- Sample size `n`: 1 to 400, default 28 (slider plus number input).
- Items per mean `L`: 1 to 10, default 1.
- Decimals reported `D`: 1, 2 or 3, default 2.
- Rounding rule: "half up" (default), "half to even", "truncate".
- Preset buttons: "Hook (3.47, n = 28)", "Four items (3.47, n = 28, L = 4)", "Win rate (0.537, n = 40, D = 3)", "Drop rate (0.013, n = 50, D = 3)".

**Computation.** `T = nL`. Candidate sums `k` from `floor(M × T) − 1` to `floor(M × T) + 2`. For each, the shown value is `k/T` rounded to `D` decimals by the selected rule, computed in integers or with a tolerance of `1e-9` to avoid floating-point error. The mean is consistent if any shown value equals `M`. Possible share `= min(1, T / 10^D)`.

**Left panel, "What the table says".** A horizontal number line spanning `M ± 5 × max(1/T, 10^−D)`. A tick at every `k/T` in range, labelled with `k` when there is room. A band covering the rounding interval of `M` (for half up, `[M − 0.5 × 10^−D, M + 0.5 × 10^−D)`). The band is solid with the label "possible (sum = k)" when a tick falls inside, and hatched with the label "impossible for this n" when none does. Mark the nearest possible reported values on each side.

**Right panel, "How much the check can see".** Horizontal axis `n × L` on a log scale from 1 to 10,000. Vertical axis: share of `D`-decimal values that are possible, 0 to 100%. Draw `min(1, T / 10^D)` for the current `D`, and a dot at the current `T`. Shade the region `T ≥ 10^D` and label it "check has no power".

**Readout.** `T`, grid step `1/T`, possible share, consistent yes/no, the sum `k` that fits (or the two nearest possible reported values).

**Test values (the builder must check these).**
- `M = 3.47, n = 28, L = 1, D = 2`: step 0.0357, share 28%, impossible; neighbors 3.46 (k = 97) and 3.50 (k = 98).
- `M = 3.47, n = 28, L = 4`: step 0.0089, share 100%, possible with k = 389.
- `M = 2.15, n = 45`: impossible; neighbors 2.13 (96) and 2.16 (97).
- `M = 4.12, n = 60`: possible, k = 247.
- `M = 4.05, n = 22`: possible under half up (k = 89, 4.0454...), impossible under truncate.
- `M = 0.537, n = 40, D = 3`: impossible; neighbors 0.525 and 0.550.

**Accessibility and style.** Use `templates/interactive-tokens.css`. The possible and impossible states differ by fill pattern and text, not color alone. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Numbers selectable for copying. No game art or logos.
