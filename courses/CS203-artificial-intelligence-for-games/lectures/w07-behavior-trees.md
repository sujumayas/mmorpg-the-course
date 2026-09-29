# CS203 · Week 07 — Behavior Trees

**Why this matters:** Last week's guard had four states and seven transitions, and every new behavior meant asking how it connects to every old one. A behavior tree replaces that web with a ranked list of "try this first" branches, which is why it became the default decision structure in shooters and in the Unreal engine. The catch is that the tree alone does not decide how fast your NPC reacts. The rule for *re-reading* the tree each tick does, and the wrong rule gives you a guard that ignores the player for half a second or never runs away at all.

**You will be able to:**
- Trace a behavior tree tick by tick, giving the status of every visited node and the action the NPC performs.
- Compute the reaction delay and the per-tick node visits of a tree under reactive, memory and hybrid tick rules.
- Build selectors, sequences and decorators in Python and convert a priority-ordered state machine into a tree.
- Critique a tree's ordering and tick rule, and predict the visible bug each choice produces.

**Before class:** Champandard, A. and Dunstan, P., "The Behavior Tree Starter Kit", *Game AI Pro* (2013), chapter 6, sections 6.1 to 6.3 (free at gameaipro.com). Isla, D., "Handling Complexity in the Halo 2 AI", GDC 2005 (free on gamedeveloper.com), the sections on the behavior DAG and on impulses. Millington, *AI for Games* (3rd ed., 2019), chapter 5, the section on behavior trees.

**Prerequisites from earlier courses:** [CS203 week 6, finite state machines](w06-finite-state-machines.md) (the four-state guard, transition growth, commitment). [CS203 week 1](w01-game-ai-vs-academic-ai.md) (the five tests, and the 0.2 s human reaction time). [CS102 week 7, trees](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md) (children, recursion, pre-order traversal). [CS102 week 11, state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md) (hierarchical machines). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (why trees end up in data files that designers edit).

**Interactive:** [`examples/w07-bt-tick-trace.html`](../examples/w07-bt-tick-trace.html). Keep it open during section 2.

---

## 1. From a web of transitions to a list of priorities

Week 6's guard lives in four states: PATROL, CHASE, ATTACK and SEARCH. Now the designer asks for one more behavior. When the guard is badly hurt, it runs for safety. In the state machine, that request touches every state. PATROL, CHASE, ATTACK and SEARCH each need a new row to FLEE, and FLEE needs rows back out. Five states allow up to 5 × 4 = 20 transitions, and each one is a guard condition someone has to write and test.

Look at what the designer actually said, though. It was a priority. "If you are hurt, flee. Otherwise, if you see the player, fight. Otherwise, if you heard something, search. Otherwise, patrol." That is a ranked list, and a behavior tree is a way of writing ranked lists, nested inside each other, so the ranking itself does the job of the transitions.

### The vocabulary

A **behavior tree** is a tree of nodes that the game **ticks**, usually several times a second. A tick starts at the root and walks down, the same pre-order walk you wrote in CS102 week 7. Every node that is visited returns one of three **statuses**:

- **SUCCESS**: I did my job.
- **FAILURE**: I could not do my job.
- **RUNNING**: I am doing my job and need more ticks.

The third status is what makes behavior trees fit games. An action such as "walk to the noise" takes seconds. It returns RUNNING each tick until it arrives.

The nodes come in three kinds.

- **Leaves** do the work. A **condition** reads the world and returns SUCCESS or FAILURE, never RUNNING ("do I see the player?"). An **action** changes the world or the NPC and may return RUNNING ("shoot", "walk to the noise").
- **Composites** have several children and decide which of them to tick. There are two you will use constantly. A **selector** ticks its children in order and stops at the first one that does *not* fail. It means "try these, best first". A **sequence** ticks its children in order and stops at the first one that does *not* succeed. It means "do these, in order, and give up if a step fails".
- **Decorators** have one child and change its result or when it runs. An **inverter** swaps SUCCESS and FAILURE. A **cooldown** refuses to run its child for a few seconds after it last ran. A **repeat** runs its child a fixed number of times.

The facts that leaves read live in a **blackboard**, a dictionary of named values ("sees", "hurt", "last noise position") that sensors write and the tree reads. Keeping them in one place means the tree never computes a line-of-sight test itself. Week 10 builds the sensors.

Read a tree aloud this way. A selector is "or", and a sequence is "and then". The guard above reads like this.

```
Selector                         try in order:
├─ Sequence  "flee"                hurt?            and then RunToSafety
├─ Sequence  "fight"               sees enemy?      and then
│   └─ Selector "engage"             ( in range? and then Shoot )  or  Chase
├─ Sequence  "search"              heard noise?     and then GoToNoise, LookAround
└─ Action    Patrol                otherwise patrol
```

Adding FLEE was one line at the top. Nothing else changed. That is the whole selling point, and it is real. It is also where the trouble starts, because "the first child that does not fail" hides a question. On the next tick, do you start again from the top, or do you carry on with whatever was RUNNING?

## 2. Worked example: same tree, three guards

### The hook

Halo 2 (Bungie, 2004) is where many developers first saw a behavior tree ship at scale. In his GDC 2005 talk, Damian Isla describes Halo 2's combat AI as a tree of roughly 50 behaviors (he calls it a behavior DAG, because some subtrees are shared). Most of its decisions use a prioritized list of children, where, in his words, "the first one that can run, does". Players remember what that produced. Kill the leader of a group and the smaller enemies around it can break and run. Isla lists this as a specific behavior, fleeing because the leader died, and he triggers it with an event instead of checking for it every tick.

Here is the surprising part. The priority list alone does not produce that instant reaction. You can build a tree with exactly the right priorities, flee above fight above search above patrol, and still ship a guard that keeps patrolling for half a second after it sees you, or one that stands and shoots at 5% health because it never looks at the flee branch again. The tree is identical in each case. Only the tick rule differs.

### The model

A tick rule answers one question for each composite. When a child returned RUNNING last tick, where does this tick start?

- **Reactive.** Every composite starts from its first child on every tick. Higher priorities are always re-checked. A sequence also re-runs its earlier steps.
- **Memory.** Every composite resumes at the child that was RUNNING. Nothing before it is looked at again until the running child finishes.
- **Hybrid.** Selectors are reactive, so higher priorities are always re-checked. Sequences resume at the running step, but they still re-check every *condition* before it. Finished *actions* are skipped.

One more rule applies in all three. When a composite switches to a different child than the one that was RUNNING, it **aborts** the old one. The old action is told to stop and forgets its progress. Champandard and Dunstan call a selector that re-checks and aborts like this an *active selector*.

Here is the whole tree in Python, using the reactive rule. The `finish` method does the aborting.

```python
SUCCESS, FAILURE, RUNNING = "success", "failure", "running"

class Condition:
    def __init__(self, key):
        self.key = key
    def tick(self, bb):
        return SUCCESS if bb[self.key] else FAILURE
    def halt(self):
        pass

class Action:
    def __init__(self, name, ticks=0):          # ticks=0: runs until stopped
        self.name, self.ticks, self.done = name, ticks, 0
    def tick(self, bb):
        bb["acted"] = self.name
        self.done += 1
        if self.ticks and self.done >= self.ticks:
            self.done = 0
            return SUCCESS
        return RUNNING
    def halt(self):
        self.done = 0

class Composite:
    def __init__(self, *children):
        self.children, self.running = list(children), None
    def halt(self):
        for c in self.children:
            c.halt()
        self.running = None
    def finish(self, i, status):                # abort the branch we left
        if self.running is not None and self.running != i:
            self.children[self.running].halt()
        self.running = i if status == RUNNING else None
        return status

class Selector(Composite):                      # "try these in priority order"
    def tick(self, bb):
        for i, child in enumerate(self.children):
            status = child.tick(bb)
            if status != FAILURE:
                return self.finish(i, status)
        return self.finish(None, FAILURE)

class Sequence(Composite):                      # "do these in order"
    def tick(self, bb):
        for i, child in enumerate(self.children):
            status = child.tick(bb)
            if status != SUCCESS:
                return self.finish(i, status)
        return self.finish(None, SUCCESS)

guard = Selector(
    Sequence(Condition("hurt"), Action("RunToSafety", 3)),
    Sequence(Condition("sees"),
             Selector(Sequence(Condition("in_range"), Action("Shoot")),
                      Action("Chase"))),
    Sequence(Condition("noise"), Action("GoToNoise", 2), Action("LookAround", 2)),
    Action("Patrol", 4),
)

TIMELINE = {"noise": {2, 3, 4, 5, 6}, "sees": {5, 6, 7, 8},
            "in_range": {7, 8}, "hurt": {9, 10, 11}}
trace = []
for t in range(12):
    bb = {fact: t in ticks for fact, ticks in TIMELINE.items()}
    guard.tick(bb)
    trace.append(bb["acted"])
print(trace[:6])
print(trace[6:])
```

Output:

```
['Patrol', 'Patrol', 'GoToNoise', 'LookAround', 'GoToNoise', 'Chase']
['Chase', 'Shoot', 'Shoot', 'RunToSafety', 'RunToSafety', 'RunToSafety']
```

`TIMELINE` is a scripted encounter. The tree ticks 5 times a second, a rate the Starter Kit mentions as common because it spreads the cost of many NPCs across frames, so 12 ticks cover 2.4 seconds. The guard hears a noise at tick 2, sees the player at tick 5, gets in range at tick 7, and is badly hurt from tick 9. Action durations are in ticks: a patrol leg takes 4, walking to the noise 2, looking around 2, running to safety 3. Shoot and Chase run until something interrupts them.

### Numbers you can check

The same tree and the same timeline under the three tick rules. A dash in the world columns means the fact is false. The last column counts node visits (every `tick` call on any node, root included) under the reactive rule.

| Tick | noise | sees | in range | hurt | Reactive | Memory | Hybrid | Visits (reactive) |
|---|---|---|---|---|---|---|---|---|
| 0 | — | — | — | — | Patrol | Patrol | Patrol | 8 |
| 1 | — | — | — | — | Patrol | Patrol | Patrol | 8 |
| 2 | yes | — | — | — | GoToNoise | Patrol | GoToNoise | 8 |
| 3 | yes | — | — | — | LookAround | Patrol | LookAround | 9 |
| 4 | yes | — | — | — | **GoToNoise** | GoToNoise | LookAround | 8 |
| 5 | yes | yes | — | — | Chase | LookAround | Chase | 9 |
| 6 | yes | yes | — | — | Chase | LookAround | Chase | 9 |
| 7 | — | yes | yes | — | Shoot | Shoot | Shoot | 9 |
| 8 | — | yes | yes | — | Shoot | Shoot | Shoot | 9 |
| 9 | — | — | — | yes | RunToSafety | **Shoot** | RunToSafety | 4 |
| 10 | — | — | — | yes | RunToSafety | **Shoot** | RunToSafety | 4 |
| 11 | — | — | — | yes | RunToSafety | **Shoot** | RunToSafety | 4 |

Totals over the 12 ticks: reactive 89 visits, memory 58, hybrid 89.

Check a few rows by hand before you trust the table.

**Tick 0, reactive, 8 visits.** Root (1). The flee sequence (2) ticks "hurt?" (3), which fails, so the sequence fails. The fight sequence (4) ticks "sees?" (5), fails. The search sequence (6) ticks "heard noise?" (7), fails. Patrol (8) returns RUNNING, so the root returns RUNNING.

**Tick 3, reactive.** The search sequence starts over. GoToNoise is on its second tick, so it returns SUCCESS, and the sequence moves straight on to LookAround in the same tick, which returns RUNNING. Nine visits, one more than tick 0.

**Tick 4, reactive, the stutter.** The sequence starts over again. GoToNoise finished last tick and reset its counter, so it runs again from scratch and returns RUNNING. The sequence stops there and aborts LookAround. On screen, the guard glances around for one tick and then walks back to the noise it already reached. A reactive *sequence* repeats finished steps.

**Ticks 5 and 6, memory, the late reaction.** The root selector resumes the search branch, which is RUNNING, and never ticks the fight branch above it. The guard is looking around while the player stands in plain view. LookAround finishes on tick 6, so the root finally starts from the top on tick 7 and the guard reacts then. That is 2 ticks, 0.4 seconds at 5 Hz. Week 1 set about 0.2 s as the fastest a human reacts. This guard is twice as slow as that, for no reason the player can see.

**Ticks 9 to 11, memory, the guard that never flees.** Shoot never finishes; it runs until interrupted. Under the memory rule nothing interrupts it, because nothing above it is ever re-checked. The guard stands and fights to the death with the flee branch sitting unused at the top of its tree. Priorities only mean something if someone looks at them.

**Hybrid.** Reacts at tick 5 like the reactive rule, and at tick 4 it skips the finished GoToNoise and finishes LookAround instead of stuttering. It flees at tick 9. This is the behavior the designer asked for.

Now the price. The memory rule made 58 visits, the other two 89. Memory is cheaper because it skips everything above the running branch. That is exactly why it misses the player. Reactivity costs visits, and at 100 guards ticking 5 times a second, 89 against 58 over 12 ticks is the difference between about 3,700 and 2,400 visits per second. That gap is small in this tree and large in Halo 2's 50-behavior one.

### Move it yourself

Open [the interactive](../examples/w07-bt-tick-trace.html). The left view draws the tree and lights up every node visited on the current tick, colored by the status it returned. The right view is the 12-tick timeline from the table, with one row per tick rule, and the world-fact rows above it. Step through the ticks with the slider and switch the tick rule. Then click cells in the world rows to change the encounter. Move "sees" earlier and watch the memory guard's reaction delay readout grow, because the player now appears in the middle of a patrol leg. Make "hurt" last only one tick and watch the reactive guard flee for exactly one tick and then turn back to shoot.

### Cross-game recognition

**Halo 2 (Bungie, 2004).** Isla's tree is a priority list, and most of his talk is about how to keep it reactive without paying for it. Two of his tools map straight onto this lecture. **Behavior tags** are bit flags ("in a vehicle", "alert") that switch whole branches off, so a tick never visits children that cannot apply. **Stimulus behaviors** are branches inserted into the tree by an event handler at the moment something happens, such as the leader dying, instead of being checked on every tick. Rewritten in our terms, a stimulus behavior is a reactive check that costs nothing until its event fires.

**Unreal Engine behavior trees (Unreal Engine 5, current documentation).** Epic's documentation lists how its trees differ from "traditional" ones. They are event-driven, so they avoid re-walking the tree every frame. Conditions are not leaves but **decorators** attached to a branch. A decorator can be set to **abort** the running branch when the blackboard value it watches changes. That is our hybrid rule, delivered by events. The selector re-checks higher priorities only when a watched value changes, so the tree pays the memory rule's visit cost and gets the reactive rule's response.

**Final Fantasy XV (Square Enix, 2016).** Miyake and colleagues describe the game's "AI Graph", which nests state machines and behavior trees inside each other. A designer can put a behavior tree inside a state and a state machine inside a tree node. In our terms, the state machine holds the slow, stable choices (which mode is the character in) and the tree handles ordered steps inside each mode. This is the answer to the question week 6 left open. You do not have to choose between the two structures.

Three engines, one principle. The tree's order encodes priority, and the tick rule, or the events that replace it, decides whether a change in the world reaches that priority in time.

### Eyes-open design judgment

- **Reactive is the safe default for selectors.** A guard that ignores the player looks broken. A guard that visits a few extra nodes costs a fraction of a millisecond. Start reactive and optimize with events or tags when profiling tells you to.
- **Memory is right for some sequences.** A reload, a door-opening animation or a three-step combo should finish once started. If a sequence's steps are expensive or visible, give it memory, and put the conditions that must interrupt it in a place that is always re-checked.
- **Watch actions that never finish.** Shoot and Chase return RUNNING forever. Under any rule that does not re-check priorities, a never-finishing action locks the tree. Give such actions a timeout, or make sure a reactive selector sits above them.
- **Reactivity is also flicker.** Make "hurt" true for one tick and the reactive guard flees for one tick, then turns back. Week 6's commitment lock applies to trees too. A cooldown decorator or a "flee for at least 3 ticks once started" sequence with memory fixes it.
- **The tick rate is part of the design.** At 5 Hz, a perfectly reactive tree still responds up to 0.2 s after a change, because the change can arrive just after a tick. That happens to match human reaction time, which is often what you want. Ticking at 60 Hz would make the guard react faster than any player can, and cost 12 times as much.

## 3. Decorators, parallels and conditions that watch

A selector and a sequence are enough to write most trees. Three more pieces cover most of the rest.

**Decorators** wrap one child. Beyond the inverter, the ones you will use most are these:

- **Cooldown**: fail at once if the child ran less than *T* seconds ago. It is the simplest way to stop a grenade throw or a taunt from repeating every tick. Isla describes Halo 2 grenade throws being disallowed for a while after the last successful one.
- **Repeat *n***: run the child *n* times, succeeding on the last. The Starter Kit's example guard fires three times this way.
- **Timeout**: fail the child if it has been RUNNING longer than *T*. It is a cure for actions that never finish.
- **Force success**: always return SUCCESS, so an optional step ("shout a warning") cannot break its sequence.

**Parallels** tick several children on the same tick and combine their results with a policy, such as "succeed when all succeed, fail when any fails". They are not about threads. Their main job is watching. One child keeps checking a condition while the other acts, and the parallel stops the action when the condition fails. The Starter Kit calls this pattern a **monitor**. Unreal replaces most parallels with decorators that abort.

**Guard conditions at the front of a sequence** are how most trees encode "only while". The hybrid rule re-checks them every tick, which is why the hybrid guard stops fighting the moment "sees" turns false. Under the memory rule they are checked once, when the sequence starts, and then forgotten. When a tree misbehaves, the first question to ask is "when was this condition last checked?"

### Converting a state machine

You can turn any priority-driven state machine into a tree mechanically.

1. List the states in priority order, highest first: the state that should win when several could apply.
2. For each state, write a sequence: the conditions that let you enter it, then the action it performs.
3. Put the sequences under one selector in that order. The lowest-priority state, the one with no entry condition, goes last as a bare action.

Week 6's guard becomes the tree in section 1 minus the flee branch. What you lose is anything that depended on *which state you came from*. "Go to SEARCH only if you were chasing" has no direct translation, because a selector has no memory of its last choice. You write that history into the blackboard instead ("last_seen_time") and test it with a condition. That is usually an improvement, since the fact is now visible and testable, but it is a change you must make on purpose.

## 4. Where trees go wrong

**Order is the design.** Swap the search and fight branches, so "heard noise?" is checked before "sees enemy?". Under the hybrid rule, at ticks 5 and 6 of our encounter the guard keeps looking around the noise while the player stands in view, because a noise that is still ringing outranks a visible enemy. Nothing is broken in the code. The priorities are wrong. Most behavior tree bugs are ordering bugs, and you find them by asking "what should win when both are true?" for every pair of neighboring branches.

**Deep trees hide their state.** A 50-behavior tree may be eight levels deep. When an NPC does something odd, you need to know which node is running and why its higher-priority siblings failed. Every production tree tool draws the tree with the running path lit up, as the interactive does. Final Fantasy XV's AI Graph tool highlights active nodes as the game runs. Budget time for that tool. Without it you are guessing.

**Priorities are fixed.** A selector always prefers its first child when it can run. Real priorities shift. Grabbing a health pack should outrank fighting when you are at 20% and the pack is close, but not when you are at 60% or the pack is across the map. You can fake that with more conditions and duplicated branches, and Halo 2 used **impulses** to move a behavior up the list under specific conditions. When you find yourself writing many of those, you want scores instead of an order. That is next week's utility AI.

**Trees do not plan.** A tree does what its author wrote, in the order written. If the right sequence of actions depends on the situation (reload first, or take cover first, or fetch ammo), you either write a branch for each case or let the NPC work the order out. Week 9's planner does the second.

## In-class activity (25 minutes)

Pairs. Each pair gets a printout of the guard tree, the 12-tick world timeline and a blank trace grid.

1. **Trace (10 min).** One partner traces ticks 0 to 6 under the memory rule, the other under the hybrid rule. Write the action and the visit count for each tick. Swap and check each other against the table in section 2.
2. **Break it (8 min).** Invent a new 12-tick world timeline on which the *reactive* guard does something that looks wrong but the hybrid guard does not. Write one sentence saying what the player would see.
3. **Add a behavior (7 min).** The designer wants the guard to call for help once when it first sees the player, then fight. Add it to the tree. Decide where it goes, which decorator stops it repeating, and whether its sequence needs memory. Trace ticks 5 to 8 with your change.

Expected output: two trace grids, one timeline with its one-sentence bug, and a modified tree diagram with a 4-tick trace.

## Common misconceptions

- **"A behavior tree is re-evaluated from the top every tick, so it is always reactive."** Only under the reactive rule. Many implementations resume the running branch, and then higher priorities are not seen until it finishes. Check what your engine does before you trust a priority.
- **"A selector is an if/else."** An if/else picks once. A selector also handles RUNNING. It remembers which child is running and, depending on the rule, may abort it when a higher child becomes possible. The abort is where most of the behavior comes from.
- **"Behavior trees replace state machines."** They organize the same decisions differently. Shipped games mix them, as Final Fantasy XV does, and a sequence with memory is a small state machine.
- **"More reactive is always better."** Reactivity makes an NPC respond to one-tick flickers in its inputs. A guard that flees for one tick and turns back looks as broken as one that never flees.

## Check yourself

1. Under the reactive rule, how many node visits does the guard's tree make on tick 7 of the encounter? List them in order.
2. Change the timeline so that "hurt" is true on tick 6 only, everything else unchanged. What does each of the three guards do on ticks 6 and 7? Which one would you ship?
3. At 5 Hz, the memory guard reacted to the player 2 ticks late. Move the start of "sees" to tick 1, while the guard is on its first patrol leg. How late is the memory guard now, in ticks and seconds? (Patrol legs take 4 ticks and start at tick 0.)
4. Swap the fight and search branches. Under the hybrid rule, what does the guard do on ticks 5 and 6? Explain in one sentence why this is an ordering bug and not a tick-rule bug.
5. A designer says "our trees are too slow, switch every composite to the memory rule." Using the section 2 numbers, give the saving and the two visible bugs it would ship.

<details>
<summary>Answers</summary>

1. Nine: root, flee sequence, "hurt?" (fails), fight sequence, "sees?" (succeeds), engage selector, shoot sequence, "in range?" (succeeds), Shoot (RUNNING).
2. Reactive: RunToSafety on tick 6, then on tick 7 "hurt?" fails, the root aborts RunToSafety and the guard shoots. Hybrid: the same, because selectors are reactive in both. Memory: the root resumes the running search branch on tick 6 (LookAround) and never checks "hurt?", then shoots on tick 7. Reactive and hybrid flee for one tick and turn back, which looks indecisive. Memory never flees. None is right as it stands. Ship hybrid with a commitment rule on fleeing, for example a sequence with memory that runs RunToSafety to completion once it starts.
3. The patrol leg runs ticks 0 to 3 and succeeds on tick 3. The root starts from the top on tick 4 and finds "sees?" true. The guard reacts on tick 4, 3 ticks late, 0.6 s. The delay depends on where in a long action the change arrives, which is why memory-rule reaction times feel random to players.
4. It runs GoToNoise and LookAround on ticks 5 and 6 while the player is in view, and starts shooting on tick 7 once the noise fact has cleared. The code does exactly what the tree says. The tree says a noise matters more than a visible enemy, which is the wrong priority.
5. 58 visits instead of 89 over the 12 ticks, about 35% fewer. The guard reacts to the player 0.4 s late (ticks 5 and 6) and never flees (ticks 9 to 11). A better saving is to keep reactive selectors and add events or tags, as Halo 2 and Unreal do.

</details>

## Lab / assignment hook

[Lab 07, a behavior tree you can trace](../labs/lab07.md). You write `Selector`, `Sequence` and `Inverter` so that one tree runs under all three tick rules, reproduce this lecture's trace table and visit counts, then extend the guard with a "call for help" branch and a cooldown and defend your placement with a trace. The tests in `test_bt.py` fail on the starter and pass when you are done.

## Sources

- Isla, D. (2005). "Handling Complexity in the Halo 2 AI." Game Developers Conference 2005, published on Gamasutra (now gamedeveloper.com), March 11, 2005. Halo 2 (Bungie, 2004). The behavior DAG of roughly 50 behaviors; prioritized-list selection ("the first one that can run, does"); impulses; behavior tags as bit vectors; stimulus behaviors added to the tree by an event handler, with fleeing after the leader's death as the example; grenade throws disallowed for a time after a successful one. https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai
- Champandard, A. J. and Dunstan, P. (2013). "The Behavior Tree Starter Kit." In S. Rabin (ed.), *Game AI Pro*, chapter 6. CRC Press. Free at gameaipro.com. The three statuses; sequences, selectors, decorators, filters, parallels and monitors; active selectors that re-check higher priorities and abort the running branch; the example guard that fires three times; many games update trees every other frame or at 5 Hz; first- and second-generation trees, with Bulletstorm's event-driven version as an example.
- Epic Games. "Behavior Tree in Unreal Engine: Overview." Unreal Engine 5 documentation (page read September 2026, engine version 5.8). Event-driven trees; conditionals as decorators; observer aborts; simple parallel; services; blackboard. https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview
- Miyake, Y. et al. (2017). "A Character Decision-Making System for FINAL FANTASY XV by Combining Behavior Trees and State Machines." In S. Rabin (ed.), *Game AI Pro 3*, chapter 11. CRC Press. Free at gameaipro.com. The AI Graph that nests state machines and behavior trees in either direction; the debugger that highlights active nodes at run time.
- Francis, A. (2017). "Overcoming Pitfalls in Behavior Tree Design." In S. Rabin (ed.), *Game AI Pro 3*, chapter 9. Background on Isla's four features and on keeping trees maintainable.
- Rabin, S. (2017). "The Illusion of Intelligence." *Game AI Pro 3*, chapter 1. Human reaction times of about 0.2 s, via [CS203 week 1](w01-game-ai-vs-academic-ai.md).
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapter 5, behavior trees.
- The guard tree, the 12-tick encounter, the action durations and all trace numbers are invented for teaching and computed with the code in this lecture and in `labs/lab07-starter/bt.py`.

## Interactive spec: examples/w07-bt-tick-trace.html

**The one insight:** the same behavior tree produces three different guards depending only on the tick rule. The memory guard ignores the player for 2 ticks and never flees; the reactive guard stutters back to a finished step; the hybrid guard does what the designer meant. Seeing the three timeline rows diverge under identical world facts, with the tree view lighting up which nodes were even looked at, is the moment the lesson lands.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (tree on top).

- **Left, "Tree":** the guard tree drawn top-down with generic rounded boxes. Composite nodes show a symbol and a word: selector "? Selector", sequence "→ Sequence". Conditions are ellipses with a question ("hurt?"), actions are rectangles with the action name and a small progress counter "done/ticks" (or "∞" for Shoot and Chase). On the current tick, every visited node gets a status badge (S, F or R, plus color from the palette: success green, failure red, running amber). Unvisited nodes are dimmed to 40% opacity. Status must never be shown by color alone; always show the letter.
- **Right, "Timeline":** a grid with 12 columns (ticks 0 to 11) and a column header showing seconds at the chosen tick rate. Four world-fact rows (noise, sees, in range, hurt) with filled cells where true. Below them three result rows, Reactive, Memory, Hybrid, each cell showing the action's abbreviation (Pat, GoN, Look, Cha, Sho, Run). Cells where a guard's action is judged wrong are outlined with a dashed border and a tooltip: a sequence re-running a finished step ("stutter"), a lower-priority action running while a higher-priority condition is true ("ignoring"). The current tick column is highlighted in all rows.
- **Readouts** under the timeline, one line per rule: "reacts to sees after N ticks (X s)", "flees after N ticks (X s)" or "never flees", "visits: N total".

**Controls (keyboard accessible, labelled):**

1. Tick slider 0 to 11, plus Prev and Next buttons and Play/Pause (1 tick per second).
2. Radio group "Tree view shows": Reactive, Memory, Hybrid (default Memory, to match the first screen). The tree view shows that rule's state at the current tick. The timeline always shows all three.
3. The world-fact cells are toggle buttons (Space or Enter toggles, arrow keys move between cells). Changing a cell recomputes all three rows from tick 0.
4. Tick rate select: 5 Hz (default) or 10 Hz. It only changes the seconds labels and readouts (seconds = ticks / rate).
5. Reset button restores the lecture's timeline.

**Formulas.** Implement exactly the classes in `labs/lab07-starter/bt.py` with the reference solution: `Condition`, `Action(name, ticks)` where `ticks = 0` means never finishes, `Composite.finish(i, status)` aborting the previously running child when `i` differs, `Selector` and `Sequence` with modes. Mode rules: reactive, both composites start at child 0 every tick. Memory, both resume at `running` when it is not null. Hybrid, selectors start at 0; sequences resume at `running` but still tick any Condition child with index below `running`, skipping only non-Condition children. A visit is one call to any node's `tick`, root included. Each rule gets its own fresh tree built at tick 0. Tree: Selector[ Sequence[hurt?, RunToSafety(3)], Sequence[sees?, Selector[ Sequence[in range?, Shoot(0)], Chase(0) ]], Sequence[heard noise?, GoToNoise(2), LookAround(2)], Patrol(4) ]. "Reacts to sees" is the first tick at or after the first "sees" tick on which the action is Chase or Shoot, minus the first "sees" tick. "Flees" is the same with RunToSafety and "hurt".

**Test values (must match).** Default timeline: noise on ticks 2 to 6, sees 5 to 8, in range 7 to 8, hurt 9 to 11.

- Reactive actions: Patrol, Patrol, GoToNoise, LookAround, GoToNoise, Chase, Chase, Shoot, Shoot, RunToSafety, RunToSafety, RunToSafety. Visits per tick 8, 8, 8, 9, 8, 9, 9, 9, 9, 4, 4, 4; total 89. Reacts after 0 ticks; flees after 0 ticks.
- Memory actions: Patrol ×4, GoToNoise, LookAround, LookAround, Shoot ×5. Visits per tick 8, 2, 2, 2, 8, 4, 3, 9, 5, 5, 5, 5; total 58. Reacts after 2 ticks (0.4 s at 5 Hz); never flees.
- Hybrid actions: Patrol, Patrol, GoToNoise, LookAround, LookAround, Chase, Chase, Shoot, Shoot, RunToSafety ×3. Total 89. Reacts after 0; flees after 0.
- Timeline with hurt on tick 6 only: reactive and hybrid show RunToSafety on tick 6 and Shoot on tick 7, then Patrol on ticks 9 to 11; memory shows LookAround on tick 6 and Shoot on ticks 7 to 11.
- Timeline with sees starting at tick 1 (sees ticks 1 to 8, all else default): memory reacts after 3 ticks (0.6 s).

**First screen.** Default timeline, tick slider at 5, tree view on Memory, so the student first sees the memory guard's tree with the fight branch dimmed (never visited) while "sees" is filled in the timeline and the Memory row shows LookAround. Caption: "Same tree, same world. The memory guard never looks at the fight branch."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces the current tick and each rule's action ("Tick 5. Reactive Chase, Memory LookAround, Hybrid Chase."). Respect `prefers-reduced-motion` (Play steps without animated transitions) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art; generic shapes only.
