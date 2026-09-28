# MMO305 · Lab 06: Reputation replay

**Assigned:** week 6. **Due:** start of week 7. **Weight:** part of the final design project component (50% of the course).
**Lecture:** [Week 6, trust and reputation systems](../lectures/w06-trust-and-reputation-systems.md). **Interactive:** `examples/w06-reputation-memory.html`, for checking single players by hand.

## Objective

Replay a log of matched games for eight fictional players through three reputation designs, find which design misjudges which player, then design and justify your own. By the end you should be able to choose a forgetting factor and a prior from the behaviour you want to catch, not by habit.

## Starter materials

**Tool.** A spreadsheet or Python (standard library only).

**The model** (from the lecture). For each match the player plays, in order:

```
r = λ × r + (1 if the match was rated good, else 0)
s = λ × s + (1 if the match was rated bad,  else 0)
score = (r + a) / (r + s + a + b)
```

Decay applies only on matches the player plays. A `.` in the log means the player did not play that match slot, and their counts do not change.

**The match log.** 60 match slots per player, split into two lines of 30 for readability (slots 1 to 30, then 31 to 60). `G` is a good rating, `B` a bad rating, `.` not played.

| Player | Slots 1-30 | Slots 31-60 |
|---|---|---|
| P1 Steady | `GGGGGGGGGGGGGGGGBGGGGGGGGGGGGG` | `GGGGGGGGGGGGGBGGGGGGGGGGGGGGGG` |
| P2 Turncoat | `GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG` | `GGGGGGGGGGGGGGGBBBBBBBBBBBBBBB` |
| P3 Reformed | `BBBBBBBBBBBBBBBBBBBBGGGGGGGGGG` | `GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG` |
| P4 Bad week | `GGGGGGGGGGGGGGGGGGGGGGGGGGGGGB` | `BBBGGGGGGGGGGGGGGGGGGGGGGGGGGG` |
| P5 Noisy | `GGGGBGGGGBGGGGBGGGGBGGGGBGGGGB` | `GGGGBGGGGBGGGGBGGGGBGGGGBGGGGB` |
| P6 Toxic | `BBBGBBBGBBBGBBBGBBBGBBBGBBBGBB` | `BGBBBGBBBGBBBGBBBGBBBGBBBGBBBG` |
| P7 Late joiner | `..............................` | `..........GGGGGGGGGGGGGGGGGGGG` |
| P8 Whitewasher | `BBBGBBBGBBBGBBBGBBBGBBBGBBBGBB` | `BGBBBGBBBG....................` |

P8 abandons the account after slot 40 and starts a new one, which plays slots 41 to 60 with the same pattern as P6 over those slots. Call the new account P8b; build its log yourself from P6's slots 41 to 60.

**Three designs to compare.**

| Design | `λ` | `a` | `b` | Idea |
|---|---|---|---|---|
| A, lifetime | 1.00 | 1 | 1 | Nothing forgotten, neutral newcomer |
| B, short memory | 0.90 | 1 | 1 | About 10 matches of memory, neutral newcomer |
| C, dues-paying | 0.95 | 1 | 3 | About 20 matches of memory, newcomer starts at 0.25 |

**Check values.** Your final scores (after slot 60) for P1 should be 0.952 under A, 0.900 under B and 0.846 under C. P2 should be 0.742, 0.254 and 0.405. If yours differ, check that you skip `.` slots and apply decay before adding the new rating.

## Steps

1. **Replay.** Compute each player's score after every slot under all three designs. Report the final scores in a 9 × 3 table (P1 to P8 and P8b).
2. **Plot.** For P2, P3 and P4, plot score against slot for all three designs on one chart per player.
3. **Threshold test.** Suppose matchmaking puts any player scoring below 0.50 into a "low-trust" queue. For each design, list who is in the low-trust queue at slot 60, and at slot 35. Mark each placement as correct or wrong, using the behaviour you can see in the log over the last 15 slots as the truth.
4. **Whitewashing.** For each design, compute P8b's score at slot 41 (the new account's first match), 45 and 60. Compare with P8's score at slot 40. Under which design does whitewashing pay, and for how many matches?
5. **Your design D.** Choose `λ`, `a` and `b` (and, if you want, one extra rule such as a floor, a cap or a reset). Replay it and add a fourth column to the tables from steps 1, 3 and 4.
6. **Recommend.** Write a 350-word recommendation for a 4-player cross-server dungeon queue. It must state your design's half-life and newcomer score, name the player type it serves worst and why you accept that, and say whether the score should be visible to players.

## Deliverable

The spreadsheet or script, a results document with the tables from steps 1, 3, 4 and 5, the three charts from step 2, and the recommendation.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Correct replay | 25 | All 27 final scores correct to three decimals; check values match | Minor errors in a few players | Check values not matched |
| Charts | 10 | Three charts, three designs each, labelled | Missing a design or labels | Missing |
| Threshold test | 20 | Both slots, all designs, each placement judged with a reason | Placements listed without judgment | Missing |
| Whitewashing | 15 | Scores at 41, 45, 60 for all designs; payoff duration stated | Partial scores | Missing |
| Design D | 10 | Parameters stated and replayed in all tables | Parameters without replay | Missing |
| Recommendation | 20 | Half-life, newcomer score, worst-served type and visibility decision all argued with numbers | Argued without numbers | Missing |
