# MMO309 · Week 02 — Never trust the client

**Why this matters:** In CS202 you learned that the server must decide what happens. That rule has a second half that most games break. The server must also decide what each player gets to know, because anything sent to a client can be read by the player who owns it. This week you put a number on how much hidden information each design leaks, and on what the checks cost to run.

**You will be able to:**
- List what a game client can lie about and what it can learn, and assign each item to a server-side control.
- Compute the look-ahead a server needs to reveal an enemy in time for a given ping and tick, and the information a cheater gains from it.
- Compare send-everything, area-of-interest, visibility-set and line-of-sight policies by leak per round and by server cost.
- Compute the chance that a sampled expensive check catches an attacker within `n` actions, and choose a sampling rate.

**Before class:** Chamberlain, P. (2020), "Demolishing Wallhacks with VALORANT's Fog of War", Riot Games technology blog, 14 April 2020 (about 15 minutes). Hoglund & McGraw (2007), *Exploiting Online Games*, chapter 2 ("Game Hacking 101"). Reread section 3 of [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md).

**Prerequisites from earlier courses:** [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (intent versus results, and the range, rate, state, ownership and reach checks; this lecture does not repeat them). [CS202 week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (why remote players are drawn slightly in the past). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success in `n` tries, used in section 3). [Week 1](w01-threat-modeling-for-games.md) of this course (STRIDE, and the ledger you will add rows to).

**Interactive:** [the fog-of-war leak explorer](../examples/w02-fog-of-war-leak.html). Keep it open during section 2.

---

## 1. The trust ledger

CS202 week 4 gave you one rule, clients send intent and servers compute results. That rule covers only one direction of traffic. A client is on the far side of a trust boundary in both directions, so there are two questions for everything that crosses it.

- **What can the client claim?** Anything the server accepts from a client is a claim the player can forge. This is STRIDE's tampering and spoofing.
- **What can the client learn?** Anything the server sends to a client is known to the player, whatever the game draws on screen. This is STRIDE's information disclosure.

The second question is the one teams forget. A game that validates every input perfectly can still send each client the position of every enemy on the map, the contents of an unopened chest, or the result of a dice roll a few hundred milliseconds early. A wallhack does not break any rule the server enforces. It draws data the server chose to send.

Here is a trust ledger for a typical MMO feature set. Fill in one like it for every feature you design.

| Data | Crosses to client? | If the player reads or changes it | Server-side control |
|---|---|---|---|
| Player's movement input | Claim from client | Speed, teleport, fly | Movement validation (week 3) |
| Player's own health | Sent to client | Nothing gained by reading it | Never accept it back |
| Positions of nearby enemies | Sent to client | Wallhack, radar | Send only what the player could see (section 2) |
| Loot table of a boss | Should not cross | Know which boss to farm, time runs | Keep tables on the server, roll on the server |
| Result of a loot roll | Sent on open | Early knowledge if sent before the chest opens | Send the result only when revealed |
| Cooldown timers | Both | Cast faster than allowed | Server keeps the clock (CS202 week 4) |
| Random number seed | Should not cross | Predict every future roll | Keep seeds on the server |
| Quest and dialogue text | Sent in the client install | Spoilers | Accept it; not an asset |
| Client's own code and memory | Lives on client | Anything the client knows | Client integrity (week 5) |

Two principles fall out of the table.

**The need-to-know rule.** Send a client only what its player needs to see now. The common summary of "never trust the client" among game developers includes exactly this half. No information should go to a client unless it is need-to-know. A server that synchronizes every client with every other client's full state is fast and simple, and a wallhack on it shows every player's position, team, health and ammunition.

**The accept-the-leak rule.** Some leaks are not worth closing. Quest text, map geometry and item art ship in the install, and a player who datamines them gains a spoiler. Your week 1 ledger decides which leaks cost enough to fix. Hidden information in PvP usually does. Spoilers usually do not.

## 2. Worked example: how much does fog of war leak?

### The hook

*VALORANT* is a tactical shooter where seeing an enemy a moment early decides a round. In April 2020, before launch, Riot's anti-cheat lead Paul Chamberlain described how the game fights wallhacks. The server does not send an enemy's position to a client until that enemy is close to being visible to that player. A cheat that draws enemies through walls then has nothing to draw.

The hard part was not the idea. It was timing and cost. If the server waits until an enemy is actually visible, the enemy's data arrives one network trip late, and on the defender's screen the enemy pops into view after they have already started shooting. So Riot sends the data a little early. The post describes extending each player's box by their velocity times a look-ahead time chosen to be larger than the expected ping. That look-ahead is information a cheater can see and an honest player cannot. It is the leak the design accepts. The first prototype also used about half of the server's frame time. The shipped version, built on precomputed visibility data, used under 2%, on 128-tick servers.

So there are two numbers to understand. How early must the server reveal an enemy, and how much does each reveal policy leak?

### The model

An enemy comes around a corner into a player's view. Call the moment they become visible `t_v`. The server re-evaluates visibility once per tick and sends the enemy's data to the client if the enemy will be visible within a **look-ahead** `τ` (tau). The data then needs one trip across the network to reach the client.

For the enemy to appear on the honest player's screen on time, the data must leave the server at least one one-way trip plus one tick before `t_v`:

```
τ_min = ping / 2 + T
pop_in = max(0, τ_min − τ)
```

- `ping` is the round-trip time in ms, so `ping / 2` is the one-way trip.
- `T` is the server tick, 1000 / 128 ≈ 7.8 ms at 128 ticks per second. In the worst case the server notices the enemy one tick late.
- `pop_in` is how late the enemy appears on an honest screen, in ms, when `τ` is too small.

The **leak** is the time the cheater's client holds an enemy's position while the player cannot see that enemy. Under a look-ahead policy it is `τ` for each time an enemy comes into view (each **peek**). Over a round, for one enemy,

```
leak per round = peeks × τ
```

This ignores interpolation delay (CS202 week 10), which shifts both sides of the comparison by the same amount, and assumes the server's visibility test is exact. Real tests are not exact, and that changes the leak, as you will see.

### Numbers you can check

Fix `τ = 60 ms`, four peeks per round, and vary the player's ping.

| Ping | `τ_min` | Pop-in at `τ = 60 ms` | Leak per round at 60 ms | Adaptive `τ = τ_min + 20` | Leak per round, adaptive |
|---|---|---|---|---|---|
| 20 ms | 17.8 ms | 0 ms | 0.24 s | 37.8 ms | 0.15 s |
| 60 ms | 37.8 ms | 0 ms | 0.24 s | 57.8 ms | 0.23 s |
| 100 ms | 57.8 ms | 0 ms | 0.24 s | 77.8 ms | 0.31 s |
| 150 ms | 82.8 ms | 22.8 ms | 0.24 s | 102.8 ms | 0.41 s |

Check the 150 ms row. The one-way trip is 75 ms, plus 7.8 ms of tick, gives 82.8 ms. With 60 ms of look-ahead the enemy's data arrives 22.8 ms late, so the enemy pops in. An adaptive look-ahead, one that grows with each player's own ping, fixes the pop-in but leaks more to high-ping players.

This script reproduces the table.

```python
TICK_MS = 1000 / 128          # server tick, about 7.8 ms
PEEKS = 4                     # times one enemy comes into view per round

def tau_min(ping_ms):
    """Shortest look-ahead that still gets the enemy to the client in time."""
    return ping_ms / 2 + TICK_MS

def pop_in(ping_ms, tau_ms):
    """How late an enemy appears on an honest screen, in ms."""
    return max(0.0, tau_min(ping_ms) - tau_ms)

print("ping  tau_min  pop-in@60  leak@60  adaptive tau  leak adaptive")
for ping in (20, 60, 100, 150):
    adaptive = tau_min(ping) + 20
    print(f"{ping:4}  {tau_min(ping):7.1f}  {pop_in(ping, 60):9.1f}  "
          f"{PEEKS * 60 / 1000:6.2f}s  {adaptive:12.1f}  {PEEKS * adaptive / 1000:12.2f}s")
```

Output:

```
ping  tau_min  pop-in@60  leak@60  adaptive tau  leak adaptive
  20     17.8        0.0    0.24s          37.8          0.15s
  60     37.8        0.0    0.24s          57.8          0.23s
 100     57.8        0.0    0.24s          77.8          0.31s
 150     82.8       22.8    0.24s         102.8          0.41s
```

Now compare whole policies. Take one enemy over a 100-second round. The enemy is visible for 3 s in total across 4 peeks, is within 50 m of the player for 40 s, and stands in map cells that a coarse visibility table marks as "could be visible" for 10 s.

| Policy | When the enemy's position is sent | Leak per round (sent but not visible) | Server cost per pair per tick |
|---|---|---|---|
| Send everything | Always | 100 − 3 = 97 s | None |
| Area of interest, 50 m | While within 50 m | 40 − 3 = 37 s | One distance check |
| Visibility table (PVS) | While in cells that could see each other | 10 − 3 = 7 s | One table lookup |
| Exact line of sight + `τ` | Only `τ` before each peek | 4 × 0.06 = 0.24 s | Several ray tests |

A **potentially visible set (PVS)** is a table, computed offline from the map, that says for each pair of map cells whether anything in one could ever see anything in the other. It is cheap to query and conservative, because it says "maybe visible" more often than the truth.

Read down the leak column. It falls from 97 s to 37 s to 7 s to a quarter of a second, and each step costs more server work per pair of players. The cheapest policy leaks the whole round. The most expensive leaks a quarter of a second.

### Move it yourself

Open `examples/w02-fog-of-war-leak.html`. The left view is a top-down corridor with a corner. An enemy walks toward the corner. The player's screen and the cheater's screen are drawn side by side, and the cheater's shows every enemy the server has sent. Switch the policy and watch the cheater's view fill up or empty out. The right view plots leak per round against pop-in for the look-ahead slider. Drag `τ` down and the leak falls toward zero while the pop-in line rises from zero at exactly `τ_min`. Then drag the ping slider up and watch `τ_min` move right. There is no setting that gives both zero leak and zero pop-in, because the network trip has to be paid by someone.

### Cross-game recognition

**VALORANT (2020 onward).** A single ray to each enemy's center was too pessimistic. Riot's first attempt cast ten rays, to the corners of each enemy's box, its camera and its center, which was still fallible and ten times as expensive. The shipped design uses a PVS built from the map with enemies' boxes stretched by velocity times the look-ahead. In our table, Riot picked the third row with row four's `τ` added, and paid for it with under 2% of frame time. The post says that hiding irrelevant enemies also reduced network traffic, so the change paid for part of its own cost.

**Age of Empires (1997) and deterministic lockstep.** Mark Terrano and Paul Bettner's 2001 account of the game's networking describes the opposite design. Every machine ran the same simulation and players exchanged only commands. Sending each unit's state instead would have capped the game at about 250 moving units over a 28.8k modem. The trade for security is stark. Tampering was hard, because a client that computed anything differently fell out of sync and the game stopped. But every client simulated the whole world, so every client held every enemy's position all the time. That is the first row of our table by construction. Map-revealing hacks in lockstep strategy games are not a bug to fix. They follow from the architecture. [CS202 week 12](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) covers lockstep.

**MMO area of interest.** Most MMO servers already filter what they send by distance, for bandwidth rather than security. [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) covers the grid and radius schemes. That is row two. For a raid or a quest hub, a 37-second leak does not matter. For open-world PvP, where a radar hack shows the gankers waiting behind a hill, it does, and the same visibility tests apply.

Three games, one model. Every design sits somewhere on the ladder from "send all" to "exact line of sight with look-ahead", and each rung trades server cost for leak.

### Design judgment

- **Decide per asset.** Hidden enemy positions in competitive PvP are worth a visibility system. Positions of other players in a safe city are not. Put each piece of hidden information in your week 1 ledger with its cost before you pay for protecting it.
- **Cap the look-ahead.** An adaptive `τ` that follows each player's ping gives more information to high-ping players. A cheater can add fake latency to buy more look-ahead. Cap `τ` at a value you chose, and accept pop-in beyond it for very high pings.
- **Conservative is fine.** A PVS that says "maybe visible" too often leaks a few seconds. A test that says "not visible" too often makes enemies pop in and shoot honest players from nowhere. When in doubt, err toward sending.
- **Sound is information too.** Footsteps heard through a wall need the enemy's position. If the game plays positional audio for enemies at 30 m, the server must send positions at 30 m, and a wallhack gets them. Coordinate the audio design with the leak budget.
- **Designs that need no secret beat designs that hide one.** A stealth mechanic that relies on the client not drawing an invisible player leaks. One where the server does not send the invisible player's position does not.

### Check this example

1. A game runs a 64-tick server. What is `τ_min` for a player with 80 ms ping?
2. A designer sets `τ = 150 ms` for everyone "to be safe". With six peeks per round, how much does each enemy leak per round, and at what ping does pop-in begin?
3. In the policy table, the team replaces the 50 m area of interest with a 25 m radius, and the enemy is within 25 m for 12 s. What is the new leak, and why might footsteps make this change impossible?

<details>
<summary>Answers</summary>

1. `T = 1000 / 64 = 15.6 ms`, so `τ_min = 40 + 15.6 = 55.6 ms`.
2. Leak is `6 × 0.15 = 0.9 s` per enemy per round. Pop-in begins when `ping / 2 + 7.8 > 150`, so at a ping above 284 ms.
3. `12 − 3 = 9 s`. If footsteps are audible at more than 25 m, the client needs positions out to the audible range, so the radius cannot be smaller than the audio range without changing the audio design.

</details>

## 3. What validation costs, and how to pay for it

Every check you add runs on a server you pay for. Security checks compete with game simulation for the same frame time, which is why Riot's first prototype, at half the frame, could not ship.

### Pairwise checks scale badly

Visibility is a check between pairs. With `N` players who can see each other, there are `N × (N − 1)` ordered pairs, each checked every tick.

| Situation | Players `N` | Pairs | Tick rate | Pair checks per second |
|---|---|---|---|---|
| 5 v 5 shooter | 10 | 90 | 128 | 11,520 |
| MMO battleground | 40 | 1,560 | 20 | 31,200 |
| MMO city at peak | 200 | 39,800 | 10 | 398,000 |

Pair counts grow with the square of the crowd. If an exact line-of-sight test costs 2 µs (an assumed figure for illustration), the city needs 0.8 s of CPU per second, most of a core, for visibility alone. That is why an MMO uses cheap tests (distance, grids, PVS) for crowds and saves exact tests for the few places where they pay, such as PvP zones.

### Sampled validation

Some checks are too expensive to run every time. Re-simulating a player's last ten seconds of movement from their inputs, replaying a crafting chain to confirm its output, or asking a human to review a trade are all examples. The standard answer is to run the expensive check on a random sample of events, a fraction `p` of them.

If an attacker performs `n` bad actions and each is checked independently with probability `p`, the chance at least one is checked is the complement rule from MA102 week 3:

```python
def p_caught(p, n):
    """Chance that at least one of n bad actions is picked for a full check."""
    return 1 - (1 - p) ** n

for p in (0.01, 0.02, 0.05):
    row = "  ".join(f"n={n}: {p_caught(p, n):.3f}" for n in (10, 50, 100, 200))
    print(f"p={p:.2f}  expected actions before caught {1 / p:5.0f}  {row}")
```

Output:

```
p=0.01  expected actions before caught   100  n=10: 0.096  n=50: 0.395  n=100: 0.634  n=200: 0.866
p=0.02  expected actions before caught    50  n=10: 0.183  n=50: 0.636  n=100: 0.867  n=200: 0.982
p=0.05  expected actions before caught    20  n=10: 0.401  n=50: 0.923  n=100: 0.994  n=200: 1.000
```

Two readings matter. First, sampling works against repeat offenders. An exploit worth running once is rarely caught, but an exploit run 200 times at a 2% sampling rate is caught 98% of the time. Most profitable exploits are repeated, because that is how they pay. Second, the expected number of actions before the first catch is `1 / p`. If each bad action yields `g` gold, an attacker expects to take `g / p` before the first check fires. At `p = 0.02` and 1,000 gold per action, that is 50,000 gold. Your penalty on being caught must take back at least that much, or the attack still pays on average. Confiscating all the proceeds and the account makes sampling a deterrent. Taking back only the last action's gold does not.

Pick `p` from your budget, then check the deterrence. If the full check costs `c` CPU-seconds and there are `E` events per second, sampling costs `p × E × c` CPU-seconds each second. Week 7's detection features will tell you where to aim the sample instead of choosing at random, which raises the catch rate for the same cost.

## 4. Designing so the client has nothing worth lying about

The strongest defense is a design in which the client never holds a secret and never makes a decision. Server checks catch lies. Good design removes the reason to lie. Some patterns that do this:

- **Roll on the server, reveal on open.** Decide loot when the boss dies, but send the result only when the player opens the chest. A client that never has the result cannot show it early.
- **Keep seeds and tables server-side.** If the client can see the random number generator's seed, it can predict every roll. If it can see a loot table, the community will publish it within a day, which may be fine for items and bad for a rare-spawn timer.
- **Give requests IDs.** A client that sends "buy item 17, request 9,041" twice gets one purchase. The server remembers request IDs it has processed. This makes retries safe and makes replaying a message useless. Week 4 builds on this for trades.
- **Rate-limit by design.** A crafting action that takes 3 seconds on the server cannot be done 50 times a second by a macro, whatever the client sends.
- **Prefer mechanics that do not need hidden state on the client.** Invisibility, fog, hidden traps and bluffs all need the server to withhold data. Budget for that in design review, not after the first wallhack appears.

None of these is about catching cheaters. They make whole categories of cheat pointless, which is cheaper than detecting them forever.

## In-class activity (25 minutes)

Pairs. You receive the feature list of a small open-world PvP MMO: stealth class with invisibility, player-built traps, a boss with a timed rare drop, footsteps audible at 40 m, a 30 m nameplate range, and an area-of-interest radius of 120 m. The server runs at 20 ticks per second.

1. (8 min) Build the trust ledger for these six features: what each sends to the client, what a player gains by reading it, and the control you propose.
2. (7 min) For the stealth class, choose a look-ahead `τ` for revealing an invisible player who is about to become visible. Compute `τ_min` for 50 ms and 200 ms ping. Decide your cap and state the pop-in above it.
3. (5 min) The designers want footsteps at 40 m but the security lead wants the AOI radius for enemy players cut to 30 m. Propose a compromise and state what leaks under it.
4. (5 min) The boss's rare drop is decided by a server roll. Propose a sampled check for suspicious kill timing with a `p` that catches a farmer repeating the kill 100 times with at least 90% probability.

Expected output: the six-row ledger, two `τ_min` values and a cap, one compromise, and a value of `p` with its working.

## Common misconceptions

- **"If the game doesn't draw it, the player can't see it."** The client holds whatever the server sent. What the renderer draws is a choice the player controls.
- **"Encrypting the traffic hides the data."** The client decrypts it to use it, on a machine the player owns. Encryption protects against third parties, not against the player.
- **"Perfect fog of war means zero leak."** Zero leak means pop-in for every player with nonzero ping. Every workable design leaks at least the look-ahead.
- **"Sampling 2% of events only catches 2% of cheaters."** It catches 2% of single events. A cheater who repeats the exploit 100 times is caught 87% of the time.

## Check yourself

1. Rank these by leak per round for an enemy visible for 5 s over a 120 s round, within 60 m for 45 s, in PVS-visible cells for 14 s, and peeking 5 times at `τ = 50 ms`: send all, AOI 60 m, PVS, exact line of sight with look-ahead.
2. A 30-tick MMO server must reveal a stealthed player to a victim with 120 ms ping. What is `τ_min`? What is the pop-in if the designer caps `τ` at 50 ms?
3. An MMO city has 150 visible players and a 10 Hz tick. How many pair checks per second does exact visibility need?
4. An exploit yields 2,000 gold per use. You sample 1% of uses for a full re-simulation. How much gold does an attacker expect to take before the first catch, and what must your penalty confiscate to make the exploit lose money on average?
5. Explain why deterministic lockstep makes tampering hard and information hiding impossible.

<details>
<summary>Answers</summary>

1. Send all `120 − 5 = 115 s`. AOI `45 − 5 = 40 s`. PVS `14 − 5 = 9 s`. Line of sight `5 × 0.05 = 0.25 s`.
2. `T = 33.3 ms`, `τ_min = 60 + 33.3 = 93.3 ms`. With `τ = 50 ms`, pop-in is `43.3 ms`.
3. `150 × 149 × 10 = 223,500` checks per second.
4. Expected uses before the first catch is `1 / 0.01 = 100`, so `100 × 2,000 = 200,000` gold. The penalty must take back at least that much, so confiscate everything gained from the exploit, which usually means the whole account's proceeds, not the last use.
5. Every machine runs the full simulation from the same commands. A client that changes a result falls out of sync, so tampering is detected. But running the full simulation needs every unit's state, so every client holds every enemy's position.

</details>

## Lab / assignment hook

No new lab this week. Add rows to your [Lab 01](../labs/lab01.md) threat ledger for every information-disclosure threat in the sample game, using this week's leak model to estimate `I`. Next week's [Lab 03](../labs/lab03.md) builds the movement validator, which is the claim side of the trust ledger.

## Sources

- Chamberlain, P. "Arkem" (14 April 2020). "Demolishing Wallhacks with VALORANT's Fog of War." Riot Games technology blog (riotgames.com/en/news/demolishing-wallhacks-valorants-fog-war). The single ray, then ten rays to the box corners, camera and center; the shipped PVS approach with boxes extended by velocity times a look-ahead larger than the expected ping; the prototype at about 50% of server frame time and the result under 2%; 128-tick servers; reduced network traffic for hidden players.
- Terrano, M. & Bettner, P. (March 2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond." Gamasutra, republished on Game Developer. Identical simulation on every machine exchanging only commands; the estimate that sending unit state would limit the game to 250 moving units; the 28.8k modem target; out-of-sync detection making client tampering hard.
- Wikipedia, "Cheating in online games" (accessed September 2026). The "never trust the client" maxim and its need-to-know half; wallhacks and world-hacking in strategy games with fog of war.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games*. Addison-Wesley, chapter 2.
- The corridor scenario, peek counts, round times, pair-check costs and gold figures are teaching values, not measurements from any game.

## Interactive spec: examples/w02-fog-of-war-leak.html

**Insight the visual must make obvious:** every fog-of-war policy trades leak (what a cheater sees that an honest player cannot) against either server cost or pop-in. Revealing earlier protects honest players from pop-in and hands cheaters the look-ahead. No setting gives zero leak and zero pop-in, because someone has to pay for the network trip.

**Layout.** Two linked views and a number panel. Left: a top-down corridor. Right: a leak and pop-in plot. On screens under 700 px wide, stack left view, right plot, numbers. No page-level horizontal scroll.

1. **Left view, "What each screen shows".** A generic top-down L-shaped corridor. The player dot sits in one arm facing the corner. An enemy dot walks along the other arm toward the corner at 5 m/s, loops back, and repeats (a 4-second loop, one peek per loop). Draw two small panels under the map, "Honest screen" and "Cheater's screen". The honest screen shows the enemy only while in line of sight. The cheater's screen shows the enemy whenever the server has sent it, as a hollow marker when not visible. Shade the corridor region in which the current policy would send the enemy's position. A timeline strip under the panels marks, for the last loop, the interval the enemy was sent (bar) and visible (filled bar), and a red tick where the enemy popped in late on the honest screen.
2. **Right plot, "Leak vs pop-in".** x axis look-ahead `τ` from 0 to 250 ms. Left y axis leak per round in seconds (0 to 1.2, for `peeks` = 4). Right y axis pop-in in ms (0 to 150). Draw `leak = peeks × τ / 1000` as a rising line and `pop_in = max(0, τ_min − τ)` as a falling line, with a vertical marker at `τ_min` labelled with its value, and a dot at the current `τ` on each line.
3. **Number panel.** `T`, `τ_min`, current `τ`, pop-in, leak per round for the current policy, and the four-row policy table from the lecture computed live.

**Controls.**
- Policy radio: "Send everything", "Area of interest 50 m", "Visibility table (PVS)", "Line of sight + look-ahead" (default).
- Look-ahead `τ` slider, 0 to 250 ms, step 1, default 60.
- Ping slider, 0 to 300 ms, step 5, default 150.
- Tick rate select: 20, 30, 64, 128 (default 128).
- Peeks per round stepper, 1 to 10, default 4.
- All controls reachable by Tab, with visible focus. Animation pauses under `prefers-reduced-motion`, with a step button instead.

**Formulas.** `T = 1000 / tickRate`. `τ_min = ping / 2 + T`. `pop_in = max(0, τ_min − τ)` for the line-of-sight policy, 0 for the others. Leak per round for one enemy in a 100 s round, visible 3 s, within 50 m for 40 s, in PVS cells for 10 s: send all `100 − 3`, AOI `40 − 3`, PVS `10 − 3`, line of sight `peeks × τ / 1000`.

**Test values** (assert on load):
- 128 Hz, ping 60: `τ_min = 37.8` (one decimal), pop-in at `τ = 60` is 0.
- 128 Hz, ping 150, `τ = 60`: `τ_min = 82.8`, pop-in 22.8.
- 64 Hz, ping 80: `τ_min = 55.6`.
- Line of sight, 4 peeks, `τ = 60`: leak 0.24 s. Send all 97 s, AOI 37 s, PVS 7 s.
- 6 peeks, `τ = 150`: leak 0.9 s.

**First screen:** line-of-sight policy at 128 Hz, ping 150 and `τ = 60`, so the honest screen shows a red pop-in tick of 22.8 ms and the cheater's screen shows the enemy 60 ms early. Caption: "Reveal later and honest players get shot by enemies they cannot see. Reveal earlier and cheaters see them first."
