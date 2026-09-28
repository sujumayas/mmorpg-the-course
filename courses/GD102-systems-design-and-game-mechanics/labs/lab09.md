# GD102 · Lab 09: Skill and power table

**Assigned:** week 9. **Due:** start of week 10. **Weight:** part of the economy design component (30% of the course); the tuned boss and valve analysis feed the progression section of the final system design document.
**Lecture:** [Week 9, progression systems: skill vs power](../lectures/w09-progression-systems-skill-vs-power.md). **Interactive:** [w09-skill-power-map.html](../examples/w09-skill-power-map.html), for checking your numbers.

## Objective

Build the lecture's win-probability model in a spreadsheet, map the 50% iso-win curve, tune a boss for a target player, and test three valves for stuck players. Then measure a real mistake rate with a five-minute paper playtest and use the model to predict how that player would do.

## Starter materials

**Part A, spreadsheet.** Inputs tab with named cells:

| Name | Value | Meaning |
|---|---|---|
| `HPb` | 2,000 | boss health |
| `db` | 250 | boss hit |
| `hp_per_L` | 100 | player health per level |
| `dmg_per_L` | 10 | player damage per level |
| `scale_on` | 0 | 1 = boss scales with `L / 10` |
| `losses` | 0 | failed attempts, for the assist valve |
| `assist_on` | 0 | 1 = damage reduction `min(0.02 × losses, 0.8)` |
| `summon_on` | 0 | 1 = player damage × 1.3 |

Useful spreadsheet functions: `CEILING` (or `ROUNDUP`), and `BINOM.DIST(A, H, m, TRUE)` for `P(X ≤ A)` (Google Sheets and Excel; LibreOffice uses `BINOMDIST`). Subtract a tiny amount such as `1e-9` inside the ceiling to avoid rounding errors when a division is exact.

**Part B, paper playtest kit.** One standard 52-card deck, a phone metronome set to 80 beats per minute, a partner, and a tally sheet with 20 boxes per fight. The deck plays the boss. Each exchange, the partner flips a card on a beat. You must call its color ("red" or "black") before the next beat. A wrong or late call is a mistake (you got hit). A fight is 20 exchanges.

## Steps

1. **Fight table.** On a Model tab, compute for one level and one mistake rate: `d_p`, `HP_p`, effective boss hit and health (with scaling, assist and summon switches), `H = ceil(HPb_eff / d_p)`, `A = ceil(HP_p / db_eff) − 1`, budget `A / H`, power ratio `(HP_p × d_p) / (HPb_eff × db_eff)`, and `P(win) = BINOM.DIST(A, H, m, TRUE)` (use 1 if `A ≥ H`).
2. **Verify.** Level 10, `m = 0.1`: `H = 20`, `A = 3`, `P(win) = 0.867`. Level 15, `m = 0.2`: 0.956. Level 8, `m = 0.3`: 0.033.
3. **Map.** On a Map tab, build a grid: levels 5 to 25 across, mistake rates 0.00 to 0.80 in steps of 0.05 down. Each cell is `P(win)`. Apply conditional formatting as a color scale.
4. **Iso-win curve.** For each level, find the mistake rate that gives 50% win (use Goal Seek, or a column of `m` at 0.001 steps and `MATCH`). Check: 0.181 at level 10, 0.395 at level 15. Chart the curve.
5. **Tune a boss.** The target player arrives at level 12 with `m = 0.25`. The default boss gives them 57.4%, and the team wants a harder first boss: a first-attempt win chance between 30% and 40%. Change `HPb` and `db` to hit that range. Record your values and the win chance. (One answer: `db = 300` gives 35.3%. Find a different one.)
6. **Grind test.** With your boss, record the target player's win chance at levels 12, 14, 17 and 20. Decide whether that curve is what you want, and justify it in two sentences.
7. **Valves.** For the target player at level 12 with `m = 0.35`, record the win chance with no valve, with scaling on, with assist after 1, 5 and 11 losses, and with the summon. Note every case where the valve does nothing, and explain it with `H` or `A`.
8. **Playtest.** Play three 20-exchange fights with the card kit, and have your partner do the same. Record each fight's mistakes. Estimate each player's `m` as total mistakes divided by 60.
9. **Predict and compare.** Using your measured `m`, find each player's win chance against the default boss at level 10 and the level at which they reach 50%. Then run 5 more card fights with the rule "you lose on the 4th mistake" (this is level 10, `A = 3`) and compare the observed wins with the prediction. In one paragraph, say whether the mistake rate stayed constant across fights or improved, and what that means for the model's assumption that `m` is fixed.

## Deliverable

The spreadsheet (file or share link) with Inputs, Model, Map and Valves tabs and the iso-win chart; the tally sheets (photo is fine); and a memo of about 400 words. The memo reports your tuned boss, the grind curve with your judgment on it, the valve you would ship with its cost, and what the playtest showed about skill growth during a session.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Model and verification | 20 | All switches work, ceilings guarded, all check values match | Check values match without switches working | Check values do not match |
| Map and iso-win curve | 15 | Full grid with color scale, curve matches check values | Grid or curve incomplete | Missing |
| Boss tuning and grind test | 20 | Target range met, grind curve recorded and judged with a reason | Target met but judgment missing | Target not met |
| Valve analysis | 20 | All valve cases recorded, every null effect explained by a breakpoint | Most cases, explanations partial | Few cases or no explanations |
| Playtest and comparison | 15 | 3 + 5 fights per player recorded, prediction compared honestly, comment on changing `m` | Fights recorded, weak comparison | No playtest |
| Memo | 10 | Clear recommendations backed by numbers from the sheet | Recommendations with few numbers | Restates the steps |
