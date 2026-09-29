# CS201 · Week 03 — Memory Allocators: Stack, Pool and Frame

**Why this matters:** A game can run out of memory while half of it is free. It happens when the free memory is scattered in pieces too small for the next request, and on a console without virtual memory that is a crash in front of the player. Engines avoid it by grouping allocations by how long they live and giving each group its own allocator. This week you build the three allocators most engines use.

**You will be able to:**
- Compute the external fragmentation of a heap from its list of free runs, and trace a first-fit heap through a load sequence by hand.
- Implement a stack allocator with alignment and markers, and compute the padding a sequence of aligned requests wastes.
- Implement a pool allocator with an embedded free list and state its cost per allocation and its internal fragmentation.
- Choose an allocator (stack, double-ended stack, pool, frame, general heap) for a given lifetime pattern and defend the choice.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), section 6.2 "Memory Management" (stack, pool, single-frame and double-buffered allocators, and fragmentation). Pedriana, "EASTL" (WG21 paper N2271, 2007), the section "Game software issues" and appendix item 7 on permanent and temporary memory. Optional, 10 minutes: the comment block at the top of `WinQuake/zone.h` in id Software's Quake source on GitHub.

**Prerequisites from earlier courses:** [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (last in, first out). [CS102 week 5, arrays and linked lists](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md), section 4 (a linked list earns its place when you already hold the node). [CS201 week 1, runtime layers](w01-engine-anatomy-and-runtime-layers.md) (allocators live in the core layer; Doom and Quake). [CS201 week 2, ownership, relocation and dangling pointers](w02-cpp-for-engines-memory-raii-and-move-semantics.md).

**Interactive:** [`examples/w03-fragmentation.html`](../examples/w03-fragmentation.html). Keep it open during section 2.

---

## 1. What `new` costs

When you write `new Particle` or `std::malloc(20)`, the call goes to a **general-purpose allocator**, the heap manager that comes with your C++ runtime or OS. It must handle any size, in any order, from any thread, and it can't know how long each block will live. To do that it keeps lists of free blocks, searches them, splits big blocks, merges neighbors when they're freed, and usually takes a lock or uses per-thread caches so two threads don't corrupt its lists.

Modern general allocators are fast in the easy cases. The trouble for engines is elsewhere:

- **Fragmentation.** After many allocations and frees in mixed order, free memory ends up in many small runs between blocks that are still in use. This is **external fragmentation**. A request can fail even though the total free memory is far larger than the request. Section 2 shows it happening.
- **Unpredictable cost.** Most calls are quick, a few are slow (a search, a merge, a trip to the OS for more pages). A frame that happens to hit the slow path misses its deadline.
- **No lifetime knowledge.** The general allocator can't free "everything from this level" in one step, because it doesn't know which blocks belong to the level. You have to free each block, and you have to find each one first.

Pedriana's EASTL paper lists these problems from a big studio's point of view. It stresses that consoles of that era had no paged (virtual) memory, so fragmentation could kill an application, and that games often run with nearly all memory in use, which makes fragmentation worse. PCs and current consoles do have virtual memory, which hides some fragmentation by mapping scattered physical pages into contiguous addresses. It doesn't hide all of it: the address space and the pages still fragment, and a fragmented heap still wastes cache and TLB (page-table cache) entries.

### Lifetime is the key

An engine knows something the general allocator doesn't: how long each allocation will live. Nearly every allocation in a game falls into one of a few lifetime classes.

| Lifetime | Examples | Freed |
|---|---|---|
| Permanent | engine systems, the font atlas | at shutdown |
| Level | the level's meshes, navmesh, sound bank | when the level unloads, all at once |
| Frame | render command lists, temporary strings, collision query results | at the end of this frame, all at once |
| Object | a particle, a projectile, a network message | one at a time, in no fixed order |

Three of the four classes are freed *all at once*, in reverse order of when their class started. That is the LIFO shape of a stack, from CS102 week 6. The fourth class has a different gift: its objects are usually all the same size. Each shape gets an allocator that exploits it.

**Internal fragmentation** is the other kind of waste: bytes inside an allocated block that the caller didn't ask for, because the allocator rounded the size up. You'll see both kinds this week, and choosing an allocator is often a trade between them.

## 2. Worked example: out of memory with half the memory free

### The hook

Quake's memory manager, which id Software released with the rest of the Quake source in 1999, opens with a comment explaining the whole design. All the memory Quake uses is one contiguous block, the "hunk," allocated once at start-up. It hands out memory from *both* ends in a stack fashion, and the only way memory is released is by resetting one of the two pointers. EA's EASTL paper describes the same trick eight years later as a studio-wide practice: permanent memory from the top of the heap downward, temporary memory from the bottom, so permanent blocks pack tightly and don't leave dead spots.

Two studios, two decades apart, splitting one heap into two ends. What problem makes that worth doing?

### The model

A level load reads each asset file into a temporary **read buffer**, decompresses it into a permanent **asset** block, and frees the read buffer. Take a general heap that places each request at the lowest address where it fits. That policy is called **first fit**, and it is a common, reasonable choice.

Measure the damage with one number. List the **free runs**, the maximal stretches of contiguous free memory. Then:

```
free        = sum of all free runs
largest     = the longest free run
fragmentation = 1 − largest / free
```

Fragmentation 0% means all the free memory is in one piece. Fragmentation 80% means the largest piece is only one fifth of what's free. The request that matters is always the next big one, so `largest` is the number that decides whether it succeeds.

### Numbers you can check

A 100 MiB memory budget, empty at the start of the load. The level has six files. Each read buffer is smaller than its decompressed asset, and the files get a little bigger each time:

| File | Read buffer | Asset | Buffer placed at | Asset placed at | Hole left by the freed buffer |
|---|---|---|---|---|---|
| 1 | 4 | 6 | 0-4 | 4-10 | 0-4 (4 MiB) |
| 2 | 5 | 7 | 10-15 (5 doesn't fit in the 4 MiB hole) | 15-22 | 10-15 (5 MiB) |
| 3 | 6 | 8 | 22-28 | 28-36 | 22-28 (6 MiB) |
| 4 | 7 | 9 | 36-43 | 43-52 | 36-43 (7 MiB) |
| 5 | 8 | 10 | 52-60 | 60-70 | 52-60 (8 MiB) |
| 6 | 9 | 11 | 70-79 | 79-90 | 70-79 (9 MiB) |

Trace one row by hand to see the pattern. At file 2 the only hole is 4 MiB, too small for a 5 MiB buffer, so the buffer goes after file 1's asset. The 7 MiB asset doesn't fit in the 4 MiB hole either, so it goes after the buffer. Then the buffer is freed and leaves a 5 MiB hole. Each file leaves a hole one size too small for the next file.

After the load, the assets use 6 + 7 + 8 + 9 + 10 + 11 = 51 MiB. So 49 MiB is free, in seven runs: 4, 5, 6, 7, 8, 9 and the 10 MiB tail at 90-100. The largest run is 10 MiB. Fragmentation is `1 − 10/49 = 80%`.

Now the audio system asks for a 16 MiB streaming buffer. It fails. There are 49 MiB free.

Now split the heap into two ends, as Quake and EA do. Assets go to the top, packed downward: 94-100, 87-94, and so on down to 49-100. Each read buffer goes to the bottom, at address 0, and the bottom is reset after each file. When the load ends, the bottom is empty and the free memory is one run, 0-49. Fragmentation is 0%, and the 16 MiB request succeeds with 33 MiB to spare.

The whole experiment, in Python:

```python
ARENA = 100                                   # MiB of memory for the whole game
FILES = [(4, 6), (5, 7), (6, 8), (7, 9), (8, 10), (9, 11)]
#        (read buffer, decompressed asset) for each file in the level, in MiB


def first_fit(used, size):
    """Lowest address where `size` fits between the blocks in `used`."""
    cursor = 0
    for start, length in sorted(used):
        if start - cursor >= size:
            return cursor
        cursor = start + length
    return cursor if ARENA - cursor >= size else None


def free_runs(used):
    runs, cursor = [], 0
    for start, length in sorted(used):
        if start > cursor:
            runs.append(start - cursor)
        cursor = start + length
    return runs + ([ARENA - cursor] if cursor < ARENA else [])


def one_heap():
    used = []
    for buf, asset in FILES:
        b = (first_fit(used, buf), buf)
        used.append(b)
        used.append((first_fit(used, asset), asset))
        used.remove(b)                        # the read buffer is done
    return used


def two_ended():
    used, top = [], ARENA                     # assets from the top down
    for buf, asset in FILES:                  # buffers at the bottom, reset each file
        top -= asset
        used.append((top, asset))
    return used


for name, used in (("one heap", one_heap()), ("two ends", two_ended())):
    runs = free_runs(used)
    frag = 1 - max(runs) / sum(runs)
    print(f"{name}: free {sum(runs)} MiB in runs {runs}, largest {max(runs)}, "
          f"fragmentation {frag:.0%}")
```

```
one heap: free 49 MiB in runs [4, 5, 6, 7, 8, 9, 10], largest 10, fragmentation 80%
two ends: free 49 MiB in runs [49], largest 49, fragmentation 0%
```

Same files, same total memory, same free total. The only change is where each lifetime class is allowed to live.

### Open the interactive

The top view draws the 100 MiB arena as a horizontal bar, with permanent blocks in one color, read buffers in another and free space empty. Step through the six files with the "Next step" button (three steps per file) and watch the staircase of holes appear. The bottom view shows two numbers side by side, total free and largest run, as bars. Total free drops steadily in both modes. In "one heap" mode the largest-run bar collapses to 10 MiB while total free still says 49. Switch to "two ends" and replay: the largest-run bar tracks total free exactly. Then drag the "Request" slider to 16 MiB and press "Allocate request": red failure in one mode, green success in the other. The first view shows plenty of empty space, and the second shows why that space is useless.

### Cross-game recognition

**Quake (1996, GPL source 1999).** The hunk is a double-ended stack. `Hunk_AllocName` bumps the low end, `Hunk_HighAllocName` bumps the high end, and `Hunk_LowMark` and `Hunk_FreeToLowMark` save and restore the low end. After start-up the engine records a mark, `host_hunklevel`, and `Host_ClearMemory` frees everything above it with a single `Hunk_FreeToLowMark` call when a map changes. Every hunk allocation is rounded up to 16 bytes, which you'll recognize in section 3 as alignment. The same comment explains that video buffers are allocated from the high end so that changing video mode doesn't leave a hole under the server's allocations. That is this worked example's reasoning, in id's own words.

**Doom (1993, source released 1997).** Doom's zone allocator is a general heap, not a stack, but it attacks the same problem through lifetime tags. The Linux release takes one 6 MiB block from the OS at start-up (`mb_used = 6` in `i_system.c`), and every `Z_Malloc` call carries a tag such as `PU_STATIC`, `PU_LEVEL` or `PU_CACHE`. When a new level starts, `P_SetupLevel` calls `Z_FreeTags(PU_LEVEL, PU_PURGELEVEL - 1)` and every level-lifetime block goes in one call. The source has 65 `Z_Malloc` call sites outside the zone code itself (not counting one commented out). The 18 plain `malloc` calls sit in start-up and platform code.

**EA (2007, EASTL paper).** Pedriana describes separating memory into permanent and temporary classes: allocations made once at start-up or once per level are permanent and come from the top of the heap downward; allocations freed in arbitrary order are temporary and come from the bottom. He adds that some EA games would not have run at all without it.

Three code bases, one move: classify by lifetime, give each class its own end or its own tag, and free a class in one step. When you meet an engine's memory system, ask which lifetime classes it recognizes and where each one lives.

### Design judgment

- **Two ends need a lifetime discipline.** A permanent block allocated in the middle of a temporary phase is fine at the top. A temporary block that someone forgets to release pins the bottom forever. The double-ended stack gives you zero fragmentation only if every caller respects the classes.
- **You must size the arena in advance.** A single fixed hunk means a hard limit. Quake takes its hunk size from the command line (`-mem` on Linux, `-heapsize` on Windows); consoles give you a fixed budget anyway. On a PC with virtual memory you can reserve a large address range and commit pages as needed, which softens the limit.
- **General heaps are not the enemy.** Some allocations really are unpredictable (strings from chat, UI widgets). Leave them on a general heap, ideally a separate one, so their fragmentation doesn't spill into the level's memory. Doom kept a general heap and added tags. Quake kept a small general zone (about 48 KiB, its comment says) for command text.
- **Measure `largest`, not `free`.** An engine memory overlay that shows only total free memory will say "49 MiB free" right up to the failed allocation. Show the largest free run per heap. Lab 3 adds it to your allocator.

## 3. The stack allocator

A **stack allocator** owns one block and a single offset, `top`, that starts at 0. To allocate `n` bytes, it returns the address at `top` and adds `n`. That's the entire algorithm, often called **bump allocation**. It can't free an individual block. It can only roll `top` back.

Two additions make it usable.

**Alignment.** A type with alignment `a` must start at an address that is a multiple of `a`. A `double` or a pointer needs 8 on the platforms in this course, a SIMD vector of four floats needs 16. The allocator rounds the current address up to the next multiple of `a`, which, for `a` a power of two, is one line of bit arithmetic:

```
aligned = (address + a − 1) & ~(a − 1)
```

Adding `a − 1` pushes any address that isn't already a multiple past the next one, and the mask clears the low bits to land exactly on it. The skipped bytes are **padding**, internal fragmentation in the stack.

**Markers.** A **marker** is just a saved value of `top`. `free_to(marker)` rolls `top` back to it, freeing everything allocated since, in one assignment. Quake's `Hunk_LowMark` and `Hunk_FreeToLowMark` are exactly this.

```cpp
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

// A stack (bump) allocator over one block it owns.
class StackAllocator {
public:
    using Marker = std::size_t;

    explicit StackAllocator(std::size_t bytes)
        : base_(static_cast<std::uint8_t*>(std::malloc(bytes))), size_(bytes) {}
    ~StackAllocator() { std::free(base_); }
    StackAllocator(const StackAllocator&) = delete;
    StackAllocator& operator=(const StackAllocator&) = delete;

    // align must be a power of two.
    void* alloc(std::size_t bytes, std::size_t align) {
        std::uintptr_t start = reinterpret_cast<std::uintptr_t>(base_) + top_;
        std::uintptr_t aligned = (start + align - 1) & ~(std::uintptr_t)(align - 1);
        std::size_t new_top = (aligned - reinterpret_cast<std::uintptr_t>(base_)) + bytes;
        if (new_top > size_) return nullptr;          // out of memory: caller decides
        top_ = new_top;
        return reinterpret_cast<void*>(aligned);
    }

    Marker marker() const { return top_; }
    void free_to(Marker m) { top_ = m; }             // frees everything after m at once
    void reset() { top_ = 0; }

    std::size_t offset_of(const void* p) const {
        return static_cast<const std::uint8_t*>(p) - base_;
    }

private:
    std::uint8_t* base_;
    std::size_t size_;
    std::size_t top_ = 0;
};

int main() {
    StackAllocator level(1024);                      // malloc returns 16-byte aligned memory here
    struct Req { const char* what; std::size_t bytes, align; };
    Req reqs[] = {{"name (13 B)", 13, 4}, {"id (8 B)", 8, 8}, {"matrix (64 B)", 64, 16},
                  {"flags (3 B)", 3, 1}, {"count (4 B)", 4, 4}};
    for (const Req& r : reqs) {
        void* p = level.alloc(r.bytes, r.align);
        std::printf("%-14s align %2zu -> offset %3zu\n", r.what, r.align, level.offset_of(p));
    }
    std::printf("top after five allocations: %zu\n", level.marker());

    StackAllocator::Marker before_load = level.marker();
    level.alloc(500, 16);                            // temporary work while loading
    std::printf("top during load: %zu\n", level.marker());
    level.free_to(before_load);
    std::printf("top after free_to(marker): %zu\n", level.marker());
    std::printf("600 more bytes: %s\n", level.alloc(600, 16) ? "ok" : "nullptr");
    std::printf("1000 more bytes: %s\n", level.alloc(1000, 16) ? "ok" : "nullptr");
}
```

```
name (13 B)    align  4 -> offset   0
id (8 B)       align  8 -> offset  16
matrix (64 B)  align 16 -> offset  32
flags (3 B)    align  1 -> offset  96
count (4 B)    align  4 -> offset 100
top after five allocations: 104
top during load: 612
top after free_to(marker): 104
600 more bytes: ok
1000 more bytes: nullptr
```

Check the offsets by hand with the alignment formula, working in offsets because the base is 16-byte aligned:

| Request | `top` before | Rounded up to | Padding | `top` after |
|---|---|---|---|---|
| 13 B, align 4 | 0 | 0 | 0 | 13 |
| 8 B, align 8 | 13 | 16 | 3 | 24 |
| 64 B, align 16 | 24 | 32 | 8 | 96 |
| 3 B, align 1 | 96 | 96 | 0 | 99 |
| 4 B, align 4 | 99 | 100 | 1 | 104 |

Twelve bytes of padding for 92 bytes of data, 11.5% of the space used. Sort the same requests from largest alignment to smallest, and within one alignment put the sizes that are multiples of it first (64/16, 8/8, 4/4, 13/4, 3/1). The offsets become 0, 64, 72, 76 and 89, the end is 92, and the padding drops to zero. Ordering allocations by alignment is a cheap trick when you control the order, for example when laying out a level's data at build time.

The stack allocator costs one addition and one comparison per allocation, never fragments externally, and frees any number of blocks in one assignment. Its rule is strict: you may only free in reverse order, and only by marker. A caller who keeps a pointer to something above a marker after `free_to` holds a dangling pointer, week 2's bug in a new place.

### Double-ended stack

Put two stacks in one block, one growing up from the bottom and one growing down from the top. Allocation fails only when the two tops would cross. That is Quake's hunk and the "two ends" arrangement from section 2. It lets two lifetime classes share one budget without either one reserving a fixed share.

## 4. The pool allocator

The object lifetime class, particles and projectiles freed one at a time in any order, doesn't fit a stack. It usually fits a **pool**: a block cut into `count` slots of one fixed size. Because every slot is the same size, any free slot satisfies any request, so the allocator never searches and never fragments externally.

The free slots are kept in a **free list**, a singly linked list threaded through the free slots themselves. A free slot isn't holding an object, so its first bytes can hold the pointer to the next free slot. The list costs no memory beyond the slots. Allocation pops the head. Freeing pushes onto the head. Both are O(1), a couple of pointer moves. This is the case CS102 week 5 described where a linked list wins: you always hold the node you want, the head.

```cpp
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <new>

// A pool of fixed-size blocks. Free blocks form a linked list that is stored
// inside the free blocks themselves, so the list costs no extra memory.
class PoolAllocator {
public:
    // Every block starts on a 16-byte boundary, enough for any scalar or SIMD
    // type and for the free-list pointer. (std::malloc returns 16-byte aligned
    // memory on the 64-bit desktop platforms this course uses.)
    PoolAllocator(std::size_t block_size, std::size_t count)
        : block_(round_up(block_size < sizeof(Node) ? sizeof(Node) : block_size)),
          memory_(static_cast<std::byte*>(std::malloc(block_ * count))) {
        for (std::size_t i = count; i-- > 0;) {        // push in reverse so block 0 comes out first
            push(memory_ + i * block_);
        }
    }
    ~PoolAllocator() { std::free(memory_); }
    PoolAllocator(const PoolAllocator&) = delete;
    PoolAllocator& operator=(const PoolAllocator&) = delete;

    void* alloc() {
        if (!head_) return nullptr;
        Node* n = head_;
        head_ = n->next;
        return n;
    }
    void free(void* p) { push(static_cast<std::byte*>(p)); }

    std::size_t block_size() const { return block_; }
    std::size_t index_of(const void* p) const {
        return (static_cast<const std::byte*>(p) - memory_) / block_;
    }

private:
    struct Node { Node* next; };
    static std::size_t round_up(std::size_t n) {
        return (n + 15) / 16 * 16;
    }
    void push(std::byte* p) { head_ = new (p) Node{head_}; }

    std::size_t block_;
    std::byte* memory_;
    Node* head_ = nullptr;
};

struct Particle { float x, y, vx, vy, life; };      // 20 bytes

int main() {
    PoolAllocator pool(sizeof(Particle), 4);
    std::printf("particle %zu bytes, block %zu bytes\n", sizeof(Particle), pool.block_size());
    void* a = pool.alloc();
    void* b = pool.alloc();
    void* c = pool.alloc();
    std::printf("a=%zu b=%zu c=%zu\n", pool.index_of(a), pool.index_of(b), pool.index_of(c));
    pool.free(b);                                    // b's block goes to the front of the list
    void* d = pool.alloc();
    std::printf("d reuses block %zu\n", pool.index_of(d));
    void* e = pool.alloc();
    void* f = pool.alloc();
    std::printf("e=%zu f=%s\n", pool.index_of(e), f ? "a block" : "nullptr (pool full)");
}
```

```
particle 20 bytes, block 32 bytes
a=0 b=1 c=2
d reuses block 1
e=3 f=nullptr (pool full)
```

Two things to read off the output. First, the pool is LIFO: the block freed last is handed out next. That's good for the cache, because the most recently freed block is the one most likely still in it. Second, the 20-byte particle occupies a 32-byte block. That's internal fragmentation of 12 / 32 = 37.5%. The 16-byte rounding is there so the same pool works for SIMD types. For a pool that holds only particles, you could align to 4 bytes (the alignment of `float`), but then the block must still be at least 8 bytes and 8-aligned to hold the free-list pointer, so 24 bytes and 17% waste. Pools are sized per type for exactly this reason.

How much faster is it? On the reference machine (Apple M4 Pro, clang 17, `-O2`), creating and destroying 5,000 particles with `new` and `delete` took about 0.070 ms per frame, and with the pool about 0.006 ms, roughly 12 times less (median of five runs of case 1 in Lab 3's `bench.cpp`). Be honest about what that says. The general allocator was already fast here, because the test is its best case: one size, one thread, freed in order. The pool's bigger wins are that its cost never spikes, it never fragments, and the particle memory is one contiguous block you can see in a memory overlay. Lab 3 has you rerun this benchmark with mixed sizes and random free order, where the general allocator has to work harder.

A pool also makes **compaction** possible. If game code refers to particles by slot index rather than by address (week 2's handles), the engine can move live objects to close gaps, because no pointer needs updating. [Week 7](w07-resource-management-and-hot-reload.md) relies on this for resources.

## 5. The frame allocator

The frame lifetime class, memory that lives until the end of this frame, is a stack allocator with one extra rule: call `reset()` at the end of every frame. That is a **single-frame allocator**. Render command lists, temporary strings for the debug overlay, the list of entities a raycast hit: allocate them freely, never free any of them, and the whole lot vanishes in one assignment when the frame ends. [Week 4](w04-the-frame-update-render-present.md) places that reset in the frame at the step it calls "end of frame."

The single-frame allocator has one failure mode worth naming. Data that must survive into the next frame, such as the render commands the GPU is still reading while the CPU prepares the next frame, would be overwritten. The fix is a **double-buffered frame allocator**: two stacks, used on alternate frames. At the start of frame N, reset the stack used in frame N − 2 and make it current. Anything allocated in frame N stays valid through frame N + 1. Gregory's section 6.2 describes both.

Frame allocators are also the safest allocator in the engine to misuse, and the most dangerous to misuse silently. A pointer into frame memory that is kept past the reset points at whatever the next frame wrote there. In debug builds, fill the stack with a recognizable byte pattern (for example `0xCD`) on every reset, so stale reads produce obviously wrong values instead of plausible ones.

## 6. Choosing an allocator

| Lifetime | Pattern | Allocator | Cost per alloc | Frees | Fragmentation |
|---|---|---|---|---|---|
| Permanent | once at start-up | top of a double-ended stack | bump | never (or at shutdown) | none |
| Level | during load, all freed together | stack with a marker at level start | bump | one `free_to` | padding only |
| Frame | any time in a frame | frame stack, reset each frame (double-buffer if read next frame) | bump | one `reset` | padding only |
| Object, one size | any order | pool per type | pop | push | internal (rounding) only |
| Unpredictable | any size, any order | general heap, kept separate | varies | one at a time | external |

Most engines use all five, carved out of a few large blocks taken from the OS at start-up. The payoff is the one section 2 measured. Fragmentation is confined to the one heap that genuinely needs a general allocator. Everything else frees in one step, and the memory overlay can say exactly how much each lifetime class is using.

## In-class activity (25 minutes)

Work in pairs with the interactive open.

1. Switch the interactive to "custom" and enter this load sequence (read buffer, asset, in MiB): (3, 8), (9, 4), (2, 6), (10, 5), (4, 7). Before pressing play, predict on paper where first fit puts every block, and compute total free, largest run and fragmentation at the end. (10 min)
2. Press play and check. Where were you wrong? (5 min)
3. Reorder the same five files to bring one-heap fragmentation below 5%. (No order reaches 0%; the best is about 3%.) Explain in one sentence why your order works. (5 min)
4. Write down, for your team's final engine project, three allocations it will make, their lifetime class, and the allocator from section 6 you'll use. (5 min)

Expected output: the hand trace with the three numbers, the reordering, and the three-row allocation plan.

## Common misconceptions

- **"If there's enough free memory, allocation succeeds."** Only if enough of it is contiguous. Section 2 fails a 16 MiB request with 49 MiB free.
- **"Custom allocators are about speed."** Speed helps, but the general allocator is often fast enough. The bigger reasons are predictable cost, no external fragmentation, and freeing a whole lifetime class in one step.
- **"A pool wastes nothing because every block is used."** Every block is rounded up to the pool's block size and alignment. A 20-byte particle in a 32-byte block wastes 37.5%.
- **"Resetting the frame allocator frees the objects."** It frees the memory. It does not run destructors. Put only trivially destructible data in a frame allocator, or run the destructors yourself before the reset.

## Check yourself

1. A heap has free runs of 12, 3, 30, 5 and 10 KiB. Compute total free, largest run and fragmentation. Can a 20 KiB request succeed? A 32 KiB one?
2. A stack allocator's `top` is at offset 37 (base 16-byte aligned). You request 24 bytes with alignment 8, then 16 bytes with alignment 16, then 1 byte with alignment 1. Give each returned offset, the padding, and the final `top`.
3. You need a pool for 10,000 `Projectile` objects of 44 bytes, alignment 4. Using this lecture's 16-byte rounding, what is the block size, the pool size in bytes, and the internal fragmentation? What is the smallest block size that still holds the free-list pointer if you round to 8 instead?
4. In section 2's one-heap mode, the level designer adds a seventh file with a 10 MiB buffer and a 12 MiB asset. Where do they go, and what is the fragmentation after the load?

<details>
<summary>Answers</summary>

1. Total 60 KiB, largest 30 KiB, fragmentation `1 − 30/60 = 50%`. 20 KiB succeeds (fits in the 30 run). 32 KiB fails even though 60 KiB is free.
2. 37 rounds up to 40 (padding 3), block at 40, `top` 64. 64 is already a multiple of 16 (padding 0), block at 64, `top` 80. 80 (padding 0), block at 80, `top` 81. Total padding 3 bytes.
3. 44 rounds up to 48. Pool size 10,000 × 48 = 480,000 bytes. Internal fragmentation 4/48 = 8.3%. Rounding to 8: 44 rounds up to 48 as well, since 48 is the next multiple of 8. (At 40 bytes the two rules would differ: 48 versus 40.)
4. After six files the free runs are 4, 5, 6, 7, 8, 9 at the bottom and 90-100 at the top. The 10 MiB buffer doesn't fit any hole below 90, so it goes at 90-100. The 12 MiB asset fits nowhere: the largest run left is 9 MiB. The load fails, with 39 MiB free. In two-ends mode the assets use 63 MiB at the top, the 10 MiB buffer fits at the bottom, and the load succeeds with 37 MiB free in one run.

</details>

## Lab / assignment hook

[Lab 03, three allocators](../labs/lab03.md). You implement a stack allocator with markers, a double-ended stack with a `largest_free()` report, and a pool allocator, and the tests check alignment, markers, pool reuse and that nothing touches the global heap after start-up. You then rerun the particle benchmark with mixed sizes and random free order and explain the result.

## Sources

- id Software, *Quake* source code, `WinQuake/zone.h` and `zone.c` (GPL release, December 21, 1999; GitHub `id-Software/Quake`). The hunk design comment (one contiguous block, low and high stack ends, release only by resetting a pointer, 16-byte alignment, video buffers allocated high, a small zone for command text), `Hunk_AllocName`, `Hunk_HighAllocName`, `Hunk_LowMark`, `Hunk_FreeToLowMark`, `host_hunklevel` in `host.c`. Paraphrased.
- id Software, *DOOM* source code, `linuxdoom-1.10` (released December 23, 1997; GitHub `id-Software/DOOM`). `z_zone.h` purge tags, `Z_FreeTags` in `z_zone.c`, the call in `p_setup.c`, `mb_used = 6` and `I_ZoneBase` in `i_system.c`; 65 live `Z_Malloc` call sites counted with `grep "Z_Malloc *("` outside `z_zone.c`, minus one commented-out line.
- Pedriana, P. (2007). "EASTL: Electronic Arts Standard Template Library." WG21 paper N2271, open-std.org. Fragmentation on consoles without paged memory, games running with nearly all memory allocated, pools, and the permanent/temporary (high/low) heap technique. Paraphrased.
- Gregory, J. (2018). *Game Engine Architecture* (3rd ed.). CRC Press. Section 6.2: stack, double-ended stack, pool, single-frame and double-buffered frame allocators, alignment, fragmentation.
- Benchmark in section 4 (about 0.070 ms vs 0.006 ms per frame for 5,000 particles, median of five runs) measured with case 1 of `labs/lab03-starter/bench.cpp` and a reference `PoolAllocator`, Apple clang 17, `-O2`, Apple M4 Pro, September 2026.

## Interactive spec: examples/w03-fragmentation.html

**The one insight:** total free memory is the wrong number. The same files in the same budget leave one big free run or many useless small ones, depending only on where each lifetime class is allowed to live.

**Layout.** Two linked views stacked vertically (arena on top, numbers below) at every width.

- **Top view, "Arena".** A horizontal bar for the whole arena (default 100 MiB), with tick marks every 10 MiB and labels at 0, 50, 100. Draw permanent assets as solid blocks (accent color, labeled "A1".."An" when wide enough), live read buffers as hatched blocks (secondary color, "B1".."Bn"), free space empty with a thin outline. When a buffer is freed, flash its hole briefly (skip the flash under `prefers-reduced-motion`). Under the bar, list the free runs as text: "Free runs: 4, 5, 6, 7, 8, 9, 10".
- **Bottom view, "What the next request sees".** Two horizontal bars on the same scale as the arena: "Total free" and "Largest free run", each with its exact value in MiB. Beside them: "Fragmentation = 1 − largest / free = X%". A request marker (vertical line) at the current request size across both bars, so the student sees it fit under "Total free" but not under "Largest free run".

**Controls.**
- Toggle "Mode": "One heap (first fit)" (default) and "Two ends (assets top, buffers bottom)".
- Buttons "Next step", "Play" (one step per 600 ms; instant under reduced motion), "Reset". A step is one of: place buffer, place asset, free buffer. A step counter shows "File k of n, step s of 3".
- Select "Load sequence": "Lecture: growing files" (default: (4,6), (5,7), (6,8), (7,9), (8,10), (9,11)), "Activity" ((3,8), (9,4), (2,6), (10,5), (4,7)), and "Custom" (a text field accepting pairs like `4,6; 5,7`; validate that every number is a positive integer).
- Slider "Request (MiB)": 1 to 60, default 16. Button "Allocate request" runs first fit (one-heap mode) or allocates from the bottom (two-ends mode) against the current arena and shows green "fits at X-Y" or red "fails: largest run is Z MiB, Q MiB free". It does not change the arena.
- Number input "Arena (MiB)": 50 to 200, default 100.
- All controls keyboard reachable; values update immediately.

**Exact algorithms.**
- One heap. For each file (buffer b, asset a): place b at the lowest start s such that [s, s+b) overlaps no used block and s+b ≤ arena; then place a the same way (the buffer is still in use); then remove b. If a placement fails, stop and show "Load failed at file k: needed X MiB, largest run Y MiB".
- Two ends. Keep `top = arena`. For each file: place b at [0, b); place a at [top − a, top) and set `top -= a`; remove b. Fail if b > top − a before placing a.
- Free runs: maximal gaps between sorted used blocks, including the gap before the first block and after the last. Fragmentation = 1 − max(runs) / sum(runs), shown as a whole percent; 0% when there is one run; "n/a" when nothing is free.

**Test values.**
- Lecture sequence, one heap, arena 100: final assets at 4-10, 15-22, 28-36, 43-52, 60-70, 79-90; free runs 4, 5, 6, 7, 8, 9, 10; total 49; largest 10; fragmentation 80%. Request 16: fails. Request 10: fits at 90-100.
- Lecture sequence, two ends: assets at 94-100, 87-94, 79-87, 70-79, 60-70, 49-60; one run 0-49; fragmentation 0%. Request 16: fits at 0-16.
- Lecture sequence plus a seventh file (10, 12), one heap: buffer at 90-100, asset fails ("needed 12 MiB, largest run 9 MiB"), 39 MiB free at the failure point (after the buffer is placed, 39 MiB free; show the state at failure). Two ends: succeeds, one run of 37 MiB.
- Activity sequence, one heap: assets at 3-11, 20-24, 11-17, 34-39, 39-46; free runs 3, 3, 10, 54; total 70; largest 54; fragmentation 23%. Best reordering for the activity: (4,7), (2,6), (10,5), (3,8), (9,4), runs 2 and 68, fragmentation 3%.
- After file 1 only, one heap: buffer freed, runs 4 and 90 (0-4 and 10-100), fragmentation 1 − 90/94 = 4%.

**First screen.** The lecture sequence already played to the end in one-heap mode, with the request at 16 MiB shown failing, and the caption "49 MiB free. The largest piece is 10 MiB." A one-line hint below: "Switch to Two ends."
