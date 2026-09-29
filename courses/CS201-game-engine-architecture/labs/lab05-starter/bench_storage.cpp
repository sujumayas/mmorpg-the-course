// bench_storage.cpp: CS201 week 5. Two costs of two ECS storage layouts, measured.
//   1. Toggle a tag component (Stunned) on 1,000 random entities per frame.
//   2. Run a movement system (Position += Velocity * dt) over every entity.
// "Archetype" keeps each entity's components together in a table with one column per
// type, and moves the entity to another table when its component set changes.
// "Sparse set" keeps one packed pool per component type and never moves other components.
// Build: c++ -std=c++20 -O2 bench_storage.cpp -o bench_storage && ./bench_storage
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <numeric>
#include <random>
#include <vector>

using Clock = std::chrono::steady_clock;
constexpr std::uint32_t NONE = UINT32_MAX;
struct Vec3 { float x, y, z; };
struct Other { double health; float sprite[4]; char ai[64]; };  // the rest of a unit: 88 bytes

struct Table {                       // archetype table: one column (array) per component type
    std::vector<Vec3> pos, vel;
    std::vector<Other> other;
    std::vector<std::uint32_t> id;
    void push(const Table& from, std::uint32_t row) {
        pos.push_back(from.pos[row]); vel.push_back(from.vel[row]);
        other.push_back(from.other[row]); id.push_back(from.id[row]);
    }
    void swap_pop(std::uint32_t row) {
        pos[row] = pos.back(); vel[row] = vel.back(); other[row] = other.back(); id[row] = id.back();
        pos.pop_back(); vel.pop_back(); other.pop_back(); id.pop_back();
    }
};

template <class T> struct Pool {     // sparse set
    std::vector<std::uint32_t> sparse, dense;
    std::vector<T> data;
    explicit Pool(std::size_t n) : sparse(n, NONE) {}
    void add(std::uint32_t e, T v) { sparse[e] = dense.size(); dense.push_back(e); data.push_back(v); }
    void remove(std::uint32_t e) {
        std::uint32_t s = sparse[e], last = dense.back();
        dense[s] = last; data[s] = data.back(); sparse[last] = s;
        dense.pop_back(); data.pop_back(); sparse[e] = NONE;
    }
};

double ms_since(Clock::time_point t) { return std::chrono::duration<double, std::milli>(Clock::now() - t).count(); }

int main() {
    const std::uint32_t N = 100'000;
    const int FRAMES = 200, TOGGLES = 1'000;
    const float dt = 1.0f / 60.0f;
    std::mt19937 rng(42);

    // Archetype world: table 0 = {Pos, Vel, Other}, table 1 = {Pos, Vel, Other, Stunned}.
    Table t[2];
    std::vector<std::pair<int, std::uint32_t>> where(N);        // entity -> (table, row)
    for (std::uint32_t e = 0; e < N; ++e) {
        t[0].pos.push_back({0, 0, 0}); t[0].vel.push_back({1, 2, 3});
        t[0].other.push_back({}); t[0].id.push_back(e); where[e] = {0, e};
    }
    // Sparse-set world: Position and Velocity pools filled in different orders,
    // as happens when components are added at different times in a real game.
    Pool<Vec3> pos(N), vel(N);
    Pool<char> stunned(N);
    std::vector<std::uint32_t> order(N);
    std::iota(order.begin(), order.end(), 0);
    for (auto e : order) pos.add(e, {0, 0, 0});
    std::shuffle(order.begin(), order.end(), rng);
    for (auto e : order) vel.add(e, {1, 2, 3});

    std::uniform_int_distribution<std::uint32_t> pick(0, N - 1);
    double toggle_arch = 0, toggle_sparse = 0, move_arch = 1e9, move_sparse = 1e9;
    for (int f = 0; f < FRAMES; ++f) {
        std::vector<std::uint32_t> hit(TOGGLES);
        for (auto& e : hit) e = pick(rng);

        auto t0 = Clock::now();
        for (auto e : hit) {                                    // archetype: move the whole row
            auto [src, row] = where[e];
            int dst = 1 - src;
            t[dst].push(t[src], row);
            where[e] = {dst, std::uint32_t(t[dst].id.size() - 1)};
            std::uint32_t moved = t[src].id.back();
            t[src].swap_pop(row);
            if (moved != e) where[moved] = {src, row};
        }
        toggle_arch += ms_since(t0);

        t0 = Clock::now();
        for (auto e : hit) {                                    // sparse set: touch one pool
            if (stunned.sparse[e] == NONE) stunned.add(e, 1); else stunned.remove(e);
        }
        toggle_sparse += ms_since(t0);

        t0 = Clock::now();
        for (auto& tb : t)                                      // archetype: columns in step
            for (std::size_t i = 0; i < tb.pos.size(); ++i) {
                tb.pos[i].x += tb.vel[i].x * dt; tb.pos[i].y += tb.vel[i].y * dt; tb.pos[i].z += tb.vel[i].z * dt;
            }
        move_arch = std::min(move_arch, ms_since(t0));

        t0 = Clock::now();
        for (std::size_t i = 0; i < vel.dense.size(); ++i) {   // sparse set: walk Velocity,
            Vec3& p = pos.data[pos.sparse[vel.dense[i]]];       // look up Position per entity
            const Vec3& v = vel.data[i];
            p.x += v.x * dt; p.y += v.y * dt; p.z += v.z * dt;
        }
        move_sparse = std::min(move_sparse, ms_since(t0));
    }
    std::printf("toggle Stunned, per toggle: archetype %.1f ns, sparse set %.1f ns\n",
                toggle_arch * 1e6 / (FRAMES * TOGGLES), toggle_sparse * 1e6 / (FRAMES * TOGGLES));
    std::printf("movement over %u entities:  archetype %.3f ms, sparse set %.3f ms\n",
                N, move_arch, move_sparse);
}
