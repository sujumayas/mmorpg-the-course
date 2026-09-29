# MMO407 · Week 11 — Shutdowns and emulation communities

**Why this matters:** When an MMO shuts down, the players keep the client and lose the server. Whether their world comes back in months, in fifteen years or never depends on what left the building on the last day: code, data, documents, or only the memories and packet logs players gathered on their own. This week you learn to estimate how long a fan rebuild takes, why the evidence left behind matters more than the number of volunteers, and what a studio can hand over when it closes a world.

**You will be able to:**
- Compute the volunteer-hours and years a from-scratch emulator needs, from the number of server behaviours, the share with evidence and the team's weekly hours.
- Explain, with the model, why the last unrecorded share of a game takes as long to rebuild as everything before it, and why a source release changes the timeline by an order of magnitude.
- Classify a real revival (Star Wars Galaxies, City of Heroes, Asheron's Call, Meridian 59, Ryzom) by the evidence it started from, and predict its timeline.
- Design a preservation package and a capture window for a shutdown, and name the legal, licensing and privacy work each item needs.

**Before class:** Read MMO301 week 13, sections 3 and 4 (the case files and the five questions of a sunset plan); they are not repeated here. Read the "Emulation" and "Source code leak" sections of the Wikipedia article "Star Wars Galaxies" and the README of the ACEmulator project on GitHub (about 20 minutes together).

**Prerequisites from earlier courses:** [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (why worlds close, the sunset plan, Stop Killing Games). [MMO308 week 14, sunsetting content and servers](../../MMO308-live-operations-analytics-and-experimentation/lectures/w14-sunsetting-content-and-servers.md) (when to close and the notice period). [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (the messages a client and server exchange). [DB201 week 13, privacy and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (what you may not hand over). [MMO404 week 13, cost engineering](../../MMO404-advanced-networked-simulation/lectures/w13-cost-engineering.md) (what a player-hour costs a volunteer host). [Week 10 of this course](w10-recovery-strategies.md) (the three stocks of a recovery).

**Interactive:** [examples/w11-rebuild-clock.html](../examples/w11-rebuild-clock.html). Keep it open during section 2.

---

## 1. What a shutdown takes away

An MMO is two programs. The **client** runs on the player's machine. It draws the world, plays the sounds and sends the player's inputs. The **server** runs in the studio's data centre. It decides what happens: whether the sword hit, what the monster dropped, what the quest giver says next, how much the auction house charges. MMO302 taught you why the server must be the authority on all of that. The same design choice decides what happens on the last day.

When the servers go dark, players still have the client files on their disks. What vanishes is everything the server knew and did.

| Lost with the server | Examples | Can players see it from outside? |
|---|---|---|
| Rules | damage formulas, crafting results, AI decisions | partly, by testing and measuring |
| Content data | spawn points, loot tables, quest scripts, NPC dialogue trees | only the parts a player triggered |
| Messages | the network protocol, the exact bytes of each message type | yes, if someone recorded them |
| State | every character, item, house and guild | only a player's own view |

A **server emulator** is a new server program, written by people outside the studio, that talks to the original client well enough that the client cannot tell the difference. The community that builds and runs one is an **emulation community**. Some rebuild the last version of the game. Many rebuild a particular past version they loved, which the studio itself no longer offers. [Week 7 of this course](w07-classic-and-legacy-servers.md) looks at the studios' own answer to that wish, official classic servers. This week is about what fans can do without the studio, and what the studio can do on the way out to help or hinder them.

The column on the right is the key to the whole week. An emulator can only copy what someone saw. Whatever no one recorded must be guessed, and guessing is slow.

## 2. Worked example: the rebuild clock

### The hook

Star Wars Galaxies shut down on 15 December 2011. Seven years earlier, in 2004, fans had founded SWGEmu to rebuild the game as it was before the 2005 Combat Upgrade, from scratch, with no code from the studio. In 2020, sixteen years after it started, the project announced it was near completion of its base game, and said one large system, the Jump to Lightspeed space expansion, might not make it into version 1.0 because it was too complex.

City of Heroes shut down on 30 November 2012. On 15 April 2019 news broke that a private server built from the game's own server code had been running in secret for years. Three days later the code was widely distributed, and a public server based on it went up almost at once. Several more followed.

Here is the puzzle. Both were large MMOs with devoted fans. One revival took sixteen years to get near the finish line. The other went from "we have the code" to public servers in days. The difference is not the fans' talent or number. It is what they started with.

### The model

Name the numbers.

- `B` is the number of server behaviours the emulator must reproduce. A **behaviour** here is one unit of server work a player can notice: one message type handled, one quest script, one monster's AI, one crafting recipe. Real games have thousands.
- `q` is the share of behaviours for which the team has **evidence**: recorded network traffic, documentation, datamined client files, wiki pages written from careful testing. It runs from 0 to 1.
- `w` is the volunteer-hours to rebuild one behaviour when you have evidence.
- `g` is the guesswork multiplier. A behaviour without evidence takes `g` times as long, because the team must invent a version, test it against players' memories, argue, and redo it.
- `V` is the team's volunteer-hours per week.
- `w_s` is the hours per behaviour when the original server source is available, spent porting, fixing and configuring rather than rebuilding.

```
hours needed      H = B × w × (q + g × (1 − q))
weeks to rebuild  T = H / V
faithful part done at   t_q = B × q × w / V         (evidence-backed behaviours first)
with source       T_s = B × w_s / V
```

Read the first line carefully. Each behaviour with evidence costs `w`. Each one without costs `g × w`. So the bracket `q + g × (1 − q)` is the cost of the game relative to a perfectly documented one. At `q = 1` it is 1. At `q = 0` it is `g`.

Two consequences follow.

1. **Missing evidence is expensive at the margin.** Every 10 points of `q` you lose adds `0.1 × B × w × (g − 1) / V` weeks. With `g = 4`, each missing behaviour costs three extra behaviours' worth of work.
2. **Progress slows sharply at `q`.** A sensible team rebuilds the evidence-backed behaviours first. So the completeness curve climbs at `V / w` behaviours a week until it reaches `q`, then slows to `V / (g × w)`. On a chart this is a kink. The kink sits exactly at the share of the game somebody recorded.

The source term is separate. With the server code in hand, a team is no longer rebuilding behaviours. It is running them. `w_s` is a small fraction of `w`, and the timeline shrinks by the same factor.

### Numbers you can check

Take an invented mid-sized MMO with `B = 1,500` behaviours. With evidence, each takes `w = 60` volunteer-hours (read the captures, write the handler, write tests, compare with footage). Without evidence, `g = 4`. The team has 25 volunteers at 8 hours a week, so `V = 200` hours a week. With the source, `w_s = 3` hours a behaviour.

| Evidence `q` | Hours `H` | Faithful part done (years) | All done (years) |
|---|---|---|---|
| 100% | 90,000 | 8.7 | 8.7 |
| 90% | 117,000 | 7.8 | 11.2 |
| 80% | 144,000 | 6.9 | 13.8 |
| 60% | 198,000 | 5.2 | 19.0 |
| 40% | 252,000 | 3.5 | 24.2 |
| Source released | 4,500 | — | 0.4 |

Check the 80% row by hand. The bracket is `0.8 + 4 × 0.2 = 1.6`, so `H = 1,500 × 60 × 1.6 = 144,000` hours. At 200 hours a week that is 720 weeks, 13.8 years. The faithful part is `1,500 × 0.8 × 60 / 200 = 360` weeks, 6.9 years. So the last 20% of the game takes exactly as long as the first 80%. With `g = 4` that always happens at `q = 0.8`, because `g × (1 − q) = q` there.

Now the source row. `1,500 × 3 / 200 = 22.5` weeks, under half a year. Compared with a perfectly documented from-scratch rebuild, that is `w / w_s = 20` times faster.

This script prints the table:

```python
BEHAVIOURS = 1_500   # server behaviours the emulator must reproduce
HOURS_SEEN = 60      # volunteer-hours per behaviour with evidence (captures, docs)
GUESS = 4            # hours multiply by this when there is no evidence
PER_WEEK = 200       # volunteer-hours per week (25 people x 8 hours)
HOURS_PORT = 3       # hours per behaviour when the server source is released

def rebuild_weeks(q):
    """Evidence-backed behaviours first, then the guessed ones at GUESS times the cost."""
    seen = BEHAVIOURS * q * HOURS_SEEN / PER_WEEK
    guessed = BEHAVIOURS * (1 - q) * HOURS_SEEN * GUESS / PER_WEEK
    return seen, seen + guessed

for q in (1.0, 0.9, 0.8, 0.6, 0.4):
    seen, total = rebuild_weeks(q)
    print(f"evidence {q:4.0%}  faithful part done {seen / 52:4.1f} y  all done {total / 52:4.1f} y")
print(f"source released        all done {BEHAVIOURS * HOURS_PORT / PER_WEEK / 52:4.1f} y")
```

It prints:

```
evidence 100%  faithful part done  8.7 y  all done  8.7 y
evidence  90%  faithful part done  7.8 y  all done 11.2 y
evidence  80%  faithful part done  6.9 y  all done 13.8 y
evidence  60%  faithful part done  5.2 y  all done 19.0 y
evidence  40%  faithful part done  3.5 y  all done 24.2 y
source released        all done  0.4 y
```

Notice what the table says about recruiting. Doubling the team to 50 volunteers halves every number, so an 80% game drops to 6.9 years. Raising `q` from 80% to 100% before the servers close does about the same, with no new volunteers at all. And the servers only run once. After the last day, `q` is frozen forever.

### Move it yourself

Open the interactive. The left view plots the share of the game rebuilt against years. Each curve climbs steeply and then bends at a kink. Drag the evidence slider `q` down from 100% to 40%. The kink slides down and to the left, and the tail after it stretches across the chart. The right view plots total years against `q` for the current team size, with a flat line for the source-release timeline near the bottom. Drag the volunteer slider. Both curves scale together, but the gap between "from scratch" and "source released" never closes. The one thing that moves a curve onto the flat line is the source.

### Cross-game recognition

Every revival you will read about sits somewhere on this chart. Rewrite each as the model's inputs.

**Star Wars Galaxies (SWGEmu from 2004; source leak 2013).** SWGEmu is the from-scratch case, a large `B` with evidence gathered by players, and the model predicts a timeline of well over a decade. Sixteen years to near-completion fits, and the unfinished space expansion is a large block of behaviours with thin evidence and high `g`. Galaxies also shows the other regime. In 2013 a former SOE employee leaked the 2010 server and client source to a few players behind Project SWG, a second emulator aimed at the later version of the game, and the code later spread further. With source, the question stops being "how do we rebuild it" and becomes "may we run it." That is a legal question, not an engineering one.

**City of Heroes (servers off November 2012; code public April 2019; licence January 2024).** The source regime. Once the code spread in April 2019, a public server ran within days, which is the `T_s` row. On 4 January 2024 NCSoft granted Homecoming Servers LLC a licence to host the game. MMO301 week 13 covers the story. Here, note that seven years passed before the code appeared, and after that it took days to run.

**Asheron's Call (servers off 31 January 2017).** This is the capture-window case, and it shows `q` being set in real time. The ACEmulator project's GitHub repository was created on 16 January 2017, fifteen days before the servers closed. Its organisation also hosts aclog, an automatic network packet capture tool for the game, and repositories of packet-capture data built for use as the emulator's world database. The project describes its server as completely from scratch. Its base world database is labelled as content from February 2005, and work on later content is listed as ongoing. In the model, the players who recorded their sessions in the final weeks were raising `q` while it could still be raised. The eras with fewer recordings are the slow tail.

**Meridian 59 (closed by 3DO in 2000; source released in 2012).** Shortly after 3DO shut the game on 31 August 2000, a developer leaked the server software to a player, and free community servers have run ever since. The original technical developers, Andrew and Chris Kirmse, later took the game back and on 15 September 2012 released it as freeware with most of the source under GPLv2. Meridian 59 went through the source regime twice, once unofficially and once by choice.

**Ryzom (source released while running, 2010).** On 6 May 2010, the game's operator released the full source, client and server, under the AGPL, and the artwork under a Creative Commons licence, while the game was still running. In the model, this sets `w_s` for any future community on day one, before any shutdown. It is the only case here where nobody had to leak, capture or guess anything.

Five games, one chart. When you hear about a fan revival, ask two questions first. What evidence did they start from? And did the source ever leave the building?

### Eyes-open design judgment

- **The studio controls `q` and `w_s`. The fans control `V`.** Volunteers can only add hours. The studio decides what evidence exists and whether the source ever leaves. If your team cares whether its world survives, those are your levers, and you have them only until the last day.
- **A source release is cheap in engineering and expensive in paperwork.** The code may include licensed middleware you may not redistribute. The world may belong to a licensor (Galaxies was a Star Wars licence). The code may contain security secrets, and the databases hold personal data you must not hand over (DB201 week 13). Budget the legal work, and start it while the team that knows the code still exists. MMO301 week 13 showed with WildStar what happens when the studio closes first.
- **A capture window is nearly free.** If a full release is impossible, you can still raise `q`. Say publicly that recording your own network traffic during the notice period will not be treated as cheating, keep old content reachable until the end, and publish static data (item lists, quest text, drop tables) before closing. None of it needs a licence to your code.
- **Emulators freeze a version, and that is often the point.** SWGEmu chose a 2005 version on purpose. Players rebuild the rules they miss, not the last patch. If your studio will not offer that version, someone else may, with or without your blessing.
- **An unlicensed revival has costs for everyone.** Fans who host without a licence risk takedowns and cannot take money openly. The studio loses control of its brand and its players' safety. A licence, as with Homecoming, turns that into a relationship with rules. Decide in the sunset plan which outcome you want.

### Check this example

1. With the section 2 values, what is `T` at `q = 70%`? When is the faithful part done?
2. A team of 40 volunteers at 6 hours a week rebuilds a game with `B = 2,400`, `w = 50`, `g = 5` and `q = 0.9`. How many years?
3. For the section 2 values, at what `q` does the guessed tail take as long as the faithful part? Explain why the answer does not depend on `B`, `w` or `V`.

<details>
<summary>Answers</summary>

1. Bracket `0.7 + 4 × 0.3 = 1.9`. `H = 1,500 × 60 × 1.9 = 171,000` hours, 855 weeks, 16.4 years. Faithful part `1,500 × 0.7 × 60 / 200 = 315` weeks, 6.1 years.
2. `V = 240`. Bracket `0.9 + 5 × 0.1 = 1.4`. `H = 2,400 × 50 × 1.4 = 168,000` hours, 700 weeks, about 13.5 years.
3. Set `q = g × (1 − q)`, so `q = g / (1 + g) = 0.8`. Both sides share the factor `B × w / V`, which cancels.

</details>

## 3. What a studio can hand over

MMO301 week 13 gave five questions for a sunset plan, and MMO308 week 14 showed how to pick the date and the notice period. The fifth question, preservation, is where this week's model applies. Here is a menu of what a studio can leave behind, ordered by how far each moves a revival along the chart.

| Handover | Moves | Main work before release |
|---|---|---|
| Nothing, and enforce against private servers | nothing | none, but expect leaks and conflict |
| Capture window and public data dumps | `q` up | a statement to players; export scripts |
| Protocol and data documentation | `q` up, `w` down | engineers' time to write it |
| Server binaries with a hosting licence | `w_s`, and makes hosting legal | licence terms; strip secrets |
| Full source under an open licence | `w_s`, and allows forks | audit third-party code; licensor consent |
| Official community hosting licence (after the fact) | makes an existing revival legal | contract, brand rules, revenue terms |

Three questions decide which row you can reach.

1. **Who owns what?** The game's code, the art, the world and its characters, and each middleware library may each have a different owner. A licensed world needs the licensor's consent for anything past the first two rows.
2. **What is in the database?** Character names, chat logs, emails and payment references are personal data. A world export for fans must be built from content tables only. Never from a backup.
3. **Who will be left to do it?** Every row past the second needs engineers who know the code. Plan it in the months before the announcement, not the week after the studio closes.

The last row deserves a note. A studio that refuses every option is not choosing "no revival." On this week's evidence it is choosing an unlicensed revival, years later, with no say in how its world is run. Players of Meridian 59, Star Wars Galaxies and City of Heroes all got their code eventually, through leaks. The only question the studio answered was whether it would be involved.

## 4. Running a revived world

An emulation community that succeeds faces this whole course again, with volunteers.

**Its launch is a launch.** A popular revival draws a crowd on its first night, and the funnel from [week 1](w01-launch-day-anatomy.md) and the queue from [week 2](w02-capacity-planning-and-login-queues.md) apply unchanged. Nostalrius, a fan server for the original 2004-era World of Warcraft, opened on 28 February 2015 and registered over 800,000 accounts before Blizzard's cease-and-desist letter closed it on 10 April 2016. Fan servers that big face the capacity questions of a commercial launch with a hobby budget.

**Its costs are real and its income is awkward.** Every player-hour costs hosting money, and MMO404 week 13 shows how to price one. A licensed server like Homecoming can fund itself openly with donations. An unlicensed one takes money at legal risk. Toontown Rewritten, a fan remake of Disney's Toontown Online, which closed on 19 September 2013, reached open beta on 19 September 2014. Its team refuses outside donations for server costs and runs no advertising, to avoid legal conflict with Disney. Those are design decisions about money, made for legal reasons.

**Its end is also a shutdown.** Volunteers leave, hosts stop paying, rights holders send letters. Nostalrius's team then wrote a long post-mortem of their own project and presented it to Blizzard. [Week 12](w12-writing-a-post-mortem.md) looks at how to write one.

The practical point for a studio designer is this. The people who rebuild your world after you are, in effect, your last live-ops team. What you hand them sets how many years they spend rebuilding before they can start running it.

## In-class activity (25 minutes)

Groups of three. Your studio will close a mid-sized MMO in six months. Your numbers: `B = 2,000` behaviours. Today the fan wiki and existing packet logs give evidence for `q = 55%`. A fan group has promised 30 volunteers at 6 hours a week. Use `w = 60`, `g = 4`, `w_s = 3`. Your options, pick at most two:

- (a) A capture window with a public statement and an in-game tour of every old zone and event. Estimated to raise `q` to 85%.
- (b) A protocol document written by two engineers for a month. Estimated to cut `w` to 40 for evidence-backed behaviours.
- (c) Server binaries under a hosting licence. Needs the licensor's consent, which your legal team rates at 50%.

1. Compute `T` for no action, (a), (b), (a)+(b), and (c) if consent is granted.
2. Compute the expected `T` for "try (c), fall back to (a)+(b) if consent is refused," weighting each outcome by its 50% chance.
3. Write the one-paragraph preservation section of your sunset plan, with the numbers.

Expected output. `V = 180`. No action: bracket `0.55 + 4 × 0.45 = 2.35`, `H = 282,000`, about 30.1 years. (a): bracket `0.85 + 0.6 = 1.45`, about 18.6 years. (b): `w = 40` applies only to the evidence share, so `H = 2,000 × (0.55 × 40 + 0.45 × 240) = 260,000`, about 27.8 years. (a)+(b): `2,000 × (0.85 × 40 + 0.15 × 240) = 140,000`, about 15.0 years. (c): `2,000 × 3 / 180 = 33` weeks, about 0.6 years. Expected with fallback: `0.5 × 0.6 + 0.5 × 15.0 ≈ 7.8` years. A strong answer notices that (a) costs almost nothing and should run in any case, and that the legal ask for (c) must start now.

## Common misconceptions

- **"More volunteers is the main way to speed up a revival."** Volunteers scale the whole curve. Evidence moves the kink, and source moves the whole curve onto a different line. The studio's choices on the last day usually outweigh years of recruiting.
- **"The client contains the game, so players already have it."** The client draws the world and sends inputs. The rules, loot tables, scripts and state live on the server, and only the parts a player triggered and recorded can be copied.
- **"An emulator recreates the last version."** Many deliberately rebuild an older version players preferred, such as SWGEmu's pre-Combat Upgrade target.
- **"If the studio does nothing, the world is gone."** Meridian 59, Star Wars Galaxies and City of Heroes all had their server code leak. Doing nothing mostly decides whether the studio has any say.

## Check yourself

1. An emulator team has `V = 300` hours a week. The game has `B = 3,000`, `w = 50`, `g = 5`. How many years at `q = 0.6`? How many at `q = 0.9`? How many volunteer-hours per week would the `q = 0.6` team need to match the `q = 0.9` timeline?
2. With the section 2 values, how many weeks does each point of `q` (1%) add to the full rebuild? Show the formula.
3. A studio can either publish full drop tables and quest text for 30% of its behaviours (raising `q` from 50% to 80%) or pay for a protocol document that halves `w` for evidence-backed behaviours. Using the section 2 values otherwise, which saves more years?
4. Place Asheron's Call and Ryzom on the model. For each, which parameter did the last weeks or the studio's decision change, and in which direction?
5. Your game uses a licensed film world and a commercial physics library. List the approvals you need for a source release, and say which row of the section 3 table you can reach without any of them.

<details>
<summary>Answers</summary>

1. `q = 0.6`: bracket `0.6 + 5 × 0.4 = 2.6`, `H = 3,000 × 50 × 2.6 = 390,000`, 1,300 weeks, 25.0 years. `q = 0.9`: bracket `0.9 + 0.5 = 1.4`, `H = 210,000`, 700 weeks, 13.5 years. To match 700 weeks at `q = 0.6`, `V = 390,000 / 700 ≈ 557` hours a week, nearly double.
2. `ΔT = 0.01 × B × w × (g − 1) / V = 0.01 × 1,500 × 60 × 3 / 200 = 13.5` weeks per point.
3. Drop tables: bracket goes from `0.5 + 2.0 = 2.5` to `0.8 + 0.8 = 1.6`, saving `1,500 × 60 × 0.9 / 200 = 405` weeks, 7.8 years. Protocol document at `q = 0.5`: evidence-backed work falls from `1,500 × 0.5 × 60` to `1,500 × 0.5 × 30`, saving 22,500 hours, 112.5 weeks, 2.2 years. The data dump saves more, because the expensive part is the guessed tail.
4. Asheron's Call: players capturing traffic in the final weeks raised `q` before it froze; the eras they did not capture remain the slow tail. Ryzom: the 2010 source release set `w_s` for every future community, moving it to the source line before any shutdown.
5. The film licensor's consent for anything that ships the world's names, art or characters; the physics vendor's permission to redistribute its library (or a replacement); legal review of the code for secrets. Without any of them, you can run a capture window and publish your own data and documents about your own systems, the second and third rows, provided the published data does not reproduce the licensor's material beyond what your licence allows.

</details>

## Lab / assignment hook

[Lab 11, preservation plan](../labs/lab11.md). You implement the rebuild model with a piecewise completeness curve, fit it to a small invented project history, compare handover packages for a shutdown, and write the preservation section of a sunset plan with the numbers. It counts toward the case analyses (50%).

## Sources

- Wikipedia, "Star Wars Galaxies" (read September 2026). Servers shut down on 15 December 2011; SWGEmu founded in 2004 to recreate the pre-Combat Upgrade version from scratch, targeting publish 14.1; in 2020 the project announced it was near completion of the base game and that Jump to Lightspeed might not be in version 1.0; Project SWG founded in 2011; in 2013 a former SOE employee leaked the 2010 client, server and tools source to people involved with Project SWG, and it later spread.
- Wikipedia, "City of Heroes" (read September 2026). Private server revealed on 15 April 2019; server code widely distributed three days later and a public server quickly started; licence to Homecoming Servers LLC on 4 January 2024. MMO301 week 13 (this program) for the closure dates.
- ACEmulator, GitHub organisation and README of ACEmulator/ACE (github.com/ACEmulator, read September 2026). Repository created 16 January 2017; a from-scratch open-source server for Asheron's Call; aclog, an automatic network packet capture tool; ACE-PCAP-Exports, packet-capture data built for use as world database data; ACE-World-16PY-Patches README, base content labelled February 2005, later content ongoing.
- Wikipedia, "Asheron's Call" (read September 2026). All servers closed on 31 January 2017; new account creation disabled in December 2016.
- Wikipedia, "Meridian 59" (read September 2026). 3DO shut the game on 31 August 2000; a developer leaked the server software soon after; the game returned to Andrew and Chris Kirmse in February 2010; released as freeware with most of the source under GPLv2 on 15 September 2012.
- Wikipedia, "Ryzom" (read September 2026). On 6 May 2010 the full source code was released under the AGPL and the artwork under CC-BY-SA.
- Wikipedia, "Nostalrius" (read September 2026). Opened 28 February 2015, over 800,000 registered accounts, closed after a cease-and-desist letter on 10 April 2016; the team later presented a post-mortem document to Blizzard.
- Wikipedia, "Toontown Online" and "Toontown Rewritten" (read September 2026). Toontown Online closed on 19 September 2013; Toontown Rewritten open beta on 19 September 2014; its team refuses external donations for server costs and runs no advertising to avoid legal conflict with Disney.
- The rebuild model, its parameters and all hours, team sizes and probabilities in sections 2 and 3 and the activity are invented teaching values, not measurements of any real project.

## Interactive spec: examples/w11-rebuild-clock.html

**The one insight:** a from-scratch rebuild slows sharply at the share of the game somebody recorded, so evidence gathered before the shutdown moves the finish line more than extra volunteers, and a source release puts the project on a different line altogether.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the rebuild": x = years 0 to 30, y = share of the game rebuilt, 0% to 100%. The completeness curve `C(t)` for the current settings (`--steel`), with a marker and label at the kink `(t_q, q)`. A second curve for the source-released case (`--moss`) that reaches 100% near the left edge. When `q` changes, the previous curve stays as a faint ghost.
- View B, "years against evidence": x = `q` from 0% to 100%, y = total years `T`. The from-scratch curve `T(q)` (`--blood`) for the current `B`, `w`, `g`, `V`, and a flat line at `T_s` (`--moss`). A vertical marker at the current `q`.

**Controls:**

- Evidence `q`, slider 0% to 100%, step 1% (default 80%).
- Behaviours `B`, slider 200 to 5,000, step 100 (default 1,500).
- Hours per behaviour with evidence `w`, slider 10 to 150, step 5 (default 60).
- Guess multiplier `g`, slider 1 to 10, step 0.5 (default 4).
- Volunteers, slider 1 to 100 (default 25), and hours per volunteer per week, slider 1 to 20 (default 8); `V` is their product.
- Hours per behaviour with source `w_s`, slider 1 to 20 (default 3).
- Preset buttons: "section 2 example", "capture window (q 55% to 85%)", "double the team".

**Readout (always visible, `aria-live="polite"`):** `V`, `H`, `T` in weeks and years, `t_q` in years, `T_s` in years, the extra weeks per missing point of `q` (`B × w × (g − 1) / (100 × V)`), and a sentence such as "The last 20% of the game takes 6.9 years, as long as the first 80%."

**Formulas:**

```
V   = volunteers × hours per week
H   = B × w × (q + g × (1 − q))
T   = H / V   weeks;  years = weeks / 52
t_q = B × q × w / V
C(t) = min(q, V × t / (B × w))                                  for t ≤ t_q
C(t) = min(1, q + (V × (t − t_q)) / (B × g × w))                for t > t_q
T_s = B × w_s / V;  C_s(t) = min(1, V × t / (B × w_s))
(t in weeks for the formulas; the axis shows years)
```

**Test values (must match):**

- Defaults: `V = 200`, `H = 144,000`, `T = 720` weeks = 13.8 years, `t_q = 360` weeks = 6.9 years, `T_s = 22.5` weeks = 0.4 years, 13.5 extra weeks per missing point.
- `q = 100%`: `T = 450` weeks = 8.7 years, no kink.
- `q = 40%`: `T = 1,260` weeks = 24.2 years, `t_q` = 3.5 years.
- `q = 70%`: `T = 855` weeks = 16.4 years.
- "Double the team" (50 volunteers): `T = 360` weeks = 6.9 years at `q = 80%`.
- `g = 1`: `T` does not depend on `q` (450 weeks).

**First screen:** defaults, View A showing the kink at 80% and 6.9 years with the tail reaching 100% at 13.8 years, the source curve finished at 0.4 years, and the caption "Somebody recorded 80% of this game. The other 20% takes as long to rebuild."

**Accessibility:** every control keyboard operable with visible focus; readout in `aria-live="polite"`; key values also shown in a small table under View B (`q` = 40%, 60%, 80%, 90%, 100%); `prefers-reduced-motion` disables curve animation; respects `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art, logos or screenshots.
