# GD102 · Week 06 — Machinations diagrams II: converters, traders, gates

**Why this matters:** Most interesting decisions in a game economy are exchanges. You turn wood into planks, four sheep into one ore, a kill into a random item. Last week's pools, sources and drains cannot draw an exchange. This week's three nodes can, and once you can draw an exchange you can price it.

**You will be able to:**
- Model an exchange with a converter, a trader or a gate, and explain which of the three conserves resources.
- Compute the flow estimate for a converter path, `time ≈ amount needed / (input rate ÷ ratio)`, and explain why a simulation of the same diagram comes out slower.
- Use triggers and activators to connect nodes, including a drain that switches on when a pool grows too large.
- Critique a converter ratio as a price: what it makes possible, what it makes pointless, and what it exposes to other rules.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), the rest of chapter 5 (converters, traders, gates, triggers, activators). Skim the base-game rulebook of Catan (free from catan.com), sections on production, trade and rolling a 7.

**Prerequisites from earlier courses:** [GD102 week 5, Machinations diagrams I](w05-machinations-diagrams-i.md) and [week 4, negative feedback loops](w04-negative-feedback-loops-rubber-banding.md). Two-dice probabilities and Catan's number tokens from [MA102 week 8, dice sums](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md). Expected value from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). Weighted drop tables from [MA102 week 9](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md).

**Interactive:** [A converter charges twice](../examples/w06-catan-converter.html). Keep it open during section 2.

---

## 1. Three nodes for exchange

### Converters

A **converter** takes resources of one kind in and puts resources of another kind out. In Dormans' notation it is drawn as a vertical line over a triangle pointing right. A trader is a vertical line over two triangles, one pointing left and one pointing right. Its incoming connections say what it consumes each time it fires, and its outgoing connections say what it produces. A converter that takes 4 wool and gives 1 ore has an incoming label of 4 and an outgoing label of 1.

A converter is a drain and a source glued together. The inputs are destroyed and the outputs are created. So a converter **does not conserve resources**. Four wool go out of existence and one ore comes into existence. That is why converters are where prices live. The ratio of input to output is an exchange rate the designer sets.

Converters almost always pull **all or nothing**. A crafting recipe that took 3 of the 4 wool it needed and produced nothing would be a bug. Remember the `&` mark from week 5.

### Traders

A **trader** moves resources between two owners in both directions at once. When it fires, resource A flows from the first party to the second and resource B flows from the second party to the first. Nothing is created or destroyed. So a trader **conserves resources**. The total amount of wool and ore in the game is the same before and after.

Traders are how Machinations draws player-to-player trade, where the value comes from the fact that the two players need different things. The negotiation itself happens outside the diagram. The trader only records the swap once both sides agree.

### Gates

A **gate** holds nothing. It is drawn as a diamond. Resources arriving at a gate leave immediately along one of its outputs, and the gate decides which one.

- A **deterministic gate** distributes by rule. Labels on the outputs are weights or conditions. A gate with three outputs weighted 1, 1, 1 sends the first resource to output one, the second to output two, the third to output three, then starts again. This is how you draw "split the loot evenly".
- A **random gate** is marked with a die. Its output labels are probabilities or weights, and each arriving resource goes to one output chosen at random. This is how you draw a loot table, a dice roll or a card draw.

A gate's outputs can also be state connections. Then the gate does not move a resource to an output, it *fires* whatever that output is connected to. That lets one random roll decide which of several things happens. The gate becomes a switch.

### Triggers and activators

Two more kinds of state connection complete the language you need for this course.

- A **trigger** is a dotted arrow marked `*`. When its source node fires (or, for a pool, when it receives resources), the node at the other end fires too. Triggers chain events: "when a card is played, draw a card".
- An **activator** is a dotted arrow labelled with a condition, such as `>7` or `==0`. The target node can only fire while the condition on the source pool is true. Activators switch nodes on and off: "the shop is open only when you have at least 10 gold".

With converters, traders, gates, triggers and activators added to last week's elements, you can draw the internal economy of almost any game you have played. Week 7 uses them to build complete economies.

## 2. Worked example: the bank trade that prices ore you do not mine

### The hook

In Catan, a city costs 3 ore and 2 grain. It replaces one of your settlements, is worth 2 victory points instead of 1, and produces two resource cards instead of one whenever its hexes pay out. Cities are the fastest way to grow.

Now suppose none of your settlements touches a mountain hex. You produce no ore at all. You are not locked out, because the rules let you trade with the bank at 4 identical cards for 1 card of your choice, any time on your turn. A settlement on a harbor improves that rate to 3 of any one type for 1, or at special harbors to 2 of the named type for 1.

Players feel two things about this. First, the bank trade is always there, so no resource is ever truly out of reach. Second, the bank trade is slow and it seems to get slower than it should. Hands grow large while you save up four of a kind, and then someone rolls a 7. With more than 7 cards in hand you lose half, rounded down.

This worked example measures both feelings with one diagram.

### One model, stated once

The Machinations diagram has four parts.

```
   random gate (2d6) ──▶ Grain, Wool, Lumber, Brick, Ore pools
   converter  (r : 1)   : r identical cards  ──▶ 1 ore
   city       (& pull)  : 3 ore + 2 grain    ──▶ done
   discard drain        : activated when hand > 7, triggered by a roll of 7
```

- The **random gate** is the dice roll. Each output goes to a hex's resource pool with probability `pips / 36`, where pips is the number of ways two dice make that number (MA102 week 8). A 6 or an 8 has 5 pips, a 9 has 4, a 10 has 3. A 7 produces nothing.
- The **converter** is the bank or a harbor. It has ratio `r`: 4 at the bank, 3 at a generic harbor, 2 for the named resource at a special harbor.
- The **city** is an all-or-nothing drain that needs 3 ore and 2 grain.
- The **discard drain** is the 7 rule. It is triggered by the 7 output of the gate, and an activator with condition `hand > 7` decides whether it removes anything.

The **flow estimate** ignores the dice's randomness and treats each hex as a steady trickle of `pips / 36` cards per roll. Then:

```
rolls to collect n cards of a resource  ≈  n / (pips / 36)
ore arriving per roll via a converter   ≈  (surplus cards per roll) / r
rolls to a city                         ≈  the slower of (grain needed, ore needed)
```

### Numbers you can check

Two players. Both have settlements touching four hexes and both start with an empty hand. We count every roll of the dice, since in Catan every player collects on every roll. We let them trade right after each roll and spend nothing else. These are simplifications, and we will come back to them.

- **Ore player.** Grain on 6 (5 pips), ore on 8 (5 pips), lumber on 9 (4 pips), brick on 10 (3 pips). This player also uses the bank. Whenever they hold 4 spare cards of one kind (grain beyond the 2 they need, lumber or brick), they trade them 4:1 for an ore, exactly as the no-ore player does.
- **No-ore player.** Grain on 6 (5 pips), wool on 8 (5 pips), lumber on 9 (4 pips), brick on 10 (3 pips).

Grain is the same for both. Two grain at `5/36` per roll takes `2 × 36 / 5 = 14.4` rolls. Ore decides the race.

| Setup | Ore arriving per roll | Flow estimate, rolls to 3 ore |
|---|---|---|
| Ore player, mines it (bank ignored) | `5/36 = 0.139` | `3 / 0.139 = 21.6` |
| No ore, bank 4:1 | `(5 + 4 + 3)/36 ÷ 4 = 3/36 = 0.083` | `36.0` |
| No ore, generic harbor 3:1 | `12/36 ÷ 3 = 4/36 = 0.111` | `27.0` |
| No ore, wool harbor 2:1 (others 4:1) | `(5/2 + 4/4 + 3/4)/36 = 4.25/36 = 0.118` | `25.4` |

Check the bank row by hand. The no-ore player makes `5 + 4 + 3 = 12` pips of spare cards, wool, lumber and brick, which is 12 cards every 36 rolls. At 4 for 1 that is 3 ore every 36 rolls. So 36 rolls for the 3 ore a city needs.

So the flow estimate says the bank is a 67% time penalty on a city (36 against 21.6), and a harbor cuts it to about a 25% penalty.

Now run the same diagram for real, with random rolls, whole cards, and the rule that you can only convert when you hold 4 *identical* cards. The simulation below plays 20,000 games per row.

| Setup | Flow estimate | Mean rolls, no discard | Mean rolls, with 7-discard | 90th percentile, with discard |
|---|---|---|---|---|
| Ore player | 21.6 | 22.0 | 22.8 | 35 |
| No ore, bank 4:1 | 36.0 | 39.4 | 83.8 | 143 |
| No ore, harbor 3:1 | 27.0 | 30.0 | 37.5 | 57 |
| No ore, wool harbor 2:1 | 25.4 | 30.4 | 39.0 | 60 |

Two gaps open up between the estimate and the simulation.

**The batching gap.** Even with no discard, the converter paths are about 3 to 5 rolls slower than the flow estimate. A converter works only on whole batches of identical cards. Three wool, three lumber and two brick is eight spare cards, which the flow estimate counts as two ore, but at 4:1 you can convert none of them. Cards sit idle below the ratio. The bigger the ratio, the more cards sit idle. The ore player's estimate is almost exact. Mining needs no batches, and the occasional 4:1 trade of spare lumber, brick or grain (which the estimate leaves out) makes up for the dice's randomness.

**The exposure gap.** Turn on the discard rule and the bank path more than doubles, from 39.4 to 83.8 rolls, and one game in ten takes 143 rolls or more. The ore player barely notices, 22.0 to 22.8. The reason is in the diagram. The converter path needs a big hand. You need 12 spare cards plus 2 grain, and you cannot spend them early because they only convert in fours. So you spend many rolls holding more than 7 cards, and the activator on the discard drain is switched on for all of that time. Each 7 (one roll in six) then takes half your hand. The ore player holds a small hand and spends it quickly, so the activator is almost never on.

That is the insight. **A converter makes a resource reachable, but it charges you twice. Once in the ratio, and again in whatever the game does to large stockpiles.**

### A visual you can move

Open `examples/w06-catan-converter.html`. The left panel is the diagram above, drawn with the random gate, the resource pools, the converter and the city, with the discard drain and its activator shown as a dotted line that lights up whenever the hand holds more than 7. The right panel is a histogram of rolls-to-city across 2,000 simulated games, with a vertical line at the flow estimate and another at the simulated mean.

Choose "No ore, bank 4:1" and toggle the discard rule. The diagram looks the same with the rule on or off, apart from one dotted line. The histogram's long right tail appears and disappears. Then switch to "Ore player" and toggle again. Nothing happens. The rule is identical for both players, but it only bites the one whose strategy requires a stockpile.

Below the histogram, a single sample game shows hand size over time, with a line at 7 cards and a mark for each 7 rolled. Watch how long the converter player spends above the line.

### Cross-game recognition

Rewrite each of these as a converter, trader or gate with a ratio.

**Minecraft (Java Edition, current).** One log crafts into 4 planks. That is a converter with input 1 and output 4. Converters can multiply as well as divide. The ratio still sets a price: a log is worth four planks, and every plank recipe inherits that price.

**Factorio (base game, 2.0 era).** An iron gear wheel takes 2 iron plates and 0.5 seconds of crafting time. A converter with ratio 2:1 and a delay. The time is a second cost, like the stockpile cost in Catan. It is the reason Factorio players build many assemblers in parallel instead of one. The throughput of a converter is its ratio *and* its speed.

**Mario Kart 8 Deluxe.** The item box is a random gate. Its output weights are not fixed. They depend on how far the racer is from the front-runner, which in Machinations is a state connection from a "distance behind" pool to the gate's weights. It is the week 4 balancing loop drawn in this week's language.

**Catan, player-to-player trade.** On your turn you may trade cards with other players on any terms you agree. That is a trader. Unlike the bank trade, it conserves cards. Four wool leave you and one ore leaves your partner. And it can be better for both of you, because each gives away what they value less. The bank never gains from a trade, so it has no reason to offer you a good rate. That is why 4:1 is the rate you get from nobody in particular.

Four games, and each exchange is either a converter (resources change kind at a set ratio), a trader (resources swap owners and are conserved), or a gate (resources or events are routed by rule or by chance).

### Eyes-open design judgment

A converter ratio is a price, and every price has consequences.

- **A universal converter makes every resource partly interchangeable.** Catan's bank means no player is ever locked out of a building type. That keeps weak starting positions playable. It also means resource specialization is never total, which makes the map's layout matter a bit less.
- **The ratio decides whether specialization matters.** At 2:1 everywhere, producing ore yourself would barely beat trading for it, and placement would stop mattering. At 8:1, a player without ore could not build cities at all in a normal game. The 4:1 bank sits where trading is possible but clearly worse than producing, and harbors let a player buy a better ratio with a settlement spot.
- **Converters create stockpiles, and stockpiles meet other rules.** Batching means players hold cards they cannot yet use. Any rule that punishes large holdings, a discard, a theft, a storage cap, a decay drain, taxes the converter path hardest. Whether the Catan designers intended the discard to tax the bank path is not something the rules tell us. Your job is to notice the interaction and decide whether you want it.
- **Traders create social play; converters do not.** A trader needs two parties who both agree, so it creates negotiation, and it favours players that others are willing to deal with. If you want to reduce social pressure, replace traders with converters. If you want more of it, make converter rates poor.

Decide deliberately: the ratio, the batch size (the input label), whether there is a delay, and which other rules act on the pools a converter needs.

## 3. Traders in more detail

A trader is the only node that is guaranteed to conserve resources in both directions. That makes it the right tool for checking whether an economy is inflating. If every exchange in your game is a trader, the total amount of each resource can only change through sources and drains, and you can see all of them.

Real games often disguise converters as traders. A shop where you "trade" gold for a sword is not a Machinations trader, because the shopkeeper's gold and swords are not tracked. It is a converter: gold destroyed, sword created. That distinction matters in week 7 and in MMO304, because a converter from money to items is a **sink** for money, while a real player-to-player trade is not. Mislabel it, and your inflation model is wrong.

When you draw a trader, draw both owners' pools. If you find yourself drawing only one side, it is a converter.

## 4. Gates in more detail

### Deterministic gates share things out

A deterministic gate with outputs weighted 2 and 1 sends two resources to the first output, then one to the second, and repeats. So two thirds of the flow goes one way and one third the other, *exactly*, in a fixed order. Use this for any rule that splits by fixed shares: loot shared by a party, tax taken as a fixed fraction, a production building that alternates its output.

A deterministic gate can also have conditions on its outputs, such as `>3` on one and `<=3` on the other. Then it routes by value, for example sending resources to a reserve pool once a primary pool is full.

### Random gates are drop tables

A random gate with outputs labelled 70%, 25% and 5% is a drop table with a common, uncommon and rare item. Its behaviour is the weighted table from MA102 week 9. What Machinations adds is what happens *next*: the items land in pools, and those pools can feed converters, activate other nodes, or be sold. The gate is the start of a chain, not the end of the calculation.

When the output labels sum to less than 100%, the rest goes nowhere. In other words, "nothing drops". It is good practice to draw that missing share as an explicit output into a drain labelled "nothing", so that a reader sees it.

### Gates as switches

Connect a gate's outputs to triggers instead of resource connections, and each arriving resource fires one of several events. A random gate with four trigger outputs is a random-event table. A turn-counter feeding a deterministic gate with conditions is a scripted sequence. Catan's dice are exactly this: one roll, eleven trigger outputs, one of which fires the robber and the discard.

## 5. Putting it together: one Catan turn in six nodes

To see how the pieces work together, read a full turn of the worked example off the diagram.

1. An **interactive** node, "roll", pushes one resource into the **random gate**.
2. The gate chooses an output with weights 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1 for the totals 2 to 12.
3. If the output is a production number, a **trigger** fires every source attached to that number, and each pushes 1 card (2 for a city) into its resource pool.
4. If the output is 7, a **trigger** fires the discard drain. The drain has an **activator** with condition `hand > 7`, and pulls half the hand rounded down.
5. The player may fire the **converter** (interactive, all-or-nothing) as often as they can pay.
6. The player may fire the **city** (interactive, all-or-nothing) if the ore and grain pools hold 3 and 2.

Every node in that list comes from weeks 5 and 6. The diagram now answers questions you could not answer before, such as "how much does a 3:1 harbor speed up my first city", by running.

## In-class activity (25 minutes)

Pairs, one laptop with machinations.io and one sheet of paper.

1. **Classify.** For each of these, write converter, trader or gate, and the ratio or weights: a blacksmith recipe of 3 iron and 1 coal to 1 sword; an auction house where players list items for other players' gold; a chest that drops gold 60%, a potion 30%, nothing 10%; a quest that turns in 10 wolf pelts for 50 gold and 200 experience. (5 minutes)
2. **Draw.** Draw the Catan diagram from section 5 for the no-ore player with a 3:1 harbor. Include the discard drain and its activator. (10 minutes)
3. **Build and predict.** Build the gate, the pools and the converter in the tool. Before running, write down your predicted mean rolls to 3 ore with the discard off. Run it 50 times with the tool's batch runner if available, or by hand-stepping 5 games. (10 minutes)

Expected output: the classification list with ratios, one paper diagram, one prediction and one measured mean. Compare with the lecture's table.

## Common misconceptions

- **"A converter and a trader are the same, since both swap one thing for another."** A converter destroys its inputs and creates its outputs. A trader moves both resources between two owners and conserves them. For inflation this is the difference between a sink and no sink.
- **"The flow estimate is the answer."** The flow estimate is a lower bound on a converter path. Batching means cards sit idle below the ratio, and any rule acting on large holdings adds more delay. Simulate before you tune.
- **"A rule that applies equally to everyone is neutral."** Catan's discard hits every player with the same threshold, but in the simulation it more than doubles the bank-trade path and barely touches the ore producer. Rules act on strategies, not on players.
- **"A random gate with weights 70, 25, 5 gives a rare item every 20 opens."** On average, yes. MA102 weeks 7 and 10 showed how far individual players stray from that. A gate's weights describe the long run, not anyone's session.

## Check yourself

1. A no-ore player's spare cards arrive at 15 pips per 36 rolls, and they have a 3:1 generic harbor. What is the flow estimate for 3 ore? Will the simulated mean be higher or lower, and why?
2. A game has a converter that turns 5 wood into 1 plank and another that turns 1 plank into 4 wood. What happens if a player fires them in a loop? What single number would you change to fix it, and to what range?
3. A crafting system gives "3 ore → 1 bar" with a 10-second delay. A player has 60 ore and one furnace. How long until all bars are made? What changes with three furnaces?
4. You want to reduce how often players are stuck holding large hands in a Catan-like game without changing the converter ratio. Name two changes to the diagram, one to the drain and one to the activator, and predict the effect on the bank path.

<details>
<summary>Answers</summary>

1. Ore per roll ≈ `15/36 ÷ 3 = 5/36`, so 3 ore takes `3 × 36 / 5 = 21.6` rolls. The simulated mean will be higher, because conversions happen only in whole batches of 3 identical cards and spare cards sit idle below the ratio, and because the discard rule punishes the hand needed to form those batches.
2. 5 wood → 1 plank → 4 wood loses 1 wood per loop, so the loop drains the player and is harmless. If the second converter gave 6 wood, each loop would create 1 wood from nothing, an infinite source. The plank-to-wood output must stay at or below 5. Better, remove the reverse converter or make it give no more than the forward input.
3. 60 ore makes 20 bars. With one furnace, 20 × 10 s = 200 seconds. With three furnaces working in parallel, about 7 bars each, so 7 × 10 = 70 seconds, the last furnace finishing one bar fewer. Ratio unchanged, throughput tripled.
4. Change the drain to remove fewer cards (a quarter instead of half), or change the activator threshold (for example, `hand > 9`). Both shrink the exposure gap. The threshold change helps the bank path most, because that path spends many rolls holding 8 or 9 cards, all of which would now be safe.

</details>

## Lab hook

**Lab 06, pricing a converter** ([labs/lab06.md](../labs/lab06.md)). You rebuild the worked example's diagram in Machinations or a script, reproduce two table rows, then design a converter ratio and a hand-limit rule for a new resource that meets a stated target for how much slower trading should be than producing.

## Sources

- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 5: converters, traders, gates (deterministic and random), triggers and activators. Element behaviour in this lecture follows the book.
- Dormans, J. (2012). *Engineering Emergence: Applied Theory for Game Design*. PhD thesis, University of Amsterdam (ILLC DS-2012-12). Chapter 4: converter as a vertical line over a right-pointing triangle, trader as a vertical line over left- and right-pointing triangles, gates as diamonds (deterministic gates plain, random gates marked with a die), triggers labelled `*`, activators labelled with a condition such as `==0` or `>=4`, interactive nodes with a double outline and automatic nodes marked `*`.
- Machinations.io documentation, "Converters & Traders" (accessed September 2026). A converter acts as a drain that triggers a source, in one step; a trader changes the ownership of two colour-coded resources.
- Catan GmbH, *Catan: Game Rules & Almanac*, base game, 2015 edition (downloaded from catan.com). City costs 3 ore and 2 grain, is worth 2 victory points and produces 2 cards per paying hex. Maritime trade at 4:1 always available; harbors give 3:1 or, for the named resource, 2:1. Rolling a 7: no production, players with more than 7 resource cards return half rounded down. Players may trade with each other on their turn. Number tokens carry pips, and 6 and 8 have 5 each.
- Wikipedia, "Catan" (accessed 2026). Summary of bank trade at four-to-one and harbor trades at three-to-one and two-to-one.
- Minecraft Wiki, "Planks" (Java Edition, accessed September 2026). One log crafts into 4 planks.
- Factorio Wiki, "Iron gear wheel" (base game, 2.0 era, accessed September 2026; the infobox recipe is "Time, 0.5 + Iron plate, 2"). 2 iron plates, 0.5 s crafting time, 1 gear.
- Super Mario Wiki, "Spiny Shell (Mario Kart)". Item distribution in Mario Kart 8 Deluxe depends on distance from the front-runner.
- Simulation results in section 2 were computed for this course (Python, 20,000 games per row, seed 7) with the model and policies given in the interactive spec. They describe the course model, not measured play.

## Interactive spec: examples/w06-catan-converter.html

**The one insight.** A converter makes a missing resource reachable, but it charges twice: once in the ratio, and again through any rule that punishes the stockpile the converter needs. Toggling the discard rule must visibly wreck the bank-trade path and leave the ore producer almost untouched.

**Layout.** Left (top on mobile): the Machinations diagram. Right (below on mobile): the histogram, then the sample-game trace. Control bar above both.

**Controls.**
- Radio group `setup`: "Ore player" or "No ore" (default "No ore").
- Radio group `converter` (only enabled for "No ore"): "Bank 4:1" (default), "Harbor 3:1", "Wool harbor 2:1 (others 4:1)". The ore player always has the bank at 4:1 for spare grain, lumber and brick; the control is disabled because that player has no other choice.
- Checkbox `7-discard rule`, default on.
- Button "Run 2,000 games" (runs on load and on every change). Button "New sample game".
- Keyboard: all controls reachable by Tab, radio groups respond to arrow keys.

**Model (one game).**
- Hexes. Ore player: grain on 6, ore on 8, lumber on 9, brick on 10. No-ore player: grain on 6, wool on 8, lumber on 9, brick on 10. One settlement per hex (1 card per payout).
- Hand starts empty. Each roll is the sum of two fair d6 from a seeded PRNG (mulberry32, seed 7 by default).
- If the roll is 7 and the discard rule is on and hand size > 7: discard `floor(hand / 2)` cards one at a time, each time taking one card from the resource with the largest *surplus*, where surplus is count minus need (need is 2 for grain, 3 for ore, 0 otherwise); ties broken by larger count, then by the order grain, wool, lumber, brick, ore.
- Otherwise add 1 card to each resource whose hex number equals the roll.
- Then convert: while ore < 3, repeatedly go through wool, lumber, brick, grain in that order; for each, if `count − need ≥ ratio`, spend `ratio` of it for 1 ore. Ratio is 4 for the bank, 3 for the generic harbor, 2 for wool and 4 for others with the wool harbor. The ore player runs the same loop at ratio 4 (its hand has no wool, so only lumber, brick and spare grain convert). Stop when no conversion is possible or ore reaches 3.
- The game ends on the first roll after which grain ≥ 2 and ore ≥ 3. Record the roll count. Cap at 500 rolls.

**Diagram panel.** Random gate (diamond with a die mark) with outputs to the four hex pools labelled with pips/36; resource pools as circles with live counts in the sample game; converter (right-pointing triangle with bar) labelled with the ratio; city drain with `&`; discard drain with a dotted activator line from the hand total labelled `> 7` and a dotted trigger from the gate's 7 output. The activator line glows when the sample game's hand exceeds 7.

**Histogram panel.** x axis rolls to city (0 to 200, bins of 5, overflow bin "200+"), y axis share of games. Vertical lines: flow estimate (dashed) and simulated mean (solid). Readout: flow estimate, mean, median, 90th percentile.

**Sample-game trace.** x axis roll number, y axis hand size. Horizontal line at 7. Mark each roll of 7 with a small tick and each conversion with a dot.

**Flow estimates to display.** Ore player 21.6; bank 36.0; harbor 3:1 27.0; wool harbor 25.4 (formulas in lecture section 2).

**Test values** (2,000 games; accept ± 2 rolls on means under 40 and ± 6 rolls on the bank-with-discard mean; percentiles ± 10%):

| Setup | Converter | Discard | Mean | Median | 90th pct |
|---|---|---|---|---|---|
| Ore player | bank 4:1 for spares | off | 22.0 | 21 | 32 |
| Ore player | bank 4:1 for spares | on | 22.8 | 21 | 35 |
| No ore | bank 4:1 | off | 39.4 | 39 | 50 |
| No ore | bank 4:1 | on | 83.8 | 74 | 143 |
| No ore | harbor 3:1 | off | 30.0 | 29 | 39 |
| No ore | harbor 3:1 | on | 37.5 | 34 | 57 |
| No ore | wool harbor 2:1 | off | 30.4 | 30 | 40 |
| No ore | wool harbor 2:1 | on | 39.0 | 36 | 60 |

**Style.** Shared palette from `templates/interactive-tokens.css`. Hexes and cards drawn as plain shapes with text labels; no Catan art, logo or card designs. Name Catan only in the caption.
