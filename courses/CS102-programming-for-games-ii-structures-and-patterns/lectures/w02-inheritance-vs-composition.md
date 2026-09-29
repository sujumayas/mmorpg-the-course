# CS102 · Week 02 — Inheritance vs Composition (the "God Class" Trap)

**Why this matters:** The first class hierarchy you draw for a game looks clean: Entity, then Character and Item, then Player and Enemy. Six months later a designer asks for an exploding barrel that also talks, and the tree has no place for it. The usual fix is to push every feature into the base class until one enormous class does everything. This lecture shows why that happens, measures it, and gives you the alternative most modern engines use.

**You will be able to:**
- Write a subclass that overrides and extends a base class method using `super()`, and state the "is-a" test for when inheritance fits.
- Compute, for a given set of entity types and capabilities, how many capability implementations a single-inheritance tree needs versus a component design, and how many unused fields a god class carries.
- Refactor a god class into a container of components without changing its behaviour.
- Critique a proposed class hierarchy and predict which future entity will break it.

**Before class:** Nystrom, *Game Programming Patterns* (2014), chapter "Component", sections "Motivation" and "The Pattern". West, M. (2007), "Evolve Your Hierarchy" (cowboyprogramming.com), the whole article, about 20 minutes.

**Prerequisites from earlier courses:** [CS102 week 1, classes, objects and encapsulation](w01-classes-objects-encapsulation.md) (constructors, private state, objects owning objects). Godot scenes and nodes from [CS101 week 7](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md). The idea that a system is parts plus relationships, from [GD102 week 1](../../GD102-systems-design-and-game-mechanics/lectures/w01-systems-thinking-parts-relationships-emergence.md).

**Interactive:** [w02-hierarchy-vs-components.html](../examples/w02-hierarchy-vs-components.html). Keep it open during section 2.

---

## 1. Inheritance, and what it promises

### Subclasses

**Inheritance** lets one class (the **subclass** or child) start with everything another class (the **base class** or parent) has, then add or change parts. In Python you name the parent in brackets:

```python
class Entity:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def update(self, dt):
        pass                       # most entities do nothing each frame

    def describe(self):
        return f"{self.name} at ({self.x}, {self.y})"


class Enemy(Entity):
    def __init__(self, name, x, y, speed):
        super().__init__(name, x, y)   # let Entity set up its part
        self.speed = speed

    def update(self, dt):              # override: replace the parent's version
        self.x += self.speed * dt

    def describe(self):                # extend: reuse the parent's version
        return super().describe() + f", speed {self.speed}"
```

Three words to keep straight. A subclass **inherits** every method it doesn't define. It **overrides** a method by defining one with the same name. It **extends** a method by overriding it and calling `super().method(...)` inside, so the parent's work still happens.

### The is-a test

Inheritance makes a promise: anywhere code expects an `Entity`, an `Enemy` will do. The quick check is the **is-a test**. "An enemy is an entity" sounds right. "A crate is a bush" sounds wrong, and if your tree says it, your tree is lying about the game. Keep that sentence in mind. The worked example produces exactly that tree.

A stricter version of the test is the **Liskov substitution principle**: a subclass should work anywhere its parent works, without the caller noticing. If `Entity.update` promises "never moves the entity" and `Enemy.update` moves it, code that relied on the promise breaks. You'll use this principle properly next week when we talk about interfaces.

### Where inheritance works well

Inheritance fits when three things hold. The relationship is a real is-a. The tree is shallow, one or two levels. And the variation is along **one axis**. Godot's own node classes are a good example. `Sprite2D` is a `Node2D`, which is a `CanvasItem`, which is a `Node`, and each level adds one well-defined layer: tree membership, then drawing, then 2D transforms, then a textured sprite. The Godot docs describe their node types as a hierarchy where every node inherits from its parents up to `Node`.

Game entities break the third condition. A goblin varies along many axes at once. Does it render? Collide? Move? Have health? Think? Explode? Those are independent yes/no questions, and a single tree can only branch on one question at a time.

## 2. Worked example: 7,300 object types from 169 parts

### The hook

At GDC 2002, Scott Bilas of Gas Powered Games described the object system behind *Dungeon Siege* (2002). The game had more than 7,300 unique object types, where "type" meant something a designer could place in the editor: monsters, chests, doors, levers, spell effects and so on. His slides show the class tree they started from, and the problems it caused: rearranging the tree was expensive, and features had to be merged or hoisted up the tree in ways that fought clean object-oriented design.

The engine they shipped had no deep tree. It had 21 components written in C++ and 148 components written in the game's scripting language, Skrit. Every one of those 7,300 types was a data description of which components to attach and how to configure them.

Seven thousand three hundred types from 169 parts. A few years later Mick West described the same journey on the *Tony Hawk* games at Neversoft: a hierarchy that grew over three games into what he called "the blob", then a two-year refactor into components. Why does a tree fail at this scale, and why do parts succeed?

### The model

Describe each entity type by its set of **capabilities**, independent features it may or may not have. Use six: Render, Collide, Move, Health, AI, Explode. Call the number of capabilities `k`.

**Combinations.** Each capability is on or off, so there are `2^k` possible capability sets. With `k = 6` that's 64. A design with a few dozen entity types will use only some of them, but you can't predict which.

**Single inheritance.** Each class has one parent, and it gets that parent's capabilities for free. Any capability it has that the parent lacks must be written in that class. Define:

```
written(class)   = capabilities(class) − capabilities(parent)
impl_inherit     = Σ over classes of |written(class)|
```

To be fair to inheritance, choose each parent as well as possible: the existing class with the largest capability set that is a subset of the new class's set.

**God class.** Hoist every capability into one base class so nothing is duplicated. Every object then carries every capability's data, used or not:

```
impl_god        = k                       (each capability written once)
unused_slots    = Σ over types of (k − |capabilities(type)|)
```

**Composition.** Write one component class per capability. An entity is a container holding the components it needs:

```
impl_compose    = number of distinct capabilities used    (at most k)
unused_slots    = 0
```

The question for each design is "how many times did I write the same feature, and how much dead data does each object drag around?"

### Numbers you can check

Eight entity types, the kind any action game has in its first milestone:

| Entity | Render | Collide | Move | Health | AI | Explode |
|---|---|---|---|---|---|---|
| Bush | ✓ | | | | | |
| TriggerZone | | ✓ | | | | |
| Crate | ✓ | ✓ | | ✓ | | |
| Rock (physics) | ✓ | ✓ | ✓ | | | |
| Grenade | ✓ | ✓ | ✓ | | | ✓ |
| Barrel | ✓ | ✓ | | ✓ | | ✓ |
| Turret | ✓ | ✓ | | ✓ | ✓ | |
| Goblin | ✓ | ✓ | ✓ | ✓ | ✓ | |

Build the best single-inheritance tree. Add classes smallest first, each under its largest subset parent:

| Class | Parent | Must write |
|---|---|---|
| Bush | Entity | Render |
| TriggerZone | Entity | Collide |
| Crate | Bush | Collide, Health |
| Rock | Bush | Collide, Move |
| Grenade | Rock | Explode |
| Barrel | Crate | Explode |
| Turret | Crate | AI |
| Goblin | Turret | Move |

Add the right column: 1 + 1 + 2 + 2 + 1 + 1 + 1 + 1 = **10 implementations** for 6 capabilities. Collide is written three times (TriggerZone, Crate, Rock). Move is written twice (Rock, Goblin). Explode is written twice (Grenade, Barrel). Four of the ten are copies.

Now read the Parent column aloud. A crate is a bush. A goblin is a turret. The tree that minimises duplication makes claims the design never meant, and the moment a designer asks for a bush that can burn (Health, but no Collide), the tree has no good place for it.

The god-class alternative writes each feature once. The cost is data: 8 types × 6 capabilities = 48 slots, and 23 of them are unused. The bush carries a health bar, an AI brain and an explosion radius. That's the blob.

Composition writes 6 component classes and has 0 unused slots. Here are the three designs side by side:

| Design | Implementations written | Duplicated | Unused data slots | Classes |
|---|---|---|---|---|
| Single-inheritance tree | 10 | 4 | 0 | 9 (Entity + 8) |
| God class | 6 | 0 | 23 of 48 | 1 |
| Components | 6 | 0 | 0 | 7 (GameObject + 6) |

And the scaling that explains Dungeon Siege:

| Capabilities `k` | Possible sets `2^k` |
|---|---|
| 4 | 16 |
| 6 | 64 |
| 10 | 1,024 |
| 169 | about 7.5 × 10^50 |

With 169 components, the space of possible types is effectively infinite, and the game used 7,300 points in it. No tree could name them. A list of parts per type can.

### The code

The composition version in Python. The container knows nothing about any particular capability:

```python
class Component:
    def update(self, owner, dt):
        pass


class GameObject:
    def __init__(self, name, *components):
        self.name = name
        self._components = {type(c): c for c in components}

    def get(self, kind):
        return self._components.get(kind)      # None if absent

    def update(self, dt):
        for c in self._components.values():
            c.update(self, dt)


class Health(Component):
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self._hp = max_hp

    @property
    def hp(self):
        return self._hp

    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)


class Mover(Component):
    def __init__(self, vx, vy):
        self.vx, self.vy = vx, vy
        self.x = self.y = 0.0

    def update(self, owner, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


class Explode(Component):
    def __init__(self, radius):
        self.radius = radius

    def update(self, owner, dt):
        h = owner.get(Health)
        if h is not None and h.hp == 0:
            print(f"{owner.name} explodes, radius {self.radius}")


barrel  = GameObject("Barrel",  Health(30), Explode(4.0))
grenade = GameObject("Grenade", Mover(8, 0), Explode(3.0))
goblin  = GameObject("Goblin",  Health(50), Mover(2, 0))
```

`Health` is written once and used by the barrel and the goblin. `Explode` is written once and used by the barrel and the grenade, which share no parent. The burning bush the designer asked for is one line: `GameObject("Bush", Render(...), Health(5))`. No class changes.

Notice how `Explode` finds out whether it should fire: it asks its owner for a `Health` component. The grenade has none, so its explosion needs a different trigger (a fuse timer, which lab 02 asks you to add). Components still depend on each other; composition makes those dependencies explicit lookups instead of hidden inheritance.

Open the interactive now. The left view draws the best single-inheritance tree for the entities in the table, with duplicated capabilities in the warning colour. The right view is the component matrix, one row per entity, one column per component. Toggle any cell or press "Add entity type" and watch the two views update. The matrix just gains a row. The tree reshuffles, a parent changes to something that fails the is-a test, and the duplicate count jumps. Press "Hoist to base class" to see the god-class version: one box, with its unused-slot count.

### Cross-game recognition

**Tony Hawk series (Neversoft, early to mid 2000s).** Mick West describes an object hierarchy that grew over three successive games until it matched the blob anti-pattern: heavyweight objects, unnecessary data and functionality, and the same feature duplicated in different branches. The skater class was so large that the team first wrapped it whole as a single "blob component", then broke that apart piece by piece. The refactor took about two years while the team shipped a game a year. His model is ours: the deep tree duplicates (our 4 copies) or hoists (our 23 unused slots), and components remove both.

**Unity (all versions).** Unity's manual describes a GameObject as a container that does little on its own, and whose behaviour comes from the Components attached to it. A cube is a GameObject with a Mesh Filter, a Mesh Renderer and a Box Collider. That's our `GameObject("Cube", Render, Collide)` row, built into the editor.

**Godot 4 (current).** Godot sits deliberately in between. Its node types form an inheritance tree (Sprite2D is a Node2D is a CanvasItem is a Node), because each level adds one layer along one axis, which is where inheritance works. Game objects are then built by **composing** nodes into scenes, and scenes can be nested inside other scenes. The Godot design-philosophy page explicitly says its nodes don't work like components in some other engines, so read "composition" here as "a tree of child nodes", not "a flat list of components". Same principle, different container.

Three codebases, one lesson: use inheritance along a single axis that really is an is-a, and use composition for the many independent features a game object may or may not have.

### Design judgment, eyes open

Composition is the default for game entities in most modern engines. It is not free.

- **Strength: features combine without new classes.** Designers can make new types from data, which is how Dungeon Siege reached 7,300 of them. You'll build that in [week 13, data-driven design](w13-data-driven-design-stats-in-json-and-csv.md).
- **Strength: no dead data.** Each object carries only what it uses, which also matters for memory once you have tens of thousands of objects. [CS201 week 5](../../CS201-game-engine-architecture/lectures/w05-entity-component-system-design.md) takes this further with entity-component-system storage.
- **Cost: components need each other, and the lookups are yours to manage.** `Explode` asks for `Health`. West reports that routing every component lookup through a central manager cost over 5% of CPU time on Tony Hawk, so they let components hold direct pointers to each other. You trade the hidden coupling of inheritance for explicit coupling you must design.
- **Cost: update order becomes a bug source.** If one object updates physics before animation and another does the reverse, they drift out of sync. West names this directly. A tree fixes order by the call chain. With components you must decide and enforce it.
- **Cost: the code is harder to read at first.** A class `Goblin` with all its behaviour in one file is easier to follow than a goblin spread over five components and a data file. For a small game with eight types that will never change, a shallow hierarchy may honestly be the right call.
- **Keep inheritance for one-axis variation.** `Component` itself is a base class, and `Health(Component)` passes the is-a test. Inheritance didn't disappear. It moved to where it fits.

## 3. The god class, from the inside

### How a god class grows

Nobody writes a god class on purpose. It grows through a series of reasonable decisions:

1. `Entity` has position and a draw method. Fine.
2. Enemies and the player both need health. They share `Entity`, so health goes into `Entity`. Crates get health too, harmlessly.
3. Physics objects need velocity. Most entities move, so velocity goes into `Entity`. The trigger zone now has a velocity of zero forever.
4. Enemies need AI, but so does one special NPC who isn't an `Enemy`. Put `ai_state` on `Entity` with a flag `has_ai`.
5. `Entity.update` is now 400 lines of `if self.has_ai`, `if self.can_explode`, `if self.is_pickup`.

Each step saved a day. The total cost is a class that every programmer on the team must understand to change anything, and where every change risks every entity. West's "blob" and Nystrom's opening character, a single class that touches input, physics and graphics at once, are this class.

### Symptoms you can check for

You'll be given code like this in lab 02, and you can diagnose it with numbers:

- **Flag fields.** Booleans like `has_ai`, `can_explode`, `is_pickup` that decide which parts of the class are live. Each flag is a missing component.
- **Unused-field ratio.** For each entity type, count fields it never reads. Above a third, the class is carrying other types' data. Our table gave 23 of 48, almost half.
- **Long `update`.** A method with a branch per entity kind.
- **Shotgun edits.** One design change requires edits spread across the class. Adding "burning" touches health, rendering and AI branches.

### Refactoring, step by step

West's advice about refactoring is practical, and the lab follows it. Don't rewrite. Move one feature at a time, keeping behaviour identical after each step:

1. Write tests that pin down current behaviour (a barrel at 0 HP explodes; a goblin moves 2 units per second).
2. Pick one feature, such as health. Create `Health(Component)` and move the fields and methods into it.
3. Make the god class hold a `Health` and forward to it (`self.hp` becomes `self.health.hp`). Run the tests.
4. Change callers to use the component directly. Run the tests.
5. Repeat for the next feature. When the god class is only forwarding, replace it with `GameObject`.

West calls the intermediate stage an "organised blob": the big class still exists but its work lives in sub-objects. It is a perfectly good place to stop if time runs out.

## In-class activity (25 minutes)

Groups of three. Each group gets one card naming a small game: a tower defence, a farming sim, a 2D platformer or a roguelike.

1. **List entity types (5 min).** Write at least eight entity types your game needs.
2. **List capabilities (5 min).** Name 5 to 7 independent capabilities and fill in the capability table like the one in section 2.
3. **Build the tree (8 min).** Use the smallest-first, largest-subset-parent rule. Count implementations written and duplicates. Find the worst is-a lie in your Parent column.
4. **Break it (7 min).** Pass your table to the next group. They invent one new entity type that fits your game. Count how many existing classes the tree version must change and how many the component version must change.

Expected output: the capability table, the tree with its two counts, the worst is-a lie, and the "new entity" costs from step 4.

## Common misconceptions

- **"Inheritance is how you reuse code."** It's one way, and it ties the reuse to an is-a claim. Composition reuses code without the claim. Our tree reused Collide by claiming a crate is a bush.
- **"Composition means no inheritance."** Component classes inherit from `Component`. Inheritance is fine along one real axis; the trap is using it to combine many independent features.
- **"A god class is just a big class."** Size is a symptom. The disease is many unrelated responsibilities with flags choosing between them. A long class with one job (a parser, say) may be fine.
- **"Multiple inheritance solves it."** Python allows `class Barrel(Crate, Grenade)`, and you can mix capabilities that way. But when two parents share an ancestor you get the "diamond" Nystrom describes, where the rules for which parent's method wins become part of your game's behaviour. With six capabilities you'd still need a class per combination you use.

## Check yourself

1. Add a ninth entity type, **Healer NPC**: Render, Collide, Move, Health, AI. Where does it go in the section 2 tree, and does the implementations count change? (Hint: compare it with an existing type.)
2. Add a tenth, **Burning Bush**: Render, Health. Using the smallest-first rule with this type in the list from the start, which class is its parent and what must it write? Does any existing class's parent change?
3. A god-class design has 12 entity types and 8 capabilities. The types use 3 capabilities each on average. How many unused data slots are there?
4. Your teammate proposes `class FlyingEnemy(Enemy)` and `class ShieldedEnemy(Enemy)`. The designer then asks for a flying shielded enemy. List the options and say which you'd pick.

<details>
<summary>Answers</summary>

1. It has the same set as Goblin (Render, Collide, Move, Health, AI). It goes under Goblin and writes nothing, so the count stays 10. But now "a healer is a goblin" is the is-a claim, which is wrong for the design and will break the moment goblins get a goblin-only feature.
2. Burning Bush has 2 capabilities, so it is placed after the two size-1 types. Its largest subset parent is Bush, so it writes Health. Crate is placed next. Its set (Render, Collide, Health) now contains Burning Bush's set, which is larger than Bush's, so Crate's parent changes to Burning Bush and Crate writes only Collide. The total stays at 10: Collide is still written three times (TriggerZone, Crate, Rock), Move twice, Explode twice. Nothing got cheaper, and now a crate is a burning bush. Adding one type moved an existing class to a new parent, which in a real codebase means every crate changes behaviour when someone edits Burning Bush.
3. Each type has `8 − 3 = 5` unused slots, so `12 × 5 = 60` of 96.
4. (a) `FlyingShieldedEnemy(FlyingEnemy)` and copy the shield code (duplication). (b) Multiple inheritance from both (diamond on `Enemy`). (c) Hoist flying and shields into `Enemy` with flags (the start of a god class). (d) Make `Flying` and `Shield` components and build the new enemy from data. Pick (d). The request shows that "flying" and "shielded" are independent capabilities, and the next request will combine them differently again.

</details>

## Lab / assignment hook

[Lab 02, breaking up the blob](../labs/lab02.md). You'll receive a working 120-line `Entity` god class and a behaviour test suite. Refactor it into `GameObject` plus components one feature at a time, keeping the tests green after every step, then add two new entity types that the original class could not express without new flags. Deliverable: the refactored code, the tests passing at each commit, and a table of unused slots before and after.

## Sources

- Bilas, S. (2002). "A Data-Driven Game Object System". Game Developers Conference, San Jose. Slides: scottbilas.com/files/2002/gdc_san_jose/game_objects_slides.pdf (retrieved via the Internet Archive, September 2026). Dungeon Siege with more than 7,300 unique object types; problems of the class-tree approach; 21 C++ components and 148 Skrit components.
- West, M. (2007). "Evolve Your Hierarchy: Refactoring Game Entities with Components". Cowboy Programming, 5 January 2007 (from his "Inner Product" column). The blob anti-pattern; the Tony Hawk series refactor at Neversoft over two years; the blob component for the skater; component lookups exceeding 5% of CPU; update-order problems.
- Nystrom, R. (2014). *Game Programming Patterns*, chapter "Component". The single-class character that spans input, physics and graphics; the Decoration, Prop and Zone example; the "Deadly Diamond" of multiple inheritance.
- Unity Technologies, Unity Manual, "GameObjects" (current documentation, retrieved September 2026). GameObjects as containers for Components; the cube with Mesh Filter, Mesh Renderer and Box Collider.
- Godot Engine documentation, "Godot's design philosophy", section "Object-oriented design and composition" (stable branch, Godot 4.x, retrieved September 2026). Composing and inheriting scenes; nodes inherit up to `Node`; Sprite2D is a Node2D, a CanvasItem and a Node; nodes "do not work like components in some other game engines".

## Interactive spec: examples/w02-hierarchy-vs-components.html

**Purpose.** Make visible that a single-inheritance tree must duplicate capabilities (or lie about is-a), a god class carries unused data, and a component matrix does neither, and that the gap grows every time a designer adds an entity type.

**Data.** Capabilities `CAPS = [Render, Collide, Move, Health, AI, Explode]`. Initial entities, in this order:

```
Bush {Render}
TriggerZone {Collide}
Crate {Render, Collide, Health}
Rock {Render, Collide, Move}
Goblin {Render, Collide, Move, Health, AI}
Grenade {Render, Collide, Move, Explode}
Barrel {Render, Collide, Health, Explode}
Turret {Render, Collide, Health, AI}
```

**Tree algorithm (must match exactly).** Sort entities by `(|caps|, original index)`. Start with `placed = [Entity {}]`. For each entity in order: candidates are placed classes whose set is a subset of this entity's set; parent is the candidate with the largest set, ties broken by earliest placed. `written = caps − parent.caps`. Append the entity to `placed`. Totals: `impl_inherit = Σ|written|`, `duplicates = impl_inherit − |union of all caps used|`.

**God class.** `unused = Σ (6 − |caps|)`, total slots `6 × n`.

**Layout.** Three linked views; on mobile, tabs.

- **View A, "Inheritance tree".** Node-link tree, root Entity at top. Each node shows the class name and its `written` capabilities as chips. A chip is in the warning colour if that capability is also written in another node (a duplicate). Edges labelled "is a".
- **View B, "Components".** A matrix: rows are entities, columns are the six capabilities, cells are toggles (checkbox styled as a filled square). This is the input for all views.
- **View C, "God class"** (toggle button "Hoist to base class"). One box listing all six capabilities and a bar of `n × 6` small squares, filled for used, hollow for unused.
- **Metrics strip** always visible: `Implementations written: tree X / components Y`, `Duplicates: D`, `God class unused slots: U of T`, `Possible capability sets: 2^6 = 64`.

**Controls.** Toggle any cell in View B. "Add entity type" adds a row with a text name and all cells off. "Remove" on each row. "Reset" restores the initial data. Presets: "Section 2 table" (initial), "Add Healer NPC" (Render, Collide, Move, Health, AI), "Add Burning Bush" (Render, Health).

**The one insight the visual must make obvious.** Adding or editing a row in the matrix changes one row; the tree view reshuffles parents, and duplicates appear in the warning colour, and the god-class bar fills with hollow squares.

**Test values.**

1. Initial data: tree parents Bush→Entity, TriggerZone→Entity, Crate→Bush, Rock→Bush, Grenade→Rock, Barrel→Crate, Turret→Crate, Goblin→Turret. Implementations 10, components 6, duplicates 4, god unused 23 of 48.
2. Add Healer NPC (appended last): parent Goblin, writes nothing. Implementations 10, duplicates 4, god unused 24 of 54.
3. Reset, then add Burning Bush (appended last): Burning Bush→Bush writes Health; Crate→Burning Bush writes Collide. Implementations 10, duplicates 4 (Collide written 3 times, Move 2, Explode 2, the rest once), god unused 27 of 54.
4. Reset, then set every entity to all six capabilities: implementations 6 (Bush writes all six, every other class writes nothing), duplicates 0, god unused 0.

**Accessibility.** Matrix cells are real checkboxes with labels "Goblin: Move"; the tree has a text alternative listing `Class → Parent: writes ...`; no animation beyond a 150 ms fade, disabled under reduced motion.
