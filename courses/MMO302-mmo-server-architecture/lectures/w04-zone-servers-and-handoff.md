# MMO302 · Week 04 — Zone servers and handoff

**Why this matters:** One process cannot simulate a whole MMO world, so you cut the map into pieces and give each piece its own server. Every cut you draw becomes a line where players change owner, where AOI queries must look across a machine boundary, and where bugs duplicate or lose characters. This week you learn to price those lines before you draw them.

**You will be able to:**
- Compute the handoff rate and the ghost count of a zone layout from player count, speed, world size and AOI radius.
- Predict the most loaded zone server when players cluster, and explain why adding zone servers stops helping.
- Design a handoff protocol with a single owner at every instant, and a hysteresis band that stops ping-pong at borders.
- Critique a real game's partitioning (Second Life, EVE Online, Old School RuneScape) in terms of this model.

**Before class:** Alexander (ed.), *Massively Multiplayer Game Development* (Charles River Media, 2003), the chapters on server architecture assigned on the course page. Second Life Wiki, "Region crossing" (the whole page, it is short). Reread your notes on grid AOI from week 3.

**Prerequisites from earlier courses:** [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) (the dedicated server and its upload formula). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the `c(n) = a + d·n + e·n²` cost of one tick). [DB201 week 1, why persistence is hard in games](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (why the database is the source of truth when a process dies). From this course, [week 1, scale targets](w01-scale-targets-ccu-messages-and-n-squared.md) (the n-squared problem), [week 2, shards, realms, zones, instances, layers](w02-shards-realms-zones-instances-layers.md) (shards and zones as words) and [week 3, area of interest](w03-area-of-interest-grids-radius-hysteresis.md) (grid AOI with hysteresis).

**Interactive:** [examples/w04-zone-handoff.html](../examples/w04-zone-handoff.html). Keep it open during section 2.

---

## 1. What a zone server owns

In week 2 you met the vocabulary. A **shard** is a full copy of the world with its own players. A **zone** is a piece of one shard's map. This week is about how a shard's map is split across machines, and what happens at the seams.

A **zone server** is a process that simulates every entity inside one region of the map. It runs the tick, moves NPCs, resolves combat, and sends updates to the clients whose players stand in its region. Three terms carry the rest of the lecture.

- The **owner** of an entity is the one server allowed to change it. Owning means you run its AI, apply damage to it and write its position. At every instant, every entity has exactly one owner. Break that rule and you get the two classic seam bugs: an entity with two owners (a duplicate) or with none (a lost character).
- A **ghost** (also called a proxy or a mirror) is a read-only copy of an entity kept on a neighbouring server. Your week 3 AOI query asks "who is within 100 m of me?". If you stand 20 m from a border, part of that circle lies on another machine. The neighbour sends you ghosts of its entities near the border so your query can see them. Ghosts are never simulated, only updated.
- A **handoff** is the transfer of ownership from one zone server to another when an entity crosses a border. The old owner stops simulating it and the new owner starts. Done well, the player never notices.

A **static partition** fixes the borders at design time, often on a grid. A **dynamic partition** moves borders while the game runs, usually to split an overloaded zone or merge two empty ones. Most shipped MMOs are static, for reasons section 2 will make concrete.

## 2. Worked example: the boundary tax

### The hook

Second Life cuts its world into regions of exactly 256 m by 256 m, and one simulator process hosts each region. Drive a car with a passenger across a region line and you are testing one of the least reliable parts of the platform. The Second Life Wiki's own page on crossings calls the operation brittle and says vehicles carrying several avatars tend to be unreliable. It notes that at corners, where four regions meet, a second crossing can start before the first has finished, with results it describes as generally unsatisfactory. Linden Lab's engineers were not careless. They drew thousands of borders, and every border has a price. Here is how to compute it.

### The model

Take a square world of side `W` metres with `N` players spread across it, cut into a `g × g` grid of equal zones. Each zone is one server.

```
zones                      Z = g²
players per zone (even)    N / Z
total border length        L = 2 × W × (g − 1)
handoffs per second        H = (2 / π) × ρ × v × L          where ρ = N / W²
ghost fraction             G ≈ 2 × R × L / W²
```

- `v` is the average speed of a player in m/s, counting idle time. A player who runs half the time at 4 m/s and stands still the other half has `v = 2`.
- `ρ` is the density of players, per square metre.
- `R` is the AOI radius from week 3.
- `H` counts crossings in both directions. It comes from a result in physics about particles crossing a line. If players move in random directions, the number crossing a line of length `L` each second is `(2/π) ρ v L`. The `2/π` is the average of `|cos θ|` over all directions, because a player walking along the border does not cross it and a player walking straight at it does.
- `G` is the share of players standing within `R` of some border. Each of those must exist as a ghost on at least one neighbour. It ignores corners, which is fine while `R` is much smaller than a zone.

The grid is the simplest partition. The first line tells you what you gain from more zones. The next three tell you what you pay. Notice that the price grows with `g` while the gain in players per zone shrinks as `1/g²`.

### Numbers you can check

Take a shard of `N = 3,000` players in a `W = 6,000` m (6 km) world, moving at an average `v = 2` m/s, with an AOI radius `R = 100` m. Then `ρ = 3,000 / 36,000,000 = 8.33 × 10⁻⁵` per m², and `H` simplifies to `(4/π) × (g − 1) = 1.27 × (g − 1)` handoffs per second.

| Grid `g` | Zones | Players per zone (even) | Border length (m) | Handoffs/s | Ghost fraction |
|---|---|---|---|---|---|
| 1 | 1 | 3,000 | 0 | 0 | 0% |
| 2 | 4 | 750 | 12,000 | 1.27 | 6.7% |
| 3 | 9 | 333 | 24,000 | 2.55 | 13.3% |
| 4 | 16 | 188 | 36,000 | 3.82 | 20.0% |
| 6 | 36 | 83 | 60,000 | 6.37 | 33.3% |
| 8 | 64 | 47 | 84,000 | 8.91 | 46.7% |

Check one row by hand. At `g = 4`, `L = 2 × 6,000 × 3 = 36,000` m. `H = 0.6366 × 8.33 × 10⁻⁵ × 2 × 36,000 = 3.82`. `G = 2 × 100 × 36,000 / 36,000,000 = 0.20`.

I checked the handoff formula with a simulation. Three thousand random walkers on this map, run for 1,500 simulated seconds, produced 1.28 handoffs per second at `g = 2` and 3.79 at `g = 4`. The formula says 1.27 and 3.82.

So far the grid looks healthy. Four handoffs a second is nothing for a data centre, and each zone holds under 200 players. Now make the world look like a real MMO.

### Add a capital city

Real players are not spread evenly. They gather in the capital, at the auction house, at the world boss. Put 40% of the shard in one city of radius 300 m, and spread the other 60% evenly. If the whole city sits inside one zone, that zone holds

```
max zone load = f × N + (1 − f) × N / g²       with f = 0.4
```

| Grid `g` | Zones | Busiest zone | Quietest zones |
|---|---|---|---|
| 1 | 1 | 3,000 | — |
| 2 | 4 | 1,650 | 450 |
| 4 | 16 | 1,313 | 113 |
| 8 | 64 | 1,228 | 28 |
| 100 | 10,000 | 1,200 | 0.2 |

Suppose one zone server can hold 1,000 players at your tick rate (week 5 shows how to find that number). No grid ever fits. Going from 4 to 64 servers, sixteen times the hardware, lowers the busiest zone by 85 players, about 6%. Meanwhile handoffs among the 60% who live outside the city rise from 2.3 to 5.3 per second (`0.6 × 3.82` and `0.6 × 8.91`), and the ghost fraction of the countryside climbs from 20% to 47%. **The crowd sets a floor that no number of zones can go under.**

Open the interactive. Drag the grid slider from 2 to 8 with the city on. The left map fills with border lines and ghost markers, while the bar chart on the right barely moves. One red bar stays above the capacity line.

### Cut the city in half?

The obvious fix is to put a border through the city, so two servers share it. Price that border. Inside the city the density is `ρ = 1,200 / (π × 300²) = 0.0042` per m², fifty times the countryside. People in town walk slowly, say `v = 1` m/s. One straight border through the centre is 600 m long.

```
handoffs from that one border  = 0.6366 × 0.0042 × 1 × 600 = 1.62 per second
players within 100 m of it     ≈ 0.0042 × (200 × 600) = 509
```

One short line in the city costs 71% as many handoffs as the entire 36 km of countryside border at `g = 4` (2.29 per second with the city on), and 42% of what that grid would cost with the whole shard spread evenly (3.82). And 509 of the city's 1,200 players, 42% of them, now must be ghosted to the other half, updated every tick, because everybody's AOI circle crosses the line. You have halved the owners per server but each server still sees most of the crowd. Its AOI and replication work, the `e × n × k` term from CS202 week 13, hardly drops.

That is the lesson of the example. **A border is cheap where nobody stands and expensive where everybody stands.** The zone layout that minimises cost puts borders in empty places, and the crowd has to be handled some other way.

### Same idea elsewhere

**Second Life (Linden Lab, current wiki).** The purest grid. Every region is 256 m square, and each is hosted by one simulator process. In our form, `W / g = 256` is fixed forever, so the border length grows in direct proportion to the land area. A crossing triggers when the root of an object is one metre past the edge, which is a hysteresis band of only one metre (section 4 shows why that is small). And the wiki's warning about four-region corners is our `G` term in its worst case. Near a corner, an object is a ghost on three neighbours at once, and a second handoff can start before the first commits.

**EVE Online (CCP, current mechanics and the 2015 hardware blog).** EVE's zone is the solar system, and a server node hosts many of them. The EVE University wiki says a typical node handles hundreds of systems. The borders between systems are stargates, and they are not places in space. You cannot drift across one. You jump, and you arrive 12 km from the far gate. In our model this sets `L` to zero between zones and replaces continuous crossings with discrete, requested ones, so there are no ghosts across systems at all. EVE also hides the handoff. After a jump you get a 60-second jump cloak, which the wiki explains exists so the arriving player has time to load the system before anyone can shoot them. For crowds, EVE does not cut the system. In its 2015 Tranquility Tech III blog, CCP described one special "Everest" node assigned to the highest-load situations, typically the biggest fleet battles, and planned to have six such nodes. That is the crowd floor handled with bigger hardware instead of more borders. When even that is not enough, EVE slows time (week 12).

**Old School RuneScape (Jagex, current).** OSRS takes `g = 1` and multiplies shards instead. Each members' world holds up to 2,000 players and simulates the whole map on one clock. The OSRS Wiki notes that a tick lasts the same for every player on a world, and that ticks run slightly longer on the fullest worlds. There are no zone borders, so `H = 0` and `G = 0`. The cost moves to the crowd floor. The whole world is the busiest zone, so the cap is on the world. The handoff still exists, but the player triggers it. Moving to another world, called world hopping, is a logout and login on a different server.

Three games, one trade-off. Second Life pays in border length. EVE removes continuous borders and pays in hardware for hot spots. OSRS removes borders entirely and pays with a hard population cap. When you meet a new MMO's topology, ask the model's questions: how long are the borders, how dense is the traffic across them, and where does the crowd go?

### Design judgment

- **Draw borders where players are not.** Mountain ridges, oceans, a narrow pass, a portal. A border along a mountain ridge has a small `ρ v` across it, and a portal makes `L` zero.
- **Never cut a city.** If one zone cannot hold the crowd, the fix is capacity (a bigger node for that zone), layering (week 2), or a softer game rule that spreads people (more auction houses, several banks), not a border through the market square.
- **Prefer fewer, bigger zones until the crowd floor bites.** The table shows the gain from zones falls off as `1/g²` while border costs climb as `g`. Past the point where the busiest zone stops shrinking, extra servers buy you seams.
- **Hide the seam in the fiction when you can.** A loading screen, a gate, a boat ride. Seamless worlds are a feature players value, and they cost engineering time at every border forever. Decide that you want it, instead of assuming it.

### Check this example

1. A shard has 5,000 players in a 10 km square world, `v = 1.5` m/s, on a `5 × 5` grid. Compute the handoffs per second and the ghost fraction with `R = 80` m.
2. In the capital-city table, what share of the shard `f` would let a `4 × 4` grid keep every zone under 1,000 players?
3. A designer halves the world's side `W` for the same `N` and `g`. What happens to `H`? Explain in one sentence using the formula.

<details>
<summary>Answers</summary>

1. `L = 2 × 10,000 × 4 = 80,000` m, `ρ = 5,000 / 10⁸ = 5 × 10⁻⁵`. `H = 0.6366 × 5 × 10⁻⁵ × 1.5 × 80,000 = 3.82` per second. `G = 2 × 80 × 80,000 / 10⁸ = 0.128`, so 12.8%.
2. `f × 3,000 + (1 − f) × 3,000 / 16 < 1,000`. That is `187.5 + 2,812.5 f < 1,000`, so `f < 0.289`. The city may hold at most about 28.9% of the shard.
3. `L` halves (it is proportional to `W`) but `ρ` quadruples (it is `N/W²`), so `H` doubles. Denser worlds cross borders more often.

</details>

## 3. Static or dynamic borders

A dynamic partition answers the crowd by moving borders. The usual structure is a tree. Start with one zone. When a zone's load passes a threshold, split it in two along the axis that balances the load, and give one half to a fresh server. When two sibling zones fall below a lower threshold, merge them. A quadtree splits into four at a time. A k-d tree splits into two and alternates axes.

Dynamic partitions solve the problem static grids cannot: 1,000 players spread across a battlefield can get four servers, then give them back at midnight. But section 2 already showed you the price. The split lands exactly where the crowd is, so the new border sits in the densest part of the map, with the highest `ρ` and the most ghosts. Moving a border also means handing off every entity in the strip that changed sides, all at once. A border that moves 50 m through the city centre hands off `0.0042 × 50 × 600 ≈ 127` players in one tick.

Use two thresholds with a gap between them, for example split above 900 and merge below 500. With one threshold, a zone at 899 players that gains two would split, lose a few to its new sibling and merge again on the next check. This is the same hysteresis idea as in week 3's AOI and in section 4 below. You will see it in almost every control loop in this course.

When is the dynamic partition worth it? When crowds are large, move around, and the game cannot hide them behind loading screens. Large open-world battle games with sieges are the classic case. For a city that never moves, a fixed bigger server is simpler and more reliable.

## 4. The handoff protocol

A handoff is a small distributed transaction. It must keep the single-owner rule even if a message is lost or a server crashes in the middle. Here is the version you will build in lab. Server A owns player P, who has just crossed into B's zone.

1. **Decide.** A sees P's position is past the border plus the hysteresis margin. A marks P as "leaving" and stops applying P's inputs. New inputs from P are buffered, not dropped.
2. **Serialize.** A packs P's live state: position, velocity, health, buffs with their remaining times, cooldowns, target, threat tables. A does not pack the inventory. Items live in the database and are referenced by ID (week 8 explains why you never ship item ownership inside a handoff message).
3. **Offer.** A sends `HANDOFF(P, state, seq)` to B. The sequence number `seq` increases every time P changes owner.
4. **Accept.** B creates P from the state, becomes the owner, and replies `ACK(P, seq)`. From this moment B simulates P.
5. **Release.** On the ACK, A turns its copy of P into a ghost, forwards the buffered inputs to B, and tells the gateway (week 9) to route P's traffic to B.
6. **Tell the client.** B's next update to P's client carries the new owner. The client does not reconnect. It keeps talking to the gateway.

In a data centre, the whole exchange is a few messages at under a millisecond each. At 10 ticks per second there is 100 ms between ticks, so if A decides at the end of a tick and B accepts before its next tick begins, P misses no ticks at all. The latency is not the problem. The failures are.

| Failure | What goes wrong without care | The rule that prevents it |
|---|---|---|
| The ACK is lost | A never releases and P has no owner; or A times out, takes P back while B also owns P | A may only retake P by sending B a `REVOKE(P, seq)` that B acknowledges. Owners change only through acknowledged messages. |
| B crashes after ACK | P lived only in B's memory | Periodic saves (week 7) bound the loss. P reloads from the last save on login. |
| A crashes before sending | P is gone from A | Same as above. A handoff never moves data the database does not already have for durable state. |
| Two borders at once (a corner) | P is offered to B and C | A sends one offer at a time. P stays "leaving" until one handoff completes. |
| Stale message arrives late | An old `HANDOFF` for P overwrites a newer state | B rejects any message whose `seq` is not greater than the last one it saw for P. |

Notice the pattern. Every rule makes ownership a fact that two servers agreed on with numbered messages, and it puts anything that must survive a crash into the database. That is the same reasoning as DB201's transactions, applied to live memory.

### Ping-pong and the hysteresis band

A player who stands on a border and shuffles about will cross it back and forth. Every crossing is a handoff, and each handoff is a small risk. The fix from week 3 applies here too. Do not hand P from A to B when P crosses the line. Hand P over only when P is `h/2` metres past it, and hand P back only when P is `h/2` metres past it the other way. Inside the band of width `h`, the current owner keeps P.

How much does that matter? Take 40 players milling within 5 m of a border, perhaps around a quest giver someone placed on the line. Each wanders randomly, about half a metre per second, and the server checks ownership on every tick. I simulated it.

| Band `h` | Handoffs/s, checked 1×/s | Handoffs/s, checked 10×/s |
|---|---|---|
| 0 m | 1.60 | 4.91 |
| 1 m | 0.64 | — |
| 2 m | 0.39 | 0.45 |
| 4 m | 0.22 | — |
| 8 m | 0.11 | 0.13 |

With no band and checks every tick, those 40 idle players cause 4.9 handoffs a second. That is more than all 3,000 players travelling across the whole `g = 4` grid when they are spread evenly (3.8). A 2 m band cuts it by a factor of eleven. Without a band, checking more often makes it worse, because a random walk crosses a line more times the more closely you look. With a band, the check rate barely matters.

Second Life's one-metre trigger is a band of 1 m on each side of the line, a total of `h = 2` m in our terms. That is enough for someone standing still. It is not enough for a vehicle bouncing along a border at speed, which fits the wiki's warning about vehicles.

## In-class activity (25 minutes)

In groups of three, you are the server team for a new MMO. The world is 8 km by 8 km. The design team expects 4,000 players per shard at peak, with a capital city holding 30% of them and a world boss that can draw 400 players into one 200 m circle anywhere on the map. One zone server holds 900 players.

1. Pick a static layout (grid size, or hand-drawn regions on the provided map sketch). Compute `H`, `G` and the busiest zone for your layout, using `v = 2` m/s and `R = 100` m.
2. Decide how you handle the world boss crowd. It may appear on a border.
3. Choose a hysteresis band and say why.
4. Trade with another group. Find the one moment in a week of play where their design fails, and estimate the numbers at that moment.

Expected output: a one-page sketch with the layout, the three computed numbers, the boss plan, and the failure your partners found.

## Common misconceptions

- **"More zone servers means more capacity."** Only for spread-out players. When a fraction `f` of the shard gathers in one place, the busiest zone never drops below `f × N`, and more zones add borders.
- **"Handoffs are expensive because of the data they move."** A player's live state is a few kilobytes, and four a second is nothing. The cost is the correctness work: a protocol that never leaves an entity with zero or two owners.
- **"Ghosts are free because they are not simulated."** They must be updated every tick and they take part in every AOI query that reaches across the border. Near a crowd, the ghost set can be as large as the owned set.
- **"Seamless worlds are strictly better than loading screens."** A loading screen or a gate is a zero-length border. It trades a moment of immersion for the removal of an entire class of bugs.

## Check yourself

1. A 2,000-player shard in a 4 km world uses a `3 × 3` grid, and players average 2.5 m/s. How many handoffs per second? If the team adds a flying mount that doubles average speed, what happens to that number?
2. A zone server's tick cost is `c = 1 + 0.01 n` ms for `n` owned players plus `0.002 m` ms for `m` ghosts. With 600 owned players and 25% of them duplicated as ghosts on neighbours (so each server also holds about 150 ghosts from others), what is the tick cost? How many owned players fit in a 50 ms budget if the ghost share stays at 25%?
3. Explain why a handoff message carries a sequence number, using a concrete sequence of three messages that goes wrong without it.

<details>
<summary>Answers</summary>

1. `L = 2 × 4,000 × 2 = 16,000` m, `ρ = 2,000 / 1.6 × 10⁷ = 1.25 × 10⁻⁴`. `H = 0.6366 × 1.25 × 10⁻⁴ × 2.5 × 16,000 = 3.18` per second. `H` is proportional to `v`, so doubling speed doubles it to 6.37.
2. `c = 1 + 6 + 0.3 = 7.3` ms. With `m = 0.25 n`, `c = 1 + 0.01n + 0.0005n = 1 + 0.0105 n ≤ 50`, so `n ≤ 4,666`. The ghosts cost 5% of per-player work here. They matter far more when the ghost share is 40% and the per-ghost cost includes AOI work.
3. A hands P to B with `HANDOFF seq 5`. The ACK is slow, so A retransmits the same message, and the network holds that second copy back. B accepts the first copy, P walks back across the border, and B hands P to A with `HANDOFF seq 6`. Now the delayed duplicate of seq 5 reaches B. Without sequence numbers, B re-creates P from the older state and both servers own P. With them, B has already recorded seq 6 for P, sees `5 ≤ 6`, and rejects the duplicate.

</details>

## Lab / assignment hook

[Lab 04, zone handoff simulator](../labs/lab04.md). You run a random-walk shard over a zone grid, check the handoff formula against the simulation, add a capital city and measure the busiest zone, then implement the hysteresis band and the numbered handoff protocol and show that a lost or reordered message never produces two owners. It feeds the zone layer of your final world server.

## Sources

- Second Life Wiki, "Region" (accessed September 2026). A region is 256 m by 256 m (65,536 m²) and is hosted by a single simulator process; one server process can host several regions.
- Second Life Wiki, "Region crossing" (accessed September 2026). A crossing triggers when the root prim's centre is one metre past the edge; the losing simulator sends the object to the gaining one; the page calls the operation brittle, calls multi-avatar vehicle crossings unreliable, and describes double crossings at corners. Paraphrased.
- EVE University Wiki, "Server tick" (accessed September 2026). A typical server node handles hundreds of systems.
- EVE University Wiki, "Stargates" (accessed September 2026). Arrival 12 km from the gate; the 60-second jump cloak exists so arriving pilots can load the system.
- CCP Gun Show, "Tranquility Tech III" (EVE Online news, 14 October 2015). The single "Everest" node assigned to the highest-load situations, typically the biggest fleet battles; six Everest nodes planned for TQ Tech III; standard and enhanced SOL nodes.
- Old School RuneScape Wiki, "Server" and "Game tick" (accessed September 2026). Members' worlds allow 2,000 players (free-to-play worlds 1,400); several worlds can share one physical server; tick length is constant across a world and longer on full worlds.
- Alexander, T. (ed.) (2003). *Massively Multiplayer Game Development*. Charles River Media.
- The crossing-rate result `(2/π) ρ v L` for randomly oriented motion is standard kinetic theory; the simulations quoted in this lecture were run for this course and can be repeated with the lab 04 starter code.

## Interactive spec: examples/w04-zone-handoff.html

**Insight the visual must make obvious:** adding zone servers shrinks the busiest zone only while players are spread out. With a city on, the busiest bar stays above the capacity line whatever the grid, while handoffs and ghosts climb with every border you add. A border through the crowd is far more expensive than many borders through empty land.

**Layout.** Two linked views and a number panel. Desktop: map on the left, bars on the right, panel beneath. Under 700 px: stacked, map first.

1. **Map (left).** A square world, side `W = 6,000` m, drawn as a square canvas. `N` dots (default 3,000) move by random walk. Grid lines for the current `g`. Each dot is coloured by its owning zone (use a repeating 4-colour pattern from the shared palette so neighbours differ). Dots that are ghosts somewhere (within `R` of a border) get a hollow ring. A shaded strip of width `h` around each border shows the hysteresis band (visible only if `h ≥ 20` m at the map scale, else draw a thin line and state the band in the panel). When the city is on, draw a faint circle of radius 300 m at the city centre.
2. **Zone bars (right).** One bar per zone, sorted by load, height = owned players. Horizontal dashed line at the capacity `C`. Bars above `C` are red. Label the busiest bar with its count. Above the bars, a small line chart (last 60 s) of handoffs per second, measured, with the predicted `H` as a dashed horizontal line.
3. **Number panel.** Zones `g²`; border length `L`; predicted `H`; measured `H` (60 s moving average); ghost fraction predicted `G` and measured; busiest zone predicted and measured; handoffs in the last second caused by ping-pong (a handoff back to the previous owner within 5 s).

**Controls.**
- Slider `g`, 1 to 8, default 4.
- Slider `N`, 500 to 6,000, step 100, default 3,000.
- Slider `v`, 0.5 to 6 m/s, step 0.5, default 2.
- Slider `R`, 25 to 200 m, default 100.
- Toggle "Capital city" (default on) with slider `f`, 0 to 0.6, default 0.4. City dots walk inside the 300 m circle at `v_city = 1` m/s and reflect at its edge.
- Toggle "Border through the city" (default off). When on, keep the grid fixed and move the city centre onto the vertical border nearest the map centre (relative to the city this is the same as shifting the grid, and it keeps `L = 2W(g − 1)` exact).
- Slider hysteresis `h`, 0 to 20 m, default 2.
- Slider capacity `C`, 200 to 2,000, default 1,000.
- Button "Idle crowd on a border": adds 40 dots confined to ±5 m of the border nearest the map centre, random walk with σ = 0.5 m per second, and shows their handoffs separately.
- Play/pause, and a speed selector (1×, 10×, 60× simulated time). Respect `prefers-reduced-motion` by starting paused.
- All sliders keyboard accessible (arrows ±1 step, Page Up/Down ±10 steps).

**Formulas.** Countryside players: uniform start, heading uniform in `[0, 2π)`, each simulated second move `v` metres and re-draw heading with probability 0.02; wrap at the world edge (torus) and do not count wrap moves as crossings. `ρ = N_country / W²` for the prediction when the city is on, and `H_pred = (2/π) × ρ × v × L + H_city`, where `H_city = (2/π) × ρ_city × v_city × L_city`, `ρ_city = f N / (π × 300²)`, and `L_city` is the length of border lying inside the city circle (0 unless a border passes through it; 600 m for a line through the centre). `L = 2W(g − 1)`. `G_pred = 2 R L / W²` (countryside only), plus `ρ_city × 2R × L_city` ghosts from the city. Busiest zone predicted: `f N + (1 − f) N / g²` when the city is inside one zone. Ownership with hysteresis: an entity owned by zone A moves to zone B only when its position is inside B and at least `h/2` from A's border; check once per simulated 0.1 s.

**Test values** (assert on load with a fixed random seed and the formulas above, not the simulation).
- `N = 3,000`, `W = 6,000`, `v = 2`, city off: `g = 2` gives `H = 1.27`, `G = 6.7%`; `g = 4` gives `H = 3.82`, `G = 20.0%`; `g = 8` gives `H = 8.91`, `G = 46.7%`.
- City on, `f = 0.4`: busiest zone 1,650 at `g = 2`, 1,313 at `g = 4`, 1,228 at `g = 8`.
- City density `0.00424` per m²; border through the city centre adds `1.62` handoffs/s and about 509 ghosts.
- Idle crowd, 40 players, checks at 10 Hz: about 4.9 handoffs/s at `h = 0`, 0.45 at `h = 2`, 0.13 at `h = 8` (simulation; allow ±15%).

**First screen:** `g = 4`, city on with `f = 0.4`, running. Caption: "16 zone servers, 2.3 handoffs a second, and one zone still holds 1,313 players. Drag the grid to 8 and watch which number moves."
