# GS101 · Lab 01: Reconstructing an ancient game

**Week:** 1 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** practice for close reading 1 (formative, feedback only)

**Lecture:** [Week 01, play before computers](../lectures/w01-play-before-computers.md)

## Objective

Test the four-lot model from the lecture against real throws, then play two reconstructed rule sets for the Royal Game of Ur and write a short close reading. By the end you will have evidence, from your own tally, of how a scoring rule changes play. You will also have practised separating what the evidence shows from what a reconstruction assumes.

## Starter materials

Everything below is described here. There is nothing to download.

- **Lots.** Four identical coins per pair. Heads counts as "marked". If you have tetrahedral dice with two marked tips, use them instead and note it.
- **Board.** Draw it on squared paper, one square about 3 cm. The layout matches the surviving boards: a block of 3 rows × 4 squares on the left, a bridge of 2 squares in the middle row only, and a block of 3 rows × 2 squares on the right, 20 squares in all. Label rows A (top), B (middle), C (bottom), and columns 1 to 8 from left to right. The squares that exist are A1-A4, B1-B8, C1-C4, A7-A8, C7-C8.

```
      1    2    3    4    5    6    7    8
A   [A1] [A2] [A3] [A4]           [A7] [A8]
B   [B1] [B2] [B3] [B4] [B5] [B6] [B7] [B8]
C   [C1] [C2] [C3] [C4]           [C7] [C8]
```

- **Pieces.** Seven tokens per player in two colours (coins, beads or paper circles).
- **Route and rosettes (lab version).** The pathway on the real board is disputed among scholars. For this lab, use the route found in many modern sets. Player A enters at A4, moves left to A1, drops to B1, runs right along row B to B8, rises to A8, moves left to A7 and bears off. Player C mirrors this on row C. Mark rosettes on A1, C1, B4, A7 and C7. Rows A and C are private. Row B is shared.
- **Rules (lab version, following Finkel's reconstruction as summarised in the lecture).**
  1. Throw the four lots. Move one piece forward by the number of marked lots. A throw of 0 means no move.
  2. You may not land on your own piece. Landing on an opponent's piece in row B sends it back off the board.
  3. A piece on B4 (the shared rosette) cannot be captured.
  4. Landing on any rosette gives an extra throw.
  5. To bear off, you need the exact number of squares to the end of the route plus one.
  6. The first player to bear off all seven pieces wins.
- **Variant rule for game 2 (Senet-style scoring).** Identical, except a throw of 0 moves 5.
- **Tally sheet.** Copy this table twice, one per game, into your notebook or a spreadsheet.

| Throw (marked lots) | Tally | Count | Observed % | Expected % |
|---|---|---|---|---|
| 0 | | | | 6.25 |
| 1 | | | | 25.0 |
| 2 | | | | 37.5 |
| 3 | | | | 25.0 |
| 4 | | | | 6.25 |
| Total | | | 100 | 100 |

- **Game log.** For each game, record the total number of turns, the number of captures, and the turn on which the eventual loser was furthest behind (count pieces borne off plus squares advanced, roughly).

## Steps

1. **Throw test (25 min).** In pairs, throw your four coins 200 times. Tally every result. Compute observed percentages and the observed mean throw. The model predicts a mean of 2.00. Write one sentence on how close you came.
2. **Bias check (5 min).** Count heads across all 800 coin landings. Compute your observed `p`. If it is outside 0.45 to 0.55, note it and use the lecture's formula to predict the mean throw for your `p` (`4 × p` under Ur scoring).
3. **Game 1, Ur scoring (30 min).** Play one full game with the lab rules. Tally throws and fill in the game log.
4. **Game 2, Senet-style scoring (30 min).** Swap first player and play again with 0 moving 5. Tally and log.
5. **Compare (10 min).** Compute the mean move per throw in each game. The model predicts 2.00 and 2.31. Did game 2 finish in fewer turns? Did the player who was behind make a comeback, and did a 0 throw contribute?
6. **Evidence audit (at home).** For each of the six lab rules and the route, write whether it rests on an artifact, a text or a modern reconstruction, based on the lecture and its sources. At least one must be marked "disputed".
7. **Close reading (at home).** Write the reading described under Deliverable.

## Deliverable

One document with:
- Both tally tables, the observed `p`, and observed and predicted means for the 200-throw test and both games.
- Both game logs.
- The evidence audit table (seven rows: route plus six rules).
- A 500-word close reading that makes one arguable claim about how the scoring of a 0 throw changes the Royal Game of Ur. Use the five steps of the method in section 5 of the lecture. Classify each version with Caillois's categories. Cite your own tallies as evidence, and state plainly which parts of the game you played are reconstruction.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Data and model | 200 throws tallied; observed and predicted values computed correctly; bias checked | Tally complete with a minor arithmetic slip or no bias check | Tally incomplete or model not applied | 20% |
| Game comparison | Both games logged; comparison uses the numbers and notes whether one game is enough evidence | Both games logged; comparison is descriptive | One game missing | 15% |
| Evidence audit | Every rule classified correctly with a reason; disputed route identified | Mostly correct, reasons thin | Missing, or reconstruction presented as fact | 20% |
| Claim | One clear, arguable claim tied to a specific rule | Claim present but vague | No claim, or only description | 20% |
| Use of evidence and vocabulary | Tallies and Caillois's categories used as evidence; sources cited | Some evidence, vocabulary used loosely | Opinion only | 15% |
| Writing | 450-550 words, plain and precise | Within 20% of length, some unclear sentences | Far off length or hard to follow | 10% |
