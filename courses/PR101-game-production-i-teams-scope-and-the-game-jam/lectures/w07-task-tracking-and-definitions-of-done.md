# PR101 · Week 07 — Task Tracking and Definitions of Done

**Why this matters:** Next week you make a game in 48 hours. The most common way a jam team loses is not a missing skill. It is a board where every card says "in progress" at hour 40 and nothing is playable. This week gives you a board that tells the truth, a rule that keeps it honest, and one line of math that explains why starting more work finishes less.

**You will be able to:**
- Split a feature into tasks of four person-hours or less, each with acceptance criteria someone else can check.
- Compute cycle time, work in progress and throughput with Little's law, and predict what a WIP limit does to a team's output before a deadline.
- Write a definition of done for a jam team and explain what hidden work it prevents.
- Critique a task board and name the column where work is piling up.

**Before class:** Clinton Keith, *Agile Game Development* (2nd ed., 2020), the chapter on Kanban and the section on definitions of done in the Scrum chapters (about 30 pages). Ken Schwaber and Jeff Sutherland, *The Scrum Guide* (November 2020), the short section "Commitment: Definition of Done" (one page, free at scrumguides.org).

**Prerequisites from earlier courses:** [PR101 week 1, roles on a game team](w01-roles-on-a-game-team.md) (the producer owns the task list). [PR101 week 2, Git](w02-git-fundamentals-and-branching.md) (one short branch per task, which only works if tasks are small). [PR101 week 5, agile and Scrum](w05-agile-and-scrum-adapted-for-games.md) (stand-ups and jam check-ins) and [week 6, estimation](w06-estimation-and-why-it-fails.md) (where card estimates come from). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (rates like "tasks per hour"). [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (why a playable build early beats a perfect build late).

**Interactive:** [examples/w07-wip-limit.html](../examples/w07-wip-limit.html). Keep it open during section 2.

---

## 1. What a task board is for

A **task board** is a shared list of the work a team has agreed to do, arranged in columns that show where each piece of work is. The simplest board that works for a game team has four columns:

| To do | Doing | Review | Done |
|---|---|---|---|
| Agreed, not started | Someone is working on it now | Built, waiting for a second person to check it | Meets the definition of done |

Each piece of work is a **card** (or ticket, or issue; the tools use different names for the same thing). A good card has five fields:

- **Title**, written as a verb and an object: "Add dash to player", not "Dash".
- **Owner**, one person. Two names on a card means nobody owns it.
- **Estimate**, in person-hours, from your week 6 method.
- **Tier**, must, should or could (MVP, slice or polish in week 4's terms), so the cut list can find it.
- **Acceptance criteria**, one or more sentences that are true or false in a build. "Player dashes 3 tiles in 0.2 s when Shift is pressed, with a 1 s cooldown shown on the HUD."

The board is not a to-do list for one person. It is how four people who are all busy can see the state of the game without asking each other. Week 1 made the producer the owner of the list. That doesn't mean the producer writes every card. It means the producer notices when the board and the game disagree, and fixes the board.

### Splitting work into tasks

Games have a habit of producing cards like "Enemy AI" or "Level 2". Those are not tasks. They are projects with a task-shaped label. You can't estimate them, you can't review them, and they sit in "Doing" for two days while the owner insists they are "mostly done."

Split until each card passes three tests:

1. **It fits in four person-hours** during the jam, or two working days during the term. The two-day rule is the same one week 2 gave for branch lifetime. One card, one branch, merged within two days.
2. **It changes something you can see in a build.** "Write enemy state machine class" fails. "Enemy walks toward the player when closer than 5 tiles" passes. Tasks that produce visible changes can be reviewed by playing, and they show progress on the board that matches progress in the game.
3. **Someone other than the owner can check it** by reading the acceptance criteria and playing the build.

Here is "Enemy AI" split for a jam:

| Card | Estimate | Acceptance criteria |
|---|---|---|
| Enemy idles in place with an idle animation | 1 h | Enemy placed in the test room plays its idle loop and does not move |
| Enemy chases player within 5 tiles | 2 h | Enemy moves toward the player when within 5 tiles and stops at walls |
| Enemy deals 1 damage on touch | 1.5 h | Touching the enemy removes 1 health and gives 1 s of invulnerability |
| Enemy dies at 0 health with a sound | 1.5 h | Three hits kill the enemy; a death sound plays; the enemy is removed |

Six hours of work, four cards, and every card could be cut on its own if time ran out. The first card alone gives the level designer something to place. That is the point of a vertical split: each slice is useful before the next one exists.

## 2. Worked example: why starting more finishes less

### The hook

Duke Nukem Forever was announced by 3D Realms in April 1997 with a Christmas 1998 target. It was released in June 2011, fourteen years later. As the delays piled up, George Broussard of 3D Realms answered questions about the date by saying the game would ship "when it's done." Years of work were in progress, and there was no shared, checkable meaning of done.

You won't take fourteen years. But you will feel a small version of it. In 1985, Jon Bentley's "Programming Pearls" column in *Communications of the ACM* passed on a joke from Tom Cargill of Bell Labs: the first 90 percent of the code takes the first 90 percent of the time, and the last 10 percent takes the other 90 percent. Jam teams live this joke at hour 40. Every card is started. Every card is "90 percent." The game does not run from title screen to ending.

Why does a team that is working hard, all the time, end up with nothing finished? There is a law about this.

### The model

Watch any board for a while and you can measure three numbers:

- **Work in progress (WIP)**, `L`: how many cards are started but not done, on average.
- **Throughput**, `λ` (lambda): how many cards reach Done per hour, on average.
- **Cycle time**, `W`: how long a card takes from the moment someone starts it to the moment it is done, on average.

A warning about letters. These are the standard symbols for Little's law, and every queueing text uses them, so this course keeps them. They are not week 5's symbols. In [week 5](w05-agile-and-scrum-adapted-for-games.md), `L` was the sprint length, `λ` the rate of wrong turns and `W` the team's capacity. In this lecture, in its interactive and in week 10, `L`, `λ` and `W` always mean WIP, throughput and cycle time.

**Little's law** connects them:

```
L = λ × W        so        W = L / λ
```

Average cycle time equals average WIP divided by throughput. John Little proved it in 1961 for queues of customers, and it holds for any stable system where things arrive, wait and leave: shoppers in a store, players in a login queue, cards on a board. It needs no assumptions about how the work is done. It only needs averages taken over a long enough stretch.

Read it the way a producer should. Your team's throughput is set by how many people you have and how fast they work. You can't raise it by wishing. So **if you raise WIP, cycle time rises in proportion.** Twice as many cards in progress, with the same people, means each card takes twice as long to finish.

Little's law tells you that cycle time rises. To see *when* cards finish, which is what matters before a deadline, we need a small model of how people share work. Assume:

- `n` people, all equally fast.
- `N` cards, each needing `s` person-hours.
- A **WIP limit** `w`: the team never has more than `w` cards in Doing.
- If there are more cards in Doing than people, people split their time evenly across them, so every card in the batch advances at the same speed. Each person carries `k = b / n` cards, where `b` is the number of cards in the batch (and `k = 1` if `b` is smaller than `n`, since one card can only use one person).
- Every extra card a person juggles costs a **switching overhead** `c`: the time spent reloading your head, reopening files and asking "where was I?" The batch takes

```
d = s × k × (1 + c × (k − 1))
```

hours. With one card per person (`k = 1`), `d = s`. With three cards per person and `c = 0.1`, each card takes `3 × 1.2 = 3.6` times as long as it would alone.

### Numbers you can check

A four-person jam team (`n = 4`) has twelve cards of three person-hours each (`N = 12`, `s = 3`). That's 36 person-hours of work, nine hours of clock time if nobody wastes a minute. The team has promised a playtest at hour 8. Only Done cards count at the playtest, because a half-built feature can't be played. Compare WIP limits, first with no switching cost, then with `c = 0.1`:

| WIP limit `w` | Cards finish at (h), `c = 0` | Done by hour 8 | Average cycle time `W` | Cards finish at (h), `c = 0.1` | Done by hour 8 |
|---|---|---|---|---|---|
| 2 | 3, 6, 9, 12, 15, 18 | 4 | 3 h | same | 4 |
| 4 | 3, 6, 9 | 8 | 3 h | same | 8 |
| 6 | 4.5, 9 | 6 | 4.5 h | 4.725, 9.45 | 6 |
| 8 | 6, 9 | 8 | 5 h | 6.6, 9.6 | 8 |
| 12 (no limit) | 9 | **0** | 9 h | 10.8 | **0** |

Check one row by hand. With `w = 12` and `c = 0.1`, all twelve cards start together. Each person carries `k = 3` cards, so `d = 3 × 3 × (1 + 0.1 × 2) = 10.8` hours. Every card finishes at the same moment, 10.8 hours in. At the hour 8 playtest the board shows twelve cards in Doing and zero in Done. The team has worked 32 person-hours and has nothing to show.

With `w = 4`, each person takes one card. Four cards are done at hour 3, four more at hour 6. At the playtest there are eight playable features.

Now check Little's law on the `c = 0` column. For `w = 4`: WIP is 4 the whole time, throughput is 12 cards in 9 hours = 1.33 per hour, and `W = 4 / 1.33 = 3` hours. For `w = 12`: WIP is 12, throughput is the same 1.33 per hour, and `W = 12 / 1.33 = 9` hours. **Same throughput, same people, three times the cycle time.** For `w = 8` the WIP is 8 for six hours and 4 for three, an average of `(8 × 6 + 4 × 3) / 9 = 6.67`, and `6.67 / 1.33 = 5` hours, matching the table.

Three things stand out.

- With no switching cost, every limit from 4 to 12 finishes the whole list at hour 9. The limit doesn't change *how much* gets done by the end. It changes *when* things become done, and a jam, a playtest and a milestone all cut the work off at a fixed time.
- Too low a limit also hurts. With `w = 2`, two people sit idle, throughput halves, and the list takes 18 hours.
- Switching costs make big WIP worse on every count. With `c = 0.1` the unlimited board finishes 1.8 hours late, and the moderate limits lose time too.

The best limit for equal-sized cards and no blockers is `w = n`, one card per person.

### The visual

Open the interactive. The left panel draws the board over time: a stacked band showing how many cards are in To do, Doing and Done at every hour. Drag the WIP limit to 12. The Doing band fills the whole height for nine hours. The board looks as busy as a board can look. The right panel shows the burn-up: cards Done against time, with a vertical line at the playtest. At `w = 12` the burn-up is flat at zero until the very end, then jumps.

Now drag the limit down to 4. The left panel looks calmer, with only four cards in Doing at any time. The right panel shows steps at hours 3, 6 and 9, and the playtest line crosses the burn-up at 8 cards. A busy board and a productive board are different pictures, and only the right-hand one tells you what you can play.

Raise the switching overhead slider and watch the unlimited board's finish slide past the playtest line while the `w = 4` steps don't move.

### Cross-game recognition

Little's law shows up anywhere things wait. Rewrite each case as `L = λ × W` and ask which of the three numbers the designer controlled.

**Final Fantasy XIV: A Realm Reborn (launch, August 2013).** The relaunch drew more players than its servers could hold at once, and Square Enix temporarily suspended digital sales of the game while it added capacity. In queue terms, the servers had a fixed throughput and the queue (`L`) was too long. Square Enix could not make each player's session shorter, so it cut the arrival rate. That is a WIP limit applied to customers: stop admitting new work until the system can finish what it has. MMO302 week 9 works through login queues with this law in detail ([MMO302 week 9](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md)).

**Voices in a game's audio mixer.** The number of sounds playing at once equals the rate at which sounds start times how long each one lasts. A sound designer who doubles every footstep's tail length doubles the average number of voices the engine must mix, with no change in how often players step. AU101 week 12 uses exactly this form to budget voices for a raid ([AU101 week 12](../../AU101-audio-for-games/lectures/w12-audio-for-mmos-many-players-one-mix.md)).

**Your bug tracker.** Open bugs `L`, bugs fixed per day `λ`, average days a bug stays open `W`. A team that lets 60 bugs sit open while fixing 10 a day should expect a new bug to wait six days. [Week 10](w10-bug-tracking-and-qa-basics.md) builds a full model of the bug backlog on top of this.

Login queue, mixer, bug list, task board. Four systems, one law. When anything in a game or a studio feels slow, first ask: is the throughput low, or is the pile too big?

### Eyes-open judgment

A WIP limit is a policy, not a law of nature, and it has costs you should choose knowingly.

- **Blocked cards break the simple model.** If the programmer's card waits on an art asset, a strict `w = n` leaves the programmer idle. Most teams set `w = n + 1` so one card can be blocked without idling anyone, and they mark blocked cards in red so the producer sees them at the next check-in.
- **Unequal cards change the numbers, not the direction.** Real cards range from 30 minutes to four hours. Large cards raise cycle time for the same reason high WIP does, which is one more reason to split them.
- **Switching costs differ by discipline.** An artist alternating between two small sprites loses little. A programmer alternating between the save system and the physics loses a lot. Don't use one `c` for everyone when you set limits in a studio.
- **The limit is a lever for conversation.** When Doing is full and someone wants to start a new card, the limit forces the question "whose card can I help finish?" That question, asked at hour 20, is worth more than any formula.
- **Little's law needs a stable system.** If cards arrive faster than the team finishes them for the whole jam, averages keep drifting and `W` has no steady value. The law still tells you something: the pile will grow until you cut scope.

## 3. The definition of done

The table in section 2 counted only Done cards at the playtest. That is only fair if "done" means the same thing on every card. It usually doesn't.

A **definition of done** (DoD) is a short checklist, written by the whole team before work starts, that every card must pass before it moves to Done. The Scrum Guide (November 2020 edition) calls it a formal description of the state the work must be in to meet the product's quality measures, and says that work which doesn't meet it goes back to the backlog rather than counting as finished.

It is different from **acceptance criteria**. Acceptance criteria are specific to one card: "dash moves 3 tiles." The definition of done applies to every card: "merged to main, runs from the title screen, checked by someone else." A card is done when both are true.

### What "done" hides when nobody defines it

Here is a board at hour 40 of a jam. It shows 18 of 20 cards in Done, 90 percent. The team relaxes. Then the producer applies the team's DoD to the 18 cards and finds 6 that fail: two never got merged, three work only when started from their test scene, and one leaves a debug overlay on screen. Each needs about 1.5 person-hours to fix.

| | Believed remaining | Actual remaining |
|---|---|---|
| Two cards in To do, 3 h each | 6 person-hours | 6 person-hours |
| Six "done" cards that fail the DoD | 0 | 6 × 1.5 = 9 person-hours |
| Total | **6 person-hours** | **15 person-hours** |

The team believed it had 6 person-hours left. It had 15, two and a half times as much. With four people and 8 hours to go, 6 person-hours looked like an easy afternoon. 15 means the two cards in To do must be cut, now, before anyone starts them. This is the ninety-ninety rule in miniature: the missing work was always there, but the board hid it inside cards marked Done.

The DoD doesn't reduce the work. It moves the work onto the board, where the producer can see it at hour 20 instead of hour 46.

### A jam definition of done

Keep it short enough to check in under two minutes per card. A good starting point for the jam:

1. Every acceptance sentence on the card is true in a build, checked by someone other than the owner.
2. The change is merged to main, and main still builds with no new errors in the console.
3. The feature works when the game is started from the title screen, not only from a test scene.
4. New assets are in the repository, binary ones tracked by LFS (week 3), with their source or licence noted.
5. Nothing a player could see is debug-only: no test keys, no placeholder text, no overlay.

Every line is there because a real jam team lost points without it. Item 3 is the one most teams skip, and it's the one that breaks the most submissions: a feature that only works from the editor's "play this scene" button is not in the game.

### Levels of done

Studios often have more than one definition, stacked:

- **Task done**: the list above.
- **Feature done**: all of a feature's cards are done, and a playtester who hasn't seen it can use it without help (GD101 week 7).
- **Release done**: the whole build passes the release checklist. Week 13 builds that checklist and puts numbers on it.

For the jam, you need the first one only. Write it on the board itself, at the top of the Done column, so nobody has to remember it.

## 4. Running the board during the jam

A board that nobody updates is worse than no board, because people trust it. Three habits keep it honest.

**Update at the check-in, not at the end.** Week 5 turned the stand-up into a jam check-in at each checkpoint and after every sleep. Hold it at the board: each person moves their own cards and says what is blocking them. The producer reads out the Doing column and asks "who is helping finish these?" before anyone pulls a new card.

**Keep a remaining estimate on every open card.** Every six hours (hours 6, 12, 18 and so on to 48), the owner writes how many person-hours they think are left on the card. Not how many they've spent. How many are left. This number is the one you'll analyse after the jam, so write it honestly even when it's embarrassing. A card that was estimated at 2 hours, has taken 3, and still needs 2 is exactly the data week 9 needs. Lab 8 gives you the log format. Each card gets one row per check-in with the hours spent so far and the hours you think remain.

**Watch the columns, not the cards.** The board's shape tells you where the team is stuck:

| Board shape | What it means | What to do |
|---|---|---|
| Doing is overfull | Too much started; cycle time rising | Stop starting. Swarm the oldest card. |
| Review is piling up | Nobody is checking others' work | Next free person reviews before pulling a card |
| To do is empty but Done isn't growing | Scope ran out of cards but not of work: hidden work | Apply the DoD to Done; the missing work is there |
| Done grows, To do never shrinks | Cards are being added as fast as they are finished | Freeze scope; next week's lecture shows when |

A physical board of sticky notes on a wall works well for a jam where everyone is in one room. A shared spreadsheet or a tracker such as GitHub Projects works when people are spread out. Pick one and use only one. Two boards always disagree, and then neither is true.

## In-class activity (25 minutes)

Work in your jam teams from week 1.

1. **Split (10 min).** Take the one-pager your team wrote in week 4. Pick its core feature and split it into cards using the three tests from section 1. Each card needs an owner, an estimate of four person-hours or less, a tier and at least one acceptance sentence.
2. **Define done (5 min).** Write your team's definition of done. Start from the five items in section 3, delete any that don't apply to your engine, and add one that comes from something that went wrong in your week 2 or week 3 lab.
3. **Set the limit (5 min).** Choose a WIP limit. Use the interactive with your team size and your average card size to show the rest of the room what your burn-up looks like at your limit and at no limit, with a playtest at hour 8.
4. **Swap (5 min).** Give your cards to another team. They pick the two cards whose acceptance criteria they couldn't check without asking you. Rewrite those two.

Expected output: a card list of 8 to 15 cards, a five-line DoD, a WIP limit with one sentence of justification, and two rewritten acceptance sentences.

## Common misconceptions

- **"A full Doing column means the team is productive."** It means the team is busy. Throughput is set by people and speed. Extra WIP only lengthens cycle time, and at a deadline it turns finished features into unfinished ones.
- **"A WIP limit makes the team slower."** For equal cards with no blockers, it doesn't change the total time at all, and it makes features playable earlier. It slows the team only when set below the number of people, or when cards are blocked and no slack is allowed.
- **"Acceptance criteria and the definition of done are the same thing."** Acceptance criteria belong to one card. The DoD applies to every card. A card is done only when both hold.
- **"90 percent done means 10 percent left."** Percent complete counts cards, not work. Unless every card in Done passes the same checklist, the remaining work can be several times what the board shows.

## Check yourself

1. A team's board averages 10 cards in Doing, and the team finishes 2.5 cards per hour. What is the average cycle time? The producer halves the WIP to 5 without changing the team. What happens to throughput and cycle time?
2. Three people, nine cards of 2 person-hours each, switching overhead `c = 0.1`, playtest at hour 5. How many cards are done at the playtest with `w = 3`? With `w = 9`?
3. A card says "Improve the menu". Rewrite it as one or more cards that pass the three splitting tests.
4. At hour 30 a board shows 24 of 30 cards Done. Applying the DoD, you find that one third of the Done cards need 1 more person-hour each. The six cards in To do average 2.5 person-hours. What fraction of the real remaining work was hidden?
5. Your artist says: "I work on six sprites at once, because I get bored." Use the model to say what that does to the playtest, and what limit you'd propose for art cards.

<details>
<summary>Answers</summary>

1. `W = L / λ = 10 / 2.5 = 4` hours. Halving WIP leaves throughput at 2.5 cards per hour, because the same people work at the same speed, so cycle time halves to 2 hours. (If switching costs were significant, throughput would even rise slightly.)
2. With `w = 3`, `k = 1`, so each batch takes 2 hours: three cards at hour 2, three at hour 4, three at hour 6. At hour 5, **6 cards** are done. With `w = 9`, `k = 3`, so `d = 2 × 3 × 1.2 = 7.2` hours. All nine finish at 7.2 hours, and **0 cards** are done at the playtest.
3. One possible split: "Title screen has Start and Quit buttons that work with keyboard and controller" (acceptance: Enter or A starts the game; Esc or B on Quit closes it). "Menu shows the game's title in the chosen font at 1080p and 720p without clipping." "Menu plays the title music, looping, at −12 dB relative to gameplay music." Each is under four hours, visible in a build and checkable by someone else.
4. Believed remaining: `6 × 2.5 = 15` person-hours. Hidden: one third of 24 is 8 cards, at 1 hour each, 8 person-hours. Real remaining: `15 + 8 = 23`. Hidden fraction `8 / 23 ≈ 35%`.
5. Six sprites at once means `k = 6` for that person. Even with a small `c`, none of the six is done until all six are, so the playtest sees no new art from the artist at all. Propose a limit of 1 or 2 art cards per artist; with `c` small for art, 2 costs little and keeps variety.

</details>

## Lab / assignment hook

[Lab 07, a board that tells the truth](../labs/lab07.md). Your team builds its jam board, card list and definition of done, sets a WIP limit, and runs a checker script that rejects oversized cards, missing acceptance criteria and a thin DoD. The script also writes the first rows of the jam log you will fill during the jam (lab 08) and analyse afterward (lab 09).

## Sources

- Wikipedia, "Duke Nukem Forever" (read September 2026). Announced by 3D Realms on 27 April 1997 with a Christmas 1998 target; released 14 June 2011 in North America (10 June in Europe and Australia); George Broussard's repeated answer that it would ship "when it's done."
- Wikipedia, "Ninety–ninety rule" (read September 2026). Attributed to Tom Cargill of Bell Labs; popularized in Jon Bentley's "Programming Pearls" column, *Communications of the ACM*, September 1985.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research* 9(3), 383-387.
- Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition, section "Commitment: Definition of Done." https://scrumguides.org/scrum-guide.html
- Wikipedia, "Final Fantasy XIV: A Realm Reborn" (read September 2026). August 2013 relaunch; servers unable to hold concurrent demand; temporary suspension of digital sales; new servers promised; a week of free play time as compensation.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Chapters on Kanban and on Scrum's definition of done.

## Interactive spec: examples/w07-wip-limit.html

**The one insight.** A board with more cards in progress looks busier but finishes later. With the same people, raising the WIP limit leaves throughput unchanged (or lowers it, with switching costs) and pushes every finish time later, so at a fixed playtest time the unlimited board has nothing done.

**Layout.** Two linked views sharing one time axis (hours), side by side on desktop, stacked on mobile.

1. **Left view, the board over time.** A stacked area chart from `t = 0` to `t_max = max(makespan, deadline) + 1`. Three bands from bottom to top: Done, Doing, To do. They always sum to `N`. Label the bands in text, not only by colour.
2. **Right view, the burn-up.** A step line of Done cards against time, with a vertical dashed line at the playtest (`deadline`) and a label "Done at playtest: X of N". Draw a second, faint step line for the `w = n` case as a reference, labelled "one card per person".

**Controls** (native inputs, keyboard operable, values shown).

- People `n`: 1 to 8, default 4.
- Cards `N`: 1 to 30, default 12.
- Card size `s` (person-hours): 0.5 to 8, step 0.5, default 3.
- WIP limit `w`: 1 to `N`, default 12. A "No limit" button sets `w = N`.
- Switching overhead `c`: 0 to 0.5, step 0.05, default 0.
- Playtest at hour `deadline`: 1 to 24, step 0.5, default 8.

**Formulas.** Cards run in batches. While cards remain:

```
b = min(w, cards left)             cards in this batch
k = max(1, b / n)                  cards per person
d = s × k × (1 + c × (k − 1))      batch duration; all b cards finish together at t + d
t = t + d
```

Makespan is the final `t`. Throughput `λ = N / makespan`. Average cycle time `W` = mean of each card's batch duration. Average WIP `L` = (sum over batches of `b × d`) / makespan. Show `L`, `λ`, `W` and the check `L / λ` beside the charts, to 2 decimals, so students see Little's law hold.

**Readout table** under the charts: for `w = 1, 2, n, 1.5n (rounded down), 2n, N` at the current settings, columns finish times, done at playtest, `W`, makespan.

**Test values** (must match lecture section 2; `n = 4`, `N = 12`, `s = 3`, `deadline = 8`).

- `c = 0`: `w = 2` finishes at 3, 6, 9, 12, 15, 18, done at 8 = 4, `W` = 3. `w = 4` finishes at 3, 6, 9, done = 8, `W` = 3. `w = 6` finishes at 4.5, 9, done = 6, `W` = 4.5. `w = 8` finishes at 6, 9, done = 8, `W` = 5, `L` = 6.67. `w = 12` finishes at 9, done = 0, `W` = 9. Throughput 1.33 per hour for every `w ≥ 4`; 0.67 for `w = 2`.
- `c = 0.1`: `w = 6` finishes at 4.725, 9.45 (done = 6); `w = 8` at 6.6, 9.6 (done = 8, `W` = 5.4); `w = 12` at 10.8 (done = 0, throughput 1.11).
- Check-yourself 2: `n = 3`, `N = 9`, `s = 2`, `c = 0.1`, `deadline = 5`: `w = 3` gives done = 6; `w = 9` gives all nine at 7.2, done = 0.

**Behaviour.** Everything redraws on input. No animation is needed; if a "play" button animates time, it respects `prefers-reduced-motion` by jumping to the end. Colours from `templates/interactive-tokens.css`. Cards are plain rectangles; no tool logos.
