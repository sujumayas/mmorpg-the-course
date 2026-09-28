# GD101 · Week 08 — Iteration loops and kill-your-darlings

**Why this matters:** Most game ideas do not survive contact with players, including the ones you love most. You can't raise the odds that any one idea works by much, but you can raise the number of ideas you try before the deadline, and that is where most of a designer's luck comes from.

**You will be able to:**
- Describe the iteration loop (prototype, playtest, evaluate, decide) and measure your own loop length in days.
- Compute how many loops fit in a schedule and the chance that at least one produces a keeper, for a given hit rate.
- Apply a keep, change or kill decision to a feature using criteria written before the playtest, and explain why effort already spent does not belong in that decision.
- Design a shorter loop for a given design question by cutting what the question does not need.

**Before class:** Fullerton, *Game Design Workshop* (4th ed.), chapter 1 (the iterative process) and the prototyping chapters you started in week 6. Eric Zimmerman, "Play as Research: The Iterative Design Process" (2003), a short essay. Skim the Wikipedia article on the cancelled Blizzard game Titan (see Sources) for the timeline.

**Prerequisites from earlier courses:** [GD101 week 7, playtesting method](w07-playtesting-observe-dont-explain.md), especially section 5 (findings lists) and the complement rule in section 2. [GD101 week 6, paper prototyping](w06-paper-prototyping-cards-dice-boards.md). Exponents and logarithms from [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [MA101 week 5](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md).

**Interactive:** [Iteration clock](../examples/w08-iteration-clock.html). Keep it open during section 2.

---

## 1. The loop

Every design method you will meet in this program is a version of one loop.

1. **Prototype.** Make the smallest thing that can answer a question about your design. In week 6 that meant cards, dice and a board drawn on paper.
2. **Playtest.** Put it in front of people and watch, as in week 7.
3. **Evaluate.** Turn observations into findings and compare them with what you hoped would happen.
4. **Decide.** For each part of the design, keep it, change it, or kill it. Then go back to step 1 with the next question.

Designers call one pass through these four steps an **iteration**, and the process of repeating it **iterative design**. Eric Zimmerman's 2003 essay "Play as Research" describes it as a cycle of prototyping, testing, analyzing and refining, where decisions are made on the basis of the experience of playing the current version rather than on the plan. Fullerton's textbook puts the same loop at the center of its first chapter.

The alternative is sometimes called **waterfall**: write a complete design, build all of it, test at the end. Waterfall works when you can predict the result of a design before building it. Game designers can't, because the thing they are designing (the players' experience, the aesthetics in MDA terms) only exists once people play. So you build a little, play, and learn.

### Loop length

The **loop length**, which we will write as `c`, is the calendar time from starting a prototype to having a decision about it. It includes everything: building, finding testers, running sessions, reading your notes, arguing with your team.

Loop lengths vary by orders of magnitude.

| Kind of loop | Typical loop length |
|---|---|
| Paper prototype, tested with classmates in the same session | under an hour |
| Paper prototype, tested with recruited strangers, findings written up | 1 to 3 days |
| Small digital prototype, a week of programming, one test day | 1 to 2 weeks |
| Playable level of a commercial game, external playtest | several weeks |
| Soft launch of a mobile game to a test country, reading the retention data | months |

These are rough ranges, not measured figures. The point of the table is that the same four steps can take an hour or half a year, and the difference decides how many ideas you can try before the deadline.

## 2. Worked example: the loop clock

### The hook

In late 1997 Valve had most of a game. Half-Life was scheduled for November of that year. According to Ken Birdwell's account, by late September the team concluded that the game was not fun, and they made what he calls a painful decision to start over and rework every part of it. A small group pulled the promising pieces into one prototype level, and that level became the base for the game Valve shipped in late 1998.

Twelve years later, a small Finnish studio released a mobile game about birds and pigs on iOS in December 2009. By then Rovio had, per its history, developed 51 games for other publishers. Angry Birds was its 52nd game.

Both stories have the same shape. The keeper came only after many attempts that were not keepers. This worked example turns that shape into a number you can plan with.

### The model

Assume, as a planning simplification, that each loop on a new idea has the same chance `q` of producing a **keeper**: a result good enough to build on. Call `q` the **hit rate**. You have a schedule of `T` days and a loop length of `c` days. Then:

```
loops that fit     I = floor(T / c)
P(at least one keeper) = 1 − (1 − q)^I
expected loops to the first keeper  = 1 / q
expected days to the first keeper   = c / q
```

- `q` is the hit rate per loop, between 0 and 1.
- `T` is the time you have, in days.
- `c` is your loop length, in days.
- `I` is the number of complete loops that fit.
- `floor` rounds down, because a half-finished loop gives you no decision.

The second line is last week's complement rule, with loops in place of testers. The chance a loop fails is `1 − q`, the chance all `I` loops fail is `(1 − q)^I`, and at least one keeper is everything else. The third line comes from a fact you will prove in MA102 [week 7](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md): if each try succeeds with chance `q`, the average number of tries until the first success is `1/q`. A 10% hit rate means ten loops on average.

The hit rate is the part you can barely change. Experience helps, taste helps, but nobody reliably predicts which paper prototype will be fun. The loop length is the part you control.

### Numbers you can check

Take a 60-day schedule and a hit rate of 10%, meaning one idea in ten survives a playtest well enough to keep. Vary only the loop length.

| Loop length `c` | Loops that fit `I` | P(at least one keeper) | Expected days to first keeper `c/q` |
|---|---|---|---|
| 1 day | 60 | 99.8% | 10 |
| 3 days | 20 | 87.8% | 30 |
| 7 days | 8 | 57.0% | 70 |
| 14 days | 4 | 34.4% | 140 |
| 30 days | 2 | 19.0% | 300 |

Check a row by hand. For `c = 7`, `I = floor(60/7) = 8`, `0.9^8 = 0.4305`, and `1 − 0.4305 = 0.5695`, or 57.0%. The expected wait, 70 days, is longer than the whole schedule, which is why the chance of success is only just above a coin flip.

The per-loop odds are identical in every row. Every single loop is a 10% shot. What changes is how many shots you get. A team with one-day paper loops and a team with one-month digital loops can have exactly the same talent and the same taste. After 60 days, the first team almost certainly has something worth building on. The second team, four times out of five, does not.

The same effect holds for other hit rates. With `T = 60` days:

| Loop length `c` | q = 0.05 | q = 0.10 | q = 0.20 |
|---|---|---|---|
| 1 day | 95.4% | 99.8% | 100.0% |
| 3 days | 64.2% | 87.8% | 98.8% |
| 7 days | 33.7% | 57.0% | 83.2% |
| 14 days | 18.5% | 34.4% | 59.0% |
| 30 days | 9.8% | 19.0% | 36.0% |

Look at the diagonal from `q = 0.20, c = 14` (59.0%) to `q = 0.10, c = 7` (57.0%) to `q = 0.05, c = 3` (64.2%). Halving your hit rate and halving your loop length roughly cancel. If you are not sure you are twice as talented as the team next door, you can still be twice as fast.

### Averages hide the waiting

"Ten loops on average" does not mean ten loops is typical. The number of loops to the first keeper is skewed: many teams get lucky early and a few wait a very long time. With `q = 0.1`, the median is seven loops (`1 − 0.9^7 = 52.2%`, the first count past one half), and about one team in eight still has nothing after twenty loops (`0.9^20 = 12.2%`). If your loop is a month long, the unlucky team is out of time for years.

### The visual

Open [`examples/w08-iteration-clock.html`](../examples/w08-iteration-clock.html). The left view shows a single loop as a coloured bar with a label "10% chance of a keeper." Change the loop length and the bar gets shorter or longer, but its label never changes. The right view plots, against calendar days, the chance that a team has found at least one keeper so far, with one curve per loop length. Drag the loop-length slider from 30 days down to 1 and watch the curve for your team climb from the bottom of the chart to the top. The simulation button runs 20 teams with the same settings and marks the day each one found its first keeper, so you can see the long tail for yourself.

### Cross-game recognition

**Rovio (Finland, up to 2009).** Rovio's 51 earlier games were largely work for other publishers, so they were not 51 failed attempts at Angry Birds. They were, though, 51 complete production loops before the studio's first original hit. The studio built its skill and its tools on those loops. Read the story as "many loops before the keeper," not as "51 failures."

**Supercell (Finland, 2010 onward).** Supercell is known for killing games in or before soft launch, and the company treats these cancellations as something to celebrate rather than hide. As of September 2026, Wikipedia's list of Supercell games shows seven titles that reached global release (one of them, Squad Busters, is scheduled to shut down in 2026) and more than a dozen discontinued ones, including Spooky Pop, Smash Land and Rush Wars. Discontinued games outnumber released ones. In our model, a soft launch is one very long, very expensive loop, with an honest keep-or-kill decision at the end. Supercell's approach is to accept a low hit rate and make sure the kill decision actually happens.

**Blizzard, Titan to Overwatch (2007 to 2016).** Blizzard worked on an MMO code-named Titan from 2007. By 2013 the team had grown past 140 people. In May 2013 Blizzard rebooted the project, and it publicly cancelled Titan in September 2014. Around 40 people stayed, and they were given roughly six weeks to come up with a new concept. They built a team-based shooter prototype using pieces of Titan, which became Overwatch, released May 24, 2016. In loop terms, Titan was one loop that lasted about six years and ended in a kill. The next loop was six weeks long and produced a keeper. Mike Morhaime later said the company had failed to control the game's scope, which is another way of saying the loop had grown too long to give feedback.

**Valve, Half-Life (1997).** The restart in September 1997 was a kill decision on roughly a year of work, followed by a short loop on a single prototype level. It is the same move as Blizzard's, a decade earlier and on a smaller scale.

Four studios, one line of algebra. When you hear a success story, count the loops that came before it and ask how long each one took.

### Eyes-open design judgment

- **The hit rate is not fixed.** Real ideas are not independent coin flips. An idea that failed three playtests is probably worse than a fresh idea, and a change informed by week 7 findings is probably better than a random new idea. Use the model for planning ("how many loops do we need?"), not as a claim that learning doesn't happen.
- **Short loops answer small questions.** A one-hour paper loop can tell you whether a trading rule is understood. It can't tell you whether a 40-hour campaign is paced well. Match the loop to the question. Section 4 is about doing that.
- **A loop without a real decision is not a loop.** If every playtest ends with "keep going, it'll get better," your effective `I` is zero no matter how often you test. This is where kill-your-darlings comes in.
- **Survivor stories are biased.** You hear about Rovio and Overwatch because they succeeded. Many studios ran many loops and never found a hit. More loops raise your odds. They do not guarantee anything, and 99.8% is not 100%.

## 3. Kill your darlings

"Kill your darlings" is an old piece of writing advice: be willing to cut the passage you are proudest of when the work is better without it. In game design, a **darling** is a mechanic, level, character or idea you are attached to for reasons that have nothing to do with how it plays. You invented it. It was the first thing you drew. You spent three weekends on it.

### The sunk cost trap

Look at the model in section 2 again. The chance that the next loop produces a keeper depends on `q`, on `c` and on the time left. The days you already spent appear nowhere in it. That is not an oversight. Effort already spent, called **sunk cost**, cannot be recovered whatever you decide next, so it should not change what you decide next.

People find this hard. "We've spent three weeks on the crafting system, we can't cut it now" feels like a reason. It isn't one. The only question is whether the next week is better spent on crafting or on something else. The three weeks are gone either way.

Blizzard's Titan is the extreme case: roughly six years and more than a hundred developers, cut in favour of a six-week prototype. Valve's restart in 1997 is the same decision at the scale of one year. Both teams could have argued "we've come too far to stop." Both would have shipped a worse game.

### Write the kill criteria before the test

The practical defence against the sunk cost trap is to decide *before* the playtest what result would make you keep, change or kill a feature. You are at your most honest before you see the data and before you have spent another week on it.

A **kill criterion** is a specific, observable result, written in the language of your week 7 findings, that would lead you to cut the feature. For example, for a trade action in a card game:

| Decision | Criterion (written before testing, 5 silent testers) |
|---|---|
| Keep | At least 3 of 5 testers trade by round 3 without prompting, and at least 2 describe trading as a choice they thought about in the debrief. |
| Change | 1 or 2 of 5 trade, or testers trade but say it felt automatic. Try one change aimed at the finding, then retest. |
| Kill | 0 of 5 trade after two change loops, or trading produces a severity-3 finding (a stalled game) twice. |

Notice what the table does. It turns an argument about taste into a check against evidence. It also puts a limit on "change": two loops, then a decision. Without that limit, "change" becomes the place darlings go to live forever.

### What killing actually means

Killing a feature rarely means throwing everything away. Valve kept its promising pieces and built the new prototype level from them. The Overwatch team reused Titan's art and ideas. A killed mechanic goes into a notebook, sometimes called a **design graveyard** or idea bank, with the findings that killed it. Some ideas come back years later in a game where they fit.

Kill decisions also apply to small things. The most common darling in a student prototype is not a whole game. It is one rule, one card, or one bit of flavour that the designer keeps explaining to testers in the debrief. If you find yourself explaining it every time, week 7 already told you what that means.

## 4. Shortening the loop

Since loop length is the part you control, most practical iteration advice is really advice about cutting `c`. Here are five techniques. For each, the key is to ask what the current question needs and cut everything else.

1. **Test one question per loop.** Write the question at the top of the prototype sheet. "Do players understand trading?" needs a trading rule and something to trade. It does not need art, a scoring track, or a full deck.
2. **Stay on paper as long as the question allows.** If a question is about rules, choices or balance, paper answers it in hours. Move to digital only for questions paper cannot answer: real-time timing, feel, animation, large hidden calculations.
3. **Fake it.** A **Wizard of Oz prototype** is one where a human secretly does the work the finished system would do. The designer plays the "AI opponent" by following a written rule sheet, or flips cards to simulate a random event table. You learn whether the system is worth building before building it.
4. **Test the riskiest part first.** Order your loops so the idea most likely to fail gets tested first. If the core loop isn't fun, knowing that in week 2 is worth far more than knowing it in week 10.
5. **Fix between testers, not between rounds.** The RITE method from week 7 changes the build as soon as a problem is clearly seen. In loop terms, it shrinks `c` to a single session.

### A worked calculation

Your team has 60 days and a digital prototype loop of 14 days. From the table in section 2, with `q = 0.10`, that gives four loops and a 34.4% chance of at least one keeper. You decide to answer the first rules questions on paper with a three-day loop for the first 30 days, then use the last 30 days for two 14-day digital loops on whatever survives.

- Paper phase: `floor(30/3) = 10` loops, `1 − 0.9^10 = 65.1%` chance of a keeper.
- Digital phase: 2 loops, `1 − 0.9^2 = 19.0%` chance of a keeper on the digital questions alone.
- Chance at least one phase finds a keeper: `1 − 0.9^12 = 71.8%`.

The mixed plan roughly doubles the odds of the all-digital plan (71.8% against 34.4%) with the same people and the same 60 days. It also means the digital loops start from a paper design that has already survived ten rounds of playtesting.

## 5. The iteration log

Keep a written record of every loop. An **iteration log** (also called a design change log) has one entry per loop with five fields:

1. **Question.** What this loop was meant to answer.
2. **Change.** What you changed from the last version, and why (link the finding).
3. **Kill criteria.** Written before the test.
4. **Result.** Key findings with counts ("4 of 5").
5. **Decision.** Keep, change or kill, and the next question.

The log does three jobs. It forces the kill criteria to exist before the test. It gives you evidence when a teammate says "we tried that already." And it is most of the material for your playtest reports and your final paper game showcase. Lab 08 gives you a template.

## In-class activity (25 minutes)

Groups of three or four, using the findings list you produced in lab 07 or the sample findings the instructor hands out.

1. (5 min) Pick the two findings with the highest severity. For each, write one design question the next loop should answer.
2. (8 min) For one of the questions, write a keep / change / kill table like the one in section 3, with criteria a silent five-tester playtest could check.
3. (7 min) Design the shortest loop that could answer the question. Name what you would cut from the current prototype and estimate `c` in hours.
4. (5 min) Swap tables with another group. Find one criterion that could not actually be observed in a silent playtest, and rewrite it so it can.

**Expected output:** two design questions, one decision table with observable criteria, one loop plan with an estimated length, and one rewritten criterion from the other group.

## Common misconceptions

- **"Good designers get it right the first time."** Published accounts from Valve, Blizzard and Supercell describe the opposite: many loops, frequent restarts and planned kills. What experienced designers do better is run short loops and decide honestly at the end of each one.
- **"We've invested too much to cut it now."** That is the sunk cost trap. The investment is gone whatever you choose. Compare only the future: what will the next loop teach, and what else could that time do?
- **"Changing it is safer than killing it."** An endless series of small changes is a slow way of never deciding. Put a limit on change loops in the criteria, before testing.
- **"Shorter loops mean lower quality."** Short loops answer small questions quickly. Quality comes from the number of honest decisions you make, and short loops give you more of them.

## Check yourself

1. A team has 45 days, a loop length of 5 days and a hit rate of 15%. How many loops fit, and what is the chance of at least one keeper? What is the expected number of days to the first keeper?
2. With `q = 0.1` and a 60-day schedule, what is the longest loop length, in whole days, that gives at least a 90% chance of a keeper?
3. A teammate says "The crafting system took four weeks, so we should give it at least two more weeks of polish before we decide." Rewrite this as a decision that ignores sunk cost, using the kill-criteria format from section 3.
4. Team A has a 20% hit rate and a 14-day loop. Team B has a 10% hit rate and a 7-day loop. Over 56 days, which team is more likely to have found a keeper? Show the numbers.

<details>
<summary>Answers</summary>

1. `I = floor(45/5) = 9`. `1 − 0.85^9 = 1 − 0.2316 = 0.7684`, about 76.8%. Expected days to first keeper `c/q = 5/0.15 = 33.3` days.
2. Solve `1 − 0.9^I ≥ 0.9`: `I ≥ ln(0.1)/ln(0.9) = 21.85`, so at least 22 loops. `60/22 = 2.73`, so the loop must be at most 2 whole days (30 loops, `1 − 0.9^30 = 95.8%`). A 3-day loop gives only 20 loops and 87.8%.
3. Example: "Before the next playtest, we agree: keep crafting if at least 3 of 5 testers craft an item by round 4 without prompting; change it once if 1 or 2 do; kill it if none do after one change loop." The four weeks already spent do not appear in any criterion.
4. Team A: `floor(56/14) = 4` loops, `1 − 0.8^4 = 59.0%`. Team B: `floor(56/7) = 8` loops, `1 − 0.9^8 = 57.0%`. Team A is slightly ahead, 59.0% against 57.0%. Doubling the hit rate and doubling the loop length almost cancel.

</details>

## Lab hook

**Lab 08, two-loop iteration sprint** ([labs/lab08.md](../labs/lab08.md)). Starting from your lab 07 findings list, you write kill criteria, run two short iteration loops on your prototype, and keep an iteration log. The second of the course's three playtest reports comes out of this lab.

## Sources

- Birdwell, K. (1999, December 10). "The Cabal: Valve's Design Process for Creating Half-Life." Game Developer. Source for the November 1997 schedule, the late-September 1997 judgment that the game was not fun, the decision to start over, and the prototype level that became the new base. https://www.gamedeveloper.com/design/the-cabal-valve-s-design-process-for-creating-i-half-life-i-
- Wikipedia, "Angry Birds (video game)" (accessed September 2026). Rovio had developed 51 games for other publishers before Angry Birds; iOS release December 11, 2009 (soft launch in Finland December 1). The article cites GameSpot and PC World for the game count. https://en.wikipedia.org/wiki/Angry_Birds_(video_game)
- Wikipedia, "Supercell (video game company)" (accessed September 2026). Founded 2010; the company celebrates cancelled games; games table lists seven globally released titles (Hay Day, Clash of Clans, Boom Beach, Clash Royale, Brawl Stars, Squad Busters, mo.co; Squad Busters marked as shutting down in 2026) and at least 13 discontinued titles, including Gunshine.net, Spooky Pop, Smash Land, Rush Wars, Clash Quest, Clash Mini and Everdale. https://en.wikipedia.org/wiki/Supercell_(video_game_company)
- Wikipedia, "Titan (cancelled video game)" (accessed September 2026). Development from 2007, team over 140 by 2013, reboot May 2013, public cancellation September 23, 2014, about 40 retained with roughly six weeks for a new concept, Overwatch released May 24, 2016, Morhaime's comment on scope. https://en.wikipedia.org/wiki/Titan_(cancelled_video_game)
- Zimmerman, E. (2003). "Play as Research: The Iterative Design Process." In B. Laurel (Ed.), *Design Research: Methods and Perspectives*. MIT Press.
- Fullerton, T. (2018). *Game Design Workshop* (4th ed.). CRC Press. Chapter 1.
- Medlock, M. et al. (2002). "Using the RITE method to improve products." Usability Professionals Association (see week 7 Sources).
- The hit rates, schedules and trade-action criteria are illustrative values for this lecture, not measured industry figures.

## Interactive spec: examples/w08-iteration-clock.html

**The one insight.** Every loop has the same odds, but shorter loops give you more of them before the deadline. The single-loop view looks identical at every loop length; the calendar view shows the chance of success climbing as loops get shorter.

**Layout.** Two linked views, side by side on desktop (≥ 900px), stacked on mobile. Controls above.

**Left view, "One loop".** A horizontal timeline 0 to T days. Draw the loops as consecutive blocks of width `c` (show at most 60 blocks; beyond that, draw them as thin ticks). Each block carries the same label on hover or focus: "q = 10% chance of a keeper." A caption under the timeline reads "I loops fit in T days" with live numbers. A partial final loop (when T is not a multiple of c) is drawn hatched and labelled "no decision."

**Right view, "Chance of at least one keeper by day t".** Step chart. x = calendar day 0 to T. y = 0% to 100%. For the chosen c, `P(t) = 1 − (1 − q)^floor(t / c)`. Also draw faint reference curves for c = 1, 3, 7, 14 and 30 days with labels. A horizontal guide at 50% and 90%. A marker at day T with the final value.

**Readouts (aria-live).** Loops `I`, `P(at least one keeper)` to one decimal, expected days to first keeper `c/q` to one decimal, median loops `ceil(ln 0.5 / ln(1 − q))`, and "Longest whole-day loop for 90% in T days": the largest integer c with `floor(T/c) ≥ ceil(ln 0.1 / ln(1 − q))`, or "not reachable" if even c = 1 fails.

**Controls.**
- Slider "Loop length c (days)", 1 to 30, step 1, default 7.
- Slider "Hit rate q", 0.02 to 0.50, step 0.01, default 0.10.
- Slider "Schedule T (days)", 10 to 180, step 5, default 60.
- Button "Simulate 20 teams": using a seeded PRNG (mulberry32, seed 2026, reseeded on each press with seed + press count), each team draws a Bernoulli(q) per loop; plot each team's first-keeper day as a dot on the right chart's x-axis (dots at day T+ for teams that found nothing, in a separate "none" bin). Show "k of 20 teams found a keeper."
- Button "Mixed plan" that sets up section 4: first 30 days at c = 3, last 30 at c = 14; the right chart then shows the piecewise curve and the readout the combined probability.

**Formulas.** As above. Mixed plan: loops = `floor(30/3) + floor(30/14)` = 10 + 2 = 12, `P = 1 − (1 − q)^12`.

**Test values (must match).**
- T = 60, q = 0.10: c = 1 → I = 60, 99.8%, 10.0 days; c = 3 → 20, 87.8%, 30.0; c = 7 → 8, 57.0%, 70.0; c = 14 → 4, 34.4%, 140.0; c = 30 → 2, 19.0%, 300.0.
- T = 60: q = 0.05, c = 3 → 64.2%; q = 0.20, c = 7 → 83.2%; q = 0.20, c = 14 → 59.0%.
- Median loops for q = 0.10: 7.
- Longest whole-day loop for 90%, T = 60, q = 0.10: 2 days.
- Mixed plan, q = 0.10: 12 loops, 71.8%.
- T = 45, c = 5, q = 0.15: 9 loops, 76.8%, 33.3 days.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Sliders keyboard operable with visible labels and numeric readouts. The right chart has a "Show as table" fallback listing P at each loop boundary. Respect `prefers-reduced-motion` (simulation dots appear without animation) and `prefers-color-scheme`. No studio names or logos in the visual; the cross-game stories live in the lecture text.
