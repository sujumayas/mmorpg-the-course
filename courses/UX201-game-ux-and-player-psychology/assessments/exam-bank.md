# UX201 · Exam bank: quiz, practice and viva questions

UX201 has no written exam. The grade comes from three pieces of research you run yourself: the usability test (30%, [usability-test-brief.md](usability-test-brief.md)), the heuristic evaluation (20%, [heuristic-eval-brief.md](heuristic-eval-brief.md)) and the final UX study of a shipped game (50%, [final-study-brief.md](final-study-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go faster, because every lab asks you to apply the same model to your own data.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Viva.** The final study ends with an individual viva (see the final study brief), and the markers of the usability test and heuristic evaluation may ask one question during feedback. Examiners draw questions in the style of this bank and rewrite them with the numbers from your own study.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model or method behaves the way it does, with a number or a mechanism as evidence.
- **design**: choose values, a method or a layout that meets a stated goal, and show that it meets it.
- **critique**: find what is wrong with a claim, a study or a design, and say how to fix it.

All games, testers, studios and numbers are invented unless a question names a real game. Every real-game fact used here comes from the lecture of the tagged week, which cites its source and version. No question relies on a game fact the lectures do not state. The lecture constants (for example `a = 500 ms` in week 1, `M = 1.35 s` in week 2, `s₀ = 20` and `g = 2.5` in week 7) are teaching values, and the questions use them unless they say otherwise. Every numeric answer was recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: Perception, attention and memory

1. *Week 1 · compute.* A crafting screen lists 24 materials as plain text labels in no fixed order. A player checks whether they own a particular material about 40 times an hour, and they own it 25% of the time. Use the lecture's values (`a = 500 ms`, `k = 30 ms` per item with the target present, `60 ms` with it absent). (a) What is the expected search time per check, and per hour? (b) The team splits the list into four tabs of six, and the player always knows which tab to open, at no extra cost. Recompute. (c) Instead, the team highlights in gold the 10 materials the player owns. What kind of search is the player now doing, and what does it cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,760 ms per check, 70.4 s per hour. (b) 815 ms per check, 32.6 s per hour. (c) Guided search among the 10 gold items, item by item. 1,025 ms per check, 41.0 s per hour.

(a) Present: `500 + 30 × 24 = 1,220 ms`. Absent: `500 + 60 × 24 = 1,940 ms`. Expected: `0.25 × 1,220 + 0.75 × 1,940 = 305 + 1,455 = 1,760 ms`. Per hour: `40 × 1.76 = 70.4 s`.

(b) Now `N = 6`. Present `680 ms`, absent `860 ms`. Expected `0.25 × 680 + 0.75 × 860 = 815 ms`, or 32.6 s an hour.

(c) Gold marks "owned", not "the material I want". The target differs from the other gold items only by its name, so the gold does not make it pop out. It cuts the set the player must read from 24 to 10, which is a filter. Present `800 ms`, absent `1,100 ms`, expected `0.25 × 800 + 0.75 × 1,100 = 1,025 ms`, or 41.0 s an hour. It is the same trap as the lecture's "beam on every blue item". A highlight that marks a category changes `N`. Only a feature unique to the target changes `k`.
</details>

2. *Week 1 · compute.* In a lab 01 study, the group means (ms) at set sizes 4, 8, 16 and 32 were: item by item, target present 610, 745, 990, 1,450; item by item, target absent 700, 980, 1,450, 2,420; pop-out 520, 505, 515, 510. (a) Fit `a` and `k` for each line by least squares. (b) What is the ratio of the absent slope to the present slope, and does it match the model? (c) Predict the absent search time for 24 items.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Present `a = 501.5`, `k = 29.8`. Absent `a = 473.5`, `k = 60.9`. Pop-out `a = 514.8`, `k = −0.15`. (b) 2.04, close to the model's 2. (c) About 1,936 ms.

(a) The mean set size is `x̄ = 15`. The sum of squared deviations is `11² + 7² + 1² + 17² = 460`. For the present line, `ȳ = 948.75`, and `Σ(x − x̄)(y − ȳ) = 13,715`, so `k = 13,715 / 460 = 29.8` and `a = 948.75 − 29.8 × 15 = 501.5`. The other two lines follow the same steps, or use `=SLOPE` and `=INTERCEPT` in a spreadsheet.

(b) `60.9 / 29.8 = 2.04`. The model says a self-terminating search checks `(N + 1)/2` items on average when the target is there and all `N` when it isn't, which gives a factor of about 2. The data agree.

(c) `473.5 + 60.9 × 24 = 1,936 ms`. The absent intercept came out lower than the present one. That happens with small samples. The intercepts carry most of the timing noise, and the slopes are the quantities to trust.

The pop-out slope is slightly negative, which is noise around zero. Report it as "no measurable cost per item".
</details>

3. *Week 1 · explain.* In an action RPG, the message "Your bags are full" appears in small white text at the top centre of the screen while the player is looting in the middle of a fight. Testers keep losing items they thought they had picked up. Use this week's ideas about attention and memory to explain why, and propose two changes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The message arrives where attention isn't, during a task that uses all of it, and nothing about it is distinct enough to break through.

- **Inattentional blindness.** The player's attention is on the fight. As in Simons and Chabris's gorilla study, a fully visible message can go unnoticed when attention is engaged elsewhere. Being on screen is not being noticed.
- **No bottom-up signal.** Small white text is not a basic feature that pops out. It has no motion, no unique colour, no sound. It competes with everything else on screen.
- **Nothing in the world afterwards.** Once the text fades, the player has no way to recover the information. They carry the belief "I looted it" in their head, and it is wrong.

Changes that follow from the model (any two):

- Put the signal where the task already takes the eyes. Show "Bag full" on or next to the loot the player just tried to take.
- Give it a feature nothing else has, such as a distinct sound or a brief shake of the item, and save that feature for important failures only, so it stays unique.
- Put the knowledge in the world. Leave the item on the ground with a marker, and show a bag-full icon on the HUD until the player makes space.
</details>

4. *Week 1 · critique.* A puzzle game shows a six-symbol code on a wall. Three rooms later, the player must enter it on a keypad. The code is shown once, and there is no journal. The designer says, "Players remember seven things, so six is fine." Critique the claim and say when keeping the code in the player's head is a legitimate design choice.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The claim uses Miller's 1956 estimate, and the lecture recommends designing for about four chunks, fewer under stress. Six unfamiliar symbols are six chunks, carried for minutes while the player does other things, which also invites forgetting.

The model says three things.

- **Capacity.** Six new chunks exceed the four-chunk budget. Unless the symbols form a pattern the player can chunk (a word, a familiar sequence), most players will lose one.
- **Time.** Three rooms of play fill working memory with other material. Long-term storage needs rehearsal or meaning, and the game gives neither.
- **Recognition rather than recall.** A journal entry, a sketch the character makes, or the code shown on the keypad as a set of options would move the knowledge into the world.

It is legitimate to keep it in the head when remembering is the puzzle. Then say so to the player, make the code chunkable (for example two groups of three that relate to the room), and remove other demands on memory in those three rooms. If the puzzle is really about finding the code, not memorising it, the memory load is extraneous and a journal costs nothing.
</details>

## Week 2: Cognitive load and UI

5. *Week 2 · compute.* An expert player stands at a vendor with the sell window open and wants to sell 3 junk items from a bag of 30 unsorted entries. Selling an item is a right-click on it. Treat each scan as `S(30)` and include one `M` at the start. (a) Write the operators and compute the time. (b) The team adds a "Sell junk" button. Compute the expert time (`M P BB`) and the novice time, where the novice must first find the button among the 8 buttons in the window. (c) When would the button delete something that should stay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12.23 s. (b) Expert 2.65 s, novice 3.33 s. (c) When deciding what counts as junk is a real decision.

(a) `M + 3 × (S(30) + P + BB)`. `S(30) = 0.15 × 31 / 2 = 2.325 s`. Each item costs `2.325 + 1.1 + 0.2 = 3.625 s`. Total `1.35 + 3 × 3.625 = 12.225 s`.

(b) Expert: `1.35 + 1.1 + 0.2 = 2.65 s`. Novice: `M + S(8) + P + BB = 1.35 + 0.675 + 1.1 + 0.2 = 3.325 s`. Nearly all of the saving is the three scans, which a click count never shows.

(c) If some grey items are secretly crafting reagents, or the game's economy is built around judging what to keep, then "which items are junk?" is an intrinsic decision. A button that decides for the player deletes part of the game. If junk is always junk, the decision is only arithmetic and the button removes extraneous load.
</details>

6. *Week 2 · explain.* Classify each as intrinsic, extraneous or germane load, and say in one sentence why. (a) Reading a boss's wind-up animation to decide when to dodge. (b) Opening a separate codex window to check what a gem does, then returning to the socketing screen. (c) Practising a five-input combo until it feels like one move. (d) Remembering which of three unlabelled icons in a menu means "sell".

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Intrinsic. (b) Extraneous. (c) Germane. (d) Extraneous.

(a) Reading the boss is the challenge the designers built. Removing it would remove the fight.

(b) This is split attention. The player holds the gem's effect in working memory while switching screens. A tooltip on the socketing screen would remove the holding.

(c) This is effort spent building a chunk. Once the combo is chunked, it costs one `M` instead of five, so the effort pays back.

(d) This is recall where recognition would do. Labels, or a tooltip on hover, put the knowledge in the world.
</details>

7. *Week 2 · design.* A shop lists 48 unsorted items. The team is debating category tabs, which would cut the list the player must scan to 8. For a novice, tabs add one extra `M` and two extra `K`s. An expert pays the two `K`s but not the `M`. Without tabs, both pay `M K S(48)`. (a) Compute novice and expert times with and without tabs. (b) What is the smallest unsorted list size at which tabs save a novice time? (c) What does this imply for a shop that sells 20 items?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Without tabs 5.31 s for both. With tabs, novice 4.22 s, expert 2.87 s. (b) 34 items. (c) Below about 34 items, tabs cost novices time, so a 20-item shop should use a single list, sorted if possible.

(a) Without tabs: `1.35 + 0.28 + 0.15 × 49 / 2 = 1.35 + 0.28 + 3.675 = 5.305 s`. Novice with tabs: `M K M 2K S(8) = 1.35 + 0.28 + 1.35 + 0.56 + 0.675 = 4.215 s`. Expert with tabs: `1.35 + 0.28 + 0.56 + 0.675 = 2.865 s`.

(b) Tabs pay off for a novice when `0.075 × (N + 1) > 1.35 + 0.56 + 0.675 = 2.585`, so `N + 1 > 34.5`. At `N = 33` the untabbed time is 4.18 s, less than 4.215. At `N = 34` it is 4.255 s, more. So 34.

(c) Tabs are an investment in germane load. They pay novices only for long lists, and they pay experts almost at once. For a 20-item shop, sorting the list (so the player can skip to the right region) cuts the effective `N` without the extra decision.
</details>

8. *Week 2 · design.* In a boss fight, the player must hold: (1) which of two adds to kill first, set by a chat message before the fight; (2) the time until the next floor-wipe attack; (3) which colour of orb heals them this phase; (4) whether their interrupt is off cooldown, shown by an icon; (5) the boss's current attack, read from its animation. Count the items held in the head, then choose, for each held item, one of the lecture's three options (put it in the world, make it chunkable, keep it in the head on purpose), and justify one choice where you keep it in the head.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Three items are held in the head: (1), (2) and (3). Item (4) is already in the world. Item (5) is the intrinsic challenge and should stay.

One defensible plan:

- (1) Put it in the world. A marker over the first add costs nothing in challenge, because remembering a chat message is not what the fight is about.
- (2) Make it chunkable. Use a fixed rhythm so the floor-wipe always follows the same boss animation. Experienced players store the fight as one pattern, and the timing becomes germane rather than extraneous. A visible timer is the alternative if the team wants new players to succeed on the first night.
- (3) Keep it in the head on purpose, if the phase's challenge is "learn which orb is safe". Then say so in the encounter journal, test it with a clear failure message, and don't add anything else to remember in that phase.

With (1) moved and (2) chunked, the player holds one item plus the boss's animation, well inside the four-chunk budget, leaving room for the fight.
</details>

## Week 3: Flow and difficulty

9. *Week 3 · compute.* Use the lecture's ramp `C = 2, 3, 3.5, 4, 5, 5.5, 6, 7, 7.5, 8` and the strain rule with band 0.8 to 1.25. Two new testers: Fay has skill 2.0, 2.3, 2.6, 3.0, 3.6, 4.0, 4.4, 5.0, 5.6, 6.2, and Gil has 4.0, 4.3, 4.6, 4.9, 5.2, 5.5, 5.8, 6.1, 6.4, 6.7. (a) With `Q = 3`, when does each quit? (b) With `Q = 5`? (c) Which conclusion survives both thresholds, and which doesn't?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Fay quits after level 4, anxious. Gil quits after level 3, bored. (b) Fay quits after level 6. Gil finishes. (c) "Fay leaves from anxiety in the early middle" survives. "Gil leaves" does not.

(a) Fay: `2/2.0 = 1.00` flow (0), `3/2.3 = 1.30` anxious (1), `3.5/2.6 = 1.35` anxious (2), `4/3.0 = 1.33` anxious (3), quits. Gil: `2/4.0 = 0.50` bored (1), `3/4.3 = 0.70` bored (2), `3.5/4.6 = 0.76` bored (3), quits.

(b) Fay continues with `5/3.6 = 1.39` (4) and `5.5/4.0 = 1.38` (5), and quits after level 6. Gil continues to level 4, where `4/4.9 = 0.82` is inside the band, and strain falls 2, 1, 0. His ratios then stay between 0.96 and 1.19 to the end.

(c) Fay's ratios never return to the band after level 1, so any threshold only delays her exit. Gil is different from the lecture's Ana. His ratios climb into the band at level 4, so whether he quits depends on how patient the model assumes he is. Report Fay as a robust dropout and Gil as "at risk early, depends on patience", and check Gil's stop against the observation log.
</details>

10. *Week 3 · compute.* Ten testers each clear level 6 once, dying 16 times in total. The intended count is one death per clear. (a) Estimate `R`. (b) Using the link `p = 1/(1 + R)`, compute the standard deviation of deaths per tester and the standard error of the mean. (c) Can you say the level is outside the flow band? (d) Roughly how many testers would give a standard error of 0.3?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1.6. (b) SD 2.04, SE 0.645. (c) No. (d) About 47.

(a) `16 / 10 = 1.6`, and with an intended count of 1, `R ≈ 1.6`.

(b) `p = 1 / 2.6 = 0.385`. SD `= √(1 − p) / p = √0.615 / 0.385 = 2.04`. SE `= 2.04 / √10 = 0.645`.

(c) Two standard errors either side of 1.6 run from 0.31 to 2.89, which spans all three zones. The estimate leans towards anxious, but ten testers cannot separate 1.6 from 1.2.

(d) `n = (2.04 / 0.3)² = 46.2`, so 47. That is one reason difficulty tuning moves to telemetry once a game has players. In a small playtest, pool levels, watch each tester's trend, and add time and think-aloud signals.
</details>

11. *Week 3 · compute.* An invented platformer's achievements show 90% of players beat world 1, 72% world 2, 50% world 3, 44% world 4 and 41% world 5. (a) Compute retention per step. (b) What share of players who beat world 1 went on to beat world 5? (c) A producer says, "Retention in worlds 4 and 5 is above 88%, so the late game is well tuned." What is wrong with the inference?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 80.0%, 69.4%, 88.0%, 93.2%. (b) 45.6%. (c) Late retention describes who is left, not how well the late worlds fit the average player.

(a) `72/90 = 0.800`, `50/72 = 0.694`, `44/50 = 0.880`, `41/44 = 0.932`.

(b) `41 / 90 = 0.456`.

(c) The players whose flow channel didn't match the curve left in worlds 2 and 3, where retention is lowest. The players still present in worlds 4 and 5 are mostly those the curve suits, so high retention there is survivorship, not evidence of tuning. Look first at world 3, where three in ten players who reached it didn't beat it, and remember that achievement data can't tell you why. A playtest with think-aloud and death counts on world 3 can.
</details>

12. *Week 3 · critique.* A team's playtest summary reads: "Mean challenge ratio across all testers and levels: 1.02. Levels 7 to 10 all in flow. Difficulty is well tuned. Two testers stopped early, but that's normal." In the data, one genre veteran stopped after level 2 and one new player stopped after level 7. Critique the summary and recommend one fix for each dropout, with its cost.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The pooled mean cancels boredom against anxiety, and the late levels look good because only the testers they suit are left. The summary should lead with the dropouts.

- **Pooled mean.** Averaging ratios across testers lets a bored veteran (ratios well below 0.8) and an anxious newcomer (ratios above 1.25) average to "flow". Report each tester's path.
- **Survivorship.** Levels 7 to 10 were played only by testers who didn't quit. Their ratios say nothing about the players who left.
- **"Normal".** Two of the testers left, for opposite reasons. That is the finding.

Fixes: for the veteran who left early bored, an entry point or skill check that lets experienced players start further along, at the cost that they may skip something unique to this game. For the new player who left anxious in the middle, an assist option or better teaching before level 7, at the cost of design time and, for some players, a sense that the achievement is cheaper. A flat difficulty cut would help the new player a little and make the veteran's problem worse.
</details>

## Week 4: Self-Determination Theory

13. *Week 4 · compute.* Players spend a mean `μ = 45` minutes a week on an optional activity, `σ = 30`. A three-week engagement-contingent event ("log 30 minutes a day") adds `X = 12` minutes a week while it runs. Use `d = −0.40`. (a) Predict weekly play after the event and the share of players below the old mean. (b) After how many weeks does the event break even? (c) If the drop lasts 10 weeks, what is the net change per player? (d) What uplift would break even over 10 weeks?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 33 minutes a week, 65.5% below. (b) 3 weeks. (c) −84 minutes. (d) 40 minutes a week.

(a) `45 − 0.40 × 30 = 33`. Share below `Φ(0.40) = 0.655`.

(b) Gain `3 × 12 = 36` minutes. Loss `0.40 × 30 = 12` minutes a week. Break-even `36 / 12 = 3` weeks.

(c) `36 − 10 × 12 = −84` minutes per player.

(d) `10 × 12 / 3 = 40` minutes a week, more than three times the uplift the event produced. The persistence of the drop in a live game is an assumption. Measure it with a holdout group.
</details>

14. *Week 4 · explain.* For each feature, name the contingency (engagement, completion, performance or informational), apply the lecture's test "what happens if the player says no?", and name the need most affected. (a) +5% experience for each consecutive day logged in, lost if you miss a day. (b) A weekly chest for completing any four dungeons. (c) A badge for clearing a dungeon under a par time. (d) A replay screen that marks your fastest split against your last ten runs.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) Engagement-contingent, with a loss added. Saying no costs the whole streak, so it is controlling. It thwarts autonomy. A grace day or streak freeze would turn part of the threat back into a choice.
- (b) Completion-contingent. Saying no costs a bonus, nothing more, so it is mildly controlling. Autonomy is mostly intact, and competence is barely informed because the chest reports quantity, not skill.
- (c) Performance-contingent. Saying no costs nothing. It feeds competence for players who make par and reports failure to those who don't.
- (d) Informational. There is nothing to say no to. It feeds competence for every player, because it reports growth against their own history.

In the meta-analysis numbers, (a) and (b) carry the largest expected undermining (`d` of −0.40 and −0.36), (c) less (−0.28), and (d) points the other way (+0.33).
</details>

15. *Week 4 · compute.* A crafting activity has `σ = 18` minutes a week. The team is choosing between a completion-contingent weekly event (`d = −0.36`) and a personal-best display (`d = +0.33`). (a) After each stops, how far apart does the model predict weekly crafting to be? (b) What share of players ends up below the old mean under each? (c) Why can't the team see this difference on its dashboard, and what would show it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12.4 minutes a week. (b) 64.1% against 37.1%. (c) The dashboard shows only the treated players over time. A holdout group shows it.

(a) `(0.36 + 0.33) × 18 = 12.42` minutes a week.

(b) `Φ(0.36) = 0.641` and `Φ(−0.33) = 0.371`.

(c) The event's uplift while it runs is visible, and its after-effect looks like a normal settle, because the pre-event baseline is gone. Keep a small random group that never sees the event, as in MA102 week 14, and compare the two groups for weeks after it ends. The cumulative difference from the holdout is the right-hand chart in the lecture's interactive.
</details>

16. *Week 4 · design.* An invented MMO cuts loot drops by half after two hours of continuous play, to discourage marathon sessions. Players call it a punishment. (a) Explain the reaction with cognitive evaluation theory. (b) Redesign it using the lecture's World of Warcraft rest example so the ratio between long-session and fresh play stays the same. (c) Place this player's reason on the SDT continuum: "I keep playing past two hours because my guild counts on my crafting." What change would move it one row towards autonomy?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) The penalty is controlling. It tells players what they must not do, so it moves the reason for stopping outside them. (b) Give a loot bonus for the first stretch of play after time away, and remove the penalty. (c) Introjected, moving to identified.

(a) CET says every reward or penalty carries a message. "Your loot is halved because you played too long" says "you are being punished for playing". It thwarts autonomy even though it serves the player's wellbeing.

(b) Double loot for the first period after a break, decaying to normal, keeps the same ratio between fresh and tired play. The World of Warcraft beta did exactly this, replacing an experience penalty with rested experience, and the developers described it as the same numbers seen from the opposite side. Now the message is "here is a gift for coming back", and the natural stopping point is framed as a choice.

(c) Guild obligation and guilt drive the reason, so it is introjected. It moves to identified when the player values the outcome for themselves. Design can help by letting a crafter queue work or hand off recipes so the guild isn't hurt when they log off. That removes the guilt lever and leaves the reason that remains.
</details>

## Week 5: Reinforcement schedules and their ethics

17. *Week 5 · compute.* Use `k = 1`, `A = 100`, pause `= 100 / V` seconds and one second per action. (a) List the FR 4 values of the next action at `j = 0` to 3. (b) The VR 4 value is `Σ 0.25 × 0.75^(d−1) × 100 / (1 + d)`. Compute it. (c) For which `θ` does the FR player stop after rewards while the VR player never stops? (d) Compare actions per minute. What does the comparison say about the claim that random schedules matter because they are faster?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 20.0, 25.0, 33.3, 50.0. (b) 28.28. (c) `20 < θ < 28.28`. (d) FR 13.33 and VR 13.23 actions per minute. At a small ratio, the rates are almost equal, and the stopping point is the whole difference.

(a) `D = 4, 3, 2, 1` gives `100/5, 100/4, 100/3, 100/2`.

(b) The first terms are `0.25 × 50 = 12.5`, `0.1875 × 33.3 = 6.25`, `0.1406 × 25 = 3.52`, and the series sums to 28.28.

(c) The FR value right after a reward is 20. The VR value is always 28.28. A player whose alternative is worth between them stops on FR and keeps going on VR.

(d) FR: pauses `5 + 4 + 3 + 2 = 14 s` plus 4 s of actions, 18 s per four actions, 13.33 per minute. VR: `4 × (3.536 + 1) = 18.14 s`, 13.23 per minute. The VR player is not faster here. The lecture's misconception section makes the same point. The difference that holds up is that the fixed schedule contains a moment where the next reward is furthest away, and the random one never does.
</details>

18. *Week 5 · explain.* For a mean ratio `N = 10`, the lecture gives FR 9.09 and VR 17.32 right after a reward at `k = 1`. Compute the same pair for `k = 2` and `k = 0.5`, and the VR ÷ FR ratio for each. Which kind of player feels the variable schedule's pull most, and why does the checklist ask about the audience?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `k = 2`: FR 4.76, VR 10.19, ratio 2.14. `k = 1`: ratio 1.90. `k = 0.5`: FR 16.67, VR 27.37, ratio 1.64. The variable schedule's advantage grows with the discount rate.

FR right after a reward is `100 / (1 + 10k)`. VR is `Σ 0.1 × 0.9^(d−1) × 100 / (1 + k d)`, summed numerically.

At `k = 0` the two are equal (question 3 in the lecture's worked example). The advantage exists because near rewards are worth much more than far ones lose, and a steeper discount makes that asymmetry larger. Players who discount the future steeply (the lecture singles out any group that does, and regulators single out minors) feel the pull of a random schedule most. That is why the ethics checklist asks who the audience is.
</details>

19. *Week 5 · compute.* A cosmetic drops with chance 1 in 250 per kill. (a) What is the mean number of kills? (b) After how many kills have half of players got it? (c) How many dry kills before the streak has less than a 5% chance? (d) The store page says "about 250 kills on average". What should it add?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 250. (b) 173. (c) 748. (d) The worst case, and the fact that half of players need fewer than the mean.

(a) The geometric mean is `1 / p = 250`.

(b) `ln 0.5 / ln(0.996) = 172.9`, so 173.

(c) `ln 0.05 / ln(0.996) = 747.4`. Check: `0.996^747 = 0.0501` and `0.996^748 = 0.0499`, so 748.

(d) The mean hides a long tail. One player in twenty is still empty-handed after almost three times the mean. Publish "1 in 250" and the 95th-percentile figure, or cap it with a visible counter. A player on this schedule also cannot detect from their own results whether the drop was removed, which is the extinction argument for published odds.
</details>

20. *Week 5 · explain.* Name the schedule and the response pattern the lecture predicts for each. (a) A fish bites at a random moment between 5 and 25 seconds after you cast. (b) A battle pass grants a tier every 1,000 experience points. (c) A daily chest that becomes available at the server reset. (d) Card packs with a random rare card and a guaranteed rare at 40 packs without one.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) Variable interval. Steady, moderate checking.
- (b) Fixed ratio, counted in experience rather than actions. A post-reward pause after each tier, then a steady run to the next.
- (c) Fixed interval. Little activity early in the day and a rise towards the reset. In practice, a login spike just after it.
- (d) Variable ratio with a fixed-ratio ceiling, like the Hearthstone pity timer in the lecture. The flat value line of a random schedule for most players, with the worst dry streak cut off. No natural stopping point is added, because the counter resets when the guarantee fires.
</details>

21. *Week 5 · critique.* An invented mobile game sells pulls with premium currency. Each pull has a 1-in-150 chance of the featured character, with a guarantee at 90 pulls that resets when it fires. The odds are listed on a web page linked from the settings menu. The game is rated for ages 12 and up. (a) What share of players reaches the guarantee? (b) Without the guarantee, what would the 95th-percentile cost be? (c) Run the seven-question checklist and recommend two changes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 54.8%. (b) 448 pulls. (c) Five of seven answers are concerns. Recommended changes are odds at the point of purchase in "1 in N" form, and a visible counter or a direct purchase option.

(a) The chance of no character in 90 pulls is `(149/150)^90 = 0.548`, so just over half of players hit the guarantee.

(b) `ln 0.05 / ln(149/150) = 447.9`. Check: `(149/150)^447 = 0.0503` and `(149/150)^448 = 0.04995`, so 448 pulls. The guarantee cuts the worst case by a factor of five.

(c) Checklist:

1. *Stopping points.* None. The value line is flat, and the reset guarantee adds no dip.
2. *Money in.* Yes, through premium currency.
3. *Disclosure.* Weak. Odds exist but not where the player chooses, and in percentage form.
4. *Worst case.* Capped at 90, but the cap is not shown in the pull screen.
5. *Audience.* Includes minors.
6. *Exit.* If the counter is hidden or players believe it resets on leaving, leaving feels like a loss.
7. *Informational alternative.* Possible, for example earning the character through a skill challenge.

Two changes, each tied to a "yes": show "1 in 150, guaranteed by pull 90, you are at pull 37" on the pull button, and offer the featured character for direct purchase. Neither removes the system, and both answer questions regulators have acted on.
</details>

## Week 6: Player motivation models

22. *Week 6 · compute.* Use the lecture's forced-choice design (four types, each pair asked five times, 15 appearances per type). Player X's interests are Achiever 5, Explorer 2, Socialiser 9, Killer 4.5. Player Y's are 9, 7, 9.5, 8. (a) Compute both forced-choice profiles. (b) Apply Yee's primary rule (`top × 0.75 > second`) to the rating scores. (c) What does the comparison show?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Both players score Socialiser 100%, Achiever 66.7%, Killer 33.3%, Explorer 0%. (b) X has a primary motivation, Socialiser. Y has none. (c) Forced choice sees only the order of interests, never their levels or gaps.

(a) Both players rank S > A > K > E. The top type wins all 15 of its questions, the second wins 10, the third 5, the last 0. The sum is 200% for both.

(b) X: `9 × 0.75 = 6.75 > 5`, so primary Socialiser. Y: `9.5 × 0.75 = 7.125 < 9`, so no primary.

(c) X is a clear socialiser who is lukewarm about everything else. Y is enthusiastic about all four. The forced-choice test calls them identical. A rating scale shows both the difference in level and Y's near-tie at the top.
</details>

23. *Week 6 · compute.* A student builds a forced-choice test with three types (Achievement, Social, Immersion), asking each pair six times. (a) How many questions are there, and how many times does each type appear? (b) What do the scores sum to, and what is the maximum score? (c) For a population with independent interests, what is the average correlation between two types' scores? (d) Generalise (b) and (c) to `T` types.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 18 questions, 12 appearances each. (b) 150%, maximum 100%. (c) −0.5. (d) Sum `T/2 × 100%`, average correlation `−1/(T − 1)`.

(a) Three pairs × 6 = 18 questions. Each type is in 2 pairs × 6 = 12.

(b) Every question gives one win, so wins total 18, and the scores total `18 / 12 × 100% = 150%`. A type chosen every time scores `12 / 12 = 100%`.

(c) With a fixed total and equal variances, the pairwise correlations must average `−1/(T − 1) = −1/2`. A simulation of 4,000 players with independent random interests gives −0.50, −0.51 and −0.49, while the rating-scale correlation is about 0.00.

(d) With `r` repetitions, questions `= T(T − 1)/2 × r`, appearances per type `= (T − 1) × r`, so the sum is `T/2`. For four types that is 200% and −1/3, as in the lecture.
</details>

24. *Week 6 · critique.* A studio's community survey (forced choice, Bartle's four types) reports: "Achiever and Socialiser scores correlate at r = −0.38, so our achievers are not social. We will build progression and social systems as separate tracks." Critique the reasoning.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Most of that correlation is built into the instrument. With four types and a fixed 200% total, forced-choice scores for any two types correlate at about −1/3 even when interests are unrelated. An observed −0.38 is barely different from what the questionnaire manufactures.

Yee's rating-scale data found the opposite relationship, Achievement and Socializing correlating at a mild positive `r = .10`. To learn whether this community's achievers are social, the studio needs rating-scale items for each motivation, scored independently. It should then report overlapping segments, for example "top quartile on Achievement" and "top quartile on Community", and look at how many players are in both. The design decision to split progression from social play may still be right, but this survey can't support it.
</details>

25. *Week 6 · explain.* A text-based online world has a large, stable social population because player killing is impossible. The owners plan to allow open player killing everywhere to "add excitement". Using Bartle's population dynamics, predict what happens, and say why the lecture recommends Bartle's model as a lens rather than a measurement.

<details>
<summary>Answer and worked solution</summary>

**Answer:** More killing drives achievers away and socialisers even more strongly, according to Bartle's dynamics. A world that socialisers dominate because killing is prevented is one of his stable configurations, and removing the prevention removes what holds it stable. The likely path is a shrinking social population, then fewer targets for the killers, with the risk of the empty-world configuration.

The dynamics are useful because they describe how one group's play changes the experience of another, which is exactly the question here. The four types themselves came from one community's debate in 1989 and 1990, not from measurement, and Bartle said most players lean a little to all four. So use the model to reason about interactions ("what does open killing do to people who come to talk?"), and measure your actual players with a rating-scale instrument before you size any group.
</details>

26. *Week 6 · design.* You have five minutes of a playtest session to learn whether testers of a co-op exploration game are motivated by Discovery, Community and Challenge. Design the instrument (item format, number of items, scoring) and the reporting table you would show the team. Say what your report will not claim.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One good design:

- **Format.** Rating-scale items, one statement at a time, 1 to 5 from "not at all" to "extremely" important to me. No forced choice.
- **Items.** Three or four per motivation, written for this course, for example "Finding places the game didn't point me to" for Discovery. At least one item per motivation phrased so that a low rating means high interest, to catch acquiescence (week 12).
- **Scoring.** Mean per motivation per tester. Standardise within the sample if you want to compare motivations, and compare with a benchmark only if you have one for the genre.
- **Reporting table.** One row per motivation, with the share of testers in the top quartile, the share in the bottom quartile, and the count behind each share. Segments may overlap and needn't sum to 100%.

The report will not assign each tester a single type, will not state population percentages from a playtest sample, and will not treat self-report as behaviour. Pair it with what testers did in the session (week 3 and week 8 methods).
</details>

## Week 7: Onboarding and tutorials

27. *Week 7 · compute.* A game needs three mechanics at minute 50. Grapple is taught at minute 3 and used at 12 and 30. Parry is taught at 15 and used at 20. Glide is taught at 35 and not used again. With `s₀ = 20` and `g = 2.5`, compute recall at minute 50 for each, all-ready recall, and the expected number of mechanics missing. Which number would a tutorial checklist report instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Grapple 0.852, Parry 0.549, Glide 0.472. All-ready 0.221. Expected missing 1.13. The checklist would report "all taught by minute 35".

- Grapple: two uses, `s = 20 × 2.5² = 125`, gap `50 − 30 = 20`, recall `e^(−20/125) = e^(−0.16) = 0.852`.
- Parry: one use, `s = 50`, gap 30, recall `e^(−0.6) = 0.549`.
- Glide: no uses, `s = 20`, gap 15, recall `e^(−0.75) = 0.472`.

All-ready `0.852 × 0.549 × 0.472 = 0.221`. Expected missing `3 − (0.852 + 0.549 + 0.472) = 1.13`.

Glide was taught most recently and is still the weakest, because it has no practice uses. Recency without repetition leaves stability at `s₀`.
</details>

28. *Week 7 · design.* For the schedule in question 27, the team can add exactly one unprompted practice use before minute 50. (a) If it goes at minute 49, which mechanic should get it, and what is all-ready recall then? (b) Is a Glide use at minute 45 better or worse than a Parry use at minute 49? (c) Why does the weakest mechanic win?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Glide, giving 0.458. (b) Better, 0.423 against 0.399. (c) All-ready recall is a product, so raising the smallest factor raises it most.

(a) At minute 49, Grapple would reach 0.997 (all-ready 0.258), Parry 0.992 (0.399), Glide 0.980 (0.458). Glide wins.

(b) Glide at 45: `s = 50`, gap 5, recall `e^(−0.1) = 0.905`, all-ready `0.852 × 0.549 × 0.905 = 0.423`. That still beats Parry at 49.

(c) Raising Glide from 0.472 to about 0.9 nearly doubles the product. Raising Grapple from 0.852 barely moves it. The same logic says Parry needs the next use. A late use just before a moment of need is massed practice, so it helps this fight more than it builds stability for later ones.
</details>

29. *Week 7 · compute.* (a) A mechanic has stability `s = 125` minutes. How long after its last use does recall fall below 0.8? (b) How many practice uses does a mechanic need so that recall is still at least 0.8 after a 45-minute gap?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 27.9 minutes. (b) Three.

(a) `e^(−Δ/125) = 0.8` gives `Δ = 125 × ln(1.25) = 27.9`.

(b) Need `s ≥ 45 / ln(1.25) = 201.7`. `20 × 2.5^k ≥ 201.7` gives `k ≥ ln(10.08) / ln(2.5) = 2.52`, so 3. Check: two uses give `e^(−45/125) = 0.698`, and three give `e^(−45/312.5) = 0.866`.
</details>

30. *Week 7 · design.* Choose a teaching pattern from the lecture's toolkit for each mechanic in an invented action RPG, and justify each with the model or an earlier week. (a) Dodge, needed hard in the first boss fight at minute 20. (b) Fast travel, used about once every 90 minutes. (c) A rune-combination system that is the game's main source of discovery. (d) Controls for genre veterans who already know the standard layout.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One defensible set:

- (a) Safe practice then test. Teach dodge in a low-risk room, require it several times before minute 20, and put one use shortly before the boss. The boss is a hard moment of need, so dodge needs stability and a short gap.
- (b) Contextual prompt at the travel point. With 90 minutes between uses, the forgetting curve will win unless the player gets many spaced uses. Knowledge in the world at the moment of need costs little screen space and no pace.
- (c) Delayed hint. Discovery is the fun, so a prompt would replace the retrieval and the pleasure. Show a hint only after the player has been stuck for a while, and accept that some players wait out the timer.
- (d) A skill check or skip, which keeps week 3's bored veteran. Make sure the skip doesn't also skip mechanics unique to this game.
</details>

## Week 8: Usability testing methods

31. *Week 8 · compute.* A tutorial has four sections. Section 1 has a non-blocking problem P1 (`p = 0.2`) and a blocker B1 (`b = 0.5`). Section 2 has a blocker B2 (`b = 0.3`). Section 3 has problem Q (`p = 0.7`). Section 4 has problem R (`p = 0.5`). (a) Compute `p_eff` for each problem and expected errors per tester on the original build. (b) Recompute after B1 is fixed, and after both blockers are fixed. (c) How many testers does a batch test need for a 90% chance of seeing Q on each of the three builds?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) P1 0.20, B1 0.50, B2 0.15, Q 0.245, R 0.175, total 1.27. (b) After B1: 0.20, 0, 0.30, 0.49, 0.35, total 1.34. After both: 0.20, 0, 0, 0.70, 0.50, total 1.40. (c) 9, then 4, then 2 testers.

(a) Reach of section 2 is `1 − 0.5 = 0.5`, so B2's `p_eff = 0.5 × 0.3 = 0.15`. Reach of sections 3 and 4 is `0.5 × 0.7 = 0.35`, so Q is `0.35 × 0.7 = 0.245` and R is `0.35 × 0.5 = 0.175`.

(b) Fixing B1 removes a problem met by half of testers, yet expected errors rise from 1.27 to 1.34, because twice as many testers now reach sections 2 to 4. Fixing B2 as well raises it to 1.40. That is the Age of Empires II spike, from reach alone.

(c) `n ≥ ln 0.1 / ln(1 − p_eff)`. Original `ln 0.1 / ln 0.755 = 8.2`, so 9. After B1, `ln 0.1 / ln 0.51 = 3.4`, so 4. After both, `ln 0.1 / ln 0.3 = 1.9`, so 2. Fixing early blockers buys sight of everything behind them.
</details>

32. *Week 8 · compute.* A tester answers the ten SUS items 3, 2, 4, 2, 3, 3, 4, 1, 3, 2. (a) Compute the score. (b) Another group's mean SUS for a different game's crafting screen is 78. Why shouldn't your team conclude its screen is less usable?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 67.5. (b) Different screens, testers and wording, and with five to eight testers SUS has wide uncertainty.

(a) Odd items `3 + 4 + 3 + 4 + 3 = 17`. Even items `2 + 2 + 3 + 1 + 2 = 10`. `SUS = 2.5 × (20 + 17 − 10) = 67.5`.

(b) SUS is a thermometer for comparing your own builds. The other group tested a different part of a different game with different recruits, and probably adapted the item wording differently. With a handful of testers, any rate or mean from a small sample is loose (MA102 week 13). Compare your build against your own next build, with the same wording.
</details>

33. *Week 8 · compute.* (a) After a fix, how many clean testers do you need for 95% confidence that a problem with `p = 0.15` is gone? (b) After four clean testers, what is your confidence for a problem that used to hit half of testers? (c) Eight clean testers after a fix give what confidence at `p = 0.1` and `p = 0.3`? (d) A test found 24 problems and fixed 21. It made 25 changes, 4 of which re-fixed an earlier change. Compute the impact and re-fix ratios.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 19. (b) 93.75%. (c) 57.0% and 94.2%. (d) Impact 87.5%, re-fix 16%.

(a) `1 − 0.85^m ≥ 0.95` gives `m ≥ ln 0.05 / ln 0.85 = 18.4`. Check: `0.85^18 = 0.054`, `0.85^19 = 0.046`. So 19.

(b) `1 − 0.5^4 = 0.9375`.

(c) `1 − 0.9^8 = 0.570` and `1 − 0.7^8 = 0.942`.

(d) Impact `21 / 24 = 0.875`. Re-fix `4 / 25 = 0.16`. The high impact ratio says the test changed the game. The re-fix ratio says about one first idea in six was wrong, which a RITE test catches because the next tester tries the fix.
</details>

34. *Week 8 · design.* Choose a method for each team, and say what to watch out for. (a) A live-service team wants to know whether its redesigned inventory is faster than the old one for typical players, with a fixed build. (b) A small team has a paper prototype of a new onboarding flow, a designer who attends every session, and can change screens in minutes. (c) A shooter team wants think-aloud data on a fast combat tutorial.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) A benchmark (summative) test on a fixed build, measuring time on task and success for old and new designs. Watch the sample. Rates and time differences need about 20 or more testers per condition, and the week 2 KLM prediction is a useful check on what the measured difference should be.
- (b) RITE. The conditions the Age of Empires II paper lists are present: decision-makers in the room, fast changes, and a team that has agreed to act. Watch for rare problems slipping through, and sort every issue into the four categories before changing anything.
- (c) Retrospective think-aloud, or live think-aloud with permission to go quiet in intense moments and prompts afterwards. Talking uses working memory the fight needs. Watch for reconstructed accounts in the retrospective version.
</details>

## Week 9: Heuristic evaluation for games

35. *Week 9 · compute.* On a project where one evaluator finds `λ = 0.28` of the problems: (a) how many evaluators does the team need to expect to find 80%? (b) If the interface has 30 problems, how many do three evaluators expect to find, and how many more does a fourth add? (c) What do five find?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5. (b) 18.8, and the fourth adds 3.1. (c) 24.2.

(a) `1 − 0.72^i ≥ 0.8` gives `i ≥ ln 0.2 / ln 0.72 = 4.9`, so 5.

(b) `30 × (1 − 0.72³) = 30 × 0.627 = 18.8`. The fourth adds `30 × 0.28 × 0.72³ = 3.1`.

(c) `30 × (1 − 0.72⁵) = 24.2`. The model assumes every problem is equally findable, which is never true. The problems left after five evaluators are the hard ones.
</details>

36. *Week 9 · compute.* Four evaluators inspect a group-finder screen. E1 finds problems 1, 2, 3, 5. E2 finds 1, 2, 4, 6, 7. E3 finds 1, 3, 4, 8. E4 finds 1, 2, 5, 9, 10. (a) Compute `S`, `f₁`, `f₂` and the Chao estimate. (b) Compute Lincoln-Petersen and Chapman for the split A = {E1, E2}, B = {E3, E4}. (c) Across all three ways to split four evaluators into two pairs, the Lincoln-Petersen estimates are 11.2, 12.0 and 14.0. What range do you report, and why is Chao at the top?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `S = 10`, `f₁ = 5`, `f₂ = 3`, Chao 14.2. (b) Lincoln-Petersen 11.2, Chapman 11.0. (c) Report "10 found, an estimated 11 to 14 in total".

(a) Counts per problem: problem 1 found by 4, problem 2 by 3, problems 3, 4 and 5 by 2, problems 6 to 10 by 1. So `f₁ = 5`, `f₂ = 3`, and `N̂ = 10 + 25 / 6 = 14.2`.

(b) A found {1, 2, 3, 4, 5, 6, 7}, `n_A = 7`. B found {1, 2, 3, 4, 5, 8, 9, 10}, `n_B = 8`. Shared {1, 2, 3, 4, 5}, `m = 5`. `7 × 8 / 5 = 11.2`. Chapman `8 × 9 / 6 − 1 = 11.0`.

(c) Problem 1, found by everyone, sits in every overlap and pulls Lincoln-Petersen down. Chao reads the five singletons as the visible tip of hard-to-find problems. When problems differ in findability, Lincoln-Petersen tends to underestimate, so report both as a range and say that both assume the evaluators worked independently.
</details>

37. *Week 9 · critique.* An evaluator flags this in a survival horror game: "The inventory does not pause the game (heuristic 3, user control and freedom). Severity 3. Fix: pause while the inventory is open." The lecture on HUDs notes that Dead Space keeps time running while you browse its holographic menus. How should the report handle this finding?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Record it, then decide whether it is a usability problem or deliberate challenge, and write down the reason.

If the design intent is that managing your inventory under threat is part of the tension, the finding describes intrinsic load, and pausing would delete part of the game. Mark it "deliberate challenge" with that reason, as the lecture's judgment section says to. Then check the extraneous parts separately. Can the player read the inventory quickly, find items without scanning a long unsorted list (week 1 and week 2), and see the threat while browsing? If testers can't tell that time is running, or lose items to confusing controls rather than to monsters, the challenge has become extraneous load. Fix the feedback and layout without pausing.

The severity rating should also come from the mean of at least three raters working from the consolidated list, not from the evaluator who found it.
</details>

38. *Week 9 · critique.* A studio runs a heuristic evaluation of its new-player raid interface with five evaluators, all veteran raiders from the design team. They work together in one room for an afternoon, and whoever finds a problem rates its severity on the spot. List what is wrong with the procedure and how to fix each part.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Not independent.** Working together makes the lists overlap, which inflates `m` and pushes both capture estimates down. It also removes the differences between evaluators that give the method its power. Have each evaluate alone, one to two hours, two passes, no sharing until all finish.
- **Wrong perspective.** Veteran raiders judge the screen for veterans, which is week 3's problem again. Include evaluators who can take the new player's view, and state who the evaluators were in the report.
- **No reach scenarios.** The lecture's missed problems needed a leader disconnect and atypical colour vision. Give every evaluator unusual states to try (disconnects, full bags, a colour-vision simulator) in their second pass.
- **Severity by the finder only.** One rater is unreliable, and ratings made while hunting are poor. Send the consolidated list to every evaluator afterwards and use the mean of at least three.
</details>

## Week 10: HUD and information design

39. *Week 10 · compute.* A 27-inch 16:9 monitor is 59.8 cm wide and 33.6 cm tall, viewed from 70 cm. A minimap sits with its centre 4 cm in from the top-right corner, and the player checks it 8 times a minute. (a) Compute θ, the cost of one check and the look-away share. (b) Put the minimap at the same relative position on a 65-inch TV (143.9 × 80.9 cm) viewed from 280 cm, and recompute. Use the lecture's model (`L = 200 ms`, `F = 250 ms`, `θ_f = 2.5°`, saccade `20 + 2.5θ` ms).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 22.4°, 802 ms, 10.7%. (b) 13.9°, 760 ms, 10.1%.

(a) Distance from the centre `d = √((29.9 − 4)² + (16.8 − 4)²) = √(25.9² + 12.8²) = 28.9 cm`. `θ = atan(28.9 / 70) = 22.4°`. `T = 2 × (200 + 20 + 2.5 × 22.4) + 250 = 802 ms`. `E = 8 × 0.802 / 60 = 0.107`.

(b) The element is at 43.3% of the width and 38.1% of the height out from the centre, so on the TV `d = √(62.3² + 30.8²) = 69.5 cm`. `θ = atan(69.5 / 280) = 13.9°`. `T = 760 ms`, `E = 10.1%`.

The TV corner is 8.5° closer to the eye, yet the look-away share barely changes, because most of a glance is latency and reading. Only crossing into the reading radius, or checking less often, moves `E` much.
</details>

40. *Week 10 · compute.* A shooter shows ammunition as a number at θ = 18°, checked 15 times a minute in firefights. Compute the look-away share now and for three proposals. (a) Move the number to 6°. (b) Move it to 2°, beside the crosshair. (c) Leave it at 18° and add a bar that pulses when the magazine is low, so players look only 3 times a minute. Rank them and name one cost of each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Now 19.5%. (a) 18.0%. (b) 6.25%. (c) 3.9%. The pulse wins, then the crosshair position, and moving to 6° barely helps.

Now: `T = 2 × (200 + 20 + 45) + 250 = 780 ms`, `E = 15 × 0.78 / 60 = 19.5%`.

(a) `T(6°) = 2 × (200 + 35) + 250 = 720 ms`, `E = 18.0%`. Cost: it now sits nearer the action and adds clutter, for 1.5 points.

(b) Inside the reading radius, `T = 250 ms`, `E = 6.25%`. Cost: it occludes the area the player aims at and adds a distractor to every search near the crosshair.

(c) `E = 3 × 0.78 / 60 = 3.9%`. Cost: resolution. A pulse says "low", not "7 rounds". Players who need the exact count still look.
</details>

41. *Week 10 · explain.* Place each in the Fagerholt and Lorentzon grid and predict one trade-off. (a) Glowing footprints on the ground showing the quest path. (b) A device on the character's wrist that shows ammunition. (c) The screen edges frosting over as body temperature falls. (d) A flat compass bar across the top of the screen.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) Spatial: in the 3D space, not in the fiction. It puts the information where it is used and cuts split attention, but it adds scene clutter and raises `N` for every search.
- (b) Diegetic: in the fiction and in the space. It fits the world and may sit near the action, but it is hard to resize or recolour for accessibility, and it is far from the crosshair unless the camera shows the wrist.
- (c) Meta: in the fiction's effect on the view, as a flat overlay. It is readable in the periphery and cheap to check, but low in resolution. It says "cold", not how many seconds are left.
- (d) Non-diegetic: outside the fiction, flat overlay. It is cheap to build, easy to make accessible and easy to read, but it sits at the screen edge, at a large θ.
</details>

42. *Week 10 · design.* (a) Compute the radius of the 2.5° reading circle in centimetres, and as a share of screen width, for a 55-inch TV at 250 cm (121.8 cm wide), a 24-inch monitor at 60 cm (53.1 cm wide) and a 7-inch handheld at 35 cm (15.5 cm wide). (b) A team wants to put health, ammunition and a cooldown ring within the reading radius on every platform. What does (a) imply for the PC layout?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) TV 10.9 cm, 9.0% of the width. PC 2.6 cm, 4.9%. Handheld 1.5 cm, 9.9%. (b) On PC the circle is half as wide relative to the screen, so the three elements must be much smaller or tighter around the crosshair, and they will cover more of what the player aims at.

(a) Radius `= D × tan 2.5°`. TV `250 × 0.0437 = 10.9 cm`, and `10.9 / 121.8 = 0.090`. PC `2.62 cm`, `0.049`. Handheld `1.53 cm`, `0.099`.

(b) A layout drawn as fractions of the screen for the TV will put the PC elements outside the reading radius. Either design a separate PC layout, or spend the centre on the one or two elements with the highest checks-per-minute and urgency, and give the rest a peripheral encoding that cuts `f`. Let players move and scale elements, since the team can't know every seat.
</details>

## Week 11: Accessibility guidelines

43. *Week 11 · compute.* Compute the WCAG contrast ratio and say whether each passes 4.5:1 for standard text, 3:1 for large text, and 7:1 for high-contrast mode. (a) White text on grass green `#5B8C3A`. (b) Gold `#FFD700` on night sky `#1B2233`. (c) Gold `#FFD700` on white. (d) Light grey `#E0E0E0` on mid grey `#9E9E9E`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.99:1, large text only. (b) 11.3:1, passes all three. (c) 1.40:1, fails all. (d) 2.03:1, fails all.

(a) `0x5B = 91`, `c = 0.357`, `lin = ((0.357 + 0.055)/1.055)^2.4 = 0.104`. Green `0x8C = 140` gives `lin = 0.262`. Blue `0x3A = 58` gives `lin = 0.042`. `L = 0.2126 × 0.104 + 0.7152 × 0.262 + 0.0722 × 0.042 = 0.213`. `C = 1.05 / 0.263 = 3.99`.

(b) `L(gold) = 0.699`, `L(night) = 0.016`. `C = 0.749 / 0.066 = 11.3`.

(c) `C = 1.05 / 0.749 = 1.40`. Gold text for speaker names works in dark scenes and vanishes in bright ones.

(d) `L = 0.745` and `0.342`. `C = 0.795 / 0.392 = 2.03`.
</details>

44. *Week 11 · compute.* The brightest scene behind the subtitle line in a game is a salt flat with `L = 0.85`. White subtitles sit on a black box. (a) What opacity keeps them at 4.5:1? At 7:1? (b) The shipped default is 70%. What contrast does it give over the salt flat? (c) Give one fix other than raising the default.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 78.4% and 88.2%. (b) 3.44:1. (c) A black outline on the letters, or darker art behind the subtitle area in that scene.

(a) `α ≥ 1 − 0.1833 / 0.85 = 0.784`. For 7:1, `1.05/7 − 0.05 = 0.10`, so `α ≥ 1 − 0.10 / 0.85 = 0.882`.

(b) `1.05 / ((1 − 0.7) × 0.85 + 0.05) = 1.05 / 0.305 = 3.44`. It fails for standard text.

(c) An outline guarantees contrast at the letter edges whatever the background, as For Honor's symbols and Immortals Fenyx Rising's text do in the lecture. A darker vignette behind the subtitle area changes `L` instead of `α`. Keep the 0 to 100% slider either way. The linear-light model is conservative, so measure the real result on a screen capture.
</details>

45. *Week 11 · compute.* XAG 101 sets a console minimum of 26 px at 1080p. (a) What visual angle, in arcminutes, does 26 px subtend on a 65-inch TV (80.9 cm tall) viewed from 300 cm? (b) On a 42-inch TV viewed from 250 cm? (c) Why does the guideline also require scaling to 200%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 22.3 arcminutes. (b) 17.3 arcminutes. (c) Designers don't know the player's screen or seat, and players do.

(a) One pixel is `80.9 / 1080 = 0.0749 cm`, so 26 px is 1.95 cm. `atan(1.95 / 300) = 0.372° = 22.3′`.

(b) A 42-inch 16:9 TV is 52.3 cm tall, so 26 px is 1.26 cm. `atan(1.26 / 250) = 0.289° = 17.3′`, which matches the lecture's "about 17".

(c) The same pixel height gives different angles on different setups. A minimum protects the typical case, and scaling lets the player with a small TV, a far couch or low vision fix their own case.
</details>

46. *Week 11 · critique.* A team marks item rarity only by colour: common items green `#388E3C`, cursed items red `#D32F2F`. In a review, one designer says "we'll add a colour-blind filter later", and another says "a subtitle background would make the game easier, so it should be off by default". Critique both remarks, with a number.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The luminance contrast between the two colours is 1.21:1, so for a player with red-green deficiency they can look almost the same. The fix is a second channel first, then colour options. The subtitle remark confuses accessibility with assist.

- **Colour.** Red-green deficiency collapses hue differences on that axis and leaves mostly luminance, and these two differ by only 1.21:1. That is the lecture's "Material red and green" trap. Guideline order: never carry essential information by colour alone (add an icon, a border shape or a text label for cursed items), then let players choose colours or presets. A filter alone still leaves colour-only information failing for some players, and XAG 103 notes that simulation filters don't replace testing with players.
- **Subtitles.** A subtitle background removes a barrier, reading text over a bright scene. It doesn't change the intended challenge. XAG 104 asks for a background the player can turn on, with opacity from 0 to 100%. Assist options, such as slowing time, change the challenge and are a separate decision.
</details>

## Week 12: Surveys and interviews

47. *Week 12 · compute.* True satisfaction with a feature is 55%. Satisfied players answer the survey at 6% and unsatisfied players at 15%. (a) What share does the survey show? (b) With 5,000 respondents, what is the Wilson 95% interval, and does it contain the truth? (c) In another survey, 62% of respondents are satisfied, and you know satisfied players answered twice as often. Estimate the truth.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 32.8%. (b) 31.6% to 34.2%, which misses 55% by about 21 points. (c) About 44.9%.

(a) `k = 0.06 / 0.15 = 0.4`. `odds_true = 0.55 / 0.45 = 1.222`. `odds_obs = 0.489`. `p_obs = 0.489 / 1.489 = 0.328`.

(b) With 1,642 satisfied of 5,000 the Wilson interval is 31.6% to 34.2%. The interval is narrow and wrong. Sample size shrinks sampling error and does nothing about who answered.

(c) `k = 2`. `odds_obs = 0.62 / 0.38 = 1.632`. `odds_true = 0.816`. `p = 0.816 / 1.816 = 0.449`.
</details>

48. *Week 12 · compute.* Telemetry says players are 30% new, 50% active and 20% lapsed. Survey respondents are 10% new, 75% active and 15% lapsed. Satisfied within each group: new 50%, active 80%, lapsed 25%. (a) Compute the raw and weighted satisfaction. (b) Give each group's weight. (c) Name two limits of the weighted number.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Raw 68.75%, weighted 60.0%. (b) New 3.0, active 0.67, lapsed 1.33. (c) It corrects only through these three groups, and the new-player group carries a large weight.

(a) Raw `0.10 × 0.50 + 0.75 × 0.80 + 0.15 × 0.25 = 0.6875`. Weighted `0.30 × 0.50 + 0.50 × 0.80 + 0.20 × 0.25 = 0.60`.

(b) Weight = population share ÷ respondent share: `0.30/0.10 = 3.0`, `0.50/0.75 = 0.67`, `0.20/0.15 = 1.33`.

(c) If the new players who answered are happier than those who didn't, the weighted figure is still too high. That bias runs through mood, which telemetry can't see. And each new respondent counts three times, so if only a handful answered, the result is noisy. Report the counts behind each group.
</details>

49. *Week 12 · compute.* (a) A survey pops up at the end of each match. Of 1,500 answers, 35% came from players who had just lost, and losses are 50% of matches. Estimate the response-rate ratio `k` between players after a win and after a loss, and say which way it biases "matchmaking feels fair". (b) How many interviews give a 90% chance of hearing a problem that 12% of players have? (c) What chance do four interviews give for a problem 20% of players have?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `k ≈ 1.86`. The survey overstates fairness. (b) 19. (c) 59%.

(a) Response rates are proportional to share of answers over share of matches: losers `0.35 / 0.5 = 0.7`, winners `0.65 / 0.5 = 1.3`. `k = 1.3 / 0.7 = 1.86`. Winners are more likely to call matchmaking fair and are overrepresented, so the observed share is too high. Showing the survey on the next launch, or to a random sample, would bring `k` nearer 1.

(b) `1 − 0.88^n ≥ 0.9` gives `n ≥ ln 0.1 / ln 0.88 = 18.01`. Check: `0.88^18 = 0.1002`, just above 0.1, so 19.

(c) `1 − 0.8^4 = 0.590`. Four interviews miss a problem held by one player in five about four times in ten, which is why lab 12 asks you to state that risk.
</details>

50. *Week 12 · critique.* Name the fault in each item and rewrite it. (a) "How much did you love the new housing system?" (b) "The housing editor was quick and intuitive." (c) "Would you pay for extra housing plots?" (d) "Was the housing UX consistent with genre affordances?"

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) Leading. It assumes enjoyment. Rewrite: "How would you rate the new housing system?" on a balanced scale from very poor to very good.
- (b) Double-barrelled. Quick and intuitive are two questions. Split it into "The housing editor let me do what I wanted quickly" and "The housing editor was easy to understand", each on a balanced agreement scale. Better still, measure speed with task timing (week 2).
- (c) Hypothetical. People predict their own spending badly. Ask about past behaviour, or measure it in telemetry.
- (d) Jargon. Players don't share the terms. Rewrite as a question about a specific recent episode: "Tell us about the last time you placed furniture. Did anything work differently from what you expected?"
</details>

## Week 13: Biometrics and eye tracking

51. *Week 13 · compute.* A competitive shooter session has 400 five-second windows. Coded states and hit rates: neutral 300 windows (`h = 0.06`), frustration 50 (`0.70`), excitement 40 (`0.75`), fear 10 (`0.80`). (a) Compute `P(state | peak)` for each state and the share of peaks from aroused states. (b) In the 20 windows after the player's own death, the coding is 3 neutral, 15 frustration, 2 excitement, 0 fear. In the 20 windows after a multi-kill, it is 4 neutral, 1 frustration, 15 excitement, 0 fear. Compute the leading state's share of peaks in each context. (c) What would a "peak means excitement" rule get right over the whole session?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Neutral 19.8%, frustration 38.5%, excitement 33.0%, fear 8.8%. Aroused 80.2%. (b) After a death, frustration 86.2%. After a multi-kill, excitement 92.3%. (c) One peak in three.

(a) Peaks: `300 × 0.06 = 18`, `50 × 0.70 = 35`, `40 × 0.75 = 30`, `10 × 0.80 = 8`, total 91. Shares `18/91`, `35/91`, `30/91`, `8/91`. Aroused `73 / 91 = 0.802`.

(b) After a death: peaks `0.18 + 10.5 + 1.5 + 0 = 12.18`, frustration `10.5 / 12.18 = 0.862`. After a multi-kill: `0.24 + 0.7 + 11.25 = 12.19`, excitement `11.25 / 12.19 = 0.923`.

(c) `30 / 91 = 33%`. Because the hit rates are close, the peak barely shifts the odds between aroused states. The game's event log does the discriminating. Physiology says when and how much, and context says what.
</details>

52. *Week 13 · compute.* (a) Tester A rests at 5.0 µS (SD 0.4) and reaches 6.2 µS at a boss reveal. Tester B rests at 10.2 µS (SD 1.2) and reaches 12.0 µS. Compute each z-score. Who responded more strongly? (b) Seven testers see a tutorial prompt. Three fixate it, and one of those can say what it said. Give the hit ratio with its Wilson 95% interval, and the recall share. Which goes in the headline?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) A 3.0, B 1.5. A responded more strongly, though B's raw rise was larger. (b) Hit ratio 3/7, Wilson 15.8% to 75.0%. Recall 1/7. Lead with recall and the count who never looked.

(a) `(6.2 − 5.0) / 0.4 = 3.0` and `(12.0 − 10.2) / 1.2 = 1.5`. Raw microsiemens would say B rose more, 1.8 against 1.2. Relative to each tester's own baseline, A's response is twice as large. Compare testers only after normalising.

(b) The Wilson interval for 3 of 7 is 15.8% to 75.0%. Even the upper end says a real share of players never looked. Only one tester in seven took the message in. The headline is "one of seven testers could say what the prompt said, and four never looked at it". A heatmap would glow over the prompt and hide both facts.
</details>

53. *Week 13 · critique.* A rhythm game proposal: "A wristband reads heart rate. When it rises, the song speeds up, so skilled players stay challenged." Critique it with this week's model and propose a safer design.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Heart rate indexes arousal, not skill or boredom. A player who misses notes and gets frustrated will have a rising heart rate, and the design will speed the song up for exactly that player. That is a positive feedback loop, as in Valve's Alien Swarm timer, which needed a decay factor.

Problems in order:

- **Reverse inference.** "Heart rate up" is read as "under-challenged", when frustration, excitement and plain movement all raise it. Rhythm games involve a lot of movement, a known confound.
- **Loop.** Arousal raises difficulty, which raises arousal. Without a cap or decay it runs away.
- **Baseline.** Resting heart rate varies between people, so a fixed threshold treats testers differently.

Safer design: adapt from performance, which the game already measures (accuracy over the last phrase), and use arousal, if at all, the way Left 4 Dead 2's Director did, to shape intensity peaks and quiet valleys, not to punish. If biofeedback stays, normalise each player to a rest baseline, cap the change, add a decay, and tell the player what the sensor does. Say in the consent form what is recorded.
</details>

54. *Week 13 · explain.* A team presents an eye-tracking heatmap in which the new quest marker glows bright red, and concludes "players see the marker". Explain two separate ways the conclusion could be wrong, and what the team should report instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **A heatmap is a sum.** One tester staring for three seconds makes a hot spot. The map can't show how many testers contributed. Report the hit ratio with its interval, and time to first fixation against a deadline.
- **Looked at is not seen.** The eye-mind hypothesis often fails in games. A tester can fixate a marker and not process it, as in the lecture's prompt study, where one of two testers who looked couldn't recall it. Covert attention works the other way, so a player can notice something they never fixated.

Report per tester: hit (yes or no), time to first fixation, whether it came before the deadline, and whether they could recall or act on the marker. Pair gaze with a second channel such as recall or behaviour.
</details>

## Week 14: UX research reporting

55. *Week 14 · compute.* Six testers played a co-op game. Use weights `1, 3, 10, 30` and bar `T = 1`. The Wilson 95% intervals for `x` of 6 are: 1 of 6, 3.0% to 56.4%; 2 of 6, 9.7% to 70.0%; 3 of 6, 18.8% to 81.2%; 4 of 6, 30.0% to 90.3%; 5 of 6, 43.6% to 97.0%. Compute `L`, `U` and the tier for: G1 hotbar keys unlabelled (5 of 6, severity 2); G2 accepting a party invite during a cutscene loses it for good (1 of 6, severity 4); G3 crafting fails with no message (3 of 6, severity 3); G4 map font too small (4 of 6, severity 1); G5 skipping a cutscene deletes the quest note (2 of 6, severity 3); G6 respawn point unclear (2 of 6, severity 2). Then compare with the lecture's F2, a blocker at 1 of 5.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Finding | `L` | `U` | Tier |
|---|---|---|---|
| G1 | 1.31 | 2.91 | Fix now |
| G2 | 0.90 | 16.91 | Investigate |
| G3 | 1.88 | 8.12 | Fix now |
| G4 | 0.30 | 0.90 | Backlog |
| G5 | 0.97 | 7.00 | Investigate |
| G6 | 0.29 | 2.10 | Investigate |

For example, G1: `0.436 × 3 = 1.31` and `0.970 × 3 = 2.91`. G2: `0.030 × 30 = 0.90` and `0.564 × 30 = 16.91`.

With five testers, a single blocker sighting has `L = 0.036 × 30 = 1.09` and clears the bar. With six, the lower bound of 1 of `n` falls to 3.0% and `L` to 0.90, so G2 drops to investigate. The tier rule is working as designed, since one sighting in six is weaker evidence than one in five. But G2 is a deterministic loss of progress. The lecture's judgment section says to take such bugs out of the sampling question. Have QA reproduce it, and if it reproduces every time, file it as a bug and fix it. Its `U` of 16.9 is also the largest in the table. Sort the investigate tier by `U`, so G2 comes first with a named next step.
</details>

56. *Week 14 · critique.* Rewrite this finding in the five-part form, inventing plausible evidence, and say what was wrong with it: "Crafting is broken and players hate it. Redo the crafting UI."

<details>
<summary>Answer and worked solution</summary>

**Answer:** The original has no count, mixes observation with opinion ("hate"), blames a feature rather than naming a problem, and prescribes a full redesign.

One good rewrite:

> **G3. Crafting fails with no message when a reagent is missing.** Severity 3 (major), 3 of 6 testers (Wilson 95%: 19% to 81%). Tier: fix now.
>
> *Observation.* P1, P4 and P5 pressed Craft, saw nothing happen, and pressed it again two to five times. P4 said "is it lagging?" (P4, 14:32). P5 left the station and bought a second copy of a reagent she already had (P5, 18:10 to 21:40).
>
> *Interpretation.* The button gives no feedback when a recipe is incomplete, so testers read the silence as a bug or lag, not as a missing ingredient.
>
> *Impact.* Up to four minutes lost, and one wasted purchase.
>
> *Recommendation.* Show which reagent is missing, next to the button, when Craft is pressed. Retest with the next build.
>
> *Evidence.* Clips G3-a to G3-c.

The rewrite keeps observation and interpretation in separate sentences, puts severity, count, interval and tier on one line, uses short marked quotes with timestamps, and offers a direction the owner can reject.
</details>

57. *Week 14 · compute.* After a fix for G3, a retest with 10 new testers shows 0 of 10 hitting the problem. The Wilson 95% upper bound for 0 of 10 is 27.8%. (a) What does the rule of three give? (b) What do you write in the tracker? (c) Would you close it? Would you close a severity 4 finding on the same evidence? (d) What upper bound would 0 of 20 give?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 30%. (b) "0 of 10 after fix in build X (Wilson 95%: 0% to 28%)." (c) Not on the retest alone, because G3's upper impact is still above the bar. Close it once a reproduction confirms the fix. Keep a blocker open longer. (d) 16.1%.

(a) `3 / 10 = 0.30`, a rougher bound close to Wilson's.

(c) For severity 3, `U = 0.278 × 10 = 2.78`, which is still above a bar of 1. So the retest alone does not close it. Close it if the fix is also confirmed by a reproduction (crafting with a missing reagent now shows the message every time), which is deterministic. For a severity 4 finding, `0.278 × 30 = 8.3`, so keep it open until reproduction confirms the fix and watch telemetry after launch.

(d) The Wilson upper bound for 0 of 20 is 16.1%.
</details>

58. *Week 14 · critique.* After seeing the tier table, a producer asks the researcher to (a) order the report by how many testers hit each problem, "because that's what the team understands", and (b) raise the bar to `T = 2` "so we have fewer fix-now items this sprint". Respond to both.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

(a) Sorting by frequency buries rare, severe problems. In the lecture's example, the softlock fell to fifth of six and a cosmetic icon rose to second. A reader who schedules the top three would ship the blocker. Keep the tiers, and inside each tier sort by `U`, then by cost. If the team wants frequency, show it as a column with the count and interval, never as the order.

(b) The bar states what the team can afford, and it must be set before the evidence arrives. Changing it after seeing the data lets anyone make findings appear or disappear. In the lecture's example, `T = 2` moves every fix-now finding to investigate. If capacity really is short, keep the bar, and use the cost column to decide which fix-now items go this sprint and which next. Record that decision as a scheduling choice, not a change in the evidence.
</details>

## Across weeks: viva questions

59. *Weeks 1, 10 and 11 · design.* A console game shows health as a small green number in the top-left corner. On the lecture's TV setup that corner is at θ = 13.6°, and in boss fights players check it about 20 times a minute. Propose a redesign of the health display and justify it with three models from the course: glance cost, pop-out, and contrast or colour vision. Give the look-away share before and after, assuming your design cuts checks to 4 a minute.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One good redesign is a health bar under the character with colour bands, a shape change and a pulse at low health, plus a heartbeat sound near death, and the exact number shown next to the bar.

- **Glance cost.** Before: `T = 2 × (200 + 20 + 34) + 250 = 758 ms`, `E = 20 × 0.758 / 60 = 25.3%`. After, with 4 checks a minute: `E = 4 × 0.758 / 60 = 5.1%` even if the bar stayed in the corner. Placing it under the character, near the action, lowers `T` a little more. The big gain comes from `f`.
- **Pop-out.** A pulse is motion, a basic feature the periphery detects well. Reserve it for low health so it stays unique, since pop-out is a budget.
- **Contrast and colour vision.** Green-to-red bands alone fail for red-green deficiency. Add a second channel (the bar's fill level, a cracked border shape at low health, the sound). Check the bar against the brightest arena floor for at least 3:1 as a large element, with an outline if it fails.

The exact number stays for decisions that need it ("can I survive one more hit?"), but the player now looks at it only when the pulse says to.
</details>

60. *Weeks 3, 8, 12 and 14 · design.* Telemetry shows that 40% of players who finish the second dungeon of an invented MMO never start the third. Design a two-week study to find out why, and say how you will report it. Name the methods, sample sizes and what each can and cannot tell you.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One defensible plan:

1. **Telemetry first (days 1 to 2).** Split the leavers by what they did in the second dungeon (deaths, time, group disbands) and after it (logins, other activities). This finds where to look, not why. It is the week 3 funnel reading.
2. **Survey of leavers and stayers (days 2 to 7).** Invite a random sample of both groups by the same method, record invitation counts per group, and compute response rates. Ask about specific recent episodes, with no hypothetical items. Weight by group, and state `k` and the direction of remaining bias (week 12).
3. **Interviews (days 5 to 10).** Ten or twelve leavers. For a reason held by 20% of leavers, 10 interviews give `1 − 0.8^10 = 89%` to hear it at least once. Code into themes, counting participants.
4. **Moderated usability test (days 8 to 12).** Five to eight new testers play into the third dungeon's entry. Fix clear blockers between testers (RITE). This finds interface and wayfinding problems that stop players reaching the third dungeon.
5. **Report (days 13 to 14).** Triage with weights and bar set on day 1. One-page summary with fix-now findings, counts with Wilson intervals, "investigate" items each with a next step, method and limits. For example, recruited testers are not leavers, and interviews can't estimate prevalence.

The design principle across weeks is to ask about experiences, measure behaviour, and state who answered.
</details>

61. *Weeks 4, 5 and 6 · critique.* A live-ops proposal for an invented competitive game: "Win 3 matches a day to open a streak chest of random cosmetics. Missing a day resets the streak. Players can buy a reroll of the chest with premium currency. Our survey says 70% of players are Achievers, so they'll love it." Using `μ = 60` and `σ = 40` minutes a week of play, critique the proposal with all three weeks and propose one change per week.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Week 4.** The chest is performance-contingent (wins) with an engagement-style streak loss on top, the most controlling combination in the lecture. At the engagement value `d = −0.40`, play after the event would drop to `60 − 0.40 × 40 = 44` minutes a week, a loss of 16 minutes a week for as long as it lasts. Performance rewards also report failure to the players who can't win three a day. Change: add a grace day, or reward personal improvement rather than wins.
- **Week 5.** The chest is a variable-ratio reward, and the reroll puts money into the draw. The checklist answers "yes" to money in and "no stopping point", and exit costs a streak. Change: publish odds as "1 in N" at the reroll button, cap the worst case with a visible counter, or sell the cosmetics directly.
- **Week 6.** "70% Achievers" needs its instrument. If it was forced choice, it is a ranking, not a level, and many players have no primary motivation (43% in Yee's data). Change: measure with rating-scale items and report overlapping segments. Then check with telemetry whether the players the chest targets actually play for wins.

A reviewer should also ask for a holdout group, because the dashboard will show the event's uplift and hide its after-effect.
</details>
