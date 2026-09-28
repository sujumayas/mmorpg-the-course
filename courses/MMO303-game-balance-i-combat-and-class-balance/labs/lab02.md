# MMO303 · Lab 02: Mitigation spreadsheet

**Week:** 2 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the problem sets (30%)

## Objective

Put four shipped armor formulas side by side in one sheet, rewrite each into the `A / (A + K)` form, and see where they agree and where they differ. Then add your own formula from the week 2 in-class activity and defend it in a short memo.

This lab uses [week 2](../lectures/w02-armor-and-damage-mitigation.md): mitigation `A / (A + K)`, damage taken `D × K / (A + K)` and effective HP `HP × (1 + A/K)`.

## Starter materials

- A blank spreadsheet (Google Sheets, Excel or LibreOffice Calc).
- The four formulas from week 2, section 2, as cited in that lecture's Sources.

| Game (era) | Formula for the share of damage removed | What plays the role of K |
|---|---|---|
| League of Legends (current) | `A / (A + 100)` for `A ≥ 0` | 100 |
| Diablo II (equal attacker and defender level) | chance to miss `DR / (DR + AR)`, clamped so hit chance stays in 5-95% | attacker's attack rating AR |
| World of Warcraft (classic era, attacker level 1-59) | `A / (A + 400 + 85 × level)`, capped at 75% | `400 + 85 × level` |
| Path of Exile 2 | `A / (A + 10 × hit)`, capped at 90% | `10 × hit damage` |

- Fixed test inputs for everyone: defender HP 1,000; armor (or defense) from 0 to 2,000 in steps of 50; Diablo II attack rating 500; WoW attacker level 50; Path of Exile 2 hit of 100 damage and a second column for a hit of 1,000.

## Steps

1. **One tab per game.** For each armor value, compute the share of damage removed (or expected share, for Diablo II), damage taken from a 100-damage hit, and EHP. Apply each game's cap or clamp.
2. **Rewrite check.** In a cell next to each game, write the value of K implied at the test inputs. Confirm that where mitigation equals 50%, armor equals K (before any cap applies).
3. **One chart, two views.** Plot all five series (four games plus Path of Exile 2's large hit) twice: mitigation against armor, then EHP against armor. Put the two charts next to each other.
4. **Where caps bite.** For WoW and Path of Exile 2, mark the armor value where the cap starts to apply. What EHP multiplier does each cap imply?
5. **Your formula.** Add the armor rule your pair designed in the week 2 in-class activity as a sixth series. If it uses a level-based or hit-based K, add columns for two different attackers.
6. **Break it.** Find one attacker (level, hit size or attack rating) for which your formula behaves badly: armor worthless, armor too strong, or a cap reached too early. Record the numbers.

## Deliverable

The spreadsheet and a memo of about 300 words recommending your formula for a small MMO with levels 1-30. The memo must cite at least two numbers from your sheet, state what K depends on and why, and describe the case from step 6 and how you would handle it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Four game tabs | All formulas, caps and clamps correct at the fixed test inputs | One formula or cap wrong | Two or more wrong | 25% |
| K rewrite and 50% check | K correct for every game, the 50% check shown | K stated but not checked | Missing | 15% |
| Two-view chart | Both views plotted, legible, labelled, cap points marked | Plotted but unlabelled or caps missing | One view only | 20% |
| Own formula and stress test | Sixth series with a clear K rule, a failure case with numbers | Formula added, failure case vague | Missing | 20% |
| Memo | Recommendation argued from the sheet's numbers, trade-offs named, about 300 words | Recommendation made but weakly supported | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- League at `A = 100`: 50% removed, 50 damage taken, EHP 2,000.
- Diablo II with AR 500 at `DR = 500`: expected 50% of swings miss; at `DR = 2,000` the formula gives 80% miss, which is inside the clamp (hit chance 20%).
- WoW, attacker level 50: `K = 4,650`. At `A = 2,000`, removal is `2,000 / 6,650 = 30.1%`. The 75% cap needs `A = 13,950`, off the chart; the cap implies at most a 4× EHP multiplier.
- Path of Exile 2 with a 100 hit: `K = 1,000`, so `A = 1,000` gives 50%. The 90% cap is reached at `A = 9,000`, beyond the chart. With a 1,000 hit, `K = 10,000`, so `A = 1,000` removes 9.1%.

</details>
