#pragma once
// Game-specific code: the player.
#include "gameplay/entity.h"

struct Player {
    const char* name = "Ari";
    Entity body;
};

inline Player g_player;
