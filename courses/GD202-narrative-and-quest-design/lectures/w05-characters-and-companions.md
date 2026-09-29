# GD202 · Week 05 — Characters and Companions

**Why this matters:** Companions are the characters players remember longest, because they are with the player for forty hours and react to what the player does. That reaction usually runs on a number, an approval meter, and the way you tune that number decides who gets a romance, who walks out, and whether "just playing my character" ever works. This week you learn to write a companion as a set of values and to predict what their approval meter will do.

**You will be able to:**
- Write a companion's values sheet and derive approval changes from it.
- Compute the distribution of a companion's final approval for a player who agrees with them a given fraction of the time, and the chance that approval reaches a threshold.
- Recognize the same accumulator under different presentations in Dragon Age: Origins, Baldur's Gate 3, Mass Effect 2 and Hades, and say what each changes.
- Estimate the share of companion reaction content a single player sees, and design around it.

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames* (2nd ed., 2021), the chapter on characterization. Reread [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md), sections 1 and 3.

**Prerequisites from earlier courses:** [MA102 week 6, binomial crits over a fight](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (counting successes in `n` independent tries). [MA102 week 5, variance and swingy designs](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md). [GD101 week 5, player experience goals](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md). [GD202 week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md) (facts, counters and rules).

**Interactive:** [`examples/w05-approval-walk.html`](../examples/w05-approval-walk.html). Keep it open during section 2.

---

## 1. What a companion is for

A **companion** is a named character who travels with the player, fights or helps beside them, and comments on what they do. In a single-player RPG the companion does the job other players do in an MMO. They make the world feel witnessed.

Before you write a line, decide which jobs this companion does. Most do several.

- **Mechanical role.** What they add to play: a healer, a lockpicker, a second opinion in puzzles.
- **Witness.** They see what the player does and react, so the player's choices land on someone.
- **Foil.** Their values differ from the player's likely values, so agreement is not automatic. A foil creates the tension that makes approval mean something.
- **Guide.** They know the world and explain it, which lets you deliver lore through a voice instead of a text dump. Week 10 returns to this.
- **Story owner.** They have a personal problem that becomes a quest (Mass Effect 2 calls these loyalty missions).

### The values sheet

Characters in films are defined by what they want and what they will do to get it. Game companions add one more question: what do they *react to*? A companion who reacts to nothing is scenery.

Write a **values sheet** before any dialogue. It is a short list of things the companion approves and disapproves of, each with a reason in their voice. For an invented companion, a retired smuggler named Oda:

| Oda approves of | Why (in her head) | Oda disapproves of | Why |
|---|---|---|---|
| Paying debts | "A deal is the only law that works." | Charity with no return | "Soft hearts get people killed." |
| Clever shortcuts | "Why climb a wall with a door in it?" | Needless cruelty | "Waste. Of time and of people." |
| Protecting crew | "You don't leave your own." | Bowing to authority | "Titles are just prices." |

The sheet does two jobs. It is a writing guide. Every Oda line should sound like the "why" column. It is also a design spec. Each row turns into approval changes at events where the player's choice touches that value. Values that pull against each other (paying debts versus charity) make Oda feel like a person, because the player cannot please her by following one simple rule.

### Voice in three tests

A companion's **voice** is how they sound: vocabulary, sentence length, what they joke about, what they never say. Three quick tests catch most voice problems.

1. **Cover the name.** Hide the speaker labels in a scene. Can a reader tell Oda from the other companions? If not, the voices are too close.
2. **The never list.** Write three things this character would never say. Oda never says "please" to an official. When a line breaks the list, the character breaks.
3. **Length budget.** Companion barks are heard many times. Keep reaction lines to one or two sentences. Long reactions are fine once. At the fourth repeat they become noise.

## 2. Worked example: the approval walk

### The hook

In Baldur's Gate 3 (Larian, 2023), every companion keeps an approval number toward the player character. The community wiki documents the rules. Choices typically move approval by 1, 5 or 10 for small, medium and large events. Approval tops out at 100. At −20 and again at −40 the companion warns you, and at −50 or lower they leave the party for good, taking their equipped gear with them. Romance and some personal-quest outcomes need approval above set thresholds.

Dragon Age: Origins (BioWare, 2009) did the same thing fourteen years earlier with a −100 to +100 meter, named bands such as Warm and Adore, stat bonuses at high approval, and a walk-out attempt at −100.

Here is the question players argue about on forums, and designers should settle with numbers. **If I just play my character, agreeing with a companion some of the time, will I ever reach their romance threshold?**

### The model

Treat each approval event as a coin flip weighted by the player's taste.

- `n` is the number of approval events the player meets with this companion.
- `s` is the step size. The player gains `+s` when they choose what the companion likes and `−s` otherwise.
- `p` is the chance the player picks what the companion likes at any one event. A player who shares the companion's values has high `p`. A player who ignores the companion entirely has `p` near 0.5, if the companion's values are unrelated to the player's.
- `K` is the number of events where the player agreed. Each event is independent, so `K` follows the binomial distribution from MA102 week 6.

Final approval is agreements minus disagreements, times the step:

```
A = s × (K − (n − K)) = s × (2K − n)

mean of A  = s × n × (2p − 1)
spread (SD) = 2s × √(n × p × (1 − p))

P(A ≥ T) = P(K ≥ ⌈(n + T/s) / 2⌉)
```

The model ignores caps. With `n × s ≤ 100`, a meter capped at ±100 never binds, so the cap changes nothing. Section 4 deals with caps that do bind.

### Numbers you can check

Take `n = 20` events with `s = 5`, and a threshold of `T = 50`. The player needs `2K − 20 ≥ 10`, so `K ≥ 15` agreements out of 20.

For a player at `p = 0.5` you can check this by hand with binomial coefficients:

```
P(K ≥ 15) = [C(20,15) + C(20,16) + C(20,17) + C(20,18) + C(20,19) + C(20,20)] / 2^20
          = (15,504 + 4,845 + 1,140 + 190 + 20 + 1) / 1,048,576
          = 21,700 / 1,048,576 ≈ 2.1%
```

The same calculation for other values of `p`, in Python:

```python
from math import comb, ceil

def p_reach(n, s, T, p):
    """Chance that approval s * (2K - n) ends at T or more, K ~ Binomial(n, p)."""
    k_min = max(0, ceil((n + T / s) / 2))
    return sum(comb(n, k) * p**k * (1 - p)**(n - k) for k in range(k_min, n + 1))

n, s, T = 20, 5, 50
print("p     mean    sd   P(A >= 50)")
for p in [0.5, 0.6, 0.7, 0.75, 0.8, 0.9]:
    mean = s * n * (2 * p - 1)
    sd = 2 * s * (n * p * (1 - p)) ** 0.5
    print(f"{p:.2f}  {mean:4.0f}  {sd:5.1f}  {p_reach(n, s, T, p):7.1%}")
```

It prints:

```
p     mean    sd   P(A >= 50)
0.50     0   22.4     2.1%
0.60    20   21.9    12.6%
0.70    40   20.5    41.6%
0.75    50   19.4    61.7%
0.80    60   17.9    80.4%
0.90    80   13.4    98.9%
```

Read the last column slowly. A player who agrees with the companion 60% of the time, which is a player who mostly likes them, has about a one-in-eight chance of the romance. At 70% it is still under half. The chance crosses 50% at about `p = 0.72`. Then it climbs fast, reaching 80% at `p = 0.8`.

Now move the threshold instead, holding `p = 0.7`:

| Threshold `T` | Agreements needed out of 20 | `P(A ≥ T)` at `p = 0.7` |
|---|---|---|
| 25 | 13 (12.5 rounded up) | 77.2% |
| 50 | 15 | 41.6% |
| 75 | 18 (17.5 rounded up) | 3.6% |
| 100 | 20 | 0.08% |

A threshold at 75 is effectively "only players who deliberately court this companion". A threshold at 25 is "most players who like them". Neither is wrong, but you should choose knowingly.

### The two views

Open the interactive. The left panel is a histogram of final approval for the current `n`, `s` and `p`, with the threshold drawn as a vertical line and the area to its right shaded. The right panel plots `P(A ≥ T)` against `p` from 0 to 1, with a dot at the current `p`.

The histogram looks gentle. At `p = 0.6` it is a wide hump centred at +20, and the threshold at +50 sits only about 1.4 standard deviations away. It looks reachable. The right panel shows the truth. The curve is an S, flat near zero until about `p = 0.55`, then steep. Small changes in how often the player agrees make huge changes in who gets the payoff. Drag `n` up to 40 and watch the S get steeper. With more events, the outcome depends more on the player's real leaning and less on luck. At `p = 0.6` and `n = 40`, the chance of reaching 50 rises from 12.6% to 44%, while the indifferent `p = 0.5` player only rises from 2.1% to 7.7%.

That is the insight. **An approval meter is a sorting machine.** With enough events it reliably separates players who lean toward a companion from those who do not. The designer's knobs (`n`, `s`, `T`) decide how hard it sorts.

### Cross-game recognition

Each of these systems is the same accumulator. What changes is who controls the steps, how big they are, and where the walls are.

**Dragon Age: Origins (2009).** Approval runs from −100 to +100 and everyone except the dog starts at 0. The Dragon Age wiki lists bands (Neutral from −25 to 25, Warm from 26, and higher bands above that) and primary-attribute bonuses at approval 25, 50, 75 and 90 (+1, +2, +4 and +6, not cumulative). At −100 the companion tries to leave, and you get one chance to talk them down. Gifts also raise approval. In our model a gift is an extra event with `p = 1`, one the player can trigger at will. Gifts are an escape valve. A player who disagrees with a companion can still buy their way up, which flattens the S-curve and weakens the sorting.

**Baldur's Gate 3 (2023).** Same accumulator, with steps of 1, 5 or 10 so `s` varies by event importance. The meter has a hard ceiling at 100 and a leaving wall at −50, with warnings at −20 and −40. One more rule changes `n`. The wiki notes that approval usually only changes if the companion is close enough to the player when the event happens. So the companions you bring along face more events, and a companion left at camp barely moves. Party choice becomes a quiet way of choosing `n`.

**Mass Effect 2 (BioWare, 2010).** Loyalty is binary. Each squad member has one personal loyalty mission. Completing it (and, for some members, making the choice they wanted during it) makes them loyal, which unlocks a bonus power and an alternate outfit and improves their chance of surviving the final suicide mission. In our model that is `n = 1` with a threshold of one success. There is no sorting and no drift. The design trades subtlety for clarity. Every player knows exactly how to earn loyalty, and the drama moves to the choices inside the mission.

**Hades (Supergiant, 2020).** Relationships grow when you give Nectar, a rare currency, to characters. The first gift returns a Keepsake item, and after about five or six gifts the character offers a favor quest that unlocks the rest of the relationship. Approval never goes down. In our model every event has `p = 1`, and the player decides when events happen by spending a scarce resource. There is nothing to predict. The design question moves from "will they like me?" to "whom do I spend on first?"

Four games, one ledger. When you meet a relationship system, ask four questions. What are `n` and `s`? Can steps be negative? Who controls when steps happen? Where are the thresholds and walls?

### Design judgment

- **Signed meters reward consistency.** A player who role-plays one coherent character (high or low `p` for a companion) gets a clear outcome. A player who picks options on a whim ends near zero with every companion. If your game's promise is "be whoever you want", check that whim players still get a relationship worth having. Lower thresholds or gifts help.
- **Visible numbers change `p`.** Baldur's Gate 3 shows approval pop-ups on screen. Once players see "+10 approval", many stop choosing by conscience and start choosing for the meter, pushing their `p` toward 1 for the companion they want. That is fine if you want relationships as an optimization game. If you want them to reflect honest play, hide or delay the feedback.
- **Step sizes carry meaning.** A single big step (`s = 20`) on a defining moment tells the player "this mattered". Many small steps say "this is a slow drift". Mixing them lets a companion forgive small slights but not a betrayal.
- **Walls are drama.** A companion who can leave (DA:O at −100, BG3 at −50) makes the negative side of the meter a story instead of a missing bonus. It also means some players lose content. Warn them first, as BG3 does twice.

## 3. How much of your companion writing does a player see?

Companions are expensive. Every event a companion can react to needs a line from that companion, and usually one line for approve and one for disapprove.

```
reaction lines written = c × e × v
```

where `c` is the number of companions, `e` the number of reactable events and `v` the variants per event (2 for approve and disapprove, more if lines depend on approval band).

Now count what one player hears. Dragon Age: Origins has ten full companions but a field party of the Warden plus up to three. If every companion has a line for an event and only party members react, a player hears at most 3 of 10 companions per event, 30% of what was written for it. A player who sticks with one party for the whole game hears only 30% of the reaction writing across the game. A second playthrough with a different party finds new material, which is part of why reactive RPGs reward replays.

This is the same pressure as [week 3's branch explosion](w03-branching-structures-and-the-combinatorial-explosion.md), arriving from a different direction. You cannot cut companions to save lines, because choice of companion is the point. So teams use three tactics.

- **Tier the events.** Write reactions from every companion only for major events. For minor events, write for two or three companions whose values the event touches, and let the others stay silent.
- **Use the rule matcher from week 4.** Give each companion a fallback "general approval" and "general disapproval" line, then specific lines for events that touch their values. Specific rules win when they match. Everything else falls back.
- **Let companions talk to each other.** Banter between two companions is written once per pair, not per event, and does not depend on the player's choices, so its value per line is high. With `c` companions there are `c(c − 1)/2` pairs. Ten companions make 45 pairs, so budget banter for the pairs players are most likely to bring together.

## 4. Conflicting companions and walls

### Opposed values

Suppose two companions have exactly opposite values on every event, so whatever pleases one displeases the other. Then their approvals are exact negatives of each other. At most one can end above zero, and if you set both romance thresholds at +50, no player can reach both. That is a strong design statement. It makes the player choose, but it also makes the choice for them after a few events, since they drift toward one side.

Real casts are partly opposed. If companions A and B disagree on half the events and are indifferent on the rest, a player can reach high approval with both only by being consistent on the events each cares about. Map your cast's values in a grid (companions down the side, events across the top, +, − or blank in each cell) before writing lines. Columns where two companions have opposite signs are where the player will feel torn. You want some of those columns, not all.

### When the cap binds

The model in section 2 assumed the meter never hits its limits. Games that allow many events per companion often do hit them. In Baldur's Gate 3 approval stops at 100. Once there, further approval is lost, and a later disapproval takes the companion down from 100, not from wherever the uncapped sum would be. Caps make approval **path-dependent**. The order of events matters as well as the count. A player who earns ten approvals and then suffers two disapprovals ends lower than one who takes the disapprovals first, if the ten approvals would have overshot the cap.

The fix in your spreadsheet is to simulate the walk step by step and clamp after every step, which is what Lab 05 asks you to do. The designer's decision is whether you want this. A cap stops players banking approval early and coasting, which keeps late choices meaningful.

## In-class activity (25 minutes)

In pairs, design one companion for a 20-hour RPG.

1. Write a values sheet with three approvals and three disapprovals, each with a one-line reason in the companion's voice.
2. List ten approval events the player will meet in a typical playthrough. For each, write the step for the approved and disapproved choice (you may use different sizes).
3. Pick a romance or friendship threshold. Using the interactive (or the Python above), find the smallest `p` at which at least half of players reach it. Write that `p` down and say, in one sentence, what kind of player it describes.
4. Swap with another pair. Read their values sheet, then play their ten events honestly as yourself, choosing without looking at the steps. Report your final approval and whether you reached their threshold.

Expected output: the values sheet, the event table, the threshold with its 50% `p`, and your partners' honest-play result.

## Common misconceptions

- **"Average approval is what matters."** The payoff depends on crossing a threshold, not on the average. At `p = 0.7` the average is +40 but only 42% of players reach +50.
- **"More approval events make the meter fairer to everyone."** More events make it sort more sharply. Leaning players gain, and indifferent players stay near zero with narrower spread.
- **"A companion who disapproves is a failure state."** Disapproval and walk-outs are content. Players remember the companion who left.
- **"Write every companion's reaction to everything."** The player hears only the companions in their party. Tier events and use fallbacks.

## Check yourself

1. A companion has `n = 12` events with `s = 10` and a threshold of 60. How many agreements does the player need? What is the chance for a `p = 0.5` player? Give the exact fraction.
2. You double the number of events from 20 to 40, keeping `s = 5` and `T = 50`. Without computing, which player's chance of reaching the threshold grows more in percentage points, the `p = 0.6` player or the `p = 0.5` player? Why?
3. A companion in the style of Hades gains one heart per gift, never loses them, and offers a quest at five gifts. Rewrite this in the model's terms (`n`, `s`, `p`, `T`). What is `P(A ≥ T)`, and what does the design test instead of the player's values?
4. A game has 8 companions, a party of the player plus 2, 60 reactable events and 2 variants per event. How many reaction lines are written if every companion reacts to every event? What fraction does a player who never changes party hear?

<details>
<summary>Answers</summary>

1. `2K − 12 ≥ 6`, so `K ≥ 9`. The chance is `[C(12,9) + C(12,10) + C(12,11) + C(12,12)] / 2^12 = (220 + 66 + 12 + 1) / 4,096 = 299 / 4,096 ≈ 7.3%`.
2. The `p = 0.6` player. Their mean rises with `n` (from +20 to +40, since mean is `s × n × (2p − 1)`) while the spread grows only with `√n`. The `p = 0.5` player's mean stays at 0 and only the spread grows. The numbers from section 2 are 12.6% to 44% versus 2.1% to 7.7%.
3. `s = 1` heart per event, `p = 1` because every gift is a positive step, `T = 5`, and `n` is however many gifts the player chooses to give. `P(A ≥ T) = 1` once `n ≥ 5`. The design tests whether the player chooses to spend scarce Nectar on this character, not whether they share the character's values.
4. `8 × 60 × 2 = 960` lines. The player hears 2 of 8 companions, one variant each, so `2 × 60 = 120` lines, 12.5% of what was written.

</details>

## Lab / assignment hook

[Lab 05, approval tuning](../labs/lab05.md). You implement the exact approval distribution with a step-by-step walk that supports different step sizes per event and a clamped meter, then tune a companion of your own so that three player personas get the outcomes you intend. The values sheet and event table feed the dialogue-exercise portion of the course assessment.

## Sources

- bg3.wiki, "Approval" (Baldur's Gate 3, full release 2023 and later patches). Typical approval changes of ±1, 5 or 10; maximum 100; companions leave at −50 or lower after warnings at −20 and −40; approval bands; approval changes only for companions near the player.
- Dragon Age Wiki, "Approval (Origins)" (Dragon Age: Origins, 2009). Range −100 to +100, start at 0 except Dog; band table; attribute bonuses +1, +2, +4, +6 at 25, 50, 75, 90 approval, not cumulative; crisis at −100 with a single chance to talk the companion out of leaving; field party of the Warden plus up to three companions; ten full companions in Origins.
- Mass Effect Wiki, "Loyalty" (Mass Effect 2, 2010). One loyalty mission per squad member; loyalty unlocks a bonus power and alternate outfit and improves survival in the suicide mission; some missions can end without loyalty.
- Hades Wiki, "Nectar" (Hades, 2020 release). First Nectar gift returns a Keepsake; about 5 to 6 Nectar gifts lead to a favor quest.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury Academic.

## Interactive spec: examples/w05-approval-walk.html

**Purpose.** Show that an approval meter sorts players by how often they agree with a companion, and that the chance of reaching a threshold is an S-curve in `p` even when the histogram looks gentle.

**Layout.** Two linked panels, stacked on mobile, side by side from 900px. Controls above them.

- **Left panel, "Where approval ends".** Bar chart of the exact distribution of `A = s(2K − n)` for `K = 0..n`, bar heights `C(n,k) p^k (1−p)^(n−k)`. X axis is approval (from `−n·s` to `+n·s`), y axis is probability in percent. Draw a vertical line at `T`; bars with `A ≥ T` are filled in the accent colour, the rest in neutral. Label the mean with a small tick and print "mean = …, SD = …" above the chart. If the cap toggle is on, bars beyond ±cap are stacked into the end bar.
- **Right panel, "Who gets the payoff".** Line chart of `P(A ≥ T)` against `p` from 0 to 1 in steps of 0.01. A dot marks the current `p`, with its value printed next to it. A dashed horizontal line at 50% and a label "50% at p ≈ …" computed by bisection.
- **Readout row** under both panels, in large tabular numerals: `P(A ≥ T) = 41.6%`, `agreements needed: 15 of 20`, `mean +40, SD 20.5`.

**Controls.**
1. `p`, agreement probability, slider 0.00 to 1.00, step 0.01, default 0.70.
2. `n`, number of events, slider 1 to 60, default 20.
3. `s`, step size, select from 1, 5, 10, 20, default 5.
4. `T`, threshold, slider from −100 to 100 in steps of 1, default 50 (step 1 so the BG3-like preset can hold `T = 41`).
5. Toggle "Clamp at ±100". When on, compute the distribution by dynamic programming over the walk, clamping to [−100, 100] after every step, instead of the closed form. Show a note "path-dependent: order matters" when clamping changes any probability by more than 0.1 percentage points.
6. Preset buttons: "BG3-like" (`s = 5`, `T = 41`, `n = 30`), "Lecture default" (`n = 20`, `s = 5`, `T = 50`, `p = 0.7`), "Hades-like" (`p = 1`, `s = 1`, `T = 5`, `n = 6`).

**The one insight.** Moving `p` from 0.6 to 0.8 moves the right-panel dot from about 13% to about 80%, while the left histogram only slides 40 points. The left view looks smooth; the right view shows the cliff.

**Exact test values** (closed form, no clamp):

| n | s | T | p | P(A ≥ T) |
|---|---|---|---|---|
| 20 | 5 | 50 | 0.50 | 2.07% (21,700 / 1,048,576) |
| 20 | 5 | 50 | 0.60 | 12.56% |
| 20 | 5 | 50 | 0.70 | 41.64% |
| 20 | 5 | 50 | 0.75 | 61.72% |
| 20 | 5 | 50 | 0.80 | 80.42% |
| 20 | 5 | 50 | 0.90 | 98.87% |
| 20 | 5 | 25 | 0.70 | 77.23% |
| 20 | 5 | 75 | 0.70 | 3.55% |
| 12 | 10 | 60 | 0.50 | 7.30% (299 / 4,096) |
| 40 | 5 | 50 | 0.60 | 44.02% |
| 40 | 5 | 50 | 0.50 | 7.69% |

- Mean `s·n·(2p − 1)`; SD `2s·√(n·p·(1 − p))`. At `n = 20, s = 5, p = 0.7`: mean 40, SD 20.49.
- Agreements needed: `k_min = max(0, ceil((n + T/s) / 2))`; `P = 0` if `k_min > n`.
- 50% crossing at `n = 20, s = 5, T = 50` is `p ≈ 0.721`.
- Clamp check: `n = 30, s = 10, T = 50, p = 0.7` must differ between clamped and unclamped computations (the walk can hit +100); the builder should verify the DP against the closed form when `n·s ≤ 100`, where they must match exactly.

**Accessibility.** Native range inputs with visible numeric values and `aria-valuetext` (e.g. "p equals 0.70, 70 percent agreement"). Charts have a text summary in an `aria-live="polite"` region that updates on change. Colour is paired with pattern (hatched fill for bars at or above `T`).
