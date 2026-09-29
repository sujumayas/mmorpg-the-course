# CS201 · Week 04 — The Frame: Update, Render, Present

**Why this matters:** A 60 Hz frame is 16.67 ms long, and the player never sees your profiler. They see when a new image reaches the screen. Miss the budget by 0.03 ms with vsync on and the game drops from 60 to 30 fps. Queue three frames ahead and a game at a perfect 60 fps answers the controller in 50 ms instead of 17. This week you learn where a frame's time goes and how the engine turns that time into images on a display.

**You will be able to:**
- Break a frame into its stages (input, update, render preparation, GPU work, present) and compute CPU time, GPU time and the bottleneck from a stage breakdown.
- Compute the displayed frame interval under FIFO vsync for serial and pipelined CPU/GPU execution.
- Trace when each frame starts, is ready and reaches the screen for a given queue depth and swap interval, and compute on-screen time and input latency from the trace.
- Choose a queue depth, swap interval and present mode for a given game and defend the trade between smoothness and latency.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 8, sections 8.1 to 8.3 and 8.6 (the rendering loop, the game loop, loop styles, multiprocessor loops). Nystrom, *Game Programming Patterns* (2014), "Game Loop" chapter, reread the part on rendering. Android developer documentation, "Frame Pacing library" overview page (about 10 minutes).

**Prerequisites from earlier courses:** [CS101 week 3, the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md) (input, update, draw, repeat). [CS101 week 9, delta time and the fixed-timestep accumulator](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (this lecture treats the accumulator as a black box inside "update" and does not re-teach it). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (a frame as a budget of work). [CS102 week 9, the frame as a list of systems](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w09-pattern-component.md) (section 5, deferred destruction). From this course, [week 1, engine anatomy](w01-engine-anatomy-and-runtime-layers.md) and [week 3, the frame allocator](w03-memory-allocators-stack-pool-and-frame.md), which is reset at the point this lecture calls "end of frame". [Week 13](w13-profiling-cpu-gpu-frame-budgets.md) measures the numbers this lecture models.

**Interactive:** [`examples/w04-frame-budget.html`](../examples/w04-frame-budget.html). Keep it open during sections 2 and 3.

---

## 1. One frame, five stages

In CS101 you wrote the loop as three calls: read input, update, draw. An engine has to be more specific about "draw", because drawing happens on two processors and ends with a hand-off to a third piece of hardware, the display.

1. **Input.** Poll the operating system for keyboard, mouse, gamepad and window events, and turn them into the engine's input state. This takes well under a millisecond, and it starts the latency clock (section 3).
2. **Update.** Advance the simulation: gameplay, AI, physics, animation, audio triggers, networking. With a fixed timestep this stage runs zero, one or several fixed steps (CS101 week 9).
3. **Render preparation.** Still on the CPU. Decide what is visible (culling), sort it, and record **commands** for the GPU: bind this mesh, this material, draw this many triangles. Nothing is drawn yet. The CPU has written a list.
4. **GPU work.** The graphics card executes the list and shades pixels into an off-screen image, the **back buffer**. This runs on different hardware, so it can overlap with CPU work.
5. **Present.** The engine hands the back buffer to the operating system. It joins the **swap chain**, a small queue of finished images. The display picks up a new image only at a **vertical blank** (vblank), the gap between two screen refreshes. Waiting for vblank is called **vsync**.

After present comes the **end of frame**, where per-frame bookkeeping happens. Week 3's frame allocator is reset. Entities marked for destruction are removed (CS102 week 9, section 5).

Two words you will use all term. **Frame time** is the time between two images reaching the screen; the player feels it. **Stage time** is how long one stage takes; the profiler shows it. This lecture is about the gap between them.

Larger engines split the CPU work across threads. Unreal Engine runs gameplay on a game thread and render preparation on a render thread, shown as "Game" and "Draw" in its `stat unit` overlay. While the render thread records frame N, the game thread already simulates frame N+1. Gregory covers this in section 8.6. The overlap principle in section 2 works the same way for two threads as for CPU and GPU.

## 2. Worked example: the 16.6 ms budget

### The hook

Two things surprise almost every student the first time they profile a game.

The first. Unreal Engine's `stat unit` overlay shows Frame, Game, Draw and GPU times. Say Game is 12 ms, Draw 9 ms and GPU 11 ms. They add up to 32 ms, which would be 31 fps. The Frame number reads about 12 ms and the game runs at 60 fps. Epic's documentation explains that the threads sync up before a frame ends, so Frame time usually sits close to one thread's time. It is not their total.

The second. Google's documentation for the Android Frame Pacing library describes a game rendering at 30 fps on a 60 Hz phone. The counter says 30. The player sees frames that stay up for 16, 33 and 49 ms in an uneven rhythm, and the motion stutters.

Both come from how stage times turn into images. This section builds the budget model; section 3 extends it to the queue.

### The model

```
T  = 1000 / R                          refresh interval in ms (16.67 at R = 60 Hz)
C  = input + update + render_prep      CPU time of one frame
G  = GPU time of one frame

serial:     W = C + G                  CPU waits for the GPU before starting the next frame
pipelined:  W = max(C, G)              CPU prepares frame N+1 while the GPU draws frame N

FIFO vsync: D = T × ceil(W / T)        time between images on screen; fps = 1000 / D
```

- `T` is the **budget**. The syllabus rounds it to 16.6 ms and earlier courses to 16.7. Compute with 16.67.
- `W` is the **work interval**, how often the engine can produce a new image.
- **Pipelining** means CPU and GPU work on different frames at once. The CPU runs one frame ahead, so a frame costs the larger of the two times, not their sum.
- **FIFO vsync** means a finished image waits for the next vblank. A frame that misses one vblank waits for the next, so `D` is always a whole number of refresh intervals. That rounding is the `ceil`.

Two consequences follow. **Only the bottleneck matters**: with `C = 12` and `G = 11`, a twice-as-fast GPU changes nothing the player sees. **The budget is a cliff**: `W = 16.60` shows at 60 fps and `W = 16.70` at 30. There is no 59.

### Numbers you can check

One frame from a busy city scene in a small MMO-style game. The numbers are invented but typical in proportion.

| Stage | Where it runs | Time (ms) | Share of 16.67 ms |
|---|---|---|---|
| Input | CPU | 0.3 | 1.8% |
| Gameplay (scripts, AI, network messages) | CPU | 4.2 | 25.2% |
| Physics (fixed steps this frame) | CPU | 2.5 | 15.0% |
| Animation | CPU | 1.8 | 10.8% |
| Render preparation (cull, sort, record) | CPU | 3.2 | 19.2% |
| **CPU total `C`** | | **12.0** | **72.0%** |
| GPU work `G` | GPU | 11.0 | 66.0% |

Check it: `0.3 + 4.2 + 2.5 + 1.8 + 3.2 = 12.0`, and `12.0 / 16.67 = 72%`. The CPU has 28% headroom and the GPU 34%.

Now a raid of 40 players arrives. Gameplay rises to 6.0 ms, physics to 3.5, animation to 2.4, render preparation to 4.5. Then a spell fills the screen with particles and the GPU rises to 16.9 ms.

| Scene | `C` | `G` | Serial `W` | Serial shown | Pipelined `W` | Pipelined shown |
|---|---|---|---|---|---|---|
| City | 12.00 | 11.00 | 23.00 | 33.33 ms (30 fps) | 12.00 | 16.67 ms (60 fps) |
| Raid | 16.70 | 11.00 | 27.70 | 33.33 ms (30 fps) | 16.70 | 33.33 ms (30 fps) |
| Raid + effects | 16.70 | 16.90 | 33.60 | 50.00 ms (20 fps) | 16.90 | 33.33 ms (30 fps) |

- **City.** Serial execution halves the frame rate of a scene that fits easily. This is why every engine pipelines.
- **Raid.** The CPU is 0.03 ms over budget, 30 microseconds. The frame rate halves. The GPU's 5.67 ms of headroom does not help.
- **Raid + effects.** Pipelined, the frame still lands on the second vblank. A 5.9 ms GPU spike cost nothing visible, because the CPU had already dropped the frame to 30.

```cpp
// frame_budget.cpp: where does a 60 Hz frame's time go, and what does the player see?
// Build: c++ -std=c++20 -O2 frame_budget.cpp -o frame_budget && ./frame_budget
#include <algorithm>
#include <cmath>
#include <cstdio>

struct Frame {
    double input, gameplay, physics, animation, render_prep;  // CPU main thread, ms
    double gpu;                                               // GPU, ms
    double cpu() const { return input + gameplay + physics + animation + render_prep; }
};

// Time between screen updates with FIFO vsync: round work up to whole refresh intervals.
double shown_ms(double work_ms, double refresh_hz) {
    const double T = 1000.0 / refresh_hz;
    return T * std::ceil(work_ms / T - 1e-9);   // tolerance: 16.67 must not become 2 intervals
}

void report(const char* name, const Frame& f, double hz) {
    double serial = f.cpu() + f.gpu;              // CPU waits for GPU every frame
    double pipelined = std::max(f.cpu(), f.gpu);  // CPU builds frame N+1 while GPU draws N
    std::printf("%-8s CPU %5.2f  GPU %5.2f | serial %5.2f -> shown %5.2f ms (%2.0f fps)"
                " | pipelined %5.2f -> shown %5.2f ms (%2.0f fps)\n",
                name, f.cpu(), f.gpu, serial, shown_ms(serial, hz), 1000 / shown_ms(serial, hz),
                pipelined, shown_ms(pipelined, hz), 1000 / shown_ms(pipelined, hz));
}

int main() {
    Frame city   {0.3, 4.2, 2.5, 1.8, 3.2, 11.0};  // the lecture's example frame
    Frame raid   {0.3, 6.0, 3.5, 2.4, 4.5, 11.0};  // 40 players on screen
    Frame raid_gpu{0.3, 6.0, 3.5, 2.4, 4.5, 16.9}; // same, plus a spell-effect storm
    report("city", city, 60);
    report("raid", raid, 60);
    report("raid+fx", raid_gpu, 60);
}
```

Output:

```
city     CPU 12.00  GPU 11.00 | serial 23.00 -> shown 33.33 ms (30 fps) | pipelined 12.00 -> shown 16.67 ms (60 fps)
raid     CPU 16.70  GPU 11.00 | serial 27.70 -> shown 33.33 ms (30 fps) | pipelined 16.70 -> shown 33.33 ms (30 fps)
raid+fx  CPU 16.70  GPU 16.90 | serial 33.60 -> shown 50.00 ms (20 fps) | pipelined 16.90 -> shown 33.33 ms (30 fps)
```

The `1e-9` is the float rule from CS101 week 1. `1000.0 / 60.0` cannot be stored exactly, so a frame of exactly one interval might compute as a hair over and round up to two.

### The visual

Open [`w04-frame-budget.html`](../examples/w04-frame-budget.html). The left view is the budget pie: a circle for 16.67 ms, split into the five CPU stages, with the GPU as a ring around it. Past the budget, the pie overflows into a red wedge. The right view is a timeline of frames: CPU bars, GPU bars, vsync ticks, and arrows to the vblank where each image lands.

Load the Raid preset and drag gameplay from 5.95 to 6.05. The pie changes by a sliver. The timeline's display row switches from a new image every vblank to one every two. **The budget view is continuous and the player's view is not.** Then flip "pipelined" off and watch the city scene, which fits both pies comfortably, fall to 30 fps.

### Cross-game recognition

- **Unreal Engine 5.8, `stat unit`.** Frame, Game, Draw and GPU are our `D` (before vsync rounding), the two CPU threads that make up `C`, and `G`. The documentation's advice is to compare Frame with the others: whichever it is close to is the bottleneck. That is `max(C, G)` read off a screen.
- **Unity 6.6, `QualitySettings.vSyncCount`.** The number of vblanks between frames, 0 to 4, default 1. At 1 on a 60 Hz display the game targets 60 fps, at 2 it targets 30, and `Application.targetFrameRate` is ignored while it is above 0. Setting 2 chooses `D = 2T` on purpose instead of falling into it.
- **Android Frame Pacing library (Android Game Development Kit, page updated February 2026).** It measures CPU and GPU time and picks the swap interval for you. On phones with both 60 and 90 Hz modes it can run a slow game at 45 fps instead of 30, which is changing `T` so that `W` rounds up less.
- **CS203 week 14 (next semester).** The AI programmer's 2 ms slice is one wedge of this pie. [That lecture](../../CS203-artificial-intelligence-for-games/lectures/w14-performance-ai-lod-and-time-slicing.md) keeps one wedge inside its budget. This one shows what happens to the frame when any wedge does not.

### Eyes-open design judgment

- **Budget below the line.** A frame that averages 16.0 ms sometimes takes 17, and each of those costs a full extra refresh. Teams commonly plan for 14 to 15 ms at 60 Hz and keep the rest for spikes.
- **30 fps is a legitimate target.** FromSoftware targeted 30 fps for Bloodborne (2015) as a design decision. A stable 33.33 ms frame gives every stage twice the time. Players reject a game that promises 60 and delivers a mix.
- **Split the budget by owner.** Give each system a number (gameplay 4 ms, physics 3 ms, AI 2 ms) and track it every build. A total over budget does not say who should fix it. The pie does.
- **Find the bottleneck first.** Halving GPU time in the raid row changes nothing the player sees. Work on `max(C, G)`, and use week 13's profiler to find it.

### Check yourself (worked example)

1. A 60 Hz game has `C = 9.5` and `G = 15.0` ms. What does the player see, serial and pipelined? Which processor is the bottleneck?
2. The same game on a 144 Hz display, pipelined. What is `T`, and what frame rate does the player see?
3. A designer wants 3 ms more gameplay in the city scene. Does it fit at 60 Hz, pipelined, and with how much headroom?

<details>
<summary>Answers</summary>

1. Serial `W = 24.5`, `ceil(24.5 / 16.67) = 2`, shown 33.33 ms (30 fps). Pipelined `W = 15.0`, shown 16.67 ms (60 fps). The GPU is the bottleneck.
2. `T = 1000 / 144 = 6.94` ms. `15.0 / 6.94 = 2.16`, so 3 intervals, `D = 20.83` ms, 48 fps.
3. `C` becomes 15.0 ms and `W = max(15.0, 11.0) = 15.0 < 16.67`. It fits, with 1.67 ms of CPU headroom.

</details>

## 3. Pacing and latency: the queue between engine and display

Section 2 assumed every frame takes the same time and nothing waits except for vblank. Real engines also wait for the swap chain. How many finished frames may queue up, and how many vblanks each must stay on screen, decide two things the frame counter never shows: whether frames arrive evenly, and how old the image is when the player sees it.

### Three rules

For frame `i`, track three times: `start[i]` when the engine begins it (reads input), `ready[i]` when it is finished and presented, and `shown[i]`, the vblank where it appears.

```
Rule 1 (start):  start[i] = max( ready[i−1],  shown[i−Q] )       shown[i−Q] counts as 0 when i < Q
Rule 2 (ready):  ready[i] = start[i] + W
Rule 3 (shown):  shown[i] = first vblank k·T with k·T ≥ ready[i] and k·T ≥ shown[i−1] + S·T

on-screen time = shown[i+1] − shown[i]        latency = shown[i] − start[i]
```

- `W` is the work interval from section 2.
- `Q` is the **queue depth**, how many finished frames may wait for the display. Rule 1 says a new frame needs a free buffer, which appears when the frame `Q` places earlier has been shown. With `Q = 1` the engine waits for each frame to reach the screen before starting the next. Windows lets a game set this with `SetMaximumFrameLatency`, which defaults to 3.
- `S` is the **swap interval**, the minimum vblanks an image stays up. Unity's `vSyncCount` is `S`.
- Rule 3 is FIFO vsync: images appear in order, only at vblanks.
- Latency leaves out the display's scan-out and the time before input polling, which add the same amount in every setting.

A trace by hand, with `W = 12` ms, 60 Hz, `Q = 2`, `S = 1`:

| Frame | start | ready | shown | latency |
|---|---|---|---|---|
| 0 | 0.00 | 12.00 | 16.67 | 16.67 |
| 1 | 12.00 | 24.00 | 33.33 | 21.33 |
| 2 | 24.00 | 36.00 | 50.00 | 26.00 |
| 3 | 36.00 | 48.00 | 66.67 | 30.67 |
| 4 | 50.00 | 62.00 | 83.33 | 33.33 |
| 5 | 66.67 | 78.67 | 100.00 | 33.33 |

Check frame 4. Rule 1: `max(ready[3], shown[2]) = max(48, 50) = 50`. The engine finished frame 3 at 48 but waited for frame 2 to leave the queue at 50. From then on every frame starts on a vblank and appears two vblanks later. Latency has climbed from 16.67 to 33.33 ms, and the frame rate never moved from 60.

The program below prints that trace, then the steady state (frames 60 to 120) for two work times, three depths and two swap intervals.

```cpp
// swapchain.cpp: when does each frame start, reach the screen, and how long does it stay?
// Build: c++ -std=c++20 -O2 swapchain.cpp -o swapchain && ./swapchain
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>

struct Frame { double start, ready, shown; };

// work: ms the engine needs per frame. hz: display refresh rate.
// depth: how many finished frames may wait for the display (swap chain queue).
// interval: minimum vblanks each image stays on screen (1 = every vblank, 2 = half rate).
std::vector<Frame> simulate(double work, double hz, int depth, int interval, int n) {
    const double T = 1000.0 / hz;
    std::vector<Frame> f(n);
    for (int i = 0; i < n; ++i) {
        double s = (i == 0) ? 0.0 : f[i - 1].ready;               // rule 1: CPU is free...
        if (i >= depth) s = std::max(s, f[i - depth].shown);      // ...and a buffer is free
        double r = s + work;                                      // rule 2
        double v = T * std::ceil(r / T - 1e-9);                   // rule 3: next vblank...
        if (i > 0) v = std::max(v, f[i - 1].shown + interval * T);// ...after the swap interval
        f[i] = {s, r, v};
    }
    return f;
}

int main() {
    auto t = simulate(12.0, 60, 2, 1, 6);
    std::printf("trace: work 12 ms, depth 2, interval 1\n");
    for (int i = 0; i < 6; ++i)
        std::printf("  frame %d start %6.2f ready %6.2f shown %6.2f latency %5.2f\n",
                    i, t[i].start, t[i].ready, t[i].shown, t[i].shown - t[i].start);

    std::printf("\nwork depth interval |  fps  on-screen min..max  latency\n");
    for (double work : {12.0, 25.0})
        for (int depth : {1, 2, 3})
            for (int interval : {1, 2}) {
                auto f = simulate(work, 60, depth, interval, 121);
                double lo = 1e9, hi = 0, lat = 0;
                for (int i = 60; i < 120; ++i) {                  // steady state: frames 60 to 120
                    double on = f[i + 1].shown - f[i].shown;
                    lo = std::min(lo, on);
                    hi = std::max(hi, on);
                    lat = std::max(lat, f[i].shown - f[i].start);
                }
                double fps = 1000.0 * 60 / (f[120].shown - f[60].shown);
                std::printf("%4.0f %5d %8d | %4.0f  %6.2f..%6.2f    %6.2f\n", work, depth, interval, fps, lo, hi, lat);
            }
}
```

Output:

```
trace: work 12 ms, depth 2, interval 1
  frame 0 start   0.00 ready  12.00 shown  16.67 latency 16.67
  frame 1 start  12.00 ready  24.00 shown  33.33 latency 21.33
  frame 2 start  24.00 ready  36.00 shown  50.00 latency 26.00
  frame 3 start  36.00 ready  48.00 shown  66.67 latency 30.67
  frame 4 start  50.00 ready  62.00 shown  83.33 latency 33.33
  frame 5 start  66.67 ready  78.67 shown 100.00 latency 33.33

work depth interval |  fps  on-screen min..max  latency
  12     1        1 |   60   16.67.. 16.67     16.67
  12     1        2 |   30   33.33.. 33.33     33.33
  12     2        1 |   60   16.67.. 16.67     33.33
  12     2        2 |   30   33.33.. 33.33     66.67
  12     3        1 |   60   16.67.. 16.67     50.00
  12     3        2 |   30   33.33.. 33.33    100.00
  25     1        1 |   30   33.33.. 33.33     33.33
  25     1        2 |   30   33.33.. 33.33     33.33
  25     2        1 |   40   16.67.. 33.33     33.33
  25     2        2 |   30   33.33.. 33.33     66.67
  25     3        1 |   40   16.67.. 33.33     33.33
  25     3        2 |   30   33.33.. 33.33    100.00
```

**When the engine is faster than the display (`W = 12`), depth adds latency and nothing else.** Frame rate and on-screen time are identical down each swap interval. Latency is `Q × T` at `S = 1` (16.67, 33.33, 50.00 ms) and `Q × 2T` at `S = 2`, up to 100 ms. The frame counter cannot tell these games apart. A player's hands can.

**When the engine is slower (`W = 25`), depth decides the rhythm.** With `Q = 1` the engine starts every frame on a vblank, finishes 25 ms later, and waits for the 33.33 ms vblank: an even 30 fps with no setting at all. With `Q = 2` or `3` the engine never waits for a buffer, finishes a frame every 25 ms, and Rule 3 shows them for 16.67 and 33.33 ms in turn. That is 40 fps on average with a two-step rhythm, the **judder** in the Android documentation. An object moving at constant speed advances 25 ms of game time per frame while the screen holds those steps for unequal times, so it seems to speed up and slow down every 50 ms. `S = 2` restores even frames at any depth.

The interactive's timeline uses these rules too. Set `W = 12` and step the depth from 1 to 3: the frames on screen do not change and the latency readout rises by 16.67 ms per step.

Rules to take away. Keep the queue short when input matters; action games commonly cap it at 1 or 2. A deeper queue absorbs spikes (a slow frame drains a queued image instead of missing a vblank) at the price of latency in every frame. If your game cannot hold `W < T` in its heaviest scenes, lock `S = 2` rather than let it judder.

## 4. Present modes and tearing

Vulkan names four common present modes, and its specification makes FIFO the only one every implementation must support. That is why the rules above use it.

| Vulkan mode | Waits for vblank? | Queue | Tearing | In the model |
|---|---|---|---|---|
| `IMMEDIATE` | No | none | Yes | `shown = ready`, no rounding |
| `FIFO` | Yes | images wait in order | No | Rule 3 |
| `FIFO_RELAXED` | Usually | in order; a late image is shown at once | Only when late | Rule 3 unless late |
| `MAILBOX` | Yes | one slot; a newer image replaces the waiting one | No | newest finished frame wins each vblank |

**Tearing** happens when the display switches images partway through drawing one, so the top of the screen shows the old frame and the bottom the new one. `IMMEDIATE` accepts it to remove all waiting. `FIFO_RELAXED` turns a small miss into a small tear instead of a 33.33 ms frame. `MAILBOX` lets the engine render as fast as it can while the display takes the newest image, which keeps latency low but spends power on frames nobody sees, a real cost on a laptop or phone. Variable-refresh displays start each refresh when a frame is ready, within a range, so Rule 3's rounding disappears inside that range.

## 5. Where the frame ends in code

A single-threaded engine frame, with the week that builds each piece:

```cpp
while (running) {
    frame_alloc.reset();                  // week 3: per-frame memory starts empty
    input.poll();                         // stage 1, week 9; start[i] in section 3
    sim.update(clock.frame_dt());         // stage 2, fixed steps inside (CS101 week 9)
    renderer.prepare(world.snapshot());   // stage 3: cull, sort, record commands (week 8)
    gpu.submit(renderer.commands());      // stage 4 starts; returns before the GPU finishes
    swapchain.present();                  // stage 5: blocks here if the queue is full (Rule 1)
    world.flush_destroyed();              // end of frame (CS102 week 9, section 5)
    profiler.end_frame();                 // week 13
}
```

This fragment names engine objects you build over the term, so it does not compile on its own. The two programs above do.

`gpu.submit` returns almost at once. The CPU hands the list to the driver and moves on, which is what lets the CPU run ahead of the GPU. It is also why a CPU timer around `submit` says nothing about GPU time; week 13 uses GPU timestamp queries for that.

`swapchain.present` is where Rule 1 lives. If the queue is full, the CPU blocks here until the display takes an image. A profiler shows this as a long "present" or "wait" bar. It is idle time, not slow code, and in the `W = 12` rows of section 3 it is exactly the time that becomes latency.

`world.snapshot()` is the hand-off point when render preparation moves to its own thread. The game thread copies what rendering needs (transforms, visible meshes, lights) so the render thread never reads a world that is changing. The render thread therefore draws a world one frame older than the one being simulated, one more frame of latency.

## In-class activity (25 minutes)

Pairs, one laptop with the interactive, paper for traces.

1. **Pie (8 min).** Your card gives a breakdown, for example `input 0.4, gameplay 5.1, physics 3.0, animation 2.2, render prep 4.0, GPU 13.5`. Write `C`, `G`, the bottleneck and the shown frame time at 60 Hz, serial and pipelined. Raise only the bottleneck until the frame rate drops and record where. Check it against `max(C, G) = 16.67`.
2. **Queue (10 min).** Your card also gives work times `14, 14, 22, 14, 14, 14` ms. Trace them at 60 Hz with `Q = 1` and with `Q = 3`, `S = 1`. Mark every frame on screen longer than 16.67 ms and give each latency. Which depth hides the 22 ms spike, and what does it cost before the spike?
3. **Choose (7 min).** Your card names a game: a rhythm game, a turn-based strategy game, or a city builder on a laptop. Pick `Q`, `S` and a present mode. Defend the choice in two sentences with numbers from steps 1 and 2.

Expected output: the four numbers and cliff value, two traces with marked frames and latencies, and a defended setting.

## Common misconceptions

- **"Frame time is the sum of the stage times."** Only without overlap. Pipelined, it is `max(C, G)`.
- **"17 ms per frame means about 59 fps."** Under FIFO vsync at 60 Hz, 17 ms shows as 33.33 ms, 30 fps.
- **"If the frame rate is 60, latency is 16.67 ms."** With a full queue of 3 it is 50 ms.
- **"40 fps is better than 30."** On a 60 Hz FIFO display, 40 fps alternates 16.67 and 33.33 ms frames and judders. A locked 30 is smoother.
- **"Present is slow, the profiler says so."** A long present bar is the CPU waiting for a buffer. The cause is elsewhere.

## Check yourself

1. At 60 Hz, CPU stages `0.2, 3.8, 2.0, 1.5, 2.9` ms and `G = 12.5`. Compute `C`, the pipelined shown frame time, and each processor's headroom.
2. At 120 Hz, pipelined, `C = 7.9` and `G = 8.4`. What does the player see? Which 0.1 ms cut restores the full rate?
3. At 60 Hz, `W = 10`, `Q = 2`, `S = 1`. Predict steady-state frame rate, on-screen time and latency. What changes with `Q = 1`?
4. A menu renders in 2 ms and feels sluggish. Gameplay takes 18 ms and feels responsive. Both run at 60 Hz with `Q = 3`, `S = 1`. Explain with section 3.

<details>
<summary>Answers</summary>

1. `C = 10.4` ms. `W = max(10.4, 12.5) = 12.5`, shown 16.67 ms. CPU headroom 6.27 ms, GPU headroom 4.17 ms.
2. `T = 8.33`. `W = 8.4 > 8.33`, so `D = 16.67` ms, 60 fps. Cutting 0.1 ms of GPU restores 120 fps. Cutting CPU does nothing.
3. The engine outruns the display and fills the queue: 60 fps, 16.67 ms per frame, latency `2 × 16.67 = 33.33` ms. With `Q = 1`, the same frames and 16.67 ms latency.
4. Gameplay's `W = 18` is above `T`, so the queue never fills and latency is `W` plus the wait for the next vblank, 34 ms at most in the steady state. The menu's `W = 2` fills the queue, so every input waits `3 × 16.67 = 50` ms. Cap the queue in the menu, or delay the start of each menu frame.

</details>

## Lab / assignment hook

[Lab 04, frame pacer](../labs/lab04.md). You implement the budget model and the three queue rules in C++, check them against the lecture's tables, then replay a recorded 600-frame stage log under every combination of queue depth and swap interval. You diagnose what causes the long frames and choose settings for two different games. The functions become part of your engine's profiler overlay in week 13.

## Sources

- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 8, "The Game Loop and Real-Time Simulation", sections 8.1 to 8.6.
- Nystrom, R. (2014). *Game Programming Patterns*, "Game Loop" chapter. gameprogrammingpatterns.com/game-loop.html. Rendering captures an instant in time; buffer flips synchronized to the display refresh.
- Epic Games, "Stat Commands in Unreal Engine" (Unreal Engine 5.8 documentation). Frame, Game, Draw, GPU and RHIT in `stat unit`; Frame is often close to one thread's time because the game and draw threads sync before a frame ends. https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine
- Unity Technologies, "QualitySettings.vSyncCount" (Unity 6.6 scripting reference). Values 0 to 4, default 1, the 60/30 fps example, `targetFrameRate` ignored when `vSyncCount > 0`. https://docs.unity3d.com/ScriptReference/QualitySettings-vSyncCount.html
- Android Developers, "Frame Pacing library" (Android Game Development Kit, page updated 2026-02-26). The 30 fps on 60 Hz example with inconsistent frame times, automatic swap interval, and 45 fps on 60/90 Hz devices. https://developer.android.com/games/sdk/frame-pacing
- Microsoft, "IDXGIDevice1::SetMaximumFrameLatency" (Win32 documentation, DXGI 1.1, Windows 7 onward). Default 3, range 1 to 16. https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgidevice1-setmaximumframelatency
- The Khronos Group, "VkPresentModeKHR" (Vulkan specification reference page, current). IMMEDIATE, MAILBOX, FIFO and FIFO_RELAXED; FIFO is the only mode required to be supported. https://docs.vulkan.org/refpages/latest/refpages/source/VkPresentModeKHR.html
- Wikipedia, "Bloodborne" (accessed September 2026), citing the developers' 30 fps target as a design choice for the 2015 release.

## Interactive spec: examples/w04-frame-budget.html

**Purpose.** Signature example for the course ("16.6 ms budget pie chart: where a frame's time goes"). Make visible that the budget is continuous but the displayed frame time is not, that pipelining turns `C + G` into `max(C, G)`, and (secondary) that queue depth changes latency without changing frame rate.

**Layout.** Two linked views side by side on desktop (at least 900 px), stacked on mobile with the pie first. Controls in a left column on desktop, below the views on mobile. Numbers panel under the views.

**View A, budget pie.** A circle representing `T`. Inner disc: the five CPU stages as wedges, angle `= 360° × stage / T`, fixed order input, gameplay, physics, animation, render prep, five palette colours, each labelled with name and ms (leader lines when a wedge is under 15°). If `C > T`, the disc is full and a red hatched arc extends past 12 o'clock by `360° × (C − T) / T` (clipped at one extra turn), labelled "over by X ms". Outer ring: GPU, one arc of `360° × G / T`, same overflow rule. Centre text: "C = 12.00 / 16.67 ms", second line "G = 11.00 ms".

**View B, timeline.** x axis from 0 to about 200 ms. Rows: CPU bars (colour-split by stage), GPU bars, vblank ticks every `T`, and a display strip with one cell per refresh interval showing which frame is on screen (repeat cells hatched). Arrows from each frame's ready time to its shown vblank.
- Frame timing uses the lecture's section 3 rules with `W` from section 2: `W = C + G` in serial mode, `max(C, G)` in pipelined mode. `start[0] = 0`; `start[i] = max(ready[i−1], i ≥ Q ? shown[i−Q] : 0)`; `ready[i] = start[i] + W_i`; `shown[i] = T × ceil(ready[i] / T − 1e-9)`, then for `i > 0` at least `shown[i−1] + S × T`.
- In the timeline, draw the CPU bar from `start[i]` to `start[i] + C_i` and the GPU bar ending at `ready[i]` (pipelined: GPU bar from `ready[i] − G_i`; serial: GPU bar right after the CPU bar).

**Controls.**
- Five CPU stage sliders (0 to 12 ms, step 0.05) and a GPU slider (0 to 30 ms, step 0.05), each with a numeric input.
- Toggle pipelined / serial (default pipelined).
- Refresh rate: 30, 60, 90, 120, 144 Hz (default 60).
- Queue depth `Q`: 1, 2, 3 (default 1). Swap interval `S`: 1, 2 (default 1).
- Jitter slider 0 to 5 ms: adds a repeating deterministic pattern `+j, −j, 0` to each frame's gameplay time. No randomness.
- Presets: City, Raid, Raid + effects, "Fast engine, deep queue" (all stages scaled so `C = 12`, `G = 6`, `Q = 3`), and Custom.

**Numbers panel.** `C`, `G`, `W` with "= C + G" or "= max(C, G)", `D = T × ceil(W/T − 1e-9)` and fps for a constant frame, bottleneck, CPU headroom `T − C`, GPU headroom `T − G`, then from the simulated timeline (frames 0 to 11): on-screen times and latencies as a small table, and the steady-state latency over frames 60 to 120 of a 121-frame run.

**The one insight.** With Raid loaded, dragging gameplay from 5.95 to 6.05 changes the pie by a sliver while the display strip switches from one image per vblank to one per two vblanks. Caption above View B: "The player sees this row."

**Test values (60 Hz, pipelined unless stated, `Q = 1`, `S = 1`).**
- City `{0.3, 4.2, 2.5, 1.8, 3.2}`, G 11.0: C 12.00, W 12.00, D 16.67, 60 fps, bottleneck CPU. Serial: W 23.00, D 33.33.
- Raid `{0.3, 6.0, 3.5, 2.4, 4.5}`, G 11.0: C 16.70, D 33.33, 30 fps, "over by 0.03 ms". Serial D 33.33.
- Raid + effects, G 16.9: pipelined W 16.90, D 33.33. Serial W 33.60, D 50.00.
- 144 Hz, C 9.5, G 15.0: T 6.94, D 20.83, 48 fps.
- Queue check, `W = 12` (C 12, G 6, pipelined), `Q = 2`: shown 16.67, 33.33, 50, 66.67, 83.33, 100; latencies 16.67, 21.33, 26.00, 30.67, 33.33, 33.33. `Q = 3`: steady-state latency 50.00.
- Judder check: C 25, G 0, `Q = 2`: on-screen times alternate 16.67 and 33.33. `Q = 1`: all 33.33.

**Accessibility.** Every control keyboard operable with visible focus. Both views have `aria-label` summaries updated on change ("CPU 12.00 of 16.67 ms, GPU 11.00 ms, 60 fps, latency 16.67 ms"). Wedges have text labels and the overflow arc is hatched, so colour is not the only cue. With `prefers-reduced-motion`, no animated transitions.
