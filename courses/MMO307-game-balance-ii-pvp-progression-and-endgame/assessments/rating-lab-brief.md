# MMO307 · Rating lab brief

**Weight:** 30% of the course grade.
**What counts:** five labs, [08](../labs/lab08.md), [09](../labs/lab09.md), [10](../labs/lab10.md), [11](../labs/lab11.md) and [14](../labs/lab14.md), plus a one-page rating system sheet handed in with lab 14.
**When:** each lab is assigned in its lecture week and is due at the start of the next week's class. Lab 14 and the sheet are due one week after the week 14 class, so the sheet can go straight into the [final season design](final-season-design-brief.md).
**Work mode:** individual. You may discuss approaches with classmates, but the code, the numbers and the memos are your own.
**Lectures:** [week 8, Elo](../lectures/w08-elo-and-expected-score.md), [week 9, Glicko and TrueSkill](../lectures/w09-glicko-and-trueskill.md), [week 10, matchmaking](../lectures/w10-matchmaking-quality-vs-queue-time.md), [week 11, seasons and resets](../lectures/w11-seasonal-structures-and-resets.md) and [week 14, win rates and pick rates](../lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md).

## What this component is for

The course outcome "implement and tune Elo/Glicko-style rating systems" is assessed here. Implementing a rating system is short work. The update rule is one line. Tuning it is the real job, and every one of these labs is a tuning job with a target written down before you start. Lab 08 sets K against speed and noise. Lab 09 sets the drift constant `c` for Glicko and tests TrueSkill on parties. Lab 10 tunes the matchmaker that feeds the rating system its games. Lab 11 decides what a season end does to the ratings. Lab 14 shows that the rating system is part of the balance measurement.

Together they are the rating half of your final project. The simulation you build in the [final season design](final-season-design-brief.md) reuses your Elo or Glicko update, your matchmaker, your reset rule and your dashboard rule. A lab you skip is work you will still have to do in week 15.

## The labs

| Lab | Week | What you tune | Checker | Reused in the final |
|---|---|---|---|---|
| [08](../labs/lab08.md) | 8 | A two-stage K rule against a placement target and a wobble target | `test_elo.py` | the rating update |
| [09](../labs/lab09.md) | 9 | Glicko's `c`, and a system choice for a 3v3 mode with parties | `test_ratings.py` | the rating update, if you choose Glicko or TrueSkill |
| [10](../labs/lab10.md) | 10 | Window growth against a wait target and a fairness ceiling, peak and off-peak | `test_queue_model.py` | the matchmaker |
| [11](../labs/lab11.md) | 11 | Reset strength `α`, K, and a visible star bonus | `test_season_sim.py` | the season end |
| [14](../labs/lab14.md) | 14 | A dashboard rule that flags an overtuned class within 7 days | `test_ladder.py` | the balance dashboard |

## The rating system sheet

One page, handed in with lab 14. It collects the decisions from all five labs in one place, in the form your final season design will quote. Use this table, one row per decision.

| Decision | Your value | Where it came from | The number that justifies it |
|---|---|---|---|
| Rating system (Elo, Glicko-1, Glicko-2, TrueSkill) | | Lab 08 or 09 memo | |
| K rule, or `c` and RD floor, or `β` and `τ` | | Lab 08 step 5 or Lab 09 step 4 | settled wobble and games to place |
| Matchmaker window (`w₀`, growth, `w_max`) | | Lab 10 steps 5 and 6 | 90th-percentile top-band wait and population fairness |
| Season end (`α`, provisional K, visible reset, star bonus) | | Lab 11 steps 3 and 6 | games to settle and excess lopsided games |
| Dashboard rule (signal, threshold, sample-size condition) | | Lab 14 step 7 | hit rate at `δ = 0` and at `δ = +60` |

Under the table, write at most 150 words on the one place where two of your decisions pull against each other. A common example is a high provisional K after a soft reset, which settles players fast and makes the lab 14 early window shorter. Name the trade in numbers.

## Rubric

The component is out of 100 points. Each lab is marked out of 100 with its own rubric and then scaled to the points below. The sheet is marked directly.

| Part | Topic | Points |
|---|---|---|
| Lab 08 | Elo ladder, K sweep, calibration, two-stage K, pool audit | 20 |
| Lab 09 | Glicko-1 and TrueSkill, career table, idle players, parties | 20 |
| Lab 10 | Closed-form queue model, simulation, bands, peak and off-peak tuning | 16 |
| Lab 11 | Season simulation, reset sweep, model check, visible track | 16 |
| Lab 14 | Rating absorbs advantage, `f` sweep, representation, dashboard rule | 18 |
| Rating system sheet | Five decisions with sources and numbers; one trade named with numbers | 10 |
| **Total** | | **100** |

Your rating lab component is the points total multiplied by 0.30. A lab 10 marked 80 out of 100 contributes `0.80 × 16 = 12.8` points, which is 3.84% of the course grade.

### How the sheet is marked

| Criterion | Full marks | Half marks | Zero | Points |
|---|---|---|---|---|
| Decisions complete | All five rows filled with values that match your lab reports | Three or four rows, or a value that contradicts its lab | Two or fewer | 4 |
| Justifying numbers | Every row cites a measured number from your own runs, with seed | Numbers present but some from the lecture, not your runs | Opinions only | 4 |
| The named trade | Two decisions, the direction of the conflict and its size in numbers | Conflict named without numbers | Missing | 2 |

## How each lab is marked

Labs 08 and 09 score each criterion in bands from 0 to 4, labelled Excellent (4), Adequate (2 to 3) and Weak (0 to 1). A criterion earns `weight × band ÷ 4`. Labs 10, 11 and 14 score each criterion at full marks, half marks or zero. The arithmetic is the same. A half-mark criterion weighted 20% earns 10 points.

### Automatic checks

Every lab ships a checker that fails on the untouched starter and passes on a correct solution. Markers run it from a clean copy of your lab folder with the course interpreter, `.venv/bin/python`.

- **The correctness criterion is capped by the checker.** The first criterion in every lab rubric cannot score above Weak (band 1, or zero in labs 10, 11 and 14) if the checker does not pass on the marker's machine.
- **"Works on my machine" is a fail.** Absolute paths, files outside the lab folder, packages outside the standard library and edited checkers all count as a failing check.

### Seeds and reproducibility

Every number in a lab report must come with the command and seed that produced it. Markers rerun at least two numbers per report. A number that cannot be reproduced scores as missing for the criterion it supports. Where a lab asks for several seeds, report the spread as well as the mean. A single lucky seed is not evidence.

### Numbers before claims

Each lab ends with a memo or report to a named reader, a ladder designer, a PvP systems lead or a balance team. It is marked on its numbers. "K = 24 feels stable" earns the lowest band. "K = 24 gives a settled wobble of 45.7 points in the formula and 44.9 over rounds 200 to 300 on seed 7, against a target of 50" earns the highest.

## Late work and resubmission

Labs submitted up to 48 hours late lose 10% of their mark. After that they are marked for feedback only. You may resubmit one of labs 08 to 11 before the lab 14 deadline, with a short note of what you changed. The resubmitted mark replaces the original, capped at 80 out of 100.

## Practice

The [exam bank](exam-bank.md) has compute and code questions for weeks 8 to 11 and 14. Lab sessions open with two or three of them as an ungraded quiz. Questions 29 to 46 and 56 to 60 are the ones closest to these labs.
