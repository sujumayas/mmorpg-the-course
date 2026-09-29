// Lab 03 tests. Build and run with:  python run_tests.py
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <set>

#include "allocators.h"

// Count every use of the global heap through operator new.
static long long g_global_news = 0;
void* operator new(std::size_t n) {
    ++g_global_news;
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

static int g_failures = 0;
static bool g_ok = true;

#define CHECK(cond)                                                          \
    do {                                                                     \
        if (!(cond)) {                                                       \
            g_ok = false;                                                    \
            std::printf("      line %d: CHECK(%s) failed\n", __LINE__, #cond); \
        }                                                                    \
    } while (0)

template <class F>
void run(const char* name, F test) {
    g_ok = true;
    test();
    std::printf("%s  %s\n", g_ok ? "PASS" : "FAIL", name);
    if (!g_ok) ++g_failures;
}

static bool aligned(const void* p, std::size_t a) {
    return p != nullptr && reinterpret_cast<std::uintptr_t>(p) % a == 0;
}

int main() {
    std::setvbuf(stdout, nullptr, _IONBF, 0);

    run("A1 stack: the lecture's five requests land at 0, 16, 32, 96, 100", [] {
        StackAllocator s(1024);
        std::size_t want[] = {0, 16, 32, 96, 100};
        std::size_t bytes[] = {13, 8, 64, 3, 4}, align[] = {4, 8, 16, 1, 4};
        for (int i = 0; i < 5; ++i) {
            void* p = s.alloc(bytes[i], align[i]);
            CHECK(p != nullptr);
            if (p) CHECK(s.offset_of(p) == want[i]);
        }
        CHECK(s.used() == 104);
    });

    run("A2 stack: every pointer honors its alignment (1 to 256)", [] {
        StackAllocator s(8192);
        for (std::size_t a = 1; a <= 256; a *= 2) {
            CHECK(aligned(s.alloc(3, a), a));
            CHECK(aligned(s.alloc(1, a), a));
        }
    });

    run("A3 stack: a request that does not fit returns nullptr and changes nothing", [] {
        StackAllocator s(100);
        CHECK(s.alloc(60, 1) != nullptr);
        std::size_t before = s.used();
        CHECK(s.alloc(41, 1) == nullptr);
        CHECK(s.used() == before);
        CHECK(s.alloc(40, 1) != nullptr);
        CHECK(s.used() == 100);
    });

    run("A4 stack: free_to(marker) and reset() roll back", [] {
        StackAllocator s(1024);
        s.alloc(10, 1);
        StackAllocator::Marker m = s.marker();
        void* first = s.alloc(100, 16);
        s.alloc(200, 16);
        s.free_to(m);
        CHECK(s.used() == 10);
        CHECK(s.alloc(100, 16) == first);
        s.reset();
        CHECK(s.used() == 0);
    });

    run("B1 double-ended: low grows up, high grows down, both aligned", [] {
        DoubleEndedStack d(1024);
        void* h1 = d.alloc_high(10, 8);
        CHECK(h1 != nullptr);
        if (h1) CHECK(d.offset_of(h1) == 1008);
        CHECK(d.high_used() == 16);
        void* h2 = d.alloc_high(8, 16);
        CHECK(h2 != nullptr);
        if (h2) CHECK(d.offset_of(h2) == 992);
        CHECK(d.high_used() == 32);
        void* l1 = d.alloc_low(100, 4);
        CHECK(l1 != nullptr);
        if (l1) CHECK(d.offset_of(l1) == 0);
        CHECK(d.low_used() == 100);
        CHECK(d.largest_free() == 892);
        CHECK(aligned(d.alloc_high(1, 64), 64));
    });

    run("B2 double-ended: the ends may meet but never cross", [] {
        DoubleEndedStack d(256);
        CHECK(d.alloc_low(100, 1) != nullptr);
        CHECK(d.alloc_high(100, 1) != nullptr);
        CHECK(d.largest_free() == 56);
        CHECK(d.alloc_low(57, 1) == nullptr);
        CHECK(d.alloc_high(57, 1) == nullptr);
        CHECK(d.low_used() == 100 && d.high_used() == 100);
        CHECK(d.alloc_low(56, 1) != nullptr);
        CHECK(d.largest_free() == 0);
        CHECK(d.alloc_high(1, 1) == nullptr);
    });

    run("B3 double-ended: markers free each end independently", [] {
        DoubleEndedStack d(1024);
        d.alloc_low(64, 16);
        DoubleEndedStack::Marker lm = d.low_marker();
        DoubleEndedStack::Marker hm = d.high_marker();
        d.alloc_low(300, 16);
        d.alloc_high(300, 16);
        d.free_to_low(lm);
        CHECK(d.low_used() == 64);
        CHECK(d.high_used() >= 300);
        d.free_to_high(hm);
        CHECK(d.high_used() == 0);
        CHECK(d.largest_free() == 1024 - 64);
    });

    run("C1 pool: block size is max(size, pointer) rounded up to 16", [] {
        CHECK(PoolAllocator(20, 4).block_size() == 32);
        CHECK(PoolAllocator(1, 4).block_size() == 16);
        CHECK(PoolAllocator(44, 4).block_size() == 48);
        CHECK(PoolAllocator(64, 4).block_size() == 64);
    });

    run("C2 pool: hands out blocks 0, 1, 2, ... then nullptr when empty", [] {
        PoolAllocator p(20, 4);
        CHECK(p.free_count() == 4);
        for (std::size_t i = 0; i < 4; ++i) {
            void* b = p.alloc();
            CHECK(b != nullptr);
            if (b) {
                CHECK(p.index_of(b) == i);
                CHECK(aligned(b, 16));
            }
        }
        CHECK(p.alloc() == nullptr);
        CHECK(p.free_count() == 0);
    });

    run("C3 pool: the last block freed is the next one handed out", [] {
        PoolAllocator p(20, 4);
        void* a = p.alloc();
        void* b = p.alloc();
        void* c = p.alloc();
        p.free(b);
        p.free(a);
        CHECK(p.free_count() == 3);
        CHECK(a != nullptr && p.alloc() == a);
        CHECK(b != nullptr && p.alloc() == b);
        (void)c;
    });

    run("C4 pool: 1,000 blocks are distinct and survive writes to neighbors", [] {
        PoolAllocator p(24, 1000);
        std::set<void*> seen;
        void* blocks[1000];
        for (int i = 0; i < 1000; ++i) {
            blocks[i] = p.alloc();
            if (!blocks[i]) break;
            seen.insert(blocks[i]);
            static_cast<std::uint8_t*>(blocks[i])[0] = static_cast<std::uint8_t>(i);
            static_cast<std::uint8_t*>(blocks[i])[23] = static_cast<std::uint8_t>(i);
        }
        CHECK(seen.size() == 1000);
        bool intact = true;
        for (int i = 0; i < 1000 && blocks[i]; ++i)
            intact = intact && static_cast<std::uint8_t*>(blocks[i])[0] == static_cast<std::uint8_t>(i);
        CHECK(intact);
    });

    run("G1 no allocator touches the global heap after construction", [] {
        StackAllocator s(1 << 16);
        DoubleEndedStack d(1 << 16);
        PoolAllocator p(32, 256);
        long long before = g_global_news;
        for (int frame = 0; frame < 100; ++frame) {
            void* live[256];
            for (int i = 0; i < 256; ++i) live[i] = p.alloc();
            for (int i = 0; i < 256; ++i) if (live[i]) p.free(live[i]);
            for (int i = 0; i < 50; ++i) s.alloc(40, 8);
            s.reset();
            DoubleEndedStack::Marker m = d.low_marker();
            d.alloc_low(1000, 16);
            d.free_to_low(m);
        }
        CHECK(g_global_news == before);
        CHECK(p.free_count() == 256);
    });

    std::printf("%d test(s) failed\n", g_failures);
    return g_failures == 0 ? 0 : 1;
}
