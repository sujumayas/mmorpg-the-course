# MMO406 · Week 03 — Factions and Conflict

**Why this matters:** Factions are where lore meets systems most directly. The player picks one at character creation, earns reputation with others, and fights or trades with the rest. How you wire the relationships between factions decides whether your world's politics can move at all, and where the next betrayal will come from. This week gives you a way to see that wiring and measure how much pressure it holds.

**You will be able to:**
- Compute the number of balanced and unbalanced triads in a faction web and state which relationships are under pressure.
- Predict which single change of alliance would relieve the most pressure, and use that prediction to plan a story beat.
- Critique the faction structures of shipped MMOs (World of Warcraft, Dark Age of Camelot, The Elder Scrolls Online, EVE Online) in one notation.
- Design a faction web for your world bible with a target amount of tension and at least one relationship backed by a game system.

**Before class:** Cartwright and Harary, "Structural balance: a generalization of Heider's theory" (1956). Read the introduction and the definitions of balance; skip the proofs. Reread [MMO303 week 9](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md), the Dark Age of Camelot paragraph, and your lab 01 ledger.

**Prerequisites from earlier courses:** [MMO406 week 1, setting as system](w01-setting-as-system.md) (structural tensions, refill). [MMO406 week 2, geography and ecology](w02-geography-and-ecology.md) (resources that give factions something to fight over). [MMO303 week 9, intransitivity and counters](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) (why a three-way war rotates its leader; we don't redo that here). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (who a faction choice separates you from).

**Interactive:** [Faction web](../examples/w03-faction-web.html). Keep it open during section 2.

---

## 1. What a faction is for

A **faction** is any group in your world that has its own wants and that players can stand in a relationship with. Kingdoms, guilds, churches, pirate fleets, a merchant house, a clan of wolves that talk. The word covers groups players must join (Horde or Alliance), groups they earn standing with (a city's traders), and groups they fight (bandits).

In a persistent world, a faction does work in both the fiction and the systems. Check each faction in your bible against four questions.

**What does it want?** A faction without a want is a costume. Its want should block or support another faction's want, which is what makes it part of week 1's tension ledger.

**What does it hold?** Territory, a resource, a route, a secret. Week 2 gave you the tools to put scarce resources in particular regions. A faction that holds a region inherits that region's resources, and so inherits its trade partners and enemies.

**How do players touch it?** Reputation, vendors, quests, a city to live in, a flag that makes you attackable. If players never touch a faction through a system, it exists only in text, and week 1 warned what happens to tensions that live only in text.

**Who is its face?** One or two named characters who speak for the faction. Players relate to people, not organisations. GD202 week 5 covered writing them.

A faction that answers all four is playable. The rest of this lecture is about the part that sits between factions: their relationships.

## 2. Worked example: the enemy of my enemy

### The hook

The Elder Scrolls Online (April 2014) splits its world into three alliances at war over the imperial province of Cyrodiil. Each alliance joins three peoples. One of them, the Ebonheart Pact, joins the Dunmer (dark elves), the Nords and the Argonians. In the setting's history, the Dunmer had enslaved Argonians for a long time. The Pact was formed during an invasion, and the treaty that founded it freed Argonians held as slaves by the Dunmer, in thanks for their help. The game's own lore describes the Pact struggling to reconcile three very different partners.

So the writers put a former slaver people and their former slaves in one alliance, at war with two other alliances. Why build an ally relationship on top of that history? Because it is unstable, and instability is where stories come from. This section gives you a way to measure that.

### The model

Draw your factions as points. Between each pair, draw a line with a sign.

- `+1` means allies (or friendly).
- `−1` means enemies (or hostile).
- No line means neutral: the two have no strong relationship.

A **triad** is any three factions that all have a signed line between each pair. Multiply the three signs.

```
triad sign = s(A,B) × s(B,C) × s(A,C)
balanced   if the product is +1
unbalanced if the product is −1
```

The psychologist Fritz Heider proposed this idea for people in 1946, and Dorwin Cartwright and Frank Harary generalised it to whole networks in 1956. It is called **structural balance**. The four possible triads read like proverbs.

| Signs | Product | Reading | Balanced? |
|---|---|---|---|
| `+ + +` | + | three friends | yes |
| `+ − −` | + | two friends against a common enemy | yes |
| `+ + −` | − | my two friends hate each other | no |
| `− − −` | − | everyone against everyone | no |

An unbalanced triad is under pressure. In the `+ + −` case, one of the friends is being pulled toward choosing a side. In the `− − −` case, any two of the three have a reason to team up against the third. Balance theory predicts that relationships tend to change until triads are balanced. For a writer, an unbalanced triad is a place where a relationship is likely to change, which is the definition of a story beat.

Count the pressure in a whole web with the **tension index**:

```
T = unbalanced triads / complete triads
```

With `n` factions and every pair signed, there are `C(n, 3)` triads. Four factions give 4. Five give 10. Six give 20.

Two results make the model useful.

**Balanced means two camps.** Harary showed that a fully signed web is balanced (every triad balanced) exactly when the factions can be split into at most two camps, with every relationship inside a camp positive and every relationship across camps negative. A world with zero tension is a two-bloc war, and nothing else.

**One changed relationship touches `n − 2` triads.** Each pair of factions sits in a triad with each of the other `n − 2` factions. Flip that pair's sign and every one of those triads flips from balanced to unbalanced or back. So a betrayal between two factions in a six-faction world changes the balance of four triads at once.

### Numbers you can check

An invented setting with four factions: the Crown, the Temple, the Guild and the Clans.

| Web | Relationships | Unbalanced / triads | `T` |
|---|---|---|---|
| All at war | every pair `−` | 4 / 4 | 100% |
| Two blocs | Crown and Temple `+`, Guild and Clans `+`, all others `−` | 0 / 4 | 0% |
| The bribe | two blocs, then the Guild buys the Temple: Temple and Guild become `+` | 2 / 4 | 50% |

Check the bribe row by hand. The triad Crown, Temple, Guild has signs `+` (Crown and Temple), `+` (Temple and Guild), `−` (Crown and Guild). The product is negative, so it is unbalanced. The Crown's ally is now friends with the Crown's enemy. The triad Temple, Guild, Clans has `+`, `+`, `−` and is unbalanced too. The other two triads do not contain the Temple and Guild pair, so they stay balanced. Two unbalanced triads is exactly `n − 2 = 2`.

Now read the table as a writer. The two-bloc web has zero tension, and its only story is the war itself. The bribe has put pressure on precisely two relationships. Either the Crown breaks with the Temple, or the Guild breaks with the Clans, or the bribe is exposed and reversed. Each option is an expansion-sized plot beat, and the model has named them for you.

The same count in code. You will extend it in the lab.

```python
from itertools import combinations

def tension(factions, edges):
    """Count unbalanced triads. edges maps a sorted pair to +1 or -1; a missing pair is neutral."""
    unbalanced = total = 0
    for a, b, c in combinations(factions, 3):
        signs = [edges.get(tuple(sorted(p))) for p in ((a, b), (b, c), (a, c))]
        if None in signs:
            continue  # a neutral edge: not a complete triad
        total += 1
        if signs[0] * signs[1] * signs[2] < 0:
            unbalanced += 1
    return unbalanced, total

def pair(a, b):
    return tuple(sorted((a, b)))

F = ["Crown", "Temple", "Guild", "Clans"]
war = {pair(a, b): -1 for a, b in combinations(F, 2)}
blocs = {**war, pair("Crown", "Temple"): 1, pair("Guild", "Clans"): 1}
bribe = {**blocs, pair("Temple", "Guild"): 1}
for name, g in [("all at war", war), ("two blocs", blocs), ("the bribe", bribe)]:
    print(name, tension(F, g))
```

It prints:

```
all at war (4, 4)
two blocs (0, 4)
the bribe (2, 4)
```

### The visual

Open the interactive. The left view places your factions on a circle. Click a line to cycle it through ally, enemy and neutral. Unbalanced triads are shaded as filled triangles, so pressure is visible as colour. The right view lists every triad with its three signs and product, gives `T`, and names the single flip that would remove the most unbalanced triads. Start with "all at war" at four factions: every triangle is shaded. Flip any one line to ally. Two triangles clear at once, since that line sat in two triads. Flip the opposite line to ally and the web goes clear. You have made two blocs, as Harary's theorem says you must.

### Cross-game recognition

**World of Warcraft (2004 onward).** Two player factions, the Horde and the Alliance. With two factions there is one relationship and no triad at all, so `T` is not even defined. The war cannot drift toward a new alignment because there is no third party to align with. That makes it very stable, which is what week 1 wanted from a structural tension. Inside the factions, Warcraft uses the model at a smaller scale. In The Burning Crusade (2007), the player chooses between two rival factions in the city of Shattrath, the Aldor and the Scryers. On the Warcraft Wiki's account, reputation gained with the Scryers comes with a loss 10% larger with the Aldor, and the reverse holds too. Treat the player as a node: player `+` Scryers and Scryers `−` Aldor forces player `−` Aldor. The reputation system is structural balance written as code. It never lets the player sit in an unbalanced triad for long.

**Dark Age of Camelot (October 2001).** Three realms, Albion, Midgard and Hibernia, all enemies. One triad, `− − −`, unbalanced. Balance theory predicts that two realms will team up against the third. The game's systems lock each player into a realm, so a formal alliance can't form. The pressure shows up in behaviour instead: MMO303 week 9 describes how the other two realms both press whichever realm is leading. The systems froze an unbalanced triad in place, and players act out the missing alliance every night.

**The Elder Scrolls Online (April 2014).** At the top level, three alliances all at war over Cyrodiil, the same `− − −` triad as Dark Age of Camelot. Inside each alliance are three peoples with nominally positive relationships. The Ebonheart Pact's Dunmer and Argonian edge is `+` by treaty and `−` by history. In the model that pair is a contested edge, one the setting could flip, and each flip would change the balance of every triad the pair sits in. In practice, ESO's systems softened the alliance structure. The One Tamriel update (Update 12, October 2016) removed most alliance restrictions on zones outside the war, so players of any alliance could travel and group across the map. Like cross-faction play in World of Warcraft (week 1), that change serves players who want to play together, and it weakens the system that kept the alliances apart.

**EVE Online (faction warfare 2008 to March 2023, then pirate militias from late 2023).** Faction warfare has two war zones: Amarr against Minmatar, and Caldari against Gallente. From 2008 the Amarr and Caldari militias were allied, as were the Minmatar and Gallente. That is the two-bloc web, fully balanced, `T = 0`, and a Gallente pilot could help the Minmatar fight the Amarr. The Allegiance update (March 2023) removed those alliances. Across the two zones the militias are now neither allied nor at war, which in our notation is neutral. So the empire web has no complete triads, and the two wars can't pull each other into a new alignment. The Havoc expansion (2023) then added two pirate militias. Amarr and Minmatar militia members are at war with the Angel Cartel, and Caldari and Gallente members with the Guristas. That creates two `− − −` triads, one in each war zone. The model says each is under pressure for two members to team up. Whether players do so is the kind of emergent story EVE is known for (GD202 week 9).

Four games, one notation. WoW keeps its main war outside the model's reach by having only two sides, and uses balance deliberately in its reputation system. Dark Age of Camelot and ESO freeze an unbalanced triad with systems. EVE keeps its wars in separate boxes, then adds a third party to each box.

### Eyes-open design judgment

- **Zero tension is stable and flat.** A two-bloc world is the only balanced world. It gives you a war that never drifts, which is good for PvP systems and poor for political stories. If you choose two factions, plan where political stories will come from (inside each faction, or from outside threats).
- **Unbalanced triads can be frozen by systems.** Realm locks, alliance-only zones and separate cities stop a `− − −` triad from resolving into an alliance. The pressure doesn't vanish. It turns into behaviour, like two sides focusing the leader. Decide whether you want that behaviour.
- **Contested edges are your most valuable writing material.** A relationship that is `+` by treaty and `−` by history, like the Pact's, can flip in either direction. Mark these in your bible. They are pre-built story beats that affect `n − 2` triads each.
- **Neutral edges are a tool.** Leaving pairs neutral, as EVE's cross-zone empire pairs are, keeps conflicts in separate boxes. That limits how far one betrayal spreads. Use neutral edges when you want local stories that don't reshape the whole map.
- **Player choice can be a node.** When players join or earn standing with factions, each player's own triads matter. Exclusive reputations like the Aldor and Scryers keep those triads balanced by force. Letting a player be friendly with two enemies can be a deliberate story (a double agent) or a design leak (players farm both sides with no cost).
- **The model ignores strength.** Balance counts signs, not how strong a relationship is or how big a faction is. A tiny faction's alliance counts as much as an empire's. Use the model to find pressure, then use judgment about which pressure matters.

## 3. How many factions?

The number of player factions is one of the earliest and hardest to change decisions in an MMO, because content, cities, PvP and chat channels all get built around it. The model gives you part of the answer.

**Two** gives zero triads among player factions and the most stable identity. Population imbalance is the classic risk: if one side has more players, the other side's PvP and world content feel worse, and nothing in the structure pushes back.

**Three** gives one triad, always unbalanced if all three are at war. The pressure tends to act against whichever side leads, which MMO303 week 9 describes as a rotating lead. This is why three-way PvP designs recur. They build a correction into the structure.

**Many** (four or more player factions, or player-made alliances as in EVE) gives `C(n, 3)` triads and a politics that players, not writers, will drive. That is powerful and hard to write for. Your writers can react to the web, but they cannot plan it.

For NPC factions, the choice is freer, because they don't need cities, chat or PvP balance. A common pattern is a small number of player factions with a larger web of NPC factions around them, where the NPC web carries the unbalanced triads that produce story, and the player factions stay stable.

## 4. Building the faction web for your bible

A procedure for the bible, using weeks 1 and 2.

1. **List factions and their four answers.** Want, holding, player contact, face.
2. **Draw the web.** Sign every pair or mark it neutral. Aim for no more than eight factions in the first draft; `C(8, 3) = 56` triads is already a lot to read.
3. **Count.** Compute `T` and list the unbalanced triads.
4. **Mark contested edges.** For each pair, ask whether history or interest points the other way. Mark those.
5. **Tie at least one relationship to a system.** A reputation pair, a contested region from week 2, a PvP rule. Record it in your week 1 ledger as a structural tension.
6. **Plan the first flip.** Pick the contested edge whose flip you would use for the first expansion. Compute the web after the flip. Check that `T` after the flip is still above zero, or the next expansion starts from a flat world.

## In-class activity (25 minutes)

Groups of three. Use the interactive in custom mode.

1. **Draw (8 min).** Build a five-faction web for a setting of your choice (or the coastal world from week 1: two port cities, the Tide Council, the salt traders, the fishers). Sign every pair or mark it neutral. Record `T`.
2. **Tune (8 min).** Change relationships until `T` is between 20% and 40%. Explain in one sentence why that range might suit a themepark MMO.
3. **Flip (9 min).** Choose one contested edge. Flip it. Record which triads changed and write the one-paragraph story beat that the flip represents.

Expected output: the web before and after (screenshot or sketch), both `T` values, the list of changed triads, and the story paragraph.

## Common misconceptions

- **"Balanced means fair."** Structural balance is about signs forming consistent triads, not about equal power. A balanced world can have one bloc five times larger than the other.
- **"More tension is always better for story."** A web where every triad is unbalanced has pressure everywhere and no clear direction. Players can't tell which relationships matter. Moderate `T` with marked contested edges gives writers a direction.
- **"Three factions at war will naturally ally two against one."** Balance theory predicts pressure in that direction. Systems like realm locks can freeze the triad for decades, and the pressure then shows up in behaviour.
- **"Neutral means nothing is happening."** Neutral edges shape the web by keeping triads incomplete. Turning a neutral edge into an ally or enemy creates new triads, and possibly new pressure, all at once.

## Check yourself

1. Five factions are all at war with each other. How many triads are there, and how many are unbalanced? What is the smallest number of relationships you must change to ally to reach zero tension?
2. Five factions form two blocs, {A, B, C} and {D, E}. A and D sign a secret pact (`+`). How many triads become unbalanced, and which ones?
3. In The Burning Crusade, a player earns 3,000 reputation with the Scryers. Using the Warcraft Wiki's rule, how much reputation do they lose with the Aldor? Explain in model terms what the rule prevents.
4. In EVE's Amarr and Minmatar war zone with the Angel Cartel militia, all three relationships are hostile. Name one single change that would balance the triad, and describe the story it implies.

<details>
<summary>Answers</summary>

1. `C(5, 3) = 10` triads, all `− − −`, so 10 unbalanced. To reach zero you need at most two camps with all-positive relationships inside each. Camps of sizes 1 and 4 need `C(4, 2) = 6` positive edges. Camps of 2 and 3 need `C(2, 2) + C(3, 2) = 1 + 3 = 4`. One camp of 5 needs 10. So the minimum is 4 changes: ally a pair and ally a trio.
2. The A and D pair sits in `n − 2 = 3` triads: A, D with B; with C; with E. Each was balanced (`+ − −` or `− − +` pattern) and now flips, so 3 triads are unbalanced: {A, B, D}, {A, C, D}, {A, D, E}. `T = 3 / 10`.
3. They lose 3,000 × 1.1 = 3,300 Aldor reputation. With the player as a node, player `+` Scryers and Scryers `−` Aldor leaves player `+` Aldor as an unbalanced triad. The rule pushes player and Aldor toward `−` so the player's triad stays balanced. It prevents a player from being honoured by both rivals.
4. Any one relationship becomes `+`. For example, Minmatar and the Angel Cartel become allies. The triad becomes `+ − −` (balanced): the Minmatar and the pirates against the Amarr. Story: Minmatar commanders quietly arm the pirates against their old enemy, and Minmatar militia pilots have to decide whether to go along.

</details>

## Lab / assignment hook

[Lab 03, the faction web](../labs/lab03.md). You write a signed-graph analyser that counts triads, finds the two camps of a balanced web, and ranks single flips by how much pressure they relieve. Then you build and tune the faction web for your own world bible and plan its first flip.

## Sources

- Heider, F. (1946). "Attitudes and cognitive organization." *The Journal of Psychology* 21, 107-112.
- Cartwright, D. & Harary, F. (1956). "Structural balance: a generalization of Heider's theory." *Psychological Review* 63(5), 277-293.
- Harary, F. (1953). "On the notion of balance of a signed graph." *Michigan Mathematical Journal* 2, 143-146. The two-camp characterisation of balanced signed graphs.
- Wikipedia, "Balance theory" and "Signed graph" (checked September 2026). Summary of Heider, Cartwright and Harary; note that three mutual enemies form a clusterable but not balanced triad.
- UESP, "Online:Alliances" and "Lore:Ebonheart Pact" (checked September 2026). ESO's three alliances and their member peoples; the war over Cyrodiil; the Pact's founding treaty freeing Argonians enslaved by the Dunmer; the Pact's difficulty reconciling its members.
- UESP, "Online:One Tamriel" (checked September 2026). Released with Update 12 on 5 October 2016 (PC/Mac); removed most alliance restrictions on zones.
- Wikipedia, "The Elder Scrolls Online" (checked September 2026). Windows and macOS release on 4 April 2014.
- Wikipedia, "Dark Age of Camelot" (checked September 2026). Released 9 October 2001. MMO303 week 9 sources the three-realm structure.
- Warcraft Wiki, "Scryers", "Aldor" and "Reputation" (checked September 2026). The Aldor and Scryers rivalry in Shattrath (The Burning Crusade era); reputation gains with one come with a loss 10% larger with the other; reputation levels from Hated to Exalted.
- EVE University Wiki, "Faction Warfare" (checked September 2026). Introduced in Empyrean Age (2008); the Amarr-Minmatar and Caldari-Gallente war zones; Amarr-Caldari and Minmatar-Gallente militia alliances until the Allegiance update (patch notes of 14 March 2023); pirate militias added in Havoc (2023), with Amarr and Minmatar militias at war with the Angel Cartel and Caldari and Gallente militias at war with the Guristas.

## Interactive spec: examples/w03-faction-web.html

**Purpose.** Let students see structural pressure in a faction web as shaded triangles, and discover by clicking that a pressure-free web always splits into two camps.

**The one insight the visual must make obvious.** Every unbalanced triad is visible as a shaded triangle; flipping one relationship changes exactly `n − 2` triangles at once; and the only way to clear all shading is to form two camps.

**Model (exact).**
- Nodes: `n` factions, 2 to 7. Edges: each unordered pair has state `+1`, `−1` or `0` (neutral).
- A triad is complete if all three of its edges are non-zero. Sign is the product. Unbalanced if negative.
- `T = unbalanced / complete` (show "n/a" when there are no complete triads).
- Balanced check (Harary): if every pair is non-zero and `T = 0`, compute the two camps by two-colouring (start from the first faction, `+` keeps colour, `−` switches). Show the camps.
- Best single flip: for each non-zero edge, compute the number of unbalanced triads after changing its sign; report the edge with the lowest result (ties broken by alphabetical order of the pair) and the new count.

**Controls.**
- Number of factions slider 2 to 7 (custom mode), with editable faction names.
- Click or keyboard-select an edge (Tab through edges, Enter cycles enemy → ally → neutral).
- Presets: "All at war (4)", "Two blocs (4)", "The bribe (4)" (as in the lecture table), "World of Warcraft factions (2)", "Dark Age of Camelot realms (3, all enemies)", "EVE faction warfare with pirate militias (6: Amarr, Minmatar, Caldari, Gallente, Angel Cartel, Guristas; Amarr-Minmatar, Caldari-Gallente, Angels-Amarr, Angels-Minmatar, Guristas-Caldari, Guristas-Gallente enemies; all other pairs neutral)".
- Button "Apply best flip".

**Views.**
- Left: nodes on a circle, edges drawn solid (ally), dashed (enemy) or omitted (neutral), with a legend using both line style and colour. Unbalanced triads filled with a translucent warning colour; balanced complete triads outlined only.
- Right: table of complete triads (three names, three signs, product, balanced yes/no), then `T`, then the best single flip and its result, then the camps when the web is balanced.
- Readout "This edge sits in k triads" when an edge is focused (`k = n − 2` minus any triads made incomplete by neutral edges).

**Test values (must match exactly).**
- All at war, `n = 4`: 4 / 4 unbalanced. `n = 5`: 10 / 10.
- Two blocs (Crown+Temple, Guild+Clans): 0 / 4; camps {Crown, Temple} and {Guild, Clans}.
- The bribe: 2 / 4; unbalanced triads {Crown, Temple, Guild} and {Temple, Guild, Clans}.
- Five factions, blocs {A, B, C} and {D, E}, then A-D set to ally: 3 / 10.
- EVE preset: 2 complete triads, both unbalanced.
- WoW preset: 0 complete triads, `T` shown as "n/a".

**Style.** Shared tokens from `templates/interactive-tokens.css`. No faction emblems, logos or game art; factions are plain labelled circles.
