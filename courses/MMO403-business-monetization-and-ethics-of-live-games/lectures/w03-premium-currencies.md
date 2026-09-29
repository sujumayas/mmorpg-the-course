# MMO403 · Week 03 — Premium Currencies

**Why this matters:** Most online games do not sell you an item for money. They sell you coins, and then sell you the item for coins. That extra step decides what the item really costs, how much currency you are left holding, and whether you come back to spend it. Regulators in Europe now treat the step as a consumer-protection question, so a designer who sets pack sizes and item prices without doing the arithmetic is making a legal decision by accident.

**You will be able to:**
- Compute the cash a player must spend to buy an item from a given pack grid, the leftover balance, and the markup over a reference price.
- Explain why leftovers form a sawtooth over item prices, and compute the expected leftover for a store.
- Compare flat-rate, bulk-bonus and no-currency stores (Guild Wars 2, Fortnite, Final Fantasy XIV) in one model.
- Critique a store against the EU Consumer Protection Cooperation Network's 2025 key principles on in-game virtual currencies, and design a pack grid that satisfies them.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapter on virtual currencies (the course reader lists the pages). Read the CPC Network's "Key Principles on In-game Virtual Currencies" (European Commission, 21 March 2025), all eight pages. It is short and is a primary source.

**Prerequisites from earlier courses:** [MMO401 week 11, premium currencies and exchange rates](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w11-premium-currencies-and-exchange-rates.md) (soft and premium currencies, exchange rates, the token triangle; this lecture covers the purchase side and does not repeat the exchange side). [MMO304 week 1, artificial scarcity](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w01-why-virtual-economies-exist-artificial-scarcity.md). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). From this course, [week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md) (ARPPU and the payer rate).

**Interactive:** [Currency packs](../examples/w03-currency-packs.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. What a premium currency is for

A **premium currency** (also "hard currency") is an in-game money that players buy with real money. Gems, crowns, V-Bucks and coins are examples. A **soft currency** is earned by playing. MMO401 week 11 covered what happens when the two can be exchanged. This week is about the moment a player turns real money into premium currency and then into an item.

Four terms you will use all lecture:

- A **pack** is a fixed amount of currency sold for a fixed price. A store's packs form its **pack grid**.
- A **bonus** is extra currency in larger packs, so the currency per dollar rises with pack size.
- The **balance** is the currency a player holds. The **leftover** is what remains after a purchase.
- **Breakage** is currency that is bought and never spent, because the player stops playing with a balance too small to use.

Studios have real reasons to use a premium currency, and you should know them before you criticize one.

- **One price list, many markets.** A game sold in dozens of countries and on several platforms can price each pack in local money and each item once, in currency. Changing an item's price then means changing one number.
- **Earned and bought money in one wallet.** Many games let players earn some premium currency by playing. A battle pass that pays out currency, or an exchange from gold to gems, only works if items are priced in currency.
- **Fewer small payments.** Each card or platform payment has its own processing overhead. Selling one $20 pack is cheaper to process than twenty $1 items.
- **Bulk pricing.** Bonuses are a quantity discount, which many players value.

The same step has costs, and they fall on the player. The price of an item is written in a unit the player does not think in. And unless every item price matches some combination of packs, the player must buy more currency than the item needs. The worked example measures both.

## 2. Worked example: the 1,200-coin item that costs $19.98

### The hook

Two games, two ways to sell a premium currency, as listed in September 2026.

Guild Wars 2 sells gems in six packs from 400 gems for $5 to 8,000 gems for $100. Every pack is exactly 80 gems per dollar. There is no bulk discount.

Fortnite, after a price change on 19 March 2026, sells V-Bucks in four packs: 800 for $8.99, 2,400 for $22.99, 4,500 for $36.99 and 12,500 for $89.99. The rate climbs from 89 V-Bucks per dollar to 139, so the largest pack gives 56% more currency per dollar than the smallest. Before that change, the same four prices bought 1,000, 2,800, 5,000 and 13,500 V-Bucks.

Neither game lets you pay money for most items directly. So what does an item cost? On 21 March 2025, the EU's Consumer Protection Cooperation (CPC) Network, the body of national consumer authorities coordinated by the European Commission, published key principles saying every item's price in real money should be clearly shown, and listing "bundles mismatching the value of purchasable in-game digital content" as a practice to avoid. Both statements assume you can compute the real price. Here is how.

### The model

A store has packs `(q_i, p_i)`: pack `i` gives `q_i` currency for `p_i` dollars. A player holding balance `b` wants an item priced `c` in currency.

```
cash    C(c, b) = min over whole numbers n_i ≥ 0 of  Σ n_i × p_i
                  subject to  b + Σ n_i × q_i ≥ c
leftover L      = b + Σ n_i × q_i − c
reference price = c × p_1 / q_1           (the smallest pack's rate)
markup          = C / reference price
```

- `n_i` is how many of pack `i` the player buys in this checkout.
- `C` is the cheapest cash outlay that covers the item. A real player may spend more by picking a single big pack. `C` is the best case.
- The **reference price** values currency at the smallest pack's rate. That is one reading of the CPC's first principle, which says the real-money price should be based on what the consumer would pay in full, without applying quantity discounts. Other readings are possible, and week 7 returns to the legal detail.
- A markup above 1 means the player pays more cash at checkout than the item's reference price, and walks away with a balance.

Finding `C` is a small integer problem, the "cover" version of the coin-change problem. Lab 03 solves it with dynamic programming. For a four-pack store, trying every combination up to a sensible bound is fast enough.

### Numbers you can check

Take an invented store, Emberfall Online, with four packs and five item prices:

| Pack | Coins | Price | Coins per dollar |
|---|---|---|---|
| Small | 1,000 | $9.99 | 100.1 |
| Medium | 2,800 | $24.99 | 112.0 |
| Large | 5,000 | $39.99 | 125.0 |
| Huge | 13,500 | $99.99 | 135.0 |

Now price each item from a zero balance:

| Item price | Cheapest purchase | Cash `C` | Leftover | Reference price | Markup |
|---|---|---|---|---|---|
| 800 | 1 small | $9.99 | 200 | $7.99 | 1.25 |
| 1,200 | 2 small | $19.98 | 800 | $11.99 | 1.67 |
| 1,500 | 2 small | $19.98 | 500 | $14.99 | 1.33 |
| 2,000 | 2 small | $19.98 | 0 | $19.98 | 1.00 |
| 2,800 | 1 medium | $24.99 | 0 | $27.97 | 0.89 |

Check the 1,200 row. One small pack gives 1,000, which is not enough. Two small packs give 2,000 for $19.98. One medium pack gives 2,800 for $24.99, which covers it but costs more. So `C = $19.98`, leftover `2,000 − 1,200 = 800`, and reference `1,200 × 9.99 / 1,000 = $11.99`.

The item the store lists at "1,200 coins" takes $19.98 out of a new player's account. The 2,800-coin item, which looks more than twice as expensive, costs only about $5 more and leaves nothing behind. Item prices in coins and cash prices at checkout do not even rank the same way.

This code reproduces the table. It runs as shown with `.venv/bin/python`:

```python
from itertools import product

PACKS = [(1_000, 999), (2_800, 2_499), (5_000, 3_999), (13_500, 9_999)]  # coins, cents

def cheapest_cover(c, packs=PACKS, balance=0):
    """Cheapest (cents, leftover) that brings the balance to at least c coins."""
    need = max(0, c - balance)
    ranges = [range(need // q + 2) for q, _ in packs]
    best = None
    for counts in product(*ranges):
        coins = sum(n * q for n, (q, _) in zip(counts, packs))
        cents = sum(n * p for n, (_, p) in zip(counts, packs))
        if coins >= need and (best is None or (cents, -coins) < best):
            best = (cents, -coins)
    cents, neg_coins = best
    return cents, balance - neg_coins - c

for c in (800, 1_200, 1_500, 2_000, 2_800):
    cents, left = cheapest_cover(c)
    ref = (2 * c * 999 + 1_000) // 2_000          # cents, rounded half up
    print(f"{c:5d} coins: pay ${cents / 100:.2f}, leftover {left:4d}, "
          f"reference ${ref / 100:.2f}, markup {cents / ref:.2f}")
```

It prints `1200 coins: pay $19.98, leftover  800, reference $11.99, markup 1.67` and `2800 coins: pay $24.99, leftover    0, reference $27.97, markup 0.89`, matching the table. Prices are integer cents so that ties compare exactly, and the reference price rounds half up (Python's `round` would turn $14.985 into $14.98).

### The visual

Open `examples/w03-currency-packs.html`. The left view is what the store shows. Items appear as tags with coin prices, sorted from cheapest to dearest, a staircase that rises smoothly. The right view is what the player pays. For every item price from 100 to 3,000 coins, it plots the cash at checkout (a staircase with big flat steps) and the leftover (a **sawtooth** that falls from 900 to 0 and jumps back up at every pack boundary).

Drag an item along the coin axis. At 1,000 coins the leftover is 0. At 1,100 it jumps to 900. The cash line jumps by a full pack while the coin price moved by 100. Now switch the pack grid to "flat 80 per dollar" (the Guild Wars 2 shape). The sawtooth remains, because packs still come in steps. Switch to "no currency" (the Final Fantasy XIV shape). The sawtooth vanishes and the two views become one line. The picture to take away is that leftovers come from the step size of the smallest pack relative to item prices. The discount curve decides how much cheaper big packs are, which is a separate question.

### Cross-game recognition

**Guild Wars 2 (gem store, current).** A flat rate of 80 gems per dollar in packs of 400, 800, 1,600, 2,800, 4,000 and 8,000. The reference price and the per-gem price are the same for every pack, so the markup at checkout comes only from step size. The smallest step is 400 gems ($5), so the leftover for any item is below 400 gems. GW2 also lets players buy gems with gold through its currency exchange, which MMO401 week 11 analyzed. That route means a leftover can be topped up without spending money, which changes its pull.

**Fortnite (V-Bucks, from 19 March 2026).** A bulk-bonus grid with a smallest step of 800 V-Bucks for $8.99. The Battle Pass costs 800 V-Bucks, exactly one small pack, and a player who completes it earns 800 V-Bucks back. Rewrite that in our model. The flagship product sits exactly on a pack boundary (leftover 0), and the pass is a faucet that refills the balance by the price of the next pass. For an item priced at a round number that is not a multiple of 800, the sawtooth applies. A hypothetical 1,200 V-Buck item costs $17.98 from a zero balance, as two small packs, and leaves 400.

**Final Fantasy XIV (online store, current).** No premium currency for optional items. They are priced directly in real money. In our model the pack grid is continuous, `C` equals the item price, and the leftover is always 0. The cost is the flexibility of section 1. There is no single price list in currency, no bulk bonus, and no way to earn store credit in play.

**Stored-value money outside games.** Raghubir and Srivastava (2008) ran experiments in which people spent more when paying with scrip, a stored-value certificate, than with cash of the same face value. The effect shrank when the act of parting with money was made more salient. This is lab evidence about payment forms in general, not a study of game currencies, and you should cite it as such. It is the research behind the CPC principle that currency "psychologically disconnects" spending from money.

Four stores, one model. Every store sits somewhere between "items in money, no leftovers" and "items in currency, big steps, big bonuses", and the model tells you what each position costs the player at checkout.

### Eyes-open design judgment

- **Price items on pack boundaries, or make the smallest step small.** If your cheapest pack is 1,000 coins, price items at multiples of 1,000, or add a 100-coin pack. Either removes the sawtooth. Both reduce revenue from leftovers, and you should decide knowingly whether you are willing to give that up.
- **Put the real price next to the coin price.** A second line under "1,200 coins" that says "≈ $11.99" costs one label. The CPC principles ask for exactly this. Your store will convert less on impulse purchases and generate fewer complaints and refunds, and you should model both effects.
- **Bonuses are a real discount.** A bulk bonus lowers the price per coin for players who were going to spend that much anyway. It also pushes players who want one item toward a larger pack. Show both effects in your store analysis.
- **Earnable currency changes the ethics.** A leftover that the player can top up by playing is less of a pull than one that only money can complete. Guild Wars 2's gold exchange and Fortnite's pass payouts both soften the sawtooth.
- **Watch for several currencies.** A store where one currency buys another, which buys the item, stacks the translation steps. The CPC principles list this as a practice to avoid.

## 3. Leftovers pull, and some are never spent

A leftover is not lost money in a single purchase. It is prepayment for the next one. The player who bought the 1,200-coin item for $19.98 holds 800 coins. If the next item they want costs 800, it is "free":

| Purchases in order | Cash spent | Final balance |
|---|---|---|
| 1,200 then 800 | $19.98 | 0 |
| 1,500 then 800 | $29.97 | 700 |
| 1,500, 800, 800 | $39.96 | 900 |

The second row shows the pull. After the 1,500 item, the player holds 500. That does not buy the 800 item, so they buy another small pack and end with 700. The third row keeps going and ends with 900. Across a sequence of purchases the average price per coin approaches the pack rate, and the leftover is carried forward. What remains at the end, when the player quits, is breakage.

How big is a typical leftover? If item prices in the store are spread evenly over the multiples of 100 from 100 to 2,000, and a player starting from zero buys the cheapest cover, the leftover takes each value 0, 100, ..., 900 exactly twice. By MA102 week 4, the expected leftover is the average, 450 coins, about $4.50 at the small pack's rate. Across those 20 prices the average markup at checkout is 2.13, driven by the cheap items where a $9.99 pack buys a 100-coin item.

Leftovers matter for three reasons, and a balanced analysis names all three.

1. **They move cash forward.** A player pays for currency before they spend it. For the studio, this is cash in hand earlier. For the player, it is money committed to one game's store.
2. **They create a pull.** A balance that almost buys something is a reason to return and top up. That pull can be a service (the player planned to buy more anyway) or a pressure (the player would not otherwise have spent). Which one it is depends on who the player is, and the CPC principles single out children and heavy spenders.
3. **Breakage is revenue for nothing.** Currency bought and never spent was paid for and never delivered anything. A store whose revenue depends on breakage has a reason to keep leftovers large. That is the design incentive the CPC principles' third principle targets.

## 4. The 2025 EU key principles, and where they bind

The CPC Network's key principles, published 21 March 2025, are the most specific official statement so far on premium currencies. Read them yourself. In summary:

| Principle | What it asks |
|---|---|
| 1 | Show the real-money price of currency and of every item bought with currency, based on what the consumer would pay in full, without quantity discounts |
| 2 | Avoid practices that obscure cost, such as mixing several currencies or requiring several exchanges before a purchase |
| 3 | Avoid forcing players to buy currency they don't need, such as bundles mismatching item prices or not letting players choose the amount |
| 4 | Give clear pre-contractual information, including the real-money price |
| 5 | Respect the 14-day right of withdrawal for unused currency, with the rules for express consent on digital content |
| 6 | Use fair, plain contract terms; do not reserve the right to change the currency's value unilaterally |
| 7 | Respect vulnerable consumers, especially children; use parental controls with spending disabled by default where the game is not adult-only; avoid business models built on players willing to spend excessive amounts |

Three things to keep in mind about their force. First, the document itself says it is non-exhaustive and does not bind national authorities or the Commission, and that only authorities and courts decide what is lawful. It sets out how the enforcers read existing EU law (the Unfair Commercial Practices Directive, the Consumer Rights Directive and the Unfair Contract Terms Directive), which do bind. Second, the same page on the Commission's site records a coordinated action against one game, Star Stable Online, including a finding of unclear information about buying and using in-game currency. That shows the principles being applied. Third, the principles cover currencies bought with money. Currency that can only be earned in play is excluded.

For a designer, the practical test is short. Can a player see what an item costs in money? Can they buy what they need without being forced to buy more? Would a child understand the store? Week 7 places these principles next to loot-box law in Belgium, the Netherlands and elsewhere.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive, a laptop, and the Emberfall store from section 2.

1. (8 min) Redesign Emberfall's pack grid so that every item in the section 2 table has a markup of at most 1.10 from a zero balance, keeping at least one bulk bonus. Record your grid.
2. (7 min) Compute the expected leftover for item prices 100 to 2,000 in steps of 100 under your grid, using the interactive's "store audit" panel.
3. (5 min) Estimate what your change does to revenue from a player who buys exactly one 1,200-coin item and then quits. Then estimate it for a player who buys ten items over a year.
4. (5 min) Check your store against principles 1 to 3 of the CPC key principles. Write one sentence for each.

Expected output: the new pack grid, a markup table, the expected leftover, the two revenue estimates and three one-sentence checks.

## Common misconceptions

- **"The bigger pack is always the better deal."** Per coin, yes, when the store has bonuses. Per item, not necessarily. Emberfall's 1,200-coin item is cheapest as two small packs, not one medium pack.
- **"A flat rate means no leftovers."** Leftovers come from the step size of the smallest pack. Guild Wars 2's flat rate still leaves up to 399 gems unless items sit on multiples of 400.
- **"Leftover currency is wasted money."** It is prepaid money. It becomes waste (breakage) only if the player never spends it, which is why its ethical weight depends on how likely that is.
- **"Premium currencies exist only to hide prices."** They also unify pricing across markets, let players earn store credit, and allow bulk pricing. The design question is whether the store shows the real price anyway.

## Check yourself

1. In the Emberfall store, a player holds 300 coins and wants a 1,500-coin item. What is the cheapest cash outlay, and what is their leftover?
2. A store sells 500 coins for $4.99 and 1,100 for $9.99. Items cost 600 coins. What is the cheapest way to buy one item from zero, the leftover, and the markup at the smallest pack's rate?
3. With Fortnite's current pack grid, what is the cheapest way to buy exactly one Battle Pass from zero, and what does a player who completes it hold afterwards (assume they spend nothing else)?
4. A designer argues that adding a 100-coin pack for $1.29 to Emberfall is "better for players". Compute the new cash and leftover for the 1,200 item, and give one reason the claim is too simple.

<details>
<summary>Answers</summary>

1. The player needs 1,200 more. Two small packs ($19.98) give 2,000, leftover `300 + 2,000 − 1,500 = 800`. One medium pack ($24.99) costs more. So $19.98, leftover 800.
2. Options: two 500 packs ($9.98, 1,000 coins, leftover 400) or one 1,100 pack ($9.99, leftover 500). The cheapest is two 500 packs at $9.98. Reference `600 × 4.99 / 500 = $5.99`, markup `9.98 / 5.99 ≈ 1.67`.
3. One 800 pack for $8.99 buys the 800 V-Buck pass with 0 left. Completing the pass returns 800 V-Bucks, so the player holds 800, the price of the next pass.
4. With the 100-coin pack, 1,200 coins can be bought as one small plus two 100-coin packs for `9.99 + 2 × 1.29 = $12.57`, leftover 0. That beats $19.98. But $1.29 per 100 is worse per coin than the small pack, so the store now charges a premium on small top-ups, and players who top up often pay more per coin than before. "Better" depends on which players you count.

</details>

## Lab / assignment hook

[Lab 03, premium currency store audit](../labs/lab03.md). You implement the cheapest-cover solver with dynamic programming, audit the Emberfall store and a flat-rate store, and then audit one real game's store from its public pack grid and item prices. The written part checks the store against CPC principles 1 to 3 and proposes a redesign with its revenue cost. It is the first input to the ethics analysis (20%).

## Sources

- Consumer Protection Cooperation Network, "Key Principles on In-game Virtual Currencies" (European Commission, published 21 March 2025, Ref. Ares(2025)2303808). Principles 1 to 7 as summarized in section 4; the price-indication rule without quantity discounts; practices to avoid including bundles mismatching item values and several exchanges between currencies; the statement that currencies "psychologically disconnect" spending from money; exclusion of currencies obtainable only through gameplay; the non-binding status in footnote 1.
- European Commission, "Social media, online games and search engines" (commission.europa.eu, coordinated actions, accessed September 2026). The coordinated action on Star Stable Online and its common position dated 21 March 2025, including unclear information about buying and using in-game virtual currency; the key principles led by the Netherlands Authority for Consumers and Markets and the Norwegian Consumer Authority.
- Guild Wars 2 Wiki, "Gem" (accessed September 2026). Gem packs of 400, 800, 1,600, 2,800, 4,000 and 8,000 at $5 to $100; no bulk discount; 80 gems per dollar; gem cards from retailers. Guild Wars 2 Wiki, "Currency Exchange", via MMO401 week 11.
- Fortnite Wiki, "V-Bucks" (fortnite.fandom.com, accessed September 2026). Current packs of 800 for $8.99, 2,400 for $22.99, 4,500 for $36.99 and 12,500 for $89.99; the price change of 19 March 2026 citing Epic's announcement; earlier packs of 1,000, 2,800, 5,000 and 13,500 at the same prices; Battle Pass price of 800 V-Bucks and an 800 V-Buck payout on completion.
- Epic Games, "Fortnite V-Bucks price increase" (fortnite.com news, March 2026, read via the Internet Archive copy of 10 March 2026). From 19 March 2026 the $8.99, $22.99, $36.99 and $89.99 packs give 800, 2,400, 4,500 and 12,500 V-Bucks instead of 1,000, 2,800, 5,000 and 13,500; the Battle Pass costs 800 V-Bucks and awards 800 on completion, down from 1,000 plus 500 in bonus rewards.
- Square Enix, "FINAL FANTASY XIV Online Store" (store.finalfantasyxiv.com, accessed September 2026). Optional items priced in real money; optional items cannot be sold or traded.
- Raghubir, P. & Srivastava, J. (2008). "Monopoly money: The effect of payment coupling and form on spending behavior." *Journal of Experimental Psychology: Applied*, 14(3), 213-225. doi:10.1037/1076-898X.14.3.213.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w03-currency-packs.html

**Purpose.** Show that the cash a player pays for a currency-priced item depends on the pack grid, not on the item's coin price, and that leftovers form a sawtooth set by the smallest step. Insight on first load: *the store view shows 1,200 coins as a modest price between 800 and 2,800, while the checkout view shows it costing $19.98 with 800 coins left over, the same cash as a 2,000-coin item.*

**Layout.** Two linked views side by side on desktop, stacked on mobile (store first). Below them, the pack grid editor, then a store audit table. Generic tags and bars only; no game art or logos.

**Left view, the store.** Up to eight item tags on a horizontal coin axis (0 to 3,000), each showing its coin price. Default items: 800, 1,200, 1,500, 2,000, 2,800. When "show real price" is on, each tag gets a second line with the reference price `c × p_1 / q_1` in dollars. Items are draggable along the axis in steps of 100, and focusable with arrow keys (±100).

**Right view, the checkout.** x: item price in coins, 100 to 3,000 in steps of 100. Two series, sharing x:
- Cash `C(c, b)` in dollars as a step line (left y-axis), with the reference price line `c × p_1 / q_1` dashed for comparison.
- Leftover `L(c, b)` in coins as bars (right y-axis).
Highlight the x positions of the current items. `C` is the cheapest cover: minimize total cents over whole-number pack counts with `b + Σ n_i q_i ≥ c`, breaking ties by the larger coin total. Compute with a dynamic program over coins from 0 to `c − b + max q_i`.

**Controls.**
- Pack grid presets: "Emberfall (bulk bonus)" = (1,000, $9.99), (2,800, $24.99), (5,000, $39.99), (13,500, $99.99); "Flat 80 per dollar" = (400, $5), (800, $10), (1,600, $20), (2,800, $35), (4,000, $50), (8,000, $100); "Bulk bonus, small step" = Emberfall plus (100, $1.29); "No currency" = items priced directly at their reference price, leftover always 0; the reference rate stays the Emberfall small pack ($9.99 per 1,000 coins), so an 800-coin item costs $7.99 and a 1,200-coin item $11.99.
- Editable grid: up to six packs, coins (integer) and price (dollars, two decimals).
- Starting balance `b`: 0 to 2,000, step 50, default 0.
- Toggle "show real price" (default off, so the first screen shows the store as players see it; the right view already shows the truth).

**Store audit table.** For each item: coin price, cheapest purchase (pack counts), cash, leftover, reference price, markup. Footer: mean leftover and mean markup over all item prices 100 to 2,000 in steps of 100.

**Test values.**
- Emberfall, `b = 0`: 800 → $9.99, leftover 200, reference $7.99, markup 1.25; 1,200 → $19.98 (2 small), 800, $11.99, 1.67; 1,500 → $19.98, 500, $14.99, 1.33; 2,000 → $19.98, 0, $19.98, 1.00; 2,800 → $24.99 (1 medium), 0, $27.97, 0.89; 5,000 → $39.99 (1 large), 0.
- Emberfall, `b = 300`, item 1,500 → $19.98, leftover 800.
- Emberfall audit footer (100 to 2,000): mean leftover 450, mean markup 2.13.
- Emberfall leftover sawtooth: 100 → 900, 1,000 → 0, 1,100 → 900, 2,000 → 0, 2,100 → 700, 2,800 → 0, 2,900 → 100, 3,000 → 0.
- Flat 80 per dollar: 700 → $10.00, leftover 100; 800 → $10.00, leftover 0, markup 1.00.
- Bulk bonus, small step: 1,200 → $12.57 (1 small + 2 × 100), leftover 0. The reference price now uses the 100-coin pack's rate ($1.29 per 100), so 1,200 has reference $15.48 and markup 0.81.
- Sequence check (shown in a small "next purchase" box when the user clicks two items in turn): 1,500 then 800 → total $29.97, final balance 700.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Cash and leftover series differ by shape (line versus bars) and color. All tags and controls reachable by keyboard; the audit table is a real HTML table. Respect reduced motion.
