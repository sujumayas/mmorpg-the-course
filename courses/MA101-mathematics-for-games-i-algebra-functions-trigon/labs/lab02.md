# MA101 · Lab 02: Fit, compare and cross

**Week:** 2 ([Linear functions and rates](../lectures/w02-linear-functions-and-rates.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** in pairs

## Objective

Use slopes to test whether game data is linear, fit lines from two design points, convert rates between units, and design two items whose crossover level you choose in advance. You will also see the "constant absolute, shrinking relative" effect in your own numbers.

## Starter materials

- A spreadsheet program. No code needed.
- The Diablo II Barbarian life rule from lecture section 2: `Life(L) = 55 + 22·(L − 1)` with every point in Vitality.
- The classic-era WoW rules from lecture section 4: 14 AP per 1 DPS, damage per swing `= (weapon DPS + AP/14) × speed`.
- Four data sets (invented for this lab), each giving a stat at levels 1 to 6:

| Level | Set A | Set B | Set C | Set D |
|---|---|---|---|---|
| 1 | 40 | 10 | 100 | 12 |
| 2 | 46 | 13 | 110 | 19 |
| 3 | 52 | 18 | 121 | 26 |
| 4 | 58 | 25 | 133 | 33 |
| 5 | 64 | 34 | 146 | 41 |
| 6 | 70 | 45 | 161 | 48 |

- Check values: `Life(10) = 253`, relative gain from level 9 to 10 is 9.5%. A line through (1, 120) and (60, 3,660) has slope 60.

## Steps

### Part A: is it a line? (25 minutes)

1. For each data set, compute the slope between every pair of consecutive rows.
2. Classify each set as linear, not linear, or "linear with a problem." For the last kind, say which row breaks the pattern and suggest whether it is a rounding choice or a bug.
3. For each linear set, write the rule in point-slope form starting at level 1.
4. For the non-linear sets, compute the ratio between consecutive rows as well. Note which set has near-constant ratios. (You will meet that kind of curve in week 4.)

### Part B: absolute and relative gain (20 minutes)

5. Build the Barbarian life table for levels 1 to 99 with columns for life, absolute gain and relative gain. Chart life and relative gain on two separate charts.
6. Repeat with starting life 200 and slope 22, and with starting life 55 and slope 8. Put the three relative-gain curves on one chart.
7. For each of the three rules, find the first level-up that adds less than 2%. Show the inequality you solved and the table row that confirms it.

### Part C: fitting and domains (20 minutes)

8. Fit the line for enemy HP through (level 1, 120) and (level 60, 3,660). Check both endpoints.
9. Fit the line through (level 10, 200) and (level 40, 1,100). Find every level in 1 to 60 where it gives an impossible value. Propose a fix and justify it in two sentences.

### Part D: rates and crossovers (30 minutes)

10. A warrior has 1,050 AP. For weapons of speed 1.8, 2.6 and 3.6 with 40 weapon DPS each, compute DPS and damage per swing. Explain which number a once-per-swing effect uses.
11. Compute the composed rate "damage per swing per point of Strength" for each weapon.
12. Design two rings for levels 1 to 40. Ring A must be better up to level 18 and Ring B better from level 19 onward. Write both rules and show the crossover algebra.
13. Add a third ring with a different slope so that each ring is the best choice somewhere between levels 1 and 40. Chart all three and mark the two crossovers.

### Part E: write it up (at home)

14. Write at most 300 words for a design review. Explain, with at least three numbers from Part B, what "levels feel weaker" means and propose one change to the Barbarian rule or to what levels reward.

## Deliverable

One spreadsheet with sheets `Data`, `Growth`, `Fit` and `Rings`, plus the write-up as a PDF. Every value must come from a formula.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Linearity tests (20%) | All four sets classified correctly with slopes shown; the broken row in the problem set found and explained | Classification right, explanation thin | One set misclassified | Missing |
| Absolute vs relative gain (20%) | Three rules tabulated and charted; 2% thresholds solved and confirmed | Thresholds found by table only | One rule missing or wrong | Missing |
| Fitting and domains (20%) | Both lines correct, impossible values listed, fix justified | Lines correct, fix vague | One line wrong | Missing |
| Rates and crossovers (25%) | Per-second and per-swing values correct; crossovers land at the required levels; third ring works | Crossovers correct, third ring missing | Crossovers off by one or more levels | Missing |
| Write-up (15%) | Clear point, three or more numbers, one concrete change | Change proposed, evidence thin | No numbers | Missing |
