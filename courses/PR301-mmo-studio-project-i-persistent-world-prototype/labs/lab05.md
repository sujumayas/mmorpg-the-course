# PR301 Lab 05: Mob camp sizing and the camp faucet

**Week:** 5 (Sprint 2: combat and mobs). **Guide:** [week 5](../lectures/w05-sprint-2-combat-and-mobs.md). **Team lab**, submitted once per team.

## Objective

Size every mob camp in your starting area so that the alpha's peak crowd keeps utilization at or below 0.8, and put each camp's currency output into your economy sheet. You will derive time-to-kill from your combat numbers, choose a respawn rule, and show the checker passing at the crowd you expect.

## Starter materials

In [`labs/lab05-starter/`](lab05-starter/):

- `check_camps.py`. Standard library only. Run it with `.venv/bin/python check_camps.py camps.csv`. Options: `--target` (0.8), `--tmin` (20 seconds) and `--tmax` (90 seconds). For each camp and each player count it prints the respawn time used, demand, supply, utilization and idle share, flags rows above target, then prints `PASS` or `NOT READY`.
- `camps.csv`. The three Reedbank designs from the guide: fixed 90 seconds, fixed 30 seconds and dynamic. Columns: `camp`, `spawns`, `respawn_s`, `ttk_s`, `travel_s`, `players` (counts to test, separated by spaces), `dynamic` (`y` or `n`).

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file and reproduce the three tables in the guide. Keep only the dynamic row, set `spawns` to 18, and confirm `PASS`.
2. **Time to kill.** For each mob type in the starting area, compute `TTK` as effective HP over a starting character's effective DPS, using your MMO303 sheet. Record the inputs.
3. **Travel.** Walk the camp with a stopwatch in the current build, or estimate from the greybox distances and run speed. Record `travel_s`.
4. **Peak crowd.** Estimate the most players who will hunt at each camp during the alpha's busiest hour. Include that number and at least two smaller counts in `players`.
5. **Choose a rule.** Fixed or dynamic, and the spawn count. If you keep a fixed timer on purpose, say what the crowding is meant to do.
6. **Run until `PASS`.** Change spawns, timers or the number of camps, not the target.
7. **Faucet.** For each camp, compute currency per player-hour at the peak crowd as kills per player per minute times 60 times the average drop. Add it to the economy sheet.

## Deliverable

In `production/sprint2/`:

- `camps.csv` and the checker output saved as `camps-output.txt`.
- `camps-notes.md` with the `TTK` inputs, travel measurements, peak crowd estimates, the chosen rule with its intent, and the faucet line per camp.

**Checkable output:** the instructor reruns `check_camps.py` on your `camps.csv` with default options. It must print `PASS` and exit with code 0, with each camp's peak crowd in its `players` list.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun at default options; output file matches |
| `TTK` | 4 | Derived from the team's combat numbers with inputs shown |
| Peak crowd | 4 | Estimated per camp for the alpha's busiest hour, with reasoning |
| Rule and intent | 4 | Respawn rule chosen deliberately; the intended player behaviour is written in one or two sentences |
| Faucet | 4 | Currency per player-hour at peak for every camp, entered in the economy sheet |
