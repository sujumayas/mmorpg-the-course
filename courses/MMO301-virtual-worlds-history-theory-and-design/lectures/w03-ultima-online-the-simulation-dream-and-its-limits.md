# MMO301 · Week 03 — Ultima Online: The Simulation Dream and Its Limits

**Why this matters:** Ultima Online (1997) tried to build a world that ran itself, with a resource cycle, an ecology and shopkeepers who reasoned about profit. Players broke most of it within a year, not by cheating but by playing. The way it broke is the most reused lesson in MMO design, and if you can reproduce it with a few numbers, you will recognize it early in your own designs instead of in your launch post-mortem.

**You will be able to:**
- Describe the simulation systems Ultima Online planned (closed resource cycle, ecology, NPC shopkeepers, open player killing) and what happened to each, with sources.
- Compute the steady-state supply of a closed resource loop and show why it is set by how fast players give things back, not by how many resources the designers put in.
- Compare the closed loop with the faucet/drain design that replaced it and quantify what the replacement costs in stored items.
- Explain the ecology failure as a rate problem, and critique the general claim that "players are the biggest force in any simulated world."

**Before class:** Simpson, Z. B., "The In-game Economics of Ultima Online" (Computer Game Developers' Conference, March 2000; paper dated April 1999), chapters 4 and 5. It is short and readable. Bartle, *Designing Virtual Worlds* (2003), chapter 4, "Closed or Open Economic Model?" (pp. 352-355), and chapter 6, the pages summarizing Simpson (pp. 750-754). Koster, "Laws of Online World Design," the entry on why online game economies are hard.

**Prerequisites from earlier courses:** [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) gives Ultima Online's history, launch, growth and the Trammel split; read its section 3 first. [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) and [GD102 week 7, internal economies](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md) give you the stocks, sources and drains this lecture uses. If you are taking MMO304 this semester, its [week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) covers money flows in depth and [week 5, deflation and hoarding](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w05-deflation-and-hoarding.md) covers who holds the stock. Within this course, [week 1](w01-what-is-a-virtual-world-bartles-definition.md) (physics and the persistence ladder) and [week 2](w02-mud1-muds-moos-and-the-text-era.md) (stocks of content).

**Interactive:** [w03-closed-resource-loop.html](../examples/w03-closed-resource-loop.html). Keep it open during section 2.

---

## 1. The dream: a world that runs itself

GS101 week 9 introduced Ultima Online as Origin Systems' 1997 attempt to put the Ultima series online, with Richard Garriott behind the vision and Raph Koster as lead designer. It launched on 24 September 1997. This week looks inside its design.

On week 1's dials, Ultima Online turned physics up as far as the hardware of 1997 allowed. Bartle places it at level 4 of his persistence ladder, the entire world state survives a restart. Players could build houses in the open world, own them, and fill them with things. Four systems show the ambition.

**A closed resource cycle.** Zachary Booth Simpson, an Origin research fellow, described the design in his paper on the game's economy. Every object was made of basic resources. A sword might hold two units of metal. When the sword broke or decayed, the metal went back into a central store, which Simpson calls the resource bank. The bank then supplied new ore to mines, new monsters with their loot, and new goods for shopkeepers to sell. Nothing was created from nothing. The designers' aim was to prevent inflation, which had plagued earlier online worlds, by keeping a fixed total of resources circulating.

**An ecology.** The game was meant to include an artificial-life system in which ecological events would change animal behavior and open new adventures without scripting. Predators would need prey. Populations would rise and fall.

**Thinking shopkeepers.** Non-player shopkeepers ran a supply-and-demand simulation, tracking inventory, sales and cash, and set prices to keep a profit. They could make goods from the resource bank and buy goods from players.

**Freedom to be a villain.** Players could attack and kill each other in the open world. Koster defended this in terms of meaning. In paraphrase, a world where you are safe from evil is a world where you cannot be a hero.

Every one of these systems is a model of how the world should behave if its inhabitants behave like the designers expected. The next two sections show what happened when they did not.

## 2. Worked example: the resource bank that ran dry

### The hook

Simpson's paper says what happened, plainly. Resources piled up in players' possession. Little flowed back to the bank. As the bank dried up, there were no resources left to spawn creatures and their loot, and the world became boring. The designers first tried adding more resources to the bank. However much they added, it flowed into players' houses and stayed there. Within about a year of launch, Bartle notes, the closed cycle had been replaced by a faucet/drain design.

A favorite story among the designers, according to Simpson, was a character with over ten thousand identical shirts in his house.

Why did adding resources not fix it? And why would any fixed amount have failed?

### The model

Split the world's resources into three stocks:

- `B`, the **bank**: resources not in any object, waiting to be spawned.
- `W`, the **world**: spawned but unclaimed, such as ore in a vein or a monster carrying loot.
- `H`, **held**: in players' packs, banks and houses.

In the closed design the total `R = B + W + H` never changes. Each day:

```
spawn    s = min(σ, B)          the world spawns from the bank, at most σ per day
harvest  h = min(W, c × N)      N players each take up to c per day
return   r = d × H              a share d of held stock goes back to the bank
```

- `σ` (sigma) is the spawn capacity, the most the world can spawn per day.
- `c × N` is demand, what players would take if it were there.
- `d` is the **return rate**, the share of held items that breaks, decays, is consumed, or is sold to a shopkeeper who destroys it, per day. It is the only path back to the bank.

Now find the steady state. Once the bank is the bottleneck, it spawns everything it has each day, `s = B`. Players harvest all of it, so `W ≈ 0`. Everything the bank gets back tomorrow is today's return, `d × H`. Put `B + H = R` into that and the loop settles at

```
supply per day  s* = d × R          (when d × R < σ and d × R < c × N)
held at day's end H* = (1 − d) × R
```

That is the whole lesson. **In a closed loop, supply is the return rate times the total.** The designers control `R`. The players control `d`. And players who hoard, decorate, speculate, or simply never throw anything away push `d` toward zero.

### Numbers you can check

Take one shard with `R = 200,000` resource units, spawn capacity `σ = 6,000` per day, and `N = 1,500` active players who each want `c = 4` units a day, so demand is 6,000 a day. These numbers are invented. The mechanism is Simpson's.

**Supply depends on the return rate:**

| Return rate `d` per day | Steady supply `s*` | Share of demand met | Held by players at day's end |
|---|---|---|---|
| 0.005 (0.5%) | 1,000 | 17% | 199,000 (99.5%) |
| 0.01 (1%) | 2,000 | 33% | 198,000 (99%) |
| 0.02 (2%) | 4,000 | 67% | 196,000 (98%) |
| 0.03 (3%) | 6,000 | 100% | 194,000 (97%) |
| 0.05 (5%) | 6,000 (capped by `σ`) | 100% | 114,000 (57%) |

At `d = 0.005` the average item stays in a player's hands for about `1/d = 200` days. The world gets back 1,000 units a day and can spawn no more than it gets back.

**How fast it runs dry.** Start with everything in the bank (`B = R`) at `d = 0.005`, and simulate day by day:

| Day | Bank `B` | Held `H` | Spawned that day |
|---|---|---|---|
| 1 | 194,030 | 5,970 | 6,000 |
| 10 | 141,625 | 58,375 | 6,000 |
| 20 | 86,105 | 113,895 | 6,000 |
| 30 | 33,299 | 166,701 | 6,000 |
| 36 | 2,862 | 197,138 | 6,000 |
| 37 | 1,000 | 199,000 | 2,862 |
| 38 onward | 1,000 | 199,000 | 1,000 |

For five weeks the world looks healthy. Every player gets everything they want. Then in two days supply falls by 83% and stays there. Nothing in the first month's numbers warns you, unless you are watching `H`.

With fewer players the collapse comes later but lands in the same place. At `N = 500` (demand 2,000 a day), supply first drops below half of demand on day 140, and the steady supply is still 1,000. Growth makes it worse. Ultima Online grew to about 100,000 subscribers by December 1998 (GS101 week 9), so demand kept rising against a supply that could not.

**Adding resources.** Now do what Origin's designers did first. Keep `d = 0.005` and raise `R`:

| Total `R` | Steady supply | Held by players | Day supply first falls below half of demand |
|---|---|---|---|
| 200,000 | 1,000 | 199,000 | 37 |
| 400,000 | 2,000 | 398,000 | 82 |
| 1,200,000 | 6,000 | 1,194,000 | never |

Doubling the bank doubles supply and delays the collapse by six weeks, and 99.5% of what you added ends up in players' houses. To meet demand at this return rate you need `R = c × N / d = 1,200,000`, six times the original world, almost all of it sitting in storage. That is Simpson's "no matter how much they added."

### The replacement: faucet and drain

The fix Origin adopted cuts the loop. Resources are spawned from nothing at a steady rate (the **faucet**) and whatever breaks or decays is destroyed (the **drain**). In the model, step 1 becomes `s = σ` with no bank, and returns vanish instead of refilling anything. Supply is now 6,000 a day no matter what players hoard.

But look at what players are holding:

```
H* (end of day) = σ × (1 − d) / d
```

| Return rate `d` | Held after 30 days | After 365 days | Steady state |
|---|---|---|---|
| 0.005 | 166,701 | 1,002,385 | 1,194,000 |
| 0.02 | — | 293,816 | 294,000 |

The faucet world ends up storing the same 1.2 million units the closed world would have needed. The problem did not go away. It moved from "the world is empty" to "the database is full." Simpson says exactly this. The faucet solved the shortage but not the server load, because hoards kept growing, and the ten thousand shirts had to be stored somewhere. Bartle's summary adds the ending. The faucet/drain economy held up for a long time, but what finally broke it was a lack of sinks. People had too little to spend on, so wealth piled up.

### The visual

Open the interactive. The left view is a stacked area chart of `B`, `W` and `H` over 365 days. In closed mode you watch the bank's band shrink to a sliver around day 37 while the held band swallows the chart. The right view plots spawn per day against the demand line. In closed mode it drops off a cliff. Flip to faucet mode and the right chart becomes a flat line at demand, while the left chart's held band grows without a ceiling in sight. The two views disagree on purpose. One looks healthy exactly when the other looks broken. Drag `R` up in closed mode and watch the cliff move right without disappearing. Drag `d` up and watch it disappear.

### Cross-game recognition

**MUD1 (1978 onward), a closed pool with a hard reset.** GS101 week 5 showed MUD1's treasure. The world holds a fixed amount, players carry it off to score, and when most is gone the game resets and everything returns. In this model, a reset sets `d = 1` for one moment. It returns every held unit to the bank at once. That works in a world whose sessions are short and whose score is kept separately from the items. It is impossible in a world like Ultima Online's, where a reset would mean taking back every sword and shirt in every house.

**Shattered World, a closed economy that worked.** Bartle cites Geoff Wong's account of the text world Shattered World, whose money supply stayed stable from the early 1990s under a strict policy for how much the banks could lend. Every manufacturer, shop and bank was owned by a player, and players set every price. In model terms, `d` stayed high because money had to keep moving through player institutions. The cost Bartle names is new players. They could not be handed starting money, so they had to borrow or work for others. That is tolerable in a small world and fatal for one taking in thousands of newcomers a week.

**EverQuest and Asheron's Call, open from the start.** Bartle describes both as having much simpler economies than Ultima Online, open designs that suffered inflation. EverQuest's flood of new players soaked up some of the excess. Asheron's Call, helped by money-duplication bugs, went into hyperinflation and never recovered. They avoided Ultima Online's shortage by accepting the opposite problem.

**Guild Wars 2 (2012 onward), a faucet per player.** GS101 week 5 notes that most Guild Wars 2 gathering nodes can be harvested by each character separately and reset for that character hours later. There is no shared bank at all. `σ` is per player, so no hoard anywhere can starve anyone else's supply. The cost is that gathering can never be scarce enough to be worth fighting over.

Four worlds, one loop. Close it, and players' hoarding sets your supply. Open it, and your drains decide your storage and your prices.

### Eyes-open design judgment

- **The closed loop is a bet on `d`.** Its appeal is real. Bartle lists no inflation, prices set by markets, and economy-driven play, and he admits the deeper reason is that a closed economy is simply neater. But it only works if players give things back at a predictable rate. Players give things back when they must, so a closed loop needs consumption built into play (arrows, food, reagents, repairs) from the first day.
- **Drains must launch with the game.** Simpson's most repeated lesson is political. Players accept drains that were there from the start and fight drains added later, because a new drain feels like the designers taking things away. Taxes, housing upkeep and faster decay were all proposed for Ultima Online and all ran into this. Bartle makes the same point. Design your drains before launch, even if you set them low.
- **Watch the held stock, not the spawn rate.** In the table, every early number was healthy except `H`. Simpson's closing research agenda asked for exactly this telemetry: inflow, outflow, stock held in houses and vendors, and database size. It is the ancestor of the economy dashboards in MMO304.
- **Faucet/drain moves the problem, it does not solve it.** You trade a visible shortage for invisible growth in stored items and money. That is usually the right trade, because players forgive inflation more than an empty world, and servers can grow. But decide it knowingly, and size storage for `σ(1 − d)/d`, not for launch.
- **Some hoarding is play.** Simpson lists reasons players hoard: decoration, laziness, speculation, "I might need this," mementos, status and self-set goals. Several are exactly the attachment you want players to feel. A design that simply punishes holding things will punish its most invested players. Better drains give players something they want in exchange, such as consumables, services or cosmetic purchases.

### Check yourself (worked example)

1. A closed world has `R = 500,000`, `σ = 20,000`, and players return 1% of what they hold each day. Demand is 15,000 a day. What is the steady supply, and what share of demand does it meet?
2. In that world, what return rate `d` would meet demand? What total `R` would meet demand at `d = 0.01`?
3. The same world switches to a faucet of 15,000 a day with `d = 0.01`. How many units do players hold at steady state? Compare with your answer to question 2.

<details>
<summary>Answers</summary>

1. `s* = d × R = 0.01 × 500,000 = 5,000` a day (below `σ` and below demand), so 33% of demand.
2. `d = 15,000 / 500,000 = 0.03`, 3% per day. Or `R = 15,000 / 0.01 = 1,500,000`.
3. `H* = 15,000 × 0.99 / 0.01 = 1,485,000`. About the same as the 1.5 million the closed world would need. The faucet does not shrink the hoard; it stops the hoard from starving everyone else.

</details>

## 3. The ecology that never began

The resource bank failed over months. The ecology failed before launch. Garriott, interviewed in 2011, described it this way, in paraphrase. The team thought the system was fantastic and had spent a great deal of effort on it. Then players went in and killed everything, so fast that the game could not spawn creatures quickly enough for the simulation even to begin. Bartle lists it among Ultima Online's principal problems. The detailed ecological model broke down when players rapidly killed everything that moved. It never went beyond beta.

This is a rate problem, and it has the same shape as week 1's density model. Suppose a forest holds `A` animals and `P` players hunt there, each killing `k` animals per hour. If kills fall evenly, each animal is killed at a rate `μ = P × k / A` per hour, and the chance a given animal survives `T` hours is `e^(−μT)`.

Take illustrative numbers. `A = 400` deer, `P = 200` hunters, `k = 6` kills per hour each. Then `μ = 3` per hour and the average deer lives 20 minutes. Suppose the ecology needs a wolf to go two hours without food before it starts hunting deer near a town, which is the kind of event that makes an "organic" adventure. The chance a given animal lasts two hours is `e^(−6) ≈ 0.25%`. The wolves are dead long before they get hungry. As Garriott said, the simulation never begins.

The general lesson is about time scales. A simulated behavior shows only if the thing simulated lives longer than the behavior takes to appear. Players set the lifespan of anything they can kill, harvest or buy. In a busy world that lifespan is minutes. So:

- Put slow simulations where players cannot reach them (off-map populations that feed spawns), or
- Make the simulated thing hard to kill, or valuable alive, or
- Run the simulation on the player population itself, which is the one population that lives long enough. Week 6's EVE Online case is largely this idea.

## 4. The other simulation: people

The ecology and the bank simulated animals and ore. The biggest simulation in Ultima Online was social. Letting players kill each other was a bet that player behavior would regulate itself, through reputation and fear of revenge. Bartle lists the failure briefly among the game's main problems. The means of punishing players for attacking others did not work.

GS101 week 9 and [MMO401 week 10](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w10-scarcity-by-design-full-loot-and-destruction.md) cover what followed. With the Renaissance expansion on 4 May 2000, each shard's map was mirrored. Trammel forbade attacking another player without consent. Felucca kept the old rules. Players could choose their society.

Read it with this week's lens. The resource bank failed because designers modeled what players would *return*, and players returned almost nothing. The social system failed because designers modeled what players would *tolerate*, and most players tolerated far less than the design required. In both cases the planned system was sound on paper and wrong about one rate that only players controlled. Week 7 (themepark versus sandbox) takes up whether Trammel was a rescue or a retreat.

### Simpson's lessons, restated

Simpson closes his paper with a list of lessons from Ultima Online's first year. Paraphrased and grouped:

- **Hoarding is rampant**, and a closed loop turns hoarding into shortage.
- **An economy needs liquidity.** Tying new supply to returns froze the supply.
- **Micro beats macro.** The designers built a careful macro cycle and a complicated shopkeeper price simulation, and gave too little thought to how players trade with each other. Player vendors arrived only about six months after launch and changed the economy at once.
- **Every feature is an economic feature.** Early vendors charged fees based on their stock's resource value, so players priced items impossibly high and used vendors as theft-proof storage.
- **Rewarding production creates overproduction.** Skills rose by use, so crafters made piles of shirts to train, then expected shopkeepers to buy them. Many players reported the refusal as a bug.
- **Bugs outrun fixes.** Simpson calls this Hacker's Law. A gold duplication bug in the early months caused inflation so large that one designer said counterfeiting had destroyed the experiment before anyone could tell whether the original design worked.

That last point deserves respect. The closed cycle was never tested cleanly. What we know is that its structure gave players' hoarding control of supply, and that no amount of added resources fixed it. The model in section 2 shows why that part would have failed even without the bug.

## In-class activity (25 minutes)

In groups of three, you are designing the resource system for a new survival MMO shard of 2,000 players. The producer wants a closed loop "like Ultima Online wanted, but done right."

1. **Set the numbers (8 min).** Choose `R`, `σ`, demand per player `c` and a target return rate `d`. Write down three specific in-game mechanisms that produce your `d` (for example tool breakage per use, food spoilage, a repair cost that destroys material). For each, estimate its share of `d`.
2. **Stress test (8 min).** Your most invested 10% of players will hoard, so their personal `d` is one tenth of everyone else's. Assume they hold half of all held items. Compute the new average `d` and the new steady supply.
3. **Decide (9 min).** Keep the closed loop with changes, or switch to faucet/drain? If faucet/drain, compute the steady held stock `σ(1 − d)/d` and say what drain you ship at launch.

Expected output: a parameter card, the stress-test supply number, and a one-paragraph decision with its cost named. Two groups present; the class votes on which design they would rather play on day 200.

## Common misconceptions

- **"The fix for scarcity is more resources."** In a closed loop, supply is `d × R`. Adding to `R` raises supply in proportion, and nearly all of what you add ends up in hoards. Raising `d` is cheaper and lasts.
- **"Faucet/drain solved Ultima Online's economy."** It solved the shortage. Stored items kept growing, and Bartle notes the economy was finally broken by a lack of sinks.
- **"The ecology failed because the code was bad."** Garriott's account is about rates. Players killed faster than anything could spawn, so the simulated behaviors never had time to appear. Better code at the same rates would fail the same way.
- **"Ultima Online proves closed economies cannot work."** Simpson's own data was spoiled by a duplication bug, and Bartle cites a small text world, Shattered World, whose closed economy stayed stable for years. Closed economies are fragile at scale, not impossible.

## Check yourself

1. Explain in two sentences why, in a closed loop, a player who hoards hurts players they never meet.
2. A closed world with `R = 300,000` has steady supply 1,500 per day. What is `d`? How long does the average item stay in a player's hands?
3. In the ecology model, 50 players hunt a region with 1,000 animals, each killing 4 per hour. What is the average lifespan of an animal, and the chance an animal survives the 3 hours a migration behavior needs to appear?
4. A designer proposes adding a 1% daily tax on items stored in houses, eight months after launch. Using Simpson's lessons, predict the player reaction and propose an alternative with a similar effect on `d`.
5. Why is MUD1's reset not an available fix for Ultima Online? Answer in terms of the persistence ladder from week 1.

<details>
<summary>Answers</summary>

1. Supply for everyone is `d × R`, and `d` is the average return rate across all held items. A hoarder lowers that average, so the bank refills more slowly and every spawn on the shard shrinks, including the ones strangers were waiting for.
2. `d = 1,500 / 300,000 = 0.005`. Average holding time `1/d = 200` days.
3. `μ = 50 × 4 / 1,000 = 0.2` per hour, so the average lifespan is 5 hours. Survival for 3 hours is `e^(−0.6) ≈ 55%`. Here the migration would usually be visible, which shows the model is about ratios. The same system fails with 200 hunters.
4. Players will treat it as taking away what they own, and many will call it unfair. Simpson reports exactly this resistance to proposed taxes and upkeep. An alternative is a consumable that players want and that destroys resources in use, such as house decorations that decay but give a benefit, or crafting upgrades that consume stored materials. It raises `d` while feeling like a purchase.
5. Ultima Online persists the entire world state (level 4), including every player's house and its contents. A reset would destroy things players own and expect to keep. MUD1 persists characters and scores, not the placement of treasure, so it can return everything to the pool without taking anyone's property.

</details>

## Lab / assignment hook

[Lab 03, the closed loop and the faucet](../labs/lab03.md). You build the section 2 model in a spreadsheet or script, reproduce the three tables, stress-test it with a hoarding minority, and design a launch drain package for a faucet version that keeps stored items under a database budget. The analysis is the core of the first case study (40%).

## Sources

- Simpson, Z. B. "The In-game Economics of Ultima Online." Paper dated 7 April 1999, presented at the Computer Game Developers' Conference, San Jose, March 2000. Formerly at mine-control.com/zack/uoecon; read via the Internet Archive copy. The resource bank and closed cycle; natural resources and monster loot; the resource-value shopkeeper simulation; vendors arriving about six months after launch and the storage exploit; overproduction from improve-by-use; the shopkeepers going broke; hoarding, the ten-thousand-shirts anecdote, the failure of adding resources, and the switch to a faucet; counterfeiting and the designer's remark that it destroyed the experiment; "Hacker's Law"; reasons players hoard; lessons learned; proposed telemetry. Paraphrased.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Chapter 1: Ultima Online's principal problems, including ineffective punishment for player attacks, the ecological model breaking down, and the economy collapsing after a bug (p. 30); persistence ladder placing Ultima Online at full world state (pp. 77-78). Chapter 4: closed versus open economies, their benefits and failure modes (pp. 352-355); Ultima Online's economy switching to faucet/drain and later failing for lack of sinks, EverQuest and Asheron's Call inflation (p. 408). Chapter 6: summary of Simpson and Shattered World's closed economy after Geoff Wong, "A Working Mud Economy," *Imaginary Realities* 3(5), May 2000 (pp. 750-754).
- Wikipedia, "Ultima Online" (accessed September 2026). Launch on 24 September 1997; the planned artificial-life ecology and its removal; Garriott's account from "Web Extended Interview, Richard Garriott," *Good Game*, ABC Television (Australia), 1 March 2011; Trent Ward, "Ultima Online Preview," GameSpot, on ecological events affecting animal behavior; Koster's statement on safety from evil versus heroism; Renaissance expansion on 4 May 2000 with Trammel and Felucca.
- Koster, R. "The Laws of Online World Design" (raphkoster.com, accessed September 2026). The faucet-to-drain definition and the warning that without enforced expenditures wealth accumulates without limit.
- GS101 week 5 and its sources (British Legends help pages) for MUD1 resets; GS101 week 5 and the Guild Wars 2 Wiki "Gathering" page for per-character nodes; GS101 week 9 and Wikipedia "Ultima Online" for 100,000 subscribers in December 1998.
- The model parameters (`R`, `σ`, `N`, `c`, `d`) and the forest numbers in section 3 are invented for teaching. The mechanisms are from Simpson, Bartle and Garriott.

## Interactive spec: examples/w03-closed-resource-loop.html

**The one insight:** in a closed resource loop, daily supply settles at `d × R`, the players' return rate times the total. Players, not designers, set `d`, and hoarding drives it toward zero, so the world runs dry after a healthy-looking start no matter how much the designers add. The faucet/drain fix keeps supply at demand but moves the whole problem into an ever-growing held stock.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (stocks chart on top). A mode switch above both: "Closed loop" / "Faucet and drain."

- **Left view, "Where the resources are":** stacked area chart over days 0 to `days` (default 365). Closed mode stacks `B` (bank), `W` (world) and `H` (held) and the stack always sums to `R`; vertical axis 0 to `R`. Faucet mode shows only `W` and `H` (no bank), vertical axis 0 to `max(H) × 1.1`, with a dashed horizontal line at the steady held stock `σ(1 − d)/d` labeled "steady hoard." Use distinct palette colors; label each band directly, not only in a legend.
- **Right view, "Spawned per day":** line chart of `s` per day with a horizontal dashed line at demand `c × N`. Mark the "dry day," the first day `h < 0.5 × c × N`, with a vertical line and label "Dry from day X" (or "Never dry"). In closed mode, add a dotted horizontal line at `min(σ, d × R)` labeled "steady supply."
- **Readouts (copyable):** steady supply `min(σ, d × R, c × N)` (integer), share of demand met (one decimal percent), held at day's end in steady state (`(1 − d) × R` when bank-limited, integer), dry day (integer or "never"), average holding time `1/d` (one decimal days), and in faucet mode steady hoard `σ(1 − d)/d` (integer) and held stock on the last simulated day (integer).

**Controls (keyboard accessible, labeled):**

1. Mode: "Closed loop" / "Faucet and drain", default closed.
2. Total resources `R`: slider 50,000 to 1,500,000, step 50,000, default 200,000 (closed mode only; disabled in faucet mode).
3. Spawn capacity `σ`: slider 1,000 to 20,000 per day, step 500, default 6,000.
4. Players `N`: slider 100 to 5,000, step 100, default 1,500.
5. Demand per player `c`: slider 1 to 10 per day, step 0.5, default 4.
6. Return rate `d`: slider 0.001 to 0.100 per day, step 0.001, default 0.005. Show as a percentage.
7. Days simulated: 90 / 365 / 730, default 365.
8. Button "Designers add resources": in closed mode adds 200,000 to `R` and to `B` on the current day and reruns, so students can watch the added band flow into `H`. (Implement by rerunning the simulation with an injection event at a chosen day, default day 60, set by a small number input.)
9. Reset button.

**Simulation (discrete days, exactly this order).** Start: closed `B = R, W = 0, H = 0`; faucet `W = 0, H = 0`.

```
for each day t = 1..days:
    closed: s = min(σ, B); B = B − s          faucet: s = σ
    W = W + s
    h = min(W, c × N); W = W − h; H = H + h
    r = d × H; H = H − r
    closed: B = B + r                          faucet: r is destroyed
    if injection day == t (closed only): B = B + 200,000; R = R + 200,000
    record B, W, H, s, h, r
dry day = first t with h < 0.5 × c × N
```

**Test values** (closed, `R = 200,000`, `σ = 6,000`, `N = 1,500`, `c = 4`, no injection):

| `d` | Day-365 `B` | Day-365 `H` | Day-365 `s` | Dry day |
|---|---|---|---|---|
| 0.005 | 1,000 | 199,000 | 1,000 | 37 |
| 0.01 | 2,000 | 198,000 | 2,000 | 42 |
| 0.02 | 4,000 | 196,000 | 4,000 | never |
| 0.03 | 6,003 | 193,997 | 6,000 | never |
| 0.05 | 86,000 | 114,000 | 6,000 | never |

(At `d = 0.03`, `d × R` equals `σ` and demand exactly, so the loop approaches 6,000/194,000 slowly and has not fully settled by day 365. With `d = 0.02` supply is 4,000, which is 67% of demand, above the 50% dry threshold, so "never dry" is correct but the share-met readout shows 66.7%.)

Day-by-day at `d = 0.005`: day 1 `B = 194,030, H = 5,970, s = 6,000`; day 10 `B = 141,625, H = 58,375`; day 20 `B = 86,105, H = 113,895`; day 30 `B = 33,299, H = 166,701`; day 36 `B = 2,862, H = 197,138, s = 6,000`; day 37 `B = 1,000, H = 199,000, s = 2,862`; day 38 onward `s = 1,000`.

`d = 0.005`, other defaults: `R = 400,000` gives steady supply 2,000 and dry day 82; `R = 1,200,000` gives steady supply 6,000 and never dry. `N = 500` with `R = 200,000` gives dry day 140 and steady supply 1,000.

Faucet mode, `σ = 6,000`, `N = 1,500`, `c = 4`: `d = 0.005` gives held stock 166,701 on day 30, 433,531 on day 90, 1,002,385 on day 365, 1,163,249 on day 730, steady hoard 1,194,000; supply 6,000 every day, never dry. `d = 0.02` gives 293,816 on day 365, steady hoard 294,000.

**First screen:** closed mode, defaults (`d = 0.005`, 365 days). The left chart shows the bank band collapsing to a thin line by day 37 under a swelling held band; the right chart shows a flat line at 6,000 that falls off a cliff to 1,000 at the dry-day marker. Caption: "The bank ran dry on day 37. Players hold 99.5% of everything, and the world can only spawn what they give back."

**Content rules.** No game art, logos, maps or screenshots. Draw stocks as plain colored bands. Small text under the views: "Mechanism from Simpson (1999) on Ultima Online's first-year economy. All numbers are illustrative."
