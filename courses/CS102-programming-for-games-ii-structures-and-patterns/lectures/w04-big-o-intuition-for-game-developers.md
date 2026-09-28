# CS102 · Week 04 — Big-O Intuition for Game Developers

**Why this matters:** A game has about 16.7 milliseconds to produce each frame at 60 frames per second. Code that is fine with 50 enemies can eat the whole frame with 500, and the reason is almost never "Python is slow." It is how the amount of work grows as the number of things grows. Big-O is the vocabulary for that growth, and it tells you, before you ship, where your game will fall over.

**You will be able to:**
- Count the operations a loop or nested loop performs and state its growth class (O(1), O(log n), O(n), O(n log n), O(n²)).
- Compute the largest `n` that fits a frame budget from a measured cost per operation.
- Predict how much a 10× faster machine buys an O(n) algorithm versus an O(n²) one.
- Rewrite an all-pairs proximity check as a uniform grid and state when the grid stops helping.

**Before class:** Nystrom, *Game Programming Patterns* (2014), "Spatial Partition" chapter, up to "Design Decisions". Reread [CS101 week 3, the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md), section 3.

**Prerequisites from earlier courses:** [CS101 week 3, loops and the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md) (what runs once per frame). [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md) (the note that `insert(0, ...)` shifts every item). [CS101 week 10, collision basics](../../CS101-programming-for-games-i/lectures/w10-collision-basics-aabb-and-circles.md) (the circle test we count here). [MA101 week 14, squared distance](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (section 5 introduces the pair count). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (what `log₂ n` means).

**Interactive:** [w04-pair-checks-budget.html](../examples/w04-pair-checks-budget.html). Keep it open during section 2.

---

## 1. Six minutes to load a game

In February 2021 a player who wrote under the name t0st published an investigation of why GTA Online took about six minutes to load on their PC. They profiled the game and found two loops doing far more work than they needed to. The first parsed a 10-megabyte JSON file of store items, and the string routine it called measured the length of the whole remaining string on every step. The second inserted about 63,000 items into an array and, before each insert, compared the new item against every item already there to reject duplicates. Their patch cut the load to 1 minute 50 seconds. Rockstar confirmed the finding, shipped a fix in March 2021 and paid the author $10,000 through its bug bounty.

Neither loop was "slow code" in the sense a beginner means. Each individual comparison took nanoseconds. The trouble was the count. Comparing each of 63,000 items against everything before it is about 2 billion comparisons (the author computed 1,984,531,500). Nothing about the hardware can make 2 billion of anything free.

This lecture gives you the tool to see that coming. You will count work as a function of `n`, the number of things, and read off how it grows.

### Counting instead of timing

Timing a function tells you how long it took on one machine, with one input, today. Counting tells you how the cost *changes* when the input grows, on any machine. Game programmers need both, but counting comes first because it predicts.

Take three loops over a list `units` of length `n`:

```python
# A: look at one element
first = units[0]                      # 1 step, whatever n is

# B: visit every element once
for u in units:                       # n steps
    u.update(dt)

# C: visit every pair once
for i in range(n):
    for j in range(i + 1, n):         # (n-1) + (n-2) + ... + 1 + 0 steps
        check(units[i], units[j])
```

Loop C's inner body runs `(n − 1) + (n − 2) + ... + 1 + 0` times. That sum is `n(n − 1)/2`. You met it in MA101 week 14 as the number of pairs among `n` objects. For 100 units it is 4,950. For 1,000 units it is 499,500.

### The growth classes

**Big-O notation** keeps only the part of the count that dominates when `n` is large and drops constant multipliers. `n(n − 1)/2 = 0.5n² − 0.5n`, and for large `n` the `n²` term swamps the rest, so loop C is **O(n²)**, read "order n squared." Loop B is **O(n)**. Loop A is **O(1)**, "constant time," because its cost doesn't depend on `n` at all.

Five classes cover almost everything you will write in this course:

| Class | Name | Typical game code |
|---|---|---|
| O(1) | constant | read `units[7]`; look up a key in a dictionary (week 5) |
| O(log n) | logarithmic | binary search in a sorted leaderboard; one step down a balanced tree (week 7) |
| O(n) | linear | update every entity once per frame; scan a list for a match |
| O(n log n) | "n log n" | sort the render list by depth; sort a leaderboard |
| O(n²) | quadratic | every unit checks every other unit; insert-with-duplicate-scan |

Here is what those classes mean in counts. The `log₂ n` column is the number of times you can halve `n` before reaching 1 (MA101 week 5).

| n | log₂ n | n | n log₂ n | n² |
|---|---|---|---|---|
| 10 | 3.3 | 10 | 33 | 100 |
| 100 | 6.6 | 100 | 664 | 10,000 |
| 1,000 | 10 | 1,000 | 9,966 | 1,000,000 |
| 10,000 | 13.3 | 10,000 | 132,877 | 100,000,000 |
| 1,000,000 | 19.9 | 1,000,000 | 19,931,569 | 1,000,000,000,000 |

Read down the columns. Multiply `n` by 10 and the O(n) column grows 10×, the O(n²) column grows 100×, and the O(log n) column grows by about 3.3. That last one is why binary search on a million items needs only about 20 steps.

### The doubling test

The quickest way to use Big-O in your head is to ask what happens when `n` doubles:

- O(1): same cost.
- O(log n): one more step.
- O(n): twice the cost.
- O(n log n): a bit more than twice.
- O(n²): four times the cost.

You can run the doubling test on a real program with a stopwatch. Time it at `n`, then at `2n`. If the time roughly doubles, you have linear work. If it roughly quadruples, you have a nested loop somewhere, and you should find it before a designer asks for a bigger battle.

## 2. Worked example: how many units fit in a frame?

### The hook

Every game that has aggro, auras, collisions or "nearby ally" buffs needs to know which pairs of units are close to each other. The obvious code checks every pair. It works perfectly in your test scene with 40 units. A designer then builds the siege level with 800, and the frame rate collapses. Nothing in the code changed. Only `n` did.

The same thing happened to GTA Online's loader with its duplicate check, and it happens to MMO servers during large fights (you'll see EVE Online below). The question this example answers is concrete. **Given a frame budget, what is the largest number of units the all-pairs check can handle, and what does a better algorithm buy?**

### The model

We measure the cost of one pair check once, then multiply by the count.

```
pairs(n)       = n (n − 1) / 2
T_naive(n)     = pairs(n) × c_pair
n_max          = largest n with T_naive(n) ≤ B
```

- `n` is the number of units.
- `c_pair` is the measured time for one pair check (subtract positions, square, compare against the squared radius from MA101 week 14).
- `B` is the part of the frame budget you give to proximity checks.

Here is the code. It returns both the number of close pairs (`hits`) and the number of checks performed, so you can compare work as well as time. This file is `labs/lab04-starter/proximity.py`.

```python
RADIUS = 10.0

def naive_pairs(units, radius=RADIUS):
    r2 = radius * radius
    hits = checks = 0
    n = len(units)
    for i in range(n):
        xi, yi = units[i]
        for j in range(i + 1, n):
            xj, yj = units[j]
            dx, dy = xi - xj, yi - yj
            checks += 1
            if dx * dx + dy * dy < r2:
                hits += 1
    return hits, checks
```

On the course reference machine (Python 3.13, Apple silicon laptop), one pass through the inner body costs about **50 nanoseconds**. That is `c_pair = 50 ns`. Your machine will differ, which is fine. The lab has you measure your own.

We give proximity checks **half the frame**, `B = 8 ms`, and leave the rest for movement, animation, AI and drawing.

### Numbers you can check

Units are scattered at random over a 1,000 × 1,000 world, with a 10-unit interaction radius. The "model" column is `pairs × 50 ns`. The "measured" column is from running `proximity.py`.

| n | pairs n(n−1)/2 | model ms | measured ms | fits 8 ms? (model) |
|---|---|---|---|---|
| 100 | 4,950 | 0.25 | 0.3 | yes |
| 250 | 31,125 | 1.56 | 1.6 | yes |
| 500 | 124,750 | 6.24 | 6.4 | yes |
| 1,000 | 499,500 | 24.98 | 23.8 | no, 3.1× over |
| 2,000 | 1,999,000 | 99.95 | 90.5 | no, 12.5× over |
| 4,000 | 7,998,000 | 399.9 | 365.7 | no, 50× over |

The last column divides the model time by 8 ms. The model tracks the stopwatch within about 10%. That is the point of counting. Once you know `c_pair` from one measurement, the count predicts the rest.

Now solve for `n_max`. We need `n(n − 1)/2 × 50 ns ≤ 8 ms`, so `n(n − 1) ≤ 320,000`. The quadratic formula gives `n = (1 + √(1 + 4 × 320,000)) / 2 ≈ 566.2`, so **566 units**. Check it: `566 × 565 / 2 = 159,895` pairs, times 50 ns, is 7.99 ms. One more unit and you are over.

### The faster-machine trap

Suppose you port the check to C# or C++ and each pair check becomes 10× cheaper, 5 ns. How many units fit now?

The pair count must now satisfy `n(n − 1) ≤ 3,200,000`, which gives `n ≈ 1,789`. Ten times the speed bought only **3.2× the units**, because `√10 ≈ 3.16`. That is the O(n²) tax. When the cost grows with `n²`, a speedup of `k` grows your capacity by `√k`. An O(n) algorithm would have grown by the full 10×.

This is the most useful sentence in the lecture. **Constant-factor speedups (a faster language, a faster machine, tighter code) help an O(n²) algorithm by only the square root of the speedup.** Changing the algorithm changes the exponent.

### Changing the algorithm: a uniform grid

Most pairs are nowhere near each other. A unit at one corner of the map can't be within 10 units of a unit at the other corner, so checking them is wasted work. A **uniform grid** (Nystrom's "Spatial Partition" chapter) divides the world into square cells as wide as the interaction radius. Each unit goes into one cell. A unit then only checks units in its own cell and the 8 cells around it, since anything farther must be more than one radius away.

```python
def grid_pairs(units, radius=RADIUS):
    r2 = radius * radius
    cells = {}                                  # (cx, cy) -> list of unit indices
    for i, (x, y) in enumerate(units):
        cells.setdefault((int(x // radius), int(y // radius)), []).append(i)
    hits = checks = 0
    for i, (x, y) in enumerate(units):
        cx, cy = int(x // radius), int(y // radius)
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                for j in cells.get((cx + ox, cy + oy), ()):
                    if j <= i:                  # count each pair once
                        continue
                    xj, yj = units[j]
                    dx, dy = x - xj, y - yj
                    checks += 1
                    if dx * dx + dy * dy < r2:
                        hits += 1
    return hits, checks
```

The grid uses a dictionary keyed by cell coordinates, a structure you'll study properly next week. For now, treat "look up a cell" as a constant-cost step.

How much work does the grid do? The world has `C = (1000 / 10)² = 10,000` cells. With units spread evenly, each cell holds `n / C` units on average, so each unit looks at about `9n / C` neighbors, and counting each pair once halves that. Add a fixed cost per unit for filling the grid and scanning 9 cells:

```
checks_grid(n) ≈ 4.5 n² / C
T_grid(n)      ≈ n × c_unit + checks_grid(n) × c_pair
```

On the reference machine `c_unit ≈ 1 µs` (nine dictionary lookups plus loop overhead). Here is the same run as before:

| n | naive checks | grid checks (measured) | 4.5 n²/C | grid ms (measured) | same hits? |
|---|---|---|---|---|---|
| 100 | 4,950 | 6 | 4.5 | 0.10 | yes |
| 500 | 124,750 | 114 | 112 | 0.47 | yes |
| 1,000 | 499,500 | 438 | 450 | 0.88 | yes |
| 2,000 | 1,999,000 | 1,846 | 1,800 | 1.96 | yes |
| 4,000 | 7,998,000 | 7,289 | 7,200 | 4.38 | yes |

At 4,000 units the grid performs about 1,100× fewer checks and runs 83× faster. It isn't 1,100× faster because the per-unit bookkeeping (`c_unit`) now dominates. That per-unit cost is O(n), which is exactly what you want to be paying.

Solve for the grid's `n_max` at 8 ms: `1 µs × n + 4.5n²/10,000 × 50 ns ≤ 8 ms`. The quadratic term is tiny, and the answer is **6,921 units**, twelve times the naive limit. The algorithm change beat the 10× faster machine by a factor of four, and you can still port it to C# later for another boost.

### Seeing it move

Open the interactive. The left view plots work against `n` for both methods, on the same linear axes, with the 8 ms budget drawn as a horizontal line. The naive curve bends upward and crosses the line at 566. The grid curve looks nearly flat. The right view is a frame bar, a 16.7 ms strip filled by the proximity cost for the current `n`. Drag the unit slider past 566 and watch the naive bar spill over the edge while the grid bar barely moves.

Then press "cluster." All units move into a 30 × 30 corner, the way players pile into one spot for a world boss. The grid bar jumps to match the naive bar. That's the next section.

### When the grid stops helping

The grid's estimate `4.5n² / C` assumed units spread evenly over all `C` cells. If they crowd into a few cells, the grid's pair count heads straight back to `n²/2`. The lab's `--clustered` run puts every unit in a 30 × 30 square:

| n (clustered) | naive checks | grid checks | naive ms | grid ms |
|---|---|---|---|---|
| 500 | 124,750 | 75,358 | 6.6 | 5.95 |
| 1,000 | 499,500 | 307,615 | 27.2 | 24.2 |
| 2,000 | 1,999,000 | 1,201,121 | 113.4 | 95.5 |

When everybody is close to everybody, there is no wasted work to skip. The number of *real* close pairs is itself quadratic (the `hits` column in the lab reaches 504,755 at 2,000 units), and no data structure can report half a million pairs without touching them. Big-O analysis must say which inputs it assumes. "O(n) for spread-out units, O(n²) for a crowd" is an honest description of the grid.

### Cross-game recognition

**GTA Online (PC, before the March 2021 fix).** The duplicate check is loop C in disguise. Item `k` is compared against the `k − 1` items before it, so loading `n` items costs `n(n − 1)/2` comparisons, or about 2 billion for 63,000 items. The string parse had the same shape. Each read step re-measured the remaining 10 MB string, so the work was proportional to the file length times the number of steps. Both were O(n²), and both became cheap once the repeated work was removed.

**EVE Online (Time Dilation, announced April 2011).** EVE runs each star system on one server process, and large fleet fights can put well over a thousand ships in one system. CCP's developer blog introducing Time Dilation explains that an overloaded server lets its queue of waiting work grow until a single event, such as a ship's destruction, stretches over many minutes, and it walks through how the fix would handle a fight of about 1,600 pilots. As a model, not CCP's own formula, think of it this way. Each ship's action must be delivered to every other ship present, so the updates per second grow roughly with the square of the ship count. Double the fleet and you roughly quadruple the load. CCP's answer was to slow the game clock for that system, down to a floor of 10% of real time according to EVE University's wiki, so that the server finishes every frame's work correctly rather than dropping it. They couldn't change the exponent of "everyone sees everyone," so they stretched `B`.

**Your own CS101 inventory.** CS101 week 5 noted that `insert(0, ...)` and `pop(0)` shift every item in a list. One shift is O(n). Doing it for each of `n` items, for example draining a list from the front in a loop, is O(n²) in total. Week 6 shows the fix.

Three different contexts, one shape. When a cost is "for each thing, look at all the other things," expect `n²/2` and ask what structure lets you skip most of them.

### Eyes-open design judgment

- **Big-O ignores constants, and at small `n` the constants win.** For 50 units the naive check takes 0.06 ms, and the grid's per-unit bookkeeping costs about the same. Write the simple version first. Switch when a measurement or a design target (the siege level, the world boss) says you must.
- **Budget from the design, not the benchmark.** The useful question is "what is the biggest fight the design wants?", followed by solving for `n_max`. If the design wants 2,000 units and the naive check caps at 566, you know in week one, not in beta.
- **Choose what degrades.** EVE chose to slow time. Other games cap the number of players in an area, or reduce update rates for distant objects. Each is a design decision with a player-facing cost. Make it on purpose.
- **Watch for hidden loops.** GTA's duplicate check hid a linear scan inside an insert, and its parser hid one inside a library call. A one-line call can be O(n). Next week's topic is exactly this, for lists and dictionaries.

### Check yourself on the worked example

1. With `c_pair = 50 ns` and a budget of 4 ms instead of 8 ms, what is `n_max` for the naive check?
2. A designer doubles the siege from 400 to 800 units. By what factor does the naive proximity cost change? Does 800 fit in 8 ms?
3. The world grows to 2,000 × 2,000 with the same 10-unit radius and units spread evenly. What happens to `C` and to the grid's pair checks for 4,000 units?

<details>
<summary>Answers</summary>

1. `n(n − 1) ≤ 2 × 4 ms / 50 ns = 160,000`, so `n = (1 + √640,001) / 2 ≈ 400.5`, and `n_max = 400`. Halving the budget cut capacity by only √2, the same square-root effect in reverse.
2. The cost grows by `(800 × 799) / (400 × 399) ≈ 4.0×`. 800 units need 319,600 pairs, or 15.98 ms. It doesn't fit.
3. `C` becomes `200² = 40,000`, four times as many cells. Grid checks become `4.5 × 4,000² / 40,000 = 1,800`, a quarter of the 7,200 before, because the same units are spread thinner.

</details>

## 3. Reading code for its growth

You won't always have a formula. Usually you have code. Four rules cover most cases.

**Sequential blocks add, and the biggest term wins.** An O(n) update followed by an O(n²) collision pass is O(n + n²), which is O(n²).

**Nested loops multiply.** An outer loop over `n` units with an inner loop over `m` spells costs O(n × m). If `m` is fixed by the design (every unit has at most 4 spells), that is O(n). Keep a letter for anything the design can grow.

**Calls cost what their bodies cost.** This is the rule people forget. `if x in some_list` hides a loop over `some_list`. `some_list.remove(x)` finds `x` and then shifts everything after it. Sorting is O(n log n). When you call a library function inside a loop, find out its cost from the documentation. Microsoft's documentation for C#'s `List<T>.Contains`, for example, states that it performs a linear search and is O(n).

**Halving means log.** If each step throws away half of what's left, the step count is `log₂ n`. Binary search does this, and so does walking down a balanced tree.

### A short drill

What is the growth class of each fragment, with `n` enemies and `p` players?

```python
# 1
for e in enemies:
    if e.hp <= 0:
        enemies.remove(e)        # hmm

# 2
enemies.sort(key=lambda e: e.threat)
target = enemies[-1]

# 3
for p in players:
    for e in enemies:
        if dist2(p, e) < AGGRO2:
            e.target = p
```

Fragment 1 looks linear but `remove` scans and shifts, so each removal is O(n) and the loop is O(n²) in the worst case. It also has the modify-while-iterating bug from CS101 week 5, which skips elements. Fragment 2 is O(n log n) for the sort, and the pick is O(1). If you only need the maximum, `max(enemies, key=...)` is O(n) and cheaper. Fragment 3 is O(p × n). In a 5-player dungeon that's effectively linear in enemies. In a 200-player world event it is not.

## 4. Amortized cost: why `append` is O(1)

A Python list is a **dynamic array**, a block of memory with spare room at the end. When the spare room runs out, `append` allocates a bigger block and copies every element across. That copy is O(n). So is `append` O(n)?

On average, no. Because the new block is larger by a fixed *proportion*, big copies happen rarely. If the capacity doubles each time, then filling a list to `n` elements copies `1 + 2 + 4 + ... + n/2 < n` elements in total across all the resizes. Spread over `n` appends, that is less than one copy per append. We say `append` is **amortized O(1)**. Any single call may be slow, but the average over many calls is constant. (CPython grows lists by a smaller factor than 2, but the argument is the same for any fixed factor.)

Amortized is a promise about the total, not about each frame. If one frame happens to trigger a resize of a 1-million-element list, that frame pays for it. When a hitch matters more than the average, preallocate. C#'s `List<T>` has a constructor that takes a starting capacity for exactly this reason.

## 5. When not to care

Big-O is a tool for the parts of the frame that scale with content. Plenty of code doesn't. Parsing a config file once at startup, sorting a 12-item menu, or scanning 8 party members is fine at any growth class. Spend your attention where the design can make `n` large: entities, projectiles, players in view, items in a database, messages per tick.

Profiling, running the game under a tool that records how long each function takes, tells you where time goes today. It is the measuring habit from [CS101 week 12, debugging](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md), applied to time instead of wrong values. Big-O tells you where it will go when the content team triples the numbers. Use both.

## In-class activity (25 minutes)

In pairs, with laptops and `labs/lab04-starter/proximity.py`.

1. Run `proximity.py` on your machine. From the `n = 1000` row, compute your own `c_pair` (naive ms divided by checks).
2. Using your `c_pair`, predict the naive time for `n = 3000`. Add 3000 to the `sizes` list, run it and compare. Record the percentage error.
3. Compute your machine's `n_max` for an 8 ms budget and for a 4 ms budget.
4. Change `RADIUS` to 40 (a big aura) without changing anything else. Predict, before running, whether the grid's check count goes up or down, and by how much. Run it and explain the result using `4.5n²/C`.

Expected output: your `c_pair`, the prediction and its error, two `n_max` values, and a two-sentence explanation for step 4. (Hint for step 4. `C` shrinks 16×.)

## Common misconceptions

- **"O(n²) means slow."** It means the cost grows with the square of `n`. At `n = 20` it is 190 checks and nobody cares. Big-O predicts growth, not speed at one size.
- **"A faster language fixes it."** A 10× speedup gives an O(n²) algorithm only √10 ≈ 3.2× more capacity. Changing the algorithm changes the curve.
- **"The grid is O(n)."** Only while units stay spread out. In a crowd it returns to O(n²), because the number of genuinely close pairs is itself quadratic.
- **"One line of code is O(1)."** `x in list`, `list.remove(x)`, `list.insert(0, x)` and `sorted(list)` are each one line and none of them is constant time.

## Check yourself

1. A loop visits each of `n` projectiles and, for each, loops over `w` walls. The level has 30 walls and up to 400 projectiles. State the growth class you'd write in a design review and the worst-case number of checks.
2. You time a function at `n = 1,000` (3 ms) and at `n = 2,000` (12 ms). What growth class do you suspect? Predict the time at `n = 4,000`.
3. With `c_pair = 20 ns` and an 8 ms budget, what is the naive `n_max`? How many units would a 4× faster machine allow?
4. Why does `binary search` on 1,000,000 sorted scores need at most about 20 comparisons?
5. A teammate says "our grid made collisions O(n), so we can support any raid size." Write the one-sentence correction, with the case that breaks it.

<details>
<summary>Answers</summary>

1. O(n × w). Walls are fixed by the level, so in practice linear in projectiles, but write `n × w` because levels vary. Worst case `400 × 30 = 12,000` checks.
2. Doubling `n` quadrupled the time (3 to 12 ms), so O(n²). At 4,000 expect `12 × 4 = 48 ms`.
3. `n(n − 1) × 20 ns / 2 ≤ 8 ms` gives `n(n − 1) ≤ 800,000`, so `n ≈ 894.9`, round down to 894. A 4× faster machine gives `√4 = 2×`, about 1,789 units (solve `n(n − 1) ≤ 3,200,000`).
4. Each comparison halves the remaining range. `log₂ 1,000,000 ≈ 19.9`, so 20 halvings reduce a million candidates to one.
5. The grid is O(n) only while players are spread across many cells. A raid that stacks on one boss puts everyone in the same few cells, and the pair checks go back toward `n²/2`.

</details>

## Lab / assignment hook

[Lab 04, the proximity budget](../labs/lab04.md). You measure `c_pair` and `c_unit` on your machine, fit the model to your own timings, find `n_max` for both methods, and write a one-page note to a designer stating the largest battle the current code supports and what it would cost to double it.

## Sources

- t0st, "How I cut GTA Online loading times by 70%", nee.lv, 28 February 2021, with the author's later update. Six-minute load, 10 MB JSON with about 63,000 items, 1,984,531,500 duplicate-check comparisons, 1 min 50 s after the patch, Rockstar's fix in March 2021 and the $10,000 bug bounty payment. https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/
- CCP Veritas, "Introducing Time Dilation (TiDi)", EVE Online developer blog, 22 April 2011. An overloaded server's queue of waiting work stretching events such as ship death over minutes; slowing the game clock as the remedy; a worked scenario of a 1,600-pilot fight. https://www.eveonline.com/news/view/introducing-time-dilation-tidi
- EVE University Wiki, "Time dilation" (current). Floor of 10% of real time, the trigger on node load, and a note that server load grows roughly with the square of players on grid. https://wiki.eveuniversity.org/Time_dilation
- Nystrom, R. (2014). *Game Programming Patterns*, "Spatial Partition" chapter. The all-pairs battle check as O(n²) and the fixed-grid remedy. https://gameprogrammingpatterns.com/spatial-partition.html
- Microsoft Learn, "List<T>.Contains(T) Method" (.NET 8 and later). Linear search, O(n). https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.contains
- Timings in this lecture: `labs/lab04-starter/proximity.py`, run on CPython 3.13.5 on an Apple silicon laptop, September 2026. Your numbers will differ; the ratios should not.

## Interactive spec: examples/w04-pair-checks-budget.html

**The one insight:** the naive all-pairs cost curves upward and crosses the frame budget at a specific `n`, a 10× faster machine moves that crossing only about 3.2×, and a grid flattens the curve until units cluster.

**Layout (two linked views, stacked on mobile, side by side at ≥ 900px):**

- Left: line chart. x-axis `n` units, 0 to 8,000, linear. y-axis milliseconds, 0 to 40, linear, values above 40 clip at the top edge with a small "↑ N ms" label. Two lines: naive `T_naive(n)` and grid `T_grid(n)`. A dashed horizontal line at the budget `B`. A vertical marker at the current `n`. A dot where each line crosses `B`, labelled with that `n_max`.
- Right: "frame bar". A horizontal strip representing 16.67 ms. Two rows (naive, grid), each filled from the left to its cost for the current `n`. The budget `B` is drawn as a tick on the strip. Cost beyond 16.67 ms spills past the strip in the alert color and shows "N frames" (cost / 16.67, one decimal).

**Controls:**

- `n` slider, 10 to 8,000, step 10, default 500. Also a number input bound to it.
- `c_pair` select: 50 ns (Python, default), 5 ns ("10× faster machine"), 20 ns.
- Budget `B` slider, 1 to 16 ms, step 0.5, default 8.
- Toggle "cluster": off by default. When on, the grid uses the clustered formula below.
- Button "show 10× machine" that sets `c_pair` to 5 ns and briefly highlights both `n_max` labels (old and new).

**Formulas (exact):**

```
pairs(n)      = n (n − 1) / 2
T_naive(n)    = pairs(n) × c_pair                      (ms: × 1e-6 when c_pair in ns)
C             = 10,000                                 (100 × 100 cells)
c_unit        = 1.0 µs
spread:       checks_grid(n) = 4.5 n² / C
clustered:    checks_grid(n) = 0.6 × pairs(n)          (matches the lab's measured 0.60 ratio)
T_grid(n)     = n × c_unit + checks_grid(n) × c_pair
n_max_naive   = floor((1 + sqrt(1 + 8 B / c_pair)) / 2)     (B and c_pair in the same unit)
n_max_grid    = largest n with T_grid(n) ≤ B (solve numerically, step 1)
```

**Test values (must match to the shown precision):**

- `c_pair = 50 ns`, `B = 8 ms`: `n_max_naive = 566`; `T_naive(566) = 7.99 ms`; `T_naive(1000) = 24.98 ms`; `n_max_grid = 6,921` (spread).
- `c_pair = 5 ns`, `B = 8 ms`: `n_max_naive = 1,789`.
- `c_pair = 20 ns`, `B = 8 ms`: `n_max_naive = 894`.
- `n = 4,000`, `c_pair = 50 ns`, spread: `T_grid = 4.36 ms`, `T_naive = 399.9 ms` (shows "24.0 frames").

**Readouts (always visible, copyable):** `n`, pairs, naive ms, grid checks, grid ms, both `n_max` values, and "10× machine gives ×3.16 capacity" computed as `n_max(c/10) / n_max(c)` to two decimals.

**First screen:** `n = 500`, naive bar at 6.24 ms, grid at 0.51 ms, both below budget, with the naive curve visibly bending toward the budget line just to the right of the marker.

**Accessibility:** all controls keyboard operable; chart has a text summary updated on change (`aria-live="polite"`); respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. No game art or logos.
