# PR402 · Week 02 — Production sprint 2: the content pipeline and its bottleneck

**Why this matters:** A persistent game needs content, and content is made in stages by different people. The stage with the least capacity sets how many quests you ship, however hard everyone else works. Teams that do not find that stage in week 2 spend the semester polishing art for quests that never get scripted.

**You will be able to:**
- Map your content pipeline as stages with hours per item and hours per week, and compute each stage's capacity.
- Identify the bottleneck and forecast how many content items reach content lock.
- Use Little's law to set a work-in-progress limit for the pipeline and predict the lead time of one item.
- Compare two fixes by their effect on throughput, and write the remaining gap as a scope decision.

**Before class:** Time one complete content item from your vertical slice through every stage, from first words to tested, even if you have to reconstruct it from commit history. Read [MMO306 week 12, content tooling and pipelines](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w12-content-tooling-and-pipelines.md), sections 1 and 3 (about 25 minutes). Skim chapters 1 to 5 of Goldratt and Cox, *The Goal* (1984, any edition), or its summary in Keith's *Agile Game Development*, chapter on lean production.

**Prerequisites from earlier courses:** [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) (Little's law and WIP limits). [MMO306 week 1, the content treadmill](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md) (consumption against production). [MMO306 week 8, repeatable content](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w08-repeatable-content-dailies-dungeons-rotations.md). [PR401 week 9, content plan](../../PR401-capstone-i-pre-production/lectures/w09-content-plan.md). [PR402 week 1](w01-production-sprint-1-the-ops-tax.md) (the ops tax and the content budget).

**Interactive:** [Pipeline bottleneck](../examples/w02-pipeline-bottleneck.html)

---

## 1. Content is a pipeline, not a pile

In week 1 you gave content a budget in points. That is enough to know how much fits. It is not enough to know whether it will arrive, because a quest is not one task. It passes through several people in order:

1. **Write.** The designer writes the quest: goal, steps, dialogue, rewards.
2. **Block out.** A level designer places the quest's spaces, spawns and triggers in greybox.
3. **Script.** A technical designer or programmer wires the quest into the quest framework: states, conditions, server checks.
4. **Dress.** The artist replaces greybox with final props, lighting and effects.
5. **Audio.** Sound effects and ambience for the quest's spaces and events.
6. **Test.** Someone who did not build it plays it through, including edge cases such as a party member leaving halfway.

Each stage is a person's time, and each person has a fixed number of content hours per week after feature work and the ops tax. So the right question is how many quests each stage can pass per week, and which stage is slowest. Points on a board do not answer that.

Your PR401 content plan ([PR401 week 9](../../PR401-capstone-i-pre-production/lectures/w09-content-plan.md)) listed the quests, dungeons and items you want. This week you find out how many of them the pipeline can deliver by content lock at the end of week 7. Content production runs in weeks 4 to 7, the content budget from [week 1](w01-production-sprint-1-the-ops-tax.md). Weeks 2 and 3 belong to features, so this week you time one pilot item through the pipeline and fix the pipeline before production starts.

## 2. Three numbers per stage

For each stage `s`, write down:

- `h_s`, the hours per week the stage's owner can give to content in weeks 4 to 7. This is net of the ops tax from week 1.
- `k_s`, the touch hours one item needs at that stage. Measure it from the item you timed before class, not from hope.
- `m_s = h_s / k_s`, the stage's **capacity** in items per week.

Then the pipeline's **throughput** is

```
X = min over stages of m_s
```

The stage that sets `X` is the **bottleneck**. Everything upstream of it builds a queue in front of it. Everything downstream waits for it. This is the central claim of Goldratt's theory of constraints: an hour gained at the bottleneck is an hour gained by the whole system, and an hour gained anywhere else is an illusion.

## 3. Work in progress and lead time

The second number that matters is how many items are in the pipeline at once. [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) introduced **Little's law** for a board. It holds for a pipeline too:

```
lead time W = WIP / X
```

`WIP` is the number of items started and not finished. `W` is how long one item takes from its first stage to done, on average. If the designer writes eight quests in week 2 because writing is quick, and the pipeline passes one per week, each quest takes about eight weeks to come out the other end. That is longer than you have.

At content lock a half-built quest is worth nothing. It cannot ship, and it has used hours that a finished quest could have had. So a pipeline with too much WIP is a risk even when its throughput is fine. The quests finish in a bunch at the end, and the ones still in the middle on the Friday of week 7 are lost.

## 4. Worked example: the art that was never the problem

### The hook

World of Warcraft Classic launched on 26 August 2019. It recreated the game as it stood in 2006, so every zone, dungeon and raid it would ever contain was already built. Blizzard still did not release it all at once. Content arrived in a six-phase schedule, with raids and battlegrounds held back and released over the following years, to follow the rhythm of the original game's patches.

A team with every piece finished still chose to ration it, because players consume content far faster than anyone can make it ([MMO306 week 1](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md) puts numbers on that). Your team has the opposite problem. You have almost nothing finished and four weeks of content production to make it in. So you need to know, this week, how many quests your pipeline can actually produce.

### The model

```
capacity      m_s = h_s / k_s                 (items per week at stage s)
throughput    X   = min_s m_s
lead time     W   = WIP / X                   (Little's law)
forecast      N   = floor(X × weeks)
play minutes  N × minutes per item
```

- `h_s` is the stage's content hours per week, `k_s` its touch hours per item.
- `weeks` is the number of content production weeks before content lock, four in this course (weeks 4 to 7).
- `minutes per item` is how long a first-time player takes to complete one item. Measure it at a playtest.

The forecast ignores the time the first item needs to fill the pipeline. With a WIP limit that keeps `W` at two weeks or less, that error is small next to the uncertainty in `k_s`.

### Numbers you can check

Emberfall's PR401 content plan ([PR401 week 9](../../PR401-capstone-i-pre-production/lectures/w09-content-plan.md)) targets about three hours of first-play content in quest-sized units (tutorial steps, town contracts and bounties), about 12 units of 15 minutes each. This guide calls each unit a quest. The team timed a contract from its vertical slice and set the content hours each owner can give in weeks 4 to 7:

| Stage | Owner | `h_s` (h/week) | `k_s` (h/quest) | `m_s` (quests/week) |
|---|---|---|---|---|
| Write | Content designer | 8 | 6 | 1.33 |
| Block out | Systems designer | 8 | 5 | 1.60 |
| Script | Tools and UI programmer | 9 | 9 | **1.00** |
| Dress | Artist | 12 | 8 | 1.50 |
| Audio | Audio and tech-art student | 4 | 2 | 2.00 |
| Test | Rotating | 4 | 1.5 | 2.67 |

Check one row. Script: `9 / 9 = 1.00` quest per week. That is the lowest capacity, so scripting is the bottleneck and `X = 1.0`.

Together the stages use 45 hours a week, close to the 43 backlog hours a week that week 1's taxed plan leaves in weeks 4 to 7. Content production runs from week 4 to week 7, four weeks. `N = floor(1.0 × 4) = 4` quests, 60 minutes of play, a third of the target.

The team has also started eight quests, because the content designer drafted them all in week 1. Little's law gives `W = 8 / 1.0 = 8` weeks per quest, which is longer than the four production weeks. In practice some will finish, but the team will reach content lock with several quests half built.

**Plan B: more art hours.** At the week 2 review, the build looks unfinished, because greybox is visible everywhere. The audio and tech-art student moves 4 hours a week onto dressing, the kind of art help PR401 week 11 planned. Art capacity rises from 1.50 to 2.00 quests per week. Throughput stays at `X = 1.0`, because scripting has not changed. The build looks better and the forecast does not move. Four quests.

**Plan C: fix the bottleneck.** The tools and UI programmer spends 10 hours in weeks 2 and 3 on a data-driven quest template, so common steps (talk to, collect, defeat, return) become configuration instead of code. The template is a tool, so it is a feature story, paid from the feature budget and kept above the lab 01 cut line like the deploy script. That cuts `k_script` from 9 to 4 hours for most quests. The content designer drops design-doc upkeep and gives 2 more hours to writing. Production still starts in week 4, with four weeks to content lock.

| Stage | `h_s` | `k_s` | `m_s` |
|---|---|---|---|
| Write | 10 | 6 | 1.67 |
| Block out | 8 | 5 | 1.60 |
| Script | 9 | 4 | 2.25 |
| Dress | 12 | 8 | **1.50** |
| Audio | 4 | 2 | 2.00 |
| Test | 4 | 1.5 | 2.67 |

The bottleneck has moved to dressing, which is art, the constraint PR401 week 11 found for the whole plan. `X = 1.5`, and `N = floor(1.5 × 4) = 6` quests, 90 minutes. With a WIP limit of 3, `W = 3 / 1.5 = 2` weeks, so the first production quests are done by the end of week 5. The pilot quest from weeks 2 and 3 is what alpha testers play.

| Plan | Bottleneck | `X` | Weeks | Quests | Minutes | Gap to 180 |
|---|---|---|---|---|---|---|
| A status quo | Script | 1.00 | 4 | 4 | 60 | 120 |
| B more art | Script | 1.00 | 4 | 4 | 60 | 120 |
| C template | Dress | 1.50 | 4 | 6 | 90 | 90 |

Now the extra art hours from plan B would help. Art is the bottleneck in plan C, so moving 4 hours to dressing raises its capacity to 2.0 and `X` to 1.6, where block out becomes the limit. Over four weeks that is 6.4 quests, so 6 finished and a seventh most of the way through at content lock. The same change that moved nothing in plan B moves the forecast in plan C, because help only counts at the bottleneck, and only until the next stage takes over. A seventh finished quest needs dressing and block out raised together.

Even the best plan leaves a 90-minute gap. The gap is a scope decision, not a production problem. Emberfall can cut the target to what the pipeline delivers, or fill it with content that costs fewer touch hours per minute of play. A hand-made quest here gives `15 / 31.5 = 0.48` play minutes per production hour. A repeatable bounty board built on the same template, as in [MMO306 week 8](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w08-repeatable-content-dailies-dungeons-rotations.md), can return several times that, at the price of variety. That is the bet Emberfall's PR401 content plan already made.

This program reproduces the tables:

```python
import math

# stage: (hours per week on this stage, hours per quest)
plan_a = {
    "write":  (8, 6),
    "block":  (8, 5),
    "script": (9, 9),
    "dress":  (12, 8),
    "audio":  (4, 2),
    "test":   (4, 1.5),
}


def report(name, stages, weeks, wip):
    cap = {s: h / k for s, (h, k) in stages.items()}
    x = min(cap.values())
    neck = min(cap, key=cap.get)
    done = math.floor(x * weeks)
    print(f"{name}: bottleneck {neck}, X {x:.2f}/wk, lead {wip / x:.1f} wk, "
          f"{done} quests, {done * 15} min")


report("A", plan_a, 4, 8)
report("B", dict(plan_a, dress=(16, 8)), 4, 8)
plan_c = dict(plan_a, script=(9, 4), write=(10, 6))
report("C", plan_c, 4, 3)
report("C+art", dict(plan_c, dress=(16, 8)), 4, 3)
print("play minutes per production hour:", round(15 / sum(k for _, k in plan_a.values()), 2))
```

It prints:

```
A: bottleneck script, X 1.00/wk, lead 8.0 wk, 4 quests, 60 min
B: bottleneck script, X 1.00/wk, lead 8.0 wk, 4 quests, 60 min
C: bottleneck dress, X 1.50/wk, lead 2.0 wk, 6 quests, 90 min
C+art: bottleneck block, X 1.60/wk, lead 1.9 wk, 6 quests, 90 min
play minutes per production hour: 0.48
```

### Cross-game recognition

- **Diablo, released in North America on 3 January 1997.** Its dungeon levels were randomly generated, so a second or third run met layouts and enemies the player had not seen. In pipeline terms, Blizzard North took the "block out" and much of the "dress" stage off the per-play path. They built generators and tile sets once, and each new play reused them. That is plan C's template taken to its limit, with a much higher play-minutes per production hour.
- **WoW Classic, 2019.** The six phases ration a finished stock against consumption. Your version of this in week 9 onward is the live-ops cadence ([MMO306 week 13](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md)): hold back some finished quests so the launch has something for week 11.
- **Goldratt and Cox, *The Goal*, 1984.** A factory novel, not a game, but the same argument. A plant manager finds that adding capacity to non-bottleneck machines only grows inventory, and that output rises only when the constraint is fed and protected.

### Eyes-open judgment

The model assumes every quest has the same `k_s`. Real quests vary, and a boss quest may need three times the scripting of a fetch quest. Keep the model per quest type if your mix is uneven, and sequence the heavy ones first, in week 4, before the closed beta tax peaks in week 5.

The template in plan C costs something beyond its 10 hours. Templated quests look and play more alike, which is the variety price MMO306 warns about. Decide which quests are signature pieces that get hand scripting, and let the template carry the rest.

Moving people across stages has limits too. An artist cannot script, and a programmer's dressing will not pass art review. Cross-skilling works for adjacent stages, such as a designer doing blockout or the audio student running tests. Plan moves between those, and do not pretend that hours are interchangeable between the others.

Finally, do not fix the bottleneck by making its owner work more hours. That is crunch ([PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md)), and it lowers capacity by week 5 when the ops tax arrives.

## 5. Running the pipeline in the sprint

Put the pipeline on the board as columns, one per stage, with a WIP limit on the whole pipeline. Three rules keep it flowing:

- **Pull, do not push.** A stage starts a new item only when the next stage has room. The designer who finishes early helps test or writes the template's documentation. They do not start quest nine.
- **Protect the bottleneck.** The bottleneck's owner does no meetings, reviews or ops work that someone else can do. In plan A, an hour of bottleneck time lost to a deploy is a ninth of a quest.
- **Remeasure `k_s` weekly.** After two or three items through the new template, the real scripting time will differ from the estimate. Update the lab 02 sheet at each review.

## Studio session plan

Week 2 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Sprint 1 review: done points, measured ops tax, lab 01 rerun | Updated `plan.csv` |
| 0:15-0:35 | Briefing: sections 1 to 3 of this guide | |
| 0:35-1:10 | Map the pipeline: stages, owners, `h_s` and `k_s` from the timed item (lab 02, part A) | `pipeline.csv` filled |
| 1:10-1:20 | Break | |
| 1:20-1:50 | Find the bottleneck; design one fix and rerun (lab 02, part B) | Two runs of `check_pipeline.py` saved |
| 1:50-2:15 | Scope decision for the remaining gap: cut, repeatable content or both | Line in `content-plan.md` |
| 2:15-2:40 | Instructor round, 5 minutes per team: bottleneck, WIP limit, gap | Notes on the board |
| 2:40-3:00 | Sprint 2 planning with pipeline columns and the WIP limit on the board | Sprint 2 board live |

## Deliverables

Due at the end of the week 2 meeting:

1. **Pipeline sheet** in the lab 02 format ([`labs/lab02.md`](../labs/lab02.md)), with the current plan and the chosen fix. The instructor reruns `check_pipeline.py`. It must print `PASS`.
2. **Content plan update**, a revised version of your PR401 content list, with each item marked build, template, repeatable or cut, and the forecast play minutes.
3. **Sprint 2 board** with pipeline columns and a written WIP limit.

Due at the start of week 3: at least one quest (or your equivalent content item) through every stage and playable on the team server, with its measured touch hours per stage entered in `pipeline.csv`.

## Common failure modes

- **Fixing the stage that looks worst.** Greybox is visible, so the team adds art. The build looks better and nothing more ships. Find the bottleneck from numbers.
- **Writing ahead.** Eight quests written, one scripted. Upstream stages that run ahead only raise WIP and lead time.
- **Estimating `k_s` instead of measuring it.** The vertical slice quest is your only real data point. Use it, then replace it with the first production quests.
- **The bottleneck owner on deploy duty.** The one person whose hours set output spends Thursday on a server fix someone else could do.
- **A template nobody documents.** Plan C only works if the designer can use the template without the programmer. Budget an hour for a one-page guide.
- **Treating the gap as a production problem.** When the best plan still falls short, the answer is a scope decision written down, not more hours.

## Review checklist

The instructor checks at the end of week 2 and again at the start of week 3:

- [ ] Every stage has an owner, `h_s` and `k_s`; `k_s` comes from a timed item, with the source noted.
- [ ] Bottleneck and throughput are stated, and the checker's numbers match.
- [ ] A WIP limit is set, and Little's law lead time is at most two weeks under it.
- [ ] The chosen fix raises throughput (not only a non-bottleneck stage's capacity).
- [ ] Forecast play minutes are compared to the content plan target, and any gap has a written scope decision.
- [ ] Hours moved between stages only move between adjacent skills.
- [ ] At the start of week 3: one content item through every stage and playable on the server, with measured touch hours recorded.

## Sources

- Wikipedia, "World of Warcraft Classic" (read September 2026). Global launch on 26 August 2019; content released on a six-phase schedule to emulate the original game's patch cycle.
- Wikipedia, "Diablo (video game)" (read September 2026). North American Windows release on 3 January 1997, with some retailers selling it in December 1996; randomly generated dungeon levels and the replay value reviewers credited to them.
- Goldratt, E. M. and Cox, J. (1984). *The Goal: A Process of Ongoing Improvement*. North River Press. The theory of constraints: system output is set by its constraint, and gains elsewhere do not raise it.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research*, 9(3), 383-387.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Lean production and asset pipelines in game teams.
- The Emberfall pipeline, hours and quest targets are invented for teaching and continue the constructed PR401 example.

## Interactive spec: examples/w02-pipeline-bottleneck.html

**The one insight:** adding hours to any stage other than the bottleneck changes that stage's bar and leaves the output unchanged. Adding them at the bottleneck raises output until the next stage becomes the limit.

**Layout.** Two linked views, stacked below 900px and side by side above.

- **Left, stage capacities.** One horizontal bar per stage (write, block out, script, dress, audio, test), length `m_s = h_s / k_s` in quests per week, on a shared axis from 0 to 4. A vertical line marks `X = min m_s` across all bars. The bottleneck bar uses the accent color and a text label "bottleneck". Each row has two number steppers, `h_s` (0 to 20, step 1) and `k_s` (0.5 to 20, step 0.5).
- **Right, forecast.** Stacked blocks, one per quest, filling a column up to `N = floor(X × weeks)`, beside a target line at `target_minutes / minutes_per_item` quests. Under it: throughput `X`, lead time `W = WIP / X`, quests `N`, play minutes `N × minutes_per_item`, gap to target in minutes.

**Controls.** Production weeks to content lock (1 to 8, default 4). WIP (1 to 12, default 8). Minutes per quest (default 15). Target minutes (default 180). Buttons "Plan A", "Plan C" and "Plan C + art" load the guide's presets.

**Test values.** Plan A: `m` = 1.33, 1.60, 1.00, 1.50, 2.00, 2.67; bottleneck script; `X = 1.00`; weeks 4; `N = 4`; 60 minutes; WIP 8 gives `W = 8.0`. Plan B (dress `h` = 16): dress bar 2.00, `X` still 1.00, `N = 4`. Plan C (write 10/6, script 9/4, weeks 4, WIP 3): bottleneck dress, `X = 1.50`, `N = 6`, 90 minutes, `W = 2.0`. Plan C + art (dress 16/8): bottleneck block out, `X = 1.60`, `N = 6`, 90 minutes.

**Behavior.** When the bottleneck changes, briefly outline the new bottleneck bar (skip the animation under `prefers-reduced-motion`). When `W` exceeds the weeks left, show "lead time longer than the time left" in the warning color.

**Accessibility.** Every value also in a table below the bars. Keyboard operable steppers. Colors from `templates/interactive-tokens.css`.
