# MMO301 · Week 14 — Designing a world concept

**Why this matters:** Next week you hand in a world design bible. A bible built on a vague concept turns into a pile of lore and feature lists. A good concept answers a small set of hard questions early: who lives here, what lasts, how many people share a place, and how it ends. This week pulls the course together into one method and one number you can compute before anyone builds a map.

**You will be able to:**
- Write a one-page world concept that answers the seven world questions with specific, testable commitments.
- Compute a density budget: the playable area that gives a target number of players in view at peak, and the number off-peak.
- Design a response to the peak-to-trough gap (map copies, hubs, time-shifted content) and justify it with numbers.
- Critique a classmate's concept against the course's models (player types, persistence, shard density, sunset).

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 4, "Scope" (pp. 330-333) and "Geography" through "Levels of Geographic Abstraction" (pp. 357-366). Reread your notes from weeks 8, 12 and 13. Skim [GD101 week 14, design documents, one-pagers and the pitch](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) for the one-page format.

**Prerequisites from earlier courses:** [GD101 week 14, design documents](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) (the one-pager and the pitch). [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (area grows with the square of range). [MMO304 week 14, designing an economy from scratch](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w14-designing-an-economy-from-scratch.md) (the economy section of your concept). [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) (subscribers versus concurrent players). Within this course: [week 13, worlds that died](w13-worlds-that-died-shutdowns-and-their-lessons.md) (shard density and churn), and weeks [8](w08-player-types-bartle-1996-and-the-heros-journey.md), [9](w09-motivation-research-beyond-bartle-yee.md), [11](w11-kosters-laws-of-online-world-design.md) and [12](w12-persistence-and-time-what-should-last.md) on player types, motivation, Koster's laws and persistence.

**Interactive:** [examples/w14-density-budget.html](../examples/w14-density-budget.html). Keep it open during section 2.

---

## 1. What a world concept has to decide

In GD101 you wrote one-pagers for games. A game one-pager answers "what does the player do, and why is it fun?" A world concept has to answer that too, but a persistent shared world adds questions a single-player game never faces. Other people are the content, the world keeps running when you log off, and it will one day close.

Across this course we have met the pieces. Here they are as seven questions. A concept is ready for a bible when each has a specific answer, not a mood.

1. **Who is it for?** Which player motivations does the world serve first, and which does it tolerate? Use the models from weeks 8 and 9. "Socializers and explorers first, achievers second, killers only in opt-in zones" is an answer. "Everyone" is not.
2. **What do players do on a normal evening?** The core loop in one sentence, with the time it takes. A world needs a loop that works for a player with 45 minutes as well as one with four hours.
3. **What lasts?** From week 12. Which changes players make are permanent, which decay, which reset? A house that stays forever, a city wall that crumbles unless repaired, a dungeon that resets weekly.
4. **How many people share a place?** The density budget of section 2. How many players should you see at once, how big is the world, how is the population divided into shards or copies?
5. **What holds the economy together?** Faucets, sinks and the first market, from MMO304. One paragraph and one diagram at concept stage.
6. **What are the rules of conduct?** The laws a world owner cannot escape, from week 11, applied to your world. Where is player-versus-player allowed, who can grief whom, what does the operator promise not to do?
7. **How does it end?** From week 13. The sunset trigger and plan, written while the world is imaginary and nobody is attached to it yet.

Most student concepts spend three pages on question 1's fiction and one line on question 4. Professional pitches often do the same. That is backwards. The fiction can change in a week. A world built at the wrong size for its population takes a year to fix, and week 13 showed that some worlds do not survive the wait.

### Concept, pillars, commitments

Write the concept in three layers.

- **The sentence.** One sentence a stranger understands. "A drowned archipelago where every island is built by players and slowly reclaimed by the tide."
- **Pillars.** Three to five short statements of what the world will always protect, used to settle arguments later. "Building is permanent only if tended" is a pillar. "Great graphics" is not, because nobody would argue for the opposite.
- **Commitments.** The seven answers above, each with at least one number. Numbers make a concept testable. If you say "busy but never crowded," the density budget turns that into "four other players in view at peak, at least one at 3 a.m."

## 2. Worked example: the density budget

### The hook

EVE Online set its record for concurrent players on 5 May 2013, with 65,303 accounts logged in to one server. That sounds like a crowd. But the game has around 7,800 solar systems that players can visit. Spread evenly, the record is about 8 pilots per system. On an ordinary evening, with a fraction of that record online, most systems are empty and a few are packed.

Now a very different world. A Minecraft Java Edition server, with its default settings, allows 20 players. Its default view distance is 10 chunks in each direction, and a chunk is 16 by 16 blocks. So each player loads a square 336 blocks on a side around themselves. If those 20 players spread across an area only 750 blocks wide, each sees about four others. Walk a few thousand blocks in any direction and you are alone.

Both worlds face the same question. How much space should a population get? Too much and the world feels dead. Too little and it feels like a queue. You can answer it with one formula before you draw a map.

### The model

```
view area   = π × r²
E           = (1 − h) × P × π × r² / A        expected other players in view, in the field
A_needed    = (1 − h) × P × π × r² / E_target
```

- `P` is the number of players online at once on one shard or copy of the world (concurrent players, not subscribers; GS101 week 9 shows why the two differ).
- `h` is the share of those players in hubs (cities, markets, queues). Hubs are crowded on purpose. The field is everywhere else.
- `r` is the view radius in metres, the distance at which you notice and recognise another player. It is a design value, not the render distance.
- `A` is the playable field area in square metres. Count only ground players can reach and want to be on.
- `E` is the expected number of other players inside your view circle, if field players are spread evenly.

The assumption to keep in mind is "spread evenly." Real players bunch around quests, resources and roads. So `E` is an average, and the week 13 lesson applies. Players feel their local density, not the average. Treat `E` as the floor your content has to work with, then use layout to push players together where you want meetings.

Notice that `r` enters squared. That is the MA101 week 14 lesson in a new place. Double the view radius and every player sees four times as many others.

### Numbers you can check

Take an invented world with `P = 3,000` concurrent players at peak on one shard, `h = 0.4` (40% in hubs), a view radius `r = 150` m, and a target of `E = 4` others in view at peak.

The view area is `π × 150² = 70,686 m²`. The field holds `0.6 × 3,000 = 1,800` players. So

```
A_needed = 1,800 × 70,686 / 4 = 31,808,626 m² ≈ 31.8 km²
```

That is a square about 5.6 km on a side. Check it. With 1,800 players in 31.8 km², density is about 56.6 players per km². A view circle of 0.0707 km² holds `56.6 × 0.0707 ≈ 4.0` players.

Now the problem. Nobody is online at peak all day. Here is an invented but typical daily curve for a single-region shard, as a fraction of the peak:

| Hour (server time) | Share of peak | Concurrent P | Field players | E in view |
|---|---|---|---|---|
| 03:00 | 0.25 | 750 | 450 | 1.0 |
| 06:00 | 0.30 | 900 | 540 | 1.2 |
| 09:00 | 0.45 | 1,350 | 810 | 1.8 |
| 12:00 | 0.60 | 1,800 | 1,080 | 2.4 |
| 15:00 | 0.70 | 2,100 | 1,260 | 2.8 |
| 18:00 | 0.90 | 2,700 | 1,620 | 3.6 |
| 21:00 | 1.00 | 3,000 | 1,800 | 4.0 |
| 00:00 | 0.45 | 1,350 | 810 | 1.8 |

`E` is proportional to `P`, so it follows the daily curve exactly. A world sized for four at 9 p.m. has one player in view at 3 a.m.

Try the opposite. Size the world for `E = 4` at the 3 a.m. trough instead. Then `A = 450 × 70,686 / 4 ≈ 7.95 km²`, a quarter of the size, and at 9 p.m. each player sees 16 others in the field. Sixteen strangers in view feels like a busy high street. It is great for a festival and bad for a quiet forest you are meant to explore.

No single area works for the whole day. That is the finding. The ratio between busiest and quietest hour, here 4 to 1, becomes the ratio between crowded and empty, whatever size you pick.

### Closing the gap with copies

If you cannot change `A` through the day, change `P`. Build the world for the trough (7.95 km², `E = 4` at 3 a.m.) and open extra copies of each map as players arrive, so no copy passes a crowding limit `E_max`. Each copy gets `1 / n` of the players.

```
copies needed  n = ceil(E_single / E_max)
E per copy     = E_single / n
```

With `E_max = 6`:

| Hour | E if one copy | Copies needed | E per copy |
|---|---|---|---|
| 03:00 | 4.0 | 1 | 4.0 |
| 09:00 | 7.2 | 2 | 3.6 |
| 12:00 | 9.6 | 2 | 4.8 |
| 15:00 | 11.2 | 2 | 5.6 |
| 18:00 | 14.4 | 3 | 4.8 |
| 21:00 | 16.0 | 3 | 5.3 |

Now every hour sits between 3.6 and 5.6 others in view. The daily swing has gone from 4 to 1 (16 at peak against 4 at the trough) down to about 1.6 to 1 (5.6 against 3.6). That is exactly the week 13 lever, the number of shards `S`, turned from a launch decision into an hourly one.

Open the interactive. The left panel is a top-down map with dots for field players and your view circle in the middle. Move the hour slider and watch the dots thin out at night. The right panel plots `E` over 24 hours with a "lonely" band below 1 and a "crowded" band above `E_max`. Toggle "dynamic copies" and the right curve flattens into the comfortable band while the map on the left shows which copy you are in. To test a change in `r` on a fixed map, set Area mode to Manual. In the two sizing modes the map resizes itself to hold `E` at the target, so dragging `r` changes `A`, not `E`.

### Cross-game recognition

Each of these games made a density decision. Rewrite each one into the model.

**EVE Online (record of 5 May 2013).** One shard, so `S = 1`, and space divided into about 7,800 visitable solar systems. Treat a system as the area where players meet. Then the record of 65,303 is `P`, `A` is 7,800 systems, and average `E` is about 8.4 per system. The average hides how uneven the spread is, and that unevenness is part of the design. A large `A` leaves most systems quiet, and social contact concentrates in the few places players choose to gather (a large `h`).

**Minecraft, Java Edition (default server settings).** `P` is at most 20 (`max-players=20`). The view region is square, not round, so replace `π r²` with `(2 × 10 + 1)² × 16² = 112,896` square blocks. For four others in view at full capacity, `A = 20 × 112,896 / 4 ≈ 564,000` square blocks, a region about 750 blocks wide. The world itself is vastly bigger, so `A` is set by where players choose to build. Small servers stay social only when the group settles close together. The design hands the density decision to the players.

**Guild Wars 2 (megaserver system, completed 21 April 2014).** The game opens copies of open-world maps on demand and places players into them using their party, guild, language and home world. That is the copies table above, run automatically. `A` per map is fixed by the level designers, and `n` changes with the hour so that `E` stays in a band.

Three games, three answers to one formula. EVE fixes `P` on one shard and makes `A` huge. Minecraft keeps `P` small and lets players pick `A`. Guild Wars 2 fixes `A` and changes the number of copies. When you read any world's design, ask which of `P`, `A`, `r` and `n` it controls, and which it leaves to chance.

### Eyes-open design judgment

The density budget is a sizing tool, not a verdict. Decide these deliberately.

- **What `E` do you want, and where?** A survival world wants low `E` in the wilds so meetings are tense. A social world wants higher `E` along roads and at gathering points. Pick different targets for different zones, and write them in the concept.
- **Copies trade density for recognition.** Week 13 made this point for shards and it holds for map copies. If players land in a different copy every evening, they stop recognising each other. Guild Wars 2's placement rules try to keep friends and guilds together for this reason. Your concept must say how people who met yesterday can find each other today.
- **The view radius is a design choice.** Fog, terrain, forests and name-plate range all change `r`. Because `E` grows with `r²`, a thicker fog in one zone is the cheapest way to make it feel lonelier without moving a single player.
- **Hubs pull players out of the field.** Raising `h` (a great auction house, mailbox-only crafting) empties the rest of the world. A central market or bank draws players out of the field every time they visit it. Decide what must be done in the field and keep it there.
- **Size for your realistic concurrency, not your launch hope.** Week 13's 40-shard world is what happens when a team sizes for launch day. Pick `P` from a sober estimate, then plan copies for launch week and merges for month six.

## 3. From questions to a concept: a short example

Here is a compressed concept for an invented world, to show the level of commitment the bible needs. Every number is a design decision, not a claim about any real game.

**Sentence.** Tidewrack is a drowned archipelago where players build on islands the sea slowly takes back.

**Pillars.** Building is permanent only if tended. Every island is someone's. Strangers meet at the tide line. The sea is the only villain.

**Commitments.**

1. *Who is it for.* Builders and socializers first. Explorers second, through charting new islands after storms. No open player-versus-player combat; raids on untended ruins only.
2. *Normal evening.* 45 minutes: repair your island's sea wall, trade salvage at the nearest dock, join one storm event.
3. *What lasts.* Structures lose 2% integrity per real day unless repaired. At 0% they sink and become salvage for others. Characters and skills never decay.
4. *Density.* Peak `P = 3,000` per shard, `h = 0.4`, `r = 150` m, target `E = 4` at trough in the field and `E_max = 6`. Field area 7.95 km², with up to three copies per sea region at peak. Friends and guilds share a copy.
5. *Economy.* Salvage is the faucet. Sea-wall repair and sinking structures are the sinks. One dock market per region, no global auction house, to keep hubs small.
6. *Conduct.* Operators will never delete a tended structure. Harassment tools include blocking visits to your island.
7. *Ending.* Sunset trigger is median players per copy below 1,000 for eight weeks. Six months' notice, a final "great tide" event that sinks every island in order of age, character-sheet export, and a community-hosting licence for the server software.

Notice what this does to later arguments. When someone proposes a global auction house, pillar 3 and the `h` value in commitment 4 say no. You can still decide to change the pillar. But the decision is now visible.

## 4. Critiquing a concept

A world concept is easy to love and hard to test. Use these checks on your own draft and on a classmate's.

- **The number test.** Does every commitment contain a number or a rule someone could check in a build? Replace "rich crafting" with "four gathering and three crafting professions, each needing items from at least one other."
- **The night-shift test.** Run the density budget at the trough. Does the core loop still work with one other player in view? If group content is required, what does a solo player do at 3 a.m.?
- **The motivation test.** Take the player types you serve first. For each, name the thing they will do in week 10 of play, not week 1. Achievers need goals after the first goals end. Socializers need reasons to stay in one place with the same people.
- **The persistence test.** Pick one thing a player makes. Follow it for a year of real time. Is it still there, and does anyone still care? If the answer is "it piles up forever," you have a storage and clutter problem to design now.
- **The sunset test.** Could you run the ending you wrote with a team of three people and three months' notice? WildStar's closure in week 13 showed that the team may be gone before the end is announced.

## In-class activity (30 minutes)

Pairs. Bring the world idea you plan to use for the final bible.

1. (10 min) Write the sentence and three to five pillars. Swap with another pair. Each pillar must be one a reasonable designer could argue against. Rewrite any that fail.
2. (10 min) Fill in the density budget for your world. Choose `P`, `h`, `r` and a target `E`. Compute `A_needed` at peak, then `E` at a trough of your choice. Use the interactive to check your numbers and to decide whether you need copies.
3. (10 min) Apply the night-shift test and the sunset test to your partner's concept. Write one sentence each on what breaks.

Expected output: a card with the sentence, pillars, the density numbers (`P`, `h`, `r`, `E`, `A`, trough `E`, copies at peak) and the two test notes from your partners.

## Common misconceptions

- **"Bigger worlds are better worlds."** A bigger `A` with the same `P` lowers `E` in proportion. Past a point, extra space is extra emptiness. Size to the population you expect, then add space only where emptiness is the design.
- **"Subscriber numbers tell you how big to build."** Only concurrent players on one shard or copy share a space. A world with 100,000 subscribers might have 3,000 concurrent players per shard at peak and 750 at night.
- **"View distance is a graphics setting, not a design value."** It sets `r`, and `E` grows with `r²`. Changing it from 100 m to 200 m quadruples the number of players you see. In the section 2 world, `E` at peak goes from 1.8 to 7.1.
- **"Map copies fix density for free."** They move the problem from emptiness to recognition. Without placement rules that keep friends and guilds together, players stop meeting the same people twice.

## Check yourself

1. A world has `P = 5,000` concurrent players at peak, `h = 0.5`, `r = 120` m. How much field area gives `E = 5` at peak? At a trough of 20% of peak, what is `E`?
2. For the section 2 world (31.8 km², `h = 0.4`, `r = 150` m), the team adds fog that cuts `r` to 100 m in one region. What is `E` there at peak? What `r` would you need to make `E = 2` at the 3 a.m. trough without changing the map?
3. A Minecraft server keeps the default 20 players but lowers view distance to 6 chunks. With all 20 online and a target of four others in view, how wide can the shared build area be?
4. Using the copies rule with `E_max = 6`, a world sized for `E = 3` at trough has a peak-to-trough ratio of 5. How many copies are needed at peak, and what is `E` per copy?
5. A classmate's concept says "the world is huge, so explorers will love it" and gives `P = 800` for 50 km² with `r = 100` m and `h = 0.3`. Compute `E` at peak and write the one-sentence critique you would give.

<details>
<summary>Answers</summary>

1. View area `= π × 120² = 45,239 m²`. Field players `= 0.5 × 5,000 = 2,500`. `A = 2,500 × 45,239 / 5 ≈ 22.6 km²`. At 20% of peak, `E = 5 × 0.2 = 1.0`.
2. `E` scales with `r²`, so `E = 4 × (100/150)² = 1.78` at peak. At 3 a.m. with `r = 150` m, `E = 1.0`. To double `E`, multiply `r` by `√2`, so `r = 150 × 1.414 ≈ 212` m. A clearer, open landscape does the job without moving anyone.
3. View square side `= (2 × 6 + 1) × 16 = 208` blocks, area `43,264`. `A = 20 × 43,264 / 4 = 216,320` square blocks, a square about 465 blocks wide.
4. Peak `E` for one copy `= 3 × 5 = 15`. `n = ceil(15 / 6) = 3`. `E` per copy `= 5`.
5. View area `= 31,416 m²`. Field players `= 560`. `E = 560 × 31,416 / 50,000,000 ≈ 0.35`. One reasonable critique: "At peak the average player sees another person about one time in three, and at night almost never, so exploration will feel like a single-player game unless you shrink the field, merge shards or concentrate players along routes."

</details>

## Lab / assignment hook

[Lab 14, world concept and density budget](../labs/lab14.md). You write the one-page concept for your final world bible, with the seven commitments and a density budget spreadsheet, and get a structured peer critique. It is the first chapter of the world bible (40%) due in week 15.

## Sources

- Wikipedia, "EVE Online" (accessed September 2026). Record of 65,303 concurrent accounts on one server on 5 May 2013; more than 5,000 known-space systems plus about 2,500 wormhole systems, around 7,800 visitable in total; Tranquility single-universe server.
- Minecraft Wiki, "Server.properties" (Java Edition, accessed September 2026). Defaults `max-players=20`, `view-distance=10`, `simulation-distance=10`; view distance measured in chunks as a radius.
- Minecraft Wiki, "Chunk" (Java Edition, accessed September 2026). Chunks are 16 by 16 blocks horizontally.
- Guild Wars 2 Wiki, "Megaserver" (accessed September 2026). System completed 21 April 2014; placement by party, guild, language and home world.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Chapter 4, "Scope" (pp. 330-333) and "Geography" (pp. 357-366).
- The Tidewrack concept, the daily curve and every density parameter in sections 2 and 3 are invented for teaching.

## Interactive spec: examples/w14-density-budget.html

**The one insight.** A world sized for one hour of the day is wrong for the others. Expected players in view follows the daily population curve exactly, and only changing the number of map copies through the day keeps it in a comfortable band.

**Layout.** Two linked views side by side on desktop, stacked on mobile.

- Left, "What you see." A square top-down map of the field area `A` (drawn to scale as a square of side `√A`, labelled in km). Dots for field players placed uniformly at random from a fixed seed (seed 13) so the picture is stable. A circle of radius `r` at the centre is "you." Count and show the dots inside the circle next to the expected value `E`. When dynamic copies are on, show only the players of copy 1 (every n-th dot from the seeded list) and a label "copy 1 of n".
- Right, "Others in view over 24 hours." x-axis hour 0-24, y-axis `E` 0-20. Line for `E(hour)` with one copy. When copies are on, a second line for `E` per copy. Shaded bands: below 1 "lonely", above `E_max` "crowded". A vertical cursor at the selected hour, linked to the map.

**Model.**
```
share(hour) from the table below, linearly interpolated between listed hours, wrapping at 24
P(hour) = P_peak × share(hour)
field(hour) = (1 − h) × P(hour)
E1(hour) = field(hour) × π × r² / A
n(hour) = copies on ? ceil(E1(hour) / E_max) : 1
E(hour) = E1(hour) / n(hour)
A_needed(E_target) = (1 − h) × P_peak × share(hour_ref) × π × r² / E_target
```
Daily share table: 00:00 0.45, 03:00 0.25, 06:00 0.30, 09:00 0.45, 12:00 0.60, 15:00 0.70, 18:00 0.90, 21:00 1.00.

**Controls.**
- `P_peak` slider 100-20,000, default 3,000.
- `h` slider 0-0.9 step 0.05, default 0.4.
- `r` slider 20-400 m step 10, default 150.
- Area mode: "size for peak" or "size for trough" with target `E_target` slider 0.5-20 step 0.5, default 4; or "manual" with `A` in km² (0.1-200), default 31.8.
- Hour slider 0-24 step 1, default 21.
- Dynamic copies toggle (default off) with `E_max` slider 1-20, default 6.
- Readouts: `A` in km² and side length, `E` now, `E` min and max across the day, peak-to-trough ratio, copies at the selected hour.

**Test values.**
- Defaults, size for peak, `E_target = 4`: `A = 31.81 km²`, side 5.64 km; `E` at 21:00 = 4.00, at 03:00 = 1.00, at 12:00 = 2.40.
- Size for trough (03:00), `E_target = 4`: `A = 7.95 km²`; `E` at 21:00 = 16.0.
- Size for trough plus copies with `E_max = 6`: copies at 21:00 = 3 with `E = 5.33`; at 18:00 = 3 with `E = 4.8`; at 15:00 = 2 with `E = 5.6`; at 09:00 = 2 with `E = 3.6`; at 03:00 = 1 with `E = 4.0`.
- Defaults with `r = 100`: `E` at 21:00 = 1.78; with `r = 200`: 7.11.

**Accessibility and style.** All sliders keyboard operable; the hour cursor moves with arrow keys. Dots respect `prefers-reduced-motion` (no animated re-layout). Shared palette from `templates/interactive-tokens.css`. No game art. State on screen that all values are invented for teaching.
