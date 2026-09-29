# PR301 review: open items

Items the course reviewer could not fix in place. Everything in `docs/handoff/notes-PR301.md` was fixed; see the reviewer's report.

## 1. Sprint calendar does not add up (w01, w03, w04, w07, w08, w11) — CLOSED

- **Resolution.** Each sprint runs two weeks, from one planning session to the next. Reviews open weeks 5, 7 and 9, and the week 4, 6 and 8 sessions are mid-sprint sessions that keep their topics. Updated: w01 section 1, the w03 to w09 session plans and deliverables, w11, labs 03, 04, 06, 07 and 08, the m1 table, the m3 "Reviewed" line and the exam bank. The w04 example now has the login fix miss the tagged review build, so sprint 1's focus factor stays 0.46.

Original finding:

- **Problem.** w01 says three two-week sprints each open with a planning session (weeks 3, 5, 7) and close with a review session (weeks 4, 6, 8). w08 puts sessions on Tuesdays. Planning on Tuesday of week 3 and reviewing on Tuesday of week 4 is one week of work, but w03, w04 and w07 plan two weeks of capacity (13 available hours per person, 91 per team).
- **Proposed fix.** State in w01 section 1 that each sprint runs from its planning session to the planning session two weeks later, and that the review session sits at the sprint's end. Concretely, move the review into the first half of the next planning session (weeks 5, 7, 9), or say the studio meets twice a week in sprint weeks. Either choice touches w01, w03 to w08 session plans and the m3 brief's "Reviewed" line, so it needs an author decision.

## 2. Syllabus (not editable by the reviewer)

- `syllabus.md` still has the generated-stub marker and `_todo_` example cells. Weeks 5 and 9 link their examples. Weeks 12 and 13 should link `examples/w12-burndown-projection.html` and `examples/w13-beta-turnout.html`; the other weeks have no example and need "—".
- `python tools/build_plan.py` was not run, because this review was told not to change `PLAN.md`. Run it once the syllabus is finished.

## 3. Checker design notes (acceptable, flagged for the author)

- `labs/lab02-starter/check_capacity.py` passes on the starter file by design (it is the Saltmarsh reference). The fail case is the warm-up's `headroom = 2.4`. The checker cannot tell a measured `cost_us` from a copied one; the instructor checks the spike note.
- `labs/lab06-starter/check_tick.py`: CLOSED. It now prints `NOT READY` unless `planned_mobs <= m_max` or the chosen option's modelled mean (`option_mean_ms`, a new claims key) meets both limits. It fails on the starter, fails with no option modelled or with the 60.0 ms world-boss row, and passes with the grid at 56.0 ms or with mobs cut to 170.

## 4. Undated source

- w05 cites the Warcraft Wiki "Respawn" page for fast respawn. The page gives no patch date, and the guide says so ("current retail game, no patch date given"). Replace with a dated source if one is found.
