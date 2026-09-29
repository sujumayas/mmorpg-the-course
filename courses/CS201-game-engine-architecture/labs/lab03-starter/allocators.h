#pragma once
// Lab 03: three allocators. Each takes ONE block from std::malloc in its
// constructor and never touches the global heap again.
//
// Fill in every function marked TODO. The starter versions compile and are
// safe, but return nullptr or 0, so the tests fail.
#include <cstddef>
#include <cstdint>
#include <cstdlib>

// ---------------------------------------------------------------------------
// Part A. Stack allocator (lecture section 3).
class StackAllocator {
public:
    using Marker = std::size_t;

    explicit StackAllocator(std::size_t capacity)
        : base_(static_cast<std::uint8_t*>(std::malloc(capacity))), capacity_(capacity) {}
    ~StackAllocator() { std::free(base_); }
    StackAllocator(const StackAllocator&) = delete;
    StackAllocator& operator=(const StackAllocator&) = delete;

    // Return `bytes` bytes aligned to `align` (a power of two, 1 to 256),
    // or nullptr if they don't fit. A failed call must not change top.
    void* alloc(std::size_t bytes, std::size_t align) {
        (void)bytes; (void)align;
        return nullptr;                                     // TODO
    }

    Marker marker() const { return top_; }
    void free_to(Marker m) { (void)m; }                     // TODO
    void reset() {}                                         // TODO

    std::size_t used() const { return top_; }
    std::size_t capacity() const { return capacity_; }
    std::size_t offset_of(const void* p) const {
        return static_cast<std::size_t>(static_cast<const std::uint8_t*>(p) - base_);
    }

private:
    std::uint8_t* base_;
    std::size_t capacity_;
    std::size_t top_ = 0;
};

// ---------------------------------------------------------------------------
// Part B. Double-ended stack (lecture sections 2 and 3, Quake's hunk).
// Low allocations grow up from offset 0. High allocations grow down from
// capacity. An allocation fails (nullptr, nothing changes) if the two ends
// would overlap.
class DoubleEndedStack {
public:
    using Marker = std::size_t;

    explicit DoubleEndedStack(std::size_t capacity)
        : base_(static_cast<std::uint8_t*>(std::malloc(capacity))), capacity_(capacity) {}
    ~DoubleEndedStack() { std::free(base_); }
    DoubleEndedStack(const DoubleEndedStack&) = delete;
    DoubleEndedStack& operator=(const DoubleEndedStack&) = delete;

    void* alloc_low(std::size_t bytes, std::size_t align) {
        (void)bytes; (void)align;
        return nullptr;                                     // TODO
    }

    // The returned address must be aligned; the block is [p, p + bytes).
    // Round the START down to the alignment.
    void* alloc_high(std::size_t bytes, std::size_t align) {
        (void)bytes; (void)align;
        return nullptr;                                     // TODO
    }

    Marker low_marker() const { return low_; }
    Marker high_marker() const { return high_; }
    void free_to_low(Marker m) { (void)m; }                 // TODO
    void free_to_high(Marker m) { (void)m; }                // TODO

    // Bytes used at each end, counted from that end (high_used() counts
    // down from capacity). largest_free() is the single free run between them.
    std::size_t low_used() const { return low_; }
    std::size_t high_used() const { return high_; }
    std::size_t largest_free() const { return 0; }          // TODO
    std::size_t capacity() const { return capacity_; }
    std::size_t offset_of(const void* p) const {
        return static_cast<std::size_t>(static_cast<const std::uint8_t*>(p) - base_);
    }

private:
    std::uint8_t* base_;
    std::size_t capacity_;
    std::size_t low_ = 0;    // bytes used from the bottom
    std::size_t high_ = 0;   // bytes used from the top
};

// ---------------------------------------------------------------------------
// Part C. Pool allocator (lecture section 4).
// Block size = max(requested size, sizeof(void*)) rounded up to a multiple of
// 16. The free list lives inside the free blocks (no extra memory). The first
// alloc() after construction returns block 0, then block 1, and so on.
// free() pushes onto the front of the list, so the next alloc() reuses it.
class PoolAllocator {
public:
    PoolAllocator(std::size_t block_size, std::size_t count) : count_(count) {
        (void)block_size;                                   // TODO: set block_, allocate, build the free list
    }
    ~PoolAllocator() { std::free(memory_); }
    PoolAllocator(const PoolAllocator&) = delete;
    PoolAllocator& operator=(const PoolAllocator&) = delete;

    void* alloc() { return head_; }                         // TODO (head_ is always nullptr in the starter)
    void free(void* p) { (void)p; }                         // TODO

    std::size_t block_size() const { return block_; }
    std::size_t capacity() const { return count_; }
    std::size_t free_count() const { return free_count_; }
    std::size_t index_of(const void* p) const {
        return static_cast<std::size_t>(static_cast<const std::uint8_t*>(p) - memory_) / block_;
    }

private:
    struct Node { Node* next; };
    std::size_t block_ = 0;
    std::size_t count_;
    std::uint8_t* memory_ = nullptr;
    Node* head_ = nullptr;
    std::size_t free_count_ = 0;
};
