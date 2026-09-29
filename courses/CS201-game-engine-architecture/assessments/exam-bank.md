# CS201 · Exam bank: quiz, practice and viva questions

CS201 has no written exam. The grade comes from the subsystem labs (50%, see [subsystem-labs-brief.md](subsystem-labs-brief.md)) and the final engine (50%, see [final-engine-brief.md](final-engine-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session from week 2 opens with a 10-minute ungraded quiz of two questions from this bank, usually one compute or trace question and one explain or critique question.
- **Viva.** The lab spot checks and the week 15 engine viva ask questions in this style, rewritten with your own code, your own profiler captures and your own numbers.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model (port share, relocations, fragmentation, frame budget, cache lines, load time, switches, miss rate, crossings, sleep, migrations, profiler error, code sites) to numbers you have not seen before.
- **trace**: say exactly what a piece of C++ or Python prints, and why.
- **code**: write or fix a short function so it prints a stated result.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or setting for a stated situation and justify it.
- **critique**: find what is wrong with a piece of code or a plan and say how to fix it.

All numbers are invented unless a question names a game or a library. Every fact about a real game, engine or library comes from the lecture of the tagged week, which cites its source and version. Every C++ program compiles with `clang++ -std=c++17` and prints the output given in the answer; the outputs were produced with Apple clang 17 and libc++, and every vector growth count is the same on GCC's libstdc++. Every Python program runs as shown with Python 3.13 (`.venv/bin/python`). Every number in an answer was recomputed from the lecture's own model. Write your own answer before you open the solution.

---

## Week 1: Engine anatomy and runtime layers

1. *Week 1 · compute.* An engine has 120,000 lines. Its platform layer is 4,800 lines. Three files outside it include OS headers: a 1,500-line config loader, a 2,700-line crash reporter and a 900-line screenshot tool.
   (a) What are the port size, the port share and the factor by which the leaks multiply the port size?
   (b) You move the crash reporter's OS calls into the platform layer, which adds 60 lines of wrapper functions there. Recompute all three numbers, using the new total.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 9,900 lines, 8.3%, 2.1×. (b) 7,260 lines, 6.0%, 1.5×.

(a) Port size is the platform layer plus every whole file that leaks: `4,800 + 1,500 + 2,700 + 900 = 9,900` lines. Port share is `9,900 / 120,000 = 8.25%`. The multiplier is `9,900 / 4,800 = 2.06`.

(b) The platform layer grows to 4,860 lines and the total to 120,060. The crash reporter no longer touches the OS, so it leaves the port size entirely: `4,860 + 1,500 + 900 = 7,260` lines. Share `7,260 / 120,060 = 6.05%`. Multiplier `7,260 / 4,860 = 1.49`.

Sixty lines added below saved 2,640 lines a porter must read above. A leak costs the size of the file it lands in, not the size of the call.
</details>

2. *Week 1 · trace.* This is the start-up rule from Lab 01: repeatedly place the alphabetically first module whose needs are all placed. What does the program print? The second answer names eight modules. How many of them are really in the cycle, and why does the message name the others?

```python
def start_order(needs):
    placed, order = set(), []
    while len(order) < len(needs):
        ready = sorted(m for m in needs
                       if m not in placed and all(n in placed for n in needs[m]))
        if not ready:
            raise ValueError("cycle among " + ", ".join(sorted(set(needs) - placed)))
        order.append(ready[0])          # alphabetically first ready module
        placed.add(ready[0])
    return order

needs = {
    "audio": ["files", "memory"], "files": ["memory"], "input": ["window"],
    "log": ["memory"], "memory": [], "renderer": ["files", "window"],
    "script": ["files", "log"], "window": ["memory"],
}
print(start_order(needs))
needs["memory"] = ["log"]
try:
    print(start_order(needs))
except ValueError as e:
    print(e)
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
['memory', 'files', 'audio', 'log', 'script', 'window', 'input', 'renderer']
cycle among audio, files, input, log, memory, renderer, script, window
```

Trace the first call. Only `memory` needs nothing. Then `files`, `log` and `window` are ready, and `files` is first alphabetically. After `files`, the ready set is `audio`, `log`, `window`, so `audio` goes. Then `log`, which makes `script` ready (it needs `files` and `log`). `script` beats `window`. Then `window`, which makes `input` and `renderer` ready, in that order.

In the second call `memory` needs `log` and `log` needs `memory`. Nothing is ready on the first pass, so the function reports every unplaced module, all eight. Only two are in the cycle. The other six are merely stuck behind it. A better checker would walk the unresolved needs from any stuck module until it revisits one, and report only that loop (`memory -> log -> memory`). The fix is a design change, as in the lecture: let the log write early lines to a static buffer so it needs nothing below it.
</details>

3. *Week 1 · trace.* The platform layer hands key presses to the game through a function-pointer slot, as in lecture section 4. What does this print? Which file would include which header if the two layers were split into files? Suggest one change so the first key press is not lost.

```cpp
#include <cstdio>

// ---- platform layer ----
struct Event { int key; };
using EventSink = void (*)(const Event&);
static EventSink g_sink = nullptr;
static int g_dropped = 0;

void platform_set_event_sink(EventSink sink) { g_sink = sink; }
void platform_report(int key) {            // the OS reported a key press
    Event e{key};
    if (g_sink) g_sink(e);
    else ++g_dropped;
}

// ---- game layer ----
static int g_moves = 0;
void game_on_event(const Event& e) {
    if (e.key == 'W') ++g_moves;
    std::printf("game got %c\n", e.key);
}

int main() {
    platform_report('A');
    platform_set_event_sink(game_on_event);
    platform_report('W');
    platform_report('W');
    platform_set_event_sink(nullptr);
    platform_report('S');
    std::printf("moves=%d dropped=%d\n", g_moves, g_dropped);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
game got W
game got W
moves=2 dropped=2
```

`A` arrives before the game plugs in, and `S` after it unplugs, so both are counted as dropped. The two `W` presses reach the game.

The game file includes the platform header, because it calls `platform_set_event_sink` and uses `Event`. The platform file names only its own types, so it includes nothing from the game. At run time the call goes upward; at compile time the arrow points down, which is what the dependency rule cares about.

To keep early presses, put a small queue in the platform layer (Doom's 64-slot ring buffer, moved down a layer). `platform_report` pushes into it, and the game drains it once per frame. Events that arrive before the game starts wait in the queue instead of vanishing, and week 9 gets timestamps and replay for free.
</details>

4. *Week 1 · critique.* A teammate's pull request adds `#include "game/settings.h"` to `platform/audio.cpp` so the mixer can read `Settings::master_volume` every buffer. Name the rule it breaks, two costs it creates that you can measure, and a fix that needs no call from the platform layer into the game at all.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It is an upward dependency from layer 0 to the game layer. Replace it with a downward setter, `platform_audio_set_master_volume(float)`, that the game calls when the setting changes.

The dependency rule says code may name only its own layer and the layers below it. Two measurable costs follow.

- **Rebuilds.** Every change to `settings.h` now recompiles the audio driver, and every other platform file that later includes `audio.h` transitively.
- **Port size.** A porter rewriting the audio driver must now read `settings.h` and whatever it includes. If a checker like Lab 01's flags the include, the port share no longer describes the real work.

A function-pointer slot would work, but here a setter is simpler. The platform layer stores one float. The game calls the setter at start-up and whenever the options menu changes the volume. No call ever goes upward, even at run time, and the mixer reads a local float instead of a game object on every buffer.
</details>

## Week 2: C++ for engines: memory, RAII, move semantics

5. *Week 2 · compute.* An MMO client pushes 3,000 item icons of 16 KiB each into an empty `std::vector` without `reserve`. Each icon object is 24 bytes (three pointers). Use the lecture's relocation model.
   (a) With libc++ or libstdc++ (doubling), give the number of reallocations, the relocations `R(n)`, the final capacity, and the bytes moved when the move constructor is and is not `noexcept`.
   (b) Repeat for Microsoft's STL (`capacity + capacity / 2`).
   (c) What do all four byte counts become after `reserve(3000)`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 13 reallocations, `R = 4,095`, capacity 4,096; copy 67,092,480 bytes (63.98 MiB), move 98,280 bytes (95.98 KiB). (b) 21 reallocations, `R = 7,200`, capacity 3,597; copy 117,964,800 bytes (112.5 MiB), move 172,800 bytes (168.75 KiB). (c) All zero.

(a) The vector is full at sizes 1, 2, 4, ..., 2,048, so `R = 4,096 − 1 = 4,095`, over 13 reallocations counting the first allocation. Copying costs the payload: `4,095 × 16,384 = 67,092,480` bytes. Moving costs only the object: `4,095 × 24 = 98,280` bytes.

(b) Run the lecture's `relocations(3000, lambda c: c + c // 2)` and it returns `(21, 7200, 3597)`. Then `7,200 × 16,384 = 117,964,800` and `7,200 × 24 = 172,800`.

(c) With the capacity set first, the vector never fills, so nothing relocates. The container decides how many elements move; the element type decides what each move costs; `reserve` removes the first factor entirely.
</details>

6. *Week 2 · trace.* What does this print with libc++ or libstdc++? Explain the difference between `B` and `C`, and give the smallest change to `C` that makes its line match `B`'s.

```cpp
#include <cstdio>
#include <vector>

static int copies = 0, moves = 0;
struct A {
    A() {}
    A(const A&) { ++copies; }
    A(A&&) noexcept { ++moves; }
};
struct B { A a; };                 // writes none of the five
struct C { A a; ~C() {} };         // "just a destructor, for a breakpoint"

template <class T> void run(const char* name, int n, bool reserve) {
    copies = moves = 0;
    std::vector<T> v;
    if (reserve) v.reserve(n);
    for (int i = 0; i < n; ++i) v.emplace_back();
    std::printf("%s n=%d reserve=%d copies=%d moves=%d\n", name, n, reserve, copies, moves);
}

int main() {
    run<B>("B", 20, false);
    run<C>("C", 20, false);
    run<C>("C", 20, true);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
B n=20 reserve=0 copies=0 moves=31
C n=20 reserve=0 copies=31 moves=0
C n=20 reserve=1 copies=0 moves=0
```

Twenty pushes into an empty vector reallocate when it is full at sizes 1, 2, 4, 8 and 16, so `1 + 2 + 4 + 8 + 16 = 31` elements are relocated. `emplace_back` builds each new element in place, so the new element is never copied or moved.

`B` follows the rule of zero. Its generated move constructor moves `a`, and since `A`'s move is `noexcept`, so is `B`'s. The vector moves all 31.

`C` has a user-declared destructor, which stops the compiler from generating a move constructor. The copy constructor is still generated, so the only way to relocate a `C` is to copy it, 31 times. With `reserve(20)` nothing relocates at all.

Smallest fix: add `C(C&&) noexcept = default;`. Declaring it also removes the implicit copy constructor, so if you still need copies add `C(const C&) = default;` and the two assignments. Better still, delete the empty destructor and set the breakpoint elsewhere.
</details>

7. *Week 2 · trace.* What does each numbered line print? Explain line 1 and line 4.

```cpp
#include <cstdio>
#include <utility>

struct Tracker {
    Tracker() {}
    Tracker(const Tracker&) { std::puts("copy"); }
    Tracker(Tracker&&) noexcept { std::puts("move"); }
};

int main() {
    const Tracker a;
    Tracker b = std::move(a);   // line 1
    Tracker c;
    Tracker d = std::move(c);   // line 2
    Tracker e = d;              // line 3
    Tracker f = Tracker();      // line 4
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
copy
move
copy
```

Line 1 prints `copy`. `std::move` is only a cast. Applied to a `const Tracker` it gives a `const Tracker&&`, which cannot bind to the move constructor's `Tracker&&` parameter, because moving would modify a const object. It can bind to `const Tracker&`, so overload resolution picks the copy constructor, and nothing warns you.

Line 2 prints `move`, line 3 prints `copy`.

Line 4 prints nothing. Since C++17, initializing an object from a temporary of the same type constructs it directly in place. No copy or move constructor runs at all. This is the same rule that makes returning a local by value cheap, and why `return std::move(local);` is never an improvement.
</details>

8. *Week 2 · trace.* The pretend GPU API below counts live textures and destroys of ids that are already dead. What does the program print? Explain every call to `gpu_destroy`, then fix `Texture` so it prints `live=0 errors=0`.

```cpp
#include <cstdio>
#include <vector>

// A pretend GPU API that counts live textures and bad destroys.
static bool g_alive[64];
static int g_live = 0, g_errors = 0, g_next = 1;
int gpu_create() { g_alive[g_next] = true; ++g_live; return g_next++; }
void gpu_destroy(int id) {
    if (id <= 0 || !g_alive[id]) { ++g_errors; return; }
    g_alive[id] = false;
    --g_live;
}

struct Texture {
    int id;
    Texture() : id(gpu_create()) {}
    ~Texture() { gpu_destroy(id); }
};

int main() {
    {
        std::vector<Texture> v;
        v.emplace_back();
        v.emplace_back();           // capacity 1 is full: the vector grows
    }
    std::printf("live=%d errors=%d\n", g_live, g_errors);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
live=0 errors=1
```

The first element creates id 1. The second push finds the vector full. The new element creates id 2, and the old element must be relocated. `Texture` has a user-declared destructor, so it has no move constructor, and the compiler-generated copy constructor copies the integer. Now two objects hold id 1. The old one is destroyed: `gpu_destroy(1)` succeeds and `live` drops to 1. At the closing brace both elements die: `gpu_destroy(1)` again, which is an error, then `gpu_destroy(2)`, which brings `live` to 0.

`live=0` looks healthy. The error count shows the double destroy. In a real driver id 1 may already belong to another texture, which this destroy would free.

The fix follows the rule of five for a move-only owner:

```cpp
#include <cstdio>
#include <vector>

static bool g_alive[64];
static int g_live = 0, g_errors = 0, g_next = 1;
int gpu_create() { g_alive[g_next] = true; ++g_live; return g_next++; }
void gpu_destroy(int id) {
    if (id <= 0 || !g_alive[id]) { ++g_errors; return; }
    g_alive[id] = false;
    --g_live;
}

struct Texture {
    int id;
    Texture() : id(gpu_create()) {}
    ~Texture() { if (id != 0) gpu_destroy(id); }
    Texture(const Texture&) = delete;
    Texture& operator=(const Texture&) = delete;
    Texture(Texture&& o) noexcept : id(o.id) { o.id = 0; }
    Texture& operator=(Texture&& o) noexcept {
        if (this != &o) { if (id != 0) gpu_destroy(id); id = o.id; o.id = 0; }
        return *this;
    }
};

int main() {
    {
        std::vector<Texture> v;
        v.emplace_back();
        v.emplace_back();
    }
    std::printf("live=%d errors=%d\n", g_live, g_errors);
}
```

```text
live=0 errors=0
```

The moved-from element holds id 0, and its destructor does nothing. Deleting the copy constructor turns any future accidental copy into a compile error instead of a runtime double free.
</details>

## Week 3: Memory allocators: stack, pool, frame

9. *Week 3 · compute.* A 60 MiB arena starts empty. A level loads five files, each as (read buffer, asset) in MiB: (3, 5), (4, 6), (2, 7), (6, 4), (5, 8). Each buffer is placed, then its asset, then the buffer is freed.
   (a) Trace first fit on one heap. Give every final asset position, the free runs, total free, the largest run and the fragmentation.
   (b) Does a 25 MiB streaming buffer fit afterwards?
   (c) Repeat (a) and (b) with two ends: assets packed down from the top, buffers at the bottom, reset after each file.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Assets at 3-8, 12-18, 18-25, 8-12 and 30-38. Free runs 3, 5 and 22 MiB, total 30, largest 22, fragmentation 27%. (b) No. (c) Assets at 55-60, 49-55, 42-49, 38-42, 30-38; one free run of 30 MiB, fragmentation 0%; the 25 MiB buffer fits at 0-25.

| File | Buffer at | Asset at | Hole left by the buffer |
|---|---|---|---|
| 1 (3, 5) | 0-3 | 3-8 | 0-3 |
| 2 (4, 6) | 8-12 (4 does not fit in 0-3) | 12-18 | 8-12 |
| 3 (2, 7) | 0-2 | 18-25 | 0-3 again |
| 4 (6, 4) | 25-31 | 8-12 (fits the hole file 2 left) | 25-31, which joins the tail |
| 5 (5, 8) | 25-30 | 30-38 | 25-30 |

Used: `5 + 6 + 7 + 4 + 8 = 30` MiB. Free: 0-3, 25-30 and 38-60, so 3, 5 and 22 MiB. Fragmentation `1 − 22/30 = 26.7%`. A 25 MiB request fails with 30 MiB free. Notice that file 4's small asset filled an old hole. First fit is not always bad; it depends on the order of sizes.

With two ends the assets stack down from 60: 55-60, 49-55, 42-49, 38-42, 30-38. The bottom is empty after the last reset, so 0-30 is one run and fragmentation is 0%.
</details>

10. *Week 3 · compute.* A stack allocator's base is 16-byte aligned and `top` starts at 0. Six requests arrive as (bytes, alignment): (6, 2), (16, 16), (4, 4), (1, 1), (12, 8), (2, 2).
    (a) Give each returned offset, the final `top` and the total padding.
    (b) Reorder the same requests from largest alignment to smallest, keeping sizes that are multiples of their alignment first. Give the new offsets and padding.
    (c) In the original order, a marker is taken right after the (4, 4) request. After `free_to(marker)`, where does a new (8, 8) request land?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Offsets 0, 16, 32, 36, 40, 52; `top` 54; 13 bytes of padding. (b) Order (16, 16), (12, 8), (4, 4), (6, 2), (2, 2), (1, 1) at offsets 0, 16, 28, 32, 38, 40; `top` 41; no padding. (c) At offset 40, and `top` becomes 48.

(a) Use `aligned = (top + a − 1) & ~(a − 1)`.

| Request | `top` before | Rounded to | Padding | `top` after |
|---|---|---|---|---|
| 6 B, align 2 | 0 | 0 | 0 | 6 |
| 16 B, align 16 | 6 | 16 | 10 | 32 |
| 4 B, align 4 | 32 | 32 | 0 | 36 |
| 1 B, align 1 | 36 | 36 | 0 | 37 |
| 12 B, align 8 | 37 | 40 | 3 | 52 |
| 2 B, align 2 | 52 | 52 | 0 | 54 |

That is 13 bytes of padding for 41 bytes of data, 24% of the space used.

(b) Each block ends on a boundary that satisfies the next alignment: 16 ends at 16, 12 ends at 28 (a multiple of 4), 4 ends at 32, 6 ends at 38 (even), 2 ends at 40, and 1 byte needs no alignment.

(c) The marker saves `top = 36`. After `free_to(36)`, 36 rounds up to 40 for alignment 8, so the block sits at 40-48.
</details>

11. *Week 3 · trace.* This pool hands out slot indices with the lecture's LIFO free list. What does it print?

```cpp
#include <cstdio>
#include <vector>

// A pool of n slots that hands out slot indices. Free slots are linked
// through next_, the same LIFO free list as the lecture's PoolAllocator.
class IndexPool {
    std::vector<int> next_;
    int head_ = 0;
public:
    explicit IndexPool(int n) : next_(n) {
        for (int i = 0; i < n; ++i) next_[i] = (i + 1 < n) ? i + 1 : -1;
    }
    int alloc() {
        if (head_ < 0) return -1;
        int i = head_;
        head_ = next_[i];
        return i;
    }
    void free(int i) { next_[i] = head_; head_ = i; }
};

int main() {
    IndexPool pool(5);
    int a = pool.alloc(), b = pool.alloc(), c = pool.alloc();
    pool.free(a);
    pool.free(c);
    int d = pool.alloc(), e = pool.alloc(), f = pool.alloc();
    int g = pool.alloc(), h = pool.alloc();
    std::printf("a=%d b=%d c=%d d=%d e=%d f=%d g=%d h=%d\n", a, b, c, d, e, f, g, h);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
a=0 b=1 c=2 d=2 e=0 f=3 g=4 h=-1
```

The list starts `0 → 1 → 2 → 3 → 4`. Three pops give 0, 1 and 2, and the head is 3. Freeing 0 pushes it: `0 → 3 → 4`. Freeing 2 pushes it: `2 → 0 → 3 → 4`. The next four pops return 2, 0, 3 and 4 in that order, and the fifth finds the list empty.

The block freed last comes out first. That is why the lecture calls the pool cache-friendly: the most recently freed block is the one most likely still in cache.
</details>

12. *Week 3 · design.* Use the lecture's pool rule (block size at least 8 bytes, rounded up to a multiple of 16).
    (a) Give the block size and internal fragmentation for pools of 44-byte projectiles, 72-byte decals, 100-byte network messages and 8-byte handles. How many bytes does a pool of 4,096 decals take?
    (b) Choose an allocator from section 6's table for: the font atlas, a level's navmesh, the list of entities a raycast hit this frame, chat message strings, and projectiles.
    (c) A double-buffered frame allocator is used in frames numbered 10, 11, 12. At the start of frame 12, which stack is reset, and which frame's data is still valid?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 48 bytes (8.3%), 80 bytes (10%), 112 bytes (10.7%), 16 bytes (50%); 327,680 bytes. (b) Permanent top of a double-ended stack; level stack with a marker; frame allocator; a separate general heap; a pool. (c) The stack used in frame 10 is reset; frame 11's data stays valid through frame 12.

(a) `44 → 48`, waste `4/48`. `72 → 80`, waste `8/80`. `100 → 112`, waste `12/112`. An 8-byte handle already holds the free-list pointer but rounds up to 16, wasting half. Decal pool: `4,096 × 80 = 327,680` bytes. A pool of pure handles deserves its own rounding rule (8 bytes, 8-aligned), which the lecture recommends: pools are sized per type.

(b) The atlas lives for the whole run. The navmesh dies with the level, all at once. Raycast results die at the end of the frame. Chat strings are any size and freed in any order, so they go on a general heap kept apart from the level's memory. Projectiles are one size, created and destroyed one at a time.

(c) At the start of frame N the allocator resets the stack used in frame N − 2 and makes it current. Anything allocated in frame 11 survives through frame 12, which is what lets the GPU keep reading frame 11's command list. A pointer from frame 10 read in frame 12 points at overwritten memory; the debug fill pattern (`0xCD`) makes that visible.
</details>

## Week 4: The frame: update, render, present

13. *Week 4 · compute.* A frame at 60 Hz has CPU stages input 0.4, gameplay 5.3, physics 2.9, animation 1.9 and render preparation 3.6 ms, and GPU time 13.8 ms.
    (a) Give `C`, the serial and pipelined work intervals, what the player sees in each case, the bottleneck and both headrooms.
    (b) By how much can gameplay grow before the pipelined frame rate drops?
    (c) The same pipelined game on a 144 Hz display and on a 90 Hz display: what does the player see on each?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `C = 14.1` ms. Serial `W = 27.9` ms, shown 33.33 ms (30 fps). Pipelined `W = 14.1` ms, shown 16.67 ms (60 fps). CPU-bound, with 2.57 ms of CPU headroom and 2.87 ms of GPU headroom. (b) Just under 2.57 ms. (c) 20.83 ms (48 fps) at 144 Hz; 22.22 ms (45 fps) at 90 Hz.

(a) `C = 0.4 + 5.3 + 2.9 + 1.9 + 3.6 = 14.1`. Serial `W = 14.1 + 13.8 = 27.9`, and `ceil(27.9 / 16.67) = 2` refreshes. Pipelined `W = max(14.1, 13.8) = 14.1`, one refresh. Headroom is `16.67 − 14.1` and `16.67 − 13.8`.

(b) The frame stays at one refresh while `C ≤ 16.67`, so gameplay may add up to `16.67 − 14.1 = 2.57` ms, and one microsecond more halves the frame rate.

(c) At 144 Hz, `T = 6.94` ms and `14.1 / 6.94 = 2.03`, so 3 refreshes: 20.83 ms. At 90 Hz, `T = 11.11` ms and `14.1 / 11.11 = 1.27`, so 2 refreshes: 22.22 ms. The faster 90 Hz display shows fewer frames per second than the 60 Hz one, because the rounding cliff sits at 11.11 ms instead of 16.67 ms.
</details>

14. *Week 4 · trace.* This is the lecture's queue simulator with a work time per frame. Frame 2 takes 24 ms, the rest 10 ms. What does it print? Which depth shows a frame for longer than 16.67 ms, and what does the other depth pay instead?

```cpp
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>

struct Frame { double start, ready, shown; };

// The lecture's three rules, with a different work time per frame.
std::vector<Frame> simulate(const std::vector<double>& work, double hz, int depth, int interval) {
    const double T = 1000.0 / hz;
    std::vector<Frame> f(work.size());
    for (std::size_t i = 0; i < work.size(); ++i) {
        double s = (i == 0) ? 0.0 : f[i - 1].ready;                          // rule 1
        if (i >= std::size_t(depth)) s = std::max(s, f[i - depth].shown);
        double r = s + work[i];                                              // rule 2
        double v = T * std::ceil(r / T - 1e-9);                              // rule 3
        if (i > 0) v = std::max(v, f[i - 1].shown + interval * T);
        f[i] = {s, r, v};
    }
    return f;
}

int main() {
    std::vector<double> work = {10, 10, 24, 10, 10, 10};
    for (int depth : {1, 2}) {
        auto f = simulate(work, 60, depth, 1);
        std::printf("depth %d\n", depth);
        for (std::size_t i = 0; i < f.size(); ++i)
            std::printf("  frame %zu start %6.2f ready %6.2f shown %6.2f latency %5.2f\n",
                        i, f[i].start, f[i].ready, f[i].shown, f[i].shown - f[i].start);
    }
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
depth 1
  frame 0 start   0.00 ready  10.00 shown  16.67 latency 16.67
  frame 1 start  16.67 ready  26.67 shown  33.33 latency 16.67
  frame 2 start  33.33 ready  57.33 shown  66.67 latency 33.33
  frame 3 start  66.67 ready  76.67 shown  83.33 latency 16.67
  frame 4 start  83.33 ready  93.33 shown 100.00 latency 16.67
  frame 5 start 100.00 ready 110.00 shown 116.67 latency 16.67
depth 2
  frame 0 start   0.00 ready  10.00 shown  16.67 latency 16.67
  frame 1 start  10.00 ready  20.00 shown  33.33 latency 23.33
  frame 2 start  20.00 ready  44.00 shown  50.00 latency 30.00
  frame 3 start  44.00 ready  54.00 shown  66.67 latency 22.67
  frame 4 start  54.00 ready  64.00 shown  83.33 latency 29.33
  frame 5 start  66.67 ready  76.67 shown 100.00 latency 33.33
```

With depth 1 every frame waits for the previous one to reach the screen (rule 1), so it starts on a vblank. Frame 2 starts at 33.33, is ready at 57.33, and misses the 50.00 vblank. Frame 1 stays on screen from 33.33 to 66.67, a 33.33 ms frame the player sees as a hitch. Latency is 16.67 ms everywhere else.

With depth 2 the engine runs ahead. Frames 0 and 1 are finished early, so when frame 2 is slow there is already a queued image for each vblank, and a new image appears at every one of them. The spike is hidden. The price is latency: it climbs from 16.67 to 33.33 ms and stays there once the queue is full, as in the lecture's `W = 12` trace. A deeper queue trades a rare hitch for extra delay on every frame.
</details>

15. *Week 4 · compute.* An engine needs `W = 20` ms per frame on a 60 Hz FIFO display. Using the three rules, give the steady-state frame rate, the on-screen times and the latency range for (a) `Q = 1, S = 1`, (b) `Q = 2, S = 1`, (c) `Q = 2, S = 2`. Which would you ship for a platformer that cannot reach `W < 16.67`, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 30 fps, every frame 33.33 ms, latency 33.33 ms. (b) 50 fps, frames of 16.67 ms four times then one of 33.33 ms, latency 20.00 to 33.33 ms. (c) 30 fps, every frame 33.33 ms, latency 66.67 ms. Ship (a).

(a) With `Q = 1` a frame starts only when the previous one is on screen, so it starts on a vblank, finishes 20 ms later, misses the next vblank, and appears at the one after: `start + 33.33`.

(b) With `Q = 2` the engine never waits for a buffer. It finishes a frame every 20 ms, while the display shows one every 16.67 ms. Five frames take 100 ms and six vblanks pass, so one frame stays up twice as long in every group of five: 50 fps on average, with a judder every 100 ms.

(c) `S = 2` forces even 33.33 ms frames, but the queue now holds two images each shown for two refreshes, so latency is `2 × 33.33 = 66.67` ms.

For a platformer, (a) gives the same even 30 fps as (c) with half the latency, and none of (b)'s judder. The lecture's rule: if you cannot hold `W < T`, choose even frames on purpose, and keep the queue short when input matters.
</details>

16. *Week 4 · critique.* A fighting game needs `W = 9` ms per frame at 60 Hz. A teammate set the swap chain queue to 3 "so we never drop a frame", and testers say parries feel late. Compute the steady-state latency the teammate's setting gives and the latency at `Q = 1`. What does the deeper queue buy, and how would you get that benefit without paying for it on every frame?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 50.00 ms at `Q = 3` against 16.67 ms at `Q = 1`, both at a steady 60 fps. The deeper queue only helps on frames that spike above 16.67 ms.

When the engine is faster than the display, it fills the queue and then waits at present for a free buffer. Latency becomes `Q × T`: `3 × 16.67 = 50.00` ms. The frame counter reads 60 in both cases, so nothing in a plain fps overlay shows the 33 ms the teammate added.

The queue buys spike absorption: a slow frame drains a queued image instead of missing a vblank (question 14). You can keep most of that without the constant cost. Use `Q = 1` or `Q = 2`, and remove the spikes at their source with week 13's profiler. The lecture's advice for action games is to cap the queue at 1 or 2.
</details>

## Week 5: Entity-component-system design

17. *Week 5 · trace.* This is the lecture's sparse set for a tag component with no data. What does it print? In the last step the removed entity is the last element of `dense`. Why does `remove` still work, and which line order makes it work?

```cpp
#include <cstdint>
#include <cstdio>
#include <vector>

constexpr std::uint32_t NONE = UINT32_MAX;

struct SparseSet {                                 // the lecture's pool, tag component only
    std::vector<std::uint32_t> sparse, dense;
    void add(std::uint32_t e) {
        if (e >= sparse.size()) sparse.resize(e + 1, NONE);
        sparse[e] = std::uint32_t(dense.size());
        dense.push_back(e);
    }
    void remove(std::uint32_t e) {                 // swap-and-pop
        std::uint32_t slot = sparse[e], last = dense.back();
        dense[slot] = last;
        sparse[last] = slot;
        dense.pop_back();
        sparse[e] = NONE;
    }
};

void show(const char* step, const SparseSet& s) {
    std::printf("%-10s dense [", step);
    for (auto e : s.dense) std::printf(" %u", e);
    std::printf(" ]  sparse [");
    for (auto x : s.sparse) x == NONE ? std::printf(" -") : std::printf(" %u", x);
    std::printf(" ]\n");
}

int main() {
    SparseSet burning;
    burning.add(2);    show("add 2", burning);
    burning.add(0);    show("add 0", burning);
    burning.add(5);    show("add 5", burning);
    burning.remove(2); show("remove 2", burning);
    burning.add(3);    show("add 3", burning);
    burning.remove(3); show("remove 3", burning);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
add 2      dense [ 2 ]  sparse [ - - 0 ]
add 0      dense [ 2 0 ]  sparse [ 1 - 0 ]
add 5      dense [ 2 0 5 ]  sparse [ 1 - 0 - - 2 ]
remove 2   dense [ 5 0 ]  sparse [ 1 - - - - 0 ]
add 3      dense [ 5 0 3 ]  sparse [ 1 - - 2 - 0 ]
remove 3   dense [ 5 0 ]  sparse [ 1 - - - - 0 ]
```

`sparse` grows only to the highest index added so far, which is why it has three entries after `add 2` and six after `add 5`. Removing 2 (slot 0) moves the last element, 5, into slot 0 and updates `sparse[5]`.

When 3 is removed it is its own `last`. The code writes `dense[2] = 3` and `sparse[3] = 2`, which change nothing, then pops, then sets `sparse[3] = NONE`. It works because `sparse[e] = NONE` comes after `sparse[last] = slot`. Swap those two lines and the removed entity would be marked present again in slot 2, which no longer exists.
</details>

18. *Week 5 · trace and compute.* (a) What does this generational pool print? (b) EnTT's default identifier packs a 20-bit index and a 12-bit version into 32 bits. With the index in the low bits, what integer encodes index 1,000 at version 5? How many live entities can it address, and after how many recycles of one slot does a stale handle pass the check again?

```python
class EntityPool:                          # the lecture's pool, in Python
    def __init__(self):
        self.gen, self.free = [], []
    def create(self):
        if self.free:
            i = self.free.pop()            # LIFO: the last index freed comes back first
            return (i, self.gen[i])
        self.gen.append(0)
        return (len(self.gen) - 1, 0)
    def destroy(self, e):
        self.gen[e[0]] += 1
        self.free.append(e[0])
    def alive(self, e):
        return e[0] < len(self.gen) and self.gen[e[0]] == e[1]

pool = EntityPool()
e = [pool.create() for _ in range(4)]
pool.destroy(e[1])
pool.destroy(e[3])
x = pool.create()
pool.destroy(x)
y = pool.create()
z = pool.create()
print("x", x, "y", y, "z", z)
print([pool.alive(h) for h in (e[1], e[3], x, y, z)])
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
x (3, 1) y (3, 2) z (1, 1)
[False, False, False, True, True]
```

(a) The four entities are `(0,0)` to `(3,0)`. Destroying 1 then 3 leaves the free list `[1, 3]` and both generations at 1. `x` pops 3 and gets `(3, 1)`. Destroying `x` raises slot 3 to generation 2 and pushes 3 again. `y` pops 3 as `(3, 2)` and `z` pops 1 as `(1, 1)`. Slot 3 has held three different entities, and only the newest handle passes `alive`.

(b) `5 × 2^20 + 1,000 = 5,242,880 + 1,000 = 5,243,880`. Twenty bits give `2^20 = 1,048,576` indices. Twelve bits give 4,096 versions, so a stale handle passes the check again after its slot has been recycled 4,096 times while it was held. That is rare, and it is why saves and network messages use separate persistent IDs (week 12).
</details>

19. *Week 5 · compute.* On your machine, one archetype toggle of a tag costs 50 ns and one sparse-set toggle 8 ns. Your game has three join systems. Each costs 0.030 ms per frame on archetype tables and 0.120 ms on sparse sets.
    (a) What is the break-even number of toggles per frame?
    (b) Give both layouts' per-frame totals at 2,000 and at 10,000 toggles.
    (c) A unit's components total 160 bytes. How many bytes does the archetype layout move for 2,000 toggles, by the lecture's byte model?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 6,400 toggles per frame. (b) At 2,000: archetype 0.190 ms, sparse set 0.376 ms. At 10,000: archetype 0.590 ms, sparse set 0.440 ms. (c) 640,000 bytes.

(a) Archetypes save `3 × (0.120 − 0.030) = 0.270` ms per frame on joins and lose `50 − 8 = 42` ns per toggle. They stay ahead while `toggles × 42 ns < 0.270 ms`, so up to `270,000 / 42 = 6,429` toggles.

(b) Archetype `3 × 0.030 + t × 50 ns`, sparse `3 × 0.120 + t × 8 ns`. At 2,000 toggles: `0.090 + 0.100 = 0.190` against `0.360 + 0.016 = 0.376`. At 10,000: `0.090 + 0.500 = 0.590` against `0.360 + 0.080 = 0.440`.

(c) Each toggle copies the row in and moves the last row into the hole, `2 × 160 = 320` bytes, so `2,000 × 320 = 640,000` bytes per frame. The sparse set moves about 8 bytes per toggle, 16,000 bytes in all.
</details>

20. *Week 5 · design.* For a small MMO, choose archetype column, sparse set or enable flag for each component, and give the reason in one line with "changes per second" and "systems that join it": `Transform` (every unit), `Mesh` (every unit), `Burning` (about 300 of 20,000 units, flips several times a second), `Selected` (one unit at a time, read by the UI only), `InCombat` (half the units, flips every few seconds, read by five systems).

<details>
<summary>Answer and worked solution</summary>

**Answer (one defensible set):**

| Component | Choice | Reason |
|---|---|---|
| `Transform` | archetype column | Almost never added or removed; joined by movement, culling, render extract and more every frame |
| `Mesh` | archetype column | Changes only on spawn; joined with `Transform` by the renderer every frame |
| `Burning` | sparse set | Hundreds of flips per second would move whole rows; one system walks a 300-element pool |
| `Selected` | sparse set | A one-element pool; one UI system reads it; toggles cost almost nothing |
| `InCombat` | enable flag | Flips often on thousands of units, yet five systems join it; a flag keeps rows still and keeps the joins cheap |

The lecture's sentence decides each row. Archetypes pay when an entity's component set changes, and sparse sets pay every time a system joins two or more components. `InCombat` is the case where both costs are high, which is why Unity offers enableable components: the storage stays fixed and queries filter by a bit.
</details>

## Week 6: Cache locality and data-oriented design

21. *Week 6 · compute.* An entity struct is 192 bytes, and the movement loop uses 20 hot bytes at its start. Use the byte model for 500,000 entities.
    (a) Give `B_AoS`, `B_SoA`, the useful fraction and the predicted speed-up at `L = 64` and at `L = 128`.
    (b) Give the memory traffic for each layout and the time at a sustained 25 GB/s.
    (c) After a cleanup the struct is 40 bytes with the same 20 hot bytes. What does the model predict at `L = 64`, and why did the formula change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `L = 64`: 64 and 20 bytes, 31.25%, 3.2×. `L = 128`: 128 and 20 bytes, 15.6%, 6.4×. (b) AoS 32 MB (1.28 ms) at `L = 64` or 64 MB (2.56 ms) at `L = 128`; SoA 10 MB (0.40 ms). (c) `B_AoS = 40`, a 2× speed-up.

(a) `s = 192 ≥ L` in both cases, so each entity's hot bytes cost whole lines: `B_AoS = L × ceil(20 / L) = L`. SoA arrays are dense: `B_SoA = 20`. Useful fraction `20 / 64` and `20 / 128`.

(b) Traffic is `N × B`: `500,000 × 64 = 32` MB, `500,000 × 128 = 64` MB, `500,000 × 20 = 10` MB. Time is traffic divided by bandwidth, for example `32 × 10^6 / 25 × 10^9 = 1.28` ms.

(c) Now `s = 40 < 64`, so neighboring entities share lines and every byte comes in: `B_AoS = s = 40`. Speed-up `40 / 20 = 2`. Shrinking the struct helps AoS because each line holds more entities.
</details>

22. *Week 6 · trace.* What does this print on a 64-bit desktop platform (x86-64 or arm64)? Give the byte offset of every field in `A` and `C`.

```cpp
#include <cstdio>

struct A { char tag; double hp; short level; int id; char team; };
struct B { double hp; int id; short level; char tag; char team; };
struct C { bool alive; float pos[3]; bool stunned; double t; };
struct D { double t; float pos[3]; bool alive; bool stunned; };

int main() {
    std::printf("A %zu  B %zu  C %zu  D %zu\n", sizeof(A), sizeof(B), sizeof(C), sizeof(D));
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
A 32  B 16  C 32  D 24
```

`A`: `tag` at 0, 7 bytes of padding, `hp` at 8, `level` at 16, 2 bytes of padding, `id` at 20, `team` at 24, then 7 bytes of tail padding so the size is a multiple of 8. Size 32 for 16 bytes of data.

`B` has the same fields sorted from largest alignment to smallest: `8 + 4 + 2 + 1 + 1 = 16`, no padding.

`C`: `alive` at 0, 3 bytes of padding, `pos` at 4 to 15, `stunned` at 16, 7 bytes of padding, `t` at 24. Size 32.

`D`: `t` at 0, `pos` at 8 to 19, the two `bool`s at 20 and 21, 2 bytes of tail padding. Size 24.

In an array of a million, `A` instead of `B` wastes 16 MB of cache capacity on bytes that hold nothing.
</details>

23. *Week 6 · compute.* A 72-byte `Projectile` starts with position (12 bytes), velocity (12) and age (4). The rest (owner, damage, trail color, effect ids) is 44 bytes that the update loop never reads.
    (a) Give bytes fetched per projectile before and after a hot/cold split into 28-byte hot structs, at `L = 64` and at `L = 128`.
    (b) A teammate converts the loot window, which opens one chest and reads all 18 fields of each of its 12 items, to SoA. Why did it get slower?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) At `L = 64`: 64 before, 28 after, 2.3× less. At `L = 128`: 72 before, 28 after, 2.6× less. (b) Each item now costs up to 18 lines instead of one or two.

(a) At `L = 64`, `s = 72 ≥ 64`, so `B = 64 × ceil(28/64) = 64` (more for the many structs that straddle a line). At `L = 128`, `s = 72 < 128`, so structs share lines and `B = s = 72`. After the split the hot structs are 28 bytes, below either line size, so `B = 28`: every fetched byte is used.

(b) The loot window follows the "look up by key, then use many fields" pattern. In AoS one item's 18 fields sit in one or two lines. In SoA they sit in 18 arrays, one line each, and only 12 items are read, so there is no long stream for the prefetcher to follow. SoA pays off for loops over many entities that use a few fields.
</details>

24. *Week 6 · compute.* A laptop has an 8 MB level-2 cache (use 8,000,000 bytes) and 64-byte lines. The AoS entity is 96 bytes; the SoA hot arrays hold 16 bytes per entity.
    (a) Up to what entity count does each layout's working set fit in the level-2 cache?
    (b) In which range of `N` do you expect the AoS/SoA ratio to be largest, and why?
    (c) The SoA loop moves 4,000,000 entities in 2.0 ms. What bandwidth did it achieve, counting only the hot bytes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 83,000 entities for AoS, 500,000 for SoA. (b) Between about 83,000 and 500,000 entities, and to a lesser degree above that. (c) 32 GB/s.

(a) `8,000,000 / 96 = 83,333` and `8,000,000 / 16 = 500,000`.

(b) Below 83,000 both layouts stay in cache between frames, and the gap comes mostly from SIMD. Between 83,000 and 500,000 AoS streams from main memory while SoA still hits the cache, so the gap is widest there. Above 500,000 both stream, and the ratio settles near the byte model's `B_AoS / B_SoA = 64 / 16 = 4` plus whatever SIMD adds. The lecture's reference table shows the same cliff between 100,000 and 1,000,000 entities on a 16 MB cache.

(c) `4,000,000 × 16 = 64,000,000` bytes in 2.0 ms is `64 × 10^6 / 2 × 10^−3 = 32 × 10^9` bytes per second.
</details>

## Week 7: Resource management and hot reload

25. *Week 7 · compute.* A drive has access time `t_a = 10` ms and rate `R = 250` MB/s.
    (a) What is its knee `b*`, and what effective rate do 128 KB (0.128 MB) reads get?
    (b) A menu loads 400 icons of 128 KB each. Give the load time as loose files and as one packed file, and the speed-up.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `b* = 2.5` MB; 12.2 MB/s, 4.9% of the rated speed. (b) 4.205 s loose, 0.215 s packed, about 19.6× faster.

(a) `b* = t_a × R = 0.010 × 250 = 2.5` MB. `R_eff = R × b / (b + b*) = 250 × 0.128 / 2.628 = 12.18` MB/s.

(b) Bytes `400 × 0.128 = 51.2` MB, transfer `51.2 / 250 = 0.2048` s either way. Loose: `400 × 0.010 + 0.2048 = 4.2048` s. Packed: `0.010 + 0.2048 = 0.2148` s. Almost all of the loose load is waiting, not transferring.
</details>

26. *Week 7 · compute.* A game has 12 zones. Entering a zone loads 180 MB of unique data (one read) plus 90 MB of shared props in 450 files of 0.2 MB. Use the lecture's district model with `reads = 1 + round(450 × (1 − f))`.
    (a) On the laptop hard drive (`t_a = 15` ms, `R = 100` MB/s), give reads, load time and disk use for `f = 0` and `f = 1`.
    (b) What is the smallest `f`, in steps of 0.05, that brings the hard-drive load under 5 seconds, and what does it cost in disk?
    (c) On the SSD (`t_a = 0.1` ms, `R = 5,500` MB/s), how much does full duplication save?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `f = 0`: 451 reads, 9.47 s, 2,250 MB. `f = 1`: 1 read, 2.72 s, 3,240 MB. (b) `f = 0.70`: 136 reads, 4.74 s, 2,943 MB. (c) About 45 ms, from 0.094 s to 0.049 s.

(a) Transfer is `270 / 100 = 2.7` s in every layout. Store once: `451 × 0.015 + 2.7 = 9.465` s. Disk `180 × 12 + 90 = 2,250` MB. Duplicate: `0.015 + 2.7 = 2.715` s. Disk `270 × 12 = 3,240` MB.

(b) Waiting must stay under `5 − 2.7 = 2.3` s, so fewer than 153.3 reads. At `f = 0.65`: `1 + round(157.5) = 159` reads, 5.085 s, too slow. At `f = 0.70`: `1 + 135 = 136` reads, `2.04 + 2.7 = 4.74` s. Disk `2,160 + 90 × 0.3 + 90 × 0.7 × 12 = 2,943` MB, 31% more than storing once.

(c) SSD: `451 × 0.0001 + 270 / 5,500 = 0.0451 + 0.0491 = 0.094` s against `0.0001 + 0.0491 = 0.049` s. Nearly 1 GB of duplicates buys less than three frames at 60 Hz. The model says duplicate for hard drives, pack but do not duplicate for SSDs.
</details>

27. *Week 7 · trace.* This is the lecture's reference-counted cache with one switch. With `keep_unused=True`, entries that reach count zero stay in memory, as an LRU list without a budget would. What does it print, and what does the second policy still need before it can ship?

```python
class ResourceCache:
    def __init__(self, loader, keep_unused):
        self.loader, self.keep_unused = loader, keep_unused
        self.entries = {}                      # path -> [data, refcount]
        self.disk_loads = 0

    def acquire(self, path):
        entry = self.entries.get(path)
        if entry is None:
            entry = self.entries[path] = [self.loader(path), 0]
            self.disk_loads += 1
        entry[1] += 1
        return entry[0]

    def release(self, path):
        entry = self.entries[path]
        entry[1] -= 1
        if entry[1] == 0 and not self.keep_unused:
            del self.entries[path]

for keep in (False, True):
    cache = ResourceCache(lambda p: f"<{p}>", keep_unused=keep)
    for district in ("docks", "market", "docks", "market", "docks"):
        props = ["lamp", "crate", district + "_sign"]
        for p in props:
            cache.acquire(p)
        for p in props:                        # the player leaves the district
            cache.release(p)
    print(f"keep_unused={keep}: disk loads {cache.disk_loads}, resident {sorted(cache.entries)}")
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
keep_unused=False: disk loads 15, resident []
keep_unused=True: disk loads 4, resident ['crate', 'docks_sign', 'lamp', 'market_sign']
```

With free-at-zero, every district visit releases all three props before the next visit acquires them, so each visit loads three files: `5 × 3 = 15` loads. The player walking back and forth pays for the same lamp five times.

Keeping zero-count entries loads each distinct file once: lamp, crate and the two signs. The count still answers "may this be freed?". What the second policy lacks is the other half of the lecture's design, a memory budget that answers "must it be freed now?" by evicting the least recently used zero-count entry when a new load needs room. Without it, memory only grows.
</details>

28. *Week 7 · trace.* Using the lecture's generational `Pool`, what does this print? What did the second `tex.destroy(b)` do, and why is that important?

```cpp
#include <cstdint>
#include <cstdio>
#include <vector>

struct Handle { std::uint32_t index; std::uint32_t generation; };

template <typename T>
class Pool {                                   // the lecture's pool, unchanged
    struct Slot { std::uint32_t generation = 0; bool alive = false; T data{}; };
    std::vector<Slot> slots;
    std::vector<std::uint32_t> free_list;
public:
    Handle create(T data) {
        std::uint32_t i;
        if (!free_list.empty()) { i = free_list.back(); free_list.pop_back(); }
        else { i = static_cast<std::uint32_t>(slots.size()); slots.emplace_back(); }
        slots[i].alive = true;
        slots[i].data = data;
        return {i, slots[i].generation};
    }
    T* get(Handle h) {
        Slot& s = slots[h.index];
        return (s.alive && s.generation == h.generation) ? &s.data : nullptr;
    }
    void replace(Handle h, T data) { if (T* p = get(h)) *p = data; }
    void destroy(Handle h) {
        if (get(h)) { slots[h.index].alive = false; ++slots[h.index].generation; free_list.push_back(h.index); }
    }
};

void show(Pool<int>& p, const char* name, Handle h) {
    int* v = p.get(h);
    std::printf("%s (%u,%u) -> ", name, h.index, h.generation);
    if (v) std::printf("%d\n", *v); else std::printf("null\n");
}

int main() {
    Pool<int> tex;
    Handle a = tex.create(10);
    Handle b = tex.create(20);
    tex.destroy(a);
    Handle c = tex.create(30);
    tex.replace(b, 21);
    tex.destroy(b);
    tex.destroy(b);                            // a second destroy of the same handle
    Handle d = tex.create(40);
    Handle e = tex.create(50);
    show(tex, "a", a); show(tex, "b", b); show(tex, "c", c);
    show(tex, "d", d); show(tex, "e", e);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
a (0,0) -> null
b (1,0) -> null
c (0,1) -> 30
d (1,1) -> 40
e (2,0) -> 50
```

`a` is `(0,0)` and `b` is `(1,0)`. Destroying `a` bumps slot 0 to generation 1, and `c` reuses it as `(0,1)`. `replace` writes 21 into `b`'s slot, then `b` is destroyed and slot 1 goes to generation 1. `d` reuses slot 1 as `(1,1)`. The free list is empty, so `e` takes a new slot 2.

The second `destroy(b)` does nothing, because `get(b)` already fails. Without that check, slot 1 would be pushed onto the free list twice, and `d` and `e` would both be handed slot 1: two live textures sharing one slot, the bug Lab 05 asks you to explain for entities.
</details>

29. *Week 7 · code.* The lecture's breadth-first `rebuild_order` prints the list below for this graph. Which asset is rebuilt too early, and what would the player see? Write `rebuild_order_topo` so that every asset is rebuilt after everything it uses, choosing alphabetically among ready assets, and give its output.

```python
from collections import deque

uses = {
    "mat/a":    ["shader/s"],
    "tex/bake": ["shader/s"],          # a texture baked by running the shader
    "mat/z":    ["tex/bake"],
    "model/m":  ["mat/a", "mat/z"],
}

def rebuild_order(changed, uses):      # the lecture's breadth-first version
    used_by = {}
    for user, needed in uses.items():
        for n in needed:
            used_by.setdefault(n, []).append(user)
    order, seen, queue = [], {changed}, deque([changed])
    while queue:
        for user in sorted(used_by.get(queue.popleft(), [])):
            if user not in seen:
                seen.add(user)
                order.append(user)
                queue.append(user)
    return order

print(rebuild_order("shader/s", uses))
```

<details>
<summary>Answer and worked solution</summary>

**Output of the breadth-first version:**

```text
['mat/a', 'tex/bake', 'model/m', 'mat/z']
```

`model/m` is reached at distance 2 through `mat/a`, before `mat/z`, which sits at distance 3 through `tex/bake`. The model is rebuilt from the old `mat/z` and keeps showing the old baked material until the next reload. It looks like hot reload "only half worked".

A topological version first collects everything downstream of the change, then releases an asset only when all of its affected inputs are done:

```python
def rebuild_order_topo(changed, uses):
    used_by = {}
    for user, needed in uses.items():
        for n in needed:
            used_by.setdefault(n, []).append(user)
    affected, stack = set(), [changed]           # everything downstream of the change
    while stack:
        for user in used_by.get(stack.pop(), []):
            if user not in affected:
                affected.add(user)
                stack.append(user)
    waiting = {a: sum(1 for n in uses[a] if n in affected) for a in affected}
    ready = sorted(a for a in affected if waiting[a] == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for user in used_by.get(node, []):
            waiting[user] -= 1
            if waiting[user] == 0:
                ready.append(user)
                ready.sort()
    return order

uses = {"mat/a": ["shader/s"], "tex/bake": ["shader/s"],
        "mat/z": ["tex/bake"], "model/m": ["mat/a", "mat/z"]}
print(rebuild_order_topo("shader/s", uses))
```

```text
['mat/a', 'tex/bake', 'mat/z', 'model/m']
```

`model/m` waits for two affected inputs and is released only after `mat/z`. This is Kahn's algorithm, the same idea as week 1's start-up order.
</details>

## Week 8: Rendering pipeline overview

30. *Week 8 · compute.* Use `c_draw = 1.5` µs and `c_switch = 8` µs.
    (a) A scene has 3,000 draws spread evenly over 60 materials. Give the expected switches and submit time in random order and sorted by material.
    (b) Now 600 of the draws are translucent over 12 materials, and the other 2,400 are opaque over 48 materials. Give switches and submit time with the section 3 sort key.
    (c) The art team atlases the translucent effects down to 3 materials. Recompute (b).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2,950 switches and 28.1 ms random; 59 switches and 4.97 ms sorted. (b) 598 switches, 9.28 ms. (c) 448 switches, 8.08 ms.

(a) `W_random = N(1 − 1/M) = 3,000 × 59/60 = 2,950`. Time `3,000 × 1.5 + 2,950 × 8 = 4,500 + 23,600 = 28,100` µs. Sorted: `W = M − 1 = 59`, time `4,500 + 472 = 4,972` µs.

(b) Opaque sorted: 47 switches. One switch at the pass boundary. Translucent draws go back to front, so their materials land in effectively random order: `600 × (1 − 1/12) = 550`. Total 598, time `4,500 + 4,784 = 9,284` µs.

(c) `600 × (1 − 1/3) = 400`, total `47 + 1 + 400 = 448`, time `4,500 + 3,584 = 8,084` µs. The atlas helps less than you might hope, because back-to-front order still interleaves three materials.
</details>

31. *Week 8 · trace.* Using the lecture's `make_key`, what does this print? Explain why `fog` comes before `window` and `crate` before `barrel`.

```cpp
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>

enum Pass : std::uint64_t { Opaque = 0, Translucent = 1, UI = 2 };

// The lecture's key: bits 62-63 pass, the rest depends on the pass.
std::uint64_t make_key(Pass pass, std::uint16_t material, std::uint32_t depth24) {
    std::uint64_t key = std::uint64_t(pass) << 62;
    depth24 &= 0xFFFFFF;
    if (pass == Translucent)
        key |= std::uint64_t(0xFFFFFF - depth24) << 16 | material;
    else
        key |= std::uint64_t(material) << 24 | depth24;
    return key;
}

struct Draw { const char* name; std::uint64_t key; };

int main() {
    std::vector<Draw> q = {
        {"fog",     make_key(Translucent, 2, 4000)},
        {"wall",    make_key(Opaque, 9, 300)},
        {"minimap", make_key(UI, 0, 0)},
        {"barrel",  make_key(Opaque, 4, 1200)},
        {"window",  make_key(Translucent, 7, 600)},
        {"crate",   make_key(Opaque, 4, 80)},
    };
    std::sort(q.begin(), q.end(), [](const Draw& a, const Draw& b) { return a.key < b.key; });
    for (const Draw& d : q) std::printf("%016llx  %s\n", (unsigned long long)d.key, d.name);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
0000000004000050  crate
00000000040004b0  barrel
000000000900012c  wall
400000fff05f0002  fog
400000fffda70007  window
8000000000000000  minimap
```

Opaque keys are `material << 24 | depth`. `crate` and `barrel` share material 4, so depth decides, and the nearer crate (80 = `0x50`) comes before the barrel (1,200 = `0x4b0`). The wall's material 9 puts it after both.

Translucent keys store `0xFFFFFF − depth` above the material. The fog at depth 4,000 gets `0xFFF05F`, the window at 600 gets `0xFFFDA7`. The smaller value sorts first, so the farther fog is drawn before the nearer window, as blending requires, even though its material id is lower. The UI pass bits `10` put the minimap last whatever its fields.
</details>

32. *Week 8 · compute.* A 2560 × 1440 frame has opaque depth complexity 5 at every pixel, and the early depth test is on.
    (a) How many fragments are shaded for front-to-back, random and back-to-front order?
    (b) The fragment shader is the GPU bottleneck. How much GPU time can random order cost compared with front to back?
    (c) What does a depth prepass shade, and what does it cost instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.69 million, 8.42 million and 18.43 million. (b) About 2.28 times the fragment work. (c) Exactly one shaded fragment per pixel, 3.69 million, at the price of drawing the opaque geometry twice.

(a) The frame has `2,560 × 1,440 = 3,686,400` pixels. Front to back shades 1 per pixel. Random order shades `H_5 = 1 + 1/2 + 1/3 + 1/4 + 1/5 = 2.283` per pixel, 8,417,280 in all. Back to front shades all 5, 18,432,000.

(b) If fragment shading dominates, time scales with fragments: `2.283×` for random, `5×` for back to front.

(c) The prepass writes depth with a trivial shader, then the full pass shades only fragments whose depth equals the stored one. It adds a second round of vertex work and draw calls. Whether it pays is a measurement: worth it when fragments are the bottleneck, not when submission or vertices are.
</details>

33. *Week 8 · compute.* A renderer maps view distance from 0.1 m to 1,000 m onto the depth field of its sort key.
    (a) How big is one depth step with the lecture's 24-bit field, and with a 16-bit field?
    (b) The key gives material 12 bits. The game has 5,000 materials. What happens to material 4,100, and what does it cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 0.06 mm with 24 bits; about 15.3 mm with 16 bits. (b) It aliases with material 4. Their draws sort as one group and interleave, which adds switches.

(a) `999.9 / 16,777,215 = 0.0000596` m, and `999.9 / 65,535 = 0.01526` m. Two opaque objects closer than one step tie on depth, and the next field decides their order. With 16 bits, two rocks 1 cm apart share a depth value, so their order is left to chance, and the farther one may be shaded first and then overdrawn.

(b) Twelve bits hold 4,096 ids, so ids wrap: `4,100 mod 4,096 = 4`. The draws still bind their real materials, so the picture is correct. But materials 4 and 4,100 now share one key group, and within it draws are ordered by depth, alternating between the two. The switch count grows toward the random-order figure for that pair. Field widths are budgets; check them against the content.
</details>

## Week 9: Input and event systems

34. *Week 9 · compute.* A game samples input once per frame.
    (a) At 45 fps, what fraction of 12 ms taps does it miss? What frame rate would catch them all?
    (b) A player flicks the crosshair at 900 degrees per second. What are the mean and worst aim errors at 45 fps with frame timestamps, and with events time-stamped at 500 Hz?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 46%; at least 83.3 fps. (b) Mean 10° and worst 20° at 45 fps; mean 0.9° and worst 1.8° at 500 Hz.

(a) `T = 1,000 / 45 = 22.2` ms. `P(miss) = 1 − 12 / 22.2 = 0.46`. Every tap is caught when `T ≤ 12` ms, which is `1,000 / 12 = 83.3` fps or more.

(b) The worst error is `ω × T = 900 × 0.0222 = 20°`, the mean half that. With 500 Hz timestamps `T = 2` ms: `900 × 0.002 = 1.8°` worst, 0.9° mean. The frame rate stays the same; only where the time stamps come from changes.
</details>

35. *Week 9 · trace.* Using the lecture's `InputFrame`, what does this print for three frames? In which frame would a sampling design, reading `held` once per frame, lose information, and what would it lose?

```cpp
#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

enum class EventType : std::uint8_t { KeyDown, KeyUp, MouseMove };
struct InputEvent { EventType type; std::uint16_t code; float dx, dy; std::uint64_t time_ns; };
struct ButtonFrame { bool held = false; std::uint8_t presses = 0, releases = 0; };

struct InputFrame {                                   // the lecture's frame summary
    std::array<ButtonFrame, 256> keys{};
    float mouse_dx = 0, mouse_dy = 0;
    void begin_frame() {
        for (ButtonFrame& k : keys) k.presses = k.releases = 0;
        mouse_dx = mouse_dy = 0;
    }
    void apply(const InputEvent& e) {
        if (e.type == EventType::KeyDown) { keys[e.code].held = true;  ++keys[e.code].presses; }
        if (e.type == EventType::KeyUp)   { keys[e.code].held = false; ++keys[e.code].releases; }
        if (e.type == EventType::MouseMove) { mouse_dx += e.dx; mouse_dy += e.dy; }
    }
};

int main() {
    const std::uint16_t J = 'j', W = 'w';
    std::vector<std::vector<InputEvent>> frames = {
        {{EventType::KeyDown, W, 0, 0, 1}, {EventType::KeyDown, J, 0, 0, 2},
         {EventType::KeyUp, J, 0, 0, 3},   {EventType::MouseMove, 0, 3, 2, 4},
         {EventType::KeyDown, J, 0, 0, 5}, {EventType::KeyUp, J, 0, 0, 6}},
        {{EventType::MouseMove, 0, -1, 4, 7}, {EventType::MouseMove, 0, -2, -1, 8}},
        {{EventType::KeyUp, W, 0, 0, 9},   {EventType::KeyDown, W, 0, 0, 10}},
    };
    InputFrame in;
    for (std::size_t f = 0; f < frames.size(); ++f) {
        in.begin_frame();
        for (const InputEvent& e : frames[f]) in.apply(e);
        std::printf("frame %zu: w held=%d p=%d r=%d | j held=%d p=%d r=%d | mouse=(%.0f,%.0f)\n", f,
                    in.keys[W].held, in.keys[W].presses, in.keys[W].releases,
                    in.keys[J].held, in.keys[J].presses, in.keys[J].releases, in.mouse_dx, in.mouse_dy);
    }
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
frame 0: w held=1 p=1 r=0 | j held=0 p=2 r=2 | mouse=(3,2)
frame 1: w held=1 p=0 r=0 | j held=0 p=0 r=0 | mouse=(-3,3)
frame 2: w held=1 p=1 r=1 | j held=0 p=0 r=0 | mouse=(0,0)
```

Frame 0: `w` goes down and stays down. `j` is tapped twice, so it ends up with two presses and two releases. Frame 1 has only motion, summed to (−3, 3). Frame 2 releases and re-presses `w`.

A sampling design loses information in two frames. In frame 0 it sees `j` up at the end, so both jumps vanish. In frame 2 it sees `w` held at the end of frames 1 and 2, so the release and re-press vanish; if `w` were a toggle or a double-tap dash, the player's input is gone. `presses` and `releases` are counts, not flags, so the layer keeps both taps and leaves the "one jump or two" decision to gameplay.
</details>

36. *Week 9 · trace.* Using the lecture's `Context` and `Router`, what does this print? Explain why the naive gameplay context still holds two actions.

```python
class Context:
    def __init__(self, name, bindings, eats_everything=False):
        self.name, self.bindings = name, bindings
        self.eats_everything = eats_everything
        self.held = set()
    def handle(self, kind, key):
        action = self.bindings.get(key, f"type '{key}'")
        if kind == "down":
            self.held.add(action)
        else:
            self.held.discard(action)

class Router:                                   # the lecture's router
    def __init__(self, press_ownership):
        self.stack, self.owner = [], {}
        self.press_ownership = press_ownership
    def route(self, kind, key):
        if kind == "up" and self.press_ownership and key in self.owner:
            self.owner.pop(key).handle("up", key)
            return
        for ctx in reversed(self.stack):
            if key in ctx.bindings or ctx.eats_everything:
                ctx.handle(kind, key)
                if kind == "down":
                    self.owner[key] = ctx
                return

for fixed in (False, True):
    game = Context("gameplay", {"shift": "sprint", "enter": "open_chat"})
    chat = Context("chat", {"enter": "send"}, eats_everything=True)
    r = Router(press_ownership=fixed)
    r.stack.append(game)
    r.route("down", "shift")       # start sprinting
    r.route("down", "enter")       # open chat
    r.stack.append(chat)
    r.route("up", "enter")
    r.route("down", "h")           # type a letter while still holding shift
    r.route("up", "shift")         # let go of shift while chat is open
    r.stack.pop()                  # chat closes
    r.route("up", "h")
    print("fixed" if fixed else "naive", "| gameplay:", sorted(game.held), "| chat:", sorted(chat.held))
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
naive | gameplay: ['open_chat', 'sprint'] | chat: ["type 'h'"]
fixed | gameplay: [] | chat: []
```

Naive run: both downs reach gameplay before chat exists. After chat is pushed, the `enter` up and the `shift` up go to the top context, chat, which eats everything. Gameplay never hears either release, so the character sprints on after chat closes, and gameplay also believes Enter is held. The `h` up arrives after chat is popped; gameplay does not bind `h`, so nobody takes it and chat is left believing `h` is held.

With press ownership each up goes to the context that took its down: `enter` and `shift` to gameplay, `h` to chat, even though chat is no longer on the stack. Both held sets end empty. The lecture adds one more rule for real engines: when a context is popped, synthesize ups for the keys it owns.
</details>

37. *Week 9 · compute.* (a) A game runs at 60 fps but hitches for 120 ms once every 3 seconds. Players tap dodge for 20 ms at random moments. About what fraction of dodges are lost by a sampling design? (b) During a 150 ms hitch, a 1,000 Hz mouse is moving, a gamepad reports its stick at 250 Hz, and the player presses and releases three keys. How many events arrive? Does a 128-entry ring buffer hold them, and what would you change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 3.3%, all during hitches. (b) About 193 events. A 128-entry buffer overflows and may overwrite key events. Merge motion events as they arrive.

(a) The hitch frame covers `0.12 / 3 = 4%` of the time. A tap starting inside it is missed with probability `1 − 20/120 = 0.833`. Ordinary 16.7 ms frames never miss a 20 ms tap. So `0.04 × 0.833 = 3.3%`.

(b) `150` mouse events, `0.150 × 250 = 37.5`, so about 37 stick events, and 6 key events: about 193. The ring overwrites the oldest 65, which can include the key downs. Merging consecutive mouse (and stick) events into one on arrival cuts the count to a few dozen and loses nothing for camera or stick control, while every key edge is kept. That is the lecture's rule: merge motion, never merge transitions.
</details>

## Week 10: Scripting layer integration

38. *Week 10 · compute.* A game updates 6,000 scripted entities per frame. One crossing costs 1.5 µs and each entity's work 0.25 µs.
    (a) What is `B*`?
    (b) Give crossings, frame cost and crossing share at `B = 1`, `B = 6`, `B = 60` and `B = 6,000`.
    (c) Which batch size would you pick, and why not always the largest?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `B* = 6`. (b) `B = 1`: 6,000 crossings, 10.5 ms, 85.7%. `B = 6`: 1,000, 3.0 ms, 50%. `B = 60`: 100, 1.65 ms, 9.1%. `B = 6,000`: 1, 1.50 ms, 0.1%. (c) Around 60.

(a) `B* = c_cross / c_work = 1.5 / 0.25 = 6`.

(b) `T = ceil(N/B) × 1.5 + 6,000 × 0.25`. The work term is always 1,500 µs. At `B = 1`: `9,000 + 1,500 = 10,500` µs. At `B = 6`: `1,500 + 1,500`. At `B = 60`: `150 + 1,500`. At `B = 6,000`: `1.5 + 1,500`.

(c) At `B = 60` crossings are under 10% of the cost. Going to one giant call saves another 0.15 ms and costs readability, per-object hot reload and the ability to give rare entities their own logic. The first factor of `B*` is worth nearly everything.
</details>

39. *Week 10 · trace.* Using the lecture's budgeted scheduler, what does this print? How many frames does it take, and in which frame does script `b` finish?

```python
def walk(name, steps):
    for i in range(steps):
        yield f"{name}{i}"                   # each yield = one unit of script work

def run_frame(scripts, budget):              # the lecture's scheduler
    done, log = 0, []
    while scripts and done < budget:
        s = scripts.pop(0)
        try:
            log.append(next(s))
            scripts.append(s)
        except StopIteration:
            continue
        done += 1
    return log

queue = [walk("a", 2), walk("b", 4), walk("c", 3)]
frame = 1
while queue:
    print(frame, run_frame(queue, budget=4))
    frame += 1
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
1 ['a0', 'b0', 'c0', 'a1']
2 ['b1', 'c1', 'b2', 'c2']
3 ['b3']
```

Nine units of work at four per frame take `ceil(9/4) = 3` frames. Round-robin order is a, b, c, a, b, c, and so on. In frame 2, `a` is resumed, finds nothing left and is dropped at no cost, so `b` and `c` share the budget. `b` finishes with `b3` in frame 3. Without the budget, all nine units would run in frame 1. The budget turns a spike into latency: `b`'s last step lands two frames late.
</details>

40. *Week 10 · trace.* The binding layer below checks every handle, as in lecture section 3. What does it print? What would the second call have done without the check?

```python
slots = {3: (1, {"name": "wolf", "hp": 40}), 4: (0, {"name": "bandit", "hp": 25})}
#        index: (generation, object)

def alive(h):
    index, gen = h
    return index in slots and slots[index][0] == gen

def bound(fn):
    def call_from_script(h, *args):
        if not alive(h):
            return None
        return fn(slots[h[0]][1], *args)
    return call_from_script

@bound
def apply_damage(target, amount):
    target["hp"] -= amount
    return target["hp"]

target = (4, 0)                              # the script picks the bandit
print(apply_damage(target, 10))
slots[4] = (1, {"name": "chest", "hp": 1})   # bandit dies, a chest reuses slot 4
print(apply_damage(target, 10))
print(apply_damage((3, 0), 10), apply_damage((3, 1), 10))
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
15
None
None 30
```

The first call hits the bandit: `25 − 10 = 15`. Then slot 4 holds a chest at generation 1. The script's stored handle `(4, 0)` fails `alive`, so the call returns `None` (nil in Lua) and the chest is untouched. Without the check the script would have damaged the chest and returned −9, a wrong-object bug far from its cause. `(3, 0)` is stale for the wolf at generation 1; `(3, 1)` is current, and the wolf drops to 30.
</details>

41. *Week 10 · compute.* A WoW-style addon runs an `OnUpdate` handler on each of 120 unit frames on a machine drawing 240 fps. A crossing costs 3 µs and each frame's work 2 µs.
    (a) How many milliseconds of CPU per second does this spend?
    (b) The author switches to one batched update of all 120 frames on a 10 Hz timer. What does it cost now?
    (c) Instead, the author registers for health-change events, which fire about twice per second per unit, each updating one frame. What does that cost, and when would events be the worse choice?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 144 ms per second. (b) 2.43 ms per second. (c) 1.2 ms per second; events lose when they fire about as often as the poll would run.

(a) `120 × (3 + 2) × 240 = 144,000` µs per second, one seventh of a core, on a fast machine where the frame rate is highest.

(b) `(3 + 120 × 2) × 10 = 2,430` µs per second. Crossings fall from 28,800 to 10 per second.

(c) `120 × 2 × (3 + 2) = 1,200` µs per second. If health changed every frame (a damage-over-time aura on everyone), events would cost as many crossings as polling plus the dispatch overhead. Count crossings for the case you expect.
</details>

## Week 11: Physics integration basics

42. *Week 11 · compute.* Use `v(t) = v0 × e^(−kt)`.
    (a) A crate starts at 2.5 m/s with `k = 1.5` per second. When can it sleep with Box2D v3.1 defaults (0.05 m/s, 0.5 s)? With Box2D v2.4's 0.01 m/s tolerance and the same 0.5 s?
    (b) An island has four crates that could each sleep alone at 1.1, 2.0, 3.1 and 0.7 s. When does the island sleep, and how many awake body-seconds does it cost against per-body sleeping?
    (c) With `k = 2` and v3.1 defaults, what starting speed makes a crate able to sleep at exactly 2.5 s?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 3.11 s with v3.1 and 4.18 s with v2.4. (b) At 3.1 s; 12.4 against 6.9 body-seconds. (c) About 2.73 m/s.

(a) Still-time `ln(2.5 / 0.05) / 1.5 = ln 50 / 1.5 = 3.912 / 1.5 = 2.608` s, plus 0.5 s. With 0.01 m/s: `ln 250 / 1.5 = 5.521 / 1.5 = 3.681` s, plus 0.5 s. The lower threshold costs another second of solving for every such crate.

(b) The island sleeps when its slowest body is ready, 3.1 s. Awake cost `4 × 3.1 = 12.4` body-seconds against `1.1 + 2.0 + 3.1 + 0.7 = 6.9`, 80% more.

(c) Still-time must be 2.0 s: `ln(v0 / 0.05) / 2 = 2`, so `v0 = 0.05 × e^4 = 2.73` m/s.
</details>

43. *Week 11 · trace.* This builds islands with union-find from contact pairs. The floor is static. What does it print? What would it print if static bodies were allowed to join islands, and what would that cost?

```python
def build_islands(contacts, static):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving
            x = parent[x]
        return x
    for a, b in contacts:
        if a in static or b in static:       # a static body never joins or links islands
            for body in (a, b):
                if body not in static:
                    find(body)
            continue
        parent[find(a)] = find(b)
    groups = {}
    for body in parent:
        groups.setdefault(find(body), []).append(body)
    return sorted(sorted(g) for g in groups.values())

floor = "floor"
contacts = [(1, floor), (2, floor), (3, floor), (1, 4), (4, 5), (2, 6),
            (7, 8), (8, floor), (5, 9)]
print(build_islands(contacts, static={floor}))
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
[[1, 4, 5, 9], [2, 6], [3], [7, 8]]
```

Contacts with the floor only register the dynamic body. The chains 1-4-5-9, 2-6 and 7-8 become islands, and crate 3 touches nothing but the floor, so it is an island of one.

If the floor joined islands, every crate would be linked through it: one island of nine bodies. It would sleep only when the slowest crate in the room settles, and any bump anywhere would wake all nine. In a real level, every dynamic object on the ground would share one island, and the sleep system would never save anything.
</details>

44. *Week 11 · trace.* A step reported these contacts. Each contact deals 10 damage to both bodies. What does the buffered version print? What would happen if the loop deleted a body from `health` the moment it reached zero?

```python
health = {1: 25, 2: 10, 3: 15, 4: 40}
events = [(1, 2), (2, 3), (1, 3), (3, 4), (2, 4)]   # contacts reported by the step

to_destroy = set()
for a, b in events:                  # after the step: buffer, then act
    for body in (a, b):
        health[body] -= 10
        if health[body] <= 0:
            to_destroy.add(body)
for body in sorted(to_destroy):
    del health[body]
print(sorted(to_destroy), health)
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
[2, 3] {1: 5, 4: 20}
```

Body 2 appears in three events and reaches 0 at the first. Body 3 appears in three and reaches −5 at the third. Body 1 takes two hits (5 left) and body 4 two hits (20 left). Destruction happens once per body, after all damage, in id order.

Deleting on the spot would remove body 2 at event `(1, 2)`, and event `(2, 3)` would then read `health[2]` and raise `KeyError`. Inside a real physics callback the equivalent is destroying a body the solver still holds, which Box2D v2.4's documentation forbids and v3.1 turns into an assertion in debug builds.
</details>

45. *Week 11 · compute.* A world has 1,500 dynamic bodies. Profiling gives `a = 3` µs per awake body and `b = 1.2` µs per awake contact, with 1.4 contacts per awake body.
    (a) What is the step cost with everything awake, and with 5% awake?
    (b) A tower of 400 touching crates is asleep. An arrow wakes it. How big is the spike?
    (c) The game's CPU time was 15.5 ms at 60 Hz, pipelined and CPU-bound. What does the player see while the tower is awake?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 7.02 ms all awake; 0.35 ms at 5%. (b) About 1.87 ms per step. (c) The frame falls from 16.67 ms to 33.33 ms (60 to 30 fps) until the tower sleeps again.

(a) All awake: `1,500 × 3 + 2,100 × 1.2 = 4,500 + 2,520 = 7,020` µs, 42% of the frame. At 5%: 75 bodies and 105 contacts, `225 + 126 = 351` µs.

(b) `400 × 3 + 560 × 1.2 = 1,200 + 672 = 1,872` µs, all in the step after the hit, because the island wakes as a unit.

(c) `15.5 + 1.87 = 17.37` ms is over 16.67, so each frame rounds up to two refreshes (week 4). The spike lasts until the slowest crate settles plus `t_sleep`. Fixes: make most of the tower static, split it into several islands, or turn crates dynamic only when hit.
</details>

## Week 12: Serialization and save files

46. *Week 12 · compute.* A game has shipped 25 save versions.
    (a) How many migration functions exist with a chain? How many converters would direct conversion have required in total, and how many at the latest release?
    (b) A player loads a version 7 save. How many migrations run? After the game saves again, how many run on the next load?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 24; 300 in total, 24 at the latest release. (b) 18, then 0.

(a) Chain: `N − 1 = 24`, one per release. Direct: `N(N − 1)/2 = 25 × 24 / 2 = 300`, and the release that made version 25 had to rewrite all 24 existing converters, because their target moved.

(b) `25 − 7 = 18`. The next save writes version 25, so no migration runs after that. Keep the version 7 file as a backup in case a migration had a bug.
</details>

47. *Week 12 · trace.* The lecture's chain gains a fifth version: patch 2.2 turns item lists into stacks. What does this print for a version 2 save?

```python
CURRENT = 5

def v1_to_v2(s):
    s = dict(s); s["health"] = s.pop("hp"); return s
def v2_to_v3(s):
    s = dict(s); tx, ty = s.pop("pos"); s["x"], s["y"] = tx * 16, ty * 16; return s
def v3_to_v4(s):
    s = dict(s); s["wallet"] = {"gold": s.pop("gold"), "gems": 0}; return s
def v4_to_v5(s):                     # patch 2.2: items become stacks
    s = dict(s)
    stacks = {}
    for item in s.pop("items"):
        stacks[item] = stacks.get(item, 0) + 1
    s["items"] = [{"template": t, "count": n} for t, n in stacks.items()]
    return s

MIGRATIONS = {1: v1_to_v2, 2: v2_to_v3, 3: v3_to_v4, 4: v4_to_v5}

def upgrade(save):
    v = save["version"]
    if v > CURRENT:
        raise ValueError(f"save is version {v}, this build only knows up to {CURRENT}")
    while v < CURRENT:
        migrate = MIGRATIONS[v]
        save = migrate(save)
        v += 1
        save["version"] = v
    return save

print(upgrade({"version": 2, "health": 20, "gold": 7, "pos": [5, 1],
               "items": ["herb", "rope", "herb"]}))
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
{'version': 5, 'health': 20, 'x': 80, 'y': 16, 'wallet': {'gold': 7, 'gems': 0}, 'items': [{'template': 'herb', 'count': 2}, {'template': 'rope', 'count': 1}]}
```

Three migrations run, 2 to 3, 3 to 4 and 4 to 5. Tile (5, 1) becomes pixels (80, 16). Gold moves into the wallet. Items are counted in order of first appearance, because Python dicts keep insertion order, so `herb` comes first with a count of 2. Each migration pops the field it replaces, which moves the new field to the end of the dict; that is why `items` is last. `v1_to_v2` never ran and never needed to know about stacks.
</details>

48. *Week 12 · trace.* Using the lecture's header, what does this print? One of the three messages is misleading. Which, and how would you word it?

```python
import json
import struct
import zlib

MAGIC = b"LKSV"
HEADER = struct.Struct("<4sIII")                  # magic, version, payload length, CRC-32

def pack(save):
    payload = json.dumps(save, sort_keys=True).encode("utf-8")
    return HEADER.pack(MAGIC, save["version"], len(payload), zlib.crc32(payload)) + payload

def unpack(blob):
    magic, version, length, crc = HEADER.unpack_from(blob)
    payload = blob[HEADER.size:]
    if magic != MAGIC:
        raise ValueError("not a save file")
    if len(payload) != length:
        raise ValueError(f"truncated: expected {length} bytes, got {len(payload)}")
    if zlib.crc32(payload) != crc:
        raise ValueError("corrupted: checksum mismatch")
    return json.loads(payload)

blob = pack({"version": 3, "health": 20, "x": 80, "y": 16})
print(len(blob))
for name, bad in [("cut", blob[:40]), ("magic", b"LKSX" + blob[4:]),
                  ("tail", blob + b"\n")]:
    try:
        unpack(bad)
    except ValueError as e:
        print(name, "->", e)
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
62
cut -> truncated: expected 46 bytes, got 24
magic -> not a save file
tail -> truncated: expected 46 bytes, got 47
```

The payload `{"health": 20, "version": 3, "x": 80, "y": 16}` is 46 bytes, plus the 16-byte header: 62. Cutting at 40 leaves 24 bytes of payload. The wrong magic number is caught before anything else.

The third message is wrong: the file is one byte too long, not truncated. An editor or a sync tool that appended a newline gets told the file was cut short, which sends the player looking for the wrong cause. Word it as a length mismatch, for example "length mismatch: header says 46 bytes, file has 47", and treat both directions as damage: load the backup.
</details>

49. *Week 12 · trace.* What does this two-pass loader print? Why does the healer's reference resolve even though the scout appears first, and what would a single-pass loader do with the scout?

```python
import json

class Npc:
    def __init__(self, uid, name):
        self.uid, self.name, self.follows = uid, name, None

def load(text):
    rows = json.loads(text)
    by_uid = {r["uid"]: Npc(r["uid"], r["name"]) for r in rows}      # pass 1
    for r in rows:                                                    # pass 2
        if r["follows"] is not None:
            by_uid[r["uid"]].follows = by_uid.get(r["follows"])
    return by_uid

text = json.dumps([
    {"uid": 7, "name": "scout",   "follows": 9},
    {"uid": 8, "name": "healer",  "follows": 7},
    {"uid": 9, "name": "captain", "follows": 12},   # uid 12 was removed by a patch
])
npcs = load(text)
for uid, n in npcs.items():
    print(n.name, "->", n.follows.name if n.follows else None)
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
scout -> captain
healer -> scout
captain -> None
```

Pass 1 creates all three NPCs before any link is made, so every existing target is in `by_uid` by pass 2. The healer's reference points backward and would work in one pass anyway. The scout's points forward, to uid 9, which a single-pass loader would not have created yet: it would crash or leave the scout following nothing. The captain's target, uid 12, no longer exists, and `by_uid.get` turns it into `None` instead of a crash, the case Factorio's migration docs describe for removed prototypes. A good loader also logs it.
</details>

## Week 13: Profiling: CPU, GPU, frame budgets

50. *Week 13 · compute.* A game thread's true costs per frame are: `a` 4.0 ms in 20 calls, `b` 2.5 ms in 50,000 calls, `c` 3.0 ms in 1 call, `d` 1.5 ms in 6,000 calls and `e` 0.6 ms in 60,000 calls.
    (a) Every call is instrumented with a 30 ns scope. Give each measured time, the measured ranking against the true ranking, and the measured frame.
    (b) Above what scope cost does `b` appear to be the most expensive function?
    (c) With 45 ns scopes, what does the measured frame do at 60 Hz with vsync?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `a` 4.0006, `b` 4.000, `c` 3.000, `d` 1.680, `e` 2.400 ms. Measured order `a, b, c, e, d`; true order `a, c, b, d, e`. Frame 15.08 ms against 11.6 true. (b) Above about 30.0 ns. (c) It measures 16.82 ms and falls to 33.33 ms frames, 30 fps, while the real game runs at 60.

(a) `measured = t + n × o`. For `b`: `2.5 + 50,000 × 0.00003 = 4.0` ms. For `e`: `0.6 + 60,000 × 0.00003 = 2.4` ms, four times the truth. The frame has `20 + 50,000 + 1 + 6,000 + 60,000 = 116,021` scopes, so `11.6 + 116,021 × 0.00003 = 15.08` ms.

(b) `2.5 + 50,000 o > 4.0 + 20 o` when `49,980 o > 1.5` ms, so `o > 30.01` ns. At 30 ns the two are 0.6 µs apart, and the profile's top spot depends on the timer, not the code.

(c) `11.6 + 116,021 × 0.000045 = 16.82` ms is over 16.67, so the instrumented build rounds up to two refreshes. You are profiling a program that has fallen off the week 4 cliff, and it is not the program players run.
</details>

51. *Week 13 · compute.* A sampling profiler runs at 10 kHz on the thread from question 50 (11.6 ms busy per frame). Function `e` takes 0.6 ms of it.
    (a) How many samples per frame land in `e`?
    (b) How many frames must you capture to measure `e` to ±5%? To ±2%? How many seconds is that at 60 fps?
    (c) At 1 kHz, how many frames for ±5%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6. (b) 67 frames (1.1 s) for ±5%; 417 frames (6.9 s) for ±2%. (c) 667 frames, about 11 s.

(a) The thread yields `10,000 × 0.0116 = 116` samples per frame, and `e` holds `0.6 / 11.6` of them: 6.

(b) `k = 1 / e²`. For ±5%, 400 samples: `400 / 6 = 66.7`, round up to 67 frames. For ±2%, 2,500 samples: `2,500 / 6 = 416.7`, so 417 frames.

(c) At 1 kHz `e` gets 0.6 samples per frame: `400 / 0.6 = 666.7`, so 667 frames. Sampling never inflates `e`; it only needs time, and a tenth of the rate needs ten times the capture.
</details>

52. *Week 13 · trace.* Using the lecture's inclusive and self time loop, what does this print? Which scope would you investigate first, and why not `frame`?

```python
events = [                         # (name, depth, start_us, end_us), recorded as scopes close
    ("cull", 2, 200, 900),
    ("sort", 2, 900, 1300),
    ("render_prep", 1, 100, 1900),
    ("ai", 1, 1900, 3400),
    ("frame", 0, 0, 3500),
]
for name, depth, start, end in sorted(events, key=lambda e: (e[2], e[1])):
    inclusive = end - start
    children = sum(e - s for n, d, s, e in events
                   if d == depth + 1 and start <= s and e <= end)
    print(f"{'  ' * depth}{name:<12} inclusive {inclusive:>5}  self {inclusive - children:>5}")
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
frame        inclusive  3500  self   200
  render_prep  inclusive  1800  self   700
    cull         inclusive   700  self   700
    sort         inclusive   400  self   400
  ai           inclusive  1500  self  1500
```

`frame` has children of `1,800 + 1,500 = 3,300` µs, so its own code is 200 µs: the gaps at 0-100 and 3,400-3,500. `render_prep` spends 700 µs outside `cull` and `sort` (100-200 and 1,300-1,900).

Investigate `ai` first: 1,500 µs of self time, the largest in the frame. `frame` has the largest inclusive time, but inclusive time only says its children are expensive. Blame the children, not the parent. `render_prep`'s 700 µs of self time is the next place to add scopes one level deeper.
</details>

53. *Week 13 · trace.* A capture has 200 frames: 190 take 15 ms, 6 take 19 ms and 4 take 41 ms. What does this print? Which one number would you put in a stutter bug report, and what would you add to it?

```python
import math

def nearest_rank(values, p):
    ordered = sorted(values)
    return ordered[math.ceil(p / 100 * len(ordered)) - 1]

frames = [15_000] * 190 + [19_000] * 6 + [41_000] * 4      # 200 frames, microseconds
avg = sum(frames) / len(frames)
print(f"average {avg / 1000:.2f} ms")
for p in (50, 95, 97, 98, 99):
    print(f"p{p} {nearest_rank(frames, p) / 1000:.1f} ms")
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
average 15.64 ms
p50 15.0 ms
p95 15.0 ms
p97 19.0 ms
p98 19.0 ms
p99 41.0 ms
```

Sorted, frames 1 to 190 are 15 ms, 191 to 196 are 19 ms and 197 to 200 are 41 ms. p95 is item `ceil(190) = 190`, still 15 ms. p97 is item 194 and p98 item 196, both 19 ms. p99 is item 198, 41 ms.

The average of 15.64 ms says 60 fps. Under vsync at 60 Hz every one of the ten slow frames shows for at least two refreshes (19 ms) or three (41 ms). Report p99, 41 ms, together with the worst frame and how often the spikes come (4 in 200 frames, about one every 0.8 s), plus the build, scene and camera path, so someone else can reproduce it.
</details>

54. *Week 13 · compute.* GPU A reports `timestampPeriod = 1.0` and its shadow pass timestamps read 5,100,000 and 8,300,000. GPU B reports `timestampPeriod = 38.5` with readings 200,000 and 290,000. Which shadow pass is slower, and by how much? Why must the engine not wait for these results in the frame that wrote them?

<details>
<summary>Answer and worked solution</summary>

**Answer:** GPU A 3.20 ms, GPU B 3.465 ms. B is slower by 0.265 ms, about 8%.

A: `(8,300,000 − 5,100,000) × 1.0 = 3,200,000` ns. B: `90,000 × 38.5 = 3,465,000` ns. B's raw tick difference is 35 times smaller and its pass is still longer. Ticks mean nothing until you multiply by the period.

The GPU runs a frame or more behind the CPU (week 4). Waiting for this frame's timestamps would stall the CPU until the GPU catches up, the very stall you are trying to measure. Keep a ring of query sets and read frame `n`'s results two or three frames later.
</details>

## Week 14: Tools and editors

55. *Week 14 · compute.* A project has 180 reflected-worthy fields and 6 tool systems.
    (a) How many code sites do hand-written tools need, and how many does a reflection layer need? How many does each add for two more systems?
    (b) With 7 hand-written systems and a miss rate `q = 1.5%` per edit, what fraction of new fields miss at least one system? How many of 80 new fields do you expect to be broken?
    (c) What `q` would keep the expected number of broken fields at 2 or fewer for those 80 fields?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,080 against 186; two more systems add 360 by hand and 2 reflected. (b) 10.0%, about 8 fields. (c) `q ≤ 0.36%`.

(a) `F × S = 180 × 6 = 1,080` and `F + S = 186`. Each new system needs a site for every field by hand (`2 × 180`) and one loop when reflected.

(b) `1 − 0.985^7 = 1 − 0.8996 = 10.0%`, and `80 × 0.100 = 8.0`.

(c) `80 × (1 − (1 − q)^7) ≤ 2` gives `(1 − q)^7 ≥ 0.975`, so `1 − q ≥ 0.975^(1/7) = 0.99639`, `q ≤ 0.36%`: one slip in about 280 edits. No person keeps that rate, which is the practical case for declaring each field once.
</details>

56. *Week 14 · trace.* Using the lecture's `History`, what does this print? One of the three undo entries does nothing when undone. Which, and what rule should `end()` apply?

```python
class Knob:
    def __init__(self, armor):
        self.armor = armor

class History:                                     # the lecture's transactions
    def __init__(self):
        self.done, self.open = [], None
    def begin(self, label):
        self.open = (label, {})
    def set(self, obj, name, value):
        edits = self.open[1]
        key = (id(obj), name)
        if key not in edits:
            edits[key] = [obj, name, getattr(obj, name), value]
        edits[key][3] = value
        setattr(obj, name, value)
    def end(self):
        self.done.append(self.open)
        self.open = None
    def undo(self):
        label, edits = self.done.pop()
        for obj, name, old, _ in edits.values():
            setattr(obj, name, old)
        return label

goblins = [Knob(10), Knob(20), Knob(30)]
hist = History()
hist.begin("drag")
for v in range(10, 61, 5):
    hist.set(goblins[0], "armor", v)
hist.end()
hist.begin("set all")
for g in goblins:
    hist.set(g, "armor", 99)
hist.end()
hist.begin("drag again")
for v in (80, 70, 99):
    hist.set(goblins[2], "armor", v)
hist.end()
print(len(hist.done), [g.armor for g in goblins])
print(hist.undo(), [g.armor for g in goblins])
print(hist.undo(), [g.armor for g in goblins])
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
3 [99, 99, 99]
drag again [99, 99, 99]
set all [60, 20, 30]
```

The first drag sends 11 values to goblin 0 and records one edit, old 10, new 60. "set all" records three edits, one per goblin, each keeping its value from before the transaction (60, 20, 30). "drag again" moves goblin 2 from 99 through 80 and 70 back to 99: old 99, new 99.

Undoing "drag again" restores 99, so the player presses undo and nothing changes, which feels like a broken undo. `end()` should drop edits whose old and new values are equal, and drop the transaction if no edits remain. Lab 14 asks you to drop empty transactions; this is the same rule one step further.
</details>

57. *Week 14 · trace.* This is a member-pointer descriptor table in the style of lecture section 3. What does it print? What does the program fail to report, and how would you change `set_clamped` so a tool cannot miss it?

```cpp
#include <cstdio>
#include <string_view>

struct Spawner { float interval = 2.0f, radius = 5.0f, waves = 3.0f; };
struct FloatField { const char* name; float Spawner::* member; float lo, hi; };

constexpr FloatField kSpawnerFields[] = {
    {"interval", &Spawner::interval, 0.5f, 30},
    {"radius",   &Spawner::radius,   1,    50},
    {"waves",    &Spawner::waves,    1,    10},
};

int set_clamped(Spawner& s, const char* name, float v) {   // returns fields touched
    int touched = 0;
    for (const auto& f : kSpawnerFields)
        if (std::string_view(f.name) == name) {
            s.*f.member = v < f.lo ? f.lo : (v > f.hi ? f.hi : v);
            ++touched;
        }
    return touched;
}

int main() {
    Spawner s;
    int n = set_clamped(s, "interval", 0.1f) + set_clamped(s, "waves", 12)
          + set_clamped(s, "radius_m", 20) + set_clamped(s, "radius", 7.5f);
    std::printf("touched=%d interval=%g radius=%g waves=%g\n", n, s.interval, s.radius, s.waves);
}
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
touched=3 interval=0.5 radius=7.5 waves=10
```

`interval` 0.1 is clamped up to 0.5 and `waves` 12 down to 10, both from the table's metadata. `radius_m` matches no descriptor, touches nothing, and only lowers the count from 4 to 3. The caller sums the counts and never learns which name failed.

Return a status per call and make an unknown name loud: return `false`, or log "field `radius_m` is not declared on `Spawner`", and assert in debug builds. The lecture's rule for loaders applies to every tool that sets fields by name: a silent miss becomes lost data.
</details>

58. *Week 14 · trace.* Patch 1.3 renamed `Health.regen_per_s` to `regen_rate`. What does this loader print without and with the redirect table?

```python
from dataclasses import dataclass, field, fields

def prop(default, lo=None, hi=None, save=True):
    return field(default=default, metadata={"lo": lo, "hi": hi, "save": save})

@dataclass
class Health:
    current: int = prop(100, lo=0, hi=9_999)
    regen_rate: float = prop(1.5, lo=0.0, hi=50.0)     # was "regen_per_s" until patch 1.3

REDIRECTS = {("Health", "regen_per_s"): "regen_rate"}

def load(cls, data, redirects):
    obj, warnings = cls(), []
    declared = {f.name: f for f in fields(cls) if f.metadata["save"]}
    for key, value in data.items():
        key = redirects.get((cls.__name__, key), key)
        f = declared.get(key)
        if f is None:
            warnings.append(f"unknown field {cls.__name__}.{key}")
            continue
        lo, hi = f.metadata["lo"], f.metadata["hi"]
        setattr(obj, key, min(max(value, lo), hi))
    return obj, warnings

saved = {"current": 80, "regen_per_s": 4.0}
print(load(Health, saved, {}))
print(load(Health, saved, REDIRECTS))
```

<details>
<summary>Answer and worked solution</summary>

**Output:**

```text
(Health(current=80, regen_rate=1.5), ['unknown field Health.regen_per_s'])
(Health(current=80, regen_rate=4.0), [])
```

Without the redirect, the saved key matches no declared field, so `regen_rate` keeps its default of 1.5 and the designer's 4.0 is gone. This loader at least returns a warning; the lecture's section 2 loader does not, and every level would lose its tuning in silence. The redirect maps the old name to the new one before the lookup, as Unreal's Core Redirects do while assets load, and the value survives.
</details>

## Week 15: The engine as a whole

59. *Weeks 4, 8, 10, 11 · compute.* Your final engine's MMO town scene runs at 60 Hz, pipelined. The CPU stages are input 0.3 ms and animation 1.8 ms, plus three that you must compute from the lecture models: scripts (3,000 entities with per-object callbacks, `c_cross = 1.2` µs, `c_work = 0.3` µs), physics (400 awake bodies and 600 awake contacts, `a = 4` µs, `b = 1.5` µs) and render submission (1,500 draws sorted by material over 30 materials, `c_draw = 2` µs, `c_switch = 10` µs). The GPU takes 15.2 ms.
    (a) Compute `C`, `W` and what the player sees.
    (b) A raid doubles the scripted entities to 6,000. What happens?
    (c) You batch the scripts at `B = 100`. What does the player see now, and what is the new bottleneck?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `C = 12.39` ms, `W = 15.2` ms, 16.67 ms frames (60 fps), GPU-bound. (b) `C = 16.89` ms, frames of 33.33 ms (30 fps). (c) `C = 9.76` ms, back to 60 fps, with the GPU at 15.2 ms as the bottleneck.

(a) Scripts `3,000 × (1.2 + 0.3) = 4,500` µs. Physics `400 × 4 + 600 × 1.5 = 2,500` µs. Submission `1,500 × 2 + 29 × 10 = 3,290` µs. `C = 0.3 + 4.5 + 2.5 + 3.29 + 1.8 = 12.39` ms. `W = max(12.39, 15.2) = 15.2`, one refresh.

(b) Scripts become `6,000 × 1.5 = 9,000` µs, so `C = 12.39 − 4.5 + 9.0 = 16.89` ms. That is over 16.67, so the frame rounds up to 33.33 ms. The GPU's 1.47 ms of headroom does not help.

(c) `X = 60` crossings: `60 × 1.2 + 6,000 × 0.3 = 1,872` µs. `C = 16.89 − 9.0 + 1.87 = 9.76` ms. Now `W = 15.2`, 60 fps, and the next optimization belongs on the GPU. Week 13's loop in one question: find the bottleneck, change one thing, measure again, because the bottleneck moves.
</details>

60. *Weeks 1, 3, 5, 7, 12 · critique.* A team's final-engine design document says: (1) "Components hold `Texture*` pointers so the renderer can draw them fast." (2) "Save files store each entity's `(index, generation)` so references survive." (3) "`core/allocator.cpp` includes `engine/renderer.h` to report GPU memory in the same overlay." (4) "Particles use `new` and `delete`; the general allocator is fast enough in our benchmark." Find the problem in each, name the lecture that fixes it, and give the fix in one sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

1. **Raw pointers to resources (week 7, also weeks 2 and 5).** A hot reload or a free and reload into the same memory leaves the pointer dangling or pointing at the wrong texture. Store a generational resource handle and resolve it when drawing; the extra lookup is one indirection.
2. **Runtime handles in saves (weeks 5 and 12).** An `(index, generation)` pair means nothing in the next session, where slot 7 holds something else. Save persistent IDs and rebuild references with a two-pass loader.
3. **Upward dependency (week 1).** The core layer now names the renderer, so every renderer header change rebuilds the allocator and a port must read the renderer to port memory. Let the renderer push its numbers into a stats registry that lives in the core layer, or register a callback there at start-up.
4. **Wrong measure of success (week 3).** A one-size, one-thread, in-order benchmark is the general allocator's best case, and speed is not the main reason for a pool. Use a per-type pool: its cost never spikes, it never fragments externally, and its memory is one block you can see in the overlay.
</details>
