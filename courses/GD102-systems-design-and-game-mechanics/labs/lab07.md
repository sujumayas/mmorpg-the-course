# GD102 · Lab 07: Town economy spreadsheet

**Assigned:** week 7. **Due:** start of week 8. **Weight:** part of the economy design component (30% of the course).
**Lecture:** [Week 7, internal economies](../lectures/w07-internal-economies-sources-drains-converters.md). **Interactive:** [w07-town-economy.html](../examples/w07-town-economy.html), for checking your numbers.

## Objective

Rebuild towns A and B from the lecture in a spreadsheet, confirm the lecture's table, then stress both towns with a faucet change, a crafting converter and a wave of new players. Draw town B as a Machinations diagram. Finish with a one-page recommendation on which sinks a small MMO should ship with. By the end you should be able to predict, before running the sheet, whether a change causes a price-level shift or ongoing inflation. Keep the diagram: week 13 asks you to bring it.

## Starter materials

Use any spreadsheet tool (Google Sheets, Excel, LibreOffice Calc) and the free web version of Machinations (machinations.io) or paper for the diagram. Everything below is fictional and matches the lecture.

**Inputs tab.** Enter these as named cells. No other numbers may appear inside formulas.

| Name | Value | Meaning |
|---|---|---|
| `N` | 100 | players |
| `M0` | 200,000 | starting money stock (both towns) |
| `F` | 100 | faucet, gold per player per day |
| `F_new` | 110 | faucet after the patch |
| `patch_day` | 0 | day the patch takes effect |
| `DA` | 100 | town A flat drain per player per day |
| `DB` | 40 | town B flat drain per player per day |
| `tau` | 0.10 | town B market cut |
| `v` | 0.30 | share of money spent on the market per day |
| `q` | 10 | potions crafted per player per day |
| `days` | 365 | horizon |

**Simulation tab.** One row per day from 0 to 365. Columns:

| Column | Formula |
|---|---|
| `t` | day number |
| `F(t)` | `F_new` if `t > patch_day`, else `F` |
| `MA(t)` | `MA(t−1) + N × (F(t) − DA)`; `MA(0) = M0` |
| `MB(t)` | `MB(t−1) + N × (F(t) − DB) − tau × v × MB(t−1)`; `MB(0) = M0` |
| `PA(t)` | `v × MA(t) / (N × q)` |
| `PB(t)` | `v × MB(t) / (N × q)` |
| `infl30A`, `infl30B` | `P(t) / P(t−30) − 1` from day 30 on |

## Steps

1. **Build and verify.** Build both tabs. Check yourself against the lecture: day 30 gives town A 230,000 and 69.0; town B 219,966 and 65.99. Day 365 gives town A 565,000 and 169.5; town B 233,333 and 70.00.
2. **Equilibrium cell.** Add `MB_star = N × (F_new − DB) / (tau × v)` and `PB_star`. Add the half-life `ln(0.5) / ln(1 − tau × v)`. Check: 233,333, 70.0 and 22.8 days.
3. **Chart.** One chart of `PA` and `PB` against day. A second of `infl30A` and `infl30B`. In one sentence under the second chart, explain why town A's 30-day inflation rate falls over the year even though its price never stops rising.
4. **Cut sweep.** Record `PB_star` for `tau` = 0.05, 0.10, 0.15, 0.20. Plot `PB_star` against `tau`. State the relationship in words. Check: 140 at 0.05 and 35 at 0.20.
5. **Converter.** Add a crafting converter: from day 100, a recipe improvement raises `q` from 10 to 15. Predict the day-101 price in each town before running it, then check. Explain why the money stock did not change but the price did.
6. **Population wave.** Reset `q` to 10. Add a `N(t)` column: 100 until day 60, then 150 (50 new players who join with 0 gold, so the money stock does not jump). Use `N(t)` in every formula. Check: on day 60, prices fall from 78.0 to 52.0 in town A and from 68.39 to 45.59 in town B. On day 365, town A is at 143.5 and town B at 70.0. Explain in two sentences why town B's price returns to exactly 70.
7. **Machinations diagram.** Draw town B with: a source (monster gold) into a pool (player gold); a drain (flat NPC costs) from the pool; a trader or pair of pools for the market; a drain on the market for the cut whose rate depends on the gold pool; a converter (herbs to potions) that feeds a potion pool. Label every rate with the lecture's symbol. If you use machinations.io, run it for 50 steps and screenshot the pool chart.
8. **Your sink set.** You are the economy designer for a small MMO with 2,000 players. Choose a set of sinks (at least one flat, at least one proportional). Put their numbers in your sheet (scale `N` to 2,000) and show that a 15% faucet increase leaves prices within 20% of their starting value after 180 days.

## Deliverable

The spreadsheet (file or share link) with Inputs, Simulation, and a Scenarios tab holding steps 4 to 6 and 8; the Machinations diagram (screenshot or photo); and a one-page recommendation memo (about 400 words). The memo names your sink set, gives its equilibrium money per player and price, reports the 180-day result from step 8, and says which group of players each sink falls on most heavily.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Sheet structure | 15 | All inputs named, no numbers in formulas, `N(t)` used throughout | A few hard-coded numbers | Numbers typed into formulas |
| Verification (steps 1-2) | 20 | All check values match | Most match, one error explained | Check values do not match |
| Experiments (steps 3-6) | 25 | All four done with predictions stated before results and correct explanations | Three done or explanations thin | Two or fewer |
| Machinations diagram | 15 | All required nodes, rates labelled, proportional drain shown as depending on the pool | Missing one node or labels | Diagram does not match the model |
| Sink set and memo | 25 | Meets the 180-day target, numbers from the sheet, names who pays | Target met but memo vague on who pays | Target not met or no numbers |
