# MMO401 · Week 04 — Monetary Policy Tools in Games

**Why this matters:** In MMO304 you learned to read inflation off a dashboard. Now you are the one who has to act on it. Every lever you own (drop rates, fees, taxes, luxury goods, buying items back) moves money per player at a different speed and hits a different group of players. Pull the wrong one, or pull the right one on stale data, and you make the problem worse while the patch notes say you fixed it.

**You will be able to:**
- Compute the steady state and half-life of money per player under a transaction tax, and use them to predict how long a tax change takes to show up in prices.
- Compare faucet cuts, flat sinks, proportional sinks and one-off sinks by what each does to the level and the slope of money per player.
- Simulate a feedback rule for setting a tax rate, and predict when a data lag turns it into an oscillation.
- Critique a proposed intervention by naming its instrument, its target, its lag and who pays for it.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters on money and monetary policy within the course's assigned range, ch. 9-12. Reread MMO304 weeks 3 and 4 and have their steady-state formulas at hand.

**Prerequisites from earlier courses:** [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (flow sinks vs stock sinks, the trade-tax term `τ × v × M`). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (the equation of exchange and the steady state). [GD102 week 4, negative feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (half-life arithmetic). This course's agent-based modeling weeks, [MMO401 weeks 2 and 3](../syllabus.md), give you the simulation habit this lecture assumes.

**Interactive:** [The tax lever](../examples/w04-tax-lever.html). Keep it open during sections 2 and 3.

---

## 1. From diagnosis to policy

MMO304 gave you a diagnosis kit. Money per player `m` drifts up when net faucets beat sinks. Prices follow `m` when velocity and output stay put, which is the equation of exchange `M × V = P × Q` from Irving Fisher's 1911 book, rewritten per player. A stock sink, one that takes a share of the money that exists, gives the economy a ceiling. A flow sink, one that takes a fixed amount per action, only changes the slope.

This week you stop describing and start steering. A real central bank talks about three things, and you should too.

- The **target** is the number you want to hold. For a game it is usually a price index or money per active player. Sometimes it is a specific price, such as the gold price of a subscription token (week 11).
- The **instrument** is the lever you actually move. You cannot set `m` directly. You set a drop rate, a fee, a tax, or the price of something players want to buy from an NPC.
- The **lag** is the time between moving the lever and seeing the target move. It has two parts. The economy's own response time, and the time it takes you to notice, which is your telemetry delay plus your patch cycle.

The rest of this lecture is about matching instruments to targets and respecting lags.

### The instruments you own

Almost every tool a game economist has falls into one of five groups. You met most of them as bookkeeping categories in MMO304. Here they are as policy levers, sorted by what they act on.

| Instrument | Examples | What it changes in `m(t+1) = m(t) + g − σ × m(t)` |
|---|---|---|
| Faucet rate | gold drops, quest rewards, NPC bounties, vendor buy prices | `g`, the slope |
| Flat sink | repairs, travel fares, fixed fees per action | `g`, the slope |
| Proportional sink | trade tax, auction cut, upkeep as a share of wealth | `σ`, the ceiling and the speed |
| One-off sink | a limited luxury item, an event with a big entry fee | `m` itself, once |
| Open-market operation | the developer buys items with gold, or sells items for gold | `m` and the item supply at the same time |

Here `g` is net faucet per player per day (faucets minus flat sinks) and `σ` (sigma) is the share of each player's money removed per day by proportional sinks. When the proportional sink is a tax on trade, `σ = τ × v`, where `τ` (tau) is the tax rate and `v` is **velocity**, the share of the money supply that passes through the taxed market each day. This is the same notation as MMO304 week 3.

We assume a closed server in this lecture, meaning no newcomers diluting the average and no quitters carrying money away. MMO304 week 4 showed that growth hides inflation. A closed server is the case that forces you to use policy, so it is the right one to study.

## 2. Worked example: how fast does a tax work?

### The hook

On 9 December 2021, Old School RuneScape added a 1% tax to most Grand Exchange sales. On 29 May 2025, Jagex doubled it to 2%, still capped at 5 million coins per item. Most of what the tax collects is deleted. Part of it pays for an **item sink** that buys selected expensive items from players each week and deletes them. According to the Old School RuneScape Wiki, Jagex's Mod Ash reported in May 2025 that the item sink had removed about 5.73 trillion coins' worth of items since launch.

That sounds enormous. So here is the question a player might ask on the forums. If you double a tax, do prices halve? And if they do, when?

The answer surprises most students. A trade tax of a few percent does set a ceiling on money per player, and doubling it halves that ceiling. But at realistic trading volumes, it takes years to get there. A tax is a slow lever. That is not a flaw you can patch out. It follows from the model in one line.

### The model

One update per day, per player, on a closed server:

```
m(t+1) = m(t) + g − σ × m(t)          with σ = τ × v
```

- `m(t)` is money per player on day `t`.
- `g` is net faucet per player per day, after flat sinks.
- `τ` is the tax rate on trades, `v` is daily velocity, and `σ = τ × v` is the share of each player's money the tax removes per day.

Set `m(t+1) = m(t)` to get the steady state, and solve the recurrence to get the path:

```
m* = g / σ = g / (τ × v)
m(t) = m* + (m(0) − m*) × (1 − σ)^t
half-life = ln 2 / −ln(1 − σ) ≈ 0.693 / σ
```

The first line says where money per player stops. The second says how it gets there. The gap between `m` and `m*` shrinks by the same factor `(1 − σ)` every day, which is exponential decay. The third line is the time for half the gap to close, which you computed for XP curves in MA101 week 4.

Look at the half-life. It depends only on `σ`. A tax that removes 0.1% of the money supply per day has a half-life of about 693 days, whatever the faucets are. That is the whole lesson. Everything else is numbers.

### Numbers you can check

The numbers below are invented but plausible. Players on our server net `g = 40` gold per day after repairs and fares. They spend `v = 5%` of their money through the market each day, so the average coin changes hands once every 20 days. They start at `m(0) = 10,000`. Prices are proportional to `m`, so you can read a 20% rise in `m` as 20% inflation.

| Policy | `σ = τv` per day | Steady state `m*` | Half-life | `m` at day 90 | Day 365 | Day 730 | Day 1,095 |
|---|---|---|---|---|---|---|---|
| A. No tax | 0 | none | none | 13,600 | 24,600 | 39,200 | 53,800 |
| B. 1% tax | 0.0005 | 80,000 | 1,386 days | 13,081 | 21,680 | 31,411 | 39,518 |
| C. 2% tax | 0.0010 | 40,000 | 693 days | 12,583 | 19,178 | 25,548 | 29,969 |
| D. 5% tax | 0.0025 | 16,000 | 277 days | 11,210 | 13,594 | 15,035 | 15,613 |
| E. No tax, faucet cut 25% (`g = 30`) | 0 | none | none | 12,700 | 20,950 | 31,900 | 42,850 |
| F. 5% tax and `g = 30` | 0.0025 | 12,000 | 277 days | 10,403 | 11,198 | 11,678 | 11,871 |

Check one row by hand. For policy C, `m* = 40 / 0.001 = 40,000`. After 365 days the gap has shrunk by `0.999^365 ≈ 0.694`. The starting gap is `10,000 − 40,000 = −30,000`, so `m(365) = 40,000 − 30,000 × 0.694 = 19,178`.

Read the table as a designer. Going from 1% to 2% (B to C) does halve the ceiling, from 80,000 to 40,000. But after a full year the two servers differ by only 2,500 gold per player, about 13%. The ceiling is years away. A small tax is mostly a statement about year three.

Policy D gets close to its ceiling in about three years. Policy E, the faucet cut, beats a 1% tax for the first 634 days and loses after that, because it bends the slope immediately but never adds a ceiling. On day 1 the faucet cut removes 10 gold per player and the 1% tax removes only 5. The tax's bite grows with `m`, the faucet cut's does not. Policy F combines a slope lever and a ceiling lever. It is the only row that is stable within a year.

### What a one-off sink buys you

Now add a one-off sink to policy D on day 0. Say a new luxury mount, priced so that the average player spends 3,000 gold on it. Money per player drops from 10,000 to 7,000 at once. Under policy D the gap to `m*` is now 9,000 instead of 6,000, and it closes with the same 277-day half-life. After one half-life the one-off sink's effect has halved. After three years (1,095 days, about four half-lives) the server is at 15,419 instead of 15,613, a difference of about 1%.

Under policy A, with no ceiling, the same mount pushes the whole line down by 3,000 forever. That is 75 days of net faucet. Either way, a one-off sink moves the level once and changes neither the slope nor the ceiling. It buys time. It does not buy stability.

### The visual

Open the interactive. The top view plots `m(t)` over three years for the policy you set. The steady state appears as a dashed line and the half-life as a marker on the curve. Drag the tax slider from 1% to 2% and watch the dashed line drop by half while the solid curve over the first year barely moves. That mismatch is the insight. Then drag the velocity slider. Doubling `v` does exactly what doubling `τ` does, because only the product `σ` matters. Now switch the lever selector to "faucet cut" and see the line tilt immediately with no ceiling at all.

### Cross-game recognition

Each case below is the same equation with a different instrument.

**Old School RuneScape (Grand Exchange tax, 1% from December 2021, 2% from 29 May 2025).** A proportional sink, `σ = τ × v`, with `τ` doubled in 2025. The 5 million coin cap per item means the tax stops being proportional on the most expensive trades. For an item worth more than 250 million coins, the tax is flat. Items priced below 50 coins pay nothing, because 2% rounds down to zero. So the real `σ` is below `τ × v` at both ends of the price range. The item sink is an open-market operation, covered in section 4.

**EVE Online (market sales tax, release 22.02, 12 March 2025).** CCP raised the base sales tax on market sales from 4% to 7.5%. The Accounting skill cuts it by 11% per level, so a character with Accounting V pays `7.5% × (1 − 0.55) = 3.375%`. The tax is paid to NPCs and leaves the economy, so it is a proportional sink. Because skilled traders pay less than half the base rate, the effective `τ` depends on who does the trading, and a lot of volume runs through skilled traders. When you estimate `σ` for EVE, weight the rate by volume, not by player count.

**World of Warcraft (auction house, retail).** The auction house keeps 5% of each winning bid. It is also a proportional sink, and at 5% it sits near policy D in our table. The difference from EVE and Old School RuneScape is that the rate has been stable for a very long time. WoW's economy is steered mostly with faucets and flat sinks (row E), plus a steady supply of luxury goods sold by NPCs (one-off sinks, repeated every expansion).

**A real central bank.** A central bank does not tax money. It sets a short-term interest rate, and the economy responds over months to years. Milton Friedman's 1961 paper on monetary lags argued that the lag between a policy move and its effect is long and hard to predict, and that this makes aggressive fine-tuning risky. Your tax lever has the same property for a simpler reason. Its half-life is `0.693 / σ`, and `σ` is small.

Four settings, one model. When someone proposes a sink, write it as a change to `g`, to `σ`, or to `m` once. Then you know whether it changes the slope, the ceiling or the level.

### Design judgment, eyes open

- **Use proportional sinks to set where money ends up, and faucets to set how fast it gets there.** A tax sets `m*` but moves slowly at single-digit rates. A faucet change acts at once but sets no ceiling. Most healthy packages use both, which is policy F.
- **Small taxes are for year three.** If your problem is inflation this quarter, a 1% to 2% tax change is the wrong tool. Say so in the patch notes, or players will read the next price rise as proof the change failed.
- **Velocity is part of your instrument.** `σ = τ × v`, and `v` responds to `τ`. Raise the tax too far and players trade less, so `σ` rises less than you planned and fewer trades happen at all. Week 7 measures that trade-off with an order-book simulation. For now, treat `v` as fixed only for small changes.
- **Know who pays.** A trade tax falls on traders, who are usually richer and more active than average. A faucet cut falls on everyone who farms, including new players. A one-off luxury sink falls on those who want the item. The same drop in `m` has very different winners and losers.
- **Caps and exemptions change the model.** A per-item cap makes the tax regressive at the top (the richest trades pay the smallest share). Exemptions on cheap goods protect new players but lower `σ`. Put both in your model before you promise a number.

### Check yourself (worked example)

1. A server has `g = 60` and `v = 4%`. What tax rate holds `m*` at 15,000? How long until half the gap closes?
2. Under policy D, a luxury sink removes 2,000 gold per player on day 0. Roughly how far below the no-sink path is the server 277 days later?

<details>
<summary>Answers</summary>

1. `τ = g / (v × m*) = 60 / (0.04 × 15,000) = 10%`. Then `σ = 0.004`, and the half-life is about `0.693 / 0.004 ≈ 173` days.
2. About 1,000 gold. The gap created by the one-off sink closes with the tax's half-life of 277 days, so half of it remains.

</details>

## 3. Policy rules and the lag problem

A single tax setting is a one-time decision. Real economies drift, so you need a rule for changing the setting over time. Central banks call such a rule a **policy rule**. John Taylor's 1993 paper described one that became famous: raise the interest rate when inflation is above target, lower it when below, by amounts fixed in advance. The game version is short.

```
τ_new = τ_n + k × (m_obs / m_target − 1)          clamped to [0, τ_max]
```

- `τ_n` is the **neutral rate**, the tax that would hold `m_target` on its own. From section 2, `τ_n = g / (v × m_target)`.
- `k` is the **reaction strength**. With `k = 0.2`, money 10% above target adds 2 percentage points of tax.
- `m_obs` is the money per player you *observe*, which is the true value from `L` days ago. `L` is your **data lag**.
- You apply the rule every `R` days, your review period. A monthly economy review means `R = 30`.

This is a negative feedback loop from GD102 week 4. When `m` is high, the tax rises and pulls it down. When `m` is low, the tax falls and lets it rise. Negative feedback with a delay is the classic recipe for oscillation, and the numbers show it.

### Numbers you can check

Take the server from section 2 after a bad patch. It has `m(0) = 20,000`, a target of 16,000, `g = 40`, `v = 5%`, so `τ_n = 5%`. Review every 30 days. Tax is clamped between 0% and 30%. These values come from a day-by-day simulation, the same one the interactive runs.

| Reaction `k` | Data lag `L` | Lowest `m` reached | Settles within ±2% of target by day |
|---|---|---|---|
| 0 (just set 5%) | any | 16,258 at day 1,095 | 1,010 |
| 0.1 | 0 | 16,000 | 291 |
| 0.2 | 0 | 16,000 | 156 |
| 0.2 | 30 | 15,835 | 82 |
| 0.2 | 60 | 14,856 | 235 |
| 0.2 | 90 | 13,992 | 670 |
| 0.5 | 0 | 16,000 | 39 |
| 0.5 | 60 | 11,567 | never, within 3 years |

Check the first review by hand for `k = 0.2`, `L = 0`. On day 1 you observe 20,000, which is 25% above target. The rule gives `τ = 5% + 0.2 × 0.25 = 10%`. So `σ = 0.005` for the first month.

Three things stand out.

First, doing nothing clever (`k = 0`, just set the neutral rate) is safe and slow. It takes almost three years to settle.

Second, with no lag, stronger reactions are faster and still safe. `k = 0.5` settles in 39 days. It gets there by charging 17.5% tax for a month, which players will notice.

Third, lag changes everything. The same `k = 0.2` rule that settles smoothly with fresh data overshoots to 14,856 with a 60-day lag and to 13,992 with a 90-day lag. With `k = 0.5` and a 60-day lag, the rule keeps swinging the tax between 0% and 17.5% and never settles. The rule reacts to the past, and by the time the high tax takes effect, the problem it was answering is gone.

A small amount of lag can even help. With `L = 30` the rule settled faster than with `L = 0`, because a one-month-old reading kept the tax high for one extra review and closed the gap sooner. Do not read too much into that. It is a coincidence of this `R` and this `k`. Past a certain point, more lag always hurts.

### What sets your lag

In a game, `L` is the sum of several delays you can measure:

- Telemetry delay. How long until economy dashboards reflect today's trades. Daily jobs are common, and so are weekly reports.
- Analysis delay. How long until someone reads the report and decides. For monthly reviews, add up to 30 days.
- Patch delay. How long from decision to live change. A hotfix may take days. A client patch may take weeks.
- Player response delay. How long before players change their behavior. Players who hear a tax rise is coming may trade more before it lands.

Add them up honestly. If you review monthly, analyze for a week and ship with the next patch, `L` is easily 45 to 60 days. At that lag, the table says to keep `k` small.

### Design judgment for rules

- **Write the rule down before you need it.** A rule chosen in advance is predictable for players and protects you from panic. Taylor's point was that a simple, public rule can do nearly as well as discretion, and far better than discretion done under pressure.
- **Cut lag before you raise `k`.** Faster data and smaller, more frequent adjustments beat big corrections on old data.
- **Prefer levers with fast response for fast problems.** If inflation must stop this month, a faucet cut acts on tomorrow's income. The tax is for holding the level after that.
- **Clamp the instrument.** Players tolerate a 5% tax. A 30% tax changes behavior so much that the model (fixed `v`) no longer holds. The clamp in the rule keeps you in the region where your model is trustworthy.

## 4. Open-market operations: the developer as a trader

A central bank's everyday tool is the **open-market operation**. It buys or sells assets, usually bonds, paying with money it creates or receiving money it retires. The game version is the developer acting as a buyer or seller on the player market.

Old School RuneScape's item sink is the cleanest shipped example. Tax gold that is not simply deleted is used to buy a fixed, Jagex-chosen number of specific high-value items from players each week, and those items are deleted. According to the Old School RuneScape Wiki, the targets have included items such as the twisted bow and ancestral robes. Two things happen at once.

- **Money.** The coins used to buy the items were already removed by the tax. The item sink does not remove more money. It decides where the tax money goes before it disappears.
- **Items.** The item supply falls by the purchased quantity every week. That props up those items' prices against the slow growth of supply from boss drops.

In model terms, the tax is the money lever and the item sink is an item lever funded by it. You can write the item side the same way as the money side. If a boss drops `d` copies of an item per day and the sink buys `b` per day, the item's stock grows by `d − b` per day. When `b` is close to `d`, the stock stops growing, and so does the downward pressure on its price.

The reverse operation is the developer selling something for gold. Every NPC vendor that sells a luxury item does this. The difference from a one-off sink is that you can repeat it and price it. A vendor that sells a cosmetic for a price you raise with the price index is a proportional sink in disguise, because richer servers pay more.

Two cautions. First, a developer that trades on its own market has perfect information about supply, so every purchase is also a price signal players will try to front-run (week 6 covers what front-running a known buyer looks like). Fixed weekly quantities, as Old School RuneScape uses, leave less to guess. Second, if you buy items to hold their price, you are choosing winners. Players holding those items gain. Players who wanted to buy them lose. Say which in your design document.

## 5. Announcements and expectations

Policy in a game is public. Patch notes are published before the patch. Players read them and act, so every announced change has two effects, the one you modeled and the one caused by people preparing for it.

Think through a tax rise announced two weeks in advance. Sellers who planned to sell next month sell now, before the rate goes up, so volume and `v` jump during the announcement window, and prices dip as supply rushes in. After the change, volume drops below normal for a while because the rush pulled future trades forward. Your dashboard sees a spike and a dip that have nothing to do with the steady-state model. If your rule reacts to them, it adds noise.

The same logic works in reverse for a faucet cut. Players who hear that a gold farm is being nerfed will farm it harder until the patch lands. You have printed extra money right before the fix.

Three habits help.

- **Mark announcement windows on your dashboards** and exclude them when you estimate `v` or `g`.
- **For faucet cuts, ship first and explain second** when the exploit is abusable. For taxes and fees, announce early, because surprise taxes feel unfair and players are right to object.
- **Prefer rules to announcements.** A published rule ("the fee tracks the price index every month") makes each change small and expected, so there is little to front-run.

## In-class activity (25 minutes)

Work in groups of three. Each group gets a one-page economy card from the instructor with a server's `g`, `v`, current `m`, target, and a data lag.

1. Compute the neutral tax rate and its half-life. Is the half-life shorter than the time your producer has given you to fix inflation (on the card)?
2. If not, design a package that meets the deadline. You may change `g` (with a stated cost to players), add a one-off sink (with a price and a take-up share), and set a feedback rule with `k` and `R`.
3. Use the interactive to run your package with the card's lag. Record the lowest `m`, the highest tax rate reached, and the day the server settles within ±2%.
4. Write two lines of patch notes that describe the change honestly, including when players should expect to see prices move.

Expected output: one filled row per group on the whiteboard (package, lowest `m`, peak tax, settle day) and the patch notes. The class then compares which packages traded speed for player pain.

## Common misconceptions

- **"Doubling a tax halves prices."** It halves the ceiling `m*`. Prices get there with a half-life of `0.693 / σ`, which at single-digit tax rates is measured in years.
- **"A big one-off sink fixes inflation."** It lowers the level once. The slope, or the gap to the ceiling, is unchanged, so the drift resumes the next day.
- **"Reacting harder to bad numbers is being responsible."** With lag, harder reactions overshoot and can oscillate. Reduce lag first, then raise `k`.
- **"The item sink removes money."** In Old School RuneScape the money was already removed by the tax. The item sink spends that allowance on removing items, which is a separate lever with a separate target.

## Check yourself

1. A server has `g = 25`, `v = 8%` and a 2.5% trade tax. Compute `m*` and the half-life. If `m(0) = 5,000`, what is `m` after one half-life?
2. Starting from no tax, you can either cut `g` from 40 to 30 (row E) or add a 1% tax (row B), with `v = 5%` and `m(0) = 10,000`. Using the table in section 2, which gives lower `m` at day 365? At day 730? Explain why the answer flips.
3. A feedback rule has `τ_n = 5%`, `k = 0.2` and target 16,000. The observed `m` is 14,000. What tax does the rule set? What would it set if `k = 0.5`, and why might that be a problem with a 60-day lag?
4. A designer proposes raising velocity by making trading easier (lower listing friction) instead of raising the tax. Using `σ = τ × v`, explain why this could lower `m*`, and name one reason it might not.

<details>
<summary>Answers</summary>

1. `σ = 0.025 × 0.08 = 0.002`. `m* = 25 / 0.002 = 12,500`. Half-life `≈ 0.693 / 0.002 ≈ 347` days. After one half-life the gap of 7,500 has halved, so `m ≈ 12,500 − 3,750 = 8,750`.
2. At day 365 the faucet cut is lower (20,950 vs 21,680). At day 730 the tax is lower (31,411 vs 31,900). The faucet cut removes a fixed 10 gold per player per day. The 1% tax removes `0.0005 × m`, which is 5 gold at `m = 10,000` and grows as `m` grows. Once `m` passes 20,000 the tax removes more each day than the faucet cut, and its lead builds from there.
3. `τ = 5% + 0.2 × (14,000/16,000 − 1) = 5% − 2.5% = 2.5%`. With `k = 0.5`, `τ = 5% − 6.25%`, which clamps to 0%. With a 60-day lag the rule will still see low values after money has recovered, keep the tax at zero too long, and overshoot above target.
4. `σ` rises with `v`, so the same tax removes more per day and `m*` falls. It might not, because extra trading is not the same money changing hands more often. Players may trade more items at lower prices, and some of the new volume may fall under the per-item cap or the exemption threshold, where the tax is zero.

</details>

## Lab / assignment hook

[Lab 04, the policy desk](../labs/lab04.md). You build the day-by-day money model in a spreadsheet or Python, add a feedback rule, and find the fastest rule that never undershoots the target by more than 5% at your assigned data lag. It is the first piece of the final agent-based economy and policy memo.

## Sources

- Old School RuneScape Wiki, "Grand Exchange" and "Grand Exchange tax" (accessed September 2026). Tax of 1% from 9 December 2021, 2% from 29 May 2025, cap of 5 million coins per item, no tax below 50 coins, the item sink buying and deleting a fixed Jagex-chosen number of items per week, and Mod Ash's May 2025 figure of about 5.73 trillion coins of items removed.
- EVE Online, "Patch notes, version 22.02" (12 March 2025). Sales tax raised from 4% to 7.5%. EVE University Wiki, "Accounting" (current). 11% reduction per skill level.
- Warcraft Wiki, "Auction House" (World of Warcraft retail). The 5% cut of the winning bid.
- Fisher, I. (1911). *The Purchasing Power of Money*. Macmillan. Chapter II, "Purchasing Power of Money as Related to the Equation of Exchange", where `MV = PT` is stated (Library of Economics and Liberty edition, retrieved September 2026).
- Friedman, M. (1961). "The Lag in Effect of Monetary Policy." *Journal of Political Economy* 69(5).
- Taylor, J. B. (1993). "Discretion versus Policy Rules in Practice." *Carnegie-Rochester Conference Series on Public Policy* 39.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- All server numbers in sections 2 and 3 (`g`, `v`, `m(0)`, targets) are invented for teaching and computed with the stated formulas.

## Interactive spec: examples/w04-tax-lever.html

**The one insight:** a transaction tax sets where money per player ends up (`m* = g / (τv)`) but at single-digit rates it gets there slowly (half-life `0.693 / (τv)`), and a feedback rule that reacts to stale data overshoots.

**Layout.** Two tabs. Tab 1 "One lever" and tab 2 "Policy rule". Mobile: views stack vertically. Desktop: controls on the left, chart on the right.

**Tab 1, One lever.**
- Chart: `m(t)` for `t = 0..1,095` days (x axis in days, gridlines every 365). A dashed horizontal line at `m*` when `σ > 0`, labelled "ceiling m*". A dot on the curve at `t = half-life`, labelled with the day. A faint grey reference line for the no-tax path `m(0) + g × t`.
- Controls (sliders, keyboard-operable, each with its numeric value shown): tax `τ` 0% to 20% step 0.5% (default 2%); velocity `v` 1% to 20% step 1% (default 5%); net faucet `g` 0 to 100 step 5 (default 40); starting money `m(0)` 1,000 to 30,000 step 1,000 (default 10,000); one-off sink at day 0, 0 to 5,000 step 500 (default 0), subtracted from `m(0)`.
- Readouts: `σ`, `m*` (or "none" if `σ = 0`), half-life in days, `m` at days 90, 365, 730, 1,095, rounded to whole gold.
- Formulas: `σ = τ × v`. Path `m(t) = m* + (m(0) − sink − m*) × (1 − σ)^t` when `σ > 0`, else `m(0) − sink + g × t`. Half-life `ln 2 / −ln(1 − σ)`.
- Test values (must match the lecture table): defaults with `τ = 2%` give `m* = 40,000`, half-life 693, and `m` = 12,583, 19,178, 25,548, 29,969 at 90, 365, 730, 1,095. `τ = 5%` gives 16,000, 277, 11,210, 13,594, 15,035, 15,613. `τ = 5%`, `g = 30` gives 12,000 and 10,403, 11,198, 11,678, 11,871. `τ = 5%` with sink 3,000 gives 15,419 at day 1,095. `τ = 0` gives 13,600, 24,600, 39,200, 53,800.

**Tab 2, Policy rule.**
- Chart top: `m(t)` for 1,095 days, with the target as a horizontal line and a shaded ±2% band. Chart bottom (shared x axis): `τ(t)` as a step line.
- Controls: reaction `k` 0 to 1 step 0.05 (default 0.2); data lag `L` 0 to 120 days step 10 (default 0); review period `R` 1, 7, 30, 90 days (default 30); target 8,000 to 30,000 step 1,000 (default 16,000); `m(0)` (default 20,000); `g` (default 40); `v` (default 5%). Tax clamp fixed at [0%, 30%].
- Simulation: `m[0] = m(0)`. For day `t = 1..1,095`: if `(t − 1) mod R = 0`, set `obs = m[max(0, t − 1 − L)]` and `τ = clamp(τ_n + k × (obs / target − 1), 0, 0.30)` with `τ_n = g / (v × target)`. Then `m[t] = m[t − 1] + g − τ × v × m[t − 1]`. `τ` holds between reviews.
- Readouts: `τ_n`, lowest `m` reached, highest `τ` reached, first day after which `m` stays within ±2% of target (or "not within 3 years").
- Test values (defaults except as noted, `R = 30`): `k = 0.2, L = 0` lowest 16,000, settles day 156. `k = 0.2, L = 60` lowest 14,856, settles day 235. `k = 0.2, L = 90` lowest 13,992, settles day 670. `k = 0.5, L = 0` settles day 39, peak `τ` 17.5%. `k = 0.5, L = 60` lowest 11,567, never settles. `k = 0`: settles day 1,010.
- A one-line caption under the chart that updates: "Rule reacts to data L days old. Overshoot: X% below target."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Both charts have text readouts so the insight is available without the plot. Respect `prefers-reduced-motion` (no animated transitions). No game art or logos.
