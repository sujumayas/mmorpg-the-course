#pragma once
// Resource layer: loads text assets once and keeps them.
#include <map>
#include <string>
#include "core/log.h"
#include "platform/file.h"

inline std::map<std::string, std::string> g_cache;

inline const std::string& resource_text(const std::string& path) {
    auto it = g_cache.find(path);
    if (it == g_cache.end()) {
        core_log("loading resource");
        it = g_cache.emplace(path, platform_read_text(path)).first;
    }
    return it->second;
}
