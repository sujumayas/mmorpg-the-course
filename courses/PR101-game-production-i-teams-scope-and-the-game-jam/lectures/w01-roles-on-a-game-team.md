# PR101 · Week 01 — Roles on a Game Team

**Why this matters:** In week 8 you will make a game in 48 hours with people you met this semester. Most jam teams that fail do not fail on skill. They fail because two people built the same thing, nobody built the menu, or five people spent the first evening agreeing on a name. Knowing who owns what, and how big a team should be, prevents all three.

**You will be able to:**
- Compute the number of communication channels in a team and the coordination cost they add, for any team size.
- Derive the team size that maximizes useful work under the channel-cost model, and explain why jam teams are smaller than semester teams.
- Design a team structure (sub-teams with leads) that cuts channel count, and compute the saving.
- Build a RACI matrix for a small game project and critique one for missing owners and single points of failure.

**Before class:** Clinton Keith, *Agile Game Development* (2nd ed., 2020), the chapter on teams (about 25 pages). Fred Brooks, *The Mythical Man-Month* (1975, anniversary ed. 1995), chapter 2, "The Mythical Man-Month" (about 15 pages). Browse the Global Game Jam site and pick one jam game from any year whose credits list the team.

**Prerequisites from earlier courses:** [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (why short loops matter, which is what small teams buy you). [GD101 week 14, design documents and pitch](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) (the one-pager your team will write in week 4). [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (the engine most of you will use for the jam).

**Interactive:** [examples/w01-team-channels.html](../examples/w01-team-channels.html). Keep it open during section 2.

---

## 1. Jobs first, titles second

A game needs certain jobs done whether one person or three hundred make it. Learn the jobs first. Titles are just names studios give to people who hold a bundle of jobs.

Here are the jobs every project in this course needs, with the title that usually holds each one in a mid-sized studio.

| Job | What "done" looks like | Usual title |
|---|---|---|
| Decide what the game is and how it plays | Rules written down, tuned numbers in a file, a reason for each | Game designer |
| Make it run | Code that builds, runs on the target machine, and does what the design says | Programmer (gameplay, engine, tools, network) |
| Make it look like something | Sprites, models, animation, UI art, imported and working in engine | Artist (concept, 2D, 3D, animation, technical) |
| Make it sound like something | Effects, music and mix hooked to game events | Audio designer, composer |
| Check that it works | Bugs found, written up so someone else can reproduce them, and rechecked after the fix | QA tester |
| Keep the work moving | A list of what's left, who's doing it, what's blocked, and when it ships | Producer |
| Hold the vision | Decides between two good options when the team is split | Creative director, lead designer |

Three of these jobs need a word of explanation because students tend to skip them.

**Producer.** A producer does not "manage" in the sense of telling people what to do. A producer owns the schedule, the task list and the removal of blockers. When the artist can't import a sprite sheet because the programmer hasn't written the loader, the producer notices at the morning check-in and gets the two of them talking before lunch. On a jam team the producer is usually also a designer or programmer who spends 10 to 20 percent of their time on this job. Somebody has to.

**QA.** Quality assurance is the job of finding bugs and writing them up so another person can reproduce them. In a jam nobody holds this title, which is why jam games crash on the judge's machine. You'll give QA a named owner for the final hours of every milestone. Week 10 covers the craft.

**Holding the vision.** When two teammates both have a good idea and they conflict, someone must decide. If no one has that job, the team either argues until the deadline or quietly builds both. Decide up front who breaks ties and how (the lead designer decides, or the team votes, or the person who owns that feature decides). Any of these rules works. Having none does not.

### Roles and people are different things

A **role** is a bundle of responsibilities. A **person** can hold several roles, and one role can be split across several people. In a 300-person studio, "gameplay programmer" might be forty people. On your jam team of four, one person might be programmer, producer and audio designer at once.

Stardew Valley is the extreme case. Eric Barone started it after graduating in 2011 and released it on 26 February 2016. He made the code, the pixel art, the music and the sound effects himself, over roughly five years. Every job in the table above was his. That's one reason it took years. A solo developer pays no coordination cost, but also has no parallelism. Only one job advances at a time.

The rest of this lecture is about the opposite pressure. Once you add people, you get parallel work, and you also get the cost of keeping everyone in sync.

## 2. Worked example: why jam teams stay small

### The hook

The Global Game Jam is a 48-hour jam held every January at sites around the world. At the first one, in January 2009, 1,650 participants made 370 games, about 4.5 people per game. At the 2025 jam, 35,371 registered participants made 12,098 games, about 2.9 people per game. (Registered participants who didn't finish, and solo entries, both pull that average around, so treat it as rough.)

Nobody sets a team size cap that low. Jammers could form teams of ten. They mostly don't, and teams that try usually find the second day slower than the first. Why would adding people make a 48-hour project go slower? Fred Brooks asked the same question about IBM's OS/360 operating system in the 1960s and wrote the answer down in 1975: adding people to a late software project makes it later. The model below is the simplest version of his reasoning.

### The model

Every pair of people who need to agree on something is a **communication channel**. In a team of `n` people where everyone's work touches everyone else's (a "full mesh"), the number of channels is the number of pairs:

```
channels(n) = n × (n − 1) / 2
```

Now give each person `H` hours of work time, and say every channel costs each of its two people `c` hours over the same period. That covers meetings, messages, waiting for an answer, and redoing work because you misunderstood. The team's **useful capacity** is total hours minus coordination hours:

```
capacity(n) = n × H − 2c × channels(n)
            = n × H − c × n × (n − 1)
```

- `n` is team size.
- `H` is hours each person has in the period (a week, a jam).
- `c` is hours each person spends per channel in that period.
- `capacity` is hours left for building the game.

The first term grows in a straight line. The second grows with the square of `n`. Sooner or later the square wins. Set the slope to zero (the change from adding one more person) and you find the size that maximizes capacity:

```
n* = (H + c) / (2c)
```

That one line holds the whole lesson. **The best team size depends on the ratio of work time to coordination cost per channel.** Cheap coordination (clear ownership, separate files, a shared task board) allows bigger teams. Expensive coordination (everyone editing the same scene, nobody sure who decides) forces smaller ones.

### Numbers you can check

A semester project first. Each student gives the project `H = 10` hours a week, and each channel costs each of its two people half an hour a week (`c = 0.5`).

| Team size n | Channels | Total hours n × H | Coordination hours c × n × (n − 1) | Useful capacity |
|---|---|---|---|---|
| 1 | 0 | 10 | 0 | 10 |
| 2 | 1 | 20 | 1 | 19 |
| 3 | 3 | 30 | 3 | 27 |
| 4 | 6 | 40 | 6 | 34 |
| 6 | 15 | 60 | 15 | 45 |
| 8 | 28 | 80 | 28 | 52 |
| 10 | 45 | 100 | 45 | 55 |
| 11 | 55 | 110 | 55 | 55 |
| 15 | 105 | 150 | 105 | 45 |
| 20 | 190 | 200 | 190 | 10 |

The formula gives `n* = (10 + 0.5) / 1 = 10.5`, so 10 or 11, and the table agrees. Notice how flat the top is. Going from 8 to 11 people adds 3 people and only 3 hours of useful capacity a week. Each of those new people costs almost as much in coordination as they bring.

Now a jam. Over 48 hours each person gets about `H = 30` hours of real work once you subtract sleep and food. Coordination is far more expensive per channel, because everyone is working on one small game at once and nobody has time to write anything down. Say `c = 3` hours per channel per person over the jam.

| Team size n | Channels | Total hours | Coordination hours | Useful capacity |
|---|---|---|---|---|
| 1 | 0 | 30 | 0 | 30 |
| 2 | 1 | 60 | 6 | 54 |
| 3 | 3 | 90 | 18 | 72 |
| 4 | 6 | 120 | 36 | 84 |
| 5 | 10 | 150 | 60 | 90 |
| 6 | 15 | 180 | 90 | 90 |
| 8 | 28 | 240 | 168 | 72 |

Here `n* = 33 / 6 = 5.5`. The best jam team is five or six, and four is close behind. Eight people get less done than four, even though they have twice the hours. That's the Global Game Jam pattern, and it's Brooks's law in miniature.

The numbers `c = 0.5` and `c = 3` are assumptions, not measurements. You'll measure your own team's coordination time in the lab and in the week 9 jam post-mortem. What matters now is the shape. Capacity rises, flattens and then falls, and the peak moves left as `c` goes up.

### Structure changes the count

The full-mesh assumption says everyone must talk to everyone. Real teams break that on purpose. Split `n` people into `k` sub-teams of `s` people each (so `n = k × s`). Inside a sub-team, everyone talks. Between sub-teams, only the leads talk. The channel count becomes:

```
channels = k × s × (s − 1) / 2  +  k × (k − 1) / 2
           (inside the sub-teams)   (between the leads)
```

For 12 people in the semester model:

| Structure | Channels | Coordination hours (c = 0.5) | Useful capacity |
|---|---|---|---|
| Full mesh, 12 people | 66 | 66 | 54 |
| 3 sub-teams of 4, leads talk | 3 × 6 + 3 = 21 | 21 | 99 |
| 2 sub-teams of 6, leads talk | 2 × 15 + 1 = 31 | 31 | 89 |

Same 12 people, same 120 hours. The structured team gets almost twice the useful work. That is what team structure is for. A lead, a feature owner and a shared task board all exist to remove channels.

There's a catch the formula hides. The structure only works if the sub-teams really are independent. If the art sub-team can't finish anything without asking the code sub-team, those cross-team channels come back, and they're worse than before because they now go through two leads. Week 5 (Scrum) and week 7 (task tracking) are about keeping sub-teams independent.

### Watch it move

Open the interactive. The left view draws the team as a graph, one dot per person and one line per channel. The right view plots useful capacity against team size. Drag the team-size slider from 3 to 12 and watch the left view fill with lines while the right curve rises, flattens and bends down. Then switch to "sub-teams with leads" and set sub-team size to 4. Most of the lines vanish and the capacity curve lifts. Finally raise `c` from 0.5 to 3 and watch the peak slide left toward the jam numbers.

### The same idea in other places

**IBM OS/360 (1960s), via Brooks.** Brooks managed the OS/360 project and wrote *The Mythical Man-Month* about what went wrong. His chapter 2 gives the same pair count, `n(n − 1)/2`, with small cases: three workers need three times as much pairwise communication as two, and four need six times as much. Scale it up and 50 developers have 1,225 channels. He adds the other cost this lecture's model skips, ramp-up. A new person needs training from existing people, which takes their hours before the new person contributes anything. Put that in our model as a one-time extra cost on the new person's channels and you get his law. Adding people late makes things later.

**Supercell (Helsinki, founded 2010).** Supercell describes itself as built on very small, independent teams and says it tries to keep the company as small as possible. The idea is our sub-team formula taken seriously. Each game team is its own small full mesh, and the company keeps the between-team channels few. It also kills most of what it starts. Supercell lists games cancelled in development or beta, including Battle Buddies, Spooky Pop and Smash Land, next to the few that reached global launch (Hay Day, Clash of Clans, Boom Beach, Clash Royale, Brawl Stars). Small teams make cancelling cheaper, which fits GD101 week 8's argument that more loops beat bigger bets.

**Valve (after Half-Life 2).** Valve moved to a flat organization with open allocation. Outside executive management there are no assigned bosses, and people choose which project to join. In channel terms, Valve lets teams form around projects and dissolve after them, instead of fixing the structure in advance. The cost is that no structure is imposed, so the team itself has to create ownership. Otherwise it drifts back to a full mesh.

**Innersloth and Among Us (2018 to 2020).** Among Us launched on mobile in June 2018 from a very small team at Innersloth. When it suddenly became hugely popular in the second half of 2020, Innersloth announced a sequel in August 2020. On 23 September 2020 they cancelled it and chose to rework the original game's codebase instead, which they described as not built to support that much new content. A team size and a codebase that suited a small game became a constraint once the job changed. Growing the team was the obvious move, and every new person meant new channels into old code.

Four very different organizations, one formula. Useful work grows with people, coordination grows with pairs, and structure is how you choose which pairs have to talk.

### Design judgment

The model is a thinking tool, not a law of nature. Use it with these trade-offs in view.

- **Small teams finish.** Under 48 hours and with cheap tools, 3 to 5 people is the sweet spot. Your jam team will be four, and the lab asks you to justify that number with your own `c`.
- **Structure has a price.** Sub-teams need leads, and leads spend hours on between-team channels instead of building. For fewer than about six people the saving is small, and a single shared board is usually enough.
- **The model assumes interchangeable people.** It doesn't. A team of four programmers has great capacity and no art. Before you optimize size, check coverage (section 4). Headcount is the wrong number if nobody can do the audio.
- **Lower `c` before you add people.** Every tool, habit and file layout that lowers coordination cost per channel raises the best team size. Clear ownership, separate files and short daily check-ins all count. Weeks 2 and 3 on Git and assets are really about lowering `c`.

## 3. Roles as responsibilities: the RACI matrix

Job titles don't tell you who decides. A **RACI matrix** does. For each task or deliverable, you mark each person with one of four letters:

- **R, Responsible.** Does the work. There can be more than one.
- **A, Accountable.** Owns the outcome and signs it off. Exactly one per task. If it goes wrong, this person answers for it, and this person breaks ties.
- **C, Consulted.** Asked before the work is final. Two-way conversation.
- **I, Informed.** Told after the decision. One-way.

The single rule that matters most is **exactly one A per row**. Zero A's means nobody owns the outcome, so it slips. Two A's means two people think they have the final say, so it becomes an argument. The same person can be R and A (write that as "A/R").

Here's a RACI matrix for a four-person jam team making a small 2D platformer. Ana is designer and producer, Ben is programmer, Chen is artist and Dee is programmer and audio.

| Deliverable | Ana | Ben | Chen | Dee |
|---|---|---|---|---|
| Core rules and tuning numbers | A/R | C | I | C |
| Player movement code | C | A/R | I | I |
| Enemy and hazard code | C | C | I | A/R |
| Character and tile art | C | I | A/R | I |
| Sound effects and music | C | I | I | A/R |
| Menus and UI | A | R | R | I |
| Build that runs on a clean machine | I | A/R | I | R |
| Task board up to date | A/R | I | I | I |
| Final bug pass | A | R | R | R |

Read it row by row and ask whose name you'd say if a judge asked "who's in charge of this?" Every row has one answer. Menus and UI is a good example of a split: Ben writes the code, Chen draws the screens, and Ana decides when it's done.

Now read it column by column. Ana is A on five rows and R on two. For a four-person jam that's fine, because producer work is light. On a bigger project, a column with too many A's is a bottleneck, since everything waits on that one person to sign off.

### RACI and channels

RACI is a channel-cutting tool in disguise. An "I" is a one-way message, far cheaper than a "C". A task with one R, one A and everyone else "I" has almost no coordination cost. A task where everyone is "C" is a full mesh for that task. When a matrix row is all C's, ask whether each of those people really needs a say before the work is final.

## 4. Coverage, T-shaped people and the bus factor

The channel model treated people as interchangeable. Coverage is about the fact that they aren't.

A **coverage matrix** lists skills as rows and people as columns and marks who can do each skill at a usable level. A skill with no marks is a hole. A skill with one mark is a risk.

The **bus factor** of a skill is the number of people who could leave (get sick, drop the course, be hit by the proverbial bus) before nobody left can do it. A skill only one person has has a bus factor of 1. For a jam team the bus factor that matters is "who can make a build?" If only one person knows how to export the game and that person falls asleep at hour 46, you don't have a game.

You raise a bus factor two ways. One is pairing. The second person watches or helps the first on that skill for an hour, then does it once alone. The other is writing things down. A five-line "how to export the build" note in the repository raises the bus factor of that skill to "anyone who can read".

A **T-shaped** person has one deep skill (the vertical bar of the T) and working knowledge across several others (the horizontal bar). Small teams need T-shaped people, because every person must cover more than one job. When you confirm your jam team before week 8, look for coverage first and depth second.

A coverage matrix for the team above:

| Skill | Ana | Ben | Chen | Dee | Bus factor |
|---|---|---|---|---|---|
| Game design | yes | | | yes | 2 |
| Gameplay code | | yes | | yes | 2 |
| Export a build | | yes | | | 1 |
| 2D art and animation | | | yes | | 1 |
| Audio | | | | yes | 1 |
| Production | yes | | yes | | 2 |

Three skills have bus factor 1. The team can live with art and audio at 1, since jam games ship with placeholder art and no music all the time. It cannot live with the build at 1. The fix costs one hour on day one: Dee pairs with Ben on the export.

## 5. Your team for this course

From week 2 you work in a team of four that stays together through the jam (week 8) and the final release (week 15). Before any code, you write a **team charter**. It's one page, and it answers these questions:

1. **Who holds which roles?** A RACI matrix for your first milestone.
2. **Who breaks ties?** One sentence naming the rule.
3. **Where do we talk?** One chat channel for decisions, one task board. Decisions made in a direct message don't count until they're posted in the team channel.
4. **When do we meet?** A fixed 10-minute check-in, at least twice a week.
5. **What counts as late?** For example, "a task not done by its day, without warning 24 hours before".
6. **What happens when someone is late twice?** Decide this while everyone is calm. Week 11 covers conflict. A charter that answers this in advance removes most of it.

The charter also records your team's guess at `c` from section 2. You'll compare it to measured coordination time after the jam, and the week 6 lecture on estimation will use it.

## In-class activity (25 minutes)

In groups of four (your provisional team).

1. **Five minutes.** Each person writes their deep skill and up to three working skills on sticky notes. Build the coverage matrix on the table. Circle every bus factor of 1.
2. **Ten minutes.** Draft a RACI matrix for this toy brief: "a one-screen arcade game where the player dodges falling objects, with a title screen, a score, three sounds and a build that runs on the lab machines". Use the nine rows from section 3 or your own. Check that every row has exactly one A.
3. **Five minutes.** Estimate your own `c` for a jam weekend. How many hours per teammate would you expect to spend talking, waiting and redoing? Plug it into `n* = (H + c) / (2c)` with `H = 30`. Does your answer support a team of four?
4. **Five minutes.** Swap matrices with a neighbouring group. Find one row with zero or two A's, one column that's a bottleneck, or one skill nobody covers.

Expected output: a photo of your coverage matrix, a RACI table, your `c` and `n*`, and the problem your neighbours found.

## Common misconceptions

- **"More people means faster."** Only while coordination hours grow slower than work hours. In the channel model, adding the `(n + 1)`th person adds `n` new channels. At `c = 3` and `H = 30`, the sixth jam teammate adds 30 hours of work and 30 hours of coordination, a net gain of zero.
- **"The producer is the boss."** The producer owns the schedule and unblocking. The A column on each row names the boss for that row, and it's often a different person.
- **"Everyone should be consulted on everything; that's teamwork."** A row full of C's is a full mesh for that task. Consult the people whose work the decision changes, and inform the rest.
- **"We're all friends, we don't need a charter."** The charter isn't about trust. It's about removing decisions you'd otherwise make at 3 a.m. on hour 34, when nobody is at their best.

## Check yourself

1. A team has 7 people in a full mesh. How many channels are there? How many new channels does an eighth person add?
2. For a jam with `H = 30` and a very messy team with `c = 5`, what team size maximizes useful capacity? Compute capacity at 3 and 4 people.
3. A studio team of 16 is split into 4 sub-teams of 4 whose leads talk to each other. Compute the channels and useful capacity with `H = 10`, `c = 0.5`. Compare to a full mesh of 16.
4. A RACI row reads: Ana A, Ben A, Chen R, Dee C. What will go wrong, and what's the fix?
5. On a team of four, only one person knows how the audio middleware is hooked up. What is that skill's bus factor, and what's the cheapest way to raise it to 2?

<details>
<summary>Answers</summary>

1. `7 × 6 / 2 = 21` channels. An eighth person adds 7 channels (one to each existing member), giving 28.
2. `n* = (30 + 5) / (2 × 5) = 3.5`, so 3 or 4. Capacity at 3 is `90 − 5 × 3 × 2 = 60`. At 4 it's `120 − 5 × 4 × 3 = 60`. They tie. With expensive coordination, a fourth person adds nothing, which is an argument for lowering `c` before the jam.
3. Channels are `4 × (4 × 3 / 2) + 4 × 3 / 2 = 24 + 6 = 30`. Capacity is `160 − 2 × 0.5 × 30 = 130` hours. Full mesh: `16 × 15 / 2 = 120` channels, capacity `160 − 120 = 40`. The structure more than triples useful capacity.
4. Two A's means two people believe they have the final say. Chen will get conflicting instructions, and the task will stall or be done twice. Pick one A. The other becomes C.
5. Bus factor 1. The cheapest fix is a one-hour pairing session where the second person hooks up one new sound while the expert watches, plus a short written note in the repository.

</details>

## Lab / assignment hook

[Lab 01, team charter and RACI](../labs/lab01.md). Your team writes a charter, a RACI matrix and a coverage matrix for the first sprint, then runs a checker script that flags rows without exactly one A and skills with a bus factor of 1. This charter carries into the week 8 jam.

## Sources

- Brooks, F. P. (1975; anniversary ed. 1995). *The Mythical Man-Month*. Addison-Wesley. Chapter 2 states Brooks's law and the intercommunication count `n(n − 1)/2`, with the three-worker and four-worker comparisons (checked against the anniversary edition's text on the Internet Archive, September 2026). The 50-developer, 1,225-channel figure is this lecture's own application of the formula.
- Wikipedia, "Brooks's law" (accessed September 2026). Statement of the law, its 1975 origin, and Brooks's own description of it as an oversimplification.
- Wikipedia, "Global Game Jam" (accessed September 2026). First jam 30 January to 1 February 2009, 53 sites, 1,650 participants, 370 games; 48-hour format; 2025 jam 35,371 registered participants, 795 sites, 12,098 games.
- Wikipedia, "Stardew Valley" (accessed September 2026). Development began after Barone graduated in 2011; solo development of code, pixel art, music and sound; release 26 February 2016 on Windows.
- Supercell, "About us" (supercell.com, accessed September 2026). Small independent teams; founded 2010; list of cancelled games and the five games that reached global launch.
- Wikipedia, "Valve Corporation" (accessed September 2026). Move to a flat organization with open allocation after Half-Life 2.
- Wikipedia, "Among Us" (accessed September 2026). June 2018 mobile launch; 2020 popularity surge; sequel announced August 2020 and cancelled 23 September 2020 in favour of reworking the original codebase.
- Keith, C. (2020). *Agile Game Development* (2nd ed.). Addison-Wesley.

## Interactive spec: examples/w01-team-channels.html

**The one insight.** Useful team capacity rises, flattens and falls as people are added, because coordination grows with pairs. Structure (sub-teams with leads) removes most of the pairs.

**Layout.** Two linked views side by side on desktop, stacked on mobile (graph first).

1. **Left view, the team graph.** `n` dots on a circle. In "full mesh" mode, draw a line between every pair. In "sub-teams" mode, group the dots into `k = ceil(n / s)` clusters placed around the circle. Draw lines within each cluster between all pairs, and lines between the first dot (the lead, drawn with a ring) of each cluster. When `n` is not a multiple of `s`, the last cluster is smaller. Below the graph, show "Channels: X" in large text.
2. **Right view, capacity chart.** x-axis team size 1 to 20, y-axis useful capacity in hours. Plot two series: full mesh (solid) and sub-teams (dashed), both from the formulas below, as points joined by lines. Mark the current `n` with a vertical line and a labelled dot on each series. Mark the full-mesh maximum with a small triangle and the label `n* = (H + c) / (2c)` with its value.

**Controls** (all keyboard operable, values shown next to each).

- Team size `n`: slider 1 to 20, step 1, default 8.
- Hours per person `H`: slider 5 to 40, step 1, default 10.
- Cost per channel per person `c`: slider 0.25 to 5, step 0.25, default 0.5.
- Structure: toggle "Full mesh" / "Sub-teams with leads", default full mesh.
- Sub-team size `s`: slider 2 to 8, step 1, default 4 (enabled only in sub-team mode).
- Two preset buttons: "Semester (H 10, c 0.5)" and "Jam weekend (H 30, c 3)".

**Formulas.**

```
mesh_channels(n) = n (n − 1) / 2
k = ceil(n / s); sizes = [s, s, ..., n − s (k − 1)]
team_channels(n, s) = sum(size (size − 1) / 2 for size in sizes) + k (k − 1) / 2
capacity = n H − 2 c × channels
n* = (H + c) / (2c)    (report to one decimal, and the integer n with the highest capacity)
```

**Readout table** under the chart for the current settings: n, channels (mesh), channels (sub-teams), total hours, coordination hours, useful capacity for both structures.

**Test values** (must match the lecture tables).

- H 10, c 0.5: mesh capacity at n = 4, 8, 10, 11, 15, 20 is 34, 52, 55, 55, 45, 10. n* = 10.5.
- H 30, c 3: mesh capacity at n = 3, 4, 5, 6, 8 is 72, 84, 90, 90, 72. n* = 5.5.
- H 10, c 0.5, n 12, s 4: sub-team channels 21, capacity 99. s 6: channels 31, capacity 89. Mesh: 66 channels, capacity 54.
- H 10, c 0.5, n 16, s 4: sub-team channels 30, capacity 130. Mesh: 120 channels, capacity 40.

**Behaviour.** Negative capacity is allowed and drawn below a zero line with a shaded "coordination exceeds work" band. With reduced motion, lines appear without animation. Colors from `templates/interactive-tokens.css`. Dots are generic circles with initials A, B, C... No game art.
