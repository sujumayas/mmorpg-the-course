# MMO309 · Lab 03: The lag-tolerant movement validator

**Week:** 3 ([lecture](../lectures/w03-speed-hacks-and-movement-validation.md)) · **Time:** 2 hours in the lab plus about 2 hours at home · **Work mode:** pairs · **Counts toward:** labs (30%); the detector is reused in the final prototype (40%).

## Objective

Implement the two distance checks from the week 3 lecture and reproduce its table. Add a gravity check that stops fly and hover hacks without flagging jumps and falls. Then tune a violation threshold on a session log of 10,000 players and write a ban policy you can defend with precision and recall. You finish able to say what any movement tolerance gives a cheater and what any flag threshold costs honest players.

## Starter materials

Folder [`lab03-starter/`](lab03-starter/README.md). Standard library Python only; use `.venv/bin/python` from the repository root.

- `movement_validator.py`: the lag-spike simulation, a jump and fall generator, the seeded session log (`make_log()`, 10,000 players over 7 days, about 1% cheaters) and all reports are written. You write seven functions. `--check` runs 15 tests, and all fail until you write them.
- The week 3 interactive (`examples/w03-lag-tolerant-movement-check.html`) for spot checks.

This lab is about defending a server. You write validation and detection code only. No part of it involves building or running a cheat against a real game.

## Steps

### Part A: the two checks (35 min)

1. Implement `rate_allowed` and `credit_allowed`. Explain in one sentence why `credit_allowed` must use server times only.
2. Implement `min_setting`. Run `python movement_validator.py --table` and confirm it matches the lecture's section 2 table.
3. Check the 100 ms row by hand for both checks, following the lecture's worked 250 ms check. State which server tick sees the bunched packets and how many steps they carry.
4. Change `LATENCY_MS` to 45 and rerun `--table`. Explain why nothing changes, then put it back.

### Part B: gravity (30 min)

5. Implement `gravity_violations` with its two rules. The four gravity tests must pass: an honest jump, a 20 m fall off a cliff, a fly hack that climbs 0.2 m per tick, and a hover hack that descends 0.02 m per tick.
6. Find one honest movement your rules would wrongly flag (think of jump pads, ladders or water). Write it as a height sequence, show that it fails, and propose the smallest server-side change that fixes it without letting the hover hack through.

### Part C: detection (40 min)

7. Implement `violations`, `flag_stats` and `best_k`. Run `--check` until it prints `all checks passed`.
8. Run `python movement_validator.py --tune --L 250 --precision 0.9`. Report the chosen `k`, precision and recall for the 1-day and 7-day windows. Compare the 1-day `k = 3` row with the lecture's Poisson prediction for the same rule and explain any difference in one or two sentences (the log has a different cheater share and a finite sample).
9. Repeat with `L = 150` and `L = 400`. For each, give the largest jump the credit check allows and the best 7-day `k` at 99% precision. Make a small table with `L`, largest jump, honest violations per player-day, best `k`, and recall.
10. Find the largest `L` at which blinks still count as violations. What happens to recall above it, and why is that a design limit rather than a tuning problem?

### Part D: policy memo (at home)

11. Write a one-page ban policy for an invented PvP MMO using your numbers. Say what the server does at once (prevention), when accounts are flagged, when they are banned, and what happens to a flagged account in between. Name your `L`, `k` and window, and state the expected innocent bans per 10,000 players per week.

## Deliverable

Your finished `movement_validator.py` and one Markdown or PDF file with the step 1 sentence, the step 3 hand check, the step 4 explanation, the step 6 sequence and fix, the outputs and table from steps 8 and 9, the step 10 answer and the Part D memo. Submit before the week 4 lecture.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Distance checks (Part A) | Checks pass; table reproduced; hand check names the tick and step count; latency experiment explained | Passes, explanations thin | Fails the check | 20 |
| Gravity (Part B) | Four tests pass; a real false positive found and fixed without reopening the hover hack | Tests pass, false positive vague or the fix reopens a hack | Missing | 20 |
| Detection (Part C) | All checks pass; step 8 comparison explained; step 9 table complete; step 10 limit found and explained | Most numbers present, interpretation weak | Missing or fails | 30 |
| Ban policy (Part D) | Uses the pair's own numbers; separates prevention from detection; states innocent bans per week | Plausible policy with few numbers | Missing | 20 |
| Code quality | Readable, runs first time, no changes to the seeded generator | Runs with small fixes | Does not run | 10 |
| **Total** | | | | **100** |
