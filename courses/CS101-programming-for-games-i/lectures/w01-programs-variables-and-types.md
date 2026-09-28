# CS101 · Week 01 — Programs, Variables and Types: A Text Adventure's State

**Why this matters:** Every game you have played is a pile of numbers and words that a program changes many times a second. This week you learn how to name those values, what kinds of values exist, and why the kind you pick decides what can go wrong. One bad choice of type is why Pac-Man cannot be finished.

**You will be able to:**
- Write and run a Python program that stores a text adventure's state in named variables and prints it.
- Identify the type of any value (`int`, `float`, `str`, `bool`) and predict what an operator does with it.
- Compute the range of an n-bit counter and the value it wraps to after overflow.
- Predict when a 32-bit float can no longer tell two nearby positions apart.

**Before class:** Install Python 3.12 or newer and check that `python --version` works in a terminal. Read the Python Tutorial (docs.python.org), sections 3.1.1 "Numbers" and 3.1.2 "Text". Skim Jamey Pittman, *The Pac-Man Dossier*, the section on level 256 (the split screen).

**Prerequisites from earlier courses:** None. This is the first programming course. If you are taking MA101 at the same time, [MA101 week 1, functions as machines](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w01-functions-as-machines.md) uses the same idea of a named value going in and a value coming out. [GD101 week 2, players, objectives, procedures, rules](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md) describes a game as rules that change a state. This lecture is where that state lives in code.

**Interactive:** [Every box has an edge](../examples/w01-byte-counter.html). Keep it open during section 4.

---

## 1. What a program is

A program is a list of instructions that a computer carries out in order, top to bottom. Python is the language we use for weeks 1 to 6. It reads almost like English, it runs without a compile step, and its syntax is close to GDScript, the language of the Godot engine we switch to in week 7.

Here is a complete program. Save it as `hello.py` and run it with `python hello.py`.

```python
print("You wake in a dark cave.")
print("There is a lamp here.")
```

The computer runs line 1, then line 2, then stops. `print` is a function that writes text to the terminal. The text between quotes is a string, a piece of text the program treats as data.

Three words you will use every day:

- **Source code** is the text you write.
- **Running** (or executing) is the computer carrying out that text.
- **Output** is what the program shows or saves.

When Python meets a line it cannot understand, it stops and prints an error with a line number. Read errors from the bottom up. The last line names the problem (`NameError`, `TypeError`), and the line above it points to where it happened. You will see hundreds of these. They are the computer telling you exactly where to look.

## 2. State: the numbers a game remembers

In 1975 and 1976 Will Crowther wrote *Colossal Cave Adventure* in Fortran on a PDP-10 mainframe. Don Woods expanded it in 1977. You typed one- or two-word commands like `GET LAMP`, and the game described what happened. Woods's version scored you out of 350 points.

Think about what the game must remember while you play: which room you are in, what you carry, whether the lamp is lit, your score. Everything the game remembers at a given moment is its **state**. Everything the program does is reading the state, deciding something, and changing the state.

In Python you store each piece of state in a **variable**, a name bound to a value:

```python
room = "cave entrance"
score = 0
lamp_lit = False
lamp_oil = 100.0
```

Read `=` as "now refers to", not "equals". The line `score = 0` means "from now on, the name `score` refers to the value 0". That difference matters on the next line:

```python
score = score + 10
```

In algebra this equation has no solution. In Python it is an instruction. Take the current value of `score`, add 10, and make `score` refer to the result. After it runs, `score` is 10.

Names follow a few rules. They may contain letters, digits and underscores, they cannot start with a digit, and case matters (`Score` and `score` are different). By convention Python code uses `lower_case_with_underscores`. Pick names that say what the value means in the game. `lamp_oil` beats `x`, and future you will thank present you.

### A first text adventure state

This program holds the whole state of a tiny adventure and prints a status line.

```python
# The Lantern Cave: game state
player_name = "Ada"
room = "cave entrance"
score = 0
lamp_lit = False
lamp_oil = 100.0      # percent
moves = 0

print(f"{player_name} is in the {room}.")
print(f"Score: {score}  Moves: {moves}  Lamp lit: {lamp_lit}  Oil: {lamp_oil}%")

# The player lights the lamp and walks north.
lamp_lit = True
room = "hall of echoes"
moves = moves + 1
lamp_oil = lamp_oil - 2.5
score = score + 5

print(f"{player_name} is in the {room}.")
print(f"Score: {score}  Moves: {moves}  Lamp lit: {lamp_lit}  Oil: {lamp_oil}%")
```

Output:

```
Ada is in the cave entrance.
Score: 0  Moves: 0  Lamp lit: False  Oil: 100.0%
Ada is in the hall of echoes.
Score: 5  Moves: 1  Lamp lit: True  Oil: 97.5%
```

Two new pieces here. A line starting with `#` is a **comment**, a note for humans that Python ignores. A string with an `f` before the quote is an **f-string**. Anything inside `{ }` is replaced by the value of that expression. F-strings are how you will build nearly every message your games print.

Notice that nothing in the program "moved" anyone. Five variables changed. That is all a game turn is. Next week you will make the changes depend on what the player typed.

## 3. Types: what kind of value is it?

Every value has a **type**, which decides what the value can hold and what operators do with it. Python has four types you need this week:

| Type | Holds | Examples | Game use |
|---|---|---|---|
| `int` | Whole numbers | `0`, `350`, `-3` | Score, moves, level, gold |
| `float` | Numbers with a fractional part | `97.5`, `0.1`, `-2.0` | Positions, speeds, oil level |
| `str` | Text | `"hall of echoes"`, `""` | Room names, messages, commands |
| `bool` | `True` or `False` | `True` | Flags: lamp lit, door open |

Ask Python for a type with `type(value)`. `type(97.5)` gives `<class 'float'>`.

### The same operator does different things

The `+` operator adds numbers and joins strings. `*` multiplies numbers and repeats strings.

```python
print(3 + 4)        # 7
print("3" + "4")    # 34   (two strings joined)
print("3" * 4)      # 3333
print(7 / 2)        # 3.5  (/ always gives a float)
print(7 // 2)       # 3    (// rounds down to an int)
print("3" + 4)      # TypeError: can only concatenate str (not "int") to str
```

The last line fails because Python refuses to guess whether you meant 7 or "34". Convert explicitly with `int()`, `float()` and `str()`. This matters the moment you read the keyboard, because `input()` always returns a string:

```python
gold_text = input("How much gold do you drop? ")   # the player types 12
gold = int(gold_text)
print(gold * 2)     # 24, not "1212"
```

### Floats are approximations

Run `print(0.1 + 0.2)`. You get `0.30000000000000004`. A float stores a number in binary with a fixed number of digits, and 0.1 has no exact binary form, the same way one third has no exact decimal form. For game code that leads to one rule you should adopt today. Never test floats with `==`. Ask whether they are close:

```python
print(0.1 + 0.2 == 0.3)                 # False
print(abs((0.1 + 0.2) - 0.3) < 1e-9)    # True
```

Python's own `int` has no size limit, so `2 ** 200` just works. Python's `float` is 64 bits. Game engines and older hardware are less generous, and that is where the worked example lives.

## 4. Worked example: a variable's type sets its range

### The hook: why Pac-Man has no level 257

The arcade *Pac-Man* (Namco, 1980) has no ending. You clear a maze, the next one starts, and it gets faster. Then, at level 256, the right half of the screen fills with garbage characters. The dots on that side cannot all be eaten, so the level can never be cleared. Players call it the split screen or kill screen. The maximum possible score, 3,333,360, is defined by it. You earn the most you can on levels 1 to 255, then use every life to scrape the rest out of level 256.

Nobody designed that ending. The level number was stored in a variable too small to hold 256.

### The model

Hardware stores an integer in a fixed number of **bits**, binary digits that are each 0 or 1. An unsigned integer of `n` bits can hold every whole number from 0 to `2^n − 1`. When a calculation produces something outside that range, the extra high bits are thrown away. The value the variable ends up holding is

```
stored = true_value mod 2^n
```

- `n` is the number of bits in the variable.
- `true_value` is what the maths says the answer should be.
- `mod` is the remainder after division, written `%` in Python.

That behaviour is called **overflow** when you go past the top and wraps back to 0. Going below 0 wraps to the top, which is sometimes called underflow. A **signed** integer uses the same bits but splits the range in half, from `−2^(n−1)` to `2^(n−1) − 1`.

Floats fail differently. They never wrap. Instead, a 32-bit float keeps about 24 binary digits of precision, so the gap between one float and the next grows as numbers get bigger:

```
gap(x) = 2^(floor(log2(x)) − 23)      for a 32-bit float and x ≥ 1
```

- `floor(log2(x))` is which power of 2 the number is sitting above. For x between 1,024 and 2,047 it is 10.
- The gap doubles every time `x` passes a power of 2.

### Numbers you can check

Pac-Man runs on a Z80 processor, and the level counter is one byte, 8 bits. So `n = 8` and the largest level it can hold is `2^8 − 1 = 255`. Python's `int` never overflows, so we simulate the byte with `% 256`:

```python
def wrap(value, bits):
    return value % (2 ** bits)

level = 254
for _ in range(4):
    level = wrap(level + 1, 8)
    print(level)
```

The `def` line creates a small named recipe, a function, that you can reuse. You write your own from [week 4](w04-functions-and-decomposition.md). For now, read `wrap(x, 8)` as "x squeezed into 8 bits". The `for` line repeats the indented lines 4 times, which week 3 covers.

| `level` before | `level + 1`, true value | Stored in 8 bits |
|---|---|---|
| 254 | 255 | 255 |
| 255 | 256 | 0 |
| 256 | 257 | 1 |
| 257 | 258 | 2 |

The Pac-Man Dossier traces what happens next. The game's level counter starts at 0, so on level 256 it holds 255. The routine that draws the row of bonus fruit at the bottom of the screen copies that counter into a one-byte register and adds 1 to get the level number. 255 + 1 wraps to 0, exactly the second row of the table, and the routine treats 0 as an early level. Its loop counts down one step at a time, and a count that starts at 0 goes to 255 on the first step. The loop runs 256 times instead of a handful, drawing whatever memory lies past the fruit table onto the right side of the screen. You can reproduce the count:

```python
count = 0
runs = 0
while True:
    count = wrap(count - 1, 8)
    runs = runs + 1
    if count == 0:
        break
print(runs)    # 256
```

(You meet `while` and `break` properly in [week 3](w03-loops-and-the-game-loop.md). For now, read it as "repeat until the count is back to 0".)

Ranges for common sizes:

| Bits | Unsigned range | Signed range |
|---|---|---|
| 8 | 0 to 255 | −128 to 127 |
| 16 | 0 to 65,535 | −32,768 to 32,767 |
| 32 | 0 to 4,294,967,295 | about ±2.1 billion |
| 64 | 0 to about 1.8 × 10^19 | about ±9.2 × 10^18 |

Gaps for a 32-bit float, computed from the formula and confirmed with Python's `struct` module:

| Position `x` | `floor(log2 x)` | Gap to next float |
|---|---|---|
| 1 | 0 | 0.00000012 |
| 1,000 | 9 | 0.000061 |
| 1,000,000 | 19 | 0.0625 |
| 8,388,608 | 23 | 1 |
| 16,777,216 | 24 | 2 |
| 100,000,000 | 26 | 8 |

Past 8,388,608 a 32-bit float cannot store any fraction at all. Past 16,777,216 it cannot even store every whole number:

```python
import struct

def as_float32(x):
    return struct.unpack("f", struct.pack("f", x))[0]

print(as_float32(16_777_217.0))   # 16777216.0, the +1 is lost
print(as_float32(1_000_000.3))    # 1000000.3125
```

### The visual

Open `examples/w01-byte-counter.html`. The left view is a counter drawn as a ring of all its possible values. Press "+1", or "Run +50" to take 50 steps at once, and watch the pointer go round. At 255 the next step lands on 0, and the level readout below the ring shows the true level and the stored one side by side until they split. Change the width to 4, 8 or 16 bits and the ring gets smaller or larger. The wrap never goes away, it only moves.

The right view is a number line for a 32-bit float. Slide the position from 1 to 100,000,000 on a log scale. Tick marks show every float that exists near that position. Near 1 they are too dense to draw. Near 16 million they are 2 apart, and a character standing at 16,777,217 snaps to a neighbour. Two views of one idea. A variable is a box of fixed size, and every box has an edge.

### Cross-game recognition

**Minecraft (Java Edition, before Beta 1.8, 2011).** Walk about 12.55 million blocks from the centre of the world and the terrain turned into walls of stacked blocks, the Far Lands. The Minecraft Wiki traces this to integer overflow in the noise generators that shape terrain. It is Pac-Man's problem in a different variable. The generator's arithmetic produced numbers too big for its integers, and they wrapped. The Far Lands stopped generating from the Beta 1.8 pre-release. The wiki also describes a second, separate effect at the same distances. The world's rendered position drifts and jitters, and the jitter gets worse at each power of 2. That is the float gap from our table. At 12.5 million, the next float is a whole block away.

**Civilization (1991), the "Nuclear Gandhi" story.** For years players repeated a story that Gandhi's aggression was 1, adopting democracy subtracted 2, and the unsigned byte wrapped to 255, turning him into a warmonger. Run the model and you get exactly that, `wrap(1 − 2, 8) = 255`. But the model only tells you what *would* happen for a given type. Sid Meier wrote in his 2020 memoir that the variables were signed, so the result would have been −1, and that government type did not change AI aggression at all. Brian Reynolds, lead designer of Civilization II, said that part of the code had no unsigned variable. Civilization V (2010) later gave Gandhi a nuclear streak on purpose, as a joke. The lesson for you is that a type bug is testable. Given the type and the operations, the result is not a matter of opinion.

**Godot 4, the engine you use from week 7.** The official docs state that a GDScript `int` is signed 64-bit and wraps from 9,223,372,036,854,775,807 to −9,223,372,036,854,775,808. A GDScript `float` is 64-bit, but `Vector2` and `Vector3`, which hold positions, use 32-bit floats unless the engine is recompiled with double precision. So the float gap table above applies to every sprite position you will write in this course.

### Design judgment

Types are design decisions, not only technical ones.

- **Pick the range from the design.** Ask what the largest honest value is. A level counter in an endless game has no honest maximum. Pac-Man's designers had one byte to spare and never expected anyone to reach 256.
- **Decide what happens at the edge.** Wrapping is almost never what a player expects. Clamping (holding the value at the maximum) usually is. Many games cap gold, lives or ammo with a clamp, `gold = min(gold + loot, 999_999)`, and show the cap in the interface so it reads as a rule rather than a bug.
- **Keep big worlds near zero.** If positions can reach millions of units, a 32-bit float jitters. Engines handle this by moving the origin with the player or by using 64-bit positions. Both cost something. You will not need either in this course, but you should know why a space game might.
- **Do not store money or scores as floats.** `0.1 + 0.2` is not `0.3`. Store cents or whole points as `int`.
- **Know your language.** Python hides integer overflow. That makes learning easier and it is also why you must simulate it (`% 256`) when you want to reason about hardware.

### Check yourself (worked example)

1. A handheld game stores the number of keys in 4 bits, unsigned. The player has 14 keys and finds 3 more. What does the counter show?
2. A signed 8-bit health value is 120 and a potion adds 10. What does it hold now, and what would the player see?
3. A racing game stores a car's distance along a 20 km track in metres as a 32-bit float. What is the gap between representable positions at the far end? Is that a problem for a car moving 0.5 m per frame?

<details>
<summary>Answers</summary>

1. `(14 + 3) mod 16 = 17 mod 16 = 1`. The counter shows 1 key.
2. The true value is 130, above 127. Unsigned it would be 130, but as a signed byte `130 − 256 = −126`. The player would see a character with negative health, and probably die.
3. 20,000 is between 2^14 = 16,384 and 2^15. The gap is `2^(14 − 23) = 2^−9 ≈ 0.002` m. A 0.5 m step is 250 gaps, so movement is fine. It becomes a problem only far beyond this.

</details>

## 5. Reading and changing state from the keyboard

You now have everything you need for a program that asks the player something and updates the state. This version asks one question and reports the result.

```python
room = "cave entrance"
lamp_oil = 100.0
gold = 0

print(f"You are at the {room}. Your lamp has {lamp_oil}% oil.")
found = int(input("You dig in the sand. How many coins do you find? "))
gold = gold + found
lamp_oil = lamp_oil - 2.5
print(f"You now carry {gold} gold. Lamp oil: {lamp_oil}%.")
```

Three habits to build now:

1. **Initialise every variable before you use it.** Reading a name that was never assigned gives `NameError`. Put all state at the top of the file so you can see it in one place.
2. **Convert input at the moment you read it.** Keep the string version only if you need the text.
3. **Print the state often.** When something goes wrong, the first question is always "what are the variables right now?" A status line after every change answers it.

Week 2 adds decisions (if the player types `north`, change the room). Week 3 wraps the whole thing in a loop so the game keeps asking.

## In-class activity (25 min)

In pairs, with one laptop and Python open.

1. **Design the state (10 min).** Pick a small scene from a game you know: a shop, a boss room, a fishing spot. List every value the game must remember for that scene. For each value, write its name, its type and its honest maximum.
2. **Stress it (10 min).** For each `int`, say which bit width you would choose if memory were tight (8, 16 or 32) and what happens at the edge. Would you wrap, clamp, or refuse the action? Write the one line of Python that does it (for a clamp, `min(value, cap)`).
3. **Swap (5 min).** Swap lists with another pair. Find one value whose type is wrong or whose edge will surprise a player.

Expected output: a table of 6 to 10 variables with name, type, maximum and edge behaviour, and one bug your partners found.

## Common misconceptions

- **"`=` means equals."** In Python `=` assigns. `score = score + 10` is legal and useful. Equality is tested with `==`, which you use next week.
- **"`input()` gives me a number if the player types one."** It always gives a string. `"5" + "5"` is `"55"`. Convert with `int()` or `float()`.
- **"Python can overflow like Pac-Man."** Python's `int` grows as needed. Engines, older hardware and file formats have fixed sizes, so you must know the width when your values leave Python.
- **"Floats are exact, just with decimals."** They are approximations whose precision gets worse as numbers grow. Compare with a tolerance and keep large worlds near zero.

## Check yourself

1. What does this print, and why? `a = "10"`, `b = 5`, `print(a * 2, int(a) + b)`.
2. A dungeon game stores the floor number in an unsigned 8-bit variable. A player descends from floor 250 by 10 floors. Which floor does the game think they are on?
3. You store the player's gold in a signed 16-bit integer. What is the most gold a player can hold, and what happens if they sell an item that would take them 1 gold past it?
4. Write the three lines of Python that store a player's name as a string, their health as an int set to 100, and a flag for whether they have the key, then print all three in one f-string.
5. A 32-bit float position is 3,000,000. Can it represent 3,000,000.25? Show the gap calculation.

<details>
<summary>Answers</summary>

1. `1010 15`. `"10" * 2` repeats the string. `int("10") + 5` adds numbers.
2. `(250 + 10) mod 256 = 4`. The game thinks they are on floor 4.
3. `2^15 − 1 = 32,767`. One more wraps to −32,768, so the player suddenly owes a fortune. A clamp at 32,767 avoids it.
4. `name = "Ada"`, `health = 100`, `has_key = False`, `print(f"{name}: {health} HP, key: {has_key}")`.
5. 3,000,000 is between 2^21 = 2,097,152 and 2^22. The gap is `2^(21 − 23) = 0.25`. So yes, 3,000,000.25 is exactly representable, but 3,000,000.1 is not and would round to 3,000,000.0.

</details>

## Lab / assignment hook

[Lab 01, the state of a text adventure](../labs/lab01.md). You fill in a starter file that holds the state of a four-room cave, add conversions for keyboard input, and implement a clamped gold counter and an 8-bit wrapping level counter. A small checker script tells you when each part works. This is the first of the weekly exercises (40% of the course grade across the semester).

## Sources

- Wikipedia, "Colossal Cave Adventure". Crowther 1975-1976 and Woods 1977, Fortran on the PDP-10, one- or two-word commands, 350-point maximum in the Woods version.
- Wikipedia, "Pac-Man". Level 256 fails to load properly because of integer overflow; the perfect score of 3,333,360 and how it is earned. Arcade original, Namco, 1980.
- Pittman, J., *The Pac-Man Dossier* (pacman.holenet.info), chapter 5, "Deciphering the Split Screen". The 0-based level counter holds 255 on level 256; the fruit routine adds 1 in a one-byte Z80 register, gets 0, and its drawing loop then runs 256 times and draws memory outside the fruit table to the screen.
- Minecraft Wiki, "Far Lands". Java Edition, Far Lands begin about 12.55 million blocks from the origin, caused by integer overflow in the terrain noise generators, fixed in the Beta 1.8 pre-release; precision jitter is a separate floating-point effect that worsens at each power of 2.
- Wikipedia, "Nuclear Gandhi". The legend's claimed mechanism; Sid Meier's 2020 memoir (variables signed, government did not affect AI aggression); Brian Reynolds's statement; the deliberate joke in Civilization V (2010).
- Godot Engine documentation (stable, Godot 4), "int" and "float" class references. 64-bit signed `int` that wraps; 64-bit `float`; `Vector2` and `Vector3` use 32-bit floats unless compiled with `precision=double`.
- Python Software Foundation, *The Python Tutorial*, section 3.1, and the `struct` module documentation (Python 3.13).

## Interactive spec: examples/w01-byte-counter.html

**Purpose.** Make overflow and float gaps visible as "every box has an edge". The first screen shows an 8-bit counter at 254 with the true level 254, one press away from the wrap.

**Layout.** Two panels side by side on desktop, stacked on mobile (counter first).

**Panel A, integer counter.**
- A ring of `2^n` evenly spaced tick positions (for n = 8, 256 ticks; label 0, 64, 128, 192 and the current value). A pointer marks the stored value.
- Controls: bit width segmented control {4, 8, 16} (default 8); signed/unsigned toggle (default unsigned); buttons "+1", "+10", "−1"; a "run" toggle that adds 1 every 150 ms (disabled under `prefers-reduced-motion`, replaced by a "+50" button); a reset button that sets the true value to `2^n − 2`.
- Readouts, in monospace: true value (unbounded integer), stored value, and the Python line `stored = true % 2**n` with numbers filled in. For signed mode show `stored = ((true + 2**(n−1)) % 2**n) − 2**(n−1)`.
- When stored ≠ true, highlight both readouts in the accent colour and show the text "wrapped".
- A small "fruit loop" demo row: button "decrement from 0" that shows the count sequence 0 → 255 → 254 ... and a run counter; it must report 256 runs for n = 8 (16 for n = 4, 65,536 for n = 16; for n = 16 compute rather than animate).

**Panel B, 32-bit float gaps.**
- A horizontal number line centred on the chosen position `x`, showing a window of width `10 × gap(x)`, with a tick at every representable float32 in that window (compute by `Math.fround` stepping or by the gap formula).
- A slider for `x` on a log scale from 1 to 100,000,000 (keyboard step: one power of 2 per arrow press, with fine steps via shift+arrow).
- A second input "character position" `p` (defaults to `x + 0.3`). Show `p` and `Math.fround(p)` and draw where the character actually lands.
- Readouts: `floor(log2 x)`, `gap(x) = 2^(floor(log2 x) − 23)`, and `Math.fround(p)`.

**The one insight.** The value is only as good as its box. Integers wrap at a hard edge; floats blur gradually as numbers grow.

**Test values (must match the lecture tables).**
- n = 8 unsigned: true 255 → stored 255; true 256 → 0; true 258 → 2.
- n = 8 signed: true 128 → −128; true −1 → −1; unsigned −1 → 255.
- n = 4 unsigned: true 17 → 1.
- Float gaps: x = 1 → 1.1920929e−7; 1,000 → 6.1035e−5; 1,000,000 → 0.0625; 8,388,608 → 1; 16,777,216 → 2; 100,000,000 → 8.
- `Math.fround(16777217)` = 16777216; `Math.fround(1000000.3)` = 1000000.3125; `Math.fround(3000000.25)` = 3000000.25.

**Accessibility.** All controls reachable by keyboard; readouts in an `aria-live="polite"` region; colour is never the only signal (the "wrapped" label appears as text).
