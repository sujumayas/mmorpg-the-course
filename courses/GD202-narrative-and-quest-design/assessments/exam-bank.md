# GD202 · Exam bank: quiz, practice and viva questions

GD202 has no written exam. The grade comes from the dialogue exercises (40%, [dialogue-exercises-brief.md](dialogue-exercises-brief.md)) and the final quest chain (60%, [quest-chain-brief.md](quest-chain-brief.md)). This bank has three jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one analysis or critique question.
- **Showcase viva.** In week 15 each student defends their quest chain. One of the examiners' questions comes from this bank, rewritten with the numbers from your own chain.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **analysis**: explain why a model behaves the way it does, with a number as evidence.
- **design**: choose values that meet a stated goal and show that they meet it.
- **critique**: find what is wrong with a proposal and say how to fix it.

All story content in this bank is invented. Every fact about a shipped game comes from the lecture of the tagged week, which cites its source and version. Every number was recomputed in Python from the lectures' own models, and every code block runs as shown with `.venv/bin/python`. Write your own answer before you open the solution.

---

## Week 1: Story, plot and narration

Lecture: [w01, story vs narrative vs plot](../lectures/w01-story-vs-narrative-vs-plot.md).

1. *Week 1 · compute.* Use the eight-event lighthouse story from the lecture. (a) Compute `I` and `S` for the telling `[2, 1, 4, 3, 6, 5, 8, 7]`. (b) Compute `I` and `S` for `[4, 5, 6, 7, 8, 1, 2, 3]`. (c) Telling (b) has the same `I` as the lecture's mystery telling `[5, 6, 7, 2, 3, 4, 1, 8]`. Compute the open-questions profile of each and say how they would feel different to a player.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `I = 4`, `S = 0.14`. (b) `I = 15`, `S = 0.54`. (c) Profiles `[1, 2, 3, 4, 5, 5, 5, 0]` for (b) and `[1, 2, 3, 4, 5, 6, 0, 0]` for the mystery.

(a) Each adjacent pair is swapped once, and no other pair is out of order. Four swaps give `I = 4`, and `S = 4/28 = 0.14`.

(b) Each of the five events 4 to 8 appears before each of 1, 2 and 3, so `I = 5 × 3 = 15` and `S = 15/28 = 0.54`.

(c) An event is open when some smaller story number has not been shown yet. In (b) the questions build to 5 and stay there for two more steps, because events 1 and 2 arrive but event 3 is still missing. Then all five close at once. It plays like one long flashback delivered at the end. In the mystery telling the count climbs to 6, and the single event 1 closes all of them. Same count of inversions, different shape. The count says how far a telling departs from story order, not where the debt sits or when it is paid.
</details>

2. *Week 1 · compute.* Predict what this code prints, then run it. What does the second profile say about the pacing of that telling?

```python
def open_questions(plot):
    shown, out = set(), []
    for e in plot:
        shown.add(e)
        out.append(sum(1 for x in shown
                       if any(c not in shown for c in range(1, x))))
    return out

print(open_questions([6, 1, 2, 3, 4, 5, 7, 8]))
print(open_questions([2, 1, 4, 3, 6, 5, 8, 7]))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[1, 1, 1, 1, 1, 0, 0, 0]
[1, 0, 1, 0, 1, 0, 1, 0]
```

The first is the lecture's in medias res telling. Event 6 stays open until event 5 is shown.

In the second, every inversion is an effect shown one beat before its cause. Each question opens and closes on the next step. That is four tiny promises paid at once, which reads as choppy editing, not suspense. The profile never climbs above 1, so the player never has to hold anything.
</details>

3. *Week 1 · analysis.* A player-ordered game has 10 story blocks, found in any order. (a) What is the expected inversion count of a uniformly random order? (b) One player happens to see block 7 first and then 1 to 6 and 8 to 10 in order. Compute `I` and `S`. (c) The designer cannot set `S` for a single player. What can the designer control instead? Use the lecture's Her Story case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 22.5. (b) `I = 6`, `S = 0.13`. (c) Which orders are possible.

(a) There are `10 × 9 / 2 = 45` pairs, and a random order reverses each pair with chance 1/2, so the expected `I` is 22.5 and the expected `S` is 0.5.

(b) Block 7 appears before the six blocks 1 to 6. Nothing else is out of order. `I = 6` and `S = 6/45 = 0.13`.

(c) The designer controls the interface that hands out blocks. In Her Story, clips come back only for words the player types, so the most revealing clips tend to reach players who already suspect something. The designer shapes the distribution of plots without fixing any one of them.
</details>

4. *Week 1 · compute.* A zone offers 6 quests that players can take in any order. (a) How many plot orders are possible? (b) The designer gates one quest to come first and another to come last. How many orders now? (c) What does the difference mean for the writer of the four middle quests?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 720. (b) 24. (c) The middle four must still work in any of 24 orders.

(a) `6! = 720`.

(b) The first and last are fixed, so only the middle four vary: `4! = 24`.

(c) The gates buy the writer a guaranteed opening and a guaranteed close, which every player sees in the same place. The four middle quests may still come in any order, so each can lean on the opening quest but not on a sibling. Week 8 turns this into the spine and ribs of a zone.
</details>

## Week 2: The player as co-author

Lecture: [w02, the player as co-author](../lectures/w02-the-player-as-co-author.md).

5. *Week 2 · compute.* A chapter has `N = 8` scenes of `w = 1,200` words. A binary choice (`b = 2`) comes at the end of scene `s = 3`. Callbacks are `k = 5` lines of `a = 50` words. For each of the four strategies give `W`, `V/W`, extra words, `R` and extra words per acknowledgement.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Strategy | `W` | `V/W` | Extra | `R` | Extra per acknowledgement |
|---|---|---|---|---|---|
| Branch | 15,600 | 61.5% | 6,000 | 5 | 1,200 |
| Acknowledge | 9,850 | 97.5% | 250 | 5 | 50 |
| Payoff | 10,800 | 88.9% | 1,200 | 1 | 1,200 |
| Acknowledge + payoff | 11,050 | 86.9% | 1,450 | 6 | 242 |

`V = 8 × 1,200 = 9,600` for every strategy.

Branch: `W = 3 × 1,200 + 2 × 5 × 1,200 = 3,600 + 12,000 = 15,600`, `R = N − s = 5`.

Acknowledge: `W = 9,600 + 1 × 5 × 50 = 9,850`, `R = 5`.

Payoff: `W = 9,600 + 1,200 = 10,800`, `R = 1`.

Combined: `W = 9,600 + (250 + 1,200) = 11,050`, `R = 6`, `1,450 / 6 = 241.7`.
</details>

6. *Week 2 · analysis.* Show from the formulas that full branching always costs `(b − 1) × w` extra words per acknowledgement, whatever `N` and `s` are. What is the matching figure for callback lines, and what is the ratio between the two when `w = 1,200` and `a = 50`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Branching costs `(b − 1)w` per acknowledgement and callbacks cost `(b − 1)a`. The ratio is `w / a = 24`.

Branching writes `s·w + b(N − s)w`. One player sees `N·w`. The extra is `s·w + b(N − s)w − N·w = (b − 1)(N − s)w`. Branching gives `R = N − s` acknowledgements, so the cost per acknowledgement is `(b − 1)w`. The choice point cancels out.

Acknowledgement writes `(b − 1)·k·a` extra for `R = k`, so the cost per acknowledgement is `(b − 1)a`.

The ratio is `w / a`, independent of `b`, `k`, `N` and `s`. With 1,200-word scenes and 50-word callbacks it is 24. That is why the lecture says the factor grows with scene length: longer scenes make each branched acknowledgement dearer, while a callback line stays the same size.
</details>

7. *Week 2 · design.* A producer allows 8% extra writing on a chapter of `N = 12` scenes of 900 words, for one binary choice with 40-word callbacks. (a) Can you afford the acknowledge + payoff strategy with a full-length payoff scene? (b) What is the largest `k` with acknowledge only? (c) Propose a way to keep one heavy acknowledgement inside the budget, and give its `k`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) No. (b) `k = 21`. (c) A half-length payoff variant of 450 words plus `k = 10` callbacks.

The budget is `0.08 × 12 × 900 = 864` words.

(a) A full payoff variant alone costs 900 words, more than 864, so no.

(b) `40k ≤ 864` gives `k ≤ 21.6`, so 21.

(c) The model writes the payoff as one whole scene in `b` versions, but only the part that differs needs a second version. If the payoff scene shares its first half and diverges for 450 words, the cost is `450 + 40k ≤ 864`, so `k ≤ 10.35` and `k = 10`. That gives 11 acknowledgements, one of them heavy. Any design that keeps one heavy acknowledgement and shows the arithmetic under 864 words is right.
</details>

8. *Week 2 · critique.* A studio's flag ledger for one episode has three rows. Flag `spared_smuggler` is written in scene 2 and read in scenes 5 and 9. Flag `burned_letter` is written in scene 4, the game shows "Ashe will remember that", and nothing reads it. Flag `paid_toll` is read in scene 3 and written in scene 6. Name each problem in the lecture's terms, give the cheapest fix for each, and classify these player actions as select, perform, express or retell: (a) designing your family crest; (b) a guard captain grumbling that nobody saw the intruder, after you sneaked in; (c) a guild writing a history page about its first boss kill; (d) picking "Let him go" from a menu.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `spared_smuggler` is fine. `burned_letter` is a broken promise. `paid_toll` is a bug. (a) express, (b) perform, (c) retell, (d) select.

`burned_letter` has a notification and no read. The player expects a result that never comes, which players call lying. The cheapest fix is one callback line on the critical path that reads the flag, for example Ashe mentioning the letter at the next meeting.

`paid_toll` is read before it is written, so in scene 3 it is always false. That is a read with no matching earlier write, which the lecture calls a bug. Move the write before scene 3, or move the read after scene 6.

In (b) the guard's line is an acknowledgement of a performance. The player did something, and a flag set by the stealth system is read by a line.
</details>

## Week 3: Branching structures and the combinatorial explosion

Lecture: [w03, branching structures](../lectures/w03-branching-structures-and-the-combinatorial-explosion.md). Interactive: [branch explosion calculator](../examples/w03-branch-explosion.html).

9. *Week 3 · compute.* A pure tree has `b = 4` options per choice and depth `d = 3`. Give nodes, endings, nodes seen and share seen. At 250 words per node, how many words are written and how many does one player read?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 85 nodes, 64 endings, 4 seen, share 4.7%. 21,250 words written, 1,000 read.

Nodes `1 + 4 + 16 + 64 = 85`, or `(4^4 − 1)/(4 − 1) = 255/3 = 85`. Endings `4^3 = 64`. Seen `d + 1 = 4`. Share `4/85 = 4.7%`.

Words: `85 × 250 = 21,250` written, `4 × 250 = 1,000` read.
</details>

10. *Week 3 · compute.* A structure has `b = 2`, `d = 8` and folds back every `k = 2` choices. Give nodes, endings, paths, nodes seen and share seen, and compare the node count with the pure tree.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 28 nodes, 4 endings, 256 paths, 12 seen, share 42.9%. The pure tree has 511 nodes.

`grow(2) = 2 + 4 = 6` and `m = 8/2 = 4` segments. Nodes `1 + (m − 1)(grow + 1) + grow = 1 + 3 × 7 + 6 = 28`. Endings `2^2 = 4`. Paths `2^8 = 256`. Seen `d + d/k = 8 + 4 = 12`. Share `12/28 = 42.9%`.

The pure tree has `2^9 − 1 = 511` nodes for the same 256 paths, 18 times as many.
</details>

11. *Week 3 · design.* Your quest has a budget of 7,500 words at 250 words per node. Players should make 6 choices of 3 options each. Which fold values `k` fit? How many nodes are left for acknowledgements, and how many paths does the player get?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Only `k = 1` fits, with 24 nodes, leaving 6 nodes (1,500 words). Paths stay at 729.

The budget is `7,500 / 250 = 30` nodes. With `b = 3`, `d = 6`:

| `k` | Nodes |
|---|---|
| 1 | 24 |
| 2 | 39 |
| 3 | 80 |
| 4 | 134 |
| 5 | 368 |
| 6 (pure tree) | 1,093 |

For `k = 1`: `1 + 5 × (3 + 1) + 3 = 24`. For `k = 2`: `grow = 12`, `m = 3`, `1 + 2 × 13 + 12 = 39`, already over.

The 6 spare nodes pay for week 2's callback lines and one heavy payoff after the bottlenecks. Paths are `3^6 = 729` whatever `k` is.
</details>

12. *Week 3 · analysis.* A quest is a chain of 10 nodes. You add one unmerged binary branch. How many extra nodes does it cost after node 3? After node 8? What about a three-way branch after node 8? What rule of thumb does this give?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 7, 2 and 4 extra nodes. Branch late.

A single unmerged branch after node `s` of an `N`-node chain costs `(b − 1)(N − s)` extra nodes. After node 3: `1 × 7 = 7`. After node 8: `1 × 2 = 2`. Three-way after node 8: `2 × 2 = 4`.

A late three-way branch costs less than an early two-way one. Put expensive divergence near the end, where little is left to duplicate, and fold early splits back fast.
</details>

13. *Week 3 · analysis.* Name the pattern from Ashwell's catalog for each invented design, give it in the model's terms, and say what it costs. (a) A 40-minute adventure where the player picks one of two sisters to follow at the start, and each sister's story is linear. (b) Every scene ends in a three-way choice, the options rejoin at the next scene, and flags remember what was picked. (c) A linear prison escape where most side choices end in a quick capture and a restart.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) sorting hat, (b) branch and bottleneck, (c) gauntlet.

(a) One early branch with `b = 2` and huge nodes. Share seen is about half of the post-choice content. High cost, but predictable, and the fork needs a clear signal so players know the other story exists.

(b) `k = 1` with `b = 3`, plus flags. Nodes grow linearly in `d`, paths stay at `3^d`. Cheap in content, but the flags must be read after each bottleneck or the choices feel cosmetic.

(c) A chain with short dead-end branches. Cheap. Choices feel risky, but they rarely change the story.
</details>

## Week 4: Dialogue systems and state flags

Lecture: [w04, dialogue systems and state flags](../lectures/w04-dialogue-systems-and-state-flags.md). Interactive: [rule matcher](../examples/w04-rule-matcher.html).

14. *Week 4 · compute.* A ferry-keeper reads three flags `a`, `b` and `c`. Her rules are R0 (no conditions), R1 (`a`), R2 (`b`), R3 (`a`, `b`), R4 (`a`, `c`) and R5 (`b`, `c`). Using "most conditions wins", find the winner in all 8 states. How many ties, silent states and dead rules are there? Which state other than all-false falls back to R0, and what should the writer decide about it?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| a | b | c | Winner |
|---|---|---|---|
| F | F | F | R0 |
| F | F | T | R0 |
| F | T | F | R2 |
| F | T | T | R5 |
| T | F | F | R1 |
| T | F | T | R4 |
| T | T | F | R3 |
| T | T | T | tie R3, R4, R5 |

One tie, no silent states, no dead rules. R0 wins two states.

In the all-true state, R3, R4 and R5 all match with 2 conditions, a three-way tie. No state is silent because R0 matches everything. Every rule wins at least one state alone, so none is dead.

The state with only `c` true matches only R0, because no rule reads `c` alone. That is the fallback working as designed, but the writer should decide whether `c` on its own deserves a line. If it does, add R6 on `c`.
</details>

15. *Week 4 · compute.* An NPC has a fallback plus one rule for every pair of `k` flags, and no single-flag rules. (a) For which states is there a tie? (b) How many tied states are there for `k = 4` and for `k = 5`? (c) How many states does the fallback win?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) States with 3 or more flags true. (b) 5 of 16 and 16 of 32. (c) `1 + k` states.

(a) A state with `j` flags true matches `C(j, 2)` pair rules, each scoring 2. With `j = 2` exactly one pair rule matches and wins. With `j ≥ 3` at least three pair rules match, all at score 2, so the state ties.

(b) Tied states `= Σ_{j≥3} C(k, j)`. For `k = 4`: `C(4,3) + C(4,4) = 4 + 1 = 5`. For `k = 5`: `10 + 5 + 1 = 16`.

(c) States with 0 or 1 flag true match no pair rule, so the fallback wins `1 + k` of them: 5 for `k = 4`. The ties sit in the states where many flags are true, which is late game. Test there first.
</details>

16. *Week 4 · compute.* A lock-keeper's lines read a quest stage with values 0, 10, 20, 30 and 40, a visit counter tested at 0, 1, 2 and 3 or more, and three booleans `repair_accepted`, `repair_done` and `repair_rewarded`. (a) How many states must a checker enumerate? (b) The three booleans are ordered steps of one side quest. How many of their combinations are legal? (c) Replace them with a stage. What is the new state count?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 160. (b) 4 of 8. (c) 80.

(a) `5 × 4 × 2 × 2 × 2 = 160`.

(b) The legal combinations are none, accepted, accepted and done, and all three. The other 4 (such as rewarded but not done) should never happen, but a rule will still match them if a bug sets one.

(c) A stage with values 0, 10, 20, 30 has exactly the 4 legal values: `5 × 4 × 4 = 80`. The state space halves and the illegal states disappear.
</details>

17. *Week 4 · critique.* Two bugs from a playtest. (a) A blacksmith says "Third time today? Sit down." on every visit from the third onward, for the rest of the game. Her rule tests `visits >= 3`. (b) A reeve praises the player for repairing the sluice gate. His rule tests `GetStage(sluice) >= 20`, where 20 means "gate repaired". A late change added a branch where the player bribes the foreman and jumps from stage 10 to stage 30. Explain each bug and fix it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) The condition should be `== 3`. (b) The rule should test whether stage 20 itself was done.

(a) `>= 3` fires on every visit from the third on, which is right for "you keep coming back" lines and wrong for a line about the third visit. Use `visits == 3`, and add a separate escalation line for `>= 4` if the joke should continue.

(b) Skyrim's `GetStage` returns the highest stage completed. A player on the bribe branch returns 30 without ever doing stage 20, so the reeve praises a repair that never happened. Test stage 20 directly (Skyrim's `GetStageDone` does this) or add a separate fact for the repair. Once steps can happen out of order, one "highest stage" number loses information.
</details>

## Week 5: Characters and companions

Lecture: [w05, characters and companions](../lectures/w05-characters-and-companions.md). Interactive: [approval walk](../examples/w05-approval-walk.html).

18. *Week 5 · compute.* A companion has `n = 16` approval events of `s = 5` and a friendship threshold `T = 40`. (a) How many agreements does the player need? (b) Give the exact chance for a `p = 0.5` player. (c) Give the mean, SD and chance of reaching `T` for `p = 0.7` and `p = 0.8`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12. (b) 2,517 / 65,536, about 3.8%. (c) `p = 0.7`: mean +32, SD 18.3, 45.0%. `p = 0.8`: mean +48, SD 16.0, 79.8%.

(a) `5(2K − 16) ≥ 40` gives `2K − 16 ≥ 8`, so `K ≥ 12`.

(b) `[C(16,12) + C(16,13) + C(16,14) + C(16,15) + C(16,16)] / 2^16 = (1,820 + 560 + 120 + 16 + 1) / 65,536 = 2,517 / 65,536 = 3.84%`.

(c) Mean `s·n·(2p − 1)`: `5 × 16 × 0.4 = 32` and `5 × 16 × 0.6 = 48`. SD `2s·√(n·p·(1 − p))`: `10 × √3.36 = 18.3` and `10 × √2.56 = 16.0`. The binomial tail `P(K ≥ 12)` is 45.0% at 0.7 and 79.8% at 0.8.

The mean at 0.7 is only 8 points short of the threshold, yet fewer than half reach it. The payoff depends on crossing a threshold, not on the average.
</details>

19. *Week 5 · compute.* A companion's 12 events have uneven steps. Four events are +10 on agreement and −5 on disagreement, six are +5 or −5, and two are +2 or −10. (a) What is the highest approval a player can reach? (b) What is the mean final approval at `p = 0.5` and at `p = 0.6`? (c) The exact chance of reaching +30 is 8.9% at `p = 0.5` and 52.1% at `p = 0.7`. Explain in one sentence why the `p = 0.5` player still ends slightly positive.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) +74. (b) +2.0 and +16.4. (c) The generous events outweigh the harsh ones.

(a) All agreements: `4 × 10 + 6 × 5 + 2 × 2 = 74`. A threshold above 74 is unreachable.

(b) Each event contributes `p × agree + (1 − p) × disagree`. At `p = 0.5`: the +10/−5 events give 2.5 each, the ±5 events give 0, and the +2/−10 events give −4 each, so `4 × 2.5 − 2 × 4 = 2.0`. At `p = 0.6`: `4 × 4 + 6 × 1 + 2 × (−2.8) = 16 + 6 − 5.6 = 16.4`.

(c) The four events that pay more than they cost add 10, and the two that cost more than they pay take away 8, so an indifferent player drifts up by 2. The exact walk (lab 05's method) gives the threshold chances quoted.
</details>

20. *Week 5 · analysis.* In a Baldur's Gate 3 style meter, a companion leaves for good the first time approval reaches −50. A player with `p = 0.3` meets `n = 20` events of `s = 5`. (a) Using the closed form, what is the chance that final approval is −50 or lower? (b) A step-by-step walk that stops at the wall gives 44.3%. Why is it higher than (a), and which number should the designer use?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 41.6%. (b) The walk counts players who touch the wall and would later have recovered. Use 44.3%.

(a) Final approval `5(2K − 20) ≤ −50` needs `K ≤ 5`. `P(K ≤ 5)` for `K ~ Binomial(20, 0.3)` is 41.6%.

(b) The closed form looks only at the end. Some players dip to −50 partway through and then climb back. In the game the companion has already left by then. The wall makes the meter path-dependent, as caps do in the lecture's section 4, so you must simulate the walk step by step. About 2.7 extra players in 100 lose the companion that the closed form says keep them.
</details>

21. *Week 5 · compute.* A meter is capped at +100. A companion stands at +70. Compare the final approval after +20, +20, −30 with the same steps in the order −30, +20, +20. What is the uncapped result, and what does the difference teach?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 70 against 80. Uncapped, both end at 80.

First order: `70 + 20 = 90`, `+20 = 110`, clamped to 100, `−30 = 70`. Second order: `70 − 30 = 40`, `+20 = 60`, `+20 = 80`.

The cap throws away 10 points of approval in the first order. With a binding cap the order of events matters, not only their count. A cap stops players banking approval early and coasting, which keeps late choices meaningful.
</details>

22. *Week 5 · compute.* A game has 6 companions, a party of the player plus 2, 80 reactable events and 2 variants per event. (a) How many reaction lines are written if every companion reacts to every event? (b) What share does a player who never changes party hear? (c) How many banter pairs are there? (d) The team tiers the events: 20 major events get lines from all 6 companions, and 60 minor events get lines from only the 2 companions whose values they touch. How many lines are written now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 960. (b) 16.7%. (c) 15. (d) 480.

(a) `6 × 80 × 2 = 960`.

(b) The player hears 2 companions, one variant each: `2 × 80 = 160`, which is `160 / 960 = 16.7%`.

(c) `6 × 5 / 2 = 15`.

(d) `6 × 20 × 2 + 2 × 60 × 2 = 240 + 240 = 480`. Half the writing. On minor events some party members stay silent, and week 4's fallback lines can cover them.
</details>

## Week 6: Quest anatomy

Lecture: [w06, quest anatomy](../lectures/w06-quest-anatomy-hook-objective-complication-reward.md). Interactive: [quest detour](../examples/w06-quest-detour.html).

23. *Week 6 · compute.* Use the classic-era World of Warcraft decay from the lecture. A level-24 player looks at a level-17 quest listed at 2,500 XP, with 4 minutes of travel and 6 of task. The baseline is `r₀ = 180` XP per minute. (a) What does the quest pay, and does it pass? (b) What is the smallest listed XP that passes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,500 XP at 150 per minute. It fails. (b) 3,000 XP.

(a) `Δ = 24 − 17 = 7`, so `m = 0.6` and the quest pays `2,500 × 0.6 = 1,500`. Rate `1,500 / 10 = 150`, below 180.

(b) It must pay `180 × 10 = 1,800`. At 60%, `1,800 / 0.6 = 3,000`, and 3,000 × 0.6 is exactly 1,800, so rounding does not bite.
</details>

24. *Week 6 · compute.* A level-23 player with `r₀ = 220` faces this invented board. Compute XP paid, minutes and rate for each quest. Which fail? Sort the board by listed XP and by rate. Then give each rate with a mount that halves travel.

| Quest | Level | Listed XP | Travel | Task |
|---|---|---|---|---|
| Reedcutter's plea | 21 | 2,400 | 3 | 7 |
| Heron hunt | 16 | 3,000 | 2 | 6 |
| Lockkeeper's key | 23 | 5,200 | 8 | 16 |
| Mill letter | 19 | 700 | 1 | 2 |

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Quest | `Δ` | Paid | Minutes | Rate | Pass at 220? | Rate with mount |
|---|---|---|---|---|---|---|
| Reedcutter's plea | 2 | 2,400 | 10 | 240.0 | yes | 282.4 |
| Heron hunt | 7 | 1,800 | 8 | 225.0 | yes | 257.1 |
| Lockkeeper's key | 0 | 5,200 | 24 | 216.7 | no | 260.0 |
| Mill letter | 4 | 700 | 3 | 233.3 | yes | 280.0 |

By listed XP the order is Lockkeeper's key, Heron hunt, Reedcutter's plea, Mill letter. By rate it is Reedcutter's plea, Mill letter, Heron hunt, Lockkeeper's key. The quest with the biggest number is the only one that fails, because 8 minutes of travel sit inside its 24.

Heron hunt is 7 levels below the player and pays 60%, but its short time keeps it above the line.

With the mount, travel halves: Lockkeeper's key becomes `5,200 / (4 + 16) = 260.0` and passes. Faster travel re-prices the whole board.
</details>

25. *Week 6 · compute.* A quest at the player's level lists 3,600 XP with 10 minutes of travel and 12 of task, against `r₀ = 160`. (a) Does it pass? (b) A tunnel collapse adds 3 minutes. Does it pass now, what is the complication tax, and what listed XP restores it? (c) Does a mount that halves travel rescue it without raising XP?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Yes, 163.6 per minute. (b) No, 144.0. Tax 480, listed XP 4,000. (c) Yes, 180.0.

(a) `3,600 / 22 = 163.6`.

(b) `3,600 / 25 = 144.0`. Each added minute costs `r₀`, so the tax is `3 × 160 = 480`. The quest needs `160 × 25 = 4,000`.

(c) `3,600 / (5 + 12 + 3) = 180.0`. The tunnel still adds 3 minutes, but the mount took away 5.
</details>

26. *Week 6 · compute.* A quest lists 1,230 XP. What does it pay at 6, 9 and 10 levels over, using the lecture's rule of rounding to the nearest 5?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 985, 245 and 125.

The lecture's code computes `(full × pct + 250) // 500 × 5`.

At `Δ = 6` (80%): `1,230 × 0.8 = 984`, which rounds to 985.

At `Δ = 9` (20%): `246`, which rounds to 245.

At `Δ = 10` (10%): `123`, which rounds to 125.
</details>

27. *Week 6 · critique.* Hook: "The lock-keeper lost his post when the sluice failed, and now his daughter has gone missing in the reeds." Objective: find the daughter. Complication: the reed-cutters who took her in are hiding her from a debt collector. Reward: 500 gold from the lock-keeper. Write the promise ledger, name the broken row, and propose a fiction-consistent reward. Which player will the fix not satisfy?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| The hook implies | The reward delivers | Kept? |
|---|---|---|
| The daughter is in danger | She is found (alive, and her reason for hiding shown) | Yes |
| The lock-keeper is out of work and poor | 500 gold from him | Broken |
| Something is wrong in the reeds | The debt collector is dealt with | Yes, if the quest resolves it |

A man who just lost his job cannot plausibly pay 500 gold. Pay in currencies the fiction supports. He can open the lock for free for the rest of the game (access), give a family item with a story, or the reed-cutters can offer a standing welcome (reputation). XP still comes from the game, which players accept as outside the fiction.

The fix does not satisfy a pure rate-maximizer who values only XP and gold per minute. Run the detour test to check the quest still passes for them on XP alone.
</details>

## Week 7: Quest types and redeeming them

Lecture: [w07, quest types](../lectures/w07-quest-types-and-redeeming-them.md). Interactive: [drop-rate tax](../examples/w07-drop-rate-tax.html).

28. *Week 7 · compute.* A collect quest asks for `n = 6` eel skins at `p = 0.4` per kill, with 18 seconds per kill. Give the mean kill count, SD, relative spread, median, P90 and P99, and the mean and P90 times in minutes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mean 15, SD 4.74, relative spread 0.32, median 14, P90 21, P99 29. Mean time 4.5 minutes, P90 time 6.3 minutes.

Mean `n / p = 15`. SD `√(6 × 0.6) / 0.4 = 1.897 / 0.4 = 4.74`. Relative spread `√(0.6 / 6) = 0.32`. The percentiles come from the binomial tail `P(K ≤ k)` with the lecture's `percentile` function.

Times: `15 × 18 = 270` s, 4.5 minutes. `21 × 18 = 378` s, 6.3 minutes.
</details>

29. *Week 7 · compute.* A single-item quest drops at `p = 0.08`. (a) What is the mean kill count? (b) What share of players still lack the item after 30 kills? (c) What is the P90? (d) You add a pity rule: the item is guaranteed on kill `m`. What is the smallest `m` for which at most 10% of players ever reach the guarantee?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12.5. (b) 8.2%. (c) 28. (d) 29.

(a) `1 / 0.08 = 12.5`.

(b) `0.92^30 = 0.082`.

(c) The smallest `k` with `0.92^k ≤ 0.1`: `ln 0.1 / ln 0.92 = 27.6`, so 28.

(d) A player reaches kill `m` without the item only if the first `m − 1` kills all missed, which has chance `0.92^(m − 1)`. That must be at most 0.1, so `m − 1 ≥ 27.6`, `m − 1 = 28` and `m = 29`. Watch the off-by-one. The P90 (28) is where 90% are done. The guarantee must sit one kill later so that only the unlucky 10% ever see it.
</details>

30. *Week 7 · analysis.* Two collect quests both average 24 kills: A asks for 2 items at `p = 1/12`, B for 12 items at `p = 0.5`. Compare their relative spread, P90 and P99. Which draws fewer complaints, and what does B cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** A: relative spread 0.68, P90 46, P99 77. B: 0.20, P90 31, P99 38. B draws fewer complaints.

Relative spread `√((1 − p)/n)`: A `√((11/12)/2) = 0.68`, B `√(0.5/12) = 0.20`.

A's unlucky tenth needs 46 kills, nearly twice the mean. B's needs 31. Players remember the worst case, so B is fairer. The cost of B is twelve items to count, which some players find dull. A fairer counter is not better writing.
</details>

31. *Week 7 · compute.* (a) A zone has 8 collect quests with long tails. For each one, a player has a 10% chance of landing past its P90. What is the chance a player hits at least one such run in the zone? (b) In a group of 3 where a quest item drops for only one member, each player needs 5 items at `p = 0.25`. What is the group's mean kill count, and how does it compare with solo play?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 57%. (b) 60 kills against 20.

(a) `1 − 0.9^8 = 0.570`. Most players will have a bad story to tell.

(b) The group needs `n_total = 3 × 5 = 15` items from one pool, so the mean is `15 / 0.25 = 60` kills. Solo it is `5 / 0.25 = 20`. Kills come faster in a group, but every player waits for the slowest share.
</details>

32. *Week 7 · design.* Rewrite "Bring me 10 reed-cat pelts" as a sequence of Doran and Parberry atomic actions. Redesign it by changing one lever from the lecture's checklist, write the new objective line, and name one cost of the change.

<details>
<summary>Answer and worked solution</summary>

**Answer (model answer; any single lever with a real cost is right):**

Sequence: goto, kill until 10 pelts, goto, give.

Lever, information. The reed-cats have started raiding the village's fish traps. The player follows tracks to find why.

New objective line: "Follow the reed-cat tracks from the fish traps to the den in the north marsh."

New sequence: goto, investigate × 3, kill (the den mother), goto, report.

Cost: a unique den location with scene dressing and a named enemy, and a track trail the level designer must place and test. You cannot build many of these per zone.
</details>

## Week 8: Quest chains and zone storytelling

Lecture: [w08, quest chains and zone storytelling](../lectures/w08-quest-chains-and-zone-storytelling.md). Interactive: [quest chain shapes](../examples/w08-quest-chain-shapes.html).

33. *Week 8 · compute.* A zone has 7 quests. The intro unlocks a, b and c. Quest d needs a. Quest e needs b and c. The finale needs d and e. With `t_task = 3` and `t_travel = 4`, compute `T`, `W`, fixed pairs, `C` and zone time.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `T = 4`, `W = 3`, 14 fixed pairs of 21, `C = 0.67`, zone time 37 minutes.

Layers: {intro}, {a, b, c}, {d, e}, {finale}.

Fixed pairs: the intro is an ancestor of all 6 others (6). a is an ancestor of d and the finale (2). b and c are each ancestors of e and the finale (4). d and e are each ancestors of the finale (2). Total 14 of `7 × 6 / 2 = 21`, `C = 14/21 = 0.67`.

Time `7 × 3 + 4 × 4 = 21 + 16 = 37`.
</details>

34. *Week 8 · analysis.* A zone is two strands of 4 quests, a1 to a4 and b1 to b4. (a) Compute `T`, `W`, `C` and zone time (`t_task = 3`, `t_travel = 4`). (b) Compute the new `T`, `C` and time after adding each arrow on its own: a2 → b3, a1 → b1, a4 → b1. Which arrow buys order control without a trip?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Zone | `T` | `C` | Time |
|---|---|---|---|
| Two strands | 4 | 12/28 = 0.43 | 40 |
| + a2 → b3 | 4 | 16/28 = 0.57 | 40 |
| + a1 → b1 | 5 | 16/28 = 0.57 | 44 |
| + a4 → b1 | 8 | 28/28 = 1.00 | 56 |

Two strands: each has `C(4, 2) = 6` fixed pairs, so 12 of 28. `W = 2`. Time `24 + 16 = 40`.

a2 → b3: b3 was already in layer 3, so no layer is added. a1 and a2 become ancestors of b3 and b4, 4 new pairs. More control for free.

a1 → b1: b1 moves to layer 2 and the b strand ends in layer 5, one extra trip. a1 becomes an ancestor of all four b quests, 4 new pairs.

a4 → b1: the zone becomes one linear chain of 8. Total control, twice the trips.

Where you put an arrow matters more than how many you draw.
</details>

35. *Week 8 · compute.* A flat zone has 45 quests and the quest log holds 20. With `t_task = 3` and `t_travel = 5`, what are the fewest trips and the zone time for a batching player? What would they be with no cap?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3 trips and 150 minutes. With no cap, 1 trip and 140 minutes.

The player can carry at most 20, so `ceil(45 / 20) = 3` trips. Time `45 × 3 + 3 × 5 = 135 + 15 = 150`. With no cap, `135 + 5 = 140`. The cap acts as a prerequisite the designer never drew, and the player chooses which 20 go first.
</details>

36. *Week 8 · analysis.* A spine-and-ribs zone: s1 unlocks r1, r2 and r3; s2 needs all three; s2 unlocks r4 and r5; s3 needs both. (a) Compute `T`, `W`, `C` and zone time (`t_task = 3`, `t_travel = 4`). (b) The designer changes s2 to need only r1 and r2. What happens to `T` and `C`, and what writing problem does it create for r3?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `T = 5`, `W = 3`, `C = 24/28 = 0.86`, 44 minutes. (b) `T` stays 5, `C` falls to `20/28 = 0.71`.

(a) Layers {s1}, {r1, r2, r3}, {s2}, {r4, r5}, {s3}. Fixed pairs: s1 with 7 (7), each of r1 to r3 with s2, r4, r5, s3 (12), s2 with 3 (3), r4 and r5 with s3 (2). Total 24 of 28. Time `8 × 3 + 5 × 4 = 44`.

(b) r3 still sits in layer 2, so the layers do not change. It loses its 4 fixed pairs with s2, r4, r5 and s3. r3 can now be done after the finale, so its text must make sense after the zone's story is resolved, and no spine quest can depend on it.
</details>

## Week 9: Emergent narrative

Lecture: [w09, emergent narrative](../lectures/w09-emergent-narrative.md). Interactive: [rival recurrence](../examples/w09-rival-recurrence.html).

37. *Week 9 · compute.* A cast has `R = 25` characters and the player's killer has weight `w = 4`. What is the chance the next encounter is the rematch, the chance of at least one rematch within 6 encounters, and the mean wait?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 14.3%, 60.3% and 7 encounters.

`P = 4 / (24 + 4) = 4/28 = 0.143`. `P_6 = 1 − (24/28)^6 = 1 − 0.397 = 0.603`. Mean wait `28 / 4 = 7`.
</details>

38. *Week 9 · compute.* You want an 80% chance of a rematch within 6 encounters on a cast of 50. What is the smallest whole weight? Check your answer and the weight below it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `w = 16`.

`P needed = 1 − 0.2^(1/6) = 0.235`. `w needed = 0.235 × 49 / 0.765 = 15.08`, so round up to 16.

Check: `w = 16` gives `P = 16/65` and `P_6 = 81.6%`. `w = 15` gives `P_6 = 79.9%`, just short.
</details>

39. *Week 9 · design.* A zone has 40 bandit lieutenants who can become rivals. The design wants at least a 60% chance of a rematch within 8 encounters, and no more than 90% within 3 (so the rival does not feel stuck to the player). Which whole weights meet both conditions?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Any `w` from 5 to 45.

Lower bound: `P needed = 1 − 0.4^(1/8) = 0.108`, `w ≥ 0.108 × 39 / 0.892 = 4.73`, so `w ≥ 5`. Check: `w = 5` gives 61.9% within 8.

Upper bound: within 3 at most 0.9 needs `P ≤ 1 − 0.1^(1/3) = 0.536`, so `w ≤ 0.536 × 39 / 0.464 = 45.02`, and `w ≤ 45`. Check: `w = 45` gives 89.99% within 3, and `w = 46` gives 90.3%.

The window is wide, so the choice inside it is about taste. Pick a small value such as 5 to 8 and decay it after each player win, as the lecture's frustration warning suggests.
</details>

40. *Week 9 · analysis.* Shadow of Mordor both shrinks the cast and raises the weight. With no weight (`w = 1`), compare the chance of a rematch within 5 encounters for the whole population (`R = 200`) and for a short list of 12 captains. Then find the smallest weight that gives the 12 captains a 60% chance within 5.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.5% against 35.3%. Weight 3.

`R = 200, w = 1`: `1 − (199/200)^5 = 2.5%`. `R = 12, w = 1`: `1 − (11/12)^5 = 35.3%`.

For 60% within 5: `P needed = 1 − 0.4^(1/5) = 0.167`, `w = 0.167 × 11 / 0.833 = 2.2`, so 3. Check: `w = 3` gives 70.1%, `w = 2` gives 56.6%.

Shrinking the cast does most of the work. A modest weight finishes the job. On the full population you would need a very large weight to reach the same chance.
</details>

41. *Week 9 · compute.* RimWorld's Cassandra Classic runs a 4.6-day on phase with 1 or 2 major threats (50-50), then a 6-day off phase. (a) What is her average number of days per major threat, and threats per 60-day year? (b) Randy Random averages about 7.1 days between major threats. Why do players still call them different games?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 7.1 days, about 8.5 threats per year. (b) Same mean, different tail.

(a) The cycle is `4.6 + 6 = 10.6` days with 1.5 threats on average, so `10.6 / 1.5 = 7.07` days per threat and `60 / 10.6 × 1.5 = 8.49` per year.

(b) Cassandra forces at least 1.9 days between threats and a 6-day rest after each on phase. Randy has no spacing rule, multiplies raid strength by 0.5 to 1.5, and can send two strong raids back to back. Colonies die in the worst case, and players tell stories about the worst case. It is week 7's lesson in a different place.
</details>

## Week 10: Lore delivery without walls of text

Lecture: [w10, lore delivery](../lectures/w10-lore-delivery-without-walls-of-text.md). Interactive: [lore chunking](../examples/w10-lore-chunking.html).

42. *Week 10 · compute.* With `s = 0.75`, compute `E(8)`, the completion rate of an 8-sentence text, the ceiling for any length, and the share of players who read sentence 4.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E(8) = 2.70`, completion 10.0%, ceiling 3, sentence 4 read by 31.6%.

`E(8) = 0.75 × (1 − 0.75^8) / 0.25 = 3 × (1 − 0.100) = 2.70`. Completion `0.75^8 = 0.100`. Ceiling `0.75 / 0.25 = 3`. Sentence 4: `0.75^4 = 0.316`.
</details>

43. *Week 10 · compute.* You have 24 sentences of lore and `s = 0.75`. Plan A is one forced wall. Plan B splits it into 8 pieces of 3 sentences, each found with chance 0.5. Compute both and the break-even find chance for plan B.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Wall 3.00, plan B 6.94, break-even `f* = 0.22`.

`E(24) = 3 × (1 − 0.75^24) = 3.00` (0.75^24 is about 0.001).

`E(3) = 0.75 + 0.5625 + 0.4219 = 1.734`. Plan B: `8 × 0.5 × 1.734 = 6.94`.

`f* = 3.00 / (8 × 1.734) = 0.216`. Pieces found more than about one time in five beat the wall.
</details>

44. *Week 10 · compute.* In a playtest, 25% of testers reach the end of a 5-sentence quest description. Estimate `s`, then predict the completion rate of a 10-sentence text.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `s = 0.758`. 6.25%.

`s = 0.25^(1/5) = 0.758`. A 10-sentence text completes at `s^10 = (s^5)^2 = 0.25^2 = 0.0625`.

Doubling the length squares the completion rate under this model. Check the page-to-page ratios in your own data before trusting a constant `s`, as lab 10 asks.
</details>

45. *Week 10 · design.* A quest's backstory is 16 sentences, and `s = 0.8`. The need-to-know fact sits in sentence 6 of the wall. You propose a mixed plan: a 2-sentence forced summary with the need-to-know fact first, plus 14 one-sentence pieces found with chance 0.4. (a) Compute the wall, the mixed plan and their ratio. (b) What share of players read the need-to-know fact before and after? (c) What is the break-even find chance if you scattered all 16 as one-liners with no forced summary?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Wall 3.89, mixed 5.92, ratio 1.52. (b) 26.2% before, 80% after. (c) 0.30.

(a) `E(16) = 4 × (1 − 0.8^16) = 3.89`. Mixed: `E(2) + 14 × 0.4 × 0.8 = 1.44 + 4.48 = 5.92`. Ratio `5.92 / 3.89 = 1.52`.

(b) Sentence 6 of the wall reaches `0.8^6 = 26.2%`. Sentence 1 of the forced summary reaches 80%.

(c) `f* = E(16) / (16 × E(1)) = 3.89 / (16 × 0.8) = 0.30`. At `f = 0.4` the one-liners are above break-even, but only just.
</details>

46. *Week 10 · analysis.* A lore fan has `s = 0.9`. Compute the ceiling, `E(10)` and `E(40)` for this reader. What does the result say about where a codex belongs, and why is it the wrong place for the need-to-know tier?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Ceiling 9, `E(10) = 5.86`, `E(40) = 8.87`.

`0.9 / 0.1 = 9`. `E(10) = 9 × (1 − 0.9^10) = 5.86`. `E(40) = 9 × (1 − 0.9^40) = 8.87`.

For a fan, quadrupling the text still adds 3 sentences read, so long reference text is worth something to them. That is the codex's audience. A player in a hurry at `s = 0.5` has a ceiling of 1 sentence, so anything the player must know to act has to sit in the first sentence of a forced channel.
</details>

## Week 11: Writing for localization

Lecture: [w11, writing for localization](../lectures/w11-writing-for-localization.md). Interactive: [plural rules](../examples/w11-plural-rules.html).

47. *Week 11 · compute.* Using the lecture's CLDR 48 rules for whole numbers, give the plural category of 0, 14, 22, 103, 111 and 2,000,000 in English, French, Russian, Polish, Arabic and Japanese.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| n | en | fr | ru | pl | ar | ja |
|---|---|---|---|---|---|---|
| 0 | other | one | many | many | zero | other |
| 14 | other | other | many | many | many | other |
| 22 | other | other | few | few | many | other |
| 103 | other | other | few | few | few | other |
| 111 | other | other | many | many | many | other |
| 2,000,000 | other | many | many | many | other | other |

Notes on the harder cells. Russian 14: last digit 4 but last two digits 14, excluded, so `many`. Russian 103: last digit 3, last two 03, so `few`. Arabic 103: `103 mod 100 = 3`, in 3 to 10, so `few`. Arabic 2,000,000: `mod 100 = 0`, so `other`. French 2,000,000 is a nonzero multiple of a million, so `many`.
</details>

48. *Week 11 · compute.* A quest tracker shows counts from 0 to 30, and the engine only has a singular slot (used for 1) and a plural slot. (a) For Russian, Polish and Arabic, how many forms does the language need over 0 to 30? (b) With the best single form in the plural slot, how many counts come out wrong in each, and which?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Russian 3, Polish 3, Arabic 5. (b) Russian 7, Polish 6, Arabic 10.

(a) Russian uses `one`, `few` and `many` in this range. Polish uses the same three. Arabic reaches `zero`, `one`, `two`, `few` and `many`, and `other` needs 100 or more.

(b) Russian, best slot `many`: wrong at 2, 3, 4, 21, 22, 23, 24. The `few` numbers are wrong, and 21 is `one` but the singular slot catches only 1.

Polish, best slot `many`: wrong at 2, 3, 4, 22, 23, 24. Polish 21 is `many`, so it prints right.

Arabic, best slot `many`: wrong at 0, 2 and 3 to 10.

A tester who checks 1, 5 and 10 in Russian sees no bug at all.
</details>

49. *Week 11 · compute.* Using the lecture's width budget, reserve space for "Hand in" (7 characters), "Accept quest" (12), "Return to the reeve" (19) and "The ferry leaves at dusk. Be on it or wait a week." (50). A button is 24 characters wide. Which labels fit?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Budgets 21, 24, 38 and 80. "Hand in" and "Accept quest" fit, "Return to the reeve" does not.

Up to 10 characters take ×3: `7 × 3 = 21`. 11 to 20 take ×2: `12 × 2 = 24` and `19 × 2 = 38`. 31 to 50 take ×1.6: `50 × 1.6 = 80`.

"Accept quest" fits exactly, with no margin. "Return to the reeve" needs a wider button or a shorter label, and the report should say which meaning a shorter label loses.
</details>

50. *Week 11 · critique.* A programmer wrote `"You gave " + n + " eel" + (n == 1 ? "" : "s") + " to " + npc + "."`. List what breaks in other languages and rewrite it as a string a translator can localize.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It bakes English plural grammar into code and fixes the word order.

Problems: English has two forms, but Russian and Polish need three for whole numbers and Arabic up to six, so the ternary prints wrong forms. The fragments cannot be reordered, so a language that puts the verb last cannot be served. The NPC name may need a case ending the code cannot add.

Rewrite, ICU style, with whole sentences in each branch:

`GAVE_EELS = "{n, plural, one {You gave # eel to {npc}.} other {You gave # eels to {npc}.}}"`

with a note such as "System message after handing eels to a quest giver. npc is a character name." Translators add `few`, `many` and the other categories their language needs and move `{npc}` where it belongs.
</details>

## Week 12: Tools, ink and Yarn Spinner

Lecture: [w12, ink and Yarn Spinner](../lectures/w12-tools-ink-and-yarn-spinner.md). Interactive: [bark repetition](../examples/w12-bark-repetition.html).

51. *Week 12 · compute.* (a) A bark has 6 variants picked at random. What is the chance of at least one repeat within the first 4 plays? (b) Under a shuffle bag? (c) With 12 random variants, what is the chance that the first 3 plays are all different?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 72.2%. (b) 0. (c) 76.4%.

(a) No repeat: `1 × 5/6 × 4/6 × 3/6 = 360 / 1,296 = 0.278`, so a repeat has chance 0.722.

(b) A bag of 6 never repeats within its first 6 plays.

(c) `1 × 11/12 × 10/12 = 0.764`.
</details>

52. *Week 12 · compute.* A companion comment fires 120 times in a play-through and has 8 variants. How many back-to-back repeats does a player hear on average under random selection, a shuffle bag, a cycle and a stopping sequence?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Random 14.9, bag 1.75, cycle 0, stopping 112.

Random: `(K − 1)/n = 119/8 = 14.9`. Bag: `floor(119/8) = 14` boundaries, each with chance 1/8, so `14/8 = 1.75`. Cycle: 0 for `n ≥ 2`. Stopping: after 8 plays it sticks on the last line, so `120 − 8 = 112` back-to-back repeats. Stopping is for escalation, not ambient barks.
</details>

53. *Week 12 · design.* A gate bark fires 200 times per play-through. The target is at most 2 expected back-to-back repeats. How many variants does each rule need: shuffle bag, random, no-repeat bag?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Bag 10, random 100, no-repeat bag 2.

Bag: `floor(199/n)/n ≤ 2`. `n = 9` gives `22/9 = 2.44`, too many. `n = 10` gives `19/10 = 1.9`.

Random: `199/n ≤ 2` gives `n ≥ 99.5`, so 100.

No-repeat bag: 0 back-to-back repeats with any `n ≥ 2`, so the target is met with 2. Pick the number of variants for variety, not for the repetition target.
</details>

54. *Week 12 · compute.* How many variants does random selection need for a 90% chance that the first 3 plays are all different? The first 4? How many does a shuffle bag need for each?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Random 30 and 59. Bag 3 and 4.

For 3 plays, the smallest `n` with `(n − 1)(n − 2)/n² ≥ 0.9` is 30. For 4 plays the lecture's `lines_needed(4, 0.9)` gives 59. A bag of `k` lines guarantees `k` different plays, so it needs 3 and 4. The rule is worth 27 or 55 extra lines of writing.
</details>

55. *Week 12 · analysis.* In this ink knot, the player visits the smith four times. What text does each visit print? Which of the lecture's four rules does each line use, and how would you write the first line in Yarn Spinner?

```
=== smith ===
{The smith nods.|The smith grunts.|The smith waves you off.}
{&Hot today.|Iron's cheap.}
+ [Leave] -> END
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Visit | First line | Second line |
|---|---|---|
| 1 | The smith nods. | Hot today. |
| 2 | The smith grunts. | Iron's cheap. |
| 3 | The smith waves you off. | Hot today. |
| 4 | The smith waves you off. | Iron's cheap. |

`{a|b|c}` is a stopping sequence: it plays in order and sticks on the last entry. `{&a|b}` is a cycle. The stopping line escalates, which is its job. The cycle never repeats back to back, but a player learns its order by the third visit.

Yarn Spinner writes escalation with `once` blocks and an `else` for the line that sticks (the lecture's section 2 design judgment), for example two `<<once>>` lines followed by a default line.
</details>

## Week 13: Shared vs personal story

Lecture: [w13, shared vs personal story](../lectures/w13-shared-vs-personal-story.md). Interactive: [phase split](../examples/w13-phase-split.html).

56. *Week 13 · compute.* A zone has `N = 61` players split across phases with shares 0.50, 0.25, 0.15 and 0.10. Compute `V`, the expected number of others a player sees, `n_eff` and what a player in the smallest phase sees.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `V = 0.345`, 20.7 others, `n_eff = 2.90`, smallest phase sees 6.0.

`V = 0.25 + 0.0625 + 0.0225 + 0.01 = 0.345`. Seen `60 × 0.345 = 20.7`. `n_eff = 1 / 0.345 = 2.90`. Smallest `0.10 × 60 = 6.0`.
</details>

57. *Week 13 · design.* A three-step chain in a zone of 41 players: step 1 changes nothing, step 2 sets the phase `burned`, step 3 is a 50/50 choice between two visible outcomes. The funnel is `[0.4, 0.3, 0.2, 0.1]` (position `k` means steps 1 to `k` done). (a) Compute the phase shares, `V`, expected visible others and the smallest phase. (b) The producer wants at least 20 visible others and at least 3 in the smallest phase. Does the design pass? (c) Keep the choice but merge its two outcomes into one visible phase with the difference stored in a private flag. Recompute.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) base 0.7, burned 0.2, burned+x 0.05, burned+y 0.05. `V = 0.535`, 21.4 visible, smallest 2.0. (b) It fails the smallest-phase target. (c) Shares 0.7, 0.2, 0.1, `V = 0.54`, 21.6 visible, smallest 4.0. It passes.

(a) Positions 0 and 1 are both in `base`: `0.4 + 0.3 = 0.7`. Position 2 has done step 2: `burned` 0.2. Position 3 has done the choice, split 50/50: 0.05 each. `V = 0.49 + 0.04 + 0.0025 + 0.0025 = 0.535`. Visible `40 × 0.535 = 21.4`. Smallest `0.05 × 40 = 2.0`.

(b) 21.4 passes the first target. The finishing players see 2 others, below 3.

(c) One finished phase of 0.1: `V = 0.49 + 0.04 + 0.01 = 0.54`, visible 21.6, smallest `0.1 × 40 = 4.0`. The average barely moves. The ending stops being lonely. The choice lives on in dialogue that reads the private flag, which is week 4's tool doing week 13's job.
</details>

58. *Week 13 · analysis.* (a) WoW Classic launched with layers, copies of the outdoor world. With 5 equally full layers, what is `V`? (b) Place each invented consequence in the lecture's scope and duration table: a sea-serpent attack on the harbour every 90 minutes; a companion who leaves you forever after you betray her; a bridge rebuilt in a patch for every player on the server; a private instance where you defend a lighthouse for one night.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `V = 0.2`. (b) Shared temporary; personal permanent; shared permanent; personal temporary.

(a) `V = 5 × (1/5)² = 1/5 = 0.2`. A player sees a fifth of the realm. Layering buys server capacity with the same currency phasing uses.

(b) The serpent attack is public drama that resets. The companion's departure defines your character and costs nothing in `V` if it lives in dialogue. The rebuilt bridge is shared history that late arrivals see without seeing it happen. The lighthouse night is action that would be absurd if twenty others did it at once.
</details>

## Week 14: Narrative testing

Lecture: [w14, narrative testing](../lectures/w14-narrative-testing.md). Interactive: [playthrough coverage](../examples/w14-playthrough-coverage.html).

59. *Week 14 · compute.* A path passes four choice points where a uniform bot has 3, 2, 4 and 2 options. What is `q`, and how many random runs give 95% confidence of seeing the path? Compare with the `3/q` shortcut.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `q = 1/48`, 143 runs. The shortcut says 144.

`q = 1/3 × 1/2 × 1/4 × 1/2 = 1/48`. Runs `ceil(ln 0.05 / ln(47/48)) = ceil(2.996 / 0.02105) = ceil(142.3) = 143`.
</details>

60. *Week 14 · compute.* A story has 32 equally likely endings. (a) About how many random runs does it take on average to see all of them? (b) What share of endings do 32 random runs see on average? (c) How does enumeration compare?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 130. (b) 63.8%. (c) Enumeration needs exactly 32.

(a) Coupon collector: `32 × (1 + 1/2 + ... + 1/32) = 32 × 4.06 = 129.9`.

(b) `1 − (1 − 1/32)^32 = 0.638`, close to the limit `1 − 1/e`.

(c) One directed run per ending, 32 in total, with no luck involved. Random play costs about 4 times as much to see everything.
</details>

61. *Week 14 · compute.* Predict the output of this state search on an invented trek scene, then run it. Name each bug in the lecture's families. How many uniform random runs would a tester need for 95% confidence of hitting each dead end?

```python
from collections import deque
from fractions import Fraction

STORY = {
    "camp":  [("share food", "trail", set(), {"fed"}),
              ("keep food", "trail", set(), set())],
    "trail": [("follow the guide", "ford", {"fed"}, set()),
              ("take the ridge", "ridge", set(), {"tired"})],
    "ridge": [("rest", "ford", set(), set()),
              ("push on", "cliff", {"fed"}, set())],
    "ford":  [("wade across", "home", {"fed", "tired"}, set())],
    "cliff": [("climb down", "home", set(), set())],
    "home":  [],
}
ENDINGS = {"home"}

def explore(story, start="camp"):
    first = (start, frozenset())
    seen, queue = {first}, deque([first])
    while queue:
        node, flags = queue.popleft()
        for _, target, needs, sets in story[node]:
            if needs <= flags:
                nxt = (target, flags | sets)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return seen

states = explore(STORY)
print("reachable states:", len(states))
for node, flags in sorted(states, key=lambda s: (s[0], sorted(s[1]))):
    open_ = [c for c in STORY[node] if c[2] <= flags]
    if node not in ENDINGS and not open_:
        print("dead end:", node, sorted(flags))

def outcomes(node, flags):
    if node in ENDINGS:
        return {node: Fraction(1)}
    open_ = [c for c in STORY[node] if c[2] <= flags]
    if not open_:
        return {"DEAD_END": Fraction(1)}
    total = {}
    for _, target, _, sets in open_:
        for k, v in outcomes(target, flags | sets).items():
            total[k] = total.get(k, 0) + v / len(open_)
    return total

print(outcomes("camp", frozenset()))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
reachable states: 10
dead end: ford ['fed']
dead end: ford ['tired']
{'DEAD_END': Fraction(3, 4), 'home': Fraction(1, 4)}
```

The 10 states: camp {}, trail {} and {fed}, ridge {tired} and {fed, tired}, ford {fed}, {tired} and {fed, tired}, cliff {fed, tired}, home {fed, tired}.

Both findings are dead ends. The writer made "wade across" need `fed` and `tired`, probably meaning either. A player who follows the guide is fed but not tired. A player who kept the food is tired but not fed.

Probabilities for a uniform bot: keeping food (1/2) forces the ridge, then only "rest" is open, so ford {tired} has `q = 1/2`. Sharing food (1/2), then following the guide (1/2), gives ford {fed} with `q = 1/4`. Runs for 95%: `ceil(ln 0.05 / ln 0.5) = 5` and `ceil(ln 0.05 / ln 0.75) = 11`. Here random testing would find both quickly. The state search finds them in one pass and names the exact flags.
</details>

62. *Week 14 · compute.* Real players pick a particular option 20% of the time, and a path needs it at four separate choice points (all else certain). (a) What is `q`? (b) Among 50,000 completed playthroughs, how many players see the path? (c) How many uniform-bot runs would give 95% confidence if the bot also picked that option 20% of the time?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.0016. (b) 80. (c) 1,871.

(a) `0.2^4 = 0.0016`.

(b) `50,000 × 0.0016 = 80`.

(c) `ceil(ln 0.05 / ln(1 − 0.0016)) = 1,871`. Human testers who play like players would need the same number of runs, which no QA team has. Coverage-seeking bots or enumeration are the right tools.
</details>

63. *Week 14 · critique.* After a comprehension playtest of an invented quest about a lock-keeper, 3 of 5 testers missed the beat "the lock-keeper sabotaged the sluice himself". The writer says "40% understood it, which is fine for a twist." The lead asked each tester "Did you notice the wrench in his cottage?" Critique both.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Five testers can find a failing beat but cannot measure a rate. The question was leading.

"2 of 5 understood" is compatible with a true rate anywhere from roughly 5% to 85%, so "40%" claims a precision five testers cannot give. What five testers do show is that a majority missed the beat, which the lecture treats as a writing problem regardless of the others.

"Did you notice the wrench?" teaches the answer. Ask open questions after play, such as "Why did the sluice fail?", and score each beat as understood, partly or missed.
</details>

## Across weeks

64. *Weeks 3 and 14 · analysis.* A branch-and-bottleneck story has `b = 3`, `d = 5`, `k = 1`. (a) How many nodes and paths does it have? (b) How many uniform random runs give 95% confidence of seeing one specific path? (c) If every choice sets a permanent flag recording which option was picked, a state search visits 484 states. Explain where that number comes from, and what it says about week 14's advice "design so that you can".

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 20 nodes, 243 paths. (b) 727. (c) `1 + 2 × (3 + 9 + 27 + 81) + 243 = 484`.

(a) From week 3, `N = d(b + 1) = 20` and paths `3^5 = 243`.

(b) `q = 1/243`, `ceil(ln 0.05 / ln(242/243)) = 727`.

(c) With permanent flags, each node is visited once for every history that can reach it. After `j` choices there are `3^j` histories. The option nodes at level `j` hold `3^j` states in total, and so does the bottleneck after them, for `j = 1` to 4. The five-choice endings add `3^5 = 243`. Folding back shrank the content to 20 nodes, but flags that remember everything bring the testing back to 484 states. Store only the flags later scenes actually read, and the search stays small.
</details>

65. *Weeks 6 and 7 · design.* A collect quest asks for 6 items at `p = 0.3` (mean 20 kills, P90 29) at 15 seconds per kill, plus 4 minutes of travel. It lists 2,000 XP with no decay, and `r₀ = 200`. (a) Does it pass the detour test at the mean time? (b) At the P90 time? (c) What listed XP passes for the unlucky tenth?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Yes, 222.2. (b) No, 177.8. (c) 2,250.

(a) Mean time `4 + 20 × 15 / 60 = 9` minutes. `2,000 / 9 = 222.2`.

(b) P90 time `4 + 29 × 15 / 60 = 11.25` minutes. `2,000 / 11.25 = 177.8`.

(c) `200 × 11.25 = 2,250`. Pricing from the mean underpays one player in ten by the gap between mean and P90, which week 7 calls the drop-rate tax. Either pay from the P90 or narrow the spread with a larger `n` and higher `p`.
</details>
