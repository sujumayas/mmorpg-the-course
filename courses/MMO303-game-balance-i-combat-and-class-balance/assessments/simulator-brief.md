# MMO303 · Combat simulator brief

**Weight:** 30% of the course grade.
**Work mode:** pairs for Milestone 1 (as in Lab 11), individual from Milestone 2 onward. If you continue your pair's Lab 11 code, say which parts you wrote.
**Language:** Python 3 is the default. Another language is allowed if the simulator takes a seed, an iteration count and a fight style from the command line.

## The job

Build a Monte Carlo combat simulator you would trust to decide a balance change. By the end of week 14 it must play single-target fights, duels and small group fights from class definitions in a data file, report every result with an error bar, and pass a validation suite built from the closed forms in this course. You will use it in week 15 for the [final balance pass](final-balance-pass-brief.md), so any shortcut you take here comes back to you there.

The simulator grows over three milestones, all from labs you already do.

| Milestone | Week due | Source | Share of this 30% |
|---|---|---|---|
| M1: group combat | end of week 11 | [Lab 11](../labs/lab11.md), scored with its rubric | 20% |
| M2: event-driven core, validated | start of week 14 | [Lab 13](../labs/lab13.md), scored with its rubric | 30% |
| M3: integrated simulator and report | end of week 14 | this brief | 40% |
| Viva | week 15, before the final presentations | this brief | 10% |

## What M3 must do

### Core

1. **Event-driven clock.** A priority queue of timed events, as in the week 13 lecture, section 3. No fixed-step loop for single-target and duel modes. The Lab 11 group mode may keep its `dt` loop if you document it.
2. **Class definitions in data.** Classes live in YAML or JSON: base hit, crit chance and multiplier, action time, health, armor, magic resistance, damage type, melee or ranged, and any special rule. Adding a fifth class must not need a code change unless it has a new kind of special rule.
3. **Special rules.** At least these three, each switched on from the data file:
   - a proc with an internal cooldown that grants a timed buff (the Lab 13 Berserker),
   - a builder and spender with a priority list (the Lab 13 Ritualist),
   - lost actions from movement for melee classes, as a probability per action.
4. **Mitigation.** Physical damage multiplied by `K / (K + armor)` and magic by `K / (K + MR)`, with `K` in the data file. This is the week 2 and 3 model.
5. **Three modes.**
   - `pve`: one actor against a dummy for a fixed fight length.
   - `duel`: two actors attack each other from full health, acting on their own clocks, until one dies. A same-step double death is a draw worth half a win.
   - `group`: the Lab 11 simulator, with focus and spread targeting.
6. **Randomness.** One seeded generator per actor, so that common random numbers work. A `--crn` flag runs two versions of the roster on the same streams and reports the difference.
7. **Stopping rule.** Either a fixed `--iterations N`, or `--target-error x`, which keeps running until the 95% half-width of every reported mean is below `x` percent of that mean, with a cap on iterations.

### Output

For every result, report the mean, the single-fight SD, the standard error and the 95% interval, plus `N` and the seed. For `pve`, also report each ability's share of damage, since Lab 14 and the final pass need it. For `duel`, report the win rate with its interval, `p̂ ± 1.96 × sqrt(p̂(1 − p̂)/N)`. Write a CSV and a short human-readable table.

### Validation suite

A `pytest` file (or the equivalent in your language) that runs in under two minutes and includes at least these checks.

| Check | Expected value | Tolerance |
|---|---|---|
| Crit chance 0%, 40 actions in 60 s, `D = 100` | 66.67 DPS exactly | exact |
| Crit chance 100%, same fight | 133.33 DPS exactly | exact |
| Duelist (100, 25%, 2×), 60 s | `μ = 83.33`, `σ = 4.56` | mean within 4 SE, SD within 5% |
| Marksman (110, 10%, 2×), 60 s | `μ = 80.67`, `σ = 3.48` | mean within 4 SE, SD within 5% |
| Armor 100, `K = 100`, one 200-damage hit | 100 damage taken | exact |
| Group mode, 10 vs 8, 1,000 HP, 100 DPS, focus vs focus | 6 survivors, about 10.5 s | survivors exact, time within 0.2 s |
| Ritualist hand calculation from Lab 13 | your derived mean | mean within 4 SE |
| Seed reproducibility | two runs with the same seed | identical output |

Add one test of your own that would have caught a bug you actually hit, and say in the report which bug.

### Report

1,500 to 2,000 words, in `report.md`.

- **Architecture.** One diagram or list of the event types and how the queue handles them.
- **Validation.** The table above with your measured values.
- **Performance.** Fights per second in each mode on your machine, and the time to reach a 0.5% half-width for the Duelist.
- **Limits.** The three kinds of error from the week 13 lecture (sampling, model, policy). For each, one concrete way your simulator could mislead a designer.
- **One experiment.** Use the simulator to answer a question from the course that a spreadsheet could not, for example the Berserker's Frenzy uptime with and without the internal cooldown, or how often a 60-second Ritualist fight ends with unspent charges. State the question, your prediction, the result with its interval, and what it means for balance.

### README

How to install, run each mode, run the tests and reproduce every table in the report, in at most 20 lines.

## Viva

Ten minutes, one examiner, in week 15. You run your simulator live on a class definition the examiner gives you. Expect to:

- run a validation check and explain why the tolerance is what it is,
- predict a result by hand before running it (examiners draw on week 13 questions in the question bank, with new numbers),
- explain one design choice in your code, such as how you order simultaneous events.

## Rubric for M3 and the viva

M3 is scored out of 100 and the viva out of 20. Point bands within each criterion are guides, and the marker picks the band that fits best.

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Correctness and validation | 25 | 22-25: every check passes, own bug-catching test present and explained | 15-21: all closed-form checks pass, one statistical check borderline or unexplained | 6-14: plain hits correct, a special rule or mode fails validation | 0-5: validation missing or failing |
| Mechanics and modes | 20 | 18-20: all three special rules and all three modes, driven by the data file | 12-17: all present, one hard-coded or with a documented gap | 5-11: one mode or special rule missing | 0-4: single-target plain hits only |
| Statistical reporting | 20 | 18-20: every number carries SE and interval, stopping rule works, CRN flag reports the difference and its SE | 12-17: error bars on most outputs, CRN present but not measured | 5-11: point estimates in places, no stopping rule | 0-4: point estimates only |
| Reproducibility and code quality | 15 | 13-15: fresh clone runs from the README, seeds recorded in every output, readable structure | 9-12: runs with one fix, seeds mostly recorded | 4-8: runs only on the author's machine or after several fixes | 0-3: does not run |
| Report | 20 | 18-20: limits named concretely, experiment has a written prediction and an interval, plain and within length | 12-17: all sections present, experiment thin or limits generic | 5-11: sections missing or claims without numbers | 0-4: missing |
| **M3 total** | **100** | | | | |
| Viva: live run and hand prediction | 10 | 9-10: prediction within the simulator's interval, reasons clear | 6-8: prediction close, reasoning partly stated | 2-5: needs prompting to use the model | 0-1: cannot run or predict |
| Viva: explaining the code | 10 | 9-10: explains any part asked, including edge cases | 6-8: explains main loop, unsure on one edge case | 2-5: explains only with the code open and prompting | 0-1: cannot explain own code |

## Rules

- M3 is due at the end of week 14 so it can be frozen before the final pass. You may fix bugs after the deadline for your own use in week 15, but the graded M3 is the tagged version.
- Copying another student's simulator code is not allowed. Using a library for the priority queue, random numbers or statistics is fine. Using an existing game simulator is not.
- If your M2 simulator fails validation, the instructor provides a reference core after the M2 deadline. You may build M3 on it, lose the M3 "Correctness" points that the reference covers, and say so in the report.
