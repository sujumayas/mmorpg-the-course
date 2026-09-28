# MMO301 · Week 02 — MUD1, MUDs, MOOs and the Text Era

**Why this matters:** Within about two years, around 1989 to 1991, text worlds split into families that disagreed about one question: who gets to build the world? Every MMO since has picked a side, usually without saying so. If you understand what each answer did to content supply, storage and community in the text era, you can predict what it will do to your game, including the user-generated-content platforms that dominate today.

**You will be able to:**
- Trace MUD1's descendants (AberMUD, TinyMUD, LPMud, DikuMUD, MOO, MUSH) and state what each decided about building, persistence and play.
- Compute when a player runs out of worthwhile content in a designer-built world and a player-built world, and the population at which building outpaces exploring.
- Find the population window in which a builder world neither runs dry nor fills its storage, and show how restricting builders widens it.
- Critique the LambdaMOO governance story as a design consequence of letting everyone build.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 1, "The Third Age: 1989-1995" (pp. 12-17) and the content and change discussion (pp. 74-83). Reread the LambdaMOO pages of chapter 6 on Curtis's observations (pp. 660-663). Dibbell, "A Rape in Cyberspace," *The Village Voice*, 21 December 1993 (the article describes sexual harassment in a text world; read the introduction and the sections on the community meeting and the petition system if you prefer to skip the account itself).

**Prerequisites from earlier courses:** [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) covers MUD1's history, its treasure-and-reset rules and a first list of MUD codebases. Read it first; this lecture does not repeat it. [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) gives you the stock-and-rate thinking the worked example uses. [MA101 week 6, rational functions and asymptotes](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) explains why the run-out time shoots to infinity at one population. Within this course, [week 1](w01-what-is-a-virtual-world-bartles-definition.md) introduced Bartle's change dial, who gets to build.

**Interactive:** [w02-content-race.html](../examples/w02-content-race.html). Keep it open during section 2.

---

## 1. After MUD1: one world, many families

GS101 week 5 left MUD1 running at Essex and later on CompuServe as British Legends. Bartle's history divides what came next into ages. The First Age, 1978 to 1985, is MUD1 and its immediate imitators. The Third Age, 1989 to 1995, is when free codebases spread across university Unix machines and the genre split.

The split was about building. Recall from week 1 that **building** means adding content directly, outside the normal rules of play. A MUD that lets you type a command to create a new room is letting you build. A MUD where new rooms appear only when an administrator edits the data files is not.

### The families

**AberMUD (1987)** was the first codebase to spread widely. Bartle describes copies appearing on thousands of Unix machines. It kept MUD1's shape, an adventure world of a few hundred rooms built by its authors.

**Monster (1988)**, by Rich Skrenta at Northwestern University, was written outside the MUD1 lineage. Its main idea was letting players create parts of the world from inside it. Bartle notes that MUD1 once had a similar facility, removed when it moved from version II to version III.

**TinyMUD (1989)**, by Jim Aspnes at Carnegie Mellon, was a stripped-down Monster with almost no game in it. Players could create rooms and objects nearly at will. Bartle gives the numbers that matter for this week. MUD1 and AberMUD had around 400 to 500 locations. A popular TinyMUD called Islandia passed 14,000 locations within a few months of opening in 1990. The "D" in TinyMUD was said to stand for "Dimension" instead of "Dungeon," which is where the MUD versus MU* naming split from week 1 began.

**LPMud (1989)**, by Lars Pensjö at the University of Gothenburg, took the opposite bet from most designers of the time. Pensjö thought players could build a better world than he could. He wrote an in-game programming language, LPC, and let *experienced* players use it to add objects and whole new behaviors while the game ran.

**DikuMUD (1990)**, by five students at the University of Copenhagen, went the other way. Bartle describes it as designed to be a better AberMUD, with everything hard-coded, and hard-coded well. A competent C programmer could change its data files and have a new world. Many did, and the Circle, Merc and ROM codebases descend from it. DikuMUD's play was combat, classes, levels and groups.

**MOO (1990)**. Stephen White extended TinyMUD into TinyMUCK and then MOO ("MUD, Object Oriented"), which added a full scripting language to a social world. Pavel Curtis at Xerox PARC used it to run **LambdaMOO**, opened to the public in January 1991.

**TinyMUSH (1990)**, by Larry Foard, added triggers and puppets that suited role-play. Its descendants, the MUSHes, are mostly role-playing worlds. Many restrict building to their own staff, even though the software would let anyone build.

### The families on week 1's two dials

| Family | Who builds | What persists (Bartle's ladder) | Center of play |
|---|---|---|---|
| AberMUD | Coders only | Initial state and characters (level 1) | Adventure, points, player killing |
| DikuMUD | Trained administrators, via data files | Plus carried items (level 2) | Combat, levels, classes, groups |
| LPMud | Experienced players, in LPC | Varies by world | Mostly combat, not required |
| TinyMUD | Anyone | Everything built | Building and talking |
| MOO | Anyone, including code | Entire world plus new functionality (level 5) | Social life, building, programming |
| MUSH | Usually staff only | High | Role-play |

Bartle's Table 1.3 in *Designing Virtual Worlds* places these codebases on the persistence-versus-change grid, and the diagonal from week 1 shows up clearly. The more people who can build, the more of the world tends to persist.

## 2. Worked example: the content race

### The hook

Islandia went from nothing to over 14,000 rooms in a few months. MUD1 has had, in Bartle's words, only minor changes to its world since 1985, and people still play it. A designer-built world like EverQuest, by contrast, had to keep adding content because its players ran out of things to do. Three very different content stories. And Bartle's summary of the TinyMUDs is not a success story. Incarnations would appear on some university machine, have a few brilliant months, then collapse under acrimony, apathy and full disk packs.

So building fixes the content supply and then breaks something else. What is the rule?

### The model

Track one player's supply of **new places worth visiting**. Everything is measured in locations (rooms) per week.

```
G(N)   = D + q × b × N              worthwhile new locations per week
T_out  = S0 / (v − G(N))            weeks until a player runs out, if G(N) < v
N*     = (v − D) / (q × b)          population where building outpaces exploring
T_full = (K − S0) / (D + b × N)     weeks until storage is full
```

- `S0` is the number of locations at opening, all built by designers and all worth visiting.
- `D` is the designers' output, locations per week.
- `v` is how many new locations one player explores per week.
- `N` is the number of active players.
- `b` is locations built per player per week, averaged over all players, builders and non-builders.
- `q` is the share of player-built locations worth another player's time. Bartle is blunt about quality. Player creations are hit and miss, and players are harsh judges who will simply stay away from a castle they think is bad.
- `K` is the storage cap, in locations. In 1990 that was a disk pack. Today it is database size, backup time and server memory. The number changed, the shape did not.

Content is **non-rival**. When you visit a room, it is still there for me. So a player runs out when their own exploring outpaces what is being added, and that is why `T_out` depends on `v − G` and not on how many other players there are, except through `b × N`.

The designer-only world is the special case `b = 0`. Then `G = D`, and a player runs out after `S0 / (v − D)` weeks no matter how many players the world has. More players never help.

### Numbers you can check

Use `S0 = 450` (MUD1 and AberMUD scale), `D = 5`, `v = 40`, `K = 20,000`. For an anyone-builds world set `b = 4` and `q = 0.1`. These parameters are invented. They are chosen so the builder world at 200 players reaches Islandia's 14,000 locations in about 17 weeks, roughly four months.

| Players `N` | Worthwhile per week `G` | Weeks until player runs out | Total growth per week | Weeks until storage full |
|---|---|---|---|---|
| 0 (designer only) | 5 | 12.9 | 5 | 3,910 |
| 25 | 15 | 18.0 | 105 | 186.2 |
| 50 | 25 | 30.0 | 205 | 95.4 |
| 75 | 35 | 90.0 | 305 | 64.1 |
| 88 | 40.2 | never | 357 | 54.8 |
| 100 | 45 | never | 405 | 48.3 |
| 200 | 85 | never | 805 | 24.3 |
| 500 | 205 | never | 2,005 | 9.8 |

The crossover is `N* = (40 − 5) / (0.1 × 4) = 87.5`. Above 88 players, building outpaces exploring and nobody runs out. Below it, even a busy builder world runs dry, just more slowly than the designer world.

Now read the last column. At 200 players, storage fills in 24 weeks. By then, 90% of everything players built is not worth visiting. Player-built junk is `0.9 × 800 × 24.3 ≈ 17,500` of the 20,000 locations, about 87% of the world. The world has not run out of content. It has drowned in it.

Put the two conditions together. Suppose you want storage to last at least a year, `T_full ≥ 52`. Then `D + b × N ≤ 19,550 / 52 ≈ 376`, so `N ≤ 92.7`. The world works only between 88 and 92 players. That is the TinyMUD lifecycle in one line. Too few players and it runs dry. A few more and it fills the disk.

Now restrict building LPMud-style. Only experienced players build, so fewer locations appear (`b = 0.5`), but more are worth visiting (`q = 0.6`), so `q × b = 0.3`:

| Players `N` | `G` | Weeks until player runs out | Weeks until storage full |
|---|---|---|---|
| 50 | 20 | 22.5 | 651.7 |
| 100 | 35 | 90.0 | 355.5 |
| 117 | 40.1 | never | 307.9 |
| 200 | 65 | never | 186.2 |
| 300 | 95 | never | 126.1 |

The crossover rises a little, to `N* = 35 / 0.3 ≈ 117`. But the upper limit for a one-year storage life jumps to `(376 − 5) / 0.5 ≈ 742` players. The working window goes from 88-92 to 117-742. Restricting who builds made the world *less* productive and *much* more robust.

### The visual

The interactive shows two linked charts against population `N`. The left chart is weeks until a player runs out, a curve that climbs and goes vertical at `N*`. The right chart is weeks until storage is full, a curve that falls as `N` grows. A shaded band marks the populations where both conditions hold. With the "anyone builds" preset the band is a sliver. Switch to "experienced players build" and the band opens wide. Drag `q` up with `b` fixed and watch the left asymptote slide left while the right curve does not move at all. Quality buys you content without costing storage. That is the one thing to take away from the picture.

### Cross-game recognition

**DikuMUD and EverQuest, designer-only supply.** Diku worlds grew only when administrators added areas. Bartle points out that for large worlds like EverQuest far more people want to play than there are things to do, so new content has to be added, and players who master the game demand high-end content fastest. In the model, `b = 0` and the only lever is `D`. To stop a player with `v = 40` from running out, `D` must reach 40 per week, for every player at once. That requirement is the content treadmill of [week 4](w04-everquest-the-treadmill-and-the-raid.md). Raph Koster has credited Diku gameplay as an inspiration for EverQuest, World of Warcraft and Ultima Online. In March 2000 Verant stated under oath that EverQuest's code was not based on DikuMUD source. The influence was the design, not the code.

**LambdaMOO, anyone builds, including code.** Everyone could build and program. Curtis reported 700 to 800 different players connecting per week and rarely more than 40 at once in the period his 1992 paper describes. By around 1994, Wikipedia's sources put the user base near 10,000 with over 300 connected at a time. `N` grew by an order of magnitude and the world kept its content. Its crisis came from a different place, section 3.

**Second Life (Linden Lab, June 2003 to now).** A graphical world built on the MOO premise. Residents build with in-world tools and a scripting language, LSL, and the terms of service let them keep copyright in what they create, so they can sell it. That is a direct attack on `b`, since ownership and income make people build more. Its marketplace listed about 2.1 million items in October 2024. With `b` that high, `q` becomes a search problem. A player cannot visit 2 million items, so the platform needs ways to find the good ones.

**Roblox (released 1 September 2006).** Every game on Roblox is built by users in Roblox Studio. Wikipedia reports 85.3 million daily active users in February 2025. By July 2020, at least 20 user-created games had passed a billion plays and at least 5,000 had passed a million. That concentration is `q` made visible. A small share of creations takes most of the play, and the platform's discovery system decides which. The storage limit `K` barely binds for a company with modern infrastructure. The attention limit, `v`, still does.

Five worlds, one race. Designer-only worlds fight `D` against `v`. Builder worlds win that race and then have to manage `K`, `q` and discovery.

### Eyes-open design judgment

- **Choose who builds before you choose how much.** The LPMud numbers show that restricting builders can widen the working window by a factor of a hundred. The usual reflex is "more user content is better." The model says quality per builder matters more than volume.
- **Every builder world needs a drain for content.** TinyMUD's drain was the whole world dying and players migrating, what Bartle calls slash-and-burn. A designed drain is gentler. Examples are deleting locations nobody has visited in 90 days, charging upkeep for building space, or letting builds decay unless maintained. Each of these makes `K` a flow instead of a wall. Each will anger the players whose builds disappear, which is the same politics Ultima Online's economy faced next week.
- **Curation is a design job, not a moderation afterthought.** On a platform with millions of creations, `q` is partly created by the platform. Search, ranking and featuring decide what counts as "worth visiting," which shapes what builders make next.
- **Remember the content you cannot build.** Bartle separates tangible content, which designers or players make, from the intangible content of other people. MUD1 survives on the second kind. A world that is scaled right for its players, as Bartle says MUD1 is, can run for decades with almost no new rooms. The model above counts only tangible content. It understates what a lively community is worth.
- **Building power is political power.** The moment players can change the world, they can change it against each other. The next section is about that.

### Check yourself (worked example)

1. A designer-only world has `S0 = 2,000` locations and adds `D = 20` per week. Players explore `v = 60` per week. How long until a player runs out? What `D` would make them never run out?
2. In an anyone-builds world with `D = 5`, `v = 40`, `b = 2` and `q = 0.25`, what is `N*`?
3. For that world with `S0 = 450` and `K = 20,000`, what is the largest `N` that keeps storage going for two years (104 weeks)? Is the working window empty?

<details>
<summary>Answers</summary>

1. `2,000 / (60 − 20) = 50` weeks. Never runs out when `D ≥ 60` per week.
2. `N* = (40 − 5) / (0.25 × 2) = 70` players.
3. `D + 2N ≤ 19,550 / 104 ≈ 188.0`, so `N ≤ 91.5`. The window is 70 to 91 players. It is not empty, but it is narrow.

</details>

## 3. When players own the world: LambdaMOO

Week 1's grid puts LambdaMOO in the quadrant where the world belongs to the players. LambdaMOO's history is what happens when a world's designers take that seriously.

### What Curtis saw

Pavel Curtis's 1992 paper, "Mudding: Social Phenomena in Text-Based Virtual Realities," reported what he observed as LambdaMOO's maintainer. Bartle summarizes it in chapter 6 of *Designing Virtual Worlds*, and the paper itself is short and readable. Around 90% of players connected from colleges and universities. Anonymity was the biggest social factor, lowering inhibitions both for good and for rudeness and harassment. The world relied on **wizards**, players with administrator powers, to police it. And the community connecting over a week was much larger than the number online at any one time. Curtis also noticed that when more than two people were in one location, passers-by tended to stop to see what was happening. That is week 1's density effect in a text world.

### Handing the world over

In December 1992 Curtis announced a policy change. The wizards would handle technical matters only. Social questions, including disputes and punishments, would be for the community to settle. This is the far end of the change dial, applied to rules as well as rooms.

In March 1993 a player called Mr. Bungle used a programmed object to make other players' characters appear to perform sexual acts they had not chosen. Many players treated it as a real violation of people, not a game event involving characters. The community argued for days over what to do, including a meeting of nearly three hours that reached no decision. One wizard, acting on his own, deleted the offending account. Julian Dibbell's article about the incident in *The Village Voice*, 21 December 1993, made LambdaMOO famous outside academia.

When Curtis returned, he set up a system of petitions and ballots. Anyone could put to a vote any change that needed administrator powers to carry out. Wikipedia, drawing on Bartle, dates the petition and ballot mechanism to summer 1993. Players also gained new tools, such as a command to eject a disruptive player.

### Reading it as design

Bartle's comment on the players' quadrant is dry. There is a problem, he writes, when what the players want is for the designers to take back control, "as they famously did with LambdaMOO." The design lesson is not that player governance fails. It is that governance comes with building, whether you design it or not.

- **Scripting is a weapon as well as a tool.** Mr. Bungle's attack used a player-built object. Any world that lets players program lets them program harm. MOO's power and LambdaMOO's crisis are the same feature.
- **"Social matters are the community's job" is still a design decision.** Petitions, ballots and eject commands are mechanics. Curtis had to design them after the crisis. You can design them before.
- **Scale changes governance.** A few dozen regulars can settle things by talking. Thousands cannot, and the numbers above show LambdaMOO grew from dozens online to hundreds. Informal rules that work at `N = 40` fail at `N = 300`.

MMO402 studies emergent governance in depth, starting with [MMO402 week 2, emergent player government](../../MMO402-emergent-society-governance-and-ethics/lectures/w02-emergent-player-government-alliances-and-councils.md). For now, carry forward the pairing. Whenever you move the change dial toward "anyone," move a governance design with it.

## 4. What the text era handed to graphical MMOs

The graphical worlds of GS101 week 9 did not start from zero. Four inheritances matter most.

**The Diku play loop.** Classes, levels, groups and hack-and-slash combat came into EverQuest and its successors through designers who had played Diku worlds. With it came the designer-only content model and its treadmill.

**The designers themselves.** Bartle notes that Raph Koster, Damion Schubert, Brad McQuaid and Jessica Mulligan were active on the MUD-Dev mailing list, where text-world designers argued theory in public. The first commercial graphical MMOs were designed by people whose instincts came from text worlds.

**The social-world lineage.** TinyMUD and MOO led to Second Life, not to EverQuest. The user-generated-content platforms of today are the MOO side of the 1990 split, rebuilt with graphics, money and search.

**The problems.** Contention and camping (GS101 week 5), player killing, harassment, content running out, storage filling up, governance. Every one was met and named in text first, usually in worlds of a few hundred players, where fixing mistakes was cheap. Graphical MMOs met them again at a hundred times the scale, often without reading the text-era record. That is the practical reason this course starts with MUDs.

## In-class activity (25 minutes)

In pairs, you run a new social world with building. Your server can hold `K = 50,000` locations. You open with `S0 = 1,000`, add `D = 10` per week, and players explore `v = 30` per week. You expect 400 active players in the first year.

1. **Choose a building policy (8 min).** Who can build (anyone, players past a time threshold, players who pass a review, staff only)? Estimate `b` and `q` for your policy and justify both numbers in one sentence each.
2. **Compute (8 min).** Find `N*` and `T_full` at `N = 400`. Is 400 inside your working window?
3. **Add a drain (5 min).** Design one mechanism that removes content. Estimate how many locations per week it removes at `N = 400`, and recompute storage life as `(K − S0) / (D + bN − drain)`.
4. **Governance (4 min).** Name one mechanism that lets players settle a dispute about a building, and who has the final say.

Expected output: your `b`, `q`, `N*`, storage life before and after the drain, and a one-line governance rule. One pair presents; another pair names who would hate the drain.

## Common misconceptions

- **"More player content is always better."** The model shows volume without quality fills storage and buries good content. The LPMud case builds less and works over a population range about a hundred times wider.
- **"A designer-built world can keep up if the team works hard."** In a designer-only world, every player needs `D ≥ v` separately. No team outbuilds a player base whose best players explore fastest. Week 4 takes this up.
- **"MUDs were a primitive stage before real MMOs."** Text worlds met and named most of the problems MMOs still have, and several are still running. LambdaMOO's governance crisis was a 1993 preview of problems modern platforms face with millions of users.
- **"TinyMUDs died because text is boring."** Bartle's account blames acrimony, apathy and full disk packs, which are social and storage failures, not a failure of the medium.

## Check yourself

1. Place TinyMUD, DikuMUD and LambdaMOO on week 1's persistence-versus-change grid and say whose world each is.
2. A builder world has `D = 0`, `v = 50`, `b = 5` and `q = 0.05`. Find `N*`. The team proposes a rating system that doubles `q`. What is the new `N*`, and what happens to storage life?
3. Why does the designer-only run-out time not depend on `N`, while the builder run-out time does?
4. LambdaMOO moved social decisions to the community in December 1992 and added petitions after March 1993. Explain, using the idea that building power is political power, why a combat-focused DikuMUD of the same size was less likely to face the same crisis.
5. A modern platform lets anyone publish a game. Storage is effectively unlimited. Which part of the content-race model still binds, and what design tool addresses it?

<details>
<summary>Answers</summary>

1. TinyMUD: anyone builds and what is built persists, so it is in the bottom-right, the players' world. DikuMUD: administrators build, carried items persist, top-left or near it, the designers' world. LambdaMOO: anyone builds including code, everything persists, bottom-right corner.
2. `N* = 50 / (0.05 × 5) = 200`. Doubling `q` gives `N* = 50 / 0.5 = 100`. Storage life does not change, because it depends on `D + bN`, not on `q`.
3. Content is non-rival. In a designer world the only new supply is `D`, which does not scale with players, so each player faces the same `v − D`. In a builder world, supply includes `q × b × N`, which grows with the population.
4. In DikuMUD players cannot create objects or code, so they cannot build tools for harming each other beyond what the designers coded, and the administrators who build also police. Disputes stay within fixed rules. In LambdaMOO players could program objects that acted on other players, so harm could be invented by players, and the rules for punishing it had been handed to the community.
5. Attention (`v`) and quality (`q`) still bind. A player can only explore so much, so most creations are never visited. The tool is discovery design (search, ranking, curation and featuring), which effectively raise the `q` of what players see.

</details>

## Lab / assignment hook

This week has no separate lab. The content-race model is one of the three models you may use in the first case study (40%), and [Lab 03](../labs/lab03.md) extends the same stock-and-flow method to Ultima Online's resources. If you want practice first, rebuild the two tables in section 2 in a spreadsheet and add a content drain that deletes a fixed share of unvisited locations per week.

## Sources

- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF from the author. Chapter 1: the ages of virtual worlds; AberMUD's spread; Monster (Skrenta, Northwestern, 1988) and the building facility removed from MUD1 between versions II and III; TinyMUD (Aspnes, Carnegie Mellon, 1989), the "Dimension" naming, MUD1 and AberMUD at about 400-500 locations and Islandia's 14,000-plus in a few months of 1990; LPMud (Pensjö, Gothenburg) and LPC; DikuMUD (Copenhagen, 1990) hard-coded with editable data files, and its Circle, Merc and ROM descendants; the TinyMUD slash-and-burn lifecycle; MOO (White, 1990), LambdaMOO (Curtis) and TinyMUSH (Foard, 1990) (pp. 12-17). The MUD-Dev list and its participants (p. 50). Tangible and intangible content, MUD1's minor changes since 1985, EverQuest's need for new content, who may build in MOOs and MUSHes, Table 1.3 (pp. 74-83). Summary of Curtis (1992) including the 700-800 weekly players and rarely more than 40 at once (pp. 660-663). Quality of player-built content (pp. 606-607). Paraphrased, with one short quoted phrase.
- Curtis, P. (1992). "Mudding: Social Phenomena in Text-Based Virtual Realities." Xerox PARC; presented at the Conference on Directions and Implications of Advanced Computing (DIAC-92), Berkeley. Checked against the paper (manuscript dated 3 March 1992, archived copy at web.archive.org/web/2003/http://www.ics.uci.edu/~jpd/moo/curtis92mudding.pdf, accessed September 2026): about 90% of players affiliated with colleges and universities; anonymity as the most significant social factor; wizards as the policing mechanism; 700 to 800 players connecting in a week but rarely more than 40 at once.
- Wikipedia, "LambdaMOO" (accessed September 2026). Founded by Curtis at Xerox PARC in 1990 and opened in January 1991; user base close to 10,000 with over 300 connected at a time around 1994; the December 1992 "New Direction" policy; the March 1993 incident; the petition and ballot mechanism from summer 1993.
- Wikipedia, "A Rape in Cyberspace" (accessed September 2026). Dibbell's article in *The Village Voice*, 21 December 1993; the community meeting of about two hours forty-five minutes; the wizard who acted alone; Curtis's petitions and ballots and the new eject command.
- Wikipedia, "Multi-user dungeon" (accessed September 2026). TinyMUD's late-1989 release and "Dimension"; Monster (1988) pioneering player building; LPMud (1989) and LPC; DikuMUD's 1990 release and influence.
- Wikipedia, "DikuMUD" (accessed September 2026). Authors and dates at DIKU, 1990-91; hack-and-slash style; Koster's statement on Diku gameplay inspiring EverQuest, World of Warcraft and Ultima Online; Verant's sworn statement of 17 March 2000 that EverQuest was not based on DikuMUD code.
- Wikipedia, "Second Life" (accessed September 2026). Launch by Linden Lab on 23 June 2003; building tools and LSL; users retain copyright in their creations; about 2.1 million marketplace items in October 2024.
- Wikipedia, "Roblox" (accessed September 2026). Release on 1 September 2006; games built in Roblox Studio with Luau; 85.3 million daily active users in February 2025; by July 2020 at least 20 games past one billion plays and at least 5,000 past one million.
- The content-race model and all its parameters are invented for teaching. Only Islandia's 14,000 locations and MUD1's 400-500 come from the sources.

## Interactive spec: examples/w02-content-race.html

**The one insight:** letting players build wins the race against content running out above a crossover population `N*`, and then loses a second race against storage. Restricting who builds lowers volume and raises quality, which barely moves `N*` but widens the working window enormously.

**Layout.** Two linked charts sharing the same horizontal axis, population `N` from 0 to 1,000 (log-scale toggle available), side by side on desktop and stacked on mobile.

- **Left chart, "Weeks until a player runs out":** vertical axis 0 to 200 weeks (values above 200 clip to the top edge and are labeled "never" when `G ≥ v`). Plot `T_out(N)`. Draw a vertical dashed line at `N*` labeled "N* = x.x".
- **Right chart, "Weeks until storage is full":** vertical axis 0 to 400 weeks (clip above). Plot `T_full(N)`. Draw a horizontal dashed line at the minimum acceptable life `T_min` and a vertical dashed line at `N_max`, where `T_full = T_min`.
- **Both charts:** shade the working window `N* ≤ N ≤ N_max` in the palette's success color. If `N_max < N*`, show a banner "No working window" in the warning color. A draggable marker for the current `N` appears on both charts.
- **Readouts (copyable):** `G` (one decimal), `T_out` (one decimal or "never"), `N*` (one decimal), total growth per week `D + bN`, `T_full` (one decimal), `N_max` (one decimal), window width `N_max − N*` (one decimal), and junk share at full storage `(1 − q) × b × N × T_full / K` (one decimal percent).

**Controls (keyboard accessible, labeled):**

1. Players `N`: slider 0 to 1,000, step 1, default 200.
2. Designer output `D`: slider 0 to 100 per week, step 1, default 5.
3. Exploration per player `v`: slider 10 to 100 per week, step 1, default 40.
4. Built per player `b`: slider 0 to 10 per week, step 0.1, default 4.
5. Share worth visiting `q`: slider 0.01 to 1.00, step 0.01, default 0.10.
6. Starting locations `S0`: number input 50 to 5,000, default 450.
7. Storage cap `K`: number input 1,000 to 200,000, default 20,000.
8. Minimum storage life `T_min`: slider 4 to 208 weeks, step 1, default 52.
9. Presets: "Anyone builds (TinyMUD-like)" `b = 4`, `q = 0.1`; "Experienced players build (LPMud-like)" `b = 0.5`, `q = 0.6`; "Designers only (Diku-like)" `b = 0`, `D = 5`. Presets keep `S0`, `K`, `v`, `T_min` and `N`.
10. Reset button.

**Formulas.**

```
G(N)    = D + q × b × N
T_out   = S0 / (v − G)            if G < v, else "never"
N*      = (v − D) / (q × b)       if q × b > 0; if D ≥ v then N* = 0; if q × b = 0 and D < v, "none"
T_full  = (K − S0) / (D + b × N)  if D + bN > 0, else "never"
N_max   = ((K − S0) / T_min − D) / b     if b > 0; else infinity
junk    = (1 − q) × b × N × T_full / K
```

**Test values** (`S0 = 450`, `D = 5`, `v = 40`, `K = 20,000`, `T_min = 52`):

Anyone builds (`b = 4`, `q = 0.1`): `N* = 87.5`, `N_max = 92.7`, window 5.2.

| `N` | `G` | `T_out` | `D + bN` | `T_full` |
|---|---|---|---|---|
| 0 | 5.0 | 12.9 | 5 | 3,910.0 |
| 25 | 15.0 | 18.0 | 105 | 186.2 |
| 50 | 25.0 | 30.0 | 205 | 95.4 |
| 75 | 35.0 | 90.0 | 305 | 64.1 |
| 88 | 40.2 | never | 357 | 54.8 |
| 100 | 45.0 | never | 405 | 48.3 |
| 200 | 85.0 | never | 805 | 24.3 |
| 500 | 205.0 | never | 2,005 | 9.8 |

Junk share at `N = 200`: 87.4%.

Experienced players build (`b = 0.5`, `q = 0.6`): `N* = 116.7`, `N_max = 741.9`, window 625.3.

| `N` | `G` | `T_out` | `D + bN` | `T_full` |
|---|---|---|---|---|
| 50 | 20.0 | 22.5 | 30 | 651.7 |
| 100 | 35.0 | 90.0 | 55 | 355.5 |
| 117 | 40.1 | never | 63.5 | 307.9 |
| 200 | 65.0 | never | 105 | 186.2 |
| 300 | 95.0 | never | 155 | 126.1 |

Designers only (`b = 0`): `T_out = 12.9` for every `N`, `N*` "none", `T_full = 3,910.0`, `N_max` infinite.

**First screen:** Anyone-builds preset at `N = 200`. The left chart shows the curve already past its asymptote ("never"), the right chart shows `T_full = 24.3`, below the 52-week line, and the shaded window is a thin sliver near 88-93. Caption: "200 builders never run out of places to go, and fill the disk in 24 weeks."

**Content rules.** No game art or logos. Draw rooms as plain squares if any illustration is used. Small text under the charts: "Only Islandia's 14,000 locations and MUD1's 400-500 are historical. All parameters are illustrative."
