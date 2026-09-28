# MMO401 · Lab 06: Corner and cartel simulation

**Week:** 6 ([lecture](../lectures/w06-manipulation-cornering-and-cartels.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade).

## Objective

Check the week 6 corner model against an agent-based version built on your lab 05 engine, find where the two disagree and why, and play a repeated cartel game to measure how patience and punishment change cheating. Finish with a one-page recommendation of defenses for a specific at-risk item.

## Starter materials

- [`lab06-starter.py`](lab06-starter.py): Python 3, standard library only. It contains
  - Part A, working: `corner_profit`, `best_corner` and `break_even_lag`, the closed-form model from lecture section 2, plus `check_part_a()`, which prints the lecture's profit table and break-even lags and must end with "Part A checks: ok";
  - `load_engine()`, which imports your lab 05 file (`lab05-starter.py` in the same folder; point it at `lab05.py` if you renamed it);
  - Part B stub `simulate_corner(...)` with step-by-step instructions in its docstring;
  - Part C: a working `cournot_profit(qs)` and a stub `run_cartel(...)`.
- Your finished lab 05 engine.
- The week 6 interactive, once built (`examples/w06-corner-calculator.html`).

## Steps

### Part A: the closed-form model (15 min)

1. Run the starter and confirm Part A. Then use `break_even_lag` to fill a table of `L*` for the three ladder shapes in the interactive spec (lecture, flat, steep) crossed with vendor ceiling off and at 12.

### Part B: the agent-based corner (60 min)

2. Implement `simulate_corner` following its docstring.
3. For hold price 17.5 and `L` = 1, 2, 3, 5, 7, average the cornerer's profit over 50 seeds. Put your numbers next to `corner_profit` in one table.
4. The two will not match exactly. Find at least two reasons. Typical ones: whole buyers per day instead of fractional demand; gatherers undercutting the cornerer's ask so that some buyers after day `L` pay less than 10; leftover stock marked at 10 even though the book is now full of gatherer asks. For each reason, state which direction it moves profit and test it by changing one thing.
5. Add an Old School RuneScape-style buy limit to the cornerer: at most 100 units bought per 4 "hours" (take 1 day as 24 hours, so 6 windows a day), with the float refilling at 50 units per day from sellers at the old prices. How many days does it take to buy the float? What happens to the premium and to profit at `L = 5`?

### Part C: the cartel game (35 min)

6. Implement `run_cartel` with the three strategies in its docstring.
7. For `n = 2` and `n = 3`, run 200 rounds with two grim-trigger players (or three) and record whether the cartel survives. Then replace one with the opportunist and sweep `delta` from 0.3 to 0.9 in steps of 0.05. Record average discounted profit for each strategy.
8. Compare the `delta` at which the opportunist stops beating the grim-trigger players with the lecture's thresholds (0.53 for two producers, 0.57 for three).

### Part D: recommendation (20 min)

9. Your live team flags a new-tier raid consumable with a float of 600 units, normal price 40, demand `D(P) = 900 − 15P` per day, and a gathering supply lag of 2 days. Using Part A (you may build the ladder as 6 levels of 100 at 38, 39, ..., 43), decide which defense to ship: a vendor ceiling (at what price), a second source (how many per day), a buy limit, or nothing. Justify with `L*` values.

## Deliverable

Your completed `lab06.py` and a report of at most two pages: the Part A table, the Part B comparison table with your two tested reasons, the buy-limit result, the Part C chart of profit against `delta`, and a 250-word Part D recommendation that names who pays for the defense.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Part A table | All six `L*` values correct | Four or five correct | Fewer | 10 |
| Agent-based corner | Runs, seeded, averaged over 50 seeds, clearly compared with the closed form | Runs but single-seed or no comparison | Does not run | 25 |
| Model gap analysis | Two reasons found, each tested by a one-change experiment with numbers | Reasons named without tests | Missing | 20 |
| Cartel game | Thresholds found for `n = 2` and `n = 3` and compared with the lecture | One `n` only | Missing | 20 |
| Recommendation | Defense chosen from computed `L*` values, costs to honest players named | Defense chosen with weak numbers | Opinion only | 25 |

<details>
<summary>Instructor check values</summary>

- Part A, vendor ceiling off: lecture ladder `L* ≈ 2.22`, flat ladder (1,000 at 10.25) `L* ≈ 0.44`. Steep ladder (100 each at 9 to 18, `C = 13,500`, premium 3,500): `L* = 3,500 / 562.5 ≈ 6.22`. With a ceiling at 12: lecture 4.81, flat `250 / 260 ≈ 0.96`, steep `3,500 / 260 ≈ 13.5`.
- Part D: ladder cost `100 × (38 + ... + 43) = 24,300`, premium `24,300 − 600 × 40 = 300`. Demand hits zero at 60, so the best hold price is 50 and daily markup income is `10 × 150 = 1,500`. `L* = 0.2` days, far below the 2-day lag, so the item is highly exposed. A vendor ceiling at `c` gives income `(c − 40)(900 − 15c)`. It needs `2 × (c − 40)(900 − 15c) < 300`, which holds for `c` below about 40.5, a ceiling so tight it removes most gathering income. A second source of `s` per day gives best daily income `15 × (20 − s/15)² / 4`. It must fall below 150, which needs `s` above about 205 a day, and at 300 a day or more the corner can never sell above 40. Good answers conclude that the practical fix is to shorten the lag (more sources) and add a buy limit, or to accept the corner as short-lived.

</details>
