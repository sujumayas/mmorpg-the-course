# MMO302 · Week 03 — Area of interest: grids, radius, hysteresis

**Why this matters:** A player in an MMO needs to hear about the few dozen things near them, not the thousands in the world. The code that decides "who hears about whom" is called area of interest, and it is the difference between week 1's square law and a server that grows in a straight line. It also has limits. When players crowd together, no interest scheme can save you, and a careless one makes characters flicker in and out at the edge of sight. This week you build it, measure it and learn exactly where it stops helping.

**You will be able to:**
- Compute the deliveries per tick for broadcast-to-all, exact-radius and grid-based interest management, and predict the grid's over-send factor from cell size and view radius.
- Explain, with numbers, why grid interest management turns `N²` into `N × density`, and why that saving disappears as players cluster.
- Implement a uniform grid (a spatial hash) with a 3 × 3 neighbourhood as a broad phase and an exact radius test as a narrow phase.
- Design enter and leave radii with hysteresis, and compute the spawn-message size at which hysteresis also saves bandwidth.

**Before class:** Epic Games, "Replication Graph" (Unreal Engine documentation), the overview section. CCP Games, "Grid Sizes & You" (EVE Online news, 8 December 2015), the whole post. Skim the comments at the top of `SpatialHashingInterestManagement.cs` in the Mirror networking library (GitHub, MirrorNetworking/Mirror, master branch).

**Prerequisites from earlier courses:** [MMO302 week 1](w01-scale-targets-ccu-messages-and-n-squared.md) (deliveries `u × Σ g(g − 1)` and the crowd ceiling). [MMO302 week 2](w02-shards-realms-zones-instances-layers.md) (layers split a crowd by copies; this week splits it by space). [CS102 week 5, hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (a grid keyed by cell coordinates is a hash map). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the interest cap `K` and the priority accumulator for when a crowd still does not fit).

**Interactive:** [examples/w03-aoi-grid-vs-broadcast.html](../examples/w03-aoi-grid-vs-broadcast.html). Keep it open during sections 2 and 4.

---

## 1. Who needs to hear about whom

Every tick, the server changes the state of many entities: players move, monsters attack, doors open. For each change it must decide which clients to tell. The rule that decides is **area of interest (AOI)**, also called **interest management** or **relevance**. The set of clients told about an entity are that entity's **observers**. The set of entities a client hears about is that client's **interest set**.

Three rules cover most games.

- **Broadcast to all.** Every change goes to every client in the zone. Simple and correct, and the cost is week 1's `N(N − 1)` deliveries per update round.
- **Radius.** A client hears about an entity if it is within distance `r`. This matches what a player could see. Computing it naively means checking every pair, `N(N − 1)` distance tests, even when few pairs are close.
- **Grid.** Cut the world into square **cells** of side `c`. Each entity lives in one cell. A client hears about everything in its own cell and the eight cells around it, the **3 × 3 neighbourhood**. Finding the neighbours costs 9 cell lookups instead of `N` distance tests.

A grid stored as a hash map from cell coordinates to the entities in that cell is called a **spatial hash**. Building it costs one insert per entity. Asking "who is near me" costs nine lookups plus the entities found. That is why engines use it.

Two properties of the grid matter below. First, if `c ≥ r`, every entity within `r` of you is somewhere in your 3 × 3 neighbourhood, so the grid never misses anything the radius rule would include. Second, the neighbourhood is a square of side `3c`, much bigger than a circle of radius `r`. So the grid **over-sends**. It tells you about some entities outside your radius.

## 2. Worked example: broadcast versus grid as the crowd gathers

### The hook

Epic's documentation for Unreal Engine's Replication Graph opens with a number. A Fortnite Battle Royale match starts with 100 connected players and about 50,000 replicated actors, and Unreal's default approach of asking every actor about every connection does not scale to that. Epic's fix is to put actors into grid cells, so each client is handed the list for the cells around it.

EVE Online went the other way in December 2015. CCP made its "grid", the volume in which everyone sees everyone, 32 times wider, from 250 km to 8,000 km across. Bigger cells mean more entities per cell. So one engine shrank its interest regions and the other grew them. To see why both can be right, you need to count deliveries and watch what happens when players stop spreading out.

### The model

`N` players stand in a square world of side `W`. Each tick, every player's state changes once, so each player produces one update per tick. An update is delivered to each of the player's observers.

```
broadcast:  D_b = N × (N − 1)
radius:     D_r = Σ_i (number of other players within r of i)
grid:       D_g = Σ_i (number of other players in the 3 × 3 cells around i)
```

These are deliveries per tick. Multiply by the tick rate for deliveries per second.

If players are spread uniformly, the density is `ρ = N / W²` players per square metre, and the expected counts are:

```
D_r ≈ N × ρ × π r²          (the area of the circle)
D_g ≈ N × ρ × 9 c²          (the area of the 3 × 3 square)
```

Both are `N × density × area`. If you add players by making the world bigger, density stays fixed and cost grows as `N`. If you add them to the same world, density grows with `N` and cost grows as `N²` again. The grid does not remove the square. It replaces one factor of `N` with the number of players nearby.

The **over-send factor** of a grid with `c = r` is the ratio of the two areas, `9c² / (π r²) = 9 / π ≈ 2.86`.

### Numbers you can check

Take `N = 1,000` players in a world with `W = 1,000` m, a view radius `r = 50` m and cells of `c = 50` m, so the world is 20 × 20 cells. A fraction `f` of the players crowd into a disc of radius 20 m at the centre of the map (a market square, a world boss). The rest are scattered uniformly. The positions come from a seeded generator (mulberry32 with seed 302, given in the spec and the lab), so your numbers will match exactly.

For the uniform case, the formulas predict `D_r ≈ 1,000 × 0.001 × π × 2,500 ≈ 7,850` and `D_g ≈ 1,000 × 0.001 × 9 × 2,500 = 22,500`. The simulation counts come out slightly lower, because players near the map edge have fewer neighbours.

| Crowd share `f` | Broadcast | Grid (3 × 3, `c = 50`) | Radius (`r = 50`) | Broadcast ÷ grid | Grid ÷ radius |
|---|---|---|---|---|---|
| 0% | 999,000 | 21,000 | 7,474 | 47.6 | 2.81 |
| 10% | 999,000 | 29,826 | 17,138 | 33.5 | 1.74 |
| 25% | 999,000 | 80,152 | 69,026 | 12.5 | 1.16 |
| 50% | 999,000 | 258,670 | 252,512 | 3.9 | 1.02 |
| 75% | 999,000 | 564,926 | 562,266 | 1.8 | 1.00 |
| 100% | 999,000 | 999,000 | 999,000 | 1.0 | 1.00 |

Check the last row by hand. With every player inside a disc 40 m across, every pair is within 50 m and within the same 3 × 3 block of cells, so all three rules give `1,000 × 999`. Check the 50% row roughly. The 500 crowded players each see the other 499, which is `500 × 499 = 249,500`. The scattered 500 add a little, and a few of them near the centre also see the crowd. The table's 252,512 and 258,670 are just above that.

Read the table from top to bottom.

- **Spread out, the grid is 48 times cheaper than broadcast.** 21,000 deliveries instead of 999,000. At 10 ticks per second that is 210,000 per second instead of about 10 million, the difference between one core and ten.
- **The grid over-sends by the predicted factor.** 21,000 against 7,474 is 2.81, close to `9 / π = 2.86`. Edges account for the rest.
- **As the crowd grows, all three rules converge.** At 50% crowding the grid saves only a factor of 3.9 over broadcast. At 100% it saves nothing. The crowd's cost is `g(g − 1)` whatever rule you use, because inside a crowd everyone really is near everyone.
- **The over-send vanishes in a crowd.** Grid ÷ radius drops from 2.81 to 1.00. When everyone is close, the square and the circle contain the same people.

That is the whole lesson in one table. Interest management is an enormous win for a spread-out world and no win at all for a crowd. Week 1's crowd fixes (fewer updates, time dilation, copies) are still needed. AOI decides how much of the world is a crowd.

### What the grid costs to compute

Deliveries are not the only cost. Deciding who is near whom also takes CPU.

- **Brute-force radius** does `N(N − 1)` distance tests every rebuild, 999,000 tests at `N = 1,000`, whether players are spread or not.
- **Grid** does `N` inserts to build the hash, then for each player 9 lookups and a scan of the entities found. When spread out, that is about `9 × 1,000 = 9,000` lookups plus 21,000 entities scanned.

So a grid wins twice when players are spread, once on deliveries and once on the work to find them. You can have both the grid's cheap search and the radius's exact answer. Use the grid as a **broad phase** to find candidates, then test the exact distance as a **narrow phase** and deliver only to those within `r`. The candidates scanned are the grid's 21,000, but the deliveries are the radius's 7,474. The lab builds this and checks that its answer matches brute force exactly.

### Choosing the cell size

The cell size `c` trades lookups against over-send. With `c = r` you need the 3 × 3 block. With `c = r / 2` you need a 5 × 5 block to guarantee coverage, and with `c = r / 3` a 7 × 7 block.

| Cell size | Block | Cells looked up | Block side | Over-send vs circle | Uniform-world grid count |
|---|---|---|---|---|---|
| `r` = 50 m | 3 × 3 | 9 | `3r` | 2.86 | 21,000 |
| `r / 2` = 25 m | 5 × 5 | 25 | `2.5r` | 1.99 | 14,690 |
| `r / 3` = 16.7 m | 7 × 7 | 49 | `2.33r` | 1.73 | 12,788 |

Smaller cells approach the circle, but never reach it (the limit of a square block around a circle is `4 / π ≈ 1.27`), and cost more lookups. With a narrow phase, over-send only costs candidate scans, not deliveries, so `c = r` with a 3 × 3 block is the usual starting point. Measure before you tune.

### Move it yourself

Open `examples/w03-aoi-grid-vs-broadcast.html`. The left view is the map: 1,000 dots, the 20 × 20 grid lines, one highlighted player with its 3 × 3 block shaded and its radius circle drawn. The right view plots deliveries per tick against crowd share, with three lines (broadcast flat at the top, grid and radius rising to meet it) and a marker at the current share. Start at 0%. The highlighted player's block holds a handful of dots. Drag the crowd slider to 50%. On the map, dots rush to the centre. On the chart, the grid line climbs toward broadcast. Click a player inside the crowd to highlight it and read its interest set in the readout, about 500. Then click one far from the centre, where the set holds a handful. Same rule, different density.

### The same idea in other games

**Unreal Engine's Replication Graph (Epic Games, current documentation).** Epic describes grouping actors by location, with the world divided into grid cells for battle royale, MOBA or MMO maps, or into predefined rooms for corridor games. Each actor is added to every cell from which it could be seen or heard. The client then gets the persistent list for its cell. In our terms, Epic moved work from the per-client query to the per-actor insert, which is the grid's broad phase. Fortnite's 100 players and 50,000 actors make the naive `actors × connections` check 5 million per frame, which is why Epic built it.

**Mirror for Unity (open source, master branch, accessed September 2026).** Mirror's `SpatialHashingInterestManagement` component uses a 2D grid and the 9 cells around the player. Its source sets the cell size to half the visibility range (`resolution = visRange / 2`), with a default range of 30 units, and rebuilds all observer sets once per second by default. The source comments credit the approach to the uMMORPG project's grid checker. Mirror also ships a plain `DistanceInterestManagement` that tests exact distance, with a default range of 500. Two choices from our model are visible here. The grid's exact coverage depends on the cell-to-range ratio, and observer sets are rebuilt far less often than the game ticks, which is a separate lever on CPU.

**EVE Online grids (CCP, 2015 change).** EVE's grid is a coarse interest region, not a view radius. CCP's 2015 post explains that a solar system is divided into grids based on where players and objects are, and that anyone in the same grid sees everyone else in it. The EVE University wiki adds that grids have fixed boundaries, are created and resized as ships move, and that the grid around the Jita 4-4 trade hub reaches about 20,000 km in each direction. In our model a grid is a single cell with no neighbourhood, so its cost is `g(g − 1)` for everyone inside. CCP made grids 32 times wider in December 2015 to fit new large structures and to stop fast ships from appearing out of nowhere. That trade increases `g` for everyone near a busy location. The old 250 km grids had another problem. Their boundaries could be pushed around by players, a tactic the wiki calls "grid-fu", which let fleets hide just across a grid wall. A fixed partition is also a game mechanic, and players will exploit it.

**Week 1's crowd, again.** Every one of these systems gives the same result as our table. Spread out, interest management turns `N²` into `N × (nearby players)`. Crowded, "nearby players" is `N`, and the square is back. EVE's largest battles happen on one grid, and that is why EVE needs time dilation as well as grids.

### Design judgment

- **Use a grid broad phase with an exact narrow phase by default.** It is cheap to build, easy to debug, and exact where it matters. Tune the cell size by measuring candidates scanned, not by guessing.
- **Size the view radius from gameplay, then check the crowd case.** A bigger radius increases `π r²` for every player. Doubling `r` quadruples deliveries in a spread-out world. Ask what the player needs to see. A melee game can use a small radius and a sniper game cannot.
- **Different entity types can have different radii.** A dragon or a siege tower should be seen from far away. A dropped coin needs 20 m. Unreal and Mirror both allow per-entity ranges. Each large radius adds its own `π r²` term, so spend them on things that matter to play.
- **Plan for the crowd separately.** AOI does not fix a crowd. When one interest set exceeds your per-client budget, use CS202 week 13's cap and priority accumulator, week 1's update-rate cut, or week 2's copies. Decide which before your first world event.
- **Beware fixed boundaries.** A player standing on a cell edge or grid wall can be seen by one neighbour and not another, or can exploit the edge as EVE players did. Section 4 handles the flicker. Level design handles the exploit.

### Check this example

1. With `N = 2,000` players spread uniformly in the same 1,000 m world, `r = c = 50` m, estimate grid and radius deliveries per tick, ignoring edges. How do they compare with `N = 1,000`?
2. At 20 ticks per second, how many deliveries per second does the 25% row of the table imply for the grid? How many cores is that at 1,000,000 deliveries per second per core?
3. A designer doubles the view radius to 100 m and keeps `c = r`. Estimate the new uniform grid count for `N = 1,000`.

<details>
<summary>Answers</summary>

1. Density doubles to 0.002. Radius `≈ 2,000 × 0.002 × π × 2,500 ≈ 31,400`. Grid `≈ 2,000 × 0.002 × 22,500 = 90,000`. Both are about 4 times the `N = 1,000` values, because both `N` and density doubled. Adding players to the same space is still a square.
2. `80,152 × 20 = 1,603,040` deliveries per second, about 1.6 cores.
3. `1,000 × 0.001 × 9 × 100² = 90,000`, four times as many, before edge effects.

</details>

## 3. Building a grid that stays fast

A few implementation details decide whether the grid is actually fast.

- **Key cells by integer coordinates.** `cell = (floor(x / c), floor(y / c))`. In C# a `Dictionary<(int, int), List<Entity>>` works. In Python a `dict` with tuple keys. Hash maps give constant-time lookup on average, as CS102 week 5 showed.
- **Update on move, not every tick.** When an entity moves, recompute its cell. Only if the cell changed, remove it from the old list and add it to the new one. Most moves stay in the same cell.
- **Reuse memory.** Mirror's grid never deletes empty cells and clears lists in place, so it does not allocate every tick. A server that allocates per tick spends its budget in the garbage collector.
- **Rebuild observer sets less often than you tick.** Mirror rebuilds once per second by default. The cost is lag at the edge. A fast entity can travel far between rebuilds, which is the "appearing out of nowhere" problem CCP describes. Choose the rebuild interval from the fastest entity's speed. At 10 m/s and a 1 s rebuild, an entity can come 10 m closer than the radius before anyone learns about it.
- **Separate "in view" from "update rate."** Being in someone's interest set does not mean receiving every update. Far entities can be updated every few ticks. That is the priority accumulator from CS202 week 13, applied inside the interest set.

## 4. Hysteresis: stopping the flicker

### The problem

When an entity enters a client's interest set, the server sends an **enter** (or spawn) message with the entity's full state: position, appearance, equipment, name, buffs. When it leaves, the server sends a short **leave** message and the client destroys it. Updates in between are small.

Now imagine a player pacing back and forth right at your view radius. Each step across the line is an enter or a leave. The server sends a full spawn every time, the client creates and destroys the character every time, and you see them blink in and out. This is called **flicker** or **boundary thrash**.

### The model

**Hysteresis** uses two radii. An entity enters your interest set when it comes within `r_in`, and it leaves only when it goes beyond `r_out`, with `r_out > r_in`. Between them, an entity stays in whatever state it was already in. The gap `r_out − r_in` is the **margin**.

Take a deterministic test. You stand still. Another player paces so that their distance from you is `d(t) = 50 − 4 cos(2π t / 4)` metres, swinging between 46 m and 54 m every 4 seconds. The server ticks 10 times a second for 60 seconds, 600 ticks. Messages cost 16 bytes for an update, 4 bytes for a leave, and either 120 bytes or 600 bytes for an enter (a plain character or one with full equipment appearance).

| `r_in` | `r_out` | Enters | Leaves | Ticks visible | Bytes, 120 B enter | Bytes, 600 B enter |
|---|---|---|---|---|---|---|
| 50 | 50 (no hysteresis) | 16 | 15 | 303 | 6,828 | 14,508 |
| 50 | 52 | 16 | 15 | 349 | 7,564 | 15,244 |
| 50 | 54 | 1 | 0 | 600 | 9,720 | 10,200 |
| 50 | 60 | 1 | 0 | 600 | 9,720 | 10,200 |

Check the first row. Bytes are `16 × 120 + 15 × 4 + 303 × 16 = 1,920 + 60 + 4,848 = 6,828`.

Three results.

- **A margin smaller than the jitter does nothing.** At `r_out = 52`, the pacing player still crosses 52 m every cycle, so the flicker count is unchanged (31 events). The margin must exceed how far entities wander at the edge.
- **With enough margin, flicker drops from 31 events a minute to 1.**
- **Hysteresis can cost bandwidth.** With cheap spawns (120 B), keeping the player visible all minute costs 9,720 bytes against 6,828 for the flickering version, because you now send updates for all 600 ticks. With expensive spawns (600 B), hysteresis saves 4,308 bytes.

The break-even spawn size solves `16s + 60 + 4,848 = s + 9,600`, which gives `s ≈ 313` bytes. Below that, hysteresis costs bytes and buys stability. Above it, it wins both. Most games choose hysteresis anyway, because flicker is visible and a few hundred bytes a minute is not.

The same idea applies to grid cells. An entity moving along a cell boundary would hop between cells every tick, and each hop changes which clients have it in their 3 × 3 block. Give the cell assignment a margin too. Move an entity to a new cell only once it is at least `m` metres inside it.

### Move it yourself

Switch the interactive to its "Boundary" tab. One observer, one pacing player, two concentric circles for `r_in` and `r_out`, and a timeline strip that marks each enter and leave. Drag `r_out` from 50 up to 60. The strip is full of marks until the margin passes the pacing amplitude, then it goes quiet. Change the spawn size and watch the bytes readout cross over at about 313.

## In-class activity (25 minutes)

Pairs. You are designing interest management for a city hub where up to 600 players stand in a 200 m × 200 m plaza on event nights, and the rest of the zone (2 km × 2 km) holds another 400 spread out.

1. Choose a view radius and cell size and justify each in one sentence.
2. Estimate the grid deliveries per tick for the spread-out 400 (use `N × ρ × 9c²`) and for the plaza (assume every plaza player sees every other).
3. The plaza's number will not fit your budget of 50,000 deliveries per tick. Choose a fix from this week or weeks 1 and 2 and compute the new number.
4. Pick an `r_out` for hysteresis given that players in a crowd shuffle about 3 m back and forth.

Expected output: radius, cell size, two delivery estimates, your fix with its new number, and `r_out`, on one card.

## Common misconceptions

- **"Interest management removes the `n²` problem."** It removes it for spread-out players. In a crowd everyone is near everyone and the cost is the crowd's `g(g − 1)` whatever rule you use.
- **"A grid is less accurate than a radius."** A grid with `c ≥ r` and a 3 × 3 block never misses anyone in range. It includes extras, and a narrow-phase distance test removes those.
- **"Smaller cells are always better."** They reduce over-send and increase lookups. With a narrow phase, over-send only costs candidate scans.
- **"Hysteresis always saves bandwidth."** It removes flicker. It saves bytes only when spawn messages are larger than the extra updates it causes, about 313 bytes in the lecture's example.

## Check yourself

1. In a uniform world with `ρ = 0.004` players per square metre and `r = c = 30` m, how many other players does each player hear about with a grid, and with an exact radius?
2. A crowd of 400 stands inside a disc of radius 20 m, with `r = c = 50` m. What are its deliveries per tick under broadcast, grid and radius, counting only the crowd? Why are they equal?
3. A game uses `r_in = 40` m. Entities at the edge jitter by up to 3 m. What is the smallest safe `r_out`, and what would you choose?
4. In the hysteresis table, with a 250-byte enter message, which policy uses fewer bytes over the minute, `r_out = 50` or `r_out = 60`?
5. An entity moves at 15 m/s and observer sets are rebuilt every 0.5 s. How far inside the view radius can it get before it appears?

<details>
<summary>Answers</summary>

1. Grid, `ρ × 9c² = 0.004 × 8,100 = 32.4`. Radius, `ρ × π r² = 0.004 × 2,827 ≈ 11.3`.
2. `400 × 399 = 159,600` for all three. Any two players in the disc are at most 40 m apart, so every pair is within the radius. A 40 m disc spans at most two cells in each direction, so every pair is also inside each other's 3 × 3 block.
3. At least `r_out > 43` m. Choose some safety margin, for example 45 m or 48 m.
4. `r_out = 50`: `16 × 250 + 60 + 4,848 = 8,908`. `r_out = 60`: `250 + 9,600 = 9,850`. The flickering policy uses fewer bytes, as expected below the 313-byte break-even.
5. `15 × 0.5 = 7.5` m.

</details>

## Lab / assignment hook

[Lab 03, build interest management](../labs/lab03.md). You implement a spatial-hash grid with a broad phase and an exact narrow phase, check it against brute force on the lecture's seeded worlds, reproduce the table, time both methods at 1,000 and 5,000 players, and implement hysteresis and reproduce section 4's event counts. Deliverable: the finished `aoi.py`, the reproduced tables, a timing plot and a one-page interest design for the in-class hub.

## Sources

- Epic Games, "Replication Graph" (Unreal Engine documentation, current as of September 2026). Fortnite Battle Royale with 100 players and about 50,000 replicated actors, the cost of default per-actor-per-connection relevance, grid cells or rooms as spatial groups, actors added to each cell from which they can be seen or heard.
- MirrorNetworking, Mirror (GitHub, master branch, accessed September 2026). `SpatialHashingInterestManagement.cs` (9-cell neighbourhood, `resolution = visRange / 2`, default `visRange` 30, rebuild interval 1 s, credited to uMMORPG's grid checker), `Grid2D.cs` (cells never deleted, lists cleared in place), `DistanceInterestManagement.cs` (exact distance, default range 500).
- CCP Games, "Grid Sizes & You" (EVE Online news, 8 December 2015). Solar systems divided into grids, everyone in a grid sees everyone in it, base grid increased 32 times from 250 km to 8,000 km across, fast ships appearing suddenly because of the interval between physics and interest updates.
- EVE University Wiki, "Grid" (accessed September 2026). Fixed grid boundaries created and resized as objects move, Jita 4-4 grid of about 20,000 km in each direction, grid manipulation ("grid-fu") under the old 250 km grids.
- EVE University Wiki, "Time dilation" (accessed September 2026). Server load `O(n²)` in players on grid.

## Interactive spec: examples/w03-aoi-grid-vs-broadcast.html

**The one insight.** A grid makes interest management 48 times cheaper than broadcast when players are spread out, and that saving collapses to nothing as they crowd together. The chart's grid line climbs to meet the flat broadcast line as the crowd slider moves right.

**Two tabs.** "Crowd" (the signature example, default) and "Boundary" (hysteresis).

**Random generator (must match the lab exactly).**
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;
  let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;
  return((t^t>>>14)>>>0)/4294967296}}
```
Seed 302 gives first three values 0.835469, 0.983486, 0.200036.

**World generation (exact).** `N` players, world side `W = 1000`, crowd disc centre (500, 500), crowd radius `R = 20`. `k = Math.round(f × N)`. One generator seeded 302, drawn in order. For `i < k`: `rr = R × √rnd()`, `th = 2π × rnd()`, position `(500 + rr cos th, 500 + rr sin th)`. For `i ≥ k`: `(W × rnd(), W × rnd())`. Regenerate from scratch whenever `N` or `f` changes, so each setting is reproducible.

**Counts (per tick, one update per player per tick).**
- Broadcast `N(N − 1)`.
- Radius: ordered pairs `i ≠ j` with squared distance `≤ r²`.
- Grid: `cell = (Math.floor(x / c), Math.floor(y / c))`; for each player, sum of counts in the 3 × 3 block around its cell, minus 1.
- Readouts: the three counts, broadcast ÷ grid, grid ÷ radius, deliveries per second at the chosen tick rate, and the highlighted player's interest-set size under grid and radius.

**Crowd tab layout.** Left: square map canvas with dots, faint 20 × 20 grid lines, the highlighted player (default: player index `N − 1`, a scattered one; click or keyboard-select any dot to change), its 3 × 3 block shaded and its radius circle outlined. Right: line chart of deliveries per tick (log y axis, 1,000 to 1,000,000) against `f` (0 to 100%), with three series computed at `f` = 0, 5, 10, … 100% on load for the current `N`, `r`, `c`, and a vertical marker at the current `f`. Stack vertically below 700 px.

**Crowd tab controls.** Crowd share `f` slider (0 to 100%, step 1%; default 0%), `N` (250, 500, 1,000, 2,000; default 1,000), view radius `r` (25 to 100 m, step 5; default 50), cell size `c` (select "= r", "= r/2 (5 × 5)", "= r/3 (7 × 7)"; for the finer options the block widens to 5 × 5 or 7 × 7), tick rate (1, 10, 20 Hz; default 10), a "narrow phase" checkbox that, when on, shows grid-with-narrow-phase deliveries (equal to radius) and candidates scanned (equal to the grid count).

**Crowd tab test values** (`N = 1000`, `r = c = 50`, 3 × 3):
- `f = 0`: broadcast 999,000; grid 21,000; radius 7,474; ratios 47.6 and 2.81.
- `f = 10%`: 999,000; 29,826; 17,138.
- `f = 25%`: 999,000; 80,152; 69,026.
- `f = 50%`: 999,000; 258,670; 252,512.
- `f = 75%`: 999,000; 564,926; 562,266.
- `f = 100%`: 999,000 for all three.
- `f = 0` with `c = 25` (5 × 5): 14,690; with `c = 50/3` (7 × 7): 12,788.

**Boundary tab (exact).** Observer at origin. Pacing distance `d(t) = 50 − A cos(2π t / P)` with amplitude `A` (default 4 m, 0 to 10) and period `P` (default 4 s). Ticks at 10 Hz for 60 s (600 ticks, `t = k / 10`). State starts outside. Each tick: if outside and `d ≤ r_in`, enter; else if inside and `d > r_out`, leave; if inside after the check, count a visible tick. Sliders for `r_in` (default 50) and `r_out` (default 50, from `r_in` to `r_in + 15`), enter size (default 120 B, 50 to 1,000), leave size 4 B, update size 16 B. Show two circles, the moving player, a 60 s timeline strip with enter and leave marks, and readouts: enters, leaves, visible ticks, total bytes, and the break-even enter size. For two settings with counts `(e1, l1, v1)` (no hysteresis, `r_out = r_in`) and `(e2, l2, v2)` (current), total bytes are `e × s + 4l + 16v`, and the break-even is `s* = (4(l2 − l1) + 16(v2 − v1)) / (e1 − e2)`, shown only when `e1 ≠ e2`.
- Test values (`A = 4`): `r_out = 50` gives 16 enters, 15 leaves, 303 visible ticks, 6,828 B at 120 B and 14,508 B at 600 B. `r_out = 52` gives 16, 15, 349, 7,564 B at 120 B. `r_out = 54` and `60` give 1, 0, 600, 9,720 B at 120 B and 10,200 B at 600 B. Break-even against `r_out = 60` is about 313 B.

**First screen.** Crowd tab, `f = 0`, with the ratio "broadcast ÷ grid = 47.6×" in large type next to the chart, and a hint arrow on the crowd slider.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Canvas has a text alternative summarising the counts; dot selection works with arrow keys cycling through players; readouts in an `aria-live="polite"` region; respect `prefers-reduced-motion` (no animated dot transitions, jump to new positions).
