# CS101 · Week 13 — Randomness: Spawning and Procedural Variety

**Why this matters:** Your arcade game needs enemies that arrive somewhere new each run, and you need to be able to replay the exact run that crashed. Both come from the same few lines of code. How you write them decides whether players call your game fair, whether a bug can be reproduced, and whether a pretty particle effect quietly changes where the boss spawns.

**You will be able to:**
- Create a seeded random generator in Python and Godot, and explain why the same seed gives the same sequence.
- Implement three piece randomizers (independent rolls, a no-repeat reroll and a shuffled bag) and compute each one's repeat rate and worst drought.
- Write a spawner that uses rejection sampling with a safe radius and an attempt cap, and compute its expected number of tries.
- Decide which game systems get their own generator, and justify the choice in terms of replays and debugging.

**Before class:** Python documentation, `random` module, the introduction and the section "Notes on Reproducibility" (about 10 minutes). Godot documentation (Godot 4), "Random number generation" tutorial page, all of it (about 15 minutes). Skim the Tetris Wiki page "Random Generator".

**Prerequisites from earlier courses:** [CS101 week 4, functions and decomposition](w04-functions-and-decomposition.md) (pure functions and passing values in, which is how we pass a generator in). CS101 [week 5](w05-arrays-and-lists-inventories.md) and [week 6](w06-dictionaries-item-databases.md) on lists and dictionaries, and [week 9](w09-delta-time-and-frame-rate-independence.md) on delta time and the accumulator. [MA102 week 2, independent events and the gambler's fallacy](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) has the probability behind bags; you do not need it yet, and this lecture computes what it needs. The spawner in section 3 uses the squared-distance test from [CS101 week 10](w10-collision-basics-aabb-and-circles.md); [MA101 week 14](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) covers it in depth the following week.

**Interactive:** [examples/w13-randomizer-droughts.html](../examples/w13-randomizer-droughts.html). Keep it open during section 2.

---

## 1. Where "random" comes from in a program

A computer follows instructions exactly. It has no coin to flip. What your code calls "random" is a **pseudo-random number generator** (PRNG). A PRNG is a small function with hidden state. Each call scrambles the state with fixed arithmetic and hands you a number derived from it. The numbers pass statistical tests for randomness, but the whole sequence is decided the moment you choose the starting state.

That starting state is set from a **seed**, a number you pick (or the system picks for you). Same seed, same sequence. Every time.

```python
import random

a = random.Random(2026)
b = random.Random(2026)
print([a.randint(1, 6) for _ in range(5)])
print([b.randint(1, 6) for _ in range(5)])   # identical to the line above
```

Run it and both lines print the same five dice. Change one seed to 2027 and the lines differ.

Python's generator is the Mersenne Twister, which the documentation says repeats only after 2^19937 − 1 numbers. You will never see it loop. The docs also warn that it is not safe for security, so never use it for passwords or tokens; that is what the `secrets` module is for. One more detail from the docs is worth knowing now. Python only guarantees that `random()` itself gives the same sequence for the same seed across Python versions. Helpers like `choice` and `shuffle` may change. If you ever store seeds for a shipped game, pin your Python version or use only `random()`.

Godot 4 gives you the same two tools. The engine has a **global generator** behind functions like `randi()`, `randf()` and `Array.shuffle()`, and the docs state that Godot seeds it randomly by default. It also has a class, `RandomNumberGenerator`, that you create yourself. Its docs say it currently uses the PCG32 algorithm and add a warning that the algorithm is an implementation detail you should not depend on.

```gdscript
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.seed = 2026
    print(rng.randi_range(1, 6), rng.randf_range(0.0, 1.0))
```

### One generator per job

Here is the rule that saves you hours of debugging. **Give each system that must be reproducible its own generator, and never share it with systems that don't need to be.**

Imagine your game uses one global generator for everything. An enemy dies and you spawn a random number of spark particles, say 8 to 12. Each particle calls `randf()` twice for its direction. Then the spawner calls `randf()` to place the next enemy. Now the next enemy's position depends on how many sparks the last explosion made. Turn particles off in the settings menu and every later spawn moves. A player's bug report with a seed can no longer be reproduced on your machine, because your machine has particles on.

The fix costs three lines:

```python
spawn_rng = random.Random(run_seed)       # enemies, pickups, pieces
fx_rng = random.Random()                  # sparks, pitch wobble; seed does not matter
```

Gameplay draws only from `spawn_rng`. Cosmetic effects draw only from `fx_rng`. The gameplay sequence now depends only on the seed and the player's actions. This is also why the functions in this lecture take the generator as a parameter (`rng`) instead of calling the global one. You met this idea in week 4 as "pass values in, don't reach out for them."

One trap in Godot. The docs for `Array.shuffle()` and `Array.pick_random()` note that they use the global seed, not any `RandomNumberGenerator` you made. If your bag must be seeded, write the shuffle yourself (section 2 shows how).

## 2. Worked example: three ways to deal a Tetris piece

### The hook

In the 1989 NES Tetris, you can wait a very long time for the long straight piece. In modern Tetris games that follow the official Tetris Guideline, you can never wait more than 12 pieces. Both games deal each of the seven pieces equally often over a long game. So what did the modern games change?

They changed the code that picks the next piece, the **randomizer**. The long-run rate is the same. The streaks are not. This worked example builds three randomizers, each about ten lines, and measures what players feel.

### The model: a randomizer is a generator plus memory

Every randomizer in this lecture has the same shape:

```
next piece = rule(rng, memory)
memory     = update(memory, next piece)
```

- `rng` is a seeded generator, as in section 1.
- `memory` is whatever the rule remembers between calls. It can be nothing.
- `rule` decides how the random numbers become a piece.

The three rules differ only in their memory.

**Pure random (no memory).** Roll 1 in 7. Every piece is independent of the past.

**NES style (remembers one piece).** The Tetris Wiki documents the NES rule as two rolls. First roll a number from 0 to 7. Eight values for seven pieces: the extra value, 7, is a dummy. If the first roll names a real piece and it is not the piece you just dealt, deal it. Otherwise roll again from 0 to 6 and deal whatever comes up, even a repeat.

**7-bag (remembers the rest of the bag).** The Tetris Wiki describes the Guideline "Random Generator" as putting all seven pieces in a bag, shuffling, dealing them in that order, and refilling when empty. The wiki credits its origin to *The New Tetris*.

In Python, each rule is a generator function, a function that uses `yield` to hand out one value per `next()` call and keeps its local variables alive in between. That is exactly the "memory" in the model:

```python
PIECES = "IJLOSTZ"

def pure_random(rng):
    while True:
        yield rng.choice(PIECES)

def nes_style(rng):
    prev = None                          # memory: the last piece
    while True:
        roll = rng.randrange(8)          # 0-7, where 7 is the dummy
        if roll == 7 or PIECES[roll] == prev:
            roll = rng.randrange(7)      # second roll, always dealt
        prev = PIECES[roll]
        yield prev

def seven_bag(rng):
    while True:
        bag = list(PIECES)               # memory: what is left in the bag
        rng.shuffle(bag)
        yield from bag
```

Our `nes_style` copies the documented rule, not the cartridge. The real game draws its numbers from its own small generator, and we replace that with Python's. So we learn what the rule does, not every quirk of the 1989 hardware.

### Numbers you can check by hand

Start with the chance that the next piece repeats the current one.

- **Pure random.** One in seven: `1/7 = 14.3%`.
- **NES style.** A repeat needs two things. The first roll must be rejected, which happens on the dummy or on the same piece, `2/8`. Then the second roll must land on the same piece, `1/7`. So `2/8 × 1/7 = 1/28 = 3.6%`. The rule cuts repeats to a quarter but does not remove them.
- **7-bag.** Inside a bag no piece repeats. A repeat can only happen across the boundary between two bags, when the last piece of one bag equals the first piece of the next. One position in seven is a boundary, and there the chance is `1/7`. So `1/7 × 1/7 = 1/49 = 2.0%`.

Now the droughts. Call a **drought** the number of other pieces between two I pieces.

- **Pure random.** The chance of 20 or more non-I pieces in a row is `(6/7)^20 = 4.6%`. There is no maximum. Any length has some chance.
- **7-bag.** The worst case puts an I first in one bag and last in the next. That leaves the other 6 pieces of the first bag plus the first 6 of the second between them. `6 + 6 = 12`, the figure the Tetris Wiki gives.

The average drought is 6 for all three. Each deals I one time in seven, so on average six other pieces sit between two I pieces. The average hides everything players complain about.

Now run the code. The lab 13 starter prints this table. Every randomizer gets its own `random.Random(13)` and deals 100,000 pieces (Python 3.13):

| Randomizer | Share of I | Mean drought | Longest drought | Droughts of 20+ | Repeat rate |
|---|---|---|---|---|---|
| Pure random | 0.1425 | 6.02 | 70 | 4.47% | 14.4% |
| NES style | 0.1428 | 6.00 | 55 | 3.56% | 3.6% |
| 7-bag | 0.1429 | 6.00 | 12 | 0% | 2.0% |

Check the simulation against the hand numbers. Repeat rates of 14.4%, 3.6% and 2.0% match `1/7`, `1/28` and `1/49`. The pure random drought share of 4.47% matches `(6/7)^20 = 4.58%` within noise. The bag never passes 12. When a simulation agrees with the math on the numbers you can check, you can trust it on the ones you cannot, like the NES rule's 3.56% share of long droughts. That rule was built to stop repeats, and it barely touches droughts.

Why 55 and 70 and not some other number? The longest drought in a run depends on the seed. Change 13 to 14 and you get different maxima. That is the point. Only the bag has a maximum written into its code.

### See it move

Open the interactive. The top view deals three lanes of pieces, one per randomizer, from the same seed, with I pieces highlighted. The bottom view is a histogram of drought lengths for each lane, with a marker at the longest one. Deal 1,000 pieces and look at the lanes. All three look equally "random" to the eye. Then look at the histogram. The bag's bars stop dead at 12. The other two trail off to the right with a long thin tail. Change the seed and watch the tails move while the bag's wall stays put. (The page runs its own JavaScript generator, not Python's, so its longest droughts for seed 13 differ from the table above. The shares, the repeat rates and the bag's wall of 12 match.) The lanes show you what the player sees in a moment. The histogram shows what the player remembers after a hundred games.

### Cross-game recognition

Once you see "generator plus memory," you find it in many places.

**Tetris: The Grand Master (arcade).** The Tetris Wiki documents the TGM randomizer as keeping a history of the last 4 pieces. It rolls a piece, and if that piece is in the history it rolls again, up to 4 tries in the first game and 6 in TGM2. It also never deals S, Z or O as the very first piece. In our model it is the NES rule with a bigger memory (4 pieces instead of 1) and more rerolls (4 or 6 instead of 1). The memory is still a short list and the rule is still "reroll if remembered."

**Godot's `AudioStreamRandomizer` (Godot 4).** This engine class plays a random sound from a pool, and one of its playback modes, `PLAYBACK_RANDOM_NO_REPEATS`, is documented as avoiding the same sound twice in a row when possible. That is the NES rule applied to footsteps. Memory of one, reroll on repeat. You will use it next week.

**Minecraft (Java Edition).** A world seed is a 64-bit signed integer, per the Minecraft Wiki, and a text seed is turned into a 32-bit number with Java's `hashCode()`. Players share seeds because the same seed and the same game version give the same world. The wiki notes that this breaks across versions when the generation code changes. That is the lesson from Python's reproducibility note, at the scale of a whole planet. A seed only reproduces a result together with the exact code that consumed it.

The Tetris randomizers and the sound randomizer vary the rule and the memory. Minecraft shows the seed half of the model. Same structure in every case: a seeded source of numbers, a small memory, and a rule that turns numbers into content.

### Design judgment

Pick the randomizer by the worst experience you are willing to allow.

- **Pure random** is the only rule players cannot predict. It also allows droughts of any length. Pick it when a bad streak is fine or even funny, such as cosmetic variety.
- **Reroll-on-repeat** (NES, TGM, sound no-repeat) removes the most visible annoyance, back-to-back repeats, at almost no cost. It does very little for long droughts. It fits sounds and animations, where a repeat is what players notice.
- **A bag** caps droughts and makes the counts exact. Its cost is predictability. A player who has seen six different pieces knows the seventh. In a competitive puzzle game that is a skill to reward. For loot, a player who can see or reset the bag can exploit it. [MA102 week 2](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) works through who wins and who loses when a bag is shared.
- **Where the memory lives is a design decision.** Per player, per run, per level, or per server all behave differently. A bag reset each level means the first pieces of every level are more predictable.

Before you choose, ask yourself two questions. What is the longest drought I accept? Can the player see or reset the memory?

### A seeded bag in Godot

Because `Array.shuffle()` uses the global seed, write the shuffle with your own generator. This is the Fisher-Yates shuffle. Walk from the end of the array to the start and swap each slot with a random slot at or before it:

```gdscript
const PIECES := ["I", "J", "L", "O", "S", "T", "Z"]
var rng := RandomNumberGenerator.new()
var bag: Array = []

func shuffle_with(r: RandomNumberGenerator, a: Array) -> void:
    for i in range(a.size() - 1, 0, -1):
        var j := r.randi_range(0, i)
        var tmp = a[i]
        a[i] = a[j]
        a[j] = tmp

func next_piece() -> String:
    if bag.is_empty():
        bag = PIECES.duplicate()
        shuffle_with(rng, bag)
    return bag.pop_back()
```

Note `randi_range(0, i)` includes `i`. A slot may swap with itself. Leave that out (use `i - 1`) and some orders can never appear, which is a classic shuffle bug.

## 3. Spawning in space: rejection sampling

Pieces are random choices from a list. Enemies need random positions. The simple version is two uniform rolls:

```python
x = rng.uniform(0, W)
y = rng.uniform(0, H)
```

The problem is fairness. Sooner or later an enemy lands on top of the player, and the player loses a life to a spawn they could not react to. So you add a rule. Nothing spawns within a **safe radius** of the player.

The easiest correct way to follow a rule like that is **rejection sampling**. Pick a point, test it, throw it away if it fails, try again. Always cap the number of tries, or a bad arena can freeze your game in an endless loop.

```python
def spawn_position(rng, px, py, safe=150, attempts=20):
    for tries in range(1, attempts + 1):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if (x - px) ** 2 + (y - py) ** 2 >= safe * safe:
            return x, y, tries
    return None, None, attempts
```

The distance test compares squared distances, so no square root is needed. [Week 10](w10-collision-basics-aabb-and-circles.md) showed why that is safe. When the function gives up it returns `None`, and the caller decides what to do. It can skip this spawn or try again next frame.

### How many tries will it take?

Each try succeeds with probability `p`, the share of the arena outside the safe circle. With the player in the middle of an 800 × 600 arena and a 150 px radius, the circle covers `π × 150² = 70,686` of `480,000` square pixels, so `p = 1 − 0.147 = 0.853`. On average you need `1/p` tries. The chance that all 20 tries fail is `(1 − p)^20`.

| Safe radius (px), player centered | Share of arena allowed `p` | Mean tries `1/p` | Chance all 20 tries fail |
|---|---|---|---|
| 150 | 85.3% | 1.17 | about 2 × 10⁻¹⁷ |
| 250 | 59.1% | 1.69 | about 2 × 10⁻⁸ |
| 350 | 24.9% | 4.01 | 0.3% |
| 450 | 2.3% | 43.5 | 63% |

For radii above 300 px (the 350 and 450 rows) the circle pokes out of the top and bottom of the arena, so those shares were measured on a 1-pixel grid, not with the circle formula. The 150 and 250 rows fit inside and match `1 − πr² / 480,000`. The lab's tests check the 150 px row by simulation (1.17 tries on average).

Read the table from the top. For normal radii, rejection sampling costs almost nothing. Near the bottom it collapses. At 450 px nearly every try lands too close, and the spawner gives up on most calls. If your design wants enemies to appear "far away," don't reject your way there. Sample the far region directly. For example, pick one of the four arena edges and a random point along it.

With the player in a corner, three quarters of the circle falls outside the arena, so `p` rises to 96.3%. The same code costs a different amount depending on where the player stands. That's normal for rejection sampling, and it's why you measure.

## 4. Picking what to spawn: weighted choices

Position is half of a spawn. The other half is what to spawn. A spawn table is a list of options with weights:

```python
SPAWN_TABLE = [("grunt", 70), ("runner", 25), ("brute", 5)]
kinds, weights = zip(*SPAWN_TABLE)
kind = rng.choices(kinds, weights=weights, k=1)[0]
```

Python's `random.choices` draws with replacement according to relative weights, so the weights don't need to add to 100. Godot 4's `RandomNumberGenerator.rand_weighted()` takes an array of weights and returns an index, where a weight of 0 means that index is never chosen. The math of weights, including why changing one weight changes every other entry's chance, is [MA102 week 9](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md). For now, know that a brute here appears `5 / (70 + 25 + 5) = 5%` of the time.

Keep the table as data, a list or a dictionary (week 6), not as a chain of `if` statements. A designer can then retune it without touching the logic, and you can load a different table per wave.

## 5. Procedural variety: randomness inside ranges

"Procedural" just means generated by code instead of placed by hand. In a small arcade game most procedural variety is humble: every enemy gets a speed between 80 and 120, every asteroid a size between 0.8 and 1.2 times normal, every wave a count between 5 and 8.

Three habits keep this under control:

1. **Randomize within ranges you chose on purpose.** Write the range down as data next to the spawn table. "Speed 80 to 120" is a design statement. `rng.uniform(0, 500)` is a bug waiting for a playtester.
2. **Tie difficulty to something that is not random.** Let the wave number set the range, and let randomness pick inside it. For example `count = rng.randint(3 + wave, 5 + wave)`. Players forgive variety. They don't forgive a wave 2 that is harder than wave 9.
3. **Log the seed.** Print the run seed at the start of every run and show it on the game-over screen. When a tester reports "the game spawned four brutes at once," the seed lets you replay it. This is week 12's debugging, made possible by week 13's generator.

A **daily challenge** is this idea turned into a feature. Build the seed from the date, for example `seed = 20260928`, and every player gets the same run that day. It only works if gameplay draws from its own generator (section 1). If a player's particle setting changes the sequence, the "same" daily run differs between players.

## In-class activity (25 minutes)

Pairs, one laptop, the lab 13 starter files.

1. **Predict (5 min).** Before running anything, each person writes down the longest I drought they expect from each randomizer in 100,000 pieces. Write the numbers on a sticky note.
2. **Implement (12 min).** One person writes `nes_style`, the other `seven_bag`. Swap and review each other's code against the rule in section 2. Run `python randomizers.py`.
3. **Break the seed (5 min).** Add one line to `report()` that calls `rng.random()` once on the pure random generator before dealing. Rerun. Which numbers changed? Which stayed the same in expectation? Explain in one sentence why a cosmetic effect sharing this generator would do the same thing.
4. **Report (3 min).** Compare your sticky-note guesses with the output. Expected output: the three rows of the table in section 2, and one sentence each about the biggest surprise.

## Common misconceptions

- **"Random means the computer picks something truly unpredictable."** A PRNG is fully determined by its seed. That is a feature. It makes runs replayable and bugs reproducible.
- **"Seeding makes the game less random for players."** Players never see the seed unless you show it. A seed taken from the clock gives a different run every time. You only fix the seed when you want repeatability, for tests, replays or daily runs.
- **"No-repeat rules fix droughts."** They fix back-to-back repeats. The NES-style rule still allowed a 55-piece drought in our run. Only memory of the whole cycle, like a bag, caps droughts.
- **"`Array.shuffle()` uses my `RandomNumberGenerator`."** In Godot 4 it uses the global seed. Write your own shuffle, or seed the global generator, if the order must be reproducible.

## Check yourself

1. A game uses a bag of 14 pieces, two copies of each of the seven. What is the longest possible run of non-I pieces between two I pieces? Reason from where the I pieces can sit in consecutive bags.
2. You change the NES rule so that the first roll is from 0 to 6 (no dummy), with the same reroll. What is the repeat chance now? Is it higher or lower than `1/28`, and why?
3. Your spawner uses a 200 px safe radius with the player centered in an 800 × 600 arena, and the circle fits inside. Compute `p` and the mean number of tries.
4. A teammate's game uses Godot's global `randf()` for both enemy positions and screen-shake jitter. A tester's seed doesn't reproduce a bug on your machine. Name the most likely cause and the fix.
5. You want enemies never to spawn within 450 px of a centered player in an 800 × 600 arena. Using the table in section 3, explain why rejection sampling is a poor fit and describe a better sampler.

<details>
<summary>Answers</summary>

1. The drought is longest when both I pieces of one bag come first and both I pieces of the next bag come last. Between the second I of the first bag and the first I of the next, you have the other 12 pieces of the first bag and the first 12 of the second: `12 + 12 = 24`.
2. The first roll is rejected only when it equals the previous piece, `1/7`. Then the second roll repeats with chance `1/7`. So `1/49 ≈ 2.0%`, lower than `1/28 ≈ 3.6%`. The dummy value was a second way to get rejected, and each rejection is a chance to repeat. Removing it cuts repeats.
3. `π × 200² = 125,664`. `p = 1 − 125,664 / 480,000 = 0.738`. Mean tries `1 / 0.738 ≈ 1.36`.
4. The shake calls `randf()` a varying number of times (it depends on frame rate and on how many hits happened), so later spawn positions depend on the machine. Give spawning its own seeded `RandomNumberGenerator` and let effects use the global one or another instance.
5. Only 2.3% of the arena is allowed, so the average spawn needs about 43 tries, and with a 20-try cap about 63% of calls fail. Sample the allowed region directly. Pick a corner region or an edge strip that lies entirely beyond 450 px, then pick a uniform point inside it.

</details>

## Lab / assignment hook

[Lab 13, seeded randomizers and a fair spawner](../labs/lab13.md). You implement the NES-style and bag randomizers, reproduce the section 2 table, write the rejection sampler and its tests, then port the seeded bag and spawner to your Godot arcade game with a run seed shown on the game-over screen. It feeds the final arcade game (week 15).

## Sources

- Python Software Foundation, `random` module documentation (Python 3.14 docs). Mersenne Twister with period 2^19937 − 1, the warning against security use, `choices` with relative weights, and the "Notes on Reproducibility" guarantee that only `random()` is stable across versions for a given seed. https://docs.python.org/3/library/random.html
- Godot Engine documentation (stable, Godot 4.7), "Random number generation" tutorial. The global seed is random by default; `randomize()`, `randi_range()`, `randf_range()`, `pick_random()`, `shuffle()`. https://docs.godotengine.org/en/stable/tutorials/math/random_number_generation.html
- Godot Engine documentation (Godot 4.7), `RandomNumberGenerator` class. PCG32 as the current algorithm, the note that the algorithm should not be depended upon, `seed`, `state` and `rand_weighted()`.
- Godot Engine documentation (Godot 4.7), `Array` class. `shuffle()` and `pick_random()` use the global random seed.
- Godot Engine documentation (Godot 4.7), `AudioStreamRandomizer` class. `PLAYBACK_RANDOM_NO_REPEATS` avoids playing the same stream twice in a row when possible.
- Tetris Wiki, "Random Generator". The 7-bag rule, the 12-piece maximum gap between I pieces, and its origin in *The New Tetris*. https://tetris.wiki/Random_Generator
- Tetris Wiki, "Tetris (NES, Nintendo)" (1989 North American release). The two-roll randomizer: a 0-7 roll rejected on the dummy value 7 or a repeat, then a 0-6 roll dealt unconditionally. https://tetris.wiki/Tetris_(NES,_Nintendo)
- Tetris Wiki, "TGM randomizer". History of 4 pieces, 4 rerolls in TGM and 6 in TGM2, and the rule that the first piece is never S, Z or O. https://tetris.wiki/TGM_randomizer
- Minecraft Wiki, "Seed (level generation)" (Java Edition). 64-bit signed seeds, text seeds converted with `hashCode()` to 32 bits, and seeds reproducing worlds only within the same version. https://minecraft.wiki/w/Seed_(level_generation)
- Simulation figures in section 2 and the lab tests: lab 13 starter code with the reference solution, `random.Random(13)`, 100,000 pieces per randomizer, run with Python 3.13.5.

## Interactive spec: examples/w13-randomizer-droughts.html

**The one insight:** three randomizers deal I pieces at the same average rate, but only the bag has a hard wall on drought length. The lanes look equally random. The histogram shows the wall.

**Layout.** Two linked views stacked on mobile, side by side from 900 px.

- **Top view, "What the player sees":** three horizontal lanes labelled Pure random, NES style and 7-bag. Each lane shows the last 70 pieces dealt as small squares with a one-letter label, newest on the right. I pieces use the accent color; the other six use one neutral tone with a thin outline (no need for seven colors). Under each lane show the current run of non-I pieces since the last I as a live number ("waiting for I: 9").
- **Bottom view, "What the player remembers":** a histogram per randomizer (small multiples, one row each, shared x axis 0 to 60+, last bin "60+"). Y axis is share of droughts. Draw a vertical marker at the longest drought seen so far with its value. Draw a dashed vertical line at x = 12 labelled "bag limit" on all three rows.

**Controls.**
- Seed: number input, default 13. Changing it resets all three lanes.
- Buttons: "Deal 1", "Deal 100", "Deal 1,000", "Deal 100,000" (the last computes without animating), and "Reset".
- Toggle: "Show theory" overlays the pure-random geometric curve `P(gap = g) = (6/7)^g × (1/7)` on the pure random row as a line.
- Reduced motion: no sliding animation, lanes redraw in place.

**Readout table** beside the histogram, one row per randomizer, columns: pieces dealt, share of I, mean drought, longest drought, share of droughts 20+, repeat rate. These must match the lecture table exactly for seed 13 and 100,000 pieces when the page uses the same algorithms and generator semantics. Because the page runs in JavaScript, it will not reproduce Python's Mersenne Twister numbers. Use a small seeded PRNG (mulberry32 is fine), state in the page footer that the exact maxima differ from the Python table, and test against the analytic values instead.

**Algorithms (each randomizer gets its own PRNG instance seeded with the same seed).**
- Pure: `piece = PIECES[floor(r() * 7)]`.
- NES: `roll = floor(r() * 8)`; if `roll == 7` or `PIECES[roll] == prev`, then `roll = floor(r() * 7)`; `prev = PIECES[roll]`.
- Bag: Fisher-Yates shuffle of the seven pieces with `j = floor(r() * (i + 1))`, deal in order, refill when empty.
- Drought: number of pieces strictly between consecutive I pieces. Repeat rate: share of positions where the piece equals the previous one.

**Test values (after 100,000 pieces, any seed).** Share of I within 0.140 to 0.146 for all three. Mean drought within 5.9 to 6.1 for all three. Repeat rates within 0.139 to 0.147 (pure), 0.033 to 0.039 (NES), 0.018 to 0.022 (bag). Bag longest drought exactly 12 or less, and equal to 12 for almost every seed at 100,000 pieces. Pure random share of droughts 20+ within 0.041 to 0.050 (theory 0.0458).

**Accessibility.** All buttons reachable by keyboard; the seed input has a label; the I piece is marked by both color and the letter; the readout table is real HTML text.
