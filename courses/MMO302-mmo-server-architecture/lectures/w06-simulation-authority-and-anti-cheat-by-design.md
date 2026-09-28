# MMO302 · Week 06 — Simulation authority and anti-cheat by design

**Why this matters:** Every message a client sends is a claim that someone can forge. Anti-cheat software catches some forgers after the fact. Server design decides what a forger could gain in the first place, and it is far cheaper to get right before launch than to patch after the first duplication exploit empties your economy. This week you learn to price each piece of trust your server extends, and to shrink the exploit to a number you chose.

**You will be able to:**
- Classify client messages as intents or claims, and state the largest advantage a forged message of each kind can buy.
- Compute the sustained speed gain and the largest single "blink" that a cheater gets past a per-packet check, a sliding-window check and a token-bucket check, for a given lag tolerance.
- Compute the honest-player correction rate that a lag tolerance produces, and choose a tolerance with both numbers in view.
- Design the authority layout for an MMO's main systems (movement, combat, loot, inventory, visibility) and defend each choice with its CPU and latency cost.

**Before class:** Glenn Fiedler, "What Every Programmer Needs To Know About Game Networking" (Gaffer on Games, 24 February 2010), the sections on client/server and client-side prediction. Paul Chamberlain, "Demolishing Wallhacks with VALORANT's Fog of War" (Riot Games, 14 April 2020). Reread CS202's material on server authority.

**Prerequisites from earlier courses:** [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md), and CS202 [week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 9, reconciliation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md); this lecture assumes you know why the client predicts its own movement. [CS202 week 2, latency, jitter and loss](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md) (where the delay spikes in this lecture come from). [DB201 week 6, race conditions and the duplication bug](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md). From this course, [week 4, zone servers and handoff](w04-zone-servers-and-handoff.md) (the single-owner rule) and [week 5, tick rate](w05-tick-rate-for-mmos-vs-shooters.md) (the CPU budget every check spends).

**Interactive:** [examples/w06-authority-dial.html](../examples/w06-authority-dial.html). Keep it open during section 2.

---

## 1. Who decides

A piece of game state has an **authority**: the one process whose version is the truth. In week 4 you met this idea as ownership between servers. This week the question is between the server and the client.

When the client is the authority over something, the server accepts whatever the client reports. When the server is the authority, the client can only ask, and the server decides. CS202 argued for the server as the authority in general. An MMO cannot apply that rule blindly, because full server authority over everything costs CPU on every tick (week 5) and adds a round trip to everything the player does. So you choose per system.

The most useful distinction is between two kinds of message.

- An **intent** asks the server to do something: "cast Fireball on target 812", "walk towards this tile", "buy item 5 from this vendor". The server checks that the action is legal and then computes the result itself. A forged intent can at most do what a perfect legal player could do. That is a botting problem (MMO309), not a hacking problem.
- A **claim** reports a result: "I hit target 812 for 450", "I am now at (1204.5, 88.1)", "my inventory contains item 5". If the server believes it, the client decides the outcome. A forged claim buys whatever the server fails to reject.

The **trust boundary** is the set of claims your server accepts. Anti-cheat by design means keeping that set small, and putting a number on the advantage each remaining claim can buy.

| System | Common authority in MMOs | Message the client sends | What a forger can buy |
|---|---|---|---|
| Combat damage | Server | Intent (use ability X on Y) | Nothing beyond perfect play |
| Loot and rewards | Server | Intent (loot corpse Z) | Nothing beyond perfect play |
| Inventory and trade | Server plus database | Intent (move item, offer trade) | Nothing, if the database transaction is right (week 8) |
| Cooldowns | Server, mirrored on client | Intent | Nothing; the client's copy is cosmetic |
| Movement | Often shared: client moves, server checks | Claim (position) plus checks | Whatever the check lets through |
| Camera, UI, animation | Client | None | Nothing that affects others |
| What the client knows | Server decides what to send | None | Anything the server sends and should not have |

Two rows stand out. Movement is the claim most MMOs keep, because walking must feel instant. And the last row is a different kind of trust. The client does not claim anything there. The server leaks, by sending information the player's screen should not show. Section 3 deals with it.

## 2. Worked example: pricing a movement check

### The hook

The first Diablo (1996) stored nothing about your character on Blizzard's Battle.net servers. Your hero lived on your own hard drive, and the servers only matched players into games. Cheaters edited their characters freely, and cheating became common. For Diablo II (2000), Blizzard added "closed" realms, where characters were stored on Blizzard's servers as a measure against cheating. Open realms, where characters still came from the player's disk, stayed open to abuse. The closed-realm fix was architectural. Blizzard moved one claim ("here is my character") across the trust boundary, and character editing stopped working there.

Most MMOs cannot make the same move with movement. If every step waited a round trip for the server's permission, walking would feel like wading. So the client moves the player at once and reports positions, and the server checks them. The question is how to write that check so a cheater gains as little as possible and an honest player on a bad connection is not punished.

### The model

A player runs at most `v` metres per second. The client sends a position every `Δ` seconds. The network sometimes delays packets and then delivers several at once, which is jitter from CS202 week 2. The server allows a **lag tolerance** `s` seconds so honest bursts pass. Three checks are common.

```
per-packet check    accept a move of d metres if  d ≤ v × (gap since last packet + s)
sliding window      accept if total distance in the last W seconds ≤ v × (W + s)
token bucket        credit += v × (time since last packet), capped at C = v × (Δ + s)
                    accept a move of d if d ≤ credit, then credit −= d
```

For each check, compute two numbers a cheater cares about. The **sustained speed factor** is how much faster than `v` a cheater can move forever without a single rejection. The **blink** is the longest single jump accepted after standing still.

```
                    sustained factor        blink
per-packet          (Δ + s) / Δ             v × (Δ + s)
sliding window      (W + s) / W             v × (W + s)
token bucket        1                       v × (Δ + s)
```

The honest player cares about one number. Suppose the connection stalls for `J` seconds and then delivers the held packets together. All three checks accept the burst when `J ≤ s`. The window and bucket checks reject part of it when `J > s`. The per-packet check behaves differently, because it judges each packet alone. The first packet of the burst carries the whole stall in its gap, and each later packet arrives with a gap near zero, so it passes only if its own move `v × Δ` fits in `v × s`. With `s ≥ Δ` the per-packet check accepts every honest burst, however long the stall. With `s < Δ` it rejects the second and later packets of every burst, however short. The same blindness to history that forgives bursts is what makes it so generous to cheaters.

### Numbers you can check

Use `v = 7` m/s, `Δ = 0.1` s (10 position updates a second), `W = 5` s and a tolerance of `s = 0.25` s.

| Check | Sustained factor | Blink after standing still |
|---|---|---|
| Per-packet | `(0.1 + 0.25) / 0.1 = 3.5×` | `7 × 0.35 = 2.45` m |
| Sliding window, `W = 5` | `5.25 / 5 = 1.05×` | `7 × 5.25 = 36.75` m |
| Token bucket | `1.0×` | `7 × 0.35 = 2.45` m |

The per-packet check lets a cheater run at three and a half times legal speed forever. The sliding window holds sustained speed to 5% over, but a player who stands still for five seconds can then teleport almost 37 metres in one packet. The token bucket gives neither. The long-run speed is exactly `v`, and the largest jump is one packet's worth of movement plus the tolerance.

I checked these against a simulation. A cheater sending on schedule every 0.1 s passed the per-packet check at 3.5× with zero rejections for a minute, and the bucket at no factor above 1.0. After 10 s of standing still, the per-packet and bucket checks accepted a single 2.45 m move and the window check a 36.75 m one.

Now price the tolerance. Suppose an honest player's connection stalls about once a minute, each stall lasting between 0.2 and 0.8 s, spread evenly. Under the window or bucket check, a stall causes a correction (the server rejects part of the burst and snaps the player back) when it is longer than `s`. The per-packet column needs no stall count, because at these tolerances `s ≥ Δ` and it corrects nothing.

| Tolerance `s` | Corrected stalls per hour | Bucket blink | Per-packet sustained factor |
|---|---|---|---|
| 0.25 s | `60 × 0.55 / 0.6 = 55` | 2.45 m | 3.5× |
| 0.5 s | 30 | 4.2 m | 6× |
| 0.8 s | 0 | 6.3 m | 9× |

The simulation of an hour of play with the bucket agreed: 58, 30 and 0 corrected stalls. The token bucket turns the tolerance into a one-off blink of a few metres. The per-packet check turns the same tolerance into a permanent speed hack.

**With the right check, lag tolerance buys a small blink, not a speed multiplier.** That is the whole design choice in one sentence.

Open the interactive and set the check to "per-packet". Slide the cheat factor up to 3.5 and the cheater's line pulls away from the honest line with no red marks. Switch to "token bucket" and the same cheater collects red rejections from the first second, while the honest line with stalls stays clean up to the tolerance you set.

### What server authority would cost instead

The alternative is to take the claim away. The client sends inputs ("moving north-east, running") and the server moves the player, with the client predicting locally as in CS202 weeks 8 and 9. The cheater's gain drops to zero. Price it with invented but typical costs for a zone of 2,000 players with 10 position updates a second (20,000 per second):

| Design | Work per update | CPU per second | Share of one core |
|---|---|---|---|
| Token bucket plus a wall check (ray cast from old to new position) | 0.2 + 3 µs | 64 ms | 6.4% |
| Server-authoritative movement with collision | 8 µs | 160 ms | 16% |

The bucket and the ray cast together cost 40% of what full authority costs. The ray cast is not optional. A speed check alone lets a player walk through a wall at legal speed. Server authority also adds a correction path. When the server's result differs from the client's prediction, the client must rewind and replay. That code is harder to write and test than a bucket.

### Same idea elsewhere

**Diablo and Diablo II (Blizzard, 1996 and 2000).** The hook, rewritten in our form: a claim ("my character") moved from the client to the server. The sustained advantage of an edited character went from unbounded to zero on closed realms, and the open realms remained as a live control group.

**EVE Online (CCP, current mechanics).** EVE takes the movement claim away entirely. Players steer by commands such as "warp to" a point at least 150 km away, and the EVE University wiki notes that the warp exit point is fixed when the command is given. The server's physics engine, which CCP's 2011 time dilation blog calls Destiny, computes the motion once per second. A speed hack in EVE has nothing to edit, because the client never claims a position. The price is the one week 5 showed: a one-second tick, with the client showing the command at once and the server's result landing on the next tick.

**Old School RuneScape (Jagex, current).** OSRS movement is on a tile grid. Walking moves one square per game tick and running two, and ticks are 0.6 s. In our terms, OSRS is a token bucket whose capacity is exactly one tick: at most two squares, and then the next tick. The coarse grid makes the check trivial and the blink zero.

**Valorant (Riot Games, 2020).** Not movement, but the same design move applied to information. Riot's fog-of-war system withholds enemy positions from a client until the client needs to draw them. It decides using a precomputed table of which map cells can see which, and it expands each enemy's box by its velocity times a look-ahead longer than the expected ping, so enemies do not pop in late. Riot reported that its prototype took 50% of server frame time and the shipped version less than 2%. That look-ahead is a tolerance `s` in our model, and its price is a small blink of information: an enemy may be sent slightly before they can truly be seen.

Four games, one move. Find the claim, shrink it to an intent where you can afford to, and where you cannot, bound what the claim can buy.

### Design judgment

- **List your claims.** Write down every message type and mark it intent or claim. Most MMO messages can be intents at no cost. Each claim that remains needs a written bound.
- **Choose the check shape before the tolerance.** A per-packet check with a small tolerance is still a speed hack. A token bucket with a generous tolerance is a small blink. Shape first, then tune.
- **Correct, don't convict.** A failed check should snap the player back, not ban them. Honest players on bad connections will fail your check sometimes, as the table shows. Log each failure. MMO309 builds detection on the logs, where a pattern of failures separates the cheater from the unlucky player.
- **Spend full authority where the value is.** An MMO's economy, loot and inventory must be server-authoritative and transactional (week 8), because a duplication exploit costs you the economy. Movement can stay a bounded claim, because a 2.45 m blink costs you almost nothing.
- **Remember the wall.** Every movement check needs a path check (a ray cast, or a navmesh query) or players walk through walls at legal speed.

### Check this example

1. A game uses a per-packet check with `v = 5` m/s, `Δ = 0.05` s (20 updates a second) and `s = 0.15` s. What is the sustained speed factor a cheater gets? What would a token bucket with the same numbers allow?
2. A team wants no more than 10 corrected stalls per hour in the stall model above (one stall a minute, 0.2 to 0.8 s). What tolerance `s` do they need, and what blink does the bucket then allow at `v = 7`, `Δ = 0.1`?
3. A designer proposes a sliding window of `W = 1` s to limit the blink. Compute the sustained factor and blink with `s = 0.25`, and say which check you would ship instead.

<details>
<summary>Answers</summary>

1. Per-packet: `(0.05 + 0.15) / 0.05 = 4×`. Token bucket: sustained 1×, blink `5 × 0.2 = 1` m.
2. Corrected stalls per hour `= 60 × (0.8 − s) / 0.6 ≤ 10`, so `0.8 − s ≤ 0.1` and `s ≥ 0.7` s. The blink is `7 × (0.1 + 0.7) = 5.6` m.
3. Sustained `1.25 / 1 = 1.25×` and blink `7 × 1.25 = 8.75` m. A short window trades a smaller blink for a 25% permanent speed gain. A token bucket gives 1.0× and 2.45 m, better on both numbers.

</details>

## 3. Information is authority too

Everything above bounds what a client can make happen. A separate class of cheats only needs to see: wallhacks, radar hacks, loot-table readers, stealth detectors. These cheats forge nothing. They read data the server sent and the game's screen chose not to draw.

The design answer is the same as for claims. Decide what each client may know and send only that. For an MMO, the week 3 AOI system already does most of the work, because it sends each client only the entities near them. Three gaps remain.

- **Stealth and invisibility.** If a stealthed rogue is inside your AOI, the server should not send their position to you, only to their allies and to players whose detection rules see them. Otherwise a radar hack shows every rogue.
- **Hidden values.** Boss health thresholds, loot results before the corpse is opened, the next spawn location. Compute them on the server and send them when the player can see them.
- **Look-ahead.** Like Valorant's fog of war, you usually send an entity slightly before it becomes visible, so it does not pop in late. Size the look-ahead from the latency, and accept that it is a small, bounded leak.

The cost is CPU per visibility decision, on every tick, for every pair in AOI. That is the `e × n × k` term from week 5, and it is why Riot's engineers spent effort cutting their check from 50% of a frame to under 2%.

## 4. When a check fails

A check that fails has to do something. There are three responses, from mild to severe.

1. **Correct.** Reject the move and send the client the server's position. The player sees a snap back, often called rubber-banding. This is the right default, because the honest player on a stalled connection gets it too.
2. **Log.** Record the failure with the player, time, size and the connection's measured latency. One failure is noise. Forty in an hour on a connection with no stalls is a pattern.
3. **Act.** Flag, kick or ban. Only on evidence from the logs, and usually after a person or a detection model (MMO309) has looked.

A common mistake is to wire a single failure straight to a kick. The stall table shows why. At `s = 0.25` s, an honest player with one stall a minute is corrected 55 times an hour. Kick on the first failure and you disconnect every honest player on a flaky connection several times a session.

## In-class activity (25 minutes)

In groups of three, you receive a list of twelve messages from a prototype MMO client (handed out in class), such as `ATTACK(target, damage)`, `MOVE(x, y, z)`, `LOOT(corpse, item)`, `SET_COOLDOWN(ability, seconds)`, `CHAT(channel, text)`, `CRAFT(recipe, result_item)`.

1. Mark each message intent or claim.
2. Rewrite every claim as an intent, or write the bound it needs (a check shape and a tolerance).
3. For the movement message, choose `s` for a target of at most 15 corrected stalls per hour under the stall model in section 2, and report the blink.
4. Swap lists with another group and find one claim they missed or one bound that a cheater can beat.

Expected output: the annotated list, the movement numbers, and the flaw your partners found.

## Common misconceptions

- **"Anti-cheat is software you install."** Client-side anti-cheat raises the cost of cheating. Server design sets the ceiling on what cheating can gain. A server that accepts damage claims cannot be saved by any client software.
- **"A bigger lag tolerance is always more dangerous."** Only with the wrong check. With a token bucket, a bigger tolerance buys a slightly longer one-off blink, never a speed hack.
- **"Server authority means no client prediction."** The server decides, and the client still predicts so the game feels instant (CS202 weeks 8 and 9). Authority is about whose answer wins when they disagree.
- **"If the server sends it, the client can't misuse it because the UI hides it."** Anything sent can be read. Information authority means not sending it.

## Check yourself

1. A crafting request is `CRAFT(recipe_id, result_item_id, quality)`. Which parts are claims, and how would you rewrite it as an intent?
2. A token-bucket check uses `v = 6` m/s and `Δ = 0.1` s. Honest stalls in your players' data never exceed 0.4 s. What capacity `C` passes every honest stall, and what is the largest blink a cheater gets?
3. Your zone has 3,000 players at 10 position updates per second. The token bucket costs 0.2 µs per update and the wall ray cast 3 µs. Server-authoritative movement costs 8 µs. How many milliseconds of CPU per second does each design use, and what is the difference as a share of one core?

<details>
<summary>Answers</summary>

1. `result_item_id` and `quality` are claims, because the client decides what it made and how good it is. Rewrite as `CRAFT(recipe_id)`, and let the server check the ingredients in the database, roll the quality and create the item inside one transaction (week 8).
2. `C = v × (Δ + s) = 6 × (0.1 + 0.4) = 3` m. The largest blink is 3 m, and sustained speed stays at 1.0×.
3. 30,000 updates per second. Bucket plus ray cast: `3.2 × 30,000 = 96,000` µs = 96 ms. Server authority: `8 × 30,000 = 240` ms. The difference is 144 ms per second, 14.4% of one core.

</details>

## Lab / assignment hook

[Lab 06, movement validators](../labs/lab06.md). You implement the per-packet, sliding-window and token-bucket checks in Python, run them against recorded honest traces with stalls and against scripted cheaters, and produce the two tables of section 2 from your own code. Then you choose a tolerance for a target correction rate and defend it in a short memo. The validator you write goes into the final world server.

## Sources

- Wikipedia, "Battle.net" (accessed September 2026). The original Battle.net stored no game data beyond account data, so characters lived locally, which led to widespread cheating.
- Wikipedia, "Diablo II" (accessed September 2026). Open and closed realms; closed-realm characters stored on Blizzard's servers as a measure against cheating; open games subject to abuse because characters are stored on players' own drives.
- EVE University Wiki, "Warp" (accessed September 2026). Warp only to locations at least 150 km away; the exit point is fixed when the command is given.
- CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011). Destiny named as EVE's physics simulation, updating once per second.
- EVE University Wiki, "Server tick" (accessed September 2026). Client shows commands immediately; effects land on the next tick.
- Old School RuneScape Wiki, "Game square" and "Game tick" (accessed September 2026). One square per tick walking, two running; 0.6 s ticks.
- Chamberlain, P. "Demolishing Wallhacks with VALORANT's Fog of War" (Riot Games, 14 April 2020). Server withholds enemy positions until needed; potentially visible sets over map cells; look-ahead from velocity longer than expected ping; from 50% of server frame time in prototypes to under 2%.
- Fiedler, G. "What Every Programmer Needs To Know About Game Networking" (Gaffer on Games, 24 February 2010). Client/server authority and client-side prediction.
- The CPU costs per check and the stall model in section 2 are invented for teaching and labelled as such; the simulations quoted were run for this course and can be repeated with the lab 06 starter code.

## Interactive spec: examples/w06-authority-dial.html

**Insight the visual must make obvious:** the shape of the movement check decides what lag tolerance buys a cheater. With a per-packet check, tolerance becomes a permanent speed multiplier; with a sliding window it becomes a huge teleport after standing still; with a token bucket it becomes a small one-off blink, and the long-run speed is exactly legal. The honest player's corrections depend only on the tolerance.

**Layout.** Two linked views and a number panel. Desktop: side by side, panel beneath. Under 700 px: stacked, distance plot first.

1. **Distance over time (left).** x axis: 0 to 20 s of server time. y axis: cumulative accepted distance in metres. Three lines: "legal limit" (`v × t`, dashed), "honest player" (stalls injected, accepted distance), "cheater" (accepted distance). Rejected packets are red ticks on the line that sent them. A shaded band above the legal line shows the check's allowance (for the bucket, the band is `C` high; for the window, `v × s` sustained plus a marker at the post-idle blink; for per-packet, a line of slope `v × (Δ + s) / Δ`).
2. **Trade-off panel (right).** A small chart with tolerance `s` (0 to 1 s) on the x axis and two y axes: corrected stalls per hour for the honest model (left axis) and the cheater's gain for the current check (right axis; sustained factor for per-packet and window, blink in metres for bucket; label the unit). A vertical cursor at the current `s`.
3. **Number panel.** Sustained factor, blink, corrected stalls per hour (formula), rejections in the current 20 s run for honest and cheater, CPU per second for 2,000 players at `1/Δ` updates per second for the chosen design.

**Controls.**
- Check selector: per-packet, sliding window, token bucket, server-authoritative (the cheater line then equals the legal line and CPU uses 8 µs per update).
- Slider `s`, 0 to 1 s, step 0.05, default 0.25.
- Slider `W`, 1 to 10 s, default 5 (window only).
- Slider cheat factor, 1.0 to 5.0, step 0.05, default 1.5. Toggle "idle then blink" (cheater stands still for 10 s, then sends one packet with the largest distance the current check accepts).
- Slider stall frequency, 0 to 4 per minute, default 1; stall length range fixed at 0.2 to 0.8 s uniform. For the 20 s run, inject stalls at fixed seeded times so the picture is repeatable; a "reroll" button changes the seed.
- `v` fixed at 7 m/s, `Δ` selector 0.05, 0.1 (default), 0.2 s.
- Keyboard accessible sliders and selectors.

**Formulas.** Per-packet: accept `d ≤ v × (gap + s)`, gap measured on server arrival times. Window: accept if the sum of accepted distances with arrival time in `(t − W, t]` plus `d` is `≤ v × (W + s)`. Bucket: `credit = min(C, credit + v × gap)` with `C = v × (Δ + s)` and initial credit `C`; accept if `d ≤ credit`, then subtract. Rejected moves are not counted in accepted distance and do not consume credit. Sustained factor: per-packet `(Δ + s)/Δ`, window `(W + s)/W`, bucket 1. Blink: per-packet and bucket `v(Δ + s)`, window `v(W + s)`. Corrected stalls per hour: `60 × f × clamp((0.8 − s) / 0.6, 0, 1)` for `f` stalls per minute under the window and bucket checks; for per-packet, 0 when `s ≥ Δ` and `60 × f` when `s < Δ` (every stall holds at least two packets at `Δ ≤ 0.1`; label it approximate at `Δ = 0.2`). CPU per second: `2,000 × (1/Δ) × cost`, cost 3.2 µs for the three checks (0.2 check plus 3 wall ray), 8 µs for server-authoritative.

**Test values** (assert on load, `v = 7`, `Δ = 0.1`).
- `s = 0.25`: per-packet factor 3.5, blink 2.45 m; window (`W = 5`) factor 1.05, blink 36.75 m; bucket factor 1.0, blink 2.45 m.
- Corrected stalls per hour at 1 per minute: 55 at `s = 0.25`, 30 at `s = 0.5`, 0 at `s = 0.8`.
- Bucket blink at `s = 0.5`: 4.2 m; at `s = 0.8`: 6.3 m. Per-packet factor at `s = 0.5`: 6.
- CPU per second: 64 ms (checks) and 160 ms (server-authoritative) at `Δ = 0.1`.

**First screen:** per-packet check, `s = 0.25`, cheat factor 3.5, so the cheater's line races away with no red marks. Caption: "This cheater runs 3.5 times legal speed and the server accepts every packet. Switch the check to token bucket."
