# CS102 · Week 05 — Arrays vs Linked Lists vs Hash Maps

**Why this matters:** Most game code does three things with collections. It walks through all of them, it finds one by a key, and it adds or removes some. Each data structure is fast at some of those jobs and slow at others. Pick by habit and you get a game that runs fine in the test level and drops frames in the city with 10,000 item definitions loaded.

**You will be able to:**
- State the cost of index, search-by-key, append, insert-at-front and remove for a dynamic array, a linked list and a hash map.
- Compute the per-frame cost of a lookup pattern and decide whether it fits a frame budget.
- Replace a linear scan with a dictionary or set, and prove with timings that it scales.
- Choose a structure from a description of how the game accesses its data, and defend the choice.

**Before class:** Nystrom, *Game Programming Patterns* (2014), "Data Locality" chapter, sections "A Data Structure for Every Occasion" up to "Contiguous arrays", and the "Event Queue" chapter section "A ring buffer". Reread [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md).

**Prerequisites from earlier courses:** [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md) (list operations and the note on `insert(0, ...)`). [CS101 week 6, dictionaries and item databases](../../CS101-programming-for-games-i/lectures/w06-dictionaries-item-databases.md), for dictionary syntax. [CS102 week 4, Big-O intuition](w04-big-o-intuition-for-game-developers.md) (growth classes, frame budget, the GTA Online case).

**Interactive:** [w05-list-vs-dict-timing.html](../examples/w05-list-vs-dict-timing.html). Keep it open during section 2.

---

## 1. Three ways to keep a collection

Last week you counted work. This week you'll see that the *shape* of the data decides which work is cheap. There are three shapes to know.

### The dynamic array (Python `list`, C# `List<T>`, GDScript `Array`)

A **dynamic array** keeps its elements side by side in one block of memory. Element `i` lives at a known offset from the start, so reading `items[i]` is one address calculation. That is O(1) for any `i`.

Being side by side has two costs. Inserting at position 0 means shifting every other element one place to the right, so it is O(n). And finding an element *by its value* ("which slot holds item 40213?") means checking elements one by one until you hit it. On average you check half the list for an item that's there, and all of it for one that isn't. That is O(n).

`append` is amortized O(1), for the reason in [week 4 section 4](w04-big-o-intuition-for-game-developers.md). The block grows by a proportion, so copies are rare.

### The linked list

A **linked list** stores each element in its own small object, a **node**, that also holds a reference to the next node. The list itself only remembers the first node, the **head**.

```python
class Node:
    __slots__ = ("value", "next")
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

head = Node("potion", Node("sword", Node("shield")))   # potion -> sword -> shield
```

To insert at the front you make one new node that points to the old head. Nothing shifts, so it is O(1). If you already hold a reference to a node, you can splice a new node in after it, or unlink its neighbor, in O(1) too. That is the linked list's whole advantage.

Its costs are the mirror image. There is no `items[i]`. To reach the 500th element you follow 499 `next` references, so indexing is O(n). Searching by value is O(n), the same as an array. And every node is a separate object somewhere in memory, which matters for speed in ways Big-O doesn't show (section 4).

### The hash map (Python `dict` and `set`, C# `Dictionary<TKey,TValue>` and `HashSet<T>`)

A **hash map** stores key-value pairs in an array of **buckets**. To store or find a key, it runs a **hash function** on the key, which turns it into a large integer, and uses that integer (modulo the number of buckets) to pick a bucket. Finding item 40213 means hashing 40213, jumping to one bucket and checking the one or two entries there. The time does not depend on how many items the map holds. That is O(1) on average.

A **set** is a hash map with keys and no values. Use it when the only question is "have I seen this?"

Microsoft's documentation for `Dictionary<TKey,TValue>` puts it plainly. Retrieving a value by key is "close to O(1)" because the class is a hash table, and the speed depends on the quality of the key type's hash function. Section 3 explains both halves of that sentence.

### The cost table

| Operation | Dynamic array | Linked list | Hash map |
|---|---|---|---|
| Read element `i` | O(1) | O(n) | — (no positions) |
| Find by key or value | O(n) | O(n) | O(1) average |
| Append at end | O(1) amortized | O(1) with a tail reference | O(1) average (insert) |
| Insert or remove at front | O(n) | O(1) | — |
| Remove a given element | O(n) (find, then shift) | O(1) if you hold its node | O(1) average |
| Walk all elements | O(n), fast in practice | O(n), slower in practice | O(n), order is insertion order in Python 3.7+ |
| Memory per element | smallest | one node object each | largest (buckets kept partly empty) |

The table is the lecture in one picture. There is no best structure, only a best structure *for an access pattern*.

## 2. Worked example: 10,000 items, one frame

### The hook

Go back to GTA Online's loader from last week. Its duplicate check kept about 63,000 item entries in an array and, before adding each new entry, scanned the whole array to see if it was already there. That's a "find by key" on a dynamic array, O(n), done `n` times, which makes about 2 billion comparisons. t0st's own patch skipped the check entirely, since every entry in the file was already unique. When you do need the check, the standard fix is to stop scanning. A hash set answers "seen it?" in one bucket check, and the same 63,000 inserts become 63,000 cheap operations.

The same mistake shows up at runtime, where it costs frames instead of loading time. An MMO client has thousands of item definitions. Every frame, the UI resolves item IDs to names, icons and stats for everything on screen. Store the definitions in a list and scan for each ID, and the game works in the starter zone and stutters in the capital city. This worked example measures exactly that.

### The model

A frame performs `q` lookups in a database of `n` items.

```
list:  T_list(n, q) = q × c_scan × (n + 1) / 2        (average, item present)
dict:  T_dict(q)    = q × c_hash                      (no n at all)
```

- `n` is the number of item definitions.
- `q` is lookups per frame.
- `c_scan` is the time to compare one list element against the ID being sought.
- `c_hash` is the time for one dictionary lookup (hash the key, jump to the bucket, compare).
- `(n + 1) / 2` is the average number of comparisons to find an item that is in a list of `n`, when every position is equally likely. A missing item costs `n`.

The frame budget is `B = 16.67 ms` at 60 fps, and the lookups must share it with everything else.

Here is the code, from `labs/lab05-starter/item_db.py`. The list version is written as an explicit loop so you can see the scan.

```python
class ListItemDB:
    def __init__(self):
        self.items = []                     # [(id, name, price), ...]
    def add(self, record):
        self.items.append(record)
    def get(self, item_id):
        for record in self.items:           # O(n) scan
            if record[0] == item_id:
                return record
        return None

class DictItemDB:
    def __init__(self):
        self.by_id = {}                     # {id: (id, name, price)}
    def add(self, record):
        self.by_id[record[0]] = record
    def get(self, item_id):
        return self.by_id.get(item_id)      # O(1) average
```

Both classes have the same interface, `add` and `get`. Code that uses the database can't tell which one it has, apart from the speed. That is the payoff of the interfaces you built in [week 3](w03-interfaces-and-polymorphism.md).

### Numbers you can check

On the course reference machine (CPython 3.13, Apple silicon laptop), the explicit loop costs about `c_scan = 15 ns` per element and the dictionary costs about `c_hash = 30 ns` per lookup, including the method call. Take `q = 250`, which is 50 characters on screen with 5 equipped items each, all resolved once per frame.

| n items | avg comparisons (n+1)/2 | list µs/lookup (model) | list µs/lookup (measured) | list ms/frame (model, q=250) | dict ms/frame (q=250) | list fits 16.67 ms? |
|---|---|---|---|---|---|---|
| 100 | 50.5 | 0.76 | 0.75 | 0.19 | 0.0075 | yes |
| 1,000 | 500.5 | 7.5 | 5.7 | 1.88 | 0.0075 | yes |
| 10,000 | 5,000.5 | 75.0 | 75.5 | **18.75** | 0.0075 | **no** |
| 100,000 | 50,000.5 | 750 | 634 | 187.5 | 0.0075 | no, 11 frames |

Look at the per-lookup column first. At 10,000 items a list lookup takes 75 microseconds. That sounds instant, and in isolation it is. The per-frame column tells the truth. 250 of them take 18.75 ms, more than an entire frame, before the game has moved or drawn anything. **That is the stall.** The dictionary column doesn't change as `n` grows, because a hash lookup never looks at the other items.

Where does the list stop fitting? Set `T_list` equal to one frame, `1000/60 ≈ 16.667 ms`, and solve: `(n + 1) / 2 = 16.667 ms / (250 × 15 ns) = 4,444`, so `n ≈ 8,888`. Past about 8,900 items the lookups alone overrun the frame. In practice they must share the frame, so the real limit is lower.

The dictionary costs 7.5 microseconds per frame at every size. It is 2,500 times cheaper at 10,000 items and 25,000 times cheaper at 100,000.

### A note on constant factors

Python's built-in `x in some_list` runs its loop in C, not in Python bytecode. On the same machine it costs about 4 ns per element instead of 15. That is almost 4× faster, and it changes nothing about the shape. At 10,000 items, `in` averages about 20 µs, and 250 lookups take 5 ms, which is still 30% of the frame and still growing linearly. Week 4's rule applies. A constant-factor speedup moves the wall, and a different structure removes it.

### Seeing it move

Open the interactive. It runs real timings in your browser, using a JavaScript array scan and a JavaScript `Map`, the browser's hash map.

The top view shows **per-lookup time** for both structures as `n` grows, on a log scale. Both lines sit in the microseconds, and the difference looks academic. The bottom view shows **per-frame time** for your chosen `q`, as two bars against a 16.67 ms frame. Slide `n` up to 10,000 with `q = 250` and the list bar runs off the end of the frame while the map bar stays a sliver. Same data, two views, and only one of them shows the problem.

A "model" toggle switches the chart from live browser timings to the formulas above with `c_scan = 15 ns` and `c_hash = 30 ns`, so you can match the table exactly. Your browser's live numbers will be faster than Python's, because JavaScript engines compile hot loops to machine code. The crossing point moves. It doesn't disappear.

### Cross-game recognition

**GTA Online (PC, before the March 2021 fix).** Duplicate rejection by scanning an array is `find by key` on a dynamic array, `n` times. The lab reproduces it. In Python, loading 20,000 unique IDs with a list-based check takes about 750 ms, and with a set about 1 ms. Scale the list version to 63,000 items and the model predicts about 7.4 seconds in Python, from 1.98 billion comparisons at about 3.7 ns each. The structure, not the language, is what turned a fraction of a second into minutes.

**World of Warcraft's addon Lua (Lua 5.1 since patch 2.0.1, 2006, to current).** WoW's UI and addons run in a subset of Lua 5.1. Lua has exactly one data structure, the **table**, and the Lua authors' paper on the Lua 5.0 implementation describes it as a hybrid. A table has an **array part** for dense integer keys 1 to `n` and a **hash part** for everything else, and it resizes the two parts automatically based on what you store. So when an addon author writes `items[itemID] = info`, Lua decides whether that key lives in an array slot or a hash bucket. It's the same trade-off as this lecture, made by the language at runtime. Dense small integers get the array's compactness, and sparse IDs such as item numbers get hashed.

**Nystrom's audio event queue (*Game Programming Patterns*, "Event Queue").** When the game asks to play a sound, the audio system checks whether the same sound is already queued, to avoid playing it twice in one frame. Nystrom's first version walks the whole queue, O(n) per request, and he notes that a hash table keyed on the sound ID makes the duplicate check constant time. It's the GTA duplicate check at a smaller scale, fixed the same way.

**Last week's grid.** `grid_pairs` stored cells in a dictionary keyed by `(cx, cy)` tuples. A list of cells would have needed a scan to find each unit's neighbors. The grid only works because "which units are in cell (57, 12)?" is a hash lookup.

Across all four, when code asks "where is the thing with this key?", a scan answers in O(n) and a hash answers in O(1).

### Eyes-open design judgment

- **Use a dictionary when you look things up by ID more than you walk the collection.** Item databases, player sessions by account ID, quest state by quest ID, buffs by spell ID. This is most of an MMO's data.
- **Use a list when you walk everything every frame and never search.** The list of active projectiles you update each tick. Order matters, indexes are stable, and walking a list is the cheapest traversal there is.
- **Use both when you need both.** A common shape is a list for iteration plus a dictionary from ID to list index, kept in sync. It costs memory and discipline. [Week 9's Component pattern](w09-pattern-component.md) builds on this.
- **Small `n` is not a free pass in every language.** In CPython the dictionary beat the list even at 2 elements (13.8 ns versus 20.3 ns on the reference machine). In compiled languages with value types, a short linear scan over a contiguous array often beats hashing because it touches fewer cache lines. Measure in your engine's language before you "optimize" a 6-element party list into a dictionary.
- **Hashing has conditions.** A key must not change while it's in the map (section 3). Its hash function must spread keys well. Dictionaries use more memory than lists. None of these is a reason to avoid them. Each is a thing to know.

### Check yourself on the worked example

1. With `c_scan = 15 ns` and `n = 10,000`, how many lookups per frame can a list handle before it uses a quarter of the frame (4.17 ms)?
2. A lookup for an item that does *not* exist (a stale ID from an old save) costs how many comparisons in a list of 10,000? What does a dictionary do differently?
3. The designers double the item count from 10,000 to 20,000. What happens to the list's per-frame cost at `q = 250`? To the dictionary's?

<details>
<summary>Answers</summary>

1. One lookup averages `15 ns × 5,000.5 ≈ 75 µs`. `4.17 ms / 75 µs ≈ 55` lookups per frame.
2. All 10,000, because the scan can't stop early. The dictionary hashes the ID, checks one bucket, finds nothing and returns, at the same cost as a hit.
3. The list's cost doubles, from 18.75 ms to 37.5 ms per frame. The dictionary's stays at 0.0075 ms.

</details>

## 3. How a hash map actually works

You can use a dictionary without knowing its insides. You can't debug one without them.

### Buckets and the hash

A **hash function** maps a key to an integer. Python's `hash(40213)` is `40213`, because small integers hash to themselves. `hash("item_40213")` is a large, scrambled number that changes between runs of the program (Python randomizes string hashes for security). The map keeps an array of `m` buckets and stores the key at index `hash(key) mod m`.

A toy version with `m = 8` buckets and integer keys:

| Key | hash(key) | hash mod 8 | Bucket |
|---|---|---|---|
| 40213 | 40213 | 5 | 5 |
| 40216 | 40216 | 0 | 0 |
| 17 | 17 | 1 | 1 |
| 40221 | 40221 | 5 | 5, a **collision** with 40213 |

### Collisions and load factor

Two keys that land in the same bucket are a **collision**. Every hash map has a rule for them. Some keep a short chain of entries per bucket. Python's dict probes other buckets in a fixed pseudo-random order until it finds a free one. Either way, a lookup that collides must compare a few keys instead of one.

Collisions stay rare as long as the table is not too full. The **load factor** is entries divided by buckets. Hash maps keep it below a threshold (CPython resizes a dict when it is about two-thirds full) by allocating a bigger bucket array and re-inserting every key. That resize is O(n), but like list `append` it happens rarely enough to be amortized O(1).

The worst case is real, though. If many keys hash to the same bucket, every lookup walks a long chain or probe sequence and the map decays to O(n). That's why Microsoft's documentation ties `Dictionary` speed to the quality of the key's hash function. In your own key classes, hash all the fields that define equality.

### The rule you can't break

A key's hash must not change while the key is in the map. Microsoft's documentation states this for `Dictionary`, and Python enforces it by refusing unhashable types. Lists can't be dict keys in Python because they can change. Tuples can, which is why the grid used `(cx, cy)`.

Here is the bug this prevents, in C# terms. You key a dictionary by a `Position` object, then move the unit by changing the object's `x`. The object's hash changes, the dictionary still has it filed under the old bucket, and `ContainsKey(unit.pos)` returns `false` for a unit that is right there. Key by something that doesn't move, such as the unit's ID, or re-insert whenever the key changes.

### Worked mini-trace

Insert 40213, 40216, 17 and 40221 into the 8-bucket table above using linear probing (on collision, try the next bucket). 40213 goes to 5, 40216 to 0, 17 to 1. 40221 wants 5, finds it taken, and goes to 6. Now look up 40221. Hash to 5, compare against 40213 (no), step to 6, compare against 40221 (yes). Two comparisons. Look up 40229 (`40229 mod 8 = 5`). Compare at 5 (no), 6 (no), 7 (empty), stop. Not found after two comparisons and one empty check. In a list of the same four items, both lookups would have scanned everything.

## 4. Why linked lists lose more often than Big-O predicts

The cost table says linked lists win at inserting and removing in the middle. Programmers learn that, reach for a linked list, and are then surprised when it's slower.

### Following pointers is slow

Modern CPUs read memory in chunks called **cache lines** (typically 64 bytes) and keep recently used lines in a small, fast **cache**. Walking an array reads memory in order, so each cache line brings in several upcoming elements for free. Walking a linked list jumps to wherever each node happens to live. Nystrom's "Data Locality" chapter explains the consequence. A **cache miss**, where the data isn't in the cache, stalls the CPU for a few hundred cycles while it waits for main memory.

In Python you won't see the full effect, because a Python list stores references to objects rather than the values themselves, so even list traversal chases pointers. On the reference machine, summing 100,000 integers takes 1.3 ms from a list and 1.7 ms from a linked list, only 1.3× apart. In C# or C++, where an array of structs stores values contiguously, the gap is much wider. CS201 week 6 measures it directly (see the [CS201 week 6 lecture](../../CS201-game-engine-architecture/lectures/w06-cache-locality-and-data-oriented-design.md)).

### Finding the spot is the real cost

"O(1) insert in the middle" assumes you already hold a reference to the node where you want to insert. Usually you don't. You have a value or a position, and finding its node is an O(n) walk, the same as the array's shift. Then the array usually wins the tie, because shifting contiguous memory is one fast block copy while walking nodes is many slow jumps.

### Where linked lists earn their place

- **You already hold the node.** Nystrom's grid in "Spatial Partition" gives each unit `prev` and `next` pointers so that moving a unit between cells unlinks and relinks it in O(1), with no search.
- **Front insertion or removal at scale.** Inserting 50,000 items at the front of a Python list took 343 ms on the reference machine. Pushing onto the front of a linked list took 6 ms. If that is your access pattern, next week's `deque` gives you the same O(1) with better memory behavior.
- **Stable references.** A node doesn't move when others are added or removed. An array element can move whenever the array shifts or grows.

For everything else, prefer the array. That's the practical rule most engine programmers follow.

## 5. Choosing by access pattern

Describe how the game touches the data, then read the answer off.

| Access pattern | Structure | Why |
|---|---|---|
| Update every active projectile each frame | list (dynamic array) | walk everything, fast traversal |
| Look up item definition by ID | dict | find by key, O(1) |
| "Has this player already claimed today's reward?" | set | membership only |
| Inventory with 36 fixed slots | list of fixed length | index by slot number |
| Chat messages, oldest removed first | deque (week 6) | O(1) at both ends |
| Units per grid cell, moving between cells often | per-cell lists, or intrusive linked list if you hold the node | cheap moves |
| Leaderboard: top 100 by score | sorted list rebuilt periodically, or a heap | order matters |

Two warnings. First, "remove from the middle of a list" is often avoidable. If order doesn't matter, swap the element with the last one and pop the end, which is O(1). This is the "swap and pop" trick, and it is how many engines remove dead entities. Second, don't convert a structure you walk every frame into a dictionary because lookups are "faster." If you never look anything up by key, you've paid memory for nothing.

## In-class activity (25 minutes)

In groups of three. Each group gets one of these access descriptions from a fictional MMO, written by a designer:

1. "The auction house shows 40 listings per page, sorted by price. Players can search by item name. There are 250,000 active listings."
2. "Every NPC in the zone checks whether it's in combat with the player who just used a spell. Zones hold up to 3,000 NPCs."
3. "The chat window keeps the last 200 lines. New lines appear at the bottom. Old ones scroll off the top."
4. "Players collect cosmetics. The wardrobe screen shows whether each of 4,000 cosmetics is owned."

For your description:
- List the operations and how often each happens (per frame, per click, per day).
- Choose a structure for each and give the Big-O of the most frequent operation.
- Estimate the cost of a poor choice using this week's model and `c_scan = 15 ns`.

Expected output: a three-row table (operation, structure, cost per occurrence) and one sentence naming the structure you would *not* use, with the number that rules it out.

## Common misconceptions

- **"Dictionaries are always faster."** They are faster at finding by key. Walking all entries, keeping order by position, and memory use all favor a list. And a dictionary with a bad hash function decays to O(n).
- **"Linked lists are fast at insertion."** Only once you hold the node. Finding the spot is O(n), and pointer chasing is slow in practice.
- **"75 µs is nothing."** Per lookup, yes. Multiply by lookups per frame before you decide. 250 of them overrun a 60 fps frame.
- **"Python dict iteration order is random."** Since Python 3.7 the language guarantees insertion order. Don't rely on it for sorting by value, though. Sort explicitly.

## Check yourself

1. A list of 4,000 active quests is scanned by quest ID 60 times per frame, with `c_scan = 15 ns`. Compute the per-frame cost, and the cost with a dictionary at `c_hash = 30 ns`.
2. You need "remove the enemy that just died" on a list of 500 enemies where order doesn't matter. Give an O(1) method and explain why it's O(1).
3. Using an 8-bucket table with linear probing, insert keys 3, 11, 19 (in that order). Where does each go? How many comparisons does looking up 19 take?
4. Why can't a Python `list` be a dictionary key, while a `tuple` can?
5. A teammate replaces the projectile list (walked every frame, never searched) with a dictionary keyed by projectile ID "for speed." What got better, what got worse, and what would you tell them?

<details>
<summary>Answers</summary>

1. List: `60 × 15 ns × 2,000.5 ≈ 1.80 ms` per frame, about 11% of a 60 fps frame. Dictionary: `60 × 30 ns = 1.8 µs`, 1,000 times less.
2. Swap the dead enemy with the last element, then `pop()` the end. Both steps touch a fixed number of elements, whatever the list's length, so the cost doesn't grow with `n`. The order changes, which is fine here.
3. All three hash to bucket 3 (`3 mod 8`, `11 mod 8`, `19 mod 8`). 3 goes to bucket 3, 11 probes to 4, 19 probes to 5. Looking up 19 compares at 3, 4 and 5, so three comparisons. Keys that share a bucket cost extra probes, which is why hash quality matters.
4. A list can change after insertion, which would change its hash and strand it in the wrong bucket. A tuple can't change, so its hash is stable.
5. Nothing that matters got better, since nothing looks projectiles up by ID. Iteration got slightly slower, and memory use went up. Keep the list. Add a dictionary only if some code genuinely needs lookup by ID.

</details>

## Lab / assignment hook

[Lab 05, the item database](../labs/lab05.md). You implement `DictItemDB` and a set-based duplicate check in the starter code, run the benchmark on your machine, fill in the frame-cost table, reproduce the GTA-style loading blow-up at 20,000 items, and write a recommendation for a designer who wants to ship 50,000 item definitions.

## Sources

- t0st, "How I cut GTA Online loading times by 70%", nee.lv, 28 February 2021, with the author's later update. About 63,000 items, the array-scan duplicate check and its 1,984,531,500 comparisons, Rockstar's fix in March 2021. https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/
- Microsoft Learn, "Dictionary<TKey,TValue> Class", Remarks (.NET 8). Retrieval by key close to O(1) as a hash table; speed depends on the hash function; keys must not change their hash while in the dictionary. https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2
- Microsoft Learn, "List<T>.Contains(T) Method". Linear search, O(n). https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.contains
- Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2005). "The Implementation of Lua 5.0". *Journal of Universal Computer Science* 11(7). Tables as hybrids with an array part and a hash part, resized automatically. https://www.lua.org/doc/jucs05.pdf
- Warcraft Wiki, "Lua" (current, retrieved September 2026). WoW implements a subset of Lua 5.1; upgraded to Lua 5.1.1 in patch 2.0.1 (2006). https://warcraft.wiki.gg/wiki/Lua
- Nystrom, R. (2014). *Game Programming Patterns*. "Data Locality" (cache lines, cache misses costing hundreds of cycles), "Event Queue" (the O(n) duplicate scan and the hash-table alternative), "Spatial Partition" (doubly linked units per cell). https://gameprogrammingpatterns.com/
- Python Software Foundation, "collections: Container datatypes", Python 3 documentation. Lists incur O(n) memory movement for `pop(0)` and `insert(0, v)`. https://docs.python.org/3/library/collections.html
- Timings in this lecture: `labs/lab05-starter/item_db.py` and a small benchmark script, CPython 3.13.5 on an Apple silicon laptop, September 2026.

## Interactive spec: examples/w05-list-vs-dict-timing.html

**The one insight:** a list lookup of 10,000 items looks instant on its own (tens of microseconds), but multiplied by the lookups a frame needs it overruns the 16.67 ms budget, while a hash map's per-frame cost stays flat as `n` grows.

**Layout (two linked views, stacked on mobile, side by side at ≥ 900px):**

- Top or left, "per lookup": line chart, x-axis `n` from 10 to 100,000 on a log scale, y-axis microseconds per lookup on a log scale (0.001 to 10,000). Two lines, "array scan" and "Map". A vertical marker at the current `n`.
- Bottom or right, "per frame": a horizontal 16.67 ms frame strip with two bars, array and Map, each filled to `q × per-lookup time`. Overflow past the strip is drawn in the alert color and labelled "+N.N frames". A label under each bar gives ms to two decimals and percent of frame.

**Controls:**

- `n` slider on a log scale: 10, 30, 100, 300, 1,000, 3,000, 10,000, 30,000, 100,000 (default 10,000).
- `q` lookups per frame slider, 1 to 2,000, default 250.
- Mode toggle: "live" (default) or "model".
- Button "re-measure" (live mode only).

**Live mode:** build an array of `n` objects `{id, name, price}` with shuffled ids, and a `Map` from id to object. Time 200 random successful lookups with `arr.find(o => o.id === key)` and 20,000 with `map.get(key)` using `performance.now()`, repeat 3 times, take the minimum per-lookup time. Precompute all nine `n` values on load in small chunks with `requestIdleCallback` or `setTimeout` so the page stays responsive; show a "measuring" state on the chart until done. Display the browser's measured values next to the model values.

**Model mode (exact formulas):**

```
t_list(n)  = c_scan × (n + 1) / 2        c_scan = 15 ns
t_dict     = c_hash                      c_hash = 30 ns
frame_list = q × t_list(n)
frame_dict = q × t_dict
n_limit    = 2 × B / (q × c_scan) − 1    B = 1000/60 ms (shown as 16.67 ms)
```

**Test values (model mode, must match):**

- `n = 10,000`, `q = 250`: per-lookup list 75.0 µs, dict 0.030 µs; frame list 18.75 ms (112.5% of frame, "+0.1 frames"), frame dict 0.0075 ms.
- `n = 1,000`, `q = 250`: frame list 1.88 ms.
- `n = 100,000`, `q = 250`: frame list 187.5 ms ("+10.3 frames").
- `q = 250`: `n_limit = 8,888` (8,887.9 rounded), shown as a dashed vertical line on the per-lookup chart labelled "list overruns frame beyond here".

**First screen:** model mode values for `n = 10,000`, `q = 250`, with the list bar visibly running past the frame edge and the Map bar a thin sliver. Live measurements replace them once measuring finishes, with a note "your browser is faster than Python; the crossing moves, the shape stays."

**Accessibility:** controls keyboard operable with visible focus; text summary with `aria-live="polite"`; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. No game art or logos.
