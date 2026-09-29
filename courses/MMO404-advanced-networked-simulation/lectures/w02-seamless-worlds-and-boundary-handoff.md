# MMO404 · Week 02 — Seamless worlds and boundary handoff

**Why this matters:** A loading screen at a zone border is honest. It tells the player "you are changing servers". A seamless world removes it, and then the server border is still there, invisible, running through town squares and battlefields. This week you price that border, choose how wide to make it, and design the transfer of authority so that crossing it can never duplicate an item or lose a player's input.

**You will be able to:**
- Compute the ghost count and cross-server cost of a seam from density, border length, area of interest and hysteresis width.
- Use a simulation to find the hysteresis width that minimizes seam cost, and explain what sets it.
- Design a handoff protocol that keeps at most one authoritative owner and applies every input exactly once, and trace it message by message.
- Choose a rule for resolving actions that cross the border, and state the latency it adds.

**Before class:** Reread MMO302 weeks 3 and 4 (area of interest with hysteresis, zone servers and handoff). De Vleeschauwer et al. (NetGames 2005), section 2.1, on cells that forward border events to their neighbours. Skim 3GPP TS 36.331 (LTE radio resource control), section 5.5.4.4, "Event A3", for how mobile networks decide when to hand a phone to the next cell.

**Prerequisites from earlier courses:** [MMO404 week 1](w01-limits-of-the-zone-model.md) (seams as a limit of the zone model, the tick budget). [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (AOI hysteresis). [MMO302 week 4, zone servers and handoff](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md). [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md). [CS202 week 6, reliability over UDP](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w06-reliability-over-udp.md) (sequence numbers and ordering). [CS202 week 9, server reconciliation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md) (numbered inputs applied in order).

**Interactive:** [examples/w02-seam-hysteresis.html](../examples/w02-seam-hysteresis.html). Keep it open during section 2.

---

## 1. What a seamless border has to do

In MMO302 week 4 your zone servers handed a player over at the border, and a loading screen covered the gap. The player could not see across, and nothing could happen across. A **seamless** world keeps the servers but removes both limits. That gives each border three jobs.

- **Visibility.** A player near the border must see what is on the other side. The neighbour's entities must be in that player's snapshots ([CS202 week 7](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md)) even though another server simulates them.
- **Interaction.** A player on server A must be able to attack, heal, trade with or bump into a player on server B, and both servers must agree on the result.
- **Transfer.** When a player walks across, authority over that character must move from A to B without a gap, without a duplicate, and fast enough that the player feels nothing.

Some vocabulary. The **owner** of an entity is the one server **authoritative** for it, the one whose simulation is the truth. A **ghost** (also called a proxy or replica) is a read-only copy of an entity kept by a server that does not own it. The owner sends the ghost updates, and the ghost's server uses them for visibility and for checking interactions. A **seam** is the border between two servers' regions, together with the strip on each side where ghosts are needed. A **handoff** is one transfer of ownership.

Ghosts solve visibility. Section 4 handles interaction. Transfer is where bugs live, and section 3 designs it properly. First, the cost.

## 2. Worked example: how wide should the seam be?

### The hook

Retail World of Warcraft moves players between copies of a crowded zone automatically, and Wowpedia notes that the borders are invisible and that players may see NPCs vanish for a moment when it happens. Its page on cross-realm zones lists a stranger known issue. Ride out of a capital city into a cross-realm zone on a two-seat mount, and your passenger is dropped on the ground. Both are symptoms of the same fact. Crossing an invisible line changed which server was simulating those players, and not every piece of state made the trip intact.

So picture the player who causes the most trouble. They are not the one who rides across the border once. They are the one standing on it, fighting, strafing left and right, crossing it twice a second. If the border is a sharp line, every step is a handoff. How often does that happen on a busy border, what does each handoff cost, and what happens if you blur the line?

### The model

Put two servers side by side. Server A owns the west (`x < 0`) and server B owns the east (`x > 0`). The border runs for a length `L`. Players stand at density `ρ` per square metre, and each has an area of interest of radius `R`.

**Hysteresis.** Instead of handing a player over the instant they cross `x = 0`, use a band of width `w` around the border. A player owned by A moves to B only when `x > w/2`. A player owned by B moves back to A only when `x < −w/2`. Inside the band, the player stays with whichever server owned them last. This is the hysteresis you used for AOI subscriptions in MMO302 week 3, applied to authority. A player dithering by a few metres inside the band never triggers a handoff.

**Ghosts.** Server B must hold a ghost of every A-owned entity that some B-owned player could see. B-owned players can stand as far west as `−w/2`, and A-owned entities can stand as far east as `+w/2`. So B needs ghosts of A-owned entities in a strip of width `R + w`. The same holds the other way. The total ghost count is

```
G(w) = 2 × ρ × L × (R + w)
```

**Handoffs.** Call the handoff rate `H(w)`, in handoffs per second across the whole seam. It falls as `w` grows, because dithering stops causing handoffs. It does not fall to zero, because players who really travel across still need one handoff each. `H(w)` depends on how players move, so we measure it with a simulation rather than a formula.

**Cost.** Each handoff costs `E_h` of CPU across both servers: serializing the character, sending it, installing it, checking its state, updating the routing. Each ghost costs `c_g` per tick on the server holding it: applying the owner's update and keeping the ghost in the AOI index. At tick rate `T`, the seam's CPU cost per second is

```
S(w) = H(w) × E_h + G(w) × T × c_g
```

We use `E_h = 1 ms`, `c_g = 3 µs` and `T = 10` ticks per second. As in week 1, the constants are teaching values. The shape of the answer does not depend on them.

The trade-off is visible in the formula. Widening `w` lowers the first term and raises the second in a straight line.

### Numbers you can check

Take a 500 m stretch of border in a busy area at `ρ = 0.002` players per m² (2,000 per km²), with `R = 100 m`. The players near the seam are of two kinds. A quarter are **travellers**, who walk across at 5 m/s and rarely turn back. Three quarters are **dwellers**, who mill around a fixed spot (a fight, a vendor, a resource node) with a spread of about 4 m. The simulation below places 400 of them in a band 200 m deep on each side, runs 300 seconds at 10 ticks per second, and counts handoffs.

| Band width `w` | Handoffs per second `H` | Ghosts `G` | Handoff CPU | Ghost CPU | Seam cost `S` |
|---|---|---|---|---|---|
| 0 m | 9.25 | 200 | 9.25 ms/s | 6.00 ms/s | 15.25 ms/s |
| 5 m | 2.69 | 210 | 2.69 | 6.30 | 8.99 |
| 10 m | 1.62 | 220 | 1.62 | 6.60 | 8.22 |
| 15 m | 1.23 | 230 | 1.23 | 6.90 | 8.13 |
| 20 m | 1.11 | 240 | 1.11 | 7.20 | 8.31 |
| 40 m | 0.94 | 280 | 0.94 | 8.40 | 9.34 |

Check one row by hand. At `w = 10`, `G = 2 × 0.002 × 500 × (100 + 10) = 220` ghosts. Ghost CPU is `220 × 10 × 0.003 ms = 6.6 ms` per second. Handoff CPU is `1.62 × 1 ms = 1.62 ms` per second. The sum is 8.22 ms per second.

Three things stand out.

- **The first few metres of band do almost all the work.** Going from 0 to 5 m removes 71% of handoffs. Going from 5 to 40 m removes only 65% of what is left, while adding 70 ghosts.
- **The cost curve is U-shaped with a flat bottom.** The minimum is near 15 m, and anything from 10 to 20 m is within 3% of it. A sharp border (`w = 0`) costs almost twice as much as any sensible band.
- **Handoffs never fall below the travellers.** Around 1 per second remain at large `w`. Those are real crossings, and no band removes them.

The CPU numbers look small. At `w = 0` the seam costs 1.5 ms per 100 ms tick, 3% of a 50 ms budget. The bigger cost of a handoff is risk. Each one is a moment where a bug can duplicate or lose a character. At 9.25 handoffs per second, one 500 m seam performs 33,300 handoffs an hour. If your handoff code has a one-in-a-million bug that duplicates an item, that seam produces a duplicate about every 30 hours. At `w = 15`, it is 4,430 handoffs an hour and a duplicate every 226 hours. Fewer handoffs means fewer chances for your worst bug.

Here is the simulation. It is part B of Lab 02, where you also write the ownership rule yourself.

```python
import math, random

def handoffs_per_s(w, travellers=100, dwellers=300, band=200.0, dt=0.1, seconds=300, seed=4):
    rng = random.Random(seed)
    tx = [rng.uniform(-band, band) for _ in range(travellers)]
    tv = [rng.choice((-5.0, 5.0)) for _ in range(travellers)]
    anchors = [rng.uniform(-band, band) for _ in range(dwellers)]
    dx = anchors[:]
    on_b = [x > 0 for x in tx + dx]
    count = 0
    for _ in range(int(seconds / dt)):
        for i in range(travellers):                  # walk across, rarely turn back
            if rng.random() < 0.05 * dt:
                tv[i] = -tv[i]
            tx[i] += tv[i] * dt
            if abs(tx[i]) > band:
                tv[i] = -tv[i]
        for i in range(dwellers):                    # mill around a spot, 4 m spread
            dx[i] += 0.5 * (anchors[i] - dx[i]) * dt + 4.0 * math.sqrt(dt) * rng.gauss(0, 1)
        for i, x in enumerate(tx + dx):              # hysteresis band of width w
            if not on_b[i] and x > w / 2:
                on_b[i], count = True, count + 1
            elif on_b[i] and x < -w / 2:
                on_b[i], count = False, count + 1
    return count / seconds

rho, L, R = 0.002, 500, 100
for w in (0, 5, 10, 15, 20, 40):
    h = handoffs_per_s(w)
    ghosts = 2 * rho * L * (R + w)
    cost = h * 1.0 + ghosts * 10 * 0.003
    print(f"w={w:>2} m  handoffs/s={h:5.2f}  ghosts={ghosts:4.0f}  seam cost={cost:5.2f} ms/s")
```

It takes about two seconds and prints the six rows of the table, from `w= 0 m  handoffs/s= 9.25  ghosts= 200  seam cost=15.25 ms/s` to `w=40 m  handoffs/s= 0.94  ghosts= 280  seam cost= 9.34 ms/s`.

The table is one run, with seed 4. Change the seed and the numbers move, most of all at `w = 0`. Across seeds 1 to 8, `H(0)` ranges from 6.2 to 10.9 handoffs per second, because it depends on how many dwellers happen to have their spot within a few metres of the line. At `w = 10` the range is much tighter, about 1.5 to 1.8. So when you compare band widths, average several seeds. The interactive does that, with 8 seeds of 120 s each.

Notice what the dwellers do at `w = 0`. Their 4 m spread moves them by about a metre per tick. A dweller whose spot is within a few metres of the line crosses it on a large share of ticks, so the handoff rate at `w = 0` depends on the tick rate itself. With no band, a player standing on the border can be handed off every tick.

### A planning estimate for travellers

For travellers you do not need a simulation. You met the formula in [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md). If players at density `ρ_t` walk straight lines at speed `v` in random directions, the number crossing a border of length `L` per second, both directions together, is

```
H_travel = 2 × ρ_t × v × L / π
```

At `ρ_t = 0.0005` per m², `v = 5 m/s` and `L = 500 m`, that is `2 × 0.0005 × 5 × 500 / π ≈ 0.80` handoffs per second. This is the floor that no band width removes. Use it to size handoff capacity for roads and borders that people travel through, then add the dwellers for the places where people stop.

### Move it yourself

Open `examples/w02-seam-hysteresis.html`. The left view is the seam from above: the border line, the hysteresis band shaded, and dots coloured by which server owns them. A dot flashes when it is handed off, and ghost strips are outlined on both sides. The right view plots seam cost against `w` from 0 to 60 m, with the handoff part falling, the ghost part rising, their sum, and a marker at the current `w`. Start at `w = 0` and watch the dots near the line flicker between colours. Drag `w` to 5 m. The flicker stops almost everywhere, and on the right the cost drops by 40%. Keep dragging to 60 m. The map barely changes, but the ghost strips widen and the cost climbs. Then raise the dwellers' spread from 4 m to 12 m and watch the curve's minimum move right. The best band width follows how far players wander, not how many there are.

### Same idea elsewhere

**Mobile phone networks (LTE, 3GPP TS 36.331).** A phone moving between cell towers has the same problem. Radio signal strength fluctuates, and a phone at the edge of two cells could bounce between them every second. LTE's "Event A3" triggers a handoff only when the neighbour's signal beats the current cell by an offset plus a **hysteresis** margin, and only if that stays true for a configured **time-to-trigger**. Our `w` is the margin in metres instead of decibels. A time-to-trigger would be a second knob, "stay past `w/2` for 3 ticks", which you can add in the lab.

**Second Life (Linden Lab, current).** The world is a grid of 256 m regions, each run by its own simulator process, with no loading screen between them. The Second Life wiki's page on region crossings describes all three jobs. For visibility, the viewer talks to several region simulators at once, so it can draw the neighbours' contents. For transfer, the losing simulator sends the avatar to the gaining one and then hands over control of the avatar's inputs. And the crossing triggers only when the avatar's centre is one metre past the boundary, a rule the wiki says exists to stop avatars on the edge from toggling back and forth. In our model that is a band of `w = 2` m, at the narrow end of the range this lecture recommends. MMO302 week 4 used the same page for the other half of the story, how brittle those crossings are. De Vleeschauwer and colleagues (2005) describe the same architecture from the research side. Cells forward events near the border to their neighbours and move player data when a player moves from one cell to another. Because each region is small, Second Life has many seams per square kilometre. That makes `L` large compared with the area, and the ghost term matters more than in a world with a few large regions.

**Star Citizen (Cloud Imperium Games, Alpha 4.0 preview, December 2024).** Alpha 4.0 shipped the first live version of what CIG calls server meshing, with a target of 500 players per shard. The Star Citizen wiki describes the static version as servers pre-assigned to areas such as a planet or a city, with the goal that players can interact, even shoot each other, across a server border without noticing it. That is the three jobs of section 1. The wiki also describes the planned dynamic version, where the areas themselves are resized as players move. Next week's lecture covers moving boundaries. Week 9 returns to meshing as a whole.

**World of Warcraft sharding (retail).** Sharding copies a crowded area rather than splitting it, so a shard change is a jump between copies, not a walk across a line. Our reading of the vanishing NPCs Wowpedia describes is that the new copy's view of the world has not yet arrived when the player lands in it. It is the visibility job, done late. The dropped passenger is the transfer job, done incompletely, because a two-seat mount is state that belongs to two players at once.

Four systems, one model. Before you tune any border, ask what the dithering scale is, what a handoff costs in CPU and in risk, and what a ghost costs per tick.

### Design judgment

- **Always use a band.** Even 2 to 5 m removes most handoffs for almost no ghost cost. A sharp border is never the right default.
- **Set `w` from player movement, not player count.** Both `H` and `G` grow in proportion to `ρ`, so density scales the curve without moving its minimum. What moves the minimum is how far dwellers wander. Measure it in playtests, around the places where players stop.
- **Do not put seams where players stop.** The cheapest seam is one nobody stands on. Draw borders through roads, rivers and open fields, not through the bank, the quest hub or the world boss's spawn. Week 3 shows how to choose borders from load data automatically, and why you sometimes cannot avoid a crowd.
- **Treat handoff count as a risk budget.** Log every handoff. Test the transfer under delay, loss and server crashes (section 3, Lab 02). A handoff bug is an item-duplication bug waiting for a busy evening.

## 3. The handoff protocol: exactly one owner

A handoff moves authority over one entity from A to B. Two things must never happen.

- **Two owners at once.** If A and B both think they own a player, both simulate them. The player can loot the same chest on both servers, or trade an item on A while it drops on B. This is how item duplication bugs happen.
- **A lost or doubled input.** The client sends numbered inputs (CS202 week 9). Every input must be applied once, by whichever server owns the player at that moment, in sequence order. An input applied twice moves the player twice. An input dropped makes the client's prediction diverge and causes a visible snap.

A brief moment with **no** owner is acceptable, as long as inputs are held, not dropped, during it. Here is a protocol that keeps both rules. Each server holds the player in one of four roles: `authoritative`, `transferring`, `ghost` or `absent`. A gateway routes the client's inputs to the server it believes is the owner.

1. At the end of a tick, A (authoritative) sees the player past `+w/2`. A sends B a `transfer` message with the player's full state and the next input sequence number it expects. A becomes `transferring`. From now on A does not simulate the player, and any inputs that still arrive at A are **buffered**, not applied.
2. B receives `transfer`. B installs the state, becomes `authoritative`, tells the gateway to route the player's inputs to B, and replies `ack`.
3. A receives `ack`. A forwards every buffered input to B, in sequence order, and becomes `ghost`.
4. B applies inputs strictly in sequence order. An input that arrives early (sequence 105 from the client while 103 and 104 are still in A's forwarded batch) waits in a pending list until the gap is filled.

At no moment are both servers authoritative. A stops being authoritative in step 1, before B starts in step 2. No input is lost. Inputs that reached A after step 1 are forwarded in step 3, and step 4's ordering puts them back in place.

How long does the gap last? Between servers in one data centre, a message takes well under a millisecond. The whole handoff is one message each way plus processing, a few milliseconds, which is much shorter than a 100 ms tick. In practice the player's inputs for the current tick simply arrive at B instead of A, and nobody notices. The lab makes the link deliberately slow (1 to 3 ticks) so that the buffering and reordering paths actually run and your tests exercise them.

### When a server fails mid-handoff

The protocol above assumes messages arrive. Suppose B crashes after A sent `transfer` but before B replied. A is `transferring` and holds buffered inputs, while B may or may not have become authoritative before it died. If A simply times out and takes the player back, and B did in fact save its new authority somewhere, you now have two owners after B restarts.

Real systems solve this with a third party that decides ownership, often called a directory or a lease service. Every ownership change gets a number, the **epoch**, that only goes up. A server may act as owner only while it holds the current epoch's lease, and every write it makes to the database carries its epoch, so the database rejects writes from an old owner. This is the same fencing idea you will meet in week 10 on consistency models. For this week, the rule to remember is that the handoff protocol needs someone outside A and B to break ties when one of them goes silent.

### What travels in a transfer

The `transfer` message carries everything the new owner needs to be the truth: position and velocity, health and resources, active effects with their remaining time, cooldowns, quest state, the inventory or a reference to it, and the next input sequence number. Anything that belongs to two entities at once, a passenger on a mount, a pending trade, a duel, needs an explicit rule for which server owns it and how both sides find out. The WoW passenger bug is the classic result of forgetting one.

## 4. Interaction across the seam

Player Ana is owned by A, and Ben by B. Both stand within 10 m of the border. Ana swings a sword at Ben. Who decides whether it hits, and who changes Ben's health?

The rule that keeps authority simple is that **only an entity's owner changes that entity's state**. So Ben's health can only change on B. That leaves two designs.

- **The attacker's owner checks, the target's owner applies.** A checks the hit against its ghost of Ben (range, line of sight, Ana's cooldowns), then sends B a `damage` event. B applies it at its next tick, after its own sanity check. A owns everything about Ana's action, and B owns everything about Ben's health.
- **The target's owner checks and applies.** A forwards Ana's attack request to B. B checks it against its ghost of Ana and applies it. This is simpler when the check depends mostly on the target's state (dodge, block, position).

Either way, the action crosses a server boundary once, and that has a latency cost. If A and B tick at 10 Hz with unaligned clocks, the event reaches B at a random point within B's tick. It waits on average half a tick, 50 ms, and at worst a full tick, 100 ms, before B applies it. Compared with the same attack inside one server, a cross-seam hit lands up to one tick later. At 10 Hz that is noticeable in fast combat and invisible in tab-target combat. Aligning the tick clocks of neighbouring servers, so that all servers tick together and exchange events before the next tick, removes most of it.

Area effects that straddle the border split cleanly under this rule. A fireball centred on A's side damages A-owned entities on A and sends `damage` events for B-owned entities to B. Each server applies damage only to its own entities.

Transactions are the hard case. A trade between Ana and Ben must remove an item from one inventory and add it to the other, on two servers, atomically. Doing that correctly is a distributed transaction, the subject of [MMO302 week 8 on item ownership](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md). Many seamless games route trades through a separate service rather than between the two zone servers, for exactly this reason.

## In-class activity (25 minutes)

In pairs. You are placing the seams for a seamless region map made of four square server areas, each 1 km on a side, meeting at a central crossroads. A market town sits 150 m east of the crossroads, and a world-boss arena sits 80 m north of it.

1. Sketch the default layout, with two straight seams crossing at the crossroads. For each of the four seam segments of 1 km, estimate `ρ` near it (use 0.002 per m² near the town and arena, 0.0003 elsewhere) and the ghost count at `R = 100 m`, `w = 10 m`. (10 min)
2. Move the seams so that no seam passes within 150 m of the town or the arena. Recompute the ghost counts. (10 min)
3. Write two sentences on what the new layout costs. Think about the size of each server's area and which server now owns the crowded places. (5 min)

Expected output: two sketches, two ghost totals, and the two sentences. You will reuse this layout in week 3.

## Common misconceptions

- **"A wider band is always safer."** It removes handoffs, but each metre adds ghosts on both sides forever. Past the dithering scale you pay ghost cost for nothing.
- **"Handoffs are cheap because the servers are in the same data centre."** The network hop is cheap. The risk is not. Every handoff is a chance for a duplication or loss bug, and busy seams do tens of thousands an hour.
- **"During a handoff, the old server can keep simulating until the new one is ready."** Then both servers simulate the player at once, and anything the player does in that window can happen twice. The old owner must stop before the new one starts, and buffer rather than apply.
- **"A seamless world has no zones."** It still has servers with borders. It just hides them, which moves the border's cost from the player's loading screen to the engineers' protocol.

## Check yourself

1. A seam is 800 m long at `ρ = 0.001` per m², with `R = 80 m`. How many ghosts does it hold at `w = 0` and at `w = 20 m`? How much ghost CPU per second at 10 Hz and 3 µs per ghost?
2. Using the table in section 2, a designer halves the handoff CPU `E_h` to 0.5 ms with a faster serializer. Recompute `S(w)` for `w = 0, 10, 20` and say whether the best `w` moves left or right.
3. In the handoff protocol, input 212 reaches A after A has sent `transfer` but before A receives `ack`. The client's input 213 reaches B directly. Trace what each server does with each input until both are applied.
4. Ana (on A) hits Ben (on B). Both servers tick at 20 Hz, clocks unaligned. What is the average and worst-case extra delay before Ben's health changes, compared with a hit inside one server?

<details>
<summary>Answers</summary>

1. `G(0) = 2 × 0.001 × 800 × 80 = 128`. `G(20) = 2 × 0.001 × 800 × 100 = 160`. Ghost CPU is `128 × 10 × 0.003 = 3.84 ms/s` and `160 × 10 × 0.003 = 4.8 ms/s`.
2. `S(0) = 9.25 × 0.5 + 6.0 = 10.63`, `S(10) = 1.62 × 0.5 + 6.6 = 7.41`, `S(20) = 1.11 × 0.5 + 7.2 = 7.76` ms/s. The best `w` moves left, from about 15 m to about 10 m (`S(15) = 7.52`, `S(5) = 7.65`). Cheaper handoffs make the handoff term less important, so the ghost term's pull toward small `w` wins sooner.
3. A is `transferring`, so it buffers 212. B is `authoritative` and has `next_seq` 212 from the transfer. When 213 arrives, B puts it in `pending` and waits. When A receives `ack`, it forwards 212 to B and becomes a ghost. B applies 212, then 213 from `pending`, in order.
4. At 20 Hz a tick lasts 50 ms. The event waits on average half a tick, 25 ms, and at worst a full tick, 50 ms, plus a sub-millisecond network hop.

</details>

## Lab / assignment hook

[Lab 02, seams and handoff](../labs/lab02.md). Part A: you implement the four-role handoff protocol from section 3 and pass tests that run a dithering player across the border with delayed messages, checking for two owners, lost inputs and doubled inputs. Part B: you implement the ownership rule and the seam cost model, reproduce the table in section 2, and find the best band width for a second population with a wider spread.

## Sources

- Wowpedia, "Sharding (term)" (retail World of Warcraft). Invisible shard borders; players may notice NPCs momentarily disappear when moved between shards.
- Wowpedia, "Cross-realm zones" (retail World of Warcraft, CRZ added in patch 5.0.4, 2012). Known issue of a passenger being dismounted when leaving a major city into a cross-realm zone on a two-seat mount.
- Second Life Wiki, "Region" (archived December 2024). 256 m × 256 m regions, each hosted by a simulator process.
- Second Life Wiki, "Region crossing" (revision of 11 February 2024, archived November 2024). Viewers talk to several region simulators at once; the losing simulator sends the avatar to the gaining one and hands over control; a crossing triggers one metre past the boundary to prevent toggling at the edge; double crossings at region corners are not interlocked.
- De Vleeschauwer, B. et al. (2005). Dynamic microcell assignment for massively multiplayer online gaming. *NetGames '05*, ACM. doi:10.1145/1103599.1103611. The introduction names Second Life's one-cell-per-server approach; section 2.1 describes cells forwarding events near the border to neighbours and moving player data between cells. Open copy at biblio.ugent.be.
- Star Citizen Wiki, "Server meshing" (Alpha 4.0 preview, December 2024). Static meshing with servers pre-assigned to areas, 500 players per shard at launch of the feature, the goal of cross-server interaction, and the planned dynamic version.
- 3GPP TS 36.331, *E-UTRA Radio Resource Control (RRC) protocol specification*, section 5.5.4.4, Event A3 (neighbour becomes offset better than serving), with hysteresis and time-to-trigger parameters.

## Interactive spec: examples/w02-seam-hysteresis.html

**The one insight:** a narrow hysteresis band removes most handoffs almost for free, and past the scale at which players wander, a wider band only adds ghosts. The best width is set by player movement, not player count.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (map first).

- **Left, the seam map.** A rectangle 400 m wide (x from −200 to 200) and 500 m tall, the border as a vertical line at x = 0. Shade the hysteresis band from `−w/2` to `+w/2`. Outline the two ghost strips, from `−w/2 − R` to `+w/2` (ghosts held by B) and from `−w/2` to `+w/2 + R` (ghosts held by A), in the two server colours at low opacity. Draw 400 dots (100 travellers, 300 dwellers) with random y positions, coloured by owner. Run the simulation live at 10 ticks per second of sim time (speed control 1×, 5×, 20×). A dot that changes owner draws a short ring (skip the ring under reduced motion). Show counters: handoffs in the last 10 s of sim time, handoffs per second (running mean), ghost count `G(w)`.
- **Right, the cost chart.** x axis `w` from 0 to 60 m. Three lines: handoff CPU `H(w) × E_h`, ghost CPU `G(w) × T × c_g`, and their sum `S(w)`. Mark the minimum of `S` with a dot and label its `w`. A vertical marker at the current `w`. The `H(w)` values come from a precomputed sweep: on load and whenever the dweller spread changes, run the same simulation headless for `w` in {0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60}, averaging 8 seeds (1 to 8) of 120 s of sim time each (fast enough in JS; show a small "computing" note), and interpolate linearly between points. A single seed is not enough: `H(0)` varies from about 6 to 11 per second across seeds. The live map runs one seed.
- **Numbers panel** under both views: current `w`, `H`, `G`, handoff CPU, ghost CPU, `S`, and "handoffs per hour" (`H × 3600`).

**Simulation (must match the lecture's model).** Travellers: x uniform in [−200, 200], velocity ±5 m/s, reverse with probability `0.05 × dt` per tick, reverse at the band edge. Dwellers: anchor `a` uniform in [−200, 200], start at `a`, each tick `x += 0.5 × (a − x) × dt + σ × √dt × N(0, 1)` with `σ = 4` (the "spread" control sets `σ`). `dt = 0.1`. Ownership: to B when `x > w/2`, to A when `x < −w/2`. Use a seeded PRNG (mulberry32) and a Box-Muller normal. Numbers will differ slightly from Python's because the PRNG differs and the sweep averages 8 seeds while the lecture table is one Python seed; that is fine, but the test values below must be within 15%.

**Controls.**
- Band width `w`: slider 0 to 60 m, step 1, default 0.
- Dweller spread `σ`: slider 1 to 12, step 1, default 4 (recomputes the sweep).
- AOI radius `R`: slider 50 to 150 m, step 10, default 100.
- Handoff cost `E_h`: slider 0.25 to 4 ms, step 0.25, default 1.
- Sim speed: 1×, 5×, 20×. Pause/play. Reset.

**Formulas.** `ρ = 400 / (400 × 500) = 0.002`. `G(w) = 2 ρ L (R + w)` with `L = 500`. `S(w) = H(w) × E_h + G(w) × 10 × 0.003` in ms per second.

**Test values** (defaults): `G(0) = 200`, `G(10) = 220`, `G(40) = 280`. From the Python reference (seed 4, 300 s, the lecture table): `H(0) = 9.25`, `H(5) = 2.69`, `H(10) = 1.62`, `H(15) = 1.23`, `H(20) = 1.11`, `H(40) = 0.94` per second; `S(0) = 15.25`, `S(10) = 8.22`, `S(15) = 8.13`, `S(40) = 9.34` ms/s; minimum near `w = 15`. With `σ = 12` the minimum must move clearly to the right. The built page shows `H(0) = 9.07`, `H(10) = 1.77`, `H(40) = 0.87`, `S(15) = 8.21` ms/s, minimum 15 m, and minimum 40 m at `σ = 12`.

**Accessibility.** Keyboard-operable controls with visible focus. `aria-live="polite"` summary of `w`, `S` and the minimum. Under `prefers-reduced-motion`, start paused and advance the sim only on a "step 1 s" button. Palette from `templates/interactive-tokens.css`, light and dark; the two server colours must differ in lightness as well as hue.
