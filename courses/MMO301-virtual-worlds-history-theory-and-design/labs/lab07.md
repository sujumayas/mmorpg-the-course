# MMO301 · Lab 07: Content supply model

**Assigned:** week 7 ([lecture](../lectures/w07-themepark-vs-sandbox.md)). **Due:** start of week 8. **Feeds:** the structure chapter of the world design bible (40%).

## Objective

Build the week 7 novelty model in a spreadsheet, extend it with sharding and population decline, run it on three game profiles, and use it to recommend a themepark, sandbox or hybrid structure for a studio brief. The point is to argue about structure with numbers you can defend, and to say which of your numbers are assumptions.

## Starter materials

Everything is in this file.

**1. Spreadsheet layout.** Build one sheet named `model` with these input cells.

| Cell | Name | Meaning | Default |
|---|---|---|---|
| B2 | `p` | New authored hours shipped per month | 10 |
| B3 | `h` | Hours played per month by the player you are modelling | 40 |
| B4 | `K` | Half-novelty population | 300 |
| B5 | `P0` | Players in reach at launch (month 0), before sharding | 3,000 |
| B6 | `shards` | Number of shards the population is split across | 1 |
| B7 | `decay` | Monthly fall in population, as a fraction | 0.05 |

Then a table from row 10 with one row per month, months 0 to 36, and these columns.

| Column | Formula |
|---|---|
| A `month` | 0, 1, 2, ... 36 |
| B `N_total` | `P0 × (1 − decay)^month` |
| C `N_reach` | `N_total / shards` |
| D `s_T` | `MIN(1, p / h)` |
| E `s_S` | `N_reach / (N_reach + K)` |
| F `s_H` | `1 − (1 − s_T) × (1 − s_S)` |
| G `sandbox_wins` | `IF(s_S > s_T, 1, 0)` |
| H `repeat_hours` | `h × (1 − s_H)` |

Add a cell `N_star` with `K × s_T / (1 − s_T)` (guard against `s_T = 1`) and a cell `first_losing_month`, the first month in which a sandbox-only design falls below the themepark line (use `MATCH(0, G11:G47, 0)` or equivalent, and show "never" if none).

**2. Check values.** With the defaults and `decay = 0`, month 0 must show `s_T = 0.25`, `s_S = 0.9091`, `s_H = 0.9318`, `N_star = 100`. With `shards = 10`, `s_S = 0.5` and `s_H = 0.625`. If your sheet disagrees, fix it before going on.

**3. Three game profiles.** These are invented, for modelling only.

| Profile | `p` | `h` | `K` | `P0` | `shards` | `decay` |
|---|---|---|---|---|---|---|
| Harbor (themepark, many realms) | 20 | 45 | 400 | 60,000 | 40 | 0.03 |
| Ironreach (single-shard sandbox) | 4 | 70 | 250 | 12,000 | 1 | 0.06 |
| Lantern Vale (small hybrid) | 8 | 35 | 300 | 1,500 | 1 | 0.08 |

**4. Studio brief for the memo.** A studio of 25 people is building a fantasy MMO for players who play about 60 hours a month. It expects 5,000 players online at launch and plans for three shards "for stability". The team can ship 10 hours of new authored content per month. Leadership wants to call the game a sandbox.

## Steps

1. **Build and check.** Build the sheet and match the check values in item 2.
2. **Chart.** Plot `s_T`, `s_S` and `s_H` against month on one chart. Mark the month where `s_S` crosses `s_T`, if it does.
3. **Run the profiles.** For each of the three profiles, record month 0, month 12 and month 36 values of `s_T`, `s_S` and `s_H`, plus `N_star` and `first_losing_month`.
4. **Heavy and light players.** For Ironreach, rerun with `h = 20` and `h = 160`. Explain in two sentences why the heavy player's crossover is so different.
5. **Sensitivity.** `K` is the least known number. For Lantern Vale, find the `K` at which the sandbox part stops beating the themepark part at month 12. Report it and say whether it is plausible.
6. **Brief.** Model the studio brief with `K = 300` and your own stated `decay`. Test at least two shard counts.
7. **Memo.** Write a 400-word recommendation to the studio's leadership.

## Deliverable

One spreadsheet file and one PDF of at most three pages.

- The chart from step 2 for each profile.
- A table with the step 3 values.
- Two sentences for step 4 and one paragraph for step 5.
- The 400-word memo. It must state a recommendation (themepark-first, sandbox-first or hybrid), the numbers that support it, the shard count you advise, and the single event that would make your recommendation wrong, with a threshold.
- A list of every number you assumed rather than took from the brief, with a line on why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Check values match; formulas correct; `N_star` and `first_losing_month` handle edge cases | Minor formula slips that do not change conclusions | Check values do not match | 25% |
| Profile analysis | All three profiles, heavy and light players, and sensitivity run and interpreted in plain words | Runs complete but thin interpretation | Missing runs | 25% |
| Memo argument | Clear recommendation tied to specific numbers, shard advice justified, break condition with a threshold | Recommendation present, numbers partly used | Opinion without numbers | 30% |
| Honesty about assumptions | Every assumed number listed with a reason; the teaching model's limits named | Some assumptions listed | None listed | 10% |
| Writing | Plain, numbers first, within length | Readable but padded | Hard to follow | 10% |
