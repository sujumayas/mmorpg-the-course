# CS102 · Week 10 — Pattern: Observer and Events

**Why this matters:** A kill in an RPG updates a quest counter, an achievement, a sound, the combat log, a damage meter and a telemetry stream. If the combat code calls each of those by name, every new feature means editing combat, and combat becomes the file nobody dares touch. The Observer pattern lets combat announce "an enemy died" and walk away, so new systems plug in without touching it.

**You will be able to:**
- Implement an event bus with subscribe, unsubscribe and emit in Python, and explain each line.
- Compute the per-second cost of polling versus events for a given frame rate, number of watchers, event rate and listener count, and find the crossover.
- Diagnose the lapsed-listener bug and the modify-while-iterating bug from symptoms, and fix both.
- Decide, for a given feature, whether it should be a direct call, a synchronous event or a queued event, and defend the choice.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "Observer" chapter (free at gameprogrammingpatterns.com). Skim the Godot documentation page "Using signals" (Godot 4.x). Reread your week 9 notes on components.

**Prerequisites from earlier courses:** [CS101 week 4, functions and decomposition](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md) (a function is a value you can pass around; that is all a callback is). [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (you have already connected a Godot signal like `timeout`). From this course, [week 3, interfaces and polymorphism](w03-interfaces-and-polymorphism.md) (a listener is any object that honours a small interface), [week 9, the Component pattern](w09-pattern-component.md) (components that need to talk without holding references to each other) and [week 6, queues and stacks](w06-queues-and-stacks-undo-and-command-buffers.md) (queues, used for deferred events in section 5).

**Interactive:** [w10-poll-vs-push.html](../examples/w10-poll-vs-push.html). Keep it open during section 2.

---

## 1. The problem: one kill, six consequences

Picture the function that runs when a player kills an enemy in a small RPG. Version one looks like this.

```python
def on_enemy_killed(enemy, player):
    quests.record_kill(enemy.kind)
    achievements.record_kill(enemy.kind)
    audio.play("enemy_death", enemy.position)
    ui.combat_log.add(f"{player.name} killed {enemy.name}")
    telemetry.log("kill", enemy.kind, player.id)
    loot.roll(enemy, player)
```

Nothing is wrong with any single line. The trouble is what the function *knows*. It imports six systems. It has to be edited every time someone adds a seventh (a bestiary, a daily challenge, a pet that gains XP from kills). It cannot be tested without building all six. And every one of those systems now breaks combat if it throws an error.

Programmers call this **coupling**. Two pieces of code are coupled when a change in one forces a change in the other. The kill function above is coupled to everything that cares about kills, which in a live MMO grows every patch.

The fix is to flip who knows whom. Instead of combat knowing about quests, quests tell something "let me know when an enemy dies." Combat announces the death to whoever registered and does not care who that is. That flip is the **Observer pattern**. Week 9 listed messages as the third way components talk to each other and left the details for now. This is that option, built properly.

### The vocabulary

- The **subject** (also called the emitter or publisher) is the code where something happens. Here, combat.
- An **observer** (listener, subscriber) is code that wants to react. Quests, achievements, audio.
- An **event** is the announcement: a name plus a small bundle of data, the **payload**. `enemy_killed` with `kind="wolf"` and `killer="p1"`.
- To **subscribe** is to register a function, the **callback**, that the subject will call when the event happens. To **emit** is to announce the event, which calls every subscribed callback.

Nystrom's chapter uses an achievement system as its example. The physics code that notices a hero falling off a bridge should not have to know that an achievement exists for it. Physics announces "this body fell." The achievement system listens and decides. As Nystrom notes, you could delete the whole achievement system and physics would not change a line.

## 2. Worked example: the event bus behind a kill quest

### Hook from a shipped game

World of Warcraft's interface is written in Lua, and players write their own interface addons in the same language. Damage meters, raid timers and quest trackers are all written by people outside Blizzard, yet they react to combat, loot and health changes the instant those happen. The game's combat code has never heard of any of them.

How? Each piece of interface code creates a frame and calls `frame:RegisterEvent("PLAYER_REGEN_DISABLED")` (the player entered combat) or `RegisterEvent("UNIT_HEALTH")`. When the game emits that event, it calls the frame's `OnEvent` handler with the event name and payload. Blizzard's own player frame, in the retail 12.1 client, registers for events such as `PLAYER_ENTER_COMBAT`, `PLAYER_LEVEL_CHANGED` and `PLAYER_UPDATE_RESTING` this way. The generated API documentation that ships with that client lists 1,782 distinct events. That is 1,782 moments where the game says "this happened" without knowing who is listening.

You will build the same thing in about twenty lines of Python.

### The model

An event bus is a dictionary from event names to lists of callbacks.

```
listeners: dict[event_name -> list of callbacks]

subscribe(name, f):   listeners[name].append(f)
emit(name, payload):  for f in listeners[name]: f(payload)
```

- `name` is a string such as `"enemy_killed"`. Name events in the past tense. They report facts, not orders.
- `f` is any callable that accepts the payload.
- `emit` is **synchronous**. It calls each callback immediately, one after another, and returns only when all of them have returned.

Two cost models go with it. If `N` systems each **poll** (check a condition every frame) at `F` frames per second, the work per second is

```
polling cost = F × N           checks per second, whether or not anything happened
```

If events arrive at `E` per second and each has `L` listeners, the work is

```
event cost   = E × L           callback calls per second, zero when nothing happens
```

Events win whenever `E × L < F × N`. The crossover is at `E = F × N / L` events per second.

### The code

```python
from collections import defaultdict


class EventBus:
    def __init__(self):
        self._listeners = defaultdict(list)
        self.calls = 0                      # instrumentation for the cost model

    def subscribe(self, event, callback):
        self._listeners[event].append(callback)

        def unsubscribe():
            self._listeners[event].remove(callback)
        return unsubscribe

    def emit(self, event, **payload):
        for callback in list(self._listeners[event]):   # copy: listeners may unsubscribe
            self.calls += 1
            callback(**payload)
```

Three details matter, and each one answers a bug you would otherwise ship.

1. `subscribe` **returns** an unsubscribe function. Whoever subscribes holds the means to leave. Without it, listeners can never be removed, which is the lapsed-listener bug in section 4.
2. `emit` iterates over `list(...)`, a **copy** of the listener list. A quest that completes on this kill will unsubscribe itself *during* the loop. Removing from a list you are iterating over in Python silently skips the next element. The copy costs a few microseconds and removes a whole class of bugs.
3. The payload is keyword arguments. Listeners name what they need (`kind`, `killer`), so adding a field later (`position`) breaks nothing that ignores it, as long as listeners accept `**rest` or you add the field to all of them. In the lab you will switch to a small dataclass per event, which catches typos earlier.

Now the listeners.

```python
class KillQuest:
    def __init__(self, bus, kind, needed):
        self.kind, self.needed, self.count = kind, needed, 0
        self.bus = bus
        self._unsub = bus.subscribe("enemy_killed", self.on_kill)

    def on_kill(self, kind, killer):
        if kind != self.kind:
            return
        self.count += 1
        if self.count == self.needed:
            self.bus.emit("quest_completed", name=f"Kill {self.needed} x {kind}")
            self._unsub()                   # done listening


class Achievement:
    def __init__(self, bus, kind, needed):
        self.kind, self.needed, self.count, self.unlocked = kind, needed, 0, False
        bus.subscribe("enemy_killed", self.on_kill)

    def on_kill(self, kind, killer):
        if kind == self.kind and not self.unlocked:
            self.count += 1
            if self.count >= self.needed:
                self.unlocked = True
                print(f"Achievement unlocked: {self.needed} x {kind}")


def combat_kill(bus, kind, killer):
    bus.emit("enemy_killed", kind=kind, killer=killer)   # combat knows only the bus
```

Notice that `combat_kill` has one dependency, the bus. The quest does not know about achievements, and neither knows about combat. A listener can itself emit (the quest emits `quest_completed`), so events chain without anyone wiring the chain by hand.

### Numbers you can check

Run a scripted session. The player alternates wolf and boar kills 20 times (40 kills, 20 wolves), then kills 5 more wolves. That is 45 kills, 25 of them wolves. Four listeners are subscribed at the start: the quest (10 wolves), the achievement (25 wolves), a `quest_completed` printer, and a combat-log lambda on `enemy_killed`.

```python
bus = EventBus()
quest = KillQuest(bus, "wolf", 10)
ach = Achievement(bus, "wolf", 25)
bus.subscribe("quest_completed", lambda name: print("Quest done:", name))
log = []
bus.subscribe("enemy_killed", lambda kind, killer: log.append(kind))
for k in ["wolf", "boar"] * 20 + ["wolf"] * 5:
    combat_kill(bus, k, "p1")
print(quest.count, ach.count, ach.unlocked, bus.calls)
```

It prints three lines. The quest's printer shows `Quest done: Kill 10 x wolf` on kill 19, the achievement shows `Achievement unlocked: 25 x wolf` on kill 45, and the last line is `10 25 True 110`. Check the 110 by hand.

| Listener | Subscribed to | Calls | Why |
|---|---|---|---|
| Kill quest | `enemy_killed` | 19 | Wolves are kills 1, 3, 5, ... The 10th wolf is kill 19, then the quest unsubscribes |
| Achievement | `enemy_killed` | 45 | Every kill, it filters by kind itself |
| Combat log | `enemy_killed` | 45 | Every kill |
| Quest-done printer | `quest_completed` | 1 | Emitted once, by the quest |
| **Total** | | **110** | |

Now compare the polling design for a whole play session. Suppose the game polls instead. Every frame, each of `N = 150` quest objectives, achievements and UI widgets checks "did my number change?" At `F = 60` frames per second, that is 9,000 checks per second. Over a 10-minute session it is 36,000 frames × 150 = **5,400,000 checks**. The event design above did 110 calls for 45 kills.

The comparison flips when events are frequent. Keep `F = 60`, `N = 150` and give each event `L = 3` listeners.

| Events per second `E` | Event calls per second `E × L` | Polling checks per second `F × N` | Cheaper |
|---|---|---|---|
| 0.1 (a rare boss kill) | 0.3 | 9,000 | Events |
| 1 (steady questing) | 3 | 9,000 | Events |
| 100 (damage ticks in a raid) | 300 | 9,000 | Events |
| 1,000 | 3,000 | 9,000 | Events |
| 3,000 | 9,000 | 9,000 | Equal (crossover `F × N / L`) |
| 10,000 (every projectile movement) | 30,000 | 9,000 | Polling |

The lesson is not "events are faster." It is that the two costs scale with different things. Polling cost scales with **time** and the number of watchers. Event cost scales with **how much happens** and how many care. Pick events for things that happen rarely relative to the frame rate (kills, level-ups, item pickups, door opens). Pick polling, or a plain loop over a tight array, for things that change every frame for every object (positions). That is why no engine fires a "position changed" event per entity per frame.

### A visual you can move

Open `examples/w10-poll-vs-push.html`. The top view is a strip of frames. Polling draws a bar of the same height on every frame. Events draw a spike only on the frames where something happened, as tall as the listener count. Drag the event-rate slider from "boss kill" to "projectile" and watch the spikes merge into a solid wall that overtakes the polling bar at the crossover. The bottom view is a dependency graph. Click "add a system" in direct-call mode and the combat node turns red, because combat's file must change. In bus mode, only the new node appears.

### Cross-game recognition

The same idea appears under different names. Learn to spot `subscribe`, `emit` and the payload in each.

**Godot 4 signals.** Godot's documentation calls signals "Godot's version of the observer pattern" and links to Nystrom's chapter. You declare `signal health_changed(old_value, new_value)` on a node, emit it with `health_changed.emit(old_health, health)`, and another node subscribes with `player.health_changed.connect(_on_health_changed)`. The declared parameters are the payload. `connect` is `subscribe`, and `disconnect` is the unsubscribe handle. Since Godot 4.0 signals are first-class values, so you pass `timeout` itself, not the string `"timeout"`.

**World of Warcraft UI (retail 12.1).** `frame:RegisterEvent("UNIT_HEALTH")` is `subscribe`. The game's internal emit calls the frame's `OnEvent(self, event, ...)` script. The event name arrives as the first argument, so one handler serves many events, usually with an `if event == ... then` chain. `UnregisterEvent` is the unsubscribe. The design choice to expose events, not internal functions, is what lets thousands of third-party addons exist without Blizzard reviewing their code paths.

**Web browsers (the DOM).** `button.addEventListener("click", handler)` subscribes. The browser emits `click` with an `Event` object as payload. `removeEventListener` unsubscribes, and it needs the *same function object* you added, which is the same reason our `unsubscribe` closure captures `callback`. Every HTML interactive in this program uses this API.

Three platforms, one shape. When you meet a new engine, find three things: how you subscribe, what the payload looks like, and how you unsubscribe. If you cannot find the third, expect leaks.

### Eyes-open design judgment

The Observer pattern trades one kind of clarity for another. Before you reach for it, weigh these.

- **You lose the call stack as documentation.** With direct calls, "what happens when an enemy dies?" is answered by reading one function. With events, the answer is scattered across every file that subscribes. Keep a list of events and their subscribers (the lab asks for one), or add a debug mode that prints each emit and each callback.
- **Synchronous means the emitter pays.** A listener that takes 5 ms runs inside combat's frame. Ten such listeners and your kill costs 50 ms, a visible hitch at 60 fps where a frame lasts 16.7 ms. If a reaction can wait, queue it (section 5).
- **Order is an accident.** Listeners run in subscription order. If the achievement must see the quest's updated count, you now depend on who subscribed first. Either make listeners independent of each other or make the order explicit (priorities).
- **Use a direct call when the emitter needs an answer.** "Can the player afford this?" is a question with a return value and one authority. Events broadcast facts; they do not return results.
- **Use events when one fact has many interested parties** and the emitter should not care who they are. Kills, level-ups, zone changes, currency changes. The MMO304 lecture on [economic telemetry](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) requires every currency change to be logged with a reason code. With an event bus, that ledger is one more listener on `currency_changed`, added without touching any faucet or sink.

## 3. Designing events that age well

An event is a public promise. Once a dozen systems listen to `enemy_killed`, renaming it or removing a field breaks all of them. Treat event definitions with the care of a function signature that other teams call.

**Name facts, in the past tense.** `enemy_killed`, `item_looted`, `door_opened`. A name like `play_death_sound` is a command wearing an event's clothes. It tells you the emitter still knows what should happen next, which is the coupling you were removing.

**Put enough in the payload that listeners do not reach back.** If the achievement needs the enemy's level, include `level` in the payload. Otherwise every listener calls `world.get_enemy(id).level`, and by the time a queued listener runs, the enemy may already be deleted. A payload is a snapshot of the facts at the moment of emission.

**Keep payloads small and plain.** Numbers, strings, IDs. Passing the whole `Enemy` object lets listeners mutate it, and now you have two-way coupling again.

**Prefer one event per fact over one event per consumer.** `enemy_killed` with a `kind` field is better than `wolf_killed`, `boar_killed`, `bandit_killed`. Listeners filter. If filtering becomes a hot spot, add a keyed subscription (`subscribe("enemy_killed", cb, kind="wolf")`) inside the bus, and leave the event name alone.

**Typed events.** In the lab you will replace keyword payloads with frozen dataclasses:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EnemyKilled:
    kind: str
    killer: str
    level: int
```

The bus then keys on the class instead of a string: `bus.subscribe(EnemyKilled, on_kill)` and `bus.emit(EnemyKilled("wolf", "p1", 12))`. A typo in a class name is an error at import time. A typo in a string is a listener that silently never fires.

## 4. The two classic bugs

### Modify while iterating

Delete the `list(...)` copy from `emit` and rerun the session. The quest reaches 10, unsubscribes during the 19th kill, and Python's list iterator moves on by index. Because the quest was at index 0, removing it shifts the achievement into index 0, which the loop has already passed. **The achievement misses kill 19.** At the end it reads 24 wolves, not 25, and never unlocks. Nothing crashes. A player just never gets their achievement, and the bug report says "sometimes."

The copy fixes it. Some buses instead mark removed listeners and sweep them after the loop. Either works. Doing nothing does not.

### The lapsed listener

Every enemy in a zone subscribes to `player_moved` so it can check aggro range. When an enemy dies, its object is removed from the world list. But the bus still holds a reference to its `on_player_moved` method. That reference keeps the dead object alive in memory, and the bus keeps calling it.

Put numbers on it. A zone spawns 1,000 enemies over an hour of play, and none unsubscribe on death. The player moves on every frame, so `player_moved` fires 60 times per second. By the end of the hour the bus makes 60 × 1,000 = **60,000 calls per second** to enemies that no longer exist. Some of those callbacks touch deleted components and throw. The rest just burn time. Frame time creeps up over a session, which is the signature of this bug. The game gets slower the longer you play, and a restart "fixes" it.

Nystrom calls this the **lapsed listener problem**. The cure is ownership. Whoever subscribes must unsubscribe, and the safest place is the same object's cleanup code:

```python
class Enemy:
    def __init__(self, bus):
        self._unsubs = [bus.subscribe("player_moved", self.on_player_moved)]

    def destroy(self):
        for unsub in self._unsubs:
            unsub()
        self._unsubs.clear()
```

Godot handles one common case for you. Its documentation for `Object.connect` notes that if the callable's object is freed, the connection is lost, so a freed enemy stops receiving signals. Python's `weakref.WeakMethod` offers a similar escape. A bus that stores weak references drops listeners whose objects were garbage-collected. Both help, and neither replaces a clear rule about who unsubscribes.

## 5. Synchronous events and queued events

Our `emit` runs every listener now. Sometimes you want "later." An **event queue** stores events and delivers them at a chosen point, for example once per frame after the simulation step. It is the week 6 queue with a dispatch loop:

```python
from collections import deque

class QueuedBus(EventBus):
    def __init__(self):
        super().__init__()
        self.pending = deque()

    def post(self, event, **payload):
        self.pending.append((event, payload))        # O(1), no listener runs yet

    def dispatch(self, budget=None):
        n = 0
        while self.pending and (budget is None or n < budget):
            event, payload = self.pending.popleft()
            self.emit(event, **payload)
            n += 1
```

What a queue buys you:

- **Decoupling in time.** Combat posts and returns immediately. A slow listener no longer stretches the combat step.
- **A budget.** `dispatch(budget=200)` handles at most 200 events per frame and leaves the rest for next frame. Audio systems do this so 50 simultaneous explosions do not play 50 sounds.
- **No re-entrancy.** A listener that posts a new event does not recurse into `emit`. The new event waits its turn.

What it costs:

- **Stale state.** By dispatch time the enemy may be gone. That is why section 3 said to put facts in the payload.
- **Latency.** A queued event is handled up to one frame late, 16.7 ms at 60 fps. Fine for achievements, wrong for "the player pressed block, cancel the incoming hit."
- **Ordering across queues.** Two queues drained in different places can deliver events out of causal order.

A good default is synchronous events for gameplay rules that must resolve within the step, and queued events for presentation (audio, UI, effects) and bookkeeping (telemetry, achievements). CS201 [week 9, input and event systems](../../CS201-game-engine-architecture/syllabus.md) builds an engine-level version with fixed-size ring buffers.

## In-class activity (25 minutes)

Work in pairs. You are designing the event list for a single boss fight in a dungeon.

1. List every consequence of these moments: the boss is pulled, the boss drops below 50% health, a player dies, the boss dies. Aim for at least 12 consequences across the four moments (music change, door locks, loot, lockout timer, achievement, combat log, telemetry and so on).
2. Group the consequences under events. Write each event as a past-tense name plus its payload fields, for example `boss_health_crossed(boss_id, threshold, time_s)`.
3. For each listener, mark it **S** (must run synchronously, inside the step) or **Q** (can be queued). Justify any S in one line.
4. Estimate `E` (events per second) for your busiest event during the fight and compute `E × L` against a polling design with `F = 60` and your number of listeners as `N`.

Expected output: a table of 4 to 8 events with payloads, listeners marked S or Q, and one cost comparison. Two pairs then swap tables and look for a payload field that is missing, forcing a listener to reach back into the world.

## Common misconceptions

- **"Events are asynchronous."** A plain observer is a synchronous function call through a list. The listener runs before `emit` returns. Only a queue makes delivery later.
- **"Events are always faster than polling."** Event cost is `E × L`. For things that change every frame on every object, polling a tight array is cheaper and simpler. The crossover is `E = F × N / L`.
- **"Once I use events, my systems are fully decoupled."** They are decoupled from each other, and all coupled to the event names and payloads. Renaming `enemy_killed` is a breaking change for every listener.
- **"The garbage collector will clean up dead listeners."** Not while the bus holds a strong reference to their bound methods. Unsubscribe on destroy, or use weak references on purpose.

## Check yourself

1. A game runs at 120 fps. It has 80 achievement conditions polled every frame. The event it would replace fires 4 times per second with 5 listeners. Compute both costs per second. At what event rate would polling become cheaper?
2. In the worked session, suppose the achievement subscribes **before** the quest, and `emit` iterates over the live list (no copy). Does the achievement still miss a kill? Trace kill 19.
3. A zone spawns 20 enemies per minute. Each subscribes to `player_moved` and never unsubscribes. The player moves every frame at 60 fps. How many callback calls per second after 30 minutes? After 2 hours?
4. A designer wants "when the player presses the parry button within 100 ms of a hit, cancel the hit." Should the parry reach combat as a synchronous event, a queued event, or a direct call? Why?
5. Rewrite this Godot line as a call on our Python `EventBus`: `player.health_changed.connect(_on_health_changed)`, followed later by `health_changed.emit(90, 75)`.

<details>
<summary>Answers</summary>

1. Polling: `120 × 80 = 9,600` checks per second. Events: `4 × 5 = 20` calls per second. Polling becomes cheaper above `E = 120 × 80 / 5 = 1,920` events per second.
2. The achievement is safe this time, but something else breaks. The list is `[achievement, quest, combat log]`. On kill 19 the loop calls index 0 (achievement) and index 1 (quest), which removes itself. The combat log slides from index 2 to index 1, the loop asks for index 2, finds nothing and stops. **The combat log misses kill 19** and records 44 kills instead of 45. The bug did not go away. It moved to whoever sits after the remover, which is why the copy is the fix and reordering is not.
3. After 30 minutes: 600 lapsed listeners, `60 × 600 = 36,000` calls per second. After 2 hours: 2,400 listeners, `144,000` calls per second.
4. A direct call, or a synchronous event resolved inside the same step. A queued event could be delivered a frame after the hit resolves, which at 60 fps is 16.7 ms out of a 100 ms window, and the hit would already have landed. Parry needs an answer ("was the hit cancelled?"), which is a question with one authority.
5. `bus.subscribe("health_changed", on_health_changed)` and later `bus.emit("health_changed", old_value=90, new_value=75)`. The Godot signal's declared parameters become our keyword payload.

</details>

## Lab / assignment hook

[Lab 10, build and instrument an event bus](../labs/lab10.md). You start from `labs/lab10-starter.py`, which ships a working polling version of a quest and achievement tracker and a buggy event bus. You fix the two classic bugs, move the tracker to typed events, and measure polling against events on a scripted 10-minute session. The lab's event-and-subscriber table is also the first deliverable of the pattern project.

## Sources

- Nystrom, R. (2014). *Game Programming Patterns*, "Observer" chapter. Genever Benning. Free web edition at gameprogrammingpatterns.com/observer.html. The bridge-and-achievement example, the point that observers are synchronous, and the name "lapsed listener problem" are paraphrased from this chapter.
- Godot Engine documentation, "Using signals" (docs for Godot 4.7, stable branch, 2026). Signals described as Godot's version of the observer pattern; `signal health_changed(old_value, new_value)`, `emit()`, `connect()`; signals as first-class values since Godot 4.0. https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html
- Godot Engine class reference, "Object" (Godot 4.7). The `connect()` entry notes that a connection is lost when the callable's object is freed.
- Blizzard Entertainment, World of Warcraft retail interface code, client build 12.1.0.69933 (September 2026), mirrored at github.com/Gethe/wow-ui-source (branch `live`). `PlayerFrame.lua` registers `PLAYER_LEVEL_CHANGED`, `PLAYER_ENTER_COMBAT`, `PLAYER_REGEN_DISABLED` and others with `RegisterEvent`. The count of 1,782 events is the number of distinct `Type = "Event"` entries in `Blizzard_APIDocumentationGenerated` in that build, counted for this lecture.
- MDN Web Docs, "EventTarget: addEventListener() method" and "removeEventListener() method". Removal requires the same listener function that was added.
- Python Software Foundation, *The Python Tutorial*, section 4.2 "for Statements" (Python 3.13). Warns that modifying a collection while iterating over it is tricky and recommends looping over a copy.

## Interactive spec: examples/w10-poll-vs-push.html

**The one insight.** Polling cost is paid every frame whether or not anything happens; event cost is paid only when something happens, once per listener. The two cross at `E = F × N / L`. A second view shows the other win of events: adding a listener does not change the emitter.

**Layout.** Two stacked panels (side by side at 1,000 px and wider). Panel A, "Work per frame", on top. Panel B, "Who depends on whom", below. A readout row sits between them.

**Panel A, work per frame.** A horizontal strip of the last 120 simulated frames (2 s at 60 fps), newest on the right, scrolling left in real time (static, redrawn on change, when `prefers-reduced-motion` is set). Each frame has two thin bars side by side:
- Polling bar, height `N` (constant), neutral colour, solid fill.
- Event bar, height `L × (number of events that landed in that frame)`, accent colour, hatched fill so it differs by pattern as well as colour.
Event arrivals are a Poisson process with rate `E` per second, simulated per frame as `k ~ Poisson(E / F)` using a seeded PRNG (mulberry32, seed 10) so the first screen is identical every load. For `E / F > 50` use the normal approximation `round(max(0, normal(E/F, sqrt(E/F))))`. The y-axis is linear by default with a "log scale" toggle; y-axis max is `max(N, L × p99 of k) × 1.1`.

**Controls.**
- `N` conditions polled: slider 10 to 1,000, default 150.
- `E` events per second: log slider 0.1 to 10,000, default 1. Tick labels at named presets: 0.1 "boss kill", 1 "questing kills", 100 "raid damage ticks", 10,000 "every projectile moved".
- `L` listeners per event: slider 1 to 20, default 3.
- `F` frame rate: segmented control 30 / 60 / 120, default 60.
All keyboard operable; sliders show their value in text next to them.

**Readouts (exact numbers, update live).** "Polling: `F × N` checks/s", "Events: `E × L` calls/s", "Crossover at `E = F × N / L` events/s", and a verdict line "Events are cheaper by a factor of X" or "Polling is cheaper by a factor of X" (X to 1 decimal). Also "10-minute session: polling `600 × F × N` checks vs events `600 × E × L` calls".

**Panel B, dependency graph.** A node "combat" on the left and system nodes on the right: quests, achievements, audio, combat log, telemetry (5 nodes). A toggle "Direct calls | Event bus".
- Direct calls: arrows from combat to each system. Label on combat: "imports 5 systems".
- Event bus: a "bus" node in the middle; combat has one arrow to bus; each system has one arrow to bus. Label on combat: "imports 1 thing".
- Button "Add a system" appends a node (bestiary, daily challenge, pet XP, then "system 9", ...). In direct mode the combat node flashes and gets an outlined badge "file edited: 1 more import" and a counter "combat.py edits: n" increments. In bus mode only the new node and its arrow appear, and the counter does not move.
- Button "Reset".

**Test values (must match exactly).**
- Defaults (`F = 60`, `N = 150`, `L = 3`, `E = 1`): polling 9,000 checks/s; events 3 calls/s; crossover 3,000 events/s; "Events are cheaper by a factor of 3,000.0".
- `E = 3,000`: both 9,000 per second; verdict "Equal".
- `E = 10,000`: events 30,000 calls/s; "Polling is cheaper by a factor of 3.3".
- `F = 120`, `N = 80`, `L = 5`, `E = 4`: polling 9,600; events 20; crossover 1,920 (matches Check yourself question 1).
- 10-minute session at defaults: 5,400,000 checks vs 1,800 calls.

**Accessibility and style.** Use `templates/interactive-tokens.css` inline. Bars differ by fill pattern (solid vs hatched). An `aria-live` region announces the verdict when a slider settles. Works at 390 px wide with no horizontal scroll (Panel A shows 60 frames on narrow screens). Draw everything generically; no game art or logos.
