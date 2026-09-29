# PR201 Lab 09: Release burn-up, forecast range and cut list

**Week:** 9 (Sprint 3 review). **Guide:** [week 9](../lectures/w09-sprint-3-review.md). **Team lab**, submitted once per team.

## Objective

Forecast the rest of the project from three sprints of evidence and cut the scope to fit, at this review, while the cut is still a choice. You will draw the release burn-up, compute the velocity range and the scope growth rate, fill the four-scenario table, choose a planning scenario, and write an ordered cut list with a pre-agreed next cut. The script recomputes the table and checks that your cuts close the gap without removing anything a kept story needs.

## Starter materials

In [`lab09-starter/`](lab09-starter/):

- `burnup_forecast.py`. Standard library only. Run `python burnup_forecast.py history.csv --sprints-left 2 --plan mean --cuts cuts.csv`. It prints the range, the done-line-only forecast the team would have made at each review, the scenario table and the cut check, then `PASS` or `NOT READY`. It exits with code 1 when the cuts fall short or cut a dependency.
- `history.csv`. The *Hollowmarch* board history from the guide. Row 0 is the week 3 plan (scope only), restated after the cuts of weeks 5, 6 and 8 as in the guide's table: 311 − 94 = 217. Units are estimated hours.
- `cuts.csv`. The team's cut list, bottom of the backlog first, with only three stories marked. The last row is a kept story that a polish item needs. Columns: `id`, `story`, `estimate_h`, `when` (`now`, `next` or blank for kept), `player_loses`, `needed_by` (ids of kept stories that depend on this one; must be empty for any cut story).

## Steps

1. **Warm-up (10 minutes).** Run the script with the starter files. The cuts fall short. Mark enough stories `now` to reach the typical-with-freeze cut (52 hours) and one story `next` so that `now` plus `next` covers the bad-sprint case with a freeze. Run it until it prints `PASS`. Compare the scenario table with the guide.
2. **Your history.** Start row 0 from your week 2 scope sheet minus every cut you have made since, with a dated table of those cuts in `forecast.md` (the guide's section 4 shows the form). Then export your board's end-of-sprint totals for weeks 3 to 9: estimated hours done in each sprint and total backlog size at each sprint end, including everything added since the TDD. If your board cannot show past scope, rebuild it from the dates stories were created, and say so in `forecast.md`.
3. **Your burn-up.** Plot the done and scope lines by sprint in any tool. Extend them forward at `v_min`, `v_mean`, `v_max` and `g`, and mark the beta sprint. Save the chart as `burnup.png`.
4. **Your scenario.** Run the script with your real `--sprints-left`. Choose the planning scenario (`--plan`) and write one sentence explaining the choice. Note the done-line-only forecasts the script prints, and say in one sentence whether your team made those forecasts at the time.
5. **Your cut list.** Order the backlog from the bottom. For each story, write what the player loses and which kept stories need it. Mark `now` cuts until the chosen scenario's cut is covered, and a `next` cut with a numeric trigger (for example, "sprint 4 velocity at or below v_min"). Nothing on the login-to-boss path may be cut.
6. **Freeze.** Write the feature freeze date and the one-in-one-out rule into your team agreement.
7. **Run the script** until it prints `PASS`.

## Deliverable

In `production/week09/` in the team repository:

- `history.csv` and `cuts.csv` that pass `burnup_forecast.py` with your stated `--sprints-left` and `--plan`, with the command and output saved as `check-output.txt`.
- `burnup.png`, the release burn-up with projections and the beta line.
- `forecast.md` with the chosen scenario and reason, the next-cut trigger, the freeze date, and the sprint 3 review record (goal met yes or no, velocity, backlog changes).

**Checkable output:** the instructor reruns `burnup_forecast.py` with the command in `check-output.txt`. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Script passes | 4 | `PASS` on rerun with the stated options |
| Honest history | 4 | Done and scope values match the board; row 0 traces to the week 2 sheet through dated cuts; added work since week 3 is counted in scope |
| Burn-up chart | 3 | Both lines, the forward projections and the beta line are shown and labeled |
| Scenario choice | 3 | Chosen deliberately with a reason; the team's own earlier done-line-only forecasts are discussed |
| Cut list quality | 4 | Cuts are leaves, not links; "player loses" is specific; the login-to-boss path is intact; next cut has a numeric trigger |
| Freeze | 2 | Date and one-in-one-out rule recorded in the team agreement |

<details>
<summary>Instructor notes</summary>

- Warm-up: the starter prints `g 15.0` and cuts of 44, 52, 82 and 92. Marking K1 to K7 `now` gives 52 hours (at least 52); K8 `next` brings the total to 62, which covers `136 − 2 × 37 = 62`. K9 stays kept: marking it cut prints a dependency failure, because the revive prompt in sprint 4 needs it.
- If a team's row 0 does not trace to its week 2 sheet, ask for the cut table before marking the history row.
- A team with `v_mean ≤ g` has a burn-up that never meets. The script prints "never" in the finish column. Make that team freeze today.
- Watch for teams that shrink estimates of remaining stories instead of cutting. Compare the scope column with last week's export.

</details>
