"""Lab 01: a layer checker for C++ source trees.

Fill in the six functions marked TODO. Each docstring says exactly what
check_lab01.py expects. Standard library only, Python 3.10 or later.

Run the checks:      python check_lab01.py
Run the tool:        python layercheck.py mini_engine layers.json
"""
import json
import re
import sys
from pathlib import Path


class CycleError(Exception):
    """Raised by start_order when the dependencies contain a cycle.

    `members` is the sorted list of every module that is part of a cycle
    or waits on one (everything that could not be ordered).
    """

    def __init__(self, members):
        super().__init__(f"dependency cycle among: {', '.join(members)}")
        self.members = members


def parse_includes(text):
    """Return the #include directives in `text`, in order, as (name, is_system).

    - `#include "core/log.h"` gives ("core/log.h", False).
    - `#include <unistd.h>` gives ("unistd.h", True).
    - Allow spaces after '#' and before 'include' ("#  include <x>").
    - Ignore lines whose first non-space characters are '//' (commented out).
    - Ignore anything after the closing quote or '>' (trailing comments).
    """
    raise NotImplementedError  # TODO


def layer_of(relpath, layers):
    """Return the layer number of a file, given its path relative to the root.

    `relpath` uses forward slashes, for example "core/log.h" or "main.cpp".
    Look up the first path component ("core") in `layers`. A file at the
    root ("main.cpp") is looked up by its full name. Raise KeyError if the
    name is not in `layers`.
    """
    raise NotImplementedError  # TODO


def scan(root):
    """Scan every .h and .cpp file under `root` (recursively).

    Return a dict keyed by path relative to root with forward slashes:
        {"core/log.h": {"lines": 9, "includes": [("cstdio", True), ...]}, ...}
    "lines" is the number of lines in the file (the count `wc -l` would give
    for a file that ends with a newline).
    """
    raise NotImplementedError  # TODO


def upward(files, layers):
    """Return every upward dependency as a sorted list of (src, dst) pairs.

    Only quoted includes that name a file present in `files` count.
    A dependency is upward when layer_of(src) < layer_of(dst).
    """
    raise NotImplementedError  # TODO


def os_leaks(files, layers, platform_layer, os_headers):
    """Return the sorted list of files OUTSIDE the platform layer that include
    an OS header.

    A system include is an OS header when its name starts with any string in
    `os_headers` ("sys/" matches "sys/stat.h"). `platform_layer` is the name
    of the platform folder, for example "platform".
    """
    raise NotImplementedError  # TODO


def start_order(deps):
    """Return a start-up order for `deps`, a dict {module: [modules it needs]}.

    Every module that appears as a key or inside a list must be in the result,
    after everything it needs. When several modules are ready at once, take
    them in alphabetical order, so the answer is unique.
    If no order exists, raise CycleError(sorted list of modules that could
    not be placed).
    """
    raise NotImplementedError  # TODO


# ---------------------------------------------------------------------------
# Provided: the report. It works once the functions above do.

def port_share(files, layers, platform_layer, os_headers):
    """Return (port_lines, total_lines) for the port-size model."""
    total = sum(f["lines"] for f in files.values())
    size = sum(f["lines"] for path, f in files.items()
                  if path.split("/")[0] == platform_layer)
    size += sum(files[p]["lines"] for p in os_leaks(files, layers, platform_layer, os_headers))
    return size, total


def report(root, config_path):
    config = json.loads(Path(config_path).read_text())
    layers, plat, osh = config["layers"], config["platform_layer"], config["os_headers"]
    files = scan(root)
    ups = upward(files, layers)
    leaks = os_leaks(files, layers, plat, osh)
    size, total = port_share(files, layers, plat, osh)
    print(f"{len(files)} files, {total} lines")
    print(f"upward dependencies: {len(ups)}")
    for src, dst in ups:
        print(f"  {src} (layer {layer_of(src, layers)}) -> {dst} (layer {layer_of(dst, layers)})")
    print(f"OS leaks: {len(leaks)}")
    for p in leaks:
        print(f"  {p}")
    print(f"port size: {size} of {total} lines = {size / total:.1%}")
    return len(ups) + len(leaks)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python layercheck.py <source root> <layers.json>")
    sys.exit(1 if report(sys.argv[1], sys.argv[2]) else 0)
