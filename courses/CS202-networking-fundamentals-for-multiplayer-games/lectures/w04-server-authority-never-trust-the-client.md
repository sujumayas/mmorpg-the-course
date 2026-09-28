# CS202 · Week 04 — Server authority: never trust the client

**Why this matters:** Every multiplayer game ships two programs, a client you control and a server your players control nothing of. Anything the client decides, a player with a memory editor or a modified client can decide instead. This week you learn to move every decision that matters to the server, and to put a number on how much any leftover trust gives away.

**You will be able to:**
- Rewrite a client-to-server protocol so the client sends intent (inputs, requests) and the server computes every result.
- Compute the tolerance a server speed check needs to survive a given jitter, and the permanent speed that tolerance hands a cheater.
- Size a per-tick command budget from jitter and packet rate, and compute the largest burst a lag-switching client can get through it.
- Write a validation checklist (range, rate, state, ownership, reach) for any client message.

**Before class:** Gabriel Gambetta, *Fast-Paced Multiplayer*, part I, "Client-Server Game Architecture" (reread it; this week turns its first rule into numbers). Frohnmayer, M. & Gift, T. (2000), "The TRIBES Engine Networking Model", the overview and the "Move Stream Manager" section (about 10 minutes).

**Prerequisites from earlier courses:** [CS102 week 12, the command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (an input as a command object is exactly what a client should send). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (speed times time step, which a server must check). [CS202 week 2](w02-latency-jitter-loss-measure-your-own.md) (jitter, and why packets bunch up) and [week 3](w03-topologies-peer-to-peer-client-server-relay.md) (topology is separate from authority).

**Interactive:** [examples/w04-movement-validator.html](../examples/w04-movement-validator.html). Keep it open during section 2.

---

## 1. Who decides what is true

Last week separated two decisions. Topology says where packets go. **Authority** says which machine decides what happened. When two machines disagree about whether a shot hit, where a player stands or how much gold is in a bag, the authority's answer wins and everyone else corrects to it.

The **trust boundary** is the line between code you control and code you do not. Your server runs in a data center. Your client runs on a machine the player owns. The player can read and change its memory, replace its code, and send any bytes they like to your server's port. So treat every byte that arrives from a client as a claim, never as a fact. Gambetta states the rule in four words. Don't trust the player.

In practice the rule becomes one design habit. **Clients send intent. Servers compute results.**

| Client-authoritative (do not ship) | Server-authoritative |
|---|---|
| "I am now at (412.0, 88.5)." | "This tick I pressed forward and strafe left, facing 271 degrees." |
| "I hit player 7 for 500 damage." | "I pressed fire at tick 9,104 with this aim." |
| "I picked up the Sword of Ages." | "I request to pick up item 55,021." |
| "My health is 100." | Nothing. The client never reports health. |
| "I bought 20 potions and have 900 gold left." | "I request to buy 20 of item 17 from vendor 3." |

Look at the right-hand column. Every message is something the player really did choose (a key, a click, a menu option). The server checks whether it is allowed, runs the game rules, and tells the client what happened. A hacked client can still send any intent it likes, but intent is small and easy to check. "Press forward" can only mean moving at the game's speed. "I am at (412, 88)" can mean anything.

### What a command looks like

An input message is a command object in the sense of CS102 week 12. It is small, it describes one tick of player intent, and the server can run it. Valve's Source engine calls it a user command. In the Source SDK 2013 code it holds a command number, a tick count, the view angles, three movement amounts (forward, side, up), a bitmask of pressed buttons, a weapon selection and a random seed. There is no position and no health in it. The server runs each command through the same movement code the client uses and gets the position itself.

*Starsiege: Tribes* (1998) took the same approach. Its client collected a "move" every 32 ms, holding translations, rotations and trigger states, and the Tribes networking paper says moves were the only way a player controlled their object. The server simulated the moves. The client never announced where it was.

A minimal command in Python, packed with week 1's `struct`:

```python
import struct

CMD = struct.Struct("!IhhbbB")     # tick, yaw*100, pitch*100, forward, side, buttons
def pack_cmd(tick, yaw, pitch, fwd, side, buttons):
    return CMD.pack(tick, round(yaw * 100), round(pitch * 100), fwd, side, buttons)
```

That is 11 bytes of payload per tick, and next week you will squeeze it further. For now, notice what the server must do with `fwd` and `side`. They are signed bytes, so a client can send 127 when the game expects -1, 0 or 1. The server must clamp them. Section 3 comes back to that.

### The price of authority

If the server decides where you are, your own character cannot move until your input has crossed the network and the answer has come back. At 100 ms RTT that is a tenth of a second of mush after every key press. No action game ships that way. The fix is **client-side prediction** (week 8). The client runs the same rules on its own input and shows the result at once, then accepts the server's correction if it disagrees (week 9, reconciliation). Prediction is a display trick. The server's answer still wins. Keep that order in mind whenever someone suggests "just let the client decide, it feels better." It feels better because prediction already makes it feel better, without giving up authority.

## 2. Worked example: how much speed does a movement check give away?

### The hook

*Diablo* (1996) put its multiplayer on Blizzard's new Battle.net service. Battle.net stored account data and nothing else. Each player's character lived in a file on their own hard drive, and the game trusted it when they joined a game. Cheating spread fast, because a player with an editor could give their character any stats and items they wanted. For *Diablo II* (2000), Blizzard split Battle.net into open and closed realms. Closed-realm characters were stored on Blizzard's servers as a measure against cheating. Open realms still accepted characters from players' hard drives, and stayed open to the same abuse.

That is authority over the *save file*. The same fight happens inside a single match, sixty times a second. Even a server that simulates everything must accept the client's inputs, and inputs arrive over a network with jitter. A speed hack is a client that sends movement faster than real time allows. The server has to tell a cheater apart from an honest player whose packets arrived in a bunch. How much can the cheater get away with? The answer depends entirely on which check you write.

### The model

The client runs at 60 ticks per second, so one tick is `T = 16.7 ms`. Each tick it makes one movement command worth at most one **step** of `s = 0.1 m` (a run speed of 6 m/s). It sends a packet every 3 ticks, so every `Δ = 50 ms`. Packets take a constant 50 ms, and **jitter** delays some of them by an extra `J` ms. To keep the numbers checkable by hand, every fourth packet is late by exactly `J`.

**Policy A, a speed check with tolerance.** The client reports how far it moved since its last packet. The server compares that with the time since the last packet arrived:

```
accept if   distance ≤ v × gap × (1 + tol)
```

- `v` is the run speed, 6 m/s.
- `gap` is the time between this packet's arrival and the previous one's.
- `tol` is the tolerance, a fraction (0.25 means 25% extra is allowed).

A late packet is followed by one that arrives only `Δ − J` after it, still claiming a full `Δ` of movement. For the honest player to pass, `v × Δ ≤ v × (Δ − J) × (1 + tol)`, which gives

```
tol_min = J / (Δ − J)
```

A cheater whose packets arrive on time can then claim `(1 + tol)` times the real speed on every packet, forever. The cheater's lead over an honest player after `t` seconds is `v × tol × t`.

**Policy B, a tick budget.** The client sends commands, never distances. The server keeps a **credit** counter for each client. Every server tick, it adds one credit, up to a cap `B`, the **budget**. It runs one queued command per credit and drops whatever commands are left. A client can never run more commands than ticks have passed, plus at most `B` saved up. The honest player's commands come 3 to a packet, and a packet that arrives `J` ms late misses `⌈J / T⌉` ticks, so the credit must cover both:

```
B_min = 3 + ⌈J / T⌉
```

Over any stretch of time, the most commands a client can run is the number of ticks that passed plus `B`. So a speed hack gains nothing on average. Whatever the hack's multiplier, the cheater's position stays within about `B − 3` steps of the honest player's.

### Numbers you can check

Ten seconds of play (200 packets, 600 commands). The policy B column shows the lead of a cheater running at double speed. Lab 04's `movement_check.py --table` prints exactly this.

| Jitter `J` | `tol_min` | Cheater speed under A | Cheater lead after 10 s, A | `B_min` | Budget window `B × T` | Cheater lead after 10 s, B |
|---|---|---|---|---|---|---|
| 0 ms | 0% | 6.0 m/s | 0 m | 3 | 50 ms | 0 m |
| 10 ms | 25% | 7.5 m/s | 15 m | 4 | 67 ms | 0.1 m |
| 20 ms | 66.7% | 10.0 m/s | 40 m | 5 | 83 ms | 0.2 m |
| 30 ms | 150% | 15.0 m/s | 90 m | 5 | 83 ms | 0.2 m |
| 40 ms | 400% | 30.0 m/s | 240 m | 6 | 100 ms | 0.3 m |

Check the 20 ms row by hand. Packet 1 is sent at 100 ms and arrives at 170 ms instead of 150. Packet 2 arrives on time at 200 ms, only 30 ms later, claiming 0.3 m. The check allows `6 × 0.030 × (1 + tol)`, which equals 0.3 only when `1 + tol = 1.667`. So `tol_min = 20 / 30 = 66.7%`. A cheater at 1.667 times 6 m/s runs at 10 m/s and gains 4 m every second, 40 m in ten. Under policy B, packet 1 would have been processed at the server tick at 150 ms. Arriving at 170, it waits for the tick at 183.3, two ticks later, so `B_min = 3 + 2 = 5`.

Now look down the columns. Under policy A, the tolerance has to grow like `J / (Δ − J)`. It explodes as jitter approaches the packet interval, and every point of tolerance is a permanent speed boost for anyone who wants it. Under policy B, the budget grows by one tick for every 16.7 ms of jitter, and the cheater's gain stays below half a metre whatever the jitter.

What if you set the budget too tight? With `J = 20 ms` the honest player needs `B = 5`.

| Budget `B` | Honest commands dropped in 10 s | Share of movement lost |
|---|---|---|
| 3 | 100 of 600 | 16.7% |
| 4 | 50 of 600 | 8.3% |
| 5 | 0 | 0% |

Each dropped command is a step the honest player's client predicted and the server never ran. In week 9 you will see what that looks like on screen. The client gets pulled backwards, which players call **rubber-banding**. A too-tight check punishes honest players on bad connections. That is the real failure mode of anti-cheat code, and it is why policy A's designers keep raising the tolerance.

### The lag switch

A cheater under policy B has one move left. Stop sending for a while, let the credit build up, then send everything at once. That is a **lag switch**. Suppose the cheater holds 6 packets (300 ms, 18 commands), then releases them together with the next packet, 21 commands in all.

| Budget `B` | Commands run in one tick | Jump in that tick | Commands dropped |
|---|---|---|---|
| 5 | 5 | 0.5 m | 16 |
| 24 | 21 | 2.1 m | 0 |

With `B = 5`, the burst is capped at half a metre and the cheater loses 1.6 m of movement for the trouble. With `B = 24`, the cheater vanishes and reappears 2.1 m away within one tick. That is the trade you set with `B`. A big budget forgives honest lag spikes and lets lag switches teleport. A small budget stops teleports and rubber-bands honest players on bad Wi-Fi.

### Move it yourself

Open `examples/w04-movement-validator.html`. The left plot shows server-accepted position over ten seconds for an honest player and a cheater. The right plot shows the cheater's lead as you drag the jitter slider, with one line for policy A (a cheater using all of the tolerance that jitter forces, `1 + tol` times normal speed) and one for policy B (a 2× cheater at the budget that jitter forces). The left plot's cheater uses the multiplier slider, capped at `1 + tol`, so at 40 ms of jitter a 2× cheater there gains 60 m while the right plot shows the 240 m that a 5× cheater could take. At the default 20 ms, policy A's line is at 40 m and policy B's at 0.2 m. Drag jitter to 40 ms and watch policy A's line leave the chart. Then switch the cheater to "lag switch," set the budget to 24, and watch the jump appear on the left.

### Same idea elsewhere

**Source engine (Source SDK 2013 code, current on GitHub).** The server gives each player one tick of credit per server tick, in a counter named `m_nMovementTicksForUserCmdProcessingRemaining`, and caps it with the setting `sv_maxusrcmdprocessticks`, default 24. When a client sends more commands than it has credit for, the server runs only as many as the credit allows. A comment in the code says the goal is to stop players manipulating game time by more than about a quarter of a second, and admits that tighter limits caused unacceptable hitching for honest players. That is policy B exactly, with `B = 24`. At Source's default 15 ms tick, 24 ticks is 360 ms, which lets a lag switch through the 2.1 m row of our table in exchange for never rubber-banding anyone on a 300 ms spike.

**Starsiege: Tribes (1998) and Tribes 2 (2001).** The server tracked moves in a sliding window. The client could only run ahead of the server by the size of that window, and if the window filled, the client's simulation stopped until the server caught up. That is a budget seen from the other side. The client may not predict more than `B` moves the server has not accepted.

**Minecraft: Java Edition (server.properties, current).** A server with `allow-flight=false` kicks a survival-mode player who stays in the air for at least 5 seconds. That is policy A with time as the tolerance. An editor's note on the Minecraft Wiki reports that a player can fly anyway by dropping a little every few seconds, which resets the check. Any fixed tolerance is a free allowance for anyone willing to stay just under it.

**Diablo and Diablo II (1996, 2000).** The same question at a larger scale. How much of the game state does the client own? In *Diablo*, all of the character. In *Diablo II* closed realms, none of it. Blizzard moved the character file across the trust boundary, which is what this whole lecture asks you to do with every field.

Four systems, one model. For any check, ask two questions. How much slack does an honest player need? And what does that slack give a cheater, once, or every second forever?

### Design judgment

- **Prefer checks that bound totals over checks that bound rates.** A rate tolerance (policy A) is a permanent gift. A budget on totals (policy B) turns the same slack into a one-off burst. The same idea applies to cooldowns, resource gathering and chat spam, as a credit that refills with time and has a cap.
- **Size the slack from measured jitter, not from a guess.** Week 2's tools give you the 99th-percentile delay spread for real players. Set `B` to cover that, then look at what the resulting burst lets a lag switch do. Source chose 360 ms of forgiveness. A competitive shooter might choose less, a casual co-op game more.
- **Do not trust client timestamps to fix policy A.** A tempting fix is to check distance against the time the client says it sent the packet, so jitter no longer matters. But a speed hack works by lying about time. Server-side ticks are the only clock the cheater cannot touch.
- **Detection and prevention are different jobs.** Policy B prevents. It never needs to decide who is cheating. When you must detect (to ban), log the evidence (dropped-command counts, lag-switch bursts) and decide offline over many matches. MMO309 weeks [2](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w02-never-trust-the-client.md) and [3](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w03-speed-hacks-and-movement-validation.md) build that side.
- **Budget for false positives.** Every check you add will fire on some honest player somewhere. Count them in your tests the way Lab 04 counts dropped commands, and decide how many you accept.

### Check this example

1. Packets every 33.3 ms (30 Hz), jitter 15 ms. What tolerance does policy A need? How far ahead is a cheater after one minute at 6 m/s?
2. Same game at a 60 Hz server tick, 2 commands per packet, jitter 15 ms. What is `B_min`?
3. A designer sets `B = 60` "to be safe." Using the lag-switch model at 0.1 m per command, what is the largest single-tick jump a cheater can make?

<details>
<summary>Answers</summary>

1. `tol_min = 15 / (33.3 − 15) = 0.82`, so 82%. The cheater runs at `6 × 1.82 = 10.9 m/s`, gaining `6 × 0.82 = 4.9 m` every second, about 295 m in a minute.
2. A 15 ms delay misses `⌈15 / 16.7⌉ = 1` tick, so `B_min = 2 + 1 = 3`.
3. 60 commands in one tick, `60 × 0.1 = 6 m`, the length of a whole second of running. At a 60 Hz tick, that is a full second of saved movement released at once.

</details>

## 3. Validating everything else

Movement is the hardest case because it arrives every tick. Every other message gets the same treatment, one check at a time. For each message type, write down five checks.

| Check | Question | Example |
|---|---|---|
| **Range** | Is every field inside its legal values? | `forward` must be -1, 0 or 1. Pitch within ±89 degrees. Item count 1 to 99. |
| **Rate** | Is the player sending this more often than possible? | At most one fire command per weapon cooldown, one trade request per second. |
| **State** | Is the action legal right now? | Cannot cast while stunned, cannot loot while dead, cannot buy with too little gold. |
| **Ownership** | Does this player own the thing named? | The item ID in "sell item 55,021" belongs to the sender. |
| **Reach** | Is the target close enough? | The chest is within 2 m, the vendor is within 5 m. |

Two range bugs are worth memorizing because they appear in shipped games again and again.

**The unnormalized diagonal.** If the server accepts `forward = 1, side = 1` and moves the player by `(1, 1) × step`, a diagonal move covers `√2 × step`, 41% faster than straight. Honest clients may have the bug too. Normalize the input vector on the server, `if |m| > 1 then m = m / |m|`, and the problem disappears.

**The trusted count.** A message like "sell 5 potions" has a count field. A signed 16-bit field can hold -5. If the server computes `gold += price × count` and `potions -= count`, a player who sells -5 potions gains 5 potions and pays for them with negative gold. Check the sign and the upper limit before you do any arithmetic. This family of bugs, where the server does what the client said with a number it never checked, is behind many item duplication exploits. [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) studies them.

### Malformed packets

A hostile client does not have to send well-formed messages at all. It can send a length field that says 60,000 in a 20-byte packet, or an enum value your code has never seen. Parse every packet as if it were written by an attacker. Check every length against the bytes actually present, reject unknown values, and never let a parse error crash the server process. Next week's bit reader is built that way from the start, and its lab throws random bytes at it to prove it.

## 4. Where games bend the rule

Full authority is the goal. Shipped games bend it in three known places, and each bend is a decision with a cost.

- **Hit detection with lag compensation.** In most shooters the server rewinds other players to where the shooter saw them, then checks the shot (week 11). That trusts the client's claim about *when* it fired, within a limit, to make aiming at a moving target work at 100 ms of latency. The limit is a budget, the same idea as policy B.
- **Cosmetic and local effects.** Particle effects, ragdolls, camera shake and sound can run entirely on the client. If a cheater changes them, they only fool themselves. Trust anything that does not affect other players or the game's record.
- **Peer-to-peer games.** In week 3's mesh, some player's machine must be the authority, or all must agree. Deterministic lockstep (week 12) has every peer run the same simulation from the same commands, so a peer who changes their own result simply desyncs. That detects cheating after the fact rather than preventing it.

For an MMO the rule is stricter, not looser. Persistent state (items, gold, experience) outlives the match, and a single duplicated item can crash a whole economy's prices. [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) designs the server side of simulation authority.

## In-class activity (25 minutes)

Pairs. You receive the message list of a small online game written by someone who never heard of server authority. It has eight client-to-server messages, including `SET_POSITION x y`, `DEAL_DAMAGE target amount`, `LOOT item_id`, `SELL item_id count price` and `SET_HEALTH hp`.

1. For each message, say what a modified client could do with it, in one line.
2. Rewrite each one as intent. Some messages disappear entirely.
3. For each rewritten message, fill in the five checks from section 3.
4. For movement, choose policy A or policy B, and give its parameter for a game that measured 25 ms of 99th-percentile jitter at 20 packets per second and a 60 Hz tick. Compute what a cheater gains under your choice.

Expected output: the rewritten protocol table with checks, and one number for the cheater's gain with the formula that produced it.

## Common misconceptions

- **"We encrypt our packets, so clients can't cheat."** Encryption stops a third party from reading or changing traffic. The player owns the client that does the encrypting, so they can change what it says before it is encrypted.
- **"The server simulates, so speed hacks are impossible."** The server still has to accept inputs at some rate. Section 2 shows a simulating server that still gives away 40 m in ten seconds with a rate tolerance.
- **"A tighter check is a safer check."** A tighter check drops honest commands and rubber-bands players on bad connections. Pick the slack from measured jitter and count the false positives.
- **"Client-side prediction means the client is authoritative."** Prediction is a guess the server overrules. The client shows its guess. The server's answer is the one that counts.

## Check yourself

1. Rewrite `ATTACK target_id damage` as intent, and list the checks the server must run on the new message.
2. A game sends packets every 50 ms. The honest 99th-percentile jitter is 35 ms. Compute policy A's `tol_min` and the cheater's speed at a base of 5 m/s. Is policy A usable here?
3. Under policy B with a 64 Hz tick and 4 commands per packet, jitter 20 ms. Find `B_min` and the largest lag-switch jump if one command moves 0.08 m.
4. A client sends `forward = 1, side = 1` and the server does not normalize. At a run speed of 6 m/s, how fast does the player move diagonally?
5. Explain why checking movement against the client's own send timestamps does not stop a speed hack.

<details>
<summary>Answers</summary>

1. Send `FIRE tick aim_angles` or `USE_ABILITY ability_id target_id`. Checks: range (the ability ID exists, the target ID exists), rate (the ability is off cooldown on the server's clock), state (the attacker is alive and not stunned), ownership (the attacker knows the ability), reach (target within the ability's range and, for a projectile, in line of sight). The server computes damage.
2. `tol_min = 35 / (50 − 35) = 2.33`, or 233%. The cheater runs at `5 × 3.33 = 16.7 m/s`. No. A tolerance that lets anyone move three times faster is not a check.
3. The tick is 15.6 ms. A 20 ms delay misses `⌈20 / 15.6⌉ = 2` ticks, so `B_min = 4 + 2 = 6`. The largest burst is 6 commands, `6 × 0.08 = 0.48 m`.
4. `√2 × 6 = 8.49 m/s`, 41% faster.
5. The cheat works by making the client's clock run fast. Its timestamps say the right amount of time passed for the distance claimed. Only a clock the server keeps, its own ticks, cannot be sped up by the client.

</details>

## Lab / assignment hook

[Lab 04, policing movement](../labs/lab04.md). You implement both policies in `movement_check.py`, reproduce the table in section 2, find the budget that stops a lag switch without rubber-banding a player with your own measured jitter from Lab 02, and audit a flawed game protocol. Deliverable: your code, the outputs, and a one-page protocol rewrite with a validation table.

## Sources

- Wikipedia, "Battle.net" (accessed September 2026). The original service (launched with *Diablo*, January 1997) stored only account data, so *Diablo* players could modify their game data locally, which led to widespread cheating. Wikipedia, "Diablo II" (accessed September 2026). Open and closed realms. Closed-realm characters stored on Blizzard's servers as a measure against cheating. Open-realm characters stored on players' own drives.
- Valve, Source SDK 2013, `src/game/server/player.cpp` (GitHub, ValveSoftware/source-sdk-2013, master, accessed September 2026). `sv_maxusrcmdprocessticks` default 24. One tick of credit per server tick in `m_nMovementTicksForUserCmdProcessingRemaining`. The code comment on limiting game-time manipulation to about 0.25 s and on hitching for legitimate users. `src/game/shared/usercmd.h`. Fields of a user command.
- Valve Developer Community, "Source Multiplayer Networking" (archived copy, 2024). Default server tick of 15 ms.
- Frohnmayer, M. & Gift, T. (2000). "The TRIBES Engine Networking Model." Dynamix. Moves collected every 32 ms and used as the only means of player-controlled movement. The sliding window of outstanding moves that halts the client when full.
- Minecraft Wiki, "Server.properties" (accessed September 2026, Java Edition). `allow-flight=false` kicks players in the air for at least 5 seconds. The wiki's note that descending a little every few seconds avoids the kick.
- Gambetta, G. *Fast-Paced Multiplayer*, part I, "Client-Server Game Architecture" (gabrielgambetta.com). Don't trust the player. Clients send inputs and the server sends back state.

## Interactive spec: examples/w04-movement-validator.html

**Insight the visual must make obvious:** a percentage speed tolerance is a permanent speed boost for a cheater that grows without limit as jitter rises, while a per-tick command budget caps the cheater's gain at a few steps whatever the jitter. The budget's only leak is a single burst (lag switch), whose size is exactly `B` steps.

**Layout.** Two linked plots and a number panel. Left: position over time. Right: cheater lead against jitter. On screens under 700 px wide, stack left plot, right plot, numbers. No page-level horizontal scroll.

1. **Left plot, "Server-accepted position".** x axis time 0 to 10 s, y axis metres. Two lines, honest (solid) and cheater (dashed), for the selected policy. Rejected packets (policy A) or dropped commands (policy B) are marked as small ticks under the x axis, honest in one color and cheater in another. In lag-switch mode, draw the burst as a vertical jump and label it with its size in metres.
2. **Right plot, "Cheater lead after 10 s vs jitter".** x axis jitter 0 to 45 ms, y axis lead in metres on a log scale from 0.05 to 1,000 m. Line A uses `tol = tol_min(J)` and a cheater at the full `1 + tol` multiplier, the most policy A accepts, independent of the multiplier slider. Line B uses `B = B_min(J)` and a 2× speed hack. A vertical marker at the current jitter, with both values printed beside it.
3. **Number panel.** `Δ`, `T`, `tol` in use, `B` in use, honest flags or drops, cheater flags or drops, honest final position, cheater final position, cheater lead, largest single-tick jump.

**Controls.**
- Policy radio: "A: speed check" (default) or "B: tick budget".
- Jitter slider `J`, 0 to 45 ms, step 1, default 20.
- Tolerance slider for policy A, 0 to 500%, with a button "Set to minimum for this jitter" (default on, which keeps it at `tol_min(J)` as `J` moves).
- Budget stepper for policy B, 1 to 60, with the same "Set to minimum" toggle (default on).
- Cheat radio: "Speed hack" with a multiplier slider 1.0 to 3.0, default 2.0 (under policy A the cheater automatically uses `min(multiplier, 1 + tol)`), or "Lag switch" (holds packets 40 to 45 and releases them with packet 46).
- All controls reachable by Tab, with visible focus.

**Formulas (match `labs/lab04-starter/movement_check.py`).** `T = 1000/60`, `s = 0.1`, `v = 6`, 3 commands per packet, `Δ = 50`, latency 50, 200 packets. Arrival of packet `k`: `(k + 1)Δ + 50 + (J if k mod 4 = 1 else 0)`. Policy A: accept packet `k` if `d_k ≤ v × gap_k / 1000 × (1 + tol) + 1e-9`, with `gap_0 = Δ`. Honest `d_k = 0.3`. Cheater arrives with `J = 0` and claims `0.3 × min(m, 1 + tol)`. `tol_min = J / (Δ − J)`. Policy B: at each tick `i = 1..⌊(200Δ + 110)/T⌋`, time `iT`, add arrived packets' commands to a queue, `credit = min(B, credit + 1)`, run `min(credit, queue)`, drop the rest. Credit starts at 0. Honest sends 3 commands per packet, cheater `round(3m)`. `B_min(J)` is the smallest `B` with zero honest drops.

**Test values** (assert on load):
- `J = 20`: `tol_min = 0.667`, cheater lead under A 40.0 m. `B_min = 5`, 2× cheater lead under B 0.2 m.
- `J = 40`: `tol_min = 4.0`, right-plot line A lead 240.0 m (cheater at `1 + tol = 5×`). `B_min = 6`, 2× cheater lead under B 0.3 m.
- `J = 40`, multiplier 2.0, policy A: left-plot cheater lead 60.0 m.
- `J = 20`, `B = 3`: 100 honest commands dropped. `B = 4`: 50.
- `J = 20`, `tol = 0.5`: 50 honest packets flagged.
- Lag switch, `J = 0`: `B = 5` gives a 0.5 m jump and 16 dropped. `B = 24` gives a 2.1 m jump and 0 dropped.

**First screen:** policy A at `J = 20` with both lines on the left plot diverging to a 40 m gap, and the right plot showing line A at 40 m against line B at 0.2 m. Caption: "Same jitter. A speed tolerance gives the cheater 40 m. A tick budget gives 0.2 m."
