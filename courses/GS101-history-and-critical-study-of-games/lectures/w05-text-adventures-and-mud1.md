# GS101 · Week 05 — Text Adventures and MUD1 (1978): The First Virtual World

**Why this matters:** Every MMO you have played descends from a text game written on a university mainframe in 1978. MUD1 took a single-player treasure hunt and let many people play it in the same world at once, and that one change produced camping, player killing, resets and the first online community of players. If you understand what sharing did to MUD1, you can predict what it will do to any system you put into a shared world.

**You will be able to:**
- Place Colossal Cave Adventure, Zork and MUD1 on a timeline and explain what each added (a playable cave, a richer parser and a portable engine, a shared world).
- Apply Bartle's six properties of a virtual world to decide whether a given game is one.
- Compute a player's point income in a shared world with a limited treasure pool, find the population at which other players turn from company into competition, and predict the behaviors that follow.
- Critique instancing and per-player resources as fixes for contention, naming what each one costs a world.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 1, the history section from "The First Age: 1978-1985" to the end of "The Fourth Age: 1995-1997" (pp. 5-24 in the author's free PDF edition at mud.co.uk/richard/DesigningVirtualWorlds.pdf). Play 20 minutes of Open Adventure (the open-source port of Colossal Cave Adventure) or of MUD1 itself at british-legends.com, and write down three commands the game did not understand.

**Prerequisites from earlier courses:** None. GS101 has no prerequisites. This week follows [GS101 week 4, home consoles and the 1983 crash](w04-home-consoles-and-the-1983-crash.md). Everything in this lecture happened on university computers, in parallel with the arcade and console story of [GS101 week 3](w03-arcade-era-and-the-coin-op-business-model.md) and week 4, not after it. If you are also taking GD101, the "resources" and "conflict" formal elements from [GD101 week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) are the lens this week uses.

**Interactive:** [Shared treasure](../examples/w05-shared-treasure.html). Use it during section 3.

---

## 1. A cave made of sentences

### Colossal Cave Adventure

In 1975 and 1976, a programmer named Will Crowther wrote a game for the PDP-10, a mainframe computer common at universities and research labs. Crowther and his former wife Patricia were both programmers and serious cavers who had mapped large parts of Mammoth Cave in Kentucky. His game was a cave you explored by typing. He wrote it partly so his two daughters could play something that needed no technical knowledge.

The game printed a description of where you were. You typed a short command, such as `go north` or `get lamp`, and it printed what happened. That was the whole interface.

In 1977, a Stanford student named Don Woods found the game and wanted to expand it. He tracked Crowther down by sending email to "crowther" at every site then on the ARPANET, the research network that grew into the internet. With permission, Woods added high-fantasy elements, such as a dragon, and a scoring system. His version had about 140 locations, a vocabulary of 293 words and 53 objects. The original had five treasures. Woods added ten more. A perfect game scored 350 points.

Colossal Cave Adventure spread across the ARPANET the way files did then, copied from machine to machine. It inspired Zork, MUD1 and the early computer role-playing games of next week. In 2019 it entered the World Video Game Hall of Fame.

### The parser, and what it made players do

A parser is the part of a program that reads what you type and turns it into an action the game understands. Adventure's parser read one- or two-word commands, a verb and maybe a noun. `Take lamp` worked. `Take the brass lamp and light it` did not.

That limit shaped the game more than any single puzzle. With 293 words, the game understood only a tiny fraction of what a player might type. Players learned to think in the game's vocabulary rather than in English. When a puzzle had one correct verb and the player tried five synonyms first, the puzzle became a hunt for the word, not for the idea. Later players called this "guess the verb," and it is still the classic complaint about parser games.

This is your first example of a theme that runs through the whole course. The technology's limits (a two-word parser, a few kilobytes of memory) are not background. They are design constraints that decide what play feels like.

### Zork, and the idea of a portable engine

In May 1977, four people at MIT's Laboratory for Computer Science, Tim Anderson, Marc Blank, Bruce Daniels and Dave Lebling, started a game they meant to be a better Adventure. Their headline improvement was the parser. Zork accepted full sentences with several objects, so a player could type something much closer to English.

In 1979 they and several colleagues founded Infocom to sell it. The mainframe game was too big for the home computers of the time, so they split it into parts. Zork I came out in December 1980.

Infocom's quieter invention mattered as much as the parser. Blank and Joel Berez designed the Z-machine, a virtual machine. A virtual machine is a program that pretends to be a simple computer. Infocom wrote its games once, for the Z-machine, and then only had to write a small Z-machine interpreter for each home computer. One game could ship on many incompatible machines. Remember this when [week 7](w07-the-pc-era-strategy-simulation-modding.md) reaches the PC era and its dozens of incompatible platforms.

Zork I sold 38,000 copies by the end of 1982 and about 150,000 by 1984. The trilogy sold more than 680,000 copies through 1986. In 2007 Zork was named to a list of the ten most important video games, prepared for the Library of Congress.

Notice what Adventure and Zork share. You explore alone. The world waits for you. The treasure is always there when you arrive, and when you finish, the next player finds the same untouched cave. The world resets for every player. That last property is exactly what MUD1 removed.

## 2. MUD1: many players, one cave

### Essex, 1978

In autumn 1978, Roy Trubshaw, an undergraduate at the University of Essex in England, began writing a multi-user adventure game. It ran on the university's DEC-10, a PDP-10 family machine, in assembly language (MACRO-10). Trubshaw had loved playing Dungeon, the version of Zork that circulated on mainframes, and he named his game MUD, for Multi-User Dungeon, in its honor. You will sometimes see MUD1 dated to 1977. Bartle's own first-hand history gives autumn 1978 for the start of Trubshaw's code, and this course uses his date.

His first version was little more than a set of connected rooms where people could chat. Starting in late 1979 he rewrote it in a language called BCPL, working until about Easter 1980. When Trubshaw left Essex, Richard Bartle, a fellow student, took over. Bartle has said the code was only about a quarter finished at that point. He added most of the game world and the whole system for becoming a wizard.

Memory was tight. Bartle recalls the machine allowing something like 50K words of memory for the program. In spring 1980 the first external players logged in over a network link from Essex to the ARPANET, which is why MUD1 is often called the first internet multiplayer role-playing game. In 1983 Essex opened the DEC-10 to outside users over BT's packet network, but only between 2am and 8am, when the university was not using it.

MUD1 had a long commercial life as British Legends on the CompuServe network, which ran it until late 1999. In 2000 Viktor Toth rewrote the surviving BCPL source in C++ and put it back online, and in 2020 the source code was published. You can still play it.

### How MUD1 is played

The rules below come from the player guides for British Legends, the later commercial version, which is the version playable today. Treat them as describing the mature game, not necessarily every detail of 1978.

- **The goal.** Become a wizard or witch ("make wiz"), which grants immortality and powers over ordinary players. You need 102,400 points to make wiz.
- **Points from treasure.** Find treasure in the world and drop it in the swamp. Players call this "swamping." Each item is worth a set number of points.
- **Points from killing.** Fighting non-player monsters, called mobiles, earns points. Killing other players is encouraged and earns large rewards.
- **Death.** If your stamina drops to zero in a fight, your character dies permanently and you start again from zero. The guides joke that you haven't lived until you've died in MUD.
- **Resets.** The world holds a limited amount of treasure. When most of it has been swamped, the game resets, usually with a wizard's help. Everyone is told to quit and re-enter a fresh world, with the treasure restored.

The beginner's guide says the gravedigger's cottage near the start has useful tools, "provided you beat the other players to them." That phrase is the whole of this week's worked example.

### What makes a world "virtual"

Bartle later set out a definition that most of the field still uses. In paraphrase, a virtual world has six properties:

1. It runs on automated rules, its physics.
2. Each player is represented by one character inside it.
3. Interaction happens in real time.
4. The world is shared. Other people are in it with you at the same time.
5. The world is persistent. It is still there when you log off.
6. It is not the real world.

Colossal Cave has the first three and the last one. It fails "shared" and "persistent." MUD1 has all six, although its persistence has a twist. Characters and scores persist, while the treasure layout persists only until the next reset. MMO301 week 1 studies this definition in depth ([MMO301 week 1 lecture](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w01-what-is-a-virtual-world-bartles-definition.md)).

The definition is a tool, not a verdict. Use it to ask precise questions. A battle-royale match is shared and real-time but not persistent. A single-player open world is persistent but not shared. Each missing property removes a set of design problems, and the rest of this lecture shows what the "shared" property adds.

## 3. Worked example: one treasure, many players

### The hook

In Colossal Cave, the brass lamp is always on the floor of the building when you arrive. In MUD1 it is there only if nobody got there first. The same cave, the same puzzles, the same points. Yet MUD1 players describe a game of races, ambushes and killing, while Adventure players describe a quiet puzzle. What changed?

The only change is that the treasure is shared. Let's measure what sharing does.

### The model

Keep it as simple as possible. One reset period of the world lasts `L` hours. The world starts each period holding treasure worth `V` points in total. Each of `N` equally skilled players, working alone in an empty world, could find and swamp treasure at `f` points per hour.

With `N` players all swamping, the pool drains at `N × f` points per hour, so it empties after `V / (N × f)` hours. If that is longer than `L`, nobody ever runs out and each player earns `f`. If it is shorter, the pool is empty for the rest of the period, and each player's share of the whole pool is `V / N`. So each player's income, in points per hour, is:

```
income(N) = min( f , V / (N × L) )

crossover population   N* = V / (f × L)
dry share of period    = max( 0 , 1 − V / (N × f × L) )
hours to make wiz      = 102,400 / income(N)
```

- `N` is the number of active players.
- `V` is the treasure value in the world per reset, `f` the solo income rate, `L` the reset period in hours.
- `N*` is the crossover population. Below it, other players cost you nothing. Above it, every extra player lowers everyone's income.
- The dry share is the fraction of each period when the world holds no treasure at all.

Only the 102,400 threshold is MUD1's real number. The values of `V`, `f` and `L` below are invented to make the arithmetic easy. MUD1's real treasure values and reset timing varied with how fast players emptied the world, and we do not need them to see the mechanism.

### Numbers you can check

Let `V = 5,000` points per reset, `f = 400` points per hour and `L = 2` hours. Then `N* = 5,000 / (400 × 2) = 6.25` players.

| Players N | Income (points/hour) | Hours to make wiz | Dry share of each period |
|---|---|---|---|
| 1 | 400 | 256 | 0% |
| 4 | 400 | 256 | 0% |
| 6 | 400 | 256 | 0% |
| 8 | 312.5 | 327.7 | 21.9% |
| 12 | 208.3 | 491.5 | 47.9% |
| 20 | 125 | 819.2 | 68.8% |

Check the row for 8 players. The pool drains at `8 × 400 = 3,200` points per hour, so it empties after `5,000 / 3,200 = 1.5625` hours. The period is 2 hours, so the world is dry for 0.4375 hours, which is 21.9% of it. Each player's share is `5,000 / 8 = 625` points per 2 hours, or 312.5 points per hour. Making wiz takes `102,400 / 312.5 = 327.7` hours.

Two regimes appear, and the line between them is sharp.

1. **Below `N*`, sharing is free.** From 1 to 6 players, income is 400 points per hour and nothing about other players affects it. They are company. You can chat, help and trade with no cost.
2. **Above `N*`, sharing is zero-sum.** Zero-sum means one player's gain is exactly another's loss. At 20 players, the pool is gone 69% of the time, and any treasure you swamp is treasure someone else cannot. Your income depends on beating others, not on skill at the puzzles.

Now ask what a player does during the dry share of the period. In MUD1 there is exactly one source of points left when the treasure is gone, and it is other players, who carry items and are worth points when killed. The model does not include player killing, and it does not need to. It shows that, above `N*`, the design leaves players with nothing else to do.

### The visual

Open the interactive. The left chart, "One player's view," plots your income against the number of players. It is flat, then it bends down at `N*`, and a marker shows the current `N`. The right chart, "The world's view," shows one reset period as a horizontal bar. The treasure pool drains as a shrinking block and the dry share is shaded red, labeled "only other players left."

Drag the player count from 1 to 20. The left line barely moves until 6, then falls. The right bar turns red from the end inward. Then switch on "Per-player treasure," which gives each player their own copy of the pool. Both charts go flat at 400 points an hour, whatever `N` is.

### Cross-game recognition

The same contention appears whenever many players want a limited resource in one shared space. Rewrite each case in the model's terms. What is `V`, what is `N`, and what happens when `N` passes `N*`?

**EverQuest (1999 onward, early years).** EverQuest's dungeons were shared, open spaces. Valuable items dropped from particular monsters that respawned on a timer. Here `V` is the loot from one respawn and `L` is the respawn timer. With many groups in one dungeon, `N` was far past `N*`. Groups competed for the same monsters and sometimes harassed each other. Players named the resulting behaviors camping (waiting at a spawn point to claim it), kill stealing (landing the last hit on someone else's monster) and ninja looting (taking loot you were not owed). Each is what the dry share of a period looks like in a graphical world.

**Instanced dungeons (The Realm Online, 1996, and most later MMOs).** An instance is a private copy of an area created for one group. It sets `V` per group instead of per world, so the pool no longer shrinks as `N` grows. The Realm Online is sometimes credited with the first instances, running each battle in a separate room outside the open world. Instancing became common in the MMOs that followed.

**Guild Wars 2 (2012 to the present).** Guild Wars 2 applies the same fix to gathering. Most resource nodes, such as ore veins, can be harvested by each character separately, then reset for that character a few hours later. Two players at the same vein never compete for it. In the model, `V` is multiplied by `N`, so `N*` disappears. That is exactly the "per-player treasure" switch in the interactive.

MUD1, EverQuest and Guild Wars 2 sit at three points on one line. MUD1 has a fully shared pool, EverQuest shared pools with timers, Guild Wars 2 per-player pools. Each chose where to sit, and the rest of their social life followed.

### Design judgment, eyes open

It is tempting to conclude that contention is a bug and per-player resources the fix. Some of the best-known designers of the genre disagree.

- **What sharing gives you.** Contention makes other players matter. They are rivals, allies, threats and stories. MUD1's reputation, the fear, the alliances and the legends of famous killers, came from its shared pool. EverQuest's lead designer Brad McQuaid wrote in 2005 that instancing harms a world's community, its economy and how long players stay. Raph Koster answered that instancing should be used only where a private space makes sense inside the fiction.
- **What sharing costs you.** Above `N*`, new players lose. A veteran who knows the world empties the pool before a beginner has found the swamp. Players who dislike conflict leave, and the world tilts toward those who enjoy it. Bartle's 1996 paper on player types, studied in MMO301, grew out of watching exactly this balance in MUDs.
- **What to decide deliberately.** For each resource in your world, choose whether it is shared, instanced or per-player, and compute `N*` for your expected population at peak hours. A resource with `N*` far above your peak population will feel generous. One with `N*` far below it will create camping, whatever your intentions. Also decide what players do in the dry share of each period, because they will find something.

## 4. After MUD1: the MUD family and how to read a text game

### A family of codebases

MUD1 ran on one machine at one university. The genre spread when other people wrote their own servers and gave the code away.

- **AberMUD (1987),** written by Alan Cox at Aberystwyth, was the first widely copied MUD codebase.
- **TinyMUD (1989)** put building the world ahead of combat. Players made rooms and objects, and it became a model for social worlds.
- **LPMud (1989)** let builders program new content in its own language, combining flexibility with adventure play.
- **DikuMUD (1990)** focused on combat and levels. Its freely available code led to a large wave of hack-and-slash MUDs.

These families split along the same line as the worked example. TinyMUD's descendants removed the contested treasure pool and put socializing first. DikuMUD's leaned into combat and progression. Week 9 follows this split into the first graphical MMOs.

### Close reading a text game

This course asks you to write two close readings. A close reading is a careful analysis of how a specific part of a game produces its effect on the player, supported by evidence from play. Text games are ideal practice, because every word the game shows is evidence you can quote and every command you type is a data point.

A simple method, which Lab 05 uses:

1. **Record.** Play with a log running. Save the full transcript of what you typed and what the game printed.
2. **Pick a moment.** Choose one short passage, a room, a puzzle or a death, of no more than a page.
3. **Describe the rule.** What rules produced that passage? For a parser game, include what the parser accepted and refused.
4. **Describe the effect.** What did the passage make you feel or do? Name the behavior, not only the emotion. ("I typed six synonyms for 'open.'")
5. **Connect.** Link the rule to the effect, and the rule to its historical context, such as the memory limit, the vocabulary size or the network.

The last step is what makes it history rather than a review. A reading of Adventure that never mentions the two-word parser, or of MUD1 that never mentions the shared treasure pool, misses the rule that explains the play.

## In-class activity (25 minutes)

Groups of three. Each group gets one of these shared resources from a game its members know. The options are a boss that drops a rare mount, a fishing spot, a rare-spawn monster, a mining vein, a quest item on the ground.

1. (10 min) Estimate `V`, `f` and `L` for your resource in whatever units make sense (items per hour, gold per respawn). Compute `N*`. Compare it with how many players you usually see at that spot during peak hours.
2. (5 min) Use the interactive to predict income and dry share at that peak population.
3. (10 min) Propose one change that moves the resource to a different point on the shared, timed, per-player line. Name one thing your change gives up, using McQuaid's or Koster's argument.

Expected output: your three estimates, `N*`, the peak-hour prediction, and your change with its cost in one sentence.

## Common misconceptions

- **"MUD1 was a chat room with monsters."** It was a competitive game with a clear goal (102,400 points), permanent death and a limited treasure pool. The social life grew around the competition.
- **"More players always makes a world more fun."** More players help only up to the crossover population for each contested resource. Past it, each new player makes things worse for everyone already there.
- **"Instancing is a technical trick."** It is a design decision that changes the economics of contention. It sets the pool per group instead of per world, and it gives up some of what makes a shared world matter.
- **"Text games had no design constraints."** Memory, vocabulary size and parser limits decided what players could do and how puzzles felt. The two-word parser created "guess the verb."

## Check yourself

1. In the worked example (`V = 5,000`, `f = 400`, `L = 2`), how many hours does it take to make wiz with 16 players? What share of each period is the world dry?
2. A wizard proposes doubling the treasure in the world while keeping the same reset period. What happens to `N*`? How many hours to make wiz with 20 players?
3. A designer halves the reset period to 1 hour without changing `V`. Show that `N*` doubles, and explain in one sentence why shorter periods help crowded worlds.
4. Use Bartle's six properties to classify a single-player game with an online leaderboard, and a Minecraft server that stays on all the time. Which properties does each have?

<details>
<summary>Answers</summary>

1. Income `= min(400, 5,000 / (16 × 2)) = 156.25` points per hour. Hours to wiz `= 102,400 / 156.25 = 655.4`. Dry share `= 1 − 5,000 / (16 × 400 × 2) = 1 − 0.390625 = 60.9%`.
2. `N* = 10,000 / (400 × 2) = 12.5`, doubled. With 20 players, income `= min(400, 10,000 / 40) = 250`, so wiz takes `102,400 / 250 = 409.6` hours instead of 819.2.
3. `N* = V / (f × L) = 5,000 / (400 × 1) = 12.5`, twice 6.25. The pool refills twice as often, so more players can share it before anyone runs dry. The world's total supply per hour doubles.
4. The single-player game with a leaderboard has rules, a character, real time and is not the real world. The leaderboard shares scores, not the world, so it is not shared, and nothing persists in the world when you leave. It is not a virtual world. The always-on Minecraft server has all six properties.

</details>

## Lab / assignment hook

[Lab 05, close reading a parser game](../labs/lab05.md). Play Open Adventure with a transcript log, pick one passage and write a 600-word close reading using the five-step method in section 4. This is a practice run for the first graded close reading.

## Sources

- Wikipedia, "Colossal Cave Adventure" (accessed September 2026). Crowther 1975-76 on the PDP-10; Mammoth Cave caving; written for his daughters; Woods's 1977 expansion and the ARPANET email search; about 140 locations, 293 words and 53 objects; one- or two-word commands; five treasures plus ten; 350 points in the 1977 version; World Video Game Hall of Fame 2019.
- Raymond, E. S. et al., Open Adventure (gitlab.com/esr/open-adventure). A BSD-licensed forward port of Crowther and Woods's Adventure 2.5 (1995), released with the authors' permission. Note that version 2.5 has a larger point total than the 1977 350-point version.
- Wikipedia, "Zork" (accessed September 2026). MIT authors and May 1977 start; parser beyond two-word commands; Infocom founded 1979; Zork I December 1980; Z-machine by Blank and Berez; sales of 38,000 by end of 1982, about 150,000 by 1984, over 680,000 for the trilogy through 1986; the 2007 Library of Congress canon list.
- Bartle, R., "Early MUD History" (mud.co.uk/richard/mudhist.htm). Trubshaw's autumn 1978 start in MACRO-10; the BCPL rewrite from late 1979 to about Easter 1980; Bartle taking over at about 25% complete and adding the wizard system; the DEC-10 memory limit; first external players in spring 1980.
- Wikipedia, "MUD1" and "Multi-user dungeon" (accessed September 2026). Naming after the Dungeon variant of Zork; 1983 outside access via BT PSS, 2am to 8am; British Legends on CompuServe until late 1999; Viktor Toth's 2000 C++ version; 2020 source release; AberMUD 1987 (Alan Cox), TinyMUD 1989, LPMud 1989, DikuMUD 1990.
- British Legends, "How to play" and "More advice" help pages (british-legends.com, current revival of the CompuServe-era game). 102,400 points to make wiz; swamping treasure; points for killing players; permanent death at zero stamina; resets when the world is emptied of treasure; the "beat the other players" advice.
- Bartle, R. (2015). *MMOs from the Inside Out*. Apress. Six-property definition of a virtual world, paraphrased (as quoted in Wikipedia, "Virtual world"). Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF edition from the author, mud.co.uk/richard/DesigningVirtualWorlds.pdf (chapter 1 is pp. 1-107).
- Wikipedia, "Instance dungeon" (accessed September 2026). EverQuest contention; camping, kill stealing, ninja looting; The Realm Online (1996) as a possible first; McQuaid's 2005 essay against instancing and Koster's reply.
- Guild Wars 2 Wiki, "Gathering" (current game). Most nodes can be used by each character and reset for that character a few hours later.
- The treasure-pool model and every number in section 3 other than 102,400 are invented for teaching.

## Interactive spec: examples/w05-shared-treasure.html

**The one insight:** in a shared world, other players cost you nothing until the population passes the crossover `N* = V / (f × L)`. Past it, income falls as `1/N`, and the world spends most of each period empty of treasure, leaving other players as the only source of points.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (income chart on top).

- **Left chart, "One player's view":** horizontal axis players `N` from 1 to 40, vertical axis income in points per hour from 0 to `max(f, 50) × 1.1`. Plot `income(N)` as a line. Draw a vertical dashed line at `N*` labeled "N* = x.xx". Mark the current `N` with a dot and its value. When "per-player treasure" is on, draw the line flat at `min(f, V / L)` and hide the `N*` marker.
- **Right view, "The world's view":** one horizontal bar representing one reset period of `L` hours, with a time axis in hours. The part of the period when the pool still has treasure is a solid block; the dry part is shaded in the palette's warning color and labeled "dry: only other players left". Above the bar, a small row of `N` player dots (cap the drawing at 40).
- **Readouts (copyable):** `N*` (two decimals), income (two decimals), hours to make wiz (one decimal), dry share (one decimal percent), time until the pool empties in hours (two decimals, or "never" when it does not).

**Controls (keyboard accessible, labeled):**

1. Players `N`: slider 1 to 40, step 1, default 12.
2. Treasure per reset `V`: slider 1,000 to 20,000, step 500, default 5,000.
3. Solo income `f`: slider 100 to 1,000 points/hour, step 50, default 400.
4. Reset period `L`: slider 0.5 to 6 hours, step 0.5, default 2.
5. Toggle "Per-player treasure" (default off). When on, the pool is `V` per player, so `income = min(f, V / L)` and the dry share uses `1 − V / (f × L)` floored at 0.
6. Reset button.

**Formulas.**

```
N*          = V / (f × L)
income(N)   = min(f, V / (N × L))            shared mode
income      = min(f, V / L)                  per-player mode
empty_at    = V / (N × f)                    shared; per-player: V / f
dry_share   = max(0, 1 − empty_at / L)
wiz_hours   = 102400 / income
```

**Test values** (`V = 5,000`, `f = 400`, `L = 2`, shared): `N* = 6.25`.

| N | Income | Wiz hours | Dry share | Empties at (h) |
|---|---|---|---|---|
| 1 | 400.00 | 256.0 | 0.0% | 12.50 (never within period) |
| 6 | 400.00 | 256.0 | 0.0% | 2.08 (never within period) |
| 7 | 357.14 | 286.7 | 10.7% | 1.79 |
| 8 | 312.50 | 327.7 | 21.9% | 1.56 |
| 12 | 208.33 | 491.5 | 47.9% | 1.04 |
| 16 | 156.25 | 655.4 | 60.9% | 0.78 |
| 20 | 125.00 | 819.2 | 68.8% | 0.63 |
| 30 | 83.33 | 1,228.8 | 79.2% | 0.42 |

When "empties at" is greater than or equal to `L`, show "never" in the readout.

`V = 10,000`, other defaults: `N* = 12.50`; at `N = 20`, income 250.00, wiz 409.6 hours, dry share 37.5%.

`L = 1`, other defaults: `N* = 12.50`; at `N = 12`, income 400.00 (5,000 / 12 = 416.67 is above `f`).

Per-player mode, defaults: income 400.00 for every `N`, wiz 256.0 hours, dry share 0.0%.

**First screen:** `N = 12`, shared mode. The left chart shows the flat-then-falling curve with the dot well past the `N*` line, and the right bar is nearly half red. Caption above both views: "12 players: income 208 points/hour, world dry 48% of the time."

**Content rules.** No game art or logos. Draw players as plain dots and the pool as a plain block. Small text under the views: "Only the 102,400-point wizard threshold is MUD1's. The pool, rates and period are illustrative."
