# AU101 · Lab 09: A quantized music director

**Week:** 9 ([Horizontal re-sequencing and stingers](../lectures/w09-horizontal-re-sequencing-and-stingers.md))
**Time:** one 2-hour lab session plus about 2 hours at home
**Work:** individually for Part A, in groups of three for Parts B and C

## Objective

Implement the music director from lecture section 4: sync points, the request and cancel rules, and beat-quantized stingers. Then use it as a design tool. You write a transition matrix for a raid boss encounter, run a scripted fight through it, and show with numbers that every transition answers its event fast enough and never flickers.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- [`lab09-starter/sequencer.py`](lab09-starter/sequencer.py), which contains:
  - `UNIT_BEATS`, `unit_seconds` and `expected_wait`: complete.
  - `next_sync(t, unit, bpm)`: you write it (Part A).
  - `Director`, with `request(t, target)` and `stinger(t, name)` for you to write, and `advance(t)` complete.
  - `run(events, ...)`: complete. It feeds a list of `(time, kind, value)` events to a director and returns the sorted log.
  - `TRANSITIONS` and `DEFAULT_UNIT`: the matrix from the lecture, which you replace in Part B.
  - `DEMO`: the lecture's fight. Once your code is correct, `python sequencer.py` prints exactly the log shown in lecture section 4.
- [`lab09-starter/test_sequencer.py`](lab09-starter/test_sequencer.py): 10 unit tests. Do not edit it. On the starter, 8 fail.
- From the `lab09-starter` folder: `python sequencer.py` prints the unit table and the demo log, and `python -m unittest test_sequencer -v` runs the tests.

## Steps

### Part A: the director (45 minutes)

1. Run the tests and note which fail.
2. Implement `next_sync`. Use the `1e-9` tolerance from the lecture. Explain in one sentence which test fails without it and why.
3. By hand, compute `next_sync` for `t = 7.3` at 100 BPM for the beat, bar and phrase units (lecture check-yourself question 1). Confirm with your code.
4. Implement `Director.request` with the three rules from lecture section 4: a new state sets the pending switch; a newer request replaces it; a request for the current state cancels it.
5. Implement `Director.stinger` so the stinger is logged at the next beat.
6. Run `python sequencer.py`. Your log must match the lecture's line for line. Then change the combat-to-explore entry in `TRANSITIONS` from `phrase` to `beat` and rerun. Explain what the player now hears between 12.2 s and 14 s, and why the phrase unit avoided it.

### Part B: the raid encounter (40 minutes, groups)

7. Replace `TRANSITIONS` with your matrix from the in-class activity: states explore, pull, phase2, enrage, victory, wipe. Set `BPM = 128`. Every transition the fight can produce must have an explicit entry; do not rely on `DEFAULT_UNIT`.
8. Write an event list `RAID` for this fight: pull at 10.0 s; phase 2 at 41.3 s; two player deaths (stinger `death`) at 55.0 s and 55.4 s; the boss drops out of phase 2 for a scripted 1.5 s intermission at 60.0 s (game sends `pull`) and returns (game sends `phase2`) at 61.5 s; enrage at 70.2 s; wipe at 75.9 s; explore at 80.0 s.
9. Run it and paste the log. For each state event, compute the wait (switch time minus request time).
10. Add a stinger cooldown to `Director.stinger`: a stinger with the same name is dropped if one is already logged within the last bar. Show the effect on the two deaths. (This is a change to your code, not to the tests. The tests still pass because they never fire the same stinger twice in a bar.)

### Part C: judging the design (25 minutes, groups)

11. For each unit you used, compute the average and worst-case wait at 128 BPM with `expected_wait` and `unit_seconds`.
12. Identify the transition in your matrix with the longest worst-case wait. Say whether that wait is acceptable for the event it answers, and if not, fix it with a shorter unit or a stinger. Rerun and show the new log.
13. Explain what your director does with the intermission at 60.0 to 61.5 s, and why. Would the player hear the phase 2 music stop?

### Part D: at home

14. Write a one-page music design brief for the encounter: the matrix as a table, the two stingers with their harmony plan (unpitched, per-chord variants, or common tones, from lecture section 3), the wait table from step 11 and the final log. End with one paragraph on which events you would handle with vertical layering (lab 8) instead of a state change.

## Deliverable

A zip with your `sequencer.py` (all 10 tests passing, your `TRANSITIONS`, `BPM = 128` and `RAID`), and a PDF with the answers to steps 2, 3, 6, 9, 12 and 13 plus the design brief from step 14.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Code and tests (25%) | All 10 tests pass; demo log matches the lecture exactly; stinger cooldown works | All tests pass, cooldown missing or buggy | Some tests fail | Most tests fail |
| Transition matrix (25%) | Every reachable transition explicit; units justified by event urgency; bridges noted where needed | Matrix complete, justifications generic | Several transitions left to the default | Missing |
| Wait analysis (25%) | Waits computed for every event and unit; worst case found and fixed with evidence from the rerun | Waits computed, fix not verified | Averages only | Missing |
| Design brief (25%) | Stinger harmony plan is specific to the progression; vertical versus horizontal split argued per event | Brief complete, harmony plan vague | Brief missing a section | Missing |
