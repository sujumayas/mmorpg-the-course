# GD102 · Lab 11: Payoff matrix lab

**Week:** 11, intransitive mechanics ([lecture](../lectures/w11-intransitive-mechanics-rock-paper-scissors.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the Machinations models and exercises component (30%).

## Objective

Build a spreadsheet that analyzes any three-option counter loop, test it against scripted opponents, and use it to write a balance change that moves one option to a target share. You finish with a tool you will reuse in the balance appendix of your final system design document.

## Starter materials

You build the sheet from this layout. Use any spreadsheet program. Named cells are shown in `code`.

**Tab `Model`.**

| Cell | Content |
|---|---|
| B2, B3, B4 | `wR`, `wP`, `wS`: the prize for a rock, paper and scissors win. Start with 2, 1, 1. |
| B6, B7, B8 | `r`, `p`, `s`: the opponent mix. Start with 1/3 each. Add a check cell B9 `= r + p + s` that must equal 1. |
| D2:F4 | The payoff matrix from the lecture: rows Rock, Paper, Scissors (you), columns Rock, Paper, Scissors (opponent). Diagonal 0; D3 `= wP`, E2 `= -wP`, F2 `= wR`, D4 `= -wR`, F3 `= -wS`, E4 `= wS`. |
| H2:H4 | Expected payoff of each of your options, each row of D2:F4 multiplied by `r, p, s` and summed (use `SUMPRODUCT`). |
| J2:J4 | Stable mix: `r* = wS / (wR + wP + wS)`, `p* = wR / (...)`, `s* = wP / (...)`. |
| L2 | Best response this round: the option with the highest value in H2:H4 (use `INDEX`/`MATCH` on `MAX`). |

**Tab `Bots`.** Three scripted opponents, each a mix:
- Bot A, "Even": 1/3, 1/3, 1/3.
- Bot B, "Rock fan": 0.50, 0.25, 0.25.
- Bot C, "Equilibrium": copies J2:J4 from `Model`.

**Tab `Tournament`.** 60 rows. Column A is the round number. Column B is the bot's throw, drawn with `RAND()` against the bot's cumulative mix (rock if `RAND() < r`, paper if `< r + p`, otherwise scissors). Column C is your throw, typed by hand. Column D is your score from the payoff matrix. Column E is your running total. Freeze the `RAND()` column with copy and paste-as-values before you start, so the bot's throws do not change while you play. Keep the unfrozen original on a hidden tab for the next bot.

**Test values your sheet must reproduce.**
- Prizes (1, 1, 1), any mix of thirds: H2:H4 all 0; J2:J4 33.3% each.
- Prizes (2, 1, 1), opponent thirds: H2:H4 = +0.333, 0, −0.333; J2:J4 = 25%, 50%, 25%.
- Prizes (2, 1, 1), opponent (0.50, 0.25, 0.25): H2:H4 = +0.25, +0.25, −0.75.
- Prizes (3, 1, 2): J2:J4 = 33.3%, 50.0%, 16.7% (the *Yomi*-shaped triangle, with rock as attack, paper as block, scissors as throw).

## Steps

1. **Build and test.** Build `Model` and reproduce all four test values. Do not continue until they match.
2. **Predict, then play Bot A.** With prizes (2, 1, 1), write down which option you think wins most against Bot A. Play 20 rounds against Bot A, then record your total and compare it with 20 times the best value in H2:H4.
3. **Exploit Bot B.** Set the opponent mix to Bot B. Read the best response from L2 and play 20 rounds. Compare your average score with the H-column value.
4. **Try to beat Bot C.** Set the opponent mix to Bot C. Play 20 rounds with any strategy you like. Show from the H column why no strategy has a positive expected score, and compare your actual total. Explain the gap using the size of a 20-round sample (MA102 weeks 5 and 13).
5. **Sensitivity table.** Make a data table of the stable mix for `wR` from 0.5 to 5 in steps of 0.5, with `wP = wS = 1`. Chart the three shares. Mark where rock's share falls below 20%.
6. **The patch.** The design lead wants scissors at 40% of play while the rock prize stays at 2. Find a change to exactly one other prize that does it. Report the new stable mix and the first-week expected payoffs against a population still at the old stable mix (25%, 50%, 25%).
7. **Class tournament (last 20 minutes of lab).** Enter your step 4 throws into the shared class sheet. The instructor shows the room's shares next to Bot C's mix.

## Deliverable

The spreadsheet with all tabs, the chart from step 5, and a patch note of at most 300 words written for players. The patch note must state the change in plain words, predict which option players will see more of in the first week and which in the long run, and give the numbers behind both predictions.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All four test values reproduced; formulas reference named cells | One test value off or hard-coded numbers | Test values not reproduced | 25% |
| Bot rounds and sampling | Predictions written first; actual versus expected compared with a sample-size explanation | Compared without explanation | Rounds missing | 20% |
| Sensitivity analysis | Table and chart correct; 20% crossing marked and explained | Chart present, crossing missing | Missing | 15% |
| Patch design | Correct single-prize change, new mix and first-week payoffs correct | Change works, one number wrong | Wrong prize changed | 25% |
| Patch note | Plain, numeric, separates first-week and long-run effects | Numbers present but unclear | Vague or missing | 15% |

<details>
<summary>Instructor key for step 6</summary>

Scissors's share is `wP / (wR + wP + wS)`. With `wR = 2` and `wS = 1`, solve `wP / (3 + wP) = 0.4`, so `wP = 2`. New stable mix: rock `1/5 = 20%`, paper `2/5 = 40%`, scissors `2/5 = 40%`. First week, against (0.25, 0.50, 0.25) with prizes (2, 2, 1): E(Rock) `= 2 × 0.25 − 2 × 0.50 = −0.50`, E(Paper) `= 2 × 0.25 − 1 × 0.25 = +0.25`, E(Scissors) `= 1 × 0.50 − 2 × 0.25 = 0`. Paper, the option whose prize was raised, looks best in the first week. In the long run, scissors (which beats paper) rises from 25% to 40%.

</details>
