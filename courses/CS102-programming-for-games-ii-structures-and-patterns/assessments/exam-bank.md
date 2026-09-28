# CS102 · Exam bank: practice, quiz and code-review questions

CS102 has no written exam. The grade comes from the labs (40%, see [labs-brief.md](labs-brief.md)), the pattern project (25%, [pattern-project-brief.md](pattern-project-brief.md)) and the final data-driven combat module (35%, [final-module-brief.md](final-module-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one is a code trace or a compute question with new values, and one asks you to explain or critique.
- **Code review.** The pattern project demo and the week 15 code review of the final module both include oral questions in the style of this bank. Examiners rewrite them with the classes, numbers and data files from your own submission.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model to values you have not seen before.
- **code**: trace what a piece of Python prints or does, or write a short function or test.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a structure or pattern for a stated situation and justify it.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet was run with Python 3.13 and every number was recomputed in Python. Write your own answer before you open the solution.

---

## Week 1: Classes, objects, encapsulation

1. *Week 1 · compute.* A Pokémon-style `StatStages` object (lecture section 2) has the ability Simple and starts at stage 0. It receives four requests in order: `change(+1)`, `change(+3)`, `change(-1)`, `change(-4)`. For each call give the value it returns, the new stage and the new multiplier.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Call | Doubled request | Returns | Stage | Multiplier |
|---|---|---|---|---|
| `change(+1)` | +2 | +2 | +2 | 4/2 = 2 |
| `change(+3)` | +6 | +4 | +6 | 8/2 = 4 |
| `change(-1)` | −2 | −2 | +4 | 6/2 = 3 |
| `change(-4)` | −8 | −8 | −4 | 2/6 = 1/3 |

Simple doubles each request before the clamp. The second call asks for `2 + 6 = 8`, which clamps to 6, so only 4 stages were applied. The fourth call asks for `4 − 8 = −4`, which is inside the range, so the whole −8 lands. The multiplier for a negative stage is `2 / (2 − n)`, so −4 gives `2/6 = 1/3`.

The order inside `change` is ability first, then clamp, then compute `applied`. Swap the first two and the second call would clamp +3 to +4 and then double it, a different game.
</details>

2. *Week 1 · code.* What does this print, and why? `StatStages` is the class from the lecture.

```python
a = StatStages()
b = a
c = StatStages()
b.change(+2)
c.change(-1)
print(a.stage, b.stage, c.stage, a is b, a == c)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `2 2 -1 True False`

`b = a` does not copy. It gives the one object a second name, so the change through `b` shows through `a`. `c` is a separate object. `a is b` is `True` because both names point at one object. `a == c` is `False` because `StatStages` defines no `__eq__`, so Python falls back to identity, and they are different objects. It would also be `False` under a field-by-field `__eq__`, because the stages differ.

In a game this means that if two fighters are built with `attack=shared_stages`, a Swords Dance on one boosts both.
</details>

3. *Week 1 · compute.* A team stores the attack stage as a public field. Forty move files write it directly, and three of them forgot the clamp. (a) A player chains moves until the stage reads +9. What multiplier does the lecture's formula `max(2, 2 + n) / max(2, 2 − n)` give, and how much harder does that hit than the legal maximum? (b) The designers then add Simple, Contrary and a change of the cap to ±4. How many move files must be edited under the public-field design, and how many files under the encapsulated class?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 11/2 = 5.5, which is 37.5% more than the legal maximum of 4. (b) 120 file edits against 3 edits to one method.

(a) `(2 + 9) / 2 = 5.5`. The cap is +6, where the multiplier is `8/2 = 4`. `5.5 / 4 = 1.375`. The formula is happy to evaluate an illegal stage. Nothing crashes, and the number looks plausible.

(b) Each rule change touches every call site under the public field: `3 × 40 = 120` edits, and each is a fresh chance to repeat the forgotten-clamp mistake. With the class, each rule is one edit inside `change`, so 3 edits, all in one file.
</details>

4. *Week 1 · code.* Write a class `Ammo` with a clip size and a reserve. Its invariant is `0 <= rounds <= clip_size` and `reserve >= 0`. It needs read-only `rounds` and `reserve`, a `fire()` that returns `True` if a round was fired, and a `reload()` that moves rounds from the reserve into the clip and returns how many it moved. A new `Ammo(6, 8)` starts full. Then give the output of: fire four times, print `rounds`, call `reload()` and print what it returns, then print `rounds` and `reserve`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** one correct class, and the output `2`, `4`, `6 4`.

```python
class Ammo:
    def __init__(self, clip_size, reserve):
        if clip_size <= 0 or reserve < 0:
            raise ValueError("clip_size must be positive and reserve non-negative")
        self._clip_size = clip_size
        self._rounds = clip_size
        self._reserve = reserve

    @property
    def rounds(self):
        return self._rounds

    @property
    def reserve(self):
        return self._reserve

    def fire(self):
        if self._rounds == 0:
            return False
        self._rounds -= 1
        return True

    def reload(self):
        loaded = min(self._clip_size - self._rounds, self._reserve)
        self._rounds += loaded
        self._reserve -= loaded
        return loaded
```

After four shots the clip holds `6 − 4 = 2`. `reload` wants 4 rounds and the reserve has 8, so it moves `min(4, 8) = 4`. The clip is 6 and the reserve is 4.

Keep going to check the edges. Six more shots empty the clip, a seventh returns `False`, `reload()` then moves `min(6, 4) = 4` and a second `reload()` returns 0. Returning the amount moved lets the UI show "+4", not "+6".
</details>

5. *Week 1 · critique.* Find three problems with this class and rewrite it.

```python
class Stamina:
    def __init__(self, max_sp):
        self.max_sp = max_sp
        self._sp = max_sp

    def get_sp(self):
        return self._sp

    def set_sp(self, value):
        self._sp = value

    def sprint(self, dt):
        self.set_sp(self.get_sp() - 20 * dt)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** the setter guards nothing, `sprint` can drive stamina negative, and `max_sp` is public, so a caller can lower it below the current value.

- `set_sp` is the getter-and-setter pair the lecture warns about. It adds typing and protects no rule, so every caller can write any value.
- `sprint` subtracts with no floor. Sprinting for 6 s from 100 leaves −20, and every system reading `get_sp()` must now guess what a negative means.
- `max_sp` is a plain public attribute. Setting it to 50 while `_sp` is 100 breaks `0 <= sp <= max_sp` without touching `_sp`.

A version with one gate per rule:

```python
class Stamina:
    def __init__(self, max_sp):
        if max_sp <= 0:
            raise ValueError("max_sp must be positive")
        self._max_sp = max_sp
        self._sp = max_sp

    @property
    def sp(self):
        return self._sp

    @property
    def max_sp(self):
        return self._max_sp

    def spend(self, amount):
        if amount < 0:
            raise ValueError("amount must be non-negative")
        before = self._sp
        self._sp = max(0, self._sp - amount)
        return before - self._sp          # what was actually spent

    def sprint(self, dt):
        return self.spend(20 * dt)
```

A negative `amount` raises instead of clamping, because it signals a programming error, not a design limit.
</details>

## Week 2: Inheritance vs composition

6. *Week 2 · compute.* A tower-defence game has five capabilities, Render (R), Collide (C), Move (M), Health (H) and Shoot (S), and seven entity types, listed in this order: Decoration {R}, PathTrigger {C}, Wall {R, C, H}, Projectile {R, C, M}, Creep {R, C, M, H}, Tower {R, C, H, S}, Gunship {R, C, M, H, S}. Build the best single-inheritance tree with the lecture's rule (smallest set first, ties by list order; parent is the placed class with the largest subset, ties to the earliest placed). Give each class's parent and what it must write, the total implementations, the duplicates, and the god-class unused slots.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9 implementations for 5 capabilities, 4 duplicates, and 14 of 35 god-class slots unused. Components need 5 implementations and 0 unused slots.

| Class | Parent | Writes |
|---|---|---|
| Decoration | Entity | R |
| PathTrigger | Entity | C |
| Wall | Decoration | C, H |
| Projectile | Decoration | C, M |
| Creep | Wall | M |
| Tower | Wall | S |
| Gunship | Creep | S |

Sum of the right column: `1 + 1 + 2 + 2 + 1 + 1 + 1 = 9`. Collide is written three times (PathTrigger, Wall, Projectile), Move twice (Projectile, Creep) and Shoot twice (Tower, Gunship). That is `9 − 5 = 4` copies.

Creep ties between Wall and Projectile, both size 3. Wall was placed first, so it wins, and the tree now claims "a creep is a wall". Gunship ties between Creep and Tower and takes Creep.

God class: `5 × 7 = 35` slots. Used slots are `1 + 1 + 3 + 3 + 4 + 4 + 5 = 21`, so 14 are unused.
</details>

7. *Week 2 · compute.* The designer adds an eighth type to question 6, a Mine {C, S} that sits on the path and fires once. Rebuild the tree with Mine in the list from the start. What is Mine's parent, what changes in the totals, and how many existing classes does the component design have to change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mine goes under PathTrigger and writes Shoot. Implementations rise to 10, duplicates to 5, god-class unused slots to 17 of 40. The component design changes no classes and adds one data row.

Mine has two capabilities, so it is placed right after the size-1 types. Its largest placed subset is PathTrigger {C}, so the tree now says "a mine is a path trigger" and Shoot is written a third time (Mine, Tower, Gunship). No existing parent changes here, but the is-a claim is the kind the lecture warns about. Edit PathTrigger for a path-only feature and every mine inherits it.

God class: `8 × 5 = 40` slots, `21 + 2 = 23` used, so 17 unused.
</details>

8. *Week 2 · code.* Using the lecture's `GameObject`, `Health`, `Mover` and `Explode` classes, what does this print? Name the gameplay bug the output reveals and one fix. Then say what `odd.get(Health).max_hp` returns and why.

```python
barrel = GameObject("Barrel", Health(30), Explode(4.0))
grenade = GameObject("Grenade", Mover(8, 0), Explode(3.0))

barrel.get(Health).take_damage(25)
barrel.update(0.5)
print("after 25")
barrel.get(Health).take_damage(25)
barrel.update(0.5)
barrel.update(0.5)
for _ in range(3):
    grenade.update(0.5)
print(grenade.get(Mover).x, grenade.get(Health))

odd = GameObject("Odd", Health(10), Health(50))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
after 25
Barrel explodes, radius 4.0
Barrel explodes, radius 4.0
12.0 None
```

and `odd.get(Health).max_hp` is 50.

The first hit leaves 5 hp, so `Explode` stays quiet. The second hit clamps to 0, and from then on `Explode.update` fires on every frame, because it tests a condition ("hp is 0") and not an event ("hp just reached 0"). The barrel explodes twice here and would explode 60 times a second in a game. One fix is a `self.done` flag set on the first explosion. A better fix is to have the owner removed (or an `Exploded` marker added) once it fires, or to trigger on a death event (week 10).

The grenade moves `8 × 0.5 = 4` units per update, 12 after three. It has no `Health`, so its `Explode` never fires. It needs a fuse timer, which lab 02 asks for.

`GameObject` stores components in a dict keyed by type, so the second `Health` overwrites the first. That silent overwrite is worth a check in the constructor.
</details>

9. *Week 2 · compute.* A god-class design has 20 entity types and 9 capabilities, and the types use 3.5 capabilities each on average. (a) How many unused data slots are there? (b) How many capability sets are possible with 9 capabilities? (c) Explain in two sentences why Dungeon Siege, with 21 C++ and 148 scripted components and more than 7,300 object types, could not have used a class tree.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 110 of 180. (b) 512. (c) See below.

(a) `20 × (9 − 3.5) = 110` unused slots out of `20 × 9 = 180`, 61% dead data.

(b) `2^9 = 512`.

(c) With 169 components there are about `2^169` possible capability sets, and 7,300 types is a scattered sample of that space that no single tree of is-a claims can name without massive duplication or a blob base class. A list of parts per type grows by one row per type, whatever combination it uses.
</details>

10. *Week 2 · critique.* A team's hierarchy is `Character → Player`, `Character → NPC → Merchant` and `NPC → Guard`. For the next milestone the designers ask that players can run their own shop stall and that merchants can defend themselves when robbed. Predict what each request does to the tree and propose a design that absorbs both.

<details>
<summary>Answer and worked solution</summary>

**Answer:** both requests cut across the tree, and the fix is to make `Shop` and `Combat` components.

"A player who sells" needs Merchant's shop code on a `Player`. The options are to copy it (duplication), to use multiple inheritance from `Player` and `Merchant` (a diamond on `Character`), or to hoist shop code into `Character` with a flag (the first step of a god class).

"A merchant who fights" needs Guard's combat code on a Merchant, the same problem on a different branch.

The requests show that selling and fighting are independent capabilities, not kinds of character. Build a character from parts: `GameObject("Stallholder", Render(...), PlayerInput(), Shop(stock=...))` and `GameObject("Merchant", Render(...), NpcBrain(), Shop(...), Combat(...))`. Inheritance can stay where it is a single axis with a true is-a, for example `Shop` and `Combat` both inheriting from `Component`.
</details>

## Week 3: Interfaces and polymorphism

11. *Week 3 · code.* Using the lecture's `Grass`, `Wood` and `apply`, what does this print?

```python
world = [Grass("grass"), Wood("crate")]
for element in ["fire", "water", "fire", "water", "water"]:
    print(element, apply(element, world))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
fire [('grass', 'catches fire and spreads'), ('crate', 'burns')]
water [('grass', 'gets wet'), ('crate', 'is put out')]
fire [('grass', None), ('crate', 'burns')]
water [('grass', 'gets wet'), ('crate', 'is put out')]
water [('grass', 'gets wet'), ('crate', None)]
```

Track each object's `state`. Grass goes burning, wet, and then stays wet, because no rule ever dries it, so the second fire does nothing. Wood goes burning, normal ("is put out"), burning again, normal again. The last water finds the crate in state normal, and `Wood.react` only reacts to water when burning.

The trace also shows a design gap the interface does not reveal. Grass never dries. If rain should be temporary, wet needs a timer, which is a state machine (week 11).
</details>

12. *Week 3 · compute.* The chemistry grid has 5 materials and 4 elements. Over a year the team adds 8 materials that each react to 3 elements, then 3 elements that each affect 6 materials. Count the existing code units edited under Design A (type switch), Design B (polymorphism with a default) and Design B′ (one abstract method per element). Which wins?

<details>
<summary>Answer and worked solution</summary>

**Answer:** A edits 24, B edits 18, B′ edits 39. Polymorphism with a default wins, narrowly.

A: each new material adds a branch to each element function it reacts to, `8 × 3 = 24`. New elements are new functions, 0 edits.

B: new materials are new classes, 0 edits. Each new element adds a branch to each material it affects, `3 × 6 = 18`.

B′: there are `5 + 8 = 13` material classes when the elements arrive, and each new abstract method must be added to all 13, `3 × 13 = 39`.

The margin between A and B is small because this plan grows on both axes. If the plan had 4 new elements instead of 3, B would reach 24 and tie A. The decision rests on which axis the content team will actually grow.
</details>

13. *Week 3 · code.* What happens at each marked line? Explain the difference between the two failures.

```python
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

class ReactiveABC(ABC):
    @abstractmethod
    def react(self, element): ...

class SandA(ReactiveABC):
    pass

@runtime_checkable
class Reactive(Protocol):
    def react(self, element): ...

class SandP:
    pass

SandA()                               # line 1
s = SandP()                           # line 2
print(isinstance(s, Reactive))        # line 3
s.react("fire")                       # line 4
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** line 1 raises `TypeError: Can't instantiate abstract class SandA without an implementation for abstract method 'react'`. Line 2 succeeds. Line 3 prints `False`. Line 4 raises `AttributeError: 'SandP' object has no attribute 'react'`.

The abstract base class is nominal and checked at object creation, so the mistake surfaces the moment anyone builds sand. The protocol is structural and checked by the type checker, not by Python at run time. Without a type checker, the missing method surfaces only when some element is finally applied to the sand, possibly deep into a play session. `@runtime_checkable` lets you ask with `isinstance`, but only whether the method names exist.
</details>

14. *Week 3 · design.* For each content plan, choose Design A, B or C and justify it with the grid's growth axis. (a) A roguelike with 6 damage types that will not change and 150 enemy types, most of which resist or are weak to one or two types by a percentage. (b) A physics sandbox with 12 materials that will stay fixed and a steady stream of new tools, each with a unique effect on every material. (c) A farming game with 40 crops and 5 weather events, where every new crop reacts to weather with its own animation and growth logic.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) C, (b) A, (c) B.

(a) Every cell is a number from a small vocabulary (a resistance percentage), like the Pokémon type chart. A table of `enemy × damage type` needs no code per enemy. 150 rows of data beat 150 classes.

(b) Materials are fixed and operations (tools) grow. Group code by column, with one function per tool that switches on the 12 materials. A new tool is a new function and edits nothing. Under B every tool would edit all 12 material classes.

(c) Kinds grow (crops) and each needs its own logic, which a table cannot hold. One class per crop with a default `on_weather` that does nothing keeps each crop in one file. A new weather event would edit only the crops it affects.
</details>

## Week 4: Big-O intuition

15. *Week 4 · compute.* Your measured pair check costs 40 ns and the design gives proximity checks 6 ms of the frame. (a) What is the naive all-pairs `n_max`? (b) You port the check and it becomes 25 times cheaper. What is the new `n_max`, and by what factor did capacity grow?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 548 units. (b) 2,739 units, 5.0 times as many.

(a) `n(n − 1)/2 × 40 ns ≤ 6 ms` gives `n(n − 1) ≤ 2 × 6,000,000 / 40 = 300,000`. `n = (1 + √1,200,001) / 2 ≈ 548.2`, so 548. Check: `548 × 547 / 2 = 149,878` pairs cost 5.995 ms, and 549 units cost 6.017 ms.

(b) At 1.6 ns the limit is `n(n − 1) ≤ 7,500,000`, so `n ≈ 2,739.1`, round down to 2,739. `2,739 / 548 ≈ 5.0 = √25`. A 25× constant-factor speedup buys an O(n²) algorithm only √25 = 5× the units.
</details>

16. *Week 4 · code.* Give the growth class of each fragment. `n` projectiles, `d` dead ids, `k` players, and a queue of `m` jobs.

```python
# (a)
for p in projectiles:
    if p.target_id in dead_ids:          # dead_ids is a list
        p.retarget()

# (b)
dead_set = set(dead_ids)
for p in projectiles:
    if p.target_id in dead_set:
        p.retarget()

# (c)
while queue:                             # queue is a list
    job = queue.pop(0)
    job.run()

# (d)
top10 = sorted(players, key=lambda p: p.score)[-10:]
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) O(n × d). (b) O(n + d). (c) O(m²) in total. (d) O(k log k).

(a) `in` on a list is a hidden linear scan, so each projectile costs up to `d` comparisons. In a big fight both grow, and the fragment behaves like O(n²).

(b) Building the set costs O(d) once, then each membership test is O(1) on average.

(c) Each `pop(0)` shifts every remaining element, so draining `m` jobs costs `(m − 1) + (m − 2) + ... + 0 = m(m − 1)/2` moves. For 10,000 jobs that is 49,995,000 moves. A `deque` with `popleft()` makes it O(m).

(d) The sort dominates. Keeping only the 10 best while scanning once is O(k) if the list is large and this runs every frame.
</details>

17. *Week 4 · explain.* You time a function three times: 5.0 ms at `n = 2,000`, 10.5 ms at `n = 4,000` and 21.0 ms at `n = 8,000`. Which growth class do you suspect, what do you predict at `n = 16,000`, and what result at 16,000 would change your mind?

<details>
<summary>Answer and worked solution</summary>

**Answer:** linear, or n log n. Predict about 42 ms.

Doubling `n` multiplied the time by 2.1 and then 2.0. Quadratic work would have multiplied it by 4 each time. "A bit more than twice" is also the signature of O(n log n), and at these sizes the two are hard to tell apart. The next doubling predicts `21 × 2 = 42` ms (or a little more for n log n). A result near `21 × 4 = 84` ms would mean a quadratic term that only starts to dominate above 8,000, for example a nested loop over a list that is usually short.
</details>

18. *Week 4 · compute.* A world is 1,500 × 1,500 units with a 10-unit interaction radius and 3,000 units spread evenly. (a) How many cells does a radius-sized uniform grid have, and how many pair checks does the lecture's estimate `4.5 n² / C` give? (b) How many does the naive check make, and what is the ratio? (c) A world boss pulls all 3,000 units into a 30 × 30 area. What happens to the grid's advantage?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 22,500 cells and about 1,800 checks. (b) 4,498,500 checks, about 2,500 times as many. (c) It mostly disappears.

(a) `C = (1,500 / 10)² = 150² = 22,500`. `4.5 × 3,000² / 22,500 = 1,800`.

(b) `3,000 × 2,999 / 2 = 4,498,500`. `4,498,500 / 1,800 ≈ 2,499`.

(c) A 30 × 30 area covers about 9 cells, so almost every unit is within one cell of every other, and the grid checks head back toward `n²/2`. The lecture's clustered run shows the grid doing about 60% of the naive checks. When the number of genuinely close pairs is quadratic, no structure can report them without touching them.
</details>

19. *Week 4 · code.* Simulate a dynamic array that starts with capacity 1 and doubles whenever it is full. Append 1,000 elements. How many resizes happen, how many element copies in total, and how many copies per append on average? Write the loop that counts them.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 10 resizes, 1,023 copies, about 1.02 copies per append.

```python
cap, size, copies, resizes = 1, 0, 0, 0
for _ in range(1000):
    if size == cap:
        copies += size
        cap *= 2
        resizes += 1
    size += 1
print(resizes, copies, cap)        # 10 1023 1024
```

The copies are `1 + 2 + 4 + ... + 512 = 1,023`, which is less than `2n`. Spread across 1,000 appends that is about one copy each, so `append` is amortized O(1). The single append that copies 512 elements still happens in one frame, which is why you preallocate when a hitch matters more than the average.
</details>

## Week 5: Arrays, linked lists and hash maps

20. *Week 5 · compute.* A UI resolves `q = 400` item ids per frame from a database of `n = 6,000` items. Use `c_scan = 15 ns` and `c_hash = 30 ns`. (a) Per-frame cost with a list and with a dict. (b) Per-frame cost with a list if every id is stale (not in the database). (c) The largest `n` for which the list stays under a quarter of a 16.67 ms frame.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 18.00 ms against 0.012 ms. (b) 36.0 ms. (c) about 1,388 items.

(a) List: `400 × 15 ns × (6,000 + 1)/2 = 400 × 15 ns × 3,000.5 = 18.00 ms`, more than a whole frame. Dict: `400 × 30 ns = 12 µs`.

(b) A missing id cannot stop early, so each lookup costs `n = 6,000` comparisons: `400 × 15 ns × 6,000 = 36.0 ms`. The dict costs the same 12 µs for misses.

(c) A quarter of the frame is 4.1675 ms. `(n + 1)/2 = 4.1675 ms / (400 × 15 ns) = 694.6`, so `n ≈ 1,388`.
</details>

21. *Week 5 · code.* An 8-bucket hash table uses integer keys, `hash(k) = k`, and linear probing. Insert 12, 20, 4, 13 and 28 in that order. Where does each key land? How many key comparisons does a lookup of 28 take, and of 36 (which is not in the table)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 12 → 4, 20 → 5, 4 → 6, 13 → 7, 28 → 0. Looking up 28 takes 5 comparisons. Looking up 36 takes 5 comparisons and then stops at an empty bucket.

- 12 mod 8 = 4, free.
- 20 mod 8 = 4, taken, probe to 5.
- 4 mod 8 = 4, taken, probe 5 (taken) and land on 6.
- 13 mod 8 = 5, taken, probe 6 (taken) and land on 7.
- 28 mod 8 = 4, probe 4, 5, 6 and 7, wrap to 0, free.

Lookup 28 compares at buckets 4, 5, 6, 7 and 0. Lookup 36 (36 mod 8 = 4) compares the same five keys, then finds bucket 1 empty and returns "not found". Four keys that share bucket 4, plus 13 landing in the run, built one long cluster. That is the cost of bad hash spread in miniature.
</details>

22. *Week 5 · code.* What does this print, and why? What would the C# version of the same bug look like to a player?

```python
class Pos:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

p = Pos(1, 2)
units = {p: "archer"}
print(p in units, units.get(Pos(1, 2)))
p.x = 5
print(p in units, units.get(Pos(5, 2)), units.get(Pos(1, 2)), len(units))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
True archer
False None None 1
```

After `p.x = 5`, `hash(p)` changes, so a lookup of `p` goes to a different bucket and finds nothing. A lookup by the old position `Pos(1, 2)` goes to the right bucket but the stored key now compares equal to `(5, 2)`, not `(1, 2)`, so it fails too. The archer is still in the dict (`len` is 1) and nothing can find it.

To a player this is a unit that is visibly standing on a tile and yet cannot be selected, targeted or healed there. Key by something that never changes (the unit id), or remove and re-insert when the position changes.
</details>

23. *Week 5 · design.* Pick a structure for each access pattern and give the cost of the most frequent operation. (a) An MMO client checks, for every one of 3,000 NPCs each frame, whether that NPC is in combat with the local player. (b) A chat window keeps the last 200 lines. (c) A wardrobe screen shows whether each of 4,000 cosmetics is owned. (d) The list of active projectiles, updated in order every frame and never searched.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) a set of NPC ids in combat with the player, O(1) per check. (b) `deque(maxlen=200)`, O(1) append and automatic drop of the oldest. (c) a set of owned cosmetic ids, O(1) per cosmetic, 4,000 checks per screen. (d) a list, O(n) per frame to walk, which is the cheapest traversal.

Why not the obvious alternatives. (a) A list of the player's combat partners scanned per NPC is O(k) each, O(3,000 × k) per frame. (b) A list with `pop(0)` shifts up to 199 lines on every new line. (c) Scanning an owned list of, say, 1,500 items per cosmetic is about `4,000 × 750 = 3,000,000` comparisons, roughly 45 ms at 15 ns. (d) A dict keyed by projectile id costs memory and slows iteration for a lookup nobody makes.
</details>

## Week 6: Queues and stacks

24. *Week 6 · code.* Use the lecture's box puzzle (7 × 5, walls on the edge, player at (2, 2), box at (3, 2), y grows downward) and `History` with a cleared redo stack. Run the script below and give the player, the box and both stacks after every step.

Script: run D, run R, run U, run R, undo, undo, run R, redo.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Step | Action | Player | Box | UNDO (bottom → top) | REDO |
|---|---|---|---|---|---|
| 1 | run D | (2, 3) | (3, 2) | D | — |
| 2 | run R | (3, 3) | (3, 2) | D, R | — |
| 3 | run U | (3, 2) | (3, 1) | D, R, U* | — |
| 4 | run R | (4, 2) | (3, 1) | D, R, U*, R | — |
| 5 | undo | (3, 2) | (3, 1) | D, R, U* | R |
| 6 | undo | (3, 3) | (3, 2) | D, R | R, U* |
| 7 | run R | (4, 3) | (3, 2) | D, R, R | — |
| 8 | redo | (4, 3) | (3, 2) | D, R, R | — (returns `False`) |

Step 3 pushes the box up from (3, 2) to (3, 1), so the command records `pushed = True`. Step 6 undoes it and pulls the box back down to (3, 2). Step 7 is a new action after an undo, so REDO is cleared, and the redo at step 8 has nothing to do.
</details>

25. *Week 6 · code.* Same puzzle, but `History(limit=2)`. Run R, run R, run D, run L, then press undo three times. Give the final player and box positions and both stacks. Why does the third undo do nothing?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the player ends at (4, 2), the box at (5, 2), UNDO is empty and REDO holds `L, D` (bottom to top).

After the four moves the player is at (3, 3) and the box at (5, 2). UNDO can hold only 2 commands, so the two pushes `R*, R*` fell off the bottom as D and L arrived, and UNDO is `D, L`. The first undo reverses L (player to (4, 3)), the second reverses D (player to (4, 2)). The third finds UNDO empty and returns `False`. The two box pushes can no longer be undone, which is the design cost of a bounded history. With a limit of 2 the player cannot get back to the start.
</details>

26. *Week 6 · compute.* A move animation lasts 120 ms. A player taps at 0, 30, 60, 90, 200 and 210 ms. Using the lecture's input buffer (a full `deque(maxlen=k)` drops the oldest waiting press), give the move start times and the time the character stops for `maxlen` unlimited, 2, 1 and 0.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `maxlen` | Move starts (ms) | Moves | Stops at |
|---|---|---|---|
| unlimited | 0, 120, 240, 360, 480, 600 | 6 | 720 ms |
| 2 | 0, 120, 240, 360 | 4 | 480 ms |
| 1 | 0, 120, 240 | 3 | 360 ms |
| 0 | 0, 200 | 2 | 320 ms |

Trace `maxlen = 1`. Tap 0 starts at once (busy to 120). Taps 30, 60 and 90 each replace the waiting press. At 120 the waiting press starts (busy to 240). Tap 200 waits and tap 210 replaces it. At 240 it starts, busy to 360, and the queue is empty.

With `maxlen = 0`, only presses that arrive while idle count. 30, 60 and 90 are lost. 200 arrives after 120, so it starts. 210 is lost.

Unlimited obeys all six taps but walks for 510 ms after the last one. One waiting press keeps the tap at 210 and stops 150 ms after it.
</details>

27. *Week 6 · compute.* A level editor uses snapshot undo on a 128 × 128 tile map at 1 byte per tile and keeps 300 undo steps. (a) How much memory does the history use? (b) How much would 300 command records of 12 bytes each use, and what is the ratio? (c) Name one operation where the command design should store a small snapshot anyway.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4,915,200 bytes, about 4.7 MiB. (b) 3,600 bytes, about 1,365 times smaller. (c) A flood fill or a random scatter.

(a) One snapshot is `128 × 128 = 16,384` bytes. `300 × 16,384 = 4,915,200`.

(b) `300 × 12 = 3,600`. `4,915,200 / 3,600 ≈ 1,365`.

(c) A flood fill that changes thousands of tiles cannot be reversed from `(x, y, new_tile)`. The command should store the list of tiles it changed, which is a snapshot of just that region.
</details>

28. *Week 6 · critique.* Find every bug in this `History` and give the symptom a player would see for each. The trace below is from the lecture's puzzle, starting at (2, 2).

```python
class History:
    def __init__(self):
        self.undo_stack, self.redo_stack = [], []

    def run(self, cmd, board):
        ok = cmd.do(board)
        self.undo_stack.append(cmd)
        return ok

    def undo(self, board):
        cmd = self.undo_stack.pop(0)
        cmd.undo(board)
        self.redo_stack.append(cmd)
```

Script: run U (player to (2, 1)), run U (blocked by the wall), run R (player to (3, 1)), undo, undo.

<details>
<summary>Answer and worked solution</summary>

**Answer:** after the first undo the player stands on the box at (3, 2). After the second the player is at (3, 3), a cell they never visited. There are four bugs.

- **Blocked moves are pushed.** `run` appends even when `do` returned `False`. Undoing a move that never happened still moves the player backward, which is why the second undo walks from (3, 2) to (3, 3).
- **`pop(0)` takes the oldest command.** Undo reversed the first U, not the last R. Applied to the current position (3, 1), it moved the player down to (3, 2), onto the box. A stack must pop from the end.
- **REDO is never cleared on a new action**, so a later redo could replay commands against a board they were not made for.
- **No empty check.** Undo on an empty history raises `IndexError` instead of returning `False`.

`pop(0)` is also O(n), but that is the least of its problems here.
</details>

## Week 7: Trees, scene graphs and skill trees

29. *Week 7 · compute.* A tank sits at (0, 0) facing 90°. Its turret is at local (10, 0) with angle 45°, the barrel at local (30, 0) with angle 0° and the muzzle at local (20, 0). (a) Give the world position and angle of the turret, barrel and muzzle, to one decimal. (b) The barrel's local angle changes to −45°. Which world positions change, and where does the muzzle end up?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) turret (0.0, 10.0) at 135°, barrel (−21.2, 31.2) at 135°, muzzle (−35.4, 45.4) at 135°. (b) Only the muzzle moves, to (−21.2, 51.2), and the barrel and muzzle now face 90°.

(a) The turret's offset is rotated by the tank's angle: `R(90°)·(10, 0) = (0, 10)`. Its own 45° adds to its world angle, 135°, but does not move it. The barrel steps 30 units at 135°, which is `(30 cos 135°, 30 sin 135°) = (−21.2, 21.2)`, from (0, 10) to (−21.2, 31.2). The muzzle steps 20 more at 135°, `(−14.1, 14.1)`, to (−35.4, 45.4).

(b) The barrel's own angle rotates its children's offsets, not its own position, so the barrel stays at (−21.2, 31.2). Its world angle becomes `135 − 45 = 90°`, so the muzzle is 20 units straight up the y axis, at (−21.2, 51.2).
</details>

30. *Week 7 · code.* A tree has root `Root` with children `A` and `B` (in that order). `A` has children `A1` and `A2`, `A2` has a child `X`, and `B` has a child `B1`. Give the pre-order, post-order and level-order sequences, and the subtree sizes of `A`, `A2` and `Root`.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- Pre-order: Root, A, A1, A2, X, B, B1.
- Post-order: A1, X, A2, A, B1, B, Root.
- Level order: Root, A, B, A1, A2, B1, X.
- Subtree sizes: A is 4, A2 is 2, Root is 7.

Pre-order visits a node before its children, so it walks down the A branch fully before touching B. Post-order finishes every child before the parent, so Root is last. Level order uses a queue and finishes depth 1 (A, B) before depth 2 (A1, A2, B1) before depth 3 (X).

If these were scene nodes, pre-order is the order to push world transforms down. If they were bags inside bags, post-order is the order to total their weights.
</details>

31. *Week 7 · compute.* An invented tank skill tree has `Shield Bash` (1 point) as root, with children `Taunt` (1) and `Fortify` (2). `Taunt` leads to `Rally` (2). `Fortify` leads to `Iron Wall` (3), which leads to `Last Stand` (5). (a) Give `path_cost` for every skill. (b) A player has learned Shield Bash, Taunt, Fortify, Iron Wall and Rally. What does `refund(Fortify)` return, and what is still learned afterwards?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Shield Bash 1, Taunt 2, Fortify 3, Rally 4, Iron Wall 6, Last Stand 11. (b) 5 points. Shield Bash, Taunt and Rally stay learned.

(a) `path_cost` adds costs up to the root. Last Stand is `5 + 3 + 2 + 1 = 11`.

(b) `refund` is post-order over Fortify's subtree. Last Stand is not learned and returns 0. Iron Wall returns 3. Fortify adds its own 2. Total 5. The Taunt branch is outside the subtree and untouched.
</details>

32. *Week 7 · code.* An invented lightning school is a DAG. `Spark` (1 point) has no prerequisites. `Static` (2) and `Arc` (2) require Spark. `Chain` (3) requires Static and Arc. `Storm` (5) requires Chain and Arc. Write a function that returns the total points to learn a skill from nothing, counting each ancestor once. What does it return for Storm, and what would a naive "cost plus the cost of each parent's path" recursion return?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 13 points. The naive recursion returns 17.

```python
PREREQS = {"Spark": [], "Static": ["Spark"], "Arc": ["Spark"],
           "Chain": ["Static", "Arc"], "Storm": ["Chain", "Arc"]}
COST = {"Spark": 1, "Static": 2, "Arc": 2, "Chain": 3, "Storm": 5}

def ancestors(skill, seen=None):
    seen = set() if seen is None else seen
    for p in PREREQS[skill]:
        if p not in seen:
            seen.add(p)
            ancestors(p, seen)
    return seen

def total_cost(skill):
    return COST[skill] + sum(COST[a] for a in ancestors(skill))
```

Storm's ancestor set is {Chain, Static, Arc, Spark}, so `5 + 3 + 2 + 2 + 1 = 13`. The naive version walks every path: Storm 5, plus Chain's path `3 + (2 + 1) + (2 + 1) = 9`, plus Arc's path `2 + 1 = 3`, for 17. It counts Arc twice and Spark three times. This is the week 7 point about Diablo II's Blizzard, which has two prerequisites: once a node can have several parents, you must collect a set.
</details>

33. *Week 7 · compute.* A scene tree has one root with 4 children, each child has 5 children, and each of those has 2 children. (a) How many nodes are there? (b) If every node's world transform is computed with the recursive `world()` that climbs to the root, and each link climbed counts as one step, how many steps does one full update take? (c) How many does the single pre-order `update_world` pass take?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 65. (b) 164. (c) 65, one per node.

(a) `1 + 4 + 20 + 40 = 65`.

(b) The climb from a node costs its depth. `4 × 1 + 20 × 2 + 40 × 3 = 164`.

(c) The pre-order pass hands each child its parent's result, so each node is computed once. The gap grows with depth. In a tree whose average depth is 8, the naive version does about 8 times the work.
</details>

## Week 8: Graphs, maps and dialogue

34. *Week 8 · code.* A map is stored as an adjacency list. Run the lecture's `bfs(MAP, "Camp")` by hand. Give the queue after each dequeue, `dist` for every room, and the paths to Lake and to Tower. Then give `dist` from Tower.

```python
MAP = {
    "Camp":   ["Bridge", "Forest"],
    "Bridge": ["Camp", "Mill"],
    "Forest": ["Camp", "Cave", "Mill"],
    "Mill":   ["Bridge", "Forest", "Tower"],
    "Cave":   ["Lake"],
    "Lake":   ["Cave", "Tower"],
    "Tower":  ["Mill"],
}
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Step | Dequeue | Newly seen (dist) | Queue after |
|---|---|---|---|
| 1 | Camp | Bridge (1), Forest (1) | Bridge, Forest |
| 2 | Bridge | Mill (2) | Forest, Mill |
| 3 | Forest | Cave (2) | Mill, Cave |
| 4 | Mill | Tower (3) | Cave, Tower |
| 5 | Cave | Lake (3) | Tower, Lake |
| 6 | Tower | none | Lake |
| 7 | Lake | none | empty |

Paths: Camp, Forest, Cave, Lake (3 moves) and Camp, Bridge, Mill, Tower (3 moves). At step 3 Forest also links to Mill, but Mill already has distance 2 through Bridge.

From Tower: Tower 0, Mill 1, Bridge 2, Forest 2, Camp 3, Cave 3, Lake 4. `V = 7`, `E = 14`. Camp to Lake is 3 moves, Lake to Camp is 4 (Lake, Tower, Mill, Forest or Bridge, Camp), because the drops Forest → Cave and Lake → Tower are one-way.
</details>

35. *Week 8 · code.* Run the lecture's `bfs` and three-line linter on this dialogue, with `endings = {"bye"}`. List the unreachable lines, dead ends and broken links, and give the shortest route to `reward`.

```python
D = {
    "start":       ["ask_job", "ask_town", "bye"],
    "ask_job":     ["accept", "decline", "start"],
    "accept":      ["reward"],
    "decline":     ["start"],
    "ask_town":    ["town_lore", "mayor"],
    "town_lore":   [],
    "reward":      ["bye"],
    "bonus_offer": ["accept"],
    "bye":         [],
}
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** unreachable `["bonus_offer"]`, dead ends `["town_lore"]`, broken links `[("ask_town", "mayor")]`. The shortest route to reward is start, ask_job, accept, reward (3 choices).

BFS gives start 0; ask_job, ask_town and bye 1; accept, decline and town_lore 2; reward 3. `mayor` is skipped because `bfs` checks `w in graph` before queuing, so the broken link does not crash the search. Nothing points at `bonus_offer`, so it never gets a distance. `town_lore` is reachable, has no choices and is not an ending, so a player who asks about the town is stuck.
</details>

36. *Week 8 · code.* A quest-prerequisite graph is `{"intro": ["rats"], "rats": ["cellar"], "cellar": ["key"], "key": ["vault"], "vault": ["cellar"], "smith": ["rats", "ore"], "ore": []}`. What does the lecture's `find_cycle` return? Which part of the result is the cycle, and why is a cycle here a bug when a cycle in a conversation is not?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `['intro', 'rats', 'cellar', 'key', 'vault', 'cellar']`. The cycle is cellar → key → vault → cellar.

`find_cycle` returns the DFS path from where it started plus the edge back to a grey node. The loop starts at the first occurrence of the repeated node, `cellar`. The prefix intro → rats is just how DFS got there.

In a prerequisite graph an edge means "must be completed before". Cellar needs key, key needs vault and vault needs cellar, so none of the three can ever start. In a dialogue, an edge means "can be said next", and returning to an earlier line ("never mind") is normal.
</details>

37. *Week 8 · explain.* (a) On the graph `{"S": ["A", "B"], "A": ["T"], "B": ["C"], "C": ["T"], "T": []}`, what path to T does BFS record from S, and what path does a stack-based DFS record if it marks nodes when pushed and pops from the end? (b) A dialogue graph has 5,000 lines with 3 choices each on average. Compare an adjacency matrix and an adjacency list in stored entries.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) BFS finds S, A, T (2 edges). DFS finds S, B, C, T (3 edges). (b) 25,000,000 cells against 20,000 entries, 1,250 times smaller.

(a) DFS pushes A and B, then pops B first (last in), follows B → C → T and marks T through C. When A is finally popped, T is already seen. Both searches reach the same set of nodes. Only BFS guarantees the fewest edges.

(b) Matrix: `5,000² = 25,000,000`. List: `5,000 + 5,000 × 3 = 20,000`.
</details>

## Week 9: The Component pattern

38. *Week 9 · compute.* A world has 25,000 entities. Every entity has Position and Health. Render is on 80%, Mover on 20%, AI on 4%, Poisoned on 0.2%, and one entity has BossPhase. Five systems query (Render, Position), (Mover, Position), (AI, Position), (Poisoned, Health) and (BossPhase, Health). Count checks per frame for polling and for the smallest-set index. What fraction of polling is the index?

<details>
<summary>Answer and worked solution</summary>

**Answer:** polling 125,000 checks, index 26,051 checks, about 21%.

Polling: `5 × 25,000 = 125,000`.

Index, smallest set per query: `20,000 + 5,000 + 1,000 + 50 + 1 = 26,051`. `26,051 / 125,000 = 0.208`.

Render saves only 20% because nearly everything renders. The boss system does 1 check instead of 25,000. The rarer the component, the larger the win.
</details>

39. *Week 9 · compute.* In a 6,000-entity battle, a `WasHit` component is added to 4,000 entities and removed from 4,000 entities every frame. Two systems query it. Using the lecture's counting rule (one index update per add or remove, one check per entity visited), which is cheaper per frame, polling or indexing `WasHit`? What would you do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** polling, 12,000 operations against 16,000.

Polling: `2 × 6,000 = 12,000` checks.

Index: `4,000 + 4,000 = 8,000` updates, plus `2 × 4,000 = 8,000` visits, total 16,000.

Indexing moves cost from reads to writes, and this component churns faster than it is read. Make "was hit this frame" a field on an existing component, or build a plain list of hit entities once per frame and let both systems read it.
</details>

40. *Week 9 · code.* A world holds four entities in spawn order, each with Health and Render: crate (3 hp, Burning 5), barrel (10 hp, Burning 5), goblin (20 hp, not burning) and chest (4 hp, Burning 5). The burn system subtracts 5 from each burning entity and removes those at 0 hp or below. Then a render query lists what it draws, then `flush()` runs. What happens in each of the three designs? (a) The burn loop iterates the live index dict and removes dead entities at once. (b) `query` returns a copy and dead entities are removed at once. (c) `query` returns a copy and dead entities are passed to `destroy()`, removed in `flush()`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `RuntimeError: dictionary changed size during iteration`. (b) Render draws barrel and goblin. (c) Render draws crate, barrel, goblin and chest, and after `flush` only barrel and goblin remain.

(a) The crate dies on the first iteration and its removal shrinks the dict being iterated, so Python stops the loop.

(b) The copy protects the loop, and later systems no longer see the dead entities.

(c) Deferred destruction keeps every entity alive until the fixed point at the end of the frame, so render still draws the crate and chest this frame at 0 hp or below. That is the price of the design. It removes crashes and half-removed entities, and in return every system that runs between `destroy` and `flush` must skip doomed entities, for example by checking `hp > 0` or a `doomed` flag in the query. Engines with a `queue_free` style call leave the same decision to you.
</details>

41. *Week 9 · design.* Order these systems for one frame and give one sentence of reason for each boundary: `render`, `move`, `collision`, `input`, `ai`, `damage`, `flush`. Then choose, for each pair, shared state, a direct reference or a message: (a) AI steering and movement; (b) a boss's Health and its on-screen health bar; (c) a death and the quest, achievement and loot systems.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `input, ai, move, collision, damage, render, flush`. (a) shared state, (b) a direct reference, (c) a message.

Gather intent first (input, AI), then apply it (move), then resolve what the new positions caused (collision, then damage), then show the result (render, skipping entities that damage doomed this frame, since deferred destruction keeps them in every query until flush), then remove the dead once (flush). Collision before move tests last frame's positions, a one-frame lag. Damage after render draws a unit alive in the frame it died, so every picture is one frame behind the damage.

(a) AI writes `Mover.vx, vy` every frame and move reads them. Neither needs to know the other. (b) The two always travel together, and the bar reads every frame, so a reference is simplest and fastest. (c) One fact, many interested and changing listeners. That is week 10's event bus.
</details>

## Week 10: Observer and events

42. *Week 10 · code.* Using the lecture's `EventBus` (with the copy in `emit`), `KillQuest` and `Achievement`, run this session. What are `quest.count`, `ach.count`, `ach.unlocked` and `bus.calls` at the end? Build the per-listener call table.

```python
bus = EventBus()
quest = KillQuest(bus, "wolf", 5)
ach = Achievement(bus, "wolf", 16)
done = []
bus.subscribe("quest_completed", lambda name: done.append(name))
log = []
bus.subscribe("enemy_killed", lambda kind, killer: log.append(kind))
for k in ["boar", "wolf", "wolf"] * 8:
    bus.emit("enemy_killed", kind=k, killer="p1")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `quest.count = 5`, `ach.count = 16`, `ach.unlocked = True`, `bus.calls = 57`.

| Listener | Calls | Why |
|---|---|---|
| Kill quest | 8 | Wolves are kills 2, 3, 5, 6, 8, ... The 5th wolf is kill 8, then the quest unsubscribes |
| Achievement | 24 | every kill, it filters by kind itself |
| Combat log | 24 | every kill |
| `quest_completed` listener | 1 | emitted once, by the quest |
| **Total** | **57** | |

There are 24 kills and 16 wolves, so the achievement reaches exactly 16.
</details>

43. *Week 10 · code.* Remove the `list(...)` copy from `emit` and rerun question 42. What changes, and which kill is missed by whom? Now set the achievement's target to 12 and rerun without the copy. Why is this version of the bug worse?

<details>
<summary>Answer and worked solution</summary>

**Answer:** with target 16, the achievement misses kill 8, ends at 15 and never unlocks, and `bus.calls` is 56. With target 12 it still unlocks, so the bug is present and invisible.

On kill 8 the listener list is `[quest, achievement, log]`. The loop calls index 0, the quest, which completes and removes itself. The list becomes `[achievement, log]`, and the iterator moves to index 1, which is now the log. The achievement at index 0 is skipped for that one event.

With a target of 12, the achievement still reaches 12 at kill 20 (it only lost one of 16 wolves), so every test that checks "unlocked" passes. The count is wrong by one, and the bug appears only when a target sits exactly at the total a player can reach. That is how "sometimes" bug reports are born.
</details>

44. *Week 10 · compute.* (a) A game runs at `F = 30` updates per second with `N = 400` polling watchers. Each event has `L = 5` listeners. At what event rate do events and polling cost the same? (b) In the same game, 400 enemies subscribe to a 30-per-second `player_moved` event over a session and none unsubscribe on death. How many wasted calls per second are there once all 400 are dead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2,400 events per second. (b) 12,000 calls per second.

(a) The crossover is `E = F × N / L = 30 × 400 / 5 = 2,400`. Below it events are cheaper, above it polling is.

(b) `30 × 400 = 12,000` calls per second to dead enemies, growing across the session. Frame time creeping up the longer you play is the signature of the lapsed listener. The fix is ownership: keep the unsubscribe handle and call it in `destroy()`.
</details>

45. *Week 10 · design.* When a boss dies, seven things happen. Loot is rolled, the dungeon door unlocks, the raid lockout timer starts, the music changes, an achievement is checked, the combat log prints a line, and telemetry records the kill. For each, choose a direct call, a synchronous listener or a queued listener, and name the payload fields `boss_killed` needs so no listener must reach back into the world.

<details>
<summary>Answer and worked solution</summary>

**Answer:** one defensible split. Other splits are fine if each choice has a reason.

| Consequence | Choice | Reason |
|---|---|---|
| Door unlocks | synchronous | a gameplay rule that must hold before the step ends, or players walk into a locked door |
| Lockout timer | synchronous | must be recorded before any player can leave and re-enter |
| Loot roll | synchronous, or a direct call if combat needs the result back | uses the fight's seeded generator, so it must happen at a fixed point |
| Music | queued | presentation, fine one frame late |
| Achievement | queued | bookkeeping |
| Combat log | queued | presentation |
| Telemetry | queued | bookkeeping, and must never stall combat |

Payload: `boss_id`, `boss_kind`, `level`, `killer_ids` (the group), `position`, `time_s`, and the dungeon `instance_id`. With these in the snapshot, a queued listener that runs after the boss entity is deleted still has everything it needs.
</details>

## Week 11: State and state machines

46. *Week 11 · compute.* A character has five booleans. `is_walking`, `is_climbing` and `is_swimming` are mutually exclusive (at most one is true). `is_poisoned` and `is_invisible` combine freely with everything. How many combinations can the flags represent, how many are valid, and how many are illegal? How would you represent the valid ones?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 32 representable, 16 valid, 16 illegal.

`2^5 = 32`. The movement group has 4 valid values (none, walking, climbing or swimming), and the two free flags give `2 × 2 = 4`, so `4 × 4 = 16` valid.

Replace the three movement flags with one `movement` state variable, which cannot hold "climbing and swimming". Keep `is_poisoned` and `is_invisible` as flags, or as two small concurrent machines if they have timers and transitions of their own.
</details>

47. *Week 11 · code.* Using the heroine's transition table from section 1 (a dash means "ignore"), start in `standing` and feed the inputs B, DOWN_PRESS, B, LANDED, DOWN_PRESS, B, DOWN_RELEASE, B. Give the state after each input.

<details>
<summary>Answer and worked solution</summary>

**Answer:** jumping, diving, diving, standing, ducking, ducking, standing, jumping.

B from standing jumps. DOWN_PRESS while jumping dives. B while diving is a dash, so she stays diving. LANDED returns to standing. DOWN_PRESS ducks. B while ducking is a dash, the cell that removed the "jumping in the ducking pose" bug. DOWN_RELEASE stands. B jumps.

As code, the whole machine is a dict lookup with a default:

```python
state = TABLE.get((state, button), state)
```
</details>

48. *Week 11 · compute.* Use the lecture's jump-chain model (4-frame landings, countdown 5, triple jump needs speed above 20, airtimes 20, 24 and 30 frames). Mario's speed is 22. Press 1 is on frame 0, press 2 comes 6 frames after the first touchdown and press 3 comes 8 frames after the second touchdown. On which frame does each jump start, which jump is it, and on which frame is Mario back in `grounded`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** jump on 0, double_jump on 26, triple_jump on 58; grounded again on 92.

| Frame | From → To | Why |
|---|---|---|
| 0 | grounded → jump | first press, timer 0 |
| 20 | jump → jump_land | 20 airborne frames |
| 24 | jump_land → grounded | 4th landing frame, `prev_land = jump_land`, timer 5 |
| 26 | grounded → double_jump | timer reads 3 (5 on 24, 4 on 25, 3 on 26), after a single |
| 50 | double_jump → double_jump_land | 24 airborne frames |
| 54 | double_jump_land → grounded | 4th landing frame, timer 5 |
| 58 | grounded → triple_jump | delay 8 is the last frame of the window, timer reads 1, speed 22 > 20 |
| 88 | triple_jump → triple_jump_land | 30 airborne frames |
| 92 | triple_jump_land → grounded | 4 landing frames |

`jumps(run([6, 8], speed=22))` returns `[(0, 'jump'), (26, 'double_jump'), (58, 'triple_jump')]`. One more frame of delay on the third press and the timer would read 0, giving a hop.
</details>

49. *Week 11 · compute.* Same model, speed 25. The player presses late the first time: press 2 comes 9 frames after the first touchdown, then presses come 3 frames after each later touchdown. List the jumps and their start frames. How many presses does it take to reach a triple jump, and why is it not three?

<details>
<summary>Answer and worked solution</summary>

**Answer:** jump 0, jump 29, double_jump 52, triple_jump 79. Four presses.

The window after a touchdown is `L + C - 1 = 4 + 5 - 1 = 8` frames. Press 2 is on frame 29, 9 frames after the touchdown on 20, and the countdown reads 0, so the grounded row falls through to `jump`. That hop is a fresh single jump. It touches down on 49, the press on 52 is inside `jump_land` and gives a double jump, which lands on 76. The press on 79 is inside `double_jump_land` at speed 25, so it gives the triple. `jumps(run([9, 3, 3], speed=25))` confirms all four frames. A late press does not end the combo; it restarts it.
</details>

50. *Week 11 · compute.* A character has movement (idle, walking, running, jumping), a weapon (none, sword, bow), a status (normal, poisoned, stunned) and a stance (guarded, open). How many states does one flat machine need, and how many do concurrent machines need? Where does "cannot draw the bow while stunned" go?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 72 flat, 12 concurrent. The rule is a guard.

Flat: `4 × 3 × 3 × 2 = 72`. Concurrent: `4 + 3 + 3 + 2 = 12`. Multiply when concerns interact, add when they do not.

The bow rule is a guard on the weapon machine's `EQUIP_BOW` transition that reads the status machine's current state. Merging the two machines to express one rule would bring back the product.
</details>

51. *Week 11 · critique.* A student simplifies the lecture's `step` like this. What goes wrong compared with the lecture's model, which run shows it, and what is the fix?

```python
def step(self, a):
    if self.timer > 0:
        self.timer -= 1
    if self.action == "grounded":
        self.grounded(a)
    elif self.action in AIR_FRAMES:
        self.airborne(a)
    else:
        self.landing(a)
    self.frame += 1
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** a handler that switches action no longer hands the same frame to the new action, so inputs on switch frames are lost and every jump starts a frame late.

On the 4th landing frame, `landing` switches to `grounded` and returns true, but nothing runs `grounded` that frame, so an A press on that frame is dropped. `run([4], speed=25)` shows it: the lecture's model double-jumps on frame 24, the student's version never jumps again. The same missing pass delays the airborne handler after every jump, so the first touchdown moves from frame 20 to 21. The fix is the lecture's loop, `for _ in range(4): ... if not again: break`, which reruns handlers until none switches action. Keep the cap, because the decompilation's own comment warns that a cycle of actions could hang the frame.
</details>

## Week 12: The Command pattern

52. *Week 12 · compute.* A match simulates at 20 ticks per second for 25 minutes. Each player's command is 3 bytes, there are 8 players, and the header is 32 bytes. (a) How big is the command recording? (b) How big is a snapshot recording of 500 entities with 6 fields of 4 bytes each, every tick? (c) What is the ratio?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 720,032 bytes. (b) 360,000,000 bytes. (c) about 500 to 1.

Ticks: `25 × 60 × 20 = 30,000`.

(a) `32 + 30,000 × 3 × 8 = 720,032`.

(b) `30,000 × 500 × 6 × 4 = 360,000,000`, 360 MB.

(c) `360,000,000 / 720,032 ≈ 500`. The command file is small only if the simulation is deterministic, so the recording should also carry a version and periodic checksums.
</details>

53. *Week 12 · compute.* Using the Doom demo format from the lecture (35 tics per second, a 13-byte header, 4 bytes per player per tic, a 1-byte end marker), how big is a 90-second two-player demo? How big would it be if the game ran at 60 tics per second with the same command size?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 25,214 bytes at 35 tics. 43,214 bytes at 60 tics.

`90 × 35 = 3,150` tics. `3,150 × 2 × 4 = 25,200`, plus 13 and 1, gives 25,214.

At 60 tics: `90 × 60 × 2 × 4 = 43,200`, plus 14, gives 43,214. File size grows linearly with tick rate, which is one reason a simulation rate is a design decision and not only a smoothness setting.
</details>

54. *Week 12 · critique.* List every source of nondeterminism in this `step`, say which part of the state each one corrupts, and give the fix for each.

```python
import random, time

class Arena:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.enemies = {"slime", "bat", "wolf"}
        self.last = time.perf_counter()
        self.x = 0.0

    def step(self, buttons, mouse_x):
        now = time.perf_counter()
        dt, self.last = now - self.last, now
        self.x += ((buttons & 8) > 0) * 90 * dt
        if buttons & 16:
            target = next(iter(self.enemies))
            if random.random() < 0.25:
                self.enemies.discard(target)
        self.aim = mouse_x
        if self.rng.random() < 0.01:
            spawn_sparkle_particles()
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** five sources.

| Source | Corrupts | Fix |
|---|---|---|
| `dt` from `perf_counter` | position | a fixed `DT` and a tick counter |
| `next(iter(self.enemies))` on a set of strings | order, which enemy is hit | a list, or sort by a stable id |
| global `random.random()` for the hit | randomness, kills | draw from `self.rng` |
| `mouse_x` read live into `self.aim` | anything aim affects | pack the aim into the recorded command |
| `self.rng` used for a cosmetic sparkle | randomness, every later roll shifts if particle rules change | give presentation its own generator |

The fifth is the Doom `P_Random` and `M_Random` split. It looks harmless because the sparkle has no gameplay effect, but it consumes a number from the gameplay stream, so changing the sparkle rate changes every later hit roll.
</details>

55. *Week 12 · code.* Two versions of `PaintTile` differ only in when they read the old tile. The level has one tile, `"grass"`. What is the tile after each undo, for each version? Which one is right, and what rule does it follow?

```python
class PaintEarly:                      # reads old_tile at creation
    def __init__(self, x, y, new, level):
        self.x, self.y, self.new = x, y, new
        self.old = level.tiles[y][x]
    def execute(self, level): level.tiles[self.y][self.x] = self.new
    def undo(self, level):    level.tiles[self.y][self.x] = self.old

class PaintLate:                       # reads old_tile at execute time
    def __init__(self, x, y, new):
        self.x, self.y, self.new, self.old = x, y, new, None
    def execute(self, level):
        self.old = level.tiles[self.y][self.x]
        level.tiles[self.y][self.x] = self.new
    def undo(self, level):    level.tiles[self.y][self.x] = self.old

# For each version: create a ("water") and b ("lava") first, then
# a.execute, b.execute, b.undo, a.undo
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `PaintEarly` gives grass after undoing b, then grass. `PaintLate` gives water after undoing b, then grass. `PaintLate` is right.

Both early commands read `"grass"` when they were created, before either ran. So undoing b restores grass, erasing a's water, and the history no longer walks back through states that existed. `PaintLate` captures at execute time, so b remembers water and the undo chain is exact. The rule is to capture what you need to reverse at execute time, not at creation, because queued, delayed and network commands run later than they are made.
</details>

56. *Week 12 · compute.* An editor has a 64 MiB undo budget (67,108,864 bytes). The map is 512 × 512 tiles at 2 bytes per tile. How many full-snapshot undo steps fit? How many 20-byte commands?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 128 snapshot steps, 3,355,443 command steps.

One snapshot is `512 × 512 × 2 = 524,288` bytes. `67,108,864 / 524,288 = 128`.

`67,108,864 / 20 = 3,355,443.2`, round down to 3,355,443. In practice the command budget is limited by something else (a step count the designer chooses), and memory stops being the constraint.
</details>

## Week 13: Data-driven design

57. *Week 13 · code.* Run the lecture's `load_weapons` on this file. Give the exact message it raises. Then explain the last line of the message, which is not a mistake in the row it names.

```
id,name,type,min_dmg,max_dmg,attacks_per_sec,req_str,upgrade
dagger,Dagger,knife,1,4,2.0,,stiletto
stiletto,Stiletto,knife,3,9,2.0,ten,
cleaver,Cleaver,axe,5,11,0,20,
maul,Maul,Mace,12,30,0.7,70,
hatchet,Hatchet,axe,-2,5,1.8,0,cleaver
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
q13.csv: 5 problem(s)
  line 3: req_str: 'ten' is not a valid int
  line 4: attacks_per_sec must be > 0
  line 5: unknown type 'Mace'
  line 6: need 0 <= min_dmg <= max_dmg, got -2..5
  dagger: upgrade 'stiletto' is not a weapon id
```

(The file name at the start is whatever path you passed.)

The dagger's upgrade is spelled correctly. The stiletto row failed to parse (`'ten'`), so `parse_row` returned `None` and the stiletto never entered the table. The reference check then reports a missing target. One mistake produced two messages. A good habit is to fix errors top to bottom and rerun, since later messages can be echoes of earlier ones.

Note what did not cascade. The cleaver row has a bad `attacks_per_sec` but still parsed, so it is in the table and the hatchet's upgrade to it resolves. `'Mace'` fails because the type check is case-sensitive, which is a decision worth writing down.
</details>

58. *Week 13 · compute.* (a) A Dagger row reads `min_dmg 1, max_dmg 4, attacks_per_sec 2.0`. What is its DPS? The designer wants 8 DPS without changing its speed. Give one integer damage range that works. (b) A Pike has `6, 18, 1.0`. Which single cell change makes its DPS 15 while keeping its damage range?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5.0 DPS. Any range with `min + max = 8`, for example 2 to 6. (b) `attacks_per_sec` to 1.25.

(a) `(1 + 4)/2 × 2.0 = 5.0`. For 8 DPS at 2.0 attacks per second, the average hit must be 4, so `min + max = 8`: 2 to 6, 3 to 5 or 1 to 7. The width is a separate design choice (swingier or steadier).

(b) The average hit is 12. `15 / 12 = 1.25`. Both are one-cell data edits. `dps` is never touched.
</details>

59. *Week 13 · compute.* A project's tuning loop has edit 0.5 min, build 5 min, restart 2 min, reach the test 2.5 min and observe 1 min. How many tweaks per hour are possible (a) with numbers in compiled code, (b) with numbers in a data file and a restart, (c) with live reload?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 5.5. (b) 10. (c) 40.

(a) `T = 0.5 + 5 + 2 + 2.5 + 1 = 11` min, `60 / 11 ≈ 5.45`.

(b) No build: `T = 6`, 10 per hour.

(c) No build, restart or reach: `T = 1.5`, 40 per hour, about 7.3 times (a). The largest saving here is not the build. It is the 4.5 minutes of restarting and getting back to the test.
</details>

60. *Week 13 · code.* What does the lecture's `resolve` return for these rows? Then what does it do with `{"a": {"parent": "b", "hp": 1}, "b": {"parent": "c"}, "c": {"parent": "a"}}`?

```python
rows = {
    "skeleton":        {"hp": 30, "armor": 2, "speed": 1.0, "loot": ["bone"]},
    "skeleton_archer": {"parent": "skeleton", "hp": 24, "range": 8},
    "skeleton_mage":   {"parent": "skeleton_archer", "armor": 0, "loot": []},
}
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
skeleton        {'hp': 30, 'armor': 2, 'speed': 1.0, 'loot': ['bone']}
skeleton_archer {'hp': 24, 'armor': 2, 'speed': 1.0, 'loot': ['bone'], 'range': 8}
skeleton_mage   {'hp': 24, 'armor': 0, 'speed': 1.0, 'loot': [], 'range': 8}
```

The second call raises `ValueError: parent cycle: a -> b -> c -> a`.

The mage inherits through two levels: `hp` 24 and `range` 8 from the archer, `speed` 1.0 from the skeleton. Its own `armor: 0` and `loot: []` are present keys, so they override, even though both are "empty". That is the point of using a missing key, not 0, to mean "inherit".
</details>

61. *Week 13 · compute.* The goblin's loot pool in the lecture has gold 60, short_sword 30 and nothing 10. A designer adds gladius 20 and potion 30. (a) What is the short sword's chance per kill now? (b) What is gold's? (c) Why did a change to two other entries alter both answers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 20%. (b) 40%. (c) Weights are shares of a total.

The new total is `60 + 30 + 10 + 20 + 30 = 150`. Short sword `30 / 150 = 20%`, down from 30%. Gold `60 / 150 = 40%`, down from 60%. A weighted table shares one pool, so adding an entry dilutes every other one. A validator warning that prints each entry's percentage after load catches this kind of surprise.
</details>

62. *Week 13 · design.* Choose code, CSV or JSON for each and give the shape that decided it. (a) 300 monster stat blocks with the same 12 columns. (b) Quests, each with a variable number of steps and each step with its own conditions. (c) The formula that turns attack and armor into damage. (d) Level-up XP thresholds for levels 1 to 60.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) CSV. (b) JSON. (c) code. (d) CSV.

(a) A grid of same-shaped rows, edited in a spreadsheet. (b) Boxes inside boxes, lists of steps with nested conditions. (c) A rule, not a number, so it lives in code once and is tested. If some monsters need a different rule, a `rule` column names one of a few tested functions. (d) One row per level with a threshold column, a flat table. A formula in code that generates it is also fine if designers never hand-tune single levels.
</details>

## Week 14: Unit testing gameplay rules

63. *Week 14 · compute.* Using the lecture's `bonus_hundreds` model of Donkey Kong's timer, what timer does each of levels 24, 50 and 76 start with? For each, does the "between 50 and 80" property fail, and does the "never drops" property fail at that level?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 24, 28 and 32. "In range" fails at all three. "Never drops" passes at all three.

| Level | 10 × level + 40 | After `& 0xFF` | Previous level | Never drops? |
|---|---|---|---|---|
| 24 | 280 | 24 | 14 | passes (24 ≥ 14) |
| 50 | 540 | 28 | 18 | passes |
| 76 | 800 | 32 | 22 | passes |

All three are under 81, so the cap does nothing. Each is past a wrap point (22, 48, 73) where the value is climbing again. "Never drops" catches only the wrap levels, 22, 48, 73 and 99. That is why the lecture writes two or three properties per rule.
</details>

64. *Week 14 · compute.* A sampling test swings a 100%-accuracy move `N` times and fails if any swing misses. The buggy rule misses with probability 1/256 per swing. (a) What is the chance the test catches the bug with `N = 500`? (b) What is the smallest `N` that catches it at least 95% of the time? (c) How many calls does the injected-roll test need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 85.9%. (b) 766. (c) 256, and it catches the bug every run.

(a) `1 − (255/256)^500 ≈ 0.859`.

(b) Solve `(255/256)^N ≤ 0.05`: `N ≥ ln 0.05 / ln(255/256) ≈ 765.4`, so 766.

(c) Inject each roll from 0 to 255 once. The test fails at `roll = 255` on every run in under a millisecond. For an ordinary 85% move no sampling size is both reliable and non-flaky, while the injected sweep still needs 256 calls.
</details>

65. *Week 14 · code.* This rule is supposed to let a shield absorb damage first. Write a property test that sweeps `damage` and `shield` from 0 to 50 with `subTest`, run it, and give the number of failing inputs and the smallest one.

```python
def shield_absorb(damage, shield):
    """Shield soaks damage first. Returns (damage_through, shield_left).
    Neither is negative, and damage_through + (shield - shield_left) == damage."""
    if damage > shield:
        return damage - shield, 0
    return 0, shield - damage + 1 if damage == shield else shield - damage
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** 51 failing inputs, the diagonal `damage == shield`. The smallest is `damage=0, shield=0`, which returns `(0, 1)`.

```python
import unittest
from shield import shield_absorb

class ShieldProperties(unittest.TestCase):
    def test_damage_is_conserved_and_nothing_negative(self):
        for damage in range(51):
            for shield in range(51):
                with self.subTest(damage=damage, shield=shield):
                    through, left = shield_absorb(damage, shield)
                    self.assertGreaterEqual(through, 0)
                    self.assertGreaterEqual(left, 0)
                    self.assertEqual(through + (shield - left), damage)
```

When damage exactly equals the shield, the rule leaves 1 shield point that never existed, so `0 + (shield − 1) = damage − 1`. A shield of 0 hit for 0 grows a shield. No example test would pick "equal values" unless you already knew. The sentence "damage is conserved" finds it in 2,601 calls.
</details>

66. *Week 14 · code.* Using the lecture's `fruits_drawn` model of Pac-Man's fruit routine, what does it return for stored levels 0, 3, 6, 7, 254 and 255? Which property catches the bug, and how many inputs fail?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1, 4, 7, 7, 7 and 256. The property `1 <= fruits_drawn(s) <= 7` fails at exactly one input, `s = 255`.

`b = (s + 1) & 0xFF`, capped to 7 from 8 up, then the loop draws, decrements and stops at 0. Stored level 255 wraps `b` to 0, the first decrement turns 0 into 255, and the loop runs 256 times. A sweep over all 256 stored levels costs 256 calls.
</details>

67. *Week 14 · critique.* A teammate's tests for the combat module look like this. Name three problems and fix each.

```python
class CombatTests(unittest.TestCase):
    def test_combat(self):
        rng = random.Random()
        w = load_weapons("weapons.csv")["long_sword"]
        hits = sum(roll_hit(w, rng) for _ in range(100))
        self.assertTrue(hits > 80)
        self.assertTrue(dps(w) == 13.2)
        self.assertTrue(damage_after_armor(20, 5) == 15)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Unseeded sampling makes the test flaky.** `random.Random()` gives a new sequence each run, and 100 swings of a rule meant to hit, say, 85% will fall to 80 or below now and then. Inject the rolls (a scripted generator) and sweep the boundary instead.
- **`assertTrue(a == b)` hides the values.** A failure says `False is not true`. Use `assertEqual(dps(w), 13.2)`, or `assertAlmostEqual` for floats, so the message shows both numbers.
- **One test does three jobs.** When it fails you do not know which rule broke, and the first failure hides the rest. Split it into sentence-named tests: `test_long_sword_dps_is_13_2`, `test_armor_subtracts`, and an injected-roll test for hits.

A fourth problem is fair game. The test reads the live `weapons.csv`, so a legitimate balance change fails a rule test. Test rules with values you construct in the test. Test the data file in separate data tests with design promises, such as "an upgrade always has higher DPS".
</details>

## Weeks 9 to 14: combining patterns

68. *Weeks 9, 10, 11, 12, 13, 14 · design.* Sketch the architecture of a data-driven combat module. Name where each of these lives and why. Weapon and monster numbers, the damage rule, a combatant's stunned or casting state, player and AI actions, the combat log and achievements, and the tests. Then give one number you would measure to decide whether combatants need a component index.

<details>
<summary>Answer and worked solution</summary>

**Answer:** one sound design.

- **Numbers** in CSV (weapons, monsters) and JSON (loot, skills with nested effects), loaded once by a validating loader keyed by id (week 13).
- **The damage rule** as pure functions taking the attacker's and defender's data and an injected `rng` (weeks 13 and 14).
- **Combatant state** as a table-driven state machine per combatant: idle, casting, stunned, dead. Timers are part of the state so replays reproduce them (week 11).
- **Actions** as commands (`Attack(target_id)`, `Cast(skill_id)`, `Guard()`) created by the player's input or the AI and validated at execute time against the state machine. The command list plus the seed is the replay (week 12).
- **Log and achievements** as listeners on `damage_dealt`, `combatant_died` and `skill_cast`, queued so presentation never stalls a combat step (week 10).
- **Tests** at four levels: rule properties, data promises, a regression test per fixed bug, and a replay fingerprint test (week 14).

The number to measure is how many combatants the largest fight has, against how many systems query them each tick. With 10 combatants, polling is a few dozen checks and an index is extra code to keep correct. With thousands of entities and rare status components, the week 9 table says index.
</details>

69. *Weeks 12 and 14 · explain.* Your replay test from the final module fails after a teammate rebalanced the War Hammer's damage in `weapons.csv`. Is the test broken? What should the teammate commit, and what should a reviewer check before accepting it? Why would a rule change to the armor floor sometimes not fail the same replay test?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the test is working. It exists to notice any change in the outcome of a recorded fight.

The teammate should re-record the fingerprint and commit the new expected value in the same change as the data edit, with a message naming the balance change. The reviewer checks three things. The only intended change is the War Hammer row, the other test groups (rules, data promises) still pass unchanged, and the new fingerprint differs in the way the change predicts (for example, the fight ends sooner, or the defender has less HP).

A replay test covers only what the recorded fight exercises. If no hit in that fight lands with `raw − armor <= 0`, a change from `max(1, ...)` to `max(0, ...)` changes nothing in it and the test still passes. That gap is why rule properties sweep the domain and replays guard whole fights. Neither replaces the other.
</details>
