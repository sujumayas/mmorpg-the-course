# MMO301 · Week 01 — What Is a Virtual World? Bartle's Definition

**Why this matters:** Every MMO you will design this year inherits a set of problems from the word "world." Some come from sharing the space with strangers, some from the space still being there tomorrow, some from the player having one body in it. If you can name which property causes which problem, you can decide which ones your game actually needs, instead of copying a feature list from the last hit.

**You will be able to:**
- State Bartle's defining properties of a virtual world and use them to classify a product, including the hard cases.
- Place a world on Bartle's two dials, persistence and change, and say who the world belongs to as a result.
- Compute how often a player in a sharded world sees nobody else, and how pooling or splitting realms changes that number.
- Critique realm pooling, layering and megaservers as answers to the same density problem, naming what each costs the "shared world" promise.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 1, the opening definitions (pp. 1-5) and "The Basics" through the end of the persistence and change discussion (pp. 51-83). The book is a free PDF from the author's site. Castronova, *Synthetic Worlds* (2005), chapter 1. Write down one game you play that you are unsure counts as a virtual world, and why.

**Prerequisites from earlier courses:** [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) introduced the six-property definition and used it on Colossal Cave and MUD1. This week assumes you have read that section and goes further. [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) separated subscribers, concurrent players and world size; we use its concurrency number `C` directly. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) gives you the "chance of at least one" calculation the worked example rests on. [GD102 week 1, systems thinking](../../GD102-systems-design-and-game-mechanics/lectures/w01-systems-thinking-parts-relationships-emergence.md) supplies the idea that a property of the whole can come from the parts' relationships, which is how "shared" behaves.

**Interactive:** [w01-shared-density.html](../examples/w01-shared-density.html). Keep it open during section 3.

---

## 1. Why a definition is worth an hour

"Virtual world" gets used for almost anything with 3D graphics and a login screen. That looseness costs designers. If a team says "we're making a world" without saying what that means, it will argue for months about features whose only justification is that other worlds have them.

Richard Bartle created MUD1 with Roy Trubshaw at the University of Essex (GS101 week 5). In *Designing Virtual Worlds* he gives a working definition in two parts. First, a description. A virtual world is an environment simulated by a computer, or a network of them. Some of the entities in it are controlled directly by people. Because several people can affect the same environment at once, the world is shared. And because the environment carries on existing and developing, at least to some degree, when nobody is connected, it is persistent.

Second, a list of conventions that separate virtual worlds from their neighbors. Paraphrased:

1. **Physics.** The world runs on automated rules. Players can change the world through those rules but cannot change the rules themselves.
2. **Character.** Each player is represented by one entity in the world that they strongly identify with. They may command an army or a party, but all their interaction with the world and other players goes through that one character.
3. **Real time.** When you act, the world responds almost at once.
4. **Shared.** Other people are in the world with you.
5. **Persistent, at least to some degree.** The world is still there when you are not.

In his 2015 book *MMOs from the Inside Out*, Bartle adds a sixth: **it is not the real world**. That is the list GS101 used.

Bartle tests each property with a near miss. A chat room has no physics. A strategy wargame does not map you onto one character. A play-by-email game is not real time. A single-player game is not shared. A first-person shooter match is not persistent. Each near miss removes exactly one property, which is why the list is useful. It tells you what you lose.

### Two terms to settle now

**Embodiment** is the course's name for the character property: you are present in the world as one body, at one place, at one time. Embodiment is what makes "shared" mean something. Two players can only be together if each of them is somewhere. [Week 10](w10-immersion-identity-and-the-avatar.md) studies identity and the avatar in depth.

**Shard.** Most commercial MMOs run many copies of their world, each on its own server cluster. Players call a copy a server, realm, world or shard. Each copy is persistent and shared, but only with the people on it. Kim Nevelsteen's 2018 technical definition makes this explicit. It asks for a real-time, shared, non-pausable environment whose data spaces together form "one persistent shard." By that reading, a game with 200 realms is 200 virtual worlds that share a rulebook. Keep that in mind. It is the root of this week's worked example.

### What the words used to be

Bartle notes that the field has renamed itself several times. The first worlds were MUDs, after MUD1. Players of social text worlds disliked the combat flavor of "dungeon" and used MU* instead. Graphical worlds were first called persistent worlds, then MMORPGs, once the huge number of simultaneous players became their defining feature. Bartle prefers "virtual world" because it describes the thing, not its genre or its head count. He also separates virtual worlds from **virtual reality**. VR is about the interface, headsets and gloves. A virtual world is about what is on the other side of whatever interface you use. A text MUD is a virtual world. A VR flight simulator is not.

## 2. The properties are dials, not checkboxes

GS101 treated the definition as a test. Does the game have all six? For a designer, each property is better read as a dial you set. The setting decides which problems you inherit.

### Physics

"Automated rules" separates a virtual world from a tabletop role-playing game, where a human referee decides what happens. Bartle calls tabletop games a close call that fails only because they are not automated. The design consequence is large. A referee can improvise a ruling when players try something unexpected. A server cannot. Whatever the rules permit, players will eventually do, at scale, including things no designer imagined. Week 3's Ultima Online case is largely about this.

### Character

One character per player sounds trivial until you look at what breaks it. Players who run a second character to hold items or scout danger (called a **mule**) are stepping outside the one-body rule, and every economy lecture in MMO304 has to deal with them. Games that let one player control a fleet or a town are drifting toward strategy games. The dial here runs from "one body, one identity" to "a player is a company."

### Real time

Real time rules out turn-based play-by-mail worlds, but the dial matters inside real-time games too. A world where travel takes 20 minutes and a world with instant teleport are both real time. They produce very different amounts of sharing, because travel time decides how spread out players are. We return to this in section 3.

### Shared

"Shared" is where a checkbox reading misleads most. Bartle himself flags the edge case. He asks whether a 500-player game with a world so vast that its players never find each other would count, and answers yes, but under protest. The definition is satisfied. The experience is not. Section 3 turns that protest into a number.

### Persistent

Bartle defines persistence by what survives a restart of the whole system. He then describes a ladder of what worlds actually keep:

| Level | What survives a restart | Bartle's example |
|---|---|---|
| 1 | Initial world state and each character's record | AberMUD |
| 2 | Plus what characters were carrying | DikuMUD |
| 3 | Plus certain classes of object, such as corpses | EverQuest |
| 4 | The entire world state | Ultima Online |
| 5 | The entire world state plus new functionality added while running | MOOs |

Higher is not automatically better. Bartle's point is that adventure-style worlds often want low persistence. A puzzle that took weeks to build and changes the whole world when solved ("you can't unlaunch a rocket") is wasted if one group solves it once and it stays solved forever. So the designers reset it. MUD1's resets, which you met in GS101 week 5, were exactly this choice. Persistence also costs storage and save time, which Bartle notes but ranks as the lesser reason.

### A second dial: who gets to change the world

Bartle pairs persistence with a dial he calls **change**: who is allowed to add content directly, outside the normal rules of play. He calls that ability **building**. The dial runs from "only the coders" through "trusted administrators," "experienced players" to "anyone." Most MOOs let anyone build. Heavy role-playing MUSHes let only their coders build.

He plots known worlds on a six-by-six grid of persistence against change (his Table 1.3) and reads the four quadrants as answers to one question. Whose world is it?

- **Low persistence, few builders.** The world belongs to the designers, like a film belongs to its director. Classic adventure MUDs sit here.
- **High persistence, few builders.** Still the designers' world, but players' actions leave lasting marks. Ultima Online and Asheron's Call sit here.
- **Low persistence, many builders.** Players borrow world-changing powers that vanish at the next reset. This quadrant is almost empty.
- **High persistence, many builders.** The world belongs to the players. Social worlds such as LambdaMOO sit here.

Bartle illustrates the gap with the advertising slogans of two companies. Verant, maker of EverQuest, told players "You're in Our World Now." Skotos, which made small text worlds where players built, promised something close to the opposite. Week 2 studies what happens at each end of that dial.

## 3. Worked example: shared is a density, not a checkbox

### The hook

By October 2010 World of Warcraft had more than 12 million subscribers (GS101 week 9). Two years later, players on many realms reported that leveling zones felt dead. How can the biggest MMO of its era feel empty?

Warcraft Wiki's account of the fix is blunt. Blizzard built cross-realm zones to deal with many players at maximum level while lower-level zones were dead. The game had not lost its players. It had lost their overlap. Everyone was on the same realm, but not in the same place at the same level.

### The model

To feel shared, a world needs other people *near you, now*. So count them. Divide your part of the world into **view cells**, patches about the size of what you can see from one spot. Then:

```
n  = k × f × C           other players in your band of the world
M  = Z × v               view cells in that band
λ  = n / M               expected other players in your view
P(alone) = (1 − 1/M)^n   chance nobody else is in your cell
         ≈ e^(−λ)
```

- `C` is concurrency, the number of players online on this shard (GS101 week 9's `C`).
- `f` is the share of them in your **band**, the zones that fit your level or activity.
- `Z` is the number of zones in that band and `v` the number of view cells per zone.
- `k` is a pooling factor. `k = 1` is one realm on its own. Pooling five realms' players into shared zones gives `k = 5`. Splitting one realm into four parallel copies, as layering does, gives `k = 1/4`.
- `λ` (lambda) is the average number of other players you can see.

`P(alone)` is the complement rule from MA102 week 3. Each of the `n` other players is somewhere in the `M` cells. The chance a given player is *not* in yours is `1 − 1/M`. If they are placed independently, the chance all `n` miss you is that number to the power `n`. For large `M` this is very close to `e^(−λ)`, so λ is the only number you need to remember.

The model assumes players spread evenly and independently inside their band. Real players cluster at quest hubs and spawn points, which raises the odds of meeting someone there and lowers them elsewhere. Treat the model as the baseline that clustering moves you away from.

### Numbers you can check

Take one realm with `C = 2,000` players online and zones of `v = 50` view cells each. Eighty percent of the players are at maximum level in 5 endgame zones. Twenty percent are leveling, spread across 35 leveling zones.

| Who | `n` | `M` | `λ` | `P(alone)` | Sees someone |
|---|---|---|---|---|---|
| Endgame player | 1,600 | 250 | 6.40 | 0.16% | 99.8% |
| Leveling player | 400 | 1,750 | 0.23 | 79.6% | 20.4% |

Same realm, same evening. The endgame player is never alone and may be fighting others for spawns, which is the contention problem from GS101 week 5. The leveling player sees nobody four times out of five. The realm is not empty. Its players are in the wrong places for each other.

Now pool leveling zones across realms. Each realm keeps its own endgame, but the 35 leveling zones are shared by `k` realms of the same size:

| Realms pooled `k` | `n` | `λ` | `P(alone)` |
|---|---|---|---|
| 1 | 400 | 0.23 | 79.6% |
| 2 | 800 | 0.46 | 63.3% |
| 5 | 2,000 | 1.14 | 31.9% |
| 10 | 4,000 | 2.29 | 10.2% |
| 11 | 4,400 | 2.51 | 8.1% |
| 20 | 8,000 | 4.57 | 1.0% |

To get `P(alone)` under 10% you need `λ ≥ ln 10 ≈ 2.30`, so `n ≥ 2.30 × 1,750 ≈ 4,030`, which takes 11 realms. Pooling is powerful but slow. Doubling the players you pool does not halve the loneliness. It squares the chance of being alone, because `(e^(−λ))^2 = e^(−2λ)`.

The other end is launch day. On day one everybody is leveling in the starting zones. Say all 2,000 are in 3 starter zones (`f = 1`, `Z = 3`, `M = 150`). Then `λ = 13.3`. Every view cell holds about 13 other players, and every quest monster has a queue. Now split the realm into `L` parallel copies, so `k = 1/L`:

| Copies `L` | `n` | `λ` | `P(alone)` |
|---|---|---|---|
| 1 | 2,000 | 13.33 | 0.00% |
| 2 | 1,000 | 6.67 | 0.12% |
| 4 | 500 | 3.33 | 3.5% |
| 8 | 250 | 1.67 | 18.8% |

Pooling and splitting are the same dial, `k`, turned in opposite directions.

### The visual

Open the interactive. The left view is a map of one band as a grid of view cells, with dots for players placed at random. The right view is the curve of `P(alone)` against `λ`, with a marker for the current settings and a shaded target band. Drag the concurrency slider down from 2,000 to 300 with the "leveling" preset and watch the map empty out while the marker slides up the curve. Then raise "realms pooled" and watch the same map fill back in without a single new player joining the game. The left view makes the point by eye, the right view gives you the number.

### Cross-game recognition

**World of Warcraft, cross-realm zones (patch 5.0.4, 28 August 2012).** This is `k > 1` applied to leveling zones. Players from a pool of realms were placed in the same copy of a zone, so they could see and group with each other. A hotfix on 20 September 2012 stopped the system from pooling players more than three time zones apart. In the model, that is a statement about `f`. Players eight hours apart are online at different times, so pooling them adds to `n` on paper and adds nobody to your evening.

**World of Warcraft Classic, layering (2019).** At Classic's launch, Blizzard ran each realm's outdoor world as several connected copies, called layers, to relieve overcrowding. This is `k = 1/L` at launch. Warcraft Wiki records that Blizzard intended to merge each realm's layers before the second content phase, which went live on 13 November 2019. Once players spread out across levels, `f` in the starter zones fell and the extra copies were no longer needed.

**Guild Wars 2, megaservers (April 2014 feature pack).** Guild Wars 2 launched on 28 August 2012 with separate home worlds. The 2014 megaserver system created map copies for players regardless of home world, so maps would feel more populated. It turns `k` both ways at once. It pools everyone, then opens a new copy of a map when one fills. The system is trying to hold `λ` inside a band rather than maximize it.

**EVE Online (2003 onward).** EVE runs all its players on one shard. GS101 week 9 cites its record of 65,303 accounts online on one server in May 2013. It never needs pooling across realms because there is only one. It still has the density problem inside that shard, since its thousands of star systems play the role of `Z`. Busy trade hubs sit at the endgame end of the table and remote systems at the leveling end.

Four games, one variable. Each fix is a way to move `λ`.

### Eyes-open design judgment

The fixes work on the number, and each one spends something the definition cares about.

- **Pooling weakens persistence of the social kind.** On a single realm you see the same people week after week. You learn names, build reputations, hold grudges. Pool 11 realms and most faces are strangers you will never meet again. You gained `λ` and lost the continuity that makes a community. Week 13 looks at worlds that died partly from this.
- **Splitting weakens "shared."** Two friends on the same realm can end up on different layers and not see each other. The server has quietly redefined which people count as "in the world with you." Players notice, and they exploit it, for example by hopping layers to reach a fresh copy of a rare spawn.
- **The time-zone hotfix is a warning about naive pooling.** Adding players who are not online when you are raises `n` in the spreadsheet only.
- **Density is not only a server setting.** You can also shrink `Z` by removing zones, retire old zones as the population ages, pull players into shared hubs, or schedule world events that concentrate `f` for an hour. These are world-design choices, not infrastructure. They cost content instead of continuity.

The decision you should make deliberately is the target band for `λ`, zone by zone. A crafting hub wants a high `λ`. A horror zone may want a low one. A leveling zone probably wants you to see someone most of the time without competing for every monster. A reasonable starting target for a leveling zone is `λ` between 1 and 3, where you see someone 63% to 95% of the time. Pick your own and defend it. The failure is not choosing and letting concurrency choose for you.

### Check yourself (worked example)

1. A realm has 600 players online. Thirty percent are leveling across 20 zones of 40 view cells each. What are `λ` and `P(alone)` for a leveling player, using `e^(−λ)`?
2. How many such realms must you pool to bring `P(alone)` below 25%?
3. A launch zone has `M = 100` and 1,200 players. How many layers do you need to bring `λ` down to 3 or less?

<details>
<summary>Answers</summary>

1. `n = 0.3 × 600 = 180`, `M = 800`, `λ = 0.225`, `P(alone) ≈ e^(−0.225) ≈ 0.80`.
2. Need `λ ≥ ln 4 ≈ 1.386`, so `n ≥ 1,109`, so `k ≥ 1,109 / 180 ≈ 6.2`. Pool 7 realms.
3. `λ = 1,200 / (100 × L) ≤ 3` gives `L ≥ 4`. Four layers give exactly `λ = 3`.

</details>

## 4. Using the definition as a design tool

A definition earns its place in a design course if it predicts problems. Here is how to use Bartle's list that way.

### Remove a property, remove a class of problems

For any product, go through the properties one at a time and ask what problems that property brings with it. Then check whether the product has them.

| Product type | Missing property | Problems you do not have |
|---|---|---|
| Battle-royale match | Persistence | No economy drift, no veterans versus newcomers, no hoarding. Every match starts equal. |
| Single-player open world | Shared | No contention, no griefing, no density problem, no moderation. |
| Chat or social app | Physics | No exploits of the rules, because there are almost no rules to exploit. |
| Turn-based online strategy | Real time and character | No travel time, no one-body limits. A player can be everywhere their empire is. |
| Persistent survival server | None | All of them, at small scale. |

This is also why hybrid products are hard to classify and easy to mis-design. A game that adds a persistent shared hub to match-based play has imported every hub problem (density, harassment, economy) into a game whose team may have no one who has dealt with them.

### The heritage test and its limits

Bartle offers a shortcut for unclear cases. If a design draws heavily on an existing virtual world, it almost certainly is one. If it doesn't, it almost certainly isn't. This works well for history, because it follows how designers actually learned from each other through MUDs, mailing lists and job changes. It works less well for design, because it hides the question you should be asking. A social platform with no MUD ancestry can still have every problem a MUD had. Use the property list when you design, and the heritage test when you write history.

### Where the definition is contested

Definitions draw borders, and borders decide who counts. Three honest objections:

- **The character rule** excludes worlds where players are towns, companies or fleets. Those games share, persist and simulate. Whether they are "worlds" is partly a matter of taste.
- **"Not the real world"** gets harder as worlds hold real money and real relationships. Bartle's own chapter on economies discusses players paying real money for virtual items. The border is porous and designers have to police it.
- **Sharding** makes "a world" plural. By Nevelsteen's reading, a 200-realm MMO is 200 worlds. By players' everyday reading, it is one game. When you write a design document, say which you mean.

You do not have to settle these debates. You do have to know which side your design lands on, because the problems follow the properties.

## In-class activity (25 minutes)

Work in groups of three.

1. **Classify (10 min).** For four products your group chooses (at least one you think is borderline), rate each of Bartle's six properties on a 0-2 scale: 0 absent, 1 partial, 2 fully present. Place each product on the persistence-versus-change grid.
2. **Compute (10 min).** For the product with the highest total, estimate `C`, `f`, `Z` and `v` for one band of the world. Rough numbers are fine; state your reasoning for each. Compute `λ` and `P(alone)`.
3. **Decide (5 min).** Choose a target band for `λ` in that part of the world and one change (pooling, splitting, or a world-design change) that would get you there.

Expected output: a filled table of scores, one `λ` calculation with stated assumptions, and a one-sentence recommendation. Two groups present.

## Common misconceptions

- **"Big subscriber numbers mean a busy world."** Subscribers spread across shards, time zones and bands. The number that decides whether you see someone is `λ`, and it can be tiny in a game with millions of players.
- **"More persistence is always better."** Persistence locks in solved puzzles, spent resources and old mistakes. Bartle's adventure worlds reset on purpose.
- **"Sharding is just a technical detail."** Each shard is a separate shared, persistent world with its own community and economy. Merging or pooling them changes the design, not only the servers.
- **"Doubling the players halves the loneliness."** `P(alone) = e^(−λ)`, so doubling `λ` squares `P(alone)`. From 80% alone you go to 64%, not 40%.

## Check yourself

1. Name the single property each of these lacks, under Bartle's conventions: a play-by-email game; a tabletop role-playing campaign; a chat room.
2. A world keeps characters and their inventories across a restart but respawns all monsters, doors and treasure. Where does it sit on Bartle's persistence ladder, and what design benefit does that give?
3. A zone band has `M = 400` view cells. Leveling players there number 120 on one realm. Using `e^(−λ)`, what is `P(alone)`? If you pool 3 realms, what is it now?
4. Explain, using the model, why a hotfix that stops pooling players across distant time zones may leave `λ` unchanged in the evening.
5. Your team's MMO has one megaserver, and every map opens a new copy when it passes 100 players. A designer says "we solved density." Name one thing this design still cannot guarantee and one thing it has given up.

<details>
<summary>Answers</summary>

1. Play-by-email lacks real time. The tabletop campaign lacks automated physics, since a human referee rules. The chat room lacks physics too, since there are no world rules to act through (it also lacks a character in the world).
2. Level 2, the DikuMUD rung. Content that designers built once (doors, puzzles, treasure) can be reused by every group, and one group's actions cannot permanently break it.
3. `λ = 120 / 400 = 0.3`, `P(alone) ≈ e^(−0.3) ≈ 74%`. With 3 realms, `λ = 0.9`, `P(alone) ≈ 41%`.
4. Players in a distant time zone are mostly offline when you play. Pooling them adds to `n` on paper, but the `n` that matters is players online now in your band, and that barely moves.
5. It cannot guarantee that players see the *same* people again, so continuity and reputation suffer. It has given up the guarantee that two friends on "the same server" are in the same copy of a map unless the grouping system puts them there.

</details>

## Lab / assignment hook

[Lab 01, world audit and density sheet](../labs/lab01.md). You audit one real online game against Bartle's properties, build a density spreadsheet for three bands of an invented world, and design a pooling and splitting policy that keeps `λ` inside targets you set and defend. The audit feeds the case-studies assignment (40%).

## Sources

- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF from the author (mud.co.uk/richard). Chapter 1: the opening definitions and five conventions with near-miss examples (pp. 3-5); naming history from MUD to MMORPG and the distinction from VR (pp. 3-4); the 500-player vast-world edge case (p. 5); the heritage test (p. 5); "The Basics" categories, the persistence ladder with AberMUD, DikuMUD, EverQuest, Ultima Online and MOO examples, and the rocket and bomb reset argument (pp. 51-78); Table 1.3, persistence versus change, the quadrant reading and the Verant and Skotos slogans (pp. 79-83). Paraphrased; one short quoted slogan.
- Bartle, R. (2015). *MMOs from the Inside Out*. Apress. The six-property definition including "not the real world," as quoted in Wikipedia, "Virtual world" (accessed September 2026).
- Nevelsteen, K. (2018). "Virtual World, Defined from a Technological Perspective, and Applied to Video Games, Mixed Reality and the Metaverse." *Computer Animation and Virtual Worlds* 29, e1752. arXiv:1511.08464. The "one persistent shard" requirement.
- Warcraft Wiki, "Cross-realm zones" and "Patch 5.0.4" (accessed September 2026). Cross-realm zones introduced in patch 5.0.4, released 28 August 2012, to address dead lower-level zones while players were at max level; the 20 September 2012 hotfix limiting pooling to within three time zones.
- Warcraft Wiki, "Layering" (accessed September 2026). Layering in World of Warcraft Classic from its 2019 launch to relieve outdoor overcrowding; the intent to merge layers before Phase 2, live 13 November 2019.
- Wikipedia, "Guild Wars 2" (accessed September 2026). Release on 28 August 2012; megaserver system in the April 2014 feature pack, creating map instances for players regardless of home world so the game feels more populated.
- Wikipedia, "Eve Online" (accessed September 2026), as cited in GS101 week 9. Record of 65,303 concurrent accounts on one server, May 2013.
- Wikipedia, "World of Warcraft" (accessed September 2026), as cited in GS101 week 9. Over 12 million subscribers in October 2010.
- Castronova, E. (2005). *Synthetic Worlds*. University of Chicago Press. Assigned reading only; no claims in this lecture depend on it.
- The density model, its parameters (`C = 2,000`, `v = 50`, the 80/20 split, zone counts) and the target band for `λ` are invented for teaching.

## Interactive spec: examples/w01-shared-density.html

**The one insight:** whether a world feels shared depends on `λ`, the expected number of other players in view, not on how many players the game has. The same realm can be crowded in one band and empty in another, and pooling or splitting realms moves `λ` without adding a single player.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (map on top).

- **Left view, "Your band of the world":** a grid of `M` view cells, drawn as `Z` zone blocks each holding `v` square cells (cap the drawing at 40 zones × 64 cells; above that, draw a representative sample of 2,000 cells and say so in small text). Place `round(n)` dots uniformly at random over the cells (cap drawn dots at 5,000 and scale with a note if above). Highlight one cell with a thicker outline as "you." Color cells that contain at least one dot slightly darker. A "reshuffle" button redraws the random placement. Under the grid, show the empirical share of empty cells from the current placement next to the model's `P(alone)` so students see them agree.
- **Right view, "Chance you are alone":** horizontal axis `λ` from 0 to 8, vertical axis `P(alone)` from 0 to 100%. Plot `e^(−λ)` as a curve. Shade the target band between two `λ` values the user sets (default 1 to 3). Mark the current `λ` with a dot and label it with `λ` (two decimals) and `P(alone)` (one decimal percent).
- **Readouts (copyable):** `n` (integer, rounded), `M`, `λ` (two decimals), `P(alone)` exact `(1 − 1/M)^n` (one decimal percent), `P(alone)` approximation `e^(−λ)` (one decimal percent), "sees someone" `1 − P(alone)`, and "realms to pool for P(alone) ≤ target" computed as `ceil(ln(1/target) × M / (f × C))` for a target the user sets (default 10%).

**Controls (keyboard accessible, labeled):**

1. Concurrency `C`: slider 50 to 5,000, step 50, default 2,000.
2. Share in band `f`: slider 0.05 to 1.00, step 0.05, default 0.20.
3. Zones in band `Z`: slider 1 to 40, step 1, default 35.
4. View cells per zone `v`: slider 10 to 100, step 5, default 50.
5. Pooling factor: a segmented control "Split into L copies / Single realm / Pool k realms" with a numeric stepper 1 to 20. Split sets `k = 1/L`; pool sets `k = k`.
6. Target band low and high for `λ`: two number inputs, defaults 1 and 3.
7. Target alone share for the "realms to pool" readout: number input 1% to 50%, default 10%.
8. Presets: "Endgame" (`f = 0.8`, `Z = 5`, `v = 50`, single realm), "Leveling" (`f = 0.2`, `Z = 35`, `v = 50`, single realm), "Launch day" (`f = 1.0`, `Z = 3`, `v = 50`, single realm). All presets keep the current `C`.
9. Reshuffle and Reset buttons.

**Formulas.**

```
k        = pool count, or 1/L when split
n        = k × f × C
M        = Z × v
λ        = n / M
P_exact  = (1 − 1/M)^n
P_approx = e^(−λ)
realms_needed(target) = ceil( ln(1/target) × M / (f × C) )
```

**Test values** (`C = 2,000`, `v = 50`):

| Preset / setting | `n` | `M` | `λ` | `P_exact` |
|---|---|---|---|---|
| Endgame (f 0.8, Z 5), single | 1,600 | 250 | 6.40 | 0.2% |
| Leveling (f 0.2, Z 35), single | 400 | 1,750 | 0.23 | 79.6% |
| Leveling, pool 2 | 800 | 1,750 | 0.46 | 63.3% |
| Leveling, pool 5 | 2,000 | 1,750 | 1.14 | 31.9% |
| Leveling, pool 10 | 4,000 | 1,750 | 2.29 | 10.2% |
| Leveling, pool 11 | 4,400 | 1,750 | 2.51 | 8.1% |
| Leveling, pool 20 | 8,000 | 1,750 | 4.57 | 1.0% |
| Launch (f 1.0, Z 3), single | 2,000 | 150 | 13.33 | 0.0% |
| Launch, split 2 | 1,000 | 150 | 6.67 | 0.1% |
| Launch, split 4 | 500 | 150 | 3.33 | 3.5% |
| Launch, split 8 | 250 | 150 | 1.67 | 18.8% |

Leveling preset with `C = 300`: `n = 60`, `λ = 0.03`, `P_exact = 96.6%`. Leveling preset, target 10%: realms needed = `ceil(2.3026 × 1,750 / 400) = ceil(10.07) = 11`.

**First screen:** Leveling preset, `C = 2,000`, single realm. The map is mostly pale empty cells with scattered dots; the dot on the curve sits high at about 80%, outside the shaded target band. Caption above both views: "2,000 players online, and a leveling player sees nobody 80% of the time."

**Content rules.** No game art, logos or maps from real games. Players are plain dots and zones are plain rectangles. Small text under the views: "Parameters are illustrative. Real players cluster, so real maps are lumpier than this one."
