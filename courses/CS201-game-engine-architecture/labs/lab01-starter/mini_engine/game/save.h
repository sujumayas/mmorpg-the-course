#pragma once
// Game-specific code: save slots.
#include <string>
#include <unistd.h>     // LEAK: game code calls the OS directly
#include "game/player.h"

inline bool save_slot_exists(int slot) {
    std::string path = "save" + std::to_string(slot) + ".dat";
    return access(path.c_str(), F_OK) == 0;
}
