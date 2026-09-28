# CS202 · Week 12 — Deterministic lockstep (RTS)

**Why this matters:** Everything since week 7 has sent *state*, the positions of things, and that cost grows with the number of things. A strategy game with a thousand units, or a factory game with a million belts, cannot afford it. Deterministic lockstep sends only the players' orders and has every machine run the identical simulation. Bandwidth stops depending on the size of the world. In exchange, every machine must compute exactly the same bits, every turn, forever, and the whole game moves at the pace of its slowest link.

**You will be able to:**
- Compute and compare the bandwidth of state synchronization and lockstep for a given player count, unit count and turn length, and find the unit count where lockstep wins.
- Compute the command delay and the effective turn length of a lockstep game from its turn length, scheduling depth `k` and worst one-way latency.
- Identify the sources of non-determinism in simulation code (floating-point order, random number generators, iteration order, local-only state) and fix them.
- Implement per-turn checksums and use them to find the first turn and the field where two peers diverge.

**Before class:** Paul Bettner and Mark Terrano, "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (Gamasutra, March 2001), up to and including "Lessons learned". Glenn Fiedler, "Deterministic Lockstep" (Gaffer on Games, November 2014). Factorio Friday Facts #76, "MP inside out" (March 2015), the section "Lock step".

**Prerequisites from earlier courses:** [CS102 week 12, the command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (a lockstep game is a command log executed on every machine; replays come free). [CS102 week 14, unit testing gameplay rules](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md) (determinism is a property you test for). [CS101 week 9, the fixed timestep](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (a variable `dt` breaks determinism). [CS202 week 3](w03-topologies-peer-to-peer-client-server-relay.md) (full-mesh upload). [CS202 week 4](w04-server-authority-never-trust-the-client.md) (lockstep detects cheating instead of preventing it). [CS202 week 8](w08-client-side-prediction.md) (the shared `step` function, which lockstep takes to its limit).

**Interactive:** [examples/w12-lockstep-timeline.html](../examples/w12-lockstep-timeline.html). Keep it open during section 2.

---

## 1. Send the orders, not the army

Every technique so far has one shape. The server simulates, and it sends the results, positions and health and animation states, to each client. This is **state synchronization**. Its cost is proportional to the amount of state that changes, which in a strategy game means the number of units.

**Deterministic lockstep** turns this around. Every machine runs the full simulation. The only thing that crosses the network is player input, "these three archers attack that catapult". Each machine applies the same inputs at the same simulation step and computes the same result. Fiedler states the benefit in one line. Bandwidth is proportional to the size of the input, not the number of objects, so a simulation of a million objects needs the same bandwidth as one of a single object.

It works only if the simulation is **deterministic**. Given the same starting state and the same inputs, it must produce exactly the same result on every machine, bit for bit. Fiedler is emphatic that "exactly" means exactly. A position that differs in the last bit of a float is a different game, because small differences grow. The Age of Empires team described a deer that stood slightly out of alignment when the random map was built. It foraged a little differently, minutes later a villager's path went a tiny bit off, the villager's spear missed, and one player's food count no longer matched the other's.

The word **lockstep** describes the timing. Machines advance in **turns**, and no machine runs turn `n` until it holds every player's commands for turn `n`. A player who issued no command must still send an empty "turn done" message, or everyone waits.

## 2. Worked example: 1500 archers on a 28.8

### The hook

In 1996 Ensemble Studios set its multiplayer targets for Age of Empires. Eight players. A Pentium 90 with 16 MB of memory. A 28.8 kbit/s modem. And armies big enough to besiege a Greek city from land and sea at once. Bettner and Terrano's 2001 postmortem says a few quick calculations ruled out sending unit state. Just X and Y coordinates, status, action, facing and damage would have limited them to about 250 moving units in the whole game. They shipped with thousands, over internet connections whose latency swung between 20 and 1,000 ms. How?

### The model

**Bandwidth.** Take `P` players in a full mesh (week 3), each sending to `P − 1` peers, with `h = 28` bytes of IPv4 and UDP header per packet (week 1) and a 4-byte turn and sequence field.

```
state sync, per peer upload  = (P − 1) × r × (h + 4 + s × N / P)
lockstep,   per peer upload  = (P − 1) × [ (1000 / T) × (h + 4) + b × c ]
```

- `N` units in the whole game, `N / P` owned by each player, `s` bytes per unit update, `r` updates per second.
- `T` the turn length in ms, one packet per turn per peer, `b` bytes per command and `c` commands per second per player.

The first line grows with `N`. The second doesn't contain `N` at all.

**Timing.** A command issued during turn `n` runs at the start of turn `n + k`. Age of Empires used `k = 2`.

```
command delay            in ((k − 1)T, kT],  average (k − ½)T
no stall if              L_max ≤ (k − 1)T
effective turn length    T_eff = max(T, (T + L_max) / k)
```

`L_max` is the worst one-way latency between any two peers. The last line comes from the rule that turn `n + k` can't start until turn `n`'s commands, sent when turn `n` ends at `start(n) + T`, have reached every peer. So `k` turns must span at least `T + L_max`. If they don't, every machine waits, and the game slows down for all eight players.

### Numbers you can check

**Table 1. Bandwidth on a 28.8 modem.** Eight players, full mesh. The modem carries at most `28,800 / 8 = 3,600` bytes per second each way. For state sync we assume an illustrative 8 bytes per unit update, sent `r = 2` times per second. For lockstep, `T = 200` ms turns (5 per second) and 2 commands per player per second (120 actions per minute) at 8 bytes each. These unit and command sizes are our assumptions, not Ensemble's.

| Units `N` | State sync upload `14 × (32 + N)` | Lockstep upload | Fits 3,600 B/s? |
|---|---|---|---|
| 50 | 1,148 B/s | 1,232 B/s | both |
| 56 | 1,232 B/s | 1,232 B/s | both, break-even |
| 225 | 3,598 B/s | 1,232 B/s | both, state sync at its limit |
| 250 | 3,948 B/s | 1,232 B/s | lockstep only |
| 1,500 | 21,448 B/s | 1,232 B/s | lockstep only |

Check the lockstep column. `7 × (5 × 32 + 8 × 2) = 7 × 176 = 1,232` B/s. Check the state column at 250 units. `7 × 2 × (32 + 8 × 250 / 8) = 14 × 282 = 3,948` B/s. With these assumptions state sync runs out at 225 units, in the same range as Ensemble's estimate of 250. At 1,500 units it needs six modems.

Two things stand out. Lockstep's cost is dominated by the 28-byte headers, not the commands. And at small unit counts state sync is *cheaper*. Lockstep's advantage is about scaling. It is not free.

**Table 2. Timing with 200 ms turns and `k = 2`.** Lab 12's `simulate_turns` produces the jitter column, with each message delayed by an extra `U(0, 60)` ms.

| Worst one-way `L_max` | `T_eff`, fixed latency | Average command delay | `T_eff`, with 60 ms jitter | Average command delay |
|---|---|---|---|---|
| 50 ms | 200 ms | 300 ms | 200.0 ms | 300 ms |
| 150 ms | 200 ms | 300 ms | 201.2 ms | 302 ms |
| 200 ms | 200 ms | 300 ms | 220.6 ms | 331 ms |
| 250 ms | 225 ms | 338 ms | 244.9 ms | 367 ms |
| 400 ms | 300 ms | 450 ms | 319.3 ms | 479 ms |

Check the 250 ms row. `(200 + 250) / 2 = 225`, larger than 200, so the game runs 225 ms turns. The average delay is `1.5 × 225 = 337.5` ms. Every player pays for the one slow link.

Now compare with what players tolerate. Ensemble's testing found that 250 ms of command latency in an RTS was not even noticed, 250 to 500 ms was very playable, and over 500 ms it started to be noticeable. Every row of Table 2 is under 500 ms. A shooter could not accept any of them, which is why lockstep is a strategy-game technique. Ensemble also found that a *consistent* delay mattered more than a small one. A steady 500 ms was playable, while a delay that jumped between 80 and 500 ms felt jerky. So they chose longer turns rather than risk stalls.

**Table 3. The `k` trade.** For `L_max = 400` ms and `T = 200`.

| `k` | `T_eff` | Average command delay | Stalls? |
|---|---|---|---|
| 2 | 300 ms | 450 ms | yes, the game slows by 50% |
| 3 | 200 ms | 500 ms | no |

Raising `k` adds 50 ms of average delay and removes the slowdown. Lockstep designers are always choosing between a longer fixed delay and a variable one, and Ensemble's finding says to prefer the fixed one.

### Move it yourself

Open `examples/w12-lockstep-timeline.html`. The left view is a timeline with one row per peer. Turns are drawn as boxes. Each peer's "turn done" message is an arrow from the end of its turn to the other peers' rows, arriving after the link's latency. When a turn can't start because an arrow hasn't arrived, the gap is shaded red and labelled "stall". The right view plots upload bytes per second against unit count, with a rising line for state sync, a flat line for lockstep and a horizontal line for the modem's budget. Drag the worst link's latency past 200 ms and watch red gaps appear on every row, not just the slow peer's. Raise `k` to 3 and they disappear while the command-delay readout grows. Then drag the unit count to 1,500 and watch the state-sync line leave the chart.

### Same idea elsewhere

Each system below chooses a turn length `T`, a depth `k`, and a response to a slow peer.

**Age of Empires (Ensemble Studios, 1997).** `T = 200` ms typically, `k = 2`. Each machine measured its own frame rate and its ping to the others and sent both with its "turn done" message, 2 bytes in all. A host picked the turn length and frame rate for everyone from those reports, raising it quickly when latency rose and lowering it slowly. Ensemble called this speed control. It is our `T_eff` rule, run on purpose instead of by stalling. Commands went over UDP with each client handling ordering and resends.

**Factorio (Wube Software, multiplayer since 0.11.0, October 2014).** Every peer simulates the whole factory and only player actions are sent, which Wube says scales equally well to a hundred objects or a million. The developers name Age of Empires and StarCraft as earlier users of the approach. Their notes list the same two costs. A player whose machine can't keep up slows the game for everyone, and a buffer they call "latency", set when starting the game, lets peers wait for messages without lagging but delays every local action by that time. That setting is `(k − 1)T` in our model. Their name for a divergence, "desync", is the one players use.

**Fiedler's deterministic lockstep demo (Gaffer on Games, 2014).** Fiedler sends one input per 60 Hz simulation frame, so `T = 16.7` ms, and replays them on the far side through a 100 ms playout delay buffer, so `(k − 1)T = 100` ms and `k = 7`. Over TCP, every lost packet froze the remote simulation for at least two round trips while TCP resent it, because frame `n` can't run without input `n`. His fix was to send over UDP and include every unacknowledged input in every packet. Inputs are only 6 bits, so even 120 of them are 90 bytes. No packet is ever resent, and a loss is covered by the next packet.

**Fighting games, delay-based and rollback.** A two-player fighting game is lockstep with `P = 2` and `T` of one 60 Hz frame. "Delay-based" netcode is exactly our model. It adds `k − 1` frames of input delay so the opponent's input usually arrives in time, and stalls when it doesn't. GGPO's documentation describes the traditional approach as adding delay to a player's input, resulting in a sluggish feel. Rollback, which GGPO implements, keeps the deterministic simulation and removes the delay. Section 5 shows how.

Four systems, one timing rule. Commands run `k` turns after they are issued, and the turn can't be shorter than `(T + L_max) / k`.

### Design judgment

- **Use lockstep when state is large and inputs are small.** Hundreds of units, a few players, commands a few times per second. Table 1's break-even says a small skirmish game might do better with state sync.
- **Use it only where command delay is acceptable.** A 300 ms delay is invisible in an RTS and unplayable in a shooter. If your genre can't hide `(k − ½)T`, you need prediction (weeks 8 and 9) or rollback.
- **Keep the delay steady.** Ensemble's players preferred a consistent 500 ms to a delay that varied between 80 and 500 ms. Adapt `T` slowly, and prefer raising `k` to stalling.
- **Budget for determinism from day one.** It is a property of every line of simulation code, and one careless call breaks it (section 3). Microsoft's product manager on the game predicted that out-of-sync would be the one stubborn bug that lasted until ship, and the postmortem says he was right.
- **Plan for what lockstep makes hard.** A player who joins mid-game needs the full state, not a command log, so you must serialize the world anyway. Every machine knows everything, so map-reveal cheats are easy, though changing the game only desyncs the cheater (week 4). And the slowest connection sets the pace for all.
- **Collect what lockstep makes easy.** A replay is the starting state plus the command log. Age of Empires II's recorded games came from exactly that, and Ensemble called them invaluable for sharing reproducible bug reports.

### Check this example

1. Twelve players, full mesh, `T = 125` ms, 3 commands per player per second at 10 bytes each, `h + 4 = 32` bytes. What is each peer's upload?
2. A lockstep game uses `T = 100` ms and `k = 3`. What is the average command delay, and what worst one-way latency can it tolerate without stalling? What is `T_eff` if one link has 300 ms?
3. With Table 1's state-sync assumptions, how many units can eight players support if they cut `r` to 1 update per second?

<details>
<summary>Answers</summary>

1. `11 × (8 × 32 + 10 × 3) = 11 × 286 = 3,146` B/s. (`1000 / 125 = 8` packets per second per peer.)
2. Average delay `2.5 × 100 = 250` ms. No stall while `L_max ≤ (3 − 1) × 100 = 200` ms. With 300 ms, `T_eff = max(100, (100 + 300) / 3) = 133.3` ms, so the game slows by a third.
3. `7 × 1 × (32 + N) ≤ 3,600`, so `N ≤ 482`.

</details>

## 3. Determinism: the hard part

"Run the same code on the same inputs" sounds automatic. It is not, because code reads more than its inputs. Four common leaks, each with its fix.

**Floating-point order.** Floating-point addition is not associative. In Python, on any machine:

```pycon
>>> (0.1 + 0.2) + 0.3
0.6000000000000001
>>> 0.1 + (0.2 + 0.3)
0.6
```

If two peers add the same damage values in a different order, their health totals differ in the last bit. On the same compiled binary, on the same CPU family, the order is the only risk. Across compilers, operating systems, instruction sets, or even debug and release builds, Fiedler warns that floating-point results can differ for the same expression. There are three fixes, from weakest to strongest. Apply events in one canonical order. Keep one build per platform and forbid mixed-platform matches. Or move simulation state to **fixed-point** integers, such as positions in millimetres and health in tenths of a point. Integers add the same way everywhere. Lab 12's simulation uses them throughout.

**Random numbers.** A lockstep game may use randomness, as long as every peer draws the same numbers in the same order. Seed one generator identically on every machine and never let anything outside the simulation draw from it. Ensemble learned this with sounds. Random terrain sounds played from inside the simulation made the games diverge, and programmers had to learn to make the same number of calls to the random generator on every machine. Give cosmetic effects their own local generator.

**Iteration order.** Many containers do not promise an order. Python randomizes string hashing per process, so this line can print a different order each time you run it:

```python
print(list({"archer", "catapult", "trireme"}))
```

If the simulation loops over a set of units to resolve combat, two peers can resolve the same fight in a different order. Iterate sorted lists or arrays keyed by a stable id.

**Local-only information.** Anything that differs per machine must stay out of the simulation. That includes the wall clock, the frame rate, which units are on your screen, your camera, your settings and who the local player is. Ensemble's rule was that simulation code must not depend on any local factor, such as having free time, special hardware or different settings. The same goes for command order. Peers receive their own commands first and other players' later, so each turn's commands must be sorted into a canonical order, such as by player and sequence number, before they are applied.

### Finding a desync

You can't prevent every leak, so you detect them. At the end of every turn each peer hashes the state that matters and includes the hash in its next message.

```python
import struct, zlib

def checksum(turn, units):
    data = struct.pack("<i", turn)
    for u in units:                                   # a list in id order, not a set
        data += struct.pack("<iiii", u.uid, u.x, u.y, u.hp)
    return zlib.crc32(data)
```

`struct.pack` with an explicit byte order makes the bytes identical on every machine. When the hashes differ, the game knows the turn of divergence, which is usually long after the cause. Age of Empires stopped such games with an "out of sync" message. Finding the cause is the hard part. Ensemble checksummed the world, the objects, pathfinding and targeting, and still sifted through 50 MB message traces. For their next engine they built sync logging that tags every checksummed value with the system it came from, such as the random generator, so the first differing tag points at the culprit.

The general method is the one you will use in Lab 12. Run two peers on the same command log. Compare per-turn checksums to find the first bad turn. Dump the state of both peers at that turn and diff them. The differing field tells you which system to read.

## 4. Lockstep in a client-server world

Pure lockstep is peer-to-peer. Each peer waits for all others, and a mesh's upload grows with `P`. Two variations are common.

- **A relay or server that orders commands.** Peers send commands to one machine, which stamps each with a turn and broadcasts the combined list. Upload per peer becomes one packet per turn, and the server can decide a late peer's turn is empty instead of making everyone wait. The simulation is still run on every client. Week 3's relay topology fits here.
- **Checksums to a server.** Peers send per-turn hashes to the server as well, so a disagreement can be judged by majority, and a single modified client can be identified and dropped. Lockstep can't stop a peer from lying, but it makes lying visible.

## 5. Removing the delay: rollback

Lockstep's delay exists because a machine waits for other players' inputs. **Rollback** refuses to wait. The machine runs frame `n` with a *guess* for each remote input, usually "the same as their last input", and saves its state. When the real input for frame `n` arrives and differs from the guess, it restores the saved state for frame `n`, applies the real input, and re-simulates every frame up to the present, all within one displayed frame.

This is week 9's reconciliation, applied to the whole game instead of one player. It needs the same deterministic `step` as lockstep, plus the ability to save and restore state cheaply. Its cost is CPU. At 60 frames per second and 100 ms of one-way latency, a mispredicted input can mean re-simulating six frames in one. That is affordable for two fighters on a stage and far too much for 1,500 archers, which is why fighting games use rollback and large RTS games keep a command delay. GGPO's documentation describes the payoff from the player's side. The timings, reactions and muscle memory built offline carry over to online play.

## In-class activity (25 minutes)

Groups of four, each student one peer in a four-player lockstep game on paper. The instructor hands out a latency matrix (one-way ms between each pair, with one bad link) and a deck of command cards.

1. With `T = 200` and `k = 2`, compute `T_eff` from the matrix. Predict which turns stall.
2. Play eight turns. Each student writes their commands for turn `n + 2` on a card during turn `n` and "sends" it by passing it on after the link's delay (the instructor calls out time in 50 ms steps). No one may start a turn without every card for it. Record actual start times.
3. Each peer applies each turn's cards to a shared starting board in the order they received them, then computes a checksum (sum of unit positions times ids, mod 97). Compare checksums after each turn.
4. Fix the process so the checksums always agree, and choose a `k` that removes the stalls. Compute the command delay you paid for it.

Expected output: the predicted and measured `T_eff`, the first turn where checksums disagreed and why, the fixed ordering rule, and the chosen `k` with its average delay.

## Common misconceptions

- **"Lockstep means everyone waits for the slowest player every frame."** Everyone waits only when a turn's commands are late. With `k` chosen so that `(k − 1)T ≥ L_max`, nobody waits. The price is a fixed command delay instead.
- **"Deterministic just means no random numbers."** Random numbers are fine if they are seeded and drawn identically. The usual culprits are floating-point order, iteration order and local-only state.
- **"Lockstep is always cheaper."** Its cost is flat in unit count, but it pays headers every turn to every peer. For a small number of units, state sync can cost less (Table 1).
- **"A checksum mismatch tells you the bug."** It tells you the turn when the states differed, which is often long after the line that caused it. You still need a diff of the two states and logs per system to find the cause.

## Check yourself

1. Four players, full mesh, `T = 250` ms, 1 command per player per second at 12 bytes. Header and turn field 32 bytes. Compute the lockstep upload per peer. Now compute state sync at `r = 4` updates per second with 10 bytes per unit for 400 units in total. Which is cheaper?
2. A game uses `T = 150`, `k = 2`. The worst one-way latency is 180 ms. What is `T_eff`, the average command delay, and how much slower does the game run than intended?
3. Two peers' checksums first differ at turn 812. The only difference in the state dump is one unit's health, 927 on one peer and 1000 on the other. List two causes from section 3 that could produce this, and what you would log next to tell them apart.
4. Why does Fiedler send every unacknowledged input in every packet instead of resending lost packets, and why is that affordable for lockstep inputs but not for snapshots?
5. Explain in two sentences why rollback suits a two-player fighting game and not an eight-player RTS.

<details>
<summary>Answers</summary>

1. Lockstep: `3 × (4 × 32 + 12 × 1) = 3 × 140 = 420` B/s. State sync: `3 × 4 × (32 + 10 × 100) = 12 × 1,032 = 12,384` B/s. Lockstep is cheaper by a factor of about 29.
2. `T_eff = max(150, (150 + 180) / 2) = 165` ms. Average delay `1.5 × 165 = 247.5` ms. The game runs `165 / 150 = 1.1` times slower, 10%.
3. A hit that one peer applied and the other did not, because a shared random draw happened on one peer only (a local-only effect drawing from the shared generator), so the "hit" roll differed. Or two commands applied in a different order, which changed who was in range. Log the shared generator's call count and the command list, as applied, for each turn on both peers. If the call counts diverge first, it is the generator.
4. Waiting for a resend stalls the simulation for at least a round trip, because frame `n` can't run without input `n`. Inputs are a few bits each, so repeating the last few dozen costs tens of bytes. Snapshots are hundreds of bytes each and old ones are useless, so repeating them would multiply the bandwidth for no benefit.
5. Rollback re-simulates several frames at once whenever a guess was wrong, which is cheap for two characters and a stage. An RTS simulation of hundreds of units already uses most of a frame's CPU, so re-running several frames in one is not affordable, and a 300 ms command delay is acceptable in that genre anyway.

</details>

## Lab / assignment hook

[Lab 12, lockstep timing and the desync hunt](../labs/lab12.md). Part A implements `execution_delay`, `simulate_turns` and a CRC-32 checksum and reproduces Table 2. Part B runs two peers on the same command script. They desync. You find the first bad turn from the checksums, diff the states, and fix every determinism bug in the starter without changing the game rules.

## Sources

- Bettner, P. & Terrano, M. (2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond." Gamasutra, 22 March 2001 (now Game Developer). Eight players, a 16 MB Pentium 90 and a 28.8 modem as targets; unit state would have limited them to about 250 moving units; latency swings of 20 to 1,000 ms; turns typically 200 ms with commands executed two turns later; speed control with 2 bytes per "turn done"; UDP with client-side ordering and resends; out-of-sync games stopped; the deer example and seeded random numbers; random terrain sounds; 50 MB traces; 250 ms unnoticed, 250 to 500 ms very playable, over 500 ms noticeable; consistent latency preferred to varying; recorded games in Age of Empires II; sync tags in the next engine.
- Fiedler, G. (2014). "Deterministic Lockstep." Gaffer on Games, 29 November 2014. Bandwidth proportional to input size; floating-point results can differ across compilers, operating systems, instruction sets and builds; 100 ms playout delay buffer; TCP hitches on loss; redundant unacknowledged inputs over UDP, 6-bit inputs, 120 inputs in 90 bytes.
- Wube Software, "Friday Facts #76: MP inside out" (factorio.com, 6 March 2015, multiplayer since version 0.11.0). Wube Software, "Friday Facts #58" (factorio.com), release of 0.11.0 with the first multiplayer on 31 October 2014. Lockstep sends only actions and scales from a hundred objects to a million; Age of Empires and StarCraft named as earlier users; desyncs; a slow machine slows everyone; the "latency" buffer that delays local actions.
- GGPO, README (GitHub, pond3r/ggpo, MIT License, accessed September 2026). Traditional netcode adds delay to input; rollback uses input prediction and speculative execution; offline timings and muscle memory carry over online.
- Python Software Foundation, *Python 3 documentation*, tutorial chapter "Floating-Point Arithmetic: Issues and Limitations" and the `PYTHONHASHSEED` entry under "Command line and environment" (accessed September 2026). Both outputs in section 3 were reproduced with Python 3.13; the set order changed between runs with different hash seeds.

## Interactive spec: examples/w12-lockstep-timeline.html

**Insight the visual must make obvious:** lockstep bandwidth is flat in unit count while state sync climbs through the budget, and lockstep's price is timing. Every command waits `k` turns, and one slow link stretches every player's turns to `(T + L_max) / k`.

**Layout.** Two views side by side on desktop, stacked under 700 px, plus a readout strip.

1. **Turn timeline** (left). Horizontal time axis 0 to 3,000 ms. One row per peer (2 to 8 peers, default 4, labelled A, B, C, D...). Each turn is a box from its start time to start + `T`, numbered. From the end of each turn on each peer, draw thin arrows to every other peer's row, arriving after the link's one-way latency plus jitter. When a peer's next turn starts later than `previous start + T`, shade the gap red and label it "stall N ms". A vertical marker shows a command issued at a clickable time; a second marker shows when it executes (start of turn `n + k`), with the delay labelled.
2. **Bandwidth chart** (right). x axis: units `N`, 0 to 2,000. y axis: upload bytes per second per peer, 0 to 25,000. Line 1, state sync `(P − 1) × r × (32 + s × N / P)`. Line 2, lockstep `(P − 1) × ((1000 / T) × 32 + b × c)`, flat. Horizontal budget line (default 3,600 B/s, "28.8 modem"). Mark the break-even point and the largest `N` state sync can afford.

**Controls.** Turn length `T` 50 to 400 ms, step 10, default 200. Depth `k` 1 to 5, default 2. Peers `P` 2 to 8, default 4 on the timeline (the bandwidth chart uses its own `P`, default 8). Latency of the worst link 0 to 600 ms, step 10, default 150 (all other links fixed at 40 ms; the worst link is between A and D, both directions). Jitter 0 to 100 ms, step 10, default 0, seeded (seed 12). Units `N` 0 to 2,000, step 10, default 1,500. Bytes per unit `s` 2 to 32, default 8. Updates per second `r` 1 to 20, default 2. Bytes per command `b` 4 to 32, default 8. Commands per player per second `c` 0 to 10, default 2. Budget preset buttons: "28.8 modem (3,600 B/s)", "1 Mbit/s (125,000 B/s)".

**Model.** Timeline: `start[0] = 0`; `start[n] = max(start[n−1] + T, max over ordered pairs (i, j), i ≠ j, of start[n−k] + T + latency[i][j] + jitter)` for `n ≥ k`, with jitter drawn from `U(0, J)` per message (matching `simulate_turns` in `labs/lab12-starter/lockstep.py`). All peers share the same start times. `T_eff` is the average turn length over the last 120 turns of a 241-turn run. Command delay for an issue time `t` in turn `n = floor(t / T)` on the nominal grid is `(n + k)T − t`; average `(k − ½)T_eff`.

**Readouts.** `T_eff`, slowdown `T_eff / T`, average and worst command delay, total stall in the visible window, state-sync and lockstep upload at the chosen `N`, break-even `N`, and the largest `N` under the budget.

**Test values** (assert on load). Bandwidth with `P = 8`, `r = 2`, `s = 8`, `T = 200`, `b = 8`, `c = 2`: lockstep 1,232 B/s; state sync 1,148, 1,232, 3,598, 3,948 and 21,448 B/s at `N` = 50, 56, 225, 250 and 1,500; break-even `N = 56`; largest `N` under 3,600 B/s is 225. Timing with 2 peers, `T = 200`, `k = 2`, no jitter: `T_eff` = 200, 200, 200, 225, 300 ms for worst latency 50, 150, 200, 250, 400; with `k = 3` and 400 ms, `T_eff = 200`. With jitter 60 and seed 12 the values should be close to 200.0, 201.2, 220.6, 244.9, 319.3 (exact values depend on the random generator; assert within 5 ms). Command delay with `T = 200`, `k = 2` for issue times 1000, 1150, 1199 ms: 400, 250, 201 ms.

**First screen:** four peers, worst link 250 ms, `k = 2`, red stall gaps visible on every row, bandwidth chart at `N = 1,500` with the state-sync point far above the modem line, and a caption: "Lockstep's bandwidth ignores the army. Its turns don't ignore the slowest link."
