# MMO405 · Week 12 — Peer Review

**Why this matters:** Every paper you cite passed peer review, and you will soon be doing it. In this course you review two classmates' drafts, and within a few years of graduating you may review for DiGRA or CHI PLAY. You need to know what review can and cannot certify, how to write a review that improves a paper, and how to read your own rejections without taking them as a verdict on your worth. The field's own experiments show that a large part of any accept-or-reject decision is chance, and this week you compute how large.

**You will be able to:**
- Compute how often two independent committees agree on accepted papers, from the reliability of their scores and the acceptance rate, and use it to explain the NeurIPS 2014 and 2021 experiments.
- Predict how the number of reviewers per paper changes that agreement, using the Spearman-Brown formula from week 4.
- Write a review of an empirical game-research paper that separates major from minor concerns and makes every request checkable.
- Apply reviewer ethics (confidentiality, conflicts of interest, bias) and write a point-by-point response to reviewers.

**Before class:** Cortes and Lawrence, "Inconsistency in Conference Peer Review: Revisiting the 2014 NeurIPS Experiment" (2021), sections 1 to 3 (about 20 minutes). Committee on Publication Ethics (COPE), *Ethical Guidelines for Peer Reviewers* (2013, revised 2017), the whole document. Reread your notes on Spearman-Brown from [week 4](w04-survey-design-and-validated-scales.md).

**Prerequisites from earlier courses:** [MMO402 week 7, justice systems](../../MMO402-emergent-society-governance-and-ethics/lectures/w07-justice-systems-reports-reviews-appeals.md) (review panels as a binomial vote; this week is the continuous-score version for papers). [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md). [UX201 week 9, heuristic evaluation](../../UX201-game-ux-and-player-psychology/lectures/w09-heuristic-evaluation-for-games.md) (several evaluators find more than one). Earlier in this course, [week 4](w04-survey-design-and-validated-scales.md) (reliability and Spearman-Brown) and [week 11](w11-writing-and-presenting-research.md) (what a complete method and result look like).

**Interactive:** [examples/w12-review-lottery.html](../examples/w12-review-lottery.html). Keep it open during section 2.

---

## 1. What peer review is for

**Peer review** is the practice of asking researchers in the same field to judge a manuscript before it is published. An **editor** (at a journal) or an **area chair** or **associate chair** (at a conference) picks two to four reviewers, reads their reports and makes the decision. Journals usually offer four outcomes: accept, minor revisions, major revisions, reject. Conferences run on a fixed timetable, often with a single round of reviews, sometimes a short **rebuttal** in which authors answer the reviewers or one round of revisions, and then accept or reject.

Review has two jobs that pull against each other.

- **Gatekeeping.** Decide whether the work meets the venue's bar: the claim follows from the evidence, the method is sound and reported, the contribution is new enough.
- **Improvement.** Tell the authors what would make the work better, whether or not it is accepted.

Reviewers see the full manuscript and often know more than the authors about some part of it. They do not see the data, rarely rerun the analysis, and spend a few hours on work that took months. Peer review is a check on reasoning and reporting. It cannot certify that a result is true. Week 13, on replication, is about what happens after publication.

### Who knows whom

In **single-blind** review, reviewers know who the authors are, and authors do not know the reviewers. In **double-blind** review, neither side knows. **Open review** publishes reviews and sometimes names. Venues differ, and each call for papers states its policy.

The choice matters. In 2017, Andrew Tomkins, Min Zhang and William Heavlin ran a controlled experiment at the WSDM computer-science conference, where each paper had two reviewers who could see author information and two who could not. Single-blind reviewers bid on 22% fewer papers and were more likely to recommend papers from famous authors, top universities and top companies. The estimated odds multipliers were 1.63, 1.58 and 2.10. Double-blind review does not remove bias. It removes one channel for it.

## 2. Worked example: how much of acceptance is luck?

### The hook

In 2014 the program chairs of NeurIPS, a large machine-learning conference, ran an experiment. From 1,678 submissions they chose about 10%, 170 papers, and had each reviewed by two independent committees, each with its own area chairs and at least three reviewers per paper. After withdrawals, 166 papers completed the experiment.

| | Committee 1 accepts | Committee 1 rejects |
|---|---|---|
| **Committee 2 accepts** | 22 | 22 |
| **Committee 2 rejects** | 21 | 101 |

The committees disagreed on 43 of 166 papers (25.9%). Of the 43 papers committee 1 accepted, committee 2 accepted only 22, about half. Had the conference been run by the other committee, about half of its accepted papers would have been different.

Most researchers, asked beforehand, expected less disagreement. The question is whether this means review is broken, or whether it is what any honest measurement with this much noise would produce.

### The model

Give each paper a **quality** `Q`, meaning whatever score an infinitely large panel of reviewers would agree on. Standardize it so `Q` has mean 0 and standard deviation 1 across submissions. A committee does not see `Q`. It sees its own **score** `S = Q + E`, where `E` is noise: this reviewer's taste, mood, expertise and reading time. Two committees have independent noise.

Two numbers describe the process.

- `ρ` (rho), the **reliability** of a committee's score: the share of the variance in `S` that comes from `Q`. It is also the correlation between the scores two independent committees give the same papers. You met reliability as Cronbach's alpha in week 4.
- `a`, the **acceptance rate**. Each committee accepts the papers whose scores fall in its top share `a`.

With normal distributions, the chance that both committees accept a paper is a bivariate normal probability, `P(both) = P(S₁ > z and S₂ > z)`, where `z` is the cutoff that leaves share `a` above it. Two summaries follow.

```
accept precision = P(both) / a           (share of one committee's accepts the other also accepts)
inconsistency    = 2 × (a − P(both))     (share of all papers where they disagree)
```

At the two extremes you can check by hand. If `ρ = 1`, the committees agree perfectly: precision 1, inconsistency 0. If `ρ = 0`, decisions are coin flips weighted by `a`. Committee 2 accepts a random share `a` of committee 1's accepts, so precision equals `a`, and inconsistency is `2a(1 − a)`. With `a = 0.26`, that is precision 0.26 and inconsistency 0.385.

Where does `ρ` come from? If each reviewer's score has reliability `ρ₁` and a committee averages `k` reviewers, the committee's reliability follows the **Spearman-Brown formula** from week 4:

```
ρ_k = k × ρ₁ / (1 + (k − 1) × ρ₁)
```

### Numbers you can check

Cortes and Lawrence report that the mean calibrated scores of the two committees correlated at 0.55 across the 166 papers. The committees' own acceptance rates were about 26% (43 and 44 of 166). Put `ρ = 0.55` and `a = 0.26` into the model.

```python
from statistics import NormalDist

N = NormalDist()

def both_accept(a, rho, steps=2000):
    """P(both committees accept) when each accepts its top share a and
    their scores correlate rho (bivariate normal, Simpson's rule)."""
    z = N.inv_cdf(1 - a)
    lo, hi = z, 8.0
    h = (hi - lo) / steps
    total = 0.0
    for i in range(steps + 1):
        x = lo + i * h
        w = 1 if i in (0, steps) else (4 if i % 2 else 2)
        total += w * N.pdf(x) * (1 - N.cdf((z - rho * x) / (1 - rho * rho) ** 0.5))
    return total * h / 3

print(" rho   accept  both   precision  inconsistency")
for rho in (0.0, 0.3, 0.55, 0.75, 0.9):
    for a in (0.26, 0.10):
        b = both_accept(a, rho)
        print(f"{rho:4.2f}  {a:5.2f}  {b:.3f}  {b / a:8.3f}  {2 * (a - b):10.3f}")
```

Output:

```
 rho   accept  both   precision  inconsistency
0.00   0.26  0.068     0.260       0.385
0.00   0.10  0.010     0.100       0.180
0.30   0.26  0.101     0.390       0.317
0.30   0.10  0.022     0.216       0.157
0.55   0.26  0.134     0.517       0.251
0.55   0.10  0.036     0.356       0.129
0.75   0.26  0.167     0.644       0.185
0.75   0.10  0.051     0.512       0.098
0.90   0.26  0.202     0.776       0.116
0.90   0.10  0.069     0.689       0.062
```

| Committee reliability `ρ` | Precision at 26% acceptance | Inconsistency at 26% | Precision at 10% acceptance |
|---|---|---|---|
| 0 (coin flips) | 0.26 | 0.385 | 0.10 |
| 0.30 | 0.39 | 0.317 | 0.22 |
| **0.55 (NeurIPS 2014)** | **0.52** | **0.251** | **0.36** |
| 0.75 | 0.64 | 0.185 | 0.51 |
| 0.90 | 0.78 | 0.116 | 0.69 |

Compare the bold row with the experiment. The model predicts precision 0.52 and inconsistency 0.251. The committees achieved 22/43 = 0.51 and 22/44 = 0.50 precision, and 43/166 = 0.259 inconsistency. A plain noise model with the measured correlation reproduces the result within sampling error. Nothing had to be broken. A score correlation of 0.55 is simply this noisy when you cut at the top quarter.

Now the reviewers. If each committee averaged three reviewers, Spearman-Brown run backward gives a single reviewer's reliability: `ρ₁ = ρ₃ / (3 − 2ρ₃) = 0.55 / 1.9 = 0.29`. Forward again:

| Reviewers per committee `k` | 1 | 3 | 5 | 10 | 22 |
|---|---|---|---|---|---|
| Committee reliability `ρ_k` | 0.29 | 0.55 | 0.67 | 0.80 | 0.90 |

To reach `ρ = 0.9`, where about three in four accepted papers would survive a rerun, you would need about 22 reviewers per paper. (With `ρ₁` rounded to 0.29, 22 reviewers give 0.8999, so a planner that demands at least 0.900 answers 23, as lab 12's does.) No venue can afford that.

### A visual you can move

Open the interactive. The left view, **"One committee"**, shows 500 simulated submissions as dots, with true quality across and the committee's score up, and a cutoff line at the acceptance rate. Accepted papers are filled. The right view, **"Two committees"**, plots committee 1's score against committee 2's for the same papers, with both cutoffs. The top-right box holds the papers both accept. Set reviewers to 3 and single-reviewer reliability to 0.29, and the counts in the four boxes land near the NeurIPS table. Now slide the acceptance rate from 26% down to 10%. The top-right box empties faster than either committee's accepted set, and precision falls. That is the NeurIPS 2021 finding, drawn.

### Cross-context recognition

**NeurIPS 2021.** Beygelzimer, Dauphin, Liang and Wortman Vaughan repeated the experiment at much larger scale, again sending 10% of submissions to two committees. The committees disagreed on 23% of papers, and about half of the accepted list would change on a rerun, the same as in 2014 although the conference had grown many times over. Their analysis suggested that making the conference more selective would increase the arbitrariness. In our table, dropping `a` from 0.26 to 0.10 at `ρ = 0.55` cuts precision from 0.52 to 0.36.

**Ludum Dare game jams.** In Ludum Dare, every participant who submits a game may rate other entries from 1 to 5 stars in categories such as Fun, Innovation and Overall, and the rankings come from these peer ratings. The rules add a **Coolness** score: the more games you rate, the more your own game is shown to raters. That is a venue designing for Spearman-Brown. A game's average from 5 ratings has much lower reliability than one from 40, so its rank is closer to a lottery. By encouraging rating, the jam raises `k` for everyone. The same model tells you that two games a few places apart in the results are, for practical purposes, tied.

**Ban review panels (MMO402 week 7).** A game's report-review panel asks the same question in binary form: how many independent judges before a decision is stable? MMO402 used the binomial distribution for yes-or-no votes. This week's model is the continuous version, with scores instead of votes. Both say that adding judges helps with diminishing returns, and that correlated judges (reviewers who share a blind spot, or players who follow the first vote) help less than their number suggests.

In each case the decision is a noisy score cut at a threshold, and the model tells you how much of the outcome is signal.

### Eyes-open design judgment

- **Noise is not the same as bias, and review has both.** The model treats reviewer error as random. The WSDM experiment shows systematic error too. More reviewers average out noise. They do not average out a shared bias.
- **Review is better at the bottom than the top.** Cortes and Lawrence found that for rejected papers that were later published elsewhere, review scores related to later citations, but for accepted papers they did not. Their summary was that the process was good at identifying poor papers and poor at identifying the best. A reviewer's "reject" on a paper with a clear flaw carries more information than an "accept" on a borderline one.
- **More reviewers is expensive and slow to pay off.** Going from 3 to 5 reviewers raises `ρ` from 0.55 to 0.67. Better instructions, calibration of each reviewer's scale and reviewers matched to the topic can raise `ρ₁` itself, which is cheaper.
- **Tell authors what the noise means.** A venue with 25% acceptance and `ρ = 0.55` rejects many papers that another committee would accept. Resubmitting a solid paper after revision is a rational response, not denial. The NeurIPS 2021 authors made the same point.
- **As a reviewer, you are one noisy measurement.** Your score will be averaged with others and cut at a threshold. The part of your review that survives the noise is the reasons, so spend your effort there.

### Check yourself (worked example)

1. A venue accepts 20% of papers and its committee scores are pure noise (`ρ = 0`). What share of papers would two committees disagree on? What is the accept precision?
2. A single reviewer's reliability is 0.4. What is the reliability of the mean of 4 reviewers? How many reviewers give 0.8?
3. Using the lecture's table, a venue with `ρ = 0.75` changes its acceptance rate from 26% to 10%. By how much does the accept precision change, and why might the venue's organizers still prefer the lower rate?

<details>
<summary>Answers</summary>

1. Inconsistency `2 × 0.2 × 0.8 = 0.32`, precision 0.20.
2. `ρ₄ = 4 × 0.4 / (1 + 3 × 0.4) = 1.6 / 2.2 = 0.727`. For 0.8, `k = 0.8 × 0.6 / (0.4 × 0.2) = 6` reviewers.
3. From 0.644 to 0.512, a drop of about 0.13. The organizers may want a smaller program or a higher average quality among accepted papers. The price is that the accepted list is more arbitrary at the margin, and they should say so to authors.

</details>

## 3. Writing a review

The review is the part of the process you control. A good one helps the editor decide and helps the authors improve, and both depend on reasons rather than scores.

### Structure

Most venues give a form. Whatever the form, write these parts.

1. **Summary (3 to 5 sentences).** What the paper claims, with what evidence. Write it in your own words. If you cannot, that is your first concern. Authors often learn more from seeing how a reviewer summarized them than from the rest of the review.
2. **Strengths.** What is new, well done or useful. Be specific ("the linked survey and telemetry design lets the authors test self-report bias directly").
3. **Major concerns.** Problems that, unfixed, mean the claim does not follow from the evidence. Number them. For each, say what the problem is, why it matters for the claim, and what would resolve it.
4. **Minor concerns.** Clarity, missing details, presentation. A list is fine.
5. **Recommendation and confidence.** Your recommendation, and how sure you are, including the parts outside your expertise.

### What to check in a game-research paper

Use the weeks of this course as a checklist. Each is a place where papers in this field go wrong.

- **Question and claim type (week 1).** Does the paper claim causation from a design that supports only association?
- **Sample (weeks 1, 2 and 4).** Who answered, how they were recruited, and whom the conclusions are generalized to. A Reddit sample does not speak for a game's player base.
- **Measures (weeks 3 and 4).** Scale reliability in this sample. For telemetry, the exact derivation rules and the game version.
- **Effect size and uncertainty (weeks 2 and 14).** Every key result with a size and an interval. Figures that show the comparison claimed, with bars labelled.
- **Internal consistency (week 11).** Means of integer data that pass GRIM, p-values that match their statistics, and `n` values that add up.
- **Qualitative warrant (weeks 6 and 7).** How themes were built, how many participants support each, and the researcher's role in the field.
- **Ethics (week 10).** Approval, consent and data protection stated and adequate. Could any published detail identify a player or guild?
- **Reproducibility (week 13).** Is the method complete enough to repeat? Are materials, code or data available, and if not, why not?

### Make every request checkable

Compare two versions of the same concern.

> The sample may not be representative.

> The participants were recruited from the game's subreddit (method, paragraph 2), but the discussion generalizes to "players of the game". Subreddit readers are likely to be more engaged than the player base. Please either restrict the claims to the recruited population, or compare the sample's playtime distribution with any public figures for the game and discuss the difference.

The second tells the authors where, why and what to do, and lets the editor check in the next round whether they did it. Every major concern should end in a request of this kind.

### Tone

Write to the authors as you would like a reviewer to write to you. Criticize the work, not the people ("the analysis does not account for", not "the authors failed to"). Do not demand the paper you would have written. Ask for new studies only when the claim cannot stand without them. If you suggest citations, suggest them because the paper needs them, and be especially careful when they are your own.

## 4. Reviewer ethics

The COPE guidelines for peer reviewers set out duties that most game-research venues adopt. The core ones, in plain terms:

- **Confidentiality.** A manuscript under review is confidential. Do not share it, discuss its content, or use its ideas or data in your own work before it is published. Check the venue's policy before pasting any part of a manuscript into an online tool, because that is sharing it.
- **Conflicts of interest.** Declare to the editor any relationship that could bias you: a recent collaborator, your own student, a competitor on the same question, a financial stake in the game studied. When in doubt, declare and let the editor decide.
- **Competence and time.** Accept a review only if you have the expertise and can deliver on time. Say which parts you are not qualified to judge.
- **Fairness.** Judge the work on its merits. Double-blind review helps, but you will sometimes guess who the authors are. Do not try to find out.
- **No contact.** Do not contact the authors directly. Everything goes through the editor.

Game research has one extra risk. Many reviewers are also players, and some work for studios. A paper criticizing a game you love, or a studio you work for, is a conflict you must at least declare.

## 5. Responding to reviewers

When the reviews come back, wait a day before replying. Then write a **response letter** that quotes each reviewer comment and answers it directly below: what you changed and where (page and line), or why you did not change it. Reviewers read these letters closely, and a clear one makes a second round shorter.

Three rules. Answer every comment, including those you disagree with. Disagree with evidence, not tone ("we kept the full sample because excluding the 40 players with missing week-one data would bias the estimate toward engaged players; table S2 shows the result is unchanged without them"). Make the change in the paper, not only in the letter, because future readers see only the paper.

## In-class activity (25 minutes)

Groups of three. Each group receives a two-page extract of an invented paper, "Voice chat increases guild retention in a fantasy MMORPG", with its abstract, method and one results figure.

1. **Summarize (5 min).** Each person writes a three-sentence summary alone. Compare. Where your summaries differ, the paper is unclear.
2. **Review (12 min).** Individually, list at most three major concerns, each ending in a checkable request, using section 3's checklist. Then score the paper from 1 (reject) to 5 (accept).
3. **Calibrate (8 min).** Put the three scores side by side. Compute their mean and range. Discuss one concern only one person found. Would you change your score after hearing it?

Expected output: three summaries, a merged list of major concerns with requests, three scores and a one-sentence note on how much they moved after discussion.

## Common misconceptions

- **"Peer-reviewed means the result is true."** It means a few experts found the reasoning and reporting acceptable. Reviewers rarely see data and do not rerun analyses (week 13).
- **"If the committees disagree half the time on accepted papers, reviewers are doing a bad job."** A score correlation of 0.55, cut at the top quarter, produces that disagreement with no failure anywhere. The fix is higher reliability or less weight on single decisions, not blame.
- **"A good reviewer finds as many problems as possible."** A good reviewer finds the problems that matter for the claim and says how to fix them. Fifty minor points bury the one major one.
- **"Double-blind review removes bias."** It removes one source, knowledge of the authors. Reviewers still bring preferences about methods, topics and writing.

## Check yourself

1. Two committees each accept 30% of 200 papers. With pure noise, how many papers would you expect both to accept? How many disagreements?
2. A journal wants two reviewers' mean to reach reliability 0.7. What single-reviewer reliability does that require?
3. Your paper was rejected with scores 2, 3 and 4 out of 5 from three reviewers. Using this lecture's model, what does the spread tell you about how to read the decision?
4. Rewrite this concern so it is checkable: "The statistics are weak."
5. You are asked to review a paper that studies harassment in a game where you are a volunteer moderator. What do you do?

<details>
<summary>Answers</summary>

1. Both accept `0.3 × 0.3 × 200 = 18`. Disagreements `2 × 0.3 × 0.7 × 200 = 84`.
2. `0.7 = 2ρ₁ / (1 + ρ₁)` gives `ρ₁ = 0.7 / 1.3 = 0.54`.
3. Single reviewers are noisy (around 0.3 reliability in the NeurIPS estimate), so a spread of two points is normal. The mean of three is a weak measurement near the cutoff. Read the reasons, fix the major concerns, and consider resubmitting.
4. For example: "Results, paragraph 3, report only p-values for the retention comparison. Please report the difference in 30-day retention with a 95% confidence interval and an effect size, and say whether the comparison was planned."
5. Tell the editor about the role before reading further. It may be a conflict (you have a stake in how moderation looks), or useful expertise, and the editor decides. If you review, declare the role in your confidential comments.

</details>

## Lab / assignment hook

[Lab 12, the review lottery and a real review](../labs/lab12.md). You simulate two committees reviewing 1,000 papers, check the simulation against the formula, and find the reviewer count and acceptance rate that give a chosen precision. Then you write a full review of an invented game-research manuscript, and a response letter to a classmate's review of your proposal draft.

## Sources

- Cortes, C. & Lawrence, N. D. (2021). "Inconsistency in Conference Peer Review: Revisiting the 2014 NeurIPS Experiment." arXiv:2109.09774. 1,678 submissions; about 10% (170) double-reviewed, 166 completed; confusion matrix 22/21/22/101; inconsistency 43/166; accept precision about 50%; correlation 0.55 between committees' mean calibrated scores; at least three reviewers per paper; 50% of score variation subjective; scores related to citations for rejected but not accepted papers. https://arxiv.org/abs/2109.09774
- Beygelzimer, A., Dauphin, Y. N., Liang, P. & Wortman Vaughan, J. (2023). "Has the Machine Learning Review Process Become More Arbitrary as the Field Has Grown? The NeurIPS 2021 Consistency Experiment." arXiv:2306.03262. Disagreement on 23% of papers; about half of accepted papers would change; more selectivity increases arbitrariness. https://arxiv.org/abs/2306.03262
- Tomkins, A., Zhang, M. & Heavlin, W. D. (2017). "Reviewer bias in single- versus double-blind peer review." *PNAS* 114(48), 12708-12713. https://doi.org/10.1073/pnas.1707323114. WSDM 2017, 15.6% acceptance; 22% fewer bids; odds multipliers 1.63, 1.58 and 2.10.
- Committee on Publication Ethics (2013, revised 2017). *Ethical Guidelines for Peer Reviewers*. https://doi.org/10.24318/cope.2019.1.9
- Ludum Dare, "Ludum Dare Rules" (ldjam.com, last modified April 2021, accessed September 2026). Participants who submit a game may judge; 1 to 5 stars per category; Coolness rewards rating others and raises a game's visibility.
- The in-class paper, the reviewer counts in the Spearman-Brown table beyond 3, and the example concerns are invented or derived for teaching.

## Interactive spec: examples/w12-review-lottery.html

**The one insight.** A noisy score cut at a threshold makes acceptance partly a lottery, and the lottery gets worse as the venue gets more selective. With the reliability measured at NeurIPS 2014 (`ρ = 0.55`), about half of accepted papers would be rejected by a second committee, and no one has to be doing a bad job for that to happen.

**Layout.** Controls on top at 390px, on the left at 1280px. Two panels, side by side at 1280px and stacked at 390px: "One committee" and "Two committees". A readout table underneath.

**Controls (keyboard operable, with visible values).**
- Single-reviewer reliability `ρ₁`: 0.05 to 0.95, step 0.01, default 0.29.
- Reviewers per committee `k`: 1 to 30, default 3.
- Acceptance rate `a`: 0.05 to 0.60, step 0.01, default 0.26.
- Number of papers: 166 or 500 or 2,000 (default 500).
- "New sample" button: redraws with a seeded PRNG (seed shown).

**Computation.** Committee reliability `ρ = kρ₁ / (1 + (k − 1)ρ₁)`. For each paper draw `Q ~ N(0,1)` and for each committee `S = √ρ × Q + √(1 − ρ) × E` with `E ~ N(0,1)` independent, so `corr(S₁, S₂) = ρ`. Each committee accepts its top `round(a × n)` papers. Also compute the formula values: `P(both) = ∫_z^∞ φ(x) [1 − Φ((z − ρx)/√(1 − ρ²))] dx` with `z = Φ⁻¹(1 − a)` (Simpson's rule, 2,000 steps), precision `P(both)/a`, inconsistency `2(a − P(both))`.

**Left panel, "One committee".** Scatter of `Q` (horizontal) against `S₁` (vertical) for all papers, with a horizontal cutoff line. Accepted papers filled, rejected hollow. Also mark the top `a` share by true quality with a vertical dashed line, so the four regions (deserved accept, lucky accept, unlucky reject, deserved reject) are visible. Label the counts in each region.

**Right panel, "Two committees".** Scatter of `S₁` against `S₂` with both cutoffs, dividing the plane into four boxes. Label each box with its count, laid out like the NeurIPS table.

**Readout.** `ρ`, simulated and formula precision, simulated and formula inconsistency, and a small line chart of formula precision against `a` from 0.05 to 0.60 at the current `ρ`, with a dot at the current `a`.

**Test values (formula; the builder must check these).**
- `ρ₁ = 0.29, k = 3`: `ρ = 0.551`. At `a = 0.26`: precision 0.517, inconsistency 0.251 (to 3 decimals, using `ρ = 0.55` exactly: 0.517 and 0.251).
- `ρ = 0.55`, `a = 0.10`: precision 0.356, inconsistency 0.129.
- `ρ₁ = 0.29, k = 22`: `ρ = 0.900`; at `a = 0.26` precision 0.776.
- `ρ₁ = 0.05, k = 1`: at `a = 0.26` precision close to 0.26 (pure-noise limit is exactly `a`).
- With 2,000 papers, simulated precision should fall within 0.05 of the formula for these settings.

**Accessibility and style.** Use `templates/interactive-tokens.css`. Accepted and rejected differ by fill and shape, not only color. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Numbers selectable for copying. No logos or art.
