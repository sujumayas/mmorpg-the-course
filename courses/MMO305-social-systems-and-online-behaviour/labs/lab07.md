# MMO305 · Lab 07: Status signal audit

**Week:** 7 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses and field observation work

## Objective

Audit the status signals of one real game. Separate how rare each achievement is from what it tells other players, estimate the precision of the achievements players treat as credentials, and recommend one rule change.

This lab uses [week 7](../lectures/w07-status-prestige-and-conspicuous-display.md): ownership `f = s × e + (1 − s) × (u + b)`, precision `P(skilled | owns) = s × e / f`, lift `= precision / s` and rarity `log2(1/f)`.

## Starter materials

- **A game with public achievement percentages.** Pick any multiplayer game on Steam with at least 30 achievements. Steam's global achievement page for each game lists every achievement with the percentage of the game's players who unlocked it. Record the date you collected it, since the numbers move.
- **Collection template.** Make a sheet with these columns:

  | Column | Content |
  |---|---|
  | `name` | Achievement name as shown |
  | `pct` | Global unlock percentage, as a decimal (4.2% becomes 0.042) |
  | `bits` | `log2(1 / pct)` |
  | `signal` | One of skill, time, wealth, luck, tenure |
  | `visible_where` | ambient, on-inspection, recorded, or not shown to others |
  | `fakeable_by` | How a player without the quality could get it (carry, purchase, luck, exploit, none) |

- **Worked row for calibration.** An achievement unlocked by 3.5% of players has `bits = log2(1/0.035) = 4.84`.
- **Field note.** One 30-minute session in the game's group finder, community Discord or forum, noting every time a player asks for or cites an achievement, rank or item as proof of ability.

## Steps

1. **Collect.** Record at least 30 achievements with `name` and `pct`. Include the 10 rarest.
2. **Classify.** Fill `signal`, `visible_where` and `fakeable_by` for every row. Where you are unsure, write down what you would need to find out.
3. **Rarity is not meaning.** Sort by `bits`. Among the 10 rarest, how many are skill signals? Name one rare achievement that says nothing about skill and explain why, in the terms of the lottery mount from week 7.
4. **Precision for three credentials.** Pick the three achievements your field note shows players treat as proof of skill. For each, estimate `s`, `e`, `u` and `b` with a one-line source or reason. Check that your estimates reproduce the observed `pct` within a factor of two, and adjust if they do not. Compute precision and lift.
5. **Break-even carry rate.** For each of the three, compute `b50 = s × e / (1 − s) − u`, the carry rate at which precision falls to 50%. Enter your numbers in `examples/w07-signal-precision.html` (custom mode) to check.
6. **One rule change.** Propose a change to one of the three achievements (earning rule, display venue, tradeability, expiry) that raises its precision by at least 15 points in your model. Name the players it upsets.

## Deliverable

The sheet, the field note (a list of observed credential requests with timestamps, no player names), and a memo of about 400 words to the game's designers recommending your rule change. The memo must quote at least three numbers from your sheet and address the gatekeeping loop from week 7, section 4.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Data collection | 30+ rows with date, bits computed correctly | Fewer rows or minor errors | Missing or copied without computation | 15% |
| Classification | Every row classified with a defensible signal and faking route | Most rows classified, some unjustified | Missing | 20% |
| Rarity versus meaning | Clear rare-but-meaningless example argued with the model | Example given, weakly argued | Missing | 15% |
| Precision estimates | Three credentials with sourced parameters that reproduce `pct`; precision, lift and `b50` correct | Numbers computed, parameters weakly sourced | Missing or wrong | 25% |
| Field note | Observed requests logged with context, anonymised | Few observations | Missing or includes names | 10% |
| Memo | Recommendation argued from numbers, costs and gatekeeping named, about 400 words | Recommendation weakly supported | Opinion without numbers | 15% |

<details>
<summary>Instructor check values</summary>

- `log2(1/0.01) = 6.64`, `log2(1/0.1) = 3.32`, `log2(1/0.5) = 1`.
- Example credential with `s = 0.05`, `e = 0.6`, `u = 0.005`, `b = 0.03`: `f = 0.0633`, precision 47.4%, lift 9.5, `b50 = 2.66%`.
- A common student error is to use `pct` as precision. Precision needs the split of owners into skilled and unskilled, which `pct` alone cannot give.
- Parameter estimates are judgment calls. Mark the reasoning and the consistency check in step 4, not closeness to any single answer.

</details>
