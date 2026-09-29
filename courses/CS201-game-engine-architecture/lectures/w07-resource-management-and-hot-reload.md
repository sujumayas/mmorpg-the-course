# CS201 · Week 07 — Resource Management and Hot Reload

**Why this matters:** A game is mostly data. Textures, meshes, sounds and levels can be a hundred times larger than the code that uses them, and the part of the engine that finds, loads, shares and frees that data decides how long players stare at a loading screen and how much memory the game eats. The same system decides how fast your artists can iterate: if a changed texture shows up in the running game in a second, they try forty ideas an hour instead of four.

**You will be able to:**
- Compute load time from the number of reads and the bytes read, find the read size where access time stops dominating, and use it to choose a file layout.
- Implement a resource cache that loads each asset once and frees it when its reference count reaches zero.
- Implement generational handles and explain which bugs they catch that raw pointers cannot.
- Design a hot-reload path that swaps data behind handles, rebuilds dependents in the right order and never swaps mid-frame.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed.), chapter 7, "Resources and the File System" (sections 7.1 and 7.2). Godot Engine documentation (4.x), "Resources" (a single page). Unity Addressables manual (1.21), "Memory management" and its reference-counting subpage.

**Prerequisites from earlier courses:** [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (you built live reload for a data table there: poll the modification time, validate, keep the last good table, pass ids instead of copies; this week does not repeat any of it). [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (the cache is a hash map). [AR101 week 14, pipeline, atlases and import settings](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) (what a texture costs in memory). [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (the shape of section 2's curve). From this course, [week 2](w02-cpp-for-engines-memory-raii-and-move-semantics.md) and [week 3](w03-memory-allocators-stack-pool-and-frame.md) on ownership, RAII and allocators, [week 4](w04-the-frame-update-render-present.md) on the frame, and [week 5](w05-entity-component-system-design.md) on generational handles.

**Interactive:** [w07-seeks-vs-bytes.html](../examples/w07-seeks-vs-bytes.html). Keep it open during section 2.

---

## 1. What the resource manager owns

Start with vocabulary, because engines use these words loosely.

A **resource** (or **asset**) is a piece of data the game loads from storage: a texture, a mesh, an animation clip, a sound, a compiled shader, a level. It is usually read-only at runtime and shared. Five hundred goblins can use one goblin texture.

An **instance** is a thing in the game world that uses a resource. Each goblin is an instance with its own position and health. The texture is not copied into each goblin. The goblin holds a reference to it.

The **resource manager** is the engine subsystem that sits between the two. It has five jobs:

1. **Find.** Turn a name the game uses (`"textures/goblin"`, or a numeric asset id) into a place in storage.
2. **Load once.** If the resource is already in memory, hand back the copy that is there.
3. **Share and track.** Know who is using each resource, so it knows when nobody is.
4. **Free.** Release memory when a resource is no longer needed, and not a frame earlier.
5. **Reload.** Replace a resource's contents while the game runs, without breaking everyone who holds it.

Jobs 2 to 5 are about memory and lifetime, and they build directly on week 2's ownership rules. Job 1 looks like bookkeeping, but it hides the biggest number in the whole subsystem, the time it takes to get bytes off a drive. That is where the worked example starts.

### Offline and runtime halves

Most engines split resource work into two halves. The **offline** half, often called the asset pipeline or "cooking", converts source files (a layered paint file, an exported mesh) into formats the runtime can use directly: compressed textures with mip levels, vertex buffers in the GPU's layout. AR101 week 14 covered the artist's side of this. The **runtime** half, this week's subject, loads the cooked output. The rule that connects them is simple: do every expensive conversion offline, so the runtime only copies bytes. A texture that the game must decode from PNG and compress at load time costs you load time on every player's machine, every time.

## 2. Worked example: seeks versus bytes

### The hook

Before the PlayStation 5, some console games stored the same asset many times on the hard drive, on purpose. Mark Cerny, the PS5's lead architect, described this in his March 2020 system presentation: slow hard drives limited how much data a game could load, where it had to sit on the disk, and how much of it developers duplicated to cut load times. Wasting gigabytes of disk to save seconds of loading sounds backwards. By the end of this section you will be able to compute when it is the right call, and why it stopped being right on solid-state drives.

### The model

Reading a file from storage costs two things. First you wait for the drive to get to the data. Then you wait while the data streams out.

```
T = S × t_a + B / R
```

- `T` is the total load time in seconds.
- `S` is the number of separate reads (seeks).
- `t_a` is the **access time**: the fixed wait before each read starts. On a spinning hard drive it is the head moving to the right track (the seek) plus half a rotation on average. On a solid-state drive it is much smaller, but not zero.
- `B` is the number of bytes read, in megabytes here.
- `R` is the drive's sustained transfer rate, in MB/s.

The first term counts reads. The second counts bytes. A layout that cuts reads can afford to read somewhat more bytes, and the model tells you exactly how much.

Now ask what rate you really get when every read is `b` megabytes long. One read takes `t_a + b/R`, so the **effective rate** is:

```
R_eff = b / (t_a + b/R) = R × b / (b + b*)       where   b* = t_a × R
```

This is the rational-function shape from MA101 week 6. `R_eff` climbs toward `R` and never reaches it. The constant `b* = t_a × R` has a plain meaning: **it is the read size at which you get exactly half the drive's rated speed.** Reads much smaller than `b*` spend most of their time waiting. Reads much larger than `b*` spend most of their time transferring. Call `b*` the knee of the drive.

### Numbers you can check

Take two drives with round numbers. The hard drive is laptop-class: a common mobile drive seeks in about 12 ms and a 5,400 rpm platter adds about 5.6 ms of rotational wait on average, so `t_a = 15 ms` is a fair round figure, with `R = 100 MB/s`. The solid-state drive gets `t_a = 0.1 ms` and `R = 5,500 MB/s`, the PS5's rated raw bandwidth. Treat the access times as assumptions for the exercise. Real drives vary, and the interactive lets you change them.

```python
def load_time(reads, megabytes, access_ms, rate_mb_s):
    """Seconds to load `megabytes` split into `reads` separate reads."""
    return reads * access_ms / 1000 + megabytes / rate_mb_s

def effective_rate(read_mb, access_ms, rate_mb_s):
    """MB/s you really get when every read is `read_mb` long."""
    return read_mb / load_time(1, read_mb, access_ms, rate_mb_s)

HDD = (15.0, 100.0)    # access ms, MB/s: assumed laptop-class hard drive
SSD = (0.1, 5500.0)    # access ms, MB/s: assumed fast NVMe-class drive

for name, drive in (("HDD", HDD), ("SSD", SSD)):
    print(name, "knee b* =", drive[0] / 1000 * drive[1], "MB")
    for read_mb in (0.064, 0.5, 1.5, 4, 16):
        print(f"  {read_mb:>6} MB reads -> {effective_rate(read_mb, *drive):7.1f} MB/s")
```

Output, as a table:

| Read size | HDD effective rate | Share of HDD peak | SSD effective rate | Share of SSD peak |
|---|---|---|---|---|
| 64 KB | 4.1 MB/s | 4% | 573 MB/s | 10% |
| 0.5 MB | 25.0 MB/s | 25% | 2,619 MB/s | 48% |
| 1.5 MB | 50.0 MB/s | 50% | 4,024 MB/s | 73% |
| 4 MB | 72.7 MB/s | 73% | 4,835 MB/s | 88% |
| 16 MB | 91.4 MB/s | 91% | 5,317 MB/s | 97% |

The hard drive's knee is `0.015 × 100 = 1.5 MB`, and the table confirms 50% there. A game that loads 64 KB files one at a time from a hard drive gets 4% of the speed on the box. The SSD's knee is 0.55 MB, so small reads hurt it too, but its absolute rates are 60 to 140 times the hard drive's.

### The duplication trade

Now the level. A city has 20 districts. Entering a district loads 200 MB: 140 MB of assets unique to that district, and 60 MB of shared props (lamp posts, mailboxes, benches) spread over 300 small files of about 0.2 MB each. You can lay the disk out two ways.

- **Store once.** Each district's unique data is one contiguous block, one read. The shared props live once, somewhere else, and each needs its own read. `S = 1 + 300 = 301`.
- **Duplicate.** Copy the 60 MB of shared props into every district's block. Now a district is one contiguous read, `S = 1`, and the disk holds 20 copies of the props.

Let a slider `f` say what fraction of the shared props get duplicated. Reads are `1 + 300 × (1 − f)`. Disk use is `140 × 20 + 60 × (1 − f) + 60 × f × 20` MB.

```python
def load_time(reads, megabytes, access_ms, rate_mb_s):
    return reads * access_ms / 1000 + megabytes / rate_mb_s

def district(dup_fraction, districts=20, access_ms=15.0, rate=100.0):
    shared_files, shared_mb, unique_mb = 300, 60.0, 140.0
    reads = 1 + round(shared_files * (1 - dup_fraction))
    seconds = load_time(reads, unique_mb + shared_mb, access_ms, rate)
    disk_mb = unique_mb * districts + shared_mb * (1 - dup_fraction) \
              + shared_mb * dup_fraction * districts
    return reads, round(seconds, 3), round(disk_mb)

for f in (0.0, 0.5, 0.9, 1.0):
    print(f, "HDD", district(f), "SSD", district(f, access_ms=0.1, rate=5500.0))
```

| Duplicated `f` | Reads | HDD load | SSD load | Disk used |
|---|---|---|---|---|
| 0 (store once) | 301 | 6.52 s | 0.066 s | 2,860 MB |
| 0.5 | 151 | 4.27 s | 0.051 s | 3,430 MB |
| 0.9 | 31 | 2.47 s | 0.039 s | 3,886 MB |
| 1 (duplicate all) | 1 | 2.02 s | 0.036 s | 4,000 MB |

On the hard drive, duplication cuts the load from 6.5 s to 2.0 s, a factor of 3.2, for 40% more disk. That is a trade many shipped games took. On the SSD the same 1.14 GB of duplicates saves 30 milliseconds, less than two frames at 60 Hz. The model says stop duplicating, which is the change Cerny's presentation described for a console built around an SSD.

### A visual you can move

Open the interactive. The left view plots `R_eff` against read size on a log axis for the chosen drive, with the knee marked. The right view shows the district: a bar for load time split into "waiting" (the `S × t_a` part) and "transferring" (the `B/R` part), and a bar for disk use. Drag the duplication slider with the hard drive selected and the waiting segment shrinks while the disk bar grows. Switch to the SSD and the waiting segment is a sliver whatever you do. The insight the picture must make obvious: **duplication buys back access time, so it only pays when access time is a large share of the load.**

### Cross-game recognition

Every packaging scheme you will meet is a way to make `b` large or `S` small.

- **Doom (1993).** id Software packed levels, textures and sounds into WAD files ("Where's All the Data?"). One big file means one open and long sequential reads. The same format made modding possible, because a patch WAD could replace entries without touching the engine.
- **Unreal Engine 5 (5.8 documentation).** Cooking produces `.pak` files, one per chunk. Assets that belong together go into the same chunk, which is the district layout above with a different name, and chunks can ship separately as downloadable content or patches.
- **Godot 4.** Exported games read from resource packs, `.pck` files (or ZIP). The documentation pitches them for patches, DLC and mods, the same roles as Doom's patch WADs.
- **Unity Addressables (1.21).** Assets are grouped into AssetBundles. Section 3 returns to them, because the bundle is also Unity's unit of freeing memory.
- **Downloads.** On mobile and web the "drive" is the network. A request's round trip is a large `t_a` and the connection's bandwidth is `R`. The knee is often hundreds of kilobytes or more, so the same rule says bundle small files for download.

Five contexts, one formula. When you meet a new packaging system, ask what its `t_a` is, what its `R` is, and how the layout moves `b` relative to `b*`.

### Eyes-open design judgment

- **Group by what loads together, not by type.** A folder of all textures and a folder of all meshes forces one read per type per level. Group by district, by encounter or by menu screen.
- **Duplication has costs beyond disk.** A patch that fixes one duplicated lamp post must ship 20 copies. Install size is also something players see on the store page before they buy.
- **Measure the drive you ship on.** A layout tuned for a hard drive wastes disk on an SSD. A layout tuned for an SSD can be three times slower on a hard drive. If you ship on both, pick the layout per platform in the cooker.
- **Opening a file is also an access.** Even on an SSD, the operating system's per-file open cost behaves like a small `t_a`. Thousands of loose files are slow on every drive, so pack them even when you stop duplicating.

### Check yourself (worked example)

1. A drive has `t_a = 8 ms` and `R = 200 MB/s`. What is its knee? What effective rate do 256 KB reads get?
2. A menu screen loads 120 icons of 40 KB each from the laptop hard drive above. Compute the load time for loose files and for one packed file.
3. In the district example with the hard drive, at what duplicated fraction `f` does the load time first drop below 3 seconds?

<details>
<summary>Answers</summary>

1. `b* = 0.008 × 200 = 1.6 MB`. `R_eff = 200 × 0.256 / (0.256 + 1.6) = 27.6 MB/s`, about 14% of peak.
2. Bytes are `120 × 0.04 = 4.8 MB`, so transfer is 0.048 s either way. Loose: `120 × 0.015 + 0.048 = 1.848 s`. Packed: `0.015 + 0.048 = 0.063 s`. Packing is 29 times faster.
3. Transfer is 2.0 s, so waiting must drop below 1.0 s, which means fewer than 66.7 reads. `1 + 300 × (1 − f) < 66.7` gives `f > 0.781`. At `f = 0.79` there are 64 reads and the load takes 2.96 s.

</details>

## 3. Load once, share, free: the reference-counted cache

Loading fast matters only if you load each thing once. The standard structure is a hash map from resource name to an entry holding the loaded data and a **reference count**: the number of current users.

```python
class ResourceCache:
    def __init__(self, loader):
        self.loader = loader
        self.entries = {}          # path -> [data, refcount]
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
        if entry[1] == 0:
            del self.entries[path]     # a real engine may keep it in an LRU list

cache = ResourceCache(loader=lambda path: f"<pixels of {path}>")
goblins = [cache.acquire("goblin.png") for _ in range(500)]
boss = cache.acquire("ogre.png")
print(cache.disk_loads, cache.entries["goblin.png"][1])   # 2 500
for _ in range(500):
    cache.release("goblin.png")
print(sorted(cache.entries))                               # ['ogre.png']
```

Five hundred goblins cost one disk load and one copy in memory. When the last goblin releases the texture, the count reaches zero and the entry goes. Every `acquire` must be matched by exactly one `release`. Miss a release and the texture never leaves memory, a leak. Release twice and the count reaches zero while someone still uses the texture, which is worse. In C++ you make the pairing automatic with week 2's RAII: a small handle object whose constructor acquires and whose destructor releases, so the compiler writes the release for you on every exit path.

### Freeing at zero is a policy, not a law

Deleting at count zero is the simplest policy and often the wrong one. A player walks out of a district and straight back in. Freeing the district's textures the instant the count hits zero means loading them again two seconds later. Many engines keep zero-count resources in a **least-recently-used (LRU) list** with a memory budget, and evict the oldest only when a new load needs the room. The count answers "may this be freed?" and the budget answers "must it be freed now?". Keep those two questions separate in your design.

### Two engines, same counter

- **Godot 4.** The documentation says a resource loaded from disk is loaded only once. Loading the same path again returns the copy already in memory. Resources inherit reference-counted memory management from Godot's `RefCounted` class, and a resource nobody references is freed.
- **Unity Addressables (1.21).** Each load increments a count and each release decrements it. The catch is granularity: an asset lives inside an AssetBundle, and Unity can load part of a bundle but cannot unload part of one. Memory returns only when the whole bundle's count reaches zero, unless you call `Resources.UnloadUnusedAssets`, which the manual warns is slow enough to cause frame hitches.

The Unity case links straight back to section 2. Big bundles make `b` large and loads fast. Big bundles also make the unit of freeing large, so one prop still in use can pin a whole district in memory. The layout decision is a load-time decision and a memory decision at once.

## 4. Handles, not pointers

The cache hands out the data itself. That is fine until something is freed or replaced. Suppose an instance keeps a raw pointer to a texture, the texture is freed, and a new texture is loaded into the same memory. The old pointer now points at the wrong texture. Nothing crashes. The goblin is drawn with the ogre's skin. This is a **dangling pointer** that happens to land on live data, and it is one of the hardest bugs to find because the symptom appears far from the cause.

The engine fix is the generational handle you built for entities in [week 5](w05-entity-component-system-design.md), applied to resources. As a reminder, a **handle** is a small value, typically two integers: an **index** into a table of slots, and a **generation** number. Each slot also stores a generation. When a resource is destroyed, its slot's generation goes up by one, and the slot can be reused. A lookup succeeds only if the handle's generation matches the slot's. Here is the pool in C++, as your engine will hold it:

```cpp
#include <cstdint>
#include <cstdio>
#include <vector>

struct Handle { std::uint32_t index; std::uint32_t generation; };

template <typename T>
class Pool {
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
    void replace(Handle h, T data) {          // hot reload: same handle, new data
        if (T* p = get(h)) *p = data;
    }
    void destroy(Handle h) {
        if (get(h)) { slots[h.index].alive = false; ++slots[h.index].generation; free_list.push_back(h.index); }
    }
};

int main() {
    Pool<int> textures;                 // int stands in for a GPU texture id
    Handle rock = textures.create(17);
    textures.replace(rock, 18);         // artist saved a new rock texture
    std::printf("rock=%d\n", *textures.get(rock));
    textures.destroy(rock);
    Handle moss = textures.create(42);  // reuses slot 0 with generation 1
    std::printf("moss=%d stale rock is %s\n", *textures.get(moss),
                textures.get(rock) ? "alive" : "null");
}
```

Compiled with `clang++ -std=c++17`, it prints `rock=18` and then `moss=42 stale rock is null`. Trace the second line. The moss texture reuses slot 0, but with generation 1. The stale rock handle still says generation 0, so `get` returns `nullptr` instead of the moss. The bug that used to draw the wrong texture now produces a clear "stale handle" that you can assert on in a debug build.

Handles buy you three things. Stale access is detected instead of silently wrong. The data can move in memory (week 3's allocators can compact a pool) because nobody holds its address. And, the reason they matter this week, the data behind a handle can be **replaced** while every holder keeps the same handle. Entity ids in an ECS often use the same index-plus-generation trick (week 5), and [week 10](w10-scripting-layer-integration.md) hands the same kind of handle to scripts, where stale references are even more common. The cost is one extra indirection per access, and a 32-bit generation that wraps after about four billion reuses of one slot, which in practice never happens within a play session.

## 5. Hot reload at engine scale

CS102 week 13 gave you hot reload for one data table: notice the file changed, validate the new version, swap it in only if it is valid, and pass ids around so that holders see the new data. An engine applies the same rules to every asset type. Three things get harder.

### Swap behind the handle

With handles, reloading is `replace(handle, new_data)`. Every goblin that holds the texture handle draws the new texture next frame, and none of them had to be told. Without handles you would need to find and patch every pointer to the old texture, which in practice means you can't hot reload at all.

Godot's loader shows the same idea in its API. `ResourceLoader.load` takes a cache mode. The default, `CACHE_MODE_REUSE`, returns the cached copy. `CACHE_MODE_REPLACE` reloads from storage and, if the cached object has the same type, refreshes its data inside the existing instance, so every node that already holds it sees the change.

### Rebuild dependents, in order

Resources depend on each other. A material uses a shader and some textures. A model uses materials. When the shader file changes, the materials built from it are stale, and the models built from those materials may be too. The resource manager keeps the "uses" edges from the cooker, inverts them into "used by" edges, and walks outward from the changed file.

```python
from collections import deque

uses = {
    "mat/rock":    ["shader/lit", "tex/rock"],
    "mat/moss":    ["shader/lit", "tex/moss"],
    "mat/ui":      ["shader/unlit", "tex/ui_atlas"],
    "model/cliff": ["mat/rock", "mat/moss"],
}

def rebuild_order(changed, uses):
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

print(rebuild_order("shader/lit", uses))   # ['mat/moss', 'mat/rock', 'model/cliff']
print(rebuild_order("tex/ui_atlas", uses)) # ['mat/ui']
```

This is a breadth-first search (CS102 week 8's graphs) on the reversed edges. It rebuilds the two materials before the cliff that uses them. Breadth-first order is safe for this graph. On a graph where one asset can be reached by paths of different lengths, you need a full topological order, which the lab asks you to handle.

### Never swap mid-frame

A texture that the GPU is reading this frame cannot be overwritten this frame. The renderer may have several frames in flight (week 4). So hot reload runs in two steps. The file watcher and loader work on a background thread and produce the new data. The swap itself happens at a fixed point in the frame, typically at the start before any system reads resources, and the old GPU copy is freed only after the frames that used it have finished. The same fixed point is where the loader's validation failure gets reported: keep the old resource, print what is wrong, and carry on.

### What does not hot reload well

Data that keeps its shape reloads cleanly: new pixels, new numbers, new vertices. Data that changes shape does not. If a designer adds a field to a component's data layout, every instance created from the old layout is now the wrong size, and no handle swap fixes that. Code is harder still. Engines that reload C++ code, and scripting layers that reload scripts (week 10), need rules about what state survives. Your minimum rule for this course: shape changes need a restart, and the engine must say so clearly instead of crashing.

## In-class activity (25 minutes)

In groups of three, design the disk layout and residency plan for a small open-world MMO zone.

The zone has 6 subzones. Each needs 90 MB of unique assets. There is also a shared set of 400 creature and prop assets totalling 120 MB, and each subzone uses about half of them (a different half each time, with overlap). Target platform: a laptop hard drive with `t_a = 15 ms` and `R = 100 MB/s`.

1. Compute the load time for entering a subzone if the shared assets are stored once as loose files, and if each subzone gets its own packed copy of the half it uses. (15 min)
2. Compute the disk cost of each layout. Propose a middle layout (for example, a few shared bundles grouped by creature family) and estimate its reads and disk cost. (5 min)
3. Decide the memory policy. When the player crosses from subzone 2 to 3, which assets may be freed, and would you free them at count zero or keep them in an LRU budget? Write one sentence of justification. (5 min)

Expected output: a three-row table (layout, reads, load time, disk) and a one-sentence memory policy.

## Common misconceptions

- **"Load time is file size divided by drive speed."** That is only the second term. On a hard drive, a few hundred small reads can cost more than the bytes themselves. Always count reads.
- **"SSDs make file layout irrelevant."** They shrink `t_a` by about two orders of magnitude, but reads smaller than the SSD's knee still waste most of its bandwidth, and per-file open costs remain. Packing still pays. Duplication mostly stops paying.
- **"Reference count zero means free it now."** It means you may free it. Whether you should depends on memory pressure and on whether it is likely to be needed again soon.
- **"A handle is a pointer with extra steps."** A handle survives the data moving, being replaced or being freed, and a stale one is detectable. A pointer survives none of these.

## Check yourself

1. A studio ships on a console whose drive has `t_a = 0.2 ms` and `R = 2,400 MB/s`. What is the knee? An artist's texture streaming system reads 64 KB tiles. What fraction of peak bandwidth does it get, and what would you change?
2. Two assets A and B are each 3 MB and always load together. On the laptop hard drive, how much time do you save per load by storing them contiguously as one read instead of two?
3. A level has 800 instances using 40 distinct textures. With the reference-counted cache, how many disk loads happen when the level loads? After 790 of the instances are destroyed, what is the smallest number of textures that could still be resident, and the largest?
4. The artist saves a new rock texture while 300 rocks are on screen. Count the pointer updates the engine must make if each rock stores a `Texture*`, and if each rock stores a `Handle`. What must the engine do in the pointer case that it can skip with handles?
5. In section 5's graph, add `"model/ruin": ["mat/moss", "mat/ui"]`. List the rebuild order when `tex/moss` changes.

<details>
<summary>Answers</summary>

1. `b* = 0.0002 × 2400 = 0.48 MB`. `R_eff / R = 0.064 / (0.064 + 0.48) = 11.8%`. Read several tiles per request (for example, 8 neighboring tiles, 0.5 MB, about 51% of peak), or issue many reads in parallel so the access waits overlap.
2. One access time, 15 ms. Transfer is the same 6 MB either way.
3. 40 disk loads, one per distinct texture. At least 1 (all 10 survivors might use the same texture) and at most 10 (each survivor uses a different one), assuming textures are freed at count zero.
4. With pointers, up to 300: every rock that points at the old texture must be found and patched, so the engine needs a list of every pointer to every resource (or it cannot reload in place). With handles, zero: `replace` writes the new data into the slot, and all 300 handles resolve to it next frame.
5. `['mat/moss', 'model/cliff', 'model/ruin']`. `mat/ui` does not use `tex/moss`, so it is not rebuilt, even though `model/ruin` also uses it.

</details>

## Lab / assignment hook

[Lab 07, a resource manager with handles and hot reload](../labs/lab07.md). You implement the reference-counted cache, a generational handle pool, dependency-ordered reload with validation, and a small load-time calculator that picks between two pack layouts. The lab's resource manager is the one your final engine uses from week 8 on.

## Sources

- Wikipedia, "PlayStation 5", section "Development" (retrieved September 2026). Summarizes Cerny's March 18, 2020 presentation: hard drive speed limited the amount of data loaded, its physical location on disk, and the duplication of data to reduce load times; 5.5 GB/s raw SSD bandwidth.
- Wikipedia, "Hard disk drive performance characteristics" (retrieved September 2026). Typical seek times of about 9 ms (desktop) and 12 ms (mobile); average rotational latency as half a rotation; sustained transfer rates. Used only to justify the rounded assumptions in section 2.
- Wikipedia, "Doom WAD" (retrieved September 2026). WAD as the package for Doom's (1993) levels, textures and sounds; the name; IWAD and PWAD.
- Epic Games, Unreal Engine 5.8 documentation, "Cooking Content and Creating Chunks". One `.pak` file per chunk, distributed separately.
- Godot Engine documentation (4.x, master branch, retrieved September 2026), "Exporting packs, patches, and mods" (`.pck` resource packs), "Resources" (loaded once, `RefCounted`), and the `ResourceLoader` class reference (`CACHE_MODE_REUSE`, `CACHE_MODE_REPLACE`).
- Unity Technologies, Addressables package manual 1.21, "Memory management" and "Reference counting". Load and release counts; bundles unload only as a whole; `Resources.UnloadUnusedAssets` is slow.
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 7.

## Interactive spec: examples/w07-seeks-vs-bytes.html

**Purpose.** Make visible that load time has a per-read part and a per-byte part, and that duplication only pays when the per-read part is large.

**Layout.** Two linked panels side by side on desktop, stacked on mobile.

- **Left panel, "Effective rate".** Line chart of `R_eff(b) = R × b / (b + t_a × R)` for `b` from 0.016 MB to 64 MB on a log-2 x axis (labels 16 KB, 64 KB, 256 KB, 1 MB, 4 MB, 16 MB, 64 MB). Y axis 0 to `R`, labelled in MB/s. A dashed horizontal line at `R` ("rated speed"). A vertical marker at the knee `b* = t_a × R` with the label "knee: b* = … MB, 50% of rated". A draggable dot on the curve for the current read size, showing `b`, `R_eff` and `R_eff/R` as a percentage.
- **Right panel, "Entering a district".** Two horizontal bars.
  - Load-time bar split into two segments, "waiting" = `S × t_a` and "transferring" = `B / R`, with seconds printed on each segment and the total at the end. Scale fixed per drive so the bar visibly shrinks (HDD scale 0 to 8 s, SSD scale 0 to 0.1 s; show the scale label).
  - Disk bar: disk used in MB, scale 0 to 4,500 MB, with the "store once" value (2,860 MB) marked as a tick.
  - Under the bars, a readout row: `S`, `B`, `T`, disk MB, and "saved vs store-once: … s for … MB extra".

**Controls.**
- Drive preset segmented control: "Laptop HDD" (`t_a = 15 ms`, `R = 100 MB/s`), "Desktop HDD" (`t_a = 13 ms`, `R = 150 MB/s`), "NVMe SSD" (`t_a = 0.1 ms`, `R = 5500 MB/s`), "Custom".
- Custom sliders (enabled when Custom is chosen, but always showing current values): `t_a` 0.05 to 30 ms (log), `R` 20 to 7,000 MB/s (log).
- Read-size slider for the left panel, 16 KB to 64 MB (log), linked to the draggable dot.
- Duplication slider `f` from 0 to 1 in steps of 0.01 for the right panel.
- Fixed scenario constants shown as text: 20 districts, 140 MB unique, 60 MB shared in 300 files.

**Formulas (right panel).** `S = 1 + round(300 × (1 − f))`, `B = 200`, `T = S × t_a / 1000 + B / R`, `disk = 140 × 20 + 60 × (1 − f) + 60 × f × 20`.

**Test values (must match to the shown precision).**
- Laptop HDD, `b = 64 KB` (0.064 MB): `R_eff = 4.1 MB/s` (4%). `b = 1.5 MB`: 50.0 MB/s (50%). `b = 16 MB`: 91.4 MB/s.
- NVMe SSD, `b = 64 KB`: 573.3 MB/s. Knee 0.55 MB.
- Laptop HDD, `f = 0`: `S = 301`, `T = 6.515 s` (waiting 4.515, transferring 2.000), disk 2,860 MB. `f = 0.5`: `S = 151`, `T = 4.265 s`, disk 3,430 MB. `f = 1`: `S = 1`, `T = 2.015 s`, disk 4,000 MB.
- NVMe SSD, `f = 0`: `T = 0.066 s` (waiting 0.030, transferring 0.036). `f = 1`: `T = 0.036 s`.

**The one insight.** On first load (Laptop HDD, `f = 0`) the waiting segment is visibly bigger than the transferring segment. Moving `f` to 1 makes it vanish while the disk bar grows by 40%. Switching to NVMe SSD shows both segments tiny and the same duplication buying almost nothing.

**Accessibility.** All sliders are native range inputs with labels and live numeric readouts (`aria-live="polite"` on the readout row). Segment colors come from the shared tokens and each segment also carries its text label, so color is never the only cue. Respect `prefers-reduced-motion` by not animating bar transitions.
