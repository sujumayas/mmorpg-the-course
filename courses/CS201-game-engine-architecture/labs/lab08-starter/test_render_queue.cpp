// Checks for CS201 Lab 08.
// Build and run from this folder:
//   c++ -std=c++17 -O2 test_render_queue.cpp -o test_render_queue && ./test_render_queue
// Exits with 0 only when every check passes.
#include <cmath>
#include <cstdio>
#include <string>
#include <vector>

#include "render_queue.hpp"

static int failures = 0;
static void check(bool ok, const char* name, const std::string& why = "") {
    std::printf("%s  %s%s%s\n", ok ? "PASS" : "FAIL", name, ok ? "" : "  -> ", ok ? "" : why.c_str());
    if (!ok) ++failures;
}

static std::vector<std::uint32_t> ids(const std::vector<Draw>& q) {
    std::vector<std::uint32_t> out;
    for (const Draw& d : q) out.push_back(d.id);
    return out;
}

int main() {
    // 1. depth quantization
    check(quantize_depth(kNear) == 0 && quantize_depth(0.0f) == 0, "1 quantize: near and below map to 0");
    check(quantize_depth(kFar) == 0xFFFFFF && quantize_depth(9999.0f) == 0xFFFFFF, "1b quantize: far and beyond map to 0xFFFFFF");
    check(quantize_depth(250.05f) == 8388608, "1c quantize: midpoint maps to 8388608",
          "got " + std::to_string(quantize_depth(250.05f)));

    // 2. key layout, values from lecture section 3
    check(make_key(Pass::Opaque, 2, 500) == 0x00000000020001f4ULL, "2 key: opaque material 2 depth 500");
    check(make_key(Pass::Translucent, 5, 800) == 0x400000fffcdf0005ULL, "2b key: translucent material 5 depth 800");
    check(make_key(Pass::UI, 1, 0) == 0x8000000001000000ULL, "2c key: UI material 1");
    check(make_key(Pass::Translucent, 9, 0) == 0x400000FFFFFF0009ULL, "2d key: translucent nearest, material 9");

    // 3. sorting the lecture's six draws
    std::vector<Draw> six = {
        {0, Pass::Translucent, 3, 10.0f}, {1, Pass::Opaque, 7, 90.0f}, {2, Pass::UI, 1, 0.0f},
        {3, Pass::Opaque, 2, 50.0f},      {4, Pass::Opaque, 7, 20.0f}, {5, Pass::Translucent, 5, 80.0f},
    };
    sort_by_key(six);
    check(ids(six) == std::vector<std::uint32_t>{3, 4, 1, 5, 0, 2}, "3 sort: tree, rock 2, rock 1, smoke, glass, UI");

    // 4. switch counting
    std::vector<Draw> s = {
        {0, Pass::Opaque, 1, 1}, {1, Pass::Opaque, 1, 2}, {2, Pass::Opaque, 2, 3},
        {3, Pass::Opaque, 2, 4}, {4, Pass::Opaque, 1, 5}, {5, Pass::Translucent, 1, 6},
    };
    check(count_switches(s) == 3, "4 switches: material changes twice, pass changes once",
          "got " + std::to_string(count_switches(s)));
    check(count_switches({}) == 0 && count_switches({s[0]}) == 0, "4b switches: empty and single queue");

    // 5. submit time
    check(std::fabs(submit_us(2000, 1950, 2.0, 10.0) - 23500.0) < 1e-9, "5 submit: lecture's shuffled city is 23,500 us");

    // 6. the recorded scene
    std::vector<Draw> scene = load_scene("scene.csv");
    check(scene.size() == 1800, "6 scene: 1,800 draws loaded", "is scene.csv in this folder?");
    int file_order = count_switches(scene);
    sort_by_key(scene);
    int keyed = count_switches(scene);
    check(file_order > 1500 && keyed < 400, "6b scene: sorting cuts switches from >1,500 to <400",
          std::to_string(file_order) + " -> " + std::to_string(keyed));
    bool passes_ordered = true, translucent_far_first = true;
    int translucent_pairs = 0;
    for (std::size_t i = 1; i < scene.size(); ++i) {
        if (scene[i].pass < scene[i - 1].pass) passes_ordered = false;
        if (scene[i].pass == Pass::Translucent && scene[i - 1].pass == Pass::Translucent) {
            ++translucent_pairs;
            if (quantize_depth(scene[i].depth) > quantize_depth(scene[i - 1].depth)) translucent_far_first = false;
        }
    }
    translucent_far_first = translucent_far_first && translucent_pairs == 319;
    check(passes_ordered && !scene.empty() && scene.back().pass == Pass::UI, "6c scene: opaque, then translucent, then UI");
    check(translucent_far_first, "6d scene: translucent draws are far to near");

    std::printf("\n%s\n", failures ? "Some checks fail." : "All checks pass.");
    return failures ? 1 : 0;
}
