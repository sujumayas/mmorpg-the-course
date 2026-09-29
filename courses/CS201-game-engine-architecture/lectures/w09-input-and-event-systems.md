# CS201 · Week 09 — Input and Event Systems

**Why this matters:** In CS101 you read input by asking "is the key down?" once a frame, and it worked. At engine scale that design quietly drops quick taps whenever the frame rate dips, rounds every click to the end of the frame, and leaves characters walking forever after a chat box opens. Players report these as "the game ate my input" or "my shot went wide", and they are right. This week you build the input layer that engines use instead: a queue of timestamped events, turned into per-frame state, routed through a stack of contexts.

**You will be able to:**
- Compute the probability that frame-sampled input misses a tap of a given length at a given frame rate, and the timing error that sampling adds to every event.
- Implement an input layer that drains a timestamped event queue each frame and derives held, pressed and released state from events rather than samples.
- Design an input context stack with consumption and press ownership, and trace the stuck-key bug it prevents.
- Decide which inputs to merge per frame and which must never be merged, and defend the choice.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed.), chapter 9, "Human Interface Devices" (sections 9.2, 9.3 and 9.5). SDL3 wiki, `SDL_GetKeyboardState` (the remarks section) and `SDL_CommonEvent`. Godot Engine class reference (4.x), `Input`: read `is_action_just_pressed` and `use_accumulated_input`.

**Prerequisites from earlier courses:** [CS101 week 8, input handling](../../CS101-programming-for-games-i/lectures/w08-input-handling-and-movement.md) (events versus polling, action names, and edge detection from held states; this week shows where edge detection from samples breaks). [CS102 week 10, observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (the event bus, synchronous versus queued events; not repeated here). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (ring buffers and the pushdown stack of screens). [CS102 week 12, the command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (actions as data, replay). From this course, [week 1, engine anatomy](w01-engine-anatomy-and-runtime-layers.md) (how the platform layer reports events upward) and [week 4, the frame](w04-the-frame-update-render-present.md) (the input stage, and input-to-photon latency, which this week does not repeat).

**Interactive:** [w09-missed-taps.html](../examples/w09-missed-taps.html). Keep it open during section 2.

---

## 1. The input layer's job

A key press travels a long way before your gameplay code hears about it. The keyboard scans its switches and reports to the computer, the operating system turns the report into a message, and the engine's platform layer reads that message during the input stage of the frame (week 4). By the time gameplay code asks about the jump button, it is looking at the end of a pipeline. The **input layer** is the part of the engine that owns that pipeline. It has four jobs:

1. **Collect.** Drain every event the operating system has queued since the last frame: key down, key up, mouse motion, button changes, gamepad axes, window focus changes, device connect and disconnect.
2. **Translate.** Turn device codes into **actions**. You met action maps in CS101 week 8. At engine scale the map is data loaded through week 7's resource manager, so players can rebind keys and designers can add actions without code changes.
3. **Route.** Decide who gets each event: a text box, a menu, the debug console, gameplay. Section 4 is about this.
4. **Summarize.** Build the per-frame state that gameplay polls: which actions are held, which started or stopped this frame, how far the mouse moved.

CS101 gave you two ways to hear the player, events (push) and polling (pull), and said neither is better. That stays true for *gameplay code*. For the *input layer itself* there is a right answer, and the worked example shows why. The layer must be built from events. Polling is something it offers to gameplay on top.

## 2. Worked example: the tap that never happened

### The hook

In November 2019, Overwatch (patch 1.42) added a gameplay option called High Precision Mouse Input. The patch notes said it lets the game use the mouse's native polling rate when working out exactly where you shot, and warned of a slight performance cost. Before it, a shot was resolved using where your crosshair was at the game's own update, not where it was at the instant you clicked. For a slow aim the difference is nothing. For a fast flick it is a miss.

Overwatch's fix is about *when* an input happened. There is a second, blunter problem with the same cause, about *whether* it happened at all. SDL's documentation for `SDL_GetKeyboardState` states it directly: the function reports the state after all queued events are processed, so a key that was pressed and released before you process events never shows up as pressed. Both problems come from the same design, reading input by sampling state once per frame. This example puts numbers on both.

### The model

Let the game sample input once per frame, every `T` milliseconds. A tap is a press that lasts `d` milliseconds. The press can start at any moment within a frame with equal chance.

The tap is seen only if some sample falls while the key is down. Samples are `T` apart, so if `d ≥ T` a sample always lands inside. If `d < T`, the tap is missed when the whole press fits between two samples, which happens for a fraction `(T − d) / T` of possible start times:

```
P(miss) = max(0, 1 − d / T)
```

Timing has the same shape. An event that happens between samples is only noticed at the next one, so the game believes it happened up to `T` later than it did. Every event's time is rounded up to a frame boundary:

```
timing error ∈ [0, T),     mean T / 2
```

If the thing that matters is moving, the timing error becomes a position error. A crosshair sweeping at `ω` degrees per second is resolved at the wrong angle by up to `ω × T`, and by `ω × T / 2` on average.

- `T` is the sampling period, 1000 / fps in milliseconds.
- `d` is the tap duration.
- `ω` is the crosshair's angular speed during a flick.

### Numbers you can check

Frame periods: 30 fps is 33.3 ms, 60 fps is 16.7 ms, 144 fps is 6.9 ms. The tap durations below are test values, not measurements. A deliberately quick tap on a light key can be short, and the lab has you measure your own.

```python
import random

def p_miss(tap_ms, frame_ms):
    return max(0.0, 1.0 - tap_ms / frame_ms)

def simulate(tap_us, frame_us, taps=100_000, seed=3):
    """Fraction of taps that no frame sample sees. Times in integer microseconds."""
    rng = random.Random(seed)
    missed = 0
    for _ in range(taps):
        down = rng.randrange(frame_us)            # press lands anywhere in a frame
        up = down + tap_us
        next_sample = frame_us                    # samples at 0, frame_us, 2*frame_us...
        if next_sample >= up:                     # released before anyone looked
            missed += 1
    return missed / taps

for fps, frame_us in ((30, 33_333), (60, 16_667), (144, 6_944)):
    row = []
    for tap_ms in (10, 25, 50):
        row.append(f"{tap_ms} ms: {p_miss(tap_ms, frame_us / 1000):.2f} / {simulate(tap_ms * 1000, frame_us):.2f}")
    print(f"{fps:>3} fps  " + "   ".join(row))
```

```
 30 fps  10 ms: 0.70 / 0.70   25 ms: 0.25 / 0.25   50 ms: 0.00 / 0.00
 60 fps  10 ms: 0.40 / 0.40   25 ms: 0.00 / 0.00   50 ms: 0.00 / 0.00
144 fps  10 ms: 0.00 / 0.00   25 ms: 0.00 / 0.00   50 ms: 0.00 / 0.00
```

Each cell shows formula / simulation. Integer microseconds keep the comparison exact, as the course conventions require. Now the timing side, with a fast flick of `ω = 600°/s` (again a test value):

| Frame rate | `T` | Taps of 10 ms missed | Mean timing error | Mean aim error at 600°/s | Worst aim error |
|---|---|---|---|---|---|
| 30 fps | 33.3 ms | 70% | 16.7 ms | 10.0° | 20.0° |
| 60 fps | 16.7 ms | 40% | 8.3 ms | 5.0° | 10.0° |
| 144 fps | 6.9 ms | 0% | 3.5 ms | 2.1° | 4.2° |
| Events at 1,000 Hz mouse polling | 1 ms | 0% | 0.5 ms | 0.3° | 0.6° |

The last row is what Overwatch's option buys: time stamps at the mouse's own rate instead of the game's. Two more things fall out of the model.

**Misses cluster in hitches.** A game that averages 60 fps but has a 100 ms hitch while streaming a district (week 7) samples input with `T = 100` during that frame. Any tap shorter than 100 ms that starts in the hitch can vanish. Players remember exactly those moments, because they happen during the busy fights that cause hitches.

**Faster frame rates only shrink the problem.** At 144 fps, 10 ms taps are safe, but 5 ms taps are missed 28% of the time (`1 − 5/6.94`). No frame rate is high enough to make sampling correct. Events are.

### A visual you can move

Open the interactive. The top view is a timeline of 2 seconds. Tall gray lines mark frame samples. Colored blocks are key presses, generated as a stream of taps with durations you control. The middle row, "what polling sees", shows the held state at each sample and marks each tap as caught (filled) or missed (hollow). The bottom row, "what the event queue sees", shows every tap caught, each with a small tick at its true time and a line to the frame where the game processes it. Drag the frame-rate slider down and hollow blocks multiply in the polling row while the event row stays complete. Toggle "hitch" and one frame stretches to 100 ms, swallowing every tap inside it. The insight the picture must make obvious: **a sampled state can only see what is still true at the moment you look, while an event queue records what happened.**

### Cross-game recognition

- **SDL (SDL3).** `SDL_GetKeyboardState` is a snapshot, and the docs warn that a press and release between event processing never appears in it. The same library's events each carry a `timestamp` in nanoseconds. SDL offers both, and says which one loses information.
- **Godot 4.** `Input.is_action_just_pressed` is built from events, not from comparing two samples. The class reference notes that it still returns true if the action was pressed and released again quickly, "so as not to miss input". This is the fix for CS101 week 8's edge-detection table, where a press between two frames would never produce a `just_pressed` frame.
- **Godot's input accumulation.** With `use_accumulated_input` on (the default), Godot merges similar events that arrive during a frame, which limits input callbacks to the frame rate. The reference suggests turning it off for freehand drawing, where the path between samples matters. Accumulation is the same trade as sampling, applied only to events where the loss is acceptable.
- **Doom (1993, linuxdoom-1.10 source).** The engine keeps a 64-entry ring buffer of events (key down, key up, mouse, joystick) and drains all of them each tic. So Doom never loses a tap. Its `event_t` has no time field, though, so every event in a tic is treated as happening at the same moment. It solved the "whether" problem and not the "when" problem.
- **Overwatch (patch 1.42, November 2019).** The opposite emphasis: the game already had its events, and the option added precise timing for the one input where timing decides a hit.

Five systems, one rule: *state tells you what is true now; events tell you what happened and when*. Every design above chooses which of the two it keeps for which input.

### Eyes-open design judgment

- **Build the layer from events, offer polling on top.** Gameplay code should still be able to ask "is jump held?" That answer should be computed from the event stream, so it can also say "jump was pressed and released this frame".
- **Merge motion, never merge transitions.** Adding up ten mouse-motion events into one delta loses nothing for camera control. Merging a key down with its key up into "not held" loses the tap. The safe rule: sum or keep the last value for continuous inputs, and count every edge for buttons.
- **Timestamps cost something.** Using a click's true time means the simulation must know where the crosshair and targets were at that instant, not at the frame. That is interpolation or rewind work, and Overwatch warned of a performance cost. Pay it only for inputs where timing decides an outcome.
- **The server decides in multiplayer.** A client can claim any timestamp. Timestamps feed into lag compensation (see, next semester, [CS202 week 11](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md)), and the server must bound how far back it will trust them.

### Check yourself (worked example)

1. A mobile game runs at 30 fps. What fraction of 20 ms taps does a sampling design miss? What frame rate would be needed to catch them all?
2. A game averages 60 fps but has one 80 ms frame every 2 seconds. Players tap a dodge button for 30 ms at random moments. Roughly what fraction of dodges are lost?
3. With events time-stamped at 500 Hz mouse polling, what is the worst aim error for a 600°/s flick?

<details>
<summary>Answers</summary>

1. `1 − 20/33.3 = 0.40`, so 40%. Any `T ≤ 20 ms`, which is 50 fps or more.
2. In 2 seconds, the 80 ms hitch frame covers 4% of the time and ordinary frames the rest. Taps starting in the hitch are missed with probability `1 − 30/80 = 0.625`. Ordinary frames (16.7 ms) never miss a 30 ms tap. So about `0.04 × 0.625 = 2.5%` of dodges are lost, all of them during hitches.
3. `T = 2 ms`, so worst error `600 × 0.002 = 1.2°`.

</details>

## 3. From event queue to frame state

Here is the core of an event-built input layer, in C++. The platform layer (week 1) pushes `InputEvent`s into a queue as the operating system reports them. At the start of each frame, the input stage clears the per-frame counts, applies every queued event in order, and exposes the result.

```cpp
#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

enum class EventType : std::uint8_t { KeyDown, KeyUp, MouseMove };

struct InputEvent {
    EventType type;
    std::uint16_t code;       // key or button id
    float dx, dy;             // mouse motion, 0 for keys
    std::uint64_t time_ns;    // when the OS saw it, not when we read it
};

struct ButtonFrame { bool held = false; std::uint8_t presses = 0, releases = 0; };

struct InputFrame {
    std::array<ButtonFrame, 256> keys{};
    float mouse_dx = 0, mouse_dy = 0;

    void begin_frame() {                       // keep `held`, clear per-frame counts
        for (ButtonFrame& k : keys) k.presses = k.releases = 0;
        mouse_dx = mouse_dy = 0;
    }
    void apply(const InputEvent& e) {
        if (e.type == EventType::KeyDown) { keys[e.code].held = true;  ++keys[e.code].presses; }
        if (e.type == EventType::KeyUp)   { keys[e.code].held = false; ++keys[e.code].releases; }
        if (e.type == EventType::MouseMove) { mouse_dx += e.dx; mouse_dy += e.dy; }   // motion adds up
    }
    bool just_pressed(std::uint16_t k) const { return keys[k].presses > 0; }
};

int main() {
    const std::uint16_t SPACE = 32;
    // Everything the OS queued during one 33 ms frame: a 10 ms tap and three mouse moves.
    std::vector<InputEvent> queue = {
        {EventType::MouseMove, 0, 4, 0, 1'000'000},
        {EventType::KeyDown, SPACE, 0, 0, 12'000'000},
        {EventType::MouseMove, 0, 6, -1, 15'000'000},
        {EventType::KeyUp, SPACE, 0, 0, 22'000'000},
        {EventType::MouseMove, 0, 5, 1, 30'000'000},
    };
    InputFrame in;
    in.begin_frame();
    for (const InputEvent& e : queue) in.apply(e);
    std::printf("held=%d just_pressed=%d presses=%d mouse=(%.0f,%.0f)\n", in.keys[SPACE].held,
                in.just_pressed(SPACE), in.keys[SPACE].presses, in.mouse_dx, in.mouse_dy);
}
```

Compiled with `clang++ -std=c++17`, it prints `held=0 just_pressed=1 presses=1 mouse=(15,0)`.

Read that line against section 2. At the end of the frame the space bar is up, so a sampled design would report nothing. The event-built frame reports `held=0` and `just_pressed=1` at the same time, which is exactly the state that CS101's edge-detection table could never produce. The three mouse moves were summed into one delta of (15, 0), because for camera motion only the total matters. The key events were counted, not merged.

Three details matter in a real engine.

- **Counts, not flags.** A player mashing a button at 30 fps can press it twice in one frame. `presses` counts both. Whether gameplay acts on both (two quick jabs in a fighting game) or one (a menu confirm) is a gameplay decision, and the input layer must not make it by accident.
- **Keep the time stamps.** Most gameplay ignores `time_ns`, but the few systems that need it (hit resolution, rhythm games, CS101's jump buffer measured in real milliseconds) cannot recover it later. Store it in the frame's event list alongside the summary.
- **The queue is bounded.** Doom's queue holds 64 events. If a frame hitches long enough for more to arrive, the oldest are overwritten. Size the queue for your worst hitch and your noisiest device (a 1,000 Hz mouse produces 100 motion events in a 100 ms hitch), or merge motion events as they arrive.

## 4. Routing: contexts, consumption and press ownership

Not every event is for gameplay. When the chat box is open, W types a letter instead of walking. When the pause menu is open, Escape closes it instead of opening it again. Engines handle this with an **input context stack**: an ordered list of handlers, each with its own bindings, where the top one sees events first. A handler that uses an event **consumes** it, and lower handlers never see it. Handlers that do not care pass it down.

This is CS102 week 6's pushdown stack of screens, applied to input. Doom's `D_ProcessEvents` is the smallest real example: each event goes to the menu's responder first, and only if the menu does not eat it does the game's responder get it. Godot draws the same line with `_input`, which runs before GUI controls, and `_unhandled_input`, which only receives what nothing else consumed. CS101 week 8 recommended the second for gameplay for exactly this reason.

### The stuck-key bug

Here is the bug every input stack has until someone designs against it. The player holds W to walk, presses Enter to open chat, and lets go of W while typing. The release goes to the top context, which is now chat. Chat consumes it as a typed character. Gameplay never hears that W came up, so the character keeps walking after the chat closes.

The fix is **press ownership**: when a context consumes a key down, the router remembers which context took it, and routes that key's up to the same context, whatever is on top now.

```python
class Context:
    def __init__(self, name, bindings, eats_everything=False):
        self.name = name
        self.bindings = bindings              # key -> action name
        self.eats_everything = eats_everything
        self.held = set()                     # actions this context thinks are held

    def handle(self, kind, key):
        action = self.bindings.get(key, f"type '{key}'")
        if kind == "down":
            self.held.add(action)
        else:
            self.held.discard(action)


class Router:
    def __init__(self, press_ownership):
        self.stack = []                       # last element is the top
        self.owner = {}                       # key -> context that got its "down"
        self.press_ownership = press_ownership

    def route(self, kind, key):
        if kind == "up" and self.press_ownership and key in self.owner:
            self.owner.pop(key).handle("up", key)      # release goes where the press went
            return
        for ctx in reversed(self.stack):
            if key in ctx.bindings or ctx.eats_everything:
                ctx.handle(kind, key)
                if kind == "down":
                    self.owner[key] = ctx
                return


for fixed in (False, True):
    game = Context("gameplay", {"w": "move_forward", "enter": "open_chat"})
    chat = Context("chat", {"enter": "send", "escape": "close"}, eats_everything=True)
    router = Router(press_ownership=fixed)
    router.stack.append(game)
    router.route("down", "w")          # start walking
    router.route("down", "enter")      # open chat while still holding W
    router.stack.append(chat)
    router.route("up", "enter")
    router.route("up", "w")            # player lets go of W while typing
    print("fixed" if fixed else "naive", "gameplay still holds:", sorted(game.held))
```

```
naive gameplay still holds: ['move_forward', 'open_chat']
fixed gameplay still holds: []
```

Trace the naive run. Both downs reach gameplay, because chat is not on the stack yet. Then chat is pushed. Both ups reach chat first, and chat eats everything, so gameplay still believes W and Enter are held. With press ownership, each up goes to the context that took its down, and gameplay's held set empties.

Press ownership handles the common case. Two related events need their own rules:

- **Focus loss.** When the window loses focus (the player alt-tabs), a key released while another window has focus sends its up to that window, not to yours. Treat focus loss as "release everything": synthesize an up for every held key, routed by ownership. Otherwise the character walks off a cliff while the player reads a message.
- **Context pop.** When a context is popped with keys still owned by it, synthesize their ups before it goes, so the popped context cleans up its own held state.

### Action maps at engine scale

Once events are routed, each context translates keys into actions with its own map. CS101 set this up in Godot's project settings. In your engine the map is a data file loaded as a resource (week 7), keyed by action name, with one or more physical bindings per action. That gives you three features for the price of one lookup: player rebinding (write a new file), per-context meanings (W is `move_forward` in gameplay and a letter in chat), and replay, because CS102 week 12's command recordings can store actions instead of keys and replay correctly after a rebind.

One decision to make deliberately: bind **physical keys** (scan codes, the position on the keyboard) or **logical keys** (the character printed on the key). Movement should bind scan codes, so WASD sits under the same fingers on a French AZERTY keyboard. Text entry and shortcuts shown in menus ("press I for inventory") should use logical keys, so the letter the player reads is the letter they press. SDL separates the two: its documentation defines a scancode as the physical key, independent of language and keyboard mapping, and the key-state array from section 2 is indexed by scancode.

## 5. Beyond keys: the same queue carries engine events

The event queue you built is not only for keyboards. Window resize, focus change, device connect and disconnect, and "the OS wants to quit" all arrive through the same platform channel, and they have the same two properties: they happen at a moment, and missing one is a bug. A gamepad disconnect missed during a hitch leaves the player with a dead controller and no pause screen. So the input stage drains everything, input or not, and the input layer forwards non-input events to whichever engine system owns them, often through the event bus from CS102 week 10.

Keep the direction of that forwarding in mind. Week 1's dependency rule says the platform layer must not call gameplay by name. The queue is what makes that possible: the platform layer only pushes, and the input stage, which is allowed to know about higher layers, drains and routes.

## In-class activity (25 minutes)

In pairs, design the input layer for an MMO client.

The client has these contexts: gameplay (movement, abilities 1 to 9, targeting with Tab, camera with right mouse drag), chat (all text keys, Enter to send, Escape to close), a vendor window (mouse clicks, Escape to close), and a debug console (backtick toggles, all text keys).

1. Draw the context stack for "player is in the vendor window with chat open". Say which context gets each of these: W, Escape, a left click, backtick. (8 min)
2. Trace the event sequence "hold right mouse to turn the camera, open chat with Enter, release right mouse, close chat with Escape". Show what gameplay believes about the right mouse button at the end, with and without press ownership. (8 min)
3. Pick two inputs that are safe to merge per frame and two that must never be merged. For one of the unsafe ones, compute the miss probability at 30 fps for a tap length you choose. (9 min)

Expected output: a stack diagram, a two-column trace, and a four-row table of merge decisions with one computed probability.

## Common misconceptions

- **"Higher frame rate fixes dropped inputs."** It shrinks the window. Only events remove it. At 144 fps a 5 ms tap is still missed 28% of the time by a sampling design.
- **"If I use events, I can't poll."** The event-built frame state is what you poll. Events and polling are two views of the same input layer, one built from the other.
- **"Merging input events per frame is always fine."** It is fine for motion and wrong for button transitions. A merged down-and-up is a lost tap.
- **"The top context should get every event."** Releases belong to whoever took the press. Routing ups to the top context is what produces stuck keys.

## Check yourself

1. At 40 fps, what is the longest tap a sampling design can miss? What fraction of 15 ms taps does it miss?
2. A frame's event queue holds, in order: KeyDown A, KeyUp A, KeyDown A. Using section 3's `InputFrame`, what are `held`, `presses` and `releases` for A at the end of the frame, and what does `just_pressed(A)` return?
3. A game hitches for 120 ms while the player drags the mouse with a 1,000 Hz mouse and taps two keys. How many events arrive? Will a 64-entry queue like Doom's hold them, and what would you change?
4. Chat is open on top of gameplay. The player presses and holds Shift (bound to sprint in gameplay, consumed as a modifier by chat), then closes chat with Escape, then releases Shift. Under press ownership, which context receives the Shift up? Is that what you want?
5. Why should movement bind scan codes while the inventory shortcut shown in a tooltip binds a logical key?

<details>
<summary>Answers</summary>

1. Any tap shorter than `T = 25 ms` can be missed. `1 − 15/25 = 0.4`, so 40%.
2. `held = true`, `presses = 2`, `releases = 1`, and `just_pressed(A)` is true. The layer saw a full tap and the start of a second press.
3. About 120 motion events plus 4 key events, 124 in total. A 64-entry ring buffer overwrites the oldest, possibly including key events. Grow the queue, or merge consecutive motion events as they arrive so that key events are never displaced.
4. Chat took the Shift down, so chat receives the Shift up even though chat is gone. If chat was destroyed, the up is lost and nobody cares, because gameplay never believed Shift was held. That is correct. If you instead wanted Shift held during chat to start sprinting when chat closes, you would need gameplay to re-query held keys on becoming the top context, a deliberate design choice.
5. Movement cares about finger position, which scan codes preserve across layouts. The tooltip shows a letter, and the player will press the key with that letter printed on it, which is the logical key.

</details>

## Lab / assignment hook

[Lab 09, an event-built input layer](../labs/lab09.md). You implement the frame summary, an action map with rebinding, and a context stack with press ownership and focus-loss release in Python, then replay a recorded 30-second event log at 30 and 144 fps and show that your layer reports the same presses at both rates while a sampling layer does not.

## Sources

- Overwatch Wiki (Fandom), "November 5, 2019 Patch" (version 1.42.0.0.63568), transcribing Blizzard's patch notes. New gameplay option High Precision Mouse Input: uses the mouse's native polling rate to determine where you shoot; slight performance cost.
- SDL3 wiki, `SDL_Scancode` (physical key representation, independent of language and keyboard mapping), `SDL_GetKeyboardState` (remarks: state after all events are processed; a press and release before processing never shows up) and `SDL_CommonEvent` (`timestamp` in nanoseconds). https://wiki.libsdl.org/SDL3/
- Godot Engine documentation (4.x, master branch, retrieved September 2026), "Using InputEvent" (event order: `_input`, then GUI controls, then shortcut and unhandled callbacks; consuming stops propagation). Godot class reference, `Input`: `is_action_just_pressed` (returns true even if pressed and released rapidly, so as not to miss input) and `use_accumulated_input` (merges similar events per frame; enabled by default; disable for freehand drawing).
- id Software, DOOM source code (linuxdoom-1.10, released 1997), `d_event.h` (`event_t` with type and three data fields; `MAXEVENTS` 64) and `d_main.c` (`D_PostEvent`, `D_ProcessEvents` passing each event to `M_Responder` before `G_Responder`). https://github.com/id-Software/DOOM
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 9.

## Interactive spec: examples/w09-missed-taps.html

**Purpose.** Show that sampling state once per frame loses short taps and rounds every event's time to a frame boundary, and that an event queue loses neither.

**Layout.** Three stacked rows sharing one time axis (0 to 2,000 ms), plus a numbers panel. On mobile the time axis scrolls horizontally inside its own container (the page itself must not overflow), with a "fit" button.

- **Row 1, "What the player did".** Colored blocks for each key press from down to up. Vertical gray lines at every frame sample time.
- **Row 2, "What polling sees".** For each sample, a small square filled if the key is held at that instant. Each press block is redrawn here as filled (caught: at least one sample inside it) or hollow with a dashed outline and the label "missed" (no sample inside).
- **Row 3, "What the event queue sees".** Every press drawn filled. A small tick at the true down time, and a thin line from it to the next frame sample, labelled with the delay in ms on hover or focus.
- **Numbers panel.** Taps generated, caught by polling, missed by polling, observed miss rate, formula `max(0, 1 − d/T)`, mean timing delay observed and formula `T/2`, and the aim-error readout `ω × T / 2` (mean) and `ω × T` (worst) for the chosen flick speed.

**Controls.**
- Frame rate slider: 10 to 240 fps (default 30). `T = 1000 / fps`.
- Tap duration slider: 2 to 100 ms (default 10).
- Tap rate: 2 to 10 taps per second (default 5). Taps are placed with a seeded PRNG (mulberry32, seed 9) so their start times are uniform and non-overlapping (reject and redraw overlaps).
- "Re-roll taps" button (advances the seed).
- "Hitch" toggle: stretches the frame containing t = 1,000 ms to 100 ms, shifting later samples.
- "Timestamp source" select for the aim readout: "frame" (uses `T`) or "mouse 1,000 Hz" (uses 1 ms) or "mouse 500 Hz" (2 ms).
- Flick speed `ω`: 100 to 1,500 °/s (default 600).

**Test values.**
- 30 fps, 10 ms taps: formula 0.70. With 1,000 generated taps (use a hidden "long run" of 200 s when computing the observed rate shown in the panel), observed rate within 0.03 of 0.70.
- 60 fps, 10 ms: 0.40. 60 fps, 25 ms: 0.00. 144 fps, 5 ms: 0.28.
- Aim readout at 60 fps, 600 °/s, frame source: mean 5.0°, worst 10.0°. Mouse 1,000 Hz: mean 0.3°, worst 0.6°.
- Hitch on, 60 fps, 30 ms taps: only taps starting inside the 100 ms hitch frame can be missed; the panel shows them highlighted.

**The one insight.** On first load (30 fps, 10 ms taps) most blocks in row 2 are hollow while row 3 is complete. Raising the frame rate reduces the hollow blocks gradually, but only moving the tap duration above `T` removes them, while row 3 never loses one.

**Accessibility.** Native sliders, select and buttons with labels and visible focus. Caught versus missed uses fill versus hollow plus the word "missed", not color alone. Numbers panel is an `aria-live="polite"` region. A text summary under the rows ("12 of 20 taps missed by polling, 0 by events") is always present for screen readers. With `prefers-reduced-motion`, redraw without transitions.
