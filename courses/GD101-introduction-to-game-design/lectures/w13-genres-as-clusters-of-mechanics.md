# GD101 · Week 13 — Genres as Clusters of Mechanics

**Why this matters:** When you tell a teammate or a publisher "it's a roguelike," you make a dozen promises about how the game plays without saying any of them out loud. This week you learn to spell out those promises as a list of mechanics, measure how close two games really are, and decide on purpose which genre expectations you keep and which you break.

**You will be able to:**
- Describe any game as a set of mechanics and compute the Jaccard similarity between two games by hand.
- Group a small collection of games into clusters at a chosen similarity threshold and explain how the threshold changes the groups.
- Critique a genre label by showing which mechanics it predicts correctly and which it hides.
- Design a genre blend by naming the mechanics you take from each parent game and the ones you drop.

**Before class:** Fullerton, *Game Design Workshop* (4th ed.), chapter 3 (formal elements) and chapter 4 (dramatic elements), skimmed for the difference between rules and theme. Read the RogueBasin page "Berlin Interpretation" (about 10 minutes). Bring a list of the five games you played most this year.

**Prerequisites from earlier courses:** none outside this course. You need the formal elements from GD101 weeks 2 and 3, MDA from GD101 week 4 and interesting decisions from GD101 week 9 (see the [GD101 syllabus](../syllabus.md)). The set operations used here (intersection and union) are taught again with probabilities in [MA102 week 1](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) next semester.

**Interactive:** `examples/w13-genre-similarity-map.html` (to be built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a genre label carries

In film and books, a genre mostly names a mood or a setting. A western has horses and dust. A horror film tries to scare you. Game genres work differently. "Platformer," "deck-builder," "real-time strategy" and "roguelike" say almost nothing about setting. They describe what you do with your hands and your head. A platformer is a game where you jump between surfaces and falling is the main danger. A deck-builder is a game where you add cards to your own deck during play and draw from it.

That is this week's claim. **A game genre is a cluster of mechanics that tend to show up together.** A mechanic here means what it meant in week 4 under MDA: a rule or procedure the game runs, such as "when you die, you start over from the beginning" or "you draw five cards each turn." Mechanics are the part of a game you could write down as rules. Dynamics are what happens when players meet those rules. Aesthetics are the feelings that result.

Genre names do leak into aesthetics. "Survival horror" names a feeling as well as a set of rules. But when two designers argue about whether a game "counts" as a roguelike, they almost never argue about the mood. They argue about a list: does it have permadeath, is the map random, is it turn-based. That list is the thing you can measure.

### Why designers need more than the label

Genre labels exist mostly for players and shops. They help a buyer find something like the last game they enjoyed. For that purpose a single word works fine.

For a designer, a single word hides too much. Suppose your pitch says "roguelike." One reader imagines Rogue itself, a turn-based game on a square grid. Another imagines Hades, a fast action game where you dash and slash in real time. A third imagines Slay the Spire, where you never move a character at all and fight by playing cards. All three readers heard the same word. They will make three different prototypes.

So the working rule for this lecture is simple. Whenever you use a genre word, you should be able to expand it into the mechanics you mean. If you can't, you don't yet know what you are promising.

### Genres grow by descent

Genres are not designed by committee. They grow from a founding game, then change as other designers copy some of its mechanics and swap others. Rogue, released in 1980 by Michael Toy and Glenn Wichman, was a turn-based dungeon crawl on a square grid, drawn with text characters, with a new random dungeon each game and permanent death. Games that copied it, such as Hack (1982) and Moria (1983), were called "roguelikes" because they were like Rogue.

A decade later, Condor pitched Diablo in 1994 with the idea of bringing the randomness of Moria, NetHack and Rogue to a modern graphical game. By the time it shipped, Diablo ran in real time. Two mechanics from the founding game survived (random dungeons, a single hero descending level by level) and one of the most defining ones (turns) did not. You will see that pitch again next week.

This pattern of descent with swaps is why genre boundaries are blurry. Every descendant keeps some of the parent's mechanics and changes others. After a few generations, two games that share a label may share only a few mechanics.

## 2. Worked example: how close is Slay the Spire to Rogue?

### The hook

Slay the Spire (Mega Crit, full release January 2019) is sold and reviewed as a "roguelike deck-building game." Its developers have said their starting goal was to fuse a roguelike with deck-building games like Dominion, the 2008 tabletop card game by Donald X. Vaccarino.

So here is a question you can actually answer. Measured by mechanics, is Slay the Spire closer to Rogue, the game its genre label points at, or to Dominion, a board game with no dungeon, no hero and no death? Most students guess Rogue. The numbers say otherwise.

### The model

Describe each game as a **set** of mechanics, meaning a list where each mechanic is either present or absent. Then compare two games A and B with the **Jaccard similarity**:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

- `A ∩ B` (the **intersection**) is the set of mechanics both games have.
- `A ∪ B` (the **union**) is the set of mechanics at least one of the games has.
- `|X|` means "how many items are in X."

J runs from 0 (the games share nothing) to 1 (the games have exactly the same mechanics on your list). A value of 0.5 means half of all the mechanics in play between the two games are shared.

Why divide by the union and not by the size of one game? Because a big game should not look similar to everything just because it has many mechanics. Dividing by the union punishes differences on both sides. A mechanic that only A has and a mechanic that only B has both push J down.

Two more ideas complete the model.

- A game's **nearest neighbour** is the other game with the highest J.
- A **cluster at threshold t** is a group of games you can connect by a chain of pairs, each with `J ≥ t`. Pick a high t and you get many small, tight groups. Pick a low t and the groups merge. A genre is one of these clusters, and the threshold is a choice someone made.

### The data

Here are eight mechanics, each written so you could check it by playing the game. The letters are just short names.

- **P, permadeath runs.** When you die, the run ends and you start again from the beginning.
- **R, randomized content each play.** The map, rooms or available cards change from one play to the next.
- **T, turn-based.** Nothing happens until you act. The game waits for you.
- **A, real-time action.** Enemies act on a clock. Hesitating costs you.
- **M, avatar movement.** You steer a character through a space.
- **J, platforming.** Jumping and falling between surfaces is a core skill.
- **D, deck-building.** You add cards to your own deck during play and draw from it.
- **U, unlocks between runs.** Something you earn in one play stays for the next.
- **G, ability-gated map.** New abilities open areas you already saw but could not reach, so you backtrack.

That is nine, not eight. Count again whenever someone hands you a list. Now the six games. The eras matter, because later versions and remakes change some of these.

| Game (version) | P | R | T | A | M | J | D | U | G | Size |
|---|---|---|---|---|---|---|---|---|---|---|
| Rogue (1980) | ✓ | ✓ | ✓ | | ✓ | | | | | 4 |
| Spelunky (2008 original) | ✓ | ✓ | | ✓ | ✓ | ✓ | | ✓ | | 6 |
| Hades (2020 release) | ✓ | ✓ | | ✓ | ✓ | | | ✓ | | 5 |
| Slay the Spire (2019 release) | ✓ | ✓ | ✓ | | | | ✓ | ✓ | | 5 |
| Dominion (2008 base set) | | ✓ | ✓ | | | | ✓ | | | 3 |
| Super Metroid (1994) | | | | ✓ | ✓ | ✓ | | | ✓ | 4 |

A few coding decisions, so you can argue with them:

- Spelunky's U is the Tunnel Man shortcut system, which persists between runs.
- Hades's U is the Mirror of Night and other permanent upgrades bought in the House of Hades between escape attempts.
- Slay the Spire's U covers new characters, cards and relics unlocked by finishing or failing runs.
- Dominion's R is its setup. Each game uses a different selection of 10 kingdom card piles from the 25 in the first-edition base set, so the cards on offer change every time you play.
- Dominion has no permadeath because nobody dies. It has no avatar because you never move a piece.

### Numbers you can check

Take Slay the Spire and Rogue first.

- Slay the Spire = {P, R, T, D, U}. Rogue = {P, R, T, M}.
- Intersection = {P, R, T}, so 3.
- Union = {P, R, T, M, D, U}, so 6.
- J = 3/6 = **0.50**.

Now Slay the Spire and Dominion.

- Dominion = {R, T, D}.
- Intersection = {R, T, D}, so 3.
- Union = {P, R, T, D, U}, so 5.
- J = 3/5 = **0.60**.

By this list of mechanics, Slay the Spire is closer to a tabletop card game than to the game that gave its genre its name. That matches what its developers said they set out to build.

Here is the full table. Check at least three cells by hand before you trust the interactive.

| | Rogue | Spelunky | Hades | Slay the Spire | Dominion | Super Metroid |
|---|---|---|---|---|---|---|
| Rogue | 1 | 3/7 = 0.43 | 3/6 = 0.50 | 3/6 = 0.50 | 2/5 = 0.40 | 1/7 = 0.14 |
| Spelunky | | 1 | 5/6 = 0.83 | 3/8 = 0.375 | 1/8 = 0.125 | 3/7 = 0.43 |
| Hades | | | 1 | 3/7 = 0.43 | 1/7 = 0.14 | 2/7 = 0.29 |
| Slay the Spire | | | | 1 | 3/5 = 0.60 | 0/9 = 0 |
| Dominion | | | | | 1 | 0/7 = 0 |
| Super Metroid | | | | | | 1 |

Nearest neighbours:

| Game | Nearest neighbour | J |
|---|---|---|
| Rogue | Hades and Slay the Spire (tie) | 0.50 |
| Spelunky | Hades | 0.83 |
| Hades | Spelunky | 0.83 |
| Slay the Spire | Dominion | 0.60 |
| Dominion | Slay the Spire | 0.60 |
| Super Metroid | Spelunky | 0.43 |

Three things jump out.

1. **Rogue is nobody's nearest neighbour.** The founding game of the roguelike genre is not the closest relative of any of its descendants on this list. Every descendant has drifted away in a different direction.
2. **Spelunky is exactly as close to Super Metroid (0.43) as to Rogue (0.43).** The shared mechanics with Super Metroid are the real-time ones (A, M, J). The shared ones with Rogue are the run structure (P, R, M). A player who picks Spelunky up for the first time meets the Super Metroid half in the first ten seconds. The Rogue half only shows itself at the first death.
3. **Dominion hits two of the three "roguelike core" mechanics.** If you define a roguelike as "P, R and T," then Dominion scores 2 out of 3. So do Spelunky and Hades. A checklist cannot tell a board game from an action game when the list is this short.

Now the clusters. Join any two games with `J ≥ t` and see what groups form.

| Threshold t | Clusters |
|---|---|
| 0.90 | every game alone |
| 0.70 | {Spelunky, Hades}; the rest alone |
| 0.55 | {Spelunky, Hades}, {Slay the Spire, Dominion}, {Rogue}, {Super Metroid} |
| 0.45 | {Rogue, Spelunky, Hades, Slay the Spire, Dominion}, {Super Metroid} |
| 0.40 | all six games in one cluster |

At t = 0.55 you get what looks like two sensible genres: an "action roguelite" pair and a "deck-builder" pair, with Rogue on its own. Drop to 0.45 and Rogue pulls both pairs together into one big "roguelike" family, because it is 0.50 away from Hades and 0.50 away from Slay the Spire. Drop to 0.40 and Super Metroid joins through Spelunky. At that point the "genre" includes a board game and a side-scrolling exploration game.

Notice that at 0.45 Dominion is in the roguelike cluster. It gets there through a chain (Dominion to Slay the Spire at 0.60, Slay the Spire to Rogue at 0.50), not because it looks like Rogue. This chaining effect is real in how genre words spread. Each step looks reasonable. The ends of the chain have little in common.

### The visual

Open `examples/w13-genre-similarity-map.html`. The left panel shows the "shop shelf," with each game sitting under the genre label a store would use. The right panel shows the same six games placed by their mechanics, with a line between every pair whose J is above the threshold slider.

Drag the threshold from 0.90 down to 0.40 and watch the clusters on the right merge while the shelf on the left stays fixed. Then click a cell in the mechanics grid. Remove D from Slay the Spire, for example, and its nearest neighbour flips from Dominion to Rogue. The shelf does not change at all. The label is stable because it ignores the mechanics. The map moves because it is made of them.

### Cross-game recognition

You have already met this model in other clothes.

**The Berlin Interpretation (roguelike community, 2008).** At the International Roguelike Development Conference in Berlin in 2008, developers wrote a list of "high-value factors" for a roguelike, including random environment generation, permadeath, turn-based play, grid-based movement, resource management and exploration, plus a shorter list of "low-value factors" such as an ASCII display. That is our model with one change. Instead of comparing two games, you compare every game against one ideal set, often called a **prototype**. A game's genre score is how much of the prototype it matches. The document itself says a game can be a roguelike without every factor, so it is a similarity threshold, not a hard rule. Rewrite it as `J(game, prototype) ≥ t` and it is this week's formula.

**Metroidvania (Super Metroid, 1994, and Castlevania: Symphony of the Night, 1997).** This genre label is named after two games, and it is defined almost entirely by one mechanic, our G. The world is one connected map, and new abilities open areas you saw earlier but could not reach. Some genres are clusters of many weak signals. Others hang on a single mechanic that carries most of the weight. In set terms, G gets such a high weight that any game with it lands in the cluster. The interactive's "weight" option lets you try this.

**Steam tags (current storefront, 2020s).** Valve's store lets developers, players and moderators attach tags to a game. Valve's own partner documentation says at least 5 tags are required before launch, up to 20 are recommended, and the top 20 are the ones used to shape how the store shows and recommends the game. The tag wizard sorts tags into genres, visual properties, themes and moods, and features such as "Resource Management." A game on Steam is literally a weighted set of tags, and "more like this" is a similarity measure over those sets. The store is running a version of this lecture's model on every game it sells.

Three presentations, one idea. A genre is a region in "mechanic space," defined either by distance between games (Jaccard, clusters), by distance to an ideal (the Berlin list), or by one decisive mechanic (Metroidvania).

### Eyes-open design judgment

The Jaccard model is a thinking tool, not a truth machine. Use it knowing what it does and does not do.

- **Your list decides the answer.** Remove the D column and Slay the Spire's nearest neighbour becomes Rogue (J = 0.60) instead of Dominion (J = 0.50). Remove the U column and Slay the Spire and Dominion rise to 0.75. Whoever picks the mechanics picks the map. Before you trust a similarity, ask who chose the columns and why.
- **Every mechanic counts the same.** Plain Jaccard treats "has platforming" and "has an unlock between runs" as equal. Players do not. Jumping changes every second of play; an unlock changes the menu between runs. When one mechanic carries a genre (G for Metroidvania), weight it, and say that you did.
- **Presence is not the same as importance.** Hades and Spelunky both have U, but the Mirror of Night shapes Hades far more than Tunnel Man shapes Spelunky. A yes/no grid cannot show that. A 0 to 3 scale per mechanic can, at the cost of more arguments about scores.
- **Aesthetics are missing.** Two games with identical mechanic sets can feel nothing alike. Horror, comedy and pacing live in the A of MDA, and this grid only sees the M. Use genre maps to plan mechanics and use your week 5 experience goals to plan feelings.
- **When to use it.** Use a mechanics grid when you need to find your game's neighbours ("what are we competing with?"), to explain a blend ("take R and P from roguelikes, D from deck-builders"), or to check that a genre word means the same thing to your whole team. Do not use a similarity score to argue that a game "is" or "is not" a genre. That argument has no answer, because the threshold is a choice.

## 3. Genre as a contract with the player

A player who reads "roguelike" on a store page arrives with expectations. They expect to die often. They expect the next run to differ from the last. They expect their knowledge, not their character, to be what grows. If your game breaks one of those expectations, some players will feel cheated even if the game is good, because it broke a promise they thought you made.

This is the practical reason to understand genres as mechanic clusters. Each mechanic in the cluster sets up a matching expectation. You can list them.

| Mechanic in the cluster | What the player expects | What happens if you remove it silently |
|---|---|---|
| Permadeath runs | A death costs the run, so each run is a fresh attempt | Players hoard resources "for later" that never comes, or feel cheated by a checkpoint that makes risk meaningless |
| Randomized content | Knowledge transfers, memorized layouts do not | Players memorize the route and the game becomes a timing test |
| Turn-based | Time to think before each action | Players who came to plan are rushed; reviews say "too hard" |
| Unlocks between runs | A failed run still moved something forward | Early deaths feel wasted and players quit sooner |

None of this means you must keep every expectation. Many good games break one on purpose. Diablo's move from turns to real time broke the "time to think" expectation of its roguelike parents and found a larger audience. The point is to break expectations deliberately and to say so in your pitch. You will write that sentence next week.

### Genre blends are unions with subtractions

Pitches often say "X meets Y." In set terms, a blend starts from the union of two parents and then removes mechanics that clash. Slay the Spire is roughly (Rogue ∪ Dominion) with avatar movement removed and unlocks added. Written out:

```
Rogue ∪ Dominion        = {P, R, T, M, D}
remove M, add U          = {P, R, T, D, U}   (Slay the Spire)
```

Two operations are worth naming.

- **Subtraction** removes a parent's mechanic that would fight the other parent. Moving an avatar on a grid while also managing a deck doubles the attention cost of every turn, so the blend drops movement and represents the dungeon as a map of nodes.
- **Addition** brings in a mechanic neither parent has, often to fix a dynamic the union creates. Permadeath plus a large random card pool can make early runs feel pointless. Unlocks between runs answer that.

When you design a blend, write both lists down. "What we take from each parent" is the easy half. "What we drop, and why" is where the design lives.

### Where the genre does not help

Two warnings before you start using this.

First, a genre cluster tells you what is common, not what is good. Plenty of games in the roguelike cluster are dull. The mechanics are the entry ticket. The interesting decisions you studied in week 9 are still yours to design.

Second, genre maps drift over time. A mechanic that was rare becomes standard, and then the columns that used to separate games stop separating anything. Unlocks between runs were unusual among early roguelikes. In the 2010s they became common enough that players coined "roguelite" for games that have them. When a column becomes a near-universal yes, it stops carrying information. Swap it for a column that still splits games.

## 4. Using a genre map in your own project

Your paper prototype for this course sits somewhere in mechanic space too. Here is a short routine that turns this week's model into a design move.

1. **List your game's mechanics** in the same yes/no form, using 8 to 12 columns written so a stranger could check them by playing.
2. **Pick three published games** you think are close. Code them with the same columns.
3. **Compute J** for your game against each. The highest is your nearest neighbour.
4. **Read the differences.** The mechanics in the union but not the intersection are what makes you different from that neighbour. If that set is empty or tiny, you are making a clone. If it is huge, players have no reference point and you will need to teach more in your tutorial.
5. **Decide one deliberate break.** Name one expectation from your nearest neighbour's cluster that your game breaks, and write one sentence on what the player gets in exchange.

A useful target for a first project is a nearest-neighbour J somewhere between about 0.4 and 0.7. That is a rule of thumb, not a finding. Below it, the game is hard to explain in one line. Above it, the game is hard to tell apart from its neighbour. You will choose your own range once you have tested a few prototypes.

## In-class activity (25 minutes)

Work in groups of three.

1. **(5 min)** Each person names two games they played this year. Write the six games on the board.
2. **(8 min)** As a group, agree on 8 mechanic columns that split these six games. Each column must be checkable by play ("you can jump," not "it feels floaty"). Fill in the yes/no grid.
3. **(7 min)** Compute J for every pair (15 pairs). Split the work: five pairs each. Find each game's nearest neighbour.
4. **(5 min)** Cluster at t = 0.5. Compare your clusters with the genre labels a store would put on these games. Write down the one pair where the label and the map disagree most, and the column that causes it.

**Expected output:** one photo of the grid, the 15 J values, a cluster list, and a two-sentence note on the biggest disagreement. Keep the grid. It is the starting point for Lab 13.

## Common misconceptions

- **"A genre is defined by its setting."** For games, it is mostly defined by mechanics. A fantasy roguelike and a sci-fi roguelike are closer to each other than a fantasy roguelike and a fantasy platformer.
- **"If it has the genre's signature mechanics, it belongs to the genre."** Dominion has two of three "core roguelike" mechanics (R and T) in our list, the same count as Hades. Short checklists let unrelated games in. Compare with the whole set, or weight the mechanics that really carry the genre.
- **"Jaccard similarity is objective."** The formula is fixed. The columns are yours. Removing one column changed Slay the Spire's nearest neighbour. Always report the columns with the score.
- **"The founding game is the center of its genre."** On our list, Rogue is no game's nearest neighbour. Descendants spread out in different directions, and the founder ends up at the edge of the cluster it named.

## Check yourself

1. Game X = {P, R, A, M, U}. Game Y = {R, T, D, U}. Compute J(X, Y). Which of the six games in section 2 is X's nearest neighbour, and what is that J?
2. You add a new mechanic column, "hub area between runs" (H). Hades has it. Spelunky does not. Rogue does not. Recompute J(Spelunky, Hades) and J(Rogue, Hades). Does Hades's nearest neighbour change?
3. A publisher says your card game "is basically Slay the Spire." Your game is {R, T, D, U, G}. Compute J with Slay the Spire and list the mechanics that make up the difference. Write the one sentence you would say back.
4. At what threshold t do Spelunky and Super Metroid first land in the same cluster, if you only allow direct links (no chains)? What changes if chains are allowed?

<details>
<summary>Answers</summary>

1. Intersection {R, U} = 2. Union {P, R, A, M, U, T, D} = 7. J = 2/7 ≈ 0.29. X has the same set as Hades, so X's nearest neighbour is Hades with J = 1 (and Spelunky next, at 5/6 = 0.83).
2. Spelunky {P, R, A, M, J, U} vs Hades {P, R, A, M, U, H}: intersection 5, union 7, J = 5/7 ≈ 0.71 (down from 0.83). Rogue {P, R, T, M} vs Hades: intersection {P, R, M} = 3, union {P, R, T, M, A, U, H} = 7, J = 3/7 ≈ 0.43 (down from 0.50). Hades's other scores against Slay the Spire, Dominion and Super Metroid also drop because the union grows by one. Its nearest neighbour is still Spelunky at 0.71.
3. Slay the Spire = {P, R, T, D, U}. Intersection {R, T, D, U} = 4. Union {P, R, T, D, U, G} = 6. J = 4/6 ≈ 0.67. The difference is P (Slay the Spire has permadeath runs, you do not) and G (you have an ability-gated map, it does not). A good reply: "It shares the deck-building run, but you keep your progress, and new cards open parts of the map you couldn't reach before."
4. J(Spelunky, Super Metroid) = 3/7 ≈ 0.43, so with direct links only they join at any t ≤ 0.43. With chains, they join at the same t, 0.43, because Super Metroid's best link to anyone is that same 0.43 link to Spelunky. Chains make no difference for Super Metroid, since it has no stronger path in.

</details>

## Lab hook

**Lab 13, Genre map of your prototype** ([labs/lab13.md](../labs/lab13.md)). Code your paper prototype and five published games in a shared mechanics grid, compute the similarity table and clusters, and write a 300-word positioning note naming your nearest neighbour and your one deliberate break. The note becomes the "what is it like" line of your one-page design in week 14.

## Sources

- Rogue: Wikipedia, "Rogue (video game)." Release in 1980 by Michael Toy and Glenn Wichman; turn-based, grid-based ASCII play, procedurally generated dungeons, permadeath; the source of the name "roguelike"; followed by Hack (1982) and Moria (1983).
- RogueBasin, "Berlin Interpretation." Drafted at the International Roguelike Development Conference, Berlin, 2008; lists of high-value and low-value factors.
- Spelunky: Wikipedia, "Spelunky." Original freeware release by Derek Yu, December 2008; enhanced remake 2012; procedurally generated levels, restart from the beginning on death, unlockables such as the Tunnel Man that persist between runs.
- Hades: Wikipedia, "Hades (video game)." Supergiant Games; early access December 2018, full release September 2020; randomized arrangement of pre-built rooms; return to the House of Hades on death; permanent upgrades such as the Mirror of Night.
- Slay the Spire: Wikipedia, "Slay the Spire." Mega Crit; early access November 2017, full release January 2019; procedurally generated spire, restart on death, unlocks of characters, cards and relics; developers' stated aim to combine a roguelike with deck-building games like Dominion.
- Dominion: Wikipedia, "Dominion (card game)." Designed by Donald X. Vaccarino, published by Rio Grande Games in 2008; 25 kingdom card piles in the first-edition base set (26 in the second edition) with a different selection used each game; Spiel des Jahres 2009; widely credited as the first deck-building game.
- Super Metroid: Wikipedia, "Super Metroid." Nintendo R&D1 and Intelligent Systems, 1994; power-ups open earlier inaccessible areas through backtracking; with Castlevania: Symphony of the Night (1997), the basis of the "Metroidvania" label.
- Diablo pitch: Wikipedia, "Diablo (video game)," development section. Condor's 1994 pitch framed the game as bringing Moria, NetHack and Rogue to modern graphics; Blizzard asked for real time in 1995; release at the turn of 1996 and 1997.
- Valve, Steamworks documentation, "Steam Tags" (current as of 2026). Who can apply tags, the 5-tag minimum before launch, the top 20 tags used for store visibility, and the tag categories.
- Hunicke, R., LeBlanc, M. & Zubek, R. (2004). "MDA: A Formal Approach to Game Design and Game Research." AAAI Workshop on Challenges in Game AI. Definitions of mechanics, dynamics and aesthetics.
- Fullerton, T. *Game Design Workshop* (4th ed., 2018), CRC Press, chapters 3 and 4.
- The yes/no coding of mechanics in section 2 is the author's, made for teaching. It uses the sources above for each game's features; students are invited to dispute individual cells.

## Interactive spec: examples/w13-genre-similarity-map.html

**Insight the visual must make obvious:** the store label stays the same while the mechanic map moves. Slay the Spire sits under "roguelike" on the shelf, but on the map its nearest neighbour is Dominion, and one column change flips it back to Rogue.

**Layout:** two linked panels, side by side on desktop (shelf left, map right), stacked on mobile (shelf on top). Below them, the editable mechanics grid and a numbers readout.

**Left panel, "The shop shelf":** three labelled boxes, "Roguelike / roguelite," "Deck-builder / card game," "Metroidvania / platformer." Default placement: Rogue, Spelunky, Hades, Slay the Spire under "Roguelike / roguelite"; Dominion under "Deck-builder / card game"; Super Metroid under "Metroidvania / platformer." Games are generic rounded chips with the game name as text only. No logos, art or screenshots. The shelf never moves when the grid changes. Show a small caption under it: "Labels ignore the grid."

**Right panel, "The mechanic map":** six nodes placed by classical multidimensional scaling (MDS) on the distance `1 − J`, recomputed whenever the grid changes; animate node moves over 300 ms unless `prefers-reduced-motion` is set. Draw an edge between every pair with `J ≥ t` (weighted J when weights are on), labelled with J to two decimals. Draw each game's nearest-neighbour link as a thicker arrow from the game to its neighbour (both arrows on ties). Colour nodes by cluster (connected components of the edge graph at threshold t) using the palette tokens. MDS may reflect or rotate between updates; fix orientation by flipping axes so Rogue is always in the upper-left quadrant.

**Mechanics grid (editable):** rows are the six games, columns P, R, T, A, M, J, D, U, G with full names in a tooltip and a visible legend. Each cell is a toggle button (`aria-pressed`), keyboard reachable with arrow keys moving between cells and Space toggling. Each column header has a checkbox "include column" (default all on). An optional weight row under the headers (numeric inputs, 0 to 5, step 1, default 1) is hidden behind a "Use weights" toggle.

**Controls:**
- Threshold slider t, 0.00 to 1.00, step 0.01, default 0.55. Show the current cluster list as text next to it.
- "Use weights" toggle (default off).
- "Chains allowed" toggle (default on). When off, clusters are replaced by "direct links only" and only edges are shown, no component colouring.
- Presets: "Lecture defaults" (the table in section 2), "Drop deck-building" (column D excluded), "Drop unlocks" (column U excluded), "Metroidvania weight" (weights on, G = 5, others 1), "Add hub column" (adds column H: Hades yes, others no; this is the only preset that adds a column).
- Reset button.

**Formulas:**
- `J(A, B) = |A ∩ B| / |A ∪ B|` over included columns; if the union is empty, J = 0.
- Weighted: `Jw(A, B) = Σ_{c ∈ A ∩ B} w_c / Σ_{c ∈ A ∪ B} w_c`.
- Nearest neighbour: argmax over other games of J; list all ties.
- Clusters at t: connected components of the graph with edges where `J ≥ t` (use a tolerance of 1e-9).
- Prototype score (readout only): `J(game, {P, R, T})` shown as "roguelike core score."

**Numbers readout:** a 6 × 6 similarity table (upper triangle, values as fraction and decimal, e.g. `3/5 = 0.60`), a nearest-neighbour list, and the roguelike core score per game. Highlight the Slay the Spire row.

**Test values (lecture defaults):**
- J(Slay the Spire, Rogue) = 3/6 = 0.50; J(Slay the Spire, Dominion) = 3/5 = 0.60; J(Spelunky, Hades) = 5/6 = 0.83; J(Spelunky, Super Metroid) = 3/7 = 0.43; J(Spelunky, Slay the Spire) = 3/8 = 0.375; J(Slay the Spire, Super Metroid) = 0.
- Nearest neighbours: Rogue to Hades and Slay the Spire (tie 0.50); Slay the Spire to Dominion (0.60); Super Metroid to Spelunky (0.43).
- Clusters: t = 0.55 gives {Spelunky, Hades}, {Slay the Spire, Dominion}, {Rogue}, {Super Metroid}; t = 0.45 gives one five-game cluster plus {Super Metroid}; t = 0.40 gives one cluster of six.
- "Drop deck-building": J(Slay the Spire, Rogue) = 0.60, J(Slay the Spire, Dominion) = 0.50; Slay the Spire's nearest neighbour becomes Rogue.
- "Drop unlocks": J(Slay the Spire, Dominion) = 0.75; J(Spelunky, Hades) = 0.80.
- "Add hub column": J(Spelunky, Hades) = 5/7 = 0.71; J(Rogue, Hades) = 3/7 = 0.43.
- Roguelike core score: Rogue 1.00 (3/3... computed as J with {P,R,T} = 3/4 = 0.75), see note below.

**Note on the core score:** compute it as the share of the prototype matched, `|game ∩ {P, R, T}| / 3`, not as J, so the readout matches the lecture's "2 out of 3" wording. Test values: Rogue 3/3, Slay the Spire 3/3, Spelunky 2/3, Hades 2/3, Dominion 2/3, Super Metroid 0/3.
