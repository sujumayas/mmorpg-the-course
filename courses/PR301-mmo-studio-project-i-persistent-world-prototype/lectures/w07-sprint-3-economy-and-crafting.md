# PR301 · Week 07 — Sprint 3: Economy and Crafting

**Why this matters:** In two weeks your world will run for a whole weekend with nobody watching. Whatever currency your design creates in that time stays in the world. A single-player game can rebalance its loot table in a patch. A persistent world has to live with every coin already minted, so you plan the money before you build it, and you build the logging that tells you whether the plan held.

**You will be able to:**
- Plan sprint 3 from a focus-factor range, with the week 6 performance story and a bug reserve taken off the top.
- Design a currency ledger in which every change to a balance has a reason code, so that the money supply can be reconciled.
- Write a per-player-hour faucet and sink budget, compute net income, hours to a target purchase and the weekend's money supply, and tune one line into a target band.
- Check every crafting recipe for the arbitrage that turns crafting into a hidden faucet.

**Before class:** Reread [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucets, sinks and transformations) and [MMO304 week 7](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w07-crafting-chains-and-gathering-professions.md) (crafting chains). Reread your week 2 persistence map and the week 5 camp faucet line. Bring the tagged sprint 2 build for the review that opens the session, the sprint 1 focus factor, the sprint 3 input list drafted in week 6 and your current loot tables. The sprint 2 focus factor is measured in that review.

**Prerequisites from earlier courses:** [MMO304 week 4](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (money per capita and prices). [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (what an economy dashboard shows). [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (item ownership). [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) (transactions). [DB201 week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (event design). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (estimation ranges).

---

## 1. What sprint 3 has to prove

The *Saltmarsh* sprint 3 goal reads: "Players earn copper from wolves and quests, spend it on repairs, salves, crafting and the market, send it to each other, and every change to any balance is logged with a reason." The last clause is the part teams drop, and it is the part weeks 9 and 10 depend on.

Sprint 3 also has to leave the world ready to run unattended. Your week 2 persistence map already says currency and items are write-through, one transaction per trade, loot or craft. Sprint 3 is where that promise meets real code: loot, vendor sales, trades, mail, crafting and market purchases. [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) and [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) showed how a transfer that is correct on its own can duplicate value when two run at once, or when the server dies between two writes. A dupe on a class playtest is a funny story. A dupe on a 48-hour weekend is a ruined economy that you will take apart in week 10.

## 2. Capacity before content

Plan the sprint in estimated hours, as in week 3, but now with two measured focus factors: 0.46 for sprint 1 and 0.54 for sprint 2. Plan with the range, not the average. Nobody on *Saltmarsh* is away this sprint, so each of the seven people has 13 available hours and the team has 91.

```
capacity, low  = 0.46 × 91 = 41.9 hours of estimated work
capacity, high = 0.54 × 91 = 49.1 hours
```

Two things come off the top before any economy story is considered.

- **Week 6's grid story**, 6 hours for Ana. It protects the 100-bot load test, so it goes first.
- **A bug reserve** of 20% of each forecast: 8.4 hours at the low end, 9.8 at the high end. Sprint 2 found bugs at a steady rate, and sprint 3 will too.

```
committed = 41.9 − 6 − 8.4 = 27.5 hours
stretch   = 49.1 − 6 − 9.8 = 33.3 hours
```

Rank the economy stories and draw the commitment line at 27.5 hours. Stories between 27.5 and 33.3 are stretch, written down as stretch at planning, not found to be late on the last Friday. Then run the week 3 per-person load check. The ledger and the market both land on Chen, and one person at 1.4 is a plan that fails even if the total fits.

## 3. The ledger rule

Every change to a currency balance goes through one server function. That function changes the balance and writes a **ledger event** in the same database transaction, the write-through transaction your persistence map already requires. A ledger event has at least these fields:

| Field | Example |
|---|---|
| `event_id`, `server_seq` | a unique ID and a per-server sequence number with no gaps |
| `time` | server time in UTC |
| `character_id` | whose balance changed |
| `delta` | +4 or −12, in whole copper |
| `reason` | `F_LOOT`, `S_REPAIR`, `T_MAIL` and so on |
| `ref` | the wolf, recipe, trade, mail or listing that caused it |
| `balance_after` | the balance once the change applied |

Reason codes come in three kinds. **Faucets** (`F_`) create currency. **Sinks** (`S_`) destroy it. **Transfers** (`T_`) move it between characters and always come in pairs that sum to zero. A market sale at 100 copper with a 5% cut is three lines: the buyer's −100 (`T_MARKET`), the seller's +95 (`T_MARKET`) and a sink of −5 (`S_MARKET_CUT`) against the seller. Written that way, the ledger answers one question exactly:

```
M_end − M_start = Σ faucets − Σ sinks
```

where `M` is the **money supply**, all currency anywhere in the world. That means character balances plus copper in mail, in market escrow and in guild banks. If the two sides differ, something changed a balance without going through the function, or saved one side of a transfer and not the other. Week 10 turns on this equation.

Three design rules keep the ledger useful.

1. **One reason code per budget line.** The budget in section 4 and the ledger use the same codes, so actuals can sit next to plans.
2. **No silent grants.** Starter copper, GM gifts and test commands are faucets too. Give them codes.
3. **Log the amount actually applied.** If a cut is rounded down on the server, log the rounded value, not the formula's result.

## 4. Worked example: the weekend money budget

### The hook

Every month, EVE Online's developer publishes a Monthly Economic Report. Among its standard charts are the ISK faucets and sinks: how much currency entered the game and how much left, broken down by source. Players read it the way traders read central bank minutes. A report like that is only possible if every currency movement is recorded with a reason. Your world can have the same chart after one weekend, if you plan the lines now and log them from the first day.

### The model

Budget currency per **player-hour**, one hour of one player online, because both faucets and sinks scale with play time. For each reason code `i`, estimate the average rate `f_i` (faucets) or `s_i` (sinks) in copper per player-hour. Then

```
net income per player-hour   n = Σ f_i − Σ s_i
sink ratio                   r = Σ s_i / Σ f_i
hours to afford price G      h_G = G / n
weekend money supply         M = M_start + H × n
money per player             m = n × hours per player
```

where `H` is the expected player-hours in the weekend. Rates come from sprint 2 bot runs where you have them (kills and deaths per hour) and from design estimates where you do not. Mark which is which.

### Numbers you can check

The *Saltmarsh* pillars say copper should feel scarce on the first weekend. The first real purchase is a guild charter at 600 copper, and a player should reach it after 5.0 to 7.5 hours of play. That is a target net income of 80 to 120 copper per player-hour.

The first draft of the budget. The loot line comes from week 5: with dynamic respawn, a hunter is not kept waiting and kills two wolves a minute. Bot runs show players hunt about 40% of their online time.

| Code | Kind | Basis | Copper per player-hour |
|---|---|---|---|
| `F_LOOT` | faucet | 0.4 × 120 kills per hunting hour = 48 kills × 5 copper (bot runs, week 5) | 240 |
| `F_QUEST` | faucet | quest rewards, averaged over a 6-hour player | 60 |
| `F_VENDOR` | faucet | selling pelts and reeds to NPC vendors | 50 |
| `S_REPAIR` | sink | 2.5 deaths per hour (bot runs) × 20, since Saltmarsh gear decays | 50 |
| `S_CONSUMABLE` | sink | salves and food from vendors | 60 |
| `S_CRAFT_FEE` | sink | 2 crafts per hour average × 20 | 40 |
| `S_TRAINING` | sink | recipe and skill purchases, averaged | 30 |
| `S_MARKET_CUT` | sink | 5% of 300 copper traded per hour | 15 |

```
Σ f = 240 + 60 + 50            = 350
Σ s = 50 + 60 + 40 + 30 + 15   = 195
n   = 350 − 195                = 155 copper per player-hour
r   = 195 / 350                = 56%
h_G = 600 / 155                = 3.9 hours
```

The charter arrives more than an hour too early. Model three single-line fixes:

| Option | Change | New `n` | `h_G` | In band? |
|---|---|---|---|---|
| A | Wolf drop 5 → 4 copper | 107 | 5.6 h | yes |
| B | Repair cost 20 → 40 per death | 105 | 5.7 h | yes |
| C | Market cut 5% → 15% | 125 | 4.8 h | no |

Option A removes `48 × 1 = 48`. Option B adds `2.5 × 20 = 50` of sink. Option C adds `0.10 × 300 = 30`, which is not enough.

A and B land in almost the same place, but they are not the same design. A charges everyone equally for every hour of hunting. B charges the players who die, and in the first weekend those are the new players. [MMO304 week 14](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w14-designing-an-economy-from-scratch.md) warns that flat charges like repair bills fall hardest on new players. C taxes the thing you most want to observe, player trade, and still misses. *Saltmarsh* takes option A.

Now the weekend. The week 9 plan expects about 33 players averaging 3.75 hours, so `H = 33 × 3.75 = 123.75`, about 124 player-hours:

```
M = 0 + 123.75 × 107  = 13,241 copper
m = 3.75 × 107        = 401 copper per player
```

The average player ends the weekend with about 400 copper, short of the 600-copper charter. Only players past 5.6 hours can found a guild alone. Is that a bug? Only if the design wants guilds on day one. *Saltmarsh* wants them for the sprint 4 social systems, so Dee keeps the price and makes the charter fundable by several founders, who send copper by mail. That also puts `T_MAIL` under real load, which matters in week 10.

### A visual you can move

No separate interactive ships this week. The faucet and sink simulator from [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) already shows how per-hour sinks slow drift while stock-based sinks cap it. Set its hours per day and faucet sliders to your budget and watch money per capita over the first days. The week 5 camp interactive shows where the loot line comes from. The lab 07 checker computes your own numbers.

### Cross-game recognition

Rewrite three shipped sinks as lines in the same table.

- **World of Warcraft's auction house** takes a 5% cut of the winning bid, and the seller also pays a deposit that is lost if the item does not sell (Warcraft Wiki, current retail rules). In our table that is `S_MARKET_CUT` at 5% of trade volume, plus a second line, `S_LISTING`, that scales with failed listings.
- **Old School RuneScape's Grand Exchange** charged a 1% tax from 9 December 2021 and 2% from 29 May 2025, capped per item, with most of it removed from the game and a small part used to buy and delete selected items (OSRS Wiki). Same line, a different rate, and a second use of the money.
- **EVE Online's Monthly Economic Report** is the whole table at once, with faucets and sinks by source, published each month.

All three are one idea. Money enters and leaves through named lines, each line scales with something players do, and a designer can move one line while watching the others.

### Eyes-open judgment

- **Per-hour budgets hide one-time lines.** `F_QUEST` and `S_TRAINING` are front-loaded. A new player's first hour nets far more than 107. Look at hour one separately if early wealth matters to your design.
- **Averages hide the tail.** A player on for 15 hours has 1,600 copper, and the players who play most will own most of the money. That is normal, and it is also where a dupe hides. Week 10 looks at individual characters.
- **Estimated rates are the weakest numbers.** Kills and deaths per hour came from bots. Crafts per hour and trade volume are guesses. The weekend will replace them with measurements, which is the point of logging by reason code.
- **Stock-based sinks do something per-hour sinks cannot.** A tax on trade volume grows with the money in circulation. MMO304 week 3 shows that only such sinks put a ceiling on per-capita money. A 48-hour alpha is too short for the difference to show, but your final economy design should account for it.

### Check yourself

1. With option A in place, the team adds a daily login reward of 30 copper. A typical player plays 2 hours on each of 2 days. What is their effective net income per player-hour?
2. The market cut stays at 5%, but players trade 900 copper per hour instead of 300. What happens to `n` and `h_G`?
3. Fay proposes cutting `F_VENDOR` to zero by making pelts unsellable. Compute `h_G`. What does the team lose besides copper?

<details>
<summary>Answers</summary>

1. Login rewards add `2 × 30 = 60` copper over 4 hours, 15 per player-hour. Effective `n = 107 + 15 = 122`, and `h_G = 600 / 122 = 4.9` hours, just out of the band. A reward per day is a faucet per day, not per hour, so it matters most to light players.
2. `S_MARKET_CUT` becomes 45, so `n = 107 − 30 = 77` and `h_G = 7.8` hours, just out of the band on the slow side. Heavy trading is what you want to test, so the fix is to lower the cut or accept the slower charter. Do not suppress the trade.
3. `n = 107 − 50 = 57`, `h_G = 600 / 57 = 10.5` hours, far out of the band. The team also loses a reason to hunt beyond the drop and a reason to visit the vendors.

</details>

## 5. Crafting is a transformation, and it can leak

A recipe turns inputs and a fee into an output. If the output can be sold to an NPC vendor, the recipe is also a possible faucet. Players will find any recipe where

```
vendor_sell(output) > fee + Σ vendor_sell(inputs)
```

and craft it in a loop. Gathered inputs count at their vendor sell value, which is often zero. That is exactly why gathered-input recipes leak, and *Saltmarsh*'s reeds and salt are both gathered. Check every recipe against this inequality before the freeze, and check again whenever a recipe is added. Where a recipe breaks it, lower the output's vendor price or make it unsellable. [MMO304 week 7](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w07-crafting-chains-and-gathering-professions.md) covers the design side of crafting chains. Lab 07 checks the inequality for you.

## Studio session plan

Week 7 meeting, 3 hours. The sprint 2 review opens it, then sprint 3 planning, with an instructor visit to each team.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:45 | Sprint 2 review, paired teams: goal answered yes or no on the tagged build, a 100-bot run in the worst-case layout, done hours, focus factor, retrospective (see week 6) | Sprint 2 review record, `f` = 0.54 for *Saltmarsh* |
| 0:45-0:55 | Sprint 3 goal drafted in one sentence, including the ledger clause | Goal on the board |
| 0:55-1:10 | Capacity: focus-factor range, week 6 story, bug reserve, per-person load check | Committed and stretch lines in hours |
| 1:10-1:40 | Ledger design: reason codes, event schema, every place currency can live, the single balance function | Schema and code list in the TDD |
| 1:40-1:50 | Break | |
| 1:50-2:20 | Budget: fill `budget.csv`, run the checker, tune one line into the band | Lab 07 part A passing |
| 2:20-2:35 | Recipe check against the arbitrage inequality | Lab 07 part B passing |
| 2:35-2:52 | Stories written, estimated in hours and ranked; commitment line drawn | Sprint 3 backlog |
| 2:52-3:00 | Instructor sign-off on goal, capacity and ledger schema | Signed planning record |

## Deliverables

The sprint 2 review record and input list are due in this session (see week 6). The items below are due at the end of the meeting, updated within 24 hours:

1. **Sprint 3 plan**: the goal, the capacity calculation with both focus factors, committed and stretch stories with estimates, and the per-person load check.
2. **Economy budget and recipe check** in the lab 07 format ([`labs/lab07.md`](../labs/lab07.md)), passing `check_budget.py`.
3. **Ledger design**: reason code list, event schema and the list of every place currency can live, added to the technical design document.
4. By the week 8 mid-sprint session: the ledger live in the build, with a query that computes money supply and a query that sums the ledger by reason code.

## Common failure modes

- **The ledger is a sprint 4 story.** Then the alpha weekend runs without it and week 10 has nothing to reconcile. The ledger is part of every economy story's definition of done.
- **A transfer that skips the persistence map.** Trade was built write-through, but mail was built as "change the balance in memory, save later" to fit the sprint. One path is enough to break the equation.
- **Logging the formula instead of the result.** The cut is `0.05 × price` in the log and `floor(0.05 × price)` in the balance. Small differences add up to a residual you cannot explain.
- **Forgetting where currency lives.** A money supply computed from character balances alone misses mail, escrow and guild banks, and a correct ledger then looks broken.
- **Tuning three lines at once.** Change one line, recompute, and write down why. Otherwise nobody can say which change did what.
- **Committing the stretch line.** The bug reserve gets spent on stories and the last two days of the sprint are all bug-fixing.

## Review checklist

The instructor checks at the meeting, at the week 8 mid-sprint session and at the sprint 3 review at the start of week 9:

- [ ] The sprint goal includes the ledger, and capacity uses both focus factors with the week 6 story and a bug reserve taken first.
- [ ] Every faucet and sink in the design has a reason code, and the budget uses the same codes.
- [ ] Starter copper, GM commands and any login rewards have faucet codes.
- [ ] Transfers (trade, mail, market) are logged as pairs that sum to zero, with cuts as separate sink lines, and every transfer path follows the persistence map.
- [ ] `check_budget.py` prints `PASS`: net income in the target band, no recipe breaks the arbitrage inequality, every line has a logged event name.
- [ ] Money supply is defined over every place currency can live.
- [ ] By week 8: the build writes ledger events and the two queries run.

## Sources

- EVE Online, "Monthly Economic Reports" news category (eveonline.com, accessed September 2026); the report's format, including sinks and faucets, as described in the MMO304 week 12 sources (June 2024 edition). https://www.eveonline.com/news/t/monthly-economic-report
- Warcraft Wiki, "Auction House" (accessed September 2026, current retail rules). The house takes 5% of the winning bid; deposits depend on vendor sell price and auction length and are lost if the item does not sell. https://warcraft.wiki.gg/wiki/Auction_House
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Tax introduced at 1% on 9 December 2021, raised to 2% on 29 May 2025, capped per item; most is removed from the game and a small part funds the item sink. https://oldschool.runescape.wiki/w/Grand_Exchange
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Faucets, sinks and money supply.
- The *Saltmarsh* team, its focus factors, rates, prices and the guild charter target are invented for teaching, continuing the example from weeks 1 to 6.
