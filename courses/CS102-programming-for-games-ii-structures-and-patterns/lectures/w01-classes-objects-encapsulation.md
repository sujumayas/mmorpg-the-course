# CS102 · Week 01 — Classes, Objects and Encapsulation

**Why this matters:** In CS101 you kept game state in loose variables and dictionaries, and any line of code could change any of them. That works for a 300-line arcade game. It stops working when a dozen systems (moves, items, abilities, status effects, UI) all touch the same number, because one of them will eventually break the rule every other one respected. A class lets you write that rule once and make it impossible to skip.

**You will be able to:**
- Write a Python class with a constructor, private state, read-only properties and methods, and explain what `self` refers to.
- State the invariant a class protects and write the single method that enforces it.
- Compute how many call sites must change when a rule changes, with and without encapsulation, and use that count to argue for a design.
- Translate the same class into GDScript or C# and point to where each language enforces privacy.

**Before class:** Nystrom, *Game Programming Patterns* (2014), "Introduction" and "Architecture, Performance, and Games" (free online at gameprogrammingpatterns.com). Python tutorial, section 9 "Classes", sections 9.1 to 9.4 and 9.6 (docs.python.org).

**Prerequisites from earlier courses:** functions and decomposition ([CS101 week 4](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md)), dictionaries as item databases ([CS101 week 6](../../CS101-programming-for-games-i/lectures/w06-dictionaries-item-databases.md)), and game state machines ([CS101 week 11](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md)). Clamping values between a floor and a ceiling is [MA101 week 7, piecewise caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md).

**Interactive:** [w01-stat-stage-gate.html](../examples/w01-stat-stage-gate.html). Keep it open during section 2.

---

## 1. From loose variables to objects

### The problem you already have

Here is the kind of code you wrote at the end of CS101. A fighter is a dictionary, and functions reach into it.

```python
fighter = {"name": "Knight", "hp": 120, "max_hp": 120, "attack_stage": 0}

def drink_potion(f):
    f["hp"] += 50            # can this exceed max_hp?

def take_hit(f, damage):
    f["hp"] -= damage        # can this go below 0?

def war_cry(f):
    f["attack_stage"] += 2   # is there a limit?
```

Nothing in this code says what a legal fighter looks like. Is `hp = 170` allowed when `max_hp` is 120? Is `hp = -30` a dead fighter or a bug? The answer lives in the heads of whoever wrote each function, and they may not agree.

### Class, object, attribute, method

A **class** is a blueprint that says what data a kind of thing holds and what operations it supports. An **object** (or **instance**) is one concrete thing built from that blueprint. Two knights are two objects of one class.

An **attribute** is a variable that belongs to one object. A **method** is a function defined inside the class. Python passes the object the method was called on as the first parameter, named `self` by convention. When you write `knight.heal(50)`, Python runs `Fighter.heal(knight, 50)`.

The **constructor** is the special method `__init__`. Python calls it once when you create the object, and its job is to put the object into a legal starting state.

```python
class Fighter:
    def __init__(self, name, max_hp):
        if max_hp <= 0:
            raise ValueError("max_hp must be positive")
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp

    @property
    def hp(self):
        return self._hp

    @property
    def is_alive(self):
        return self._hp > 0

    def heal(self, amount):
        before = self._hp
        self._hp = min(self._max_hp, self._hp + amount)
        return self._hp - before          # how much actually healed

    def take_damage(self, amount):
        before = self._hp
        self._hp = max(0, self._hp - amount)
        return before - self._hp          # how much actually landed

knight = Fighter("Knight", 120)
knight.take_damage(80)    # returns 80, hp is 40
knight.heal(100)          # returns 80, hp is 120, not 140
```

Read the last two lines slowly. The caller asked for 100 healing and got 80, and the method *told it so* by returning the amount actually applied. That return value matters later: the UI can show "+80" instead of lying with "+100".

### Invariants and encapsulation

An **invariant** is a statement about an object that is true after the constructor finishes and stays true after every method call. For `Fighter` it is `0 <= hp <= max_hp`.

**Encapsulation** means the object's data can only change through the object's own methods, so the methods can guarantee the invariant. The outside world asks the object to do things (`heal`, `take_damage`) instead of editing its numbers.

Python enforces this by convention, not by the compiler. A leading underscore (`_hp`) says "private, do not touch from outside". Python will not stop you writing `knight._hp = 9000`, but every Python programmer, linter and code reviewer reads the underscore as a boundary. The `@property` decorator turns a method into something you read like an attribute (`knight.hp`, no parentheses) while giving you no way to assign to it. Try `knight.hp = 5` and Python raises `AttributeError`.

Other languages you'll use in this program enforce the boundary harder:

| Language | Private field | Read-only access | Where the rule lives |
|---|---|---|---|
| Python | `self._hp` (convention) | `@property` with no setter | methods like `heal` |
| GDScript (Godot 4) | no `private` keyword; `_hp` by convention | property with a `get:` and no public setter | a `set(value):` block that clamps |
| C# (Unity, .NET) | `private int hp;` (compiler enforced) | `public int Hp => hp;` | methods, or a property `set` that clamps |

GDScript's property syntax is worth seeing because you'll use it in Godot:

```gdscript
var max_hp: int = 120
var hp: int = 120:
    set(value):
        hp = clampi(value, 0, max_hp)
```

Now even `hp = 9000` from another script goes through the setter and lands at 120. The rule is attached to the data.

### Tell, don't ask

A good habit follows from encapsulation. Compare:

```python
# asking: the caller does the object's job
if knight.hp - dmg < 0:
    knight._hp = 0
else:
    knight._hp = knight.hp - dmg

# telling: the object does its own job
knight.take_damage(dmg)
```

The first version copies the rule into the caller. Do that in five places and you have five copies of the rule, and five chances to get it wrong. The second version keeps one copy. This is the argument of the whole lecture, and the worked example puts a number on it.

## 2. Worked example: the stat stage that won't go any higher

### The hook

Every main-series Pokémon game from Generation III onward has a small rule that players meet in their first few battles. Use a move like Swords Dance (raises the user's Attack by two stages) enough times and the game stops you with a message along the lines of "Attack won't go any higher!" Growl (lowers the target's Attack by one stage) hits the same wall at the bottom.

Now think about how many different things in those games change a stat stage. Hundreds of moves. Abilities like Simple, which from Generation V doubles every stage change, and Contrary, which reverses every change so that a boost becomes a drop. Abilities like Clear Body, which block Attack drops caused by opponents. Held items. Yet in a normal battle no Pokémon ever reaches +7. How do hundreds of effects, written by many people over many years, all respect one limit?

You don't know how Game Freak's code is organised internally, and this lecture won't guess. What you can observe is the *behaviour*: one limit, one message, applied identically by every effect. That behaviour is exactly what an encapsulated class produces, and it is very hard to produce any other way. So let's build it.

### The model

A stat stage is an integer `n`. The rule has three parts:

```
n is always in [-6, +6]                              (the invariant)
change(d):  d' = modify(d)   (Simple: 2d, Contrary: -d, else d)
            n_new = clamp(n + d', -6, +6)
            applied = n_new - n                      (0 means "won't go any higher")
multiplier(n) = max(2, 2 + n) / max(2, 2 - n)        (Generation III onward, for Attack, Defense, Sp. Atk, Sp. Def, Speed)
```

- `n` is the current stage.
- `d` is the change a move asks for, for example +2 for Swords Dance.
- `modify` is whatever the Pokémon's ability does to the request before it lands.
- `clamp(x, lo, hi)` returns `lo` if `x < lo`, `hi` if `x > hi`, else `x`.
- `applied` is how many stages actually changed. The battle text is chosen from it.

The multiplier formula looks odd until you evaluate it. For positive stages the denominator is 2 and the numerator grows: +1 is 3/2, +6 is 8/2. For negative stages the numerator is 2 and the denominator grows: −1 is 2/3, −6 is 2/8. It is symmetric in a satisfying way: +n and −n are exact reciprocals, so a +2 boost followed by a −2 drop always returns you to ×1.

Here it is as a class:

```python
from fractions import Fraction

class StatStages:
    MIN, MAX = -6, 6

    def __init__(self, ability=None):
        self._stage = 0
        self._ability = ability           # None, "simple" or "contrary"

    @property
    def stage(self):
        return self._stage

    @property
    def multiplier(self):
        n = self._stage
        return Fraction(max(2, 2 + n), max(2, 2 - n))

    def change(self, delta):
        """Apply a requested change. Return the change that actually happened."""
        if self._ability == "simple":
            delta *= 2
        elif self._ability == "contrary":
            delta = -delta
        new = max(self.MIN, min(self.MAX, self._stage + delta))
        applied = new - self._stage
        self._stage = new
        return applied
```

Every move in the game now does the same thing: `applied = target.attack.change(+2)`, then picks its battle text from `applied`. No move ever writes `_stage`. The move's author doesn't need to know about Simple, Contrary or the cap. The ability designer who adds Simple edits one method.

`Fraction` keeps the multipliers exact (2/7 stays 2/7 instead of becoming 0.2857142857142857), which makes the numbers easy to check against a table. In a shipped game you'd more likely use integers and multiply before dividing.

### Numbers you can check

The multiplier table, straight from the formula:

| Stage | −6 | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Multiplier | 2/8 | 2/7 | 2/6 | 2/5 | 2/4 | 2/3 | 1 | 3/2 | 4/2 | 5/2 | 6/2 | 7/2 | 8/2 |
| Decimal | 0.25 | 0.286 | 0.333 | 0.40 | 0.50 | 0.667 | 1.00 | 1.50 | 2.00 | 2.50 | 3.00 | 3.50 | 4.00 |

Now use Swords Dance (+2) four times in a row on a fresh `StatStages`, for each ability. Each cell shows `applied → stage (multiplier)`:

| Use | No ability | Simple | Contrary |
|---|---|---|---|
| 1st | +2 → +2 (×2) | +4 → +4 (×3) | −2 → −2 (×1/2) |
| 2nd | +2 → +4 (×3) | +2 → +6 (×4) | −2 → −4 (×1/3) |
| 3rd | +2 → +6 (×4) | 0 → +6 (×4), "won't go any higher" | −2 → −6 (×1/4) |
| 4th | 0 → +6 (×4), "won't go any higher" | 0 → +6 (×4) | 0 → −6 (×1/4), "won't go any lower" |

Check one by hand. Simple, second use: the request is +2, Simple doubles it to +4, `4 + 4 = 8`, clamp gives 6, applied is `6 − 4 = 2`. The move asked for +2, the ability turned it into +4, and the cap trimmed it to +2. Three rules touched this one number, in a fixed order, inside one method.

### The same game without encapsulation

Suppose instead the stage is a public field and each move adjusts it directly. Five moves, five call sites:

```python
# move_swords_dance.py
target.attack_stage = min(6, target.attack_stage + 2)
# move_growl.py
target.attack_stage = max(-6, target.attack_stage - 1)
# move_charm.py
target.attack_stage = max(-6, target.attack_stage - 2)
# move_howl.py
target.attack_stage = min(6, target.attack_stage + 1)
# move_power_up.py  (added later by someone new)
target.attack_stage += 1
```

The fifth author forgot the clamp. Nothing breaks immediately. Then someone chains Swords Dance three times (stage +6) and Power-Up twice. The stage is +8, the multiplier formula happily returns `(2 + 8) / 2 = 5`, and a Pokémon hits 25% harder than the design allows. The move didn't crash. It produced a plausible wrong number, which is the worst kind of bug to find.

Now count the cost of a rule change. The design team adds Simple. With the public field, every one of the five call sites must learn to double its delta, and the next move added must remember too. With the class, one method changes. In general:

| Change to the rule | Public field: files edited | Encapsulated class: files edited |
|---|---|---|
| Add Simple (double changes) | every call site, `c` | 1 |
| Add Contrary (reverse changes) | `c` | 1 |
| Change the cap from ±6 to ±4 | `c` | 1 |
| Add a new move | 1, and it must repeat all rules correctly | 1, and it can't break the rules |

`c` is the number of call sites. With five moves it's five. With hundreds of moves, the left column stops being a chore and becomes impossible to get right by hand.

Open the interactive now. The left panel is a list of move buttons; the right panel plots the stage after every action with the legal band from −6 to +6 shaded. Switch between "encapsulated" and "public field", then press the buggy move a few times. The public-field line leaves the band at exactly the moment the forgetful call site runs. The encapsulated line flattens against the edge and the log prints "won't go any higher". Then switch the ability to Simple and watch which version needs code changes to keep up: the panel lists the files edited under each design.

### Cross-game recognition

The same idea, one gate for one number, shows up whenever a game promises a limit.

**Final Fantasy series (early games, and Final Fantasy XIII from 2009).** Many early Final Fantasy games cap a single hit at 9,999 damage, and several later ones add a Break Damage Limit ability that raises the cap to 99,999. Final Fantasy XIII (2009) was the first to set its main limit at 99,999. In model form: `damage = clamp(raw, 0, CAP)`, where `CAP` is a field the ability changes. That only works if all damage passes through one function. The Final Fantasy Wiki documents what happens at the edges when it doesn't. In the original Final Fantasy II, damage above 9,999 was possible with stacked buffs, but the damage window showed only the last four digits, so 12,345 displayed as 2,345. The display and the damage rule disagreed about the limit. Final Fantasy VII is well known for a damage overflow glitch. Both are what the "public field" panel of the interactive predicts.

**Minecraft (Java and Bedrock, current versions).** A player normally has 20 health points, drawn as 10 hearts of two halves each. Healing from any source (food, potions, regeneration) stops at the maximum. Written in our form, `hp = clamp(hp + heal, 0, max_hp)`, the same `Fighter.heal` you wrote in section 1.

**Pac-Man (arcade, 1980).** The counter-example. An integer overflow makes the 256th level load improperly, and it cannot be completed. The level number outgrew the space the code gave it, and nothing on the path checked. You can read it as a missing invariant: "the level counter fits its storage" was true for 255 levels and silently false on the 256th.

Three games, one shape: a number with a legal range, and a single method that every change must pass through. When you meet a limit in a new game, ask two questions. What is the invariant? And where is the one place that enforces it?

### Design judgment, eyes open

Encapsulation is not free, and "make everything private with getters and setters" is not a design.

- **Strength: rules live in one place.** The table above is the whole argument. Rule changes cost 1 edit instead of `c`.
- **Strength: the method can report what happened.** `change` returns `applied`, so the UI, the battle log and the sound effect can all react correctly to 0. With a raw field, the caller has to compute that itself.
- **Cost: a getter-and-setter pair that does nothing is not encapsulation.** `def set_stage(self, v): self._stage = v` guards nothing. It just adds typing. Only wrap a field when there is a rule to protect or a representation you want freedom to change.
- **Cost: the class decides the order of rules.** Our `change` applies the ability first and the clamp second. Suppose you added a rule that blocks drops caused by opponents. Should it look at the request before Contrary flips it, or after? The two orders give opposite results for a Contrary Pokémon hit by Growl. Encapsulation forces you to choose once, explicitly, which is a benefit if you notice you're choosing. Write the order in a comment.
- **Cost: over-tight classes block legitimate designs.** Suppose a boss mechanic should temporarily allow +8. A hard-coded `MAX = 6` makes that a code change. Decide deliberately whether a limit is a law of the game (a class constant) or a tunable (a constructor parameter or data). You'll return to this in [week 13, data-driven design](w13-data-driven-design-stats-in-json-and-csv.md).

## 3. Objects that hold other objects

Real game objects are rarely a single number. A fighter has hit points *and* several stat stages. The natural move is to let objects own other objects:

```python
class Fighter:
    def __init__(self, name, max_hp, ability=None):
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self.attack = StatStages(ability)
        self.defense = StatStages(ability)

    def effective_attack(self, base_attack):
        return base_attack * self.attack.multiplier
```

`knight.attack.change(+2)` reads naturally, and the stage invariant is still enforced by `StatStages`, not by `Fighter`. Each class guards its own rule. `Fighter` doesn't need to know the cap exists.

This is **composition**: building an object out of smaller objects that each keep their own invariants. Week 2 argues that composition is usually a better way to share behaviour than inheritance. For now, notice the practical payoff: when you test `StatStages`, you test it alone, with no fighter, no battle and no UI.

### Identity versus equality

Two objects can hold the same data and still be different objects:

```python
a = StatStages()
b = StatStages()
a == b      # False by default: Python compares identity unless you define __eq__
a is b      # False: two separate objects
c = a
c.change(+2)
a.stage     # 2: c and a are the same object
```

The last three lines catch many students in their first week. Assigning an object to a new name does not copy it. Both names point at one object. If two fighters are built from one shared `StatStages`, a Swords Dance on one boosts both. When you want value semantics for small immutable things (a position, a colour, a damage packet), use `@dataclass(frozen=True)`, which gives you `__eq__` that compares fields and forbids assignment after construction.

### Class attributes versus instance attributes

`MIN` and `MAX` in `StatStages` are **class attributes**: one copy shared by every instance, read through `self.MIN` or `StatStages.MIN`. `_stage` is an **instance attribute**: each object has its own. Put tuning constants that are true for every instance on the class. Put per-object state on the instance, and set every instance attribute in `__init__` so a reader can see the object's full shape in one place.

## In-class activity (25 minutes)

Work in pairs. You'll need a laptop with Python 3.11 or later and the week's starter file from [lab 01](../labs/lab01.md) (`labs/lab01/stats.py`).

1. **Find the invariant (5 min).** Your partner names a game mechanic with a limit: a stamina bar, an ammo clip, a combo counter, a level cap, an inventory with 20 slots. Write the invariant as one line of math, such as `0 <= ammo <= clip_size`.
2. **Write the gate (10 min).** Write a class for it with private state, a read-only property and one or two methods that change the state and return what actually happened.
3. **Attack it (5 min).** Swap laptops. Try to break your partner's invariant using only public methods and properties. Every successful break is a bug in their class, not a cheat.
4. **Count call sites (5 min).** Imagine the mechanic appears in a shipped game with 40 items that affect it. Under "public field", how many places change if the cap moves? Under your class?

Expected output: one class per pair, a list of attempted breaks with results, and the two numbers from step 4.

## Common misconceptions

- **"Encapsulation means adding getters and setters to every field."** A setter that assigns without checking protects nothing. Encapsulate where there's a rule or a representation to hide, and let plain data stay plain.
- **"Python has no private, so encapsulation doesn't apply."** The underscore is a contract that tools and reviewers enforce. The design benefit, one place for each rule, doesn't depend on the compiler. And `@property` without a setter really does block assignment.
- **"`b = a` makes a copy."** It makes a second name for the same object. Changes through one name show up through the other.
- **"Clamping hides bugs."** Clamping that is part of the design (a cap players can see) is a rule, not a hack. What hides bugs is clamping in some call sites but not others. If a value outside the range means a programming error, raise an exception instead of clamping.

## Check yourself

1. A Pokémon at Attack stage +3 has the ability Simple and is hit by Growl (−1 stage). What is the applied change, the new stage and the new multiplier?
2. A Pokémon with Contrary at stage −5 uses Swords Dance. What does `change(+2)` return, and what does the battle log say?
3. A game has 60 items that restore mana. Mana is a public field. The designers add a rule that mana potions restore 25% less while "Silenced". How many code locations change under the public-field design and under an encapsulated `Mana` class with a `restore(amount, source)` method?
4. What does this print, and why?

```python
x = Fighter("A", 100)
y = x
y.take_damage(30)
print(x.hp, x is y)
```

5. Your `StatStages` has `MAX = 6`. A designer wants one boss to go to +8. Give two ways to support it and say which you prefer.

<details>
<summary>Answers</summary>

1. Simple doubles −1 to −2. `3 − 2 = 1`, inside the range, so applied is −2, the stage is +1 and the multiplier is 3/2.
2. Contrary turns +2 into −2. `−5 − 2 = −7` clamps to −6, so `change` returns −1. The stage falls by one, to −6 (×1/4). The log reports a fall, because `applied` is negative. Had the stage already been −6, `applied` would be 0 and the log would say it won't go any lower.
3. Public field: all 60 item call sites, and every future item must remember. Encapsulated: one method, `restore`, which checks the source and the Silenced status.
4. It prints `70 True`. `y = x` does not copy; both names refer to one `Fighter`.
5. (a) Make the limits constructor parameters, `StatStages(min_stage=-6, max_stage=8)`, and build the boss with different limits. (b) Keep `MAX` as a class constant and make a subclass `BossStatStages` with `MAX = 8`. Option (a) is usually better because it keeps the rule in one class and moves the tunable into data; option (b) starts an inheritance tree for a single number, which week 2 warns against.

</details>

## Lab / assignment hook

[Lab 01, gated stats](../labs/lab01.md). You'll implement `StatStages` and a `Fighter` with health, make a provided test suite pass, then add one new ability of your own design without touching any move code. Deliverable: your `stats.py`, passing tests, and a short note naming each invariant and the single method that enforces it.

## Sources

- Bulbapedia, "Stat modifier" (retrieved September 2026). Stage range −6 to +6; Generation III onward multipliers 2/8 through 8/2 for Attack, Defense, Sp. Atk, Sp. Def and Speed (Generations I and II used a different percentage table); Simple doubles and Contrary reverses stage changes from Generation V onward; "won't go any higher" family of battle messages across generations.
- Bulbapedia, "Swords Dance (move)" and "Growl (move)" (retrieved September 2026). Swords Dance raises the user's Attack by two stages; Growl lowers adjacent opponents' Attack by one stage; Clear Body and related Abilities block Attack drops.
- Final Fantasy Wiki, "Break Damage Limit" (retrieved September 2026). 9,999 as the primary damage limit in early games; 99,999 with Break Damage Limit; Final Fantasy XIII first to use 99,999 as the primary limit; Final Fantasy II (original) showing only the last four digits of damage above 9,999; Final Fantasy VII's damage overflow glitch.
- Minecraft Wiki, "Health" (retrieved September 2026, current Java and Bedrock editions). Players normally have 20 health points shown as 10 hearts.
- Wikipedia, "Pac-Man" (retrieved September 2026), citing Dwyer & Dwyer, *Cult Fiction* (2014), p. 14. An integer overflow makes level 256 load improperly and impossible to complete.
- Nystrom, R. (2014). *Game Programming Patterns*. Genever Benning. gameprogrammingpatterns.com.
- Python Software Foundation, *The Python Tutorial*, section 9 "Classes", and the `dataclasses` and `fractions` module documentation (Python 3.13).
- Godot Engine documentation, "GDScript reference", properties with `set` and `get` (Godot 4.x).

## Interactive spec: examples/w01-stat-stage-gate.html

**Purpose.** Make visible that a single gate method keeps an invariant under every combination of moves and abilities, while a public field breaks it at exactly the call site that forgot the rule, and that rule changes cost 1 edit versus `c` edits.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (move panel on top).

- **Left panel, "Moves".** Five buttons, each labelled with a generic move name and its request: "Sharpen +2", "Howl +1", "Growl −1", "Charm −2", "Power-Up +1 (buggy)". Do not use Pokémon art or names other than in the caption text "Model based on Pokémon stat stages (Gen III+)". Below the buttons: an ability selector (None, Simple, Contrary), a design toggle ("Encapsulated class" / "Public field"), and a Reset button.
- **Right panel, "Stage over time".** A step chart. x-axis: action number 0 to 20 (scrolls or rescales after 20). y-axis: stage from −10 to +10 with gridlines at every integer. The band −6 to +6 shaded with the palette's safe colour; outside the band shaded with the warning colour. Points that land outside the band draw in the warning colour with a marker.
- **Readout row** under the chart: current stage, current multiplier as a fraction and decimal (3 dp), last requested delta, last modified delta, last applied delta, and the log line.
- **Files-edited panel** (small table under the readout): rows "Add Simple", "Add Contrary", "Change cap to ±4"; columns "Public field" = number of move buttons (5), "Encapsulated" = 1. When the ability selector is set to Simple or Contrary in Public-field mode, highlight that row and show a note "each move file must now double/reverse its own delta; the buggy move does not".

**Behaviour.**

- Encapsulated mode, for every button: `d' = modify(d)` per ability (Simple ×2, Contrary ×−1), `new = clamp(n + d', −6, 6)`, `applied = new − n`. Log: applied > 0 "rose", applied < 0 "fell", applied = 0 and d' > 0 "won't go any higher", applied = 0 and d' < 0 "won't go any lower".
- Public-field mode: the four correct moves compute `new = clamp(n + d', −6, 6)` but apply the ability only if the ability was present when "the move file was written", which the spec simplifies as: the ability modifier is **not** applied in public-field mode (the files were not updated). "Power-Up +1 (buggy)" computes `new = n + d` with no clamp and no ability.
- Multiplier for any stage `n`, including out-of-range: `max(2, 2+n) / max(2, 2−n)`. Show out-of-range multipliers in the warning colour.

**The one insight the visual must make obvious.** In encapsulated mode the line never leaves the shaded band, whatever you press. In public-field mode it leaves the band only after the buggy button, and the multiplier readout shows a value larger than 4 or smaller than 1/4.

**Test values (the builder must reproduce these exactly).**

1. Encapsulated, no ability, press Sharpen ×4: stages 2, 4, 6, 6; applied 2, 2, 2, 0; multipliers 2, 3, 4, 4; fourth log line "won't go any higher".
2. Encapsulated, Simple, press Sharpen ×2: stages 4, 6; applied 4, 2; multipliers 3, 4.
3. Encapsulated, Contrary, press Sharpen ×4: stages −2, −4, −6, −6; multipliers 1/2, 1/3, 1/4, 1/4.
4. Public field, no ability, press Sharpen ×3 then Power-Up ×2: stages 2, 4, 6, 7, 8; last multiplier 5 (shown as warning).
5. Encapsulated, press Growl ×7: stages −1 … −6, −6; last multiplier 1/4; last log "won't go any lower".

**Accessibility.** All buttons keyboard reachable; the chart has an `aria-live` text summary of the last action; respects reduced motion (no animated line drawing).
