# MMO304 · Week 13 — Case Studies: EVE, Diablo, RuneScape Grand Exchange

**Why this matters:** Three famous economies made three different bets about who may trade with whom. One of them shut its market down after less than two years, one publishes its money supply every month, and one froze its prices inside a 5% band for three years. Each outcome follows from the same few numbers, and you will need those numbers when you write your own economy spec next week.

**You will be able to:**
- Compute how a market's reach changes the chance that a random drop is an upgrade, and the number of drops a player waits between upgrades.
- Analyse any shipped MMO economy with a four-question lens (flows, reach, core loop, intervention) and write the result as a one-page teardown.
- Compare the market designs of Diablo III, EVE Online and RuneScape and explain which design fits which core loop.
- Critique a proposed market change (a new auction house, a tax, a price band) by predicting its effect on the loop it touches.

**Before class:** CCP, *Monthly Economic Report, January 2024* (skim every chart; read the ISK faucets and sinks section and the money supply section closely). Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters on markets and on economic design goals. Castronova (2001), *Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier*, the introduction and the sections describing how players trade.

**Prerequisites from earlier courses:** [MA102 week 7, geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (the mean wait `1/p`). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (for the lab). GD102 [week 2 on stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) and [week 7 on sources and drains](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md). From this course, [week 3 on faucets and sinks](w03-faucets-sinks-and-transformations.md), [week 6 on auction house equilibrium](w06-supply-demand-and-equilibrium-in-auction-houses.md), [week 9 on commodity money](w09-commodity-money-when-an-item-becomes-currency.md) and [week 11 on real-money trade](w11-real-money-trade-and-gold-farming.md), whose self-found upgrade model this week extends.

**Interactive:** [examples/w13-auction-house-upgrade-drought.html](../examples/w13-auction-house-upgrade-drought.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. A lens for reading an economy

A case study is only useful if you can transfer it. "Diablo III's auction house failed" is a headline. "A market that pools every player's drops divides the rate at which play produces upgrades by the size of the pool" is a rule you can apply to your own game. This lecture turns three famous stories into rules like that.

Use the same four questions on every economy you study.

1. **Flows.** Where does currency enter (faucets), where does it leave (sinks), and what converts one good into another (transformations)? You built this vocabulary in week 3.
2. **Reach.** Who can trade with whom, and at what cost? A market's *reach* is the set of sellers whose goods a buyer can get. A global auction house has maximum reach. A regional market, a bind-on-pickup rule or a trade tax each cut reach down.
3. **Core loop.** What does the player do minute to minute, and what reward keeps them doing it? Ask whether the market sells that reward.
4. **Intervention.** What did the developer change, when, and what happened next? Always record the version or date. Economies are rebuilt patch by patch, so a fact without a date is a rumour.

Question 2 is the one students skip, and it decides the most. The rest of the lecture shows why.

## 2. Worked example: the auction house that emptied the loot hunt

### The hook

Diablo III launched in 2012 with two auction houses, one for in-game gold and one for real money. [Week 11](w11-real-money-trade-and-gold-farming.md) covered the real-money house, its fees and what it meant for gold farming. This week sets the money aside and looks only at what either house did to the loot hunt.

The market worked. Items sold, prices formed, players found upgrades. Yet in March 2013 the game's director, Jay Wilson, said publicly that the auction houses had "really hurt" the game. On September 17, 2013 Blizzard announced that both houses, gold and real-money, would close, and on March 18, 2014 they did. One week later the expansion Reaper of Souls shipped, on the back of a loot overhaul that made most good items account-bound.

So here is the puzzle. The auction house did exactly what markets are supposed to do. It moved items to the players who valued them most. Why would a working market damage a game?

### The model

Strip Diablo's loot down to one number. Every item that drops has a quality percentile `q` between 0 and 1, and for now assume drops are independent and uniformly spread across that range. You wear the best item you have access to. An upgrade is any new drop that beats it.

- `n` is the number of drops you have found yourself so far.
- `K` is the number of drops you have *access to*. Without a market, `K = n`.
- `m` is the market's reach multiplier. With a market, each drop you find is matched by `m` drops from other players that you can buy, so `K = (1 + m) × n`.
- `d` is your own drops per hour, and `t` is hours played, so `n = d × t`.

This is week 11's model seen from the other end. Week 11 wrote the pool as `M` drops you can shop from for each drop you find, so `M = 1 + m`. Here `m` counts only other players' drops, which makes `m = 0` the no-market case, and we track the best item you wear rather than a running count of upgrades.

Two facts about the best of `K` uniform draws do all the work.

```
expected quality of what you wear    = K / (K + 1)
chance your next own drop upgrades it = 1 / (K + 1)
```

The second line is the chance that one new draw beats all `K` earlier ones. By symmetry each of the `K + 1` items is equally likely to be the best, so the newest one wins with probability `1 / (K + 1)`. The number of drops you then wait for an upgrade is geometric, as in MA102 week 7, with mean `K + 1`.

Multiply by drops per hour to get upgrades per hour *from play*:

```
self-found:   upgrades per hour ≈ d / (d·t + 1)        ≈ 1 / t
with market:  upgrades per hour ≈ d / ((1+m)·d·t + 1) ≈ 1 / ((1+m)·t)
```

The self-found line has a strange property. For any meaningful playtime, the rate at which play produces upgrades is about `1/t`, whatever the drop rate. Doubling the drop rate gets you to good gear sooner, but it does not change the fact that at hour 10 you are finding about one upgrade every 10 hours. The market line is the same curve divided by `1 + m`.

**The market divides the rate at which play pays out by the size of the pool you can buy from.**

### Numbers you can check

Take `d = 20` drops per hour and a market reach of `m = 99`, so each of your drops is matched by 99 on sale. That is a small reach for a game with a global market and millions of players. These numbers are invented to be easy to check, not taken from Diablo III's drop tables.

| Hours played `t` | Own drops `n` | Self-found gear quality `n/(n+1)` | Self-found chance next drop upgrades `1/(n+1)` | Market pool `K = 100n` | Market gear quality | Market chance next drop upgrades |
|---|---|---|---|---|---|---|
| 1 | 20 | 95.24% | 4.76% | 2,000 | 99.95% | 0.050% |
| 10 | 200 | 99.50% | 0.50% | 20,000 | 99.995% | 0.0050% |
| 100 | 2,000 | 99.95% | 0.050% | 200,000 | 99.9995% | 0.00050% |

Read across the first row and down the last column, and two things stand out.

First, the market player at hour 1 wears gear as good as the self-found player at hour 100. The market compressed a hundred hours of progression into one shopping trip.

Second, from then on the market player's own drops almost never matter. At hour 10, the self-found player turns up about one upgrade every 10 hours of play (`20 × 0.0050 ≈ 0.1` per hour). The market player finds one every 1,000 hours (`20 × 0.00005 = 0.001` per hour). Every drop they pick up is, in practice, something to sell.

Count the upgrades too. The expected number of times the self-found player upgrades in their first `n` drops is the harmonic number `H_n = 1 + 1/2 + ... + 1/n`, which grows like `ln n + 0.58`. After 20 drops that is 3.6 upgrades. After 200 it is 5.9, and after 2,000 it is 8.2. Each tenfold increase in playtime buys only about 2.3 more upgrades. That slow, steady trickle of "I found something better" moments is the loot game. The market player gets a burst of upgrades at the trade screen and almost none from play.

### The visual

Open the interactive. The left panel plots gear quality against hours for both players, on a scale that stretches the top of the range so you can see the gap between 99% and 99.99%. The market curve jumps to the top almost at once, and it looks like the better deal.

The right panel plots the thing the left panel hides, upgrades per hour *found by playing*. The self-found curve falls like `1/t` but stays visible for a hundred hours. The market curve sits a hundred times lower and looks like a flat line on the floor. Drag the reach slider `m` from 0 to 999 and watch the right curve sink while the left curve barely moves. Moving from `m = 99` to `m = 999` improves gear quality by a fraction of a percentage point (at hour 10, from 99.995% to 99.9995%) and cuts upgrades from play by another factor of ten. On the left panel's stretched scale that gain looks like a full step, one more nine. In percent it is almost nothing.

That is the insight. On the left, more market reach looks free. On the right, you can see what it costs.

### What Blizzard changed

Read the fix through the model. Reaper of Souls' pre-expansion patch 2.0.1 (February 25, 2014), known to players as Loot 2.0, made items drop in smaller numbers but at higher quality, biased drops towards properties the finding character could use, and made previously tradeable gear account-bound, with only a short window to trade with others. In model terms:

- Account binding sets `m` to 0 for the items that matter. Your pool is your own finds again.
- Smart loot raises the share of drops that count as candidates for your character, which works like raising `d` for useful drops.
- Removing the auction house removes the fast route to the top of the curve.

The result is a game where the `1/t` trickle of upgrades comes from play again. Real-money trade and the cash-out fee raise a separate set of problems, which you studied in week 11. This lecture's claim is narrower. Even a market with no real money in it would have produced the collapse in the right-hand panel.

### Cross-game recognition

The same rule appears wherever a market meets a reward loop. Rewrite each case as "what is `m` for the core reward?"

**World of Warcraft (all eras since launch).** Items marked bind on pickup become soulbound the moment you loot them, so they cannot be sold. Most loot from bosses is bind on pickup, which sets `m` close to 0 for the core reward of raiding. The one exception is a short window, up to two hours for instance drops, in which a looter may hand the item to another member of the same group. That keeps the pool at the size of one raid group. At the same time the auction house trades bind-on-equip items and crafting materials, taking a 5% cut of each sale. Since patch 9.2.7 (Shadowlands era, August 2022), commodities such as herbs and consumables share one region-wide market, while armour and weapons stay realm-specific. WoW gives the market enormous reach for inputs and zero reach for the reward the loop is built on. That split is the Loot 2.0 fix, adopted years earlier.

**Diablo II (original game and Lord of Destruction).** Diablo II had no auction house at all. Trading happened by haggling in game lobbies, which is a high-friction market with small `m`. As you saw in week 9, the Stone of Jordan ring became the unit of account in those trades. High friction kept the self-found trickle alive for most players, and the commodity money grew up because there was no built-in currency market to replace it.

**EVE Online (single-shard server Tranquility, 2003 onward).** EVE puts nearly everything on the market, so `m` looks enormous. The loop survives because the core reward is not "find a better item". Players build, haul, trade and fight, and ships that are destroyed in combat leave the game. Destruction resets your gear to zero every time you lose, which restarts the curve. In model terms EVE keeps `m` high and cuts `t`, the time you get to hold any one item.

Three games, three ways to handle one number. When you meet a new market, find the core reward, then ask how many other players' copies of it a player can reach.

### Design judgment, eyes open

A global open market is not a mistake. It is a set of trade-offs.

- **Strength.** Markets turn surplus drops into value, give crafting and gathering players customers, and let players who cannot play many hours still progress.
- **Strength.** A market is the best telemetry you will ever get. Every sale is a price signal (week 12).
- **Cost.** If the market sells the core reward, it divides the rate at which play pays out by roughly `1 + m`. No drop-rate tuning fixes this, because the self-found rate `1/t` does not depend on drop rate.
- **Cost.** High reach invites real-money trade (week 11). A price on every item makes every item a thing to farm for cash.
- **Choice.** Decide per item category, not per game. Bind the core reward, open the market for inputs and cosmetics, or pick a destruction rate that keeps demand fresh. Write down what `m` is for each category in your spec. If you cannot say, you have not decided.

## 3. EVE Online: the economy as a published dataset

EVE is the case study for question 4, intervention, because CCP shows its work. In 2007 CCP became the first game developer to hire an economist, Eyjólfur Guðmundsson, to oversee the in-game economy. He held the role until 2014. CCP now publishes a Monthly Economic Report. The January 2024 edition, your reading, has charts for production, mining and destruction, regional trade and imports, NPC bounties, ISK faucets and sinks, money supply and velocity, and price indices for consumer goods, minerals and producer goods. CCP also offers the raw data for download.

### Reading the flows

Map the report onto the week 3 vocabulary.

- **Faucets** are mostly NPC payouts. Bounties for killing NPC pirates are the classic example, along with mission rewards and selling to NPC buyers.
- **Sinks** include market fees. Since March 12, 2025 (release 22.02), the sales tax on market sales has a base rate of 7.5%, up from 4%. Training the Accounting skill reduces it. Placing an order at an NPC station also costs a broker fee with a 3% base, reduced by the Broker Relations skill and by standings. Both are paid to NPC entities, so the ISK leaves the economy.
- **Transformations** are mining and manufacturing. Ore becomes minerals, minerals become ships, and ships become wrecks.

The tax history matters. CCP has moved the sales tax several times, and the 2025 jump nearly doubled it. That is a live developer pulling a sink lever and then publishing the money supply chart so everyone can watch the result. You will build the same kind of lever next week.

### Reach in EVE

EVE's market is not global. Each region has its own regional market, and goods must be hauled physically between them. Hauling costs time and carries risk, since cargo ships can be destroyed. In the week 6 model, travel cost acts like a transaction cost, and it lets prices differ between regions by up to the cost of moving goods between them. That gap is a profession. Players make a living hauling from cheap regions to expensive ones.

EVE also shows the other side of real-money pressure. In November 2008 CCP introduced PLEX, an item that adds 30 days of game time. Players buy it with real money and sell it on the market for ISK. The developer created a legal, taxed channel between cash and currency, which gave a public ISK-to-dollar price and competed with gold sellers. Week 11 covers the trade-offs.

## 4. RuneScape's Grand Exchange: a market with a leash

RuneScape is the case study for question 2, reach, pulled in both directions.

### The exchange and the band

Jagex launched the Grand Exchange on November 26, 2007. It replaced informal marketplaces where players stood in crowded spots shouting offers. The exchange matches buy and sell offers anonymously and publishes a guide price for each item, computed from recent trades.

Two weeks later, on December 10, 2007, Jagex removed free player-versus-player combat in the Wilderness and began limiting unbalanced trades between players, to cut off real-money traders. The trade limit covered new and high-risk accounts at first and every account from January 2, 2008 (week 11). Until free trade returned, Grand Exchange offers were also limited to 5% above or below the item's market price. Subscriptions fell by about 60,000 during the changes. On February 1, 2011, after a player referendum with about 1.2 million votes and 91% in favour, free trade and Wilderness combat came back.

### The model: a price on a leash

A 5% band means a price can move at most 5% each time the guide price updates. If the true market-clearing price is 50% above the guide, the fewest updates needed to get there is the smallest `u` with `1.05^u ≥ 1.5`.

```
u = ln(1.5) / ln(1.05) = 0.405 / 0.0488 ≈ 8.3, so 9 updates
```

Check it: `1.05^8 ≈ 1.477`, still short of 1.5, while `1.05^9 ≈ 1.551` passes it. During those updates, sellers who know the real value refuse to sell at the capped price, so the item vanishes from the exchange (week 6, a price ceiling creates a shortage). The band slowed real-money traders, who needed lopsided trades to move value, and it also slowed every honest price discovery. Jagex judged the cost worth paying for three years, then let players vote it away.

### Old School RuneScape and the tax sink

Old School RuneScape, the separately run version of the game, got its own Grand Exchange on February 26, 2015, after a player poll passed with 76.3%. On December 9, 2021 it added a 1% tax on most sales, raised to 2% on May 29, 2025 and capped at 5 million coins per item. Part of the revenue funds a system that buys selected items from players and deletes them from the game to hold their prices up. The rest simply leaves the economy.

That tax is a sink on reach itself. It charges for every use of the pool. Notice also the cap. For an item worth more than 250 million coins, 2% would exceed 5 million, so the tax becomes flat. A proportional sink with a cap stops being proportional exactly where the richest trades happen. Next week you will see why that matters for wealth at the top.

## 5. The three cases side by side

| Question | Diablo III (2012-2014) | EVE Online (2003 onward) | RuneScape Grand Exchange (2007 onward) |
|---|---|---|---|
| Core reward | Better random items | Ships, territory, ISK from industry and trade | Skill levels and gathered goods |
| Market reach for that reward | Global, then account-bound after 2.0.1 | Regional, with hauling costs | Global, banded to 5% until February 2011 |
| Main sink on trade | 15% gold cut, US$1 or 15% real-money fees | Sales tax (7.5% base since 2025) and broker fee (3% base) | Price band, not a fee, in 2007-2011; Old School adds a 2% tax from May 2025 |
| What protects the loop | Nothing at first; binding afterwards | Destruction resets gear | Progress is XP, which cannot be traded |
| Key intervention | Close both auction houses, March 18, 2014 | Publish the data, retune taxes | Price band 2007-2011, tax in Old School from 2021 |

RuneScape's row explains why a huge market did not hurt it the way Diablo III's did. A player's levels cannot be bought on the exchange. Buying the logs you need for a Firemaking level makes the grind faster, and in `m` terms raises your throughput, but the reward, the level itself, still comes from play. The market sells inputs, not the reward.

## In-class activity (25 minutes)

Groups of three. Each group gets one economy you have not studied in this course. Choose from Guild Wars 2's Trading Post, Final Fantasy XIV's Market Board, or Old School RuneScape's Grand Exchange after the 2025 tax change.

1. (10 min) Answer the four lens questions. Use only what you can check on an official site or a maintained wiki, and write down the version or date for every fact.
2. (5 min) Name the core reward. Estimate `m` for it as "zero", "small" (a few friends or a guild), "regional" or "global".
3. (5 min) Using the section 2 model, predict whether the market speeds up or hollows out the core loop. One sentence.
4. (5 min) Propose one intervention with a number attached, such as a binding rule, a tax rate or a price band width, and say which player it hurts first.

Expected output: one filled-in row of the section 5 table, plus the intervention sentence. Groups swap rows and challenge one fact each.

## Common misconceptions

- **"The auction house failed because of real money."** Real money added its own problems, but the model in section 2 works with gold alone. Any market that sells the core reward divides the upgrade rate by `1 + m`. The gold auction house did this too.
- **"Raise the drop rate and players will find upgrades again."** The self-found upgrade rate is about `1/t` whatever the drop rate. More drops push gear quality up faster, which makes each later drop less likely to beat it.
- **"Bigger markets are always more efficient, so always better."** Efficiency is measured in allocation, meaning items reach the players who value them. The designer also cares about the rate at which play produces rewards, and reach can lower that rate.
- **"A price band stops speculation, so it is free."** A band stops prices from reaching the market-clearing level, which creates shortages and slows honest price discovery. RuneScape paid that cost for three years.

## Check yourself

1. A self-found player has found 499 items. What is the chance their next drop is an upgrade, and how many drops should they expect to wait for one?
2. In a game with `d = 30` drops per hour and a market with reach `m = 49`, estimate upgrades per hour from play at hour 20, with and without the market.
3. A price is capped to move at most 10% per update, and the clearing price is double the current guide price. What is the fewest number of updates to reach it?
4. Your MMO's best gear drops from raids. The producer wants a global auction house. Using the model, write the one-sentence argument for binding raid gear while leaving crafting materials tradeable.
5. An Old School RuneScape item sells for 400 million coins. How much tax is paid under the May 2025 rules, and what percentage of the price is that?

<details>
<summary>Answers</summary>

1. With `K = 499`, the chance is `1/500 = 0.2%`, and the expected wait is 500 drops.
2. Own drops at hour 20: `n = 600`. Self-found rate `30 / 601 ≈ 0.050` upgrades per hour, one every 20 hours. With the market, `K = 50 × 600 = 30,000`, rate `30 / 30,001 ≈ 0.001` per hour, one every 1,000 hours.
3. Smallest `u` with `1.1^u ≥ 2`. `ln 2 / ln 1.1 = 0.693 / 0.0953 ≈ 7.3`, so 8 updates. Check: `1.1^7 ≈ 1.949`, `1.1^8 ≈ 2.144`.
4. A global market for raid gear sets `m` large for the core reward, which cuts upgrades from raiding by about `1 + m`. Crafting materials are inputs, so trading them speeds progress without replacing the reward.
5. 2% of 400 million is 8 million, which is over the 5 million cap, so the tax is 5 million. That is 1.25% of the price.

</details>

## Lab / assignment hook

[Lab 13, market reach and the upgrade drought](../labs/lab13.md). You simulate the section 2 model with Monte Carlo draws, confirm the `1/(K+1)` result, then test what happens when drops are not uniform and when items are destroyed. Your write-up feeds the market section of the final economy spec (week 14 and [Lab 14](../labs/lab14.md)).

## Sources

- Wikipedia, "Diablo III" (accessed September 2026). Two auction houses at launch, the 15% gold auction house cut, Jay Wilson's March 2013 remarks, closure announcement (September 17, 2013) and closure date (March 18, 2014).
- Wikipedia, "Diablo III: Reaper of Souls" (accessed September 2026). Release March 25, 2014 (PC and Mac); patch 2.0.1 on February 25, 2014; Loot 2.0 changes, including fewer higher-quality drops, drops suited to the finding character, and account-bound items with a limited trading window.
- Warcraft Wiki, "Auction House" (accessed September 2026). 5% cut of the winning bid on the faction auction house; region-wide commodity listings from patch 9.2.7 (August 2022).
- Warcraft Wiki, "Soulbound" and "Bind on pickup" (accessed September 2026). Bind on pickup and bind on equip rules; most boss loot is bind on pickup; instance drops can be traded within the group for up to two hours.
- Wikipedia, "Eve Online" (accessed September 2026). Single-shard server Tranquility; CCP's hiring of economist Eyjólfur Guðmundsson in 2007 and his departure in 2014; PLEX introduced November 2008.
- CCP Games, *Monthly Economic Report, January 2024*, eveonline.com. Report sections, including ISK faucets and sinks and money supply; raw data download.
- EVE University Wiki, "Market" and "Sales tax" (accessed September 2026). Regional markets; sales tax base 7.5% since release 22.02 (March 12, 2025), raised from 4%; broker fee base 3% at NPC stations and its skill and standing reductions.
- RuneScape Wiki, "Grand Exchange" and "Prices" (accessed September 2026). Release on November 26, 2007; guide price from recent trades; "before free trade was reintroduced, offers were limited to 5% above or below the market price"; price restrictions removed on 1 February 2011.
- RuneScape Wiki, "Trade limit". Announced and applied to new and high-risk accounts on 10 December 2007, to all accounts on 2 January 2008.
- Wikipedia, "RuneScape" (accessed September 2026). Trade and Wilderness changes of December 10, 2007 aimed at real-money trading; subscription drop of about 60,000; restoration on February 1, 2011 after a referendum with 1.2 million votes and 91% in favour.
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Launch on February 26, 2015 after a 76.3% poll; tax of 1% from December 9, 2021, 2% from May 29, 2025, capped at 5 million coins per item; tax revenue funds an item sink.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- Castronova, E. (2001). *Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier*. CESifo Working Paper 618.

## Interactive spec: examples/w13-auction-house-upgrade-drought.html

**Purpose.** Show that market reach barely changes gear quality but divides the rate of upgrades found by playing by `1 + m`.

**Layout.** Two linked panels side by side at desktop width, stacked on mobile (left panel first). Controls above the panels. A numbers strip under each panel.

**Controls.**
- `d`, own drops per hour: slider 1 to 100, step 1, default 20.
- `m`, market reach multiplier: slider on a log scale with stops 0, 1, 4, 9, 19, 49, 99, 199, 499, 999; default 99. Label "each of your drops is matched by m on sale".
- `t` marker, hours played: slider 1 to 200, step 1, default 10. Draws a vertical line on both panels and drives the numbers strip.
- Toggle "Show market player" (default on). When off, only the self-found curve appears, so students can see the self-found story alone first.

**Left panel, gear quality vs hours.** x axis hours 0 to 200, linear. y axis gear quality shown as a "nines" scale: plot `−log10(1 − Q)` where `Q = K/(K+1)`, with tick labels 90%, 99%, 99.9%, 99.99%, 99.999% at y = 1, 2, 3, 4, 5. Self-found curve uses `K = d·t`; market curve uses `K = (1+m)·d·t`. Note in the panel caption that the scale stretches the top of the range.

**Right panel, upgrades per hour from play vs hours.** x axis hours 0 to 200. y axis upgrades per hour, linear, 0 to 1 by default, with a toggle to switch to log scale. Self-found: `r_s(t) = d / (d·t + 1)`. Market: `r_m(t) = d / ((1+m)·d·t + 1)`. Shade the area under each curve from 0 to the `t` marker and label it "expected upgrades from play so far", computed as the sum over own drops `i = 1..n` of `1/(i+1)` for self-found (starting with nothing, the first drop is always an upgrade, so use `1 + sum_{i=1}^{n-1} 1/(i+1)`, which equals `H_n`) and `sum_{i=1}^{n} 1/((1+m)·i)` for the market player, treating the first market purchase as already made. Use `n = round(d·t)`.

**Numbers strip (both panels, at the `t` marker).** Own drops `n`; pool `K` for each player; gear quality to 4 decimal places of a percent; chance next drop upgrades; expected drops until next upgrade `K + 1`; upgrades per hour; hours per upgrade `1/r`; cumulative upgrades from play.

**The one insight.** Moving `m` from 99 to 999 changes gear quality by a sliver in percent (99.995% to 99.9995% at t = 10), though on the left panel's nines scale it is a full step up, and it pushes the right panel's market curve ten times lower. The numbers strip must show quality in percent so students see the sliver next to the step. The caption under the right panel reads: "Market reach divides the rate at which play pays out."

**Test values (defaults d = 20, m = 99).**
- t = 1: self-found K = 20, quality 95.24%, upgrade chance 4.76%, rate 0.952/h. Market K = 2,000, quality 99.95%, chance 0.0500%, rate 0.0100/h (20 / 2,001 = 0.009995).
- t = 10: self-found K = 200, quality 99.50%, chance 0.498%, rate 0.0995/h (one per 10.05 h). Market K = 20,000, chance 0.0050%, rate 0.00100/h (one per 1,000 h).
- t = 100: self-found K = 2,000, quality 99.95%, chance 0.0500%, rate 0.0100/h. Market K = 200,000, rate 0.000100/h.
- Cumulative self-found upgrades: H_20 = 3.598, H_200 = 5.878, H_2000 = 8.178.
- With m = 0 the two curves coincide exactly.

**Accessibility.** Both curves use distinct line styles (solid self-found, dashed market) as well as colours from `templates/interactive-tokens.css`. All sliders keyboard operable, with the current value in text next to each. With `prefers-reduced-motion`, curves redraw without animation.
