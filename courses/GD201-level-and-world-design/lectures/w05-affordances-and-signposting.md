# GD201 · Week 05 — Affordances and signposting

**Why this matters:** Every stuck player in a playtest is a signposting failure, and every mocking comment about yellow paint is a signposting overcorrection. You need a way to decide how loud your cues should be that is better than taste. This week gives you a model that predicts how many players get lost, and shows why adding more subtle cues often fails to help the players who need it most.

**You will be able to:**
- Distinguish affordances from signifiers, and classify a level element as a true, false, hidden or absent affordance.
- Compute the chance that a player notices at least one signpost on a route, and the number of signposts needed to reach a target.
- Compute the same chance for a mixed population of players, and explain why redundancy of subtle cues can't rescue the least attentive group.
- Design a signpost language for a level and critique a shipped game's signposting with numbers.

**Before class:** Donald Norman, *The Design of Everyday Things* (revised and expanded edition, Basic Books, 2013), chapter 1, the sections on affordances and signifiers. Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 5, the sections "Symbols as Guides," "Contrast" and "Framing." Read the Wikipedia article "Yellow paint in video games" and write down which side of the debate you are on before class. We will revisit your answer at the end.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success in `n` tries is `1 − (1 − p)^n`). [MA102 week 2, independence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md). [UX201 week 1, perception and attention](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) (pop-out search). [GD101 week 12, feedback and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md). From this course, [week 4, landmarks and light](w04-guiding-the-player-landmarks-light-weenies.md). Week 4 handled cues you see from a kilometer away. This week handles the ones you see from ten meters.

**Interactive:** [`examples/w05-signpost-funnel.html`](../examples/w05-signpost-funnel.html). Keep it open during section 2.

---

## 1. What the space allows, and what it says

### Affordances

The psychologist James J. Gibson coined the word **affordance** in the 1960s and gave its best-known definition in *The Ecological Approach to Visual Perception* (1979). An affordance is what the environment offers an animal, for good or ill. A flat, knee-high rock affords sitting. A gap narrower than your shoulders doesn't afford walking through. The affordance belongs to the relation between the thing and the creature, whether or not the creature notices it.

In 1988 Donald Norman brought the word into design with *The Design of Everyday Things*, and used it to mean action possibilities the user can readily perceive. That use spread widely. In the 2013 revised edition he separated two ideas that had got mixed up. **Affordances** determine what actions are possible. **Signifiers** communicate where the action should take place. A door's hinge affords pushing. The flat metal plate at hand height is the signifier that tells you where to push.

Games make this split unusually clean.

- In a game, the **affordance** is set by the rules and collision data. A ledge is climbable because the code tags it climbable. A door opens because it has an open interaction.
- The **signifier** is whatever the player perceives that tells them so: a worn edge, a painted stripe, a rope, a lit handle, a sound.

A **signpost**, in level design, is a signifier placed on purpose to guide the player's route or next action. Every signpost is a signifier. Not every signifier is a signpost. A crate's wooden texture signifies "breakable" whether or not you meant it to guide anyone.

### Four combinations

Cross the two ideas and you get a table every level designer should keep in mind.

| | Signified (player can tell) | Not signified (player can't tell) |
|---|---|---|
| **Afforded** (rules allow it) | True affordance. The painted ledge you can climb. | Hidden affordance. A climbable wall that looks like every other wall. |
| **Not afforded** (rules forbid it) | False affordance. A ledge that looks climbable and isn't. | Correct rejection. A sheer wall that looks sheer. |

Two cells cost you players. A **hidden affordance** on the critical path is how players get stuck. A **false affordance** is how they get angry, because the game taught them a rule and then broke it. Once a player has jumped at three decorative ledges that looked exactly like climbable ones, they stop trusting any ledge, and your true affordances stop working too.

That is the core idea of this lecture. Signposting is a **language**. Each signal must mean one thing everywhere in the game, or the player can't learn it.

## 2. Worked example: how many signposts does a route need?

### The hook

In 2023 Capcom released a remake of Resident Evil 4, and players noticed that ladders, breakable crates and climbable ledges were marked with yellow paint. In 2024 Final Fantasy VII Rebirth drew the same comments about its yellow-painted ledges. Fans of Rebirth released a mod called "No More Yellow Paint" to remove the markers, because the game had no setting to turn them off. The argument even has a name, the **yellow paint debate**. One side calls the paint patronizing and immersion-breaking. The other says that without it, some players get stuck and quit. Kotaku summed the debate up in 2024 as unsolvable. Remove the paint and some players can't finish the game. Keep it and people complain. Add a toggle and you must still design every level to work with the paint off.

Here is the puzzle behind the debate. A designer places a route with several subtle cues: scuffed handholds, a bit of light, a broken railing pointing the way. In the designer's head, with that many cues, nearly everyone should find the way. Then the playtest comes back with one player in four stuck. Why would a route with plenty of cues still lose so many players? And why do studios reach for something as blunt as paint instead of adding a few more subtle cues?

### Model 1: every player is the same

Treat each signpost on a route as a chance for the player to notice the way forward. Define:

- `p` is the chance that a player notices one signpost, and acts on it, as they pass.
- `n` is the number of signposts on the route before the player would give up or wander off.

If each signpost is noticed independently of the others, the complement rule from MA102 week 3 gives the chance the player finds the route:

```
P(find) = 1 − (1 − p)^n
```

The player gets lost only by missing every signpost, and that chance is `(1 − p)^n`. To reach a target chance `T`, solve for `n` with logarithms:

```
n = ln(1 − T) / ln(1 − p)       (round up)
```

With `p = 0.3`, a fairly subtle cue:

| Signposts `n` | P(find) with `p = 0.3` |
|---|---|
| 1 | 30.0% |
| 2 | 51.0% |
| 3 | 65.7% |
| 5 | 83.2% |
| 9 | 96.0% |
| 12 | 98.6% |

And the number of signposts needed for 95% at different `p`:

| Notice chance `p` | Signposts for 95% |
|---|---|
| 0.1 | 29 |
| 0.2 | 14 |
| 0.3 | 9 |
| 0.5 | 5 |
| 0.7 | 3 |
| 0.9 | 2 |

This model says redundancy works. Nine subtle cues do the job of two loud ones. If the model were right, you would never need yellow paint. You would add more scuffed handholds. The playtest says otherwise, so something in the model is wrong.

### Model 2: players differ

The wrong assumption is that every player has the same `p`. They don't. A player who is scanning the environment, looking for the way forward, notices most cues. A player who is focused on something else (a fight that just ended, a conversation, a collectible) notices few of them. Call them **scanners** and **tunnelers**. The labels describe a state more than a personality. The same player can be either, depending on the moment.

A single player's misses are not independent of each other. If a player missed the first cue because they were tunneling, they are likely to miss the second one for the same reason. Model this with a population of groups, each with its own `p`, and apply the complement rule within each group:

```
P(find) = Σ  share_g × (1 − (1 − p_g)^n)
```

Take 70% scanners with `p = 0.5` and 30% tunnelers with `p = 0.05`. The average `p` is `0.7 × 0.5 + 0.3 × 0.05 = 0.365`. A designer who measured that average and plugged it into model 1 would predict one thing. The two-group model predicts another.

### Numbers you can check

| Signposts `n` | Scanners find | Tunnelers find | Two groups | Model 1 at `p = 0.365` |
|---|---|---|---|---|
| 1 | 50.0% | 5.0% | 36.5% | 36.5% |
| 3 | 87.5% | 14.3% | 65.5% | 74.4% |
| 5 | 96.9% | 22.6% | 74.6% | 89.7% |
| 9 | 99.8% | 37.0% | 81.0% | 98.3% |
| 20 | 100.0% | 64.2% | 89.2% | 100.0% |
| 40 | 100.0% | 87.1% | 96.1% | 100.0% |

Read across the row for `n = 9`. Model 1 says 98.3% of players find the route. The two-group model says 81.0%. Nearly one player in five is lost, and almost all of them are tunnelers. Model 1 says you need 7 signposts for 95%. The two-group model says 35.

The reason is visible in the columns. Scanners are saturated by `n = 5`. Every extra subtle cue after that helps only tunnelers, and each one helps them by 5%. You are paying for thirty extra cues to rescue a group that barely sees them.

Now add one **loud** signpost, a cue so salient that everyone notices it with `p = 0.9`, scanners and tunnelers alike. On its own it gets 90% of players through. Put it on a route with three subtle cues and the total is `1 − (0.7 × 0.1 × 0.5³ + 0.3 × 0.1 × 0.95³) = 96.6%`. One loud cue does more than 30 quiet ones.

That's the yellow paint debate in two lines. Subtle cues fix the average. Only a salient cue fixes the tail. The Python below prints the table and both targets.

```python
import math

def find_chance(p, n):
    return 1 - (1 - p) ** n

def mixture(n, groups):
    return sum(share * find_chance(p, n) for share, p in groups)

groups = [(0.7, 0.5), (0.3, 0.05)]      # (share of players, notice chance per signpost)
p_avg = sum(share * p for share, p in groups)
print(f"average p = {p_avg:.3f}")
for n in (1, 3, 5, 9, 20, 40):
    print(f"n = {n:>2}  naive {find_chance(p_avg, n):6.1%}  two groups {mixture(n, groups):6.1%}")
print("signposts for 95% (naive):", math.ceil(math.log(0.05) / math.log(1 - p_avg)))
print("signposts for 95% (two groups):", next(n for n in range(1, 1000) if mixture(n, groups) >= 0.95))
```

It prints `average p = 0.365`, the six rows of the table, then 7 and 35.

### Why the tunneler's `p` is so low, and why paint fixes it

UX201 week 1 introduced two kinds of visual search. In **pop-out** search, a target that differs in one basic feature (color, brightness, motion, size) is found in roughly constant time however much clutter surrounds it. In **item-by-item** search, the player must inspect things one at a time. A scuffed handhold on a detailed rock wall needs item-by-item search. You find it only if you are looking. A bright yellow stripe on that wall pops out. You see it even when you are thinking about something else.

In model terms, a subtle cue has a high `p` for scanners and a very low `p` for tunnelers. A pop-out cue has a high `p` for both. That's why the fix is not "more of the same." Adding a pop-out feature changes the tunnelers' `p` directly, and nothing else does that.

### The visual

Open [`examples/w05-signpost-funnel.html`](../examples/w05-signpost-funnel.html). The left view shows a route from left to right with `n` signposts and 100 simulated players as dots. Scanners and tunnelers are drawn with different shapes. Press play and watch the dots walk. At each signpost, some dots turn onto the route and leave the "lost" pool. The right view plots P(find) against `n` for model 1 (average `p`) and model 2 (two groups), with a 95% target line.

Slide `n` up from 3 to 20. On the left, the scanners are gone after a few signposts, and a cluster of tunnelers keeps walking past everything. On the right, the model 1 curve shoots to 100% while the model 2 curve crawls. Then switch on "one loud signpost." The tunneler cluster empties at the loud sign, and the model 2 curve jumps. The two views show the same fact. The gap between the average and the tail is made of tunnelers.

### Cross-game recognition

Every approach to signposting in shipped games is a choice about whose `p` to raise, and at what cost.

**Mirror's Edge (DICE, 2008).** The game's "Runner Vision" turns certain objects bold red as the player approaches, marking paths and escape routes. The city is mostly white, so red is a pop-out feature. In model terms it raises `p` for everyone on the route objects. DICE built the art direction around the signal, so it reads as the world's style rather than paint on top of it.

**Uncharted, Resident Evil 4 (2023) and Final Fantasy VII Rebirth (2024).** Yellow or white paint on ledges, ladders and interactable objects. IGN's Vikki Blake cites Uncharted as an early example. This is the loud signpost from the numbers above, applied to a realistic art style where the paint is visibly foreign to the world. It raises the tunnelers' `p` sharply and costs immersion for scanners, who didn't need it. The "No More Yellow Paint" mod for Rebirth is scanners voting with their feet.

**Horizon Forbidden West (Guerrilla Games, 2022).** Aloy's Focus device highlights climbable surfaces when the player activates it, and Aloy also speaks hints aloud about puzzle solutions. The Focus is a loud signpost on demand. Its `p` is near 1, but only for players who ask, so scanners can leave it off. The spoken hints are an audio channel that reaches tunnelers who aren't looking at the wall. Some critics found the hints too frequent. A fan mod called "Shut Up Aloy" silences them, which is the same scanner reaction as the paint mod, through a different sense.

**The Stanley Parable (2013).** A satirical game in which the narrator tells the player to follow a yellow stripe on the floor. It is the joke version, a route with `p = 1` for everyone and nothing left to find.

Four studios, four settings of one dial. In every case, ask which group's `p` the cue raises, and what it costs the other group.

### Eyes-open design judgment

- **Measure the tail, not the average.** A playtest report that says "on average testers noticed 40% of cues" is model 1 thinking. Count, per tester, how many cues they noticed. If the counts bunch at the top and bottom instead of the middle, you have two groups, and adding subtle cues won't help the bottom group.
- **Put loud signposts where the cost of being lost is high.** A missed optional collectible costs nothing. A missed exit on the critical path costs the player the game. Spend your salient signals on the critical path and keep side routes subtle so scanners still have something to discover.
- **Consider escalation.** A cue that turns loud only after a player has been stuck for a while (a light that brightens, a companion who comments) gives scanners the subtle version and tunnelers the loud one. It targets the tail without taxing everyone. It costs you design and testing time, because the trigger must fire for lost players and not for explorers.
- **A toggle is two levels.** Kotaku's point stands. If you offer "signposting off," you must playtest the level with it off, and it must still be finishable.
- **Integrate the signal into the art direction.** Mirror's Edge's red and yellow paint are the same idea. The difference is that one was part of the world's look from the start and the other was added on top of a realistic one. Decide early.
- **Don't fix a false affordance with a louder signpost.** If players keep jumping at decorative ledges, the problem is the decorative ledges. Remove the false signal before you amplify the true one.

### Check yourself on signposts

1. A route has 4 signposts, each noticed with `p = 0.4` by every player. What fraction of players finds the route? How many signposts would you need for 90%?
2. A playtest suggests 80% scanners with `p = 0.6` and 20% tunnelers with `p = 0.1`. With 4 signposts, what fraction finds the route? What share of the lost players are tunnelers?
3. You add one loud signpost with `p = 0.8` for both groups to the route in question 2. What fraction now finds the route?

<details>
<summary>Answers</summary>

1. `1 − 0.6⁴ = 1 − 0.1296 = 87.0%`. For 90%, `n = ln(0.1) / ln(0.6) = 4.51`, so 5 signposts.
2. Scanners lost `0.8 × 0.4⁴ = 0.0205`. Tunnelers lost `0.2 × 0.9⁴ = 0.1312`. Total lost 15.2%, so 84.8% find it. Tunnelers are `0.1312 / 0.1517 = 86%` of the lost players, though they are only 20% of all players.
3. Every lost player now also has to miss the loud sign, with chance 0.2. Lost becomes `0.2 × 0.1517 = 0.0303`, so 97.0% find the route.

</details>

## 3. Building a signpost language

A signpost language is the set of signals your game uses and what each means. Write it down in the level design document before artists dress a single level.

**Choose channels.** A signal can use several channels, and combining two usually raises `p` more than doubling one. The common ones are these.

- **Shape.** A distinct silhouette for interactable things (a particular ledge profile, a specific handle).
- **Color and value.** A reserved color for one meaning. Week 4's contrast ratio applies here. The cue must differ in brightness from its background, not only in hue, or colorblind players lose it.
- **Light.** A lit doorway, a shaft of light on the path. Week 4 covered why light only works by contrast.
- **Motion.** Fluttering cloth, birds taking off, a swinging sign. Motion is one of the strongest pop-out features.
- **Sound.** A waterfall you hear before you see, a radio playing behind the right door. Sound reaches tunnelers who are looking elsewhere.
- **Composition.** Totten's reading covers framing and the rule of thirds. Arches, rows of pillars and converging lines point the eye.
- **Breadcrumbs.** A trail of small pickups or objects leading along the route. Each is a small signpost, and players follow the trail as much as the objects.

**One signal, one meaning.** If yellow means "climbable," nothing unclimbable may be yellow. That includes decorative props, enemy markings and user interface elements. Audit every level for false affordances once dressing is done, because artists add yellow things for good visual reasons.

**Teach the language before testing it.** Week 1's lesson structure applies. Introduce the signal where the answer is forced (one yellow ledge, nothing else to climb), practise it, then combine it. Players who learn the signal early become scanners for it. You are raising `p` through teaching, which is cheaper than paint.

**Budget pop-out.** UX201 week 1 made the point that pop-out works only when the target is rare. Each extra kind of glowing, colored or moving thing makes every other salient signal less effective. Decide which one or two signals per screen deserve pop-out.

## 4. Measuring `p` in a playtest

The model needs numbers. You get them by watching testers, following the observation rules from GD101 week 7 (don't coach, don't point).

1. Number every signpost on the route.
2. For each tester and each signpost, record whether the tester noticed it. Noticing means a visible response, such as turning toward it, moving to it or using it within a few seconds. Record 1 or 0.
3. For each signpost, `p` is the share of testers who noticed it. For each tester, their notice rate is the share of signposts they noticed.
4. Plot the testers' notice rates as a histogram. One hump means one group, and model 1 is fine. Two humps mean two groups, and you should use model 2 with the hump sizes as shares.

Be careful with small samples. With 8 testers, a signpost noticed by 4 of them has an estimated `p` of 0.5, but the true value could plausibly be anywhere from about 0.2 to 0.8. MA102 week 13 covers why small playtests mislead. Treat each estimate as a range, and prefer decisions that hold across the range.

## 5. Signposting in shared worlds

In an online world, the most powerful signpost is often another player. A newcomer who sees three characters climbing a particular rock learns that it is climbable faster than any paint could teach them. A crowd walking in one direction is a moving breadcrumb trail. In model terms, other players raise every newcomer's `p`, including the tunnelers', because motion and crowds pop out.

This has two consequences for designers of shared spaces.

- **Signposting depends on population.** A zone that is easy to navigate at launch, full of players, can become confusing years later when it is nearly empty. Test critical routes with the zone empty, as the last player through it will see it.
- **Players will create signposts you didn't design.** Groups gather at a spot, and newcomers read the gathering as "something is here." A popular farming spot or a player marketplace can pull newcomers off the intended route. Watch where crowds form in telemetry and decide whether to support the new route or move the attraction. Week 11 on shared spaces and week 14 on heatmaps build on this.

## In-class activity (25 minutes)

Work in groups of three with a greybox route from your week 2 blockout (or the course's sample route).

1. **Audit (8 minutes).** List every signifier on the route. Mark each as true, false or hidden affordance using the table in section 1. Circle every signpost on the critical path.
2. **Test (10 minutes).** One group member who hasn't seen the route plays it while the other two record, per signpost, noticed or not. Give the player a distraction task, such as counting red objects, for the first half of the route. Swap roles once if time allows.
3. **Model (7 minutes).** Estimate `p` for each signpost from your two players. Decide whether you saw scanners, tunnelers or both. Using model 2 with your guesses, predict what share of a class of 30 would get lost. Propose one change, either a loud signpost or an escalation, and predict its effect.

Expected output: an annotated route map, a table of noticed or not per signpost per player, a predicted lost share and one proposed change with its predicted effect.

## Common misconceptions

- **"If players get lost, add more cues."** More subtle cues help the players who were already finding them. The lost tail needs a cue they will notice without looking, or a cue they get only when stuck.
- **"Yellow paint is lazy design."** It is a deliberate trade. It raises the tunnelers' `p` at an immersion cost for scanners. The failure is usually earlier, when a realistic art style left true affordances unsignified. Judge the whole system, not the paint.
- **"An affordance is a visual cue."** In this course, affordance means what the rules allow and signifier means what tells the player. Keeping them apart is what lets you find hidden and false affordances.
- **"The average notice rate tells you how many players find the route."** Only if every player has the same rate. With two groups, the average hides the tail, as the `n = 9` row showed (98% predicted, 81% actual).

## Check yourself

1. A level has 6 signposts on its critical path, each with `p = 0.25` for every player. What share of players get lost? How many signposts at `p = 0.25` would bring the lost share under 5%?
2. A designer replaces those 6 signposts with 2 signposts at `p = 0.75`. Which design gets more players through? Show the numbers.
3. A playtest of 10 testers produces per-tester notice rates of 0.9, 0.8, 0.9, 1.0, 0.8, 0.1, 0.0, 0.9, 0.2, 0.8. Which model should you use, and what shares and `p` values would you start with?
4. A game marks climbable ledges with white paint, and several decorative ledges near the start happen to be white stone. Predict what players will do, and give the fix.

<details>
<summary>Answers</summary>

1. Lost `= 0.75⁶ = 17.8%`. For under 5%, `n = ln(0.05) / ln(0.75) = 10.4`, so 11 signposts.
2. Two at 0.75 gives `1 − 0.25² = 93.75%`. Six at 0.25 gives `1 − 0.75⁶ = 82.2%`. The two loud signposts get about 12 more players in 100 through.
3. The rates bunch at the top (seven between 0.8 and 1.0) and bottom (three between 0.0 and 0.2), so use model 2. Start with 70% scanners at `p ≈ (0.9 + 0.8 + 0.9 + 1.0 + 0.8 + 0.9 + 0.8) / 7 = 0.87` and 30% tunnelers at `p = (0.1 + 0.0 + 0.2) / 3 = 0.1`.
4. Players will try to climb the white stone ledges, fail, and learn that white doesn't reliably mean climbable. After that, the true signposts lose part of their `p` for everyone. Recolor the decorative ledges (remove the false affordance) rather than making the paint louder.

</details>

## Lab / assignment hook

[Lab 05, signpost playtest and model](../labs/lab05.md). You implement both models and a small simulation, fit them to a provided playtest log, and redesign the sample route so that at least 95% of simulated players find it with the fewest loud signposts. The greybox route you fix feeds the blockouts assessment (40%).

## Sources

- Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin. The term "affordance" first appeared in Gibson's 1966 book *The Senses Considered as Perceptual Systems*. Summary checked against Wikipedia, "Affordance."
- Norman, D. A. (2013). *The Design of Everyday Things* (revised and expanded ed.). Basic Books. Affordances determine possible actions; signifiers communicate where to act. The 1988 edition popularized the design sense of "affordance." Checked against Wikipedia, "Affordance."
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press. Chapter 5, "Symbols as Guides," "Contrast," "Framing," "Rule of Thirds."
- Wikipedia, "Yellow paint in video games" (accessed September 2026). The yellow paint debate; Uncharted cited by IGN's Vikki Blake as an early example; The Stanley Parable (2013); Resident Evil 4 remake (2023) and Final Fantasy VII Rebirth (2024) in the debate; the "No More Yellow Paint" mod for Rebirth; Kotaku's 2024 summary of the trade-off; the "Shut Up Aloy" mod for Horizon Forbidden West.
- Wikipedia, "Mirror's Edge." Runner Vision turns certain objects bold red to mark paths and escape routes. DICE, 2008.
- Wikipedia, "Horizon Forbidden West." Aloy's Focus highlights climbable surfaces; critics' remarks on frequent spoken puzzle hints. Guerrilla Games, 2022.
- Capcom, *Resident Evil 4* (remake, March 2023); Square Enix, *Final Fantasy VII Rebirth* (February 2024). Release years as listed on their Wikipedia pages.

## Interactive spec: examples/w05-signpost-funnel.html

**The one insight.** When players differ in how much they notice, extra subtle signposts saturate the attentive players and barely touch the inattentive ones. The average-based prediction and the real find rate split apart, and one salient signpost closes the gap better than many subtle ones.

**Layout.** Two linked views, route left and chart right on desktop, stacked on mobile with the route on top. Readout panel under both.

**View A, "The route".** A horizontal path from left (start) to right (goal). `n` signposts drawn as small generic posts, evenly spaced. If "loud signpost" is on, draw it as a larger, brightly colored post at the position chosen by its slider. 100 simulated players as dots at the start. Scanners are circles, tunnelers are triangles (shape, not only color). On "Play," dots walk right in 4 seconds total. At each signpost, each still-lost dot rolls against its group's `p` (or `p_loud` at the loud post) and, on success, peels off upward onto a "found the route" lane. Dots that pass the last post without success end in a "lost" pile at the right. Use a seeded random generator (seed from a numeric input, default 7) so runs are repeatable. "Reroll" increments the seed. Counters show found and lost per group.

**View B, "Find chance vs signposts".** x-axis `n` from 0 to 40. y-axis P(find) from 0% to 100%. Three curves: model 1 using the population average `p̄` (dashed), model 2 mixture (solid), and model 2 with the loud signpost added (solid, second palette color, drawn only when the toggle is on). Horizontal line at the target (default 95%). Vertical marker at the current `n`. Label where each curve first crosses the target ("7 signposts", "35 signposts", or "not within 40").

**Controls.**
- Signposts `n`: 0 to 40, step 1, default 9.
- Scanner share `w`: 0% to 100%, step 5%, default 70%.
- Scanner notice chance `p_s`: 0 to 1, step 0.05, default 0.50.
- Tunneler notice chance `p_t`: 0 to 1, step 0.01, default 0.05.
- Loud signpost toggle (default off), `p_loud` 0 to 1, step 0.05, default 0.90, applied equally to both groups; position slider along the route (default the middle).
- Target: 80% to 99%, step 1%, default 95%.
- Buttons: Play, Reroll, presets "Lecture default", "Everyone the same (w = 100%, p = 0.365)", "Paint only (n = 0, loud on)", "Check yourself 2 (80% at 0.6, 20% at 0.1, n = 4)".

**Readouts (monospace, one decimal percent).** `p̄`, model 1 P(find), model 2 P(find), per-group find chances, share of lost players who are tunnelers, signposts needed for the target under each model, P(find) with the loud signpost. Simulated counts from the dots shown separately and labeled "this run (random)".

**Exact formulas.**
- `p̄ = w p_s + (1 − w) p_t`.
- Model 1: `1 − (1 − p̄)^n`.
- Model 2: `w (1 − (1 − p_s)^n) + (1 − w)(1 − (1 − p_t)^n)`.
- With loud signpost: `1 − [w (1 − p_s)^n + (1 − w)(1 − p_t)^n] × (1 − p_loud)` (position doesn't change the final probability; it only changes where dots peel off).
- Tunneler share of lost: `(1 − w)(1 − p_t)^n / [w (1 − p_s)^n + (1 − w)(1 − p_t)^n]`.
- Signposts for target `T`: smallest `n` with P(find) ≥ `T`, searched up to 1,000, shown as "more than 40" when beyond the axis.

**Test values (the build must reproduce these).**
- Defaults (`w = 0.7`, `p_s = 0.5`, `p_t = 0.05`): `p̄ = 0.365`. At `n = 1, 3, 5, 9, 20, 40`, model 1 gives 36.5%, 74.4%, 89.7%, 98.3%, 100.0%, 100.0%; model 2 gives 36.5%, 65.5%, 74.6%, 81.0%, 89.2%, 96.1%.
- Signposts for 95%: model 1 needs 7, model 2 needs 35.
- Loud on (`p_loud = 0.9`): `n = 0` gives 90.0%; `n = 3` gives 96.6%; `n = 9` gives 98.1%.
- Single group `p = 0.3`: `n = 9` gives 96.0%; 95% needs 9.
- Check yourself 2: `w = 0.8`, `p_s = 0.6`, `p_t = 0.1`, `n = 4`: model 2 gives 84.8%; tunneler share of lost 86.5%. With loud `p_loud = 0.8`: 97.0%.

**First screen.** Defaults with `n = 9`, the dots already run once (seed 7) so the lost pile shows mostly triangles. Caption: "Model 1 says 98% find the route. The two-group model says 81%. The lost pile is almost all tunnelers."

**Accessibility and motion.** All controls are native labeled inputs, keyboard reachable. Group identity uses shape as well as color. Under `prefers-reduced-motion`, Play skips the walk and draws the final positions at once. Palette from `templates/interactive-tokens.css`, light and dark.
