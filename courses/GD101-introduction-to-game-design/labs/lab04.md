# GD101 · Lab 04: Mini-opoly, find and fix a runaway leader

**Week:** 4, MDA ([lecture](../lectures/w04-mda-mechanics-dynamics-aesthetics.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** participation (10%), and the memo is practice for the analysis essay (20%).

## Objective

Play a small game with a built-in positive feedback loop, measure the gap between the round a game is decided and the round it ends, then design one rule change that shortens that gap. Predict its effect with a spreadsheet model before you test it at the table.

## Starter materials

Everything is paper. Each table of 3 or 4 students needs:

- **Board.** A loop of 24 squares drawn on A3 paper (a 7 × 7 grid of squares with the middle removed gives 24 border squares). Number them 0 to 23 clockwise. Mark squares 0 (Go), 6, 12 and 18 as safe. The other 20 squares are lots. Write "$60" on each lot.
- **Two six-sided dice**, one token per player (coins or erasers).
- **Money.** Paper slips or poker chips in $10 and $50 values; about $2,500 in total per table. One student is also the bank.
- **Lot cards.** 20 index cards numbered with the lot squares. The owner keeps the card in front of them.
- **Houses.** 80 small markers (paper clips or beans). A lot holds at most 4.
- **Log sheet.** One per game, with a row for rounds 0, 5, 10, 15, 20, 25, 30 and columns for each player's net worth.
- **Spreadsheet template.** Make a sheet with columns `turn`, `L_A`, `L_B`, `d`, `income_A`, `income_B`, `cash_B`, and input cells for `S`, `r`, `τ` and starting values. The formulas are in lecture section 2 and in the spec's "Two-player model" paragraph. There is no filled copy to download. Check your sheet against the four values in step 4 and the turn 0, 10, 20, 30, 40, 45, 50 and 55 rows of the lecture's table. Use this row logic, one row per turn starting at turn 0: `income_A = S + L_A − L_B − τ·d`, `income_B = S + L_B − L_A + τ·d`; next row's `L_A = L_A + r·income_A` if `income_A > 0`, else `L_A` unchanged and `cash_A = cash_A + income_A`; the same for B. The first row where `cash_B` is below zero is the bankruptcy turn.

**Mini-opoly rules (the same as the lecture's simulation).** Start with $300 each on square 0. On your turn, roll two dice and move. If you pass or land on Go, collect $20. If you land on an unowned lot and have at least $60, you may buy it (in this lab you must buy it). If you land on another player's lot, pay rent: $6 plus $10 per house on it. If you can't pay in full, give the owner all your cash and your lots (houses stay on them) and you are out. At the end of your turn, if you have at least $150, you must buy a house for $50 and put it on your lot with the fewest houses; repeat while you still have $150 or more. Net worth is cash plus $60 per lot plus $50 per house.

## Steps

1. **Play the base game (35 min).** Play one game for 30 rounds or until one player remains. Every 5 rounds, the bank reads out each player's net worth and the log keeper writes it down.
2. **Mark the gap (5 min).** On the log, find the **decided** round: the first logged round from which the eventual winner (highest net worth at the end) is in the lead at every later logged round. Mark the **ended** round. Compute the gap in rounds.
3. **MDA decomposition (10 min).** In three columns, list the mechanics that drive the loop, the dynamic you saw (in "who does what, when" form) and the aesthetic each player reported. Ask every player for one sentence on how the last third of the game felt.
4. **Model the loop (20 min).** Build the two-player model in your spreadsheet. Check it against the lecture: with defaults you must get `d(20) = 4.38`, `d(40) = 9.60`, and B's income first negative at turn 42, with B bankrupt (cash below zero) at turn 56.
5. **Design one fix (15 min).** Invent one rule change, not from the lecture, that should shorten the decided-to-ended gap. Examples of the kind of change: a catch-up rule tied to rank, an end condition, a cap. Express your fix in the spreadsheet as a change to the income equations, and predict the new tipping-point turn and bankruptcy turn.
6. **Test the fix at the table (30 min).** Play one game with your fix. Log it the same way. Compare the decided round, ended round and gap with your base game. Also run your nearest equivalent setting over 500 games in the [runaway leader simulator](../examples/w04-monopoly-feedback.html).
7. **Write the memo (home).**

## Deliverable

Hand in three things.

- The spreadsheet, with the base model and your fix on separate tabs.
- Both log sheets, photographed.
- A one-page memo (at most 450 words) that states the fix as a rule a player could read, your predicted and observed decided-to-ended gaps, and one aesthetic your fix protects and one it costs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Reproduces all four lecture test values; inputs are cells, not constants in formulas | One value off or inputs hard-coded | Values not reproduced | 25% |
| MDA decomposition | Mechanics, dynamic and aesthetics correctly layered; the dynamic is in "who, what, when" form and linked to a mechanic | One item in the wrong layer or vague dynamic | Layers confused | 20% |
| Fix design | Fix is a clear, playable rule; its effect on the income equations is written out and the prediction is numeric | Fix is clear but the prediction is qualitative | Fix is vague or copied from the lecture | 25% |
| Evidence | Base and fix games both logged; gap computed for each; honest about a sample of two games | One game poorly logged | Logs missing | 15% |
| Memo | Plain, numeric, names the aesthetic trade-off, within the word limit | Trade-off implied rather than stated | Hard to act on | 15% |
