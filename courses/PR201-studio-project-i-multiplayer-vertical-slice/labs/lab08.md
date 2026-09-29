# PR201 Lab 08: Content budget for sprint 3

**Week:** 8 (Sprint 3: content and progression). **Guide:** [week 8](../lectures/w08-sprint-3-content-and-progression.md). **Team lab**, submitted once per team.

## Objective

Make your content plan, your XP curve and your hours agree on one sheet before anyone builds a room. Every hour on the sheet is an estimated hour, the unit of weeks 4 to 6, and capacity is the forecast `f × U`. You will measure the real cost of one unit of content from sprint 2, compare its estimate ratio with the team's to get the content factor `k`, and check three balances: the content hands out enough XP to reach the target level, the session lasts about as long as planned, and the build hours fit the sprint. The checker computes all three and prints which hold.

## Starter materials

In [`lab08-starter/`](lab08-starter/):

- `check_content_budget.py`. Standard library only. Run `python check_content_budget.py unit_cost.csv curve.csv capacity.csv plan.csv`. It prints the focus, the forecast, the content ratio and `k`, the planned estimate-hours per item, and each balance as `holds` or `FAILS`, then `PASS` or `NOT READY`. It exits with code 1 when a balance fails.
- `unit_cost.csv`. The cost of the *Hollowmarch* sprint 2 room by step: estimate and actual hours.
- `curve.csv`. XP to the next level for levels 1 to 4 (so the target is level 5).
- `capacity.csv`. Estimated hours done and useful hours over sprints 1 and 2 (89 and 156, for the focus), sprint 3's useful hours (81), the team estimate ratio from week 5 (1.28), the bug reserve (5) and the system stories (10 for progression plus 5 for the thin bolt, 15), all in estimated hours, then XP per pack, target session minutes and the time tolerance.
- `plan.csv`. Plan A from the guide: the existing room, four new rooms, the boss room and the quest. Columns: `item`, `kind` (`existing`, `new`, `remix`, `boss`, `quest`), `estimate_h` (the raw estimate, before `k`), `packs`, `extra_xp`, `minutes`.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Time and hours fail. Change the plan and the curve to plan B from the guide (one new room, two remixes at 3.75 estimated hours each, the boss, and the last curve step lowered to 325). Run it until it prints `PASS`. Then try the other fix from the guide, pack XP of 62 with the original curve, and confirm it also passes.
2. **Your unit cost.** Replace `unit_cost.csv` with the step-by-step log of the room or area your team finished in sprint 2. If nobody logged hours, reconstruct them from commits and the board, and say so in `budget.md`.
3. **Your curve and rewards.** Enter your XP curve up to the level the sprint goal names, your XP per pack, and quest and boss rewards as `extra_xp`.
4. **Your capacity.** Enter your estimated hours done and useful hours for sprints 1 and 2, your useful hours for sprint 3 (available minus coordination, as in week 4) and your team estimate ratio from week 5. The checker computes the forecast `f × U`. Enter the bug reserve (at least the estimates of every open P1 and P2 from your week 7 playtest) and every system story at its raw estimate. Don't multiply anything by the ratio: `f` already carries it. List the system stories in `budget.md`.
5. **Your plan.** Enter every content item with its raw estimate. Run the checker. If a balance fails, pull one of the three levers (cut, remix, retune) and record which one and why. Repeat until `PASS`.
6. **Cut trigger.** Write, in `budget.md`, a dated cut trigger and the retune that goes with it, as in the guide. Show that the plan after the cut still passes: make a second `plan_cut.csv` (and `curve_cut.csv` if the curve changes) and run the checker on it.
7. **Progression criteria.** Copy the three progression rules from guide section 2 into the acceptance criteria of your XP and persistence stories.

## Deliverable

In `production/week08/` in the team repository:

- `unit_cost.csv`, `curve.csv`, `capacity.csv` and `plan.csv` that pass `check_content_budget.py`, with the output saved as `check-output.txt`.
- `plan_cut.csv` (and `curve_cut.csv` if needed) that also pass, with the output saved as `check-output-cut.txt`.
- `budget.md` with the system story list, the lever you pulled and why, the cut trigger with its date, and the progression acceptance criteria.

**Checkable output:** the instructor reruns `check_content_budget.py` on both sets of files. Both must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun for the plan and the post-cut plan |
| Measured unit cost | 4 | Unit cost comes from the real sprint 2 log, by step and discipline; `k = r_content / r_team` applied to every new content estimate |
| Honest capacity | 3 | Forecast from measured focus; bug reserve and every system story subtracted at their estimates; no hour on the sheet in actual hours |
| Lever and reasoning | 4 | Where a balance failed, the lever pulled is named and justified; retunes are recorded as slice decisions in the GDD |
| Cut trigger | 3 | Dated, specific, and the post-cut plan is checked |
| Progression criteria | 2 | Server-awarded XP with reason tags, one transaction per level-up, idempotent grants |

<details>
<summary>Instructor notes</summary>

- Starter plan A: `1.04 × 39 = 40.6` estimate-hours against a capacity of `46 − 5 − 15 = 26`, and 26 minutes. Warm-up plan B: `1.04 × 24 = 25.0` against 26; 22 minutes; 800 XP against 800 with the retuned curve. With pack XP 62 and the original curve: 816 against 815. The guide's cut plan (second remix removed, pack XP 75, last step 295): 21.1 estimate-hours, 18 minutes, 770 against 770.
- A team that multiplies estimates by its ratio and compares them with all useful hours has mixed units. Week 8 section 3 shows why that overstates capacity by about a third (63 against 46 estimate-hours).
- A team that passes by setting `bug_reserve_h` to zero after a playtest with open P1 bugs has not passed. Compare with their lab 07 bug list.
- Remix estimates should be justified. A remix at a tenth of a new room is suspicious.

</details>
