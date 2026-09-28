# GD102 · Week 01 — Systems Thinking: Parts, Relationships, Emergence

**Why this matters:** Players remember the moment a game did something nobody scripted. They set a field on fire and rode the hot air over a wall, or dropped a metal sword next to an enemy during a storm. Those moments come from rules meeting each other, and a designer who can count and draw those meetings can plan for them instead of hoping for them.

**You will be able to:**
- Describe a game as a system of elements, relationships and a purpose, and say which part a proposed change touches.
- Draw an interaction graph for a small set of game elements and compute its rules, degrees and two-step chains.
- Predict how many new chains one added rule creates, and use that number to choose between two candidate rules.
- Label the links in a causal loop and compute whether the loop reinforces or balances.

**Before class:** Donella Meadows, *Thinking in Systems: A Primer* (2008), chapter 1, "The Basics," up to the section on stocks. Ernest Adams and Joris Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 2, "Emergence and Progression", the first two sections.

**Prerequisites from earlier courses:** GD101's formal elements (players, objectives, rules, resources, boundaries) and the MDA framework. See GD101 [week 2](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md), [week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) and [week 4](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md).

**Interactive:** [The chemistry set](../examples/w01-chemistry-set.html). Keep it open during section 2.

---

## 1. What a system is

In GD101 you described games with formal elements. You listed the players, the objective, the rules, the resources. That list tells you what a game is made of. It does not tell you what the game does when you run it. This course is about the second question.

Donella Meadows, an environmental scientist who wrote the standard short introduction to the field, describes a system as three things. There are **elements**, the parts you can point at. There are **interconnections**, the relationships that let one element change another. And there is a **function** or purpose, the thing the whole arrangement ends up doing. Her key observation is that the three are not equally important. You can swap most of the elements of a football team and it is still the same team. Change the rules that connect the players and you have a different sport.

Games work the same way. Here is a quick test you can run on any design.

- **Change an element.** Replace the knight in chess with a piece that moves identically but looks like a horse-drawn cart. Nothing about play changes.
- **Change a relationship.** Let the knight move only forward. The opening, the endgame, the value of every other piece all shift.
- **Change the purpose.** Make the goal "capture the most pieces in 30 moves" instead of checkmate. Players now play a different game on the same board with the same moves.

Designers new to systems spend most of their time on elements. They add a new weapon, a new enemy, a new resource. The number of elements is easy to see in a feature list. The relationships are where the play actually happens, and they are harder to see because they are not objects. This lecture gives you a way to see them and count them.

### Terms you will use all course

- An **element** is anything in the game that has a state: a patch of grass, a player's gold, a unit, a card in hand.
- A **relationship** (or **rule**, or **link**) says how one element's state changes another's. "Fire turns grass into burning grass" is a relationship between fire and grass.
- **Emergence** is behavior of the whole system that no single rule describes. Nobody wrote a rule called "ride burning grass over a wall." It happens because one rule makes fire spread through grass, another makes fire heat the air, and a third lets a glider rise in hot air.
- A **system boundary** is the line you draw around what you are modeling. Everything inside can change. Everything outside is treated as fixed input.

Adams and Dormans use emergence as one of the two big ways games produce play. The other is **progression**, where the designer lays out challenges in a sequence. A linear adventure game is mostly progression. Chess is almost pure emergence. Week 10 of this course returns to that split through Jesper Juul's version of it ([week 10](w10-emergence-vs-progression.md)). For now, notice that emergence is something you get from relationships, so if you want more of it, relationships are what you design.

## 2. Worked example: the chemistry set

### The hook

In *The Legend of Zelda: Breath of the Wild* (Nintendo, 2017), metal objects attract lightning during thunderstorms. Players learn this the hard way, by standing on a hill with a metal sword equipped. Then they learn the other side of it. You can throw a metal weapon next to an enemy and let the storm do the damage. Wooden weapons can light fires. None of this is a special puzzle. It comes from a set of rules the developers called the **chemistry engine**, which gives objects physical properties and defines how those properties affect each other. In their GDC 2017 talk the game's directors explained that they chose to increase the number of things in the world the player could interact with, rather than add more buttons and moves for the player.

That is a bet on relationships over elements. The rest of this section shows why it pays off, and what it costs, with one small model you can compute by hand.

### The model

Draw each element as a dot. Draw a line between two dots when a rule connects them. The picture is an **interaction graph**. We will use three numbers from it.

```
E    = number of rules (lines)
d(v) = degree of element v = number of rules that touch v
C2   = number of two-step chains = sum over every element v of d(v) × (d(v) − 1) / 2
```

A **two-step chain** is a path a–b–c where one rule links a to b and another links b to c. It is the smallest unit of emergence, two rules meeting through a shared element. In the hook, lightning–metal–enemy is a two-step chain. The designers wrote "lightning strikes metal" and "lightning hurts creatures." The chain "use a sword to kill an enemy with weather" was never written down.

Why the formula works. A chain is decided by its middle element and a choice of two of that element's rules. An element with `d` rules has `d × (d − 1) / 2` ways to pick two of them.

One more result follows directly and it is the one designers use. If you add a new rule between elements `u` and `v`, which already have degrees `d(u)` and `d(v)`, the number of new two-step chains is

```
new chains = d(u) + d(v)
```

The new line can extend each of `u`'s existing rules through `u`, and each of `v`'s existing rules through `v`. Every rule you add is worth the connectedness of the two elements it joins.

### Numbers you can check

Start with a toy element set. This is our own design, loosely inspired by the kinds of properties a chemistry engine uses. It is not a list of any shipped game's rules.

Six elements: Fire, Grass, Wind, Water, Metal, Lightning. Six rules:

| Rule | Meaning in our toy game |
|---|---|
| Fire–Grass | fire spreads through grass and burns it |
| Fire–Wind | wind pushes fire; fire makes rising hot air |
| Fire–Water | water puts fire out |
| Fire–Metal | fire heats metal, which then burns whoever holds it |
| Water–Lightning | lightning electrifies water |
| Metal–Lightning | metal attracts lightning |

Count the degrees.

| Element | Rules touching it | d | d(d−1)/2 |
|---|---|---|---|
| Fire | Grass, Wind, Water, Metal | 4 | 6 |
| Grass | Fire | 1 | 0 |
| Wind | Fire | 1 | 0 |
| Water | Fire, Lightning | 2 | 1 |
| Metal | Fire, Lightning | 2 | 1 |
| Lightning | Water, Metal | 2 | 1 |
| **Total** | | **12** | **9** |

The degrees add to 12, which is twice the number of rules, because each rule touches two elements. That is a free check on your counting. Six rules produce nine two-step chains. Six of the nine run through Fire. Some of them are play you would want, like Grass–Fire–Wind (wind drives a grass fire toward the enemy camp). Some are play you might not, like Water–Fire–Metal (dousing a heated sword so you can pick it up again), which you now have to decide about.

Now the designer has budget for one more rule. Two candidates:

- **Grass–Wind**, "wind flattens grass and reveals hidden items." Degrees before adding are 1 and 1, so it creates `1 + 1 = 2` new chains.
- **Fire–Lightning**, "lightning sets things on fire." Degrees are 4 and 2, so it creates `4 + 2 = 6` new chains.

Both cost roughly the same to implement. One triples the other's contribution to the possibility space. Check it by recounting. After adding Fire–Lightning, Fire has degree 5 (10 pairs) and Lightning degree 3 (3 pairs). The total becomes `10 + 0 + 0 + 1 + 1 + 3 = 15`, which is `9 + 6`. It matches.

Finally, look at the extreme case where every element is linked to every other. With `n` elements that gives:

| Elements n | Rules E = n(n−1)/2 | Chains C2 = n(n−1)(n−2)/2 | Chains per rule |
|---|---|---|---|
| 3 | 3 | 3 | 1 |
| 4 | 6 | 12 | 2 |
| 5 | 10 | 30 | 3 |
| 6 | 15 | 60 | 4 |
| 7 | 21 | 105 | 5 |
| 8 | 28 | 168 | 6 |

Rules grow with the square of the element count. Chains grow with the cube. Each rule is worth `n − 2` chains, so every rule becomes more valuable as the system grows. This is the arithmetic behind the claim that interconnected systems produce play multiplicatively. It is also a warning, as the next steps show.

### A visual you can move

Open `examples/w01-chemistry-set.html`. The left panel is the six-element graph with the six starter rules. The right panel plots two lines as you add rules one at a time: rules written (it climbs by exactly one each time) and chains created (it climbs by a different amount each time). Hover over any empty pair and the panel previews how many chains that rule would add. Try adding rules to Grass and Wind first, then to Fire. The rules line looks the same both times. The chains line does not. Then press "Connect everything" and watch the chain count reach 60.

### Cross-game recognition

The graph gives you one question to ask of any game. Where are the high-degree elements, and what happens when you connect to them?

**Minecraft.** In current Java Edition, flowing water meeting flowing lava makes cobblestone. A lava source block touched by water becomes obsidian, and lava flowing down onto water makes stone. In our graph language, Water and Lava are two elements with a rule between them, and the rule's output is a third element, a block the player can mine. Players combined that one rule with the rules for how liquids flow and built "cobblestone generators," small machines that produce an endless supply of a building material. Nobody at Mojang needed to write a rule called "infinite cobblestone." It is a chain.

**Divinity: Original Sin 2 (Larian, 2017).** Combat takes place on a map where water, ice, oil and fire lie on the ground as surfaces, and spells interact with them. Skills used in combination can cause large damage or unusual effects. Here the high-degree elements are the surfaces themselves: nearly every spell school has a rule for at least one surface, so each new spell the designers add connects to a hub and creates many chains at once. The result is a tactical game where positioning around puddles matters as much as which spell you pick.

**Breath of the Wild, again.** The lightning example is a chain through Metal. Metal has rules with Lightning, with the player's inventory and with physics (you can throw it). Adding "lightning strikes metal" joined two elements that were already well connected, so it produced many chains for the cost of one rule.

Three games, three genres, one structure. When you study a game with a reputation for emergent play, draw its interaction graph for ten minutes. You will almost always find a small number of hub elements with many rules each.

### Design judgment, with eyes open

The chain count is a measure of possibility, not of quality. Here is what to decide on purpose.

- **Every chain is also a test case.** The Water–Fire–Metal chain above is harmless. In a real game one chain in a hundred is an exploit, a crash or a softlock. Testing cost grows with `C2`, not with `E`. A team that adds rules to hubs late in production is adding chains faster than it can test them.
- **Players must be able to predict chains.** Emergence only feels good when the player could have guessed the result. "Metal attracts lightning" works because players already believe it. If your rules are arbitrary, a high chain count produces confusion, not creativity. Keep rules consistent across every element they touch.
- **Choose your hubs.** Fire in our toy set, surfaces in Divinity, metal in the storm example. A hub is where the designer concentrates emergence. Decide which elements should be hubs based on what you want players to think about, then give them rules first.
- **Some games want few chains.** A puzzle game with one intended solution per room, or a story game that must hit fixed beats, is hurt by a high chain count. That is the progression side of Adams and Dormans's split. Pick where on the dial you want to be.

### Check yourself (worked example)

1. Add Grass–Wind to the original six-rule set. How many chains do you now have? Then add Fire–Lightning. What is the new total? Would the total change if you added the two rules in the opposite order?
2. A designer has a set where one element has degree 7 and all others have degree 1 or 2. Write one sentence about what players of that game will spend their time doing.

<details>
<summary>Answers</summary>

1. Grass–Wind adds `1 + 1 = 2`, so 11. Grass and Wind now each have degree 2. Fire–Lightning then adds `d(Fire) + d(Lightning) = 4 + 2 = 6`, giving 17. In the opposite order you get `+6` then `+2`, the same 17. The order cannot change the final `C2`, which depends only on the finished graph. It only changes how the credit is split between the two rules when they share an element.
2. With `d = 7` that element sits in the middle of `7 × 6 / 2 = 21` chains, far more than any other element, so nearly all emergent play will route through it. Players will learn that element first and build strategies around it.

</details>

## 3. Loops: when a chain comes back

A chain that returns to where it started is a **loop**. Loops are the most important structures in this course. Weeks 3 and 4 are about the two kinds, and weeks 5 and 6 teach you to draw them in the Machinations notation.

To reason about a loop you need a little more than lines. Give each link a direction and a sign.

- A **+ link** from A to B means "more A causes more B" (or less A causes less B). More grass on fire causes more hot air.
- A **− link** from A to B means "more A causes less B." More water causes less fire.

The sign of the whole loop is the product of its link signs. Count the minus signs.

- **Even number of minus signs (including zero): reinforcing loop.** A change goes around the loop and comes back bigger in the same direction. This is **positive feedback**. More gold buys more gold mines, which make more gold.
- **Odd number of minus signs: balancing loop.** A change goes around the loop and comes back pushing the other way. This is **negative feedback**. More heat makes more sweat, which makes less heat.

"Positive" and "negative" here mean the direction of the effect, not good and bad. A positive loop can be a disaster (a losing player keeps losing faster). A negative loop can be what makes a game fair.

A worked micro-example from our toy set, with one more rule added: burning grass heats the air (+), hot air makes wind (+), wind spreads the fire into more grass (+). Three plus signs, zero minus signs, so it reinforces. Left alone, a grass fire in this toy game grows until it runs out of grass. Now add a rain rule: fire makes smoke (+), smoke makes rain clouds in this toy world (+), rain reduces fire (−). One minus sign, so it balances. Which loop wins decides whether fires in your game sweep the map or fizzle. That is exactly the kind of question the rest of this course teaches you to answer with numbers.

The graph from section 2 and the signed loop here are two views of the same thing. The graph tells you how many ways rules can meet. The signed loop tells you what happens when they meet in a circle.

## 4. Where to draw the boundary

Every model leaves things out. The choice of what to leave out is a design decision, and it is where most systems arguments actually happen.

Take a simple question: "Is gold inflating in our MMO?" If your boundary includes only monster drops and vendor sales, you might conclude it is fine. Move the boundary to include players trading with each other, and you find that trades move gold between players without creating any. Move it again to include players who quit with full bags, and you find a large amount of gold leaving the economy. Each boundary gives a different answer. None is wrong. They answer different questions.

Three rules of thumb for setting a boundary:

1. **Put inside everything that the thing you care about can change.** If player gold affects item prices and item prices affect how much players farm, both belong inside.
2. **Put outside anything that changes much more slowly than your question.** For a single match, the player's skill is outside. For a two-year MMO economy, it is inside.
3. **Name the boundary out loud** in your design document, so a colleague who disagrees with your conclusion can see whether they actually disagree about the boundary.

The player is an element too. In almost every game system, the player is the element with the most rules, because the player reads the state and chooses actions based on it. When you later find that a system "behaves" in a way the numbers did not predict, the usual reason is that you left the player's decisions outside the boundary.

## 5. Levels of description

MDA, which you met in GD101, splits a game into mechanics (the rules), dynamics (the behavior that results when the rules run with players) and aesthetics (what players feel). Systems thinking gives you the tools to get from mechanics to dynamics without running a full playtest every time.

You will work at three levels in this course.

- **The element level.** Single rules. "Fire spreads to adjacent grass at one tile per second."
- **The structure level.** Graphs, chains and loops. "Fire is a hub with a reinforcing loop through wind."
- **The behavior level.** What the system does over time. "Fires spread fast and cover a third of the map before rain stops them."

The mistake to avoid is jumping from the element level to the behavior level by intuition. Two rules that each look harmless can form a reinforcing loop that runs away. Two rules that each look strong can form a balancing loop that makes both useless. The structure level is where you catch that, on paper, before anyone builds it.

Next week adds the first quantitative tool for the behavior level, stocks and flows. A stock is anything that accumulates, like gold, health or fire tiles. A flow is the rate that fills or drains it. Once you can write a stock and its flows, you can simulate a system in a spreadsheet.

## In-class activity (25 minutes)

Work in pairs. Pick a game you both know well that has at least six interacting elements. Good choices include a survival game, a tactics game with terrain, or a card game with keywords.

1. (8 min) List exactly six elements. Draw the interaction graph with every rule you can name. Write each rule as one short sentence.
2. (5 min) Compute each element's degree, the total `E`, and `C2`. Check that the degrees add to `2E`.
3. (5 min) Find the hub. Name one two-step chain through it that the game's designers probably intended, and one they might not have.
4. (5 min) Propose one new rule that creates at least four new chains, and one that creates at most two. Say which you would ship and why, in two sentences.
5. (2 min) Swap sheets with another pair and check their arithmetic.

**Expected output:** one page with the graph, a degree table, `C2`, the two chains, and the two candidate rules with their chain counts.

## Common misconceptions

- **"More content means more emergence."** Content adds elements. Emergence comes from relationships between them. Ten new enemies with no new rules add no chains. One new rule on a hub can add many.
- **"Positive feedback is good and negative feedback is bad."** The signs describe direction. A reinforcing loop amplifies whatever change enters it, including losses.
- **"Emergent means random."** A chemistry-engine game is fully deterministic. The same inputs give the same outputs. Emergence means the result is not written in any single rule, not that it is unpredictable in principle.
- **"The system is what's in the code."** The system includes the player's decisions. A rule that nobody has a reason to use contributes nothing to play, whatever the graph says.

## Check yourself

1. A game has 5 elements with degrees 3, 3, 2, 1 and 1. How many rules does it have, and how many two-step chains?
2. In the same game, you can add a rule between the two degree-3 elements or between the two degree-1 elements. How many chains does each add?
3. A loop has the links: more enemies (+) more loot dropped, more loot (+) better gear, better gear (−) fewer enemies left alive. Is it reinforcing or balancing? What does that predict about enemy counts over time?
4. A colleague says "our crafting system has 40 recipes, so it must be deep." What question would you ask, using this lecture's model?

<details>
<summary>Answers</summary>

1. Degrees add to 10, so `E = 5`. Chains are `3 + 3 + 1 + 0 + 0 = 7` (from `3×2/2`, `3×2/2`, `2×1/2`).
2. Between the degree-3 elements: `3 + 3 = 6` new chains. Between the degree-1 elements: `1 + 1 = 2`.
3. One minus sign, so the loop balances. As enemies increase, players gain loot and gear and kill enemies faster, which pulls the enemy count back down. It predicts enemy numbers settle toward a level rather than growing without limit (assuming this is the only loop).
4. How many recipes share ingredients or outputs with other recipes? Recipes are rules. Depth depends on how they connect. Forty recipes that each use unique ingredients have degree 1 everywhere and produce almost no chains. Ask for the degree of the most-used ingredient.

</details>

## Lab hook

**Lab 01: Interaction audit** ([labs/lab01.md](../labs/lab01.md)). Map a shipped game's interaction graph as an adjacency matrix in a spreadsheet, compute degrees and chains automatically, and write a short proposal for one new element.

## Sources

- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 1, the definition of a system as elements, interconnections and function, and the observation that changing interconnections or purpose changes a system more than changing elements. Paraphrased.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 2, emergence and progression as two sources of gameplay. Paraphrased.
- Fujibayashi, H., Takizawa, S. & Dohta, T. (2017). "Change and Constant: Breaking Conventions with *The Legend of Zelda: Breath of the Wild*." GDC 2017 (GDC Vault session listing). Speakers and topic.
- Wikipedia, "The Legend of Zelda: Breath of the Wild" (accessed September 2026). The chemistry engine defines physical properties of objects and their interactions; metal objects attract lightning during thunderstorms and can be thrown at enemies to draw it; wooden weapons can light fires; the developers aimed to increase the events players could interact with rather than the player's actions. Nintendo Switch and Wii U release, 2017.
- Minecraft Wiki, "Cobblestone" (Java Edition, accessed September 2026). Flowing water meeting flowing lava makes cobblestone; a lava source touched by water becomes obsidian; lava flowing onto water from above makes stone.
- Wikipedia, "Divinity: Original Sin II" (accessed September 2026). Larian Studios, 2017. Players and enemies use environmental elements such as water, ice, oil and fire in turn-based combat, and skills used in combination produce large effects.
- Hunicke, R., LeBlanc, M. & Zubek, R. (2004). "MDA: A Formal Approach to Game Design and Game Research." AAAI Workshop on Challenges in Game AI. Mechanics, dynamics, aesthetics.

## Interactive spec: examples/w01-chemistry-set.html

**The one insight:** adding a rule always adds exactly one to the rule count, but it adds `d(u) + d(v)` two-step chains, so the same authoring effort is worth far more when it connects to a hub.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (graph on top).

- **Left panel, "The system":** six labeled nodes placed on a circle: Fire, Grass, Wind, Water, Metal, Lightning (plain text labels in generic circles, no game art). Rules are lines between nodes. Below it, a 6×6 symmetric toggle matrix with the same elements on both axes; clicking a cell (or pressing Space/Enter on it) adds or removes that rule, and the graph updates. Diagonal cells are disabled. Each node shows its degree `d` in a small badge. The node or nodes with the highest degree get the accent color and the label "hub."
- **Right panel, "What each rule bought":** a step chart with the horizontal axis "rules added, in order" (0, 1, 2, ...) and two series on the same vertical axis: `E` (rules, a staircase that rises by exactly 1 each step) and `C2` (chains). Under the chart, a log list of the last 8 actions, each line like "Added Fire–Lightning: +1 rule, +6 chains (4 + 2)". Removing a rule logs a negative line.

**Hover/focus preview.** When an empty matrix cell or a pair of nodes is hovered or focused, show a ghost dashed line in the graph and the text "Adding X–Y would create d(X) + d(Y) = N new chains." This must work with keyboard focus, not only the mouse.

**Controls (keyboard accessible, labeled):**

1. The toggle matrix described above.
2. Button "Reset to starter set" (the six rules below).
3. Button "Clear all rules."
4. Button "Connect everything" (adds missing rules one at a time in row order, with a 150 ms step animation unless `prefers-reduced-motion`, in which case add them all at once and log each).
5. A chain list toggle "Show chains" that lists every two-step chain as "a – b – c" grouped by middle element.

**Formulas.**

- `E` = number of selected pairs.
- `d(v)` = number of selected pairs containing `v`.
- `C2 = Σ_v d(v)(d(v) − 1)/2`.
- Chains added by rule u–v = `d(u) + d(v)` using degrees before the addition. On removal, chains lost = `(d(u) − 1) + (d(v) − 1)` using degrees before removal.
- Readout also shows `Σ d(v) = 2E` as a check line.

**Starter set (default first screen):** Fire–Grass, Fire–Wind, Fire–Water, Fire–Metal, Water–Lightning, Metal–Lightning.

**Test values:**

| State | E | Degrees (F, G, Wi, Wa, M, L) | C2 |
|---|---|---|---|
| Starter set | 6 | 4, 1, 1, 2, 2, 2 | 9 |
| Starter + Grass–Wind | 7 | 4, 2, 2, 2, 2, 2 | 11 |
| Starter + Fire–Lightning | 7 | 5, 1, 1, 2, 2, 3 | 15 |
| Starter + both | 8 | 5, 2, 2, 2, 2, 3 | 17 |
| All 15 rules | 15 | 5, 5, 5, 5, 5, 5 | 60 |
| Empty | 0 | 0, 0, 0, 0, 0, 0 | 0 |

Preview on the starter set: hovering Grass–Wind must read "1 + 1 = 2"; hovering Fire–Lightning must read "4 + 2 = 6".

**First screen:** the starter set drawn, Fire highlighted as the hub, the readout "6 rules, 9 chains, 6 of them through Fire," and the Fire–Lightning preview shown by default next to the Grass–Wind preview as a side-by-side comparison ("+2 vs +6") so the insight is visible before any interaction.
