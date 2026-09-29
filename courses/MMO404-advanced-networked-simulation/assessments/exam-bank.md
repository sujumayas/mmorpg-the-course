# MMO404 · Exam bank: quiz, practice and viva questions

MMO404 has no written exam. The grade comes from the labs (40%, see [labs-brief.md](labs-brief.md)) and the final seamless two-server handoff demo (60%, see [final-demo-brief.md](final-demo-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute or code question and one explain, design or critique question.
- **Viva.** The lab spot checks and the week 15 demo viva ask questions in this style, rewritten with the numbers from your own runs and your own code.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model to values you have not seen before.
- **code**: say what a piece of Python prints, and why.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or setting for a stated situation and justify it.
- **critique**: find what is wrong with a claim or a design and say how to fix it.

All numbers are invented unless a question names a game. Game facts come from the lecture of the tagged week, which cites its source and era. Each question uses its own week's constants. Weeks 6 and 7 both use MMO302 week 12's battle node, `W(n) = 0.0003n + 0.000001n²` CPU-seconds per game-second with `C = 1` and a 10% floor. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), and every number below was recomputed in Python from the lectures' own models. Write your own answer before you open the solution.

---

## Week 1: Limits of the zone model

Lecture: [w01-limits-of-the-zone-model.md](../lectures/w01-limits-of-the-zone-model.md). Constants: `c_p = 20 µs`, `c_i = 2 µs`, budget 50 ms, `C(n, h) = c_p n + c_i n² (h² + (1 − h²) f)`.

1. *Week 1 · compute.* A zone is a 3 km square with an AOI radius of 120 m. At evening peak 800 players are online and a fifth of them stand at the auction house (`h = 0.2`). Compute `f`, the pair fraction, the tick time, and the zone's capacity at this density and when everyone spreads out.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `f = 0.00503`, pair fraction 0.0448, tick 73.4 ms (over budget), capacity 644 at `h = 0.2` and 1,447 spread out.

`f = π × 120² / 3000² = 45,239 / 9,000,000 = 0.00503`. The pair fraction is `h² + (1 − h²) f = 0.04 + 0.96 × 0.00503 = 0.0448`.

Per-player work is `20 µs × 800 = 16 ms`. Pair work is `2 µs × 640,000 × 0.0448 = 57.4 ms`. The tick is 73.4 ms, 47% over the 50 ms budget.

Capacity solves `a n² + b n − B = 0` with `a = 2×10⁻⁶ × 0.0448 = 8.97×10⁻⁸`, `b = 2×10⁻⁵`, `B = 0.05`: `n = (−b + √(b² + 4aB)) / (2a) ≈ 644`. With `h = 0`, `a = 1.005×10⁻⁸` and `n ≈ 1,447`. The same zone holds 1,447 or 644 players depending on one auction house.
</details>

2. *Week 1 · compute.* Show that making the CPU 4 times faster and running time dilation at 25% speed give the same zone capacity. Compute that capacity for one crowd (`h = 1`) on the lecture's 2 km zone, and the gain over the normal 153 players. Then give the gain for spread-out players (`h = 0`, normal capacity 1,258).

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both give 311 players at `h = 1`, a gain of 2.03 times. Spread out, the gain is 2.38 times (2,988 players).

Capacity solves `c_i g n² + c_p n = B`. Dividing both costs by 4 gives `(c_i g / 4) n² + (c_p / 4) n = B`, which is the same equation as `c_i g n² + c_p n = 4B`. At 25% speed a 100 ms game tick gets 400 ms of real time, so `B` goes from 50 to 200 ms. Same equation, same answer.

At `h = 1`: `2×10⁻⁶ n² + 2×10⁻⁵ n = 0.2`, so `n² + 10n − 100,000 = 0` and `n = (−10 + √400,100) / 2 ≈ 311`. That is `311 / 153 = 2.03` times, close to `√4 = 2` because the pair term dominates. Spread out, per-player work still matters, so the gain (2.38) sits between `√4` and 4.
</details>

3. *Week 1 · code.* What does this print, and what share of the single-layer work does the four-layer world do in total?

```python
import math

C_P, C_I = 20e-6, 2e-6
f = math.pi * 100**2 / 2000**2

def tick_ms(n, h):
    return 1000 * (C_P * n + C_I * n * n * (h * h + (1 - h * h) * f))

for k in (1, 2, 4):
    per_layer = tick_ms(1200 / k, 0.3)
    print(f"k={k}  one layer {per_layer:6.1f} ms  all layers {k * per_layer:6.1f} ms")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**
```
k=1  one layer  303.8 ms  all layers  303.8 ms
k=2  one layer   81.9 ms  all layers  163.9 ms
k=4  one layer   23.5 ms  all layers   93.9 ms
```
Four layers do 31% of the single-layer work (`93.9 / 303.8`).

Each layer holds `1200 / k` players at the same `h`. The per-player part of the total stays 24 ms whatever `k` is. The pair part is `c_i (n/k)² g` per layer, so the total pair work across `k` layers is divided by `k`. Pair work at `k = 1` is 279.8 ms, and at `k = 4` it is 69.9 ms. That is why layering removes load rather than moving it. Two layers already bring each copy under 100 ms, and it takes four to fit the 50 ms budget.
</details>

4. *Week 1 · critique.* A cluster runs 10 zones of the lecture's 2 km size. At peak, the capital holds 1,200 players with `h = 0.3`, and each of the other nine holds 250 spread-out players. The operations dashboard shows 72% average utilization, and a producer concludes there is room for 30% more players. Compute the numbers behind the dashboard and say what is wrong with the conclusion.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The capital's tick is 303.8 ms (608% of its budget), each quiet zone's tick is 6.0 ms (12%), and the average is `(303.8 + 9 × 6.0) / (10 × 50) = 72%`.

Quiet zone: `20 µs × 250 + 2 µs × 62,500 × 0.00785 = 5.0 + 0.98 = 6.0` ms. The capital (from question 3) is 303.8 ms.

The producer is reading the average. Players feel the busiest server, and the capital's players are already lagging at six times the budget. Adding 30% more players at the capital's density raises its pair work by about `1.3² = 1.69` times. The nine quiet servers cannot help because the zone model ties work to a place. The right statement is "the cluster has idle hardware it cannot use". The fixes are week 3's movable borders, week 1's layers for the capital, or a lower `h` by design, such as a second auction house.
</details>

## Week 2: Seamless worlds and boundary handoff

Lecture: [w02-seamless-worlds-and-boundary-handoff.md](../lectures/w02-seamless-worlds-and-boundary-handoff.md). `G(w) = 2ρL(R + w)`, `S(w) = H(w) E_h + G(w) T c_g`, with `c_g = 3 µs` unless stated.

5. *Week 2 · compute.* Use the lecture's measured handoff rates (`H` = 9.25, 2.69, 1.62, 1.23, 1.11 and 0.94 per second at `w` = 0, 5, 10, 15, 20 and 40 m) and its seam (`ρ = 0.002`, `L = 500 m`, `R = 100 m`, 10 Hz). A new character format makes each handoff cost `E_h = 2 ms` instead of 1 ms. Compute `S(w)` for every row and find the best band width. Then repeat with `E_h = 0.25 ms`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** With `E_h = 2 ms`, `S` = 24.50, 11.68, 9.84, 9.36, 9.42 and 10.28 ms/s, best at 15 m. With `E_h = 0.25 ms`, `S` = 8.31, 6.97, 7.01, 7.21, 7.48 and 8.63 ms/s, best at 5 m.

Ghost CPU is unchanged from the lecture (6.0, 6.3, 6.6, 6.9, 7.2 and 8.4 ms/s). Add `H × E_h`. For example at 15 m and 2 ms, `1.23 × 2 + 6.9 = 9.36`.

Expensive handoffs make the handoff term matter more, so the minimum stays at 15 m, and the curve's left side steepens (a sharp border now costs 2.6 times the best band). Cheap handoffs let the ghost term's pull toward small `w` win, so the minimum moves left to 5 m. The best `w` depends on the ratio of handoff cost to ghost cost, and on how far players wander.
</details>

6. *Week 2 · compute.* A 1,200 m seam runs through a busy valley at `ρ = 0.0015` players per m², with `R = 80 m`, on 20 Hz servers. How many ghosts do the two servers hold at `w = 0`, 10 and 30 m, and what is the ghost CPU per second at `w = 0` and 10 m?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 288, 324 and 396 ghosts. Ghost CPU 17.28 ms/s at `w = 0` and 19.44 ms/s at `w = 10`.

`G(0) = 2 × 0.0015 × 1,200 × 80 = 288`. `G(10) = 2 × 0.0015 × 1,200 × 90 = 324`. `G(30) = 396`. At 20 Hz each ghost is updated 20 times a second, so `288 × 20 × 0.003 ms = 17.28` ms/s and `324 × 20 × 0.003 = 19.44` ms/s. Doubling the tick rate doubles the ghost term, which pushes the best band width to the left.
</details>

7. *Week 2 · compute.* A trade road crosses a server border 2 km long. Travellers are at `ρ_t = 0.0008` per m² and walk at 4 m/s in random directions. How many handoffs per second and per hour must the border handle? If the handoff code has a one-in-a-million chance of duplicating an item, how often does this border duplicate one?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 4.07 handoffs per second, about 14,700 per hour, and one duplicate about every 68 hours.

`H_travel = 2 ρ_t v L / π = 2 × 0.0008 × 4 × 2,000 / π = 4.07` per second. Times 3,600 is 14,668 per hour. A duplicate needs on average 1,000,000 handoffs, so `1,000,000 / 14,668 = 68` hours. No band width reduces this number, because these are real crossings. The only fixes are a correct protocol or a border drawn somewhere else.
</details>

8. *Week 2 · code.* This function applies the lecture's hysteresis rule to one player's positions. What does the last line print? Explain the result for `w = 2`.

```python
def count_handoffs(xs, w):
    on_b, count = xs[0] > 0, 0
    for x in xs[1:]:
        if not on_b and x > w / 2:
            on_b, count = True, count + 1
        elif on_b and x < -w / 2:
            on_b, count = False, count + 1
    return count

path = [-3, -1, 0.5, -0.5, 1, 2.5, -1, -2, 1.5, 3, -2.5, -4]
print([count_handoffs(path, w) for w in (0, 2, 4, 6)])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `[6, 4, 2, 0]`

With `w = 2` the band runs from −1 to +1, and the comparisons are strict. The player starts on A. The steps to 0.5, −0.5 and 1 stay inside the band (1 is not greater than 1), so nothing happens. 2.5 hands over to B (1). −1 is not less than −1, so B keeps the player, and −2 hands back to A (2). 1.5 goes to B (3), and −2.5 back to A (4). With `w = 6` the band is ±3 and no position crosses it strictly, so there are no handoffs at all, even though the player walked from −4 to +3.
</details>

9. *Week 2 · explain.* In the Lab 02 harness, messages between servers take 2 ticks, and each tick handles arriving messages before the client's input. Server A sends `transfer` at the end of tick 10 with `next_seq = 11`. The gateway routes input `k` in tick `k`. (a) Which server receives inputs 11 to 16, and what does each do with them? (b) Which inputs sit in B's `pending` at the end of tick 15, and when are they applied? (c) What goes wrong if A stays `authoritative` after sending `transfer`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Input 11 reaches A in tick 11 and is buffered. `transfer` reaches B in tick 12, B becomes authoritative and points the gateway at itself, so inputs 12 to 16 go to B. A receives `ack` in tick 14 and forwards input 11, which reaches B in tick 16. (b) Inputs 12, 13, 14 and 15 wait in `pending`, because B's `next_seq` is 11. In tick 16 input 11 arrives first, B applies 11 to 15 in order, then applies 16 directly. (c) A applies input 11 itself instead of buffering it. Both servers are authoritative in ticks 12 and 13, and B, told to start at input 11, never receives it.

Both (a) and (c) match traced runs of the Lab 02 harness. In (c), A's buffer is empty when the `ack` arrives, so it forwards nothing. B holds 12, 13, 14 and every later input in `pending` forever, so on B the player freezes while the client keeps predicting, and the player sees a long snap back. The harness catches the two-owner ticks with `worst <= 1` and the missing inputs with the `applied` check. In a real game, the two-owner window is also long enough to loot the same chest on both servers.
</details>

## Week 3: Spatial partitioning at scale

Lecture: [w03-spatial-partitioning-at-scale.md](../lectures/w03-spatial-partitioning-at-scale.md). `L(m, s) = k (c_p + c_i (m − 1) + c_x (m − k))` with `k = m / s`, `c_p = 20`, `c_i = 2`, `c_x = 4` µs.

10. *Week 3 · compute.* A crowd of 240 players, everyone in everyone's AOI, meets at a world boss. Compute the per-server load and the useful share for `s = 1`, 2 and 3. Then compute the load if the same 240 were split into 3 layers instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `s = 1`: 119.52 ms. `s = 2`: 117.36 ms each, useful share 51%. `s = 3`: 91.04 ms each, useful share 44%. Three layers of 80: 14.24 ms each.

`L(240, 1) = 240 × (20 + 2 × 239) = 240 × 498 = 119,520 µs`. For `s = 2`, `k = 120` and each owned player costs `20 + 478 + 4 × 120 = 978 µs`, so 117.36 ms. For `s = 3`, `k = 80` and each costs `20 + 478 + 640 = 1,138 µs`, so 91.04 ms, total 273.1 ms, and `119.52 / 273.12 = 44%`.

A layer is a split where players cannot see across copies, so each player has only 79 neighbours and no foreign ones: `80 × (20 + 2 × 79) = 14,240 µs`. Spatial splitting leaves every server over budget. Layering fits easily, at the price of players not seeing each other.
</details>

11. *Week 3 · code.* What does this print? What does it tell you about halving `c_x` compared with any partitioning algorithm?

```python
C_P, C_I, C_X = 20, 2, 4

def load_ms(m, s, c_x=C_X):
    k = m / s
    return k * (C_P + C_I * (m - 1) + c_x * (m - k)) / 1000

def servers_needed(m, c_x=C_X, budget=50):
    s = 1
    while load_ms(m, s, c_x) > budget:
        s += 1
    return s

print(servers_needed(400), servers_needed(400, c_x=2), servers_needed(400, c_x=0))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `19 13 7`

A 400-player crowd needs 19 servers with the lecture's cut cost, 13 with half of it, and 7 if cut pairs cost nothing extra. Halving the extra cost of a cut pair saves 6 servers, a third of the fleet. No partitioning algorithm can do that for a crowd where everyone sees everyone, because every split converts local pairs into cut pairs whatever shape the regions have. The lecture's advice follows: make cut pairs cheap (batch ghost updates, send ghosts at a lower rate, resolve interactions on one side) before making partitions clever.
</details>

12. *Week 3 · compute.* A dynamic partition wants to move a 800 m border 40 m through an area at `ρ = 0.0025` players per m². Handoffs cost 1 ms each, and the rebalancer may spend at most 4 ms of handoff CPU per 100 ms tick. How many handoffs does the move cause, how many ticks must it be spread over, and what is the border's speed?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 80 handoffs, spread over at least 20 ticks (2 seconds at 10 Hz), so the border moves at most 20 m/s.

The swept strip holds `0.0025 × 800 × 40 = 80` players. At 4 handoffs per tick, `80 / 4 = 20` ticks. `40 m / 2 s = 20 m/s`. Moving it in one tick would cost 80 ms of handoff work, more than the whole 50 ms budget.
</details>

13. *Week 3 · design.* Three partitions of the same 16-server world have these results (budget 50 ms). P1: busiest 58 ms, mean 14 ms, 5% of pairs cut. P2: busiest 47 ms, mean 21 ms, 30% cut. P3: busiest 44 ms, mean 29 ms, 55% cut. Compute each imbalance and choose one for launch. Justify your choice with two numbers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Imbalances 4.14, 2.24 and 1.52. P1 is out because its busiest server is over budget. Choose P2.

`58 / 14 = 4.14`, `47 / 21 = 2.24`, `44 / 29 = 1.52`. P2 and P3 both fit. P3 buys 3 ms more margin on the busiest server, but its cluster works `29 / 21 = 1.38` times harder, and 55% of its pairs are cut. Cut pairs cost three times a local pair, so when the crowds grow, P3's load grows faster than P2's. A defensible alternative is P3 if you expect crowds to stay the same size and the busiest server is your only concern. What matters is naming the trade between busiest load and cut.
</details>

## Week 4: Replication prioritization and relevancy

Lecture: [w04-replication-prioritization-and-relevancy.md](../lectures/w04-replication-prioritization-and-relevancy.md). `p = w × d0 / max(d, d0)` with `d0 = 10 m`, fair share `ρ_i = min(1, λ p_i)`, 20 Hz.

14. *Week 4 · compute.* A client in a PvP skirmish has `B = 15` updates per tick. Relevant entities: its target (weight 5, 10 m), 4 party members (weight 2, 10 m), 10 enemy players (weight 2, 30 m), 40 NPCs (weight 1, 20 m) and 100 far NPCs (weight 1, 100 m). Compute `λ` and each group's update interval in ticks and in ms.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `λ = 0.3134`. Target every tick (50 ms). Party 1.60 ticks (80 ms). Enemies 4.79 ticks (239 ms). NPCs 6.38 ticks (319 ms). Far NPCs 31.9 ticks (1,595 ms).

Priorities: target 5, party 2 each (8 total), enemies `2 × 10/30 = 0.667` each (6.67 total), NPCs `1 × 10/20 = 0.5` each (20 total), far NPCs 0.1 each (10 total). The sum is 49.67. First guess `λ = 15 / 49.67 = 0.302` gives the target `1.51`, so it is capped. Then `λ = 14 / 44.67 = 0.3134`. The party gets `2 × 0.3134 = 0.627`, below 1, so nothing else is capped. Intervals are `1 / (λ p)`: party `1 / 0.627 = 1.60`, enemies `1 / 0.209 = 4.79`, NPCs `1 / 0.157 = 6.38`, far NPCs `1 / 0.0313 = 31.9`. Slots used: `1 + 2.51 + 2.09 + 6.27 + 3.13 = 15`.
</details>

15. *Week 4 · compute.* Continue question 14. Everything runs at 6 m/s. Compute each group's angular error `v × interval / d`. Which groups share an angle, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Target 1.72°, party 2.74°, enemies 2.74°, NPCs 5.48°, far NPCs 5.48°.

Party: `6 × 0.080 / 10 = 0.048` rad = 2.74°. Enemies: `6 × 0.239 / 30 = 0.048` rad, the same. NPCs: `6 × 0.319 / 20 = 0.096` rad = 5.48°, and far NPCs `6 × 1.595 / 100 = 0.096` rad, the same.

For uncapped entities with inverse-distance falloff, `angle = v × tick / (λ w d0)`. Distance cancels, so entities of the same weight share an angle wherever they stand. Weight-1 groups have twice the error of weight-2 groups. The capped target is better than the formula because it cannot be sent more than once per tick.
</details>

16. *Week 4 · code.* What does this print? Check that the rates use the whole budget.

```python
def fair_rates(prios, budget):
    capped = set()
    while True:
        rest = [i for i in range(len(prios)) if i not in capped]
        lam = (budget - len(capped)) / sum(prios[i] for i in rest)
        new = {i for i in rest if lam * prios[i] >= 1}
        if not new:
            break
        capped |= new
    return [1.0 if i in capped else lam * p for i, p in enumerate(prios)], lam

rates, lam = fair_rates([6, 3, 1, 1, 1, 1], 3)
print([round(r, 3) for r in rates], round(lam, 3))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `[1.0, 0.857, 0.286, 0.286, 0.286, 0.286] 0.286`

First pass: `λ = 3 / 13 = 0.231`, and the priority-6 entity gets `1.38 ≥ 1`, so it is capped. Second pass: `λ = 2 / 7 = 0.286`. The priority-3 entity gets `0.857`, below the cap, so the loop stops. The rates sum to `1 + 0.857 + 4 × 0.286 = 3.0`, the whole budget. Note that the priority-3 entity is not capped although its priority is half the capped one's. Capping one entity raises `λ` for everyone else.
</details>

17. *Week 4 · compute.* With inverse-distance falloff, `λ = 0.25` updates per unit priority, a 20 Hz tick and `d0 = 10 m`, an enemy player (weight 2) runs at 4 m/s. What angular error does it have? What does an NPC (weight 1) at the same speed have? A crowd arrives elsewhere and `λ` drops to 0.2. What is the enemy's new error?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.29°, 4.58°, then 2.86°.

`angle = v × tick / (λ w d0) = 4 × 0.05 / (0.25 × 2 × 10) = 0.04` rad = 2.29°. Weight 1 doubles it to 4.58°. With `λ = 0.2`, `0.2 / (0.2 × 2 × 10) = 0.05` rad = 2.86°, although the crowd is nowhere near the enemy. The water level is shared by every entity on the client.
</details>

18. *Week 4 · compute.* A client's relevancy rule is "open at `d < 60 m`, close at `d > 60 m`" with no hysteresis. Thirty players mill at the edge and each flickers open and closed once a second. Opening a ghost costs 150 bytes and an ongoing delta costs 25 bytes. How much extra bandwidth does the flicker cost? Separately, the same client sees 180 relevant entities and the designer wants a 1.5-second maximum interval at 20 Hz. How many of the client's slots per tick does the floor reserve?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3,750 B/s extra (30 kbit/s). The floor reserves 6 slots per tick.

Each flicker sends a 150-byte opening instead of a 25-byte delta, so 125 extra bytes, 30 times a second: 3,750 B/s. That is six deltas' worth per flicker. Fix it with a close radius of 70 m and a delay before closing, as Unreal does with its 5-second rule.

The floor promises each entity a send every `1.5 × 20 = 30` ticks, so it needs `180 / 30 = 6` slots per tick whatever the priorities say.
</details>

## Week 5: Bandwidth shaping and LOD for networking

Lecture: [w05-bandwidth-shaping-and-lod-for-networking.md](../lectures/w05-bandwidth-shaping-and-lod-for-networking.md). Error-driven rate `min(r_max, max(r_min, √(a / (2θd)) + c))`, idle rate 0.2 Hz, 20 bytes per update.

19. *Week 5 · compute.* A mount race uses `θ = 0.5°`. A rider at 60 m turns with `a = 3 m/s²` and changes input suddenly 0.5 times a second. Compute the threshold `ε`, the smooth-motion interval and the update rate. Compare with a 5 Hz tier.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ε = 0.524 m`, smooth interval 0.591 s, rate 2.19 Hz, less than half the 5 Hz tier.

`ε = θ d = 0.008727 × 60 = 0.524` m. `T = √(2ε / a) = √(1.047 / 3) = 0.591` s, so the smooth rate is 1.69 Hz. Adding 0.5 sudden changes per second gives 2.19 Hz. A 5 Hz tier sends 2.3 times as often, which only pays off if riders change input more often than the model assumes.
</details>

20. *Week 5 · compute.* A market town has 20 entities near (10 m), 60 mid (50 m) and 120 far (120 m). 40% of each band is moving, with `a = 2 m/s²`, `θ = 1°` and `c = 1`. Use the lecture's tiers (20 Hz × 20 B, 5 Hz × 12 B, 1 Hz × 6 B). Compute flat, tiered and error-driven bandwidth in kbit/s. Then compute the error-driven cost when everyone moves with `c = 3`. The client link is 96 kbit/s.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Flat 640.0 kbit/s, tiers 98.6 kbit/s, error-driven 29.1 kbit/s. In the panic the error-driven stream is 127.2 kbit/s, over the link.

Flat: `200 × 20 × 20 = 80,000` B/s. Tiers: `20 × 400 + 60 × 60 + 120 × 6 = 8,000 + 3,600 + 720 = 12,320` B/s.

Moving rates: near `√(2 / (2 × 0.1745)) + 1 = 3.39` Hz, mid (`ε = 0.873 m`) 2.07 Hz, far (`ε = 2.094 m`) 1.69 Hz. Near: `20 × (8 × 3.39 + 12 × 0.2) = 591` B/s. Mid: 1,138 B/s. Far: 1,911 B/s. Total 3,640 B/s.

Panic, everyone moving with `c = 3`: rates 5.39, 4.07 and 3.69 Hz, so `20 × (20 × 5.39 + 60 × 4.07 + 120 × 3.69) = 15,900` B/s. The tiers overrun the 96 kbit/s link by 3% every evening. Error-driven uses under a third of the link on a normal evening and needs a shaper for the panic.
</details>

21. *Week 5 · code.* This is the lecture's token bucket. The steady stream is 4,000 B/s (200 bytes per 50 ms tick) and a 6,000-byte burst arrives on tick 10. What does it print? Check the clearing time against the drain formula.

```python
def bucket(demand, rate, depth, tick=0.05):
    tokens, backlog, out = depth, 0.0, []
    for want in demand:
        tokens = min(depth, tokens + rate * tick)
        backlog += want
        sent = min(tokens, backlog)
        tokens -= sent
        backlog -= sent
        out.append(backlog)
    return out

demand = [200.0] * 40
demand[10] += 6_000
q = bucket(demand, rate=10_000, depth=3_000)
print(round(max(q)), q.index(max(q)), next(i for i in range(10, 40) if q[i] < 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `3200 10 21`

Before the burst the bucket is full at 3,000 bytes. On tick 10 the client wants 6,200 bytes, the bucket lets out 3,000, and 3,200 remain. Each later tick adds 500 tokens and 200 bytes of demand, so the backlog drains by 300 bytes per tick and needs 11 ticks, clearing on tick 21. That is 550 ms. The formula gives `(X − σ) / (ρ − s) = (6,200 − 3,000) / (10,000 − 4,000) = 0.533` s, which the 50 ms ticks round up to 0.55 s.
</details>

22. *Week 5 · compute.* Field LOD. Positions are quantized over a 512 m region with a step of `2θd`. How many bits per axis does an entity need at 5, 25 and 80 m with `θ = 1°`? And with `θ = 2°`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** At 1°: 12, 10 and 8 bits. At 2°: 11, 9 and 7 bits.

At 5 m the step is `2 × 0.01745 × 5 = 0.175` m, and `512 / 0.175 = 2,934` needs 12 bits (`2¹² = 4,096`). At 25 m the step is 0.873 m and `512 / 0.873 = 587` needs 10 bits. At 80 m the step is 2.79 m and `512 / 2.79 = 183` needs 8 bits. Doubling θ halves each ratio and saves exactly one bit per axis. Across three axes, near to far saves 12 bits per update, which is modest next to dropping whole fields.
</details>

23. *Week 5 · critique.* A team's shaper drains its queue in arrival order. The client's steady stream is 6,800 B/s, the shaper's rate is 12,000 B/s, and the player runs through a gate that opens 150 ghosts at 60 bytes each just before their target's next update. Roughly how long does the target's update wait? What two queue rules fix it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 1.7 seconds. Drain the queue in priority order, and replace a waiting update with a newer one instead of appending.

The 9,000 bytes of ghosts sit ahead of the target, and they drain at the spare rate `12,000 − 6,800 = 5,200` B/s: `9,000 / 5,200 = 1.73` s. For that time the player's target is frozen. With a priority queue the target goes out on the next tick and the ghosts fill the spare bytes after it. With replace-not-append, each entity has at most one waiting update, so the backlog is bounded by the number of entities, not by time.
</details>

## Week 6: Massive battles

Lecture: [w06-massive-battles.md](../lectures/w06-massive-battles.md). MMO302 week 12's node: `W(n) = 0.0003n + 0.000001n²` CPU-seconds per game-second, `C = 1`, `f = max(0.1, min(1, C / W(n)))`. Events: `r = 2` per pilot per game-second, `k = 12` bytes, summaries of 8 bytes once per real second.

24. *Week 6 · compute.* For a 2,500-pilot battle, compute `W(n)`, the speed `f`, and the per-client event stream with full fan-out, with full fan-out and dilation, and aggregated with dilation (circle 20, squads of 10), in kbit/s. What does the server send in total under full fan-out without dilation?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `W = 7.0`, `f = 0.143`. Per client 480, 68.6 and 16.5 kbit/s. The server sends 1,200 Mbit/s of events under full fan-out without dilation.

`W = 0.75 + 6.25 = 7.0`, so `f = 1 / 7 = 0.143`. Full fan-out: `2,500 × 2 × 12 = 60,000` B/s = 480 kbit/s. With dilation: `480 / 7 = 68.6`. Aggregated: `0.143 × 20 × 24 + 250 × 8 = 68.6 + 2,000 = 2,068.6` B/s = 16.5 kbit/s. Server total: `2,500 × 60,000 = 150` MB/s = 1,200 Mbit/s. Dilation cuts that by the same factor of 7, which a shooter cannot do.
</details>

25. *Week 6 · compute.* At 5,000 pilots, a studio widens each client's circle to 30 entities and summarizes squads of 20 instead of 10. Compute the per-client aggregated stream. Which part dominates it, and what else is wrong at this size?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 16.6 kbit/s, dominated by the summaries (2,000 of 2,072 B/s). The node is past its floor, so its backlog grows by 1.65 CPU-seconds every second.

`W(5,000) = 1.5 + 25 = 26.5`, so `C / W = 0.038` and `f` sits at the floor, 0.1. Circle: `0.1 × 30 × 2 × 12 = 72` B/s. Summaries: `(5,000 / 20) × 8 = 2,000` B/s. Total 2,072 B/s = 16.6 kbit/s. Dilation shrinks the circle's events, but the summaries go out once per real second, so squad size is the lever for the per-client stream. At the floor the node still needs `0.1 × 26.5 = 2.65` CPU-seconds per real second against `C = 1`, so MMO302's backlog grows by 1.65 each second and commands wait longer and longer.
</details>

26. *Week 6 · compute.* A shooter cannot dilate. Each player causes 3 events per second of 16 bytes, and each client's event budget is 256 kbit/s. What is the largest battle that fits under full fan-out? What must a shooter do beyond it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 666 players.

Per client the stream is `n × 3 × 16 = 48 n` B/s, and 256 kbit/s is 32,000 B/s, so `n ≤ 32,000 / 48 = 666.7`, and 666 players fit. Beyond that a shooter must aggregate (a circle in full, summaries for the rest), cut `r` or `k` (fewer, smaller events, such as batching hits), or cap `n` with queues, entry limits or objectives that spread the crowd. PlanetSide 2's 1,158-player record is well past this budget, so a real shooter at that size cannot be sending every event to everyone. The constants are invented, so the number says where the wall is in this model, not in any shipped game.
</details>

27. *Week 6 · code.* What does this print on Python 3.13? What would the last value be on Python 3.11, and why does that matter for a lockstep battle?

```python
hits = [1.0, 1e16, -1e16]

def add_all(values):
    total = 0.0
    for v in values:
        total += v
    return total

print(add_all(hits), add_all(reversed(hits)), sum(hits))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `0.0 1.0 1.0`. On Python 3.11, `sum(hits)` gives `0.0`.

Forward: `1.0 + 1e16` rounds to `1e16`, because doubles near `1e16` are spaced 2 apart, and then `1e16 − 1e16 = 0.0`. The 1.0 is lost. Reversed: `−1e16 + 1e16 = 0.0`, then `+ 1.0 = 1.0`. Since Python 3.12, the built-in `sum` uses Neumaier compensated summation and recovers the 1.0. On 3.11 it adds left to right and gives 0.0.

Two machines that add the same damage in different orders, or with different library versions, disagree in the result. In lockstep every machine must produce identical bits, so this is a desync. That is why lockstep games pin compilers and libraries or use fixed-point arithmetic for game state.
</details>

28. *Week 6 · design.* In a 1,500-player fantasy siege, which of these could be sent lockstep-style as "the cause, not the result", and which must stay server-authoritative state? (a) a catapult volley's cosmetic debris, (b) the damage the volley deals to players, (c) a flock of birds scattering from the walls, (d) which player captured the gatehouse, (e) arrow trails from 200 archer NPCs firing on orders.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Send the cause for (a), (c) and (e). Keep (b) and (d) authoritative.

Debris, birds and arrow trails only need to look right. A seed, a start time and the orders are enough, every client can generate them, and a client that gets them slightly wrong changes nothing. Damage and the capture decide outcomes and create value, so the server must compute them and send the results. If the arrows' hits matter, only their trails can be seeded, and the server still resolves each hit.
</details>

## Week 7: Time dilation revisited

Lecture: [w07-time-dilation-revisited.md](../lectures/w07-time-dilation-revisited.md). Node from MMO302 week 12: `W(n) = 0.0003n + 0.000001n²`, `C = 1`, floor 0.1. Controller as in the lecture's section 2; the backlog `q` is in CPU-seconds, and with `C = 1` it is also the extra seconds a command waits.

29. *Week 7 · compute.* A node at `f = 1` jumps from 500 to 2,500 pilots. (a) What backlog does the first second create? (b) With aim 90% and no payback term, what speed does the controller choose and how long does the backlog take to clear? (c) With `τ = 5`, what does the controller choose in the next second, how fast does the backlog fall, and why is the payback slower than you might hope?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6.0 CPU-seconds of backlog. (b) `f = 0.129`, and the backlog clears in 60 seconds. (c) The target is below the floor, so `f = 0.1`. The backlog falls 0.3 per second and clears at second 22 in the lecture's code. The floor limits how fast any controller can repay debt.

`W(2,500) = 0.75 + 6.25 = 7.0`. The first second runs at `f = 1`, so the backlog is `7.0 − 1 = 6.0`. Without payback the target is `0.9 / 7 = 0.129`, demand is 0.9, and `6.0 / 0.1 = 60` s. With `τ = 5` the target is `(0.9 − 6.0 / 5) / 7 = −0.043`, clamped to 0.1. At the floor, demand is `0.1 × 7 = 0.7`, so the backlog falls by 0.3 per second. Once the backlog drops below 1.0 the target rises above the floor and repayment slows, so it clears at 22 s rather than 20 s. In section 2's 2,000-pilot example the floor allowed a drop of 0.54 per second. A bigger fleet leaves less room under the floor.
</details>

30. *Week 7 · code.* What does this print? Explain the second and third tuples.

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1

def work(n):
    return A * n + B * n * n

def run(pilots, aim=0.9, tau=5, a_down=1.0, a_up=0.2):
    f, q, rows = 1.0, 0.0, []
    for n in pilots:
        m = work(n)
        q = max(0.0, q + f * m - C)
        rows.append((round(f, 3), round(q, 2)))
        target = min(1.0, max(FLOOR, (aim * C - q / tau) / m))
        f += (a_down if target < f else a_up) * (target - f)
    return rows

rows = run([2000] * 5 + [500] * 4)
print(rows[4:])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `[(0.102, 1.45), (0.108, 0.49), (0.286, 0.0), (0.429, 0.0), (0.543, 0.0)]`

The second tuple is the first second after the fleet leaves. The node runs at `f = 0.108` (set from the last 2,000-pilot second) on `W(500) = 0.4`, so demand is 0.043, and the backlog falls from 1.45 to `1.45 + 0.043 − 1 = 0.49`. The controller's target is then `(0.9 − 0.49 / 5) / 0.4 = 2.0`, clamped to 1. Because the target is above `f`, the slow gain applies, and `f` moves only a fifth of the way: `0.108 + 0.2 × (1 − 0.108) = 0.286`. The backlog is now zero, and `f` keeps climbing by a fifth of the remaining gap each second. It passes 0.9 ten seconds after the fleet left. That is the price of "drop fast, recover slow".
</details>

31. *Week 7 · compute.* Using the node model, what is the largest fight the node can hold at the floor without the backlog growing, (a) with aim 80% and a 10% floor, (b) with aim 90% and a 5% floor?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 2,682 pilots. (b) about 4,095 pilots.

(a) `0.1 × W(n) = 0.8`, so `n² + 300n − 8,000,000 = 0` and `n = (−300 + √(90,000 + 32,000,000)) / 2 ≈ 2,682`. (b) `0.05 × W(n) = 0.9`, so `n² + 300n − 18,000,000 = 0` and `n ≈ 4,095`. More headroom lowers the ceiling. A lower floor raises it, and each player then waits twice as long per game-second.
</details>

32. *Week 7 · compute.* Six seamless servers in a row need speeds 1.0, 0.6, 1.0, 0.3, 1.0 and 1.0 on their own. Compute delivered game-seconds per real second as one clock domain, with the best single gate, and with the best pair of gates.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One domain 1.8. Best single gate 3.2, between servers 4 and 5. Best two gates 4.1, on both sides of server 4.

One domain runs at the minimum: `6 × 0.3 = 1.8`. One gate between 4 and 5 gives `{1, 2, 3, 4}` at 0.3 and `{5, 6}` at 1.0: `1.2 + 2.0 = 3.2`. The other single gates give 2.5, 2.4, 2.7 and 2.5. Two gates around server 4 give `{1, 2, 3}` at 0.6, `{4}` at 0.3 and `{5, 6}` at 1.0: `1.8 + 0.3 + 2.0 = 4.1`. Isolate the slowest server first, then the next slowest.
</details>

33. *Week 7 · compute.* An ordinary node (`C = 1`) hosts a system with 2,200 pilots and quiet systems whose load totals 0.4. (a) What speed does everyone on the node run at? (b) The fight's system is moved at downtime to a dedicated node with `C = 2`. What are the speeds now? (c) The next evening, half the crowd follows a target into a neighbouring system that still shares the ordinary node with the quiet systems. What are the speeds, and what does this say about booking nodes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 16.9%. (b) Fight 36.4%, quiet systems 100%. (c) Reinforced system 100%, the neighbour and the quiet systems 51.5%. A booking protects a system, not a fight.

(a) `W(2,200) = 0.66 + 4.84 = 5.5`, plus 0.4 is 5.9, so `f = 1 / 5.9 = 16.9%` for every system on the node, including the quiet ones. (b) The fight runs at `2 / 5.5 = 36.4%`, and the quiet systems carry 0.4 on `C = 1`, so they run at full speed. (c) Each half has `W(1,100) = 0.33 + 1.21 = 1.54`. The reinforced node has room to spare and runs at 100%. The ordinary node carries `1.54 + 0.4 = 1.94`, so it runs at `1 / 1.94 = 51.5%`. Nodes are mapped at downtime, so the booking cannot follow the crowd. Book every system the fight can reach, and keep the controller's headroom for the rest.
</details>

## Week 8: Distributed simulation research

Lecture: [w08-distributed-simulation-research.md](../lectures/w08-distributed-simulation-research.md). `F_A(k) = max(F_A(k−1), F_B(k−L) + δ) + X_A(k)`, symmetric for B.

34. *Week 8 · code.* What do the two lines print? The same patterns over 100 ticks give 59.9 ms per tick at `L = 1` and 40.0 ms at `L = 2`. Why is 59.9 above the lecture's estimate `max(X, (X + δ) / L)`?

```python
def finish_times(xa, xb, L, delay=0):
    fa, fb = [0] * (len(xa) + 1), [0] * (len(xb) + 1)
    for k in range(1, len(xa) + 1):
        need = k - L
        wait_a = fb[need] + delay if need >= 1 else 0
        wait_b = fa[need] + delay if need >= 1 else 0
        fa[k] = max(fa[k - 1], wait_a) + xa[k - 1]
        fb[k] = max(fb[k - 1], wait_b) + xb[k - 1]
    return fa[1:], fb[1:]

print(finish_times([30, 50, 30, 50], [50, 30, 50, 30], L=1, delay=10))
print(finish_times([30, 50, 30, 50], [50, 30, 50, 30], L=2, delay=10))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**
```
([30, 110, 140, 230], [50, 80, 170, 200])
([30, 80, 110, 160], [50, 80, 130, 160])
```

At `L = 1`, A's tick 2 waits for B's tick 1 (finished at 50) plus 10 ms, so it starts at 60 and ends at 110. B's tick 2 waits for A's tick 1 (30 + 10 = 40), but its own tick 1 ends at 50, so it starts at 50 and ends at 80. The pattern repeats, and each pair of ticks costs about 120 ms.

The estimate uses the average tick, 40 ms, and gives `max(40, 50) = 50`. With `L = 1`, every tick waits for the neighbour's matching tick, which alternates between slow and fast out of phase with your own, so each server inherits the other's slow ticks. Jitter adds about 10 ms per tick on top of the delay. At `L = 2` one tick of slack absorbs both the jitter and the 10 ms delay, and the pair runs at its 40 ms average.
</details>

35. *Week 8 · compute.* Two servers average 35 ms per tick. With `max(X, (X + δ) / L)`, what is the effective tick at `L = 1` and 2 for `δ = 25 ms`, and at `L = 2`, 3 and 4 for `δ = 80 ms`? What is the smallest lookahead that keeps each pair at its average?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `δ = 25`: 60 ms at `L = 1`, 35 ms at `L = 2`, so `L = 2` is enough. `δ = 80`: 57.5 ms at `L = 2`, 38.3 ms at `L = 3`, 35 ms at `L = 4`, so `L = 4`.

`(35 + 25) / 1 = 60`. `(35 + 25) / 2 = 30 < 35`, so 35. `(35 + 80) / 2 = 57.5`, `/ 3 = 38.3`, `/ 4 = 28.75 < 35`. In general you need `L ≥ (X + δ) / X`, so `L ≥ 1.71` and `L ≥ 3.29`. Real ticks jitter, so add a tick of margin as the lecture's random run shows.
</details>

36. *Week 8 · compute.* A 30 Hz seamless MMO has four cross-border abilities: a spear throw at 40 m/s with an 8 m minimum range, a spell with a 1.2 s cast bar whose landing is fixed when the cast starts, a shield bash applied next tick, and a trap that arms 0.5 s after placement. Compute each lookahead in ticks and the border's lookahead. Propose one change that raises the border to at least 4 ticks.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Spear 6 ticks, spell 36, shield bash 1, trap 15. The border's lookahead is 1, set by the shield bash.

A tick at 30 Hz is 33.3 ms. Spear: `8 / 40 = 0.2` s = 6 ticks. Spell: 1.2 s = 36 ticks. Trap: 0.5 s = 15 ticks. The bash is applied in the next tick, so 1.

Two fixes, either enough. Give the bash a wind-up of at least 133 ms (4 ticks) whose target and hit are fixed when the wind-up starts. Or give it a range shorter than the handoff band, so attacker and target always share an owner and the bash never crosses the border. The first costs a little feel. The second costs nothing if the band is wider than the bash's reach.
</details>

37. *Week 8 · compute.* A server finishes tick 199 at 9,950 ms. Its neighbour finished tick 197 at 9,930 ms. Messages take 25 ms, the lookahead is 3, and the server's tick 200 takes 45 ms. When does it finish tick 200? Does it stall, and by how much? What would change with a lookahead of 4?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It stalls 5 ms and finishes tick 200 at 10,000 ms. With a lookahead of 4 it would not stall if the neighbour's tick 196 had finished by 9,925 ms.

Tick 200 needs the neighbour's tick `k − L = 200 − 3 = 197`, whose message arrives at `9,930 + 25 = 9,955` ms. Its own tick 199 ended at 9,950, so it waits 5 ms and finishes at `9,955 + 45 = 10,000` ms. With `L = 4` it needs tick 196 instead, which finished earlier than tick 197, so the message is more likely to be waiting already. Always check the index `k − L` before putting numbers in.
</details>

38. *Week 8 · compute.* On a border, 5% of ticks bring a straggler from the other server, and each rollback undoes 6 ticks. What share of work does optimistic synchronization waste? Compare with the conservative results in the lecture's random run at 20 ms delay for `L = 1` and `L = 3`, and choose.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 30% wasted. Conservative wastes 31% at `L = 1` (72.4 ms instead of 50) and about 1.6% at `L = 3` (50.8 ms). Choose conservative with a lookahead of 3.

`p × D = 0.05 × 6 = 0.30`. At `L = 1` the two are a tie, and rollback also has to undo ticks that clients may already have seen. At `L = 3` conservative synchronization costs almost nothing, and nothing ever has to be undone on a player's screen. Optimistic only wins when the rules cannot give you lookahead and stragglers are rare.
</details>

## Week 9: Server meshing concepts

Lecture: [w09-server-meshing-concepts.md](../lectures/w09-server-meshing-concepts.md). `T_k(N) = c_p N/k + c_i N²/k + c_g N (1 − 1/k)`, `c_p = 20 µs`, `c_i = 2 µs`, `c_g = 4 µs`, budget 50 ms.

39. *Week 9 · compute.* A 500-player crowd where everyone sees everyone is meshed across 8 servers. Compute the tick time and the ghost part of it. Does it fit? Find the fewest servers that fit and the replication layer's ghost updates per second at 20 Hz for that mesh.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 65.5 ms on 8 servers (ghosts 1.75 ms), over budget. 11 servers fit (48.2 ms). The layer then delivers 5,000 ghost updates per tick, 100,000 per second.

Owned work on 8: `(20 µs × 500 + 2 µs × 250,000) / 8 = (10 + 500) / 8 = 63.75` ms. Ghosts: `4 µs × 500 × 7/8 = 1.75` ms. Total 65.5 ms. On 10 servers: `51 + 1.8 = 52.8` ms, still over. On 11: `510 / 11 + 4 µs × 500 × 10/11 = 46.4 + 1.8 = 48.2` ms. Ghost updates: `500 × (11 − 1) = 5,000` per tick.
</details>

40. *Week 9 · compute.* Ghost updates get more expensive after a physics feature, `c_g = 8 µs`. Compute crowd capacity at `k = 1`, 4, 16 and 64 and the ghost ceiling. Compare with the lecture's 153, 308, 613 and 1,199 at 4 µs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 153, 305, 598 and 1,141 players. The ceiling halves from 12,500 to 6,250.

Capacity solves `(c_i / k) N² + (c_p / k + c_g (1 − 1/k)) N − 0.05 = 0`. At `k = 1` there are no ghosts, so 153 is unchanged. The loss grows with `k`: 1% at 4 servers, 2% at 16, 5% at 64, because ghosts are a larger share of each smaller server's tick. The ceiling is `budget / c_g = 0.05 / 8×10⁻⁶ = 6,250`. A cheaper ghost barely matters for small meshes and sets the limit for large ones.
</details>

41. *Week 9 · code.* This is a simplified authority table. What does it print? Explain the fourth entry.

```python
class AuthorityTable:
    def __init__(self):
        self.owner, self.epoch, self.log = {}, {}, []

    def grant(self, entity, server):
        self.epoch[entity] = self.epoch.get(entity, 0) + 1
        self.owner[entity] = server
        return self.epoch[entity]

    def write(self, entity, server, epoch):
        ok = epoch == self.epoch.get(entity) and server == self.owner.get(entity)
        self.log.append(f"{server}@{epoch}:{'ok' if ok else 'rejected'}")
        return ok

t = AuthorityTable()
ea = t.grant(7, "A")
t.write(7, "A", ea)
eb = t.grant(7, "B")
t.write(7, "A", ea)
ea2 = t.grant(7, "A")
t.write(7, "B", eb)
t.write(7, "A", ea)
t.write(7, "A", ea2)
print(t.log)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `['A@1:ok', 'A@1:rejected', 'B@2:rejected', 'A@1:rejected', 'A@3:ok']`

A writes with epoch 1 while it owns entity 7. Authority moves to B (epoch 2), so A's late write with 1 is rejected. Authority returns to A (epoch 3), so B's write with 2 is rejected. The fourth entry is a write from A, which is the owner again, but it carries epoch 1 from A's first term, for example a write computed before a long pause. The owner check alone would accept it and overwrite newer state. The epoch check rejects it. That is the case Lab 09 step 6 asks you to build.
</details>

42. *Week 9 · compute.* 400 players mill in a disc of 40 m radius that a mesh has cut with one straight line through the centre. Their average speed across the line is 0.8 m/s in each direction. Estimate authority transfers per second at that cut. If the crowd is split over 8 servers with parallel cuts of similar length, what is the total?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 10 transfers per second at one cut, about 71 per second across 7 cuts.

`ρ = 400 / (π × 40²) = 400 / 5,027 = 0.0796` per m². The cut is `ℓ = 80 m`. Crossings: `2 × ρ × v⊥ × ℓ = 2 × 0.0796 × 0.8 × 80 = 10.2` per second. Eight servers need 7 cuts, so about 71 per second. Parallel cuts near the edge of the disc are shorter, so treat this as an upper estimate. Each transfer is an epoch bump in the layer, and a handoff band cuts the dithering share of them.
</details>

## Week 10: Consistency models

Lecture: [w10-consistency-models.md](../lectures/w10-consistency-models.md). `W = T + d` tick-aligned, `W = d` flushed, `P(conflict) = 1 − e^(−2λW)`, forward latency `2d + T` on average and `2d + 2T` at worst.

43. *Week 10 · compute.* Two 20 Hz servers share a seam with a 2 ms link. A resource node on the seam gets 1 claim per second from the other side. What share of guessed claims conflict, tick-aligned and flushed? What does forwarding cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9.9% tick-aligned, 0.40% flushed. Forwarding adds 54 ms on average and 104 ms at worst.

`W = 50 + 2 = 52` ms, so `2λW = 0.104` and `P = 1 − e^(−0.104) = 9.9%`. Flushed, `W = 2` ms, `2λW = 0.004` and `P = 0.40%`. Forward: `2 × 2 + 50 = 54` ms and `4 + 100 = 104` ms. Flushing turns a bad guess into an acceptable one.
</details>

44. *Week 10 · compute.* The design team accepts one reversal per 200 claims (0.5%). On 20 Hz servers with a 2 ms link, above what claim rate should an object be forwarded instead of guessed? What if the servers run at 60 Hz?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.048 claims per second at 20 Hz (about one every 21 seconds). 0.134 per second at 60 Hz.

`λ* = −ln(1 − 0.005) / (2W)`. At 20 Hz, `W = 0.052` and `λ* = 0.005013 / 0.104 = 0.048`. At 60 Hz, `W = 16.7 + 2 = 18.7` ms and `λ* = 0.005013 / 0.0373 = 0.134`. Tripling the tick rate raises the threshold 2.8 times. Flushing (`W = 2 ms`) would raise it to 1.25 per second, 26 times.
</details>

45. *Week 10 · code.* Someone "simplified" the lecture's damage counter by replacing `max` with `+` in `merge`. What does this print, what is the true health, and which property of `max` did the change lose?

```python
class Counter:
    def __init__(self, me, max_hp):
        self.me, self.max_hp, self.parts = me, max_hp, {}

    def hit(self, damage):
        self.parts[self.me] = self.parts.get(self.me, 0) + damage

    def merge(self, remote):
        for server, total in remote.items():
            self.parts[server] = self.parts.get(server, 0) + total   # was max(...)

    def hp(self):
        return self.max_hp - sum(self.parts.values())

a, b = Counter("A", 5_000), Counter("B", 5_000)
a.hit(400); s1 = dict(a.parts)
a.hit(100); s2 = dict(a.parts)
b.hit(250)
b.merge(s1); b.merge(s2); b.merge(s2)
a.merge(dict(b.parts))
print(a.hp(), b.hp())
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `2850 3350`. The true health is 4,250. The change lost idempotence, and with it convergence under repeated snapshots.

A dealt 500 and B dealt 250, so the truth is `5,000 − 750 = 4,250`. Snapshots carry running totals, not increments. B adds A's total three times (`400 + 500 + 500 = 1,400`), so B sees `5,000 − 1,650 = 3,350`. A then adds B's inflated view of A to its own 500, getting 1,900 for itself plus 250 for B: `5,000 − 2,150 = 2,850`. The servers disagree with each other and with the truth, and every further merge makes it worse. `max` is idempotent, commutative and associative, so duplicates and reordering change nothing.
</details>

46. *Week 10 · code.* What does this print?

```python
def before(x, y):
    return all(a <= b for a, b in zip(x, y)) and x != y

def relation(x, y):
    if before(x, y):
        return "x->y"
    if before(y, x):
        return "y->x"
    return "concurrent"

p, q, r, s = (1, 0, 2), (1, 1, 2), (0, 2, 2), (2, 1, 3)
print(relation(p, q), relation(q, r), relation(p, r), relation(s, q))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `x->y concurrent concurrent y->x`

`p ≤ q` in every entry and they differ, so `p` happened before `q`. `q` has the larger first entry (1 against 0) and `r` the larger second (2 against 1), so they are concurrent. The same holds for `p` and `r`. For `relation(s, q)`, `s` is not below `q`, but `q = (1, 1, 2)` is below `s = (2, 1, 3)`, so the function returns `y->x`. Concurrent pairs are exactly the pairs that can conflict.
</details>

47. *Week 10 · explain.* A healer on server A shields a tank; A sends the shield to server C with its Lamport clock. Separately, the boss on server B hits the tank (a local event) and then sends the hit to C. C receives the hit first, then the shield. All clocks start at 0 and every event increments the clock. Trace the Lamport clocks. C sorts its combat log by carried timestamp. Does the log order prove the shield came first? What would vector clocks say?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Shield sent with 1 (A = 1). B's hit makes B = 1, sending it makes B = 2, so the hit carries 2. C receives the hit: `max(0, 2) + 1 = 3`. C receives the shield: `max(3, 1) + 1 = 4`. The log shows the shield (1) before the hit (2), but that does not prove anything. Vector clocks give the shield `(1, 0, 0)` and the hit `(0, 2, 0)`, which are concurrent.

A Lamport order is consistent with causality, but a smaller number does not mean "happened before" unless a chain of messages connects the events. Here none does. Which one the tank's owner applied first is a rule of your game. Let the owner decide the order and log the order it used, so the log and the result agree.
</details>

48. *Week 10 · compute.* A boss with 1,500,000 health sits on a seam. 25 players on server B each deal 400 damage per second, and the visibility window is 101 ms. By how much can server A's health bar be too high? What policy decides the boss's death?

<details>
<summary>Answer and worked solution</summary>

**Answer:** At most 1,010 health points, 0.067% of the bar. The boss's owner decides death.

`D_B × W = 25 × 400 × 0.101 = 1,010`. That is below a pixel on almost any health bar, so the merged counter is fine for display. Death is a threshold, so one server, the owner, must decide it and send a single "died" event, or both servers can award loot.
</details>

## Week 11: Physics in MMOs

Lecture: [w11-physics-in-mmos.md](../lectures/w11-physics-in-mmos.md). `N_awake = min(N, δτ)`, exact form `N (1 − e^(−δτ/N))`, `C = f × c_b × N_awake`.

49. *Week 11 · compute.* A 10,000-prop zone runs physics at 20 Hz with `c_b = 5 µs`. In a siege, 8 shots per second each wake 25 props, plus 40 random wake-ups per second. Bodies move for 2.5 s and the sleep timer is 0.5 s. Compute `δ`, `N_awake` by Little's law and by the exact form, and `C`. The physics budget is 150 ms/s. What is the highest step rate it allows?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `δ = 240` per second, `N_awake` 720 (Little) or 695 (exact), `C = 72 ms/s`. The budget allows up to 41 steps per second.

`δ = 8 × 25 + 40 = 240`. `τ = 2.5 + 0.5 = 3` s. Little: `240 × 3 = 720`. Exact: `10,000 × (1 − e^(−720/10,000)) = 695`. `C = 20 × 5 µs × 720 = 72,000 µs = 72` ms/s. For the budget, `f × 5 µs × 720 ≤ 150` ms, so `f ≤ 41.7`.
</details>

50. *Week 11 · compute.* Repeat question 49's awake count with only 1,500 props in the zone, and with 3,000. Why does Little's law overestimate here?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 572 awake with 1,500 props, 640 with 3,000, against Little's 720.

`1,500 × (1 − e^(−720/1,500)) = 1,500 × (1 − 0.619) = 572`. `3,000 × (1 − e^(−0.24)) = 640`. With few props, many wake-ups land on bodies that are already awake and only extend their time. Little's law counts each wake-up as a new body, so it is an upper bound that is tight only while few bodies are awake.
</details>

51. *Week 11 · compute.* A barrel kicked to 3 m/s slows as `v = 3 e^(−1.5t)`. With a sleep tolerance of 0.01 m/s and Box2D's 0.5 s timer, how long does it stay awake? If barrels are kicked 100 times a second, how many are awake?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `t_move = 3.80` s, `τ = 4.30` s, and about 430 barrels are awake.

`3 e^(−1.5t) = 0.01` gives `t = ln(300) / 1.5 = 5.704 / 1.5 = 3.80` s. Add the 0.5 s timer for `τ = 4.30` s. Little's law: `100 × 4.30 = 430`. The damping constant sets `t_move`. Raising damping from 1.5 to 3 per second halves `t_move` to 1.90 s, but the 0.5 s timer stays, so `τ = 2.40` s and the awake count falls from 430 to 240, not to half.
</details>

52. *Week 11 · code.* What does this print, and how many crates must change server?

```python
from collections import Counter

def islands(bodies, contacts):
    parent = {b: b for b in bodies}
    def root(b):
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        return b
    for a, b in contacts:
        parent[root(a)] = root(b)
    groups = {}
    for b in bodies:
        groups.setdefault(root(b), []).append(b)
    return sorted(sorted(g) for g in groups.values())

owner = {"p1": "A", "p2": "B", "p3": "B", "p4": "A", "p5": "B", "p6": "A", "p7": "A"}
contacts = [("p1", "p2"), ("p3", "p4"), ("p2", "p3"), ("p6", "p7")]
moves = 0
for group in islands(owner, contacts):
    votes = Counter(owner[b] for b in group)
    winner = max(sorted(votes), key=votes.get)
    moves += sum(owner[b] != winner for b in group)
    print(group, winner)
print("handoffs", moves)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**
```
['p1', 'p2', 'p3', 'p4'] A
['p5'] B
['p6', 'p7'] A
handoffs 2
```

The contacts chain p1, p2, p3 and p4 into one island even though no single contact joins p1 and p4. Its votes are 2 for A and 2 for B. `max` returns the first maximum of `sorted(votes)`, so ties go to A, and both servers can compute that without talking. p2 and p3 are handed to A, which is 2 handoffs. p5 stays alone on B and p6 and p7 already agree.
</details>

53. *Week 11 · design.* Assign an owner (server, predicted, client-owned with server checks, or client-only cosmetic) to each of these and name one risk of your choice: a boulder players roll downhill onto enemies, a supply cart the player pushes, sparks from a forge, a drawbridge that crushes whoever stands under it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Boulder: server, because it deals damage. Risk: a push feels a round trip late, so predict the push animation only. Cart: predicted (or client-owned with server checks). Risk: corrections snap the cart when the prediction disagrees, and a client-owned cart could be moved into a blocking position without a server check. Sparks: client-only cosmetic, never replicated. Risk: players see different sparks, which is harmless. Drawbridge: server, kinematic, driven by a script, since it kills. Risk: none from physics, but its timing must be replicated precisely or players will die on bridges that look open.
</details>

## Week 12: AI at scale

Lecture: [w12-ai-at-scale.md](../lectures/w12-ai-at-scale.md). Zone 4 km square, 10,000 monsters, tiers 50 / 150 / 400 m at 10 / 2 / 0.2 thinks per second, `c_t = 20 µs`, budget 250 ms/s. `covered(r) = 1 − e^(−nπr²/A)`.

54. *Week 12 · compute.* 100 players spread over the zone. Compute the near, mid and far counts from the coverage formula and the AI cost. Does it fit? What is the largest spread-out player count the default tiers can afford?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Near 479, mid 3,092, far 5,997, cost 243.5 ms/s (97% of the budget). The largest spread count that fits is 103.

`covered(50) = 1 − e^(−100 × 7,854 / 16×10⁶) = 1 − e^(−0.0491) = 0.0479`, so 479 near. `covered(150) = 1 − e^(−0.4418) = 0.357`, so 3,571 within 150 m and 3,092 mid. `covered(400) = 1 − e^(−3.142) = 0.957`, so 9,568 within 400 m and 5,997 far. `C = 20 µs × (4,790 + 6,184 + 1,199) = 243.5` ms/s. Stepping `n` upward, 103 players cost 248.9 ms/s and 104 cost 250.7 ms/s.
</details>

55. *Week 12 · code.* A 20 Hz server has 800 near monsters (10 thinks per second, every 2 ticks), 4,000 mid (every 10 ticks) and 3,000 far (every 100 ticks). What does this print, and what are the worst ticks in ms at 20 µs per think?

```python
def thinks_per_tick(periods, ticks, phased):
    out = []
    for t in range(ticks):
        n = 0
        for i, p in enumerate(periods):
            if p and ((t + i) % p == 0 if phased else t % p == 0):
                n += 1
        out.append(n)
    return out

periods = [2] * 800 + [10] * 4000 + [100] * 3000   # 20 Hz: near 10/s, mid 2/s, far 0.2/s
for phased in (False, True):
    ticks = thinks_per_tick(periods, 100, phased)
    print(phased, max(ticks), sum(ticks) / len(ticks))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**
```
False 7800 830.0
True 830 830.0
```
In step, the worst tick is `7,800 × 20 µs = 156` ms, three times a 50 ms tick. Phased, it is `830 × 20 µs = 16.6` ms.

On tick 0 every tier's period divides 0, so all 7,800 monsters think together. The average is `800/2 + 4,000/10 + 3,000/100 = 400 + 400 + 30 = 830` either way. Phasing by id spreads each tier evenly over its period, so every tick costs the average. Time-slicing removes the spike and does not change the average.
</details>

56. *Week 12 · compute.* A raid pulls 150 monsters. Per-monster A* costs 0.6 ms per search with 4 replans per second. A shared flow field costs 8 ms to build and is rebuilt 4 times a second. Compare the two and find the break-even monster count.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A* costs 360 ms/s, the flow field 32 ms/s. They break even at 13.3 monsters, so from 14 chasing monsters the field wins.

`150 × 4 × 0.6 = 360` ms/s, more than the whole 250 ms/s AI budget. `4 × 8 = 32` ms/s plus a cheap lookup per monster. Break-even: `n × 4 × 0.6 = 32`, so `n = 13.3`. Per-monster search scales with monsters, and the shared field scales with goals.
</details>

57. *Week 12 · compute.* An AI server on another machine reads the world from a 20 Hz zone server over a 3 ms link and sends commands back. Estimate the extra reaction delay. Compare it with the near tier's own average delay, and say which monsters you would keep on the zone server.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 56 ms, slightly more than the near tier's 50 ms average delay.

`W ≈ T + d = 50 + 3 = 53` ms to see the world, plus 3 ms for the command to return, so 56 ms. A near-tier monster already reacts `1 / (2 × 10) = 50` ms late on average, so the AI server roughly doubles it. Keep bosses and near-tier monsters in combat on the zone server. Move mid and far tiers, whose 250 ms and 2.5 s delays hide the extra 56 ms completely.
</details>

## Week 13: Cost engineering

Lecture: [w13-cost-engineering.md](../lectures/w13-cost-engineering.md). `K_cpu = 1000 P_s / (Z N u)`, `K_net = 1000 b × 3600 / 10⁹ × P_e`, `Z = 8`, `P_s = $0.40`, `N = 937.5` at `h = 0.1` unless stated.

58. *Week 13 · compute.* An MMO measures 5,000 B/s per client, pays $0.05 per GB of egress and $0.20 per 1,000 player-hours for services, and runs at 60% fill. Compute each term, the shares, the cost per CCU-month and the monthly bill at 50,000 average CCU.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Compute $0.089, network $0.900, services $0.200, total $1.189 per 1,000 player-hours. Shares 7.5%, 75.7% and 16.8%. $0.868 per CCU-month, about $43,400 a month at 50,000 CCU.

Compute: `1000 × 0.40 / (8 × 937.5 × 0.6) = 400 / 4,500 = 0.0889`. Network: `5,000 × 3,600 = 18` MB per player-hour, 0.018 GB, times $0.05 is $0.0009, or $0.900 per 1,000. CCU-month: `1.189 × 730 / 1,000 = $0.868`, and `0.868 × 50,000 = $43,394`.
</details>

59. *Week 13 · compute.* Continue question 58. Compute the saving of each lever: a 2× faster server, a byte cut to 3,500 B/s, and fill raised to 80%. Check the byte cut with the share rule, and explain why the share rule overstates the speed-up.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2× speed saves 2.5%, the byte cut 22.7%, and 80% fill 1.9%.

A 2× speed-up raises `N` from 937.5 to 1,419.3, only 1.51 times, so compute falls from 0.0889 to 0.0587 and the total by 2.5%. The share rule with `s = 2` would say `0.075 × 0.5 = 3.7%`, but a 2× faster CPU does not double capacity, because the pair term grows with `n²` (week 1). Bytes: `0.757 × (1 − 3,500/5,000) = 0.757 × 0.3 = 22.7%`, exact, because the network term is linear in `b`. Fill: compute falls to `0.0889 × 0.6/0.8 = 0.0667`, saving 1.9%.
</details>

60. *Week 13 · compute.* On the lecture's baseline ($2.085 per 1,000 player-hours, compute $0.107), the team moves 40% of the fleet to spot at a 70% discount. The provider can reclaim half of the spot servers at once. What is the fill limit, the blended server price and the saving? The fleet runs at 50% fill. Is it safe?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Fill limit 80%, blended price $0.288 per server-hour, saving 1.4%. At 50% fill it is safe.

`u ≤ 1 − q x = 1 − 0.5 × 0.4 = 0.8`. Price: `0.40 × (1 − 0.4 × 0.7) = $0.288`. Compute falls to `0.1067 × 0.288 / 0.40 = 0.0768`, a drop of $0.030, which is `0.030 / 2.085 = 1.4%` of the bill. The saving is capped by compute's 5.1% share. Put spot under stateless processes first.
</details>

61. *Week 1 and 13 · compute.* A world event keeps one zone at `h = 0.25` (capacity 531) for an evening, and its clients hit a shaper cap of 9,000 B/s at $0.08 per GB. What does a crowded player-hour cost, and which term grew most against the $2.085 baseline?

<details>
<summary>Answer and worked solution</summary>

**Answer:** $3.030 per 1,000 player-hours. The network term grew most, from $1.728 to $2.592.

Compute: `1000 × 0.40 / (8 × 530.9 × 0.5) = 0.188`. Network: `9,000 × 3,600 / 10⁹ × 0.08 × 1,000 = 2.592`. Services 0.250. Total 3.030. Compute rose by $0.081 and network by $0.864. The crowd's CPU cost barely shows on the bill, and its bytes dominate it. Without the shaper, the network term would have no ceiling.
</details>

## Week 14: Case study presentations

Lecture: [w14-case-study-presentations.md](../lectures/w14-case-study-presentations.md). `c_i ≤ β / (f_t × d × n (n − 1) × g)`. Reference costs from Norvig: 1 ns per instruction, 25 ns mutex lock and unlock, 100 ns main-memory fetch.

62. *Week 14 · code.* What does this print? Which assumption would you research first, and why?

```python
def implied_pair_ns(n, tick_hz, speed=1.0, usable=1.0, pair_share=1.0):
    budget_s = usable / (tick_hz * speed)
    return 1e9 * budget_s / (n * (n - 1) * pair_share)

base = implied_pair_ns(2000, 10)
for label, kw in [("half speed", dict(speed=0.5)), ("keep 40% free", dict(usable=0.6)),
                  ("a fifth of pairs", dict(pair_share=0.2))]:
    print(f"{label:17s} {implied_pair_ns(2000, 10, **kw) / base:4.2f}x")
print(round(base, 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**
```
half speed        2.00x
keep 40% free     0.60x
a fifth of pairs  5.00x
25.0
```

The base bound is `10⁸ / (2,000 × 1,999) = 25` ns per pair, one mutex lock and unlock, far too tight for an all-pairs design. The pair share moves the bound most (5 times for a plausible range), then game speed. Keeping budget free only tightens it. Research the pair share first. How many of the 2,000 players could actually interact at once?
</details>

63. *Week 14 · compute.* A battle royale runs 60 players per match at 30 Hz and the studio says it fits 5 matches per core. What is the most CPU time per player per tick? The first build took 40 ms per match frame. What speed-up did the headline require?

<details>
<summary>Answer and worked solution</summary>

**Answer:** At most 111 µs per player per tick. The headline required a 6× speed-up.

A frame at 30 Hz lasts 33.3 ms. Five matches share it, so each match frame gets 6.67 ms. Divided by 60 players, 111 µs each. With 60 players, the per-player term is the right one to invert, because the pair count (3,540 ordered pairs) is small enough that per-player work usually dominates. `40 / 6.67 = 6`.
</details>

64. *Week 14 · compute.* By what factor did the implied pair cost bound shrink from B-R5RB (2,670 pilots) to FWST-8 (6,557), both at 1 Hz and 10% speed? If the FWST-8 node spread its pair work across 8 cores, what would the bound become, and where does it sit on the reference ladder?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It shrank 6.03 times. With 8 cores the bound is about 1,861 ns, above a main-memory fetch.

The bound is inversely proportional to `n (n − 1)`, so the ratio is `(6,557 × 6,556) / (2,670 × 2,669) = 6.03`. From 232.6 ns, 8 cores give `8 × 232.6 = 1,861` ns, about 1.9 µs, room for many memory fetches per pair. The core count is a hypothesis to test against the developer's sources, not a fact.
</details>

65. *Week 14 · critique.* A pitch deck says "our 20 Hz servers will host 10,000 players in one fight, all at full speed". Compute the implied pair cost with `β = 1` and `g = 1`. Then rewrite this student slide line so it is correct: "EVE's server spent 233 ns per pair at FWST-8."

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.5 ns per pair, half of one instruction, so the claim needs `g` far below 1 or a different architecture. The slide should say "At FWST-8, EVE's node could not have spent more than 233 ns per pair per tick, unless not every pair interacted, the work was spread over several cores, or the server fell behind (model, this talk)."

`5×10⁷ ns / (10,000 × 9,999) = 0.50` ns. No server checks a pair in half an instruction, so the pitch must be relying on pairs that do not interact, which it should state. The original slide presents an upper bound as a measurement and hides the assumptions.
</details>
