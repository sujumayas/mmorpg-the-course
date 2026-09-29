# CS102 · Week 11 — Pattern: State and State Machine

**Why this matters:** Most "impossible" gameplay bugs are a character in two states at once: jumping while ducking, attacking while stunned, climbing while swimming. They come from tracking state with a handful of booleans that can combine in ways nobody intended. A state machine makes the illegal combinations impossible to write down, and it turns "what can happen next?" into a table you can read.

**You will be able to:**
- Count the representable and valid states of a flag-based design and compute how many illegal states it allows.
- Implement a table-driven finite state machine in Python with enter, exit and update behaviour per state.
- Trace a frame-stepped state machine with guards, a countdown timer and a memory of the previous state, and predict every transition it makes.
- Choose between a flat machine, a hierarchical machine, a pushdown machine and concurrent machines for a given character, and justify the choice by state counts.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "State" chapter. Skim the landing code in the Super Mario 64 decompilation (n64decomp `sm64`, `src/game/mario_actions_moving.c`, the `LandingAction` table near the top and `common_landing_cancels`). You do not need to read C fluently; look for the numbers 4, 5 and 20. Reread your CS101 week 11 notes.

**Prerequisites from earlier courses:** [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) (menu, play, pause, game over, with enter and exit actions, and Pac-Man's ghost modes traced with dictionaries; this week moves to a character's machine with guards, a timer and a memory of where it came from, then scales up to hierarchical, pushdown and concurrent machines). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (fixed steps and timers that count down). From this course, [week 3, interfaces and polymorphism](w03-interfaces-and-polymorphism.md) (used for state objects in section 4), [week 6, queues and stacks](w06-queues-and-stacks-undo-and-command-buffers.md) (the pushdown automaton) and [week 10, Observer and events](w10-observer-and-events.md) (events are the inputs that drive transitions).

**Interactive:** [w11-triple-jump-window.html](../examples/w11-triple-jump-window.html). Keep it open during section 2.

---

## 1. Four booleans, sixteen worlds

Nystrom's State chapter starts with a platformer heroine. She can stand, jump, duck and dive (a ground-pound from the air). The first version of her code grows one boolean per feature.

```python
class Heroine:
    def __init__(self):
        self.on_ground = True
        self.is_jumping = False
        self.is_ducking = False
        self.is_diving = False

    def handle_input(self, button):
        if button == "B" and self.on_ground and not self.is_jumping:
            self.is_jumping, self.on_ground = True, False
        elif button == "DOWN_PRESS":
            if self.on_ground:
                self.is_ducking = True
            else:
                self.is_diving = True
        elif button == "DOWN_RELEASE":
            self.is_ducking = False
```

Play-test it and bugs appear one at a time, each fixed with another condition. Press B while ducking and she jumps with `is_ducking` still true, so she flies through the air in the ducking pose. Press DOWN while jumping and she dives, but `is_jumping` stays true alongside `is_diving`. When landing code later clears only `is_jumping`, she stands on the ground still flagged as diving, and every system that reads `is_diving` (the ground-pound damage, the dive sound) keeps firing. Every fix adds a clause, and every clause is a new place to forget one of the other flags.

The root cause is arithmetic. Four booleans can hold `2^4 = 16` combinations. The heroine has **4** real states. So the code can represent **12 states that should never exist**, and every one of those is a bug waiting for the right input sequence.

| Flags `n` | Combinations `2^n` | Valid states (one per flag, as here) | Illegal but representable |
|---|---|---|---|
| 2 | 4 | 2 | 2 |
| 4 | 16 | 4 | 12 |
| 6 | 64 | 6 | 58 |
| 8 | 256 | 8 | 248 |
| 10 | 1,024 | 10 | 1,014 |

Real characters are not always one-hot (some flag pairs really can combine), but the shape holds. Flags grow the representable space exponentially while the valid space grows roughly linearly. Your job as the programmer is to make the representable space equal the valid space. A single variable `state` that holds exactly one of `"standing"`, `"jumping"`, `"ducking"`, `"diving"` does precisely that. There is no value of it that means "ducking and jumping."

### The model: a finite state machine

A **finite state machine** (FSM) has four parts.

- A finite set of **states** `S`. The machine is in exactly one at a time.
- A **start state** `s0`.
- A set of **inputs** (also called events or triggers), such as button presses, timers expiring, or the week 10 events like `enemy_killed`.
- A **transition function** `next = δ(state, input)`. For each state and input, it names the next state, or says "ignore this input."

The transition function is a table. Here is the heroine's.

| State \ Input | `B` | `DOWN_PRESS` | `DOWN_RELEASE` | `LANDED` |
|---|---|---|---|---|
| standing | jumping | ducking | — | — |
| jumping | — | diving | — | standing |
| ducking | — | — | standing | — |
| diving | — | — | — | standing |

A dash means "stay where you are and ignore the input." Now every bug from above is visibly impossible. B while ducking is a dash, so she stays ducking. B while diving is a dash. There is no cell that leads to a fifth state. When a designer asks "can she jump out of a duck?", you point at one cell and change it deliberately.

## 2. Worked example: the triple jump that comes out as a hop

### Hook from a shipped game

In Super Mario 64 (Nintendo, 1996), three jumps pressed in rhythm give a single jump, a higher double jump and a somersaulting triple jump. Every player also knows the failure. You press A for the third jump and Mario does a plain small hop. Sometimes you were a little late. Sometimes your timing was fine and Mario was not running fast enough. The game gives no hint which one it was, and players argue about it.

The community decompilation of the game (the n64decomp `sm64` project, which rebuilds the original ROM from C source) answers it. Mario's behaviour lives in one variable, `m->action`. The three jumps are separate actions, `ACT_JUMP`, `ACT_DOUBLE_JUMP` and `ACT_TRIPLE_JUMP`, and each has its own landing action. Three details decide which jump a press produces.

- The landings `ACT_JUMP_LAND` and `ACT_DOUBLE_JUMP_LAND` each last 4 frames. On every one of those frames the game writes 5 into a countdown, `m->doubleJumpTimer`. The triple-jump landing writes 0 and discards A presses.
- The countdown drops by 1 each frame. A press after the landing has finished still continues the chain while the countdown is above 0. Which jump comes out depends on which landing Mario came from. The code decides with a `switch` on `m->prevAction`, the action before the current one.
- The triple jump also needs forward speed above 20, in the game's internal units. At 20 or less, the third press gives `ACT_JUMP`, the hop. (With the Wing Cap, the speed check is skipped.)

So the hop has two causes: a countdown that ran out, or a speed guard that failed. That is a state machine with three features CS101's ghost machine did not need all at once: **guards** (conditions checked before a transition), a **timer that belongs to the state**, and a **memory of the previous state**. [CS101 week 11](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) traced Pac-Man's ghosts with a dictionary. This week you build a character's machine as a class and count its timing window frame by frame.

### The model

We keep the decompilation's numbers and drop everything that does not affect the chain: steep floors, quicksand, carrying objects, the Wing Cap, wall kicks and walking off after a landing. What is left is a teaching model of the rules, not the game's code.

```
states:   grounded, jump, jump_land, double_jump, double_jump_land,
          triple_jump, triple_jump_land
input:    A pressed this frame (true or false), once per frame
memory:   timer      frames left to continue the chain   (m->doubleJumpTimer)
          prev_land  the landing Mario settled from      (m->prevAction, reduced)
          speed      forward speed, held constant here    (m->forwardVel)

δ(grounded, A)          = double_jump   if timer > 0 and prev_land = jump_land
                        = triple_jump   if timer > 0 and prev_land = double_jump_land
                                           and speed > 20
                        = jump          otherwise
δ(jump_land, A)         = double_jump
δ(double_jump_land, A)  = triple_jump if speed > 20, else jump
δ(triple_jump_land, A)  = ignored
δ(any landing, 4th frame)   = grounded, and prev_land becomes that landing
δ(any jump, touchdown)      = its landing

every frame:        if timer > 0, timer = timer - 1; then run the current action
every landing frame: timer = 5 (0 for triple_jump_land)
```

- `A` is edge-triggered: true only on the frame the button goes down. Holding it does nothing more.
- The airtimes of 20, 24 and 30 frames for the three jumps are invented. In the game, airtime comes from physics. Here it only decides where on the timeline each landing falls.

Two rules come from the game's frame loop, and both change the counts. First, the countdown ticks down **before** any action runs, because the decrement sits in `update_mario_inputs`, which `execute_mario_action` calls before the action handlers. Second, when a handler switches action, the loop runs the new action's handler **in the same frame**. The handler returns true to mean "I changed action, run again." So the frame on which a landing ends is also the first frame of `grounded`, and an A press on that frame still counts.

### The code

```python
LAND_FRAMES = 4       # frames Mario spends in jump_land or double_jump_land
CHAIN_FRAMES = {"jump_land": 5, "double_jump_land": 5, "triple_jump_land": 0}
TRIPLE_SPEED = 20.0   # forward speed must be strictly greater
AIR_FRAMES = {"jump": 20, "double_jump": 24, "triple_jump": 30}   # invented
LANDS_AS = {"jump": "jump_land", "double_jump": "double_jump_land",
            "triple_jump": "triple_jump_land"}


class Mario:
    def __init__(self, speed):
        self.speed = speed
        self.action = "grounded"
        self.prev_land = None   # the landing Mario settled from
        self.timer = 0          # frames left to continue the chain
        self.count = 0          # frames spent in the current action
        self.frame = 0
        self.log = []           # (frame, from, to)

    def fast_enough(self):
        return self.speed > TRIPLE_SPEED

    def set_action(self, new):
        self.log.append((self.frame, self.action, new))
        self.action, self.count = new, 0
        return True             # run the new action's handler this frame

    def grounded(self, a):
        if not a:
            return False
        chained = self.timer > 0
        self.timer = 0
        if chained and self.prev_land == "jump_land":
            return self.set_action("double_jump")
        if chained and self.prev_land == "double_jump_land" and self.fast_enough():
            return self.set_action("triple_jump")
        return self.set_action("jump")

    def airborne(self, a):
        if self.count == AIR_FRAMES[self.action]:
            self.set_action(LANDS_AS[self.action])
            return False        # touchdown ends the frame
        self.count += 1
        return False

    def landing(self, a):
        self.timer = CHAIN_FRAMES[self.action]
        self.count += 1
        if self.count >= LAND_FRAMES:
            self.prev_land = self.action
            return self.set_action("grounded")
        if a and self.action == "jump_land":
            return self.set_action("double_jump")
        if a and self.action == "double_jump_land":
            return self.set_action("triple_jump" if self.fast_enough() else "jump")
        return False            # triple_jump_land ignores A

    def step(self, a):
        if self.timer > 0:
            self.timer -= 1     # counts down before any handler runs
        for _ in range(4):      # rerun until no handler switches action
            if self.action == "grounded":
                again = self.grounded(a)
            elif self.action in AIR_FRAMES:
                again = self.airborne(a)
            else:
                again = self.landing(a)
            if not again:
                break
        self.frame += 1


def run(delays, speed, frames=240):
    """Press A on frame 0, then delays[i] frames after the (i+1)-th touchdown."""
    m, pressed, next_press = Mario(speed), 0, 0
    for f in range(frames):
        m.step(f == next_press)
        touched_down = m.log and m.log[-1][0] == f and m.log[-1][2].endswith("_land")
        if touched_down and pressed < len(delays):
            next_press = f + delays[pressed]
            pressed += 1
    return m.log


def jumps(log):
    return [(f, to) for f, _, to in log if to in AIR_FRAMES]
```

Read it against the model. The states are the values of `self.action`. The guarded row `δ(grounded, A)` is the method `grounded`, three possible next states chosen by guards checked in a fixed order. The speed guard lives in one method, `fast_enough`, because two transitions use it. `step` is the frame loop: countdown first, then handlers until one returns false. The cap of 4 passes is a safety net. The decompilation's own comment on its loop notes that a cycle of actions that keep switching could hang the game.

`prev_land` looks redundant at first. Mario is already in `jump_land` or `double_jump_land` during the landing. But once the landing ends he is in `grounded` either way, and the only thing that still separates "just landed a single" from "just landed a double" is that one remembered value. The game solves this the same way, with `m->prevAction`.

### Numbers you can check

Append this to the same file and run it.

```python
for row in run([3, 3], speed=25):
    print(row)
print([jumps(run([d], speed=25))[1] for d in range(1, 11)])
print(jumps(run([3, 3], speed=20)))
print(jumps(run([3, 9], speed=25)))
print(jumps(run([9, 3, 3], speed=25)))
```

**A clean triple at speed 25.** Presses 3 frames after each touchdown. `run([3, 3], speed=25)` logs seven transitions.

| Frame | From | To | Why |
|---|---|---|---|
| 0 | grounded | jump | first press, timer 0 |
| 20 | jump | jump_land | touchdown after 20 airborne frames |
| 23 | jump_land | double_jump | A on landing frame 3 |
| 47 | double_jump | double_jump_land | touchdown after 24 frames |
| 50 | double_jump_land | triple_jump | A on landing frame 3, speed 25 > 20 |
| 80 | triple_jump | triple_jump_land | touchdown after 30 frames |
| 84 | triple_jump_land | grounded | 4 landing frames, timer left at 0 |

**The window.** Now move the second press. The first touchdown is on frame 20, so a delay of `d` means pressing on frame `20 + d`.

| Delay `d` | Frame | Action when A arrives | Timer when checked | Result |
|---|---|---|---|---|
| 1 to 3 | 21 to 23 | jump_land | (not read) | double_jump |
| 4 | 24 | jump_land, which ends; grounded runs in the same frame | 5 | double_jump |
| 5 | 25 | grounded | 4 | double_jump |
| 6, 7, 8 | 26, 27, 28 | grounded | 3, 2, 1 | double_jump |
| 9 | 29 | grounded | 0 | jump |

The chain survives presses on frames 1 to 8 after touchdown. That is 8 frames, not the `4 + 5 = 9` you might guess from the two constants. The landing's last frame and the countdown's first value overlap on frame 4, and the countdown ticks down before the check. In general, with landing length `L` and countdown value `C`, the window is `L + C - 1` frames.

**The two kinds of hop.** `run([3, 3], speed=20)` gives jump, double_jump, then `jump` at frame 50. The timing was perfect, and the guard `20 > 20` failed. `run([3, 9], speed=25)` gives `jump` at frame 56 for the opposite reason: the speed was fine, and the countdown hit 0 on frame 56. The player sees the same hop both times. Your log sees two different rows of the table. When you debug a machine like this, log which guard failed, not only which state you reached.

**A late press restarts the chain.** `run([9, 3, 3], speed=25)` gives jump at 0, `jump` again at 29, double_jump at 52 and triple_jump at 79. The late press does not end the combo forever. It produces a fresh single jump, and the chain counts from there.

### A visual you can move

Open `examples/w11-triple-jump-window.html`. The top view is a frame timeline from 0 to 120, one bar per action, with the countdown drawn as a small step plot under it. Drag the A-press markers and watch the result label on each jump change. Push the second press from 8 to 9 frames after touchdown and the double jump becomes a hop. Drag the speed slider across 20 and the third jump flips between triple and hop while the timeline does not move at all. The bottom view is the state diagram. The edge that fired lights up, and a caption names the guard that decided it.

### Cross-game recognition

**Super Mario 64, the rest of the machine.** The chain is a small corner of a big machine. The decompilation's `include/sm64.h` defines more than 200 `ACT_` action constants. Each constant packs an ID, a **group** (stationary, moving, airborne, submerged, cutscene, automatic, object) and flag bits such as "is in the air". The flags are derived from the action, never set separately, so "airborne" cannot drift out of sync with the action the way a separate `is_jumping` boolean can. The landings you traced sit in the moving group and the jumps in the airborne group. Each frame, `execute_mario_action` picks the handler by group, the same dispatch as `step`.

**Pac-Man ghost modes, revisited.** [CS101 week 11](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) traced the arcade Pac-Man (Namco, 1980) ghosts through scatter, chase and frightened, following Pittman's Pac-Man Dossier. The ghosts reverse on every change between scatter and chase and on entering frightened, and not on leaving frightened. What CS102 adds is where that rule should live. It depends on the pair (from, to), so it belongs in a set of edges such as `REVERSES = {("chase", "scatter"), ("scatter", "chase"), ("chase", "frightened"), ("scatter", "frightened")}`, checked in the one function every transition passes through. That is the same idea as Mario's `prev_land`: the response depends on where you came from, and the machine has to know it. Frightened mode is also a one-deep pushdown state, covered in section 3. The [ghost-mode timeline](../examples/w11-ghost-modes.html) lets you replay the schedule if you want to see those edges fire.

**Godot 4 animation state machines.** `AnimationNodeStateMachine` holds animation states connected by transitions in a graph. You ask it to `travel("some_state")` and, per the class reference, it finds a path through allowed transitions using a shortest-path search. The transition table is drawn in the editor instead of written in code, but it is the same table. Animators edit the graph; programmers send inputs.

**Your CS101 game loop.** CS101 week 11 built a machine with states menu, playing, paused and game over. Same four parts, one level up. A game is a state machine whose states contain other state machines.

The MA101 [lab on range queries](../../MA101-mathematics-for-games-i-algebra-functions-trigon/labs/lab14.md) also asks you to build an aggro and leash machine for a mob. MMO303's [lecture on threat and aggro](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w06-threat-aggro-and-control.md) describes the rules such a machine must encode.

### Eyes-open design judgment

- **Rerun on the same frame, and cap it.** Without the rerun, a press on the frame a landing ends is lost, and players feel a dropped input. Try it: change `range(4)` to `range(1)` and `run([4], speed=25)` never makes a second jump. The rerun needs a cap, because two handlers that keep handing control to each other would freeze the frame.
- **Timers are part of the state.** Two Marios both in `grounded`, one with timer 3 and one with timer 0, respond to the same press differently. When you save, replay or network a state machine, the countdown goes with it. Next week's replay system depends on this.
- **Remembered history is state too, so keep it small.** `prev_land` is one value. The alternative is more explicit states, `grounded_after_single` and `grounded_after_double`, which make the table longer but put every case on screen. SM64 stores `prevAction` instead because it has more than 200 actions and many landings. Pick explicit states while the count is small.
- **Guards hide the reason for a result.** The same visible hop has two causes here. Log the guard that failed, and give designers a debug overlay that shows the countdown. Tuning a window you cannot see is guesswork.
- **FSMs do not scale forever.** Twenty states with ten inputs is a 200-cell table. Past that, split the machine (section 3) or move to behaviour trees, which CS203 covers in week 7 (see the [CS203 week 7 lecture](../../CS203-artificial-intelligence-for-games/lectures/w07-behavior-trees.md)).

## 3. When one flat machine is not enough

### Hierarchical machines: shared behaviour in a superstate

The heroine grows. She now has standing, walking, running and ducking on the ground, plus jumping and diving in the air. In all four ground states, B should jump. In a flat machine you write that row four times, and one day someone forgets the fourth.

A **hierarchical state machine** nests states. "On ground" becomes a **superstate** containing standing, walking, running and ducking. An input is first offered to the current substate. If the substate ignores it, the superstate gets a turn. B is handled once, in "on ground." Ducking can still override it if a designer wants a special slide-jump.

In code, the simplest version is inheritance from week 3. `OnGroundState.handle_input` handles B. `DuckingState(OnGroundState)` overrides `handle_input`, handles DOWN_RELEASE itself and calls `super().handle_input(button)` for everything else.

### Pushdown machines: remembering where you were

[Week 6](w06-queues-and-stacks-undo-and-command-buffers.md) already met the **pushdown automaton**: a stack of states where the top one is active, opening a screen pushes and "back" pops. It applies inside characters too. Pac-Man's frightened mode is a one-deep version. Frightened sits on top of the paused scatter or chase mode and pops back to it, and CS101's code got away without an explicit stack because the phase index remembered the mode underneath. Mario's `prev_land` is a one-deep memory of the same kind, only it remembers the past instead of the state to return to. A character that can be stunned while frightened while in a cutscene needs the real stack.

### Concurrent machines: when states are independent

The heroine can now also hold a weapon: unarmed, sword or bow. Movement and weapon are independent. She can duck with a bow or jump with a sword. One flat machine needs every combination.

| Design | States to write | Transitions to reason about |
|---|---|---|
| One machine, movement × weapon | 4 × 3 = 12 | every pair crossing both concerns |
| Two concurrent machines | 4 + 3 = 7 | each machine on its own |

With a third concern (status: normal, poisoned, stunned) the flat count is 36 and the concurrent count is 10. The rule is to **multiply when concerns interact and add when they do not.** Run concurrent machines side by side and let each ignore the other's inputs. Where they do interact (you cannot draw the bow while diving), add a guard, a condition checked before a transition, rather than merging the machines.

### When booleans are fine

A flag is the right tool when it is truly independent of everything else and has no transitions of its own. `is_invulnerable_to_fire` from an item is a property, not a state. The test: if you find yourself writing `if a and not b and not c`, those flags are states in disguise.

## 4. The State pattern: objects as states

A table is perfect when states differ only in *where they go next*. When states also differ in *what they do each frame* (ducking charges a super-jump, diving accelerates downward), put that behaviour in the state itself. That is the **State pattern** from the Gang of Four book, as Nystrom presents it: each state is an object with the same interface, and the character delegates to its current state.

```python
class State:
    def enter(self, hero): pass
    def exit(self, hero): pass
    def handle_input(self, hero, button): return None   # or a new State
    def update(self, hero, dt): return None             # or a new State


class Ducking(State):
    def enter(self, hero):
        self.charge = 0.0
        hero.sprite = "duck"

    def handle_input(self, hero, button):
        if button == "DOWN_RELEASE":
            return Standing()

    def update(self, hero, dt):
        self.charge += dt
        if self.charge > 1.0:
            hero.super_jump_ready = True


class Hero:
    def __init__(self):
        self.state = Standing()
        self.state.enter(self)

    def _change(self, new):
        if new is not None:
            self.state.exit(self)
            self.state = new
            self.state.enter(self)

    def handle_input(self, button):
        self._change(self.state.handle_input(self, button))

    def update(self, dt):
        self._change(self.state.update(self, dt))
```

Three things to notice.

- **Per-state data lives in the state.** `charge` exists only while ducking. It cannot leak into jumping, which is exactly the kind of bug the booleans caused.
- **`enter` and `exit` are where setup and cleanup go.** Set the sprite on enter; stop the charging sound on exit. Because `_change` is the only way to switch, enter and exit always pair up.
- **States return the next state rather than setting it.** The hero stays in charge of the switch, which keeps the enter/exit guarantee.

The trade-off is that the transition table is now scattered across classes. Nobody can read "all the ways to reach diving" in one place. Many teams keep both: state objects for behaviour, plus a generated table or diagram for review.

## In-class activity (25 minutes)

Work in pairs. Design the state machine for a dungeon door that players open with a lever, that a boss fight locks, and that a rogue can pick.

1. List the states. Start with open, closed and locked, then add whatever the rules need (opening, closing, picking in progress).
2. List the inputs: `LEVER_PULLED`, `BOSS_PULLED`, `BOSS_DIED`, `PICK_STARTED`, `PICK_FINISHED`, `PICK_INTERRUPTED`, `ANIMATION_DONE`. Add any you need.
3. Fill the full transition table. Every cell gets a next state or a dash.
4. Mark which transitions have side effects (sound, collision on or off, event emitted for week 10's bus) and whether each belongs on the transition or on entering a state.
5. Count the cells. Then count how many booleans a flag-based version would need and how many combinations those flags allow.

Expected output: a filled table, a list of side effects placed on transitions or states with one-line reasons, and the two counts. Swap with another pair and try to find an input sequence that leaves their door in a state the designer would call a bug.

## Common misconceptions

- **"A state machine is a big `if` chain on a `state` string."** That is one implementation. The idea is the table: a single current state and an explicit next state for every input. You can implement it with a dict, with objects or with an editor graph.
- **"The next state depends only on the current state and the input."** In a pure FSM, yes. Real game machines add guards (Mario's speed check) and memory (the countdown, `prev_land`). Those are still state. Count them when you ask how many situations the machine can be in, and save them when you save the game.
- **"Side effects belong in states."** Many belong on transitions. What A does in `grounded` depends on the landing Mario came from, and Pac-Man's reversal depends on the pair (from, to). Putting either on "entering a state" gives the wrong behaviour.
- **"More states means more complexity."** More *representable* states means more bugs. Replacing 4 flags (16 combinations) with 4 explicit states removes 12 illegal ones, even though the word "state" now appears more often in your code.
- **"Concurrent machines are an advanced feature I can skip."** Without them, independent concerns multiply. Movement × weapon × status is 36 states flat and 10 concurrent.

## Check yourself

1. A character has flags `is_swimming`, `is_climbing`, `is_gliding`, `is_mounted` and `is_stunned`. Designers say at most one of the first four can be true at a time, and `is_stunned` can combine with any of them or with none. How many combinations can the flags represent? How many are valid?
2. Using the worked-example model at speed 25, the second press comes 2 frames after the first touchdown and the third press 7 frames after the second touchdown. On which frames do the three jumps start, and which jumps are they?
3. A designer wants the chain window to be 12 frames after touchdown without changing the 4-frame landing. What value of `CHAIN_FRAMES` for the two landings gives that? Check it with `run`.
4. A designer wants the triple jump to work at a speed of exactly 20. Which one line of the worked-example code changes, and why is it one line and not two?
5. A tank character has movement (idle, walking, charging), stance (defensive, offensive) and a shield (up, down, broken). How many states does one flat machine need? How many do concurrent machines need?

<details>
<summary>Answers</summary>

1. `2^5 = 32` representable. Valid: 5 movement choices (none or one of four) × 2 stun values = **10**. So 22 combinations are illegal.
2. Jump on frame 0, touchdown on 20. The press on 22 lands inside `jump_land`, so **double_jump on frame 22**. It lasts 24 frames and touches down on 46. The press on 53 is 7 frames after touchdown. The landing ended on 50, and the countdown reads 2 on frame 53. Speed 25 is above 20, so **triple_jump on frame 53**.
3. The window is `L + C - 1`, so `4 + C - 1 = 12` gives **C = 9**. With `CHAIN_FRAMES` set to 9 for both landings, delays 1 to 12 give a double jump and 13 gives a hop.
4. Change `return self.speed > TRIPLE_SPEED` to `return self.speed >= TRIPLE_SPEED` in `fast_enough`. Two transitions use the guard (from `grounded` and from `double_jump_land`), and both call that one method. With the comparison copied into both places, a designer's change could fix one and miss the other.
5. Flat: `3 × 2 × 3 = 18`. Concurrent: `3 + 2 + 3 = 8`.

</details>

## Lab / assignment hook

[Lab 11, table-driven state machines](../labs/lab11.md). Starting from `labs/lab11-starter.py`, you build a generic table-driven FSM class, refactor a flag-based heroine into states and prove with an exhaustive input test that no illegal state is reachable. Then you finish the jump chain from this lecture on top of the same FSM class, with guards that pick the input symbol, and reproduce the window table. The state machine you build is reused in the week 12 replay lab and in the pattern project.

## Sources

- Nystrom, R. (2014). *Game Programming Patterns*, "State" chapter. Genever Benning. gameprogrammingpatterns.com/state.html. The heroine example (standing, jumping, ducking, diving), the flag bugs, hierarchical, pushdown and concurrent machines are paraphrased from this chapter.
- n64decomp, *sm64*, a decompilation of Super Mario 64 (Nintendo, 1996), master branch, accessed September 2026. https://github.com/n64decomp/sm64
  - `include/sm64.h`: 235 `#define ACT_...` action constants; action groups stationary, moving, airborne, submerged, cutscene, automatic and object; flag bits such as `ACT_FLAG_AIR`; `ACT_JUMP_LAND` and `ACT_DOUBLE_JUMP_LAND` in the moving group, `ACT_JUMP`, `ACT_DOUBLE_JUMP`, `ACT_TRIPLE_JUMP` in the airborne group.
  - `src/game/mario_actions_moving.c`: the `LandingAction` table (jump, freefall and double-jump landings last 4 frames and set the double-jump timer to 5; triple-jump and backflip landings set it to 0); `common_landing_cancels` sets the timer, then checks the frame count, then A; `set_triple_jump_action` requires `forwardVel > 20.0f` unless Mario has the Wing Cap; `act_triple_jump_land` clears the A press.
  - `src/game/mario.c`: `set_jump_from_landing` switches on `m->prevAction` while `doubleJumpTimer` is nonzero; `update_mario_inputs` decrements `doubleJumpTimer`; `execute_mario_action` calls it before a loop that reruns the group handler while it reports an action change, with a comment that the loop could hang if actions cycled.
- Pittman, J. (2009). "The Pac-Man Dossier". Published on Game Developer (formerly Gamasutra), 23 February 2009. Arcade Pac-Man (Namco, 1980). Ghost modes chase, scatter and frightened; reversals forced on chase→scatter, chase→frightened, scatter→chase, scatter→frightened and not on leaving frightened. https://www.gamedeveloper.com/design/the-pac-man-dossier
- Godot Engine class reference, "AnimationNodeStateMachine" (Godot 4.7). States connected in a graph; `travel()` uses a shortest-path algorithm through allowed transitions.
- Gamma, E., Helm, R., Johnson, R. & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley. The State pattern.

## Interactive spec: examples/w11-triple-jump-window.html

**The one insight.** The jump chain is a frame-stepped state machine with a countdown and a speed guard. A second press continues the chain on frames 1 to 8 after touchdown (4 landing frames plus a countdown of 5, overlapping by one frame), and a third press also needs speed above 20. The same visible hop therefore has two different causes, and the page must make it obvious which one fired.

**Layout.** Two stacked panels at every width. Panel A, "When" (frame timeline and window strip), on top. Panel B, "Why" (state diagram and press table), below.

**Model (must match the lecture code exactly).** Port `Mario`, `run` and `jumps` from section 2 line for line to JavaScript.
- `LAND_FRAMES = 4`; `CHAIN_FRAMES = {jump_land: 5, double_jump_land: 5, triple_jump_land: 0}`; `TRIPLE_SPEED = 20`, guard `speed > 20`; `AIR_FRAMES = {jump: 20, double_jump: 24, triple_jump: 30}`.
- Each frame: decrement the timer if above 0, then run handlers until one returns false, at most 4 passes. The "rerun" toggle (default on) sets the cap to 4; off sets it to 1.
- Presses: frame 0, then `d2` frames after the first touchdown, then `d3` frames after the second touchdown. Simulate 150 frames, display 0 to 120.
- For every press, record: frame, action when A arrived, timer value the `grounded` handler read (or "not read" if a landing handler consumed the press, or "ignored" for `triple_jump_land` or airborne), and the result action or "none".

**Panel A, timeline.** Horizontal axis frames 0 to 120, ticks every 10. One bar coloured by action, each also with a distinct pattern: grounded plain, jump solid, double_jump dotted, triple_jump cross-hatch, the three landings diagonal hatch in the colour of their jump. Text label inside a block when it fits. Under the bar, a step plot of the timer (0 to 5) per frame. A downward triangle above the bar at each A press, labelled with its result ("double", "triple", "hop", "lost"). A result of "hop" also shows its cause: "timer 0" or "speed ≤ 20".

**Window strip.** Under the timeline, 15 cells for `d2 = 1..15` with the current `d2` outlined. Each cell shows what the second press would produce with everything else fixed: "double" for 1 to 8, "hop" for 9 to 15 (with rerun on). With rerun off, cell 4 reads "lost". Caption: "Chain window after touchdown: frames 1 to 8 (L + C - 1 = 4 + 5 - 1)."

**Controls.** Sliders: second-press delay `d2` (1 to 15, default 3), third-press delay `d3` (1 to 15, default 3), forward speed (0 to 40, step 0.5, default 25). Toggle "Rerun handlers in the same frame" (default on). Preset buttons with `aria-pressed`: "Clean triple" (3, 3, 25), "Too slow" (3, 3, 20), "Late third" (3, 9, 25), "Press on landing's last frame" (4, 3, 25), "Late second" (9, 3, 25). Play / pause steps a playhead through frames 0 to 120 at 30 frames per second of real time; a scrub slider sets it directly.

**Panel B, diagram and press table.** Seven nodes: grounded, jump, jump_land, double_jump, double_jump_land, triple_jump, triple_jump_land. Edges: grounded→jump, grounded→double_jump, grounded→triple_jump, jump→jump_land, double_jump→double_jump_land, triple_jump→triple_jump_land (touchdown), jump_land→double_jump (A), double_jump_land→triple_jump (A, speed > 20), double_jump_land→jump (A, speed ≤ 20), each landing→grounded (4th frame). Edges carry no text, to stay legible at 390 px. The node at the playhead has a thick outline. When the playhead crosses a transition, that edge highlights for 600 ms (instant under `prefers-reduced-motion`) and a caption under the diagram names the edge and the guard that decided it, for example "Frame 50: double_jump_land → jump. A during double_jump_land, speed ≤ 20." Beside it, the press table: press number, frame, action when A arrived, timer read, result, guard that decided it.

**Readouts (exact).** Summary line: "Jumps: jump (0), double_jump (23), triple_jump (50)." listing `jumps(run(...))` in order. An `aria-live` region announces each transition during playback ("frame 23, jump_land to double_jump").

**Test values (must match exactly).**
- (3, 3, 25), rerun on: transitions at 0 grounded→jump, 20 jump→jump_land, 23 jump_land→double_jump, 47 double_jump→double_jump_land, 50 double_jump_land→triple_jump, 80 triple_jump→triple_jump_land, 84 triple_jump_land→grounded. Summary "jump (0), double_jump (23), triple_jump (50)".
- (3, 3, 20): jump (0), double_jump (23), jump (50); third press cause "speed ≤ 20".
- (3, 3, 20.5): jump (0), double_jump (23), triple_jump (50).
- (3, 9, 25): jump (0), double_jump (23), jump (56); third press timer read 0.
- (4, 3, 25): jump (0), double_jump (24), triple_jump (51); second press timer read 5.
- (4, 3, 25), rerun off: jump (0) only; second press "lost".
- (9, 3, 25): jump (0), jump (29), double_jump (52).
- Window strip at speed 25, rerun on: cells 1 to 8 "double", 9 to 15 "hop".

**Accessibility and style.** `templates/interactive-tokens.css` values inline. Actions distinguished by pattern and text, not colour alone. All controls keyboard reachable. No Nintendo characters, sprites, logos or level art: Mario appears only as a name in text. No horizontal page scroll at 390 px; the timeline SVG scales to the panel width.
