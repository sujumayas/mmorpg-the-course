#pragma once
// Platform layer: a pretend window that reports key presses.
#include <cstdio>
#include "game/game.h"   // VIOLATION: the platform layer names the game

inline void platform_open_window(int w, int h) {
    std::printf("[window] %dx%d opened\n", w, h);
}

inline void platform_poll_events() {
    // Pretend the OS reported that W was pressed.
    game_on_key('W');
}
