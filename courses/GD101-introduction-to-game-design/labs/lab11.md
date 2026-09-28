# GD101 · Lab 11: Dominant strategy hunt

**Week:** 11 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** optional replacement playtest report. This lab produces one short report in playtest format; the best of the reports from labs 02, 11 and 12 can replace your lowest core report mark (see the [playtest reports brief](../assessments/playtest-reports-brief.md))

**Lecture:** [Week 11, Balance intuition: dominant strategies and how to spot them](../lectures/w11-dominant-strategies-and-how-to-spot-them.md)

## Objective

Find the dominant strategy hidden in a small card game, trace the cascade of dead cards it causes, and repair the game with one rule change. You will prove the problem on paper, watch it happen at the table, and then verify your fix both ways.

## Starter materials

- 8 index cards per pair, or paper slips. Write one set of Sell, Hoard, Steal and Guard for each player.
- Coins or tally marks for keeping score.
- A payoff-table template: a 4 by 4 grid with the cards as row and column labels (draw it on paper or in a spreadsheet).
- The rules of Market Stall below. This is an original game written for this lab.

> **Market Stall (version 1).** Two merchants compete for coins over 8 rounds. Both start with 0 coins. Each round, both players secretly choose one card and reveal at the same time. Cards return to your hand after each round. After 8 rounds, the player with more coins wins; equal coins is a draw. Coins can go below zero.
>
> - **Sell:** gain 3 coins, unless the opponent played Steal this round, in which case you gain nothing.
> - **Hoard:** gain 3 coins. Your stall is locked, so Steal cannot touch you this round.
> - **Steal:** if the opponent played Sell, you gain the 3 coins they would have made. If the opponent played Guard, you are caught: pay them 2 coins. Otherwise, nothing happens.
> - **Guard:** if the opponent played Steal, they pay you 2 coins. Otherwise, nothing happens.
>
> *Designer's note from the imaginary original team:* "Hoard is the safe, boring option. Sell is the same money with risk. Steal is the gamble, and Guard is the trap for gamblers."

## Steps

1. **Predict (5 minutes).** Before any analysis, each person writes down which card they think players will end up using most, and why. Keep this; you will compare it with your result.
2. **Build the payoff table (20 minutes).** Use net coins per round: coins you gained minus coins your opponent gained. Fill all 16 cells from the rules. Check two things before moving on: the diagonal is all zeros, and each cell (X, Y) is the negative of cell (Y, X). Your Sell row should read 0, 0, −3, +3 against Sell, Hoard, Steal, Guard.
3. **Run the row test (10 minutes).** Compare every pair of rows. Write every dominance you find as "X dominates Y (strict or weak)". If none is strict, look carefully for weak dominance.
4. **Follow the cascade (15 minutes).** Cross out each dominated row and its matching column. Rerun the row test on what is left. Repeat until nothing more can be crossed out. Write the order in which cards died and the card or cards left standing. Describe in two sentences what an 8-round game between two players who know this looks like.
5. **Watch it happen (25 minutes).** Play at least four full games of version 1 in pairs, with a third person recording every card choice by round. Do not tell the players your analysis. Count each card's share in rounds 1-2 and in rounds 7-8. Did play drift toward your step 4 answer?
6. **Fix it with one rule (20 minutes).** Write version 2 by changing exactly one rule. You may change a number or an interaction, but only one sentence of the rules. Rebuild the table and rerun the row test and the cascade. Your fix passes only if no card is dominated, strictly or weakly. If your fix fails, write down why and try another; keep the failed attempts, they count.
7. **Retest (at home, or in the lab if time allows).** Play at least four games of version 2 with players who did not help design the fix. Record choices and count card shares in rounds 7-8 again.

## Deliverable

A playtest report of up to 2 pages containing:

- Your step 1 prediction.
- The version 1 payoff table, the list of dominances, and the cascade order.
- Choice-share tallies from the version 1 games (early and late rounds).
- Your version 2 rule, its payoff table, and the row-test result showing no dominated card. Include any failed fixes and the dominance each one left behind.
- Choice-share tallies from the version 2 games.
- A 200-word reflection: was your prediction right, did the table or the table-top play reveal the problem first, and what did your fix cost in rules complexity?

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Payoff table | All 16 cells correct; diagonal and mirror checks shown | One or two cells wrong but the dominance still found | Several cells wrong, or table missing | 20% |
| Dominance and cascade | Every dominance named with strict or weak; cascade order correct; final state described | Main dominance found, cascade incomplete | Dominance not found | 25% |
| Observed play | Four or more games recorded round by round; early and late shares compared with the prediction | Fewer games, or shares without comparison | No playtest data | 15% |
| One-rule fix | Exactly one rule changed; new table correct; no dominated card; failed attempts documented | Fix works but the table has errors, or more than one rule changed | No working fix | 25% |
| Reflection | Honest comparison of prediction, table and play; names the complexity cost of the fix | Reflection present but generic | Missing | 15% |
