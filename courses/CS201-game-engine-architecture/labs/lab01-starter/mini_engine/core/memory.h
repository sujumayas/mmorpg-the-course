#pragma once
// Core layer: counts allocations so leaks show up at shutdown.
#include <cstdlib>

inline int g_live_allocations = 0;

inline void* core_alloc(std::size_t bytes) {
    ++g_live_allocations;
    return std::malloc(bytes);
}

inline void core_free(void* p) {
    if (p) { --g_live_allocations; std::free(p); }
}
