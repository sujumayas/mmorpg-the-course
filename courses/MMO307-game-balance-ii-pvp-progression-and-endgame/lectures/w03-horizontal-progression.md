# MMO307 · Week 03 — Horizontal Progression

**Why this matters:** Horizontal progression is the usual answer to week 2's power creep. Give players new options instead of bigger numbers. But a new option is only worth what the content lets it do. If the situation it is built for comes up once a month, the reward is a trophy, not progress. You can compute which rewards will be ignored before you build them.

**You will be able to:**
- Compute the expected value of a horizontal reward from how often its situation occurs, and rank a set of rewards by what they are worth to a player.
- Compute the effective number of situations in a content mix and the largest power gap that horizontal breadth can create.
- Derive how a content rotation changes both numbers, and explain the trade-off between valuable breadth and a small power gap.
- Critique a horizontal reward track by distinguishing bonus-type rewards from gate-type rewards and predicting which ones players will chase.

**Before class:** Schreiber, *Game Balance Concepts*, Level 6, "Situational Balance" (2010, free online). Warcraft Wiki, "Affix" (10 minutes, the Mythic+ section). Guild Wars 2 Wiki, "Gliding" (5 minutes, where gliders can and cannot be used).

**Prerequisites from earlier courses:** [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (the tool model `P_h = 1 + b × k/n`, the gap ceiling, and the dominance and expected-value tests, which we build on without repeating). [MMO303 week 1, what balanced means](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md) (the effective number of classes from a pick-share table). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). [Week 2 of this course](w02-vertical-progression-and-power-creep.md) (the upgrade margin `u` and the ratchet).

**Interactive:** [`examples/w03-situation-weights.html`](../examples/w03-situation-weights.html). Keep it open during section 2.

---

## 1. What GD203 gave you, and what it assumed

Week 2 showed that vertical progression creeps because every new reward must beat the old one. **Horizontal progression** avoids the ratchet. A horizontal reward is better than what you have only in some situations, so it does not have to be bigger to be wanted. It has to be different.

GD203 week 14 built the basic model. There are `n` kinds of situation and one tool for each. The right tool multiplies your power by `1 + b` in its situation and does nothing elsewhere. A player who owns `k` of the `n` tools has expected power `1 + b × k/n`, and the gap between a full collection and a newcomer's single tool can never exceed `(1 + b) / (1 + b/n)`. GD203 also gave you two tests for whether a sidegrade is really a sidegrade: dominance, and expected value across situation frequencies.

That model made one quiet assumption. Every situation is equally common. It is why each tool added exactly `b/n` and why the gap ceiling had `n` in it.

Real content is never that even. Most MMO endgames have one or two dominant activities, a handful of regular ones and a long tail of rare ones. Once the frequencies are uneven, the value of each horizontal reward changes, the gap ceiling changes, and the design question shifts from "is it balanced?" to "will anyone want it?"

A few terms for this lecture.

- A **situation** is any recurring kind of play that rewards a specific tool, such as a boss-heavy week, an armored enemy type, a zone with verticality, or a PvP map.
- A **tool** is a horizontal reward that is strong in one situation, such as a weapon type, a talent, a mount or a job.
- A **bonus** tool improves your power in its situation. A **gate** tool is required to complete its situation at all. Section 4 treats gates.
- The **content mix** is the set of frequencies `f_1, ..., f_n` with which situations occur in a player's actual play. The `f_i` add up to 1.

## 2. Worked example: the reward nobody chases

### The hook

World of Warcraft's Mythic+ dungeons change on purpose every week. The Warcraft Wiki describes the system as built around weekly-rotating affixes that reward group utility, coordination and focus. Two of them take turns. Fortified makes the trash stronger, and Tyrannical makes the bosses stronger. In the current system, one of the two switches on at keystone level 7, alternating week by week, and the other joins at level 10. The affixes are the same for every player in a given week and rotate on a fixed schedule at the weekly reset.

Guild Wars 2 does something different with one of its best-known horizontal rewards. Gliding, introduced with the Heart of Thorns expansion, is a movement ability players train and keep. Its official wiki lists where gliders work, which is most open-world zones and expansion instanced content, and where they do not, which includes PvP maps and the dungeons of the original game.

Both games are making the same decision. Blizzard is choosing how often each situation comes up. ArenaNet is choosing which situations a tool applies to. Both choices set how much a horizontal reward is worth, and a model tells you by how much.

### The model

Extend GD203's tool model with uneven frequencies. Situation `i` occurs with frequency `f_i`, sorted from most common to least common. Tool `i` gives `+b` power in situation `i` only. A player who owns the set `K` of tools has expected power:

```
P(K) = 1 + b × Σ_{i in K} f_i
```

Three quantities follow.

The **marginal value** of tool `i`, how much it adds to expected power, is simply

```
v_i = b × f_i
```

A tool for a rare situation is worth little, however strong it is in that situation.

The **gap ceiling**, the largest ratio between a player with every tool and a newcomer who owns only the most common one, is

```
G_max = (1 + b) / (1 + b × f_1)
```

When every `f_i = 1/n`, this is GD203's `(1 + b)/(1 + b/n)`.

The **effective number of situations** is

```
N_eff = 1 / Σ f_i²
```

This is the same measure you met in MMO303 week 1 as the effective number of classes, applied to situations instead of picks. With `n` equally common situations `N_eff = n`. When one situation dominates, `N_eff` falls toward 1. It tells you how many situations the content mix really has, and so roughly how many tools are worth chasing.

### Numbers you can check

Take `n = 6` situations and `b = 0.3`, GD203's numbers. First the even mix, then a **Zipf mix**, a common shape where the `i`-th most common situation occurs in proportion to `1/i`. The Zipf frequencies are `(1/i) / H_6` with `H_6 = 1 + 1/2 + ... + 1/6 = 2.45`.

| Situation `i` | Even `f_i` | Even value `b f_i` | Zipf `f_i` | Zipf value `b f_i` |
|---|---|---|---|---|
| 1 | 0.167 | 5.0% | 0.408 | 12.2% |
| 2 | 0.167 | 5.0% | 0.204 | 6.1% |
| 3 | 0.167 | 5.0% | 0.136 | 4.1% |
| 4 | 0.167 | 5.0% | 0.102 | 3.1% |
| 5 | 0.167 | 5.0% | 0.082 | 2.4% |
| 6 | 0.167 | 5.0% | 0.068 | 2.0% |

Every tool is "+30% in its situation" on the tooltip. Under the Zipf mix, the first tool is worth six times as much as the sixth. The sixth adds 2% to expected power. Recall week 2's upgrade margin `u`, the smallest gain players will do content for. If `u` is around 5%, only the first two tools clear it on value alone. The other four are rewards players will skip unless something else carries them.

The summary numbers:

| Mix | `N_eff` | Newcomer (tool 1 only) | Full collection | Gap ceiling `G_max` |
|---|---|---|---|---|
| Even | 6.00 | 1.050 | 1.300 | 1.238 |
| Zipf | 4.02 | 1.122 | 1.300 | 1.158 |

Two things happen at once. The Zipf mix has fewer effective situations (about 4 instead of 6), so breadth is worth less. It also has a smaller gap ceiling, because the newcomer's single tool covers 41% of play. Uneven content makes horizontal progression less rewarding and more equal at the same time.

You can check both tables in a few lines.

```python
n, b = 6, 0.3
H = sum(1 / i for i in range(1, n + 1))
zipf = [(1 / i) / H for i in range(1, n + 1)]

def summary(f):
    n_eff = 1 / sum(x * x for x in f)
    ceiling = (1 + b) / (1 + b * max(f))
    return round(n_eff, 2), round(ceiling, 3)

print([round(b * x, 3) for x in zipf])
print(summary([1 / n] * n), summary(zipf))
```

```
[0.122, 0.061, 0.041, 0.031, 0.024, 0.02]
(6.0, 1.238) (4.02, 1.158)
```

### A visual you can move

Open the interactive. The left panel shows six bars, one per tool, each labelled with its power in its own situation. With the defaults they are all the same height, `+30%`. That is what players see on tooltips, and it suggests six equally good rewards.

The right panel shows what each tool is worth, `b × f_i`, with a dashed line at the upgrade margin `u`. Under the Zipf mix, four of the six bars fall below the line. Drag the **rotation** slider (section 3) from 0 to 1 and watch the right-hand bars level out, `N_eff` climb from 4.02 to 6, and the gap ceiling climb from 1.158 to 1.238. Same tools, same tooltips. The content mix alone decided which rewards matter.

### Cross-game recognition

**World of Warcraft Mythic+ (The War Within and Midnight eras): rotation sets `f`.** At keystone levels 7 to 9, Fortified and Tyrannical alternate weekly. Over a season, trash-heavy and boss-heavy weeks are each half of the weeks at those levels, so a tool that shines against strong trash and one that shines against strong bosses have the same season value. In any single week one of them is worth nothing extra. A player who owns both always has the right one, which is exactly the breadth value in the model. The rest of the affix rotation works the same way on a larger set of situations. The design effect is to flatten the season's content mix, raise `N_eff`, and make a wider set of talents and utility worth owning.

**Guild Wars 2 (Heart of Thorns onward): applicability sets `f`.** Gliding works in most open-world zones and expansion instances and does not work in PvP maps or the original game's dungeons. For a player who mostly plays open-world expansion content, its `f` is large. For a player who mostly plays structured PvP, its `f` is zero. The same reward has different values for different players because their content mixes differ. When you estimate `f`, estimate it per player segment, not for the game as a whole.

**Destiny 2 (Shadowkeep onward): the gate version.** Champions, introduced in Shadowkeep (2019), are tough enemies of three types, Barrier, Overload and Unstoppable. Each type is countered by a matching weapon or ability effect, and hitting a champion with the right effect stuns it. Destinypedia notes that champions are guaranteed in Heroic and harder content such as Nightfalls, and that each enemy race fields champions of two of the three types. So in hard content the anti-champion effect is not a `+b` bonus. It is close to a requirement. Section 4 shows how that changes the model.

**Final Fantasy XIV (the Armoury system).** GD203 week 14 already read jobs as tools. The frequency lens adds one point. A tank job's value to a player is the share of their groups that need a tank, which the game's matchmaking decides. The designer sets `f` through the queue as much as through the encounters.

Four games, one question. For any horizontal reward, ask how often its situation occurs in this player's play, and whether the reward is a bonus or a gate there.

### Eyes-open design judgment

- **Tooltip strength is not value.** A tool that is `+30%` in a situation seen 5% of the time is a 1.5% reward. If you want players to chase it, either raise its situation's frequency or accept that it is a collectible.
- **Rotations make breadth worth owning, and they widen the gap.** Flattening the mix raises `N_eff` and the value of every rare tool. It also raises `G_max`, since the newcomer's one tool now covers less of play. There is no setting that maximizes both. Choose where you want to sit.
- **Per-segment mixes differ.** A PvP player and a raider have different `f` vectors. A reward that is essential to one is dead to the other. That is fine, as long as every segment has some tools above `u`.
- **Low-frequency tools need a different reason to exist.** Collections, cosmetics or achievements can carry a tool whose power value is small. Guild Wars 2's masteries carry much of their appeal through traversal and access, not stats.
- **Horizontal balance is conditional.** GD203 warned that a sidegrade balanced for one content mix becomes best-in-slot when the mix changes. The frequency model tells you by how much. When you add a new raid full of one situation, recompute every `b × f_i`.

### Check yourself (worked example)

1. A game has four situations with frequencies 0.5, 0.25, 0.15 and 0.10, and every tool gives `b = 0.4`. What is each tool worth? What is `N_eff`?
2. What is `G_max` in that game? What would it be if the four situations were equally common?

<details>
<summary>Answers</summary>

1. Values are `0.4 × f`: 20%, 10%, 6% and 4%. `Σ f² = 0.25 + 0.0625 + 0.0225 + 0.01 = 0.345`, so `N_eff = 2.90`.
2. `G_max = 1.4 / (1 + 0.4 × 0.5) = 1.4 / 1.2 = 1.167`. Equal mix: `1.4 / 1.1 = 1.273`.

</details>

## 3. Rotations: choosing the mix on purpose

A **rotation** changes which situations the content presents over time, on a schedule. The Mythic+ affix cycle, weekly featured dungeons and daily bonus activities are all rotations. MMO306 week 8 studied how quickly a rotation wears out its pool. Here the question is what a rotation does to the value of horizontal rewards.

Model a rotation by how strongly it pulls the season's mix toward even. With rotation strength `λ` between 0 and 1, the season-average frequency of situation `i` is

```
f'_i = λ × (1/n) + (1 − λ) × f_i
```

At `λ = 0`, the natural mix is unchanged. At `λ = 1`, every situation is equally common over the season. In between, the rotation features under-played situations often enough to lift them part of the way.

For the Zipf mix with `n = 6` and `b = 0.3`:

| Rotation `λ` | `f'_1` | `f'_6` | Value of tool 6 | `N_eff` | `G_max` |
|---|---|---|---|---|---|
| 0 | 0.408 | 0.068 | 2.0% | 4.02 | 1.158 |
| 0.5 | 0.287 | 0.117 | 3.5% | 5.34 | 1.197 |
| 1 | 0.167 | 0.167 | 5.0% | 6.00 | 1.238 |

A half-strength rotation raises the rarest tool's value by about 72% (from 2.04% to 3.52%) and adds more than one effective situation. The price is a gap ceiling up from 1.158 to 1.197. Both numbers are small compared with vertical progression. At GD203's band of `F = 2` all three settings are far inside it. So for most games the trade-off lands in favour of rotating, and it is the one lever that makes a long list of horizontal rewards pay off.

Rotations have their own costs, which week 1 and MMO306 cover. They create chores (log in this week or miss the featured situation), and a player whose favourite situation is off-rotation has a bad week. A rotation is also a content cost. Every featured situation must be good enough to be the whole week's content.

## 4. When the tool is a gate

The bonus model assumes that without the right tool you still play the situation, just less well. Some rewards are required. Without them, you cannot complete the content at all. Destiny 2's champions in hard content are the standard example.

Model gates with **activities** instead of situations. Each activity requires a set of tools. A player can complete an activity only if they own every tool it requires. The value of a collection is the share of activities it opens.

Take Destiny 2's structure as the shape, with invented frequencies. There are three counter types, A, B and C. Each hard activity features two of them, and the three pairs AB, AC and BC are equally common.

| Counters owned | Activities open | Share of activities |
|---|---|---|
| none | none | 0% |
| one (say A) | none (every activity needs two) | 0% |
| two (A and B) | AB | 33% |
| all three | AB, AC, BC | 100% |

Look at the marginal values. The first counter adds nothing. The second adds 33 points. The third adds 67. Under bonuses, value per tool fell as the collection grew (the Zipf table). Under gates, value per tool **rises** as the collection grows. The last tool is the most valuable one.

That flips the player's experience. With bonuses, early rewards feel great and late ones feel small, the same shape as week 1's random drops. With gates, early rewards feel useless and the last one feels essential. Players who are one counter short of full access will chase it hard, and players who own none may not start at all.

Two design responses follow.

- **Make the first gate tool free or cheap.** If the first counter opens nothing, hand it out, or change the activity mix so that some activities need only one.
- **Let players see the gate before committing.** A gate that surprises the player after they have queued is a failed run, not a choice. Show what an activity requires before the player enters.

The general point is that the same reward can be a bonus in easy content and a gate in hard content. Destinypedia's note that champions are guaranteed only in Heroic and harder content is exactly that. When you tune a tool, decide which it is, content tier by content tier.

## 5. Horizontal goals as endgame supply

Week 1 asked what fills the weeks after the gear chase ends. Horizontal rewards are one answer, and the frequency model tells you how many weeks they can fill.

Suppose a tool takes `h` hours to earn. A player will spend those hours only if the tool's value `b × f_i` clears their upgrade margin `u`, or if something else (a gate, a collection, a cosmetic) carries it. So the endgame hours that horizontal breadth really supplies are about

```
hours supplied ≈ h × (number of tools with b × f_i ≥ u)  +  hours carried by gates and collections
```

With `h = 10`, `b = 0.3`, `u = 5%` and the Zipf mix, only tools 1 and 2 clear the margin, so breadth supplies about 20 hours on value alone. With a full rotation (`λ = 1`), all six sit exactly at 5%, and breadth supplies about 60. The rotation did not add content. It changed which existing rewards count as goals.

This is the quiet strength of horizontal progression. It adds endgame hours without adding power creep. The gap ceiling stays at `1 + b` or below forever, however many tools you add. The cost moves into content design, since you must keep enough situations alive for each tool to matter.

## In-class activity (25 minutes)

Groups of three. You are designing a horizontal reward track of eight tools for an MMO's endgame. Each gives `b = 0.25` in its situation.

1. **(6 min)** Write down eight situations your game will have and estimate each one's frequency for a typical raider. Make the frequencies add to 1. Compute each tool's value and `N_eff`.
2. **(6 min)** Repeat the estimate for a typical PvP player. Which tools does each segment consider worth chasing at `u = 4%`?
3. **(8 min)** Choose one lever to make at least five tools worth chasing for both segments: a rotation (pick `λ`), changing where tools apply, or turning some tools into gates. Show the new values and the new `G_max`.
4. **(5 min)** Swap with another group. Find the tool in their design that no segment will chase and propose what should carry it (collection, cosmetic, gate, or cut).

Expected output: two frequency tables, your lever with before-and-after numbers, and the other group's orphan tool.

## Common misconceptions

- **"Horizontal rewards can't create a power gap."** They can, bounded by `G_max = (1 + b)/(1 + b f_1)`. Flattening the content mix raises it.
- **"Equal tooltip strength means equal value."** Value is `b × f_i`. The tooltip shows `b`. The content mix decides `f`.
- **"More situations always make breadth more valuable."** Only if players actually meet them. A seventh situation at 2% frequency adds a 2%-frequency tool, and it lowers every other situation's share slightly.
- **"Gates and bonuses are the same thing at different strengths."** They have opposite marginal shapes. Bonus values fall as the collection grows. Gate values can rise, making the last tool the most wanted.

## Check yourself

1. A game has five situations with frequencies 0.4, 0.3, 0.1, 0.1 and 0.1, and `b = 0.5`. Rank the tools by value. With `u = 6%`, which ones will players chase on value alone?
2. For the same game, compute `N_eff` and `G_max`. Then apply a rotation with `λ = 0.5` and recompute both.
3. An activity system has four counter types. Each activity needs exactly three of them, and all four triples are equally common. What share of activities does a player open with two counters, with three, and with four? What is the marginal value of each counter from the first to the fourth?
4. A designer adds a new raid in which situation 5 (from question 1) makes up half of all play for raiders. What happens to tool 5's value for raiders? What does GD203's expected-value test now say about tool 5?

<details>
<summary>Answers</summary>

1. Values `0.5 × f`: 20%, 15%, 5%, 5%, 5%. Only tools 1 and 2 clear 6%.
2. `Σ f² = 0.16 + 0.09 + 0.01 + 0.01 + 0.01 = 0.28`, `N_eff = 3.57`. `G_max = 1.5 / (1 + 0.5 × 0.4) = 1.5 / 1.2 = 1.25`. With `λ = 0.5`, `f' = 0.1 + 0.5 f`, giving 0.30, 0.25, 0.15, 0.15, 0.15. `Σ f'² = 0.09 + 0.0625 + 0.0225 × 3 = 0.22`, `N_eff = 4.55`. `G_max = 1.5 / (1 + 0.5 × 0.30) = 1.5 / 1.15 = 1.304`.
3. Two counters open none (every activity needs three). Three counters open exactly one of the four triples, 25%. Four counters open all, 100%. Marginal values are 0, 0, 25 points, 75 points.
4. For raiders, `f_5` becomes about 0.5 (the other situations share the remaining half), so tool 5's value rises from 5% to about 25%, the highest of any tool. By the expected-value test it is now far above the others for raiders. Yesterday's sidegrade is today's best-in-slot for that segment, and every raider will chase it.

</details>

## Lab / assignment hook

[Lab 03, horizontal reward track](../labs/lab03.md). You will implement the frequency model, the rotation and the gate model, estimate content mixes for two player segments from a play log, and tune a reward track so that every segment has enough tools worth chasing while `G_max` stays under a limit. It feeds the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Mythic+" (The War Within and Midnight eras, 2024-2026). Weekly-rotating affixes that reward group utility, coordination and focus; Fortified (trash) or Tyrannical (bosses) at keystone level 7, alternating weekly, with the other at level 10. https://warcraft.wiki.gg/wiki/Mythic%2B
- Warcraft Wiki, "Affix" (current). Mythic+ affixes are the same for all players each week and rotate on a fixed schedule with the weekly reset. https://warcraft.wiki.gg/wiki/Affix
- Guild Wars 2 Wiki, "Gliding" (current, through Visions of Eternity). Introduced with Heart of Thorns; usable in most open-world zones and expansion instanced content; not usable in PvP maps or Central Tyria instanced content such as dungeons. https://wiki.guildwars2.com/wiki/Gliding
- Guild Wars 2 Wiki, "Mastery" (current). Account-wide PvE progression for level-80 characters, including gliding and mounts. https://wiki.guildwars2.com/wiki/Mastery
- Destinypedia, "Champion" (Destiny 2, Shadowkeep onward, 2019-2026). Three champion types, each countered by a matching effect that stuns it; guaranteed in Heroic or harder content such as Nightfalls; each enemy race has champions of two of the three types. https://www.destinypedia.com/Champion
- Schreiber, I. (2010). *Game Balance Concepts*, Level 6, "Situational Balance". https://gamebalanceconcepts.wordpress.com/
- Zipf, G. K. (1949). *Human Behavior and the Principle of Least Effort*. Addison-Wesley. The origin of the `1/i` frequency shape used as an illustrative mix.

## Interactive spec: examples/w03-situation-weights.html

**The one insight.** Horizontal rewards that look identical on their tooltips have very different values, set by how often their situation occurs. A rotation can make more of them worth chasing, and the price is a larger (but always bounded) power gap.

**Layout.** Two linked bar charts side by side at 1280px, stacked at 390px, controls below, readout under the controls. A second tab, "Gates," holds the activity model.

**Left panel, "What the tooltip says."** One bar per tool `i = 1..n`, height `b` (as a percentage), labelled "+{b}% in situation i". All bars equal height by construction.

**Right panel, "What it's worth."** One bar per tool, height `b × f'_i` (percentage points of expected power), sorted by frequency. A dashed horizontal line at `u`. Bars below the line drawn in a muted colour with the label "below upgrade margin". Above the bars, a small row of the frequencies `f'_i` (3 decimals).

**Controls.**
- Mix preset: "Even", "Zipf" (default), "Custom" (six number inputs, normalised to sum 1 on change; show "normalised" when they did not sum to 1).
- `n` stepper 2 to 10 (default 6; Custom limited to the current `n`).
- `b` slider 0.05 to 1.00, step 0.05 (default 0.30).
- Rotation `λ` slider 0 to 1, step 0.05 (default 0).
- `u` slider 0% to 15%, step 0.5% (default 5%).
- Keyboard operable with labels and live values; respects `prefers-reduced-motion`.

**Readout.** `N_eff` (2 decimals), `G_max` (3 decimals), number of tools with `b f'_i ≥ u`, newcomer power `1 + b f'_1` (3 decimals), full-collection power `1 + b`, and a cumulative power table for owning the top `k` tools, `k = 1..n`.

**Tab 2, "Gates."** `m` counter types (stepper 2 to 5, default 3) and requirement size `r` (stepper 1 to `m`, default 2). Activities are all `C(m, r)` subsets of size `r`, equally common. A row of toggles marks which counters the player owns. Show the share of activities open, and a bar chart of marginal value when counters are added in order 1, 2, ..., `m` (share open with `j` counters is `C(j, r) / C(m, r)`). Caption: "Bonus values fall as you collect. Gate values can rise."

**Formulas.**
```
zipf_i   = (1/i) / H_n,   H_n = sum_{j=1..n} 1/j
f'_i     = lambda / n + (1 - lambda) * f_i
value_i  = b * f'_i
N_eff    = 1 / sum_i f'_i^2
G_max    = (1 + b) / (1 + b * max_i f'_i)
gate_open(j) = C(j, r) / C(m, r)        // j counters owned, any j of the m
```

**Test values.**
- Zipf, `n = 6, b = 0.3, λ = 0`: values 12.24, 6.12, 4.08, 3.06, 2.45, 2.04 (%); `N_eff = 4.02`; `G_max = 1.158`; with `u = 5%`, 2 tools clear the margin (12.24 and 6.12).
- Same with `λ = 0.5`: `f'_1 = 0.287`, `f'_6 = 0.117`, tool 6 value 3.52%; `N_eff = 5.34`; `G_max = 1.197`.
- `λ = 1` or Even: all values 5.00%; `N_eff = 6.00`; `G_max = 1.238`.
- Custom `f = (0.5, 0.25, 0.15, 0.10)`, `b = 0.4`: values 20, 10, 6, 4 (%); `N_eff = 2.90`; `G_max = 1.167`.
- Gates `m = 3, r = 2`: shares 0%, 0%, 33.3%, 100% for 0 to 3 counters; marginal values for the 1st, 2nd and 3rd counter 0, 33.3, 66.7. `m = 4, r = 3`: 0, 0, 0, 25%, 100%.
