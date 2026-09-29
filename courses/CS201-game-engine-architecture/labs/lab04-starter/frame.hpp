// frame.hpp: CS201 lab 04, the frame budget (lecture week 4, section 2) and the
// swap chain queue (section 3). Fill in every function marked TODO.
#pragma once
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>

// Tolerance for comparing times in ms. Use it wherever you round up to a vblank.
constexpr double EPS = 1e-9;

// Refresh interval T in ms for a display running at hz.
inline double refresh_ms(double hz) { return 1000.0 / hz; }

struct Frame { double start = 0, ready = 0, shown = 0; };

// ---------- Part A: the budget (section 2) ----------

// One frame's stage times in milliseconds.
struct Stages {
    double input = 0, gameplay = 0, physics = 0, animation = 0, render_prep = 0;  // CPU
    double gpu = 0;                                                               // GPU
};

// TODO A1: CPU time C, the sum of the five CPU stages.
inline double cpu_ms(const Stages& s) {
    (void)s;
    return 0.0;
}

// TODO A2: the work interval W. Serial: C + G. Pipelined: max(C, G).
inline double work_ms(const Stages& s, bool pipelined) {
    (void)s; (void)pipelined;
    return 0.0;
}

// TODO A3: which stage limits a pipelined frame? "gpu" if G > C, otherwise the name of
// the largest CPU stage: "input", "gameplay", "physics", "animation" or "render_prep".
// Ties go to the stage listed first.
inline std::string bottleneck(const Stages& s) {
    (void)s;
    return "";
}

// ---------- Part B: the queue (section 3) ----------

// TODO B1: the first vblank (a multiple of T, including 0) at or after time t.
// A t that is exactly on a vblank, up to EPS of rounding, returns that vblank.
// Section 2's displayed interval D for a constant frame is next_vblank(W, hz) when W > 0.
inline double next_vblank(double t, double hz) {
    (void)t; (void)hz;
    return -1.0;
}

// TODO B2: the three rules (depth is the lecture's Q, interval is S).
//   start[0] = 0; start[i] = max(ready[i-1], shown[i-depth] if i >= depth else 0)
//   ready[i] = start[i] + work[i]
//   shown[i] = next_vblank(ready[i]), then for i > 0 at least shown[i-1] + interval * T
inline std::vector<Frame> simulate(const std::vector<double>& work, double hz, int depth, int interval) {
    (void)work; (void)hz; (void)depth; (void)interval;
    return {};
}

// TODO B3: on-screen time of each frame, shown[i+1] - shown[i].
// One element fewer than frames (empty for fewer than 2 frames).
inline std::vector<double> on_screen_ms(const std::vector<Frame>& f) {
    (void)f;
    return {};
}

// TODO B4: latency of each frame, shown[i] - start[i].
inline std::vector<double> latency_ms(const std::vector<Frame>& f) {
    (void)f;
    return {};
}

// TODO B5: count on-screen times longer than interval * T + 0.001 ms.
// With interval 2, a steady 33.33 ms frame is expected, not long.
inline int long_frames(const std::vector<double>& on_screen, double hz, int interval) {
    (void)on_screen; (void)hz; (void)interval;
    return -1;
}

struct Summary { double fps = 0, max_latency = 0, mean_latency = 0; int long_frames = 0; };

// TODO B6: summarize a run. fps = 1000 * (n - 1) / (shown[n-1] - shown[0]).
// Latency statistics over all frames. long_frames from TODO B5.
// Return a default Summary for fewer than 2 frames.
inline Summary summarize(const std::vector<Frame>& f, double hz, int interval) {
    (void)f; (void)hz; (void)interval;
    return {};
}
