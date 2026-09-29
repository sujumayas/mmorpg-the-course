# MMO406 · Week 01 — Setting as System

**Why this matters:** A persistent world has to supply stories for ten years or more, to thousands of players at once, written by writers who have not been hired yet. A setting written as a finished story runs out. A setting built as a set of rules and standing conflicts keeps producing material, and you can measure which kind you have before the first expansion ships.

**You will be able to:**
- Classify the parts of a setting by the job they do: explaining a game system, constraining content, or generating content.
- Compute how many expansions a setting can supply from its stock of plot tensions, its consumption per expansion and its refill from structural tensions.
- Critique the story arcs of shipped MMOs (Guild Wars 2, World of Warcraft, Final Fantasy XIV, EVE Online) as stock being spent or refilled.
- Design a first tension ledger for your own world bible, with at least one structural tension tied to a game system.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), the Introduction and chapter 3, "World Structures and Systems of Relationships." Reread your notes on the content treadmill from MMO306 week 1 and on world concepts from MMO301 week 14.

**Prerequisites from earlier courses:** [MMO306 week 1, the content treadmill](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md) (how fast players consume what you build). [GD102 week 7, sources, drains and converters](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md) (stock-and-flow thinking, which this week applies to story). [MMO301 week 14, designing a world concept](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w14-designing-a-world-concept.md) (the one-page concept your bible grows from). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (why an online world cannot let one player's story change it for everyone).

**Interactive:** [Tension ledger](../examples/w01-tension-ledger.html). Keep it open during section 2.

---

## 1. A setting does three jobs

When students hear "setting," they picture a map, a timeline and a list of gods. Those are the outputs. For an online world, a setting is better described by the work it does. Every fact in your bible does at least one of three jobs, and a fact that does none of them is decoration you can cut.

### Job 1: explain the systems

Every online game has mechanics that would be strange in a real world. Characters come back after dying. They cross a continent in seconds. A sword put in a bank in one city comes out of a bank in another. Ten thousand players each kill the same named boss every week.

The setting can do one of two things with each mechanic. It can **explain** it, so the mechanic becomes a fact of the world with its own consequences. Or it can **tolerate** it, so players accept it as a convention of the genre and the fiction never mentions it. Both are valid. The mistake is to make the choice by accident.

EVE Online is the standard example of explaining. Player characters are capsuleers, pilots whose consciousness can move between cloned bodies. When a pilot's escape pod is destroyed, the pilot wakes in a fresh clone at a chosen home station. Jump clones let a pilot move their mind to a second body far away, which works as fast travel. The explanation then produces rules the game enforces. Items don't travel with the mind, and implants stay in the brain they were installed in, so a jump or a death can cost you the implants in your old head. The lore turned respawn and fast travel into world facts with prices.

Compare the ghost run in World of Warcraft, where a dead character walks back to their corpse as a spirit. The world gives it a look and a place (the spirit healer at the graveyard) but no deeper rule. That is a tolerated mechanic with some dressing, and it works fine. Nobody quits over it.

The deciding question is whether the explanation will create obligations you want. EVE's clone rule obliges every future story to accept that capsuleers are effectively immortal and that ordinary humans are not. That split became central to EVE's fiction. If your explanation would force awkward questions ("if heroes can't die, why does anyone fear the villain?"), tolerate the mechanic instead.

### Job 2: constrain content

A setting also says what can't happen. There is no gunpowder. The dead do not speak. The sea to the west cannot be crossed. Constraints look negative, but they are what let many writers work in parallel. A quest writer in year five does not need to ask the lead whether a character may teleport into a sealed vault, because the bible already says teleportation needs an anchor stone inside the destination.

Good constraints are short, testable and tied to a reason. "Magic is rare" is not testable. "Fewer than one person in a thousand can cast, and each caster is registered with the Collegium" is testable, and it tells a writer what a village looks like.

### Job 3: generate content

The third job is the one this week measures. A setting has to produce new stories for years. The unit of production is the **tension**: an unresolved want that something in the world is blocking. A dragon that wants to eat the world. Two kingdoms that both claim the same river. A guild of healers whose power comes from the same source as the plague.

A tension is not a story yet. A writer turns a tension into content: a quest chain, a zone, a raid, a world event. When that content ships, the tension is either used up or still standing. That difference is the whole model.

## 2. Worked example: the dragon count

### The hook

When Guild Wars 2 launched in August 2012, its setting was built around six Elder Dragons, ancient beings each threatening Tyria. The launch story ended with the death of the first one, Zhaitan. Then the game killed the rest, one arc at a time. Mordremoth died in Heart of Thorns (October 2015). Kralkatorrik fell in the Living World episode War Eternal (May 2019). Jormag and Primordus destroyed each other in the Icebrood Saga's final chapter (April 2021). Soo-Won was defeated in End of Dragons (February 2022).

Six dragons, a little under ten years. By 2022, the villain supply that the setting was built on had been spent. The next expansion, Secrets of the Obscure (August 2023), opened a new arc with new threats.

Was this a failure of planning? Not necessarily. It is a stock running down on a schedule that you could have computed in 2012. That is the point of this section.

### The model

Sort the tensions in a setting into two kinds.

- A **plot tension** is resolved by content. When the story in which the dragon dies ships, that tension is gone. It can be told once.
- A **structural tension** is built into how the world works, usually through a game system. Two factions that players must join, a border that is always contested, a scarce resource everyone needs. One story cannot resolve it. Instead, it keeps producing new plot tensions: a new warlord on the border, a new famine, a new betrayal.

Now track the plot tensions as a stock, the way you tracked gold in GD102 week 7.

```
P(t+1) = P(t) − c + R        where R = g × S
```

- `P(t)` is the stock of unresolved plot tensions at the start of expansion `t`. `P(0)` is what the bible holds at launch.
- `c` is how many plot tensions one expansion consumes (its main arc plus side arcs that end).
- `S` is the number of structural tensions.
- `g` is how many new plot tensions each structural tension spawns per expansion, on average.
- `R = g × S` is the refill per expansion.

An expansion can ship with a full story only if the stock covers it: `P(t) ≥ c`. If consumption beats refill (`c > R`), the stock drains by `d = c − R` each expansion, and the number of full expansions the setting can supply is

```
N = floor((P(0) − c) / d) + 1        when P(0) ≥ c and d > 0
N = unlimited                       when R ≥ c
```

The model is deliberately crude. It ignores tensions that writers invent later, and it treats all tensions as the same size. What it captures is the one thing a bible author controls on day one: the ratio between what the setting spends and what it refills.

### Numbers you can check

Take an invented setting with `P(0) = 12` plot tensions at launch and `c = 3` consumed per expansion. Vary the refill.

| Refill `R` per expansion | Drain `d = c − R` | Stock at start of expansions 1, 2, 3, 4, 5, 6 | Full expansions `N` |
|---|---|---|---|
| 0 (no structural tensions) | 3 | 12, 9, 6, 3, 0, — | 4 |
| 1 (for example `S = 2`, `g = 0.5`) | 2 | 12, 10, 8, 6, 4, 2 | 5 |
| 2 (`S = 4`, `g = 0.5`) | 1 | 12, 11, 10, 9, 8, 7 | 10 |
| 3 (`S = 6`, `g = 0.5`) | 0 | 12, 12, 12, 12, 12, 12 | unlimited |

Check the second row with the formula. `(12 − 3) / 2 = 4.5`, floor 4, plus 1 is 5. At the start of expansion 6 the stock is 2, less than the 3 needed, so expansion 6 must invent new material or ship a thinner story.

Look at the jump between the second and third rows. Refill went from 1 to 2 and the setting's life doubled from 5 to 10 expansions. Near the break-even point, small changes in refill make large changes in lifetime, because `N` has `d` in the denominator. That is the non-obvious result, and it is why structural tensions are worth more than their count suggests.

The same ledger in code, which you will extend in the lab:

```python
def expansions(P0, c, R, cap=50):
    """Full expansions a setting can supply. R = g*S plot tensions spawned per expansion."""
    stock, n, history = P0, 0, [P0]
    while stock >= c and n < cap:
        stock = stock - c + R
        n += 1
        history.append(stock)
    return n, history

for R in (0, 1, 2, 3):
    n, h = expansions(12, 3, R)
    print(f"R={R}: {n if n < 50 else 'unlimited'} expansions, stock {h[:8]}")
```

It prints:

```
R=0: 4 expansions, stock [12, 9, 6, 3, 0]
R=1: 5 expansions, stock [12, 10, 8, 6, 4, 2]
R=2: 10 expansions, stock [12, 11, 10, 9, 8, 7, 6, 5]
R=3: unlimited expansions, stock [12, 12, 12, 12, 12, 12, 12, 12]
```

### The visual

Open the interactive. The left panel shows the stock `P(t)` as bars across twelve expansions, with a line at `c` marking the level an expansion needs. The right panel shows the same setting as a split: how much of each expansion's story came from launch stock and how much from refill. Start with `R = 0`. The bars fall in a straight staircase and hit the line at expansion 4. Now drag the structural-tension slider up. On the left the staircase flattens. On the right, the refill share grows until, at break-even, every expansion runs entirely on refill and the launch stock is never touched. The bible that looks richest at launch (a big `P(0)`) is not the one that lasts. The one with the most refill is.

### Cross-game recognition

**Guild Wars 2 (2012 to 2022).** The six Elder Dragons were a launch stock of plot tensions with `R = 0` for dragons: nothing in the systems made new dragons. Six dragons fell in the 114 months from August 2012 to February 2022, about one every 19 months, with two in a single chapter in 2021. When it ran out, ArenaNet started a new stock rather than a refill.

**World of Warcraft (Legion to Battle for Azeroth).** The Burning Legion had been the Warcraft series' great enemy since Warcraft III. Legion (August 2016) ended that plot tension, with the Legion's master Sargeras imprisoned at the end of the final raid. The next expansion, Battle for Azeroth (August 2018), was built on the war between the Horde and the Alliance. That is a structural tension. Every player belongs to one of the two factions, and for most of the game's life the factions had separate capitals and could not group together. The systems kept the war alive between stories, so when the plot stock was low, the writers could draw on it again. Watch what happens to a structural tension when its system weakens. Patch 9.2.5 (May 2022) let Horde and Alliance players group for dungeons and raids. That is a good change for players who want to play with friends, and it also lowers `g` for the faction war, since the systems no longer produce daily friction between the sides.

**Final Fantasy XIV (2013 to 2024).** Endwalker (December 2021) concluded the story arc that began with A Realm Reborn in 2013, which the game's director described as the Hydaelyn and Zodiark arc. The next expansion, Dawntrail (July 2024), sent players to a new continent, Tural, to take part in a contest of succession for its throne. Like Guild Wars 2, FFXIV chose to close one stock and open another. Unlike Guild Wars 2, it did so with a new region, which brings its own tensions. Opening new geography is the most common way MMOs restock, and it is the subject of week 2.

**EVE Online (since 2003).** EVE is the extreme case of refill. Its four empires are locked in cold wars, and since the Empyrean Age expansion (2008) players can enlist in faction warfare militias to fight over border systems. More important, players' own alliances produce wars, betrayals and collapses without any writer. In the model, EVE's `g` is set by its players, and it is large enough that CCP has never needed to kill a villain to keep the setting alive. [MMO301 week 6](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md) covers the systems that make that possible.

Four games, one ledger. Guild Wars 2 and FFXIV spend and restock. WoW spends plot stock and falls back on a system-backed structural tension. EVE runs almost entirely on refill.

### Eyes-open design judgment

Plot tensions are not worse than structural ones. They are what give an expansion a climax. Players remember killing a dragon. Nobody remembers "the border remained contested." So the choice is a mix, and you should set it on purpose.

- **Plot-heavy settings** give strong endings and clear marketing ("the final battle against X"). They drain on a schedule, and the restock (a new continent, a new threat from outside) can feel arbitrary if the bible never prepared it.
- **Structure-heavy settings** last, but they can feel like nothing ever changes. If every expansion is "the war continues," players stop believing the war matters. Structural tensions need plot tensions on top of them to have a shape.
- **Tie structural tensions to systems** where you can. A tension that only lives in lore text depends on writers remembering it. A tension enforced by faction choice, a contested resource or territory control is renewed every day by players, whether writers touch it or not.
- **Watch changes that weaken the system under a structural tension.** Cross-faction play in WoW is an example of a sensible change with a narrative cost. The cost may be worth paying. Make it a known cost.
- **Keep a restock plan in the bible.** Name the region, the outside force or the internal split you will open when the launch stock runs low. The budgeting habit from [GD202 week 3](../../GD202-narrative-and-quest-design/lectures/w03-branching-structures-and-the-combinatorial-explosion.md), never plan a story you can't pay for, applies to settings too.

## 3. From lore to ledger: auditing a bible

The ledger is only useful if you can fill it from a real bible. Here is a procedure you will use in the lab and again in the final bible.

1. **List every tension.** Go through the bible and write one line per tension in the form "who wants what, and what blocks them." If a paragraph contains no want and no block, it is not a tension. It may still do job 1 or job 2.
2. **Classify each one.** Ask: if we ship a story that resolves this, is it gone? If yes, it is a plot tension. If the world would regenerate it (because a system, a geography or a faction structure keeps producing it), it is structural.
3. **Estimate `g` for each structural tension.** How often, in expansions, could a writer pull a new plot tension out of it without repeating themselves? A contested border might give one new crisis per expansion (`g = 1`). A theological dispute might give one every two expansions (`g = 0.5`).
4. **Estimate `c`.** Look at a comparable game. How many arcs close per expansion? Three to five is common for a large themepark expansion (one main arc and a few zone arcs). A smaller team might close one or two.
5. **Compute `N`.** If it is under the number of years your business plan assumes, the bible needs more refill or a restock plan.

A worked mini-audit. A student bible for a coastal world lists:

| Tension | Kind | `g` |
|---|---|---|
| The Drowned King wants to flood the coast; the lighthouses hold him back | plot | — |
| The Tide Council hides that it made a pact with the Drowned King | plot | — |
| Two port cities both claim the only deep-water harbour | structural (tied to a territory-control system) | 1 |
| Salt traders and fishers fight over the tidal flats | structural (tied to gathering nodes) | 0.5 |
| A lost fleet waits beyond the fog | plot | — |
| Seven more minor villains and mysteries | plot | — |

That is `P(0) = 10` and `R = 1.5`. If each expansion closes `c = 3` arcs, `d = 1.5` and `N = floor(7 / 1.5) + 1 = 5`. Five expansions at one every two years is ten years, which may be enough. At one per year it is not. The fix is cheap: one more structural tension with `g = 1` brings `R` to 2.5, `d` to 0.5 and `N` to 15.

## 4. What makes a structural tension good

Not every standing conflict produces stories at the same rate. Four properties raise `g`.

**It is tied to a system players touch.** The harbour in the audit is good because a territory-control system changes who owns it. Every change of owner is a new situation for a writer to use.

**It has more than two sides.** A conflict with two sides has one relationship. A conflict with four sides has six, and alliances can shift. Week 3 treats this as a graph and shows why three or more parties keep a conflict moving.

**Both sides are partly right.** If one side is plainly evil, the conflict is a plot tension waiting to be resolved, however long you delay it. If both sides have a legitimate claim, players will argue about it, and that argument is itself content. GD202 week 9 on [emergent narrative](../../GD202-narrative-and-quest-design/lectures/w09-emergent-narrative.md) explains how players turn such conflicts into their own stories.

**It is cheap to restate.** A structural tension should fit in one sentence that any new writer can pick up. "Both cities need the harbour" can be restated in a new zone, a new quest, a new event. "The metaphysical implications of the Third Convergence" cannot.

## 5. Explaining systems: a checklist for your bible

Section 1 said every mechanic is either explained or tolerated. For your bible, make that choice visible. List the mechanics your game design commits to, and for each one write a line.

| Mechanic | Explain or tolerate? | If explained, the world rule | Obligations the rule creates |
|---|---|---|---|
| Respawn after death | explain | Heroes are bound to a waystone that rebuilds their body | Villains can target waystones; NPCs who are not bound die permanently |
| Fast travel | explain | Waystones link to each other | Travel between unlinked places is slow; new regions start unlinked |
| Shared bank across cities | tolerate | — | — |
| Many players kill the same boss | tolerate (instancing) | — | See GD202 week 13 on phasing |

Notice that the two explained rows share one invention, the waystone. A good explanation covers several mechanics with one idea, and it creates obligations writers can use as tensions. "Villains can target waystones" is a plot tension generator you got for free.

The right-hand column is the part students skip. Write it. Every explanation has costs, and the worst lore problems in long-running games come from an explanation that obliges the world to something writers later forget.

## In-class activity (25 minutes)

Groups of three. Each group gets one invented setting summary (half a page, provided by the instructor) or uses the coastal world from section 3.

1. **Ledger (10 min).** List every tension in the summary. Classify each as plot or structural. For each structural one, estimate `g` and write one sentence justifying it.
2. **Compute (5 min).** Using `c = 3`, compute `R`, `d` and `N`. Check your stock sequence with the interactive.
3. **Fix (10 min).** Propose one change to the setting that raises `N` above 8 without adding more than one new tension. Name the game system it attaches to.

Expected output: a table of tensions, the numbers `P(0)`, `R`, `d` and `N` before and after your change, and a two-sentence justification of the change.

## Common misconceptions

- **"A richer bible lasts longer."** A bigger `P(0)` adds lifetime only linearly. Refill changes the drain in the denominator, so near break-even one structural tension can add more expansions than ten plot tensions.
- **"Structural tensions are just long plots."** A long plot still ends. The test is whether the world regenerates the tension after a story resolves one instance of it. The Burning Legion lasted many years in Warcraft and still ended.
- **"Every mechanic needs a lore explanation."** Explaining creates obligations. Tolerating a mechanic as a genre convention is often the better choice, and players accept it.
- **"The model says plot tensions are bad."** Plot tensions give expansions their climaxes. The model tells you how fast you spend them, not whether to have them.

## Check yourself

1. A bible holds `P(0) = 20` plot tensions. Each expansion closes `c = 4`. There are 3 structural tensions with `g = 0.5`. How many full expansions can the setting supply? What is the stock at the start of the first expansion that cannot be fully supplied?
2. The same studio can afford one change: add 8 plot tensions to the launch bible, or add one structural tension with `g = 1`. Which gives more expansions? Show both numbers.
3. A game explains respawn as "the gods return fallen champions to the nearest shrine." Name two obligations this creates for future writers, and one tension it could generate.
4. Classify each as plot or structural, and justify in one sentence: (a) a lich who wants to raise an army; (b) a mountain pass that is the only land route between two trade leagues; (c) a prophecy of a comet that will strike in 1,000 years.

<details>
<summary>Answers</summary>

1. `R = 1.5`, `d = 2.5`. `N = floor((20 − 4) / 2.5) + 1 = floor(6.4) + 1 = 7`. The stock goes 20, 17.5, 15, 12.5, 10, 7.5, 5, then 2.5 at the start of expansion 8, which is less than 4.
2. Adding 8 plot tensions: `P(0) = 28`, `d = 2.5`, `N = floor(24 / 2.5) + 1 = 10`. Adding a structural tension: `R = 2.5`, `d = 1.5`, `N = floor(16 / 1.5) + 1 = 11`. The structural tension wins, and it keeps winning in later expansions.
3. Obligations: NPC champions presumably also return, so their deaths in stories can't be permanent unless the gods refuse them; shrines must exist wherever players can die, including new regions. A tension: a region where the gods' reach fails, or a faction that desecrates shrines to make champions mortal.
4. (a) Plot: killing the lich resolves it. (b) Structural: any number of wars, tolls, bandits and smugglers can arise from it, and nothing resolves geography. (c) Plot, but a slow one. It gives one climax whenever you choose to spend it. It can feed structural tensions (cults, evacuation politics) if the bible builds them.

</details>

## Lab / assignment hook

[Lab 01, the tension ledger](../labs/lab01.md). You implement the ledger and an audit tool that reads a bible's tensions from a JSON file, then audit the first draft of your own world bible and fix it until it supplies at least eight expansions. This is the first exercise toward the final world bible (60% of the course).

## Sources

- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter list and scope from the publisher's page (chapter 3, "World Structures and Systems of Relationships", https://doi.org/10.4324/9780203096994-10; worlds treated as transnarrative, transmedial and transauthorial).
- EVE University Wiki, "Clones" (current, checked September 2026). Pod destruction wakes the pilot in a new clone at the home station; jump clones carry skills and standings but not items; implants stay with the body.
- Guild Wars 2 Wiki, "Elder Dragon" (checked September 2026). The six Elder Dragons and the story steps in which each was defeated: Zhaitan (personal story), Mordremoth (Heart of Thorns), Kralkatorrik (War Eternal), Jormag and Primordus (Dragonstorm), Soo-Won (End of Dragons).
- Guild Wars 2 Wiki, "Guild Wars 2: Heart of Thorns", "War Eternal", "Champions", "Guild Wars 2: End of Dragons", "Guild Wars 2: Secrets of the Obscure" and "Release". Launch 28 August 2012; Heart of Thorns 23 October 2015; War Eternal 14 May 2019; Champions chapter 4, Judgment (containing Dragonstorm), 27 April 2021; End of Dragons 28 February 2022; Secrets of the Obscure 22 August 2023.
- Warcraft Wiki, "World of Warcraft: Legion", "Burning Legion", "Battle for Azeroth" and "Patch 9.2.5" (checked September 2026). Legion released 30 August 2016; Sargeras listed as imprisoned; Battle for Azeroth released 13/14 August 2018 with the Horde and Alliance conflict as its premise; patch 9.2.5 released 31 May 2022 with cross-faction instances.
- Wikipedia, "Final Fantasy XIV: Endwalker" and "Final Fantasy XIV: Dawntrail" (checked September 2026). Endwalker released 7 December 2021, described by Naoki Yoshida as the conclusion of the Hydaelyn and Zodiark arc begun with A Realm Reborn in 2013; Dawntrail released 2 July 2024, set in Tural around a rite of succession.
- EVE University Wiki, "Faction Warfare" (checked September 2026). Faction warfare introduced in the Empyrean Age expansion (2008).

## Interactive spec: examples/w01-tension-ledger.html

**Purpose.** Show that a setting's lifetime depends far more on refill (structural tensions) than on the size of its launch stock, and that lifetime explodes near break-even.

**The one insight the visual must make obvious.** Two settings with very different launch stocks can have the same lifetime, and a small increase in refill near `R = c` doubles or triples the number of expansions.

**Model (exact).**
- Inputs: `P0` (launch plot tensions), `c` (consumed per expansion), `S` (structural tensions), `g` (spawn per structural tension per expansion). `R = g × S`.
- Simulate expansions `t = 1 … 12`. Stock at start of expansion 1 is `P0`. Expansion `t` is "full" if `stock ≥ c`; then `stock ← stock − c + R`. If not full, mark it "short" and set `stock ← stock + R` (nothing consumed; the bar is drawn in the warning color).
- Report `N` = number of full expansions before the first short one, using the closed form `floor((P0 − c)/(c − R)) + 1` when `c > R` and `P0 ≥ c`, `0` when `P0 < c`, and "unlimited" when `R ≥ c`. The closed form must match the simulation for all integer inputs in range.
- For each full expansion, split its `c` into "from launch stock" and "from refill": refill share is `min(R, c) / c`.

**Controls.**
- Slider `P0`: 0 to 40, step 1, default 12.
- Slider `c`: 1 to 6, step 1, default 3.
- Slider `S`: 0 to 10, step 1, default 0.
- Slider `g`: 0 to 1.5, step 0.25, default 0.5.
- Preset buttons: "Invented setting, R = 0" (12, 3, 0, 0.5), "R = 1" (12, 3, 2, 0.5), "R = 2" (12, 3, 4, 0.5), "Break-even" (12, 3, 6, 0.5), "Guild Wars 2 dragons" (P0 = 6, c = 1, S = 0, g = 0; label that c is dragons per major release, illustrative).
- All controls keyboard operable with visible labels and current values.

**Views.**
- Left: bar chart of stock at the start of each expansion 1 to 12, horizontal line at `c`. Full expansions in the primary color, short ones in the warning color.
- Right: stacked bar per full expansion showing launch-stock share and refill share, and a large readout "N = 5 expansions" (or "unlimited").
- Below: a small line chart of `N` against `R` from 0 to `c` (at fixed `P0` and `c`), with the current `R` marked. This is the "near break-even" curve and should visibly shoot up as `R` approaches `c`.
- Numbers table: `R`, `d`, `N`, and the stock sequence, copyable.

**Test values (must match exactly).**
- `P0 = 12, c = 3, S = 0`: stock 12, 9, 6, 3, 0; `N = 4`.
- `P0 = 12, c = 3, S = 2, g = 0.5`: `R = 1`, stock 12, 10, 8, 6, 4, 2; `N = 5`.
- `P0 = 12, c = 3, S = 4, g = 0.5`: `R = 2`, `N = 10`.
- `P0 = 12, c = 3, S = 6, g = 0.5`: `R = 3`, `N` unlimited.
- `P0 = 20, c = 4, S = 3, g = 0.5`: `R = 1.5`, `N = 7`, stock at start of expansion 8 is 2.5.

**Style.** Shared tokens from `templates/interactive-tokens.css`. No game art or logos. Draw dragons, if at all, as plain numbered markers.
