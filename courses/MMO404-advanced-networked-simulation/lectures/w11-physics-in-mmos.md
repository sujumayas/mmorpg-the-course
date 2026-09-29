# MMO404 · Week 11 — Physics in MMOs

**Why this matters:** Physics is the feature players ask for and servers cannot afford. A zone full of barrels you can kick, walls you can breach and carts you can push sounds like a few more objects to simulate, until a siege wakes all of them at once. This week you learn to price server physics by what is moving rather than by what exists, to decide who owns each body, and to keep a pile of crates from being split across two servers.

**You will be able to:**
- Compute the number of awake bodies and the physics CPU cost of a zone from its disturbance rate and sleep rules, using Little's law.
- Explain why a sleep timer is a budget setting, and predict how changing it moves the cost of a siege.
- Choose between server-authoritative, client-owned and predicted physics for each kind of object, and name the cheat or artifact each choice invites.
- Design an ownership rule for physics islands that cross a server seam, and implement it with union-find.

**Before class:** Epic Games, "Networked Physics Overview" (Unreal Engine 5.8 documentation), the section on replication modes. Roblox, "Network ownership" (Roblox Creator Documentation), the whole page. Skim `b2_island.cpp` in Box2D v2.4.1 (GitHub `erincatto/box2d`, tag `v2.4.1`), the end of `b2Island::Solve`, where bodies go to sleep.

**Prerequisites from earlier courses:** [MMO404 week 1](w01-limits-of-the-zone-model.md) (the tick budget and cost that follows density), [week 2](w02-seamless-worlds-and-boundary-handoff.md) (owners and seams), [week 5](w05-bandwidth-shaping-and-lod-for-networking.md) (error-driven updates and dormancy) and [week 10](w10-consistency-models.md) (guess or forward). MA201 weeks 7, 9, 10 and 14 on integration, collision detection, impulses and determinism ([MA201 syllabus](../../MA201-linear-algebra-and-physics-for-games/syllabus.md)). [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md). [MMO302 week 6, simulation authority](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md).

**Interactive:** [w11-sleeping-bodies.html](../examples/w11-sleeping-bodies.html). Keep it open during section 2.

---

## 1. Why most MMOs have so little physics

Walk through almost any MMO and push against a barrel. It will not move. That is not because the developers could not make it move. It is because a moving barrel on an MMO server has three costs that a barrel in a single-player game does not.

- **CPU.** A physics engine advances every moving body by one **step** (one integration and collision pass, MA201 week 7) many times a second. The server pays for every body in every zone, not only the ones one player can see.
- **Bandwidth.** A barrel that moves on the server must be replicated to every client that can see it. Week 5 showed that a moving entity costs bytes and a still one costs almost nothing.
- **Authority.** If the barrel matters to gameplay (it blocks a door, it hides a player, it rolls onto someone), then the server must decide where it is, and the client's copy is a guess that can be wrong (week 10).

So MMO developers split the world's objects into kinds, and the split decides the cost.

- A **static** body never moves: terrain, buildings, trees. It takes part in collision tests but is never stepped.
- A **kinematic** body moves because code says so, not because of forces: player characters, doors on a script, a moving platform. Most MMO characters are kinematic. Their movement code checks collisions but does not simulate momentum or impacts.
- A **dynamic** body is moved by the physics engine through forces and impulses (MA201 week 10): a kicked barrel, falling debris, a pushed cart. This is the expensive kind, and the subject of this lecture.

A dynamic body that has stopped moving can be put to **sleep**. The engine stops stepping it until something touches it or a force is applied, which **wakes** it. Bodies that touch each other form an **island**, a group the solver must handle together because a push on one moves the others. Sleep and islands together decide how much of a zone's physics the server actually runs.

## 2. Worked example: 20,000 crates and one siege

### The hook

EVE Online resolves almost everything in space on a server tick of one second, according to the EVE University wiki. Rocket League simulates its physics at 120 steps per second, which is the ceiling the RLBot project documents for how often a bot can act. Roblox, by default, hands the simulation of loose parts near a player to that player's own machine and lets the server skip them.

That is a range of 120 times in step rate, plus one game that moves the work off the server entirely. All three shipped and are known for their physics, good or bad. They made different choices because they have different numbers of bodies, and more importantly different numbers of *moving* bodies. Here is a zone designed with the physics players ask for: 20,000 loose props (crates, barrels, fence planks, market stalls). On a quiet evening it runs fine. On siege night the server falls over. Why, and what do you change?

### The model

Every awake body costs the same per step. Call it `c_b`, including its share of collision tests and contact solving. With `f` steps per second, the physics CPU cost per second is

```
C = f × c_b × N_awake
```

Everything interesting is in `N_awake`, the number of bodies awake at a given moment. Bodies wake when something disturbs them (a player walks into one, an explosion throws it, a cart hits it). Let the **disturbance rate** `δ` be the number of wake-ups per second across the zone. After a disturbance, a body moves for a while, `t_move`, and then must stay still for the **sleep timer** `t_sleep` before the engine lets it sleep. So each wake-up keeps one body awake for

```
τ = t_move + t_sleep
```

Now use **Little's law**, from queueing theory: the average number of items in a system equals their arrival rate times the average time each one stays. Wake-ups arrive at `δ` per second and each stays awake for `τ`, so

```
N_awake = δ × τ           (capped at N, the total number of bodies)
```

The cost of the zone is set by how often things get pushed and how long they take to settle. The number of props in the zone does not appear at all until nearly all of them are awake.

We use `c_b = 4 µs` per awake body per step, `f = 30` steps per second and `t_sleep = 0.5 s`. The constants are teaching values of a realistic size. The server gives physics 20% of one core, a budget of 200 ms of CPU per second.

### Numbers you can check

The zone holds `N = 20,000` props. Players bump into things on an ordinary evening. On market day the square is packed. On siege night, catapults land 10 explosions a second, each throwing 40 props for about 3 seconds.

| Scenario | Wake-ups `δ` per s | `t_move` | `τ` | Awake `N_awake` | CPU `C` | Share of 200 ms/s budget |
|---|---|---|---|---|---|---|
| Nothing sleeps | — | — | — | 20,000 | 2,400 ms/s | 1,200% |
| Quiet evening | 30 | 1.5 s | 2.0 s | 60 | 7.2 ms/s | 3.6% |
| Market day | 150 | 1.5 s | 2.0 s | 300 | 36.0 ms/s | 18% |
| Siege | 430 | 3.0 s | 3.5 s | 1,505 | 180.6 ms/s | 90% |
| Siege, sleep timer 2 s | 430 | 3.0 s | 5.0 s | 2,150 | 258.0 ms/s | 129% |

Check two rows by hand. On market day, `N_awake = 150 × 2.0 = 300`, and `C = 30 × 4 µs × 300 = 36,000 µs = 36 ms` per second. In the siege, `δ = 10 × 40 + 30 = 430`, `N_awake = 430 × 3.5 = 1,505`, and `C = 30 × 4 µs × 1,505 = 180.6 ms` per second.

Three things stand out.

- **The zone is affordable only because things sleep.** Without sleeping, the same 20,000 props would need 2.4 cores. With it, a quiet evening costs 0.7% of one core. The props are free while nobody touches them.
- **The siege is 25 times the quiet evening, with the same props.** Cost follows activity, just as week 1's tick cost followed density rather than headcount. Plan for the siege, because that is the night your players will remember.
- **The sleep timer is a budget knob.** Raising `t_sleep` from 0.5 s to 2 s (to stop piles from twitching when they fall asleep too early) adds 1.5 s to every wake-up. It costs almost nothing on a quiet evening, 12.6 against 7.2 ms/s, and pushes the siege 29% over budget.

Is Little's law honest here? The simulation below pushes random bodies at Poisson rate `δ` and counts how many are awake.

```python
import math, random

N = 20_000                     # physics props in the zone
C_B, F = 4e-6, 30              # CPU seconds per awake body per step, steps per second

def awake_model(delta, tau, n=N):
    return min(n, delta * tau)                     # Little's law, capped at every body

def cpu_ms_per_s(n_awake):
    return 1000 * C_B * F * n_awake

def awake_measured(delta, tau, n=N, seconds=120, seed=11):
    """Push a random body at Poisson rate delta; it stays awake tau after its last push."""
    rng = random.Random(seed)
    wake_until = [0.0] * n
    t, samples, total = 0.0, 0, 0
    next_sample = 20.0                             # skip the first 20 s of warm-up
    while t < seconds:
        t += rng.expovariate(delta)
        while next_sample < t:
            total += sum(1 for u in wake_until if u > next_sample)
            samples += 1
            next_sample += 0.5
        wake_until[rng.randrange(n)] = t + tau
    return total / samples

print(f"no sleeping: {cpu_ms_per_s(N):,.0f} ms/s")
for name, delta, t_move in (("quiet evening", 30, 1.5), ("market day", 150, 1.5), ("siege", 430, 3.0)):
    tau = t_move + 0.5
    a = awake_model(delta, tau)
    print(f"{name:13}  awake: model {a:5.0f}, measured {awake_measured(delta, tau):5.0f}"
          f"  cpu {cpu_ms_per_s(a):6.1f} ms/s")
```

It prints `no sleeping: 2,400 ms/s`, then model and measured counts of 60 and 58, 300 and 300, and 1,505 and 1,464. The siege is the only row with a visible gap, and it has a clear cause. When 7% of props are awake, some wake-ups hit a body that is already awake and only extend its time instead of adding a new one. The exact form for random pushes is `N × (1 − e^(−δτ/N))`, which gives 1,450 for the siege. Little's law is an upper bound that is tight while few bodies are awake, which is exactly the safe direction for a budget.

### Move it yourself

Open `examples/w11-sleeping-bodies.html`. The left view is the zone from above, with 20,000 props drawn as faint dots and awake ones drawn bright. The right view is a bar of physics CPU against the 200 ms/s budget line, with the awake count beside it. It opens on the siege, with bright patches where explosions land and the bar at 90% of the budget. Switch to the quiet evening. The map goes dark except for a few sparks, and the bar shrinks to a sliver, while the total number of dots never changes. Switch back to the siege. Then drag the sleep timer from 0.5 s to 2 s. The map looks nearly the same, a slightly wider glow around each blast. The bar crosses the budget line. Finally toggle "no sleeping" to see why every engine ships with sleep turned on.

### Same idea elsewhere

Every physics budget below changes one letter of `C = f × c_b × δ × τ`. Naming the letter is the skill.

**Box2D (v2.4.1).** Box2D is open source, so you can read its rule. A body is a candidate for sleep once its speed stays under 0.01 m/s and its turning rate under 2 degrees per second, and it must stay under both for `b2_timeToSleep`, which is 0.5 s. That constant is our `t_sleep`. The island solver then puts a whole island to sleep only when every body in it has been still for that long. In our form, the second rule means a pile's `τ` is set by its most restless body.

**NVIDIA PhysX (5.x documentation).** PhysX expresses the same idea as a **wake counter**. Each step in which an actor's mass-normalized kinetic energy is below a threshold counts the wake counter down, and a disturbance resets it. When it reaches zero with no velocity and no pending force, the actor sleeps. The threshold sets when `t_move` ends. The counter's reset value is `t_sleep`. Both are per-actor settings, so a designer can make debris sleep quickly and a precariously balanced sculpture sleep slowly.

**EVE Online (current mechanics).** EVE lowers `f`. The server resolves ship movement, module activations and damage on a one-second tick, so its step rate is 1 where ours is 30. That divides `C` by 30 before anything else happens, which is part of how one node can handle thousands of ships (MMO302 week 12). The price is precision. EVE University notes that actions are rounded up to the next full second, so no player can act faster than the tick.

**Rocket League (Psyonix, current).** Rocket League goes the other way. Its physics runs at 120 steps per second, four times our 30, but its arena holds a ball and at most eight cars (4v4 modes), six in the standard 3v3. Take seven bodies, a ball and six cars, all always awake: `f × N_awake = 120 × 7 = 840` body-steps per second. Our quiet evening costs `30 × 60 = 1,800`, and the siege `30 × 1,505 = 45,150`. A competitive physics game spends its budget on step rate for a handful of bodies. An MMO spends it on bodies and must keep `f` low.

**Roblox (current).** Roblox changes who pays `c_b`. The engine gives ownership of loose parts near a player's character to that player's client, which simulates them and sends the results. For those parts the server's `c_b` is close to zero. Roblox's own documentation states the price. The server cannot verify physics from a client that owns a part, so an exploiter can teleport it or push it through walls, and games must check any gameplay event that client-owned physics produces.

Five systems, one formula. When you meet a new game's physics, ask whether it cuts the step rate, the cost per body, the disturbances, the time to settle, or moves the work to someone else's machine.

### Design judgment

- **Decide which objects are dynamic at all.** A market stall that could fall over is a cost every siege night for the life of the game. Make it dynamic only if falling over changes play. Otherwise make it static and give it a canned destruction animation.
- **Separate gameplay physics from cosmetic physics.** Debris that nobody can stand on or hide behind can be simulated on each client independently, never sent over the network and never checked. Different clients will see different debris, and that is fine. Only bodies that affect gameplay need the server.
- **Budget the worst night, then cap it.** Size `f`, `c_b` and `t_sleep` against the siege, not the evening. Then add a hard ceiling: when `N_awake` passes a limit, lower the step rate of the least relevant islands (week 4's priority, applied to physics) or despawn the smallest debris early.
- **Tune sleep with the budget in view.** A long sleep timer hides twitchy piles. A short one saves CPU and may make stacks freeze in odd poses. Pick it by measuring both, and set it per object type where the engine allows.
- **Remember the bytes.** Every awake body is also an error-driven update stream (week 5). The siege's 1,505 awake props cost bandwidth to every client in view as well as CPU. Sleeping bodies send a final resting state and then nothing.

### Check this example

1. A zone has 5,000 dynamic props, `f = 60`, `c_b = 3 µs` and `t_sleep = 0.5 s`. Players cause 80 wake-ups per second, each with `t_move = 1 s`. What is the physics cost in ms per second?
2. In the siege, the design team wants the physics to fit in the 200 ms/s budget with `t_sleep = 2 s`. How far must they cut the step rate?
3. A designer doubles the number of props in the market square from 20,000 to 40,000 without changing how often players or catapults push things. What happens to `C` on market day?

<details>
<summary>Answers</summary>

1. `τ = 1.5 s`, so `N_awake = 80 × 1.5 = 120`. `C = 60 × 3 µs × 120 = 21,600 µs = 21.6 ms` per second.
2. With `t_sleep = 2 s`, `N_awake = 2,150`. Solve `f × 4 µs × 2,150 ≤ 200 ms`, so `f ≤ 200,000 / 8,600 ≈ 23` steps per second. Down from 30, that is about a 23% cut.
3. Nothing, to first order. `N` does not appear in `δ × τ`. In practice, a denser square means each push is more likely to hit a neighbour, which raises `δ` and makes islands bigger, so measure it. The formula says the count of props is not the cost.

</details>

## 3. Who owns a body?

Week 10 asked whether a copy should wait for the truth or guess. Physics asks the same question 30 times a second for every awake body, and there are three standard answers.

### Server-authoritative

The server simulates the body. Clients receive its state and interpolate (CS202 week 10). This is the only choice that is safe against cheating, and it is the one all the numbers in section 2 assume. Its weakness is interaction. When a player pushes a crate, the client must wait a round trip to see it move, or predict the push and risk a correction. For a crate, a 100 ms delay before it slides is acceptable. For a ball in a sports game, it is not.

### Client-owned

The server hands the body to one client, usually the nearest player, which simulates it and reports the result. The server's CPU cost for that body drops to near zero and the owning player sees no delay at all. Roblox does this automatically and lets developers override it. The price is trust. The owner's machine is the authority, so a modified client can put the body anywhere. The rule for client-owned physics follows directly: never let a client-owned body produce a gameplay result that the server does not check. A client-owned crate can be pushed. A client-owned crate should not be able to kill another player without the server checking the hit.

### Predicted with resimulation

The client runs the physics itself, ahead of the server, and the server also runs it authoritatively. When the server's state arrives, the client compares it with what it predicted for that moment. If they differ, the client rewinds to the server's state and replays its inputs forward, the same idea as server reconciliation in CS202 week 9. Unreal Engine 5.8 offers exactly this as its **resimulation** replication mode, in which the client runs about half a round-trip time ahead of the server. Its other two modes are the older **default** mode, which nudges each client object's velocity toward the server's, and **predictive interpolation**, which lets the client change a server-owned object locally as long as it does so predictively.

Resimulation gives the best feel and costs the most. The client runs physics for every predicted body, and every correction runs several steps again. It also depends on the client's simulation matching the server's closely, because every small difference becomes a correction. That brings back the determinism problem from MA201 week 14 and CS202 week 12. You do not need bit-for-bit determinism, since corrections repair drift, but a client that disagrees often will stutter.

### Choosing per object

| Kind of object | Recommended owner | Why |
|---|---|---|
| Loot that has value, siege rams, anything that deals damage | Server | Gameplay results must be trusted |
| A crate a player is pushing, a vehicle they drive | Predicted (or client-owned with server checks) | Needs instant response; results can be validated |
| Debris, ragdolls, cloth, leaves | Each client, not replicated | Cosmetic; nobody needs to agree |
| Terrain, buildings | Static | Never steps |

The same zone usually uses all four rows at once.

## 4. Physics across a seam

Weeks 2 and 9 gave every entity one owner ([week 9, server meshing concepts](w09-server-meshing-concepts.md)). Physics adds a rule that ownership must respect. **Bodies that touch must be solved together.** A stack of three crates is one problem, not three, because the solver needs the forces between them. If crate 1 is on server A and crate 3 on server B, neither server can solve the stack alone.

The unit of physics ownership is therefore the island, not the body. An island is a connected component of the contact graph, with bodies as nodes and contacts as edges. You met connected components as reachability in [CS102 week 8](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md). Physics engines find them with a faster structure, **union-find** (also called a disjoint set). Every body points to a parent, and following parents leads to its set's **root**. Start with each body as its own root. For every contacting pair, find both roots and point one at the other, which merges the two sets. At the end, bodies with the same root form one island. The engine already does this each step, because islands are also what it puts to sleep.

For a seam, pick one owner per island. A simple rule is that the server owning most of the island's bodies takes all of them, with ties going to a fixed server so that both sides agree without talking.

```python
from collections import Counter

def islands(bodies, contacts):
    """Group bodies that touch, directly or through a chain of contacts (union-find)."""
    parent = {b: b for b in bodies}
    def root(b):
        while parent[b] != b:
            parent[b] = parent[parent[b]]          # path halving keeps the trees shallow
            b = parent[b]
        return b
    for a, b in contacts:
        parent[root(a)] = root(b)
    groups = {}
    for b in bodies:
        groups.setdefault(root(b), []).append(b)
    return sorted(sorted(g) for g in groups.values())

owner = {"c1": "A", "c2": "A", "c3": "B", "c4": "B", "c5": "B", "c6": "A"}
contacts = [("c1", "c2"), ("c2", "c3"), ("c4", "c5")]      # c1-c2-c3 is a stack across the seam
for group in islands(owner, contacts):
    votes = Counter(owner[b] for b in group)
    winner = max(sorted(votes), key=votes.get)              # most bodies wins, ties go to A
    print(group, "->", winner, dict(votes))
```

It prints three lines. The stack `['c1', 'c2', 'c3']` goes to A, which owns two of its three crates. The pair `['c4', 'c5']` stays on B, and the lone `['c6']` stays on A. Crate `c3` changes owner from B to A for as long as it touches the stack.

Three consequences follow, and each links back to an earlier week.

- **Island merges are handoffs.** When `c3` joins the stack, B must hand it to A with week 2's protocol. A crate bouncing on and off a pile at the seam would hand off many times a second, so use week 2's hysteresis. Keep an island together until it has been apart for a few hundred milliseconds.
- **One restless body keeps a whole island awake.** Box2D sleeps an island only when all its bodies have been still for 0.5 s. A seam-crossing pile that one player keeps poking stays awake, and stays on one server, for as long as they poke it.
- **Big islands defeat load balancing.** A chain of carts coupled together across a zone is one island and must be on one server. If players build long connected structures, week 3's movable boundaries cannot split the load. Many games limit how many bodies can be joined for this reason. The islands a design allows to form matter as much as the number of bodies.

## In-class activity (25 minutes)

In pairs, you are the physics lead for a castle siege mode. The castle zone has 8,000 dynamic props, 400 wall segments that can break into 6 pieces each, and 200 players. Catapults fire 4 shots a second. Each shot wakes 30 props and breaks one wall segment.

1. Compute `δ` and `N_awake` for the siege, assuming `t_move = 3 s` for props and pieces and `t_sleep = 0.5 s`. (5 min)
2. With `c_b = 4 µs`, find the largest step rate `f` that fits a 200 ms/s budget. Is it playable? (5 min)
3. Assign an owner (server, predicted, client-only cosmetic) to props, wall pieces, catapult stones and battering rams. Justify each in one sentence. (10 min)
4. Recompute `C` after your assignment, counting only the server's bodies. (5 min)

Expected output: `δ = 4 × (30 + 6) = 144` per second and `N_awake = 504`, a step rate of up to about 99, a four-row ownership table, and the server's cost after cosmetic pieces leave it.

## Common misconceptions

- **"More objects means more physics cost."** More moving objects does. A zone of 20,000 sleeping props costs almost nothing. What you pay for is `δ × τ`.
- **"Sleeping is an optimisation you can add later."** It is a budget setting. Change `t_sleep` and the siege goes from 90% to 129% of budget. Decide it early and test it under load.
- **"Client-owned physics is free."** It is free in server CPU and expensive in trust. Roblox's documentation spells out that the server cannot verify a client's physics.
- **"Physics must be deterministic to network it."** Only lockstep needs bit-for-bit determinism. Server-authoritative physics needs none, and predicted physics tolerates small drift because corrections repair it, at the cost of visible snaps when drift is large.

## Check yourself

1. A zone runs physics at 20 Hz with `c_b = 5 µs`. On a raid night, 300 wake-ups per second each keep a body awake for 2.5 s. What is `C`, and what share of one core is it?
2. Using the exact form `N × (1 − e^(−δτ/N))`, how many bodies are awake in the siege from section 2 if the zone had only 2,000 props instead of 20,000? Compare with Little's law.
3. A stack of four crates sits on the seam. Three belong to server A and one to server B. Another crate owned by B slides into the stack. Using the majority rule from section 4, who owns the island? What must happen to B's crates?
4. Your team proposes moving all prop physics to clients with Roblox-style ownership. Name one gameplay feature this makes unsafe and one server check that would make it safe again.

<details>
<summary>Answers</summary>

1. `N_awake = 300 × 2.5 = 750`. `C = 20 × 5 µs × 750 = 75,000 µs = 75 ms` per second, 7.5% of one core.
2. `δτ = 1,505`, so `N × (1 − e^(−1,505 / 2,000)) = 2,000 × (1 − e^(−0.7525)) = 2,000 × 0.529 ≈ 1,058`. Little's law says 1,505, which is too high because most wake-ups now land on bodies that are already awake. When a large share of the zone is awake, use the exact form.
3. The island now has five crates, three from A and two from B, so A owns it. B must hand both of its crates to A with the week 2 handoff protocol. Hysteresis should keep them with A until each has been apart from the stack for a while.
4. Crushing or blocking damage from props, for example a boulder rolled onto enemies. The server should recompute any damage event from its own coarse check (was the prop plausibly there, moving that fast) before applying it, or keep damage-dealing props server-owned.

</details>

## Lab / assignment hook

[Lab 11, physics budget](../labs/lab11.md). You implement a sleep rule on a small 2D physics world, measure awake bodies against Little's law and its exact form, find islands with union-find and assign them to servers across a seam, and write a physics budget for a siege mode.

## Sources

- EVE University Wiki, "Server tick" (current mechanics). The server tick runs once per second; locking and activation times are rounded up to the full second; damage and module activation are resolved on the tick.
- RLBot Wiki, "Tick Rate" (GitHub `RLBot/RLBot` wiki, accessed September 2026). A bot's tick rate cannot exceed 120 because that is the rate at which Rocket League simulates its physics. Community documentation, not an official Psyonix source.
- Cone, J. (2018). "It IS Rocket Science! The Physics of Rocket League Detailed." GDC 2018, GDC Vault. Background on Rocket League's networked physics.
- Wikipedia, "Rocket League" (maintained article, accessed September 2026, citing GameSpot). Match sizes from 1v1 to 4v4; standard competitive play is 3v3.
- Roblox Creator Documentation, "Network ownership" (accessed September 2026). Automatic ownership of parts near a player's character; `SetNetworkOwner`; anchored parts stay with the server; the server cannot verify physics from a client that owns a part.
- Box2D v2.4.1 (Catto, E., GitHub `erincatto/box2d`, tag `v2.4.1`), `include/box2d/b2_common.h` and `src/dynamics/b2_island.cpp`. `b2_timeToSleep = 0.5 s`, linear sleep tolerance 0.01 m/s, angular tolerance 2 degrees per second; an island sleeps when every body's sleep time reaches `b2_timeToSleep`.
- NVIDIA, *PhysX SDK 5.4.1 Documentation*, "Rigid Body Dynamics", section on sleeping. Wake counter decremented while kinetic energy is below the sleep threshold; conditions for an actor to be asleep.
- Epic Games, "Networked Physics Overview" (Unreal Engine 5.8 documentation). Default, predictive interpolation and resimulation replication modes; resimulation runs the client about half a round trip ahead of the server and rewinds on correction.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research* 9(3), 383-387.

## Interactive spec: examples/w11-sleeping-bodies.html

**The one insight:** a zone's physics cost follows how often things are pushed and how long they take to settle, not how many things exist. The same 20,000 props cost 7 ms/s on a quiet evening and 181 ms/s in a siege, and one slider, the sleep timer, can push the siege over budget without visibly changing the map.

**Layout.** Two linked views and a numbers panel. Desktop: map on the left (55%), bar and curve on the right. Under 700 px: map, bar, curve, panel.

- **Left, the zone map.** A square zone drawn with `N` props as 1-pixel faint dots, positions from a seeded PRNG (mulberry32, seed 11). For performance, draw at most 20,000 dots on a canvas. Run a live simulation of wake-ups: disturbances arrive as a Poisson process at rate `δ` (scaled by the "speed" of the animation, real time by default). In the quiet and market scenarios, each disturbance wakes one random prop. In the siege scenario, 10 explosions per second each wake the 40 props nearest a random point, plus 30 random single wake-ups per second. An awake prop is drawn bright for its `τ` seconds, then fades back to faint. A counter above the map shows the live awake count.
- **Right top, the budget bar.** One horizontal bar of physics CPU in ms/s from the model `C = f × c_b × N_awake` with `N_awake = min(N, δτ)`, and a thin marker for the live measured count from the map. Vertical line at the budget (default 200 ms/s). Axis to max(300, 1.1 × C) ms/s, with a break label when "no sleeping" makes it 2,400.
- **Right bottom, a small line chart** of `C` against `t_sleep` from 0 to 3 s for the current scenario, with the budget line and a marker at the current `t_sleep`.
- **Numbers panel.** `δ`, `τ`, `N_awake` by Little's law, `N_awake` by the exact form `N(1 − e^(−δτ/N))`, live measured awake (average over the last 5 s), `C` in ms/s, share of budget, and body-steps per second `f × N_awake`.

**Controls.**
- Scenario: segmented control "Quiet evening" (`δ = 30`, `t_move = 1.5`), "Market day" (`δ = 150`, `t_move = 1.5`), "Siege" (`δ = 430`, `t_move = 3.0`). Default siege.
- Sleep timer `t_sleep`: slider 0 to 3 s, step 0.1, default 0.5.
- Step rate `f`: select 1, 10, 20, 23, 30, 60, 120 Hz, default 30. The 23 Hz option is the answer to check question 2.
- Props `N`: slider 2,000 to 40,000, step 1,000, default 20,000.
- Toggle "no sleeping" (sets `N_awake = N`).
- Reset.

**Formulas.** `τ = t_move + t_sleep`. `N_awake = min(N, δτ)`. `C = 1000 × f × 4e-6 × N_awake` ms/s. Exact form `N × (1 − exp(−δτ / N))`. Budget 200 ms/s.

**Test values** (`f = 30`, `N = 20,000`, `t_sleep = 0.5` unless stated). No sleeping: 2,400 ms/s. Quiet: `N_awake = 60`, 7.2 ms/s. Market: 300, 36.0 ms/s. Siege: 1,505, 180.6 ms/s, 90% of budget, exact form 1,450. Siege with `t_sleep = 2`: 2,150, 258.0 ms/s, 129%. Quiet with `t_sleep = 2`: 105, 12.6 ms/s. Siege with `N = 2,000`: Little 1,505, exact 1,058. Siege at `f = 23`: 138.5 ms/s with `t_sleep = 0.5`, 197.8 ms/s with `t_sleep = 2`.

**First screen.** Siege scenario running, with the caption "Same 20,000 props every night. Only the awake ones cost CPU."

**Accessibility.** All controls keyboard operable with visible focus. Announce `C` and the share of budget in an `aria-live="polite"` region when a control changes (not on every animation frame). With `prefers-reduced-motion`, stop the live animation and draw a static snapshot of a random awake set of the model's size, with a "step" button to advance one second. Palette from `templates/interactive-tokens.css`, light and dark. Awake props must differ from sleeping ones by size as well as colour.
