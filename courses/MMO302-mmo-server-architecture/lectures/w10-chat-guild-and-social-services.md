# MMO302 · Week 10 — Chat, Guild and Social Services

**Why this matters:** Chat, friends lists and guild rosters look like small features next to combat and the world simulation. They are the parts of an MMO that touch every player at once, across every zone and every server process. A world server that handles 2,000 players can be brought down by one busy channel or by a guild of 1,000 logging in after maintenance, and the cause has the same shape every time. One event is copied to many receivers.

**You will be able to:**
- Compute the delivery rate, CPU cost and bandwidth of a chat channel from its size and posting rate, and explain why the cost grows with the square of the channel's size.
- Design a channel topology (scope, split, rate limit, delivery guarantee) for a stated player count and defend it with numbers.
- Implement a token-bucket rate limiter and a fan-out router, and measure their load against the model.
- Estimate a presence "login storm" and cut it with batching.

**Before class:** Discord Engineering, "How Discord Scaled Elixir to 5,000,000 Concurrent Users" (July 2017), the sections on guild processes and Manifold. Riot Games Tech Blog, "Chat Service Architecture: Servers" (September 2015). The Redis documentation page "Redis Pub/Sub", the sections on delivery semantics and sharded Pub/Sub. Reread MMO305 week 10, section 2.

**Prerequisites from earlier courses:** [MMO305 week 10, communication design](../../MMO305-social-systems-and-online-behaviour/lectures/w10-communication-design-chat-emotes-pings.md) (the reader's side of a channel, the saturation point `L*`, and why scope and splits exist; this week is the server's side of the same channel). [CS102 week 10, observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (subscribe and emit, the pattern a chat channel scales up). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). Transactions and Redis come from [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) and [DB201 week 7](../../DB201-data-persistence-and-telemetry/lectures/w07-nosql-and-key-value-stores-redis.md). From this course, [week 1, the n-squared problem](w01-scale-targets-ccu-messages-and-n-squared.md) (chat is its section on channels), [week 3, area of interest](w03-area-of-interest-grids-radius-hysteresis.md) and [week 9, the gateway](w09-login-character-select-gateway-services.md). Item transactions come from [week 8](w08-item-ownership-and-transactional-integrity.md).

**Interactive:** [examples/w10-chat-fanout.html](../examples/w10-chat-fanout.html). Keep it open during section 2.

---

## 1. Social services live beside the world, not inside it

In weeks 3 and 4 you split the world by space. A zone server owns a region of the map, and area of interest (AOI) decides which nearby players hear about an event. That works for anything that happens *somewhere*: a spell, a footstep, a shout.

A lot of what players send has no place. A guild message goes to guild members wherever they stand. A whisper goes to one named player, who may be on another continent served by another process. A friend logging in should light up your friends list whatever zone you are in. These messages are addressed by *identity*, not by *position*.

So most MMOs run a second family of processes beside the zone servers. Call them **social services**. The usual set is:

- **Chat.** Routes text on channels. Some channels are scoped by position (say, yell), some by place (a zone or city channel), and some by group (party, raid, guild, whisper).
- **Presence.** Tracks who is online, on which character, in which zone, and pushes changes to people who care: friends, guildmates, party members.
- **Friends and ignore lists.** A small social graph per player, stored durably.
- **Guild service.** Roster, ranks, permissions, message of the day, and often a shared bank.
- **Mail.** Store-and-forward messages, sometimes with items or gold attached.

In the reference stack for this course, the client connects to a **gateway** (week 9), which forwards world traffic to zone servers and social traffic to social services. Durable social data (friends, guild rosters, mail) lives in PostgreSQL. Fast, disposable state (who is online, which channel each session is in) lives in Redis or in the memory of the chat processes themselves.

Why separate them from the zone server? Three reasons you can measure.

1. **Different scaling axis.** A zone server's load grows with the players *in that zone*. A guild channel's load grows with the guild's online members, who are spread over every zone. Putting guild chat inside zone servers would force every zone server to talk to every other one.
2. **Different failure cost.** If chat restarts, players lose a minute of messages and complain. If a zone server restarts, players lose position, combat state and maybe items. Keeping them apart means a chat bug cannot crash combat.
3. **Different delivery needs.** Section 4 shows that each social feature wants a different guarantee, from "best effort" to "never lose it."

The rest of this lecture is about one number that decides whether these services survive a busy evening. That number is how many copies of each message the server has to make.

## 2. Worked example: the fan-out wall

### The hook

In July 2017 Discord's engineers described a problem with their largest communities. A Discord server (they call it a guild) is handled by one process on their backend. When anyone posts, that process sends a copy of the event to the session process of every connected member. Guilds with up to 30,000 people connected started to fall behind at peak hours. Each copy cost 30 to 70 microseconds to send, and publishing one event to a big guild took between 0.9 and 2.1 seconds.

Now multiply those two numbers yourself: 30,000 members at 30 µs is 0.9 s, and at 70 µs it is 2.1 s. The whole delay is the cost of one copy times the number of receivers. Nothing else is going on. And while one message took two seconds to fan out, more messages were arriving.

You met the same channel from the reader's side in MMO305 week 10. A big Trade channel scrolls too fast to read. Here you will see what the same channel costs the server, and why the cost grows much faster than the player count.

### The model

Take one channel with `L` members. Each member posts on average `q` messages per second. Every accepted message is copied to every other member.

```
messages in       m = q × L                   (per second)
copies out        D = m × (L − 1) = q × L × (L − 1)  ≈ q × L²
CPU               cores = D × t_send
bandwidth         bytes/s = D × S
one post's delay  (L − 1) × t_send            (if one process sends the copies in turn)
```

- `L` is the number of members connected to the channel, lurkers included.
- `q` is posts per member per second, averaged over everyone. MMO305 wrote it as `s × r`, the share who post times their rate.
- `D` is **fan-out**, the number of copies the server sends per second. One message to `L − 1` receivers is a fan-out of `L − 1`.
- `t_send` is the CPU time to make and hand off one copy (serialize, queue on the socket, account for it).
- `S` is the bytes on the wire per copy, headers included.

The important line is the second one. The inbound rate `m` is linear in `L`. The outbound rate `D` is `m` times `L` again. Double the channel and you double the posts *and* double the receivers of each post, so you quadruple the work. This is the n-squared problem from week 1 in its simplest form, with no positions or movement involved.

The last line is a separate problem. Even if total CPU is fine, a single process that sends copies one by one makes the *last* receiver wait `(L − 1) × t_send` for each message. That delay is linear in `L`, and it is the one Discord hit first.

### Numbers you can check

Use MMO305's channel. One member in ten posts, each poster sends one message every two minutes, so `q = 0.1 × 0.5 / 60 ≈ 0.000833` posts per member per second. Take `t_send = 50 µs`, the middle of Discord's measured range, and `S = 200` bytes per copy.

```python
q = 0.05 / 60      # posts per listener per second (MMO305 week 10: s = 0.1, r = 0.5 per minute)
t_send = 50e-6     # CPU-seconds per delivered copy (Discord measured 30-70 us per send)
size = 200         # bytes per delivered copy, headers included

print(f"{'L':>7} {'posts/s':>8} {'copies/s':>10} {'cores':>7} {'Mbit/s':>8} {'one post':>9}")
for L in [400, 1_000, 3_000, 10_000, 30_000]:
    posts = q * L                    # messages in per second
    copies = posts * (L - 1)         # every other member gets a copy
    cores = copies * t_send
    mbit = copies * size * 8 / 1e6
    one_post_ms = (L - 1) * t_send * 1000
    print(f"{L:>7,} {posts:>8.2f} {copies:>10,.0f} {cores:>7.2f} {mbit:>8.1f} {one_post_ms:>6.0f} ms")
```

It prints:

```
      L  posts/s   copies/s   cores   Mbit/s  one post
    400     0.33        133    0.01      0.2     20 ms
  1,000     0.83        832    0.04      1.3     50 ms
  3,000     2.50      7,498    0.37     12.0    150 ms
 10,000     8.33     83,325    4.17    133.3    500 ms
 30,000    25.00    749,975   37.50   1200.0   1500 ms
```

Check the 3,000 row by hand. 3,000 members at 0.000833 posts each is 2.5 posts per second. Each post goes to 2,999 others, so about 7,500 copies per second. At 50 µs each that is 0.375 seconds of CPU every second, a bit over a third of a core. At 200 bytes each it is 1.5 MB/s, or 12 Mbit/s. (The 1,000 row's exact value is `0.833 × 999 = 832.5` copies a second. Python rounds an exact half to the even digit, so it prints 832.)

Now read down the columns. From 3,000 to 30,000 members, the posts per second grow 10 times. The copies, cores and bandwidth grow 100 times. At 30,000 members a single channel needs 37.5 cores and 1.2 Gbit/s of outbound traffic. And the last column says a single-process design needs 1.5 seconds to push out *one* post, while 25 new posts arrive every second. That process falls behind by 36.5 seconds of work every second. This is the regime Discord described.

### A visual the student can move

Open `examples/w10-chat-fanout.html`. The left panel shows what one reader experiences, the messages per second arriving in their chat window. It is a straight line in `L`. The right panel shows what the server does, the copies per second. It is a parabola, drawn against a horizontal line for the cores you have. Drag `L` from 400 to 30,000. The left line climbs politely. The right curve crosses your core budget and leaves the chart.

Then use the split control. Splitting the channel into `k` equal channels divides both the reader's rate and the server's copies by `k`. Turn on "parallel fan-out" and watch the one-post delay drop while the total cores stay the same. The two panels show that the reader's problem and the server's problem have the same cure, and that the server's problem is the steeper one.

### Rewriting the levers in the model

Every chat design choice changes one symbol.

- **Scope cuts `L`.** A zone channel only holds players in that zone. A proximity channel holds only players within a radius, which is an AOI query from week 3.
- **Splitting cuts `L` per channel.** `k` channels of `L/k` members produce `q × L × (L/k − 1)` copies in total, about `1/k` of the unsplit load. Splitting 30,000 members into 100 channels of 300 drops copies from 750,000 to 7,475 per second.
- **Rate limits cap `q`** for the heaviest posters. Section 5 builds one.
- **Parallel fan-out cuts the one-post delay** by spreading the copies over `P` workers: `(L − 1) × t_send / P`. It does not cut total CPU.
- **Batching cuts `t_send` and `S` per copy.** Sending one packet with five messages to a client costs less than five packets. It does not change the number of message copies.
- **Pulling instead of pushing** removes copies to readers who are not looking. If a client only fetches a channel while its tab is open, `L` becomes "members with the tab open."

### Cross-game recognition

**World of Warcraft (current retail, Warcraft Wiki "Chat").** WoW's channel list reads like a table of scopes. Say reaches players within 60 yards and yell within 400 yards, both proximity channels. General and Local Defense are per zone. Trade works only in capital cities and is shared across them. Looking for Group is global per faction and was mostly used in classic. Party, raid, guild and officer are group channels, and whispers go to one player. In the model, every one of these is a choice of `L`. The only global public channel is the one players join for a narrow purpose.

**Discord (2017).** Discord's fix is our parallel fan-out lever. Their Manifold library groups the receiving sessions by the machine they live on and sends one message per machine, where local workers do the final copies. Total copies stay `L − 1` per post. The per-process serial work drops from `L − 1` sends to about one send per remote machine, so the one-post delay stops growing with `L` at the same rate.

**League of Legends chat (Riot Games, 2015).** Riot's chat runs on XMPP, the Extensible Messaging and Presence Protocol, with servers written mostly in Erlang and started from the open-source ejabberd. In 2015 Riot reported routing about a billion events a day, and it counted presence updates alongside messages. Each region had its own cluster of six to twelve machines, sized so half of them could shut down without interrupting service. In the model, Riot's `L` for each post is small (a friend, a lobby, a team), and the volume comes from the number of small channels. The next section is about the event type that makes up much of that billion.

**Redis Pub/Sub (Redis documentation, current).** If you build chat on Redis, the documentation states the cost of `PUBLISH` as `O(N + M)`, where `N` is the number of subscribers to the channel and `M` the number of pattern subscriptions. That `N` is our `L − 1`. Redis does the fan-out inside one server process, so the serial-delay line of our model applies to it directly. Redis 7 added **sharded Pub/Sub**, which keeps each channel's traffic inside one shard of a cluster. That lever spreads *different* channels over machines. It does not help one huge channel.

### Eyes-open design judgment

The model tells you that a public channel has a cost that grows with the square of its membership, and it tells you where to spend.

- **Default every public channel to a scope.** A global channel is a decision, not a starting point. If a design document says "global chat," ask for the expected `L` and `q` and do the table above before anyone writes code.
- **Split by topic before you split by shard.** Topic splits (trade, services, looking-for-group) cut `L` *and* help readers, as MMO305 showed. Hash splits ("Trade 1", "Trade 2") cut `L` just as well but break the market in two, because a seller in Trade 1 cannot reach a buyer in Trade 2.
- **Parallel fan-out buys latency, not capacity.** Discord's fix was right because their pain was the one-post delay. If you are CPU bound in total, more workers only move the bill.
- **Push is expensive, and players do not read most of it.** MMO305 showed that a saturated reader sees only a share `R / (60 × m)` of the messages (`R` is per minute, `m` here is per second). Every copy beyond that is sent, paid for, and scrolled past. A design that sends only the newest `R` messages per second to each reader, or pulls on demand, can cut `D` far below `q × L²` without any player noticing.

### Check this example

1. A zone channel has 2,000 members and `q = 0.002` posts per member per second. How many copies per second? At 40 µs per copy, what share of one core?
2. You split that channel into four topic channels, and each player joins two of them. What happens to total copies? Assume posts spread evenly over the four channels.
3. A single-process chat server must deliver each post to all members within 250 ms. At `t_send = 50 µs`, what is the largest channel it can serve?

<details>
<summary>Answers</summary>

1. `m = 0.002 × 2,000 = 4` posts per second, `D = 4 × 1,999 = 7,996` copies per second. CPU is `7,996 × 40 µs ≈ 0.32` s per second, about 32% of a core.
2. Each channel has `2,000 × 2 / 4 = 1,000` members and receives a quarter of the 4 posts per second, so 1 post per second. Copies per channel `= 1 × 999`, total `4 × 999 = 3,996`, about half the original. Joining two of four channels is like having half the members per channel.
3. `(L − 1) × 50 µs ≤ 0.25 s` gives `L − 1 ≤ 5,000`, so `L ≤ 5,001`.

</details>

## 3. Presence and the login storm

Presence is fan-out without anyone typing. When you log in, the presence service tells everyone who has you on their friends list, and everyone online in your guild, that you are here. When you change zone, it may tell them again. When you log out, it tells them once more.

### The model

Take a guild of `G` members who all log in over a window of `T` seconds, spread evenly. When the `i`-th member logs in, `i − 1` members are already online and each gets a notification. Total packets:

```
push packets = 0 + 1 + 2 + … + (G − 1) = G × (G − 1) / 2
```

That is the n-squared shape again. A guild of 1,000 is the largest World of Warcraft allows (a cap added in patch 4.0.1, 2010). If all 1,000 log in over the ten minutes after a server restart, the guild alone generates `1,000 × 999 / 2 = 499,500` presence packets. Most realms hold many guilds, and friends lists add more on top.

### Batching

Presence is a good place to trade a little freshness for a lot of packets. Instead of pushing each login as it happens, collect logins for `B` seconds and send each online member one packet that lists everyone who arrived in that window. New arrivals download the whole roster once at login, so they need no batch for the window they joined in.

```python
MEMBERS, WINDOW, BATCH = 1_000, 600, 5    # guild size, login window (s), batch period (s)
logins = [i * WINDOW / MEMBERS for i in range(MEMBERS)]   # one login every 0.6 s

# Push: each login sends one packet to every member already online.
push = sum(range(MEMBERS))

# Batch: at the end of each 5 s window, every member who was online when the
# window opened gets one packet listing that window's logins. New arrivals
# download the whole roster once when they log in, so they are not counted here.
batch = 0
for start in range(0, WINDOW, BATCH):
    online_before = sum(1 for t in logins if t < start)
    if any(start <= t < start + BATCH for t in logins):
        batch += online_before
print(f"push:  {push:,} packets")
print(f"batch: {batch:,} packets, {push / batch:.1f}x fewer")
```

It prints:

```
push:  499,500 packets
batch: 59,540 packets, 8.4x fewer
```

The saving is close to the number of logins per batch window, `B × G / T = 5 × 1,000 / 600 ≈ 8.3`. The cost is that a friend's name turns green up to five seconds late. Nobody has ever filed a bug about that.

Two more presence levers are worth knowing. **Interest filtering** sends roster updates only to clients that have the roster panel open, and sends the rest a count ("312 online"). **Coalescing** replaces a pending update instead of queuing a second one, so a player who changes zone three times in five seconds costs one packet, not three.

### Why presence dominates

Riot counted presence together with messages when it reported a billion events a day. The reason is structural. A message is sent when a person chooses to type. A presence update is sent every time anyone logs in, logs out, changes zone, starts a match or goes idle, to everyone who might care. In a game with large friends lists and large guilds, presence can outnumber chat. Budget for it first.

## 4. Guilds, mail and choosing a delivery guarantee

Not every social message deserves the same effort. The useful question is what happens if one copy is lost.

| Feature | If a copy is lost | Guarantee to build | Where the truth lives |
|---|---|---|---|
| Zone and trade chat | Nobody notices | At most once | Nowhere; memory only |
| Presence | Wrong dot color until the next update | At most once, plus a full refresh on reconnect | Redis (who is online now) |
| Guild chat | Mildly annoying | At most once live, recent history on login | A short capped list per guild |
| Whisper | The recipient misses a direct message | At least once while online | Memory, plus an offline queue if you support it |
| Guild roster, ranks | Wrong permissions | Transactional | PostgreSQL |
| Mail with items or gold | Lost or duplicated property | Exactly-once effect | PostgreSQL, in one transaction with the items |

**At most once** means each copy is sent once and may be lost. Redis Pub/Sub works this way, and its documentation says a message the subscriber cannot handle is lost for good. That is fine for public chat.

**At least once** means the sender retries until it gets an acknowledgment. The receiver may then see a duplicate, so each message carries an id and the receiver drops ids it has seen.

**Exactly-once effect** is what you need for anything that moves property. Mail with an attached sword is an item transfer, and it must follow the rules of week 8: one database transaction that removes the item from the sender's inventory and creates the mail row. A second transaction moves it from the mail row to the recipient when they collect it. Retrying the collection is safe because the second attempt finds the mail row already emptied. DB201 weeks 5 and 6 cover why this has to be a transaction.

A guild is a good example of the **single-writer** rule. Give each guild one owner process at a time, the way Discord gives each guild one process. Every change to the roster, ranks or bank goes through that owner, which applies changes in order and writes them to PostgreSQL. Two officers who promote and kick the same member at the same moment are then two messages in one queue, not two writers racing in the database. When the owner process moves (a restart, a rebalance), it reloads the guild from PostgreSQL. A guild bank still needs week 8's item transactions, because items cross the boundary into player inventories owned by other processes.

## 5. Rate limiting with a token bucket

The fan-out table assumed an average `q`. Real channels have a few players who post far more than average, and a spam bot can post as fast as its connection allows. A rate limit caps each sender's `q`.

The standard tool is the **token bucket**. Each sender has a bucket holding up to `capacity` tokens. Tokens refill at `rate` per second. Sending costs one token. If the bucket is empty, the message is dropped (or the sender is told to wait). The capacity allows a short burst, such as a raid leader typing three quick orders. The rate sets the long-run limit.

```python
class TokenBucket:
    """Allow bursts of `capacity` messages, refilled at `rate` tokens per second."""
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity
        self.last = 0.0

    def allow(self, now):
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

bucket = TokenBucket(capacity=3, rate=0.2)      # burst of 3, then one message per 5 s
sends = [0.0, 0.5, 1.0, 1.5, 2.0, 6.0, 7.0, 12.0]
print([("ok" if bucket.allow(t) else "drop") for t in sends])
```

It prints:

```
['ok', 'ok', 'ok', 'drop', 'drop', 'ok', 'drop', 'ok']
```

Trace it. The bucket starts with 3 tokens. The first three sends spend them, with a little refill in between (0.1 token per half second), leaving 0.2. At 1.5 s and 2.0 s the bucket holds 0.3 and 0.4, so both drop. By 6.0 s it has refilled to 1.2, so one message passes. At 7.0 s it holds 0.4 and drops. By 12.0 s it holds 1.4 and passes.

Three design points follow from the model.

1. **Limit per channel scope, not per player only.** A raid channel of 20 can let its leader post five times a second without hurting anyone, because `L` is 20. A realm-wide channel cannot. Tie the bucket's rate to the channel's `L`.
2. **Charge by copies, not by messages, if you must pick one number.** A post to a 5,000-member channel costs the server `4,999 / 19 ≈ 263` times more than a post to a 20-member raid. Some games make the cost visible to players, for example with a longer cooldown on wide channels.
3. **Drop silently, or tell the sender?** A visible "you are sending messages too fast" teaches legitimate players the limit. A silent drop (the sender sees their own message, nobody else does) frustrates spammers, who cannot tell they have been limited. Many games do both. They show the warning for mild overuse and drop silently for accounts flagged as bots (MMO309 covers bot detection).

## In-class activity (25 minutes)

Groups of three. You are the server team for an MMO with 12,000 peak concurrent players on one realm, split over 40 zones and 4 capital cities. Design reports say 30% of players are in capitals at peak, and a member posts to public channels at `q = 0.001` per second.

1. Compute copies per second for one realm-wide Trade channel that everyone in a capital joins (3,600 members). Use `t_send = 50 µs`.
2. Compute the same if Trade is per capital city, with players spread evenly.
3. Propose one more lever from section 2 and compute its effect.
4. Write the delivery-guarantee row of the section 4 table for a new feature your group invents (for example, "guild event sign-ups").

Expected output: three numbers, one lever with its numbers, one table row, and a sentence on what players lose with your design.

## Common misconceptions

- **"Chat is cheap because messages are small."** The size of one message barely matters. The number of copies is what costs, and it grows with `L²` for a public channel.
- **"Add more servers and a big channel scales."** More workers cut the time to send one post. Every copy still has to be made, so the total CPU and bandwidth do not change. Only cutting `L` or `q` does that.
- **"Sharded Pub/Sub fixes a huge channel."** It spreads different channels across machines. One channel with 30,000 subscribers still lives on one shard.
- **"All messages need guaranteed delivery."** Public chat can lose a copy and nobody notices. Guaranteeing it costs acknowledgments and retries on every copy. Pay for guarantees where property or trust is at stake, like mail with items.

## Check yourself

1. A city channel has 1,500 members and `q = 0.001`. Another design joins three such cities into one Trade channel. Compute copies per second for both designs. By what factor does the shared channel cost more than one city channel, and why is it not 3?
2. A guild of 400 logs in over 200 seconds. How many presence packets without batching? About how many with 4-second batches?
3. A player sends messages at 0, 0.2, 0.4, 0.6 and 10 seconds against a bucket with capacity 2 and rate 0.25 per second. Which pass?
4. A designer wants mail to arrive "instantly, always, and never twice." Which part of that sentence needs a database transaction, and which can use at-most-once push?

<details>
<summary>Answers</summary>

1. One city: `m = 1.5` posts per second, `D = 1.5 × 1,499 ≈ 2,249` copies per second, so three separate cities total `6,746`. Shared: `L = 4,500`, `m = 4.5`, `D = 4.5 × 4,499 ≈ 20,246`. The shared channel costs about 3 times the three separate ones combined, and 9 times one city channel. Tripling `L` triples both posts and receivers per post.
2. Push: `400 × 399 / 2 = 79,800`. Batching saves about `B × G / T = 4 × 400 / 200 = 8` times, so about 10,000 packets. The exact count is 9,800: 50 windows, with `8 × j` members online when window `j` opens, and `8 × (0 + 1 + … + 49) = 9,800`.
3. Start with 2 tokens. 0 passes (1.0 left). 0.2 refills to 1.05 and passes (0.05). 0.4 has 0.1 and drops. 0.6 has 0.15 and drops. At 10 s it has refilled to the capacity of 2 and passes. So 0, 0.2 and 10 pass.
4. "Never twice" and "always" for the attached items need the transactional path. One transaction creates the mail and removes the item from the sender, and a second one claims it. "Instantly" is a notification, which can be at-most-once push, because the mailbox is re-read from the database when the recipient opens it.

</details>

## Lab / assignment hook

[Lab 10, chat router under load](../labs/lab10.md). You implement the token bucket and a fan-out router in Python, simulate a Trade channel at 400, 1,000 and 3,000 members, check the copies against this lecture's model, then measure what splits, spam and rate limits do. Deliverable: code, a results table and a one-page channel design for the in-class activity's realm.

## Sources

- Discord Engineering, "How Discord Scaled Elixir to 5,000,000 Concurrent Users" (6 July 2017). Guild processes fan out every event to each connected session; guilds of up to 30,000 concurrent users; 30 to 70 µs per `send/2`; 900 ms to 2.1 s to publish an event in a large guild; the Manifold library, which groups sends by remote node.
- Riot Games Tech Blog, "Chat Service Architecture: Protocol" (24 July 2015). XMPP chosen for messaging and presence; servers based on open-source ejabberd, later rewritten.
- Riot Games Tech Blog, "Chat Service Architecture: Servers" (23 September 2015). Chat servers about 90% Erlang and 10% C; per-region clusters of six to twelve machines sized to lose half without interruption; about a billion routed events a day including presences, messages and IQ stanzas.
- Warcraft Wiki, "Chat" (accessed September 2026, current retail with classic notes). Say within 60 yards, yell within 400 yards; General and Local Defense per zone; Trade in cities, shared across them; Looking for Group global per faction.
- Warcraft Wiki, "Guild" (accessed September 2026). Guild member cap of 1,000 introduced in patch 4.0.1 (2010).
- Redis documentation, `PUBLISH` command (complexity `O(N+M)`), and "Redis Pub/Sub" (at-most-once delivery; sharded Pub/Sub from Redis 7.0). Accessed September 2026.

## Interactive spec: examples/w10-chat-fanout.html

**Insight the visual must make obvious:** what one reader sees grows in a straight line with channel size, while what the server must send grows as a parabola. Splitting the channel divides both by `k`; parallel fan-out shortens the delay for one post but does not reduce total cores.

**Layout.** Two linked charts side by side on desktop, stacked under 700 px (reader chart first), with a number panel beneath. Shared x axis: channel members `L`, log scale from 100 to 50,000, with tick labels at 100, 1k, 10k, 50k.

**Left chart, "What a reader sees".** y axis: messages per second arriving in one member's window for their channel, `m_c = q × L / k`, linear, auto-scaled with a minimum top of 5. Draw a dashed horizontal line at `R / 60` labelled "reading budget" (default `R = 20` per minute, from MMO305). Marker at the current `L`.

**Right chart, "What the server sends".** y axis: copies per second, `D = q × L × (L/k − 1)`, log scale from 10 to 10^7. Draw a horizontal line at the core budget, `cores × 1 / t_send` copies per second, labelled "N cores". Shade the region above it. When `D` exceeds it, the number panel shows "over budget by X cores" in the warning color. Marker at the current `L`.

**Controls.**
- `L`: slider, 100 to 50,000 on a log scale, default 3,000. Also a numeric input.
- `q` posts per member per second: slider 0.0001 to 0.01, log scale, default 0.000833 (shown as "0.05 per minute").
- `k` split: stepper 1 to 100, default 1.
- `t_send`: slider 10 to 100 µs, default 50.
- Core budget: stepper 1 to 64, default 4.
- `P` parallel fan-out workers: stepper 1 to 64, default 1.
- `S` bytes per copy: stepper 50 to 1,000, default 200.
- Preset buttons: "MMO305 channel (L = 3,000)", "Discord 2017 (L = 30,000, q = 0.000833, t_send = 50 µs)", "Split 100 ways".

**Number panel** (all live): posts in per second `q × L`; copies per second `D`; cores `D × t_send`; outbound Mbit/s `D × S × 8 / 10^6`; one-post delay `(L/k − 1) × t_send / P` in ms; reader messages per second `m_c`.

**Formulas.** `m = q × L`. Per-channel members `n = L / k`. `D = q × L × (n − 1)`. `cores = D × t_send`. `delay = (n − 1) × t_send / P`. `Mbit/s = D × S × 8 / 1e6`.

**Test values** (assert on load, with `q = 0.05/60`, `t_send = 50 µs`, `S = 200`, `k = 1`, `P = 1`):

| L | posts/s | copies/s | cores | Mbit/s | one post |
|---|---|---|---|---|---|
| 400 | 0.33 | 133 | 0.01 | 0.2 | 20 ms |
| 3,000 | 2.50 | 7,498 | 0.37 | 12.0 | 150 ms |
| 30,000 | 25.00 | 749,975 | 37.50 | 1,200.0 | 1,500 ms |

With `L = 30,000` and `k = 100`: copies/s 7,475, cores 0.37. With `L = 30,000`, `k = 1`, `P = 30`: one post 50 ms, cores still 37.50.

**First screen:** `L = 3,000`, `k = 1`, caption "3,000 members: 2.5 posts a second in, 7,498 copies a second out. Drag to 30,000: ten times the posts, a hundred times the copies."

**Accessibility.** All controls keyboard reachable; the number panel is an `aria-live="polite"` region; the over-budget warning uses text as well as color.
