# MMO304 · Week 11 — Real-Money Trade and Gold Farming

**Why this matters:** If your game's gold or items can be traded between players, someone will sell them for real money, whether you allow it or not. How you respond decides how many bots flood your faucets, how many accounts get stolen, and whether finding loot still means anything. Diablo III tried the boldest answer on record and removed it less than two years later.

**You will be able to:**
- Compute how often a player's own drops are upgrades with and without access to a market, and explain why an open market can empty the loot loop of meaning.
- Compute the price band in which a black market for gold survives next to a sanctioned exchange such as the WoW Token.
- Classify a studio's real-money trade policy (ban, tolerate, sanction currency, sanction items) and predict its effect on bots, theft and the reward loop.
- Critique a proposed real-money feature using the two models from this lecture.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), the chapter on real-money trade. Reread [week 10](w10-market-design-auction-houses-vendors-barter.md), section 2, on how a central exchange changes prices.

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (the expected wait for an upgrade is a geometric mean, `1 / p`). [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (why gear upgrades carry the reward loop in loot games). From this course, [week 3 on faucets and sinks](w03-faucets-sinks-and-transformations.md) (bots are a faucet) and [week 10 on market design](w10-market-design-auction-houses-vendors-barter.md).

**Interactive:** [Self-found upgrades](../examples/w11-self-found-upgrades.html). Keep it open during section 2.

---

## 1. What real-money trade is, and why it happens

**Real-money trade (RMT)** is any exchange of in-game currency, items or accounts for real money. **Gold farming** is the supply side, made up of people, or bots run by people, who play to collect currency and items for sale. A **sanctioned** exchange is one the studio runs or permits. An **unsanctioned** one breaks the terms of service and happens on third-party sites.

RMT happens because players differ in two resources. Some have more free time than money. Others have more money than free time. An MMO that rewards time with power creates a price for that time, and a trade between the two groups makes both better off in their own terms. That is why no MMO with open trade has ever stopped RMT entirely. The studio can only choose where it happens and who carries the risk.

The scale has been large for twenty years. Estimates collected by Wikipedia's gold farming article range from 100,000 full-time gold farmers in China in 2005 (a New York Times estimate) to around a million by 2009, and a global market for virtual goods in the hundreds of millions of US dollars per year by 2006-2007. Treat these numbers as rough. They come from journalists and researchers counting an informal industry. The order of magnitude is the point.

Unsanctioned RMT causes four problems a designer has to care about.

1. **Bots are a faucet you don't control.** A bot that farms gold around the clock adds currency faster than any player. In week 4's terms, it raises money supply per capita without raising the number of real players.
2. **Account theft.** Stolen accounts get stripped and their gold sold. Blizzard named this directly when it launched the WoW Token in 2015, calling unauthorized gold sellers one of the main sources of account compromises.
3. **Payment fraud.** Sellers use stolen credit cards to buy subscriptions and then farm on them.
4. **The reward loop.** If the best items can be bought, finding them yourself matters less. This one is the subject of section 2, because it is the one players feel most and designers understand least.

## 2. Worked example: the Diablo III auction house and the self-found upgrade

### The hook

Diablo III launched in May 2012 with two auction houses. One traded items for gold. The other, the Real-Money Auction House (RMAH), opened on 12 June 2012 (15 June in the Americas) and traded items for real money. Blizzard took a flat US$1 per equipment sale, 15% of commodity sales, and a further 15% when a seller cashed out to an external account.

In March 2013 the game's director, Jay Wilson, said the auction houses had "really hurt" the game. On 17 September 2013, Blizzard announced it would close both. They closed on 18 March 2014. One month earlier, patch 2.0.1 (25 February 2014) had brought in "Loot 2.0": fewer drops, of higher quality, more often suited to the character who found them, and mostly bound to the account instead of tradable.

A studio built a feature it expected to earn money, then paid to remove it. The complaint you hear from players of any loot game with an open market fits in one line. Why kill monsters for gear when the auction house has better gear for less time? A simple model shows why that complaint is almost exact.

### The model

Think of every item drop as a random draw of "item power" from the same distribution. Your equipped item sits at **percentile** `q` of that distribution, which means a fraction `q` of all drops are worse than it.

- `q` is the percentile of your current item, between 0 and 1.
- `u = 1 − q` is the chance a single new drop is an upgrade.
- `n` is the number of drops you have found yourself.
- `M` is the market multiplier, the number of drops you can effectively shop from for each drop you find. With no market, `M = 1`. If a thousand players feed the market and you can afford the best of what they sell, `M = 1,000`.

Two results follow.

**The wait for an upgrade.** Each drop is an upgrade with probability `u`, so the number of drops until the next upgrade is geometric (MA102 week 7) with mean

```
expected drops to next upgrade = 1 / (1 − q)
```

**How many of your own drops were upgrades.** With no market, your `j`-th drop is an upgrade only if it is the best of the `j` drops you have seen, which happens with probability `1 / j`. Add these up and the expected number of self-found upgrades after `n` drops is the harmonic number

```
H(n) = 1 + 1/2 + 1/3 + ... + 1/n    (about ln n + 0.577)
```

With a market, you have already bought the best of the `M × j` drops in the pool. Your own `j`-th drop is an upgrade only if it beats all of them, with probability `1 / (M × j)`. So:

```
expected self-found upgrades with a market = H(n) / M
```

Every one of your drops still happens. The market divides their value to you by `M`.

### Numbers you can check

First the wait, for an item at percentile `q`:

| Your item's percentile `q` | Chance a drop is an upgrade | Expected drops to next upgrade |
|---|---|---|
| 50% | 50% | 2 |
| 90% | 10% | 10 |
| 99% | 1% | 100 |
| 99.9% | 0.1% | 1,000 |
| 99.99% | 0.01% | 10,000 |

Now self-found upgrades after `n` drops, for several market sizes:

| Drops found `n` | No market, `M = 1` | `M = 10` | `M = 100` | `M = 1,000` |
|---|---|---|---|---|
| 10 | 2.93 | 0.29 | 0.029 | 0.003 |
| 100 | 5.19 | 0.52 | 0.052 | 0.005 |
| 1,000 | 7.49 | 0.75 | 0.075 | 0.007 |

Check one by hand. `H(10) = 1 + 0.5 + 0.333 + 0.25 + 0.2 + 0.167 + 0.143 + 0.125 + 0.111 + 0.1 = 2.93`.

Read the tables together. A solo player who finds 100 items gets about five upgrades from them, spread out so that each one feels earned, with waits that grow from 2 drops to about 100. A player who shops in a market fed by a thousand others finds an upgrade from their own drops roughly once in every 200 play sessions of 100 drops. After only 10 drops the pool holds 10,000 items, so their gear already sits near the 99.99th percentile and the next self-found upgrade is about 10,000 drops away. Their drops are still worth something, but only as goods to sell.

That is the loop players complain about. Before the market, the loop is kill, find, equip. After it, the loop is kill, find, sell, buy. The RMAH added a real-money price to the "buy" step, which let players skip the first three steps entirely.

### What a studio can do about it

The equation shows the options. You can lower `M` or change what counts as an item.

- **Lower `M` directly.** Bind items to the player so they never enter the market. That makes `M = 1` for those items.
- **Lower `M` by price.** A player can only buy what they can afford, so wealth inequality lowers the effective `M` for poorer players. This is not a lever you want to depend on.
- **Make drops disappear.** If items are destroyed through use, the pool never accumulates, and the market sells replacements, not upgrades.
- **Lower drop quality.** If everyone can buy from a huge pool, you can make top items rarer so the pool stays thin. That keeps `q` for market buyers lower, but it makes self-found play even more hopeless.

Diablo III's Loot 2.0 chose the first option and reversed the last. Drops got better and more targeted, which only works once most of them can no longer be sold.

### The visual

Open `examples/w11-self-found-upgrades.html`. The left panel plots your item power against drops found, for two players side by side. One plays solo and the other buys the best item in the market pool after every drop. The right panel counts upgrades by source. Drag the market-size slider from 1 up to 1,000. The market player's gear line jumps high and stays there, while the green "found it myself" count on the right flattens to almost zero. The solo player's line climbs in rare, visible steps. Both players had exactly the same drops.

### Cross-game recognition

**World of Warcraft (bind rules, retail and classic).** WoW sorts tradable items with binding. A bind-on-pickup item becomes soulbound, unable to be traded, the moment a player picks it up. A bind-on-equip item can be traded until someone equips it. In this lecture's terms, bind on pickup sets `M = 1` for that item at the moment it drops, while bind on equip lets the market set `M` until the item is used. The designer chooses per item which of the two loops applies.

**Diablo III after Loot 2.0 (patch 2.0.1, February 2014).** The same game, with `M` pushed back toward 1. Most gear became account-bound, with only a short window to trade drops with the players who were present. The model predicts what happened to drop design. Once your own drops matter again, they can be more generous without collapsing the loop, and Loot 2.0 made them fewer but better.

**EVE Online (current).** EVE's markets trade almost everything and the game has a sanctioned real-money item, PLEX, yet the self-found problem does not dominate. The reason is that ships and modules are destroyed when a ship is lost. CCP's Monthly Economic Report tracks the value destroyed each month next to the value produced and mined. The market pool drains as fast as players fill it, so the market sells replacements, and `q` for any pilot keeps falling back. Destruction is the third lever, applied at the scale of a whole economy.

Three games, one fraction. When a player says "why farm when I can buy," look for `M`, and ask which of the levers the game uses to keep it small.

### Eyes-open design judgment

- **Open trade is a choice about the reward loop, not only about the economy.** If your core loop is "find better gear," every tradable upgrade shrinks it by a factor of `M`. Decide which items belong to the loop and which to the market.
- **Binding creates its own problems.** Bound items can't move between a player's characters, can't be gifted, and make bad luck feel worse, since nobody can help you. Diablo III's short trading window for group drops is a compromise between the two.
- **Destruction is powerful and expensive.** Full loss on death is a sink that keeps markets alive, but it drives many players away. Durability loss (week 8) is a milder form.
- **Real money raises the stakes.** A gold auction house shrinks the loop. A real-money one also puts a price in dollars on skipping the game, and makes the studio a party to every trade. Once the fee revenue is part of the business plan, fixing the loop costs money.

## 3. Sanctioned exchanges and the black-market price band

Most studios that sanction RMT today do it differently from Diablo III. They sell an item for real money that players can trade for in-game currency and that can be redeemed for game time. Gold changes hands between players. No new gold is created.

| System (introduced) | Bought for | Redeemed for | Price of currency set by |
|---|---|---|---|
| EVE Online PLEX (current form) | Real money from CCP | Omega game time, 500 PLEX per 30 days | Player market, in ISK |
| WoW Token (patch 6.1.2, Americas from 7 April 2015) | US$20 in the in-game shop | 30 days of game time, or Battle.net balance | The game, from supply and demand |
| Old School RuneScape bond (30 March 2015) | US$9.99 | 14 days of membership | Grand Exchange |
| Guild Wars 2 gem exchange (current) | Gems, bought with real money | Store items | Supply and demand, with a transaction fee |

A sanctioned exchange doesn't end the black market. It puts a ceiling on it.

### The model

Let the token cost `$T` and sell for `G` gold. The sanctioned price of gold is then

```
p_s = T / G      (dollars per gold)
```

A buyer who buys from a gold seller pays `p_b`, but also carries risk, such as a ban, a stolen account or a chargeback. Call the expected cost of that risk a fraction `r` of the purchase. The buyer prefers the black market only if

```
p_b × (1 + r) < p_s
```

A gold farmer can only sell above their own cost. If a farming account costs `h` dollars per hour to run, earns `g` gold per hour, and costs `A` dollars to replace when banned after an expected `t` hours, then

```
farmer's cost per gold = (h + A / t) / g
```

The black market survives only when the farmer's cost is below the ceiling the token sets, `(h + A / t) / g < p_s / (1 + r)`.

### Numbers you can check

The numbers below are invented for teaching, not measured from any game. Use per-100,000-gold units to keep them readable. A token costs $20 and sells for 250,000 gold, so `p_s = $8.00` per 100k gold. A bot runs for `h = $0.30` per hour, farms `g = 30,000` gold per hour, and a fresh account costs `A = $50`.

| Expected hours before a ban `t` | Hourly cost `h + A/t` | Farmer's cost per 100k gold | Black market possible (with `r = 0.5`, ceiling $5.33)? |
|---|---|---|---|
| 500 | $0.40 | $1.33 | Yes |
| 50 | $1.30 | $4.33 | Yes, barely |
| 20 | $2.80 | $9.33 | No |
| 5 | $10.30 | $34.33 | No |

Check the second row: `(0.30 + 50 / 50) / 0.3 = 4.33`. With 30,000 gold per hour, one hour is 0.3 units of 100k.

The token sets the ceiling. Bans, bot detection and account prices set the floor. The black market lives between them. A studio can push the floor up by banning faster, by making accounts cost more (a box price or a subscription), or by cutting how much gold a bot can make per hour. It can push the ceiling down by making tokens cheaper in gold, which happens when more players sell gold for tokens. It can raise `r` by warning and banning buyers too.

Notice what changed in the second row. Cutting a bot's lifetime from 500 hours to 50 more than triples the farmer's cost. Bot detection that is fast is worth much more than detection that is thorough but slow. MMO309 covers the detection side.

## 4. Policy choices, compared

Studios have tried four broad policies.

**Ban and enforce.** Trade stays open, RMT is against the rules, and the studio hunts sellers. This is the default. It keeps the reward loop intact for honest players and leaves the risk with buyers.

**Restrict trade.** RuneScape announced a trade limit on 10 December 2007 and applied it to all players on 2 January 2008, as part of measures to curb real-world trading. Trades judged too unbalanced, measured against Grand Exchange prices, were blocked. The Wilderness was changed at the same time. Players disliked the restrictions for three years. In a referendum that closed on 14 January 2011, 91% voted to restore free trade and the old Wilderness, and free trade returned on 1 February 2011. A smaller limit remains for new accounts that have never paid for membership. The lesson is that restricting trade works against farmers and against every honest player who trades, and players will tell you which group they care about.

**Sanction currency.** PLEX, the WoW Token and bonds. Gold moves between players, the studio earns from the token sale, and the price ceiling from section 3 squeezes gold sellers. The cost is that players can openly buy gold, so wealth no longer signals time played.

**Sanction items.** The Diablo III RMAH. The studio earns a fee on every trade, and the reward loop takes the full `M` effect from section 2.

These are not exclusive. Old School RuneScape sells bonds and still bans gold sellers. WoW sells tokens and still uses bind-on-pickup to keep top raid gear out of the market.

## 5. The people behind the farms

Gold farming is labor. One estimate summarized by Wikipedia puts the average monthly earnings of gold farmers in 2005-2006 at about US$145, with most of them based in China. When you design against farming you are also designing against someone's income. That doesn't change the case for protecting your players, but it should shape how you talk about it. Anti-RMT messaging built on a national stereotype invites harassment of ordinary players who happen to share a language or a play style with it. Target the behavior (botting, spam, theft) and never a group of players. MMO402 and MMO403 cover the ethics in depth.

## In-class activity (25 minutes)

Groups of four. Each group gets a game profile on a card:

- **A:** A loot-driven action RPG where all drops are tradable.
- **B:** A sandbox MMO with full loot on death.
- **C:** A theme-park MMO with a subscription and bind-on-pickup raid gear.
- **D:** A free-to-play MMO with no box price.

For your game:

1. Estimate `M` for top-end gear and say which lever from section 2 keeps it small, if any.
2. Using the section 3 model, say whether a black market for gold can survive, and which variable (`h`, `A`, `t`, `g` or `r`) you would push first.
3. Choose one policy from section 4 and write two sentences on its biggest risk for your game.

Expected output: a three-line answer per question, presented in two minutes.

## Common misconceptions

- **"A token stops gold selling."** It caps the black-market price. Sellers who can farm below the cap keep selling.
- **"If gold can be bought, the economy inflates."** Tokens move gold between players without creating any. Bots create gold. The inflation risk comes from the farming, not the purchase.
- **"The RMAH failed because people didn't like paying money."** It changed the reward loop for every player, including those who never spent a cent. The `H(n) / M` result applies to the gold auction house too.
- **"Making items untradable solves RMT."** It moves RMT to account selling and piloting services, where a seller logs in as the buyer. Every policy moves the trade. None removes it.

## Check yourself

1. Your item is at the 95th percentile of the drop distribution. How many drops do you expect to need for the next upgrade?
2. A game has trade and an effective market multiplier of `M = 50`. A player finds 1,000 items in a season. How many self-found upgrades do they expect? How many without the market?
3. A token costs $15 and sells for 90,000 gold. Buyers carry a risk of `r = 0.25`. Bots farm 15,000 gold per hour at $0.20 per hour, and accounts cost $30. What is the largest expected account lifetime, in hours, at which the black market can no longer undercut the token?
4. A designer wants to sell a "gear chest" for real money that contains random tradable items. Using section 2, explain what it does to the reward loop of players who never buy one.

<details>
<summary>Answers</summary>

1. `1 / (1 − 0.95) = 20` drops.
2. `H(1,000) / 50 = 7.49 / 50 = 0.15`. Without the market, about 7.5.
3. `p_s = 15 / 90,000` dollars per gold, or $16.67 per 100k gold. The ceiling after risk is `16.67 / 1.25 = $13.33` per 100k. The bot earns 0.15 units of 100k per hour, so the farmer's hourly cost must be at least `13.33 × 0.15 = $2.00` to be priced out. That needs `0.20 + 30 / t ≥ 2.00`, so `30 / t ≥ 1.80` and `t ≤ 16.7` hours. Bans must land within about 17 hours on average.
4. The chests add items to the market pool, which raises `M` for everyone who can afford to buy from it. Their own drops become upgrades less often, even though they never paid. The loop shifts toward "farm, sell, buy" for all players.

</details>

## Lab / assignment hook

This week feeds the final economy spec (week 15), which must include an RMT policy. Use the section 3 model to justify it with numbers. Lab 12 (next week) asks you to spot bot farming in a telemetry dataset, so keep the "bots are a faucet" idea in mind.

## Sources

- Wikipedia, "Diablo III". RMAH opening 12 June 2012 (15 June in the Americas); fees of US$1 per equipment sale, 15% on commodities and a 15% cash-out fee; Jay Wilson's March 2013 comment; the 17 September 2013 announcement and 18 March 2014 closure.
- Wikipedia, "Diablo III: Reaper of Souls". Patch 2.0.1 on 25 February 2014 and Loot 2.0: fewer, better, targeted drops; most gear account-bound with limited trading windows.
- Warcraft Wiki, "WoW Token". Patch 6.1.2, Americas launch 7 April 2015, US$20 price, 30 days of game time, gold price from supply and demand, Blizzard's stated reasoning about account compromises.
- Warcraft Wiki, "Binding". Definitions of bind on pickup and bind on equip.
- EVE University Wiki, "PLEX" (current). Bought from CCP, sold for ISK on the market, 500 PLEX for 30 days of Omega time.
- CCP Games, EVE Online Monthly Economic Report (June 2024 edition as an example). Includes production, mining and destruction, money supply, faucets and sinks.
- Old School RuneScape Wiki, "Bond". Introduced 30 March 2015, US$9.99, 14 days of membership, tradable on the Grand Exchange.
- Guild Wars 2 Wiki, "Currency Exchange" (current). Gem-gold rates set by supply and demand, with a transaction fee.
- RuneScape Wiki, "Trade limit". Announced 10 December 2007, applied 2 January 2008, removed 1 February 2011 after a 91% referendum vote that closed 14 January 2011. A limit remains for never-paid new accounts.
- Wikipedia, "Gold farming". Summary of estimates of farmer numbers and market size, 2005-2009, with their original sources.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w11-self-found-upgrades.html

**Insight the visual must make obvious:** with the same drops, a player with market access gets far better gear, but almost none of their upgrades come from their own drops. The market divides the value of finding loot by `M`.

**Layout:** two linked panels, side by side on desktop, stacked on mobile.

- **Left panel, "Your best item":** x-axis drops found `j` from 1 to `n` (log scale toggle, default linear). y-axis item percentile shown as "1 in X" on a log scale (percentile `q` plotted as `1 / (1 − q)`, so 90% is "1 in 10", 99.9% is "1 in 1,000"). Two step lines: "Solo" (steel token) and "With market" (gold token). Mark each self-found upgrade with a filled dot and each purchase with a hollow dot.
- **Right panel, "Where your upgrades came from":** cumulative counts against `j`. Series: solo self-found (steel), market player self-found (green), market player purchases (gold). Overlay dashed theory curves `H(j)` and `H(j) / M`.

**Controls:**
- Market multiplier `M`: slider on a log scale, values 1, 2, 5, 10, 20, 50, 100, 200, 500, 1,000. Default 100.
- Drops `n`: 10, 100, 1,000 (buttons). Default 100.
- Seed (integer, default 11) and "New run" button. "Run 500 seasons" button that averages self-found counts and shows them next to the theory values.
- Keyboard: all controls focusable; arrow keys move the `M` slider through its values.

**Simulation (seeded PRNG, mulberry32):**
- Item power is a uniform draw on (0, 1), so power equals percentile.
- Solo: each drop `x_j`; if `x_j > best`, then `best = x_j` and count a self-found upgrade.
- With market: both players see the same `x_j` sequence. Before the market player's drop `j`, the pool gains `M − 1` other draws (skip this when `M = 1`; generate them lazily as the max of `M − 1` uniforms, which is distributed as `U^(1/(M−1))`). The market player's drop counts as self-found if `x_j > pool_max` and `x_j > best`; otherwise, if `pool_max > best`, the player buys it (count a purchase) and sets `best = pool_max`.

**Readout:** for the current run, final percentile for each player as "1 in X", self-found upgrades for each, purchases, and theory values `H(n)` and `H(n) / M` to two decimals. Also show "Expected drops to your next self-found upgrade: `1 / (1 − best)`" for each player.

**Test values:**
- `H(10) = 2.929`, `H(100) = 5.187`, `H(1,000) = 7.485`.
- `M = 10, n = 100`: theory 0.519. `M = 1,000, n = 1,000`: theory 0.0075.
- "Run 500 seasons" with `M = 1, n = 100` should average within about ±0.2 of 5.19. With `M = 10, n = 100`, within about ±0.07 of 0.52.
- Percentile table: `q = 0.9` → 10 drops, `q = 0.99` → 100, `q = 0.999` → 1,000.
