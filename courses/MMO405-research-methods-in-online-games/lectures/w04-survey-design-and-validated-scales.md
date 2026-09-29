# MMO405 · Week 04 — Survey Design and Validated Scales

**Why this matters:** Telemetry tells you what players did. It can't tell you whether they felt competent, lonely or pressured by their guild. For that you ask, and the answer only counts as evidence if the questions measure one thing reliably and measure the thing you meant. The most-cited game experience questionnaire of the 2010s failed that test, and dozens of papers were built on it before anyone checked.

**You will be able to:**
- Compute Cronbach's alpha from raw item scores and from the average inter-item correlation, and predict how alpha changes when a scale gets longer or shorter.
- Show with numbers why a high alpha does not prove that a scale measures one thing.
- Critique a published game questionnaire using four kinds of validity evidence: content, structure, convergent and discriminant, and criterion.
- Design a short survey for an online game that uses validated scales correctly, including reverse-coded items, adaptation rules and consent for linking answers to telemetry.

**Before class:** Law, Brühlmann and Mekler (2018), "Systematic Review and Validation of the Game Experience Questionnaire (GEQ)", CHI PLAY 2018, read the introduction and the validation study (the free preprint on PsyArXiv has the same tables). Cortina (1993), "What Is Coefficient Alpha?", *Journal of Applied Psychology* 78(1), 98-104, read in full (seven pages). Reread Ryan, Rigby and Przybylski (2006), the measures sections of studies 1 and 4.

**Prerequisites from earlier courses:** [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (who answers a survey, weighting, Likert-type items, the PENS alphas; this week does not repeat them). [MMO301 week 9, motivation research beyond Bartle](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w09-motivation-research-beyond-bartle-yee.md) (what a factor analysis does, with Yee's components). [MMO308 week 10, player feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md) (in-game survey placement and who gets asked). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (variance and correlation).

**Interactive:** [examples/w04-alpha-length-and-structure.html](../examples/w04-alpha-length-and-structure.html). Keep it open during section 2.

---

## 1. From a question to a number

Suppose your research question is "Do players in large guilds feel less connected to their guild than players in small ones?" Guild size is in the database. Connection is not. It lives in players' heads, and you have to turn it into a number before you can compare anything.

Four terms carry the rest of the lecture.

- A **construct** is the thing you want to measure but can't observe directly, such as belonging, competence or perceived toxicity.
- An **item** is one question or statement, such as "I feel like I matter to my guild," answered on a fixed scale.
- A **scale** is a set of items whose answers you combine, usually by averaging, into one score for the construct.
- A **validated scale** is a scale whose authors published evidence that it measures the construct: its items agree with each other, its structure holds in new samples, and its scores relate to other measures the way theory predicts.

Two properties decide whether a score is evidence.

**Reliability** is consistency. If the same player answered twice under the same conditions, would the score be the same? A scale with low reliability adds noise to every comparison you make, so real differences between groups look smaller than they are.

**Validity** is whether the score measures the construct you named. A scale can be perfectly reliable and still invalid. A bathroom scale that always reads 3 kg heavy is reliable. It is not valid.

UX201 week 12 covered the practical side of asking: who answers, how to weight, how to write a Likert-type item. This week is about the measuring instrument itself. The main tool is **Cronbach's alpha**, the reliability figure almost every game survey paper reports, and the main lesson is what alpha cannot tell you.

## 2. Worked example: alpha rewards length, not unity

### The hook

Through the 2010s, a questionnaire called the **Game Experience Questionnaire (GEQ)** became one of the standard tools in games user research. Its core module has 33 items in seven components: competence, sensory and imaginative immersion, flow, tension, challenge, negative affect and positive affect. Researchers used it to compare game versions, controllers and difficulty settings.

In 2018 Effie Law, Florian Brühlmann and Elisa Mekler reviewed 73 publications that used it and ran their own validation study with 633 participants. Their findings were uncomfortable:

- Only 17 of the 73 papers (23%) reported any reliability figure.
- Papers that said they used the "unmodified" GEQ reported anywhere from 33 to 42 items.
- In their own data, the seven-factor structure did not fit well, and several components shared a lot of variance with components they were supposed to be distinct from.

Here is the surprising part. Some components with poor structure had respectable alphas. Tension scored α = .82 in their sample, well above the usual .70 threshold, and was still flagged for poor discriminant validity. Their conclusion was blunt: they did not recommend using the GEQ in its current form.

How can a scale pass the reliability check and still not measure a clean, separate thing? The answer is in the formula.

### The model

For a scale of `k` items, Cronbach's alpha compares the variance of the individual items with the variance of the total score:

```
α = k / (k − 1) × (1 − Σ σ²_i / σ²_X)
```

- `k` is the number of items.
- `σ²_i` is the variance of item `i` across respondents.
- `σ²_X` is the variance of the total score `X`, the sum of all items.

If items move together, the total varies much more than the items do separately, the ratio is small, and alpha is high. If items are unrelated, the total's variance is just the sum of the item variances, and alpha is zero.

When items are standardized (or have similar variances), alpha depends on only two numbers, the number of items `k` and the average correlation between pairs of items, `r̄`:

```
α = k × r̄ / (1 + (k − 1) × r̄)
```

This is the **standardized alpha**. It has the same form as the Spearman-Brown prophecy formula, which predicts how reliability changes when a test is lengthened. Rearranged, it lets you recover the average inter-item correlation from a published alpha:

```
r̄ = α / (k − (k − 1) × α)
```

Look at what the formula does not contain. It has no term for *which* items correlate with which. Alpha sees only the average.

### Numbers you can check

First, hold the average inter-item correlation at `r̄ = 0.30`, which is typical of attitude items, and add items.

| Items `k` | α at `r̄ = 0.30` |
|---|---|
| 2 | .462 |
| 4 | .632 |
| 6 | .720 |
| 8 | .774 |
| 10 | .811 |
| 20 | .896 |

Nothing about the items changed. Each pair correlates exactly as weakly as before. Alpha still climbs from "poor" to "excellent" by length alone.

Now build a worse scale on purpose. Take two groups of items that measure unrelated things, say "I enjoy the raid content" items and "I feel obliged to log in for my guild" items. Within each group, items correlate at `r_w = 0.60`. Between the groups, they correlate at `r_b = 0`. With `k` items split evenly, `k/2` in each group:

```
within-group pairs  = 2 × C(k/2, 2)
between-group pairs = (k/2)²
r̄ = (within pairs × r_w + between pairs × r_b) / C(k, 2)
```

| Items `k` (two groups) | Within pairs | Between pairs | `r̄` | α | Correlation between the two halves |
|---|---|---|---|---|---|
| 6 (3 + 3) | 6 | 9 | .240 | .655 | 0 |
| 12 (6 + 6) | 30 | 36 | .273 | .818 | 0 |
| 20 (10 + 10) | 90 | 100 | .284 | .888 | 0 |

A 12-item scale made of two halves that share nothing has α = .82, the same figure as GEQ Tension. A 20-item version has α = .89, which most papers would call excellent. The score you get by averaging it is a blend of two constructs, and two players with the same score can have opposite profiles.

You can check both tables with a few lines of Python:

```python
from math import comb

def alpha_std(k, rbar):
    return k * rbar / (1 + (k - 1) * rbar)

for k in (2, 4, 6, 8, 10, 20):
    print(k, round(alpha_std(k, 0.30), 3))

def rbar_two_groups(k, r_w, r_b):
    h = k // 2
    within, between = 2 * comb(h, 2), h * h
    return (within * r_w + between * r_b) / comb(k, 2)

for k in (6, 12, 20):
    r = rbar_two_groups(k, 0.60, 0.0)
    print(k, round(r, 3), round(alpha_std(k, r), 3))
```

It prints:

```
2 0.462
4 0.632
6 0.72
8 0.774
10 0.811
20 0.896
6 0.24 0.655
12 0.273 0.818
20 0.284 0.888
```

### A visual you can move

Open the interactive. The left panel shows alpha as a gauge with the conventional bands (.70 acceptable, .80 good, .90 excellent). The right panel shows the full item correlation matrix as a heat map. Start with the preset "two unrelated halves, 12 items." The gauge says good. The matrix shows two bright blocks on the diagonal and a dark off-diagonal, which is what two separate constructs look like. Now slide `k` upward. The gauge climbs into "excellent" while the blocks stay exactly as separate as before. Then set `r_b` to 0.60 so both groups correlate equally. Alpha rises again, and the matrix becomes one uniform block. Only the right panel tells those two situations apart.

### Cross-game recognition

**PENS, from a lab to an MMO community (2006).** Ryan, Rigby and Przybylski measured in-game competence and autonomy with 5-item scales in their first study (89 undergraduates playing Super Mario 64) and with 3-item versions in study 4 (730 members of an online community with MMO experience). Use the rearranged formula on study 1:

- Competence, 5 items, α = .79, gives `r̄ = .79 / (5 − 4 × .79) = .429`.
- Autonomy, 5 items, α = .66, gives `r̄ = .66 / (5 − 4 × .66) = .280`.

Now predict the 3-item versions with the same `r̄`. Competence: `3 × .429 / (1 + 2 × .429) = .69`. Autonomy: `3 × .280 / (1 + 2 × .280) = .54`. Study 4 reported .71 and .63. The competence prediction lands within .02. Autonomy came out better than predicted, which is a reminder that the samples, the game genre and the items differ between studies. The direction is what the model says. Shorter scales have lower alpha, and a 3-item autonomy scale starting from weak inter-item correlations will sit near the .60 line whatever else you do. The same arithmetic shows why the 9-item presence scale in study 1 reached α = .85 with an average correlation (`r̄ ≈ .39`) lower than competence's. Part of its alpha is its length.

**GEQ (2013 to 2018 era).** In Law, Brühlmann and Mekler's sample, alpha was .85 or higher for immersion, flow, competence and positive affect, .82 for tension, .68 for negative affect and .57 for challenge. Their structural checks told a different story from the alphas. A confirmatory factor analysis of the seven-factor model gave a comparative fit index of .879, below the usual .95 guideline for good fit. For five of the seven components, including tension and competence, the average variance explained by a component's own items was lower than the variance it shared with another component. In the terms of this worked example, the matrix did not have seven clean blocks, and alpha could not see that.

Two questionnaires, one principle. Alpha is a function of length and average correlation. It says nothing about whether the correlations form one block.

### Eyes-open design judgment

- **Report alpha, but don't stop there.** A low alpha is informative: the items don't hang together, so the average is mostly noise. A high alpha is necessary and not sufficient. Pair it with evidence of structure, such as the item correlation matrix, a factor analysis (MMO301 week 9), or **McDonald's omega**, a reliability coefficient computed from a factor model that Law and colleagues also reported.
- **Don't pad a scale to raise alpha.** Adding near-duplicate items ("I felt skilful," "I felt skilled," "I felt capable") raises alpha and wastes the player's patience. In a live game every extra item costs completions (MMO308 week 10).
- **Very high alpha can be a warning.** Above about .95 the items may be rewordings of one sentence. The scale then measures a narrow slice of the construct.
- **Short scales are a legitimate choice.** A 3-item scale with α = .65 inside a 5-minute in-game survey may beat a 10-item scale with α = .85 that half your sample abandons. Decide deliberately, and report the alpha so readers can judge.

### Check yourself (worked example)

1. A published 8-item "guild belonging" scale reports α = .84. What is its average inter-item correlation? What alpha would you expect from a 4-item short form with the same items' average correlation?
2. A student merges a 5-item flow scale and a 5-item immersion scale into one 10-item "engagement" score and reports α = .83. Name one thing alpha can't tell you here and one check that would.

<details>
<summary>Answers</summary>

1. `r̄ = .84 / (8 − 7 × .84) = .84 / 2.12 = .396`. A 4-item form gives `4 × .396 / (1 + 3 × .396) = 1.585 / 2.189 = .724`.
2. Alpha can't show whether the ten items form one block or two. Inspect the correlation matrix or run a factor analysis. If flow and immersion items correlate much more within their groups than across, report them as two scores.

</details>

## 3. Evidence of validity

Reliability is the entry fee. Validity is the argument that the score means what you say it means. Modern measurement texts treat validity as one argument built from several kinds of evidence. For game research, four kinds carry most of the weight.

**Content evidence.** Do the items cover the construct and nothing else? Ask experts and players to sort the items into the constructs they think each one measures. An item that half your raters put under "challenge" and half under "tension" will likely cross-load in the data too, which is what happened to several GEQ items. Content evidence also covers wording that no longer fits the setting. The GEQ review found researchers dropping or rewording items that did not suit board games or games with no story, often without saying which.

**Structural evidence.** Does the pattern of correlations match the claimed components? An **exploratory factor analysis** asks the data how many factors there are. A **confirmatory factor analysis** tests a structure you specify in advance and reports fit indices. A useful rule of thumb from Law and colleagues' discussion: an exploratory factor analysis needs a large sample, above about 200 and at least 5 participants per item. A class project with 40 respondents can compute alpha and inspect a correlation matrix. It cannot test a seven-factor structure.

**Convergent and discriminant evidence.** Scores should correlate with other measures of the same construct (convergent) and correlate weakly with measures of different constructs (discriminant). The GEQ failure was mostly discriminant. Tension and negative affect overlapped so much that a high tension score could not be read as "tension, as distinct from feeling bad."

**Criterion evidence.** Does the score predict something it should predict? In the PENS studies, competence and autonomy predicted enjoyment and the intention to keep playing, which is part of the case that they measure motivation-relevant experience. For an online game you have an unusually strong criterion available: behavior in telemetry. A "guild belonging" score that does not predict whether players stay in their guild over the next month has a problem, however high its alpha.

That last point is where online games give researchers an advantage over most survey fields. You can check self-report against logged behavior, but only if the player has agreed to that link (section 5).

## 4. Choosing, adapting and building scales

### Choose before you build

Building a scale properly takes item writing, expert review, a pilot, an exploratory study and a confirmatory study in a new sample. That is a thesis, not a week. For a course project, choose a published scale whose validation paper you have read. Three checks before you adopt one:

1. **Is there a validation paper?** The GEQ's core module circulated for years as a "manuscript in preparation." A scale with no peer-reviewed validation is a set of questions, not a validated scale.
2. **Was it validated on people like yours?** A scale validated on undergraduates after 20 minutes of a platform game may behave differently for guild members after three years in an MMO.
3. **Does it measure your construct?** Read the items, not the name. "Immersion" means different things in different questionnaires.

Newer instruments were built partly in response to the GEQ problems. The **Player Experience Inventory (PXI)**, published by Abeele and colleagues in 2020, was developed and validated across several studies and separates functional consequences (such as clarity of goals and ease of control) from psychosocial ones (such as mastery and immersion). Treat it the same way: read its validation paper before you trust it for your population.

### Adapt with a paper trail

You will often need to change a scale. The rules:

- **Change the context words only**, such as "the game" to "my guild" or "the raid". Keep the stem and the response format.
- **Keep every item** unless you have a reason you can state. If you drop items, say which and why, and don't claim the original validation still covers you.
- **Report the version.** The GEQ review found that "the same" questionnaire appeared with 33, 34, 35, 36, 38 or 42 items across papers. Readers could not tell which instrument had been used.
- **Re-check reliability in your sample**, every time. A published alpha is a property of the published sample, not of the items.
- **Translate with back-translation.** One bilingual person translates, a second translates back without seeing the original, and you compare. Differences show items whose meaning shifted.

### Reverse-coded items

A **reverse-coded item** is worded so that agreeing means *less* of the construct, such as PENS autonomy's "I felt controlled and pressured to be a certain way". They exist to catch **acquiescence**, the tendency of some respondents to agree with everything. Before you compute any alpha, recode them. On a scale from `lo` to `hi`:

```
recoded = lo + hi − raw
```

On a 1-to-7 scale, a 7 becomes 1 and a 2 becomes 6. If you forget, the reversed item correlates negatively with the rest and pulls alpha down. A negative item-total correlation in your output almost always means a forgotten reversal. Reverse-worded items are also harder to read, and some respondents misread them. In the lab you will see the signature of both problems.

### Item statistics you should always look at

Three per-item numbers catch most problems:

- **Corrected item-total correlation**: the correlation between an item and the sum of the *other* items. Below about .30, the item may not belong.
- **Alpha if item deleted**: the scale's alpha without that item. If deleting an item raises alpha noticeably, investigate the item. Don't delete it automatically, because every deletion is a small change to what the scale measures.
- **Floor and ceiling shares**: the share of respondents at the lowest or highest option. An item that 80% of players answer "strongly agree" can't separate them.

## 5. Fielding a survey in an online game

The sampling problems from UX201 week 12 and MMO308 week 10 apply fully. Players who are online now, who read the forum, or who click a pop-up are not a random sample of your population. Three issues are specific to research surveys in online games.

**Linking answers to telemetry.** This is the strongest design available to you. It lets you test criterion validity and ask how feelings relate to behavior. It also turns an anonymous survey into one tied to an account, which is personal data. Tell participants before they answer that their responses will be linked to their play data, what data, for what purpose and for how long. Store the link key separately from the analysis file. Under data protection law such as the EU's GDPR, pseudonymized data linked by a key is still personal data. MMO402 week 12 covers why "anonymized" account data often is not anonymous, and week 10 of this course covers ethics review.

**Minors.** Many online games allow players under 18. Your ethics board will set the rules for your institution, but expect to need parental consent for minors in addition to the player's own agreement. The practical step is to screen age before the first question and route under-age players out if your approval does not cover them.

**Attention and bots.** Long online surveys attract speeders and, if you offer rewards, automated responses. An **attention check** is an item with a correct answer ("Select 'somewhat disagree' for this item"). Use one or two, decide your exclusion rule before data collection, and report how many responses it removed. In-game rewards for completion raise response rates and bring in players who want the reward more than they want to answer carefully, so compare completion times between rewarded and unrewarded waves if you can.

A short, well-built survey for an online game has this shape:

1. Screening and consent, including the telemetry link if you use it.
2. Your primary validated scale, unmodified except for context words.
3. One or two secondary scales for convergent or discriminant evidence.
4. An attention check placed in the middle.
5. A few demographic and play-history items, only those your analysis uses.
6. One optional open question, which gives you material for the interviews of week 6.

## In-class activity (25 minutes)

In groups of three, you are given a printed 10-item "Guild Commitment Scale" invented for this class, with a correlation matrix from 150 respondents. Some items are reverse-coded and one has not been recoded.

1. (5 min) Read the items. Sort them into the constructs you think they measure (content evidence). Do all three of you agree?
2. (8 min) Using the correlation matrix, find the item that was not recoded. Estimate `r̄` for the full scale by averaging the off-diagonal cells after flipping that item's sign, and compute standardized alpha.
3. (7 min) Look for blocks. If the matrix shows two groups, compute alpha for each group separately using the formula.
4. (5 min) Write a two-sentence recommendation: report one score or two?

Expected output: the name of the unrecoded item, the full-scale alpha, the per-group alphas and the recommendation, with one number that justifies it.

## Common misconceptions

- **"α above .70 means the scale is valid."** Alpha is a reliability estimate, and even as that it assumes the items measure one thing. Two unrelated halves of 6 items each give α = .82.
- **"A validated scale is valid for my study."** Validation belongs to a population and a use. Check reliability in your own sample and read who the original sample was.
- **"Dropping the worst item always improves the scale."** It usually raises alpha, and it always changes what the scale measures. Report the change, and prefer to keep the published version when you want to compare with other studies.
- **"Survey data can't be checked."** In an online game, self-reports can be checked against logged behavior when players consent to the link. That is criterion evidence most survey fields can't get.

## Check yourself

1. A 4-item scale has α = .60. Assuming the average inter-item correlation stays the same, how many items would you need to reach α = .80?
2. A paper reports a 6-item "social play" scale with α = .71 and says it measures one construct. The correlation matrix in its appendix shows items 1 to 3 correlating around .65 with each other, items 4 to 6 around .65 with each other, and every cross-pair near .05. Compute the average correlation and explain what you would report instead.
3. You translate PENS autonomy into Spanish and get α = .48 in your sample. The item "I felt controlled and pressured to be a certain way" has a corrected item-total correlation of −.35. What happened, and what do you check first?
4. Your survey links a "loneliness in the game" score to 30 days of telemetry. Name one behavioral measure that would give criterion evidence and the direction of the relationship you would expect.

<details>
<summary>Answers</summary>

1. `r̄ = .60 / (4 − 3 × .60) = .60 / 2.2 = .273`. Solve `k × .273 / (1 + (k − 1) × .273) = .80`: `k = .80 × (1 − .273) / (.273 × (1 − .80)) = .5818 / .0545 ≈ 10.7`, so 11 items.
2. Within pairs: 2 × 3 = 6 at .65. Between pairs: 9 at .05. `r̄ = (6 × .65 + 9 × .05) / 15 = (3.90 + .45) / 15 = .29`, and `α = 6 × .29 / (1 + 5 × .29) = 1.74 / 2.45 ≈ .71`, which matches the reported figure. Alpha is acceptable, and the structure is still two blocks. Report two 3-item scores, each with its own alpha (`3 × .65 / (1 + 2 × .65) = .85`).
3. The reverse-coded item was not recoded, or it was translated in a way that flipped or blurred its meaning. First check the scoring script for the reversal. If the recode is correct, compare the translation with the back-translation for that item.
4. Examples: number of group activities joined, messages sent to guild members, days with at least one party. Expect higher loneliness scores to go with fewer social actions (a negative correlation). If the correlation is near zero, question the scale or the measure.

</details>

## Lab / assignment hook

[Lab 04, reliability and structure of a player survey](../labs/lab04.md). You receive synthetic responses from 400 players to a 10-item guild scale, write the functions for reverse coding, alpha, standardized alpha, corrected item-total correlations and alpha-if-deleted, and use them to find the unrecoded item and the scale's hidden two-part structure. Deliverable: the passing code and a one-page measurement report. The same functions go into the methods section of your proposal.

## Sources

- Law, E. L.-C., Brühlmann, F. & Mekler, E. D. (2018). "Systematic Review and Validation of the Game Experience Questionnaire (GEQ): Implications for Citation and Reporting Practice." *Proceedings of CHI PLAY 2018*, 257-270. https://doi.org/10.1145/3242671.3242683. Abstract checked via OpenAlex; details checked in the PsyArXiv preprint (https://doi.org/10.31234/osf.io/u94qt, September 2026): 73 publications, N = 633, 17 papers (23%) reporting alpha, item counts 33 to 42, the component alphas and omegas in its Table 7, CFI .879, poor discriminant validity for five components, the recommendation not to use the GEQ in its current form, and the sample-size guidance for exploratory factor analysis.
- Cronbach, L. J. (1951). "Coefficient Alpha and the Internal Structure of Tests." *Psychometrika*, 16(3), 297-334. https://doi.org/10.1007/BF02310555.
- Cortina, J. M. (1993). "What Is Coefficient Alpha? An Examination of Theory and Applications." *Journal of Applied Psychology*, 78(1), 98-104. https://doi.org/10.1037/0021-9010.78.1.98. Effects of test length and dimensionality on alpha.
- Ryan, R. M., Rigby, C. S. & Przybylski, A. (2006). "The Motivational Pull of Video Games: A Self-Determination Theory Approach." *Motivation and Emotion*, 30(4), 344-360. https://doi.org/10.1007/s11031-006-9051-8. Checked in the authors' PDF (selfdeterminationtheory.org, September 2026): study 1 with 89 undergraduates and Super Mario 64, 5-item competence (α = .79) and autonomy (α = .66) with the reverse-coded "controlled and pressured" item, 9-item presence (α = .85); study 4 with 730 online-community members with MMO experience, 3-item competence (α = .71) and autonomy (α = .63).
- Abeele, V. V., Spiel, K., Nacke, L., Johnson, D. & Gerling, K. (2020). "Development and Validation of the Player Experience Inventory." *International Journal of Human-Computer Studies*, 135, 102370. https://doi.org/10.1016/j.ijhcs.2019.102370.

## Interactive spec: examples/w04-alpha-length-and-structure.html

**Purpose.** Make visible that alpha rises with the number of items and with the average correlation, and cannot see whether the correlations form one block or two.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (gauge first).

- **Left panel, "What alpha sees".** A horizontal gauge from 0 to 1 with bands: below .60 "poor", .60 to .70 "questionable", .70 to .80 "acceptable", .80 to .90 "good", .90 and above "excellent". A marker at the current alpha, with the exact value to three decimals. Below it, a small line chart of alpha against `k` from 2 to 24 (even values only) for the current `r_w` and `r_b`, with the current `k` highlighted.
- **Right panel, "What the items do".** A `k × k` heat map of the model correlation matrix. Diagonal cells are 1. Cells within the same group are `r_w`. Cells across groups are `r_b`. Color scale from 0 (background) to 1 (accent), with a legend. Group boundaries drawn as thin lines when `r_w ≠ r_b`.

**Controls.**
- `k`, number of items: slider, even integers 2 to 24, default 12.
- `r_w`, within-group correlation: slider 0 to 0.95, step 0.05, default 0.60.
- `r_b`, between-group correlation: slider 0 to 0.95, step 0.05, default 0.00. Clamp `r_b ≤ r_w` and show a note when clamped.
- A toggle "one group" that sets `r_b = r_w` (one uniform block).
- Presets as buttons: "Two unrelated halves, 12 items" (`k = 12, r_w = .60, r_b = 0`), "One scale, 6 items" (`k = 6, r_w = r_b = .40`), "Typical attitude items, 10" (`k = 10, r_w = r_b = .30`), "Padded to 20" (`k = 20, r_w = .60, r_b = 0`).

**Readouts next to the visual.** `r̄`, α (standardized), number of within and between pairs, and the correlation between the two half-scale sums, computed as `ρ_halves = (h² × r_b) / (h + h(h−1) × r_w)` with `h = k/2`, which is 0 whenever `r_b = 0`.

**Formulas.**
- `h = k / 2`, within pairs `W = 2 × h(h−1)/2`, between pairs `B = h²`, total pairs `k(k−1)/2`.
- `r̄ = (W × r_w + B × r_b) / (k(k−1)/2)`.
- `α = k × r̄ / (1 + (k − 1) × r̄)`.
- Half-score correlation: `ρ_halves = h² × r_b / (h + h(h − 1) × r_w)`.

**Test values (must match to three decimals).**
- `k = 10, r_w = r_b = .30`: `r̄ = .300`, `α = .811`.
- `k = 6, r_w = .60, r_b = 0`: `r̄ = .240`, `α = .655`, `ρ_halves = 0`.
- `k = 12, r_w = .60, r_b = 0`: `r̄ = .273`, `α = .818`.
- `k = 20, r_w = .60, r_b = 0`: `r̄ = .284`, `α = .888`.
- `k = 6, r_w = r_b = .40`: `α = .800`, `ρ_halves = 9 × .40 / (3 + 6 × .40) = .667`.

**The one insight.** With the "two unrelated halves" preset, the gauge reads "good" while the heat map plainly shows two separate blocks. Sliding `k` up pushes the gauge to "excellent" without changing the blocks.

**Accessibility and style.** Sliders keyboard operable with visible focus. Heat map cells have a text alternative: a sentence under the map stating "k items in 2 groups of h; within r_w, between r_b". Respect `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. No game art.
