# CS101 · Week 11 — Game state machines (menu, play, pause, game over)

**Why this matters:** Your game is always in exactly one mode. The title screen, the level, the pause menu, the game-over screen. Code that tracks those modes with a pile of `True`/`False` flags breaks in ways players find within minutes, like a score that resets when you unpause. A state machine makes the illegal combinations impossible to write.

**You will be able to:**
- Draw a state diagram for a game's flow and turn it into a transition table.
- Implement a finite state machine in Python and GDScript with one state variable, enter and exit actions, and ignored events.
- Compute, from a mode schedule, which state a timed machine is in at any moment, including when another state pauses the clock.
- Critique a flag-based design by counting its reachable illegal states.

**Before class:** Nystrom, *Game Programming Patterns*, the "State" chapter (free online), up to and including "Enter and Exit Actions". Skim the rest. Godot 4 documentation, "Pausing games and process mode".

**Prerequisites from earlier courses:** [CS101 week 2, conditionals and room transitions](w02-conditionals-room-transitions-and-win-lose.md) (a text adventure's rooms are already a state machine). [CS101 week 6, dictionaries](w06-dictionaries-item-databases.md) (tuple keys, used for the transition table). [CS101 week 3, the game loop](w03-loops-and-the-game-loop.md), because a state machine is something the loop asks every frame. [CS101 week 9, delta time](w09-delta-time-and-frame-rate-independence.md) (the accumulator's leftover time). Next semester, [GD102 week 1, systems thinking](../../GD102-systems-design-and-game-mechanics/lectures/w01-systems-thinking-parts-relationships-emergence.md) reads diagrams of states and flows from the design side.

**Interactive:** [Ghost mode machine](../examples/w11-ghost-mode-machine.html). Open it before section 2.

---

## 1. One variable instead of many flags

Here is how most first games track their mode. Something like this appears around week 8:

```python
in_menu = True
paused = False
game_over = False
```

Then the update function grows a tangle of `if` statements:

```python
if in_menu:
    update_menu()
elif not paused and not game_over:
    update_play()
if paused:
    draw_pause_overlay()
```

Three booleans can be in `2 × 2 × 2 = 8` combinations. Your game has four legal modes. That leaves four combinations that should never happen, such as "paused and game over at once" or "in the menu and paused". Nothing in the code prevents them. One missed `paused = False` in the retry button and the next run starts frozen.

| Flags | Combinations | Legal modes | Illegal combinations |
|---|---|---|---|
| 3 (`in_menu`, `paused`, `game_over`) | 8 | 4 | 4 |
| 4 (add `in_shop`) | 16 | 5 | 11 |
| 5 (add `in_cutscene`) | 32 | 6 | 26 |

Each flag doubles the combinations and adds only one legal mode. The bugs grow faster than the features.

A **finite state machine** replaces the flags with a single variable that holds one value from a fixed list:

```python
state = "MENU"   # one of "MENU", "PLAY", "PAUSE", "GAME_OVER"
```

Four legal values, zero illegal combinations. You can't be paused and in the menu at once, because `state` can't hold two strings. Nystrom's "State" chapter tells the same story with a platformer heroine. Flags like `isJumping_` and `isDucking_` pile up until she can do things she shouldn't, such as jump again in mid-air forever. The single `enum` ends that class of bug.

The vocabulary, defined once:

- A **state** is one of the named values. Only one is current.
- An **event** is something that happens, such as a key press, a timer running out, or the player losing the last life.
- A **transition** is a rule "in state S, event E moves you to state T."
- An **enter action** runs once when you arrive in a state. An **exit action** runs once when you leave.
- An event with no rule for the current state is **ignored**. Pressing Pause on the title screen does nothing, and that is a feature.

## 2. Worked example: Pac-Man's ghosts are a state machine you can see

### The hook

Play the first level of the original Pac-Man arcade game (Namco, 1980) and watch one ghost for half a minute. It chases you, then without warning it turns around and heads for its home corner. A little later it turns around again and resumes the chase. Players who notice this often assume the ghost "saw" them or got bored. It didn't. Jamey Pittman's reverse-engineered guide, *The Pac-Man Dossier*, shows that the ghosts are driven by a timer that switches them between two modes, **scatter** (head for your corner) and **chase** (hunt Pac-Man). The sudden U-turn is an enter action. The game forces every ghost to reverse whenever the mode changes between scatter and chase, or when a power pellet sends them into **frightened** mode. There is one exception, and it is the kind of detail that only a clean state machine keeps straight. Ghosts do **not** reverse when frightened mode ends.

### The model

Three states and the events that move between them:

```
             timer ends                power pellet
  SCATTER  ──────────────►  CHASE  ───────────────►  FRIGHTENED
     ▲  ◄──────────────────   │                          │
     │        timer ends      │ power pellet             │ fright time ends
     │                        ▼                          │ (back to the mode
     └──────── power pellet ─► FRIGHTENED ◄──────────────┘  it interrupted)
```

The rules, from the Dossier, for level 1:

1. The ghosts follow a fixed schedule of scatter and chase phases: scatter 7 s, chase 20 s, scatter 7 s, chase 20 s, scatter 5 s, chase 20 s, scatter 5 s, then chase forever.
2. Eating a power pellet switches to frightened for 6 s on level 1. **While frightened, the schedule timer is paused.** When fright ends, the ghosts return to the mode they were in, and the schedule timer resumes.
3. **Enter action.** Changing mode from scatter or chase to any other mode reverses every ghost's direction. Leaving frightened does not.
4. The schedule resets when Pac-Man loses a life or finishes the level.

Rule 3 is where the state machine earns its keep. The reversal is not written in the chase code or the scatter code. It belongs to the *transition*, and the transition knows where it came from.

Here is the machine in Python, using the dictionaries from week 6. It is a model of the rules the Dossier describes, not the original Z80 program.

```python
SCHEDULE = [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20),
            ("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", None)]

def new_ghost():
    return {"mode": "scatter", "phase": 0, "phase_time": 0.0,
            "fright_left": 0.0, "reversals": 0}

def change_mode(ghost, new_mode):
    old_mode = ghost["mode"]
    if old_mode in ("scatter", "chase"):     # rule 3: leaving scatter/chase reverses
        ghost["reversals"] += 1
    ghost["mode"] = new_mode

def update(ghost, dt):
    if ghost["mode"] == "frightened":
        ghost["fright_left"] -= dt           # the schedule clock does NOT advance
        if ghost["fright_left"] <= 0:
            change_mode(ghost, SCHEDULE[ghost["phase"]][0])
        return
    ghost["phase_time"] += dt
    duration = SCHEDULE[ghost["phase"]][1]
    if duration is not None and ghost["phase_time"] >= duration:
        ghost["phase_time"] -= duration
        ghost["phase"] += 1
        change_mode(ghost, SCHEDULE[ghost["phase"]][0])

def eat_power_pellet(ghost, seconds=6.0):
    change_mode(ghost, "frightened")
    ghost["fright_left"] = seconds
```

Read the structure before the lines. There is one state variable, `mode`. There is one function, `change_mode`, through which every transition passes, so the enter action (the reversal) cannot be forgotten on some path. And `update` begins by asking "which state am I in?", then runs only that state's behavior. That shape is every state machine you will write this term.

Notice `phase_time -= duration` rather than `phase_time = 0`. If a frame is 1/60 s long and the phase ends partway through it, the leftover time carries into the next phase. That's the same care you took with the accumulator in week 9. Setting it to zero would make each phase a fraction of a frame too long, and over 90 seconds the drift adds up.

### Numbers you can check

Add up the schedule to get the moment of each transition. With no power pellet eaten, the phase boundaries fall at 7, 27, 34, 54, 59, 79 and 84 seconds.

| Phase | Mode | Starts at | Ends at |
|---|---|---|---|
| 1 | scatter | 0 s | 7 s |
| 2 | chase | 7 s | 27 s |
| 3 | scatter | 27 s | 34 s |
| 4 | chase | 34 s | 54 s |
| 5 | scatter | 54 s | 59 s |
| 6 | chase | 59 s | 79 s |
| 7 | scatter | 79 s | 84 s |
| 8 | chase | 84 s | never |

So at 30 seconds the ghosts are in scatter phase 3. At 60 seconds they are chasing. Across the first 90 seconds there are seven scatter-chase switches and so seven reversals.

Now eat a power pellet at 25 seconds, during the first chase. The ghosts go frightened from 25 to 31, and the schedule clock stops at 25 s of schedule time. When fright ends at 31 s, the ghosts go back to chase with 2 seconds of chase left, so chase phase 2 now ends at 33 s instead of 27 s. Every later boundary moves 6 seconds too.

| Event | Without pellet | With pellet at 25 s | Reverses? |
|---|---|---|---|
| scatter → chase | 7 s | 7 s | yes |
| chase → frightened | — | 25 s | yes |
| frightened → chase | — | 31 s | **no** |
| chase → scatter | 27 s | 33 s | yes |
| scatter → chase | 34 s | 40 s | yes |
| chase → scatter | 54 s | 60 s | yes |
| scatter → chase | 59 s | 65 s | yes |
| chase → scatter | 79 s | 85 s | yes |
| scatter → chase | 84 s | 90 s | yes |

You can reproduce the right-hand column with the code above. Run `update` in steps of 1/60 s, call `eat_power_pellet` once when the clock passes 25, and print the time whenever `mode` changes. By 91 seconds you should count eight reversals, one more than without the pellet. The frightened-to-chase change at 31 s adds a transition but not a reversal.

Your printout will say 7.02 where the table says 7. Adding 1/60 in floating point 420 times gives a number a hair under 7, so the switch fires one frame later. A per-frame timer is only ever accurate to one frame, which is 0.017 s here. That's fine for ghosts. It is not fine for a replay system that must match another machine exactly, which is one reason week 9's fixed timestep counts whole steps instead of summing seconds.

### The visual

The interactive draws two linked views. On top, a state diagram with three circles, the current one lit. Below, a timeline from 0 to 100 seconds, colored by mode, with a small U-turn mark at every reversal. A play button runs the clock at ×1, ×5 or ×10, and presets load the two pellet cases from this section and the check-yourself question. The "Power pellet" button (or the P key) drops a frightened band into the timeline at the current moment.

Press it at 25 s and watch every later band slide 6 seconds to the right. The picture makes rule 2 obvious in a way the text doesn't. A paused clock means everything downstream shifts. Then look at the end of the frightened band. It has no U-turn mark, while every other boundary has one. That's rule 3, the exit from frightened, drawn as an absence.

### Cross-game recognition

**Your game's flow (menu, play, pause, game over).** This is the same machine with different names. `PAUSE` is to `PLAY` what frightened is to scatter and chase. It interrupts, it stops the play clock, and when it ends you return to where you were. Section 3 builds it.

**Godot 4 (engine pause, current documentation).** Setting `get_tree().paused = true` stops `_process`, `_physics_process` and input callbacks on every node whose process mode is Pausable, and it halts the physics servers. A pause menu sets its own process mode to When Paused so it runs only while the game is frozen. Pac-Man's schedule timer and Godot's pausable nodes are the same design. The clocks that belong to "play" stop, and the one state that should keep running does.

**Nystrom's heroine (Game Programming Patterns, "State").** A platformer character with standing, jumping, ducking and diving states. The book shows enter actions doing the same job as the ghost reversal. Entering the standing state sets the standing sprite, so no transition can forget it. It then introduces a **pushdown automaton**, a stack of states where a new state is pushed on top and popped off to return to the one below. That is exactly how frightened "remembers" whether to go back to scatter or chase, and it's how a pause menu remembers which level screen to return to.

One principle across all three. The current mode decides which code runs, and anything that must happen "whenever we switch" belongs to the transition, not to the states on either side.

### Eyes-open design judgment

- **State machines make behavior readable to players.** Pac-Man's ghosts feel alive, yet a good player learns the schedule and exploits scatter phases to clear tough corners. That's a design choice. A machine with visible, regular transitions rewards learning. Add randomness to the timings and you trade learnability for surprise.
- **Enter actions are where polish lives.** The reversal tells the player "something changed" without a word of text. Your pause state should dim the screen and your game-over state should play a sting. Put those in enter actions and they always fire.
- **Flat machines explode.** If "shooting" must work in every movement state, a flat machine needs standing-shooting, jumping-shooting and so on. Nystrom's fix is two machines running side by side, one for movement and one for the weapon. Watch for states whose names are two words glued together.
- **Pausing is a luxury of single-player games.** In a shared online world you cannot stop the clock for everyone because one player opened a menu. Online games turn "pause" into an overlay state that captures input while the world keeps running. That is the MMO version of this lecture, and it's why MMO client code keeps "UI state" and "world state" in separate machines.

## 3. Building the game-flow machine

Your arcade game needs four states. Here is the diagram as a transition table, which is easier to type than to draw:

| Current state | Event | Next state | Transition action |
|---|---|---|---|
| MENU | `start` | PLAY | reset score and lives |
| PLAY | `pause` | PAUSE | — |
| PLAY | `out_of_lives` | GAME_OVER | save high score |
| PAUSE | `resume` | PLAY | — |
| PAUSE | `quit` | MENU | — |
| GAME_OVER | `retry` | PLAY | reset score and lives |
| GAME_OVER | `quit` | MENU | — |

Seven rows. Every pair that is **not** in the table is ignored. Four states times five events is 20 pairs, and 13 of them do nothing, on purpose.

In Python, the table is a dictionary keyed by `(state, event)` pairs, a use of tuples as keys that you saw in week 6:

```python
TRANSITIONS = {
    ("MENU", "start"): "PLAY",
    ("PLAY", "pause"): "PAUSE",
    ("PLAY", "out_of_lives"): "GAME_OVER",
    ("PAUSE", "resume"): "PLAY",
    ("PAUSE", "quit"): "MENU",
    ("GAME_OVER", "retry"): "PLAY",
    ("GAME_OVER", "quit"): "MENU",
}

def handle(game, event):
    key = (game["state"], event)
    if key not in TRANSITIONS:
        return False                      # ignored on purpose
    old, new = game["state"], TRANSITIONS[key]
    on_exit(game, old)
    if event in ("start", "retry"):
        game["score"] = 0
        game["lives"] = 3
    game["state"] = new
    on_enter(game, new)
    return True

def on_enter(game, state):
    if state == "PAUSE":
        game["clock_running"] = False
    elif state == "PLAY":
        game["clock_running"] = True

def on_exit(game, state):
    pass
```

### The unpause bug, and where resets belong

Look at where the score reset lives. It's tied to the `start` and `retry` events, not to entering `PLAY`. Put it in `on_enter(game, "PLAY")` instead and test it. Start a game, score 500 points, pause, resume. Your score is zero. Entering `PLAY` from `PAUSE` is still entering `PLAY`.

This is the same lesson as the ghost reversal, seen from the bug side. Some actions belong to a state ("whenever I'm in PLAY, the clock runs"). Some belong to one transition ("when a new run starts, reset the score"). Mixing them up is the most common state machine bug in student games. When you write an enter action, ask whether it should really fire on every path into the state. If not, move it to the transition.

### The same machine in Godot

In GDScript you'd use an `enum` and a `match` statement:

```gdscript
enum State { MENU, PLAY, PAUSE, GAME_OVER }
var state := State.MENU

func change_state(new_state: State) -> void:
    match new_state:
        State.PAUSE:
            get_tree().paused = true
            $PauseMenu.show()
        State.PLAY:
            get_tree().paused = false
            $PauseMenu.hide()
    state = new_state

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        match state:
            State.PLAY: change_state(State.PAUSE)
            State.PAUSE: change_state(State.PLAY)
```

Two Godot details matter. The node that runs this script must keep processing while the tree is paused, or it will never see the second press of the pause key. Set its process mode to Always, and set the pause menu's to When Paused. And `match` without a case for `MENU` means the pause key does nothing on the title screen, which is the "ignored event" rule for free.

### Per-state update

The final piece is the loop. Each frame, the loop asks the machine which state it is in and runs that state's update. Nothing else:

```python
def update(game, dt):
    if game["state"] == "PLAY":
        update_play(game, dt)
    elif game["state"] == "MENU":
        update_menu(game, dt)
    elif game["state"] == "GAME_OVER":
        update_game_over(game, dt)
    # PAUSE: world does not update; only the overlay is drawn
```

Compare this with the flag version from section 1. Every branch is exclusive, and a new state is one new branch, not a new flag that doubles the combinations.

## 4. Timers inside states

Pac-Man's schedule is a timer that belongs to a group of states. Your game will have smaller ones. The game-over screen should ignore input for 1 second so a player mashing the fire button doesn't skip it by accident. A "get ready" state might last 2 seconds before play begins.

The pattern is the same each time. Reset a timer in the enter action, count it down in that state's update, fire an event when it reaches zero:

```python
def on_enter_game_over(game):
    game["input_lock"] = 1.0

def update_game_over(game, dt):
    game["input_lock"] = max(0.0, game["input_lock"] - dt)

def can_retry(game):
    return game["input_lock"] == 0.0
```

Because `update_game_over` only runs while the state is `GAME_OVER`, the timer stops by itself in any other state. You didn't write any pause logic for it. That's the frightened-mode rule again. A clock owned by a state only runs in that state.

## In-class activity (25 minutes)

In groups of three, pick a game you all know that has at least five screens or modes (a fighting game with character select, a racing game with a replay mode, a mobile puzzle game with a shop).

1. (10 min) Draw its flow as a state diagram. Then turn it into a transition table.
2. (5 min) Count the pairs of state and event your table ignores. Pick two and say what would go wrong if they weren't ignored.
3. (10 min) Find one action that you first wrote as an enter action but which really belongs to a single transition, or the reverse. Explain the bug it would cause.

Expected output: one diagram, one table, the ignored-pair count, and a two-sentence bug report.

## Common misconceptions

- **"A state machine is a special library or engine feature."** It is one variable plus a rule for changing it. A dictionary and an `if` chain are enough.
- **"Enter actions run when the game starts."** They run every time the state is entered, from any direction. That's why a score reset there breaks resume.
- **"Pause means stopping the game loop."** The loop keeps running, or nothing could unpause it. Pause is a state in which the world's update is skipped and the menu's update runs.
- **"More states means more bugs."** More *flags* means exponentially more combinations. More states in one variable adds one case each.

## Check yourself

1. Using the level 1 schedule with no pellet, what mode are the ghosts in at 55 seconds, and how many reversals have happened by then?
2. A power pellet is eaten at 30 seconds, and another at 70 seconds. Frightened lasts 6 seconds each time. When does the final, endless chase begin?
3. A game uses four booleans `menu`, `paused`, `dead`, `shop` and has five legal modes. How many illegal combinations exist? Rewrite it as a transition table sketch with at most one state variable.
4. A student puts `lives = 3` in `on_enter` for `PLAY`. Describe exactly what a player sees.

<details>
<summary>Answers</summary>

1. 55 s lies in phase 5 (scatter, 54 to 59). Reversals at 7, 27, 34 and 54 make four.
2. The pellet at 30 s interrupts scatter phase 3 at 3 seconds in. That adds 6 s to every later boundary, so phase 3 ends at 40 instead of 34 and phase 6 (chase) now runs 65 to 85. The pellet at 70 s falls in that chase and adds 6 s more, so phase 6 ends at 91, scatter phase 7 runs 91 to 96, and the endless chase starts at 96 s. Check: 84 + 6 + 6 = 96.
3. `2⁴ = 16` combinations, 5 legal, so 11 illegal. One variable with values such as `MENU`, `PLAY`, `PAUSE`, `DEAD`, `SHOP`, and a table with rows like `(PLAY, open_shop) → SHOP` and `(SHOP, close) → PLAY`.
4. Every time the player unpauses, their lives go back to 3, so a player who is about to die can pause and resume to refill lives. It's an exploit, and players will find it.

</details>

## Lab / assignment hook

[Lab 11, the game-flow machine](../labs/lab11.md). You implement the ghost mode machine and the menu, play, pause, game-over machine in Python, pass the provided tests (including the unpause test), and write the same machine in GDScript for your mini-game. Deliverable: completed starter files, your Godot scene, and a one-page state diagram.

## Sources

- Pittman, J. (2009). "The Pac-Man Dossier", Game Developer (originally Gamasutra), February 2009. Level 1 scatter and chase schedule (7, 20, 7, 20, 5, 20, 5, then indefinite); forced reversal on mode changes and the exception when leaving frightened; the schedule timer pauses during frightened mode; 6 s frightened time on level 1; timer reset on life lost or level completed. Original arcade Pac-Man (Namco, 1980). https://www.gamedeveloper.com/design/the-pac-man-dossier
- Nystrom, R. (2014). *Game Programming Patterns*, "State". Flag bugs in the heroine example, `enum` and `switch` solution, enter and exit actions, concurrent machines, pushdown automata. https://gameprogrammingpatterns.com/state.html
- Godot Engine documentation, "Pausing games and process mode" (Godot 4 stable, checked September 2026). `SceneTree.paused`, process modes Inherit, Pausable, When Paused, Always, Disabled; which callbacks stop. https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html

## Interactive spec: examples/w11-ghost-mode-machine.html

**Purpose.** Show a timed state machine with an interrupting state. The one insight: frightened mode pauses the schedule clock, so every later transition shifts right by the fright duration, and every transition reverses the ghost except the exit from frightened.

**Layout.** Mobile-first, two linked views stacked (side by side above 900 px).
- View 1, state diagram: three labelled circles SCATTER, CHASE, FRIGHTENED with arrows as in the lecture's diagram. The current state is filled; the last transition's arrow flashes (a static highlight if `prefers-reduced-motion`).
- View 2, timeline: horizontal axis 0 to 100 s with ticks every 10 s. Colored bands for each phase (scatter, chase, frightened use three distinct tokens and text labels inside bands wide enough to hold them). A vertical play head at the current time. A U-turn glyph above the axis at every reversal; no glyph at the end of a frightened band.
- Readout row: current time (one decimal), current mode, current phase number (1-8), time left in phase, reversal count, schedule-clock time (which lags wall time after pellets).

**Model (must match the lecture's Python exactly).** `SCHEDULE = [scatter 7, chase 20, scatter 7, chase 20, scatter 5, chase 20, scatter 5, chase ∞]`. Step at dt = 1/60 s. Leaving scatter or chase for any mode increments reversals. Leaving frightened returns to `SCHEDULE[phase].mode` without a reversal. Frightened duration slider default 6 s. While frightened, `phase_time` does not advance. The timeline must be recomputed from the event list (pellet times) so bands after a pellet visibly shift.

**Controls.**
- Play/Pause button, speed selector ×1, ×5, ×10, and a time scrubber (0 to 100 s). Scrubbing replays the simulation from 0 with the recorded pellet times.
- "Power pellet" button: records a pellet at the current time. If pressed while frightened, restart the fright countdown without a reversal (frightened to frightened is not a scatter/chase exit).
- Fright duration slider, 0 to 10 s in 1 s steps (default 6).
- "Clear pellets" and a preset menu: "No pellet", "Pellet at 25 s", "Pellets at 30 s and 70 s".
- Toggle "Without pause" that compares, as a faint second timeline underneath, the schedule with no pellets, so the 6 s shift is visible side by side.

**Test values (must match).**
- No pellet: transitions at 7, 27, 34, 54, 59, 79, 84 s; 7 reversals by 90 s; mode at 30 s is scatter, at 60 s chase.
- Pellet at 25 s, 6 s fright: frightened 25 to 31; transitions at 7, 25, 31, 33, 40, 60, 65, 85, 90; reversals by 91 s = 8 (in the dt = 1/60 simulation each transition lands up to one frame after the table value, for example 7.02 s; display times rounded to one decimal); no glyph at 31.
- Pellets at 30 s and 70 s: endless chase starts at 96 s.

**Accessibility.** All controls keyboard operable with visible focus. Space toggles play; P triggers a pellet. A live region announces mode changes ("Chase, reversal"). Colors from `templates/interactive-tokens.css`, and bands also carry text labels so color is never the only cue. No Pac-Man art: ghosts are drawn as a plain arrow showing direction, which flips at each reversal.
