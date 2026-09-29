# MMO306 · Lab 11: The event clock

**Week:** 11 ([lecture](../lectures/w11-events-and-world-bosses.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** encounter designs (40%). The boss scaling and calendar from Part C go into your encounter design document.

## Objective

Implement the reach and crowd model, test it against a session simulation, find where its uniform-day assumption breaks, and plan the event calendar for one zone at launch and a year later.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`event_schedule.py`](lab11-starter/event_schedule.py), a skeleton with six functions to write: `reach`, `crowd`, `n_crit`, `kill_time`, `load_hourly_weights` and `simulate`. The `simulate` docstring states the exact rules.
- [`online_by_hour.csv`](lab11-starter/online_by_hour.csv), an invented but typical share of session starts by hour of day, peaking at 20:00.
- [`test_event_schedule.py`](lab11-starter/test_event_schedule.py), eight tests using the lecture's numbers. All fail on the starter.
- The [interactive](../examples/w11-event-clock.html) for spot checks.

## Steps

### Part A: formulas and simulation (40 min)

1. Implement `reach`, `crowd`, `n_crit` and `kill_time`. Running `python event_schedule.py` must print the lecture's table.
2. Implement `simulate` for uniform session starts. Run the tests. Then compare simulation and formula for `T` = 30, 60, 105, 180 and 360 with `N = 3,000`, `S = 90`, `W = 15`. Report both in one table.
3. The formulas assume one session per player per day. Change the simulation so 30% of players play two sessions a day (same `S`, independent start times, still one reward per day). Which of reach and crowd changes, and by how much at `T = 360`? Explain in two sentences.

### Part B: prime time (35 min)

4. Implement `load_hourly_weights` and the weighted branch of `simulate`. Run all tests.
5. With the hourly weights, `N = 3,000`, `S = 90`, `W = 15`, run `T` = 120, 240 and 360. For each, list the crowd at every start time of day. Mark which occurrences fall below `n_min = 60`.
6. Find a timetable (a list of start times, not necessarily evenly spaced) of at most six occurrences a day in which every occurrence gets at least 60 players on average. You'll need to change `simulate` to accept a list of start times. Report the timetable, the crowds and the day's reach.

### Part C: plan a zone (45 min)

7. Your zone launches with `N = 5,000` interested daily players, falling to 40% a year later. Median session is 75 minutes.
8. Design two world bosses and one hourly event. For each boss give `W`, `T` or a timetable, `n_min`, and a health rule `H(n) = H0 + h n` with kill time between 2 and 4 minutes from `n_min` up to three times the expected crowd (use `d = 400`). Show the kill times.
9. Check the plan at launch and at 40% population, using the hourly weights. Report every occurrence that falls below its `n_min` and change the plan until none does. Name the lever you used for each change (scaling, window, timetable, merging copies).
10. Draw the zone's day as a clock strip with one row per event.

## Deliverable

- The completed `event_schedule.py` with all tests passing, plus your changed simulation for steps 3 and 6.
- A report of at most 3 pages: the step 2 table, the step 3 explanation, the step 5 and 6 results, and the zone plan with the clock strip, kill-time table and the launch and year-two check.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and simulation (Part A) | Tests pass; formula and simulation agree within noise; two-session change explained correctly | Tests pass, explanation missing or wrong | Tests fail | 30 |
| Prime-time analysis (Part B) | Crowds by start time reported; a six-occurrence timetable meets 60 everywhere | Analysis done, timetable misses the target at one occurrence | Missing | 25 |
| Zone plan (Part C, steps 8-9) | Both bosses and the hourly event meet their `n_min` at launch and year two; kill times in band; levers named | Plan works at launch only, or kill times out of band | Missing | 30 |
| Clock strip and clarity | Readable strip, all numbers traceable to code | Strip present, some numbers unexplained | Missing | 15 |
| **Total** | | | | **100** |
