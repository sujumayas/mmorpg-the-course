# GD203 · Lab 13: Difficulty ladder

**Assigned:** week 13. **Due:** start of week 14. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 13, difficulty modes and scaling](../lectures/w13-difficulty-modes-and-scaling.md).

## Objective

Build a spreadsheet that turns a default combat setup into a four-rung difficulty ladder with target safety ratios and a cap on fight length, solves for the multipliers on each rung, and shows how a level-scaling exponent changes the ladder across the game. By the end you should be able to change one target on the `Inputs` tab and see every rung, every enemy and every level update.

## Starter materials

Create these yourself from the definitions below. Any spreadsheet tool works (Google Sheets, Excel, LibreOffice Calc). Keep every input on one `Inputs` tab.

**Base fights on the default rung.** Use the enemy roles from your week 10 lab if you have them. Otherwise use this default:

| Enemy | TTK₀ (s) | TTD₀ (s) | Base safety ratio R₀ |
|---|---|---|---|
| Fodder | 2 | 40 | 20 |
| Soldier | 8 | 24 | 3 |
| Elite | 20 | 30 | 1.5 |

**Ladder targets.**

| Rung | Safety ratio vs Normal | Fight length cap vs Normal |
|---|---|---|
| Story | ×2 | ×1.0 |
| Normal | ×1 | ×1.0 |
| Hard | ×½ | ×1.25 |
| Nightmare | ×¼ | ×1.5 |

**Calibration data.** Skyrim's six difficulty multipliers as listed in lecture section 2 (from UESP). The [difficulty ladder](../examples/w13-difficulty-ladder.html) interactive prints the same table, so you can check your calibration against it.

**Formulas from the lecture.**

```
TTK = TTK0 × h / p
TTD = TTD0 / e
R   = R0 × p / (h × e)
health cost = 1 / R
R(P) = R0 × p / (h × e) × P^(1 − α)
```

## Steps

1. **Calibrate.** On a `Skyrim` tab, reproduce the lecture's table (TTK, TTD, safety ratio, health cost, ratio vs Adept) for a base fight of `TTK₀ = 10`, `TTD₀ = 30`. Your numbers must match the lecture to one decimal place. This checks your formulas before you use them.
2. **Solve the ladder.** On a `Ladder` tab, one row per rung. For each rung choose `p` and `h` so that `h / p` equals the fight length cap, with `p` no lower than 0.75. Then solve for `e` from the safety ratio target: `e = (p / h) / target`. Reference the `Inputs` tab only.
3. **Apply to enemies.** For each rung and each enemy, compute TTK, TTD, safety ratio and health cost. Use conditional formatting to flag any enemy whose health cost exceeds 100% (a straight trade is lost) and any fight longer than 30 s.
4. **Enemy-count variant.** Build a second version of Hard and Nightmare that keeps `p = h = 1` and uses a whole number of enemies `N` plus an enemy damage multiplier `e`. With `N` identical enemies focused one at a time, the encounter costs `N(N + 1) / 2` single fights of damage, so its safety ratio is `2 × R₀ / (N(N + 1) × e)`, and fight length is `N × TTK₀` (lecture section 3, and the focus-fire cost from week 10). Find the smallest `N` and matching `e` that hit each target without breaking the length cap, or show that no whole `N` can.
5. **Scaling tab.** On a `Scaling` tab, let player power grow as `P(L) = 1.08^(L − 1)` for levels 1 to 30. Plot the soldier's safety ratio on Normal against level for `α = 0`, `0.5` and `1`, and for a fourth `α` of your choice read from `Inputs`. Mark the level where each line leaves the band from 2 to 6.
6. **Choose.** Pick the `α` you would ship with your ladder. Add a row that shows, for each rung, the soldier's safety ratio at levels 1, 15 and 30 under that `α`.

## Deliverable

- The spreadsheet file, with tabs `Inputs`, `Skyrim`, `Ladder`, `Scaling`.
- A 400-word design memo. State which lever carries most of the difficulty on your ladder and why, what the elite fight feels like on Nightmare (in health cost and seconds), whether the enemy-count variant is better or worse than the multiplier version for your game, and which `α` you chose and what the player feels at level 30.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Calibration (15%) | Skyrim tab matches the lecture on every row | One row off | Several rows off, or formulas typed as constants | Missing |
| Ladder solution (25%) | Every rung meets its safety ratio and length targets exactly, `p ≥ 0.75`, all driven from `Inputs` | Targets met with one hardcoded value | Targets missed on one rung | Missing or unsolved |
| Enemy application and flags (15%) | All 12 enemy-rung cells correct; flags work and update | One error | Several errors or flags not driven by formulas | Missing |
| Enemy-count variant (15%) | Correct smallest `N` and `e`, or a correct proof that none exists | Correct `N`, wrong `e` | Formula for `N` enemies wrong | Missing |
| Scaling tab (15%) | Four curves plotted, band exits marked, chosen `α` table complete | Curves correct, band exits missing | One curve wrong | Missing |
| Memo (15%) | Every question answered with numbers from the sheet, with a clear recommendation | Complete but one claim unsupported | Vague or mostly qualitative | Missing |
