# CS101 · Week 07 — Engine Intro: Scenes, Nodes and Scripts (Godot)

**Why this matters:** For six weeks you wrote the whole program yourself, including the loop that keeps it running. An engine takes that loop away from you and calls your code instead. If you don't know when it calls your code, and in what order, you will ship bugs that look like "the health bar is a few pixels behind the enemy" and never find them by reading one script.

**You will be able to:**
- Build a small Godot scene from nodes, attach a script, and say which callback (`_ready`, `_process`) runs when.
- Predict the exact order in which Godot calls `_enter_tree`, `_ready` and `_process` for any scene tree you are given.
- Compute the gap, in pixels, that a one-frame update-order lag produces at a given speed and frame rate.
- Choose between three fixes for an ordering bug (reorder, priority, parenting) and justify the choice.

**Before class:** Godot Engine documentation (stable, 4.x), "Getting started", the pages "Nodes and Scenes", "Creating instances" and "Scripting languages". Nystrom, *Game Programming Patterns* (2014), "Update Method", reread the sections on update order and on modifying the object list. Install Godot 4 (standard build, not .NET) before class.

**Prerequisites from earlier courses:** [CS101 week 3, loops and the game loop concept](w03-loops-and-the-game-loop.md) (the `while running:` loop you wrote by hand). [CS101 week 4, functions and decomposition](w04-functions-and-decomposition.md) (one frame split into named calls). [CS101 week 6, dictionaries and item databases](w06-dictionaries-item-databases.md) (you will meet the same "look it up by name" idea in node paths).

**Interactive:** [w07-update-order.html](../examples/w07-update-order.html). Use it during section 3.

---

## 1. What the engine takes off your hands

In week 3 you wrote a loop like this one:

```python
running = True
while running:
    command = read_input()      # 1. listen to the player
    update(command)             # 2. change the world
    draw()                      # 3. show the result
```

Every game has this loop somewhere. An **engine** is a program that already contains it, plus the hard parts around it: opening a window, reading the keyboard and gamepad, drawing images to the screen sixty or more times a second, playing sound, and running physics. You no longer write the loop. You write small pieces of code that the engine calls from inside its loop.

This is the biggest shift in the course, so name it clearly. Before, your program was in charge and called functions when it wanted. Now the engine is in charge and calls *your* functions when *it* wants. Programmers call this **inversion of control**. The functions the engine calls are **callbacks**, because you hand them over and the engine calls you back.

We use **Godot** in this course. It is free and open source (MIT licence), it runs on a school laptop, and it is used for commercial games. The official showcase lists titles such as Brotato, Dome Keeper, Cassette Beasts, Buckshot Roulette and Slay the Spire 2. Everything in this lecture holds for Godot 4.x. Where a detail comes from the documentation, the Sources section says which version.

Godot's own scripting language is **GDScript**. It looks a lot like Python on purpose. Indentation marks blocks, `var` declares a variable, `func` declares a function. You already know most of it. We will keep writing plain Python beside it this week, because Python lets us *simulate* what the engine does and check it with numbers, while GDScript is what you type into the editor.

## 2. Nodes, scenes and scripts

Godot builds every game out of three ideas.

A **node** is one object with one job. It has a name, a type, and a list of child nodes. Godot ships with hundreds of node types. A `Sprite2D` draws an image. A `Camera2D` decides what part of the world is on screen. A `Timer` counts down and tells you when it hits zero. A plain `Node2D` has only a position, rotation and scale, which makes it a good parent for a group of other nodes.

Nodes form a **tree**. Each node has exactly one parent, except the root, which has none. A typical enemy looks like this in the editor's Scene panel:

```
Enemy          (CharacterBody2D)
├── Sprite     (Sprite2D)
├── Hitbox     (CollisionShape2D)
└── HealthBar  (Node2D)
```

A child's position is stored *relative to its parent*. If `HealthBar` has position `(0, -20)`, it always sits 20 pixels above wherever `Enemy` is. Move the parent and every child moves with it, for free. Keep that fact in mind, because it becomes the cleanest fix in section 3.

A **scene** is a tree of nodes saved to a file (a `.tscn` file). The enemy above is a scene. Your level is also a scene, and it contains *instances* of the enemy scene, as many as you like. If you have used Unity, a scene here plays the role of both a Unity scene and a prefab. An instance is like calling a function: the `.tscn` file is the definition, and each instance is one call with its own copy of the data. Change the definition and every instance changes.

A **script** is a code file attached to one node. It *extends* that node's type, which means it inherits everything the node can do and adds your behaviour on top. Here is the whole script for a scrolling enemy:

```gdscript
extends Node2D

@export var speed := 300.0      # pixels per second, editable in the Inspector

func _ready() -> void:
    print(name, " is ready at ", position)

func _process(delta: float) -> void:
    position.x += speed * delta
```

Three things to read carefully:

- `@export` puts `speed` in the Inspector panel, so a designer can change it without touching code. It is the same idea as keeping item stats in a dictionary in week 6: data you tune lives outside the logic.
- `_ready()` is called once, when the node and all its children have entered the running game.
- `_process(delta)` is called once per rendered frame. `delta` is the time since the previous frame, in seconds. At 60 frames per second it is about 0.0167. Multiplying speed by `delta` makes the enemy move 300 pixels per *second* rather than per *frame*. Week 9 is entirely about why that multiplication matters. For today, just copy the habit.

### The callbacks you need this week

| Callback | When Godot calls it | Typical use |
|---|---|---|
| `_enter_tree()` | When the node is added to the running tree, parent before children | Rarely needed in CS101 |
| `_ready()` | Once, after the node *and all its children* are in the tree | Find other nodes, set starting values |
| `_process(delta)` | Every rendered frame | Movement, timers, visuals |
| `_physics_process(delta)` | At a fixed rate, 60 times a second by default | Physics bodies, anything that must be consistent (week 9) |
| `_unhandled_input(event)` | When an input event reaches the node and nothing else used it | Menus, one-off key presses (week 8) |

### Finding other nodes

Scripts often need to talk to other nodes. The simplest way is a **node path** with the `$` shorthand, which looks up a child by name, much like a dictionary lookup:

```gdscript
@onready var sprite: Sprite2D = $Sprite
@onready var bar = $HealthBar
```

`@onready` delays the lookup until `_ready()`, when the children are guaranteed to exist. The other common way is an `@export var target: Node2D`, which lets you drag the node you want onto the script's slot in the Inspector. Both are fine. The `@export` version survives renaming nodes, which the `$` version does not.

## 3. Worked example: who moves first? Tree order and the one-frame lag

### The hook

Celeste (2018) is famous for how tight its controls feel. Its developers later published the game's `Player.cs` on GitHub as a learning resource, with a readme explaining the choices they would and would not change. One choice they defended is that the player's update is one long method, not many small ones spread over files. Their reason, paraphrased, is that a precise platformer's player code must run in a tightly controlled order, and splitting it up makes that order harder to follow. Read the file and you can see the order at work. The player's movement is applied first (`MoveH`, `MoveV`) and the camera update comes about a hundred lines later in the same method, so the camera always reads the position the player has *this* frame.

The same problem shows up in games that get it wrong. You have probably seen a floating name or health bar that trails its character by a few pixels when the character runs, then snaps back when it stops. Nothing is wrong with either script. The two scripts simply run in the wrong order.

### The model

Each frame, Godot calls `_process` on every node in **tree order**. The documentation defines tree order as top to bottom as seen in the editor, also known as **pre-order traversal**: visit a node, then visit each of its children in order, fully, before moving to the next sibling. (A node's `process_priority` can override this. Lower values run first, and nodes with equal priority run in tree order.)

Now suppose node `F` (the follower) copies the position of node `L` (the leader) every frame, and `L` moves at speed `v`.

- If `L` comes before `F` in tree order, `F` copies the position `L` has *this* frame. The gap is 0.
- If `F` comes before `L`, `F` copies the position `L` had at the *end of the previous frame*. `F` is always one frame behind.

With a frame time of `dt = 1 / fps` seconds, one frame of lag is a gap of

```
gap = lag_frames × v × dt = lag_frames × v / fps
```

where `lag_frames` is 0 or 1 for a single follower. If followers are chained (a label follows a health bar that follows an enemy) and each one is updated before the thing it copies, the lags add up: `lag_frames` is the number of links in the chain that run in the wrong order.

Nystrom puts the underlying idea well in the Update Method chapter. The game *looks* simultaneous, but inside it is turn-based, and one full turn is one frame. Whoever moves earlier in the turn is seen by everyone who moves later. Whoever moves later is seen by the earlier ones only on the next turn.

### Code you can run

Here is the model as Python. It builds a tiny tree, walks it in pre-order each frame, and prints the gap.

The code uses two Python tools you haven't written yourself yet. Read them this way for now. A `class` is a template for making objects that carry their own variables (`self.x`) and their own functions (`process`); `Enemy(Node)` means "an Enemy is a Node with a different `process`", the same idea as a Godot script that `extends` a node type. `__init__` runs when an object is made, and `super().__init__(name)` runs the parent template's setup first. `yield` makes `pre_order` hand back nodes one at a time to the `for` loop that calls it, and `yield from` passes along everything a child's walk hands back. CS102 teaches classes properly. You only need to read this code, not write it.

```python
class Node:
    def __init__(self, name, children=()):
        self.name = name
        self.children = list(children)
        self.x = 0.0

    def process(self, dt):
        pass


def pre_order(node):
    """Parent first, then each child in order (Godot's 'tree order')."""
    yield node
    for child in node.children:
        yield from pre_order(child)


class Enemy(Node):
    def process(self, dt):
        self.x += 300 * dt          # 300 px/s to the right


class HealthBar(Node):
    def __init__(self, name, target):
        super().__init__(name)
        self.target = target

    def process(self, dt):
        self.x = self.target.x      # copy whatever the enemy has right now


def run(order_names, frames=3, fps=60):
    enemy = Enemy("Enemy")
    bar = HealthBar("HealthBar", enemy)
    by_name = {"Enemy": enemy, "HealthBar": bar}
    root = Node("Main", [by_name[n] for n in order_names])
    dt = 1 / fps
    for f in range(1, frames + 1):
        for node in pre_order(root):
            node.process(dt)
        print(f"frame {f}: enemy {enemy.x:6.2f}  bar {bar.x:6.2f}  gap {enemy.x - bar.x:5.2f}")

run(["HealthBar", "Enemy"])   # bar listed above the enemy
run(["Enemy", "HealthBar"])   # enemy listed above the bar
```

Output:

```
frame 1: enemy   5.00  bar   0.00  gap  5.00
frame 2: enemy  10.00  bar   5.00  gap  5.00
frame 3: enemy  15.00  bar  10.00  gap  5.00
frame 1: enemy   5.00  bar   5.00  gap  0.00
frame 2: enemy  10.00  bar  10.00  gap  0.00
frame 3: enemy  15.00  bar  15.00  gap  0.00
```

Same two scripts, same speed, same frame rate. Swapping two lines in the Scene panel removes a 5-pixel error.

### Numbers you can check

Take `v = 300` px/s. Use `gap = lag_frames × 300 / fps`.

| Frame rate | Frame time | Gap, 1 frame of lag | Gap, 2 frames of lag (chained) |
|---|---|---|---|
| 30 fps | 33.3 ms | 10.00 px | 20.00 px |
| 60 fps | 16.7 ms | 5.00 px | 10.00 px |
| 144 fps | 6.9 ms | 2.08 px | 4.17 px |

Check the 144 row by hand: `300 / 144 = 2.083`. Two things follow from the table. First, the bug is worst on slow machines, which is where you, testing on a fast desktop, are least likely to see it. Second, the gap depends on speed. A bar on a slow zombie at 40 px/s trails by 0.67 px at 60 fps, which nobody notices. Put the same bar on a dashing boss at 1,200 px/s and it trails by 20 px. Ordering bugs hide until something moves fast.

### A visual you can move

Open the interactive. The left panel is a scene tree with four nodes: `Main`, `Enemy`, `HealthBar` and `NameLabel` (which follows the bar). Use the up and down buttons to reorder them, or press the indent button (⇥) next to `HealthBar` to make it a child of `Enemy`. The presets "Bar before enemy", "Correct order", "Worst chain" and "Parented" jump to the four cases worth comparing. Each node shows the number of its turn this frame. The right panel shows the world. The enemy runs back and forth, the bar and label follow, and a ruler measures each gap in pixels. A speed slider (0 to 1,500 px/s) and a frame-rate selector (30, 60 or 144 fps) feed the formula, and the readout shows `lag_frames`, the predicted gap and the measured gap side by side.

The insight to look for is that the gap depends only on the *numbers in the tree panel*, never on the code. The code is identical in every configuration you can build.

### Cross-game recognition

Every engine has this problem, and each gives you a different tool for it. Learn to see them as the same idea.

- **Unity.** Unity calls `Update` on every script, then `LateUpdate` on every script, each frame. Its documentation says a follow camera should always go in `LateUpdate`, because the objects it tracks may have moved during `Update`. That is our model with two passes instead of one tree walk: everything in the second pass sees everything from the first.
- **Unreal Engine (5.x).** Actors tick in *tick groups* that run in a fixed sequence (`TG_PrePhysics`, `TG_DuringPhysics`, `TG_PostPhysics`, `TG_PostUpdateWork`). For finer control, `AddTickPrerequisiteActor` makes one actor wait to tick until a named other actor has finished. That is a direct statement of "leader before follower".
- **Celeste.** No engine feature at all. The developers wrote the player's movement and camera in one method in the order they wanted, so the order is visible in the source.
- **Godot.** Tree order by default, `process_priority` to override it, and parenting to avoid the copy entirely.

Four toolkits, one rule: *a reader must run after the writer it reads, or it sees the past.*

### Eyes-open design judgment

You have three ways to fix the health bar. They are not equal.

1. **Reorder the tree.** Cheapest. Also fragile. The fix lives in the Scene panel, not the code, so a teammate who drags nodes into a tidier order brings the bug back, and nothing tells them why.
2. **Set `process_priority`.** Give the bar a higher number than the enemy (for example `process_priority = 10`). Now the order is written down and survives reordering. The cost is that priorities are global numbers, and a project with twenty of them becomes its own puzzle. Reserve it for "run after everything else" jobs such as cameras and UI that follows the world.
3. **Make the bar a child of the enemy.** The bar no longer copies anything. Its position is relative to the enemy, so Godot computes its screen position from the enemy's *current* transform when drawing. The gap is zero at every speed and frame rate, and there is no code to get wrong. This is usually the right answer for things that are physically attached.

When is parenting wrong? When the follower must *not* inherit everything. A health bar parented to an enemy also inherits its rotation and scale, so a spinning enemy spins its bar. A camera parented to the player cannot smooth or lead. In those cases copy the position on purpose and control the order with priority. Decide deliberately, and leave a one-line comment saying why the order matters.

### Check yourself (worked example)

1. A camera copies the player's position every frame and is listed above the player in the tree. The player moves at 450 px/s. The game runs at 90 fps. What gap do you see?
2. A label follows a bar, which follows an enemy. The tree order is `Label`, `Enemy`, `Bar`. How many frames of lag does the label have, relative to the enemy?
3. Why would a playtester on a 144 Hz monitor report this bug less often than one on a laptop running at 30 fps?

<details>
<summary>Answers</summary>

1. One frame of lag. `450 / 90 = 5` px.
2. `Enemy` then `Bar` is correct, so the bar has 0 lag. `Label` runs before `Bar`, so the label copies last frame's bar position. Total lag is 1 frame.
3. The gap is `v / fps`. At 144 fps it is about a fifth of the gap at 30 fps (2.08 px against 10 px at 300 px/s), which is much harder to see.

</details>

## 4. Ready runs the other way

Here is the surprise that catches most students in their first Godot week. `_process` runs parent first, but `_ready` runs **children first**. The documentation says it plainly. For groups of nodes, `_ready()` is called in reverse order, starting with the children and moving up to the parents. `_enter_tree()` goes the other way, parent first.

Take this tree:

```
Main
├── Player
│   ├── Sprite
│   └── HealthBar
└── Enemy
```

| Callback | Order | Traversal |
|---|---|---|
| `_enter_tree` | Main, Player, Sprite, HealthBar, Enemy | pre-order |
| `_ready` | Sprite, HealthBar, Player, Enemy, Main | post-order |
| `_process` (every frame) | Main, Player, Sprite, HealthBar, Enemy | pre-order |

In Python, post-order is one line moved:

```python
def post_order(node):
    """Every child first, then the parent (the order of _ready)."""
    for child in node.children:
        yield from post_order(child)
    yield node
```

Why would Godot do this? Because a parent's `_ready` usually wants to *use* its children: read the sprite's size, connect to the timer, set the bar's maximum. Children-first guarantees they are all ready. The consequence is the rule you should memorise: **in `_ready`, it is safe to reach down to your children and unsafe to rely on your parent or siblings being ready.** `Player._ready` can safely touch `Sprite`. `Sprite._ready` cannot safely assume `Player` has finished setting itself up, because it hasn't started yet.

## 5. Scenes as building blocks

A scene can be instanced from code as well as from the editor. This is how you spawn bullets, pickups and enemies:

```gdscript
const Bullet = preload("res://bullet.tscn")

func fire() -> void:
    var b = Bullet.instantiate()      # build a fresh copy of the bullet's tree
    b.position = $Muzzle.global_position
    get_parent().add_child(b)         # it enters the tree now; _ready runs now
```

Three habits save you pain later.

- **One scene, one job.** A bullet scene should work when you open and run it on its own (press F6). If it only works inside the level, it depends on something it shouldn't.
- **Children don't reach up.** A child that calls `get_parent().get_parent().score += 1` breaks the day you move it. Let the child send a *signal* ("I was hit") and let whoever cares connect to it. Signals are Godot's name for the Observer pattern, which [CS102 week 10](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) covers properly. For now, know that `$Timer.timeout.connect(_on_timeout)` means "call my function when the timer fires".
- **Add to a parent that outlives you.** The code above adds the bullet to the gun's parent, not to the gun. If the bullet were a child of the gun, it would move and turn with the gun after firing, and disappear when the gun is freed. That is the parenting rule from section 3 again: children inherit their parent's transform and lifetime.

## In-class activity (25 minutes)

Pairs, one laptop with Godot 4 open.

1. Create a scene `Main` (Node2D) with two children, `Enemy` and `HealthBar`, both `Node2D` with a `Sprite2D` or `ColorRect` under them so you can see them. Put `HealthBar` above `Enemy` in the Scene panel.
2. Attach the enemy script from section 2 (speed 1,200 so the effect is easy to see). Attach a bar script whose `_process` sets `global_position = target.global_position + Vector2(0, -20)`, with `target` as an `@export`.
3. Add `print(Engine.get_process_frames(), " ", name)` to both `_process` functions. Run for one second, stop, and read the log. Confirm the order matches pre-order.
4. Predict the gap at 60 fps with the formula. Measure it: print `target.global_position.x - global_position.x` in the bar's `_process` after the copy, one frame later in the enemy's own `_process`, or draw it. Compare.
5. Apply each of the three fixes in turn. For each, write one line: did the gap go to 0, and what could break it later?

Expected output: a log excerpt showing the order, your predicted and measured gap (about 20 px at 1,200 px/s and 60 fps), and three one-line verdicts.

## Common misconceptions

- **"All nodes update at the same time."** They update one after another within a frame, in tree order. It only *looks* simultaneous because a frame is short.
- **"`_ready` runs top to bottom like everything else."** `_ready` runs children first (post-order). `_process` and `_enter_tree` run parent first.
- **"If the gap is small on my machine, there is no bug."** The gap is `v / fps`. It grows on slower machines and with faster objects. Test with a fast mover and a frame cap.
- **"A scene is a level."** A scene is any saved tree of nodes. A bullet is a scene. A level is a scene that contains instances of other scenes.

## Check yourself

1. Write the `_ready` order and the `_process` order for this tree: `Level` with children `HUD` and `World`; `World` has children `Player` and `Coins`; `Coins` has children `Coin1` and `Coin2`.
2. A minimap marker copies the player's position. It is in a `CanvasLayer` that sits above `World` in the tree. The player sprints at 600 px/s. What gap appears at 60 fps, and which fix would you choose? Say why parenting is not an option here.
3. In `Sprite._ready()`, a student writes `get_parent().max_hp` and gets a value of 0, even though `Player._ready()` sets `max_hp = 100`. Explain what happened, using the traversal order.
4. A bullet scene is added with `add_child(b)` to the gun, and players report bullets curving when they turn. Explain and fix.

<details>
<summary>Answers</summary>

1. `_ready`: HUD, Player, Coin1, Coin2, Coins, World, Level. `_process`: Level, HUD, World, Player, Coins, Coin1, Coin2.
2. The marker is updated before the player, so one frame of lag: `600 / 60 = 10` px on the world scale (scaled down by the minimap's zoom). Parenting is out because the marker lives in a UI layer with its own coordinates, and making it a child of the player would put it in the world. Use `process_priority` to make the marker run after the player, or move the minimap's node below `World`.
3. `_ready` is post-order, so `Sprite._ready` runs before `Player._ready`. At that moment `max_hp` still holds its default of 0. Move the logic into `Player._ready`, where the child is guaranteed ready, or give `max_hp` its value in the variable declaration.
4. The bullet is a child of the gun, so it inherits the gun's transform after it is fired. When the gun turns, every live bullet turns with it. Add the bullet to a node that does not move with the gun, such as the gun's parent or the level.

</details>

## Lab / assignment hook

[Lab 07, a scene tree you can test](../labs/lab07.md). You implement pre-order and post-order traversal in Python, reproduce the callback table from section 4, add `process_priority`, and measure follower gaps across frame rates. Then you rebuild the same scene in Godot and compare its log with your simulator's.

## Sources

- Godot Engine documentation 4.7 (stable), class reference "Node". `_ready()` called in reverse order, children before parents; `_enter_tree()` parent before children; processing in order of `process_priority`, lower first, ties in tree order; tree order defined as pre-order traversal; `_physics_process` at a fixed rate, 60 per second by default. https://docs.godotengine.org/en/stable/classes/class_node.html
- Godot Engine documentation 4.7, "Idle and physics processing". `_process` frequency depends on frame rate; `_physics_process` runs at a fixed rate. https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html
- Godot Engine, "Showcase" page (accessed September 2026). Lists Brotato, Dome Keeper, Cassette Beasts, Buckshot Roulette and Slay the Spire 2 as made with Godot. https://godotengine.org/showcase/
- NoelFB, `Celeste` repository, `Source/Player/Player.cs` and `Source/Player/Readme.md` (file history from March 2019; code from the released game, Celeste, 2018). Movement (`MoveH`, `MoveV`) precedes the camera update in the player's update; the readme's explanation of keeping player code sequential for order of operations. https://github.com/NoelFB/Celeste
- Unity Scripting API, `MonoBehaviour.LateUpdate` (current manual). Called after all `Update` functions; follow cameras belong in `LateUpdate`. https://docs.unity3d.com/ScriptReference/MonoBehaviour.LateUpdate.html
- Epic Games, "Actor Ticking in Unreal Engine" (Unreal Engine 5.8 documentation). Tick groups in order and `AddTickPrerequisiteActor`. https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine
- Nystrom, R. (2014). *Game Programming Patterns*, "Update Method". Update order matters; a frame is one turn. https://gameprogrammingpatterns.com/update-method.html

## Interactive spec: examples/w07-update-order.html

**Purpose.** Make visible that a follower's pixel gap is decided by its position in the update order, not by its code, and that parenting removes the gap entirely.

**Layout.** Two linked panels. Stacked on mobile (tree on top), side by side at 900 px and up.

- **Left: scene tree panel.** A vertical list of nodes drawn as an indented tree: `Main` (root, fixed), and three movable nodes `Enemy`, `HealthBar`, `NameLabel`. Each row shows a turn number badge (1, 2, 3, 4 in pre-order) that updates live. Each movable row has up and down buttons (keyboard focusable, `aria-label` "Move HealthBar up") and an "indent under previous" toggle that makes the node a child of the row above it (only allowed for `HealthBar` under `Enemy` and `NameLabel` under `HealthBar`).
- **Right: world panel.** Canvas 600 × 220 logical px, scaled to fit. Enemy is a 32 × 32 square that moves horizontally between x = 40 and x = 560 at speed `v`, bouncing at the ends. HealthBar is a 40 × 6 bar drawn 20 px above its computed x. NameLabel is a 40 × 10 rounded rectangle drawn 32 px above its computed x. A thin ruler under each follower shows its horizontal gap to the enemy's current x, with the number in px.

**Controls.**
- Speed slider `v`: 0 to 1,500 px/s, step 50, default 300.
- Frame rate selector: 30, 60, 144 fps (simulation dt = 1/fps; the drawing may run at the browser's rate, but the simulation must step with the selected dt, using an accumulator so the logical frame rate is exact).
- Pause/step button: pauses and advances exactly one simulated frame per press, showing the turn order being executed with a highlight moving down the tree rows.
- Preset buttons: "Bar before enemy" (Main, HealthBar, Enemy, NameLabel flat), "Correct order" (Main, Enemy, HealthBar, NameLabel flat), "Worst chain" (Main, NameLabel, HealthBar, Enemy flat), "Parented" (HealthBar child of Enemy, NameLabel child of HealthBar).

**Simulation (per simulated frame).** Walk the tree in pre-order. `Enemy.process`: `x += dir × v × dt`, bounce at ends by flipping `dir` (clamp x into range). `HealthBar.process`: if flat, `bar.x = enemy.x`. `NameLabel.process`: if flat, `label.x = bar.x`. If a node is parented, it does not copy in process. Its drawn x is its parent's drawn x plus local offset 0, computed at draw time from the parent's current x.

**Readouts (exact numbers, copyable).** For each follower: `lag_frames` (count of wrong-order links from the enemy to it, computed from the tree, 0 when parented), predicted gap `lag_frames × v / fps` to 2 decimals, and measured gap `|enemy.x − follower.x|` to 2 decimals (ignore the frame of a bounce, or show "bounce" for that frame).

**Insight the first screen must show.** Load with preset "Bar before enemy", v = 1,200, 60 fps, running. The bar visibly trails by 20.00 px and the readout says so. One click on "Correct order" snaps it to 0.00.

**Test values.**
- v = 300, 60 fps, "Bar before enemy": HealthBar 5.00 px, NameLabel 5.00 px (label copies the bar after the bar updates, lag 1 in total).
- v = 300, 60 fps, "Worst chain": HealthBar 5.00 px, NameLabel 10.00 px.
- v = 300, 144 fps, "Worst chain": HealthBar 2.08 px, NameLabel 4.17 px.
- v = 300, 30 fps, "Bar before enemy": HealthBar 10.00 px.
- Any v and fps, "Parented": 0.00 px for both.

**Accessibility.** All controls reachable by keyboard; the turn-order badges have text equivalents; respect `prefers-reduced-motion` by starting paused with step mode; light and dark themes from the shared tokens.
