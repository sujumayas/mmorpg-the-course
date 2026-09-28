# MMO401 · Week 09 — Regional Economies and Logistics

**Why this matters:** The moment your world has more than one market, distance becomes a price. The gap between what an item costs at the hub and what it costs at the frontier is set by rules you write about travel time, cargo space and danger. Get those rules right and hauling becomes a profession and places feel different. Get them wrong and either every region is the same or the frontier starves.

**You will be able to:**
- Compute the per-unit transport cost of a route from trip time, capacity, the hauler's wage, fees and loss risk.
- Derive regional prices, trade flow and the gains from trade for two linked markets, and show that the price gap equals the transport cost.
- Explain why trade concentrates in one hub and predict what happens to a second hub.
- Design a set of logistics rules that produces a chosen price gap between regions, and critique global markets that remove geography.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters 9-12 block, reading for market structure and space (about 25 pages). EVE University Wiki, "Hauling" and "Jita" (about 20 minutes together). Reread MMO304 week 10 on search costs and market scope.

**Prerequisites from earlier courses:** [MMO304 week 10, market design](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w10-market-design-auction-houses-vendors-barter.md) (search cost `c`, market scope, EVE's regional markets, WoW's 9.2.7 change). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) (reach, and EVE's hauling profession). [MMO304 week 6, supply and demand](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md) (linear markets and equilibrium). [MMO304 week 7, crafting chains](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w07-crafting-chains-and-gathering-professions.md) (where inputs come from). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (expected loss of a cargo). This course: [week 7, taxes and fees](w07-taxes-and-fees-as-policy.md) (a toll is a per-unit tax on a route), [week 5, order books and spreads](w05-market-microstructure-order-books-and-spreads.md) (depth and liquidity), and [week 6, manipulation](w06-manipulation-cornering-and-cartels.md) (regional corners that hauling undoes).

**Interactive:** [Two-region trade](../examples/w09-two-region-trade.html). Drag trip time, capacity, danger and tolls and watch the price gap track the transport cost.

---

## 1. One item, two prices

Economists have a rule called the **law of one price**: in a market where goods move freely, the same good sells for the same price everywhere. The rule sounds obvious. It is almost never true, and the ways it fails are what make geography interesting.

If a sword sells for 50 in one town and 70 in another, a player can buy in the first and sell in the second. That is **arbitrage**, profiting from a price difference between places. Arbitrage pushes the cheap price up (more buyers) and the expensive price down (more sellers). If moving the sword were free, arbitrage would continue until the two prices matched.

Moving goods is never free. It takes time, which has a wage. It takes cargo space, which is limited. And on the way, the goods can be lost. Call the total cost of moving one unit from the cheap place to the expensive place `τ` (tau), the **transport cost**. Arbitrage stops paying once the gap falls to `τ`. So the corrected rule is:

```
|P_B − P_A| ≤ τ
```

Prices in two connected places can differ by up to the transport cost and no more. Inside that band, nobody hauls. At the edge of the band, haulers are indifferent. The band is the whole story of regional prices, and `τ` is a number you control.

## 2. Worked example: the price gap is the cost of the trip

### The hook

EVE Online has no global market. Each region of space has its own market. A player can see every order in their region and buy remotely, but the item stays in the station where the seller listed it until someone hauls it away. The biggest hub is Jita, in The Forge region. The EVE University Wiki lists its market offers at around 687 trillion ISK, far ahead of every other hub, with over a thousand players in the system at once. The same ship or module is usually cheaper in Jita than out in the frontier, and there are player corporations, such as Red Frog Freight and Push X, whose business is moving cargo for a fee.

Everyone can see both prices. So why doesn't the gap close? And what sets its size? The model answers both.

### The model

Two regions trade one good. Region A is the hub, where the good is cheap to make. Region B is the frontier, where it is costly to make.

```
Region A:  demand Q = 100 − P      supply Q = P
Region B:  demand Q = 100 − P      supply Q = P − 40
```

On their own (economists say **autarky**), A clears at `P_A = 50` and B at `P_B = 70`. The gap is 20.

Now open a route. Haulers buy in A, carry to B and sell. Each unit carried costs `τ`. Let `F` be the flow, units per day moved from A to B. Region A must supply its own buyers plus the exports. Region B's buyers take local supply plus the imports.

```
A:  P_A − (100 − P_A) = F        so  F = 2 × P_A − 100
B:  (100 − P_B) − (P_B − 40) = F  so  F = 140 − 2 × P_B
arbitrage:  P_B = P_A + τ         (when F > 0)
```

Solve the three equations:

```
P_A = 60 − τ / 2
P_B = 60 + τ / 2
F   = 20 − τ              (and F = 0 once τ ≥ 20)
```

The price gap is exactly `τ`. The flow shrinks one unit for every gold of transport cost. When `τ` reaches the autarky gap of 20, trade stops and the regions go back to 50 and 70.

The **gains from trade** are the extra value created by moving goods from where they are cheap to make to where they are wanted, minus what the moving costs. For this pair of linear markets they come to

```
G = (20 − τ)² / 2
```

### Where τ comes from

A designer never sets `τ` directly. You set trip time, cargo size, danger and fees, and players turn those into a cost per unit.

```
τ = w × h / k + f + λ × P_A
```

- `w` is the hauler's wage, the gold per hour they could earn doing something else.
- `h` is the round-trip time in hours.
- `k` is the number of units one trip can carry.
- `f` is any per-unit fee or toll on the route.
- `λ` (lambda) is the chance the whole cargo is lost on a trip, so `λ × P_A` is the expected loss per unit bought in A.

Because the loss term depends on `P_A`, which depends on `τ`, solve once more. Substituting `P_A = 60 − τ/2`:

```
τ = (w × h / k + f + 60 × λ) / (1 + λ / 2)
```

### Numbers you can check

Take `w = 600` gold per hour and `k = 200` units per trip.

| Route | Trip `h` | Loss `λ` | Toll `f` | `τ` | `P_A` | `P_B` | Flow `F` | Gains `G` |
|---|---|---|---|---|---|---|---|---|
| No route | — | — | — | ≥ 20 | 50.00 | 70.00 | 0 | 0 |
| Safe highway | 0.5 h | 0 | 0 | 1.50 | 59.25 | 60.75 | 18.50 | 171.1 |
| Long road | 2 h | 0 | 0 | 6.00 | 57.00 | 63.00 | 14.00 | 98.0 |
| Short, dangerous | 0.5 h | 10% | 0 | 7.14 | 56.43 | 63.57 | 12.86 | 82.7 |
| Long and dangerous | 2 h | 10% | 0 | 11.43 | 54.29 | 65.71 | 8.57 | 36.7 |
| Safe highway with a toll | 0.5 h | 0 | 5 | 6.50 | 56.75 | 63.25 | 13.50 | 91.1 |
| Safe highway, 50-unit cargo | 0.5 h | 0 | 0 | 6.00 | 57.00 | 63.00 | 14.00 | 98.0 |

Check the dangerous row. Time cost is `600 × 0.5 / 200 = 1.5`. Then `τ = (1.5 + 60 × 0.1) / 1.05 = 7.5 / 1.05 = 7.14`. `P_A = 60 − 3.57 = 56.43` and `P_B = 63.57`. The expected loss per unit is `0.1 × 56.43 = 5.64`, and `1.5 + 5.64 = 7.14`. It closes.

Three things in the table deserve attention.

1. **Different rules can produce the same τ.** A long road and a small ship give identical prices. Players will feel them differently (hours of travel against more trips), but the market sees only `τ`.
2. **Danger is expensive.** A 10% loss chance adds more to `τ` than quadrupling trip time. Risk falls hardest on valuable cargo, because the loss term scales with price.
3. **Gains fall faster than flow.** Going from the highway to the long road cuts flow by a quarter and cuts gains from trade by more than 40%. That comes from the square in `G`. Each extra gold of `τ` costs more gains than the one before it, until trade stops.

### The visual

Open the interactive. The top view is a map with two towns and a road. Each town shows its price, and the road carries an arrow whose width is the flow. The bottom view plots `P_A`, `P_B` and flow against `τ` from 0 to 25, with a marker at the current route. Drag the danger slider. On the map, the prices drift apart and the arrow thins. On the chart, the marker slides right, and you can see that the gap between the two price lines is always the same as the marker's `τ`. Push `τ` past 20 and the arrow vanishes. The frontier is on its own.

### Cross-game recognition

Rewrite each game's logistics into `w`, `h`, `k`, `f` and `λ`.

**EVE Online (current).** Markets are regional and items stay at the station where they were listed. Within a region, buying is remote but collecting still needs a trip. Between regions, `τ` comes from travel time (`h`), cargo holds (`k`; the EVE University Wiki lists standard freighters at roughly 435,000 to 465,000 cubic metres), and the risk of being destroyed on the way (`λ`). Busy hubs like Jita have players waiting outside the station to attack haulers, and the wiki gives a rule of thumb for how much cargo value a ship can safely carry for its toughness. EVE's **compression** is a direct cut to the volume part of `τ`. Compressed asteroid ore takes 1% of the volume of raw ore (10% for ice and gas), so a hold carries 100 times more ore. That makes mining in remote regions pay, because the frontier's ore can reach the hub. Hauling corporations such as Red Frog Freight and Push X sell `τ` as a service. Their prices are a published estimate of `τ` for each route.

**World of Warcraft, patch 9.2.7 (16 August 2022).** Before this patch each realm had its own auction house, so the same herb could cost different amounts on different realms, and moving it meant moving characters. After it, commodities such as herbs, gems, flasks and consumables share one listing across every realm in a region. For commodities, `τ` between realms fell to zero, and the model says the price gaps should close entirely. Gear stayed realm-specific. WoW now runs two regimes side by side, with zero `τ` for inputs and a large `τ` for finished equipment.

**Guild Wars 2 (current).** The Trading Post is shared by every world in North America and Europe. `τ = 0` everywhere, so there are no regional prices and no hauling profession. What GW2 gives up in geography it gains in liquidity and simplicity. You can see this as the end point of WoW's direction of travel.

**Albion Online (since the 17 July 2017 launch).** Every item is crafted by players, and in the red and black zones anything a player carries drops on death, full loot. In model terms, any route through those zones has a large `λ`, set by other players. Carrying goods through safe zones and carrying them through full-loot zones are two different routes with two different `τ`, and players choose between them.

Four games, one band. Global markets set `τ = 0`. EVE sets a large `τ` and lets players compete to lower it. WoW picks per category. Albion lets players raise `λ` for each other.

### Eyes-open design judgment

- **Choose the gap you want, then build `τ` to match.** If you want frontier prices about 10% above the hub, you need `τ` of about 10% of the price. Work backwards to trip time, capacity and risk.
- **Too small a `τ` erases places.** Every region has the same prices, nobody hauls, and the world's geography stops mattering to the economy. That is a fine choice for a game focused on combat or story (Guild Wars 2), and a poor one for a sandbox.
- **Too large a `τ` starves the frontier.** Once `τ` passes the autarky gap, trade stops. Players in the frontier pay full autarky prices, and new players there have a worse game than players at the hub.
- **Risk-based `τ` is set by players, not by you.** Where `λ` comes from other players (EVE's gankers, Albion's full-loot zones), the gap moves with player behavior. Expect it to widen during wars and narrow in quiet periods. Your dashboards should track it.
- **Every fast-travel feature is a `τ` decision.** A teleport that can carry cargo sets `h` near zero. Many games let players teleport but not with a full cargo hold for exactly this reason.

## 3. Why one hub wins

Look again at Jita's numbers. Why does one hub hold most of the market when several stations could?

A market is more useful the more people use it. A seller in a busy hub finds a buyer in minutes. In a quiet one they wait hours, or have to cut the price. A new trader choosing between hubs will pick the busier one, which makes it busier still. This is a **positive feedback loop**, the kind you drew in GD102. Economists call the result **agglomeration**: activity clusters because clustering itself is valuable.

A small example. Two hubs start with 60% and 40% of traders. Each new trader joins the hub where they expect a faster sale, and expected sale time falls with the number of counterparties. Every newcomer joins the 60% hub. After 1,000 newcomers it holds 1,600 of 2,000 traders (80%), and the share keeps rising. Nothing needs to be wrong with the second hub. The EVE University Wiki describes Jita's rise in exactly these terms. A crossroads location drew early traders, and convenience drew the rest.

Agglomeration has design consequences.

- **The hub has its own `τ` advantage.** Goods flow toward the hub because that is where they sell fastest. Regional price gaps are measured from the hub outward.
- **Second hubs need a reason.** A secondary hub survives when it is far enough from the main one that `τ` to reach the main hub exceeds the cost of slower sales locally. That is a rule you can compute.
- **A dominant hub concentrates risk.** Jita attracts players who attack haulers at the station exit for the same reason it attracts traders. Everyone passes through.
- **Deliberate hub design is possible.** Put the best crafting stations, the main quest hub or the safest travel at one location, and you choose where agglomeration starts.

## 4. Regional price levels and where money enters

Week 4 treated money supply as one number. In a world with regions, where money enters matters too. If most gold enters the economy in a dangerous frontier region (bounties, rare drops), players there have more gold than goods, and local prices rise above the hub's by more than `τ` would predict until the money flows out. The flow out is the hub buying goods from frontier players, and goods flowing back the other way, both paying `τ`.

The practical point is for your dashboards. A price index per region, not only one global index, tells you whether a region is starving (prices above hub plus `τ`, flow not arriving) or flooded (prices below hub, money leaving). CCP's Monthly Economic Reports for EVE include regional trade and import data for this reason (MMO304 week 13).

## In-class activity (25 minutes)

Groups of three. You are designing a two-continent MMO. Your lead wants frontier prices for crafted gear to sit about 15% above the capital's, so that hauling pays but the frontier is playable.

1. Using the two-region model with the capital at `P_A ≈ 55`, what `τ` do you need?
2. Choose values for trip time, cargo capacity, loss chance and tolls that produce that `τ` with `w = 600`. Show the calculation.
3. The monetization team proposes a "caravan teleport" that carries full cargo for a premium item. Compute the new `τ` if it sets `h = 0` and `λ = 0` for users. What happens to the hauling profession and to the price gap?
4. Propose a restriction on the teleport that keeps `τ` near your target.

Expected output: a target `τ`, a route design with its calculation, the effect of the teleport, and one restriction.

## Common misconceptions

- **"Price differences between regions mean the market is broken."** They mean moving goods costs something. A gap up to `τ` is the market working.
- **"Faster travel always helps players."** It helps buyers in the frontier and hurts haulers, frontier producers and the sense that places differ. Decide who you are helping.
- **"Risk is just another cost."** It scales with the value of the cargo, so it hits expensive goods hardest, and in player-driven games it moves with player behavior.
- **"A second trade hub will spread the load."** Without a `τ` reason to exist, agglomeration pulls traders back to the first hub.

## Check yourself

1. A route has `h = 1` hour, `k = 100` units, `w = 600`, no toll and no risk. What are `τ`, `P_A`, `P_B`, `F` and `G` in the two-region model?
2. The same route gains a 5% loss chance. What is the new `τ`?
3. What `τ` makes the gains from trade exactly half of what they are with free transport?
4. A game's two regions have prices of 58 and 71 for the same good, and the transport cost is 6. What do you expect to happen, and what might be stopping it?
5. A designer doubles cargo capacity on every ship. Which routes' prices change most, the safe ones or the dangerous ones? Use the formula for `τ`.

<details>
<summary>Answers</summary>

1. `τ = 600 × 1 / 100 = 6`. `P_A = 57`, `P_B = 63`, `F = 14`, `G = 14² / 2 = 98`.
2. `τ = (6 + 60 × 0.05) / 1.025 = 9 / 1.025 ≈ 8.78`.
3. With free transport `G = 200`. Half is 100, so `(20 − τ)² = 200` and `τ = 20 − √200 ≈ 5.86`.
4. The gap of 13 exceeds `τ = 6`, so hauling should be very profitable and flow should rise until the gap falls to 6. If it doesn't, something is missing from `τ`: danger that has risen (a war), a capacity limit on haulers, or players not knowing the prices (a search cost, MMO304 week 10).
5. Capacity only divides the time term `w × h / k`. On safe routes that is all of `τ`, so doubling `k` halves `τ`. On dangerous routes most of `τ` is the loss term, which capacity doesn't touch, so prices barely move.

</details>

## Lab / assignment hook

[Lab 09, haulers between two regions](../labs/lab09.md). You will write the hauler agents for a two-region simulation, check that prices settle within the transport-cost band, then add a war that raises danger mid-run and design a logistics rule that holds the frontier's prices within a target. It counts toward the ABM labs (40%).

## Sources

- EVE University Wiki, "Trading" (current, checked September 2026). Each region has its own market; items remain at their station until hauled.
- EVE University Wiki, "Jita" (current). Located in The Forge, main station Jita IV - Moon 4 - Caldari Navy Assembly Plant; total market offers about 687 trillion ISK; over 1,000 players in system; rise to dominance through a self-reinforcing cycle starting from a gate crossroads.
- EVE University Wiki, "Hauling" (current). Trade hubs including Jita, Amarr, Dodixie and Rens; undock camping at busy hubs; freighter capacities of roughly 435,000 to 465,000 m³; a value-per-EHP rule of thumb; Red Frog Freight and Push X as hauling services.
- EVE University Wiki, "Compression" (current, after patch 20.03). Compressed asteroid ore, moon ore and Mercoxit at 1% of raw volume, ice and gas at 10%; purpose is to save cargo space when moving materials to hubs.
- Warcraft Wiki, "Auction House" (retail). Patch 9.2.7 (16 August 2022): commodities shared across all realms in a region, other items realm-specific.
- Guild Wars 2 Wiki, "Trading Post" (current). One market for all NA and EU worlds.
- Wikipedia, "Albion Online" (checked September 2026). Released 17 July 2017; fully player-driven economy with all equipment made by players; full loot on death in red and black zones.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Chapters 9-12.
- Two-market trade with transport costs and agglomeration follow standard trade and economic geography texts, for example Krugman, P. (1991), "Increasing Returns and Economic Geography", *Journal of Political Economy* 99(3).

## Interactive spec: examples/w09-two-region-trade.html

**The one insight:** the price gap between two linked regions always equals the transport cost, and the designer sets that cost through trip time, capacity, danger and tolls. Gains from trade fall with the square of the remaining gap, so small increases in `τ` near zero cost little and increases near the autarky gap cost a lot.

**Layout.** Two linked views, stacked on all screen sizes (map on top).

- Top view, "The route": two town markers labelled "Hub (A)" and "Frontier (B)" connected by a road. Each shows its price. An arrow from A to B has width proportional to `F` and is hidden when `F = 0`. Under the road print `τ` and its three parts as a small stacked bar: time cost `w × h / k`, toll `f`, expected loss `λ × P_A`.
- Bottom view, "Prices against transport cost": x-axis `τ` from 0 to 25. Lines for `P_A = 60 − τ/2` and `P_B = 60 + τ/2` up to `τ = 20`, then flat at 50 and 70. Flow `F = max(0, 20 − τ)` on a secondary axis, dashed. Shade the gap between the price lines lightly. Vertical marker at the current `τ`. A second small chart or inset plots `G = max(0, 20 − τ)² / 2`.

**Formulas.**

```
t0  = w × h / k + f
τ   = (t0 + 60 × λ) / (1 + λ / 2)
if τ ≥ 20: P_A = 50, P_B = 70, F = 0, G = 0
else:      P_A = 60 − τ/2, P_B = 60 + τ/2, F = 20 − τ, G = (20 − τ)² / 2
```

**Controls.**

- Trip time `h`: 0 to 5 hours, step 0.1, default 0.5.
- Capacity `k`: 10 to 500 units, default 200.
- Loss chance `λ`: 0% to 40%, step 0.5%, default 0.
- Toll `f`: 0 to 20 gold per unit, default 0.
- Wage `w`: 100 to 2,000 gold per hour, default 600.
- Presets matching the lecture table rows: "Safe highway", "Long road", "Short, dangerous", "Long and dangerous", "Highway with toll", "Small cargo", and "Global market" (`h` 0, `λ` 0, `f` 0).

**Readout table** (copyable): `t0`, `τ`, `P_A`, `P_B`, gap, `F`, `G`, expected loss per unit.

**Test values.**

- Safe highway: `τ` 1.50, `P_A` 59.25, `P_B` 60.75, `F` 18.50, `G` 171.13.
- Long road: `τ` 6.00, 57.00, 63.00, 14.00, 98.00.
- Short, dangerous: `τ` 7.14, 56.43, 63.57, 12.86, 82.65.
- Long and dangerous: `τ` 11.43, 54.29, 65.71, 8.57, 36.73.
- Highway with toll 5: `τ` 6.50, 56.75, 63.25, 13.50, 91.13.
- `h` 5, `k` 50, `λ` 0: `t0` = 60, `τ` capped, prices 50 and 70, `F` 0, arrow hidden.

**Accessibility.** Keyboard-operable sliders with visible focus; lines distinguished by style and direct labels; arrow width also printed as a number; `prefers-reduced-motion` disables the arrow animation. Towns drawn as simple generic shapes, no game art.
