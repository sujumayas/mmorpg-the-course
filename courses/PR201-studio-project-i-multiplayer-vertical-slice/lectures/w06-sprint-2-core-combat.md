# PR201 · Week 06 — Sprint 2: Core Combat

**Why this matters:** Sprint 1 proved that two machines can share a world. Sprint 2 has to prove that the world is worth sharing. Combat is the verb your players will repeat hundreds of times, and in a networked game it touches every discipline at once. A team that plans this sprint by adding up estimates will end it with five half-features and nothing to playtest in week 7.

**You will be able to:**
- Compute a sprint forecast from sprint 1's measured velocity and next sprint's availability.
- Order a combat backlog by dependency so the committed stories form one playable loop.
- Estimate the chance that a chain of dependent stories finishes, and change the plan when it is too low.
- Decide which combat feedback the client predicts and which waits for the server, using a latency budget.

**Before class:** Bring your sprint 1 board export (committed stories, estimates, done or not done) and each member's hours from sprint 1. Reread [PR101 week 5, section 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) on sprint planning and [GD203 week 4, section 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) on designing from a target time-to-kill. Martin Fowler's two-paragraph note "Yesterday's Weather" (martinfowler.com, 2004) takes five minutes.

**Prerequisites from earlier courses:** [PR101 week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (estimate ratios and buffers). [PR101 week 7, task tracking and definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) (WIP limits, levels of done). [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md). [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md). [CS202 week 11, lag compensation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md). [GD203 week 10, enemy design by the numbers](../../GD203-combat-and-progression-design/lectures/w10-enemy-design-by-the-numbers.md).

---

## 1. What sprint 2 has to prove

Sprints 2 and 3 run over weeks 6 to 9. Sprint 2 covers weeks 6 and 7 and ends at the week 7 review, where another team plays your build. So the calendar fixes the sprint goal. **By the end of week 7, three players on three machines can fight one enemy type, kill it, die, respawn and understand what happened, in a build made outside the editor.**

Read that goal as a list of things the sprint must connect, not a list of features to start:

- an input on one client becomes an attack request to the server;
- the server checks the request (range, cooldown, target alive) and applies damage;
- health changes replicate to every client;
- death and respawn happen on the server and replicate;
- each client shows feedback (animation, sound, a number, a health bar) that matches what the server decided.

Every item crosses a boundary between two disciplines or two machines. The programmer who writes the damage code needs the designer's numbers, the artist's hit animation needs a network event to trigger it, and the audio student needs to know which events are predicted locally and which arrive a tenth of a second later. That is why combat is the sprint where cross-discipline teams most often fall apart. Everyone can be busy all fortnight without the parts ever meeting.

The rest of this guide gives you three tools for keeping them together. The first is a forecast that tells you how much fits. The second is a rule for choosing what fits. The third is a latency budget that tells the artist and audio student what "responsive" means in milliseconds.

## 2. Combat is a networking feature

You met the pieces in CS202. Here is how they land on your board.

**Authority.** The server owns health, cooldowns and death, as in [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md). A client that sends "I hit goblin 7 for 40" is a cheat waiting to happen. The client sends "I pressed attack, aimed here, at tick 1,204". The server decides the rest. Write this into the acceptance criteria of the attack story, or someone will build the fast wrong version on day 2 and it will be too entangled to remove by day 9.

**Prediction.** The local player's swing animation and whoosh sound should start the frame the button is pressed. That is [client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) applied to presentation. The damage number and the enemy's health bar should wait for the server, because predicting a hit that the server rejects looks worse than a short delay.

**Lag compensation.** Melee in a small co-op slice usually does not need it. The server can check range against its own current positions with a small tolerance. Ranged attacks against moving targets do need it, and [CS202 week 11](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md) shows it is a week of careful work. Put it below the line unless your pitch depends on it.

**Tuning targets.** Before anyone types a damage number, the designer writes a time-to-kill target for the enemy, per [GD203 week 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md), and solves for the stat block, per [GD203 week 10](../../GD203-combat-and-progression-design/lectures/w10-enemy-design-by-the-numbers.md). For example: "a grunt dies in about 6 seconds to three players, and kills an idle player in about 12". Those two numbers are the acceptance test for the tuning story. Without them, tuning never finishes.

## 3. The latency budget for feedback

"Make combat feel responsive" is not a task anyone can finish. A latency budget turns it into a table. For feedback that waits for the server, the delay from button press to feedback is roughly:

```
delay ≈ RTT + wait for the next server tick
average wait = T / 2, worst wait = T
```

where `RTT` is the round-trip time between client and server and `T` is the server tick interval (50 ms at 20 Hz, 33 ms at 30 Hz). This ignores rendering and client interpolation delay, which add more. [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) covers why you might pick one tick rate over the other.

| CS202 week 14 profile | RTT (ms) | Tick | Average delay (ms) | Worst delay (ms) |
|---|---|---|---|---|
| LAN | 2 | 30 Hz | 19 | 35 |
| Good broadband | 40 | 20 Hz | 65 | 90 |
| Evening Wi-Fi (the campus Wi-Fi case) | 60 | 20 Hz | 85 | 110 |
| Mobile | 120 | 20 Hz | 145 | 170 |

The RTT column doubles each profile's one-way delay and ignores jitter.

Check one row. Mobile has 120 ms RTT at 20 Hz, so `T = 50`. Average `120 + 25 = 145`, worst `120 + 50 = 170`.

Now split the feedback into two columns and agree it as a team:

| Predicted on the client (0 ms) | Confirmed by the server (the table's delay) |
|---|---|
| Swing animation, whoosh sound, own stamina bar | Hit spark on the target, damage number, target health bar, death |

The artist and the audio student now know two things. The swing must read well on its own, because on a poor connection it plays alone for up to about 170 ms. The impact sound belongs to the confirmed column, so it should not be baked into the swing animation. That one decision prevents the most common sprint 2 bug report, "sound plays when I miss".

## 4. Worked example: the sprint that adds up and doesn't play

### The hook

BioWare's *Anthem* was released on 22 February 2019 after development that began around 2012. According to reporting summarized on its Wikipedia page, flying, the game's signature traversal verb, was added and removed several times during development. It was put back for a six-week push in 2017 to build a demo for EA executive Patrick Söderlund, and that demo became the E3 2017 reveal. When reviews came in, flying and combat were among the few parts critics praised.

A large studio took years to lock its core verb. You have two weeks. The lesson for sprint 2 is not "work faster". It is that a verb nobody can play end to end has not been decided, however many parts of it exist. Sprint planning is where you choose whether this sprint ends with a playable verb or with parts.

### The model

The plan has two steps. Each is one line.

**Step 1, the forecast.** Use **yesterday's weather**. Plan to finish about as much this sprint as you finished last sprint, scaled by how many hours the team will actually have. The term comes from the Extreme Programming community. Martin Fowler describes it as crude but hard to beat. In this course the unit of work is the **estimated hour**, as in weeks 4 and 5, so the rate is week 5's focus factor measured on sprint 1.

```
f         = estimated hours done in sprint 1 / useful hours in sprint 1
forecast  = f × useful hours in sprint 2
```

"Estimated hours done" is the sum of the original estimates of tasks that met your definition of done at the sprint 1 review. Half-finished tasks count zero. "Useful hours" are the hours people actually had after illness, deadlines in other courses and travel, minus week 4's coordination cost.

**Step 2, the dependency rule.** Commit stories in an order where every committed story's dependencies are also committed (or already done). Among the orderings that satisfy this, commit first the chain that makes the sprint goal playable. Only then add stories that widen it.

A supporting number tells you how risky a chain is. If a chain has `k` stories that must all finish, and each finishes with probability `q`, then

```
P(chain finishes) = q^k
```

This treats the stories as independent, which they are not quite. It is still a good warning light.

### Numbers you can check

The sample team is *Hollowmarch* from weeks 1 to 5: six members (two programmers, a designer, an artist, an audio student and a producer) building a three-player co-op slice. Their sprint 1 record comes straight from weeks 4 and 5:

| Sprint 1 | Value |
|---|---|
| Estimated hours committed at planning | 48 |
| Estimated hours added during the sprint (relay and enemy packing) | 10 |
| Estimated hours done (met definition of done) | 43 |
| Tasks in the sprint (16 planned + 2 added) / done | 18 / 14 |
| Useful hours: 90 available − 15 coordination (week 4) | 75 |

Coordination is week 1's `c = 0.25` hours per channel per week, times five channels, so 1.25 hours a week each, 15 hours for the team over two weeks. In sprint 2 the artist's exam is over and everyone has 16 hours, so useful hours are `6 × 16 − 15 = 81`, the figure week 5 planned with.

```
f        = 43 / 75 = 0.573
forecast = 0.573 × 81 = 46.4  →  commit 46 estimated hours
```

Planning on all 81 useful hours "because we'll work harder" ignores what sprint 1 measured: it finished 43 of the 58 estimated hours it ended up holding. Yesterday's weather says 46.

Two items come first, before any combat story. The **R2 prediction spike** (8 hours) is the first task of the sprint, because week 3's risk register says its loss doubles if it slips past day 1. The **carry-over** from sprint 1 was re-estimated at the week 5 review. The hit sounds (3 hours) become part of C4 below, whose 6 hours include them. The relay (6 hours) is only needed to play from home, and every playtest and the showcase run in the lab, so the team moves it to the cut list with its player-loses line. Enemy state packing (4) and the R6 export spike (2) are not on the path to the sprint 2 goal, since one grunt type fits the default synchronizer and the lab server can run windowed. They go to sprint 3's system list. That leaves `46 − 8 = 38` hours for combat.

Now the combat backlog, estimated in hours. The product owner (the designer) ordered it by excitement:

| Order | Story | Estimate (h) | Depends on |
|---|---|---|---|
| 1 | C1 Server-authoritative basic attack (range, cooldown checks) | 10 | sprint 1 skeleton |
| 2 | C6 Second ability: ranged bolt | 10 | C1 |
| 3 | C8 Lag compensation for the bolt | 16 | C6 |
| 4 | C5 Grunt enemy, server-side AI | 10 | C2 |
| 5 | C2 Server health and damage, replicated | 6 | C1 |
| 6 | C9 Combat particle pass | 6 | C4 |
| 7 | C3 Death and respawn, replicated | 6 | C2 |
| 8 | C4 Hit feedback: spark, number, impact sound | 6 | C2 |
| 9 | C7 Party health bars | 4 | C2 |
| 10 | C10 Hit-stop and camera shake | 4 | C4 |

**Plan A, hours in list order.** Take stories from the top until the next one would pass 38. C1 (10), C6 (10) and C8 (16) make 36. C5 would make 46, so stop. The plan fits the forecast, and it is useless. Nothing in it applies damage (C2 is missing), so the ranged bolt and its lag compensation hit nothing that can die. At the week 7 playtest, testers can swing and shoot at the air.

**Plan B, the loop first.** Follow the dependencies from the sprint goal backwards. The goal needs death (C3) and feedback (C4). Both need damage (C2), which needs the attack (C1). A target needs the grunt (C5).

| Committed | Estimate (h) | Running total |
|---|---|---|
| R2 prediction spike | 8 | 8 |
| C1 Basic attack | 10 | 18 |
| C2 Health and damage | 6 | 24 |
| C3 Death and respawn | 6 | 30 |
| C4 Hit feedback (includes the carried hit sounds) | 6 | 36 |
| C5 Grunt enemy | 10 | 46 |
| *line* | | |
| C7 Party health bars (first stretch story) | 4 | 50 |
| C10 Hit-stop and shake | 4 | 54 |

The combat stories take 38 hours, the whole room left after the spike, and every one of them is needed for the goal. The ranged bolt moves to sprint 3, where it can be judged against a loop that already plays. Lag compensation for it (C8, 16 hours) goes to the cut list with its player-loses line ("the bolt can miss a target that moved in the last 100 ms"). Section 2 says a small co-op slice can check range against the server's current positions, and nothing in the pitch depends on precise ranged hits.

**The chain risk.** Plan B's combat is one chain of five stories. Sprint 1 finished 14 of its 18 tasks, so a rough `q` is `14 / 18 = 0.78`. Then `q^5 = 0.28`. Less than one chance in three that the whole loop works by week 7. That number is too low. It also explains sprint 1, where every goal task finished only because the team stopped starting other work on day 6. Long chains of stories that each look likely rarely finish together.

| Per-story finish rate `q` | Chain of 3 | Chain of 5 | Chain of 7 |
|---|---|---|---|
| 0.78 (14 / 18) | 0.47 | 0.28 | 0.17 |
| 0.80 | 0.51 | 0.33 | 0.21 |
| 0.90 | 0.73 | 0.59 | 0.48 |
| 0.95 | 0.86 | 0.77 | 0.70 |

The team cannot make the chain shorter, because the goal needs all five. It can raise `q`. Three changes do that, and none adds hours:

- **Swarm the chain.** Set a WIP limit of two stories in progress ([PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md)). Nobody starts C10 while C2 is open.
- **Build the thin version first.** C4 starts as a white flash and a placeholder beep. The artist's final spark is a separate story below the line.
- **Integrate daily.** Every story on the chain is merged and playable in a networked build the day it is done, not at the end.

If those changes lift `q` to 0.9, the chain's chance rises to 0.59. That is still not certain, which is why C7 and C10 wait below the line rather than being promised.

### Cross-game recognition

The same two rules show up far outside this course. Mark Cerny's "Method", which he set out in 2002 while consulting for Sony's first-party studios, ends pre-production with a "publishable first playable". That is a small piece of the game that proves the core at shipping quality. That is plan B at studio scale. Fowler's yesterday's weather comes from Extreme Programming on business software. He and Kent Beck named a practice teams already used, and Fowler's point is that the crude rule is not much less accurate than elaborate ones. And the chain product `q^k` is the reliability formula for components in series, used for machines and supply chains. A system of five parts that must all work is weaker than its weakest part.

### Eyes-open judgment

Yesterday's weather has limits. After one sprint, you have one data point. Sprint 1 was mostly programmer work, and sprint 2 leans on art and audio, so the rate may not transfer. Treat 46 as the middle of a range, and put two stretch stories below the line so a good fortnight has somewhere to go. Do not treat the total as one pool of interchangeable hours. Six hours of art cannot be done by a networking programmer, so check each discipline's share against the person who will do it, as week 4's per-person limits do.

The dependency rule also costs something. Plan B leaves the product owner's favorite story, the ranged bolt, out of the sprint. That is a real loss if the pitch sold the game on ranged combat. In that case the right move is to swap C5's grunt for the bolt's target dummy, not to commit both. Decide which verb the slice is about, write it in the sprint goal, and let the rule do the rest.

## 5. Running the sprint

Three habits keep sprint 2 on the rails.

**A combat test map.** One small scene, checked in on day 1, with a grunt spawner, a respawn point, a training dummy that prints received damage, and a debug overlay showing RTT and tick. Everyone tests here, so bug reports are comparable.

**Network conditions from day 1.** Run the game through a conditioner with the Evening Wi-Fi profile from the latency table at least once a day. [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md) shows how. Combat that feels fine at 0 ms is not tested.

**Standup against the chain.** Each standup starts with one question. Which link of C1 to C5 is not done, and who is on it? Stories off the chain are discussed after.

## Studio session plan

Week 6 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:20 | Briefing: sections 1 to 3 of this guide | Sprint goal wording agreed per team |
| 0:20-0:45 | Teams compute sprint 1 rate and sprint 2 forecast (lab 06, part A) | Forecast in the sheet, checked by a neighbor team |
| 0:45-1:30 | Sprint planning: write combat stories with acceptance criteria and dependencies; draw the chain; set the line (lab 06, part B) | Ordered backlog with the line drawn |
| 1:30-1:40 | Break | |
| 1:40-2:00 | Latency budget: fill in the predicted and confirmed columns with the artist and audio student present | Feedback table in the TDD |
| 2:00-2:15 | Run `check_sprint_plan.py`; fix what it flags | Clean checker output |
| 2:15-2:45 | Instructor round: 5 minutes per team on chain risk and the top story's acceptance criteria | Notes on the board |
| 2:45-3:00 | Start C1 on the combat test map; set up the conditioner | First commit of sprint 2 |

## Deliverables

Due at the end of the week 6 meeting:

1. **Sprint 2 plan** in the lab 06 format ([`labs/lab06.md`](../labs/lab06.md)): the forecast inputs, the ordered backlog with estimates, owners and dependencies, the line, and the sprint goal as one sentence. Checked by running `check_sprint_plan.py`. It must report no errors.
2. **Feedback table** (predicted versus confirmed) added to your technical design document, with the RTT and tick rate you designed for.
3. **Tuning targets** for the enemy: target time-to-kill and time-to-die, written as acceptance criteria on the tuning story.

Due at the start of the week 7 meeting is a networked build of the sprint 2 increment, made outside the editor, tagged in version control. Week 7 describes how it is reviewed.

## Common failure modes

- **Planning by hours only.** The plan fits the forecast and contains no loop. The fix is the dependency rule, which commits the chain first.
- **Committing sprint 1's number again.** "We'll catch up" is the planning fallacy from PR101 week 6. Commit the forecast, and put the catch-up work below the line.
- **Client-authoritative damage "for now".** It gets built on day 2, the feedback code grows around it, and removing it in sprint 3 costs more than doing it right. Put server authority in C1's acceptance criteria.
- **Final art on the chain.** The artist's polished spark sits on the critical path and arrives on day 9. Split every presentation story into a placeholder on the chain and a final version below the line.
- **Testing only on localhost.** Combat that has never seen 100 ms of RTT will surprise you at the playtest. Use the conditioner daily.
- **Everyone starts their own story on day 1.** Five stories in progress, none done, and the chain stalls at C2. Keep a WIP limit.

## Review checklist

The instructor checks at the week 6 meeting and again at the start of week 7:

- [ ] Forecast computed from sprint 1's estimated hours done and real useful hours; the committed total does not exceed it by more than 10%.
- [ ] Every committed story has an owner, an estimate, acceptance criteria and its dependencies listed; the checker reports no dependency above the line that points below it.
- [ ] The committed set contains a complete loop from input to server decision to replicated result to feedback.
- [ ] The chain's risk is stated (`q`, `k`, `q^k`) with at least one concrete change to raise `q`.
- [ ] Damage, health, cooldown and death are server-authoritative in the acceptance criteria.
- [ ] Feedback table exists and names RTT and tick rate; impact sound is in the confirmed column.
- [ ] Enemy tuning targets are written as numbers.
- [ ] At the start of week 7: a tagged build outside the editor, which the instructor can join from a second machine.

## Sources

- Wikipedia, "Anthem (video game)" (accessed September 2026), summarizing Schreier, J., "How BioWare's *Anthem* Went Wrong", *Kotaku*, 2 April 2019. Release on 22 February 2019; flying added and removed several times during development and re-added for the six-week demo prepared for Patrick Söderlund's 2017 visit; that demo as the basis for the E3 2017 reveal; critics' praise for combat and flight.
- Fowler, M. "Yesterdays Weather." martinfowler.com, 12 May 2004. The principle of planning an iteration to match the last one's output, its origin in Extreme Programming, and its defense as crude but hard to beat.
- Wikipedia, "Mark Cerny" (accessed September 2026), section "The Method process". Set out in 2002 while consulting for Sony first-party studios; freeform pre-production ending in a "publishable first playable".
- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. Sprint goal and increment.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on sprint planning in cross-discipline game teams.
- The *Hollowmarch* team, its sprint 1 record (from weeks 4 and 5) and its backlog are invented for teaching. The latency table uses the teaching profiles from CS202 week 14 and omits rendering and interpolation delay by design.
