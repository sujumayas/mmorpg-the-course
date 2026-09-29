# GD201 · Week 10 — Hubs, spokes, and gating

**Why this matters:** Every time a player finishes something, your layout decides how far they walk before they can start the next thing. That walk is paid again and again, dozens or hundreds of times in a playthrough. Choose the wrong shape and the player spends more time commuting than playing. Choose the gates badly and they spend it redoing content they didn't want to.

**You will be able to:**
- Compute the mean errand cost (hub to destination and back) for chain, ring and hub-and-spoke layouts, by hand and with breadth-first search.
- Predict how each layout's errand cost grows as you add destinations, and find the single shortcut that cuts it most.
- Compute gate slack for a sequence of count gates and redesign thresholds that squeeze the player too hard.
- Critique a hub design in a single-player game and a persistent world, naming what the hub costs as well as what it saves.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019). Use the index entries for "hub" and "spoke" and read the passages on hub-and-spoke and branching layouts (about 15 pages). Super Mario Wiki, "Big Star Door" and "★ door" (10 minutes; note every star count). If you own Super Mario 64 in any version, play from the start until you have opened the first Big Star Door and count how many times you walked through the castle's main hall.

**Prerequisites from earlier courses:** [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (adjacency lists and breadth-first search; this lecture uses BFS without re-teaching it). [GD102 week 6, converters, traders and gates](../../GD102-systems-design-and-game-mechanics/lectures/w06-machinations-diagrams-ii-converters-traders-gates.md) (a gate as a node that holds flow until a condition is met). From this course, [week 7, verticality and navigation](w07-verticality-and-navigation.md) (edge times, one-way edges and the return ratio). [Week 9, open-world structure and POI density](w09-open-world-structure-poi-density.md), turned distance into seconds between points of interest. This week asks how those points should be connected.

**Interactive:** [`examples/w10-hub-errands.html`](../examples/w10-hub-errands.html). Keep it open during section 2.

---

## 1. Three ways to connect the same places

Take eight places a player must visit. Call them **destinations**: a level, a dungeon, a quest area, a boss arena. Add one more place, the **hub**, where the player returns between destinations to heal, save, shop, hand in quests or pick the next goal. How you join these nine places is the **topology** of your world, the pattern of connections regardless of the art or the exact distances.

Three topologies cover most of what ships.

**Chain (or linear).** Hub, then destination 1, then 2, then 3, in a line. Classic side-scrolling levels are chains, and so is a corridor shooter. The player meets content in the order you wrote it. There are no choices about order, and nothing is skipped.

**Hub and spoke.** Every destination hangs off the hub on its own path, called a **spoke**. The player picks a spoke, clears it, comes back, and picks another. The hub sees traffic after every destination.

**Ring (or loop).** A chain whose last destination connects back to the hub. The player can go either way round and never has to retrace the whole route.

Real worlds mix them. A spoke can itself be a short chain. Two spokes can be joined at their far ends. A hub can sit inside a larger hub. But these three are the parts you build the mixes from, and each has a price you can compute.

Two more terms. An **errand** is one round trip: leave the hub, reach a destination, come back. **Backtracking** is walking through space you have already cleared to get somewhere else. Errands are the reason backtracking exists. The player needs something at the hub (a shop, a quest giver, a save point) and the content is out there.

A **gate** is anything that blocks a path until a condition is met: a locked door and its key, a door that opens when you hold enough of some collectible, a zone whose monsters are too strong until you reach a level. Gates decide which spokes exist *yet*. Section 3 is about them.

## 2. Worked example: the castle you keep coming back to

### The hook

In Super Mario 64 (Nintendo, 1996), you enter a course by jumping into a painting in Princess Peach's castle. When you collect a Power Star, the game ends the course and puts you back in the castle room you came from. The one exception is the 100-coin star, which lets you keep playing. The game has 120 stars across fifteen main courses, nine smaller secret courses and a handful of castle secrets. You need 70 to finish.

Think about what that means. Every star is an errand. Collect one and you are back at the hub, walking to the next painting. A player who finishes the game walks through the castle at least 70 times. And almost nobody complains about it. Compare that with a game where you must walk back through the whole level after beating its boss, which players describe as a chore after the second time.

Why does one feel fine and the other feel like work? The castle is a hub, and a hub keeps every errand short no matter how many destinations the game adds. That is a property of the topology, and you can put a number on it.

### The model

Draw the world as a graph (CS102 week 8). The hub is node `h`. The destinations are nodes `1` to `n`. For now, every link is the same length `L` in metres, so the distance between two nodes is `L` times the number of links on the shortest path, `d(h, i)`, which breadth-first search gives you.

The **mean errand cost** is the average round trip from the hub to a destination and back:

```
E = (2 / n) × Σ d(h, i) × L        summed over destinations i = 1 … n
```

- `n` is the number of destinations.
- `d(h, i)` is the number of links on the shortest path from the hub to destination `i`.
- `L` is the length of one link.
- The 2 is there because every errand goes out and comes back.

Divide `E` by the player's speed `v` and you get seconds per errand, which is the number the player actually feels. This course uses `v = 6` m/s for teaching levels (week 1).

For the three topologies, with `n` destinations, the sum has a closed form:

```
chain (hub at one end):        E = L × (n + 1)
ring (chain + one link home):  E = L × (n + 2) / 2          (n even)
hub and spoke:                 E = 2L
```

The chain's destinations sit at 1, 2, …, `n` links from the hub, so the mean distance is `(n + 1) / 2` links and the round trip doubles it. The ring lets you go whichever way is shorter, so the far half of the chain is reached from the other end. The mean distance roughly halves. In the hub-and-spoke layout, every destination is exactly one link away, so the cost doesn't depend on `n` at all.

That last line is the lesson. **In a chain, errand cost grows in proportion to the size of the world. In a hub, it stays flat.** Double the content of a chain and every errand gets about twice as long. Double the content of a hub and nothing changes.

### Numbers you can check

Take `L = 100` metres. At 6 m/s, one link takes about 16.7 seconds.

| Destinations `n` | Chain `E` | Ring `E` | Hub and spoke `E` | Chain in seconds | Hub in seconds |
|---|---|---|---|---|---|
| 4 | 500 m | 300 m | 200 m | 83.3 s | 33.3 s |
| 8 | 900 m | 500 m | 200 m | 150.0 s | 33.3 s |
| 16 | 1,700 m | 900 m | 200 m | 283.3 s | 33.3 s |

Check one row by hand. With `n = 8`, the chain's destinations are 1 to 8 links from the hub. The sum is 36, the mean is 4.5 links, the round trip is 9 links, or 900 metres. For the ring with `n = 8` there are nine nodes on the loop. Going the short way, destinations are 1, 2, 3, 4, 4, 3, 2, 1 links from the hub. The sum is 20, the mean 2.5, the round trip 5 links, 500 metres.

Now multiply by the number of errands. If a player runs one errand per destination, eight destinations cost 7,200 metres of walking in the chain (20 minutes at 6 m/s) and 1,600 metres in the hub (under 4.5 minutes). The content is identical. The topology alone moved 15 minutes of walking.

The same numbers from code, using the BFS you wrote in CS102:

```python
from collections import deque

def distances(graph, start):
    """Breadth-first search: number of links from start to every node."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def link(g, a, b):
    g.setdefault(a, set()).add(b)
    g.setdefault(b, set()).add(a)

def chain(n):   # hub 0, then 1-2-...-n in a line
    g = {}
    for i in range(n):
        link(g, i, i + 1)
    return g

def ring(n):    # the chain plus one link from n back to the hub
    g = chain(n)
    link(g, n, 0)
    return g

def star(n):    # every destination one link from the hub
    g = {}
    for i in range(1, n + 1):
        link(g, 0, i)
    return g

def errand_cost(g, L):
    d = distances(g, 0)
    dests = [v for v in g if v != 0]
    return 2 * L * sum(d[v] for v in dests) / len(dests)

L = 100
for n in (4, 8, 16):
    print(n, [round(errand_cost(f(n), L)) for f in (chain, ring, star)])
```

It prints:

```
4 [500, 300, 200]
8 [900, 500, 200]
16 [1700, 900, 200]
```

Open the interactive. The left panel draws the world as nodes and links, with the hub in the centre. The right panel plots `E` against `n` for all three layouts. Drag the `n` slider from 2 to 20. The chain's line climbs steadily, the ring climbs at half the rate, and the hub's line doesn't move. Then switch the left panel to "chain" and click the far end and the hub to add a link between them. The chain becomes a ring, and its line on the right drops to the ring's.

### One link is worth half the walking

That last move deserves a second look. Going from chain to ring costs you one link. It is one path, one door, one elevator. For `n = 8` it cuts the mean errand from 900 to 500 metres, a 44% cut, and for large `n` the saving approaches half. No other single link you could add to a chain saves as much, because it is the only one that brings the far end close to home.

This is why level designers love the **loop-back shortcut**: a path that opens at the far end of an area and drops the player next to where they started. Week 7 took one such shortcut in Dark Souls apart as an edge-time problem. The topology view explains why one link has such a large effect. It turns the chain's worst destinations into its best ones.

You will use this in the lab: given a chain-shaped zone and a list of possible shortcuts, find the one that minimizes `E`. The best one is usually the link that joins the node farthest from the hub back to it.

### Cross-game recognition

**Super Mario 64 (1996).** The castle is the hub, each painting a spoke. The game resets you to the hub after almost every star, so the errand is literally built into its rules. You land in the room that holds the painting you jumped into, so the trip to the next course is a walk across the castle, never back through a course. `E` stays close to `2L` for the whole game, even as the number of open courses grows from one to fifteen. The design spends its variety inside the spokes and keeps the commute flat.

**World of Warcraft (quest hubs, 2004 onward).** A levelling zone is a set of small hubs, usually a town with an inn, a flight master and a cluster of quest givers. Quests send you out along spokes to kill or collect something and back to hand in. The game also sells the player a shortcut home: the Hearthstone, an item that teleports you to the inn you bound it to. Since patch 3.1.0 (April 2009) its cooldown has been 30 minutes. In our model, the Hearthstone sets the return leg of one errand to nearly zero, but only one errand in every half hour. It turns `E` into `d(h, i) × L` for that trip and leaves the rest at full price. A cooldown on the shortcut is the designer deciding how much of the commute to keep.

**Dark Souls (FromSoftware, 2011).** Firelink Shrine is the hub, with paths leading up to the Undead Burg, down to New Londo Ruins and the Catacombs, and on to other areas. For the first part of the game there is no fast travel. You reach every destination on foot and every errand costs its full walk. After you defeat Ornstein and Smough in Anor Londo, Princess Gwynevere gives you the Lordvessel, which lets you warp between bonfires you have rested at. At that moment every bonfire becomes one link from every other. The whole world turns into a hub-and-spoke graph with `E ≈ 0` for travel. The game holds that change back on purpose. The early game's long, one-way walks and hard-won shortcuts are the experience, and the warp arrives when the world has been learned.

Three games, three uses of the same number. Mario keeps `E` flat from the start. WoW keeps `E` at spoke length and sells a limited discount. Dark Souls starts with chain-like errands and hands you a hub later as a reward.

### Design judgment, eyes open

The hub's flat line looks like a free win. It isn't. Here is what it costs.

- **Hubs remove the journey.** In a chain, getting to destination 6 means passing 1 to 5. In a hub, destinations never touch each other. If you want players to see an earlier area change, or to pass a landmark on the way to the next goal, a pure hub prevents it. Look at the pairwise distance too: the mean distance between two *destinations*. In the hub it is always `2L`, because you must pass through the centre. In a chain of eight the mean is 300 metres, but neighbours are only 100 metres apart, so nearby places feel like parts of one region. Worlds that want destinations to feel like one place join spokes at their far ends.
- **Hubs concentrate traffic.** Every errand passes through one place. In a single-player game that is fine. In a persistent world, the hub is where every player on the server stands between quests. Next week measures what that density does to a space.
- **Hubs need a reason to return.** If nothing at the hub matters (no shop, no save, no new quest), players stop returning and the "hub" is just a crossroads. Mario forces the return by rule. Most games earn it with services.
- **Chains aren't wrong.** A chain gives you total control of order and pacing, which week 3's intensity graphs need. Use a chain when order matters more than freedom and when errands are rare. The chain's cost only hurts when the player must go back.

The deliberate decision is how often your player runs errands and how long you want each to take. If a player returns to the hub every five minutes, a 150-second commute is a third of their time. If they return once an hour, it doesn't matter.

## 3. Gating: deciding when a spoke opens

A hub offers many spokes. Most games don't open them all at once. They put **gates** on some, and the player's progress opens them. Gating gives you back some control over order, which the hub took away.

### Kinds of gate

- **Key gates.** A specific item opens a specific door. The player must visit the key's location first, so a key gate turns two spokes into a short chain. Super Mario 64's basement is locked until you take a key from Bowser at the end of his first course, and a second key from his second course opens the upper floors.
- **Count gates.** A door opens when the player holds enough of a collectible, from anywhere. Super Mario 64's star doors are count gates: its smaller star doors ask for 1 or 3 stars, and its Big Star Doors ask for 8, 30 and 50, with 70 stars needed before the final staircase stops looping.
- **Ability gates.** A path needs a verb the player doesn't have yet: a double jump, a swim upgrade, a grapple. The player sees the gap long before they can cross it, and later remembers it. Week 5's affordances do the signposting.
- **Level and stat gates.** Common in MMOs. Nothing physically blocks the path, but the monsters beyond it will kill an under-levelled player. The gate is soft: skilled or lucky players can slip through.

### Gate slack

A count gate asks "how many of the available things must you have done?" If the answer is "all of them", the gate forces completion. If it is "half", the player can skip what they dislike. Put a number on that.

The **slack** of a count gate is the amount available before the gate divided by the amount the gate requires:

```
slack = available / required
```

- `available` is the number of collectibles the player can earn using only spokes that are open before this gate.
- `required` is the gate's threshold.

Slack of 1.0 means the player must do everything open to them. Slack of 2.0 means they can skip half. The inverse, `required / available`, is the fraction of the open content the gate forces.

Super Mario 64's final requirement is 70 of 120 stars, so a player finishing the game has done 58% of its stars and could skip 50. The final gate has a slack of about 1.7 over the whole game, which is a large part of why players remember choosing what to do next.

Now a teaching hub of our own. It has five spokes, A to E, with 10 tokens in each. A is open from the start. The other four are behind count gates, and a final boss door needs 40.

| Gate | Opens | Required | Available before it | Slack | Fraction forced |
|---|---|---|---|---|---|
| 1 | Spoke B | 5 | 10 (A) | 2.00 | 50% |
| 2 | Spoke C | 15 | 20 (A, B) | 1.33 | 75% |
| 3 | Spoke D | 25 | 30 (A to C) | 1.20 | 83% |
| 4 | Spoke E | 35 | 40 (A to D) | 1.14 | 88% |
| Boss | Final door | 40 | 50 (A to E) | 1.25 | 80% |

Read the slack column. It falls from 2.0 to 1.14 across the first four gates. Early on the player chooses. By gate 4 they must clear 35 of the 40 tokens they can reach, which means nearly every token in every open spoke, including the ones behind the challenge they hate. The designer probably meant this as a steady staircase (5, 15, 25, 35 looks even). The slack column shows it is a squeeze.

Two fixes, both deliberate:

- **Keep the ratio, not the gap.** Set each threshold to about 60% of what is available: 6, 12, 18, 24 and a boss door at 30. Slack stays near 1.67 at every gate.
- **Add content faster than thresholds.** Keep the thresholds but put 15 tokens in later spokes. Slack rises again as the game goes on.

Either way, you compute slack before you ship, because players experience it as either "I can skip this" or "I have to grind this", and they notice the difference within the first hour.

### Gates change the errand model

A gate removes spokes from the graph until it opens. In the hub model, that doesn't change `E` for the spokes that are open, which is a strength: a new spoke appearing at the hub costs nothing extra to reach. A key gate is different. If the key for spoke C lies at the far end of spoke A, then a player who needs C runs an errand to A first. The effective errand to C becomes `2L + 2L = 4L`. Key gates add errands, so place keys near the doors they open or at the end of a spoke the player wanted to finish anyway.

## 4. Hubs in persistent worlds

MMO zones mix all three topologies at different scales. A continent is often a chain of zones in level order, each one a gated spoke (by level) from the one before. Inside a zone, the quest hub is a hub-and-spoke system: a town with spokes to the monster camps around it. A player moves the whole hub forward as they level, trading one town for the next.

Three things are different from a single-player hub.

**Many players share one hub.** The hub is the densest place in the zone, because every errand passes through it. That is good for the social side (you see other players, you form groups) and bad for performance and for anything scarce there. Week 11 builds the density model for this.

**Travel is a system with prices.** Persistent worlds sell errand shortcuts: bind points with cooldowns, flight networks that cost currency, teleports tied to progress. Each one changes `E` for some trips at some price. Treat every travel feature as a change to the graph. Ask which links it adds, for whom, and how often.

**Gates are shared by everyone.** A key gate in a single-player game is a puzzle. In an MMO, level gates decide where players at different levels can meet. A zone that is gated too hard splits friends of different levels. Guild Wars 2 answers this by scaling players down: a level 50 character in a level 10 area fights with the attributes of a level 11 character. High-level players can return to low zones with friends and still face a challenge. That trades some gate control for social contact.

## In-class activity (25 minutes)

In groups of three, with squared paper and the interactive.

1. **(5 min)** Draw a hub with six destinations. Arrange them as a chain, then as a hub and spoke. Compute `E` for both with `L = 80` m by hand.
2. **(8 min)** Your producer says the chain version "has better flow" and wants to keep it. Add exactly two links to the chain to bring `E` as close as possible to the hub version. Record the new `E`. Check it in the interactive's custom mode.
3. **(7 min)** Add three count gates to your hub with thresholds of your choice, 12 tokens per spoke. Compute slack at each. Adjust until no gate forces more than 75%.
4. **(5 min)** Swap with another group. Find the errand in their layout that costs most, and say what single change you would make.

Expected output: two `E` values and the improved one, a slack table, and one change proposed by the other group.

## Common misconceptions

- **"Hubs are for small games."** The hub's cost doesn't grow with the number of destinations, so it scales best of the three. Large worlds use nested hubs (a hub of hubs) for exactly that reason.
- **"Backtracking is always bad."** Backtracking is only as bad as its cost and its repetition. A 30-second walk past things that have changed is content. A 5-minute walk past things that haven't is a tax. Measure `E` and count the errands.
- **"An even staircase of thresholds is fair."** Thresholds 5, 15, 25, 35 look even, but slack is a ratio to what is available, and it can fall at every gate. Compute slack, not gaps.
- **"Fast travel makes layout irrelevant."** Fast travel changes `E`, often to near zero for some trips. The layout still sets the cost of first visits and of every trip fast travel doesn't cover, and the designer still chooses when fast travel arrives.

## Check yourself

1. A chain has 12 destinations with `L = 80` m and the hub at one end. What is `E`? What would it be as a hub and spoke? How many seconds does one errand save at 6 m/s?
2. You add one link from destination 12 back to the hub of the chain in question 1. What is the new `E`? What fraction of the chain's errand cost did one link remove?
3. A hub has four spokes of 8 tokens each. A is open. Gates for B, C and D need 4, 10 and 18 tokens, and the final door needs 24. Compute the slack at every gate. Which gate is the tightest?
4. A WoW-style quest hub sends players on errands to camps 300 m away, at 7 m/s, and a return-home item with a 30-minute cooldown. A player runs one errand every 4 minutes. What fraction of their return legs does the item remove, and how much walking does that save per hour?

<details>
<summary>Answers</summary>

1. Chain: `E = L × (n + 1) = 80 × 13 = 1,040` m. Hub: `2L = 160` m. The difference is 880 m, which is about 146.7 seconds per errand.
2. It becomes a ring with `n = 12`: `E = L × (n + 2) / 2 = 80 × 7 = 560` m. It removed `(1,040 − 560) / 1,040 ≈ 46%` of the errand cost.
3. Gate B: 8 available / 4 = 2.0. Gate C: 16 / 10 = 1.6. Gate D: 24 / 18 = 1.33. Final: 32 / 24 = 1.33. Gates D and the final door tie as the tightest, each forcing 75% of what is open.
4. In an hour the player runs 15 errands and can use the item twice (at minute 0 and minute 30). That removes 2 of 15 return legs, about 13%. Each return leg is 300 m, so the item saves 600 m per hour, about 86 seconds at 7 m/s. The cooldown keeps most of the commute in place.

</details>

## Lab / assignment hook

[Lab 10, errand costs and shortcut placement](../labs/lab10.md). You implement the errand model on weighted graphs, find the best single shortcut for a chain-shaped zone, and compute slack for a gated hub. You then redesign your final-zone blockout's connections and justify them with `E` and slack. This feeds the final greybox zone.

## Sources

- Super Mario Wiki, "Super Mario 64" (accessed September 2026). 120 Power Stars; 70 needed to complete the game; fifteen main courses and nine secret courses; the castle is a hub with paintings as portals; collecting a star returns Mario to the room he came from, except for 100-coin stars.
- Super Mario Wiki, "★ door" and "Big Star Door" (accessed September 2026). Star doors at 1 and 3 stars; Big Star Doors at 8, 30 and 50 stars in Super Mario 64 (N64, 1996); the final staircase loops endlessly with fewer than 70 stars.
- Warcraft Wiki, "Hearthstone" (accessed September 2026). Cooldown reduced to 30 minutes in patch 3.1.0 (14 April 2009).
- Dark Souls Wiki (Fextralife), "Lordvessel" and "Firelink Shrine" (Dark Souls, 2011; accessed September 2026). The Lordvessel is received from Gwynevere in Anor Londo after Ornstein and Smough, and grants warping between bonfires; Firelink Shrine connects to the Undead Burg, New Londo Ruins and the Catacombs.
- Guild Wars 2 Wiki, "Dynamic level adjustment" (accessed September 2026). In PvE a character is scaled down to the area's maximum level plus one, for example a level 50 character in a level 10 area plays as level 11.
- Super Mario Wiki, "Key" (accessed September 2026). Two Big Keys in Super Mario 64, one from each of the first two Bowser courses; the first opens the basement, the second the upper floors.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.

## Interactive spec: examples/w10-hub-errands.html

**Purpose.** Make the student see that errand cost grows with world size in a chain, grows at half the rate in a ring, and stays flat in a hub, and that one loop-back link turns a chain into a ring.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (graph first).

- **Left panel, the world.** SVG node-link drawing. The hub is a larger circle labelled "Hub". Destinations are small numbered circles. Layouts:
  - Chain: hub at left, destinations in a line (wrap into a zigzag if `n > 10` so it fits at 390 px).
  - Ring: nodes on a circle, hub at the top.
  - Hub and spoke: hub in the centre, destinations evenly around it.
  - Custom: starts as the chain. Clicking one node then another toggles a link between them (keyboard: Tab to a node, Enter to select, Tab to a second node, Enter to toggle). A "Reset links" button restores the chain.
  - Each destination node shows its distance label `d(h, i)` in links. Hovering or focusing a node highlights its shortest path to the hub.
- **Right panel, the cost.** Line chart of `E` (y-axis, metres, with a secondary label in seconds at speed `v`) against `n` (x-axis, 2 to 20). Three lines: chain, ring, hub. A fourth line for the custom graph appears only in custom mode, computed for the current `n` only (a single marker, since custom links are not defined for other `n`). A vertical marker shows the current `n`.
- **Readout (below both panels).** For the current layout: `n`, `Σ d(h, i)`, mean distance in links, `E` in metres, `E / v` in seconds, and the total walking for one errand per destination (`n × E`). Also show the pairwise mean distance between destinations (average of `d(i, j) × L` over distinct pairs).

**Controls.**
- Layout selector (radio buttons): Chain, Ring, Hub and spoke, Custom. Default: Chain.
- `n` slider 2 to 20, step 1, default 8.
- `L` slider 20 to 200 m, step 10, default 100.
- `v` slider 2 to 12 m/s, step 1, default 6.
- "Add loop-back" button (chain only): adds the link from node `n` to the hub, switches to Custom and animates the new link (no animation under `prefers-reduced-motion`).

**Formulas.** Compute all distances by BFS on the current graph (do not hard-code the closed forms). `E = (2 / n) × Σ d(h, i) × L`. Pairwise mean `= L × mean over i < j of d(i, j)`.

**Test values** (`L = 100`, `v = 6`):
- Chain, `n = 8`: `Σ d = 36`, `E = 900` m, 150.0 s. Pairwise mean 300 m.
- Ring, `n = 8`: `Σ d = 20`, `E = 500` m, 83.3 s. Pairwise mean 250 m.
- Hub, `n = 8`: `Σ d = 8`, `E = 200` m, 33.3 s. Pairwise mean 200 m.
- Chain `n = 16`: `E = 1,700` m. Ring `n = 16`: `E = 900` m. Hub any `n`: 200 m.
- Chain `n = 8` plus loop-back gives exactly the ring values.
- `L = 80`, chain `n = 12`: `E = 1,040` m; with loop-back `E = 560` m (check-yourself questions 1 and 2).

**The one insight.** With the default chain on screen, the first thing a student does (drag `n` up) must show the chain line climbing while the hub line stays flat, and the "Add loop-back" button must visibly drop the chain's cost to the ring line.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Lines distinguished by colour and by dash pattern. All controls keyboard reachable. Numbers in the readout use tabular figures so they can be copied into the lecture table.
