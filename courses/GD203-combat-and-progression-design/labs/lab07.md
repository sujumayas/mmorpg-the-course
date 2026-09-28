# GD203 · Lab 07: XP curve and 40-hour pacing sheet

**Assigned:** week 7. **Due:** start of week 8. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 7, XP curves](../lectures/w07-xp-curves.md).

## Objective

Build a spreadsheet that designs an XP table backwards from a play-time target, then use the same sheet to classify two shipped XP tables and to test how income changes break pacing. By the end you should be able to change one growth ratio and watch the XP table, the halfway level and the time plan all update. Keep the file. Lab 08 extends it.

## Starter materials

Create everything in any spreadsheet tool (Google Sheets, Excel, LibreOffice Calc). The practice game is fictional. The two shipped tables come from the sources cited in the week 7 lecture.

**Inputs for the practice game.**

| Input | Symbol | Default |
|---|---|---|
| Total play time to cap | H | 40 hours |
| Level cap | N | 30 |
| Time growth per level | g | 1.08 |
| XP income at level 2 | I₂ | 600 XP per hour |
| Income growth per level | q | 1.12 |

**Shipped tables to rebuild.**

- Old School RuneScape skills: `T(L) = floor( (1/4) × Σ_{ℓ=1}^{L−1} floor(ℓ + 300 × 2^(ℓ/7)) )`, levels 1 to 99.
- D&D 3.5 edition: `T(n) = 500 × n × (n − 1)`, levels 1 to 20.

## Steps

1. **Inputs tab.** Enter the five inputs in labeled cells. No formulas here.
2. **Pacing tab.** One row per level `n = 2 … N`. Columns: `t(n)` in minutes, `I(n)` in XP per hour, per-level cost `c(n) = t(n) / 60 × I(n)`, cumulative XP `T(n)`, cumulative minutes. Compute `t₂ = 60H × (g − 1) / (g^(N−1) − 1)`, and handle `g = 1` with `t₂ = 60H / (N − 1)`. Every formula must reference the inputs tab. Check yourself: `t₂ = 23.1` minutes, `c(10) = 1,058`, `T(30) = 273,397`.
3. **Halfway levels.** Add two cells. The XP halfway level is the first `n` where `T(n) ≥ T(N) / 2`. The time halfway level is the first `n` where cumulative minutes reach `30H`. Check yourself: time halfway level is 23 with defaults.
4. **Sensitivity.** Record the time halfway level and `T(30)` for `g = 1.00`, `1.08` and `1.12`. Check yourself: 16 and 177,586 for `g = 1.00`; 25 and 314,150 for `g = 1.12`.
5. **Chart.** One chart with two series on separate axes: minutes per level and XP per level. Add a second chart with cumulative share of XP and cumulative share of time, both from 0 to 100%, against level.
6. **RuneScape tab.** Rebuild the table for levels 1 to 99 with a helper column for the inner term. Add a column for the ratio of consecutive per-level costs `c(L) / c(L − 1)`. Check yourself: `T(92) = 6,517,253`, `T(99) = 13,034,431`, and the ratio is about 1.101 at level 10 and 1.104 at level 99. State which family it belongs to and give `r`.
7. **D&D tab.** Rebuild the 3.5 table for levels 1 to 20 and add the difference of consecutive per-level costs. State the family and its parameter. Find the halfway level.
8. **Scale test.** On the pacing tab, multiply `I₂` by 2. Record what happens to `T(30)`, the XP halfway level and the time halfway level. Explain in one sentence why the halfway levels did not move.
9. **Income shock.** Keep the XP table from the default inputs fixed (paste values). Now double XP income for levels 15, 16 and 17 only, as if a new boss drop were added there. Compute the new time for those levels and the minutes saved. Check yourself: about 102 minutes saved. Say which content the player will now skip.

## Deliverable

The spreadsheet file (or a share link) with the five tabs and two charts, and a pacing memo of about 300 words. The memo states where half the play time falls and why you think that is right for a 40-hour game, which family each shipped table belongs to with evidence from your ratio columns, and what the income shock did.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Sheet structure | 15 | Inputs isolated, all formulas reference them, `g = 1` handled | Some hard-coded numbers | Numbers typed into formulas |
| Pacing table and checks | 25 | All check values match, both halfway levels correct | Table correct but one halfway level wrong | Check values do not match |
| Shipped tables | 20 | Both rebuilt, family and parameter identified from ratio or difference columns | One table rebuilt or family asserted without evidence | Neither rebuilt |
| Charts | 10 | Both charts readable, axes labelled, two axes where needed | One chart or unlabelled axes | No charts |
| Sensitivity, scale and shock | 15 | All three experiments done with numbers | Two done | One or none |
| Pacing memo | 15 | Clear design decision backed by numbers from the sheet | Decision stated with few numbers | Restates the lab without decisions |
