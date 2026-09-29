# MMO306 · Week 09 — Procedural and Systemic Content

**Why this matters:** A generator can make more dungeons than any team could build, and players will still say "I've seen this one." The number that matters is how many outcomes a player can tell apart, not how many the generator can produce. That number is usually tiny, you can compute it before you ship, and it tells you how many runs a player gets before the content starts to repeat.

**You will be able to:**
- Compute a generator's perceived variety and effective variety from its salient features and their weights.
- Predict the chance that a player has met a repeat within `n` runs, and the run at which half of players have, with and without a memory rule.
- Compute the expected cost of generating valid content by rejection, and design a fallback.
- Critique a procedural or systemic content plan for an MMO: where it adds variety players notice, and where it breaks fairness, guides or shared experience.

**Before class:** Kate Compton, "So you want to build a generator" (2016 blog essay, about 20 minutes; read the part on the 10,000 bowls of oatmeal). Shaker, Togelius and Nelson, *Procedural Content Generation in Games* (Springer, 2016), chapter 1.

**Prerequisites from earlier courses:** [MA102 week 9, weighted tables](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md) (weights to probabilities). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). [MMO301 week 10, immersion, identity and the avatar](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w10-immersion-identity-and-the-avatar.md) (the birthday model, `M_eff = 1 / Σp²` and `n_50` for character looks; this week applies the same model to generated content and does not re-derive it). [GD102 week 12, emergent behavior from simple rules](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md) (a cave generator from a cellular automaton). [GD202 week 9, emergent narrative](../../GD202-narrative-and-quest-design/lectures/w09-emergent-narrative.md). [GD201 week 9, POI density](../../GD201-level-and-world-design/lectures/w09-open-world-structure-poi-density.md). From this course, [week 1](w01-the-content-treadmill-production-vs-consumption.md) (the replay multiplier) and [week 8](w08-repeatable-content-dailies-dungeons-rotations.md) (rotation exposure).

**Interactive:** [`examples/w09-oatmeal-meter.html`](../examples/w09-oatmeal-meter.html). Keep it open during section 2.

---

## 1. Two ways to make content without authoring each piece

Week 1 showed that authored content runs out on a calendar you can't beat by hiring. Two families of techniques make play without authoring every piece.

**Procedural content generation (PCG)** is an algorithm that assembles content from parts and rules. A dungeon generator picks a layout template, fills rooms with enemy groups, places a boss and applies a modifier. A **seed** is the number that starts the generator's random choices. The same seed always gives the same output, which matters in an MMO because every player in a group must see the same dungeon and because a bug report is useless if nobody can reproduce the layout.

**Systemic content** is play that arises from systems interacting, not from a generated artifact. Faction armies that push a front line back and forth, predators that move when prey runs out, a market that makes a resource worth gathering this week: none of these is a level. They are states of a simulation that a player experiences as "something is happening here." GD102 week 12 showed how simple local rules produce patterns no rule mentions, and GD202 week 9 showed how systems produce stories.

Many shipped systems mix the two. The Elder Scrolls V: Skyrim's Radiant quest system builds quests from components such as a location, an enemy type and a reward. Some are randomized each time the quest starts, and the system tries to send you to places you haven't discovered yet.

Both families share one risk, and this lecture is about measuring it. A generator can produce a vast number of outputs that a player experiences as a handful.

## 2. Worked example: the oatmeal meter

### The hook

No Man's Sky has more than 18 quintillion possible planet seeds. The exact figure is 18,446,744,073,709,551,616, which is `2^64`, the largest count a 64-bit number can index. Each seed is a different planet.

In 2016, the procedural generation researcher Kate Compton named the problem with numbers like that. You can generate 10,000 bowls of plain oatmeal with every oat in a different place, and each bowl will be mathematically unique. The player will see a lot of oatmeal. Her essay uses the 18 quintillion planets as its example and argues that **perceptual uniqueness** is the metric that counts.

The game itself hints at how players perceive its planets. When you scan a planet from orbit, it is named by its biome: lush, barren, frozen, toxic, and a short list of others. Eighteen quintillion seeds, described to the player by one word from a short list.

### The model

Describe each generated output by its **signature**: the tuple of features a player actually notices and remembers. For a dungeon, maybe layout, boss and modifier. Leave out everything the player can't tell apart, such as exact room positions or the rotation of a rock. The signature is the design decision in this model. The arithmetic after it is borrowed.

[MMO301 week 10](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w10-immersion-identity-and-the-avatar.md#the-model) derived that arithmetic for avatar twins in a crowd. Go there for the derivation. The recap, with a signature axis in place of a creator category:

```
M     = v_1 × v_2 × ... × v_k                        perceived variety
M_eff = Π_i 1 / (p_i1² + p_i2² + ...)                effective variety
P(n)  ≈ 1 − exp(−n (n − 1) / (2 × M_eff))            chance of a repeat within n runs
n_50  ≈ 0.5 + √(0.25 + 2 ln 2 × M_eff) ≈ 1.18 √M_eff
```

Every symbol:

- `k`, the number of salient axes. `v_i`, the values on axis `i` a player can tell apart.
- `p_ij`, the probability the generator picks value `j` on axis `i`. Even weights give `M_eff = M`, and skew lowers it.
- `n`, the number of runs one player has done. `n_50`, the run by which half of players have met a repeat.

Two things change when the crowd becomes one player's run history.

**The crowd is spread over time.** In MMO301 the `n` avatars stood in one city square. Here the `n` runs belong to one player, so `n_50` divided by runs per day is a date: the day half your players first say "I've seen this one." That turns the model into a production number you can put in a plan.

**A generator can remember.** A crowd can't refuse a duplicate face, but a generator can refuse a recent signature. Call the rule "not one of the last `k`." Run `n` can then only repeat one of the `n − 1 − k` older runs, so the pairs that count shrink from `n(n − 1)/2` to about `(n − k)(n − k − 1)/2`, and

```
n_50 with a memory of k  ≈  n_50 + k
```

- `k`, the number of recent signatures the generator refuses to repeat.

The two levers grow differently, and that is the lesson of this week in two lines. **Variety buys runs with a square root: to double the runs before a repeat, you need four times `M_eff`. Memory buys runs one for one.** The raw number of seeds appears in neither.

### Numbers you can check

Start small. Skyrim's Radiant quest "Bounty: Giant" can send you to any of 12 giant camps. Suppose the camp were drawn uniformly each time. With `M = 12` the exact chance of no repeat in `n` quests is `(12 × 11 × ... × (12 − n + 1)) / 12^n`:

| Bounties taken `n` | P(some camp visited twice) |
|---|---|
| 2 | 8.3% |
| 3 | 23.6% |
| 4 | 42.7% |
| 5 | 61.8% |
| 6 | 77.7% |

Check `n = 5`: `12 × 11 × 10 × 9 × 8 = 95,040` and `12^5 = 248,832`, so no repeat has probability 0.382 and a repeat 0.618. By your fifth giant bounty, the odds favor a return trip. The UESP wiki notes that Skyrim's system tries to send you somewhere you haven't discovered, which pushes the real chance down. That preference is a design response to exactly this curve.

Now a generator at MMO scale. An invented dungeon generator has 6 layout templates, 4 bosses and 5 modifiers, plus a 32-bit seed that shuffles decoration and exact enemy positions. The layouts and bosses are picked evenly. The modifiers are weighted 4 : 3 : 1 : 1 : 1.

- Raw outputs: `6 × 4 × 5 × 2^32 ≈ 5.2 × 10^11`.
- Perceived variety: `M = 6 × 4 × 5 = 120`. The decoration seed adds nothing a player remembers.
- Modifier probabilities 0.4, 0.3, 0.1, 0.1, 0.1. Sum of squares `0.16 + 0.09 + 0.01 + 0.01 + 0.01 = 0.28`, so `M_eff,modifier = 1 / 0.28 ≈ 3.57`.
- Effective variety: `M_eff = 6 × 4 × 3.57 ≈ 85.7`.

| Runs `n` | P(repeat), even weights (`M = 120`, exact) | P(repeat), skewed modifiers (`M_eff = 85.7`, approximation) |
|---|---|---|
| 5 | 8.1% | 11.0% |
| 10 | 32.0% | 40.8% |
| 15 | 59.8% | 70.6% |
| 20 | 81.3% | 89.1% |
| Median first repeat | run 14 | run 12 |

Half a trillion outputs, and half of players meet a dungeon they have already seen by their twelfth run. At three runs a day, that is day four. The skewed modifier weights alone cost about two runs.

The same numbers from code, with a Monte Carlo check of the median and of the memory rule:

```python
import math
import random

def effective_variety(weights):
    """1 / (sum of squared probabilities): how many equally likely outcomes this axis is worth."""
    total = sum(weights)
    return 1 / sum((w / total) ** 2 for w in weights)

def p_repeat(n, m_eff):
    """Chance that some two of n runs share a signature (approximation)."""
    return 1 - math.exp(-n * (n - 1) / (2 * m_eff))

axes = {"layout": [1] * 6, "boss": [1] * 4, "modifier": [4, 3, 1, 1, 1]}
m_eff = math.prod(effective_variety(w) for w in axes.values())
print(f"effective variety: {m_eff:.1f}")
for n in (5, 10, 15, 20):
    print(f"  P(repeat within {n} runs) = {p_repeat(n, m_eff):.3f}")

rng = random.Random(9)

def draw():
    return tuple(rng.choices(range(len(w)), weights=w)[0] for w in axes.values())

def first_repeat(k=0):
    """Run number of a player's first repeat. With k > 0, never repeat one of the last k signatures."""
    history = []
    while True:
        sig = draw()
        while k and sig in history[-k:]:
            sig = draw()
        if sig in history:
            return len(history) + 1
        history.append(sig)

for k in (0, 3, 10):
    runs = sorted(first_repeat(k) for _ in range(20000))
    print(f"memory k = {k:>2}: simulated median run of first repeat = {runs[len(runs) // 2]}")
```

Output:

```
effective variety: 85.7
  P(repeat within 5 runs) = 0.110
  P(repeat within 10 runs) = 0.408
  P(repeat within 15 runs) = 0.706
  P(repeat within 20 runs) = 0.891
memory k =  0: simulated median run of first repeat = 12
memory k =  3: simulated median run of first repeat = 14
memory k = 10: simulated median run of first repeat = 21
```

The simulation agrees with `n_50 + k`. The formula gives 11.4, 14.4 and 21.4, and the simulated medians are 12, 14 and 21. The memory rule redraws a few signatures, which nudges the weights, so the match is close but not exact.

### What moves the number

Use the formula to rank design changes by what they buy.

| Change | New `M_eff` | Median first repeat |
|---|---|---|
| Baseline (skewed modifiers) | 85.7 | run 12 |
| Flatten modifier weights to even | 120 | run 14 |
| Add 2 layouts (8 in all) | 114.3 | run 14 |
| Add a noticeable axis: 4 weather states, even | 342.9 | run 23 |
| Add 2^32 more decoration seeds | 85.7 | run 12 |
| Memory rule: not one of the last 3 | 85.7 | run 14 |
| Memory rule: not one of the last 10 | 85.7 | run 21 |

The cheapest change on this list is flattening weights, which is a number in a data file. The most effective is a new axis the player notices, because it multiplies. Two new layouts, which may be the most expensive item in art time, buy the same two runs. More seeds buy nothing. A memory of 10 matches the weather axis and costs no content, but the design judgment below says what it costs players.

### A visual you can move

Open the interactive. The left panel compares three bars on a logarithmic scale: raw outputs, perceived variety `M` and effective variety `M_eff`. The raw bar towers over the others. The right panel plots `P(repeat within n runs)` against runs, with a marker at `n_50` and a vertical band for "runs per week" that you set.

Drag the decoration-seed slider from 0 to 32 bits. The raw bar shoots up by nine orders of magnitude. The curve on the right doesn't move at all. Now drag the modifier skew toward even: the curve shifts right by two runs. Finally add a new salient axis with four values. The curve stretches right and `n_50` nearly doubles. Last, set the memory rule to "not the last 3." A second, simulated curve appears, shifted right by about three runs, while every bar on the left stays put. The picture makes the oatmeal problem literal: the tallest bar is the one that does nothing, and the one lever that moves the curve without touching variety is memory.

### Cross-game recognition

**The Elder Scrolls V: Skyrim (2011), Radiant quests.** Each Radiant quest has a list of possible locations, often about a dozen, and some have more than 140. A 12-camp bounty is `M = 12`, `n_50 ≈ 4.6`. A quest that can use any of 140-plus dungeons with a boss chest has `M > 140`, so `n_50 > 14`. The preference for undiscovered locations works like a memory rule that forbids repeats while new places remain, which delays the first repeat until the list is exhausted.

**World of Warcraft, Island Expeditions (Battle for Azeroth era).** Each island had four possible starting points, and the enemy forces on an island were randomized, so a player might meet one invading faction on one visit and a different one the next. A developer interview at the time suggested about a thousand possible scenarios. Rewrite that in this model's terms. The signature a player notices is roughly island × invading force × starting point. But only 3 islands were available each week (week 8), so the variety a player could meet within one week was the weekly slice: `3 × 4 × (number of invading forces)`. Rotations and generators multiply, and a weekly rotation divides the generator's variety by the share of the pool on offer.

**No Man's Sky (2016 to present).** `2^64` seeds, but one biome label per planet on the orbital scan. If a player's memory of a planet is roughly biome × a few other salient features (weather severity, water or no water, notable creatures), `M_eff` might be in the hundreds or low thousands. That is still a large number: with `M_eff = 1,000`, `n_50 ≈ 38` planets. The point is not that the game fails. It is that its variety budget lives in a few salient axes, and the seed count only guarantees those axes get mixed.

Three games, three scales, one formula. When someone quotes a generator's output count, ask what the signature is and compute `M_eff`.

### Eyes-open design judgment

- **Spend on axes players notice.** Before building a generator, list the features players will talk about ("the ice one with the spider boss"). Those are the signature. Every other axis is decoration: good for texture, worthless for variety.
- **Weights are variety.** Designers skew weights to make a favorite outcome common. That costs `M_eff`, and the formula prices it exactly.
- **Use memory rules deliberately.** "Not one of the last three" guarantees at least four runs without a repeat and costs nothing to build. It adds runs, not variety. As `k` approaches `M_eff` the generator turns into a shuffled deck, a player who tracks recent runs can rule outcomes out, and that predictability is fine for flavor and bad for anything competitive. Memory is also per player or per group, so a group of five whose members have different histories needs a rule for whose history counts.
- **Some content should not be generated.** Content with leaderboards is compared across players, and a generated layout makes one run easier than another. World of Warcraft's Mythic+ system runs hand-built dungeons and varies them with weekly-rotating affixes, so every group in a given week faces the same dungeon at the same keystone level. Content that players learn from guides, or coordinate as a group of 20, also depends on being the same every time.
- **Generated variety still wears out.** Players remember signatures, and a generator with `M_eff = 86` behaves like a rotation pool of 86. Week 8's exposure math applies. Plan for the day your most active players have seen most of it.

## 3. Valid by construction or valid by rejection

A generator's output must be playable: every room reachable, the boss beatable, the difficulty inside the band you promised. There are two ways to guarantee it.

**Valid by construction.** Build the generator so it can only produce valid output. A layout grammar that always connects the entrance to the boss room, for example. This is the safer choice, but it restricts what the generator can make.

**Valid by rejection.** Generate freely, test the output against your constraints, and throw it away if it fails. If a fraction `v` of raw outputs pass, the number of attempts until one passes follows the geometric distribution from [MA102 week 7](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md):

```
expected attempts          = 1 / v
P(more than k attempts)    = (1 − v)^k
```

With `v = 0.2`, the average is 5 attempts. The chance of needing more than 20 is `0.8^20 ≈ 1.2%`. If generation happens on the server while a group waits in a loading screen, that 1.2% tail is a real delay for real players. Two responses:

- **Cap the attempts and fall back.** After 20 failures, use a hand-authored layout. Players never see the tail.
- **Pre-generate.** Generate and validate seeds offline, and serve only seeds from a vetted list. Your perceived variety is then the list's variety, which you can measure directly.

Rejection has a subtler cost. The constraints filter the distribution. If layouts with long corridors fail the difficulty check more often, the surviving layouts under-represent them, and your weights no longer mean what the data file says. Measure `M_eff` on the accepted outputs, not on the generator's inputs.

### Difficulty spread

Validity is not only pass or fail. Two valid generated dungeons can differ in difficulty. If a generated dungeon's clear time varies by 30% between seeds, some players get an easier reward than others. Treat difficulty as a constraint with a band ("clear time for a reference group within ±10% of 20 minutes") and reject outside it. Week 7's logs are how you check the band after launch: group clear times by seed and look for seeds that are outliers.

## 4. Systemic content: variety from state

Systemic content produces variety differently. There is no generator to call. The world's state changes because systems act on one another, and players meet whatever state the world is in.

The oatmeal meter still applies, with one change. The signature is the set of state features a player notices when they arrive. "The northern fort is held by the enemy and the mine is overrun" is a signature. If your faction system has 3 forts that can each be held by 2 sides, and 2 mines that can each be overrun or not, the perceived variety of the region is at most `2^3 × 2^2 = 32`. In practice it is much smaller, because systems settle into a few common states. A faction war that almost always ends with the stronger side holding all three forts has `M_eff` close to 1.

That tendency to settle is the main design problem of systemic content. [GD102 week 4](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) called the fix a negative feedback loop: make the winning side's advantages shrink as it wins, so the state keeps moving. Week 11 of this course covers the scheduled version of this, events and world bosses, where the designer chooses the timing instead of letting systems drift.

Three rules for systemic content in an MMO:

- **Bound every stock.** A system with an unbounded quantity (a population, a resource, a faction's strength) will eventually hit a state you never tested. Set floors and ceilings (GD102 week 2).
- **Log the state, not only the player.** You can't tune a system whose history you didn't record. Record state changes as events, as week 7 did for combat.
- **Give players a lever.** Systemic content feels like content when players can push it. A front line that moves only on a timer is a rotation with extra steps.

## 5. Using procedural content responsibly

The outcome for this course says "use procedural and repeatable content responsibly." The model gives that word concrete meaning.

- **Don't claim variety you haven't measured.** "Infinite dungeons" in a patch note, for a generator with `M_eff = 86`, sets an expectation that players will test within a week.
- **Don't generate to pad hours.** A generator raises week 1's replay multiplier `r` only while its outputs still feel new. Past `n_50`, extra runs are the same content with a different seed, and players who need a reward from it are grinding.
- **Keep seeds on the server.** If the client can predict a seed, players can predict the dungeon, the loot or the modifier, and choose only the good ones. That turns variety into an exploit.
- **Keep generation reproducible.** Store the seed and generator version with every instance, so a bug report can be replayed exactly and a later generator change doesn't silently alter old content.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive.

1. Your team's dungeon generator has 5 layouts (weighted 3 : 3 : 2 : 1 : 1), 3 bosses (even) and 4 modifiers (even), plus a large decoration seed. Compute `M`, `M_eff` and `n_50`.
2. Players run it 4 times a day. Your target is that half of players meet their first repeat no sooner than day 7. What `M_eff` do you need? Propose the cheapest set of changes that reaches it, using only (a) flattening weights, (b) adding values to an axis, (c) adding a new axis. Show the new `n_50`.
3. The generator uses rejection with `v = 0.25`. What is the chance a group waits more than 10 attempts? Design a fallback.
4. Name one piece of your dungeon that should stay hand-authored, and say why in one sentence.

Expected output: three numbers for step 1, a change list with its `n_50`, a probability and a fallback rule, and one sentence.

## Common misconceptions

- **"More seeds means more variety."** Seeds only index outputs. Variety is what a player can tell apart, and it lives in a handful of salient axes.
- **"Half the variety means half the runs before a repeat."** Runs before a repeat scale with the square root of `M_eff`. Halving variety cuts `n_50` by about 30%, and quadrupling it only doubles `n_50`.
- **"Weights don't affect variety, they only affect which outcome is common."** Skewed weights lower `M_eff`. A 4 : 3 : 1 : 1 : 1 axis of five values is worth about 3.6.
- **"A memory rule adds variety."** It adds runs before a repeat, about one per remembered signature, and leaves `M_eff` unchanged. Once a player has seen most of the signatures, memory has nothing left to hold back.
- **"Rejection sampling is free because failed outputs are discarded."** Each failure costs time, the tail can be long, and the surviving outputs follow a different distribution from the generator's inputs.

## Check yourself

1. A quest generator has 8 locations, 3 enemy types and 2 reward types, all even. Compute `M` and `n_50`. What is the exact chance that a player's first 3 quests include a repeat?
2. An axis has four values weighted 7 : 1 : 1 : 1. What is its effective variety? How many even values is it equivalent to?
3. A designer adds a salient axis with 3 even values to a generator with `M_eff = 50`. By what factor does `n_50` grow?
4. A weekly rotation offers 3 of 11 islands, and each island has 4 starting points and 5 possible invading forces, all even. What is the perceived variety available in one week? After how many runs in one week does half the player base meet a repeat?
5. A generator's outputs pass validation 40% of the time. What is the expected number of attempts, and the chance of needing more than 8?
6. A generator has `M_eff = 50` and a target of 15 runs before half of players meet a repeat. Compare adding a memory of `k` with adding variety: what `k` meets the target, and what `M_eff` would meet it with no memory?

<details>
<summary>Answers</summary>

1. `M = 8 × 3 × 2 = 48`. `n_50 ≈ 0.5 + √(0.25 + 1.386 × 48) = 0.5 + √66.8 ≈ 8.7`, so by the ninth quest. Exact for 3 quests: `1 − (48 × 47 × 46) / 48^3 = 1 − 103,776 / 110,592 = 6.2%`.
2. Probabilities 0.7, 0.1, 0.1, 0.1. Sum of squares `0.49 + 0.03 = 0.52`. `M_eff = 1 / 0.52 ≈ 1.92`, about as varied as two even values.
3. `M_eff` becomes 150, three times larger, so `n_50` grows by about `√3 ≈ 1.73`. (From about 8.8 to about 14.9 runs.)
4. `3 × 4 × 5 = 60`. `n_50 ≈ 0.5 + √(0.25 + 1.386 × 60) ≈ 0.5 + 9.13 ≈ 9.6`, so about 10 runs within the week.
5. `1 / 0.4 = 2.5` attempts on average. `P(more than 8) = 0.6^8 ≈ 1.7%`.
6. `n_50 ≈ 0.5 + √(0.25 + 1.386 × 50) ≈ 8.8`, so a memory of `k = 7` gives about 15.8. With no memory, `n_50 = 15` needs `(15 − 0.5)² − 0.25 = 1.386 × M_eff`, so `M_eff ≈ 151.5`, three times the variety.

</details>

## Lab / assignment hook

[Lab 09, measuring a generator](../labs/lab09.md). You write the signature, effective-variety and repeat-probability functions for an invented dungeon generator, check them against a Monte Carlo simulation of first repeats, add a memory rule and a rejection step, and redesign the generator to meet a first-repeat target at the lowest authoring cost. The final dungeon (60%) may use generated elements only with a stated `M_eff` and `n_50`.

## Sources

- Compton, K. (2016). "So you want to build a generator." Blog essay, galaxykate0.tumblr.com (archived August 2026). The 10,000 bowls of oatmeal problem, the 18,446,744,073,709,551,616 planets example, perceptual uniqueness versus perceptual differentiation. https://galaxykate0.tumblr.com/post/139774965871/so-you-want-to-build-a-generator
- No Man's Sky Wiki, "Planet" and "Galaxy" (current version). More than 18 quintillion possible planet seeds (18,446,744,073,709,551,616, the maximum of a 64-bit unsigned integer). https://nomanssky.fandom.com/wiki/Planet
- No Man's Sky Wiki, "Biome" (current version, Voyagers). The biome description appears before "planet" or "moon" on a starship scan; each planet has a single biome. https://nomanssky.fandom.com/wiki/Biome
- UESP, "Skyrim:Radiant" (The Elder Scrolls V: Skyrim, 2011). Radiant quests built from components such as location, enemy type and reward; preference for undiscovered locations; Bounty: Giant uses all 12 giant camps; some quests use 140+ dungeons. https://en.uesp.net/wiki/Skyrim:Radiant
- Warcraft Wiki, "Island Expedition" (Battle for Azeroth, patches 8.0 to 8.2). Four possible starting points per island; randomized enemies per visit; about a thousand possible scenarios per a developer interview reported by MMO-Champion; 11 islands in rotation with 3 available each week. https://warcraft.wiki.gg/wiki/Island_Expedition
- Warcraft Wiki, "Mythic+" (The War Within era). Five-player Mythic dungeons with weekly-rotating affixes and keystone scaling. https://warcraft.wiki.gg/wiki/Mythic%2B
- Shaker, N., Togelius, J. & Nelson, M. J. (2016). *Procedural Content Generation in Games*. Springer.

## Interactive spec: examples/w09-oatmeal-meter.html

**The one insight.** Raw output count does not change how soon players meet a repeat. Only salient axes and their weights do, and runs-to-repeat grow with the square root of effective variety.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.

- **Left panel, "How much variety?"** Three horizontal bars on a log10 scale from 1 to 10^15: "raw outputs" (`M × 2^b`, where `b` is decoration seed bits), "perceived variety M" and "effective variety M_eff". Bars in `--ink-soft`, `--steel`, `--ochre`. Exact values printed at the end of each bar (raw in scientific notation, the others to one decimal).
- **Right panel, "Chance a player has met a repeat."** x-axis: runs `n` from 1 to 60. y-axis: 0% to 100%. Curve `P(n) = 1 − exp(−n(n−1)/(2 M_eff))` in `--ochre`. A dashed horizontal line at 50% and a dot where the curve crosses it, labeled "n₅₀ ≈ X runs". A shaded vertical band from 0 to "runs per week" (control) labeled "one week of play". If memory rule "not one of the last k" is on, overlay the simulated curve (see below) in `--moss`.

**Controls.**

- Three axes, each with a "values" stepper (1 to 12) and a "skew" slider (0 to 1). Weights for an axis with `v` values and skew `s`: `w_j = (1 − s) + s × v × [j == 1]`, normalized; `s = 0` is even. Defaults: layout 6 values, skew 0; boss 4 values, skew 0; modifier 5 values with the lecture weights 4 : 3 : 1 : 1 : 1 (implement as a preset button "lecture weights" that sets exact weights, and let the skew slider override).
- "Add a fourth axis" toggle with its own values stepper (default 4, even), labeled "weather".
- Decoration seed bits `b`: slider 0 to 32, default 32.
- Runs per week: slider 1 to 40, default 21.
- Memory rule: select "none" / "not the last 1" / "not the last 3". When on, run a seeded Monte Carlo of 5,000 players (signature drawn from the weighted axes, redrawn if it matches any of the last `k` signatures) and plot the empirical share with a repeat by each `n`. Show "simulated n₅₀".

**Formulas.** `M = Π v_i`. `M_eff = Π 1 / Σ_j p_ij²`. `P(n) ≈ 1 − exp(−n(n−1)/(2 M_eff))`. `n₅₀ = 0.5 + √(0.25 + 2 ln 2 × M_eff)`.

**Test values.**

| Setting | `M` | `M_eff` | `P(10)` | `P(20)` | `n₅₀` |
|---|---|---|---|---|---|
| Lecture defaults (6, 4, lecture weights) | 120 | 85.7 | 40.8% | 89.1% | 11.4 |
| Modifiers even | 120 | 120.0 | 31.3% | 79.5% | 13.4 |
| Layouts 8, lecture weights | 160 | 114.3 | 32.5% | 81.0% | 13.1 |
| Lecture defaults + weather 4 | 480 | 342.9 | 12.3% | 42.5% | 22.3 |
| Skyrim giant camps (one axis, 12 values, others 1) | 12 | 12.0 | 97.6% | 100.0% | 4.6 |

Memory rule, lecture defaults, simulated `n₅₀` (interpolated between runs, 5,000 players, so allow ±0.3): "not the last 1" about 12.2, "not the last 3" about 14.1. The formula readout stays at 11.4 because memory does not change `M_eff`.

Changing `b` from 0 to 32 changes only the raw bar (for the defaults, from 120 to about 5.2 × 10^11). The note under the left panel reads "raw outputs changed; n₅₀ did not" whenever `b` is the last control moved.

**First screen.** Lecture defaults, `b = 32`. The raw bar reaching 10^11 next to a short `M_eff` bar, and the right curve with "n₅₀ ≈ 11.4 runs" inside the "one week of play" band, visible without scrolling. Caption under the title: "The tallest bar does nothing. Find the one that does."

**Accessibility.** Keyboard-operable steppers and sliders with visible focus; numeric readouts in an `aria-live="polite"` region; the Monte Carlo runs in chunks so the page stays responsive; animation off under `prefers-reduced-motion`.
