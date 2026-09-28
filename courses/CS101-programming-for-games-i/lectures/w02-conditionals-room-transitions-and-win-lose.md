# CS101 · Week 02 — Conditionals: Room Transitions and Win/Lose

**Why this matters:** A game is a machine that makes decisions. Which room you enter, whether a door opens, who wins. Every one of those is an `if` statement, and the order you write them in is a design decision. Get it wrong and the game hands a victory to the wrong player on the one frame that decides a tournament.

**You will be able to:**
- Write `if`, `elif` and `else` chains that move a player between rooms based on a typed command.
- Evaluate boolean expressions with `==`, `!=`, `<`, `<=`, `and`, `or` and `not` by hand.
- Enumerate every case of a win/lose check with a truth table and find the case a chain handles wrongly.
- Choose between `==` and `<=` for threshold checks and justify the choice.

**Before class:** Python Tutorial (docs.python.org), section 4.1 "if Statements". FIDE *Laws of Chess* (effective 1 January 2023), Article 5, "The completion of the game" (one page). Reread your week 1 state program.

**Prerequisites from earlier courses:** [CS101 week 1, programs, variables and types](w01-programs-variables-and-types.md) (variables, `bool`, `input()` returns a string). [GD101 week 2, players, objectives, procedures, rules](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md) and [GD101 week 3, resources, conflict, boundaries, outcome](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md), which define the outcome rules this lecture turns into code.

**Interactive:** [Who wins the tie?](../examples/w02-win-lose-order.html). Keep it open during section 3.

---

## 1. Questions with yes-or-no answers

Last week every line of your program ran, top to bottom, every time. A game needs to run some lines only sometimes. The tool for that is a **condition**, an expression whose value is `True` or `False`.

Comparison operators build conditions:

| Operator | Means | Example | Value when `hp = 0` |
|---|---|---|---|
| `==` | equal to | `hp == 0` | `True` |
| `!=` | not equal to | `hp != 0` | `False` |
| `<` | less than | `hp < 0` | `False` |
| `<=` | less than or equal to | `hp <= 0` | `True` |
| `>` | greater than | `hp > 0` | `False` |
| `>=` | greater than or equal to | `hp >= 100` | `False` |

Watch the difference between `=` and `==`. One `=` assigns a value (week 1). Two `==` asks whether two values are equal. Writing `if hp = 0:` is a syntax error in Python, which is a kindness. In some languages it silently sets `hp` to zero.

Strings compare too. `command == "north"` is `True` only if the text matches exactly, including case. `"North" == "north"` is `False`. That is why text games usually normalise input first with `command = input("> ").strip().lower()`, which removes stray spaces and lowercases everything.

### Combining conditions

Three **logical operators** combine conditions:

- `a and b` is `True` only when both are `True`.
- `a or b` is `True` when at least one is `True`.
- `not a` flips `True` and `False`.

A **truth table** lists every combination of inputs and the result. With two inputs there are exactly four rows:

| `has_key` | `door_locked` | `has_key or not door_locked` (can open) |
|---|---|---|
| False | False | True |
| False | True | False |
| True | False | True |
| True | True | True |

Python evaluates `not` first, then `and`, then `or`, the way multiplication comes before addition. `True or False and False` is `True`, because the `and` part runs first. When in doubt, add brackets. `(room == "hall") and has_key` reads the same to Python and better to humans.

## 2. `if`, `elif`, `else`: moving between rooms

An `if` statement runs its indented block only when the condition is `True`:

```python
if lamp_oil <= 0:
    lamp_lit = False
    print("Your lamp sputters out.")
```

The colon and the indentation are part of the syntax. Python uses indentation (four spaces by convention) to know which lines belong to the `if`. Line up the block carefully. A line indented by the wrong amount either belongs to the wrong block or raises `IndentationError`.

Add `else` for what happens otherwise, and `elif` ("else if") for more branches. Python checks the conditions from the top and runs **only the first branch whose condition is true**. Every later branch is skipped, even if its condition is also true. Hold on to that sentence. The worked example is built on it.

Here is a three-room cave. The state is one string, the current room. The player's command decides the next room.

```python
room = "entrance"
command = input("> ").strip().lower()

if room == "entrance" and command == "north":
    room = "hall"
elif room == "hall" and command == "south":
    room = "entrance"
elif room == "hall" and command == "east":
    room = "vault"
elif room == "vault" and command == "west":
    room = "hall"
else:
    print("You can't go that way.")

print(f"You are in the {room}.")
```

Draw it before you code it. Each room is a box and each legal command is a labelled arrow. Every arrow becomes one `elif`. The `else` catches everything without an arrow, including typos. Without that `else`, a typo would do nothing silently, and players read silence as a bug.

### Nested conditions and locked doors

A locked vault needs a second decision inside the first:

```python
has_key = False

if room == "hall" and command == "east":
    if has_key:
        room = "vault"
        print("The key turns. The vault door swings open.")
    else:
        print("The vault door is locked.")
```

This works, but nesting gets hard to read after two or three levels. Often you can flatten it by putting the more specific case first:

```python
if room == "hall" and command == "east" and has_key:
    room = "vault"
elif room == "hall" and command == "east":
    print("The vault door is locked.")
```

Both versions do the same thing. The second only works because the more specific branch comes first. Swap the two branches and the locked message shows even when the player has the key, because the general branch matches first and the specific one never gets a turn.

That swap is the whole of today's bug.

## 3. Worked example: who wins when both fall on the same frame?

### The hook

In the Super Smash Bros. series, a timed match can end in a tie, and so can an untimed stock match. The SmashWiki documents that when all remaining fighters lose their last stock on the same frame, the game goes to Sudden Death. Every tied fighter comes back with one stock at 300% damage, so almost any hit knocks them out.

Someone at Nintendo had to decide that both players falling at once is a separate case. In a two-player game there are two ways to lose, which means four situations. Code that forgets one of them still runs. It just gives the wrong answer, once in a few hundred matches, usually in the one match someone recorded.

### The model

Name one boolean per way to lose:

```python
p1_out = p1_hp <= 0
p2_out = p2_hp <= 0
```

- `p1_hp` and `p2_hp` are the players' health after this frame's damage has been applied.
- `p1_out` is `True` when player 1 has no health left.

Two booleans give `2 × 2 = 4` cases. In general, `k` independent conditions give `2^k` cases. An `if`/`elif` chain checks branches in order and runs the first true one. So:

> **A chain is correct only if every case reaches the branch meant for it, which means a case that makes several conditions true must be tested before any of them alone.**

Here is the chain most people write first. It checks for a winner in the obvious way.

```python
# Naive version
if p2_hp <= 0:
    result = "P1 wins"
elif p1_hp <= 0:
    result = "P2 wins"
else:
    result = "keep playing"
```

And here is the chain that handles all four cases:

```python
# Correct version
p1_out = p1_hp <= 0
p2_out = p2_hp <= 0

if p1_out and p2_out:
    result = "sudden death"
elif p2_out:
    result = "P1 wins"
elif p1_out:
    result = "P2 wins"
else:
    result = "keep playing"
```

### Numbers you can check

The table runs both chains, plus a third variant that uses `==` instead of `<=`, on six frames. Negative health appears because damage is subtracted in one step. A 12-damage hit on a player with 10 health leaves −2. That is called **overkill**.

| `p1_hp` | `p2_hp` | Case | Naive chain | Correct chain | `== 0` chain |
|---|---|---|---|---|---|
| 30 | 20 | neither out | keep playing | keep playing | keep playing |
| 30 | 0 | P2 out | P1 wins | P1 wins | P1 wins |
| 0 | 20 | P1 out | P2 wins | P2 wins | P2 wins |
| 0 | 0 | both out | **P1 wins** | sudden death | sudden death |
| −5 | −12 | both out, overkill | **P1 wins** | sudden death | **keep playing** |
| 30 | −4 | P2 out, overkill | P1 wins | P1 wins | **keep playing** |

Trace row 4 through the naive chain yourself. `p2_hp <= 0` is `True`, so the first branch runs and prints "P1 wins". The `elif p1_hp <= 0` is never checked. Player 1 was knocked out too, and the code never looked.

Rows 5 and 6 show the second bug. With `== 0`, overkill slips past every branch. The match continues with a player on −4 health, a zombie who can still act. Use `<=` for "has run out" whenever a value can jump past the threshold in one step.

Here is a short program that prints the table, so you can check it on your own machine:

```python
frames = [(30, 20), (30, 0), (0, 20), (0, 0), (-5, -12), (30, -4)]

for p1_hp, p2_hp in frames:
    p1_out = p1_hp <= 0
    p2_out = p2_hp <= 0
    if p1_out and p2_out:
        result = "sudden death"
    elif p2_out:
        result = "P1 wins"
    elif p1_out:
        result = "P2 wins"
    else:
        result = "keep playing"
    print(p1_hp, p2_hp, result)
```

(The `for` line repeats the block once for each pair. Week 3 covers loops.)

### The visual

Open `examples/w02-win-lose-order.html`. The left view is the code. It shows the chain's branches as cards you can drag by the handle, or focus and move with Alt+Up and Alt+Down, into any order. Two buttons jump to the "Naive order" and "Most specific first". Two health sliders set `p1_hp` and `p2_hp` from −20 to 50, and a toggle switches every test between `<=` and `==`. The branch that fires lights up, and the branches that were never checked are greyed out.

The right view is the truth. It lists the six frames from the table above, and each row shows the intended result next to what the current chain answers, in red where they disagree. Click a row to load it into the sliders. With the naive order the two "both out" rows are red. Drag the `and` branch to the top and they turn green. Now switch to `==` and watch the two overkill rows go red. The left view looks reasonable in every order. The right view shows which order is wrong.

### Cross-game recognition

**Chess (FIDE Laws of Chess, in force from 1 January 2023).** Article 5 says a player who checkmates the opponent's king wins, and a game is drawn when the player to move has no legal move and is not in check. Both situations start with "no legal moves". The in-check condition separates a win from a draw. Written as code:

```python
if no_legal_moves and in_check:
    result = "checkmate"
elif no_legal_moves:
    result = "stalemate: draw"
```

Put the `elif no_legal_moves` line first and every checkmate becomes a draw. It is the locked-door bug from section 2 with higher stakes.

**Tetris (Tetris Guideline games).** TetrisWiki lists several separate ways to top out. Block out happens when a new piece spawns overlapping blocks already in the field. Lock out happens when a piece locks entirely above the visible field. Partial lock out happens when a piece locks partly above it, even if it would clear a line. Garbage out happens when incoming garbage lines push blocks out of bounds. Each game in the Guideline family uses some combination. Here the conditions join with `or`, because any one ends the game:

```python
game_over = block_out or lock_out or garbage_out
```

The design question moves from "which order?" to "which conditions are in the list?". A game that includes partial lock out ends your run even on the move that would have cleared the line. One that leaves it out lets you survive it. The same truth-table habit, listing every case, is how you notice the difference.

**Super Smash Bros., again.** Sudden Death is Nintendo's answer to the "both out" row. A designer could just as well declare a draw, replay the round, or give it to whoever had more health at the start of the frame. There is no single correct result. There is only a result you chose deliberately, or one your `elif` order chose for you.

### Design judgment

- **List the cases before writing the chain.** For `k` conditions, write the `2^k` rows. Two conditions give 4 rows, three give 8. If you cannot list them, the design is not finished.
- **Most specific first.** Branches that require several conditions go above branches that require one of them. The `and` case sits on top.
- **Name the tie policy in the design document.** Draw, sudden death, attacker wins, defender wins, or host wins. Each is a real choice with a feel. "Whoever the code checked first" is not a policy.
- **Use `<=` for "ran out" and `>=` for "reached".** Values jump. Damage overshoots, gold jumps by 50, and scores skip. `==` only catches the exact value.
- **Decide when you check.** Resolve all damage for the frame, then check win/lose once. If you check after each hit, the player hit first always loses the tie. That may be the rule you want, but write it down.

### Check yourself (worked example)

1. A three-player free-for-all has booleans `a_out`, `b_out`, `c_out`. How many cases are there? How many of them should end the match with exactly one winner?
2. A designer writes `if p1_hp <= 0: result = "P2 wins"` followed by `elif p2_hp <= 0: result = "P1 wins"`. Which tie does this code resolve, and in whose favour?
3. Rewrite the chess snippet so the `elif` comes first, then give a position type where it returns the wrong answer.

<details>
<summary>Answers</summary>

1. `2^3 = 8` cases. Exactly one winner means exactly two players out, which happens in 3 cases. (One case has nobody out, 3 have one out, 3 have two out, and 1 has all three out, which needs a tie rule.)
2. When both are at or below 0, the first branch fires, so player 2 wins every tie. It is the mirror image of the naive chain.
3. `if no_legal_moves: result = "stalemate: draw"` then `elif no_legal_moves and in_check: result = "checkmate"`. Every checkmate (no legal moves and in check) matches the first branch and is scored as a draw.

</details>

## 4. Win, lose and "nothing happened"

Most game states are not wins or losses. Your chains should make the "nothing happened" path boring and explicit. A common structure for a text adventure turn is:

```python
# 1. Read the command
command = input("> ").strip().lower()

# 2. Change the state (movement, items)
if room == "hall" and command == "take lamp" and not has_lamp:
    has_lamp = True
    print("You take the lamp.")
elif command == "take lamp":
    print("There is no lamp here.")

# 3. Check the outcome, once, after all changes
if room == "vault" and has_treasure:
    print("You escape with the treasure. You win!")
elif lamp_oil <= 0 and room != "entrance":
    print("Darkness. You are lost. Game over.")
else:
    print(f"You are in the {room}.")
```

Notice the order inside step 3. If the lamp runs out on the very turn you reach the vault with the treasure, you win. That is a design choice encoded by putting the win check first. Swap them and the same turn ends in darkness. Neither is wrong, but only one is what you meant.

Keeping the three steps separate (read, change, check) will matter next week. Wrap them in a loop and you have a game loop.

## 5. Readable conditions

A few habits make conditions easier to get right:

- **Name conditions with booleans.** `p1_out = p1_hp <= 0` then `if p1_out and p2_out:` reads like the design document.
- **Avoid double negatives.** `if not door_unlocked` is harder to read than `if door_locked`. Pick the name that makes the common test positive.
- **Compare with the right type.** `input()` returns a string, so `if choice == 1` is always `False` when the player typed `1`. Compare with `"1"` or convert first with `int()`.
- **Check your `else`.** Ask of every chain, "what reaches the `else`, and is that all right?"

## In-class activity (25 min)

In groups of three.

1. **Case table (10 min).** Pick a two-player game you know (a fighting game, a racing game with a finish line, a card game). Name two or three ways the match can end, as booleans. Write the full truth table and fill in the outcome you want for every row, including ties.
2. **Chain (10 min).** Write the `if`/`elif`/`else` chain in Python and test it on every row. Use `<=` or `>=` wherever a value can jump past its threshold.
3. **Break it (5 min).** Give your chain to another group without the table. They try to find an input where it gives an answer you did not intend.

Expected output: one truth table with a tie policy, a chain that passes every row, and a note of what the other group tried.

## Common misconceptions

- **"`elif` checks every condition and runs all true ones."** Only the first true branch runs. Later branches are skipped even if they are true.
- **"`if hp == 0` detects death."** Only if health lands on exactly 0. Overkill skips past it. Use `hp <= 0`.
- **"The order of `elif` branches is a style choice."** When conditions overlap, order changes results. Most specific first.
- **"`if choice == 1` works with `input()`."** `input()` returns the string `"1"`, which is not equal to the integer `1`.

## Check yourself

1. What does this print when `gold = 50`? `if gold >= 100: print("rich")`, `elif gold >= 20: print("comfortable")`, `elif gold >= 50: print("exactly fifty")`, `else: print("poor")`.
2. Evaluate `not has_key or door_open and room == "hall"` when `has_key = True`, `door_open = True`, `room = "vault"`.
3. A race ends when a car crosses `x >= 1000`. Both cars cross in the same frame, at `x = 1004` and `x = 1011`. Write a chain that awards the win to the car that got further, and says "dead heat" if they are exactly equal.
4. A dungeon has three rooms in a line, west, middle and east. Players type `east` or `west`. How many `elif` branches does a movement chain need (not counting `else`)? Write them.

<details>
<summary>Answers</summary>

1. `comfortable`. `50 >= 20` is the first true branch. The `>= 50` branch is never reached, so it should go above `>= 20` or be removed.
2. `not has_key` is `False`. `door_open and room == "hall"` is `True and False`, which is `False`. `False or False` is `False`.
3. `if a_x >= 1000 and b_x >= 1000:` then nested `if a_x > b_x: result = "A wins"`, `elif b_x > a_x: result = "B wins"`, `else: result = "dead heat"`. Then `elif a_x >= 1000: result = "A wins"`, `elif b_x >= 1000: result = "B wins"`. With 1004 and 1011, B wins.
4. Four: west to middle (`east`), middle to east (`east`), middle to west (`west`), east to middle (`west`). For example `if room == "west" and command == "east": room = "middle"`, and so on.

</details>

## Lab / assignment hook

[Lab 02, a cave with a way out](../labs/lab02.md). You extend a starter cave with conditional room transitions, a locked door, and a win/lose check that handles the tie case. A checker script feeds scripted commands to your program and compares the output. Part of the weekly exercises (40%).

## Sources

- SmashWiki, "Sudden Death". Ties in timed matches, and simultaneous loss of last stocks on the same frame in untimed Stock and Stamina matches, lead to Sudden Death; fighters restart with one stock at 300% damage. Applies across the series from Super Smash Bros. (1999) to Ultimate (2018), with per-game variations.
- FIDE, *Laws of Chess*, taking effect from 1 January 2023, Articles 5.1.1 (checkmate wins) and 5.2.1 (stalemate is a draw). handbook.fide.com.
- TetrisWiki, "Top out". Definitions of block out, lock out, partial lock out and garbage out in Tetris Guideline games.
- Python Software Foundation, *The Python Tutorial*, section 4.1, and *The Python Language Reference*, section 6.17 "Operator precedence" (Python 3.13).

## Interactive spec: examples/w02-win-lose-order.html

**Purpose.** Show that an `if`/`elif` chain returns the first true branch, so the order of overlapping branches changes the outcome. The first screen shows the naive chain with `p1_hp = 0`, `p2_hp = 0` and the "both out" cell marked red with the result "P1 wins".

**Layout.** Two linked views. Left: the code chain. Right: the case grid. Stacked on mobile (code first).

**Left view, the chain.**
- Four branch cards, each showing one line of Python: `if p1_out and p2_out: "sudden death"`, `p2_out: "P1 wins"`, `p1_out: "P2 wins"`, and a fixed final `else: "keep playing"` card that cannot move. The first movable card is always labelled `if`, the rest `elif`, updated as they move.
- Reorder by drag, and by keyboard (focus a card, then Alt+Up/Alt+Down or on-screen up/down buttons).
- Default order (the naive chain): `p2_out`, `p1_out`, `p1_out and p2_out`.
- Above the cards, the two definitions update with the comparison toggle: `p1_out = p1_hp <= 0` or `p1_out = p1_hp == 0`.
- Controls: sliders `p1_hp` and `p2_hp`, integers from −20 to 50 (default 0 and 0); toggle `<=` / `==` (default `<=`); preset buttons for the six table rows.
- While evaluating, mark each card as "checked: False", "fired" (accent colour plus the word "fired") or "skipped" (greyed, with the word "skipped").

**Right view, the case grid.**
- Rows: neither out (30, 20), P2 out (30, 0), P1 out (0, 20), both out (0, 0), both out overkill (−5, −12), P2 out overkill (30, −4).
- Columns: case, intended result (the correct chain with `<=`), this chain's result, status mark (tick or cross plus text "matches" / "wrong").
- The grid recomputes for every reorder or toggle. The row matching the current slider values is outlined.
- A summary line: "This chain is wrong in N of 6 cases."

**The one insight.** The code looks plausible in every order. Only the case grid shows that the `and` branch must come first and that `==` misses overkill.

**Test values (must match the lecture table).**
- Naive order, `<=`: rows give keep playing, P1 wins, P2 wins, P1 wins, P1 wins, P1 wins. Wrong in 2 of 6.
- Correct order (`and` first), `<=`: matches intended in 6 of 6.
- Correct order, `==`: row 5 gives keep playing, row 6 gives keep playing. Wrong in 2 of 6.
- Naive order, `==`: rows 4, 5, 6 give P1 wins, keep playing, keep playing. Wrong in 3 of 6.

**Accessibility.** Status never relies on colour alone; results are announced in an `aria-live="polite"` region; all reordering works without a pointer.
