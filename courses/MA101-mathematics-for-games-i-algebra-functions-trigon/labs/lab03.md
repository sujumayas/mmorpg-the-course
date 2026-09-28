# MA101 · Lab 03: Jump designer

**Week:** 3 ([Polynomials and quadratic curves](../lectures/w03-polynomials-and-quadratic-curves.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually, discussing with a neighbor is fine

## Objective

Build a jump from a chosen height and time to apex, step it frame by frame the way a game does, and measure how far three common update rules drift from the exact parabola. Add a fall multiplier and a ledge test. Then use differences to find the degree of three game data tables.

By the end you should be able to hand a programmer two numbers (`h` and `t_h`) and one update rule, and know exactly what jump they will get.

## Starter materials

- A spreadsheet, or a short script in any language you know (Python, JavaScript, C#, GDScript). Both routes are marked the same.
- The design formulas from lecture section 2: `g = 2h / t_h²`, `v₀ = 2h / t_h`.
- Three update rules to compare, each run once per frame with step `dt` (upward positive, `a = −g`):
  - **Rule 1 (position first):** `y += v·dt`, then `v += a·dt`.
  - **Rule 2 (speed first):** `v += a·dt`, then `y += v·dt`.
  - **Rule 3 (constant-acceleration step, from Pittman's GDC 2016 talk):** `y += v·dt + ½·a·dt²`, then `v += a·dt`.
- Data tables for Part D:
  - D&D 3.5 XP for levels 1 to 6: 0, 1,000, 3,000, 6,000, 10,000, 15,000.
  - Pokémon Medium Fast XP for levels 1 to 6: 1, 8, 27, 64, 125, 216.
  - League of Legends total growth with `g = 4` for levels 2, 6, 10, 14, 18 (from the week 2 lecture): 2.88, 15.80, 30.96, 48.36, 68.00. Note the spacing.
- Check values with `h = 3` tiles and `t_h = 0.4` s: `g = 37.5`, `v₀ = 15`.
  - `dt = 0.1`: highest point reached is 3.75 with Rule 1, 2.25 with Rule 2, 3.00 with Rule 3.
  - `dt = 1/60`: highest point is 3.125 with Rule 1, 2.875 with Rule 2, 3.000 with Rule 3.

## Steps

### Part A: design and exact arc (20 minutes)

1. Enter `h` and `t_h` as inputs. Compute `g` and `v₀`.
2. Tabulate the exact `y(t) = v₀·t − ½·g·t²` every 0.1 s from 0 to landing. Add first and second difference columns. Confirm the second difference equals `−g·dt²`.
3. Chart the exact arc and the exact speed line on two charts that share the time axis.

### Part B: stepping it like a game (35 minutes)

4. Implement the three update rules with `dt = 0.1`. For each, record the highest `y` reached and the time of landing (first step with `y ≤ 0`). Match the check values.
5. Repeat with `dt = 1/60` and `dt = 1/30`.
6. For Rule 1 and Rule 2, compute the apex error (highest point minus 3) for each `dt`. Show that it is proportional to `dt` by computing error divided by `dt`.
7. Write two sentences explaining why Rule 3 is exact for constant gravity and what would break that exactness.

### Part C: feel and ledges (30 minutes)

8. Add a fall multiplier `m` that multiplies gravity once `v < 0`. Use Rule 3. For `m` = 1, 2 and 3, record the fall time and total air time, and compare with `t_h / √m`.
9. Add horizontal speed `vx = 8` tiles/s. Use the quadratic formula to find where the character comes down to height 2 on the way down, for `m = 1` and `m = 2`. Confirm with your stepped table (within one frame).
10. Choose your own `h`, `t_h`, `m` and `vx` so that the character clears a 5-tile gap and lands on a ledge 1.5 tiles higher than take-off, with at least 0.5 tiles of margin. Show the discriminant and landing distance.

### Part D: find the degree (20 minutes)

11. For the D&D and Pokémon tables, compute differences until they are constant. State the degree and the leading coefficient, then the full formula.
12. The League table has levels 4 apart. Compute differences, then explain how to correct for the spacing. Show that the second difference per level step is `2 × 0.0175 × 4 = 0.14`, matching the lecture.

### Part E: write it up (at home)

13. Write a one-page jump spec for a programmer: the two design numbers, the fall multiplier, the update rule to use and why, the frame rate you assume, and one table of expected positions they can test against. At most 300 words plus the table.

## Deliverable

The spreadsheet or script (with a short README on how to run it), your charts, and the jump spec as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Design and exact arc (15%) | `g`, `v₀` correct; difference columns show constant second difference `−g·dt²` | Values right, difference check missing | One value wrong | Missing |
| Update rules (30%) | All three rules at three step sizes match the check values; error-over-`dt` analysis correct; Rule 3 explanation names constant acceleration | Rules correct, analysis thin | One rule wrong | Missing |
| Feel and ledges (25%) | Fall times match `t_h/√m`; ledge crossings solved and confirmed; own design clears the gap with stated margin | Crossings correct, own design lacks margin evidence | Quadratic formula misapplied | Missing |
| Degree detection (15%) | Three degrees and formulas correct; uneven spacing handled | Two correct | One correct | Missing |
| Jump spec (15%) | A programmer could implement it and test against the table without asking questions | Spec complete, table missing | Key number missing | Missing |
