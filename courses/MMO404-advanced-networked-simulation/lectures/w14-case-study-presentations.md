# MMO404 · Week 14 — Case study presentations

**Why this matters:** Studios publish headline numbers, such as a record battle, a tick rate or a region cap, and rarely publish how they made them possible. An engineer who can turn a headline into the constraint it implies can learn from every public postmortem, spot marketing that cannot be true, and ask the one question in a design review that matters. This week you learn that method and use it to build your case study presentation.

**You will be able to:**
- Invert a cost model to compute the largest per-pair or per-player cost that a published headline allows, from player count, tick rate, game speed and budget share.
- Compare the implied constant with known hardware costs and list what must be true for the headline to hold.
- Bracket a conclusion by moving each assumption across a plausible range, and say which assumption the conclusion depends on.
- Structure and deliver a 12-minute case study teardown that separates sourced facts, model results and your own judgment.

**Before class:** Choose your case from the instructor's list and read its primary source in full (developer blog, postmortem or talk). Peter Norvig, "Teach Yourself Programming in Ten Years" (norvig.com), the table of approximate timings in the answers section. Reread the worked examples of this course's [week 1](w01-limits-of-the-zone-model.md) and [week 13](w13-cost-engineering.md).

**Prerequisites from earlier courses:** In this course, [week 1](w01-limits-of-the-zone-model.md) (the tick-cost model `C = c_p n + c_i P`), [week 5](w05-bandwidth-shaping-and-lod-for-networking.md) and [week 13](w13-cost-engineering.md) (bytes and dollars per player). [MMO302 week 12, single-shard architectures and time dilation](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md). Launch postmortems are treated in depth in MMO407 ([MMO407 syllabus](../../MMO407-launch-scaling-and-post-mortems/syllabus.md)).

**Interactive:** [w14-implied-cost-ladder.html](../examples/w14-implied-cost-ladder.html). Keep it open during section 2.

---

## 1. What a case study presentation is for

This week each group presents a teardown of one shipped system from the instructor's list. A **teardown** takes a system you cannot see inside, such as a record battle, a crowd policy or a server-density project, and reconstructs what it must be doing from what the public can check. You have no access to the source code. You have a few published numbers, the models from this course and your judgment.

A good teardown does three things a summary does not.

- **It turns a headline into a constraint.** "6,557 pilots in one system" is a fact. "So the server spent at most 233 ns per pair of pilots per tick" is a constraint, and constraints are what engineers can reason about.
- **It names what must be true.** A constraint that looks impossible means some assumption is wrong. Finding which one is the insight.
- **It separates three kinds of claim.** Things the source says, things your model computes from them, and things you believe. Your audience must always know which kind they are hearing.

The rest of this lecture teaches the method on one worked case, then turns it into a presentation structure.

## 2. Worked example: what must be true for 6,557 pilots in one system?

### The hook

In January 2014, the battle of B-R5RB put 2,670 EVE Online pilots in one star system at the same time, and the fight ran at 10% speed for most of 21 hours. On 6 October 2020, the battle at FWST-8 peaked at 6,557 pilots in one system, with 8,825 players taking part over about 12 hours. CCP's battle report and Guinness World Records give the same two figures, and Guinness listed them as two records, the largest multiplayer videogame PvP battle (8,825) and the most concurrent participants in such a battle (6,557).

Here is the puzzle. The second battle had 2.46 times as many pilots. But week 1 taught you that a crowd costs per pair, and pairs grow with the square. 6,557 pilots make 6.03 times as many ordered pairs as 2,670. EVE's time dilation floor was 10% speed in both years, so the server did not get more time. What did it get? The answer cannot be read off any press release. It can be computed.

### The model

Start from week 1's tick cost, written for one server running one game tick:

```
C = c_p × n + c_i × n (n − 1) × g
```

- `n` is the number of players the server simulates together.
- `c_p` and `c_i` are the CPU time per player and per interacting ordered pair per tick, as in week 1.
- `g` is the **pair share**, the share of all ordered pairs that interact. In week 1 it was `h² + (1 − h²) f`. For a fight where everyone is in range of everyone, `g = 1`.

(Week 1 used `n²` for the pair count. Here we use `n (n − 1)`, which excludes a player paired with itself. For hundreds of players the two differ by less than 1%.)

The server keeps up if `C` fits the real time it has for one game tick. That time is

```
budget = β / (f_t × d)
```

- `f_t` is the tick rate in game ticks per second of game time.
- `d` is the game speed. `d = 1` is normal speed, and `d = 0.1` is EVE's time dilation floor, where one game second takes ten real seconds.
- `β` is the **usable share** of that time, the part not kept free for spikes and the operating system. Week 1 used 0.5. We start with `β = 1`, the most generous possible value.

Now invert the model. We know `n`, `f_t` and `d` from public sources. We do not know `c_i`. If the pair term alone had to fit the budget, `c_i` could be at most

```
c_i ≤ β / (f_t × d × n (n − 1) × g)
```

This is the **implied constant**. It is an upper bound. Any per-player work, any budget held back and any time spent on other things make the true value smaller still. That is what makes the method safe. When the bound itself looks too small to be possible, the conclusion survives every generous assumption you made along the way.

The final step is to compare the bound with the cost of something a computer actually does. Norvig's table of approximate timings on a typical PC gives about 1 ns to execute a typical instruction, 25 ns to lock and unlock a mutex and 100 ns to fetch a value from main memory. These are orders of magnitude, not measurements of any EVE server, and that is all the method needs.

### Numbers you can check

EVE's server tick runs once per second of game time, `f_t = 1`. Take `β = 1` and `g = 1` for now.

| Case | `n` | Tick rate | Game speed | Real budget per tick | Implied `c_i` at most |
|---|---|---|---|---|---|
| B-R5RB, EVE 2014 | 2,670 | 1 Hz | 10% | 10,000 ms | 1,403 ns |
| FWST-8, EVE 2020 | 6,557 | 1 Hz | 10% | 10,000 ms | 233 ns |
| FWST-8 at full speed | 6,557 | 1 Hz | 100% | 1,000 ms | 23 ns |
| Second Life, full region | 100 | 45 Hz | 100% | 22.2 ms | 2,245 ns |
| Week 1 zone, one crowd | 153 | 10 Hz | 100% | 100 ms | 4,300 ns |

Check the FWST-8 row by hand. The number of ordered pairs is `6,557 × 6,556 = 42,987,692`. The budget is 10 real seconds, `10⁹ × 10 = 10¹⁰` ns. Divide, and you get 233 ns per pair per tick.

Read the table from the bottom up.

- **The control row recovers what we know.** The week 1 zone used invented constants, so we know the truth, `c_i = 2 µs`. The method gives 4.3 µs. The gap has two causes, both named in the model. Week 1 kept half the tick free (`β = 0.5`, which halves the bound to 2.15 µs), and per-player work used 3 ms of the budget, which brings it to about 2.0 µs. The method gives an upper bound within a factor of about two of the truth, in the safe direction.
- **At full speed, FWST-8 is impossible under an all-pairs design.** 23 ns per pair is about 23 instructions, or a quarter of one main-memory fetch. No server can check range, decide visibility and prepare replication for a pair of ships in that time. The fight could not have run at normal speed with everyone interacting with everyone. Time dilation was not a comfort feature. It was the only way the headline could exist.
- **At 10% speed, FWST-8 allows 233 ns.** That is about two main-memory fetches per pair. Still very tight, and six times tighter than B-R5RB's 1,403 ns. Between 2014 and 2020, the per-pair work had to get about six times cheaper, or the pair share `g` had to fall, or the work had to be spread across more cores.

Here is the calculation as code. It is the core of Lab 14.

```python
def implied_pair_ns(n, tick_hz, speed=1.0, usable=1.0, pair_share=1.0):
    """Upper bound on CPU nanoseconds per interacting ordered pair per tick
    if the pair term alone filled the usable budget."""
    budget_s = usable / (tick_hz * speed)        # CPU seconds per game tick
    return 1e9 * budget_s / (n * (n - 1) * pair_share)

cases = [                       # name, players, tick Hz, game speed
    ("B-R5RB, EVE 2014",       2670,  1, 0.1),
    ("FWST-8, EVE 2020",       6557,  1, 0.1),
    ("FWST-8 at full speed",   6557,  1, 1.0),
    ("Second Life region",      100, 45, 1.0),
    ("Week 1 zone, one crowd",  153, 10, 1.0),
]
for name, n, hz, speed in cases:
    print(f"{name:23s} n={n:5d}  budget={1000 / (hz * speed):7.1f} ms"
          f"  pair cost <= {implied_pair_ns(n, hz, speed):6.0f} ns")
```

It prints:

```
B-R5RB, EVE 2014        n= 2670  budget=10000.0 ms  pair cost <=   1403 ns
FWST-8, EVE 2020        n= 6557  budget=10000.0 ms  pair cost <=    233 ns
FWST-8 at full speed    n= 6557  budget= 1000.0 ms  pair cost <=     23 ns
Second Life region      n=  100  budget=   22.2 ms  pair cost <=   2245 ns
Week 1 zone, one crowd  n=  153  budget=  100.0 ms  pair cost <=   4300 ns
```

### What must be true

A bound this tight is a list of hypotheses, not an answer. For FWST-8 at 10% speed, at least one of these must hold:

1. **Not every pair interacts every tick** (`g` well below 1). In EVE, space in a system is divided into grids, cubes roughly 16,000 km on a side, and pilots on different grids do not appear on each other's overview. A fleet fight on one grid pushes `g` back toward 1, so this hypothesis needs evidence about where the pilots actually were. If only a quarter of the pairs interact, the bound rises to 930 ns. If a tenth do, to 2.3 µs.
2. **The work per pair is tiny or not really per pair.** Some work that looks per pair can be done once per player and shared. Week 4's relevancy step, for example, can build one list per spatial cell instead of testing every pair.
3. **The work is spread over more than one core, or the core is faster.** The model assumes one core does all of it. If the node splits the work over `k` cores, the bound grows by up to `k`. CCP's battle report says the system had been moved in advance to one of its most powerful nodes and still reached the 10% floor, so better hardware helped but did not remove the dilation.
4. **The server did not keep up.** If ticks ran late or players' commands waited in a queue, the headline is true but the simulation was degraded beyond the time dilation. Player reports from the battle are evidence here.

Your presentation's job is to take this list to the sources. Which hypotheses do the developer's own blogs support? Which does the player community report? Which remain open? A teardown that ends with "hypotheses 1 and 3 are supported by the developer's posts, and 4 is contradicted by nobody" is a strong result. You did not need the source code to get there.

### Bracket every assumption

Every number in the model came with an assumption. Move each one across a range you can defend, and watch whether the conclusion moves.

| Assumption changed | Implied `c_i` for FWST-8 at 10% | Conclusion still holds? |
|---|---|---|
| None (`β = 1`, `g = 1`) | 233 ns | Tight: about two memory fetches |
| Keep half the tick free, `β = 0.5` | 116 ns | Tighter |
| A quarter of pairs interact, `g = 0.25` | 930 ns | Looser, still under 1 µs |
| A tenth of pairs interact, `g = 0.1` | 2,326 ns | Comfortable |
| Full speed, `d = 1` | 23 ns | Impossible |

The table tells you which assumption the conclusion depends on. It is `g`, the pair share, and the game speed `d`. The usable share `β` matters less, but only because its defensible range is narrow. A server that keeps between none and half of its tick free moves the bound by at most a factor of two, from 233 to 116 ns. Push `β` down to 0.1 and it moves the bound tenfold, as much as the game speed does, but no one runs a server at 10% of its tick. The pair share can plausibly sit anywhere from 1 to below 0.1, a spread of ten or more, and the game speed is fixed by the headline. So in your presentation, spend your research time on the pair share, not on the budget. This is called a **sensitivity check**, and it is what lets an audience trust a number built on assumptions.

### Move it yourself

Open `examples/w14-implied-cost-ladder.html`. The left view is a vertical ladder on a logarithmic scale from 1 ns to 100 µs. Fixed rungs mark Norvig's reference costs: one instruction, a mutex lock and unlock, one main-memory fetch. A marker for each case sits at its implied `c_i`. The right view shows one case at a time, with the pair count as a square of `n × n` cells shaded by the pair share `g`, and the budget as a bar. Select FWST-8 and drag the game speed from 10% to 100%. The marker falls through the main-memory rung and past the mutex rung toward the single-instruction rung. Then drag the pair share from 1 down to 0.1 and watch it climb back above 1 µs. The left view shows whether a headline is plausible. The right view shows which assumption decides it.

### Same idea elsewhere

The method works on any headline that gives you a player count and a time budget. Only the dominant term changes.

**VALORANT (Riot Games, August 2020).** Ten players per game, 128 ticks per second and a published target of 2.34 ms per frame, so that three games share one core. Here the pairs are few (90 ordered pairs), so the per-player term dominates. Invert it instead, `c_p ≤ budget / n`, and you get at most 234 µs per player per tick. Riot's first build took about 50 ms per frame, so the target required a speed-up of `50 / 2.34 = 21` times. The headline "128-tick for everyone" implies a 21× optimization project, and Riot's post describes exactly that.

**Second Life (Linden Lab, current).** A full region holds up to 100 avatars and the region simulator is capped at 45 frames per second. At full speed that gives 22.2 ms per frame and an implied pair cost of at most 2.2 µs, even if every avatar interacts with every other. That is roomy compared with EVE. The small cap on avatars, not a clever pair algorithm, is what keeps a region inside its frame. Week 1 made the same point from the other direction.

**Week 13's cost model.** The same inversion works on money. If a studio says its hosting costs a certain amount per player per month, divide by 730 hours and by the bytes a client of that genre needs, and you get the egress price it must be paying or the byte rate it must be sending. When the implied price is below any price a cloud provider lists, the studio owns hardware or has a special contract, as Roblox described in its 2022 postmortem.

Three systems, one move. Write the model, put the published numbers in, solve for the number nobody published, and compare it with something physical.

### Design judgment for analysts

- **Bound, don't guess.** An upper bound built on generous assumptions is stronger than a best guess, because it survives criticism. Say "at most 233 ns", not "about 200 ns".
- **Name the assumption the result depends on.** Run the sensitivity check and tell the audience which assumption carries the conclusion. If you cannot defend its range, say so.
- **An impossible bound is the best result.** When the numbers do not fit, something in the system is doing what your model does not. That gap is the most interesting part of your talk.
- **Do not present a bound as a measurement.** "The server spent 233 ns per pair" is false. "The server could not have spent more than 233 ns per pair, unless one of these four things was true" is the finding.

## 3. Structure of the presentation

You have 12 minutes and 5 minutes of questions. Use this structure. Each part names the kind of claim it contains, so the audience always knows whether it is hearing a fact, a result or an opinion.

| Part | Minutes | Content | Kind of claim |
|---|---|---|---|
| 1. The headline | 1 | The public fact, with its source, game version or date | Sourced fact |
| 2. The system | 2 | What the game does, in the terms of this course: zones, ticks, AOI, replication | Sourced fact |
| 3. The model | 2 | Which of the course's models applies, and which term dominates | Model |
| 4. The implied constant | 3 | The inversion, the comparison with hardware costs and the sensitivity table | Model result |
| 5. What must be true | 2 | Your hypotheses, each marked supported, contradicted or open, with the evidence | Evidence and judgment |
| 6. What players paid, and what you would do | 2 | The lever the developer pulled, its player price, and your alternative | Judgment |

Two rules for the slides. Every number on a slide carries its source and era in small text under it, such as "EVE Online, October 2020, CCP battle report" or "model, this talk". And every computed number shows the one-line formula that produced it, so a listener can check it with a phone calculator during your talk.

### Choosing the case

The instructor's list draws on systems this course has already met: EVE's time dilation and record battles, World of Warcraft Classic's layering, Second Life's region grid, VALORANT's server density, Roblox's infrastructure choices and others. A good case has at least one hard number (a player count, a tick rate, a cap or a price), a primary source from the developer, and something surprising about it. If your case has no hard number, you cannot invert a model, and your talk will turn into a summary. Pick another.

## 4. Sources and evidence

Your conclusions are only as strong as the numbers you put into the model. Grade every source before you use it.

- **Primary sources** come from the developer: dev blogs, patch notes, postmortems, conference talks, official documentation. They are the best evidence for what the system does, and the weakest for how well it worked, because developers rarely publish their failures in full.
- **Maintained community references** such as the EVE University wiki, Wowpedia or the Second Life wiki. Good for mechanics and numbers that players can observe and check. Always note the page's era, because mechanics change between patches.
- **Press and encyclopedias** such as news coverage and Wikipedia. Useful for dates and event records. Follow their citations back to a primary source when you can.
- **Player reports** such as forum threads and videos. Weak evidence for any single claim, but useful for the question "did the server keep up?" when many independent reports agree.

Three habits keep a teardown honest. State the version or era of every mechanic. Separate what the game shows (a tooltip, a counter) from what the game computes. And never invent a quote. Paraphrase the source, and quote at most one short phrase from it.

## 5. Asking and answering questions

The question period is where the method gets tested. As a listener, aim your questions at the joints of the argument.

- "Which assumption does your conclusion depend on, and what range did you check?"
- "Is that number the developer's, or yours?"
- "If your bound is right, what would you expect to see in the player reports, and did you see it?"
- "What would change your mind?"

As a presenter, answer with the kind of claim the question asks about. If someone challenges a number, say where it came from and what era it describes. If someone challenges a conclusion, go back to the sensitivity table. It is fine to say "that range is outside what we checked, and here is how the bound would move". It is not fine to defend a guess as a fact.

## In-class activity (30 minutes)

In your presentation groups, run a dry run of parts 1 to 4 with the case you chose.

1. Write your headline on one line with its source and era. (3 min)
2. Choose the model and the dominant term. Write the inversion for your case with symbols. (7 min)
3. Compute the implied constant with `implied_pair_ns` or its per-player version, and place it on the ladder in the interactive. (7 min)
4. Build a sensitivity table with at least three assumptions. Mark which one the conclusion depends on. (8 min)
5. Swap with another group. Each group asks the other two questions from section 5 and writes down the answers. (5 min)

Expected output: one headline line, one formula, one implied constant with units, a three-row sensitivity table and two peer questions with the answers you got.

## Common misconceptions

- **"The implied constant is what the server spent."** It is an upper bound under generous assumptions. The true value is smaller, often by a factor of two or more, as the week 1 control row showed.
- **"If the bound looks impossible, the headline must be false."** Usually a modelling assumption is wrong instead, most often the pair share. Finding which one is the result.
- **"More players, proportionally more work."** Pair work grows with the square. 2.46 times as many pilots meant 6.03 times as many pairs between B-R5RB and FWST-8.
- **"A case study is a summary of the developer's blog."** A summary repeats the source. A teardown computes something the source did not publish and tests it against the evidence.

## Check yourself

1. A claim says a 20 Hz zone server holds 1,000 players in one crowd at full speed. What is the implied pair cost at most, with `β = 1` and `g = 1`? Place it against the reference costs.
2. For the claim in question 1, the developer later says the server keeps 40% of the tick free and only a fifth of pairs interact. What is the new bound?
3. A game runs 12 players per match at 64 ticks per second, and the studio says it fits four matches per core. What is the most CPU time per player per tick, if the whole frame is usable?
4. Time dilation drops from 100% to 25% speed. By what factor does the implied pair cost bound change? By what factor could the player count grow at the same pair cost?

<details>
<summary>Answers</summary>

1. Budget `1 / 20 = 50 ms = 5 × 10⁷ ns`. Pairs `1,000 × 999 = 999,000`. Bound `5 × 10⁷ / 999,000 ≈ 50 ns`, between a mutex lock and unlock (25 ns) and a main-memory fetch (100 ns). Tight enough to doubt.
2. `β = 0.6` and `g = 0.2`: `0.6 / 0.2 = 3` times the earlier bound, about 150 ns. Still under two memory fetches.
3. A frame at 64 Hz lasts 15.625 ms. Four matches per core leave `15.625 / 4 = 3.906` ms per match frame. Divided by 12 players, at most 326 µs per player per tick.
4. The budget grows by `1 / 0.25 = 4`, so the bound grows 4 times. At the same pair cost, the pair count may grow 4 times, so the player count may grow about `√4 = 2` times.

</details>

## Lab / assignment hook

[Lab 14, case study teardown](../labs/lab14.md). You implement the inversion for pairs and for players, bracket it with a sensitivity sweep, and deliver your group's 12-minute presentation with a one-page handout of sources and formulas. The final demo in week 15 is assessed separately.

## Sources

- Wikipedia, "Bloodbath of B-R5RB" (battle of 27 to 28 January 2014, article as of 2026). 2,670 players in the system at peak, about 21 hours, time dilation at 10% speed.
- Wakeham, L. "EVE Online's record-breaking Fury at FWST-8" (Guinness World Records news, 29 October 2020). Battle of 6 October 2020; 8,825 players overall and 6,557 concurrent at the peak; records for the largest multiplayer videogame PvP battle and the most concurrent participants in one.
- CCP Games. "Fury at FWST-8 Battle Report" (eveonline.com, December 2020). The same 8,825 and 6,557 figures, peak reached during a battle of about 12 hours; the system had been reinforced on one of CCP's most powerful nodes and still ran at maximum time dilation.
- EVE University Wiki, "Server tick" (current mechanics). EVE's server aims to run one tick per second (1 Hz), and a player can be dead for up to 10 seconds without knowing it under severe time dilation.
- EVE University Wiki, "Time dilation" (current mechanics). Floor of 10% speed, applied per node.
- EVE University Wiki, "Grid" (current mechanics). A grid is a cube of about 8,000 km in each direction from its centre; objects on another grid in the same system do not show on the overview.
- Randall, B. "VALORANT's 128-Tick Servers" (Riot Games technology blog, 31 August 2020). First build at about 50 ms per frame, target of three games per core, 2.34 ms per frame budget. Paraphrased.
- Second Life Wiki, "Region" (current). A full region holds up to 100 avatars.
- Second Life Wiki, "llGetRegionFPS" (current). Region frame rate capped at 45 frames per second.
- Roblox. "Roblox Return to Service 10/28-10/31 2021" (Roblox newsroom, January 2022). On-premises infrastructure chosen partly for cost.
- Norvig, P. "Teach Yourself Programming in Ten Years" (norvig.com). Approximate timings on a typical PC: 1 ns per typical instruction, 25 ns mutex lock and unlock, 100 ns main-memory fetch.

## Interactive spec: examples/w14-implied-cost-ladder.html

**The one insight:** a public headline (players, tick rate, game speed) pins down a hidden per-pair cost, and comparing it with physical costs shows at once whether the headline needs a special explanation. The game speed and the pair share decide the answer. The usable share moves it by at most a factor of two over its defensible range of 0.5 to 1, though the slider's full range of 0.1 to 1 shows a tenfold spread.

**Layout.** Two linked views side by side on desktop, stacked on mobile (ladder first).

- **Left, the ladder.** A vertical logarithmic axis from 1 ns to 100 µs (labels at 1, 10, 100 ns, 1, 10, 100 µs). Three fixed reference rungs as dashed horizontal lines with labels: "typical instruction 1 ns", "mutex lock/unlock 25 ns", "main-memory fetch 100 ns". One marker per case (five cases below) at its implied `c_i`, labelled with the case name and value. The selected case is drawn larger in blood colour; others in ink-soft. Markers above 100 µs clamp to the top with an arrow.
- **Right, the selected case.** A square grid representing the `n × n` ordered pairs (draw it as a fixed 20 × 20 cell square; the shaded share of cells equals `g`, moss). Beside it, a horizontal budget bar showing the real time per tick in ms (steel), labelled with `β / (f_t d)`. Under both, the formula line with the current numbers substituted, e.g. `c_i ≤ 1 × 10⁹ / (1 × 0.1 × 6557 × 6556 × 1) = 233 ns`.
- **Sensitivity strip** under the right view: for the selected case, three small read-outs showing the bound when each of `β`, `g`, `d` is set to its slider minimum and maximum, with the spread factor between the two and the largest spread highlighted while the others stay at their current values, so the student sees which assumption moves the result most.

**Controls.**
- Case selector (radio group): B-R5RB 2014 (n 2,670, 1 Hz, d 0.1), FWST-8 2020 (n 6,557, 1 Hz, d 0.1), Second Life region (n 100, 45 Hz, d 1), Week 1 zone (n 153, 10 Hz, d 1), Custom.
- Players `n`: number input 2 to 20,000 (editable in Custom; shows the case value otherwise).
- Tick rate `f_t`: number input 0.5 to 256 Hz (Custom only).
- Game speed `d`: slider 0.1 to 1, step 0.05 (applies to the selected case; defaults to the case value).
- Pair share `g`: slider 0.01 to 1, step 0.01, default 1.
- Usable share `β`: slider 0.1 to 1, step 0.05, default 1.
- Reset button.

**Formulas.** `budget_ns = 1e9 × β / (f_t × d)`. `pairs = n (n − 1) g`. `c_i_max = budget_ns / pairs`. Show `c_i_max` rounded to the nearest ns below 10 µs and to 0.1 µs above. Show pairs with thousands separators.

**Test values** (`β = 1`, `g = 1` unless stated). B-R5RB: 1,403 ns. FWST-8: pairs 42,987,692, 233 ns. FWST-8 with `d = 1`: 23 ns. FWST-8 with `g = 0.25`: 930 ns; `g = 0.1`: 2,326 ns (shown as 2.3 µs); `β = 0.5`: 116 ns. Second Life: budget 22.2 ms, 2,245 ns (2.2 µs). Week 1 zone: 4,300 ns (4.3 µs). Custom `n = 1000`, `f_t = 20`, `d = 1`: 50 ns.

**Accessibility.** All controls keyboard operable with visible focus. The ladder markers have text equivalents in a list under the chart. An `aria-live="polite"` region announces the selected case's bound when it changes. Respect `prefers-reduced-motion` (markers jump, no easing). Palette from `templates/interactive-tokens.css`, light and dark.
