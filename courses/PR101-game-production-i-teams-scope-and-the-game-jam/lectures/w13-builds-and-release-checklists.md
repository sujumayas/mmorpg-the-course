# PR101 · Week 13 — Builds and Release Checklists

**Why this matters:** In two weeks your team uploads its final game, and the graders play the build you upload, not the project on your laptop. Teams rarely lose marks on that day because the game is bad. They lose them because the upload is missing a folder, still shows the debug overlay, or crashes on a machine that isn't the one it was made on. A release checklist is the cheapest tool you will ever use against that, and this week shows you with numbers why it works.

**You will be able to:**
- Compute the chance that a release ships clean from the number of things that can go wrong, their per-item risk and how well your checks catch them.
- Explain with the model why checking every item loosely can beat checking half the items carefully, and decide which checks to automate.
- Produce a reproducible Godot release build from a clean checkout, with a version number that follows Semantic Versioning and matches the changelog.
- Write and run a release checklist for your final game, with an owner and a pass condition for every line.

**Before class:** Godot Engine documentation (stable, 4.x), "Exporting projects", the sections "Export templates", "Configuration files" and "Exporting from the command line" (about 15 minutes). Semantic Versioning 2.0.0 at semver.org, the summary and rules 1 to 11 (10 minutes). itch.io, "butler" documentation, the page "Pushing builds" (5 minutes). Google, *Site Reliability Engineering* (2016), chapter 8, "Release Engineering", the section on hermetic builds (10 minutes).

**Prerequisites from earlier courses:** [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (the Godot project you will export). [CS101 week 12, debugging](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md) (the logging you must switch off or tame for release). [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) and [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the product of probabilities used in section 2). From this course, [week 2, Git fundamentals and branching](w02-git-fundamentals-and-branching.md) (commits and tags), [week 7, task tracking and definitions of done](w07-task-tracking-and-definitions-of-done.md), and [week 10, bug tracking and QA basics](w10-bug-tracking-and-qa-basics.md) (smoke tests and severity). This lecture assumes your project is in Git and your team has a definition of done.

**Interactive:** [w13-release-risk.html](../examples/w13-release-risk.html). Keep it open during section 2.

---

## 1. What a build is, and why "it works on my machine" is not a build

Your project folder is not your game. It is the source for your game: scenes, scripts, imported assets, editor settings, and a pile of cache files the editor made for its own use. A **build** is what you get when a tool turns that source into something a player can run without the editor. In Godot that step is called **exporting**. You pick an **export preset** (a named set of options for one platform, such as "Windows Desktop" or "Web"), and Godot combines your project data with an **export template**, a prebuilt copy of the engine runtime for that platform. The Godot documentation is blunt about the dependency: without the templates installed, the export menu refuses to export for that platform.

Three facts about builds cause most first-release accidents.

**A build depends on more than your code.** The same commit can produce different builds depending on the engine version, the template version, the export preset and any files that happen to sit in your folder but not in Git. When a teammate says "it works for me", they usually mean their editor, with their cache and their local files, runs it. That is a different claim from "the build works".

**Debug and release builds differ.** Godot can export a debug build (`--export-debug`) or a release build (`--export-release`). Debug builds keep extra checks and error output that help you during development. Your own code often has debug switches too: an FPS counter, a god mode key, a "skip to level 5" shortcut, verbose logging. Players should get none of these, and graders certainly shouldn't find the god mode key.

**Some settings are secret and some are not.** Godot stores export settings in two files. `export_presets.cfg` holds most of the configuration and the documentation says it can be committed to version control. `.godot/export_credentials.cfg` holds confidential options such as passwords and encryption keys and should generally stay out of it. If you clone the project onto a fresh machine, the credentials are missing, and some exports will change or fail. That is a feature. It forces you to notice what your build depends on.

The professional answer to all three is a **reproducible build**: given the same commit and the same tool versions, anyone on the team gets the same result. Google's release engineers call the strict version of this a **hermetic** build, one that depends only on known versions of its tools and libraries and not on whatever happens to be installed on the build machine. You don't need Google's infrastructure to get most of the benefit. You need three habits.

1. **Build from a clean checkout.** Clone the repository into a fresh folder, open it, export. Anything the build needs that isn't in Git shows up as a missing file now, not on release day.
2. **Pin your tools.** Write the exact Godot version in the README (for example, "Godot 4.x.y stable, standard build") and make everyone use it. Templates must match the editor you export with.
3. **Script the export.** Godot can export from the command line: `godot --headless --path /path/to/project --export-release "Windows Desktop" build/game.exe`. The preset name goes in quotes. The output path is relative to the project, not to the folder you ran the command from, which surprises everyone once. A script that runs the same command every time removes a whole class of "I forgot to tick the box" mistakes.

Hold on to that last idea. Some mistakes you catch by checking. Others you delete by making them impossible. Section 2 puts numbers on both.

## 2. Worked example: why a release needs a checklist

### The hook

Aliens: Colonial Marines (Gearbox and Sega, February 2013) launched to poor reviews and became, in Game Developer's words, a bomb. In October 2017 a modder who goes by James Dickinson posted a note on ModDB describing a typo in one line of the game's configuration. The line remapped an AI behaviour class to a name spelled "Teather" instead of "Tether". The misspelled class did nothing. The correctly spelled one handled, in the modder's reading, the aliens' positioning, patrolling and flanking. Delete one letter in a config file and, by players' reports, the aliens track and follow you far better. The story spread in July 2018, more than five years after release.

Nobody on that team meant to ship the typo. It was one line in a configuration file, and the game still ran, so nothing crashed to tell anyone. That is the shape of most release failures. Each one is a small, unlikely mistake. The question is what happens when you have many of them.

### The model

List everything that could be wrong with a release build. Call each one a **failure item**. For a student game, the list might hold "a scene references a missing asset", "the FPS counter is still on", "the version number wasn't bumped", "the web build doesn't load audio until a click", "the build was exported from someone's uncommitted changes". Then:

- `N` is the number of failure items on your list.
- `p` is the chance that any one item is wrong in a given build, before anyone checks. Use one number for all items at first; the interactive lets you vary it.
- `c` is the **catch rate** of the check for that item: the chance that, if the item is wrong, your check notices before upload. `c = 0` means there's no check. `c = 1` means the check never misses.
- `v` is **coverage**, the share of the `N` items that have a check at all.

If the items fail independently (MA102 week 2), an item escapes into the release with probability `p` if it has no check and `p × (1 − c)` if it does. The release is **clean** only if no item escapes, so you multiply the chances that each one doesn't:

```
P(clean) = (1 − p × (1 − c))^(v × N) × (1 − p)^((1 − v) × N)
```

With no checks at all (`v = 0`), this is just `(1 − p)^N`. That is the complement rule from MA102 week 3 turned around. There, the chance of at least one drop in `n` kills was `1 − (1 − p)^n`. Here, the chance of at least one broken thing in `N` items is `1 − (1 − p)^N`, and that is the chance your release goes out broken.

The **expected number of escaped defects** is simpler still: `N × p` without checks and `N × p × (1 − c)` with full coverage.

### Numbers you can check

Start with a small game and an honest guess. Twenty failure items, each with a 3% chance of being wrong in a given build. Three percent sounds like nothing. Now multiply.

| Failure items `N` | No checks: `(0.97)^N` | Every item checked, `c = 0.9`: `(0.997)^N` |
|---|---|---|
| 10 | 73.7% | 97.0% |
| 20 | 54.4% | 94.2% |
| 40 | 29.6% | 88.7% |
| 80 | 8.7% | 78.6% |

With 20 items and no checks, your release is a coin flip. About 46% of builds go out with at least one problem, and the expected number of problems per release is `20 × 0.03 = 0.6`. Check every item with a 90% catch rate and each item's escape chance falls to `0.03 × 0.1 = 0.003`. Clean releases rise to 94.2%, and expected escapes fall to 0.06, a tenth of what they were.

Check one row by hand. `0.97^20`: square 0.97 to get 0.9409, square again for `0.97^4 = 0.8853`, then `0.8853^5 ≈ 0.544`. The table says 54.4%.

Now the comparison that changes how you write checklists. Take `N = 20`, `p = 0.03`, and two ways to spend the same effort.

| Plan | Coverage `v` | Catch rate `c` | `P(clean)` |
|---|---|---|---|
| No checklist | 0 | — | 54.4% |
| Check the 10 items you worry about, carefully | 0.5 | 0.9 | 71.6% |
| Check all 20 items, quickly | 1.0 | 0.6 | 78.5% |
| Check all 20 items, carefully | 1.0 | 0.9 | 94.2% |

Checking half the items well scores 71.6%. Checking every item loosely scores 78.5%. The ten unchecked items still carry their full 3% each, and `0.97^10 = 0.737` caps you no matter how perfect the other ten checks are. **A checklist's weakest line is the line that isn't on it.**

This script prints both tables. Run it with `.venv/bin/python` and change the numbers to your own team's guesses.

```python
def p_clean(n, p, coverage=1.0, catch=0.0):
    """Chance that no failure item escapes into the release."""
    checked = round(n * coverage)
    unchecked = n - checked
    return (1 - p * (1 - catch)) ** checked * (1 - p) ** unchecked

print("items  no checks  all checked c=0.9")
for n in (10, 20, 40, 80):
    print(f"{n:5}  {p_clean(n, 0.03):9.1%}  {p_clean(n, 0.03, 1.0, 0.9):17.1%}")

plans = [("no checklist", 0.0, 0.0), ("half, careful", 0.5, 0.9),
         ("all, quick", 1.0, 0.6), ("all, careful", 1.0, 0.9)]
for name, v, c in plans:
    print(f"{name:14} {p_clean(20, 0.03, v, c):6.1%}")
```

It prints:

```
items  no checks  all checked c=0.9
   10      73.7%              97.0%
   20      54.4%              94.2%
   40      29.6%              88.7%
   80       8.7%              78.6%
no checklist    54.4%
half, careful   71.6%
all, quick      78.5%
all, careful    94.2%
```

### Move it yourself

Open the interactive. The left view shows one failure item: a single bar at 3%, which looks harmless. The right view shows 100 simulated releases as a grid of squares, each one green if it shipped clean and red if anything escaped, with `P(clean)` printed above it. Drag `N` from 10 to 40 and watch the left bar stay exactly where it was while the grid turns red. Then drag coverage down from 100% to 50% with the catch rate at 90%, and see the red come back even though every check you kept is excellent. Finally, press "Automate 5 items". It removes five items from `N` (a script makes them impossible, as section 1 described) and the grid improves more than a better catch rate would give you.

### Cross-game recognition

The same multiplication turns up wherever a small team has to ship something with many ways to be wrong.

**Surgery, 2007 to 2008.** The World Health Organization's Safe Surgery Saves Lives study introduced a 19-item surgical safety checklist in eight hospitals in eight cities, from Toronto to Ifakara. Haynes and colleagues compared 3,733 patients before the checklist with 3,955 after. Deaths fell from 1.5% to 0.8%, and inpatient complications from 11.0% to 7.0%. Rewrite the complications result in our form. If the checklist acted as a combined catch rate on complications, then `11.0% × (1 − c) = 7.0%`, which gives `c ≈ 0.36`. A checklist that catches only about a third of problems still cut complications by a third, because it runs on every operation. That's coverage doing the work, the same effect as the "all, quick" row in the table. (The study shows association, not a controlled experiment, and the authors say so.)

**Steam for Linux, January 2015.** A user reported that launching Steam after moving its data folder deleted every file his account owned, including a mounted backup drive (issue 3671 on Valve's public steam-for-linux tracker). Users reading the launcher script pointed to a line of the form `rm -rf "$STEAMROOT/"*`. If the variable `STEAMROOT` came out empty, the command became "delete everything under `/`". Commenters proposed checks such as failing if the variable is empty. In our model this is one failure item with a tiny `p` and a catastrophic cost, and a one-line automated check would have given it `c = 1`. Notice also who found it: a player, after release. The item was never on anyone's list, so it had no check, the `(1 − v)` part of the formula.

**Steam's own release gate.** Valve reviews both a game's store page and its build before the first release, and the Steamworks documentation says the store review typically takes 3 to 5 business days. The same page says that once a game passes, there's no need to review again, and you can update as often as you like. In our terms, the platform adds one strong check with high coverage exactly once. Every patch after launch goes out with only your own checklist between it and the players. Your `v` and `c` matter more after launch than before.

**Hermetic builds at Google.** The *Site Reliability Engineering* book describes release builds that depend only on known versions of the build tools and libraries, so two people building the same revision on different machines get identical results. That doesn't raise `c` for any item. It removes whole items from `N`: "built with the wrong engine version", "built with an uncommitted file", "built on the one laptop where it works". The interactive's "Automate" button models exactly this.

Four settings, one formula. Many small risks multiply into a large one. Checks divide each risk. Coverage decides how many risks get divided at all. Automation removes risks instead of dividing them.

### Eyes-open design judgment

- **Coverage first, rigor second.** A short check on every item beats a careful check on half of them. When you write the list, go through every system and every file type in your game before you polish any single line.
- **Automate what a script can decide.** "Is the version number valid?", "is the debug flag off?", "are all referenced files present?" have yes-or-no answers. A script gets them right every time and never gets tired. Humans should spend their attention on what a script can't judge, such as "does the first minute feel right on a stranger's laptop?".
- **Delete items when you can.** Pinning the engine version, building from a clean checkout and exporting from a script each shrink `N`. Shrinking `N` helps every release forever. Raising `c` helps only the releases where someone does the check.
- **Distrust the independence assumption.** The model treats failures as independent. Real ones cluster. A rushed final night raises `p` for every item at once, and one missing template can break three platforms together. When failures cluster, the real `P(clean)` is worse on bad nights than the formula says. That's an argument for freezing features before the release, which section 4 covers.
- **Long lists get skimmed.** Every item costs attention, and a 60-line list that nobody reads has an effective `c` near zero. Keep each checklist to what one person can do properly in one sitting, and split it by stage (before export, after export, after upload).

### Check this example

1. A team has 30 failure items at 2% each and no checks. What is `P(clean)`? How many releases out of 10 would you expect to ship with at least one problem?
2. The same team checks all 30 items with `c = 0.8`. What is the new `P(clean)` and the new expected number of escaped defects per release?
3. A teammate proposes a 10-item checklist with `c = 0.99` instead. Which plan is better, and why?

<details>
<summary>Answers</summary>

1. `0.98^30 ≈ 0.545`, so about 54.5% clean and about 4 or 5 of 10 releases broken.
2. Each item escapes with `0.02 × 0.2 = 0.004`. `0.996^30 ≈ 0.887`. Expected escapes `30 × 0.004 = 0.12`, down from 0.6.
3. `0.9998^10 × 0.98^20 ≈ 0.998 × 0.668 ≈ 0.667`. The full-coverage plan (88.7%) wins by a wide margin, because the 20 unchecked items keep their full 2% each.

</details>

## 3. Build identity: versions, build numbers and changelogs

A player who reports "the boss fight crashes" is only useful to you if you know which build they played. Every build you hand to anyone needs an identity that is visible, unique and traceable back to a commit.

**Semantic Versioning.** The SemVer 2.0.0 specification writes a version as `MAJOR.MINOR.PATCH`. You increment MAJOR for incompatible changes, MINOR for new functionality that stays compatible, and PATCH for compatible bug fixes. The spec adds two optional labels. A **pre-release** label after a hyphen (`1.0.0-rc.1`) marks a version that isn't final yet, and it sorts before the plain version, so `1.0.0-rc.1 < 1.0.0`. **Build metadata** after a plus sign (`1.0.0+a3f9c21`) is ignored when comparing versions. It's a good place for a Git commit hash.

SemVer was written for software libraries, where "incompatible" means other programs break. For a game, translate it. MAJOR changes when saves from the old version no longer load, or when multiplayer versions can't play together. MINOR changes when you add content. PATCH changes when you only fix things. For this course, your jam build is `0.1.0`, your final release candidates are `1.0.0-rc.1`, `1.0.0-rc.2` and so on, and the build you submit is `1.0.0`.

**Show the version in the game.** Put it on the title screen or the pause menu, small, with the commit hash. Godot lets you set `application/config/version` in the project settings and read it at runtime with `ProjectSettings.get_setting("application/config/version")`. A screenshot of a bug with the version in the corner is worth ten written reports.

**Build numbers and stores.** itch.io's command-line uploader, butler, generates its own increasing integer version for each channel unless you pass your own with `--userversion` (or `--userversion-file`, a file holding one line). The documentation notes that itch.io orders builds by upload order, not by comparing your version strings. So your version string is for humans, and you are responsible for making it increase.

**The changelog.** A changelog is a plain file (`CHANGELOG.md`) with one heading per version and a short list of what changed, written for players and graders rather than for developers. "Fixed crash when pausing during the boss intro" belongs there. "Refactored BossController" doesn't. Your release checklist should refuse to ship a version that has no changelog heading, and the lab script does exactly that.

**Keep old builds.** Keep every build you upload, zipped, with its version in the file name. If `1.0.1` breaks something `1.0.0` didn't, the fastest fix is often to re-upload `1.0.0` while you investigate. You can only do that if you still have it. MMO308 week 9 returns to this idea at live-game scale, with staged rollouts and rollbacks ([MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md)).

## 4. The release checklist, stage by stage

A release is a short sequence of stages. Each stage has its own checks, and each check has an owner and a pass condition. Here is the sequence for your final game, working back from the deadline.

**Feature freeze (release minus 5 days).** No new features after this point, only fixes. Freezing lowers `p` for every item at once, because the code stops moving under your checks. It's also the date where your week 4 cut list does its job. Anything not done at freeze is cut.

**Release candidate (release minus 3 days).** Tag the commit in Git (`v1.0.0-rc.1`), build it from a clean checkout with your export script, and treat that exact file as the thing you might ship. A **release candidate** (RC) is a build you would be willing to release if no blocking bug is found. If you fix a bug, you make `rc.2` and check again. You never "just patch" the RC by hand.

**Smoke test (on every RC).** You met the smoke test in week 10, the few minutes of play that tell you whether a build is worth testing at all. For a release candidate, tighten it. Write it down, have someone who didn't make the build run it, and run it on a machine that isn't the build machine. Start the game, start a new session, reach the first checkpoint, pause, quit, restart, confirm the settings persisted. Your week 10 bug tracker gets anything that fails.

**Go/no-go (release minus 1 day).** A short meeting with one question: do we ship this RC? The producer asks each owner whether their checklist section passed. Any open bug marked as a blocker means no-go. Decide the blocker rule in advance, so the meeting doesn't turn into a debate at midnight.

**Upload and verify (release day).** Upload with a script, then download the build from the store page as a player would, on a different machine, and run the smoke test once more. The build on the store is the one that counts, and uploads can fail quietly. With butler, the command has the form `butler push build/windows yourname/yourgame:windows --userversion 1.0.0`, where the part after the colon is the **channel**, the slot that build goes into (for example `windows`, `linux` or `html5`).

A checklist for a student Godot game might start like this. Notice that each line says who checks it and how to tell it passed.

| Stage | Check | Owner | Pass condition | Automated? |
|---|---|---|---|---|
| RC | Built from a clean clone of the tagged commit | Build owner | Script log shows the tag and a fresh folder | Yes |
| RC | Version is valid SemVer and newer than the last release | Build owner | `release_check.py` passes | Yes |
| RC | Changelog has a heading for this version | Producer | `release_check.py` passes | Yes |
| RC | No debug flags on (FPS counter, god mode, level skip) | Programmer | `release_check.py` passes | Yes |
| RC | Every file in the asset manifest is in the build | Art lead | `release_check.py` passes | Yes |
| Smoke | Game starts on a machine that isn't the build machine | QA owner | Title screen in under 10 s | No |
| Smoke | New game to first checkpoint, pause, quit, restart | QA owner | No errors, settings persist | No |
| Smoke | Web build plays audio after first click | QA owner | Sound heard in two browsers | No |
| Upload | Store build downloaded and run | Producer | Version on title screen matches the RC | No |

Two rules keep such a list honest. First, every line needs a pass condition someone else could verify. "Check audio" is not a line. "Sound heard in two browsers" is. Second, the list lives in Git next to the code, and you edit it after every release. When a problem escapes, the week 14 post-mortem asks which line should have caught it, and the answer is either "tighten that line" or "add a line". That is how `v` climbs over time.

## In-class activity (25 minutes)

In your final-project teams.

1. **List failure items (10 minutes).** Write every way your final build could ship broken. Aim for at least 20. Go system by system (input, save, audio, UI, each level, each platform) so coverage comes first.
2. **Estimate (5 minutes).** Give each item a rough `p` (1%, 5% or 20%). Using the interactive's custom mode, enter your `N` and the average `p`, and record `P(clean)` with no checks.
3. **Plan (10 minutes).** Mark each item "automate", "delete" (make impossible) or "human check". For human checks, write the pass condition. Enter the new `N` and your guessed catch rate into the interactive and record the new `P(clean)`.

Expected output: one page with the item list, the two `P(clean)` numbers, and the three items your team thinks are most likely to escape anyway.

## Common misconceptions

- **"Each risk is tiny, so the release is safe."** Small risks multiply. Twenty items at 3% give a 46% chance that something ships broken. Judge the release, not the item.
- **"A careful check on the risky items is enough."** Unchecked items keep their full risk and cap `P(clean)`. In section 2, half coverage at 90% loses to full coverage at 60%.
- **"If it runs in the editor, the build works."** The editor uses your cache, your local files and debug settings. Only a build made from a clean checkout, run on another machine, tells you what players get.
- **"The version number is cosmetic."** Without a unique, visible version you can't match a bug report to a build, can't roll back, and can't tell whether a fix shipped.

## Check yourself

1. Your checklist covers 16 of 20 items with `c = 0.95`, and `p = 0.04` for every item. Compute `P(clean)`. Which change helps more, raising `c` to 1.0 or adding checks with `c = 0.5` to the last four items?
2. Put these versions in SemVer order: `1.0.0`, `1.0.0-rc.2`, `0.9.3`, `1.0.0-rc.10`, `1.0.1`. (Pre-release identifiers that are numbers compare as numbers.)
3. A teammate exports the final build from their laptop, where it works. It crashes on the grader's machine with a missing texture. Name two habits from section 1 that would have caught this and say which model variable each one changes.
4. Your team found an error in the Aliens: Colonial Marines kind of shape: a config line names a class that doesn't exist, and the game runs anyway. Write the pass condition for an automated check that would catch it.

<details>
<summary>Answers</summary>

1. Checked items escape with `0.04 × 0.05 = 0.002`, so `0.998^16 × 0.96^4 ≈ 0.9685 × 0.8493 ≈ 0.823`. Raising `c` to 1.0 gives `1 × 0.8493 ≈ 0.849`. Adding checks at `c = 0.5` to the last four gives `0.998^16 × 0.98^4 ≈ 0.9685 × 0.9224 ≈ 0.893`. Covering the last four items helps more.
2. `0.9.3 < 1.0.0-rc.2 < 1.0.0-rc.10 < 1.0.0 < 1.0.1`. Numeric identifiers compare as numbers, so rc.10 is after rc.2, and any pre-release sorts before its release.
3. Building from a clean checkout (reveals files that exist only on the laptop, which catches the item, raising `c`) and running the smoke test on a machine that isn't the build machine (also raises `c`). A scripted export from the tagged commit removes the "built from local state" item entirely, which lowers `N`.
4. For example, "every class name on the right-hand side of a remapping line exists in the class list exported from the engine, and the check fails the build with the line number if not". Any answer works if a script can decide it and it fails loudly.

</details>

## Lab / assignment hook

[Lab 13, release checker and dry-run release](../labs/lab13.md). You finish a small Python script that checks a build folder for a valid version, a changelog entry, debug flags and missing files, then use it together with a written checklist to do a dry-run release of your final game to a private itch.io page. The checklist becomes part of your final team game submission in week 15.

## Sources

- Wawro, A. "Colonial Marines modder finds big AI fix by changing one letter of code." Gamasutra (now Game Developer), 13 July 2018. The ModDB note by the modder James Dickinson (October 2017), the `Teather`/`Tether` class remapping line, and the modder's description of what the correct class controls. The game's 2013 release by Gearbox and Sega is from the same article; the article's description of the AI effect is based on players' reports and the modder's own inference.
- ValveSoftware/steam-for-linux, GitHub issue 3671, "Moved ~/.local/share/steam. Ran steam. It deleted everything on system owned by user." Opened 14 January 2015. The comments quote the `rm -rf "$STEAMROOT/"*` line in `steam.sh` and propose empty-variable checks. https://github.com/ValveSoftware/steam-for-linux/issues/3671
- Haynes, A. B., Weiser, T. G., Berry, W. R., et al. (2009). "A surgical safety checklist to reduce morbidity and mortality in a global population." *New England Journal of Medicine* 360(5), 491-499. 19-item checklist, eight hospitals, 3,733 and 3,955 patients, deaths 1.5% to 0.8%, complications 11.0% to 7.0%. PubMed 19144931.
- Valve, Steamworks documentation, "Review Process" (read September 2026). Store presence and build reviewed before release; store review typically 3 to 5 business days; no further review for updates. https://partner.steamgames.com/doc/store/review_process
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 8, "Release Engineering", section "Hermetic Builds". Free online at sre.google.
- Godot Engine documentation (stable branch, 4.x, read September 2026), "Exporting projects". Export templates required; `export_presets.cfg` safe to commit, `.godot/export_credentials.cfg` confidential; `--export-release`, `--export-debug` and `--path` command-line options; output path relative to the project.
- Preston-Werner, T. *Semantic Versioning 2.0.0*. semver.org. MAJOR.MINOR.PATCH rules, pre-release and build-metadata labels and their precedence.
- itch.io, butler documentation, "Pushing builds" (read September 2026). `butler push directory user/game:channel`, channel names, `--userversion` and `--userversion-file`, ordering by upload.

## Interactive spec: examples/w13-release-risk.html

**The one insight.** A per-item risk that looks negligible multiplies into a large release risk, and coverage (how many items have any check) matters more than how good each check is.

**Layout.** Two linked views side by side on desktop, stacked on mobile (grid first on mobile, since it holds the insight).

1. **Left view, "one item".** A single horizontal bar from 0% to 100% showing the per-item escape chance. Draw two segments: the raw risk `p` (outline) and the escape chance after a check `p × (1 − c)` (filled). Under it, large text: "One item: p = 3.0%. Escapes after check: 0.3%." Below that, a stacked bar of the `N` items, one thin cell per item, shaded "checked" (filled) or "unchecked" (outline) by coverage.
2. **Right view, "100 releases".** A 10 × 10 grid of squares. Each square is one simulated release: green (survival/value token color) if clean, red (damage token color) if at least one item escaped. Above the grid, large text: "P(clean) = 54.4% (model)" and "Clean in this sample: 52 of 100 (seed 13)". The sample count comes from the seeded simulation and differs from the model, which is the point of showing both. Under the grid, "Expected escaped defects per release: 0.60".

**Controls** (keyboard operable, values shown beside each; every change redraws both views immediately).

- Failure items `N`: slider 1 to 100, step 1, default 20.
- Per-item risk `p`: slider 0.5% to 20%, step 0.5%, default 3%.
- Coverage `v`: slider 0% to 100%, step 5%, default 0%.
- Catch rate `c`: slider 0% to 100%, step 5%, default 90% (disabled look when coverage is 0%).
- Button "Automate 5 items": subtracts 5 from `N` (minimum 1) and shows a note "N reduced by automation: 20 → 15". A "Reset" button restores defaults.
- Button "New sample": reseeds the simulation.
- Preset buttons that set coverage `v` and catch rate `c` only, leaving `N` and `p` where they are: "No checklist" (v 0, c 90%), "Half, careful" (v 50%, c 90%), "All, quick" (v 100%, c 60%), "All, careful" (v 100%, c 90%).

**Formulas.**

```
checked   = round(N × v)
unchecked = N − checked
P_clean   = (1 − p × (1 − c))^checked × (1 − p)^unchecked
E_escapes = checked × p × (1 − c) + unchecked × p
```

Simulation: for each of 100 releases, for each item draw a uniform number; the item escapes if the draw is below its escape chance (`p × (1 − c)` if checked, else `p`). Use a seeded PRNG (mulberry32, default seed 13) so the default screen is identical every load. Show model and sample values side by side, never only the sample.

**Readout table** below both views with columns: Plan, v, c, P(clean). Rows are the four presets computed for the current `N` and `p`, with the row matching the current sliders highlighted.

**Test values** (must match the lecture tables to one decimal).

- p 3%, v 0: N 10, 20, 40, 80 give 73.7%, 54.4%, 29.6%, 8.7%.
- p 3%, v 100%, c 90%: N 10, 20, 40, 80 give 97.0%, 94.2%, 88.7%, 78.6%.
- N 20, p 3%: v 50% c 90% gives 71.6%; v 100% c 60% gives 78.5%.
- N 20, p 3%, v 0: E_escapes 0.60. v 100%, c 90%: 0.06.
- N 30, p 2%, v 100%, c 80%: 88.7%, E_escapes 0.12.

**Behaviour.** The first screen shows the default (N 20, p 3%, v 0) so about half the grid is red. Grid squares change color with a 150 ms fade, none under `prefers-reduced-motion`. Colors from `templates/interactive-tokens.css`. Squares are plain; no game art, no logos.
