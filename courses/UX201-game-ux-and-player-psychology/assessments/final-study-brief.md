# UX201 · Final study brief: UX study of a shipped game

**Weight:** 50% of the course grade.
**Group size:** three students (two or four with the course team's approval). Group report and presentation, individual viva and individual method log.
**Assigned:** week 11. **Presentation and viva:** week 15. **Report due:** seven days after the week 15 session.
**Labs that feed it:** [lab 14](../labs/lab14.md) is the dry run for the report, with the same structure, triage script and tracker. [Lab 08](../labs/lab08.md) and the [usability test](usability-test-brief.md) give you the core method, which every study must include. Your second and third methods come from the method labs listed in the table below, most often [lab 12](../labs/lab12.md) (surveys and interviews), [lab 13](../labs/lab13.md) (arousal and gaze) and [lab 09](../labs/lab09.md) with the [heuristic evaluation](heuristic-eval-brief.md).
**Exam bank:** the viva draws on [exam-bank.md](exam-bank.md), rewritten with your study's numbers.

## What this component is for

This is where the course comes together. All three course outcomes meet in one piece of work: apply Self-Determination Theory and flow to design decisions, run usability tests and heuristic evaluations, and design onboarding and interfaces with cognitive load in mind. You pick one question about a shipped game, answer it with at least three methods from the course, and report the result so a team could act on it the same day.

A shipped game makes the task honest. You can't change the build, so you can't hide behind "we'll fix it next round". You have to find the problems, show the evidence, say how sure you are, and recommend directions the developers could take.

## Choosing the game and the question

- **The game.** Any shipped game you can play and test legally, on hardware you can bring to sessions. Record the version or season, the platform and the dates. If the game sells random items for money, don't spend money for the study. Log what you can observe for free and read the published odds where they exist, as in lab 05.
- **The question.** One research question about a part of the game's player experience, narrow enough to answer with 5 to 8 testers. Good questions name a player and a moment. "Can a new player complete the first hour of this action RPG without help, and which mechanics are they missing at the first boss?" is a study. "Is this game good?" is not.
- **The player.** Define the target player the way week 8 does, with recruitment criteria and exclusions. Most studies should use new players, because shipped games have many experienced ones already.

## Methods

Every study uses the **core method** and at least **two method modules**.

**Core method: a moderated usability test** with 5 to 8 testers who match your player definition, run with the week 8 method (plan, tasks with success criteria, zero-tolerance items, think-aloud, logged assists, rescue rule). There is no RITE, because you can't change the build. Run it as a single round, and use the rescue rule so testers still reach later parts.

**Method modules.** Choose at least two that serve your question. Each module must produce its own numbers and be analysed with the lecture's model.

| Module | What you produce | Lecture and lab |
|---|---|---|
| Search or task cost | Fitted or lecture search slopes applied to a real screen, or KLM operator sequences compared with measured task times | Weeks 1 and 2; labs 01 and 02 |
| Difficulty and dropout | Deaths, time and ratings per level, `R` estimates, strain, predicted against actual stops | Week 3; lab 03 |
| Reward and motivation | Reward-stream log with schedule labels, stopping points and the ethics checklist; or a need audit with a short PENS-style or rating-scale motivation survey | Weeks 4, 5 and 6; labs 04, 05 and 06 |
| Onboarding timeline | Coded teach, use and need events, recall at each moment of need, sensitivity runs | Week 7; lab 07 |
| Heuristic evaluation | Independent evaluators, consolidated findings, severity means, capture-recapture range | Week 9; lab 09 and the heuristic evaluation brief |
| HUD glance audit | Information inventory, θ, `T` and look-away share for measured setups, observed glance counts | Week 10; lab 10 |
| Accessibility audit | Scoped guideline audit, contrast on worst-case backgrounds, text size in degrees, colour analysis | Week 11; lab 11 |
| Survey and interviews | A survey with invitation counts per group, response-rate ratio and weighting; four or more interviews coded into themes | Week 12; lab 12 |
| Biometrics or gaze | Peaks with a second channel, or AOI hit ratio, time to first look and recall, with consent covering sensitive data | Week 13; lab 13 |

You may reuse work from your heuristic evaluation if you evaluated a screen of the same game. Say what you reused, and add new analysis that serves the final study's question. Data from labs doesn't count as new data unless the course team approves it at the proposal stage.

**Triage and reporting** follow week 14. Fix your weights and bar before you look at the data, and write them in the method section of your proposal.

## Ethics

- Adult testers only. Informed consent before any recording, naming what you record, why, how long you keep it, and that the tester can stop at any time.
- Tester codes, never names, in every file and slide. Crop or blur faces in any clip shown beyond your group.
- Physiological and face data are sensitive (week 13). If you use them, say so in the consent sheet, store them under codes and delete raw recordings when grades are released.
- The course team has registered the course's minimal-risk exercises with the institution. Studies outside those exercises (anything involving minors, deception beyond the lab 04 protocol, or health data beyond a consumer wristband) need approval at the proposal stage.
- Report problems as properties of the design, never as failings of testers or developers.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Week 11 lab session | Game and draft question declared; groups confirmed | No |
| End of week 12 | **Proposal**, one page (see below) | Yes, 5 points |
| Week 13 lab session | Pilot session run; setup fixed; proposal comments answered | No |
| Weeks 13 and 14 | Data collection | No |
| Week 14 lab session | Lab 14 dry run. Bring a draft one-page summary of your own study for a five-minute check | No, but required |
| Week 15 session | **Presentation** (10 minutes per group) and **individual vivas** (8 minutes each) | Yes |
| Seven days after week 15 | **Report**, tracker, appendices and individual method logs | Yes |

### The proposal (one page)

1. Game, version, platform.
2. Research question and target player, with recruitment criteria.
3. The core usability test: three to five tasks with success criteria, and the zero-tolerance items.
4. The two or more method modules, each with one sentence on what it adds to the question.
5. Triage policy: severity weights and bar. Use the week 14 defaults (`1, 3, 10, 30` and `T = 1`) unless you justify a change in two sentences.
6. Ethics: what you record, and any item that needs approval.
7. Who does what.

## The report

At most eight pages, plus appendices, in the week 14 structure.

1. **One-page summary.** The question in one sentence, what was tested and with whom, the fix-now findings in one line each, what works, and the single most important limit.
2. **Findings by tier.** Fix now, then investigate (each with a named next step), then backlog. Inside each tier, sort by `U`. Each finding in the five-part form with severity, count, Wilson interval and tier on the title line. Every quote is verbatim with tester code and timestamp.
3. **What worked.** Positive findings in the same format, briefly.
4. **Module results.** For each method module, its numbers and model output in half a page to a page, and one paragraph on how it supports, contradicts or adds to the usability findings.
5. **Method and limits.** Build and version, tasks, tester profiles (codes), `n` per method, how severity was rated and by how many raters, the weights and bar, and what the study can't tell you.
6. **Appendix.** Observation logs, script outputs, survey instruments, coding sheets, consent text, clip index, and the findings tracker in the lab 14 format.

Screenshots and short clips of the game may appear as evidence, cropped to the interface under study and labelled with game, version and date. Don't use the game's art, logos or characters decoratively.

### The individual method log (one page per member)

Each member writes one page on their own, submitted with the report. Name the parts of the study you ran and analysed. Pick one decision the group made about method or analysis (a sample size, a severity call, a model parameter, a tier on the boundary) and say what the alternative was and why you chose as you did. End with one thing you would do differently.

## The presentation and viva

**Presentation (10 minutes per group).** The question, the method in one slide, the fix-now findings with one clip each (20 to 40 seconds), what works, and the main limit. Stop and let the audience respond, as week 14 describes. Timing is enforced.

**Viva (8 minutes per student, individually, in the same week).**

| Minutes | What happens |
|---|---|
| 0 to 3 | The examiner picks one of your findings or module results and asks you to explain the number behind it: where it came from, what model produced it, and what would change it. |
| 3 to 6 | One question from the exam bank for a week your study used, rewritten with your study's numbers. |
| 6 to 8 | The examiner changes one assumption (a weight, the bar, a model parameter, the number of testers) and asks what happens to one finding's tier or one module's conclusion. |

## Rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Proposal (group) | 5 | 5: all seven parts, question and player precise, policy fixed | 4: one part vague | 3: several parts vague | 0-2: missing or after data collection |
| Question and method choice (group) | 10 | 9-10: narrow question with a named player and moment; modules clearly serve it; sample sizes justified | 7-8: good question, one module loosely connected | 4-6: broad question, or modules chosen for convenience | 0-3: no clear question |
| Data collection and ethics (group) | 10 | 9-10: usability test run to the week 8 standard; modules run to their lab standard; consent, codes and sensitive data handled | 7-8: minor slips, documented | 4-6: coaching, loose logging, or thin recruitment | 0-3: data unusable, or identifiable data |
| Analysis with the course models (group) | 15 | 13-15: each module analysed with its lecture model, parameters stated, uncertainty used (intervals, sensitivity runs, capture ranges, response-rate ratio); robust and fragile results separated | 10-12: models applied, uncertainty mentioned but not always used | 6-9: models applied with errors, or uncertainty ignored | 0-5: description without models |
| Findings and triage (group) | 15 | 13-15: problem-first titles, testers counted not notes, policy fixed before analysis, tiers correct, five parts kept apart, verbatim quotes with codes, investigate items with next steps | 10-12: tiers right, writing blurs parts | 6-9: frequency ordering in places, or percentages without counts | 0-5: findings are opinions |
| Summary, structure and limits (group) | 10 | 9-10: a producer reading page one would schedule the right fixes; limits stated plainly; within length | 7-8: summary clear, one limit missing | 4-6: summary buries a blocker or overclaims | 0-3: no summary |
| Presentation (group) | 10 | 9-10: on time, one clip per fix-now finding, numbers readable, responds to questions with evidence | 7-8: minor overrun or one weak clip | 4-6: reads slides, few numbers | 0-3: missing or far over time |
| Viva (individual) | 15 | 13-15: explains own numbers and models correctly, answers the rewritten bank question, predicts the effect of the changed assumption with a reason | 10-12: one slip, method sound | 6-9: partial method, or explains only parts they ran | 0-5: can't explain the group's main results |
| Individual method log (individual) | 10 | 9-10: names own contribution, one decision with a real alternative weighed, one concrete change | 7-8: decision described, alternative thin | 4-6: generic reflection | 0-3: missing |

Group criteria (75 points) give every member the same score. Individual criteria (25 points) are scored per student.

## Late work and extensions

- The proposal can be up to three days late with no penalty to its points, but data collection may not start until it is approved.
- The report may be up to 48 hours late for a 10-point penalty. After that it scores 0 unless an extension was agreed before the deadline.
- A missed presentation or viva can be rescheduled only for documented illness or emergency. A missed viva without one scores 0 for that criterion.

## Academic integrity

Discuss methods with other groups, and you should. The data, analysis and words are your group's own, and the method log and viva answers are yours alone. Cite any published source you use about the game (patch notes, developer talks, wiki pages) with its date and version. Don't invent quotes. Every quote in the report must come from your own logs.
