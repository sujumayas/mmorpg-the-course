# MMO305 · Week 02 — Playing Alone Together

**Why this matters:** Your guild roster says 40 members, 12 online. Your players say they play "for the social side." Both statements can be true while almost nobody plays with anybody. If you measure sociability by counting who is online, you will design for a society that isn't there. This week gives you three ways to count togetherness from the same log, and shows why they disagree by a factor of five or more.

**You will be able to:**
- Distinguish co-presence, co-location and co-activity, and say which one a given feature or metric measures.
- Compute network density and a main core from census snapshots, by hand, for a small guild.
- Summarize the main quantitative findings of Ducheneaut, Yee, Nickell and Moore (2006) and explain the "alone together" interpretation.
- Critique a social feature by which layer of togetherness it creates, using WoW, Star Wars Galaxies, Guild Wars 2 and Journey as cases.

**Before class:** Nicolas Ducheneaut, Nicholas Yee, Eric Nickell and Robert J. Moore, "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games," *Proceedings of CHI 2006*, pp. 407-416. Read all ten pages, and study Table 1 and Figure 8. Reread Steinkuehler and Williams (2006) from week 1, sections on bridging and bonding.

**Prerequisites from earlier courses:** [MMO305 week 1, social capital](w01-mmos-as-societies-social-capital.md), for nodes, ties, bridging and bonding. [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md), for means, medians and why a single average hides the spread. [GS101 week 10, World of Warcraft and the mass-market MMO](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md), for the game the study measured. [MMO304 week 2, functional, hedonic and social value](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w02-functional-hedonic-and-social-value.md), for why items need an audience.

**Interactive:** [examples/w02-three-networks.html](../examples/w02-three-networks.html). Use it during section 3.

---

## 1. What players say, and what the census saw

Ask MMO players why they play an MMO instead of a single-player RPG and most will mention other people. Surveys and interviews from the early 2000s said the same. The "social factor" was the genre's selling point, and earlier studies of games like EverQuest emphasized time spent in groups.

In 2005 a team at the Palo Alto Research Center (PARC) and Stanford decided to stop asking and start counting. World of Warcraft had a built-in `/who` command that lists characters currently online, and its interface could be extended with add-ons. The team wrote software that took a census of whole servers every 5 to 15 minutes. Each observation recorded the server, date, character name, level, race, class, whether the character was in a group, the zone, and the guild. They ran it on five US servers (PvE, PvP and RP types) from June 2005 and observed 129,372 unique characters. This was the classic era, with a level cap of 60, parties of up to 5 and raids of up to 40.

What they found surprised the field.

- **Grouping was a minority activity.** Time spent in groups rose roughly linearly with level to about 40%, then climbed sharply after level 55. Only from level 59 did characters spend more than half their time in a group.
- **Solo play was faster.** Characters never seen in a group levelled about twice as fast as characters who grouped at any frequency.
- **Players chose soloable classes.** The class that grouped least (Warlocks, about 30% of time grouped) and the one that grouped most (Priests, about 40%) differed a lot. The three most played classes (Warrior, Hunter and Rogue) all grouped less than 32% of the time.
- **Guilds were common but small.** 66% of characters were in a guild. The median guild had 6 members (9 if one-person guilds are excluded), the mean was 14.5, and the largest had 257. 17.5% of characters were in a guild where nobody else was ever observed.
- **Guilds mattered anyway.** Between levels 41 and 60, guilded characters were in groups about 43% more often than unguilded ones, after controlling for playing time.
- **Guilds were sparse.** Inside guilds of 6 or more, players were online at the same time as about 1 in 4 of their guildmates, and in the same zone as about 1 in 10.

The authors' reading of this is where the title comes from. Most WoW players, most of the time, are not playing *with* other people. They are playing *among* them. One player the team interviewed described the population as "alone together." The rest of this lecture turns that phrase into three numbers you can compute.

## 2. Three layers of togetherness

Two players can be "together" in three different senses. Each is a different network drawn from the same log.

- **Co-presence.** Both are online at the same time. They could talk in guild chat and they see each other's names in the roster. This is the weakest layer. Ducheneaut and colleagues call these ties weak or bridging.
- **Co-location.** Both are in the same zone at the same time. The study excluded major cities, because cities hold everyone and say little about shared play. Co-location suggests shared activity, and the authors treat these ties as the stronger, bonding kind.
- **Co-activity.** Both are in the same group at the same time. This is the strongest evidence that they are actually playing together.

Each layer is a subset of the one above it. Every grouped pair is co-located. Every co-located pair is co-present. So the networks shrink as you go down, and the question is how fast.

The number we use to compare them is **network density**, the share of possible ties that actually exist.

```
D = L / P
P = n × (n − 1) / 2
```

- `n` is the number of members in the group being studied.
- `L` is the number of pairs that have a tie in this layer.
- `P` is the number of possible pairs.

Density runs from 0 (nobody is tied) to 1 (everyone is tied to everyone). A guild whose co-presence density is 0.27 is one where the average pair of members overlaps online at some point. A guild whose co-location density is 0.09 is one where fewer than 1 pair in 10 was ever seen in the same place.

We also need a way to find the tight group inside a sparse network. A **k-core** is the largest set of members in which every member has ties to at least `k` others *inside the set*. You find it by repeatedly deleting anyone with fewer than `k` ties and recounting. The **main core** is the k-core with the largest `k` that is not empty. In Ducheneaut's data the main core is the guild's real play group.

## 3. Worked example: the guild that looks full

### The hook

A guild leader looks at the roster at 19:30 on a Tuesday. Seven of eight members are online. Guild chat is lively. It feels like a busy, social guild. Is it?

### The model

Take census snapshots. For each pair of members, record a tie in each layer if the pair meets the layer's condition in at least one snapshot. Then compute the three densities, the share of online time spent grouped, and the main core of the co-location network.

```
co-presence tie:  both online in the same snapshot
co-location tie:  both in the same zone (not a city) in the same snapshot
co-activity tie:  both grouped, in the same zone, in the same snapshot

D_layer = L_layer / (n(n − 1)/2)
grouped share = grouped member-snapshots / online member-snapshots
```

The paper weighted ties by how long pairs overlapped. We use "at least one snapshot" so you can check everything by hand. The lab uses a threshold instead.

### Numbers you can check

Here is an invented census of an eight-member guild over one evening, one snapshot every 15 minutes. A blank cell means offline. An asterisk means the member was in a group.

| Member | 19:00 | 19:15 | 19:30 | 19:45 | 20:00 | 20:15 |
|---|---|---|---|---|---|---|
| Ash | Marsh | Marsh | Marsh | Ridge | Ridge | |
| Bryn | City | Crypt* | Crypt* | Crypt* | City | |
| Cato | | Crypt* | Crypt* | Crypt* | | |
| Dara | Ridge | Ridge | City | Fen | Fen | Fen |
| Eli | | | Fen | Fen | City | City |
| Fenn | City | City | City | City | City | City |
| Gus | Marsh | Marsh | | | | |
| Hal | | Crypt* | Crypt* | Crypt* | | |
| **Online** | **5** | **7** | **7** | **7** | **5** | **3** |

There are `n = 8` members, so `P = 8 × 7 / 2 = 28` possible pairs.

**Co-presence.** Find the pairs who are never online together. Gus is online only at 19:00 and 19:15. Eli is online only from 19:30. They never overlap. Every other pair overlaps at least once. So `L = 27` and `D = 27 / 28 = 0.96`.

**Co-location.** Now look for pairs in the same non-city zone at the same time.
- Bryn, Cato and Hal share the Crypt from 19:15 to 19:45. That gives three pairs.
- Ash and Gus share the Marsh at 19:00 and 19:15.
- Dara and Eli share the Fen at 19:45.
- Ash and Dara are both in the Ridge, but never at the same time.
- Fenn is only ever in the City, which does not count.

So `L = 5` and `D = 5 / 28 = 0.18`.

**Co-activity.** Only Bryn, Cato and Hal were ever grouped, together, so `L = 3` and `D = 3 / 28 = 0.11`.

| Layer | Ties | Density | What it means |
|---|---|---|---|
| Co-presence | 27 | 0.96 | Almost every pair could have chatted |
| Co-location | 5 | 0.18 | Fewer than 1 pair in 5 was ever in the same place |
| Co-activity | 3 | 0.11 | Three people played together; that is the whole group play |

**Grouped share.** Add up the online column totals: `5 + 7 + 7 + 7 + 5 + 3 = 34` member-snapshots online. Grouped member-snapshots are Bryn, Cato and Hal at three snapshots each, `9`. So the guild spent `9 / 34 = 26%` of its online time grouped. That is close to what the census found at low and middle levels.

**Main core.** In the co-location network, Bryn, Cato and Hal each have 2 ties, to each other. Ash, Gus, Dara and Eli have 1 tie each. Fenn has none. Delete everyone with fewer than 2 ties and the trio remains, still with 2 ties each. So the main core is the 2-core {Bryn, Cato, Hal}, 3 of 8 members, or 37.5%.

**Alone together, literally.** Ash and Gus spent two snapshots in the same zone without grouping. Dara and Eli did the same once. Those are six member-snapshots of players sharing a place, probably seeing each other, and not playing together.

The roster said "busy guild." The census says one trio plays together, four members sometimes share a zone, and one member stands in the city all evening.

### The visual

Open the interactive. The top strip is the roster's view, a bar per snapshot showing how many members were online. Underneath, the same eight members are drawn three times, once per layer, with the density printed under each. The co-presence network is a nearly complete web. The co-activity network is a single triangle. Click any cell in the census grid to change a member's zone or group status and watch all three networks update. Try to raise co-activity density above 0.5 and notice how many cells you have to change.

### Cross-game recognition

Every social design fills one of these three layers. Recognizing which one is the skill.

**World of Warcraft (classic era, 2005, the study itself).** At scale, the census found exactly this pattern. For guilds of 6 or more, mean co-presence density was 0.27 and mean co-location density was 0.09. Both fell as guilds grew. For guilds of more than 120 members, co-location density averaged 0.04. The main core shrank from about 37% of a small guild to about 12% of a large one, and core members spent about 154 minutes playing together over 30 days against 22.8 minutes for the average pair of guildmates. The paper's Figure 8 shows a real guild of 41 in which 17 members were never in the same zone as any guildmate. Our eight-member guild is a small copy of that figure.

The paper also names a design choice that raised co-presence for everyone. WoW's chat channels were not limited by distance. Each zone had a general channel, and guild chat reached across the whole world. Few people talked, but everyone could hear background chatter. The authors compare it to reading a book in a busy café, and argue that this sense of social presence is part of why WoW did not feel like a single-player game.

**Star Wars Galaxies (2003 to 2005, before the New Game Enhancements).** SWG filled the co-location layer by design. Entertainers danced and played music in cantinas. Players who watched or listened received an inspiration buff at the end of the performance (a bonus to combat experience, faction points and crafting success), and entertainers earned experience from having an audience. Entertainer skills also included wound healing through music and dance. So the game gave combat players a reason to stand in the same room as other players without grouping with them. In the model, this is a feature that raises co-location density and gives the entertainer a large audience, while co-activity stays low. It is "alone together" turned into a system. Ducheneaut and Moore studied these cantinas in a 2004 paper.

**Guild Wars 2 (2012 onward, current era).** Dynamic events turn co-location into co-activity without a group. Every player who participates in an event receives full experience and has loot rolled for them as if they were the only participant, and the event scales its difficulty with the number of participants. In older MMOs, the first player to hit a monster usually got the kill, so a second player in the same zone was a competitor. In GW2 that same stranger is a helper. In the model, GW2 changed the rule that decides whether a co-located pair counts as co-active. The formal group is no longer needed.

**Journey (thatgamecompany, 2012).** Journey removes every layer except the thinnest form of co-activity. Two players can meet in the desert and help each other, but they cannot speak or type, and they cannot see each other's names until the credits. The only signal is a musical chime. In the model, co-presence and co-location are hidden from the player, and a tie is co-activity with no identity attached. It shows that shared activity can feel social even when it cannot become a lasting tie, because the player can never find that partner again.

Four games, one model. Ask of any social feature, "which layer does it fill, co-presence, co-location or co-activity, and does it let a tie in that layer repeat?"

### Eyes-open design judgment

- **Co-presence is cheap and valuable.** World-wide chat, rosters and busy hubs give players the feeling of being among others at almost no cost. The census shows this may be most of what players experience as "the social factor." Do not dismiss it because it is not grouping.
- **Co-presence metrics flatter you.** "Guild members online together" and "concurrent players" measure the weakest layer. If your social health dashboard uses only co-presence, it will show 0.96 when real play density is 0.11. Instrument co-location and co-activity too. This is a telemetry request you will make to your data team (DB201 covers event design).
- **Co-activity is expensive for the player.** The census found solo play about twice as fast for levelling. If grouping costs players progress, they will solo, however much they like other people. Next week asks what happens when you force it.
- **Audiences are a design space.** Ducheneaut and colleagues argue that other players act as an audience, a source of social presence, and a spectacle. SWG's entertainers and every raid mount parked outside a bank are designs for the audience role. Week 7 builds on this.
- **Big guilds are sparse by nature.** Density fell with size in the census. That is expected. One player can only play with a handful of others at once, so as `n` grows, `L` grows more slowly than `n²`. A large guild is not failing because its density is low. It is failing if its main core is too small to run its content.

## 4. Why players solo

The census numbers explain a lot of solo play without any appeal to personality. Three costs push players out of groups.

**Formation cost.** A group needs the right number of people, at the same level, in the same place, with complementary classes, at the same time. Each condition shrinks the pool. Time spent assembling a group is time not spent playing.

**Coordination cost.** A group moves at the speed of its slowest member and stops when anyone needs a break. Loot must be shared. Experience per kill is split.

**Scheduling cost.** A solo player can play for 20 minutes and log off. A group player has to commit. Guild members' play time in the census was more regular after level 40, and the authors link that to guild events that require several hours.

Against those costs, the game offered a reward rate that was about twice as high for solo levelling. A rational player who wants progress solos until the content forces them not to. That is exactly what the census saw. Grouping stayed below 40% until the level-55-plus content, which was designed for groups, forced it up.

None of this means players are antisocial. It means that when grouping is optional and costly, players choose co-presence, which is free, over co-activity, which is not. Week 3 asks how to make grouping cheaper, and what forcing it does to the ties that follow.

## 5. Designing for people who play alone

If most of your players spend most of their time alone together, you have two design jobs, not one.

**Make being among others better.** Hubs where players pass each other and see each other's achievements. Chat that reaches far enough to create background life. Spectacle, such as world events many players watch at once. Ways to help a stranger in one click without forming a group. Visible traces of other players (player-built houses, names on a leaderboard, a message left on the ground). These all raise co-presence and co-location and ask nothing of a solo player.

**Make it easy to step up a layer.** A stranger you helped in a public event should be one click away from a friend request. A guildmate in the same zone should be visible on the map. The step from co-location to co-activity should be short and cheap, so that the players who want to play together can find each other when they want to. Week 11 (newcomers and mentoring) and week 14 (positive social play) come back to this.

A useful rule of thumb from this week is to design for the density you have, not the one on the roster. If co-activity density in a typical guild is 0.1, design guild features for a trio that plays together and a periphery that watches, not for a 40-person village.

## In-class activity (25 minutes)

Pairs. Materials: the census table in section 3 printed on paper, the interactive, and one laptop.

1. (5 min) Redraw the three networks on paper. Label every tie with the snapshot(s) that created it.
2. (8 min) You may change exactly **four cells** of the census (a zone name, an online or offline mark, or an asterisk). Your goal is the highest co-activity density you can reach. Record your four changes and your new density.
3. (7 min) Translate each of your four changes into a design feature that would make that change happen in a real game. For example, "Gus stays online later" might be "a weekly event at 20:00 with a guild bonus."
4. (5 min) Compare with another pair. Whose features would a solo player resent?

Expected output: four cell changes, the new co-activity density (the best possible with four changes is worth finding), four features, and one note about solo players.

## Common misconceptions

- **"Players who solo don't want social play."** The census found grouping was slower for levelling and guilds still raised grouping by 43%. Players respond to costs. Many who solo value co-presence highly.
- **"A full roster means a healthy guild."** A roster measures co-presence at best. Check co-location and co-activity, and find the main core.
- **"Low density means the guild is failing."** Density falls with size in every social network, because each person can only sustain a few active ties. Judge a guild by whether its core can run its content.
- **"The 2006 census shows modern WoW."** It measured the classic era in 2005, before cross-realm group finding. Its method still applies, and its numbers describe that era only.

## Check yourself

1. A guild of 12 members has 30 co-location ties. What is its co-location density? Compare it with the census mean for guilds of 6 to 15 members (0.12).
2. In the section 3 census, suppose Gus stays online in the Marsh until 19:30. Which layers gain ties, and what are the new densities?
3. In the section 3 census, Fenn joins Bryn's group in the Crypt at 19:45. What happens to co-activity density and to the main core of the co-location network?
4. A designer adds a feature that pays a small bonus to everyone who stands within 30 meters of a guildmate. Which layer does this raise? Would you expect co-activity to follow? Use Star Wars Galaxies to support your answer.
5. Ducheneaut and colleagues found guilds of more than 120 had co-location density 0.04. Roughly how many co-location ties does a member of a 150-member guild have, on average?

<details>
<summary>Answers</summary>

1. `P = 12 × 11 / 2 = 66`, so `D = 30 / 66 = 0.45`. That is almost four times the census mean for guilds this size, a much more tightly knit guild than typical classic-era WoW.
2. Gus is now online at 19:30, when Eli is online, so Eli and Gus become co-present. Co-presence goes to `28 / 28 = 1.00`. At 19:30 Ash is also in the Marsh, but Ash and Gus already had a co-location tie, so co-location stays at 5 ties (0.18). Co-activity is unchanged at 0.11.
3. Fenn gains co-location and co-activity ties to Bryn, Cato and Hal. Co-location rises to 8 ties (0.29) and co-activity to 6 ties, `6 / 28 = 0.21`. In the co-location network, Bryn, Cato, Hal and Fenn now each have 3 ties to each other, so the main core becomes the 3-core {Bryn, Cato, Hal, Fenn}, 4 of 8 members (50%).
4. It raises co-location, and probably co-presence in hubs. Co-activity need not follow. SWG's cantinas filled rooms with players who received a buff from an entertainer without grouping or even talking to one another. A proximity bonus gives a reason to stand near someone, not to play with them. If you want co-activity, the reward has to depend on doing something together.
5. Each member has `D × (n − 1) = 0.04 × 149 ≈ 6` co-location ties on average, out of 149 guildmates.

</details>

## Lab / assignment hook

[Lab 02, three networks from one census](../labs/lab02.md). You will take a 20-member guild's census over 16 snapshots, compute the three densities and the main core, find the members who are alone together, and propose two features, each aimed at one specific layer. This lab is also practice for the field observation (30% of the grade), where you will collect a census of your own.

## Sources

- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI 2006)*, ACM, 407-416. https://doi.org/10.1145/1124772.1124834. Census method (`/who`, every 5 to 15 minutes, five servers, from June 2005, 129,372 characters); grouping by level and class; solo levelling about twice as fast; 66% guilded; guild size mean 14.5, median 6 (9 without one-person guilds), largest 257; 17.5% in one-person guilds; 43% more grouping for guilded characters at levels 41-60; Table 1 densities (co-presence 0.27, co-location 0.09 for guilds of 6 or more; 0.12 co-location for 6-15; 0.04 for more than 120); main core ratio from 37% to 12%; 154 versus 22.8 minutes; the 41-member guild with 17 isolates; chat channels and social presence; audience, presence and spectacle. Classic era World of Warcraft (level cap 60, parties of 5, raids of 40).
- Ducheneaut, N. & Moore, R. J. (2004). "The Social Side of Gaming: A Study of Interaction Patterns in a Massively Multiplayer Online Game." *Proceedings of CSCW 2004*, ACM, 360-369. Study of Star Wars Galaxies cantinas.
- Star Wars Galaxies Wiki (fandom), "Entertainer (pre-NGE)". Inspiration buff for audience members (10% bonus to combat experience, faction points and crafting success); entertainer experience from players watching or listening; wound-healing skill modifiers for music and dancing. Era: launch (June 2003) to the New Game Enhancements (November 2005). https://swg.fandom.com/wiki/Entertainer_(pre-NGE)
- Wikipedia, "Star Wars Galaxies". Release date June 26, 2003 (North America); New Game Enhancements reduced professions in November 2005.
- Guild Wars 2 Wiki, "Dynamic event" (current era). Every participant receives full experience without a party; loot calculated per participant as if they were the only one; difficulty scales with participants; contrasted with first-tag rules in older MMOs. https://wiki.guildwars2.com/wiki/Dynamic_event
- Wikipedia, "Journey (2012 video game)". Released March 2012 on PlayStation 3; players can meet and assist each other but cannot communicate by speech or text or see names until the credits; the only communication is a musical chime.
- Steinkuehler, C. A. & Williams, D. (2006). "Where Everybody Knows Your (Screen) Name." *Journal of Computer-Mediated Communication* 11(4), 885-909.
- The census table in section 3 is invented for this lecture. Its densities, grouped share and main core are computed from it and can be checked by hand.

## Interactive spec: examples/w02-three-networks.html

**The one insight.** The same census gives three networks. The roster view (who is online) looks busy and nearly complete, while the network of who actually played together is a single triangle. Densities 0.96, 0.18 and 0.11 from the same eight people.

**Data model.** A grid of 8 members (rows: Ash, Bryn, Cato, Dara, Eli, Fenn, Gus, Hal) by 6 snapshots (19:00 to 20:15 every 15 minutes). Each cell has a state: offline, or a zone from {City, Marsh, Ridge, Fen, Crypt}, plus a grouped flag. The default grid is exactly the lecture's table.

```
pairs P = n(n − 1)/2
co-presence tie (a,b): exists t with a online and b online
co-location tie (a,b): exists t with zone_a = zone_b ≠ City, both online
co-activity tie (a,b): exists t with both grouped and zone_a = zone_b (City allowed only if both grouped)
density = ties / P
grouped share = grouped member-snapshots / online member-snapshots
main core: repeat { remove nodes with degree < k in the co-location network } for increasing k; report the largest k with a non-empty set, and its members
alone-together count: member-snapshots in a non-city zone, not grouped, with at least one other online member in the same zone
```

**Layout.**
- **Top, "What the roster shows."** A bar per snapshot with the online count. The default shows 5, 7, 7, 7, 5, 3.
- **Middle, the census grid.** Editable. Clicking a cell (or Enter on a focused cell) cycles: offline, City, Marsh, Ridge, Fen, Crypt. A separate "grouped" toggle per cell (Shift+click or the G key). Grouped cells show an asterisk as well as a fill.
- **Bottom, three networks side by side (stacked on mobile).** The same 8 node positions in each (a circle). Titles "Online together", "Same place", "Played together". Under each, "ties L of 28, density D" (2 decimals). The co-location view marks main-core members with a ring and prints "main core: k = 2, {Bryn, Cato, Hal}, 37.5%".
- **Readout.** Grouped share, alone-together count.

**Controls.** Grid editing as above; "Reset to lecture census"; "Random evening" (seeded, seed shown, reproducible) for exploration.

**Test values (default grid, must match).** Co-presence 27 of 28, 0.96; the missing pair is Eli-Gus. Co-location 5 of 28, 0.18: Ash-Gus, Bryn-Cato, Bryn-Hal, Cato-Hal, Dara-Eli. Co-activity 3 of 28, 0.11. Online member-snapshots 34; grouped 9; grouped share 26%. Main core k = 2, {Bryn, Cato, Hal}, 37.5%. Alone-together count 6.

**Check-yourself values.** Gus online in Marsh at 19:30 (ungrouped): co-presence 28 of 28, 1.00; co-location 5; co-activity 3. Fenn in Crypt, grouped, at 19:45: co-location 8 of 28, 0.29; co-activity 6 of 28, 0.21; main core k = 3, {Bryn, Cato, Fenn, Hal}, 50%.

**Accessibility.** Ties differ by line style per layer as well as color. Grid cells are buttons with labels such as "Bryn, 19:15, Crypt, grouped." Network readouts in an `aria-live="polite"` region. Respect `prefers-reduced-motion` and `prefers-color-scheme`.
