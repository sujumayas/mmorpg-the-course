// test_frame.cpp: checks for lab 04. Build and run:
//   c++ -std=c++20 -O2 test_frame.cpp -o test_frame && ./test_frame
// Exit code 0 means every check passed.
#include <cmath>
#include <cstdio>
#include "frame.hpp"

static int failures = 0;
static void check(bool ok, const char* name) {
    std::printf("%s  %s\n", ok ? "PASS" : "FAIL", name);
    if (!ok) ++failures;
}
static bool near(double a, double b) { return std::fabs(a - b) < 0.005; }
static bool all_near(const std::vector<double>& v, std::initializer_list<double> want) {
    if (v.size() != want.size()) return false;
    std::size_t i = 0;
    for (double w : want) if (!near(v[i++], w)) return false;
    return true;
}
static std::vector<double> col(const std::vector<Frame>& f, double Frame::*m) {
    std::vector<double> out;
    for (auto& x : f) out.push_back(x.*m);
    return out;
}

int main() {
    Stages city{0.3, 4.2, 2.5, 1.8, 3.2, 11.0};
    Stages raid{0.3, 6.0, 3.5, 2.4, 4.5, 11.0};
    Stages fx  {0.3, 6.0, 3.5, 2.4, 4.5, 16.9};
    check(near(cpu_ms(city), 12.0) && near(cpu_ms(raid), 16.7), "A1 cpu_ms sums the CPU stages");
    check(near(work_ms(city, false), 23.0) && near(work_ms(city, true), 12.0) && near(work_ms(fx, true), 16.9) &&
          near(work_ms(fx, false), 33.6), "A2 work_ms serial and pipelined");
    check(bottleneck(city) == "gameplay" && bottleneck(fx) == "gpu" &&
          bottleneck(Stages{1, 1, 1, 1, 1, 2}) == "input", "A3 bottleneck names the limiting stage");

    check(near(next_vblank(12, 60), 16.67) && near(next_vblank(16.7, 60), 33.33) && near(next_vblank(33.6, 60), 50.0) && near(next_vblank(0, 60), 0) &&
          near(next_vblank(1000.0 / 60.0, 60), 16.67) && near(next_vblank(3 * (1000.0 / 60.0), 60), 50.0) &&
          near(next_vblank(17, 144), 20.83), "B1 next_vblank, including exact vblanks");

    auto t = simulate(std::vector<double>(6, 12.0), 60, 2, 1);   // lecture trace
    check(all_near(col(t, &Frame::start), {0, 12, 24, 36, 50, 66.67}) &&
          all_near(col(t, &Frame::ready), {12, 24, 36, 48, 62, 78.67}) &&
          all_near(col(t, &Frame::shown), {16.67, 33.33, 50, 66.67, 83.33, 100}),
          "B2 simulate reproduces the lecture trace (W 12, Q 2, S 1)");
    auto d1 = simulate(std::vector<double>(4, 25.0), 60, 1, 1);
    check(all_near(col(d1, &Frame::start), {0, 33.33, 66.67, 100}) &&
          all_near(col(d1, &Frame::shown), {33.33, 66.67, 100, 133.33}), "B2b depth 1 waits for the screen");
    auto s2 = simulate({2.0, 2.0, 2.0}, 60, 3, 2);
    check(all_near(col(s2, &Frame::shown), {16.67, 50, 83.33}), "B2c swap interval 2 spaces images");

    check(all_near(on_screen_ms(t), {16.67, 16.67, 16.67, 16.67, 16.67}) && on_screen_ms({Frame{}}).empty(),
          "B3 on_screen_ms");
    check(all_near(latency_ms(t), {16.67, 21.33, 26, 30.67, 33.33, 33.33}), "B4 latency_ms");

    auto j = simulate(std::vector<double>(7, 25.0), 60, 2, 1);   // judder: 16.67 / 33.33
    check(long_frames(on_screen_ms(j), 60, 1) == 3 && long_frames(on_screen_ms(d1), 60, 2) == 0 &&
          long_frames(on_screen_ms(d1), 60, 1) == 3, "B5 long_frames respects the swap interval");

    auto big = simulate(std::vector<double>(121, 12.0), 60, 3, 1);
    Summary s = summarize(big, 60, 1);
    Summary jj = summarize(j, 60, 1);
    check(near(s.fps, 60) && near(s.max_latency, 50) && s.long_frames == 0 && s.mean_latency > 48.8 &&
          s.mean_latency < 48.95 && jj.long_frames == 3 && near(jj.fps, 1000.0 * 6 / (j[6].shown - j[0].shown)),
          "B6 summarize");

    std::printf("\n%d check(s) failed\n", failures);
    return failures == 0 ? 0 : 1;
}
