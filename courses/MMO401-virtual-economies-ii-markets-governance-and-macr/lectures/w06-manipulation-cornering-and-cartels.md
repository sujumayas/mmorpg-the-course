# MMO401 · Week 06 — Manipulation: Cornering and Cartels

**Why this matters:** Sooner or later a player or a guild will buy every unit of something your raiders need and relist it at three times the price. Your forums will demand a ban. Before you act, you need to know whether the corner will collapse on its own in two days or hold for a month, and whether the real problem is one trader or a group of producers who agreed to stop competing. This lecture gives you the arithmetic to tell those cases apart and the levers to make your markets harder to push around.

**You will be able to:**
- Compute the cost of cornering a market from its order book and the corner's profit as a function of the hold price and the supply lag.
- Derive the break-even supply lag for a corner and use it to evaluate design levers (vendor price ceilings, buy limits, alternative sources).
- Compute cartel, cheating and competitive payoffs in a Cournot model and the patience a cartel needs to hold together.
- Design detection signals and interventions for market manipulation and critique them for false positives and player trust.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the market-design and player-institutions material within the course's assigned range, ch. 9-12. Skim the Wikipedia article "Silver Thursday" for the 1979-1980 silver market.

**Prerequisites from earlier courses:** [MMO401 week 5, order books and spreads](w05-market-microstructure-order-books-and-spreads.md) (walking the book, depth, buy limits). [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (the prisoner's dilemma shape). [MA101 week 3, quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (the peak of a downward parabola). [MMO304 week 6, supply and demand in auction houses](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md).

**Interactive:** [Corner calculator](../examples/w06-corner-calculator.html). Keep it open during section 2.

---

## 1. What counts as manipulation

Economists use **market manipulation** for trading that makes money by distorting prices rather than by providing goods or services. Three patterns show up in every game with a player market.

- A **corner** is when one trader buys enough of an item's available supply to set its price, then sells back at a higher price to players who need it.
- A **cartel** is a group of producers who agree to limit output or fix prices so all of them earn more than they would by competing.
- **Front-running** and **pump-and-dump** are schemes that exploit information. Front-running means buying ahead of a buyer you know is coming. Pump-and-dump means talking a price up and selling into the rush.

Not all of this is banned in all games. Many sandbox games treat cornering and cartels as legitimate play, and players who pull them off become legends. Other games treat them as abuse. Whether manipulation breaks your rules is a governance question, and MMO402 covers the ethics and the terms of service side. This lecture is about the economics. When does manipulation work, how much does it cost players, and which design choices make it harder? You need those answers whichever policy you pick.

## 2. Worked example: can you corner this market?

### The hook

In 1979 the Hunt brothers and their associates accumulated about 195 million troy ounces of silver. Silver had traded below $10 an ounce before August 1979. In January 1980 it passed $50. On 7 January 1980 the exchange (COMEX) imposed position limits on silver futures. On 21 January it allowed only trades that closed positions or were genuine hedges. On 27 March 1980, the day now called Silver Thursday, silver closed at $10.80. The Hunts could not meet their margin calls.

The same shape plays out every week in some MMO. A trader buys every listing of a crafting reagent the day before a raid tier opens and relists at triple the price. For a few days it works. Then the price falls back and the trader is left holding stock they overpaid for.

Why do some corners pay and others lose money? The answer is one number, the **supply lag**, meaning how long it takes new supply to reach the market once the price rises.

### The model

A trader buys the whole ask side of an item's book, which we call the **float**, and then holds a higher price for a while. Here are the pieces.

- The float is `F` units, bought by walking the ask ladder at total cost `C`. From week 5, `C` is the sum of price times quantity over every ask level.
- `P_0` is the normal market price, the price the item returns to once supply comes back.
- The **premium** is `C − F × P_0`, how much more than normal value the trader paid for the float by walking up the ladder.
- Demand per day at price `P` is `D(P) = a − bP`. Players who need the item keep buying, fewer of them as the price rises.
- `L` is the supply lag, in days. During the lag, no new supply arrives. After it, gatherers and other sellers flood back and the price returns to `P_0`. Any unsold float is then only worth `P_0` each.

The trader chooses a hold price `P` and sells to demand at that price for `L` days. They sell `D(P) × L` units, or the whole float if that comes first. The rest is sold at `P_0` after the lag.

```
units sold at P  = min(F, D(P) × L)
profit(P, L)     = P × units sold + P_0 × (F − units sold) − C
```

When the float is not used up during the lag, this simplifies to

```
profit(P, L) = (P − P_0) × D(P) × L − premium
```

The first term is a daily **markup income** times the number of days. The second is the entry fee the trader paid to get control. The markup income `(P − P_0)(a − bP)` is a downward parabola in `P`, as in MA101 week 3, with its peak halfway between `P_0` and the price where demand hits zero.

```
best hold price  P* = (P_0 + a/b) / 2
break-even lag   L* = premium / max daily markup income
```

A corner pays only if the supply lag is longer than `L*`.

### Numbers you can check

Take a crafting reagent with a normal price of `P_0 = 10`. Its ask side holds 1,000 units in ten levels of 100, at 9.0, 9.5, 10.0, and so on up to 13.5. Walking the whole ladder costs

```
C = 100 × (9.0 + 9.5 + ... + 13.5) = 100 × 112.5 = 11,250
premium = 11,250 − 1,000 × 10 = 1,250
```

Demand is `D(P) = 250 − 10P`. At the normal price, players buy 150 a day. Demand hits zero at 25.

The best hold price is `(10 + 25) / 2 = 17.5`. At 17.5, players buy `250 − 175 = 75` a day, and each sale earns `17.5 − 10 = 7.5` above normal. The maximum daily markup income is `7.5 × 75 = 562.5`. So the break-even lag is `1,250 / 562.5 ≈ 2.2` days.

| Supply lag `L` (days) | Best hold price | Units sold at hold price | Profit |
|---|---|---|---|
| 1 | 17.50 | 75 | −687.5 |
| 2 | 17.50 | 150 | −125.0 |
| 3 | 17.50 | 225 | +437.5 |
| 5 | 17.50 | 375 | +1,562.5 |
| 7 | 17.50 | 525 | +2,687.5 |
| 14 | 17.86 | 1,000 (float sold out) | +6,607 |

Check the `L = 3` row: `7.5 × 75 × 3 − 1,250 = 1,687.5 − 1,250 = 437.5`. In the `L = 14` row the float runs out before the lag ends, so the trader raises the price until `D(P) × 14 = 1,000`. That gives `P = 25 − 1,000/140 ≈ 17.86` and profit `17.86 × 1,000 − 11,250 ≈ 6,607`.

Now the part a designer cares about. Here is what four design levers do to the same corner.

| Scenario | Max daily markup income | Premium | Break-even lag `L*` | Profit at `L = 3` |
|---|---|---|---|---|
| Baseline | 562.5 at `P = 17.5` | 1,250 | 2.2 days | +437.5 |
| NPC vendor sells the item at 12 (a price ceiling) | 260 at `P = 12` | 1,250 | 4.8 days | −470 |
| Gatherers overshoot, price falls to 8 after the lag | 722.5 at `P = 16.5` | 3,250 | 4.5 days | −1,082.5 |
| A second source keeps supplying 50 a day | 250 at `P = 15` | 1,250 | 5.0 days | −500 |

Check the vendor row. A vendor selling at 12 means nobody pays more than 12, so the best hold price is 12 and daily income is `(12 − 10) × (250 − 120) = 2 × 130 = 260`. Break-even lag `1,250 / 260 ≈ 4.8`.

Check the overshoot row. If the price after the lag is 8, the unsold float is worth 8 a unit, so the premium becomes `11,250 − 8,000 = 3,250`. The markup is measured from 8, so the best hold price is `(8 + 25)/2 = 16.5` and daily income is `8.5 × 85 = 722.5`.

Check the second-source row. If 50 units a day arrive from another source whatever the price, the cornerer sells only `D(P) − 50 = 200 − 10P` a day. The best price is `(10 + 20)/2 = 15`, and daily income is `5 × 50 = 250`.

Every lever works by pushing `L*` above the real supply lag. None of them bans anything.

### The visual

Open the interactive. The left view plots profit against hold price, one curve per supply lag. At short lags every curve sits below zero. As you drag the lag slider up, the curve lifts until its peak crosses zero at `L ≈ 2.2` days. The right view is a timeline for your chosen hold price. The price sits at the hold level for `L` days, then drops back. The cornerer's inventory falls during the lag, and the leftover is marked at `P_0`. Now switch on the vendor ceiling and watch the whole family of curves flatten and cut off at 12. The corner that paid at three days now loses at five.

### Cross-game recognition

**The 1979-1980 silver market.** Rewrite it in the model's terms. The Hunts' float was the silver they bought. Their premium grew as prices rose during the buying. What ended the corner early was the exchange changing the rules in January 1980. Position limits capped how much more anyone could buy, and liquidation-only trading stopped new buying of futures altogether. That cut the effective lag short. Heavy leverage added a holding cost the simple model ignores, and margin calls forced a sale at the worst time. The market operator acted like a game developer patching the market, and it did not need to prove intent first.

**Old School RuneScape (Grand Exchange, current).** Every item has a buy limit per account every four hours (week 5). A would-be cornerer cannot walk the whole book at once. They have to buy the float in slices over many four-hour windows, and while they buy, the rising price draws sellers in and tells other traders what is happening. In model terms the buy limit raises the premium, because the float refills as they buy it, and shortens the effective lag, because supply starts responding before the corner is complete.

**EVE Online (regional markets, current).** Each region has its own order book. Cornering an item in one region's main trade hub works only until traders haul the same item in from other regions. The supply lag `L` is literally the hauling time plus the time for traders to notice the gap. Regional markets make corners easier, since each book is thinner, and self-limiting, since arbitrage supplies the missing units after a travel delay. Week 9 treats travel time as a design parameter.

**World of Warcraft (retail, crafting reagents sold by NPC vendors).** When an NPC vendor sells an item at a fixed price, that price is a hard ceiling on the player market. Nobody pays a player 30 for something a vendor sells for 12. This is the vendor-ceiling row of the table. The trade-off is that the vendor price also caps what gatherers can earn, so you remove a corner risk and a gathering career at the same time.

Four settings, one question. How long before new supply reaches the market, and is it longer than the premium divided by the markup income?

### Design judgment, eyes open

- **Short supply lags are the best defense.** Multiple sources, crafting substitutes and fast respawn times all shorten `L`. They also make the item less interesting to gather, because nobody's supply matters much.
- **Price ceilings work and cost something.** A vendor ceiling kills corners above its price. It also caps gatherer income and pins your economy to a fixed number that inflation (week 4) will slowly make irrelevant. If you use one, index it to your price level.
- **Buy limits slow corners but not alts.** Limits per account can be dodged with more accounts. They work best when paired with detection (section 4).
- **Thin books are the target.** Corners happen in items with small float relative to demand, where the premium is low. Your most at-risk items are niche reagents needed by many players at the same time, such as a new tier's consumables. Watch those in the first week of a patch.
- **A failed corner is a sink for the cornerer and a gift to sellers.** Players who sold into the corner earned above-normal prices. Before you intervene, check who lost. If it was the cornerer, the market may have handled it.

### Check yourself (worked example)

1. In the baseline, the supply lag is 4 days. What is the best profit?
2. With a 7-day lag, what is the highest NPC vendor price that still makes the corner unprofitable?

<details>
<summary>Answers</summary>

1. `562.5 × 4 − 1,250 = 1,000`. The trader sells `75 × 4 = 300` units at 17.5, which fits inside the float.
2. With a ceiling `c` below 17.5, the best hold price is `c`. The corner is unprofitable when `(c − 10)(250 − 10c) × 7 < 1,250`. Put `x = c − 10`. Then `x (150 − 10x) < 178.6`, which holds for `x` below about 1.30. So any vendor price below about 11.30 makes the corner lose money.

</details>

## 3. Cartels: agreeing not to compete

A corner is one trader controlling supply that already exists. A cartel is several producers controlling supply that has not been made yet. The economics are older than games. Augustin Cournot modelled competing producers in 1838, and the model still gives the cleanest numbers.

### The Cournot model

Two producers sell the same good. The market price falls as total output rises, `P = A − B × Q`, where `Q` is total output per day. Each unit costs `c` to produce. Each producer picks its own output to maximize its own profit, `(P − c) × q`.

Use `A = 100`, `B = 1`, `c = 10`. There are three outcomes to compare.

- **Cartel.** The producers act as one monopolist and split the output. The monopoly output is `(A − c) / (2B) = 45`, so each makes 22.5. The price is `100 − 45 = 55`. Each earns `(55 − 10) × 22.5 = 1,012.5`.
- **One cheats.** One producer keeps to 22.5. The other picks the output that is best for itself given that, `(A − c − 22.5) / 2 = 33.75`. Total output is 56.25, the price is 43.75. The cheater earns `33.75 × 33.75 ≈ 1,139`. The loyal member earns `33.75 × 22.5 ≈ 759`.
- **Competition.** Both produce the Cournot quantity `(A − c) / (3B) = 30`. Total 60, price 40. Each earns `30 × 30 = 900`.

Put these in a payoff matrix, as in MMO303 week 10 (row player's payoff first).

| | Other keeps quota | Other cheats |
|---|---|---|
| **Keep quota** | 1,012.5 , 1,012.5 | 759 , 1,139 |
| **Cheat** | 1,139 , 759 | 900 , 900 |

This is a prisoner's dilemma. Whatever the other does, cheating pays more for you. Both cheat, and both end up with 900 instead of 1,012.5. Cartels are unstable for the same reason every prisoner's dilemma is.

The real-world record agrees. OPEC, founded in Baghdad in 1960, sets production quotas for its members. Political scientist Jeff Colgan's analysis, cited on Wikipedia, found members cheated on 96% of their commitments between 1982 and 2009.

### What holds a cartel together

The dilemma is for one round. Producers in a game meet every day. If a member knows that cheating today means everyone competes forever after, the choice is between 1,012.5 every day and 1,139 once followed by 900 every day. Let `δ` (delta) be how much a member values tomorrow's profit compared with today's, between 0 and 1. Staying loyal is better when

```
1,012.5 / (1 − δ) ≥ 1,139 + δ × 900 / (1 − δ)
δ ≥ (1,139 − 1,012.5) / (1,139 − 900) ≈ 0.53
```

So the cartel holds if members care about the future at least about half as much as the present. More members make it harder. With three producers the same calculation needs `δ ≥ 0.57` (check yourself question 3).

Games change this calculation in two ways real markets usually do not.

- **Punishment can be direct.** In a game with territory and combat, a cartel can punish a cheater by force rather than by price war. That makes cheating much more expensive, which is the same as raising the loyalty payoff. In EVE Online since the Lifeblood expansion (24 October 2017), moon ore is extracted by refinery structures that players anchor at moons. Whoever holds the space around a moon controls its output, so control of a resource can be defended with fleets.
- **Entry can be blocked.** A real cartel breaks when outsiders start producing. In a game, if production needs territory, outsiders must fight their way in. The cartel's durability depends on your map design, not on economics alone.

### What designers can do about cartels

A cartel concentrates production. The cleanest defenses spread it out.

- **Distribute the resource.** If a critical input exists in many places, controlling all of them is expensive. In March 2020, CCP changed how moon ores were distributed across all types of space in EVE Online. Whatever the motive, changing where a resource exists is the strongest lever on who can control it.
- **Offer substitutes.** A recipe that accepts either of two inputs caps the cartel's price at the cost of the substitute.
- **Leave an NPC source at a high price.** Like the vendor ceiling in section 2, it caps the cartel's price without removing player production.
- **Or accept it.** In a sandbox, a cartel that holds territory is content. Players fight wars over it. If your game is about player politics, a cartel may be the point. Decide deliberately, and make sure the damage lands on players who chose to play that game.

## 4. Detecting manipulation

You cannot intervene against what you cannot see. Order-book data (week 5) gives you several signals. None proves intent. Each is a reason to look.

- **Concentration of purchases.** The share of an item's buy volume in a day that came from one account or one group of linked accounts. A corner shows up as one buyer taking most of the float. The **Herfindahl-Hirschman Index (HHI)**, the sum of squared market shares, is a standard concentration measure. With shares in percent, one buyer taking everything gives 10,000, and ten equal buyers give 1,000.
- **Book emptied, then refilled higher.** Most of the ask side disappears within an hour and reappears at a much higher price.
- **Sales concentration by seller.** The same test on the sell side detects cartels. A few sellers supplying nearly all units at matched prices is a warning sign, especially if their prices move together.
- **Trades ahead of announcements.** Buying spikes in an item shortly before a patch note that raises its demand suggest leaked information. Your own staff are the most likely source, which is a governance problem for your studio, not only for players.

Build these as dashboard alerts with thresholds, then review them by hand. Automatic punishment on a concentration signal will catch honest players. A guild buying supplies for forty raiders looks like a corner.

### Front-running and pump-and-dump, briefly

Front-running needs advance knowledge of a large buyer. In a game, the largest predictable buyer is often the developer. If you run an item sink (week 4) whose purchases react to prices in ways players can predict, anyone who guesses the next purchase can buy ahead and sell to you. A fixed weekly quantity, which is how the Old School RuneScape Wiki describes that game's item sink, leaves little to guess. The same logic applies to announced crafting changes. Once patch notes say an item becomes an input, its price moves before the patch lands.

Pump-and-dump needs a crowd that can be talked into buying. It thrives on items with thin books and on price-tracking sites that highlight "rising" items. Showing a longer price history next to the current price makes pumps easier to spot for ordinary players.

## In-class activity (25 minutes)

Groups of four play a cartel game for six rounds.

1. Each player is a producer in a Cournot market with `P = 100 − Q` and cost 10 per unit. The group first discusses and may agree on quotas.
2. Each round, every player secretly writes an output between 0 and 45 on a card. The instructor reveals the cards, computes `Q`, `P` and each player's profit, and writes them on the board.
3. After round 3, the instructor announces that from now on, any player may pay 100 profit to "attack" another, which removes 150 from the target's profit that round.
4. After round 6, each group computes average profit per player and compares it with the four-player cartel (monopoly output 45, split four ways) and the four-player Cournot outcome (each makes 18, price 28).

Expected output: a round-by-round table and a two-sentence account of how the attack rule changed cheating. Check your targets. The four-player cartel earns `45 × 45 / 4 = 506.25` each. The Cournot outcome earns `18 × 18 = 324` each.

## Common misconceptions

- **"Anyone with enough gold can corner any market."** Gold buys the float, but profit needs a supply lag longer than `L*`. In items with fast supply response, rich cornerers simply lose money faster.
- **"A price ceiling is the only real fix."** Buy limits, second sources, substitutes and faster respawns all raise `L*` or shorten `L`. The ceiling is the bluntest option, and it caps honest earnings too.
- **"Cartels are stable because everyone gains."** Everyone gains together, but each gains more by cheating. Cartels last only when the future matters enough or cheating can be punished.
- **"High concentration proves manipulation."** Concentration is a signal. Guilds, crafters and resellers can all be concentrated for legitimate reasons. Review before you punish.

## Check yourself

1. In the baseline corner, the ladder is flatter. All 1,000 units are listed at 10.25, so `C = 10,250`. What is the premium and the break-even lag?
2. A designer adds a second source of 100 units a day to the baseline. What is the best hold price, the daily markup income, and `L*`? What happens to the corner if the second source supplies 150 a day?
3. Three identical producers face `P = 100 − Q` with cost 10. Compute each member's profit under a cartel (equal split), under Cournot competition, and for one cheater when the other two keep quota. What patience `δ` keeps the cartel together?
4. A concentration alert fires. One account bought 90% of an herb's volume in an hour. Name two facts you would check before acting, and what each would tell you.

<details>
<summary>Answers</summary>

1. Premium `10,250 − 10,000 = 250`. `L* = 250 / 562.5 ≈ 0.44` days. A flat, shallow ladder makes the corner cheap to enter, so even a short lag pays.
2. The cornerer sells `D(P) − 100 = 150 − 10P`. Markup income is `(P − 10)(150 − 10P)`, which peaks halfway between 10 and 15, at 12.5. Daily income `2.5 × 25 = 62.5`, so `L* = 1,250 / 62.5 = 20` days. With 150 a day, the cornerer sells `100 − 10P`, which is zero at 10. They can never sell above the normal price, so the corner always loses its premium.
3. Cartel: output 45 split three ways, 15 each, price 55, profit `45 × 15 = 675` each. Cournot: each makes `90/4 = 22.5`, price 32.5, profit `22.5 × 22.5 = 506.25` each. Cheater's best response to 30 from the others is `(90 − 30)/2 = 30`, so `Q = 60`, `P = 40`, cheater earns `30 × 30 = 900`, each loyal member `15 × 30 = 450`. `δ ≥ (900 − 675) / (900 − 506.25) = 225 / 393.75 ≈ 0.57`.
4. Whether the account is linked to a guild whose raid schedule matches the purchase, which would suggest legitimate supply buying. Whether the account relisted the item at a higher price soon after, which would suggest a corner. The price history before and after, and whether the buyer traded ahead of a patch announcement, are also good answers.

</details>

## Lab / assignment hook

[Lab 06, corner and cartel simulation](../labs/lab06.md). Using your week 5 matching engine, you add a cornering agent and a group of producer agents with a quota agreement, run both across a grid of supply lags and patience values, and write a one-page recommendation on which defenses to ship for a given item. This feeds the final agent-based economy and policy memo.

## Sources

- Wikipedia, "Silver Thursday" (accessed September 2026). Holdings of about 195 million troy ounces by end of 1979; price below $10 before August 1979 and above $50 in January 1980; COMEX position limits on 7 January 1980 and liquidation-only trading from 21 January; close of $10.80 on 27 March 1980; margin calls.
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Buy limits per account every four hours; the item sink's fixed, Jagex-specified weekly quantities.
- EVE University Wiki, "Trading" (current). Each region has its own market. EVE University Wiki, "Moon mining". Lifeblood released 24 October 2017, replacing starbase moon harvesting with refinery structures; moon ore distribution changed across all types of space on 30 March 2020.
- Wikipedia, "OPEC" (accessed September 2026). Founded 14 September 1960 in Baghdad; production quotas; Jeff Colgan's finding that members cheated on 96% of commitments from 1982 to 2009.
- Cournot, A. (1838). *Recherches sur les principes mathématiques de la théorie des richesses*. Paris.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- The reagent, its ladder, its demand curve and the Cournot parameters are invented for teaching.

## Interactive spec: examples/w06-corner-calculator.html

**The one insight:** a corner pays only if the supply lag is longer than the break-even lag `L* = premium / max daily markup income`, and every defensive lever works by raising `L*` or shortening the real lag.

**Layout.** Two linked views plus controls. Mobile: controls, then view 1, then view 2, stacked. Desktop: controls on the left, views side by side.

**Controls** (sliders with visible numeric values, keyboard-operable):
- Supply lag `L`, 0.5 to 21 days, step 0.5 (default 3).
- Normal price `P_0`, fixed at 10 for the ladder, plus "price after the lag" `P_after`, 6 to 12 step 0.5 (default 10).
- Ladder shape: "Lecture ladder" (100 units each at 9.0, 9.5, ..., 13.5), "Flat" (1,000 at 10.25), "Steep" (100 units each at 9, 10, 11, ..., 18).
- Demand intercept `a` (default 250) and slope `b` (default 10), as number inputs.
- Toggle "NPC vendor ceiling" with price input (default 12).
- Second-source supply `s`, 0 to 200 units per day, step 10 (default 0).
- A "hold price" slider for view 2, 10 to 25 step 0.1, with a "use best" button.

**Computation.**
- `F` = sum of ladder quantities; `C` = sum of price × quantity.
- Net daily sales at hold price `P`: `n(P) = max(0, a − bP − s)`. If the ceiling is on, `P` is limited to the ceiling.
- `sold(P) = min(F, n(P) × L)`. `profit(P) = P × sold + P_after × (F − sold) − C`.
- Best price: search `P` from `P_after` to the ceiling or `a/b`, step 0.01, and report the maximum.
- `L*`: the smallest `L` (search step 0.01) for which the best profit is ≥ 0, or "never" if no `L` up to 60 works.

**View 1, profit vs hold price.** X axis hold price, y axis profit, with a zero line. Draw curves for `L` = 1, 2, 3, 5, 7 in muted colors and the current `L` in the accent color. Mark the best price and its profit on the current curve.

**View 2, timeline.** X axis days 0 to `L + 5`. Top: price (hold price during `[0, L]`, then `P_after`). Bottom: cornerer inventory (starts at `F`, falls by `n(P)` per day, clamps at 0, and the remaining units are shown as a marked-down block at day `L`).

**Readouts.** `F`, `C`, premium `C − F × P_after`, best hold price, daily markup income at best price, units sold during the lag, profit, `L*`.

**Test values (lecture ladder, a = 250, b = 10, P_after = 10, no ceiling, s = 0 unless stated).**
- `C = 11,250`, `F = 1,000`, premium 1,250, best price 17.5, daily markup 562.5, `L* = 1,250 / 562.5 ≈ 2.22` (the 0.01-step search reports 2.23, the first grid value with profit ≥ 0; either display is acceptable if labelled).
- `L` = 1, 2, 3, 5, 7 give profit −687.5, −125, 437.5, 1,562.5, 2,687.5. `L = 14` gives best price ≈ 17.86 and profit ≈ 6,607.
- Ceiling 12: daily markup 260, `L* ≈ 4.81`, profit at `L = 3` is −470.
- `P_after = 8`: premium 3,250, best price 16.5, daily markup 722.5, `L* = 4.5`, profit at `L = 3` is −1,082.5.
- `s = 50`: best price 15, daily markup 250, `L* = 5.0`, profit at `L = 3` is −500.
- `s = 100`: best price 12.5, daily markup 62.5, `L* = 20`. `s = 150`: "never".
- Flat ladder: premium 250, `L* ≈ 0.44`.

**Caption** under view 1, updating live: "Supply returns in L days. The corner needs at least L* days. Profit: X."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Readouts duplicate every plotted number. Respect `prefers-reduced-motion`. No logos or game art; the item is a generic "reagent".
