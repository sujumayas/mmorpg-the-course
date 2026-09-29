# CS201 · Week 14 — Tools and Editors

**Why this matters:** Most people who touch your engine will never read its code. Designers, artists and level builders work through an editor, and every number they tune has to reach an inspector panel, a save file, the undo history and often the network. If each of those is written by hand for each field, your tools fall behind the game within a month. This week you learn how engines describe their own data once, so that every tool can read it, and what that choice costs.

**You will be able to:**
- Compute how the amount of tool code grows with the number of fields and tool systems, with and without a reflection layer, and estimate how many hand-added fields will miss a system.
- Implement a small reflection layer (field declarations with metadata) and write an inspector, a serializer and a validated loader that work for any component.
- Design an undo history that groups many small edits into one transaction and works for every field without per-field code.
- Critique a tool plan: what belongs in the editor, what in an in-game debug panel, and what breaks when a reflected field is renamed.

**Before class:** Unreal Engine 5.8 documentation, "Unreal Engine UProperties" (the introduction and the table of specifiers; skim the rest) and "Core Redirects" (the introduction and the property example). Godot 4.7 documentation, "Godot's design philosophy", the section "The Godot editor is a Godot game", and "GDScript exported properties", the introduction. The Dear ImGui README on GitHub, the first two sections.

**Prerequisites from earlier courses:** [CS101 week 7, scenes, nodes and scripts](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (you used `@export` there; this week shows what sits behind it). [CS102 week 12, the Command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (undo and redo stacks; not re-taught here). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (validation on load, and the cost of a tuning loop). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one miss). [AR101 week 14, the art pipeline](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) (import settings, which are reflected fields from the artist's side). From this course: [week 5, components as plain data](w05-entity-component-system-design.md), [week 7, resources and hot reload](w07-resource-management-and-hot-reload.md), [week 10, the scripting layer](w10-scripting-layer-integration.md) and [week 13, profiling](w13-profiling-cpu-gpu-frame-budgets.md). [Week 12, serialization and save files](w12-serialization-and-save-files.md) (versioned saves and migrations).

**Interactive:** [`examples/w14-fields-times-systems.html`](../examples/w14-fields-times-systems.html). Keep it open during section 2.

---

## 1. What an editor is for

An **editor** is a program whose users are the rest of the team and whose output is data. The level designer drags a spawner into a room and sets its wave count to 4. The editor writes that into a level file. The runtime, the part of the engine that ships to players, reads the file and spawns four waves. Nobody recompiled anything.

That is the whole contract. Everything else in this lecture is about keeping it cheap to maintain as the game grows.

Some vocabulary first.

- A **tool** is any program that helps build the game without being part of it: the level editor, an importer that turns art files into engine textures (AR101 week 14), a crash reporter, a localization checker.
- An **inspector** (Unity and Godot) or **details panel** (Unreal) is the part of an editor that shows the fields of the selected object and lets you change them.
- **Play-in-editor** means running the game inside the editor window, with the editor's data already loaded, so a designer can press play, test and stop in seconds.
- **Editor-only code** is code compiled into the editor build but stripped from the shipped game: gizmos, inspectors, validation that runs at save time.
- **Reflection** is a program's ability to describe its own types: which fields a type has, their names, their types and anything else you attach to them. C# and Python can do this at run time. C++ could not until compile-time reflection was voted into the draft C++26 standard in June 2025, and compiler support is still arriving, so C++ engines have long built their own.

Where does the editor live? Two families exist. In Godot, the editor is itself a Godot program. The Godot documentation says the editor runs on the game engine and uses the engine's own UI system, so any code or scene you write for a game can also run inside the editor. Unreal and Unity likewise ship an editor that contains the full engine runtime, which is what makes play-in-editor possible. The other family keeps tools as separate programs (a standalone level editor, a spreadsheet exporter) that talk to the game through files or a network connection. That keeps the runtime small and the tools free to use any UI library, at the cost of never seeing the real game while you edit.

Your course engine will do the first, in a small way. The same executable runs as game or editor depending on a flag, and editor-only code sits behind `#ifdef ENGINE_EDITOR`. The question for today is how the editor finds out what to show.

## 2. Worked example: one declaration, every tool

### The hook

In Unreal Engine, put one line above a C++ member:

```cpp
UPROPERTY(EditAnywhere, meta = (ClampMin = "0"))
float Armor;
```

This fragment needs Unreal's build tools and does not compile on its own. Build the project, and `Armor` appears in the editor's Details panel with a number box that refuses negative values. It is saved with the level and loaded back. Add `BlueprintReadWrite` and designers can use it in visual scripts. Add `Replicated` and it is sent to clients over the network. Unreal's documentation lists these specifiers side by side: `EditAnywhere` for property windows, `BlueprintReadWrite` for Blueprint access, `Replicated` for networking, `ClampMin` for the smallest value the editor accepts.

Nobody on your team wrote the number box, the save code, the load code or the network code for `Armor`. Somebody wrote each of those once, for every property in the engine. How much work does that save, and what does it cost?

### The model

Name the quantities.

- `F` is the number of fields that tools must know about, across all component types.
- `S` is the number of **tool systems** that handle every field: for example the inspector, save, load, undo and network replication.
- `q` is the chance that a programmer forgets one of the places a new field must be added.

Without reflection, every system has a hand-written line (or block) for every field. With reflection, each field is declared once with its metadata, and each system is written once as a loop over the declarations:

```
by hand:     code sites = F × S           a new field costs S edits in S places
reflected:   code sites = F + S           a new field costs 1 edit
chance a hand-added field reaches every system = (1 − q)^S
```

The first line is a product and the second a sum. That difference is the whole argument for reflection. The third line is the complement rule from MA102 week 3. Each of the `S` edits has to go right, independently, so the chance that at least one is missed is `1 − (1 − q)^S`.

### Numbers you can check

Here is a reflection layer in Python, small enough to read in a minute. Python's `dataclasses` module already knows each class's fields, so the only thing we add is metadata: range, and which systems want the field.

```python
from dataclasses import dataclass, field, fields

def prop(default, lo=None, hi=None, save=True, edit=True, net=False):
    """Declare a field once; the metadata tells every tool what to do with it."""
    return field(default=default,
                 metadata={"lo": lo, "hi": hi, "save": save, "edit": edit, "net": net})

@dataclass
class Health:
    current: int = prop(100, lo=0, hi=9_999, net=True)
    maximum: int = prop(100, lo=1, hi=9_999)
    regen_per_s: float = prop(1.5, lo=0.0, hi=50.0)
    last_hit_by: int = prop(0, save=False, edit=False)      # runtime bookkeeping only

# Each tool below is written once and works for every component.
def inspector(obj):
    for f in fields(obj):
        if f.metadata["edit"]:
            lo, hi = f.metadata["lo"], f.metadata["hi"]
            print(f"  {f.name:<12} [{lo}..{hi}]  {getattr(obj, f.name)}")

def save(obj):
    return {f.name: getattr(obj, f.name) for f in fields(obj) if f.metadata["save"]}

def load(cls, data):
    obj = cls()
    for f in fields(cls):
        if f.metadata["save"] and f.name in data:
            lo, hi = f.metadata["lo"], f.metadata["hi"]
            setattr(obj, f.name, min(max(data[f.name], lo), hi))
    return obj

def replicate(obj):
    return {f.name: getattr(obj, f.name) for f in fields(obj) if f.metadata["net"]}

h = Health(current=80)
print("inspector:"); inspector(h)
print("save:     ", save(h))
print("load:     ", load(Health, {"current": 12_000, "regen_per_s": 2.0}))
print("replicate:", replicate(h))
```

It prints:

```
inspector:
  current      [0..9999]  80
  maximum      [1..9999]  100
  regen_per_s  [0.0..50.0]  1.5
save:      {'current': 80, 'maximum': 100, 'regen_per_s': 1.5}
load:      Health(current=9999, maximum=100, regen_per_s=2.0, last_hit_by=0)
replicate: {'current': 80}
```

Four tools, and none of them mentions `current`, `maximum` or `regen_per_s` by name. `last_hit_by` is invisible to the inspector and the save file because its metadata says so. The loader clamped a bad value of 12,000 to the declared maximum, the kind of validation CS102 week 13 wrote by hand for each column.

Now the designer asks for armor. Append this to the same file:

```python

@dataclass
class Health:                                               # the same class, one line longer
    current: int = prop(100, lo=0, hi=9_999, net=True)
    maximum: int = prop(100, lo=1, hi=9_999)
    regen_per_s: float = prop(1.5, lo=0.0, hi=50.0)
    armor: int = prop(0, lo=0, hi=500, net=True)            # the new field
    last_hit_by: int = prop(0, save=False, edit=False)

h = Health(current=80, armor=35)
print("inspector:"); inspector(h)
print("save:     ", save(h))
print("replicate:", replicate(h))
```

The new lines print:

```
inspector:
  current      [0..9999]  80
  maximum      [1..9999]  100
  regen_per_s  [0.0..50.0]  1.5
  armor        [0..500]  35
save:      {'current': 80, 'maximum': 100, 'regen_per_s': 1.5, 'armor': 35}
replicate: {'current': 80, 'armor': 35}
```

One edit, and armor is in the inspector with its range, in the save file and on the network. That is what `UPROPERTY` does for Unreal programmers.

Now count. This short program applies the model to a few project sizes.

```python
def sites(fields_, systems):
    return {"by hand": fields_ * systems, "reflected": fields_ + systems}

def p_complete(systems, q):
    """Chance a hand-added field reaches every system if each edit is missed with chance q."""
    return (1 - q) ** systems

for F, S in [(6, 5), (240, 5), (240, 8), (1_000, 8)]:
    print(f"F={F:5}  S={S}  ", sites(F, S))
for S in (3, 5, 8):
    print(f"S={S}: {100 * (1 - p_complete(S, 0.02)):4.1f}% of new fields miss at least one system")
print(f"60 new fields, S=5: expect {60 * (1 - p_complete(5, 0.02)):.1f} with a hole")
```

It prints:

```
F=    6  S=5   {'by hand': 30, 'reflected': 11}
F=  240  S=5   {'by hand': 1200, 'reflected': 245}
F=  240  S=8   {'by hand': 1920, 'reflected': 248}
F= 1000  S=8   {'by hand': 8000, 'reflected': 1008}
S=3:  5.9% of new fields miss at least one system
S=5:  9.6% of new fields miss at least one system
S=8: 14.9% of new fields miss at least one system
60 new fields, S=5: expect 5.8 with a hole
```

Check the middle rows by hand. A modest game with 40 component types of about 6 fields each has `F = 240`. With five systems, hand-written tools need `240 × 5 = 1,200` code sites. Reflected, they need 240 declarations and 5 loops. Add three more systems (a diff view for merging level files, a search tool, a scripting binding from week 10) and the hand-written count rises by 720. The reflected count rises by 3.

The miss rate is where players notice. Suppose a careful programmer forgets one of the places a field must go only 2% of the time (the `q` here is an assumption; plug in your own team's). With five systems, `1 − 0.98^5 = 9.6%` of new fields have a hole. Sixty new fields in a milestone means about six of them are, for example, editable but not saved, or saved but not loaded. That second one is the classic bug where a designer's change "does not stick" after reloading the level.

### Move it yourself

Open [`examples/w14-fields-times-systems.html`](../examples/w14-fields-times-systems.html). The main view is a grid, one row per field and one column per tool system. In "by hand" mode every cell is a separate code site, drawn as a small block, and with the miss rate `q` above zero some blocks are drawn as red holes. In "reflected" mode the cells fill themselves: one block per row at the left (the declaration) and one per column at the top (the loop). The second view is a line chart of code sites against `F` for both modes. Drag `F` from 6 to 300 and watch the by-hand grid fill with red while the reflected count creeps up. Then drag `S` from 5 to 8. The by-hand line gets steeper. The reflected line barely moves.

### Cross-game recognition

Every major engine has this layer. The syntax differs; the shape `F + S` does not.

**Unreal Engine 5.8, `UPROPERTY`.** The macro is the declaration, the specifiers are the metadata, and a code generator writes the reflection data. Unreal's documentation describes Unreal Header Tool as parsing the C++ headers for these macros and generating code for the UObject system, before the C++ compiler runs. The Details panel, serialization, Blueprint access, garbage collection and replication are the `S` systems that read it.

**Unity 6.6, `[SerializeField]`.** C# has reflection built into the language, so Unity needs no code generator. Unity serializes public fields by default. The `[SerializeField]` attribute makes a private field serialized too, and a serialized field appears in the Inspector. Attributes such as `[Range]` (which turns a number field into a slider limited to a range) and `[Tooltip]` are the metadata. One attribute feeds save, load and the Inspector at once.

**Godot 4.7, `@export`.** Godot's documentation says an exported property is saved with the resource or scene it belongs to and is editable in the property editor, and that exported values are also transferred in remote procedure calls. Hints such as a range (`@export_range(0, 500)`) are the metadata. You wrote `@export var speed` in CS101 week 7. That line was a reflected field declaration.

Three engines, three syntaxes: a macro processed by a code generator, a language attribute read by C# reflection, and a script annotation. In all three, a field is declared once, and every tool loops over the declarations.

### Eyes-open design judgment

- **Reflection has a build cost.** Unreal pays for it with a code-generation step before every compile, and with rules about where macros may appear. A hand-rolled C++ table (section 3) has no generator but must be kept in step with the struct by hand. The miss rate `q` moves; it does not vanish.
- **It has a run-time cost.** Looping over field descriptors and converting values through a generic path is slower than direct member access. That is fine in an inspector redraw and wrong in a system that touches 100,000 components per frame. Keep reflection on the tools side and at load time. Week 10 showed the same trade-off for a reflection-based script binding.
- **Everything reflected becomes data that outlives code.** Once a field is in a save file, renaming it breaks old files (section 5). Declare fields as carefully as you would design a file format, because that is what they are.
- **Metadata can lie.** If the declaration says `save=False` for a field that must persist, every tool will faithfully get it wrong. The failure moves from "forgot a system" to "declared it wrong". The second kind is easier to find, because there is one place to look.
- **Small projects may not need it.** With `F = 6` and `S = 5`, you save 19 code sites. For a jam game, a hand-written debug panel is the right call. The break-even comes quickly once a team and a level editor exist.

### Check yourself on the worked example

1. A project has 150 fields and 6 tool systems. How many code sites by hand and reflected? How many more does each approach need if you add a seventh system?
2. With `q = 3%` and `S = 6`, what fraction of new hand-added fields miss at least one system? Out of 40 new fields, how many do you expect to be broken?
3. In the Python example, a designer sets armor to 900 in a save file by hand. What does `load` produce, and which line of code enforces it?

<details>
<summary>Answers</summary>

1. By hand `150 × 6 = 900`, reflected `150 + 6 = 156`. A seventh system adds 150 sites by hand and 1 reflected.
2. `1 − 0.97^6 = 1 − 0.833 = 16.7%`. Out of 40 fields, about 6.7 are expected to be broken.
3. `armor = 500`. The loader clamps with `min(max(value, lo), hi)`, reading `hi = 500` from the field's metadata. No line mentions armor.

</details>

## 3. Reflection in C++ without a code generator

C++17 and C++20, the standards your engine uses, cannot list a struct's fields. You can still build the reflection data yourself with **pointers to members**: a value like `&Health::current` that names a field of a type, not of an object. Given an object `h`, the expression `h.*member` reads that field.

```cpp
#include <cstdio>
#include <string_view>

struct Health { float current = 100, maximum = 100, regen_per_s = 1.5f; };

struct FloatField { const char* name; float Health::* member; float lo, hi; };

// The reflection data: written once per component type, read by every tool.
constexpr FloatField kHealthFields[] = {
    {"current",     &Health::current,     0, 9999},
    {"maximum",     &Health::maximum,     1, 9999},
    {"regen_per_s", &Health::regen_per_s, 0, 50},
};

void inspect(const Health& h) {                 // one tool: the inspector
    for (const auto& f : kHealthFields)
        std::printf("%-12s [%g..%g]  %g\n", f.name, f.lo, f.hi, h.*f.member);
}

void set_clamped(Health& h, const char* name, float v) {   // another: a validated setter
    for (const auto& f : kHealthFields)
        if (std::string_view(f.name) == name)
            h.*f.member = v < f.lo ? f.lo : (v > f.hi ? f.hi : v);
}

int main() {
    Health h;
    set_clamped(h, "current", 12000);
    inspect(h);
}
```

Compiled with `clang++ -std=c++17 fields.cpp`, it prints:

```
current      [0..9999]  9999
maximum      [1..9999]  100
regen_per_s  [0..50]  1.5
```

This version handles one struct and one field type to stay short. A real engine generalizes it in three steps: a field descriptor that stores a type tag and a byte offset or a getter and setter pair instead of a typed member pointer; a registry that maps a component's name to its descriptor table; and a macro so that declaring the table takes one line per field. Components as plain data (week 5) make this easy, because every field is a number, a small fixed array, an enum or a handle.

The weak point is visible in the code. The table sits next to the struct, not inside it. Add a field to `Health` and forget the table, and every tool silently ignores it. That is `q` again, now with `S = 1`: one place to forget instead of five. Unreal's code generator and C#'s built-in reflection remove even that one, at the build and runtime costs listed above.

## 4. Editing as transactions

Undo is one of the `S` systems, and reflection makes it generic. CS102 week 12 built undo from command objects, each storing enough to reverse itself. An editor needs only one command type for most edits: "set field `name` of object `obj` from `old` to `new`". Reflection supplies the name and the ability to read and write any field.

The new problem in an editor is granularity. When a designer drags a slider, the mouse sends dozens of move events. If each becomes an undo entry, pressing undo once moves the slider back by one pixel. The fix is a **transaction**: a group of edits that undo and redo together, opened when the drag starts and closed when the mouse button comes up. Within one transaction, repeated edits to the same field keep the first old value and the last new value.

Append this to the same file as section 2's example:

```python

class History:
    """Generic undo: one record type (object, field, old, new) serves every component."""
    def __init__(self):
        self.done, self.open = [], None

    def begin(self, label):
        self.open = (label, {})                      # (obj id, field) -> [obj, field, old, new]

    def set(self, obj, name, value):
        edits = self.open[1]
        key = (id(obj), name)
        if key not in edits:                         # keep the value from before the drag
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

hist = History()
hist.begin("drag armor slider")
for v in range(35, 95, 1):                           # 60 mouse-move events
    hist.set(h, "armor", v)
hist.end()
print("after drag:", h.armor, "| undo entries:", len(hist.done))
print("undo:", hist.undo(), "->", h.armor)
```

The last two lines of output are:

```
after drag: 94 | undo entries: 1
undo: drag armor slider -> 35
```

Sixty events, one undo entry, and undo restores the value from before the drag. The same `History` handles a multi-select edit too: set `armor` on 30 selected enemies inside one transaction and a single undo restores all 30. The lab adds redo and range clamping through the field metadata.

Two design rules follow from transactions.

- **Every edit goes through the history.** If one inspector widget writes to a field directly, that change cannot be undone and may not even be marked as unsaved. Route every write through one function, the way week 13 routed every timing through one scope type.
- **Transactions are also the unit of saving and networking in collaborative editors.** Some editors let several people edit one level at once. What travels between their machines is exactly these `(object, field, old, new)` records, which is one more system reading the same reflection data.

## 5. Data outlives code: renames and versions

Reflection makes it cheap to add fields. It does not make it cheap to change them. A level file written last month contains the name `regen_per_s`. Rename the field to `regen_rate` and the loader no longer finds it. In our Python loader the value silently falls back to the default, 1.5. Every level in the game has now lost its regeneration tuning, and nothing crashed to tell you.

Engines handle this in two ways.

- **Redirects.** A table that maps old names to new ones, applied at load time. Unreal calls these Core Redirects. They are entries in the project's `DefaultEngine.ini` under a `[CoreRedirects]` section, for example a `PropertyRedirects` line with an old name and a new name, and Unreal's documentation describes them as remapping obsolete data while assets load so that renames do not lose data. The lab asks you to implement the same idea in a dozen lines.
- **Versions.** Each saved object records the schema version it was written with. The loader runs a chain of small upgrade functions, version 3 to 4, 4 to 5, until the data matches the current code. Week 12 covers versioned save formats; the editor's level files are the same problem with more data.

Whichever you choose, add a check that fails loudly. A loader that reports "field `regen_per_s` in `forest.level` is not declared on `Health`" at load time turns a silent data loss into a one-line fix. CS102 week 13 made this argument for tables of item stats, and it applies unchanged to every reflected field.

## 6. Debug panels inside the game

Not every tool belongs in the editor. Some questions only make sense while the game runs: why is this enemy stuck, how many draw calls is this room, what does the AI think it sees. For these, engines keep **in-game debug tools**: a console for commands, overlays like Unreal's `stat unit` and Minecraft's debug screen from week 13, and small panels of sliders and checkboxes drawn over the game.

The usual library for those panels in C++ engines is **Dear ImGui**, which its README describes as a "bloat-free" graphical user interface library for C++. It uses the **immediate-mode** style. Instead of building a tree of widget objects that you keep in sync with your data (**retained mode**, the style of most editor UIs), you call a function every frame for each widget, passing it your data directly. If the call `SliderFloat("armor", &armor, 0, 500)` runs this frame, the slider exists this frame. Stop calling it and it is gone. The README argues that this removes state duplication and synchronization, so there is less code and fewer bugs. It also points out that immediate-mode GUI is not the same as immediate-mode rendering; the library produces vertex buffers and a few draw-call batches that your renderer draws.

Immediate mode fits debug panels because they change with the code and nobody but programmers sees them. It fits a full editor less well: large editors need layout, docking, accessibility and undo, which retained widget trees provide. Many teams use both. The editor is retained, and the dozens of little developer panels are immediate. Reflection connects them: a generic debug panel can loop over a component's field descriptors and draw one ImGui widget per field, with the same `F + S` saving as the editor's inspector.

A final judgment call for your own projects: what earns a tool at all? A good rule is to watch where the team loses time. CS102 week 13 gave you the arithmetic for a tuning loop. If designers wait for a programmer to change a number, the number needs an inspector field. If artists re-export the same file ten times to see it in game, the importer needs hot reload (week 7). If testers cannot reproduce a bug, the game needs a console command that sets up the situation. Build the tool where the loop is slowest.

## In-class activity (25 minutes)

Groups of three. Each group gets the component list for a small co-op dungeon game: `Transform` (position, rotation, scale), `Health` (current, maximum, regen), `Spawner` (enemy type, wave count, interval, radius), `Door` (locked, key id, open time), `Loot` (table id, gold min, gold max).

1. Count `F`. Your editor needs an inspector, save, load, undo and network replication. Compute the code sites by hand and reflected. The producer wants a "search by field value" tool next month. How many sites does it add each way?
2. Write the declaration for every field in the style of the Python `prop()`: range, `save`, `edit`, `net`. Decide which fields are runtime-only and which must replicate. Justify one `net=False` decision.
3. A teammate renames `Spawner.interval` to `Spawner.interval_s`. Write the redirect entry you would add, and one sentence on what would have happened to the 40 existing levels without it.
4. Pick one question a tester might ask during play ("why did this door not open?"). Sketch the in-game debug panel that answers it: which fields it shows, and whether it should be generic (loop over descriptors) or hand-written.

Expected output: the counts from step 1, a declaration table, the redirect entry, and the panel sketch with one sentence of justification.

## Common misconceptions

- **"Reflection is a C# or Python feature, so C++ engines can't have it."** Standard C++ gets reflection only with C++26. Engines have built it for decades with descriptor tables, macros or code generators. Unreal's `UPROPERTY` is exactly that.
- **"Reflection makes adding fields free."** Adding is cheap. Renaming and removing still break saved data unless you add redirects or version upgrades.
- **"The editor and the runtime should share all code."** They should share the data model and the runtime systems. Editor-only code (inspectors, gizmos, validation at save time) should be stripped from the shipped game.
- **"Undo means one entry per change."** An editor needs transactions: one entry per user action, however many field writes it contains.
- **"Immediate-mode UI redraws everything with many draw calls, so it is slow."** Dear ImGui's README makes the point directly: immediate mode describes the API, not the rendering, and it outputs batched vertex buffers.

## Check yourself

1. A team has `F = 320` fields and hand-writes five tool systems. It plans to add replication and a diff tool. By how many code sites does the hand-written approach grow, and by how many the reflected one?
2. With `S = 5` hand-written systems and 50 new fields per milestone, what miss rate `q` would keep the expected number of broken fields at or below 1?
3. In the `History` class, a designer drags the armor slider from 35 to 94, releases, then drags it from 94 to 10. How many undo entries exist? What value does each undo restore?
4. A level file contains `{"regen_per_s": 4.0}` and the field was renamed `regen_rate`. What does the section 2 loader produce for `regen_rate`, and why is that worse than a crash?
5. For each, say editor or in-game debug panel, and why: tuning a boss's attack timings; checking which navmesh polygon an agent stands on; setting the light color of a room; toggling collision shapes on and off during a playtest.

<details>
<summary>Answers</summary>

1. By hand, each new system needs a site for every field: `2 × 320 = 640` more. Reflected: 2 more.
2. Expected broken fields `50 × (1 − (1 − q)^5) ≤ 1`, so `(1 − q)^5 ≥ 0.98`, `1 − q ≥ 0.98^(1/5) = 0.99597`, `q ≤ 0.4%`. One slip in 250 edits is a very high standard for a person, which is the practical case for reflection.
3. Two entries, one per drag. The first undo restores 94 (the value before the second drag). The second restores 35.
4. It produces the default, 1.5, because no saved key matches the declared name. It is worse than a crash because nothing reports the loss, so every level quietly loses its tuning until someone notices in play.
5. Boss timings: editor (they are saved content, need undo and review), though a live-tuning panel during play can help find the values. Navmesh polygon: in-game panel (it only exists at run time). Light color: editor (saved, part of the level). Collision shapes: in-game debug toggle (a view, not data).

</details>

## Lab / assignment hook

[Lab 14, a reflected inspector](../labs/lab14.md). You write the tool half of a reflection layer: an inspector that lists editable fields with their ranges, a save and load pair with clamping, unknown-key warnings and rename redirects, a field-by-field diff, and an undo history with transactions and redo. Then you port the descriptor table to your C++ engine and draw a generic debug panel for one component.

## Sources

- Epic Games, "Unreal Engine UProperties" (Unreal Engine 5.8 documentation). `UPROPERTY` specifiers including `EditAnywhere`, `BlueprintReadWrite`, `Replicated`, `Transient`, and the `ClampMin` metadata. https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-uproperties
- Epic Games, "Unreal Header Tool" (Unreal Engine 5.8 documentation). UHT parses C++ headers for UObject metadata and generates code before compilation. https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-header-tool-for-unreal-engine
- Epic Games, "Core Redirects" (Unreal Engine 5.8 documentation). Remapping renamed classes and properties while loading assets; `[CoreRedirects]` in `DefaultEngine.ini`; `PropertyRedirects` syntax. https://dev.epicgames.com/documentation/en-us/unreal-engine/core-redirects-in-unreal-engine
- Unity Technologies, "SerializeField" (Unity 6.6 scripting reference). Unity serializes public fields by default; `[SerializeField]` serializes a private field and makes it editable in the Inspector. https://docs.unity3d.com/ScriptReference/SerializeField.html
- Unity Technologies, "RangeAttribute" and "TooltipAttribute" (Unity 6.6 scripting reference). A range-restricted int or float shown as a slider in the Inspector; a tooltip for a field.
- Godot Engine, "GDScript exported properties" (Godot 4.7 documentation). Exported members are saved with their resource or scene, editable in the property editor, and transferred in RPC calls. https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html
- Godot Engine, "Godot's design philosophy", section "The Godot editor is a Godot game" (Godot 4.7 documentation). The editor runs on the game engine and uses its UI system. https://docs.godotengine.org/en/stable/getting_started/introduction/godot_design_philosophy.html
- Sutter, H., "Trip report: June 2025 ISO C++ standards meeting (Sofia, Bulgaria)" (herbsutter.com, 21 June 2025). P2996 "Reflection for C++26" and related papers voted into draft C++26.
- Cornut, O., Dear ImGui, `docs/README.md` (master branch, accessed September 2026). "Bloat-free" GUI library for C++; the immediate-mode paradigm; outputs vertex buffers and draw-call batches rather than rendering in immediate mode. https://github.com/ocornut/imgui

## Interactive spec: examples/w14-fields-times-systems.html

**The one insight.** Hand-written tool code is a grid of `F × S` separate code sites, and every new field must be added `S` times, so holes (fields missing from a system) appear in proportion to the grid. A reflection layer turns the grid into one declaration per field plus one loop per system, `F + S`, so adding systems or fields barely grows the code.

**Layout.** Two linked views. Desktop: grid on the left (about 60% width), chart on the right. Mobile: grid first, chart below.

- **Grid view.** Rows are fields (`F`), columns are tool systems (`S`). Column headers in order: Inspector, Save, Load, Undo, Network, Diff, Search, Script binding, Validation, Localization (show the first `S`). When `F` is larger than about 40, draw the grid as a dense matrix of small squares with no row labels, and a caption "F rows × S columns".
  - **By hand mode:** each cell is a filled square (one code site). A seeded pseudo-random generator marks each cell as a hole with probability `q`; holes are drawn in the danger color with an outline so they are distinguishable without color. Rows containing at least one hole get a marker at the right edge. Readout: "code sites F×S = N", "fields with a hole: H of F (expected F × (1 − (1 − q)^S) = E)".
  - **Reflected mode:** cells are drawn pale (generated, not written). One solid square per row in an extra leftmost column labeled "Declaration" and one solid square per column in an extra top row labeled "Loop". Holes are not possible in this mode; show "code sites F+S = N".
- **Chart view.** x axis: `F` from 0 to 300. y axis: code sites, linear. Two lines: `F × S` (by hand) and `F + S` (reflected) for the current `S`. A vertical marker at the current `F` with both values labeled. Below, a second small chart: percentage of new fields with a hole, `100 × (1 − (1 − q)^S)`, against `S` from 1 to 10, with the current `S` marked.

**Controls.**
- `F` slider, 1 to 300, default 240 (log-ish steps are fine; must hit 6, 60, 150, 240, 300 exactly).
- `S` slider, 1 to 10, default 5.
- `q` slider, 0 to 10% in steps of 0.5%, default 2%.
- Mode toggle: "By hand" / "Reflected" (default By hand).
- "Add a field" button: increments `F` by 1 and briefly highlights the new row. In by-hand mode, the row's `S` cells appear one by one (skip the animation under `prefers-reduced-motion`), and the counter "edits for this field" shows `S`. In reflected mode it shows 1.
- "Add a system" button: increments `S` by 1 (max 10). Readout "sites added: F" or "sites added: 1".
- "Reseed" button to redraw the random holes.
- All controls keyboard operable; values shown as text.

**Formulas.**
```
by hand sites   = F × S
reflected sites = F + S
p_hole(field)   = 1 − (1 − q)^S
expected holes  = F × p_hole
```

**Readout table** (copyable): F, S, q, by-hand sites, reflected sites, p_hole %, expected holes, actual holes in the current seed.

**Test values.**
- F = 6, S = 5: by hand 30, reflected 11.
- F = 240, S = 5: 1,200 and 245. F = 240, S = 8: 1,920 and 248.
- F = 150, S = 6: 900 and 156; adding a system adds 150 by hand, 1 reflected.
- q = 2%: S = 3 gives 5.9%, S = 5 gives 9.6%, S = 8 gives 14.9%.
- F = 60, S = 5, q = 2%: expected holes 5.8.
- q = 3%, S = 6: 16.7%; F = 40 gives expected 6.7.
- q = 0: no holes in any mode.

**First screen.** By-hand mode with F = 240, S = 5, q = 2%, the grid showing about 23 fields with a hole (expected 240 × 0.0961 = 23.1; the 1,200 cells hold about 24 red holes), and the chart showing the two lines far apart at F = 240. Caption: "240 fields × 5 tools = 1,200 places to forget one. Reflected: 245."
