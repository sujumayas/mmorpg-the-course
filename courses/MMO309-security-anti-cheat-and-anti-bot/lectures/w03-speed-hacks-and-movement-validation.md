# MMO309 · Week 03 — Speed hacks and movement validation

**Why this matters:** Movement is the one claim every client makes twenty or more times a second, over a network that delivers packets late and in bunches. A movement check that is too loose hands cheaters free speed. One that is too tight drags honest players backwards on bad Wi-Fi, and a detector built on it bans innocent people. This week you learn to set the tolerance with numbers and to turn violations into ban decisions you can defend.

**You will be able to:**
- Compute the tolerance a per-tick distance check needs to survive a given lag spike, and the speed that tolerance gives a cheater.
- Design a server-time credit check with a lag tolerance `L`, and compute the largest jump it allows and the distance it takes from an honest player.
- Compute false-positive rate, recall and precision for a "flag after `k` violations" rule at a given cheater base rate.
- Argue, with numbers, for flagging on one session's evidence or waiting for a week of it.

**Before class:** Hoglund & McGraw (2007), *Exploiting Online Games*, chapter 5, section "Pathing Bugs in Games" (pp. 104-107). Reread section 2 of [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (the speed-check tolerance and the tick budget) and section 2 of [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) (per-packet, sliding-window and token-bucket checks). This lecture builds on both instead of repeating them.

**Prerequisites from earlier courses:** [MMO302 week 6, simulation authority and anti-cheat by design](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) (the sustained speed factor and the blink of three check shapes, and "correct, don't convict"). [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (policy A, policy B and the lag switch). [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 9, server reconciliation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md) (what a correction looks like on the player's screen). [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) and [week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (counting rare events, and false positives). [Week 1](w01-threat-modeling-for-games.md) and [week 2](w02-never-trust-the-client.md) of this course.

**Interactive:** [the lag-tolerant movement check](../examples/w03-lag-tolerant-movement-check.html). Keep it open during section 2.

---

## 1. Why MMOs accept position claims at all

CS202 week 4 taught the clean design. The client sends inputs ("forward, strafe left"), the server runs them through its own movement code, and a speed hack has nothing to claim. Many shipped games do not work that way for player movement. The client simulates its own character and sends the server its new position, and the server checks the claim.

There are real reasons for this.

- **Server cost.** Running full physics for every player's every input, with collision against the world, is the most expensive thing a game server does. An MMO zone with hundreds of players may not afford it at the tick rate the client uses.
- **Feel.** A client that owns its own movement never gets corrected when it agrees with itself. Players on high ping feel no rubber-banding from server disagreements they did not cause.
- **History.** Engines and games built before prediction was common kept their protocols.

*Minecraft: Java Edition* is the clearest public example, because its server code is widely studied. The client sends position packets, and the server compares each claim with where the player was and decides whether to accept it. *Minecraft: Bedrock Edition* offers both models through a server setting, with client-authoritative movement as one choice and server-authoritative movement, with or without rewind, as the others.

So a movement check on a position claim is a design you will meet and may have to ship. MMO302 week 6 already compared the shapes such a check can take, and showed that a token bucket turns lag tolerance into a one-off blink while a per-packet check turns it into a speed multiplier. This week keeps that result and asks two new questions. How much tolerance does a measured lag spike force on you, tick by tick on a real server loop? And once the check has clamped a claim, when does a pile of violations become evidence against a player?

### What a speed hack is, from the server

A **speed hack** is any client change that makes the character cover more ground per second than the rules allow. From the server's side it has only a few forms, whatever the tool does inside the client:

- **Steady speed.** Every claim is a little too far, say 1.3 times the legal step.
- **Teleport or blink.** An occasional claim far beyond one step.
- **Freeze and jump.** No claims for a while (the character stands still on everyone else's screen), then a claim that catches up. This is the lag switch from CS202 week 4.
- **Time manipulation.** The client's clock runs fast, so it sends legal-looking steps more often than real time allows.

A **fly hack** and **noclip** (walking through walls) are relatives. They claim positions that are legal in distance but illegal in physics. Section 3 covers them.

## 2. Worked example: a max-distance-per-tick check with lag tolerance

### The hook

A sprinting *Minecraft* player moves about 5.6 blocks per second, or 0.28 blocks per server tick at 20 ticks per second. Now read the vanilla server's movement check in *Minecraft: Java Edition* (version 26.3, 2026). For each position packet, the server takes the squared distance the player claims to have moved since the start of the tick, subtracts the square of the player's current velocity, and compares the result with 100 for each packet received that tick (300 while gliding with an elytra). If the claim is larger, the server logs "moved too quickly" and puts the player back where they were.

A squared distance of 100 is 10 blocks. The server lets one packet move a player about 35 times as far as a sprinting player moves in one tick, before it complains. That is not a speed check. It is a teleport guard. Anything slower than a 10-block jump per packet passes this check.

Why would a shipped game use such a loose check? Because every tighter check punishes honest players. Packets arrive in bunches after a lag spike, knockback and explosions launch players, and the server's idea of the player's speed is always a network trip out of date. This worked example shows exactly what tightening costs, and a better shape for the check.

### The model

A server tick lasts `T = 50 ms`. The legal speed is `v = 6 m/s`, so one tick's legal step is `s = v × T = 0.3 m`. The honest client sends its position once per tick, and packets take 40 ms to arrive. A **lag spike** of length `J` holds every packet sent during the spike, then releases them together. The server handles the packets that arrived since the last tick, takes the newest claimed position, and measures `d`, the distance from the last position it accepted.

**The rate check.** Accept if the distance claimed in one tick is at most one step plus a tolerance:

```
accept if d ≤ s × (1 + tol)
```

After a spike of `J` ms, `J / T + 1` steps arrive in one tick, so an honest player passes only if

```
tol ≥ J / T
```

Any tolerance is available to every client all the time. A cheater can claim `(1 + tol)` times the legal speed on every tick without a single violation.

This is the per-tick relative of MMO302's per-packet check. It judges each server tick alone, with no memory of earlier ticks.

**The credit check.** MMO302's token bucket, written in time instead of metres. Measure the time since the last accepted claim on the server's own clock, and allow the distance that time permits, capped at one tick plus a **lag tolerance** `L`:

```
accept if d ≤ v × min(t_now − t_last_accept, T + L)
```

- `t_now` and `t_last_accept` are server times. The client's clock is never used.
- `L` is how long a gap in the client's packets the server will forgive in one step.

After a spike of `J` ms, the server has not accepted anything for `J + T`, and the honest player claims `v × (J + T)`. It passes if `J ≤ L`. A steady-speed cheater gains nothing, because each tick allows exactly one tick of distance. The only thing `L` gives away is the **largest single jump**, `v × (T + L)`, and with it the longest a freeze-and-jump cheater can stand frozen on other screens without a violation.

When a claim fails either check, the server accepts only the allowed distance and sends a correction. Our model assumes the client snaps back at once. The distance the honest player loses is `d − allowed`, which is what the player sees as rubber-banding. In a real game the correction takes a round trip, which CS202 week 9 handles.

### Numbers you can check

This script simulates one honest player through one lag spike under both checks and finds the smallest setting that produces no violation.

```python
TICK_MS, SPEED, LATENCY_MS = 50, 6.0, 40
STEP = SPEED * TICK_MS / 1000            # 0.3 m per tick

def run(spike_ms, check, param, ticks=60, spike_start=1000):
    """Honest client, one position per tick, one lag spike. Returns (violations, metres pulled back)."""
    arrivals = []
    for k in range(ticks):
        sent = k * TICK_MS
        held = spike_start <= sent < spike_start + spike_ms
        arrivals.append(((spike_start + spike_ms if held else sent) + LATENCY_MS, (k + 1) * STEP))
    accepted, last_ok, violations, pulled = 0.0, 0, 0, 0.0
    for i in range(1, ticks + 3):
        now = i * TICK_MS
        batch = [pos for t, pos in arrivals if now - TICK_MS < t <= now]
        if not batch:
            continue
        d = batch[-1] - pulled - accepted      # the client snapped back by `pulled` metres
        if check == "rate":                    # fixed tolerance on each tick's distance
            allowed = STEP * (1 + param)
        else:                                  # "credit": server time since last accept, capped at T + L
            allowed = SPEED * min(now - last_ok, TICK_MS + param) / 1000
        if d > allowed + 1e-9:
            violations += 1
            pulled += d - allowed
            d = allowed
        accepted, last_ok = accepted + d, now
    return violations, pulled

for J in (50, 100, 250, 500):
    tol = next(t / 100 for t in range(0, 2001, 10) if run(J, "rate", t / 100)[0] == 0)
    L = next(l for l in range(0, 1001, 10) if run(J, "credit", l)[0] == 0)
    print(f"spike {J:3} ms | rate: tol {tol:5.0%}, cheater {SPEED * (1 + tol):2.0f} m/s"
          f" | credit: L {L:3} ms, largest jump {SPEED * (TICK_MS + L) / 1000:.1f} m")
v, m = run(500, "credit", 250)
print(f"spike 500 ms, L = 250 ms: {v} violation, honest player pulled back {m:.1f} m")
```

Output:

```
spike  50 ms | rate: tol  100%, cheater 12 m/s | credit: L  50 ms, largest jump 0.6 m
spike 100 ms | rate: tol  200%, cheater 18 m/s | credit: L 100 ms, largest jump 0.9 m
spike 250 ms | rate: tol  500%, cheater 36 m/s | credit: L 250 ms, largest jump 1.8 m
spike 500 ms | rate: tol 1000%, cheater 66 m/s | credit: L 500 ms, largest jump 3.3 m
spike 500 ms, L = 250 ms: 1 violation, honest player pulled back 1.5 m
```

As a table:

| Spike `J` to forgive | Rate check: `tol` needed | Cheater's free speed | Credit check: `L` needed | Largest jump allowed |
|---|---|---|---|---|
| 50 ms | 100% | 12 m/s | 50 ms | 0.6 m |
| 100 ms | 200% | 18 m/s | 100 ms | 0.9 m |
| 250 ms | 500% | 36 m/s | 250 ms | 1.8 m |
| 500 ms | 1,000% | 66 m/s | 500 ms | 3.3 m |

Check the 250 ms row by hand. Packets sent during the spike are released at 1,250 ms and arrive at 1,290 ms, together with the next packet, so the server's tick at 1,300 ms sees them all. The last accepted claim was at the tick at 1,000 ms. The newest claim is 6 steps ahead, 1.8 m. The rate check allows `0.3 × (1 + tol)`, so it needs `tol = 5`, or 500%. The credit check allows `6 × min(300, 50 + L) / 1000`, which is 1.8 m once `L ≥ 250`.

The two columns forgive the same honest spike and give away very different things. The rate check turns the spike you forgive into permanent free speed for anyone. Forgiving a quarter-second hiccup lets a cheater run at six times the legal speed all day. The credit check turns it into a one-off jump of 1.8 m, less than a body length and a half, and gives no steady speed at all.

The last line shows the cost of setting `L` too low. With `L = 250 ms`, a 500 ms spike produces one violation, and the server pulls the honest player back 1.5 m (`6 × (500 − 250) / 1000`). Every honest spike longer than `L` is a rubber-band and, as section 4 shows, a piece of false evidence against an innocent player.

### Move it yourself

Open `examples/w03-lag-tolerant-movement-check.html`. The left plot shows claimed and accepted position over three seconds for an honest player who hits a lag spike, with violations marked in red. The right plot shows, for the check you choose, what the cheater gets as you drag the tolerance. That is free speed in m/s for the rate check and the largest jump in metres for the credit check, both plotted against the longest spike the setting forgives. Start on the rate check at 250 ms and watch the cheater's line on the left pull away at 36 m/s. Switch to the credit check and the cheater's line snaps back to the honest one, with one small step at the spike. Then drag `L` below the spike length and watch the honest player's red mark appear.

### Cross-game recognition

**Minecraft: Java Edition (26.3).** The vanilla check is a rate check in squared distance with an enormous tolerance, scaled by the number of packets received that tick. Scaling by packet count forgives bunching, the way our credit check does, but it counts something the client controls. So the server caps it. If more than five packets arrive in one tick, it treats the batch as a single packet. The same server runs a second check after its own collision code moves the player. If the client's claimed position and the server's result differ by more than a quarter of a block (a squared distance of 0.0625), it logs "moved wrongly" and, unless the player was already stuck inside a block, puts them back. That second check is the noclip defense in section 3.

**Minecraft: Bedrock Edition (current server settings).** Bedrock's server settings include one called `player-position-acceptance-threshold`, default 0.5 blocks. The documentation describes it as a tolerance for differences between client and server positions, so that non-cheating players are not corrected too often when the two disagree about when a motion started. That is our `L`, stated in distance rather than time. It exists for the same reason, and it has the same cost, a small jump any client may take.

**Source engine (Source SDK 2013).** CS202 week 4 showed Source's command budget, one tick of credit per server tick, capped by `sv_maxusrcmdprocessticks` at 24 ticks. At Source's 15 ms default tick, that forgives 360 ms. It is the credit check applied to input commands instead of positions, with `L` of about a third of a second.

**Old School RuneScape (current).** Movement advances in whole tiles on the server's 0.6-second game tick, one tile per tick walking and two running. There is no continuous speed to hack. The server's clock and the tile grid are the check. That shows the far end of the design space. If movement is coarse and server-timed, the whole problem in this lecture disappears, and so does the smooth movement a shooter needs.

Four games, one model. Every movement check forgives some amount of lag, and the question to ask of any design is what that forgiveness gives a cheater, speed forever or a jump once.

### Design judgment

- **Bound totals, not rates.** A tolerance on each tick's distance is permanent free speed. A cap on distance per unit of server time is a one-off burst. This is the same lesson CS202 week 4 taught for commands, now applied to positions.
- **Set `L` from measured spikes.** Look at the distribution of packet gaps in your telemetry. Choose `L` to cover the gaps you want to forgive, perhaps the 99.9th percentile, and then compute the jump it allows. If the jump is too large for your game (a 3 m jump crosses a PvP choke point), you have a real trade to make, not a bug to fix.
- **Never use the client's clock.** A check against the client's own timestamps accepts time manipulation, because the cheat's whole method is to lie about time. Server time is the only clock the cheater cannot move.
- **Prevention and detection are different outputs.** Clamping a claim to the allowed distance is prevention. It needs no verdict about anyone. Counting violations is evidence for detection, which does need a verdict, and section 4 shows how easily that evidence misleads.
- **Loose checks are a choice.** Minecraft's 10-block guard stops only teleports. That can be right for a cooperative building game where speed matters little, and wrong for a PvP MMO. Match the tightness to what speed is worth in your week 1 ledger.

### Check this example

1. A game runs a 30 Hz tick (`T = 33.3 ms`) with a legal speed of 7 m/s. Using the rate check, what `tol` forgives a 200 ms spike, and what speed does that give a cheater?
2. Same game, credit check with `L = 200 ms`. What is the largest single jump?
3. With `L = 150 ms`, an honest player on the same game suffers a 400 ms spike. How far is the player pulled back?

<details>
<summary>Answers</summary>

1. `tol = J / T = 200 / 33.3 = 6`, so 600%. The cheater runs at `7 × 7 = 49 m/s`.
2. `7 × (33.3 + 200) / 1000 = 1.63 m`.
3. `7 × (400 − 150) / 1000 = 1.75 m`.

</details>

## 3. The other movement checks

Distance is one of several properties a claim must satisfy. A complete movement validator asks four questions of every claim, each backed by server state.

| Question | Check | Catches | Honest cases to forgive |
|---|---|---|---|
| Is it too far? | Credit check (section 2) | Speed, teleport, freeze and jump | Lag spikes, knockback, speed buffs |
| Is it physically possible? | Re-run the move through server collision | Noclip, walking through walls | Tiny float differences, moving platforms |
| Is the height legal? | Gravity check on time spent airborne | Fly hacks | Jump pads, falling, swimming, climbing |
| Is the state legal? | Speed limit from server-known state | Moving while rooted or stunned | A stun that started less than one trip ago |

**Collision.** The server runs the claimed move through its own collision code and compares the result with the claim. If they differ by more than a small threshold (Minecraft Java uses a quarter of a block), the claim went somewhere the world does not allow. The threshold exists because client and server floating-point results differ slightly. Doors, elevators and moving platforms are the hard part. The server's platform may be one tick behind the client's.

**Gravity.** A claim that stays in the air too long is a fly hack. Minecraft Java's simplest version is a server setting. With `allow-flight` off, a survival player who stays in the air for at least 5 seconds is kicked. The Minecraft Wiki notes that dropping a little every few seconds avoids it, which is the rate-check problem again. A better check tracks vertical speed against gravity per tick, using the same credit idea with a separate `L` for vertical motion.

**State changes lag behind.** The server applies a slow or a root at its own time, and the client learns about it a one-way trip later. For that trip, an honest client is still moving at the old speed. So when the legal speed drops, the check must keep allowing the old speed for about one round trip. This is lag tolerance in another form, and it is an opening for a cheater with high ping. The server can cap the grace period at a fixed value rather than following each player's measured ping, as with the look-ahead cap in week 2.

**Knockback and launches.** When the server itself pushes a player (an explosion, a charge ability), it knows the push and should add it to the allowed distance. Minecraft's check does this by subtracting the square of the player's current velocity before comparing. If you forget, every explosion becomes a violation for everyone in range.

## 4. From violations to verdicts

Prevention clamps claims. Detection decides who is cheating, and it runs on violations as evidence. The trouble is that honest players produce violations too, every time a lag spike exceeds `L`. How many violations should it take to flag an account?

### The model

Count violations per 10-minute session. Two populations produce them.

- **Honest players.** Suppose an honest player has about 6 lag spikes per session, and spike lengths follow an exponential distribution with a 100 ms mean. The chance a spike exceeds `L` is `e^(−L / 100)`, so honest violations per session average `λ_h = 6 × e^(−L / 100)`. At `L = 250 ms`, that is 0.49.
- **Blink cheaters.** A cheater who teleports 5 m at a time violates every time, because the credit check allows at most 1.8 m at `L = 250 ms`. Suppose they blink an average of 5 times a session, `λ_c = 5`.

Rare, independent events in a fixed window follow the Poisson distribution, the limit of the binomial from MA102 week 6. The rule "flag if a session has `k` or more violations" has

- a **false-positive rate** (FPR), the share of honest sessions flagged, `P(Poisson(λ_h) ≥ k)`,
- a **recall**, the share of cheating sessions flagged, `P(Poisson(λ_c) ≥ k)`,
- a **precision**, the share of flagged sessions that are really cheaters.

Precision depends on the **base rate**, the share of sessions that are cheating. Take 100,000 sessions a day, 0.5% of them cheating (500).

```python
from math import exp, factorial

def p_at_least(k, lam):
    """Poisson chance of k or more events when lam are expected."""
    return 1 - sum(exp(-lam) * lam ** i / factorial(i) for i in range(k))

SESSIONS, CHEAT_SHARE = 100_000, 0.005
honest_lam = 6 * exp(-250 / 100)        # spikes longer than L = 250 ms per session
cheat_lam = 5                           # blinks per cheating session
cheaters = SESSIONS * CHEAT_SHARE
print(f"honest violations per session: {honest_lam:.2f}")
for k in range(1, 6):
    fpr, tpr = p_at_least(k, honest_lam), p_at_least(k, cheat_lam)
    fp, tp = (SESSIONS - cheaters) * fpr, cheaters * tpr
    print(f"k={k}  FPR {fpr:.4f}  recall {tpr:.3f}  innocent flags {fp:6.0f}"
          f"  cheaters caught {tp:3.0f}  precision {tp / (tp + fp):.1%}")
```

Output:

```
honest violations per session: 0.49
k=1  FPR 0.3889  recall 0.993  innocent flags  38696  cheaters caught 497  precision 1.3%
k=2  FPR 0.0879  recall 0.960  innocent flags   8750  cheaters caught 480  precision 5.2%
k=3  FPR 0.0138  recall 0.875  innocent flags   1376  cheaters caught 438  precision 24.1%
k=4  FPR 0.0017  recall 0.735  innocent flags    165  cheaters caught 367  precision 69.0%
k=5  FPR 0.0002  recall 0.560  innocent flags     16  cheaters caught 280  precision 94.6%
```

Read the `k = 3` row slowly. The rule catches 87.5% of cheaters and flags only 1.4% of honest sessions, which sounds excellent. But honest sessions outnumber cheating ones 199 to 1, so 1.4% of them is 1,376 innocent flags against 438 real ones. Three in four flagged players are innocent. This is the **base-rate fallacy**, and it is the most common way anti-cheat systems end up banning the wrong people. Raising `k` to 5 buys 94.6% precision at the price of letting 44% of cheaters through that day.

### Evidence accumulates for cheaters, not for the honest

A cheater cheats again tomorrow. An honest player's lag spikes are random, session to session. Wait a week (7 sessions) and count violations across them. Honest players average `7 × 0.49 = 3.45`, cheaters `7 × 5 = 35`. Flag at 14 or more violations in the week, and on the same population the expected innocent flags fall to about 1.6 while essentially all 500 cheaters are caught (recall above 99.99%). That is precision above 99.6%, from the same detector, just by waiting.

That is the statistical argument for waiting before a verdict: evidence piles up against cheaters and not against the unlucky. It is one of two reasons studios ban in delayed waves. The other is strategic, since an instant ban tells the cheat maker which check fired, and [week 5](w05-memory-editing-and-client-integrity.md) builds the model that sets the delay. The cost of waiting is that cheaters keep playing, and ruining matches, until the verdict. For a PvP game that cost is high, so many teams combine the two. They clamp at once (prevention, no verdict needed) and ban later (detection, with more evidence).

### Where to spend a false positive

Every flag goes somewhere. A flag that triggers an automatic ban needs precision near 100%, because each false ban is a customer lost and a support ticket, and in week 12 you will see it can be a legal problem. A flag that sends a session to a human reviewer or to a more expensive automated check (week 2's sampled validation) can tolerate much lower precision, because the next stage filters it. Design a pipeline, not a single threshold. A cheap check with high recall feeds a costly check with high precision.

## In-class activity (25 minutes)

Pairs. You are tuning movement validation for an invented PvP MMO with a 20 Hz tick and a run speed of 7 m/s. Telemetry from 10,000 honest sessions shows packet gaps with 99th percentile 180 ms and 99.9th percentile 420 ms.

1. (6 min) Compute the rate-check tolerance and the credit-check `L` that forgive the 99th and the 99.9th percentile gaps. For each, state what a cheater gets.
2. (6 min) The design lead says any jump over 2 m breaks the game's choke points. Which of your settings are acceptable? What happens to honest players above your chosen `L`?
3. (8 min) With your chosen `L`, honest players average 0.3 violations per session and blink cheaters average 4. At a 1% cheater base rate, compute precision for `k = 3` and `k = 4` in a single session. Use the Poisson formula or the lecture's code.
4. (5 min) Write a two-sentence ban policy: what happens at once, what happens later, and why.

Expected output: a four-row table of settings with their cheater gains, one chosen `L` with its justification, two precision values, and the policy.

## Common misconceptions

- **"A tighter check is more secure."** A tighter credit check rubber-bands more honest players and floods detection with false evidence. The rate check never becomes secure at any tolerance that honest players survive.
- **"If 99% of honest sessions pass, a flag means 99% guilt."** Precision depends on the base rate. At 0.5% cheaters, a rule with a 1.4% false-positive rate is wrong three times in four.
- **"Using the client's timestamps fixes lag tolerance."** It fixes it for honest players and accepts every time-manipulating cheat. Only the server's clock is safe.
- **"Waiting for more evidence is just slow."** A week of sessions lifts precision from 24% to above 99.6% with the same detector, and a delayed ban also hides which check fired from cheat sellers (week 5). The cost, cheaters staying in matches longer, is real and should be weighed, not ignored.

## Check yourself

1. A rate check forgives 150 ms spikes on a 50 ms tick with a legal speed of 5 m/s. What speed does a cheater get for free? What would a credit check with `L = 150 ms` give instead?
2. Why does the credit check cap the time since the last accept at `T + L` instead of leaving it uncapped?
3. With `L = 500 ms` in the section 4 model, honest players average `6 × e^(−5) = 0.04` violations per session. Without computing, say whether precision at `k = 2` rises or falls compared with `L = 250 ms`, and what the team pays for it.
4. A detector flags 2% of honest sessions and 90% of cheating sessions. At a base rate of 1 cheater in 1,000 sessions, what share of flags are cheaters?
5. A studio bans instantly on any single "moved too quickly" warning. Name two groups who will write to support.

<details>
<summary>Answers</summary>

1. `tol = 150 / 50 = 3`, so the cheater runs at `5 × 4 = 20 m/s` forever. The credit check gives no steady speed, only a largest jump of `5 × (50 + 150) / 1000 = 1 m`.
2. Without a cap, a client could send nothing for 30 seconds and then claim 180 m in one packet. The average speed would be legal, but the player would stand frozen on every other screen for 30 s, dodging attacks, and then appear somewhere else. The cap bounds that freeze-and-jump to `L`.
3. Precision rises, because honest players produce about twelve times fewer violations. The team pays with a larger jump allowance, `6 × 0.55 = 3.3 m`, which a freeze-and-jump cheater can use.
4. Per 1,000 sessions, `0.9` cheaters flagged and `999 × 0.02 = 19.98` honest flagged. Precision is `0.9 / 20.88 = 4.3%`.
5. Players with bad connections whose spikes exceeded the check, and players launched by explosions or knockback that the check did not account for. (Also players on moving platforms, and anyone caught during a server lag spike.)

</details>

## Lab / assignment hook

[Lab 03, the lag-tolerant movement validator](../labs/lab03.md). You implement the rate and credit checks, reproduce this lecture's table, add a gravity check, then tune a violation threshold on a supplied log of honest and cheating sessions until you meet a precision target. The detector you build becomes part of the course's final prototype (40%).

## Sources

- Mojang, *Minecraft: Java Edition* 26.3 server code, class `ServerGamePacketListenerImpl`, movement handling, as shown in the unmodified (vanilla) lines of PaperMC's patch file `paper-server/patches/sources/net/minecraft/server/network/ServerGamePacketListenerImpl.java.patch` (GitHub, PaperMC/Paper, main branch, `mcVersion=26.3`, accessed September 2026). Squared-distance threshold of 100 per received packet (300 while gliding) after subtracting squared velocity, with the "moved too quickly" warning and reset; packet count above 5 treated as 1; the post-collision "moved wrongly" threshold of 0.0625 (squared distance).
- Minecraft Wiki, "Sprinting" (accessed September 2026). Sprinting at about 5.612 m/s and walking at about 4.317 m/s.
- Minecraft Wiki, "Server.properties" (accessed September 2026). Java Edition `allow-flight`, default false, kicks players in the air for at least 5 seconds. Bedrock Edition `player-position-acceptance-threshold`, default 0.5, and its description; Bedrock's client-authoritative, server-authoritative and server-authoritative-with-rewind movement modes.
- Old School RuneScape Wiki, "Game tick" and "Energy" (accessed September 2026). A 0.6-second server game tick; one tile per tick walking and two tiles per tick running.
- Valve, Source SDK 2013, `sv_maxusrcmdprocessticks` default 24 and Source's 15 ms default tick, as cited in CS202 week 4.
- *MDY Industries, LLC v. Blizzard Entertainment, Inc.*, 629 F.3d 928 (9th Cir. 2010, amended 2011), statement of facts. Warden launched September 2005 and used at once to ban most Glider users; Glider modified to avoid detection; Warden afterwards detecting Glider only occasionally.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games*. Addison-Wesley, chapter 5, "Pathing Bugs in Games", pp. 104-107 (page numbers from the publisher's table of contents, InformIT).
- The tick, speed, latency, spike distribution, session counts and cheater base rates in sections 2 and 4 are teaching values, not measurements from any game.

## Interactive spec: examples/w03-lag-tolerant-movement-check.html

**Insight the visual must make obvious:** a tolerance on each tick's distance (rate check) turns the lag you forgive into permanent free speed for cheaters, while a cap on distance per unit of server time (credit check) turns the same forgiveness into one small jump. A second panel makes the detection point: a violation threshold that looks strict on honest players can still produce mostly innocent flags when cheaters are rare.

**Layout.** Two tabs, "Validation" (default) and "Detection". On screens under 700 px wide, panels stack vertically. No page-level horizontal scroll.

**Validation tab.** Two linked plots and a number panel.
1. **Left plot, "Position over 3 seconds".** x axis time 0 to 3,000 ms, y axis metres 0 to 60. Lines for honest claimed (thin solid), honest accepted (thick solid), cheater accepted (dashed). The honest player has one lag spike of length `J` starting at 1,000 ms. The cheater, when "steady speed" is selected, claims `m × s` every tick with no spikes. When "freeze and jump" is selected, the cheater sends nothing for `H` ms from 1,000 ms and then claims its true position. Mark violations as red dots on the x axis, honest and cheater in different shapes. Shade the spike interval.
2. **Right plot, "What the forgiveness gives away".** x axis spike forgiven, 0 to 600 ms. Two lines: rate check free speed `v × (1 + J/T)` in m/s (left y axis, 0 to 80), credit check largest jump `v × (T + J) / 1000` in metres (right y axis, 0 to 8, so the two lines do not overlap). A vertical marker at the current setting (`tol × T` for the rate check, `L` for the credit check).
3. **Number panel.** `T`, `s`, current setting, honest violations, honest metres pulled back, cheater violations, cheater lead over honest at 3 s, largest single accepted jump.

**Validation controls.**
- Check radio: "Rate check" or "Credit check" (default "Rate check").
- Rate tolerance slider, 0 to 1,200%, step 10, default 500.
- Lag tolerance `L` slider, 0 to 600 ms, step 10, default 250.
- Honest spike `J` slider, 0 to 600 ms, step 50, default 250.
- Cheat radio: "Steady speed" with multiplier `m` slider 1.0 to 8.0, default 6.0; or "Freeze and jump" with hold `H` slider 0 to 1,000 ms, step 50, default 400.

**Detection tab.** A bar chart of flagged sessions per day split into cheaters (one colour) and innocent (another), for `k` from 1 to 8, with precision printed above each bar and the current `k` highlighted. Beside it, a confusion table for the current `k`: true positives, false positives, false negatives, true negatives, and precision and recall.

**Detection controls.** `L` (shared with the Validation tab), spikes per honest session (0 to 20, default 6), mean spike length (20 to 300 ms, default 100), blinks per cheating session (0 to 20, default 5), cheater base rate (0.1% to 10%, log slider, default 0.5%), sessions per day (fixed 100,000), threshold `k` (1 to 8, default 3), window (1 session or 7 sessions, default 1).

**Formulas (match the lecture's code and `labs/lab03-starter/movement_validator.py`).** `T = 50`, `v = 6`, `s = 0.3`, latency 40 ms, client sends at `k × T` for `k = 0, 1, ...`. A packet sent in `[1000, 1000 + J)` arrives at `1000 + J + 40`, others at `sent + 40`. Server tick `i` at `i × T` handles packets with arrival in `(iT − T, iT]`, takes the newest claim. `d = claim − pulled − accepted`. Rate: `allowed = s × (1 + tol)`. Credit: `allowed = v × min(now − t_last_accept, T + L) / 1000`. Violation if `d > allowed + 1e-9`; then `pulled += d − allowed` and `d = allowed`. Accept `d`, set `t_last_accept = now`. Detection: `λ_h = spikes × e^(−L / mean)`, `λ_c = blinks`, both multiplied by 7 in the 7-session window. FPR `= P(Poisson(λ_h) ≥ k)`, recall `= P(Poisson(λ_c) ≥ k)`.

**Test values** (assert on load, log failures to the console):
- Smallest rate tolerance with no honest violation: 100% at `J = 50`, 500% at `J = 250`, 1,000% at `J = 500`.
- Smallest credit `L` with no honest violation equals `J` for `J` in {50, 100, 250, 500}.
- Credit check, `L = 250`, `J = 500`: 1 honest violation, 1.5 m pulled back.
- Largest jump at `L = 250`: 1.8 m.
- Detection at defaults: `λ_h = 0.49` (two decimals); `k = 3` gives 1,376 innocent flags, 438 cheaters caught, precision 24.1%; `k = 5` gives precision 94.6%.
- 7-session window, `k = 14`: innocent flags about 1.6, precision above 99.6%.

**First screen:** Validation tab, rate check at 500% tolerance, `J = 250`, steady-speed cheater at `m = 6`, so the cheater's dashed line pulls away with no red dots while the right plot's marker sits at 36 m/s. Caption: "Forgive a quarter-second of lag with a rate check and a cheater runs six times faster, unflagged."
