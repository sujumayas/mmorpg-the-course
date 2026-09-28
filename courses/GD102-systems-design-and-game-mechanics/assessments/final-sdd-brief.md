# GD102 · Final system design document and simulation brief

**Weight:** 40% of the course grade.
**Assigned:** week 12, when the economy design project is handed in. **Final submission:** week 15, day 3. **Viva:** week 15, days 4 and 5.
**Milestones that count toward it:** [lab 13](../labs/lab13.md) (system specification) and [lab 14](../labs/lab14.md) (tuning an idle economy).
**Lectures:** [week 13, systems documentation](../lectures/w13-systems-documentation.md) and [week 14, tuning with spreadsheets](../lectures/w14-tuning-with-spreadsheets.md) set the format. The content draws on every week, especially [week 7](../lectures/w07-internal-economies-sources-drains-converters.md), [week 8](../lectures/w08-core-loops-and-meta-loops.md) and [week 9](../lectures/w09-progression-systems-skill-vs-power.md).

## What this component is for

A system design document (SDD) is done when someone can build and test the system without asking you a question. That is the week 13 test, and it is the test this component applies. The simulation is the other half. Every derived number in your document must come from a model that runs, so that a reader who doubts a number can change an input and watch it move.

You write the SDD for the game from your [economy design project](economy-design-brief.md). By week 12 you have its economy, its core and meta loops and one source of power. The SDD turns that into a specification an engineer could build, adds two more systems, and shows the whole thing tuned against targets you state in advance.

## The document

### Front page: the one-page view

One page, diagram-heavy, in the spirit of the one-page designs the week 13 lecture describes. It holds the Machinations diagram of the whole game's economy, the parameter table for the ten most important numbers, the derived-numbers table, and one sentence naming the play rhythm the game rewards (the knee or the cadence, in hours or sessions). A reader who sees only this page should know what the game's systems do.

### Body: the week 13 template

Use the ten headings from the week 13 lecture, section 3, in this order: purpose, vocabulary, model, rules, parameters, derived numbers, edge cases and states, interfaces, telemetry and success criteria, open questions and change log. Number every rule (4.1, 4.2 ...) so review comments can point at it.

The body must specify three systems. Give each its own numbered block of rules, parameters and derived numbers, and one shared vocabulary and change log.

| System | What it must contain | Where you practised it |
|---|---|---|
| **S1. Economy** | Your Part C economy, revised after feedback. Every source, drain, converter and trader as a numbered rule. `M*`, half-life and money per player in the derived numbers. The three stress tests restated as success criteria. | Lab 07 and Part C |
| **S2. Progression** | The power source from Part C, specified. For one representative challenge, `H`, `A`, the mistake budget and the 50% iso-win mistake rate at the expected level and at +5 levels. One valve for stuck players, with the breakpoint at which it first helps. | Lab 09 |
| **S3. One more system**, your choice | One of: a capped regenerating stock with its knee and timer rule (lab 13); a counter loop with its stable mix and first-week picture (lab 11); a systemic object set with property rules, pair counts and a QA budget (lab 10); or a generator with a sweep table and a threshold (lab 12). It must connect to S1 or S2 through a named interface. | Labs 10 to 13 |

### Appendices

- **A. Loop anatomy.** The clock table (moment, core, meta, long arc), the core loop as a `min` of limits, the bend, and the meta loop's exchange rate and cadence. The lab 08 part B method applied to your own game.
- **B. Tuning appendix.** Three design targets written as check columns before tuning. For each, the knob you changed, its old and new value, the range that would also work, what else it moved, and the alternative you rejected. One one-at-a-time sensitivity table and a tornado chart for your most important target. The lab 14 method applied to your own game.
- **C. Test cases.** At least 12 given/when/then cases across the three systems. At least one must separate two plausible implementations of a timer or cap rule, one must cover a stock at zero, and one must cover a parameter changed by a patch while players hold a stock.
- **D. Simulation README.** How to run the simulation, which tab or function holds each derived number, and the seed for any random run.

Length: the body is 4,000 to 6,000 words plus tables. Long prose that restates a table loses marks, as the week 13 lecture warns.

## The simulation

One spreadsheet workbook, or one script with a results file. Python standard library, with `matplotlib` optional, is fine for scripts.

- **Names match.** Every parameter in the document's tables has the same name in the simulation's inputs. A reader who searches for `regen_minutes` finds it in both places.
- **Runs the whole economy.** At least 180 days, or 100 runs or cycles if your step is not a day. Every derived number in the document is a cell or printed value in the simulation, with its formula next to it.
- **Checks.** One check column or assertion for each derived number and each tuning target, green when it passes. The conservation check from week 5 for your main currency.
- **Scenarios.** At least three named scenarios switchable from one cell or one argument: your baseline, a target-player scenario from your purpose section, and one patch proposal from your open questions.
- **Randomness.** If any flow is random, either compute expected values and say so, or run at least 500 trials with a fixed seed and report the mean with a 5th and 95th percentile.

Two tests are applied at marking.

- **Trace test.** The marker picks three numbers from the document and finds each in the simulation. Each must come from inputs by formula, not be typed in.
- **Change test.** The marker changes one input named in your sensitivity table by the amount in the table and checks that the results move as the table says.

## Milestones

| When | Milestone | Points |
|---|---|---|
| Week 12 lab session | Brief handed out after the economy design project is submitted. Choose S3 and tell the marker. | — |
| Week 13 lab session | **Outline.** One-page view draft, the list of headings with one line each, and the three tuning targets written as check conditions. Five minutes with a marker. | 5 |
| Start of week 14 | **Lab 13** submitted, marked with its own rubric. Its methods (derived numbers, testable rules, parameter table, given/when/then) are the model for your S3 or for the rules of S1. | 10 |
| Week 14 lab session | **Implementer swap.** A classmate reads your S1 rules and writes pseudocode for one event handler from your document alone, logging every question as in lab 13. Bring the log to the final submission. | Required, not graded |
| Start of week 15 | **Lab 14** submitted, marked with its own rubric. | 10 |
| Week 15, day 3 | **Final SDD and simulation** submitted. | 60 |
| Week 15, days 4 and 5 | **Presentation and viva**, 12 minutes each. | 15 |

Labs 13 and 14 are converted to points as `lab score / 100 × 10`, using the band conversion in the [Machinations models brief](machinations-models-brief.md) (`weight × band points / 4`, where the lab's top band is 4, "half marks" is 2 and missing is 0).

### Outline rubric (5 points)

| Points | What earns it |
|---|---|
| 5 | One-page view drafted with a diagram, all ten headings listed with a line each, three targets stated as pass or fail conditions with numbers |
| 3 | Two of the three parts present, or targets stated without numbers |
| 1 | Headings only |
| 0 | Not presented |

## Final submission rubric (60 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| One-page view, purpose and vocabulary | 6 | 6: a reader can state the play rhythm from the front page alone; every term used in the rules is defined once | 5: front page complete, one term undefined | 3-4: front page crowded or missing the derived numbers | 0-2: missing |
| Model and loops | 10 | 9-10: whole-game diagram runs, every loop signed with its minus count, S1, S2 and S3 connected through named interfaces | 7-8: diagram runs, one loop unsigned or one interface vague | 5-6: diagram does not match the rules in places | 0-4: no runnable model |
| Rules, parameters and edge cases | 14 | 13-14: rules numbered and testable with parameter names, every parameter has unit, safe range, reason and owner, edge cases cover zero, cap, offline and patch, implementer log closed | 10-12: one or two vague rules or missing ranges | 7-9: several rules in prose, table incomplete | 0-6: a reader could not build it |
| Economy analysis (S1) | 10 | 9-10: `M*`, half-life and money per player match the simulation, stress tests pass or are fixed, who pays named for each drain | 7-8: one number off or one stress test missing | 5-6: equilibrium without stress tests | 0-4: missing or wrong |
| Progression and third system (S2, S3) | 8 | 7-8: mistake budget and iso-win at both levels, valve breakpoint found, S3 applies its week's model correctly with its key number | 6: one of those thin | 4-5: models named but not applied to your numbers | 0-3: missing |
| Simulation, trace and change tests | 8 | 7-8: both tests pass, scenarios switch from one cell, checks green, randomness handled as specified | 6: one traced number is typed in, or one check red without comment | 4-5: several numbers fail to trace | 0-3: the simulation does not support the document |
| Tuning appendix, tests and change log | 4 | 4: targets written before tuning, knob choices defended with the sensitivity table, 12 or more test cases including the three required types, dated change log | 3: one of those thin | 2: tuning by trial and error, or fewer than 12 tests | 0-1: missing |

## Presentation and viva (15 points)

Each student has 12 minutes: 5 to present and 7 for questions. Present the one-page view and the one decision you are proudest of. The examiners then ask four questions. One is drawn from the [exam bank](exam-bank.md) and rewritten with your document's numbers.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Walkthrough | 4 | 4: the play rhythm and one decision explained with their numbers and the rejected alternative | 3: decision clear, alternative missing | 2: describes rather than defends | 0-1: not prepared |
| Change prediction | 4 | 4: the examiner changes one input, you predict two outputs in the right direction with a reason from the model, then run it | 3: one right, reasoning sound | 2: guesses, reasons after the run | 0-1: cannot find the input |
| Exam-bank question | 4 | 4: correct answer with the model named | 3: right method, arithmetic slip | 2: partial method | 0-1: no method |
| Defending the weakest part | 3 | 3: names the weakest part, its cost in numbers and a fix | 2: names the weakness and a fix | 1: defends it without evidence | 0: no answer |

## Late work

The final SDD cannot be submitted late without documented illness or emergency, because the vivas run the next day. Work submitted up to 24 hours late with permission is marked normally. Labs 13 and 14 lose 10 of their 100 points per 48 hours late and cannot use the free lab extensions.

## Academic integrity

Your game, rules, numbers and simulation are your own. You may reuse your own lab sheets and your economy design project. You may use a classmate's pseudocode in the implementer log, because that is the point of the swap. Name any template you started from. Every fact about a shipped game must come from a course lecture and cite that lecture.
