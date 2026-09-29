# MMO403 · Week 11 — Subscription Tokens

**Why this matters:** A subscription token lets one player pay for another player's game time. To players it looks like a way to play for free. To the studio it is a pricing decision, a retention tool and a promise that the game's gold will now have a dollar value, all at once. This week you learn to compute what a token does to revenue, which two unknowns decide whether it pays, and what it changes about who your customer is.

**You will be able to:**
- Compute the monthly revenue change from adding a token, given the token price, the subscription price, the months paid with tokens, and the two unknowns `k` (would they have paid anyway?) and `σ` (did the token dollars come from elsewhere in your store?).
- Derive the break-even substitution rate and explain why a token priced above the subscription cannot lose game-time revenue on its own.
- Rewrite the World of Warcraft Token, Old School RuneScape bonds and EVE Online PLEX in the same form and compare their token premiums.
- Critique a token proposal for its effect on who pays, platform fees, pay-to-win perception and players who cannot or should not spend.

**Before class:** Fields, T. & Cotton, B., *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the sections on virtual currency and on converting non-payers into payers. Look up the current price of the WoW Token in your region's in-game shop and of a month of subscription, and write both down with the date.

**Prerequisites from earlier courses:** [MMO401 week 11, premium currencies and exchange rates](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w11-premium-currencies-and-exchange-rates.md). That lecture built the token triangle and the market price of a token in gold, `P = B / Q`. This week takes that price as given and studies the studio's dollars instead; do not re-derive the triangle. [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (why a sanctioned token competes with gold sellers). [GD101 week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) (the magic circle as a membrane, with the WoW Token as its example). From this course, [week 1, business models](w01-business-models-box-subscription-f2p-hybrid.md) (hybrids and whose experience pays for whose), [week 4, cosmetics vs power](w04-cosmetics-vs-power.md), [week 10, pricing experiments](w10-pricing-experiments.md) (break-even lines), [week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md) (LTV) and [week 3, premium currencies](w03-premium-currencies.md).

**Interactive:** [Token revenue map](../examples/w11-token-revenue.html). Keep it open during section 2.

---

## 1. What a subscription token is

A **subscription token** is an item a player buys from the studio with real money, which can be sold to other players for in-game currency, and which the final owner redeems for game time. MMO401 week 11 called it one corner of a three-currency triangle. Here you need only three facts about it.

- The studio sells the token for a fixed price `c` in dollars.
- The token is redeemed for game time worth one subscription period, which a player could otherwise buy for `s` dollars.
- Between purchase and redemption, the token usually changes hands once, from a player with more money than time to a player with more time than money, for gold.

The words used this week:

- **Cash subscriber.** A player who pays `s` directly.
- **Token player.** A player whose game time is paid with a token they bought for gold.
- **Token buyer.** The player who paid `c` in dollars and sold the token for gold. Often a cash subscriber too.
- **Token premium.** The ratio `c / s`, how much more the studio charges for a month of game time sold as a token than as a subscription.
- **Cannibalization** `k`. The share of token players who would have paid `s` in cash if the token did not exist.
- **Substitution** `σ` (sigma). The share of the dollars spent on tokens that token buyers would otherwise have spent in your own store, on other items.

## 2. Worked example: who pays for the player who pays with gold?

### The hook

In World of Warcraft, a month of game time costs US$15 as a subscription. The same month bought as a WoW Token costs US$20. Since patch 6.1.2 (April 2015 in the Americas) a player can buy that token in the shop, sell it on the auction house for gold, and the buyer redeems it for 30 days. Players who pay with gold say they play WoW for free.

They do not. Every month of game time redeemed from a token was paid for in dollars by someone, at US$20, a third more than the subscription. So a token must make the studio money, surely? Not necessarily. It depends on who the gold-payer would have been without it, and on where the token buyer's US$20 came from.

### The model

Let `T` be the number of game-time months paid with tokens each month. In a steady state, that is also the number of tokens bought for game time each month. Compare the studio's monthly revenue with the token and without it.

- With the token, the studio receives `c` for each of the `T` tokens.
- Without the token, a share `k` of the token players would have paid `s` in cash. The rest, `1 − k`, would have left or never subscribed.
- A share `σ` of the token dollars would have been spent in the studio's store anyway, so those dollars are not new.

```
ΔR = T × ( c × (1 − σ) − k × s )

break-even substitution   σ* = 1 − k × s / c
```

- `ΔR` is the change in monthly revenue from adding the token.
- `T` is token-paid months per month. MMO401 week 11 showed that the market sets it, through the token's gold price.
- `c` is the token's dollar price and `s` the subscription price for the same period.
- `k` is the share of token players who would have paid cash anyway, between 0 and 1.
- `σ` is the share of token dollars that displaced other spending in your store, between 0 and 1.

Read the model before you compute anything. If nobody's other spending is displaced (`σ = 0`), the gain is `T × (c − k × s)`. Since `k ≤ 1`, it is positive whenever `c ≥ s`. **A token priced at or above the subscription cannot lose game-time revenue on its own.** The worst case is that every token player would have paid cash anyway, and then each token month still earns `c − s`, US$5 in WoW's case. The only way a token loses money is through `σ`, when buyers pay for tokens with dollars they would otherwise have spent with you.

### Numbers you can check

Take WoW-like prices, `s = 15` and `c = 20`, and `T = 100,000` token months a month. These are invented round numbers for teaching, not Blizzard's figures.

```python
s, c = 15.00, 20.00        # subscription price and token price, US$ per 30 days
T = 100_000                # game-time months paid with tokens each month

def token_gain(k, sigma):
    """Monthly revenue change from adding the token.
    k: share of token-time players who would have paid cash without the token.
    sigma: share of token dollars that would otherwise have been spent in your store."""
    return T * (c * (1 - sigma) - k * s)

print("k \\ sigma     0.0         0.3         0.6")
for k in (0.0, 0.5, 1.0):
    print(f"{k:.1f}   " + "  ".join(f"{token_gain(k, sg):>10,.0f}" for sg in (0.0, 0.3, 0.6)))
for k in (0.0, 0.5, 1.0):
    print(f"break-even sigma at k = {k:.1f}: {1 - k * s / c:.2f}")
```

Output:

```
k \ sigma     0.0         0.3         0.6
0.0    2,000,000   1,400,000     800,000
0.5    1,250,000     650,000      50,000
1.0      500,000    -100,000    -700,000
break-even sigma at k = 0.0: 1.00
break-even sigma at k = 0.5: 0.62
break-even sigma at k = 1.0: 0.25
```

Check the middle cell by hand. `c × (1 − σ) = 20 × 0.7 = 14`. `k × s = 0.5 × 15 = 7.5`. The gain per token month is `14 − 7.5 = 6.5` dollars, and `100,000 × 6.5 = 650,000` a month.

Read the table from corner to corner.

- **Top left, `k = 0`, `σ = 0`.** Every token player is someone you would otherwise have lost, and every token dollar is new. The token earns the full US$20 per month for players who would have paid nothing. This is the case the token was built for.
- **Bottom left, `k = 1`, `σ = 0`.** Every token player would have paid cash anyway. You still gain US$5 per month each, because the token buyer paid US$20 for what the token player would have bought at US$15.
- **Bottom right, `k = 1`, `σ = 0.6`.** Token players would have paid anyway, and most token dollars came out of your cosmetics shop. Now the token loses US$700,000 a month. The damage is not in game time. It is in the store.
- **The break-even column.** At `k = 0.5`, the token pays as long as less than 62.5% of token dollars are substitutes. At `k = 1`, the limit falls to 25%. The more of your token players are cannibalized subscribers, the less substitution you can afford.

There is a second effect the table does not count. The `T × (1 − k)` token players who would otherwise have left are still in the world. They group, trade, fill raids and buy other things. With `k = 0.5` that is 50,000 players a month kept. Week 2's LTV model and MMO305's social capital both put a value on them. The token is also a retention tool.

### A visual you can move

Open the interactive. The left view is two stacked bars, revenue without and with the token, split into cash subscriptions, token sales, and a red "displaced store spending" slice drawn below the axis. The right view is a map of the `(k, σ)` square, colored by `ΔR`, with the break-even line `σ = 1 − k × s / c` drawn across it. Drag the token price toward the subscription price and watch the line swing down until, at `c = s`, the whole bottom edge (`k = 1`) becomes break-even at `σ = 0`. Then raise a platform fee (section 4) and watch the profitable region shrink.

### Cross-game recognition

Each of these is the same model. What differs is the token premium `c / s`, and what else the token can be redeemed for.

**World of Warcraft Token (retail, since patch 6.1.2; Americas launch 7 April 2015).** US$20 in the Americas. It redeems for 30 days of game time or, since patch 7.1.5 in February 2017, US$15 of Battle.net balance. The one-month subscription is US$15 and has been since 2004. Token premium `c / s = 20 / 15 = 1.33`, or `20 / 13 = 1.54` against the US$13-a-month 12-month plan. The Battle.net option adds a use. A token redeemed for balance earns the studio US$20 in cash against US$15 of store credit spent on its own digital goods. Since February 2017 the token has been redeemable for more than game time, so in this model some token dollars now land in the store on purpose.

**Old School RuneScape bonds (Jagex, introduced 30 March 2015; prices as of September 2026).** A bond costs US$9.99 and redeems for 14 days of membership. A one-month membership costs US$14.99. Per 30 days, a bond costs `9.99 × 30 / 14 = US$21.41`, a token premium of `21.41 / 14.99 = 1.43`. Twenty bonds buy 12 months for US$192.99 against US$131.88 for the 12-month plan, a premium of 1.46. Bonds also buy name changes and other services. A traded bond becomes untradeable, and making it tradeable again costs 10% of its Grand Exchange value in coins, which is MMO401's fee on the token edge. It does not change the dollars in this model.

**EVE Online PLEX (introduced November 2008, current form since 9 May 2017, prices as of September 2026).** In May 2017 CCP turned each old PLEX into 500 new ones, so anything that cost one PLEX, including 30 days of Omega (subscriber) time, now costs 500. The EVE University wiki lists 5,500 PLEX for 360 days and 450 PLEX for 30 days of training on an extra character. On the official EVE store in late September 2026, 500 PLEX list at US$25 and one month of Omega at US$20, a token premium of `25 / 20 = 1.25` at list prices. The EVE University wiki likewise advises that buying game time directly is almost always cheaper than buying PLEX for it. PLEX goes further than the others. It is also the store currency, so it buys New Eden Store items. The line between token dollars and store dollars, which is `σ` in the model, is blurred on purpose. When the same currency pays for game time and cosmetics, you cannot measure `σ` from the store's books alone. Since November 2016 EVE has also had a free Alpha tier, so a lapsed subscriber is not lost to the game, only to the Omega revenue line. That lowers the cost of `k`.

Three games, one formula. Each prices the token above the subscription (premiums of about 1.25 to 1.54 in dollars), and each adds uses beyond game time. Those extra uses raise demand for tokens, and they also raise `σ`.

### Eyes-open design judgment

- **Price the token above the subscription.** A premium protects game-time revenue against cannibalization with no further assumptions. A token priced below the subscription turns every cash subscriber who can afford gold into a revenue loss.
- **Watch `σ`, not only token sales.** Token revenue is visible on day one. Displaced store spending is not. Track store spending per token buyer before and after their first token, against a matched group (MMO308 week 7's segments), or you will book cannibalized cosmetics as token growth.
- **Every extra use is a trade.** Redeeming for store credit or store items raises token demand, which raises the token's gold price and `T`. It also raises `σ` by design. Decide whether you want the token to be a subscription device or a second store currency, and price it for that.
- **You cannot set `T`.** The gold market sets it. If cash-rich players do not want gold, few tokens sell, whatever you decide. MMO401 week 11 shows how store sales and faucet changes move the gold price and so `T`.
- **The retained players are the point.** A token that earns little on paper but keeps 50,000 players who would have lapsed may be worth more to a social game than its `ΔR` says.

## 3. Who is the customer now?

A token changes who pays for whom. Before it, each subscriber paid for their own access. After it, some players pay for other players' access, and the gold changes hands in the other direction. It is a cross-subsidy, the same shape as free-to-play, where payers fund the world for non-payers. Week 1 traced the pattern in hybrid models.

Three consequences follow.

**Your best customers now include people who never pay you.** A token player who plays 60 hours a month, runs a guild and farms the gold that token buyers want is producing value the studio sells. Their LTV in dollars is zero, and their value to the game is high. Revenue dashboards that sort players by spend will rank them at the bottom.

**The token buyer's motive matters.** A player buys a token to get gold. What they do with gold decides how the rest of the game feels. If gold buys cosmetics and convenience, token buyers are paying to skip effort. If gold buys the best gear from other players, as it can through WoW's auction house and EVE's market, token buyers are paying for power through a legal channel. Week 4 drew the line between cosmetics and power. A token puts a dollar price on everything gold can buy, so it moves that line for every item on your market at once.

**The black market shrinks, and the gold price becomes public.** Blizzard presented the WoW Token in 2015 as a secure and legitimate way to get gold, set against third-party gold sellers and the account theft that feeds them (MMO304 week 11). Some of the token dollars in `ΔR` are dollars that used to go to gold sellers. In the model, they have `σ = 0` for your store and are pure gain. They also remove a harm, compromised accounts, that no revenue figure captures. In exchange, the token's gold price turns every item into a dollar figure that players will quote, which MMO401 called the implied wage.

## 4. Tokens, platforms and players who should not be spending

Two practical issues decide whether the model's numbers survive contact with reality.

**Platform fees come off `c`, not `s`.** If a subscription is paid on your own website and the token is sold through a platform store that keeps 30%, the studio receives `0.7 × c` for each token, not `c`. With `c = 20`, that is US$14, less than the US$15 subscription. The token premium in net dollars has become a discount. Put `c = 14` into the model and the bottom row, `k = 1`, now loses US$1 per token month even with `σ = 0`. Note that US$14 is also exactly what the table's middle column gets from `20 × (1 − 0.3)`. A 30% platform fee does to the token what 30% substitution does. Week 12 builds the full platform fee model. The practical rule is to compare token and subscription revenue net of each one's channel costs.

**A token makes gold worth money, which makes gold-spending decisions money decisions.** Before the token, a player who spent all their gold on a cosmetic spent play time. After it, they spent the equivalent of dollars. That matters most for players who cannot see the conversion, and for minors. [MMO402 week 11](../../MMO402-emergent-society-governance-and-ethics/lectures/w11-minors-in-online-worlds.md) covers the specific duties toward minors, and [MMO402 week 10](../../MMO402-emergent-society-governance-and-ethics/lectures/w10-addiction-wellbeing-and-responsible-design.md) covers spending that harms the player. A token does not create these risks by itself, since players already spent time. It does give them a price. A responsible token design keeps gold-to-token purchases under the same spending limits and parental controls as cash purchases.

It is fair to put the other side too. For many players, a token turns time into access. A student with more hours than money can keep playing a subscription game, and a working adult can skip a grind they have no time for, through a channel the studio controls and taxes. Both players get something they want, and the trade happens between consenting players. The ethical question is less whether tokens are acceptable than what gold can buy once it has a dollar price.

## In-class activity (25 minutes)

In groups of three, you advise a subscription MMO at US$12 a month that plans a token. Telemetry says about 60,000 lapsed or at-risk players could afford a token in gold at the expected gold price, and a survey says about a third of them would keep paying cash if there were no token.

1. Propose a token price `c` and justify the premium in one sentence.
2. Set `T = 60,000` and `k = 1/3`. Compute `ΔR` at `σ = 0`, `0.2` and `0.4`, and the break-even `σ`.
3. The business team wants to sell the token only through a console store that keeps 30%. Recompute the break-even `σ` with net `c`. Would you still launch?
4. Name one item that gold should never be able to buy once the token exists, and why.
5. Propose one measurement that would estimate `σ` in the first three months after launch.

Expected output: a price with a one-line rationale, three `ΔR` values and two break-even `σ` values (for example, with `c = 16`: `ΔR` = 720,000, 528,000 and 336,000; break-even `σ = 0.75` direct and about 0.64 through the console store), one protected item, and one measurement plan.

## Common misconceptions

- **"Token players play for free."** Someone paid dollars for every token month, usually at a premium. The studio is paid either way. The question is how much more.
- **"A token can only add revenue."** It can lose revenue when token dollars displace other store spending (`σ`) or when platform fees push the net token price below the subscription.
- **"If most token players were already subscribers, the token failed."** With `c > s` and low `σ`, even full cannibalization earns `c − s` per month. It is a smaller win, not a loss.
- **"The token is an economy feature, so the business team need not care."** Its price in gold is the economy team's problem (MMO401). Its price in dollars, its platform and its effect on store spending are the business team's.

## Check yourself

1. A game sells a token for US$18 and a subscription for US$15. With `T = 40,000`, `k = 0.8` and `σ = 0.25`, what is `ΔR`? What is the break-even `σ`?
2. OSRS sells a bond for US$9.99 for 14 days of membership. What is the dollar price per 30 days, and what token premium does that give against the US$14.99 one-month membership?
3. A studio sells tokens only through a mobile store that keeps 30% and sells subscriptions on its website with a 3% payment cost. With `c = 20` and `s = 15`, what are the net prices, and what is the largest `k` for which the token still gains at `σ = 0`?
4. A designer proposes redeeming tokens for store credit as well as game time. Which of `T`, `k` and `σ` does this move, and in which direction?

<details>
<summary>Answers</summary>

1. `ΔR = 40,000 × (18 × 0.75 − 0.8 × 15) = 40,000 × (13.5 − 12) = 60,000` dollars a month. Break-even `σ = 1 − 0.8 × 15 / 18 = 1 − 0.667 = 0.333`.
2. `9.99 × 30 / 14 = 21.41` dollars per 30 days. Premium `21.41 / 14.99 = 1.43`.
3. Net token `0.7 × 20 = 14.00`. Net subscription `0.97 × 15 = 14.55`. With `σ = 0`, the gain per token month is `14 − k × 14.55`, positive for `k < 14 / 14.55 = 0.962`. If more than about 96% of token players would have paid cash anyway, the token loses money.
4. It raises demand for tokens from players who want store credit, so `T` rises. It also raises `σ`, because token dollars now buy store items by design. `k` does not change directly, since it describes token players who redeem for game time.

</details>

## Lab / assignment hook

[Lab 11, a token for a subscription MMO](../labs/lab11.md). You build the token revenue model and run it on a population of 50,000 players with different cash and time budgets. You find how `T`, `k` and `ΔR` move with the token's gold price, add substitution and a platform fee, and write a launch recommendation. It counts toward the models component (40%).

## Sources

- Blizzard Entertainment, "Introducing the WoW Token" (2 March 2015) and "WoW Token: New Details" (6 April 2015): 30 days of game time per token, US$20 in the Americas, Americas launch on 7 April 2015, and the stated aim of a secure, legitimate way to get gold. Blizzard, "Trade a WoW Token for Battle.net Balance" (6 February 2017): US$15 of balance per token.
- Warcraft Wiki, "WoW Token" (accessed September 2026). Enabled in patch 6.1.2, Americas on 7 April 2015; US$20 in the Americas; redeemable for 30 days of game time or, from patch 7.1.5 (Americas 6 February 2017), US$15 of Battle.net balance; cites Blizzard's announcement "Introducing the WoW Token" (2 March 2015).
- Warcraft Wiki, "Game time" (accessed September 2026). US$15 for one month since 2004; US$14, US$13 and US$13 a month on the 3-, 6- and 12-month plans.
- Old School RuneScape Wiki, "Old school bond" (accessed September 2026). Released 30 March 2015; US$9.99 per bond and US$192.99 for 20; 14 days of membership per bond and 12 months for 20; 10% conversion fee to make a bond tradeable again. "Membership" (accessed September 2026). US$14.99 for one month and US$131.88 for 12 months.
- CCP Games, "PLEX Changes On The Way!" (EVE Online dev blog, 16 March 2017): every existing PLEX converted to 500 new PLEX, and anything that cost 1 PLEX now costs 500; Aurum retired into PLEX. EVE Online news, "Changes to PLEX packages coming with May release" (28 April 2017): release on 9 May 2017.
- EVE Online store (store.eveonline.com, checked 29 September 2026): 500 PLEX list price US$25; one month of Omega US$20 a month. Store prices change with sales; the list prices are used here.
- EVE Online support, "ISK and PLEX" and "New Eden Store" (Fenris Creations, updated September 2026): PLEX bought with money or for ISK on the player market; PLEX is the New Eden Store currency.
- EVE University Wiki, "Accounts", section "PLEX" (accessed September 2026). 500 PLEX for 30 days of Omega, 5,500 PLEX for 360 days, 450 PLEX for 30 days of Multiple Character Training, use in the New Eden Store; the advice that buying game time directly is almost always cheaper than buying PLEX for it.
- Wikipedia, "Eve Online" (accessed September 2026). PLEX introduced in November 2008; converted in May 2017 so that one old PLEX became 500 new PLEX and Aurum was retired into PLEX; limited free-to-play (Alpha) version added 11 November 2016. Wikipedia, "CCP Games" (accessed September 2026) notes the developer now operates as Fenris Creations, announced 6 May 2026.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w11-token-revenue.html

**The one insight:** a token priced above the subscription cannot lose game-time revenue, whatever share of token players would have paid cash anyway. It loses money only when token dollars displace other store spending or a platform fee pushes the net token price below the subscription. The student should see the break-even line in the `(k, σ)` square and watch it move as prices and fees change.

**Layout.** Two panels side by side on desktop, stacked on mobile (bars first). Readout table below.

**Left panel: revenue without and with the token.** Two stacked bars for one month.
- "Without token": cash subscriptions `N × s + k × T × s`.
- "With token": cash subscriptions `N × s`, token sales `T × c_net` stacked on top, and "displaced store spending" `σ × T × c_net` drawn as a red segment hanging below the zero line.
- A label between the bars shows `ΔR` in dollars and as a percentage of revenue without the token.

**Right panel: the `(k, σ)` map.** x-axis `k` from 0 to 1, y-axis `σ` from 0 to 1. Fill each cell (at least 50 × 50) by `ΔR = T × (c_net × (1 − σ) − k × s_net)` with a diverging scale centered on 0, and draw contour labels at 0 and at ±25% of the maximum. Draw the break-even line `σ = 1 − k × s_net / c_net`, clipped to the square, and label it. The current `(k, σ)` is a draggable dot, linked to the sliders.

**Controls.**
- Subscription price `s`: US$5 to US$30, step 0.50, default 15.
- Token price `c`: US$5 to US$40, step 0.50, default 20.
- Token months per month `T`: 0 to 500,000, step 5,000, default 100,000.
- Cash subscribers who keep paying cash `N`: 0 to 5,000,000, step 50,000, default 1,000,000 (only scales the bars).
- `k`: 0 to 1, step 0.01, default 0.5.
- `σ`: 0 to 1, step 0.01, default 0.3.
- Platform fee on tokens `f_c`: 0% to 35%, step 1%, default 0%. Then `c_net = c × (1 − f_c)`.
- Channel cost on subscriptions `f_s`: 0% to 35%, step 1%, default 0%. Then `s_net = s × (1 − f_s)`.
- Preset buttons: "WoW-like" (`s` 15, `c` 20), "OSRS-like per 30 days" (`s` 14.99, `c` 21.41), "Token below subscription" (`s` 15, `c` 12).

**Readout table** (copyable). `c_net`, `s_net`, token premium `c_net / s_net`, `ΔR`, break-even `σ` at the current `k`, break-even `k` at the current `σ` (`c_net × (1 − σ) / s_net`, shown as "any k" when it exceeds 1), and retained players `T × (1 − k)`.

**Test values.**
- Defaults: `ΔR = 650,000`; break-even `σ = 0.625`; retained players 50,000.
- `k = 1`, `σ = 0`: `ΔR = 500,000`. `k = 1`, `σ = 0.6`: `ΔR = −700,000`.
- `k = 0`, `σ = 0`: `ΔR = 2,000,000`.
- Platform fee 30%, `k = 1`, `σ = 0`: `c_net = 14`, `ΔR = −100,000`.
- Preset "Token below subscription", `k = 1`, `σ = 0`: `ΔR = −300,000`.

**Accessibility.** Keyboard-operable sliders and dot (arrow keys move it by 0.01). The map's color scale has a text legend with numbers, and the break-even line has a text label. The displaced-spending segment is hatched as well as red. No animation under `prefers-reduced-motion`. Uses the shared palette tokens.
