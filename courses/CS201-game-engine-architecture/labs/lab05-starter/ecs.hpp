// ecs.hpp: CS201 lab 05, a small sparse-set ECS.
// Fill in every function marked TODO. Lecture week 5, sections 1 and 2, has the rules.
#pragma once
#include <cstdint>
#include <vector>

constexpr std::uint32_t NONE = UINT32_MAX;

struct Entity {
    std::uint32_t index = NONE, generation = 0;
    bool operator==(const Entity&) const = default;
};

// Hands out entity handles and recycles indices with a LIFO free list.
class EntityPool {
    std::vector<std::uint32_t> gen_;    // current generation of each index
    std::vector<std::uint32_t> free_;   // destroyed indices, reused last-in first-out
public:
    // TODO 1: reuse the most recently freed index if there is one (with its current
    // generation), otherwise append a new index with generation 0.
    Entity create() { return {}; }

    // TODO 2: if e is alive, bump its slot's generation, push its index on the free
    // list and return true. If e is not alive (stale or never created), do nothing
    // and return false. Destroying twice must not put an index on the free list twice.
    bool destroy(Entity e) { (void)e; return false; }

    // TODO 3: true only if e.index exists and its generation matches.
    bool alive(Entity e) const { (void)e; return false; }

    // Number of live entities.
    std::size_t live_count() const { return gen_.size() - free_.size(); }
};

// All components of type T, packed. Keyed by entity index.
template <class T>
class Pool {
public:
    std::vector<std::uint32_t> sparse;  // entity index -> slot in dense, or NONE
    std::vector<std::uint32_t> dense;   // slot -> entity index
    std::vector<T> data;                // slot -> component

    std::size_t size() const { return dense.size(); }

    // TODO 4: true if entity index e has a component in this pool.
    // Must be safe for any e, including indices beyond sparse.size().
    bool has(std::uint32_t e) const { (void)e; return false; }

    // TODO 5: add a component. Grow sparse on demand (fill with NONE).
    // If e already has one, overwrite the value in place and return false.
    // Otherwise append and return true.
    bool add(std::uint32_t e, const T& value) { (void)e; (void)value; return false; }

    // TODO 6: remove with swap-and-pop. Return false and change nothing if e has none.
    bool remove(std::uint32_t e) { (void)e; return false; }

    // Precondition: has(e).
    T& get(std::uint32_t e) { return data[sparse[e]]; }
};

// TODO 7: call fn(entity_index, a_component, b_component) for every entity that has
// both components. Walk the smaller pool's dense array (ties: walk pool a) and check
// the other pool with has(). Visit entities in the walked pool's dense order.
template <class A, class B, class Fn>
void each2(Pool<A>& a, Pool<B>& b, Fn&& fn) {
    (void)a; (void)b; (void)fn;
}
