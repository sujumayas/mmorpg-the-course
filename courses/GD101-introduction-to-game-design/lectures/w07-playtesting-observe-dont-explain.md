# GD101 · Week 07 — Playtesting method: observe, don't explain

**Why this matters:** You cannot see your own game. You know every rule, so you never trip over the ones that are badly written. A playtest is the only cheap way to borrow a fresh pair of eyes, and the moment you explain something to the tester you spend those eyes and get nothing back.

**You will be able to:**
- Compute the chance that a playtest with n testers shows a problem that affects a fraction p of players, and the number of testers needed to reach a target chance.
- Explain, with numbers, why coaching a tester removes problems from your report without removing them from your game.
- Run a 30-minute playtest session from a written script, using neutral prompts and a separate observation log.
- Turn raw observation notes into a findings list ranked by frequency and severity.

**Before class:** Fullerton, *Game Design Workshop* (4th ed.), the chapter on playtesting (read it in full; it is the practical companion to this lecture). Jakob Nielsen, "Why You Only Need to Test with 5 Users" (Nielsen Norman Group, 2000), a short web article. Ken Birdwell, "The Cabal: Valve's Design Process for Creating Half-Life" (Game Developer, 1999), the section on playtesting.

**Prerequisites from earlier courses:** GD101 week 6, paper prototyping, which gives you the prototype you test this week (see the [GD101 syllabus](../syllabus.md)). Exponents and logarithms from [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [MA101 week 5](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md). No probability course is assumed; the one rule you need is taught here.

**Interactive:** `examples/w07-discovery-curve.html` (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a playtest is for

A **playtest** is a session where someone who did not design your game plays it while you watch, so you can learn what they actually experience. That is the whole definition, and each part of it matters.

- *Someone who did not design it.* Your own play is useful for checking that the rules work at all, but you cannot be surprised by your own game. You already know that the blue cards are the defensive ones and that you are meant to save gold for round three.
- *Plays it.* A playtest is not a pitch meeting and not a focus group. You are not asking whether they like the idea. You are watching what happens when the rules meet a real person.
- *While you watch.* Most of the value comes from what you see: the pause before a move, the card turned over twice, the rule the tester invents because the real one was unclear.
- *What they actually experience.* Not what you intended. Week 4 gave you the MDA framework (mechanics, dynamics, aesthetics). You write mechanics. Players experience aesthetics. The playtest is where you find out whether your mechanics produce the dynamics you hoped for.

Playtesting is different from **quality assurance (QA) testing**, which hunts for bugs against a specification: does the card do what the rules say it does? A playtest asks a harder question. Given the rules as written, what does a person do, and is that the experience you wanted?

### The one rule of this week

When a tester is confused, you will want to help. You will want to say "oh, you can also trade with the bank" or "the arrow means clockwise." Do not.

Every explanation you give fixes the problem for this tester, in this room, today. It does nothing for the thousands of players who will open the box or download the build when you are not there. Worse, it erases the evidence. If you explain the trade rule to every tester, your notes will say "nobody had trouble with trading," and you will ship the confusing rule.

Valve's team on the original Half-Life worked under this rule. According to Ken Birdwell's 1999 account of their process, designers watching a playtest had to sit quietly taking notes and were not allowed to give hints. He describes how humbling it was to watch testers miss things the team considered obvious. Section 2 turns that rule into numbers.

## 2. Worked example: how many testers does it take to see a problem?

### The hook

Valve ran more than 200 playtest sessions on Half-Life (1998), and Birdwell reports that a single two-hour session typically produced about 100 action items. That sounds like a lot of testing. It also raises two questions any small team has to answer. If one session finds so much, why run 200? And if you only have five friends willing to play your paper prototype, what will those five sessions miss?

### The model

Suppose some problem in your game affects a fraction `p` of players. "Affects" means a player who sits down with the game hits the problem in a way you can observe: they misread a rule, they get stuck, they skip a mechanic you meant to be central. Assume each tester hits it independently of the others.

The chance that one tester does **not** hit it is `1 − p`. The chance that none of `n` testers hit it is `(1 − p)^n`, because independent chances multiply. The chance that **at least one** tester shows you the problem is everything else:

```
P(seen) = 1 − (1 − p)^n
```

- `p` is the problem's frequency: the share of all players who would hit it.
- `n` is the number of independent testers.
- `P(seen)` is the chance your playtest shows the problem at least once.

This "1 minus the chance of never" move is called the **complement rule**. MA102 covers it in depth in its [week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), where the same formula answers "what is my chance of at least one rare drop in n kills?" You only need the one line above for this course.

### Numbers you can check

Here is the formula for four problem frequencies. Each cell is `1 − (1 − p)^n` as a percentage.

| Testers `n` | Common (p = 0.50) | Typical (p = 0.31) | Uncommon (p = 0.10) | Rare (p = 0.05) |
|---|---|---|---|---|
| 1 | 50.0% | 31.0% | 10.0% | 5.0% |
| 2 | 75.0% | 52.4% | 19.0% | 9.8% |
| 3 | 87.5% | 67.1% | 27.1% | 14.3% |
| 5 | 96.9% | 84.4% | 41.0% | 22.6% |
| 10 | 99.9% | 97.6% | 65.1% | 40.1% |
| 15 | 100.0% | 99.6% | 79.4% | 53.7% |

Check one by hand. For p = 0.10 and n = 5, `0.9^5 = 0.59049`, and `1 − 0.59049 = 0.40951`, or 41.0%.

Read the table in two directions. Down a column, each extra tester adds less than the one before, because each new tester mostly re-finds what earlier testers already showed you. Across a row, rare problems hide from small tests. Five testers will almost certainly show you a rule that confuses half of all players. Five testers will miss a problem that hits one player in twenty more than three times out of four.

You can also run the formula backwards. How many testers do you need for a 90% chance of seeing a problem with frequency p? Solve `1 − (1 − p)^n ≥ 0.9` for n. Taking logarithms (MA101 week 5):

```
n ≥ ln(1 − 0.9) / ln(1 − p)
```

| Problem frequency p | Testers for 90% chance | Testers for 95% chance |
|---|---|---|
| 0.31 | 7 (6.21 rounded up) | 9 (8.07) |
| 0.10 | 22 (21.85) | 29 (28.43) |
| 0.05 | 45 (44.89) | 59 (58.40) |

This is why Valve ran hundreds of sessions. A studio that wants to catch the one-in-twenty problems needs dozens of fresh testers per build.

### What explaining does to the numbers

Now apply the formula to a whole prototype. Here is a fictional paper card game about running a trading post, after its first internal play. Your team suspects eight problems. You don't know their frequencies in advance; for this example, suppose they are:

| # | Problem | Kind | p |
|---|---|---|---|
| 1 | Rolls the wrong die for travel | Onboarding | 0.50 |
| 2 | Doesn't notice the market deck refills | Onboarding | 0.40 |
| 3 | Forgets to pay upkeep at end of round | Rules memory | 0.31 |
| 4 | Thinks healing is capped at 3 | Onboarding | 0.25 |
| 5 | Never uses the trade action | Strategy | 0.20 |
| 6 | Ends turns with unspent gold | Strategy | 0.15 |
| 7 | Both players turtle and the game stalls | Dynamics | 0.10 |
| 8 | Game soft-locks when the market deck is empty | Rules hole | 0.05 |

Problems 1, 2 and 4 are **onboarding** problems: they come from learning the game for the first time. They are exactly the problems you are tempted to fix by talking.

Because the expected number of problems seen is just the sum of each problem's `P(seen)`, you can add the column. Run the test two ways.

| Testers `n` | Expected problems seen, silent facilitator | Expected problems seen, facilitator explains 1, 2 and 4 up front |
|---|---|---|
| 1 | 1.96 | 0.81 |
| 3 | 4.20 | 1.96 |
| 5 | 5.36 | 2.71 |
| 10 | 6.66 | 3.72 |
| 15 | 7.19 | 4.20 |

Explaining the three onboarding rules sets their `p` to zero *in the test room*. It does not change their `p` for players at home. With a silent facilitator, five testers show you problem 1 with 96.9% probability, problem 2 with 92.2% and problem 4 with 76.3%. With a helpful facilitator, the chance of seeing any of them is 0%, and no number of extra testers changes that. You could run fifteen coached sessions and report fewer findings than five silent ones.

This is the week's core idea in one sentence. **An explanation hides a problem from your data; it never removes it from your game.**

### The visual

Open `examples/w07-discovery-curve.html`. The left chart plots `P(seen)` against the number of testers for each of the eight problems, one curve each. The right chart shows two bars per problem: "in your report" and "at launch." Drag the tester slider and watch the common problems saturate by five testers while the rare ones crawl. Then tick "Explain the onboarding rules." The three onboarding curves on the left drop flat to zero. On the right, their "at launch" bars do not move at all. The report looks cleaner. The game got no better.

### Cross-game recognition

The same formula appears wherever people test designs with humans.

**Web and software usability.** Jakob Nielsen and Tom Landauer published this model in 1993, written as `problems found = N × (1 − (1 − L)^n)`, where N is the total number of problems and L is the share found by a single user. Averaged over many projects they studied, L was about 31%, so one user shows you about a third of the problems and five users about 85%. That 85% is our p = 0.31 column at n = 5. Nielsen's 2000 article then argues that a team with a budget for 15 users should run three rounds of five, fixing problems between rounds, rather than one round of 15. The table shows why: users 6 to 15 mostly re-find what users 1 to 5 found. Note what the 85% figure is: an average over problem frequencies from real web projects. It does not promise that five testers find 85% of the problems in *your* game, and it says nothing about rare problems.

**Valve, Half-Life (1997 to 1998).** Valve paired silent observation with **instrumentation**, meaning the game logged data automatically. Birdwell describes recording player position, health, weapons, elapsed time, and events such as saving, dying, taking damage and solving puzzles, then graphing it to find areas that were boring, too easy or too hard. Logging raises the effective `n`: every session contributes data about every room, even the ones where the observer was busy writing about something else.

**Microsoft Games User Research, the RITE method (2002).** Michael Medlock and colleagues at Microsoft described the Rapid Iterative Testing and Evaluation (RITE) method, where the team changes the build as soon as a problem is clearly identified, sometimes after a single participant. In our model, that means a problem with a high `p` is fixed after tester one or two, and the remaining testers spend their time hitting problems further down the list. It is Nielsen's "three rounds of five" pushed to its limit, and it needs the decision-makers in the room so fixes can happen same-day.

Three contexts, one line of algebra. When someone tells you how many testers are enough, your first move should be to ask "enough to see a problem of what frequency?"

### Eyes-open design judgment

The model is simple on purpose, and you should know where it breaks.

- **It assumes testers are independent and representative.** Five friends from your game design class are not five independent draws from your future players. They share vocabulary, genre habits and your house rules. A problem that hits 30% of the public may hit 0% of your classmates. Recruit outside your circle as early as you can.
- **It counts seeing, not understanding.** A tester who hits a problem gives you one observation. Whether you recognize it as a problem depends on your notes and your attention. Two observers, or a video recording, raise the real `P(seen)` closer to the formula.
- **It treats problems as fixed.** Real problems hide behind each other. If half your testers never get past round two because of problem 1, they never reach the round-four stall in problem 7. Fixing the common problems early and retesting, as Nielsen and RITE recommend, exposes the problems underneath. Week 8 builds on this.
- **Small tests are for finding, not measuring.** Five testers can tell you that a problem *exists*. They cannot tell you whether it affects 30% or 60% of players. If you need a rate, you need a bigger sample and the tools from MA102 [week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md). In a GD101 report, write "3 of 5 testers" and never "60% of players."
- **Silence is a rule for the test, not for the whole session.** After the test, you can and should ask questions (section 3). The rule is about the order: watch first, talk later.

## 3. Running a session: a protocol

Good playtests look boring from the outside. The facilitator reads a script, sits slightly behind the tester, writes a lot and says very little. Here is the protocol this course uses. The lab asks you to follow it exactly once before you adapt it.

### Before the session

1. **Write one to three test goals.** A goal is a question the session can answer. "Is the game fun?" is not a goal. "Do players use the trade action by round three without being told?" is. Goals decide where you look.
2. **Prepare the prototype so it teaches itself.** Put the rules on a sheet the tester can read. If the game can't be played from the sheet, that is your first finding, and it is a good one.
3. **Write the intro script.** Read it word for word to every tester so each one starts from the same place. A standard script says who you are, that you are testing the game and not the player, that nothing they do is wrong, that you will not answer rules questions during play, and that you would like them to think aloud.
4. **Get consent.** Tell the tester what you will record (notes, photos of the table, audio) and that they can stop at any time. For any recording, get their clear agreement.

### During the session

**Think-aloud** means the tester says what they are thinking as they play: "I'm going to buy this because... wait, can I afford it?" It is the cheapest window into their head. People forget to do it, so you may prompt. Use only neutral prompts:

- "What are you thinking right now?"
- "What are you looking for?"
- "What do you expect will happen?"

Do not use leading prompts: "Did you see the trade button?", "Isn't that card strong?" A **leading prompt** is any question that tells the tester what to notice or what to feel. It works exactly like an explanation: it sets `p` to zero for whatever it points at.

When a tester asks you a rules question, reply with a neutral deflection: "What do you think the rules say?" or "What would you do if I weren't here?" Then write down the question. A question from the tester is a finding.

### The one exception: the rescue

Sometimes a tester is stuck so badly that the session will produce nothing else. Set a threshold in advance, for example "stuck for three minutes with no progress." When you cross it, you may give the smallest hint that unblocks them. Then write **ASSIST** in the log with the time and exactly what you said. In your findings, an assisted problem counts as observed, with the highest severity, because at home nobody will rescue them.

### After the session

Once play ends, you can finally talk. Ask open questions, from general to specific:

1. "Tell me about that game in your own words."
2. "What was the most interesting moment? The most frustrating?"
3. "Was there anything you wanted to do but couldn't?"
4. Then, and only then, questions about your test goals: "How did you decide when to trade?"

Treat what testers *say* after the session as weaker evidence than what they *did* during it. People are poor at explaining their own choices, and they tend to be polite to the person who made the game. When the debrief and the log disagree, trust the log.

## 4. Recording what you see: observation versus interpretation

Your notes are the data. Most beginner playtest notes fail in the same way: they record conclusions instead of events.

| Weak note (interpretation) | Strong note (observation) |
|---|---|
| "Confused by trading." | "12:40. Picks up trade card, reads it, puts it back. Says 'I don't get what this is for.' Never plays a trade." |
| "Liked combat." | "14:05. Leans forward, rolls both dice before being told. Says 'come on, come on.'" |
| "Economy is broken." | "Round 4: tester has 11 gold, nothing to buy. Passes three turns in a row." |

An **observation** is something a camera could have recorded: an action, a quote, a time. An **interpretation** is your explanation for it. You need both, but keep them in separate columns. Two reasons. First, interpretations are often wrong, and you want to be able to reread the evidence later with fresh eyes. Second, when you pool notes across five testers, observations can be counted and interpretations cannot.

Use a three-column log: **time**, **what happened** (observation, with direct quotes in quotation marks), and **why I think it happened** (interpretation, optional). Lab 07 gives you a printable template.

## 5. From notes to findings

After the sessions, turn the logs into a findings list. A **finding** is one problem or one surprising success, stated as an observation, with the evidence behind it.

1. **Cluster.** Put every observation on a sticky note or a row in a sheet. Group notes that describe the same underlying issue.
2. **Count.** For each cluster, count how many testers showed it. Write "4 of 5." Do not convert to percentages. As section 2 showed, a count from five testers tells you the problem exists and is probably not rare, and not much more.
3. **Rate severity.** Use a simple scale.
   - **3, blocker:** the tester could not continue without an ASSIST, or the game broke.
   - **2, major:** the tester continued but played a different game than you designed (never traded, misread scoring).
   - **1, minor:** friction that cost time but did not change play.
4. **Rank.** Sort by severity first, then by count. A severity-3 finding seen once beats a severity-1 finding seen five times. The rare blocker is exactly the kind of problem that section 2 showed small tests usually miss, so when you do see it, take it seriously.
5. **Separate the problem from the fix.** Write "4 of 5 testers never used trade" as the finding. Write "maybe add a trade reminder to the round summary" as a separate, optional suggestion. Keeping them apart stops the team from arguing about the fix before agreeing on the problem.

This findings list is the core of the playtest report you will write three times this semester.

## In-class activity (25 minutes)

Work in groups of three with a paper prototype from week 6 (yours or one the instructor provides). Roles rotate each round: **designer** (facilitator), **tester**, **observer**.

1. (3 min) The designer writes two test goals and reads the standard intro script from section 3 aloud.
2. (8 min) The tester plays from the rules sheet only. The designer may use only neutral prompts and deflections. The observer keeps a three-column log and also tallies every time the designer breaks the rule (explains, leads, or answers a rules question).
3. (4 min) Short debrief with the four open questions.
4. Rotate roles and repeat once if time allows.

**Expected output:** one observation log per round, with at least eight timed observations, and the observer's tally of rule breaks. Most groups record three to six rule breaks in their first round. Before you leave, write down one problem that a rule break hid, using the section 2 language: which problem had its `p` set to zero in your room?

## Common misconceptions

- **"Five testers find 85% of the problems."** That average comes from web usability studies where the typical problem affected about 31% of users. For a problem affecting 5% of players, five testers have only a 22.6% chance of showing it. Always ask "85% of problems of what frequency?"
- **"If nobody in the test had trouble, there is no problem."** Only if you stayed silent and your testers are like your players. If you explained the rule, or tested only with people who already know the genre, the evidence is missing, not negative.
- **"Asking testers what they thought is the main output."** What they did is the main output. The debrief adds context, but when it contradicts the log, trust the log.
- **"More testers in one round is always better."** Past a handful of testers, the extra sessions mostly re-find the same common problems. Spending the same testers across several rounds, with fixes in between, usually finds more.

## Check yourself

1. A problem affects 20% of players. What is the chance that four silent testers show it at least once? What if the facilitator explains the relevant rule to two of the four before they start?
2. Your team can afford 12 tester sessions. Designer A wants one round of 12. Designer B wants three rounds of 4 with fixes in between. For a problem with p = 0.40 that you will fix as soon as you see it, what is the chance it survives into round 2 under Designer B's plan? What does Designer B's plan gain from the remaining eight sessions?
3. How many silent testers do you need for at least an 80% chance of seeing a problem that affects 15% of players?
4. A classmate's notes read "Tester found the map confusing." Rewrite it as an observation, invent plausible details, and say what extra information the rewrite gives the team.

<details>
<summary>Answers</summary>

1. Silent: `1 − 0.8^4 = 1 − 0.4096 = 0.5904`, about 59%. With two testers coached, only two can show it: `1 − 0.8^2 = 0.36`, or 36%. The explanation cost you almost two fifths of your chance, and the problem is exactly as common at launch.
2. The problem survives round 1 only if none of the first four testers hit it: `0.6^4 = 0.1296`, about 13%. So 87% of the time it is fixed before round 2, and the remaining eight sessions are spent on a build without it, where they can hit problems that it used to hide or crowd out. With one round of 12, the problem is seen almost surely (`1 − 0.6^12 ≈ 99.8%`) but most sessions keep re-finding it.
3. `n ≥ ln(0.2) / ln(0.85) = −1.609 / −0.1625 = 9.90`, so 10 testers. Check: `1 − 0.85^10 = 1 − 0.197 = 0.803`.
4. Example: "03:15. Turns the map sideways twice. Asks 'which way is north?' Moves the caravan west when the quest card says east." The rewrite shows *what* was confusing (orientation, not route length or icons), when it happened, and that it changed play. The team can now count it across testers and target a fix.

</details>

## Lab hook

**Lab 07, silent playtest and observation log** ([labs/lab07.md](../labs/lab07.md)). You run three silent playtests of your week 6 prototype with the section 3 protocol, keep three-column logs, and build a ranked findings list. It is the first of the course's three playtest reports. Week 8 uses your findings list as the input to an iteration loop.

## Sources

- Birdwell, K. (1999, December 10). "The Cabal: Valve's Design Process for Creating Half-Life." Game Developer (formerly Gamasutra). Source for silent observers who could not give hints, more than 200 playtest sessions, about 100 action items per two-hour session, and the logged data (position, health, weapons, time, key events). Describes Half-Life (1998) development. https://www.gamedeveloper.com/design/the-cabal-valve-s-design-process-for-creating-i-half-life-i-
- Nielsen, J. (2000, March 18). "Why You Only Need to Test with 5 Users." Nielsen Norman Group. Source for the formula, the average L of 31%, the 85% at five users, and the three-rounds-of-five recommendation. https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- Nielsen, J. & Landauer, T. K. (1993). "A mathematical model of the finding of usability problems." *Proceedings of ACM INTERCHI '93*, pp. 206-213. Original model.
- Medlock, M., Wixon, D., Terrano, M., Romero, R. & Fulton, B. (2002). "Using the RITE method to improve products: a definition and a case study." Usability Professionals Association annual conference. Summary via Wikipedia, "RITE Method" (accessed September 2026). https://en.wikipedia.org/wiki/RITE_Method
- Fullerton, T. (2018). *Game Design Workshop* (4th ed.). CRC Press. Playtesting chapter.
- The trading-post prototype and its problem frequencies are fictional, built for this lecture.

## Interactive spec: examples/w07-discovery-curve.html

**The one insight.** Explaining a rule to testers makes a problem disappear from the test report while leaving it exactly as common at launch. Secondary: common problems saturate after a handful of testers, rare ones need many.

**Layout.** Two linked views side by side on desktop (≥ 900px), stacked on mobile. Controls above both.

**Left view, "Chance your test shows each problem".** Line chart. x = number of testers n, integers 1 to 30. y = `P(seen)` from 0% to 100%. One line per problem (8 lines), coloured by kind (Onboarding, Rules memory, Strategy, Dynamics, Rules hole), labelled at the right end with the problem number. A vertical marker at the current slider value n. When "Explain onboarding rules" is on, the three onboarding lines are drawn at 0% (solid) with their silent curves shown as faint dashed ghosts.

**Right view, "In your report vs at launch".** Horizontal paired bar chart, one row per problem (8 rows, labels "1. Wrong travel die", etc.). Bar A, "In your report": `P(seen)` at the current n, respecting the explain toggle. Bar B, "At launch": the problem's p (share of real players who hit it), which never changes with the toggle or n. Show exact percentages at the end of each bar.

**Readouts (below charts, aria-live).** "Expected problems seen: X.XX of 8" (sum of Bar A values, two decimals). "Onboarding problems seen: X.XX of 3." "Testers needed for 90% on the rarest problem you can still see: N."

**Controls.**
- Slider "Testers (n)", 1 to 30, default 5.
- Checkbox "Explain the onboarding rules before play" (default off). When on, p used in Bar A and the left chart is 0 for problems 1, 2 and 4.
- Slider "Frequency of the selected problem" 0.01 to 0.90, step 0.01, applies to the problem selected by clicking a row or line (keyboard: problem select dropdown as an accessible alternative). A "Reset frequencies" button.
- Preset button "Nielsen average (all p = 0.31)": sets every p to 0.31 and n to 5 so the readout shows 8 × 0.844 = 6.75 expected problems (84.4% each).

**Formulas.**
- `P(seen) = 1 − (1 − p_eff)^n`, `p_eff = 0` for onboarding problems when explain is on, else `p`.
- Expected problems seen = Σ `P(seen)` over the 8 problems.
- Testers for 90%: `ceil( ln(0.1) / ln(1 − p) )` for the smallest non-zero `p_eff`.

**Default data.** p = [0.50, 0.40, 0.31, 0.25, 0.20, 0.15, 0.10, 0.05], kinds = [Onboarding, Onboarding, Rules memory, Onboarding, Strategy, Strategy, Dynamics, Rules hole], names as in the lecture table.

**Test values (must match).**
- n = 5, explain off: Bars A = 96.9, 92.2, 84.4, 76.3, 67.2, 55.6, 41.0, 22.6%; expected 5.36.
- n = 5, explain on: expected 2.71; onboarding seen 0.00 of 3.
- n = 1: expected 1.96 (off), 0.81 (on). n = 3: 4.20 / 1.96. n = 10: 6.66 / 3.72. n = 15: 7.19 / 4.20.
- Testers for 90% on problem 8 (p = 0.05): 45. On p = 0.31: 7.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. All controls keyboard operable with visible labels; the left chart has a text table fallback (toggle "Show as table") with the values at n = 1, 3, 5, 10, 15, 30. Respect `prefers-reduced-motion` (no line animation) and `prefers-color-scheme`. No game art; the problems are text rows.
