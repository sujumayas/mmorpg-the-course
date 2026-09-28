# MMO301 · Lab 04: Contested versus instanced loot

**Week:** 4 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the case-studies assignment (40%)

## Objective

Simulate a year of one server's endgame with one contested boss and one instanced boss, measure how loot reaches each guild under rotation and under a race, and recommend an endgame policy for a server that is about to double in size.

This lab uses [week 4](../lectures/w04-everquest-the-treadmill-and-the-raid.md): `s = 7 / T`, contested `i = s × d / (G × R)`, instanced `i = 7 × d / (L × R)`, `W = 1 / i`, and the race share `q`.

## Starter materials

- A blank spreadsheet (Google Sheets, Excel or LibreOffice Calc).
- The parameter sheet below. Everyone uses these values for steps 1 to 5 so results can be compared.

| Parameter | Contested boss ("Ash Wyrm") | Instanced boss ("Vault Keeper") |
|---|---|---|
| Respawn `T` or lockout `L` | `T = 7` days | `L = 7` days |
| Drops per kill `d` | 3 | 3 |
| Raid size `R` | 40 | 40 |
| Guilds `G` | 6 | 6 |
| Weeks simulated | 52 | 52 |

- Guild strength table, used for race mode. Guild 1 is the strongest.

| Guild | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Race weight | 0.40 | 0.20 | 0.15 | 0.10 | 0.10 | 0.05 |

- Random numbers: use `RAND()` (or `=RAND()` in each row) and then copy and paste as values, so your results do not change on every edit. Record the date you froze them.

## Steps

1. **Spawn list.** Make one row per spawn of the contested boss over 52 weeks. With `T = 7` that is 52 rows. Add columns for week number and winning guild.
2. **Rotation.** In a second column, assign winners round-robin (1, 2, 3, 4, 5, 6, 1, ...). Count kills per guild. Compute items per raider per week and `W` for each guild, and check them against the formula `W = G × R / (s × d)`.
3. **Race.** In a third column, assign each spawn's winner by comparing a frozen random number to the cumulative race weights (0 to 0.40 is guild 1, 0.40 to 0.60 is guild 2, and so on). Count kills per guild and compute each guild's `W`.
4. **Instanced boss.** Every guild kills the Vault Keeper once per lockout. Compute each guild's kills and `W`. Confirm that `W` does not depend on `G`.
5. **Charts.** Plot kills per guild for rotation, race and instanced side by side as a grouped bar chart. Then plot `W` for guild 1 and guild 6 under all three.
6. **Growth.** The server doubles to 12 guilds. Extend the race weights by halving each existing weight and giving the six new guilds 0.5/6 each. Recompute the race and rotation results for the contested boss and the instanced results.
7. **Your policy.** Choose one change for the doubled server: shorten `T`, raise `d`, add a second contested boss, instance the Ash Wyrm, or add a participation reward. Recompute the numbers under your change.

## Deliverable

The spreadsheet, with steps 1 to 7 on labelled tabs, and a memo of about 400 words to the server's design lead. The memo must give the `W` for the weakest guild before and after doubling under your policy, say what your policy keeps from contested content and what it gives up, and cite at least one historical case from week 4 (EverQuest's move to instances, WoW's Azuregos problem, or the once-per-server Sleeper).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Rotation and instanced results | Kills and `W` correct for every guild and checked against the formulas | Correct but not checked, or one guild wrong | Two or more wrong | 20% |
| Race simulation | Winners drawn correctly from the weights, frozen, counts and `W` correct | Method right with an arithmetic slip | Weights ignored or results unfrozen | 20% |
| Charts | Both charts clear, labelled, three conditions comparable | One chart weak or unlabelled | Missing | 15% |
| Growth and policy | Doubled server computed for all conditions; the policy change recomputed with numbers | Growth computed, policy vague | Missing | 20% |
| Memo | Argued from the sheet's numbers, trade-offs named, historical case used correctly, about 400 words | Recommendation made but weakly supported | Opinion without numbers | 25% |

<details>
<summary>Instructor check values</summary>

- Rotation, 6 guilds: each guild gets `52 / 6 ≈ 8.67` kills (8 or 9 in the sheet). Formula: `W = 6 × 40 / (1 × 3) = 80` weeks.
- Instanced: 52 kills per guild, `W = 7 × 40 / (7 × 3) = 13.3` weeks, independent of `G`.
- Race, expected kills: guild 1 `0.40 × 52 = 20.8`, guild 6 `0.05 × 52 = 2.6`. Expected `W`: guild 1 `40 / (0.40 × 3) = 33.3` weeks; guild 6 `40 / (0.05 × 3) = 266.7` weeks. Sheets will vary with the random draw; accept values within about a factor of 1.5 for guild 6.
- Doubled server, rotation: `W = 12 × 40 / 3 = 160` weeks. Race: guild 1 weight 0.20, `W = 66.7`; each new guild weight 0.0833, `W = 160`; old guild 6 weight 0.025, `W = 533.3`.

</details>
