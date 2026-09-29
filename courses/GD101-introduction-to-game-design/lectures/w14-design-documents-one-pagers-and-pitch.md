# GD101 · Week 14 — Design Documents: One-Pagers and Pitch

**Why this matters:** Your paper game only exists in your group's heads until you write it down. A one-page design is how a teammate, a tutor or a publisher finds out what you are making and why. It is also how you find out whether you know. This week you learn to write a one-pager whose promises are backed by mechanics, and to pitch it in three minutes.

**You will be able to:**
- Build a pillar-mechanic map from any design document and compute each pillar's support and each mechanic's load.
- Identify orphan mechanics, unsupported pillars and fragile pillars, and predict which mechanic changes are safe.
- Write a one-page design for your paper prototype that passes the swap test.
- Deliver a three-minute pitch whose every claim points to something on the page or something you playtested.

**Before class:** Fullerton, *Game Design Workshop* (4th ed.), chapter 6, "Conceptualization", and the pages on design documents in chapter 14, "Communicating Your Designs", about 30 pages in total. Read the Condor *Diablo* pitch (1994), which David Brevik hosts as a scanned PDF on his studio site (linked in Sources). It is eight pages including the cover. Bring your paper prototype's current rules.

**Prerequisites from earlier courses:** none outside this course. You need experience goals and the 8 kinds of fun from [GD101 week 5](w05-player-experience-goals-and-the-8-kinds-of-fun.md), iteration and cutting features from [GD101 week 8](w08-iteration-loops-and-kill-your-darlings.md), playtesting from [GD101 week 7](w07-playtesting-observe-dont-explain.md) and the mechanics grid from [GD101 week 13](w13-genres-as-clusters-of-mechanics.md).

**Interactive:** [The pitch pillar map](../examples/w14-pitch-pillar-map.html). Keep it open during section 2.

---

## 1. What a design document is for

A design document is any written description of a game that someone other than its author will act on. It can be a 200-page wiki or a single sheet. Its job is not to record everything you know. Its job is to let other people make the same decisions you would make when you are not in the room.

Documents fail in two opposite ways.

**Too long to read.** In November 1992, Tom Hall delivered the "Doom Bible" to his colleagues at id Software. It set out a science-fiction horror plot, a backstory and design goals for the game that became Doom. The rest of the team felt it put realism ahead of fun gameplay, and some of them did not see the need for a design document at all. The story was dropped and most of the design was removed. Hall left the company in July 1993, months before Doom shipped in December. A long document that the team does not share becomes a record of one person's game, not the team's.

**Too thin to act on.** The opposite failure is a page of adjectives. "Epic battles, deep crafting, a living world." Nobody can build from that. Every reader fills the gaps with a different game, and you find out at the first playtest that your team made three.

Stone Librande, then a designer at Maxis, gave a talk at GDC 2010 called "One-Page Designs." His argument, paraphrased, is that if most readers only get through the first page anyway, the design should fit on that page. He showed single-sheet designs from projects including Spore and Diablo III, drawn more like annotated posters than prose. The one-page limit forces you to choose. That is the point of it.

This course asks you for a one-pager because choosing is the skill you are learning. It is also short enough to check. And checking is where this lecture's model comes in.

### Promises and machinery

Every design document mixes two kinds of statement.

- **Pillars** are promises about the player's experience. "Every run feels different." "You always know why you lost." These are aesthetics in the MDA sense from week 4, and they are close cousins of the experience goals you wrote in week 5. A pillar is a sentence you want a playtester to say back to you unprompted.
- **Mechanics** are the machinery. "The dungeon is generated when you enter a level." "When you die, your character is deleted." These are the rules a programmer or a paper-prototype facilitator can carry out.

A design document is good when each promise is held up by machinery, and each piece of machinery holds up a promise. It is bad when a promise floats with nothing under it, or when a mechanic is in the document because someone liked it, with no promise it serves. That relationship is simple enough to count.

## 2. Worked example: the Diablo pitch that survived losing its turns

### The hook

In 1994, a small studio called Condor wrote an eight-page pitch for a computer role-playing game named Diablo. The pitch describes a player guiding one hero down through a dungeon, clicking square by square. It says plainly that the whole game runs on a "turn-based system," and it walks through an example turn where a fighter trades moves with two skeletons.

The game that reached shops at the turn of 1996 and 1997 is real-time. In January 1995 Blizzard, which had taken the project on, asked for two big changes, real-time play and multiplayer. (Blizzard bought Condor in 1996, after Blizzard's own parent company was sold to CUC International.) David Brevik, who led Condor, first resisted real time because he feared it would slow development. According to the development history, he then converted the game to real time over a single weekend.

So here is the puzzle. The most basic rule of the pitch changed. Yet if you read the pitch today, after playing the shipped game, you recognize almost everything else in it. Random dungeons, a town above, loot, classes and a descent to the devil are all there. Why did the document survive losing the rule it described most carefully? And which rule could it not have survived losing?

### The model

Write the document as a **pillar-mechanic map**, a grid with mechanics as rows and pillars as columns. Put a 1 in a cell when the document says, or clearly shows, that the mechanic serves that pillar. Otherwise leave it at 0.

```
L[m, p] = 1 if mechanic m serves pillar p, else 0

support(p) = Σ over mechanics of L[m, p]    (how many mechanics hold pillar p up)
load(m)    = Σ over pillars of L[m, p]      (how many pillars mechanic m holds up)
```

Four terms follow from the two counts.

- An **unsupported pillar** has `support = 0`. It is a promise with nothing under it.
- A **fragile pillar** has `support = 1`. One mechanic change and it falls.
- An **orphan mechanic** has `load = 0`. It costs production time and serves no promise. This is the "darling" from week 8 made visible.
- A mechanic is **critical** if removing it drops some pillar's support to 0. It is **structural** if removing it drops some pillar to 1 or less.

The **swap test** is the check you run before changing a mechanic. Remove its row, recompute every pillar's support, and see whether any pillar becomes unsupported or fragile. If none does, the change is safe at the level of the document. You can make it without rewriting your pitch. If one does, you are not changing a mechanic any more. You are changing what game you promised.

### Coding the Diablo pitch

The pitch names its own pillars in its first paragraph. It says the game is designed for maximum replayability, expandability and versatility, and that the emphasis will be on exploration, conflict and character development. That gives six candidates. "Versatility" is never tied to anything specific later in the pitch, so we leave it out and note it. That leaves five pillars.

| Code | Pillar (from the pitch, paraphrased) |
|---|---|
| Rp | Replayability: no two games are the same |
| Ex | Expandability: new content can be added after purchase |
| Xp | Exploration: the dungeon is revealed as you go |
| Cf | Conflict: tactical fights against monsters and traps |
| Cd | Character development: the hero grows in skill and gear |

Now the mechanics the pitch describes, with the links it makes. Each 1 below points to something the pitch says. Read the pitch and check them.

| Mechanic in the 1994 pitch | Rp | Ex | Xp | Cf | Cd | Load |
|---|---|---|---|---|---|---|
| m1 Random dungeon generated on entering each level | 1 | 1 | 1 | 0 | 0 | 3 |
| m2 Turn-based combat with action points | 0 | 0 | 0 | 1 | 0 | 1 |
| m3 Races, classes, stat points, spell schools | 0 | 0 | 0 | 0 | 1 | 1 |
| m4 Magic items and equipment | 0 | 1 | 0 | 1 | 1 | 3 |
| m5 Town trips (shop, temple, home) | 0 | 0 | 0 | 0 | 1 | 1 |
| m6 Lighting and line of sight | 0 | 0 | 1 | 0 | 0 | 1 |
| m7 Permanent death (character erased) | 0 | 0 | 0 | 0 | 0 | 0 |
| m8 Multiplayer by modem or network, with an arena | 0 | 1 | 0 | 1 | 0 | 2 |
| m9 Cheap expansion disks sold at the register | 1 | 1 | 0 | 0 | 0 | 2 |
| **Support** | **2** | **4** | **2** | **3** | **3** | |

Why each link is there:

- m1 serves Rp because the pitch says no two games will ever be the same. It serves Xp because new layouts create new exploration. It serves Ex because new items and creatures from expansion disks are fed into the random generator.
- m4 serves Ex because expansion disks were to carry new magic items. It serves Cf through themed items meant for specific monsters. It serves Cd because better equipment is part of how the hero grows.
- m8 serves Cf through the arena where players fight each other, and Ex because the pitch argues that playing with friends will sell expansion packs.
- m9 serves Ex directly, and Rp because the pitch says expansions add replay value.
- m7 has no link. The pitch describes a dead character being erased from the hard drive and the player starting from scratch. It never says which pillar this serves. That does not make permadeath a bad idea. It makes it an unjustified one, in this document.

### Numbers you can check

Totals first.

- Pillar coverage: every pillar has `support ≥ 1`, so coverage is 5 of 5.
- Fragile pillars: none. The lowest support is 2 (Rp and Xp).
- Orphans: one, m7.
- Total links: 2 + 4 + 2 + 3 + 3 = 14, which matches the load column, 3 + 1 + 1 + 3 + 1 + 1 + 0 + 2 + 2 = 14. The two totals must always agree. If yours do not, you miscounted.

Now the swap test, one mechanic at a time.

| Remove | Rp | Ex | Xp | Cf | Cd | Result |
|---|---|---|---|---|---|---|
| nothing | 2 | 4 | 2 | 3 | 3 | baseline |
| m2 turn-based combat | 2 | 4 | 2 | **2** | 3 | safe |
| m3 races and classes | 2 | 4 | 2 | 3 | **2** | safe |
| m7 permadeath | 2 | 4 | 2 | 3 | 3 | safe, nothing moves |
| m9 expansion disks | **1** | **3** | 2 | 3 | 3 | structural, Rp becomes fragile |
| m1 random dungeon | **1** | **3** | **1** | 3 | 3 | structural, Rp and Xp both fragile |

This answers the hook. Turn-based combat carried one pillar, Conflict, and Conflict had two other supports. Removing turns left every pillar standing. And the replacement, real-time combat, links to Conflict too, so after the swap Cf is back to 3. The change that took Brevik a weekend of programming took zero sentences of pitch rewriting.

The random dungeon is the opposite. It is the only mechanic whose removal leaves two pillars fragile at once. The pitch itself calls it the heart of the game. Take it out and you have a different pitch.

Now compare with what shipped. The released Diablo is real-time. It has sixteen randomly generated dungeon levels, three classes (Warrior, Rogue and Sorcerer), multiplayer for up to four players over a direct link, modem, network or Battle.net, and one expansion, Hellfire (1997), made by Synergistic Software and published by Sierra. Map those changes onto the table.

- m2 swapped for real-time combat. Safe, as computed.
- m3 simplified. Races are gone, classes remain. Still serves Cd. Safe.
- m1 kept. The one mechanic the swap test says is structural for two pillars made it through untouched.
- m8 kept and grown.
- m9 replaced by a full expansion from another studio. Ex keeps its support from m1, m4 and m8. Rp drops to 1, resting on the random dungeon alone, unless you count Hellfire as a new link to replay value. That is a coding choice worth arguing about in class.

We do not trace m7 here. Whether and how the shipped game handled character death is not something this lecture's sources confirm, so leave that cell for your own research.

### The visual

Open [`examples/w14-pitch-pillar-map.html`](../examples/w14-pitch-pillar-map.html). The left panel is the document as a reader sees it, a list of nine mechanics, all the same size and all looking equally important. The right panel is the same document as a structure. Five pillar columns rise to the height of their support, with a line from each mechanic to each pillar it serves.

Click a mechanic to remove it. On the left, one line of text disappears and the list still looks full. On the right, pillar bars drop, turn amber at support 1 and red at 0. Remove m2 and nothing turns amber. Remove m1 and two pillars do. Then press "Swap in real-time combat" and watch Conflict return to 3. The list view cannot tell you which removal matters. The pillar view shows it at once.

### Cross-game recognition

**The Doom Bible (id Software, 1992 to 1993).** Recode the story from section 1 as a map. Hall's document held up pillars of story and realism with levels built for them, such as realistic designs based on military architecture. The rest of the team held a different pillar, fast action built on new technology. In map terms, the document and the team had different columns. When the team removed the story mechanics, the story pillar became unsupported, and they dropped it rather than build new support. The map would have shown the mismatch before a single level was built. Two people could each list their pillars and see that the columns did not match.

**Librande's one-page designs (examples from Spore and Diablo III, GDC 2010).** Librande's sheets draw the relationships between parts of a design as a picture on one page. The pillar-mechanic grid is the plainest version of that picture. His format and this model share one goal: a reader should see, without reading paragraphs, which parts of the design hold up which goals. When a mechanic has no arrow to anything on a one-page diagram, it stands out the same way an orphan row does here.

**Your paper prototype (this course, weeks 6 to 15).** In week 8 you cut features. The swap test is the check you should have run before each cut. An orphan can go at no cost. A mechanic that is the last support of a pillar cannot go unless you also drop or re-support that pillar. In your playtest reports, each pillar becomes a question you ask testers, and support becomes something you can observe. If testers never mention "every game feels different," your Rp support was weaker than your grid claimed.

Three settings, one idea. A document is a set of promises plus a set of mechanisms, and its strength is in the links between them.

### Eyes-open design judgment

The pillar-mechanic map is quick and blunt. Use it knowing where it misleads.

- **A link is a claim, not a fact.** Putting a 1 in a cell says "we believe this mechanic produces this experience." Only a playtest confirms it. Treat the grid as a list of hypotheses and your playtest report as the results.
- **Counts ignore strength.** A random dungeon supports replayability far more than a shop does, but both score 1. If one link does most of the work, say so in a note. Some teams use 0 to 3 in each cell. That adds precision and adds arguments. For a one-pager, 0 or 1 plus a short note is usually enough.
- **Vague pillars break the model.** "Fun" or "polished" links to every mechanic, so its support is always high and tells you nothing. A useful pillar is specific enough that some mechanics do not serve it. If a pillar links to everything, rewrite it.
- **Too many pillars is the same as none.** With ten pillars, every mechanic serves something and nothing is an orphan. Three to five pillars is the common range, and it is the range the Diablo pitch landed in by itself.
- **Orphans are not always wrong.** A mechanic can be there for production reasons, for a business model, or because you want to test it. Permadeath in the Diablo pitch may have come from its roguelike parents (week 13) without anyone asking which pillar it served. That is exactly the moment to ask. Keep it, cut it or add a pillar it serves, but decide.

## 3. Anatomy of a one-page design

Your one-pager for this course has a fixed structure, so that tutors and classmates can compare them quickly. Each part has a job. The word counts are targets, and the whole page should land between 400 and 650 words plus the grid.

1. **Title and one-line description (under 25 words).** What the player does, in the present tense. "Two players race to map a flooding cave, trading tiles that open paths for you and close them for your rival."
2. **What it is like (under 60 words).** Your nearest neighbour from the week 13 genre map, and your one deliberate break. "Closest to Carcassonne-style tile laying, but tiles you place can be removed by rising water, so your map shrinks as it grows."
3. **Pillars (three to five, one sentence each).** Written as what a tester should say after playing. "I had to decide whether to help myself or hurt you."
4. **Core loop (a diagram or four to six steps).** What the player does again and again, every turn or every minute.
5. **Mechanics (a short list).** Only the ones that make this game different from its nearest neighbour. The rulebook holds the rest.
6. **Pillar-mechanic grid.** The table from section 2, with support and load totals. Every orphan either removed or labelled with the reason it stays.
7. **Out of scope (three to five bullets).** What you are deliberately not doing. This protects the project from the "wouldn't it be cool if" conversation.
8. **Evidence so far (under 80 words).** What your playtests have shown, with numbers from your week 7 method. "In 6 of 8 sessions, players named the water as the reason they changed plans."
9. **Open questions (two or three).** What you do not know yet and how you will find out.

Two rules keep the page honest.

- **Every pillar must appear in the grid with support at least 2**, or come with a sentence explaining why one support is enough for now.
- **Every sentence in the pitch must point to a line on this page.** If you say it out loud, it has to be written down.

### What to leave out

Long backstory, lists of every card, art direction boards and monetization plans do not belong on this page. They may belong in other documents. On the one-pager they push out the grid and the evidence, which are what a reader needs to decide whether your design holds together.

The Diablo pitch is a useful contrast here. It spends a full page on marketing, including a plan to sell small expansion disks at the register, inspired by the collectible model of Magic: The Gathering. It spends two more on a development plan, a one-year schedule for a team of eleven. For a company seeking a publisher in 1994, that was the right content, because the reader was deciding whether to fund it. Your reader is deciding whether your design is coherent. Know your reader and cut for them.

## 4. The pitch: three minutes, one page

A pitch is the spoken version of the one-pager. It has a different constraint. A reader can go back up the page. A listener cannot go back up the talk. So a pitch needs a fixed order and fewer ideas.

Use this structure for the course showcase. The times add up to three minutes.

| Part | Time | What you say | Points to |
|---|---|---|---|
| Hook | 0:00 to 0:20 | The one-line description, plus the moment players remember | Title line |
| What it is like | 0:20 to 0:40 | Nearest neighbour and the one break | What it is like |
| One turn | 0:40 to 1:40 | Walk the audience through one turn or one minute of play, with a real decision in it | Core loop, mechanics |
| Why it holds together | 1:40 to 2:20 | Each pillar and the two mechanics that hold it up | Grid |
| Evidence | 2:20 to 2:45 | One number from playtesting, and what you changed because of it | Evidence |
| Ask | 2:45 to 3:00 | What you want from the listener: testers, feedback on a named risk | Open questions |

The "one turn" part gets the most time on purpose. The Diablo pitch does the same thing. It walks through a sample session from the main menu to the dungeon, down to one fight played square by square. Listeners judge a game by imagining themselves playing it. Give them one concrete turn to imagine, with a choice in it, and they will fill in the rest in your favour. Give them a list of features and they will fill it in with whatever game they already know.

### Common pitch failures

- **The feature list.** "It has crafting, and trading, and a day-night cycle, and..." Features without pillars sound like a list of costs.
- **The adjective pitch.** "It's deep, strategic and emotional." These are claims the listener cannot check. Replace each adjective with the turn that produces it.
- **The lore opening.** Two minutes of world history before the listener knows what they do. Put setting inside the one-turn walk-through, where it shows up as things the player touches.
- **The hidden break.** Your game breaks a genre expectation from week 13 but you don't say so. Listeners assume the expectation holds, and your demo surprises them in the wrong way. Name the break in the first 40 seconds.

## 5. Documents that stay true

A one-pager is correct on the day you write it. After that, every playtest and every iteration moves the game away from it. A document the team stops trusting is worse than no document, because new team members still read it.

Three habits keep the page true.

- **Date and version the page.** Put "v3, week 12" at the top. When someone quotes the document, you know which game they mean.
- **Keep a change log under the page.** One line per change, with the reason and the evidence. "Removed trading (m6), orphan, testers never used it in 5 sessions." That line is your week 8 kill-your-darlings decision made visible.
- **Run the swap test on every change.** If a change makes a pillar fragile or unsupported, the change is not finished until you have fixed the grid or rewritten the pillar. The Diablo team could swap turns for real time because the pitch absorbed it. Check that yours will.

## In-class activity (30 minutes)

Work in your prototype teams, then swap with another team.

1. **(10 min)** On one sheet, write your prototype's pillars (three to five) and its mechanics (six to ten), without the grid.
2. **(5 min)** Swap sheets with another team. The other team fills in the grid for your game, using only what is on the sheet and what they remember from playing it in earlier weeks.
3. **(10 min)** Get your sheet back. Fill in your own grid on a second copy. Compare. Circle every cell where the two grids disagree.
4. **(5 min)** For each circled cell, write one sentence. Either the link is real but not visible on the page (fix the page), or the link is something you believe but your players did not see (plan a playtest question).

**Expected output:** two grids for your game, a list of disagreements, and at least one change to your one-pager draft. Teams with many disagreements are not failing. They have found out cheaply what their players would have found out expensively.

## Common misconceptions

- **"A longer document is a more complete design."** Completeness is about links, not length. The Doom Bible was long and the team built a different game. A one-pager with every pillar supported twice is more complete in the sense that matters.
- **"If a mechanic is cool, it belongs in the document."** A mechanic with load 0 is an orphan. It may still be worth testing, but it needs a reason written next to it, or it goes.
- **"Pillars should be broad so the design can change."** Broad pillars link to everything and stop telling you anything. The Diablo pitch changed its most basic rule without rewriting a pillar because its pillars were specific and well supported, not because they were vague.
- **"The pitch is a performance, separate from the design."** Every claim in the pitch should point to a line on the page. A pitch that says more than the document promises something nobody has designed.

## Check yourself

1. A one-pager has pillars A, B, C and mechanics m1 to m5. The links are m1 to A and B; m2 to B; m3 to C; m4 to nothing; m5 to A and C. Compute each pillar's support and each mechanic's load. Which mechanics are critical, and which are orphans?
2. In the Diablo grid, suppose the team had also dropped multiplayer (m8) and the expansion disks (m9) at the same time as the switch to real time. Recompute every pillar's support. Which pillars are now fragile?
3. A classmate's pillar is "the game is fun." It links to all eight of their mechanics. Explain, using support, why this pillar tells the team nothing, and rewrite it into a pillar that links to at most three of the mechanics in a trading card game you know.
4. Your pitch says "every game tells a different story," but your grid has no mechanic linked to that pillar. Give two ways to fix the mismatch, and say which you would choose if the showcase is in one week.

<details>
<summary>Answers</summary>

1. Support: A = 2 (m1, m5), B = 2 (m1, m2), C = 2 (m3, m5). Load: m1 = 2, m2 = 1, m3 = 1, m4 = 0, m5 = 2. Totals agree (6 and 6). No mechanic is critical, because every pillar has two supports and removing any one mechanic leaves each pillar at least 1. Every non-orphan mechanic is structural, because each pillar sits at exactly 2. Removing m1 leaves A and B at 1, m2 leaves B at 1, m3 leaves C at 1, m5 leaves A and C at 1. m4 is an orphan and can go at no cost.
2. Remove m8 and m9, and replace m2 with real-time combat linked to Cf. Rp = 1 (m1). Ex = 2 (m1, m4). Xp = 2 (m1, m6). Cf = 2 (real-time combat, m4). Cd = 3 (m3, m4, m5). Replayability is fragile, resting on the random dungeon alone. No pillar is unsupported.
3. A pillar linked to everything has support equal to the number of mechanics, so removing any one mechanic never changes it and the swap test can never fail. It gives no guidance about what to keep or cut. For a trading card game where you build a deck before each match, a better pillar is "Before the match, I made a bet on which cards would matter." It links to deck construction and card collection, but not to turn order or life totals.
4. Either add or name a mechanic that produces different stories (for example, random event cards or a variable setup), or remove the pillar from the pitch. With one week left, remove or narrow the claim to what the current mechanics support, because a new mechanic needs playtesting before you can claim its effect. Note the idea under open questions.

</details>

## Lab hook

**Lab 14, One-page design and pitch** ([labs/lab14.md](../labs/lab14.md)). Write the one-pager for your paper prototype using the structure in section 3, including the grid and a change log, and record a three-minute pitch. The one-pager is submitted with the final paper prototype and is read by showcase playtesters before they play.

## Sources

- Condor, Inc. (1994). *Diablo* game concept (pitch document, eight pages, scanned), hosted by David Brevik at graybeardgames.com. Pitch contents checked page by page against the scan (September 2026). Source for the turn-based design, the random level generator, the five named emphases, permanent character erasure, modem and network play with an arena, expansion disks sold at the register, and the Magic: The Gathering comparison. The short phrase "turn-based system" is quoted from its overview; everything else is paraphrased.
- Wikipedia, "Diablo (video game)," development and gameplay sections (re-read September 2026). Davidson & Associates, with Blizzard, sold to CUC International in February 1996, after which Condor became a Blizzard subsidiary; Wikipedia, "Blizzard Entertainment," also dates the acquisition to 1996. Blizzard's January 1995 request for real-time play and multiplayer; Brevik's conversion over one weekend; the 1994 pitch framing around Moria, NetHack and Rogue; release at the turn of 1996 and 1997; three classes; sixteen randomly generated levels; up to four players including Battle.net; *Hellfire* (November 1997) by Synergistic Software, published by Sierra.
- Wikipedia, "Doom (1993 video game)," development section. Tom Hall's Doom Bible (November 1992), the team's view that it put realism over gameplay, removal of the story and most of the design, Hall's departure in July 1993, release on December 10, 1993.
- Librande, S. (2010). "One-Page Designs." Game Developers Conference, GDC Vault. Talk by a designer then at EA/Maxis, with examples from Spore, Diablo III and a Simpsons project.
- Hunicke, R., LeBlanc, M. & Zubek, R. (2004). "MDA: A Formal Approach to Game Design and Game Research." Definitions of mechanics and aesthetics used for pillars and mechanics here.
- Fullerton, T. *Game Design Workshop* (4th ed., 2018), CRC Press, chapter 6 ("Conceptualization") and chapter 14 ("Communicating Your Designs"), the sections on design documentation. Chapter numbers checked against the publisher's chapter DOIs (10.1201/b22309).
- The pillar-mechanic coding of the Diablo pitch in section 2 is the author's, made for teaching from the pitch's own statements. Students should check each cell against the pitch.

## Interactive spec: examples/w14-pitch-pillar-map.html

**Insight the visual must make obvious:** a list of mechanics looks equally full whichever line you delete, but the pillar view shows that removing turn-based combat changes nothing structural while removing the random dungeon leaves two promises standing on one leg each.

**Layout:** two linked panels, side by side on desktop (list left, structure right), stacked on mobile (list on top). Below them, the editable grid and a readout.

**Left panel, "What the reader sees":** the nine mechanics as a plain text list in the order m1 to m9, all the same size. Each line is a toggle button (`aria-pressed`) labelled with the mechanic's name. Removed lines are struck through and dimmed but keep their place, so the list never visibly shrinks by more than the struck line.

**Right panel, "What holds the promises up":** five vertical bars, one per pillar (Rp, Ex, Xp, Cf, Cd), with full names below. Bar height equals current support, on a fixed axis from 0 to 5 with gridlines at each integer. Bar colour uses the palette tokens: neutral at support ≥ 2, amber (warning) at 1, red (danger) at 0, and each bar has a text status label ("ok", "fragile", "unsupported") so colour is not the only signal. Above the bars, draw each active mechanic as a small node, with a line from the node to each pillar it serves. Orphan nodes (load 0) get a dashed outline and the label "orphan."

**Grid (editable):** mechanics as rows, pillars as columns, 0/1 toggle cells (`aria-pressed`), arrow-key navigation and Space to toggle. Row totals (load) and column totals (support) update live. Show a check line "links by row = links by column" with both totals.

**Controls:**
- Clicking a mechanic in either panel removes or restores it.
- "Swap in real-time combat" button: replaces m2 with a new row "Real-time combat" linked to Cf only. Pressing again restores m2.
- "Run swap test" button: produces a table with one row per active mechanic showing the pillar supports after removing that mechanic alone, with a verdict column: "safe" (no pillar below 2 that was at 2 or above before, and none at 0), "structural" (some pillar drops to 1), "critical" (some pillar drops to 0).
- Presets: "Diablo pitch, 1994" (the lecture grid, default), "As shipped" (m2 replaced by real-time combat, m9 removed, m3 renamed "Classes (three)" with the same link, m7 greyed out and labelled "not traced"), "Blank 3 by 5" (pillars A, B, C; mechanics m1 to m5; empty grid, for the check-yourself questions), "Check yourself 1" (m1 to A and B; m2 to B; m3 to C; m4 none; m5 to A and C).
- Editable pillar and mechanic names (text inputs) in the blank preset.
- Reset button.

**Formulas:**
- `support(p) = Σ_m active(m) × L[m, p]`
- `load(m) = Σ_p L[m, p]`
- Swap test for mechanic k: `support_k(p) = support(p) − L[k, p]`; verdict critical if any `support_k(p) = 0` where `support(p) ≥ 1`; else structural if any `support_k(p) = 1` where `support(p) ≥ 2`; else safe.

**Test values (Diablo pitch preset):**
- Support: Rp 2, Ex 4, Xp 2, Cf 3, Cd 3. Loads: 3, 1, 1, 3, 1, 1, 0, 2, 2. Total links 14 both ways.
- Orphan: m7 only.
- Swap test: m2 safe (Cf 3 to 2); m3 safe (Cd 3 to 2); m5 safe; m6 structural (Xp 2 to 1); m7 safe; m8 safe; m4 safe (Ex 4 to 3, Cf 3 to 2, Cd 3 to 2); m9 structural (Rp 2 to 1); m1 structural (Rp 2 to 1 and Xp 2 to 1).
- "Swap in real-time combat": Cf returns to 3.
- "As shipped" preset: Rp 1 (fragile), Ex 3, Xp 2, Cf 3, Cd 3.
- "Check yourself 1" preset: support A 2, B 2, C 2; loads 2, 1, 1, 0, 2; m4 orphan and safe; m1, m2, m3 and m5 all structural; none critical.
