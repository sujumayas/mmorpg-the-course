# MMO302 · Week 09 — Login, character select, gateway services

**Why this matters:** The first thing every player touches is the login path, and it fails in the most public way possible, on launch night, in front of everyone. A login queue that says "position 3,600" and then does not move for twenty minutes is a design error, not bad luck. This week you learn what happens between "Log in" and standing in the world, why a full server's queue moves at the speed players log out, and how to build the services around the world server so a crash or a launch does not take the whole game down.

**You will be able to:**
- Trace the login pipeline (authentication, realm list, character select, world entry) and say which stages are stateless and scale by adding machines.
- Compute the wait for a queue position at a full world server, `wait = position × L / C`, and the growth and drain of a queue from arrival rates.
- Design a signed session ticket that lets a world server admit a player without calling the login database, and list what it must contain.
- Size the jitter window that keeps a reconnect storm below the login tier's capacity after a crash.

**Before class:** TrinityCore source code (branch 3.3.5), read two short pieces with the comments: `World::AddQueuedPlayer` and `World::RemoveQueuedPlayer` in `src/server/game/World/World.cpp`, and the `HandleLogonChallenge` and `HandleLogonProof` functions in `src/server/authserver/Server/AuthSession.cpp`. You do not need to follow the C++ in detail. Read for what gets stored and when. Then read any short introduction to Little's law (the Wikipedia article is enough).

**Prerequisites from earlier courses:** [CS202 week 1, TCP vs UDP](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w01-networks-for-game-devs-tcp-vs-udp.md) (login uses a reliable, ordered connection). [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (the server decides, including who is allowed in). [DB201 week 7, Redis as a key-value store](../../DB201-data-persistence-and-telemetry/lectures/w07-nosql-and-key-value-stores-redis.md), which holds sessions in this week's design. [MMO302 week 1](w01-scale-targets-ccu-messages-and-n-squared.md) (peak concurrency and headroom) and [week 2 on shards, realms and layers](w02-shards-realms-zones-instances-layers.md). [MMO302 week 8](w08-item-ownership-and-transactional-integrity.md) (one owner at a time, which a login must respect).

**Interactive:** [examples/w09-login-queue.html](../examples/w09-login-queue.html). Keep it open during section 2.

---

## 1. From "Log in" to standing in the world

A player clicks "Log in" and, a few seconds later, stands in a town. In between, a well-designed MMO runs four stages, usually on different machines.

| Stage | What it does | What it reads | Keeps state per player? |
|---|---|---|---|
| Authentication | proves the player knows the password, issues a session | account row | no, after it answers |
| Realm or world list | shows which worlds exist, how full they are, where the player has characters | a small cached table | no |
| Character select | lists this account's characters on the chosen world | character summary rows | no |
| World entry | loads the full character, places them in a zone, starts the simulation | the full character, inventory, quests | yes, for the whole session |

The first three stages share a useful property. Each request is answered from the database or a cache, and the service forgets the player once it has answered. A service like that is called **stateless**. Stateless services scale by adding identical machines behind a load balancer, and two machines handle twice the logins. World entry is different. A world server holds the player in memory for hours, simulates them every tick, and owns them in the week 8 sense. You cannot add a second machine and split one player across them.

That split, stateless front stages and a stateful world, is the shape of every MMO login path. It explains most launch-night failures, which happen when the stateful part fills up and the stateless part keeps letting people through to wait.

### A real pipeline, read from source

TrinityCore, the open-source server emulator for the World of Warcraft 3.3.5 client, implements this pipeline in two programs, and the code is short enough to read.

- `authserver` listens on port 3724 by default. The client sends a logon challenge, and the server answers using **SRP6** (Secure Remote Password, version 6). SRP is a protocol in which the server stores a salted verifier instead of the password, and client and server each prove they know their side without the password crossing the network. If the proof checks out, both ends now share a **session key**. The auth server writes that key into the account's row in the database, then sends the realm list.
- `worldserver` listens on port 8085 by default. The client connects and sends an authentication packet. The world server looks up the account, reads the session key the auth server stored, and uses it to verify the client and to set up packet encryption. If the world is full, it puts the session in a queue instead of admitting it.

So the two programs never talk to each other directly. The database is the hand-off point, and the session key is the proof that login happened. Section 3 improves on this design. First, the queue.

## 2. Worked example: why the queue moves at the speed of logouts

### The hook

In August 2013, Final Fantasy XIV: A Realm Reborn relaunched to so much demand that its servers could not hold everyone who wanted to play. Players reported continued server problems through early access, and Square Enix did something few companies ever do on purpose. It temporarily stopped selling digital copies of its own game. It later compensated every player with a week of free play time.

Why stop selling? Surely the company could just let players queue. The model below shows why a queue at a full server can grow for hours while the servers themselves look healthy, and why cutting off new arrivals was one of only two levers available.

Look first at how TrinityCore decides who gets in. When a session leaves the world, `RemoveQueuedPlayer` checks whether the world is below its player limit. If so, it takes exactly one session from the front of the queue and initializes it. Then it sends every remaining queued player their new position. The queue advances by one player per player who leaves. The login servers may be able to process a thousand logins a second, and it makes no difference. At a full world, the admission rate is the logout rate.

### The model

Name the numbers.

- `C`, the world's capacity, the most players it admits at once.
- `L`, the average session length.
- `λ` (lambda), new players arriving at the login queue per minute.
- `μ` (mu), players admitted per minute.

At a full world, players leave at rate `C / L` (on average, each of the `C` players leaves once per `L` minutes), and each departure admits one queued player. So:

```
admission rate         μ = C / L                 (full world)
wait for position p    wait = p / μ = p × L / C
queue growth           Q(t) = (λ − μ) × t       while λ > μ
drain time             Q / (μ − λ_later)          once arrivals fall below μ
```

This is **Little's law** in disguise. For any stable queue, the average number waiting equals the arrival rate times the average wait. Here the world itself is the "queue" of length `C` with average stay `L`, so its throughput is `C / L`.

Two consequences stand out. The wait is proportional to `L`, so a game whose players stay longer has slower queues, and a good game is punished for being good. And the login tier's capacity does not appear anywhere in the formulas. You cannot fix a full-world queue by adding login servers.

### Numbers you can check

Take one world with `C = 3,000` and `L = 120` minutes. Then `μ = 3,000 / 120 = 25` admissions per minute.

| Queue position | Wait `p × L / C` |
|---|---|
| 100 | 4 min |
| 500 | 20 min |
| 1,500 | 60 min |
| 3,600 | 144 min |

Now an evening. The world starts full. For three hours, 45 new players per minute try to log in, then arrivals fall to 10 per minute. The queue grows at `45 − 25 = 20` per minute, so after 180 minutes it holds 3,600 people, and the last of them waits 144 minutes. Once arrivals fall to 10 per minute, it drains at `25 − 10 = 15` per minute, which takes `3,600 / 15 = 240` minutes. The last queue clears around 7 hours after it started.

This minute-by-minute simulation reproduces those numbers. Each minute, a fraction `1 / L` of online players leave, and the world fills its free slots from the front of the queue.

```python
C = 3000          # world server cap (players in the world)
L = 120           # average session length, minutes

def evening(arrivals, minutes, cap=C, session=L):
    """Minute-by-minute: a full world admits one queued player per logout."""
    online, queue, log = cap, 0, []
    for t in range(minutes):
        queue += arrivals(t)
        leaving = online / session            # logouts this minute
        online -= leaving
        admitted = min(queue, cap - online)   # fill the free slots from the queue
        queue -= admitted
        online += admitted
        log.append((t, round(queue)))
    return log

peak = lambda t: 45 if t < 180 else 10         # 45 new players/min for 3 h, then 10/min
log = evening(peak, 480)
for t, q in log[::60]:
    print(f"minute {t:3}: queue {q:5}")
print("queue empties at minute", next(t for t, q in log if t > 180 and q == 0))
```

It prints:

```
minute   0: queue    20
minute  60: queue  1220
minute 120: queue  2420
minute 180: queue  3585
minute 240: queue  2685
minute 300: queue  1785
minute 360: queue   885
minute 420: queue     0
queue empties at minute 419
```

Check minute 60 by hand. The queue gains 20 per minute and the log records it after each minute, so after 61 minutes it holds `61 × 20 = 1,220`. The drain from minute 180 runs at 15 per minute, and `3,600 / 15 = 240` minutes brings it to minute 420 (the simulation reaches zero a minute earlier because of rounding at the switch).

### Seeing it move

Open the interactive. The top view is the world: a population bar sitting at 3,000, flat and green. By every server metric, the world is fine. CPU is steady and the tick is on time. The bottom view is the queue over the evening, climbing in a straight line to 3,600, then draining for four hours. Drag `L` from 120 to 60 minutes and the climb flattens, because players leave twice as often. Drag `C` up to 6,000 and it vanishes. Now drag the login-tier capacity slider from 5 to 5,000 logins per second. Nothing changes. That flat response is the insight. The queue is set by `C / L`, and the part of the system most teams rush to scale has no effect on it.

Then press "add a layer at minute 120". A second copy of the world opens with another 3,000 slots, 2,420 queued players are admitted at once, and `μ` doubles to 50 per minute, which is above the 45 arriving. The queue never comes back.

### Cross-game recognition

Every queue fix changes one of three numbers: `λ`, `C` or `L`.

**TrinityCore (World of Warcraft 3.3.5 server emulator).** Exactly the model. The `PlayerLimit` setting is `C`, and admission happens only in `RemoveQueuedPlayer`, one session per departure. Each queued client is sent its new position whenever the queue moves. The emulator ships with `PlayerLimit = 0`, meaning no limit, which moves the problem from a queue to an overloaded world. That trade is the subject of the design judgment below.

**Final Fantasy XIV: A Realm Reborn (August 2013 launch).** Suspending digital sales lowered `λ`: fewer new accounts meant fewer people arriving at the queue. Square Enix also said it would create new servers, which raises `C`. Those are the two levers the model allows. The week of free time was compensation, not a fix.

**World of Warcraft Classic (2019 launch).** Blizzard ran the launch realms with **layering**: when a realm's outdoor world filled up, it created another copy of the whole world, each with its own players, monsters and resources. In the model, that raises `C` in steps of one world at a time without adding realms players must choose between. Layering was meant to be temporary, and Blizzard brought every realm down to a single layer in November 2019, once launch demand had passed. The cost shows up in the same source: players on different layers cannot see each other, and players used layers to exploit the economy (reaching fresh copies of rare spawns and resources).

**Outside games.** A theme-park ride's queue, a restaurant's waitlist and a support hotline all follow Little's law. The ride's throughput is fixed by seats per car and ride time, just as the world's is fixed by `C` and `L`. The queue-length signs at theme parks are `p / μ` computed from a measured throughput. Nobody thinks a second ticket booth speeds up the ride.

### Eyes-open design judgment

- **Show a wait estimate from measured `μ`, not a guess.** Count admissions over the last 10 minutes and divide. A position alone says nothing about the wait. "Position 1,500, about 60 minutes" lets players decide whether to wait, eat or leave.
- **Pick `C` from the world, not from the login tier.** The cap is the player count at which the busiest zone still makes its tick with headroom (week 1, week 5). Setting it higher empties the queue and moves the pain into the game: lag, monsters killed before they spawn, unplayable town squares. No cap at all (TrinityCore's default) is the choice for a private server with friends, not a launch.
- **Protect players who were disconnected.** A player who crashed out and comes back within a few minutes should skip the queue. Otherwise a server-side hiccup puts 3,000 people at the back of a 3,000-person line. Hold their slot for a grace period.
- **Adding worlds is permanent, adding layers is not.** New realms split communities for years, and some end up nearly empty after launch. Layers reverse cleanly but break the promise that everyone in a zone shares one world. Choose knowing which cost your game can carry.
- **Reduce `λ` last, and say so honestly.** Suspending sales costs revenue and good will. It is still better than selling copies to people who cannot play.

### Check this example

1. A world has `C = 5,000` and `L = 150` minutes. How long does position 2,000 wait?
2. With the section 2 numbers, how many arrivals per minute can the world absorb without a queue ever forming?
3. At minute 120 of the evening, the team raises `C` from 3,000 to 4,000 instead of opening a layer. How many queued players are admitted at once, what is the new `μ`, and does the queue keep growing?

<details>
<summary>Answers</summary>

1. `μ = 5,000 / 150 = 33.3` per minute, so `2,000 / 33.3 = 60` minutes.
2. Up to `μ = 25` per minute. Any more and the queue grows without limit.
3. 1,000 free slots admit 1,000 of the 2,420 waiting, leaving 1,420. The new `μ = 4,000 / 120 = 33.3` per minute. Arrivals of 45 per minute still exceed it, so the queue grows again at about 11.7 per minute until arrivals fall.

</details>

## 3. Gateway services and session tickets

### What a gateway does

A **gateway** (also called a front-end or proxy server) is the machine the game client actually connects to. It sits between the internet and the world servers and does four jobs.

- **Holds the connection.** It terminates the client's TCP or UDP session, handles encryption and keeps the connection open across zone changes. When a player crosses from one zone server to another (week 4), the client does not reconnect. The gateway reroutes its messages to the new zone server.
- **Checks identity once.** It verifies the session when the client connects, then tags every message with the account ID it proved. Zone servers trust the tag and never parse login credentials.
- **Routes.** It forwards movement and combat messages to the zone server that owns the player, chat to the chat service (week 10), and trade and auction requests to their services.
- **Absorbs abuse.** It rate-limits messages per connection and drops malformed packets before they reach the simulation.

EVE Online's server cluster, Tranquility, has the same split. CCP's 2015 dev blog on its third-generation hardware lists proxy nodes as a separate machine class from the SOL nodes that run the solar systems, with their own hardware specification. The simulation machines and the machines that face players are sized and scaled separately.

Sizing a gateway is mostly about connections, not CPU. Suppose each connection needs 64 kB of buffers and a gateway machine has 16 GB of RAM to spare for them. That is about 250,000 connections of memory, far more than the per-message CPU will support. At 20 messages per second per player and 5 microseconds of routing work per message, one core routes `1 / 0.000005 = 200,000` messages per second, which is 10,000 players per core. A 3,000-player world needs one gateway core, and you run two gateways so one can fail.

### Session tickets

TrinityCore hands the session from login to world through the database. The auth server writes the session key into the account row and the world server reads it back. That works, and it puts a database read on every world entry. It also means the world server cannot admit anyone while the account database is down.

The alternative is a **signed session ticket**. The login service, after checking the password, gives the client a short string that says "account 40213 may enter world-3 until time 1,060", plus a signature. The world server checks the signature with a secret key it shares with the login service, and checks the fields. It needs no database call. The signature is an **HMAC** (hash-based message authentication code), a keyed hash that only someone with the secret key can produce. Change one character of the ticket and the HMAC no longer matches.

```python
import hashlib, hmac

SECRET = b"shared-by-login-and-world-servers"   # in production: rotated, from a vault

def issue(account_id, world, now, ttl=60):
    body = f"{account_id}|{world}|{now + ttl}"
    tag = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()[:32]
    return f"{body}|{tag}"

def verify(ticket, world, now):
    account_id, w, expires, tag = ticket.split("|")
    body = f"{account_id}|{w}|{expires}"
    good = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()[:32]
    if not hmac.compare_digest(tag, good):
        return "reject: forged"
    if w != world:
        return "reject: wrong world"
    if now > int(expires):
        return "reject: expired"
    return f"accept account {account_id}"

t = issue(40213, "world-3", now=1_000)
print(t.split("|")[:3])
print(verify(t, "world-3", now=1_030))
print(verify(t, "world-3", now=1_090))
print(verify(t, "world-5", now=1_030))
print(verify(t.replace("40213", "1"), "world-3", now=1_030))
```

It prints:

```
['40213', 'world-3', '1060']
accept account 40213
reject: expired
reject: wrong world
reject: forged
```

The last line is the important one. A client that edits its ticket to claim account 1 fails the signature check. Each field earns its place:

- **Account ID,** so the world server knows who this is without asking.
- **Audience** (the world name), so a ticket stolen from world-3 is useless on world-5.
- **Expiry,** short (here 60 seconds), so a ticket copied from a log file or a stolen machine is worthless by the time anyone tries it.
- **Signature,** compared with `hmac.compare_digest`, which takes the same time whether the first byte or the last one differs. An ordinary `==` returns early on the first mismatch, and an attacker who measures response times can recover a valid tag byte by byte.

A signed ticket can be replayed within its lifetime. The fix follows week 8's pattern. Give each ticket a unique ID and have the world server record used IDs (in Redis, with the same 60-second expiry) and reject a second use. Also check that the account is not already in the world, and if it is, disconnect the old session first. Two copies of one character in two zones is a dupe waiting to happen.

### Character select is a read burst

Character select looks trivial, since it only lists five characters. At scale it is a read burst on the database, because it happens at the worst possible moment, right after a restart when everyone logs in at once. If 20,000 players log in over 5 minutes and each character-select screen costs three queries (account settings, character summaries, world population), that is `20,000 × 3 / 300 = 200` queries per second on top of normal load. Cache the summaries (name, level, class, zone, appearance) in Redis, update them on logout, and the database sees almost nothing.

## 4. Reconnect storms

A world server crashes with 20,000 players connected across its zones. Every client notices within a few seconds and tries to log back in. The login tier can process `A = 100` logins per second (SRP is deliberately expensive to compute, and each login reads the database). What happens next?

If every client retries immediately, 20,000 requests arrive in about 5 seconds, 4,000 per second, against a capacity of 100. After 30 seconds only 3,000 have been served. Clients that have waited 30 seconds time out and retry, adding their retries to the backlog, so the tier now receives more requests than there are players. The login service falls over, and a 2-minute world crash becomes a 30-minute outage. This is a **thundering herd**: many clients woken by the same event, all hitting the same service at once.

The fix is **jitter**. Each client waits a random delay, spread over a window `J`, before its first retry. Arrivals are then about `N / J` per second. To keep them below capacity:

```
N / J ≤ A     so     J ≥ N / A = 20,000 / 100 = 200 seconds
```

A 200-second window sounds long, but average wait is 100 seconds, every player gets in on the first try, and the login tier never overloads. Without jitter, many players wait far longer, some forever. For later retries, clients use **exponential backoff with jitter**: wait a random time between 0 and `base × 2^attempt` seconds, capped at a few minutes, so repeated failures thin out instead of piling up.

Two server-side measures work alongside client jitter. The login tier should reject excess requests quickly with a "try again in N seconds" answer, rather than accepting them and timing out, because a fast rejection costs almost nothing. And the grace-period rule from section 2 means a returning player skips the world queue, so the crash does not also create a 20,000-person line.

## In-class activity (25 minutes)

In groups of three. Your MMO launches next month with 8 worlds of `C = 4,000` each. By 20:00 on launch night every world is full. Marketing expects another 60,000 players to try logging in between 20:00 and midnight, spread evenly over the 4 hours and across the worlds. Playtests show `L = 150` minutes on launch night. The login tier handles 150 logins per second.

1. Compute the arrival rate per world and the admission rate `μ`. Does a queue form?
2. How long is each world's queue at midnight, and how long does the last player in it wait?
3. The team can open one extra layer per world at any time. When would you open it, and what happens to the queue?
4. At 21:00 one world crashes and its 4,000 players reconnect while the other 7 worlds keep receiving their arrivals. What jitter window keeps the login tier under capacity?

Expected output: arrivals are `60,000 / 8 / 240 = 31.25` per minute per world and `μ = 4,000 / 150 = 26.7`, so a queue forms and grows at about 4.6 per minute, reaching about 1,100 by midnight. The last player waits `1,100 × 150 / 4,000 ≈ 41` minutes. A layer opened at 20:00 raises `μ` to 53.3 and no queue forms; opening it later admits the whole queue at once. For the crash, the other worlds send `7 × 31.25 / 60 ≈ 3.6` logins per second, so `J ≥ 4,000 / (150 − 3.6) ≈ 27` seconds. Round up to 60 for safety.

## Common misconceptions

- **"The login servers are the bottleneck in a queue."** At a full world the queue moves at `C / L`, the logout rate. Login capacity matters for storms and for empty worlds filling up, not for a full-world queue.
- **"A queue position tells players how long they will wait."** Only when multiplied by `L / C`. Position 1,500 is 60 minutes on one world and 20 minutes on a world with three times the cap.
- **"Raising the cap is free."** It moves the wait from outside the world to inside it, as lag and crowding, and week 1's `n²` costs grow with it.
- **"A signed ticket is safe to reuse."** A signature proves the ticket is genuine, not that it is being used for the first time. Record used ticket IDs until they expire.

## Check yourself

1. A world with `C = 2,500` and `L = 90` minutes has 1,000 players queued. Arrivals are 20 per minute. How long does the last player wait, and does the queue grow or shrink?
2. Explain in two sentences why TrinityCore's world server can verify a client without talking to the auth server, and what it depends on instead.
3. A developer compares ticket signatures with `if tag == good:`. What attack does this allow, and what is the fix?
4. After a crash, 12,000 players reconnect to a login tier that handles 80 logins per second. What is the smallest jitter window that avoids overload? What is the average extra wait it adds?
5. A world's measured admission rate is 40 per minute, but `C / L` predicts 25. Name two reasons the measured rate could be higher.

<details>
<summary>Answers</summary>

1. `μ = 2,500 / 90 = 27.8` per minute, which exceeds arrivals of 20, so the queue shrinks at 7.8 per minute. The last of the current 1,000 waits `1,000 / 27.8 = 36` minutes, since players who arrive later join behind them and do not slow them down.
2. The auth server stores the session key it agreed with the client in the account's database row. The world server reads that key from the same database and uses it to check the client's proof, so the database, not a direct connection, is the link between them.
3. A timing attack. `==` stops at the first differing character, so an attacker who measures response times can learn how many leading characters of a forged tag are correct and build a valid tag piece by piece. Use a constant-time comparison such as `hmac.compare_digest`.
4. `J ≥ 12,000 / 80 = 150` seconds. The average added delay is `J / 2 = 75` seconds.
5. Any two of these. The cap was raised or a layer opened. Sessions are shorter than the assumed `L` tonight (on a patch day many people log in briefly). The world was not full, so free slots admitted players without waiting for logouts. (Players abandoning the queue do not count: they move you forward without raising admissions.)

</details>

## Lab / assignment hook

[Lab 09, login queue and session tickets](../labs/lab09.md). You build a discrete-time login service with a capped world, a queue with a reconnect grace period and abandonment, and a ticket issuer and verifier with replay protection, then check your queue against the section 2 formulas and your tickets against a battery of forged, expired and replayed tickets. Deliverable: the completed `login_service.py` passing the tests and a one-page launch plan for the in-class MMO.

## Sources

- TrinityCore, `src/server/game/World/World.cpp` (`AddQueuedPlayer`, `RemoveQueuedPlayer`, `GetQueuePos`), `src/server/authserver/Server/AuthSession.cpp`, `src/server/game/Server/WorldSocket.cpp`, `src/server/authserver/authserver.conf.dist` and `src/server/worldserver/worldserver.conf.dist` (branch 3.3.5, the World of Warcraft 3.3.5a client era, read September 2026). Admission of one queued session per departure; SRP6 logon challenge and proof; session key stored in the account row and read by the world server; `RealmServerPort = 3724`, `WorldServerPort = 8085`, `PlayerLimit = 0` (no limit). https://github.com/TrinityCore/TrinityCore
- Wikipedia, "Final Fantasy XIV: A Realm Reborn" (read September 2026). Early access from 24 August 2013, launch 27 August 2013, continued server issues, temporary suspension of digital sales, new servers promised, a week of free play time as compensation.
- Warcraft Wiki, "Layering" (read September 2026). Layering at the 2019 Classic launch, each layer a copy of the outdoor world with its own NPCs and resources; realms reduced to a single layer on 13 November 2019; criticism that layering split communities and was used to exploit the economy.
- CCP Games (2015, October 14). "Tranquility Tech III". EVE Online news. Proxy nodes listed as a separate machine class from SOL nodes.
- Python documentation, `hmac.compare_digest` (Python 3.13). Constant-time comparison to reduce timing attacks.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula L = λW". *Operations Research*, 9(3), 383-387.
- World capacities, session lengths, arrival rates, gateway sizes and login-tier capacities in sections 2 to 4 are invented teaching values.

## Interactive spec: examples/w09-login-queue.html

**The one insight:** at a full world, the login queue advances at the rate players log out, `C / L`. The world looks healthy while the queue explodes, and adding login capacity changes nothing. Only arrivals (`λ`), capacity (`C`) or session length (`L`) move the queue.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the world": a horizontal population bar from 0 to `C` (and to `2C` when a layer is open, drawn as a second bar), a "server health" badge that stays green whenever population is at or below capacity, and small readouts for logouts per minute and admissions per minute.
- View B, "the queue": a line chart of queue length against time, x from 0 to 480 minutes (18:00 to 02:00 on the axis labels), with the arrival rate drawn as a step function on a secondary axis. A draggable "you" marker on the queue line shows "position p, estimated wait p × L / C min" and, on hover or focus, the actual wait from the simulation (the time until the queue has admitted p people from that moment).

**Controls:**

- `C` slider, 500 to 10,000, step 100 (default 3,000).
- `L` slider, 15 to 300 minutes, step 5 (default 120).
- Peak arrivals `λ₁` slider, 0 to 200 per minute (default 45), peak duration 0 to 480 minutes (default 180), later arrivals `λ₂` 0 to 100 per minute (default 10).
- Login-tier capacity slider, 5 to 5,000 logins per second, log scale (default 100). It limits admissions per minute to `60 × capacity` and nothing else, so at defaults it has no visible effect. This is intentional and the caption says so when it is moved.
- "Add a layer at minute" input (default off; when on, default 120) which doubles `C` from that minute.
- Abandonment toggle: each queued player leaves the queue with probability `1/q` per minute, `q` slider 10 to 600 minutes (default off, 90).
- Play, pause and scrub along the time axis.

**Readout (always visible, `aria-live="polite"`):** `μ = C/L`, current queue, queue at minute 180, the minute the queue empties, and the wait at the back of the queue at its peak (`Q_peak × L / C`).

**Formulas:**

```
each minute t:
  queue  += λ(t)                    λ(t) = λ₁ if t < peak duration else λ₂
  online -= online / L              (logouts)
  admit   = min(queue, capacity(t) − online, 60 × login_capacity)
  queue  -= admit;  online += admit
  if abandonment: queue -= queue / q
start: online = C, queue = 0
estimated wait for position p = p × L / C
```

**Test values (must match):**

- Defaults: queue 20 at minute 0, 1,220 at 60, 2,420 at 120, 3,585 at 180, 2,685 at 240, 885 at 360, empties at minute 419. `μ = 25`. Peak back-of-queue wait 144 minutes (3,600 × 120 / 3,000).
- Position 1,500 at defaults: estimate 60 minutes.
- `C = 5,000`, `L = 150`: `μ = 33.3`; position 2,000 estimate 60 minutes.
- Layer at minute 120, defaults otherwise: the queue drops to 0 at minute 120 and stays at 0 (`μ` becomes 50, above 45).
- Login capacity changed from 100 to 5 per second at defaults (300 per minute): no change in any queue value.
- `L = 60`, defaults otherwise: `μ = 50`, no queue forms.

**First screen:** defaults, played to minute 180, the population bar full and green, the queue line at 3,585, and a caption: "The server is healthy. The queue is 3,585 people and 144 minutes long. Try adding login servers."

**Accessibility:** all controls keyboard operable with visible focus; the "you" marker movable with arrow keys (plus or minus 10 positions, Shift plus or minus 100); readout in an `aria-live="polite"` region; respects `prefers-reduced-motion` (no animated playback, jump to end) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
