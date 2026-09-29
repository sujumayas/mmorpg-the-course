# PR301 Lab 12: Encounter numbers, pull log and the day-3 burn-down

**Week:** 12 (Sprint 5: group encounter). **Guide:** [week 12](../lectures/w12-sprint-5-group-encounter.md). **Team lab**, submitted once per team.

## Objective

Run sprint 5 with three records the instructor can check: encounter numbers set from your simulator, a pull log in which every pull tests a stated question, and a burn-down log with a day-3 projection and a cut at least as large as the slower projection says. The checker recomputes all three.

## Starter materials

In [`labs/lab12-starter/`](lab12-starter/):

- `check_burndown.py`. Standard library only. Run it with `.venv/bin/python check_burndown.py backlog.csv burndown.csv encounter.csv pulls.csv`. It prints both projections, the cut needed and the cut made, the encounter's kill time, enrage margin and `D_min`, then `PASS` or `NOT READY`. It exits with code 1 on any problem.
- `backlog.csv`. The *Saltmarsh* sprint 5 backlog from the guide. `planned` marks items in the day-0 plan, committed and stretch alike (the burn-down tracks both); `minimum` marks the items the encounter cannot ship without. Statuses are `done`, `remaining` and `cut`. A replacement item that brings hours back, such as the round-robin loot rule, gets a note starting `replaces`.
- `burndown.csv`. Remaining estimated hours and added scope per day, filled to day 3.
- `encounter.csv`. The Drowned Warden's numbers, with `D_min` blank.
- `pulls.csv`. Two pulls, one missing its question.

## Steps

### Part A: plan (in the studio session)

1. **Warm-up (15 minutes).** Make the starter files pass: cut the three non-minimum items the guide cuts, mark the round-robin rule as `remaining` with a `replaces` note, fill in `D_min` and give pull 2 a question. The checker should report a cut of 6.5 against 6.0 needed.
2. **Your sprint 5 backlog.** Replace `backlog.csv` with your own, committed by the week 11 capacity rule. Mark every item `minimum` yes or no now, before any work starts. The five requirements in section 1 of the guide are minimum by definition.

### Part B: numbers

3. Run your combat simulator on a light party at the encounter's level. Enter `D`, your estimate of `u`, the target kill time, `H`, the enrage time and `D_min` in `encounter.csv`. Save the simulator output as `sim-run.txt`.
4. Write one sentence of design statement in `encounter-notes.md`: "a party at X% of simulated DPS beats the enrage".

### Part C: pulls

5. Book two pull sessions. Compute your pull budget as in the guide and write it in `encounter-notes.md`.
6. Before each pull, write its question in `pulls.csv`. After it, fill outcome and deaths by ability from the encounter telemetry, not from memory.
7. Include at least one pull that tests the leash, one with a planned disconnect, and one where the party wipes on purpose to test the reset.

### Part D: day 3

8. Update `burndown.csv` at the end of every day, including added scope.
9. On day 3, run the checker. If it asks for a cut, make it from non-minimum items and record it in `backlog.csv`. Write the decision, who made it and the margin left in `encounter-notes.md`.
10. Fill days 4 and 5 as the sprint ends. The checker only uses days 0 to 3, but the review compares your projection with what happened.

## Deliverable

In `production/week12/` in the team repository:

- `backlog.csv`, `burndown.csv`, `encounter.csv` and `pulls.csv` that pass `check_burndown.py`, with the output saved as `check-output.txt`.
- `sim-run.txt` and `encounter-notes.md` (design statement, pull budget, day-3 decision, and one paragraph comparing the day-3 projection with the day-5 result).

**Checkable output:** the instructor reruns `check_burndown.py` on your four CSV files. It must print `PASS` and exit with code 0. Two pulls are then checked against the encounter telemetry.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; output file matches |
| Minimum marked at planning | 3 | Every item marked before work started; cut items were non-minimum |
| Encounter numbers | 4 | From a saved simulator run; design statement as a percentage of simulated DPS |
| Pull log | 4 | Every pull has a question; leash, disconnect and reset pulls present; outcomes match telemetry |
| Day-3 decision | 3 | Both projections computed; cut made on day 3 with its margin written down |
| Projection review | 2 | Day-3 projection compared honestly with the day-5 result |
