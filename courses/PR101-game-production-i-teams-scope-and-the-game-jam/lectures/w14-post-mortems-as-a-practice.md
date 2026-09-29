# PR101 · Week 14 — Post-Mortems as a Practice

**Why this matters:** Next week you hand in your final game and its post-mortem, which is 20% of this course. You already wrote one post-mortem, for the jam. If your final post-mortem lists the same problems, the first one was a diary entry, not a lesson. This week is about turning post-mortems from a document you write once into a habit that changes what your team does on the next project.

**You will be able to:**
- Code a set of post-mortem problems into categories and compute a Pareto table: each category's share, the running total, and how many categories it takes to reach 80%.
- Explain, using the Politowski dataset of 200 published post-mortems, why the level of your categories changes which problem looks biggest.
- Compute a lesson recurrence rate between two projects and write action items that someone can check.
- Rewrite a blaming post-mortem line as a blameless one, and critique a published post-mortem for what it leaves out.

**Before class:** Politowski, Petrillo, Ullmann and Guéhéneuc, "Game Industry Problems: An Extensive Analysis of the Gray Literature" (arXiv 2009.02440, 2020-2021), sections 2 and 3 and the first four subsections of section 4 (about 30 minutes). Google, *Site Reliability Engineering* (2016), chapter 15, "Postmortem Culture: Learning from Failure" (15 minutes). John Allspaw, "Blameless PostMortems and a Just Culture", Etsy Code as Craft blog, 22 May 2012 (10 minutes). Bring your team's week 9 jam post-mortem.

**Prerequisites from earlier courses:** [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (a post-mortem is the slowest loop you run, one turn per project). [MA102 week 13, sampling and why n = 5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why one team's two post-mortems prove little). From this course, [week 9, the jam post-mortem and its cone of uncertainty](w09-jam-post-mortem.md); [week 10, bug tracking](w10-bug-tracking-and-qa-basics.md) (categories and severity for bugs); and [week 13, builds and release checklists](w13-builds-and-release-checklists.md) (every escaped release problem becomes a checklist line).

**Interactive:** [w14-postmortem-pareto.html](../examples/w14-postmortem-pareto.html). Keep it open during section 2.

---

## 1. From a document to a practice

A **post-mortem** is a written review of a finished project (or a finished milestone, or a failed release) that records what happened, why, and what to do differently. The name comes from medicine, where it means an examination after death, and game developers use it even for projects that went well. You met its short-cycle cousin in week 5. A sprint **retrospective** looks back over two weeks and changes the next sprint. A post-mortem looks back over a whole project and is meant to change the next project.

The format most of you know comes from the website Gamasutra (now Game Developer), which published developers' post-mortems across the whole period the study below samples, 1997 to 2019. They usually have two lists, "what went right" and "what went wrong", often written by a lead or senior developer soon after launch. This course's readings include a selection from that archive.

One post-mortem on its own has a basic weakness. It describes one project, and one project can teach you almost anything, because you can't tell the problems that will recur from the ones that were bad luck. A **practice** adds three things the single document lacks.

1. **A shared category list.** If the jam post-mortem says "we ran out of time" and the final one says "the schedule slipped", are those the same problem? You can only count what you name the same way. Researchers call assigning categories to free text **coding**.
2. **A store.** Post-mortems go in one place where the next team can find them. Google's SRE book describes adding each finished postmortem to a team or organization repository of past incidents, so others can learn from it.
3. **A loop.** Each lesson becomes an action item with an owner, and the next post-mortem checks whether the problem came back.

Section 2 is about the first two, using the largest public store of game post-mortems we have. Section 4 is about the loop.

## 2. Worked example: what 200 post-mortems complain about

### The hook

Cristiano Politowski and three colleagues read 200 post-mortems published on Gamasutra between 1997 and 2019. They focused on the "what went wrong" sections and coded every problem they found. They got 927 problems in 20 types. Two findings should bother you as a future producer. First, production problems stayed at a steady share across 23 years, so a whole industry writing post-mortems did not make them go away. Second, the most common problem types were technical (116 problems) and game design (112), yet the authors concluded that most of the main root causes were about people, not technology.

Both can be true at once only if the answer to "what's the biggest problem?" depends on how you group the problems. That's the lesson of this example. The categories you choose decide the lesson you draw.

### The model

A **Pareto table** sorts categories by how often they occur and adds a running total. It's named after the economist Vilfredo Pareto. The "80/20 rule" people attach to it says a few causes account for most of the effect. Whether that's true for your data is something the table tells you, not something you assume.

- `n_i` is the number of problems coded to category `i`.
- `N = Σ n_i` is the total number of problems.
- `s_i = n_i / N` is category `i`'s **share**.
- Sort the categories from largest `n_i` to smallest (break ties alphabetically so everyone gets the same order). The **cumulative share** of the top `k` categories is `C_k = (n_(1) + n_(2) + ... + n_(k)) / N`.
- The **vital few** is the smallest `k` with `C_k ≥ 0.8`. If the 80/20 rule held, `k` would be about 20% of the number of categories.

```
s_i  = n_i / N
C_k  = sum of the k largest n_i, divided by N
k_80 = smallest k with C_k ≥ 0.80
```

### Numbers you can check

Here are Politowski's 20 problem types with the counts from their Figure 3b, sorted. The counts add up to exactly 927. The shares below are computed from those counts. The paper prints slightly lower percentages beside each bar (11% for technical, for example), so use the counts, which you can check.

| Rank | Type | Problems `n_i` | Share `s_i` | Cumulative `C_k` |
|---|---|---|---|---|
| 1 | Technical | 116 | 12.5% | 12.5% |
| 2 | Game design | 112 | 12.1% | 24.6% |
| 3 | Team | 84 | 9.1% | 33.7% |
| 4 | Tools | 74 | 8.0% | 41.6% |
| 5 | Planning | 73 | 7.9% | 49.5% |
| 6 | Marketing | 61 | 6.6% | 56.1% |
| 7 | Communication | 53 | 5.7% | 61.8% |
| 8 | Testing | 48 | 5.2% | 67.0% |
| 9 | Cutting features | 45 | 4.9% | 71.8% |
| 10 | Bugs | 34 | 3.7% | 75.5% |
| 11 | Scope | 34 | 3.7% | 79.2% |
| 12 | Crunch time | 31 | 3.3% | 82.5% |
| 13-20 | Delays, feature creep, monetization, documentation, budget, prototyping, multiple projects, security | 162 | 17.5% | 100.0% |

Check two rows by hand. Technical: `116 / 927 = 0.125`. After four types: `(116 + 112 + 84 + 74) / 927 = 386 / 927 = 0.416`.

Now read the table as a producer. The top 4 types, 20% of the categories, cover 41.6% of the problems, not 80%. You need 12 of the 20 types to pass 80%. At this level of grouping, game development problems are **spread out**. There's no single thing to fix.

This script builds the table and finds `k_80`. Run it and then change the counts to your own team's.

```python
types = {
    "technical": 116, "game design": 112, "team": 84, "tools": 74,
    "planning": 73, "marketing": 61, "communication": 53, "testing": 48,
    "cutting features": 45, "scope": 34, "bugs": 34, "crunch time": 31,
    "delays": 29, "feature creep": 27, "monetization": 26,
    "documentation": 22, "budget": 21, "prototyping": 19,
    "multiple projects": 16, "security": 2,
}

def pareto(counts):
    total = sum(counts.values())
    rows, running = [], 0
    for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        running += n
        rows.append((name, n, n / total, running / total))
    return rows

def vital_few(rows, threshold=0.8):
    for k, row in enumerate(rows, start=1):
        if row[3] >= threshold:
            return k

rows = pareto(types)
print(f"{sum(types.values())} problems in {len(types)} types")
for k, (name, n, share, cum) in enumerate(rows[:5], start=1):
    print(f"{k:2} {name:15} {n:4} {share:6.1%} {cum:6.1%}")
print("types needed for 80%:", vital_few(rows))
print("top 4 types (20% of 20) cover:", f"{rows[3][3]:.1%}")
```

It prints:

```
927 problems in 20 types
 1 technical        116  12.5%  12.5%
 2 game design      112  12.1%  24.6%
 3 team              84   9.1%  33.7%
 4 tools             74   8.0%  41.6%
 5 planning          73   7.9%  49.5%
types needed for 80%: 12
top 4 types (20% of 20) cover: 41.6%
```

### Looking inside the buckets

Now open the two biggest-looking buckets. Politowski and colleagues also coded each problem's **sub-type**, which they call its root cause, and list the counts in their appendix. (The sub-type counts come from separate tables and don't add up to the type totals, so compare them with each other, not with the table above.)

| Type | Sub-types listed | Largest sub-types |
|---|---|---|
| Technical | 18 | Platform and technology constraints 24, optimization and performance 17, game engine and libraries 13 |
| Game design | 7 | Unclear game design vision 28, lack of fun 27, game design complexity 23 |
| Team | 6 | Insufficient workforce 49, environment problems 48, unexpected team disruption 11 |

"Technical" tops the type chart because it's a **wide bucket**. It collects 18 different root causes, from porting to physics to build times, and none of them is large. "Team" is a **narrow bucket**. Two root causes dominate it, and each one alone is about twice the size of the largest technical sub-type. The paper's own top-10 list of sub-types starts with insufficient workforce (49), environment problems (48), wrong marketing strategy (35) and underestimation (34). Only 2 of the 10 (platform and technology constraints, 24, and inadequate or missing tools, 22) are about technology.

So the two findings from the hook don't conflict. Group coarsely and technology looks like the biggest problem. Group by root cause and people do. Neither view is wrong. They answer different questions. "Which area of our pipeline generates the most complaints?" wants the type view. "Which single change would remove the most problems?" wants the root-cause view.

### Move it yourself

Open the interactive. The left view is the Pareto chart of the 20 types: sorted bars, a cumulative line, and a dashed line at 80% with `k_80 = 12` marked where the line crosses it. It looks like a list of 20 roughly equal complaints. Click the "technical" bar and the right view opens it: 18 short bars. Click "team" and the right view shows 6 bars, two of them taller than anything inside technical. Switch the right view to "Top 10 root causes" and the order of the left chart falls apart. Finally, switch the left view to "Your team", type in the counts from your jam post-mortem, and watch `k_80` for your own data.

### Cross-game recognition

Counting coded reports to find what recurs is the same move in every field that learns from its failures.

**Google's postmortem repository.** The SRE book says Google writes a postmortem when an incident crosses predefined triggers, such as user-visible downtime beyond a threshold or data loss of any kind, and then adds it to a shared repository. The triggers do the job our category list does. They decide what gets counted before anyone knows the outcome, so the store isn't filled only with the incidents people felt like writing up. A repository of consistently triggered reports is what lets you build a Pareto table at all.

**NASA's Aviation Safety Reporting System.** Pilots, controllers and others submit voluntary, confidential incident reports. The program analyzes them, issues alerts to people who can fix the problems it finds, and keeps a public database. Its program briefing notes that over two-thirds of aviation accidents and incidents are generally held to have their roots in human performance errors. That's the same shape as Politowski's result. Code incidents by component (engine, radio, runway) and the equipment categories fill the chart. Code them by root cause and people dominate.

**Your week 10 bug tracker.** Sort your team's bugs by the component field and you get a Pareto table of bugs. The same trap applies. A component called "gameplay" is a wide bucket that will top the chart. Splitting it into "input", "collision" and "state machine" may show that one small script produces most of the bugs.

Three settings, one model. Code, count, sort, and read the running total. Then check whether the top of the chart is a real cause or just a wide bucket.

### Eyes-open design judgment

- **Categories are a design decision.** Wide buckets win Pareto charts. Before you trust the top bar, ask how many different causes it holds. A good category is narrow enough that one kind of action could fix it.
- **Frequency isn't cost.** The table counts mentions. One "insufficient workforce" problem can cost a month; one "documentation" problem can cost an afternoon. When you pick what to fix, weigh the count by a rough cost, even if it's just small, medium or large.
- **Small samples lie.** Politowski's list stabilized after about 140 post-mortems, meaning new ones stopped adding new types. Your team has two post-mortems. With five problems in each, one problem moves a share by 20 points (MA102 week 13). Use your own counts to start a conversation, not to settle one.
- **The archive is biased.** Published post-mortems are written by people who shipped, often soon after launch, and often for an audience. They say little about projects that never shipped. MMO407 week 12 shows how to add the missing comparison group ([MMO407 week 12, writing a post-mortem](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md)); for now, don't read "most often mentioned" as "most important".
- **Code before you argue.** Two people coding the same list separately, then comparing, surfaces disagreements that a single author would bury. The researchers here had each author code post-mortems and then discussed until they reached consensus on the types.

### Check this example

1. A team codes 40 problems from its projects: scope 12, communication 9, tools 6, bugs 5, planning 4, audio 2, documentation 2. Compute the cumulative shares and `k_80`. Does the 80/20 rule hold here?
2. The same team splits "scope" into "overambitious scope" (7) and "late design changes" (5). What happens to the top of the chart and to `k_80`?
3. Why can't you add the sub-type counts in the "inside the buckets" table to get the type counts?

<details>
<summary>Answers</summary>

1. Cumulative: 30.0%, 52.5%, 67.5%, 80.0%, 90.0%, 95.0%, 100%. `k_80 = 4` of 7 categories (57%). The top 20% of categories (1.4, so one or two) cover 30% to 52.5%, so the 80/20 rule doesn't hold.
2. Communication (9) becomes the top bar, followed by overambitious scope (7), tools (6), then bugs and late design changes (5 each). Cumulative after five: `(9 + 7 + 6 + 5 + 5) / 40 = 80%`, so `k_80 = 5` of 8. Splitting a wide bucket drops it down the chart, which is the point of section 2.
3. The paper reports them in separate tables, and they don't sum to the type totals (for example, the listed technical sub-types sum to more than 116). Some problems may carry more than one sub-type. Compare sub-types with each other only.

</details>

## 3. Writing it blameless

A post-mortem stops working the day people learn that it's used to find someone to blame. They stop writing down what really happened, and the store fills up with safe, vague lines. The SRE book defines a **blameless** postmortem as one that focuses on the contributing causes without indicting any individual or team, and that assumes everyone involved had good intentions and did the right thing with the information they had. Allspaw's 2012 Etsy post makes the same argument for engineers. If people are punished for honest accounts of mistakes, the organization loses the accounts.

Blameless doesn't mean nobody is responsible. It means the post-mortem asks what the system let happen, not who was careless. In practice it changes the questions you ask.

| Blaming question | Blameless question |
|---|---|
| Who uploaded the broken build? | What in our release process let a broken build be uploaded? |
| Why didn't the artist tell anyone the animations were late? | What made it hard to see that the animations were late? |
| Who agreed to that scope? | What did we know about our speed when we agreed to that scope, and where did it come from? |

Here is one line from a student team's draft, and a blameless rewrite.

- **Draft:** "Sam pushed untested code the night before the deadline and broke the build."
- **Rewrite:** "At 23:00 on the last night, a fix was merged to `main` without a smoke test, because we had no rule about merges after the freeze and everyone was fixing bugs in parallel. The web export failed to load. Action item: after feature freeze, merges to `main` need a second person to run the week 13 smoke test (owner: producer; check: freeze rule in the checklist before the next jam)."

The rewrite has more information, not less. It has the time, the missing rule, the effect and an action item. It also points at the one thing the team can change. Sam will be just as tired next time. The rule can be different.

Two cautions. First, blameless writing is harder when the problem really is one person's behaviour, such as someone who stopped showing up. Week 11 covered how to handle that directly and early. The post-mortem records the effect on the project and what the team will do about workload next time; it isn't the place to settle a conflict. Second, in a course with peer review (10% of your grade here), keep the two apart. The post-mortem is about the project. Peer review is about contributions, and it's confidential.

## 4. Closing the loop: action items and recurrence

A lesson counts as learned when the problem doesn't come back. You can measure that.

### Action items that can be checked

Every "what went wrong" item should end in at most one **action item** with three parts: an **owner** (one named person), a **change** (a rule, a checklist line, a tool, a habit), and a **check** (when and how someone will see whether it happened). "Communicate better" fails all three. "At every standup, each person says the one thing blocking them; owner Priya; check at the week 3 retro whether any blocker was reported later than a day" passes.

Week 13 gave you the cleanest example of this. When a problem escapes into a release, the action item is a new or tighter checklist line, and the check is the next release run. That's how the checklist's coverage `v` climbs.

### The recurrence rate

Take the set of problem categories in project 1's "what went wrong" list and the set in project 2's. The **recurrence rate** is the share of project 1's categories that show up again in project 2:

```
R = |C1 ∩ C2| / |C1|
```

`C1` and `C2` are the sets of categories, and `|C1 ∩ C2|` is how many appear in both. `R = 0` means nothing came back. `R = 1` means every lesson from project 1 was ignored.

Here is an invented but typical example. A team's jam post-mortem (project 1), coded with Politowski's types, listed scope, planning, communication, bugs and crunch time. The team wrote five action items and completed three of them: a cut list at the start (scope), a "no new features after Saturday noon" rule (crunch time), and a bug board (bugs). The planning and communication items ("estimate better", "talk more") were never turned into anything checkable. The final project's post-mortem (project 2) lists planning, testing, communication and tools.

| Jam category | Action item done? | Back in the final project? |
|---|---|---|
| Scope | Yes (cut list) | No |
| Crunch time | Yes (feature freeze) | No |
| Bugs | Yes (bug board) | No |
| Planning | No ("estimate better") | Yes |
| Communication | No ("talk more") | Yes |

`R = 2 / 5 = 40%`. The **closure rate**, the share of action items actually done, is `3 / 5 = 60%`. In this table every closed item stayed away and every open item came back. Five items prove nothing statistically. But the pattern is the one to look for, and it's the argument for writing action items someone can check. Testing and tools are new problems. They're the next post-mortem's input, not failures of this one.

Lab 14 computes both numbers from your team's real post-mortems.

## In-class activity (25 minutes)

In pairs, from two different jam teams.

1. **Code separately (10 minutes).** Each of you takes both teams' week 9 jam post-mortems and codes every "what went wrong" item with one of Politowski's 20 types (the list is in lecture section 2). Don't talk while coding.
2. **Compare (5 minutes).** Count the items where you chose the same type. Compute your **percent agreement**, matching items divided by total items. Discuss every disagreement and agree on one type.
3. **Class Pareto (10 minutes).** Enter your agreed counts into the shared class sheet. The instructor loads the class totals into the interactive's "Your team" mode. As a class, find `k_80` and open the top bar. Is it a wide bucket?

Expected output: your pair's coded list, your percent agreement before discussion, and one sentence on which category you found hardest to code.

## Common misconceptions

- **"The biggest bar is the biggest problem."** The biggest bar may be the widest bucket. Open it before you act. In Politowski's data, technical is the top type while the top root causes are about people.
- **"80/20 always holds."** It's a pattern some data shows, not a law. The 200-post-mortem data needs 12 of 20 types to reach 80%.
- **"Blameless means nobody is accountable."** Blameless post-mortems still produce action items with named owners. What they avoid is punishing people for honest accounts.
- **"We wrote the post-mortem, so we learned the lessons."** A lesson is learned when the problem doesn't recur. Measure it with the recurrence rate, and close the loop with checkable action items.

## Check yourself

1. Your jam post-mortem lists 6 categories. Your final post-mortem lists 5, and 3 of them were also on the jam list. What is `R`? What would you need to know before calling that good or bad?
2. A team's coded problems: tools 3, scope 3, communication 2, testing 1, bugs 1. Break ties alphabetically. Write the Pareto table and give `k_80`.
3. Rewrite as blameless, with an action item: "Alex forgot to include the music folder in the export, so the build had no sound."
4. A producer reads that "technical" is the most common problem type in 200 post-mortems and proposes hiring another programmer. Using section 2, give one reason that may not help and suggest what to look at first.

<details>
<summary>Answers</summary>

1. `R = 3 / 6 = 50%`. You'd want to know which categories recurred, whether their action items were closed, and whether the final project was much larger (a bigger project gives problems more chances to recur). One pair of projects is a tiny sample.
2. Scope and tools tie at 3, so scope comes first alphabetically. Scope 3 (30%, 30%), tools 3 (30%, 60%), communication 2 (20%, 80%), bugs 1 (10%, 90%), testing 1 (10%, 100%). `k_80 = 3`.
3. For example: "The release build had no music because the export preset's resource filter excluded the `music/` folder, and nothing in our process compared the build's contents with our asset list. Action item: add an asset-manifest check to `release_check.py`; owner: build owner; check: the next RC fails if any manifest file is missing."
4. "Technical" is a wide bucket of 18 small root causes, from porting to physics, so no single hire addresses most of it. Look at the sub-types (and at your own team's) first. The largest root causes in the dataset are insufficient workforce and team environment. More people might help the first, but not by fixing "technical" as such.

</details>

## Lab / assignment hook

[Lab 14, coding post-mortems and closing the loop](../labs/lab14.md). You finish a small Python tool that builds Pareto tables and recurrence rates from coded post-mortem data, check it against Politowski's counts, then code your own team's jam and final-project problems and write checkable action items. The coded data and action items go straight into your week 15 post-mortem.

## Sources

- Politowski, C., Petrillo, F., Ullmann, G. C. & Guéhéneuc, Y.-G. "Game Industry Problems: An Extensive Analysis of the Gray Literature." Preprint submitted to Elsevier, arXiv:2009.02440v3 (posted September 2020, revised January 2021; read September 2026). 200 Gamasutra post-mortems from 1997 to 2019; 927 problems in 20 types; type counts from Figure 3b; production problems constant over time; main root causes related to people; list of types stable after about 140 post-mortems; authors coded separately and reached consensus; top-10 sub-types in Table 3; sub-type counts in appendix Tables 7 to 9. Also its summary of Washburn et al. (2016), 155 post-mortems, and its description of "what went right" and "what went wrong" sections.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 15, "Postmortem Culture: Learning from Failure": postmortem triggers (user-visible downtime beyond a threshold, data loss of any kind, and others), definition of a blameless postmortem, and the shared repository of past incidents. Free online at sre.google.
- Allspaw, J. "Blameless PostMortems and a Just Culture." Etsy Code as Craft, 22 May 2012.
- NASA Aviation Safety Reporting System, "Program Briefing" (asrs.arc.nasa.gov, read September 2026). Voluntary incident reports from pilots, controllers and others; analysis and alerting; public database; the statement that over two-thirds of aviation accidents and incidents are generally held to have roots in human performance errors.

## Interactive spec: examples/w14-postmortem-pareto.html

**The one insight.** The top of a Pareto chart depends on how wide the categories are. "Technical" leads the type chart because it's a wide bucket of many small causes; open it and "team" holds bigger single causes.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view first).

1. **Left view, Pareto chart.** Vertical bars sorted by count (ties alphabetical), labelled with name and count, plus a cumulative-share line with dots on a right-hand 0-100% axis. A dashed horizontal line at the threshold (default 80%) and a vertical marker at `k_80` with the label "k₈₀ = 12 of 20 types". Above the chart, large text: "Top 20% of categories cover 41.6%". Data sets (segmented control): "200 post-mortems, by type" (default) and "Your team".
2. **Right view, inside a bucket.** When a type bar is selected (click, or arrow keys plus Enter), show horizontal bars of its sub-types from the table below, sorted, with a caption "Technical: 18 root causes, largest 24". A second segmented option, "Top 10 root causes", shows the paper's Table 3 list instead, each bar tagged "people", "design" or "technology" by color (tag mapping below; label it "tags: this course's reading, not the paper's"). A note under the right view, always visible: "Sub-type counts come from separate tables and do not add up to type totals."

**Data.** Types (Politowski et al., Figure 3b): technical 116, game design 112, team 84, tools 74, planning 73, marketing 61, communication 53, testing 48, cutting features 45, bugs 34, scope 34, crunch time 31, delays 29, feature creep 27, monetization 26, documentation 22, budget 21, prototyping 19, multiple projects 16, security 2.

Sub-types (appendix Tables 7 and 8), only for these three types; other type bars show "sub-types not shown in this example":
- Technical (18): platform and technology constraints 24, optimization and performance 17, game engine and libraries 13, network and multiplayer 9, re-work and wasted work 8, build and load time 8, animation and 3D 7, source control and file management 6, porting issues 6, networking complexity 6, programming language and algorithms 5, production pipeline 5, physics and collision 5, novelty and change 5, performance issues 4, patch strategies and infrastructure 4, UI and localization 4, coding/architecture issues 4.
- Game design (7): unclear game design vision 28, lack of fun 27, game design complexity 23, balancing issues 19, lack of polish 13, game too short/simple 10, release/censorship issues 8.
- Team (6): insufficient workforce 49, environment problems 48, unexpected team disruption 11, outsourcing issues 5, inexperienced staff 5, overstaffing 2.

Top 10 root causes (Table 3) with tags: insufficient workforce 49 (people), environment problems 48 (people), wrong marketing strategy 35 (people), underestimation 34 (people), unclear game design vision 28 (design), lack of fun 27 (design), platform and technology constraints 24 (technology), game design complexity 23 (design), inadequate or missing tools 22 (technology), misaligned teams 22 (people).

**"Your team" mode.** An editable table of category name and count (start with 5 empty rows, "Add row" button, up to 20 rows). The chart and readouts recompute on every edit. Prefill button "Example team" loads: scope 12, communication 9, tools 6, bugs 5, planning 4, audio 2, documentation 2.

**Controls.** Data set toggle; threshold slider 50% to 95%, step 5%, default 80%; bar selection by click or keyboard; right-view toggle "Inside selected type" / "Top 10 root causes". All keyboard operable with visible focus.

**Formulas.**

```
N    = sum(n_i)
s_i  = n_i / N
C_k  = sum of the k largest n_i / N      (ties broken alphabetically)
k_T  = smallest k with C_k ≥ T
top20 = C_ceil(0.2 × categories)          (label "Top 20% of categories cover ...")
```

**Readout table** under the chart: rank, category, count, share, cumulative, for all rows, with the `k_T` row highlighted.

**Test values** (must match the lecture).

- Types, T 80%: N 927, k 12, C_4 41.6%, technical share 12.5%, C_5 49.5%, C_11 79.2%, C_12 82.5%.
- Example team, T 80%: N 40, cumulative 30.0, 52.5, 67.5, 80.0, 90.0, 95.0, 100.0; k 4; top 20% = ceil(1.4) = 2 categories cover 52.5%.
- Example team with scope split into "overambitious scope" 7 and "late design changes" 5: top bar communication 9, k 5.

**Behaviour.** Bars and line animate over 200 ms on data change, none under `prefers-reduced-motion`. Colors from `templates/interactive-tokens.css`; the people/design/technology tags use three distinct token colors with a text label on each bar, never color alone. No game art or logos.
