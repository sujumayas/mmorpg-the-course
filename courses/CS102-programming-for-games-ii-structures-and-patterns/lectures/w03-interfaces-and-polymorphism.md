# CS102 · Week 03 — Interfaces and Polymorphism

**Why this matters:** Your fire spell has to burn grass, char wooden crates, bounce off stone and do something sensible to a material a designer will invent next spring. If the fire code has to know every material by name, every new material means editing the fire code, and the ice code, and the lightning code. Polymorphism lets the fire code say "whatever you are, react to fire" and trust the answer. This week is about when that trust pays off and when it costs more than it saves.

**You will be able to:**
- Define an interface in Python with `typing.Protocol` or an abstract base class, implement it in several classes, and call it without knowing the concrete class.
- Replace an `isinstance` chain with polymorphic dispatch and explain what changed about where the code lives.
- Compute, for an interaction grid of elements and materials, how many existing code units each design must edit when a row or a column is added.
- Choose between polymorphism, a type switch and a data table for a given content plan, and defend the choice.

**Before class:** Nystrom, *Game Programming Patterns* (2014), chapters "Update Method" and "Subclass Sandbox". Python documentation, `typing.Protocol` and PEP 544 ("Protocols: Structural subtyping"), the "Rationale" section.

**Prerequisites from earlier courses:** [CS102 week 1](w01-classes-objects-encapsulation.md) (classes, invariants) and [CS102 week 2](w02-inheritance-vs-composition.md) (subclasses, overriding, the is-a test). The update step of the game loop, from [CS101 week 3](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md). The idea that simple local rules can produce rich emergent play, from [GD102 week 12, emergent behavior from simple rules](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md).

**Interactive:** [w03-reaction-grid.html](../examples/w03-reaction-grid.html). Keep it open during section 2.

---

## 1. One call, many behaviours

### Polymorphism

**Polymorphism** means one piece of code works with objects of different classes, and each object responds in its own way. The calling code is written once. Which method actually runs is decided at run time by the object's class. That decision is called **dynamic dispatch**.

You've already relied on it. In week 2, `GameObject.update` looped over its components and called `c.update(self, dt)`. It never asked whether `c` was a `Mover` or an `Explode`. Each component did its own thing. That loop is polymorphism.

### Interfaces

An **interface** is a named set of methods (and sometimes attributes) that a class promises to provide. It says nothing about how. Code that depends only on the interface can accept any object that keeps the promise.

Python gives you three ways to express one, from loosest to strictest.

**Duck typing.** No declaration at all. If the object has a `react` method, call it. "If it walks like a duck and quacks like a duck." Fast to write, and the mistake shows up only when the missing method is finally called.

**Abstract base class** (`abc.ABC`). A base class that declares methods with `@abstractmethod`. Python refuses to create an instance of any subclass that hasn't implemented them. This is **nominal** typing: a class conforms because it names the base class.

```python
from abc import ABC, abstractmethod

class Reactive(ABC):
    @abstractmethod
    def react(self, element: str) -> str | None: ...

class Stone(Reactive):
    pass

Stone()   # TypeError: Can't instantiate abstract class Stone ...
```

**Protocol** (`typing.Protocol`, Python 3.8 onward, from PEP 544). Declares the shape, and any class with a matching shape conforms, whether or not it names the protocol. This is **structural** typing. The type checker (mypy, pyright, your editor) verifies conformance before you run anything. At run time Python doesn't check it unless you ask.

```python
from typing import Protocol

class Reactive(Protocol):
    name: str
    def react(self, element: str) -> str | None: ...
```

Here is the same idea in the two other languages you'll meet this year:

| Language | How you declare it | How a class conforms | Checked when |
|---|---|---|---|
| Python, `Protocol` | `class Reactive(Protocol)` | by having the methods | type-check time |
| Python, `ABC` | `class Reactive(ABC)` with `@abstractmethod` | by subclassing | object creation |
| C# | `interface IReactive { string? React(string e); }` | `class Grass : IReactive` | compile time |
| GDScript (Godot 4) | no interface keyword; duck typing with `has_method("react")`, or a base class, which can be `@abstract` from Godot 4.5 | by having the method, or by `extends` | run time |

### Liskov, again

Last week you met the is-a test. Its sharper form, the **Liskov substitution principle**, is what makes polymorphism safe: any object that claims the interface must honour its contract, not only its method names. If `react` promises "returns a description or `None`, and never raises for an element it doesn't know", then a `Metal.react` that raises `KeyError` on `"wind"` compiles, passes the protocol check and still breaks the fire code. Write the contract in the docstring, then write a test that runs every class through it. Lab 03 does exactly that.

## 2. Worked example: fire doesn't need to know what it's burning

### The hook

At GDC 2017, Takuhiro Dohta, technical director of *The Legend of Zelda: Breath of the Wild*, described what the team called a "chemistry engine". A physics engine decides how objects move each other. The chemistry engine decides how things change each other's *state*. As reported by VentureBeat from the talk, it runs on three rules:

1. Elements can change the state of materials. Fire sets a tree burning.
2. Elements can change each other's state. Water puts fire out.
3. Materials cannot change each other's state. One tree cannot set another tree on fire by itself; the fire does that.

Players discovered combinations the designers never scripted one by one: a metal sword drawing lightning onto a group of enemies, a fire spreading across dry grass into a camp. How do you build a system where adding a material doesn't mean rewriting fire, and adding an element doesn't mean rewriting every material?

Nintendo hasn't published the engine's code, and this lecture doesn't guess at it. What we can build is a system that obeys those three rules, and then measure the cost of growing it.

### The model

Picture the chemistry as a grid. Rows are materials, columns are elements, and each cell holds a reaction or nothing.

| Material \ Element | fire | water | electric |
|---|---|---|---|
| grass | catches fire and spreads | gets wet | — |
| wood (crate) | burns | put out if burning | — |
| metal (sword) | — | — | conducts, shocks nearby |
| stone (boulder) | — | — | — |

- `E` is the number of elements (columns), here 3.
- `M` is the number of materials (rows), here 4.
- A **code unit** is one function or one class, the thing a programmer opens to make a change.

Every design has to store these 12 cells somewhere. The only question is how to group them into code units. That grouping decides what each future change costs.

**Design A, type switch: group by column.** One function per element, each with an `isinstance` branch per material.

```python
def apply_fire(target):
    if isinstance(target, Grass):
        target.state = "burning"; return "catches fire and spreads"
    elif isinstance(target, Wood):
        target.state = "burning"; return "burns"
    return None

def apply_water(target):
    if isinstance(target, Grass): ...
    elif isinstance(target, Wood): ...
    return None
```

**Design B, polymorphism: group by row.** One class per material, each implementing `react(element)`. The world code calls `react` and never looks at the class.

```python
class Material:
    """Contract: react(element) returns a description or None. Never raises."""
    def __init__(self, name):
        self.name = name
        self.state = "normal"

    def react(self, element):
        return None                     # default: ignore everything


class Grass(Material):
    def react(self, element):
        if element == "fire" and self.state != "wet":
            self.state = "burning"
            return "catches fire and spreads"
        if element == "water":
            self.state = "wet"
            return "gets wet"
        return None


class Wood(Material):
    def react(self, element):
        if element == "fire" and self.state != "wet":
            self.state = "burning"
            return "burns"
        if element == "water" and self.state == "burning":
            self.state = "normal"
            return "is put out"
        return None


class Metal(Material):
    def react(self, element):
        if element == "electric":
            return "conducts, shocks nearby"
        return None


class Stone(Material):
    pass                                # inherits the default: reacts to nothing


def apply(element, targets):
    return [(t.name, t.react(element)) for t in targets]
```

Look at `apply`. It is one line and it will never change, no matter how many materials you add. That's the whole point. Notice too that the three chemistry rules are visible in the structure: elements are arguments passed *to* materials (rule 1), a material's state tracks what elements did to it so water can undo fire (rule 2, in simplified form), and no material class has a method that takes another material (rule 3).

Run it on a world of `[Grass, Wood, Metal, Stone]`:

```
fire     -> grass: catches fire and spreads, crate: burns, sword: None, boulder: None
water    -> grass: gets wet, crate: is put out, sword: None, boulder: None
electric -> grass: None, crate: None, sword: conducts, shocks nearby, boulder: None
```

Order matters because materials hold state. Water the grass first, then apply fire, and the grass returns `None`: wet grass doesn't catch.

**Design C, data table: group by nothing.** Store the grid itself, keyed by `(material, element)`:

```python
REACTIONS = {
    ("grass", "fire"):  ("burning", "catches fire and spreads"),
    ("grass", "water"): ("wet",     "gets wet"),
    ("wood",  "fire"):  ("burning", "burns"),
    ("metal", "electric"): (None,   "conducts, shocks nearby"),
}
```

Code reads the table. New cells are new rows of data, as long as the effect is one the engine already knows how to perform.

### Numbers you can check

Now grow the game. Count **existing code units edited** (the risky part: code someone else wrote and tested) and **new code units** (the safe part).

**Change 1: add a material, Ice, that melts under fire.** One new row, one non-empty cell.

- Design A: open `apply_fire` and add a branch. 1 existing unit edited, 0 new.
- Design B: write `class Ice(Material)`. 0 edited, 1 new.
- Design C: add one table row. 0 code units edited.

**Change 2: add an element, Wind, that fans flames on burning grass and pushes wooden crates.** One new column, two non-empty cells.

- Design A: write `apply_wind`. 0 edited, 1 new.
- Design B: open `Grass` and `Wood` and add a branch to each. 2 edited, 0 new.
- Design C: two table rows, but "fans flames" and "pushes" are new effects the engine can't yet perform, so someone writes that code once.

In general, for a new row with `r` non-empty cells and a new column with `g` non-empty cells:

| Design | New material (row): units edited | New element (column): units edited |
|---|---|---|
| A, type switch | `r` | 0 |
| B, polymorphism with a default | 0 | `g` |
| B′, one abstract method per element (`on_fire`, `on_water`, ...) | 0 | `M` (every class must add the method) |
| C, data table | 0 | 0, if the effects already exist |

Polymorphism doesn't make changes free. It moves the cost from one axis to the other. Design B′ shows how a stricter interface makes the column axis worse: if every element is its own abstract method, adding one forces an edit to every material, even stone.

Now apply a content plan. Over a year, the team adds 20 materials that each react to 2 elements, and 2 new elements that each affect 10 materials.

| Design | Edits from 20 materials | Edits from 2 elements | Total existing-unit edits |
|---|---|---|---|
| A, type switch | 20 × 2 = 40 | 0 | 40 |
| B, polymorphism | 0 | 2 × 10 = 20 | 20 |
| B′, abstract method per element | 0 | 2 × 24 = 48 | 48 |
| C, data table | 0 | 0 (plus code for any new effect) | 0 |

Check B′ by hand: after 20 new materials there are `4 + 20 = 24` material classes, and each of the 2 new elements forces a method into all 24.

Open the interactive now. The grid is the same under every design. What changes is the outline drawn around the cells: columns boxed together for the type switch, rows for polymorphism, nothing for the table. Press "Add material" and "Add element" and watch the counters. The edited units light up in the warning colour. Then load the "content plan" preset and compare the totals. The insight to take away is in the picture: the design doesn't change the grid, it changes which way you cut it, and the cut decides which kind of growth is cheap.

### Cross-game recognition

**Pokémon type chart (Generation VI onward).** Pokémon has 18 regular types, and damage depends on the attacking move's type against the defender's type or types. That's an 18 × 18 grid of effectiveness values, and it's naturally a data table (Design C). Every cell holds one number from a small vocabulary (no effect, half, normal, double). New types have been added across generations: Dark and Steel in Generation II, Fairy in Generation VI. Adding a type means adding a row and a column of numbers, with no new *kind* of effect. When every cell's effect comes from a fixed vocabulary, the table wins.

**Godot 4, the `_process` callback.** Every Godot node can override the virtual method `_process(delta)`. The engine walks the scene tree each frame and calls it on every node that has processing enabled, in tree order unless priorities say otherwise. The engine never asks whether a node is a player, a door or a particle spawner. That's Design B at engine scale. Here the axis that grows is node types (game scripts), and the set of operations (process, physics process, ready, input) is small and stable, so polymorphism is the right cut. Nystrom's Update Method chapter describes the same shape.

**Unity, `MonoBehaviour.Update`.** Unity calls `Update` every frame on each enabled `MonoBehaviour`. The same cut: many script types, one small stable set of callbacks. Unity finds the method by name, which is closer to duck typing than to a declared interface, but the design is the same.

Three systems, one principle stated in the model's terms: decide which axis of your grid will grow, and group code along the other one. Many kinds of things with few operations? Polymorphism. Few kinds with many operations? Type switch. Many of both, with effects from a small vocabulary? Table.

### Design judgment, eyes open

This trade-off is well known in programming language research as the **expression problem**: it is hard to make both new types and new operations cheap to add at once. You can't escape it; you can only choose.

- **Choose polymorphism when content grows by kinds of thing.** Game content usually does. Artists and designers add materials, enemies, items and spells far more often than programmers add fundamentally new operations. That's why the update-method and component shapes you saw above are everywhere.
- **Give the interface a safe default.** Design B's base `react` returns `None`, so stone needs no code and a new element costs only the materials that care. Design B′'s strict per-element methods look tidier and cost more.
- **Keep knowledge in one place.** With the type switch, everything Ice does is spread across every element function it reacts to, written by whoever owns those files. With polymorphism, `Ice` is one file. When a bug report says "ice behaves wrong", which design do you want to open?
- **Watch for `isinstance` chains.** A chain of `isinstance` checks on your own classes is often a missing method. It isn't always wrong: code that sits *outside* a hierarchy (a save-file writer, a debug inspector) may reasonably switch on type rather than push serialization into every game class.
- **Pairwise interactions break single dispatch.** "What happens when a fire arrow hits an ice shield" depends on *two* objects' types. `react` dispatches on one. Double dispatch or a table is the usual answer, and it's one reason games with many pairwise rules (like the Pokémon chart) reach for tables.
- **Don't let polymorphism hide order.** Our grass example depends on whether water arrived before fire. `apply` looks innocent and hides that order entirely. The rules for simultaneous elements need to be written down somewhere, and the interface won't do it for you.

## 3. Polymorphism in everyday game code

### Interfaces for capabilities

The chemistry example had one interface. Real games have several small ones, each describing one capability:

```python
class Damageable(Protocol):
    def take_damage(self, amount: int, source: object) -> int: ...

class Interactable(Protocol):
    def interact(self, actor: object) -> None: ...
```

A sword's hit code accepts any `Damageable`: enemies, destructible crates, the player, a training dummy. A "press E" prompt accepts any `Interactable`: doors, levers, shopkeepers. Keep each interface to one job and a handful of methods, so a class can implement only what it needs. That's the interface version of week 2's advice about components.

This combines well with composition. A `GameObject` can conform to `Damageable` by forwarding to its `Health` component:

```python
class GameObject:
    ...
    def take_damage(self, amount, source):
        h = self.get(Health)
        return h.take_damage(amount) if h else 0
```

Now the sword doesn't care whether the thing it hit is a goblin built from five components or a hand-written `Boss` class. Both are `Damageable`.

### Checking conformance

With `Protocol`, your editor and `mypy` flag a class that is missing a method. If you also want a run-time check, for example when loading content from data files, decorate the protocol with `@runtime_checkable` and use `isinstance(obj, Damageable)`. Be aware that the run-time check only confirms the methods *exist*. It doesn't check their signatures or their behaviour. The contract test from section 1 is still your real safety net.

### When not to use an interface

An interface with one implementation and no plans for a second is just an extra file. Don't create `IPlayerController` because a style guide says every class needs an interface. Wait until you have two concrete classes that some caller wants to treat alike. Then extract the interface from what they actually share.

## In-class activity (25 minutes)

Pairs. Start from the chemistry code in section 2 (it's also `labs/lab03/chemistry.py`).

1. **Design your grid (5 min).** Add one material and one element of your own. Fill in their row and column of the grid on paper, including empty cells.
2. **Predict (5 min).** For Designs A, B and C, predict how many existing units each change edits. Write the numbers down before touching code.
3. **Implement in B (10 min).** Add both to the polymorphic version. Count the files you actually opened.
4. **Compare (5 min).** Did your prediction match? Name the one cell that was hardest to place and say which design would have made it easiest.

Expected output: the extended grid, the predicted and actual edit counts, and a two-sentence verdict on which design suits your extended game.

## Common misconceptions

- **"Polymorphism means inheritance."** Inheritance is one way to get it. Duck typing and protocols give polymorphism with no shared base class at all. `apply` would work with any object that has `name` and `react`.
- **"Polymorphism makes the code easier to extend."** Along one axis. It makes adding kinds of thing cheap and adding operations expensive. The type switch does the reverse.
- **"A `Protocol` checks my objects at run time."** Only the type checker checks it, unless you add `@runtime_checkable`, and even then only method names are checked.
- **"`isinstance` is always a code smell."** It's a smell inside a hierarchy you own, where a method would do. At the boundary of a system (serialization, debugging tools, reading untrusted data) it's often the honest choice.

## Check yourself

1. The grid has 6 materials and 4 elements. You add a material that reacts to 3 elements. How many existing units are edited under Design A, Design B and Design B′?
2. You add an element that affects 5 of the 6 materials. Same question.
3. The content plan changes to 5 new materials (2 reactions each) and 6 new elements (each affecting 4 materials), starting from 4 materials and 3 elements. Compute total existing-unit edits for A, B and B′. Which design wins now, and why did the answer change?
4. A `Shield` class implements `react` but raises `ValueError` for any element it doesn't recognise. The protocol check passes. What goes wrong, and which principle does it violate?
5. Would you use Design A, B or C for a card game with 300 cards and 6 keywords, where each keyword's effect is a small, fixed rule? Justify in one sentence.

<details>
<summary>Answers</summary>

1. A: 3 (one branch in each of the three element functions it reacts to). B: 0 (one new class). B′: 0 (one new class that implements all four methods).
2. A: 0 (one new function). B: 5 (one branch in each affected class). B′: 6 (every material class gets the new abstract method, including the unaffected one).
3. A: `5 × 2 = 10`. B: `6 × 4 = 24`. B′: there are `4 + 5 = 9` material classes, so `6 × 9 = 54`. The type switch wins because this plan grows by operations (elements) more than by kinds (materials). The cheap axis flipped.
4. `apply` calls `react` on every target for every element, so the first unfamiliar element crashes the whole world update. The shield keeps the interface's method names but breaks its contract ("never raises"), which violates the Liskov substitution principle.
5. C, or B with keywords as data: 300 cards is a lot of rows, but if each card is a combination of 6 fixed keyword effects, the cards are data (a table of keywords per card) and only the 6 effects are code.

</details>

## Lab / assignment hook

[Lab 03, the chemistry engine](../labs/lab03.md). You'll get the Design B code, a contract test that every material must pass, and a scenario runner. Add three materials and one element, keep the contract test green, then implement the same additions as a data table (Design C) and write a 300-word comparison with your edit counts.

## Sources

- Minotti, M. (2017). "The Legend of Zelda: Breath of the Wild makes chemistry just as important as physics". VentureBeat, 2 March 2017 (retrieved via the Internet Archive, September 2026). Reports Takuhiro Dohta's GDC 2017 description of the chemistry engine and its three rules.
- Dohta, T., Fujibayashi, H. & Takizawa, S. (2017). "Change and Constant: Breaking Conventions with 'The Legend of Zelda: Breath of the Wild'". Game Developers Conference, San Francisco. GDC Vault session page (retrieved September 2026).
- Wikipedia, "The Legend of Zelda: Breath of the Wild" (retrieved September 2026). Release on 3 March 2017; the chemistry engine defining physical properties of most objects and how they interact.
- Bulbapedia, "Type" (retrieved September 2026). 18 regular types; Dark and Steel added in Generation II, Fairy in Generation VI.
- Godot Engine, class reference for `Node`, method `_process(delta)` (Godot 4.x, `doc/classes/Node.xml` on the master branch, retrieved September 2026). Called each idle frame on nodes with processing enabled; order by `process_priority`, then tree order.
- Godot Engine documentation, "GDScript reference", section "Abstract classes and methods" (Godot 4.5 onward).
- Unity Technologies, Scripting API, `MonoBehaviour.Update` (current documentation, retrieved September 2026). Called every frame if the MonoBehaviour is enabled.
- Levkivskyi, I., Lehtosalo, J. & Langa, Ł. (2017). PEP 544, "Protocols: Structural subtyping (static duck typing)". Python 3.8.
- Nystrom, R. (2014). *Game Programming Patterns*, chapters "Update Method" and "Subclass Sandbox".
- Wadler, P. (1998). "The Expression Problem". Message to the java-genericity mailing list. The name for the trade-off in section 2's design judgment.

## Interactive spec: examples/w03-reaction-grid.html

**Purpose.** Make visible that the element × material grid is the same under every design, that each design only groups the cells differently, and that the grouping decides which additions edit existing code.

**Data.** Elements (columns): fire, water, electric. Materials (rows): grass, wood, metal, stone. Non-empty cells: grass×fire, grass×water, wood×fire, wood×water, metal×electric. Cell text as in the lecture's grid.

**Layout.**

- **Main view: the grid.** Rows labelled with material names, columns with element names. Non-empty cells are filled with a short label; empty cells show a faint dot. Clicking a cell toggles it (keyboard: arrow keys move, Space toggles).
- **Design selector** (segmented control): "A: type switch", "B: polymorphism", "B′: method per element", "C: table". The grid is overlaid with outlines for the code units: A draws one outline per column (label `apply_fire()` etc.); B and B′ draw one outline per row (label `class Grass` etc.); C draws a single outline around the whole grid labelled `REACTIONS table`.
- **Buttons.** "Add material" (prompts for a name, adds an empty row), "Add element" (adds an empty column), "Reset", and preset "Content plan" (see test 4).
- **Counters** next to the grid: "Existing units edited" and "New units", for the most recent change and cumulative since reset. Units counted as edited are outlined in the warning colour for 2 s (static highlight under reduced motion) and listed in text.

**Counting rules (must match exactly).** A change is either adding a row, adding a column, or toggling a cell on.

- Toggle cell (m, e) on in a row or column that already existed at reset or was added earlier: A edits the unit for column e; B edits the unit for row m; B′ edits the unit for row m; C edits 0 code units.
- Add material: A creates 0 new units, and each later toggle in the new row edits that column's existing unit (+1 each). B and B′ create 1 new unit (+1 new), and toggles in the new row edit the new unit, which does not count as an existing-unit edit. C: 0 and 0.
- Add element: A: +1 new unit, toggles in the new column edit the new unit (not counted). B: 0 new, each toggle in the new column edits that row's existing unit (+1 per distinct row). B′: 0 new, and adding the column immediately edits every existing row unit (+M), and toggles add nothing further. C: 0 and 0.

**The one insight the visual must make obvious.** Pressing "Add material" lights up column outlines under A and nothing under B; pressing "Add element" does the reverse; under B′ adding an element lights every row. The grid itself never changes shape between designs.

**Test values.**

1. Design A, add material Ice, toggle ice×fire: existing edited 1, new 0.
2. Design B, same change: existing edited 0, new 1.
3. Design B, add element Wind, toggle grass×wind and wood×wind: existing edited 2, new 0. Under B′: existing edited 4 (all 4 original rows), new 0. Under A: 0 edited, 1 new.
4. "Content plan" preset (start from reset, add 20 materials named M1 to M20 each with fire and water toggled on, then add 2 elements W1 and W2 each toggled on for the first 10 rows in grid order): cumulative existing-unit edits A 40, B 20, B′ 48, C 0.

**Accessibility.** The grid is a real `<table>` with focusable cells and `aria-pressed`; counters are in an `aria-live` region; outlines use colour plus a dashed pattern so they read without colour.
