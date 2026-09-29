# MMO404 · Week 03 — Spatial partitioning at scale

**Why this matters:** Week 1 showed that fixed zones overload one server while others sit idle. The obvious fix is to let the borders move, so that busy places get smaller regions and more servers. That fix works well for spread-out worlds and fails in a specific, predictable way for crowds. This week you learn to partition a world across many servers, to measure how well a partition does, and to recognise the point where cutting space stops helping.

**You will be able to:**
- Compute a partition's imbalance (busiest server over mean) and its cut (interacting pairs split across servers) from a load model.
- Derive the per-server and total load when one crowd is split across `s` servers, and find how many servers it needs.
- Compare a static grid, recursive bisection by headcount and recursive bisection by measured load, and explain each result.
- Design a rebalancing rule that moves borders without causing handoff storms.

**Before class:** De Vleeschauwer et al., "Dynamic microcell assignment for massively multiplayer online gaming" (NetGames 2005), sections 2 and 3. Reread your notes on trees from CS102 week 7 and on spatial grids from MMO302 week 3.

**Prerequisites from earlier courses:** [MMO404 week 1](w01-limits-of-the-zone-model.md) (the tick-cost model, per-player and per-pair work). [MMO404 week 2](w02-seamless-worlds-and-boundary-handoff.md) (ghosts, cross-server interaction, handoff cost). [CS102 week 7, trees](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md) (recursive structures). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (AOI with grids). [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md).

**Interactive:** [examples/w03-crowd-split.html](../examples/w03-crowd-split.html). Keep it open during section 2.

---

## 1. What a partition is, and how to grade one

A **partition** assigns every entity in the world to exactly one server, its owner. The zone model of week 1 is the simplest partition, a fixed map of regions drawn before launch. A **dynamic** partition redraws the regions while the game runs, following the players.

You grade a partition on three numbers.

- **Imbalance**, the busiest server's load divided by the mean load. A perfect partition scores 1. Players feel the busiest server, because that is where the tick overruns. A cluster with a mean load of 15 ms and a busiest server at 70 ms is broken, even though its average looks healthy.
- **Cut**, the number of interacting pairs whose two members are owned by different servers. Every cut pair needs ghosts and cross-server messages (week 2). A cut pair costs more than a pair that stays on one server.
- **Churn**, the number of entities that change owner when the partition is redrawn. Each one is a handoff, with the cost and risk from week 2.

These three pull against each other. Balance wants small regions where players are dense. Low cut wants region borders where players are sparse. Low churn wants borders that rarely move. Every partitioning scheme in this lecture is a different compromise among the three.

### The load model with cut pairs

Extend week 1's tick cost to many servers. Each server pays, per tick:

- `c_p` for each player it owns (20 µs);
- `c_i` for each neighbour of each player it owns (2 µs), whoever owns the neighbour;
- an extra `c_x` for each neighbour owned by **another** server (4 µs). This covers the ghost update, the cross-server messages for interactions, and the bookkeeping that keeps the ghost consistent.

A pair on one server costs that server `2 × c_i = 4 µs`, one for each direction. A cut pair costs each of its two servers `c_i + c_x = 6 µs`, so 12 µs in total, three times as much. De Vleeschauwer and colleagues use the same structure in their 2005 model. Their server load is a weighted sum of processing player actions, forwarding actions to neighbouring cells, receiving forwarded actions and moving players between cells, and work between cells on different servers is weighted higher than work between cells on the same server.

## 2. Worked example: you cannot split a crowd

### The hook

The Star Citizen wiki describes the promise of **dynamic server meshing**, which Cloud Imperium Games is building beyond the static version shipped in Alpha 4.0 (December 2024). If one area holds more players than one server can handle, the area is subdivided across as many servers as needed, without players noticing, whether 200 people gather there or 2,000. The same page notes that critics have called this impossible.

Both sides are partly right, and the model tells you exactly where the line is. [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) already found the warning sign. One border through a crowded city left 42% of its players ghosted on the other side, so each server still saw most of the crowd. This week prices the whole split, for any number of servers. Splitting a region works when the players in it are spread out. When every player in the region can see every other, splitting it across servers stops removing work and starts multiplying it. The question is how fast.

### The model

Take a crowd of `m` players standing close enough that everyone is in everyone's area of interest. On one server, from week 1, it costs

```
L(m, 1) = m × (c_p + c_i × (m − 1))
```

Now split it evenly across `s` servers, so each owns `k = m / s` players. Each owned player still has `m − 1` neighbours, because splitting the crowd across servers does not move anyone. Of those neighbours, `m − k` belong to other servers. So each server's load is

```
L(m, s) = k × (c_p + c_i × (m − 1) + c_x × (m − k)),   k = m / s
```

- `m` is the crowd size, `s` the number of servers, `k` the players each server owns.
- `c_p`, `c_i` and `c_x` are the per-player, per-neighbour and extra per-foreign-neighbour costs above.

The total work across all servers is `s × L(m, s)`. Compare it with `L(m, 1)` and you get the **useful share**, the fraction of the cluster's work that the crowd would have needed on one ideal server. The rest is the price of the split.

### Numbers you can check

A crowd of 300 players, the constants above, and the 50 ms tick budget from week 1:

| Servers `s` | Players each `k` | Per-server load | Total load | Useful share |
|---|---|---|---|---|
| 1 | 300 | 185.40 ms | 185.40 ms | 100% |
| 2 | 150 | 182.70 ms | 365.40 ms | 51% |
| 4 | 75 | 113.85 ms | 455.40 ms | 41% |
| 8 | 37.5 | 62.55 ms | 500.40 ms | 37% |
| 16 | 18.75 | 32.68 ms | 522.90 ms | 35% |
| 32 | 9.375 | 16.69 ms | 534.15 ms | 35% |

Check the second row by hand. Each server owns 150 players. Each owned player costs `20 + 2 × 299 + 4 × 150 = 20 + 598 + 600 = 1,218 µs`. Times 150 players is 182,700 µs, or 182.7 ms.

Three things stand out.

- **Splitting a crowd in two does almost nothing for the busiest server.** It drops from 185.4 to 182.7 ms. Each server now owns half the players, but every one of those players now has 150 foreign neighbours, and each foreign neighbour costs three times a local one. The saving and the new cost almost cancel.
- **The total work nearly triples and never comes back.** As `s` grows, almost every neighbour becomes foreign, so each pair costs `2 × (c_i + c_x) = 12 µs` instead of 4. The useful share falls toward `c_i / (c_i + c_x)`, one third.
- **You can still fit the crowd, at a price.** Eleven servers bring the per-server load to 46.6 ms, under budget. Without the cross-server cost, four servers would have been enough (185.4 / 4 = 46.4 ms).

Now vary the crowd. Here is the smallest number of servers that fits each crowd in the 50 ms budget:

| Crowd size `m` | One server | Servers needed | Load per server at that count |
|---|---|---|---|
| 150 | 47.7 ms | 1 | 47.7 ms |
| 200 | 83.6 ms | 5 | 42.3 ms |
| 300 | 185.4 ms | 11 | 46.6 ms |
| 600 | 730.8 ms | 43 | 49.7 ms |
| 1,000 | 2,018.0 ms | 120 | 49.9 ms |

Servers needed grow roughly as `m²`. Going from 150 to 200 players, a third more, takes you from one server to five. A 1,000-player crowd needs 120 servers, each receiving updates about all 1,000 players every tick. This is the answer to the hook. A dynamic mesh can subdivide a crowd, but the hardware it needs grows with the square of the crowd, and every one of those servers must hear about everyone.

Here is the model as code. Lab 03 builds on it.

```python
C_P, C_I, C_X = 20, 2, 4     # microseconds per tick: per player, per neighbour, extra per foreign neighbour

def crowd_split_ms(m, s):
    """Per-server tick load when m players who all see each other are split over s servers."""
    k = m / s
    return k * (C_P + C_I * (m - 1) + C_X * (m - k)) / 1000

one = crowd_split_ms(300, 1)
for s in (1, 2, 4, 8, 16, 32):
    per = crowd_split_ms(300, s)
    print(f"s={s:>2}  per server {per:6.2f} ms  total {per * s:6.2f} ms  "
          f"useful share {one / (per * s):4.0%}")
```

It prints the six rows of the first table, from `s= 1  per server 185.40 ms  total 185.40 ms  useful share 100%` to `s=32  per server  16.69 ms  total 534.15 ms  useful share  35%`.

### Move it yourself

Open `examples/w03-crowd-split.html`, tab "Split a crowd". The left view shows the crowd as a disc of dots, coloured by owning server, cut into `s` wedges. A sample of cut pairs is drawn as faint lines crossing wedge borders. The right view shows one bar per server, stacked in three colours (players, local pairs, cross-server pairs), against the 50 ms budget line, with the total work and the useful share printed above. Start at `m = 300, s = 1`. Step `s` to 2. On the left, the crowd is now two colours and a mesh of lines appears. On the right, the bar splits into two bars that are almost as tall as the one before, because the cross-server part filled the space the local part gave up. Keep stepping `s` up and watch the cross-server colour take over every bar. Then drag `c_x` to 0 and watch the problem disappear. The cost of a cut pair is the whole story.

### Same idea elsewhere

**World of Warcraft layering (Classic, August to November 2019).** Week 1 showed layering dividing a crowd into copies. Rewrite it in this week's model. A copy is a split in which the players on different servers cannot see each other, so there are no foreign neighbours at all. Set `c_x = 0` and drop the cross-server neighbours from `m − 1`, and splitting 300 players into three layers of 100 costs three servers `100 × (20 + 2 × 99) = 21.8 ms` each. That is why layering works where spatial splitting fails. It is also why players hated it for some events, because the thing it removes is the ability to see each other.

**EVE Online (current mechanics).** The EVE University wiki describes Tranquility as nodes, each hosting part of New Eden, and time dilation acting per node. In the B-R5RB fight from week 1 (2,670 pilots, January 2014), the node answered by slowing time to 10% for most of the fight. In this week's terms, EVE stretched the budget, the lever from week 1, instead of cutting the crowd. For a crowd where everyone sees everyone, this model says that is a reasonable choice, because every split would multiply the work.

**Microcell assignment (De Vleeschauwer et al., 2005).** The Ghent group divides the world into many small cells and assigns cells to servers, rather than drawing a few large regions. Their greedy "balanced deployment" algorithm takes cells from heaviest to lightest and puts each on the server that keeps the maximum load lowest. They report that microcells raise the average load, because more cell borders mean more forwarding, while lowering the busiest server's load, which is what players feel. That is our trade-off between imbalance and cut, measured in their simulation.

**Star Citizen (Alpha 4.0 preview, December 2024, and the planned dynamic version).** The static mesh that shipped in 4.0 pre-assigns servers to areas such as a planet or a city, a partition drawn before the game runs, like week 1's zones. The dynamic version described on the wiki is a partition redrawn at run time. This lecture's model predicts where it will struggle. Cities with players spread across streets split well. The one hangar where everybody gathers does not.

Four systems, one load model. When you evaluate any scheme that promises to "just add servers", ask what a cut pair costs and whether the players in the hot spot can all see each other.

### Design judgment

- **Split sparse space, not dense crowds.** Moving borders is excellent at spreading many moderate hot spots across idle servers. It is poor at a single crowd where everyone sees everyone. Know which one your design creates.
- **Make cut pairs cheap before making partitions clever.** The whole problem in the table comes from `c_x`. Batching ghost updates, sending ghosts at a lower rate, and resolving interactions on one side (week 2) all shrink it. Halving `c_x` does more for a crowd than any partitioning algorithm.
- **For true crowds, change the rules, not the map.** Copies (layers), slower time (week 7), fewer and coarser interactions in a battle (week 6), or smaller interest radii reduce `m − 1`, the number each player must consider. Spatial partitioning cannot.
- **Price the servers.** A 1,000-player crowd fitting on 120 servers is not a success if those servers are idle 23 hours a day. Week 13 costs this out.

## 3. Partitioning a whole world

A real world has several hot spots of different sizes, plus players spread between them. Lab 03 uses a seeded 4 km × 4 km world with 3,000 players. About a third gather around five hot spots of different spreads, and the rest are spread evenly. The AOI radius is 50 m, which gives 33,056 interacting pairs. Sixteen servers, three partitions.

- **Static 4 × 4 grid.** The zone model. Sixteen equal squares of 1 km, drawn without looking at the players.
- **k-d tree by headcount.** Recursive bisection. Split the players at the median x coordinate into two halves, then split each half at its median y, and so on, until there are 16 regions with 187 or 188 players each. A **k-d tree** is a binary tree whose nodes alternate between splitting on x and on y (CS102 week 7 covers trees in general).
- **k-d tree by load.** The same recursion, but each player is weighted by its actual cost, `c_p + 2 × c_i × (neighbours)`. At each split, among the cut positions within 15% of the target load share, it takes the one that separates the fewest interacting pairs.

| Partition | Busiest server | Mean load | Imbalance | Cut pairs |
|---|---|---|---|---|
| Static 4 × 4 grid | 68.0 ms | 12.7 ms | 5.34 | 1,448 (4.4%) |
| k-d by headcount | 64.7 ms | 16.8 ms | 3.86 | 9,502 (28.7%) |
| k-d by load | 42.1 ms | 18.3 ms | 2.30 | 12,654 (38.3%) |

Read the table as a story.

The static grid cuts almost nothing, because its borders rarely pass through a crowd. But its busiest server is at 68 ms, over budget, while the mean is 12.7 ms. Five times the mean is week 1's idle-hardware problem.

Balancing by headcount barely helps the busiest server. It gives every server the same number of players, but players in a crowd cost far more than players alone, because each has many neighbours. A server that owns 188 players of one crowd is much busier than one that owns 188 wanderers. Worse, the median lines cut straight through the crowds, so the cut jumps from 4% to 29% and the mean load rises by a third.

Balancing by load is the only partition that fits every server under the 50 ms budget. It does this by giving crowded servers small regions. The price is that the mean load rises 44% above the static grid, from 12.7 to 18.3 ms, because 38% of pairs are now cut. In total the cluster works harder, and the busiest server works less. That is the trade that De Vleeschauwer and colleagues report for microcells, and it is the right trade, because the busiest server is the one players feel.

### Other shapes of partition

- A **quadtree** splits any region that holds too much load into four equal squares, recursively. It is simple and its borders line up with a grid, which makes neighbour lookups cheap. It cannot put a border where a gap between two crowds happens to be. It can only halve.
- **Microcells with assignment** (the 2005 paper) fix a fine grid of small cells and move cells between servers. Borders can take any shape made of cells, and rebalancing moves whole cells, which is simple to implement. Without a locality rule, a greedy assignment can give one server cells scattered across the map, which raises the cut sharply.
- **k-d trees** give contiguous rectangular regions and put borders anywhere along an axis, which lets a load-aware version look for gaps. Their weakness is that they only cut along x or y.

None of these can split a single crowd well, for the reason in section 2. They differ in how well they handle many crowds.

## 4. Moving borders over time

A dynamic partition must be redrawn as players move. Every redraw moves some players to new owners, and each move is a handoff.

Suppose a border 1 km long moves 50 m to shift load off a busy server, through an area at `ρ = 0.002` players per m². The strip it sweeps holds `0.002 × 1,000 × 50 = 100` players, and each needs a handoff. At week 2's 1 ms of CPU per handoff, that is 100 ms of handoff work, twice a tick's budget, if done in one tick. Spread over 20 ticks, it is 5 ms per tick. Borders must move gradually, a few players per tick, never all at once.

The second risk is oscillation. If the rule is "rebalance whenever imbalance exceeds 1.5", load that hovers around that threshold makes borders jump back and forth, and every jump costs handoffs. This is week 2's dithering problem again, one level up, and the fix is the same. Use hysteresis in time and in load.

- Rebalance only when imbalance has stayed above a high threshold (say 2.0) for several seconds.
- Stop rebalancing when it falls below a lower threshold (say 1.4).
- Move a border by a bounded amount per second, and prefer moves that sweep through sparse areas.

A partition that is 10% less balanced but moves once a minute is usually better than one that is perfect and moves every second.

## In-class activity (25 minutes)

In groups of three, take your seam layout from the week 2 activity (four 1 km areas, a market town and a world-boss arena).

1. The arena event draws 250 players into one crowd where everyone sees everyone. Using the model in section 2 and the lecture's constants, find how many servers the crowd needs under the 50 ms budget. (10 min)
2. Your cluster has 6 servers in total for the whole map. Propose what happens during the event. Use at least one lever from section 2's design judgment and state its price to players in one sentence. (10 min)
3. Write a rebalancing rule for the hour before the event, when players stream toward the arena. Give the two thresholds and the maximum border speed in metres per second. (5 min)

Expected output: the server count from step 1 (7, at 49.1 ms each), a two-sentence event plan, and a rule with three numbers.

## Common misconceptions

- **"More servers always means more capacity."** For spread-out players, roughly yes. For a crowd where everyone sees everyone, each extra server adds cut pairs, and the total work approaches three times the single-server cost in this lecture's model.
- **"Balance the players and you balance the load."** Players in crowds cost more than players alone, because load follows pairs. Balancing by headcount left the busiest server at 64.7 ms in the lab world.
- **"The best partition has the lowest total load."** The static grid has the lowest total and the worst busiest server. Players feel the busiest server.
- **"A dynamic partition should rebalance as soon as it detects imbalance."** Without hysteresis, borders oscillate, and each move is a batch of handoffs.

## Check yourself

1. A crowd of 120 players, everyone in everyone's AOI, uses the lecture's constants. What is its load on one server? Split across 2 servers, what is each server's load? Is splitting worth it?
2. With `c_x` halved to 2 µs, recompute the per-server load for `m = 300` and `s = 4`. How many servers does the crowd now need to fit 50 ms?
3. A border 600 m long moves 30 m through an area at `ρ = 0.003` players per m². How many handoffs does that cause, and how many ticks must the move be spread over to keep handoff CPU under 5 ms per tick at 1 ms per handoff?
4. In the section 3 table, the k-d by load partition cuts more pairs than the k-d by headcount partition, yet its busiest server is lighter. Explain why in two sentences.

<details>
<summary>Answers</summary>

1. `L(120, 1) = 120 × (20 + 2 × 119) = 30,960 µs = 30.96 ms`. With 2 servers, `k = 60`, `L = 60 × (20 + 238 + 4 × 60) = 60 × 498 = 29,880 µs = 29.88 ms`. Splitting saves about 1 ms per server while doubling the hardware. It fits on one server already, so do not split.
2. `k = 75`, `L = 75 × (20 + 598 + 2 × 225) = 75 × 1,068 = 80,100 µs = 80.1 ms`. Search upward: `s = 6` gives `k = 50`, `50 × (618 + 2 × 250) = 55.9 ms`; `s = 7` gives `k ≈ 42.9`, `42.9 × (618 + 2 × 257.1) ≈ 48.5 ms`. Seven servers, instead of eleven.
3. `0.003 × 600 × 30 = 54` handoffs, 54 ms of CPU. At most 5 per tick, so spread over at least 11 ticks (1.1 s at 10 Hz).
4. The headcount partition gives every server the same number of players, so the server that owns part of a big crowd gets many expensive players. The load partition gives that server fewer players and a smaller region, which cuts more pairs but moves work from the busiest server to idle ones.

</details>

## Lab / assignment hook

[Lab 03, partitioning a crowded world](../labs/lab03.md). You implement `crowd_split_us`, recursive bisection by headcount and by load, reproduce the tables in sections 2 and 3, and then design and test a rebalancing rule with hysteresis.

## Sources

- Star Citizen Wiki, "Server meshing" (Alpha 4.0 preview, December 2024; dynamic version planned). Static versus dynamic server meshing, subdividing a crowded area across as many servers as needed, criticism that the dynamic version is impossible.
- De Vleeschauwer, B., Van Den Bossche, B., Verdickt, T., De Turck, F., Dhoedt, B. & Demeester, P. (2005). Dynamic microcell assignment for massively multiplayer online gaming. *NetGames '05*, ACM. doi:10.1145/1103599.1103611. Microcells, server load as a weighted sum including forwarding and migration between cells, higher weight across servers, the greedy balanced deployment algorithm, lower peak load at the price of higher average load.
- Wowpedia, "Layering" (World of Warcraft Classic, patch 1.13.2, August to November 2019). Copies of the world per realm, players only see others on the same layer.
- EVE University Wiki, "Tranquility" and "Time dilation" (current mechanics). Nodes hosting parts of New Eden, time dilation per node, 10% floor.
- Wikipedia, "Battle of B-R5RB" (formerly "Bloodbath of B-R5RB") (27 to 28 January 2014). 2,670 players in one system with time dilation at 10%.

## Interactive spec: examples/w03-crowd-split.html

**The one insight:** splitting spread-out players across servers removes work, but splitting a crowd where everyone sees everyone mostly converts local pairs into more expensive cross-server pairs. Balancing by load beats balancing by headcount.

**Two tabs.** Tab 1 "Split a crowd" (default, the insight on first screen). Tab 2 "Partition a world".

**Tab 1 layout.** Two linked views, side by side on desktop, stacked on mobile.
- **Left, the crowd.** A disc containing `m` dots (seeded uniform in the disc, mulberry32 seed 3). The disc is cut into `s` equal wedges from the centre; each dot is coloured by its wedge (server). Draw up to 400 randomly sampled pairs as faint lines: pairs within one wedge in a neutral colour, cut pairs in an accent colour. Print "cut pairs: X of Y" with the exact numbers `m × (m − k)` ordered foreign neighbour relations summed, or equivalently `m (m − k) / 2` unordered cut pairs, and `m (m − 1) / 2` total unordered pairs.
- **Right, the servers.** One vertical stacked bar per server (all equal here): players `k × c_p`, local neighbours `k × c_i × (m − 1)`, cross-server extra `k × c_x × (m − k)`, in three palette colours, in ms. A horizontal line at the budget (50 ms). Above the bars: per-server load, total load `s × L`, useful share `L(m, 1) / (s × L(m, s))` as a percent, and "servers needed" (smallest `s` with `L ≤ budget`, searched from 1 to 200).
- **Below, a small line chart** of per-server load against `s` from 1 to 32 for the current `m`, with the budget line and a second dashed line for the same crowd with `c_x = 0`.

**Tab 1 controls.** Crowd `m`: slider 20 to 1,000, step 10, default 300. Servers `s`: stepper 1 to 32, default 1. `c_x`: slider 0 to 8 µs, step 0.5, default 4. Budget: slider 20 to 100 ms, default 50. Toggle "layers instead of space" (sets foreign neighbours to 0 and neighbours to `k − 1`, and relabels the wedges as copies).

**Tab 1 formulas.** `k = m / s`. `L(m, s) = k × (c_p + c_i (m − 1) + c_x (m − k))` in µs, shown in ms, with `c_p = 20`, `c_i = 2`. Layers mode: `L = k × (c_p + c_i (k − 1))`.

**Tab 1 test values.** `m = 300`: `s = 1` 185.40 ms; `s = 2` 182.70 ms, total 365.40, useful 51%; `s = 4` 113.85 ms, total 455.40, 41%; `s = 8` 62.55 ms; `s = 16` 32.68 ms, total 522.90, 35%; servers needed 11 (46.61 ms). Servers needed: `m = 150` → 1 (47.70 ms), `m = 200` → 5 (42.32 ms), `m = 600` → 43, `m = 1000` → 120. Layers mode, `m = 300`, `s = 3`: 21.80 ms each.

**Tab 2 layout.** Left: a square 4 km map with 3,000 dots generated in JS like Lab 03's `make_world` (35% of players in five Gaussian hot spots with standard deviations 80, 60, 50, 40 and 30 m, the rest uniform; seeded, so it is stable), with region borders drawn for the selected partition and regions tinted by load relative to budget (sequential palette, red outline above budget). Right: a bar per server (16 bars) with the budget line, sorted by load, plus a numbers row: busiest, mean, imbalance, cut pairs and percent. Controls: partition selector (static 4 × 4 grid, k-d by headcount, k-d by load with 15% slack), AOI radius (30 to 80 m, default 50), a "regenerate world" button with a seed field. Implement pairs with a uniform grid of cell side `R`, the load function exactly as in Lab 03's `loads` (`C_P = 20`, `C_I = 2`, `C_X = 4` µs), and the two k-d algorithms exactly as the Lab 03 docstrings describe. Because the JS generator differs from Python's, numbers will not match the lecture table exactly; the qualitative result must hold for the default seed: grid busiest above budget with imbalance above 4, headcount k-d busiest above budget with cut above 15%, load k-d busiest under budget with the highest mean. Lab 03's Python world uses seed 7, but the JS world with seed 7 does not meet these conditions, so the example's default world seed is 18 (the seed field lets students try others).

**Accessibility.** Tabs are real buttons with `aria-selected`; controls keyboard operable with visible focus. `aria-live="polite"` summary of per-server load, servers needed and useful share. No animation needed; under `prefers-reduced-motion` skip transitions. Palette from `templates/interactive-tokens.css`, light and dark.
