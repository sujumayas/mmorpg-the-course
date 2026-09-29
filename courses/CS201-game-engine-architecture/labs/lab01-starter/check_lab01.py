"""Checks for Lab 01. Run from inside lab01-starter:  python check_lab01.py

Each check prints PASS, FAIL (with the reason) or TODO (function not written).
The exit code is 0 only when every check passes.
"""
import json
import sys
from pathlib import Path

import layercheck as lc

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / "layers.json").read_text())
LAYERS = CONFIG["layers"]
PLATFORM = CONFIG["platform_layer"]
OS_HEADERS = CONFIG["os_headers"]
ROOT = HERE / "mini_engine"

SAMPLE = """#include <cstdio>
#  include "core/log.h"   // logging
// #include "game/game.h"
   #include<unistd.h>
int x; // #include "nope.h"
"""


def check_parse():
    got = lc.parse_includes(SAMPLE)
    want = [("cstdio", True), ("core/log.h", False), ("unistd.h", True)]
    assert got == want, f"parse_includes(SAMPLE) returned {got}, expected {want}"


def check_layer_of():
    assert lc.layer_of("core/log.h", LAYERS) == 1, "core/log.h should be layer 1"
    assert lc.layer_of("main.cpp", LAYERS) == 6, "main.cpp should be layer 6"
    assert lc.layer_of("game/save.h", LAYERS) == 5, "game/save.h should be layer 5"
    try:
        lc.layer_of("tools/editor.h", LAYERS)
    except KeyError:
        return
    raise AssertionError("an unknown folder should raise KeyError")


def check_scan():
    files = lc.scan(ROOT)
    assert len(files) == 14, f"expected 14 files, got {len(files)}"
    assert "main.cpp" in files and "core/log.h" in files, "keys must be relative paths with '/'"
    assert files["core/log.h"]["lines"] == 8, f"core/log.h has 8 lines, got {files['core/log.h']['lines']}"
    assert sum(f["lines"] for f in files.values()) == 170, "total lines should be 170"
    assert ("game/player.h", False) in files["core/log.h"]["includes"], "core/log.h includes game/player.h"


def check_upward():
    files = lc.scan(ROOT)
    got = lc.upward(files, LAYERS)
    want = [("core/log.h", "game/player.h"), ("platform/window.h", "game/game.h")]
    assert got == want, f"upward() returned {got}, expected {want}"


def check_leaks():
    files = lc.scan(ROOT)
    got = lc.os_leaks(files, LAYERS, PLATFORM, OS_HEADERS)
    assert got == ["game/save.h"], f"os_leaks() returned {got}, expected ['game/save.h']"
    fake = {"platform/a.h": {"lines": 1, "includes": [("sys/stat.h", True)]},
            "core/b.h": {"lines": 1, "includes": [("sys/stat.h", True), ("vector", True)]},
            "game/c.h": {"lines": 1, "includes": [("cstdio", True)]}}
    got = lc.os_leaks(fake, LAYERS, PLATFORM, OS_HEADERS)
    assert got == ["core/b.h"], f"prefix match: expected ['core/b.h'], got {got}"


def check_order():
    deps = {"Audio": ["Files", "Memory"], "Files": ["Memory"],
            "Renderer": ["Files", "Memory", "Window"], "Window": ["Memory"]}
    got = lc.start_order(deps)
    want = ["Memory", "Files", "Audio", "Window", "Renderer"]
    assert got == want, f"start_order() returned {got}, expected {want}"


def check_cycle():
    deps = {"a": ["b"], "b": ["a"], "c": []}
    try:
        lc.start_order(deps)
    except lc.CycleError as e:
        assert e.members == ["a", "b"], f"CycleError.members should be ['a', 'b'], got {e.members}"
        return
    raise AssertionError("a <-> b is a cycle: start_order must raise CycleError")


CHECKS = [("1 parse_includes", check_parse), ("2 layer_of", check_layer_of),
          ("3 scan", check_scan), ("4 upward", check_upward),
          ("5 os_leaks", check_leaks), ("6 start_order", check_order),
          ("7 cycle detection", check_cycle)]


def main():
    passed = 0
    for name, fn in CHECKS:
        try:
            fn()
        except NotImplementedError:
            print(f"TODO  {name}")
        except Exception as e:  # noqa: BLE001 - report every failure the same way
            print(f"FAIL  {name}: {e}")
        else:
            print(f"PASS  {name}")
            passed += 1
    print(f"{passed}/{len(CHECKS)} checks pass")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
