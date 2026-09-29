# MMO301 · Week 08 — Player types (Bartle 1996) and the hero's journey

**Why this matters:** Bartle's four player types are the most quoted idea in online game design, and most people who quote them have not read the part that matters most. The 1996 paper is less about sorting people into boxes and more about how groups of players change each other's numbers. That part predicts which worlds collapse and which grow. It explains design moves that studios still make, such as splitting a world in two to fence off player killers.

**You will be able to:**
- Place a player on Bartle's interest graph from their behaviour, and explain the two axes without the card-suit shorthand.
- Translate Bartle's qualitative statements about player types into a population model and compute one week of it by hand.
- Predict what happens to a world's population when killers outnumber socialisers, and compute the killer count a socialiser community can tolerate.
- Critique the model and Bartle's later development tracks and hero's journey, naming what is observed, what is assumed and what is invented.

**Before class:** Bartle, "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs" (1996), the whole paper, free at mud.co.uk. Read the sections "Player interactions" and "Dynamics" twice. Bartle, *Designing Virtual Worlds* (2003, free Creative Commons edition), chapter 3, the sections on player types. Skim Bartle's talk notes "A Self of Sense" (Selfware, 2003) at mud.co.uk.

**Prerequisites from earlier courses:** [GD101 week 5, the 8 kinds of fun](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md) (which previewed Bartle's axes). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md), [week 3, positive feedback](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [week 4, negative feedback](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) (every term in this week's model is one of these). [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) (the world Bartle co-wrote). From this course, [week 6, EVE Online](w06-eve-online-the-single-shard-sandbox.md) (pricing aggression) and [week 7, themepark vs sandbox](w07-themepark-vs-sandbox.md) (players as content).

**Interactive:** [When killers outnumber socialisers](../examples/w08-bartle-populations.html). Keep it open during section 2.

---

## 1. Four things people enjoyed

### Where the types came from

Between November 1989 and May 1990, the most experienced players (wizards and witches, "wizzes") of a commercial MUD in the UK argued on its bulletin board about what people want from a MUD. Bartle was the senior administrator. About 15 people took a major part and about 15 more joined in from time to time. When the argument ran out of new points, Bartle summarized it, and the summary sorted what players found fun into four groups. He wrote it up in an article in 1990 and extended it into the paper you read for today in April 1996.

That origin matters. The four types are not the result of a survey or a statistical test. They are one experienced administrator's summary of a long discussion among advanced players of one game that allowed player killing. Bartle says so, and adds that most players leaned a little toward all four. Next week you will see what happened when someone tried to measure them.

### The four types

In the paper's terms, players enjoyed:

- **Achievement** within the game's own terms. Points, levels, treasure, kills of monsters. These are **achievers**.
- **Exploration** of the game. First its geography, then its physics and hidden mechanics. These are **explorers**.
- **Socializing** with other players, using the game as a context for conversation and relationships. These are **socialisers**.
- **Imposition upon others**, using the game's tools to cause other players distress (or, rarely, to help them). Where the game allows it, that means attacking other players' characters. These are **killers**.

Bartle gave each a card suit as a memory aid. Achievers are diamonds (treasure), explorers are spades (they dig), socialisers are hearts (empathy), killers are clubs (they hit people).

### The interest graph

The part worth remembering is not the suits but the two axes that generate them.

```
                     ACTING
         Killers        |        Achievers
                        |
  PLAYERS --------------+-------------- WORLD
                        |
      Socialisers       |        Explorers
                   INTERACTING
```

- The horizontal axis asks what the player is interested in, other **players** or the **world**.
- The vertical axis asks how they engage with it, **acting on** it (imposing their will) or **interacting with** it (being responsive to it).

Achievers act on the world. Explorers interact with the world. Socialisers interact with players. Killers act on players.

The graph is a plane, not four boxes. A player can sit anywhere on it, and Bartle expected players to drift across it with mood and over time. Use the axes when you design. "This feature lets players act on other players" is a more useful sentence than "this feature is for killers", because it tells you what the feature does, not who you are stereotyping.

"Killer" in Bartle's sense means imposing on other players, not fighting. A player who corners a market to ruin rivals is acting on players. A player who enjoys formal, consensual duels may be closer to an achiever. Keep the axis, not the label.

## 2. Worked example: when killers outnumber socialisers

### The hook

On 4 May 2000, Ultima Online released its *Renaissance* expansion. The headline feature was strange. It doubled the size of the world by copying the whole existing map. The copy, called Trammel, allowed player-versus-player combat only by consent. The original map, renamed Felucca and made visually grimmer, kept open player killing.

Why would a studio build an entire mirror world just to separate one kind of player from everyone else? Bartle's 1996 paper answers that question four years early. It argues that killers affect other players' numbers more than any other type does, that socialisers are the most sensitive to them, and that a world left alone drifts to one of a few stable mixes. You will now turn his statements into a model and watch it happen.

### From Bartle's statements to a model

The paper's "Player interactions" section describes, pair by pair, how a change in one type's numbers changes another's. For example, it says that more killers reduce achievers, that more killers reduce socialisers by a much greater degree, that more socialisers attract more socialisers, and that more achievers and more socialisers feed a slow growth in killers. It then draws these as an influence diagram with plus and minus signs.

An influence diagram with signs is a set of flows. You met that idea in GD102 weeks 2 to 4. Each type is a **stock** (a number of players), and each arrow in Bartle's diagram becomes a term in that stock's weekly flow. Here is the model. Populations are in **hundreds of players**, and one step is one week.

```
N    = A + E + S + K                    total population
room = max(0, 1 − N / 40)               share of server capacity still free (capacity 4,000 players)
w    = N / (N + 10)                     word of mouth: arrivals scale with who is already there
g    = w × room                         the arrival gate
q    = 1 − protection                   share of killer attacks the rules allow (protection from 0 to 1)

A_next = A + 1.00·g        − A·(0.03 + 0.08·q·K)
E_next = E + 0.15·c·g      − E·(0.03 + 0.01·q·K)
S_next = S + 0.15·g        + S·(0.04·S·room − 0.04 − 0.20·q·K)
K_next = K + 0.10·g        + K·(0.04·q·(A + S) − 0.08 − 0.05·E)
```

Any value that would go below zero is set to zero.

- `A`, `E`, `S`, `K` are achievers, explorers, socialisers and killers.
- `protection` is a design lever. 0 means open player killing everywhere. 1 means no non-consensual attacks at all (Trammel). Values between mean attacks are possible but restricted, for example to some zones.
- `c` is a second lever, the rate of new areas and mysteries for explorers. 1 is normal, 3 means three times as many explorers arriving.
- The first number in each line is arrivals. The bracket is the per-player rate of change.

Each term traces to a sentence in the paper.

| Bartle's statement (paraphrased) | Term in the model |
|---|---|
| Achievers do not need other types to join, and the game cannot have too many of them | Largest arrival rate (1.00), no other-type bonus |
| More killers mean fewer achievers | `−0.08·q·K` in the achiever bracket |
| Killers affect explorers only mildly | `−0.01·q·K`, one eighth of the achiever effect |
| Explorer numbers are hard to raise except by giving them more to find | Lever `c` on explorer arrivals |
| More socialisers attract more socialisers | `+0.04·S·room`, a per-player rate that grows with `S` |
| More killers cut socialisers much more than achievers | `−0.20·q·K`, 2.5 times the achiever effect |
| More achievers and socialisers mean more killers, slowly ("Malthusian", in Bartle's word) | `+0.04·q·(A + S)` in the killer bracket |
| More explorers slightly reduce killers | `−0.05·E` in the killer bracket |

Be honest about what this is. Bartle gave signs and relative sizes, never equations or numbers. Every coefficient above is ours, chosen to keep his signs and his relative sizes. We also left out his weaker effects, for example that explorers help achievers by sharing puzzle solutions, and that too few killers make achievement feel cheap. The model is a way to see what his statements imply when they act at the same time. It is not a measurement of any real game.

### Numbers you can check

Start a world of 1,000 players where killers outnumber socialisers: 400 achievers, 100 explorers, 200 socialisers and 300 killers. In hundreds, `A = 4, E = 1, S = 2, K = 3`. Open player killing, so `protection = 0` and `q = 1`. Normal explorer content, `c = 1`.

Work one week by hand.

```
N    = 4 + 1 + 2 + 3 = 10
room = 1 − 10/40 = 0.75
w    = 10 / 20 = 0.5
g    = 0.5 × 0.75 = 0.375

A_next = 4 + 0.375 − 4·(0.03 + 0.08·3)             = 4 + 0.375 − 1.08  = 3.295
E_next = 1 + 0.05625 − 1·(0.03 + 0.03)             = 1 + 0.05625 − 0.06 = 0.996
S_next = 2 + 0.05625 + 2·(0.04·2·0.75 − 0.04 − 0.60) = 2 + 0.05625 − 1.16 = 0.896
K_next = 3 + 0.0375 + 3·(0.04·6 − 0.08 − 0.05·1)   = 3 + 0.0375 + 0.33 = 3.368
```

In players, after one week: 330 achievers, 100 explorers, 90 socialisers, 337 killers. The socialisers lost more than half their number in seven days. The killers grew, because they are feeding on a crowd of targets.

Now let the model run. The table rounds to whole players.

| Week | Achievers | Explorers | Socialisers | Killers | Total |
|---|---|---|---|---|---|
| 0 | 400 | 100 | 200 | 300 | 1,000 |
| 1 | 330 | 100 | 90 | 337 | 856 |
| 4 | 184 | 96 | 9 | 344 | 633 |
| 13 | 127 | 88 | 8 | 204 | 427 |
| 26 | 173 | 87 | 13 | 114 | 387 |
| 52 | 248 | 96 | 18 | 100 | 462 |
| 156 | 247 | 104 | 17 | 106 | 475 |

Within a month the socialisers are nearly gone. With them gone and achievers thinned out, the killers run short of victims and fall from 344 to about 100, and achievers recover. By the end of the first year the world has settled at about 475 players, less than half its starting size, in a standing balance between achievers and killers. The killers never "won". They ended with about a third of their starting number.

That end state is Bartle's first stable configuration, killers and achievers in equilibrium. More achievers feed more killers, more killers cut achievers, and the two settle against each other.

### The socialiser survival line

Why do socialisers fall so fast? Look at their bracket alone. Socialisers grow, before arrivals, only when

```
0.04·S·room − 0.04 − 0.20·q·K > 0
q·K < 0.2·S·room − 0.2
```

At `room = 0.75` and converted to players, a socialiser community of size `S` survives on its own only if the number of killers able to attack it is below `0.15·S − 20`.

| Socialisers | Killers tolerated, open PvP (`q = 1`) | With 90% protection (`q = 0.1`) |
|---|---|---|
| 200 | 10 | 100 |
| 400 | 40 | 400 |
| 1,000 | 130 | 1,300 |
| 2,000 | 280 | 2,800 |

The line has two features Bartle described in words. First, the threshold grows with the socialiser count. That is the positive feedback in his paper. A big social community can absorb more hostility than a small one, and a small one dies from a handful of killers. Second, below about 133 socialisers (where `0.15·S − 20 = 0`), the community shrinks even with no killers at all. That is his critical mass. So "killers outnumber socialisers" is not a close call in this model. Under open killing, 200 socialisers can tolerate about 10 killers. They were facing 300.

The swap does not save them. Start with 300 socialisers and 200 killers and the world reaches the same 475-player balance by week 156. A social-heavy world with only 20 killers (400, 100, 600, 20) is worse in a sense. The socialisers boom to 822 in four weeks, the killers feed on them and grow from 20 to 346 by week 13, and the socialisers crash to 7. It is the boom-and-bust Bartle warned about when he called socialisers the most volatile group.

### Pulling the levers

Now try Bartle's other configurations by changing the design, not the starting mix. All rows start from (400, 100, 200, 300) and report week 520 (ten years).

| Design | Achievers | Explorers | Socialisers | Killers | Total | Bartle's configuration |
|---|---|---|---|---|---|---|
| Open killing, `c = 1` | 247 | 105 | 17 | 106 | 475 | 1, killers and achievers in balance |
| Full protection, `c = 1` | 69 | 10 | 3,813 | 2 | 3,895 | 2, socialiser-dominated |
| 90% protection, `c = 1` | 161 | 54 | 2,462 | 642 | 3,319 | 2, with killers living among socialisers |
| 50% protection, `c = 1` | 545 | 157 | 47 | 90 | 839 | 1, softened |
| 50% protection, `c = 3` | 797 | 501 | 287 | 30 | 1,615 (cycling, 1,050 to 2,800) | 3, all groups have influence |
| Open killing, `c = 4` | 685 | 682 | 66 | 31 | 1,465 | Explorers holding killers down |
| All arrivals switched off | 0 | 0 | 0 | 0 | 0 | 4, a world with no players |

Three things to notice.

**Protection alone makes a social world, and it is almost only social.** With full protection the socialisers' positive feedback fills the server, and achievers and explorers are squeezed out by crowding, not by killers. Bartle describes the other types in this configuration as swamped. With 90% protection, killers come back and settle at 642, because a huge socialiser crowd is a lot of prey even when most attacks are blocked.

**The balanced world needs two levers, and it is slow.** Only partial protection plus a steady supply of new things for explorers gives all four groups real numbers. Bartle calls this third configuration the most balanced and the hardest to reach. In the model it never settles. About every 100 weeks the socialisers surge (1,475 at week 260), the killers follow (245), and the socialisers crash back. Its week-520 row is one moment of that cycle. Every other row is steady. Watch the cycle in the interactive.

**Explorers are the only lever on killers that costs nobody else.** In the open-killing row with `c = 4`, killers fall to 31 without any protection rule, and every other group grows. That is Bartle's point about explorers. The catch, which he also notes, is that few people are explorers by nature. In the model you had to quadruple their arrivals.

### A visual you can move

Open the interactive. The top panel shows the four populations over time. The bottom-left panel is the interest graph with a disc per type, sized by population. The bottom-right panel is the socialiser-killer plane with the survival line and the world's weekly path.

Start from the default mix with open killing and press play. Watch the path in the bottom-right panel. It starts far above the survival line, drops straight down the socialiser axis, and curls into the killer-achiever balance. Now drag protection to 90% and replay. The survival line swings up, the world starts below it, and the socialiser count takes off. The same starting population, a different rule, a different world.

### Cross-game recognition

**Ultima Online, Renaissance (May 2000).** Trammel sets protection to 1 on one copy of the map and leaves Felucca at 0. In model terms, the studio stopped choosing a single configuration for its world and ran two worlds, one heading for configuration 2 and one for configuration 1, with players choosing where to live. Ultima Online history is covered in [GS101 week 9](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) and in week 3 of this course.

**World of Warcraft, War Mode (patch 8.0.1, 17 July 2018).** Before this patch, WoW split open-world combat by server type. PvP realms made players always attackable by the other faction, and normal realms let players opt in. War Mode replaced that with a toggle on every realm. Players who turn it on are placed on shards with other War Mode players, and they receive a 10% bonus to experience and to gold and currency from world quests. Read it with the model. The shards separate the pool with `q` near 1 from the pool with `q = 0`. The bonus raises arrivals of achievers into the killer pool, because killers need prey and achievers will accept risk for reward. Bartle's paper already notes that achievers accept killers as the price of their achievements meaning something.

**EVE Online (week 6).** EVE's security levels set protection per region, from high-security space where the police punish attackers to lawless space where nobody does. That is a map of `q` values rather than one number or two copies. [Week 6](w06-eve-online-the-single-shard-sandbox.md) prices aggression in detail.

**Outside games, predator and prey.** The killer line in the model, growth proportional to prey and loss when prey is scarce, has the shape of the Lotka-Volterra equations that ecologists use for predators and prey. The cycles you saw in the balanced world (socialisers surge, killers follow, socialisers fall) are the same cycles those equations produce for lynx and hares. Bartle's "Malthusian" was the right word.

### Eyes-open design judgment

- **Decide which configuration you want before launch.** Bartle's point, which the model makes concrete, is that a world left to itself goes to configuration 1 or 2 depending on your killing rules. If you want a mixed world, you need rules and content aimed at it from the start.
- **Protection is a strong lever with a side effect.** It saves socialisers and it removes the threat that makes achievement feel earned. Bartle notes that achievers in a killer-free world can feel any fool can win. The model does not include that effect, so it flatters protection.
- **Splitting the world is honest but costly.** Trammel and War Mode let players choose, and they split `N`, which week 7 showed costs a sandbox novelty.
- **Explorers are cheap to keep and expensive to recruit.** Content that rewards curiosity is the one lever that lowers aggression without hurting anyone. It works only if you can keep producing it.

### Check yourself (worked example)

1. Compute one week from `A = 4, E = 1, S = 2, K = 3` with `protection = 0.5`. Which group changes the most?
2. Using the survival line with `room = 0.75`, how many killers can 600 socialisers tolerate under open killing? Under 75% protection?
3. In the "open killing, `c = 4`" row, killers end at 31. Which single term in the killer equation is responsible? Compute its size at `E = 6.82`.

<details>
<summary>Answers</summary>

1. `q = 0.5`, `g = 0.375` as before. `A_next = 4 + 0.375 − 4·(0.03 + 0.12) = 3.775`. `E_next = 1 + 0.05625 − 1·(0.03 + 0.015) = 1.011`. `S_next = 2 + 0.05625 + 2·(0.06 − 0.04 − 0.30) = 1.496`. `K_next = 3 + 0.0375 + 3·(0.04·0.5·6 − 0.08 − 0.05) = 3.0075`. Socialisers still change the most (a 25% fall), but far less than the 55% fall under open killing.
2. `0.15 × 600 − 20 = 70` killers under open killing. With `q = 0.25`, `70 / 0.25 = 280` killers.
3. The explorer term `−0.05·E`. At `E = 6.82` it is `−0.341` per killer per week, larger than the base loss of 0.08 and enough to cancel a prey gain of `0.04 × (6.85 + 0.66) ≈ 0.30`.

</details>

## 3. Where the model, and the paper, break

Bartle himself warns that his dynamics are rough. They ignore outside forces, and he suggests that role-playing rules, a shared purpose (an educational MUD) or a strong community could hold together a mix his model calls unstable. Two further problems are worth naming.

**The types were never measured.** The 1996 paper derives the types and their interactions from discussion and administrative experience. Nobody counted achievers in 1990. So the dynamics describe how a thoughtful administrator believed populations moved, not measured movements. Next week, Nick Yee's surveys test whether the four types exist as separate groups at all. Some of them do not.

**Players are not one type.** The model never moves a player from one type to another. Bartle's own paper says players drift, and his later work says they drift in patterns (section 4). A model with transitions between types, for example 1% of achievers becoming socialisers each week, behaves differently. Lab 08 asks you to add one.

## 4. The eight types and the hero's journey

### A third axis

In *Designing Virtual Worlds* (2003) and in a talk the same year, Bartle added a third axis to the interest graph, **implicit versus explicit**. Implicit means acting without forethought, by instinct. Explicit means acting with a plan. Splitting each of the four types by that axis gives eight.

| Original type | Implicit | Explicit |
|---|---|---|
| Achiever | Opportunist, takes chances as they appear | Planner, sets a goal and works toward it |
| Explorer | Hacker, understands the world intuitively | Scientist, experiments methodically |
| Socialiser | Friend, enjoys the company of people they know | Networker, seeks out and assesses new contacts |
| Killer | Griefer, acts on others with no aim beyond the reaction | Politician, acts on others to build influence and reputation |

The split explains one thing the four-type model could not. A politician (a guild leader, a market organizer, a "den mother" in Bartle's phrase) acts on other players as much as a griefer does, but with a completely different effect on the world.

### Development tracks

The bigger payoff, Bartle argued, is that players move through the eight types in common sequences as they gain experience. He called these **development tracks** and reported four from observation.

- **Main sequence:** griefer, then scientist, then planner, then friend. In the four-type terms, a new player tries to kill others, then explores, then tries to "win", then settles into the community.
- **Socialiser sequence:** griefer, then networker, then politician, then friend.
- **Explorer sequence:** opportunist, then scientist, then planner, then hacker.
- **Minor sequence:** opportunist, then networker, then planner, then friend.

Each track runs implicit, explicit, explicit, implicit. Bartle's reading is that it is a learning pattern. You find out what you can do by trial, work out which combinations matter, practise them deliberately, and finally do them without thinking. He adds that designers influence how fast a player moves along a track.

### The hero's journey

Joseph Campbell's *The Hero with a Thousand Faces* (1949) proposed that many myths share one structure, the **monomyth**, usually told in three parts (departure, initiation, return) and 17 stages. A hero leaves the ordinary world, faces trials in a strange one, gains something, and comes back changed.

Bartle's claim is that a virtual world runs this journey on the player, not on their character. You, the real person, are the hero. The virtual world is the strange land. His mapping, paraphrased:

| Campbell's stage | In a virtual world | Development track |
|---|---|---|
| Call to adventure | An ad, a friend who plays | |
| Crossing the first threshold | Installing the client and logging in | |
| Belly of the whale | Character creation, a formal rebirth | |
| Road of trials | Small tests of what you can do | Opportunist or griefer |
| Meeting with the goddess | Seeking knowledge, by experiment or from others | Scientist or networker |
| Atonement with the father | Trying to "win" by the game's measures; Bartle names the father as the lead designer | Planner or politician |
| Apotheosis | The game's challenges stop mattering | Friend or hacker |
| Master of the two worlds | Your real and virtual selves line up | |

Two stages matter for design. At **the ultimate boon**, the hero is supposed to gain something and go home. Bartle points out that most studios do not want players to leave, so they offer no boon and add content to keep the player instead. He asks whether that is ethical. At **master of the two worlds**, the player no longer needs the world to be who they are. For Bartle, that is the finished journey and the right time to stop playing.

Bartle ties the journey to immersion. As a player moves along a track, their sense of being in the world deepens, from player to avatar to character to persona. [Week 10](w10-immersion-identity-and-the-avatar.md) covers that ladder, so it is not repeated here.

### Reading this critically

Treat the tracks and the journey as a design lens, not as findings.

- The tracks come from Bartle's observation of players over years. He says there may be others he missed. They have not been tested the way Yee tested motivations (next week).
- Campbell's monomyth is influential in screenwriting and widely criticized by folklorists, who argue that it was built from examples chosen to fit. A lens that fits every story is hard to test.
- The lens is still useful for the questions it raises. Does your character creation feel like a threshold? What does your world offer a player at apotheosis other than more of the same? Is there a boon at all?

## In-class activity (25 minutes)

Pairs. Materials: the interactive, a printed copy of the model equations, and a calculator.

1. **Predict first (5 min).** Your world starts at (400 achievers, 300 explorers, 100 socialisers, 200 killers). Before running anything, write down which of Bartle's configurations it reaches under open killing and under 90% protection, and why, citing one sentence from the paper for each.
2. **Hand-step (8 min).** Compute week 1 by hand under open killing. One partner computes `A` and `E`, the other `S` and `K`. Swap and check.
3. **Run and compare (7 min).** Run both settings in the interactive for 520 weeks. Record the final populations.
4. **Design move (5 min).** Your producer wants at least 500 socialisers and at least 100 killers at week 520. Find a protection and `c` setting that does it, or argue that none exists in this model.

Expected output: two written predictions with citations, the hand-computed week 1 (check: `S_next` is about 0.65 hundred, 65 players), the two recorded runs, and one setting or a short argument.

## Common misconceptions

- **"Bartle's types are a personality test."** They were a summary of what players of one MUD said they enjoyed. The "Bartle Test" that many people take online was written later by other people, and it forces choices between types. Next week covers why that matters.
- **"Killers are bad for the game, so remove them."** In the paper and in the model, killers keep achievement meaningful and are part of configuration 3. Removing them leads to configuration 2, which is a fine world but a different one.
- **"A balanced world has equal numbers of each type."** Bartle says balanced means similar influence, not similar numbers. In the model's balanced row, killers are about 2% of the population and still hold socialisers in check.
- **"The model predicts real populations."** Its shapes follow Bartle's statements. Its coefficients are invented for teaching. It can tell you direction and rough speed, not headcounts.

## Check yourself

1. Place each on the interest graph and name the eight-type label: (a) a player who writes the definitive spreadsheet of drop rates by testing each monster 500 times; (b) a player who organizes a server-wide event to raise their guild's standing; (c) a player who repeatedly kills new characters at the starting town to watch them react.
2. In the model, what single change turns Bartle's "increasing socialisers increases killers" off? What would you lose by making that change in a real game?
3. A world has 1,500 socialisers and 150 killers, open killing, and `room = 0.75`. Is the socialiser community growing on its own? What protection level is the minimum for it to grow if killers double to 300?
4. Explain, using the model's killer equation, why War Mode's 10% bonus might be necessary for the War Mode shards to have any killers at all.

<details>
<summary>Answers</summary>

1. (a) Interacting with the world, explicit: scientist (explorer). (b) Acting on players, explicit: politician (killer quadrant). (c) Acting on players, implicit: griefer.
2. Set the killer prey term to use only achievers, `0.04·q·A`, or set protection to 1 so `q = 0`. In a real game this means killers cannot target socialisers, for example through safe social spaces. You lose some of the conflict socialisers talk about, and killers turn to achievers instead.
3. Threshold `0.15 × 1,500 − 20 = 205` killers. 150 is below it, so yes, it grows. With 300 killers you need `q × 300 < 205`, so `q < 0.683`, protection above about 32%.
4. Killers grow only if `0.04·q·(A + S)` exceeds their losses `0.08 + 0.05·E`. If players who dislike risk stay out of War Mode, `A + S` in the War Mode pool is small and killers there decline. The bonus pays achievers to join, which raises `A` in that pool above the level where killers can persist.

</details>

## Lab / assignment hook

[Lab 08, the Bartle population model](../labs/lab08.md). You build this week's model in a spreadsheet, reproduce the test values, add one transition along a development track, and write a critique of one claim in the 1996 paper using your runs. The critique is a first draft for the player-type critique assignment (20% of the course grade).

## Sources

- Bartle, R. A. (1996). "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs." April 1996 extension of his 1990 article "Who Plays MUAs". Free at mud.co.uk/richard/hcds.htm. Origin in the November 1989 to May 1990 wizzes' discussion (about 15 major and 15 minor contributors); the four types, suits and interest graph axes; the pair-by-pair interaction statements; the dynamics summary and influence diagram; the four stable configurations; the word "Malthusian"; the note that the dynamics model is imprecise.
- Bartle, R. A. (2003). "A Self of Sense." Talk notes, Selfware conference, 20 June 2003. mud.co.uk/richard/selfware.htm. The implicit/explicit axis and eight types; the four development tracks; the mapping of Campbell's stages onto a player's time in a virtual world, including the lead designer as "father", the missing boon and the "magic flight" by the live team.
- Bartle, R. A. (2003). *Designing Virtual Worlds*. New Riders. Free Creative Commons edition from the author. Chapter 3, player types and the eight-type model.
- Wikipedia, "Bartle taxonomy of player types" (accessed September 2026). Names and one-line descriptions of the eight types; the Bartle Test written in 1999 to 2000 by Erwin Andreasen and Brandon Downey.
- Wikipedia, "Ultima Online" and "Ultima Online expansions" (accessed September 2026). *Renaissance* released 4 May 2000 in North America; Trammel as a mirror of the map with consensual PvP only; Felucca keeping open player killing. Date confirmed by UOGuide (September 2026).
- Warcraft Wiki, "War Mode" and "Patch 8.0.1" (accessed September 2026). War Mode added in patch 8.0.1, released 17 July 2018; replaced PvP and PvE realm types; separate shards for War Mode players; 10% bonus to experience and to gold and currency from world quests.
- Wikipedia, "Hero's journey" (accessed September 2026). Campbell (1949), 17 stages in departure, initiation and return; criticism by folklorists of source-selection bias.
- The population model, all its coefficients and all populations in this lecture are teaching constructions derived from Bartle's qualitative statements. They are not data from any game.

## Interactive spec: examples/w08-bartle-populations.html

**The one insight.** When killers outnumber socialisers under open killing, socialisers collapse within weeks, killers then lose their prey and fall too, and the world settles at less than half its starting size. The same starting population under a protection rule becomes a social world. The student must see that the rule, not the starting mix, decides the ending, and see the socialiser survival line that explains why.

**Layout.** Controls on top. Below, three panels: a time-series panel full width, then two square panels side by side (stacked on mobile), the interest graph and the socialiser-killer plane.

**Controls.**
- Four number inputs for the starting mix in players, `A0, E0, S0, K0`, each 0 to 2,000, step 10. Defaults 400, 100, 200, 300.
- Preset buttons: "Killers outnumber socialisers" (400, 100, 200, 300), "Socialisers outnumber killers" (400, 100, 300, 200), "Social boom" (400, 100, 600, 20), "Your world" (400, 300, 100, 200).
- Slider `protection` 0 to 1, step 0.05, default 0. Label the ends "open killing" and "no non-consensual attacks".
- Slider `c` (explorer content) 1 to 5, step 0.5, default 1.
- Checkbox "Arrivals on" (default on). Off sets all four arrival coefficients to 0.
- Slider `weeks` 52 to 1,040, step 52, default 156.
- Buttons Play (animates week by week at 30 weeks per second), Reset, and Step (+1 week). Under `prefers-reduced-motion`, Play draws the final state at once.
- All controls keyboard operable.

**Model (per week, internal units are hundreds of players; display players).**
```
N = A+E+S+K; room = max(0, 1 − N/40); w = N/(N+10); g = w·room; q = 1 − protection
A' = A + 1.00·g − A·(0.03 + 0.08·q·K)
E' = E + 0.15·c·g − E·(0.03 + 0.01·q·K)
S' = S + 0.15·g + S·(0.04·S·room − 0.04 − 0.20·q·K)
K' = K + 0.10·g + K·(0.04·q·(A+S) − 0.08 − 0.05·E)
```
Update all four from the old values at the same time, then clamp each at 0. If `N = 0`, then `w = 0`.

**Time-series panel.** x axis weeks, y axis players. Four lines, one per type, with the total as a thin dashed line. Readout of all four values and the total at the current week.

**Interest graph panel.** The Bartle axes (players to world horizontally, interacting to acting vertically) with a disc in each quadrant corner. Disc area proportional to that type's population, scaled so 4,000 players fills a quarter of the panel. Label each disc with its type and count.

**Socialiser-killer plane.** x axis socialisers 0 to 4,000, y axis killers 0 to 1,000. Draw the survival line `K = (0.15·S − 20) / q` using the current `q` and `room = 0.75`, shade the region below it "socialisers grow" and above it "socialisers shrink". If `q = 0`, shade everything "socialisers grow" and hide the line. Draw the world's path week by week as a polyline with a dot at the current week. Caption: "The line uses room = 0.75, its value at 1,000 players."

**Test values (players, rounded; tolerance ±1 player).**

| Start (A, E, S, K) | protection | c | arrivals | Week | A | E | S | K |
|---|---|---|---|---|---|---|---|---|
| 400, 100, 200, 300 | 0 | 1 | on | 1 | 330 | 100 | 90 | 337 |
| 400, 100, 200, 300 | 0 | 1 | on | 4 | 184 | 96 | 9 | 344 |
| 400, 100, 200, 300 | 0 | 1 | on | 156 | 247 | 104 | 17 | 106 |
| 400, 100, 300, 200 | 0 | 1 | on | 156 | 247 | 105 | 17 | 106 |
| 400, 100, 600, 20 | 0 | 1 | on | 4 | 449 | 109 | 822 | 85 |
| 400, 100, 600, 20 | 0 | 1 | on | 13 | 143 | 103 | 7 | 346 |
| 400, 100, 200, 300 | 1 | 1 | on | 520 | 69 | 10 | 3,813 | 2 |
| 400, 100, 200, 300 | 0.9 | 1 | on | 520 | 161 | 54 | 2,462 | 642 |
| 400, 100, 200, 300 | 0.5 | 1 | on | 520 | 545 | 157 | 47 | 90 |
| 400, 100, 200, 300 | 0.5 | 3 | on | 260 | 464 | 425 | 1,475 | 245 |
| 400, 100, 200, 300 | 0.5 | 3 | on | 520 | 797 | 501 | 287 | 30 |
| 400, 100, 200, 300 | 0 | 4 | on | 520 | 685 | 682 | 66 | 31 |
| 400, 100, 200, 300 | 0.5 | 1 | on | 1 | 378 | 101 | 150 | 301 |

**Hand-check panel (collapsible).** Shows the full arithmetic of the next week from the current state, term by term, in hundreds, exactly as in the lecture's "Numbers you can check" block.

**Style.** Shared palette from `templates/interactive-tokens.css`. One color per type, used identically in all three panels, plus shape or label so the figure reads in grayscale. No card-suit glyphs as the only identifier. No game art or logos. Game names appear only in captions ("Ultima Online's Trammel is protection = 1").
