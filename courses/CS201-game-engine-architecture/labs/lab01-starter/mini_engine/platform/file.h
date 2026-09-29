#pragma once
// Platform layer: file access. OS headers are allowed here.
#include <cstdio>
#include <string>
#include <unistd.h>

inline bool platform_file_readable(const std::string& path) {
    return access(path.c_str(), R_OK) == 0;
}

inline std::string platform_read_text(const std::string& path) {
    std::string out;
    if (FILE* f = std::fopen(path.c_str(), "rb")) {
        char buf[256];
        std::size_t n;
        while ((n = std::fread(buf, 1, sizeof buf, f)) > 0) out.append(buf, n);
        std::fclose(f);
    }
    return out;
}
