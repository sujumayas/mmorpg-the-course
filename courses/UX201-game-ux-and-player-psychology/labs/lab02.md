# UX201 · Lab 02: Keystroke-level audit of a shipped game

Assigned in week 2 ([lecture](../lectures/w02-cognitive-load-and-ui.md)). Due at the start of week 3. Pairs allowed; each pair submits one report.

## Objective

Model one frequent interface task in a shipped game with the keystroke-level model (KLM), check the model's prediction against measured times from real players, and propose a redesign whose saving you can predict. The point is to count thinking (`M`) and scanning (`S`) along with the clicks, and to see how far a 1980s office model transfers to a game.

## Starter materials

Everything you need is in this file.

**1. Operator table (use these values unless you measure better ones).**

| Operator | Meaning | Time |
|---|---|---|
| `K` | Key or button press | 0.28 s (average); 0.12 s for players you judge fast |
| `P` | Point with the mouse | 1.1 s |
| `B` | Mouse button press or release (`BB` = click) | 0.1 s |
| `H` | Hand moves between keyboard and mouse | 0.4 s |
| `M` | Decide or recall the next step | 1.35 s |
| `S(N)` | Scan an unordered list of `N` text entries for a known item | `e × (N + 1) / 2`, with `e = 0.15 s` |
| `W(t)` | Wait for the game (animation, loading, menu transition) | Measure `t` with a stopwatch or a frame counter |

`W` is the KLM system-response operator `R`, renamed so it doesn't clash with the challenge ratio from week 3.

**2. Placing `M`s (simplified from Card, Moran and Newell).** Put an `M` before every step where the player must decide or recall something. Delete it when the step is fully anticipated as part of a sequence the player already knows by heart. For a *novice* model, keep an `M` at every decision. For an *expert* model, keep one `M` per chunk.

**3. Task candidates** (pick one, or propose another to your instructor by the end of week 2's lab session).

- Sell all junk items to a vendor in an RPG or MMO.
- Equip a specific item from the inventory in an action RPG.
- Craft a known item in a survival game.
- Find and track a specific quest in a quest log.
- Change one setting (for example subtitles on) from the main menu of a console game.

**4. Timing sheet (one per participant).**

| Participant | Experience with this game (none / some / a lot) | Trial | Start cue | Time (s) | Errors or detours (describe) |
|---|---|---|---|---|---|
| | | 1 | | | |

Start the clock when you say "go" and the game is at the agreed starting state. Stop it when the task's end state is visible.

**5. Prediction sheet.**

| Model | Operator sequence | Predicted time (s) |
|---|---|---|
| Expert, current design | | |
| Novice, current design | | |
| Expert, your redesign | | |
| Novice, your redesign | | |

## Steps

1. **Choose the task and the starting state.** Write down exactly where the player begins (for example, "standing at the vendor, vendor window open, 14 junk items in bags") so every trial starts the same.
2. **Walk it yourself three times** and write the step list.
3. **Write two operator sequences**, expert and novice, using the `M` rule. Measure any `W` waits with a stopwatch or a screen recording (count frames at 30 or 60 fps).
4. **Predict** both times with the operator table.
5. **Time five participants,** at least two who have never played the game and at least two who have played it a lot. Two trials each. Don't coach. If someone is stuck for more than 60 seconds, give the smallest hint and log it as an error.
6. **Compare** predicted and measured times for each group. Report the difference in seconds and as a percentage. Where the model is wrong by more than 30%, look at the detours column and name the cause (an error, an `M` you missed, a slower `K`, a longer scan).
7. **Redesign** the interface on paper to remove at least one `M` or cut one `S`. Write its operator sequences and predict the new times. Classify what you removed as extraneous or intrinsic load, with one sentence of justification.

## Deliverable

A PDF of at most two pages of memo plus appendices.

- The task, the starting state and the two operator sequences.
- A table of predicted against measured times, novice and expert, with the percentage error.
- One paragraph explaining the largest gap between model and measurement.
- The redesign as a sketch, with operator sequences, predicted saving, and the load classification.
- Appendices: all timing sheets.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Operator sequences | Complete, `M` placement justified for novice and expert, `S` and `W` included where they occur | Mostly complete, one or two unjustified `M`s | Clicks only, or missing a model | 25% |
| Measurement | Five participants across experience levels, fixed start state, errors logged | Four participants or loosely controlled start | Fewer than four or no timing sheets | 20% |
| Model vs data | Percentage errors computed, largest gap explained with a specific cause | Comparison made, explanation generic | No comparison | 25% |
| Redesign | Removes a named `M` or `S`, predicted saving correct, load type argued well | Redesign plausible, weak prediction | Vague or no prediction | 20% |
| Writing | Numbers first, plain, within length | Readable, some padding | Hard to follow | 10% |
