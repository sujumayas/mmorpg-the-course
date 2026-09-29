# CS201 · Week 12 — Serialization and Save Files

**Why this matters:** A save file is a promise to a player that outlives the build that wrote it. Every patch you ship after launch changes the data, and the game must still open saves from every earlier version. Players forgive a crash. They do not forgive losing a 60-hour character. This week you design the engine's save system so that old saves keep loading, references survive the trip to disk, and a damaged file is detected instead of trusted.

**You will be able to:**
- Implement a versioned migration chain and compute how many upgrade functions it needs compared with direct converters.
- Design what an entity saves and what the engine rebuilds on load, using persistent IDs instead of runtime handles.
- Implement a two-pass loader that restores references, including cycles, and a file header that detects truncation and corruption.
- Critique a save format (Minecraft, Factorio, Protocol Buffers style) for how it handles change over years of patches.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 16, sections 16.3 "World Chunk Data Formats" and 16.4 "Loading and Streaming Game Worlds". Protocol Buffers documentation, "Language Guide (proto 3)," the section "Updating a Message Type" (about 10 minutes). Skim the Minecraft Wiki page "Data version."

**Prerequisites from earlier courses:** [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (templates plus per-instance data, and validation). [CS201 week 5, ECS design](w05-entity-component-system-design.md) (generational handles, which do not survive a save). [CS201 week 11, physics integration](w11-physics-integration-basics.md) (the physics world as derived state). Looking ahead to next semester: [CS202 week 5, serialization and bit packing](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w05-serialization-and-bit-packing.md) packs the same kind of data into network packets, [DB201 week 1, why persistence is hard](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) returns to the atomic write for servers, and [DB201 week 9, schema migrations in a live game](../../DB201-data-persistence-and-telemetry/lectures/w09-schema-migrations-in-a-live-game.md) is the server-side version of this week's problem.

**Interactive:** [`examples/w12-save-migration-chain.html`](../examples/w12-save-migration-chain.html). Keep it open during section 2.

---

## 1. What goes into a save

**Serialization** is turning in-memory objects into a sequence of bytes, and **deserialization** is the reverse. A **save file** is serialized game state that must be readable later, by a different build, on a different day, perhaps on a different machine.

The first design decision is what to leave out. A running game holds far more state than it needs to restore. Sort every piece of it into one of three bins.

- **Persistent state** cannot be recomputed. The player's health, inventory, quest flags, the world seed, which chests are open, where every dropped item lies.
- **Derived state** can be rebuilt from persistent state and game data on load. Pathfinding graphs, the physics world with its broad phase and islands (week 11), render caches, spatial grids, UI layout. Save none of it.
- **Transient state** does not matter after reload. Particles in flight, a camera shake, the frame accumulator's leftover time, which sound is half played.

Each bin has a cost when you get it wrong. Saving derived state bloats the file and, worse, lets it disagree with the persistent state it came from after a patch changes the rebuild rules. Forgetting persistent state is a bug players find in an hour. The door you opened is closed again, or the boss you killed is back.

Two habits keep saves small and stable.

**Save references to data, not copies of it.** CS102 week 13 put item stats in a table and gave each instance a template ID plus its own few values. A saved sword is `{"template": "iron_sword", "durability": 31}`, not a full copy of the sword's stats. When a patch rebalances iron swords, old saves get the new numbers for free.

**Save persistent IDs, not runtime handles.** Week 5's generational handle `(index, generation)` is only meaningful inside one run of the game. Load the save in a new session and slot 7 holds something else, or nothing. Every object that other objects can refer to gets a **persistent ID**, a number or string assigned once and stored in the save. Section 3 shows how references are rebuilt from those IDs.

In an ECS, these decisions become one flag per component type. `Health`, `Inventory` and `QuestState` are marked saveable. `RigidBodyHandle`, `RenderMeshInstance` and `PathCache` are not, and a load step rebuilds them from the saved components.

## 2. Worked example: the world that is nine years old

### The hook

Minecraft Java Edition stores an integer called the **data version** in every world save. The Minecraft Wiki records that data versions were added in snapshot 15w32a (the 1.9 development cycle, 2015), starting at 100. Release 1.21.1, in August 2024, has data version 3955. When you open a world whose data version is older than the game's, Minecraft does not refuse. It offers to back the world up first, and then loads it. When the world is *newer* than the game, it warns you that the world may become corrupted.

Thousands of version numbers, and a world from any of them can be opened by today's game. Mojang did not write a converter from every old version to every new one. They could not have. So what did they write?

### The model

Give every save a version number `v`. Keep one small upgrade function per version step, `f_v`, that converts a version `v` save into a version `v + 1` save. To load a save written at version `v` when the game is at version `N`, apply the chain:

```
load(save at v) = f_(N−1)( ... f_(v+1)( f_v(save) ) ... )
refuse if v > N
```

- `N` is the current save version, the one this build writes.
- `f_v` knows only about two adjacent versions. It is written once, in the patch that changed the format, and never edited after that.
- A save `N − v` versions old runs `N − v` functions on load.

Compare the alternative, **direct converters** from each old version straight to the current one. When you ship version `k`, every existing direct converter is now out of date, because its target moved. You must write `k − 1` new ones. Over `N` versions:

```
chain:   N − 1 functions written in total, 1 per release
direct:  1 + 2 + ... + (N − 1) = N(N − 1) / 2 functions written in total, k − 1 at release k
```

The chain grows linearly, and each release adds exactly one small function that a single programmer can test. Direct conversion grows quadratically, and old converters are rewritten over and over.

### Numbers you can check

Here is a toy save across four versions of a small RPG. Patch 1.1 renamed `hp` to `health`. Patch 1.2 changed positions from tile coordinates to pixels, with 16-pixel tiles. Patch 2.0 moved gold into a wallet that also holds a new currency.

```python
CURRENT = 4

def v1_to_v2(s):                     # patch 1.1: "hp" renamed to "health"
    s = dict(s)
    s["health"] = s.pop("hp")
    return s

def v2_to_v3(s):                     # patch 1.2: tile coordinates become pixels (16 px tiles)
    s = dict(s)
    tx, ty = s.pop("pos")
    s["x"], s["y"] = tx * 16, ty * 16
    return s

def v3_to_v4(s):                     # patch 2.0: gold moves into a wallet with a new currency
    s = dict(s)
    s["wallet"] = {"gold": s.pop("gold"), "gems": 0}
    return s

MIGRATIONS = {1: v1_to_v2, 2: v2_to_v3, 3: v3_to_v4}   # key = version it upgrades FROM

def upgrade(save):
    v = save["version"]
    if v > CURRENT:
        raise ValueError(f"save is version {v}, this build only knows up to {CURRENT}")
    while v < CURRENT:
        migrate = MIGRATIONS[v]
        save = migrate(save)
        v += 1
        save["version"] = v
        print(f"  -> v{v}: {save}")
    return save

old = {"version": 1, "hp": 35, "gold": 120, "pos": [3, 4]}
print(f"loaded v1: {old}")
new = upgrade(old)
try:
    upgrade({"version": 5, "health": 1})
except ValueError as e:
    print("refused:", e)
```

```
loaded v1: {'version': 1, 'hp': 35, 'gold': 120, 'pos': [3, 4]}
  -> v2: {'version': 2, 'gold': 120, 'pos': [3, 4], 'health': 35}
  -> v3: {'version': 3, 'gold': 120, 'health': 35, 'x': 48, 'y': 64}
  -> v4: {'version': 4, 'health': 35, 'x': 48, 'y': 64, 'wallet': {'gold': 120, 'gems': 0}}
refused: save is version 5, this build only knows up to 4
```

Check the pixel step by hand: tile `(3, 4)` times 16 is `(48, 64)`. Each function touches one field and knows nothing about the others. `v1_to_v2` was written when version 2 was current and still works unchanged when version 4 ships. The version 5 save is refused with a clear message, because a build cannot know what a future patch meant.

Now the counts:

| Save versions shipped `N` | Chain: functions written | Direct: functions written | Direct: written at the latest release |
|---|---|---|---|
| 2 | 1 | 1 | 1 |
| 4 | 3 | 6 | 3 |
| 10 | 9 | 45 | 9 |
| 20 | 19 | 190 | 19 |
| 50 | 49 | 1,225 | 49 |

At 20 versions, a modest number for a game with a few years of patches, direct conversion has had you write 190 converters, and every release adds one more per old version. The chain has 19, each a few lines long, each tested once against a real old save and then frozen.

The insight is that **each change to the format is paid for once, at the moment it is made, by the person who made it.** Nobody has to understand version 3's layout when writing version 20.

### A visual you can move

Open `examples/w12-save-migration-chain.html`. The left view is a row of boxes, one per version, joined by arrows labeled with what each migration does. Pick a starting version for the toy save and press "load". The save's fields are shown under the first box and flow along the arrows, changing at each step until they reach the current version. The right view plots functions written against versions shipped, with the chain as a straight line and direct conversion as a curve bending upward.

Drag the "versions shipped" slider to 50 and watch the gap open. Then click "new patch" to add a version. The chain gains one arrow on the left. The direct counter on the right jumps by the number of old versions, and every old-version box flashes because its converter is now out of date.

### Cross-game recognition

**Minecraft Java Edition (DataFixerUpper, 1.9 onward).** Mojang publishes the library behind the upgrade, DataFixerUpper, on GitHub. Its README describes two core types. A `Schema` defines the data types at one version, and a `DataFix` is a rewrite rule between types. A builder takes the list of schemas and fixes and produces an optimized converter. That is our chain, `f_v` as `DataFix`, with an optimization pass so a very old world does not pay for every step one at a time. Each `.dat` file carries its own `DataVersion`, so different parts of one world can be upgraded independently.

**Factorio (migrations, API docs version 2.1).** Factorio's migrations are `.lua` or `.json` files in a mod's `migrations` folder, run in order of mod and then file name. The key difference is how the save remembers progress. Instead of one version integer, each save records *by name* which migrations from which mods have already run, and never runs the same one twice. Factorio saves are shared by many mods that update on their own schedules, so a single integer could not describe them all. A set of applied names can. It is the same chain, with the "current version" replaced by "every migration not yet applied."

**Protocol Buffers (proto3, current documentation).** Here there is no chain at all. Every field carries a number on the wire. Adding a field is safe, because old data simply lacks it and the reader uses a default. Old readers skip fields they do not know. Removing a field is safe as long as its number is never reused. Changing an existing field's number is unsafe. This is **schema evolution by rule**. It handles additions and deletions for free, and it cannot express a transformation like "tiles become pixels" or "gold moves into a wallet." Many games combine the two. Tagged fields absorb the easy changes, and a small chain handles the rest.

Three systems, one question answered three ways. How does data written yesterday find its meaning today? By a numbered chain, by a set of named steps, or by tags that let most changes need no step at all.

### Eyes-open design judgment

- **Never edit or delete a shipped migration.** Some player somewhere has a save that needs it. If a migration had a bug, add a new migration that repairs its output.
- **Keep a real save from every shipped version in your test suite.** A "golden file" per version, loaded and upgraded on every build, is the only proof the chain still works. Generated test saves miss the odd data real players create.
- **Write back upgraded saves, and keep the original.** After a successful load and upgrade, the next save writes the current version, so the chain runs once per save file, not on every load. Keep the old file as a backup, as Minecraft offers to.
- **Refuse newer saves loudly.** A build that half-reads a future format will quietly drop fields and then write the damaged save back.
- **Decide what you will not support.** Some studios cut off saves older than a major release, with a message. That is a legitimate choice if you announce it. Silent failure is not.
- **Transformations need a chain, additions do not.** If most of your changes are "add a field with a default," tagged fields cost less. If you rename, split, merge and change units, you need the chain.

### Check yourself (worked example)

1. A game has shipped 12 save versions. How many migration functions exist with a chain? How many converters would the direct approach have had you write in total?
2. Patch 2.1 makes version 5: `health` becomes a fraction of `max_health`, with `max_health = 50` for every existing save. Write `v4_to_v5`. What does the lecture's v1 save look like after loading in the 2.1 build?

<details>
<summary>Answers</summary>

1. Chain: `12 − 1 = 11`. Direct: `12 × 11 / 2 = 66`.
2. `def v4_to_v5(s): s = dict(s); s["max_health"] = 50; s["health"] = s["health"] / 50; return s`. The v1 save becomes `{"version": 5, "health": 0.7, "x": 48, "y": 64, "wallet": {"gold": 120, "gems": 0}, "max_health": 50}`, after four migrations.

</details>

## 3. References: from handles to IDs and back

Objects point at each other. A guard follows a captain, a quest tracks a target, a chest remembers who looted it. In memory these are pointers or week 5 handles, and neither means anything in a file. The fix has two halves.

**On save,** write each reference as the target's persistent ID. **On load,** use two passes. First create every object from its saved data, with references empty, and record each one in a table keyed by persistent ID. Then walk the saved data again and fill in each reference by looking up the ID. Two passes are needed because a reference can point forward to an object not yet created, or form a cycle.

```python
import json

class Npc:
    def __init__(self, uid, name):
        self.uid, self.name, self.follows = uid, name, None   # follows: another Npc or None

guard = Npc(1001, "guard")
captain = Npc(1002, "captain")
guard.follows = captain                       # a live reference (a pointer in C++)
captain.follows = guard                       # references can form cycles

def save(npcs):
    return json.dumps([{"uid": n.uid, "name": n.name,
                        "follows": n.follows.uid if n.follows else None} for n in npcs])

def load(text):
    rows = json.loads(text)
    by_uid = {r["uid"]: Npc(r["uid"], r["name"]) for r in rows}      # pass 1: create everything
    for r in rows:                                                    # pass 2: link by uid
        if r["follows"] is not None:
            by_uid[r["uid"]].follows = by_uid.get(r["follows"])     # missing target -> None
    return list(by_uid.values())

text = save([guard, captain])
print(text)
g, c = load(text)
print(g.name, "follows", g.follows.name, "| captain follows", c.follows.name)
print("cycle intact:", g.follows.follows is g)
```

```
[{"uid": 1001, "name": "guard", "follows": 1002}, {"uid": 1002, "name": "captain", "follows": 1001}]
guard follows captain | captain follows guard
cycle intact: True
```

A single-pass loader would crash or leave the guard following nothing, because the captain does not exist yet when the guard is read. Note the `by_uid.get` in pass 2. If a patch removed the thing a reference pointed at, the reference becomes empty instead of crashing the load. Factorio's migration docs describe exactly this case. When a prototype is removed, saved references to it become invalid.

Where do persistent IDs come from? Three common sources.

- **A counter saved with the world.** Simple and compact. The counter itself must be saved, or IDs will repeat after a reload.
- **Level-authored IDs** for objects placed in the editor, such as the chest in room 4. The save then stores only what changed about them, a **delta** against the level file, which keeps saves small in big hand-built worlds.
- **Random 64- or 128-bit IDs** when objects are created in many places at once and cannot share a counter, for example on several servers. Bigger, but collision-free in practice.

At load time, each persistent ID maps to a fresh runtime handle. The mapping lives only as long as the session.

## 4. The file on disk

### Header and checksum

A save file should say what it is before it says anything else. A small fixed **header** at the start holds a **magic number** (a few bytes that identify the file type), the save version, the payload length and a **checksum**. A checksum is a short number computed from the payload, here CRC-32. It lets the loader detect a truncated or damaged file instead of parsing garbage.

```python
import json
import struct
import zlib

MAGIC = b"LKSV"                                   # identifies our file type
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

blob = pack({"version": 4, "health": 35, "x": 48, "y": 64, "wallet": {"gold": 120, "gems": 0}})
print(len(blob), "bytes, header", HEADER.size)
print(unpack(blob)["wallet"])
for name, bad in [("truncated", blob[:-5]),
                  ("one byte flipped", blob[:30] + bytes([blob[30] ^ 1]) + blob[31:])]:
    try:
        unpack(bad)
    except ValueError as e:
        print(name, "->", e)
```

```
98 bytes, header 16
{'gems': 0, 'gold': 120}
truncated -> truncated: expected 82 bytes, got 77
one byte flipped -> corrupted: checksum mismatch
```

The header is 16 bytes, `<` for **little-endian** (least significant byte first, the order x86 CPUs and nearly all ARM systems use) and four 4-byte fields. Putting the version in the header, outside the payload, lets the loader pick the right parser before it reads anything else. That matters when a patch changes the payload encoding itself, say from JSON to a binary format.

A CRC detects accidents, not attacks. Anyone who edits the save can recompute it. For a single-player game that is fine, and many players see editing their own save as their right. For anything competitive, the server keeps the authoritative state and the client's file is a cache (next semester, [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md)).

### Writing without destroying the old save

The fix is an **atomic write** (DB201 week 1 returns to it for servers next semester). Write the new save to a temporary file, flush it to disk with `fsync`, then rename it over the old one with `os.replace`, so a crash leaves either the old file or the new one, never half of each. Minecraft's world folder shows the same pattern. The Minecraft Wiki's level format page lists `level.dat_new`, which is written first and then renamed to `level.dat`, and `level.dat_old`, a backup of the previous `level.dat`. Keep a backup like that. If a migration has a bug, the backup is the only copy of the player's world that the bug has not touched.

### Text or binary

JSON is easy to read, diff and hand-edit, and it keeps field names, which makes migrations easy to write. A binary format with fixed fields and quantization (CS202 week 5 builds one next semester) is smaller and faster to parse. A reasonable engine default is text during development and a compact binary for shipped builds, both produced from the same component descriptions, with the version in the header either way. If your saves are small, stay with text. The disk will not notice 98 bytes.

## In-class activity (25 minutes)

In groups of three, design the save system for a farming game with a player, 30 crops per field in up to 10 fields, 12 NPCs with friendship levels and daily schedules, and a calendar.

1. Sort at least 15 pieces of state into persistent, derived and transient.
2. Write the version 1 save layout as JSON. Give every referable object a persistent ID and say where the ID comes from.
3. Your producer announces three patches: crops gain a "quality" field (default "normal"), friendship changes from 0-10 hearts to 0-1,000 points, and two NPCs merge into one. Write the three migration functions as pseudocode. Which of the three would tagged fields have handled without a migration?
4. Swap with another group. Load their version 1 save with your migrations applied in your head. Find one reference that breaks.

Expected output: the state table, the v1 JSON, three migrations, and the broken reference your partners found.

## Common misconceptions

- **"Saving is dumping every object to JSON."** Most of the state in memory is derived or transient. Saving it bloats the file and freezes today's rebuild rules into every save.
- **"We'll add versioning when we need it."** The first save you ship without a version field is the one you cannot upgrade, because the loader cannot tell it apart from a later format. Put `version` in the header from day one.
- **"A runtime handle is a good enough ID."** It is valid for one session. After a reload, slot 7 holds a different object. Save persistent IDs.
- **"A checksum stops cheating."** It detects accidental damage. Anyone can recompute it.

## Check yourself

1. A game saves a `PathCache` component for every NPC. Name two problems this causes after a patch that changes the navigation mesh.
2. A save chain has 30 versions. A player loads a version 3 save. How many migrations run? After the game saves again, how many will run the next time that file is loaded?
3. In the two-pass loader, what happens if the save lists the captain before the guard? What happens with a single-pass loader in each order?
4. A 200-byte save file's header says its payload is 184 bytes, but the file on disk is 150 bytes. Which check fires, and what should the game do next?
5. Your team uses tagged fields only, with no migrations. Name one change from this lecture's toy save history that tagged fields cannot express, and what would happen to old saves if you shipped it anyway.

<details>
<summary>Answers</summary>

1. The cached paths follow the old mesh, so NPCs walk through new walls or get stuck. And the save is larger than it needs to be for data the engine can rebuild in milliseconds.
2. `30 − 3 = 27` migrations. After the game writes the upgraded save, it is version 30, so zero run next time.
3. Two-pass works in either order, because every object exists before any link is made. Single-pass fails for whichever object is read first when its target comes later. The guard-first order leaves the guard's reference unresolved, and with a cycle, one of the two references always fails.
4. The header is 16 bytes, so the payload on disk is `150 − 16 = 134` bytes, not 184. The length check fires ("truncated"). The game should not load it. It should try the backup (for example, the `_old` copy) and tell the player what happened.
5. Tiles to pixels (or gold into a wallet). A tagged reader would find no `x` and `y`, use defaults (0, 0), and put every old player at the map origin. Or it would find no `wallet` and give them zero gold, while the old `gold` field is ignored.

</details>

## Lab / assignment hook

[Lab 12, a save system that survives patches](../labs/lab12.md). You build the engine's save pipeline in Python: a migration chain with golden-file tests, persistent IDs with a two-pass loader, a checksummed header, and an atomic write with a backup. Then you ship three patches to your own format and prove every old save still loads.

## Sources

- Minecraft Wiki, "Data version" (Java Edition, retrieved September 2026). Added in 15w32a during 1.9 development, starting at 100; stored as `DataVersion` in `.dat` files; backup prompt for older worlds and corruption warning for newer ones. https://minecraft.wiki/w/Data_version
- Minecraft Wiki, "Java Edition 1.21.1" (released 8 August 2024; data version 3955). https://minecraft.wiki/w/Java_Edition_1.21.1
- Minecraft Wiki, "Java Edition level format." `level.dat_new` written then renamed to `level.dat`; `level.dat_old` backup. https://minecraft.wiki/w/Java_Edition_level_format
- Mojang, DataFixerUpper README (GitHub). `Schema`, `DataFix`, and a builder that creates an optimized converter between schemas. https://github.com/Mojang/DataFixerUpper
- Factorio Lua API, Auxiliary docs, "Migrations," version 2.1.20. Migration files per mod, ordering, per-save record of applied migrations by name, invalid references after a prototype is removed. https://lua-api.factorio.com/latest/auxiliary/migrations.html
- Protocol Buffers documentation, "Language Guide (proto 3)," section "Updating A Message Type." Adding and removing fields is wire-safe; changing field numbers is not; old parsers ignore unknown fields. https://protobuf.dev/programming-guides/proto3/
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 16, sections 16.3 and 16.4.

## Interactive spec: examples/w12-save-migration-chain.html

**The one insight:** a migration chain costs one small function per release forever, while direct converters cost a growing pile of rewrites, so the chain is what lets a game open saves from years ago.

**Layout.** Two linked views, stacked on mobile, side by side at 1,280 px.

- **Left view, "the chain".** A horizontal (on mobile, vertical) row of version boxes v1 to vN (N from the slider). When N > 8, draw the four built-in boxes v1 to v4, a dashed "..." gap box standing for the middle patches (one animation step), and the last four versions, so the named migrations stay visible. Arrows between boxes carry short labels. For the four built-in versions use: v1→v2 "hp → health", v2→v3 "tiles × 16 → pixels", v3→v4 "gold → wallet", and for any further versions "patch k" (identity migrations that only bump the version). Under the chain, a code-styled panel shows the current save JSON.
- **Right view, "the cost".** Line chart of functions written (y) against versions shipped `N` (x, 1 to 50). Two series: chain `N − 1` (straight) and direct `N(N − 1)/2` (curve). A dot on each at the current `N`. Readouts beside the chart.

**Controls.**
- Starting version selector (v1 to v4, and "v(N+1): from the future").
- "Load" button: animates the save moving box by box (one step per 600 ms; instant under `prefers-reduced-motion`), updating the JSON panel after each migration and highlighting the arrow used. Loading "from the future" shows a red refusal message: "save is version N+1, this build only knows up to N".
- "Versions shipped" slider `N`: 4 to 50, default 4.
- "New patch" button: increments `N` by 1. The chain gains one arrow. The direct counter shows "+(N−1) converters to rewrite", and every earlier box flashes once.
- Toggle "tagged fields": marks each built-in migration as "needs a migration" (renames, unit change, restructure) or "free with tags" (patches that only add a field with a default). With the toggle on, the "patch k" versions are treated as additive and drawn with dashed arrows.

**Readouts.** Current `N`; chain functions `N − 1`; direct total `N(N − 1)/2`; direct written at the latest release `N − 1`; migrations run for the selected start version `N − v`.

**Exact states (test values).**
- v1 start: `{"version": 1, "hp": 35, "gold": 120, "pos": [3, 4]}`.
- After v2: `{"version": 2, "gold": 120, "pos": [3, 4], "health": 35}`.
- After v3: `{"version": 3, "gold": 120, "health": 35, "x": 48, "y": 64}`.
- After v4: `{"version": 4, "health": 35, "x": 48, "y": 64, "wallet": {"gold": 120, "gems": 0}}`.
- Counts: `N = 4` gives chain 3, direct 6. `N = 10` gives 9 and 45. `N = 20` gives 19 and 190. `N = 50` gives 49 and 1,225.

**First screen.** `N = 20`, v1 selected and already loaded to the end, so the chain, the final JSON and the 19-versus-190 gap are visible without interaction. Keyboard: all controls reachable with Tab; the Load button responds to Enter and Space. Respect `prefers-color-scheme`.
