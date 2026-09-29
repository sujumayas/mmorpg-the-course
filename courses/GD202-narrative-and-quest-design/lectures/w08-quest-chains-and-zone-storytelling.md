# GD202 · Week 08 — Quest Chains and Zone Storytelling

**Why this matters:** A single quest can tell a scene. A zone has to tell a story across twenty or thirty quests that players take in orders you don't control. Every prerequisite you add buys you control over that order and charges the player a walk back to the quest giver. This week you learn to see both sides of that trade in one small graph, and to build zones whose stories hold together without wasting the player's evening.

**You will be able to:**
- Model a zone's quests as a prerequisite graph and compute its trips `T`, width `W` and order control `C` by hand and in code.
- Compare linear, parallel, braided and flat chain shapes by play time and by how much of the story order they fix.
- Design a zone arc with a small fixed spine and order-free side quests, and justify where each bottleneck beat sits.
- Critique a shipped zone's chain structure from its quest list, naming the shape and its cost.

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the chapter on nonlinear and branching structure (the course reader lists the pages). Warcraft Wiki, "Breadcrumb quest" and "Quest Log" (10 minutes together). If you have a World of Warcraft or Guild Wars 2 account, spend 30 minutes in one levelling zone and write down every quest or task you pick up, in order, with the place you picked it up.

**Prerequisites from earlier courses:** [CS102 week 8, graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) taught adjacency lists and graph search. This week uses directed graphs without cycles and does not re-teach storage or search. [GD201 week 10, hubs, spokes and gating](../../GD201-level-and-world-design/lectures/w10-hubs-spokes-and-gating.md) (same semester) computes the cost of one errand from the hub. Here that cost is the round trip `t_travel`, and we count how many errands a chain forces. [UX201 week 2, cognitive load](../../UX201-game-ux-and-player-psychology/lectures/w02-cognitive-load-and-ui.md) explains why a full quest log is a working-memory problem. Within this course, [week 1](w01-story-vs-narrative-vs-plot.md) promised that zone quests must work "first, middle or last", and [week 4](w04-dialogue-systems-and-state-flags.md) gave you the flags a chain reads.

**Interactive:** [`examples/w08-quest-chain-shapes.html`](../examples/w08-quest-chain-shapes.html). Keep it open during section 2.

---

## 1. From quests to chains

Last week you priced one quest. Players never meet one quest alone. They meet them in a **zone**, a region of the world with its own quest givers, enemies and story, and they meet them in groups.

Three terms carry this week.

- A **prerequisite** is a quest that must be finished before another unlocks. "Kill the bandit scouts" before "Find the bandit camp."
- A **quest chain** is a sequence of quests linked by prerequisites. The Warcraft Wiki notes that most World of Warcraft quests are not single steps but belong to follow-up series that players call chains.
- A **hub** is the place where quests are handed out and turned in, usually a town or camp. GD201 week 10 measured hubs as spaces. This week measures them as the points where a chain forces the player to come back.

A fourth term connects zones to each other. A **breadcrumb quest** exists only to send the player from one zone to the next. World of Warcraft usually makes breadcrumbs to the same place mutually exclusive, so taking one closes the others. A breadcrumb is a prerequisite edge that leaves the zone.

Put these together and a zone's quest design is a **directed graph**. Each quest is a node. Each prerequisite is an arrow from the earlier quest to the later one. A zone graph never has a cycle, because a cycle would mean two quests each waiting for the other, and neither could ever unlock. A directed graph with no cycles is called a **DAG** (directed acyclic graph).

The graph is the plot structure of the zone, in the sense of week 1. It fixes which story beats a player can meet in which orders. It is also the zone's travel plan. That double role is the whole lesson.

## 2. Worked example: nine quests, five shapes

### The hook

Two successful online RPGs made opposite choices about quest chains.

Final Fantasy XIV runs its story through one long Main Scenario chain. In the base game, A Realm Reborn, that chain is about 160 quests long, and finishing it is how players unlock cities, dungeons, trials and mounts. Square Enix also sells story-skip items that jump a character to the start of a later expansion's chain.

Guild Wars 2, at launch in 2012, filled its zones with renown hearts. A heart is a fixed area with a list of tasks, and it needs no quest giver and no prerequisite. A player can walk into any heart on the map, in any order.

World of Warcraft has moved between the two. In patch 4.0.3a (November 2010), Blizzard rebuilt the original continents with thousands of new quests, and the patch notes also mention new level ranges for some zones "to improve the questing flow". Zones such as Westfall became one continuous storyline: an investigation at Sentinel Hill uncovers the rebirth of the Defias Brotherhood under Vanessa VanCleef, the Brotherhood burns Sentinel Hill, and the arc ends in the Deadmines dungeon.

So what are these teams trading? When is a long chain worth selling a skip for, and when is a map of order-free tasks better?

### The model

Take a zone of `n` quests with their prerequisites as a DAG. Assume a **batching player**. They take every quest that is currently unlocked, go out and do them all in one trip, come back to the hub, turn them in, and repeat. Most experienced players play close to this.

Three numbers describe the zone.

```
layers   L1 = quests with no prerequisites
         Lk = quests whose prerequisites all lie in L1 … L(k−1)

T  (trips)          = number of layers
W  (width)          = size of the largest layer
C  (order control)  = fixed pairs / all pairs,  all pairs = n(n − 1) / 2

zone time           = n × t_task + T × t_travel
```

- `T` is the number of round trips to the hub. It equals the length of the longest chain in the zone, counted in quests.
- `W` is the most quests a player holds at once. It is what the quest log has to show.
- A pair of quests is **fixed** when one is an ancestor of the other, meaning the first must be finished, directly or through other quests, before the second unlocks. Then every player meets them in the same order. `C` is the share of pairs the designer has fixed, from 0 (any order) to 1 (one order for everyone).
- `t_task` is the minutes of work per quest (the fighting and gathering, priced last week).
- `t_travel` is the minutes per round trip from the hub to the quest area and back, GD201's errand cost. Week 6 used the same name for the same walk when it priced a single quest's detour.

`T` is the travel side of the trade. `C` is the story side. A chain edge usually raises both.

### Numbers you can check

Nine quests, each with `t_task = 3` minutes of work, and a round trip of `t_travel = 4` minutes. Five shapes.

- **Linear.** q1 → q2 → … → q9. One story, told in order.
- **Strands.** Three separate chains of three (a1→a2→a3, b1→b2→b3, c1→c2→c3). Three short stories that never meet.
- **Braided.** One intro quest unlocks three parallel quests. All three unlock a "turn" quest. The turn unlocks three more parallel quests, and all three unlock a finale.
- **Waves.** Three quests, then three that each need all of the first three, then three that each need all of the second three.
- **Flat.** Nine quests with no prerequisites.

| Shape | `T` (trips) | `W` (width) | Fixed pairs of 36 | `C` | Zone time (min) |
|---|---|---|---|---|---|
| Linear | 9 | 1 | 36 | 1.00 | 27 + 36 = 63 |
| Braided | 5 | 3 | 30 | 0.83 | 27 + 20 = 47 |
| Waves | 3 | 3 | 27 | 0.75 | 27 + 12 = 39 |
| Strands | 3 | 3 | 9 | 0.25 | 27 + 12 = 39 |
| Flat | 1 | 9 | 0 | 0.00 | 27 + 4 = 31 |

Check the braided row by hand. The intro is an ancestor of all 8 other quests (8 pairs). Each of the three first-half quests is an ancestor of the turn, the three second-half quests and the finale (5 each, 15 in total). The turn is an ancestor of the four quests after it (4). Each second-half quest is an ancestor of the finale (3). That makes `8 + 15 + 4 + 3 = 30` fixed pairs of 36. The only free pairs are the three pairs within each parallel group (6 in total).

Now read the table. Linear gives the designer total control and costs 32 minutes more than flat, which is more than the 27 minutes of actual quest work. Strands and waves cost exactly the same time (3 trips each), yet waves fix three times as many pairs. The shape of the edges matters more than the count of edges. Braided spends two extra trips over waves to buy three **bottleneck** quests: layers of width 1, where every player in the zone meets the same beat at the same point in their story.

You can reproduce the table with a short function:

```python
from itertools import combinations

def layers(zone):
    done, out = set(), []
    while len(done) < len(zone):
        layer = sorted(q for q, pre in zone.items() if q not in done and pre <= done)
        if not layer:
            raise ValueError("cycle")
        out.append(layer)
        done |= set(layer)
    return out

def ancestors(zone, q):
    seen, stack = set(), list(zone[q])
    while stack:
        x = stack.pop()
        if x not in seen:
            seen.add(x)
            stack.extend(zone[x])
    return seen

def measure(zone, t_task=3, t_travel=4):
    L = layers(zone)
    anc = {q: ancestors(zone, q) for q in zone}
    pairs = list(combinations(zone, 2))
    fixed = sum(1 for x, y in pairs if x in anc[y] or y in anc[x])
    return len(L), max(map(len, L)), fixed, len(zone) * t_task + len(L) * t_travel

mid, end = {"b1", "b2", "b3"}, {"d1", "d2", "d3"}
braided = {"intro": set(), "b1": {"intro"}, "b2": {"intro"}, "b3": {"intro"},
           "turn": mid, "d1": {"turn"}, "d2": {"turn"}, "d3": {"turn"}, "finale": end}
linear = {f"q{i}": ({f"q{i-1}"} if i > 1 else set()) for i in range(1, 10)}
print("braided", measure(braided))
print("linear ", measure(linear))
```

```
braided (5, 3, 30, 47)
linear  (9, 1, 36, 63)
```

### A visual you can move

Open the interactive. The left view draws the zone graph with quests arranged in layers, left to right, so each column is one trip. The right view is a scatter plot with trips `T` on the horizontal axis and order control `C` on the vertical, with a dot for each of the five preset shapes and a larger dot for the zone you are editing.

Pick the linear preset, then click any arrow to remove it. The graph gains a column-merge and the dot jumps left and down. Pick flat and draw arrows between quests. Watch which arrows move the dot straight up (they fix pairs without adding a layer) and which move it right as well. The top-left corner, high control for few trips, is where good zone designs live. You cannot reach the corner itself, but you can get closer to it than the linear chain does.

### Cross-game recognition

Each of the games in the hook is a point on the same scatter plot.

**Final Fantasy XIV, Main Scenario (A Realm Reborn onward).** A very long linear spine. `C` is close to 1 for the main story and `T` is roughly the number of quests, around 160 in the base game alone. The game softens this by mixing side quests and content unlocks around the spine, and by letting players who don't want the chain buy their way past it. A paid skip is what a high-`T` design looks like from the business side. Some players value the time more than the fixed story.

**Guild Wars 2, renown hearts (2012 onward).** Each heart has no prerequisite, so a zone of hearts is the flat shape. `T` is 1 per heart, with no hub at all, and `C` is 0. The zone story is carried by the place and by dynamic events rather than by order. Later expansions added repeatable and tiered hearts, and some zones dropped hearts entirely for large meta event chains that span the whole map. Those chains move a zone back toward the braided shape.

**World of Warcraft, Cataclysm revamp (patch 4.0.3a, 2010).** The rebuilt Westfall reads as a braid. Groups of parallel quests around Sentinel Hill feed the investigation, the attack on Sentinel Hill is a bottleneck beat that every player meets at the same point, and the Deadmines is the finale. Later, patch 9.0.2 (Shadowlands, 2020) added a separate marker for campaign quests that advance the main narrative, distinguished from optional side quests that tell local stories. That is the braid made visible to the player: a marked spine with high `C`, and unmarked side quests with `C` near 0.

**Quest log caps.** `W` has a hard limit in most games. World of Warcraft launched with a 20-quest log, raised it to 25 with The Burning Crusade, and to 35 during Dragonflight (a hotfix in December 2022). With a cap of `m` quests, a zone can never have `T < n / m` for a batching player. A flat zone of 60 quests under a 20-quest cap needs at least 3 trips. Designers who build wide zones are also designing against the log.

### Eyes-open design judgment

The model makes the trade visible. It does not choose for you.

- **Spend chain edges where order carries meaning.** A reveal, a betrayal, a death: these need a fixed order, because the later beat makes no sense without the earlier one. Most other beats don't. The Westfall arc needs the investigation before the attack. It does not need the farm chores in any order.
- **Prefer waves over strands when the stories should touch.** Both cost the same trips here. Waves fix far more pairs, which means the writer can refer back to earlier quests. Strands keep stories apart, which is right when they really are separate.
- **Put bottlenecks at the turns of the zone arc.** A width-1 layer is expensive (it adds a trip) and valuable (every player shares that beat). Use two or three per zone, not nine.
- **Watch `W` as well as `T`.** A flat zone looks cheap in trips but hands the player nine open quests at once. UX201 week 2 would call that a working-memory load. It is also nine quests that must each make sense in any order, which is the hardest kind to write (week 1).
- **The batching player is an assumption.** New players often take one quest at a time. For them `T = n` in every shape, and chain edges cost nothing extra. The batching model is the right one for players who already know the game, and they are the ones who complain about walking.

## 3. Zone storytelling: the spine and the ribs

A good zone arc usually has the braided shape in disguise. Call the chain of bottleneck quests the **spine** and the parallel groups between them the **ribs**.

### Writing the spine

The spine is a short linear chain, often four to six quests, that carries the zone's story from setup to resolution. Treat it like the plot of a short story (week 1).

1. **Arrival.** The first bottleneck. It names the zone's problem and its main characters. In the Westfall arc, this is the arrival at Sentinel Hill and the first word of trouble.
2. **Turn.** A middle bottleneck where the player learns that the problem is not what it seemed. The turn needs everything before it to land, so it must be a bottleneck.
3. **Crisis.** The problem hits the hub itself. Burning the hub the player has been returning to is a strong crisis, because the player has walked through it many times (GD201 week 10's hub is also a character).
4. **Resolution.** The finale, often a dungeon or a big fight, followed by a breadcrumb out.

### Writing the ribs

Rib quests sit in a parallel group, so they must work in any order within their group. Week 1 gave the rule: each one should make sense first, middle or last. Three techniques help.

- **Self-contained setup.** Each rib quest introduces its own NPC and problem in its own text. It can refer to the last spine beat, which every player has seen, but not to a sibling rib quest.
- **Converging evidence.** Each rib quest yields one clue, object or favor that the next spine quest needs. The spine quest then reads "with what you've found" rather than a specific item, so it works whichever ribs the player did first. If the spine quest needs all three, you get the braided shape exactly. If it needs any two, the player can skip one rib, and your graph needs an "any `k` of" rule that plain prerequisites don't express. Week 4's counters and flags implement it.
- **Place-based story.** Rib quests can tell the zone's story through the places they send players, the burned farmhouse, the abandoned mine. GD201 week 8 showed how to compute the chance a player notices an environmental clue. Rib quests are how you make sure they walk past it.

### Chains between zones

A breadcrumb connects one zone's resolution to the next zone's arrival. Treat the breadcrumb as the last rib of one zone and the first spine beat of the next. If several breadcrumbs lead to the same zone, make them mutually exclusive, as World of Warcraft usually does, so the player never carries two quests that say "go to Westfall."

## 4. When the graph lies

Three cases where the simple DAG model misleads you.

**Field handoffs.** A follow-up quest handed out in the field (by an NPC at the camp, or by an item you loot) doesn't need a trip back to the hub. An edge that is handed off in the field adds a layer but not a trip. The lab asks you to extend the model: count only layers that start at the hub.

**Any-of prerequisites.** Real quest systems allow "finish any two of these three." That is not an edge in a plain DAG. Model it with a counter (week 4) and compute `T` for the worst and best choice of which two.

**Shared worlds.** In an online game, the zone's state is not only the player's. If the Defias burn Sentinel Hill for one player, they cannot also leave it standing for the player next to them. How games show different versions of the same place to different players is week 13's topic. For now, notice that every bottleneck beat that changes the world raises that problem.

## In-class activity (25 minutes)

Work in groups of three. You get a deck of 12 quest cards for a fictional zone, the Saltmarsh. Each card names a quest, its giver and a one-line summary. Three cards are marked "story" and describe a smuggling ring, the discovery of its leader, and a raid on its warehouse.

1. **(5 min)** Arrange all 12 cards as a flat zone and compute `T`, `W` and `C`. (`T = 1`, `W = 12`, `C = 0`.)
2. **(10 min)** Add prerequisite arrows (drawn on the table with string or on a whiteboard) to reach `C ≥ 0.6` with `T ≤ 5`. The three story cards must be bottlenecks. Record your arrows as a list.
3. **(5 min)** Compute zone time with `t_task = 3` and `t_travel = 4`, and compare with the flat zone.
4. **(5 min)** Swap arrow lists with another group. Enter their zone in the interactive, confirm their numbers, and find one rib quest in their design that cannot be written to work in any order within its group. Explain why.

Expected output: an arrow list, `T`, `W`, `C`, zone time, and the other group's critique.

## Common misconceptions

- **"Linear chains are bad design."** They buy full control of order, which is exactly what a reveal needs. The cost is trips, and it is worth paying on the spine. It is rarely worth paying on every quest.
- **"More prerequisites always mean more control per trip."** No. Strands and waves have the same `T` here, but waves fix three times as many pairs. Where you put the arrows matters more than how many you draw.
- **"A flat zone has no story."** It has no order. Story can still come from place, character and the world state. It just can't rely on the player having seen something first.
- **"`T` is the number of chains."** `T` is the length of the longest chain, in quests. Nine short strands of one quest each give `T = 1`, not 9.

## Check yourself

1. A zone has one intro quest, four parallel quests that each need the intro, and a finale that needs all four. Compute `T`, `W`, `C` and zone time with `t_task = 3`, `t_travel = 4`.
2. A 12-quest linear chain has `t_travel = 5` minutes. How many minutes of travel does it cost the batching player? You split it into four strands of three. What are the new travel time and the new `C`?
3. A flat zone has 30 quests and the game's quest log holds 20. What is the smallest possible `T` for a batching player, and why does the log cap act like a hidden prerequisite?
4. In the braided zone, the designer removes the arrow from b2 to the turn (b2 still needs the intro). Without the interactive, say how `T` and `C` change. Then say what writing problem this creates for b2.

<details>
<summary>Answers</summary>

1. Layers {intro}, {four quests}, {finale}, so `T = 3` and `W = 4`. Fixed pairs: intro with 5 others (5) and each of the four with the finale (4), 9 of 15, so `C = 0.6`. Time `6 × 3 + 3 × 4 = 30` minutes.
2. Linear: `T = 12`, travel `12 × 5 = 60` minutes. Four strands of three: `T = 3`, travel 15 minutes. Fixed pairs: 3 per strand, 12 of 66, so `C = 12/66 = 0.18`.
3. At most 20 quests can be carried, so at least `30 / 20 = 1.5`, rounded up to 2 trips. The cap forces a split that the designer did not draw. The player chooses which 20 go first, so the order of the split is theirs, not the designer's.
4. b2 now needs only the intro, so it sits in layer 2 and no longer leads to the turn. The layers are unchanged, so `T` stays 5. b2 loses its 5 fixed pairs with the turn, d1, d2, d3 and the finale, so `C` falls from 30/36 to 25/36, about 0.69. The writing problem: b2 can now be done after the finale, so its text must make sense after the zone's story is resolved, and nothing in the spine can depend on it.

</details>

## Lab / assignment hook

[Lab 08, chain shapes](../labs/lab08.md). You implement layers, `T`, `W` and `C` for a prerequisite graph, extend the model with field handoffs, and design the quest graph for your final project's zone. The graph and its numbers are part of the quest chain assignment (60% of the course grade).

## Sources

- Warcraft Wiki, "Quest". Most World of Warcraft quests belong to follow-up series called chains. https://warcraft.wiki.gg/wiki/Quest
- Warcraft Wiki, "Quest Log". Log limit of 20 at launch, 25 from The Burning Crusade, 35 in Dragonflight (hotfix of 9 December 2022); patch 9.0.2 marks major narrative quests separately from optional side quests. https://warcraft.wiki.gg/wiki/Quest_Log
- Warcraft Wiki, "Breadcrumb quest". Purpose of leading a player from one zone to another; usually mutually exclusive. https://warcraft.wiki.gg/wiki/Breadcrumb_quest
- Warcraft Wiki, "Patch 4.0.3a" (released 23 November 2010). Rebuilt Eastern Kingdoms and Kalimdor with thousands of new quests for levels 1 to 60; the patch notes phrase about improving questing flow. https://warcraft.wiki.gg/wiki/Patch_4.0.3a
- Warcraft Wiki, "Westfall" (Cataclysm-era storyline). Sentinel Hill hub, Defias Brotherhood reborn under Vanessa VanCleef, attack on Sentinel Hill, resolution in the Deadmines. https://warcraft.wiki.gg/wiki/Westfall
- Final Fantasy XIV Online Wiki (consolegameswiki), "Main Scenario Quests" (as of the Dawntrail era, 2026). MSQ required for many features and endgame activities; roughly 160 quests in A Realm Reborn; Tales of Adventure story skips sold in the online store. https://ffxiv.consolegameswiki.com/wiki/Main_Scenario_Quests
- Guild Wars 2 Wiki, "Renown Heart" (game version as of 2026). Tasks rather than a checklist in sequence; no need to talk to the NPC; repeatable and tiered hearts in later zones; some zones use meta event chains instead. https://wiki.guildwars2.com/wiki/Renown_Heart
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury. Course text.
- The nine-quest zones, work times and round-trip times in the worked example are invented for teaching.

## Interactive spec: examples/w08-quest-chain-shapes.html

**The one insight.** Every prerequisite arrow buys story order and may cost a trip back to the hub, but not every arrow costs the same. Some arrows raise order control `C` without adding a trip, so where you put arrows matters more than how many you draw.

**Layout.** Two linked views, side by side on wide screens, stacked on phones.
- **Left view, "The zone graph".** Nine quest nodes (up to 16 in edit mode) drawn in columns by layer (column k = layer k, top to bottom sorted by id). Arrows from prerequisite to quest. Bottleneck layers (width 1) get a highlighted column background labeled "shared beat". Above the graph: `T`, `W`, fixed pairs / all pairs, `C`, and zone time.
- **Right view, "The trade".** Scatter plot, horizontal axis `T` from 1 to 16, vertical axis `C` from 0 to 1. A labeled dot for each of the five presets at its (`T`, `C`). A larger, outlined dot for the current zone, with a faint trail of its last five positions so students see which edits moved it right and which moved it up. Show the line "zone time" as a secondary label on each dot.

**Controls.**
- Preset buttons: Linear, Braided, Waves, Strands, Flat (the lecture's five shapes).
- Edit mode: click (or press Enter on) a source node, then a target node, to add or remove an arrow. Reject an arrow that would create a cycle, with the message "That arrow would make a loop: neither quest could unlock." Keyboard: Tab moves between nodes.
- Buttons: add quest (up to 16), remove selected quest.
- Sliders: work per quest `t_task` (1 to 10 min, default 3), round trip `t_travel` (1 to 15 min, default 4).
- Number field: quest log cap `m` (blank = no cap). When set, the batching player takes at most `m` unlocked quests per trip (lowest ids first). Recompute trips by simulation, and show "log cap adds k trips" when it changes `T`.

**Formulas.**
- Layers: repeatedly take every not-yet-done quest whose prerequisites are all done.
- `T` = number of layers (without cap), or the number of simulated trips (with cap). `W` = largest layer (or `min(m, largest layer)` with cap).
- Ancestors by graph search. Fixed pair = one is an ancestor of the other. `C = fixed / (n(n − 1)/2)`; `C = 1` if `n < 2`.
- Zone time `= n × t_task + T × t_travel`.

**Test values** (`t_task = 3`, `t_travel = 4`, no cap).
- Linear: `T = 9`, `W = 1`, fixed 36/36, `C = 1.00`, 63 min.
- Braided: `T = 5`, `W = 3`, fixed 30/36, `C = 0.833`, 47 min.
- Waves: `T = 3`, `W = 3`, fixed 27/36, `C = 0.75`, 39 min.
- Strands: `T = 3`, `W = 3`, fixed 9/36, `C = 0.25`, 39 min.
- Flat: `T = 1`, `W = 9`, fixed 0/36, `C = 0`, 31 min.
- Braided with the arrow b2 → turn removed: `T = 5`, fixed 25/36, `C = 0.694` (check yourself Q4).
- Flat with log cap `m = 4`: 3 trips, 39 min.

**First screen.** Linear preset, with the scatter plot showing all five presets and the linear dot highlighted in the top-right corner, so the student sees immediately that the braid and waves sit higher than strands for the same or fewer trips.
