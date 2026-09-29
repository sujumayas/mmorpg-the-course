// test_ecs.cpp: checks for lab 05. Build and run:
//   c++ -std=c++20 -O2 test_ecs.cpp -o test_ecs && ./test_ecs
#include <cstdio>
#include <string>
#include "ecs.hpp"

static int failures = 0;
static void check(bool ok, const char* name) {
    std::printf("%s  %s\n", ok ? "PASS" : "FAIL", name);
    if (!ok) ++failures;
}
template <class T> static std::string arr(const std::vector<T>& v) {
    std::string s;
    for (auto x : v) s += (x == NONE ? std::string("-") : std::to_string(x)) + " ";
    return s;
}

struct Pos { float x, y; };
struct Vel { float x, y; };
struct Stunned {};

int main() {
    {   // 1 to 3: handles
        EntityPool p;
        Entity e0 = p.create(), e1 = p.create(), e2 = p.create();
        check(e0 == Entity{0, 0} && e1 == Entity{1, 0} && e2 == Entity{2, 0} && p.alive(e1),
              "1 create hands out fresh indices with generation 0");
        bool d1 = p.destroy(e1), d2 = p.destroy(e1);
        check(d1 && !d2 && !p.alive(e1) && p.live_count() == 2, "2 destroy kills once, stale destroy is refused");
        p.destroy(e0);
        Entity a = p.create(), b = p.create(), c = p.create();
        check(a == Entity{0, 1} && b == Entity{1, 1} && c == Entity{3, 0} && !p.alive(Entity{0, 0}) &&
              !p.alive(Entity{9, 0}), "3 LIFO reuse with bumped generation; unknown index is dead");
    }
    {   // 4 to 6: the lecture trace
        Pool<Stunned> h;                        // built by hand so check 4 needs only has()
        h.sparse = {NONE, 0}; h.dense = {1}; h.data = {Stunned{}};
        check(h.has(1) && !h.has(0) && !h.has(2) && !h.has(1000), "4 has, including out-of-range index");
        Pool<Stunned> s;
        bool ok = s.add(1, {}) && s.add(3, {}) && s.add(4, {});
        check(ok && arr(s.dense) == "1 3 4 " && arr(s.sparse) == "- 0 - 1 2 " && s.has(3) && !s.has(2),
              "5 add grows sparse on demand");
        bool r = s.remove(1), r2 = s.remove(1);
        check(r && !r2 && arr(s.dense) == "4 3 " && arr(s.sparse) == "- - - 1 0 " && s.size() == 2,
              "6 remove is swap-and-pop, missing remove refused");
    }
    {   // 5b and 6b: values follow their entities
        Pool<Pos> p;
        p.add(0, {1, 1}); p.add(1, {2, 2}); p.add(2, {3, 3});
        bool dup = p.add(1, {9, 9});
        p.remove(0);
        check(!dup && p.size() == 2 && p.get(1).x == 9 && p.get(2).x == 3 && p.dense[0] == 2,
              "5b duplicate add overwrites; data moves with dense");
        p.remove(2);
        check(p.size() == 1 && p.get(1).x == 9 && !p.has(2), "6b removing the last element");
    }
    {   // 7: join
        Pool<Pos> pos; Pool<Vel> vel;
        for (std::uint32_t e : {0u, 1u, 2u, 3u, 4u, 5u}) pos.add(e, {0, 0});
        for (std::uint32_t e : {5u, 2u, 9u}) vel.add(e, {float(e), 1});
        std::string seen;
        int calls = 0;
        each2(pos, vel, [&](std::uint32_t e, Pos& p, Vel& v) { p.x += v.x; seen += std::to_string(e) + " "; ++calls; });
        check(calls == 2 && seen == "5 2 " && pos.get(5).x == 5 && pos.get(2).x == 2 && pos.get(0).x == 0,
              "7 each2 walks the smaller pool and skips non-matches");
    }
    std::printf("\n%d check(s) failed\n", failures);
    return failures == 0 ? 0 : 1;
}
