# PR201 Lab 10: Alpha gate sheet and gate-bug forecast

**Week:** 10 (Alpha milestone). **Guide:** [week 10](../lectures/w10-alpha-milestone.md). **Team lab**, submitted once per team.

## Objective

Arrive at the alpha review knowing whether you pass. You will triage your open bugs with the PR101 priority matrix, count the gate bugs, forecast on Monday whether they reach zero by the review day, test that forecast against a cut and against worse capacity or regressions, and fill the seven alpha criteria with owners and evidence. The checker recomputes priorities, the gate count and the forecast, and flags a criteria sheet that claims more than the evidence shows.

## Starter materials

In [`lab10-starter/`](lab10-starter/):

- `check_alpha.py`. Standard library only. Run `python check_alpha.py bugs.csv forecast.csv criteria.csv`. It prints every bug with its matrix priority, the gate-bug count, the day-by-day forecast and a forecast verdict, then `PASS` or `NOT READY`. `--cut FEATURE` drops the open bugs tagged with that feature, as a cut behind a flag would, and `--f0-after-cut N` sets the find rate after the cut. It exits with code 1 when the sheet is inconsistent.
- `bugs.csv`. The twelve *Hollowmarch* bugs from the guide with priorities blank. Columns: `id`, `summary`, `severity` (1 to 4), `frequency` (`always`, `often`, `rare`), `priority` (1 to 4), `status` (`open`, `fixed`, `verified`, `closed`, `cut`), `owner`, `feature`.
- `forecast.csv`. The forecast inputs from the guide: `f0`, `d`, `c`, `r` and `review_day`.
- `criteria.csv`. Criteria A1 to A7 with owner, evidence and status blank.

`PASS` means the sheet is consistent. The priorities match the matrix, every gate bug and criterion has an owner, and A4 is not marked pass while gate bugs are open. The forecast verdict is printed on its own line. A consistent sheet can still forecast a failed gate, and the team must act on it.

## Steps

1. **Warm-up (10 minutes).** Fill the priorities in the starter `bugs.csv` by hand and run `python check_alpha.py bugs.csv forecast.csv`. When the priorities match, compare the forecast with the guide's table (4 open on day 5, zero on day 7). Then run with `--cut ranged --f0-after-cut 3` and confirm zero on day 4. Finally set `c` to 3, then `r` to 0.4, and record what happens on day 5.
2. **Monday triage.** Export your tracker in the same columns. Set severity and frequency from evidence (the week 7 and alpha playtests, the network matrix). Compute priorities and run the checker.
3. **Your inputs.** Estimate `f0` and `d` from the bugs found per day in the last week of sprint 3, `r` from the share of sprint 3 fixes that were reopened or caused a new bug, and `c` from bugs closed per day in sprint 3 divided by the share of hours spent on bugs. Write each estimate and its source in `alpha.md`, and name the input you trust least.
4. **Decide on Monday.** If the forecast fails, choose among more capacity, a cut behind a flag (tag the bugs with the feature and use `--cut`), or asking to move the review. Record the choice and the numbers that support it. A cut of the pitch's central verb needs the instructor's agreement.
5. **Track the week.** Each evening, record the real count of open gate bugs next to the forecast in `alpha.md`. On Wednesday evening, compare with the forecast and act if you are behind.
6. **Criteria sheet.** Fill `criteria.csv` with an owner, evidence (a link, a log, a query result or a video) and pass or fail for A1 to A7. Run the full checker until it prints `PASS`.
7. **Alpha playtest plan.** Write the questions, units, tracked events and thresholds for the sessions before week 11, dated today, as deliverable 6 in the guide describes.

## Deliverable

In `production/week10/` in the team repository:

- `bugs.csv`, `forecast.csv` and `criteria.csv` that pass `check_alpha.py`, with the command and output saved as `check-output.txt` (include `--cut` if you cut a feature).
- `alpha.md` with the inputs and their sources, the Monday decision, the daily forecast-versus-actual table, the network matrix summary and the placeholder list.
- `alpha-playtest-plan.md`, dated before the first session.

**Checkable output:** the instructor reruns `check_alpha.py` with the command in `check-output.txt`. It must print `PASS` and exit with code 0, and the gate-bug count must match the tracker on the review day.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; gate count matches the tracker at the review |
| Triage quality | 4 | Severity and frequency come from evidence; no bug is inflated or deflated to reach the gate |
| Forecast inputs | 3 | Each input justified from sprint 3 data; least-trusted input named; the warm-up sensitivity runs recorded |
| Monday decision | 3 | Decision made on Monday, follows from the forecast, and its cost is stated |
| Daily tracking | 3 | Forecast and actual counts side by side for every day; Wednesday checkpoint acted on |
| Criteria and playtest plan | 3 | Every criterion has owner and checkable evidence; playtest plan has questions, units, events and dated thresholds |

<details>
<summary>Instructor notes</summary>

- Warm-up priorities: B-31 P2, B-32 P1, B-33 P1, B-34 P2, B-35 P2, B-36 P2, B-37 P2, B-38 P2, B-39 P1, B-40 P3, B-41 P4, B-42 P3. Nine gate bugs.
- Sensitivity runs: `c = 3` leaves 9 open on day 5; `r = 0.4` leaves 8.
- Teams sometimes downgrade severities on Thursday to pass A4. Compare Monday's export with Friday's for any bug whose severity or frequency changed without a note.

</details>
