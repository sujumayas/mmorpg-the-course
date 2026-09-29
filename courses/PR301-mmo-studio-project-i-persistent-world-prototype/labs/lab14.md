# PR301 Lab 14: Triage table, fix budget and release candidate record

**Week:** 14 (Stabilization). **Guide:** [week 14](../lectures/w14-stabilization.md). **Team lab**, submitted once per team.

## Objective

Decide what happens to every must-fix bug from the beta, using the week 8 persistent-world severity scale, and show that the fix demand fits the hours the team has. Then record the release candidate's checks. The checker enforces the triage rules and recomputes demand and capacity from your tracker history.

## Starter materials

In [`labs/lab14-starter/`](lab14-starter/):

- `check_stabilization.py`. Standard library only. Run it with `.venv/bin/python check_stabilization.py bugs.csv params.csv`. It counts decisions, computes the reopen rate, effective demand, capacity and margin, then prints `PASS` or `NOT READY` and exits with code 1 on any problem.
- `bugs.csv`. The *Saltmarsh* S1 and S2 bugs from the guide, all marked `fix`.
- `params.csv`. The *Saltmarsh* tracker history and hours.

Decisions are `fix`, `disable` (with the name of the week 8 kill switch in `flag`; bugs behind the same switch pay the half-hour re-check once) and `reclassify` (with `new_severity` S3 or S4 and `evidence`). The checker refuses to reclassify any S1, and any bug with `data_loss` or `crash` set to `yes`. An S1 must have `data_loss` or `crash` set to `yes`.

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files. It reports a 21.6-hour gap. Apply options A and B from the guide: disable the five market bugs behind the `market_enabled` switch, and reclassify the three north reed beds bugs to S3 with their telemetry evidence. The checker should pass with a margin of 9.7 hours. Then try to reclassify B108 and read the error.
2. **Your parameters.** Replace `params.csv` from your tracker: mean hours to fix S1 and S2 bugs in sprints 1 to 5, reopened and closed fix counts, the number of new must-fix bugs your internal testing found in sprint 5 and their mean hours, and your team's real hours for week 14 and the two days of week 15. Itemize the reserved hours in `budget-notes.md`.
3. **Triage.** Replace `bugs.csv` with every S1 and S2 from the beta. Apply the week 8 scale as section 2 of the guide describes. Put the beta frequency (sessions or players affected, from the telemetry export) in `evidence` for every S2.
4. **Decide.** Mark every bug `fix`, `disable` or `reclassify`. Only switch off a system whose week 8 kill switch exists and was tested. For each one, confirm in `budget-notes.md` that the world still meets the course brief without it, and write its showcase note.
5. **Run the checker** until it prints `PASS`. If your margin is under 10% of capacity, name the next switch-off candidate in `budget-notes.md`.
6. **Daily count.** Record the open must-fix count at the end of each working day until the release candidate, in `mustfix-daily.csv` with columns `date,open,found_today`.
7. **Release candidate record.** Copy the template below into `rc-record.md` and fill it in for the candidate you tag.

```markdown
## Release candidate
Version and tag: ___   Commit: ___   Changelog link: ___

## PR101 week 13 checklist
Completed by: ___   Items failed and fixed: ___

## Clean install
Tester (did not build it): ___   Machine: ___   Result: ___

## Backup and restore
Backup taken at: ___   Restored into: ___   Restore time: ___
| Character | Level | Gold | Item count | Guild | Matches? |
|---|---|---|---|---|---|

## Soak test (2 h, 50 bots)
Memory at start / end: ___   p99 tick at start / end: ___   Graph files: ___
```

## Deliverable

In `production/week14/` in the team repository:

- `bugs.csv` and `params.csv` that pass `check_stabilization.py`, with the output saved as `check-output.txt`.
- `budget-notes.md` (reserved hours, brief check and showcase note for each switched-off system, next switch-off candidate if needed), `mustfix-daily.csv` and `rc-record.md`.

**Checkable output:** the instructor reruns `check_stabilization.py`, which must print `PASS` and exit with code 0. Two severities are traced to beta evidence, and the release candidate is installed from its artifact.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; output file matches |
| Triage | 4 | Week 8 scale applied; every S2 has beta frequency; no data or crash bug reclassified |
| Parameters | 3 | Taken from tracker history; reserved hours itemized |
| Switch-offs | 3 | Each kill switch re-checked on the candidate, checked against the brief, with a showcase note and its bugs left open on main |
| Daily count | 2 | Recorded every working day, including bugs found during the week |
| Release candidate | 4 | Checklist, clean install, restore with three characters and a two-hour soak all recorded |
