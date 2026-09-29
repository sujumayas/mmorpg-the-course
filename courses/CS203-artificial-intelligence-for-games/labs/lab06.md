# CS203 · Lab 06: A guard that commits

**Week:** 6 ([Finite state machines](../lectures/w06-finite-state-machines.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; pair up for the step 8 swap

## Objective

Finish a small table-driven state machine engine, then use it to turn a designer's twitchy first-draft guard into one that fights the player steadily without becoming slow to react. You will fix the guard by changing data (guards, margins, dwell times), not by adding special cases in code. By the end you should be able to look at a transition log and say which rule is missing.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab06-starter/guard.py`](lab06-starter/guard.py). It contains:
  - `Transition` (source, destination, guard function, interrupt flag) and `Machine`, whose `step()` you write in Part A. The docstring states the exact rules: transitions tried in list order, a non-interrupt transition may fire only after `min_dwell` ticks in the current state, exit hook before enter hook, at most one transition per tick, and a log of `(tick, src, dst)`.
  - `GUARD_TRANSITIONS` and `MIN_DWELL`: the designer's first draft, with single thresholds and no dwell. You fix these in Part B.
  - Four traces of player behavior at 10 ticks per second: `strafe_trace()` (circling at about 2 m, behind a pillar 2 ticks in every 17), `approach_trace()` (walks in from 10 m), `escape_trace()` (seen for 6 s, then hides for good) and `juke_trace()` (in melee, dashes out to 4 m for 3 ticks right after the fight starts, returns, then leaves for good at tick 25).
  - `python guard.py` prints each trace's transition count and a compressed state timeline.
- [`labs/lab06-starter/check_lab06.py`](lab06-starter/check_lab06.py). Ten checks. A1 to A5 test `Machine.step()`. B1 to B5 test the guard on the traces. On the starter all ten fail. With Part A done and the draft table unchanged, A1 to A5 and B3 pass and the other four fail. That is the point: the engine is right and the design is wrong.
- The interactive [`examples/w06-target-commitment.html`](../examples/w06-target-commitment.html) for the time-versus-margin intuition.

## Steps

### Part A: the engine (40 minutes)

1. Read the docstring of `Machine.step()` and write it. Keep it under 20 lines.
2. Run `python check_lab06.py` until A1 to A5 pass. If A5 fails, print `m.tick` and `m.time_in_state` inside a guard to see when your counters move.
3. Run `python guard.py` with the draft table. Copy the strafe line into your report. Count how many times the guard enters SEARCH on that trace and explain, in one sentence each, the two separate causes of the flicker you see.

### Part B: the design (50 minutes)

4. Fix the pillar problem: the guard should not give up the fight because the player was out of sight for 0.2 s. Change only guard functions. The `seen_ago` input is there for this.
5. Fix the range problem: the guard should not drop from ATTACK to CHASE every time the strafing player's distance crosses 2 m. Use a band (MA101 week 14). Choose the width from the strafe trace: its distance stays within 2 ± 0.9 m.
6. Fix the give-up problem: after losing the player for good, the guard should search for several seconds before returning to patrol, not one tick. Check B4 gives the exact tick windows. This is Metal Gear's evasion countdown.
7. Fix the juke problem with a minimum dwell on ATTACK, and only that. Then find the smallest and the largest ATTACK dwell (in ticks) for which all ten checks still pass. Report both, and explain from the juke trace's tick numbers why each limit is where it is.
8. Swap `guard.py` with a classmate. Write one new trace (at most 15 lines, using `with_memory`) that makes their guard behave badly while every existing check still passes on it. Describe the bad behavior in one sentence and propose the one-line fix.

### Part C: the note (at home)

9. Write at most 300 words for a combat designer explaining your final table. For each change, name the problem it solved, the number you chose, and what a player would notice if the number were twice as large. Include the strafe trace's transition count and attack fraction before and after.

## Deliverable

Your `guard.py` with `check_lab06.py` passing (paste its output), your step 8 trace and its description, and a PDF with the step 3 analysis, the step 7 limits, and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Engine (25%) | A1-A5 pass; `step()` is short and follows the stated rules exactly | Passes, but duplicated or hard-to-follow logic | Some A checks fail | Not attempted |
| Guard design (30%) | B1-B5 pass using only guard changes, a band and one dwell; each change is the smallest that works | All pass, with extra special cases | One or two B checks fail | Most fail |
| Dwell limits (15%) | Both limits found, each tied to the check that sets it with a reason | Limits found, reasons vague | One limit | Missing |
| Adversarial trace (15%) | A short trace that exposes a real weakness, a clear description and a one-line fix | Trace works, fix missing | Trace does not actually misbehave | Missing |
| Designer note (15%) | Every change justified with its number and the "twice as large" consequence; before/after strafe numbers | Mostly complete | Numbers missing | Missing |
