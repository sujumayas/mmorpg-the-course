# CS102 · Week 12 — Pattern: Command (Input, Replay, Undo)

**Why this matters:** Key rebinding, undo in a level editor, instant replays, bug reports you can reproduce exactly, and lockstep multiplayer all come from one idea. You turn "do this" into a small object you can store, send, delay, repeat or reverse. Get that right and a 30-second replay costs less than two kilobytes. Get determinism wrong and the replay drifts off into a different game within seconds.

**You will be able to:**
- Implement input handling, replay and undo with command objects in Python.
- Compute the size of a command recording and of a snapshot recording for a given tick rate, duration and entity count, and compare them.
- Record 30 seconds of input and replay it with a matching checksum, and name every source of nondeterminism that would break the match.
- Design an undo/redo stack for an editor and decide what each command must store to reverse itself.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "Command" chapter. Bettner, P. & Terrano, M., "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (2001), the sections on the lockstep model and on synchronization. Reread your week 6 notes on undo stacks and your week 11 notes on timers.

**Prerequisites from earlier courses:** [CS101 week 9, delta time and frame-rate independence](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (why this week uses a fixed timestep instead of the frame's `dt`). [CS101 week 13, randomness](../../CS101-programming-for-games-i/lectures/w13-randomness-spawning-and-procedural-variety.md) (random spawns, now made reproducible). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (a seed fixes a pseudo-random sequence). From this course, [week 6, queues and stacks](w06-queues-and-stacks-undo-and-command-buffers.md) (undo and redo stacks, input buffers), [week 10, Observer and events](w10-observer-and-events.md) and [week 11, State machines](w11-state-and-state-machines.md) (timers are part of the state you must reproduce).

**Interactive:** [Record and replay](../examples/w12-record-and-replay.html). Keep it open during section 2.

---

## 1. A call you can hold in your hand

Here is the input code most first games start with.

```python
def handle_input(keys, player):
    if keys["space"]:
        player.jump()
    if keys["j"]:
        player.fire()
```

The call `player.jump()` happens and is gone. You cannot store it, send it to another machine, run it later, run it again or take it back. It is also welded to the space bar, so rebinding keys means editing this function.

The **Command pattern** turns the call into an object. Nystrom's one-line definition is that a command is a *reified* method call. "Reified" means made into a thing, data you can keep in a variable, a list or a file.

```python
class Command:
    def execute(self, actor): ...


class Jump(Command):
    def execute(self, actor):
        actor.jump()


class Fire(Command):
    def execute(self, actor):
        actor.fire()


bindings = {"space": Jump(), "j": Fire()}      # rebinding = editing this dict

def handle_input(pressed_keys):
    return [bindings[k] for k in pressed_keys if k in bindings]

for command in handle_input(pressed):
    command.execute(player)
```

Three things changed. The input handler no longer knows about the player; it *returns* commands. The binding is data, so an options menu can rebind keys by editing a dictionary. And `execute(actor)` takes the actor as a parameter, so the same `Jump` drives the player, an AI enemy that chooses commands, or a replay that feeds recorded ones.

That last point is the one this lecture builds on. **If every change to the game world comes from a command, then the list of commands is a complete description of what happened.**

## 2. Worked example: record 30 seconds, replay it exactly

### Hook from a shipped game

When you leave Doom (id Software, 1993) sitting on its title screen, it plays demos, short recordings of a player moving through a level, fighting, taking damage. They are not videos. The demo lumps are tiny, and in the source code id released in 1997 you can see why.

The game runs its simulation at a fixed **35 tics per second** (`TICRATE`). Every tic, each player's input is packed into a structure called `ticcmd_t`, literally a "tic command": forward movement, sideways movement, turning and a byte of button flags. A demo stores a 13-byte header (version, skill, episode, map, a few game options and which of the four players are present), then exactly **4 bytes per player per tic**, then an end marker. Playback reads those 4 bytes back each tic and runs the same simulation.

It works because the simulation is **deterministic**. Doom's gameplay randomness comes from `P_Random()`, which walks a fixed table of 256 bytes with an index that is reset to zero whenever a new game starts, including when a demo starts playing. A second function, `M_Random()`, uses the same table with its own index for things that do not affect gameplay. The source even carries a comment asking which of the two is the deterministic one. And the loader refuses a demo whose version byte differs from the game's own: "Demo is from a different game version!" Different code means a different simulation, which means the same commands would produce a different game. Doom players call that a **desync**.

So a demo of 30 seconds is `30 × 35 = 1,050` tics, times 4 bytes, plus 13 bytes of header and 1 end marker: **4,214 bytes**. That is the whole recording.

### The model

```
state[t+1] = step(state[t], command[t])      fixed dt, seeded RNG inside state

record:  state[0], seed, command[0..T-1]
replay:  state'[0] = state[0]; state'[t+1] = step(state'[t], command[t])
claim:   state'[t] == state[t] for every t   if and only if step is deterministic
```

- `state[t]` is everything the simulation reads: positions, health, timers from week 11, and the random number generator's internal state.
- `command[t]` is the input for tick `t`, packed into a few bytes.
- `step` is the fixed-timestep update from CS101 week 9. Its `dt` is a constant, never the measured frame time.
- **Deterministic** means that `step` depends on nothing except its two arguments. No clock, no unseeded randomness, no iteration order that changes between runs.

Size model, for `T` ticks:

```
command recording = header + T × (bytes per command)
snapshot recording = T × (entities × fields × bytes per field)
```

### The code

```python
import hashlib
import random
import struct

HZ = 60
DT = 1 / HZ
TICKS = 30 * HZ                      # 30 seconds = 1,800 ticks
UP, DOWN, LEFT, RIGHT, FIRE = 1, 2, 4, 8, 16      # one byte per tick


class World:
    def __init__(self, seed):
        self.rng = random.Random(seed)            # the only source of randomness
        self.x, self.y = 0.0, 0.0
        self.score = 0
        self.shots = 0

    def step(self, buttons, dt=DT):
        speed = 90.0                               # units per second
        dx = ((buttons & RIGHT) > 0) - ((buttons & LEFT) > 0)
        dy = ((buttons & DOWN) > 0) - ((buttons & UP) > 0)
        self.x += dx * speed * dt
        self.y += dy * speed * dt
        if buttons & FIRE:
            self.shots += 1
            if self.rng.random() < 0.25:           # 25% hit chance
                self.score += 1

    def checksum(self):
        data = struct.pack("<ddii", self.x, self.y, self.score, self.shots)
        return hashlib.sha1(data).hexdigest()[:8]


def play(seed, commands):
    world = World(seed)
    for buttons in commands:
        world.step(buttons)
    return world
```

The byte `buttons` is our `ticcmd_t`. It is a serialized command with one bit per button, the same way Doom packs its button flags. Recording is appending that byte to a `bytearray` each tick. Replay is `play(seed, recording)`. The checksum is a short fingerprint of the state; if two runs print the same checksum, their states match to the last bit.

For a repeatable "human", this lecture and the interactive use a scripted player you can check by hand. It holds RIGHT for ticks 0 to 599, UP for 600 to 1,199 and LEFT for 1,200 to 1,799, and it adds FIRE on every tick divisible by 10. Each tick moves `90 × 1/60 = 1.5` units, so the run ends at `(0, −900)` after 180 shots. The replay test also needs a jittery timestep, so the code includes a replay whose `dt` wobbles by up to 20% around 1/60 s, drawn from its own seeded generator.

```python
def scripted():
    out = []
    for tick in range(TICKS):
        held = RIGHT if tick < 600 else UP if tick < 1200 else LEFT
        out.append(held | (FIRE if tick % 10 == 0 else 0))
    return out


def play_jittery(seed, commands, jitter_seed=5):
    world, jitter = World(seed), random.Random(jitter_seed)
    for buttons in commands:
        world.step(buttons, DT * (0.8 + 0.4 * jitter.random()))
    return world


recording = bytearray(scripted())       # 1,800 bytes, one per tick
```

Lab 12 uses a different scripted player, one that holds a random direction for 20 ticks at a time. Its choices are recorded too, so how a player decided does not matter to the replay.

### Numbers you can check

Record the scripted 30 seconds with world seed 1234, then replay the 1,800 recorded bytes with `play(1234, recording)`, `play(999, recording)` and `play_jittery(1234, recording)`.

| Run | Seed | Timestep | Checksum | Position (x, y) | Score / shots |
|---|---|---|---|---|---|
| Live recording | 1234 | fixed 1/60 s | `0b9868fa` | (0.0, −900.0) | 48 / 180 |
| Replay | 1234 | fixed 1/60 s | `0b9868fa` | (0.0, −900.0) | 48 / 180 |
| Replay, wrong seed | 999 | fixed 1/60 s | `0b058595` | (0.0, −900.0) | 43 / 180 |
| Replay, jittery `dt` (±20%) | 1234 | 1/60 s × 0.8 to 1.2 | `72e94a16` | (0.473, −898.245) | 48 / 180 |

Read the table slowly, because each failure breaks a different part of the state.

- The **true replay** matches to the bit. The recording is 1,800 bytes.
- The **wrong seed** leaves the path identical. Movement never touches the RNG. But the same 180 shots now roll different numbers, and the score is 43 instead of 48. A replay viewer would see the player walk the same route and hit different enemies.
- The **jittery timestep** keeps the score, because the RNG is consumed once per shot in the same order. But each tick moves the player by `90 × dt` with a slightly different `dt`, and the errors add up to 1.8 units of drift in 30 seconds. The wobble averages out over many ticks, which is why the drift is small, and why nobody notices it by watching. In a real game that drift changes which enemy a shot hits, which changes the RNG calls from then on, and the two games part ways for good.

Now the sizes. Suppose the alternative is to record a snapshot of the world every tick: 200 entities with 5 numbers each (x, y, vx, vy, hp) as 8-byte floats.

| Recording method, 30 s at 60 Hz | Size |
|---|---|
| Commands, 1 byte per tick | 1,800 bytes |
| Commands, only when input changes (2-byte tick + 1-byte buttons) | 360 changes × 3 = 1,080 bytes |
| Doom demo format, 30 s at 35 tics, one player | 4,214 bytes |
| Snapshots, 200 entities × 5 fields × 8 bytes × 1,800 ticks | 14,400,000 bytes |

Commands are about **8,000 times smaller** than snapshots here. The change-only encoding saves only 40%, because our scripted player taps fire every tenth tick, and each tap is two changes, press and release. The direction switches at ticks 600 and 1,200 land on fire ticks, so they add no extra changes. A real player who holds a direction for seconds would compress much better. Try it in the lab.

The price of that tiny file is the claim in the model. Commands describe a game only if the simulation turns the same commands into the same game every time.

### A visual you can move

Open `examples/w12-record-and-replay.html`. The left view is the arena. The recorded run draws a solid trail and the replay draws a dotted trail on top of it. The right view plots the distance between the two runs over 30 seconds, and a byte counter shows the recording size next to the snapshot size. It runs the same scripted player and step rule, but its hit rolls come from mulberry32, a small seedable generator, because JavaScript has no seeded one built in. So its score and jitter drift differ from the Python table, while position, shots and every size match. With every "deterministic" switch on, the dotted trail sits exactly on the solid one and the error line is flat at zero. Turn off "fixed timestep" and the error line starts climbing within a second. Turn off "seeded RNG" and the trail stays put while the hit markers change. The two views disagree about *what* went wrong, and that is the lesson. Each unrecorded input corrupts a different part of the state.

### Cross-game recognition

**Age of Empires (Ensemble Studios, 1997).** Bettner and Terrano describe how the game kept hundreds of units in sync over 28.8k modems without sending unit positions at all. Every machine ran the same simulation and exchanged only player **commands**. A command issued during communications turn 1000 was scheduled to execute on turn 1002, giving it time to reach everyone. Turns were typically 200 ms long. Any machine whose simulation disagreed was declared "out of sync" and the game stopped. The authors describe how a tiny difference in one villager's foraging could show up minutes later as a mismatch in food totals. That is our jittery-`dt` row, stretched across a network. [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) builds this model properly.

**Pac-Man patterns (Namco, 1980).** The Pac-Man Dossier reports that the arcade resets the frightened ghosts' random number generator with the same seed at the start of every level and every life. Combined with the fixed mode schedule from week 11, that makes the ghosts deterministic given Pac-Man's inputs. Players famously memorised **patterns**, exact routes that beat a level the same way every time. A pattern is a replay file stored in a human head, and it works for the same reason Doom demos do.

**Godot's `UndoRedo` (Godot 4).** The editor's undo system, also available to your games, asks you to register an "action" with `do` methods and properties and matching `undo` ones, then `commit_action()`. Calling `undo()` runs the undo side and `redo()` runs the do side again. Each action is a command that knows how to reverse itself, which is section 4 of this lecture.

### Eyes-open design judgment

- **Choose commands when the simulation is deterministic and the state is big.** RTS games with hundreds of units, fighting games, puzzle games, turn-based games. The file is tiny, and a bug report can include the exact replay.
- **Choose snapshots when determinism is too expensive.** Physics engines that differ across CPUs, games with heavy threading, or games where replays must survive patches. Snapshots are big but robust. Anything that must replay correctly after a patch has to record state, because the old commands meet new code. CS202 [week 7, snapshots and delta compression](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md) shows how to shrink them.
- **Put a version in the header and refuse mismatches.** Doom does. A replay from last month's build is a different program's input.
- **Add periodic checksums to the recording.** Store the state checksum every second. On playback, compare. You will know *which second* diverged, which turns a vague "the replay goes weird" into a bisectable bug. Age of Empires checksummed the world, the objects and even pathfinding and targeting to track down its out-of-sync bugs.
- **Hybrid is common.** Store a snapshot every N seconds plus commands in between. You can then seek to minute 12 without simulating minutes 0 to 11.

## 3. The determinism checklist

Every item below is something `step` might read that is not in `state` or `command`. Each one breaks replay.

**Wall-clock time.** `time.time()`, `time.perf_counter()` or a frame `dt` inside the simulation. Use a fixed `DT` and a tick counter. Render with interpolation between ticks if the display runs faster (CS101 week 9).

**Unseeded or shared randomness.** The global `random.random()` is seeded from the operating system at start-up. Give the simulation its own `random.Random(seed)` and never let presentation code (particles, UI shimmer) draw from it. Doom's split between `P_Random` and `M_Random` is exactly this rule. Python guarantees that `Random.random()` gives the same sequence for the same seed across versions; its other methods, like `choice`, may change between Python versions. Another reason to version your replay files.

**Iteration order you did not choose.** In Python, the iteration order of a `set` of strings changes from one run of the interpreter to the next, because string hashing is randomized per process. Run `print(list({"wolf", "boar", "bandit", "spider", "slime"}))` three times and you will likely get three different orders. If "fire at the first enemy in the set" is a rule, replays diverge on the first shot. Use lists, dicts (which keep insertion order) or sort by a stable key.

**Floating-point differences across machines.** The same float operations in a different order can round differently, and some platforms and compilers reorder them. Within one Python build on one machine you are safe. Across platforms, lockstep games often switch the simulation to fixed-point integers. MA201 week 14, determinism and floating point, covers why (see the [MA201 syllabus](../../MA201-linear-algebra-and-physics-for-games/syllabus.md)).

**Input sampled outside the command.** If the fire direction is read from the live mouse position inside `step`, it is not in the recording. Everything the player controls must be packed into `command[t]`.

**Uninitialized or leftover state.** Timers not reset, a cache from the previous level, a pooled enemy that still carries last round's health. Replays start from `state[0]`, so `state[0]` must really be the same.

## 4. Undo and redo: commands that reverse themselves

[Week 6](w06-queues-and-stacks-undo-and-command-buffers.md) built undo and redo for a box-pushing puzzle with two stacks of command objects: run pushes onto UNDO and clears REDO, undo moves a command from UNDO to REDO, redo moves it back. It named the methods `do` and `undo`; Nystrom calls the first one `execute`. Same idea. This section adds two things week 6 did not need.

**Capture at execute time, not at creation time.** A level editor paints tiles.

```python
class PaintTile:
    def __init__(self, x, y, new_tile):
        self.x, self.y, self.new_tile = x, y, new_tile
        self.old_tile = None                      # unknown until execute runs

    def execute(self, level):
        self.old_tile = level.tiles[self.y][self.x]
        level.tiles[self.y][self.x] = self.new_tile

    def undo(self, level):
        level.tiles[self.y][self.x] = self.old_tile
```

If `old_tile` were read in `__init__`, a command created now and executed a tick later (queued input, a macro, a network command) would remember the wrong tile, and undo would restore something that was never there. The same rule protects redo: executing again re-captures `old_tile` against the level as it is at that moment.

**Scale changes the answer.** Week 6's puzzle had 300 cells, so snapshots were affordable. A 256 × 256 editor map at one byte per tile is 65,536 bytes. A full copy before each of 500 edits costs `500 × 65,536 = 32,768,000` bytes. Five hundred packed `PaintTile` commands at 16 bytes each cost 8,000 bytes. Some operations are awkward to reverse exactly, such as a flood fill across 10,000 tiles or a random scatter of props. For those, let the command store the changed region as a small snapshot. That is the same hybrid as replay keyframes in section 2.

Replays and undo share one data structure, a list of commands. Replays walk it forward from the start. Undo walks it backward from the end.

## 5. Command buffers: when to execute

Week 6 also queued commands in an input buffer so a press made during an animation still counts. Once commands are objects, *when* they execute is a separate decision from *what* they do.

- **Scheduled execution.** Age of Empires' rule that a command from turn 1000 runs on turn 1002 is a queue keyed by turn number. Every machine executes the same commands on the same turn.
- **AI and players share a path.** An AI that emits `Move` and `Fire` commands goes through the same validation as a player. If the command is illegal for the current state, it is rejected in one place for everyone, and an AI's decisions land in the replay file like anyone else's.
- **Validate at execute time.** A `Fire` created while the player had ammo may execute on a tick when they have none. The command checks the current state; it does not trust the state from when it was made. The week 11 state machine is often the thing it asks.

## In-class activity (25 minutes)

Work in groups of three. Each group gets one of these small games on a card: a top-down shooter, a turn-based tactics game, a racing game with ghost cars, a match-3 puzzle.

1. Define the command for your game. What fields does one tick's (or one turn's) command need? How many bytes, packed?
2. Compute the size of a 30-second (or 30-turn) recording and of a 10-minute one.
3. List every source of nondeterminism your simulation would have if written naively. Use section 3 as a checklist and add anything specific to your genre.
4. Decide: commands, snapshots or hybrid for (a) replays and (b) undo. Give one number that justifies each choice.
5. Present in 90 seconds. Other groups try to find one more source of nondeterminism you missed.

Expected output: a command layout with byte counts, two recording sizes, a nondeterminism list of at least five items, and two decisions with a number each.

## Common misconceptions

- **"A replay is a video."** A command replay stores inputs and re-simulates. It is thousands of times smaller than a video or a snapshot stream, and it breaks if the simulation changes.
- **"If the replay looks right, it is deterministic."** A 1.8-unit drift after 30 seconds is invisible on screen. Compare checksums, not eyeballs, and store checksums inside the recording.
- **"Seeding the random generator is enough."** The seed fixes the sequence. You also need the same *order and number* of calls, which breaks with a variable `dt`, a set of strings, or presentation code sharing the generator.
- **"Undo means saving the previous state."** Saving full states works but costs `edits × state size`. A reversible command stores only what it changed.

## Check yourself

1. Your game simulates at 30 ticks per second. Each command packs a 1-byte button field, two 1-byte stick axes and a 2-byte aim angle. What is the size of a 10-minute single-player recording with a 16-byte header? What is it for a 4-player match?
2. A Doom demo of a full 4-player cooperative level runs 3 minutes. Using the 1997 source format, how many bytes is it?
3. In the worked example, replay with the wrong seed kept the same position but changed the score. Replay with jittery `dt` kept the score but changed the position. Describe a one-line change to `World.step` that would make the jittery replay change the score too, and explain why.
4. An editor stores a full 65,536-byte snapshot before each edit and has a 50 MB undo budget. How many undo steps can it keep? How many if each step is a 16-byte packed command?
5. A player undoes 3 paint commands and then paints a new tile. Why must the redo stack be cleared? Describe what would go wrong on redo if it were not.

<details>
<summary>Answers</summary>

1. Each command is `1 + 1 + 1 + 2 = 5` bytes. 10 minutes is `600 × 30 = 18,000` ticks, so `16 + 18,000 × 5 = 90,016` bytes for one player. Four players: `16 + 18,000 × 5 × 4 = 360,016` bytes.
2. `3 × 60 × 35 = 6,300` tics. `6,300 × 4 players × 4 bytes = 100,800` bytes, plus the 13-byte header and 1 end marker: **100,814 bytes**.
3. Make hits depend on position, for example hit only if `abs(self.x) < 200` or roll with a chance that depends on distance to a target. Now a drifted position changes which shots can hit, so a shot that hit in the recording may be skipped (no RNG call) in the replay, the RNG call sequence shifts, and every later roll differs. Position error has leaked into the random stream, which is how small drifts become different games.
4. Snapshots: `50,000,000 / 65,536 ≈ 762` steps (using 50 MB = 50,000,000 bytes). Commands: `50,000,000 / 16 = 3,125,000` steps.
5. The undone edits were made against the level as it was before the new paint. After the new paint, redoing them would apply `execute` with stale assumptions. `PaintTile` would record the wrong `old_tile`, so a later undo would restore a tile that never existed at that point in the history, and the history would no longer be a straight line you can walk back.

</details>

## Lab / assignment hook

[Lab 12, record, replay and find the desync](../labs/lab12.md). Starting from `labs/lab12-starter.py`, you record 30 seconds of a small arena game, replay it, and hunt down three planted determinism bugs using per-second checksums stored in your recording. Then you add undo and redo to the game's level editor. The replay recorder is a required component of the pattern project, and the final module in week 15 must ship with a deterministic combat replay.

## Sources

- Nystrom, R. (2014). *Game Programming Patterns*, "Command" chapter. Genever Benning. gameprogrammingpatterns.com/command.html. The phrase "reified method call" is quoted from this chapter; input rebinding, actor-parameterized commands, undo/redo and the point that games record commands rather than full state for replays are paraphrased.
- id Software, DOOM source code (Linux release 1.10, published December 1997), github.com/id-Software/DOOM, files `linuxdoom-1.10/d_ticcmd.h` (`ticcmd_t` fields), `doomdef.h` (`TICRATE 35`, `MAXPLAYERS 4`), `g_game.c` (`G_InitNew` calls `M_ClearRandom`; `G_WriteDemoTiccmd` and `G_ReadDemoTiccmd` store 4 bytes per tic; `G_DoPlayDemo` reads the 13-byte header and rejects other versions with "Demo is from a different game version!"; `DEMOMARKER 0x80`) and `m_random.c` (`P_Random` and `M_Random` over one 256-entry table).
- Bettner, P. & Terrano, M. (2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond". Gamasutra (now Game Developer). Commands scheduled two communications turns ahead, turns typically 200 ms, "out of sync" detection, the foraging-villager desync example. https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond
- Pittman, J. (2009). "The Pac-Man Dossier". Game Developer. The frightened ghosts' PRNG is reset with the same seed every level and every life. https://www.gamedeveloper.com/design/the-pac-man-dossier
- Godot Engine class reference, "UndoRedo" (Godot 4.7). Actions with `add_do_method`, `add_undo_method`, `add_do_property`, `add_undo_property`, `commit_action`, `undo` and `redo`.
- Python Software Foundation, *The Python Standard Library*, `random` module, "Notes on Reproducibility" (Python 3.13). Only `Random.random()` is guaranteed to reproduce the same sequence for a seed across versions.

## Interactive spec: examples/w12-record-and-replay.html

**The one insight.** A replay built from commands is exact only when every input to `step` is in the recording. Each unrecorded input corrupts a different part of the state: a wall-clock timestep bends the path, an unseeded generator changes the hits, and the error never shrinks once it appears. Meanwhile the command file is thousands of times smaller than a snapshot stream.

**Layout.** Two linked panels plus a readout strip. Panel A, "Arena" (left, or top on narrow screens). Panel B, "Replay error over time" (right, or below). Readout strip under both.

**Simulation (identical for recording and replay).**
- 60 ticks per second, 1,800 ticks (30 s). Commands are one byte per tick: `UP=1, DOWN=2, LEFT=4, RIGHT=8, FIRE=16`.
- `step(buttons, dt)`: `x += (right − left) × 90 × dt`, `y += (down − up) × 90 × dt` (screen y grows downward). On FIRE: `shots += 1`; draw `u` from the simulation PRNG; if `u < 0.25`, `score += 1` and draw a hit marker at the player's position.
- Simulation PRNG: mulberry32 seeded with the world seed (default 1234). Presentation effects (the hit-marker sparkle) must use a separate PRNG so they never consume simulation numbers.
- Input source, selectable: "Scripted" (default) holds RIGHT for ticks 0 to 599, UP for 600 to 1,199, LEFT for 1,200 to 1,799, and adds FIRE when `tick % 10 == 0`; or "Record my own" (arrow keys or WASD and Space, sampled once per tick, 30 s countdown). Mobile: on-screen d-pad and fire button.

**Panel A, arena.** The recorded run draws a solid trail; the replay draws a dotted trail on top. Hit markers: filled circles for the recording, hollow rings for the replay, so a mismatch shows as a ring without a circle or the reverse. The replay's current position is a hollow square; the recording's is a filled square.

**Replay switches (all on by default).** Each switch, when turned off, changes only the replay run:
- "Fixed timestep": off means the replay uses `dt = (1/60) × (0.8 + 0.4 × v)` with `v` from a separate jitter PRNG (mulberry32 seed 5).
- "Seeded RNG": off means the replay's simulation PRNG is seeded with 999 instead of the recorded seed.
- "Record every input": off means the replay drops FIRE bits on ticks where `tick % 7 == 0` (simulating an input read outside the command).

**Panel B, error over time.** x-axis 0 to 30 s. Two lines: position error `sqrt((x_rec − x_rep)² + (y_rec − y_rep)²)` in units, and score difference `|score_rec − score_rep|` on a second y-axis. Linear y by default; log toggle (clamp zeros to the axis floor and label them "exact"). A vertical marker at the first tick where the full state (x, y, score, shots) differs, labelled with its time.

**Readouts (exact).** "Recording: 1,800 bytes (1 byte per tick)". "Change-only encoding: n changes × 3 = m bytes", computed from the actual command stream. "Snapshots: 200 entities × 5 fields × 8 bytes × 1,800 ticks = 14,400,000 bytes". "Ratio: 8,000×". "Doom-style demo for the same 30 s: 13 + 1,050 × 4 + 1 = 4,214 bytes". Final state for both runs: x, y, score, shots, and a 32-bit FNV-1a checksum of those four values, with "MATCH" or "DESYNC at t = s".

**Controls.** Play / pause, restart, speed 1× / 4× / instant, the three switches, input source select, seed field (integer), "Show Doom-style size" toggle. All keyboard reachable; switches are real checkboxes with labels.

**Test values (must match exactly).**
- Scripted input, all switches on: recording and replay both end at `x = 0`, `y = −900` (1.5 units per tick; 600 ticks right, 600 up, 600 left), `shots = 180`, identical score, "MATCH", error line identically 0. The score comes from mulberry32, so it need not equal the lecture's Python value of 48.
- Scripted input, change-only encoding: 360 changes × 3 = 1,080 bytes, the lecture's value. Count by comparing each tick's byte with the previous one, with tick 0 counted as a change. Every FIRE tap is two changes, and the direction switches at ticks 600 and 1,200 fall on FIRE ticks.
- Scripted input, "Seeded RNG" off: position error 0 at all times and `shots` equal. The score line may differ; the first-difference marker sits on the first FIRE tick whose hit roll differs between the two seeds.
- Scripted input, "Fixed timestep" off: position error is above 0 from tick 1 and at 30 s is non-zero; shots equal; score equal (the PRNG is consumed once per shot in the same order).
- Sizes: 1,800 bytes; 14,400,000 bytes; 8,000×; 4,214 bytes.

**Accessibility and style.** `templates/interactive-tokens.css` inline. Recording vs replay differ by line style and marker shape, not only colour. Honour `prefers-reduced-motion` by defaulting speed to "instant". An `aria-live` region states "MATCH" or "DESYNC at t = 1.2 s" after each run. Draw everything generically; no Doom or Age of Empires art, names in text only.
