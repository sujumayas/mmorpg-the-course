# PR402 · Post-mortem brief: the launch post-mortem, reflection and viva

**Weight:** 20% of the course grade, the whole post-mortem component. It has a team part (PMT, 10%) and an individual part (PMI, 10%).
**Assigned:** week 13. **Due:** the post-mortem document and lab 14 workbook at the week 15 showcase, in `production/postmortem/`; the individual reflection 48 hours after the showcase; the viva in week 15 or the exam period.
**Work mode:** the document is team work, marked once and adjusted per person by the [peer assessment](peer-assessment-brief.md). The reflection and viva are individual and are not adjusted.
**Session guide:** [week 14, post-mortem](../lectures/w14-post-mortem.md). **Lab:** [14](../labs/lab14.md). **Question bank:** [exam-bank.md](exam-bank.md).

## What this assessment proves

That the team can use its own records to test what it believes it learned, and write lessons the next team can act on. You have more evidence than in any earlier project: sprint records, a patch sized from your own ratio, a live ledger, incident logs, a cohort table. A good post-mortem uses that evidence against the team's own beliefs. A weak one lists what hurt ([week 14, section 1](../lectures/w14-post-mortem.md)).

The individual part checks that each student understands the whole launched game and the concepts it ran on, not only the part they built.

## Part A. The team post-mortem document (50 points, PMT)

**Length.** 4,000 to 6,000 words, excluding tables, code and appendices. Anything longer is read to 6,000 words.

**Structure.** The seven parts of [MMO407 week 12, section 3](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md), applied to the whole project from the PR401 production plan to the end of week 13, with the launch as its own section:

1. Scope and sources: dates covered, systems in scope, where the evidence comes from.
2. Plan against actual: the date table and the scope table from lab 14 part B, and every launch forecast from lab 08 and lab 09 beside what happened.
3. Timeline with incidents: from logs, in UTC, including decisions (shard opened, kill switch flipped, patch cut).
4. What went right, what went wrong: as events with numbers.
5. Contributing factors: each with a counterfactual test, using a course model where one exists.
6. Lessons, graded A, B or C by their evidence, including the planning claim from lab 14 part A with its sample-size caveat, and the recurrence and closure rates against your PR401 pre-production review.
7. Action items: one owner, one change and one check each, written for the team you will be on next.

**Standard.** Blameless as in [PR101 week 14, section 3](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md). Every claim cites a record from lab 14 or the production folders by part and row.

## Part B. Individual reflection and viva (50 points, PMI)

**Reflection.** 800 to 1,200 words, written alone. Choose one decision you made or argued for during PR402 (a cut, a triage call, a shard plan, a balance change, an economy lever). State what you knew when you made it, citing the dated record. Then say what the evidence now says about it, and what you would do differently as a change someone could check. Hindsight is the trap here. Judge the decision by what was known at the time ([MMO407 week 12, section 4](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md)).

**Viva.** 15 minutes with two examiners. They pick five or six questions from the [exam bank](exam-bank.md), rewritten with your team's own numbers. At least two are about a part of the game you did not build. The repository, the dashboard and the live game are open, and you may look things up. Each question is marked 0 to 5 on the bank's scale.

**Peer rating conduct.** Whether you submitted each peer round on time with evidence for every extreme rating, as set in the [peer assessment brief](peer-assessment-brief.md).

## Evidence required

| Evidence | Format | How it is checked |
|---|---|---|
| Sprint records | `sprints.csv`, `sprints.py`, output | The instructor runs the script; output must match lab 14 part A |
| Plan against actual | PR401 production plan and pre-production review; lab 14 part B | Two rows are traced back to the PR401 documents |
| Builds | Tags for alpha, both betas, launch and the patch | Dates in the timeline must match the tags |
| Telemetry | Queries behind every number the document cites | One number per section is rerun |
| Incident logs | Logs and postmortems since week 5 | One timeline entry is matched to its log |
| Playtest and beta data | Lab 05, 06 and 08 outputs | One forecast-against-actual row is recomputed |
| Patch follow-up | Week 12 expected-number list with actuals | The patch forecast error is recomputed |
| Reflection record | The dated record the student cites | The examiner opens it and checks the date |

## How it is marked

Two staff members mark the document independently and agree a mark. One random line is checked against the records for the blameless standard. The reflection is marked by one examiner and moderated on a sample. The viva is marked by both examiners on the day.

`PMT = 2 × Part A points` and `PMI = 2 × Part B points`, each out of 100.

## Rubric

| Part | Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|---|
| A | Evidence base | 10 | Lab 14 complete; the script runs; every sprint and the patch present; feature and live ratios separated | Workbook missing or numbers that do not recompute |
| A | Plan against actual | 10 | Date and scope tables start from the PR401 plan; every unplanned item listed and classified; launch forecasts with errors | Tables built from memory |
| A | Timeline and contributing factors | 8 | Timeline from logs with decisions; counterfactuals tested with a number where a model exists | "Had we been more careful" |
| A | Lessons graded and tested | 12 | Each lesson a claim that could be wrong, graded A to C, citing a record; the planning claim uses both `r` and `q`; recurrence and closure against PR401 with every recurring category explained | Lessons with no evidence; "we got better at planning" |
| A | Action items and blameless writing | 10 | One owner, change and check each; no line blames a person; the random line check passes | Action items without checks; blame |
| B | Reflection | 20 | One specific decision; what was known then, with a dated record; what the evidence says now; a checkable change | A diary; hindsight presented as foresight |
| B | Viva | 25 | Scaled from the bank: `total / (5 × questions asked) × 25` | |
| B | Peer rating conduct | 5 | All three rounds on time; every rating of 0, 1 or 4 has an evidence comment that holds up | A round missing, or ratings excluded after review |
| **Total** | | **100** | | |

## Late and missing work

The document is due at the showcase. Up to 48 hours late, Part A rows are capped at 70%. The viva cannot be moved without an agreed extension. A student who misses it without one scores 0 for that row.

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) and [week 14, pre-production review](../../PR401-capstone-i-pre-production/lectures/w14-pre-production-review.md) (the plan and lessons this post-mortem is tested against).
- [PR101 week 9, jam post-mortem](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w09-jam-post-mortem.md), [week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) and [week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md).
- [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (logs for the timeline).
- [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (incident postmortems that feed the timeline).
- [MMO407 week 12, writing a post-mortem](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md).
