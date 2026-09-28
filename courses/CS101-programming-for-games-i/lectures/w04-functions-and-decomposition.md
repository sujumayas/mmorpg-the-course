# CS101 · Week 04 — Functions and Decomposition

**Why this matters:** By week 3 your text adventure works, but the same ten lines appear in four places and fixing a bug means finding all four. Functions let you write a rule once, give it a name, and call it from everywhere. That also means one mistake in a function shows up everywhere, which is exactly what happened to every attack in the first Pokémon games.

**You will be able to:**
- Write functions with parameters and return values, and call them from other functions.
- Trace a call by hand: which values go in, which value comes out, which variables exist where.
- Decompose one turn of a game into four or five named functions with one job each.
- Test a function at its boundary values with `assert` and predict which inputs will expose an off-by-one.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "Update Method" chapter (read it for how a game splits one frame into small calls; skip the C++ details). Python tutorial, section 4.8 "Defining Functions" (docs.python.org).

**Prerequisites from earlier courses:** [CS101 week 1, programs, variables and types](w01-programs-variables-and-types.md), [week 2, conditionals](w02-conditionals-room-transitions-and-win-lose.md) and [week 3, loops and the game loop](w03-loops-and-the-game-loop.md) (variables, `if`, `while` and the turn loop that runs your text adventure). [MA101 week 1, functions as machines](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w01-functions-as-machines.md) (a function maps an input to one output; a Python function is the same idea with extra powers). Section 2 counts outcomes to get a probability; this lecture shows you how, and [MA102 week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) builds the full method next semester.

**Interactive:** [One function, many callers](../examples/w04-one-function-many-callers.html). Use it during section 2.

---

## 1. What a function is, in Python

A **function** is a named block of code that you can run on demand. You define it once with `def` and then **call** it by writing its name followed by parentheses.

```python
def describe_room(name, exits):
    exit_text = ", ".join(exits)
    return f"You are in the {name}. Exits: {exit_text}."

line = describe_room("cellar", ["north", "up"])
print(line)   # You are in the cellar. Exits: north, up.
```

Four words to learn here.

- A **parameter** is a name in the `def` line (`name`, `exits`). It is a placeholder.
- An **argument** is the actual value you pass in a call (`"cellar"`, `["north", "up"]`). When the call happens, each parameter is bound to its argument.
- The **return value** is what the function hands back. `return` ends the function immediately and sends that value to the caller. A function with no `return` hands back the special value `None`.
- The **caller** is the line of code that called the function. After the function returns, Python carries on from the caller.

### Return is not print

This is the single most common beginner confusion, so settle it now. `print` shows text on the screen for a human. `return` gives a value to the code that called the function. A function that prints its answer instead of returning it is useless to other code.

```python
def damage_print(attack, armor):
    print(attack - armor)       # shows a number, returns None

def damage(attack, armor):
    return attack - armor       # hands the number back

hp = 30
hp = hp - damage(12, 4)         # hp is now 22
hp = hp - damage_print(12, 4)   # prints 8, then crashes: 22 - None
```

The crash message is `TypeError: unsupported operand type(s) for -: 'int' and 'NoneType'`. When you see `NoneType` in an error, the first thing to check is a function that forgot to `return`.

### Local variables

Variables created inside a function are **local**. They exist only while that call is running, and each call gets fresh ones. `exit_text` in `describe_room` does not exist after the function returns, and it cannot clash with an `exit_text` somewhere else in your program.

This is a feature. It means you can read a function by itself, without scrolling through the whole program to see what else might touch its variables. The inputs are the parameters, the output is the return value, and everything in between is private.

A function can *read* a variable defined at the top level of your file (a **global**), but if it assigns to that name, Python treats the name as a new local variable instead. For now, follow a simple rule: pass what a function needs as arguments and return what it produces. Week 11's state machine will show a cleaner way to hold shared game state than globals.

### Tracing a call

When you're unsure what a function does, trace it on paper. Write the call, bind each parameter to its argument, run the body line by line, and write down the returned value.

```python
def heal(hp, amount, max_hp):
    hp = hp + amount
    if hp > max_hp:
        hp = max_hp
    return hp

player_hp = 25
player_hp = heal(player_hp, 10, 30)
```

| Step | `hp` (local) | `amount` | `max_hp` | Note |
|---|---|---|---|---|
| call | 25 | 10 | 30 | parameters bound to arguments |
| `hp = hp + amount` | 35 | 10 | 30 | |
| `if hp > max_hp` | 30 | 10 | 30 | condition true, clamp |
| `return hp` | 30 | — | — | caller receives 30 |

After the call, `player_hp` is 30. Notice that the function changed its own local `hp`, not `player_hp`. The caller had to assign the result to `player_hp` to keep it.

## 2. Worked example: one comparison, every attack

### The hook

In Pokémon Red and Blue (1996 in Japan, 1998 in North America), a move listed as 100% accurate could miss. Not often. About once every 256 uses. Players noticed, and the fan wikis now call it the "1/256 miss glitch." It hit every move that went through the accuracy check: Tackle, Pound, Thunderbolt, all of them.

Why every move? Because there was one accuracy check, and every move called it. That's the power of a function and its danger in one sentence.

### The model

The pret project has reconstructed the game's source as assembly code, and its move table stores accuracy as a byte (a whole number from 0 to 255), converted from a percentage by multiplying by 255 and dividing by 100. Bulbapedia describes the check itself: the game picks a random integer from 0 to 255 inclusive, and the move hits if that number is strictly less than the move's accuracy byte.

Here is that rule written as Python functions. We ignore accuracy and evasion stat changes to keep one model.

```python
def percent_to_byte(percent):
    """Convert a listed accuracy (0-100) to the stored byte (0-255)."""
    return percent * 255 // 100

def hits(accuracy_byte, roll):
    """One accuracy check. roll is a random integer from 0 to 255."""
    return roll < accuracy_byte

def hit_chance(accuracy_byte):
    """Count how many of the 256 possible rolls hit."""
    wins = 0
    for roll in range(256):
        if hits(accuracy_byte, roll):
            wins += 1
    return wins / 256
```

Every symbol, named:

- `percent` is the accuracy printed in the move list, like 100 or 85.
- `//` is integer division. It throws away the remainder, just as the original integer maths did.
- `accuracy_byte` is the stored value, 0 to 255. A 100% move stores 255, the largest number a byte can hold.
- `roll` is one random draw from the 256 values 0, 1, ..., 255. In the game the roll comes from a random number generator. `hit_chance` sidesteps randomness by trying every possible roll once, which is how you count a probability exactly (next semester's [MA102 week 1](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md)).

Now look at the problem. The largest possible roll is 255. The largest possible accuracy byte is also 255. `255 < 255` is false. So roll 255 always misses, even for a perfect move.

### Numbers you can check

Run the three functions for four real moves from the Red and Blue move table:

```python
for name, percent in [("Pound", 100), ("Fire Blast", 85),
                      ("Hydro Pump", 80), ("Thunder", 70)]:
    b = percent_to_byte(percent)
    print(name, percent, b, round(hit_chance(b) * 100, 2))
```

| Move | Listed accuracy | Stored byte | Rolls that hit | Real hit chance | Miss chance |
|---|---|---|---|---|---|
| Pound | 100% | 255 | 0 to 254 (255 rolls) | 99.61% | 0.39% |
| Fire Blast | 85% | 216 | 0 to 215 (216 rolls) | 84.38% | 15.62% |
| Hydro Pump | 80% | 204 | 0 to 203 (204 rolls) | 79.69% | 20.31% |
| Thunder | 70% | 178 | 0 to 177 (178 rolls) | 69.53% | 30.47% |

Check one row by hand. For Fire Blast, `85 × 255 = 21,675`, and `21,675 // 100 = 216`. The rolls that pass `roll < 216` are 0 through 215, which is 216 rolls out of 256. `216 / 256 = 0.84375`. Every move comes out a little below its listed accuracy, and the 100% move is the one players notice, because "never misses" is a promise and 99.61% breaks it.

### Move it

Open the interactive. The left view is a 16 by 16 grid, one cell per possible roll, coloured hit or miss for the selected move. The bottom-right cell, roll 255, is red for every move. The right view is a list of callers, the moves that use `hits()`, each with its live hit chance.

Now flip the comparison toggle from `<` to `<=`. One character changes in one function, and every caller's number updates at once. Pound becomes 100%. Fire Blast becomes 217 of 256, 84.77%. That's the insight to take away. **A function is a single point of truth. A bug in it is everywhere, and a fix to it is everywhere.**

The second toggle, in `percent_to_byte`, switches `255` to `256`. It fixes the 100% move from the other function. Turn both on and every move lands above its listing, which is what two fixes to one bug do.

The interactive also has a "Swift" caller that skips `hits()` entirely. In the English-language releases, Swift and Bide skipped the accuracy check and always hit, so they were immune to the glitch. A caller that bypasses the shared function also bypasses its bugs and its fixes. Keep that in mind when you are tempted to write "just this once" special-case code.

### The same idea in other games

Every game with a hit roll has one function that decides it. What differs is how deliberately its designers chose the edges.

**Diablo II (original and Lord of Destruction).** The chance to hit is `2 × AR / (AR + DR) × alvl / (alvl + dlvl)`, where AR is attack rating, DR is defense and the last factor compares attacker and defender levels. The result is then clamped between 5% and 95%. As a Python function:

```python
def d2_hit_chance(ar, dr, alvl, dlvl):
    raw = 2 * ar / (ar + dr) * alvl / (alvl + dlvl)
    return min(0.95, max(0.05, raw))
```

At equal levels (30 vs 30), AR 1,000 against DR 100 gives a raw 90.9%, left alone. AR 5,000 against DR 100 gives a raw 98.0%, clamped to 95%. AR 100 against DR 3,000 gives 3.2%, raised to 5%. Diablo II has the same kind of edge rule as Pokémon, "you can never be sure to hit," but here it's written on purpose, in one visible line, at 5% instead of 0.39%. You will study this formula's shape in year 3, in [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md), and the `min(max(...))` clamp in [MA101 week 7](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md).

**Dungeons & Dragons 5th edition (System Reference Document 5.1).** A tabletop game, but the rule is a function all the same. You roll a twenty-sided die and add your bonus, and you hit if the total meets the target's Armor Class. A natural 20 always hits, and a natural 1 always misses, whatever the modifiers.

```python
def d20_hits(roll, bonus, armor_class):
    if roll == 20:
        return True
    if roll == 1:
        return False
    return roll + bonus >= armor_class
```

Count the rolls 1 to 20 that hit, the same way `hit_chance` counts 0 to 255. With bonus 5 against Armor Class 25, only the natural 20 hits, 5%. With bonus 5 against Armor Class 4, everything except the natural 1 hits, 95%. The two special cases produce the same 5% to 95% band as Diablo II's clamp, written as early returns instead of `min` and `max`.

Three games, three `hits()` functions, one shape: a comparison, plus a decision about the edges. Pokémon's edge was an accident of `<` against a byte that tops out at 255. Diablo II's and D&D's were design choices. Whenever you write a check function, ask what happens at the smallest and largest input, and whether that is what you meant.

### Design judgment

Putting a rule in one shared function is almost always right. You get one place to read it, one place to test it, one place to fix it. The cost is that a mistake in it has a big blast radius, so shared functions deserve the most careful tests. Some trade-offs to decide on purpose:

- **Where the edges go.** A guaranteed hit is a strong promise to players. If you want a floor or ceiling on chance (5%, 95%), write it as an explicit clamp with a name, so the next programmer sees it was intended. Pokémon's 0.39% "floor" is invisible in the code, which is why it survived until release.
- **Bypasses.** Swift's special case shows the other side. Callers that skip the shared function need a reason, and the reason should be written down. Otherwise, when you fix the function, you'll forget the callers that don't use it.
- **What the tooltip says.** Players read the listed number, not the byte. If rounding or integer maths moves the real chance, either make the display match the computation or make the computation match the display. The Pokémon move list says 85, and the game computes 84.38%.
- **Test at the boundaries.** The bug lives at roll 255, the last value. Tests at a "typical" input like roll 100 pass forever and prove nothing. Section 4 turns this into a habit.

## 3. Decomposition: splitting a turn into functions

**Decomposition** means breaking a big task into smaller named tasks until each one is simple enough to write and test on its own. For a game, the natural first cut is one turn (or one frame, from week 7 onward).

Here is a week 3 style loop, written as one long block:

```python
room = "hall"
hp = 30
while hp > 0:
    text = input("> ").strip().lower()
    words = text.split()
    if len(words) == 0:
        continue
    verb = words[0]
    if verb == "go" and len(words) > 1:
        if room == "hall" and words[1] == "north":
            room = "cellar"
        elif room == "cellar" and words[1] == "south":
            room = "hall"
        else:
            print("You can't go that way.")
    elif verb == "look":
        if room == "hall":
            print("A dusty hall. Exits: north.")
        elif room == "cellar":
            print("A damp cellar. Exits: south.")
    elif verb == "quit":
        break
    else:
        print("I don't understand.")
```

It works. It is also hard to extend. Adding a third room means editing two different `if` chains, and adding a verb means reading the whole loop to find the right spot. Decompose it by asking "what are the steps of one turn?" and giving each step a function.

```python
EXITS = {("hall", "north"): "cellar", ("cellar", "south"): "hall"}
DESCRIPTIONS = {"hall": "A dusty hall. Exits: north.",
                "cellar": "A damp cellar. Exits: south."}

def read_command():
    return input("> ").strip().lower()

def parse(text):
    """Split 'go north' into ('go', 'north'). Missing parts become ''."""
    words = text.split()
    verb = words[0] if len(words) > 0 else ""
    noun = words[1] if len(words) > 1 else ""
    return verb, noun

def move(room, direction):
    """Return the new room, or the same room if there is no exit."""
    return EXITS.get((room, direction), room)

def describe(room):
    return DESCRIPTIONS[room]

def play():
    room = "hall"
    while True:
        verb, noun = parse(read_command())
        if verb == "quit":
            break
        elif verb == "go":
            new_room = move(room, noun)
            if new_room == room:
                print("You can't go that way.")
            room = new_room
        elif verb == "look":
            print(describe(room))
        else:
            print("I don't understand.")

if __name__ == "__main__":
    play()
```

The dictionaries `EXITS` and `DESCRIPTIONS` are a preview of week 6. Read them for now as "look up the answer by key."

What did decomposition buy?

- **Each function has one job and a name that says it.** You can read `play()` top to bottom like a to-do list.
- **Three of the five functions are pure.** A **pure function** uses only its arguments and returns a value, with no printing, no input and no changes to anything outside. `parse`, `move` and `describe` are pure. Pure functions are the easiest code in the world to test, because the same input always gives the same output.
- **Input and output are pushed to the edges.** Only `read_command` and `play` talk to the player. Everything in between is data in, data out. This split is what lets you later swap the keyboard for a Godot input event (week 8) without rewriting the rules.
- **Adding content means adding data, not code.** A third room is one line in each dictionary.

The line `if __name__ == "__main__":` runs `play()` only when you run this file directly. When another file (like a test file) does `import adventure`, the functions become available but the game doesn't start. You'll use this in the lab.

### How small should a function be?

There's no line limit, but there are good signs that a function should be split:

- You need the word "and" to describe what it does ("parses the command and moves the player").
- It has a comment in the middle saying "now do the next part."
- You copied a block of it somewhere else.

And a sign you've split too far: a function whose body is one line that just calls another function with the same arguments, adding nothing. Nystrom's "Update Method" chapter makes the same argument at game scale, where each game object gets one `update` call per frame and the game loop does not need to know what happens inside.

### Default arguments and keyword arguments

Two conveniences that make functions nicer to call:

```python
def attack(attacker, defender, bonus=0, crit=False):
    ...

attack(hero, rat)                    # bonus=0, crit=False
attack(hero, rat, crit=True)         # skip bonus, name crit
```

A **default argument** (`bonus=0`) is used when the caller leaves it out. A **keyword argument** (`crit=True`) names the parameter in the call, which makes the call readable and lets you skip the ones in between. Put parameters with defaults after those without.

## 4. Testing a function at its edges

You now have small pure functions, so you can test them without playing the game. The simplest tool is `assert`, which does nothing when its condition is true and stops the program with an `AssertionError` when it's false.

```python
from adventure import parse, move

assert parse("go north") == ("go", "north")
assert parse("look") == ("look", "")
assert parse("") == ("", "")
assert move("hall", "north") == "cellar"
assert move("hall", "west") == "hall"
print("all tests passed")
```

Which inputs should you test? The Pokémon example gives the rule: **test the edges, not the middle.** For any function, list:

1. The smallest input (an empty string, 0, an empty list).
2. The largest input (roll 255, a full inventory, maximum HP).
3. Each side of every comparison. If the code says `roll < accuracy`, test `roll = accuracy − 1` and `roll = accuracy`.
4. One ordinary case, so you know the normal path works.

Here is what a boundary test for the accuracy check would have looked like:

```python
assert hits(255, 254) is True
assert hits(255, 255) is True     # fails: 255 < 255 is False
```

The second line fails and points straight at the bug. If the designers intended "100% means always," this test is the spec written as code. If they had intended the tiny miss chance, they'd write `is False` and a comment saying why.

A test that fails is not bad news. It is the cheapest moment to find a bug, long before a player does.

## In-class activity (25 minutes)

Work in pairs with one laptop. Materials: the long-loop version of the text adventure from section 3 and this lecture's decomposed version, both copied into two files.

1. (10 min) Add a third room, "tower," reached by going "up" from the hall, to **both** versions. Count how many lines you changed in each. Write both numbers down.
2. (5 min) Add a verb "hp" that prints the player's health. In the decomposed version, decide which function should own it. If none fits, write a new one and explain why in a comment.
3. (10 min) Write five `assert` tests for `move` and `parse`, at least two of them at edges (an empty command, a three-word command like "go north quickly", a direction with no exit). Swap tests with the pair next to you and run theirs against your code.

Expected output: the two line counts, the new function (if any) with its comment, and a note of any test from the other pair that failed on your code and why.

## Common misconceptions

- **"My function printed the right answer, so it works."** Printing is not returning. If other code needs the value, the function must `return` it. Watch for `None` in error messages.
- **"Changing a parameter inside the function changes the caller's variable."** Assigning to a parameter rebinds the local name only. `heal` changed its own `hp`, and the caller had to write `player_hp = heal(...)`. (Lists behave differently when you change their contents rather than rebind the name. Week 5 covers that.)
- **"The code in a `def` runs when Python reads it."** Defining a function only stores it. The body runs each time you call it, and not before.
- **"If a test passes for a normal input, the function is correct."** The 1/256 bug passes every test except the one at roll 255. Correctness lives at the edges.

## Check yourself

1. Suppose the Pokémon check had been `roll <= accuracy_byte` with the same `percent_to_byte`. What would Thunder's (70%) real hit chance be? Is any move now above its listed accuracy?
2. A game designer wants every move to have at least a 2% chance to miss, deliberately. Write the one-line change to `hit_chance`'s result (or to `hits`) that achieves this without touching `percent_to_byte`, and say which moves it affects.
3. In the D&D function, a character has bonus 7. For which Armor Class values is the hit chance exactly 5%? Exactly 95%?
4. The following function has a bug. Trace `clamp_hp(35, 30)` and `clamp_hp(-5, 30)` and say what goes wrong.

```python
def clamp_hp(hp, max_hp):
    if hp > max_hp:
        return max_hp
    if hp < 0:
        hp = 0
```

5. Name the four functions you would write to decompose "the enemy's turn" in a text adventure fight. For each, say whether it can be pure.

<details>
<summary>Answers</summary>

1. The byte is `70 × 255 // 100 = 178`. With `<=`, rolls 0 through 178 hit, which is 179 rolls. `179 / 256 = 69.92%`. Pound becomes exactly 100%. Hydro Pump goes slightly above its listing: byte 204, so 205 rolls hit, 80.08%. The fix swapped a small shortfall for a small overshoot. The interactive's second toggle shows another fix, `× 256` in `percent_to_byte` with `<` kept, and turning on both fixes at once pushes Fire Blast, Hydro Pump and Thunder above their listings.
2. Clamp the chance, for example `return min(0.98, wins / 256)`. Only moves whose chance exceeds 98% change. With the original `<` check that is just the 100% moves (99.61% becomes 98%). A 95% move (byte 242, 94.53%) is unaffected. To make it a real rule of the game, not a display change, put the clamp inside the function the battle actually calls.
3. A normal roll hits when `roll + 7 >= AC`. The best normal roll is 19, reaching 26. So for AC 27 and above, only the natural 20 hits: 5%. The worst normal roll is 2, reaching 9. So for AC 9 and below, everything but the natural 1 hits: 95%.
4. `clamp_hp(35, 30)` returns 30, correct. `clamp_hp(-5, 30)` sets the local `hp` to 0 but never returns it, so the function returns `None`. Also, `clamp_hp(20, 30)` returns `None`. The fix is a final `return hp` after the second `if`.
5. One reasonable answer: `choose_action(enemy, player)` (pure if it uses no randomness, or if you pass the random roll in as an argument), `resolve_attack(attacker, defender, roll)` returning damage (pure), `apply_damage(hp, damage)` returning the new HP (pure), and `report(event)` printing a message (not pure, it does output). Passing the roll in as an argument is the trick that keeps random functions testable.

</details>

## Lab / assignment hook

[Lab 04, refactoring the combat turn](../labs/lab04.md). You get a working but tangled text-adventure fight in one 70-line loop. Split it into pure functions, make the provided boundary tests pass, and find the off-by-one that the tests expose. Deliverable: the refactored file with all tests passing and a short note on the bug.

## Sources

- pret, `pokered` disassembly of Pokémon Red and Blue (English release, 1998), `macros/data.asm` (the `percent` macro, `* $ff / 100`) and `data/moves/moves.asm` (listed accuracy of Pound 100, Fire Blast 85, Hydro Pump 80, Thunder 70, Swift 100). https://github.com/pret/pokered
- Bulbapedia, "Accuracy" (Generation I section). Random integer 0 to 255 inclusive; the move hits if the roll is strictly less than the modified accuracy; the result is a minimum 1 in 256 miss chance for moves that take the check.
- Bulbapedia, "List of battle glitches in Generation I", section on the 1/256 miss. 100% accuracy moves hit 255/256 of the time; in non-Japanese versions Swift and Bide skip the accuracy check.
- Bulbapedia, "Swift (move)", Generation I. Bypasses accuracy checks in Western versions; behaves as a 100% move in the Japanese versions.
- The Amazon Basin (Diablo II), "Technical Formulas", and Mann M., "Come and Get It: Attack and Defense Ratings" (d2library). Diablo II and Lord of Destruction chance to hit with the 5% and 95% limits. Same sources as MMO303 week 2.
- Wizards of the Coast, System Reference Document 5.1 (D&D 5th edition, 2016), "Making an Attack: Attack Rolls". A natural 20 always hits and a natural 1 always misses. Read via 5thsrd.org.
- Nystrom, R. (2014). *Game Programming Patterns*, "Update Method". gameprogrammingpatterns.com.
- Python Software Foundation, *The Python Tutorial*, section 4.8 "More on Defining Functions" (Python 3.12 documentation).

## Interactive spec: examples/w04-one-function-many-callers.html

**Purpose.** Make visible that one comparison inside one shared function decides the hit chance of every move that calls it, and that roll 255 misses for everyone under `<`.

**Layout.** Two linked views side by side on desktop, stacked on mobile (grid first).

- **Left: the roll grid.** A 16 × 16 grid of 256 cells, laid out row-major so the top-left cell is roll 0 and the bottom-right is roll 255. Each cell shows its roll number on hover/focus (and as tiny text at widths ≥ 900px). Cells are filled with the "hit" token colour if `hits(byte, roll)` is true, else the "miss" token colour. Roll 255's cell has a thicker outline at all times so the eye finds it. Above the grid, one line: `Pound: 255 of 256 rolls hit (99.61%)` for the selected move.
- **Right: the callers list.** A table of moves that call `hits()`: Pound (100), Fire Blast (85), Hydro Pump (80), Thunder (70), plus a user row "Custom" with a numeric input 0-100. Columns: listed accuracy, stored byte, rolls that hit, real hit chance (2 decimals), difference from listed (percentage points, signed). Clicking or pressing Enter on a row selects it for the grid. A final row "Swift (skips hits())" always shows 100.00% and is greyed, with the note "does not call the function".
- **Top: the function source.** A code box showing:
  ```
  def hits(accuracy_byte, roll):
      return roll [<] accuracy_byte
  ```
  where `[<]` is a two-state toggle button (`<` / `<=`), keyboard operable, `aria-pressed`. A second toggle switches the scale in `percent_to_byte` between `× 255 // 100` (original) and `× 256 // 100, capped at 256` (a "fixed" alternative). Changing either toggle updates the grid and every row of the callers table within the same frame, and briefly highlights (200 ms, none under `prefers-reduced-motion`) every value that changed.

**Formulas.**
- `byte = floor(percent × 255 / 100)` (original) or `min(256, floor(percent × 256 / 100))` (alternative).
- `hits = roll < byte` or `roll <= byte`, for roll in 0..255.
- `chance = count(hits) / 256`.
- Swift row: always 256/256.

**Test values (must match exactly).**

| Move | Byte (×255) | `<` chance | `<=` chance |
|---|---|---|---|
| Pound 100 | 255 | 99.61% | 100.00% |
| Fire Blast 85 | 216 | 84.38% | 84.77% |
| Hydro Pump 80 | 204 | 79.69% | 80.08% |
| Thunder 70 | 178 | 69.53% | 69.92% |

With the ×256 scale and `<`: Pound byte 256, 100.00%; Fire Blast byte 217, 84.77%; Thunder byte 179, 69.92%.

**The one insight.** On first load (Pound selected, `<`, ×255) the only red cell is the outlined bottom-right one, and the heading reads 99.61%. Flipping one toggle turns it green and changes every row of the table at once.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css` inline; hit/miss colours must also differ in pattern (miss cells get a diagonal hatch) for colour-blind users. Grid is an `aria-hidden` visual; the heading line and table carry the numbers for screen readers. No game art, no Pokémon names or sprites beyond move names in text.
