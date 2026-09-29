# PR301 Lab 13: Beta plan, go/no-go sheet and run sheet

**Week:** 13 (Beta: open class playtest). **Guide:** [week 13](../lectures/w13-beta-open-class-playtest.md). **Team lab**, submitted once per team.

## Objective

Plan the beta so that 50 humans online at your event is likely rather than hoped for, and so that the server has measured headroom above that number with every system switched on. Then run the peak hour from a written sheet. The checker recomputes your invitation target from your alpha logs and your capacity from your load test.

## Starter materials

In [`labs/lab13-starter/`](lab13-starter/):

- `check_beta.py`. Standard library only. Run it with `.venv/bin/python check_beta.py turnout.csv loadtest.csv`. It prints the alpha show rate `s` and event attendance `e` with their Wilson intervals, the event share `a = e + (1 − e) × LP`, the invitations needed for your goal in four cases (alpha or low-end `s`, alpha or planned `e`), the modelled chance of reaching the target with your planned invitations, the mean tick at the 100-player load-test crowd, capacity (where p99 crosses 80 ms) and headroom. It prints `PASS` or `NOT READY` and exits with code 1 on any problem.
- `turnout.csv`. The *Saltmarsh* alpha numbers and beta plan from the guide, with `e_assumption` blank.
- `loadtest.csv`. The *Saltmarsh* first beta load test, before the area-of-interest fix.

## Steps

### Part A: invitation plan

1. **Warm-up (10 minutes).** Run the checker on the starter files. It fails twice. Fill `e_assumption` with the levers the *Saltmarsh* team used, then replace the 50, 75 and 100 rows with the retest from the guide (mean 20, 32 and 44 ms; p99 36, 58 and 76 ms). It should pass with capacity "at least 100".
2. Replace the alpha figures in `turnout.csv` with your own from the week 10 report: sign-ups (`alpha_invited`), players who logged in at least once, players who attended the event, and the evening share `LP`.
3. Choose your planned event attendance `e`. If it is above the alpha value, name the lever that justifies it (a clash-free rota slot, a reward, reminders) in `e_assumption`.
4. Set `planned_invitations` so the checker passes at the low end of the show rate. In `beta-plan.md`, write the recruitment plan, which shared sign-up you use so testers are not double-booked, and a trigger date and number (as the *Saltmarsh* team did with "85 confirmed two days before").

### Part B: load test

5. Run a stepped bot load test on the beta build, with chat, parties and the encounter instance count from week 12 active. Hold each step for ten minutes after warm-up. Record mean and p99 tick from the per-tick log in `loadtest.csv`.
6. Step to 100 players. If the checker reports a mean above 60 ms at 100, or headroom below 2 (p99 crossing 80 ms before 100 players), profile, fix and retest. Record the fix in `beta-plan.md`.

### Part C: go/no-go and run sheet

7. Copy the template below into `run-sheet.md` and fill it in before the session.
8. Thirty minutes before your peak hour, the lead reads the go/no-go list aloud and signs it with the time.
9. During the peak hour, the operator records the restart drill values in the table.

```markdown
## Roles
Lead: ___  Operator: ___  Comms: ___  Observers: ___

## Go/no-go (answer yes, no, or accepted with a reason)
1. Load test at 100 bots on this build; mean and p99 at 100 within the week 6 rule:
2. Dashboard shows humans and bots separately, p99 tick, disconnects, errors, ledger residual:
3. World database backup in the last hour; restore tested this week:
4. Restart drill time, five check characters, one guild, and one change made seconds before the save:
5. Roles named:
6. Confirmed sign-ups against the trigger; reminders sent:
7. Open S1 bugs; kill switches tested on this build:
Decision (go / no-go), time, lead's name:

## Timeline
Doors open: ___  Event: ___  Restart drill: ___  Close: ___

## Restart drill
| Check | Before | After | Match? |
|---|---|---|---|
Restart duration:
```

## Deliverable

In `production/week13/` in the team repository:

- `turnout.csv` and `loadtest.csv` that pass `check_beta.py`, with the output saved as `check-output.txt`.
- `beta-plan.md` (recruitment plan, trigger, any load-test fix) and `run-sheet.md` (signed go/no-go, timeline, restart drill table).
- The peak-hour export of player count (humans and bots separately) and p99 tick, as the guide's deliverables describe.

**Checkable output:** the instructor reruns `check_beta.py`, which must print `PASS` and exit with code 0, then reads the humans-only peak from your exported metrics.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; output file matches |
| Turnout inputs | 3 | Taken from the alpha server logs; any raised event attendance justified by a named lever |
| Load test | 4 | Beta build with chat, parties and encounter instances; steps held; p99 recorded; stepped to 100 |
| Go/no-go | 3 | Completed and signed before the peak hour; every line answered |
| Restart drill | 3 | Before-and-after values recorded, including one change made seconds before the save |
| Peak evidence | 3 | Humans-only peak marked in the server export, or an honest shortfall report with recomputed `s` and `e` |
