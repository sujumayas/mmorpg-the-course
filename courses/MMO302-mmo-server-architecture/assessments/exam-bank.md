# MMO302 · Exam bank: quiz, practice and viva questions

MMO302 has no written exam. The grade comes from the labs (40%, see [labs-brief.md](labs-brief.md)), the week 15 load test (20%, see [load-test-brief.md](load-test-brief.md)) and the final world server (40%, see [final-server-brief.md](final-server-brief.md)). This bank has three jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab goes quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute or code question and one explain or critique question.
- **Viva.** The final server viva and the load-test debrief ask questions in this style, rewritten with the numbers from your own server, your own bots and your own measurements.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model (deliveries, handoffs, tick cost, commits, queue waits, fan-out, p99, dilation, headroom, stall rates) to values you have not seen before.
- **code**: say what a piece of Python prints and why.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or a setting for a stated situation and justify it with a number.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Game facts come from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`) and prints exactly what the answer says, and every number was recomputed in Python from the lectures' own models. Write your own answer before you open the solution.

---

## Week 1: Scale targets, CCU, messages per second, the n-squared problem

Lecture: [week 1](../lectures/w01-scale-targets-ccu-messages-and-n-squared.md).

1. *Week 1 · compute.* A game has 120,000 daily active users who play 2.5 hours a day, and the evening peak factor is 1.7. Find the average CCU and the PCU. Then use the lecture's section 3 planning chain (0.062 ms per player per tick at normal density, 2 ms fixed, 100 ms tick) at 50% target utilization to find how many servers you need, with one spare.

<details>
<summary>Answer and worked solution</summary>

**Answer:** average CCU 12,500, PCU 21,250, 29 servers (28 plus one spare).

Average CCU is `120,000 × 2.5 / 24 = 12,500`. PCU is `1.7 × 12,500 = 21,250`. Players per server at 50% are `(0.5 × 100 − 2) / 0.062 = 774`. Servers are `ceil(21,250 / 774) = ceil(27.45) = 28`, plus one spare for a failure, so 29.

Notice that PCU, not DAU or registered accounts, drives the count. Planning for all 120,000 daily users at once would buy almost six times too many machines.
</details>

2. *Week 1 · compute.* A world of 3,900 players has one crowded zone of 300 (a world boss) and 180 ordinary zones of 20. Each player sends `u = 4` updates per second. Compute the world's deliveries per second with `D = u × Σ g(g − 1)`, and the share of them that come from the boss zone.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 632,400 deliveries per second, 56.7% of them from the boss zone.

Boss zone: `300 × 299 = 89,700`. Ordinary zones: `180 × 20 × 19 = 68,400`. Sum `158,100`, times `u = 4` gives 632,400. The boss zone holds 7.7% of the players (`300 / 3,900`) and produces `358,800 / 632,400 = 56.7%` of the work. That gap between share of players and share of load is the n-squared problem in one line.
</details>

3. *Week 1 · code.* What does this print? Explain why the last value on the second line differs from the first.

```python
import math

def deliveries(groups, u):
    return u * sum(g * (g - 1) for g in groups)

def c_max_estimate(budget, u):
    return math.floor(math.sqrt(budget / u))

def c_max_exact(budget, u):
    c = math.floor((1 + math.sqrt(1 + 4 * budget / u)) / 2)
    while u * (c + 1) * c <= budget:
        c += 1
    while u * c * (c - 1) > budget:
        c -= 1
    return c

print(deliveries([354], 8), deliveries([355], 8))
print(c_max_estimate(1_000_000, 8), c_max_exact(1_000_000, 8))
print(deliveries([50] * 20, 8), deliveries([1000], 8) // deliveries([50] * 20, 8))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
999696 1005360
353 354
392000 20
```

A crowd of 354 at `u = 8` needs `8 × 354 × 353 = 999,696` deliveries per second, just under the 1,000,000 budget. A crowd of 355 needs 1,005,360, just over. So the largest crowd is 354. The estimate `√(B / u) = √125,000 = 353.6` rounds down to 353, because it replaces `c − 1` with `c`. The exact root of `c² − c − B/u = 0` is about `√(B/u) + 0.5`, so the estimate can be one short. That is why lab 01 asks for a correction step after the closed form.

The last line compares 1,000 players in one crowd with the same 1,000 split into 20 groups of 50. The crowd costs 20 times as much, which is `999 / 49 ≈ 20.4` rounded down by the integer division.
</details>

4. *Week 1 · compute.* Use the lecture's tick model (2 ms fixed, 0.05 ms per player, 0.001 ms per delivery, 10 Hz, `u = 5`). A server hosts 19 zones of 25 players and one zone where a crowd of 300 gathers. What is its tick time? What is the largest crowd this server can host inside a 100 ms tick?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 91.3 ms. The largest crowd that fits is 324.

Players `= 300 + 19 × 25 = 775`. Deliveries per second `= 5 × (300 × 299 + 19 × 25 × 24) = 5 × (89,700 + 11,400) = 505,500`, so 50,550 per tick. Tick time `= 2 + 0.05 × 775 + 0.001 × 50,550 = 2 + 38.75 + 50.55 = 91.3` ms.

For a crowd `c`, tick time is `2 + 0.05 × (c + 475) + 0.0005 × (c(c − 1) + 11,400)`. At `c = 324` it is 99.98 ms and at `c = 325` it is 100.35 ms. The lecture's server 0 broke at 327 because its other zones held slightly fewer players (the other 19 zones shared the rest of the world's population, not a flat 25 each).
</details>

5. *Week 1 · critique.* A pitch deck says "Our servers handle 10,000 players per realm, and if we need more we will buy servers twice as fast." Name the assumption hidden in the first half and put a number on the second half using `c_max ≈ √(B / u)`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The first half assumes players stay spread out in small groups. The second half buys only 41% more crowd.

"10,000 per realm" says nothing about `g`. The same 10,000 cost `u × 10,000 × 24` deliveries per second in groups of 25 and `u × 10,000 × 9,999` in one crowd, a factor of about 417. Ask the team for the densest moment the design invites (a capital, a world boss, a siege) and its `g`.

Doubling `B` raises the crowd ceiling by `√2 ≈ 1.41`. At `u = 5` and `B = 1,000,000` the ceiling goes from 447 to 632. Only cutting `u` (fewer updates, time dilation) or `g` (interest management, layers) changes the square.
</details>

## Week 2: Shards, realms, zones, instances, layers

Lecture: [week 2](../lectures/w02-shards-realms-zones-instances-layers.md).

6. *Week 2 · compute.* A starting zone holds `Z = 2,400` players. 10% are on the same kill quest, which needs `k = 10` kills. There are `S = 20` spawn points with a `R = 45` s respawn, and a player kills `q = 2` per minute uncontested. Find the kill supply per layer, the layers needed, and the quest time and players-you-can-meet at `L = 6` and at the layers needed.

<details>
<summary>Answer and worked solution</summary>

**Answer:** supply 26.7 kills per minute per layer, 18 layers. At `L = 6`, 15 minutes and 399 others. At `L = 18`, 5 minutes and about 132 others.

Supply `= 20 × 60 / 45 = 26.67`. Demand `= 0.10 × 2,400 × 2 = 480`. Layers needed `= ceil(480 / 26.67) = 18`.

At `L = 6`, each layer has 400 players and 40 questers who share 26.67 kills a minute, 0.667 each, so 10 kills take 15 minutes. Each player can meet `400 − 1 = 399` others. At `L = 18`, 13.3 questers share the supply, so each kills at the uncontested 2 per minute, 5 minutes, and each layer holds 133.3 players, about 132 others to meet. Adding a 19th layer would cut the meetable crowd again and save no quest time.
</details>

7. *Week 2 · compute.* A zone runs 16 layers with no party-joining. What is the chance that one ungrouped friend lands on your layer? That a group of four friends who log in separately all land together? What changes with party-joining?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 6.25% for one friend, 0.024% (1 in 4,096) for the group of four, and 100% for anyone who groups.

Each friend matches you with probability `1 / 16`. The other three friends must each match the first, independently, so `(1/16)^3 = 1 / 4,096`. Party-joining moves the whole group to the leader's layer, so the social cost of layering falls on strangers only.
</details>

8. *Week 2 · compute.* In the lecture's launch model (`Z(1) = 3,000`, `ceil(Z / 150)` layers needed), suppose the zone's population halves every 3 days instead of every 2. How many layers are needed on day 7? If the 20 day-1 layers are kept until restart, how many players does each layer hold on day 7?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 5 layers needed. 37.5 players per layer under the "keep" policy.

`Z(7) = 3,000 × 0.5^((7 − 1) / 3) = 3,000 × 0.25 = 750`. Layers needed `= ceil(750 / 150) = 5`. Kept at 20 layers, `750 / 20 = 37.5` per layer. A slower exodus buys a few days before the ghost-town problem, but the same decision (retire on demand and disturb players, or keep and empty the world) still arrives.
</details>

9. *Week 2 · design.* For the zone in question 6, a designer proposes halving the respawn time to 22.5 s instead of running 18 layers. Compute the new layers needed and quest time, and name what the change costs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9 layers, quest time 5 minutes. The cost is a less scarce world and more drops entering the economy.

Supply per layer `= 20 × 60 / 22.5 = 53.3` kills per minute. Layers needed `= ceil(480 / 53.3) = 9`. At `L = 9`, 26.7 questers share 53.3 kills, 2 each, the uncontested rate, so 10 kills take 5 minutes. Each layer now holds 267 players instead of 133, so the community is twice as large. The price is that monsters (and their loot) arrive twice as often, which inflates any economy built on those drops (MMO304).
</details>

## Week 3: Area of interest, grids, radius, hysteresis

Lecture: [week 3](../lectures/w03-area-of-interest-grids-radius-hysteresis.md).

10. *Week 3 · compute.* 4,000 players stand uniformly in a 2,000 m square world. The view radius is `r = 40` m and cells are `c = 40` m with a 3 × 3 block. Estimate deliveries per tick under broadcast, grid and radius, ignoring edges. How many times cheaper is the grid than broadcast?

<details>
<summary>Answer and worked solution</summary>

**Answer:** broadcast 15,996,000, grid 57,600, radius about 20,106. The grid is about 278 times cheaper.

`ρ = 4,000 / 2,000² = 0.001` per m². Grid `≈ N × ρ × 9c² = 4,000 × 0.001 × 14,400 = 57,600`. Radius `≈ N × ρ × π r² = 4,000 × 0.001 × 5,027 ≈ 20,106`. Broadcast `= 4,000 × 3,999 = 15,996,000`. The ratio `15,996,000 / 57,600 ≈ 278` is large because the world is big for its population. Pack the same 4,000 into a disc 40 m across, so everyone is within `r` of everyone, and all three counts become 15,996,000 again.
</details>

11. *Week 3 · code.* What does this print? Which pairs does the grid send that the radius test drops?

```python
import math
from collections import defaultdict

pts = {"A": (1, 1), "B": (9, 9), "C": (12, 2), "D": (25, 5), "E": (31, 31)}
c = r = 10

grid = defaultdict(list)
for name, (x, y) in pts.items():
    grid[(math.floor(x / c), math.floor(y / c))].append(name)

grid_count = radius_count = 0
for name, (x, y) in pts.items():
    cx, cy = math.floor(x / c), math.floor(y / c)
    block = [o for i in (-1, 0, 1) for j in (-1, 0, 1) for o in grid[(cx + i, cy + j)] if o != name]
    near = [o for o in block if math.dist(pts[o], (x, y)) <= r]
    grid_count += len(block)
    radius_count += len(near)
    print(name, sorted(block), sorted(near))
print("grid", grid_count, "radius", radius_count)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
A ['B', 'C'] []
B ['A', 'C'] ['C']
C ['A', 'B', 'D'] ['B']
D ['C'] []
E [] []
grid 8 radius 2
```

A and B share cell (0, 0), C is in (1, 0), D in (2, 0) and E alone in (3, 3). The grid's broad phase finds 8 ordered pairs. Only B and C are within 10 m of each other (`√(9 + 49) ≈ 7.6` m). The grid over-sends A–B (11.3 m), A–C (11.0 m) and C–D (13.3 m) in both directions, which the narrow phase removes. The grid never misses a pair within `r`, because `c ≥ r`, and E, far from everyone, costs nothing.
</details>

12. *Week 3 · compute.* An observer watches a player pace at the view edge for one minute at 10 Hz. Without hysteresis the server sends 20 enters, 19 leaves and 280 visible-tick updates. With `r_out` wide enough it sends 1 enter, 0 leaves and 600 updates. Updates cost 16 bytes and leaves 4 bytes. At what enter size do the two policies cost the same? Which uses fewer bytes with a 120-byte enter and with a 400-byte enter?

<details>
<summary>Answer and worked solution</summary>

**Answer:** break-even at about 265 bytes. At 120 B the flickering policy is cheaper (6,956 against 9,720 bytes). At 400 B hysteresis is cheaper (10,000 against 12,556 bytes).

Solve `20s + 4 × 19 + 16 × 280 = s + 16 × 600`, so `19s = 9,600 − 76 − 4,480 = 5,044` and `s ≈ 265.5` bytes. At 120 B, `2,400 + 76 + 4,480 = 6,956` against `120 + 9,600 = 9,720`. At 400 B, `8,000 + 76 + 4,480 = 12,556` against `400 + 9,600 = 10,000`. Most games choose hysteresis either way, because 19 visible blinks a minute is worse than a few kilobytes.
</details>

13. *Week 3 · design.* A game rebuilds observer sets on a timer. Its fastest mount moves at 24 m/s, and designers accept that a newcomer may appear up to 6 m inside the view radius. What rebuild interval does that allow? The enter radius is 60 m and entities at the edge jitter by up to 4 m. What is the smallest `r_out` that stops flicker, and what would you ship?

<details>
<summary>Answer and worked solution</summary>

**Answer:** rebuild at least every 0.25 s. `r_out` must be above 64 m. Ship something like 66 to 68 m.

Distance covered between rebuilds is `speed × interval`, so `24 × interval ≤ 6` gives `interval ≤ 0.25` s, four rebuilds a second. For hysteresis, the margin `r_out − r_in` must exceed the jitter, so `r_out > 60 + 4 = 64` m. A little extra covers players who jitter more than the measured 4 m, at the cost of a few more update messages per departing player.
</details>

14. *Week 3 · explain.* A student sets `c = r / 2` with `r = 50` m (so `c = 25` m) but keeps the 3 × 3 block. Give two positions that are within 50 m of each other but that the grid never pairs, and state the rule that would have prevented it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** for example, A at (24, 1) and B at (60, 1). They are 36 m apart, but A is in cell (0, 0) and B in cell (2, 0), outside A's block. The rule is `k × c ≥ r` for a `(2k + 1) × (2k + 1)` block.

A's 3 × 3 block spans cells 0 to 1 on each side of column 0, so x from −25 to 50 m. B at x = 60 falls outside. With `c = 25` you need `k = 2` (a 5 × 5 block) to guarantee `k × c = 50 ≥ r`. Unlike over-sending, which only wastes scans, this is a correctness bug. B moves in plain sight and A never hears about it.
</details>

## Week 4: Zone servers and handoff

Lecture: [week 4](../lectures/w04-zone-servers-and-handoff.md).

15. *Week 4 · compute.* A shard of 6,000 players lives in a 12 km square world on a 4 × 4 zone grid. Players average 1.5 m/s and the AOI radius is 120 m. Compute the border length, handoffs per second and ghost fraction. What happens to `H` if the designers double the world's side and keep everything else?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `L = 72,000` m, `H ≈ 2.86` handoffs per second, `G = 12%`. Doubling `W` halves `H` to about 1.43.

`L = 2 × 12,000 × 3 = 72,000`. `ρ = 6,000 / 1.44 × 10⁸ = 4.17 × 10⁻⁵`. `H = (2/π) × 4.17 × 10⁻⁵ × 1.5 × 72,000 ≈ 2.86`. `G = 2 × 120 × 72,000 / 1.44 × 10⁸ = 0.12`.

With `W = 24` km, `L = 144,000` m and `ρ = 1.04 × 10⁻⁵`, so `H = 0.6366 × 1.04 × 10⁻⁵ × 1.5 × 144,000 ≈ 1.43`. Substituting `ρ = N / W²` and `L = 2W(g − 1)` shows why: `H = (4/π) × N × v × (g − 1) / W`. The border doubles but the density falls to a quarter. A student who answers "a quarter" has scaled `ρ` and forgotten that `L` grows too.
</details>

16. *Week 4 · compute.* A 4,000-player shard puts 35% of its players in one capital city that fits inside a single zone. What is the busiest zone on a 4 × 4 grid and on an 8 × 8 grid? What is the largest city share that keeps every zone of an 8 × 8 grid under 900 players?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1,562.5 on 4 × 4, about 1,441 on 8 × 8. The city may hold at most about 21.3% of the shard.

Busiest zone `= f × N + (1 − f) × N / g²`. At `g = 4`, `1,400 + 2,600 / 16 = 1,562.5`. At `g = 8`, `1,400 + 2,600 / 64 = 1,440.6`. Four times the servers took 122 players off the busiest zone.

For 8 × 8, `4,000 f + (1 − f) × 62.5 < 900` gives `f < (900 − 62.5) / (4,000 − 62.5) = 0.213`. The fix for a bigger city is not more zones. It is a bigger node for that zone, layers, or more banks and auction houses to spread the crowd.
</details>

17. *Week 4 · compute.* A capital holds 1,500 players in a disc of radius 250 m, walking at 0.8 m/s. A straight border is drawn through its centre (500 m long). With `R = 80` m, how many handoffs per second does that one border cause, and roughly how many players must be ghosted across it? If a dynamic partition moves that border 30 m in one step, how many players change owner at once?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 1.95 handoffs per second, about 611 ghosts, and about 115 players handed off in one step.

City density `= 1,500 / (π × 250²) = 0.00764` per m². `H = (2/π) × 0.00764 × 0.8 × 500 ≈ 1.95`. Ghosts are players within 80 m of the line, `0.00764 × (160 × 500) ≈ 611`, 41% of the city. A 30 m move sweeps `30 × 500 = 15,000` m², which holds `0.00764 × 15,000 ≈ 115` players, all handed off in the same tick. A border is cheap where nobody stands and expensive where everyone does.
</details>

18. *Week 4 · code.* This is a stripped-down version of the lab 04 protocol. What does it print, and what would go wrong if you deleted the `if seq <= ...` check?

```python
class ZoneServer:
    def __init__(self, name):
        self.name, self.owned, self.last_seq = name, set(), {}

    def on_handoff(self, pid, seq):
        if seq <= self.last_seq.get(pid, 0):
            return f"{self.name}: reject {pid} seq {seq}"
        self.last_seq[pid] = seq
        self.owned.add(pid)
        return f"{self.name}: owns {pid} seq {seq}"

    def hand_to(self, other_name, pid, seq):
        self.last_seq[pid] = seq
        self.owned.discard(pid)
        return ("HANDOFF", other_name, pid, seq)

a, b = ZoneServer("A"), ZoneServer("B")
a.owned.add("p")
m5 = a.hand_to("B", "p", 5)          # A offers p to B
print(b.on_handoff("p", 5))
m6 = b.hand_to("A", "p", 6)          # p walks straight back
print(a.on_handoff("p", 6))
print(b.on_handoff("p", 5))          # a retransmitted copy of m5 arrives late
print(sorted(s.name for s in (a, b) if "p" in s.owned))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
B: owns p seq 5
A: owns p seq 6
B: reject p seq 5
['A']
```

B accepts seq 5, then hands p back with seq 6 and records 6 as the last sequence it saw. When the retransmitted copy of seq 5 arrives, `5 <= 6`, so B rejects it and p has exactly one owner, A. Without the check, B would add p again and the last line would print `['A', 'B']`, a duplicated character that both servers simulate and both may save.
</details>

## Week 5: Tick rate for MMOs vs shooters

Lecture: [week 5](../lectures/w05-tick-rate-for-mmos-vs-shooters.md).

19. *Week 5 · compute.* A zone has `n = 2,500` entities with `k = 40` neighbours on average. On this hardware `a = 2` ms, `d = 4` µs and `e = 0.25` µs. Find the tick cost, the utilization at 10 Hz and `T_max` for `u_max = 0.6`. Then 600 of the entities gather in a siege with `k = 300` (the rest keep 40). Recompute, and pick a tick rate for the siege.

<details>
<summary>Answer and worked solution</summary>

**Answer:** normal `c = 37` ms, `u = 37%`, `T_max ≈ 16.2` Hz. Siege `c = 76` ms, 76% at 10 Hz, `T_max ≈ 7.9` Hz. Drop to 5 Hz (38%) for the siege, or shed load another way.

Normal: `2 + 0.004 × 2,500 + 0.00025 × 2,500 × 40 = 2 + 10 + 25 = 37`. `u = 37 × 10 / 1,000 = 0.37`. `T_max = 600 / 37 = 16.2`.

Siege: neighbour work `= 600 × 300 + 1,900 × 40 = 256,000`, times 0.00025 is 64 ms, so `c = 2 + 10 + 64 = 76`. At 10 Hz, 76% is over the 60% target. `T_max = 600 / 76 = 7.9`, so a 5 Hz siege rate fits at 38%, at the price of an average input wait of 100 ms instead of 50.
</details>

20. *Week 5 · compute.* Ability timers are 0.8, 1.2 and 2.0 s. For tick rates of 2.5, 3 and 4 Hz, how long does each timer really last? At which rate is no timer rounded up? At that rate, what is the chance two actions 150 ms apart land in the same tick?

<details>
<summary>Answer and worked solution</summary>

**Answer:** only 2.5 Hz keeps all three exact. Same-tick chance 62.5%.

A timer lasts `ceil(τ × T) / T`. At 2.5 Hz: 2, 3 and 5 ticks, so 0.8, 1.2 and 2.0 s exactly. At 3 Hz: `0.8 × 3 = 2.4` rounds to 3 ticks (1.0 s), `1.2 × 3 = 3.6` rounds to 4 (1.33 s), 2.0 stays. At 4 Hz: `3.2` rounds to 4 (1.0 s), `4.8` to 5 (1.25 s). A faster tick is not automatically more accurate. What matters is that durations are whole multiples of the tick.

At 2.5 Hz, `P = 1 − 0.15 × 2.5 = 0.625`.
</details>

21. *Week 5 · compute.* Take the lecture's zone (`n = 3,000`, `k = 50`, `a = 1` ms, `d = 5` µs, `e = 0.2` µs, so `c = 46` ms) but run it at 20 Hz. Of its 2,000 NPCs, 1,200 have no player within AOI. What is the CPU per second at a single rate, and with the 1,200 idle NPCs moved to 1 Hz? What share of a core do you save?

<details>
<summary>Answer and worked solution</summary>

**Answer:** single rate 920 ms per second. Multi-rate 578 ms per second, a 37% saving.

Single: `20 × 46 = 920` ms, 92% of a core. Active entities are `3,000 − 1,200 = 1,800`, so `c_active = 1 + 0.005 × 1,800 + 0.0002 × 1,800 × 50 = 1 + 9 + 18 = 28` ms, and `20 × 28 = 560`. Idle work once a second `= 0.005 × 1,200 + 0.0002 × 1,200 × 50 = 6 + 12 = 18` ms. Total 578 ms. The zone goes from nearly full to about 58% busy for a change no player can see, as long as an NPC that wakes up computes its state from elapsed time.
</details>

22. *Week 5 · code.* What does this print? What would a player notice during the ticks marked late?

```python
def stretch(costs, interval):
    """Each tick starts at its due time or when the previous tick ends, whichever is later."""
    end, late = 0, []
    for i, c in enumerate(costs):
        start = max(i * interval, end)
        late.append(start - i * interval)
        end = start + c
    return late, end

late, end = stretch([60, 130, 130, 60, 60, 60], 100)
print(late, end)
late, end = stretch([60, 130, 130, 60, 60, 60], 200)
print(late, end)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[0, 0, 30, 60, 20, 0] 560
[0, 0, 0, 0, 0, 0] 1060
```

At 10 Hz (100 ms), tick 1 runs from 100 to 230, so tick 2 starts 30 ms late and ends at 360. Tick 3 starts at 360, 60 ms late, and ends at 420. Tick 4 starts at 420, 20 ms late. Tick 5 is back on time. Under "stretch", game time runs slow for those ticks, so everyone in the zone sees movement slow down briefly and then recover. At 5 Hz (200 ms) every tick fits, and the cost moves to the player as a longer average wait, 100 ms instead of 50.
</details>

## Week 6: Simulation authority and anti-cheat by design

Lecture: [week 6](../lectures/w06-simulation-authority-and-anti-cheat-by-design.md).

23. *Week 6 · compute.* A game uses `v = 6` m/s and sends positions every `Δ = 0.05` s with a tolerance `s = 0.2` s. For a per-packet check, a 3-second sliding window and a token bucket, give the sustained speed factor and the blink after standing still.

<details>
<summary>Answer and worked solution</summary>

**Answer:** per-packet 5× and 1.5 m. Window 1.067× and 19.2 m. Bucket 1× and 1.5 m.

Per-packet factor `(Δ + s) / Δ = 0.25 / 0.05 = 5`, blink `6 × 0.25 = 1.5` m. Window factor `(W + s) / W = 3.2 / 3 = 1.067`, blink `6 × 3.2 = 19.2` m. Bucket factor 1, blink `v × (Δ + s) = 1.5` m. The per-packet check turns a quarter-second tolerance into a permanent five-times speed hack, and the faster send rate made it worse, because `Δ` sits in the denominator.
</details>

24. *Week 6 · compute.* Honest players stall twice a minute, each stall lasting between 0.1 and 0.9 s, spread evenly. A stall longer than `s` causes a correction. What tolerance keeps corrections at or below 24 per hour? What blink does the token bucket then allow at `v = 7`, `Δ = 0.1`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `s ≥ 0.74` s, and the blink is 5.88 m.

Corrections per hour `= 120 × (0.9 − s) / 0.8`, because 120 stalls an hour happen and a share `(0.9 − s) / 0.8` of them are longer than `s`. Setting that `≤ 24` gives `0.9 − s ≤ 0.16`, so `s ≥ 0.74`. The bucket's capacity is `7 × (0.1 + 0.74) = 5.88` m. With the right check shape, a generous tolerance costs a blink of a few metres, never a speed multiplier.
</details>

25. *Week 6 · code.* This token bucket works in integer millimetres and milliseconds so it never compares floats. What does it print? Why does the rejected packet at 400 ms not lose the player any credit?

```python
V = 7                 # mm per ms (7 m/s)
CAP = V * (100 + 250) # capacity for a 100 ms send interval and 250 ms tolerance, in mm

class Bucket:
    def __init__(self):
        self.credit, self.last = CAP, 0

    def check(self, t, d):
        credit = min(CAP, self.credit + V * (t - self.last))
        if d > credit:
            return False            # rejected: state unchanged
        self.credit, self.last = credit - d, t
        return True

b = Bucket()
packets = [(100, 700), (200, 2000), (300, 1000), (400, 1000), (1400, 2450), (1500, 800)]
print([b.check(t, d) for t, d in packets])
print(b.credit)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[True, True, True, False, True, False]
0
```

`CAP = 2,450` mm. At 100 ms the bucket is full, the 700 mm move passes and leaves 1,750. At 200 ms credit refills to 2,450, the 2,000 mm burst passes, leaving 450. At 300 ms credit is 1,150, the 1,000 mm move passes, leaving 150. At 400 ms credit would be 850, so 1,000 mm is rejected and nothing is stored. At 1,400 ms the refill is computed from 300 ms, not 400, so credit caps at 2,450 and the 2,450 mm move passes, leaving 0. At 1,500 ms only 700 has refilled and 800 mm is rejected.

Because a rejected move stores nothing, the refill that would have happened by 400 ms is still counted at the next accepted packet. The player loses the rejected move, not any credit.
</details>

26. *Week 6 · compute.* A zone of 5,000 players sends 20 position updates per second each. A token bucket costs 0.2 µs per update and a wall ray cast 3 µs. Server-authoritative movement costs 8 µs per update. What CPU per second does each design use, and what share of a core separates them?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 320 ms per second for the bucket plus ray cast, 800 ms for server authority. The difference is 480 ms, 48% of a core.

`5,000 × 20 = 100,000` updates per second. `100,000 × 3.2 µs = 320` ms. `100,000 × 8 µs = 800` ms. At this update rate full authority would take 80% of one core for movement alone, which is why many MMOs keep movement as a bounded claim and spend authority on loot, inventory and trade.
</details>

27. *Week 6 · critique.* A prototype client sends `USE_ITEM(slot, target)`, `PICKUP(item_id, x, y)`, `REPORT_KILL(npc_id, loot_list)` and `EQUIP(slot, item_id, stats)`. Mark each as intent or claim, and rewrite every claim as an intent.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- `USE_ITEM(slot, target)` is an intent. The server checks the slot holds a usable item and the target is legal.
- `PICKUP(item_id, x, y)` contains a claim, the position. Send `PICKUP(item_id)` and let the server check the player's server-side position against the item's.
- `REPORT_KILL(npc_id, loot_list)` is two claims. The server decides whether the NPC died and rolls the loot. The client sends nothing, or at most `LOOT(corpse_id)`.
- `EQUIP(slot, item_id, stats)` claims the stats. Send `EQUIP(slot, item_id)`. The server reads the item's stats from its own database row.

Each rewrite shrinks the trust boundary to what a perfect legal player could do. A forged `REPORT_KILL` with an invented loot list would otherwise mint items, which week 8's audit would see as drift.
</details>

## Week 7: Persistence strategies

Lecture: [week 7](../lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md).

28. *Week 7 · compute.* Fill in the lecture's five-strategy table for a shard with `N = 2,000`, `c = 0.8`, `S = 30` kB, `s = 100` B, `h = 4`, `T_world = 600` s, `W = 300` MB, `R = 150` MB/s, `T = 120` s, `F = 15` s, `g = 5` ms, `K = 900` s, `r = 150,000`. Then cross out any strategy that breaks a budget of 400 commits per second or freezes the shard for more than one second.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Strategy | Commits/s | kB/s | Avg loss (s) | Freeze (s) | Replay (s) |
|---|---|---|---|---|---|
| Stop-the-world | 0.002 | 500 | 300 | 2.0 | 0 |
| Periodic | 16.7 | 500 | 60 | 0 | 0 |
| Write-through | 1,600 | 160 | 0 | 0 | 0 |
| Write-behind | 133.3 | 53.3 | 7.5 | 0 | 0 |
| Event log | 200 | 160 | 0 | 0 | 4.8 |

Changes per second `= 2,000 × 0.8 = 1,600`. Write-behind: each player makes `0.8 × 15 = 12` changes per window but touches at most 4 rows, so `(2,000 / 15) × 4 × 100 = 53,333` B/s. Event log: `min(1 / 0.005, 1,600) = 200` commits, replay `1,600 × 900 / 2 / 150,000 = 4.8` s.

Write-through (1,600 commits) and stop-the-world (a 2-second freeze, 40 ticks at 20 Hz) are out. Periodic, write-behind and the event log remain, and a good policy mixes them by kind of state.
</details>

29. *Week 7 · compute.* A shard of 8,000 players makes 0.6 persistent changes per player per second, and recovery replays 300,000 events per second. The average restart after a crash must stay at or under 4 seconds. What is the longest snapshot interval `K`? What is the worst-case replay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `K ≤ 500` s. Worst case 8 s.

Events per second `= 8,000 × 0.6 = 4,800`. Average replay `= 4,800 × K / 2 / 300,000 ≤ 4` gives `K ≤ 4 × 2 × 300,000 / 4,800 = 500`. A crash just before a snapshot replays the full interval, `4,800 × 500 / 300,000 = 8` s, twice the average. If the target is a worst case, halve `K`.
</details>

30. *Week 7 · code.* A GM issued a refund, and the event was written with a new kind. What does this print, and what is the bug?

```python
import copy

def apply(state, event):
    kind, who, amount = event
    char = state.setdefault(who, {"gold": 0, "xp": 0})
    if kind == "loot_gold":
        char["gold"] += amount
    elif kind == "buy":
        char["gold"] -= amount
    elif kind == "kill_xp":
        char["xp"] += amount
    return state

log = [
    ("loot_gold", "cato", 200), ("buy", "cato", 50), ("kill_xp", "dara", 90),
    ("gm_refund", "cato", 500), ("loot_gold", "dara", 40), ("buy", "dara", 15),
]

snapshot, seq = {}, 3
for e in log[:seq]:
    apply(snapshot, e)
restored = copy.deepcopy(snapshot)
for e in log[seq:]:
    apply(restored, e)
print(snapshot)
print(restored)
print("replayed", len(log) - seq)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
{'cato': {'gold': 150, 'xp': 0}, 'dara': {'gold': 0, 'xp': 90}}
{'cato': {'gold': 150, 'xp': 0}, 'dara': {'gold': 25, 'xp': 90}}
replayed 3
```

The snapshot after three events is correct. The replay of the tail applies three events, but `apply` has no branch for `gm_refund`, so it silently does nothing and Cato ends with 150 gold instead of 650. Recovery "succeeds" and quietly loses 500 gold. The fix is to make `apply` raise on an unknown kind, so a replay with a newer event than the code understands fails loudly, and to version events with an upcaster, as section 3 of the lecture describes.
</details>

31. *Week 7 · compute.* An event log uses a 10 ms group-commit window. A quiet shard writes only 50 events per second. How many commits per second does it actually make? Why is that below `1 / g`? What does it make at 5,000 events per second?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 39 commits per second at 50 events per second, and 100 at 5,000.

A window with no events commits nothing. With Poisson arrivals, the chance a 10 ms window holds at least one event is `1 − e^(−λg)`. At `λ = 50`, `λg = 0.5`, so commits `= 100 × (1 − e^(−0.5)) = 39.3`. At `λ = 5,000`, `λg = 50` and every window has events, so the log hits its ceiling of `1 / g = 100`. This is the lab 07 Part C correction, and it shows why the event log's commit count stays flat as the shard grows.
</details>

32. *Week 7 · compute.* A write-behind store holds 1,000 players with `F = 10` s. Each player makes 0.4 changes per second, each change picks one of 4 fields at random, and a row is 150 bytes. The lecture's formula with `h = 4` predicts bytes per second. Correct it for fields that are never touched in a window.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the formula says 60 kB/s. The corrected prediction is about 37.9 kB/s.

Formula: `(1,000 / 10) × min(0.4 × 10, 4) × 150 = 100 × 4 × 150 = 60,000` B/s. But 4 changes spread over 4 fields rarely hit all four. The number of changes to one field in a window is roughly Poisson with mean `4 / 4 = 1`, so a field is untouched with probability `e^(−1) = 0.368`. Expected distinct fields per flush `= 4 × (1 − 0.368) = 2.53`. Corrected: `100 × 2.53 × 150 ≈ 37,900` B/s. Coalescing saves more than the `min(c × F, h)` bound suggests when changes and fields are about equal in number.
</details>

## Week 8: Item ownership and transactional integrity

Lecture: [week 8](../lectures/w08-item-ownership-and-transactional-integrity.md).

33. *Week 8 · compute.* A shard does `M = 800,000` value-moving operations a day with `f = 1` in 4,000 and `a = 1` in 2,500. A quarter of retried operations draw from a one-time source (mail, reward, escrow), and the average value is 400 gold. For each of the four designs, give dupes, losses and double charges per day, and the daily drift in gold.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Design | Dupes | Losses | Double charges | Drift per day |
|---|---|---|---|---|
| 1. Give first | 280 | 0 | 240 | +112,000 |
| 2. Take first | 80 | 200 | 240 | −48,000 |
| 3. One transaction | 80 | 0 | 240 | +32,000 |
| 4. Transaction + idempotency | 0 | 0 | 0 | 0 |

Half-done `= 800,000 / 4,000 = 200`. Retried `= 800,000 / 2,500 = 320`, of which 80 hit one-time sources (dupes in designs 1 to 3) and 240 draw from players (double charges, supply unchanged). Design 1 drift `= (200 + 80) × 400 = 112,000`. Design 2 `= (80 − 200) × 400 = −48,000`, a net loss that still hides 80 dupes. Only design 4 removes both kinds.
</details>

34. *Week 8 · compute.* Three exploiters each dupe 5,000 gold every 20 seconds on a shard with 250 million gold. The audit runs every 15 minutes and alarms on any nonzero drift. What drift does the first audit see? How long would it take to reach 1% of the money supply if nobody looked?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 675,000 gold at the first audit. 1% of supply in about 56 minutes.

Each exploiter dupes `900 / 20 = 45` times in 15 minutes, so the first audit sees `3 × 45 × 5,000 = 675,000`. Per hour it is `3 × 180 × 5,000 = 2.7` million. 1% of 250 million is 2.5 million, reached after `2.5 / 2.7 × 60 ≈ 55.6` minutes. An exact 15-minute audit catches it at 0.27% of supply. An audit with a 1% tolerance would not alarm for almost an hour.
</details>

35. *Week 8 · critique.* A teammate copied the lecture's transfer but dropped the `try` around the two wallet updates. Their version is used for an overdraft. What does this print, and what is wrong with the function? Give the fix.

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
    CREATE TABLE wallet (player TEXT PRIMARY KEY, gold INTEGER NOT NULL CHECK (gold >= 0));
    CREATE TABLE applied_op (op_id TEXT PRIMARY KEY, result TEXT NOT NULL);
    INSERT INTO wallet VALUES ('ayla', 1000), ('bren', 0);
""")

def transfer(op_id, src, dst, amount):
    db.execute("BEGIN")
    try:
        db.execute("INSERT INTO applied_op VALUES (?, 'ok')", (op_id,))
    except sqlite3.IntegrityError:
        db.execute("ROLLBACK")
        return db.execute("SELECT result FROM applied_op WHERE op_id = ?", (op_id,)).fetchone()[0] + " (replayed)"
    db.execute("UPDATE wallet SET gold = gold - ? WHERE player = ?", (amount, src))
    db.execute("UPDATE wallet SET gold = gold + ? WHERE player = ?", (amount, dst))
    db.execute("COMMIT")
    return "ok"

print(transfer("t1", "ayla", "bren", 600))
try:
    print(transfer("t2", "ayla", "bren", 600))
except sqlite3.IntegrityError as e:
    print("error:", e)
print(db.in_transaction, dict(db.execute("SELECT player, gold FROM wallet")))
try:
    print(transfer("t3", "bren", "ayla", 100))
except sqlite3.OperationalError as e:
    print("error:", e)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
ok
error: CHECK constraint failed: gold >= 0
True {'ayla': 400, 'bren': 600}
error: cannot start a transaction within a transaction
```

The `CHECK` refuses the second debit, as intended, but the exception escapes between `BEGIN` and `COMMIT`. The transaction stays open, holding the `t2` row in `applied_op`, and the connection can no longer start the next transfer. On a real server the open transaction also holds locks until the connection is dropped. Worse, if anything later commits it, `t2` is recorded as applied, so a retry of `t2` returns "ok (replayed)" for a transfer that never moved gold.

The fix is to wrap the updates in `try`, and on `IntegrityError` roll back, then record the outcome under the operation ID in a fresh transaction (`INSERT INTO applied_op VALUES (?, 'insufficient')`), so a retry replays "insufficient". This is the lecture's version, and Lab 08 step 4 asks for exactly this.
</details>

36. *Week 8 · compute.* Since launch the ledger shows 900 million gold minted and 780 million destroyed, on top of a starting supply of 50 million. Wallets and banks hold 168 million. The team then adds mail and auction escrow to the sum, which hold 4 million. What drift does each count show, and what does the difference teach?

<details>
<summary>Answer and worked solution</summary>

**Answer:** −2 million with wallets and banks only, +2 million with every container. The second is the truth, a dupe.

Expected supply `= 50 + 900 − 780 = 170` million. Wallets and banks alone give `168 − 170 = −2` million, which looks like a loss. Counting mail and escrow gives `172 − 170 = +2` million, a dupe. An incomplete sum did not only blur the drift, it flipped its sign. Every container must be in the audit, and the result must be exactly zero.
</details>

37. *Week 8 · design.* Two officers click "withdraw item 88213" from the guild bank in the same second, from different zone servers. Write the one SQL statement that moves the item so that exactly one of them gets it, and say what the other one's request sees.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```sql
UPDATE item
SET owner_container_id = :officer_bag
WHERE item_id = 88213 AND owner_container_id = :guild_bank;
```

Run it inside one transaction together with the operation-ID insert. The first request to commit changes one row and wins. The second finds `owner_container_id` no longer equal to the guild bank, updates zero rows, and returns "not owner". The ownership check lives inside the write, so no gap exists between checking and moving. A `SELECT` followed by an `UPDATE` would let both requests pass the check.
</details>

## Week 9: Login, character select, gateway services

Lecture: [week 9](../lectures/w09-login-character-select-gateway-services.md).

38. *Week 9 · compute.* A full world has `C = 4,500` and `L = 100` minutes. What is the admission rate, and how long does position 2,700 wait? If 60 players arrive per minute for two hours, how long is the queue at the end, how long does its last player wait, and how long does it take to drain once arrivals fall to 30 per minute?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `μ = 45` per minute. Position 2,700 waits 60 minutes. The queue reaches 1,800 after two hours, its last player waits 40 minutes, and it drains in 120 minutes.

`μ = 4,500 / 100 = 45`. Wait `= 2,700 / 45 = 60` min. Growth `= 60 − 45 = 15` per minute for 120 minutes, so 1,800. Last wait `= 1,800 × 100 / 4,500 = 40` min. Drain rate `= 45 − 30 = 15` per minute, so `1,800 / 15 = 120` min. Adding login servers changes none of these numbers.
</details>

39. *Week 9 · code.* This is the lecture's evening simulation with new inputs. What does it print?

```python
def evening(arrivals, minutes, cap, session):
    online, queue, log = cap, 0, []
    for t in range(minutes):
        queue += arrivals(t)
        leaving = online / session
        online -= leaving
        admitted = min(queue, cap - online)
        queue -= admitted
        online += admitted
        log.append((t, round(queue)))
    return log

peak = lambda t: 30 if t < 60 else 5          # 30 per minute for an hour, then 5
log = evening(peak, 180, cap=2000, session=100)
print(log[59], log[89], log[119])
print("empties at minute", next(t for t, q in log if t > 60 and q == 0))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
(59, 600) (89, 150) (119, 0)
empties at minute 99
```

`μ = 2,000 / 100 = 20` per minute. For 60 minutes the queue grows by `30 − 20 = 10` per minute, 600 at minute 59. Then it drains at `20 − 5 = 15` per minute, so 30 minutes later (minute 89) it holds `600 − 450 = 150`, and it reaches zero `600 / 15 = 40` minutes after the switch, at minute 99.
</details>

40. *Week 9 · code.* What does this print? Which line shows that the verifier still needs one more rule?

```python
import hashlib, hmac

SECRET = b"shared-by-login-and-world-servers"

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

t = issue(777, "world-2", now=5_000)
print(verify(t, "world-2", now=5_060))
print(verify(t, "world-2", now=5_061))
print(verify(t.replace("|5060|", "|9999|"), "world-2", now=5_061))
print(verify(t, "world-2", now=5_010), verify(t, "world-2", now=5_020))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
accept account 777
reject: expired
reject: forged
accept account 777 accept account 777
```

The ticket expires at 5,060, and the check is `now > expires`, so 5,060 is still accepted and 5,061 is not. Editing the expiry to 9,999 changes the signed body, so the tag no longer matches. The last line accepts the same ticket twice, ten seconds apart. A signature proves the ticket is genuine, not that it is being used for the first time. Add a unique ticket ID and record used IDs (in Redis, with the ticket's expiry) so the second use is rejected as a replay.
</details>

41. *Week 9 · compute.* A world crashes with 15,000 players on it. The login tier handles 120 logins per second, and other worlds keep sending 20 per second. What is the smallest jitter window, and the average extra delay it adds? Separately, the gateway routes 40 messages per second per player at 4 µs each. How many cores route 25,000 players?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `J ≥ 150` s, adding 75 s on average. Four cores route 25,000 players, and you run at least one more for failure.

Spare login capacity is `120 − 20 = 100` per second, so `J ≥ 15,000 / 100 = 150` s, and a uniform delay over 150 s averages 75 s. One core routes `1 / 4 µs = 250,000` messages per second, which is `250,000 / 40 = 6,250` players, so 25,000 players need `ceil(25,000 / 6,250) = 4` cores.
</details>

## Week 10: Chat, guild and social services

Lecture: [week 10](../lectures/w10-chat-guild-and-social-services.md).

42. *Week 10 · compute.* A channel has 5,000 members who post at `q = 0.0005` per member per second. Copies cost 40 µs and 180 bytes each. Compute posts per second, copies per second, cores, outbound Mbit/s and the one-post delay for a single process. Then split it into 5 equal channels.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.5 posts/s, about 12,498 copies/s, 0.50 cores, 18.0 Mbit/s, 200 ms per post. Split five ways, about 2,498 copies/s and 40 ms per post.

`m = 0.0005 × 5,000 = 2.5`. `D = 2.5 × 4,999 = 12,497.5`. Cores `= 12,497.5 × 40 µs ≈ 0.50`. Bandwidth `= 12,497.5 × 180 × 8 / 10⁶ ≈ 18.0` Mbit/s. Delay `= 4,999 × 40 µs ≈ 200` ms. Split: `q × L × (L/k − 1) = 2.5 × 999 = 2,497.5`, and each post now waits `999 × 40 µs ≈ 40` ms. One fifth of the copies, as the model says, and each reader sees one fifth of the traffic too.
</details>

43. *Week 10 · compute.* A guild of 600 members logs in evenly over 300 seconds after maintenance. How many presence packets does per-login push send? How many with 3-second batches, counted the lecture's way? Compare the saving with `B × G / T`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** push 179,700 packets, batch 29,700, about 6.05 times fewer. `B × G / T = 6`.

Push `= 600 × 599 / 2 = 179,700`. One member logs in every 0.5 s, so each 3-second window has 6 logins, and there are 100 windows. When window `j` opens, `6j` members are online, and each gets one packet, so the batch total is `6 × (0 + 1 + … + 99) = 6 × 4,950 = 29,700`. The ratio is `179,700 / 29,700 = 6.05`, close to the 6 logins per window.
</details>

44. *Week 10 · code.* What does this print?

```python
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.tokens, self.last = capacity, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

b = TokenBucket(capacity=2, rate=0.5)
sends = [0.0, 0.5, 1.0, 1.5, 3.0, 3.5, 7.0]
print([("ok" if b.allow(t) else "drop") for t in sends])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
['ok', 'ok', 'drop', 'drop', 'ok', 'drop', 'ok']
```

Start with 2 tokens. At 0 s send (1 left). At 0.5 s refill to 1.25, send (0.25). At 1.0 s, 0.5, drop. At 1.5 s, 0.75, drop. At 3.0 s, 1.5, send (0.5). At 3.5 s, 0.75, drop. At 7.0 s the refill would reach 2.5 and caps at 2, send. Note that this chat bucket stores its refill time even on a drop, unlike week 6's movement bucket. Both give the same totals here, because refilling in two steps under a cap reaches the same value as refilling in one.
</details>

45. *Week 10 · compute.* A 20,000-member channel posts at `q = 0.001` per member per second with `t_send = 50` µs. How many cores does its fan-out need? What is the one-post delay for one process, and with 16 parallel workers? Does the channel fit on 4 cores with 16 workers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 20.0 cores. One process takes 1.0 s per post, 16 workers take about 62.5 ms. It does not fit on 4 cores, because parallel fan-out does not reduce total work.

Posts `= 0.001 × 20,000 = 20` per second. Copies `= 20 × 19,999 ≈ 400,000` per second, times 50 µs is 20.0 cores. One post's delay is `19,999 × 50 µs ≈ 1.0` s, and with 20 posts arriving each second a single process falls further behind every second. Sixteen workers cut the delay to `1.0 / 16 ≈ 62.5` ms but still need 20 cores in total. Only cutting `L` (scope, splits) or `q` (rate limits) cuts the bill.
</details>

46. *Week 10 · design.* Choose the delivery guarantee (at most once, at least once, or exactly-once effect) and where the truth lives for each feature: a zone "looking for group" channel, a "guild event sign-up" list, and a whisper to an online friend. One sentence each.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- Zone LFG channel: at most once, memory only. A lost copy is a post someone scrolls past.
- Guild event sign-up: transactional, in PostgreSQL through the guild's single-writer process. A lost sign-up means a player turns up to a raid that does not expect them, and two officers editing the list must not race.
- Whisper to an online friend: at least once with a message ID, so the receiver drops duplicates. A missed direct message breaks trust, and a duplicate costs nothing once filtered.
</details>

## Week 11: Load testing with bots

Lecture: [week 11](../lectures/w11-load-testing-with-bots.md).

47. *Week 11 · compute.* A zone's action service finishes `μ = 800` requests per second, and each player sends 0.4 actions per second. With the M/M/1 model, what is the largest player count that keeps p99 at or under 60 ms? What is the utilization there?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1,808 players, at about 90% utilization.

`4.605 / (800 − 0.4 n) ≤ 0.060` gives `800 − 0.4 n ≥ 76.75`, so `n ≤ 1,808.1`. At 1,808 players, `λ = 723.2` and `ρ = 723.2 / 800 = 90.4%`. The lecture advises planning for 60 to 70% at expected peak, so promise about 1,200 to 1,400 players and keep the rest as margin for bursts.
</details>

48. *Week 11 · compute.* Use Little's law for both. A gateway handles 1,200 requests per second with a mean time in system of 15 ms. How many requests are inside it on average? A login queue holds 6,000 players and admits 30 per second. How long does a player joining the back wait?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 18 requests in the gateway, and a 200-second wait.

`N = λ × W = 1,200 × 0.015 = 18`. `W = N / λ = 6,000 / 30 = 200` s. Little's law needs no distribution, only a stable queue, which is why it works for both.
</details>

49. *Week 11 · code.* Three percentile rules appear in this course. What does this print, and which number would you put in a load-test report?

```python
import math

lat = [10] * 95 + [50, 60, 70, 80, 500]          # 100 response times, ms

def p99_index(xs):                                # the week 11 simulation's rule
    xs = sorted(xs)
    return xs[int(0.99 * (len(xs) - 1))]

def nearest_rank(xs, q):                          # the week 14 rule
    xs = sorted(xs)
    return xs[math.ceil(q * len(xs)) - 1]

def interpolated(xs, p):                          # the MA102 week 12 rule
    xs = sorted(xs)
    h = (len(xs) - 1) * p + 1
    lo = math.floor(h)
    if lo >= len(xs):
        return xs[-1]
    return xs[lo - 1] + (h - lo) * (xs[lo] - xs[lo - 1])

print(p99_index(lat), nearest_rank(lat, 0.99), round(interpolated(lat, 0.99), 1))
print(sum(lat) / len(lat), nearest_rank(lat, 0.5), max(lat))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
80 80 84.2
17.1 10 500
```

The index rule takes position `int(0.99 × 99) = 98`, the 99th value, 80. Nearest rank takes `ceil(0.99 × 100) − 1 = 98`, also 80. Interpolation sits at `h = 99.01`, one hundredth of the way from 80 to 500, so 84.2. With 100 samples, p99 is decided by one or two values, so the rules disagree in the tail.

Report the rule you used, the sample count, and the max next to p99. Here the max of 500 ms is one request in a hundred that no p99 shows, and the mean of 17.1 ms hides it completely. For small samples, report p99 and max together.
</details>

50. *Week 11 · compute.* 2,000 bots play on a 200-cell map with the lecture's same-cell grid AOI (each bot hears only the others in its own cell). Compare updates per tick for an even spread and for 800 bots in one town cell with the rest spread over the other 199 cells (6 cells with 7 bots, 193 with 6).

<details>
<summary>Answer and worked solution</summary>

**Answer:** 18,000 even, 645,242 clustered, about 36 times more.

Even: 10 per cell, `2,000 × 9 = 18,000`. Clustered: `800 × 799 + 6 × 7 × 6 + 193 × 6 × 5 = 639,200 + 252 + 5,790 = 645,242`. A bot fleet that wanders at random tests a server that will never exist on launch night.
</details>

51. *Week 11 · critique.* A report says: "1,200 bots, offered 600 req/s, achieved 505 req/s, p99 540 ms, SLO 1,000 ms, PASS." Find the problem and say what to do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** achieved load is 16% below offered, so the p99 was measured on a load the test did not intend. The PASS is not valid.

The server finished only 505 requests per second when 600 were asked for. That is the signature of closed-loop bots (coordinated omission) or a saturated bot machine. In the lecture's simulation, the same situation measured open loop gave a p99 of about two minutes, because the queue grew by roughly 100 requests every second. Rerun with open-loop bots that measure from the intended send time, check that achieved matches offered at every step, and keep the bots off the server's machine.
</details>

## Week 12: Single-shard architectures and time dilation

Lecture: [week 12](../lectures/w12-single-shard-architectures-and-time-dilation.md).

52. *Week 12 · compute.* With the lecture's constants (`a = 0.3` ms, `b = 1` µs, `C = 1`, floor 10%), a fight has 1,800 pilots. What is the game speed, and how long in real time does a 15-minute game-time engagement last?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 26.5% speed, and 56.7 real minutes.

`W = 0.0003 × 1,800 + 0.000001 × 1,800² = 0.54 + 3.24 = 3.78`. `f = 1 / 3.78 = 26.5%`. Each game-second takes 3.78 real seconds, so 15 game-minutes take `15 × 3.78 = 56.7` real minutes.
</details>

53. *Week 12 · compute.* A node three times as fast (`C = 3`) hosts the fight. At what pilot count does dilation start, and where does the 10% floor bite? Compare with 861 and 3,016 at `C = 1`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** dilation starts at about 1,589 pilots and the floor bites at about 5,329. Three times the hardware carries 1.85 and 1.77 times the pilots.

Solve `0.000001 n² + 0.0003 n = W` with `W = 3` and `W = 30`. `n = (−0.0003 + √(0.00000009 + 0.000004 W)) / 0.000002`, which gives 1,588.5 and 5,329.3. The ratios `1,589 / 861 ≈ 1.85` and `5,329 / 3,016 ≈ 1.77` sit just above `√3 ≈ 1.73`, and the small extra comes from the linear term. Hardware buys a square root in crowd size.
</details>

54. *Week 12 · code.* This is the lecture's controller with a new fight. What does it print? Why does the third run repay its backlog even though the floor binds?

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1

def work(n):
    return A * n + B * n * n

def run(alpha, aim, seconds=600):
    f, backlog, worst = 1.0, 0.0, 0.0
    for t in range(seconds):
        n = 800 if t < 20 else 2800
        target = max(FLOOR, min(1.0, aim * C / work(n)))
        f = f + alpha * (target - f)
        backlog = max(0.0, backlog + f * work(n) - C)
        worst = max(worst, backlog)
    return round(worst, 1), round(backlog, 1)

print(run(1.0, 1.0), run(0.3, 1.0), run(0.3, 0.85))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
(0.0, 0.0) (17.9, 17.9) (15.7, 0.0)
```

`W(2,800) = 0.84 + 7.84 = 8.68`. With `α = 1` the speed jumps straight to `1 / 8.68 = 11.5%` and the node never overloads. With `α = 0.3` it lags during the warp-in and builds 17.9 CPU-seconds of backlog. Aimed at 100%, nothing repays it, so it is still there after ten minutes.

With `aim = 0.85`, the target `0.85 / 8.68 = 9.8%` is below the floor, so `f` settles at 10%. The node then does `0.1 × 8.68 = 0.868` CPU-seconds of new work per real second and has 0.132 left to repay the debt, which clears 15.7 CPU-seconds in about two minutes. The floor binding did not hurt here because 2,800 pilots are still below the 3,016 where the floor stops being enough.
</details>

55. *Week 12 · compute.* A structure timer runs on real time and has 30 minutes left when a fight on its node drops to 20% speed. How many game-seconds of combat fit before it expires? Separately, with dilation off, a 2,500-pilot fight starts at `C = 1`. After how many real seconds does a new command wait more than two minutes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 360 game-seconds, and after about 19.8 real seconds.

`30 × 60 × 0.2 = 360` game-seconds, six minutes of combat for a timer that reads 30 minutes. The side that wants it to expire gains by making the fight bigger and slower.

Without dilation, `W(2,500) = 0.75 + 6.25 = 7.0`, so the backlog grows by 6 CPU-seconds per real second and the delay is `6t + 1`. It passes 120 s when `t > 119 / 6 ≈ 19.8` s.
</details>

## Week 13: Cloud deployment and autoscaling

Lecture: [week 13](../lectures/w13-cloud-deployment-and-autoscaling.md).

56. *Week 13 · compute.* 36,000 players are online and demand rises by 1,200 per minute. Servers hold 500 players and take 10 minutes from decision to ready. What is the highest safe target utilization, and how many servers must run? Repeat with the lag cut to 4 minutes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** at 10 minutes, `u ≤ 75%` and 96 servers. At 4 minutes, `u ≤ 88.2%` and 82 servers.

`r × L = 12,000`. `u ≤ 36,000 / 48,000 = 0.75`, `N = 48,000 / 500 = 96`. With `L = 4`, `r × L = 4,800`, `u ≤ 36,000 / 40,800 = 0.882`, `N = ceil(40,800 / 500) = 82`. Cutting six minutes of lag saves 14 servers, every hour the ramp policy is in force.
</details>

57. *Week 13 · code.* This is the lecture's `simulate` on a patch-day trace. What does it print? Check the first line against `u ≤ D / (D + r × L)`.

```python
import math

def simulate(demand, cap=500, util=0.8, lag=8):
    ready = math.ceil(demand[0] / (util * cap))
    booting = []
    peak_wait, paid = 0, 0
    for t, d in enumerate(demand):
        ready += booting.count(t)
        booting = [m for m in booting if m > t]
        want = math.ceil(d / (util * cap))
        short = want - ready - len(booting)
        if short > 0:
            booting += [t + lag] * short
        peak_wait = max(peak_wait, d - ready * cap)
        paid += ready + len(booting)
    return peak_wait, paid

patch = [10_000 + 1_000 * min(t, 15) for t in range(60)]
for util, lag in [(0.8, 5), (0.6, 5), (0.8, 2)]:
    wait, paid = simulate(patch, util=util, lag=lag)
    print(util, lag, max(wait, 0), round(paid / 60, 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
0.8 5 2500 57.9
0.6 5 0 77.2
0.8 2 0 57.9
```

With `D = 10,000`, `r = 1,000` and `L = 5`, the rule allows `u ≤ 10,000 / 15,000 = 66.7%`. At 80% the fleet has too little headroom and 2,500 players wait at the peak. At 60% there is no queue, at a cost of 77.2 server-hours against 57.9. Cutting the lag to 2 minutes raises the limit to `10,000 / 12,000 = 83.3%`, so 80% works with no queue and no extra cost.
</details>

58. *Week 13 · compute.* Session lengths are exponential with a mean of 120 minutes. How long does passive draining take to reach 2% of a server's players? If you instead kill a server holding 8 players, each with a 5% chance of being mid-trade or mid-craft, what is the chance at least one of them loses progress?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 469 minutes (7.8 hours), and a 33.7% chance.

`e^(−t/120) = 0.02` gives `t = 120 × ln 50 ≈ 469` min, longer than most daily troughs. `1 − 0.95^8 ≈ 0.337`. Drain to zero with packed placement and handoff, or wait for maintenance.
</details>

59. *Week 13 · compute.* Using the lecture's daily curve and 400 players per server, committed servers now cost $0.20 per hour and on-demand $0.40. How many servers should you commit, and what does the day cost? Compare with autoscaling on demand only ($569.20).

<details>
<summary>Answer and worked solution</summary>

**Answer:** commit 55 servers (56 to 58 cost the same), for $372.00 a day, 35% below on-demand autoscaling.

Break-even is `0.20 / 0.40 = 50%` of the day, 12 hours. From the curve, the 55th server is needed in 14 hours, the 56th, 57th and 58th in exactly 12, and the 59th in 11. Servers needed 14 hours or more are worth committing, servers needed exactly 12 are a tie, and the 59th is not. Cost at 55: `55 × 24 × 0.20 = $264.00` committed plus 270 on-demand server-hours at $0.40, $108.00, total $372.00. A cheaper commitment moves the line up the curve, from 53 at the lecture's 60% ratio to 55 here.
</details>

## Week 14: Observability, logs, metrics, traces

Lecture: [week 14](../lectures/w14-observability-logs-metrics-traces.md).

60. *Week 14 · compute.* A zone runs at 60 Hz with an overrun rate of 0.2%. How many stalls per minute does a player see, and what share of seconds contain one? The design goal is at most 2 stalls per minute. Which percentile must stay under the budget?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 7.2 stalls per minute and about 11.3% of seconds. The goal needs p99.944.

`60 × 60 × 0.002 = 7.2`. `1 − 0.998^60 ≈ 0.113`. For the goal, `p ≤ 2 / 3,600 = 0.056%`, so `q = 1 − 0.00056 = 99.944%`. The faster the tick, the further into the tail the alert must look for the same player experience.
</details>

61. *Week 14 · code.* This uses the lecture's cumulative histogram and interpolated quantile. What does it print? What are the true p95 and p99 of the data, and how many stalls per minute would this zone show at 20 Hz?

```python
BOUNDS = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 250]

def histogram(values):
    return [sum(v <= b for v in values) for b in BOUNDS] + [len(values)]

def quantile(q, counts):
    rank = q * counts[-1]
    lower_bound, lower_count = 0, 0
    for bound, count in zip(BOUNDS, counts):
        if count >= rank:
            return lower_bound + (bound - lower_bound) * (rank - lower_count) / (count - lower_count)
        lower_bound, lower_count = bound, count
    return BOUNDS[-1]

ticks = [20] * 900 + [35] * 80 + [60] * 15 + [120] * 5
h = histogram(ticks)
print(h[BOUNDS.index(20)], h[BOUNDS.index(40)], h[BOUNDS.index(50)], h[-1])
print(round(quantile(0.95, h), 1), round(quantile(0.99, h), 1))
print("over budget:", h[-1] - h[BOUNDS.index(50)])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
900 980 980 1000
36.2 66.7
over budget: 20
```

The cumulative counts at 20, 40 and 50 ms are 900, 980 and 980 of 1,000. Rank 950 falls in the 30 to 40 ms bucket, `30 + 10 × 50 / 80 = 36.25`, which Python's rounding prints as 36.2. The true p95 is 35. Rank 990 falls in the 50 to 75 bucket, `50 + 25 × 10 / 15 = 66.7`, while the true p99 is 60. The count over budget is exact because 50 is a bucket edge. 20 of 1,000 ticks is `p = 2%`, which at 20 Hz is `60 × 20 × 0.02 = 24` stalls per minute.
</details>

62. *Week 14 · compute.* 12,000 players each cause 0.6 log lines per second across all services, 300 bytes each. How many GB per day is that? If 70% of lines are routine combat events and you keep 1 in 50 of those, what is the new daily volume? Separately, a tick histogram (15 series per zone) is labelled by zone (120 zones) and build version (3 live builds). How many series?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 187 GB per day unsampled, about 59 GB per day sampled, and 5,400 series.

`12,000 × 0.6 × 300 = 2,160,000` B/s, times 86,400 s is 186.6 GB. Sampling keeps `30% + 70% / 50 = 31.4%` of lines, so `2.16 × 0.314 = 0.678` MB/s, about 58.6 GB per day. Series `= 15 × 120 × 3 = 5,400`. Build version is a small, fixed set of values and a fair label. A `player_id` label would multiply this by the player count.
</details>

63. *Week 14 · compute.* The gateway handles 60 logins per second and 0.4% fail. How many failed-login traces per hour do you keep with 5% head sampling? With tail sampling that keeps every failure plus 1% of successes, how many traces per hour in total?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 43 failures an hour with head sampling. Tail sampling keeps all 864 failures plus about 2,151 successes, about 3,015 traces an hour.

Failures `= 60 × 0.004 = 0.24` per second, 864 per hour. Head sampling at 5% keeps 43.2. Successes are `60 × 0.996 = 59.76` per second, and 1% of them for an hour is `59.76 × 0.01 × 3,600 ≈ 2,151`. Tail sampling costs a stateful collector and gives you every example of the failure you are investigating.
</details>

64. *Week 14 · critique.* A team's plan: "The dashboard shows the average of each zone server's p99 tick time. Metrics are written to the game's Redis so the dashboard is fast. We page when fleet average tick time passes 40 ms." Find three problems and fix each.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- The average of p99s is not a percentile of anything. In the lecture's example it read 18.4 ms while the fleet p99 was 23.8 ms and one zone stalled 12 times a minute. Merge histogram buckets, and show and alert per zone.
- Metrics in the game's Redis share its failure mode. When Redis fails, the game and its monitor go dark together, which is what slowed Roblox's 2021 diagnosis when monitoring depended on Consul. Send metrics to a separate store in another failure domain, and add an outside login probe.
- Mean tick time is a capacity number, not an experience number. A zone can average 19.8 ms and still stall 12 times a minute. Page on stalls per minute per zone (for example more than 2 per minute for 5 minutes), counted exactly from a bucket edge at the budget.
</details>

## Synthesis: several weeks at once

65. *Weeks 1, 2, 5 and 12 · compute.* A zone server hosts 19 zones of 25 players and a world-boss zone of 400. Use week 1's tick model (2 ms fixed, 0.05 ms per player, 0.001 ms per delivery, 10 Hz, `u = 5`). Compute the tick time. Then compute it for each fix: (a) halve `u` in the boss zone and everywhere else (as 50% time dilation would); (b) split the boss crowd into two layers of 200 on the same server; (c) drop the server to 5 Hz with `u` unchanged. Which fixes fit their tick?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 131.25 ms against a 100 ms budget. (a) 88.5 ms, fits. (b) 91.25 ms, fits. (c) 216.75 ms against a 200 ms budget, does not fit.

Players `= 400 + 475 = 875`, per-player cost `0.05 × 875 = 43.75`. Deliveries per second `= 5 × (400 × 399 + 19 × 600) = 5 × 171,000 = 855,000`, so 85,500 per tick, and the tick is `2 + 43.75 + 85.5 = 131.25` ms.

(a) Halving `u` halves the deliveries, `2 + 43.75 + 42.75 = 88.5`. (b) Two layers of 200 give `5 × (2 × 200 × 199 + 11,400) = 455,000`, 45,500 per tick, so `2 + 43.75 + 45.5 = 91.25`. (c) At 5 Hz the budget doubles to 200 ms, but each tick now carries twice the deliveries (171,000) because players still send 5 updates per second, and the per-player cost is per tick. `2 + 43.75 + 171 = 216.75`. A slower tick only helps if the update rate falls with it, which is exactly what time dilation does by slowing the game clock.
</details>

66. *Weeks 5, 6, 7 and 11 · critique.* A student's final-server plan says: "The zone ticks at 30 Hz like a shooter. Movement uses a per-packet check with `s = 0.5` s at 10 updates a second. Every change is written through to PostgreSQL. We will load test with 500 closed-loop bots spread evenly over the map." Find the four problems and put a number on each using the lecture models.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **30 Hz.** With week 5's example zone (`c = 46` ms), 30 Hz is 138% utilization. Size the rate from the fastest player decision and the densest moment, then check `u ≤ 0.6`.
- **Per-packet check at `s = 0.5`.** The sustained factor is `(0.1 + 0.5) / 0.1 = 6`, a permanent six-times speed hack. A token bucket with the same tolerance gives 1.0× and a 4.2 m blink at 7 m/s.
- **Write-through for everything.** At 3,000 players and 0.5 changes per second that is 1,500 commits per second from one shard, and every action waits on the database. Use write-behind for counters, an event log for valuable events, and one transaction for trades.
- **Closed-loop bots spread evenly.** Closed-loop bots hide overload (week 11's 1,200-bot run reported 562 ms against about two minutes open loop), and an even spread under-loads grid AOI badly. In the lecture's 1,000-bot, 100-cell example, putting half the bots in one cell gives 28 times the updates. Use open-loop bots, report offered against achieved load, and include a clustered scenario.
</details>
