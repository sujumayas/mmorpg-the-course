# PR201 Lab 13: Beta exit criteria and soak plan

**Week:** 13 (Beta milestone). **Guide:** [week 13](../lectures/w13-beta-milestone.md). **Team lab**, submitted once per team.

## Objective

Show, with evidence, that your beta build meets the course's exit criteria, and plan a soak test long enough to support a stated reliability target for the showcase. The output is an evidence sheet the instructor can spot-check and a soak log that a script turns into `PASS`, `ON TRACK` or `NOT READY`.

## Starter materials

In [`labs/lab13-starter/`](lab13-starter/):

- `soak_target.py`. Standard library only. Run `.venv/bin/python soak_target.py soak_plan.csv soak_log.csv`. It computes `λ_max` and the hours needed from your target, sums the logged hours and crashes on the current build only, and prints `PASS`, `ON TRACK` (with the hours still to run) or `NOT READY`. It exits with code 1 on `NOT READY`.
- `soak_plan.csv`. Keys `S` (showcase server-hours), `R` (target), `R_set_on` (ISO date), `build_tag`, `booked_hours` (overnight hours you have booked machines for, before week 15). Three are blank.
- `soak_log.csv`. One row per soak run: date, build tag, hours, crashes, bot route version, note. The starter holds Tuesday's one-hour team playtest with no route version.

## Steps

### Part A: exit criteria sheet (before the review)

1. Copy the criteria table from guide section 2 into `exit-criteria.md`. Add at least two criteria specific to your slice (for example "the boss resets after a party wipe for every party size from 1 to 3").
2. For each criterion, fill the evidence column with a link or file path in the repository, taken from the tagged beta build. Mark any criterion without evidence as `OPEN` with a dated plan.
3. Commit the sheet before the week 13 meeting. The commit time is checked.

### Part B: soak plan (in class)

4. **Warm-up.** Run the script on the starter files and read the three failures. Then set `R = 0.9`, a `R_set_on` date before the log's date, and `booked_hours = 0`. Run it again. Explain in one sentence in `soak.md` why a clean one-hour playtest leaves you `NOT READY`, citing the worst-case probability from the guide's table.
5. **Your target.** Set `S` from your showcase schedule and choose `R`. Record the date. If you choose below 0.9, write in `soak.md` how you will recover from a crash during the showcase (who restarts the server, how long it takes, what the party does meanwhile) and rehearse it once.
6. **Bot route.** Write `route.md`: the scripted actions of your bot clients, as a list, with each system the showcase uses (movement, party join, combat, abilities, revive, boss, loot, disconnect and reconnect) marked covered or not. For every system not covered, name the human test that covers it instead. Give the route a version (`r1`, `r2`, ...).
7. **Book nights.** Work out the server-hours per night your machines can run and book enough nights before week 15. Enter the total in `booked_hours`.
8. **Log every run** in `soak_log.csv`, with the build tag and route version. A crash on the current build is logged with its crash count and a tracker ticket in the note.
9. **After a fix.** If you fix a crash, tag a new build, change `build_tag` in the plan and start the count again, as guide section 3 explains.

## Deliverable

In `production/week13/`: `exit-criteria.md` (committed before the review), `soak_plan.csv`, `soak_log.csv`, `route.md`, `soak.md`, and the script output as `soak-output.txt`.

**Checkable output:** the instructor reruns `soak_target.py` at the week 14 meeting. It must print `PASS` or `ON TRACK`. At the week 15 showcase it must print `PASS`, or the team must show the rehearsed recovery plan from step 5.

## Rubric (25 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Exit criteria sheet | 7 | All course criteria plus two slice-specific ones; evidence from the beta build; committed before the review |
| Target and model | 4 | `R` and `S` justified; set before the first soak on the build; warm-up sentence uses the model correctly |
| Bot route | 5 | Every showcase system listed; uncovered systems have a named human test; route versioned |
| Soak log | 5 | Every run logged with build and route; crashes ticketed; count restarted after fixes |
| Script status | 4 | `ON TRACK` at week 14 and `PASS` at week 15, or a rehearsed recovery plan for a lower target |
