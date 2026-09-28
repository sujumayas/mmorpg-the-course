# UX201 · Usability test brief

**Weight:** 30% of the course grade.
**Group size:** three or four students. One report per group, plus a short individual contribution statement from each member.
**Assigned:** week 8. **Report due:** start of week 13.
**Labs that feed it:** [lab 08](../labs/lab08.md) is the practice run and uses the same method, scripts and log formats. [Lab 07](../labs/lab07.md) gives you the moments of need that become your zero-tolerance list. [Lab 02](../labs/lab02.md) gives you the keystroke-level model you use to predict task times. [Lab 03](../labs/lab03.md) gives you the moderation habits (verbatim script, observation kept apart from interpretation, logged assists).
**Related briefs:** [heuristic-eval-brief.md](heuristic-eval-brief.md) and [final-study-brief.md](final-study-brief.md). The final study requires a usability test, and this assignment is where you learn to run one well.

## What this component is for

The course outcome behind this component is "run usability tests and heuristic evaluations", together with "design onboarding and interfaces with cognitive load in mind". A usability test answers one question. Can players do what the game needs them to do, without help? This assignment asks you to answer it for a real sequence, change the build while you test, and report honestly what you fixed, how sure you are that each fix worked, and what is still open.

Lab 08 was a rehearsal on a small scale. Here the bar is higher in three ways. You predict before you test, with the week 2 and week 7 models. You recruit testers who are not your classmates. And you triage what remains with the week 14 tier model, so the report ends in decisions.

## What to test

A sequence of 10 to 20 minutes that a new player meets early and that your group can change between testers in under 30 minutes. Choose one.

- An onboarding sequence or first level of your own prototype, digital or paper (a team member plays the "computer" for a paper prototype).
- A tutorial or level built in a shipped game's level editor or modding tools.
- A clickable or paper mock-up of a menu flow from a game genre you know (inventory, crafting, group finder, shop, character creation).

You may reuse the lab 08 sequence only if you start from the build that ended lab 08, list its open problems as known issues before the first session, and test with new testers. Otherwise pick a new sequence, or the next part of the lab 08 one. Get the choice approved in the week 9 lab session.

## Before the first tester

Submit these together as the **test pack** (milestone 1). The course team returns comments within three days. The pack is not graded on its own, but the plan counts toward the report.

1. **One-page test plan** with the eight headings from week 8, section 3: question, players, tasks (each with a success criterion and time limit), zero-tolerance items, measures, script, change policy, report.
2. **Moments of need.** For the sequence's core mechanics or screens, list when each is taught and when the player first needs it without a prompt, as in lab 07. Every moment of need is a zero-tolerance item. If the sequence teaches four or more things, compute recall at each moment of need with the week 7 model (`s₀ = 20`, `g = 2.5`) and flag any below 0.8.
3. **Predicted times.** For two tasks, write the novice operator sequence with the week 2 keystroke-level model (including `M`, `S(N)` and `W` where they occur) and predict the time.
4. **Session materials.** The script from lab 08 (you may adapt the words for your sequence), task cards, the consent sheet, and the SUS items with "system" replaced by the name of the part you test.
5. **Change policy.** Who decides on a change during the test, how fast a build can change, and the four RITE categories you will sort issues into (obvious and quick, obvious and slow, unclear cause, might be the test).

## Running the test

- **Testers.** Six to eight people who match your player definition and have never seen the sequence. At least half must come from outside this course. No one who took part in your lab 08 test.
- **Roles.** Moderator, observer and builder, as in lab 08. Rotate roles so every member moderates at least one session.
- **Think-aloud.** Live, with permission to go quiet in fast moments and a prompt afterwards. If your sequence is mostly fast action, use retrospective think-aloud for those parts and say so.
- **RITE.** After each tester, spend five minutes sorting issues into the four categories. Fix category 1 issues before the next tester. Log every change in `changes.csv`, including re-fixes.
- **Rescue rule.** If a tester is stuck at a failure for three minutes, rescue them, log `ASSIST`, and let them continue so later sections still get tested. Report the blocker as found, and don't count problems behind it as absent.
- **Time on task.** Time the two tasks you predicted in step 3, with the same start and end states for every tester.
- **SUS** after each session.
- **Ethics.** Adult testers only. Consent before recording. Tester codes, never names, in every file. Delete raw video at the end of the semester unless a tester agreed otherwise in writing.

## The report

At most five pages, plus appendices. Use these sections in this order.

1. **Summary (half a page).** What you tested and with whom, the number of builds, the three most important open problems with their tiers, and what worked.
2. **Plan and predictions.** The one-page plan (it counts toward the five pages), the moments-of-need table and the predicted task times.
3. **What happened.** The errors-per-tester chart from `rite_report.py` with every build change marked, and a paragraph explaining its shape. For any rise after a change, say whether it came from reach (testers got further) or from a fix that broke something, with evidence from the observation log.
4. **Problem table.** One row per problem: id, description from the player's side, cause or heuristic, first seen, times seen, status (fixed after tester k, re-fixed, open), and verification confidence `1 − (1 − p)^m` at `p = 0.1` and `p = 0.3` for every fix. Name the fixes you don't yet trust.
5. **Model against measurement.** Predicted against measured time for the two tasks, novice testers only, with the percentage error. Explain the largest gap with a specific cause (an error, an `M` you missed, a longer scan). For each moment of need, say how many testers met it without help.
6. **Ratios and SUS.** Impact ratio and re-fix ratio, each with one sentence on what it says about your test. SUS per tester and the mean, with one sentence on why you shouldn't compare it with another group's number.
7. **Open problems, triaged.** Apply the week 14 model (weights `1, 3, 10, 30`, bar `T = 1`, unless you justify a change before looking at the data) to every problem still open at the end. Use as `n` the number of testers who ran builds where the problem was present. Write the three most important in the five-part form (observation, evidence, interpretation, impact, recommendation). Give every "investigate" item a named next step.

**Appendices:** `observations.csv`, `changes.csv`, the script output, timing sheets, SUS sheets, consent tick-list (codes only) and handwritten notes.

**Individual contribution statement:** half a page per member, submitted separately. Say which sessions you moderated, observed and built for, and which parts of the report you wrote.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Week 8 lab session | Groups formed; lab 08 run as practice | Lab 08 is graded as a lab |
| Week 9 lab session | Sequence approved | No |
| End of week 9 | Test pack submitted (plan, moments of need, predictions, materials, change policy) | No, but comments are returned within three days and the plan is graded in the report |
| Week 10 lab session | Pilot session with one classmate. Fix the setup, not the game | No |
| Weeks 10 and 11 | Sessions with six to eight testers | No |
| Start of week 13 | Report, appendices and contribution statements | Yes |

## Rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Plan and predictions | 15 | 13-15: precise question and player definition, tasks with observable success criteria, zero-tolerance list built from moments of need, KLM predictions with justified `M` placement | 10-12: all parts present, one vague | 6-9: tasks or success criteria loose, predictions thin | 0-5: no plan, or plan written after testing |
| Session method and ethics | 15 | 13-15: script used, think-aloud kept up, assists logged, rescue rule followed, half the testers from outside the course, consent and codes handled | 10-12: minor slips, documented | 6-9: coaching in places, or recruitment mostly classmates | 0-5: moderator explained the design, or identifiable data |
| RITE decisions | 15 | 13-15: changes made between testers, each categorised and logged, re-fixes recorded, unclear issues left for more data | 10-12: changes made and logged, categories thin | 6-9: few changes, or changes without categories | 0-5: no changes during the test, or changes not logged |
| Analysis | 25 | 22-25: error curve explained with reach and evidence; verification confidence computed and read correctly; both ratios reported; SUS used as a thermometer | 17-21: numbers right, one explanation thin | 11-16: numbers mostly right, error counts partly read as quality | 0-10: error counts treated as a quality score, or no verification |
| Model against measurement | 10 | 9-10: predicted and measured times compared with percentage error, largest gap explained with a named cause, moments of need checked against testers | 7-8: comparison made, cause generic | 4-6: prediction or measurement missing for one task | 0-3: no comparison |
| Open problems and recommendations | 15 | 13-15: tiers computed with `n` stated, policy fixed before analysis, top three written in five parts, every investigate item has a next step | 10-12: tiers right, writing blurs observation and interpretation | 6-9: problems ranked by frequency or gut | 0-5: no triage, or recommendations missing |
| Writing | 5 | 5: numbers first, plain, within length | 4: minor padding | 2-3: hard to follow in places | 0-1: over length or unreadable |

**Individual adjustment.** Each member receives the group mark. If the contribution statements and the course team's observation of the lab sessions show a clearly unequal share of the work, the course team may move an individual mark by up to 10 points after talking with the group.

## Late work

Up to 48 hours late loses 10 points. After that the report scores 0 unless an extension was agreed before the deadline. Extensions are given for documented illness or emergency, and for a tester no-show that leaves you below six testers, if you tell the course team within a day of the no-show.

## Academic integrity

Discuss methods freely with other groups. The plan, data, analysis and words you submit are your group's own. The scripts from lab 08 are course materials, and you should use them. Say in the appendix if you changed them.
