# CS202 · Week 05 — Serialization and bit packing

**Why this matters:** Week 3 showed that a server's upload grows with the square of the player count, multiplied by the bytes in each player's state. You cannot change the square. You can change the bytes. Most game state is sent at far more precision than anyone can see, and cutting it to what the game needs often shrinks a packet to a third of its size with no visible change.

**You will be able to:**
- Compute the bits a value needs from its range and precision, and the largest error that choice allows.
- Write a bit writer and a bit reader, and pack a player state into a byte count you can predict before running the code.
- Compute what a smaller state saves in server upload with week 3's bandwidth model.
- Parse untrusted bytes without crashing, and explain why general-purpose formats (JSON, pickle) do not belong on a game's hot path.

**Before class:** Glenn Fiedler, "Reading and Writing Packets" (Gaffer on Games, 1 September 2016) and "Snapshot Compression" (4 January 2015), the sections on quantized position and "smallest three" orientation. Reread MA101 week 5 on logarithms.

**Prerequisites from earlier courses:** [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (`log2` answers "how many bits"). [MA101 week 7, piecewise caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md) (clamping and rounding are what quantization does). [CS102 week 14, unit testing](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md) (round-trip tests catch every serialization bug). [CS202 week 3](w03-topologies-peer-to-peer-client-server-relay.md) (the server upload formula) and [week 4](w04-server-authority-never-trust-the-client.md) (every packet from a client is hostile until checked).

**Interactive:** [examples/w05-quantization-bits.html](../examples/w05-quantization-bits.html). Keep it open during section 2.

---

## 1. From objects to bytes

In your game a player is an object with fields. On the wire it must be a row of bytes. **Serialization** turns the object into bytes. **Deserialization** turns bytes back into an object. Both ends must agree on the layout exactly, down to the bit, or the receiver reads garbage.

### The first attempt

The obvious layout writes each field in its natural machine type. Here is a player state for a small arena shooter.

```python
import struct

NAIVE = struct.Struct("<3f2f3fii4?")   # position, yaw+pitch, velocity, health, state, 4 flags
NAIVE.size                              # 44 bytes
```

Three 4-byte floats for position, two for aim angles, three for velocity, two 4-byte integers for health and an animation state, and four one-byte booleans. That is 44 bytes, and it works. It is also what week 3's `s = 40` bytes was standing for.

A text format is worse. The same player written as compact JSON, with the lab's sample values, is 179 bytes, because every field name and every digit is spelled out in characters. JSON is fine for a login request sent once. It is four times too big for a state sent twenty times a second to sixty players.

**Never use a language's native object serializer on network data.** Python's `pickle`, and its equivalents in other languages, can rebuild any object, which means a crafted packet can make your server run code of the attacker's choosing. Week 4's rule applies to the parser too. Anything that reads client bytes must only ever produce the values you expect.

### Byte order

A 4-byte integer can be stored most significant byte first (**big-endian**) or least significant byte first (**little-endian**). Most CPUs today are little-endian. Internet protocol headers use big-endian, which is why it is called **network byte order**, and why week 1's `struct` formats start with `!`. Your own game protocol can use either, as long as both ends agree. Pick one, write it in the protocol document, and put it in every `struct` format string. The bug you are preventing is a server built for one platform and a client for another, each reading the other's numbers backwards.

### Where the waste is

Look at the 44 bytes again and ask what each field really needs.

- **Health** is a whole number from 0 to 100. That is 101 values. A 32-bit integer can hold four billion.
- **The animation state** has five values (idle, run, jump, crouch, dead). It is sent in 32 bits.
- **Each boolean** takes a whole byte, 8 bits, for 1 bit of information.
- **Position** is a float, with about seven significant digits everywhere in the arena. Near the far wall at 511 m, a float can tell apart positions 0.03 mm apart. Nobody can see 0.03 mm.

Every one of those is precision the game pays for twenty times a second and never uses.

## 2. Worked example: a player state in 14 bytes

### The hook

In January 2015 Glenn Fiedler published a networked physics demo, a pile of 901 cubes sent from one machine to another 60 times a second. Sent the obvious way, each cube's state took 40.125 bytes and the stream needed 17.37 megabits per second, far past a home connection. Two of his first steps involved no clever compression at all. He cut the orientation, four 32-bit floats of a quaternion (128 bits), down to 29 bits. And he sent position as whole numbers of 1/512 m, about 2 mm, which fits the horizontal axes of a 512 m wide world in 18 bits each.

Where do numbers like 18 and 29 come from? Why not 16 or 20? There is a one-line formula behind every one of them.

### The model

A value lies between `lo` and `hi`. You decide the **precision** `p`, the size of one step. Replace the value with the whole number of steps from `lo`. That is **quantization**.

```
q     = round((x − lo) / p)                 the integer you send
x'    = lo + q × p                           what the receiver rebuilds
count = (hi − lo) / p + 1                    distinct values, closed range [lo, hi]
count = (hi − lo) / p                        if the value wraps (an angle: 360° is 0°)
bits  = ⌈log2(count)⌉
max error = p / 2
```

- `x` is the true value and `x'` the value after the round trip.
- `count` is how many different integers `q` can be.
- `⌈ ⌉` rounds up, because you cannot send part of a bit.

Read the last two lines together. Each extra bit doubles `count`, so it halves `p` and halves the error. **Halving the error costs exactly one bit.** Going from centimetres to millimetres costs about 3.3 bits (`log2 10`), not ten times the space.

Turned around, `b` bits over a range give a precision of `p = (hi − lo) / (2^b − 1)`. Pick whichever question you are asking.

### Numbers you can check: one axis

A 512 m arena, `lo = 0`, `hi = 512`.

| Precision `p` | Values `count` | Bits | Largest error |
|---|---|---|---|
| 10 cm | 5,121 | 13 | 50 mm |
| 5 cm | 10,241 | 14 | 25 mm |
| 1 cm | 51,201 | 16 | 5 mm |
| 5 mm | 102,401 | 17 | 2.5 mm |
| 1 mm | 512,001 | 19 | 0.5 mm |
| 0.1 mm | 5,120,001 | 23 | 0.05 mm |
| float32 | — | 32 | about 0.03 mm near 512 m |

Check the 1 cm row by hand. `512 / 0.01 + 1 = 51,201`. `2^15 = 32,768` is too few and `2^16 = 65,536` is enough, so 16 bits. Every row down the table buys a smaller error with a bit or three. Even the 0.1 mm row saves 9 bits over a float.

### Numbers you can check: the whole player

Choose each field's precision from what the game needs, not from what the type holds.

| Field | Range | Precision | Values | Bits | Largest error |
|---|---|---|---|---|---|
| x, y | 0 to 512 m | 1 cm | 51,201 | 16 each | 5 mm |
| z | 0 to 64 m | 1 cm | 6,401 | 13 | 5 mm |
| yaw (wraps) | 0 to 360° | 360/1024° | 1,024 | 10 | 0.18° |
| pitch | -90 to 90° | 180/511° | 512 | 9 | 0.18° |
| vx, vy, vz | -20 to 20 m/s | 5 cm/s | 801 | 10 each | 2.5 cm/s |
| health | 0 to 100 | 1 | 101 | 7 | none |
| state | 5 values | 1 | 5 | 3 | none |
| 4 flags | true or false | — | 2 each | 1 each | none |
| **Total** | | | | **108 bits = 14 bytes** | |

Add it up. `16 + 16 + 13 + 10 + 9 + 30 + 7 + 3 + 4 = 108` bits, which rounds up to 14 bytes. The naive struct was 44. That is 3.1 times smaller.

Two rows hide a trap that catches almost everyone once.

- **Yaw wraps.** If you treat 0 to 360 as a closed range, `count = 1,025` and you need 11 bits. But 360° is the same direction as 0°, so only 1,024 values are distinct, and 10 bits do. One wasted bit per player per packet.
- **Fiedler's z.** His vertical range is 0 to 32 m at 1/512 m. As a closed range that is 16,385 values and 15 bits. He used 14 bits, which holds exactly the 16,384 values of the half-open range `[0, 32)`. Neither choice is wrong. Know which one you made, because the top value either fits or silently clamps.

### What 30 bytes buy

Put both sizes into week 3's dedicated server formula, `server upload = n × r × (n × s + h)`, at 20 Hz with a 28-byte header.

| Players `n` | Upload at `s = 44` | Upload at `s = 14` | Saved |
|---|---|---|---|
| 8 | 486 kbit/s | 179 kbit/s | 63% |
| 64 | 29,123 kbit/s | 9,462 kbit/s | 68% |
| 100 | 70,848 kbit/s | 22,848 kbit/s | 68% |

Check the 64-player cell. `64 × 20 × (64 × 14 + 28) = 64 × 20 × 924 = 1,182,720` bytes per second, times 8 and divided by 1,000, is 9,462 kbit/s. The saving approaches `1 − 14/44 = 68%` as `n` grows, because the header becomes a smaller share of each snapshot. At 100 players the packed state saves 48 Mbit/s of server upload, every second the match runs. Week 13 turns that into money.

### The bit writer

You cannot write 13 bits with `struct`, which works in whole bytes. You need a **bit writer**, which appends values of any width to a buffer, and a **bit reader** that takes them back out in the same order. This version writes the least significant bit first.

```python
class BitWriter:
    def __init__(self):
        self.buf, self.nbits = bytearray(), 0

    def write(self, value, nbits):
        if not 0 <= value < (1 << nbits):
            raise ValueError(f"{value} does not fit in {nbits} bits")
        for i in range(nbits):
            byte, bit = divmod(self.nbits, 8)
            if byte == len(self.buf):
                self.buf.append(0)
            if (value >> i) & 1:
                self.buf[byte] |= 1 << bit
            self.nbits += 1
```

Trace it once by hand. Write 5 in 3 bits, then 1 in 1 bit, then 300 in 9 bits. The bits go into the first byte from bit 0 upward, `1 0 1` (the 5), `1` (the 1), then the low four bits of 300, `0 0 1 1`. Reading the byte from bit 7 down, that is `1100 1101`, which is `0xCD`. The last five bits of 300, `0 1 0 0 1`, fill the second byte from the bottom, giving `0x12`. Thirteen bits in two bytes. Lab 05's check uses exactly these values.

A bit-by-bit loop is slow in Python and fine for learning. Fiedler's production version keeps a 64-bit scratch word and flushes 32 bits at a time, which is the same idea at machine speed.

### Move it yourself

Open `examples/w05-quantization-bits.html`. The left view is a zoomed patch of the arena. A dot moves along a smooth curve, and a second dot shows where the receiver thinks it is after quantization. The grid of legal positions is drawn behind them. The right view is a staircase of bits against precision, with the current setting marked, and a readout of the player's total bytes and the server's upload at your chosen `n`. Drag precision from 1 cm to 50 cm and watch the received dot start to hop from grid point to grid point, while the bit count falls by only five, from 16 to 11. Then switch the field to yaw and find the setting where a target 30 m away starts to jump by more than its own width.

### Same idea elsewhere

**Source engine (Source SDK 2013).** Every networked field of an entity is declared with a bit count. In the player's send table, `deadflag` is 1 bit, `m_lifeState` 3 bits, the field of view `m_iFOV` 8 bits, and `m_flMaxspeed` is a float sent in 12 bits over the range 0 to 2,048. Health uses a variable-length integer instead (section 4). Its general coordinate encoding uses 14 integer bits plus 5 fractional bits, a precision of 1/32 unit. Those are our formula's decisions, written as code.

**Unreal Engine (Unreal Engine 5.8 API documentation).** Unreal offers vector types chosen by precision. `FVector_NetQuantize` keeps whole units and uses up to 20 bits per component. `FVector_NetQuantize10` keeps one decimal place in up to 24 bits. `FVector_NetQuantize100` keeps two decimal places in up to 30 bits. Each step of ten times more precision costs 4 to 6 more bits, which is `log2 10 ≈ 3.3` bits of precision plus the extra range each type also covers.

**Fiedler's cube demo (2015).** Position at 1/512 m in 18, 18 and 14 bits. For orientation, a unit quaternion's four components satisfy `a² + b² + c² + d² = 1`, so the largest can be rebuilt from the other three. He sends 2 bits saying which one was dropped and the three smallest in 9 bits each, `2 + 9 + 9 + 9 = 29` bits instead of 128. That is the same principle pushed one step further. Do not send what the receiver can work out.

**League of Legends (Riot, 2015).** Week 1 quoted Riot's figure of about 55 bytes for a typical game packet. Every one of those bytes has been through decisions like the ones in this section.

Four codebases, one formula. When you meet a networked field, ask what its range is, what precision the game needs, and whether it wraps.

### Design judgment

- **Choose precision from what the game needs.** Two very different consumers read positions. The renderer only needs error below a pixel at typical view distances. Hit detection needs error well below a hitbox. Work out both and use the stricter.
- **Aim is the dangerous field.** An 8-bit yaw (1.41° steps, as a byte per axis gives) has a largest error of 0.70°. At 30 m that is 0.37 m sideways, wider than a head. A 10-bit yaw gives 0.09 m, and 16 bits gives 1.4 mm. Send other players' aim for display at low precision if you like. Never do hit detection with it.
- **Quantize the server's own state too.** If the server simulates with full floats and sends quantized values, the client's picture differs slightly from the server's truth. When the client predicts (week 8), those tiny differences grow into corrections. One fix is to round the authoritative state to the network precision every tick, so both ends start from the same numbers.
- **Clamping is a decision.** A value outside the range gets clamped to its edge. Make sure the range covers every legal value, and treat an out-of-range value from a client as a bug report or a cheat (week 4), not something to clamp quietly.
- **Plan for the next version.** Protocols change after launch. Put a protocol version number in the connection handshake, and refuse a client whose version does not match, rather than letting two layouts misread each other.

### Check this example

1. A racing game's track is 4 km long. You want 2 cm precision along it. How many bits? What is the largest error?
2. Your team sends health (0 to 1,000) in 16 bits. How many bits are wasted per player per packet, and what does that cost per second on a 64-player server at 30 Hz?
3. You have 12 bits for yaw. What is the step size, and how far sideways is the largest error at 50 m?

<details>
<summary>Answers</summary>

1. `4,000 / 0.02 + 1 = 200,001` values. `2^17 = 131,072` is too few, `2^18 = 262,144` is enough, so 18 bits. Largest error 1 cm.
2. 1,001 values need 10 bits, so 6 bits are wasted. Each snapshot holds 64 players and goes to 64 clients 30 times a second: `6 × 64 × 64 × 30 = 737,280` bits per second, about 737 kbit/s of pure waste.
3. Yaw wraps, so 4,096 values, a step of `360 / 4,096 = 0.088°`. The largest error is half a step, 0.044°, which at 50 m is `50 × 0.044 × π / 180 = 0.038 m`, about 4 cm.

</details>

## 3. Reading bytes you did not write

The reader is the half an attacker attacks. Week 4 said every client packet is a claim. Here is what that means for a parser.

- **Check before you read.** Before reading `n` bits, check that `n` bits remain. A short packet must produce a clean error, not an index error that kills the server thread or, in C++, a read past the end of the buffer.
- **Check every value against its range.** A 3-bit state field can hold 0 to 7. If only 0 to 4 are defined, 5, 6 and 7 are malformed and must be rejected.
- **Check lengths against what is left.** If a packet says "a string of 200 bytes follows" and only 30 remain, reject it before allocating anything.
- **Reject, don't guess.** When a packet fails any check, drop it and count it. Do not try to make sense of the rest.

The standard way to test all of this is **fuzzing**. Feed the reader thousands of random byte strings and assert that each one either decodes or raises your own error type, and never anything else. Lab 05 runs 10,000 of them. Your reader will almost certainly fail the first run. That failure is a bug an attacker would otherwise have found for you.

```python
class ReadError(Exception):
    pass

def read(self, nbits):
    if self.pos + nbits > len(self.data) * 8:
        raise ReadError("read past end of packet")
    ...
```

## 4. Beyond fixed widths

Fixed-width quantized fields cover most of a game's state. Three further tools are worth knowing by name. The rest of the course uses them.

- **Variable-length integers (varints).** Some values are usually small and occasionally large, like an ammo count or a player ID. A varint uses 7 bits of each byte for the number and the top bit to say "another byte follows." Values below 128 take 1 byte, below 16,384 take 2, below about 2 million take 3. Source sends health and ammo this way.
- **Delta encoding.** Most of a player's state is the same as last packet. Send only what changed, relative to a state the receiver has confirmed. This is week 7, and it usually saves more than quantization does. The two multiply.
- **Entropy coding.** Values that are common can get shorter codes than rare ones (Huffman coding, arithmetic coding). It helps most after delta encoding, when most values are zero.

The order in practice is quantize first, then delta, then entropy-code if the budget still does not fit. Each step's saving multiplies the last.

## In-class activity (25 minutes)

Pairs. You get a card describing an entity from a game genre. Examples: "MMO player character, open world 16 km across, 40 fields"; "RTS unit, map 256 × 256 tiles, 12 fields"; "racing car, 6 km track, 10 fields".

1. For each field, choose a range and a precision, and say who reads it (renderer, hit detection, UI). Mark any field that wraps.
2. Compute bits per field and the total in bytes. Compare with the naive layout of floats and 32-bit integers.
3. Using week 3's formula, compute the server's upload at your genre's typical player count and send rate, for both layouts.
4. Swap cards with another pair and find the one field whose precision you think is wrong. Settle it with the largest-error number.

Expected output: a field table like the one in section 2, two upload figures, and one disputed field with the numbers that settled it.

## Common misconceptions

- **"Floats are the natural way to send positions."** A float spends its bits on precision near zero and range up to 10^38. Your arena has neither. A fixed-point integer with a known range and step is smaller and has the same error everywhere.
- **"More precision always looks better."** Past the point where the error is smaller than a pixel or a hitbox, extra bits change nothing a player can see.
- **"Bit packing is a micro-optimization."** At 100 players it moved the server's upload by 48 Mbit/s in section 2. That is the largest single saving in this course before delta compression.
- **"If it round-trips on my machine, the format is correct."** Your test only sends well-formed data. The real test is a fuzzer sending malformed data, and a client on another platform reading your byte order.

## Check yourself

1. How many bits do you need for an enum with 12 values? For one with 16? For one with 17?
2. A field uses 11 bits over the range -50 to 50. What is its precision and largest error?
3. Pack a 3D position in a 2 km × 2 km × 200 m world at 1 cm precision. How many bits? How many bytes, if nothing else is in the packet?
4. Explain why a yaw sent as `round(yaw / 360 × 1024)` must be taken modulo 1,024 before writing it into 10 bits.
5. A packet claims to contain 40 players, and each player takes 14 bytes. The packet has 300 bytes after its header. What should the reader do, and why?

<details>
<summary>Answers</summary>

1. 12 values: `⌈log2 12⌉ = 4` bits. 16: exactly 4 bits. 17: 5 bits.
2. `2^11 − 1 = 2,047` steps over 100, so `p = 100 / 2,047 = 0.0489`, and the largest error is 0.0244.
3. x and y: `200,000 + 1` values, 18 bits each. z: `20,000 + 1` values, 15 bits. Total 51 bits, 7 bytes.
4. A yaw of 359.9° gives `round(1,023.7) = 1,024`, which does not fit in 10 bits. But 1,024 steps is 360°, the same as 0. Taking it modulo 1,024 gives 0, the correct direction.
5. 40 × 14 = 560 bytes are needed and only 300 remain, so the packet is malformed. Reject it before reading any players and count the error. Reading 21 players and then failing wastes work, and allocating space for 40 from an attacker's count is how a denial-of-service bug starts.

</details>

## Lab / assignment hook

[Lab 05, 108 bits](../labs/lab05.md). You write `bits_for_count`, quantization, a bit writer and a bit reader, pack the section 2 player state into 14 bytes, fuzz your reader with 10,000 random packets, and design a packed state for an entity of your own game with an upload comparison. Deliverable: your code, the outputs and a one-page field table with justifications.

## Sources

- Fiedler, G. (2015). "Snapshot Compression." *Gaffer on Games*, 4 January 2015. 901 cubes at 60 Hz, 40.125 bytes per cube and 17.37 Mbit/s uncompressed. Position bounds of -256 to 255 m horizontally and 0 to 32 m vertically at 512 values per metre, in 18, 18 and 14 bits. Smallest-three quaternion in 2 + 9 + 9 + 9 = 29 bits, down from 128.
- Fiedler, G. (2016). "Reading and Writing Packets." *Gaffer on Games*, 1 September 2016. Bits required for a range, the bitpacker with a 64-bit scratch word flushed 32 bits at a time, and byte order.
- Valve, Source SDK 2013, `src/game/server/player.cpp` (send table `DT_BasePlayer`, GitHub ValveSoftware/source-sdk-2013, master, accessed September 2026). Bit counts for `deadflag` (1), `m_lifeState` (3), `m_iFOV` (8), `m_flMaxspeed` (12 bits, 0 to 2,048), and `SPROP_VARINT` for health and ammo. `src/public/coordsize.h`. `COORD_INTEGER_BITS` 14, `COORD_FRACTIONAL_BITS` 5.
- Epic Games, Unreal Engine API documentation, `FVector_NetQuantize`, `FVector_NetQuantize10` and `FVector_NetQuantize100` (dev.epicgames.com, accessed September 2026). Precision of 0, 1 and 2 decimal places in up to 20, 24 and 30 bits per component.
- Riot Games Technology blog, "Fixing the Internet for Real Time Applications: Part I" (6 November 2015). *League of Legends* packets of about 55 bytes.
- Python documentation, `struct` module (Python 3.13). Byte-order characters `<`, `>` and `!` (network, big-endian).

## Interactive spec: examples/w05-quantization-bits.html

**Insight the visual must make obvious:** each halving of the error costs exactly one bit, so bits grow slowly while error shrinks fast. Picking precision from what the game needs, instead of sending floats, cuts a player state to a third with no visible change, and too little precision shows up as visible hopping.

**Layout.** Two linked views and a number panel. Left: a zoomed patch of the world with the true and received positions. Right: bits against precision. Under 700 px wide, stack left, right, numbers. No page-level horizontal scroll.

1. **Left view, "What the receiver sees".** A 2 m × 2 m window of the arena. A dot moves along a smooth curve (a circle of radius 0.7 m, one lap every 6 s; static at its start position under `prefers-reduced-motion`, with a "step" button to advance 0.1 s). The quantization grid (spacing `p`) is drawn behind it when `p ≥ 1 cm`, and hidden below that because it would be solid. A second dot shows `lo + round((x − lo)/p) × p` on each axis. A short trail shows the last 1 s of the received dot so hopping is visible. Show the current error in mm.
2. **Right view, "Bits per axis".** x axis precision on a log scale from 0.01 mm to 1 m, y axis bits from 0 to 32. A staircase of `⌈log2((hi − lo)/p + 1)⌉` for the chosen range. A horizontal line at 32 labelled "float32". A marker at the current precision with its bits. Second y axis or tooltip: largest error `p/2`.
3. **Number panel.** For the chosen field: range, precision, count, bits, largest error. For the whole player (section 2 table with the current field's setting swapped in): total bits, bytes, the naive 44 bytes, the ratio. Server upload at `n` players and 20 Hz with 28-byte header, for naive and packed, in kbit/s.

**Controls.**
- Field selector: "Position (x)" default, "Yaw", "Velocity". Changing the field sets the range (0 to 512 m, 0 to 360° wrapping, -20 to 20 m/s) and switches the left view: position uses the moving dot; yaw shows a top-down view of a shooter and a target 30 m away with the aim line quantized (error shown in cm at the target); velocity shows a speedometer needle with true and received values.
- Precision slider, log scale, snapping to the rows of the section 2 one-axis table (1 m, 50 cm, 10 cm, 5 cm, 1 cm, 5 mm, 1 mm, 0.1 mm) plus free values. For yaw, a bits slider 6 to 16 instead.
- Range `hi` field for position (64 to 8,192 m, default 512).
- "Treat as wrapping" checkbox (on for yaw, off for others), which shows the one-bit difference.
- Players `n` slider, 2 to 128, default 64.
- All controls reachable by Tab, with visible focus.

**Formulas (match `labs/lab05-starter/bitpack.py`).** `count = round((hi − lo)/p) + 1`, or `round((hi − lo)/p)` if wrapping. `bits = ⌈log2 count⌉` (0 if `count ≤ 1`). `q = round((clamp(x) − lo)/p)`, for wrapping `round(((x − lo) mod (hi − lo))/p) mod count`. Largest error `p/2`. Player total = sum of section 2 field bits + 4 flag bits, bytes `⌈bits/8⌉`. Server upload `n × 20 × (n × s + 28)` bytes/s, kbit/s = × 8 / 1000.

**Test values** (assert on load):
- Position 0 to 512: `p` = 10 cm gives 13 bits, 5 cm 14, 1 cm 16, 5 mm 17, 1 mm 19, 0.1 mm 23.
- Yaw at 10 bits wrapping: step 0.3516°, 1,024 values. Not wrapping: 11 bits. Aim error at 30 m for 8 bits: 0.368 m. For 10 bits: 0.092 m.
- Whole player: 108 bits, 14 bytes, ratio 3.1 against 44.
- `n = 64`: naive 29,122.6 kbit/s, packed 9,461.8 kbit/s.
- `bits(0 to 32 m at 1/512 m)`: 15 closed, 14 wrapping/half-open.

**First screen:** position field at 1 cm, received dot on top of the true dot, 16 bits marked on the staircase, and the panel showing "44 bytes → 14 bytes, server at 64 players: 29.1 → 9.5 Mbit/s". Caption: "At 1 cm you cannot see the difference. At 10 cm it hops. It is only 3 bits between them."
