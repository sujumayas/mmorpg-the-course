# CS201 · Week 06 — Cache Locality and Data-Oriented Design

**Why this matters:** Two versions of the same movement loop, over the same million entities, doing the same arithmetic, can differ fifteenfold in speed. The only change is how the struct is declared. At that scale the difference is 4 ms against 0.3 ms, a quarter of a 60 Hz frame against almost nothing. The processor was never the problem. The memory was. This week you learn to predict that difference from a drawing of cache lines, and to lay out data so the hardware works with you.

**You will be able to:**
- Compute the bytes a loop pulls from memory per entity for a given struct layout and cache line size, and predict the speed ratio between two layouts.
- Measure array-of-structs, hot/cold split and struct-of-arrays layouts on your machine and explain where the measurements agree with the model and where they depart from it.
- Reorder and split a struct to cut padding and separate hot fields from cold ones.
- Critique a data layout for a given set of systems, and decide when struct-of-arrays is worth its costs.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 3, section 3.5 (memory architectures, caches). Nystrom, *Game Programming Patterns* (2014), "Data Locality" chapter, the whole chapter. Watch the first 30 minutes of Mike Acton's CppCon 2014 talk "Data-Oriented Design and C++".

**Prerequisites from earlier courses:** [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md), section 4. It introduced cache lines and cache misses and promised this week would measure them in a language that stores values contiguously; it does not repeat here. [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (constant factors are real). From this course: [week 2, C++ for engines](w02-cpp-for-engines-memory-raii-and-move-semantics.md) (where an object's bytes live), [week 4, the frame](w04-the-frame-update-render-present.md) (what a millisecond is worth) and [week 5, ECS design](w05-entity-component-system-design.md), whose archetype columns are this week's struct-of-arrays and whose measured join costs are a locality effect.

**Interactive:** [`examples/w06-aos-vs-soa-cache-lines.html`](../examples/w06-aos-vs-soa-cache-lines.html). Keep it open during section 2.

---

## 1. Memory arrives in lines

A processor core runs billions of simple operations a second. Main memory cannot feed it at that rate, so every modern CPU keeps copies of recently used memory in small, fast **caches** close to the core. When the core needs a value that is in the cache, it gets it in a few cycles. When it is not, the core waits while the value comes from main memory. That wait is a **cache miss**, and Nystrom puts its cost at hundreds of cycles.

Two facts about caches decide everything in this lecture.

**Memory moves in lines.** The cache never fetches a single byte or a single float. It fetches a **cache line**, a fixed-size aligned block of memory that contains the address you asked for. If you read one 4-byte float, the whole line comes with it. Line size depends on the processor:

| Processor family | Cache line | Source |
|---|---|---|
| x86-64 (most PCs) | 64 bytes | Linux kernel default for 64-bit x86 |
| Apple M4 Pro (the reference machine) | 128 bytes | `sysctl hw.cachelinesize` |

**Caches are small.** The reference machine's performance cores have 128 KB of level-1 data cache each, and a 16 MB level-2 cache shared by five cores. A working set that fits in those sizes stays close to the core across frames. One that does not is streamed from main memory every time you walk it.

Put the two facts together and you have the rule for this week. **The cost of a loop over a big array is set by the lines it touches, not the bytes it uses.** Use 24 bytes out of every 128-byte line and you pay for all 128.

The processor has one more trick. A **hardware prefetcher** watches the addresses you touch, and when it sees a steady pattern (such as every 128 bytes, upward) it starts fetching the following lines before you ask. Walking an array in order is the pattern every prefetcher recognises. Jumping around, as a linked list does, defeats it. That is why CS102 week 5 told you linked lists lose more often than Big-O predicts.

## 2. Worked example: one million entities, two layouts

### The hook

Take the movement system from week 5: `position += velocity × dt` for every entity. Here it is over one million entities, written twice. The arithmetic is identical. The only difference is whether each entity's fields sit together in one struct (**array of structs**, AoS) or each field sits in its own array (**struct of arrays**, SoA).

On the reference machine, the AoS version takes 4.2 ms. The SoA version takes 0.27 ms. Same compiler, same flags, same result to the last bit.

This is not a lab curiosity. Unity's Entities package stores each archetype in 16 KiB chunks that hold one array per component type (week 5). Bevy's default table storage keeps one column per component. Nystrom's "Data Locality" chapter reports a pointer-chasing game loop made fifty times faster by putting components into contiguous arrays. Mike Acton's 2014 CppCon talk argues that engine code should be designed around how data moves through the machine, not around objects. Every one of them is responding to the effect you are about to compute.

### The model

A loop walks `N` entities. Each entity's struct is `s` bytes (the **stride**, the distance from one entity to the next). The loop uses `h` **hot** bytes per entity, stored together at the start of the struct. The cache line is `L` bytes.

```
bytes fetched per entity:
  AoS, stride s ≥ L:   B_AoS = L × ceil(h / L)      each entity's hot bytes cost whole lines
  AoS, stride s < L:   B_AoS = s                    entities share lines; every byte comes in
  SoA:                 B_SoA = h                    each array is dense, every fetched byte is used

memory traffic      = N × B
useful fraction     u = h / B
predicted speed-up  = B_AoS / B_SoA                 when the data does not fit in cache
```

- The model counts bytes read into the cache. It assumes the struct starts on a line boundary and that the data is too big to stay cached between frames.
- When the working set fits in cache, the lines come from the cache instead of main memory, and the model's prediction shrinks toward whatever the arithmetic costs.
- The model leaves out two things you will meet in the measurements: modified lines written back to memory, and SIMD instructions, which process several floats per instruction when the data is laid out for it.

### Numbers you can check

The entity is the kind of struct a first engine grows. 128 bytes, with the movement system's six hot floats first.

```cpp
struct EntityAoS {            // 128 bytes per entity
    float px, py, pz;         // hot: read and written by movement
    float vx, vy, vz;         // hot: read by movement
    float health, armor;      // cold for movement
    std::uint32_t flags, team;
    float world[16];          // 64-byte matrix, cold for movement
    char name[24];
};
```

So `s = 128` and `h = 24`. The model, for `N = 1,000,000`:

| Line size `L` | `B_AoS` | `B_SoA` | Useful fraction AoS | Traffic AoS | Traffic SoA | Predicted speed-up |
|---|---|---|---|---|---|---|
| 64 bytes (x86-64) | 64 | 24 | 37.5% | 64 MB | 24 MB | 2.7× |
| 128 bytes (Apple M4 Pro) | 128 | 24 | 18.75% | 128 MB | 24 MB | 5.3× |

Check the second row by hand. Each entity starts a fresh 128-byte line, and the six hot floats sit in the first 24 bytes of it, so `ceil(24 / 128) = 1` line, 128 bytes. The SoA arrays are dense, so a line of `px` values holds 32 entities' worth, all used. `128 / 24 = 5.33`. Notice what the table says about portability. **The same code, on a machine with bigger lines, wastes a larger share of every fetch.**

Now the code. Build it and run it yourself.

```cpp
// aos_soa.cpp: move 1,000,000 entities with AoS and SoA storage.
// Build: c++ -std=c++20 -O2 aos_soa.cpp -o aos_soa && ./aos_soa
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>

struct EntityAoS {            // 128 bytes per entity
    float px, py, pz;         // hot: read and written by movement
    float vx, vy, vz;         // hot: read by movement
    float health, armor;      // cold for movement
    std::uint32_t flags, team;
    float world[16];          // 64-byte matrix, cold for movement
    char name[24];
};
static_assert(sizeof(EntityAoS) == 128);

struct EntitiesSoA {          // one array per field; only the hot ones are shown
    std::vector<float> px, py, pz, vx, vy, vz;
};

using Clock = std::chrono::steady_clock;

int main() {
    const int N = 1'000'000, RUNS = 50;
    const float dt = 1.0f / 60.0f;
    std::vector<EntityAoS> aos(N);
    EntitiesSoA soa;
    for (auto* v : {&soa.px, &soa.py, &soa.pz, &soa.vx, &soa.vy, &soa.vz}) v->resize(N);
    for (int i = 0; i < N; ++i) {
        aos[i] = {};
        aos[i].vx = soa.vx[i] = 1.0f;
        aos[i].vy = soa.vy[i] = 2.0f;
        aos[i].vz = soa.vz[i] = 3.0f;
        soa.px[i] = soa.py[i] = soa.pz[i] = 0.0f;
    }
    double best_aos = 1e9, best_soa = 1e9;
    for (int r = 0; r < RUNS; ++r) {
        auto t0 = Clock::now();
        for (auto& e : aos) { e.px += e.vx * dt; e.py += e.vy * dt; e.pz += e.vz * dt; }
        auto t1 = Clock::now();
        for (int i = 0; i < N; ++i) {
            soa.px[i] += soa.vx[i] * dt; soa.py[i] += soa.vy[i] * dt; soa.pz[i] += soa.vz[i] * dt;
        }
        auto t2 = Clock::now();
        best_aos = std::min(best_aos, std::chrono::duration<double, std::milli>(t1 - t0).count());
        best_soa = std::min(best_soa, std::chrono::duration<double, std::milli>(t2 - t1).count());
    }
    std::printf("AoS: %.3f ms  SoA: %.3f ms  ratio %.1f\n", best_aos, best_soa, best_aos / best_soa);
    std::printf("check: px[0] %.4f %.4f\n", aos[0].px, soa.px[0]);
}
```

Three runs on the reference machine (Apple M4 Pro, Apple clang 17, September 2026) printed:

```
AoS: 4.177 ms  SoA: 0.267 ms  ratio 15.7
check: px[0] 0.8333 0.8333
AoS: 4.172 ms  SoA: 0.269 ms  ratio 15.5
check: px[0] 0.8333 0.8333
AoS: 4.176 ms  SoA: 0.273 ms  ratio 15.3
check: px[0] 0.8333 0.8333
```

The timings will differ on your machine. The check line will not: 50 runs of `0 + 1 × (1/60)` give `50/60 = 0.8333` in both layouts.

**Measured against the model.** The file `bench_layouts.cpp` in [lab 06's starter](../labs/lab06-starter/) adds a third layout, the **hot/cold split**: an array of small 24-byte structs holding only the hot fields, with the cold fields moved to a separate array. It runs all three at four sizes. Best of 50 runs (10 at 10 million), times in milliseconds, two runs agreed within 10%.

| N | Working set, AoS | AoS | Hot/cold split | SoA | AoS ÷ SoA |
|---|---|---|---|---|---|
| 10,000 | 1.28 MB | 0.010 | 0.006 | 0.003 | 3.7 |
| 100,000 | 12.8 MB | 0.097 | 0.054 | 0.027 | 3.5 |
| 1,000,000 | 128 MB | 4.09 | 0.61 | 0.27 | 15.2 |
| 10,000,000 | 1.28 GB | 44.1 | 6.2 | 3.0 | 14.6 |

Read it in two steps.

**The cliff between 100,000 and 1,000,000.** At 100,000 entities the AoS array is 12.8 MB, which fits in the 16 MB level-2 cache, and 10 times more entities take 10 times longer, as Big-O says. At one million it is 128 MB and does not fit. AoS jumps from 0.097 ms to 4.09 ms, 42 times longer for 10 times the entities. The SoA arrays at one million total 24 MB, just over the cache, and grow 10×. That jump is the model switching on. Below the cache size, layout costs you a factor of 3 or 4. Above it, a factor of 15.

**The factor itself.** The model predicted 5.3× for any compact layout on 128-byte lines. The same benchmark compiled with `-fno-vectorize -fno-slp-vectorize`, which forbids SIMD, gives at one million entities: AoS 3.80 ms, hot/cold 0.47 ms, SoA 0.92 ms, a ratio of 4.1× for SoA. Scalar SoA lands close to the prediction. Two effects the model leaves out explain the rest.

- **Write-back.** Movement writes `px, py, pz`, so every AoS line it touches is modified, and the cache must eventually write the whole 128-byte line back to memory. AoS moves about 256 bytes per entity in total. The hot/cold split writes back 24-byte structs, a tenth of that. That is why the split beats the read-only model, at about 7×.
- **SIMD.** With the six fields in six dense arrays, the compiler processes several entities per instruction. Scalar SoA took 0.92 ms and vectorized SoA 0.27 ms. The AoS layout gives the compiler nothing to vectorize, because consecutive `px` values are 128 bytes apart.

So the honest summary is this. **The byte model predicts the size of the problem (a factor of about 5 from memory alone) and exactly when it appears (when the data leaves the cache). The layout that fixes it also unlocks SIMD, which multiplies the gain again.**

### The visual

Open [`w06-aos-vs-soa-cache-lines.html`](../examples/w06-aos-vs-soa-cache-lines.html). The left view is memory, drawn as a column of cache lines, each a row of cells, one cell per 4 bytes. In AoS mode each entity fills a band of lines, with the hot bytes coloured and the cold bytes grey. As the loop cursor advances, every line it touches lights up, whole. In SoA mode the same memory is re-drawn as six dense arrays, and the lit lines are solid colour from edge to edge. The right view is a bar pair: megabytes fetched for `N` entities in each layout, the useful fraction, and the predicted time at a bandwidth you set.

Switch the line size between 64 and 128 bytes and watch the AoS lines get longer while the hot cells stay the same. The grey inside each lit line is the waste. **Same loop, same entities; the only thing that changes is how much grey the machine has to carry.** Then drag the hot bytes slider up to 128 (a system that uses every field) and watch the two layouts converge. SoA helps only the systems that use a few fields of many entities.

### Cross-game recognition

- **Unity Entities 1.3.** Each chunk is 16 KiB and holds one array per component type plus one of entity IDs. Within a chunk, that is SoA by component. A system that reads Position and Velocity walks two dense arrays and never loads Health or RenderMesh.
- **Bevy 0.19.** The default table storage keeps one column per component type, documented as fast and cache-friendly to iterate. It is the same layout as our SoA, grouped by archetype.
- **Nystrom, "Data Locality" (2014).** His example game loop jumps through pointers to components scattered on the heap. Moving the components into contiguous arrays made it about fifty times faster in his measurement, well beyond our 15×, because pointer chasing also defeats the prefetcher. The chapter's other two techniques, hot/cold splitting and keeping active particles at the front of the array so the loop never tests an "active" flag, are both applications of `u = h / B`.
- **Your own week 5 measurement.** The sparse-set movement join took 0.133 ms when the Velocity and Position pools were in different orders and 0.068 ms when they were in the same order. Same bytes, different pattern. Aligned pools walk memory in order, and the prefetcher keeps up.

Four sources, one principle: **arrange data in the order and grouping the hot loop reads it, and every fetched byte gets used.**

### Eyes-open design judgment

- **SoA is for loops over many entities that use a few fields.** Movement, culling, particle updates and animation sampling qualify. A system that reads every field of one entity (an inspector panel, a save routine) touches one line per field in SoA, which can be worse than one or two lines in AoS.
- **The hot/cold split is the cheap first step.** It needs no change to how code reads a field, `hot[i].px` instead of `px[i]`, and it recovered most of the memory gain in the table. Many engines stop there.
- **SoA has costs in code.** Adding a field means adding an array and keeping every array the same length. Deleting an entity means swap-and-pop in every array (week 5). A debugger shows six arrays, not one entity. Plan for helpers that hide this, or use an ECS whose storage already does it.
- **Hybrids exist.** Array of structs of arrays (AoSoA) stores small blocks, for example 8 entities' `px` values together, then their `py` values, and so on. Unity's chunks are one form of this at a coarser grain. It keeps SIMD-friendly runs while keeping one entity's data within a few nearby lines.
- **Measure on your target.** The 64-byte and 128-byte rows of the model differ by a factor of two. A console, a phone and a desktop can disagree about which layout wins by how much. Week 13's profiler is where you check.

### Check yourself (worked example)

1. An entity struct is 96 bytes with 16 hot bytes at the start, and `L = 64`. Compute `B_AoS`, `B_SoA`, the useful fraction and the predicted speed-up for a loop over 2 million entities. How much memory does each layout move?
2. The same struct shrinks to 48 bytes after a cleanup, still with 16 hot bytes and `L = 64`. What does the model predict now, and why did the formula change?
3. At 100,000 entities the measured AoS to SoA ratio was 3.5, well below the 15 at one million. Using the cache sizes in section 1, explain why.

<details>
<summary>Answers</summary>

1. `s = 96 ≥ 64`, so `B_AoS = 64 × ceil(16/64) = 64`. `B_SoA = 16`. Useful fraction 25%, predicted speed-up 4×. AoS moves 128 MB, SoA 32 MB. (If the 96-byte structs are not line-aligned, some entities' hot bytes cross a line boundary and cost two lines, so AoS does a little worse.)
2. Now `s = 48 < 64`, so entities share lines and every byte comes in: `B_AoS = 48`. Speed-up `48 / 16 = 3×`. Shrinking the struct helped AoS because more entities fit in each line.
3. At 100,000 entities the AoS array is 12.8 MB, less than the 16 MB level-2 cache, so after the first run the lines come from the cache and memory traffic hardly matters. The remaining 3.5× is mostly SIMD. At one million the 128 MB array must stream from main memory every run, and the byte model applies.

</details>

## 3. Padding, alignment and field order

Before you split anything, check what the compiler did to your struct. Each type has an **alignment**: a `double` must start at an address divisible by 8, a `float` at one divisible by 4. The compiler inserts **padding**, unused bytes, to meet those rules, and it rounds the struct's size up to a multiple of its largest alignment so arrays of it stay aligned.

```cpp
// padding.cpp: the same four fields in two orders.
// Build: c++ -std=c++20 padding.cpp -o padding && ./padding
#include <cstdio>
struct Bad  { bool alive; double hp; bool stunned; float x; };
struct Good { double hp; float x; bool alive; bool stunned; };
int main() { std::printf("Bad %zu bytes, Good %zu bytes\n", sizeof(Bad), sizeof(Good)); }
```

Output:

```
Bad 24 bytes, Good 16 bytes
```

Trace `Bad`. `alive` at byte 0, then 7 bytes of padding so `hp` starts at 8, `hp` at 8 to 15, `stunned` at 16, 3 bytes of padding so `x` starts at 20, `x` at 20 to 23. Size 24. `Good` puts the largest field first and packs the two `bool`s at the end, then pads to 16. A third of `Bad` is empty, and in an array of a million that is 8 MB of cache capacity holding nothing.

The rule of thumb is to order fields from largest alignment to smallest. Better still, group fields by which systems read them, then sort within each group. Grouping decides which bytes share a line with the hot data. Sorting decides how much space the padding wastes.

## 4. Designing for the access pattern

Data-oriented design starts from a question object-oriented design rarely asks: **what does the hot loop read, in what order, and how often?** Answer it first, then choose the layout. Three patterns cover most of an engine.

**Walk everything, use a few fields.** Movement, culling, cooldown timers. Use SoA or a hot/cold split, sorted in the order the loop walks.

**Walk a changing subset.** Particles that live and die, entities that are on screen. Keep the active ones packed at the front of the array and track the count, as Nystrom's particle example does. Swap a dying element with the last active one. The loop then runs `for (i = 0; i < active; ++i)` with no branch and no wasted lines. This is swap-and-pop from week 5, used for locality.

**Look up by key, then use many fields.** A quest log, an item definition, one NPC's dialogue state. AoS is fine, and a hash map in front of it is fine (CS102 week 5). These run a few times per frame, not a million.

A worked design, to make the steps concrete. An MMO client keeps 20,000 nearby entities. Each frame three systems run over all of them:

| System | Reads | Writes |
|---|---|---|
| Interpolation | previous and next position (24 bytes), timestamp (4) | position (12) |
| Culling | position (12), bounding radius (4) | visible flag (1) |
| Nameplate update, visible only (about 300) | position, name, guild, health | — |

Interpolation and culling walk all 20,000 and share `position`. So store `position`, `prev_pos`, `next_pos`, `timestamp` and `radius` as hot arrays. Store `name`, `guild` and other text in a cold array indexed the same way. The nameplate system runs over 300 entities and reads a mix, so it is fine to gather from both. The visible flag becomes a packed list of visible indices, rebuilt by culling each frame, which is the "changing subset" pattern and saves nameplates from scanning 20,000 flags.

## In-class activity (25 minutes)

Groups of three, paper and the interactive.

1. **Predict (8 min).** Your card has a struct (for example, a 72-byte `Projectile` with fields listed) and one system with the fields it reads. Compute `B_AoS`, `B_SoA` and the predicted speed-up at `L = 64` and `L = 128`. Check with the interactive's custom mode.
2. **Pad (5 min).** Compute `sizeof` for the card's struct by hand with padding, then reorder the fields to minimize it. Verify with a one-line `static_assert` if a laptop is free.
3. **Split (12 min).** Your card also lists three systems that use the struct. Design a hot/cold split or SoA layout that serves all three. Write, for each system, the bytes it fetches per entity under your layout and under the original.

Expected output: a card with the model numbers, the before and after `sizeof`, and a layout with a per-system bytes table.

## Common misconceptions

- **"SoA is always faster."** It is faster for loops over many entities that use a few fields. For per-entity access to many fields it can be slower, and inside the cache the gap is small.
- **"Using 24 bytes costs 24 bytes."** Memory moves in lines. It costs whole lines, 64 or 128 bytes each.
- **"If it fits in cache, layout doesn't matter."** It matters less. The measured ratio inside the cache was still 3.5×, mostly from SIMD.
- **"The compiler will fix my layout."** C++ compilers keep fields in the order you declared them and cannot split a struct into arrays for you. Padding and grouping are your job.
- **"Big-O says both loops are O(N), so they cost the same."** Big-O hides constant factors. Here the constant differs by 15.

## Check yourself

1. A particle struct has position (12 bytes), velocity (12), color (16), age (4), lifetime (4), texture index (4) and a 16-byte padding field someone added "for alignment", 68 bytes declared. The update loop reads position, velocity and age and writes position and age. Compute `sizeof` with natural padding (all fields are 4-byte aligned), then propose a hot/cold split and give `B` per particle for the loop before and after, at `L = 64`.
2. A system reads 8 of the 128 bytes in each entity. At `L = 128`, how many times more bytes does AoS fetch than SoA? At `L = 64`?
3. A teammate converts the inventory system (which opens one player's bag and reads every item's 20 fields) to SoA and reports it got slower. Explain why in two sentences.
4. In the table in section 2, SoA at 10 million entities took 3.0 ms. Estimate the effective memory bandwidth it achieved, counting only the 24 bytes per entity read.

<details>
<summary>Answers</summary>

1. All fields are 4-byte aligned, so no padding is added: 68 bytes. Hot struct: position, velocity, age = 28 bytes; cold: color, lifetime, texture index (and delete the useless padding field) = 24 bytes. Before: `s = 68 ≥ 64`, hot bytes at the start, `B = 64 × ceil(28/64) = 64` (more if the 68-byte structs straddle lines, which most do). After, with an array of 28-byte hot structs: `s = 28 < 64`, `B = 28`. About 2.3× less traffic.
2. `L = 128`: AoS fetches 128, SoA 8, 16×. `L = 64`: 64 against 8, 8×.
3. The inventory system reads all 20 fields of a few items, so under SoA each item costs up to 20 separate lines instead of one or two. It is a "look up, use many fields" pattern, the one where AoS wins.
4. `10,000,000 × 24 bytes = 240 MB` in 3.0 ms, about 80 GB/s. Compare AoS: `1.28 GB / 44.1 ms ≈ 29 GB/s`. The SIMD SoA loop kept the memory system much busier than the AoS loop did.

</details>

## Lab / assignment hook

[Lab 06, AoS to SoA](../labs/lab06.md). You convert the 128-byte entity to SoA and to a hot/cold split, implement the byte model as a function, pass the correctness tests, then run `bench_layouts` on your own machine and compare it with the model for your cache line size. You finish by redesigning the layout of an MMO client's entity struct for three given systems.

## Sources

- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 3, section 3.5, "Memory Architectures".
- Nystrom, R. (2014). *Game Programming Patterns*, "Data Locality" chapter. gameprogrammingpatterns.com/data-locality.html. Cache lines of about 64 to 128 bytes, misses costing hundreds of cycles, the contiguous-array version about fifty times faster, hot/cold splitting, and keeping active particles at the front.
- Acton, M. (2014). "Data-Oriented Design and C++". CppCon 2014. Slides in the CppCon 2014 GitHub repository, Presentations folder. https://github.com/CppCon/CppCon2014
- Linux kernel source, `arch/x86/Kconfig.cpu` (master branch, September 2026). `X86_L1_CACHE_SHIFT` defaults to 6 (64-byte lines) for `X86_64` and generic x86.
- Apple M4 Pro cache sizes and line size read on the reference machine with `sysctl hw.cachelinesize hw.perflevel0.l1dcachesize hw.perflevel0.l2cachesize hw.perflevel0.cpusperl2` (macOS 26, September 2026): 128-byte lines, 128 KB L1 data per performance core, 16 MB L2 shared by five performance cores.
- Unity Technologies, Entities package 1.3 manual, "Archetypes concepts". 16 KiB chunks with one array per component type plus entity IDs. https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/concepts-archetypes.html
- Bevy, `StorageType` API documentation (bevy 0.19.1, August 2026). Table storage is the default and gives fast, cache-friendly iteration. https://docs.rs/bevy/latest/bevy/ecs/component/enum.StorageType.html
- Benchmark numbers: `aos_soa.cpp` from this lecture and `bench_layouts.cpp` from lab 06's starter, Apple clang 17, `-O2` (and `-O2 -fno-vectorize -fno-slp-vectorize` for the scalar comparison), Apple M4 Pro, September 2026.

## Interactive spec: examples/w06-aos-vs-soa-cache-lines.html

**Purpose.** Make visible that a loop pays for whole cache lines, so an AoS layout with a few hot fields drags mostly unused bytes through the cache, while SoA fills every fetched line with used data. Signature example for the course: "Array-of-structs vs struct-of-arrays: iterate 1M entities, visualize cache lines".

**Layout.** Left: memory view (about 60% width on desktop). Right: numbers and bars. Stacked on mobile, memory view first. Controls above the views.

**Memory view.** A vertical stack of cache lines, each drawn as a row of cells, one cell per 4 bytes (so 16 cells for a 64-byte line, 32 for 128). Show the first 12 entities' memory (enough rows to fill the view; scroll inside the panel if needed, no page overflow). In AoS mode: each entity occupies `s / 4` consecutive cells starting at `entity × s`; hot cells (the first `h / 4` cells of each entity) in the accent colour with a per-field label on hover or focus (px, py, pz, vx, vy, vz); cold cells neutral grey. In SoA mode: the same number of entities re-drawn as `h / 4` separate dense arrays (one per hot float field), each starting on a new line, all cells coloured, followed by a note "cold fields: separate arrays, never touched". A loop cursor steps entity by entity (Play/Pause, Step buttons, speed slider). Each line the cursor touches for the first time gets a bold outline and a "fetched" tint; a counter shows lines fetched and bytes fetched so far, and bytes used so far.

**Numbers and bars.** For the chosen `N` (default 1,000,000): `B_AoS`, `B_SoA`, useful fraction AoS `u = h / B_AoS` (as %), traffic AoS and SoA in MB (`N × B / 1e6`), predicted speed-up `B_AoS / B_SoA`, and predicted time for each layout at a bandwidth slider value (`time_ms = N × B / (bandwidth_GBps × 1e6)`). Two horizontal bars for traffic, drawn to the same scale. Below, a small static table of the lecture's measured results (the four-row N table) with a caption "measured on the reference machine; the model predicts the jump between 100,000 and 1,000,000".

**Controls.**
- Layout toggle: AoS / SoA (both views update; the bars always show both).
- Line size `L`: 64 or 128 bytes (default 128).
- Struct size `s`: 16 to 256 bytes, step 4 (default 128).
- Hot bytes `h`: 4 to `s`, step 4 (default 24).
- Entities `N`: 10,000 / 100,000 / 1,000,000 / 10,000,000 (default 1,000,000).
- Bandwidth: 10 to 200 GB/s (default 30).
- Presets: "Lecture entity" (s 128, h 24, L 128), "x86 line" (s 128, h 24, L 64), "Small struct" (s 48, h 16, L 64), "Every field" (s 128, h 128, L 128).

**Model (exact).** If `s ≥ L`: `B_AoS = L × ceil(h / L)`. Else `B_AoS = s`. `B_SoA = h`. When `s` is not a multiple of `L` and `s ≥ L`, still use the formula but show a note "some entities straddle lines; real cost is higher".

**The one insight.** With the Lecture entity preset, the memory view shows each fetched 128-byte line with 6 coloured cells and 26 grey ones in AoS, and fully coloured lines in SoA. Switching `L` from 128 to 64 halves the grey per line and the predicted speed-up drops from 5.3× to 2.7×. Caption: "The loop is the same. The grey is what you pay for and never use."

**Test values.**
- s 128, h 24, L 128, N 1,000,000: B_AoS 128, B_SoA 24, u 18.75%, traffic 128 MB vs 24 MB, speed-up 5.33×. At 30 GB/s: 4.27 ms vs 0.80 ms.
- s 128, h 24, L 64: B_AoS 64, u 37.5%, traffic 64 MB, speed-up 2.67×.
- s 96, h 16, L 64, N 2,000,000: B_AoS 64, B_SoA 16, u 25%, 128 MB vs 32 MB, 4×.
- s 48, h 16, L 64: B_AoS 48, speed-up 3×.
- s 128, h 128, L 128: speed-up 1×.

**Accessibility.** All controls keyboard operable with visible focus; the Step button advances the cursor one entity per press. Cells are not individually focusable, but each line row has an accessible label ("line 3: 6 of 32 cells used, fetched"). A live region reports the counters on each step. Hot versus cold uses fill plus a pattern (hot cells solid, cold cells dotted) so colour is not the only cue. With `prefers-reduced-motion`, Play advances without animation.
