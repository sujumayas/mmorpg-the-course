# PR402 Lab 04: Alpha triage sheet

**Week:** 4 (Alpha). **Guide:** [week 4](../lectures/w04-alpha-review-and-bug-triage.md). **Team lab**, submitted once per team.

## Objective

Turn the bugs found at your alpha review into a fix plan for the week before closed beta. You will estimate reach, mark gate bugs, rank the rest by impact per fix hour, fill your capacity and record the open impact. The checker confirms that gates are fixed, the plan fits and the order follows from the numbers.

## Starter materials

In [`labs/lab04-starter/`](lab04-starter/):

- `check_triage.py`. Standard library only. Run it with `.venv/bin/python check_triage.py bugs.csv --sessions 450 --capacity 31.5`. It prints every bug's impact and impact per hour, gates first, then the planned hours, the open impact and `PASS` or `NOT READY`. It exits with code 1 when a rule fails.
- `bugs.csv`. The nine Emberfall bugs from the guide, planned severity first. It fails the checker on purpose.

Decisions are `fix`, `workaround`, `defer` or `wontfix`. A workaround counts against capacity like a fix. Write `data loss` or `exploit` in the `gate` column where it applies. The checker adds S1 bugs with reach of 1% or more by itself.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file and read the failure. Change the decisions to the guide's second plan. The open impact should fall from 567.0 to 292.5 and the checker should print `PASS`.
2. **Merge and complete.** Put every bug from your alpha review into `bugs.csv`, one row per distinct bug. Merge duplicates and keep the report IDs in the summary. Each bug needs severity, a reach estimate and a fix estimate from the person who would fix it.
3. **Sessions and capacity.** Compute next week's sessions from your closed beta plan (testers times sessions each). Use your week 4 ops-tax hours from lab 01, less the hours of non-fix ops work (deploys, tester setup, FAQ), as capacity.
4. **Gates.** Mark data loss and value-path exploits. Check the S1s.
5. **Plan.** Set decisions until the checker passes. If you depart from the ranking for a reason the formula cannot see (a dependency, the only person who can fix it is away), write it in `note`.
6. **Reach telemetry.** For every open S2, add a telemetry event that will measure its real reach in closed beta. List the event names in `telemetry.md`.
7. **Go or no-go.** Before the closed beta starts, verify each gate fix on staging and record the decision in `go-no-go.md` with the open impact number.

## Deliverable

In `production/week04/` in the team repository:

- `bugs.csv` passing `check_triage.py` with your sessions and capacity, and the output saved as `check-output.txt`.
- `telemetry.md` listing the reach events.
- `go-no-go.md` with the decision, the date and the staging verification of each gate bug.

**Checkable output:** the instructor reruns `check_triage.py` with the sessions and capacity stated at the top of `check-output.txt`. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun with the stated inputs |
| Complete reports | 4 | Every bug has repro steps in the tracker, severity, reach and a fix estimate from its fixer; duplicates merged |
| Gates | 3 | Data loss and exploits marked correctly; every gate fixed and verified on staging |
| Reasoned order | 3 | Plan follows impact per hour, and every departure has a note that holds up |
| Reach telemetry | 3 | One event per open S2, named and placed in the build |
| Go or no-go | 3 | Decision recorded with date, open impact and evidence |
