# MMO304 · Lab 14: Economy spec and steady-state simulation

**Assigned:** week 14. **Due:** with the final economy spec (week 15). **Weight:** feeds the final spec (50%); the simulation itself is graded here.
**Lecture:** [Week 14, designing an economy from scratch](../lectures/w14-designing-an-economy-from-scratch.md). Uses your [Lab 13](lab13.md) memo for the market section.

## Objective

Build a day-by-day simulation of your final-project game's currency, tune its sinks to hit a target steady-state wealth and half-life, and show that the server average behaves as the week 14 model predicts once players arrive and leave. The tuned sheet and its telemetry table become the core of your final spec.

## Starter materials

Use Google Sheets, Excel or LibreOffice Calc. Build a workbook named `MMO304_lab14_<yourname>` with three sheets laid out exactly as below, so graders can find every value.

**Sheet `inputs`** (one value per row, name in column A, value in column B, unit in column C):

| A: name | B: starter value | C: unit |
|---|---|---|
| faucet_quests | 3000 | gold/day |
| faucet_loot | 5000 | gold/day |
| faucet_daily | 2000 | gold/day |
| sink_repair | 2500 | gold/day |
| sink_travel | 1000 | gold/day |
| sink_consumables | 500 | gold/day |
| tax_rate | 0.03 | share of each sale |
| velocity | 0.3 | share of holdings sold per day |
| luxury_rate | 0.011 | share of holdings per day |
| arrivals | 100 | new players per day |
| stay_days | 90 | days each player stays active |
| target_wealth | 300000 | gold |
| target_half_life | 35 | days |

Add computed rows: `F = sum of faucets`, `S = sum of sinks`, `N = MAX(0, F − S)`, `s = tax_rate × velocity + luxury_rate`, `W_star = N / s`, `half_life = LN(2) / s`. With the starter values these give `F = 10,000`, `S = 4,000`, `N = 6,000`, `s = 0.02`, `W_star = 300,000` and `half_life ≈ 34.66`. These are the lecture's Tidewater design C numbers, so your sheet is correct when it reproduces them.

**Sheet `player`** (one row per day, days 0 to 365):

| Column | Header | Formula (row for day `t`, previous row is day `t−1`) |
|---|---|---|
| A | day | 0, 1, 2, ... 365 |
| B | wealth | day 0: `0`; later: `B_prev + N − s × B_prev` |
| C | tax_paid | `tax_rate × velocity × B_prev` |
| D | luxury_paid | `luxury_rate × B_prev` |
| E | continuous_model | `W_star × (1 − EXP(−s × day))` |
| F | gap_to_N | `N − (C + D)` |

The spreadsheet steps once per day, so column B is the discrete model `W_t = W* × (1 − (1 − s)^t)`. It runs slightly ahead of the lecture's continuous curve. Check values with starter inputs: B at day 30 ≈ 136,355 (continuous 135,357), day 90 ≈ 251,307 (continuous 250,410), day 365 ≈ 299,812. The steady state is the same, 300,000, in both.

**Sheet `server`** (one row per day, days 0 to 400): track cohorts. The simplest correct layout is a wealth-by-age lookup. For day `t`, the players active are those who arrived on days `max(0, t − stay_days + 1)` to `t`. Their wealth is `player!B` at their age. Compute:

| Column | Header | Formula |
|---|---|---|
| A | day | 0 to 400 |
| B | active_players | `arrivals × MIN(day + 1, stay_days)` |
| C | total_wealth | sum of `player!B` over ages 0 to `MIN(day, stay_days − 1)`, times `arrivals` (use `SUM(INDEX(...):INDEX(...))` or `OFFSET`) |
| D | average_wealth | `C / B` |
| E | share_of_W_star | `D / W_star` |

Check value: once `day ≥ stay_days`, the average settles near 160,385, which is 53.5% of `W*`. The lecture's continuous formula gives 53.6%. The small difference is the daily step.

A Python version is acceptable if you prefer. It must print the same check values and write the three tables to CSV with the same headers.

## Steps

1. **Reproduce Tidewater.** Build the workbook with starter values and confirm every check value above. Screenshot the three check rows.
2. **Replace the numbers with your game.** Rewrite the faucet and flat-sink rows for your final-project game. You may add rows. Every faucet and sink must name the activity that produces it. Keep `N > 0`.
3. **Set targets.** Choose `target_wealth` and `target_half_life` and justify each in two sentences (what should a settled player be able to buy, and how long should saving feel?).
4. **Tune.** Solve for the `s` you need, `s = LN(2) / target_half_life`, then check that `N / s` is near `target_wealth`. If not, change faucets or flat sinks, not `s`, to move `W*`. Split `s` into at least two proportional sinks, one of which reaches players who rarely trade.
5. **Chart.** On one chart, plot `player!B`, `player!E` and a horizontal line at `W_star`. On a second chart, plot `N` and `tax_paid + luxury_paid` per day. Mark the half-life.
6. **Stress test.** Run three scenarios and record `W*`, half-life and server average for each: (a) velocity halves because players dodge the tax, (b) `stay_days` doubles after a content update, (c) one exploit farm raises `F` tenfold for 1% of players (model this as a separate cohort row). Say which lever from your telemetry table you would pull in each case.
7. **Write the telemetry table.** At least four rows in the week 14 format: metric, segment, target band, lever if above, lever if below. At least one row must be segmented by account age.

## Deliverable

The workbook (or Python script plus CSVs), the two charts, and a two-page write-up containing your targets and justification, the tuned faucet and sink table, the stress-test results table, the telemetry table, and a one-paragraph market section that cites your Lab 13 memo.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) |
|---|---|---|---|
| Reproduction (step 1) | All check values match within rounding | Most match; one error explained | Check values missing or wrong |
| Model of own game (steps 2-4) | Every flow tied to an activity; targets justified; `s` split with one sink reaching low-velocity players; `W*` and half-life hit | Targets hit but thin justification or single proportional sink | Targets not hit or flows unexplained |
| Charts (step 5) | Both charts correct, labelled, half-life marked, steady state visible where sinks meet `N` | Charts present with minor labelling issues | Charts missing or misleading |
| Stress tests (step 6) | Three scenarios run, results tabulated, a named lever for each with its expected effect | Two scenarios or levers vague | Fewer than two scenarios |
| Telemetry and market sections (step 7, write-up) | Four or more rows with segments and levers; age-segmented row present; market section uses Lab 13 numbers | Table present but levers or segments missing | No telemetry table |

Total 20 points, scaled to the lab weight.
