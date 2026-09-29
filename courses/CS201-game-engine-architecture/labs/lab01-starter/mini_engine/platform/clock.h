#pragma once
// Platform layer: the only place allowed to ask the OS for the time.
#include <chrono>

inline double platform_seconds() {
    using namespace std::chrono;
    return duration<double>(steady_clock::now().time_since_epoch()).count();
}
