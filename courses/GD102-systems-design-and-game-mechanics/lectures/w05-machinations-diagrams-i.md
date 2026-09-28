# GD102 · Week 05 — Machinations diagrams I

**Why this matters:** A loop you can only describe in words is a loop you can only argue about. Machinations gives you a small drawing language for resources, where they come from, where they go and what controls the flow, and the drawing runs. This week you learn enough of it to model a real resource system and read the answer off the simulation.

**You will be able to:**
- Draw a resource system with pools, sources, drains and resource connections, choosing an activation mode and a pull or push rule for each node.
- Compute waste in a capped pool with the rule `waste = rate × time at cap`, and check any model with the conservation equation.
- Translate a resource rule from a shipped game (mana, energy, elixir) into a Machinations diagram and back.
- Add a state connection that turns a flow diagram into a feedback loop, and name the loop's sign.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 4 (internal economy) and chapter 5 (Machinations) up to, but not including, converters and traders. Create a free account at machinations.io and open one of its starter templates.

**Prerequisites from earlier courses:** GD102 [week 2, stocks and flows](w02-stocks-and-flows.md), and [week 4, negative feedback loops](w04-negative-feedback-loops-rubber-banding.md). Resources as a formal element from GD101 [week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md). Rates as slopes from [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md).

**Interactive:** [Capped pool simulator](../examples/w05-capped-pool.html). Keep it open during section 3.

---

## 1. Why a diagram that runs

Week 2 gave you stocks and flows, and weeks 3 and 4 gave you loops with signs. Those causal loop drawings are good for thinking. They are poor for testing, because a `+` arrow says "more of this means more of that" without saying how much, how fast, or what happens when a stock runs out.

**Machinations** is a diagram language for game economies created by Joris Dormans and set out in the Adams and Dormans book. A Machinations diagram has two properties that a whiteboard sketch lacks:

- **Every element has exact behaviour.** A node that produces resources produces a stated number per step. A connection that moves resources moves a stated amount. There is no "roughly".
- **The diagram can be run.** Press play and resources move step by step according to those rules. You can watch a pool fill, see where resources pile up, and run the same diagram a thousand times to collect statistics.

The browser tool at machinations.io implements this language with a few extra features and some differences in how symbols are drawn. This course uses the book's element names and describes each element by behaviour, so you can work in either the tool or on paper. When the tool's symbol differs from the book's, trust the behaviour, not the picture. One naming difference to know now: the tool calls activation modes "trigger modes", and it calls the starting action mode "enabling".

A useful way to see the language: a **causal loop diagram** tells you the *shape* of a system, which loops exist and their signs. A **Machinations diagram** tells you the *numbers*, and so it can tell you which loop dominates (week 4, section 4) instead of leaving that to argument.

## 2. The first four elements

### Resources

A **resource** is anything the game counts that can be moved, created or destroyed. Gold, wood, health points, ammunition, cards in hand, victory points, even time. In Machinations resources are drawn as small tokens. Different kinds of resources can be told apart by colour.

### Pools

A **pool** is a place where resources collect. It is the Machinations name for a stock. It is drawn as an open circle, with the number of resources inside written in it or drawn as tokens. A pool can have a **capacity**, a maximum it can hold. Anything arriving when the pool is full is lost.

### Resource connections

A **resource connection** is a solid arrow that moves resources from one node to another. Its label is the **flow rate**, the number of resources it tries to move each time it fires. An unlabelled connection moves one. A label can also be random, for example a die roll, or a fraction that fires only part of the time.

### Sources and drains

A **source** creates resources from nothing. It is drawn as a triangle pointing up. A **drain** destroys resources. It is drawn as a triangle pointing down. In economic language, sources are **faucets** and drains are **sinks**, terms you will meet in week 7 and throughout MMO304.

With four elements you can already draw a surprising amount. A source feeding a pool is income. A pool feeding a drain is spending or decay. A source feeding a pool feeding a drain is a flow-through system, and the pool's level over time tells you whether income or spending is winning.

### The conservation check

Every diagram built from these elements obeys one bookkeeping rule. For any pool, over any stretch of time:

```
start + arrived = end + left + lost
```

where "lost" counts resources that arrived at a full pool and were discarded. For a whole diagram, "arrived" is everything the sources created and "left" is everything the drains destroyed. If your spreadsheet or simulation breaks this rule, it has a bug. Check it every time. It costs one line and catches most mistakes.

## 3. Worked example: the capped pool and the price of waiting

### The hook

Three games handle a spending resource in three ways that players feel immediately.

In **Hearthstone**, you gain one permanent mana crystal at the start of each of your turns, up to 10, and your crystals refill at the start of every turn. Mana you do not spend is simply gone, because it refills next turn anyway. A turn that ends with crystals unspent has thrown those crystals away.

In **Slay the Spire**, every character gains 3 energy at the start of each turn. Energy normally resets rather than carrying over. The Ice Cream relic changes exactly that rule, so that energy is conserved between turns. It is a single-line change to the system, and it changes how the whole deck is played.

In **Clash Royale**, elixir is generated continuously during the battle, up to a maximum of 10. Battles last up to three minutes of normal time, and elixir generation doubles during the final minute. When your elixir bar is full, the elixir that would have arrived is lost, so every second you spend at 10 while deciding what to play costs you.

Each of these is the same small machine. A source fills a pool that has a limit, and the player decides when to empty it. The question this worked example answers is exactly how much waiting costs, and why.

### One model, stated once

```
source ──r──▶ pool (capacity C) ──c──▶ drain
```

- The **source** is automatic. It produces `r` resources per second.
- The **pool** holds the player's current amount `p`, starting at `p_0`, with capacity `C`.
- The **drain** is interactive. It fires when the player plays a card, removing the card's cost `c`.

While the pool is below `C`, it rises at `r` per second. While it sits at `C`, everything the source makes is lost. So:

```
waste = r × (seconds spent at capacity)
```

and the conservation check becomes

```
p_0 + r × T = p_T + spent + waste
```

for a stretch of `T` seconds.

### Numbers you can check

We use the course's practice card battler, *Lanes*, a fictional game with round numbers. The numbers below are ours, not Clash Royale's. Elixir starts at `p_0 = 5`, the source makes `r = 0.5` per second, capacity is `C = 10`, and a match lasts 180 seconds.

**Table 1. Doing nothing for 20 seconds.**

| Time (s) | Generated | Pool | Wasted | Check `5 + generated = pool + wasted` |
|---|---|---|---|---|
| 0 | 0 | 5 | 0 | 5 = 5 |
| 5 | 2.5 | 7.5 | 0 | 7.5 = 7.5 |
| 10 | 5 | 10 | 0 | 10 = 10 |
| 15 | 7.5 | 10 | 2.5 | 12.5 = 12.5 |
| 20 | 10 | 10 | 5 | 15 = 15 |

The pool hits the cap at 10 seconds. After that, every 5 seconds of waiting throws away 2.5 elixir, which is `0.5 × 5`. Nothing about the waste depends on how you got to the cap. Only the time spent there matters.

**Table 2. A player who waits at the cap before each play.** Now the player plays a 4-cost card each time the pool is full, but first *holds* at the cap for `H` seconds (waiting to see what the opponent does). After each play the pool is at 6, and it takes `4 / 0.5 = 8` seconds to refill to 10. So one cycle takes `8 + H` seconds and wastes `0.5 × H` elixir.

| Hold `H` | First play at | Cycle length | Cards played in 180 s | Wasted | Pool at 180 s | Check `5 + 90 = spent + wasted + pool` |
|---|---|---|---|---|---|---|
| 0 s | 10 s | 8 s | 22 | 0 | 7 | 88 + 0 + 7 = 95 |
| 2 s | 12 s | 10 s | 17 | 17 | 10 | 68 + 17 + 10 = 95 |
| 4 s | 14 s | 12 s | 14 | 29 | 10 | 56 + 29 + 10 = 95 |

Work out the `H = 2` row yourself. Plays happen at 12, 22, 32, and so on, every 10 seconds. The last one that fits is at 172 seconds, which is play number `(172 − 12) / 10 + 1 = 17`. Each play wasted 1 elixir during its hold, so 17 are wasted. After the play at 172 the pool is at 6 and it reaches 10 exactly at 180.

For `H = 4`, check the waste with the rule rather than by counting cycles. There are 14 holds of 4 seconds each, plus 2 more seconds at the cap at the very end (the pool refills at 178), for 58 seconds at capacity. `0.5 × 58 = 29`.

A two-second habit of waiting at full cost the player 5 cards out of 22 over a match, almost a quarter of their plays. If the rate doubles in the final minute, as Clash Royale's does, the same habit costs twice as much per second in that minute. With `H = 2` and double rate from 120 seconds on, the player makes 21 plays and wastes 31, against 29 plays and zero waste for a player who never holds.

### A visual you can move

Open `examples/w05-capped-pool.html`. The top half is the Machinations diagram itself: a source, a pool drawn as a circle with a capacity ring, and a drain. Tokens move along the arrows as the match plays. The bottom half is a timeline of the pool level, shaded wherever the pool sits at capacity, with running totals for generated, spent, wasted and the conservation check.

Move the **hold** slider from 0 to 4 and watch the shaded bands appear. The diagram looks identical in every setting. The timeline shows the cost. Then move the **capacity** slider up. A bigger pool does not reduce waste for a player who always waits until it is full, because they simply wait longer to fill it. It only helps a player who spends before the cap. The capacity is not a limit on how much you can own. It is a limit on how long you can wait without paying for it.

### Cross-game recognition

Draw each of these in the same four elements.

**Hearthstone (current rules).** Source, automatic, fires once at the start of your turn and fills the mana pool up to your crystal count. Pool capacity equals your crystal count, which itself grows by one per turn to a maximum of 10. Drain, interactive, playing cards. A second drain, automatic, fires at the end of your turn and empties the pool. That end-of-turn drain is the whole design. It makes waste certain for any mana you do not spend this turn, which is the same as a capacity problem where the "hold time" is a full turn.

**Slay the Spire.** Source, automatic, 3 energy at the start of your turn. Interactive drain, playing cards. Automatic end-of-turn drain, which empties the pool. The Ice Cream relic removes that end-of-turn drain. Delete one node and the resource changes character, from "use it this turn" to "save it for a big turn".

**Clash Royale.** Source, automatic, continuous. Pool capacity 10. Interactive drain, deploying cards. The doubling in the final minute is a rate change on the source's connection, triggered by the clock. In Machinations that change is a state connection, which section 5 introduces.

Three games, one diagram, and the differences between them are one node or one label each.

### Eyes-open design judgment

The capped pool is one of the most common structures in game design, and each choice in it has a cost.

- **Low cap or end-of-turn drain.** This forces tempo. Players must act now, and holding back is always punished. It makes decisions frequent and small. It also means a player who is behind cannot save up for a big comeback turn.
- **High cap or carry-over.** This rewards planning and allows big turns. It also allows a player to sit on resources indefinitely, which can slow a game down and make it hard to read.
- **Automatic source with a fixed rate.** Both players get equal income, so skill shows up in *spending* well. If you add income-boosting cards, you add a reinforcing loop (week 3), and you should expect snowballing.
- **Rate changes over time.** Doubling the rate late in a match compresses the end and raises the stakes of waiting. It also doubles the penalty for every hesitation, which is exactly what makes the final minute tense.

Decide on purpose whether waiting should be a choice with a cost (a cap), a mistake (an end-of-turn drain), or free (unlimited carry-over). Most players never notice the choice. They notice how the game feels because of it.

## 4. Activation modes, pull and push

Every node in Machinations has an **activation mode** that says when it fires:

- **Passive.** The node does nothing on its own. It only acts when another node pulls from it or pushes into it, or when something triggers it. This is the default for pools.
- **Interactive.** The player fires it by clicking. Drawn with a double outline. The card-play drain in the worked example is interactive.
- **Automatic.** The node fires every time step, on its own. Drawn with a star. The elixir source is automatic.
- **Starting action.** The node fires once, at the start of the run. Drawn with the letter `s`. Handy for dealing a starting hand.

Nodes also decide which direction they work in:

- **Pull** (the default). When a node fires, it tries to pull resources along its *incoming* connections. A drain pulls from the pool it is connected to.
- **Push** (drawn with the letter `p`). When a node fires, it pushes resources along its *outgoing* connections. A source always pushes, since it has nothing to pull from.
- **All or nothing** (drawn with `&`). A pulling node with this mark only takes resources if every incoming connection can deliver its full amount. Otherwise it takes nothing. Without the mark, a node takes whatever it can get.

The all-or-nothing rule matters more than it looks. Consider the card-play drain with cost 4 when the pool holds 3. With all-or-nothing, the play fails and the pool keeps its 3. Without it, the drain takes 3, the card is not paid for, and your model is wrong. Buying anything with a price should be all-or-nothing.

Time also has modes. In **synchronous** time every automatic node fires on each step at once. In **turn-based** time the diagram advances only when a player spends their actions for the turn. Real-time games like Clash Royale are closest to synchronous time. Hearthstone and Slay the Spire are turn-based.

## 5. State connections: drawing the feedback

So far every arrow moves resources. A **state connection**, drawn as a dotted arrow, moves nothing. It carries information. It says "the number in this pool changes the behaviour of that other element".

The simplest kind is a **label modifier**. A dotted arrow from a pool to a resource connection, labelled `+1`, means "each resource in this pool adds 1 to that connection's flow rate". Labelled `−1`, each resource subtracts 1.

Now you can draw the loops from weeks 3 and 4 so that they run.

**Week 3's worker loop.** An automatic source feeds a Gold pool. An interactive converter-like step (for now, a drain from Gold plus a source into Workers, fired together) buys workers. A dotted arrow from the Workers pool to the source's output connection, labelled `+1`, means each worker adds one gold per step. Follow the loop: more workers, more gold per step, more workers bought. One `+` on the state connection and one `+` from buying, no minus signs, reinforcing.

**Week 4's catch-up loop.** Put the gap into a pool called Lead. A source adds `d` to Lead every step. An automatic drain removes from Lead, and a dotted arrow from Lead to that drain's connection, labelled with a fraction `+k`, makes the drain rate grow with the lead. More lead, more drained, less lead. One `−` in the loop, balancing. Run it and the Lead pool settles at `d / k`, exactly as the recurrence predicted.

This is why Machinations is worth learning. The same diagram that shows the loop's sign also computes its behaviour. Week 6 adds the remaining state connections, triggers and activators, along with converters, traders and gates.

## 6. Reading a diagram in five questions

When someone hands you a Machinations diagram, ask these in order:

1. **What are the resources?** List the colours or pool names.
2. **Where do they enter and leave?** Find every source and drain. A diagram with sources and no drains inflates without limit.
3. **Who acts, and when?** Mark each node's activation mode. Interactive nodes are the player's decisions. Everything else happens to them.
4. **What changes the rates?** Follow every dotted arrow. Each closed path of arrows through a state connection is a feedback loop. Count its signs.
5. **What does it do when run?** Predict first, then press play. If the prediction was wrong, find out which question you answered wrongly.

## In-class activity (25 minutes)

Work in groups of three with paper and one laptop open on machinations.io.

1. **Draw.** Each person draws one of the three games from section 3 on paper using the four elements plus activation-mode marks. Five minutes, no talking.
2. **Compare.** Put the three drawings side by side and circle the one node or label that differs between each pair. Five minutes.
3. **Build.** Build the *Lanes* capped pool in the tool: automatic source with rate 1 per step (treat one step as 2 seconds), pool with capacity 10 starting at 5, and an interactive drain of 4 with all-or-nothing pulling. Ten minutes.
4. **Test the rule.** Run it for 30 steps, clicking the drain only when the pool is full and after waiting one step. Record how much was wasted and check it against `waste = rate × time at cap`. Five minutes.

Expected output: three annotated paper diagrams, a screenshot of the working model, and one line showing the conservation check.

## Common misconceptions

- **"A bigger capacity means less waste."** Only for players who spend before they hit the cap. A player who waits until full wastes `r × H` per hold at any capacity. Capacity changes how long you can delay without cost, not the cost of each second of delay.
- **"Arrows in Machinations mean 'affects'."** Solid arrows move resources. Dotted arrows carry information about quantities. Mixing them up produces diagrams that cannot run.
- **"Pools and sources are the same thing, since both hold resources."** A source creates resources and holds none. A pool holds resources and creates none. Income always needs a source somewhere.
- **"A drain is always bad for the player."** Drains are how prices, decay and upkeep work. Removing a drain, as Slay the Spire's Ice Cream does, is a design change, not a gift of free resources.

## Check yourself

1. A pool with capacity 8 starts at 2. An automatic source adds 1.5 per second and the player spends nothing for 10 seconds. When does the pool hit capacity, how much is wasted, and does the conservation check hold?
2. In *Lanes*, a player plays a 3-cost card every time the pool is full after holding 1 second. With `r = 0.5` and `C = 10`, how long is one cycle and what fraction of all generated elixir is wasted over a long match?
3. Draw a Machinations diagram for a shooter where ammunition regenerates at 2 rounds per second up to 30, and firing uses 1 round per shot. Which node is interactive, which is automatic, and which should pull all-or-nothing?
4. A designer adds a card: "Each card you play this turn adds 1 mana to your next turn." Which element and which kind of connection do you add to the Hearthstone diagram, and what is the sign of the loop it creates?

<details>
<summary>Answers</summary>

1. It needs 6 more, at 1.5 per second, so it hits capacity at 4 seconds. It then sits at the cap for 6 seconds, wasting `1.5 × 6 = 9`. Check: `2 + 1.5 × 10 = 17`, and `pool + wasted = 8 + 9 = 17`. It holds.
2. After a play the pool is at 7 and refills in `3 / 0.5 = 6` seconds, then holds 1 second, so a cycle is 7 seconds. Generated per cycle is `0.5 × 7 = 3.5`, of which `0.5 × 1 = 0.5` is wasted, so `0.5 / 3.5 ≈ 14%` of all income is wasted.
3. Automatic source, rate 2 per second, into an Ammo pool with capacity 30. An interactive drain, rate 1, fired by the trigger, pulling all-or-nothing so an empty magazine cannot fire a partial round. The source is automatic, the drain is interactive.
4. Add a pool for "next turn bonus" that gains 1 each time a card is played (the play drain and this new source fire together; week 6 draws that link as a trigger), and a state connection (label modifier, `+1`) from that pool to the mana refill connection at the start of the next turn. More cards played means more mana next turn, which means more cards played. No minus signs, so it is a reinforcing loop.

</details>

## Lab hook

**Lab 05, three spending machines** ([labs/lab05.md](../labs/lab05.md)). You build the capped pool, the turn-reset pool and the carry-over pool in Machinations, run each against two spending policies, and compare waste and cards played in a one-page report. It is the first of the Machinations models that make up 30% of the course grade.

## Sources

- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 4, internal economy; chapter 5, the Machinations language (pools, sources, drains, resource and state connections, activation modes, pull and push, time modes). Element names and behaviour in this lecture follow the book.
- Dormans, J. (2012). *Engineering Emergence: Applied Theory for Game Design*. PhD thesis, University of Amsterdam (ILLC DS-2012-12, CC BY-NC). Chapter 4 defines the notation the book uses: pools as open circles, interactive nodes with a double outline, automatic nodes marked `*`, starting action marked `s`, push mode marked `p`, all-or-none marked `&`, sources and drains as up and down triangles, state connections as dotted arrows.
- Machinations.io documentation, "Trigger Modes" and "Pulling & Pushing Resources" (accessed September 2026). The tool's four trigger modes are passive, interactive, automatic and enabling; enabling was formerly called "on start". Its symbols differ in places from the book.
- Hearthstone Wiki (hearthstone.wiki.gg), "Mana" (current rules, accessed September 2026). One permanent crystal gained at the start of each turn up to 10, crystals refilled at the start of each turn, unspent mana wasted.
- Slay the Spire Wiki (slaythespire.wiki.gg), "Keywords" (Energy entry) and "Ice Cream" (original game, 2019 release version, accessed September 2026). Every character gains 3 energy at the start of their turn; energy normally resets at the start of each turn; Ice Cream makes energy conserved between turns.
- Wikipedia, "Clash Royale" (accessed 2026). Elixir generates passively up to a maximum of 10; battles last up to three minutes of normal time with elixir generation doubled in the final minute. The exact per-second rate was not verified for this lecture, so the numbers in the worked example use the fictional game *Lanes*.

## Interactive spec: examples/w05-capped-pool.html

**The one insight.** Waste in a capped pool equals rate times time spent at capacity. The diagram looks the same whatever the player does; only the timeline, shaded where the pool is full, shows what hesitation costs.

**Layout.** Top panel, a live Machinations diagram (source triangle pointing up with a star for automatic, pool circle with capacity ring and numeric level, drain triangle pointing down with a double outline for interactive). Bottom panel, a timeline. Stack vertically on all widths; cap the diagram's height at 40% of the viewport on mobile.

**Controls.**
- `rate r`, 0.25 to 2 per second, step 0.25, default 0.5.
- `capacity C`, 4 to 20, step 1, default 10.
- `start p0`, 0 to C, step 1, default 5.
- `card cost c`, 1 to 8, step 1, default 4. If `c > C`, show a warning that no card can ever be played.
- `hold H`, 0 to 10 seconds, step 0.5, default 2.
- Checkbox `double rate in final minute`, default off.
- Play / pause and a "Jump to end" button. With `prefers-reduced-motion`, tokens do not animate and the timeline draws instantly.
- A "Manual" toggle: when on, the automatic policy stops and a "Play card" button (also the Space key) fires the drain, so students can feel the timing themselves.

**Model.** Match length `T = 180` s, simulated in steps of `dt = 0.01` s. At each step: `rate = r`, doubled when the checkbox is on and `t ≥ 120`. Add `rate × dt` to the pool; any amount above `C` goes to `wasted`. Track `held`, time continuously at `C`. Automatic policy: when the pool is at `C` and `held ≥ H`, remove `c` (all-or-nothing, only if `pool ≥ c`), add `c` to `spent`, increment `plays`, reset `held` to 0. Use a small epsilon (1e-9) in comparisons.

**Timeline panel.** x axis 0 to 180 s, y axis 0 to `C`. Pool level as a line. Every interval at capacity shaded in the warning colour. If doubling is on, shade the final minute's background lightly and label it "double rate". Beneath, a numeric row: generated, spent, wasted, pool, plays, seconds at cap, and the check `p0 + generated = pool + spent + wasted` shown as two numbers and a tick when they agree to 0.01.

**Test values** (`r = 0.5, C = 10, p0 = 5, c = 4`):

| `H` | double | plays | spent | wasted | pool at 180 s |
|---|---|---|---|---|---|
| 0 | off | 22 | 88 | 0 | 7 |
| 2 | off | 17 | 68 | 17 | 10 |
| 4 | off | 14 | 56 | 29 | 10 |
| 0 | on | 29 | 116 | 0 | 9 |
| 2 | on | 21 | 84 | 31 | 10 |

With no plays at all (set `c` to 8 and `H` to 10, then compare to Table 1 over the first 20 s): the pool reaches 10 at 10 s and 5 has been wasted by 20 s.

**Style.** Shared palette from `templates/interactive-tokens.css`. No game names, logos or art in the diagram; the caption may mention that mana, energy and elixir systems share this structure.
