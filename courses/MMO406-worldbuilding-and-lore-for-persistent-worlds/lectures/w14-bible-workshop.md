# MMO406 · Week 14 — Bible Workshop

**Why this matters:** Your world bible is due next week, and its real readers are writers who haven't been hired yet. Every question the bible can't answer goes to a person, usually the lore lead, and that person has a limited number of hours. This week you learn why a bible that answers 60% of questions and one that answers 70% produce very different studios, and you spend the session testing your own bible against questions from people who have never seen your world.

**You will be able to:**
- Compute the escalated question rate, the lore lead's load and the average wait for an answer, from the team's question rate, the bible's answer rate and the lead's answering capacity.
- Derive the minimum answer rate a bible needs for a given team, and show how it rises when the team grows for an expansion.
- Run a question test on a bible, estimate its answer rate with an honest margin of error, and rank its chapters by the gaps they cause.
- Critique how Blizzard's Ask CDev and Chronicle, a TV series bible and a server cache handle the same load problem.

**Before class:** Bring your bible draft (chapters from labs 1 to 12, with the lab 13 community chapter at least in outline) as one document with a table of contents and fact ids. Warcraft Wiki, "Ask CDev" (skim the dates and the first ten answers of round 1, 10 minutes) and "World of Warcraft: Chronicle" (the introduction, 5 minutes). Wikipedia, "Series bible" (5 minutes). Wolf, *Building Imaginary Worlds* (2012), chapter 1, "Worlds within the World," the parts on completeness and consistency (use the contents page, reread about 10 pages).

**Prerequisites from earlier courses:** [MMO302 week 11, load testing](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (the M/M/1 queue and `W = 1 / (μ − λ)`; this week reuses the formula without deriving it again). [DB201 week 8, caching](../../DB201-data-persistence-and-telemetry/lectures/w08-caching-and-write-behind.md) (a cache hit spares the database). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the margin of error of a proportion). [GD101 week 14, design documents](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) (why the one-pager comes first). From this course, [week 1](w01-setting-as-system.md) (the tension ledger), [week 10](w10-expansion-planning.md) (open hooks) and [week 11](w11-retcons-and-continuity.md) (fact ids, the canon graph and tiers).

**Interactive:** [The lore desk](../examples/w14-lore-desk.html). Keep it open during section 2.

---

## 1. What the bible is for

A **world bible** (also called a series bible or setting bible) is the reference document that writers, designers and licensees consult to keep a world consistent. Television has used them for decades. The *Frasier* bible, for example, was maintained so carefully that anything established on air went into it, down to a character's list of food allergies.

For a persistent world, the bible has a harder job than for a TV series. It has to serve dozens of writers over ten years or more, across expansions planned by people who have not joined yet (week 1). So judge it the way you would judge a tool, by what happens when someone uses it. A writer opens it with a question. Either the bible answers, or the writer asks a person, or the writer guesses. Guesses become contradictions (week 11). Questions to a person become a queue.

Your bible for this course has the chapters you built in labs 1 to 13:

| Chapter | Built in | What a writer looks up there |
|---|---|---|
| Front matter: one-page pitch, pillars, tone | Week 1 | What kind of world is this? What must never happen? |
| Tensions and expansion supply | Lab 01 | What conflicts can I build on? |
| Regions, resources and ecology | Lab 02 | What lives and grows here? Who needs what from where? |
| Factions | Lab 03 | Who is allied with whom, and where is the pressure? |
| History and calendars | Lab 04 | When did this happen? How old is this person? |
| Cultures and naming | Lab 05 | What would this person be called? |
| Religions and myths | Lab 06 | What do they believe, and what is actually true? |
| Lore delivery and assumed knowledge | Lab 07 | What can I assume the player knows? |
| Canon policy | Lab 08 | Which player choices are world canon? |
| Living events | Lab 09 | What did the world keep from past events? |
| Expansion briefs and hooks | Lab 10 | What is planted, and what must I not resolve? |
| Canon graph and tiers | Lab 11 | What depends on this fact? Which source wins? |
| Beyond the game | Lab 12 | What did the novel establish? What may a licensee touch? |
| Community | Lab 13 | Where do roleplayers gather? What slots are open? |

This week is about whether those chapters work together as a tool. The worked example explains why the answer rate is the number to watch.

## 2. Worked example: the lore desk

### The hook

In November 2010, Blizzard's Creative Development team started Ask CDev, a series in which players posted lore questions for World of Warcraft on the official Story forum and the team published official answers. The first answer of the first round replied to a player who had asked, more or less, whether a developer would ever answer anything in the thread. The series ran four rounds: November 2010, June 2011, May 2012 and April 2014. The wiki's copy of the answers holds 90 questions in total, 18 to 26 per round, with gaps of seven months to almost two years between rounds.

Blizzard is not a small studio, and the people answering were its senior lore staff. Yet the channel answered about 26 questions a year, and then stopped.

Meanwhile, at the Mists of Pandaria launch party in 2012, Chris Metzen first mentioned a Warcraft equivalent of the *Book of Cain*, the illustrated history released for Diablo III. It became *World of Warcraft: Chronicle*, a series of illustrated history books whose first volume came out in March 2016. Its stated aim was to codify, tighten up and clarify Warcraft's history, and one of its writers compared it to a bible with illustrations. Internal readers and Blizzard's historians checked it.

One channel answered questions one at a time and could never keep up. The other answered thousands of questions before anyone asked them. The model below says why the second approach is the one that scales, and how to tell how much of it you need.

### The model

Picture the lore lead's desk inside a studio. Writers produce questions at a steady rate. The bible answers some of them. The rest land on the desk.

```
Questions reaching the desk:   λ_e = (1 − a) × λ
Lead's load:                   ρ = λ_e / μ
Average wait for an answer:    W = 1 / (μ − λ_e)      if λ_e < μ
                               W = never clears       if λ_e ≥ μ
Minimum answer rate:           a_min = 1 − μ / λ
Answer rate for a target wait: a_target = 1 − (μ − 1/W_target) / λ
```

- `λ` is the number of lore questions the writing team produces per week, counting every question a writer has, whether the bible answers it or not.
- `a` is the **answer rate**, the share of those questions a writer can settle from the bible alone.
- `λ_e` is the **escalated rate**, questions per week that reach a person.
- `μ` is the number of questions the lead can answer per week.
- `ρ` is the lead's load, the share of their answering capacity in use.
- `W` is the average time from asking to answer, in weeks. Multiply by 5 for working days.

The waiting-time line is the M/M/1 queue from MMO302 week 11, with questions instead of server requests. That week derived it and listed its assumptions: questions arrive at random, answering times vary at random, and one person answers them in order. What is new here is the first line. The bible sits in front of the desk and removes a share `a` of the arrivals, exactly as a cache sits in front of a database (DB201 week 8).

Look at the denominator `μ − λ_e`. It is the lead's **spare capacity**. As spare capacity approaches zero, the wait grows without limit. So small changes in `a` near `a_min` produce huge changes in `W`.

### Numbers you can check

Take *Thornmere*'s writing team during development of its first expansion: 12 writers, each producing about 4 lore questions a week, so `λ = 48`. The lore lead spends about half their time answering, roughly 4 questions a day, so `μ = 20`.

The minimum answer rate is `a_min = 1 − 20/48 = 58.3%`. Below that, questions arrive at the desk faster than the lead can answer them, and the pile grows forever.

| Answer rate `a` | Reaching the desk `λ_e` | Load `ρ` | Average wait | Questions on the desk `λ_e × W` |
|---|---|---|---|---|
| 50% | 24.0 | 1.20 | never clears | grows forever |
| 55% | 21.6 | 1.08 | never clears | grows forever |
| 60% | 19.2 | 0.96 | 6.25 days | 24.0 |
| 65% | 16.8 | 0.84 | 1.56 days | 5.3 |
| 70% | 14.4 | 0.72 | 0.89 days | 2.6 |
| 80% | 9.6 | 0.48 | 0.48 days | 0.9 |
| 90% | 4.8 | 0.24 | 0.33 days | 0.3 |

Check the 70% row by hand. `λ_e = 0.3 × 48 = 14.4`. Spare capacity is `20 − 14.4 = 5.6` per week, so `W = 1/5.6 = 0.179` weeks, and `0.179 × 5 = 0.89` working days. The last column is Little's law from MMO302: `14.4 × 0.179 = 2.6` questions waiting or being answered on average.

Moving from 60% to 70% answered, a change in one question in ten, cuts the average wait from more than a working week to less than a day. Moving from 80% to 90% saves a few hours. The payoff of improving the bible is largest exactly where the lead is busiest.

A writer who waits six days for an answer does not wait. They guess, and week 11 showed what guesses cost.

### The expansion problem

Now the studio staffs up for the expansion and the writing team doubles to 24. The lead's capacity doesn't change. So `λ = 96`.

| | 12 writers (`λ = 48`) | 24 writers (`λ = 96`) |
|---|---|---|
| Minimum answer rate `a_min` | 58.3% | 79.2% |
| Answer rate for a 1-day wait | 68.8% | 84.4% |
| Wait at `a = 70%` | 0.89 days | never clears |
| Wait at `a = 85%` | 0.39 days | 0.89 days |

The bible that was comfortable for the launch team collapses the moment the team doubles. To keep the same 0.89-day wait, the answer rate has to rise from 70% to 85%, which means answering half of the questions that used to escalate. That is what "a bible that scales across expansions" means in numbers: the bible has to answer more as the team grows. Adding pages that nobody finds doesn't count.

You can reproduce both tables:

```python
def wait_days(lam, mu, a, days_per_week=5):
    escalated = (1 - a) * lam
    if escalated >= mu:
        return float("inf")
    return days_per_week / (mu - escalated)

mu = 20
for lam in (48, 96):
    a_min = 1 - mu / lam
    a_day = 1 - (mu - 5) / lam
    print(f"lam={lam}: a_min={a_min:.1%}  a for 1 day={a_day:.1%}")
    for a in (0.6, 0.7, 0.8, 0.85, 0.9):
        print(f"   a={a:.0%}  wait={wait_days(lam, mu, a):.2f} days")
```

It prints:

```
lam=48: a_min=58.3%  a for 1 day=68.8%
   a=60%  wait=6.25 days
   a=70%  wait=0.89 days
   a=80%  wait=0.48 days
   a=85%  wait=0.39 days
   a=90%  wait=0.33 days
lam=96: a_min=79.2%  a for 1 day=84.4%
   a=60%  wait=inf days
   a=70%  wait=inf days
   a=80%  wait=6.25 days
   a=85%  wait=0.89 days
   a=90%  wait=0.48 days
```

### A visual you can move

Open the interactive. The left panel, "The bible", shows the answer rate as a single bar with a page count beside it. Moving from 60% to 70% looks like a small step. The right panel, "The desk", shows the lead's in-tray as a stack of question cards and a curve of average wait against answer rate, with a shaded "never clears" region to the left of `a_min`. Start at `a = 60%` and nudge it to 65%, then 70%. The bar barely moves; the stack on the desk drops from about 24 cards to 3. Then double the team with the "expansion" toggle. The shaded region swallows your current answer rate, and the stack starts growing without limit.

### Cross-game recognition

**World of Warcraft: Ask CDev (2010 to 2014) and Chronicle (2016 onward).** Ask CDev was a desk with a very small `μ`, about 26 answers a year in public. With a player base far larger than any lore team, no realistic `μ` could keep up, so the only lever was `a`. *Chronicle* moves the answers into a reference that anyone can consult. It also shows the second benefit of a written answer: one ruling answers many future questions. Ask CDev's round 2 opened by ruling that the Warcraft tabletop RPG books were not canon, a single answer that settles every later question of the form "is this RPG book detail true?"

**Television: the series bible.** The *Frasier* bible's practice of recording everything established on air is the rule "answer once, write it down". Each fact that appears on screen goes into the bible, so the next writer who needs Frasier's mother's name finds it without asking. In the model, every escalated question that gets written into the bible raises `a` for the rest of the show.

**Servers and caches (MMO302 week 11, DB201 week 8).** A cache in front of a database is the same arrangement with different items. Requests that hit the cache never reach the database, so the database sees `(1 − h) × λ`, where `h` is the hit rate. The curve is the same too. Run the section 2 numbers with a database in place of the lead, and a cache whose hit rate falls from 60% to 55% takes the database from 96% load to overload, while a rise to 70% cuts its average response time sevenfold. The bible is the cache in front of the lore lead's memory.

**Star Wars: the Holocron.** Week 11 described Lucasfilm's continuity database, run by a dedicated administrator from 2000 and holding over 55,000 entries. A franchise with dozens of licensees producing books, comics and games has a `λ` that no single person could answer one question at a time. The database raised `a` for everyone at once.

Four settings, one rule. When askers outnumber answerers, the only answer that scales is a written one that people can find without asking.

### Eyes-open design judgment

- **Measure the bible by `a`, not by pages.** A 600-page bible with no index can have a lower answer rate than a 60-page one with fact ids and a good table of contents. The question test in section 3 measures `a` directly.
- **Answer once, write it down.** Make it a rule that every escalated question produces a bible edit, or a note that the question is reserved. Then `a` rises over time and the desk empties itself.
- **Protect the hooks.** Some questions should escalate. An open hook from week 10 ("who told Harrow the enemy was inside?") must not be answered in the bible, or a writer will resolve it by accident. Mark such entries "reserved, ask the lead". They count as escalations, so keep the list short.
- **`μ` is fragile.** When the lead is on holiday, `μ` is zero and every escalated question waits. A second trained reader, even at half speed, keeps the desk out of the "never clears" region.
- **The model is a best case.** Real questions arrive in bursts (a new zone kickoff, a script deadline) and answers are batched into weekly meetings. Both make waits longer than M/M/1 predicts, as MMO302 week 11 warned for servers. Aim for a load well below 1.

### Check yourself (worked example)

1. A team of 8 writers asks 5 questions each per week. The lead answers 15 per week. What is `a_min`? What answer rate gives an average wait of one working day?
2. Your bible answers 75% of questions, `λ = 60` and `μ = 20`. The lead goes on leave and a junior writer covers at `μ = 12`. What happens to the wait?

<details>
<summary>Answers</summary>

1. `λ = 40`. `a_min = 1 − 15/40 = 62.5%`. A one-day wait is `W = 0.2` weeks, so spare capacity must be 5: `a = 1 − (15 − 5)/40 = 75%`.
2. `λ_e = 0.25 × 60 = 15`. With the lead, `W = 5/(20 − 15) = 1` day. With cover, `λ_e = 15 ≥ 12`, so the pile grows without limit. The bible needs `a ≥ 1 − 12/60 = 80%` just to stay stable during the leave.

</details>

## 3. The question test

You can't compute `a` from the bible itself. You have to ask it questions. A **question test** estimates the answer rate by having people who don't know your world ask it the questions a new writer would, and recording what happens.

### The procedure

1. **Recruit askers.** Two or more people who have not read your bible. In class, that is the other members of your workshop group.
2. **Give them a writing task.** "Write a quest set in the eastern marshes during the second expansion." A task produces realistic questions. "Ask anything" produces trivia.
3. **Collect questions blind.** Each asker writes 15 questions before opening your bible. Aim for at least 30 in total.
4. **Classify each question** by searching the bible with the asker watching, and time-box it at three minutes per question:

| Status | Meaning | Counts toward `a`? |
|---|---|---|
| Answered | The bible states it; you can point to a fact id | Yes |
| Derivable | Not stated, but a rule in the bible settles it without judgment | Yes |
| Missing | The bible doesn't settle it | No |
| Contradicted | Two places in the bible give different answers | No, and it is the worst kind |
| Reserved | Deliberately open; the bible says to ask | No, but it is not a defect |

5. **Compute** `a = (answered + derivable) / total`.
6. **Rank the gaps.** For each chapter, score `missing + 2 × contradicted` and fix the highest scores first. Contradictions count double because a writer who finds one of the two answers doesn't know to ask.

### How precise is your `a`?

Thirty questions is a small sample. MA102 week 13 gave you the margin of error for a proportion, about `1.96 × √(a(1 − a)/n)` for a 95% interval. With 21 of 30 answered, `a = 70%` and the margin is `1.96 × √(0.7 × 0.3 / 30) = 1.96 × 0.084 = 16` points. The true answer rate could be anywhere from about 54% to 86%.

Compare that with the tables in section 2. For a 12-writer team, 54% is "never clears" and 86% is a wait of a few hours. A single question test can't tell you which side of `a_min` you are on. So treat the first test as a way to find gaps, not a certificate. Fix the gaps, then run a **second test with new questions** from new askers. Reusing the first test's questions measures whether you fixed those questions, not whether the bible got better.

## 4. The workshop

The class session this week is the workshop itself. It has three passes, in this order.

### Pass 1: the question test

Run section 3's procedure in groups of three. Each of you is the author once and an asker twice. Record every question in a shared sheet with columns `id, asker, chapter, question, status`. The lab uses the same format.

### Pass 2: the consistency pass

Your labs gave you checkers for most chapters. Run them all against the final versions, because chapters written in week 3 have not seen the facts you added in week 12.

- Tension ledger (lab 01): still supplies at least eight expansions after the expansion briefs spent some tensions?
- Timeline (lab 04): every character in the expansion briefs and transmedia plan alive and of age on the dates you use?
- Canon graph (lab 11): every new fact from labs 12 and 13 added with its dependencies, and `validate` clean?
- Names (lab 05): new characters from the community chapter's examples pass the naming language?

A failure here is a contradiction you found before a writer did. Fix it and log the fix in the graph.

### Pass 3: the front and the index

Writers read the front of a bible and search the rest. So the last pass is about findability.

- **The one-page front.** Pitch, three to five pillars, tone rules, and a list of the ten facts every writer must know. GD101 week 14 showed why the one-pager comes first. Here it also lowers `λ`, because a writer who has read it asks fewer basic questions.
- **Fact ids everywhere.** Every checkable statement carries the id from your canon graph, so a writer can cite it and a reviewer can trace it.
- **A reserved list.** One page listing every open hook and reserved question, with who to ask. It is the only place in the bible allowed to say "ask".
- **A change log.** Each revision after the first release lists the fact ids it touched. Week 11's frozen media depend on writers being able to see what changed.

## In-class activity (30 minutes)

The workshop's first pass, run as a timed exercise in groups of three.

1. **(5 min) Tasks.** Each author writes a one-line writing task for their world (a quest, a festival, a tie-in short story).
2. **(8 min) Questions.** Each asker writes 15 questions for each of the other two authors' tasks without opening their bibles.
3. **(12 min) Classify.** Each author classifies the 30 questions they received, with the askers watching, three minutes per question at most. Record statuses in the shared sheet.
4. **(5 min) Compute.** Each author computes `a`, its margin of error, and the top two chapters by gap score. Then assume a team of 12 writers at 4 questions a week and a lead at 20 a week: is your bible above `a_min`? What wait does your `a` imply?

Expected output: a sheet of 30 classified questions per author, an answer rate with a margin (typically 50% to 75%, with margins of 15 to 18 points), two chapters to fix first, and a wait in days. Most first tests land within one margin of `a_min = 58.3%`, which is why the lab asks for a second test.

## Common misconceptions

- **"A longer bible answers more questions."** Length helps only if writers can find the answer. Index, fact ids and the one-page front raise `a` more per hour of work than new chapters.
- **"If the lead is busy, hire writers to take pressure off."** More writers raise `λ`. Unless the bible improves, the desk gets worse, and a team that doubles needs an answer rate that rises from about 70% to 85% to keep the same wait.
- **"The bible should answer every question."** Open hooks must stay open. A bible that answers everything has closed its own future. Reserved questions are escalations by design.
- **"Going from 90% to 95% is as valuable as going from 60% to 65%."** The wait depends on spare capacity, which changes fastest near `a_min`. Measure where you are before deciding where to spend revision time.

## Check yourself

1. A studio has 20 writers asking 3 questions a week each, and two leads who together answer 30 a week. What is `a_min`? What wait does an answer rate of 70% give?
2. Your question test finds 18 of 30 questions answered or derivable. What is `a` and its approximate 95% margin? For the team in question 1, can you tell whether the desk is stable?
3. Your gap ranking shows: History 2 missing, 1 contradicted; Factions 4 missing, 0 contradicted; Religion 1 missing, 2 contradicted. Which chapter do you fix first, and why?
4. A colleague proposes answering all open-hook questions in the bible so that `a` rises to 95%. Give one argument for and one against using the model and week 10.

<details>
<summary>Answers</summary>

1. `λ = 60`, `μ = 30`, `a_min = 1 − 30/60 = 50%`. At 70%, `λ_e = 18`, `W = 5/(30 − 18) = 0.42` days.
2. `a = 60%`, margin `1.96 × √(0.6 × 0.4/30) = 1.96 × 0.089 ≈ 17.5` points, so roughly 42% to 78%. The interval straddles `a_min = 50%`, so one test can't tell. Fix gaps and run a second test with new questions.
3. Scores: History `2 + 2 = 4`, Factions `4`, Religion `1 + 4 = 5`. Fix Religion first, because its two contradictions can mislead writers who never think to ask.
4. For: `a = 95%` drops the load sharply, and the wait falls well below a day. Against: resolving open hooks spends the future expansions' payoffs early and removes the team's freedom to change plans (week 10's plan-change risk). The few escalations that hooks cause are cheap, and they are the questions the lead should see.

</details>

## Lab / assignment hook

[Lab 14, the question test](../labs/lab14.md). You implement the desk model and a question-log scorer, run them on a *Thornmere* question log, then run two question tests on your own bible, with a revision between them. It is the last exercise (40%) and the final check before you submit the world bible (60%) in week 15.

## Sources

- Warcraft Wiki, "Ask CDev" (current). A Q&A series by Blizzard's Creative Development team with Chris Metzen and Alex Afrasiabi in the official Story forum; round dates 8 November 2010, 23 June 2011, 9 May 2012 and 4 April 2014; the wiki's copy lists 90 answered questions across the four rounds (counted September 2026), round 1 opening with a reply to whether a developer would answer, round 2 opening with the ruling that the RPG books are not canon. https://warcraft.wiki.gg/wiki/Ask_CDev
- Warcraft Wiki, "World of Warcraft: Chronicle" (current). The series' aim to codify, tighten up and clarify Warcraft history; first mentioned by Chris Metzen at the Mists of Pandaria launch party in 2012 as a Warcraft counterpart to Diablo III's *Book of Cain*; Micky Neilson's comparison to a bible with illustrations; checking by internal readers and Blizzard's historians. https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Chronicle
- Warcraft Wiki, "World of Warcraft: Chronicle Volume 1" (current). Released 15 March 2016 by Dark Horse Books. https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Chronicle_Volume_1
- Wikipedia, "Series bible" (accessed September 2026). Definition of a show bible; the *Frasier* bible recording everything established on air.
- Wikipedia, "Star Wars Legends" (accessed September 2026), as cited in week 11. The Holocron continuity database, run from 2000, over 55,000 entries.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".
- The M/M/1 waiting time and Little's law are standard queueing results, derived in MMO302 week 11. The margin of error for a proportion is standard, covered in MA102 week 13.

## Interactive spec: examples/w14-lore-desk.html

**The one insight the visual must make obvious:** near the minimum answer rate, a small improvement in the bible produces a huge drop in how long writers wait, and when the team grows, a bible that was good enough becomes one that never clears its questions.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left on top).

- **Left, "The bible".** One horizontal bar for the answer rate `a` (0% to 100%), with a numeric label, and beside it a page count that scales with `a` for flavour (`pages = round(40 + 400 × a)`). A thin vertical tick on the bar marks `a_min`. This panel shows no waiting times.
- **Right, "The desk".** Top: a stack of question cards representing the average number on the desk, `L = λ_e × W` (cap the drawing at 40 cards; above that, draw 40 and a label "and growing"). Big counters: "Average wait" in working days (2 decimals, or "never clears") and "Lead's load ρ" (percent). Bottom: a chart of wait in days (y, 0 to 10, clipped) against answer rate (x, 0% to 100%). The region `a < a_min` is shaded and labelled "never clears". A dot marks the current `a`. When the expansion toggle is on, draw the curve for the other team size as a faint second line.

**Controls.**

1. Answer rate `a`: slider 0% to 100%, step 1%, default 60%.
2. Writers: slider 1 to 40, default 12. Questions per writer per week: slider 1 to 10, default 4. `λ` = writers × questions, shown.
3. Lead capacity `μ`: slider 1 to 60 per week, default 20.
4. "Expansion: double the team" toggle (doubles writers while on).
5. "Lead on leave" toggle: sets `μ` to half its value (a junior covering).
6. Presets: "Lecture 60%" (12, 4, 20, `a = 60%`), "Lecture 70%" (same, `a = 70%`), "Expansion at 70%" (24 writers, `a = 70%`), "Expansion at 85%" (24 writers, `a = 85%`).

All controls are labelled native inputs, keyboard operable. An `aria-live` region states, for example, "Answer rate 70%. 14.4 questions a week reach the lead. Load 72%. Average wait 0.89 working days. Minimum answer rate 58.3%."

**Formulas.**

```
λ = writers × questions per writer
λ_e = (1 − a) × λ
ρ = λ_e / μ
W_days = 5 / (μ − λ_e)           if λ_e < μ, else "never clears"
L = λ_e × W_weeks = λ_e / (μ − λ_e)
a_min = max(0, 1 − μ / λ)
a_1day = 1 − (μ − 5) / λ          (shown as "for a one-day wait"; if μ ≤ 5, show "not reachable")
```

**Test values (must match).**

| Writers | Q/writer | `μ` | `a` | `λ_e` | `ρ` | Wait (days) | `L` |
|---|---|---|---|---|---|---|---|
| 12 | 4 | 20 | 60% | 19.2 | 96% | 6.25 | 24.0 |
| 12 | 4 | 20 | 65% | 16.8 | 84% | 1.56 | 5.25 |
| 12 | 4 | 20 | 70% | 14.4 | 72% | 0.89 | 2.57 |
| 12 | 4 | 20 | 85% | 7.2 | 36% | 0.39 | 0.56 |
| 12 | 4 | 20 | 55% | 21.6 | 108% | never clears | growing |
| 24 | 4 | 20 | 70% | 28.8 | 144% | never clears | growing |
| 24 | 4 | 20 | 85% | 14.4 | 72% | 0.89 | 2.57 |
| 12 | 4 | 10 (leave) | 70% | 14.4 | 144% | never clears | growing |

`a_min` is 58.3% for 12 writers and 79.2% for 24; `a_1day` is 68.8% and 84.4%.

**First screen.** The "Lecture 60%" preset with the caption: "One more answer in ten. How much sooner does the writer hear back?" The first nudge of the slider to 70% should visibly collapse the card stack.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (cards appear without animation). The "never clears" region uses a hatch pattern as well as colour. No game art or logos.
