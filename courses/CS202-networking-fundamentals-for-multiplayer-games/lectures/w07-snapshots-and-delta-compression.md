# CS202 · Week 07 — Snapshots and delta compression

**Why this matters:** An authoritative server has to tell every client what the world looks like, many times a second, over a network that loses packets. Send the whole world every time and you run out of bandwidth. Send only the changes and one lost packet can leave a client wrong for the rest of the match. This week gives you the model that makes deltas both small and safe, and the numbers to size them.

**You will be able to:**
- Compute the size of a full snapshot and of a delta snapshot from entity count, field sizes and change rates.
- Explain why a delta must be encoded against the newest snapshot the client has *acknowledged*, and predict what goes wrong if it is not.
- Compute how delta size grows with the age of the baseline, and choose when to fall back to a full snapshot.
- Implement a delta encoder and decoder for a field-masked entity format in Python.

**Before class:** Glenn Fiedler, "Snapshot Compression" (Gaffer on Games, January 2015), the sections on delta compression. Frohnmayer, M. & Gift, T., "The TRIBES Engine Networking Model" (Dynamix, undated), the ghost manager section (about 2 pages). Valve Developer Community, "Source Multiplayer Networking", the paragraph on delta compression.

**Prerequisites from earlier courses:** [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (the server keeps a ring of recent snapshots per client, looked up by tick). [CS202 week 1](w01-networks-for-game-devs-tcp-vs-udp.md) (28-byte UDP/IPv4 header, why state goes over UDP). [CS202 week 3](w03-topologies-peer-to-peer-client-server-relay.md) (server upload `n × r × (n × s + h)`, the formula this week shrinks). [CS202 week 5, serialization and bit packing](w05-serialization-and-bit-packing.md) (the `struct` module and quantization) and [CS202 week 6, reliability over UDP](w06-reliability-over-udp.md) (sequence numbers and acks, which this week uses without re-teaching).

**Interactive:** [examples/w07-delta-baseline.html](../examples/w07-delta-baseline.html). Keep it open during section 2.

---

## 1. What a snapshot is

The server runs the game in fixed steps called **ticks** (CS101 week 9's fixed timestep, now on a server). After some ticks it takes a **snapshot**, a record of the state of every **entity** (player, projectile, door, pickup) that one client needs to see, and sends it to that client. The client draws the world from the snapshots it receives.

There are two ways to keep a client's copy of the world in step with the server's.

- **Send events.** "Door 12 opened." "Player 3 moved to (40, 7)." Every event must arrive, in order, or the client's copy drifts. That means reliable delivery, and week 1 showed what reliable delivery costs when a packet is lost.
- **Send state.** "Here is what the world looks like at tick 812." A snapshot replaces what the client had. If one is lost, the next one makes up for it. No retransmission needed.

Fast games send state for anything that changes often, and reliable events for the rest (a chat line, a match result). This week is about the state half.

### The size of a full snapshot

Take the running example for this week, an arena with 16 players and 48 props (doors, pickups, destructible crates), 64 entities in all. Each entity has five fields.

| Field | Type | Bytes |
|---|---|---|
| `x`, `y` | 32-bit float each | 8 |
| `yaw` (facing) | 16-bit unsigned | 2 |
| `hp` | 8-bit unsigned | 1 |
| `anim` (animation state) | 8-bit unsigned | 1 |
| **Entity state** | | **12** |

A full snapshot writes a 10-byte header (the tick, a baseline tick that we will need shortly, and an entity count), then a 2-byte id and 12 bytes of state for each entity.

```
full = 10 + E × (2 + 12)          E = entities
     = 10 + 64 × 14 = 906 bytes
```

With the 28-byte UDP/IPv4 header from week 1, one full snapshot is 934 bytes on the wire. At 20 snapshots a second that is 18,680 bytes per second, or 149.4 kbit/s, to *each* client. A 16-player server sends 16 of those streams, about 2.4 Mbit/s. Week 3's formula said the server's upload grows with `n²`. This week attacks the other factor, the bytes per entity.

The waste is easy to see. Between two ticks, 50 ms apart, the 48 props almost never change. A door that has been open for a minute is sent 1,200 times, open every time.

## 2. Worked example: the baseline must be one the client has

### The hook

*Quake III Arena* (id Software, 1999) sends its snapshots as plain unreliable UDP. The server never retransmits a lost snapshot. Yet every snapshot is a **delta**, a list of changes from some earlier snapshot, and a client that misses one never ends up with a wrong world. In id's source code, released in 2005, each client's snapshot records the number of the last snapshot the client acknowledged, and the server encodes the next delta against *that* one, even when newer snapshots have already been sent. On purpose, the server sends a slightly bigger delta than it could. This section is about why that is the right trade.

### The model

A **delta snapshot** lists only the entities whose state differs from a **baseline**, an earlier snapshot the client is assumed to hold. For each changed entity it writes the id, a one-byte **field mask** (bit `i` set means field `i` is present), and the new absolute value of each changed field. Unchanged entities are not written at all.

```
delta = 10 + Σ over changed entities of (2 + 1 + bytes of its changed fields)
```

For this arena, a moving player changes `x`, `y` and `yaw` every tick, which costs `3 + 4 + 4 + 2 = 13` bytes. A prop that changes (a crate takes damage, a pickup respawns) changes `hp` and `anim`, which costs `3 + 1 + 1 = 5` bytes. Suppose `P` players move every tick and each of the `Q` props changes with probability `p` per tick. Against a baseline `k` ticks old, a prop appears in the delta if it changed at least once in those `k` ticks, which by the complement rule has probability `1 − (1 − p)^k`.

```
expected delta(k) = 10 + 13P + 5Q × (1 − (1 − p)^k)
```

- `k` is the **baseline age**, how many ticks separate the snapshot being sent from its baseline.
- `P = 16`, `Q = 48`, `p = 0.02` in our arena.

Now the rule that the hook is about. The client can only decode a delta if it holds the baseline. The server learns what the client holds from **acknowledgements** (acks), the "I received snapshot 812" numbers that ride back on the client's own packets (week 6). So:

```
baseline = the newest snapshot the client has acknowledged
k        ≥ round trip time / snapshot interval
```

At 20 Hz and a 100 ms round trip, an ack for snapshot `t` reaches the server around tick `t + 2`, so `k` is at least 2 even on a perfect network.

### Numbers you can check

Sizes for one snapshot, from the formulas above:

| What is sent | Payload | On the wire (+28) | At 20 Hz |
|---|---|---|---|
| Full snapshot, 64 entities | 906 B | 934 B | 149.4 kbit/s |
| Delta, 16 players moving, 1 prop changed | 10 + 16 × 13 + 5 = 223 B | 251 B | 40.2 kbit/s |
| Delta, nobody moving (between rounds) | 10 B | 38 B | 6.1 kbit/s |
| Delta, all 64 entities change all fields | 10 + 64 × 15 = 970 B | 998 B | 159.7 kbit/s |

Two rows deserve a sentence. The typical delta is 4.1 times smaller than the full snapshot. And the last row is *bigger* than a full snapshot, because every entity pays a mask byte on top of all its fields. An encoder should compute both and send the smaller one.

Now vary the baseline age. Each extra tick of age gives the props another chance to change:

| Baseline age `k` | Props changed `1 − 0.98^k` | Expected delta | Versus `k = 1` |
|---|---|---|---|
| 1 | 2.0% | 222.8 B | — |
| 2 | 4.0% | 227.5 B | +2.1% |
| 5 | 9.6% | 241.1 B | +8.2% |
| 10 | 18.3% | 261.9 B | +17.6% |
| 20 | 33.2% | 297.8 B | +33.7% |
| 28 | 43.2% | 321.7 B | +44.4% |

Check one row by hand. At `k = 5`, `0.98^5 = 0.904`, so 9.6% of 48 props, 4.6 props, appear in the delta at 5 bytes each: `10 + 208 + 23.1 = 241.1`.

The cost of an old baseline grows slowly. Even 28 ticks, 1.4 seconds of lost acks, leaves the delta at about a third of a full snapshot. The moving players dominate, and they cost the same at any age.

### The code

Here is an encoder and decoder for this format. Lab 07 asks you to write these two functions inside `labs/lab07-starter/snapcodec.py`, which supplies the rest. The code uses Python's `struct` module (week 5) and byte-aligned fields to stay readable.

```python
import struct

FIELDS = [("x", "f"), ("y", "f"), ("yaw", "H"), ("hp", "B"), ("anim", "B")]
HEADER = struct.Struct("<IIH")   # tick, baseline tick (0 = full), entity count

def encode_delta(tick, base_tick, base, world):
    body, changed = [], 0
    for eid in sorted(world):
        mask, vals = 0, []
        for i, (name, code) in enumerate(FIELDS):
            if world[eid][name] != base[eid][name]:
                mask |= 1 << i
                vals.append(struct.pack("<" + code, world[eid][name]))
        if mask:
            changed += 1
            body.append(struct.pack("<HB", eid, mask) + b"".join(vals))
    return HEADER.pack(tick, base_tick, changed) + b"".join(body)

def apply_delta(data, base):
    world = {eid: dict(ent) for eid, ent in base.items()}
    _, _, count = HEADER.unpack_from(data, 0)
    pos = HEADER.size
    for _ in range(count):
        eid, mask = struct.unpack_from("<HB", data, pos); pos += 3
        for i, (name, code) in enumerate(FIELDS):
            if mask & (1 << i):
                (world[eid][name],) = struct.unpack_from("<" + code, data, pos)
                pos += struct.calcsize("<" + code)
    return world
```

Notice that the delta carries **absolute values** ("x is now 41.25"), not differences ("x grew by 0.25"). That choice matters in a moment.

### What goes wrong with the wrong baseline

The obvious design is to delta each snapshot against the one sent just before it. It saves a few bytes, since `k` is always 1. The lab's simulator runs both designs for 30 seconds at 20 Hz on the arena, with a 100 ms round trip and seeded random loss (seed 1). "Client wrong" counts the snapshots after which the client's world differs from the server's world at that tick.

| Loss | Baseline = last acked: bytes/snapshot | Client wrong | Baseline = last sent: bytes/snapshot | Client wrong |
|---|---|---|---|---|
| 0% | 258.5 | 0.0% | 252.3 | 0.0% |
| 1% | 258.6 | 0.0% | 252.3 | 19.3% |
| 5% | 258.8 | 0.0% | 252.3 | 80.2% |
| 20% | 259.7 | 0.0% | 252.3 | 99.8% |

Byte counts include the 28-byte header and the two full snapshots the acked design sends before its first ack arrives.

The "last sent" design saves 2.5% of the bytes and is wrong most of the time at a loss rate that week 2 called ordinary. Here is the mechanism. Snapshot 300 is lost, and it carried "crate 41, hp 60". Snapshot 301 is a delta against 300, which the client never saw. The client applies it to what it has, snapshot 299. The players look fine, because every delta carries their full new `x`, `y` and `yaw`. The crate does not, because it has not changed since 300, so no later delta mentions it. The client shows the old crate until the crate happens to change again, which at `p = 0.02` takes 50 ticks on average. Meanwhile other props go stale the same way. The errors pile up on exactly the entities that change rarely, which are the ones nobody is watching in a test.

Absolute values are what make even this partial recovery possible. Had the delta carried differences ("x grew by 0.25"), one lost packet would shift every moving player for the rest of the match.

With the acked baseline, snapshot 301 is encoded against the last snapshot the client confirmed, say 298. It mentions everything that changed since 298, including crate 41. The loss of 300 costs nothing but a few bytes in 301.

### Move it yourself

Open `examples/w07-delta-baseline.html`. The top strip shows snapshots leaving the server at 20 Hz, with lost ones crossed out and an arc from each snapshot to its baseline. Below, two 8 × 8 grids show the server's 64 entities and the client's copy, with wrong cells outlined. Switch the policy to "last sent" and raise loss to 5%. Watch outlined cells appear in the prop rows and stay there while the player rows stay clean. Switch back to "last acked" and watch the arcs stretch across the lost packets while the grids stay identical. The byte bar barely moves.

### Same idea elsewhere

**Quake III Arena (1999, source released 2005).** The server keeps the last 32 snapshots for each client (`PACKET_BACKUP`), and deltas the next one against the snapshot the client last acknowledged. If that ack is 29 or more packets old, the server gives up and sends a full snapshot. Entities that did not change are left out. A changed entity writes a change bit for each field up to the last one that changed, then the new values, and the whole message is Huffman-compressed. Our format is the same design, with a byte mask instead of per-field bits.

**Source engine (Valve, current developer documentation).** Valve describes the same scheme in one paragraph. The server sends only the changes since the last acknowledged update, using ack numbers carried on every packet. Full snapshots go out when a game starts, or when a client has suffered heavy loss for a couple of seconds, which is Quake's 29-packet rule in different units. A player can ask for one with `cl_fullupdate`.

**Starsiege: Tribes (Dynamix, 1998).** Tribes reached the same guarantee without keeping old snapshots. Each object keeps a **state mask** per client, one bit per group of fields (position, rotation, animation, often 20 or more bits). When a group changes, its bit is set. When the server writes an object into a packet, it records which bits went into that packet and clears them. If the packet is later reported lost, those bits are set again, *unless a later packet already carried the same bit for that object*. Rewrite it in our terms and the "baseline" is implicit. Every group is resent until a packet carrying its newest value is known to have arrived. Tribes also sorts objects by priority when a packet fills, which our model does not need yet.

**Fiedler's cube demo (Gaffer on Games, 2015).** 901 physics cubes at 60 snapshots a second start at 17.37 Mbit/s uncompressed. Quantization (week 5's topic), an "at rest" bit and delta encoding against the most recent acknowledged snapshot aim for a target of 256 kbit/s, about 1.5% of the original. Most of the win comes from the same observation as our arena. Most cubes are at rest most of the time, and the acked baseline lets the encoder say "unchanged" in one bit.

Four systems, one rule. A delta is only as good as its baseline, and the only baseline the sender can trust is one the receiver has confirmed.

### Design judgment

- **Delta against the last ack, always.** The saving from a newer, unconfirmed baseline is a few percent. The failure it causes is silent and hits the entities that change least.
- **Send absolute values of changed fields.** Differences are smaller after quantization, and some engines do use them *relative to an acked baseline*, which is safe. Differences relative to the previous packet are not.
- **Cap the baseline age.** The server must keep every snapshot a client might still acknowledge. Quake's 32 per client at 906 bytes would be about 29 KB per client in our arena. Pick a cap, and send a full snapshot when a client's last ack is older than the ring.
- **Always compare with the full size.** A delta can be bigger than the full snapshot (the 970-byte row). The rule "send the smaller" costs one comparison.
- **The client must keep baselines too.** It stores the snapshots it acked until the server stops referring to them. In the lab, a dictionary keyed by tick.
- **Deltas make every snapshot depend on another.** That complicates debugging, replays and spectators joining mid-match. Store full snapshots at intervals when you record a match.

### Check this example

1. In the arena, 8 players move and 4 props change in one tick. What is the delta against the previous tick, and how much smaller is it than the full snapshot?
2. A client's acks stop arriving for 20 ticks while its snapshots still get through. What is the expected delta size at `k = 20`, and what fraction of the full snapshot is it?
3. With baseline = last sent, a pickup respawns in snapshot 500, and 500 is lost. The pickup does not change again until tick 540. For how many seconds does the client show it missing?

<details>
<summary>Answers</summary>

1. `10 + 8 × 13 + 4 × 5 = 134` bytes, against 906. About 6.8 times smaller.
2. `297.8` bytes, `297.8 / 906 = 33%` of a full snapshot.
3. From tick 500 to tick 540 is 40 ticks at 20 Hz, so 2 seconds. Every delta in between is against an unconfirmed baseline and none mentions the pickup.

</details>

## 3. Beyond the baseline: other ways to shrink a snapshot

The delta cuts the props. The players now dominate: 208 of the 223 bytes. Three further tools attack them. Each has its own week, so this section only places them.

**Quantize.** A 32-bit float position is accurate to far less than a millimeter across the arena. Week 5 packs positions into a fixed number of bits, for example 16 bits for a 256-meter arena at about 4 mm resolution. Fiedler's cubes dropped from 96 bits of position to 50 before any delta. In our arena, `x` and `y` at 16 bits each and `yaw` at 9 bits would shrink a moving player from 13 bytes to about 8.

**Send less often, or to fewer clients.** A client does not need entities behind a wall on the far side of the map. Choosing which entities each client receives is **interest management**, and in an MMO it matters more than any encoding trick. [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) builds it with grids and radii. Week 13 of this course puts all of this into a bandwidth budget.

**Prioritize when full.** Tribes fills each packet up to a size cap in priority order, and whatever does not fit waits for the next packet. Its mask bits stay set, so nothing is lost, only delayed. That turns bandwidth into a knob, not a cliff.

The order matters. Deltas and quantization are nearly free and make every snapshot smaller. Interest management changes *which* entities appear, and it is the only tool that breaks week 3's `n²`.

## In-class activity (25 minutes)

Pairs. Each pair gets a card describing a game's entities: "4-player co-op dungeon, 200 monsters, 30 of them awake at a time", "2v2 racing game, 4 cars and 60 physics cones", or "battle royale endgame, 20 players and 400 loot items on the ground".

1. Choose fields and sizes for each entity type. Compute the full snapshot size.
2. Estimate how many entities change per tick and which fields they change. Compute the delta at `k = 1` and at `k = 10`.
3. Compute the bandwidth per client at your snapshot rate, full and delta, with the 28-byte header.
4. Name the entity type that benefits most from deltas and the one that benefits least, and say which tool from section 3 you would try next.

Expected output: a small table like section 2's, and one sentence for step 4.

## Common misconceptions

- **"Deltas are fragile, so they need reliable delivery."** A delta against an acknowledged baseline needs no retransmission. A lost delta is replaced by the next one, which carries everything since the same baseline.
- **"The baseline is the previous snapshot."** It is the newest snapshot the client has confirmed. On any real network that is at least a round trip old.
- **"A delta is always smaller than a full snapshot."** Not when everything changes. Masks and ids add bytes. Compare and send the smaller.
- **"If players look right, the client is in sync."** Frequently changing fields heal themselves. Rarely changing ones are where a bad baseline shows, and they are the last place a tester looks.

## Check yourself

1. A game has 40 entities of 20 bytes each, 2-byte ids and a 10-byte header. What is the full snapshot size? If 10 entities change 8 bytes of fields each per tick, with a 1-byte mask, what is the delta?
2. At 30 snapshots per second and a 200 ms round trip, what is the smallest baseline age the server can use?
3. In the arena, what prop change probability `p` would make the expected delta at `k = 10` equal to 300 bytes?
4. Explain in two sentences why Tribes needs no ring of old snapshots but still recovers from loss.
5. A teammate proposes sending `x` as "change since the last snapshot" to save bits. Under which baseline policy is that safe, and why is it unsafe under the other?

<details>
<summary>Answers</summary>

1. Full: `10 + 40 × 22 = 890` bytes. Delta: `10 + 10 × (2 + 1 + 8) = 120` bytes.
2. The ack for snapshot `t` returns after about 200 ms, 6 snapshot intervals at 30 Hz, so `k ≥ 6`.
3. `10 + 208 + 240 × (1 − (1 − p)^10) = 300` gives `1 − (1 − p)^10 = 0.342`, so `(1 − p)^10 = 0.658` and `p = 1 − 0.658^0.1 ≈ 0.041`.
4. It tracks, per object and per client, which groups of fields still need sending, and it learns from packet notifications which packets were lost. A lost group is marked for resending unless a later packet already carried it, so every group's newest value eventually arrives.
5. Safe only as a change relative to an acknowledged baseline, because the client is known to hold that baseline and the sum is exact. Relative to the last *sent* snapshot, one lost packet removes one change for good and every later position is off by it.

</details>

## Lab / assignment hook

[Lab 07, a snapshot codec](../labs/lab07.md). You implement `encode_delta` and `apply_delta`, reproduce the tables in section 2 with `--check`, run the loss simulation for both baseline policies, then add 16-bit quantization for positions and measure what it saves.

## Sources

- id Software, *Quake III Arena* source code (GPL release, August 2005), `code/qcommon/qcommon.h`, `code/server/sv_snapshot.c`, `code/qcommon/msg.c`. `PACKET_BACKUP` of 32. Delta from the client's acknowledged frame, and full snapshots when the ack is `PACKET_BACKUP − 3` or more packets old. Unchanged entities omitted, per-field change bits up to the last changed field, Huffman coding of messages. Default 20 snapshots per second (`sv_fps` default "20" in `code/server/sv_init.c`, `snaps` default "20" in `code/client/cl_main.c`). Checked against the repository in September 2026. https://github.com/id-Software/Quake-III-Arena
- Sanglard, F. (30 June 2012). "Quake 3 Source Code Review: Network Model." fabiensanglard.net. Snapshot history per client, deltas against the last acknowledged snapshot, a zeroed dummy baseline forcing a full update.
- Valve Developer Community, "Source Multiplayer Networking" (accessed September 2026). Delta snapshots since the last acknowledged update, acks on every packet, full snapshots at game start or after a couple of seconds of heavy loss, `cl_fullupdate`.
- Frohnmayer, M. & Gift, T. (undated). "The TRIBES Engine Networking Model." Dynamix. No date or venue appears on the paper; its abstract says the model is being developed for Tribes II. Describes *Starsiege: Tribes* (December 1998) and Tribes 2. State masks per object, "upwards of 20" state flags, lost bits resent only if no later packet carried them, priority ordering.
- Fiedler, G. (4 January 2015). "Snapshot Compression." Gaffer on Games. 901 cubes at 60 Hz, 17.37 Mbit/s uncompressed and a 256 kbit/s target, deltas against the most recent acknowledged snapshot.
- Gambetta, G. *Fast-Paced Multiplayer*, part I (gabrielgambetta.com). Authoritative server, clients as spectators of server state.

## Interactive spec: examples/w07-delta-baseline.html

**Insight the visual must make obvious:** a delta against the last *acknowledged* snapshot survives packet loss for a few extra bytes, while a delta against the last *sent* snapshot is slightly smaller and leaves the client silently wrong, mostly on entities that rarely change.

**Layout.** Three stacked panels plus a readout column. On desktop (≥ 900 px) the readouts sit to the right; below that they go under the panels. No horizontal page scroll at 390 px.

1. **Timeline strip.** The last 40 ticks scroll right to left. Top row: server snapshots as small squares labelled with the tick (every 5th label). Lost snapshots are drawn crossed out. From each snapshot, a thin arc goes back to its baseline tick (none for full snapshots, which are drawn filled). Bottom row: ack arrivals at the server, drawn as ticks `rtt_ticks` later.
2. **Two grids.** "Server" and "Client", each 8 × 8 cells, one per entity. Rows 1-2 (ids 1-16) are players, rows 3-8 are props. A cell flashes for 150 ms when its entity changes. On the client grid, any cell whose five fields differ from the server's values at the tick of the last snapshot the client decoded gets a thick outline in the warning color and a small "stale" dot. Under reduced motion, no flash, only the outline.
3. **Byte bars.** One bar per tick for the last 40 ticks, height = payload bytes, with a dashed line at the full-snapshot size (906 with default settings) and a label on the line.

**Controls.**
- Policy radio: "Baseline = last acked" (default), "Baseline = last sent", "Always full".
- Loss slider 0-30%, default 5%, step 1%.
- Round trip in ticks, 1-10, default 2 (label shows ms at 20 Hz).
- Moving players `P`, 0-64, default 16. Props are `64 − P`.
- Prop change probability `p`, 0-0.20, default 0.02, step 0.01.
- Play/pause (default playing at 20 ticks per second, 5 under reduced motion), Step, Reset, Seed field (default 2, because seed 1 shows only one stale prop in the first 60 ticks; seed 1 is the lab's default and is used for the lecture's table).
All controls are native inputs with labels and work from the keyboard.

**Readouts.** Mean payload bytes per snapshot, kbit/s at 20 Hz including 28 bytes of header, current baseline age `k`, full snapshots sent, stale entities now, and "client wrong after X% of snapshots". Also the expected delta from the formula for the current `k`, next to the measured mean.

**Model (must match `labs/lab07-starter/snapcodec.py`).** Entity 12 bytes, id 2, mask 1, header 10. Full = `10 + 64 × 14`. Delta = `10 + Σ(3 + changed field bytes)`, and the encoder sends the full snapshot instead when that is smaller or when `tick − acked ≥ 29`. Each tick every player changes `x`, `y`, `yaw` (13 bytes in a delta); each prop changes `hp` and `anim` with probability `p` (5 bytes). Loss applies to snapshots only; acks are never lost and arrive `rtt_ticks` later. Under "last sent", the client applies each delta to its current world even if it never received the baseline. Expected delta `10 + 13P + 5(64 − P)(1 − (1 − p)^k)`. Use a seeded PRNG (mulberry32); the lecture's simulation table comes from Python's generator, so measured means may differ from it by a few bytes, but the pattern (0% wrong for acked, most snapshots wrong for sent at 5% loss) must hold.

**Test values** (assert on load with `P = 16`, `p = 0.02`): full 906 B; delta with 16 players and 1 prop changed 223 B; no change 10 B; all 64 entities changing all fields 970 B, so the encoder picks full (906). Expected delta at `k = 1, 2, 5, 10, 20, 28`: 222.8, 227.5, 241.1, 261.9, 297.8, 321.7.

**First screen:** policy "last sent", loss 5%, already 60 ticks into the run so several stale outlines are visible, with a caption: "Last sent: 2.5% fewer bytes. Client wrong after most snapshots. Switch to last acked."
