# CS101 · Week 12 — Debugging: breakpoints, logging, rubber-ducking

**Why this matters:** You will spend more of your programming life finding bugs than writing new code. Students who debug by staring and changing things at random lose whole evenings. Students who follow a method find most bugs in minutes, and they can explain the bug to a teammate afterward. This week teaches the method and the three tools that power it.

**You will be able to:**
- Apply a six-step debugging loop (reproduce, shrink, observe, hypothesize, fix, guard) to a failing game rule.
- Use a conditional breakpoint and a log line to watch a variable change, in Python and in Godot.
- Compute how many runs a binary search over inputs needs to find the first failing case, and use it.
- Explain an 8-bit overflow bug from its numbers, and write the regression test that keeps it fixed.

**Before class:** Python documentation, "pdb, the Python Debugger" (the commands `p`, `n`, `s`, `c`, `b`) and the `breakpoint()` built-in. Godot 4 documentation, "Debugger panel", the Stack Trace section. Hunt and Thomas, *The Pragmatic Programmer*, the section on debugging (any edition).

**Prerequisites from earlier courses:** [CS101 week 3, loops and the game loop](w03-loops-and-the-game-loop.md) (loop conditions and off-by-one errors). [CS101 week 4, functions and decomposition](w04-functions-and-decomposition.md) (small pure functions are the ones you can test). [CS101 week 7, Godot scenes, nodes and scripts](w07-engine-intro-scenes-nodes-scripts.md). [CS101 week 11, game state machines](w11-game-state-machines.md) (the unpause bug). Two weeks from now, [MA101 week 14, distances and squared distance](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) has a lab with a 32-bit overflow exercise you can compare with this week's 8-bit one. The 8-bit wrap itself was taught in [CS101 week 1](w01-programs-variables-and-types.md).

**Interactive:** [examples/w12-level-256-debugger.html](../examples/w12-level-256-debugger.html). You'll use it in section 2.

---

## 1. A bug is a gap between two stories

Every bug has the same shape. There is the story you believe about your code ("`count` is always at least 1") and the story the computer is actually running ("`count` is 0"). Debugging is the work of finding the exact line where the two stories split.

That framing matters because it tells you what *not* to do. Changing lines at random until the symptom goes away doesn't find the split. It hides it, and the bug comes back in a different costume. Every technique in this lecture is a way to make the computer tell its story, one variable at a time, so you can compare it with yours.

### The debugging loop

Here is the method. Keep it next to your keyboard for the rest of the term.

1. **Reproduce.** Make the bug happen on demand. If you can't reproduce it, you can't know when you've fixed it.
2. **Shrink.** Find the smallest input, level, or sequence of key presses that still shows it. Smaller cases have fewer places to hide.
3. **Observe.** Watch the actual values with a log line or a breakpoint. Don't guess them.
4. **Hypothesize.** State, in one sentence, which line makes the two stories split and why. Make it a sentence that a test could prove false.
5. **Fix.** Change the fewest lines that make the hypothesis's cause go away.
6. **Guard.** Turn your reproduction into an automated test that fails before the fix and passes after. Keep it forever.

Steps 1 and 2 are where most of the time goes and where beginners skip ahead. Step 6 is the one people forget. A bug you fixed without a test is a bug you'll fix twice.

### Three tools

**Logging** means printing values as the program runs, with enough context to read them later. A bare `print(x)` is a log line. A better one names the variable and the moment: `print(f"frame={frame} state={state} x={x}")`. Python's `logging` module adds levels (`DEBUG`, `INFO`, `WARNING`) so you can leave the lines in and switch them off. Logs are the right tool when you need to see a *history*. What happened over 300 frames? Which event came before the crash?

**Breakpoints** stop the program at a line and let you inspect every variable, then step forward one line at a time. In Python, write `breakpoint()` on a line and run the script. You land in `pdb`, the Python debugger, where `p count` prints a value, `n` runs the next line, `s` steps into a function call, and `c` continues to the next breakpoint. In Godot, click in the gutter to the left of a line number to place a red dot, or write the `breakpoint` keyword in GDScript, which is saved in the script file itself. When execution reaches it, the Stack Trace tab opens with the call stack and the current values. Breakpoints are the right tool when you need to see a *moment* in full detail.

A **conditional breakpoint** only stops when a condition is true. Games run the same line thousands of times per second, so an unconditional breakpoint in `_process` is useless. You'd stop every frame. Write the condition as an `if` around the call:

```python
if level_counter == 255:
    breakpoint()
```

**Rubber-ducking** means explaining your code, line by line and out loud, to someone or something that can't help you. The name comes from an anecdote in Hunt and Thomas's *The Pragmatic Programmer* (1999) about a programmer who carried a rubber duck and explained code to it. It works because explaining forces you to say your story out loud, one step at a time, and you hear the step where your story claims something the code doesn't do. It is the right tool when you don't yet know what to observe.

## 2. Worked example: Pac-Man's level 256, found in eight runs

### The hook

The original Pac-Man arcade game (Namco, 1980) has no ending. It has a wall. Players who clear 255 levels reach level 256, where the left half of the maze looks normal and the right half is a jumble of letters, numbers and colored symbols. Nobody can finish that level, so it's where the game stops. Players call it the split screen, or the **kill screen**.

Jamey Pittman's *The Pac-Man Dossier* (2009) traces it to one arithmetic step in the routine that draws the bonus fruit symbols at the bottom of the screen. The game keeps the level in a single byte, a memory cell that holds 0 to 255, and counts from 0, so level 256 is stored as 255. The fruit routine adds 1 to that byte, gets 256, which doesn't fit, and is left holding 0. From 0, its drawing loop runs 256 times instead of a handful, and it paints symbols far past the fruit area, over the right half of the maze.

You can't debug the original ROM in this course, but you can debug an exact model of its logic in Python. That's what the rest of this section does, step by step, with the loop from section 1.

### The model

Two ideas carry the whole bug.

**An 8-bit value wraps.** A byte keeps only the remainder after dividing by 256:

```
byte(n) = n mod 256          so byte(255 + 1) = 0 and byte(0 − 1) = 255
```

**A loop that decrements and then tests for zero runs 256 times when it starts at zero.** Its first decrement turns 0 into 255, and it has to count all the way down.

Here is a Python model of the fruit routine's logic as the Dossier describes it. It is a reconstruction for teaching, not the original Z80 code. Python's own integers never overflow, so the model imitates the byte with `% 256`.

```python
def byte(n):
    return n % 256                     # what an 8-bit register keeps

def symbols_to_draw(level_counter):
    """level_counter is 0 on level 1, as in the original game."""
    count = byte(level_counter + 1)
    if count < 7:                      # early levels: draw one symbol per level
        drawn = 0
        while True:
            drawn += 1                 # draw one symbol
            count = byte(count - 1)
            if count == 0:
                break
        return drawn
    return 7                           # later levels: the row is full
```

The designer's story is "the fruit row shows one symbol per level for the first few levels, then stays full at 7." The rule says nothing about 256 symbols anywhere.

### Numbers you can check

Run `symbols_to_draw` for a few levels. Each row is one call.

| Level on screen | `level_counter` | `level_counter + 1` | `count` after `byte()` | Branch | Symbols drawn |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 | early | 1 |
| 6 | 5 | 6 | 6 | early | 6 |
| 7 | 6 | 7 | 7 | full | 7 |
| 200 | 199 | 200 | 200 | full | 7 |
| 255 | 254 | 255 | 255 | full | 7 |
| 256 | 255 | 256 | **0** | early | **256** |

The last row is the whole bug in numbers. `count` should be 256, which would take the "full" branch and draw 7. Instead it's 0, which is less than 7, so it takes the early branch, and the loop counts 0, 255, 254, ... 1, 0 and draws 256 symbols.

Now walk through the debugging loop as if you didn't know any of this.

**1. Reproduce.** A playtester reports "garbage on screen at the end of a very long run." You write a test that states the designer's story for every level:

```python
def test_fruit_row_never_exceeds_seven():
    for level_counter in range(256):
        assert symbols_to_draw(level_counter) <= 7, level_counter
```

It fails and reports `255`. You can now reproduce the bug in a fraction of a second instead of 255 levels of play.

**2. Shrink.** Suppose you had no such loop, only a slow "play to level N" function that takes a minute per run. Which level is the first bad one? Test the middle of the range and keep the half that contains the change from good to bad. This is a **binary search over inputs**, also called bisecting.

| Probe | Test level | Result | Range still in doubt |
|---|---|---|---|
| — | — | — | 1 to 256 |
| 1 | 128 | good | 129 to 256 |
| 2 | 192 | good | 193 to 256 |
| 3 | 224 | good | 225 to 256 |
| 4 | 240 | good | 241 to 256 |
| 5 | 248 | good | 249 to 256 |
| 6 | 252 | good | 253 to 256 |
| 7 | 254 | good | 255 to 256 |
| 8 | 255 | good | 256 |

Eight probes, because each one halves the range and `2⁸ = 256`. In general, bisecting `N` candidates takes about `log₂ N` runs. A thousand candidates take 10 runs. A million take 20. The same trick works on time (which frame did the value go wrong?), on commits (which change broke it? `git bisect` automates this), and on code (comment out half the new lines).

**3. Observe.** Put a log line where the value is born and run the failing case:

```python
count = byte(level_counter + 1)
print(f"level_counter={level_counter} count={count}")
```

```
level_counter=254 count=255
level_counter=255 count=0
```

Or stop there with a conditional breakpoint and type `p level_counter + 1`, `p count`, then `n` a few times to watch the loop. Either way, you've seen the split. The designer's story says `count` is the level plus one. The computer's story says it's 0.

**4. Hypothesize.** In one testable sentence: *the level-plus-one step wraps to 0 on the last level, and 0 falls into the early-level branch, whose loop then runs 256 times.* Test it by predicting something you haven't looked at yet. If the hypothesis is right, `symbols_to_draw(255)` must return exactly 256, not some other large number. It does.

**5. Fix.** Decide the rule *before* doing the arithmetic that can wrap. Check for the full row first:

```python
def symbols_to_draw_fixed(level_counter):
    if level_counter >= 6:             # level 7 and later: full row
        return 7
    return level_counter + 1           # levels 1-6: one symbol per level
```

The fixed version has no byte arithmetic in the path that matters and no loop that can run away. It's also shorter, which is common. Many bugs live in code that was more clever than it needed to be.

**6. Guard.** The test from step 1 now passes. Add one more for the exact boundary, so a future edit can't bring the bug back quietly:

```python
def test_last_level_boundary():
    assert symbols_to_draw_fixed(255) == 7
    assert symbols_to_draw_fixed(5) == 6
    assert symbols_to_draw_fixed(6) == 7
```

### The visual

The interactive shows a step-through debugger on the Python model. The left pane shows the source with the current line highlighted. The right pane is a watch list showing `level_counter`, `level_counter + 1`, `count` and `drawn`, each also shown as eight bits. Under both is a fruit row drawn into a small maze grid. A slider picks the level from 250 to 256, and Step, Run and Reset buttons drive execution.

At level 255 the bits of `level_counter + 1` read `11111111` and the row fills to 7 and stops. Move to 256 and step once. The ninth bit has nowhere to go, the watch shows `count = 0`, and when you press Run the symbols march out of the fruit row and across the right half of the grid. Those are two views of one fact. The number wraps in the watch pane, and the loop runs away in the picture.

### Cross-game recognition

**Donkey Kong (Nintendo arcade, 1981).** The famous kill screen at level 22 has the same cause. The game computes the stage's bonus timer, which is also its time limit, in an 8-bit register. Ars Technica's account of the 2025 clear explains that at level 22 the calculation overflows past 256 and wraps down to 4. The player gets a few seconds instead of a normal time limit and dies before reaching the top. Same model, one byte and a wrap, with a timer instead of a fruit row.

**Civilization (MicroProse, 1991), a bug that never existed.** For years the internet repeated that the original game's peaceful Gandhi became a nuclear warmonger because his aggression score of 1 dropped by 2 under democracy and wrapped to 255. It's a perfect story in this lecture's model. It's also false. Sid Meier wrote in his 2020 memoir that the bug could not have happened in the original game, and Civilization V (2010) is where Gandhi was deliberately given a high nuclear tendency. The lesson for debugging is step 1. A story that fits your model perfectly is still not a reproduction. Believe the run, not the story.

**Godot 4 (GDScript `int`, current versions).** GDScript integers are signed 64-bit, and the class reference says they wrap around past about 9.2 quintillion. So your Godot score counter won't hit the Pac-Man bug. But the moment you pack a value into a byte to save space, in a save file, a network packet ([CS202 week 5](../../CS202-networking-fundamentals-for-multiplayer-games/syllabus.md)) or a shader, you are back in 1980. MMO servers pack values this way constantly. Know how many bits every stored value has.

Three games, one idea. A value stored in `b` bits lives in a circle of `2^b` values, and any arithmetic near the edge of that circle needs a test.

### Eyes-open design judgment

- **Kill screens were not designed, but they became design.** Level 256 is part of Pac-Man's legend, and the Donkey Kong kill screen drives a whole competitive scene. That's luck, not a plan. In your game, an unreachable-level bug is a bug. Test your boundaries (level 1, the last level, the first level past any cap) on purpose.
- **Pick the tool by the question.** If you ask "what happened over time?", log. If you ask "what is true right now, in detail?", use a breakpoint. If you ask "what should I even look at?", explain the code to a duck. Switching tools after 15 minutes without progress is a better habit than staring harder.
- **Logs cost something.** A `print` inside a loop that runs 10,000 times per frame will tank your frame rate and bury the one line you need. Log at the event, not every frame, or guard the log with the same condition you'd use for a breakpoint.
- **Some bugs hide from breakpoints.** Timing bugs, such as a collision that only fails at 30 fps (week 10's tunneling), disappear when you pause the game, because pausing changes the timing. Log those with frame numbers instead.

## 3. Reading an error message

Many bugs arrive with a message, and students often skip it. A Python traceback lists the chain of calls that led to the error, oldest first, and the line that failed at the bottom:

```
Traceback (most recent call last):
  File "game.py", line 88, in <module>
    run()
  File "game.py", line 71, in run
    handle_collisions(world)
  File "game.py", line 42, in handle_collisions
    if aabb_overlap(player, enemy["box"]):
KeyError: 'box'
```

Read it from the bottom up. The last line names the kind of error (`KeyError`) and the value (`'box'`). The line above names the exact source line. The lines above that tell you who called it. Here some enemy dictionary has no `"box"` key. Your hypothesis should be about how that enemy was created, not about `aabb_overlap`, which never ran.

Godot's Debugger panel shows the same information in the Errors tab and the Stack Trace tab. The frame list there is Godot's version of the traceback.

## 4. Making bugs reproducible in games

Games are harder to debug than most programs because they depend on time, input and randomness. Three habits make a game bug reproducible:

1. **Seed your randomness.** `random.seed(42)` in Python, or a fixed `seed` on Godot's `RandomNumberGenerator`, gives the same "random" spawns every run. Week 13 builds on this. When a player reports a bug, the seed is the first thing to log.
2. **Record input.** If your update reads input from a list of recorded key presses instead of the keyboard, you can replay a bug exactly. CS102's Command pattern ([CS102 week 12](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md)) turns this into a full replay system.
3. **Fix the timestep.** A simulation that steps at a fixed 1/60 s gives the same result on every machine (week 9). Variable steps make bugs appear on one laptop and not another.

A reproducible bug is half fixed. A bug you can only trigger "sometimes, on Dan's machine" can eat a week.

## In-class activity (25 minutes)

Pairs. Each pair gets a printed copy of `lab12-starter/asteroids_sim.py` from the lab folder (a headless arcade simulation with planted bugs) and one rubber duck, eraser or coffee mug.

1. (8 min) Partner A explains `update_play()` to the duck, line by line, out loud. Partner B writes down every sentence where A says "this always..." or "this can't...". Those are the assumptions to test.
2. (10 min) Pick one assumption. Write a log line or a conditional breakpoint that would prove it false. Run the simulation with seed 7 and check.
3. (7 min) Swap roles on `handle_event()` and repeat step 1 only.

Expected output: a list of at least five assumptions, one of them tested with the evidence (a log excerpt or a screenshot of the debugger), and a one-sentence hypothesis if you found a bug.

## Common misconceptions

- **"The bug is where the error appears."** The error appears where the bad value is *used*. The bug is where it was *made*. Walk back up the traceback or the log.
- **"If the fix makes the symptom go away, it's fixed."** Only if you can say why the new code is right. Otherwise you've moved the bug. The regression test and the one-sentence hypothesis are your proof.
- **"Printing is for beginners; real programmers use debuggers."** Professionals use both. Logs show history, breakpoints show a moment. Timing bugs often need logs.
- **"Rubber-ducking is a joke."** It's a structured way to make your assumptions audible. The duck is optional. The out-loud, line-by-line part is not.

## Check yourself

1. A bug appears somewhere in the first 3,000 frames of a recorded replay. Each replay run to a chosen frame takes about 20 seconds. How many runs does bisecting need to find the first bad frame, and roughly how long does it take?
2. A wave counter is stored in one byte and the wave's enemy count is `3 + 2 × wave`. What enemy count does wave 256 get, and what does wave 257 get? Which test would have caught it?
3. In `symbols_to_draw`, suppose the byte were 16 bits (values 0 to 65,535) and levels were unlimited. At what level would the split-screen bug appear, and how many symbols would the loop draw?
4. A collision bug only happens when the frame rate drops. Your breakpoint in `handle_collisions` never catches it. Why not, and what do you do instead?

<details>
<summary>Answers</summary>

1. `2¹¹ = 2,048` and `2¹² = 4,096`, so about 12 runs. 12 × 20 s is about 4 minutes.
2. `byte(256) = 0`, so wave 256 gets `3 + 0 = 3` enemies, and wave 257 gets 5. The game suddenly becomes easy. A boundary test at the storage limit (`wave = 255` and `wave = 256`), or a test that asserts the enemy count never decreases, would catch it.
3. The counter wraps when `level_counter + 1 = 65,536`, that is `level_counter = 65,535`, which is level 65,536. The loop would start at 0 and draw 65,536 symbols.
4. Stopping at a breakpoint changes the timing, and the bug depends on large steps between frames. Log the positions and `delta` with the frame number, for example only when an object's step exceeds the wall thickness, then read the log after the run.

</details>

## Lab / assignment hook

[Lab 12, bug hunt](../labs/lab12.md). A headless arcade simulation with three planted bugs. For each one you write a failing test first, record the log line or breakpoint session that exposed it, write a one-sentence hypothesis, fix it, and keep the test. Deliverable: the fixed files, the tests, and a debugging journal of at most 400 words.

## Sources

- Pittman, J. (2009). "The Pac-Man Dossier", Game Developer (originally Gamasutra), February 2009. Level counter starts at zero and is one byte; the fruit routine's increment overflows 255 to 0; the loop runs 256 times and draws past the bonus symbol table over the right half of the maze. Original arcade Pac-Man (Namco, 1980). https://www.gamedeveloper.com/design/the-pac-man-dossier
- Orland, K. (2025). "Donkey Kong's famed kill screen has been cleared for the first time", Ars Technica, February 7, 2025. The 8-bit bonus timer calculation overflows past 256 and wraps to 4 at level 22 (original 1981 arcade game). https://arstechnica.com/gaming/2025/02/donkey-kongs-famed-kill-screen-has-been-cleared-for-the-first-time/
- Wikipedia, "Donkey Kong (1981 video game)", section "Bugs and exploits" (checked September 2026). Kill screen at the first stage of level 22.
- Meier, S. (2020). *Sid Meier's Memoir!: A Life in Computer Games*. W. W. Norton, pp. 261-266, as summarized in Wikipedia, "Nuclear Gandhi" (checked September 2026). The original Civilization (1991) bug is a legend; Civilization V (2010) gave Gandhi the nuclear behavior on purpose.
- Hunt, A. & Thomas, D. (1999). *The Pragmatic Programmer*. Addison-Wesley. Origin of the rubber duck anecdote, via Wikipedia, "Rubber duck debugging".
- Godot Engine documentation, "Debugger panel" (Godot 4 stable). Gutter breakpoints, the Stack Trace tab. "GDScript reference", the `breakpoint` keyword stored in the script. "int" class reference, signed 64-bit, wraps on overflow. https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html
- Python documentation, "pdb, the Python Debugger" and built-in `breakpoint()` (Python 3.7 and later). https://docs.python.org/3/library/pdb.html

## Interactive spec: examples/w12-level-256-debugger.html

**Purpose.** A tiny step-through debugger on the lecture's `symbols_to_draw` model. The one insight: at level 256, `level_counter + 1` needs a ninth bit, the byte keeps 0, and that one wrong value sends the loop from at most 7 iterations to 256.

**Layout.** Mobile-first. Three panes, stacked on phones, source and watch side by side above 900 px with the picture underneath.
1. Source pane: the Python model from section 2 (the `symbols_to_draw` function only), monospace, line numbers, current line highlighted. A red dot on the `count = byte(level_counter + 1)` line shows a breakpoint; clicking the gutter toggles breakpoints on any line.
2. Watch pane: rows for `level_counter`, `level_counter + 1` (unwrapped), `count`, `drawn`, and the branch taken. Each numeric row shows the decimal value and its 8-bit binary form; for `level_counter + 1` show 9 bits and grey out the ninth bit with a note "dropped by byte()". A row "loop iterations so far".
3. Picture pane: a 28 × 12 cell grid standing for the maze. The bottom row's right 7 cells are the fruit row. Each drawn symbol fills the next cell leftward along the fruit row; after 7 cells, further symbols continue into the maze cells above, row by row from the right half, in varied generic glyphs (letters, digits, simple shapes). No Pac-Man art or maze reproduction; a plain grid.

**Controls.**
- Level slider 250 to 256 (integer), default 255, plus quick buttons "1", "6", "7", "255", "256". `level_counter = level − 1`.
- Step (runs one source line), Run (runs to the next breakpoint or the end, animating symbols at about 30 per second, instant if `prefers-reduced-motion`), Reset.
- Toggle "fixed version" swaps the source pane to `symbols_to_draw_fixed` and reruns.
- A small bisect helper below: "Bisect levels 1-256" button that shows the probe table from the lecture filling in one row per click.

**Test values (must match).**
- Level 1: count 1, early branch, drawn 1. Level 6: count 6, drawn 6. Level 7: count 7, full branch, returns 7. Level 255: `level_counter = 254`, count 255, returns 7. Level 256: `level_counter = 255`, `level_counter + 1 = 256` = `1 0000 0000`, count 0, early branch, 256 iterations, drawn 256.
- Fixed version returns 7 for level 256 and 6 for level 6.
- Bisect helper: probes 128, 192, 224, 240, 248, 252, 254, 255, all good, first bad level 256, 8 probes.

**Accessibility.** Keyboard: N = step, C = run (continue), R = reset, slider with arrow keys. A live region announces the current line number and changed watch values. Colors from `templates/interactive-tokens.css`; binary digits and branch names are text, not only color. Works in light and dark schemes.
