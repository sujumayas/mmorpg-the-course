// Prints switch counts and simulated submit time for three orderings of scene.csv.
// Build: c++ -std=c++17 -O2 analyze.cpp -o analyze && ./analyze [c_draw_us] [c_switch_us]
// Prints nonsense until render_queue.hpp is complete.
#include <cstdio>
#include <cstdlib>
#include <map>
#include <vector>

#include "render_queue.hpp"

static void report(const char* label, const std::vector<Draw>& q, double c_draw, double c_switch) {
    int w = count_switches(q);
    std::printf("%-26s draws %5zu  switches %5d  submit %8.1f us\n", label, q.size(), w,
                submit_us(static_cast<int>(q.size()), w, c_draw, c_switch));
}

int main(int argc, char** argv) {
    double c_draw = argc > 1 ? std::atof(argv[1]) : 2.0;
    double c_switch = argc > 2 ? std::atof(argv[2]) : 10.0;
    std::vector<Draw> scene = load_scene("scene.csv");

    std::map<Pass, std::map<int, int>> per_pass;
    for (const Draw& d : scene) per_pass[d.pass][d.material]++;
    std::printf("opaque materials %zu, translucent materials %zu, UI materials %zu\n\n",
                per_pass[Pass::Opaque].size(), per_pass[Pass::Translucent].size(), per_pass[Pass::UI].size());

    report("file order", scene, c_draw, c_switch);

    std::vector<Draw> by_material = scene;
    std::stable_sort(by_material.begin(), by_material.end(),
                     [](const Draw& a, const Draw& b) { return a.material < b.material; });
    report("material only (WRONG)", by_material, c_draw, c_switch);

    std::vector<Draw> keyed = scene;
    sort_by_key(keyed);
    report("sort key (lecture)", keyed, c_draw, c_switch);

    int translucent_switches = 0;
    for (std::size_t i = 1; i < keyed.size(); ++i)
        if (keyed[i].pass == Pass::Translucent && keyed[i - 1].pass == Pass::Translucent &&
            keyed[i].material != keyed[i - 1].material)
            ++translucent_switches;
    std::printf("\nswitches inside the translucent pass: %d\n", translucent_switches);
}
