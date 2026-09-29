# PR101 · Week 08 — The 48-Hour Game Jam

**Why this matters:** This week you make a game, start to finish, in 48 hours. Everything from weeks 1 to 7 gets tested at once, under a clock that doesn't move. The teams that do well are rarely the ones with the best idea. They are the ones who always have a working build and who know, before they are tired, when to stop adding things.

**You will be able to:**
- Plan a 48-hour jam schedule with checkpoints, a feature freeze, a content lock and a submission buffer, and justify each time.
- Compute the expected value of one more late change, with and without a tagged last-good build, and find the point where adding features stops paying.
- Keep a jam log that records spent and remaining hours for every task at every checkpoint, in the format week 9 analyses.
- Ship a jam game as a team: a tagged build that runs on a machine it wasn't made on.

**Before class:** Reread your team's week 4 scope sheet and week 7 board. Browse the Global Game Jam games archive (globalgamejam.org) and play two games from any year for five minutes each; note how long each takes to reach something you can do. Keith, *Agile Game Development* (2nd ed., 2020), the section on continuous integration (reread from week 2).

**Prerequisites from earlier courses:** [PR101 week 1, roles](w01-roles-on-a-game-team.md) (your team and its capacity), [week 2, Git](w02-git-fundamentals-and-branching.md) (short branches and tags), [week 3, asset workflows](w03-asset-workflows-and-large-files-lfs.md), [week 4, scope and cut lists](w04-scope-mvp-vertical-slice-cut-lists.md) (the MVP, the cut line and the cut triggers at hours 12, 24, 36 and 42), [week 5, Scrum in a jam](w05-agile-and-scrum-adapted-for-games.md) (two-hour build cycles and "the build must always run"), and [week 7, task tracking](w07-task-tracking-and-definitions-of-done.md) (the board, WIP limits and the definition of done). [Week 6, estimation](w06-estimation-and-why-it-fails.md). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the `(1 − q)^k` in section 2).

**Interactive:** [examples/w08-feature-freeze.html](../examples/w08-feature-freeze.html). Keep it open during section 2.

---

## 1. What a jam is, and how ours runs

A **game jam** is a short event, usually 24 to 72 hours, in which people make a game from scratch around a theme announced at the start. The two best-known public jams set the formats most others copy:

- The **Global Game Jam** runs once a year, in January, at hundreds of sites at once. Each site runs for 48 hours, from 5 p.m. on the start day to 5 p.m. two days later. Week 1 used its participant numbers to show why jam teams stay small.
- **Ludum Dare**, first held in April 2002, has two tracks. The **Compo** is solo, with 48 hours and every asset made during the event. The **Jam**, added in 2010, allows teams and runs for 72 hours.

Jams matter beyond the weekend. Week 4 met *Surgeon Simulator* and *Baba Is You*, both jam games that became commercial releases. Here's a third. The original *Celeste* was made by Maddy Thorson and Noel Berry in three days in August 2015, for the PICO-8 fantasy console. The full *Celeste* shipped in January 2018. What the jam version proved was the core feel of the climbing and the dash. It did not have to prove anything else.

### Our jam

Our jam runs for 48 hours in the lab, starting at 17:00 on the first day of jam week and ending at 17:00 two days later, the Global Game Jam format. The rules:

1. **Teams** are the ones you formed in week 1. No changes after the theme is announced.
2. **The theme** is announced at hour 0. Your game must connect to it in a way a stranger can see in the first minute.
3. **Assets** are made during the jam, or taken from a source whose licence allows it and credited in the game and on the submission page. Engines, frameworks and code libraries are allowed. Code or art written before the jam, other than libraries, is not.
4. **The build** must run on a lab machine, or in a web browser, without the engine installed. A game that only runs from the editor has not been submitted.
5. **Submission** is a zipped build, the Git tag it was built from (`v0.1.0`, the version week 13 gives the jam build), your jam log (section 3), and photos or screenshots of your board at hours 12, 24, 36 and 42.

### The schedule

Every checkpoint below comes from an earlier week. The jam is where they meet.

| Hour | What happens | From |
|---|---|---|
| 0 | Theme announced | |
| 0-2 | One-pager with the MVP sentence; task list with estimates, tiers and the cut line; cards on the board; first jam log rows | Weeks 4, 6, 7 |
| 2-12 | Build the MVP. A playable build every two working hours. Log remaining hours at 6 and 12. | Weeks 4, 5 |
| 12 | **Cut trigger:** if the MVP loop isn't playable, all slice work stops | Week 4 |
| 12-24 | Slice work. Sleep in shifts: every person gets a block of at least six hours before hour 24. | Week 12 (crunch) |
| 24 | **Cut trigger:** re-estimate everything left and redraw the cut line | Week 4 |
| 36 | **Feature freeze:** no new tasks enter; tasks in Doing may finish | Week 4, and section 2 below |
| 42 | **Content lock:** only bug fixes and the build | Week 4 |
| 44 | Tag `v0.1.0-rc.1`, build from a fresh clone, play it on a machine that isn't the builder's | Weeks 2, 13 |
| 46 | Submit | |
| 48 | Hard close. Anything not submitted is not submitted. | |

Two hours between the release candidate and the upload, and two more between the upload and the close, may look generous. They aren't. Exporting, zipping, uploading and testing a download take longer when you're tired, and one missing folder in the zip means rebuilding. The buffer at the end is the cheapest insurance in the whole schedule.

Why is the freeze at hour 36, twelve hours before the end? Week 4 set it as a rule. Section 2 shows the reasoning behind it, and when you might move it.

## 2. Worked example: the freeze point

### The hook

Minecraft: Java Edition has been updated by Mojang for well over a decade. Since version 1.16 in 2020, Mojang has published **release candidates** before its updates: builds intended to be the last before release unless a game-breaking bug turns up. The Minecraft Wiki notes that the full release is often identical to the last release candidate apart from the version name and a couple of internal version numbers.

Think about what that means. For the last days before a release, a professional team that knows its game deeply makes no changes to it at all. Meanwhile a jam team with 48 hours of experience with its own code adds a new enemy at hour 47. One of them is behaving rationally. The model below says which, and it also says the answer depends on a single tool that the jam team probably has but isn't using.

### The model

It's late in the jam. Your build works and has `F` features that a player can use. You have a list of `k` more small changes you could make: an extra enemy, a sound, a tweak to the jump. Each change is worth one feature if it works. Each change also has a chance `q` of leaving the game broken at submission time (it crashes, a level won't load, the build fails to export), because a change you make late has little time left for anyone to notice and fix what it broke.

- `F` is the number of working features now.
- `k` is the number of late changes you make.
- `q` is the chance that any one late change leaves the submitted build broken.

A broken submission scores nothing, however many features it has. If the changes break things independently, the chance none of them breaks the build is `(1 − q)^k`. That's the complement rule from MA102 week 3, used the other way round. So:

```
P(submitted build works) = (1 − q)^k
Expected features shipped = (F + k) × (1 − q)^k
```

Should you make one more change? It is worth it only if the expected value goes up. Compare `k` and `k + 1` changes, and the rule simplifies to one line:

```
make one more change only if   F + k < (1 − q) / q
```

The right-hand side is a threshold set by `q` alone. When the number of features at risk (`F + k`) passes it, every further change *lowers* what you can expect to ship. The more you've built, the more a single late mistake can destroy, so the less a new feature is worth.

Now add a **safety net**. Before each late change, the working build is tagged in Git (`git tag`, week 2). After each change, someone plays the build. If the change broke it, you revert to the tag. A broken change now costs only itself:

```
with a tagged last-good build:
P(submitted build works) = 1
Expected features shipped = F + k × (1 − q)
```

Every change now adds `1 − q` expected features. None of them can cost you the game.

### Numbers you can check

Take `F = 8` working features and `q = 0.1`: one late change in ten leaves the build broken.

| Late changes `k` | Expected features, no net `(8 + k) × 0.9^k` | P(submitted build broken) `1 − 0.9^k` | Expected features, with net `8 + 0.9k` |
|---|---|---|---|
| 0 | 8.00 | 0% | 8.0 |
| 1 | 8.10 | 10.0% | 8.9 |
| 2 | 8.10 | 19.0% | 9.8 |
| 3 | 8.02 | 27.1% | 10.7 |
| 4 | 7.87 | 34.4% | 11.6 |
| 6 | 7.44 | 46.9% | 13.4 |
| 10 | 6.28 | 65.1% | 17.0 |

Check a row by hand. For `k = 4`: `0.9^4 = 0.6561`, and `12 × 0.6561 = 7.87`. The chance of a broken build is `1 − 0.6561 = 34.4%`.

The threshold is `(1 − 0.1) / 0.1 = 9`. With `F = 8`, the first change passes the test (`8 + 0 < 9`), the second is break-even (`8 + 1 = 9`), and every change after that loses. Look at what the "winning" changes buy: two changes raise expected features from 8.0 to 8.1 and raise the chance of shipping nothing from 0% to 19%. **In expected value, late changes without a net are almost free. In risk, they are ruinous.** Nearly one team in five that makes those two changes ships a broken game, to gain a tenth of a feature on average.

The last column shows why the net matters so much. With a tagged last-good build, ten late changes are worth an expected 17 features, and the chance of shipping a broken game stays at zero.

### How `q` changes over the jam

`q` is not a constant. It depends mostly on how much time is left to notice and fix a break. At hour 10, a broken build gets fixed long before anyone submits, so a change's `q` is close to zero. At hour 47 there is no time to fix anything. Here are plausible values for one small change on a jam team (the numbers are assumptions for illustration; your own jam log can give you better ones: count the changes that broke the build in each part of the jam):

| Time left | Assumed `q` | Threshold `(1 − q) / q` | Meaning for a game with about 8 features |
|---|---|---|---|
| 12 hours | 0.02 | 49 | Keep adding |
| 6 hours | 0.05 | 19 | Keep adding, carefully |
| 3 hours | 0.10 | 9 | At the edge: one more at most |
| 1 hour | 0.25 | 3 | Every change loses |

The threshold falls as the deadline approaches, and it crosses the size of a typical jam game somewhere between 6 and 3 hours before the end. Put the freeze a few hours before that crossing, to leave time to build and upload, and you land close to week 4's hours 36 and 42. Week 4's rule and this model agree. The model also tells you when to break the rule: with a tagged build and someone playing after every merge, late changes stay safe, and you can keep making small ones until content lock.

### The visual

Open the interactive. It has two linked panels, both plotted against the number of late changes `k`. The left panel shows expected features shipped, with and without a net. The right panel shows the chance that the submitted build is broken.

With the net switched off and `q = 0.1`, the left curve is almost flat for the first three changes. It looks harmless. The right curve climbs steeply from the first change. That contrast is the lesson: a flat expected-value curve hides a fast-rising chance of losing everything. Drag `F` up to 15 and the left curve starts falling from the very first change, because more working features means more to lose. Switch the net on and the right panel drops to zero while the left panel turns into a rising straight line.

The "hours left" presets set `q` from the table above, so you can watch the threshold marker slide left as the deadline approaches.

### Cross-game recognition

The same trade appears wherever a build ships on a date.

**Minecraft: Java Edition release candidates (since 1.16, 2020).** A release candidate is a freeze made formal. Mojang's `F` is enormous, so its threshold is passed by any change that isn't fixing a game-breaking bug. The rule "only game-breaking fixes after RC" is exactly "stop when `F + k` is above `(1 − q)/q`," for a game where `F` is in the thousands.

**Week 13's release candidates.** Your final project will tag `v1.0.0-rc.1` five days before release and never patch an RC by hand. If a fix is needed, you make `rc.2`. That is the safety net from this model, run with more time: every candidate is a tagged, known-good build you can fall back to.

**Week 2's tags, and any team using version control.** Week 2 asked you to tag milestones so you can always rebuild what was submitted. In this model, a tag is the difference between the two formulas. It converts a late mistake from "lose the game" to "lose one feature." This is why the most useful thing a jam team can do at hour 30 is often not a feature but a one-line habit: tag every build that works.

Three contexts, one rule: the more you have that works, the more carefully you should change it, unless you can always get back to what worked.

### Eyes-open judgment

- **A freeze trades upside for safety.** A team that freezes at hour 36 gives up the chance that a brilliant idea at hour 40 makes the game. Sometimes it would have. The model says that on average, and especially in the bad cases, the freeze wins. Decide whether your team would rather have a small chance of a great game or a high chance of a finished one. For a graded jam, choose finished.
- **`q` is not the same for every change.** Changing a sound file almost never breaks a build. Changing the scene loader often does. A team that freezes code at hour 36 but lets the audio designer swap sounds until hour 42 is using the model correctly.
- **Independence is optimistic.** Late changes pile onto each other. The third change may break the second. Real risk grows faster than `(1 − q)^k`, which makes the freeze more valuable, not less.
- **The net only works if someone plays the build.** A tag you never test is a tag of an unknown build. The rule is: merge, build, play for two minutes, tag. Week 13 turns "someone plays it" into a checklist with measured catch rates.
- **Don't freeze too early either.** A frozen MVP at hour 20 with nothing else is a finished game nobody enjoys. The cut triggers at hours 12 and 24 exist to make sure the freeze arrives when there's something worth protecting.

## 3. The jam log: data for next week

Next week you'll analyse how good your team's estimates were. That needs data that nobody can reconstruct afterward from memory, so you log it during the jam.

The **jam log** is one CSV file per team. It has one row for every open task at every six-hour checkpoint (hours 0, 6, 12 and so on to 48):

| Column | Meaning |
|---|---|
| `team` | Your team code |
| `task` | The card's ID from the board |
| `hour` | The checkpoint: 0, 6, 12, ..., 48 |
| `spent` | Person-hours spent on this task so far, in total, to the nearest half hour |
| `remaining_est` | Person-hours you believe are still needed to reach Done, from now |
| `status` | `open`, `done` or `cut` |

The rules for filling it in:

- A task's first row is written when the card is created, with `spent = 0` and `remaining_est` equal to its estimate.
- At every checkpoint, each owner gives the producer two numbers for each open card: hours spent so far and hours they think remain. It takes two minutes per person.
- When a card meets the definition of done, its next row has `status = done`, `remaining_est = 0`, and `spent` equal to the actual total person-hours.
- When a card is cut, its next row has `status = cut`.
- No row after `done` or `cut`.

Two honesty rules. First, **the log is graded on completeness, never on accuracy**. A task estimated at 2 hours that took 7 is valuable data, not a mark against you. Second, **"0 hours left" means Done**. If a card isn't done, its remaining estimate is not zero, however close it feels. Week 7's ninety-ninety rule is exactly the gap between "0 left" and done, and next week you'll count how often your team fell into it.

Lab 8 gives you a checker script that rejects a malformed log. Run it at hour 24 and again before submission, so you don't find out at hour 47 that the file is broken.

## 4. Getting through 48 hours

A few rules that come from the teams who didn't finish.

**Build the whole loop first.** Title screen, play, end state, back to the title. Grey boxes, no sound. Week 4's MVP is a loop, not a feature. A beautiful character who can't win or lose is not a game.

**Integrate constantly.** Week 2's overlap model says merge conflicts grow with the square of the time between merges. In a jam, merge each card as soon as it passes review, which with four-hour cards means several merges per person per day.

**One person owns the build.** Pick them at hour 0. From hour 36 on, nothing goes into main without the build owner knowing. That person exports and tests the release candidate at hour 44.

**Sleep is a production tool.** Everyone sleeps at least six hours in each night of the jam, in shifts, so someone is always awake to keep the build running. [Week 12](w12-crunch-causes-costs-alternatives.md) covers what long hours do to a team's output. For now, the rule of thumb is that the work you do at hour 30 without sleep is the work you fix at hour 40.

**The board decides, not the loudest voice.** When someone has a new idea at hour 20, it goes through week 4's one-in-one-out rule: it gets an estimate and a tier, and something at least as large leaves the plan. When Doing is full, week 7's WIP limit says help finish a card before starting one.

**Credit every asset.** A credits screen listing every person and every third-party asset, with its licence, is part of the definition of done for the final build.

## In-class activity (25 minutes)

Hold this in the lecture slot before the jam starts, in your jam teams.

1. **Your `q` (10 min).** Look at your week 2 and week 3 labs and your week 5 sprint. How often did a merge leave main broken? Turn that into a rough `q` for a change made with 12, 6, 3 and 1 hours left. Write the four numbers down with one sentence of reasoning each.
2. **Your freeze (5 min).** Guess how many features your MVP plus slice will have (`F`). Using your `q` values, find where `(1 − q)/q` drops below `F`. Is that earlier or later than hour 36? Decide your team's freeze and content-lock hours, and write them on the board.
3. **Your net (5 min).** Write the exact commands your build owner will run to tag a working build and to go back to it. Try them now on your team repository.
4. **Your log (5 min).** Create the jam log file from your week 7 cards with lab 7's script. Agree who collects the numbers at each checkpoint.

Expected output: four `q` values, a freeze hour and a content-lock hour with the reasoning, tested tag and revert commands, and a seeded jam log.

## Common misconceptions

- **"A feature freeze is for big studios with QA departments."** The model says the opposite. A small team has fewer people to notice a break, so its `q` near the deadline is higher, and its threshold is lower.
- **"One more feature can't hurt, it's a small change."** The size of the change affects `q`. The size of what it can break is `F`, the whole game. Late, the second number dominates.
- **"We'll just fix it if it breaks."** At hour 47 you may not know it's broken. A build that crashes on the judge's machine and not yours breaks after you've stopped looking.
- **"Tags are for releases."** A tag is a free bookmark on a known-good build. During a jam, tag every build that works. It is the single change that turns late risk from losing the game into losing one feature.

## Check yourself

1. Your game has 12 working features and it's 3 hours before the deadline, where you estimate `q = 0.1`. Without a net, should you make one more change? What is the expected value of the build with 0 and with 1 more change?
2. At hour 30 your team has 6 features. You estimate `q = 0.05` for changes made now. How many features can the game have before a change made now stops paying, without a net?
3. With a net, a team makes 5 late changes at `q = 0.2`. How many features do they expect to add? What is the chance they ship a broken build?
4. A teammate argues: "The expected value only goes from 8 to 8.1, so the late change is harmless." Using the table in section 2, write two sentences explaining what the expected value hides.
5. Why does the jam schedule put the release candidate two hours before submission, and the submission two hours before the close? Name two things that go wrong in each gap.

<details>
<summary>Answers</summary>

1. The threshold is `(1 − 0.1)/0.1 = 9`. `F + k = 12 + 0 = 12`, which is above 9, so the change lowers expected value. With 0 changes: 12. With 1: `13 × 0.9 = 11.7`. Don't make it, unless you have a tagged build to fall back to.
2. Threshold `(1 − 0.05)/0.05 = 19`. A change pays while `F + k < 19`, so up to about 19 features at risk. At 6 features you are far below; keep building. (By hour 42, with a higher `q`, the answer changes.)
3. Expected features added: `5 × (1 − 0.2) = 4`. Chance of a broken build: 0, because every broken change is reverted to the tag. (That assumes someone plays the build after each change. If nobody does, the net does nothing.)
4. The expected value averages over good and bad outcomes. Two changes at `q = 0.1` give 8.1 expected features but a 19% chance of shipping a broken build worth nothing, so the average hides a nearly one-in-five chance of losing the whole game for a tenth of a feature.
5. RC to submission: the export is missing a folder or a file; the build runs only on the builder's machine (a path or an installed runtime it depends on); a debug overlay is still on. Submission to close: the upload fails or is slow; the zip is the wrong build; the page is missing the credits or the tag. Two hours each is enough to redo one export and one upload.

</details>

## Lab / assignment hook

[Lab 08, the jam](../labs/lab08.md). The lab is the jam itself. You submit the tagged build, the jam log (checked with the lab's script), board photos at the four checkpoints, the one-pager and a one-paragraph freeze record: when you froze, what you cut, and any change you made after the freeze and why. The game itself is graded as the jam game assessment (30% of the course); the lab grades the production evidence. The log feeds [lab 09](../labs/lab09.md).

## Sources

- Wikipedia, "Global Game Jam" (read September 2026). Annual January event; each site runs 48 hours from 5:00 p.m. on the start date to 5:00 p.m. two days later.
- Wikipedia, "Ludum Dare" (read September 2026). First held April 2002; the 48-hour solo Compo; the 72-hour team Jam introduced at the 18th event, August 2010.
- Wikipedia, "Celeste (video game)" (read September 2026). Original version made by Maddy Thorson and Noel Berry in three days in August 2015 for PICO-8; full game released 25 January 2018.
- Minecraft Wiki, "Release candidate" (Java Edition, read September 2026). Definition as the intended last build before a release unless a game-breaking bug is found; first used for 1.0.0 in 2011, then not again until 1.16 in 2020; the full release often identical to the last release candidate except the version name, protocol version and data version. https://minecraft.wiki/w/Release_candidate
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Section on continuous integration.

## Interactive spec: examples/w08-feature-freeze.html

**The one insight.** Without a tagged last-good build, late changes barely move the expected number of features but rapidly raise the chance of shipping a broken game. With a net, every change adds value and the risk stays at zero.

**Layout.** Two linked charts with the same x-axis, `k` = late changes from 0 to 15, side by side on desktop, stacked on mobile.

1. **Left, expected features shipped.** Two lines: "no net" `(F + k)(1 − q)^k` and "with net" `F + k(1 − q)`. Mark the no-net maximum with a dot and label its `k`. Draw a vertical marker at the break-even point where `F + k = (1 − q)/q` (if it is inside the axis range), labelled "threshold".
2. **Right, chance the submitted build is broken.** "No net" `1 − (1 − q)^k` as a line from 0% to 100%, and "with net" as a flat line at 0%. Hovering or focusing a `k` value highlights the same `k` on both charts and shows both values in a tooltip.

**Controls** (native inputs, keyboard operable, values shown).

- Working features `F`: 0 to 30, default 8.
- Break chance per change `q`: 0.01 to 0.5, step 0.01, default 0.10.
- Hours-left presets (buttons that set `q`): 12 h = 0.02, 6 h = 0.05, 3 h = 0.10, 1 h = 0.25.
- Safety net: checkbox, default off. When off, the with-net lines are faint; when on, the no-net lines are faint.

**Formulas.**

```
no net:   E(k) = (F + k) × (1 − q)^k        P_broken(k) = 1 − (1 − q)^k
net:      E(k) = F + k × (1 − q)            P_broken(k) = 0
threshold: make change k+1 only if F + k < (1 − q) / q
```

**Readout table** below the charts for `k = 0, 1, 2, 3, 4, 6, 10`: E no net (2 decimals), P broken (1 decimal %), E with net (1 decimal). Show the threshold `(1 − q)/q` to 2 decimals.

**Test values** (must match lecture section 2).

- `F = 8`, `q = 0.10`: E no net 8.00, 8.10, 8.10, 8.02, 7.87, 7.44, 6.28; P broken 0.0%, 10.0%, 19.0%, 27.1%, 34.4%, 46.9%, 65.1%; E with net 8.0, 8.9, 9.8, 10.7, 11.6, 13.4, 17.0. Threshold 9.00.
- `F = 12`, `q = 0.10`: E(0) = 12, E(1) = 11.70.
- `F = 10`, `q = 0.20`: E no net 10.00, 8.80, 7.68, 6.66, 5.73; threshold 4.00.
- Threshold for presets: 49.00, 19.00, 9.00, 3.00.

**Behaviour.** Instant updates, no animation needed. Colours from `templates/interactive-tokens.css`. No game art; features can be drawn as plain counters.
