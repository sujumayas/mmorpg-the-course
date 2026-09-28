# GD203 · Lab 08: Power curves and scaling bands

**Assigned:** week 8. **Due:** start of week 9. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 8, power curves and level scaling](../lectures/w08-power-curves-and-level-scaling.md). Builds on [Lab 07](lab07.md).

## Objective

Extend your Lab 07 pacing sheet with player and enemy power curves. Compute the power ratio `R` for every zone of a five-zone practice game under two scaling schemes, compare linear and exponential power, and recommend one scheme with evidence.

## Starter materials

Your Lab 07 spreadsheet with default inputs (40 hours, 30 levels, `g = 1.08`, `I₂ = 600`, `q = 1.12`). The five zones of the practice game:

| Zone | Level range | Fixed enemy level (midpoint, rounded down) |
|---|---|---|
| Meadow | 1 to 6 | 3 |
| Forest | 5 to 12 | 8 |
| Marsh | 10 to 18 | 14 |
| Peaks | 16 to 24 | 20 |
| Citadel | 22 to 30 | 26 |

**Power models.**

- Exponential: `a(L) = 10 × 1.1^(L − 1)`, `h(L) = 100 × 1.1^(L − 1)`, so power grows 21% per level.
- Linear: `a(L) = 10L`, `h(L) = 100L`.
- Power `P = a × h`. Power ratio `R = P_player / P_enemy`.

## Steps

1. **Power tab.** Rows for levels 1 to 30. Columns: `a`, `h`, `P` for both models, and the ratio `P(L + 5) / P(L)` for both. Check yourself: the exponential ratio is 2.594 on every row; the linear ratio is 4.00 at level 5 and 1.5625 at level 20.
2. **Levels to double.** Add a column giving the number of levels needed to double power from each level for both models. Check yourself: 3.64 for the exponential model at every level; 4.14 for the linear model at level 10.
3. **Scaling tab.** Make a grid with player levels 1 to 30 down the side and the five zones across the top. Fill it twice, once for fixed levels (`L_e` = the zone's fixed level) and once for banded scaling (`L_e = clamp(L_p, min, max)`). Use the exponential model, `R = 1.21^(L_p − L_e)`. Check yourself: player level 20 in the Forest gives `R = 9.85` fixed and `R = 4.59` banded; player level 10 in the Marsh gives 0.47 fixed and 1.00 banded.
4. **Conditional formatting.** Colour cells with `0.67 ≤ R ≤ 1.5` as "fair", `R > 3` as "trivial" and `R < 0.4` as "wall".
5. **Journey check.** Use your Lab 07 pacing table to find the player's level at hours 5, 10, 20, 30 and 40. For each, list which zones are fair under each scheme.
6. **Progress per hour.** Add a column to the pacing tab with the power gained per hour at each level, `21% / (t(n) / 60)`. Check yourself: 54.6% per hour at level 2 and 6.3% per hour at level 30. Repeat for the linear model using `(n / (n − 1))² − 1` in place of 21%.
7. **Downscaling variant.** Add a third grid where the player is downscaled to the zone's maximum level plus one, keeps gear worth a 1.3 times power bonus, and fights enemies at the zone's fixed level. Show that the Meadow never becomes "trivial" under this scheme and give the largest `R` a player can reach there. Check yourself: 2.79.
8. **Recommendation.** Choose one scheme for the practice game. Change at most two zone bands or fixed levels so that at every hour mark in step 5 at least two zones are fair.

## Deliverable

The extended spreadsheet (or a share link) with the power tab, three scaling grids and progress-per-hour columns, plus a recommendation memo of about 300 words with one chart of `R` against player level for the Forest and the Peaks under your chosen scheme.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Power tab | 20 | Both models, ratio and levels-to-double columns match check values | One model or one column wrong | Check values do not match |
| Scaling grids | 25 | Fixed, banded and downscaled grids correct with formatting | Two grids correct | One grid or wrong formulas |
| Journey and progress per hour | 20 | Hour marks mapped to levels, fair zones listed, both progress columns computed | Partly done | Missing |
| Chart | 10 | R against level for two zones, log axis, fair band marked | Chart present but hard to read | No chart |
| Recommendation memo | 25 | Scheme chosen with numbers, changes justified, every hour mark has two fair zones | Scheme chosen but constraint not met or not checked | Restates the lab without a decision |
