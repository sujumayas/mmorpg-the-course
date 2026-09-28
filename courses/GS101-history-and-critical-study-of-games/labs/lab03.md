# GS101 · Lab 03: The operator's spreadsheet

**Week:** 3 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** feeds the timeline project (25%) as one "business cause" entry

**Lecture:** [Week 03, arcade era and the coin-op business model](../lectures/w03-arcade-era-and-the-coin-op-business-model.md)

## Objective

Build the quarter-clock model from the lecture, fit it to a session log from an invented arcade, and use it to recommend a difficulty ramp. By the end you will have seen that the ramp raising revenue per session can also cost you players, and you will have written a recommendation that weighs the two with numbers and a historical precedent.

## Starter materials

**The situation (invented).** An arcade operator tested one cabinet for two weeks in 1981. The cabinet costs $2,400, charges $0.25 a play and sits in a location open 10 hours a day. The operator keeps half the takings. In week 1 the difficulty ramp was set to `r = 0.5` per minute. In week 2 it was set to `r = 1.0`. Starting difficulty is `d₀ = 1` in both weeks. Staff logged a sample of sessions and whether the player immediately put in another coin.

**Session log.** Copy it into a spreadsheet.

| Session | Week | Ramp `r` | Group | Length (min) | Played again? |
|---|---|---|---|---|---|
| 1 | 1 | 0.5 | novice | 1.4 | Y |
| 2 | 1 | 0.5 | novice | 0.9 | Y |
| 3 | 1 | 0.5 | novice | 2.5 | N |
| 4 | 1 | 0.5 | novice | 0.6 | Y |
| 5 | 1 | 0.5 | novice | 2.1 | Y |
| 6 | 1 | 0.5 | regular | 7.6 | Y |
| 7 | 1 | 0.5 | regular | 6.6 | Y |
| 8 | 1 | 0.5 | regular | 8.0 | N |
| 9 | 1 | 0.5 | regular | 6.5 | Y |
| 10 | 1 | 0.5 | expert | 21.8 | Y |
| 11 | 1 | 0.5 | expert | 20.6 | N |
| 12 | 1 | 0.5 | expert | 20.7 | Y |
| 13 | 2 | 1.0 | novice | 0.9 | N |
| 14 | 2 | 1.0 | novice | 1.5 | Y |
| 15 | 2 | 1.0 | novice | 0.5 | N |
| 16 | 2 | 1.0 | novice | 0.6 | N |
| 17 | 2 | 1.0 | novice | 1.2 | Y |
| 18 | 2 | 1.0 | regular | 4.7 | Y |
| 19 | 2 | 1.0 | regular | 4.1 | Y |
| 20 | 2 | 1.0 | regular | 3.8 | Y |
| 21 | 2 | 1.0 | regular | 4.8 | N |
| 22 | 2 | 1.0 | expert | 10.3 | Y |
| 23 | 2 | 1.0 | expert | 11.6 | Y |
| 24 | 2 | 1.0 | expert | 10.7 | Y |

**Utilization log.** The operator also recorded how many of the 10 opening hours the cabinet was in use: an average of 7.1 hours a day in week 1 (`u = 0.71`) and 6.2 hours a day in week 2 (`u = 0.62`).

**Model sheet layout.** On a second sheet, set up these inputs: `p`, `u`, `H`, `s`, cabinet price, `r`, `d₀`, and a skill and share for each of the three groups. Compute, for each group, `L(S) = MIN(30, MAX(0.5, (S − d₀) / r))`, then the weighted average `L`, plays per day, revenue per hour, operator share per day and payback days, using the formulas in section 2 of the lecture.

**Check values.** With the lecture's defaults (`u = 0.75`, skills 2 / 5 / 12, mix 50 / 35 / 15, `r = 1`), your sheet must give an average `L` of 3.55 minutes and revenue per hour of $3.17.

## Steps

1. **Summarise the log (20 min).** For each week and group, compute mean session length and the share who played again. Put the results in a 6-row summary table.
2. **Fit skills (15 min).** The model says `L = (S − d₀) / r`, so `S = d₀ + r × L`. Estimate each group's skill from week 1 and again from week 2. The two estimates should be close. Explain any gap in one sentence.
3. **Build the model (25 min).** Build the model sheet and pass the check values. Then enter your fitted skills and the group shares from the log (5 / 4 / 3 of 12 sessions).
4. **Compare the weeks (15 min).** Compute revenue per hour and payback days for each week using that week's measured `u`. Which week earned more per day? Is the answer the same if you wrongly assume `u = 0.75` for both?
5. **Explore (15 min).** Find the ramp between 0.3 and 2.0 that maximises operator share per day if `u` stays at 0.75. Then assume `u` falls by 0.05 for every 0.25 of ramp above 0.5, and find the best ramp again. Record both.
6. **Precedent (10 min).** Choose one historical case from the lecture (Pong's rally speed-up, Space Invaders' accelerating aliens, Computer Space's operator timer, Dragon's Lair's 50-cent price, or Galaxy Game's free game for winners). Say which variable in the model it acts on.
7. **Memo (at home).** Write the recommendation described under Deliverable.

## Deliverable

- The spreadsheet: log, summary table, fitted skills, model sheet passing the check values, the week comparison and the ramp search.
- A 500-word memo to the operator recommending a ramp setting (or a price change instead). It must cite at least three numbers from your sheet, name the assumption your recommendation depends on most, and use your chosen historical precedent to support or challenge it. Say plainly that the data set is invented and small, and what you would measure next with a real cabinet.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Log summary and fit | Summary correct; skills fitted from both weeks with the gap explained | Summary correct, fit from one week only | Errors in means or no fit | 20% |
| Model | Passes check values; formulas traceable | Minor errors that do not change conclusions | Fails check values | 20% |
| Week comparison and search | Uses measured `u`; shows how the answer changes when `u` is assumed fixed; both searches done | One of the three parts missing | Not done | 20% |
| Precedent | Correct variable identified; precedent described accurately with source | Variable right, description thin | Wrong variable or invented history | 10% |
| Memo | Clear recommendation backed by three numbers, the key assumption named, limits of the data stated | Recommendation with weak support | No recommendation, or claims the invented data prove something about real arcades | 20% |
| Writing | 450-550 words, plain and precise | Length or clarity slightly off | Far off length or hard to follow | 10% |
