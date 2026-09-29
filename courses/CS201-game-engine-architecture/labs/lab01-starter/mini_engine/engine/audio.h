#pragma once
// Engine systems layer: plays sounds (to stdout, for now).
#include <cstdio>
#include "resources/cache.h"

inline void audio_play(const char* name) {
    std::printf("[audio] play %s\n", name);
}
