# GD101 · Lab 05: Experience goals and a difficulty ramp

**Week:** 5, player experience goals ([lecture](../lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** participation (10%); part A becomes the first page of your paper prototype (40%).

## Objective

Write experience goals for the game you will prototype in week 6. Then test the lecture's flow-channel model against real people: run a short timed card game with a rising difficulty ramp, measure each player's challenge ratio round by round, and compare it with what they say they felt.

## Starter materials

- **Your game concept.** One paragraph describing the paper game you plan to prototype in week 6. If you don't have one yet, use the instructor's fallback concept: "a two-player card game about racing to build a bridge before a flood arrives."
- **Aesthetics table** from lecture section 1 and the goal template from section 2.
- **Spreadsheet template.** Columns `n` (0 to 29), `S` for three learners, `C`, `R` and `zone` for each learner. Put `S0`, the three `g` values, `a`, `b` and the band edges (0.8 and 1.25) in input cells. Formulas: `S = 10 − (10 − S0) × g^n`, `C = a + b × n`, `R = C / S`, zone by the band edges. Add a count of each zone per learner.
- **Sort Sprint kit, per pair.** From a standard 52-card deck take the ace to 4 of each suit (16 cards). A phone stopwatch. A printed record sheet with columns: round, time limit, time taken, success (yes or no), felt (1 = bored, 2 = absorbed, 3 = stressed).
- **Sort Sprint rules.** The timer shuffles the 16 cards and hands them face down to the player. On "go," the player turns them over and lays them out in four rows, one per suit, each in order ace, 2, 3, 4. The round succeeds if the layout is correct before the limit. Time limits for rounds 1 to 10: 40, 36, 32, 29, 26, 23, 21, 19, 17, 15 seconds. The timer calls out the limit before each round. Right after each round the player says 1, 2 or 3 for how it felt, before hearing the time.

## Steps

**Part A: goals (25 min)**

1. Rank the top four aesthetics for your concept, most important first. Under each, name the mechanic you expect to produce it.
2. Write three experience goals in the template: who, feeling, observable moment. At least one goal must be about a moment in the first five minutes of play.
3. For each goal, write one observable sign that it's working and one that it's failing (lecture section 4 table).

**Part B: model (30 min)**

4. Build the spreadsheet. Check it with the lecture values: with `a = 2`, `b = 0.5`, `S0 = 2`, the zone counts must be fast 10 / 11 / 9, average 0 / 18 / 12 and slow 0 / 8 / 22 (bored / flow / anxious).
5. Find a linear ramp that keeps the average learner in flow for at least 25 of 30 rounds. Record `a`, `b` and all three learners' counts.
6. Find the ramp that maximizes the slow learner's flow rounds while keeping the fast learner bored for no more than 5 rounds. Say in one sentence why no single straight ramp does well for all three.

**Part C: Sort Sprint (40 min)**

7. In pairs, each partner plays all 10 rounds while the other times and records. Swap.
8. For each round from 2 to 10, compute the observed challenge ratio `R_obs(n) = t(n − 1) / L(n)`, where `t(n − 1)` is the time taken in the previous round and `L(n)` is this round's limit. It compares what the round demands with what the player just showed they could do. A failed round counts its full limit as the time taken.
9. Label each round's zone using the lecture's band (below 0.8 bored, 0.8 to 1.25 flow, above 1.25 anxious). Put the model's zone next to the player's own 1, 2 or 3.
10. Pool your pair's data with two other pairs (about 54 rounds). Count how often the model zone matched the self-report.

## Deliverable

- **Goals page** (Part A), one page. This becomes the front page of your week 6 prototype.
- **Spreadsheet** with Part B's checks, the two ramps you found and the pooled Sort Sprint data.
- **Short report** (at most 400 words). Report the match rate between model zone and self-report. Name one case where they disagreed and a likely reason. Say whether you would move the band edges for this game, and to what.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Aesthetic profile and goals | Ranked profile tied to mechanics; three goals each with who, feeling and moment; clear working and failing signs | One goal vague or signs missing for one goal | Goals are features or "be fun" | 30% |
| Model and ramps | Lecture checks reproduced; both ramps found with counts; clear reason no straight ramp fits all learners | Checks reproduced, one ramp weak or unexplained | Checks not reproduced | 25% |
| Sort Sprint data | Clean records for both partners; `R_obs` computed correctly, including failed rounds; pooled data present | Minor errors in `R_obs` or small gaps | Data missing or ratio computed wrongly | 25% |
| Report | Match rate stated; a disagreement explained with a plausible cause; a band change proposed with numbers | Match rate stated, discussion general | No numbers | 20% |
