# MMO404 · Week 08 — Distributed simulation research

**Why this matters:** Splitting one battle across several servers raises a question the military and physics simulation communities spent forty years on. When may a server simulate the next tick without waiting for its neighbours? Game developers keep rediscovering their answers under new names. Knowing the research lets you read a server meshing design and say how much waiting it will do before anyone writes code.

**You will be able to:**
- Compute the tick-by-tick finish times of two servers that exchange border events, for a given lookahead and message delay, and find their effective tick length.
- Derive the lookahead a border allows from the minimum delay of every interaction that crosses it, and name the game design rules that raise or destroy it.
- Compare conservative and optimistic synchronization for a given interaction rate and rollback cost, and choose between them.
- Place the research systems (SIMNET, DIS, HLA, Time Warp, Colyseus, Donnybrook) on one map and say what each contributed to shipped games.

**Before class:** Richard Fujimoto, "Parallel Discrete Event Simulation" (Winter Simulation Conference, 1989), sections on conservative and optimistic mechanisms. Bharambe, Pang and Seshan, "Colyseus: A Distributed Architecture for Online Multiplayer Games" (NSDI 2006), sections 1 to 3. Skim the abstract of Donnybrook (SIGCOMM 2008).

**Prerequisites from earlier courses:** [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) (command turns and the effective turn length `max(T, (T + L_max) / k)`; this lecture generalizes it). [CS202 week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (clients already draw the world in the past). [MMO302 week 4, zone servers and handoff](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) (ghosts and the border). [Week 2, seamless worlds and boundary handoff](w02-seamless-worlds-and-boundary-handoff.md). [Week 7, time dilation revisited](w07-time-dilation-revisited.md) (clock domains).

**Interactive:** [w08-lookahead-timeline.html](../examples/w08-lookahead-timeline.html). Keep it open during section 2.

---

## 1. An older field than MMOs

In the early 1980s DARPA paid Bolt, Beranek and Newman (BBN) to link tank simulators across a network so crews in different buildings could fight in one virtual battlefield. The project, SIMNET, ran from the early to the late 1980s. It introduced ideas every MMO programmer now uses. Each simulator owns its own vehicles. Simulators broadcast state rather than asking for it. And instead of sending a tank's position every frame, a simulator sends it with a velocity and lets everyone else **dead reckon** (extrapolate) until the error grows too large. That is CS202's extrapolation, thirty years earlier.

SIMNET became the IEEE 1278 standard, Distributed Interactive Simulation (DIS), drafted from 1992 and last revised as IEEE 1278.1-2012. DIS was followed by the High Level Architecture (HLA), first published as IEEE 1516-2000, revised as "HLA Evolved" in 2010 and again as IEEE 1516-2025. HLA calls each simulator a **federate** and the whole exercise a **federation**. A middleware layer, the run-time infrastructure (RTI), moves data between federates and, if asked, manages time.

Alongside the military work, computer scientists studied **parallel discrete event simulation** (PDES), running one large simulation on many processors. Their vocabulary is the one this lecture uses.

- A **logical process** (LP) is one piece of the simulation with its own state and clock. For us, one server.
- An **event** is a change with a timestamp. A spell landing at game tick 1,204 is an event.
- The **causality rule**: every LP must process its events in timestamp order. If server A has simulated tick 1,210 and then receives an event for tick 1,204, it has already shown players a world that could not have happened.

There are two families of answers. **Conservative** synchronization, from Chandy and Misra (1979) and independently from Bryant (1977), and usually named after all three, never lets an LP process an event until it is certain no earlier event can still arrive. **Optimistic** synchronization, from Jefferson's Time Warp (1985), lets every LP run ahead and undoes its work when an earlier event turns up. Games use both, usually without saying so. Lockstep RTS games are conservative. Fighting game rollback is optimistic.

The rest of this lecture turns the two families into numbers for the case you care about, two servers sharing a border in a seamless world.

## 2. Worked example: how far can two servers drift apart?

### The hook

In CS202 week 12 you met Age of Empires (Ensemble Studios, 1997). Eight players on 28.8 kbit/s modems stayed in step although their latency swung between 20 and 1,000 ms. The trick was to schedule every command two turns in the future. A command issued in turn `n` ran in turn `n + 2`, so each machine had a whole turn of slack in which the command could travel. The game never had to wait unless a link was slower than that slack.

Now put two MMO servers side by side. Server A owns the west of a battlefield and server B the east. Every tick, fights on the border create events that cross between them. Must A wait for B every tick, like a lockstep game with no scheduling slack? Or can A run a few ticks ahead? The answer is a single number, the **lookahead**, and the research literature has a precise definition of it. HLA defines a federate's lookahead as the interval into the future below which it promises not to send any more messages. If B has reached tick 50 and its lookahead is 10, A knows it will receive nothing from B stamped before tick 60, so A may safely run up to tick 60.

### The model

Count time in ticks. Server A's tick `k` takes `X_A(k)` milliseconds of real time to compute, and B's takes `X_B(k)`. Every event B creates in tick `j` affects A no earlier than tick `j + L`. `L` is the lookahead in ticks, at least 1, since no event can affect the tick that is already being computed. Messages take `δ` milliseconds to cross between the servers.

The conservative rule says A may start tick `k` once it has finished tick `k − 1` and has received everything B produced in tick `k − L`. Write `F_A(k)` for the real time at which A finishes tick `k`.

```
F_A(k) = max( F_A(k−1),  F_B(k−L) + δ ) + X_A(k)
F_B(k) = max( F_B(k−1),  F_A(k−L) + δ ) + X_B(k)
F(k) = 0 for k ≤ 0
```

That is the whole model. The first term in each `max` is "finish my own previous tick." The second is "hear from my neighbour." A server **stalls** whenever the second term is larger.

When `L = 1` and `δ = 0`, both servers start each tick together and every tick costs `max(X_A, X_B)`, the slower of the two. This is lockstep. As `L` grows, a server that had a slow tick can fall behind by up to `L − 1` ticks without holding the other one up.

### Numbers you can check

Give both servers an average tick of 50 ms, but out of phase. A takes 40, 60, 40, 60 ms and B takes 60, 40, 60, 40 ms. Neither is slower on average. With `L = 1` and `δ = 0`, work out the first ticks by hand.

| Tick | A starts | A finishes | B starts | B finishes |
|---|---|---|---|---|
| 1 | 0 | 40 | 0 | 60 |
| 2 | max(40, 60) = 60 | 120 | max(60, 40) = 60 | 100 |
| 3 | max(120, 100) = 120 | 160 | max(100, 120) = 120 | 180 |
| 4 | max(160, 180) = 180 | 240 | max(180, 160) = 180 | 220 |

Every pair of ticks takes 120 ms. Each server does 50 ms of work per tick and pays 10 ms per tick waiting for the other's slow tick. Now let `L = 2`. A's tick 3 needs B's tick 1, which finished at 60, long before A needs it. Neither server ever waits, and the pair runs at 50 ms per tick. One tick of slack absorbed all the jitter.

The code below runs 100 ticks for several settings.

```python
def finish_times(xa, xb, L, delay=0):
    """Finish time of every tick on two servers that exchange border events.
    Tick k on one server may start once its own tick k-1 is done and the other
    server's tick k-L has finished and its message has travelled `delay` ms."""
    fa, fb = [0] * (len(xa) + 1), [0] * (len(xb) + 1)
    for k in range(1, len(xa) + 1):
        need = k - L
        wait_a = fb[need] + delay if need >= 1 else 0
        wait_b = fa[need] + delay if need >= 1 else 0
        fa[k] = max(fa[k - 1], wait_a) + xa[k - 1]
        fb[k] = max(fb[k - 1], wait_b) + xb[k - 1]
    return fa[1:], fb[1:]

xa = [40, 60] * 50          # server A: 40 ms, 60 ms, 40 ms, ...
xb = [60, 40] * 50          # server B: the opposite
for L, delay in [(1, 0), (2, 0), (1, 20), (2, 20), (2, 60)]:
    fa, fb = finish_times(xa, xb, L, delay)
    print(f"L={L} delay={delay:2d}  A {fa[:4]}  B {fb[:4]}  per tick {max(fa[-1], fb[-1]) / 100:.1f} ms")
```

```
L=1 delay= 0  A [40, 120, 160, 240]  B [60, 100, 180, 220]  per tick 60.0 ms
L=2 delay= 0  A [40, 100, 140, 200]  B [60, 100, 160, 200]  per tick 50.0 ms
L=1 delay=20  A [40, 140, 180, 300]  B [60, 100, 220, 260]  per tick 79.8 ms
L=2 delay=20  A [40, 100, 140, 200]  B [60, 100, 160, 200]  per tick 50.0 ms
L=2 delay=60  A [40, 100, 160, 220]  B [60, 100, 160, 200]  per tick 55.0 ms
```

The third row is the one to worry about. Servers in the same data centre still take a few milliseconds per message once you count serialization, the network stack and the time a message waits for the next send. At `L = 1`, 20 ms of delay turns a 50 ms tick into an 80 ms tick, a 20 Hz server into a 12.5 Hz server. With `L = 2` the delay disappears into the slack. With `δ = 60` even `L = 2` is not enough. Each server needs `50 + 60 = 110` ms between a tick and the neighbour tick that depends on it, spread over 2 ticks, so 55 ms per tick.

That is the same rule you derived for lockstep in CS202 week 12, with the neighbour's tick in place of the turn:

```
effective tick ≈ max( X,  (X + δ) / L )
```

where `X` is the average tick time. Jitter adds a penalty on top when `L` is small, as the next run shows. Tick times are random between 30 and 70 ms (average 50), from the seeded generator the interactive uses.

```python
def mulberry32(seed):
    s = seed & 0xFFFFFFFF
    def rnd():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((s ^ (s >> 15)) * (s | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd

def finish_times(xa, xb, L, delay=0):
    fa, fb = [0] * (len(xa) + 1), [0] * (len(xb) + 1)
    for k in range(1, len(xa) + 1):
        need = k - L
        fa[k] = max(fa[k - 1], fb[need] + delay if need >= 1 else 0) + xa[k - 1]
        fb[k] = max(fb[k - 1], fa[need] + delay if need >= 1 else 0) + xb[k - 1]
    return fa[1:], fb[1:]

rnd = mulberry32(404)
ticks = 10_000
xa = [30 + 40 * rnd() for _ in range(ticks)]     # 30 to 70 ms, mean 50
xb = [30 + 40 * rnd() for _ in range(ticks)]
print("L    delay 20 ms   delay 60 ms   (ms per tick; 50 would be perfect)")
for L in (1, 2, 3, 4, 6, 8):
    row = [max(finish_times(xa, xb, L, d)[0][-1], finish_times(xa, xb, L, d)[1][-1]) / ticks
           for d in (20, 60)]
    print(f"{L}    {row[0]:8.1f}      {row[1]:8.1f}")
```

```
L    delay 20 ms   delay 60 ms   (ms per tick; 50 would be perfect)
1        72.4         111.0
2        51.7          58.8
3        50.8          51.4
4        50.5          50.7
6        50.3          50.3
8        50.3          50.3
```

Three or four ticks of lookahead bring the pair within 3% of a server running alone. Beyond that you gain nothing. The whole question becomes where those few ticks come from.

### Where lookahead comes from

Lookahead is not a setting. It is a property of the game's rules. It is the smallest delay, over every kind of interaction that crosses the border, between the tick where a cause happens and the tick where its effect must be applied on the other server. At 20 Hz a tick is 50 ms.

| Interaction crossing the border | Minimum cause-to-effect delay | Lookahead at 20 Hz |
|---|---|---|
| Instant melee or hitscan hit, applied next tick | 50 ms | 1 tick |
| Arrow at 50 m/s with a 5 m minimum range | 100 ms | 2 ticks |
| Walking at 7 m/s through a 7 m handoff band before any contact | 1 s | 20 ticks |
| Spell with a 1.5 s cast bar, landing time fixed when the cast starts | 1.5 s | 30 ticks |
| Trade window that needs both players to confirm | about 1 s or more | 20+ ticks |

The border's lookahead is the minimum of the column. **One instant, cross-border ability sets the lookahead of the whole border to 1.** A single designer adding "blink strike: teleport 30 m and hit instantly" can halve the tick rate of every border fight, as the 20 ms row showed.

The flip side is that designers can buy lookahead. A projectile with travel time, a cast bar, a wind-up animation, a minimum range. Each one is a delay players already accept for gameplay reasons, and each one is slack a distributed server can use. The one catch is anything that can cancel an effect. An interrupt that lands on the last tick of a cast is itself a cross-border event with a lookahead of 1, unless you rule that interrupts must arrive a few ticks before the cast completes.

Reading ghosts does not count against lookahead. When A draws B's entities for its own players, a ghost position that is 2 or 3 ticks old is invisible, because clients already draw the world about 100 ms in the past (CS202 week 10). Lookahead matters only for events that change the other server's state, such as damage, deaths, pickups and collisions.

### Move it yourself

Open `examples/w08-lookahead-timeline.html`. The top view is two horizontal timelines, one per server, with each tick drawn as a box whose width is its compute time and red gaps where the server stalls. Arrows show the border messages each tick waits for. The bottom view plots effective tick length against lookahead, with a dashed line at the average tick time. Start with the out-of-phase pattern at `L = 1`. Every other tick has a red gap on each row. Drag `L` to 2 and every gap closes. Then add 60 ms of delay and watch the gaps come back until `L` reaches 3. Switch the ability list to include "blink strike" and the lookahead slider locks to 1.

### Same idea elsewhere

**Age of Empires (Ensemble Studios, 1997; Bettner and Terrano, 2001).** Commands issued in turn `n` run in turn `n + 2`. In our form, each player is a logical process, the turn is the tick, and `L = 2`. CS202's `T_eff = max(T, (T + L_max) / k)` is our `max(X, (X + δ) / L)` with the scheduling depth `k` as the lookahead. Ensemble's measurement that players tolerated a steady 250 to 500 ms command delay in an RTS is a statement about how much lookahead the game's design can afford.

**HLA time management (IEEE 1516, 2000 onwards).** A time-regulating federate declares its lookahead to the RTI. The RTI grants each federate permission to advance to the least time at which a message could still arrive, which later versions call the greatest available logical time. For a fixed-step federate, the lookahead is usually the step size. That is our `L = 1`, the most common and most costly choice, because it is the one that needs no thought about the rules of the simulation.

**Chandy-Misra-Bryant null messages (1979).** In a network of logical processes, an LP with no real event to send still sends a **null message** carrying its clock plus its lookahead, a promise that nothing earlier will come. Without it, two idle LPs could each wait for the other forever. In our servers the null message is the "tick `k` done, nothing for you" packet, the same as the empty "turn done" message of a lockstep game in CS202 week 12. Game servers send it every tick for free because they send ghost updates anyway.

Three communities, one quantity. How far a process may run ahead of its neighbour is bounded by the smallest delay its neighbour promises, and the waiting it does is set by the ratio of message delay to that promise.

### Design judgment

- **Budget lookahead like bandwidth.** Decide the border's lookahead in the design document, list every interaction that crosses it, and check each against the budget. An instant long-range ability is a network cost, and it should be argued for like one.
- **Keep instant effects inside one server.** If a fast ability must exist, make its range smaller than the handoff band, so both ends of it are always owned by one server. Week 2's handoff band and this lecture's lookahead are the same margin viewed two ways.
- **Do not overpay.** The random run shows 3 or 4 ticks is enough at these delays. A 1.5 s cast bar gives 30 ticks, and the extra 26 buy nothing. Spend the slack on smaller ghost margins instead.
- **Remember the stall is shared.** In the model a slow tick on B delays A. With `L = 1` a server with a noisy neighbour inherits the neighbour's worst ticks. Lookahead is also isolation.

### Check this example

1. With `L = 1`, `δ = 0`, A's ticks take 30, 70, 30, 70 ms and B's take 70, 30, 70, 30 ms. What is the effective tick length? What is it at `L = 2`?
2. Two servers average 40 ms per tick and messages take 30 ms. Using `max(X, (X + δ) / L)`, what lookahead makes the pair run at its average tick? What tick rate does the pair reach at `L = 1`?
3. A designer adds a charge ability that sprints for 0.4 s and then hits, on a 20 Hz server whose other border interactions all allow 4 ticks. In version (a) the target and landing tick are fixed when the charge starts. In version (b) the hit is decided when the charge ends, against whoever is in front. What lookahead does each version allow, and what does each do to the border?

<details>
<summary>Answers</summary>

1. At `L = 1` each pair of ticks takes `70 + 70 = 140` ms, so 70 ms per tick, 40% slower than the 50 ms average. At `L = 2` neither server waits and the pair runs at 50 ms.
2. You need `(40 + 30) / L ≤ 40`, so `L ≥ 1.75`, and `L = 2` is enough. At `L = 1` the formula gives 70 ms per tick, about 14 Hz. Jitter adds a little on top.
3. In version (a) the effect is known 0.4 s, 8 ticks, before it lands, so the border keeps its lookahead of 4. In version (b) the effect is decided in the tick it lands, so its lookahead is 1 and the whole border drops to 1. Same animation, same feel, very different cost.

</details>

## 3. Optimistic simulation and rollback

Conservative synchronization waits for certainty. Jefferson's Time Warp, published as "Virtual Time" in 1985, does the opposite. Every logical process runs as fast as it can and keeps a history of its states. When a **straggler**, an event stamped earlier than the process's clock, arrives, the process rolls back to the straggler's time, restores that state, and simulates forward again. Any messages it sent during the undone ticks may now be wrong, so it sends **antimessages** that cancel them, and the receivers may roll back in turn. A background computation, **global virtual time** (GVT), finds the earliest time any process could still be rolled back to, and history older than GVT is thrown away.

You met the game version in CS202 week 12: fighting game rollback, where each player's machine predicts the other's input and re-simulates when the real input arrives. The cost structure is the same. Optimistic simulation never waits. It wastes the work it undoes, and it needs memory for history.

A rough cost model shows when each wins. Suppose that on a fraction `p` of ticks a straggler arrives from the other server, and each rollback undoes `D` ticks on average. The wasted share of work is about `p × D`. For a border where a cross-server hit happens on 2% of ticks and arrives 3 ticks late, rollback wastes about 6% of the server's time. The conservative server at `L = 1` and `δ = 20` from section 2 wasted 31% (72.4 ms per tick instead of 50). Rollback wins there. But rollback also re-sends the undone ticks' ghost updates, and in a 2,000-player battle where border hits happen every tick, `p` is near 1 and the server spends most of its time undoing work.

Optimistic simulation has a harder problem in games, which is output. A research simulator can hide undone work because nobody watches it live. A game server has already sent the undone ticks to clients. If A shows a player dying at tick 1,204 and then rolls back because B's heal was stamped tick 1,203, the client must undo a death animation it has already played. Fighting games accept this for two players and a few frames. An MMO would show it to hundreds of players at once. So shipped MMOs that speculate usually do it in a narrow way, for example by predicting movement ghosts and correcting them (harmless, as section 2 showed) while applying state-changing events conservatively.

## 4. What game research added

Two systems from Carnegie Mellon and Microsoft Research are the ones most cited by later MMO architecture work.

**Colyseus (Bharambe, Pang and Seshan, NSDI 2006).** Colyseus spreads a game's objects over many nodes. Each object has one **primary** copy on the node that runs its logic and read-only **replicas** on the nodes that need to see it. A node finds the objects it needs with **range queries**, "everything within this box," and **prefetches** replicas for objects its players are about to see. The authors built it into Quake II. In our terms, primary copies are authority, replicas are ghosts, range queries are interest management (MMO302 week 3), and prefetching is a way to widen the margin in time rather than space, a form of lookahead for the replica set.

**Donnybrook (Bharambe, Douceur, Lorch, Moscibroda, Pang, Seshan and Zhuang, SIGCOMM 2008).** Donnybrook asked how to run a fast shooter with far more players than the usual 16 to 32 without dedicated servers. It estimates which few players each player is paying attention to and sends those updates often, sending the rest rarely. It spreads updates with a multicast system designed for many sources and fast-changing groups. Built on Quake III, its simulations showed battles of up to 900 players. The attention estimate is the priority function of week 4 in another form, and the rarely sent updates are the low-detail updates of week 5.

Neither system became a product, but their parts did. Primary and replica copies, spatial range queries and attention-weighted update rates are all in current engines and in the server meshing designs of week 9.

## 5. What transferred and what did not

It helps to sort the research into what games adopted and what they rejected.

| Idea | Source | In shipped games? | Where you have seen it |
|---|---|---|---|
| Dead reckoning with an error threshold | SIMNET, DIS | Yes, everywhere | CS202 extrapolation |
| Each simulator owns its entities, others hold copies | SIMNET, Colyseus | Yes | Ghosts, week 2 handoff |
| Publish and subscribe by region | HLA, Colyseus range queries | Yes | Interest management, week 4 relevancy |
| Lookahead from scheduled commands | PDES, lockstep RTS | Yes, in RTS and some border rules | CS202 week 12 |
| Strict global timestamp order for all events | HLA time management, PDES | Rarely | Lockstep only |
| General optimistic rollback with antimessages | Time Warp | Narrowly (fighting games, prediction) | CS202 rollback |
| Attention-based update rates | Donnybrook | Yes | Week 4 priority |

The pattern is that games take the parts that cut bandwidth or CPU and reject the parts that guarantee exact ordering. Research simulators must produce the same answer every run, because their output is the point. A game must feel fair and stay responsive, and it can tolerate two players seeing slightly different orders of events a few milliseconds apart, as long as nobody can see the difference and the final state agrees. Week 10 turns that tolerance into named consistency models. This week's lookahead tells you what the strict option costs, so you can decide when to pay it.

## In-class activity (25 minutes)

Groups of three. Each group gets an ability list for one class in a seamless-world MMO: a warrior (charge, cleave, taunt, shield wall), a mage (fireball with a 2 s cast, blink 15 m, frost nova, polymorph with a 1.5 s cast) or a ranger (arrow at 60 m/s, trap, pet attack, disengage leap 12 m).

1. For each ability, state the minimum cause-to-effect delay if it crosses a server border, and the lookahead in ticks at 20 Hz.
2. Find the ability that sets the class's lookahead. Propose one change to it that raises the lookahead to at least 3 ticks without changing how it feels in play. Name the cost in feel, if any.
3. With a 25 ms message delay and 45 ms average ticks, compute the effective tick length before and after your change using `max(X, (X + δ) / L)`. Check it with the interactive.
4. Say whether your changed ability should be conservative or optimistic at the border, and why.

Expected output: an ability table with delays and lookaheads, the one change and its cost, the two tick lengths, and a one-line synchronization choice. Groups with different classes then combine their tables to find the border's lookahead for a mixed party.

## Common misconceptions

- **"Servers in one data centre have no latency, so they can run in lockstep for free."** A few milliseconds of message delay per tick at `L = 1` turned 50 ms ticks into 80 ms ticks in section 2. At `L = 1` delay adds directly to every tick.
- **"Lookahead is a configuration value."** It is set by the fastest cross-border interaction in the game's rules. Setting a larger number than the rules allow produces causality errors, not speed.
- **"Optimistic synchronization is always faster because it never waits."** It trades waiting for undone work, and in a game the undone work may already be on players' screens.
- **"Research systems failed, so the research does not matter."** Almost every technique in current MMO netcode, from dead reckoning to range-query interest management, comes from these systems.

## Check yourself

1. Two servers each take 50 ms per tick with no jitter. Message delay is 40 ms. Compute the effective tick length at `L = 1`, 2 and 3.
2. A server finishes tick 99 at 4,950 ms. Its neighbour finished tick 98 at 4,940 ms. Message delay is 20 ms, lookahead is 2, and the server's tick 100 takes 55 ms. When does it finish tick 100? Did it stall, and by how much?
3. A border sees a cross-server state change on 10% of ticks, and a rollback undoes 4 ticks on average. What share of work does optimistic synchronization waste? Compare with the conservative `L = 1`, `δ = 20` result from section 2, and say which you would choose and one more thing you would want to know.
4. Map Colyseus's primary, replica and range query onto the terms of MMO302 week 4.

<details>
<summary>Answers</summary>

1. With no jitter, `max(50, (50 + 40) / L)`. `L = 1` gives 90 ms. `L = 2` gives 50 ms, since 45 is below 50. `L = 3` gives 50 ms.
2. Tick 100 needs the neighbour's tick `100 − 2 = 98`, whose message arrives at `4,940 + 20 = 4,960` ms. That is later than 4,950, so the server stalls for 10 ms and finishes tick 100 at `4,960 + 55 = 5,015` ms.
3. About `0.10 × 4 = 40%` wasted, against 31% for the conservative server. Conservative wins here. You would also want to know whether rolled-back ticks were already sent to clients, and how much memory the history needs.
4. Primary copy is the authoritative entity on its owning zone server. Replica is the ghost on the neighbouring server. The range query is the interest test that decides which ghosts a server holds, the border band in MMO302 week 4.

</details>

## Lab / assignment hook

[Lab 08, lookahead on the border](../labs/lab08.md). You implement the finish-time model, a stall counter and a border-lookahead calculator, reproduce this lecture's tables, find the smallest lookahead that keeps a pair of servers within 5% of their average tick for several delays, and compute the lookahead of an ability list. Deliverable: your `lookahead.py`, a table of smallest lookahead against delay, and a one-page border rule for the in-class class you were given.

## Sources

- Wikipedia, "Distributed Interactive Simulation" (maintained article, accessed September 2026). SIMNET developed by BBN for DARPA from the early to the late 1980s; BBN introduced dead reckoning for battlefield entities; IEEE 1278, drafts from 1992-1993, current IEEE 1278.1-2012; succeeded by HLA.
- Wikipedia, "High-level architecture" (maintained article, accessed September 2026). IEEE 1516-2000, 1516-2010 (HLA Evolved) and 1516-2025; lookahead as the interval below which a federate will not send messages; for fixed-step federates the lookahead usually equals the step; greatest available logical time (GALT).
- Chandy, K. M. and Misra, J. "Distributed Simulation: A Case Study in Design and Verification of Distributed Programs." *IEEE Transactions on Software Engineering* SE-5(5), 440-452, September 1979.
- Bryant, R. E. "Simulation of Packet Communication Architecture Computer Systems." MIT Laboratory for Computer Science, technical report MIT-LCS-TR-188, November 1977 (MIT DSpace handle 1721.1/149478). The independent conservative algorithm.
- Su, W.-K. and Seitz, C. L. "Variants of the Chandy-Misra-Bryant Distributed Discrete-Event Simulation Algorithm" (Caltech technical report CS-TR-88-22, 1988, DTIC ADA447721). Source for the algorithm's three-author name.
- Jefferson, D. R. "Virtual Time." *ACM Transactions on Programming Languages and Systems* 7(3), 404-425, July 1985.
- Fujimoto, R. M. "Parallel Discrete Event Simulation." *Proceedings of the 1989 Winter Simulation Conference*, 19-28.
- Bharambe, A., Pang, J. and Seshan, S. "Colyseus: A Distributed Architecture for Online Multiplayer Games." *3rd USENIX Symposium on Networked Systems Design and Implementation (NSDI '06)*, May 2006. Primary and replica objects, range queries, prefetching, evaluated on Quake II.
- Bharambe, A., Douceur, J. R., Lorch, J. R., Moscibroda, T., Pang, J., Seshan, S. and Zhuang, X. "Donnybrook: Enabling Large-Scale, High-Speed, Peer-to-Peer Games." *ACM SIGCOMM 2008*, 389-400. Usual limit of 16-32 players; attention-based update rates; multicast for games; Quake III prototype; simulated battles of up to 900 players.
- Bettner, P. and Terrano, M. "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (Gamasutra, March 2001), as summarized and cited in CS202 week 12. Commands scheduled two turns ahead; latency tolerance figures.

## Interactive spec: examples/w08-lookahead-timeline.html

**Insight the visual must make obvious:** with a lookahead of one tick, every millisecond of message delay and every slow tick on one server is added to both servers' ticks. Two or three ticks of lookahead make the stalls disappear, and one instant cross-border ability takes that slack away.

**Layout.** Top: two-row timeline. Bottom left: effective tick length against lookahead. Bottom right: ability list. Controls in a panel under the timeline on mobile, beside it on desktop (width over 900 px).

**Model (must match section 2 code exactly).**
- `F_A(k) = max(F_A(k−1), F_B(k−L) + δ) + X_A(k)`, symmetric for B, with `F(k) = 0` for `k ≤ 0` and the second term dropped when `k − L < 1`.
- Tick patterns: "Out of phase" (A: 40, 60 repeating; B: 60, 40 repeating), "Random" (both from `mulberry32(seed)`, one draw per tick, A's 10,000 draws first, then B's, `X = lo + (hi − lo) r`, defaults lo 30, hi 70, seed 404), "Custom" (two text fields of comma-separated ms).
- Effective tick length: `max(F_A(N), F_B(N)) / N`, `N = 100` for patterns, 10,000 for random.

**Timeline view.** Show ticks 1 to 12 (scrollable to 40). Each tick is a box from its start to its finish, labelled with its tick number. Stalls (start minus own previous finish, if positive) drawn as red hatched gaps with the stall in ms. For each tick, a thin arrow from the neighbour's tick `k − L` finish, offset by `δ`, to this tick's start; draw it solid when it is the binding term of the `max`, faint when not.

**Chart view.** x axis lookahead 1 to 8, y axis ms per tick (40 to 120). Two lines, current delay and delay 0, with a dashed line at the mean tick. Current `L` marked with a dot and the value printed.

**Ability list.** Checkboxes: "Melee hit, next tick (1)", "Arrow, 5 m minimum range at 50 m/s (2)", "Handoff band walk (20)", "1.5 s cast (30)", "Blink strike, instant (1)". Border lookahead = minimum over checked items, at 20 Hz. When "lock L to abilities" is on, the `L` slider is set to that minimum and disabled, with the text "Lookahead set by: <ability>".

**Controls (keyboard accessible, live value labels).** `L` slider 1 to 8, default 1. Delay `δ` slider 0 to 100 ms, step 5, default 0. Pattern selector. Seed input. Lock toggle, default off.

**Number panel.** Effective tick length, equivalent tick rate in Hz, total stall ms per server over the run, the estimate `max(X̄, (X̄ + δ) / L)` beside the measured value.

**Test values.**
- Out of phase, `L = 1`, `δ = 0`: A finishes 40, 120, 160, 240; B 60, 100, 180, 220; 60.0 ms per tick.
- Out of phase, `L = 2`, `δ = 0`: A 40, 100, 140, 200; B 60, 100, 160, 200; 50.0 ms.
- Out of phase, `L = 1`, `δ = 20`: 79.8 ms. `L = 2`, `δ = 20`: 50.0 ms. `L = 2`, `δ = 60`: 55.0 ms, A's tick 3 finishes at 160.
- Random, seed 404, delay 20: `L` 1 to 4 give 72.4, 51.7, 50.8, 50.5 ms. Delay 60: 111.0, 58.8, 51.4, 50.7 ms.

**First screen.** Out of phase, `L = 1`, `δ = 20`, so red gaps appear on every other tick of both rows. Caption: "Neither server is slow on average. Both run at 80 ms." Next to it a button "Give them 2 ticks of lookahead."
