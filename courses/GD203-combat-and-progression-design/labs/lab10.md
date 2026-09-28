# GD203 · Lab 10: Enemy roster from player units

**Assigned:** week 10. **Due:** start of week 11 (the workshop reuses this sheet). **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 10, enemy design by the numbers](../lectures/w10-enemy-design-by-the-numbers.md).

## Objective

Build a spreadsheet that turns enemy role templates, written in player units, into stat blocks at every level from 1 to 30, and then prices five encounters against a budget. By the end you should be able to change one role target and watch every enemy at every level update, and see at once which rooms break their budget.

## Starter materials

Create these yourself from the definitions below. Any spreadsheet tool works (Google Sheets, Excel, LibreOffice Calc). Keep every input on one `Inputs` tab.

**Player curve (levels 1-30).** Use the curve from your week 8 lab if you have one. Otherwise use this default:

| Quantity | Formula | Level 1 | Level 30 |
|---|---|---|---|
| Player DPS `P(L)` | `10 × 1.06^(L − 1)` | 10.0 | 54.2 |
| Player health `H(L)` | `100 × 1.05^(L − 1)` | 100 | 411.6 |

**Role templates.**

| Role | Target TTK `t` (s) | Cost share alone `s` | Attack interval (s) |
|---|---|---|---|
| Fodder | 1.5 | 0.02 | 1.2 |
| Soldier | 5 | 0.09 | 2.0 |
| Caster | 3 | 0.12 | 2.5 |
| Elite | 20 | 0.35 | 3.0 |

**Five rooms.** Each room has a level and a list of enemies. The budget is the share of player health the room may cost under the best kill order and focus fire.

| Room | Level | Enemies | Budget |
|---|---|---|---|
| A | 3 | 5 fodder | 20% |
| B | 8 | 2 soldiers, 1 caster | 40% |
| C | 15 | 1 elite, 3 fodder | 60% |
| D | 22 | 3 soldiers, 2 casters | 70% |
| E | 30 | 1 elite, 2 casters, 2 fodder | 90% |

## Steps

1. **Player table.** On a `Levels` tab, one row per level 1-30 with columns `L`, `P`, `H`. Reference the growth rates from `Inputs`; no constants typed into formulas.
2. **Stat blocks.** For each role add columns for health `h = P × t`, DPS `d = s × H / t`, damage per hit `d × interval`, hit size as a share of `H`, and priority ratio `d / h`. Use absolute references to the role table so the whole block fills down cleanly.
3. **Breakpoint pass.** Pick one weapon from your week 4 lab (or assume the player hits every 0.8 s for `0.8 × P`). For the soldier row at levels 5, 15 and 25, compute hits-to-kill and move `h` to the middle of its breakpoint step, as in week 4 section 4. Record the damage margin in both directions.
4. **Encounter cost.** On a `Rooms` tab, for each room pull the stat blocks at the room's level, sort the enemies by priority ratio (highest first), and compute each death time `T_i` and the cost `Σ d_i × T_i`. Also compute the worst-order cost (lowest ratio first).
5. **Checks.** Add a column `best cost / H` and one for the budget. Use conditional formatting: green when inside budget, red when over. Add a second check that flags any single hit above 25% of `H`.
6. **AoE variant.** Add an input `a` for an AoE class (start at 0.4). Compute the AoE cost of each room with `T_i = h_i / (a × P)`. Add a column showing whether AoE or focus fire is cheaper per room.
7. **Tune.** Change role targets (not individual cells) until every room passes its budget for the focus-fire player and no room costs the AoE class less than a third of its budget. Record every change you make in a `Changelog` tab with the reason.

## Deliverable

- The spreadsheet file, with tabs `Inputs`, `Levels`, `Rooms`, `Changelog`.
- A 300-word memo: which room was hardest to fix, which role target you changed and why, and how big the best-order versus worst-order gap is in room D (in health and in percent). State whether that gap is large enough that kill order feels like a decision.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Structure and traceability (20%) | All constants on `Inputs`, no hardcoded numbers in formulas, clear labels and units | One or two hardcoded values | Several hardcoded values or unlabeled columns | Formulas cannot be followed |
| Stat block correctness (20%) | `h`, `d`, hit size and ratio correct at all spot-checked levels | One formula error that propagates | Several errors | Stat blocks missing |
| Encounter cost (25%) | Best and worst orders correct for all five rooms, matches a hand check | Correct for four rooms | Order not sorted by ratio, or cost formula wrong | Missing |
| Checks and AoE variant (15%) | Conditional formatting and hit-size flag work; AoE cost and comparison correct | Checks work, AoE partly wrong | Checks present but not driven by inputs | Missing |
| Tuning and memo (20%) | Changes made at the role level, logged with reasons; memo answers every question with numbers | Memo complete, changelog thin | Memo vague or unsupported by the sheet | Missing |
