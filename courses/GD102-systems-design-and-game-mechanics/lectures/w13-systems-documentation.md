# GD102 · Week 13 — Systems Documentation

**Why this matters:** A system you cannot write down is a system nobody else can build, test or tune. The sentence "players get a life every 30 minutes, up to 5" sounds complete, yet it allows at least three different implementations, and one of them quietly takes a third of the income away from your most loyal players. This week you learn to write a system specification that closes those gaps before an engineer has to guess.

**You will be able to:**
- Write a system specification with stocks, flows, rules, a parameter table, derived numbers and edge cases, so that an engineer can build it and QA can test it without asking you.
- Derive the "knee" of a capped regeneration system (cap × regeneration time) and use it to state the play rhythm the system rewards.
- Rewrite a vague rule as testable statements and given/when/then test cases.
- Critique a system document by finding the rules it leaves undefined and computing what each reading would do to players.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 1 (designing game mechanics, the section on mechanics and the design process) and skim the Machinations chapters you used in weeks 5 and 6; Meadows, *Thinking in Systems* (2008), chapter 1 (stocks, flows and the "bathtub"). Bring the Machinations diagram you built for week 7.

**Prerequisites from earlier courses:** design documents, one-pagers and pitches from GD101 [week 14](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md); stocks and flows (week 2), feedback loops (weeks 3 and 4) and Machinations diagrams (weeks 5 and 6) from this course ([week 2](w02-stocks-and-flows.md), [week 3](w03-positive-feedback-loops-snowballing.md), [week 4](w04-negative-feedback-loops-rubber-banding.md), [week 5](w05-machinations-diagrams-i.md), [week 6](w06-machinations-diagrams-ii-converters-traders-gates.md)); caps written as `min` and `max` from [MA101 week 7](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md).

**Interactive:** [Refill timer knee](../examples/w13-refill-timer.html). Keep it open during section 2.

---

## 1. What a system document is for

In GD101 you wrote one-pagers and pitches. Those documents sell an idea. Their reader is a producer, a publisher or a teammate deciding whether to spend time on the game. A system document has a different reader and a different job. Its readers are the people who will make the system real:

- The **engineer** who implements it. They need every rule, every number and every edge case, because code cannot say "roughly".
- The **QA tester** who checks it. They need statements they can prove true or false.
- The **other designers** who connect their systems to yours. They need to know what your system consumes and produces.
- **You, three months later**, trying to remember why the cap is 5 and not 6.

Here is the test this lecture keeps returning to. **A system document is done when someone can build and test the system without asking you a question.** Every question they would have to ask is a hole. Every hole gets filled by somebody's guess, usually the engineer's, usually at 6 pm, usually in the way that is easiest to code.

The easiest implementation is often reasonable. The trouble is that "reasonable" can mean several things, and the differences show up in the numbers players feel. Section 2 shows a concrete case.

### Systems documents describe models, not features

A feature description says what the player sees, such as "a lives counter with a timer under it." A system description says which quantities are stored (stocks), what changes them (flows), what limits them (caps, floors, gates) and which feedback loops connect them. That vocabulary is the outline of your document.

If you built a Machinations diagram for a system, you already have most of a system document. The diagram shows the stocks and flows. The document adds what a diagram cannot hold: the exact timing of each flow, what happens at the edges, why each number is what it is, and how you will know the system is working after launch.

## 2. Worked example: documenting a refill timer

### The hook

Candy Crush Saga gives players five lives. Failing a level costs one. A lost life comes back on its own, one every half hour, and players can also buy or receive more. That is the whole rule as most players would describe it, and as most design documents would write it.

Now try to implement it. Suppose a player has 2 lives and 15 minutes on the timer, and then plays and fails a level. Does the timer keep its 15 minutes, or start again from zero? Suppose the player is at 5 lives. Is the timer still running, so a life "arrives" and is thrown away every 30 minutes, or is it paused? Suppose the player closes the game for three hours. Are they owed six lives? The one-line rule answers none of these questions. Each answer changes how many lives a real player gets per day.

We will not claim to know how King implements these details inside Candy Crush. The point of this example is that you, writing your own refill timer, must decide them, and the document is where the decision lives.

### The model

Start with the stock and the flow. `L` is the number of lives, a stock. It has one inflow (regeneration) and one outflow (spending a life on a failed level). The inflow is capped.

Name every symbol:

- `C` is the **cap**, the most lives the regeneration can fill to. Candy Crush uses 5.
- `R` is the **regeneration time**, how long one life takes to come back. Candy Crush uses 30 minutes.
- `T` is the **check-in interval**, how long the player stays away between sessions. This is a player behavior, not a parameter you set, and your system has to work for every value of it.

Assume the simplest player. They come back every `T` hours and play until their lives run out. In one visit they spend everything that regenerated while they were gone, up to the cap:

```
lives per visit  = min(C, T / R)
lives per day    = (24 / T) × min(C, T / R)
```

Split the `min` into its two pieces (this is the piecewise reading from MA101 week 7):

```
if T ≤ C × R:   lives per day = 24 / R           (the full regeneration rate)
if T > C × R:   lives per day = 24 × C / T       (capped; falls as 1/T)
```

The switch happens at one point, which this lecture calls **the knee**:

```
knee = C × R
```

For Candy Crush's numbers the knee is `5 × 30 min = 2.5 hours`. Any player who returns at least every 2.5 hours receives the full 48 lives a day. A player who returns less often receives less, and the lost lives are not delayed, they are gone. They were regenerated into a full stock and discarded.

That is the model. The knee is the most useful single number in the document, because it tells every reader the play rhythm the system rewards. A designer who writes "5 lives, 30 minutes" has chosen a 2.5-hour rhythm whether they meant to or not. A designer who writes "the knee is 2.5 hours, by design, because we want players to fit a session into each part of their day" has made a decision a reviewer can argue with.

### Numbers you can check

Use `C = 5`, `R = 30 min`, and a player who spends every life at each visit. Work each row from the formulas above.

| Check-in interval `T` | Lives per visit | Visits per day | Lives per day | Share of maximum | Lives lost to the cap per day |
|---|---|---|---|---|---|
| 1 h | 2 | 24 | 48 | 100% | 0 |
| 2 h | 4 | 12 | 48 | 100% | 0 |
| 2.5 h (the knee) | 5 | 9.6 | 48 | 100% | 0 |
| 3 h | 5 | 8 | 40 | 83% | 8 |
| 4 h | 5 | 6 | 30 | 63% | 18 |
| 8 h | 5 | 3 | 15 | 31% | 33 |
| 12 h | 5 | 2 | 10 | 21% | 38 |
| 24 h | 5 | 1 | 5 | 10% | 43 |

Below the knee, checking in more often gains nothing. The one-hour player and the two-hour player get the same 48 lives. Above the knee the loss is steep. A player who opens the game morning and evening gets about a fifth of what the system can produce.

### The rule the sentence did not define

Now the hole from the hook. Three plausible implementations of "a life every 30 minutes, up to 5":

- **Wall clock.** A life arrives at every multiple of 30 minutes since some fixed start. If the stock is full, that life is discarded.
- **Pause at full.** The timer runs only while `L < C`. When you spend a life below the cap, the timer keeps its progress. When the stock fills, the timer stops and resets.
- **Restart on spend.** Every time a life is spent, the timer starts again from zero, throwing away partial progress.

The third is a natural bug. An engineer writes "when a life is spent, start the refill timer" and forgets the timer may already be running.

A minute-by-minute simulation over three weeks, for a player who checks in every `T` and spends every life, gives:

| Check-in interval `T` | Wall clock | Pause at full | Restart on spend |
|---|---|---|---|
| 30 min | 48 | 48 | 48 |
| 45 min | 48 | 48 | 32 |
| 60 min | 48 | 48 | 48 |
| 100 min | 48.1 | 48.1 | 43.3 |
| 4 h | 30 | 30 | 30 |

(The 48.1 is rounding in a finite simulation window; the long-run value is 48.)

You can check the 45-minute row by hand. Under restart on spend, the player arrives 45 minutes after spending. The timer finished one life at 30 minutes and has 15 minutes of progress toward the next. The player spends that one life, and the spend wipes the 15 minutes. So every visit yields exactly one life: 32 visits a day, 32 lives. Under the other two rules the 15 minutes carry over, and the player averages 1.5 lives per visit, 48 a day.

Notice who is hurt. Restart on spend changes nothing for a player who checks in every 4 hours. It punishes frequent players whose interval is not a whole multiple of `R`, your most engaged players. That is what a hole in a document costs. It creates a behavior difference that falls on one group of players, and nobody chose it.

Wall clock and pause at full agree on every row of this table. They differ elsewhere. Under wall clock, the first life after a spend from full can arrive in less than 30 minutes, because the clock does not care when you spent. Under pause at full, it always takes exactly 30. A tester can check that difference in one minute, so the document must say which one you want.

### See it move

Open the interactive. The top view is a timeline of the lives stock over one day, with the player's visits marked and the regenerated-but-discarded lives shaded in the warning color. Drag the check-in interval past 2.5 hours and watch the shading appear. The bottom view plots lives per day against the check-in interval. It stays flat at 48 until the knee, then falls as `1/T`. Now switch the timer rule to "restart on spend" and set the interval to 45 minutes. The top timeline barely changes shape, but the bottom curve grows a set of dips at every interval that is not a multiple of 30 minutes. The one-line rule hid those dips. The document has to rule them out.

### Cross-game recognition

The capped regenerating stock is one of the most common structures in games. Once you look for the knee, you find a design decision in each.

**World of Warcraft, rested experience (retail, Dragonflight-era documentation).** While a character is logged out in an inn or a capital city, it accumulates "rested" experience at one bubble, 10% of a level, every 16 hours. Outside a rest area it accumulates at a quarter of that rate. The stock is capped at 15 bubbles, 150% of a level. While rested, the character earns double experience from kills and several gathering activities, which drains the stock. In this lecture's form, `R = 16 h` per bubble, `C = 15` bubbles, so the knee is `15 × 16 h = 240 h`, ten days. Compare that with Candy Crush's 2.5 hours. Blizzard chose a system that rewards coming back after a break and punishes nobody who plays a few times a week. A player away for a month loses accrual, but that is a small group. Same stock, same `min`, a knee 96 times longer (240 h against 2.5 h), and a completely different play rhythm.

**EVE Online, skill training (before and after the Phoebe release, November 2014).** EVE characters train skills in real time, whether or not the player is logged in. Before the Phoebe release of 4 November 2014, the skill queue only let a player schedule skills to start within the next 24 hours. The queue behaved like a cap measured in time. Once the scheduled skills finished, training stopped until the player logged in to add more. The knee was roughly a day, so players who could not log in daily lost training time. Phoebe raised the queue to 50 skills and up to ten years. In this lecture's terms, CCP moved the knee from about a day to effectively infinite, which removed the pressure to log in every day. That is a documented, deliberate change to exactly the parameter this worked example is about.

Three games share one structure, a stock with a capped inflow and a knee at cap × rate. When you read any energy, stamina, rest or queue system, compute the knee first. It tells you what rhythm of play the designer is paying for.

### Eyes-open design judgment

The capped timer is a strong tool with clear costs. Here is what your document should decide on purpose.

- **The knee is a statement about the player's day.** A short knee (minutes to a few hours) asks for many short sessions and turns the timer into a reason to come back. A long knee (days) rewards returning and punishes nobody. Pick the knee first, then choose `C` and `R` to hit it. Changing `R` alone changes both the knee and the daily maximum; changing `C` alone changes only the knee.
- **Lost lives are invisible to the player.** Nothing in the interface says "you just lost 33 lives today by sleeping." Players feel it as scarcity, not as a rule. If you want the system to feel fair, consider showing "full in 1 h 30 min" so players can plan around the knee.
- **Timer semantics are a fairness decision.** Restart on spend penalizes frequent players. Wall clock can hand out a life a few seconds after a spend. Pause at full is the least surprising, and it is the one to choose unless you have a reason.
- **The time source must be named.** If the timer is computed from the device clock, a player who moves the clock forward gets free lives. If it is computed from the server, offline play needs a rule. Either way, the document must say which clock is authoritative. This course does not need to know how any specific game handles it; your spec does.
- **Overfill needs a rule.** Can bought or gifted lives take `L` above `C`, and does regeneration stop until `L` falls back? Write it down.
- **Alternatives exist.** No cap (the post-Phoebe EVE queue) removes the pressure to return and the timer's pacing role with it. A slower rate in some conditions, like WoW's out-of-town rest, moves the knee without removing it. Draw the lives-per-day curve for each before you choose.

## 3. The anatomy of a system specification

The refill timer shows why each part of a system document exists. Here is the template this course uses for the final system design document (SDD). Use these headings in this order. Section numbers make review comments easy ("4.3 is ambiguous").

1. **Purpose.** One or two sentences in player terms, then one sentence naming the design goal the system serves. "Lives limit how many levels a player can fail in a row, so that sessions stay short and the player returns later. Target rhythm: one session every 2 to 3 hours."
2. **Vocabulary.** Every term with a precise meaning. "Life: one attempt at a level. Spent when a level is failed, not when it is started." Most arguments between designers and engineers turn out to be two meanings of one word.
3. **Model.** The stocks, flows and feedback loops, as a Machinations diagram or a stock-flow sketch, plus a sentence for each loop saying whether it is reinforcing or balancing.
4. **Rules.** Numbered, testable statements. Section 4 below explains how to write them.
5. **Parameters.** A table of every tunable number. Section 3.1 shows the format.
6. **Derived numbers.** Values that follow from the parameters and tell a reader what the system does: the knee, the daily maximum, the equilibrium stock, the time to reach a milestone. Readers skip formulas and read these.
7. **Edge cases and states.** What happens at zero, at the cap, offline, across a patch, on two devices at once, when the parameter changes while a player has a stock.
8. **Interfaces.** What this system reads from other systems and what it writes to them. "Reads: level result (win/fail). Writes: lives count to the HUD; purchase events to the store."
9. **Telemetry and success criteria.** What you will log and what result means the system works. "Median lives lost to the cap per active player per day below 10."
10. **Open questions and change log.** Decisions not yet made, with an owner, and a dated list of every change.

### 3.1 The parameter table

The parameter table is the part of the document engineers read most and designers maintain worst. Give every parameter these columns:

| Name | Value | Unit | Safe range | Why this value | Owner |
|---|---|---|---|---|---|
| `lives_cap` | 5 | lives | 3 to 8 | Knee of 2.5 h with `regen_minutes = 30` | Systems designer |
| `regen_minutes` | 30 | minutes per life | 15 to 60 | Daily maximum of 48 lives | Systems designer |
| `timer_rule` | pause_at_full | enum | pause_at_full, wall_clock | Least surprising; see rule 4.3 | Systems designer |
| `clock_source` | server | enum | server | Device clock can be changed by the player | Engineering |

Four habits make the table useful.

- **Units in their own column.** "30" is not a value. "30 minutes per life" is. Many bugs are unit bugs.
- **A safe range.** It tells the person tuning the system later how far they can move the number before the design breaks. It also tells QA which values to test.
- **A reason.** "Why 5?" should have an answer in the document. If the honest answer is "placeholder," write that. A placeholder marked as a placeholder is fine. A placeholder that looks like a decision is how bad numbers ship.
- **Names that match the data.** The name in the document should be the name in the data file or spreadsheet, so a search finds both. Next week's spreadsheet uses exactly these names in its inputs tab.

### 3.2 Derived numbers go next to the parameters

Put the knee, the daily maximum and other derived numbers in a small table after the parameters, each with its formula. When someone changes `lives_cap` from 5 to 6, the table shows the knee moving from 2.5 h to 3 h. Without it, the change looks like a small gift. With it, the change is visibly a new play rhythm.

## 4. Writing rules that can be tested

A rule in a system document should read like something a tester can prove false. Compare:

- Vague: "Lives regenerate over time."
- Testable: "4.1 While `lives < lives_cap`, one life is added each time the refill timer reaches `regen_minutes`."

Guidelines that make rules testable:

- **One rule per numbered line.** "4.2 When a life is spent while `lives < lives_cap`, the refill timer keeps its progress." "4.3 When `lives` reaches `lives_cap`, the refill timer stops and resets to zero." Each can pass or fail on its own.
- **Use "must" or plain present tense, never "should" or "usually".** "Should" invites an engineer to decide it is optional.
- **Name the parameter, not the number.** Write `regen_minutes`, not 30. When the number is tuned, the rule stays true.
- **State boundaries explicitly.** Is the cap `≤` or `<`? Does the timer tick at exactly 30:00 or after it? At the edges of a rule, "roughly" becomes a bug.

### Given, when, then

For every rule that has an edge case, add a test case in a fixed three-part form. It is borrowed from software testing and it works for design.

| # | Given | When | Then |
|---|---|---|---|
| T1 | `lives = 2`, timer at 15:00 | a life is spent | `lives = 1`, timer at 15:00 |
| T2 | `lives = 5`, timer stopped | a life is spent | `lives = 4`, timer starts at 0:00 |
| T3 | `lives = 4`, timer at 29:59 | one second passes | `lives = 5`, timer stopped |
| T4 | `lives = 0`, player offline for 3 h | player opens the game | `lives = 5`, timer stopped |

Test T1 is the one that rules out restart on spend. Test T4 is the one that rules out "owed six lives." A document with these four rows answers every question from the hook. Notice that writing the test cases is where you find the holes. If you cannot fill in the "then" column, the rule above it is not finished.

### Diagrams: which one for which question

- **Machinations or stock-flow diagrams** answer "where do resources come from and go?" Use them in the Model section.
- **State diagrams** answer "what modes can this be in, and what moves it between them?" The refill timer has two states, running and stopped. Drawing them makes missing transitions obvious.
- **Timelines** answer "what happens in what order?" Draw one for anything with timers, cooldowns or offline time.
- **Tables** answer "what are all the cases?" When a paragraph says "if this, then that, unless the other," make it a table.

## 5. Keeping the document alive

A system document written once and never touched again is worse than none, because people trust it. Three practices keep it honest.

**One source of truth per number.** A number should live in exactly one place. If `regen_minutes` is 30 in the document, 25 in the spreadsheet and 30 in the data file, somebody will tune the wrong one. The usual arrangement is that the data file (or the spreadsheet that exports it) is the source of truth, and the document names the parameter and points there. Next week's lecture builds that spreadsheet. Data-driven design, where tuning values live in data files rather than code, is covered from the programming side in CS102 week 13 ([CS102 syllabus](../../CS102-programming-for-games-ii-structures-and-patterns/syllabus.md)).

**A dated change log.** Every change gets a line: date, what changed, why, and who approved it. "2026-11-02: `lives_cap` 5 to 6. Knee moves from 2.5 h to 3 h. Reason: evening players losing too many lives in the week-2 playtest." Six months later that line is the only record of the reasoning.

**A one-page view.** Long documents go unread. Stone Librande's GDC 2010 talk on one-page designs argued for putting a whole design on a single page, on the grounds that most people only read the first page anyway. Use that as the front page of your SDD: the stock-flow diagram, the parameter table, the derived numbers and the knee. The full rules and test cases follow behind it for the people who need them. In GD101 you met the one-pager as a pitch. Here it is a reference.

Tim Ryan's 1999 Gamasutra series on design documents separated concept, proposal and detailed specification into different documents for different readers. That still holds. Keep your pitch out of your spec, and your parameter table out of your pitch.

### When the game and the document disagree

When a playtester finds the game doing something the document does not say, either the build is wrong (file a bug) or the build found a better behavior (update the document and the change log). Never leave both standing. MMO303 week 14 shows what happens when the player-facing version of this problem, patch notes that say one thing while the game does another, reaches players ([MMO303 week 14](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md)).

## In-class activity (25 min)

Work in pairs. Materials: the one-line rule below, the interactive, paper.

> "Players have up to 3 stamina charges. A charge refills every 2 hours. Entering a dungeon costs 1 charge. Players can buy a charge for 10 gems."

1. **Derived numbers (5 min).** Compute the knee and the daily maximum. Name the play rhythm this system rewards in one sentence.
2. **Find the holes (8 min).** List every question an engineer would have to ask. You should find at least five. Hints: timer behavior on spend, behavior at the cap, buying at the cap, offline time, what "entering" means if the player disconnects inside.
3. **Write the rules (7 min).** Write numbered, testable rules that close each hole, and a parameter table with units, safe ranges and reasons.
4. **Swap and attack (5 min).** Give your rules to another pair. They write one given/when/then case your rules cannot answer. If they succeed, you fix your rules.

Expected output: one page with derived numbers, 5 to 8 rules, a parameter table and at least four test cases. Keep it. It is a good first draft for lab 13.

## Common misconceptions

- **"The design is in my head, the document is paperwork."** The document is where decisions become visible. The restart-on-spend dip in section 2 is a real design decision that nobody made, because nobody wrote the rule down.
- **"More detail is always better."** Detail belongs in rules, parameters and test cases. Prose explaining the same rule three ways adds contradictions, not clarity. If a paragraph restates a table, delete the paragraph.
- **"Checking in more often always gives more."** Only below the knee does the regeneration rate limit you, and there more visits change nothing. Above the knee each extra visit matters a lot. Ask which side of the knee a player is on.
- **"A cap is just a safety limit."** A cap on a regenerating stock sets the play rhythm through the knee. Changing it is a design change, and the derived-numbers table should make that visible.

## Check yourself

1. A mobile game gives 1 energy every 6 minutes with a cap of 120. Compute the knee and the daily maximum. A player checks in every 8 hours and spends everything. How much energy do they get per day, and what share of the maximum is that?
2. You want a knee of 4 hours and a daily maximum of 36 lives. What `C` and `R` do you need?
3. Under restart on spend with `R = 30 min`, a player checks in every 50 minutes and spends everything. How many lives do they get per visit and per day? What do they get under pause at full?
4. A document says "the timer pauses when lives are full." Write two given/when/then cases that a correct implementation passes and a wall-clock implementation fails.

<details>
<summary>Answers</summary>

1. Knee `= C × R = 120 × 6 min = 720 min = 12 h`. Daily maximum `= 24 h / 6 min = 240`. At `T = 8 h`, the player is below the knee, so they get the full `8 h / 6 min = 80` per visit, 3 visits, 240 per day, 100% of the maximum.
2. Daily maximum `= 24 / R = 36`, so `R = 24 h / 36 = 40 min`. Knee `= C × R = 4 h = 240 min`, so `C = 240 / 40 = 6`.
3. Under restart on spend, each visit finds one life done (at 30 minutes) and 20 minutes of progress, which the spend wipes. One life per visit. Visits per day `= 1440 / 50 = 28.8`, so 28.8 lives per day. Under pause at full the 20 minutes carry over, so the player averages `50 / 30 ≈ 1.67` lives per visit and gets the full 48 per day. Restart on spend costs this player 40% of their income.
4. Example cases. (a) Given `lives = cap` for 45 minutes, when a life is spent, then the next life arrives exactly `R` later. Under wall clock it can arrive sooner, because the clock kept ticking while full. (b) Given `lives = cap`, when the player checks the timer display, then it shows stopped (or full). Under wall clock a running timer is visible. Other correct answers exist; the case must separate the two rules.

</details>

## Lab hook

**Lab 13, write a system specification** ([labs/lab13.md](../labs/lab13.md)). You write a complete specification for a crafting-energy system from a deliberately vague brief, including derived numbers, rules, a parameter table and test cases. A classmate then tries to implement it on paper from your document alone, and every question they ask counts against the document. The specification becomes a section of your final SDD in week 15.

## Sources

- Wikipedia, "Candy Crush Saga" (accessed September 2026). Players start with five lives, and a life is restored every half-hour; lives can also be bought. This lecture does not claim how King implements timer details; the three timer rules are hypothetical implementations used to show why a document must choose.
- Warcraft Wiki, "Rest" (retail World of Warcraft, page describing the Dragonflight era, patch 10.x; accessed September 2026). One bubble (10% of a level) per 16 hours in an inn or capital city, a quarter of that rate elsewhere, cap of 15 bubbles (150% of a level), and double experience from kills and several gathering activities while rested.
- Wikipedia, "Eve Online" (accessed September 2026). Skills train in real time even while the player is logged out; the skill queue allows up to 50 skills and up to 10 years of training; before the Phoebe release of 4 November 2014 skills could only be scheduled to start within the next 24 hours.
- Librande, S. (2010). "One-Page Designs." GDC 2010, GDC Vault session 1012356 (accessed September 2026). Argues for single-page design documents.
- Ryan, T. (1999, October 19). "The Anatomy of a Design Document, Part 1." Gamasutra (now gamedeveloper.com, accessed September 2026). Part 1 covers concept and proposal documents; part 2 (17 December 1999) covers the specifications.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Internal economies and Machinations diagrams as a design and documentation tool.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 1, stocks, flows and balancing loops.
- The lives-per-day tables in section 2 are computed from the model in this lecture (closed form) and from a minute-by-minute simulation over a 21-day window, which the interactive reproduces.

## Interactive spec: examples/w13-refill-timer.html

**The one insight the visual must make obvious:** a capped refill timer has a knee at `C × R`. Below it, extra visits gain nothing; above it, lives are silently thrown away. And the undocumented timer rule ("restart on spend") cuts income for frequent players at intervals that are not multiples of `R`.

**Layout.** Two linked views stacked vertically (side by side at 1,000 px and wider).

- **Top view, "One day of lives".** A step chart of `lives` (y, 0 to `C`, integer gridlines) against time of day (x, 0 to 24 h, gridline every 2 h). Visits are vertical tick marks on the x axis with a small "visit" label. At each visit the line drops to 0. Regeneration events are small dots on the line. Every regeneration event that would have occurred while `lives = C` (wall-clock rule) or every whole `R` that elapsed while full (other rules, computed as potential lives) is drawn as a hollow dot in the warning color above the cap line, labelled "lost to the cap". The simulated day is day 8 of a 21-day run so the start-up transient is gone.
- **Bottom view, "Lives per day vs check-in interval".** x axis: check-in interval `T` from 15 min to 24 h on a log scale with labelled ticks at 30 min, 1 h, 2 h, 4 h, 8 h, 12 h, 24 h. y axis: lives per day, 0 to `24 h / R` plus 10%. Draw the closed-form curve `(24/T) × min(C, T/R)` as a solid line and, for the selected timer rule, the simulated curve as a second line (sampled every minute of `T` from 15 to 180 min, then every 15 min to 24 h). Mark the knee with a vertical dashed line labelled "knee = C × R = 2.5 h" (text updates). A draggable marker at the current `T` links to the top view.

**Controls** (all keyboard accessible, with visible numeric values):

- Cap `C`: integer slider 1 to 20, default 5.
- Regeneration time `R`: slider 5 to 120 minutes, step 5, default 30.
- Check-in interval `T`: slider 15 min to 24 h (log scale), default 3 h. Arrow keys step by 5 minutes below 3 h and 15 minutes above.
- Timer rule: segmented control with "Pause at full" (default), "Wall clock", "Restart on spend".
- Presets: "Candy Crush lives (5, 30 min)", "WoW rested XP (15 bubbles, 16 h)". The WoW preset switches units to hours, sets `R = 960 min`, `C = 15`, and extends the `T` range to 30 days with the x axis of the top view set to 30 days. Label it "rested XP bubbles" instead of lives.

**Readouts** (next to the charts, copyable): knee (h:mm), daily maximum `24 h / R`, lives per visit, lives per day (closed form and simulated for the current rule), share of maximum, lives lost to the cap per day.

**Simulation (exact).** Integer minutes. State: `lives` (start `C`), `timer` (start 0). For each minute `t = 1 … 21 × 1440 − 1`:
- Wall clock: if `t mod R == 0`, add 1 if `lives < C`, else count 1 lost.
- Pause at full and restart on spend: if `lives < C`, `timer += 1`; if `timer ≥ R`, `lives += 1`, `timer = 0`. If `lives == C`, `timer = 0`.
Then, if `t mod T == 0` (and at `t = 0`), the player spends all lives (`lives = 0`); under restart on spend also set `timer = 0`. Report per-day averages over days 8 to 21 (`t ≥ 7 × 1440`).

**Test values** (`C = 5`, `R = 30`, lives per day over days 8 to 21):

| `T` | Pause at full | Wall clock | Restart on spend |
|---|---|---|---|
| 30 min | 48 | 48 | 48 |
| 45 min | 48 | 48 | 32 |
| 60 min | 48 | 48 | 48 |
| 100 min | 48.1 | 48.1 | 43.3 |
| 3 h | 40 | 40 | 40 |
| 4 h | 30 | 30 | 30 |
| 8 h | 15 | 15 | 15 |
| 24 h | 5 | 5 | 5 |

Closed form: knee 2.5 h, daily maximum 48, lives lost per day at 8 h = 33 (wall clock counts them directly; for the other rules show `48 − lives per day`). WoW preset: knee 240 h (10 days).

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark themes, `prefers-reduced-motion` disables the line-draw animation. No game art or logos; lives are drawn as plain circles. A text summary under the charts restates the current numbers in one sentence, for example "Checking in every 3 h, you get 40 of 48 possible lives a day; 8 are lost to the cap."
