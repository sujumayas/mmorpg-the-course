# MMO401 · Week 11 — Premium Currencies and Exchange Rates

**Why this matters:** Once players can turn real money into your in-game currency through a token, your game has an exchange rate. That rate is published every minute, players watch it like a stock ticker, and it moves with every faucet you open and every store sale your business team runs. You need to know what sets it, what it tells you about your economy, and which of your own levers push it around.

**You will be able to:**
- Compute the market price of a subscription token from the currency spent on tokens and the number of tokens supplied, and derive the implied exchange rate and the implied hourly wage in real money.
- Predict the direction and size of a token-price move after a faucet change, a store sale or a new token use.
- Rewrite EVE Online's PLEX, the World of Warcraft Token, the Guild Wars 2 currency exchange and RuneScape bonds as the same three-currency triangle and say what each design chooses.
- Critique the use of a token price as an inflation gauge, and name what else moves it.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the course's assigned chapters 9-12, reading for premium currencies and exchange between game money and real money. Reread MMO304 week 11, section 3, on the black-market price band. Look up today's PLEX price in ISK on any public EVE market tracker and write it down, with the date.

**Prerequisites from earlier courses:** [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (sanctioned exchanges and the black-market price band). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (the equation of exchange). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) (EVE's market fees and the Monthly Economic Report). [MMO304 week 1, artificial scarcity](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w01-why-virtual-economies-exist-artificial-scarcity.md) (price as hours of labour). Related in the same semester: MMO403, [week 3](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w03-premium-currencies.md) (premium currencies) and [week 11](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w11-subscription-tokens.md) (subscription tokens), which cover the revenue side. This course: [week 4, monetary policy tools in games](w04-monetary-policy-tools-in-games.md), [week 7, taxes and fees as policy](w07-taxes-and-fees-as-policy.md) and [week 13, reading an economic report](w13-reading-an-economic-report.md).

**Interactive:** [The token triangle: PLEX price, money supply and the implied wage](../examples/w11-token-triangle.html)

---

## 1. A premium currency is a second money

Most MMOs now run two monies. The **soft currency** (gold, ISK, coins) is earned by playing. The **premium currency** (gems, PLEX, credits) is bought with real money. Some definitions:

- An **exchange rate** is the price of one money in another. "5 million ISK per PLEX" is an exchange rate.
- A **one-way** premium currency can be bought with real money and spent in a store, but never traded to other players. It has a posted price and no market.
- A **token** is a premium item that can be bought with money, traded to players for soft currency, and redeemed for something with a real-money value, such as game time. A token links three currencies: real money, the premium currency, and the soft currency.
- A **two-way exchange** lets players convert soft currency into premium currency and back through the game itself.
- A **peg** is a fixed exchange rate the operator guarantees. A **float** is a rate set by trading.

MMO304 week 11 asked what a token does to the black market. It sets a ceiling on what gold sellers can charge. This week asks the question from the other side. What sets the token's price, and what does that price tell the studio?

## 2. Worked example: the EVE PLEX market, one price that links two monies

### The hook

In EVE Online you can pay your subscription with ISK you earned in space. You never touch a credit card. Someone else did. They bought PLEX from CCP with real money and sold it to you on the market. You paid ISK. They got ISK to spend on ships. CCP got paid in dollars either way.

CCP introduced PLEX in November 2008. Under the current rules, 500 PLEX buys 30 days of Omega (subscriber) time, 5,500 PLEX buys a year, and 450 PLEX adds 30 days of training on a second character. PLEX also buys items in the New Eden Store. And it trades between players for ISK at whatever price the market sets.

So the PLEX price in ISK is an exchange rate between ISK and dollars. It moves every day. What moves it?

### The model

Draw a triangle with three corners: **dollars**, **PLEX** and **ISK**.

- **Dollars to PLEX** is set by CCP's store. Call the price `c` dollars per 500 PLEX. It varies by bundle and by sale, so treat it as a lever, not a constant.
- **PLEX to game time** is fixed by CCP: 500 PLEX per 30 days.
- **PLEX to ISK** floats on the player market. Call the price `P` ISK per PLEX.

The market price comes from a simple balance. Each month, players who want PLEX spend a total of `B` ISK on it. Players who bought PLEX with money sell `Q` PLEX. When the market clears:

```
P = B / Q
```

This is the equation of exchange from MMO304 week 4, applied to a single good. `B` is the ISK side and `Q` is the goods side. Write `B = s × Y`, where `Y` is the monthly ISK income of the players who buy PLEX and `s` is the share of it they spend on PLEX.

From `P` you get two derived rates that designers watch:

```
ISK per dollar       e = 500 × P / c
hours per month      H = 500 × P / w          (w = ISK a player earns per hour)
wage in dollars      W = c / H = c × w / (500 × P)
```

- `P` is the market price of one PLEX in ISK.
- `B` is ISK spent on PLEX per month, `Q` is PLEX sold per month.
- `c` is the dollar price of 500 PLEX in the store.
- `e` is the implied exchange rate, ISK per dollar.
- `w` is a player's ISK income per hour of play, `H` the hours to earn a month of Omega, `W` what that play is worth per hour in dollars.

The last line is the one players argue about. It says what an hour of ISK-farming is worth in real money, given today's PLEX price.

### Numbers you can check

The numbers below are invented round values for teaching. They are not CCP's store prices or current market data. Use `c = 20` dollars per 500 PLEX and `w = 100` million ISK per hour.

| Scenario | `B` (trillion ISK per month) | `Q` (million PLEX per month) | `P` (million ISK) | 500 PLEX (billion ISK) | `e` (million ISK per $) | `H` (hours) | `W` ($ per hour) |
|---|---|---|---|---|---|---|---|
| Base | 75 | 15 | 5.0 | 2.5 | 125 | 25 | 0.80 |
| Store sale lifts supply 50% | 75 | 22.5 | 3.33 | 1.67 | 83.3 | 16.7 | 1.20 |
| ISK incomes up 20% | 90 | 15 | 6.0 | 3.0 | 150 | 30 | 0.67 |
| New PLEX use doubles `s` | 150 | 15 | 10.0 | 5.0 | 250 | 50 | 0.40 |

Check the base row. `P = 75 × 10^12 / 15 × 10^6 = 5 × 10^6`. Then 500 PLEX cost 2.5 billion ISK, `e = 2.5 × 10^9 / 20 = 125` million ISK per dollar, and `H = 2.5 × 10^9 / 10^8 = 25` hours. Twenty dollars for 25 hours is 80 cents an hour.

Read the table as a designer.

- **A store sale is deflationary for PLEX in ISK.** More PLEX reach the market, the price in ISK falls, and ISK-rich players get cheaper game time. Your business team's sale is also a monetary event.
- **Faucet growth shows up in the PLEX price.** If ISK incomes rise 20% and nothing else changes, the PLEX price rises 20%. This is why players read the PLEX price as an inflation gauge.
- **A new use for PLEX is also a price shock.** If CCP adds something desirable that costs PLEX, `s` rises, and the price climbs even though no ISK was created. The gauge moves without any inflation.
- **The implied wage is low.** At 80 cents an hour, most players with a job earn a month of game time faster by working than by farming. That is why the market has two sides: players with more money than time sell PLEX, players with more time than money buy it.

Notice where currency goes in all this. When a player buys PLEX for ISK, the ISK moves to the seller. That is a transfer. The PLEX is later consumed for game time, which removes PLEX from the world. The only ISK sink in the trade is the market's fees. Listing an order on EVE's market carries a broker fee, 3% at base skills, and sales are taxed (MMO304 week 13 gives the current rates). A token market with no fee moves money between players and removes none.

### A visual you can move

Open the interactive. The left view is the triangle: three corners with live rates on each edge, so you can see `c`, `P`, `e` and the hours per month change together. The right view is two years of monthly PLEX prices with the ISK money supply drawn as an index on the same axis. Set ISK income growth to 2% a month and watch the two lines climb together. Then trigger a store sale in month 8. The PLEX line dips while the money line keeps rising. Finally add a "new PLEX use" in month 16. The PLEX line jumps while the money line does not. The two lines agree only when the gauge is measuring what you think.

### Cross-game recognition

Each design below is the same triangle. What differs is which edges are fixed, which float, and whether currency is destroyed when it crosses an edge.

**World of Warcraft Token (patch 6.1.2, Americas from 7 April 2015).** Bought for US$20 in the shop. Redeemed for 30 days of game time or, since February 2017, 15 dollars of Battle.net balance. It launched at 30,000 gold in the Americas. The gold price is set dynamically by the game from supply and demand, rather than by an order book. A seller receives the gold amount quoted when they list, whatever the price is when the token actually sells. In our model, Blizzard runs the `P = B / Q` balance itself and posts the result. The quote-at-listing rule removes the seller's price risk. Blizzard stated the aim as a secure, legitimate way to acquire gold, in competition with gold sellers. The Battle.net option matters. It makes the token redeemable for things beyond game time, which raises `s` exactly as the fourth row of the table does.

**Guild Wars 2 currency exchange (current).** A two-way exchange. Players convert gold to gems and gems to gold through the game. The exchange holds a supply of both, and the rate depends on the ratio between them, so each trade moves the price against the trader. The Guild Wars 2 wiki lists a transaction fee on every exchange. Because the exchange works in both directions, the fee destroys gold on one leg and gems on the other. That makes this edge of the triangle a sink that grows with trading volume, the same shape as the sales tax in week 7.

**RuneScape bonds (introduced 25 September 2013).** Bought with real money and redeemable for membership (14 days and longer periods), premium currency, bank space and more. A newly bought bond trades on the Grand Exchange. Once it has been traded it becomes untradeable, and making it tradeable again costs 10% of its Grand Exchange value in coins. That fee is a coin sink attached to every resale. Jagex taxes the edge from items back to the market, not the first sale.

**EVE PLEX (current).** Both non-fixed edges float. `c` is set by CCP's store bundles and sales, and `P` by an order-book market with broker fees and sales tax. PLEX is consumed for game time, training and store items, so the premium currency has its own sinks.

Four designs, one triangle. When you meet a new premium currency, draw the three corners, mark each edge as fixed, posted or floating, and note where a fee destroys currency. That tells you who sets the exchange rate and what it measures.

### Eyes-open design judgment

- **You are now running a currency board.** A token links your soft currency to real money. Every faucet change, sink change and store promotion moves the rate. Coordinate economy design and store planning, or one team will undo the other's work in public.
- **The token price is a noisy inflation gauge.** It measures ISK spent on tokens per token supplied. It rises with money supply, but also with new token uses, and it falls with store sales. Before you read inflation from it, correct for supply changes you caused. Better still, track a basket of ordinary goods as well (week 13).
- **A fee on the edge is a sink you can tune.** A token market with no fee is a pure transfer. A fee on listing or exchange removes currency in proportion to volume. It also widens the gap between what buyers pay and sellers get, which pushes some trade to the black market (MMO304 week 11).
- **Wealth stops meaning time.** With a token, a player's ISK can come from a credit card. Players who value status earned by play will object. Decide which goods money should never reach, and bind those.
- **The implied wage is a public number.** Players will compute `W` and post it. A very low `W` tells time-rich players their grind is worth pennies. A very high `W` invites farming for real money. Neither is wrong by itself, but you should know the figure before your community does.

### Check yourself (worked example)

1. With `c = 20` dollars, `w = 100` million ISK per hour and `Q = 15` million PLEX per month, what `B` gives a wage `W` of 1 dollar per hour?
2. A store sale cuts `c` from 20 to 15 dollars and, as a result, lifts `Q` from 15 to 20 million PLEX per month. With `B = 75` trillion, compute the new `P` and `e`. Did the ISK-per-dollar rate move up or down, and why?

<details>
<summary>Answers</summary>

1. `W = c × w / (500 × P) = 1` gives `P = 20 × 10^8 / 500 = 4 × 10^6` ISK. Then `B = P × Q = 4 × 10^6 × 15 × 10^6 = 60` trillion ISK per month.
2. `P = 75 × 10^12 / 20 × 10^6 = 3.75` million ISK. `e = 500 × 3.75 × 10^6 / 15 = 125` million ISK per dollar, unchanged from the base. The cheaper store price and the lower market price cancel exactly here. A buyer of PLEX with dollars gets the same ISK per dollar, while an ISK-rich buyer of game time pays 25% less.

</details>

## 3. Pegs, floats and who carries the risk

A premium currency can link to soft currency in three ways. The choice decides who absorbs shocks.

**Pegged.** The studio sells soft currency at a fixed rate, for example "100 gems = 10,000 gold". The studio is then a gold faucet with a cash register attached. Every gem converted creates gold from nothing. If the studio inflates its own faucets, the peg makes buying gold cheaper in real terms, so players buy more, which inflates further. A peg removes rate risk from players and hands all of the monetary risk to the studio.

**Floating through players.** Tokens such as PLEX and bonds. No soft currency is created. Gold moves from one player to another. The rate absorbs shocks, so the studio's monetary risk is small. The cost is volatility: a sudden supply change can move the price a great deal in a week, and players who planned their subscription around it complain.

**Posted by the studio from supply and demand.** The WoW Token. The studio smooths the price and guarantees the seller's quote. It carries a little risk, since it must hold inventory between listing and sale, but players see a calmer price.

Here is a numerical feel for volatility under a float. Take the base case, `B = 75` trillion and `Q = 15` million. Suppose the store runs a sale for one week that adds 3 million PLEX to that month's supply. The monthly price falls to `75 / 18 = 4.17` million, a drop of about 17%. If the sale is announced a month ahead, speculators buy PLEX before the sale and sell during it. That spreads the effect over two months and smooths the drop. Traders who absorb price moves this way do the studio a favour, and the market fees you charge are what they pay for the privilege.

### When the exchange runs both ways

A two-way exchange, like Guild Wars 2's, lets players move soft currency into premium currency. That turns the premium currency into a store of value for gold. If gold inflates, players convert into gems to protect their savings, which raises the gem price in gold further. That is a feedback loop, and the exchange fee is the friction that damps it. With a fee of `f` on each leg, a round trip costs roughly `2f` of the value. With `f = 0.15`, a round trip loses about 28% (`1 − 0.85^2 = 0.2775`), enough to stop casual speculation. When you design a two-way exchange, pick `f` from the round-trip loss you want, not from a revenue target.

## 4. Premium currency sinks and the second money supply

Everything you learned about faucets and sinks in MMO304 week 3 now applies twice. Premium currency has a supply too.

- **Premium faucets:** store purchases, and any premium currency the game gives away (login rewards, event prizes).
- **Premium sinks:** redemption for game time, store items, fees on the premium edge.
- **Premium stock:** unspent premium currency sitting in wallets. Accountants treat it as a liability, because the studio still owes the service it was sold for.

Suppose players buy 15 million PLEX a month and redeem 14 million for game time and store items. The stock in wallets grows by 1 million a month. Such a stock matters for two reasons. First, it is an overhang: if CCP added a desirable PLEX-priced item, a year of this build-up, 12 million PLEX, could be spent at once, a shock like the fourth row of the table. Second, if PLEX is used as a store of value by ISK-rich players, some ISK is effectively parked in PLEX, which lowers the ISK velocity you measure.

Treat the premium stock as part of your money supply when you read reports. In week 13 you will read a real monthly economic report that tracks it.

## In-class activity (25 minutes)

In pairs, you are the economy team of an MMO launching a token next quarter. Soft currency is gold.

1. Draw the triangle. Choose, for each edge, fixed, posted or floating. Justify each in one sentence.
2. Your telemetry says token buyers earn a total of 40 billion gold per month and will spend about 10% of it on tokens. The business team expects to sell 200,000 tokens per month at $15 each. Compute the launch gold price per token, `e` in gold per dollar, and the implied wage `W` for a player earning 20,000 gold per hour.
3. The business team proposes a "double tokens" week in month 3 that would sell 100,000 extra tokens. Predict the gold price that month. Propose one change, either to timing or to announcing it early, that would soften the drop.
4. Decide on a fee on the token edge. State what it removes per month at launch and what it does to the gap with the black market.

Expected output: an annotated triangle, the three numbers from step 2 (answer: 20,000 gold per token, about 1,333 gold per dollar, and $15 per hour), a predicted price from step 3 (about 13,333 gold), and a one-paragraph fee decision.

## Common misconceptions

- **"Players buying tokens for gold means the studio is printing gold."** With a token, gold moves from buyer to seller. No gold is created. Only a pegged sale of soft currency creates it.
- **"The token price is the inflation rate."** It moves with inflation, but also with token supply and with every new use of the token. Correct for those before you read inflation from it.
- **"A store sale is only a revenue decision."** It raises token supply, lowers the token price in soft currency, and changes the implied wage. It is also a monetary decision.
- **"Two-way exchanges are strictly better for players."** They let players hedge inflation, but they also create a feedback loop from gold inflation to premium demand. The fee that damps it costs every player who converts.

## Check yourself

1. A game's token sells for 400,000 gold, costs 20 dollars and grants 30 days of play. A player earns 25,000 gold an hour. How many hours of farming buy a month, and what is the implied wage?
2. Over a quarter, gold incomes of token buyers rise 15% while token supply rises 5%. Estimate the change in the token's gold price. How much of it would you blame on inflation?
3. A two-way exchange charges 10% on each leg. What share of value does a round trip lose? Your economist wants round trips to lose at least 30%. What fee per leg does that need?
4. Classify the RuneScape bond's 10% re-tradeability fee: faucet, sink or transfer, and of which currency? Why might Jagex put the fee on resale rather than on the first sale?

<details>
<summary>Answers</summary>

1. `H = 400,000 / 25,000 = 16` hours, so `W = 20 / 16 = 1.25` dollars per hour.
2. `P = B / Q`, so the price scales by `1.15 / 1.05 ≈ 1.095`, about +9.5%. The 15% income rise is the inflation signal. The 5% supply rise hides part of it, so the token alone understates inflation.
3. `1 − 0.9^2 = 0.19`, so 19%. For 30%, `(1 − f)^2 = 0.7` gives `1 − f ≈ 0.837`, so `f ≈ 16.3%` per leg.
4. It is a coin sink. Coins are destroyed and nothing is created. Putting it on resale leaves the first, real-money sale frictionless for buyers and sellers, and taxes speculators who trade bonds repeatedly.

</details>

## Lab / assignment hook

[Lab 11, a token market in an agent-based economy](../labs/lab11.md). You add a token market to the course's agent-based economy: cash-rich agents buy tokens and sell them for gold, time-rich agents buy them with gold. You run a faucet increase, a store sale and a new token use, and show which of the three the token price can and cannot distinguish. This is part of the ABM labs component (40%).

## Sources

- EVE University Wiki, "Accounts", section on PLEX (current). 500 PLEX for 30 days of Omega, 5,500 PLEX for a year, 450 PLEX for 30 days of Multiple Character Training, use in the New Eden Store, trade to players for ISK at a floating price, and a 3% base broker fee when listing.
- Wikipedia, "Eve Online" (retrieved September 2026). PLEX introduced in November 2008 as an in-game item that extends a subscription by 30 days, bought for real money and sold on the market for ISK; selling ISK for money is prohibited.
- Warcraft Wiki, "WoW Token" (current). Introduced in patch 6.1.2, Americas on 7 April 2015 at 30,000 gold; US$20; 30 days of game time; Battle.net balance option added February 2017 (US$15); gold price set dynamically from supply and demand; seller receives the gold quoted at listing; Blizzard's stated aim of a secure, legitimate way to get gold.
- Guild Wars 2 Wiki, "Currency Exchange" (current). Two-way gold and gem exchange with a rate set by the supply of each held by the exchange, and a transaction fee on trades.
- RuneScape Wiki, "Bond" (current). Introduced 25 September 2013; redeemable for membership and other benefits; tradeable on the Grand Exchange when newly bought; re-tradeability costs 10% of Grand Exchange value in coins.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w11-token-triangle.html

**The one insight:** the token's price in soft currency is ISK spent on tokens divided by tokens supplied. It tracks the money supply only when supply and token uses stay fixed. A store sale pulls it down and a new token use pushes it up without any inflation, so the student sees the price line and the money-supply line agree, then separate.

**Layout.** Two panels side by side on desktop, stacked on mobile with the triangle first. Readout table below.

**Left panel, the triangle.** Three labelled nodes: Dollars, PLEX, ISK. Edge Dollars to PLEX shows `c` per 500 PLEX. Edge PLEX to game time (a small fourth node "30 days") shows "500 PLEX, fixed". Edge PLEX to ISK shows `P` in million ISK. A derived label across the Dollars to ISK side shows `e` in million ISK per dollar. Under the triangle: "Hours of play per month `H`" and "Wage `W` in $ per hour", in large type. All values update for the month selected on the right panel (default: latest month).

**Right panel, 24 months.** x-axis month 0 to 24. Line 1: `P(t)` in million ISK. Line 2: money index `B(t) / B(0) × P(0)` drawn on the same axis as a dashed line, labelled "if price followed money only". Event markers as vertical bands for the store sale and the new use. A slider or click on the chart selects the month shown in the triangle.

**Controls.**
- `c` store price per 500 PLEX: 5 to 40 dollars, step 1, default 20.
- `B(0)` ISK spent per month at month 0: 20 to 200 trillion, step 5, default 75.
- Monthly ISK income growth `g`: −5% to +10%, step 0.5%, default 2%.
- `Q` base supply: 5 to 40 million PLEX per month, step 0.5, default 15.
- Store sale: toggle, month (1-24, default 8), supply boost (0-100%, default 50%). Applies to that month only.
- New PLEX use: toggle, month (default 16), multiplier on `s` from that month on (1.0-3.0, default 2.0).
- `w` ISK per hour: 10 to 500 million, step 10, default 100.

**Model.** `B(t) = B(0) × (1 + g)^t × (new-use multiplier if t ≥ use month)`. `Q(t) = Q × (1 + boost if t = sale month)`. `P(t) = B(t) / Q(t)`. `e = 500 × P / c`. `H = 500 × P / w`. `W = c / H`.

**Readout table** (copyable, for the selected month): `B`, `Q`, `P`, 500 PLEX in ISK, `e`, `H`, `W`, and the gap between `P` and the money-only line in percent.

**Test values.**
- Month 0, defaults: `P = 5.0` million, 500 PLEX = 2.5 billion, `e = 125` million per dollar, `H = 25`, `W = 0.80`.
- `g = 0`, sale in month 8 with 50% boost: month 8 `P = 3.33` million, `H = 16.7`, `W = 1.20`; month 9 back to 5.0.
- `g = 0`, new use ×2 from month 16: `P = 10.0` million, `H = 50`, `W = 0.40`, gap to the money-only line +100%.
- `g = 2%`, no events: month 12 `P = 5 × 1.02^12 = 6.34` million.

**Accessibility.** Keyboard-operable controls with visible focus. Triangle values in text, not only in graphics. Price and money lines distinguished by dash and label. No animation when `prefers-reduced-motion` is set.
