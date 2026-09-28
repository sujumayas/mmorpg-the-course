# CS102 · Week 06 — Queues and Stacks: Undo and Command Buffers

**Why this matters:** Two of the most loved features in puzzle and tactics games, "undo" and "the game remembered what I pressed," are two tiny data structures. A stack gives you undo. A queue gives you input buffering. Getting either one slightly wrong produces bugs players describe as "the box teleported" or "my character kept walking after I let go," and both come down to which end of a collection you take from.

**You will be able to:**
- Implement a stack and a queue in Python with O(1) operations, and explain why `list.pop(0)` is the wrong queue.
- Build undo and redo with two stacks of command objects, and trace their contents through a sequence of moves.
- Compute the memory cost of snapshot undo versus command undo for a given history length.
- Choose an input-buffer length and predict, from a list of key-press times, which moves run and when.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "Command" chapter (sections "Undo and Redo" and "Classy and Dysfunctional?") and the "Event Queue" chapter, section "A ring buffer". Skim the "State" chapter section "Pushdown Automata".

**Prerequisites from earlier courses:** [CS102 week 4, Big-O intuition](w04-big-o-intuition-for-game-developers.md) (O(1) versus O(n), amortized cost). [CS102 week 5, arrays, linked lists and hash maps](w05-arrays-linked-lists-and-hash-maps.md) (why inserting at the front of a list is O(n)). [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md) (`append` and `pop`). [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md), for section 4's menu stack.

**Interactive:** [Undo stacks and input queue](../examples/w06-undo-stacks-and-input-queue.html). Keep it open during sections 2 and 3.

---

## 1. Two orders of service

A **stack** hands things back in the reverse order they went in. The last thing pushed is the first thing popped. This is **LIFO**, last in, first out. Think of a pile of plates.

A **queue** hands things back in the order they went in. The first thing added is the first thing removed. This is **FIFO**, first in, first out. Think of a line at a shop.

Both are restrictions of a list. You give up the ability to touch the middle, and in exchange every operation you do keep is O(1) and the order of service is guaranteed. That guarantee is the point. Undo must reverse the *most recent* action, not some action. A buffered input must run the *earliest* press first, or the character dances out of order.

### Stacks in Python

A Python list is already a good stack, as long as you only use its end.

```python
history = []
history.append("move right")    # push, amortized O(1)
history.append("push box")
last = history.pop()            # pop from the end, O(1) -> "push box"
top = history[-1]               # peek without removing -> "move right"
```

### Queues in Python, and the trap

The obvious queue is a list where you append at the end and remove with `pop(0)`. It gives the right answer and the wrong cost. As CS101 week 5 warned and week 5 of this course explained, removing the first element of a dynamic array shifts every other element left. Each `pop(0)` is O(n), so draining a queue of `n` items is O(n²).

The Python documentation says the same thing about lists in its description of `collections.deque`. Lists incur O(n) memory movement for `pop(0)` and `insert(0, v)`, while a deque supports appends and pops at either end with roughly O(1) cost. On the course reference machine (CPython 3.13, Apple silicon):

| Items drained from the front | `list.pop(0)` | `deque.popleft()` |
|---|---|---|
| 10,000 | 4.0 ms | 0.23 ms |
| 100,000 | 588 ms | 2.4 ms |

Ten times the items made the list version 147 times slower, the O(n²) signature. The deque grew 10×, which is linear, as it should be.

```python
from collections import deque

inputs = deque()
inputs.append("jump")          # enqueue at the back, O(1)
inputs.append("attack")
first = inputs.popleft()       # dequeue from the front, O(1) -> "jump"
```

A deque (pronounced "deck") is a **double-ended queue**. CPython builds it from linked blocks of slots, so it gets the linked list's O(1) at both ends without paying for one node object per item.

### Bounded versions

Games almost never want unlimited buffers. `deque(maxlen=k)` keeps at most `k` items. When it is full and you append on the right, the oldest item falls off the left. That one argument gives you a fixed-size undo history (section 2) and a short input buffer (section 3).

In engines without a deque, the usual bounded queue is a **ring buffer**, a fixed array with a head index and a tail index that wrap around to 0 when they reach the end. Nystrom's "Event Queue" chapter builds one for audio requests. It never allocates after startup and every operation is O(1), which is why it shows up in audio, networking and input code.

## 2. Worked example: undo in a box-pushing puzzle

### The hook

Puzzle and tactics games treat undo very differently, and players feel the difference immediately.

*Baba Is You* (2019) records every turn since the start of the level. You can step back through all of them. Its *New Adventures* level pack, added on 17 November 2021, goes further. It includes a rule word, BACK, that makes an object rewind through its own past positions one turn at a time, while the rest of the level carries on. The undo history isn't only a safety net there. It is a game object you can build puzzles from.

*Into the Breach* (2018) is stricter. You may undo your mechs' moves as often as you like, but only until a mech uses an ability such as a weapon or a repair. Separately, once per battle you may "Reset Turn," which returns every unit to where it stood at the start of the turn. One pilot, Isaac Jones, grants a second reset.

Two shipped games, two undo rules. Both are a stack. The design question is what goes on it and how deep it goes.

### The model

The **Command pattern** (Nystrom's "Command" chapter; [CS102 week 12](w12-command-pattern-input-replay-undo.md) covers it in full) turns each action into an object with two methods. `do(board)` performs the action and records whatever it needs to reverse it. `undo(board)` reverses it. With commands, undo and redo need two stacks:

```
run(cmd):   if cmd.do() succeeds: push cmd on UNDO;  clear REDO
undo():     cmd = pop UNDO;  cmd.undo();  push cmd on REDO
redo():     cmd = pop REDO;  cmd.do();    push cmd on UNDO
```

- `UNDO` holds actions you've done, most recent on top.
- `REDO` holds actions you've undone, most recently undone on top.
- **Clearing REDO on a new action** is the rule that keeps history a single line. Once you do something new after undoing, the old "future" no longer follows from the present, so it is discarded.

Here is the move command for a box-pushing puzzle, from `labs/lab06-starter/puzzle.py`. The board is a set of wall cells, a set of box cells and a player position.

```python
class Move:
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy
        self.pushed = False               # recorded by do(), used by undo()

    def do(self, board):
        px, py = board.player
        ahead = (px + self.dx, py + self.dy)
        if ahead in board.walls:
            return False                  # blocked: nothing happens, nothing recorded
        if ahead in board.boxes:
            beyond = (ahead[0] + self.dx, ahead[1] + self.dy)
            if not board.free(beyond):
                return False
            board.boxes.remove(ahead)
            board.boxes.add(beyond)
            self.pushed = True
        else:
            self.pushed = False
        board.player = ahead
        return True

    def undo(self, board):
        px, py = board.player
        if self.pushed:                   # pull the box back to where the player stands
            box = (px + self.dx, py + self.dy)
            board.boxes.remove(box)
            board.boxes.add((px, py))
        board.player = (px - self.dx, py - self.dy)
```

Notice `self.pushed`. A move to the right can mean "step right" or "step right and push a box." `undo` needs to know which, and only `do` knows, so `do` writes it down. This is the whole trick of command-based undo. **A command stores the smallest fact that makes its own reversal exact.**

The history uses a `deque` so it can be bounded:

```python
class History:
    def __init__(self, limit=None):
        self.undo_stack = deque(maxlen=limit)   # oldest falls off the bottom when full
        self.redo_stack = []

    def run(self, cmd, board):
        if cmd.do(board):
            self.undo_stack.append(cmd)
            self.redo_stack.clear()             # a new action ends the old future
            return True
        return False

    def undo(self, board):
        if not self.undo_stack:
            return False
        cmd = self.undo_stack.pop()
        cmd.undo(board)
        self.redo_stack.append(cmd)
        return True

    def redo(self, board):
        if not self.redo_stack:
            return False
        cmd = self.redo_stack.pop()
        cmd.do(board)
        self.undo_stack.append(cmd)
        return True
```

Note that a *blocked* move is never pushed. If walking into a wall went on the stack, the player would press undo and see nothing happen, which reads as a bug.

### Numbers you can check

The level is 7 × 5 with walls around the edge. The player starts at (2, 2) with a box at (3, 2). Coordinates are (x, y) with y growing downward. `R*` means "moved right and pushed a box." Run `python puzzle.py` after finishing the lab and you get exactly this trace:

| Step | Action | Player | Box | UNDO (bottom → top) | REDO (bottom → top) |
|---|---|---|---|---|---|
| 0 | start | (2, 2) | (3, 2) | — | — |
| 1 | run R | (3, 2) | (4, 2) | R* | — |
| 2 | run R | (4, 2) | (5, 2) | R*, R* | — |
| 3 | run D | (4, 3) | (5, 2) | R*, R*, D | — |
| 4 | undo | (4, 2) | (5, 2) | R*, R* | D |
| 5 | undo | (3, 2) | (4, 2) | R* | D, R* |
| 6 | redo | (4, 2) | (5, 2) | R*, R* | D |
| 7 | run U | (4, 1) | (5, 2) | R*, R*, U | — |

Trace it by hand before you look at the code. Three things to check:

- Step 5 undoes a push. The box moves back from (5, 2) to (4, 2) because the command remembered `pushed = True`.
- Step 6 redoes that push by calling `do` again. `do` re-checks the board, which is still in the same state it was before the original move, so it succeeds identically.
- Step 7 is a new action after an undo. The `D` waiting on REDO is gone. Pressing redo now does nothing.

### What undo costs in memory

The other common design is **snapshot undo**. Before each action you copy the whole state and push the copy. It is simpler to write, since there is no `undo` method to get wrong, but it stores far more. Compare storage after 1,000 moves on a 20 × 15 level (300 cells) with 6 boxes:

| Undo design | Stored per move | After 1,000 moves |
|---|---|---|
| Snapshot of every cell | 300 cells | 300,000 cells |
| Snapshot of moving parts only (player + 6 boxes) | 7 positions = 14 integers | 14,000 integers |
| Command (`dx`, `dy`, `pushed`) | 3 small values | 3,000 values |

Command undo is 100 times smaller than full snapshots here. In a small puzzle all three fit in memory without effort. The difference matters for a level editor with a large map, or for a game that must keep undo history in a save file.

A bounded history caps it. `History(limit=50)` keeps the 50 most recent commands, so memory stays at 150 values regardless of how long the player plays. The cost is a design one. Move 51 can't be undone.

### Seeing it move

Open the interactive. The left view is the puzzle board. Use arrow keys or the on-screen pad to move, `Z` to undo and `Y` to redo. The right view draws the two stacks as columns of labelled tiles, with the top of each stack at the top. Every action animates one tile moving between the columns or appearing on UNDO.

Play steps 1 to 6 of the table, then make a new move. The REDO column empties in one flash. That's the moment players lose a "future" they didn't know was being discarded. Then set the history limit to 3 and make five moves. Watch the bottom tile of UNDO fall off each time a new one lands on top.

### Cross-game recognition

**Baba Is You (2019; New Adventures pack, November 2021).** Unlimited undo is a stack with no `maxlen`, reaching back to the level's start. The BACK property reads the same history but applies it to one object instead of the whole world. The Baba Is You wiki notes that once a BACK object has rewound every turn since the level began, it stops. It has emptied its own stack.

**Into the Breach (2018).** Two stacks with different lifetimes. Undo Move behaves like our UNDO stack, except that using an ability clears it, the way a new action clears REDO in our code. Reset Turn is a one-entry snapshot stack. The game saves the state at the start of each turn and lets you restore it once per battle. The limit on that restore, not the data structure, is the design.

**Level editors and tools.** Nystrom's "Command" chapter observes that undo is expected in any tool used to build games, and that designers will resent a tool without it. Godot exposes the same idea to tool and game scripts as its `UndoRedo` class. You register an action's do and undo calls, commit it, and the class keeps the history. The pattern in your puzzle is the one in your tools.

**The call stack.** Every time a function calls another, Python pushes a frame holding the caller's local variables and pops it on return. That's why a recursive flood fill on a huge region can raise `RecursionError`. The stack is bounded, and each recursive call is a push. [Week 8](w08-graphs-maps-and-dialogue.md) meets the same limit in depth-first search, and the fix there is an explicit stack like the one in this lecture.

Different games, one mechanism. Undo is "reverse the most recent thing," and the most recent thing is the top of a stack.

### Eyes-open design judgment

- **Unlimited undo changes what a puzzle is.** With free undo, a puzzle tests whether you can *find* a solution, not whether you can *execute* one without slipping. That's why Baba Is You can have puzzles with long, precise solutions. If execution under pressure is part of your challenge, undo removes it.
- **Limited undo is a resource.** Into the Breach's single Reset Turn turns undo into a decision. Spend it on this mistake or save it. A bounded stack can be a design tool as well as a memory limit.
- **Undo exposes hidden information and randomness.** If an attack rolls a hit chance, undo lets players reroll until it hits. Either make actions deterministic, fix the random seed per turn so the redo gives the same result, or block undo past any random event, the way Into the Breach blocks undo once an ability is used.
- **Choose commands or snapshots deliberately.** Commands are small but every command needs a correct `undo`, and one wrong `undo` corrupts every state below it on the stack. Snapshots are larger but can't be wrong in that way. Many tools use commands and take an occasional snapshot as a checkpoint.
- **Multiplayer changes everything.** You can't undo an action another player has already seen. Undo is a single-player or turn-local luxury unless the whole game is designed to rewind and replay state. [CS202 week 9, server reconciliation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md), and [CS202 week 11, lag compensation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md), do exactly that.

### Check yourself on the worked example

1. Starting from step 7 of the table, the player presses undo three times. Give the player's position, the box's position, and both stacks after each press.
2. A designer wants "undo goes back 20 moves." Which line of code changes, and what happens on move 21?
3. Why does `Move.undo` compute the box's position from the player's *current* position rather than storing the box's old position?

<details>
<summary>Answers</summary>

1. Undo U: player (4, 2), box (5, 2), UNDO `R*, R*`, REDO `U`. Undo R*: player (3, 2), box (4, 2), UNDO `R*`, REDO `U, R*`. Undo R*: player (2, 2), box (3, 2), UNDO empty, REDO `U, R*, R*`. You are back at the start.
2. `History(limit=20)`, which sets `deque(maxlen=20)`. On move 21 the oldest command falls off the bottom, so the starting position can no longer be reached by undo.
3. After `do`, the box is always exactly one step ahead of the player in the move's direction. So the command needs only `pushed`, not a coordinate. Storing less means less to get wrong and less memory.

</details>

## 3. Command buffers: a queue between the player and the game

### The problem

In a grid game, one move plays an animation that lasts, say, 150 ms. A player who taps right five times quickly, at 0, 40, 80, 120 and 160 ms, has pressed faster than the character can move. The game has three choices. It can ignore presses that arrive mid-move, remember all of them, or remember a few. Each is a queue with a different `maxlen`.

The **input buffer** is a queue of commands. A key press enqueues a command. Whenever the current move finishes, the game dequeues the front command and starts it. FIFO order matters. If the player tapped right, then up, the character must go right first.

### The model and the numbers

`labs/lab06-starter/puzzle.py` has an `InputBuffer` class and a `simulate_buffer(taps, step_ms, maxlen)` function that returns when each move starts. With `step_ms = 150` and taps at `[0, 40, 80, 120, 160]`:

| Buffer (`maxlen`) | Moves that start (ms) | Moves made | Character stops at | Time after last tap |
|---|---|---|---|---|
| unlimited | 0, 150, 300, 450, 600 | 5 | 750 ms | 590 ms |
| 2 | 0, 150, 300, 450 | 4 | 600 ms | 440 ms |
| 1 | 0, 150, 300 | 3 | 450 ms | 290 ms |
| 0 (no buffer) | 0, 160 | 2 | 310 ms | 150 ms |

Read the rows as feel, not as numbers:

- **Unlimited** obeys every press, but the character is still walking more than half a second after the player's thumb has left the key. Players describe this as slidey or unresponsive, even though the game did exactly what they typed.
- **No buffer** stops fast, but it swallowed three of the five presses. The press at 160 ms only counted because the first move had just finished at 150. Players describe this as dropped inputs.
- **One or two** is the usual compromise. The press you made just before a move ended still counts, and extra mashing is discarded.

With `deque(maxlen=k)`, a full buffer drops the *oldest* waiting press when a new one arrives. That keeps the player's most recent intent, which is usually what you want for movement. For a combo input, dropping the newest might be better. Decide on purpose.

### Queues on the server

The same structure sits on the other side of the network. A game server receives commands from many players, queues them, and processes them in order each tick. When the work arriving per second exceeds what the server can process, the queue grows. CCP's 2011 blog post introducing Time Dilation for EVE Online describes exactly this. In big fleet fights the server's queue of waiting work grew so long that events such as a ship's destruction stretched over many minutes. Slowing the game clock let the queue drain at the rate work was arriving. Week 4 looked at why the work grows. The queue is where you see it pile up.

## 4. Stacks of screens: the pushdown automaton

CS101 week 11 built a state machine for menu, play, pause and game over. Menus in real games nest. From play you open the inventory, from the inventory you open an item's details, and "back" should return you to the inventory, not to play.

A plain state machine has one current state, so "back" doesn't know where it came from. Nystrom's "State" chapter describes the fix, which automata theory calls a **pushdown automaton**. Keep a *stack* of states. The top one is active. Opening a screen pushes it, and "back" pops it.

```python
screens = ["play"]
screens.append("inventory")    # open inventory
screens.append("item_detail")  # open an item
screens.pop()                  # back -> inventory is active again
current = screens[-1]          # "inventory"
```

Nystrom's example is a character that fires a weapon from any state and then returns to whatever it was doing. Push "firing," pop it when done. The same pattern handles a pause menu over any screen, or a dialogue box that can open over combat or exploration. When you write the state machines of [week 11](w11-state-and-state-machines.md), reach for a stack whenever "go back" should mean "go back to where I was."

## In-class activity (25 minutes)

In pairs, with `labs/lab06-starter/`.

1. On paper, trace this script from the lecture's starting board: run R, run R, undo, run D, undo, redo, redo. Record player, box and both stacks after each step. One of the `redo` presses does nothing. Say which one and why.
2. Run the same script in code (after finishing `History.undo` and `redo` in the lab, or with the instructor's solution) and compare with your trace.
3. Change the tap times to `[0, 100, 200, 300]` with `step_ms = 150`. Before running, predict the start times for `maxlen = 1` and `maxlen = 0`. Then run `simulate_buffer` and check.
4. Decide one buffer length for a turn-based tactics game and one for a fast grid-based action game. Justify each in one sentence with a number from step 3 or the lecture table.

Expected output: a trace table, a note on which `redo` fails, two predicted and actual start-time lists, and two one-sentence design decisions.

## Common misconceptions

- **"A list works fine as a queue."** It gives correct results, but each `pop(0)` shifts the whole list. Draining 100,000 items took 588 ms with `pop(0)` and 2.4 ms with `deque.popleft()`.
- **"Redo should survive a new action."** If it did, redoing an old command on a changed board could push a box through a wall or move the player from a position they aren't in. Clearing REDO keeps every stored command valid for the state it will run against.
- **"Undo is easy, just reverse the move."** Only if `do` recorded everything the reversal needs. A move that pushed a box and a move that didn't look identical until you store `pushed`.
- **"A bigger input buffer is more responsive."** It is more *obedient*. Past one or two entries it makes the character keep acting after the player stops, which feels less responsive.

## Check yourself

1. You push A, B, C onto a stack and enqueue A, B, C into a queue. Then you remove two items from each. What remains in each?
2. A level editor uses snapshot undo on a 256 × 256 tile map, with 2 bytes per tile, and keeps 200 undo steps. How much memory does history use? How much would 200 command records of 16 bytes each use?
3. With `step_ms = 200`, `maxlen = 1` and taps at `[0, 50, 100, 250]`, when does each move start, and when does the character stop?
4. A tactics game lets players undo attacks, and attacks have a 70% hit chance rolled when the attack happens. Describe the exploit and give two fixes.
5. Why is the inventory → item detail → back behaviour a stack and not a queue?

<details>
<summary>Answers</summary>

1. Stack: removing two gives C then B, so A remains. Queue: removing two gives A then B, so C remains.
2. One snapshot is `256 × 256 × 2 = 131,072` bytes (128 KiB). 200 snapshots are 26,214,400 bytes, 25 MiB. 200 commands are 3,200 bytes. The command history is 8,192 times smaller.
3. Tap 0 starts at once (busy until 200). Taps 50 and 100 arrive while busy; with `maxlen = 1`, 100 replaces 50. At 200 the waiting press starts (busy until 400). Tap 250 waits. At 400 it starts (busy until 600). Starts at 0, 200, 400. The character stops at 600 ms.
4. Players attack, and undo if the attack missed, repeating until it hits, so the effective hit chance becomes 100%. Fixes include rolling from a per-turn seed so a retried attack gives the same result, or making attacks unundoable (clearing the undo stack when an attack resolves).
5. "Back" must return to the most recently opened screen, which is last in, first out. A queue would return to the oldest screen, which here is "play."

</details>

## Lab / assignment hook

[Lab 06, undo and the input buffer](../labs/lab06.md). You finish `History.undo`, `History.redo` and the redo-clearing rule, implement `InputBuffer`, pass the provided checks in `test_puzzle.py`, then add a bounded history and a playtest-style comparison of buffer lengths. The Command pattern project in week 12 builds on this code.

## Sources

- Wikipedia, "Baba Is You" (current). Released 13 March 2019 for PC and Nintendo Switch. https://en.wikipedia.org/wiki/Baba_Is_You
- Baba Is You Wiki, "BACK" (current, Fandom). BACK rewinds an object through its past positions and stops after rewinding every turn since the level started; appears in New Adventures. https://babaiswiki.fandom.com/wiki/BACK
- Baba Is You Wiki, "New Adventures" (current, Fandom). Official level pack added 17 November 2021. https://babaiswiki.fandom.com/wiki/New_Adventures
- Baba Is You Wiki, "Infinite Loop" (current, Fandom). The player's options of undo or restart. https://babaiswiki.fandom.com/wiki/Infinite_Loop
- Into the Breach Wiki, "Into the Breach" (current, Fandom). Released 27 February 2018 on Windows, Mac and Linux. https://intothebreach.fandom.com/wiki/Into_the_Breach
- Into the Breach Wiki, "Reset Turn" (current, Fandom). Once per battle; Isaac Jones's ability grants a second reset. https://intothebreach.fandom.com/wiki/Reset_Turn
- Into the Breach Wiki, "Tips and tricks" (current, Fandom). Moves can be undone freely until a weapon or repair is used. https://intothebreach.fandom.com/wiki/Tips_and_tricks
- Nystrom, R. (2014). *Game Programming Patterns*. "Command" (undo and redo, undo in editors), "Event Queue" (ring buffer), "State" (pushdown automata). https://gameprogrammingpatterns.com/
- Godot Engine documentation, "UndoRedo" class reference (stable, Godot 4). Actions registered with do and undo methods, then committed. https://docs.godotengine.org/en/stable/classes/class_undoredo.html
- Python Software Foundation, "collections: Container datatypes", Python 3 documentation. Deque appends and pops at either end in about O(1); lists incur O(n) memory movement for `pop(0)` and `insert(0, v)`; `maxlen` bounds. https://docs.python.org/3/library/collections.html
- CCP Veritas, "Introducing Time Dilation (TiDi)", EVE Online developer blog, 22 April 2011. Server work backlog in large fights stretching ship death over minutes. https://www.eveonline.com/news/view/introducing-time-dilation-tidi
- Timings and traces in this lecture: `labs/lab06-starter/puzzle.py` and a small benchmark script, CPython 3.13.5 on an Apple silicon laptop, September 2026.

## Interactive spec: examples/w06-undo-stacks-and-input-queue.html

**The one insight:** undo and redo are two stacks, and a new action after an undo empties the redo stack in one step; an input buffer is a queue whose length decides whether the game drops presses or keeps moving after the player stops.

**Tab 1, "Undo stacks" (two linked views, stacked on mobile, side by side at ≥ 900px):**

- Left: the 7 × 5 board from the lecture. Walls on the border, player at (2, 2), box at (3, 2). Cells drawn as squares; player a circle, box a square with an outline. Generic shapes only.
- Right: two columns labelled UNDO and REDO, bottom-aligned, each tile showing the command label (`R`, `L`, `U`, `D`, with `*` for a push). Top tile of each column highlighted.
- Controls: arrow keys and an on-screen 4-button pad; buttons Undo (`Z`) and Redo (`Y`), disabled when their stack is empty; "History limit" select: unlimited (default), 3, 5, 10; "Reset level"; "Play lecture script" which runs steps 1 to 7 of the lecture table with a 600 ms pause between steps (instant under reduced motion).
- Behaviour: exactly the lecture's `Move.do`, `Move.undo` and `History` logic. A blocked move does nothing and pushes nothing (flash the wall cell). When a new move clears a non-empty REDO, flash the REDO column and show "REDO cleared (N commands discarded)" for 2 s. With a limit, when UNDO is full the bottom tile is removed as the new one is added, with the note "oldest command dropped".
- Readout table under the board, one row per action: step, action, player, box, UNDO, REDO, matching the lecture's trace format.
- Test: "Play lecture script" must produce the lecture table rows 1 to 7 exactly (player (4, 1), box (5, 2), UNDO `R*, R*, U`, REDO empty at the end).

**Tab 2, "Input buffer":**

- A timeline 0 to 1,000 ms. Top lane: key presses as ticks. Bottom lane: executed moves as bars of length `step_ms`. Presses that were dropped are drawn hollow with a strike; presses that waited are joined to their move bar by a line.
- Controls: `step_ms` slider 50 to 300 (default 150); `maxlen` select: unlimited, 2, 1 (default), 0; tap-time preset select: lecture `[0, 40, 80, 120, 160]` (default), even `[0, 100, 200, 300]`, check-yourself `[0, 50, 100, 250]` with `step_ms` 200; a "Tap" button (and Space key) that records live presses relative to the first tap, capped at 12 taps and 1,000 ms.
- Algorithm (exact): process presses in time order. Before handling a press at time `t`, while the queue is non-empty and `busy_until ≤ t`, dequeue the front and start a move at `busy_until` (`busy_until += step_ms`). Then, if `t ≥ busy_until` and the queue is empty, start a move at `t` (`busy_until = t + step_ms`); otherwise append `t` to a queue bounded at `maxlen`, dropping the oldest waiting press when full (`maxlen = 0` drops every press made while busy). After the last press, drain the queue the same way.
- Readouts: move start times, moves made, stop time, "time after last tap".
- Test values: lecture preset with `step_ms = 150` gives starts `[0,150,300,450,600]` / stop 750 (unlimited), `[0,150,300,450]` / 600 (2), `[0,150,300]` / 450 (1), `[0,160]` / 310 (0). Check-yourself preset with `step_ms = 200`, `maxlen = 1` gives `[0,200,400]` / 600.

**First screen:** Tab 1 with the lecture script already played to step 6 (UNDO `R*, R*`, REDO `D`) and a prompt "make any move to see what happens to REDO".

**Accessibility:** all controls keyboard operable, arrow keys only captured when the board has focus; stack changes announced through `aria-live="polite"` ("Undo: R*. Redo stack now D, R*"); respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. No game art, characters or logos.
