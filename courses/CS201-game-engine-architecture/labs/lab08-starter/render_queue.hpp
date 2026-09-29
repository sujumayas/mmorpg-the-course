// CS201 Lab 08: a sorted render queue.
// Fill in TODO 1 to TODO 5. Each comment states exactly what test_render_queue.cpp expects.
#pragma once
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

enum class Pass : std::uint64_t { Opaque = 0, Translucent = 1, UI = 2 };

struct Draw {
    std::uint32_t id;         // row id from the scene file
    Pass pass;
    std::uint16_t material;   // dense material id (the slot index of its lab 07 handle)
    float depth;              // view-space distance in metres, 0 for UI
};

constexpr float kNear = 0.1f;     // depth range the key can represent
constexpr float kFar = 500.0f;

// TODO 1. Map depth in [kNear, kFar] to an integer in [0, 0xFFFFFF].
// Clamp values outside the range. Use t = (d - kNear) / (kFar - kNear) computed in double,
// and return static_cast<std::uint32_t>(t * 16777215.0 + 0.5).
inline std::uint32_t quantize_depth(float d) {
    (void)d;
    return 0;
}

// TODO 2. Build the lecture's 64-bit key (section 3).
// Bits 62-63: pass. Opaque and UI: material in bits 24-39, depth24 in bits 0-23 (near first).
// Translucent: (0xFFFFFF - depth24) in bits 16-39, material in bits 0-15 (far first).
inline std::uint64_t make_key(Pass pass, std::uint16_t material, std::uint32_t depth24) {
    (void)pass; (void)material; (void)depth24;
    return 0;
}

inline std::uint64_t key_of(const Draw& d) {
    return make_key(d.pass, d.material, quantize_depth(d.depth));
}

// TODO 3. Sort the queue by key, ascending. Ties keep their original relative order
// (use std::stable_sort) so the result is the same on every compiler.
inline void sort_by_key(std::vector<Draw>& q) {
    (void)q;
}

// TODO 4. Count state switches while walking the queue in order: one switch for each
// adjacent pair whose material differs OR whose pass differs (a pass change changes
// blend and depth-write state). An empty or one-element queue has 0 switches.
inline int count_switches(const std::vector<Draw>& q) {
    (void)q;
    return 0;
}

// TODO 5. CPU submit time in microseconds: draws * c_draw + switches * c_switch.
inline double submit_us(int draws, int switches, double c_draw, double c_switch) {
    (void)draws; (void)switches; (void)c_draw; (void)c_switch;
    return 0.0;
}

// Provided: load scene.csv (id,pass,material,depth).
inline std::vector<Draw> load_scene(const std::string& path) {
    std::vector<Draw> q;
    std::ifstream in(path);
    std::string line;
    std::getline(in, line);  // header
    while (std::getline(in, line)) {
        std::stringstream ss(line);
        std::string id, pass, mat, depth;
        std::getline(ss, id, ',');
        std::getline(ss, pass, ',');
        std::getline(ss, mat, ',');
        std::getline(ss, depth, ',');
        Pass p = pass == "opaque" ? Pass::Opaque : pass == "translucent" ? Pass::Translucent : Pass::UI;
        q.push_back({static_cast<std::uint32_t>(std::stoul(id)), p,
                     static_cast<std::uint16_t>(std::stoi(mat)), std::stof(depth)});
    }
    return q;
}
