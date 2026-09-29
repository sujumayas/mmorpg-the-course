#pragma once
// Lab 02, part A: a class that owns a block of heap memory.
//
// The constructor and destructor are done. Write the four TODO functions so
// that PixelBuffer follows the rule of five:
//   - copying makes an independent deep copy (and adds to g_stats.bytes_copied),
//   - moving steals the block, leaves the source empty (data() == nullptr,
//     size() == 0) and allocates nothing,
//   - both move operations are noexcept,
//   - no path leaks or frees twice, including self-assignment.
// Always allocate with allocate_bytes() and free with free_bytes() so the
// tests can count.
#include <cstddef>
#include <cstdint>
#include <cstring>

struct BufferStats {
    long long allocations = 0;
    long long frees = 0;
    long long bytes_copied = 0;
};
inline BufferStats g_stats;

inline std::uint8_t* allocate_bytes(std::size_t n) {
    ++g_stats.allocations;
    return new std::uint8_t[n]();          // zero-filled
}

inline void free_bytes(std::uint8_t* p) {
    if (p != nullptr) {
        ++g_stats.frees;
        delete[] p;
    }
}

class PixelBuffer {
public:
    explicit PixelBuffer(std::size_t size) : data_(allocate_bytes(size)), size_(size) {}
    ~PixelBuffer() { free_bytes(data_); }

    // TODO: deep copy. Allocate size bytes, copy them, add size to bytes_copied.
    PixelBuffer(const PixelBuffer& other)
        : data_(allocate_bytes(other.size_)), size_(other.size_) {
        // (starter forgets to copy the bytes)
    }

    // TODO: deep copy assignment. Must survive a = a.
    PixelBuffer& operator=(const PixelBuffer& other) {
        (void)other;                       // (starter does nothing)
        return *this;
    }

    // TODO: steal other's block. No allocation. Must be noexcept.
    PixelBuffer(PixelBuffer&& other)
        : data_(allocate_bytes(other.size_)), size_(other.size_) {
        // (starter copies instead of moving)
        std::memcpy(data_, other.data_, size_);
        g_stats.bytes_copied += static_cast<long long>(size_);
    }

    // TODO: free our block, steal other's. No allocation. Must be noexcept.
    PixelBuffer& operator=(PixelBuffer&& other) {
        (void)other;                       // (starter does nothing)
        return *this;
    }

    std::uint8_t* data() { return data_; }
    const std::uint8_t* data() const { return data_; }
    std::size_t size() const { return size_; }

private:
    std::uint8_t* data_;
    std::size_t size_;
};
