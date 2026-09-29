# PR101 · Post-mortem brief: from data to changes, twice

**Weight:** 20% of the course grade.
**Part 1, jam post-mortem:** assigned week 9, due end of week 9 through [lab 09](../labs/lab09.md). **Part 2, final post-mortem:** assigned week 14 through [lab 14](../labs/lab14.md), due the last day of week 15, at least three days after your release.
**Work mode:** a team document, plus an individual reflection from each member that is marked individually.
**Lectures:** [week 9, jam post-mortem](../lectures/w09-jam-post-mortem.md) and [week 14, post-mortems as a practice](../lectures/w14-post-mortems-as-a-practice.md), with the models from [week 6](../lectures/w06-estimation-and-why-it-fails.md), [week 10](../lectures/w10-bug-tracking-and-qa-basics.md), [week 12](../lectures/w12-crunch-causes-costs-alternatives.md) and [week 13](../lectures/w13-builds-and-release-checklists.md).

## What this component is for

Week 14 made the point that one post-mortem is a diary entry. Two post-mortems, coded the same way, with the first one's changes checked in the second, are a practice. This component marks both halves. Part 1 is the jam post-mortem you write from your jam log in week 9. Part 2 is the final post-mortem, which analyses the final project and asks whether the changes you promised in week 9 actually happened and actually worked.

Three habits run through both parts, and the rubric rewards them. Data comes before the story. Every item is written blameless, about the process and not the person. Every lesson ends in an action item with an owner, a change and a check.

## Part 1: the jam post-mortem (20 points)

Written in lab 09 after the week 9 meeting, at most 1,500 words, with the sections lab 09 lists: what we made, the numbers (both views of your cone, median ratio with and without cut tasks, plan ratio, zero-remaining claims, planned against shipped cards, freeze record), what went right, what went wrong, and three changes. Every member signs off in the repository.

Part 1 is marked with lab 09's rubric. Its percentage is multiplied by 20. Keep it. Part 2 checks its three changes.

## Part 2: the final post-mortem (80 points)

### Length and form

A team document of 2,500 to 4,000 words, plus tables, as `POSTMORTEM.md` in your repository at a tag `postmortem`. Numbers carry their source: a file and row, a commit, a tracker id or a script output. Put the scripts' printouts in an appendix, not in the body.

### Sections

1. **What we made.** One paragraph, the `v1.0.0` link, and a table of must, should and could cards planned at milestone 1 against shipped, with every cut and the date and trigger that caused it.
2. **The numbers.** One short subsection per model, each with the plan, the actual and one sentence on the gap.
   - *Estimation (weeks 6 and 9).* From `task_log.csv`: the median ratio, p10, p90 and plan ratio `R` from lab 06's module, with the same numbers for the jam beside them. The remaining-view spread in the first and last `x` bins from lab 09's `cone.py`. Cut tasks as lower bounds.
   - *Scope (week 4).* `P`, the cut line and `m_max` at milestone 1, and the overrun you actually experienced (your `R`). Would your `m_max` have covered it?
   - *Bugs (week 10).* Your lab 10 forecast of peak and zero days against what the tracker shows. Your measured regression rate `r` (reopened plus caused-by-fix, over fixes). Open P1, P2 and P3 at release.
   - *Hours (week 12).* Logged overtime against your lab 12 policy. If anyone worked long weeks, run the ledger on their real schedule and report the lead at release and three weeks later.
   - *Release (week 13).* `P(clean)` from your lab 13 plan against what escaped after upload. For each escape, the checklist line that should have caught it.
3. **Timeline.** One line per sprint and milestone: what was playable, what was cut, what surprised you. Link the sprint records.
4. **What went right and what went wrong.** Three to five of each. Every item points to evidence and is written blameless, in the week 14 form.
5. **Coded problems.** Both projects' went-wrong items coded into Politowski's 20 types by two members separately, with percent agreement before discussion. Both Pareto tables with `k_80`. Your top category opened into narrower root causes, and what that did to the chart. This is lab 14's note, revised.
6. **Closing the loop.** A table of the jam's three changes: was it done, what did its check show, and did the problem it targeted come back? The recurrence rate `R = |C1 ∩ C2| / |C1|` and the closure rate, with one paragraph that is honest about the sample size.
7. **Action items for the next project.** At most one per final-project category, each with an owner (a role, since teams change in PR201), a change and a check. Any problem that escaped into a release also becomes a line in `RELEASE_CHECKLIST.md`, and this section links it.

### Individual reflection (each member, 400 to 600 words)

Written alone and submitted privately through the course page, not in the repository. It covers:

- The role you held and one decision you owned. Name the decision log entry.
- One of your own estimates that went badly, with its log rows, and what you now think caused the miss (optimism, skew, missing work, interruption, dependency; week 6 section 3).
- One habit from this course you will carry into PR201, and the evidence from your own work that it helped.
- One thing you would change about how you worked with the team. Write it about your own behaviour and the process. Contribution concerns about others belong in the confidential [peer review](peer-review-brief.md), not here.

## Rubric

The post-mortem mark is the total below, out of 100, multiplied by 0.20. The individual reflection row is marked per student. Everything else is a team mark.

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Part 1: jam post-mortem | Lab 09 rubric percentage × 20 | | | | 20 |
| The numbers | 18 to 20: every model subsection has plan, actual and gap from real files; jam and final compared; cut tasks included as lower bounds; each gap explained with the model | 13 to 17: one model missing or one number without a source | 7 to 12: numbers reported without comparison or explanation | 0 to 6: little data, or numbers that don't match the files | 20 |
| Went right and went wrong | 13 to 15: three to five of each, every one with evidence; blameless throughout; each wrong item names the process that let it happen | 10 to 12: most have evidence; one item slips into blame | 5 to 9: opinions with little evidence | 0 to 4: missing, or items name people | 15 |
| Coding, Pareto and recurrence | 13 to 15: two coders with agreement reported; both tables and `k_80` correct; top bucket opened and the change explained; `R` and closure correct with a sample-size caveat | 10 to 12: numbers right, one step missing (single coder, or bucket not opened) | 5 to 9: tables with errors or no interpretation | 0 to 4: missing | 15 |
| Action items | 9 to 10: one per category, each with an owner, a change and a check someone else could apply; escaped problems added to the checklist | 6 to 8: most checkable | 3 to 5: vague ("communicate better") | 0 to 2: missing | 10 |
| Individual reflection | 14 to 15: all four points with evidence from your own log rows and decisions; honest about your own misses; blameless | 10 to 13: one point thin or without evidence | 5 to 9: general statements, little evidence | 0 to 4: missing, or used to blame teammates | 15 |
| Structure and writing | 5: sections in order; numbers sourced; plain, specific prose; within length | 3 to 4: one section out of place or over length | 1 to 2: hard to follow | 0: missing | 5 |
| **Total** | | | | | **100** |

## How the post-mortem is marked

- **Honesty scores, failure doesn't cost.** A plan that ran 60% over, reported with its log rows and a clear cause, can earn full marks in "the numbers". The rubric marks the quality of the account, not the quality of the project. The game is marked elsewhere.
- **Numbers are checked against the files.** The marker reruns lab 06's module, `cone.py` and `postmortem_tools.py` on your committed files. A number that doesn't match costs more than a number you left out and explained.
- **Blame costs marks.** A line that names a person as the cause of a problem loses marks in the "went right and went wrong" row, even if the facts are right. Rewrite it in the week 14 form.

## Rules

- **Late submission.** Up to 48 hours late, Part 2 is marked out of 60 instead of 80. Part 1 cannot be late, because Part 2 depends on it. A missing Part 1 can be submitted with Part 2 for half marks.
- **Invented data.** A post-mortem built on a log reconstructed after the fact must say so, row by row. Undisclosed invented data is misconduct.
- **Individual reflections are private.** Teammates do not see each other's reflections.

## Advice

- **Start from lab 14's note.** Its coded data, Pareto tables and action items are section 5 and part of section 7 already.
- **Check the week 9 changes in week 13, not week 15.** Each change had a check you could apply in week 13. If you ran the check then, section 6 writes itself.
- **One project proves little.** Two post-mortems of five items each can't tell a pattern from bad luck. Say so, and use the numbers to start a conversation about the next project, not to settle one.
