# MMO406 · Week 11 — Retcons and Continuity

**Why this matters:** A live world's canon grows by thousands of facts a year, written by dozens of people who never met the writers before them. Contradictions will happen. The question is what a contradiction costs when you find it, and that cost is set long before, by how the facts depend on each other. This week you learn to measure the cost of changing a fact before you change it, and to pick the kind of retcon that costs least.

**You will be able to:**
- Compute a fact's blast radius, its weighted revision cost and the frozen works it touches, from a canon dependency graph.
- Compute the chance that new content contradicts canon somewhere, from the number of facts it touches and the per-fact error rate, and show how a continuity database changes it.
- Classify a retcon as substitutive, subtractive or additive, and choose the cheapest one that solves a given problem.
- Design canon tiers and a precedence rule for your world bible, and critique the continuity practice of World of Warcraft, Star Wars and Final Fantasy XIV.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 1, "Worlds within the World," the parts on completeness and consistency, and the canon material in chapter 7, "Circles of Authorship" (use the contents page, about 20 pages). Wikipedia, "Star Wars Legends", the sections on the Holocron database and the 2014 announcement (15 minutes). Warcraft Wiki, "Draenei", the section "Design and retcon" (5 minutes).

**Prerequisites from earlier courses:** [GD202 week 4, dialogue systems and state flags](../../GD202-narrative-and-quest-design/lectures/w04-dialogue-systems-and-state-flags.md) (the "one writer per fact" rule and stale reads; the same problems at the scale of a whole setting). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one event in `k` tries). [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (what relaunches and shutdowns do to a world). [MMO406 week 4](w04-history-and-timelines.md) (the timeline's "referenced by" column and the precision gradient) and [week 10](w10-expansion-planning.md) (the broken-promise cost `D`).

**Interactive:** [w11-retcon-blast-radius.html](../examples/w11-retcon-blast-radius.html). Keep it open during section 2.

---

## 1. Canon, continuity and the retcon

Three terms, defined once.

**Canon** is the set of facts about your world that the team treats as true. A fact is anything a player could check: a date, a family tree, who opened the dikes, what the Tidewardens swore. Canon lives in your bible, in shipped content (quests, items, dialogue, zones) and in anything published outside the game (novels, comics, websites).

**Continuity** is the property that no two canon facts contradict each other. A world has continuity errors when two canon facts cannot both be true: a character acts two years after her death, or a book dates a founding to 939 while a quest says 941.

A **retcon** (retroactive continuity change) is a decision to change what was true in the past of the fiction. You make one either to fix a continuity error or because a new story needs the past to be different.

Retcons come in three kinds, and the difference between them is the subject of this lecture:

- **Substitutive.** Replace a fact with a different one. "Harrow did not open the dikes; they failed on their own."
- **Subtractive.** Declare a fact, or a whole body of work, no longer canon. "The novella is not part of the game's continuity."
- **Additive.** Leave the old fact standing and add a new one that changes what it means. "Harrow opened the dikes, but a spy had told him the enemy was already inside."

MMOs make continuity harder than any other medium. The canon is written over decades by writers who rotate. Players can walk into any old zone and read what it says, so old facts don't retire. And content that has shipped is expensive to change, and sometimes cannot be changed at all.

## 2. Worked example: the blast radius of a fact

### The hook

When World of Warcraft: The Burning Crusade introduced the draenei as a playable race in 2007, their new history had them as the eredar who refused Sargeras's offer of power. That contradicted the Warcraft III manual (2002), which Chris Metzen had also written. Metzen told players he had simply forgotten what he wrote, and that Blizzard would keep the new version because he believed it was stronger.

Here is the puzzle. The contradiction was obvious and public, and Blizzard kept it anyway. Years later the same studio spent several books, the *World of Warcraft: Chronicle* series (volumes in 2016, 2017, 2018 and 2024), trying to codify and tighten up the setting's history. Why was it cheap to live with one contradiction and worth a multi-volume project to consolidate the rest? The answer is in how many things depended on each fact.

### The model

Draw your canon as a **dependency graph**. Each node is a fact or a piece of content. An arrow from `A` to `B` means `B` relies on `A`: if `A` changed, `B` might become wrong. A quest that sends you to the Tidewardens' hall relies on the Tidewardens existing. A raid in Harrow's tomb relies on Harrow having died.

For a fact `x`:

```
Desc(x)   = every node reachable from x by following arrows
Review(x) = {x} ∪ Desc(x)
radius(x) = |Desc(x)|
W(x)      = Σ c(y) over y in Review(x) that are not frozen
F(x)      = the frozen nodes in Review(x)
```

- `Desc(x)` is the set of **descendants**: everything that depends on `x`, directly or through other facts.
- `Review(x)` is the **review set**: what someone must reread if `x` changes.
- `radius(x)` is the **blast radius**, the number of descendants.
- `c(y)` is the **revision cost** of node `y`, in writer-days: the work to check it and rewrite it if needed. A bible sentence costs little. A voiced quest chain costs a lot. A raid with a boss built around the fact costs most.
- A node is **frozen** if it cannot be revised at all: a printed novel, a physical manual, a cinematic already in players' hands, a statement from the lead writer that went viral. Frozen nodes are listed in `F(x)`, not added to the cost, because no amount of work fixes them.

The model assumes a change to `x` might break every descendant. In practice some descendants survive, so `W(x)` is an upper bound on the work. That is the right number to plan with, since you only find out which descendants survive by reviewing them.

### Numbers you can check

Here is a small part of the canon of *Thornmere*, the invented world from weeks 4 and 10. The Drowning began in 912. Harrow the Elder (870 to 941) is a hero of that era.

| Id | Node | Depends on | Cost `c` (writer-days) | Frozen |
|---|---|---|---|---|
| F1 | The Drowning began in 912 when the sea dikes broke | — | 1 | no |
| F2 | Harrow opened the dikes on purpose to drown an invading army | F1 | 1 | no |
| F3 | The Tidewardens were founded in 941 to rebuild the dikes | F1 | 1 | no |
| F4 | Harrow died in 941 holding the last dike | F2, F3 | 1 | no |
| Y1 | Queen Adelmar descends from Harrow | F2 | 1 | no |
| Q1 | Quest chain "The Dikewalk" | F3 | 8 | no |
| T1 | Tidewarden reputation faction | F3 | 5 | no |
| I1 | Item text on "Harrow's Signet" | F4 | 0.5 | no |
| D1 | Dungeon "The Drowned Archive" | F1, F2 | 15 | no |
| R1 | Raid "Harrow's Tomb" | F4, D1 | 30 | no |
| Y2 | Ysolde's coronation quest chain | Y1 | 10 | no |
| N1 | Printed novella *The Last Tidewarden* | F3, Q1 | — | yes |

Compute the blast radius of F2 by following the arrows. F2 feeds F4, Y1 and D1. F4 feeds I1 and R1. Y1 feeds Y2. D1 feeds R1, which you already have. So `Desc(F2) = {F4, Y1, D1, I1, R1, Y2}`, radius 6. The review set adds F2 itself, so `W(F2) = 1 + 1 + 1 + 15 + 0.5 + 30 + 10 = 58.5` writer-days. No frozen nodes.

Now the rest:

| Fact changed | Radius | Cost `W` (days) | Frozen touched |
|---|---|---|---|
| F1, the date of the Drowning | 11 | 73.5 | N1 |
| F2, Harrow opened the dikes | 6 | 58.5 | none |
| F3, Tidewardens founded 941 | 6 | 45.5 | N1 |
| F4, Harrow died at the last dike | 2 | 31.5 | none |
| D1, the Drowned Archive dungeon | 1 | 45 | none |
| I1, the signet's item text | 0 | 0.5 | none |

Three things stand out.

First, the root is everything. F1 sits under every other node. Changing the date of the Drowning means reviewing the whole setting, and it touches a printed book you can never fix. Roots should be the vaguest facts in your bible, which is week 4's precision gradient seen from the other side.

Second, radius and cost disagree. F4 has only two descendants but costs 31.5 days, because one of them is a raid. D1 has one descendant and costs 45. Counting references is a useful first check. Weighting them by what they cost to revise is what you plan with.

Third, frozen nodes change the question. F3 costs less than F2 to revise, but it reaches the novella. Any change to F3 leaves a permanent contradiction with a printed book, and no budget fixes that. For a frozen node, your only options are to leave the old fact true or to demote the frozen work to a lower tier of canon (section 4).

The graph in code, which you will extend in the lab:

```python
# id: (depends on, revision cost in writer-days, frozen?)
CANON = {
    "F1": ([], 1, False),            # the Drowning began in 912
    "F2": (["F1"], 1, False),        # Harrow opened the dikes on purpose
    "F3": (["F1"], 1, False),        # the Tidewardens were founded in 941
    "F4": (["F2", "F3"], 1, False),  # Harrow died holding the last dike
    "Y1": (["F2"], 1, False),        # Queen Adelmar descends from Harrow
    "Q1": (["F3"], 8, False),        # quest chain: The Dikewalk
    "T1": (["F3"], 5, False),        # Tidewarden reputation faction
    "I1": (["F4"], 0.5, False),      # item text: Harrow's Signet
    "D1": (["F1", "F2"], 15, False), # dungeon: the Drowned Archive
    "R1": (["F4", "D1"], 30, False), # raid: Harrow's Tomb
    "Y2": (["Y1"], 10, False),       # Ysolde's coronation chain
    "N1": (["F3", "Q1"], 0, True),   # printed novella: The Last Tidewarden
}

def descendants(canon, fact):
    """Every fact that depends on `fact`, directly or through others."""
    children = {f: [g for g, (deps, _, _) in canon.items() if f in deps] for f in canon}
    seen, stack = set(), [fact]
    while stack:
        for child in children[stack.pop()]:
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen

def blast(canon, fact):
    review = descendants(canon, fact) | {fact}
    cost = sum(canon[f][1] for f in review if not canon[f][2])
    frozen = sorted(f for f in review if canon[f][2])
    return len(review) - 1, cost, frozen

for fact in ("F1", "F2", "F3", "F4", "D1", "I1"):
    radius, cost, frozen = blast(CANON, fact)
    print(f"{fact}: radius {radius:>2}, cost {cost:>5} days, frozen {frozen}")
```

It prints:

```
F1: radius 11, cost  73.5 days, frozen ['N1']
F2: radius  6, cost  58.5 days, frozen []
F3: radius  6, cost  45.5 days, frozen ['N1']
F4: radius  2, cost  31.5 days, frozen []
D1: radius  1, cost    45 days, frozen []
I1: radius  0, cost   0.5 days, frozen []
```

### Three ways to make the same change

Suppose the writers for the next expansion want Harrow to be morally grey. The pitch is that the Drowning was not a noble sacrifice. Three retcons deliver it.

| Retcon | What changes | Review set | Cost | Contradictions left |
|---|---|---|---|---|
| Substitutive: "the dikes failed; Harrow lied about it" | F2 rewritten | F2 and its 6 descendants | up to 58.5 days | none if all revised |
| Subtractive: "F2 was a legend, not history" | F2 demoted to in-world rumor | the same 7 nodes must be re-supported or demoted | 0 to 58.5 days | descendants that still state F2 as fact |
| Additive: "a spy told Harrow the enemy was inside; they were not" | new node F2b depending on F2 | F2b only, plus a check of F2's siblings | about 3 days for the new content | none |

The additive version keeps every shipped fact true. Harrow still opened the dikes on purpose, still died at the last one, and his tomb still stands. What changes is why. It costs the new content and nothing else. That is why experienced continuity teams reach for additive retcons first. They only work if the new fact can be squared with what players already saw, which is a writing problem, not a budget problem.

### A visual you can move

Open the interactive. The left panel shows the canon graph the way a writer sees it when proposing a change: one node highlighted, the sentence they want to edit. The right panel shows the same graph with the review set lit up, costs as node sizes, frozen nodes outlined in the warning colour, and a running total. Click F2. The left panel shows one small node. The right panel lights six more, including the raid. Now switch the retcon type to "additive". A new node appears under F2, and the lit set on the right collapses to that one node. Click F1 and try every type. Nothing you do avoids the frozen novella except leaving F1 alone.

### Cross-game recognition

**World of Warcraft, the draenei (2007).** A substitutive retcon of a fact in the Warcraft III manual. In graph terms, the manual's account of Sargeras and the eredar had very few descendants inside World of Warcraft, so the review set was small, but the manual was frozen. Blizzard chose the only option a frozen node allows. It left the contradiction standing and let the new version win. Metzen's admission was a public statement of the precedence rule: newer game content outranks older print.

**World of Warcraft, Chronicle (2016 onward).** A consolidation pass: rewriting the roots of the graph as a single, checked reference, with internal readers and Blizzard's historians reviewing it. Two policy details are worth copying. Matt Burns stated that canon information left out of *Chronicle* still counts, so the books add authority without deleting everything they omit. And at BlizzCon 2019, Steve Danuser said *Chronicle* is written from the titans' point of view. Attributing a history to a biased narrator is an additive safety valve, because a later story can reveal that the narrator was wrong without contradicting what the book said.

**Star Wars, 25 April 2014.** A subtractive retcon at franchise scale. Lucasfilm had tracked the franchise's continuity in the Holocron, a database of over 55,000 entries run since 2000 by a continuity database administrator, Leland Chee. It sorted canon into levels in order of precedence: G-canon (George Lucas's films), T-canon (the Clone Wars TV series), C-canon (most books, comics and games), S-canon (secondary: older material that other sources contradicted), and a low D-canon level for an unreleased comedy series. In 2014, Lucasfilm kept the films and The Clone Wars and renamed everything else "Legends", no longer canon. In graph terms it cut the arrows from the films down into the whole C-canon branch, so new work need not review any of it. One live game sat inside that branch. Star Wars: The Old Republic kept shipping, and Wookieepedia notes it became the only continuing source of new Legends material. A subtractive retcon doesn't delete a branch. It detaches it, and anything still growing on the branch grows on its own.

**Final Fantasy XIV, 2012 to 2013.** The original 2010 game failed and had to be rebuilt. Rather than pretend it never happened, the team wrote an ending into the old game's last year. Dalamud, the lesser moon, fell and released the primal Bahamut in the Seventh Umbral Calamity. The old servers closed on 11 November 2012 after a final battle that all players were invited to, and A Realm Reborn launched in August 2013 set five years later. That is an additive retcon at world scale. Everything in 1.0 stays history. One new event explains why the map, the cities and the game changed, and the game later marks its main story quests with a meteor icon that recalls Dalamud's fall.

Four cases, one graph. Blizzard accepted a contradiction with a frozen node that had few dependents, and later consolidated the roots. Lucasfilm cut a whole branch loose. Square Enix added a node that explained everything downstream.

### Eyes-open design judgment

- **Keep roots vague and leaves specific.** The more a fact is depended on, the less precise it should be. Put exact dates, names and numbers at the leaves, where the blast radius is small.
- **Record the arrows as you ship.** The "referenced by" column from week 4 is the dependency graph. Without it, you cannot compute a blast radius, and every retcon becomes a guess.
- **Price frozen media before you publish it.** A tie-in novel that states a root fact freezes that fact. Either let tie-ins touch only leaves, or accept that they will be the first thing demoted.
- **Prefer additive retcons, and don't abuse them.** Each additive retcon adds a node with its own descendants. A setting with too many "but actually" layers becomes hard for players to follow. Use substitutive retcons for leaves (a wrong date on an item) and additive ones for roots.
- **Decide your precedence rule before the first conflict.** When two sources disagree, someone must know which wins, and that rule should be written in the bible, not settled in an argument after launch.

### Check yourself (worked example)

1. Compute the radius, cost and frozen set for Y1 and for Q1.
2. A new expansion adds a dungeon, "The Signet Vault" (cost 12), that depends on I1 and Y2. What is the new radius and cost of F2?

<details>
<summary>Answers</summary>

1. Y1: descendants {Y2}, radius 1, cost `1 + 10 = 11`, no frozen. Q1: descendants {N1}, radius 1, cost 8 (N1 is frozen and adds no cost), frozen {N1}.
2. The vault is a descendant of F2 through both I1 and Y2, but it counts once. Radius 7, cost `58.5 + 12 = 70.5` days.

</details>

## 3. Why contradictions are certain: the lookup problem

Metzen's explanation for the draenei contradiction was that he forgot. That is not a character flaw. It is arithmetic.

Suppose a new quest chain touches `k` existing facts: names, dates, who knows what, who is alive. For each one the writer relies on memory, and memory is wrong with some small probability `ε` per fact. The chance that the quest contradicts canon somewhere is the complement rule from MA102 week 3:

```
P(at least one contradiction) = 1 − (1 − ε)^k
```

| Facts touched `k` | `ε = 0.02` (from memory) | `ε = 0.002` (looked up) |
|---|---|---|
| 10 | 18.3% | 2.0% |
| 20 | 33.2% | 3.9% |
| 50 | 63.6% | 9.5% |
| 100 | 86.7% | 18.1% |
| 200 | 98.2% | 33.0% |

Check the middle row. `0.98^50 = 0.364`, so `1 − 0.364 = 0.636`.

A writer who is right 98% of the time will contradict canon in most expansion-sized stories. The fix is not better writers. It is a continuity database that makes checking cheap enough that writers do it. Cutting `ε` tenfold cuts the 50-fact risk from 64% to under 10%. That is what the Holocron was for, and why Lucasfilm staffed it with a dedicated administrator from 2000.

The two models connect. Contradictions are more likely when `k` is large, and `k` is large for content that sits deep in the graph and touches many facts. The same content, if it contradicts a root, has the largest blast radius. So a continuity team should spend its checking time on content that touches roots.

## 4. Canon tiers and precedence

When two canon facts conflict, you need a rule that says which one wins. A **canon tier** is a rank attached to every source, and the **precedence rule** says the higher tier wins. The Holocron's G, T, C, S levels are the best documented example.

A workable set of tiers for an MMO bible:

| Tier | Includes | Can be overridden by | Typical revision cost |
|---|---|---|---|
| Core | The bible's root facts, reviewed by the continuity lead | Only a deliberate, logged retcon | High, many descendants |
| Game | Anything shipped in the game: quests, dialogue, items, zones | Core | Medium to high |
| Tie-in | Novels, comics, short stories, websites | Core and game | Frozen once printed |
| Flavor | In-world books, rumors, songs, character opinions | Anything above | Low, and may be wrong in-world |

Three rules make tiers work.

1. **Tiers are assigned when content is commissioned, not when a conflict appears.** A tie-in writer who knows their book is tier 3 knows to touch leaves.
2. **Within a tier, conflicts are bugs.** If two game-tier facts disagree, one must be fixed, and the blast radius tells you which one is cheaper to fix.
3. **The flavor tier is a planned escape route.** A fact stated by an in-world author with a motive (the titans in *Chronicle*, a court historian, a propaganda poster) can be overturned later by an additive retcon. It gives writers a way to add richness without adding roots. [Week 6](w06-religion-and-myth-in-fiction.md) showed how several in-world accounts of one myth let players work out what really happened. The same device protects your roots, because an account can be wrong without the world being wrong.

## 5. The continuity workflow

Put the model into a weekly routine.

1. **Every fact has an owner and an id.** GD202 week 4's "one writer per fact" rule applies to the whole setting. The owner approves changes to it.
2. **Every shipped piece of content records its dependencies.** A quest's ticket lists the fact ids it relies on. This takes a minute per quest and builds the graph for free.
3. **Every proposed retcon comes with a blast report.** Radius, cost, frozen nodes, and which of the three retcon types was chosen and why.
4. **Every conflict found is logged, not only fixed.** A log of contradictions tells you where `ε` is high, which usually means a part of the setting that is poorly documented.
5. **Consolidate roots periodically.** Every few years, rewrite the roots as a clean reference, the way *Chronicle* did, and re-link the graph to it.

## In-class activity (25 minutes)

In groups of three, you are the continuity team for *Thornmere*'s next expansion. The design lead has three requests:

- A. Move the founding of the Tidewardens (F3) from 941 to 925, so they can appear in a flashback during the Drowning.
- B. Reveal that Queen Adelmar is not Harrow's descendant (Y1), to set up a succession crisis for Ysolde.
- C. Change the text of Harrow's Signet (I1) to hint at the spy.

1. (10 min) For each request, compute the blast radius, cost and frozen nodes with the table in section 2.
2. (10 min) For each, propose the cheapest retcon type that still delivers the design goal, and estimate its cost.
3. (5 min) Rank the three requests by risk and write one sentence to the design lead about A.

Expected output: a three-row table and a sentence. Request A touches the frozen novella through F3 (radius 6, 45.5 days). An additive solution (a group of dike-keepers during the Drowning that later became the Tidewardens) avoids the change entirely. B costs 11 days as a substitutive retcon of a fact with one dependent. C is a leaf, and costs half a day.

## Common misconceptions

- **"A retcon means we made a mistake."** Many retcons are deliberate, made because a better story needs a different past. The model prices both kinds the same way.
- **"The number of references tells you the cost."** Radius counts dependents. Cost weights them. A fact with two dependents, one of them a raid, can cost more than a fact with six cheap ones.
- **"Declaring something non-canon makes the problem go away."** A subtractive retcon detaches a branch. Players still own the books, and anything still being written on that branch keeps going, as The Old Republic did after 2014.
- **"Good writers don't need a database."** At a 2% error rate per fact, a 50-fact story contradicts canon about two times in three. The database is what makes checking cheap enough to do.

## Check yourself

1. A new quest touches 30 canon facts. With `ε = 0.01`, what is the chance it contradicts something? How low must `ε` be to bring that under 5%?
2. In the Thornmere graph, the tie-in team proposes a second novella that depends only on F1. What does it do to the radius and frozen set of every fact? Which facts become frozen-reaching that were not before?
3. A comic (tie-in tier) says the Drowned Archive flooded in 912. The dungeon (game tier) says 915. The bible's core timeline says nothing. What wins under the tier table, and what should the continuity team do next?
4. Classify each as substitutive, subtractive or additive: (a) FFXIV's Seventh Umbral Calamity; (b) the Star Wars Legends announcement; (c) the draenei history in The Burning Crusade.

<details>
<summary>Answers</summary>

1. `1 − 0.99^30 = 1 − 0.740 = 26.0%`. For 5%: `(1 − ε)^30 ≥ 0.95`, so `1 − ε ≥ 0.95^(1/30) = 0.99829`, and `ε ≤ 0.0017`.
2. Only F1 has it as a descendant, so F1's radius rises from 11 to 12 and its frozen set becomes {N1, the new novella}. No other fact reaches it. Adding frozen work under the root freezes the root a second time, but it spreads to nothing else.
3. The dungeon wins, since the game tier outranks tie-in. The comic is frozen once printed, so the team logs the conflict, keeps 915 in the bible, and considers an additive fix: for example, a flavor-tier line that the Archive's upper halls flooded in 912 and its vaults in 915.
4. (a) additive; (b) subtractive; (c) substitutive (the older manual fact was replaced, and the contradiction was left standing because the manual is frozen).

</details>

## Lab / assignment hook

[Lab 11, the continuity checker](../labs/lab11.md). You implement blast radius, cycle and dependency validation, and tier-based conflict resolution, run it on a larger *Thornmere* canon file with planted problems, then build the dependency graph for your own world bible and write a retcon memo for one change. It feeds the "canon and continuity" chapter of the final world bible (60%).

## Sources

- Warcraft Wiki, "Draenei", section "Design and retcon" (current). Chris Metzen's statement during The Burning Crusade's development (about 2006) that the new draenei history contradicted the Warcraft III manual, which he had forgotten, and that Blizzard would keep the new lore. https://warcraft.wiki.gg/wiki/Draenei
- Warcraft Wiki, "World of Warcraft: Chronicle" (current). Purpose (to codify and clarify Warcraft history); internal readers and historians; Matt Burns on omitted canon still counting; Steve Danuser at BlizzCon 2019 on the titans' point of view; volumes 1 to 4 (2016, 2017, 2018, 2024). https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Chronicle
- Wikipedia, "Star Wars Legends" (accessed September 2026). The Holocron database, Leland Chee's hiring in 2000, over 55,000 entries, the G, T, C, S and D canon levels in order of precedence, and the 25 April 2014 announcement that renamed the Expanded Universe "Legends".
- Wookieepedia, "Star Wars: The Old Republic" (current). The game as the only remaining continuing source of Legends material after 25 April 2014. https://starwars.fandom.com/wiki/Star_Wars:_The_Old_Republic
- Wikipedia, "Final Fantasy XIV (2010 video game)" (accessed September 2026). The Seventh Umbral Era storyline written as an in-story reason for the relaunch; servers closed 11 November 2012 after a final battle.
- Wikipedia, "Final Fantasy XIV" (accessed September 2026). A Realm Reborn released August 2013, set five years after the Seventh Umbral Calamity.
- Final Fantasy XIV Online Wiki (consolegameswiki), "Main Scenario Quests" (accessed September 2026). All main scenario quests carry the meteor icon, meant to resemble Dalamud as it fell in version 1.x.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".

## Interactive spec: examples/w11-retcon-blast-radius.html

**The one insight the visual must make obvious:** the fact a writer wants to change looks like one small node, but its review set can be most of the setting, and the kind of retcon you choose (not the fact you pick) decides how much of that you pay for. Frozen nodes stay lit whatever you do.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.

- **Left, "What the writer sees".** The Thornmere graph (12 nodes, 15 arrows, from the table in section 2), laid out top to bottom in fixed positions by depth: row 1 F1; row 2 F2, F3; row 3 F4, Y1, D1, Q1, T1; row 4 I1, R1, Y2, N1. Nodes are equal-size circles with their id; only the selected node is filled with the accent colour. The node's sentence appears in a caption below the panel.
- **Right, "What it costs".** The same layout and arrows. Nodes in the review set are filled; node radius scales with `sqrt(c)` (minimum radius for cost 0.5 so it stays visible). Frozen nodes in the review set get a thick outline in the warning colour and a small "frozen" label. Nodes outside the review set are faded to 25% opacity.
- **Stat row under both panels:** radius, cost `W` in writer-days (one decimal), frozen nodes touched (ids), and "contradictions left" (see below).

**Controls.**

1. **Select a fact**: click or tap any node in either panel, or use a labelled select listing all 12 ids with short names. Keyboard: nodes are focusable buttons in reading order (row by row, left to right); Enter or Space selects.
2. **Retcon type**: segmented control, Substitutive (default), Subtractive, Additive.
3. **Add a node** (optional stretch): a button "Add the Signet Vault" that adds node V (cost 12) depending on I1 and Y2, placed in row 5, to reproduce check-yourself question 2. A second press removes it.
4. **Reset** button.

**Rules per retcon type.**

- *Substitutive*: review set `{x} ∪ Desc(x)`; cost `W(x)`; contradictions left = number of frozen nodes in the set.
- *Subtractive*: same review set and frozen list; cost shown as a range "0 to W(x)" (0 if every descendant is demoted with it, `W(x)` if all are re-supported); contradictions left = frozen nodes in the set.
- *Additive*: a new node `x*` appears as a child of `x` (dashed outline, cost 3). Review set is `{x*}` only; cost 3; contradictions left 0. Frozen nodes are drawn with their outline but not lit.

An `aria-live` region states the result in one sentence, e.g. "Substitutive change to F2: 6 dependents, 58.5 writer-days, no frozen works."

**Formulas.** Descendants by breadth- or depth-first search over the arrows (each node counted once). `W(x) = Σ c(y)` over non-frozen `y` in the review set.

**Test values (must match).**

| Selected | Type | Radius | Cost | Frozen |
|---|---|---|---|---|
| F1 | Substitutive | 11 | 73.5 | N1 |
| F2 | Substitutive | 6 | 58.5 | none |
| F3 | Substitutive | 6 | 45.5 | N1 |
| F4 | Substitutive | 2 | 31.5 | none |
| D1 | Substitutive | 1 | 45.0 | none |
| Y1 | Substitutive | 1 | 11.0 | none |
| Q1 | Substitutive | 1 | 8.0 | N1 |
| I1 | Substitutive | 0 | 0.5 | none |
| F2 | Additive | 0 | 3.0 | none |
| F2, with Signet Vault added | Substitutive | 7 | 70.5 | none |

**First screen.** F2 selected, Substitutive. Caption above the panels: "One sentence on the left. Seven nodes and a raid on the right." The student's first move (switching to Additive) collapses the right panel to one dashed node.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no animated lighting when set). Colour is never the only cue: the review set also uses fill and the frozen nodes use a label. No game art or logos.
