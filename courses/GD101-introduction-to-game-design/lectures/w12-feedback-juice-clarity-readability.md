# GD101 · Week 12 — Feedback: Juice, Clarity, Readability

**Why this matters:** Players can only respond to what they notice in time. A boss attack that is fair in a quiet test room becomes "cheap" once the screen fills with sparks, and a rule players never see working might as well not exist. Feedback is how your game tells players what happened and what is about to happen, and you can budget it in milliseconds.

**You will be able to:**
- Name the three jobs of feedback (confirm, report, forecast) and identify which one a given effect does.
- Compute the time a player needs to react to a warning, from reaction time, number of possible warnings, action start-up and display lag, and decide whether a warning is fair.
- Predict how adding attack types or screen effects changes that budget, and design a warning that fits it.
- Critique a screen or a paper-prototype card for readability, using hierarchy, consistency and redundancy.

**Before class:** Steve Swink, *Game Feel* (2008), the opening chapter on what game feel is. Watch Martin Jonasson and Petri Purho, "Juice It or Lose It" (GDC Europe 2012), and Jan Willem Nijman, "The Art of Screenshake" (INDIGO Classes 2013). Bring a 30 cm ruler.

**Prerequisites from earlier courses:** None outside GD101. From this course, [week 7's playtesting method](w07-playtesting-observe-dont-explain.md), [week 9's discernability test](w09-choice-and-meaningful-decisions.md), and week 11's [dominant strategies](w11-dominant-strategies-and-how-to-spot-them.md) (an option nobody picks may be dead, or may just be unclear). If you want the math of animation curves behind "feel", MA101 covers [easing curves for animation feel](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w09-easing-curves-for-animation-feel.md).

**Interactive:** [The telegraph budget](../examples/w12-telegraph-budget.html). Keep it open during section 2.

---

## 1. The three jobs of feedback

In this lecture, **feedback** means any signal the game sends back to the player: a sound, a flash, a number, a card flipped face up, a token moved. (Next year GD102 uses "feedback loop" for something different, a system that feeds its output back into itself. Same word, different idea.)

Every piece of feedback does one or more of three jobs.

1. **Confirm.** "I heard you." The button clicks, the character starts to swing, the card is placed with a snap. Confirmation tells players their input registered. Without it they press again, or they assume the game is broken.
2. **Report.** "Here's what happened." The damage number, the enemy staggering, the score going up, the opponent's card revealed. Reports tell players the consequence of their choice, which is how they learn.
3. **Forecast.** "Here's what's about to happen." The enemy winding up, the cast bar filling, the fuse burning, the countdown to the end of the round. Forecasts let players decide before the consequence lands. Designers usually call a forecast of an enemy action a **telegraph**.

Each job has its own timing rule.

Confirmation must be fast. Usability research going back to Robert Miller (1968) and Card, Robertson and Mackinlay (1991) puts the limit for a response that feels instant at about 0.1 seconds. Jakob Nielsen's summary of that research names it as the first of three response-time limits. Past that, players feel a gap between pressing and seeing. At 60 frames per second, 0.1 seconds is 6 frames, and the game, the controller and the screen all take a share of those frames.

Reports must be unmistakable. A report the player misses teaches nothing. If players can't tell whether an attack hit, they can't tell whether their choice was good, and week 10 showed how much noise already slows learning.

Forecasts must be early enough. This is the job with the tightest math, and the worked example is about it.

## 2. Worked example: the telegraph budget

### The hook

In World of Warcraft, enemy spells show a cast bar that fills while the spell is being cast. Players with an interrupt ability can stop the cast before it finishes. The game draws casts that *can't* be interrupted differently: a silver bar with a shield around the spell icon, instead of the colored bar used for interruptible casts. Why would a design team spend a whole visual style on a message that amounts to "don't bother"?

Because deciding takes time, and the time depends on how many things you have to tell apart. If every cast bar might or might not be interruptible, a player must identify the spell, remember whether it can be stopped, and then act. The shield lets them skip a step. It turns a harder decision into an easier one, and that buys back reaction time. You can put a number on it.

### The model

A telegraph is fair if the player has enough time between the moment the warning becomes visible and the moment the attack lands to notice it, decide what to do, and do it. Write that as a budget:

```
T_needed = a + b × log2(n) + t_act + t_lag + t_hidden
fair if  T_telegraph ≥ T_needed
margin = T_telegraph − T_needed
```

- `T_telegraph` is the warning time: from when the telegraph starts until the attack hits.
- `a` is the **simple reaction time**: how long it takes to respond to one known signal. Lab studies of college-age people put the average for a visual signal at roughly 190 milliseconds. We round to `a = 200 ms`.
- `b × log2(n)` is the **choice cost**. `n` is the number of different warnings the player must tell apart, each needing a different response. The Hick-Hyman law (Hick 1952, Hyman 1953) found that choice time grows with the logarithm of the number of choices: each doubling of `n` adds the same fixed amount `b`. The value of `b` depends on the person and the task, and published fits vary. **For this lecture we assume `b = 150 ms` per doubling.** You will measure your own in the in-class activity.
- `t_act` is the **action start-up**: the time from pressing the button until the dodge or block actually protects the character. We use 4 frames at 60 fps, `t_act = 4 × 16.7 = 67 ms`.
- `t_lag` is the **display and input lag**: time for the controller, the game and the screen to turn a press into pixels. It varies by hardware; we assume `t_lag = 50 ms` (3 frames at 60 fps).
- `t_hidden` is the time the telegraph is visible on screen but covered by other effects: a flash, a burst of particles, a big shake. Until the player can see the warning, their reaction clock hasn't started. Default 0.

Notice what this model says and doesn't say. The numbers are assumptions you should replace with measurements from your own game and players. The structure is the lesson: warning time is spent on four things, and variety (`n`) and visual noise (`t_hidden`) are two of them.

### Numbers you can check

With `a = 200`, `b = 150`, `t_act = 67`, `t_lag = 50`, all in milliseconds. `log2(n)` is 0 for one warning, 1 for two, 2 for four, 3 for eight. For three and six, use `log2(3) = 1.585` and `log2(6) = 2.585`. The "frames" column converts to 60 fps and rounds up.

| Distinct warnings n | Choice cost b·log2(n) | T_needed, clear screen | Frames at 60 fps | T_needed with 150 ms hidden | Frames |
|---|---|---|---|---|---|
| 1 | 0 | 317 ms | 19 | 467 ms | 28 |
| 2 | 150 | 467 ms | 28 | 617 ms | 37 |
| 3 | 238 | 554 ms | 34 | 704 ms | 43 |
| 4 | 300 | 617 ms | 37 | 767 ms | 46 |
| 8 | 450 | 767 ms | 46 | 917 ms | 55 |

Check one row by hand. `n = 4`: `200 + 150 × 2 + 67 + 50 = 617 ms`. Divide by 16.7 ms per frame: 37 frames.

Now use it. Your boss has a 30-frame (500 ms) windup on every attack.

- With **two** attack types (one you dodge left, one you dodge right), the budget is 28 frames. Margin: +2 frames, about 33 ms. Tight but fair.
- Add two more attack types for variety: `n = 4`, budget 37 frames. Margin: −7 frames. Players now get hit by attacks they "should" have dodged, and they'll call it cheap.
- Keep two attack types but add a 150 ms hit flash that covers the boss whenever the player lands a blow: budget 37 frames. Same −7 frames, from a completely different cause.

The last two rows are the surprise. Adding variety and adding juice cost the same currency. Both come out of the telegraph.

### A visual you can move

Open [`examples/w12-telegraph-budget.html`](../examples/w12-telegraph-budget.html). The top view is a horizontal timeline for one attack. A bar shows the telegraph window, and under it a stacked bar shows the budget: reaction (a), choice cost (b·log2 n), hidden time, start-up and lag, each a different segment. When the stack is longer than the telegraph, the overflow turns red and the verdict reads "unfair by N frames". The bottom view plots `T_needed` against `n` from 1 to 8, with a horizontal line at your telegraph length. Drag the "distinct warnings" slider from 2 to 4 and watch the stack cross the line. Then set it back to 2 and drag "hidden by effects" up to 150 ms. The same crossing happens. That is the one thing to take away: variety and visual noise are paid from the same fixed budget.

### Cross-game recognition

**World of Warcraft cast bars.** A cast bar is a telegraph with its clock drawn on screen, so players can see `T_telegraph` shrink. The silver bar and shield on uninterruptible casts removes one decision ("can I stop this?") from every cast, which lowers the effective `n`. Colored bars for interruptible casts and a changed bar for the rest also mean players don't have to read the spell name, which lowers `a` for experienced players. The design adds information in order to reduce thinking.

**Guitar Hero's note highway.** In Guitar Hero, colored gems travel down the screen toward a strike line in time with the music, and each gem's color and position match one of the five fret buttons. The distance a gem travels before it reaches the line is a telegraph. The five frets are `n = 5` possible responses, and chords make it more. Rhythm games are telegraph budgets turned into the whole game: the difficulty lies in how many notes arrive and how early you can see them.

**Team Fortress 2 silhouettes.** Valve's artists wrote that a key gameplay goal was letting players identify each other quickly during fast action, and they designed the nine classes with distinct silhouettes that can be told apart even without lighting cues (Mitchell, Francke and Eng, 2007). In our model, a player seeing an enemy must first identify which of nine classes it is, `n = 9`. A silhouette that can be read at a glance keeps that step fast, so the choice cost doesn't eat the whole budget. The art style is a reaction-time decision.

**Traffic lights.** Outside games, the amber light is the same model. Drivers must see the change, decide between stopping and continuing, and then act. The UK fixes amber at three seconds and the US uses at least three seconds. A driver who can't see the light because of glare is `t_hidden`, and a junction with several confusing signals raises `n`.

Four places, one budget. Wherever a player must react to a warning, ask what the warning time is spent on.

### Eyes-open design judgment

- **Telegraphs are a difficulty dial, and a fair one.** Shortening a telegraph makes a game harder in a way players accept, as long as the budget is still met for skilled players. Making attacks deal more damage without longer telegraphs just makes the game punishing.
- **Variety has a price.** Each new attack type raises `n` for every attack. If you add types, make them share responses (three attacks that all mean "dodge left" count as one for `n`) or give them longer windups.
- **Learning lowers the budget.** Hick-Hyman costs fall with practice, because familiar warnings are recognized faster. That's why the first encounter with a boss feels unfair and the tenth feels fine. Design early encounters with extra margin.
- **Juice and warnings must not collide.** Effects that fire when the player acts (hits, kills) tend to land right when the next warning appears. Keep warnings visible through effects: draw them on top, give them a color no effect uses, or dim effects during a windup.
- **The model's numbers are placeholders.** Replace `a`, `b`, `t_act` and `t_lag` with your platform's and your players' measured values. Players with slower reactions, older hardware or a TV in game mode need more margin; accessibility options that lengthen telegraphs or reduce effects are cheap ways to give it.

### Check yourself (worked example)

1. An enemy has three attacks, each needing a different response, and a 36-frame windup. Using the lecture's assumptions, is it fair on a clear screen? With 150 ms hidden?
2. A designer wants six distinct attacks on a clear screen. How many frames of windup does each need, at minimum?
3. A team changes their dodge so it protects from frame 1 instead of frame 4 (start-up 1 frame instead of 4). How many frames of telegraph does that save for every attack?

<details>
<summary>Answers</summary>

1. `n = 3`: budget 554 ms, 34 frames. 36 ≥ 34, fair with a 2-frame margin. With 150 ms hidden: 704 ms, 43 frames, unfair by 7 frames.
2. `T_needed = 200 + 150 × 2.585 + 67 + 50 = 704 ms`, which is 42.2 frames, so 43 frames at minimum.
3. Start-up drops from 67 ms to 17 ms, saving 50 ms, which is 3 frames.

</details>

## 3. Juice: amplifying the signal

**Juice** is the name designers use for extra, non-essential feedback that makes actions feel satisfying: screen shake, particles, flashes, a sound with a crunch, a tiny freeze on impact (often called **hit-stop**), a squash-and-stretch on a bouncing object. Jonasson and Purho's talk made the term popular by starting with a plain block-breaking game and adding effects one at a time until the same rules felt alive. Nijman's talk on screenshake did the same for a shooter, showing how many small effects add up to a feeling of power.

Juice isn't decoration for its own sake. Look at it through the three jobs:

- A tiny delay-free shake when the player fires **confirms** the input.
- Particles and a knockback when an enemy is hit **report** the result, with size matched to damage.
- A glow that builds on a charged attack **forecasts** its release.

Good juice amplifies information the player needs, in proportion to how much it matters. The biggest effect should go to the biggest event. The problem starts when effects stop carrying information:

- **Uniform juice is noise.** If every hit shakes the screen equally, the shake no longer tells players which hit mattered.
- **Juice can hide warnings.** That's the `t_hidden` term. Flashes and particles land right when the player acts, which is exactly when the next enemy telegraph may start.
- **Juice can hurt players.** Heavy shake and flashing can cause motion sickness or discomfort, and some people are sensitive to flashing light. Offer options to reduce shake and flashes, and test your effects with that in mind.
- **Juice can hide bad design, for a while.** A satisfying hit effect makes a dull decision more pleasant for the first few minutes. Playtest with juice turned off at least once to see whether the choices hold up on their own.

The animation curves that make movement feel snappy or heavy, ease-out on a hit and anticipation before a swing, are covered in [MA101 week 9](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w09-easing-curves-for-animation-feel.md). A windup with an anticipation pose is both juice and telegraph at once, which is why fighting game characters rear back before a heavy blow.

## 4. Clarity and readability

**Clarity** means the player can tell what a signal means. **Readability** means they can tell it quickly, at a glance, under pressure. Four habits get you most of the way.

**Hierarchy.** Decide what matters most on the screen or the table at any moment, and make it the loudest thing: biggest, brightest, most contrasting, most central. Health when you're about to die. The enemy's windup. The card in play. Everything else steps back. A quick test: squint at a screenshot or step back from the table until detail blurs. What's left is what players notice first. If it's the background art, the hierarchy is wrong.

**One meaning per signal.** If red means "damage" in one place and "rare item" in another, every red thing costs a decision. Keep a small dictionary of signals (colors, sounds, icon shapes) and don't reuse entries for different meanings.

**Consistency.** The same event should always look and sound the same. Consistency is what lets practice drive the Hick-Hyman cost down: players learn a signal once and then recognize it instantly. An exception ("this boss's red attack is actually safe") costs every player a failure before they learn it.

**Redundancy.** Carry important information in more than one channel: color *and* shape, sound *and* animation, icon *and* position. Guitar Hero's gems do this with color and lane position. It helps everyone under pressure and it's essential for players who can't perceive one channel. The Web Content Accessibility Guidelines state the same principle for interfaces: never use color as the only way to convey information. Among people of Northern European descent, as many as 8% of men and about 0.5% of women have red-green color deficiency, so a red-versus-green distinction alone will fail a noticeable share of your players.

### The same ideas on paper

You're building a paper prototype, and every one of these habits applies at the table.

- **Card hierarchy.** The number players need every turn goes in a corner, large, where it's visible when cards are fanned in a hand. Rules text goes smaller, lower.
- **Feedback on paper is physical.** A token moved, a card flipped, a die placed on a track. If a rule changes the game state without anything moving, players forget it. Give every state change a physical action.
- **Forecasts on paper.** A face-up "next event" card, a countdown track, a revealed intent. Board games telegraph too, and a player who is surprised by something that was hidden in a rule booklet feels as cheated as one hit by an unreadable boss.
- **The one-second glance test.** Show a new player the board mid-game for one second and ask who is winning. If they can't tell, your game's most important state isn't readable.

## In-class activity (25 minutes)

Pairs. You need a 30 cm ruler, paper and a pen.

1. **Measure a (8 minutes).** One partner holds the ruler vertically, zero end at the bottom, just between the other's open thumb and finger. Without warning, they drop it; the catcher grabs it as fast as possible. Record the catch distance `d` in centimeters. The fall time is `t = √(2d / 980)` seconds (from `d = ½ g t²`, with `g = 980 cm/s²`). A 20 cm catch is `√(40/980) = 0.202 s`. Do five catches each and take the median.
2. **Measure the choice cost (8 minutes).** Repeat, but the dropper now holds a red or blue card up at the moment of release, and the catcher must catch only on red. Blue drops are allowed to fall. This is `n = 2`. The difference between the median catch time here and in step 1 is your personal estimate of `b`. Compare with the lecture's assumed 150 ms, and don't be surprised if yours is different; that's the point of measuring.
3. **Re-budget (5 minutes).** Put your own `a` and `b` into the model. For a 30-frame telegraph, what is the largest `n` that is still fair for you?
4. **Pool (4 minutes).** Collect every pair's `a` and `b` on the board. What's the range? What telegraph length would be fair for the slowest quarter of the class with `n = 4`?

Expected output: a table of five catches per condition, your estimates of `a` and `b`, and a one-line answer to step 4.

## Common misconceptions

- **"More juice always feels better."** Juice makes events feel stronger by contrast. When everything shakes, nothing does, and effects start hiding the warnings players need.
- **"If players get hit, they should just react faster."** Below the budget, no amount of practice helps; the warning is shorter than human perception plus the game's own lag. Measure before blaming players.
- **"Clear means simple."** A screen can show a lot and still be readable if its hierarchy is strong. Readability is about how fast the important part is found, not how few things are shown.
- **"Feedback only matters in video games."** A paper game with hidden state changes and no forecasts has the same problems: forgotten rules, surprise losses and players who can't tell who is winning.

## Check yourself

1. Classify each effect by job (confirm, report, forecast): (a) a coin sound when you pick up gold; (b) a red circle that appears on the ground where a meteor will land; (c) a button that visibly depresses when clicked; (d) "Critical!" text over a large hit.
2. Using the lecture's assumptions, a boss with `n = 2` has a 32-frame telegraph. Your artist wants to add a hit flash that hides the boss for some of the telegraph. What is the longest the flash can hide the boss, in milliseconds, before the telegraph becomes unfair?
3. A team makes three of their boss's four attacks share the same correct response (dodge backward), and the fourth needs a jump. What is the new `n`, and how many frames of budget does it save compared with four distinct responses?
4. Your paper prototype's players keep forgetting that the "storm" rule reduces everyone's movement by one after round 5. Propose two changes, one for forecast and one for report.

<details>
<summary>Answers</summary>

1. (a) Report (and confirm the pickup). (b) Forecast. (c) Confirm. (d) Report.
2. Budget with nothing hidden, `n = 2`: 467 ms. Telegraph: 32 frames × 16.7 = 533 ms. The flash can hide at most `533 − 467 = 66 ms`, about 4 frames.
3. Two distinct responses, so `n = 2`. Budget drops from 617 ms (37 frames) to 467 ms (28 frames), saving 150 ms or 9 frames.
4. Forecast: a round track with a storm icon printed on round 5, so players see it coming. Report: from round 5, place a storm token on every player's movement stat, or flip a card over the board showing "movement −1". Either change gives the rule a physical presence.

</details>

## Lab hook

**Lab 12: Feedback and readability pass.** You audit your paper prototype for the three jobs of feedback, run the one-second glance test and a squint test with outside players, redesign one card or board element for hierarchy and redundancy, and give every state change a physical action. The deliverable is a before-and-after comparison and a short playtest report. See [labs/lab12.md](../labs/lab12.md).

## Sources

- Warcraft Wiki (warcraft.wiki.gg), "Interrupt" (current retail era, accessed September 2026): interrupts cancel casts; interruptible abilities show a colored cast bar; uninterruptible ones show a silver cast bar with a shield around the icon.
- Wikipedia, "Guitar Hero": colored gems travel down the screen in time with the music and match the five fret keys by color and position.
- Mitchell, J., Francke, M. & Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." *Proceedings of the 5th International Symposium on Non-Photorealistic Animation and Rendering (NPAR 2007)*, ACM, doi:10.1145/1274871.1274883 (title, venue and authors checked against Crossref and Valve's publications page). Summarized on the Official TF2 Wiki, "Art style": nine classes with distinct silhouettes readable without lighting cues, to support quick identification during fast action.
- Wikipedia, "Color blindness": red-green deficiency in up to 8% of men and about 0.5% of women of Northern European descent.
- Wikipedia, "Traffic light": amber fixed at three seconds in the UK; the US uses a minimum of three seconds.
- Nielsen, J. "Response Times: The 3 Important Limits." Nielsen Norman Group (accessed September 2026). Cites Miller (1968) and Card, Robertson & Mackinlay (1991) for the 0.1 s, 1 s and 10 s limits.
- Wikipedia, "Mental chronometry": mean simple visual reaction time of roughly 190 ms for college-age people.
- Hick, W. E. (1952). "On the rate of gain of information." *Quarterly Journal of Experimental Psychology*. Hyman, R. (1953). "Stimulus information as a determinant of reaction time." *Journal of Experimental Psychology*. Via Wikipedia, "Hick's law": choice time grows with the logarithm of the number of choices; the slope is fitted empirically.
- Jonasson, M. & Purho, P. (2012). "Juice It or Lose It." GDC Europe 2012 (GDC Vault).
- Nijman, J. W. (2013). "The Art of Screenshake." INDIGO Classes 2013 (recorded talk, Vlambeer).
- Swink, S. (2008). *Game Feel: A Game Designer's Guide to Virtual Sensation*. Morgan Kaufmann.
- W3C, WCAG 2.1, Success Criterion 1.4.1 "Use of Color": color must not be the only visual means of conveying information.
- The values of `b = 150 ms`, `t_lag = 50 ms` and a 4-frame dodge start-up are teaching assumptions, not measurements from any game.

## Interactive spec: examples/w12-telegraph-budget.html

**Purpose.** Let students see the time budget of a telegraphed attack and how variety and screen effects spend it.

**The one insight the visual must make obvious.** Adding attack types (raising `n`) and adding effects that hide the warning (raising `t_hidden`) push the same stacked bar past the same line; both are paid from one fixed telegraph.

**Layout.** Two stacked views, full width on both desktop and 390px.

- Top, "One attack": a horizontal timeline in milliseconds from 0 to 1,200. A light bar from 0 to `T_telegraph` labeled "telegraph (N frames)", ending in a marker "attack lands". Below it, a stacked bar starting at 0 with segments in this order: hidden by effects `t_hidden` (hatched), reaction `a`, choice cost `b·log2(n)`, start-up `t_act`, lag `t_lag`. Each segment labeled with its value in ms when wide enough, and listed in a legend with values otherwise. The part of the stack past `T_telegraph` is drawn in the palette's negative color with a label. A verdict line: "Fair, margin +M ms (F frames)" or "Unfair by M ms (F frames)", where frames use the current fps and round toward the safe side (ceil for the needed time).
- Bottom, "Budget vs variety": x axis `n` from 1 to 8 (integer ticks), y axis ms from 0 to 1,200. Plot `T_needed(n)` as a line with dots for the current settings. A horizontal line at `T_telegraph`. Shade the region where the line is above the telegraph. Highlight the dot for the current `n`. If `t_hidden > 0`, draw a faint second line for `t_hidden = 0` so students see the shift.

**Controls** (keyboard accessible, values printed):

- Telegraph length: slider 10 to 72 frames, step 1, default 30. Show both frames and ms.
- Frame rate: segmented 30 / 60 / 120 fps, default 60. Changing it keeps the telegraph in frames and recomputes ms, so students see that a 30-frame windup is twice as long at 30 fps.
- Distinct warnings `n`: slider 1 to 8, default 2.
- Hidden by effects `t_hidden`: slider 0 to 300 ms, step 10, default 0.
- Reaction `a`: slider 150 to 350 ms, step 5, default 200.
- Choice cost per doubling `b`: slider 50 to 250 ms, step 5, default 150.
- Action start-up: slider 0 to 12 frames, default 4.
- Lag: slider 0 to 150 ms, step 5, default 50.
- Preset buttons: "Lecture default", "Add two attack types" (n = 4), "Add a hit flash" (n = 2, t_hidden = 150), "Tutorial boss" (n = 1, telegraph 45 frames).
- Reset button.

**Formulas.**

- Frame time `f = 1000 / fps` ms. `T_telegraph = frames × f`. `t_act = startup_frames × f`.
- `T_needed = t_hidden + a + b × log2(n) + t_act + t_lag`.
- Margin `= T_telegraph − T_needed`. Needed frames `= ceil(T_needed / f − 1e-9)`.

**Test values** (60 fps, a = 200, b = 150, start-up 4 frames, lag 50).

| n | t_hidden | T_needed (ms) | Needed frames | Verdict at 30-frame telegraph |
|---|---|---|---|---|
| 1 | 0 | 316.7 | 19 | Fair, +183.3 ms |
| 2 | 0 | 466.7 | 28 | Fair, +33.3 ms |
| 3 | 0 | 554.4 | 34 | Unfair by 54.4 ms |
| 4 | 0 | 616.7 | 37 | Unfair by 116.7 ms |
| 2 | 150 | 616.7 | 37 | Unfair by 116.7 ms |
| 8 | 0 | 766.7 | 46 | Unfair by 266.7 ms |

At 30 fps with the same settings and n = 2: start-up is 133.3 ms, `T_needed = 533.3 ms`, telegraph 30 frames = 1,000 ms, fair by 466.7 ms.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes. Segments use pattern or label as well as color. Respect reduced motion: no animated attack playback unless the user presses a "Play attack" button, and none at all when reduced motion is set. No game art; the attacker is a plain labeled shape if drawn at all.
