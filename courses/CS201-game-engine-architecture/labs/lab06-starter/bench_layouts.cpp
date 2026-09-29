// bench_layouts.cpp: time movement over AoS, hot/cold split and SoA at four sizes,
// and print the byte model's prediction. Works once layout.hpp is complete.
//   c++ -std=c++20 -O2 bench_layouts.cpp -o bench_layouts && ./bench_layouts 128
// The argument is your cache line size in bytes (macOS: sysctl hw.cachelinesize;
// Linux: getconf LEVEL1_DCACHE_LINESIZE; Windows x86-64: use 64).
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include "layout.hpp"

using Clock = std::chrono::steady_clock;

template <class F> double best_ms(F f, int runs) {
    double best = 1e9;
    for (int r = 0; r < runs; ++r) {
        auto t0 = Clock::now();
        f();
        best = std::min(best, std::chrono::duration<double, std::milli>(Clock::now() - t0).count());
    }
    return best;
}

int main(int argc, char** argv) {
    const int L = argc > 1 ? std::atoi(argv[1]) : 64;
    const float dt = 1.0f / 60.0f;
    std::printf("line %d bytes: model predicts AoS / SoA = %d / %d = %.2f out of cache\n", L,
                bytes_per_entity_aos(128, 24, L), bytes_per_entity_soa(24),
                bytes_per_entity_soa(24) ? double(bytes_per_entity_aos(128, 24, L)) / bytes_per_entity_soa(24) : 0.0);
    std::printf("%10s %10s %10s %10s %9s %9s\n", "N", "AoS ms", "split ms", "SoA ms", "AoS/SoA", "AoS/split");
    for (int n : {10'000, 100'000, 1'000'000, 10'000'000}) {
        std::vector<EntityAoS> aos(n);
        for (auto& e : aos) { e = {}; e.vx = 1; e.vy = 2; e.vz = 3; }
        auto soa = to_soa(aos);
        auto split = to_split(aos);
        int runs = n >= 10'000'000 ? 10 : 50;
        double a = best_ms([&] { move_aos(aos, dt); }, runs);
        double h = best_ms([&] { move_split(split, dt); }, runs);
        double s = best_ms([&] { move_soa(soa, dt); }, runs);
        std::printf("%10d %10.3f %10.3f %10.3f %9.1f %9.1f\n", n, a, h, s, s > 0 ? a / s : 0.0, h > 0 ? a / h : 0.0);
    }
}
