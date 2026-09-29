// Lab 03, Part D: new/delete versus pools.
// Build:  c++ -std=c++20 -O2 bench.cpp -o bench && ./bench
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>

#include "allocators.h"

struct Particle { float x, y, vx, vy, life; };        // 20 bytes

static std::uint32_t g_rng = 12345;                   // fixed seed: same run every time
static std::uint32_t next_random() { g_rng = g_rng * 1664525u + 1013904223u; return g_rng >> 8; }

template <class F> double ms_per_frame(int frames, F frame) {
    auto t0 = std::chrono::steady_clock::now();
    for (int f = 0; f < frames; ++f) frame();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count() / frames;
}

// Shuffle indices so objects are freed in random order.
static void shuffle(std::vector<int>& order) {
    for (std::size_t i = order.size(); i > 1; --i) std::swap(order[i - 1], order[next_random() % i]);
}

int main() {
    const int N = 5000, FRAMES = 200;
    std::vector<void*> live(N);
    std::vector<int> order(N);
    for (int i = 0; i < N; ++i) order[i] = i;

    // Case 1 (lecture section 4): one size, freed in allocation order.
    double heap1 = ms_per_frame(FRAMES, [&] {
        for (int i = 0; i < N; ++i) live[i] = new Particle{1, 2, 3, 4, 5};
        for (int i = 0; i < N; ++i) delete static_cast<Particle*>(live[i]);
    });
    PoolAllocator pool(sizeof(Particle), N);
    void* probe = pool.alloc();
    if (probe == nullptr) {
        std::printf("PoolAllocator is not implemented yet: finish Part C first.\n");
        return 1;
    }
    pool.free(probe);
    double pool1 = ms_per_frame(FRAMES, [&] {
        for (int i = 0; i < N; ++i) live[i] = new (pool.alloc()) Particle{1, 2, 3, 4, 5};
        for (int i = 0; i < N; ++i) pool.free(live[i]);
    });

    // Case 2: sizes 16..256 bytes, freed in random order.
    std::vector<std::size_t> sizes(N);
    for (int i = 0; i < N; ++i) sizes[i] = 16u << (next_random() % 5);   // 16, 32, 64, 128, 256
    double heap2 = ms_per_frame(FRAMES, [&] {
        for (int i = 0; i < N; ++i) live[i] = ::operator new(sizes[i]);
        shuffle(order);
        for (int i = 0; i < N; ++i) ::operator delete(live[order[i]]);
    });
    // TODO (Part D): make one PoolAllocator per size class and time the same
    // work as heap2 with them. Include the shuffle in the timed region, as above.
    double pool2 = -1.0;

    std::printf("case 1, one size, in order:     new/delete %.3f ms, pool %.3f ms per frame\n", heap1, pool1);
    std::printf("case 2, five sizes, random order: new/delete %.3f ms, pools %.3f ms per frame\n", heap2, pool2);
    return 0;
}
