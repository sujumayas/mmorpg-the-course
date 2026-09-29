// layout.hpp: CS201 lab 06, three layouts for the same entity (lecture week 6).
// Fill in every function marked TODO.
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <vector>

// The lecture's 128-byte entity. Movement uses the first 24 bytes.
struct EntityAoS {
    float px, py, pz;
    float vx, vy, vz;
    float health, armor;
    std::uint32_t flags, team;
    float world[16];
    char name[24];
};
static_assert(sizeof(EntityAoS) == 128);

// Hot/cold split: movement's fields in one array, everything else in another.
struct Hot  { float px, py, pz, vx, vy, vz; };
struct Cold { float health, armor; std::uint32_t flags, team; float world[16]; char name[24]; };
static_assert(sizeof(Hot) == 24);
struct SplitEntities { std::vector<Hot> hot; std::vector<Cold> cold; };

// Struct of arrays: one array per field used by this lab's systems.
struct EntitiesSoA {
    std::vector<float> px, py, pz, vx, vy, vz, health;
    std::vector<std::uint32_t> team;
    std::size_t size() const { return px.size(); }
};

// Reference system, given: the lecture's movement loop over AoS.
inline void move_aos(std::vector<EntityAoS>& es, float dt) {
    for (auto& e : es) { e.px += e.vx * dt; e.py += e.vy * dt; e.pz += e.vz * dt; }
}

// TODO 1: copy every entity into SoA form. Entity i must be at index i in every array.
inline EntitiesSoA to_soa(const std::vector<EntityAoS>& es) {
    (void)es;
    return {};
}

// TODO 2: copy every entity into the hot/cold split. Same index rule.
inline SplitEntities to_split(const std::vector<EntityAoS>& es) {
    (void)es;
    return {};
}

// TODO 3: the movement loop over SoA. Must give bit-identical results to move_aos.
inline void move_soa(EntitiesSoA& s, float dt) {
    (void)s; (void)dt;
}

// TODO 4: the movement loop over the hot array of the split.
inline void move_split(SplitEntities& s, float dt) {
    (void)s; (void)dt;
}

// TODO 5: the lecture's byte model. stride s, hot bytes h at the start of the struct,
// line size L, all in bytes. AoS: L * ceil(h / L) if s >= L, otherwise s.
inline int bytes_per_entity_aos(int s, int h, int L) {
    (void)s; (void)h; (void)L;
    return 0;
}
inline int bytes_per_entity_soa(int h) {
    (void)h;
    return 0;
}

// TODO 6: a second system. Subtract `amount` from the health of every entity on `team`,
// never going below 0. Return how many of them reached exactly 0 during this call
// (entities already at 0 before the call do not count).
inline int damage_team_soa(EntitiesSoA& s, std::uint32_t team, float amount) {
    (void)s; (void)team; (void)amount;
    return -1;
}
