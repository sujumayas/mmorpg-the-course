#pragma once
// Gameplay foundations: the entity everything in the game is made of.
#include "core/math.h"
#include "core/memory.h"

struct Entity {
    const char* name = "entity";
    Vec2 position;
    Vec2 velocity;
};

inline void entity_step(Entity& e, float dt) {
    e.position = e.position + e.velocity * dt;
}
