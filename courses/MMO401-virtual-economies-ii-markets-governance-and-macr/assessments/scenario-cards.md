# MMO401 · Final project scenario cards

**Released:** week 9. **Choose one by:** the end of week 10 (proposal milestone).
**Brief:** [Final brief: agent-based economy and policy memo](final-model-and-memo-brief.md).

Each card describes an invented game. The games, currencies, items and numbers are fictional. None of them is based on a real game's data. Every card gives you:

- a short setting and the economy's rules;
- six months of report data in the [lab 13](../labs/lab13.md) format, so your `read_reports.py` runs on it unchanged;
- a price basket, and any extra data the question needs;
- what the team may and may not change;
- the producer's question, which your memo must answer.

Money is in billions of the card's currency unless a column says otherwise. The sales tax column is the stated rate times `trade_value`, rounded to one decimal. `volume_index` is real trade volume at fixed prices, 100 in month 1. Each ledger should reconcile as `money_end = money_start + faucets − sinks + R`. Finding any residual `R` is part of the job.

To use a card, save its CSV block as `cardX_reports.csv` and point `load()` at it.

---

## Card A. Starter squeeze

**Game.** *Hollowmere*, a fantasy MMO with a single world and a currency called marks. Most marks enter through monster bounties and quest rewards, and through NPC vendors who buy loot. Marks leave through a 2% sales tax on the player market, repair costs and a few fees. The game has grown steadily since a marketing push in month 1.

**What happened.** In month 2, a patch let veterans upgrade their end-game forges. The upgrade recipe uses iron ingots and tanned leather, the same materials new players need for their first set of gear. Forum threads from new players say starter gear costs "twice what the guides say".

**Six months of report data.**

```
month,active_players,money_start,faucet_bounties,faucet_quests,faucet_npc_sales,sink_sales_tax,sink_repairs,sink_other,money_end,trade_value,volume_index
1,50000,1000.0,85,35,20,80.0,20,10,1030.0,4000.0,100
2,52000,1030.0,88,37,20,83.0,20,10,1062.0,4150.0,101
3,54500,1062.0,91,39,21,86.0,21,10,1096.0,4300.0,102
4,57500,1096.0,94,41,21,89.6,21,11,1130.4,4480.0,103
5,60500,1130.4,97,43,22,93.0,22,11,1166.4,4650.0,104
6,63500,1166.4,100,45,22,96.6,22,11,1203.8,4830.0,105
```

**Two price baskets.** Prices are monthly averages in marks. Quantities are the base-month basket for each group.

| Basket | Item | Quantity | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|---|---|
| Veteran | Ship-grade alloy | 10 | 40.0 | 40.4 | 40.9 | 41.3 | 41.8 | 42.2 |
| Veteran | Elite potion | 20 | 12.0 | 12.1 | 12.2 | 12.4 | 12.5 | 12.6 |
| Veteran | Mount feed | 30 | 5.0 | 5.0 | 5.1 | 5.1 | 5.2 | 5.2 |
| Starter | Iron ingot | 20 | 2.0 | 2.2 | 2.4 | 2.6 | 2.8 | 3.0 |
| Starter | Tanned leather | 10 | 3.0 | 3.2 | 3.5 | 3.8 | 4.1 | 4.4 |
| Starter | Minor potion | 30 | 0.50 | 0.52 | 0.54 | 0.57 | 0.60 | 0.63 |

**Extra data.** New accounts (under 30 days old) held a median of 4,000 marks in every month. A new player earns about 1,500 marks an hour from quests and bounties in the starting zones.

**Constraints.** The team will not remove the forge upgrade. Anything that lowers veterans' earnings per hour needs a written reason in the patch notes.

**The producer's question.** New players say they cannot afford their first gear. Is the economy inflating, and what do we change?

<details>
<summary>Instructor notes</summary>

- Every month reconciles with `R = 0`. Net flow grows from +30.0 to +37.4 a month. Money supply is up 20.4% over the six months (1,000 to 1,203.8).
- Money per active player falls, from 20.6 million to 19.0 million marks, because players grow faster than money.
- Velocity `T / money_end` (the lab 13 definition) is 3.883, 3.908, 3.923, 3.963, 3.987, 4.012. Price level `T / Q` is 40.00, 41.09, 42.16, 43.50, 44.71, 46.00, up 15.0%. Monthly `gP` runs 2.6% to 3.2%.
- Laspeyres indices, base month 1: veteran basket 100.0, 100.8, 102.0, 103.0, 104.3, 105.1. Starter basket 100.0, 107.8, 116.7, 126.0, 135.3, 144.6.
- The starter basket costs 85 marks in month 1 and 122.9 in month 6. At 1,500 marks an hour that is 3.4 minutes of play rising to 4.9 minutes. The complaint is real but narrow. Strong memos find that the general price level is rising about 3% a month (money growth), that the starter basket is rising about 8% a month (a demand shock from the forge recipe), and treat them as two problems with two levers, for example a second source of ingots and leather or a sink sized against `M` growth.

</details>

---

## Card B. The top pulls away

**Game.** *Saltreach*, a seafaring sandbox with a currency called shells. Shells enter through bounties, quest rewards and **estate rent**. Estate rent is paid by the game each month to players who own island estates, at 0.5% of the value of goods stored in them. Only about 1% of accounts own an estate. Shells leave through a 2% sales tax, repairs and docking fees.

In this card's CSV, the column `faucet_npc_sales` holds estate rent. The other columns mean what they mean in lab 13.

**What happened.** The monetary team is pleased. The money supply has been flat for six months. The community team is not. The leaderboard of richest players now shows balances twice as large as a year ago, and guild leaders say new members "can never catch up".

**Six months of report data.**

```
month,active_players,money_start,faucet_bounties,faucet_quests,faucet_npc_sales,sink_sales_tax,sink_repairs,sink_other,money_end,trade_value,volume_index
1,80000,2000.0,62,40,48,120.0,20,12,1998.0,6000.0,100
2,79500,1998.0,61,40,50,120.0,20,12,1997.0,6000.0,100
3,79500,1997.0,60,39,52,119.6,20,12,1996.4,5980.0,99.5
4,79000,1996.4,59,39,54,119.6,20,12,2002.8,5980.0,99.5
5,79000,2002.8,58,38,56,119.2,20,12,2003.6,5960.0,99
6,78500,2003.6,57,38,58,119.0,20,12,2005.6,5950.0,99
```

**Wealth distribution.** From the monthly balance snapshot, all active accounts.

| Month | Median balance (million shells) | Top 1% share of all shells | Gini |
|---|---|---|---|
| 1 | 12.0 | 18.0% | 0.58 |
| 2 | 11.8 | 18.9% | 0.59 |
| 3 | 11.6 | 19.8% | 0.60 |
| 4 | 11.5 | 20.8% | 0.60 |
| 5 | 11.3 | 21.7% | 0.61 |
| 6 | 11.1 | 22.6% | 0.62 |

**Price basket.** Monthly average prices in shells.

| Item | Quantity | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|---|
| Rope coil | 40 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 |
| Hull plank | 20 | 8.0 | 8.0 | 8.1 | 8.0 | 8.1 | 8.1 |
| Ship's biscuit | 50 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |

**Context from the team.** In month 4 the support team refunded goods and shells to players hit by a docking bug. Support refunds are not a category in the report.

**Constraints.** Estates are a paid expansion feature. The team may change estate rent, but may not take estates away.

**The producer's question.** The money supply is flat but the richest accounts keep growing. Do we need a new sink, and what shape?

<details>
<summary>Instructor notes</summary>

- Months 1-3, 5 and 6 reconcile with `R = 0`. Month 4 has `R = 2,002.8 − (1,996.4 + 152 − 151.6) = +6.0` billion, 0.3% of `M`. That is the support refunds, an unlogged faucet. Strong diagnoses name it and ask for a refunds category.
- Faucets total 150 to 153 a month, sinks 152.0 to 151.0. Net flow drifts from −2.0 to +2.0. Money is flat within 0.3%.
- Estate rent grows from 48 to 58 a month (+21%), while bounties and quests fall. Rent is a proportional faucet paid to the top 1%. This is the week 3 policy B pattern: the money line is flat and the distribution spreads.
- Velocity is flat near 3.0, the price level `T / Q` is 60.0 to 60.2, and the basket is flat (Laspeyres 100.0, 100.0, 100.6, 100.0, 100.6, 100.6). There is no inflation to fight.
- Good answers reject a flat sink (it takes the same from everyone and raises the Gini) and propose reshaping the faucet (cap or taper estate rent) or a proportional sink on large holdings, tested with the week 3 model.

</details>

---

## Card C. Frontier shortage

**Game.** *Ironmarch*, a territorial MMO with a currency called crowns. Ore is cheap to refine at the hub and expensive at the frontier, so haulers carry refined bars from the hub to the frontier. The frontier is reached by one road through contested land. The sales tax is 3%.

**What happened.** In month 3, a border war started between two large guilds. The road became dangerous and many haulers took a longer detour. The war also opened new bounty contracts in the war zone, which pay well. Frontier players say bars cost far more than at the hub and that "nobody hauls any more".

**Six months of report data.**

```
month,active_players,money_start,faucet_bounties,faucet_quests,faucet_npc_sales,sink_sales_tax,sink_repairs,sink_other,money_end,trade_value,volume_index
1,60000,1500.0,110,40,20,135.0,25,15,1495.0,4500.0,100
2,60500,1495.0,111,40,20,135.9,25,15,1490.1,4530.0,100.5
3,61000,1490.1,118,40,20,131.4,32,15,1489.7,4380.0,97
4,61000,1489.7,120,40,20,129.0,34,15,1491.7,4300.0,95.5
5,60500,1491.7,121,39,20,127.8,35,15,1493.9,4260.0,94.5
6,60000,1493.9,121,39,20,127.2,35,15,1496.7,4240.0,94
```

**Regional data for refined bars.** The two markets follow the [week 9](../lectures/w09-regional-economies-and-logistics.md) model. Hub demand `Q = 100 − P` and supply `Q = P`. Frontier demand `Q = 100 − P` and supply `Q = P − 40`. Quantities are in thousands of bars a day. Hauler telemetry gives the other columns. `w` is what a hauler earns per hour doing something else, taken from the median bounty income of hauler accounts. Cargo `k` is 400 bars per trip, and there is no toll.

| Month | Loss chance per trip `λ` | Round trip `h` (hours) | Hauler outside wage `w` (crowns/hour) | Hub price `P_A` | Frontier price `P_B` | Bars hauled (thousand/day) |
|---|---|---|---|---|---|---|
| 1 | 0.01 | 2 | 600 | 58.21 | 61.79 | 16.42 |
| 2 | 0.01 | 2 | 600 | 58.21 | 61.79 | 16.42 |
| 3 | 0.10 | 3 | 800 | 54.29 | 65.71 | 8.57 |
| 4 | 0.10 | 3 | 1,000 | 53.57 | 66.43 | 7.14 |
| 5 | 0.12 | 3 | 1,100 | 52.71 | 67.29 | 5.42 |
| 6 | 0.12 | 3 | 1,200 | 52.36 | 67.64 | 4.72 |

**Constraints.** The war is player-driven and the team will not stop it. The team may change the road (a second route, escorts, cargo size) and may add or remove tolls.

**The producer's question.** Frontier prices sit far above the hub since the border war started. Is hauling broken, and what do we change?

<details>
<summary>Instructor notes</summary>

- All six months reconcile with `R = 0`. Money is flat (1,500 to 1,496.7). Repairs rise from 25 to 35 as the war destroys gear. Volume falls 6%, velocity `T / money_end` falls from 3.01 to 2.83, and the economy-wide price level `T / Q` stays near 45. The shortage is regional, so the national report hides it.
- With `τ = (w × h / k + f + 60λ) / (1 + λ/2)`, the transport cost is 3.58, 3.58, 11.43, 12.86, 14.58, 15.28. The observed gap `P_B − P_A` equals `τ` every month (3.58 before the war, 15.28 in month 6). Hauling is not broken. It is pricing a higher cost correctly.
- Decomposing month 6 against month 2: the wage term `w h / k` goes from 3.0 to 9.0 and the risk term `60λ` from 0.6 to 7.2. Almost half of the increase comes from haulers' better outside option, the new war bounties, which no road fix touches.
- Gains from trade `G = (20 − τ)² / 2` fall from 134.8 to 11.1. Strong memos size a lever against `τ` (for example, a larger cargo `k = 800` halves the wage term) and say who pays, including hauling corporations and war-zone gankers.

</details>

---

## Card D. The token climb

**Game.** *Lumen Coast*, a subscription MMO with a currency called gold and a **lantern token**. A token costs 15 US dollars in the store and redeems for 30 days of game time. Players who buy tokens for money sell them to other players for gold on an order book. The sales tax is 3%.

**What happened.** The token's gold price rose from 1.00 million to 1.39 million over six months, about 40%. A popular streamer called it "hyperinflation". In month 4 the team added a second use for tokens: each one can also be redeemed for a cosmetic outfit.

**Six months of report data.**

```
month,active_players,money_start,faucet_bounties,faucet_quests,faucet_npc_sales,sink_sales_tax,sink_repairs,sink_other,money_end,trade_value,volume_index
1,100000,5000.0,375,150,100,450.0,60,40,5075.0,15000.0,100
2,101000,5075.0,386,155,103,456.0,60,40,5163.0,15200.0,100.5
3,102000,5163.0,398,159,106,462.0,61,40,5263.0,15400.0,101
4,102500,5263.0,410,164,109,469.5,61,40,5375.5,15650.0,101.5
5,103000,5375.5,422,169,112,477.0,62,41,5498.5,15900.0,102
6,103000,5498.5,434,174,116,484.5,62,41,5635.0,16150.0,102.5
```

**Token market data.** Tokens sold on the market per month, gold spent on them, and the monthly gold income of the players who buy tokens (from faucet logs by account).

| Month | Tokens sold `Q` | Gold spent on tokens `B` (billion) | Income of token buyers `Y` (billion) | Average price (million gold) |
|---|---|---|---|---|
| 1 | 100,000 | 100.00 | 500.0 | 1.000 |
| 2 | 100,000 | 103.04 | 515.2 | 1.030 |
| 3 | 100,000 | 106.08 | 530.4 | 1.061 |
| 4 | 100,000 | 131.14 | 546.4 | 1.311 |
| 5 | 100,000 | 134.98 | 562.4 | 1.350 |
| 6 | 100,000 | 139.01 | 579.2 | 1.390 |

**Price basket.** Monthly average prices in gold.

| Item | Quantity | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|---|
| Health draught | 50 | 20 | 20 | 20 | 21 | 21 | 21 |
| Enchanting dust | 30 | 60 | 61 | 61 | 62 | 62 | 63 |
| Travel scroll | 20 | 25 | 25 | 25 | 25 | 26 | 26 |

**Extra data.** A median player earns 25,000 gold per hour. The store price of a token has stayed at 15 dollars.

**Constraints.** The team will not change the store price. It may change token uses, add a fee on token trades, or change faucets and sinks.

**The producer's question.** The token's gold price rose 40% in two quarters. Is that inflation, and should we act?

<details>
<summary>Instructor notes</summary>

- All six months reconcile with `R = 0`. Net flow grows from +75 to +136.5 a month, so money grows 1.5% rising to 2.5% a month, up 12.7% in six months. Faucets grow 3% a month and sinks about 1.3%.
- The week 11 model `P = B / Q` with `B = s × Y` gives `s = B / Y` = 0.20 for months 1-3 and 0.24 for months 4-6. The token price rise splits into income growth (579.2 / 500 = 1.158) and the new token use (0.24 / 0.20 = 1.2). `1.158 × 1.2 = 1.39`.
- General prices rose far less. The price level `T / Q` goes from 150.0 to 157.6 (+5.0%). The basket's Laspeyres index is 100.0, 100.9, 100.9, 103.3, 103.9, 104.8.
- Hours of play per token at 25,000 gold an hour rise from 40.0 to 55.6. The implied dollar value of an hour falls from 0.38 to 0.27.
- Strong memos say the token climb is mostly a demand shift that happened once (month 4) on top of a steady money-growth problem that the faucet line shows (faucets growing 3% a month against sinks at about 1.3%). They size a response to the money growth and treat the token use as a separate design choice.

</details>
