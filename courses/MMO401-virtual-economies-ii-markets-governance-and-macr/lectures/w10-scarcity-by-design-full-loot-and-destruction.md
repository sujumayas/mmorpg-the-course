# MMO401 · Week 10 — Scarcity by Design: Full Loot and Destruction

**Why this matters:** When a fleet dies, players and journalists count what was "destroyed". That number mixes three different things: items that left the world, items that moved to the winners, and money the game paid out for the loss. Your loss rules decide how much of each happens, and that split sets item prices, the size of your crafting industry and even your currency supply. If you only feel the loss, you cannot tune it.

**You will be able to:**
- Split any loss event into destroyed value, transferred value and currency created, using the recovery fraction `r` and the insurance payout.
- Derive the effective destruction rate `δ = h × (1 − r)` and use it to compute the steady-state stock, price and daily crafting revenue of an item class.
- Rewrite the loss rules of EVE Online, Ultima Online, Old School RuneScape and World of Warcraft in the same `(h, r, insurance)` form and predict what each does to the market.
- Critique a proposed loss rule by separating what the victim feels from what the economy sees.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the course's assigned chapters 9-12, reading for how item destruction and scarcity are treated. Reread MMO304 week 8 (destruction as a sink) and week 3 (faucets, sinks and transfers). Skim one recent EVE Online *Monthly Economic Report* and find the production and destruction chart.

**Prerequisites from earlier courses:** [MMO304 week 8, item decay, durability and destruction as sinks](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w08-item-decay-durability-and-destruction-as-sinks.md) (the steady-state stock `S* = F / d`, mean lifetime `1 / d`). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucet, sink, transformation, transfer). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md). [MMO304 week 1, artificial scarcity](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w01-why-virtual-economies-exist-artificial-scarcity.md). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (the `(1 − δ)^t` approach to a steady state). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). This course: [week 7, taxes and fees as policy](w07-taxes-and-fees-as-policy.md), [week 13, reading an economic report](w13-reading-an-economic-report.md), and the agent-based models of [weeks 2](w02-agent-based-modeling-i.md) and [3](w03-agent-based-modeling-ii.md), which Lab 10 extends.

**Interactive:** [Loss ledger](../examples/w10-loss-ledger.html). Two linked ledgers for items and currency under loss rules `(h, r, insurance)`.

---

## 1. Three fates for a lost item

In MMO304 week 8 you modelled an item stock with one number, the daily destruction rate `d`. That was enough for durability systems, where an item either survives or is gone. Loss in PvP games is messier. When a character dies in a full-loot zone, each item it carried meets one of three fates:

- **Destroyed.** The item leaves the world. This is an item sink.
- **Transferred.** The item moves to the killer, or to whoever reaches the body first. The world holds exactly as many items as before. This is a transfer.
- **Returned.** The owner gets it back: kept on death, recovered from a grave, or protected by a rule. For the economy this is as if nothing happened.

Some definitions for the rest of the lecture:

- **Full loot** means everything the victim carried can be taken by other players. **Partial loot** means some share can be taken and the rest is destroyed or kept. **No loot** means the victim keeps their items.
- The **loss hazard** `h` is the chance per day that a given copy of an item is on a character who dies with it at risk. If a typical ship is lost once every 50 days in service, `h = 0.02`.
- The **recovery fraction** `r` is the share of a lost item's copies that stay in the world after the loss, whether the killer takes them or the owner gets them back. `1 − r` is the share destroyed.
- The **effective destruction rate** is `δ = h × (1 − r)`. It plays the role of `d` from MMO304 week 8.
- **Insurance** is a rule that pays the victim currency when an item is lost. If the currency comes from an NPC, the payout is a **faucet**.

The key move is to keep two ledgers. One counts items. The other counts currency. A loss can shrink the first and grow the second at the same moment, and players only ever see the first.

## 2. Worked example: "11 trillion ISK destroyed", so where did it go?

### The hook

On 27 and 28 January 2014, two coalitions in EVE Online fought for 21 hours in the system B-R5RB. The fight started because a corporation missed a scheduled sovereignty payment, which left its space open to attack. More than 7,500 characters took part and 75 titans, the game's largest ships, were destroyed. The value lost was reported as about 11 trillion ISK, roughly 300,000 to 330,000 US dollars at the time.

Here is the puzzle. Right after the battle, how much ISK had left the EVE economy? Close to none. The ISK that paid for those titans had changed hands months earlier, when the ships were bought. The battle removed ships, not money. And because EVE insures hulls, the battle *added* ISK to the economy through insurance payouts. A battle that headlines called the most destructive in gaming history may have been a small net ISK faucet.

That is not a paradox once you keep two ledgers.

### The model

Take one item class, for example one type of combat ship, with a stock of `S` copies.

**Item ledger.** New copies are built at `F` per day. Each day a share `h` of copies is lost, and of those a share `r` stays in the world. So:

```
S(next day) = S + F − h × (1 − r) × S
            = S + F − δ × S          with δ = h × (1 − r)
```

This is MMO304 week 8's model with `d` replaced by `δ`. The steady state is `S* = F / δ`, reached along `S(t) = S* × (1 − (1 − δ)^t)`, and the mean lifetime of a copy in the world is `1 / δ` days.

**Price.** Give the item a simple market. Suppose players as a group are willing to hold `A` ISK in this item class, whatever the number of copies. The price is then:

```
p = A / S
```

This is a demand curve with elasticity 1: double the copies and each is worth half. It differs from the linear demand of MMO304 week 8, and it gives a clean result. At the steady state:

```
p* = A / S* = A × δ / F
crafting revenue per day = p* × F = A × δ
```

Read the last line twice. **The daily income of the whole crafting industry for this item is `A × δ`. It does not depend on how many copies crafters build.** Building more only lowers the price. What sets the size of the industry is how fast the world destroys the item.

**Currency ledger.** When a copy is lost, the game may pay insurance `I` per copy from an NPC. That is a faucet of `h × S × I` ISK per day. Losses destroy no currency on their own. Currency leaves only through sinks on the replacement trade, such as a sales tax `τ` on each purchase, worth `τ × A × δ` per day at the steady state.

- `S` copies in the world, `F` copies built per day.
- `h` loss hazard per copy per day, `r` recovery fraction, `δ = h(1 − r)`.
- `A` the ISK players hold in the item class, `p` the market price per copy.
- `I` the insurance paid per lost copy, `τ` the sales tax rate on replacement purchases.

### Numbers you can check

Use invented round numbers, not measured EVE data. One ship class. `F = 1,000` hulls per day. `h = 0.02` (each hull is lost once every 50 days on average). Players hold `A = 50` billion ISK in this class.

| Recovery `r` | `δ = h(1 − r)` | Mean life `1/δ` | Steady stock `S*` | Price `p*` | Crafting revenue per day `A × δ` |
|---|---|---|---|---|---|
| 0 (all destroyed) | 0.020 | 50 days | 50,000 | 1,000,000 | 1.0 billion |
| 0.5 | 0.010 | 100 days | 100,000 | 500,000 | 0.5 billion |
| 0.9 | 0.002 | 500 days | 500,000 | 100,000 | 0.1 billion |
| 1 (all transferred) | 0 | forever | no limit | falls toward 0 | 0 at the limit |

Check the second row: `S* = 1,000 / 0.01 = 100,000`, and `p* = 50,000,000,000 / 100,000 = 500,000`. Revenue is `500,000 × 1,000 = 0.5` billion, which equals `A × δ = 50 billion × 0.01`.

Notice that production and destruction are equal in every row with `δ > 0`. At the steady state, 1,000 hulls leave the world each day and 1,000 arrive. Counting "ships destroyed per day" tells you the production rate. It does not tell you how scarce ships are. The recovery fraction changes the stock tenfold between the first and third rows while the daily destruction count stays at 1,000.

Now one battle, using the ledger. A fleet of 1,000 ships dies. Each hull is worth 1,000,000 ISK and each carries fittings worth another 1,000,000. Hulls have `r = 0`. Fittings have `r = 0.5`, EVE's rule, described below. Insurance pays a net `I = 400,000` per hull.

| Ledger line | Amount |
|---|---|
| "Value destroyed" as the victims count it: `1,000 × (1M + 1M)` | 2.0 billion ISK |
| Items actually removed from the world: hulls `1.0B` + half the fittings `0.5B` | 1.5 billion ISK of items |
| Items transferred to the winners: half the fittings | 0.5 billion ISK of items |
| ISK destroyed by the battle | 0 |
| ISK created by insurance: `1,000 × 400,000` | +0.4 billion ISK |

The victims lost 2 billion minus 0.4 billion of insurance. The world lost 1.5 billion in goods. The currency supply grew by 0.4 billion. In the language of MMO304 week 4, the battle pushed the price level up twice: fewer goods and more money.

### A visual you can move

Open the interactive. The left view is the item ledger: stock over one year, with production and destruction per day drawn underneath. The right view is the currency ledger for the same year: insurance paid in, sales tax taken out, and the net. Drag `r` from 0 to 0.9. At `r = 0` the stock reaches its steady state of 50,000 within a few months, and destruction climbs to meet production at 1,000 a day. At `r = 0.9` the mean life is 500 days, so one year is not long enough. By day 365 the stock is about 259,000, only 52% of `S* = 500,000`, and destruction has reached only about 518 hulls a day. The year-end stock is about 5.2 times the `r = 0` stock and still rising, and the year-end price is lower by the same factor. Slower destruction does two things at once. It raises the eventual stock tenfold, and it makes the economy take much longer to settle, so a gap between production and destruction is not proof that something is broken. Now drag insurance up. The left view does not move at all. The right view turns from a small net sink to a clear net faucet. Players experience the left view. Your economist watches the right one.

### Cross-game recognition

Each game below is rewritten in the form `(h, r, insurance)`. Look for which of the three fates each rule chooses.

**EVE Online (current rules).** A destroyed ship's hull is always gone, so `r = 0` for hulls. Each fitted module and cargo item has a fixed 50% chance to drop into the wreck, where anyone can loot it, and is destroyed otherwise. Players call the coin flip the "loot fairy". So `r = 0.5` for fittings and cargo. Insurance pays up to 100% of CCP's own estimate of the hull's value (platinum level), covers only the hull, and is an NPC payout, so it is an ISK faucet. EVE is the full model: high `h`, split `r`, and a faucet attached to the sink.

**Ultima Online (launched 24 September 1997).** The game launched with unrestricted player-versus-player combat. A dead character's unblessed, uninsured items stay on the corpse, and the corpse decays after a few minutes if nobody recovers them. Here `r` is the chance that someone, the owner or another player, reaches the body in time. Decay is the destruction. In the Renaissance expansion (4 May 2000) the world was copied into two facets: Felucca kept non-consensual PvP, and Trammel allowed only consensual combat. In our terms, players were offered a copy of the world with `h` near zero for PvP losses. Letting players choose their own `h` is a design decision you will meet again in section 4.

**Old School RuneScape (current rules).** A player normally keeps their 3 most valuable items on death, 4 with the Protect Item prayer, and 0 if "skulled" for attacking another player. In the Wilderness, all unprotected items drop for the killer. That is `r ≈ 1`: a transfer, not a sink. The victim loses everything and the world loses almost nothing. Deaths to monsters work differently. Unprotected items go to a grave and can be reclaimed within 15 minutes, or later from an NPC for a fee. The item comes back (`r = 1`) and the fee is a **coin** sink. So OSRS moves the sink from items to currency.

**World of Warcraft (current).** Death never destroys equipment. It costs durability, which costs gold to repair (MMO304 week 8). For gear, `h × (1 − r) = 0`. Any item scarcity has to come from somewhere else, chiefly binding and obsolescence.

Four games, one form. EVE destroys items and pays ISK. UO destroys items only if nobody arrives in time. OSRS transfers items in PvP and sinks coins in PvM. WoW sinks gold and keeps every item. When you meet a new game's death rules, write down `h`, `r` and whether anything pays out, and you know which ledger each rule touches.

### Eyes-open design judgment

- **The victim feels `h`, the economy feels `h(1 − r)`.** Under full loot with `r = 1`, a victim loses their whole kit, yet the world is no scarcer. If your goal is to keep crafters employed, pure full loot does not do it. It redistributes gear from the weak to the strong. If your goal is tension and high stakes, `r` hardly matters to the victim.
- **The destruction rate sets the size of your industry.** Under unit-elastic demand, crafting income is `A × δ`. If you want a large crafting profession, you need a high `δ`, and you pay for it in player loss. Real demand is not exactly unit-elastic, but the direction holds.
- **Insurance couples your two ledgers.** Insurance makes loss bearable, which lets you raise `h`. It also turns every loss into a faucet. A game that encourages big battles and insures hulls must have currency sinks that grow with destruction, such as a tax on the replacement trade. Check the net on the right-hand ledger, not the gross.
- **Headlines count the victim's ledger.** Players, press and even studio marketing report "value destroyed" at market price. That number is neither currency destroyed nor goods destroyed. Do not let it guide policy.
- **Loss aversion is real.** Players weigh a loss more heavily than an equal gain. UO's Trammel split showed that when players can pick their own `h`, many pick a low one. Decide deliberately which activities carry loss, and make sure the players who opt in get something in return.

### Check yourself (worked example)

1. With `F = 1,000`, `h = 0.02` and `A = 50` billion, what `r` gives a steady-state price of 800,000 ISK?
2. In the battle ledger, what insurance payout per hull would make the battle's ISK effect exactly zero if a 5% sales tax is charged when the winners sell their looted fittings at full value?

<details>
<summary>Answers</summary>

1. `p* = A × δ / F`, so `δ = 800,000 × 1,000 / 50,000,000,000 = 0.016`. Then `1 − r = 0.016 / 0.02 = 0.8`, so `r = 0.2`.
2. Looted fittings are worth 0.5 billion, so the tax removes `0.05 × 0.5B = 25M` ISK. Insurance over 1,000 hulls must total 25M, so `I = 25,000` ISK per hull. Any real insurance level is far above this, which is why one-off taxes on loot cannot balance insurance.

</details>

## 3. The risk budget: what players choose to lose

Loss rules do not only move items. They change what players bring. A player deciding whether to take a ship out compares the fun or profit of the outing with the expected loss.

Let `q` be the chance of dying on one outing, `H` the hull's value, `G` the value of the fittings and cargo, and `I` the insurance. From the victim's point of view every carried item is lost, whatever `r` is, because recovered items go to someone else. So:

```
loss if killed     = H + G − I
expected loss      = q × (H + G − I)
```

Take `q = 0.1`, `H = 1,000,000`, `G = 1,000,000`, `I = 400,000`. The loss if killed is 1.6 million and the expected loss per outing is 160,000 ISK. A player who earns 2 million ISK per hour can fund that outing with 5 minutes of income. A player who earns 200,000 ISK per hour needs 48 minutes of income.

EVE players summarise this as "fly what you can afford to lose". The design consequence is that the player base sorts itself by risk. Rich players bring expensive fits, poorer players bring cheap ones, and a whole market for cheap "doctrine" ships appears. That is the demand side of the steady state in section 2. The items with the highest `h` are the cheap ones, because they are the ones players are willing to risk.

Two levers follow.

- **Insurance lowers the loss per death and raises `q` players will accept.** If insurance covers the hull fully, the player's risk is only the fittings. Expect more hulls to be flown and lost, and a larger ISK faucet.
- **Protection rules cap the loss.** OSRS's "keep 3 items" rule means a player's best three items never enter the risk budget. Players respond by carrying three valuable items and little else. The rule protects the victim, and it also removes the most valuable items from the item sink.

Protection rules deserve a closer look. Suppose a player carries items worth 10, 5, 3, 1, 1 and 1 million. Under a keep-3 rule, only 3 million is at risk. Under a keep-1 rule with Protect Item, the kept items are the 10 and 5, so 6 million is at risk. A skulled player keeps nothing, so all 21 million is at risk. The rule sets the size of the risk budget almost on its own. Players will optimise their inventory to it, so tune it before you tune drop rates.

## 4. Choosing `h` and `r`: zones, consent and the shape of loss

Most modern loss designs let the player choose `h` by choosing where to go. UO did this with two facets of the same world. EVE does it with security levels, where CONCORD, the NPC police, punishes attackers in high-security space and does not in null-security space. OSRS does it with the Wilderness boundary. The pattern is the same: a gradient of zones, with loss rules that get harsher and rewards that get richer as you move out.

Treat each zone as its own row in your ledger. A zone's contribution to item destruction is its population times `h × (1 − r)` times the value carried. If the rewarding zones are empty because the loss is too high, their `δ` is zero in practice, however harsh the rules on paper.

A zone design has three knobs, and each touches a different ledger:

| Knob | Item ledger | Currency ledger | What the victim feels |
|---|---|---|---|
| Raise `h` (more open PvP) | More destruction if `r < 1` | More insurance paid, if any | More frequent loss |
| Lower `r` (more destroyed, less looted) | More destruction | No change | No change: the victim lost it either way |
| Raise insurance `I` | No change directly, but players risk more | Larger faucet | Smaller net loss |

The middle row surprises students. Lowering `r` is almost invisible to victims. It changes what the killer receives, not what the victim loses. It is the cheapest lever you have for adding item scarcity without making loss feel worse. EVE's 50% coin flip is a compromise between rewarding the winner, who gets something, and feeding industry, since half is gone.

Why not set `r = 0` and destroy everything? Because the winner's reward matters. Loot is the payoff for PvP, and a PvP win that drops nothing gives players only the pleasure of the kill. The design question is how to split the loser's kit between the winner's pocket and the sink. Make that split on purpose.

### The currency side of destruction

Destruction removes goods, not money. So an economy with a lot of destruction and no matching currency sink tends toward rising prices, because the same money chases fewer goods. The standard fix is a tax on trade, which you will study in week 7 of this course. Replacement demand runs through the market, so a sales tax `τ` removes `τ × A × δ` ISK per day at the steady state. With `τ = 0.05`, `A = 50` billion and `δ = 0.01`, that is 25 million ISK per day. Compare it with insurance of `h × S* × I = 0.02 × 100,000 × 400,000 = 800` million ISK per day. The insurance faucet in this invented example is 32 times larger than the tax on the same trade. That is the kind of comparison CCP's economic reports let you make for the real game, and you will practise it in week 13.

## In-class activity (25 minutes)

In groups of three, design loss rules for a three-zone MMO: a safe starter zone, a contested middle zone and a lawless outer zone.

1. For each zone, choose `h` (per day, for a typical player's gear), `r` and an insurance rule. Write one sentence of justification per zone.
2. Assume `F = 500` sets of gear per day, `A = 20` million gold held in gear, and population shares of 60%, 30% and 10% across the three zones. Compute the effective `δ` for the whole server as the population-weighted average, then `S*`, `p*` and daily crafting revenue.
3. Compute the currency ledger: insurance paid per day and a 5% sales tax on replacement purchases. Is your design a net faucet or a net sink?
4. Swap designs with another group. Find the zone that nobody will visit, or the zone that makes crafting pointless, and say which knob you would turn.

Expected output: a filled table with three rows (one per zone), the server-wide numbers from step 2, the net currency figure from step 3 and one critique from step 4.

## Common misconceptions

- **"Full loot is a sink."** Only the destroyed share is. With `r = 1`, full loot is a transfer: the victim loses, the killer gains and the world's stock is unchanged.
- **"A battle that destroyed trillions shrank the money supply."** Losses destroy goods. Currency leaves only through sinks, and insurance adds currency. The money supply after a large battle can be higher than before.
- **"More destruction per day means items are scarcer."** At the steady state, destruction equals production. Scarcity is set by the stock `F / δ`, and the same daily destruction count fits a stock of 50,000 or 500,000 depending on `r`.
- **"If players hate losing gear, lower the drop rate for the killer."** Lowering `r` does not reduce what the victim loses. To reduce the victim's pain, lower `h`, add insurance or protect items.

## Check yourself

1. A game has `h = 0.03` per day for a helmet class and destroys 40% of lost helmets, looting the rest. Players build 600 helmets a day. What are `δ`, `S*` and the mean life of a helmet?
2. With `A = 12` million gold held in helmets, what is the steady-state price and the daily crafting revenue from question 1? If crafters double production to 1,200 per day, what happens to each?
3. A designer adds insurance paying 30 gold per lost helmet from an NPC. At the steady state of question 1, how much gold does it create per day? What sales tax rate on replacement purchases would cancel it?
4. Rewrite this rule in `(h, r, insurance)` form and say which ledger it touches: "On death in dungeons, you drop nothing but pay 2% of your gold to resurrect."

<details>
<summary>Answers</summary>

1. `δ = 0.03 × (1 − 0.6) = 0.012`. Here 40% are destroyed, so `r = 0.6`. `S* = 600 / 0.012 = 50,000`. Mean life `1 / 0.012 ≈ 83` days.
2. `p* = 12,000,000 / 50,000 = 240` gold. Revenue `240 × 600 = 144,000` gold per day, which equals `A × δ = 12M × 0.012`. At 1,200 per day, `S* = 100,000`, `p* = 120`, and revenue stays `144,000`. Doubling output halves the price.
3. Helmets lost per day `= h × S* = 0.03 × 50,000 = 1,500`, so insurance creates `45,000` gold per day. Replacement spending is 144,000 per day, so a tax of `45,000 / 144,000 ≈ 31%` would be needed. That is far too high, which tells you the insurance is too generous.
4. `h > 0` for currency only, `r = 1` for every item (nothing drops), no insurance. It touches only the currency ledger: a death-scaled currency sink, and a stock sink since it is proportional to wealth (MMO304 week 3). The item stock is untouched.

</details>

## Lab / assignment hook

[Lab 10, loss rules in an agent-based economy](../labs/lab10.md). You extend a starter agent-based model so that agents fight, lose items under `(h, r, insurance)` rules, rebuild from crafters and pay a sales tax. You run three loss policies for a simulated year and write a 400-word memo recommending one. This feeds the ABM labs component (40%) and the final agent-based economy.

## Sources

- Wikipedia, "Bloodbath of B-R5RB" (retrieved September 2026). Dates 27-28 January 2014, 21 hours, over 7,500 characters, 75 titans destroyed, about 11 trillion ISK, an estimated US$300,000-330,000, and the missed sovereignty payment that started it.
- EVE University Wiki, "Loot Fairy" (current). The fixed chance that a destroyed ship's modules and cargo drop, 50% for most of EVE's history.
- EVE University Wiki, "Insurance" (page updated March 2023). Platinum pays 100% of CCP's estimate of hull value, covers only the hull, and is an NPC payout.
- Wikipedia, "Ultima Online" and "Ultima Online: Renaissance" (retrieved September 2026). Launch on 24 September 1997 with unrestricted PvP; Renaissance released 4 May 2000 in North America, splitting the world into Felucca and Trammel.
- UOGuide, "Death" (current). Unblessed, uninsured items stay on the corpse and decay beyond recovery after a few minutes.
- Old School RuneScape Wiki, "Items Kept on Death" (current). Keep 3 items, 4 with Protect Item, 0 when skulled; unprotected items drop for the killer in PvP; PvM deaths use a grave with a 15-minute window and a fee for later recovery.
- MMO304 week 8 for World of Warcraft's durability rules and their sources.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w10-loss-ledger.html

**The one insight:** at the steady state, items destroyed per day always equals items built per day, whatever the loss rules. The recovery fraction `r` and the hazard `h` change the *stock* and the *price* by large factors while the daily destruction count looks the same, and insurance changes only the currency ledger. Two linked views make this visible: the item ledger (what players see) and the currency ledger (what the economist sees).

**Layout.** Two panels side by side on desktop, stacked on mobile with the item ledger first. A readout table below both panels.

**Left panel, item ledger.** x-axis: day 0 to 365. Top chart: stock `S(t)` as a solid line, with a dashed horizontal line at `S* = F / δ` (hidden when `δ = 0`). A second y-axis or a small chart underneath: price `p(t) = A / S(t)` (clip to a maximum of `10 × A / F` when `S` is near 0 on day 0; start the simulation at `S(0) = F`). Bottom strip: two lines for production per day (flat at `F`) and destruction per day `δ × S(t)`.

**Right panel, currency ledger.** Same x-axis. Stacked bars or lines per day: insurance paid `h × S(t) × I` (positive, labelled "faucet"), sales tax `τ × p(t) × F` (negative, labelled "sink"), and the net as a bold line. A running total "net ISK added this year" in large type.

**Controls.**
- `F` built per day: 100 to 5,000, step 100, default 1,000.
- `h` loss hazard per day: 0 to 0.10, step 0.005, default 0.02.
- `r` recovery fraction: 0 to 1, step 0.05, default 0.5.
- `A` ISK held in the class: 5 to 200 billion, step 5, default 50.
- `I` insurance per lost copy: 0 to 1,000,000, step 50,000, default 400,000.
- `τ` sales tax: 0 to 0.10, step 0.005, default 0.05.
- A "one battle" button that removes 1,000 copies at day 180 (applying `r`: `1,000 × (1 − r)` destroyed) and adds `1,000 × I` to the currency ledger that day, so students see the spike on the right and the dent on the left.
- Preset buttons: "EVE-like" (`h 0.02, r 0.5, I 400,000`), "Full-loot transfer" (`r 1, I 0`), "No loot, destroy all" (`r 0, I 0`), "WoW-like" (`h 0`).

**Model, per day.** `δ = h × (1 − r)`. `S(t+1) = S(t) + F − δ × S(t)`. `p(t) = A / S(t)`. Insurance `h × S(t) × I`. Tax `τ × p(t) × F`. Use the discrete update exactly, not the continuous formula.

**Readout table** (copyable): `δ`, mean life `1/δ` (show "forever" at 0), `S*`, `p* = A δ / F`, crafting revenue `A × δ`, insurance per day at steady state `h × S* × I`, tax per day at steady state `τ × A × δ`, net per day.

**Test values** (defaults except where stated, steady-state figures):
- `r = 0`: `δ = 0.02`, `S* = 50,000`, `p* = 1,000,000`, revenue 1.0 billion per day.
- `r = 0.5`: `δ = 0.01`, `S* = 100,000`, `p* = 500,000`, revenue 0.5 billion, insurance 800 million per day, tax 25 million per day, net +775 million per day.
- `r = 0.9`: `δ = 0.002`, `S* = 500,000`, `p* = 100,000`, revenue 0.1 billion.
- `r = 1`: stock line rises by exactly 1,000 per day, readout shows "no steady state".
- Discrete check with `r = 0.5` from `S(0) = 1,000`: `S(1) = 1,000 + 1,000 − 10 = 1,990`.

**Accessibility.** Keyboard-operable sliders with visible focus and live-region readouts. Lines distinguished by dash pattern and label, not colour alone. With `prefers-reduced-motion`, update charts without animated transitions.
