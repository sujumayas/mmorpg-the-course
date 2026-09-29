#pragma once
// Engine systems layer: draws sprites (to stdout, for now).
#include <cstdio>
#include "core/math.h"
#include "platform/window.h"

inline void render_sprite(const char* name, Vec2 p) {
    std::printf("[render] %s at (%.1f, %.1f)\n", name, p.x, p.y);
}
