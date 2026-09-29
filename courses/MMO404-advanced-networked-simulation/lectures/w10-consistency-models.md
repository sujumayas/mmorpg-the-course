# MMO404 · Week 10 — Consistency models

**Why this matters:** Once two servers hold copies of the same world, they will sometimes disagree, and the only choice you get is which disagreements players may see and for how long. Pick too strict a rule and every cross-server action waits a round trip. Pick too loose a rule and two players both loot the same chest. This week you learn to choose a rule per operation, and to put a number on what each choice costs.

**You will be able to:**
- Compute the conflict rate of optimistic cross-server actions from claim rate and visibility window, and the latency of forwarding them to the owner.
- Classify game operations as exclusive, commutative or cosmetic, and assign each the weakest consistency model that keeps it correct.
- Design a replicated counter that converges under late, duplicated and reordered messages, and explain why a threshold on it still needs one decider.
- Critique a cross-server design by naming the anomaly players will see and how often.

**Before class:** Martin Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 5 (Replication), the sections on replication lag and on detecting concurrent writes, and chapter 9 (Consistency and Consensus), the section on linearizability. Evan Wallace, "How Figma's multiplayer technology works" (Figma blog, 16 October 2019), the whole post.

**Prerequisites from earlier courses:** [MMO404 week 2, seamless worlds and boundary handoff](w02-seamless-worlds-and-boundary-handoff.md) (owners, ghosts, the rule of one authoritative owner). [MMO404 week 8, distributed simulation research](w08-distributed-simulation-research.md) (lookahead, optimistic simulation and rollback) and [week 9, server meshing concepts](w09-server-meshing-concepts.md) (authority transfer and fencing). [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 9, server reconciliation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md) (guessing, then correcting). [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) (everyone runs the same commands in the same order). [DB201 week 5, transactions and ACID](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) and [MMO302 week 8, item ownership](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (one item, one owner).

**Interactive:** [w10-optimistic-conflicts.html](../examples/w10-optimistic-conflicts.html). Keep it open during section 2.

---

## 1. What "consistent" means when there are two copies

In week 2 you gave every entity exactly one **owner**, the server whose simulation is the truth, and let other servers hold read-only **ghosts**. That rule settles who writes. It does not settle what everyone else sees in the meantime. A ghost on server B is a copy of an entity owned by A, and it is always a little behind, by the link delay plus however long A waits before sending. During that gap, B's players are looking at the past.

A **consistency model** is a promise about those gaps. It says which orders of events a reader might observe, and which it never will. Databases have a long list of them. Four are enough for game servers, from strictest to loosest.

- **Linearizable.** Every read sees the latest write, as if there were only one copy. In a game, you get this by sending every read and write of an entity to its owner and waiting for the answer. Week 2's owner is linearizable for anything you ask the owner directly.
- **Sequential (total order).** Every copy applies the same operations in the same order, possibly late. Nobody sees the latest state immediately, but nobody ever sees a different history. Deterministic lockstep (CS202 week 12) is the game form.
- **Causal.** If one event could have caused another, every copy shows them in that order. Events that could not have influenced each other may appear in different orders on different copies. A reply never shows up before the message it answers.
- **Eventual.** If writes stop, all copies end up equal. Until then, anything goes. A week 2 ghost is eventually consistent. So is a player's friend list shown on another server.

Two more terms. **Staleness** is how far behind a copy is, in seconds or in game units. A **conflict** is a pair of writes that were each made without knowing about the other and cannot both stand. Stale reads are normal and mostly harmless. Conflicts are what cause bugs players report.

The main idea of this week fits in one sentence. **A game does not pick one consistency model. It picks one per operation.** Movement, damage, loot, chat and emotes each need a different promise, and the stricter promises cost latency. Choosing well means using the loosest model that keeps each operation correct.

## 2. Worked example: the chest on the seam, forward or guess?

### The hook

In 1997 Age of Empires kept eight players' games identical by having every machine run every command in the same order. The Ensemble programmers wrote that commands issued in one 200 ms turn were executed two turns later on every machine, and that a game whose machines drifted apart, even over one misplaced deer, was stopped as out of sync. That is the strictest promise there is, and they paid for it with about 400 ms of built-in delay on every order.

At the same time, Quake-lineage shooters went the other way. Your own client moves your character the instant you press a key, before the server has agreed, and fixes the picture if the server later disagrees (CS202 week 8). Valve's documentation for the Source engine notes that this prediction runs for the local player only.

Two shipped games, opposite answers to the same question: should a copy wait for the truth, or guess and fix it later? Now put that question on an MMO server seam. A treasure chest sits two metres inside server B's region. Players on both sides can reach it. A player on server A clicks it. Server A can forward the click to B and wait for B's answer, or it can open the chest at once and tell B afterwards. Which is right?

### The model

The chest is an **exclusive** object. Only one player may win it. Call a click on it a **claim**.

**Policy F, forward.** Server A sends the claim to the owner B, B decides on its next tick and sends the result back, and A shows it on its next tick. No two players can ever both win, because one server decides. The price is latency. With one-way link delay `d` and tick interval `T`, each server waits on average half a tick for its next tick, so

```
added latency (average) = 2d + T
added latency (worst)   = 2d + 2T
```

**Policy G, guess.** Server A grants the claim locally and at once, then tells B. B does the same with claims from its own players. A claim on A is in **conflict** if B granted a claim of its own that A had not yet heard of, before B heard of A's. Call the time a grant stays unknown to the other server the **visibility window** `W`. In a tick-based server, news of a grant leaves in the update A sends at its next tick, spends `d` on the wire, and is applied at B's next tick. On average that is half a tick waiting to leave, `d` travelling, and half a tick waiting to be applied, so `W ≈ T + d`. A claim on A conflicts with any B claim made up to `W` before it or up to `W` after it.

If the other server's players click at an average rate `λ` per second, and each click is independent of the others, the clicks form a **Poisson process**. In such a process the number of clicks in a window of length `t` has mean `λt`, and the chance that the window holds none at all is `e^(−λt)`. So the number of rival claims in a window of length `2W` has mean `2λW`, and by the complement rule ([MA102 week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md)) the chance that there is at least one is

```
P(conflict) = 1 − e^(−2 λ W)
```

- `λ` is the **claim rate** from the other server, in claims per second on this one object.
- `W` is the **visibility window**, the time before a grant on one server is known to the other.
- `P` is the share of claims that will need to be undone, because two players were told they won.

When `2λW` is small, `P ≈ 2λW`. Doubling the claim rate or the window doubles the conflicts.

### Numbers you can check

Use `T = 100 ms` (10 Hz) and `d = 1 ms` between servers in the same data centre, so `W = 101 ms`. Policy F costs every claim 102 ms on average and 202 ms at worst, whatever `λ` is. Policy G costs nothing when it works and a visible reversal when it does not.

| Object | Claim rate `λ` from the other server | `P(conflict)`, tick-aligned `W = 101 ms` | `P(conflict)`, flushed `W = 1 ms` |
|---|---|---|---|
| Chest in a quiet side room | 0.01 per s | 0.20% | 0.002% |
| Limited-stock vendor item | 0.1 per s | 2.00% | 0.02% |
| Gathering node in a busy square | 0.5 per s | 9.61% | 0.10% |
| World-boss chest, first seconds | 2 per s | 33.2% | 0.40% |
| World-boss chest, 20 players spamming | 5 per s | 63.6% | 1.00% |

Check two cells by hand. For the busy node, `2λW = 2 × 0.5 × 0.101 = 0.101`, and `1 − e^(−0.101) = 0.0961`. For the spamming crowd, `2λW = 1.01`, and `1 − e^(−1.01) = 0.636`. Nearly two in three claims would be granted and then taken back.

The last column changes one thing. Instead of waiting for the tick, each server sends news of a grant the moment it makes one, and the other server applies it the moment it arrives. Now the window is only the wire, `W = d = 1 ms`, and conflicts fall a hundredfold.

Three things stand out.

- **At low contention, guessing is almost free.** One claim in 500 conflicts on the quiet chest. Forwarding would charge all 500 claims 102 ms to prevent that one reversal.
- **At high contention, guessing is wrong most of the time.** A world-boss chest with 20 players clicking cannot be guessed. You would grant the loot to several players and take it back from all but one, which feels worse than any delay.
- **The window is mostly the tick, not the network.** In a data centre, 100 of the 101 ms of `W` is waiting for a tick. Flushing claims immediately shrinks conflicts far more than a faster network ever could.

You can also turn the formula around. Suppose the design team accepts one reversal per 100 claims. Solve `1 − e^(−2λW) = 0.01` for `λ` with `W = 0.101`: `λ = −ln(0.99) / 0.202 = 0.050` per second. Any object clicked more often than once every 20 seconds from across the seam should be forwarded, not guessed.

Here is the model with a simulation that checks it. It is the core of Lab 10.

```python
import math, random

T, d = 0.100, 0.001            # tick interval and one-way delay between servers, in seconds

def conflict_p(lam, W):
    """Chance that a claim has a claim from the other server within W on either side."""
    return 1 - math.exp(-2 * lam * W)

def simulate(lam, W, claims=200_000, seed=10):
    """Poisson claims on A and on B at rate lam. Share of A's claims with a B claim within W."""
    rng = random.Random(seed)
    def arrivals():
        t, out = 0.0, []
        for _ in range(claims):
            t += rng.expovariate(lam)
            out.append(t)
        return out
    a, b = arrivals(), arrivals()
    j = hits = 0
    for t in a:
        while j < len(b) and b[j] < t - W:
            j += 1
        hits += j < len(b) and b[j] <= t + W
    return hits / claims

print(f"forward: +{1000 * (2 * d + T):.0f} ms on average, +{1000 * (2 * d + 2 * T):.0f} ms at worst")
for lam in (0.01, 0.1, 0.5, 2, 5):
    print(f"lam={lam:<4}  tick-aligned P={100 * conflict_p(lam, T + d):5.2f}%"
          f"  simulated={100 * simulate(lam, T + d):5.2f}%  flushed P={100 * conflict_p(lam, d):4.2f}%")
```

It prints `forward: +102 ms on average, +202 ms at worst`, then one line per claim rate. The simulated share lands within 0.3 percentage points of the formula in every row, for example `simulated= 9.67%` against `9.61%` at `λ = 0.5`. This simulation uses a fixed window. Lab 10 gives you a second one where grants really wait for ticks, so each window is a little different, and you measure how far the average `W = T + d` is from the truth. With the two servers' ticks offset by 37 ms it stays within half a percentage point in every row. With the ticks in step, news always just misses the other server's tick, and the lab asks you to work out what that costs.

### Move it yourself

Open `examples/w10-optimistic-conflicts.html`. The left view shows two timelines, one per server, over ten seconds. Each claim is a dot with a shaded bar of width `2W` around it. Where a dot on one line falls inside a bar on the other, both turn red: two players were told they won. The right view plots `P(conflict)` against `λ` for the current window, with a flat line at the forward policy's latency for comparison. It opens at `λ = 0.5`, the busy gathering node. Each lane holds about five claims in ten seconds, and red is rare, about one red dot per screen on average. Drag it to 2 and watch the bars start to overlap everywhere, while the curve on the right has only moved to a third. Then press "flush immediately". The bars shrink to slivers and the red disappears, although nothing about the players changed.

### Same idea elsewhere

Every design below chooses between forwarding and guessing, and each can be written with the same two quantities, the latency it adds and the conflict chance it accepts.

**Age of Empires (Ensemble Studios, 1997; Bettner and Terrano, 2001).** Lockstep is Policy F taken to its limit. Every command waits two 200 ms turns so that every machine has it before anyone runs it. The added latency is about 400 ms, and the conflict chance is zero by construction, because nobody acts on a command before all copies have it. The paper reports that players did not notice 250 ms and found 250 to 500 ms very playable. The whole design depends on hiding that fixed delay behind the acknowledgement sound a unit makes when you click.

**Source and QuakeWorld prediction (Valve and id Software, late 1990s onward).** Prediction is Policy G for one object, your own character. The claim rate from anyone else on your inputs is zero, so conflicts only come from the world disagreeing (you walked into a door another player closed), and the server corrects them. Valve limits prediction to the local player, which in our form says: guess only where `λ` from others is near zero. Predicting other players would mean guessing their inputs, a high-`λ` object, and the corrections would be constant.

**Figma (Wallace, October 2019).** A design document, not a game, but the same problem. Every client applies its own edits immediately (a guess), and a central server decides. Two edits to the same property of the same object are settled by last writer wins at the server, and the losing client simply sees its value replaced. That works because `λ` is tiny, since two people rarely change the same property of the same shape in the same fraction of a second, and because a lost edit is cheap to redo. Wallace's post calls a client's unacknowledged change its "best prediction", which is Policy G in one phrase.

**GGPO rollback (fighting games, SDK released 2009).** Rollback guesses the remote player's input, runs ahead, and resimulates when the real input arrives (CS202 week 12). A misprediction is a conflict. It works because in a fighting game the remote input usually stays the same from one frame to the next, so the effective rate of changes the guess gets wrong is low, and a rollback of a few frames is barely visible.

Four systems, one trade. Each accepts either a fixed added latency or a conflict rate that grows with `λW`. When you meet a new design, find its `λ`, its `W` and what a conflict costs the player.

### Design judgment

- **Choose per object, by contention.** Forward objects that many players compete for at once, such as boss loot, capture points and auction purchases. Guess on objects that one player at a time uses, such as their own movement, their own inventory sorting and a door on a quiet road.
- **Weigh what a reversal costs, not only how often it happens.** A reversed door opening is a stutter. A reversed legendary drop is a support ticket and a forum thread. Even a 0.2% conflict rate is too high for an item worth real money on a grey market.
- **Shrink `W` before you give up on guessing.** Flushing claims as they arrive, instead of on the tick, cut conflicts a hundredfold in the table. That is usually cheaper than any other fix.
- **Hide the forward latency.** A chest-opening animation of 300 ms covers a 202 ms worst-case round trip. Age of Empires hid 400 ms behind a voice line. When you forward, give the player something to watch while the owner decides.
- **Never guess on anything that creates value.** Loot, currency and experience should not be granted until one server has decided. A guessed kill on a trash mob can be taken back. A guessed item may already have been traded on before you notice, and MMO302 week 8 showed what that does to your economy.

### Check this example

1. A crafting station near a seam gets 0.05 claims per second from the other server. With `W = 101 ms`, what share of guessed claims conflict? What if the servers flush claims immediately with `d = 2 ms`?
2. At what claim rate does the tick-aligned guess policy produce one conflict per ten claims?
3. A team proposes raising the server tick rate from 10 Hz to 30 Hz instead of flushing. Estimate the new conflict rate for the busy gathering node.

<details>
<summary>Answers</summary>

1. `2λW = 2 × 0.05 × 0.101 = 0.0101`, so `P = 1 − e^(−0.0101) ≈ 1.0%`. Flushed, `W = 0.002`, so `2λW = 0.0002` and `P ≈ 0.02%`.
2. `1 − e^(−0.202 λ) = 0.1` gives `λ = −ln(0.9) / 0.202 ≈ 0.52` per second.
3. `T = 33.3 ms`, so `W = 34.3 ms` and `2λW = 0.0343`. `P = 1 − e^(−0.0343) ≈ 3.4%`, down from 9.6%. Tripling the tick rate helps by about three times. Flushing helps by a hundred times, and costs far less CPU.

</details>

## 3. Operations that cannot conflict

Section 2 treated every claim as exclusive. Many game operations are not. If you can arrange an operation so that any order of arrival gives the same result, you never have a conflict to resolve, and every server can apply writes immediately.

### Commutative writes and the damage counter

Two writes **commute** if applying them in either order gives the same state. Damage to a boss commutes. Taking 300 then 500 leaves the same health as taking 500 then 300. So a boss that sits across a seam, fought by players on both servers, does not need every hit forwarded.

The trick is to store the damage in a form that also survives duplicated and late messages. Give each server its own running total of the damage it has dealt, and let only that server raise its entry. To merge a message from another server, keep the larger of the two values for each entry. Health is the maximum minus the sum of the entries.

```python
class DamageCounter:
    """Boss damage split by server. Each server only ever raises its own entry."""
    def __init__(self, me, max_hp):
        self.me, self.max_hp, self.parts = me, max_hp, {}

    def hit(self, damage):
        self.parts[self.me] = self.parts.get(self.me, 0) + damage

    def merge(self, remote_parts):
        for server, total in remote_parts.items():
            self.parts[server] = max(self.parts.get(server, 0), total)

    def hp(self):
        return self.max_hp - sum(self.parts.values())

a, b = DamageCounter("A", 10_000), DamageCounter("B", 10_000)
a.hit(300); snap_a1 = dict(a.parts)
b.hit(500); snap_b1 = dict(b.parts)
a.hit(200); snap_a2 = dict(a.parts)
b.merge(snap_a2); b.merge(snap_a1); b.merge(snap_a2)   # late, out of order, duplicated
a.merge(snap_b1)
print("A sees", a.hp(), "B sees", b.hp())
```

It prints `A sees 9000 B sees 9000`. B received A's snapshots late, in the wrong order and one of them twice, and still agrees. This structure is a **grow-only counter**, one of the **conflict-free replicated data types** (CRDTs) described by Shapiro and colleagues in 2011. The property that makes it work is that `max` is commutative, associative and idempotent (applying it twice changes nothing). Any merge function with those three properties gives you eventual consistency with no conflicts at all.

How stale is each server's view? Server A lacks B's damage from the last `W` seconds. If B's players deal `D_B` damage per second, A's health bar is too high by at most `D_B × W`. With 40 players on B at 500 damage per second each, `D_B = 20,000`, and with `W = 0.101 s`, A's view is at most 2,020 health points behind. On a boss with 2,000,000 health, that is 0.1% of the bar, less than one pixel on most health bars.

### Thresholds need one decider

The counter converges. The decisions you make from it do not. Suppose the boss has 1,500 health left. A's players deal 1,000 and B's players deal 1,000 in the same tick. A sees `1,500 − 1,000 = 500` and the boss alive. B sees 500 too. Both are correct about their own view and both are wrong about the truth, which is −500. One `W` later both learn the boss is dead, and if each server runs its own death logic, each awards kill credit and rolls loot. That is the double-loot bug, built from a perfectly consistent counter.

A threshold turns a commutative quantity into an exclusive event. Death, phase changes at 50% health and the first player to reach a quest count are all thresholds. The rule is simple. Let the counter be eventual, and let exactly one server, the boss's owner, decide every threshold. Other servers show the bar from their merged counter and wait for the owner's "died" event before playing the death animation or opening loot. The event is a forwarded claim from section 2, and it happens once per boss, so its latency is invisible.

### Last writer wins, and when it lies

Many values are not counters. A player's chosen title, a guild's message of the day or a house's paint colour are single values that someone overwrites. The usual merge rule is **last writer wins** (LWW): each write carries a timestamp and the larger timestamp survives. It converges, which is why Figma uses it per property.

It also silently discards the losing write, and its idea of "last" is only as good as its timestamps. Server clocks drift. If A's clock runs 30 ms fast, A's writes win every tie within 30 ms even when they came second. Use LWW for values where losing a write is harmless and the user can see and redo it. Never use it for anything a player would call theirs, such as inventory, currency or an auction bid.

## 4. Ordering and causality

The last kind of anomaly is about order rather than value. A player on server A writes "anyone want to group?" in zone chat. A player on B answers "yes, inviting you". A third player on server C receives both, but the message from B reaches C before the one from A because the A to C link was slow. The third player sees an answer to a question nobody has asked yet.

Nothing was lost and nothing conflicted. Causality was broken. The reply **happened after** the question in the sense Lamport defined in 1978: event `x` happened before event `y` if they are on the same server in that order, or if `x` is the sending of a message and `y` its receipt, or through a chain of those.

A **Lamport clock** is a counter on each server that respects this order. Each server increments its counter on every event. Every message carries the sender's counter, and a receiver sets its counter to `max(own, received) + 1`. If `x` happened before `y`, `x` gets a smaller number. Trace the chat example.

| Step | Server | Event | Clock after |
|---|---|---|---|
| 1 | A | player asks, message sent with 1 | A = 1 |
| 2 | B | receives A's message: `max(0, 1) + 1` | B = 2 |
| 3 | B | player replies, message sent with 3 | B = 3 |
| 4 | C | receives B's reply first: `max(0, 3) + 1` | C = 4 |
| 5 | C | receives A's question: `max(4, 1) + 1` | C = 5 |

Server C can now sort what it shows by the carried timestamps, 1 before 3, and hold the reply until everything with a smaller timestamp from the senders it knows about has arrived. The price is a short hold, bounded by the slowest link.

Lamport clocks have one limit. A smaller number does not prove the events are related. Two unrelated events on different servers may get 7 and 9 for no reason. When you need to tell "caused" from "concurrent", for example to show a merge conflict to a designer in a debug tool, give each event a **vector clock**, one counter per server. Event `x` happened before `y` exactly when every entry of `x`'s vector is at most the matching entry of `y`'s and at least one is smaller. Two vectors where neither is below the other mark concurrent events, which is exactly the definition of a conflict in section 1. Lab 10 has you implement both.

Where does causal order matter in a game? Chat and combat logs are the obvious places. The less obvious one is cross-server effects. A healer on A shields a tank on B, and the boss owned by B hits the tank. If B applies the hit before it has processed the shield, the tank takes full damage even though the shield was cast first in real time. Whether that is a bug depends on your game's rules, but players will report it as one if the combat log shows the shield first. Order the log by causal timestamps and let the owner of the tank decide the order it actually applied, and at least the log and the result will agree.

## In-class activity (25 minutes)

In groups of three, you are the server team for a seamless MMO with 10 Hz servers and a 1 ms link between them. For each operation below, choose one policy: **forward** to the owner, **guess** locally, **merge** with a commutative structure, or **eventual** with last writer wins. Estimate `λ` where it applies, compute `P(conflict)` for guessed operations, and name the anomaly a player would see.

1. Player movement.
2. Damage to a world boss fought from both sides of a seam.
3. The world boss's death and loot roll.
4. Buying the last copy of an item at a player-run shop.
5. Changing your character's displayed title.
6. Planting a guild flag on a contested capture point.
7. Emotes.
8. Zone chat.

Expected output: a table of eight rows with the policy, `λ` or "not applicable", `P` where needed, and the anomaly in one short phrase. At least two groups compare their answers for rows 4 and 6, where the choice depends on how busy you assume the object is.

## Common misconceptions

- **"Strong consistency is always safer."** It is safer against conflicts and worse for latency, and latency is also a correctness problem in a real-time game. Forwarding a player's own movement to a remote owner would make every step lag by a round trip.
- **"Eventual consistency means the copies are wrong."** It means they may be behind. With a grow-only counter, every server shows a value that was true within the last `W`, and all converge as soon as messages arrive.
- **"Server timestamps give the true order of events."** Clocks on different machines drift, and last writer wins trusts them blindly. Use logical clocks for order and the owner for decisions.
- **"Conflicts are rare, so we can ignore them."** Rare times volume is not rare. At 0.2% per claim, a million guessed claims a day produce 2,000 double grants a day.

## Check yourself

1. Two servers run at 20 Hz with a 1 ms link. A capture point receives 1 claim per second from the other side. What share of guessed captures conflict? What is the forward policy's average added latency?
2. A designer proposes a boss whose health is stored as one number that every server decrements and broadcasts. Give a sequence of three messages that leaves two servers with different health forever, and fix the design.
3. Event `x` has vector clock `(2, 1, 0)` and event `y` has `(2, 3, 1)`. Event `z` has `(3, 0, 0)`. Which pairs are ordered, and which are concurrent?
4. Your team flushes claims immediately and finds conflicts still at 2% on a busy node. Using the model, what must `λ` be if `d = 1 ms`? Is guessing still a good choice there?

<details>
<summary>Answers</summary>

1. `T = 50 ms`, so `W = 51 ms`, and `P = 1 − e^(−2 × 1 × 0.051) = 1 − e^(−0.102) ≈ 9.7%`. Forward adds `2d + T = 52 ms` on average.
2. A has 1,000 health and sends "hp = 900" after a hit. B, also at 1,000, sends "hp = 950" after its own hit. Each applies the other's value as the new health: A ends at 950, B at 900, and neither is 850. Any later message only overwrites one value with another. Fix it with the per-server damage counter of section 3, and let the owner decide death.
3. `x` happened before `y`, because every entry of `x` is at most the matching entry of `y` and one is smaller. `x` and `z` are concurrent: `z` has the larger first entry (3 against 2), but `x` has the larger second entry (1 against 0), so neither vector is below the other. `y` and `z` are concurrent for the same reason, since `y` has larger second and third entries and `z` a larger first.
4. `1 − e^(−2λ × 0.001) = 0.02` gives `λ = −ln(0.98) / 0.002 ≈ 10` claims per second. That is a mob of players spamming one object. Forward it. At that contention, a 2% reversal rate is a reversal every five seconds.

</details>

## Lab / assignment hook

[Lab 10, conflicts and convergence](../labs/lab10.md). You implement the conflict model and a simulator that checks it with tick-aligned claims, measure where the formula stops being accurate, build a replicated damage counter and a vector clock that pass adversarial message orders, and write a one-page consistency plan for a boss fight across a seam.

## Sources

- Bettner, P. & Terrano, M. (2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond." Gamasutra, 22 March 2001 (now Game Developer). Commands executed two 200 ms turns later on every machine; checksums to detect out-of-sync games; the deer example; players' tolerance of 250 to 500 ms.
- Valve Developer Community, "Source Multiplayer Networking" (accessed September 2026, as cited in CS202 week 8). Input prediction runs the same code as the server and applies to the local player only.
- Carmack, J. .plan entries for August 1996 on QuakeWorld client-side movement prediction (John Carmack .plan archive, `johnc_plan_1996.txt`).
- Wallace, E. (2019). "How Figma's multiplayer technology works." Figma blog, 16 October 2019. Central server decides; last writer wins per property; CRDT-inspired rather than true CRDTs; a client's unacknowledged change is its best prediction.
- GGPO SDK, README (GitHub `pond3r/ggpo`, MIT licence, created 2009). Input prediction of the remote player, speculative execution and rollback.
- Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM* 21(7), 558-565. The happened-before relation and logical clocks.
- Shapiro, M., Preguiça, N., Baquero, C. & Zawirski, M. (2011). "Conflict-free Replicated Data Types." *Stabilization, Safety, and Security of Distributed Systems (SSS 2011)*, LNCS 6976. Grow-only counters and merge by maximum.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 5 (replication lag, concurrent writes, last write wins) and chapter 9 (linearizability, ordering).

## Interactive spec: examples/w10-optimistic-conflicts.html

**The one insight:** guessing is nearly free while claims from the two servers rarely fall within one visibility window of each other, and fails fast once they do. The window is mostly the tick, so flushing claims immediately removes most conflicts without changing the players at all.

**Layout.** Two linked views and a numbers panel. Desktop: timelines on the left (60% width), curve on the right. Under 700 px: timelines, then curve, then panel.

- **Left, two timelines.** Horizontal lanes labelled "Server A" and "Server B" covering a 10-second window. Draw claims as dots, generated as Poisson arrivals at rate `λ` per lane with a seeded PRNG (mulberry32, seed 10 for A, seed 20 for B). Around each dot draw a translucent bar from `t − W` to `t + W`. A dot is **in conflict** if a dot on the other lane lies within `W` of it (inclusive). Colour conflicting dots and their bars in the palette's warning colour, others in the neutral accent. Under the lanes, print "claims shown: a + b, conflicts: k (x%)" and the expected number of conflicting claims in the picture, `2 × 10 s × λ × P`. Include a "new seed" button that advances both seeds by 1. When `λ` changes, regenerate from the same seeds so the picture changes smoothly with `λ`.
- **Right, the curve.** `P(conflict) = 1 − e^(−2 λ W)` for `λ` from 0.001 to 10 per second on a log x axis, y from 0 to 100%. A marker at the current `λ`. A dashed horizontal reference line labelled with the forward policy's average added latency `2d + T` in ms (as text, on a secondary label, since it is a different unit). Shade the region where `P` exceeds the tolerance slider value and label the crossover `λ* = −ln(1 − tol) / (2W)`.
- **Numbers panel.** `W` in ms, `2λW`, `P(conflict)` as a percent to 2 decimals, forward latency average and worst (`2d + T`, `2d + 2T`) in ms, `λ*` for the tolerance, and the conflicts counted in the current 10-second picture.

**Controls.**
- Claim rate `λ`: log slider 0.01 to 10 per second, default 0.5. Show the value to 2 significant figures. Preset chips for the table's five rates.
- Tick rate: select 10, 20, 30, 60 Hz (`T = 1 / rate`), default 10.
- Link delay `d`: slider 0 to 50 ms, step 1, default 1.
- Toggle "flush immediately" (sets `W = d` instead of `T + d`).
- Tolerance: select 0.1%, 1%, 5%, default 1%.
- Reset.

**Formulas.** `W = T + d` (or `d` when flushed), in seconds. `P = 1 − exp(−2 λ W)`. Forward average `= 2d + T`, worst `= 2d + 2T`. `λ* = −ln(1 − tol) / (2W)`.

**Test values** (10 Hz, `d = 1 ms`, not flushed unless stated): `W = 101 ms`. Forward average 102 ms, worst 202 ms. `λ = 0.01`: 0.20%. `λ = 0.1`: 2.00%. `λ = 0.5`: 9.61%. `λ = 2`: 33.24%. `λ = 5`: 63.58%. Flushed with `λ = 5`: 1.00%. Tolerance 1%: `λ* = 0.0498` per second. 30 Hz with `λ = 0.5`: `W = 34.3 ms`, 3.38%.

**First screen.** `λ = 0.5`, 10 Hz, not flushed, with the caption "Red dots: two players were both told they won."

**Accessibility.** All controls keyboard operable with visible focus. Announce `P(conflict)` and the conflict count in an `aria-live="polite"` region. No animation needed; with `prefers-reduced-motion`, skip any transition when regenerating dots. Palette from `templates/interactive-tokens.css`, light and dark. Do not rely on colour alone for conflicts: draw conflicting dots as hollow rings as well.
