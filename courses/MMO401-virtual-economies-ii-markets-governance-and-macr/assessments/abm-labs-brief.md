# MMO401 · ABM labs brief

**Weight:** 40% of the course grade.
**Covers:** the fourteen weekly labs, [lab 01](../labs/lab01.md) to [lab 14](../labs/lab14.md).
**Related:** [final-model-and-memo-brief.md](final-model-and-memo-brief.md) (60%). Labs 03, 07, 13 and 14 feed the final project directly. The [exam bank](exam-bank.md) supplies the questions for code reviews.

## What this component is for

The course promises three things. You can run agent-based simulations of an MMO economy. You can design interventions and predict their effects. You can evaluate player-run institutions. The labs are where you practise each of those one model at a time, on numbers you can check, before the final project asks you to combine them.

Most labs are agent-based models in Python. Four are not. Lab 01 and lab 13 are measurement labs on report data, lab 08 may be a spreadsheet, and lab 12 is a ledger investigation. They count here because the in-house economist's job is measurement as much as simulation, and a model you cannot check against a ledger is not evidence.

## Which labs count

| Lab | Topic | Assigned | Due | Builds on | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | Reading a real economic report | Week 1 | Start of week 2 | — | Yes |
| [02](../labs/lab02.md) | Your first agent-based economy | Week 2 | Start of week 3 | — | Yes |
| [03](../labs/lab03.md) | A policy experiment | Week 3 | Start of week 4 | Lab 02 | **No** |
| [04](../labs/lab04.md) | The policy desk | Week 4 | Start of week 5 | — | Yes |
| [05](../labs/lab05.md) | Build a matching engine | Week 5 | Start of week 6 | — | Yes |
| [06](../labs/lab06.md) | Corner and cartel simulation | Week 6 | Start of week 7 | Lab 05 | Yes |
| [07](../labs/lab07.md) | Tuning a transaction tax | Week 7 | Start of week 8 | — | Yes |
| [08](../labs/lab08.md) | The honesty ceiling | Week 8 | Start of week 9 | — | Yes |
| [09](../labs/lab09.md) | Haulers between two regions | Week 9 | Start of week 10 | — | Yes |
| [10](../labs/lab10.md) | Loss rules in an agent-based economy | Week 10 | Start of week 11 | — | Yes |
| [11](../labs/lab11.md) | A token market | Week 11 | Start of week 12 | — | Yes |
| [12](../labs/lab12.md) | Incident response from a server ledger | Week 12 | Start of week 13 | — | Yes |
| [13](../labs/lab13.md) | Reading a year of reports | Week 13 | Start of week 14 | — | Yes |
| [14](../labs/lab14.md) | Sizing an intervention | Week 14 | Start of week 15 | Lab 13 | **No** |

"Start of week N" means before the first class session of that week.

Lab 03 cannot be dropped because its calibrated, replicated model is the starting point of the final project. Lab 14 cannot be dropped because its one-page spec is the first draft of your policy memo.

## How the grade is computed

1. Each lab is marked out of 100 with the rubric printed in that lab. The labs use three rubric formats, converted as follows.
   - **Four bands with percentage weights** (labs 01, 02, 03, 10, 11 and 12). Each criterion scores `weight × band points / 4`. Take the band points as Excellent 4, Adequate 3 or 2, Missing or wrong 1 or 0, as the marker judges within the band. For example, an Adequate 3 on a 25% criterion scores `25 × 3/4 = 18.75`.
   - **Points with full, half or zero marks** (labs 04 to 09). The points already sum to 100.
   - **Twenty points** (labs 13 and 14, five criteria at 4 points each). Multiply the total by 5.
2. Your two lowest lab scores are dropped, except labs 03 and 14, which always count.
3. The twelve remaining labs are averaged with equal weight. That average is worth 40% of the course grade, so each counted lab is worth about 3.3%.

A missing lab scores 0 and can be dropped like any other score.

## What to submit each week

- The code, spreadsheet or notebook the lab names, runnable as submitted. Python labs must run with `python3` and the standard library unless the lab says otherwise. Put every parameter and every seed in one place near the top of the file.
- The report or memo the lab asks for, as a PDF or Markdown file. Page and word limits are targets. Within 20% either way is fine. Going far over usually means the report restates the lab instead of making a decision.
- The CSVs and charts the lab lists.

Labs 04 to 09 are pair labs, as their headers say. Each pair submits one set of files with both names on it, and both partners get the same mark. Work alone on every other lab. Discuss methods with classmates as much as you like, but the lines and the words are yours (or your pair's). If you reuse code from a published reference solution (see late work below), say which file and which functions.

## Habits every lab is marked on

These are the habits the lectures teach. Markers look for them in every lab, whatever that lab's rubric calls the criterion.

- **Reproduce before you experiment.** Each lab prints reference values. Match them first. If you cannot, say so, say which number you trust and why, and carry on. An honest mismatch loses fewer points than a silent one.
- **Verify with an identity.** Every simulation that moves money keeps a ledger and asserts `M_end = M_start + faucets − sinks` at every tick (weeks 3, 10, 12 and 13). A model that fails its own ledger check is not evidence.
- **Seed everything.** Use a private generator per run (`random.Random(seed)`), record the seed list, and use common random numbers when you compare policies (week 3).
- **Report uncertainty.** A single run is one story. Results that compare policies need replications and a 95% interval, or a stated reason why one run is enough (for example, a deterministic model).
- **Memos decide.** Every lab memo recommends something, backs each claim with a number from your own runs, names who pays, and states what result would reverse the recommendation.

## Code reviews

Three times during the semester, in a lab session, a marker opens one of your submitted labs with you for five minutes. They change one parameter or one seed and ask you to predict, before the code runs, which way two outputs will move. They may also ask one question in the style of the [exam bank](exam-bank.md), rewritten with a number from your own results.

A code review is not graded on its own. If you cannot explain how a number in your own submission was produced, that lab is capped at 60 until you can. You may book a second attempt within a week.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Start of week 4 | Lab 03 submitted, with its calibrated model and seed list | Yes |
| Weeks 5, 9 and 12 | Code reviews in lab sessions | No, but can cap a lab at 60 |
| Start of week 8 | Lab 07 submitted. Its market module is the default market for the final model | Yes |
| Start of week 14 | Lab 13 submitted. Its decomposition code is the diagnostic step of the final memo | Yes |
| Start of week 15 | Lab 14 submitted. Its spec is the first draft of the final memo | Yes |

## Late work and extensions

- You have two free 48-hour extensions for the semester. Tell the course team before the deadline. No reason is needed.
- Beyond that, late work loses 10 points per 24 hours, up to 72 hours.
- After 72 hours the course team releases a reference solution for the labs that others build on: lab 02 (for lab 03), lab 05 (for lab 06) and lab 13 (for lab 14). Late submissions for those three labs are not accepted after the release. Starting the next lab from a reference solution costs nothing on that next lab, as long as you say so.
- Lab 14 cannot use a free extension, because the final project deadline is fixed.

## Rubric

Each lab's own rubric sets its criteria and weights, and it wins where the two differ. This common rubric is the band guide markers use to keep grades consistent across fourteen labs with three rubric formats. Every lab rubric row maps onto one of these criteria.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Reproduction and verification | 25 | 23-25: every reference value matched or the mismatch found and explained; ledger or unit test asserted every tick | 18-22: values matched, one test trivial or run only at the end | 13-17: some values off without explanation, tests thin | 0-12: reference values not attempted, or code does not run |
| Experiment design | 25 | 23-25: every experiment the lab asks for, seeded, common random numbers where policies are compared, replications sized to the question | 18-22: all experiments run, replication count thin for one comparison | 13-17: an experiment missing, or single runs used to compare policies | 0-12: experiments skipped |
| Analysis | 20 | 18-20: each result explained by a named mechanism from the lecture, gaps between the closed form and the simulation found and tested | 14-17: results explained, one gap asserted but not tested | 10-13: results reported with little explanation | 0-9: numbers without interpretation |
| Charts and tables | 10 | 9-10: every required chart and table, labelled, with the reference or target line drawn | 7-8: present, one missing a label or reference line | 5-6: some missing | 0-4: none |
| Memo or recommendation | 20 | 18-20: a clear decision, every claim backed by the student's own numbers, who pays named, a reversal condition stated | 14-17: decision with some unsupported claims | 10-13: decision with few numbers | 0-9: restates the lab, no decision |

Total: 100 points per lab.
