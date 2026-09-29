// Lab 02 tests. Build and run with:  python run_tests.py
// (or by hand: c++ -std=c++20 -Wall -Wextra -g -fsanitize=address,undefined test_lab02.cpp -o test_lab02 && ./test_lab02)
#include <cstdio>
#include <type_traits>
#include <utility>
#include <vector>

#include "gpu_texture.h"
#include "pixel_buffer.h"

static int g_failures = 0;
static int g_checks_in_test = 0;
static bool g_test_ok = true;

#define CHECK(cond)                                                          \
    do {                                                                     \
        ++g_checks_in_test;                                                  \
        if (!(cond)) {                                                       \
            g_test_ok = false;                                               \
            std::printf("      line %d: CHECK(%s) failed\n", __LINE__, #cond); \
        }                                                                    \
    } while (0)

template <class F>
void run(const char* name, F test) {
    g_test_ok = true;
    g_checks_in_test = 0;
    g_stats = BufferStats{};
    g_gpu = GpuStats{};
    g_live_ids.clear();
    test();
    std::printf("%s  %s\n", g_test_ok ? "PASS" : "FAIL", name);
    if (!g_test_ok) ++g_failures;
}

static void fill(PixelBuffer& b, std::uint8_t start) {
    for (std::size_t i = 0; i < b.size(); ++i) b.data()[i] = static_cast<std::uint8_t>(start + i);
}

static bool same_bytes(const PixelBuffer& a, const PixelBuffer& b) {
    if (a.size() != b.size()) return false;
    for (std::size_t i = 0; i < a.size(); ++i)
        if (a.data()[i] != b.data()[i]) return false;
    return true;
}

int main() {
    std::setvbuf(stdout, nullptr, _IONBF, 0);   // show each result as it happens
    run("A1 constructor allocates once, zero-filled", [] {
        PixelBuffer b(100);
        CHECK(b.size() == 100);
        CHECK(b.data() != nullptr);
        CHECK(b.data()[0] == 0 && b.data()[99] == 0);
        CHECK(g_stats.allocations == 1);
    });

    run("A2 copy constructor makes an independent deep copy", [] {
        PixelBuffer a(100);
        fill(a, 7);
        PixelBuffer b(a);
        CHECK(same_bytes(a, b));
        CHECK(a.data() != b.data());
        b.data()[0] = 200;
        CHECK(a.data()[0] == 7);
        CHECK(g_stats.bytes_copied == 100);
    });

    run("A3 copy assignment replaces contents and frees the old block", [] {
        {
            PixelBuffer a(64), b(32);
            fill(a, 1);
            b = a;
            CHECK(b.size() == 64);
            CHECK(same_bytes(a, b));
            CHECK(a.data() != b.data());
            PixelBuffer& same = b;
            b = same;                           // self-assignment
            CHECK(same_bytes(a, b));
        }
        CHECK(g_stats.allocations == g_stats.frees);
    });

    run("A4 move constructor steals without allocating", [] {
        PixelBuffer a(100);
        fill(a, 3);
        const std::uint8_t* old = a.data();
        long long before = g_stats.allocations;
        PixelBuffer b(std::move(a));
        CHECK(g_stats.allocations == before);
        CHECK(b.data() == old);
        CHECK(b.size() == 100 && b.data()[1] == 4);
        CHECK(a.data() == nullptr && a.size() == 0);   // NOLINT: testing moved-from state
        CHECK(g_stats.bytes_copied == 0);
    });

    run("A5 move assignment frees the old block and steals", [] {
        {
            PixelBuffer a(100), b(50);
            fill(a, 9);
            const std::uint8_t* old = a.data();
            long long before = g_stats.allocations;
            b = std::move(a);
            CHECK(g_stats.allocations == before);
            CHECK(b.data() == old && b.size() == 100);
            CHECK(a.data() == nullptr && a.size() == 0);   // NOLINT
            CHECK(g_stats.frees == 1);                     // b's 50-byte block
        }
        CHECK(g_stats.allocations == g_stats.frees);
    });

    run("A6 move operations are noexcept", [] {
        CHECK(std::is_nothrow_move_constructible_v<PixelBuffer>);
        CHECK(std::is_nothrow_move_assignable_v<PixelBuffer>);
    });

    run("A7 a growing vector never deep-copies a PixelBuffer", [] {
        {
            std::vector<PixelBuffer> v;
            for (int i = 0; i < 1000; ++i) v.emplace_back(64);
            CHECK(g_stats.bytes_copied == 0);
            CHECK(g_stats.allocations == 1000);
        }
        CHECK(g_stats.allocations == g_stats.frees);
    });

    run("B1 GpuTexture cannot be copied", [] {
        CHECK(!std::is_copy_constructible_v<GpuTexture>);
        CHECK(!std::is_copy_assignable_v<GpuTexture>);
    });

    run("B2 GpuTexture moves are noexcept and transfer ownership", [] {
        CHECK(std::is_nothrow_move_constructible_v<GpuTexture>);
        CHECK(std::is_nothrow_move_assignable_v<GpuTexture>);
        {
            GpuTexture a(128, 128);
            int id = a.id();
            GpuTexture b(std::move(a));
            CHECK(b.id() == id);
            CHECK(a.id() == 0);                 // NOLINT
            CHECK(g_live_ids.size() == 1);
        }
        CHECK(g_gpu.created == 1 && g_gpu.destroyed == 1 && g_gpu.errors == 0);
    });

    run("B3 move assignment releases the texture it held", [] {
        {
            GpuTexture a(64, 64), b(32, 32);
            int old_b = b.id();
            b = std::move(a);
            CHECK(g_live_ids.count(old_b) == 0);
            CHECK(g_live_ids.size() == 1);
        }
        CHECK(g_gpu.destroyed == 2 && g_gpu.errors == 0);
    });

    run("B4 a vector of 100 textures grows, then frees all of them once", [] {
        {
            std::vector<GpuTexture> v;
            for (int i = 0; i < 100; ++i) v.emplace_back(16, 16);
            CHECK(g_live_ids.size() == 100);
        }
        CHECK(g_live_ids.empty());
        CHECK(g_gpu.created == 100 && g_gpu.destroyed == 100 && g_gpu.errors == 0);
    });

    std::printf("%d test(s) failed\n", g_failures);
    return g_failures == 0 ? 0 : 1;
}
