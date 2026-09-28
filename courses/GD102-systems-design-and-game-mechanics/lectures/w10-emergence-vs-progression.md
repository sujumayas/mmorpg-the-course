# GD102 · Week 10 — Emergence vs Progression

**Why this matters:** Every hour of play in your game comes from one of two places. Either you wrote it, one room or quest at a time, or it falls out of rules combining in ways you never listed. The choice decides your content budget, your QA bill and whether players will ever surprise you. Most teams make it by accident.

**You will be able to:**
- Classify a game, or a part of a game, as emergence or progression using Juul's walkthrough test.
- Compute how many interactions a set of systemic objects produces, and compare that count with an authored-content plan of the same size.
- Estimate the untested share of an emergent system for a given QA budget.
- Design a hybrid structure and justify which parts are authored and which are systemic.

**Before class:** Juul, "The Open and the Closed: Games of Emergence and Games of Progression" (2002, free on jesperjuul.net, the whole paper). Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 2, "Emergence and Progression".

**Prerequisites from earlier courses:** From this course, [week 1, systems thinking](w01-systems-thinking-parts-relationships-emergence.md) (parts, relationships, emergence) and [week 9, progression systems](w09-progression-systems-skill-vs-power.md). Formal elements and rules from GD101 [week 2](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md) and [week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md), and dominant strategies from GD101 [week 11](../../GD101-introduction-to-game-design/lectures/w11-dominant-strategies-and-how-to-spot-them.md). Counting pairs uses the combinations idea from [MA102 week 1, sample spaces](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md).

**Interactive:** [Interaction grid](../examples/w10-interaction-grid.html). Keep it open during section 2.

---

## 1. Two ways to make a game last

Ask two people how they finished a game.

The first says, "I went to the lighthouse, got the brass key, used it on the cellar door, and pulled the lever behind the barrels." That is a list of actions. If you do them in order, you finish. Nothing about the list depends on who you are or what the game did that day.

The second says, "Early on I build economy and keep one unit back to scout. If they rush me I switch to defense. If they are greedy I attack before their second base finishes." That is a set of rules of thumb. It does not tell you what to click. It tells you how to think when the situation changes, because it will.

Jesper Juul turned this difference into a pair of terms in a 2002 conference paper, and they are the vocabulary for this week.

**Emergence** is a game structure where a small number of rules combine to produce a large number of situations. The designer writes the rules. The situations come from the rules meeting each other, and from players. Chess, poker, football and most multiplayer shooters are games of emergence.

**Progression** is a game structure where the designer lays out challenges in a sequence, and each challenge has a solution the designer intended. Adventure games, puzzle games with fixed levels, and quest chains are progression.

Juul gives a test you can run on any game. **Progression games have walkthroughs. Emergence games have strategy guides.** A walkthrough is the lighthouse list above. A strategy guide is the scouting advice. If the most useful document a player could write is a walkthrough, you are looking at progression. If it is a set of principles, you are looking at emergence.

Two more points from the paper matter for designers.

First, emergence is the older structure. Board games, card games and sports are almost all emergent. Juul calls progression the historically newer structure, and says it entered computer games through the adventure genre. Before computers, a designer could not easily hide a sequence of authored surprises inside a box.

Second, the two mix. Juul's main case study is *EverQuest*, which he describes as a game of emergence with progression structures embedded in it. The open world runs on combat and movement rules, and quests with fixed steps sit on top. He traces the pattern back to text MUDs. Almost every modern game you will work on is a hybrid, so the real design question is never "which one?" It is "which parts of this game should be which?"

### What each structure buys you

Progression gives the designer **control**. You decide the order of events, so you can pace difficulty, place story beats, teach one mechanic before the next, and guarantee that every player sees the room you are proud of. You can also test it. Each authored challenge has a known solution, so QA can play it, confirm the solution works and move on.

Emergence gives the designer **multiplication**. Each rule you add can combine with every rule already there, so the number of situations grows faster than the work you put in. Players find strategies you did not plan, the game stays fresh after hundreds of hours, and a community of experts forms around it. The cost is the mirror image of progression's benefit. You lose control of the order of events, and you cannot test every combination.

Those two sentences are claims. The worked example turns them into numbers.

## 2. Worked example: twenty objects or twenty puzzles?

### The hook

In *Deus Ex* (2000), the player carries proximity mines that stick to walls. They are weapons. Nobody on the team wrote a "climb" feature for them. Players found that a mine stuck to a wall is also a small ledge you can stand on, and that a column of mines is a ladder. They used it to reach rooftops and skip routes the level designers had planned. Juul uses this case in his 2002 paper, alongside rocket jumping in *Quake II*, where the blast that pushes enemies around also pushes the player who fired it upward.

Neither trick was designed. Each came from two rules meeting. "Mines stick to walls" met "the player can stand on solid objects." "Explosions push bodies" met "the player is a body." Where did those extra hours of play come from, and what did they cost?

### The model

Picture two ways to spend the same budget on a small puzzle-adventure game.

**Plan P (progression).** You author `k` puzzles. Each puzzle is one situation with one intended solution. The number of distinct situations is

```
S_P(k) = k
```

**Plan E (emergence).** You author `k` systemic objects. A systemic object is one that follows general rules rather than a script, for example a crate that burns, floats and can be stacked, whatever room it is in. Each pair of objects can meet, and each meeting is a potential situation. The number of distinct pairs is

```
S_E(k) = k × (k − 1) / 2
```

- `k` is the number of things you author (puzzles in plan P, objects in plan E).
- `S` is the number of distinct situations.
- `k × (k − 1) / 2` is the number of ways to choose 2 things from `k`, written `C(k, 2)`. You met it in MA102 as a count of outcomes.

The model makes one big simplification. It counts a pair as one situation. Real pairs can produce several situations or none, and triples of objects add more (`C(k, 3) = k(k − 1)(k − 2)/6`). The simplification is conservative. Adding triples only makes the gap wider.

There is a second number that matters just as much. Emergent designers rarely write a rule for each pair of objects. That would cost `C(k, 2)` rules, and the advantage would vanish. They give each object a few **properties** (burns, conducts, floats, heavy) and write rules between properties. Fire meets something that burns, it catches fire. Electricity meets something that conducts, the current spreads. With `m` properties, the number of property-pair rules is at most

```
R(m) = m × (m + 1) / 2
```

(pairs of different properties, plus each property with itself). That count does not grow with `k` at all. Add a new object, tag it "burns, floats", and it joins every rule already written for free.

Finally, testing. Suppose QA can check `B` pairs before ship. The share of pairs nobody has checked is

```
untested share = 1 − B / S_E(k)     (0 if B ≥ S_E(k))
```

In plan P, QA checks `k` puzzles and the untested share is zero as long as `B ≥ k`.

### Numbers you can check

Work these by hand before opening the interactive. For each `k`, compute `k(k − 1)/2`.

| Things authored `k` | Plan P situations | Plan E pairs `C(k,2)` | Plan E triples `C(k,3)` | New pairs from the last object |
|---|---|---|---|---|
| 2 | 2 | 1 | 0 | 1 |
| 4 | 4 | 6 | 4 | 3 |
| 6 | 6 | 15 | 20 | 5 |
| 8 | 8 | 28 | 56 | 7 |
| 10 | 10 | 45 | 120 | 9 |
| 12 | 12 | 66 | 220 | 11 |
| 16 | 16 | 120 | 560 | 15 |
| 20 | 20 | 190 | 1,140 | 19 |

Read the last column. In plan P every new puzzle adds one situation, whether it is your first or your fiftieth. In plan E the 20th object adds 19 new pairs, because it can meet all 19 objects already there. The value of each new object rises as the set grows. That is the quantitative meaning of Juul's "few rules, many variations."

Now the rules. With `m = 4` properties, `R = 4 × 5 / 2 = 10` property rules. Those 10 rules decide the outcome of all 190 object pairs at `k = 20`. That is 19 pairs per rule. Double the objects to 40 and the same 10 rules cover `40 × 39 / 2 = 780` pairs.

Now the bill. Give QA a budget of `B = 50` pair checks.

| `k` | Pairs | Untested share with B = 50 |
|---|---|---|
| 8 | 28 | 0% |
| 10 | 45 | 0% |
| 12 | 66 | 24.2% |
| 16 | 120 | 58.3% |
| 20 | 190 | 73.7% |
| 30 | 435 | 88.5% |

At 20 objects, three out of four pairs ship without a human ever having tried them. The same quadratic growth that gave you variety gave you the untested share. Those untested pairs are where the mine ladder lives. They are also where the bugs live.

### A visual you can move

Open the interactive. The left panel plots situations against `k` for both plans. Plan P is a straight line. Plan E is a curve that bends upward, and they cross between `k = 3` and `k = 4` (at `k = 3` both give 3; from 4 on, plan E is ahead). Drag the `k` slider and watch the gap open.

The right panel shows the same numbers a different way. It is a grid with one cell per pair of objects. Cells light up when the two objects share a property, which means a rule fires when they meet. Cells that QA has checked, up to your budget `B`, get a solid outline. Everything else is untested.

Keep `B` at 50 and drag `k` from 10 to 20. On the left, the curve climbs and looks like pure gain. On the right, the grid fills with cells nobody has outlined. Same numbers, two views. The left view is the pitch deck. The right view is the QA schedule.

Then change `m`, the number of properties. With `m = 1`, only objects that share that one property react, and most of the grid is dark, so you have many pairs but few interesting ones. With `m = 4` or more, most cells light up. The property count controls how much of the grid is alive. The rule count on the readout stays small the whole time.

### Cross-game recognition

**The Legend of Zelda: Breath of the Wild (2017).** Nintendo's team described a "chemistry engine" in their GDC 2017 talk, "Change and Constant." It defines the physical properties of most objects in the world and governs how they interact with the player and with each other. Rewrite that in our model and it is plan E with property rules. The designers did not script what happens when each specific weapon meets each specific fire source. They gave objects properties and wrote rules between properties, so a large `k` rides on a small `R`. The same talk showed the team building these rules in a simple 2D prototype before the 3D game existed, which is what a small `R` makes possible. You can test ten rules on paper. You cannot test 190 scripted pairs that way.

**Quake II and Deus Ex, from Juul.** Rocket jumping is one pair (explosion pushes bodies, player is a body). The mine ladder is one pair (mines stick to walls, player stands on solids). In our grid each is a single cell, and in each case the cell was untested when the game shipped, in the sense that nobody designed the use players found. Rocket jumping became a celebrated skill that competitive players practice. That is emergence working as intended. A designer who "fixes" such a cell deletes the kind of play that emergence exists to produce.

**Chess.** Six piece types. Pairs of types, counting a type with itself, number `6 × 7 / 2 = 21`. The rules fit on one page, and the game supports a library of strategy books that has grown for centuries. Nobody has ever written a chess walkthrough, because one cannot exist. The opponent changes the situation every move. Chess is the pure emergent end of the scale, and the reason it has no QA problem is that it has had millions of testers for centuries.

**EverQuest's quests.** Juul's hybrid case. The open world is plan E (combat, movement, grouping). The quests are plan P. Each is a fixed sequence of steps. A quest adds exactly one situation to the game, like a puzzle in our model, and it can be tested exhaustively. That is why quest content is expensive to produce per hour of play, and why MMOs pair it with systemic play that players repeat for years.

Four games, one question. When you look at any feature, ask: *does adding one more of these add one situation, or does it add a situation for every thing already in the game?*

### Eyes-open design judgment

Neither structure is better. Each is a trade you should make on purpose.

- **Choose emergence where replay matters.** Combat, economy, physics, social systems, anything the player will meet hundreds of times. The upward curve pays for itself only if players spend long enough in the system to find the pairs.
- **Choose progression where the first experience matters.** Tutorials, story beats, set pieces, the first hour. You want to guarantee what the player sees, in what order.
- **Write rules between properties, not between objects.** This is the move that keeps `R` small. If your design document has a row for "wooden shield meets fire arrow," you are writing plan P with extra steps.
- **Budget QA for the curve, not the line.** A systemic game with 30 objects has 435 pairs. Your schedule must either test by property rule (10 rules, each checked against a sample of objects) or accept a large untested share and plan to patch what players find.
- **Decide in advance what you will do with discovered pairs.** Keep exploits that create skill (rocket jumping). Fix pairs that break a progression gate you care about, or that create a dominant strategy (GD101 week 11). Write the policy down before launch. Otherwise you will decide under pressure, one forum thread at a time.
- **Beware emergence inside progression gates.** A mine ladder is harmless in an open level. It is a problem if the story assumed you could not reach the roof yet. The more progression you stack on top of emergent rules, the more of your untested cells become sequence breaks.

### Check this example

1. Your prototype has 14 systemic objects. How many object pairs are there? How many does the 15th object add?
2. You have 5 properties. What is the maximum number of property rules? How many object pairs does each rule cover, on average, at `k = 25`?
3. QA can test 80 pairs. At what `k` does the untested share first exceed 50%?

<details>
<summary>Answers</summary>

1. `14 × 13 / 2 = 91` pairs. The 15th object adds 14 pairs (total 105).
2. `R = 5 × 6 / 2 = 15` rules. At `k = 25`, pairs `= 25 × 24 / 2 = 300`, so 20 pairs per rule.
3. You need `C(k, 2) > 160`. `C(18, 2) = 153`, `C(19, 2) = 171`. So at `k = 19`, with `1 − 80/171 = 53.2%` untested.

</details>

## 3. Progression, looked at honestly

Progression gets called the lesser structure in some design writing. That is a mistake. It has its own mechanics and its own math, and the linear cost line in section 2 is not a flaw. It is the price of a guarantee.

**Gates and keys.** Progression is built from **gates**, things that block the player, and **keys**, things that open gates. A key can be an item (the brass key), an ability (double jump), knowledge (the code on the painting) or a stat threshold (level 20). The designer arranges gates so the player meets content in the intended order. Adams and Dormans treat these as the basic parts of progression and diagram them as a graph of locks and keys. Lab 10 puts one locked gate in a systemic room so you can see what happens to it.

**Content consumption.** An authored puzzle is used up when it is solved. A player who knows the solution gets little from a second play. So the useful life of plan P content is roughly one playthrough, and the play-hours you get are

```
hours_P ≈ k × (average minutes per challenge) / 60
```

If a puzzle takes 10 minutes and your team can build 3 puzzles a week, a 30-week production gives 90 puzzles and about 15 hours. Doubling the hours means doubling the team or the schedule. That linear relationship is why progression-heavy games are expensive per hour and why their teams plan content in spreadsheets of rooms, levels and quests.

**What progression does that emergence cannot.** It can tell a story with a structure. It can make sure the player learns mechanic A before mechanic B, so B can assume A. It can deliver a moment of surprise at a place and time the designer chose. Emergent systems can surprise players too, but not on schedule.

**The walkthrough is a design signal.** When players publish walkthroughs for your game, that tells you where your progression is. When players publish tier lists and build guides, that tells you where your emergence is. Search for both before a postmortem. The documents your players wrote are a cheap map of which structure they actually experienced, which may not be the one you designed.

## 4. Designing the hybrid

Most games you will ship combine the two structures. Three common patterns:

**Emergent world, embedded progression.** Juul's *EverQuest* pattern. A systemic world (combat, movement, economy) with authored quests placed in it. The quests give direction and pacing. The systems give replay. The risk is the one from section 2. A quest that assumes the player cannot yet reach a place can be broken by any systemic trick that reaches it.

**Authored sequence, emergent encounters.** A fixed order of levels, each built from systemic parts. The level designer controls where the player goes. Inside a room, the player combines objects freely. This is common in immersive sims and action games. The designer tests each level's intended path and accepts that the room holds more solutions than were planned.

**Emergent core, progression as unlocks.** A single systemic core that players repeat (a match, a run, a raid), with progression delivered as new objects added to the core over time. Each unlock is a new `k`, and by section 2's table, each one adds more pairs than the one before. This is why roguelikes and competitive games can make a small unlock feel large. It is also why each new unlock needs more testing than the last. Week 9's progression systems (skill versus power) sit on top of this pattern, and GD203 week 14 on [horizontal and vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) follows it into the numbers of power growth.

A practical way to design a hybrid is to write two lists before you write any content.

1. **Guarantees.** What must every player see, learn or feel, in what order? These go in progression.
2. **Replays.** What will players do more than twenty times? These go in emergence, built as properties and rules.

Then check the boundary between the lists. For each guarantee, ask which systemic tricks could skip or break it. If the answer is "any of 190 untested pairs," either make the gate robust (a story gate rather than a physical wall) or accept the break as a feature.

## 5. Emergence as a system property

This course is about systems, so tie Juul's terms back to week 1. There you defined emergence as behavior of the whole that no single part has. Juul's emergence is the same idea applied to play. No single rule in *Deus Ex* says "the player can climb walls." The climb exists only in the relationship between two rules.

That link explains why emergence resists planning. You design parts. The situations live in the relationships. With `k` parts there are `C(k, 2)` relationships and each can host one. When you plan an emergent game, you design parts and relationships with the confidence you would give a single part, and you design the whole with the humility of someone who knows they cannot enumerate it. Next week (intransitive mechanics) shows one family of relationships you can analyze completely. Week 12 goes the other way, to systems of simple rules whose results you can only find by running them.

## In-class activity (25 minutes)

In groups of three, you receive a card list of 12 objects for a small top-down puzzle game (crate, rope, torch, puddle, iron bar, balloon, oil barrel, grass patch, stone block, fan, magnet, ice block) and a blank 12 × 12 grid.

1. Choose four properties that you think will produce the most interesting pairs. Tag each object with zero to three of them. (5 min)
2. Write the property rules. You may write at most `m(m + 1)/2 = 10`. (5 min)
3. Fill the upper triangle of the grid. Mark each of the 66 cells as "reacts" or "nothing" by applying your rules, not by imagining the pair. (8 min)
4. Pick the three pairs you think are most surprising. Could any of them break a door that is meant to be locked until the player finds a key? (4 min)
5. Report to the room: your properties, the share of the grid that reacts, and one pair you would keep and one you would patch. (3 min)

Expected output: a filled grid with a percentage of reacting cells, a list of 10 or fewer rules, and a keep/patch decision with a reason.

## Common misconceptions

- **"Emergent means random."** Emergent situations come from rules meeting, and the rules are usually deterministic. Chess has no randomness and is the textbook emergent game. Randomness can add variety, but it is a different tool (GD101 week 10).
- **"Progression is lazy design and emergence is the real thing."** Progression buys control and testability, and many of the best-remembered moments in games are authored. The linear cost is a price, not a defect.
- **"More objects always means more fun."** More objects means more pairs. Pairs are fun only if the rules make them different from each other. With too few properties, most cells of the grid are dead, and players see a large list of things that all behave the same.
- **"We can test all the combinations if we try hard."** At 30 objects you have 435 pairs and 4,060 triples. Test the rules, sample the pairs, and plan for players to find the rest.

## Check yourself

1. A designer adds 6 new systemic objects to a game that already has 18. How many new object pairs does the update create? How does that compare with adding 6 authored quests?
2. Apply Juul's test to a game you played this month. What document would players write about it? Is there any part of it where the other kind of document would be more useful?
3. A team has 8 properties. What is the maximum number of property rules? Is that a reason to cut properties, and what would you lose if you did?
4. QA can test 120 pairs before launch. The team wants to ship with at most 40% of pairs untested. What is the largest `k` they can ship?

<details>
<summary>Answers</summary>

1. Before: `18 × 17 / 2 = 153`. After: `24 × 23 / 2 = 276`. New pairs `= 123`. Six quests add six situations. The systemic update gives about 20 times as many new situations, and about 20 times as much to test.
2. Answers vary. A good answer names the document (walkthrough or strategy guide), gives a concrete example of its contents, and points to a mode or section where the other structure applies, such as the story campaign of a competitive shooter.
3. `8 × 9 / 2 = 36` rules at most. That is still small next to the object pairs it covers, so it is not by itself a reason to cut. Cutting properties shrinks the share of the grid that reacts. You lose variety between pairs and gain testability. The decision depends on how many objects you plan.
4. Untested share `1 − 120 / C(k,2) ≤ 0.4` means `C(k,2) ≤ 200`. `C(20,2) = 190` and `C(21,2) = 210`. So `k = 20`.

</details>

## Lab hook

**Lab 10, emergence audit** ([`labs/lab10.md`](../labs/lab10.md)). You take a 16-object property sheet, build the interaction matrix in a spreadsheet, compute pairs, rules and untested share under two QA budgets, playtest a paper version for 20 minutes, and write a keep/patch policy for every surprising pair your testers found. The property sheet you build feeds your final system design document.

## Sources

- Juul, J. (2002). "The Open and the Closed: Games of Emergence and Games of Progression." In F. Mäyrä (ed.), *Computer Games and Digital Cultures Conference Proceedings*, Tampere University Press. Online at jesperjuul.net. Source of the two definitions, the walkthrough versus strategy guide test, the claim that emergence is the older structure and progression entered through adventure games, the *Quake II* rocket jump and *Deus Ex* proximity mine examples, and the *EverQuest* hybrid case.
- Juul, J. (2005). *Half-Real: Video Games between Real Rules and Fictional Worlds*. MIT Press. Later book-length treatment of the same distinction.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 2 on emergence and progression, and chapter 11 for the lock-and-key treatment of progression.
- Fujibayashi, H., Dohta, T. & Takizawa, S. (2017). "Change and Constant: Breaking Conventions with *The Legend of Zelda: Breath of the Wild*." GDC 2017 (GDC Vault). Speakers and title confirmed on the GDC Vault listing.
- Wikipedia, "The Legend of Zelda: Breath of the Wild" (accessed September 2026). Describes the chemistry engine as defining the physical properties of most objects and governing their interactions, and the GDC 2017 prototype demonstration.
- Chess piece count (six types) is common knowledge; the pair count is our calculation.

## Interactive spec: examples/w10-interaction-grid.html

**The one insight:** the curve that makes an emergent system rich is the same curve that makes it untestable. Plan E's situations and plan E's untested pairs grow together as `k(k − 1)/2`, while the number of rules stays small.

**Layout.** Two linked panels. Side by side at 900px and wider, stacked at 390px. Controls sit above the panels. A number readout sits under the panels.

**Left panel, "Situations vs things authored."** Line chart. x-axis `k` from 1 to 30. y-axis situations, linear, auto-scaled to the larger of `S_E(k_max_shown)` and 50. Two lines: plan P `y = k` (solid, accent color 2) and plan E `y = k(k − 1)/2` (solid, accent color 1). Optional toggle "show triples" adds a dashed line `y = k(k − 1)(k − 2)/6`, clipped at the top of the chart with a small "off chart" marker. A vertical marker at the current `k` with both values labeled. A shaded band under plan E marks the untested pairs, from `y = min(B, S_E)` up to `S_E`, so the student sees the untested region grow on the same chart.

**Right panel, "Pair grid."** A `k × k` grid, upper triangle only (cells `i < j`), with row and column labels 1..k. Cell fill: the number of properties objects `i` and `j` share among the first `m` properties. 0 shared means a neutral background ("no rule fires"). 1, 2, 3+ shared use three increasing tints of accent 1 ("rule fires"). Tested cells: the first `B` cells in row-major order over the upper triangle (row 1 left to right, then row 2, and so on) get a solid 2px outline. Untested reacting cells get a diagonal hatch overlay so they stand out without color alone.

**Object properties.** Properties indexed `j = 0..5`, names shown in a legend: burns, conducts, floats, heavy, wet, sharp. Object `i` (1-based) has property `j` if bit `j` of `(i × 37) mod 64` is 1. Only the first `m` properties are active.

**Controls.**
- `k`, objects: range 2 to 30, step 1, default 20.
- `m`, properties: range 1 to 6, step 1, default 4.
- `B`, QA budget in pairs: range 0 to 450, step 10, default 50.
- Toggle "show triples", default off.
- All controls keyboard accessible with visible numeric values. Grid cells are focusable with arrow-key navigation, and focusing a cell shows "Object i × object j, shares: burns, floats, tested: no".

**Readout.** `k`; plan P situations `k`; plan E pairs `k(k − 1)/2`; triples `k(k − 1)(k − 2)/6`; property rules `R = m(m + 1)/2`; pairs per rule `S_E / R` to one decimal; reacting pairs (share at least one active property) as count and percent; untested share `max(0, 1 − B / S_E)` as percent to one decimal.

**Test values (builder must reproduce).**
- `k = 20`: pairs 190, triples 1,140, plan P 20.
- `k = 20, B = 50`: untested 73.7%. `k = 12, B = 50`: 24.2%. `k = 10, B = 50`: 0.0%. `k = 30, B = 50`: 88.5%.
- `m = 4`: R = 10; at `k = 20`, pairs per rule 19.0. `m = 5`: R = 15.
- `k = 3`: both plans 3. `k = 4`: plan P 4, plan E 6.
- Object 1 under the bit rule: `37 mod 64 = 37 = 100101₂`, so properties 0, 2, 5 (burns, floats, sharp). Object 2: `74 mod 64 = 10 = 001010₂`, properties 1, 3 (conducts, heavy). They share nothing, so cell (1,2) is neutral for every `m`.

**First screen.** Load at the defaults (`k = 20, m = 4, B = 50`), so the left chart shows a wide gap between the lines and the right grid shows a large hatched region. Caption: "20 objects, 190 pairs, 10 rules. QA has tried 50 pairs."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes. Hatching and outlines carry meaning in addition to color. `prefers-reduced-motion` disables transitions. No game art, logos or item icons. Objects are numbered squares.
