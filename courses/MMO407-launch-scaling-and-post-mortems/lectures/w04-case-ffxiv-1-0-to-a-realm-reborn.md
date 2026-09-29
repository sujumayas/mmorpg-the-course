# MMO407 · Week 04 — Case: Final Fantasy XIV 1.0 to A Realm Reborn

**Why this matters:** Most failed MMO launches end in one of two ways. The team patches the game for years and it never recovers, or the studio shuts it down. Final Fantasy XIV took a third path. Square Enix rebuilt the game from scratch while keeping the broken one running, and relaunched it three years later as one of the most successful MMOs ever made. This week you learn to tell when a rebuild beats patching, what it costs to keep the old game alive while you rebuild, and why a relaunch is a second launch with all of week 1's problems.

**You will be able to:**
- Compute the time to close a quality gap by patching and by rebuilding, from the size of the gap, the share of it that is structural and the penalty the old code puts on structural fixes.
- Derive the crossover penalty above which a rebuild is faster, and explain which parameters move it.
- Compute what it costs in months to keep part of the team on the old game during a rebuild, and argue what that time buys.
- Critique a relaunch plan (Final Fantasy XIV, The Elder Scrolls Online, No Man's Sky) by naming which parameter each studio's decision depended on.

**Before class:** Read Kevin Gifford, "The death and rebirth of Final Fantasy 14" (Polygon, 21 November 2012), about 15 minutes. Watch Naoki Yoshida's GDC 2014 talk "Behind the Realm Reborn" (GDC Vault, the first 30 minutes), or read Philip Kollar's report of it in Polygon (20 March 2014). Read Joel Spolsky, "Things You Should Never Do, Part I" (Joel on Software, 6 April 2000), 10 minutes. It argues the opposite of this case, and you need both sides.

**Prerequisites from earlier courses:** [MMO306 week 12, content tooling and pipelines](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w12-content-tooling-and-pipelines.md) (the 1.0 asset budget failures, including the flowerpot; not repeated here). [MMO305 week 12, community management](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md) (Yoshida's Letters from the Producer; this week treats them as one part of the rebuild plan). [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (how suspending sales lowered the arrival rate at the 2013 relaunch). [Week 1 of this course](w01-launch-day-anatomy.md) (the launch pipeline and its bottleneck) and [week 3](w03-beta-strategies.md) (beta exposure, and A Realm Reborn's four beta phases).

**Interactive:** [examples/w04-patch-or-rebuild.html](../examples/w04-patch-or-rebuild.html). Keep it open during section 2.

---

## 1. What happened, in order

Before you model a case, fix its timeline. Dates discipline the story. They stop you from explaining an early decision with a fact that only came out later.

| Date | Event |
|---|---|
| 22 September 2010 | Collector's edition early access for Final Fantasy XIV (Windows) |
| 30 September 2010 | Launch. Metacritic average later settles at 49 out of 100 |
| November 2010 | The 30-day free trial is extended for the second time |
| December 2010 | Producer Hiromichi Tanaka and director Nobuaki Komoto removed. Naoki Yoshida becomes producer and director. Subscription fees suspended. PlayStation 3 version postponed |
| January 2011 | Planning starts for a new game built from scratch |
| April 2011 | Work on the new engine and server structure begins in earnest |
| July 2011 | Patch 1.18 to the old game: battle changes, auto-attack, instanced dungeons, fatigue system removed |
| September 2011 | Square Enix president Yoichi Wada says at Tokyo Game Show that the launch "greatly damaged" the Final Fantasy brand |
| October 2011 | "Version 2.0" announced publicly, with a roadmap and the Legacy Campaign |
| January 2012 | Billing resumes for the old game |
| 1 November 2012 | Final patch to the old game |
| 11 November 2012 | Old servers shut down after a world-ending in-game event |
| February 2013 | First of four beta phases for A Realm Reborn |
| 24 August 2013 | Early access for A Realm Reborn |
| 27 August 2013 | A Realm Reborn launches |

At GDC 2014, Yoshida described the whole effort as maintaining one MMO while building another, over two years and eight months. Count it from his appointment in December 2010 to the August 2013 launch and you get 32 months.

His post-mortem named three causes of the 2010 failure. The first was an obsession with graphical quality at the expense of server performance. The second was a team without experience of modern MMOs, whose brief was to make something different from Final Fantasy XI. The third was a belief that anything wrong could be fixed in later patches. The third cause is this week's subject. When is "we'll patch it" true, and when is it a trap?

## 2. Worked example: patch forward or rebuild?

### The hook

Every game that launches badly faces the same meeting. One camp says the game is 70% right and the team should fix the rest in patches, as players watch it improve. The other camp says the foundation is broken and every patch will fight it. Both camps can point at shipped games that prove them right.

In 2011 Final Fantasy XIV's team had both kinds of evidence in the same codebase. Patch 1.18 showed the old game could change. It added auto-attack and instanced dungeons and removed the hated fatigue system. Yet Wikipedia's summary of the development record says the old source code's outdated and cumbersome choices blocked the more radical changes the game needed, and that the engine and server structure were critically flawed. The team patched and rebuilt at once. Why was that right for this game, when Spolsky's essay says a rewrite is the single worst strategic mistake a software company can make?

### The model

Put the choice in one unit, months of team work. Name the numbers.

- `G` is the **quality gap**, the work needed to turn the current game into one you are willing to charge for, in fix-units. A **fix-unit** is one month of the whole team's work on a healthy codebase.
- `φ` (phi) is the **structural share**, the fraction of `G` that lives in the foundation: engine, server architecture, data formats, the asset pipeline. The rest, `1 − φ`, is content and tuning.
- `m` is the **structural penalty**, how many times more a structural fix costs when you make it inside the old code. You have to work around what the foundation assumes, keep old saves loading, and ship without breaking a live game. `m = 1` means the old code is no obstacle.
- `F` is the team's capacity in fix-units per month. With the definition above, `F` is 1 per month for the whole team. Using `F = 10` lets you think of ten squads, each doing one unit a month.
- `T_r` is the **rebuild time**, the months to build a new foundation and bring the existing content across. When it is done, the structural gap is gone by design.

The two paths:

```
patch:    T_patch   = G × (φ × m + 1 − φ) / F
rebuild:  T_rebuild = T_r + (1 − φ) × G / F
```

Patching pays the penalty `m` on the structural part and the normal price on the rest. Rebuilding pays `T_r` up front and then the normal price on the content part.

Set them equal to find the **crossover penalty** `m*`, the penalty at which the two paths take the same time:

```
G × φ × m / F  =  T_r      ⇒      m* = T_r × F / (φ × G)
rebuild is faster when m > m*
```

Read it out loud. A rebuild wins when the structural share is large (`φ` big), the gap is large (`G` big) and the old code taxes structural work heavily (`m` big). It loses when the rebuild itself is long (`T_r` big). How bad the game looks is not in the formula on its own. What matters is how much of the badness lives in the foundation, and how much the foundation charges for each fix.

### Numbers you can check

Take a team with `F = 10` fix-units per month, a gap of `G = 300` fix-units, and a rebuild that takes `T_r = 24` months. These are invented teaching values. Three games have the same gap but different causes.

| Game | `φ` | `m` | `T_patch` | `T_rebuild` | `m*` | Faster path |
|---|---|---|---|---|---|---|
| A, surface problems | 0.1 | 3 | 36.0 | 51.0 | 8.00 | patch |
| B, deep but cheap to fix | 0.5 | 1.5 | 37.5 | 39.0 | 1.60 | patch, just |
| C, deep and taxing | 0.5 | 4 | 75.0 | 39.0 | 1.60 | rebuild |

Check game C by hand. Patching costs `300 × (0.5 × 4 + 0.5) / 10 = 300 × 2.5 / 10 = 75` months. Rebuilding costs `24 + 0.5 × 300 / 10 = 24 + 15 = 39` months. The crossover is `24 × 10 / (0.5 × 300) = 1.6`, and C's penalty of 4 is far above it.

Game A is the lesson Spolsky wanted Netscape to learn. Only 10% of the gap is structural. Even a penalty of 3 leaves patching 15 months faster, and the crossover sits at 8, a penalty few codebases reach. Game B is the dangerous one. It feels like game C, because half of what is wrong is deep. But the old code is not fighting the team hard, so patching still wins by a month and a half, and it wins with players in the game the whole time.

This script prints the table:

```python
G, F, T_R = 300, 10, 24     # gap (fix-units), team (units/month), rebuild (months)

def patch_months(phi, m):
    """Fix everything inside the old code: structural work costs m times more."""
    return G * (phi * m + 1 - phi) / F

def rebuild_months(phi, s=0.0, c=0.0):
    """New foundation first (structural gap gone), then the rest of the gap.
    s = share of the team kept on the old game, c = share of that work that carries over."""
    build = T_R / (1 - s)
    carried = c * s * F * build
    rest = max(0.0, (1 - phi) * G - carried)
    return build + rest / F

def crossover_m(phi):
    return T_R * F / (phi * G)

for label, phi, m in [("A, surface problems", 0.1, 3), ("B, deep but cheap", 0.5, 1.5),
                      ("C, deep and taxing", 0.5, 4)]:
    p, r = patch_months(phi, m), rebuild_months(phi)
    print(f"{label:22} patch {p:5.1f}  rebuild {r:5.1f}  m* {crossover_m(phi):4.2f}"
          f"  -> {'rebuild' if r < p else 'patch'}")
for s, c in [(0, 0), (0.25, 0), (0.25, 0.5)]:
    print(f"C with s={s:.2f}, c={c:.1f}: rebuild {rebuild_months(0.5, s, c):5.1f} months")
```

It prints:

```
A, surface problems    patch  36.0  rebuild  51.0  m* 8.00  -> patch
B, deep but cheap      patch  37.5  rebuild  39.0  m* 1.60  -> patch
C, deep and taxing     patch  75.0  rebuild  39.0  m* 1.60  -> rebuild
C with s=0.00, c=0.0: rebuild  39.0 months
C with s=0.25, c=0.0: rebuild  47.0 months
C with s=0.25, c=0.5: rebuild  43.0 months
```

The last three lines belong to section 3. They show what happens when you keep part of the team on the old game during the rebuild, as Final Fantasy XIV did.

### Move it yourself

Open the interactive. The top view plots the remaining gap against months for both paths. The patch line starts falling at once and falls slowly. The rebuild line stays flat for `T_r` months, drops by the structural share the moment the new foundation lands, then falls at the healthy rate. Where the lines cross the zero axis tells you which path finishes first. The bottom view is a map with `φ` across and `m` up. The curve `m = m*(φ)` splits it into a patch region below and a rebuild region above, and a dot marks your current game.

Drag `m` up from 1 for game B. The dot rises through the curve at 1.6 and the finishing order flips. Now drag `T_r` from 24 to 36. The whole curve rises and the rebuild region shrinks. Notice what the top view shows that the formula hides. Even when the rebuild finishes first, the patch line is below it for many months. Patch-path players see progress every month, and rebuild-path players see none for two years. Section 3 is about that gap.

### Cross-game recognition

The decision recurs whenever a shipped product disappoints. What changes is where the gap lives.

**Final Fantasy XIV (2010 to 2013).** In the model, the case is a large `φ` and a large `m`. The record says the engine and server structure were critically flawed, and that the source code blocked radical changes. Yoshida also said in 2012 that Square Enix's engines of the time were built for offline games and could not handle hundreds of characters on screen online. That is a structural gap no patch could close. Square Enix chose to rebuild and to keep the old game running. The model says the rebuild was right. Section 3 asks whether running both was.

**No Man's Sky (Hello Games, August 2016 onward).** A single-player and online survival game, not an MMO, but the best-known patch-forward recovery. It launched on 9 August 2016 to anger over missing features. Hello Games shipped free updates, starting with Foundation in November 2016, and added multiplayer with the Next update in 2018. The game's gap was mostly content and features (`1 − φ` large), and the engine could carry them (`m` near 1). The model says patch, and patching worked. Players saw each step.

**The Elder Scrolls Online (ZeniMax Online, 2014 to 2015).** Launched on 4 April 2014 on Windows and macOS with a compulsory monthly subscription and a mixed reception. On 17 March 2015 it relaunched as Tamriel Unlimited, buy-to-play with an optional subscription, and reception improved. ZeniMax patched the game and changed the business model instead of rebuilding. Part of its gap was the price, not the code. A pricing gap has `φ = 0` for engineering, so a rebuild could not have helped.

**Outside games: Netscape (1997 to 2000).** Spolsky's essay points out that Netscape went nearly three years between version 4.0 and the beta of version 6.0, with no version 5.0, because the company rewrote its browser from scratch. Netscape 6.0 shipped on 14 November 2000 and was widely judged too unstable. Spolsky's case against rewrites is about `T_r`. Old code holds years of forgotten fixes, so rebuilding takes far longer than estimated, and an underestimated `T_r` flatters the rebuild.

Four products, one comparison. Ask first what fraction of the gap is structural and what the old code charges for it.

### Eyes-open design judgment

- **Estimate `φ` by listing the gap, not by feel.** Write down every problem, tag each one structural or content, and size it. Teams in a crisis overrate `φ`, because structural problems are the ones that feel hopeless. An honest list often shows game B, not game C.
- **Measure `m`, do not guess it.** Pick two structural fixes and make them in the old code. How long they take compared with a clean estimate is your `m`. Patch 1.18 was, among other things, a measurement of what the old game could absorb.
- **Pad `T_r`.** Spolsky's point is that rebuild estimates run long. Add 50% to `T_r` and check the decision still holds. In game C, `T_r = 36` gives `m* = 2.4`, and a penalty of 4 is still above it. In game B it moves further into patch territory.
- **A rebuild shows nothing for `T_r` months.** On the model's clock, rebuilding finishes first. On the players' clock, patching improves the game every month and rebuilding does not improve it at all until launch. If players leave during the wait, the rebuild launches to fewer of them. That is the cost the next section prices.
- **Do not rebuild a pricing problem.** Some gap items are not code at all, such as price or platform.

### Check this example

1. For game C, what `T_r` makes patching and rebuilding take exactly the same time?
2. A team estimates `φ = 0.3`, `G = 400`, `F = 10`, `T_r = 30` and measures `m = 2`. Which path is faster, and by how many months?
3. Why does a larger gap `G` make a rebuild more attractive, when `G` appears on both sides of the comparison?

<details>
<summary>Answers</summary>

1. Patching takes 75 months. Rebuilding takes `T_r + 15`. They are equal at `T_r = 60` months.
2. `T_patch = 400 × (0.6 + 0.7) / 10 = 52` months. `T_rebuild = 30 + 0.7 × 400 / 10 = 58` months. Patching is faster by 6 months. Check with the crossover: `m* = 30 × 10 / (0.3 × 400) = 2.5`, and `m = 2` is below it.
3. The content part `(1 − φ) × G / F` is the same on both paths and cancels. What is left is `φ × G × m / F` against `T_r`. A larger `G` makes the structural work bigger, so the penalty `m` is paid on more units, while `T_r` stays fixed.

</details>

## 3. Running two games at once

Final Fantasy XIV did not stop the old game while it built the new one. Yoshida kept a share of the team on version 1.0, shipped real patches, told a story that ended the old world on purpose, and brought the old players into the new game with rewards. Put that choice into the model.

### What it costs

Let `s` be the share of the team kept on the old game during the rebuild. The rebuild team now has capacity `(1 − s) × F`, so the build phase stretches to `T_r / (1 − s)`. Some of the old-game work carries over. The team can test new features, pipelines and ideas on live players, then rebuild them in the new game with fewer false starts. Let `c` be the share of the old-game work that carries over:

```
build     = T_r / (1 − s)
carried   = c × s × F × build
T_rebuild = build + max(0, (1 − φ) × G − carried) / F
```

The last lines of the script show game C. Keeping a quarter of the team on the old game (`s = 0.25`) stretches the build from 24 to 32 months. With nothing carried over, the rebuild finishes in 47 months instead of 39. If half the old-game work carries over (`c = 0.5`), 40 fix-units come across and the rebuild finishes in 43. The parallel plan costs four months.

The GDC record says the old game really did serve this way. The team tested the new workflow on updates to version 1.0 and then used it for A Realm Reborn, and features trialled on live players carried into the relaunch. That is a positive `c`.

### What it buys

Four months are a real cost. Here is what Final Fantasy XIV bought with them.

- **A player base that did not reset to zero.** Players who stayed through 2011 and 2012 carried their characters into the new game. A relaunch that begins with a community already in it has guilds, veterans who can answer questions, and a market with sellers on the first day.
- **Proof, delivered monthly.** Patch 1.18 in July 2011, seven months after the change of leadership, was visible evidence that the new team could ship. A rebuild alone shows players nothing until launch. MMO305 week 12 covered the Letters from the Producer. Here, notice that the letters were credible because patches followed them.
- **A story for the break.** The team rewrote the old game's plot to end with the moon Dalamud falling on the world. The servers closed on 11 November 2012 after a final battle open to every player, and A Realm Reborn picked up the story after that disaster. The changed map, systems and look of the new game had an in-world reason. A rebuild that simply swaps the game under players' feet has none.
- **A reason to keep paying.** When billing resumed in January 2012, the Legacy Campaign offered players who paid for at least three months a permanently reduced subscription, an exclusive chocobo mount, and their name in the credits of version 2.0. Each reward was cheap to give and hard to get anywhere else, and each one tied a paying player to the relaunch.

There were costs the model does not show. Server merges carried out before the relaunch drew an angry first reaction from players. Wada said in late 2012 that A Realm Reborn's development had delayed many other Square Enix titles. The team, in Yoshida's words at GDC, maintained one MMO while building another for two years and eight months. Crunch has a price the model has no column for.

### When not to run both

The parallel plan is worth its months when the old game still has players who would come to the new one, and when old-game work can carry over. It is not worth it when the old game is empty, or when its code is so far from the new one that nothing learned in it transfers (`c` near 0). In that case, close the old game honestly, keep the community channels open, and put everyone on the rebuild. Week 11 covers shutdowns.

## 4. A relaunch is a launch

A Realm Reborn launched into week 1's problems. Early access opened on 24 August 2013, and players reported server trouble through the whole period to launch on 27 August. Square Enix described the response as overwhelmingly positive, the servers could not hold the number of concurrent players, and the company temporarily suspended digital sales. Yoshida apologized for a rocky launch and promised fixes and new servers. A week after launch the game went down for ten hours of maintenance and patches, and every player got a week of free play time.

Three things about this second launch are worth carrying to your own plans.

**Relaunch demand is harder to forecast than launch demand.** A new game's forecast starts from pre-orders and beta sign-ups. A relaunch has those plus lapsed players, whose return rate nobody knows. Many of them quit in 2010 and may never have told anyone they were watching. Square Enix had run four beta phases in 2013 (week 3 covers why), yet it still underestimated concurrency.

**Stopping sales is a lever on the arrival rate.** MMO302 week 9 modeled this. Suspending digital sales lowers `λ`, the rate of new players arriving at the login queue, and adding servers raises capacity. Square Enix pulled both levers. The lesson for a launch plan is to decide in advance who may stop sales, and on what signal, so the decision takes minutes, not a board meeting.

**A reputation gap closes slowly.** Yoshida said after the relaunch that A Realm Reborn was only the first step in regaining player trust, and that the process would take a long time. A rebuild can close the quality gap in a known number of months. The trust gap has no `F`. It closes at the pace players are willing to believe you, and each broken promise sends it back. That is why the team said it would not release "until it is ready," and why a rocky relaunch week was forgiven in a way the 2010 launch was not.

By October 2021, Final Fantasy XIV had more than 24 million registered players, and Square Enix credited the game in part for its return to profit in 2014. The case is famous because it is rare. Most games that launch at a Metacritic 49 never get a second launch.

## 5. Reading this case as a post-mortem

The course ends with you writing a post-mortem (week 12) and a launch plan (week 13). Practise the habits now on this case.

- **Separate causes from symptoms.** "Bad reviews" is a symptom. Yoshida's three causes (graphics before server performance, no modern MMO experience, faith in later patches) are causes, and each one maps to a decision someone made before launch.
- **Name the parameter each cause moved.** Graphics before performance raised `φ`, because the problem was in the engine. Faith in later patches is a belief that `m` is 1. The lack of MMO experience made `G` larger than the team knew.
- **Ask what was known at the time.** Week 3 noted that the 2010 beta was bug-laden and shortened. Evidence that the gap was structural existed before launch.
- **Keep what transfers.** The transferable lessons here are the structure of the decision (list the gap, measure `m`, pad `T_r`) and the parallel plan's four purposes (keep players, show proof, give the break a story, reward those who stay). Final Fantasy XIV's specific numbers do not transfer. Its method does.

## In-class activity (25 minutes)

Groups of three. Each group gets the same studio brief with a different gap list.

Your MMO launched eight weeks ago to poor reviews. The team has `F = 12` fix-units per month. A rebuild of the foundation is estimated at `T_r = 20` months. The gap list totals `G = 360` fix-units. The group's card gives the structural items and their sizes, from which you compute `φ`. The card also reports the time two structural fixes took inside the old code against their clean estimates, from which you compute `m`.

1. Compute `φ`, `m`, `T_patch`, `T_rebuild` and `m*`. Name the faster path.
2. Pad `T_r` by 50%. Does the decision change?
3. Decide whether to keep a share of the team on the old game. Choose `s` and justify a value of `c`. Compute the cost in months.
4. Write one sentence for players announcing your decision, and list the first thing players will see change, with its month.

Expected output for the card with structural items of 90, 60 and 30 units and measured times of 2.5× and 3.5× the estimate: `φ = 180 / 360 = 0.5`, `m = 3` (the mean), `T_patch = 360 × 2 / 12 = 60` months, `T_rebuild = 20 + 15 = 35` months, `m* = 20 × 12 / 180 = 1.33`. The rebuild wins. With `T_r = 30`, `T_rebuild = 45` and `m* = 2.0`, so it still wins. With `s = 0.25` and `c = 0.5`, the build takes 26.7 months, 40 units carry over, and the rebuild finishes in about 38.3 months.

## Common misconceptions

- **"The game is terrible, so it needs a rebuild."** How bad the game is sets `G`, and `G` alone does not decide. A large gap made of content problems is faster to patch. Look at `φ` and `m`.
- **"A rebuild is always a mistake."** Spolsky's argument is that `T_r` is usually underestimated and that old code holds hidden fixes. Both are true, and both go into the model. When `φ × m` is large enough, a padded rebuild still wins, as it did for Final Fantasy XIV.
- **"Keeping the old game running is wasted effort."** It costs months, and it buys players, proof and carry-over. Whether it is worth it depends on whether the old game still has players and whether `c` is above zero.
- **"Once the relaunch ships, the problem is solved."** The relaunch was a launch with a queue, a sales suspension and an apology. Trust took years more. Plan the relaunch as carefully as the first launch.

## Check yourself

1. A game has `G = 250`, `φ = 0.4`, `F = 10`, `T_r = 18`. What is `m*`? The team measures `m = 2.2`. Which path wins, and by how many months?
2. In question 1, the team keeps `s = 0.2` of its people on the old game, and `c = 0.3` of their work carries over. What is the new rebuild time? Does the decision change?
3. A studio's gap is 60% "the monthly fee is too high for what we offer" and 40% content. Which of the section 2 cases is it most like, and what should the studio do first?
4. Explain, using the model's top view, why a rebuild that finishes two months before patching could still lose more players than patching.
5. Name two things Final Fantasy XIV's Legacy Campaign did in the model's terms, and one thing it could not do.

<details>
<summary>Answers</summary>

1. `m* = 18 × 10 / (0.4 × 250) = 1.8`. `T_patch = 250 × (0.4 × 2.2 + 0.6) / 10 = 250 × 1.48 / 10 = 37` months. `T_rebuild = 18 + 0.6 × 250 / 10 = 33` months. The rebuild wins by 4 months.
2. Build `= 18 / 0.8 = 22.5` months. Carried `= 0.3 × 0.2 × 10 × 22.5 = 13.5` units. Rest `= 150 − 13.5 = 136.5` units, 13.65 months. Total 36.15 months. Patching takes 37, so the rebuild still wins, now by less than a month. A small error in `T_r` would flip it.
3. The Elder Scrolls Online. The pricing part has no engineering cost, so neither path in the model touches it. Change the business model first, then decide on the 40% content gap, which is a patch job.
4. The rebuild shows players no improvement for the whole build phase, while patching improves the game every month. If players leave at a rate that depends on how the game looks now, more of them leave during the flat part of the rebuild line. The model finishes on the team's clock. Players leave on theirs.
5. It kept players paying during the rebuild (it raised the base the relaunch would start with), and it tied them to the new game with rewards they could only use there. It could not shorten `T_r` or close the trust gap on its own.

</details>

## Lab / assignment hook

[Lab 04, patch or rebuild](../labs/lab04.md). You implement the section 2 and 3 model with a month-by-month gap simulator, reproduce the tables, add a player-retention term that makes players leave faster while the visible game stays bad, and find the value of `s` that maximizes players at relaunch. Then you write a 600-word case analysis of one other relaunch (The Elder Scrolls Online or No Man's Sky) with the model's parameters estimated from the public record. The case analysis counts toward the course's case-analysis grade.

## Sources

- Wikipedia, "Final Fantasy XIV (2010 video game)" (read September 2026). Collector's edition early access 22 September 2010, launch 30 September 2010; Metacritic 49 from 26 reviews; free trial extended twice; Tanaka and Komoto removed in December 2010 and Yoshida appointed; subscriptions suspended; PS3 version postponed; Crystal Tools engine judged unsuitable; engine and server structure critically flawed; reboot chosen over scrapping to regain trust; reduced fees reintroduced with bonuses; server merges and negative reaction; final revision 1 November 2012 and shutdown 11 November 2012 after a final battle; Wada's apology at Tokyo Game Show 2011.
- Wikipedia, "Final Fantasy XIV" (read September 2026), development and release sections. Planning for a new game from January 2011 and development from April; patch 1.18 in July 2011 (battle changes, auto-attack, instanced dungeons, fatigue removed); "Version 2.0" announced October 2011; billing from January 2012; the Legacy Campaign (at least three months paid, permanently reduced fee, exclusive chocobo mount, name in the version 2.0 credits); Yoshida's 2012 comment that Square Enix's engines were optimized for offline games; four beta phases from February 2013 and the "until it is ready" statement; early access 24 August 2013, launch 27 August 2013; server problems, temporary suspension of digital sales, apology, ten-hour maintenance and a week of free play; Wada on delays to other titles; over 24 million registered players by October 2021; return to profitability in 2014.
- Yoshida, N. "Behind the Realm Reborn." GDC 2014, GDC Vault, https://gdcvault.com/play/1020179/Behind-the-Realm. Summarized in the Wikipedia development section: two years and eight months of maintaining one MMO while developing another; three causes of the 2010 failure; about 400 fundamental design decisions; the new workflow tested on version 1.0 updates.
- Kollar, P. "Final Fantasy 14 killed by Square Enix's stubbornness, reborn by a new approach." Polygon, 20 March 2014. Report of the GDC 2014 talk.
- Gifford, K. "The death and rebirth of Final Fantasy 14." Polygon, 21 November 2012.
- Spolsky, J. "Things You Should Never Do, Part I." Joel on Software, 6 April 2000. https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/. Netscape's gap of nearly three years between version 4.0 and the 6.0 beta; the argument that old code holds accumulated fixes.
- Wikipedia, "Netscape 6" (read September 2026). Release on 14 November 2000; judged too unstable at release.
- Wikipedia, "No Man's Sky" (read September 2026). Release in August 2016 (PS4 9 August); free updates beginning with Foundation in November 2016; multiplayer added with the Next update in 2018.
- Wikipedia, "The Elder Scrolls Online" (read September 2026). Release on 4 April 2014 with a mandatory subscription; mixed reviews; relaunch as Tamriel Unlimited, subscription no longer required from 17 March 2015; improved reception.
- The gap sizes, capacities, rebuild times, penalties and carry-over shares in sections 2 and 3 and the activity are invented teaching values. The model is this course's simplification, not a formula from the sources.

## Interactive spec: examples/w04-patch-or-rebuild.html

**The one insight:** a rebuild beats patching only when the structural share of the gap, times the penalty the old code puts on structural fixes, outweighs the rebuild time. Even when the rebuild finishes first, it shows players nothing until it lands.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the gap over time": x axis months 0 to 90, y axis remaining gap in fix-units 0 to `G`. Line 1 (patch, `--steel`): `gap_patch(t) = G × max(0, 1 − t / T_patch)`. Line 2 (rebuild, `--moss`): flat at `G` for `0 ≤ t < build`, then at `t = build` it drops to `max(0, (1 − φ) × G − carried)`, then falls at `F` per month to 0. A thin dashed third line (`--ink-soft`) appears when `s > 0`, "what players of the old game see": `gap_old(t) = G − (s × F / (φ × m + 1 − φ)) × t` until `build`, then it ends with a marker "old servers close". Mark each path's finish time with a vertical tick and its value. Shade the region where the rebuild line is above the patch line in pale `--blood` and label it "players see more progress on the patch path".
- View B, "the decision map": x axis `φ` from 0.05 to 0.95, y axis `m` from 1 to 6. Draw the curve `m*(φ) = T_r × F / (φ × G)` (clipped to the plot). Shade above it `--moss` pale, "rebuild faster"; below `--steel` pale, "patch faster". A dot at the current `(φ, m)`; the dot's color matches the faster path. The dot is draggable (pointer and arrow keys), and dragging it updates the `φ` and `m` sliders.

**Controls:**

- `G` slider 100 to 600, step 10 (default 300).
- `F` slider 4 to 20, step 1 (default 10).
- `T_r` slider 6 to 60 months, step 1 (default 24).
- `φ` slider 0.05 to 0.95, step 0.05 (default 0.5).
- `m` slider 1.0 to 6.0, step 0.1 (default 4.0).
- `s` slider 0 to 0.5, step 0.05 (default 0), and `c` slider 0 to 1, step 0.1 (default 0). `c` is disabled when `s = 0`.
- Preset buttons: "A, surface problems" (φ 0.1, m 3), "B, deep but cheap" (φ 0.5, m 1.5), "C, deep and taxing" (φ 0.5, m 4), "C, run both" (φ 0.5, m 4, s 0.25, c 0.5). Each preset resets G 300, F 10, T_r 24.
- "Pad T_r by 50%" toggle: multiplies the current `T_r` by 1.5 while on.

**Readout (always visible, `aria-live="polite"`):** `T_patch`, `T_rebuild`, `m*`, the faster path and its margin in months, build months, carried units, and the months during which the rebuild line is above the patch line.

**Formulas:**

```
T_patch   = G × (φ × m + 1 − φ) / F
build     = T_r / (1 − s)
carried   = c × s × F × build
T_rebuild = build + max(0, (1 − φ) × G − carried) / F
m*        = T_r × F / (φ × G)
months rebuild line above patch line = min(build, T_patch) plus any later interval where gap_rebuild(t) > gap_patch(t); compute numerically at 0.1-month steps
```

**Test values (must match):**

- Preset A: `T_patch = 36.0`, `T_rebuild = 51.0`, `m* = 8.00`, patch faster by 15.0.
- Preset B: `T_patch = 37.5`, `T_rebuild = 39.0`, `m* = 1.60`, patch faster by 1.5.
- Preset C: `T_patch = 75.0`, `T_rebuild = 39.0`, `m* = 1.60`, rebuild faster by 36.0.
- C with `s = 0.25`, `c = 0`: build 32.0, `T_rebuild = 47.0`.
- "C, run both": build 32.0, carried 40.0, `T_rebuild = 43.0`.
- C with `T_r` padded to 36: `m* = 2.40`, `T_rebuild = 51.0`, rebuild still faster.
- `G = 400, φ = 0.3, F = 10, T_r = 30, m = 2`: `T_patch = 52.0`, `T_rebuild = 58.0`, `m* = 2.50`.

**First screen:** preset C, with the flat rebuild line and the shaded region visible, and the caption "The rebuild finishes 36 months sooner, and shows players nothing for 24 months. Drag m down and watch the answer flip at 1.6."

**Accessibility:** all controls keyboard operable with visible focus; the draggable dot also moves with arrow keys (φ by 0.05, m by 0.1); readout in `aria-live="polite"`; the shaded region also described in text; respects `prefers-reduced-motion` (no animated line transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art, logos or screenshots.
