# PR101 · Week 05 — Agile and Scrum Adapted for Games

**Why this matters:** A team can meet every day for years and still not know whether its game is fun. The meetings are not the point. The point is how often the team plays a working build and changes course because of it. Scrum is one way to force that to happen on a schedule, and this week you learn how to set that schedule for a semester project and for a 48-hour jam.

**You will be able to:**
- Describe Scrum's accountabilities, events and artifacts, and map each one to a small game team.
- Compute the sprint length that minimizes overhead plus wasted work, and explain why it grows with the square root of the overhead.
- Adapt Scrum for game development: playable increments, pre-production versus production sprints, and content work that doesn't fit a sprint.
- Run a standup and a retrospective that each end in a decision.

**Before class:** The Scrum Guide (Schwaber and Sutherland, November 2020 edition, free at scrumguides.org, about 14 pages). The Manifesto for Agile Software Development (one page, agilemanifesto.org). Clinton Keith, *Agile Game Development* (2nd ed., 2020), the chapters on Scrum and on agile across pre-production and production (about 40 pages).

**Prerequisites from earlier courses:** [PR101 week 1, team capacity](w01-roles-on-a-game-team.md) (this week's `W` is week 1's useful capacity). [PR101 week 4, scope and cut lists](w04-scope-mvp-vertical-slice-cut-lists.md) (sprint planning is the cut line applied to one sprint). [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (why short loops give more chances at a keeper; this week prices each loop). [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (the `1/L` curve in the cost model).

**Interactive:** [examples/w05-sprint-length.html](../examples/w05-sprint-length.html). Keep it open during section 2.

---

## 1. From a manifesto to a framework

### The manifesto

In February 2001, seventeen software developers met at a ski resort in Snowbird, Utah. Several of them had invented their own "lightweight" methods, including Extreme Programming and Scrum. They agreed on a one-page statement, the Manifesto for Agile Software Development. It sets four preferences. The team values people talking to each other over processes and tools, working software over complete documentation, working with the customer over negotiating contracts, and responding to change over following a plan. The manifesto says the items on the right still have value; it just ranks the left side higher.

For games, translate "working software" into **a playable build**. Almost everything in this lecture follows from taking that phrase seriously. A design document that says the combat is fun is a claim. A build where a stranger laughs at the combat is evidence.

**Agile** is the family of methods that share those values. **Scrum** is the most common specific framework in that family, and the one most game studios mean when they say "we're agile".

### Scrum in one page

The Scrum Guide (2020 edition) describes a small team, typically 10 or fewer people, working in fixed-length cycles called **sprints**. Each sprint is one month or less. Here's what is in the framework, with the jam-team version beside it.

**Three accountabilities.**

| Accountability | What the guide says it's for | On your team of four |
|---|---|---|
| Product Owner | Maximizing the value of the product; owns and orders the Product Backlog | The person your charter names as tie-breaker for "what goes in the game" |
| Scrum Master | Making Scrum work: removing blockers, keeping events on time | Your producer from week 1, 10 to 20 percent of their time |
| Developers | Building a usable increment every sprint | Everyone, including the two people above |

**Three artifacts, each with a commitment.**

| Artifact | What it is | Its commitment |
|---|---|---|
| Product Backlog | The ordered list of everything the game might need | Product Goal: the long-term objective |
| Sprint Backlog | The tasks picked for this sprint, plus the plan to do them | Sprint Goal: one objective for this sprint |
| Increment | The working result, added to everything done before | Definition of Done: the checklist a piece of work must pass to count |

Week 4's prioritized task list *is* a product backlog. The cut line is how you pick a sprint backlog from it. Week 7 covers the Definition of Done in detail.

**Five events.** The guide sets maximum lengths ("timeboxes") for a one-month sprint and says they are usually shorter for shorter sprints.

| Event | Purpose | Max for a one-month sprint |
|---|---|---|
| Sprint | The container for everything else | One month |
| Sprint Planning | Pick the Sprint Goal and the work | 8 hours |
| Daily Scrum | Inspect progress toward the Sprint Goal and adjust the plan | 15 minutes |
| Sprint Review | Inspect the increment with stakeholders and decide what to change | 4 hours |
| Sprint Retrospective | Inspect how the team worked and pick improvements | 3 hours |

The guide describes the Sprint Review as a working session, not a presentation. For a game team that means people play the build. A review where the team shows slides about progress has skipped the only part that produces evidence.

That's the whole framework. It's short on purpose. It says what must happen, and it leaves out almost everything about *how* long a sprint should be, beyond "a month or less". The next section works that out.

## 2. Worked example: how long should a sprint be?

### The hook

BioWare began work on *Anthem* in 2012, after *Mass Effect 3*. The game released on 22 February 2019. Staff who spoke anonymously to *Kotaku* for its April 2019 report said the game spent years in pre-production and did not enter production until its final 18 months. One said the core loop, the story and the missions were made in the last 12 to 16 months. The flying mechanic, which critics later praised, had been added and removed several times during development. It went back in for good when the team spent six weeks building a demo for an EA executive's visit in spring 2017, and he was particularly impressed by the flying.

Think about what that timeline means. For years the team was working, meeting and producing. What it lacked was a regular moment where a playable build answered a question and the answer stuck. When that moment finally came, it changed the game within weeks. The question for a production course is how often that moment should come, and what it costs each time.

This worked example gives you a number. It also shows why "as often as possible" is the wrong answer.

### The model

Picture work between two reviews. Every hour the team builds, it builds on assumptions: this jump feels good, this enemy is readable, players will understand the light meter. Some of those assumptions are wrong, and you don't find out until someone plays a build. Everything built on a wrong assumption since the last review has to be redone. Call it **wasted work**.

Reviews cost something too. Each sprint needs a build that actually runs, a planning session, a review where people play, and a retrospective. Call that the **overhead** per sprint.

Short sprints mean lots of overhead and little waste. Long sprints mean little overhead and lots of waste. Put numbers on both:

```
overhead per week   = h / L
waste per week      = λ × W × L / 2
cost per week  C(L) = h / L  +  λ × W × L / 2
best sprint length  L* = √( 2h / (λW) )
```

- `L` is the sprint length in weeks (or hours, in a jam).
- `h` is the overhead of one sprint in team-hours: making a stable build, planning, review, retrospective. Only count the part that doesn't shrink when the sprint gets shorter.
- `W` is the team's useful capacity in team-hours per week, from week 1's channel model.
- `λ` (lambda) is the **wrong-turn rate**, the average number of times per week the team starts building on an assumption that a playtest would reject.
- `C(L)` is the total cost in team-hours per week.

Where does `L / 2` come from? A wrong turn can happen at any moment in the sprint. On average it happens halfway through, so on average half a sprint's work is built on it before the review catches it. Each wrong turn wastes about `W × L / 2` team-hours, and there are `λ × L` wrong turns per sprint. Divide the sprint's waste by `L` to get waste per week, and you get `λ × W × L / 2`.

**Why the best `L` sits where the two costs are equal.** Write the cost as `a / L + b × L` with `a = h` and `b = λW / 2`. For any positive numbers, `(√(a/L) − √(bL))² ≥ 0`. Expand the square and you get `a / L + bL ≥ 2√(ab)`, with equality only when `a / L = bL`. So the cost is smallest exactly when overhead per week equals waste per week. Solve `h / L = λWL / 2` and you get `L* = √(2h / (λW))`.

That square root is the whole lesson. **Halving your overhead doesn't halve your sprint length. It shortens it by about 29%** (because `√0.5 ≈ 0.71`). And the cost curve is flat near the bottom, so being a little off the best length costs little, while being far off costs a lot.

### Numbers you can check

Use the semester team from week 1: four people, 10 hours each per week, `c = 0.5`, so `W = 34` useful team-hours per week. Say a sprint's fixed overhead is 1.5 hours per person (half an hour to get a clean build, and an hour for planning, review and retrospective), so `h = 6` team-hours.

Now two phases. In **pre-production**, you're still finding the fun, so wrong turns are common. Say `λ = 0.5`, one every two weeks. In **production**, the core is proven and you're building content on it. Say `λ = 0.1`, one every ten weeks.

| Sprint length L | Overhead h/L | Pre-production waste (λ = 0.5) | Pre-production total | Production waste (λ = 0.1) | Production total |
|---|---|---|---|---|---|
| 0.5 week | 12.0 | 4.25 | 16.25 | 0.85 | 12.85 |
| 1 week | 6.0 | 8.5 | **14.5** | 1.7 | 7.7 |
| 2 weeks | 3.0 | 17.0 | 20.0 | 3.4 | **6.4** |
| 4 weeks | 1.5 | 34.0 | 35.5 | 6.8 | 8.3 |

The formula gives:

```
pre-production: L* = √(2 × 6 / (0.5 × 34)) = √0.706 ≈ 0.84 weeks, C ≈ 14.3 h/week
production:     L* = √(2 × 6 / (0.1 × 34)) = √3.53  ≈ 1.88 weeks, C ≈ 6.4 h/week
```

Check one cell by hand. Pre-production, 2-week sprints: overhead `6 / 2 = 3`, waste `0.5 × 34 × 2 / 2 = 17`, total 20 team-hours per week. That's 20 of your 34 hours gone, most of it to rework.

Three things to read off the table.

1. **One-week sprints in pre-production, two-week sprints in production.** The same team, with the same overhead, should change sprint length when its wrong-turn rate changes.
2. **Monthly sprints in pre-production are a disaster.** At `L = 4`, expected waste per week equals the team's entire capacity. The model is telling you that almost everything built between reviews gets redone. That's the *Anthem* pattern: long stretches between moments where a playable build settles a question.
3. **Very short sprints lose too.** Half-week sprints in production spend 12 of 34 hours on overhead. Teams that "review constantly" without a cheap build process pay for it here.

### A jam, in hours

The same model works in a 48-hour jam if you measure in hours. With four people working, `W = 4` team-hours per working hour. Stopping everyone for 20 minutes to make a build and play it costs `h = 4 × 1/3 ≈ 1.33` team-hours. Jams are all pre-production, so wrong turns are frequent. Say one every five working hours, `λ = 0.2` per hour.

```
L* = √(2 × 1.33 / (0.2 × 4)) = √3.33 ≈ 1.8 working hours
```

A playable build roughly every two working hours. That's why experienced jam teams build and play constantly, while first-time teams often play their game for the first time on the second morning.

### Move it yourself

Open the interactive. The left view plots the two cost curves and their sum against sprint length. The overhead curve falls, the waste line rises, and a marker sits at the minimum. The right view is a timeline of one term: sprints drawn as blocks, wrong turns as red ticks at random moments, and the wasted work after each tick shaded until the next review. Drag `L` and watch the shaded area grow on the right while the overhead stripes thin out. Then drag `h` down, as if you'd automated your build. The best `L` moves left, but slower than you'd expect. Switch the phase toggle from pre-production to production and watch `L*` roughly double.

### Cross-game recognition

This `√(2 × cost / rate)` shape turns up wherever something is saved or checked at intervals and failures arrive at random. Once you see it, you'll recognize it in engines, levels and servers.

**Checkpointing long computations (Young, 1974).** A long computer job saves its state every `T` time units, taking `δ` each time. When the machine fails (on average once every `M` time units), the work since the last save is lost. John Young's 1974 paper gives the best interval as roughly `T = √(2δM)`. Rewrite our model with `δ = h / W` (overhead measured in weeks of team time) and `M = 1 / λ` (weeks between wrong turns). Then `L* = √(2h / (λW)) = √(2δM)`. It's the same formula. A sprint review is a checkpoint for decisions.

**Checkpoints in a level (Celeste, 2018).** A level designer placing respawn points faces the same trade. Each checkpoint costs something: it interrupts tension, and it can make a section trivial. Each death costs the player replaying everything since the last checkpoint, on average half the gap. The more often players die (high `λ`), the closer checkpoints should sit. *Celeste*, a game about dying often, splits its chapters into single-screen challenges with a checkpoint between screens, so each death costs a few seconds. A game where deaths are rare can afford long gaps. The designer is solving `√(2 × cost / rate)` by feel.

**Save intervals on a game server (DB201, year 2).** A server that saves player state every `T` seconds pays for each write, and a crash loses the progress since the last save. [DB201 week 8](../../DB201-data-persistence-and-telemetry/lectures/w08-caching-and-write-behind.md) builds this model for write-behind caches. The expected loss is again half the interval.

**Ordering stock (Harris, 1913).** The oldest version is the economic order quantity. A shop that orders in large batches pays less in ordering fees and more in storage. Ford Harris's 1913 formula puts the best batch size at a square root of fee over storage cost, the same balance of a per-event cost against a cost that grows with the interval.

Four settings, one equation. A cost you pay every cycle, a loss that grows with the length of the cycle, and a best cycle length at the square root of their ratio.

### Eyes-open design judgment

The model is useful because it shows which numbers to change. Use it with its limits in view.

- **The review has to catch the mistake.** `L` is the time between moments where people *play* a build and *decide* something. A review with slides, or a playtest nobody acts on, doesn't reset the clock. Your effective `L` is the gap between real decisions, however many meetings happen in between.
- **Cut `h` before you shorten `L`.** An automated build, a playtest script and a 15-minute review template all lower `h`. Because of the square root, a team that cuts overhead from 6 to 1.5 team-hours can halve its sprint length at the same total cost. Week 13 covers builds and release checklists, which is where most of `h` hides.
- **`λ` is a guess, and that's all right.** You can't measure the wrong-turn rate precisely. You can count, after each review, how many things you decided to redo. Two or three sprints of counts give you a usable number. Lab 05 has you do exactly that.
- **Keep the rhythm stable within a phase.** Changing sprint length every sprint makes it impossible to compare one sprint's output to the next. Change it when the phase changes (pre-production to production), not because one sprint went badly.
- **The model ignores morale.** Very short sprints can feel like constant inspection. Very long ones can feel like drifting. Neither shows up in `C(L)`, but both show up in your retrospectives.

This is a different question from GD101 week 8's. That model counted how many loops fit in a schedule and the chance that one of them produces a keeper. This one prices each loop: what a review costs, and what it saves.

## 3. Scrum adapted for games

Scrum came from general software development. Games differ in ways that matter, and every studio that uses Scrum bends it in similar places.

### The increment must be playable

In a business application, a sprint might deliver a working login page. It's usable even if nothing else is finished. In a game, a finished inventory screen with no game around it tells you nothing about fun. So the game version of the rule is stricter: **every sprint ends with a build someone outside the team can play.** It might be one mechanic in a gray room. It must run, and it must be played at the review.

This is why week 4 put the MVP first. A vertical build order gives you a playable increment from the first sprint. A system-by-system order gives you a stack of parts that nobody can play until late, and a Sprint Review with nothing to inspect.

### Pre-production is for questions, production is for content

In 2002, Mark Cerny described what became known as "the Method", which he developed while consulting for Sony's first-party studios, including Naughty Dog and Insomniac. Its core idea is that pre-production and production need different rules. Pre-production is open-ended exploration and can't be scheduled precisely. It ends when the team has a **publishable first playable**, a build that is not content-complete but good enough to test with players and decide whether the game deserves full production. Production, after that point, can be planned and scheduled.

Scrum fits both phases if you change the sprint goal.

| | Pre-production sprint | Production sprint |
|---|---|---|
| Sprint Goal | A question: "Is grappling more fun than double-jumping?" | A deliverable: "Levels 3 and 4 dressed and playable" |
| Done means | The question is answered by a playtest, and the answer is written down | The content passes the Definition of Done |
| Typical length (from section 2) | Short, because `λ` is high | Longer, because `λ` is low |
| Failure looks like | Building content on an unanswered question | Reopening a settled question without new evidence |

A pre-production sprint can succeed with the answer "no, grappling is worse." That's a result. The failure is not finding out.

### Content doesn't fit neatly into sprints

Art, animation, audio and level dressing often move through a pipeline of stages: concept, model, texture, rig, animate, import, review. One asset might take three weeks through all stages, and each stage is done by a different person. Forcing each asset to start and finish inside one sprint either breaks it into meaningless pieces or leaves it half-finished at every review.

Many game teams run content through a **Kanban** board instead: columns for each stage, cards that move across, and a limit on how many cards each column may hold at once (a **work-in-progress limit**). The code and design side runs sprints; the content side flows. They meet at the Sprint Review, where whatever content has reached "in the build" gets played. Week 7 builds the board.

### Cross-discipline teams

Week 1 showed that sub-teams cut coordination channels. The obvious way to split a larger team is by discipline: programmers together, artists together. Scrum pushes the other way, toward **cross-discipline teams** that can each deliver a playable feature alone. A "combat team" with a designer, two programmers, an animator and a sound designer can finish a combat feature within a sprint without waiting for anyone. A "programming team" can't finish anything a player would notice without the art team. The channel count may be the same; what changes is whether the channels cross a team boundary.

For your team of four, this means every sprint goal should need everyone. If the artist has nothing to do with this sprint's goal, the goal is too narrow.

### The product owner on a student team

In a studio, the product owner is often a lead designer or producer with authority to order the backlog. On a student team there's no boss, so your charter's tie-breaker rule does the job. Two things matter more than who holds it. First, one person orders the backlog, so there is one list with one top item. Second, that person can say "not this sprint" without a debate. That's the cut line, applied every sprint.

## 4. Scrum in a 48-hour jam

Scrum's vocabulary sounds heavy for a weekend. Its structure fits well if you shrink the units.

- **The product backlog** is your week 4 task list, ordered, with the cut line drawn.
- **Sprints** are the two-hour build cycles from section 2. Each ends with everyone playing the current build for a few minutes. That's your Sprint Review.
- **Sprint planning** happens at the four checkpoints from week 4's cut triggers (hours 12, 24, 36 and 42), where you re-estimate and redraw the line. Between checkpoints, each two-hour cycle just takes the next items from the top.
- **Daily Scrums** become check-ins at each checkpoint and after every sleep. Five minutes, standing, next to the build.
- **The retrospective** is week 9's jam post-mortem.

There's one jam-specific rule. **The build must always run.** If a change breaks the build, fixing it comes before any new work, because a broken build sets your effective `L` to infinity. Nobody can play anything until it's fixed. Week 2's branching workflow is what makes this rule affordable.

## 5. Standups and retrospectives that end in decisions

### The daily standup

The Daily Scrum is a 15-minute event where the developers check progress toward the Sprint Goal and adjust the plan. Many teams use three questions: what did I finish since last time, what will I finish next, and what's blocking me? The 2020 Scrum Guide no longer requires those questions, and you can drop them if they turn into status reports. Two rules keep a standup useful whatever format you use.

1. **Talk about the goal, not about effort.** "I worked on the player controller" is effort. "The double jump is in the build; wall-jump is next; I'm blocked on the collision layer" moves the goal.
2. **Solve problems after, not during.** When a blocker comes up, name the two people who'll fix it and move on. They talk after the standup. Everyone else goes back to work.

A standup that ends without changing anything is fine most days. A standup that never changes anything is a status meeting.

### The retrospective

The retrospective looks at *how* the team worked. One format that works for small teams is **start, stop, continue**. Each person writes, silently for three minutes, things the team should start doing, stop doing, and keep doing. Group the notes, vote, and pick **one** change for next sprint, with an owner and a way to tell whether it happened.

The most common retrospective failure is picking five improvements and doing none. The second most common is picking improvements nobody can check ("communicate better"). "Post every decision in the team channel within an hour; Ana checks on Friday" is a change you can check. Week 11 goes deeper on team conflict, and week 14 on post-mortems, which are retrospectives for a whole project.

## In-class activity (25 minutes)

In your team of four, with the interactive open.

1. **(5 min) Estimate `h`.** List everything your team would have to do to end a sprint: make a build, get it onto a second machine, playtest, plan, retrospective. Put a time per person on each. Sum to team-hours.
2. **(5 min) Estimate `λ`.** Look back at your GD101 prototype or your week 4 plan. How many times in the last month did a playtest make you redo work? Convert to a rate per week. Do it once for "now" and once for "after the core is proven".
3. **(5 min) Compute `L*`.** Use `W` from your lab 01 charter. Compute `L*` for both phases and check it in the interactive. Then halve `h` and recompute.
4. **(10 min) Plan your jam cycle.** Using `W = 4` team-hours per hour and your own guesses, compute a jam `L*`. Write a one-line jam schedule: check-in times, build-and-play times, and who runs each.

Expected output: your `h`, your two `λ` values, three `L*` values (pre-production, production, jam) and a jam schedule on one index card.

## Common misconceptions

- **"Agile means no planning."** Scrum plans every sprint and keeps an ordered backlog for the whole project. What it drops is the pretence that a plan made at the start will survive unchanged.
- **"Shorter sprints are always better."** Only while overhead is cheap. Past `L*`, each extra review costs more than it saves. Cut overhead first, then shorten.
- **"The Sprint Review is a demo for the teacher."** It's where the team plays the build and changes the backlog because of what it learned. If nothing in the backlog changes after a review, you did a demo.
- **"Scrum doesn't work for art."** Sprint-sized chunks often don't fit an art pipeline. Many teams run content on a Kanban flow and meet the sprint rhythm at the review, which is still agile.

## Check yourself

1. A team has `W = 40` team-hours per week, overhead `h = 5` team-hours per sprint, and a wrong-turn rate `λ = 0.25` per week. Compute `L*` and the weekly cost `C(L*)`. Check that overhead and waste are equal at `L*`.
2. The same team automates its build and cuts `h` to 1.25. By what factor does `L*` change? Why isn't it a factor of 4?
3. A studio runs four-week sprints through pre-production with `λ = 0.5` per week and `W = 34`. Using the section 2 model, what fraction of the team's capacity is expected waste? What would you change first, and why?
4. A jam team of three (`W = 3` per hour) takes 30 minutes each to make and play a build (`h = 1.5`). Wrong turns happen about once every four hours (`λ = 0.25`). How often should they build and play?
5. A team's pre-production sprint goal is "implement grappling hook". Rewrite it as a pre-production goal, and say what "done" means for it.

<details>
<summary>Answers</summary>

1. `L* = √(2 × 5 / (0.25 × 40)) = √(10 / 10) = 1` week. Overhead `5 / 1 = 5`; waste `0.25 × 40 × 1 / 2 = 5`. They're equal, and `C = 10` team-hours per week.
2. `L* = √(2 × 1.25 / 10) = √0.25 = 0.5` weeks, so it halves. The overhead went down by a factor of 4, and `L*` goes with its square root, `√4 = 2`. The new cost is `1.25 / 0.5 + 0.25 × 40 × 0.5 / 2 = 2.5 + 2.5 = 5` team-hours per week, half the old cost.
3. Waste per week is `0.5 × 34 × 4 / 2 = 34`, which is 100% of capacity. In practice it means almost everything built between reviews gets redone. Shorten the sprint first: `L*` is under a week for this team. Also check that reviews involve playing the build, since otherwise the effective `L` is even longer than four weeks.
4. `L* = √(2 × 1.5 / (0.25 × 3)) = √4 = 2` working hours. Build and play every two working hours.
5. For example, "Find out whether grappling or double-jumping makes the first room more fun, by testing both with three players." Done means the playtest happened and the team wrote down the decision and the evidence. Building a polished grappling hook is not required, and the sprint succeeds even if the answer is "double-jump".

</details>

## Lab / assignment hook

[Lab 05, one sprint, measured](../labs/lab05.md). Your team runs a one-week sprint on the week 4 prototype with a written sprint goal, three logged standups, a review where outsiders play the build, and a start-stop-continue retrospective. You time every piece of overhead to measure your real `h`, count your wrong turns to estimate `λ`, and compute the sprint length you'll use for the next two sprints and the jam cycle for week 8.

## Sources

- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. scrumguides.org. Sprints of one month or less; team typically 10 or fewer; accountabilities, artifacts and commitments; event timeboxes of 8 hours (planning), 15 minutes (Daily Scrum), 4 hours (review) and 3 hours (retrospective) for a one-month sprint, usually shorter for shorter sprints; the Sprint Review as a working session.
- Manifesto for Agile Software Development (2001), agilemanifesto.org; and Wikipedia, "Agile software development" (accessed September 2026). Seventeen practitioners at Snowbird, Utah, in 2001; the four value statements.
- Schreier, J., "How BioWare's Anthem Went Wrong", *Kotaku*, 2 April 2019 (read September 2026). Work from late 2012; production only in the final 18 months; core loop, story and missions made in the last 12 to 16 months; flying added and removed several times; the six-week demo for Patrick Söderlund's spring 2017 visit and his enthusiasm for the flying in it. Release date 22 February 2019 from Wikipedia, "Anthem (video game)" (accessed September 2026).
- Wikipedia, "Mark Cerny" (accessed September 2026), section "The Method process". Established in 2002 while consulting for Naughty Dog, Insomniac and other Sony first-party studios; freeform pre-production ending in a "publishable first playable".
- Young, J. W. (1974). A first order approximation to the optimum checkpoint interval. *Communications of the ACM*, 17(9), 530-531.
- Wikipedia, "Economic order quantity" (accessed September 2026). Developed by Ford W. Harris in 1913.
- Wikipedia, "Celeste (video game)" (accessed September 2026). Chapters divided into single-screen challenges with checkpoints between screens (2018 release).
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. First edition 2010 as *Agile Game Development with Scrum*.

## Interactive spec: examples/w05-sprint-length.html

**The one insight.** Sprint length trades overhead against wasted work, and the best length is where the two are equal. Because `L* = √(2h / (λW))`, cutting overhead shortens the best sprint less than you expect, and a high wrong-turn rate (pre-production) makes long sprints very expensive.

**Layout.** Two linked views: side by side above 900px, stacked below (cost chart first).

1. **Left view, cost curves.** x-axis sprint length `L` from 0.25 to 6 (units follow the mode: weeks or hours). y-axis team-hours per week (or per hour in jam mode). Three curves: overhead `h/L` (falling, dashed), waste `λWL/2` (rising straight line, dotted), total `C(L)` (solid, thicker). A filled marker at `(L*, C(L*))` labelled with both values. A vertical line at the current `L` with a readout box showing overhead, waste and total at that `L`, and the total as a percentage of `W`. Clip the y-axis at `1.2 × W` and draw a horizontal reference line at `W` labelled "all capacity".
2. **Right view, timeline.** A horizontal strip 12 weeks long (or 24 hours in jam mode) divided into sprints of length `L`. Each sprint boundary is drawn as a narrow striped block whose width is proportional to `h / W` (the overhead's share of time). Wrong turns are red ticks placed by a seeded pseudo-random Poisson process with rate `λ` (use a fixed seed so the same settings give the same picture; a "reroll" button changes the seed). From each tick to the next sprint boundary, shade the strip (hatched pattern plus color) to show wasted work. Below the strip, print "Wasted this run: X team-hours (expected: Y)", where `Y = λ × W × L / 2 × T` for a strip of length `T` (12 weeks or 24 hours), and X is computed from the drawn ticks as `W × Σ (time from tick to next boundary)`.

**Controls** (native inputs, values shown, keyboard operable).
- Mode toggle: "Semester (weeks)" / "Jam (hours)".
- `L` slider: 0.25 to 6, step 0.05. Default 2, so the first screen shows a sprint well past `L*` in pre-production.
- `h` slider: 0.5 to 20 team-hours, step 0.25, paired with a number input (step 0.01) for exact values such as the jam's 1.33. Default 6 (semester), 1.33 (jam).
- `λ` slider: 0.02 to 1.0 per week (or per hour), step 0.01. Default 0.5 (semester, pre-production), 0.2 (jam), matching section 2's jam case.
- `W` number input: default 34 (semester), 4 (jam).
- Phase buttons (semester mode only): "Pre-production" sets `λ = 0.5`; "Production" sets `λ = 0.1`.
- Button "Snap to L*" sets `L` to the optimum.
- Reroll button for the timeline seed.

**Formulas.**
- `overhead(L) = h / L`; `waste(L) = λ × W × L / 2`; `C(L) = overhead + waste`.
- `L* = sqrt(2h / (λW))`; `C(L*) = sqrt(2hλW)`.

**Test values (must match the lecture).**
- Semester, `W = 34`, `h = 6`, `λ = 0.5`: `L* = 0.840`, `C(L*) = 14.28`; at `L = 1`: 6.0 + 8.5 = 14.5; at `L = 2`: 3.0 + 17.0 = 20.0; at `L = 4`: 1.5 + 34.0 = 35.5 (104% of W, above the reference line).
- Same with `λ = 0.1`: `L* = 1.879`, `C(L*) = 6.39`; at `L = 0.5`: 12.85; at `L = 2`: 6.4.
- Jam, `W = 4`, `h = 1.33`, `λ = 0.2`: `L* = 1.82` hours (with `h = 4/3` exactly, 1.826).
- Check-yourself 1: `W = 40`, `h = 5`, `λ = 0.25` gives `L* = 1.000`, `C = 10.0`; with `h = 1.25`, `L* = 0.500`, `C = 5.0`.

**Insight on first screen.** Default state is semester pre-production at `L = 2`, so the first view shows the total well above its minimum, with the marker at 0.84 visibly to the left.

**Accessibility and style.** Curves are distinguished by dash pattern as well as color; the waste shading uses a hatch. Respects `prefers-reduced-motion` (no tick animation) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art.
