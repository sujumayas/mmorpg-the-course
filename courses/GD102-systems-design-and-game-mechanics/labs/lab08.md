# GD102 · Lab 08: Loop anatomy and the bend

**Assigned:** week 8. **Due:** start of week 9. **Weight:** part of the Machinations models component (30% of the course). The loop anatomy in part B is reused in the final system design document.
**Lecture:** [Week 8, core loops and meta loops](../lectures/w08-core-loops-and-meta-loops.md). **Interactive:** [w08-farm-loops.html](../examples/w08-farm-loops.html), for checking your numbers.

## Objective

Rebuild the lecture's parsnip loop in a spreadsheet, find the cycle where the watering limit binds, and show that the better crop flips when the binding constraint changes. Then apply the same analysis to a game you play: write its core loop as a `min` of limits, find the bend, and name the meta loop that moves it.

## Starter materials

**Part A, spreadsheet.** Create an Inputs tab with these named cells. Values come from the Stardew Valley Wiki as cited in the lecture (current 1.6-era game).

| Name | Value | Meaning |
|---|---|---|
| `G0` | 300 | starting gold |
| `E` | 270 | energy bar |
| `w0` | 2 | watering energy at Farming level 0 |
| `dw` | 0.1 | energy saved per Farming level |
| `S` | 0 | quality sprinklers (8 tiles each) |
| `season` | 28 | days |
| `levels_on` | 0 | 1 to let Farming level change `w` |

Crop table (one row each):

| Crop | Seed cost `c` | Sale price `p` | Days | XP per harvest |
|---|---|---|---|---|
| Parsnip | 20 | 35 | 4 | 8 |
| Cauliflower | 80 | 175 | 12 | 23 |

Farming XP thresholds for levels 0 to 10: 0, 100, 380, 770, 1,300, 2,150, 3,300, 4,800, 6,900, 10,000, 15,000.

**Part B, a game of your choice.** Any game you have played for at least ten hours. You will need about 30 minutes of play to take notes, or a clear memory of its opening hours.

## Steps

1. **Cycle tab.** One row per harvest cycle. Columns: cycle `k`, day, level `L`, limit `W = floor(E / (w0 − dw × L × levels_on)) + 8 × S`, tiles `n = min(floor(G / c), W)`, gold after harvest, XP after harvest, new level (use `MATCH` or `LOOKUP` against the threshold list). Stop when the next harvest would end after day 28.
2. **Verify.** Parsnip, 300 gold, levels off: gold 525, 915, 1,590, 2,775, 4,800, 6,825, 8,850. Levels on: final gold 10,425, final XP 5,400. Add a "binding" column that shows "gold" or "water" for each row.
3. **The bend.** Add an "on paper" column `G0 × (p/c)^k`. Chart both on a log axis. Mark the first cycle where "water" binds.
4. **The flip.** Run parsnip and cauliflower with `G0 = 300` and with `G0 = 20,000`, levels off. Record final gold for each. Check: with 20,000, parsnip ends at 34,175 and cauliflower at 45,650 after 24 days. In three sentences, explain the flip using "growth factor per day" and "profit per tile per day".
5. **Meta sweep.** With parsnip, 300 gold, levels on, vary `S` from 0 to 20 in steps of 5. Record final gold and the day the limit first binds. Check: `S = 10` gives 12,555. Describe what happens to the day of the bend.
6. **Part B: clock table.** For your chosen game, fill in the four-row clock table from the lecture (moment-to-moment, core, meta, long arc). For each row, name the action, its typical length and the resource it produces.
7. **Part B: the `min`.** Write the core loop's growth as `n = min(limit 1, limit 2, ...)`. For each limit, say what the player sees on screen that tells them it is binding. Say which limit binds in hour 1 and which in hour 10.
8. **Part B: the meta move.** Name the meta upgrade that moves the late-game constraint. Classify it as changing numbers or verbs. Propose one change that would move the bend by about 50%, and state which term in your `min` it changes.

## Deliverable

The spreadsheet (file or share link) with the Cycle tab, charts and a Scenarios tab for steps 4 and 5; and a two-page loop anatomy for part B containing the clock table, a Machinations-style diagram of the core and meta loops (hand-drawn is fine), the `min` formula with every limit explained, a sketch of the main currency over time with the bend marked, and your proposed change.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Model sheet | 20 | Inputs named, `min` and level lookup correct, all check values match | Check values match with one level of hard-coding | Check values do not match |
| Bend and flip (steps 3-4) | 20 | Log chart with bend marked, flip explained with both rates | Chart or explanation incomplete | Missing |
| Meta sweep (step 5) | 10 | Five runs recorded, bend day trend described | Fewer runs | Missing |
| Loop anatomy (steps 6-7) | 30 | Clock table complete, `min` names real limits with on-screen evidence, hour-1 and hour-10 constraints differ or the author explains why not | Table complete but limits vague | Loop is a list of verbs with no limits |
| Meta move and proposal (step 8) | 20 | Classifies numbers vs verbs, proposal targets a named term and estimates the effect | Proposal present but not tied to a term | Missing |
