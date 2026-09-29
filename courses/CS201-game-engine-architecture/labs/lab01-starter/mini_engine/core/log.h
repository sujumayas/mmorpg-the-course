#pragma once
// Core layer: logging.
#include <cstdio>
#include "game/player.h"   // VIOLATION: core reaches up into game code

inline void core_log(const char* msg) {
    std::printf("[%s] %s\n", g_player.name, msg);
}
