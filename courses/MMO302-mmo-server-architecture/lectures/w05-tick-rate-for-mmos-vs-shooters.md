# MMO302 · Week 05 — Tick rate for MMOs vs shooters

**Why this matters:** A shooter server ticks 20 to 128 times a second. Many MMO servers tick between once and ten times a second, and players still call them responsive. Neither choice is lazy or old-fashioned. The tick interval is a budget, and each genre spends it on a different thing. Pick your MMO's rate by copying a shooter and your servers will fall over the first time players crowd together.

**You will be able to:**
- Compute a zone server's CPU utilization from its tick rate, entity count and average AOI neighbours, and find the highest tick rate that keeps a target headroom.
- Compute the delay, timer rounding and same-batch probability that a tick rate adds to gameplay.
- Design a multi-rate schedule (different systems at different rates) and compute what it saves.
- Choose and defend an overrun policy (skip, stretch, dilate or shed load) for a given game.

**Before class:** CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), the sections on tasklets and on why they chose to slow time. Old School RuneScape Wiki, "Game tick". Reread CS202 week 13, sections 1 and 3.

**Prerequisites from earlier courses:** [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the three clocks, the latency table, and the per-tick cost `c(n) = a + d·n + e·n²`). [CS202 week 2, latency, jitter and loss](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md) (where the waiting time for the next tick fits in the latency chain). [CS101 week 9, delta time and the fixed timestep](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md). From this course, [week 1, scale targets](w01-scale-targets-ccu-messages-and-n-squared.md) (the crowd-cost model), [week 3 on AOI](w03-area-of-interest-grids-radius-hysteresis.md) (which turns `n²` into `n × k`) and [week 4, zone servers and handoff](w04-zone-servers-and-handoff.md) (where the per-zone player count comes from).

**Interactive:** [examples/w05-tick-budget.html](../examples/w05-tick-budget.html). Keep it open during section 2.

---

## 1. What a tick buys and what it costs

Recall the definition from CS202. The **tick rate** `T` is how many times per second the server advances the simulation. The **tick interval** `t = 1000 / T` milliseconds is the time between ticks. One tick reads every queued input, runs every system (movement, AI, combat, buffs, loot) and produces the updates that go out to clients.

Two facts from CS202 week 13 frame this lecture.

1. **A tick must finish before the next one starts.** If one tick takes `c` milliseconds of CPU and the interval is `t`, then the server is busy `c / t` of the time. Call that the **utilization** `u = c × T / 1000`. At `u = 1` the server has no spare time. Above 1, it falls behind.
2. **The cost of a tick grows with the crowd.** CS202 split it into fixed, per-entity and per-pair work. With week 3's AOI, "per pair" becomes "per entity per neighbour", so for `n` entities with an average of `k` neighbours each:

```
c(n, k) = a + d × n + e × n × k
```

- `a` is fixed work per tick: timers, world events, bookkeeping.
- `d` is per-entity work: applying inputs, moving, running AI, ticking buffs.
- `e` is per-neighbour work: the AOI query result, collision checks against nearby entities, writing each visible entity into each client's update.

A shooter and an MMO differ in all three letters. A shooter match has `n = 10` to 100 players and a small map. An MMO zone may hold 1,000 players and 2,000 NPCs. The NPCs matter. They run AI, they have threat tables and buffs, and players expect them to react. A zone's `n` counts them all.

What does a higher tick rate buy? Three things, and you can compute each.

- **Less waiting.** An input that arrives at a random moment waits on average `t / 2` for the next tick. At 10 Hz that is 50 ms. At 128 Hz it is 3.9 ms.
- **Finer timers.** If game rules count time in ticks, a timer of length `τ` seconds actually lasts `ceil(τ × T) / T`. A slow tick rounds timers up.
- **Fewer ties.** Actions that land in the same tick are resolved together, as if simultaneous. Two actions `δ` seconds apart land in the same tick with probability `max(0, 1 − δ × T)`, if the tick boundary falls at a random moment between them.

A shooter needs all three at their best, because a duel is decided in tens of milliseconds. Most MMO combat is decided over seconds. The question for an MMO is how much of each it can give up to afford its crowd.

## 2. Worked example: choosing a tick rate for a crowded zone

### The hook

Old School RuneScape advances its world once every 0.6 seconds. The OSRS Wiki calls this game tick the fundamental unit of time. Walking moves you one square per tick, running two, and a dagger attacks every 4 ticks (2.4 s). A members' world holds up to 2,000 players on that one clock. Valorant's servers tick 128 times a second for 10 players. That is a tick rate 77 times higher for a two-hundredth of the players. Players describe both games as responsive. So what is a tick rate *for*, and how do you choose one?

### The model

```
tick interval          t = 1000 / T                     (ms)
cost per tick          c = a + d × n + e × n × k        (ms)
utilization            u = c × T / 1000                 (keep u ≤ u_max)
highest safe rate      T_max = 1000 × u_max / c
average input wait     t / 2
timer of τ seconds     lasts ceil(τ × T) / T
same-tick probability  P = max(0, 1 − δ × T)           (two actions δ seconds apart)
```

- `u_max` is the headroom target. Servers are rarely run near 100%, because load arrives in bursts and a tick that overruns delays every player. This lecture uses `u_max = 0.6`.
- All the costs are for one core. Week 13 of this course covers spreading a zone across cores and machines.

### Numbers you can check

Take one zone with 1,000 players and 2,000 NPCs, so `n = 3,000`, and an average of `k = 50` neighbours within AOI. Use invented but realistic costs, measured on one core of a typical server: `a = 1` ms, `d = 5` µs (0.005 ms) per entity, and `e = 0.2` µs (0.0002 ms) per neighbour.

```
c = 1 + 0.005 × 3,000 + 0.0002 × 3,000 × 50
  = 1 + 15 + 30 = 46 ms per tick
```

| Tick rate `T` | Interval `t` (ms) | Utilization `u` | Verdict |
|---|---|---|---|
| 1 | 1,000 | 4.6% | Lots of headroom |
| 2 | 500 | 9.2% | |
| 5 | 200 | 23% | |
| 10 | 100 | 46% | Under the 60% target |
| 13 | 76.9 | 59.8% | `T_max = 600 / 46 = 13.04` |
| 20 | 50 | 92% | No headroom |
| 30 | 33.3 | 138% | Overruns every tick |

The shooter's rates are out of reach. At 30 Hz, this zone cannot finish one tick before the next is due. Now look at what the low rate costs the player.

| Tick rate `T` | Average wait (ms) | A 1.2 s timer lasts | P(same tick), actions 100 ms apart |
|---|---|---|---|
| 1 | 500 | 2.0 s | 90% |
| 1.67 (0.6 s) | 300 | 1.2 s | 83% |
| 5 (200 ms) | 100 | 1.2 s | 50% |
| 10 | 50 | 1.2 s | 0% |
| 50 (20 ms) | 10 | 1.2 s | 0% |
| 128 | 3.9 | 1.203 s | 0% |

Check two cells. At `T = 1`, `ceil(1.2 × 1) / 1 = 2` seconds. At `T = 5`, `P = 1 − 0.1 × 5 = 0.5`.

For an MMO whose fastest meaningful decision is an ability every 1 to 2.5 seconds, a 10 Hz tick adds an average of 50 ms, about 2 to 5% of the decision interval. A shooter duel is decided in tens of milliseconds, so the same 50 ms would be most of it. **The right tick rate depends on how fast your game asks players to decide.** Fast decisions need a short tick, and a short tick needs a small crowd.

### Now the crowd moves

Averages hide the moment that matters. Suppose a siege draws 800 of the zone's 3,000 entities into one castle courtyard, where each of them now has `k = 400` neighbours. The other 2,200 keep `k = 50`.

```
c = 1 + 0.005 × 3,000 + 0.0002 × (800 × 400 + 2,200 × 50)
  = 1 + 15 + 0.0002 × 430,000
  = 1 + 15 + 86 = 102 ms per tick
```

At 10 Hz that is 102% utilization. The zone overruns on every tick of the siege. The per-neighbour term, 30 ms before, is now 86 ms. The same number of entities, gathered together, cost more than twice as much. That is the `n × k` term doing what CS202 warned about.

You have four ways out, and section 4 compares them. The simplest is already in the table. At 5 Hz the siege costs 51%. A zone that normally runs at 10 Hz and drops to 5 Hz under a siege keeps up, at the price of 100 ms average wait instead of 50.

Open the interactive. Set the "MMO zone" preset, then drag the crowd slider. The bar that shows one tick's cost grows past the tick interval line, and the timeline on the right shows ticks starting late, one after another. Drag the tick rate down and watch the bar fit again, while the timeline shows actions bunching into fewer, larger batches.

### Same idea elsewhere

**Old School RuneScape (Jagex, current).** OSRS runs `T = 1/0.6 = 1.67` Hz and designs every rule in whole ticks, so the timer-rounding column never hurts it. A dagger is 4 ticks, all combat spells 5 ticks. Actions registered during a tick take effect from the start of the next, so a click waits between 0 and 0.6 s, on average 300 ms, which is 12.5% of a 2.4 s attack. The OSRS Wiki records that ticks on the fullest worlds take 0.616 to 0.618 s, against 0.606 to 0.611 s on quieter ones, and that busy worlds occasionally miss ticks. In our form, `c` rises with the world's population and the tick stretches a few percent rather than falling behind. The wiki also notes that players who know the clock can time their actions to it, so the tick grid becomes part of player skill.

**EVE Online (CCP, current mechanics and 2011 dev blog).** EVE aims for `T = 1`. The EVE University wiki gives an example of the rounding column: a 1.2-second target lock rounds up to 2 ticks, so 2 seconds. It also explains why the tick must be long. A node hosts hundreds of solar systems, so a tick for one grid may get a hundredth of a second of CPU or less, and it cannot wait on the database. In the 2011 Time Dilation blog, CCP's developer wrote that the physics simulation itself was only about 5 to 10% of the load in large fights. Lowering its rate would buy little. Most of the load was tied to game time, such as module cycles, travel and warping. So CCP chose to stretch game time itself, down to 10% speed in the heaviest fights. That is the "stretch" policy of section 4 taken to its limit, and it gets week 12 to itself.

**World of Warcraft (Blizzard, 2004 to today).** WoW's server groups actions into batches and resolves each batch together, which Blizzard confirmed in a 2019 forum post about WoW Classic. The post gives an example from the original game: a warrior's interrupt and a mage's Polymorph cast in the same batch could both succeed, because both were valid at the start of the batch. Blizzard said it had since made batches more frequent and kept the original behaviour in Classic on purpose. Blizzard's patch notes for WoW Classic 1.13.7 (2021) give the number. Classic had used a 400 ms batch window, and that patch cut it to 10 ms. In our form, `T` went from 2.5 to 100. With actions 100 ms apart, the same-batch probability falls from `1 − 0.1 × 2.5 = 75%` to 0. Two players reacting 10 ms apart tied 97.5% of the time at 400 ms batches and never tie at 10 ms.

**Shooters (Riot 2020, Respawn 2021).** Valorant runs at 128 Hz. Riot's engineers set a budget of 2.34 ms per game per tick so that three games share each core, 108 games on a 36-core host. With our invented constants, a 10-player match costs `1 + 0.005 × 10 + 0.0002 × 10 × 9 ≈ 1.07` ms, so the shape fits: tiny `n`, tiny `k`, and all the savings spent on `T`. Apex Legends, with 60 players, runs at 20 Hz. Respawn argued that tripling to 60 Hz would triple bandwidth and CPU for about two frames of input delay in the best case. Their decision is the same trade in reverse.

Four games, one model. Each chose the rate its decisions need and then shaped `n` and `k` so the budget closes.

### Design judgment

- **Start from the decision interval, not the genre.** List the fastest thing a player can meaningfully do. If it is a 1.5 s global cooldown, 10 Hz is generous. If it is a parry window of 200 ms, you need at least 20 Hz in that zone, and you should budget the crowd for it.
- **Design in ticks when the tick is slow.** OSRS shows that a 600 ms tick is fine when every rule is an integer number of ticks. What hurts is a 1.2 s timer on a 1 s tick. Pick durations that are multiples of `t`.
- **Budget the siege, not the average.** The utilization at the average `k` is a comfort number. Size `T` so the densest moment your design allows still fits, or decide in advance what gives way.
- **Buy responsiveness on the client.** The client can play the animation and sound the instant the key is pressed, while the server confirms at the next tick. The EVE wiki describes exactly this. The client shows the action immediately, and the effect lands on the next tick. Players read the feedback, not the server clock.

### Check this example

1. A zone has 2,000 entities with `k = 30`, and the same costs (`a = 1`, `d = 0.005`, `e = 0.0002` ms). Find `c`, the utilization at 10 Hz, and `T_max` for `u_max = 0.6`.
2. Your ability timers are 1.0, 1.5 and 2.5 s. Which of 2, 4 and 5 Hz rounds none of them up?
3. Two healers press their big cooldown 30 ms apart. What is the chance the server resolves both in the same tick at 10 Hz? At 20 Hz?

<details>
<summary>Answers</summary>

1. `c = 1 + 10 + 0.0002 × 2,000 × 30 = 1 + 10 + 12 = 23` ms. `u = 23 × 10 / 1000 = 23%`. `T_max = 600 / 23 = 26.1` Hz.
2. At 2 Hz, 1.0 → 2 ticks, 1.5 → 3, 2.5 → 5 ticks: none rounded. At 4 Hz, 1.0 → 4, 1.5 → 6, 2.5 → 10: none rounded. At 5 Hz, 1.5 × 5 = 7.5 rounds up to 8 ticks, 1.6 s. So 2 and 4 Hz both work; 5 Hz does not.
3. `1 − 0.03 × 10 = 0.7` at 10 Hz. `1 − 0.03 × 20 = 0.4` at 20 Hz.

</details>

## 3. Not everything needs the same rate

A tick runs every system at the same rate only if you let it. Most MMO systems need far less than the movement and combat rate.

| System | Rate that feels right | Why |
|---|---|---|
| Player movement and combat | 10 to 20 Hz | Players watch it directly |
| NPCs near players | same as players | They fight players |
| NPCs with no player within AOI | 1 Hz or asleep | Nobody can see them |
| Health and mana regeneration, buffs | 1 Hz, or computed on demand | Changes slowly; can be computed from elapsed time |
| Weather, day/night, world events | 0.1 Hz or less | Minutes-long changes |
| Saving to the database | once per minutes, or on events | Week 7 |

A **multi-rate schedule** runs each system on its own period, as a multiple of the base tick. The cost per second becomes a sum:

```
CPU per second = Σ over systems  T_i × c_i
```

Apply it to the example zone. Of the 2,000 NPCs, suppose 1,600 have no player within AOI. Run them at 1 Hz and everything else at 10 Hz.

```
single rate:  10 × 46 ms = 460 ms of CPU per second
multi-rate:   10 × (1 + 0.005 × 1,400 + 0.0002 × 1,400 × 50)   = 10 × 22 = 220 ms
            +  1 × (0.005 × 1,600 + 0.0002 × 1,600 × 50)        = 1 × 24  = 24 ms
            = 244 ms of CPU per second
```

That is 47% less CPU for a change no player can see. The cost is complexity. An NPC that wakes because a player walked up must catch up on the time it slept, and systems that run at different rates must agree on the order of events. Put the rate change at the AOI boundary you built in week 3, and give every system a clear rule for catching up (usually "compute from elapsed time" rather than "replay the missed ticks").

## 4. When a tick does not fit

Sooner or later a tick will take longer than its interval. Decide what happens before it does. There are four policies, and every shipped MMO uses one of them or a mix.

1. **Skip.** Drop the late tick's simulation and jump the clock ahead. Movement jumps and timers stutter. Cheap to implement, unpleasant to watch, and it can break rules that assume every tick runs.
2. **Stretch.** Let the tick take as long as it needs and start the next one late. Game time runs slower than wall-clock time by the overrun ratio. OSRS's full worlds, with ticks a few percent over 0.6 s, behave like this in a mild way. Fair to everyone on the server, because everyone slows together.
3. **Dilate on purpose.** Stretch, but measure the load and set the clock rate deliberately, smoothly and in fine steps, and tell the players. This is EVE's Time Dilation. Its blog argued that because most load is tied to game time, slowing time cuts load in proportion.
4. **Shed load.** Keep the tick rate and do less per tick. Shrink the AOI radius so `k` falls, send distant entities less often, or lower the tick rate for this one zone. The siege example did this when it dropped the zone to 5 Hz.

| Policy | Players notice | Fairness | Cost to build |
|---|---|---|---|
| Skip | Jumps, broken timers | Poor, rules can misfire | Low |
| Stretch | Everything slower | Fair within the zone | Low |
| Dilate | Everything slower, shown on screen | Fair, predictable | Medium |
| Shed load | Less detail or lower rate in one place | Fair if rules are rate-independent | Medium to high |

Shedding load keeps the world's time honest, so it suits PvE zones and events with timers players race against. Dilation suits fights where correctness matters more than speed, such as EVE's thousand-ship battles. Skipping is almost never the right answer for a game with rules. It is the default you get if you never decide.

## In-class activity (25 minutes)

In pairs, pick one of these three games-in-design and choose a tick rate for its busiest zone.

- A: A tab-target MMO with a 1.5 s global cooldown, 800 players and 1,500 NPCs per zone, and a 120-player world boss.
- B: An action MMO with dodges that have a 250 ms invulnerability window, 200 players per zone and 40-player raids.
- C: A sandbox MMO with 2,000 players per zone and ships that take 5 to 20 seconds to turn.

Use `a = 1` ms, `d = 5` µs and `e = 0.2` µs.

1. Estimate `n` and `k` for the busiest moment, and compute `c`.
2. Choose `T` so that `u ≤ 0.6` at that moment, and check the delay and timer-rounding columns against the game's fastest decision.
3. Choose an overrun policy and a multi-rate schedule for one system.
4. Write one sentence a player would read in a patch note explaining your choice.

Expected output: a filled-in table with `n`, `k`, `c`, `T`, `u`, average wait, the overrun policy, and the patch-note sentence.

## Common misconceptions

- **"A higher tick rate is always better."** It buys less waiting at a cost that grows linearly, and the benefit falls as `1/T`. For decisions measured in seconds, going from 10 to 60 Hz saves 42 ms of average wait for six times the CPU.
- **"The server tick rate is the rate at which clients see updates."** CS202 separated the tick rate from the snapshot rate. An MMO can simulate at 10 Hz and send distant entities at 2 Hz.
- **"Lag in big fights is network lag."** In EVE's large fights, the blog describes server-side CPU queues, with tasks waiting seconds for a turn. The fix was to slow game time, not to buy bandwidth.
- **"A slow tick makes the game feel slow."** A slow tick with client-side feedback, and rules designed in whole ticks, feels deliberate. OSRS is the proof.

## Check yourself

1. A zone runs at 20 Hz with `c = 18` ms on a normal evening. A holiday event doubles `k` for everyone. Before the event the per-neighbour term was 10 ms of the 18. What are `c` and `u` during the event, and which policy would you choose?
2. A designer wants a parry with a 150 ms window that opens exactly on a tick. At 10 Hz, give a press time inside the window that the server resolves after the window has closed. Which of 5, 10 and 20 Hz resolves every press inside the window no later than the moment it closes? What rule does that suggest?
3. You have 300 ms of CPU per second available for one zone. A system costs 20 ms per tick at 10 Hz. If you run it at 2 Hz instead, how much CPU do you free, and what did you trade?

<details>
<summary>Answers</summary>

1. The per-neighbour term doubles from 10 to 20 ms, so `c = 28` ms and `u = 28 × 20 / 1000 = 56%`. That still fits under a 60% target. If it had not, shedding load (smaller AOI radius during the event) keeps the event's timers honest.
2. At 10 Hz the ticks fall at 0, 100 and 200 ms. A press at 140 ms waits for the tick at 200 ms, after the window closed at 150. At 5 Hz a press at 10 ms waits until 200 ms, so it fails too. At 20 Hz the ticks fall at 50, 100 and 150 ms, so every press inside the window is resolved by 150 ms. The rule is to make timing windows a whole number of ticks, or to timestamp inputs and judge them against the window, which is the rewind idea from CS202 week 11.
3. `10 × 20 = 200` ms per second before, `2 × 20 = 40` after, so 160 ms per second freed. You traded that system's responsiveness. Its average wait rises from 50 to 250 ms and its timers round to 0.5 s.

</details>

## Lab / assignment hook

[Lab 05, tick budget profiler](../labs/lab05.md). You run a small Python world server with grid AOI, measure the cost of a tick at several `n` and `k`, fit `a`, `d` and `e` from your own measurements, and find the highest tick rate your machine can hold for a 60% target. Then you add a multi-rate schedule and an overrun policy and show the saving. The fitted constants feed the capacity model in week 11's load test.

## Sources

- Old School RuneScape Wiki, "Game tick" (accessed September 2026). 0.6 s per tick; actions registered in a tick take effect from the next; observed tick lengths of 0.616 to 0.618 s on World 302 and 0.606 to 0.611 s on quieter worlds; busy worlds sometimes miss ticks.
- Old School RuneScape Wiki, "Attack speed" and "Game square" (accessed September 2026). Dagger 4 ticks (2.4 s), combat spells 5 ticks (3.0 s); walking one square per tick, running two.
- Old School RuneScape Wiki, "Server" (accessed September 2026). Members' worlds allow 2,000 players.
- EVE University Wiki, "Server tick" (accessed September 2026). One tick per second target; a 1.2 s lock rounds up to 2 ticks; a node handles hundreds of systems and a grid may get a hundredth of a second of work per tick; the tick does not talk to the database; the client shows commands immediately and effects land on the next tick.
- EVE University Wiki, "Time dilation" (accessed September 2026). Slowest speed 10%.
- CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011). Tasklets waiting seconds for a turn under load; physics about 5 to 10% of the load; most load tied to the game clock; dynamic, fine-grained slowing of time. Paraphrased.
- Blizzard Entertainment, "Spell Batching in Classic" (WoW forums, 2019), as quoted in Anshlun, "Spell Batching in Classic WoW" (Wowhead, 28 March 2019). Batching confirmed, the Pummel and Polymorph example, more frequent batches in modern WoW, original behaviour kept for Classic.
- Blizzard Entertainment, WoW Classic patch 1.13.7 notes (2021), as reproduced on Warcraft Wiki, "Patch 1.13.7" (accessed September 2026). The 400 ms spell batch window reduced to 10 ms.
- Randall, B. "VALORANT's 128-Tick Servers" (Riot Games, 31 August 2020). 128 Hz, 7.8125 ms per tick, 2.34 ms per game, three games per core, 108 games on a 36-core host.
- Respawn Entertainment, "Servers & Netcode Developer Deep Dive" (Apex Legends news, 28 April 2021). 20 Hz; 60 Hz would triple bandwidth and CPU for about two frames of input delay.
- The cost constants `a`, `d`, `e` in this lecture are invented for teaching and labelled as such. Lab 05 has you measure your own.

## Interactive spec: examples/w05-tick-budget.html

**Insight the visual must make obvious:** a tick interval is a CPU budget, and the crowd spends it. When players gather, one tick's cost grows past the interval and ticks start late; lowering the tick rate makes the cost fit again, and the price appears on the timeline as bigger batches and longer waits. Shooters and MMOs sit at opposite corners of the same picture.

**Layout.** Two linked views and a number panel. Desktop: side by side, panel beneath. Under 700 px: stacked, budget bar first.

1. **Budget bar (left).** A horizontal time axis from 0 to `max(t, c) × 1.2` ms. One stacked bar for one tick's cost, segments `a` (fixed), `d × n` (per entity), `e × Σ n_i k_i` (per neighbour), each labelled with its ms value. A vertical line at the interval `t` labelled "next tick due", and a dashed line at `u_max × t` labelled "headroom target". The bar is green below the dashed line, amber between, red past `t`. When multi-rate is on, draw the average cost per tick (`CPU per second / T`) as a second, thinner bar beneath.
2. **Timeline (right).** Three seconds of wall-clock time. Tick marks every `t` ms, each drawn as a block of width `c`. If `c > t` and the policy is "stretch", each tick starts when the previous one ends, so blocks drift right of their due marks; show the drift in ms at the end. If the policy is "skip", drop every tick whose start would be late by more than one interval and draw a red "skipped" marker. Two rows of player actions: player A presses at a random time each 1.5 s, player B presses `δ` ms after A. Draw a bracket over any pair that resolves in the same tick, and colour the pair's dots gold.
3. **Number panel.** `t`, `c`, `u`, `T_max` for the target, average wait `t/2`, a timer of `τ` seconds rounded to `ceil(τT)/T`, the same-tick probability `max(0, 1 − δT)`, CPU per second single-rate and multi-rate, and "late by" drift after 3 s.

**Controls.**
- Preset buttons: "MMO zone" (`n = 3,000`, `k = 50`, `T = 10`), "Siege" (as MMO zone plus crowd 800 at `k = 400`), "Shooter match" (`n = 10`, `k = 9`, `T = 128`), "OSRS-like world" (`n = 2,000`, `k = 60`, `T = 1.667`).
- Slider `T`, log scale over 1 to 128 Hz, with snap points 1, 1.667, 2, 5, 10, 20, 30, 60, 128.
- Slider `n`, 10 to 6,000. Slider `k`, 1 to 200.
- Crowd: slider "entities in crowd" `n_c`, 0 to `n`, default 0, and slider `k_c`, 50 to 800, default 400. The per-neighbour term uses `n_c × k_c + (n − n_c) × k`.
- Cost constants: number fields `a` (ms, default 1), `d` (µs, default 5), `e` (µs, default 0.2). Target `u_max`, slider 0.3 to 1.0, default 0.6.
- Toggle multi-rate (default off) with "idle NPCs" slider, 0 to `n`, default 1,600, run at 1 Hz; their `d` and `e` work leaves the per-tick bar and is charged once per second.
- Overrun policy selector: stretch (default) or skip.
- Sliders `δ` (0 to 500 ms, default 100) and `τ` (0.1 to 5 s, default 1.2).
- All sliders keyboard accessible.

**Formulas.** `t = 1000 / T`. `c = a + d_ms × n + e_ms × (n_c × k_c + (n − n_c) × k)`, with `d_ms = d / 1000`, `e_ms = e / 1000`. `u = c × T / 1000`. `T_max = 1000 × u_max / c`. Multi-rate with `m` idle NPCs: per-tick cost `c_active = a + d_ms × (n − m) + e_ms × (neighbour work of the n − m active entities)`, idle cost per second `c_idle = d_ms × m + e_ms × m × k` (idle NPCs use `k`, never the crowd `k_c`), CPU per second `= T × c_active + 1 × c_idle`.

**Test values** (assert on load).
- `n = 3,000`, `k = 50`, defaults: `c = 46.0` ms; `u` at 10 Hz `= 46.0%`; at 30 Hz `138%`; `T_max = 13.04` Hz.
- Siege, `n_c = 800`, `k_c = 400`: `c = 102.0` ms; `u` at 10 Hz `= 102%`, at 5 Hz `51%`.
- Multi-rate with 1,600 idle NPCs at 10 Hz: `c_active = 22` ms, `c_idle = 24` ms, CPU per second `244` ms against `460` single-rate.
- Shooter preset: `c = 1.068` ms; `u` at 128 Hz `= 13.7%`.
- `τ = 1.2` s: 2.0 s at 1 Hz, 1.2 s at 1.667 Hz, 1.203 s at 128 Hz. `δ = 100` ms: `P` = 90% at 1 Hz, 83.3% at 1.667 Hz, 50% at 5 Hz, 0% at 10 Hz.

**First screen:** "Siege" preset at 10 Hz with the policy on stretch, so the bar is red and the timeline blocks drift late. Caption: "800 players in one courtyard: each tick needs 102 ms but only has 100. Drag the tick rate to 5 Hz."
