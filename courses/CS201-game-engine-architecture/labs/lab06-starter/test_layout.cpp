// test_layout.cpp: checks for lab 06. Build and run:
//   c++ -std=c++20 -O2 test_layout.cpp -o test_layout && ./test_layout
#include <cstdio>
#include <cstring>
#include "layout.hpp"

static int failures = 0;
static void check(bool ok, const char* name) {
    std::printf("%s  %s\n", ok ? "PASS" : "FAIL", name);
    if (!ok) ++failures;
}

static std::vector<EntityAoS> make(int n) {
    std::vector<EntityAoS> es(n);
    for (int i = 0; i < n; ++i) {
        es[i] = {};
        es[i].px = float(i); es[i].py = float(-i); es[i].pz = 0.5f * i;
        es[i].vx = 1.0f + i % 7; es[i].vy = 2.0f - i % 5; es[i].vz = 0.25f * (i % 3);
        es[i].health = float(10 + i % 20); es[i].team = std::uint32_t(i % 3);
        std::snprintf(es[i].name, sizeof es[i].name, "unit%d", i);
    }
    return es;
}

int main() {
    const int N = 1000;
    const float dt = 1.0f / 60.0f;
    auto aos = make(N);
    auto soa = to_soa(aos);
    auto split = to_split(aos);

    bool ok1 = soa.size() == N && soa.vz.size() == N && soa.health.size() == N && soa.team.size() == N &&
               soa.px[7] == 7.0f && soa.vy[12] == aos[12].vy && soa.team[5] == 2 && soa.health[25] == 15.0f;
    check(ok1, "1 to_soa keeps entity i at index i in every array");
    bool ok2 = split.hot.size() == N && split.cold.size() == N && split.hot[9].vx == aos[9].vx &&
               std::strcmp(split.cold[42].name, "unit42") == 0 && split.cold[3].team == 0;
    check(ok2, "2 to_split copies hot and cold fields");

    for (int r = 0; r < 10; ++r) { move_aos(aos, dt); move_soa(soa, dt); move_split(split, dt); }
    bool same3 = soa.size() == N, same4 = split.hot.size() == N;
    for (int i = 0; i < N && same3; ++i)
        same3 = soa.px[i] == aos[i].px && soa.py[i] == aos[i].py && soa.pz[i] == aos[i].pz;
    for (int i = 0; i < N && same4; ++i)
        same4 = split.hot[i].px == aos[i].px && split.hot[i].py == aos[i].py && split.hot[i].pz == aos[i].pz;
    check(same3 && soa.px[1] != 1.0f, "3 move_soa matches move_aos exactly");
    check(same4 && N > 1 && split.hot[1].px != 1.0f, "4 move_split matches move_aos exactly");

    check(bytes_per_entity_aos(128, 24, 128) == 128 && bytes_per_entity_aos(128, 24, 64) == 64 &&
          bytes_per_entity_aos(96, 16, 64) == 64 && bytes_per_entity_aos(48, 16, 64) == 48 &&
          bytes_per_entity_aos(256, 200, 64) == 256 && bytes_per_entity_soa(24) == 24,
          "5 byte model matches the lecture table");

    EntitiesSoA t;
    t.px = t.py = t.pz = t.vx = t.vy = t.vz = {0, 0, 0, 0, 0};
    t.health = {5, 12, 3, 0, 8};
    t.team = {1, 1, 2, 1, 1};
    int dead = damage_team_soa(t, 1, 8.0f);
    check(dead == 2 && t.health[0] == 0 && t.health[1] == 4 && t.health[2] == 3 && t.health[3] == 0 &&
          t.health[4] == 0, "6 damage_team_soa clamps and counts new zeros");

    std::printf("\n%d check(s) failed\n", failures);
    return failures == 0 ? 0 : 1;
}
