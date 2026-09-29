# PR101 · Week 04 — Scope: MVP, Vertical Slice, Cut Lists

**Why this matters:** In a game jam the deadline and the team are fixed before you write a line of code. Scope is the only dial left. Teams that finish do not have smaller ideas than teams that don't. They decide early what the smallest playable game is, build that first, and keep a written list of what they will drop when time runs short.

**You will be able to:**
- Compute a team's plannable hours from its capacity and buffer, and place the cut line on a prioritized task list.
- Define an MVP, a vertical slice and a cut list for a jam game, and write each one down in a form your team can check.
- Compute how much estimate overrun a plan survives, and compare build orders by that number.
- Critique a scope plan by finding the point where it stops producing a playable game.

**Before class:** Clinton Keith, *Agile Game Development* (2nd ed., 2020), the chapter on release planning and the parts on the minimum viable game (about 20 pages). Reread your GD101 one-pager. Play one jam game from the Global Game Jam or itch.io and write down, in one sentence, what the player does in it.

**Prerequisites from earlier courses:** [PR101 week 1, roles and team capacity](w01-roles-on-a-game-team.md) (the channel model gives this week's capacity number). [GD101 week 8, iteration loops and kill-your-darlings](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (cutting is the same skill applied to a schedule). [GD101 week 14, one-pagers](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) (your MVP sentence goes on the one-pager). [GD101 week 12, feedback and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (which feedback belongs in the MVP).

**Interactive:** [examples/w04-cut-line.html](../examples/w04-cut-line.html). Keep it open during section 2.

---

## 1. Scope is the one dial you control

Every project trades off three things. **Time** is how long you have. **People** is who works on it. **Scope** is how much game you try to make. Some writers add quality as a fourth corner. For this course, treat quality as part of scope, since "the same features, with bugs" is a smaller game than "the same features, working".

In a studio all three can move. A publisher can grant six more months, or a studio can hire. In a jam, the clock is fixed at 48 hours and your team was fixed in week 1. A plan that holds time and people fixed and lets scope float is called a **timebox**. The week 8 jam is one timebox. Every sprint you run from week 5 on is a smaller one.

A timebox changes the question you ask. You stop asking "how long will our game take?" and start asking "what is the best game we can finish in this time?" The second question has an answer you can work out on the first evening.

### Four words you will use all semester

**Scope.** The full list of work you intend to do: features, content, art, sound, menus, builds. If it takes someone's hours, it's in scope.

**MVP, the minimum viable product.** Eric Ries popularized the term in *The Lean Startup* (2011) for the smallest product that lets you learn whether an idea works with real users. For a game, use this sharper version: **the smallest build that a stranger can play from start to end.** Start means they know what to do. End means they can win or lose and try again. Gray boxes are fine. Silence is fine. A missing ending is not.

**Vertical slice.** A short section of the game (one level, one fight, one minute of play) built to final quality through every layer: code, art, sound, UI, feedback. It shows what the whole game will look and feel like. The name comes from thinking of the game as layers stacked on top of each other. A vertical cut goes through all of them in a thin strip. A **horizontal slice** is the opposite: one layer built across the whole game, such as all the levels in graybox with no art.

**Cut list.** A written, ordered list of work you have decided not to do unless time appears. It is not a list of failures. It is the part of your plan that lets the rest of the plan survive.

### Tiers

Most teams sort work into tiers. Dai Clegg's MoSCoW method (1994, later used in the DSDM framework) names four: **Must have, Should have, Could have, Won't have this time**. For a jam, map them like this:

| MoSCoW | Jam tier | Test |
|---|---|---|
| Must | MVP | Without it, a stranger can't play start to end |
| Should | Slice | Without it, the game plays but doesn't look or sound like itself |
| Could | Polish and content | Without it, the game is shorter or plainer |
| Won't | Cut list | Nobody touches it until everything above is done |

Tiers alone do not save a jam. The next section shows why the *order* you build them in matters as much as the tiers themselves.

## 2. Worked example: the cut line and the build order

### The hook

Three games you may have played began as tiny timeboxed builds.

- **Celeste.** In August 2015, Maddy Thorson and Noel Berry made a version of *Celeste* for the PICO-8 fantasy console over a few days. The PICO-8 limits every game to a 128 × 128 pixel, 16-color screen. The full *Celeste* shipped on 25 January 2018, about two and a half years later.
- **Surgeon Simulator.** Tom Jackson, Jack Good, Luke Williams and James Broadley made the first version at the 2013 Global Game Jam, in 48 hours. They then spent 48 days on a commercial version, which launched on Steam in April 2013.
- **Baba Is You.** Arvi Teikari built it for the 2017 Nordic Game Jam, where teams get around 40 hours. It won the jam. The full game released on 13 March 2019.

Each of those first builds was small and each was complete. A player could start, understand the one strange thing they do (dash and climb; control a clumsy hand; push the words that make up the rules), and reach an end. The years afterwards added content and polish around a core that already worked.

Now picture a jam game that doesn't get finished. At hour 44 the player can run, jump and look beautiful, but can't win or lose. The team built lots of game and no MVP. This worked example shows how a sensible-looking plan produces that, and how to see it coming on the first evening.

### The model

Start with the capacity your team computed in week 1. Using the channel model with `n = 4` people, `H = 30` working hours each over the jam and `c = 3` coordination hours per channel, useful capacity was

```
C = n × H − c × n × (n − 1) = 120 − 36 = 84 team-hours
```

You don't plan all 84 hours. You hold back a **buffer**, a fraction `b` of capacity that is assigned to nothing, to absorb the work you didn't think of and the estimates that run long.

```
P = (1 − b) × C           plannable hours
S_k = e_1 + e_2 + ... + e_k    cumulative estimate of the first k tasks, in build order
cut line: the largest k with S_k ≤ P
m_max = C / S_MVP         overrun the plan survives
```

- `C` is useful capacity in team-hours.
- `b` is the buffer fraction, between 0 and 1.
- `P` is the hours you are allowed to assign to tasks.
- `e_i` is the estimate for task `i`, in team-hours, and tasks are numbered in the order you will build them.
- `S_k` is the running total of estimates.
- The **cut line** sits after the last task that fits inside `P`. Everything below it is the cut list.
- `S_MVP` is the running total at the moment the last MVP task is finished, in your build order.
- `m` is an **overrun factor**: if every task takes `m` times its estimate, `m = 1.5` means everything takes 50% longer. Week 6 replaces this single number with a spread of different overruns per task. For now one number is enough.
- `m_max` is the largest overrun at which you still have a playable game when capacity runs out.

The last line is the one to remember. **Your plan's safety depends on how early in the build order the MVP is complete, not on how much you planned.** If the MVP is done after 24 of your 84 hours, estimates can run 3.5 times long and you still ship something playable. If it's done at hour 68, a 25% overrun leaves you with nothing to submit.

### Numbers you can check

Take a jam game, *Lantern*: a platformer where your light shrinks as your oil runs out. Here is the team's task list in priority order, with estimates in team-hours. The system column says which part of the game each task belongs to. P is the player, E enemies and hazards, L levels, A audio and effects, U user interface.

| # | Task | System | Tier | Estimate | Running total `S_k` |
|---|---|---|---|---|---|
| 1 | Player run and jump | P | MVP | 6 | 6 |
| 2 | Lantern drains, light radius shrinks | P | MVP | 4 | 10 |
| 3 | One hazard that kills on touch | E | MVP | 4 | 14 |
| 4 | One graybox level, start to exit | L | MVP | 6 | 20 |
| 5 | Win, lose and restart loop | U | MVP | 4 | 24 |
| 6 | Player sprite and animations | P | Slice | 8 | 32 |
| 7 | Hazard art and death feedback | E | Slice | 5 | 37 |
| 8 | Three sounds: jump, death, ambience | A | Slice | 4 | 41 |
| 9 | Title screen and how-to-play | U | Slice | 5 | 46 |
| 10 | Level 1 dressed in final tiles | L | Slice | 7 | 53 |
| 11 | Oil pickups refill the lantern | P | Polish | 4 | 57 |
| 12 | Second hazard: a moth swarm that follows light | E | Polish | 8 | 65 |
| 13 | Levels 2 and 3 | L | Polish | 12 | 77 |
| 14 | Music loop | A | Polish | 6 | 83 |
| 15 | Particles and screen shake | A | Polish | 5 | 88 |
| 16 | Best-time board | U | Polish | 5 | 93 |

The whole list is 93 hours, more than the team's 84 even before any buffer. With `b = 0.25`, `P = 0.75 × 84 = 63` hours. The running total passes 63 at task 12 (65 hours), so **the cut line falls after task 11**, at 57 planned hours. Tasks 12 to 16 (36 hours) are the cut list. The team plans 57 hours, keeps 27 in reserve, and has a ready answer if the reserve goes unused: pull task 12, then 13.

Why stop at task 11 and not skip ahead to the small tasks further down? Because the list is in priority order. If you can afford task 14 but not task 12, you have 6 spare hours and a more important task that needs 8. Leave those hours in the buffer. Skipping ahead to "things that fit" is how teams end up with music and no second hazard, when the second hazard was the reason the game was interesting.

Now the MVP. In this build order it's complete after task 5, so `S_MVP = 24` and

```
m_max = 84 / 24 = 3.5
```

Every estimate could be three and a half times too small and the team would still have a playable game when the time ran out.

### The same list, built by system

Here is a build order many teams fall into without deciding to. Each person owns a system and builds it to completion before handing over: the player first (tasks 1, 2, 6, 11), then the hazards (3, 7, 12), then the levels (4, 10, 13), then the UI, audio and effects (5, 8, 9, 14, 15, 16). Nobody changed a single estimate. Only the order changed.

| Order | Tasks in plan (`S_k ≤ 63`) | Win/lose loop in plan? | `S_MVP` | `m_max = 84 / S_MVP` |
|---|---|---|---|---|
| Vertical (MVP tier first) | 1-11, 57 h | Yes | 24 | 3.5 |
| By system (horizontal) | 1, 2, 6, 11, 3, 7, 12, 4, 10, 52 h | **No** | 68 | 1.24 |

In the system order, the running total reaches 52 hours after task 10, and task 13 (12 hours) would take it to 64, over `P`. So the plan stops there, and **it contains no win or lose condition at all.** The plan looks busy and balanced. Every person has work. It just isn't a game.

Now let estimates run long. Here is what's finished when the 84 real hours are gone:

| Overrun `m` | Vertical: finished | Playable? | By system: finished | Playable? |
|---|---|---|---|---|
| 1.0 | 1-14 | Yes | 1, 2, 6, 11, 3, 7, 12, 4, 10, 13, 5, 8, 9, 14 | Yes |
| 1.25 | 1-12 | Yes | 1, 2, 6, 11, 3, 7, 12, 4, 10, 13 | **No** |
| 1.5 | 1-10 | Yes | 1, 2, 6, 11, 3, 7, 12, 4, 10 | **No** |
| 2.0 | 1-8 | Yes | 1, 2, 6, 11, 3, 7, 12 | **No** |
| 3.0 | 1-5 | Yes | 1, 2, 6, 11, 3 | **No** |

Check one row yourself. At `m = 1.5`, 84 real hours buy `84 / 1.5 = 56` estimated hours. In the vertical order the running total is 53 after task 10 and 57 after task 11, so tasks 1 to 10 are done and task 11 is three-quarters done. In the system order, 52 estimated hours are done after task 10 and the next task, levels 2 and 3, needs 12. The lantern glows, the moths swarm, level 1 is beautiful, and there's no way to win.

At `m = 1` the two orders finish almost the same work. The difference shows only when estimates run long, which week 6 shows is the usual case.

### Move it yourself

Open the interactive. The top view is the task list as a single bar of blocks in build order, colored by tier, with a line at `P` and a shaded zone for the buffer. The bottom view plots "playable at the deadline?" against the overrun `m` for both build orders. Drag the overrun slider from 1 to 3. In the vertical order, the blocks that fall off the end are polish. In the system order, the win/lose block falls off almost at once. Then toggle the build order and drag a task up or down the list. Watch `S_MVP` and `m_max` update. Try to find an order that keeps `m_max` above 3 while getting the moth swarm into the plan.

### Cross-game recognition

The same model, `C`, `P`, a cut line and `S_MVP`, describes how shipped games handled scope. What changes between cases is which variable is fixed and what counts as the MVP.

**Surgeon Simulator (Bossa Studios, 2013).** The jam version had `C` = four people × 48 hours. Its MVP was one operation with the awkward hand controls. That was enough for a stranger to start, fail hilariously and try again. The commercial version then had the same four people for 48 days, roughly 24 times the calendar time. They did not rebuild the core. They added operations and modes on top of a working MVP, which is the vertical order at the scale of a whole product. Later versions kept adding content: the iPad release in March 2014 had the heart and kidney transplants plus new eye and teeth ones.

**Celeste on PICO-8 (2015).** Here the platform set part of the cut list. A 128 × 128, 16-color screen with 4-channel audio means that high-resolution art, voice and most UI are cut before you start. Rewrite it in our terms: the platform limits shrink the list, so the whole list fits inside `P` and the MVP (climb, jump, dash, one mountain) is nearly the whole game. Choosing a small engine or a strict art style for a jam is a way of writing your cut list in advance.

**World of Warcraft's Dance Studio (2007 to 2013).** Timeboxes are not only for jams. Blizzard announced a Dance Studio feature for *Wrath of the Lich King* at BlizzCon 2007. It never shipped with the expansion. Over the following years Blizzard staff described it as postponed, still a work in progress, not dropped. In 2013 Greg Street called it a "shelved project" and said shelved did not mean cancelled. In our model, each expansion and patch was a timebox with a fixed date, and the Dance Studio sat below the cut line each time. The feature was never deleted from the list. It just never rose above the line. That is a cut list working as intended in a live game, with a real cost: players had seen it announced, so every postponement was public.

Three cases, one idea. Time and people are fixed per timebox, the list is ordered, the line falls where `P` runs out, and the build that matters is the one that becomes playable earliest.

### Eyes-open design judgment

The model makes the choices visible. It does not make them for you.

- **Buffer size is a bet.** `b = 0.25` is a starting point for a first jam. Teams with a track record can shrink it. Teams using a new engine should grow it. Week 6 gives you a way to set `b` from data rather than guesswork.
- **Vertical first has a cost.** The first hours of a vertical build look ugly. Artists may wait on programmers for the graybox level. Give them MVP-tier art tasks that don't depend on code (a palette, a player silhouette at final size) so they aren't idle. The order is about what's *finished* first, not about who is busy.
- **The MVP can be wrong.** If the MVP isn't fun, the slice won't save it. That's why you build the MVP first. You find out at hour 12, not hour 44. GD101 week 8's kill criteria apply here too: decide before you playtest what result would make you change the core.
- **Don't trust a cut line you set once.** Estimates move. Re-run the cut line at fixed checkpoints (section 5), not only when things feel bad.
- **Cutting in public costs trust.** A feature you announced and then postpone (the Dance Studio case) costs goodwill that a quiet cut would not.

## 3. Writing the MVP: one sentence, one loop

You'll put your MVP on your one-pager as a single sentence. Use this template:

> The player **[verb]** to **[goal]** while **[pressure]**. They lose when **[fail state]** and win when **[win state]**.

For *Lantern*: the player **jumps between platforms** to **reach the exit** while **their light shrinks**. They lose when **they touch a hazard or the light goes out** and win when **they reach the exit**.

Every word in brackets maps to tasks. The verb is task 1. The pressure is task 2. The fail state is tasks 3 and 5. The goal and win state are tasks 4 and 5. If a bracket maps to no task, your plan has a hole. If a task maps to no bracket, it isn't MVP. Check your list this way before you estimate anything.

### What goes in the MVP and what doesn't

Most things you are proud of are not MVP. Title screens, art, sound, particles, menus and second levels all belong in the slice or polish tiers. There is one exception worth arguing about: **feedback the player needs to understand the verb.** GD101 week 12 showed that a hit nobody can see might as well not have happened. If the player can't tell they died, the lose state doesn't work, so a crude death flash is MVP. A good-looking death animation is slice.

A quick test for any disputed task is to ask, "Could a stranger play start to end without it, if we were standing behind them saying nothing?" If yes, it's not MVP.

### Three MVP mistakes

1. **The MVP is a feature list, not a loop.** "Movement, enemies, three levels, a boss" has no win state and no restart. A loop is what makes it playable.
2. **The MVP is the whole game.** If your MVP is 70% of `P`, you have no room to learn. Aim for an MVP under 40% of `P`. In *Lantern* it's `24 / 63 = 38%`.
3. **The MVP tests the wrong risk.** If your game's one strange idea is "light as a resource", an MVP without the shrinking light is a generic platformer. Put the risky mechanic in the MVP, not in polish.

## 4. The vertical slice

Once the MVP is playable, the next milestone is a vertical slice. In *Lantern* that's tasks 6 to 10: one level, dressed, with sprites, sounds, a title screen and death feedback.

The slice proves things the MVP can't.

- **The pipeline works.** Art goes from the artist's tool into the engine, at the right size, with the right import settings, and appears in a build. Week 3's asset workflow is tested for real here, not in theory. A team that first imports final art at hour 40 finds the problems at hour 40.
- **The game has a look.** One dressed level tells the team, and later the judges, what every other level should look like. It becomes the reference everyone matches.
- **Estimates for content become real.** It took 7 hours to dress level 1. Now you know what levels 2 and 3 cost, instead of guessing. That number feeds the cut decision on task 13.

A slice goes deep on a small piece. Two more levels or a second enemy is breadth, and breadth is polish tier.

## 5. Cut lists and cut triggers

A cut list does its work only if the cutting decision is made before you are tired and attached. Write two things on the first evening.

### The ordered cut list

For each task below the line, write one line: what the player loses, and what else depends on it. For *Lantern*:

| Cut task | What the player loses | Depends on it |
|---|---|---|
| 12 Moth swarm | A second threat that turns the light from a timer into a risk | Nothing |
| 13 Levels 2 and 3 | Length; the game is one level | 16 (a best-time board needs more than one level to matter) |
| 14 Music | Mood | Nothing |
| 15 Particles and shake | Feel on death and pickups | Nothing |
| 16 Best-time board | Replay reason | 13 |

The dependency column stops a classic late-jam mistake: cutting a task, then discovering at hour 46 that something you kept doesn't work without it.

### Cut triggers

A **cut trigger** is a rule, agreed in advance, that fires at a fixed checkpoint. Write triggers as "at hour X, if Y is not true, we do Z." For a 48-hour jam with checkpoints every 12 hours:

- **Hour 12:** if the MVP loop is not playable in a build, stop all slice work. Everyone works on MVP tasks until it is.
- **Hour 24:** re-estimate everything left. Re-run the cut line with the new numbers. If the MVP plus slice doesn't fit in the remaining capacity with a 25% buffer, cut from the bottom of the slice tier and write down what you cut.
- **Hour 36:** **feature freeze.** No new tasks enter. Only tasks already in progress get finished.
- **Hour 42:** **content lock.** From here, only bug fixes and the build. Week 13 covers build and release checklists in detail.

The triggers take the argument out of the decision. At hour 24 nobody has to say "I think we should drop your level." The rule says re-run the line, and the line says where the cut falls.

### Scope creep, and one-in-one-out

**Scope creep** is new work entering the plan without anything leaving. In a jam it arrives as "wouldn't it be cool if...", usually around hour 20 when the MVP works and everyone is excited. The rule that handles it is **one in, one out**. A new idea gets an estimate and a tier. If it goes above the cut line, tasks at least as large as its estimate drop below. Otherwise it goes on the cut list. Nobody is told no. The idea just joins the queue with a price on it.

## In-class activity (25 minutes)

In your jam team of four, with laptops and the interactive open.

1. **(5 min)** Write your game's MVP sentence using the template from section 3. Map each bracket to at least one task.
2. **(10 min)** List 12 to 20 tasks, estimate each in team-hours, and assign a tier. Put them in the order you would build them. Don't discuss the order yet; just write it.
3. **(5 min)** Compute `C` from your lab 01 charter (your team's `c` and `H = 30`), set `b = 0.25`, and find `P`, the cut line and `S_MVP`. Enter the list into the interactive's custom mode and check your numbers.
4. **(5 min)** Swap lists with a neighbouring team. Find the overrun `m` at which their plan stops producing a playable game. Suggest one change of order that raises it.

Expected output: an MVP sentence, a task table with running totals and a marked cut line, the value of `m_max`, and the other team's suggestion.

## Common misconceptions

- **"The MVP is a rough version of the whole game."** It's a *complete* version of the smallest game. Rough is fine. Incomplete is not. A game that has every system at 50% and no win state is not an MVP.
- **"A bigger buffer means we're being lazy."** The buffer is a planned place for work you haven't discovered yet. Unused buffer isn't lost. It pulls tasks back from the cut list in order.
- **"We'll cut when we need to."** Teams that cut when they feel they need to cut late and cut the wrong things. Triggers at fixed hours cut early, and the ordered list decides what goes.
- **"Vertical slice means a demo."** A demo can be faked. A slice is built through the real pipeline, and its purpose is to measure what the rest of the game will cost.

## Check yourself

1. A team of three has `C = 60` team-hours and chooses `b = 0.2`. Their MVP tasks, in build order, total 30 hours and come first. What is `P`, and what overrun `m_max` does the plan survive?
2. In *Lantern*, the team moves task 13 (levels 2 and 3, 12 hours) to position 6, straight after the MVP. Compute the new cut line with `P = 63`. Which slice tasks fall below it? Has `m_max` changed?
3. A team's system-order plan has the MVP complete at `S_MVP = 70` with `C = 84`. How long can their estimates run before they have nothing playable? What one move fixes it without dropping any task?
4. At hour 24, *Lantern*'s team re-estimates: 40 real hours of capacity remain, tasks 6 to 10 still need 29 hours, and nothing else is done beyond the MVP. With a 25% buffer on what remains, which slice tasks survive?

<details>
<summary>Answers</summary>

1. `P = 0.8 × 60 = 48` hours. `m_max = 60 / 30 = 2.0`. The plan survives estimates that run up to twice as long.
2. The running totals become 24, 36 (levels 2 and 3), 44 (task 6), 49 (task 7), 53 (task 8), 58 (task 9), 65 (task 10). The line falls after task 9 at 58 hours. Task 10 (dressing level 1) and everything after drop below the line. The team now has three graybox levels and no finished-looking level at all, so no vertical slice. `m_max` is still `84 / 24 = 3.5`, because the MVP didn't move. The cost of the change is the slice, not safety.
3. `m_max = 84 / 70 = 1.2`. Estimates can run only 20% long. Move the MVP tasks to the front of the build order. The total work is unchanged, `S_MVP` drops to the MVP's own total, and `m_max` rises accordingly.
4. Plannable hours are `0.75 × 40 = 30`. Tasks 6 to 10 need 29, which fits, so the whole slice survives, with 1 hour of plannable slack and 10 hours of buffer. Nothing from the polish tier makes it in unless the buffer goes unused. Task 11 (4 hours) is the first to pull back.

</details>

## Lab / assignment hook

[Lab 04, the jam scope sheet](../labs/lab04.md). Your team writes the one-pager for your jam concept with an MVP sentence, a prioritized task list with estimates, the cut line, the cut list with dependencies, and four cut triggers. You check `m_max` for your build order and for a system-by-system order, and you build the MVP of your one-screen prototype from lab 01. The scope sheet is reused in week 6 (estimates) and during the week 8 jam.

## Sources

- Wikipedia, "Celeste (video game)" (accessed September 2026). The PICO-8 version made by Maddy Thorson and Noel Berry in August 2015 over a few days (the article gives both "a weekend" and "three days"); full release on PC, Switch and PS4 on 25 January 2018; the full game divided into single-screen challenges with checkpoints between screens.
- Wikipedia, "PICO-8" (accessed September 2026). 128 × 128 pixel, 16-color display and 4-channel audio.
- Wikipedia, "Surgeon Simulator" (accessed September 2026). Initial version made by Tom Jackson, Jack Good, Luke Williams and James Broadley in 48 hours at the 2013 Global Game Jam; 48 days to the commercial version; Steam release April 2013; iPad release 7 March 2014 with heart, kidney, eye and teeth transplants.
- Wikipedia, "Baba Is You" and "Nordic Game Jam" (accessed September 2026). Built for the 2017 Nordic Game Jam (theme "Not There"), won first place; full release 13 March 2019. The Nordic Game Jam gives participants around 40 hours.
- Warcraft Wiki, "Dance Studio" (warcraft.wiki.gg, accessed September 2026). Announced at BlizzCon 2007 for *Wrath of the Lich King*; staff statements on postponement in October 2008, January 2009 and April 2009; Greg Street's August 2013 description of it as shelved, not cancelled.
- Wikipedia, "MoSCoW method" (accessed September 2026). Developed by Dai Clegg in 1994; used with timeboxing; adopted by DSDM.
- Wikipedia, "Vertical slice" (accessed September 2026). Definition as a milestone demonstrating progress across all components.
- Ries, E. (2011). *The Lean Startup*. Crown Business. Origin of the popular use of "minimum viable product".
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley.

## Interactive spec: examples/w04-cut-line.html

**The one insight.** Two plans with the same tasks and the same estimates can have very different safety. What decides it is how early in the build order the MVP is finished. When estimates run long, the vertical order loses polish; the system order loses the game.

**Layout.** Two linked views, stacked on mobile (top view first), side by side above 900px.

1. **Top view, the build bar.** A horizontal bar whose length represents `C` team-hours (default 84). Tasks are drawn as blocks laid end to end in build order, each block's width equal to `e_i × m` (estimate times the current overrun). Color by tier: MVP, Slice, Polish (use three palette colors from `templates/interactive-tokens.css`; also mark MVP blocks with a small solid square icon and polish with a hollow one, so tier is not color-only). Draw a dashed vertical line at `P = (1 − b) × C` labelled "plan limit P", and a solid line at `C` labelled "time's up". Blocks that end beyond `C` are drawn faded and hatched, with the part beyond `C` clipped. A marker labelled "MVP playable" sits at the point in the bar where the last MVP block ends; if that point is beyond `C`, show the marker in red past the end with the text "no playable game".
   Below the bar, a list of the tasks in order (number, name, tier, estimate, running total `S_k`) with a horizontal rule at the cut line. Each row has up and down buttons to reorder (keyboard: focus a row, Alt+Up/Alt+Down).
2. **Bottom view, the safety chart.** x-axis overrun `m` from 1.0 to 4.0. Two horizontal step strips, one per build order ("Your order", "By system"). Each strip is green (pattern: solid) where the MVP finishes within `C` and grey-hatched where it does not. Mark `m_max = C / S_MVP` on each strip with a labelled tick. A vertical line shows the current `m` from the slider.

**Controls.**
- Overrun `m` slider: 1.0 to 4.0, step 0.05, default 1.0.
- Buffer `b` slider: 0 to 0.5, step 0.05, default 0.25.
- Capacity `C` number input: 20 to 200, default 84.
- Build order toggle: "Vertical (as listed)" / "By system (P, E, L, then U and A)" / "Custom" (custom becomes active when the user reorders rows).
- Reset button restores the *Lantern* list and defaults.
- "Custom list" mode: a textarea accepting CSV lines `name,system,tier,estimate`, replacing the list.

**Readouts, always visible next to the views.** `P`, planned hours (sum above the cut line), cut-list hours, `S_MVP`, `m_max` for the current order, `m_max` for the system order, and "At m = X: finished tasks 1-k; playable: yes/no".

**Formulas.**
- `P = (1 − b) × C`.
- Cut line: walk the list in order, accumulating `e_i`; the cut line is after the last task where the running total ≤ `P`. Stop at the first task that would exceed `P` (do not skip ahead).
- Finished at overrun `m`: walk in order accumulating `e_i × m`; a task is finished if the running total ≤ `C` (use a tolerance of 1e-9); the first task past `C` is partial, with `(C − previous total) / m` estimated hours done.
- `S_MVP`: running total of `e_i` (unscaled) at the position where every MVP task has appeared. `m_max = C / S_MVP`.
- System order: all P tasks in list order, then all E tasks, then all L tasks, then all U and A tasks together in list order. For the default list this gives 1, 2, 6, 11, 3, 7, 12, 4, 10, 13, 5, 8, 9, 14, 15, 16.

**Default data (Lantern).** `(1, Player run and jump, P, MVP, 6) (2, Lantern drains light radius shrinks, P, MVP, 4) (3, One hazard that kills on touch, E, MVP, 4) (4, One graybox level start to exit, L, MVP, 6) (5, Win lose and restart loop, U, MVP, 4) (6, Player sprite and animations, P, Slice, 8) (7, Hazard art and death feedback, E, Slice, 5) (8, Three sounds, A, Slice, 4) (9, Title screen and how-to-play, U, Slice, 5) (10, Level 1 dressed in final tiles, L, Slice, 7) (11, Oil pickups refill lantern, P, Polish, 4) (12, Second hazard moth swarm, E, Polish, 8) (13, Levels 2 and 3, L, Polish, 12) (14, Music loop, A, Polish, 6) (15, Particles and screen shake, A, Polish, 5) (16, Best-time board, U, Polish, 5)`.

**Test values (must match the lecture).**
- Defaults: `P = 63`, cut line after task 11, planned 57 h, cut list 36 h, `S_MVP = 24`, `m_max = 3.5`; system order `S_MVP = 68`, `m_max = 1.24` (84/68 = 1.235, display 2 decimals), system-order plan = tasks 1, 2, 6, 11, 3, 7, 12, 4, 10 (52 h), no task 5.
- `m = 1.5`: vertical finishes 1-10, task 11 partial with 3.0 estimated hours done, playable yes; system finishes 1, 2, 6, 11, 3, 7, 12, 4, 10, task 13 partial with 4.0 done, playable no.
- `m = 2.0`: vertical finishes 1-8, playable yes; system finishes 1, 2, 6, 11, 3, 7, 12, playable no.
- `m = 3.0`: vertical finishes 1-5 exactly, playable yes.
- Check-yourself 2: moving task 13 to position 6 gives a cut line after task 9 at 58 h.

**Accessibility and style.** Keyboard reorder as above; sliders are native range inputs with visible values; the strip states use pattern as well as color; respects `prefers-reduced-motion` (no block slide animation) and `prefers-color-scheme`. No game art; blocks are plain rectangles with task names.
