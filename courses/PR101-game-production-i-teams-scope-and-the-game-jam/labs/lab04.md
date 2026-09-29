# PR101 · Lab 04: The jam scope sheet

**Week:** 4, scope ([lecture](../lectures/w04-scope-mvp-vertical-slice-cut-lists.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home with your team.
**Weight:** part of the jam game component (30%). The scope sheet is the plan you carry into the week 8 jam, and week 6 and lab 06 re-estimate it.

## Objective

Write the scope plan for your team's jam concept: a one-pager with an MVP sentence, a prioritized and estimated task list with the cut line drawn, a cut list with dependencies, and four cut triggers. Then test the plan's safety by computing `m_max` for your build order and for a system-by-system order, and prove your MVP is buildable by making it for the one-screen prototype your lab 01 charter committed to.

## Starter materials

Everything below is in this file, plus:

- Your lab 01 charter, for your team's `c` and capacity `C`.
- Your GD101 week 14 one-pager format ([lecture](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md)).
- The [cut-line interactive](../examples/w04-cut-line.html), custom mode. The formulas in lecture section 2 give the same numbers if the interactive isn't available.

**Task table template.** One row per task, in build order. Estimates in team-hours. No task above 6 hours; split bigger ones.

| # | Task | System (P, E, L, A, U or your own) | Tier (MVP, Slice, Polish) | MVP bracket it serves (MVP rows only) | Estimate | Running total `S_k` |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

**Cut list template.**

| Cut task | What the player loses | Other tasks that depend on it |
|---|---|---|
| | | |

**Cut trigger template.** "At hour __, if ______ is not true, we ______." Write one for hours 12, 24, 36 (feature freeze) and 42 (content lock).

**Self-check list** (the marker uses the same list).

1. The MVP sentence fills all five brackets: verb, goal, pressure, fail state, win state.
2. Every MVP bracket maps to at least one MVP task, and every MVP task maps to a bracket.
3. `P = (1 − b) × C` is computed from your charter's `C`, with `b` stated.
4. The cut line is placed by walking the list in order and stopping at the first task that would pass `P` (no skipping ahead).
5. MVP tasks total at most 40% of `P`, or the sheet explains why not.
6. `S_MVP` and `m_max = C / S_MVP` are computed for your build order and for a system-by-system reordering of the same list.
7. Every cut-list row has a dependency entry, even if it's "nothing".
8. Four triggers exist, each with an hour, a test anyone can check in a build, and an action.

## Steps

1. **MVP sentence (15 min).** As a team, write your MVP sentence with the template from lecture section 3. Read it aloud to another team. If they can't say what the player does, rewrite it.
2. **Task list (30 min).** Each person lists tasks for their own area alone for 10 minutes, then merge. Estimate each task. Write each person's estimate privately first and take the median. Split anything over 6 hours.
3. **Tier and order (20 min).** Tag every task with a tier and a system. Put all MVP tasks first, in the order that makes the loop playable soonest, then slice, then polish. Fill the MVP bracket column.
4. **Cut line (10 min).** Compute `C` from your charter (`n = 4`, `H = 30`, your `c`), choose `b` (0.25 unless you can argue otherwise), compute `P`, fill the running totals and draw the line. Enter the list in the interactive's custom mode and check that it agrees.
5. **Safety test (15 min).** Compute `S_MVP` and `m_max`. Then reorder the same tasks by system (all of one system's tasks together) and compute both again. Write two sentences on what the difference means for your team.
6. **Cut list and triggers (20 min).** Fill the cut list with dependencies. Write the four triggers. Name the person who checks each trigger at its hour.
7. **Build the MVP (at home).** Build the MVP loop of your one-screen prototype from lab 01 in your team repository. Graybox only. Log the actual hours each MVP task took, per person. Record one screen-capture video (under 60 seconds) of a teammate who didn't build it playing from start to a win or a loss.
8. **Compare (at home, 10 min).** For each MVP task, write estimate, actual and the ratio actual / estimate. Keep this table; lab 06 uses it.

## Deliverable

A single PDF or Markdown file, `scope-sheet.md` in your team repository, at most three pages plus the tables, containing:

- The one-pager with the MVP sentence at the top.
- The task table with running totals and the cut line marked.
- `C`, `b`, `P`, `S_MVP` and `m_max` for both build orders, with working.
- The cut list and the four triggers with owners.
- The MVP estimate-versus-actual table from step 8.
- A link to the commit that contains the playable MVP, and the video.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| MVP sentence and mapping | All brackets filled; every bracket maps to a task and every MVP task to a bracket; risky mechanic is in the MVP | One gap in the mapping, or the risky mechanic sits in polish | No loop (no win or lose state), or no mapping | 20% |
| Task list and estimates | Complete across disciplines; no task over 6 h; private estimates merged by median | Some large or vague tasks | Missing whole disciplines (no audio, no UI) | 15% |
| Cut line and safety | Correct `P`, cut line without skipping, `S_MVP` and `m_max` right for both orders, sensible reading of the difference | Minor arithmetic errors | Line placed by feel, or `m_max` missing | 25% |
| Cut list and triggers | Dependencies filled; four triggers with checkable tests and owners | Triggers vague ("if we're behind") | Missing | 15% |
| Playable MVP | Builds from the repository; video shows a non-builder reaching win or loss | Playable with help, or video missing | Not playable start to end | 15% |
| Estimate log | Estimate, actual and ratio for every MVP task | Partial | Missing | 10% |
