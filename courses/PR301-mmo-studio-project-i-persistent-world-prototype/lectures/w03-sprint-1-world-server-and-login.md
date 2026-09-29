# PR301 · Week 03 — Sprint 1: World Server and Login

**Why this matters:** Sprint 1 builds the part of the world that everything else stands on: an account, a login, a character that appears in a shared space and is still there after a restart. It is also the sprint where every story lands on the programmers. Teams that plan it by adding up everyone's hours commit twice what their programmers can finish, and the artists spend two weeks waiting for a server to put things in.

**You will be able to:**
- Compute each person's sprint capacity from a focus factor measured in PR201.
- Find the person-level bottleneck in a sprint plan whose team total looks fine.
- Reshape a sprint 1 plan with four moves (narrow the goal, stub, move, mob) until no one's load is above 1.
- Write a sprint goal and a definition of done for server stories that a bot test can check.

**Before class:** Reread [PR201 week 3](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w03-technical-design-document.md) section 2 (spikes and the walking skeleton) and [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) section 4 (yesterday's weather and chain risk). Reread [MMO302 week 9](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) sections 1 and 3 (the login pipeline and session tickets). Bring your week 2 decision record, your sprint 1 proof, and your PR201 team's sprint records.

**Prerequisites from earlier courses:** [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) for sprint planning. [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) for definitions of done. [PR201 week 1](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w01-pitch-and-team-formation.md) for the channel cost and discipline loads. [DB201 week 2](../../DB201-data-persistence-and-telemetry/lectures/w02-relational-modeling-characters-inventories-items.md) for the character schema. [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) for the save strategies in your persistence map.

---

## 1. What sprint 1 has to prove

Week 2 ended with one sentence. For the *Saltmarsh* team it reads: "50 bots log in, walk, log out and log back in at the position they left, and the server survives a restart in the middle." That sentence is the **sprint goal**. The sprint runs two weeks, to the start of the week 5 session, where the sprint 1 review answers it yes or no. The week 4 session is the midpoint check.

Notice what the goal leaves out. It has no art, no combat and no human player. It asks for the thinnest path through every layer that the rest of the course depends on. That means account, authentication, session, world, replication, database and restart. PR201 week 3 called that path a **walking skeleton**, the smallest end-to-end version of the real system, built to production habits and kept.

Notice also who the players are. They are bots. A human-playable client matters, but a bot proves more in sprint 1. It can log in fifty times at once, it logs what happened, and it runs again tomorrow without anyone giving up an evening. Treat the bot client as a product with an owner, not a test script someone writes on the last night.

## 2. Worked example: the sprint that fits the team and not the programmers

### The hook

Square Enix released Final Fantasy XIV on 30 September 2010. Reviews were harsh, with a Metacritic score of 49. The development team later concluded that the game's foundations could not be repaired. Its engine was a poor fit for an MMO and its internal structure was broken. The servers closed on 11 November 2012. The game returned in August 2013 as *A Realm Reborn*, with a new engine, new server infrastructure and redesigned systems. A large studio rebuilt its foundations from nothing because the first ones could not carry the game.

You cannot rebuild in week 9. Your foundation is what sprint 1 finishes. The trouble is that sprint 1's work is almost all code, and a plan that counts the whole team's hours will promise a foundation that the programmers cannot build in two weeks.

### The model

A **focus factor** turns hours into promises. In PR201 you recorded, for each sprint, the hours of estimated work in stories that met the definition of done, and the hours people were actually available. Their ratio is your focus factor:

```
f = estimated hours of done stories / available hours
```

It is below 1 because of interruptions, debugging, review, integration and estimates that run long. Then for a sprint of `w` weeks, a team of `n`, and person `i` with `H_i` hours a week:

```
capacity_i = f × (H_i − c × (n − 1)) × w
charge     = estimate × x    if the story is outside the owner's primary discipline, else estimate
load_i     = Σ charges on stories owned by i / capacity_i
```

- `c × (n − 1)` is the coordination cost from PR201 week 1, with `c = 0.25`.
- `x` is the **cross-discipline factor**. A designer writing a bot script takes longer than a programmer would. Use `x = 1.5` until you measure your own.
- The plan fits when **every** `load_i ≤ 1`, not only the team total.

Stories done together in the studio session, with the whole team in the room, are charged to nobody, up to the session's three hours. This is called **mobbing**: one keyboard, everyone watching and talking. It is slow for most work. It is fast for decisions everyone must share, such as the message protocol.

### Numbers you can check

The *Saltmarsh* team has seven people: three programmers (Ana on the server, Ben on the client, Chen on tools and the database), a designer (Dee), two artists (Eli and Fay) and a producer (Gus). Everyone has `H = 8`. Their PR201 median focus factor was `f = 0.62`. The sprint is two weeks.

```
capacity_i = 0.62 × (8 − 0.25 × 6) × 2 = 0.62 × 6.5 × 2 = 8.06 hours each
team       = 7 × 8.06 = 56.4 hours
code       = 3 × 8.06 = 24.2 hours
```

The first draft, written by the programmers on the evening after week 2:

| ID | Story | Owner | Estimate |
|---|---|---|---|
| S1 | Message protocol and schema document | Ana | 3 |
| S2 | Database schema: accounts, characters, positions | Chen | 4 |
| S3 | Login with full password auth and session ticket | Chen | 6 |
| S4 | World server accepts ticket, spawns character, ticks | Ana | 6 |
| S5 | Client login screen and connect | Ben | 6 |
| S6 | Replicate movement to nearby players | Ben | 4 |
| S7 | Save position on logout, load on login | Ana | 4 |
| S8 | Bot client and 50-login soak script | Chen | 5 |
| S9 | Build and deploy script for the test host | Ben | 4 |
| S11 | Starter zone greybox | Fay | 8 |
| S12 | Player character model, placeholder animation | Eli | 8 |
| S13 | Chat channel | Ben | 5 |

The team total is 63 hours against 56.4, a load of 1.12. That looks like "a bit ambitious". Now by person:

| Person | Capacity | Charged | Load |
|---|---|---|---|
| Ana | 8.06 | 13 | 1.61 |
| Ben | 8.06 | 19 | **2.36** |
| Chen | 8.06 | 15 | 1.86 |
| Dee | 8.06 | 0 | 0.00 |
| Eli | 8.06 | 8 | 0.99 |
| Fay | 8.06 | 8 | 0.99 |
| Gus | 8.06 | 0 | 0.00 |

Code stories total 47 hours against 24.2 hours of code capacity, a code load of 1.94. Two people are at zero. The team total hid a plan that needs nearly twice the programmers it has.

### Reshaping the plan

Four moves, applied in order of how little they cost.

1. **Narrow the goal to what it says.** The goal needs bots, not a human client. The client login screen (S5, 6 h) and chat (S13, 5 h) move to sprint 2. Code falls to 36 hours, a load of 1.49.
2. **Move work to people with slack, at a price.** Dee takes the bot client (S8). Designers script, and she will own the bots for the rest of the course. Gus takes the build and deploy script (S9). At `x = 1.5`, those stories charge 7.5 and 6 hours. Code falls to 27 hours, 1.12.
3. **Stub what can wait.** Full password authentication (6 h) becomes a dev-token login (3 h): the login service issues a signed session ticket to any name on an allow-list. Real authentication goes into the backlog as S14 for sprint 2. The session ticket path is the same, so nothing downstream changes. Code falls to 24 hours, 0.99. That is a bet, not a plan.
4. **Mob the contract.** The whole team writes the message protocol and the schema document (S1) together in today's session. It is the one story everyone needs to agree on, and doing it together means Ana, Ben and Chen can work in parallel from tonight against the same document. Code falls to 21 hours, 0.87.

Ben also takes S7 (save and load position) from Ana, because Ana owns the longest chain.

| Person | Stories | Charged | Load |
|---|---|---|---|
| Ana | S4 | 6.0 | 0.74 |
| Ben | S6, S7 | 8.0 | 0.99 |
| Chen | S2, S3 (dev tokens) | 7.0 | 0.87 |
| Dee | S8 (× 1.5) | 7.5 | 0.93 |
| Eli | S12 | 8.0 | 0.99 |
| Fay | S11 | 8.0 | 0.99 |
| Gus | S9 (× 1.5) | 6.0 | 0.74 |
| Team | | 50.5 | 0.90 |

Every load is at or below 1 and the goal is intact. Three people sit at 0.99, which the team should say out loud. If anyone on those three lines loses a day, a named story drops. The team writes the drop order now: S12 first (placeholder capsules are fine for bots), then S11.

Run `check_sprint.py` from [lab 03](../labs/lab03.md) on the starter files to reproduce the first table. It prints `NOT READY` with three overloaded programmers. Apply the four moves and it prints `PASS`.

### The same idea elsewhere

**PR201, week 1.** You found that a pitch can fit the team total and fail one discipline. Sprint 1 is the same test at a finer grain, per person, per sprint. The discipline check hides a person-level bottleneck when one discipline's work lands on one of its people.

**The theory of constraints.** Goldratt's first step is to find the constraint and his third is to subordinate everything else to it. Moves 2 and 4 are subordination: a designer and a producer take work so the programmers only do what only they can do. Mobbing S1 spends everyone's time to save the constraint's.

**Chain risk.** In PR201 week 6, a chain of `k` stories that must all finish, each with probability `q`, finishes with probability `q^k`. The skeleton is a chain: S1, S2, S3, S4, S7 and the soak test. Moves 3 and 4 shorten it. S1 is done before the sprint starts, and the stub makes S3 small enough to finish early.

### Eyes-open judgment

Stubs are debt with a date. The dev-token login is safe only because S14 is already in the sprint 2 backlog with an owner. A stub without a backlog story is how test worlds reach the beta with a login that accepts any name.

Moving work has a cost the model shows (`x = 1.5`) and one it doesn't. Dee now owns the bot client, so her design work starts a week late. That is the right trade in sprint 1, where there is little to design without a server. It would be the wrong trade in sprint 3.

Finally, `f = 0.62` came from a different project with a different mix of work. Sprint 1 of a server is integration-heavy, and integration is where estimates break. The sprint 1 review at the start of week 5 measures your real sprint 1 focus factor and replaces the borrowed one.

### Check yourself

1. Dee falls ill for four of her working hours. What is her new capacity and load? What should the team do?
2. Instead of moving S8 to Dee, the team gives it to Ana, whose primary is code. Compute Ana's load. Is that better or worse than the plan above?
3. The team's PR201 focus factor was 0.5, not 0.62. Recompute one person's capacity and find which people are over 1 in the final plan.

<details><summary>Answers</summary>

1. Her available hours fall from 13 to 9, so capacity is `0.62 × 9 = 5.58` and her load is `7.5 / 5.58 = 1.34`. The bot client is on the goal's chain, so something else must move. Gus is at 0.74 and has 2.06 hours spare, not enough for a 7.5-hour story. The team should cut S8 to the minimum the goal needs (log in, walk, log out, no reporting) and re-estimate.
2. Ana would carry `6 + 5 = 11` hours, a load of 1.36. Worse. The 1.5 factor on Dee's version costs 2.5 extra hours, but it puts them where there is slack.
3. Capacity becomes `0.5 × 13 = 6.5`. Ana is at `6 / 6.5 = 0.92`. Everyone charged 7 hours or more is over: Ben 1.23, Chen 1.08, Dee 1.15, Eli 1.23, Fay 1.23. The plan needs a further cut, and S12 and S11 go first.

</details>

## 3. The definition of done for server stories

PR101 week 7 defined done as a list the whole team agrees to before the sprint. Server stories need three lines that a client story does not.

- **Runs on the test host.** Not on a laptop. The tagged build is deployed by the build script (S9) to the machine the alpha will use.
- **Survives a restart.** If a story touches state, the reviewer kills the server process mid-test, restarts it and checks the state against the persistence map from week 2.
- **Has a bot check.** A story is done when a bot scenario exercises it and logs the result. "Login works" becomes "the soak script logs 50 successful logins and 0 failures".

Write these into `docs/definition-of-done.md` today. Next week the review counts only stories that meet every line.

## 4. Working in parallel against a contract

Three programmers can only work in parallel if they agree on the seams. The S1 document is that agreement. It names every message between client, login service and world server, with fields and types, and every table the world server reads or writes. It is short, one or two pages, and it is versioned in the repository.

Two habits keep the contract honest.

- **Change it by pull request.** Anyone may propose a change. The other two programmers approve it. A silent change to a message field is how sprint 1 ends with a client that connects and a server that cannot parse it.
- **Test against it on day two.** Ben's movement replication and Ana's world server should exchange one real message by the end of the second working day, even if nothing else works. That is the first integration, and it should be early and small. PR201 week 7 showed the burn-down shape of a team that integrates on the last day.

## 5. Running the sprint

Hold a standup twice a week, not daily. A part-time team that meets daily spends a large share of its hours reporting. Each standup answers one question per story on the goal's chain. Is it on track to be done by the review? The producer keeps a burn-down of goal-chain hours, separate from the rest. When the chain burn-down is flat for three days, the drop order from section 2 comes into force without a meeting.

Tag a build at the midpoint, before the week 4 session, and run the soak script against it there, even if half the stories are missing. A soak test that fails on day five tells you what the review will say on day ten.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Briefing: sprint 1 goal, per-person loads, the four moves | |
| 0:15 to 1:00 | Mob session: the whole team writes S1, the message protocol and schema document, on one screen | `docs/protocol.md` version 1 |
| 1:00 to 1:10 | Break | |
| 1:10 to 1:50 | Planning: each owner estimates their stories; the producer fills `sprint.csv` and runs `check_sprint.py` | First loads |
| 1:50 to 2:25 | Reshape until `PASS`; write the drop order and the stub backlog stories | Plan at `PASS` |
| 2:25 to 2:45 | Definition of done for server stories; bot scenario list | `docs/definition-of-done.md` |
| 2:45 to 3:00 | Instructor check: each team reads its goal, its highest load and its drop order | Sign-off |

## Deliverables

Due at the end of this session, with the burn-down updated through the sprint.

- **Sprint plan** (`sprint.csv`, `team.csv`) and the saved `check_sprint.py` output showing `PASS`.
- **Sprint goal** (one sentence) and **drop order** at the top of the sprint board.
- **Protocol and schema document**, version 1.
- **Definition of done** with the three server lines.
- **Backlog stories** for every stub, each with an owner and a target sprint.

At the week 4 mid-sprint session: the midpoint build on the test host, a first soak log and the goal-chain burn-down. At the sprint 1 review at the start of week 5: the tagged sprint 1 build, the full soak results and the final burn-down. See [lab 03](../labs/lab03.md).

## Common failure modes

- **Team-total planning.** The plan fits 56 hours and nobody checks who owns them. Fix: read the load column by person.
- **The client first.** A programmer spends the first week on a login screen with nothing behind it. Fix: the goal is bots. The screen comes in sprint 2.
- **Stubs that stay.** Dev tokens reach the beta. Fix: every stub has a backlog story with a sprint number.
- **The contract in someone's head.** Two programmers build to different message formats. Fix: the protocol document exists before anyone writes networking code, and changes go by pull request.
- **Artists idle.** Art waits for a server to put things in. Fix: art works to the greybox and a capsule stand-in, and the zone is checked against bot walk paths, not against a finished client.

## Review checklist

The instructor checks the sprint plan when:

- [ ] `check_sprint.py` prints `PASS`, with every goal story committed and every dependency inside the plan.
- [ ] No person is above a load of 1; anyone at 0.95 or more is named in the drop order.
- [ ] The sprint goal is one sentence a bot test can answer, and includes a restart.
- [ ] Every stub has a backlog story with an owner and a sprint.
- [ ] The protocol and schema document is in the repository and versioned.
- [ ] The definition of done includes the test host, restart and bot check lines.

## Sources

- Wikipedia, "Final Fantasy XIV (2010 video game)" (read September 2026). Released 30 September 2010; Metacritic score of 49; the development team concluded the engine was unsuitable and the internal structure broken; servers closed 11 November 2012; rebuilt with a new engine, server infrastructure and gameplay systems as *A Realm Reborn* in 2013.
- Wikipedia, "Final Fantasy XIV: A Realm Reborn" (read September 2026), as cited in MMO302 week 9. Launch on 27 August 2013.
- Cockburn, A. "Walking skeleton", as cited in PR201 week 3.
- Goldratt, E. M. (1984). *The Goal*. North River Press. The five focusing steps, as used in PR201 week 1.
- The *Saltmarsh* team, its members, stories, estimates and the focus factor of 0.62 are invented for teaching. The cross-discipline factor of 1.5 and twice-weekly standups are course conventions.
