# PR201 Lab 07: Multiplayer playtest plan and issue log

**Week:** 7 (Sprint 2 review and playtest). **Guide:** [week 7](../lectures/w07-sprint-2-review-and-playtest.md). **Team lab**, submitted once per team.

## Objective

Size your playtest slot before the session, run it with a shared issue log, and turn the log into prioritized bugs. You will compute how many matches the slot holds, how many first-time testers you observe, and the smallest problem frequency the slot can reach with 90% confidence. After the session you compute each issue's observed frequency and priority. The checker recomputes all of it and flags any claim or priority that does not follow from the numbers.

## Starter materials

In [`lab07-starter/`](lab07-starter/):

- `check_playtest.py`. Standard library only. Run `python check_playtest.py slot.csv issues.csv`. It prints the slot arithmetic, a small table of `P(seen)` for four frequencies, and every issue with its frequency and band. It prints `PASS` or `NOT READY` and exits with code 1 when anything disagrees. Blank claims are reported as blank, without the answer, so do the hand calculation first.
- `slot.csv`. The *Hollowmarch* slot from the guide (11 testers, 3 per match, 5 observers, 12-minute matches, 6 minutes of turnaround, 75 minutes) with the three claims left blank.
- `issues.csv`. Five issues from a sample log. `kind` is `match` for per-match problems and `first_time` for problems only a first-time tester can hit. `seen` is the tally of matches (or first-time testers) in which the issue appeared. `priority` is blank.

## Steps

1. **Warm-up (10 minutes).** Compute `claimed_matches`, `claimed_first_time` and `claimed_reach_p` for the starter slot by hand, using the formulas in guide section 4. Enter them. Then set a priority for each starter issue with PR101's matrix and the frequency bands from guide section 5. Run the checker until it prints `PASS`.
2. **Your slot.** Before class, replace the slot values with your real numbers: the testers you have been assigned, your match size, how many team members can observe (one must run the server), your match length measured in a practice run, and the window in the session plan. Enter your hand-computed claims.
3. **Reach statement.** Write one sentence in `report.md` in this form: "Per-match problems with frequency above X would have been seen with 90% confidence; first-time problems above Y." Compute Y yourself from `n_first` with the same formula.
4. **Network conditions.** Decide which rounds run under a CS202 week 14 profile, and write down how that changes `n` for each condition.
5. **Run the session.** Keep one shared issue log. Log what the tester did and what the game did, the round, the host machine and the network profile. Tally each issue once per match (or once per first-time tester).
6. **Enter the log.** Put every issue into `issues.csv` with severity, kind, tally and your priority. Run the checker until it prints `PASS`.
7. **Bugs and soak plan.** File every P1 and P2 as a bug report in your tracker (PR101 week 10 fields). For problems below your reach, write a soak test plan: which checks, which profile, how many scripted runs, and the frequency the soak run can reach.

## Deliverable

In `production/week07/` in the team repository:

- `slot.csv` and `issues.csv` that pass `check_playtest.py`, with the output saved as `check-output.txt`.
- `report.md` with the reach statement, the network plan, the survey summary (five to eight items, about the sprint goal), the list of P1 and P2 bugs with tracker ids, and the soak test plan.
- The sprint 2 review record: goal met (yes or no), estimated hours committed and done, and the backlog changes.

**Checkable output:** the instructor reruns `check_playtest.py` on your two CSV files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Slot plan | 3 | Inputs match the session as run; the waiting testers had a job; hosts rotated |
| Reach statement | 3 | Both per-match and first-time thresholds stated and correct |
| Issue log quality | 4 | Issues describe behavior, not guessed causes; network profile and host recorded; tallies per match |
| Bugs filed | 3 | Every P1 and P2 has a reproducible report with build number and conditions |
| Soak plan | 3 | Covers the rare problems the slot could not reach, with a run count justified by `1 − (1 − p)^n` |

<details>
<summary>Instructor notes</summary>

- Warm-up answers: 12 matches, 9 first-time testers, reach 0.175. Priorities: I1 P2 (S2 often), I2 P3 (S3 often, 4 of 9), I3 P1 (S2 always, 11 of 12), I4 P2 (S1 rare), I5 P3 (S4 always).
- I4 is the teaching case. One crash in 12 matches is "rare", so P2, and the slot cannot say how rare it is. It belongs in the soak plan.
- Teams often tally sightings instead of matches. Ask to see the raw log for one issue.

</details>
