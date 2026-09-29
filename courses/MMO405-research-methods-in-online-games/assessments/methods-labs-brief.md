# MMO405 · Methods labs brief

**Weight:** 30% of the course grade.
**Due:** each lab is due at the start of the following week's lab session, unless the lab sheet says otherwise. Lab 14's talk is given in the week 14 session.
**Work mode:** as stated on each lab sheet. Labs 05, 06, 07, 08 and 09 have pair parts; the rest are individual.
**Related briefs:** [proposal-brief.md](proposal-brief.md) and [paper-brief.md](paper-brief.md). Most labs produce a section of one of them.

## What the labs are for

Each lab does two jobs. It makes you run one week's model on data where you can check the answer, usually invented data whose generator you open at the end. And it produces one piece of your own study: a question card, a consent section, a codebook, a recording plan, an ethics application, a figure. By week 14 you have written most of the proposal and much of the paper's method section in small, graded steps.

## The fourteen labs

| Lab | Week topic | What you compute | What it feeds | Weight |
|---|---|---|---|---|
| [01](../labs/lab01.md) | Research questions | Observed and stratified gaps, the selection term | Proposal section 1 (question card) | 7 |
| [02](../labs/lab02.md) | Quantitative methods | `d`, intervals, four verdicts, Fisher's `z`, pooling across servers | Proposal section 5 (SESOI) | 7 |
| [03](../labs/lab03.md) | Telemetry | Sessionization rules, cleaning, attenuation and its correction | Proposal sections 4 and 7 (data and consent) | 7 |
| [04](../labs/lab04.md) | Surveys and scales | Alpha, item statistics, a hidden two-part structure | Proposal section 4 (measures) | 7 |
| [05](../labs/lab05.md) | Experiments | Pooled change, DiD, placebo DiD | Proposal section 3 (threats to validity) | 7 |
| [06](../labs/lab06.md) | Interviews | Kappa, specific agreement, PABAK; codebook revision | Proposal sections 4 and 6 (guide, IRR decision) | 7 |
| [07](../labs/lab07.md) | Ethnography | Continuous, scan and one-zero recording; a field hour | Proposal section 4 (recording plan) | 7 |
| [08](../labs/lab08.md) | Mixed methods | Survey-log linkage, bias decomposition, connecting rule, joint display | Proposal sections 3 and 6 (design memo) | 7 |
| [09](../labs/lab09.md) | Guild networks | Degree, strength, betweenness, eigenvector, threshold sensitivity | Paper analysis section | 7 |
| [10](../labs/lab10.md) | Ethics | Randomized response estimator, privacy level, sample-size planner | Proposal section 7 (ethics application) | 7 |
| [11](../labs/lab11.md) | Writing | GRIM and p-value checks on a manuscript | Paper results and abstract | 7 |
| [12](../labs/lab12.md) | Peer review | Two-committee simulation; a full review; a response letter | Proposal appendix D | 7 |
| [13](../labs/lab13.md) | Replication | Filter model, five criteria, replication sample size | Paper limitations or future work | 7 |
| [14](../labs/lab14.md) | Presentations | Error-bar audit, redrawn figure, the 12-minute talk | Paper main figure | 9 |
| | | | **Total** | **100** |

Lab 14 carries more weight because it includes your research presentation.

## How a lab is marked

Each lab sheet has its own rubric. Labs 04 to 09 are marked out of 20 and the others out of 100. Your mark on each lab is converted to a percentage and multiplied by the weight in the table. For example, 16 of 20 on lab 05 is 80%, which earns `0.80 × 7 = 5.6` of the lab component's 100 points. The lab component's total is then scaled to its 30% of the course grade.

Three rules apply to every lab, whatever its rubric says.

1. **Code must run as submitted.** Starter tests or checkers must pass with `.venv/bin/python` from inside the starter folder. Code that does not run scores 0 on the lab's code criterion.
2. **Numbers must come from your code.** Every number in a results sheet must be reproducible by running your submitted files. Hand-edited output scores 0 on the criterion it appears in.
3. **Predictions come before results.** Where a lab asks you to write something down first (a SESOI in lab 02, a construct in lab 03, a kappa threshold in lab 06, a prediction in lab 08), submit it as written at the time. Changing it afterwards scores 0 on that criterion.

## Ethics and consent rules for the labs

The labs follow the same standard as the proposal ([week 10](../lectures/w10-ethics-and-irb.md)). Almost all lab data are invented. Three labs touch real people, and each has a fixed rule.

- **Lab 06, the role-play pilot.** Your partner plays an invented persona. No real experiences, real names or real character names, so no personal data is collected. Any recording is deleted after you have written your pilot notes.
- **Lab 07, the field hour.** Public spaces only, in an open role with a profile note where the game allows it, and with the instructor's sign-off on your recording plan before you log in. Do not start conversations for research, join private channels, record names, or quote chat verbatim. Blur every name and chat line in any screenshot. A submission that breaks these rules scores 0 on the field components, as the lab sheet states.
- **Lab 14, the talk.** Your slides are publication. Every screenshot, quote, character, guild or server name and network figure must be cleared against your approved protocol ([week 14](../lectures/w14-research-presentations.md), section 4). The people check in step 8 is marked.

The ethics application you write in lab 10 is a draft for the proposal. Writing it does not approve your study. Only the milestone 2 sign-off or your board's approval does ([proposal brief](proposal-brief.md), "No data from real players before sign-off").

## Pair work

In a pair lab, both partners receive the pair's mark for the shared parts. The individual parts (the lab 06 guide, the lab 07 field notes and reflexive paragraph) are marked separately. If a partnership fails, tell the instructor before the deadline; the instructor may mark the shared parts individually. Name your partner on every submission.

## Late work, resubmission and missed labs

- Up to 72 hours late: 10% of the lab's marks per 24 hours. After 72 hours: 0, but feedback is still given if you submit before the next milestone that depends on the lab.
- **One resubmission.** Once in the term, you may resubmit one of labs 01 to 13 within a week of receiving its feedback. The resubmission is capped at 80% of that lab's marks, and the higher mark counts.
- **Missed talk.** If you miss the week 14 talk with a documented reason, you give it in a make-up slot. Without one, the talk criterion of lab 14 scores 0.

## Rubric: how the 100 points are made

| Component | Points |
|---|---|
| Labs 01 to 13, each converted to a percentage and weighted at 7 | 91 |
| Lab 14, including the research presentation, weighted at 9 | 9 |
| **Total** | **100** |

## Academic integrity

Discuss the models and the starter code with anyone. The code, numbers and writing you submit must be your own, or your pair's for shared parts. Say which parts you reused from your own earlier labs. If you use a generative AI tool, say how, and make sure you can explain every line of code: the paper's oral check may ask you to rerun a lab function by hand ([paper brief](paper-brief.md), "Oral check").
