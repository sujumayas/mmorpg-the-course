# MMO404 · Week 09 — Server meshing concepts

**Why this matters:** Server meshing promises that a world will never be full, because any crowd can be spread across as many servers as it needs. For spread-out players that is close to true. For a crowd in which everyone can see and hit everyone, the arithmetic is much less generous, and you should be able to say exactly how much less before you promise players a 5,000-person battle.

**You will be able to:**
- Compute the tick time of each server when a dense crowd is split across `k` servers, and the largest crowd `k` servers can hold.
- Derive why, for a crowd where everyone interacts with everyone, four times the servers buys only twice the players, and find where ghost cost sets a hard ceiling.
- Design an authority transfer that stays correct when the old owner is slow or paused, using epochs as fencing tokens.
- Compare static and dynamic meshing for a given world and event plan, including the load on the replication layer.

**Before class:** Martin Kleppmann, "How to do distributed locking" (8 February 2016), the sections on fencing tokens. Star Citizen Wiki, "Server meshing" and "Replication layer" (maintained wiki pages). Reread your MMO404 lab 01 notes on crowd capacity.

**Prerequisites from earlier courses:** [MMO302 week 1, scale targets and the n-squared problem](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md). [MMO302 week 4, zone servers and handoff](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md). [MMO302 week 8, item ownership and transactional integrity](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (one owner at a time). This course's [week 1 capacity model](w01-limits-of-the-zone-model.md), [week 2 boundary handoff](w02-seamless-worlds-and-boundary-handoff.md) and [week 4, replication prioritization](w04-replication-prioritization-and-relevancy.md). [Week 7, clock domains](w07-time-dilation-revisited.md) and [week 8, lookahead](w08-distributed-simulation-research.md).

**Interactive:** [w09-mesh-crowd.html](../examples/w09-mesh-crowd.html). Keep it open during section 2.

---

## 1. What server meshing changes

Every architecture you have studied so far ties authority to space. A zone server (MMO302 week 4) owns everything inside its zone. A seamless world (week 2) moves the lines closer together and hands entities across them, but a line still decides who owns what. **Server meshing** is the family of designs that loosens that tie. Four ideas define it.

- **Authority.** Every entity has exactly one server allowed to change its state. That server is its **authority**. Every other server that needs the entity holds a read-only copy, a **ghost** in this course's words, a replica in Colyseus's (week 8).
- **Replication layer.** Entity state lives in a shared service between the servers and the clients. The authority writes to it. Everyone else, servers and clients alike, subscribes to what they need from it. Servers no longer talk to each other directly.
- **Interest.** Each server subscribes to the entities its owned entities can interact with. This is the relevancy of week 4 applied to servers instead of clients.
- **Authority transfer.** Authority moves between servers at run time, for load or because an entity moved. The rules for moving it safely are the subject of section 3.

Two variants matter. In **static meshing**, the assignment of territory to servers is fixed ahead of time, for example one server per planet or per region of a star system. In **dynamic meshing**, a coordinator changes the assignment while the game runs, splitting a busy region across more servers and merging quiet ones.

The shipped example today is Star Citizen (Cloud Imperium Games). Its replication layer arrived in Alpha 3.18. It moved the state of the universe, characters, ships and items, out of the dedicated game servers, so that clients and servers both connect to the layer, and a crashed server can be replaced without resetting the world around its players. Alpha 4.0, released on 19 December 2024 as the "4.0 Preview", turned on static server meshing across the Stanton and Pyro systems, with shards of 500 players. The Star Citizen Wiki describes dynamic meshing as the goal. This lecture found no record of it shipping as of September 2026.

Meshing solves the problem of week 1 for spread-out players. It is much weaker against the problem of week 6, a crowd in one place. The next section shows why with numbers.

## 2. Worked example: four times the servers, twice the crowd

### The hook

Star Citizen's Alpha 4.0 put 500 players in one shard and spread them across several servers, each responsible for its own locations in two star systems. A natural reading is "more servers, more players, in proportion," and it holds as long as the players spread out over planets and stations. Now ask what happens if all 500 fly to one space station and start shooting. Every server that owns some of them must know about all of them. Where did the gain go?

### The model

Take week 1's cost model. A server that owns `n` players, all within interaction range of each other, spends per tick

```
c_p × n            simulating each owned player
c_i × n × n        handling every ordered pair that interacts
```

with `c_p = 20 µs`, `c_i = 2 µs` and a budget of 50 ms per tick. MMO404 lab 01 found that one server holds 153 such players.

Now split the crowd of `N` across `k` servers, `N / k` owned by each. Everyone still sees everyone. So each server

- simulates its `N / k` owned players,
- handles the interactions of each owned player with all `N` players, which is `(N / k) × N` pairs,
- and keeps a ghost of every player it does not own, `N × (1 − 1/k)` of them, paying `c_g` per ghost per tick to receive and apply its update. Take `c_g = 4 µs`, a fifth of an owned player.

```
T_k(N) = c_p × N/k  +  c_i × N²/k  +  c_g × N × (1 − 1/k)
```

The first two terms fall as `1/k`. That is the meshing gain. The last term grows toward `c_g × N`, which no number of servers can reduce, because every server must know about every player it might hit.

The largest crowd `k` servers can hold solves `T_k(N) = 50 ms`, a quadratic in `N`. The model has one more output, the load on the replication layer. Each tick, every player's update goes to the `k − 1` servers that hold its ghost, so the layer delivers `N × (k − 1)` ghost updates per tick.

### Numbers you can check

Check the first row by hand. With `k = 1`, there are no ghosts, and `20 µs × N + 2 µs × N² = 50 ms` gives `N² + 10 N − 25,000 = 0`, so `N = 153`, week 1's number. Check the tick column at `k = 4` and `N = 1,000`. Owned work is `(20 µs × 1,000 + 2 µs × 1,000,000) / 4 = 505` ms, and ghosts add `4 µs × 750 = 3` ms, for 508 ms.

```python
import math

C_P = 20e-6      # CPU s per owned player per tick (week 1)
C_I = 2e-6       # CPU s per interacting ordered pair per tick (week 1)
C_G = 4e-6       # CPU s per ghost per tick: receive and apply one update
BUDGET = 0.050   # usable CPU s per tick (week 1)

def tick_ms(n, k):
    """Tick time of each of k servers sharing a crowd of n in which everyone sees everyone."""
    own = C_P * n / k + C_I * n * n / k
    ghosts = C_G * n * (1 - 1 / k)
    return 1000 * (own + ghosts)

def capacity(k):
    """Largest crowd (float) whose tick fits the budget on k servers."""
    a = C_I / k
    b = C_P / k + C_G * (1 - 1 / k)
    return (-b + math.sqrt(b * b + 4 * a * BUDGET)) / (2 * a)

print(" k   crowd   vs k=1   tick at 1,000   ghost share   ghost updates per tick")
for k in (1, 2, 4, 16, 64, 256):
    n = capacity(k)
    ghost_ms = 1000 * C_G * n * (1 - 1 / k)
    print(f"{k:3d}  {n:6.0f}   {n / capacity(1):5.2f}x   {tick_ms(1000, k):9.1f} ms"
          f"   {ghost_ms / 50:9.0%}   {n * (k - 1):12,.0f}")
```

```
 k   crowd   vs k=1   tick at 1,000   ghost share   ghost updates per tick
  1     153    1.00x      2020.0 ms          0%              0
  2     218    1.42x      1012.0 ms          1%            218
  4     308    2.01x       508.0 ms          2%            925
 16     613    4.00x       130.0 ms          5%          9,192
 64    1199    7.83x        35.5 ms          9%         75,520
256    2283   14.90x        11.9 ms         18%        582,203
```

Read the "vs k=1" column. 4 servers hold 2× the crowd, 16 hold 4×, 64 hold about 8×. **For a crowd where everyone interacts with everyone, capacity grows as the square root of the number of servers.** The reason is in the model. The pair term `c_i × N² / k` dominates, and keeping it inside the budget as `N` doubles needs `k` to quadruple. Meshing divides the work of the crowd, but the work of a crowd grows with the square of its size.

Then read the "ghost share" column. At 256 servers, 18% of every server's tick goes to receiving other servers' players. As `k` grows without limit, the ghost term approaches `c_g × N`, and it alone fills the budget at `N = 50 ms / 4 µs = 12,500`. No mesh of any size holds a crowd larger than that. Long before that point the fleet is absurd. A crowd of 1,000 needs 44 servers, and one of 2,000 needs 192.

The last column is the bill someone else pays. At 64 servers and a crowd of 1,199, the replication layer delivers 75,520 ghost updates per tick, 1.5 million per second at 20 Hz, all for one fight. That traffic is on top of what the clients receive.

### What the square root means in practice

The same model with spread-out players gives a very different answer. If the players are spread over planets and stations so that each one interacts with only a few dozen others, the pair term is small, ghosts are few, and `k` servers hold close to `k` times the players. That is the case static meshing was built for, and the 500-player shards of Star Citizen's 4.0 Preview, spread over two star systems, are of that kind.

So a mesh has two capacities, and you must quote both. The **spread capacity** is roughly linear in servers. The **crowd capacity** is roughly the square root, with a ceiling. Every event you design, a world boss, a siege, a festival, has to be checked against the second.

### Move it yourself

Open `examples/w09-mesh-crowd.html`. The left view is a top-down picture of a crowd split into `k` vertical strips, one colour per server, with one server's ghosts drawn as outlines. The right view plots crowd capacity against `k` on log-log axes, with a dashed line of slope 1 ("linear") and the model's curve, plus a horizontal line at the ghost ceiling. Start at `k = 1`. Drag `k` up and watch the owned strip shrink while the outlined ghosts cover the whole crowd. The curve on the right runs parallel to a slope of one half, not one. Then switch the crowd to "spread," which limits each player's interactions to the nearest 30, and watch the curve bend up to the linear line.

### Same idea elsewhere

**Star Citizen (Cloud Imperium, Alpha 3.18 replication layer; Alpha 4.0 static meshing, December 2024).** In our form, each dedicated game server is one of the `k`. The replication layer is where the `N × (k − 1)` ghost updates flow. Static meshing assigns territory per location, so `k` servers hold close to `k` times the players while they stay spread. Dynamic meshing, still planned, would let the mesh put more servers on a busy station. This model says what it could expect for a dense firefight, the square root.

**SpatialOS (Improbable, open beta February 2017).** SpatialOS split a world among many **workers**, each with authority over part of the entities and read access to the rest within its interest. Bossa Studios' Worlds Adrift, a physics-heavy sandbox of floating islands, ran on it from its July 2017 early access until development ceased on 26 July 2019. In our form, workers are the `k`, authority and interest are exactly the model's owned players and ghosts, and a physics-rich world raises `c_i`, the pair term that sets the square root.

**EVE Online (CCP, current).** EVE does not mesh inside a solar system. The EVE University wiki describes time dilation as acting on a node, the hardware that hosts a region of space. In our form, EVE chose `k = 1` per system and pays for crowds with dilation, week 7's answer, rather than with ghosts. The model says why that is a defensible choice. For a crowd of 2,000 in one system, a mesh would need 192 servers of week 1's size, with 16% of each one's tick spent on ghosts, and every one of them in one clock domain.

Three platforms, one equation. Split authority across `k` servers and the owned work falls by `k`. The interaction work falls by `k` only if interactions are local, and the ghost work never falls.

### Design judgment

- **Quote the crowd capacity, not the shard size.** "500 players per shard" and "500 players in one fight" are different promises. Put both numbers in your design document.
- **Cut `c_i` before adding servers.** Everything that reduces pairwise work, such as target caps on area attacks, aggregate updates for distant players (week 5) and relevancy limits inside the crowd, moves the square root curve up. Adding servers moves along it.
- **Watch the ghost share.** Past about 10% of each tick spent on ghosts, adding servers mostly adds replication layer traffic. That is the point where time dilation (week 7) or a design change is cheaper than more hardware.
- **Remember the clock.** All `k` servers of one crowd share one clock domain (week 7). If one of them runs slow, all of them do, and the lookahead of week 8 decides how much they wait for each other.

### Check this example

1. Compute each server's tick time for a crowd of 600 on 16 servers. Does it fit the 50 ms budget?
2. Using the square-root rule, roughly how many servers does a crowd of 1,200 need if 16 servers hold about 600? Compare with the table.
3. A designer halves `c_i` by capping area attacks at 20 targets. Without running the code, estimate how the crowd capacity at `k = 16` changes, and explain why it is not doubled.

<details>
<summary>Answers</summary>

1. Owned work `(20 µs × 600 + 2 µs × 360,000) / 16 = (12 + 720) / 16 = 45.75` ms. Ghosts `4 µs × 600 × 15/16 = 2.25` ms. Total 48.0 ms, which fits.
2. Doubling the crowd needs four times the servers, so about 64. The table gives 1,199 at 64 servers, which matches.
3. When the pair term dominates, `N ≈ sqrt(budget × k / c_i)`, so halving `c_i` multiplies `N` by `√2 ≈ 1.41`, from about 613 to about 867. The exact solution is 855, a little lower because the ghost and per-player terms take a larger share of the tick. It is not doubled because the pair work grows with `N²`, so halving its cost lets the crowd grow by only `√2`.

</details>

## 3. Authority transfer and fencing

Meshing moves authority far more often than zone handoff did. A dynamic mesh reassigns entities when it splits or merges regions, and even a static mesh transfers every entity that crosses a boundary. The rule from MMO302 week 8 still holds, one owner at a time. It is harder to keep when the owners are servers that can pause.

### How often

Estimate the transfer rate at one boundary. Players at density `ρ` (players per m²) milling across a boundary of length `ℓ`, with an average speed `v⊥` across the line in each direction, cross it about `2 × ρ × v⊥ × ℓ` times per second. Take the crowd that 16 servers hold in section 2's table, 613 players in a disc of 50 m radius has `ρ = 613 / 7,854 = 0.078` per m². One straight cut through the middle has `ℓ = 100` m. With `v⊥ = 1` m/s, that is about 16 transfers per second at one cut, and a 16-server split has 15 such cuts. A handoff band (week 2) reduces this, since a player must move a band's width past the line before the transfer starts, and pacing back and forth inside the band costs nothing.

### Why transfers go wrong

A transfer has three steps. The old authority A stops writing. The replication layer records B as the new authority. B loads the latest state and starts simulating. The danger is A not knowing it has stopped. A garbage collection pause, a slow tick or a network stall can hold A for 200 ms. The layer decides A is gone and gives authority to B. Then A wakes up and writes the state it computed before the pause, a position, a health value, an item it thinks the player still holds. Two authorities have written one entity, and one of them is stale.

Kleppmann's 2016 article on distributed locking gives the standard fix, the **fencing token**. Every time authority is granted, the granting service hands out a number that only ever increases. Every write carries the number it was granted with. The storage refuses any write whose number is lower than one it has already accepted. In Kleppmann's example, a client holding token 33 pauses, its lease expires, a second client gets token 34 and writes, and the storage then rejects the first client's late write with 33.

Applied to meshing, the token is an **authority epoch** stored per entity in the replication layer.

| Step | Replication layer record for entity 12 | Event |
|---|---|---|
| 1 | owner A, epoch 7 | A simulates and writes with epoch 7 |
| 2 | owner A, epoch 7 | A pauses for 200 ms |
| 3 | owner B, epoch 8 | Coordinator transfers entity 12 to B |
| 4 | owner B, epoch 8 | B loads state and writes with epoch 8 |
| 5 | owner B, epoch 8 | A wakes, writes with epoch 7, rejected |
| 6 | owner B, epoch 8 | A reads the rejection and drops entity 12 to a ghost |

The rule is on the layer, not on the servers. A server cannot know it has been paused, so it cannot be trusted to step aside. The layer can always compare two numbers.

### What the player sees

During a transfer the entity is not simulated. The gap is the time from A's last accepted write to B's first, at least one tick plus one round trip to the layer. At 20 Hz with 2 ms round trips, that is about 55 ms, one missed update. Clients interpolating 100 ms behind (CS202 week 10) do not see it. What they do see is a transfer during an action, a spell half cast when the caster moves to B. The ability's state must travel with the entity, and the cast timer must resume on B's clock, which is the same clock if both are in one domain (week 7). Designs that keep in-flight effects on the server that started them, and transfer only when the entity is idle, avoid most of these bugs at the cost of a slightly later transfer.

## 4. Static or dynamic, and the replication layer's bill

The choice between static and dynamic meshing is a choice about what you know in advance.

| | Static meshing | Dynamic meshing |
|---|---|---|
| Territory assignment | Fixed per location, planned before launch | Changed at run time from measured load |
| Handles | Players spread by content (planets, towns, zones) | Crowds that form where you did not plan them |
| Transfers | Only when entities cross fixed lines | Also when lines move, which can move hundreds of entities at once |
| Fails when | A crowd forms inside one location | Crowds grow faster than the mesh can split, or splits cost more than they save |
| Cost to build | Moderate, much like seamless zones | High: a coordinator, load prediction, bulk transfers |
| Shipped examples | Star Citizen Alpha 4.0 | None at MMO scale as of 2026 |

A dynamic split is itself a bulk transfer. Cutting a 613-player region in two moves about 300 entities at once, each with its epoch bump and state load. Done in one tick, that is a 300-entity spike in the replication layer and a noticeable hitch on the receiving server. Done gradually, over a few seconds, the old server stays overloaded while the split is in progress. Either way, a mesh that splits only after it is overloaded is too late. This is the same lesson as MMO302 week 13's autoscaling. Capacity must be added before the load, from a forecast or a schedule, which is why event calendars matter as much as algorithms.

Finally, the replication layer has to scale too. Section 2's table shows it delivering 75,520 ghost updates per tick for one fight on 64 servers. It must also stream state to every client, persist entity state, and apply every epoch check. It is sharded by entity like any database (MMO302 week 7), and its shards have hot spots in exactly the places the game has crowds. A mesh moves the crowd problem out of the game servers and into the layer. It does not make it disappear.

## In-class activity (25 minutes)

Groups of three. Each group gets an event card for a meshed world with week 1's server size: a 400-player world boss in a 60 m arena, a 1,500-player city festival where players spread over a 600 m square and each sees about 40 others, or a 2,500-player planetary invasion where fights happen in clusters of about 150.

1. Decide whether your event is a crowd (everyone sees everyone) or spread. Use the model to find the number of servers it needs. For clusters, apply the model per cluster.
2. Compute the ghost share per server and the ghost updates per tick through the replication layer.
3. Choose static or dynamic meshing for the event. If dynamic, say when the split must happen and how many entities it moves.
4. Name one design change that cuts `c_i` or the crowd size, and recompute the servers needed.

Expected output: a half-page table (servers, ghost share, layer load) before and after your change, and a one-sentence meshing choice. Groups present the event that needs the most servers and the change that cut it most.

## Common misconceptions

- **"Meshing makes capacity unlimited."** For spread players capacity grows about linearly with servers. For a crowd that interacts all-to-all it grows as the square root, and ghost cost caps it at `budget / c_g`, 12,500 in this model, whatever the number of servers.
- **"A crashed or paused server simply loses authority."** Only if the replication layer rejects its late writes. Without epochs, a server waking from a pause can overwrite the new authority's state.
- **"Dynamic meshing reacts to crowds, so no planning is needed."** Splits are bulk transfers and must happen before overload. Scheduled events should be meshed ahead of time.
- **"Moving state into a replication layer removes the bottleneck."** It moves it. The layer carries `N × (k − 1)` ghost updates per tick and must be sharded itself.

## Check yourself

1. Each server has a 100 ms budget instead of 50 ms, with the same costs. What crowd does one server hold? About what crowd do 16 servers hold, using the square-root rule, and what is the new ghost ceiling?
2. A crowd of 800 is split across 32 servers. Compute the tick time and the replication layer's ghost updates per second at 20 Hz.
3. Entity 40's record is "owner B, epoch 12." Server A sends a write with epoch 11, then server C sends one with epoch 13. What does the layer do with each, and what must have happened for C to hold epoch 13?
4. A static mesh assigns one server per space station. A new event sends 900 players to one station. Using the table in section 2, what happens on that station's server, and what are your two cheapest options?

<details>
<summary>Answers</summary>

1. `2 µs × N² + 20 µs × N = 100 ms` gives `N² + 10 N − 50,000 = 0`, so `N ≈ 219`. With the square root, 16 servers hold about 4 times that, about 875. The ghost ceiling is `100 ms / 4 µs = 25,000`.
2. Owned `(20 µs × 800 + 2 µs × 640,000) / 32 = (16 + 1,280) / 32 = 40.5` ms. Ghosts `4 µs × 800 × 31/32 = 3.1` ms. Tick 43.6 ms, which fits. Layer: `800 × 31 = 24,800` ghost updates per tick, 496,000 per second.
3. The epoch 11 write is rejected, since 11 is below the recorded 12. The epoch 13 write is accepted only if the layer has granted epoch 13 to C, which means authority moved from B to C after B's grant. If the layer has not granted 13, the write is invalid and rejected too. Epochs are issued by the layer, never chosen by servers.
4. One server holds 153 in a crowd. 900 players on one server is far over budget, so the station server lags or, with week 7's controller, dilates. From the table, 900 needs roughly 36 servers as a crowd. The cheapest options are to cut the crowd (instance or layer the event, spread it across the station's decks so it is not all-to-all) and to lower `c_i` (target caps, aggregate updates), then accept time dilation for the rest.

</details>

## Lab / assignment hook

[Lab 09, a mesh for a crowd](../labs/lab09.md). You implement the meshing cost model and its capacity solver, reproduce the table in section 2, add a spread-crowd variant and compare the two capacity curves, then build an authority table with epoch fencing and test it against a paused server. Deliverable: your `mesh.py`, the two capacity curves on one log-log plot, the fencing test log, and a one-page meshing plan for an event card from the in-class activity.

## Sources

- Star Citizen Wiki, "Server meshing" (maintained wiki, accessed September 2026). Static and dynamic meshing defined; server meshing live with Alpha 4.0 in December 2024 at 500 players per shard; dynamic meshing still planned.
- Star Citizen Wiki, "Update:Star Citizen Alpha 4.0.0" (maintained wiki, citing RSI patch notes "Star Citizen Alpha 4.0 Preview"). Release date 19 December 2024; first release of static server meshing; Pyro added beside Stanton; build information lists 500-player shards.
- Star Citizen Wiki, "Replication layer" (maintained wiki, citing "Inside Star Citizen: Dev Diary - Server Meshing", 4 July 2024). Introduced in Alpha 3.18; moved the state of the universe out of the dedicated game servers; clients and servers connect to it; crash recovery without resetting state.
- Wikipedia, "Improbable (company)" (maintained article, accessed September 2026). SpatialOS open beta February 2017; Worlds Adrift among the first games built on it.
- Wikipedia, "Worlds Adrift" (maintained article, accessed September 2026). Early access July 2017 on SpatialOS; development ceased 26 July 2019.
- EVE University Wiki, "Time dilation" (maintained wiki, current mechanics). Time dilation acts on a node, the hardware hosting a region of space.
- Kleppmann, M. "How to do distributed locking" (martin.kleppmann.com, 8 February 2016). Fencing tokens that increase on every grant; the token 33 and 34 example of a paused client's rejected write.

## Interactive spec: examples/w09-mesh-crowd.html

**Insight the visual must make obvious:** for a crowd where everyone interacts with everyone, capacity grows with the square root of the server count, because the pair work grows with the square of the crowd, and ghosts cap it. For spread players the same mesh scales nearly linearly.

**Layout.** Left: crowd map. Right: log-log capacity chart. Below: controls and number panel. Under 700 px: map, chart, controls, numbers stacked.

**Model (must match section 2 code).**
- `c_p = 20 µs`, `c_i = 2 µs`, `c_g = 4 µs`, budget 50 ms (all editable in an "advanced" disclosure).
- Crowd mode: `T_k(N) = c_p N/k + c_i N²/k + c_g N (1 − 1/k)`. Capacity is the positive root of `(c_i/k) N² + (c_p/k + c_g (1 − 1/k)) N − budget = 0`.
- Spread mode: each player interacts with `m = min(N, 30)` others (slider 10 to 100), and each server ghosts only the players within reach of its own, taken as `min(N (1 − 1/k), 2 m)`. `T = c_p N/k + c_i (N/k) m + c_g × ghosts`. Capacity by bisection on `N` in `[1, 10^6]` to 0.01.
- Ghost updates per tick `N (k − 1)` in crowd mode and `k × ghosts` in spread mode.

**Crowd map.** A disc of 50 m radius with `N` dots (cap drawing at 2,000, sampled by `mulberry32(9)`, uniform in the disc). Split into `k` vertical strips of equal player count, each strip a series colour (cycle the palette when `k` is large). Highlight server 1's strip; draw every dot it ghosts as a hollow outline. In crowd mode that is every other dot.

**Capacity chart.** x axis `k` from 1 to 1,024, log scale. y axis crowd from 100 to 20,000, log scale. Lines: crowd-mode capacity, spread-mode capacity, a dashed reference of slope 1 through `(1, capacity(1))` labelled "linear", a dotted reference of slope 1/2 labelled "square root", and a horizontal line at `budget / c_g` labelled "ghost ceiling". Marker at the current `k` on the active mode's curve.

**Controls (keyboard accessible, live labels).** `k`: slider over 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1,024 (default 1). Mode: segmented control "Crowd" / "Spread" (default Crowd). Crowd size `N` for the tick readout: slider 100 to 3,000 (default 1,000). `m` for spread mode.

**Number panel.** Capacity at the current `k`, its ratio to `k = 1`, tick time at the chosen `N` (with a red "over budget" state above 50 ms), ghost share of the budget at capacity, ghost updates per tick and per second at 20 Hz, and the fewest servers that fit the chosen `N` (search `k` upward to 100,000; show "no mesh fits" above the ghost ceiling).

**Test values (crowd mode, default costs).** Capacity: `k = 1` 153.2, `k = 2` 217.7, `k = 4` 308.3, `k = 16` 612.8, `k = 64` 1,198.7, `k = 256` 2,283.1. Tick at `N = 1,000`: 2,020.0 ms (`k = 1`), 508.0 ms (`k = 4`), 130.0 ms (`k = 16`), 35.5 ms (`k = 64`). Ghost updates at capacity for `k = 64`: 75,520 per tick. Fewest servers for `N = 1,000`: 44; for `N = 2,000`: 192. Ghost ceiling 12,500.
- Spread mode, `m = 30`: capacity 625.0 at `k = 1`, 2,488.0 at `k = 4`, 9,952.0 at `k = 16`.

**First screen.** Crowd mode, `k = 16`, `N = 1,000`, with the map showing one strip filled and the rest of the crowd outlined, and the chart marker sitting on the square-root curve well below the linear line. Caption: "16 servers, 4 times the crowd." A button "Spread the players out" switches the mode.
