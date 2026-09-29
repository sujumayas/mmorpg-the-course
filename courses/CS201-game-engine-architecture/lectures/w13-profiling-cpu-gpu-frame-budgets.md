# CS201 · Week 13 — Profiling: CPU, GPU, Frame Budgets

**Why this matters:** In week 4 you learned what a frame budget is and why only the slowest stage matters. That model needs numbers, and numbers come from a profiler. Every profiler changes or blurs what it measures, and two honest tools can rank the same frame differently. This week you learn to measure a frame on the CPU and the GPU, to compute how wrong each measurement can be, and to report frame time in a form that catches the stutters players feel.

**You will be able to:**
- Compute how much instrumentation overhead inflates each function's measured time from its call count, and predict when it changes the ranking of hot spots.
- Compute how many samples, and so how many frames of capture, a sampling profiler needs to measure a function to a given relative error.
- Instrument a frame with scoped timers, compute inclusive and self time, and export the scopes as a trace a timeline viewer can open.
- Measure GPU time with timestamp queries, and report a capture as median and high-percentile frame times against a per-subsystem budget.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), the profiling-tools section of chapter 2 ("Tools of the Trade"). Tracy Profiler manual (`tracy.pdf`, current release), chapter 1, the sections on nanosecond resolution and the performance-impact benchmark, and the "Call stack sampling" section. Unity 6.6 manual, "Deep Profiling" (one page).

**Prerequisites from earlier courses:** [CS201 week 4, the frame](w04-the-frame-update-render-present.md) (the budget `T`, CPU time `C`, GPU time `G`, `W = max(C, G)` and vsync rounding; this lecture uses that notation and does not re-derive it). [CS101 week 12, debugging](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md) (reproduce, observe, hypothesize, fix). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (cost per call times number of calls). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (median and spread) and [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why error shrinks with the square root of the sample size).

**Interactive:** [`examples/w13-two-profilers.html`](../examples/w13-two-profilers.html). Keep it open during section 2.

---

## 1. From a budget to a measurement

Week 4 gave you the frame model. With a refresh interval `T` (16.67 ms at 60 Hz), a CPU time `C` and a GPU time `G`, a pipelined engine produces a frame every `W = max(C, G)`, and vsync rounds that up to a whole number of refreshes. Only the larger of `C` and `G` sets the frame rate. When the game and render work sit on separate threads, `C` becomes the slowest thread.

Every symbol in that model is a measurement. Week 4 invented its numbers. This week you get real ones. A **profiler** is a tool that measures where a running program spends its time. Two families matter.

- An **instrumenting profiler** records the clock at points you mark in the code. Each marked region is a **scope** (Unity calls them samples or markers, Tracy calls them zones). You get an exact count of calls and a timeline of every scope on every frame. You pay a small cost every time a scope opens and closes, and you see nothing you did not mark.
- A **sampling profiler** interrupts the program many times a second and records which function is running, usually with its call stack. It needs no code changes and sees everything, including libraries and the operating system. It gives statistical answers, and it cannot tell you what happened in one particular frame.

Two numbers describe each scope.

- **Inclusive time** is the scope's full duration, including the scopes inside it.
- **Self time** is inclusive time minus the inclusive time of its direct children. It is the time spent in the scope's own code.

A physics scope with 3.0 ms inclusive and 0.6 ms self is telling you that its children (broadphase, solver) hold 2.4 ms. Blame the children, not the parent.

The rest of this lecture answers one question before any optimization starts: **how wrong can the number on the screen be?**

## 2. Worked example: two profilers, two answers

### The hook

Unity's profiler has a switch called Deep Profiling. It injects instrumentation into every script method, so that every C# function call appears in the profile. The Unity 6.6 manual warns that the game runs much slower while it profiles this way, that it uses a lot of memory, and that it works best for small games with simple scripts.

At the other end, the Tracy profiler, an open-source profiler built for games, advertises that recording a zone takes only a few nanoseconds (its manual's benchmark gives 2.25 ns). Tracy also includes a sampling profiler, which by default samples at 8 kHz on Windows and 10 kHz on Linux and Android.

So some instrumentation is almost free and some slows the whole game down. Which numbers do you trust? Here is a frame where the answer changes what you would fix first.

### The model

Name the quantities for one function `f` on one thread.

- `t_f` is its true time per frame.
- `n_f` is how many times it is called per frame.
- `o` is the cost of one instrumented scope: two clock reads plus writing a record.
- `r` is a sampling profiler's rate in samples per second of running time, and `F` is the number of frames captured.

The error model of the two profilers:

```
instrumented:   measured_f = t_f + n_f × o                  inflation = 1 + o / (t_f / n_f)
sampling:       k_f = r × F × t_f                            samples that land in f
                relative error ≈ 1 / sqrt(k_f)               one standard error
```

Read the inflation term carefully. It depends on `t_f / n_f`, the **cost per call**, and not on the function's total cost. A function that runs once for 3 ms barely notices a 50 ns scope. A function that runs 40,000 times for 10 ns each is dominated by it.

The sampling error comes from counting. If a function holds a share `p` of the running time, each sample lands in it with probability `p`, and the count `k` of hits has a spread of about `sqrt(k)`. Divide by `k` and the relative error is `1 / sqrt(k)`. You met this square-root rule in MA102 week 13. To halve the error you need four times the samples.

### Numbers you can check

Here is one game-thread frame of the course engine. The numbers are invented for teaching but realistic in shape: a few expensive functions called rarely, and two cheap math helpers called many thousands of times. Times are in integer nanoseconds.

```python
import math

# True cost of one game-thread frame: name -> (total ns per frame, calls per frame)
frame = {
    "script_update":    (3_600_000,    600),
    "solver":           (3_000_000,      8),
    "anim_sample":      (2_200_000,    300),
    "ai_think":         (2_000_000,     50),
    "update_transform": (1_200_000, 20_000),
    "vec_normalize":    (  400_000, 40_000),
}
TRUE_TOTAL = sum(ns for ns, _ in frame.values())       # 12,400,000 ns = 12.4 ms

def instrumented(overhead_ns):
    """Every call opens and closes a zone; the zone's cost lands inside it."""
    return {f: ns + calls * overhead_ns for f, (ns, calls) in frame.items()}

def sampled(rate_hz, frames):
    """Expected samples per function and the relative standard error 1/sqrt(k)."""
    busy_s = frames * TRUE_TOTAL / 1e9                   # seconds the thread is running
    total = rate_hz * busy_s
    return {f: (total * ns / TRUE_TOTAL, 1 / math.sqrt(total * ns / TRUE_TOTAL))
            for f, (ns, _) in frame.items()}

deep = instrumented(overhead_ns=50)
print(f"{'function':17}{'true ms':>8}{'deep ms':>9}{'x':>6}   samples  error (8 kHz, 1 frame / 60 frames)")
one, sixty = sampled(8_000, 1), sampled(8_000, 60)
for f, (ns, calls) in frame.items():
    print(f"{f:17}{ns / 1e6:8.2f}{deep[f] / 1e6:9.2f}{deep[f] / ns:6.2f}"
          f"   {one[f][0]:5.1f} ±{100 * one[f][1]:3.0f}%   {sixty[f][0]:6.0f} ±{100 * sixty[f][1]:4.1f}%")
print(f"{'frame':17}{TRUE_TOTAL / 1e6:8.2f}{sum(deep.values()) / 1e6:9.2f}")
print("deep ranking: ", ", ".join(sorted(deep, key=deep.get, reverse=True)))
```

It prints:

```
function          true ms  deep ms     x   samples  error (8 kHz, 1 frame / 60 frames)
script_update        3.60     3.63  1.01    28.8 ± 19%     1728 ± 2.4%
solver               3.00     3.00  1.00    24.0 ± 20%     1440 ± 2.6%
anim_sample          2.20     2.21  1.01    17.6 ± 24%     1056 ± 3.1%
ai_think             2.00     2.00  1.00    16.0 ± 25%      960 ± 3.2%
update_transform     1.20     2.20  1.83     9.6 ± 32%      576 ± 4.2%
vec_normalize        0.40     2.40  6.00     3.2 ± 56%      192 ± 7.2%
frame               12.40    15.45
deep ranking:  script_update, solver, vec_normalize, anim_sample, update_transform, ai_think
```

Check two rows by hand.

- `vec_normalize` costs `400,000 / 40,000 = 10` ns per call. A 50 ns scope adds `40,000 × 50 = 2,000,000` ns. Measured: 2.4 ms, six times the truth. The cheapest function in the frame is now ranked third, ahead of animation and AI.
- `solver` costs 375,000 ns per call. Eight scopes add 400 ns, invisible at two decimal places.

The whole frame grew from 12.4 to 15.45 ms under deep instrumentation. That is the slowdown Unity's manual warns about, and 3 ms of it is the profiler measuring itself.

Now vary the overhead for the worst-hit function. The 2.25 ns row uses Tracy's published benchmark. The others are what you would get from slower timing code; measure your own engine's `o` in the lab.

| Scope cost `o` | `vec_normalize` measured | Inflation | Whole frame measured |
|---|---|---|---|
| 2.25 ns | 0.49 ms | 1.23× | 12.54 ms |
| 20 ns | 1.20 ms | 3.0× | 13.62 ms |
| 50 ns | 2.40 ms | 6.0× | 15.45 ms |
| 300 ns | 12.40 ms | 31× | 30.69 ms |

Even the fast profiler inflates the tiny function by 23%. The frame's scope count is `600 + 8 + 300 + 50 + 20,000 + 40,000 = 60,958`, so the whole-frame column is `12.4 + 60,958 × o`.

The sampling columns tell the other half. In one frame, 8 kHz sampling of a 12.4 ms thread gives about 99 samples in total. `vec_normalize` gets about 3, with a ±56% error. That is noise, not a measurement. Over 60 frames (one second of game) it gets 192 samples, ±7.2%, and every function is ranked correctly. Sampling never inflates anything, because the program does no extra work per call. It is only uncertain, and waiting reduces the uncertainty.

How long must you capture? Solve `1 / sqrt(k) = e` for `k = 1 / e²`. For ±10% you need 100 samples in the function; for ±2%, 2,500. `vec_normalize` collects 3.2 samples per frame at 8 kHz, so ±10% takes `100 / 3.2 = 31.25`, rounded up to 32 frames, about half a second at 60 fps. ±2% takes `2,500 / 3.2 = 781.25`, so 782 frames, about 13 seconds.

### Move it yourself

Open [`examples/w13-two-profilers.html`](../examples/w13-two-profilers.html). The left view is the instrumented profile: one horizontal bar per function, the true time in solid color and the overhead stacked on top in a hatched pattern, sorted by measured time. The right view is the sampling profile: the estimate for each function as a dot with an error bar, sorted by estimate. Drag the scope cost from 2.25 to 300 ns and watch `vec_normalize` and `update_transform` climb the left ranking while the right one stays put. Then drag the capture length down to one frame and watch the right view's error bars swallow each other. One profiler is biased and precise. The other is unbiased and noisy.

### Cross-game recognition

The same two error terms, per-call overhead and sample count, show up in every profiling tool you will meet.

**Unity 6.6, Deep Profiling versus markers.** Unity's normal profiler records a fixed set of engine markers plus the ones you add, a coarse instrumented profile with small `n × o`. Deep Profiling instruments every script method, so `n` becomes every call in your scripts, and the manual's warning about slowdown is our `n × o` term. The standard advice follows from the model: find the expensive subsystem with coarse markers, then add scopes only one level deeper, only there.

**Tracy (current releases).** Tracy is a hybrid: instrumented zones with a small `o` (2.25 ns in its own benchmark, using the CPU's timestamp counter rather than the operating-system timer, whose resolution its manual puts at roughly 300 ns to 1 µs), plus call-stack sampling at 8 or 10 kHz. Its manual suggests starting from sampling and adding zones later where you need them. That is our table used as a workflow: sampling first because it has no bias, instrumentation second where you need exact per-frame detail.

**Minecraft Java Edition, the debug profiler.** Minecraft ships a profiler every player can open. On the debug screen, F3 + 1 (since 1.20.2; earlier versions used Shift + F3) toggles a pie chart of named sections, and pressing Shift with a section's number drills into its sub-sections. Mojang added it in the Beta 1.9 prereleases in 2011. It is a coarse instrumented profile: a few dozen named sections, each opened once or a few times per frame, so `n × o` stays small. F3 + 2 shows a bar graph of the last 240 frame times with their minimum, average and maximum, which is the capture history you need in section 5.

Three tools, one pair of trade-offs. Instrumentation is exact per frame and biased per call. Sampling is unbiased and needs time.

### Eyes-open design judgment

- **Instrument coarsely, always on.** Subsystem-level scopes (a few hundred per frame) cost microseconds even with a slow timer, so you can leave them in development builds and ship an overlay like Minecraft's. Deep instrumentation belongs in short, targeted sessions.
- **Correct for known overhead, or don't trust small numbers.** If you know `o` and count calls, you can subtract `n × o`. Some profilers do this. Many do not. A function with thousands of calls and a tiny per-call cost is exactly where an uncorrected profile misleads.
- **Use sampling for "where", instrumentation for "when".** Sampling over many seconds tells you where time goes on average. Only instrumentation tells you what happened in frame 812, the one that hitched.
- **Your profiler's frame is not the player's frame.** Once measuring adds 3 ms, you are looking at a different program: one that may fall off the vsync cliff from week 4 while the real one would not. Always check the uninstrumented frame time before and after.

### Check yourself on the worked example

1. `update_transform` costs 60 ns per call. With `o = 20` ns, what is its inflation? At what `o` would its measured time double?
2. A function takes 0.8 ms of a 12.8 ms thread. At 10 kHz, how many frames must you capture to measure it to ±5%?
3. A teammate removes the scopes from `vec_normalize` and `update_transform` only (the profile still has the other 958 scopes). With `o = 50` ns, what is the measured frame now, and is the ranking correct?

<details>
<summary>Answers</summary>

1. `1 + 20 / 60 = 1.33×`. It doubles when `o` equals the per-call cost, 60 ns.
2. `k = 1 / 0.05² = 400` samples needed. Per frame the thread gives `10,000 × 0.0128 = 128` samples, of which `128 × 0.8 / 12.8 = 8` land in the function. `400 / 8 = 50` frames.
3. Overhead `958 × 50 ns = 0.048` ms, so the frame measures 12.45 ms. The four instrumented functions now show their true order. The helpers' 1.6 ms has not gone away; it shows up as self time in whatever calls them. You lose their per-call detail, which sampling can give you.

</details>

## 3. Building an instrumenting profiler

In your engine, scopes come from an object that reads the clock when it is created and again when it is destroyed. Week 2's RAII does the work: the destructor runs when the scope ends, even on an early return.

```cpp
#include <chrono>
#include <cstdio>

struct ScopedTimer {
    const char* name;
    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    explicit ScopedTimer(const char* n) : name(n) {}
    ~ScopedTimer() {
        auto us = std::chrono::duration_cast<std::chrono::microseconds>(
            std::chrono::steady_clock::now() - start).count();
        std::printf("%s: %lld us\n", name, static_cast<long long>(us));
    }
};

volatile double sink = 0;
void physics() {
    ScopedTimer t("physics");             // starts here
    for (int i = 0; i < 1'000'000; ++i) sink = sink + i * 0.5;
}                                         // destructor prints, even on early return

int main() { physics(); }
```

Compile it with `clang++ -std=c++17 -O2 timer.cpp` and it prints one line in the form `physics: 4105 us`. Your number will differ with your machine. `steady_clock` is the right clock because it never jumps backward when the system time changes. A real engine does not print from the destructor, because printing costs far more than `o`. It appends `(name, start, end)` to a per-thread buffer and flushes the buffer once per frame.

### Inclusive and self time in code

The Python version below records nested scopes with a fake clock, so it prints the same numbers every run. The lab extends it.

```python
from contextlib import contextmanager

class Profiler:
    def __init__(self, clock):
        self.clock = clock              # any function that returns microseconds
        self.events = []                # (name, depth, start_us, end_us)
        self.depth = 0

    @contextmanager
    def scope(self, name):
        start = self.clock()
        self.depth += 1
        try:
            yield
        finally:
            self.depth -= 1
            self.events.append((name, self.depth, start, self.clock()))

class FakeClock:                        # so this example prints the same numbers every run
    def __init__(self):
        self.now = 0
    def __call__(self):
        return self.now
    def work(self, us):
        self.now += us

clock = FakeClock()
prof = Profiler(clock)
with prof.scope("frame"):
    with prof.scope("physics"):
        clock.work(600)
        with prof.scope("broadphase"):
            clock.work(900)
        with prof.scope("solver"):
            clock.work(1_500)
    with prof.scope("render_submit"):
        clock.work(4_100)

for name, depth, start, end in sorted(prof.events, key=lambda e: (e[2], e[1])):
    inclusive = end - start
    children = sum(e - s for n, d, s, e in prof.events
                   if d == depth + 1 and start <= s and e <= end)
    print(f"{'  ' * depth}{name:<16} inclusive {inclusive:>5} us   self {inclusive - children:>5} us")
```

It prints:

```
frame            inclusive  7100 us   self     0 us
  physics          inclusive  3000 us   self   600 us
    broadphase       inclusive   900 us   self   900 us
    solver           inclusive  1500 us   self  1500 us
  render_submit    inclusive  4100 us   self  4100 us
```

The `with` statement plays the role of the C++ destructor: the `finally` block runs when the scope ends. Scopes are recorded when they close, so children appear in the list before their parents. The sort by start time and then depth restores reading order.

### Seeing it on a timeline

A list of numbers is hard to read. Timeline viewers draw each scope as a bar under its parent, one lane per thread, frame after frame. You do not need to write one. The Chrome JSON trace format, first built for Chrome's `about:tracing`, is a JSON array of events that the Perfetto UI (`ui.perfetto.dev`) opens directly. A `B` event opens a scope and an `E` event closes it. Each carries `name`, `ts` (a timestamp in microseconds), `pid` and `tid`. Perfetto requires scopes on a thread to nest properly, which scoped timers guarantee. In the lab you export your profiler's events in this format and scroll through your own frames.

## 4. Measuring the GPU

A CPU timer cannot see the GPU. As week 4 showed, submitting commands returns almost at once, and the GPU runs them later, often a frame or more behind. A CPU scope around a draw call measures only the time to record the command.

To time GPU work, the GPU must time itself. Graphics APIs provide **timestamp queries**: a command placed in the command buffer that tells the GPU to write its own clock value to memory when it reaches that point. Put one before and one after a render pass and the difference is the pass's GPU time. In Vulkan the command is `vkCmdWriteTimestamp`, the result is in ticks, and the device limit `timestampPeriod` gives the nanoseconds per tick:

```
GPU time (ns) = (end_ticks − start_ticks) × timestampPeriod
```

Direct3D 12 does the same with timestamp queries and a tick frequency that `ID3D12CommandQueue::GetTimestampFrequency` returns. Three practical rules follow.

- **Results arrive late.** A query can be read only after the GPU has finished that frame. Engines keep a small ring of query sets, read frame `n`'s results two or three frames later, and show them with that delay. Never make the CPU wait for a result. You would add the very stall you are trying to measure.
- **Time passes, not draws.** A handful of timestamps per frame (shadows, opaque geometry, transparent effects, post-processing, UI) gives the budget breakdown `G` needs. For per-draw detail, use a platform or vendor tool: PIX on Windows and Xbox, NVIDIA Nsight Graphics, AMD Radeon GPU Profiler, or a frame-capture tool such as RenderDoc.
- **Ask CPU or GPU first.** The quickest check needs no tool at all. Drop the rendering resolution sharply. If the frame time falls, GPU pixel work was the bottleneck `max(C, G)`. If it does not move, the CPU was.

## 5. Spikes: capture many frames, report percentiles

A budget is a limit on every frame, not on the average frame. Players feel the one frame that took 50 ms. Week 4 showed how vsync turns uneven frame times into judder. Here the question is how to report a capture so the spikes cannot hide.

Two seconds of a game at 60 Hz: 118 frames take 14 ms, and two hit a streaming stall.

```python
import math

frames = [14_000] * 118 + [48_000, 52_000]        # two seconds at 60 Hz, in microseconds

def nearest_rank(values, p):
    ordered = sorted(values)
    return ordered[math.ceil(p / 100 * len(ordered)) - 1]

avg = sum(frames) / len(frames)
print(f"average {avg / 1000:.1f} ms = {1_000_000 / avg:.0f} fps")
print(f"median  {nearest_rank(frames, 50) / 1000:.1f} ms")
print(f"p99     {nearest_rank(frames, 99) / 1000:.1f} ms")
print(f"worst   {max(frames) / 1000:.1f} ms")
print(f"frames over 16.7 ms: {sum(f > 16_667 for f in frames)}")
```

It prints:

```
average 14.6 ms = 68 fps
median  14.0 ms
p99     48.0 ms
worst   52.0 ms
frames over 16.7 ms: 2
```

The average says 68 fps. The player sees a clear stutter once a second. The **99th percentile** (p99) is the frame time that 99% of frames meet or beat, and at 48 ms it tells the truth. [CS203 week 14](../../CS203-artificial-intelligence-for-games/lectures/w14-performance-ai-lod-and-time-slicing.md) makes the same point for one subsystem next semester, with "worst frame versus average". Percentiles generalize it: report the median for typical cost and p99 (or p99.9 for long captures) for smoothness, and set targets for both. "p99 under 16.7 ms on the minimum-spec machine, over a two-minute scripted fly-through" is a budget anyone can test. "Averages 60 fps" is not.

Spikes usually come from work that does not happen every frame: loading or streaming assets (week 7), a garbage-collection pause in the scripting layer (week 10), writing a save (week 12), a burst of physics contacts (week 11), or a shader compiled the first time a material appears. Finding them needs a profiler that keeps many frames, such as Minecraft's 240-frame graph or a trace you can scroll in Perfetto. A single-frame snapshot will almost always show you a normal frame, and a sampling profile averages the spike away, which is the section 2 trade-off again.

## 6. A profiling loop you can repeat

Put the week together into a loop you will run on your final engine.

1. **Fix the conditions.** Same build type (optimized, with coarse scopes), same scene, same camera path, same machine. Write the settings down next to the numbers.
2. **Capture many frames.** Report median and p99 of the whole frame, of each thread, and of the GPU.
3. **Find the bottleneck** with week 4's `max`. Only the slowest thread or the GPU matters for now.
4. **Locate the cost.** Sample that thread for several seconds to find where time goes, then add scopes one level deeper around the suspects to see per-frame behavior. Mind `n × o`.
5. **Change one thing** with a stated hypothesis, for example "the solver walks entities in pointer order and misses cache" from week 6.
6. **Measure again under the same conditions.** Keep the change only if the median or p99 improved by more than the frame-to-frame noise. Then return to step 3, because the bottleneck may have moved.

This is the CS101 week 12 debugging loop with a stopwatch attached. Its most common failure is skipping step 3 and optimizing a thread that was never the bottleneck.

## In-class activity (25 minutes)

Pairs, with the interactive open. Your table gets this profile of a city-builder's game thread (true times, measured with sampling over 30 seconds):

| Function | ms per frame | Calls per frame |
|---|---|---|
| citizen_update | 5.2 | 2,000 |
| path_step | 2.4 | 12,000 |
| building_tick | 1.6 | 400 |
| grid_lookup | 0.9 | 90,000 |
| ui_layout | 1.3 | 1 |

1. A teammate adds a scope to every function using a timer that costs 40 ns per scope. Compute each measured time and the new ranking. Which function would the teammate try to optimize first, and is that right?
2. Which functions can you instrument at 40 ns while keeping every function's inflation under 10%?
3. At 8 kHz, how long must you sample to measure `ui_layout` to ±5%? How long for `grid_lookup` to ±5%?
4. Write a two-sentence instrumentation plan for this game: what gets always-on scopes, and what gets measured only by sampling.

Expected output: the measured table with the new ranking, the list from step 2 with the inflation of each, the two capture lengths, and the plan.

## Common misconceptions

- **"The profiler shows the truth."** Instrumentation adds `n × o` to every scope, and sampling has an error of `1 / sqrt(k)`. Every number has an error bar; know its size.
- **"The function with the most time in a deep profile is the slowest."** Deep instrumentation inflates cheap, frequently called functions most. Check the call count and cost per call before believing it.
- **"Sampling is less accurate than instrumentation."** Sampling is noisy but unbiased. Capture long enough and it beats a biased instrument. It cannot show you one specific frame.
- **"A CPU timer around a draw call measures rendering."** It measures command recording. GPU time needs timestamp queries.
- **"My average is 60 fps, so it is smooth."** Averages hide spikes. Report median and p99.

## Check yourself

1. A physics scope has 5.0 ms inclusive time and children of 1.2, 0.9 and 2.4 ms. What is its self time? What would a negative self time tell you?
2. A function takes 0.3 µs per call and runs 10,000 times per frame. Your scope costs 45 ns. What does the profiler show for it, and by what factor is it inflated?
3. At 1 kHz (a low-rate sampler), a function holds 5% of a thread busy 15 ms per frame at 60 fps. How many seconds of capture give ±10%?
4. A GPU reports `timestampPeriod = 1.0` and the shadow pass timestamps read 1,204,000 and 3,654,000. Another GPU has `timestampPeriod = 52.08` with readings 10,000 and 57,000. Which pass is slower?
5. In a capture of 1,000 frames, 990 take 12 ms and 10 take 40 ms. Compute the average, the median, the p99 and the p99.9 (nearest rank). Which number would you put in a bug report about stutter?

<details>
<summary>Answers</summary>

1. `5.0 − (1.2 + 0.9 + 2.4) = 0.5` ms. A negative self time means the children overlapped or ran outside the parent, usually because they ran on another thread and should not be subtracted.
2. True time `10,000 × 0.3 = 3.0` ms. Overhead `10,000 × 45 ns = 0.45` ms. It shows 3.45 ms, inflated 1.15×.
3. `k = 100` samples needed. Samples per frame on this thread: `1,000 × 0.015 = 15`, of which 5% is 0.75. `100 / 0.75 ≈ 134` frames, about 2.2 seconds at 60 fps.
4. First: `(3,654,000 − 1,204,000) × 1.0 = 2,450,000` ns = 2.45 ms. Second: `47,000 × 52.08 = 2,447,760` ns ≈ 2.45 ms. They are the same to within 0.1%. Raw tick counts are meaningless until you multiply by the period.
5. Average `(990 × 12 + 10 × 40) / 1,000 = 12.28` ms. Median 12 ms. p99 is item 990 in sorted order, 12 ms. p99.9 is item 999, 40 ms. The capture lasts about 12.3 s, so the ten hitches come about every 1.2 s. Report p99.9 and the worst frame; the p99 hides this stutter because the hitches are exactly 1% of frames.

</details>

## Lab / assignment hook

[Lab 13, a frame profiler](../labs/lab13.md). You write the analysis half of a small profiler (self times, overhead correction, sample counts, percentiles and Chrome trace export), open your frame in Perfetto, then add a `ScopedTimer` with a per-thread buffer to your C++ engine, measure its `o`, and produce a budget report for your final project's demo scene. The pacing function from [lab 04](../labs/lab04.md) becomes one line of that report.

## Sources

- Unity Technologies, "Deep Profiling" (Unity 6.6 manual). Deep Profiling instruments all script methods; the application runs much slower and uses a lot of memory while profiling; best for small games with simple scripting. https://docs.unity3d.com/Manual/profiler-deep-profiling.html
- Taudul, B., Tracy Profiler, README and manual (`manual/tracy.tex`, master branch, accessed September 2026). Hybrid frame and sampling profiler for games; zone overhead 2.25 ns in the manual's benchmark; OS timers with roughly 300 ns to 1 µs resolution; default sampling at 8 kHz on Windows and 10 kHz on Linux and Android; advice to start from sampling and add instrumentation where needed. https://github.com/wolfpld/tracy
- Minecraft Wiki, "Debug screen" (Java Edition). Profiler pie chart toggled with F3 + 1 since Java Edition 1.20.2 (snapshot 23w33a), previously Shift + F3; drill-down with Shift and the section number; added in Beta 1.9 Prerelease 3 (2011); frame-time graph (F3 + 2) of the last 240 frames with minimum, average and maximum. https://minecraft.wiki/w/Debug_screen
- Khronos Group, Vulkan specification, `VkPhysicalDeviceLimits` (latest). `timestampPeriod` is the number of nanoseconds for a timestamp query to increase by 1; `vkCmdWriteTimestamp`.
- Microsoft, `ID3D12CommandQueue::GetTimestampFrequency` (Win32 API reference, d3d12.h). The tick rate for converting Direct3D 12 timestamp queries to time.
- Perfetto documentation, "Other trace formats", section "Chrome JSON format". A JSON array of events with `pid`, `tid`, `ts` in microseconds, `ph` and `name`; `B`/`E` and `X` events shown as slices; duration events must nest. https://perfetto.dev/docs/getting-started/other-formats
- Gregory, J. (2018). *Game Engine Architecture* (3rd ed.). CRC Press. Profiling tools, chapter 2.

## Interactive spec: examples/w13-two-profilers.html

**The one insight.** An instrumenting profiler is exact per frame but adds a fixed cost per call, so it inflates cheap, frequently called functions and can reorder the hot-spot list. A sampling profiler adds nothing per call but is noisy, with a relative error of `1 / sqrt(samples)` that only a longer capture reduces. Biased and precise versus unbiased and noisy.

**Layout.** Two linked views side by side on desktop, stacked on mobile (instrumented first).

- **Left, "Instrumented (every call scoped)".** Horizontal bars, one per function, sorted by measured time, largest at top. Each bar is the true time in solid color plus the overhead `n × o` stacked on the right in a hatched fill of the same hue. A label at the bar end: measured ms and inflation "×1.83". Rank numbers on the left. When a function's rank differs from its true rank, show the true rank in a small grey badge ("true #6"). Under the chart: "frame measured X.XX ms (true 12.40 ms)".
- **Right, "Sampled".** Same functions, sorted by true time (sampling is unbiased, so this is also the expected ranking). For each function, a dot at the true time and a horizontal error bar of ±1 standard error, `t_f × (1 / sqrt(k_f))`. Label: expected samples `k_f` and "±NN%". Under the chart: "total samples X over F frames".
- Use the same hue per function in both views.

**Controls.**
- Scope cost `o`: a slider on a log scale from 1 to 500 ns, with snap marks at 2.25, 20, 50 and 300 ns. Default 50.
- Instrumentation depth: radio "every function" (default) / "skip helpers" (removes scopes from `update_transform` and `vec_normalize`, which then show no overhead and a note "not instrumented").
- Sampling rate: select 1, 8, 10 kHz (default 8).
- Capture length `F`: slider from 1 to 600 frames on a log scale (default 60).
- Preset buttons: "Lecture table" (o = 50, every function, 8 kHz, F = 60), "Tracy-like" (o = 2.25), "Slow timer" (o = 300), "One frame" (F = 1).
- All controls keyboard operable with visible values.

**Data (true cost per frame in ns, calls per frame).** script_update 3,600,000 / 600; solver 3,000,000 / 8; anim_sample 2,200,000 / 300; ai_think 2,000,000 / 50; update_transform 1,200,000 / 20,000; vec_normalize 400,000 / 40,000. True total 12,400,000 ns.

**Formulas.**
```
measured_f = t_f + n_f × o                (0 overhead for uninstrumented functions)
inflation  = measured_f / t_f
frame      = sum of measured_f
k_f        = rate × F × t_f / 1e9         (t_f in ns)
error_f    = 1 / sqrt(k_f)                (relative), bar half-width = t_f × error_f
```

**Readout table** under the views, copyable: function, true ms, calls, ns per call, measured ms, inflation, samples, ±%.

**Test values.**
- o = 50, every function: vec_normalize 2.40 ms ×6.00, update_transform 2.20 ms ×1.83, frame 15.45 ms; ranking script_update, solver, vec_normalize, anim_sample, update_transform, ai_think.
- o = 2.25: vec_normalize 0.49 ms ×1.23, frame 12.54 ms; ranking equals the true ranking.
- o = 20: vec_normalize 1.20 ms ×3.00, frame 13.62 ms.
- o = 300: vec_normalize 12.40 ms ×31.0, frame 30.69 ms (12.4 + 60,958 × 0.0003 = 30.6874).
- o = 50, skip helpers: frame 12.45 ms (958 scopes), ranking equals the true ranking.
- 8 kHz, F = 1: vec_normalize 3.2 samples ±56%; script_update 28.8 ±19%.
- 8 kHz, F = 60: vec_normalize 192 ±7.2%; script_update 1,728 ±2.4%.
- 10 kHz, F = 50: a 0.8 ms function in a 12.8 ms thread would get 400 samples (±5%); use this as a sanity check if a custom-function mode is added.

**First screen.** The lecture preset, with `vec_normalize` visibly jumping to third place on the left with its "true #6" badge, and the right view showing the correct order with modest error bars. Caption above both views: "Same frame, two profilers. One adds cost per call; the other needs time."
