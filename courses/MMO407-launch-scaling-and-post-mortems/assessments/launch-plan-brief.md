# MMO407 · Launch plan brief

**Weight:** 50% of the course grade.
**Assigned:** week 1, built up through the labs. **Groups formed:** end of week 10. **Full draft:** start of week 14. **Final submission:** start of week 15, followed by the readiness-review panel in week 15.
**Work mode:** labs as each lab states (mostly pairs). The final plan and the panel are done in your launch plan group of 3 or 4, with a contribution statement.
**Lectures:** all fourteen, most directly [week 1, launch day anatomy](../lectures/w01-launch-day-anatomy.md), [week 2, capacity planning and login queues](../lectures/w02-capacity-planning-and-login-queues.md), [week 3, beta strategies](../lectures/w03-beta-strategies.md), [week 9, communication during crises](../lectures/w09-communication-during-crises.md), [week 13, launch plan workshop](../lectures/w13-launch-plan-workshop.md) and [week 14, presentations](../lectures/w14-presentations.md).

## What this component is for

A launch plan is the document a producer reads the night before the doors open. It says how the game will open, what can go wrong in the first week, what the team has bought to stop each thing going wrong, and who does what when it happens anyway. This component assesses the course outcome "plan a launch with capacity, queue and contingency strategies". A plan that says "we will scale as needed" earns little here. A plan that says "hour-3 wait of 30 to 100 minutes across three session models, layers close on day 7, trading switch owned by the live-ops lead with a 10% reopening limit" earns a lot, because every one of those numbers can be checked.

The component has three parts.

| Part | What is assessed | When | Weight within this component | Share of the course grade |
|---|---|---|---|---|
| Lab marks | Labs 01, 02, 03, 07, 08, 09, 10, 13 and 14, each marked by its own rubric | weekly | 30 | 15% |
| Written launch plan | The group's final plan, marked with the rubric below | start of week 15 | 40 | 20% |
| Readiness-review panel | The group's presentation of the plan and the post-mortem analysis, marked with the panel rubric below | week 15 | 30 | 15% |
| **Total** | | | **100** | **50%** |

The lab part is the mean of the nine lab marks. Labs 04, 05, 06, 11 and 12 count toward the [case analyses](case-analyses-brief.md) instead, although Lab 06's reopening rule and Lab 11's preservation numbers also appear in your plan.

## Which launch you plan

Choose one of these by the end of week 10 and tell the instructor.

- **The course reference launch.** Use the scenarios the labs already give you: Lab 02 step 8 for arrivals, worlds and the day-30 forecast; Lab 03 step 7 for launch-week exposure and the beta budget; Lab 07 step 8 for the fresh PvP realm; Lab 08 step 10 for the monthly siege. Invent the game's name, genre and platforms, and keep every given number.
- **Your PR402 capstone.** You may plan the launch of your capstone game if the instructor approves it by the end of week 10. You must then state forecast inputs at the same level of detail as the reference launch (arrival rates by phase, world cap, session length, launch-week player-hours, day-30 peak), each with where it came from.

Groups of 3 or 4 are usually two lab pairs merged. When your pairs' lab outputs disagree, reconcile them in the plan and say which numbers you kept and why.

## What you submit

A folder or repository link containing:

1. **`launch-plan.md`** (or PDF), at most 6,000 words for sections 1 to 7 and at most 3,000 words for the annexes. Tables and code output do not count toward the limits.
2. **`code/`**, your lab code and any scripts that produce the plan's numbers, runnable with the course Python (`.venv/bin/python`) from a clean copy. A `README` lists the command that produces each table and chart.
3. **`slides.pdf`**, the panel deck (see the panel section).
4. **`contribution.md`**, one paragraph per member on what they wrote and built, signed by all members.

### Required sections

The seven sections come from [week 13's table](../lectures/w13-launch-plan-workshop.md). Each names the lab it grows from.

| Section | Must contain | Grows from |
|---|---|---|
| 1. Launch shape | Preload, head start, unlock time and region order, each justified by a failure it prevents; the capacity table with the expected bottleneck marked; at least four measurable go/no-go criteria | Lab 01 |
| 2. Capacity | World count, caps, layers and when each closes; the queue and back-of-queue wait at hours 1 to 6 as a range across session models; the day-30 population per world against the "alive" threshold | Lab 02 |
| 3. Test evidence | Beta phases with player-hours, the rarest crash rate they can rule out, per-path and crowd exposure, and a risk-to-exposure table with every uncovered row given a launch response | Lab 03 |
| 4. Risk register | At least six risks with `p`, `I` in k ph and a source for each number (guesses labelled as guesses); at least one scenario row; the disaster line `D`, who agreed it and when | Lab 13 |
| 5. Mitigations | Candidate fixes with costs; the plan each of the three rules picks; `E[L]`, `P(L > D)` and the exceedance curve for your chosen plan and the expected-loss plan; the break-even penalty and the rule you used | Lab 13 |
| 6. Triggers and war room | At least four triggers in the six-part form (signal, threshold, action, owner, lead time, stand-down), each with a `t_s + T ≤ t_h` check; war room roles by name; the kill-switch list with owners | Labs 01 and 13 |
| 7. Communication | Cost ratios with reasons; the announcement each implies; update templates with all five parts; the channel plan and source of truth | Lab 09 |

Annexes:

- **A. Population health.** The faction or realm balance plan, its alert rule and the social tie it breaks (Lab 07).
- **B. Player-scheduled peaks.** The event plan for the siege, with objective size, travel rule and real-time brake (Lab 08).
- **C. Exploits and reopening.** The value-path inventory and the reopening rule with its risk limit and owner (Lab 06 Part B).
- **D. Recovery.** What the team does if the launch goes badly anyway: which stock each move works on and the months the store page will lag (Lab 10).
- **E. Sunset.** The preservation section with the rebuild-clock numbers and approval dates (Lab 11).
- **F. Readiness scorecard.** Criteria, weights, gates, measured scores with evidence, and the verdict under all three rules (Lab 14).
- **G. The borrowed lesson.** One lesson from your group's post-mortem analysis, written as a gate, weight, risk or trigger, and the line of the plan it changed.

## Milestones

| Week | Milestone | What it gives the plan |
|---|---|---|
| 1 | Lab 01 due | readiness review, first page of section 1 |
| 2 | Lab 02 due | capacity memo, section 2 |
| 3 | Lab 03 due | beta program and risk-to-exposure table, section 3 |
| 6 | Lab 06 due (case analyses) | reopening rule, annex C |
| 7 | Lab 07 due | balance plan, annex A |
| 8 | Lab 08 due | event plan, annex B |
| 9 | Lab 09 due | communications kit, section 7 |
| 10 | Lab 10 due; groups formed; launch chosen | recovery plan, annex D |
| 11 | Lab 11 due (case analyses) | preservation numbers, annex E |
| 13 | In-class premortem; Lab 13 due | register, mitigations and triggers, sections 4 to 6 |
| 14 | Full draft at the start of class; mock review; Lab 14 dry run | scorecard (annex F) and revised slides |
| 15 | Final submission at the start of the week; panel slots | the assessed plan and presentation |

The week 14 draft is not marked. It is what the mock review and the dry-run group read, so a missing draft costs you the feedback, not marks.

## Gates

Section 2 of the week 14 lecture argues that a readiness review should check gates before it adds points. This component follows its own advice. A plan that fails a gate is returned for resubmission within one week, and the written plan and panel marks are then capped at 50.

1. **Capacity reproduces.** The marker runs your Lab 02 code from a clean copy, and it prints the section 2 queue numbers.
2. **Every real-game fact is sourced.** Every claim about a shipped game in the plan or on a slide has a source with a date or version.
3. **The disaster line came first.** Section 4 states `D`, who agreed it and when, and section 5 states the rule used to choose mitigations.
4. **The post-mortem analysis uses a model.** The analysis presented at the panel names a model from this program and a parameter that moved (the written analysis is marked in the [case analyses brief](case-analyses-brief.md)).

## Rubric: written launch plan (100 points)

A criterion earns full points for Excellent, half for Adequate and zero for Missing or wrong. Markers may award a point or two between bands where the work sits between them.

| Criterion | Excellent | Adequate | Missing or wrong | Points |
|---|---|---|---|---|
| Launch shape and go/no-go (section 1) | Every timeline item tied to a failure it prevents; bottleneck marked from measured capacities; four or more go/no-go criteria with thresholds | Timeline and capacities present; criteria vague ("auth stable") | No capacity table or no criteria | 8 |
| Capacity as a range (section 2) | Queue and wait at hours 1 to 6 across session models; layers with close dates; day-30 test passed or the trade-off stated with numbers | Single-model forecast, or day-30 test missing | Single number with no model | 15 |
| Test evidence (section 3) | Beta sized from a stated crash rate with `3 / r`; per-path and crowd exposure covered; every uncovered risk has a launch response | Sizing correct, one exposure type ignored | "The beta will find bugs" | 10 |
| Register and mitigations (sections 4 and 5) | Six or more sourced risks and a scenario row; `D` agreed first; both candidate plans with `E[L]` and `P(L > D)`; exceedance curves; break-even `B` and the chosen rule | Register and plans present, sources or the break-even thin | Sorted by `p × I` only, or no `D` | 20 |
| Triggers and war room (section 6) | Four or more complete triggers, each with a passing lead-time check; roles by name; every kill switch owned | Triggers missing owner, stand-down or lead-time check | "The team will decide" | 12 |
| Communication (section 7) | Cost ratios justified; announcements computed from a log; templates with all five parts and no promise the log says is likely to break; channels survive a domain outage | Templates complete, times not computed | Missing | 8 |
| Annexes A to E | Each annex carries its lab's numbers into this launch, with its owner and its trigger | Annexes copied from the labs without adapting to this launch | Two or more annexes missing | 10 |
| Scorecard and borrowed lesson (annexes F and G) | Every gate tied to a risk above `D`; measured scores with evidence; no-evidence rows scored 0; the borrowed lesson changes a named line of the plan | Scorecard present, evidence thin or lesson not traced to a line | Missing | 10 |
| Reproducibility and sources | Every number traced to a command or a cited source; guesses labelled | Minor gaps | Numbers cannot be traced | 7 |
| **Total** | | | | **100** |

## The readiness-review panel

The panel is set up as a launch readiness review ([week 14](../lectures/w14-presentations.md), section 1). It is the instructor, one guest from industry where possible, and one student from another group. Each group has a 30-minute slot.

| Part | Time | Content |
|---|---|---|
| Launch plan | 12 minutes | The seven-part order from week 14 section 3: decision, gate table, capacity as a range, the tail, triggers and roles, the borrowed lesson, what would change your recommendation |
| Post-mortem analysis | 8 minutes | The four-part order from week 14 section 4: what happened with dates, the model, what the team could have seen and when, the transferable lesson |
| Questions | 8 minutes | At least one gate, one tail and one transfer question, and at least one question to each member |
| Changeover | 2 minutes | |

The mark is the mean of the instructor's and the guest's sheets. The student panellist fills in the same sheet, and it is returned to the group as feedback. The four gates above are checked first, and a presentation that fails one is returned as described there.

## Rubric: readiness-review panel (100 points)

The weights are the ones announced in [week 14, section 5](../lectures/w14-presentations.md). A criterion earns full points for Excellent, about half for Adequate, and a quarter or less for Weak.

| Criterion | Excellent | Adequate | Weak | Points |
|---|---|---|---|---|
| Launch plan content | Decision and date first; gate table with measured scores and the closest-to-failing gate at the top; capacity as a range with its source; both exceedance curves and the rule that chose between them; triggers with lead times | All parts present, but the weakest gate is buried or capacity is a single number | Plan described in adjectives; numbers without sources or units | 40 |
| Post-mortem analysis | Dated timeline with facts kept apart from interpretation; one model applied with the parameter that moved and roughly how far; a fair account of what was knowable then; a lesson written as a gate, weight, risk or trigger | Model named but the parameter or its size is vague, or the lesson is sound but not in a plan-ready form | A story with no model, or hindsight blame | 25 |
| Link between the halves | The borrowed lesson is shown as a specific line of the plan, and the group says what the plan would look like without it | The link is stated but not traced to a line | No link | 10 |
| Handling of questions | Answers the gate, tail and transfer questions with a number and a slide or appendix reference; says what would change the recommendation; every member answers at least one question well | Answers correct but general, or one member cannot answer | Reassurance instead of numbers | 15 |
| Clarity of the slides | Every number has its unit and source on the slide; the red is shown; one idea per slide; readable at the back of the room | Mostly clear, a few unsourced numbers or crowded slides | Hard to follow; numbers without units | 10 |
| **Total** | | | | **100** |

## Individual marks

The written plan and panel marks are group marks. The instructor may adjust an individual's mark by up to 10 points either way, using the contribution statement and that member's answers at the panel. A group that splits up tells the instructor before week 13, and each part hands in the sections it wrote with a note saying who built what.

## Late work and integrity

- **Late submission.** Up to 48 hours late, the written plan is marked out of 80 instead of 100. The panel slot cannot move unless the timetable allows it. Labs follow their own deadlines. Extensions for illness or other documented reasons follow the university policy.
- **Integrity.** Every number must come from your own runs or a cited source. You may reuse your own lab work and your partner's, and you must say so. Real-game facts must be verified and cited with a version or era, and the plan must not use copyrighted art, characters or long quotes. At the panel you must be able to explain every number on your slides.
