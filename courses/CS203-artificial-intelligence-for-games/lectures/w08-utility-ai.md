# CS203 · Week 08 — Utility AI

**Why this matters:** A behavior tree always prefers its first branch. Real priorities slide. Drinking a potion should beat attacking at 15% health and lose at 60%, and where exactly it flips should depend on how close the enemy is to dying. Utility AI gives every action a score from 0 to 1 and picks the best one, so the priority moves with the situation. The designer's job moves too. You stop writing rules and start drawing curves, and the shape of each curve is the character's personality.

**You will be able to:**
- Compute an action's score from response curves and considerations, and pick the winning action for a given situation.
- Derive the switch point where two actions' scores cross, and predict how a curve's exponent or a second consideration moves it.
- Compare product, geometric-mean, weighted-random and bucketed selection, and name the failure each one prevents or causes.
- Design and tune a small utility NPC in Python so it switches actions at the health values a designer asks for, without dithering.

**Before class:** Graham, D. "Rez", "An Introduction to Utility Theory", *Game AI Pro* (2013), chapter 9 (free at gameaipro.com). Lewis, M., "Choosing Effective Utility-Based Considerations", *Game AI Pro 3* (2017), chapter 13, sections 13.1, 13.2 and 13.5 (free). Skim Dill, K., "Dual-Utility Reasoning", *Game AI Pro 2* (2015), chapter 3 (free, 6 pages).

**Prerequisites from earlier courses:** [CS203 week 7, behavior trees](w07-behavior-trees.md) (fixed priorities, and why they run out). [CS203 week 6, finite state machines](w06-finite-state-machines.md) (commitment and dithering; section 5 applies the same fix to scores). [MA101 week 3, polynomials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (what an exponent does to a curve's shape). [MA101 week 8, lerp, inverse lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (normalizing inputs to 0 to 1, and piecewise curves). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (solving for an exponent). [MA102 week 9, weighted tables](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md) (weighted random choice).

**Interactive:** [`examples/w08-utility-curves.html`](../examples/w08-utility-curves.html). Keep it open during section 2.

---

## 1. Scores instead of an order

A behavior tree answers "what should I do?" by asking yes-or-no questions in a fixed order. Utility AI asks every action the same question at once. How good would you be right now, from 0 to 1? Then it does the best one.

Four terms carry the whole idea.

- An **input** is a number the NPC can read, normalized to the range 0 to 1. Health as a fraction of maximum is already normalized. A distance needs "bookends", a minimum and a maximum, and the inverse lerp from MA101 week 8: `x = (d − d_min) / (d_max − d_min)`, clamped.
- A **response curve** turns an input into a score between 0 and 1. This is where the design lives. The same input, "my health", can feed a curve that rises early (a cautious NPC) or late (a brave one).
- A **consideration** is one input passed through one curve. An action usually has several. "Drink a potion" might consider my health, whether I have a potion, and how many enemies are near.
- An action's **score** combines its considerations, usually by multiplying them. The NPC picks the action with the highest score. Re-scoring every action on each decision is called a **think**.

The curves you will use most come from MA101.

| Curve | Formula (input `x` in 0 to 1) | Reads as |
|---|---|---|
| Linear | `x` | "matters in proportion" |
| Power | `x^k` | `k > 1`: "only matters when it is extreme"; `0 < k < 1`: "matters early" |
| Inverted | `1 − x`, or `(1 − x)^k` | the same, for inputs where low is urgent (health) |
| Logistic | `1 / (1 + e^(−s(x − m)))` | "a soft switch at `m`"; larger `s` is sharper |
| Piecewise linear | lerp between hand-placed points | "exactly the shape I drew" |

Why multiply? Because a product lets any one consideration veto the action. If you have no potion, the "have a potion" consideration is 0, and so is the whole score, however hurt you are. Multiplication also means every consideration matters. An action scores high only if all its considerations are high.

## 2. Worked example: when does the brute drink?

### The hook

In The Sims, a Sim who is a little hungry keeps watching TV. A Sim who is very hungry drops the remote and heads for the fridge. Nobody wrote the rule "at 40% hunger, stop watching TV". David Graham, writing in *Game AI Pro*, describes how The Sims scores its motives with hand-drawn piecewise curves, and why. A smooth formula would make a Sim occasionally eat when nearly full, or never notice hunger until too late. A drawn curve can ignore hunger for a while, then rise, then shoot up. The moment the Sim changes its mind is the point where two scores cross. Move the curve, and you move the moment.

That is the lesson in one sentence, and you can build it with two actions.

### The model

A melee brute has two actions. Write its health fraction as `h` and its enemy's health fraction as `e`, both from 0 to 1.

```
Attack(e)   = 0.6 + 0.3 × (1 − e)
Drink(h)    = [has a potion] × (1 − h)^k
choose the action with the larger score
```

- `Attack` has one consideration, the enemy's health through a linear curve. Against a fresh enemy (`e = 1`) it scores 0.6. Against an enemy on its last legs (`e = 0`) it scores 0.9. The brute gets greedier as the kill gets closer.
- `Drink` has two considerations. `[has a potion]` is 1 or 0, the veto. `(1 − h)^k` is urgency: 0 at full health, 1 at zero health.
- `k` is the designer's **panic knob**. At `k = 1` urgency grows steadily. At `k = 3` it stays low until health is very low, then climbs fast.

The brute switches from attacking to drinking where the two scores are equal. Solve `(1 − h)^k = A`, where `A` is the attack score:

```
h* = 1 − A^(1/k)
```

That single number, the **switch point**, is what players experience. Everything a designer tunes is really a way of moving it.

### The code

```python
def power(x, k):
    return max(0.0, min(1.0, x)) ** k

def attack_score(enemy_hp):          # 0.6 against a fresh enemy, 0.9 at a dying one
    return 0.6 + 0.3 * (1 - enemy_hp)

def drink_score(hp, k, potions=1):
    if potions == 0:
        return 0.0                   # a zero vetoes the action
    return power(1 - hp, k)

def choose(hp, enemy_hp, k=2):
    return "Drink" if drink_score(hp, k) > attack_score(enemy_hp) else "Attack"

def threshold(k, enemy_hp):          # solve (1 - hp)^k = attack_score for hp
    return 1 - attack_score(enemy_hp) ** (1 / k)

for k in (1, 2, 3):
    print(f"k={k}: drink below {threshold(k, 1.0):.1%} HP against a fresh enemy")
for e in (1.0, 0.5, 0.1):
    print(f"enemy at {e:.0%}: drink below {threshold(2, e):.1%} HP")
print(choose(0.20, 1.0), choose(0.20, 0.5))
```

Output:

```
k=1: drink below 40.0% HP against a fresh enemy
k=2: drink below 22.5% HP against a fresh enemy
k=3: drink below 15.7% HP against a fresh enemy
enemy at 100%: drink below 22.5% HP
enemy at 50%: drink below 13.4% HP
enemy at 10%: drink below 6.7% HP
Drink Attack
```

The last line is the point of the whole example. At 20% health the brute drinks if the enemy is fresh and keeps swinging if the enemy is at half health. You never wrote "finish off a weak enemy before healing". It fell out of two considerations meeting.

### Numbers you can check

Drink scores by health, for three values of `k`, against the flat Attack score of 0.6 for a fresh enemy. Bold marks the cells where Drink wins.

| Brute's health `h` | `(1 − h)^1` | `(1 − h)^2` | `(1 − h)^3` |
|---|---|---|---|
| 100% | 0.000 | 0.000 | 0.000 |
| 80% | 0.200 | 0.040 | 0.008 |
| 60% | 0.400 | 0.160 | 0.064 |
| 40% | 0.600 (tie) | 0.360 | 0.216 |
| 30% | **0.700** | 0.490 | 0.343 |
| 20% | **0.800** | **0.640** | 0.512 |
| 10% | **0.900** | **0.810** | **0.729** |
| 0% | **1.000** | **1.000** | **1.000** |
| Switch point `h*` | 40.0% | 22.5% | 15.7% |

Check one by hand. With `k = 2`, `h* = 1 − √0.6 = 1 − 0.7746 = 0.2254`. At 20% health, `0.8² = 0.64 > 0.6`, so Drink wins. At 30%, `0.7² = 0.49 < 0.6`, so Attack wins. The switch point sits between them, as it should.

Now hold `k = 2` and vary the enemy.

| Enemy's health `e` | Attack score | Switch point `h* = 1 − √Attack` |
|---|---|---|
| 100% | 0.60 | 22.5% |
| 50% | 0.75 | 13.4% |
| 10% | 0.87 | 6.7% |

Each row is a different brute as far as the player is concerned. Against a fresh opponent it drinks at about a fifth of its health. Against a nearly dead one it fights on to 6.7%. That second number is worth a pause. Is a brute that gambles at 6.7% health what you wanted? Section 4 comes back to it.

### Move it yourself

Open [the interactive](../examples/w08-utility-curves.html). The left view plots both scores against the brute's health. You see the Drink curve for your `k` and a flat Attack line whose height comes from the enemy-health slider. The crossing is marked, with `h*` printed beside it. The right view is a **decision map**: brute health across, enemy health down, every point colored by the action that wins. The boundary between the two colors is the switch point for every enemy health at once.

Drag `k` and watch the whole boundary slide left or right. Drag the enemy's health and watch the flat line rise, the crossing move left, and the dot on the map cross the boundary. Toggle "has potion" off and the map turns solid Attack. The two views show the same numbers. The curve view tells you why. The map view tells you what the player will see.

### Cross-game recognition

**The Sims (Maxis, from 2000).** Graham describes Sims scoring motives such as Hunger with piecewise linear curves, hand-placed points joined by straight lines, because no single formula gave the "ignore it, then notice it, then panic" shape designers wanted. In our form, `(1 − h)^k` is replaced by a drawn curve, and the Sim's behavior changes where that curve crosses the score of whatever it is doing now.

**Guild Wars 2: Heart of Thorns (ArenaNet, 2015).** Mike Lewis describes the expansion's AI, built on Dave Mark's Infinite Axis Utility System. Each possible action has a list of considerations. Each consideration normalizes one input to 0 to 1, passes it through a response curve, and the results are multiplied. Any consideration that scores 0 disqualifies the action at once, and evaluation stops early, so cheap checks go first. This is our model exactly. Our `[has a potion]` is one of their zero-scoring considerations. Lewis adds a production detail. Most curves in the game were chosen from a small palette of presets, because free-form curves were powerful but hard for designers to reason about.

**Dragon Age: Inquisition (BioWare, 2014).** Hanlon and Watts use a potion as their own example of knowledge an AI lacks. Drinking is good at low health, wasteful at full health, and impossible without a potion. Their Behavior Decision System scores each possible action by walking a small "evaluation tree" that adds points. Scores follow a designer convention of bands: basic actions 10, offensive 20 to 40, support 25 to 45, and reactions to immediate threats 50 to 70. Rewrite that in our terms. The band is a coarse priority, and the points within a band are the fine-grained score. A reaction always beats an attack, however good the attack. That is a behavior tree's ordering and a utility score in one number, and section 4 gives it its general name.

Three games, one principle. Every action gets a number from the situation, the highest number wins, and the designer's control lives in the shapes that turn situations into numbers.

### Eyes-open design judgment

- **You tune switch points, not scores.** No player sees 0.64. They see the brute drink at 22%. When a designer says "drink earlier", compute the `k` that puts `h*` where they want it (this lecture's check-yourself question 2 does exactly that) instead of nudging numbers until it looks right.
- **Considerations interact.** The enemy-health consideration moved the switch point from 22.5% to 6.7%. That may be wonderful or terrible. Every consideration you add changes every switch point it touches. Draw the decision map before you ship.
- **Utility is harder to read than a tree.** A player can learn "the guard flees when hurt". "The brute drinks when `(1 − h)²` exceeds `0.6 + 0.3(1 − e)`" is not learnable, even if the behavior feels right. Give the switch a visible cue, such as a bark or an animation, or keep the curves simple enough that the behavior has a nameable rule.
- **Curves are data.** Put them in the data files from CS102 week 13 and give designers a slider tool like the interactive. Lewis makes the same recommendation. Tuning curves by editing code and recompiling is where utility systems go to die.

## 3. Combining considerations

Multiplying scores is the common choice, but it has a side effect you need to know about.

Take two actions. "Attack" has two considerations, both scoring 0.8. "Flank" has five, all scoring 0.9. Every one of Flank's considerations is better than every one of Attack's. Now multiply.

| Action | Considerations | Product | Geometric mean |
|---|---|---|---|
| Attack | 0.8, 0.8 | 0.640 | 0.800 |
| Flank | 0.9 × 5 | 0.590 | 0.900 |

The product picks Attack. Each extra consideration can only pull a score down, so actions with more considerations lose just for being described in more detail. One common fix is the **geometric mean**, the product raised to the power `1/n` for `n` considerations. It keeps the veto (any zero still makes the result zero) and puts actions with different numbers of considerations on the same footing. Its cost is that one low consideration hurts less, so a mean can let through an action that one consideration was trying to discourage. Pick one rule for the whole game and tell your designers which.

Two more rules from production are worth copying.

- **Zero means no.** If a consideration can make an action impossible (no potion, on cooldown, target out of line of sight), let it return exactly 0, and stop evaluating that action. Lewis notes this made it trivial to encode "never do this here" in Heart of Thorns.
- **Cheap first.** Because a zero stops the evaluation, order considerations from cheapest to most expensive. A "have I got a potion?" lookup should come before a pathfinding query that finds the nearest safe spot.

## 4. Choosing among the scores

Once every action has a score, you still have to pick one. There are three common ways, and each one trades something.

**Take the highest.** Predictable and easy to debug. It is also robotic. In the same situation the NPC always does the same thing, and near a switch point it can flip between two actions every think (section 5).

**Weighted random.** Treat scores as weights and roll, as with the loot tables of MA102 week 9. Suppose the brute's scores are Attack 0.60, Drink 0.36, Taunt 0.04. The chance of Taunt is `0.04 / (0.60 + 0.36 + 0.04) = 4%`. At one think per second, in a one-minute fight the brute taunts about 2.4 times, and some of those will be at 5% health with a potion in its pocket. Graham warns about exactly this. Weighted random behaves well most of the time and every now and then chooses something utterly stupid. A common patch is to roll only among actions scoring within some fraction of the best, for example within 10%. Here that leaves Attack alone, since Drink's 0.36 is far below 0.54.

**Buckets, or dual utility.** Give every action two numbers: a **rank**, an integer category, and a **weight** within it. Only the highest rank that has any valid action is considered, and the choice within it uses the weights. Kevin Dill describes using this in Zoo Tycoon 2 (Blue Fang Games, 2004). Animals' ordinary behaviors shared one low rank and competed by weight, while urgent behaviors were given higher ranks so nothing else could interrupt them. Graham describes The Sims bucketing motives the same way. A starving Sim only considers actions that fix hunger and never even scores the TV.

Now look back at Dragon Age: Inquisition's bands. Reactions at 50 to 70 can never lose to offense at 20 to 40. That is a rank written into the score's range. And it answers the question section 2 left open. If a brute fighting on to 6.7% health is not what you want, do not bend the curves until they break. Put "drink when below 10% health" in a higher rank than every attack. The utility scores choose inside the everyday band, and the rank guarantees the non-negotiable rule. That is the behavior tree's fixed priority, used only where you actually want a fixed priority.

## 5. Stability: scores that hover

Week 6 met an NPC that could not pick a target and switched on every hit. Utility systems do the same thing with scores. If the brute's health hovers around its switch point, because a healer keeps topping it up while the enemy keeps hitting it, then every think can land on a different side.

Here are twelve thinks in which the brute's health hovers between 18% and 30% (`k = 2`, fresh enemy, so `h* = 22.5%`). The potion takes 3 thinks in a row to drink, and switching away restarts it. The trace stops mattering once a potion finishes, so read it as "what the rule decides", not as a full fight.

```python
HP = [30, 24, 21, 25, 22, 18, 23, 21, 24, 20, 23, 27]   # percent, one per tick

def replay(bonus):
    current, row = "A", ""
    for hp in HP:
        scores = {"A": 0.6, "D": (1 - hp / 100) ** 2}
        scores[current] *= 1 + bonus                   # commitment bonus
        current = max(scores, key=scores.get)
        row += current
    switches = sum(a != b for a, b in zip("A" + row, row))
    return row, switches

for bonus in (0.0, 0.1, 0.2):
    print(bonus, *replay(bonus))
```

Output:

```
0.0 AADADDADADAA 8
0.1 AAAAADDDDDDA 2
0.2 AAAAAAAAAAAA 0
```

With no bonus the brute switches 8 times in 12 thinks and never drinks for 3 thinks in a row, so no potion ever finishes. It fidgets through the fight.

Graham and Lewis both describe the fix, a **commitment bonus**. Multiply the score of whatever the NPC is already doing by `1 + b`. This turns one switch point into two. While attacking, the brute starts drinking only when `(1 − h)² > 0.6 × (1 + b)`. While drinking, it stops only when `(1 − h)² × (1 + b) < 0.6`. For `b = 0.1`:

```
start drinking below  h = 1 − √(0.66)       = 18.8%
stop drinking above   h = 1 − √(0.6 / 1.1)  = 26.1%
```

Between 18.8% and 26.1% the brute keeps doing whatever it was doing. That band is week 6's hysteresis, applied to scores. The trace shows the result: 2 switches, and a potion finishes on the 8th think.

Look at the third line, though. With `b = 0.2` the start threshold drops to 15.1%, and since health never goes below 18% in this trace, the brute never drinks at all. The bonus buys stability by delaying every decision, including the ones that matter. Size it from the noise you expect in your inputs, not from how calm you want the NPC to look. The Sims Medieval took the blunt approach, according to Graham. A Sim chose a new action only when its queue of actions was empty, and committed until then.

## In-class activity (25 minutes)

Pairs. You are tuning a healer companion in an MMO dungeon with two actions: "Heal tank" and "Damage boss".

1. **Write the model (8 min).** Heal tank's score is `(1 − t)^k`, where `t` is the tank's health fraction. Damage boss scores a flat 0.5. The lead designer wants the healer to start healing at 35% tank health. Compute `k`. (Use logarithms from MA101 week 5.)
2. **Add a consideration (8 min).** Add "my mana fraction `m`" to Heal tank through the curve `m^0.5`. At 25% mana, where does the healer now start healing? Is that what a player in the group wants?
3. **Pick a rule (9 min).** The designer says "the healer must always heal below 15%, whatever its mana." Write the change as a rank (dual utility), and give one sentence on why a curve change alone is the wrong tool.

Expected output: the value of `k` with working, the new switch point, and a two-rank table for the healer's actions.

## Common misconceptions

- **"The highest score is the smartest action."** It is the action your curves prefer. If the curves are wrong the NPC is confidently wrong. Always check switch points against what a designer would say out loud.
- **"Adding considerations makes the AI smarter."** Under a product, each extra consideration also pushes the action's score down, and each one moves the switch points it touches. Add considerations to fix a named behavior, not to add realism.
- **"Utility AI is random."** Take-the-highest selection is fully deterministic. Randomness is a separate choice, and usually a patch for robotic behavior that brings its own "utterly stupid" moments.
- **"A commitment bonus is free."** It widens a single switch point into a band. The NPC reacts later in both directions, and a large bonus can stop it reacting at all.

## Check yourself

1. The brute's designer sets `k = 4`. Against a fresh enemy, at what health does the brute start drinking?
2. The designer wants the brute to drink at 30% health against a fresh enemy, with Attack left at 0.6. What `k` gives that? Show the working.
3. Flee has three considerations, each 0.9. Attack has one, scoring 0.75. Which wins under the product? Under the geometric mean?
4. With a commitment bonus of `b = 0.25` (`k = 2`, fresh enemy), where does the brute start drinking, and where does it stop?
5. The brute's scores are Attack 0.60, Drink 0.36 and Taunt 0.04, and it thinks once per second. Under weighted random selection, how many taunts do you expect in a 60-second fight? Under "roll only among actions within 10% of the best"?

<details>
<summary>Answers</summary>

1. `h* = 1 − 0.6^(1/4) = 1 − 0.880 = 12.0%`.
2. `(1 − 0.3)^k = 0.6`, so `k = ln 0.6 / ln 0.7 = (−0.511) / (−0.357) ≈ 1.43`. Check: `0.7^1.43 ≈ 0.60`.
3. Product: `0.9³ = 0.729 < 0.75`, so Attack wins. Geometric mean: `0.729^(1/3) = 0.9 > 0.75`, so Flee wins. Same inputs, different winner, only because Flee has more considerations.
4. Start: `(1 − h)² > 0.6 × 1.25 = 0.75`, so `h < 1 − √0.75 = 13.4%`. Stop: `(1 − h)² < 0.6 / 1.25 = 0.48`, so `h > 1 − √0.48 = 30.7%`. The band is 13.4% to 30.7%, much wider than with `b = 0.1`.
5. Taunt's chance is `0.04 / 1.00 = 4%`, so `0.04 × 60 = 2.4` taunts. With the 10% filter only actions scoring at least `0.9 × 0.60 = 0.54` are in the roll. That is Attack alone, so zero taunts, and the brute is deterministic again in this situation.

</details>

## Lab / assignment hook

[Lab 08, utility scoring you can tune](../labs/lab08.md). You implement power, logistic and piecewise curves, product and geometric-mean scoring with the zero veto, and selection with a commitment bonus, and reproduce this lecture's switch points and 12-think trace. Then you tune a companion so it matches a designer's written brief, and justify every curve with a switch point.

## Sources

- Graham, D. "Rez" (2013). "An Introduction to Utility Theory." In S. Rabin (ed.), *Game AI Pro*, chapter 9. CRC Press. Free at gameaipro.com. Normalized scores; linear, quadratic, logistic and piecewise linear curves; The Sims' Hunger scored with a hand-tuned piecewise linear curve; weighted random selection that occasionally picks something stupid, and choosing among the top options or those within a percentage of the best; bucketing of motives in The Sims so a starving Sim does not consider the TV; inertia by weighting the current action; The Sims Medieval deciding only when a Sim's interaction queue was empty.
- Lewis, M. (2017). "Choosing Effective Utility-Based Considerations." In S. Rabin (ed.), *Game AI Pro 3*, chapter 13. Free at gameaipro.com. Guild Wars 2: Heart of Thorns (ArenaNet, 2015). Built on the Infinite Axis Utility System (Mark 2013); considerations normalized to 0 to 1, passed through response curves and multiplied; a zero disqualifies the decision and stops evaluation; most curves chosen from a palette of presets; a "commitment bonus" for the last chosen decision against oscillation; a slider tool for tuning.
- Hanlon, S. and Watts, C. (2017). "Behavior Decision System: Dragon Age Inquisition's Utility Scoring Architecture." In S. Rabin (ed.), *Game AI Pro 3*, chapter 31. Free at gameaipro.com. Dragon Age: Inquisition (BioWare, 2014). The health-potion example; evaluation trees that add score; the scoring convention of basic 10, offensive 20 to 40, support 25 to 45, reaction 50 to 70.
- Dill, K. (2015). "Dual-Utility Reasoning." In S. Rabin (ed.), *Game AI Pro 2*, chapter 3. Free at gameaipro.com. Rank and weight; weight-based random; its use in Zoo Tycoon 2 (Blue Fang Games, 2004) for animals and guests.
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapter 5, the section on decision making with scores.
- The brute, its curves, the 12-think health trace and all computed numbers are invented for teaching and computed with the code in this lecture and in `labs/lab08-starter/utility.py`.

## Interactive spec: examples/w08-utility-curves.html

**The one insight:** an NPC's behavior changes exactly where two score curves cross, and every tuning knob (curve exponent, a second consideration, a commitment bonus) is a way of moving that crossing. The curve view shows the crossing; the decision map shows the same crossing as a boundary the player will experience. Dragging `k` and watching the whole boundary slide is the moment the lesson lands.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (curves on top), and a trace strip underneath both.

- **Left, "Scores":** x axis "brute health h" from 0% to 100%, y axis "score" from 0 to 1. Draw the Drink curve `(1 − h)^k` (or a flat 0 line when "has potion" is off) and the Attack line at height `A = 0.6 + 0.3 × (1 − e)`. Mark the crossing with a vertical line and the label "switch point h* = X%". When the bonus `b > 0`, also draw two dashed horizontal lines at `A × (1 + b)` and `A / (1 + b)`, mark where each meets the Drink curve, and shade the band between those two health values with the label "keeps current action".
- **Right, "Decision map":** x axis brute health 0% to 100%, y axis enemy health 100% (top) to 0% (bottom), a 100 × 100 grid of cells colored by the winner with no bonus (Drink or Attack, two palette colors plus a hatch pattern on Drink so color is not the only cue). A dot marks the current (h, e) from the sliders. The boundary curve `h = 1 − (0.6 + 0.3(1 − e))^(1/k)` is drawn as a line.
- **Bottom, "12 thinks":** the lecture's health trace `[30, 24, 21, 25, 22, 18, 23, 21, 24, 20, 23, 27]` as a small bar chart, and under it one row of 12 cells with A or D from the replay at the current `k`, `e` and `b`, plus readouts "switches: N" and "first finished potion: think N" or "none" (a potion finishes after 3 consecutive D). Draw the start and stop thresholds as horizontal lines across the bar chart.

**Controls (keyboard accessible, labelled, each with a numeric readout):**

1. `k` slider, 0.5 to 4.0, step 0.1, default 2.0.
2. Enemy health `e` slider, 0% to 100%, step 1, default 100%.
3. Brute health `h` slider, 0% to 100%, step 1, default 20% (moves the dot and a marker on the left view; shows both scores and the winner as text).
4. Commitment bonus `b` slider, 0 to 0.5, step 0.05, default 0.
5. Checkbox "has potion", default on.
6. Reset button.

**Formulas.** `A(e) = 0.6 + 0.3 × (1 − e)`. `D(h) = potion × (1 − h)^k`. Winner without bonus: Drink if `D > A`, else Attack (ties go to Attack). Switch point `h* = 1 − A^(1/k)`. With bonus while attacking, start drinking when `D > A(1 + b)`, i.e. `h < 1 − (A(1 + b))^(1/k)` (no crossing if `A(1 + b) > 1`, show "never"). While drinking, stop when `D(1 + b) < A`, i.e. `h > 1 − (A / (1 + b))^(1/k)`. Replay: start with current = Attack; each think, multiply the current action's score by `1 + b`, pick the larger (ties keep current), count switches.

**Test values (must match).**

- `k = 1, 2, 3`, `e = 100%`: `h*` = 40.0%, 22.5%, 15.7%.
- `k = 2`: `e = 50%` gives `A = 0.75`, `h* = 13.4%`; `e = 10%` gives `A = 0.87`, `h* = 6.7%`.
- `k = 2`, `e = 100%`, `h = 20%`: Drink 0.640, Attack 0.600, winner Drink. With `e = 50%`: Attack 0.750 wins.
- `k = 4`, `e = 100%`: `h* = 12.0%`.
- Replay at `k = 2`, `e = 100%`: `b = 0` gives AADADDADADAA, 8 switches, no potion; `b = 0.1` gives AAAAADDDDDDA, 2 switches, potion at think 8, band 18.8% to 26.1%; `b = 0.2` gives all A, 0 switches, band 15.1% to 29.3%; `b = 0.25` band 13.4% to 30.7%.
- "Has potion" off: Drink score 0 everywhere, map all Attack, replay all A.

**First screen.** Defaults (`k = 2`, `e = 100%`, `h = 20%`, `b = 0`, potion on). The left view shows the crossing labelled "switch point h* = 22.5%", the map shows the dot just inside the Drink region, and the trace row shows 8 switches. Caption: "The brute changes its mind where the curves cross. Drag k."

**Accessibility.** All sliders reachable by Tab, arrow keys adjust, values announced through `aria-valuetext` ("k equals 2.0, switch point 22.5 percent"). A live region states the current winner and switch point. Respects `prefers-reduced-motion` (no animated curve transitions) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art or logos.
