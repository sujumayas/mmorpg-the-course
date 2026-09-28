# MMO304 · Lab 07: Crafting chain workbook

**Week:** 7 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Build a spreadsheet that follows a branching crafting chain down to its raw materials, prices every stage, and finds the point where experience crafting pulls the finished item's price away from its cost. Then redesign one rule of the chain to hit a target and defend it.

This lab uses [week 7](../lectures/w07-crafting-chains-and-gathering-professions.md): the effective input ratio `e = q × (1 − r) / s`, the bill of materials `R`, the experience-crafter market with threshold `a − b × C`, and the opportunity-cost price `p ≈ W / u`.

## Starter materials

- A blank spreadsheet (Google Sheets, Excel or LibreOffice Calc).
- The chain below, from an invented game. Every number is fixed for the whole class.

| Stage | Output | Inputs per attempt | Success `s` | Refund `r` |
|---|---|---|---|---|
| Smelt | 1 bronze bar | 2 copper ore, 1 tin ore | 0.8 | 0 |
| Cut | 4 rivets | 1 bronze bar | 1 | 0 |
| Tan | 1 leather | 2 hides | 1 | 0 |
| Assemble | 1 bronze helm | 3 bronze bars, 8 rivets, 2 leather | 0.9 | 0.05 on every input |

Note that the Cut stage makes 4 rivets per bar, so its ratio is `1/4 = 0.25` bars per rivet.

- Raw prices: copper ore 6 gold, tin ore 10 gold, hide 4 gold.
- Market for helms: `Q_d = 900 − 3 × P` per day. Vendor floor 20 gold.
- Gathering data: a player mines 150 copper ore per hour or 90 tin ore per hour. The best alternative activity pays 1,200 gold per hour.

## Steps

1. **Ratios.** Make a table with one row per stage and per input. Compute `e` for each. Check that the Assemble stage's factor `(1 − 0.05) / 0.9` is the same for all three inputs.
2. **Bill of materials.** Follow every path to raw materials. Compute copper ore, tin ore and hides per helm. Show the path for rivets explicitly (rivets to bars to ore).
3. **Cost waterfall.** Compute the cost of one bronze bar, one rivet, one leather and one helm. Draw a waterfall or stacked bar showing how much of the helm's cost comes from each raw material.
4. **Recipe card versus reality.** Compute the ore the "recipe card" suggests if every success chance were 1 and there were no refund. Report the gap as a percentage.
5. **Market.** Compute the threshold `a − b × C`. For experience-crafter volumes `X` of 0, 200, 400, 600 and 800 per day, compute the market price, profit-crafter output, and value destroyed per helm. Plot price against `X` from 0 to 900.
6. **Gathering check.** Using `p ≈ W / u`, estimate the long-run prices of copper and tin. Are the starter prices above or below these? What does that predict about gatherers' behaviour?
7. **Redesign.** The design lead wants the helm's material cost below 130 gold without changing raw prices. Change exactly one rule (a quantity, a success chance or a refund) to get there. Recompute and report the new cost and threshold.

## Deliverable

The spreadsheet and a memo of about 300 words. The memo must state the helm's bill of materials, the `X` at which the price leaves cost, your redesign and its new numbers, and one side effect of your redesign on gatherers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Ratios and bill of materials | All `e` values and raw totals correct, rivet path shown | One ratio or path wrong | Two or more wrong | 25% |
| Cost waterfall | Costs correct at every stage, chart legible and labelled | Costs right, chart unclear | Costs wrong | 15% |
| Market analysis | Threshold, five prices and plot correct, kink and floor marked | One case wrong or plot missing the kink | Missing | 25% |
| Gathering check | Both prices estimated and the behaviour prediction argued | Prices only | Missing | 10% |
| Redesign and memo | One rule changed, cost below 130 shown, side effect on gatherers named with numbers | Redesign works, side effect vague | Target missed or no memo | 25% |

<details>
<summary>Instructor check values</summary>

- Assemble factor `(1 − 0.05) / 0.9 = 1.0556`. Ratios: 3.1667 bars, 8.4444 rivets, 2.1111 leather per helm.
- Bars per helm including rivets: `3.1667 + 8.4444 × 0.25 = 5.2778`.
- Per bar: 2.5 copper, 1.25 tin; bar cost 27.50. Per helm: 13.19 copper, 6.60 tin, 4.22 hides.
- Rivet cost 6.875; leather cost 8; helm cost `5.2778 × 27.5 + 2.1111 × 8 = 162.03`.
- Recipe card: 5 bars (3 + 8/4) at 2 copper and 1 tin each, 10 copper, 5 tin, 4 hides, cost 126. The real chain uses about 29% more gold of materials.
- Without the refund, cost is 170.56.
- Threshold `900 − 3 × 162.03 = 413.9`. `X = 0, 200, 400`: price 162.03. `X = 600`: price 100.0, loss 62.03. `X = 800`: price 33.3, loss 128.69. The floor of 20 binds from `X = 840`.
- Opportunity-cost prices: copper `1,200 / 150 = 8`, tin `1,200 / 90 = 13.3`. Starter prices (6 and 10) are below, so players will drift away from gathering until prices rise.
- A tempting redesign that just misses: smelting success `s = 1` gives bar cost 22 and helm cost `5.2778 × 22 + 16.89 ≈ 133.0`. One that works: 1 copper ore per bar instead of 2, giving bar cost `(6 + 10) / 0.8 = 20` and helm cost `5.2778 × 20 + 16.89 ≈ 122.4`. Side effect: copper demand per helm halves, from 13.19 to 6.60 ore, so copper miners lose half their helm-driven sales.

</details>
