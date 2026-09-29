# MMO404 · Week 01 — Limits of the zone model

**Why this matters:** Almost every MMO you have played splits its world into zones and gives each zone to one server. That design works until players decide, all at once, to stand in the same place. This week you learn to predict exactly when a zone server fails, why buying a faster machine barely helps, and which escape route each shipped game took.

**You will be able to:**
- Compute a zone server's tick time from player count, hot-spot share and area of interest, and solve for its capacity.
- Explain why a zone's capacity depends on density rather than headcount, and why doubling CPU raises crowded capacity by about 1.4 times, not 2.
- Rewrite layering, time dilation and region caps as changes to one term of the same tick-cost model.
- Critique a zone layout by finding its overload case and its idle hardware.

**Before class:** Reread your notes from MMO302 weeks 1, 2 and 4 (scale targets, zones and shards, zone handoff). CCP Games, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), the whole post. De Vleeschauwer et al., "Dynamic microcell assignment for massively multiplayer online gaming" (NetGames 2005), sections 1 and 2 only.

**Prerequisites from earlier courses:** [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the `n²` bandwidth wall and the CPU tick budget). [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) (the dedicated server). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). MMO302 [week 1, scale targets](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md), [week 2, shards, zones and layers](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md), [week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md), [week 4, zone servers and handoff](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) and [week 12, single-shard architectures and time dilation](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md). [MMO301 week 6, EVE Online as a single shard](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md).

**Interactive:** [examples/w01-zone-hotspot.html](../examples/w01-zone-hotspot.html). Keep it open during section 2.

---

## 1. What the zone model promises

In MMO302 you built a world the standard way. You cut the map into regions, and each region, called a **zone**, belongs to exactly one **zone server**. The zone server is the authority for everything inside its borders. It reads player inputs, moves characters, runs monster AI, resolves combat and sends each client the part of the world near it. When a player walks off the edge, the zone hands the character to the neighbour, often behind a loading screen.

The model makes three promises.

- **Capacity adds up.** Ten zones on ten servers hold ten times the players of one.
- **Each server's work is local.** A zone server only has to think about what is inside its borders.
- **Capacity is a headcount.** You can write "this zone holds 1,000 players" on a planning sheet and admit players until the counter hits it.

All three are true on average and false at the moments that matter. This course is about those moments. Weeks 2 to 13 each attack one broken promise. This week you measure how badly they break.

Two terms first. A **tick** is one step of the server simulation, run at a fixed rate (CS202 week 13). At 10 ticks per second a tick lasts 100 ms, and the server must finish all its work inside that time or the world slows down. We keep half of it free for spikes, garbage collection and the operating system, so the **tick budget** in this lecture is 50 ms. The **area of interest** (AOI) of a player is the region around them whose contents they need to know about, here a circle of radius `R` (MMO302 week 3). Two players are an **interacting pair** if each is inside the other's AOI, so the server must check, replicate and resolve things between them every tick.

## 2. Worked example: the town square that breaks a 1,000-player zone

### The hook

On 27 January 2014, a missed sovereignty payment in EVE Online started a fight in a system called B-R5RB. Neither side had planned it for that day. Within hours, 2,670 pilots were in that one system, and the battle ran for about 21 hours. For most of it the game ran at 10% speed, so one second of game time took ten seconds of real time.

Here is the puzzle. EVE's cluster, Tranquility, hosts the whole universe as one shard, and on that day the rest of it kept running at normal speed. The EVE University wiki describes Tranquility as a set of nodes, each machine hosting a part of New Eden, and time dilation acts per node. So the hardware as a whole had capacity to spare. One node did not. Nobody ran out of servers. They ran out of one server, because the players chose where to stand.

Five years later, World of Warcraft Classic launched in August 2019 (patch 1.13.2) with a different fix for the same problem. Blizzard ran several copies of each realm's outdoor world, called **layers**, and put crowds in different copies. Players on one layer could not see players on another. By 13 November 2019 every realm was down to a single layer. Both studios were fighting the same term in the same formula.

### The model

A zone server's tick has two kinds of work. Some work is per player: reading inputs, moving the character, running its buffs. Some is per interacting pair: visibility checks, replicating each character to the other, resolving area effects and collisions. Write the tick time as

```
C(n) = c_p × n + c_i × P
```

- `n` is the number of players in the zone.
- `c_p` is the CPU time per player per tick. We use 20 µs.
- `P` is the number of **ordered** interacting pairs. If Ana sees Ben and Ben sees Ana, that counts twice, because the server replicates Ana to Ben and Ben to Ana.
- `c_i` is the CPU time per ordered pair per tick. We use 2 µs.

The constants are invented for teaching, but their ratio is realistic. One pair is cheap compared with one player. There are just far more pairs than players. The pair term is the `g(g − 1)` delivery count from [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md), priced in CPU time. What this week adds is where the pairs come from inside one zone, and what that does to the zone's capacity.

Everything interesting is in `P`. Take a square zone of side 2 km with an AOI radius `R` of 100 m. One player's AOI disc covers a fraction of the zone:

```
f = π R² / A = π × 100² / 2000² = 0.00785
```

If players spread evenly, each one sees about `f × n` others, so `P ≈ n² × f`. Now suppose a share `h` of the players (the **hot-spot share**) crowds into one spot smaller than the AOI, a bank, an auction house, a boss spawn, and so everyone there sees everyone else there. The rest stay spread out. Counting the pairs inside the crowd, among the spread players, and between the two groups gives

```
P ≈ n² × (h² + (1 − h²) × f)
C(n, h) = c_p × n + c_i × n² × (h² + (1 − h²) × f)
```

When `h = 0` the pair fraction is just `f`, less than 1%. When `h = 1` it is 1, every player sees every other. That factor of 127 between the two cases is the whole lecture.

The zone's **capacity** is the largest `n` whose tick fits the budget `B`. Set `C(n, h) = B` and solve the quadratic `a n² + b n − B = 0`, with `a = c_i × (h² + (1 − h²) f)` and `b = c_p`:

```
n_max = (−b + √(b² + 4 a B)) / (2a)
```

### Numbers you can check

With `c_p = 20 µs`, `c_i = 2 µs`, `B = 50 ms` and the 2 km zone:

| Hot-spot share `h` | Pair fraction | Tick at 1,000 players | Capacity | Capacity with 2× CPU |
|---|---|---|---|---|
| 0 (spread out) | 0.00785 | 35.7 ms | 1,258 | 1,966 |
| 0.1 | 0.0178 | 55.6 ms | 938 | 1,419 |
| 0.25 | 0.0699 | 159.7 ms | 531 | 777 |
| 0.5 | 0.256 | 531.8 ms | 294 | 423 |
| 1 (one crowd) | 1 | 2,020 ms | 153 | 219 |

Check two cells by hand. At `h = 0` and 1,000 players, per-player work is `20 µs × 1,000 = 20 ms`, and pair work is `2 µs × 1,000,000 × 0.00785 = 15.7 ms`, so the tick takes 35.7 ms and fits. At `h = 1` the capacity solves `2×10⁻⁶ n² + 2×10⁻⁵ n = 0.05`, which is `n² + 10 n − 25,000 = 0`, so `n = (−10 + √100,100) / 2 = 153`.

Three things stand out.

- **The same zone holds 1,258 players or 153, depending on where they stand.** Nothing about the hardware or the code changed between those rows. A capacity written as a headcount is a guess about player behaviour.
- **A small crowd costs a lot.** Moving 10% of the players into one spot drops the capacity by a quarter. Moving 25% there more than halves it. Because pairs grow as `h²`, the first people to gather are cheap and each later one is more expensive than the last.
- **A machine twice as fast buys 1.56× the capacity when players spread out and only 1.43× in one crowd.** Once the pair term dominates, capacity grows as the square root of CPU speed. To double a crowded zone's capacity you need a server about four times faster. No such server exists on the price list, which is why every studio in this lecture changed the model instead of the hardware.

Here is the model as code. It is the core of Lab 01.

```python
import math

C_P, C_I = 20e-6, 2e-6      # CPU seconds per player and per interacting pair, per tick
BUDGET = 0.050              # usable seconds per tick at 10 Hz
f = math.pi * 100**2 / 2000**2

def tick_ms(n, h, c_p=C_P, c_i=C_I):
    return 1000 * (c_p * n + c_i * n * n * (h * h + (1 - h * h) * f))

def capacity(h, c_p=C_P, c_i=C_I, budget=BUDGET):
    a, b = c_i * (h * h + (1 - h * h) * f), c_p
    return (-b + math.sqrt(b * b + 4 * a * budget)) / (2 * a)

for h in (0.0, 0.1, 0.25, 0.5, 1.0):
    print(f"h={h:<4}  tick(1000)={tick_ms(1000, h):7.1f} ms  capacity={capacity(h):5.0f}"
          f"  with 2x CPU={capacity(h, C_P / 2, C_I / 2):5.0f}")
```

It prints the table above, one row per `h`, ending with `h=1.0   tick(1000)= 2020.0 ms  capacity=  153  with 2x CPU=  219`.

Is the formula honest? Lab 01 places 1,000 players on a seeded map, counts the real pairs with a spatial grid and compares. The measured count is 7% below the model when players spread out, because players near the zone's edge have part of their AOI outside the map. With a crowd, the error falls under 2%. That is close enough to plan with, and the error runs in the safe direction.

### Move it yourself

Open `examples/w01-zone-hotspot.html`. The left view is the zone from above, with one dot per player and the AOI circle of one player drawn. The right view is a bar showing the tick time, split into its per-player and per-pair parts, against lines at the 50 ms budget and the 100 ms tick. Start at 1,000 players and `h = 0`. The bar sits at 35.7 ms. Now drag the hot-spot slider slowly toward 0.25. On the left, only a quarter of the dots move, and the map still looks mostly empty. On the right, the pair part of the bar grows until the tick is past 150 ms. The map shows where players are. The bar shows what they cost, and the two views disagree about how bad things are. Then toggle "2× CPU" and watch how little the crowded bar shrinks compared with the spread one.

### Same idea elsewhere

Each of these games changed one letter in `C(n, h)`. Learning to name the letter is the skill.

**EVE Online, time dilation (dev blog April 2011, current mechanic).** Time dilation slows the game clock on an overloaded node, down to a floor of 10% speed. In our model, that stretches the budget `B`. At 10% speed a 100 ms tick of game time gets 1,000 ms of real time, so the usable budget grows tenfold, from 50 to 500 ms. Solve the capacity for `h = 1` with `B = 0.5 s` and you get 495 pilots instead of 153. Ten times the time buys about 3.2 times the players, the same square-root law as buying CPU. B-R5RB's 2,670 pilots were more than five times that, which is why the fight sat at the 10% floor for most of a day. The EVE University wiki notes that server load grows as `O(n²)` with players on grid, which is our pair term.

**World of Warcraft Classic, layering (August to November 2019).** Layering splits the players into `k` copies of the world. Each copy runs the same formula with `n / k` players, so the pair work in each copy falls by `k²` and the total pair work across all copies falls by `k`. A crowd of 1,000 players with `h = 0.25` costs 159.7 ms on one layer. Split into three layers of 333, each layer costs 22.2 ms, and the three together cost 66.6 ms. Layering removes pairs rather than moving them, so the total work goes down. The price is social. Players on different layers cannot see, group with or fight each other, and the game had to teach them that joining a party moves you to the leader's layer.

**World of Warcraft, sharding and cross-realm zones (retail; cross-realm zones since patch 5.0.4, 2012).** Retail WoW applies the layering idea per zone or smaller, automatically, when an area gets crowded. Wowpedia notes that the shard borders are invisible and that players may see NPCs vanish for a moment when the game moves them. Cross-realm zones solve the opposite problem. When a low-level zone is nearly empty on every realm, the game merges several realms' players into one copy. In our model, CRZ raises `n` on purpose because an empty zone has a design cost even when its CPU cost is near zero. Section 3 returns to that.

**Second Life (Linden Lab, current).** The Second Life wiki describes the world as regions of 256 m × 256 m, each run by a simulator process. A full region admits at most 100 avatars, and mainland regions at most 40. That is capacity written as a hard headcount per fixed area, enforced at the door. In our model, the cap bounds `n`, and the small region bounds how spread out anyone can be, since a 256 m square is barely wider than two 100 m AOIs. Every avatar in a busy region is close to every other, so the region is effectively always at `h` near 1, and 100 avatars is a cap that holds in the worst case.

Four games, one tick-cost model. When you meet a new game's crowd policy, ask which term it attacks: the players per server `n`, the pairs through `h` or `R`, the budget `B`, or the admission count.

### Design judgment

- **Plan capacity for the densest moment your design invites, not the average.** Your content decides `h`. A single auction house, a world boss with a fixed spawn point, a festival in one city and a siege of one castle all raise `h`. If you want those features, budget the zone at `h = 0.25` or worse, or give it a way to shed pairs.
- **Prefer levers that cut pairs over levers that add CPU.** CPU speed and time buy capacity at the square root. Copies (layers, shards, instances) and smaller interaction radii cut the pair term directly. Each has a design cost you should name out loud. Copies split the community, and a smaller radius means players cannot see as far.
- **Decide what fails first.** When the tick overruns, something gives. The world can slow for everyone (EVE's choice), players can be refused entry (Second Life), they can be moved to a copy (WoW), or updates can be dropped for the least important entities (week 4). Choose deliberately and tell players, because an unexplained failure is always worse.
- **Beware the fixed-price feature.** A feature priced per player looks cheap on the planning sheet. A feature priced per pair is cheap for the average zone and ruinous for the crowded one. Ask of every new system, does it cost per player or per pair?

## 3. Three more limits of the zone model

The hot spot is the famous limit. Three quieter ones matter as much when you plan a real world.

### Idle hardware

Zones are fixed in space, and players are not. [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) showed this as a headcount, with a capital city that no grid could fit. Here you price it in tick time. Take a world of 8 zones on 8 servers, sized so that each zone holds 1,258 spread-out players. At evening peak 4,000 players are online. One zone is the capital and holds 1,000 of them, a quarter at the bank (`h = 0.25`). The other 3,000 spread over the remaining seven zones, about 429 each.

- The capital's tick costs 159.7 ms, more than three times its budget.
- Each quiet zone's tick costs `20 µs × 429 + 2 µs × 429² × 0.00785`, about 8.6 + 2.9 = 11.5 ms. That is 23% of its budget.
- Averaged over the cluster, the servers are 60% busy: `(159.7 + 7 × 11.5) / (8 × 50)`.

A capacity dashboard showing the cluster average would say "60%, healthy". The capital's players are lagging. Seven machines are mostly idle, and none of them can help, because the zone model ties work to a place and the place is already assigned. Week 3 attacks this directly by letting the boundaries move.

### Seams

A zone border is a line the players cannot see and the servers cannot ignore. A player standing one metre inside zone A can see a player one metre inside zone B, so A must know about B's player. Either the servers exchange copies of entities near the border, or the game hides the border with a loading screen, a mountain range or a corridor. The first costs CPU and bandwidth on both servers. The second costs the illusion of one world. When a character walks back and forth over the line, each crossing is a transfer of authority, and a bug in that transfer can duplicate an item or lose a character. Week 2 prices the seam and designs a transfer that cannot duplicate.

### Emptiness

The zone model also fails in the other direction. A low-level zone two years after launch may hold three players on a realm. Its CPU cost is near zero, but its design cost is high. Group quests fail, the world feels dead, and the social ties that keep players in an MMO never form. MMO301 treated this as a design problem. Here it is an architecture one. The zone model assigns hardware and players to places at the same time, so it cannot move players between copies of a place to reach a healthy density. WoW's cross-realm zones and connected realms exist for this reason. A modern design wants both directions. It sheds pairs when a place is crowded and merges copies when it is empty.

## 4. The escape routes, and the map of this course

Every technique in this course changes one assumption of the zone model. Here they are in the terms of the tick-cost formula, with the week that treats each one.

| Escape route | What it changes in `C(n, h)` | Price | Weeks |
|---|---|---|---|
| Seamless borders with ghosts | Removes loading screens; adds work near borders | Cross-server traffic, handoff bugs | 2 |
| Movable boundaries | Moves work to idle servers | Migration churn, cut pairs | 3 |
| Priority and relevancy | Sends less per pair, drops the least important | Some entities update less often | 4, 5 |
| Battle-specific designs | Changes what a pair costs in a fight | Special cases in game rules | 6 |
| Time dilation | Stretches `B` | Everyone in the fight slows down | 7 |
| Splitting by function | Moves AI, physics or combat to other processes | Consistency between processes | 8, 9, 11, 12 |
| Copies (layers, shards) | Divides `n` per copy | Players cannot see each other | this week |

Notice what is not on the list, "buy a bigger server". You have seen why. It is the one lever whose return shrinks as the problem grows.

## In-class activity (25 minutes)

In groups of three, you are the server team for a new MMO's launch city. The design document says the city is 1 km × 1 km, the AOI radius is 60 m, and the city should hold 800 players at peak with the crafting hall as the one gathering place.

1. Compute `f` for the city. (5 min)
2. Using the model and the lecture's constants, find the largest hot-spot share `h` at which 800 players still fit in the 50 ms budget. Use the interactive's custom mode or the code above. (10 min)
3. The design lead wants a world boss to spawn in the city square once a day. Estimate `h` during that event and say what fails. Choose one escape route from section 4 and state its price in one sentence a producer would understand. (10 min)

Expected output: `f` to three significant figures (0.0113), the critical `h` to two decimals (about 0.12), and a three-sentence recommendation.

## Common misconceptions

- **"This zone holds 1,000 players."** It holds 1,000 players at one density. The same zone in this lecture holds between 153 and 1,258. Always state the density a capacity assumes.
- **"Twice the CPU, twice the players."** Only while per-player work dominates. In a crowd, capacity grows as the square root of CPU, so twice the CPU gives about 1.4 times the players.
- **"Layering just moves the load around."** It removes load. Splitting 1,000 crowded players into three copies cuts total pair work by three, because pairs across copies no longer exist.
- **"Average utilization tells you if the cluster is healthy."** Players feel the busiest server, not the average one. A cluster at 60% average can have one zone at 320% of budget.

## Check yourself

1. A zone uses the lecture's constants and 2 km map but shrinks the AOI radius to 50 m. What is the capacity when everyone spreads out? When everyone stands in one crowd?
2. A zone at `h = 0.5` holds 294 players. The team proposes three layers. How many players can the zone admit in total, assuming each layer keeps the same `h`?
3. EVE time dilation reaches its 10% floor. Using the lecture's constants, with `h = 1`, how many players fit? Explain in one sentence why this is not 10 × 153.
4. A producer says "our cluster averages 45% CPU at peak, so we can double the player count." Name the information you need before you agree, and why.

<details>
<summary>Answers</summary>

1. `f = π × 50² / 2000² = 0.00196`. Spread out, `a = 2×10⁻⁶ × 0.00196 = 3.93×10⁻⁹`, and `n = (−2×10⁻⁵ + √(4×10⁻¹⁰ + 4 × 3.93×10⁻⁹ × 0.05)) / (2 × 3.93×10⁻⁹) ≈ 1,837`. In one crowd, the radius does not matter because everyone is within it, so capacity stays 153.
2. Each layer is its own zone at the same density, so each holds 294, and three layers hold 882. Pairs only count within a layer.
3. The budget becomes 500 ms. `2×10⁻⁶ n² + 2×10⁻⁵ n = 0.5` gives `n ≈ 495`. Because the pair term grows as `n²`, ten times the budget buys `√10 ≈ 3.2` times the players.
4. You need the load of the busiest server at peak, and the density (hot-spot share) on it. If one zone is already at 100% because of a crowd, doubling players at that density needs four times its capacity, not two.

</details>

## Lab / assignment hook

[Lab 01, zone capacity](../labs/lab01.md). You implement this lecture's model, check it against pairs counted on seeded zones, sweep the hot-spot share, and write a one-page capacity plan for a launch city with an event that draws a crowd.

## Sources

- CCP Games, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011). The idea of slowing the game clock under load because most load is tied to the clock. Paraphrased.
- EVE University Wiki, "Time dilation" (current mechanics). The 10% floor, time dilation acting per node, and the note that server load scales as `O(n²)` with players on grid.
- EVE University Wiki, "Tranquility" (current). The cluster serves one persistent world but is split into nodes, each hosting part of New Eden.
- Wikipedia, "Battle of B-R5RB" (formerly "Bloodbath of B-R5RB") (battle of 27 to 28 January 2014). A missed sovereignty payment as the trigger, the unplanned start, a peak of 2,670 players in the system, about 21 hours, time dilation at 10% speed.
- Wowpedia, "Layering" (World of Warcraft Classic, patch 1.13.2, August 2019). Copies of the outdoor world per realm, visibility only within a layer, party moves you to the leader's layer, single layer on all realms from 13 November 2019.
- Wowpedia, "Sharding (term)" and "Cross-realm zones" (retail World of Warcraft; CRZ added in patch 5.0.4, 2012). Invisible shard borders, NPCs that may vanish briefly when players change shard, CRZ as the fix for under-populated zones.
- Second Life Wiki, "Region" (archived December 2024). 256 m × 256 m regions, one simulator process per region, avatar limits of 100 (full region) and 40 (mainland).
- De Vleeschauwer, B., Van Den Bossche, B., Verdickt, T., De Turck, F., Dhoedt, B. & Demeester, P. (2005). Dynamic microcell assignment for massively multiplayer online gaming. *NetGames '05*, ACM. doi:10.1145/1103599.1103611. Hot spots in static cells overload single servers.

## Interactive spec: examples/w01-zone-hotspot.html

**The one insight:** the same number of players can fit comfortably or break the server, depending only on how many of them stand together. Doubling CPU helps the spread-out case much more than the crowded one.

**Layout.** Two linked views side by side on desktop, stacked on mobile (map first).

- **Left, the zone map.** A square representing a 2 km × 2 km zone. Draw `n` dots. `round(h × n)` dots are placed uniformly in a disc of radius `R / 2` at a fixed hot spot (at 60%, 40% of the map, not the centre, so the student can see it is a place). The rest are uniform over the square. Use a seeded PRNG (mulberry32, seed 1) so the picture is stable; when `n` or `h` changes, keep existing dots and add or move only the ones that must change, so the map does not flicker. Draw one faint AOI circle of radius `R` around a spread-out dot and one around a hot-spot dot. Above the map, show `n`, the number in the hot spot, and `f`.
- **Right, the tick bar.** One horizontal stacked bar for tick time in ms: per-player part `c_p × n` and pair part `c_i × n² × (h² + (1 − h²) f)`, in two palette colours. Vertical lines at the budget `B` (default 50 ms, labelled "budget") and at the tick interval (100 ms, labelled "tick"). The axis extends to max(200 ms, 1.1 × tick time), with a note "off scale" if above 2,000 ms. Under the bar, a small line chart of `C(n)` for the current `h` with `n` from 0 to 2,000, the budget line, and a marker at `n_max`.
- **Numbers panel** under both views: `f`, pair fraction, tick ms (1 decimal), per-player ms, pair ms, capacity `n_max` (integer), capacity with 2× CPU, and "utilization = tick / budget" as a percent. All must match the formulas below exactly.

**Controls.**
- Players `n`: slider 50 to 2,000, step 10, default 1,000.
- Hot-spot share `h`: slider 0 to 1, step 0.01, default 0.
- AOI radius `R`: slider 25 to 200 m, step 5, default 100.
- Toggle "2× CPU" (halves `c_p` and `c_i`).
- Toggle "Time dilation 10%" (multiplies `B` by 10 and relabels the budget line).
- Layers `k`: stepper 1 to 4, default 1. With `k > 1`, the map shows `k` small copies tinted differently, each with `n / k` players at the same `h`, and the bar shows one layer's tick; the numbers panel adds "total work across layers = k × tick(n/k)".
- Reset button.

**Formulas.** `f = π R² / 2000²`. `g = h² + (1 − h²) f`. `C = 1000 × (c_p n + c_i n² g)` in ms with `c_p = 20e-6`, `c_i = 2e-6` (halved with 2× CPU). `B = 0.050` s (×10 with dilation). `n_max = (−c_p + √(c_p² + 4 c_i g B)) / (2 c_i g)`.

**Test values** (R = 100, one layer, normal CPU unless stated): `f = 0.00785`. `n = 1000, h = 0`: tick 35.7 ms, capacity 1,258, 2× CPU 1,966. `h = 0.1`: 55.6 ms, 938. `h = 0.25`: 159.7 ms, 531, 2× CPU 777. `h = 0.5`: 531.8 ms, 294. `h = 1`: 2,020.0 ms, 153, 2× CPU 219, with dilation 495. Layers `k = 3`, `n = 1000`, `h = 0.25`: one layer 22.2 ms, total 66.6 ms.

**Accessibility.** All controls keyboard operable with visible focus. Announce the tick ms and capacity in an `aria-live="polite"` region when they change. Respect `prefers-reduced-motion` (no dot animation; jump to new positions). Palette from `templates/interactive-tokens.css`, light and dark.
