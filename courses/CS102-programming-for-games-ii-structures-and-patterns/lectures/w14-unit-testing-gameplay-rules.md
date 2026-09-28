# CS102 · Week 14 — Unit Testing Gameplay Rules

**Why this matters:** A gameplay rule that is wrong for one input in a hundred will pass every playtest you have time for and then ruin someone's run in week three after launch. Unit tests let the computer try the inputs you would never think to play, in milliseconds, every time you change the code. This week you learn to write them for rules that involve levels, caps and dice.

**You will be able to:**
- Write `unittest` test cases for a pure gameplay function using the arrange-act-assert shape.
- State a property of a rule and check it for every input in a small domain, finding failures no hand-picked example would.
- Test a rule that uses randomness by injecting the random source, and compute how many random samples a statistical test would need to catch the same bug.
- Design a test suite for a data-driven combat module: rules, data rows and a replay regression test.

**Before class:** Python documentation, `unittest` (sections "Basic example", "Organizing test code" and "Distinguishing test iterations using subtests"). Nystrom, *Game Programming Patterns* (2014), "Command" (reread the part on undo and replay; you will test a replay). Skim the Hypothesis documentation's front page (hypothesis.readthedocs.io) to see what a property-based testing library looks like.

**Prerequisites from earlier courses:** Boundary tests with `assert` and the Pokémon 1/256 miss, [CS101 week 4, functions and decomposition](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md). Debugging habits, [CS101 week 12](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md), and seeded randomness, [CS101 week 13](../../CS101-programming-for-games-i/lectures/w13-randomness-spawning-and-procedural-variety.md). From this course, the state machine ([week 11](w11-state-and-state-machines.md)), Command pattern replay ([week 12](w12-command-pattern-input-replay-undo.md)) and the validated data loader ([week 13](w13-data-driven-design-stats-in-json-and-csv.md)). Sample size and confidence, [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md).

**Interactive:** [Property sweep](../examples/w14-property-sweep.html). Keep it open during section 2.

---

## 1. From `assert` to a test suite

In CS101 week 4 you wrote boundary checks as bare `assert` lines at the bottom of a file. That habit is right, and it stops scaling at about ten checks. The first failing `assert` stops the script, so you never learn whether the other nine passed. Nothing records which checks exist. And nobody runs a file of asserts unless they remember to.

A **unit test** is a small, automatic check of one piece of code (a *unit*, usually one function or one class) in isolation from the rest of the game. A **test suite** is the collection of all of them, run together by a **test runner** that reports every pass and failure. Python ships one in the standard library, `unittest`.

```python
# rules.py
def damage_after_armor(raw, armor):
    """Subtractive armor with a floor of 1 (GD203 week 2)."""
    return max(1, raw - armor)
```

```python
# test_rules.py
import unittest
from rules import damage_after_armor

class DamageAfterArmorTests(unittest.TestCase):
    def test_armor_subtracts(self):
        raw, armor = 20, 5                         # arrange
        result = damage_after_armor(raw, armor)    # act
        self.assertEqual(result, 15)               # assert

    def test_floor_is_one_when_armor_exceeds_damage(self):
        self.assertEqual(damage_after_armor(5, 20), 1)

    def test_floor_is_one_at_exact_equality(self):
        self.assertEqual(damage_after_armor(5, 5), 1)
```

Run it from the folder that holds both files:

```
python -m unittest -v
```

The runner finds every file named `test*.py`, every class that inherits from `unittest.TestCase`, and every method whose name starts with `test`. It runs each one separately, so one failure does not hide the others, and prints a line per test plus a summary.

Three words to learn.

- **Arrange, act, assert.** Every test sets up its inputs, calls the code once, and checks the result. When a test does more than that, split it.
- **Assertion methods.** `assertEqual(a, b)`, `assertTrue(x)`, `assertGreaterEqual(a, b)`, `assertRaises(Error)` and friends. Prefer the specific ones. When `assertEqual(result, 15)` fails, the message says `14 != 15`. When `assertTrue(result == 15)` fails, it says `False is not true`, which tells you nothing.
- **Test names are sentences.** `test_floor_is_one_at_exact_equality` tells the next programmer what the rule is supposed to be. Six months from now, the test name is the spec.

### What makes gameplay code testable

A rule is easy to test when it is a **pure function**: its output depends only on its arguments, and it changes nothing outside itself. `damage_after_armor` is pure. A method that reads the global clock, rolls `random.random()` internally, looks up the player through a singleton and plays a sound is not. To test it you would have to control the clock, the random generator, the singleton and the audio system.

So the design rule for testable gameplay code is to pass things in. Pass time in as `dt` (CS101 week 9). Pass the random source in as an argument (section 3). Pass the weapon's data in, looked up from the table by id (week 13). Keep drawing and sound outside the rule, triggered by events the rule returns (the Observer pattern, week 10). Every one of these choices is also good architecture for other reasons. Testability is the cheapest way to find out whether you made them.

## 2. Worked example: Donkey Kong's level 22

### The hook

Donkey Kong (Nintendo, arcade, 1981) has a famous **kill screen**. On the first stage of level 22, the bonus timer starts so low that Mario dies after a few seconds, before he can climb past the second girder. For decades no player could go further, and the game became a record-chasing sport built around reaching this wall.

Here is the surprising part. The programmers *did* write a cap on the timer, and they also capped the level counter at 99 so that the level display could never overflow. Don Hodges' disassembly of the ROM shows both. They thought about big numbers. They still shipped a bug at level 22, because the cap was in the wrong place.

### The model

Hodges walks through the routine that sets the timer at the start of a level. Rewritten in Python it is four lines. The timer is stored in hundreds of points, so 80 means a bonus of 8,000.

```python
def bonus_hundreds(level):
    """Donkey Kong's starting bonus timer, in hundreds, as the arcade ROM computes it."""
    a = (level * 10 + 40) & 0xFF      # 8-bit register: keeps only the low 8 bits
    if a >= 81:
        a = 80
    return a
```

- `level` is the level number, 1 to 99.
- `level * 10 + 40` is the intended formula: 5,000 points at level 1, then 1,000 more per level.
- `& 0xFF` keeps the lowest 8 bits, which is what the Z80 processor's 8-bit register does when a result exceeds 255. It is the same as `% 256` for non-negative numbers. This is the step the original programmers did not guard.
- `if a >= 81: a = 80` is the cap. It is correct as far as it goes, but it runs *after* the overflow has already happened.

What the designers meant is `min(80, level * 10 + 40)`. At level 22 the intended value is `260`, capped to `80`. The ROM computes `260 & 0xFF = 4`, which is under 81, so the cap does nothing. The timer starts at 400 points.

### Example tests: they all pass

Suppose you had written tests for this function the usual way, by picking levels you thought were interesting.

```python
import unittest
from timer import bonus_hundreds

class ExampleTests(unittest.TestCase):
    def test_first_levels_ramp_up(self):
        self.assertEqual(bonus_hundreds(1), 50)
        self.assertEqual(bonus_hundreds(2), 60)
        self.assertEqual(bonus_hundreds(3), 70)

    def test_cap_at_8000(self):
        self.assertEqual(bonus_hundreds(4), 80)
        self.assertEqual(bonus_hundreds(10), 80)
        self.assertEqual(bonus_hundreds(20), 80)
```

Both tests pass. They check the start, the moment the cap kicks in, and two comfortable levels past it. A careful student would write exactly these. They are also blind to the bug, because nobody picks 22 as an interesting number unless they already know about it.

### Property tests: say what must always be true

An **example test** checks one input against one expected output. A **property test** states something that must hold for *every* input, then checks it across the whole domain (or a large sample of it). For this function, two properties come straight from the design intent:

1. The timer is always between 50 and 80 hundreds.
2. The timer never goes down as the level goes up.

Neither mentions level 22. Both are things a designer would say out loud in a meeting.

```python
class PropertyTests(unittest.TestCase):
    LEVELS = range(1, 100)        # the game caps the level at 99

    def test_timer_in_range(self):
        for level in self.LEVELS:
            with self.subTest(level=level):
                t = bonus_hundreds(level)
                self.assertGreaterEqual(t, 50)
                self.assertLessEqual(t, 80)

    def test_timer_never_drops(self):
        for level in self.LEVELS[1:]:
            with self.subTest(level=level):
                self.assertGreaterEqual(bonus_hundreds(level), bonus_hundreds(level - 1))
```

`self.subTest(level=level)` makes each level its own reported case, so one failure does not stop the loop and the report names the level. The domain is 99 values; the whole sweep runs in about a millisecond.

### Numbers you can check

Here is the function at the levels that matter. Compute any row by hand: multiply by 10, add 40, subtract 256 if the result is 256 or more, then cap at 80 if it is 81 or more.

| Level | 10 × level + 40 | After `& 0xFF` | After cap (shipped) | Intended |
|---|---|---|---|---|
| 1 | 50 | 50 | 50 | 50 |
| 4 | 80 | 80 | 80 | 80 |
| 21 | 250 | 250 | 80 | 80 |
| **22** | 260 | **4** | **4** | 80 |
| 23 | 270 | 14 | 14 | 80 |
| 29 | 330 | 74 | 74 | 80 |
| 30 | 340 | 84 | 80 | 80 |
| 47 | 510 | 254 | 80 | 80 |
| **48** | 520 | **8** | **8** | 80 |
| **73** | 770 | **2** | **2** | 80 |
| **99** | 1,030 | **6** | **6** | 80 |

And here is what each kind of test reports when you run the suite:

| Test | Levels checked | Failures | Failing levels |
|---|---|---|---|
| Example tests (6 hand-picked levels) | 1, 2, 3, 4, 10, 20 | 0 | none |
| Property: timer between 50 and 80 | 1 to 99 | 16 | 22-26, 48-52, 73-77, 99 |
| Property: timer never drops | 2 to 99 | 4 | 22, 48, 73, 99 |
| Oracle: equals `min(80, 10 × level + 40)` | 1 to 99 | 25 | 22-29, 48-55, 73-80, 99 |

Read the table slowly, because it holds the week's lesson. The example tests are six for six and wrong. Both properties catch the bug, and the "never drops" property points at exactly the four places where the timer wraps around. The **oracle** test, which compares against a simple reference implementation, catches the most, including levels like 29 where the timer is 74 instead of 80, a bug that is inside the "between 50 and 80" range and so invisible to property 1.

### Move it

Open the interactive. The left view plots the timer for levels 1 to 99: a flat line at 80 for the intended value, and bars for what the ROM computes. Below the chart, six chips mark the example-test levels; all six are green. The bars at 22, 48, 73 and 99 dive to almost nothing, and no chip sits on them.

Press **Run property sweep**. Every level is checked against the selected property and the failing bars turn red, with a count. Switch the property between "in range," "never drops" and "equals intended" and watch the failing set change: 16, then 4, then 25.

Now switch the implementation to **Hodges' fix** (clamp the level to 4 before the arithmetic, so it can never overflow) and run the sweep again: zero failures under all three properties. Or switch to a **16-bit register** and see that a wider number type also removes every failure for levels up to 99. Both fixes work. The sweep is how you would know.

### The same idea in other games

The Donkey Kong bug has a shape: a small integer, a domain the designers did not fully walk, and a failure at one edge. You have seen it before.

**Pac-Man (Namco, arcade, 1980), level 256.** Pac-Man stores the level in one byte, counting from 0, so level 256 is stored as 255. Hodges' disassembly shows the routine that draws the fruit icons at the bottom of the screen. It adds 1 to the level byte, and for levels under 8 it uses that number as a loop counter to draw one to seven fruit. At level 256 the byte wraps from 255 to 0. The loop decrements the counter *before* testing it, so a counter of 0 wraps to 255 and the loop runs 256 times, drawing whatever memory lies past the fruit table across the right half of the maze. The level cannot be finished.

```python
def fruits_drawn(stored_level):
    """Number of fruit icons Pac-Man's routine draws. stored_level is 0 for level 1."""
    b = (stored_level + 1) & 0xFF
    if b >= 8:
        b = 7                       # from level 8 on, always the last 7 fruit
    count = 0
    while True:                     # Z80 DJNZ: draw, decrement, loop if not zero
        count += 1
        b = (b - 1) & 0xFF
        if b == 0:
            return count
```

Property: `1 <= fruits_drawn(s) <= 7` for every `s` in `range(256)`. The sweep takes 256 calls and fails at exactly one input, `s = 255`, returning 256.

**Pokémon Red and Blue (1996 to 1998), the 1/256 miss.** In CS101 week 4 you met the accuracy check `roll < accuracy_byte` with a roll from 0 to 255, and saw that a 100% move stores 255 and misses on roll 255. As a property: "a move listed at 100% hits for every possible roll." The domain is 256 rolls. The sweep fails at exactly one, `roll = 255`.

Three games, three bugs at the edge of a byte, one test shape: **state the property, then walk the whole domain.** When the domain has 99 or 256 values, walking all of it is cheaper than thinking about which values to pick. You don't have to guess 22, 255 or roll 255. The sweep finds them for you.

### Design judgment

Property tests are not a replacement for example tests. Each kind catches things the other misses, and each has costs you should weigh.

- **Exhaustive when you can, sampled when you must.** Levels 1 to 99, 256 rolls and 20 faces of a d20 are small enough to walk completely. A damage function of attack (1 to 9,999), armor (0 to 9,999) and level (1 to 60) has about six billion inputs. There, you check a few thousand random inputs plus the edges, which is what a library like Hypothesis automates: you describe the input ranges and it picks inputs, including edge cases it knows are often buggy, and shrinks any failure to a small example.
- **A property is only as good as the sentence behind it.** "Between 50 and 80" missed level 29. "Never drops" missed levels 23 to 29. Each property encodes one piece of intent. Write two or three per rule, from different angles, and add an oracle when a simpler (slower, more obvious) reference implementation exists.
- **The test is the spec, so decide the spec.** A property test forces a design decision that nobody wrote down. Should Pac-Man have a final level? Should the timer be capped at 8,000 or keep growing? Donkey Kong's programmers answered "capped" for the level counter and forgot to answer it for the timer. Write the intent as a test and the forgotten case shows up.
- **Keep the examples too.** Example tests are the best documentation of what the rule is *for*: `bonus_hundreds(1) == 50` tells a reader more than any property. Use examples to explain, properties to explore.

## 3. Testing rules that roll dice

Most gameplay rules involve randomness, and randomness is the first thing that makes students give up on testing. There are three ways to test a random rule. Only one is reliable.

### Option 1: sample and check the rate

Run the rule many times with the real random generator and check that the observed rate is close to the intended one. It feels natural, and it is the weakest option. Take the Pokémon accuracy check. Suppose you test a 100% move by swinging it `N` times.

If your test says "hit rate must be at least 99%," it can never fail on the 1/256 bug: the real rate is 99.61%. If your test says "zero misses allowed," the chance it catches the bug in one run is `1 − (255/256)^N`:

| Swings `N` | Chance one test run catches the bug |
|---|---|
| 10 | 3.8% |
| 100 | 32.4% |
| 256 | 63.3% |
| 1,000 | 98.0% |
| 2,000 | 99.96% |

That looks survivable for a 100% move, where any miss at all is a failure. It collapses for the ordinary case. For an 85% move the ROM gives 84.38%, a shortfall of 0.62 points. No tolerance is loose enough to pass the correct rule and tight enough to fail the buggy one until `N` is in the tens of thousands (MA102 week 13 shows how to size it), and even then a correct rule fails occasionally by bad luck. A test that sometimes fails on correct code is called **flaky**, and teams learn to ignore flaky tests, which is worse than not having them.

### Option 2: fix the seed

Create the random generator with a fixed seed, `random.Random(42)`, so the "random" sequence is the same every run, and compare against output you recorded once. This makes tests repeatable, and it is the right tool for whole-fight simulations and replays (section 4). It is brittle for rules. Add one extra random call anywhere earlier in the fight, and every later roll shifts, and every recorded result changes, though nothing is wrong.

### Option 3: inject the roll

Make the random source an argument, and in tests pass a fake one that returns the rolls you choose.

```python
def attack_hits(accuracy_byte, rng):
    return rng.randrange(256) < accuracy_byte

class ScriptedRng:
    """A stand-in for random.Random that returns pre-chosen values."""
    def __init__(self, values):
        self.values = iter(values)
    def randrange(self, n):
        return next(self.values)

class AccuracyTests(unittest.TestCase):
    def test_perfect_move_hits_every_roll(self):
        for roll in range(256):
            with self.subTest(roll=roll):
                self.assertTrue(attack_hits(255, ScriptedRng([roll])))
```

In the game you call `attack_hits(255, random.Random())`, or pass the fight's shared generator. In the test you walk all 256 rolls. The test fails at exactly `roll=255`, every run, in under a millisecond. No statistics, no flakiness. Compare 256 deterministic calls with 1,000 random swings that still miss the bug 2% of the time.

The fake object works because Python checks only that `rng` has a `randrange` method, not what class it is. This is the interface idea from week 3: the rule depends on "something that can give me a number below n," and both the real generator and the script satisfy it.

## 4. Testing a data-driven module

Your final project for this course is a data-driven combat module. Its tests fall into four groups, and each catches a different kind of bug.

**Rule tests.** Example and property tests for each pure function: damage, armor, hit chance, crit, time-to-kill. These are sections 1 to 3.

**Data tests.** Week 13's validator checks that the file is well formed. Tests check that the *content* keeps promises the design depends on. `subTest` makes each row its own case.

```python
from weapons_loader import load_weapons, dps

class WeaponDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weapons = load_weapons("weapons.csv")

    def test_every_upgrade_has_higher_dps(self):
        for w in self.weapons.values():
            if w.upgrade:
                with self.subTest(weapon=w.id):
                    self.assertGreater(dps(self.weapons[w.upgrade]), dps(w))

    def test_no_id_was_removed(self):
        with open("known_ids.txt") as f:
            known = {line.strip() for line in f if line.strip()}
        self.assertLessEqual(known, set(self.weapons))
```

The first test encodes a design promise: an upgrade is never a downgrade. The second protects save files. `known_ids.txt` lists every id that has ever shipped, and `assertLessEqual` on two sets checks that every known id still exists. Renaming `long_sword` fails the build instead of breaking saves.

**Regression tests.** A **regression** is a bug that was fixed and came back. The discipline is simple. When you find a bug, first write a test that fails because of it, then fix the code, then watch the test pass. The test stays in the suite forever. The Donkey Kong property test is exactly the regression test Hodges' patch would ship with.

**Replay tests.** Week 12's Command pattern records every input as a command. Record a 30-second fight once, save the command list and a fingerprint of the final state (every unit's HP, position and status, turned into one string). The test replays the commands with the same seed and asserts that the fingerprint matches. This is the one place a fixed seed belongs, because the whole point is to notice *any* change. When the fingerprint changes on purpose (you rebalanced a weapon), re-record it and commit the new file along with the change, so a reviewer sees both.

### How many tests, and which first

You will not test everything, so test in order of blast radius. The shared rules that every attack calls come first: damage, hit chance, the timer. Then the data promises that protect players' saved progress. Then the replay, which catches the unexpected. Cosmetic code (menu layout, particle counts) rarely earns a unit test at all.

A good sign that you have enough is that you change a rule with confidence. If you are afraid to touch `damage_after_armor` because you don't know what depends on it, the tests are missing.

## In-class activity (25 minutes)

Pairs, one laptop. Materials: `rules.py` from the lab 14 starter, which contains six small gameplay rules, each with one planted bug, and only two example tests. Work on the first three (`damage_after_armor`, `is_crit`, `rage_bonus`) and leave the other three for the lab.

1. (5 min) For each of the three rules, write one sentence of intent: what must always be true. Do not read the code closely yet.
2. (15 min) Turn each sentence into a property test that sweeps a small domain (levels 1 to 60, rolls 0 to 99, stacks 0 to 20, and so on) with `subTest`. Run the suite. For each failure, record the smallest failing input.
3. (5 min) Compare with the pair next to you. Did you both find all three bugs? For any bug one pair missed, what was different about the property?

Expected output: three properties as test methods, the smallest failing input for each rule, and one sentence on the property that worked best.

## Common misconceptions

- **"All my tests pass, so the rule is correct."** Six Donkey Kong example tests pass on a function that kills every player at level 22. Passing tests prove the rule is right *for the inputs you tested*.
- **"You can't unit-test random code."** You can't usefully test it by sampling. You can test it exactly by injecting the random source and choosing the rolls.
- **"A fixed seed makes random tests correct."** It makes them repeatable. A seeded test that recorded a wrong answer will keep passing on the wrong answer. Seeds belong in replay tests, where any change is the signal.
- **"Property tests replace example tests."** Properties explore; examples explain. A suite with only properties tells a reader what can never happen but not what the rule is for.

## Check yourself

1. Using the `bonus_hundreds` model, what timer does level 25 start with? Which of the two properties in section 2 fails at level 25?
2. A designer proposes fixing Donkey Kong by changing the cap check to `if a >= 81 or a < 50: a = 80`. Run the three properties in your head (or in Python) over levels 1 to 99. Does it pass all of them? Is it a good fix?
3. A test swings a 100% move 500 times and fails if there is any miss. What is the chance it catches the 1/256 bug in one run? How many swings are needed for a 99% chance?
4. Rewrite `crit(rng, chance)`, which returns `rng.random() < chance`, and a `ScriptedRng` with a `random()` method, so that you can test the exact boundary for `chance = 0.25`. Which two scripted values would you use?
5. Your weapon table gains a `tier` column. Write, in one sentence each, two data-test properties about tiers that protect the design.

<details>
<summary>Answers</summary>

1. `25 × 10 + 40 = 290`, and `290 − 256 = 34`, under 81, so the timer starts at 34 hundreds (3,400 points). "Between 50 and 80" fails (34 < 50). "Never drops" does not fail at 25, because level 24 is 24 and 34 is higher. It fails only at 22, where the timer falls from 80 to 4.
2. It passes "between 50 and 80," because every wrapped value below 50 becomes 80. It fails "never drops" at levels 27, 53 and 78, where the timer falls from 80 to 54, 58 and 52. It fails the oracle at nine levels (27-29, 53-55, 78-80): those timers are legal but lower than intended. The patch hides some of the overflow instead of preventing it. Hodges' fix (clamp the level first) or a wider integer removes the cause.
3. `1 − (255/256)^500 ≈ 85.9%`. For 99%, solve `(255/256)^N ≤ 0.01`: `N ≥ ln(0.01) / ln(255/256) ≈ 1,177` swings.
4. `def crit(rng, chance): return rng.random() < chance`, with `ScriptedRng.random` returning the next scripted value. Test `0.2499999` (must crit) and `0.25` (must not crit, since the rule uses `<`). Those two values sit on either side of the boundary.
5. For example, "within a weapon type, a higher tier never has lower DPS," and "every weapon's upgrade is exactly one tier higher." Each is a `subTest` loop over the rows.

</details>

## Lab / assignment hook

[Lab 14, a test suite for the combat module](../labs/lab14.md). You get `rules.py` with six gameplay rules and planted bugs, and the week 13 loader. Write example, property, injected-roll and data tests that find every bug, fix them one regression test at a time, and add a replay test for a recorded fight. Your suite runs as part of the final module's grading.

## Sources

- Hodges, D. "How High Can You Get? The Fix for Donkey Kong's Kill Screen" (posted 2007, updated 2017). Disassembly of the Donkey Kong arcade timer routine: level × 10 + 40 computed in an 8-bit register with no overflow check, the cap to 80 hundreds, 400 points at level 22, the level cap at 99, and a patch that clamps the level to 4 first. http://donhodges.com/how_high_can_you_get.htm
- Hodges, D. "Splitting Apart the Split Screen" (posted 2007, updated 2017). Pac-Man's fruit-drawing routine: level stored from 0, incremented to 0 at level 256, the loop running 256 times. http://donhodges.com/how_high_can_you_get2.htm
- Wikipedia, "Donkey Kong (1981 video game)", section "Bugs and exploits" (accessed September 2026). Level 22 kill screen kills Mario after a few seconds. And "Glossary of video game terms", "Kill screen": Pac-Man level 256 unbeatable due to an integer overflow.
- pret, `pokered` disassembly, and Bulbapedia, "Accuracy" (Generation I). The 0 to 255 roll and the strict less-than check; see CS101 week 4 for the full treatment.
- Python Software Foundation, `unittest` documentation (Python 3.13): test discovery, `TestCase`, assertion methods, `subTest`, `setUpClass`. Detection percentages computed with Python 3.13.5.
- Hypothesis documentation (latest, accessed September 2026), front page: a property-based testing library for Python that chooses inputs in a described range, including edge cases. https://hypothesis.readthedocs.io
- Nystrom, R. (2014). *Game Programming Patterns*, "Command". gameprogrammingpatterns.com.

## Interactive spec: examples/w14-property-sweep.html

**Purpose.** Make visible that hand-picked example tests all pass on Donkey Kong's timer while a property sweep over every level finds the bug, and that the choice of property decides which failures you see.

**Layout.** Chart on top (full width), test panel below it on mobile, to its right at widths ≥ 1000px.

- **Chart.** X-axis levels 1 to 99; y-axis bonus in hundreds, 0 to 90, gridlines at 50 and 80. One bar per level showing the selected implementation's value. A dashed line shows the intended value `min(80, 10 × level + 40)`. Hover/focus on a bar shows `Level 22: 10 × 22 + 40 = 260 → & 0xFF = 4 → cap: 4 (intended 80)`. Six small chips under the x-axis mark the example-test levels (default 1, 2, 3, 4, 10, 20), green if the example matches, red if not. Clicking a bar toggles it as an example level (keyboard: arrow keys move focus between bars, Enter toggles).
- **Test panel.**
  - Implementation radio group: "Shipped ROM (8-bit, cap after)" (default), "Hodges' fix (clamp level to 4 first)", "16-bit register".
  - Property radio group: "Timer between 50 and 80", "Timer never drops", "Equals intended (oracle)".
  - Button "Run property sweep". On press, bars that fail the selected property turn to the error token colour (with a hatched pattern for colour-blind users), and a summary reads `Property: never drops · 98 levels checked · 4 failures: 22, 48, 73, 99`. The sweep result updates live if the property or implementation changes after it has been run.
  - Example summary line, always visible: `Example tests: 6 of 6 pass`.

**Formulas.**
- Shipped: `a = (10L + 40) mod 256; if a ≥ 81 then a = 80`.
- Hodges' fix: `L' = min(L, 4); a = 10L' + 40`.
- 16-bit: `a = (10L + 40) mod 65536; if a ≥ 81 then a = 80`.
- In range: fail if `a < 50 or a > 80`. Never drops: for L ≥ 2 fail if `a(L) < a(L − 1)` (checked levels 2 to 99, report 98 checked). Oracle: fail if `a ≠ min(80, 10L + 40)`.

**Test values (shipped).** Level 22 → 4, 23 → 14, 29 → 74, 30 → 80, 48 → 8, 55 → 78, 73 → 2, 99 → 6. In range: 16 failures (22-26, 48-52, 73-77, 99). Never drops: 4 failures (22, 48, 73, 99). Oracle: 25 failures (22-29, 48-55, 73-80, 99). Hodges' fix and 16-bit: 0 failures under all three. Default example levels: 6 of 6 pass; adding level 22 as an example makes it 6 of 7.

**The one insight.** Six green example chips sit on a chart whose bars collapse at 22, 48, 73 and 99; one button press on a plain-English property turns exactly those bars red.

**Accessibility.** Radio groups and button keyboard operable; failing bars distinguished by pattern and by the text summary, not colour alone; summary in an `aria-live="polite"` region; no transitions under `prefers-reduced-motion`.
