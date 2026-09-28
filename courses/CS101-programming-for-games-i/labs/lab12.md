# CS101 · Lab 12: Bug hunt

**Week:** 12, debugging ([lecture](../lectures/w12-debugging-breakpoints-logging-rubber-ducking.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). Graded on your method as much as your fixes.

## Objective

Find and fix three bugs in a small arcade simulation using the six-step loop from the lecture: reproduce, shrink, observe, hypothesize, fix, guard. For each bug you leave behind a regression test that fails on the original code and passes on yours, plus the evidence (a log excerpt or a debugger session) that led you to it.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python 3.10 or later, no packages.

- [`asteroids_sim.py`](lab12-starter/asteroids_sim.py) is a headless game. A ship sits in the middle of a 320 × 240 field while rocks drift across. It uses the week 10 box test and the week 11 state machine. It has three planted bugs. It's deterministic for a given seed, and `python asteroids_sim.py --debug` turns on the log lines already in the code. `run(seed, frames, events)` plays a session, where `events` maps frame numbers to events such as `"pause"`.
- [`test_lab12.py`](lab12-starter/test_lab12.py) has four tests that already pass (keep them passing) and three empty tests, one per bug, for you to write. On the starter it reports `4/7 tests passed`.

## The three player reports

1. "Rocks that skim just over the top of my ship kill me, but rocks that skim just under it never do." (Several players. One says it happened early with seed 3.)
2. "If I'm about to die I pause and unpause, and I get my lives back."
3. "I left endless mode running overnight. After wave 255 it suddenly got really easy, like the first wave."

## Steps

1. **Duck first (15 min).** Before running anything, explain `overlap`, `handle_event`, `on_enter` and `next_wave` to a rubber duck or a partner, line by line. List every sentence where you said "always" or "never". Keep the list. You'll check it against what you find.
2. **Bug 1.** Reproduce it with `python asteroids_sim.py --debug` on seed 3 and find the hit at frame 76. Record the rock's position from the log. Is it really overlapping the ship, which spans x 150 to 170 and y 110 to 130? Shrink it to two boxes. Write `test_bug_1_grazing_rocks` so it builds a rock whose bottom edge sits exactly on the ship's top edge and asserts no overlap. Watch it fail. Then write the mirror case, a rock whose top edge sits on the ship's bottom edge, and explain why that one already passes. State your hypothesis in one sentence, fix the line, and rerun.
3. **Bug 2.** Reproduce it with `run(7, 600, {400: "pause", 420: "resume"})` and compare `lives` with a run that has no events. Then set a **conditional breakpoint**: put `if game["state"] == "PLAY" and game["lives"] < 3: breakpoint()` at the top of `on_enter`, run again, and use `p game["lives"]`, `n` and `c` to watch the value change. Copy that session into your journal. Write `test_bug_2_pause_refills_lives` as the smallest test that fails (no `run`, just `new_game` and `handle_event`). Fix it so lives still reset on `start` and `retry`. The lecture's section 3 tells you where that reset belongs.
4. **Bug 3.** Nobody will wait for 255 waves. Shrink the reproduction by setting `game["wave"] = 255` and calling `next_wave` directly. Log the wave number and `enemies_for_wave` for waves 253 to 257 in a table. Write `test_bug_3_wave_256_is_easy`, then fix the counter so the game logic never wraps. Extension: if the save format really must store the wave in one byte, what would you do? Write two sentences.
5. **Bisect (short).** Using the original, unfixed `next_wave`, how many calls to a "is wave N easy?" check would bisecting the waves 1 to 1,000 need to find the first bad wave? Show `log₂` working.
6. **Clean up.** Remove every `breakpoint()` and any `print` you added. Keep useful `log.debug` lines. Run `python test_lab12.py` and confirm `7/7 tests passed`.

## Deliverable

- Your fixed `asteroids_sim.py` and completed `test_lab12.py` with `7/7 tests passed`.
- A debugging journal of at most 400 words. For each bug give the reproduction (seed, frame, or direct call), the evidence (log excerpt or the pdb session from step 3), your one-sentence hypothesis, the fix as a one-line diff, and the test name. End with the step 5 answer and one line on which "always/never" sentence from step 1 turned out false.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Regression tests | Three minimal tests, each shown failing before and passing after; the four given tests still pass | Tests pass after fix but are not minimal, or failing run not shown | Missing tests or tests that pass on the buggy code | 30% |
| Fixes | Each fix changes the fewest lines and keeps intended behavior (lives reset on start and retry) | One fix over-broad or introduces a new problem | A bug not fixed | 25% |
| Evidence | Log excerpt and pdb session included and read correctly | Evidence present for two bugs | Guesswork only | 20% |
| Hypotheses | One testable sentence per bug that names the line and the value | Vague for one bug | Missing | 15% |
| Method and bisect | Duck list checked against findings, bisect count correct with working | One missing | Both missing | 10% |
