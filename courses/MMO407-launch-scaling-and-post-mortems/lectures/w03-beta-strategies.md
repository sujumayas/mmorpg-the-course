# MMO407 · Week 03 — Beta strategies

**Why this matters:** A beta that "went fine" is the most common last sentence before a bad launch. A beta has a fixed amount of play in it, and launch week has ten or a hundred times more, so the rare bugs, the load that only appears in crowds and the exploit that takes a week to find all arrive after the doors open. This week you learn to measure what a beta can and cannot tell you, and to design one that tests the risks you actually have.

**You will be able to:**
- Compute the chance that a beta sees a bug of a given rate, and the number of times that bug will fire in launch week.
- Apply the rule of three to a clean beta and state the largest bug rate it rules out.
- Design a beta program (phases, size, length, who is invited, what is capped) whose exposure matches a list of launch risks.
- Critique a beta plan by naming which risks it has zero exposure to: content paths, crowd sizes or elapsed time.

**Before class:** Read Hanley, J. A. & Lippman-Hand, A. (1983), "If nothing goes wrong, is everything all right?", *JAMA* 249(13), 1743-1745 (3 pages). Reread [MA102 week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) on the chance of at least one drop; this week uses the same rule with bugs in place of loot.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (`1 − (1 − p)^n`). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why a small sample misleads). [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (stress tests, EVE's mass tests and the WoW Classic stress tests). [MMO309 week 4, duplication exploits](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (why attackers search for failures that honest players hit by accident). [Week 2 of this course](w02-capacity-planning-and-login-queues.md) (session lengths, which a beta is the first chance to measure).

**Interactive:** [examples/w03-beta-exposure.html](../examples/w03-beta-exposure.html). Keep it open during section 2.

---

## 1. What a beta is for

A **beta** is a period before launch when real players, outside the studio, play a nearly finished game. Studios run betas for four different reasons, and each reason wants a different design.

| Job | What it measures | What it needs |
|---|---|---|
| Find bugs | defects that real play triggers and internal QA did not | many player-hours, across all content |
| Measure load | server behaviour when many players act at once | many players at the same time, in the same places |
| Tune the game | balance, pacing, session length, early retention | players who resemble the launch audience |
| Sell the game | pre-orders, wishlist adds, word of mouth | access as a reward, a polished first impression |

The last row pulls against the first three. A beta used as a pre-order bonus invites the most eager fans, who are not typical players. It also becomes a first impression, and a buggy first impression is bad marketing. Most beta plans fail because they try to do all four jobs with one population and one weekend.

Betas come in named phases. The names vary by studio, but the usual ladder is:

- **Technical alpha or closed alpha.** Hundreds to a few thousand invited players, under a non-disclosure agreement (NDA), testing whether the game runs at all.
- **Closed beta.** Thousands to tens of thousands, often by application or pre-order, with a character **wipe** at the end (all progress deleted before launch).
- **Stress test.** Short, scheduled sessions whose only goal is load. Players are often pushed into a few zones on purpose.
- **Open beta.** Anyone can join. By now it is mostly marketing and a final load check.
- **Head start or early access.** Paid, not wiped, and technically launch. Week 1 treated it as a way to spread arrivals. This week treats it as the last beta phase.

## 2. Worked example: the bug your beta could not see

### The hook

SimCity (2013) needed a server connection to play. Starting in August 2012, EA let players apply for closed beta tests, which ran in January and February 2013, and the stated purpose was to load-test the game servers. On launch in March, those servers were overloaded. Players had outages, disconnections and lost cities, and EA turned off features to keep the service up.

A beta built specifically to test load did not predict the load. That is not a story about carelessness. It is about arithmetic. A beta holds a fixed amount of play, and launch holds far more. This section puts numbers on the gap.

### The model

Treat a bug as something that fires at random while people play, at an average rate `r` firings per player-hour. Define **exposure** as total play:

```
E = players × hours each          (player-hours)
```

Over `E` player-hours, the bug is expected to fire `r × E` times, and the chance it fires at least once is

```
P(seen) = 1 − e^(−r × E)
```

This is MA102 week 3's `1 − (1 − p)^n` in the form it takes when `p` is tiny and `n` is huge. `(1 − p)^n` is very close to `e^(−pn)` then, and the second form is easier to work with.

Now run it backwards. Suppose the beta saw the bug **zero** times. What does that tell you about `r`? The **rule of three** answers. If an event did not happen in `n` trials, a 95% confidence interval for its rate runs from 0 to `3 / n`. It comes from solving `e^(−r × E) = 0.05`, which gives `r × E = −ln 0.05 ≈ 3.0`. So:

```
clean beta ⇒ r < 3 / E_beta        (95% confidence)
expected launch firings < 3 × E_launch / E_beta
```

The second line is the whole lesson. A clean beta does not show the bug is absent. It shows only that the bug's rate is below `3 / E_beta`, and launch week can still see up to three times the ratio of launch exposure to beta exposure.

### Numbers you can check

Take a closed beta of 5,000 testers who play 20 hours each, so `E_beta = 100,000` player-hours. Launch week brings 200,000 players who play 15 hours each, `E_launch = 3,000,000` player-hours, thirty times the beta. All invented teaching values, in a realistic ratio.

| Bug fires once per | `P(seen in beta)` | Expected firings in launch week |
|---|---|---|
| 10,000 player-hours | 99.995% | 300 |
| 50,000 player-hours | 86.5% | 60 |
| 200,000 player-hours | 39.3% | 15 |
| 1,000,000 player-hours | 9.5% | 3 |
| 5,000,000 player-hours | 2.0% | 0.6 |

Check the middle row by hand. `r × E_beta = 100,000 / 200,000 = 0.5`, and `1 − e^(−0.5) = 0.393`. In launch week, `3,000,000 / 200,000 = 15` firings. That bug has a 61% chance of never appearing in the beta, and then it appears fifteen times in the first week, in front of 200,000 players and on forums with screenshots.

And if the beta saw nothing at all? The rule of three gives `r < 3 / 100,000`, a rate below once per 33,333 player-hours. At launch exposure that allows up to `3 × 30 = 90` firings of a bug nobody has ever seen.

```python
import math

BETA = 5_000 * 20          # player-hours: 5,000 testers playing 20 hours each
LAUNCH = 200_000 * 15      # player-hours in launch week: 200,000 players, 15 hours each

print("bug fires once per   P(seen in beta)  expected at launch")
for every in [10_000, 50_000, 200_000, 1_000_000, 5_000_000]:
    rate = 1 / every                                 # firings per player-hour
    seen = 1 - math.exp(-rate * BETA)                # chance of at least one firing
    print(f"{every:>13,} h {seen:16.1%} {rate * LAUNCH:19,.1f}")

bound = 3 / BETA                                     # rule of three, 95% upper bound
print(f"clean beta: rate below 1 per {1 / bound:,.0f} h, "
      f"so launch week may still see up to {bound * LAUNCH:.0f}")
```

It prints:

```
bug fires once per   P(seen in beta)  expected at launch
       10,000 h           100.0%               300.0
       50,000 h            86.5%                60.0
      200,000 h            39.3%                15.0
    1,000,000 h             9.5%                 3.0
    5,000,000 h             2.0%                 0.6
clean beta: rate below 1 per 33,333 h, so launch week may still see up to 90
```

The first row prints 100.0% because 99.995% rounds up at one decimal place.

To find a bug of a given rate with 95% confidence, you need `E_beta ≥ 3 / r`. For the once-per-200,000-hours bug, that is 600,000 player-hours, six times this beta. That could be 30,000 testers for 20 hours, or 10,000 testers for 60 hours. Either one is a bigger beta than most studios plan.

### Move it yourself

Open the interactive. The left view shows `P(seen in beta)` against the bug's rate on a log axis, an S-shaped curve that falls from nearly 1 to nearly 0. The right view shows expected launch-week firings for the same rates, a straight line on log axes that sits thirty times higher than the beta's expected firings. A shaded band marks the rates a clean beta cannot rule out, everything left of `3 / E_beta`. Drag the beta size up from 5,000 to 30,000. The curve on the left slides, and the shaded band on the right shrinks, but it never disappears. Then set the launch audience to 2 million. The band's top edge climbs to 900 possible firings. However large you make the beta, launch is larger.

### Cross-game recognition

Every beta decision changes `E_beta`, or changes which part of the game the exposure lands on.

**World of Warcraft Classic (beta, May to July 2019).** The Classic beta ran from 15 May to 12 July 2019 with the level cap first at 30 and later raised to 40. The game launched with a cap of 60. For any code that runs only above level 40, such as high-level dungeons, raids and the items they drop, `E_beta` was zero. The rule of three then bounds nothing. A capped beta is a deliberate trade. It keeps endgame content fresh for launch, and in exchange the team gives up all evidence about that content's bugs.

**Guild Wars 2 (beta weekends, 2012).** ArenaNet ran small closed tests in 2011, invited press in February 2012, and in March and April opened beta weekends to anyone who had pre-purchased. That one decision multiplied `E_beta` by the number of pre-orders, and it turned the beta into a sales incentive at the same time. The first job and the last job in the section 1 table were served by one lever.

**Final Fantasy XIV (2010 and 2013).** The original release followed what Wikipedia describes as a bug-laden and shortened beta, and launched in September 2010 to near-universal negative reviews. For A Realm Reborn, producer Naoki Yoshida published a roadmap of four beta phases from February 2013, saying the team was adamant the game would not ship "until it is ready." In the model, the relaunch bought exposure in stages, each phase larger than the last, before committing to a date. Week 4 of this course studies the whole case.

**Outside games: drug trials.** The rule of three was popularised for exactly this problem in medicine. If a drug is tested on 1,500 people with no serious side effect, the rule says only that the rate is below 1 in 500. When the drug is prescribed to a million people, a side effect at 1 in 5,000 would appear about 200 times. That is why regulators keep watching drugs after approval. Hanley and Lippman-Hand's 1983 paper is titled with the question every beta lead should ask: if nothing goes wrong, is everything all right?

**Outside games: phased app releases.** Apple's App Store lets a developer release an update in phases over 7 days, to 1%, 2%, 5%, 10%, 20%, 50% and then 100% of users, and pause it if something goes wrong. Google Play offers staged rollouts that the developer can halt. Each step multiplies exposure by roughly two to five, and each step is a small beta for the next. The ladder exists because the developer accepts the section 2 arithmetic. Launch is where rare bugs are found, so launch should be allowed to find them in 1% of the audience first.

### Eyes-open design judgment

- **Size the beta from the rate you care about.** Pick the rarest bug class you must find before launch, say one firing per 100,000 player-hours for a crash, and plan `E_beta ≥ 3 / r = 300,000` player-hours. That number tells you the tester count and length. A beta sized by "what feels big" answers nothing.
- **Accept that some bugs will be found at launch.** No affordable beta reaches launch exposure. Plan the launch for the bugs that survive: kill switches (week 1), fast patch pipelines, and a telemetry alert on every crash signature from minute one.
- **Rare for honest players is not rare for attackers.** A dupe that fires once per million honest player-hours can be found in an afternoon by someone looking for it. MMO309 week 4 made this case. Exposure math protects you against accidents, not against a search. Budget for a security review separately.
- **Decide what the beta will not cover, and write it down.** A level cap, a closed region or a missing feature each leaves some code with zero exposure. That is fine if it is a decision. It is a launch-night surprise if it is not.

### Check this example

1. A beta has 8,000 testers playing 25 hours each. What is the chance it sees a crash that fires once per 400,000 player-hours?
2. The same beta sees no instance of a certain save-corruption bug. Launch week is 5 million player-hours. What is the most firings you should plan for?
3. How many player-hours of beta would you need for a 95% chance of seeing a bug that fires once per 1 million player-hours?

<details>
<summary>Answers</summary>

1. `E_beta = 200,000`. `r × E = 0.5`, so `1 − e^(−0.5) ≈ 39%`.
2. `r < 3 / 200,000`, so up to `3 × 5,000,000 / 200,000 = 75` firings.
3. `E ≥ 3 / r = 3,000,000` player-hours.

</details>

## 3. Exposure has a shape

Player-hours are the right unit for bugs that any player can trigger at any time. Many launch problems are not like that. Three kinds of exposure need their own measure, and a beta can be large in one and zero in the others.

### Exposure per content path

Divide the game into **content paths**: the tutorial, each zone band, dungeons, crafting, the auction house, PvP, the endgame raid. Each path gets its own exposure:

```
E_path = E_beta × share of beta play spent on that path
```

A 100,000 player-hour beta in which 2% of play reaches the level 50 to 60 zones has 2,000 player-hours there. The rule of three bounds that path's bug rate only to below 1 per 667 player-hours, a very weak statement. Beta players cluster in early content, because everyone starts at the beginning and betas are short. Paths near the end of the game are the least tested, and at launch they are reached last, often by the most devoted players who post first and loudest. Use per-path telemetry (DB201 week 10) to measure the shares, and if a late path is thin, run a targeted test with pre-levelled characters.

### Exposure per crowd size

Some problems appear only when many players are in the same place at the same time. Examples are a zone server that misses its tick above 1,500 players, a database lock that only contends at 200 transactions a second, the auction house on the first evening. For these, player-hours do not matter. What matters is the **peak concurrency** reached per zone or per service. A beta of 50,000 player-hours spread across a month may never put more than 400 players in one zone. That is zero exposure to a 1,500-player problem, however many hours it logged.

This is why stress tests exist as a separate phase. MMO302 week 11 described the WoW Classic stress tests of 2019, which used level caps to pile players into a few zones, and EVE Online's mass tests, which reward players for gathering in one system. Both are ways to buy crowd exposure, which a normal beta does not provide. SimCity's beta was run to test load, and launch still overloaded the servers. Read through this model, the likely gap was crowd exposure. Launch put far more players on the servers at once, for long sessions, than any beta weekend had.

### Exposure per elapsed time

The third kind needs calendar time. A weekly reset that runs for the first time on day 7, an economy that inflates over weeks, a guild bank that overflows after a month of deposits, an item timer that expires in 72 hours. A three-day beta weekend has zero exposure to anything on a longer clock, however many testers it has. For these, the measure is the longest continuous run of the live game, so plan at least one beta phase that runs for more than your longest reset cycle without a wipe.

A useful habit is a **risk-to-exposure table**, one row per launch risk, with the exposure type it needs and the beta phase that provides it:

| Risk | Exposure type | Needed | Beta phase that provides it |
|---|---|---|---|
| Client crash, any zone | player-hours | ≥ 3 / r | closed beta, 30,000 × 20 h |
| Endgame dungeon bugs | per-path hours | ≥ 3 / r on that path | pre-levelled characters, 2 weekends |
| Starting-zone tick overload | peak per-zone crowd | ≥ 1.2 × launch peak | stress test with level cap |
| Weekly reset bugs | continuous days | ≥ 8 days | open beta, no mid-phase wipe |

If a row has no phase, you have found a launch risk before your players do.

## 4. Who you invite, and what their data means

A beta's players are not a sample of your launch audience. They applied, or pre-ordered, or were invited because they are fans. That is **selection bias**, a sample chosen by a process that makes it differ from the population you care about. MA102 week 13 showed how a small sample misleads. A large biased sample misleads with more confidence.

What this does to beta data:

- **Retention and session length are too high.** Fans play longer and come back more. If you plan launch capacity from beta session lengths (week 2's `L`), you will be close for launch night, when fans dominate, and too high for week 3, when a broader audience arrives and leaves sooner. Ask which audience each number describes.
- **Difficulty feedback is skewed.** Experienced players find early content too easy and ask for harder content that a new player will bounce off. Weight feedback by player experience, or run a separate small test with genre newcomers.
- **Bug reports are skewed toward what testers care about.** Testers report what they notice. They rarely report the crash in a setting menu they never opened. Crash telemetry catches what reports miss, and it is not biased by what testers care about.

Two structural choices shape the data too.

- **Wipe or carry over.** A wipe lets testers explore, break and exploit without harming the launch economy, and it makes beta play less meaningful, so testers may play less. Carrying progress over makes testers play for real and imports every beta exploit's profits into the live economy. Most MMOs wipe betas and carry over only head-start progress, which is paid and closer to launch.
- **NDA or open talk.** An NDA keeps an unfinished game out of the press. Lifting it makes the beta marketing, for better or worse. FFXIV 1.0's short, buggy beta was a public first impression that its launch reviews then confirmed.

## 5. The last beta is the launch

Section 2's arithmetic says launch will find bugs the beta could not. Treat the first days of launch as the final beta phase, and give that phase the tools a beta has:

- **A staged start.** A paid head start (Guild Wars 2, FFXIV: A Realm Reborn, Lost Ark) runs a few days with a fraction of the audience. In exposure terms it is one rung on a ladder like Apple's phased release, and it should have the same rule: a pause condition written in advance.
- **Telemetry on everything.** Crash signatures, error codes per stage (week 1) and per-path play shares, visible to the war room from the first minute.
- **Fast fixes.** A patch pipeline that can ship a server-side fix in hours, and kill switches for any feature the fix cannot reach in time.

## In-class activity (25 minutes)

In groups of three. Your MMO launches in 12 weeks. Launch week is forecast at 150,000 players for 12 hours each. You have budget for a total of 400,000 beta player-hours, split across phases however you like, plus one stress test.

1. Compute the rarest bug rate your full budget rules out with 95% confidence, and the most firings of such a bug you should plan for in launch week.
2. The design lead wants a level cap of 35 (launch cap 50) to protect the endgame. Telemetry from an earlier test says 15% of launch-week play will happen above level 35. What is the per-path exposure above 35 with the cap? What does the rule of three say about bugs there?
3. The starting zone is forecast at 2,500 players at launch peak. Your beta's largest weekend put 700 in it. Design the stress test: how many players, where, for how long?
4. Build a risk-to-exposure table with at least four rows, and mark any row you cannot cover.

Expected output: `r < 3 / 400,000`, below 1 per 133,333 player-hours; launch week is 1.8 million player-hours, so plan for up to `3 × 1,800,000 / 400,000 = 13.5` firings. With the cap, exposure above level 35 is zero and the rule of three bounds nothing, so either lift the cap for one phase with pre-levelled characters or accept and document the risk. The stress test needs at least 2,500 in the starting zone, and a margin of 20% suggests 3,000, for long enough to see the tick behaviour settle (an hour is a common choice).

## Common misconceptions

- **"The beta saw no crashes, so we have none."** A clean beta bounds the rate below `3 / E_beta`. At launch exposure that bound can still mean dozens of crashes.
- **"A bigger beta tests load."** Load problems need players in the same place at the same time. Player-hours spread over weeks do not test crowd size.
- **"Beta retention predicts launch retention."** Beta players are a self-selected group of fans. Their numbers run high.
- **"If a bug is rare for players, it is rare for attackers."** A rate per player-hour describes accidents. An attacker searches, and finds a rare failure far faster than honest play does.

## Check yourself

1. A beta runs 12,000 testers for 15 hours. A bug fires once per 90,000 player-hours. What is the chance the beta sees it, and how many times will it fire in a launch week of 2.4 million player-hours?
2. After a clean beta of 250,000 player-hours, a producer says the bug rate is "at most 1 in 250,000". What is wrong, and what is the right statement?
3. Your beta was 300,000 player-hours, and 4% of it was spent in the crafting system. How strong a statement can you make about crafting bugs if none were seen?
4. Give one launch risk that needs crowd exposure and one that needs elapsed time, and name the beta phase you would use for each.
5. A studio wants its beta to double as a pre-order bonus. Name one benefit and one cost of this choice, in terms of this lecture.

<details>
<summary>Answers</summary>

1. `E = 180,000`, `r × E = 2`, `P = 1 − e^(−2) ≈ 86.5%`. At launch it fires about `2,400,000 / 90,000 ≈ 26.7` times.
2. Zero firings in 250,000 hours does not bound the rate at 1 in 250,000. With 95% confidence it is below `3 / 250,000`, about 1 in 83,333, which is three times higher.
3. Crafting exposure is `0.04 × 300,000 = 12,000` player-hours, so the rate is below 1 per 4,000 player-hours, a weak statement.
4. Crowd: a zone server's tick time with 2,000 players in the starting zone, tested in a stress test with a level cap. Elapsed time: the first weekly reset, tested in a beta phase that runs at least 8 days without a wipe.
5. Benefit: exposure rises with every pre-order (Guild Wars 2 in 2012). Cost: the testers are the keenest fans, so retention, session length and difficulty feedback are biased, and a rough beta becomes a public first impression.

</details>

## Lab / assignment hook

[Lab 03, beta exposure planner](../labs/lab03.md). You build a small library that computes detection chances, rule-of-three bounds, per-path exposure and a phased rollout ladder, check it against this lecture's tables, and use it to design a beta program for a given launch forecast and risk list. The risk-to-exposure table you produce becomes a section of your final launch plan.

## Sources

- Wikipedia, "SimCity (2013 video game)" (read September 2026). Closed beta sign-ups from August 2012, betas in January and February 2013 for load testing of the game servers; launch outages, disconnections and lost saves; features disabled by server patch.
- Warcraft Wiki, "World of Warcraft: Classic" (read September 2026). Beta from 15 May 2019 to 12 July 2019 with the level cap at 30, later raised to 40; launch level cap 60.
- Wikipedia, "Guild Wars 2" (read September 2026). Small closed alpha and beta tests in 2011; press beta in February 2012; beta tests opened to anyone who pre-purchased in March and April 2012; head start from 25 August, launch 28 August 2012.
- Wikipedia, "Final Fantasy XIV" (read September 2026). The 2010 release after a bug-laden, abbreviated beta, with near-universal negative reception; Yoshida's roadmap of four beta phases from mid-February 2013 and his statement that the team would not release the game until it was ready; early access from 24 August 2013.
- Wikipedia, "Rule of three (statistics)" (read September 2026). The 95% interval `[0, 3/n]` after zero events in `n` trials; derivation from `(1 − p)^n = 0.05`; the example of 1,500 subjects bounding the rate below 1 in 500.
- Hanley, J. A. & Lippman-Hand, A. (1983). "If nothing goes wrong, is everything all right? Interpreting zero numerators." *JAMA*, 249(13), 1743-1745. doi:10.1001/jama.1983.03330370053031
- Apple Developer, "Release a version update in phases" (App Store Connect Help, read September 2026). Seven-day phased release at 1%, 2%, 5%, 10%, 20%, 50% and 100%; pauses up to 30 days in total.
- Google, "Release app updates with staged rollouts" (Play Console Help, read September 2026). Rollout to a chosen percentage of users, which can be increased or halted.
- MMO302 week 11 (this program) for the WoW Classic stress tests and EVE Online mass tests, with its sources.
- Beta sizes, launch exposures, bug rates, path shares and the risk table are invented teaching values.

## Interactive spec: examples/w03-beta-exposure.html

**The one insight:** a clean beta only proves the bug rate is below `3 / E_beta`, and launch multiplies whatever rate slipped through by `E_launch`. However large the beta, a band of bugs remains that the beta almost never sees and launch week sees many times.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the beta": x axis is the bug rate as "fires once per N player-hours", log scale from 10³ to 10⁸. y axis is `P(seen in beta) = 1 − exp(−E_beta / N)` from 0 to 1, drawn in `--steel`. A vertical dashed line at `N = E_beta / 3` labelled "rule of three". Rates to the right of it (rarer bugs) are shaded as "a clean beta cannot rule these out".
- View B, "launch week": same x axis. y axis is expected launch firings `E_launch / N` on a log scale from 0.1 to 10⁴, in `--blood`. The same shaded band as View A. A horizontal marker at "1 firing". The top of the shaded band is labelled with `3 × E_launch / E_beta` ("up to K firings of a bug nobody saw").
- A draggable "bug" marker shared by both views (default at N = 200,000). Its readout shows `P(seen in beta)` and expected launch firings.
- Below the views, a "path" strip: bars for up to five content paths with share sliders; each bar shows that path's exposure `share × E_beta` and its rule-of-three bound in "once per N hours". Setting a share to 0 shows "no evidence".

**Controls:**

- Beta testers, 100 to 200,000, log slider (default 5,000); hours each, 1 to 100 (default 20).
- Launch players, 1,000 to 5,000,000, log slider (default 200,000); hours each in launch week, 1 to 40 (default 15).
- Bug marker position (drag, or a slider for keyboard users).
- Path shares (default five paths: tutorial 30%, zones 1-20 35%, zones 21-40 25%, zones 41-50 8%, endgame 2%), normalised to 100%.
- Toggle "phased launch": shows the launch ladder 1%, 2%, 5%, 10%, 20%, 50%, 100% of launch players by day, with the chance that the bug at the marker is seen by the end of each day.

**Readout (always visible, `aria-live="polite"`):** `E_beta`, `E_launch`, ratio, rule-of-three bound "once per N hours", `3 × E_launch / E_beta`, and for the bug marker the two values above.

**Formulas:**

```
E_beta = testers × hours;  E_launch = players × hours
P(seen in beta) = 1 − exp(−E_beta / N)
expected launch firings = E_launch / N
rule-of-three bound: N* = E_beta / 3;  max launch firings for a clean beta = 3 × E_launch / E_beta
path exposure = share × E_beta;  path bound N = share × E_beta / 3
phased ladder, day d with fraction f_d: cumulative exposure = E_launch / 7 × Σ_{i≤d} f_i
  (launch-week hours spread evenly over 7 days, each day's players = f_d × players)
  P(seen by day d) = 1 − exp(−cumulative exposure / N)
```

**Test values (must match):**

- Defaults: `E_beta = 100,000`, `E_launch = 3,000,000`, ratio 30; bound once per 33,333 h; up to 90 firings.
- Marker at N = 200,000: `P(seen) = 39.3%`, launch firings 15.0.
- Marker at N = 50,000: 86.5%, 60.0. N = 1,000,000: 9.5%, 3.0.
- Testers 30,000, hours 20: bound once per 200,000 h; up to 15 firings.
- Endgame path at 2% of the default beta: exposure 2,000 h, bound once per 667 h.
- Phased launch, marker N = 200,000: day 1 cumulative exposure `3,000,000 / 7 × 0.01 = 4,286`, `P = 2.1%`; day 7 cumulative `3,000,000 / 7 × 1.88 = 805,714`, `P = 98.2%`.

**First screen:** defaults with the marker at N = 200,000. Caption: "This bug has a 61% chance of never showing up in your beta. It will fire 15 times in launch week. Drag the beta size."

**Accessibility:** all controls keyboard operable with visible focus; the marker moves with arrow keys (one tenth of a decade per press); readout in `aria-live="polite"`; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
