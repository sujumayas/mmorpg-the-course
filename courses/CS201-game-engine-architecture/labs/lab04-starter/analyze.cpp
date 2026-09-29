// analyze.cpp: replay frame_log.csv. Works once frame.hpp is complete.
//   c++ -std=c++20 -O2 analyze.cpp -o analyze && ./analyze frame_log.csv
#include <cstdio>
#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include "frame.hpp"

int main(int argc, char** argv) {
    const double hz = 60.0, T = refresh_ms(hz);
    std::ifstream in(argc > 1 ? argv[1] : "frame_log.csv");
    std::string line;
    std::getline(in, line);  // header
    std::vector<Stages> frames;
    while (std::getline(in, line)) {
        std::stringstream ss(line);
        std::string cell;
        double v[7];
        for (double& x : v) { std::getline(ss, cell, ','); x = std::stod(cell); }
        frames.push_back({v[1], v[2], v[3], v[4], v[5], v[6]});
    }

    // Part A view: which stage limits each frame that misses the budget?
    std::vector<double> work;
    std::map<std::string, int> over;
    for (const Stages& s : frames) {
        work.push_back(work_ms(s, true));
        if (work.back() > T + EPS) over[bottleneck(s)]++;
    }
    std::printf("%zu frames at %.0f Hz, pipelined\n", frames.size(), hz);
    for (auto& [stage, n] : over) std::printf("  over budget, bottleneck %-12s %d frames\n", stage.c_str(), n);

    // Part B view: the same frames through every queue depth Q and swap interval S.
    std::printf("\n    Q    S |   fps  long frames  max latency  mean latency\n");
    for (int interval : {1, 2})
        for (int depth : {1, 2, 3}) {
            Summary s = summarize(simulate(work, hz, depth, interval), hz, interval);
            std::printf("%5d %4d | %5.1f  %11d  %11.2f  %12.2f\n", depth, interval, s.fps, s.long_frames,
                        s.max_latency, s.mean_latency);
        }
}
