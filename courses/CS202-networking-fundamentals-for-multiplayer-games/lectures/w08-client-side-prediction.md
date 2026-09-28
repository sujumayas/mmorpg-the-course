# CS202 · Week 08 — Client-side prediction

**Why this matters:** On an authoritative server, nothing you do is real until the server says so, and the server is a round trip away. Without help, every step you take arrives on your screen 150 to 300 ms after you press the key, and the game feels like steering a boat. Client-side prediction removes that delay for your own actions without giving up server authority. It is the first of the three techniques that make up modern netcode, and the other two only make sense once you have it.

**You will be able to:**
- Compute the key-to-screen delay of a client that waits for the server, from round trip time, tick rate, snapshot rate and frame rate.
- Implement prediction by running the server's movement code on the client, from the same inputs and the same fixed timestep.
- Compute how large a prediction error gets when the server knows something the client does not.
- Decide, action by action, what a game should predict, and defend each choice.

**Before class:** Gabriel Gambetta, *Fast-Paced Multiplayer*, part II, "Client-Side Prediction and Server Reconciliation", up to the heading on reconciliation. Valve Developer Community, "Source Multiplayer Networking", the section "Input prediction" (half a page). Optional history: John Carmack's .plan file entries for 2 and 10 August 1996 (GitHub archive of his plans).

**Prerequisites from earlier courses:** [CS101 week 9, delta time and the fixed-timestep accumulator](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (client and server must step with the same `dt`). [CS102 week 12, the command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (an input is a small command you can store, send and replay). [CS202 week 2](w02-latency-jitter-loss-measure-your-own.md) (the key-to-screen latency table). [CS202 week 7](w07-snapshots-and-delta-compression.md) (snapshots arrive at 20 Hz). [CS202 week 4, server authority](w04-server-authority-never-trust-the-client.md) (the client sends inputs, never results).

**Interactive:** [examples/w08-prediction-timeline.html](../examples/w08-prediction-timeline.html). Keep it open during section 2.

---

## 1. The dumb client

Week 4 made the server the only authority. The client sends **inputs** ("right arrow held this tick"), the server runs the game and sends back snapshots, and the client draws what the snapshots say. Gambetta calls this a **dumb client**, and it is a correct design. It cannot be cheated by editing the client, because the client decides nothing.

Its problem is time. Follow one key press through the machine.

1. The key goes down between two client ticks. It waits for the next tick to be sampled into an input.
2. The input travels to the server, half a round trip.
3. It waits for the server's next tick to be run.
4. The result waits for the next snapshot.
5. The snapshot travels back, the other half of the round trip.
6. The new position waits for the next frame to be drawn.

Only steps 2 and 5 are the network. The others are waits for a periodic event, and a wait for something that happens every `T` milliseconds averages `T/2` when the start time is random.

### The model

```
dumb delay  = w_input + RTT/2 + w_tick + w_snap + RTT/2 + w_frame
average     = RTT + T_input/2 + T_tick/2 + T_snap/2 + T_frame/2
best case   = RTT                     (every wait happens to be zero)
worst case  = RTT + T_input + T_tick + T_snap + T_frame
```

For this week's setup, the client samples input at 60 Hz (`T_input = 16.7` ms), the server ticks at 60 Hz (`T_tick = 16.7` ms), snapshots go out at 20 Hz (`T_snap = 50` ms) and the display runs at 60 Hz (`T_frame = 16.7` ms). The fixed part is `8.3 + 8.3 + 25 + 8.3 = 50` ms on average.

```
average dumb delay = RTT + 50 ms
```

A player walking at 6 m/s moves 0.1 m per 60 Hz tick. When they let go of the key, their dumb client keeps showing them walking for the same delay, so they **overshoot**: `6 m/s × delay`.

## 2. Worked example: 150 ms of lag, removed

### The hook

In August 1996, John Carmack was building QuakeWorld, the internet-play version of *Quake*. The original game drew your own movement from the server's messages, a dumb client, and on a modem it felt awful. On 2 August he wrote in his public .plan file that the client would now guess the result of the player's movement until the server's authoritative answer arrived, and that even over a link of more than 200 ms the movement felt like single-player, under the right circumstances. He also wrote that he was sad to lose the clean "client as terminal" design, and did it anyway. Eight days later, on 10 August, he wrote that he was cutting the guessing back, because simulating 300 ms ahead on the client was out of the question for a twitch game. Both entries, the win and the limit, are this lecture.

### The model

**Prediction** means the client runs the same movement code the server runs, on its own inputs, the moment it samples them. It does not wait. The server still runs the input too, and its answer is still the truth.

```
shared:   state[s+1] = step(state[s], input[s])       fixed dt, same code on both machines
client:   on each tick s:  send input[s];  predicted = step(predicted, input[s]);  draw predicted
server:   on arrival:      authoritative = step(authoritative, input[s])
claim:    predicted == authoritative after input s,
          if step, dt, the starting state and every input are the same on both sides
```

- `s` is the input's **sequence number**, 1, 2, 3 and so on. Both sides count the same inputs.
- `step` is one function, compiled into both the client and the server. Copying the logic by hand into a second function is how the claim stops being true.
- The starting state and "everything `step` reads" include the world around you, such as walls, slopes and debuffs. The client knows the walls. It does not know what another player did 50 ms ago.

With prediction, the delay for your own movement becomes the time to sample the input and show the next frame, about one tick on average, whatever the round trip. Half a tick goes to waiting for the next input sample and half a tick to waiting for the next frame.

```
predicted delay = w_input + w_frame ≈ 8.3 + 8.3 = 16.7 ms average at 60 Hz
```

### Numbers you can check

Average and worst-case delays from the model, with this week's rates:

| Round trip | Dumb, average | Dumb, worst | Predicted, average | Overshoot at 6 m/s (dumb, average) |
|---|---|---|---|---|
| 0 ms (LAN) | 50 ms | 100 ms | 16.7 ms | 0.30 m |
| 50 ms | 100 ms | 150 ms | 16.7 ms | 0.60 m |
| 100 ms | 150 ms | 200 ms | 16.7 ms | 0.90 m |
| 150 ms | 200 ms | 250 ms | 16.7 ms | 1.20 m |
| 250 ms | 300 ms | 350 ms | 16.7 ms | 1.80 m |

Check the 150 ms row. Average dumb delay `150 + 50 = 200` ms. Worst `150 + 16.7 + 16.7 + 50 + 16.7 = 250` ms. Overshoot `6 × 0.2 = 1.2` m, which is a body width or two. At that point you cannot stop in a doorway.

The lab's simulator, `labs/lab09-starter/netsim.py`, runs one scripted player. It holds right for 2 seconds, then lets go. The key goes down exactly on a client tick, so `w_input = 0`, and the result is one sample from the range above, not the average.

```
$ python netsim.py --mode dumb --no-snare
mode dumb: first visible move 183.3 ms after the key press
$ python netsim.py --mode reconcile --no-snare
mode reconcile: first visible move 0.0 ms after the key press
```

| Round trip | Simulated dumb client, first move | Simulated dumb client, stops after release | Predicted client |
|---|---|---|---|
| 0 ms | 50.0 ms | 0.0 ms | same frame |
| 50 ms | 83.3 ms | 83.3 ms | same frame |
| 150 ms | 183.3 ms | 183.3 ms | same frame |
| 250 ms | 283.3 ms | 283.3 ms | same frame |

Every simulated dumb value sits between the model's best case (the round trip) and its worst case. The 0 ms row shows how much the waits matter. The last held input reaches the server on the same tick a snapshot goes out, so the stop costs nothing, while the first press waits 50 ms for a snapshot.

### The code

The shared function from the lab's `netsim.py`, and the client method that Lab 09 asks you to write first. Movement is along one axis to keep the numbers readable.

```python
TICK = 1 / 60
SPEED = 6.0          # m/s, so 0.1 m per tick

def step(state, seq, move):
    """Shared by client and server. move is -1, 0 or +1."""
    snared = state["snare_from"] <= seq < state["snare_to"]
    speed = SPEED * (0.5 if snared else 1.0)
    new = dict(state)
    new["x"] = round(state["x"] + move * speed * TICK, 9)
    return new

class Client:
    def on_input(self, seq, move):
        """Called every tick, right after the input is sent to the server."""
        self.pending.append((seq, move))              # remembered for week 9
        self.state = step(self.state, seq, move)      # predict: do not wait
```

Two lines of `on_input` are the whole technique. The work is in the discipline around them. There is one `step` and one `TICK`, and every input carries a sequence number.

### The first snapshot arrives

Prediction raises a question the dumb client never had. Every 50 ms a snapshot arrives with the server's position for you. What should the client do with it?

The simplest answer is to trust the server and set your position to the snapshot's. Run it:

```
$ python netsim.py --mode naive --no-snare
```

At 150 ms round trip, the player starts moving on the first frame. Then, at 83 ms, the first snapshot arrives. It says `x = 0`, because it left the server at tick 0, before any input had arrived there. The client, which has predicted five, jumps back 0.5 m. The next two snapshots pull it back another 0.3 m and 0.1 m. From then on the client shows the server's position plus a few ticks, about a meter behind where prediction put it. And when the player lets go, the character keeps sliding for 183 ms, exactly like the dumb client.

Naive snapping throws prediction away one snapshot at a time. The snapshot is *old*. It describes the world before input 1, and the client has already predicted five inputs. Comparing them is comparing two different moments. Week 9 fixes this with the sequence numbers we have been carrying, a technique called **server reconciliation**. For the rest of this week, assume the client handles snapshots correctly and look at what prediction can and cannot get right.

### Move it yourself

Open `examples/w08-prediction-timeline.html`. The top panel is a one-axis track with your character. Hold the on-screen button, or the right arrow key, to walk. Two markers move, the dumb client's view and the predicted view. The bottom panel is a timeline of one key press, with the six waits drawn as colored segments for the dumb client and one short segment for the predicted client. Drag the round trip slider from 0 to 250 ms. The dumb bar stretches. The predicted bar does not move. Then set "on snapshot" to "naive snap" and walk again. Watch the predicted marker jump back three times and then trail the true position.

### Same idea elsewhere

**QuakeWorld (id Software, beta from September 1996).** Carmack's client predicted only the player's own movement, which is why it needed to know solidity, friction and gravity. He listed what it could not fix. Doors seemed to open late, because the client did not simulate other objects, and your rockets appeared to come from where you *had been* when you strafed and fired. In our model, `step` for movement was shared and `step` for projectiles was not. Eight days later he reined it in to under 100 ms of client-side motion, because a longer horizon made those errors too large.

**Source engine (Valve, current developer documentation).** Valve uses a 150 ms example. The client runs exactly the same code and rules as the server on its own user commands (`cl_predict 1`), so the player moves at once while the server still sees them at the old place. When the server's answer arrives, the client compares positions. A difference is a **prediction error**, and `cl_showerror 1` displays them. Only the local player, and entities only they affect, are predicted. Predicting other players would need their future keypresses. Weapon effects are predicted separately (`cl_predictweapons`, on by default in the Source SDK).

**Unreal Engine character movement (Epic documentation, Unreal Engine 5.8).** The owning client moves its character locally and records each step as a **saved move** (`FSavedMove_Character`), holding the inputs and the resulting position, in a queue ordered oldest to newest. It sends moves to the server as unreliable remote calls and relies on the queue for safety. It also combines similar consecutive moves to save bandwidth. The queue is our `pending` list with extra fields.

**GGPO rollback netcode (created 2009, now an MIT-licensed SDK).** Fighting games point prediction the other way. GGPO does not wait for the remote player's input. It guesses it from their past inputs and runs the frame at once, so the local player never feels delay. When the real input arrives and differs, it rewinds and re-runs, which is week 9's topic. In our terms, `step` is the whole game, and the unknown input is the opponent's, not the server's world.

Four systems, one idea. Run the authoritative code yourself on inputs you already know, show the result now, and treat the server's answer as a check that arrives later.

### Design judgment

- **Predict what only you control.** Your movement, your camera, your own weapon's recoil and muzzle flash. The client knows every input that decides them.
- **Do not predict outcomes that other players decide.** Damage, deaths, item pickups two players race for. Showing a kill the server then denies is worse than a 150 ms wait for the kill confirmation. Many games predict the *effect* (a blood puff, a hit sound) and wait for the *consequence* (the health bar).
- **Prediction costs code discipline.** The client must contain the server's movement code and collision data, and every change to one is a change to both. A constant copied into the client with a different value, or a frame-rate-dependent `dt`, shows up as a prediction error on every step.
- **The horizon limits it.** The error when the world surprises you grows with how far ahead you predict, which is the round trip plus the waits. Carmack found 300 ms too much for Quake. Section 3 puts numbers on this.
- **Prediction gives no authority.** A hacked client can predict whatever it likes on its own screen, and the server will still run the real inputs. Week 4's rule survives intact.

### Check this example

1. With snapshots at 30 Hz instead of 20 Hz and everything else as in section 1, what is the average dumb delay at a 100 ms round trip?
2. A dumb client at 250 ms round trip walks at 4 m/s. How far does it overshoot on average after the player releases the key?
3. In the naive-snap run, why is the first backward jump 0.5 m and not 1.2 m?

<details>
<summary>Answers</summary>

1. `T_snap/2 = 16.7` ms, so the fixed part is `8.3 + 8.3 + 16.7 + 8.3 = 41.7` ms, and the average delay is 141.7 ms.
2. Average delay `250 + 50 = 300` ms, so `4 × 0.3 = 1.2` m.
3. The first snapshot left the server at tick 0 and arrived 75 ms later, at the client's tick 5 (83 ms). By then the client had predicted 5 inputs, 0.5 m, while the snapshot reflected none. The full lag of a steady walk only builds up once inputs have been flowing for a whole round trip.

</details>

## 3. When the prediction is wrong

The claim in section 2 had a condition. The client must know everything `step` reads. Often it does not. The server may know that:

- an enemy's snare hit you (the client learns only from a later snapshot),
- another player is standing in the corridor you are running into (the client sees them in the past),
- you took knockback from an explosion,
- the server dropped or delayed one of your inputs.

Then the predicted state and the authoritative state differ, and the difference grows until the client finds out.

### A model for the error

Say something on the server changes your speed by `Δv` (a snare halving 6 m/s is `Δv = 3` m/s). The client keeps predicting at the old speed until a snapshot telling it about the change arrives. Every input the server runs after the change, up to the newest input the client has predicted when the news arrives, is predicted wrong.

```
inputs predicted wrong  n ≈ (RTT + w_tick + w_snap) / T_tick
error                   = Δv × n × T_tick ≈ Δv × (RTT + w_tick + w_snap)
```

The inputs already in flight when the snare lands account for half a round trip, and the snapshot's trip back and its wait account for the rest.

| Round trip | Error, model average | Error, simulated (`netsim.py`) | Inputs predicted wrong (simulated) |
|---|---|---|---|
| 50 ms | 3 × 0.0833 = 0.25 m | 0.20 m | 4 |
| 100 ms | 3 × 0.1333 = 0.40 m | 0.35 m | 7 |
| 150 ms | 3 × 0.1833 = 0.55 m | 0.50 m | 10 |
| 250 ms | 3 × 0.2833 = 0.85 m | 0.80 m | 16 |

The error is linear in the round trip. That is the mathematical version of Carmack's limit. Doubling how far ahead you predict doubles how wrong you are when the world surprises you. It is also why prediction does not make latency irrelevant. It hides latency until something unexpected happens, and then it converts latency into a correction the player sees.

What the client does with that 0.5 m (snap, blend, or replay) is week 9. What this week establishes is that the correction exists, that its size is `Δv × horizon`, and that no amount of client code can make it zero, because the client cannot know what it has not been told.

### Reducing surprises

You cannot remove prediction errors, but you can make them rarer and smaller.

- **Send inputs redundantly** (week 6) so the server never has to skip one.
- **Share more of `step`.** Anything the client can compute deterministically, such as moving platforms on a fixed schedule, should be simulated on the client too.
- **Tell the client early.** A snare with a 200 ms wind-up animation can be announced in the snapshot when the wind-up starts, so the client applies it at the same input the server does.
- **Design for it.** Slows that ramp in over 100 ms produce smaller position errors than instant ones, because `Δv` is small for the first few inputs.

## In-class activity (25 minutes)

Groups of three. Each group gets a list of eight actions from one game, a third-person action MMO ("dodge roll", "cast fireball", "open chest", "mount horse", "pick up loot", "take fall damage", "swap weapon", "use health potion").

1. For each action, decide whether to predict fully, predict the effect only, or wait for the server. Write one reason per action, naming the input or world state the client does or does not know.
2. For the two actions you predict fully, estimate the worst prediction error in meters or hit points at a 150 ms round trip, using section 3's model.
3. Pick one action you chose to wait for, and compute its delay at 150 ms with section 1's model. Is it acceptable for that action?

Expected output: an eight-row table, two error estimates, one delay, and a one-sentence verdict.

## Common misconceptions

- **"Prediction guesses where other players are going."** In client-server games it predicts only the local player. Other players are shown from snapshots, in the past (week 10). Fighting-game rollback is the exception, and it predicts inputs, not positions.
- **"Prediction lets the client decide where it is."** The server runs every input itself. The client's result is a preview.
- **"With prediction, latency no longer matters."** It no longer delays your own actions. It still delays everything else, and it sets the size of every correction.
- **"Just snap to the server's position when a snapshot arrives."** The snapshot describes an older input. Snapping to it undoes the prediction, as the naive run shows.

## Check yourself

1. A game ticks and samples input at 30 Hz, sends snapshots at 10 Hz and renders at 60 Hz. What is the average dumb delay at a 120 ms round trip?
2. Why must the client and server use a fixed `dt` for prediction to work, rather than each machine's measured frame time?
3. A knockback pushes a player at `Δv = 8` m/s for 0.3 s on the server. At a 100 ms round trip with section 3's waits, estimate the prediction error when the news arrives. Is it bounded by the knockback's duration?
4. Name one thing QuakeWorld's 1996 prediction got wrong according to Carmack, and which part of the model (`step`, `dt`, inputs or world knowledge) it comes from.
5. A designer wants the "open chest" animation to start instantly. Propose a design that is responsive but never shows loot the server has not granted.

<details>
<summary>Answers</summary>

1. `T_input/2 = 16.7`, `T_tick/2 = 16.7`, `T_snap/2 = 50`, `T_frame/2 = 8.3`. Average `120 + 91.7 = 211.7` ms.
2. The claim needs the same `step` with the same arguments. A variable `dt` makes each machine integrate differently, so the results diverge even with identical inputs (CS101 week 9).
3. The horizon is `100 + 8.3 + 25 = 133.3` ms, so about `8 × 0.133 = 1.07` m. Yes, it is bounded. If the knockback lasted less than the horizon, the error would be `Δv × duration`.
4. Rockets seemed to leave from where the player had been while strafing, because projectiles were not part of the client's `step`. Or doors opening late, because the client did not simulate other objects, a world-knowledge gap.
5. Predict the effect. Play the lid animation and a sound at once, and show the loot only when the server confirms. If the server denies it, close the lid. At a 150 ms round trip the loot appears about 200 ms after the click, hidden inside a longer opening animation.

</details>

## Lab / assignment hook

This week has no separate lab. Start [Lab 09, prediction and reconciliation](../labs/lab09.md) now. Its first part, implementing `Client.on_input` and measuring the dumb and naive clients, uses only this week's material. The rest waits for week 9.

## Sources

- Carmack, J. .plan entries for 2 August 1996 (client-side movement prediction in QuakeWorld, "client as terminal", 200+ ms links) and 10 August 1996 (reining prediction in to under 100 ms, 300 ms ruled out, projectiles appearing where the player was), and 18 September 1996 (QuakeWorld beta). John Carmack .plan archive, GitHub `ESWAT/john-carmack-plan-archive`, `by_year/johnc_plan_1996.txt`.
- Valve Developer Community, "Source Multiplayer Networking" (accessed September 2026). Input prediction with a 150 ms example, `cl_predict`, same code and rules as the server, prediction errors and `cl_showerror`, local player only.
- Valve, Source SDK 2013, `src/game/client/prediction.cpp`. `cl_predictweapons` default 1, `cl_showerror` default 0. https://github.com/ValveSoftware/source-sdk-2013
- Epic Games, "Understanding Networked Movement in the Character Movement Component" (Unreal Engine 5.8 documentation). `FSavedMove_Character`, saved-move queue, unreliable `ServerMove` calls, move combining.
- GGPO SDK documentation, README and `doc/README.md` (GitHub `pond3r/ggpo`, MIT licence, created 2009). Input prediction of the remote player, speculative execution, rollback.
- Gambetta, G. *Fast-Paced Multiplayer*, parts I and II (gabrielgambetta.com). Dumb client, 100 ms example, client-side prediction.

## Interactive spec: examples/w08-prediction-timeline.html

**Insight the visual must make obvious:** the dumb client's key-to-screen delay grows with the round trip, the predicted client's does not, and a predicted client that snaps to each snapshot loses the gain.

**Layout.** Two panels and a readout strip. Stack vertically at all widths. No horizontal page scroll at 390 px.

1. **Track panel.** A horizontal track 0 to 20 m with tick marks every meter. Three markers: "server" (hollow square, its true authoritative position), "dumb client" (grey circle, the position from the newest snapshot received), "predicted client" (filled circle in the accent color). A "Walk" button that walks right while held (pointer down) and the right arrow key do the same; the left arrow walks left. Releasing stops input. A "Reset" button returns everyone to 0.
2. **Timeline panel.** For one key press, two horizontal stacked bars on a ms axis from 0 to 400. Dumb bar segments, in order and each labelled: input wait (`T_input/2`), up (`RTT/2`), server tick wait (`T_tick/2`), snapshot wait (`T_snap/2`), down (`RTT/2`), frame wait (`T_frame/2`). Predicted bar: input wait and frame wait only. A toggle "average / worst" switches every wait between `T/2` and `T`.

**Controls.** Round trip slider 0-300 ms, default 150, step 10. Snapshot rate 10/20/30/60 Hz, default 20. "On snapshot" radio: "reconcile (week 9, correct)" default, "naive snap". Speed 6 m/s fixed. Tick 60 Hz fixed.

**Simulation.** Must match `labs/lab09-starter/netsim.py` without the snare: 60 Hz ticks, inputs sent every tick with one-way delay `RTT/2`, the server runs inputs on its first tick after arrival, snapshots every `60 / snapshot_rate` ticks, the client handles a snapshot on its first tick after arrival. Naive snap sets the predicted state to the snapshot. Reconcile sets it to the snapshot and replays unacknowledged inputs (so it never jumps without a snare).

**Readouts.** Dumb delay average and worst from the model (`RTT + 50` and `RTT + 100` ms at 20 Hz snapshots), predicted delay (16.7 ms, input wait plus frame wait), measured "first visible move" and "stops after release" for the last key press, overshoot `6 × average delay` in meters, and a count of backward jumps over 1 cm.

**Test values** (assert on load, 20 Hz snapshots): model averages 50, 100, 150, 200, 300 ms for round trips 0, 50, 100, 150, 250; worst 100, 150, 200, 250, 350. Simulated dumb first move with the key pressed on a tick: 50.0, 83.3, 183.3, 283.3 ms for 0, 50, 150, 250 ms. Naive snap at 150 ms: backward jumps of 0.5, 0.3 and 0.1 m at 83.3, 133.3 and 183.3 ms, and the character stops 183.3 ms after release.

**First screen:** round trip 150 ms, naive snap selected, a scripted 2-second walk already played so the jump markers are visible on the track, with a caption: "Predicted, then snapped: starts instantly, jumps back 0.9 m, and stops 183 ms late. Switch to reconcile."
