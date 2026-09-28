# MMO304 · Lab 12: Economy telemetry

**Week:** 12 · **Time:** 2 hours in lab plus about 4 hours at home · **Weight:** the telemetry lab (20% of the course grade)

## Objective

Turn raw ledger and market data from a fictional MMO server into the dashboard panels from [week 12](../lectures/w12-economic-telemetry-and-dashboards.md), section 5. Then use the panels to find and explain three incidents hidden in the data, and write the incident report a live team would act on.

## Starter materials

- Python 3 with pandas (or numpy) and matplotlib. A spreadsheet works for steps 1-4 but is slow for the rest.
- [`lab12-ledger.csv`](lab12-ledger.csv): 56 days of the server's currency ledger, aggregated per day and per source. 392 rows. Columns:
  - `day`: 1 to 56.
  - `active_players`: accounts that logged in that day, as the game counts them (this count does not exclude bots).
  - `source`: the ledger reason code. Faucets are `quest_rewards`, `mob_loot` and `vendor_sell`. Sinks are `repairs`, `ah_fees`, `travel` and `npc_purchases`.
  - `kind`: `faucet` or `sink`.
  - `gold`: total gold created or destroyed by that source that day.
  - `top1pct_share`: the share of that day's gold for that source that went to (or came from) the top 1% of accounts for that source.
- [`lab12-snapshots.csv`](lab12-snapshots.csv): 56 rows, `day` and `snapshot_supply_end_of_day`, the total gold held by all characters at the end of each day, read from the game database rather than the ledger.
- [`lab12-prices.csv`](lab12-prices.csv): 8 weeks of auction house data for five goods. 40 rows. Columns `week`, `item`, `avg_price` (mean price of that good that week) and `quantity` (units sold). Goods: `health_potion`, `iron_bar`, `silk_cloth`, `mount_feed`, `epic_blade`.
- Known facts about the server: total gold held on the morning of day 1 was 400,000,000. Patch notes list one content update on day 15 ("new zone, mob loot tables raised about 15%") and one on day 29 ("new raid tier, epic blade recipe needed for attunement"). No other patches are documented.
- Week 1 of the price file covers days 1-7, week 2 covers days 8-14, and so on.

The data are synthetic, generated for this course. They do not come from any real game.

## Steps

1. **Supply and reconciliation.** Compute daily faucets, sinks, net flow and the ledger-predicted supply from the starting 400,000,000. Compare it with the snapshot file each day. Plot supply, net flow and the reconciliation gap over the 56 days, and apply the week 12 alert rule (gap above 0.1% of supply).
2. **Faucets and sinks panel.** A stacked chart of gold per day by source, faucets above zero and sinks below. Add the sink/faucet ratio as a line. Mark the two documented patches.
3. **Per player.** Compute supply per active player and each source's gold per active player. Find at least one source whose per-player value changes for a reason that has nothing to do with that source. Explain it.
4. **Concentration panel.** Plot `top1pct_share` for each faucet over time. Apply the week 12 alert rule (share doubles against its 28-day average, or use the previous 14 days if fewer than 28 exist). List every day that fires.
5. **Price panel.** From the price file, compute the weekly average transaction price across all goods, the Laspeyres index with week 1 as base, and the Paasche index. Plot the average (rescaled to 100 at week 1) and both indices on one chart.
6. **Find the incidents.** There are three undocumented incidents in the data. For each, give the days it covers, the panel that shows it first, the numbers that prove it, and the most likely cause.
7. **Estimate the damage.** For each incident, estimate how much extra gold entered the economy (or failed to leave it) compared with the days just before it.

## Deliverable

1. Your notebook or script, runnable from the three CSV files.
2. A dashboard of the five panels from steps 1-5, one page, each with its alert rule written under it.
3. An incident report of 600-900 words, written for the live producer. One section per incident with dates, evidence, estimated gold impact, cause, and a recommended action with an owner. End with one change to the telemetry itself that would have caught the incidents sooner.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Supply and reconciliation | Ledger supply correct to the gold, gap computed daily, alert days listed | Minor arithmetic error or missing plot | Wrong method | 15% |
| Dashboard panels | All five panels correct, readable, patches annotated, alert rules written | One panel missing or unlabelled | Two or more missing | 25% |
| Denominator analysis | Identifies a per-player change caused by the denominator and explains it with numbers | Notices it without numbers | Missing | 10% |
| Price indices | Average, Laspeyres and Paasche correct, with a correct reading of week 5 | Numbers correct, reading weak | Wrong formulas | 15% |
| Incidents found | All three found with correct dates, evidence and cause | Two found, or three with weak evidence | One or none | 20% |
| Report and damage estimates | Clear owner and action per incident, estimates with method shown, a sound telemetry change | Actions vague or estimates missing | Unusable for a producer | 15% |

<details>
<summary>Instructor check values</summary>

Values come from the files as shipped (seeded generator, seed 1204). Small rounding differences are fine.

- Supply: day 1 net +4,449,262, end of day 1 supply 404,449,262. End of day 56 ledger supply 873,866,185; snapshot 885,866,185.
- Phase averages per day (faucets / sinks / net, in millions): days 1-14 37.99 / 34.90 / +3.09; days 15-28 43.85 / 38.36 / +5.49; days 29-42 53.07 / 38.75 / +14.32; days 43-46 43.92 / 38.40 / +5.52; days 47-56 44.35 / 31.23 / +13.12. Sink/faucet ratio 0.92, 0.87, 0.73, 0.87, 0.70.
- Documented change, day 15: active players rise from about 20,000 to about 22,000 and mob loot per active player from about 703 to about 806. Top 1% shares stay near 6%. This is healthy.
- Incident 1, bot wave, days 29-42: mob loot per active player jumps to about 1,140 and its `top1pct_share` averages 0.37 (from 0.06). Active players rise by about 1,500 with no patch to explain it. Repairs rise slightly (bots repair too). It ends on day 43, consistent with a ban wave. Extra net inflow is about 8.8 million per day over the 14 days, roughly 123 million in total.
- Incident 2, broken auction fee sink, days 47-56: `ah_fees` falls from about 350 to about 17 gold per active player with no patch note, and the sink/faucet ratio drops to 0.70. Top 1% shares are normal, so this is a fee bug, not farming. Missing sink is about 7.3 million per day, about 73 million over 10 days.
- Incident 3, duplication exploit, days 36-39: the snapshot exceeds the ledger by 2,950,000 at the end of day 36 (about 0.47% of supply, so the alert fires that day), and the gap grows to 12,000,000 by day 39, then stays flat. No ledger source moves, so the gold was never logged. It overlaps the bot wave, which is why students who only look at faucet panels miss it. The flat gap after day 39 means the exploit was closed, but the 12 million was not removed.
- Step 3 denominator check: during days 29-42, `ah_fees` per active player dips from about 352 to about 329 because bots are counted as active. No player behavior changed. Students who call this a drop in trading have been fooled by the denominator.
- Price side: average transaction price is about 19.7-20.0 in weeks 1-4 and jumps to 29.79 in week 5 (+51%) because epic blade sales quadruple with the new raid. Laspeyres is 105.0 in week 5 and 110.8 in week 6, then holds near 110. Paasche is 103.6 in week 5 and 107.8 in week 6. So real commodity inflation of about 11% happened in weeks 5-6, which is the bot wave's gold reaching prices. The average overstates it four- to five-fold in week 5.

</details>
