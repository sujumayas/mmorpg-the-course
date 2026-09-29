# CS201 · Week 05 — Entity-Component-System Design

**Why this matters:** In CS102 you built an ECS in Python with a dict of sets and learned what entities, components, systems and queries are. That design answers "who has a Burning component?" quickly, but it stores every component as a separate object somewhere on the heap. An engine has to decide where the bytes live. That one decision sets how fast systems iterate, how expensive it is to add a status effect, and whether an old handle to a dead goblin crashes the game or quietly points at a new one.

**You will be able to:**
- Implement generational entity handles and explain how they detect stale references.
- Implement a sparse-set component pool with O(1) add, remove and lookup, and trace its arrays by hand through a sequence of operations.
- Compare sparse-set and archetype storage with a cost model, and compute the break-even rate of component changes at which one beats the other.
- Choose a storage strategy (archetype, sparse set, or an enable flag) for a given component from how often it changes and how it is queried.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 16, sections 16.1, 16.2 and 16.5 (runtime object models and object references). Unity Entities documentation (package 1.3), "Archetypes concepts" and "Structural changes concepts", one page each. EnTT wiki, "Crash Course: entity-component-system", the sections on the design and on pools (about 20 minutes).

**Prerequisites from earlier courses:** [CS102 week 9, the component pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w09-pattern-component.md). It defines entity, component, system, world and query, and its worked example (polling versus a per-type index) is assumed here. [CS102 week 2, inheritance vs composition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w02-inheritance-vs-composition.md) (why components at all). [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (swap-and-pop removal). From this course, [week 2](w02-cpp-for-engines-memory-raii-and-move-semantics.md) on dangling pointers and [week 3](w03-memory-allocators-stack-pool-and-frame.md) on pool allocators with free lists. The entity pool in section 1 is a pool allocator for IDs.

**Interactive:** [`examples/w05-sparse-set-vs-archetype.html`](../examples/w05-sparse-set-vs-archetype.html). Keep it open during section 2.

---

## 1. Entities are numbers, and numbers get reused

In CS102 an entity was a Python object with a name and a dict of components. In an engine, an entity is only an identifier. It owns nothing. The components live in storage owned by the world, and the entity is the key that finds them.

The simplest identifier is an index: entity 7 is the eighth slot in every array. Indices are small, fast to compare and easy to use as array positions. They have one problem. When entity 7 dies, its slot should be reused, or the arrays grow forever in a game that spawns and kills thousands of projectiles a minute. The next thing spawned becomes the new entity 7.

Now picture the AI system that stored "my target is entity 7" before the goblin died. On the next frame it attacks entity 7 again. Entity 7 is now an arrow in flight, or a chest, or another player. No crash, no error, just a bug that shows up only in long play sessions. This is the ID version of the **dangling pointer** from week 2: a reference to something that no longer exists, which now aliases something else.

### Generational handles

The fix is to pair the index with a **generation**, a counter stored per slot that goes up each time the slot is freed.

```
Entity  = (index, generation)
alive(e) ⇔ generation_of_slot[e.index] == e.generation
destroy(e): generation_of_slot[e.index] += 1; push e.index onto the free list
create():   pop an index from the free list (or append a new slot), return (index, its generation)
```

The goblin was `(7, 0)`. When it dies, slot 7's generation becomes 1. The arrow spawned next is `(7, 1)`. The AI's stored handle `(7, 0)` now fails `alive`, and the AI can drop its target on purpose.

This is exactly the pool allocator from week 3, applied to IDs: a free list of slots, with one extra number per slot. Real engines pack both parts into one integer. EnTT's default 32-bit identifier uses 20 bits for the index and 12 for the version, so it supports about a million live entities and detects reuse until a slot has been recycled 4,096 times. Bevy's `Entity` is an index and a generation packed into 64 bits, and its documentation warns that a despawned ID can alias a later entity if you keep holding it.

Two things a generation does not do. It does not stop you from holding stale handles; it only lets you check them. And after enough recycles the counter wraps, so a handle held for a very long time can pass the check again. With 12 bits that means 4,096 deaths in the same slot while one system holds the old handle. Rare, but it is why long-lived references (saved games, network messages) use separate persistent IDs, which week 12 covers.

## 2. Worked example: where does Stunned live?

### The hook

CS102 week 9 told you to model status effects as components. A goblin catches fire, you add `Burning`. It stops burning, you remove it. The index made "who is burning?" cheap.

Now read Unity's Entities documentation (package 1.3). Adding or removing a component is a **structural change**. The entity moves to a different archetype, and the documentation says that moving entities often is resource-intensive and hurts performance. Unity offers a separate feature, enableable components, for states that change often and unpredictably. Bevy (0.19) lets you mark a single component type as `SparseSet` instead of the default `Table`, and documents the trade in one line each: tables give fast, cache-friendly iteration and slow add and remove, and sparse sets give the opposite. EnTT, the library its README says Mojang uses in Minecraft, stores every component in a sparse set by default.

So three respected ECS libraries disagree about the most basic operation in CS102's design. They are not confused. They made different bets about which is more common in a frame: iterating components or changing which components an entity has. This worked example makes that bet measurable.

### The model

Two storage layouts. Both keep components of one type packed in arrays, so both iterate far faster than CS102's per-object dicts. They differ in what "packed together" means.

**Sparse set (one pool per component type).** Each component type `C` has three arrays.

```
sparse[entity index] → slot in dense, or NONE
dense[slot]          → entity index
data[slot]           → the component value
```

- `has(e)`: `sparse[e] != NONE`. One read.
- `get(e)`: `data[sparse[e]]`. Two reads.
- `add(e, v)`: append `e` to `dense` and `v` to `data`, set `sparse[e]`. O(1).
- `remove(e)`: **swap-and-pop**. Move the last element into `e`'s slot, fix that element's `sparse` entry, shrink by one. O(1). The pool stays packed with no holes, and its order changes.

Removing `Stunned` touches only the `Stunned` pool. The entity's Position, Velocity and everything else stay where they are.

**Archetype (one table per distinct component set).** An **archetype** is the exact set of component types an entity has, for example `{Position, Velocity, Health, Sprite, AI}`. Every entity with that exact set lives in the same table. The table has one column (an array) per component type, and row `i` of every column belongs to the same entity. Unity splits each table into 16 KiB **chunks**. Each chunk holds one array per component type plus an array of entity IDs.

- Iterating `(Position, Velocity)`: for every table whose set contains both, walk the two columns side by side. No lookups at all.
- Adding `Stunned` to one entity: its set changes to `{…, Stunned}`, a different archetype. Copy its whole row (every component) to the end of that table, then fill the hole in the old table by moving that table's last row into it (swap-and-pop again), and update both entities' locations.

The costs, per operation, for an entity whose components total `S` bytes, toggling a component of `s` bytes (a tag like `Stunned` with no data has `s = 0`):

```
                         sparse set                         archetype
toggle a component       ≈ s + a few index writes           ≈ 2S + s (copy row in, move last row into hole)
iterate k components     smallest pool, then (k − 1)        k columns side by side, no lookups
over n entities          sparse lookups per entity
```

The whole trade in one sentence. **Archetypes pay when an entity's component set changes; sparse sets pay every time a system joins two or more components.**

### Numbers you can check

**Trace first.** Five goblins, indices 0 to 4. Stunned is added to goblins 1, 3 and 4, then removed from goblin 1. This is the output of the program below, and you should be able to produce every line by hand from the rules above. A dash is `NONE`.

| Step | `dense` | `sparse` (index 0 to 4) |
|---|---|---|
| add Stunned to 1 | `[1]` | `[- 0]` |
| add Stunned to 3 | `[1 3]` | `[- 0 - 1]` |
| add Stunned to 4 | `[1 3 4]` | `[- 0 - 1 2]` |
| remove Stunned from 1 | `[4 3]` | `[- - - 1 0]` |

Check the last row. Goblin 1 was in slot 0. The last element, goblin 4 in slot 2, moves into slot 0, so `dense[0] = 4` and `sparse[4] = 0`. Then the pool shrinks and `sparse[1] = NONE`. Goblin 3 never moved. The `sparse` array is only as long as the highest index added so far; it grows on demand.

Then goblin 3 dies and a new entity is created. It reuses index 3 with generation 1, and the old handle `(3, 0)` reports dead.

```cpp
// sparse_ecs.cpp: generational entity handles and one sparse set per component type.
// Build: c++ -std=c++20 -O2 sparse_ecs.cpp -o sparse_ecs && ./sparse_ecs
#include <cstdint>
#include <cstdio>
#include <vector>

constexpr std::uint32_t NONE = UINT32_MAX;

struct Entity { std::uint32_t index, generation; };

class EntityPool {                                 // hands out and recycles indices
    std::vector<std::uint32_t> gen_;               // current generation of each index
    std::vector<std::uint32_t> free_;              // destroyed indices ready for reuse
public:
    Entity create() {
        if (!free_.empty()) { std::uint32_t i = free_.back(); free_.pop_back(); return {i, gen_[i]}; }
        gen_.push_back(0);
        return {std::uint32_t(gen_.size() - 1), 0};
    }
    void destroy(Entity e) { ++gen_[e.index]; free_.push_back(e.index); }
    bool alive(Entity e) const { return e.index < gen_.size() && gen_[e.index] == e.generation; }
};

template <class T>
class SparseSet {                                  // all components of one type, packed
public:
    std::vector<std::uint32_t> sparse;             // entity index -> slot in dense, or NONE
    std::vector<std::uint32_t> dense;              // slot -> entity index
    std::vector<T> data;                           // slot -> component value

    bool has(std::uint32_t e) const { return e < sparse.size() && sparse[e] != NONE; }
    T& get(std::uint32_t e) { return data[sparse[e]]; }
    void add(std::uint32_t e, T value) {
        if (e >= sparse.size()) sparse.resize(e + 1, NONE);
        sparse[e] = std::uint32_t(dense.size());
        dense.push_back(e);
        data.push_back(value);
    }
    void remove(std::uint32_t e) {                 // swap-and-pop: the last element fills the hole
        std::uint32_t slot = sparse[e], last = dense.back();
        dense[slot] = last;
        data[slot] = data.back();
        sparse[last] = slot;
        dense.pop_back();
        data.pop_back();
        sparse[e] = NONE;
    }
};

struct Stunned { float seconds; };

template <class T>
void show(const char* step, const SparseSet<T>& s) {
    std::printf("%-22s dense [", step);
    for (auto e : s.dense) std::printf(" %u", e);
    std::printf(" ]  sparse [");
    for (auto x : s.sparse) x == NONE ? std::printf(" -") : std::printf(" %u", x);
    std::printf(" ]\n");
}

int main() {
    EntityPool pool;
    std::vector<Entity> goblin;
    for (int i = 0; i < 5; ++i) goblin.push_back(pool.create());

    SparseSet<Stunned> stunned;
    stunned.add(goblin[1].index, {2.0f}); show("add Stunned to 1", stunned);
    stunned.add(goblin[3].index, {1.5f}); show("add Stunned to 3", stunned);
    stunned.add(goblin[4].index, {0.5f}); show("add Stunned to 4", stunned);
    stunned.remove(goblin[1].index);      show("remove Stunned from 1", stunned);
    std::printf("goblin 4 is in slot %u with %.1f s left\n",
                stunned.sparse[4], stunned.get(4).seconds);

    Entity old = goblin[3];
    stunned.remove(old.index);            // destroying an entity removes its components
    pool.destroy(old);
    Entity fresh = pool.create();         // reuses index 3 with a new generation
    std::printf("old {%u,%u} alive: %d   fresh {%u,%u} alive: %d\n", old.index, old.generation,
                pool.alive(old), fresh.index, fresh.generation, pool.alive(fresh));
}
```

Output:

```
add Stunned to 1       dense [ 1 ]  sparse [ - 0 ]
add Stunned to 3       dense [ 1 3 ]  sparse [ - 0 - 1 ]
add Stunned to 4       dense [ 1 3 4 ]  sparse [ - 0 - 1 2 ]
remove Stunned from 1  dense [ 4 3 ]  sparse [ - - - 1 0 ]
goblin 4 is in slot 0 with 0.5 s left
old {3,0} alive: 0   fresh {3,1} alive: 1
```

This minimal pool assumes you never add a component twice or remove one that is missing. Lab 05 adds those checks.

**Cost in bytes.** A unit in our game has Position (12 bytes), Velocity (12), Health (8), Sprite (16) and AI state (64), so `S = 112` bytes. Stunned is a tag, `s = 0`. A raid boss stuns and releases 1,000 units per frame.

| Per frame | Sparse set | Archetype |
|---|---|---|
| Bytes moved by 1,000 toggles | about 8 per toggle (one `dense` entry, one `sparse` entry), 8 KB | `2 × 112 = 224` per toggle, 224 KB |
| Movement system over 100,000 units | walk Velocity, one `sparse` lookup and one scattered Position read per unit | walk two columns in step, 0 lookups |

**Measured.** The file `bench_storage.cpp` in [lab 05's starter](../labs/lab05-starter/) builds both layouts for 100,000 units and runs both operations. Velocity was added to the sparse-set world in a shuffled order, as happens when components are added at different times during play. Toggle costs are the mean over 200 frames and movement is the best of 200 frames, `c++ -std=c++20 -O2`, Apple M4 Pro, September 2026. The numbers varied by up to 20% between runs, so the table gives the range over five runs.

| Operation | Sparse set | Archetype | Winner |
|---|---|---|---|
| Toggle Stunned, per toggle | 6.4 to 8.8 ns | 34 to 49 ns | sparse set, about 5× |
| Movement over 100,000 units | 0.133 to 0.157 ms | 0.022 to 0.026 ms | archetype, about 6× |
| Movement, pools in the same order | 0.068 ms | 0.022 ms | archetype, about 3× |

Now the break-even, using typical values of 40 ns and 7 ns per toggle and 0.022 and 0.133 ms for movement. Per frame, the archetype layout saves `0.133 − 0.022 = 0.111` ms on movement and loses about `40 − 7 = 33` ns per toggle. It stays ahead while

```
toggles per frame × 33 ns < 0.111 ms   ⇒   toggles < 0.111 ms / 33 ns ≈ 3,400
```

At 1,000 toggles per frame the archetype layout costs 0.062 ms in total (0.022 + 1,000 × 40 ns) and the sparse set 0.140 ms. At 10,000 toggles, the archetype costs about 0.42 ms and the sparse set about 0.20 ms. And the movement system is one of maybe a dozen systems, each of which does its own join, so a real game shifts the break-even further toward archetypes. Your machine's numbers will differ. The method of comparing the two per-frame totals will not.

### The visual

Open [`w05-sparse-set-vs-archetype.html`](../examples/w05-sparse-set-vs-archetype.html). The top view shows the same eight entities stored both ways. On the left, a sparse set per component type, with `sparse` and `dense` arrays drawn as rows of cells. On the right, archetype tables drawn as grids, one column per component. Buttons add or remove Stunned on a selected entity, and each change animates the bytes that move. A counter under each side adds up the bytes moved.

The bottom view is the break-even chart. The x axis is toggles per frame (0 to 20,000), the y axis is milliseconds per frame, and two lines show each layout's total from the measured costs. Drag the "systems that join" slider from 1 to 12 and watch the crossing point slide right. Then add and remove Stunned on a few different entities in the top view. The sparse-set counter moves 8 bytes per press. The archetype counter climbs by 224, one 112-byte row copied out and the table's last row moved into the hole. Toggle the same entity twice in a row and the second press costs 112, because that entity is now the last row of its table and leaves no hole to fill. **Change is cheap in one layout and iteration is cheap in the other, and the chart tells you which your game does more of.**

### Cross-game recognition

- **Unity Entities 1.3.** Archetypes with 16 KiB chunks, one array per component type inside each chunk. Adding or removing components, creating or destroying entities, and setting shared component values are structural changes. They create sync points, where the main thread waits for running jobs to finish. That wait is not in our byte model, so in Unity a structural change costs more than the table shows. For states that flip often, Unity recommends **enableable components**: the component stays on the entity, and a per-entity enabled bit decides whether queries see it. That is a third answer to our question: keep the storage fixed and filter with a flag.
- **Bevy 0.19.** Archetype-style tables are the default storage. Individual component types can opt into sparse-set storage with a single attribute. The documented reason matches our model: sparse sets for components added and removed often, tables for everything iterated in bulk. Bevy's `Entity` is an index plus a generation, the same handle as section 1.
- **EnTT (v4, 2026).** Every component type gets its own pool, a sparse set with swap-and-pop removal. For hot joins it offers **groups**, which take ownership of several pools and reorder them so matching entities sit at the same positions in each. That removes the per-entity lookup, the last row of our measured table taken all the way. Its entity identifiers carry a version that goes up when an ID is released, the generation from section 1.
- **Overwatch (Blizzard, GDC 2017).** CS102 week 9 cited Timothy Ford's talk on the game's ECS. The same vocabulary organizes a shipped competitive shooter's gameplay code. Which storage a game picks is a detail below the vocabulary, and it is the detail this lecture is about.

Three libraries, three defaults, one trade: **move the entity when its shape changes, or look it up every time you join.**

### Eyes-open design judgment

- **Default to archetypes for components that describe what a thing is.** Position, Mesh, Health and AI rarely come and go, and they are iterated every frame by several systems.
- **Use a sparse set, or an enable flag, for what a thing is doing right now.** Stunned, Burning, Selected and "was hit this frame" flip often. In an archetype world each flip also creates a new combination of components: 5 independent tags make up to 32 archetypes from one base type, and each archetype's chunks are only partly full.
- **Iteration order is not stable.** Swap-and-pop reorders pools and tables. If a system depends on processing entities in spawn order (for deterministic replay, CS102 week 9 warned about this), sort explicitly or store an order key.
- **Handles, not pointers.** Pointers into a pool or table become invalid when the storage grows or rows move. Hand out `(index, generation)` handles and look the component up when you need it.
- **Defer structural changes.** Adding and removing components while a system iterates the same storage moves rows under the iterator. Queue changes in a command buffer and apply them at a fixed point in the frame, the same end-of-frame bracket as week 4 and CS102's deferred destruction.
- **Measure your game, not ours.** Our break-even of about 3,400 toggles per frame came from one system, one machine and one component size. Change `S` from 112 to 400 bytes and each archetype move copies 800 bytes instead of 224, about 3.6 times as many.

### Check yourself (worked example)

1. Starting from the final row of the trace table (`dense [4 3]`), add Stunned to goblin 0, then remove it from goblin 4. Write `dense` and `sparse` after each step.
2. A unit's components total 300 bytes. How many bytes does one archetype toggle of a tag move, by the model? How many for 2,000 toggles per frame?
3. Using the measured costs, suppose a game has four join systems like the movement system, each saving 0.111 ms under archetypes. What is the new break-even in toggles per frame?

<details>
<summary>Answers</summary>

1. Add 0: `dense [4 3 0]`, `sparse [2 - - 1 0]`. Remove 4 (slot 0): the last element, 0, moves into slot 0. `dense [0 3]`, `sparse [0 - - 1 -]`.
2. `2 × 300 = 600` bytes per toggle. `2,000 × 600 = 1,200,000` bytes, about 1.2 MB per frame.
3. Savings `4 × 0.111 = 0.444` ms. Break-even `0.444 ms / 33 ns ≈ 13,500` toggles per frame.

</details>

## 3. Systems, queries and the schedule

With storage fixed, a system becomes a loop over a **view**: the set of entities that have all the requested components.

In a sparse-set world, a view picks the smallest pool among its component types and walks its `dense` array. For each entity it checks `has` in the other pools and skips the ones that fail. This is CS102's index query with arrays instead of dicts, and it keeps CS102's key property: the cost follows the size of the smallest pool, not the number of entities in the world.

In an archetype world, a query first finds the matching archetypes, every table whose component set contains all requested types. Engines cache this list per query and update it only when a new archetype appears, which is rare after the first seconds of play. Then the system walks each matching table's columns.

Either way, the frame becomes a list of systems in a fixed order. That list is the "update" stage from week 4, and its order is a design decision you already met in CS102.

```
input_system        reads devices, writes Intent components
ai_system           reads Position, Target; writes Intent
movement_system     reads Intent, Velocity; writes Position
combat_system       reads Position, Weapon; queues Damage events
damage_system       applies Damage to Health; queues destroy commands
status_system       ticks Stunned and Burning timers; queues remove commands
apply_commands      applies every queued add, remove and destroy (structural changes)
render_extract      copies Position and Sprite into the render snapshot (week 4, section 5)
```

Two rules make this list safe.

**Read and write sets.** Write down which component types each system reads and writes. Two systems that write the same type must run in a defined order. Two systems whose sets do not overlap could run on different threads at the same time. Unity and Bevy both schedule systems in parallel from exactly this information. You will not build a parallel scheduler in this course, but writing the sets down now is what makes one possible later.

**One place for structural changes.** Every add, remove, create and destroy during the update goes into a command buffer. `apply_commands` runs them all at once. No system ever iterates storage that is changing under it, and every system in a frame sees the same set of entities. In an archetype world this is also where rows move, so the cost of every structural change is paid at one known point that shows up clearly in the profiler.

## 4. Components as plain data

The storage above only works if components can be copied as bytes. An archetype move copies a row, and swap-and-pop copies the last element into a hole. If a component holds a pointer into another component, or owns heap memory through a raw pointer, the copy either breaks the pointer or leaks the memory. Week 2's rule of zero applies: a component should need no custom copy constructor, move constructor or destructor.

Practical rules for component types:

- **Plain data, small and fixed size.** Numbers, small fixed arrays, enums, and entity handles. A `Health` is two floats. A `Sprite` is a texture handle and a rectangle.
- **References to other entities are handles.** A `Target` component holds an `Entity`, never a pointer. The system checks `alive` before using it.
- **Variable-size data lives elsewhere.** An inventory list or a dialogue string goes in a separate store, and the component holds a handle to it. Unity's dynamic buffers and EnTT's ability to store any type both exist for these cases, and both cost more than plain components.
- **No behaviour beyond guarding its own data.** Same rule as CS102. Logic lives in systems.

Week 6 takes this one step further and asks how the bytes inside each column are laid out, and why a column of 12-byte Positions beats an array of 128-byte "unit" structs by an order of magnitude.

## In-class activity (25 minutes)

Groups of three, paper and the interactive.

1. **Trace (8 min).** Each group gets a card with ten operations on three component pools, for example `add Pos 0, add Pos 2, add Vel 2, add Pos 5, add Vel 0, remove Pos 2, add Stun 5, remove Pos 0, add Pos 7, remove Vel 2`. Write every pool's `dense` and `sparse` arrays after each operation. Check the final state against the interactive's custom mode.
2. **Classify (10 min).** For a small MMO, list eight components (at least three that change often). For each, choose archetype column, sparse set, or enable flag, and write the reason in one line using the words "changes per second" and "systems that join it".
3. **Schedule (7 min).** Write a system list for one frame of your game with read and write sets. Circle two systems that could run in parallel and one pair that must stay ordered, and say why.

Expected output: the final pool arrays, the eight-row classification table, and the annotated system list.

## Common misconceptions

- **"ECS means archetypes."** Archetypes are one storage strategy. Sparse sets are another, and many engines mix both. ECS is the vocabulary from CS102. Storage is this week's decision.
- **"Removing from the middle of a pool is O(n)."** With swap-and-pop it is O(1), at the price of changing the order.
- **"A generation counter makes stale handles impossible."** It makes them detectable. You still have to call `alive`, and the counter eventually wraps.
- **"Tags are free because they store no data."** In an archetype world each tag doubles the number of possible archetypes, and toggling one moves the whole entity.
- **"Sparse sets are always slower to iterate."** For a system that reads one component type they walk a packed array, as fast as a table column. The cost appears in joins, and aligned pools (EnTT groups) remove most of it.

## Check yourself

1. An entity pool has created indices 0 to 5. Entities `(2, 0)` and `(4, 0)` are destroyed in that order, and two new entities are created. What handles do they get with the LIFO free list from the code, and which of `(2, 0)`, `(4, 0)`, `(4, 1)` pass `alive`?
2. Your game has 20,000 projectiles with Position, Velocity and Lifetime, and they are created and destroyed at 3,000 per second at 60 fps. Using the section 2 cost table, estimate the structural-change cost per frame in an archetype world if spawns and deaths are the only structural changes and each costs about 40 ns. Is it worth worrying about?
3. A designer wants a "Marked" status that 5 units have at a time and that one system reads every frame. Recommend a storage for it, and say what changes if 5,000 units can be Marked and it toggles every frame.
4. Why must `render_extract` run after `apply_commands` in the section 3 schedule? Describe the bug if it ran before.

<details>
<summary>Answers</summary>

1. Destroy pushes 2, then 4, so the free list is `[2, 4]`. Create pops 4 first: `(4, 1)`, then `(2, 1)`. `(2, 0)` fails, `(4, 0)` fails, `(4, 1)` passes.
2. 3,000 per second is 50 creations and 50 destructions per frame, 100 changes × 40 ns = 4 µs per frame. Negligible. Projectiles are a good fit for archetypes.
3. With 5 holders, a sparse set: the system walks a 5-element pool and toggles cost almost nothing. With 5,000 toggling every frame, an enable flag on a component every unit already has, or a sparse set; archetype moves would cost about `5,000 × 40 ns = 0.2` ms per frame plus fragmentation.
4. `apply_commands` removes dead entities and adds new ones. If `render_extract` ran first, the snapshot would contain entities destroyed this frame (a corpse drawn for one more frame) and miss entities spawned this frame (a projectile that appears one frame late).

</details>

## Lab / assignment hook

[Lab 05, a sparse-set ECS](../labs/lab05.md). You implement generational handles, a checked sparse-set pool and a two-component view in C++, pass the tests, run `bench_storage.cpp` on your machine to compute your own break-even, and write a one-page storage recommendation for five components of your final engine's demo game.

## Sources

- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 16, "Runtime Gameplay Foundation Systems", sections 16.2 (runtime object model architectures) and 16.5 (object references and world queries, including handles).
- Unity Technologies, Entities package 1.3 manual: "Archetypes concepts" (16 KiB chunks, one array per component type plus entity IDs, moving entities between archetypes is resource-intensive), "Structural changes concepts" (which operations are structural, sync points), and "Enableable components overview" (avoiding structural changes for states that change often). https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/concepts-archetypes.html
- Bevy, `StorageType` and `Entity` API documentation (bevy 0.19.1, August 2026). Table is the default and gives fast iteration with slower add and remove; SparseSet gives the reverse. Entities are an index plus a generation that increments on despawn. https://docs.rs/bevy/latest/bevy/ecs/component/enum.StorageType.html
- Caini, M. (skypjack), EnTT wiki "Crash Course: entity-component-system" and source `src/entt/entity/entity.hpp` and `sparse_set.hpp` (master branch after release v4.0.0, July 2026). Pools as specialized sparse sets, groups that own pools, 32-bit identifiers split 20 bits entity and 12 bits version, swap-and-pop deletion policy. https://github.com/skypjack/entt. The README's "EnTT in Action" section names Minecraft (Mojang) as a user.
- Ford, T. (2017). "'Overwatch' Gameplay Architecture and Netcode." GDC 2017, GDC Vault. Cited here as in CS102 week 9.
- Benchmark numbers: `bench_storage.cpp` from lab 05's starter, Apple clang 17, `-O2`, Apple M4 Pro, September 2026.

## Interactive spec: examples/w05-sparse-set-vs-archetype.html

**Purpose.** Show that toggling a component is cheap in a sparse set and expensive in an archetype table, that iterating a join is the reverse, and where the two per-frame totals cross.

**Layout.** Two stacked views. Top: storage view, split left (sparse sets) and right (archetype tables) on desktop, stacked on mobile. Bottom: break-even chart. Controls between them on mobile, in a sidebar on desktop.

**Top view, left: sparse sets.** Three pools: Position, Velocity, Stunned. Each pool drawn as two rows of cells: `sparse` (indices 0 to 7, cell shows slot or "–") and `dense` (cell shows entity index). Under Position and Velocity, a `data` row with small coloured blocks. Stunned has no data row (tag).

**Top view, right: archetype tables.** One grid per archetype that currently has at least one entity. Header lists the component set, for example `{Pos, Vel, HP, Sprite, AI}` and `{Pos, Vel, HP, Sprite, AI, Stunned}`. One row per entity, one column per component, plus an ID column. Each cell width is proportional to the component size (12, 12, 8, 16, 64 bytes; tag column 4 px wide).

**Initial state.** 8 entities, indices 0 to 7, all with Position and Velocity. The sparse-set Velocity pool starts in order `[3 0 6 1 7 4 2 5]` to show out-of-order pools; Position in order `[0 … 7]`. No entity has Stunned. One archetype table with rows 0 to 7.

**Controls.**
- Entity selector (0 to 7), buttons "Add Stunned" and "Remove Stunned" (disabled when invalid).
- "Destroy entity" and "Create entity" buttons driving a generational entity pool; show a handle list with `(index, generation)` and an "alive?" check against a handle the user pins.
- Component size slider for the "rest of the unit" `S` (32 to 512 bytes, default 112).
- Chart controls: toggle cost archetype (ns, default 40), toggle cost sparse (ns, default 7), join saving per system (ms, default 0.111), systems that join (1 to 12, default 1).
- "Step through" mode: animate each swap-and-pop in 3 beats (highlight hole, move last element, shrink). Instant if `prefers-reduced-motion`.

**Counters.** Under each side: bytes moved by the last operation and in total. Sparse set: add costs 8 bytes (dense entry + sparse entry) + `s`; remove costs 8 bytes + `s` for the moved element (0 if the removed element was last). Archetype: add or remove Stunned costs `S` bytes to copy the row out plus `S` bytes to move the source table's last row into the hole (0 if the entity was the last row).

**Bottom view, chart.** x axis: toggles per frame 0 to 20,000. y axis: ms per frame. Line A (archetype): `move_arch_total = 0.022 × systems + toggles × c_arch`. Line S (sparse): `0.133 × systems + toggles × c_sparse`, where 0.133 − 0.022 = the join saving slider value (keep 0.022 fixed as the archetype base per system). Mark the crossing `x* = systems × saving / (c_arch − c_sparse)` with a vertical line and label.

**The one insight.** Pressing Add/Remove Stunned on entities in the middle of their table: the sparse-set byte counter rises by 8 per press, the archetype counter by `2 × S` (224 at default). Repeat toggles of the same entity cost `S` (112), because it is then the last row. The chart's crossing moves right as "systems that join" rises.

**Test values.**
- Trace preset "Lecture trace" (Stunned pool only, entities 0 to 4): add 1, add 3, add 4, remove 1 must show `dense [4 3]`, `sparse [- - - 1 0]`.
- Break-even with defaults (1 system, 40 ns, 7 ns, 0.111 ms): `x* = 0.111e6 / 33 ≈ 3,364` toggles per frame; label "≈ 3,400".
- 4 systems: `x* ≈ 13,455`, label "≈ 13,500".
- At 1,000 toggles and 1 system: archetype 0.062 ms, sparse 0.140 ms.
- `S = 300`: one archetype toggle moves 600 bytes.

**Accessibility.** All buttons and sliders keyboard reachable with visible focus. Every array cell has an accessible name ("dense slot 0: entity 4"). Live region announces each operation's result ("Removed Stunned from 1. Entity 4 moved to slot 0. Sparse set 8 bytes, archetype 224 bytes."). Colour is not the only cue: moved cells get an outline and a text marker.
