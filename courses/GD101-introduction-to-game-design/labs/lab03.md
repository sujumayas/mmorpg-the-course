# GD101 · Lab 03: Tune the lives

**Week:** 3 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** part of the participation component; the dice run is reused in the paper prototype

**Lecture:** [Week 03, Formal elements II: resources, conflict, boundaries, outcome](../lectures/w03-resources-conflict-boundaries-outcome.md)

## Objective

Build the lecture's `W(n, L)` table in a spreadsheet, check it against a paper dice run you play yourself, and then use it to choose starting lives and a 1-up rule for a "casual" and a "hard" mode of the same run.

## Starter materials

- A spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No add-ons.
- Two six-sided dice and a pencil per pair.
- The dice run, fully described here:
  - A run has 6 stages. To clear a stage, roll two dice. If the total meets the stage's target, you clear it and move on. Otherwise you lose a life and retry the same stage.
  - Lives start at `L`. At 0 lives, the run is lost. Clearing stage 6 wins.
  - Chance of rolling at least the target on two dice: target 5 → 30/36 ≈ 0.833; target 6 → 26/36 ≈ 0.722; target 7 → 21/36 ≈ 0.583; target 8 → 15/36 ≈ 0.417.
- The starter workbook layout below. Create it yourself; there is no file to download.

| Sheet | Contents |
|---|---|
| `table` | Cell `B1` holds `p`. Row 3 holds `L = 0..8` in `C3:K3`. Column B holds `n = 0..12` in `B4:B16`. The grid `C4:K16` holds `W(n, L)`. |
| `tally` | Columns: run #, lives at start, target, stages cleared, won (1/0). |
| `modes` | Your casual and hard mode choices and their computed win chances. |
| `memo` | A text box for your recommendation. |

## Steps

1. **Build the table (25 min).** Fill row `n = 0` with 1 and column `L = 0` (below row 0) with 0. In every other cell, enter the recurrence: `= $B$1 * (cell above) + (1 - $B$1) * (cell to the left)`. Set `p = 0.8` and check three cells against the lecture: `W(2, 2) = 0.896`, `W(4, 3) = 0.9011`, `W(8, 3) = 0.6778`.
2. **Match the dice (10 min).** Set `p = 26/36`. Read off `W(6, 2)` and `W(6, 4)`. They must be 0.3784 and 0.7787 (to 4 decimals). Record them in `tally`.
3. **Play (35 min).** With target 6 for every stage, play 15 runs with 2 lives and 15 runs with 4 lives. Log each run. Compute your observed win rate for each setting and put it next to the model value.
4. **Add a 1-up (15 min).** Add a second grid for the rule "clearing stage 3 gives one extra life". Hint: build it from the top down as `f(cleared, lives)`, or simply play it forward in a helper table: the value after clearing stage 3 with `L` lives equals the no-1-up value for 3 stages left with `L + 1` lives. Report the win chance with 1, 2 and 3 starting lives at `p = 26/36`.
5. **Two modes (20 min).** Your target players are a first-timer (assume `p ≈ 0.72`, target 6) and an expert (assume the same dice but you raise the target to 7, `p ≈ 0.583`, to make the stages harder). Choose starting lives and whether to use the 1-up so that the casual mode wins about 60% of the time for the first-timer and the hard mode wins about 25% of the time for the expert. Use only the table, then play 10 runs of your hard mode to sanity-check it.
6. **Memo (at home).** Write the memo described under Deliverable.

## Deliverable

One spreadsheet with the four sheets and a memo of 250 to 350 words in the `memo` sheet. The memo recommends settings for both modes, quotes at least four numbers from your tables, compares your 30 logged runs with the model (and says whether the gap is surprising for 15 runs per setting), and names one thing the model ignores that your runs showed (for example, that dice players do not improve, while video game players do).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Table | Recurrence correct everywhere; all five check values match | One check value off because of a fixable reference error | Table wrong or hard-coded | 30% |
| Playtest data | 30 runs logged; observed rates computed and compared with the model | Fewer runs or no comparison | No runs | 20% |
| 1-up grid | Correct values for 1, 2, 3 starting lives; explains why the earned life helps less than a starting life | Values correct, no explanation | Missing or wrong | 15% |
| Mode design | Both modes land within 5 points of their targets, with the reasoning shown from the table | One mode on target | Guessed settings | 20% |
| Memo | Four or more numbers, a model-vs-data comparison, and a model limitation from observation | Numbers without the limitation | No numbers | 15% |
