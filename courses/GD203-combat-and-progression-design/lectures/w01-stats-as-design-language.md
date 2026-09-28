# GD203 · Week 01 — Stats as Design Language

**Why this matters:** Every number on a character sheet is a sentence you, the designer, are saying to the player. If you don't know what each stat means in terms of damage dealt or seconds survived, players will work it out before you do, and they will find the stats you forgot to price.

**You will be able to:**
- Distinguish primary, derived and hidden stats, and draw the dependency graph of a stat sheet.
- Compute the exchange rate of a stat into an outcome (damage per second, health, mana) for different classes.
- Compute the real value of an additive or multiplicative modifier at any point in a build, and explain why identical tooltips can be worth very different amounts.
- Critique a stat sheet for dead stats, overlapping stats and unreadable numbers.

**Before class:** Schreiber, *Game Balance Concepts*, Level 1 ("Intro to Game Balance") and Level 2 ("Numeric Relationships"); Schreiber & Romero, *Game Balance* (2021), chapter 9 (characters), first half.

**Prerequisites from earlier courses:** functions as input-output machines ([MA101 week 1](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w01-functions-as-machines.md)), linear functions and rates ([MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md)), and progression systems of skill versus power ([GD102 week 9](../../GD102-systems-design-and-game-mechanics/syllabus.md)).

**Interactive:** [examples/w01-modifier-stacking.html](../examples/w01-modifier-stacking.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a stat is

A **stat** is a named number attached to a character, item or enemy that the rules read to decide an outcome. Strength, Armor, Critical Strike Chance and Movement Speed are all stats. So are numbers the player never sees, such as an enemy's hidden aggro radius. We will call those **hidden stats**. Everything in this course is about choosing these numbers and the rules that read them.

Stats come in layers. Keep these three words straight, because the rest of the semester uses them constantly.

- A **primary stat** (often called an attribute) is one the player raises directly, usually by spending points on level-up or by equipping items. Strength, Dexterity, Vitality and Intelligence are the classic set.
- A **derived stat** is computed from primary stats and other sources. Maximum health, attack power, mana pool and critical chance are usually derived.
- An **outcome** is the thing the player actually cares about. Damage per second, seconds survived, fights won, gold per hour. Outcomes are rarely shown on the sheet, and that gap is where most balance problems live.

A stat's meaning is the path from it to an outcome. "Strength" means nothing until a rule turns it into something. A useful way to say this is that every stat has an **exchange rate**: how much of some outcome one point of the stat buys.

### Exchange rates in shipped games

Look at how three real games answer the question "what is one point worth?"

In Diablo II, spending one point of Vitality raises a Barbarian's maximum life by 4, but a Sorceress's by only 2. One point of Energy gives the Sorceress 2 mana and the Barbarian 1. The word "Vitality" on the level-up screen is identical for both classes. What it says is different. The game is using the same vocabulary to speak two dialects. The Barbarian's points lean toward survival, the Sorceress's toward spellcasting.

In World of Warcraft before the Cataclysm expansion (2004-2010, which covers the classic era), Warriors and Paladins turn one point of Strength into 2 melee attack power, while Mages turn it into 1. Stamina converts into maximum health at a fixed rate per point. Then attack power itself has an exchange rate. Every 14 attack power adds 1 to the weapon's damage per second. Follow the chain and one point of Strength is worth 2/14 ≈ 0.14 DPS to a Warrior. To a Mage, who rarely swings a weapon, it is worth close to nothing.

In Diablo III, each class has one **main stat**. Strength for Barbarians and Crusaders, Dexterity for Demon Hunters and Monks, Intelligence for Wizards, Witch Doctors and Necromancers. Every point of your main stat raises all your damage by 1%. The other two attributes do almost nothing for you. The designers cut the vocabulary down so each class hears one word for "hit harder."

These are three different design positions. Diablo II keeps a shared stat list and changes the exchange rates per class. Classic WoW builds chains (Strength to attack power to DPS) and lets some links go nearly to zero. Diablo III assigns one damage stat per class and makes its rate a clean percentage. None is wrong. Each one decides what the player has to learn and which mistakes they can make.

### Dead stats

A **dead stat** is a stat whose exchange rate into anything a character cares about is zero or close to it. Strength on a classic WoW Mage is the textbook case. Dead stats are not always bugs. They can be the price of a shared item pool. When every class can loot every item, some items will be useless to some classes. But each dead stat on a piece of gear is a small disappointment when it drops, and each dead choice on a level-up screen is a trap for new players. You should know where yours are and decide whether you want them.

### The stat sheet as a graph

Draw your stat sheet as a graph before you write any formulas. Put primary stats on the left, derived stats in the middle and outcomes on the right. Draw an arrow for every rule that reads one number to produce another, and write the exchange rate on the arrow.

```
Strength --x2--> Attack power --÷14--> +DPS -----> Damage per second
Stamina  --xk--> Max health ----------------------> Seconds survived
Armor    --(formula, week 3)--> % mitigation ------> Seconds survived
```

The graph answers questions that a list of stats hides. Which outcome has the most arrows pointing into it? (That outcome is where players will stack.) Which primary stat has only one arrow, and does that arrow run into an outcome this class cares about? (If not, it is dead for that class.) Which arrows are multiplications and which are additions? That last question is the subject of the worked example, and it matters more than it looks.

## 2. Worked example: why the tenth "+10% damage" feels weaker than the first

### The hook

In Diablo III every point of your main stat adds 1% damage. A character with 100 main stat gets +100%. Now give two characters the same item with +50 main stat. The first character has 100 main stat and the second has 1,000. The tooltip says the same thing to both, "+50 Strength," which reads as "+50% damage." Yet one of them sees their damage jump by a quarter and the other barely notices a change. Players say late-game items "feel like nothing." They are right, and the reason is arithmetic, not imagination.

### The model

Modifiers combine in one of two ways. Let `B` be a base value (say, weapon damage).

```
Additive pool:        final = B × (1 + p1 + p2 + ... + pn)
Multiplicative chain: final = B × (1 + q1) × (1 + q2) × ... × (1 + qm)
```

- `p1 ... pn` are **additive** bonuses. They are summed first, then applied once. Diablo III's main stat works this way: `1 + S/100`, where `S` is main stat.
- `q1 ... qm` are **multiplicative** bonuses. Each one multiplies the running total.

Now ask the question the player is really asking. If I add one more bonus of size `p`, by what fraction does my damage grow?

```
Additive:        relative gain = p / (1 + P)     where P is the sum already in the pool
Multiplicative:  relative gain = q               no matter what came before
```

Read the additive line slowly. The bigger the pool you already have, the less the next bonus is worth to you. This is called **dilution**. The multiplicative line has no memory at all. A 10% multiplier is a 10% gain whether it is your first or your twentieth.

### Numbers you can check

Stack identical +10% modifiers, first in an additive pool, then as a multiplicative chain.

| Modifiers held (n) | Additive total | Gain from the n-th one | Multiplicative total | Gain from the n-th one |
|---|---|---|---|---|
| 0 | 1.00 | — | 1.000 | — |
| 1 | 1.10 | +10.0% | 1.100 | +10% |
| 2 | 1.20 | +9.1% | 1.210 | +10% |
| 3 | 1.30 | +8.3% | 1.331 | +10% |
| 5 | 1.50 | +7.1% | 1.611 | +10% |
| 10 | 2.00 | +5.3% | 2.594 | +10% |
| 20 | 3.00 | +3.4% | 6.727 | +10% |

Check one row by hand. With 10 additive modifiers the pool is 1 + 10 × 0.10 = 2.00. Before the tenth, it was 1.90. So the tenth one raised damage by 0.10 / 1.90 = 5.3%. The multiplicative total at 10 is 1.1 to the 10th power, 2.594.

Now the Diablo III hook, with the same model:

| Main stat before | Multiplier before | +50 main stat gives | Real damage gain |
|---|---|---|---|
| 100 | 2.00 | 2.50 | +25.0% |
| 1,000 | 11.00 | 11.50 | +4.5% |
| 5,000 | 51.00 | 51.50 | +1.0% |

Same item, same tooltip, a 25-fold difference in what it does.

### Move it yourself

Open the interactive. The left panel shows what the tooltip says, a row of identical "+10%" cards, one per modifier held. The right panel shows two curves, total multiplier against number of modifiers, one for the additive pool and one for the multiplicative chain, with a bar under each that shows the gain from the most recent modifier. Drag the slider from 0 to 20. The cards on the left never change. On the right, the additive bar shrinks with every step while the multiplicative bar stays at 10% and its curve bends upward. Both views show the same numbers. Only the right one shows what the numbers do.

Then switch the preset to "Diablo III main stat" and drag the main-stat slider. The item card on the left always reads "+50." The gain bar on the right falls from 25% to about 1%.

### The same idea in other games

**Path of Exile** makes the two combining rules part of its vocabulary. A modifier worded "increased" goes into an additive pool with every other "increased" modifier of the same kind. A modifier worded "more" is its own multiplier. Here is an example built on the wiki's rules. With 1,000 base damage and three 100% bonuses, if all three are "increased" you get 1,000 × (1 + 1 + 1 + 1) = 4,000. If two are "increased" and one is "more," you get 1,000 × (1 + 1 + 1) × (1 + 1) = 6,000. Same three numbers, 50% more damage, and the only difference on the tooltip is one word. In our model, "increased" is a `p` and "more" is a `q`. The relative-gain formulas predict the consequence. Once a build has a large "increased" pool, a "more" modifier of the same size is worth several times as much, so the one word on the tooltip is the most important word on the item.

**Classic World of Warcraft** has an additive pool that doesn't use percentages. Attack power adds AP/14 to a weapon's damage per second. Rewrite it in our form:

```
final DPS = weapon DPS + AP/14 = weapon DPS × (1 + (AP/14) / weapon DPS)
```

That is an additive bonus of size `(AP/14) / weapon DPS`. So 14 attack power (1 DPS) is a 2.5% gain on a 40 DPS weapon and a 1.25% gain on an 80 DPS weapon. A new weapon dilutes all the attack power you already have, which is why weapon upgrades in that era felt so large and small attack power bonuses felt so small.

**Diablo III** we already covered: main stat is one big additive pool whose size grows through the whole game.

Three games, three presentations, one idea. When you meet a new modifier, ask one question before anything else. Does it go into a pool with other bonuses, or does it multiply on its own?

### Design judgment

Additive pools and multiplicative chains each solve a problem and each create one. Choose deliberately.

Additive pools **limit power growth**. Doubling the number of bonuses a character holds far less than doubles their damage, so you can hand out many small bonuses over a long game without numbers running away. The cost is feel. Late items register as tiny, and players who don't know the math think your loot got worse. You can respond by scaling bonus sizes up over the game (which is what "+50 main stat" becoming "+500 main stat" does), or by showing the real gain on the tooltip ("+4.5% damage for you").

Multiplicative chains **keep every bonus meaningful**, which makes each pickup feel good. The cost is that they compound. Ten 10% multipliers give 2.6×, twenty give 6.7×, and when two players' multipliers stack in the same party the balance space explodes. You also have to test combinations, because a rare pairing of multipliers is where the one-shot builds come from.

Most mature games do what Path of Exile does in the open. They use one big additive pool for the common bonuses and reserve a small, controlled number of multiplicative sources for things that should feel special (a class talent, a legendary item). The number of multiplicative buckets you allow is roughly the number of dimensions your balance testing has to cover. Decide that number on purpose.

One more decision hides in here. If a stat's value depends on what the player already has, then **the same item is worth different amounts to different characters**. That is a feature when you want players to make build decisions ("I have lots of increased, so I want more"). It is a problem when the game presents stat choices as simple ("+10% is +10%"). Pick one, and make the tooltip tell the truth about the one you picked.

### Check the model

1. A character's damage pool is at +150% (multiplier 2.5). How much does a new +25% additive bonus increase their damage? How much would a +25% multiplicative bonus increase it?
2. In Diablo III terms, how much main stat must a character with 2,000 main stat gain to increase their damage by 10%?
3. Why does the relative gain of the n-th additive modifier never reach zero, even with a very large pool?

Answers are in the Check yourself section at the end.

## 3. Principles for a readable stat sheet

The worked example is one case of a general rule. The numbers a player sees are a language, and a language can be clear or misleading. Here are the questions to ask of any stat sheet you design.

### Does each stat have one job?

A stat is **orthogonal** when it affects one outcome and no other stat affects that outcome in the same way. Vitality raising health and nothing else is orthogonal. A stat called "Power" that raises damage, healing, health and movement speed is not. Non-orthogonal stats are easy to hand out and hard to price, because the one stat is secretly four stats, each with its own exchange rate. They also tend to become the only stat anyone wants.

The opposite failure is **overlapping stats**. If "Attack Power," "Physical Damage" and "Weapon Damage Bonus" all add to the same pool, players need a guide to tell them apart and you need a spreadsheet to keep their prices consistent. Merge them, or give each a distinct rule (one additive, one multiplicative, one conditional).

### Can the player predict what a point does?

Prediction needs a stable exchange rate that the player can learn and see. Classic WoW's "14 attack power is 1 DPS" never changes with level or weapon, so players learned it and quoted it in guides for years. Diablo II's per-class vitality rates are just as stable, but a player has to notice that the same point does different things for different classes. Diablo III's "+1% damage per main stat point" is the easiest of the three to hold in your head, because it is one rule for every class.

Stable rates are easier to design with too. If you change one exchange rate, every item that carries that stat changes value at once. That is a powerful lever and a dangerous one.

### Is the number scale right?

**Granularity** is how many distinct values a stat can take in normal play. Fire Emblem games keep combat stats small, often under 30, and compute damage as attack minus defense. One point of Defense is visible in every fight, because it is one less damage from every hit. Games with stats in the thousands can express tiny differences but lose that legibility. A +3 Strength ring in a game with stats near 20 is a big deal. A +3 Strength ring in a game with stats near 3,000 is noise.

Choose the scale from the decisions you want players to make. If you want players to feel each point, keep numbers small and rules simple. If you want long, smooth progression with many small upgrades, you need larger numbers, and you should plan for dilution.

### Where are the hidden stats?

Every game has numbers the player cannot see: enemy accuracy, the constant inside a formula, a threat multiplier. Hidden stats are fine when the player can still learn the outcome by playing. They become a problem when a visible stat's exchange rate depends on them. In classic WoW the armor formula depends on the attacker's level, so the mitigation your sheet shows is only correct against one kind of attacker. Week 3 returns to this.

## 4. From stat sheet to spreadsheet

This course builds almost everything in spreadsheets, starting this week. A spreadsheet is a stat graph written as cells, with one sheet of **inputs** (primary stats per class, exchange rates, base values), one sheet of **derived** values computed only from inputs, and one sheet of **outcomes** computed only from derived values. Keep the arrows flowing one way. When a formula in the outcomes sheet reaches back into the inputs sheet, you have a hidden arrow in your graph, and it will surprise you later.

Three habits make the sheets useful:

1. **Name every constant.** Put "AP per DPS = 14" in its own labeled cell and point formulas at it. When you want to test 10 or 20, you change one cell.
2. **Compute exchange rates explicitly.** Add a row per class that says "one point of X adds Y to outcome Z." This is where dead stats show up as zeros.
3. **Compute relative gain as well as totals.** For every modifier, add a column for "gain from this one, given everything else." The worked example is the reason.

[Week 9 of this course](w09-item-budgets-and-stat-weights.md) (item budgets and stat weights) turns these exchange rates into prices. Everything you set up now feeds that.

## In-class activity (25 minutes)

Work in pairs. You are designing the stat sheet for a small action RPG with three classes: a Guardian (melee, tanky), a Ranger (ranged, fast) and a Mystic (spells, fragile).

**Materials:** a sheet of paper or a blank spreadsheet, and the interactive.

1. (8 min) Pick at most five primary stats. Draw the stat graph from primary stats to derived stats to the outcomes "damage per second" and "seconds survived." Write an exchange rate on every arrow, per class if it differs.
2. (5 min) Mark every dead stat for every class. Decide, in one sentence each, whether to keep it.
3. (7 min) Choose which damage bonuses go into an additive pool and which, if any, are multiplicative. Using the interactive, find how many additive +10% modifiers a late-game character must hold before a new one adds less than 5%.
4. (5 min) Swap graphs with another pair. Find one stat on their sheet that is not orthogonal or that overlaps another stat.

**Expected output:** one stat graph with exchange rates, a list of dead stats with a keep-or-cut decision, and one written critique of another pair's sheet.

## Common misconceptions

- **"+10% is +10%."** Only for a multiplicative bonus. An additive +10% is worth 10% divided by the size of the pool it joins. At a +100% pool it is worth 5%.
- **"A stat means the same thing for every class."** Exchange rates can differ by class (Diablo II Vitality) or drop to zero (Strength on a classic WoW Mage). Always compute the rate per class.
- **"Late-game items are weaker because the designers got lazy."** In additive systems, the same bonus is genuinely worth less as the pool grows. It is an arithmetic effect you must plan around, not an accident.
- **"More stats means more depth."** More stats means more exchange rates to price and more places for dead or overlapping stats to hide. Depth comes from choices whose values depend on the rest of the build.

## Check yourself

1. A character's damage pool is at +150% (multiplier 2.5). How much does a new +25% additive bonus increase their damage? How much would a +25% multiplicative bonus increase it?
2. In Diablo III terms, how much main stat must a character with 2,000 main stat gain to increase their damage by 10%?
3. Why does the relative gain of the n-th additive modifier never reach zero, even with a very large pool?
4. In classic WoW, a Warrior gains 70 Strength. How much DPS does that add? Compute the relative gain on a 50 DPS weapon.
5. A designer proposes that each point of a new stat, Fury, gives "+2% more damage" (multiplicative per point). A late-game player might have 50 Fury. What is their multiplier, and what problem will the designer face?

<details>
<summary>Answers</summary>

1. Additive: the pool goes from 2.5 to 2.75, a gain of 0.25 / 2.5 = 10%. Multiplicative: 2.5 × 1.25 = 3.125, a gain of 25%.
2. The multiplier is 1 + 2000/100 = 21. A 10% gain means reaching 23.1, which is 1 + S/100 = 23.1, so S = 2,210. The character needs 210 more main stat.
3. The gain is p / (1 + P). It shrinks as P grows but stays positive for any finite pool. Every additive bonus still helps. It just helps less.
4. 70 Strength × 2 AP = 140 AP. 140 / 14 = 10 DPS. On a 50 DPS weapon that is 10 / 50 = +20%.
5. 1.02 to the 50th power ≈ 2.69×. The multiplier grows exponentially with Fury, so every extra point of Fury is worth more damage in absolute terms than the last. Players will stack Fury above everything, and the designer must either cap it, make it additive, or price it steeply rising.

</details>

## Lab / assignment hook

**Lab 01: Stat sheet in a spreadsheet** ([labs/lab01.md](../labs/lab01.md)). You build the three-sheet stat model (inputs, derived, outcomes) for the in-class RPG, compute exchange rates per class, flag dead stats, and chart additive versus multiplicative stacking. Deliverable: the spreadsheet and a 300-word design note.

## Sources

- Blizzard, Diablo II: Lord of Destruction class pages, classic.battle.net/diablo2exp/classes/barbarian.shtml and sorceress.shtml: life per Vitality point (4 and 2) and mana per Energy point (1 and 2). Values are the same in Diablo II: Resurrected.
- Warcraft Wiki, "Attack power" (warcraft.wiki.gg, accessed September 2026): 1 DPS per 14 attack power until patch 6.0.2 (2014) changed it to 1 per 3.5. WoWWiki archive, "Attack power" (wowwiki-archive.fandom.com), class table for the game before patch 4.0.1 (Cataclysm, 2010): melee attack power is Strength x 2 plus level terms for Warriors and Paladins, and Strength - 10 for Mages. The stamina-to-health rate is left as `k` because the sources checked give later-era values only.
- Diablo Wiki (Fandom), "Primary stat" (accessed September 2026): each primary stat grants "a direct 1% increased damage per attribute point" to classes that use it; Strength for Barbarian and Crusader, Dexterity for Demon Hunter and Monk, Intelligence for Necromancer, Witch Doctor and Wizard. Diablo III with all classes through the Necromancer (2017 onward).
- Path of Exile Wiki (pathofexile.fandom.com), "Stat" (accessed September 2026): "increased" and "reduced" effects are added into a single multiplier, and each "more" or "less" effect multiplies the base in turn. Path of Building Community, `src/Classes/ModDB.lua` (dev branch, 2026), implements the same rule, summing INC mods and multiplying MORE mods. The 1,000-damage example is our own illustration. Path of Exile 1, rules unchanged since launch.
- Fire Emblem Wiki, "Damage": damage is attack minus defense or resistance across most titles.
- Schreiber, I. (2010). *Game Balance Concepts*, Levels 1-2. gamebalanceconcepts.wordpress.com.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 9.

## Interactive spec: examples/w01-modifier-stacking.html

**Purpose.** Make visible that identical tooltips ("+10%") produce shrinking real gains in an additive pool and constant gains in a multiplicative chain.

**The one insight.** The left view (tooltips) never changes. The right view (real gain) shrinks for additive and stays flat for multiplicative, while the multiplicative total curves away upward.

**Layout.** Two linked panels side by side on desktop, stacked on mobile.

- Left panel, "What the tooltip says": a row of up to 20 identical small cards, each reading "+10% damage" (label text updates to the chosen bonus size). The number of cards equals `n`. The newest card is highlighted.
- Right panel, "What it does": a line chart. x axis `n` from 0 to 20. y axis total multiplier from 1 to 7 (auto-extend if the bonus size makes it larger). Two series: additive `1 + n·p` and multiplicative `(1 + p)^n`. A vertical marker at the current `n`. Under the chart, two horizontal bars labeled "gain from the newest modifier": additive `p / (1 + (n−1)·p)` and multiplicative `p`, both as percentages with one decimal.
- A numeric readout under each series: total multiplier (3 decimals) and gain from newest (1 decimal).

**Controls.**
- Slider `n` (modifiers held), integer 0-20, default 10. Keyboard arrows step by 1.
- Select "bonus size" `p`: 5%, 10% (default), 25%.
- Preset toggle "Diablo III main stat": switches the model to `multiplier = 1 + S/100`, replaces `n` with slider `S` (main stat) from 0 to 5,000, step 50, default 1,000, and a fixed item of +50 main stat. Left panel shows one card "+50 main stat". Right panel plots `1 + S/100` and shows the bar "gain from +50" `= 50 / (100 + S)`. The multiplicative series is hidden in this preset.

**Exact test values (must match the lecture table).**
- p = 10%: n = 1 → additive 1.100 gain 10.0%, mult 1.100 gain 10%; n = 2 → 1.200, 9.1%; 1.210. n = 5 → 1.500, 7.1%; 1.611. n = 10 → 2.000, 5.3%; 2.594. n = 20 → 3.000, 3.4%; 6.727.
- n = 0 → both totals 1.000, gain shows a placeholder dash ("-").
- Diablo III preset: S = 100 → before 2.00, after 2.50, gain 25.0%; S = 1,000 → 11.00, 11.50, 4.5%; S = 5,000 → 51.00, 51.50, 1.0%.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, additive in the primary accent, multiplicative in the secondary accent. All numbers in text as well as in the chart. Respect reduced motion (no card animation). No game logos or art; the Diablo III preset is text only.
