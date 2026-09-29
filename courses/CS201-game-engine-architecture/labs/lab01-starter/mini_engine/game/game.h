#pragma once
// Game-specific code: rules and input handling.
#include <cstdio>
#include "game/player.h"

inline void game_on_key(char key) {
    if (key == 'W') g_player.body.velocity = {0.0f, 1.0f};
    std::printf("[game] key %c\n", key);
}
