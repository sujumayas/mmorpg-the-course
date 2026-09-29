# CS202 · Week 09 — Server reconciliation

**Why this matters:** Prediction makes your own character respond at once, but every 50 ms a snapshot arrives that describes you as you were a round trip ago. Handle it badly and your character jerks backward several times a second. Handle it well and a player at 150 ms of latency never sees a correction unless the server really disagreed. The technique is a short loop over a list, and getting it exactly right is the difference between netcode that feels solid and netcode that feels drunk.

**You will be able to:**
- Implement server reconciliation, which accepts the server's state, drops acknowledged inputs and replays the rest.
- Compute how many inputs are pending at a given round trip and what replaying them costs per second.
- Compute the size of a correction after a server-side surprise, and design how it is shown (snap, or blend over a smoothing time).
- Recognize reconciliation in engines and in rollback netcode, and explain what each chooses to rewind.

**Before class:** Gabriel Gambetta, *Fast-Paced Multiplayer*, part II, the section on server reconciliation (you read the first half last week). Valve Developer Community, "Source Multiplayer Networking", the section "Input prediction", the paragraph on correcting errors. GGPO SDK documentation, "How Does It Work?" (GitHub `pond3r/ggpo`, `doc/README.md`), the rollback section.

**Prerequisites from earlier courses:** [CS102 week 12, the command pattern: input, replay, undo](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (replaying a recorded input list through a deterministic `step` is the core of this week). [CS102 week 6, queues](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (the pending-input list is a queue, removed from the front). [CS202 week 8](w08-client-side-prediction.md) (prediction, the shared `step`, the naive snap and the error model). [CS202 week 7](w07-snapshots-and-delta-compression.md) (acks, and why a snapshot is always a round trip old).

**Interactive:** [examples/w09-reconcile-replay.html](../examples/w09-reconcile-replay.html), a step-through of the reconciliation loop on the lab's simulator. Keep it open during section 2. The course's full lag lab, with all three switches, comes in week 10.

---

## 1. A snapshot is a message from the past

Last week's naive client did the obvious thing with a snapshot. It set its position to the server's. At a 150 ms round trip that moved the character back about a meter, because the snapshot described the player after an input the client had sent 10 inputs earlier.

The mistake is comparing two different moments. The server's `x = 4.7` is the right answer to "where is the player after input 47?". The client's predicted `x = 5.6` is its answer to "where is the player after input 56?". Both can be right at once.

So the snapshot must say *which* input it describes. Every input carries a sequence number (week 8), and the server puts the number of the last input it ran into each snapshot. Call it the **ack** (short for acknowledged), as in week 7. With it, the client can line up the two timelines exactly.

- Inputs up to the ack are **acknowledged**. The server has run them, and the snapshot already contains their effect.
- Inputs after the ack are **pending**. The client has predicted them, the server has not run them yet (or has, but the news has not arrived).

## 2. Worked example: reconciling at 150 ms

### The hook

Source games have a console setting, `cl_showerror 1`, that reports every prediction error. Play at a 150 ms round trip and walk in a straight line. Every snapshot you receive describes you as you were more than 150 ms ago, about a meter back at running speed. If the client compared that with where it is now, every snapshot would count as an error. It does not, and Valve's source code shows why. When a snapshot arrives, the client does not compare the server's position with where it is now. It looks up the position it *predicted* for the last command the server acknowledged, and compares those two. Same command, same moment, same answer. This section builds that comparison and the replay that follows it.

### The model

The client keeps a queue of pending inputs, each with its sequence number. When a snapshot arrives with server state `S` and ack `a`:

```
1. drop every pending input with seq ≤ a            (the server has run them)
2. state = S                                         (accept the authoritative result)
3. for each remaining input (seq > a), in order:
       state = step(state, seq, move)                (replay: re-predict from the truth)
4. correction = state − predicted state before the snapshot
```

If the client knew everything the server knew, step 3 recomputes exactly the prediction it already had, and the correction is zero. If the server knew something the client did not (a snare, a collision, a dropped input), step 3 recomputes the prediction *from the corrected starting point*, and the correction is exactly the effect of what the client did not know.

Two quantities size the work.

```
pending inputs    n ≈ (RTT + w_tick + w_snap) / T_tick
replay work       = snapshot rate × n × cost of one step        per second
```

The pending count is last week's prediction horizon counted in inputs. At 60 Hz inputs and 20 Hz snapshots it is about `(150 + 8.3 + 25) / 16.7 ≈ 11` at a 150 ms round trip.

### Numbers you can check

The lab's simulator, `labs/lab09-starter/netsim.py`, walks a player right at 6 m/s (0.1 m per tick) for 2 seconds. At 1.0 s of server time, an enemy's snare lands, and the next 60 inputs the server runs move at half speed. The client does not know until a snapshot tells it. Here are five consecutive snapshots at a 150 ms round trip, taken straight from the run.

| Arrives when the client has predicted up to input | Server `x` | Ack `a` | Predicted `x` before | Replayed inputs | `x` after replay | Correction | Naive snap would jump |
|---|---|---|---|---|---|---|---|
| 56 | 4.70 | 47 | 5.60 | 48-56 (9 × 0.1) | 5.60 | 0.00 | −0.90 |
| 59 | 5.00 | 50 | 5.90 | 51-59 (9 × 0.1) | 5.90 | 0.00 | −0.90 |
| 62 | 5.30 | 53 | 6.20 | 54-62 (9 × 0.1) | 6.20 | 0.00 | −0.90 |
| 65 | 5.55 | 56 | 6.50 | 57-65 (9 × 0.05) | 6.00 | **−0.50** | −0.95 |
| 68 | 5.70 | 59 | 6.15 | 60-68 (9 × 0.05) | 6.15 | 0.00 | −0.45 |

Check the fourth row by hand. The snapshot says the snare started at input 56 and the server ran input 56 at half speed, reaching `5.5 + 0.05 = 5.55`. The client replays inputs 57 to 65, and it now knows they are snared too, so each moves 0.05: `5.55 + 9 × 0.05 = 6.00`. It had predicted 6.50 at full speed. The correction is −0.50 m, one time, and the fifth row shows the client back in agreement with the server.

That −0.50 m is exactly last week's error model: `Δv × n × T_tick = 3 m/s × 10 inputs × 1/60 s`, where the 10 inputs are 56 to 65, all predicted at full speed and all actually snared.

Now sweep the round trip. Pending counts come from the simulator while the player walks.

| Round trip | Pending inputs (simulated) | Model `n` | Correction after the snare | Replay steps per second at 20 Hz |
|---|---|---|---|---|
| 50 ms | 4-6 | 5.0 | 0.20 m | about 100 |
| 100 ms | 6-10 | 8.0 | 0.35 m | about 160 |
| 150 ms | 10-12 | 11.0 | 0.50 m | about 220 |
| 250 ms | 16-18 | 17.0 | 0.80 m | about 340 |

Replay cost for this game is trivial. Moving one point costs well under a microsecond, so 340 steps a second is nothing. It stops being trivial when `step` is a physics engine with vehicles, a ragdoll and 20 colliding objects. Then every snapshot re-runs 17 physics ticks, and the budget matters (design judgment below).

### The code

Here is the reconciliation method, without smoothing. Lab 09 asks you to write it and then add smoothing. `on_input` is last week's prediction.

```python
def on_snapshot(self, snap):
    before = self.state["x"]
    server = {k: snap[k] for k in ("x", "snare_from", "snare_to")}
    self.pending = [(s, m) for s, m in self.pending if s > snap["ack"]]   # 1. drop
    state = server                                                        # 2. accept
    for s, m in self.pending:                                             # 3. replay
        state = step(state, s, m)
    self.state = state
    return self.state["x"] - before                                       # 4. correction
```

Run the three clients side by side.

```
$ python netsim.py --mode naive
  biggest correction 0.500 m at 83.3 ms; ... jumps over 1 cm: 10
$ python netsim.py --mode reconcile
  biggest correction 0.500 m at 1083.3 ms; ... jumps over 1 cm: 1
$ python netsim.py --mode reconcile --no-snare
  biggest correction 0.000 m at 3000.0 ms; ... jumps over 1 cm: 0
```

The naive client jumps 10 times in 3 seconds. The reconciling client jumps once, when the snare lands, and never without it.

### Showing the correction: snap or smooth

A correction of 0.5 m applied in one frame is a visible teleport. The usual fix is to correct the *state* at once, because the next prediction must start from the truth, and to correct the *drawing* over a short time. The client keeps a display offset equal to minus the correction and shrinks it to zero over a **smoothing time**.

```
drawn position = predicted position + offset × (1 − t / smooth_time),    for 0 ≤ t < smooth_time
```

Source does exactly this. The player's view offset after a prediction error fades out linearly over `cl_smoothtime`, 0.1 seconds by default in the Source SDK, and `cl_smooth 0` turns it off.

With the snare at 150 ms, frame by frame (drawn `x` in meters, 60 frames per second):

| Frame time | Predicted `x` | Drawn, snap | Drawn, smooth over 0.1 s |
|---|---|---|---|
| 1066.7 ms | 6.50 | 6.50 | 6.50 |
| 1083.3 ms (snapshot) | 6.05 | 6.05 | 6.55 |
| 1100.0 ms | 6.10 | 6.10 | 6.517 |
| 1116.7 ms | 6.15 | 6.15 | 6.483 |
| 1133.3 ms | 6.20 | 6.20 | 6.45 |
| 1150.0 ms | 6.25 | 6.25 | 6.417 |
| 1166.7 ms | 6.30 | 6.30 | 6.383 |
| 1183.3 ms | 6.35 | 6.35 | 6.35 |

Snapping moves the character back 0.45 m in one frame (0.5 m of correction minus the 0.05 m the snared step still gains). Smoothing spreads the 0.5 m over six frames, so the drawn character drifts back about 3.4 cm per frame. A player notices the snap. Most players read the smoothed drift as "the snare slowed me", which is what happened.

### Move it yourself

Open `examples/w09-reconcile-replay.html`. It replays the lab's 150 ms run one snapshot at a time. The top strip is the client's input queue, one cell per input, with the step size the client now believes each one moves. The ruler below it shows the server's `x`, the prediction before the snapshot, and a marker that walks forward cell by cell during the replay. The four lines of the model are listed beside it, and the current line lights up.

1. Step to the snapshot with ack 47. Watch inputs up to 47 drop out, the marker start at 4.70 and walk nine cells of 0.1 m. It lands on the dashed ghost of the old prediction. The correction reads 0.00.
2. Step to ack 56. The snare cells turn orange, the marker walks nine cells of 0.05 m and stops 0.50 m short of the ghost. That gap is the correction.
3. Tick "skip the replay". Every snapshot now shows the naive jump from the table's last column, about 0.9 m back, snare or no snare.
4. Set the round trip to 50 ms, then 250 ms. The queue shrinks to 3 cells and grows to 15, and the snare correction goes from 0.20 m to 0.80 m.
5. Tick "lose the snapshot with ack 56". The news arrives one snapshot later, and the correction grows to 0.65 m, as in section 3.

The full lag lab, where you drive the character yourself with all three techniques switched on and off, is week 10's interactive.

### Same idea elsewhere

**Gambetta's two squares (Fast-Paced Multiplayer, part II).** Gambetta's example uses a 250 ms lag and a character that moves one square per keypress. The player presses right twice and the client predicts `x = 12`. The server's first answer says `x = 11`, after request 1 only, and a naive client jumps back a square before jumping forward again. With a sequence number on each request and "last processed request = #1" in the reply, the client keeps request 2, reapplies it to 11, and gets 12. It is our table's third row with one-square steps.

**Source engine (Valve, Source SDK 2013).** Each user command carries a `command_number`. The client stores its predicted result for each command, and when a snapshot arrives it checks the prediction for command `commands_acknowledged − 1` against the server's values. That is step 4 of our model done per command, which is why straight-line walking shows no errors in the hook. Errors are then blended out over `cl_smoothtime`.

**Unreal Engine character movement (Epic documentation, Unreal Engine 5.8).** When the server finds a discrepancy, it sends a correction call such as `ClientAdjustPosition`. On its next tick the client takes the server's position and re-runs the moves still in its `SavedMoves` queue to get a new final position, then records the acknowledged move as `LastAckedMove`. Our `pending` list, our step 2 and our step 3, under different names.

**GGPO rollback (fighting games, 2009 onward).** GGPO reconciles the whole game, not one character. When a remote input arrives and differs from the one it guessed, it restores the saved game state from the frame before the wrong guess and re-runs every frame since with the corrected inputs, as fast as possible and without drawing them. Then it carries on from the frame it was on. Our model with `state` = the entire match and `pending` = the frames since the wrong input.

Four systems, one loop. Rewind to the last state everyone agrees on, reapply the inputs that came after it, and only then decide what to draw.

### Design judgment

- **Reconcile against the ack, never against the clock.** Matching by timestamp breaks the moment the client's frame rate stutters or the server holds an input for a tick. Sequence numbers make the match exact.
- **Correct the state at once, correct the picture slowly.** Smoothing a 0.5 m error over 0.1 s hides it. Smoothing a 5 m error (you were actually knocked off a ledge) lies to the player about where they are. Most games smooth below a threshold and snap above it. Pick the threshold from your error model, for example two times the largest `Δv × horizon` your game's abilities can produce.
- **Budget the replay.** Pending inputs grow with the round trip, and each one re-runs `step`. For heavy physics, cap the replay (above a limit, snap without replaying) or replay only the local player's body and leave the world alone.
- **Decide what you rewind.** Reconciling only the local player is cheap, and wrong when your movement depends on objects you pushed. Rewinding the whole world, as rollback does, is correct and expensive, and it requires a fully deterministic simulation (MA201 week 14, [determinism and floating point](../../MA201-linear-algebra-and-physics-for-games/lectures/w14-determinism-and-floating-point.md)).
- **Tiny constant corrections mean `step` differs.** If you see 1 mm corrections on every snapshot while walking on flat ground, client and server are not running the same code, the same `dt` or the same data. Fix the cause. Do not raise the threshold.

### Check this example

1. A snapshot arrives with `x = 12.0` and ack 200. The client's pending inputs are 198 to 209, all "right", with no snare. What does the client drop, what does it replay, and where does it end up?
2. In the table, why is the correction in the fifth row zero even though the snare is still active?
3. With smoothing time 0.2 s instead of 0.1 s, how far does the drawn character move backward per frame after the 0.5 m correction, while the snared player walks at 3 m/s?

<details>
<summary>Answers</summary>

1. It drops 198, 199 and 200, sets `x = 12.0`, and replays 201 to 209, nine inputs of 0.1 m, ending at 12.9.
2. After the fourth snapshot, the client knows the snare covers inputs 56 to 115. Its predictions for inputs 66 onward used half speed, so they already match what the server computes.
3. The offset shrinks by `0.5 / 12 = 0.0417` m per frame over 12 frames, and the character gains `3 / 60 = 0.05` m per frame. The net is `+0.0083` m, so it no longer moves backward at all, it just walks slowly for 0.2 s. That is a reason to choose a longer smoothing time for slows.

</details>

## 3. Loss and late snapshots

Snapshots get lost. Reconciliation does not care which snapshot arrives, since each carries its own ack and complete state (or a delta against an acked baseline, week 7). A lost snapshot means the client waits 50 ms more for the truth, and the pending queue grows by three inputs meanwhile.

The simulator shows the cost. At a 150 ms round trip and 20% snapshot loss (seed 1):

```
$ python netsim.py --mode reconcile --loss 0.2
  biggest correction 0.650 m at 1133.3 ms ...
  pending inputs while walking: 10 to 18
```

The snapshot that would have announced the snare was lost, so the client learned 50 ms later and three more inputs were predicted wrong: `0.50 + 3 × 0.05 = 0.65` m. Loss does not break reconciliation. It lengthens the horizon, and the correction grows with it.

Inputs are a different matter. If an input never reaches the server, or the server refuses to run it (week 4's movement check dropping a command that looks too fast), the server's state and the client's prediction differ by that input forever, and every later snapshot produces a correction. That is why clients send each input several times, in the next few packets as well as its own (week 6's redundancy, and Quake III's `cl_packetdup`, default 1). The lab's simulator assumes this is done and never loses inputs. In the lab you will turn that off and watch what happens.

## 4. The three techniques together

This course's netcode has three parts. Week 10's lag lab (`examples/w10-lag-lab.html`) lets you toggle each at 150 ms.

| Technique | Week | Applies to | Removes | Costs |
|---|---|---|---|---|
| Prediction | 8 | Your own character | Delay between key and screen | Shared code, corrections when surprised |
| Reconciliation | 9 | Your own character | Backward jumps on every snapshot | Pending-input queue, replay work |
| Interpolation | 10 | Everyone else | Stutter between snapshots | Draws others about 100 ms in the past |

The first two make *you* feel present. The third makes *others* look smooth, at the price of showing them late, which week 11's lag compensation then has to account for when you shoot at them.

## In-class activity (25 minutes)

Pairs, with the lab starter on one laptop.

1. Run `python netsim.py --mode reconcile --csv run.csv` at round trips of 50, 150 and 300 ms. For each, record the pending range and the snare correction.
2. Plot correction against round trip (a spreadsheet is fine). Fit a line. Compare its slope with `Δv = 3` m/s from the model.
3. Choose a smoothing time and a snap threshold for a game whose worst ability is a 12 m/s knockback. Justify both numbers from your plot.
4. Swap with another pair and try to break their numbers. Find a round trip or loss rate at which their choice snaps visibly or smooths something it should not.

Expected output: the plot with its slope, two chosen numbers with one sentence each, and the case the other pair found.

## Common misconceptions

- **"Reconciliation means the client rewinds time on screen."** The rewind happens inside one function call. The player sees only the final result, or a smoothed version of it.
- **"The client should reconcile to where the server is now."** The client never knows where the server is now. It knows where the server was after input `a`, and it knows its own inputs after `a`.
- **"With reconciliation, corrections never happen."** They happen exactly when the server knew something the client did not. Reconciliation removes the *false* corrections that came from comparing different moments.
- **"Smoothing makes the error go away."** The state is corrected at once. Smoothing only changes what is drawn for a tenth of a second.

## Check yourself

1. Inputs at 30 Hz, snapshots at 10 Hz, server ticks at 30 Hz, round trip 200 ms. Estimate the number of pending inputs with the model.
2. A client reconciles and sees a 2 cm correction on every snapshot while walking on flat ground with no other players. List two likely causes.
3. A vehicle game's `step` costs 0.4 ms. At 120 Hz input, 30 Hz snapshots and a 150 ms round trip, how many milliseconds per second go to replay? What fraction of a 60 fps frame budget is that on average?
4. Explain why GGPO must restore a saved state of the whole game, while the Source client only replays its own player's commands.
5. With 20% snapshot loss, the snare correction grew from 0.50 to 0.65 m. Using the model, what correction would you expect if two snapshots in a row were lost at the wrong moment?

<details>
<summary>Answers</summary>

1. `w_tick = 16.7` and `w_snap = 50` ms averages, so `n ≈ (200 + 16.7 + 50) / 33.3 ≈ 8` inputs.
2. The client and server use different `dt` values, or a constant (speed, friction) differs between the builds, or floating-point results differ between the machines (a different compiler or instruction set). Any of these makes `step` not shared.
3. `n ≈ (150 + 4.2 + 16.7) / 8.33 ≈ 20.5` inputs per snapshot, times 30 snapshots is about 615 steps, times 0.4 ms is about 246 ms of every second. Per 16.7 ms frame that is about 4.1 ms, a quarter of the budget. Too much: cap the replay or simplify the replayed `step`.
4. In a fighting game every frame depends on both players' inputs, so a wrong guess about the opponent changes everything since, including the local player. In Source, only the local player's commands are predicted, and other entities come from snapshots, so only the local player needs re-running.
5. Each lost snapshot adds 50 ms of horizon, three inputs at 60 Hz, `3 × 0.05 = 0.15` m. Two losses give about `0.50 + 0.30 = 0.80` m.

</details>

## Lab / assignment hook

[Lab 09, prediction and reconciliation](../labs/lab09.md). You implement `Client.on_input`, `Client.on_snapshot` in naive and reconciling modes, and linear smoothing, pass `--check`, then measure corrections across round trips and loss rates, remove input redundancy to see what an unrun input does, and write a short tuning memo.

## Sources

- Gambetta, G. *Fast-Paced Multiplayer*, part II, "Client-Side Prediction and Server Reconciliation" (gabrielgambetta.com). The 250 ms, two-keypress example, sequence numbers and "last processed request", reapplying pending inputs.
- Valve Developer Community, "Source Multiplayer Networking" (accessed September 2026). Prediction errors compared against the server's position, `cl_showerror`, correction smoothed over `cl_smoothtime`, `cl_smooth 0`.
- Valve, Source SDK 2013, `src/game/client/c_baseplayer.cpp` (`cl_smoothtime` default 0.1 s, linear fade of the prediction error offset; `cl_smooth` default 1), `src/game/client/prediction.cpp` (error check against the predicted frame for `commands_acknowledged − 1`), `src/game/shared/usercmd.h` (`command_number`). https://github.com/ValveSoftware/source-sdk-2013
- Epic Games, "Understanding Networked Movement in the Character Movement Component" (Unreal Engine 5.8 documentation). `ClientAdjustPosition`, replaying `SavedMoves` after a correction, `LastAckedMove`.
- GGPO SDK documentation, `doc/README.md` (GitHub `pond3r/ggpo`, created 2009). Restoring a previous state and re-running frames with corrected inputs, without rendering them.
- id Software, *Quake III Arena* source code (GPL release, 2005), `code/client/cl_input.c` and `cl_main.c`. `cl_packetdup` resends previous commands, default 1, range 0 to 5.

## Interactive spec: examples/w09-reconcile-replay.html

A small, focused example of the reconciliation loop alone. It is not the lag lab. The course's signature lag lab (prediction, reconciliation and interpolation toggles at 150 ms, with ghosts) is `examples/w10-lag-lab.html`, specified in week 10. Do not add driving, a second player or interpolation here.

**Insight the visual must make obvious:** reconciling means starting from the server's state and re-walking the pending inputs. When the client knew everything the server knew, the re-walk lands exactly on the old prediction and the correction is zero. On the one snapshot that reveals the snare, the same re-walk lands short, and the gap is `Δv × (inputs predicted wrong) × T_tick`. Skipping the replay turns every snapshot into a jump of about 0.9 m.

**Layout.** Three stacked panels at all widths, then a readout strip. No horizontal page scroll at 390 px. On narrow screens the input strip scrolls horizontally inside its own panel.

1. **Input strip.** One cell per input sequence number, from `ack − 3` to the newest predicted input. Each cell shows its sequence number and the step size the client uses for it now (0.10 or 0.05 m). Acknowledged cells (seq ≤ ack) are grey and fade out during step 1. Pending cells are outlined in the accent color. Cells inside the snare range the client knows about are filled orange. Cells the client *predicted* at full speed but now knows are snared get a small orange corner mark ("predicted wrong").
2. **Ruler.** A horizontal x axis covering `[server x − 0.3, predicted before + 0.3]` m, ticks every 0.1 m. Markers: hollow square at the snapshot's server `x` ("server, after input a"), dashed circle at the predicted `x` before the snapshot ("prediction before"), a filled circle that starts on the square and moves one cell's step per replayed input ("replay"). After the replay, a bracket between the filled circle and the dashed circle labelled with the correction in meters to two decimals (red when |correction| > 0.01 m, grey "0.00" otherwise).
3. **Algorithm panel.** The four lines of the section 2 model as text. The line being animated is highlighted: 1 drop, 2 accept, 3 replay (with a counter "input 57 of 57-65"), 4 correction.

**Controls.**
- Snapshot stepper: "Previous" and "Next" buttons and a slider over the received snapshots of the run. Default: the snapshot with ack 47 at 150 ms. Left and right arrow keys step too.
- "Play" animates the four steps for the current snapshot, 150 ms per replayed input (a "Step through" mode advances one input per click). A reduced-motion preference shows the end state at once.
- Round trip radio: 50, 100, 150, 250 ms, default 150 (the rows of the round-trip table).
- Checkbox "Snare" (default on). Off reproduces `--no-snare`.
- Checkbox "Skip the replay (naive snap)" (default off). When on, step 3 is greyed out and the result is the server `x` itself, so the bracket shows `server x − prediction before`. This is a what-if on the reconciling client's own prediction, the table's last column, not a separate naive run.
- Checkbox "Lose the snapshot that announces the snare" (default off). Removes the first snapshot whose ack is at or after the snare start (ack 56 at 150 ms). Deterministic, no random loss.
- Smoothing radio: 0, 0.1, 0.2 s, default 0. Affects only the frame strip below.
- "Jump to the snare" button selects the snapshot with the non-zero correction.

**Frame strip** (under the readouts). Eight frames around the correction, one row each: frame time, predicted `x`, drawn `x` with snap, drawn `x` with the chosen smoothing. This is the section 2 smoothing table and must reproduce it.

**Readouts.** Handled at (ms), ack `a`, server `x`, prediction before, inputs dropped, inputs replayed (count and range), `x` after replay, correction, and "inputs predicted wrong" with the product `0.05 × n` shown next to the correction.

**Simulation.** Precompute the whole run on load with exactly the model and parameters of `labs/lab09-starter/netsim.py`, port it line for line, and do not invent new constants:
- `TICK = 1/60` s, `SPEED = 6.0` m/s (0.1 m per tick), `SNARE_FACTOR = 0.5`, `SNARE_INPUTS = 60`, `SNAPSHOT_EVERY = 3` (20 Hz), snare at 1.0 s of server time, run length 3.0 s (ticks 0 to 180), script: move +1 for ticks 0 to 119, then 0.
- `step(state, seq, move)`: `speed = SPEED × (SNARE_FACTOR if snare_from ≤ seq < snare_to else 1)`, `x += move × speed × TICK`, rounded to 9 decimals. State is `{x, snare_from, snare_to}`, starting at `{0, 0, 0}`.
- Per tick, with `now = tick × TICK + 1e-9` and `one_way = RTT / 2`: the server runs every arrived input (arrival ≤ now) in order; the first input it runs at `now ≥ 1.0` sets `snare_from = seq`, `snare_to = seq + 60`; its ack is the last seq run. On ticks divisible by 3 it sends a snapshot `{x, snare_from, snare_to, ack}` arriving at `now + one_way`. Then the client handles arrived snapshots, then samples input `seq = tick + 1`, sends it (arrival `now + one_way`) and predicts it.
- Client on a snapshot: drop pending with `seq ≤ ack`, set state to the snapshot's state, replay the remaining pending inputs with `step`, correction = new `x − old x`. Smoothing: `offset = −correction` fading as `offset × (1 − t / smooth_time)`.
- "Handled at" is `tick × 1000 / 60` ms of the tick that handles the snapshot. "Prediction before" is the client's `x` before that tick's own input. The frame strip shows the predicted `x` after that tick's input, as `netsim.py`'s `predicted_x` column does.

**Test values** (assert in a hidden self-test on load; all match `python netsim.py` with a correct client):

At 150 ms with the snare, the lecture's five-row table:

| Handled at | Ack | Server `x` | Prediction before | Replayed | After | Correction | Skip-replay jump |
|---|---|---|---|---|---|---|---|
| 933.3 | 47 | 4.70 | 5.60 | 48-56 | 5.60 | 0.00 | −0.90 |
| 983.3 | 50 | 5.00 | 5.90 | 51-59 | 5.90 | 0.00 | −0.90 |
| 1033.3 | 53 | 5.30 | 6.20 | 54-62 | 6.20 | 0.00 | −0.90 |
| 1083.3 | 56 | 5.55 | 6.50 | 57-65 | 6.00 | −0.50 | −0.95 |
| 1133.3 | 59 | 5.70 | 6.15 | 60-68 | 6.15 | 0.00 | −0.45 |

Snare range 56 to 115 (`snare_from 56`, `snare_to 116`); inputs predicted wrong at ack 56: 56 to 65, ten inputs, `10 × 0.05 = 0.50`.

Round-trip sweep with the snare (the only non-zero correction of each run):

| Round trip | Replayed per snapshot while walking | Ack | Prediction before | After | Correction | Handled at | Pending after input (ticks 30-119) |
|---|---|---|---|---|---|---|---|
| 50 ms | 3 | 59 | 6.20 | 6.00 | −0.20 | 1033.3 | 4-6 |
| 100 ms | 5-6 | 58 | 6.30 | 5.95 | −0.35 | 1050.0 | 6-10 |
| 150 ms | 9 | 56 | 6.50 | 6.00 | −0.50 | 1083.3 | 10-12 |
| 250 ms | 15 | 53 | 6.80 | 6.00 | −0.80 | 1133.3 | 16-18 |

Other checks:
- Snare off, any round trip: every correction is 0.00.
- Lose the snapshot with ack 56 at 150 ms: the correction moves to the snapshot handled at 1133.3 ms with ack 59, server 5.70, prediction before 6.80, replay 60-68, after 6.15, correction −0.65 (13 inputs predicted wrong, 56 to 68). This equals the seeded 20% loss run in section 3, where the same snapshot happens to be lost.
- Smoothing 0.1 s, drawn `x` at 1066.7, 1083.3, 1100.0, 1116.7, 1133.3, 1150.0, 1166.7, 1183.3 ms: 6.500, 6.550, 6.517, 6.483, 6.450, 6.417, 6.383, 6.350; predicted `x` 6.50, 6.05, 6.10, 6.15, 6.20, 6.25, 6.30, 6.35; largest backward drawn step 0.034 m.
- Smoothing 0.2 s, same frames: 6.500, 6.550, 6.558, 6.567, 6.575, 6.583, 6.592, 6.600; no backward step (check-this-example question 3).

**First screen:** 150 ms, snare on, the snapshot with ack 47 selected and its replay already played, the marker resting on the dashed ghost, with a caption: "Start from the server, re-walk the inputs it has not seen. Correction 0.00. Press Next until something changes."
