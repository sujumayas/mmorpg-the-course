#pragma once
// Lab 02, part B: a move-only handle to a (pretend) GPU texture.
//
// The fake GPU API below counts live textures and records every mistake:
// destroying an id twice, or an id that was never created.
//
// Make GpuTexture:
//   - not copyable (delete both copy operations),
//   - movable with noexcept move constructor and move assignment,
//   - the single owner of its id: the destructor destroys it exactly once,
//     a moved-from GpuTexture holds id 0 and destroys nothing,
//   - move assignment destroys the texture it held before taking the new one.
#include <set>

struct GpuStats {
    int created = 0;
    int destroyed = 0;
    int errors = 0;          // double destroy or unknown id
};
inline GpuStats g_gpu;
inline std::set<int> g_live_ids;
inline int g_next_id = 1;

inline int gpu_create_texture(int w, int h) {
    (void)w; (void)h;
    int id = g_next_id++;
    g_live_ids.insert(id);
    ++g_gpu.created;
    return id;
}

inline void gpu_destroy_texture(int id) {
    if (g_live_ids.erase(id) == 1) {
        ++g_gpu.destroyed;
    } else {
        ++g_gpu.errors;
    }
}

class GpuTexture {
public:
    GpuTexture(int w, int h) : id_(gpu_create_texture(w, h)) {}
    ~GpuTexture() { if (id_ != 0) gpu_destroy_texture(id_); }

    // TODO: delete the copy operations and write noexcept move operations.

    int id() const { return id_; }

private:
    int id_;
};
