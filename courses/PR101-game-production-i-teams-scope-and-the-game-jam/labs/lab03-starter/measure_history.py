"""PR101 Lab 03: measure how Git stores repeated versions of a binary file.

Usage:
    python measure_history.py [versions] [size_bytes]

Builds two throwaway repositories in a temp folder, commits `versions`
versions of one binary file in each, packs them with `git gc --aggressive`,
and prints the packed size:
  resave  each version is fully re-randomized (like a re-exported PNG)
  patch   each version changes 10 bytes in place
"""
import os
import random
import shutil
import subprocess
import sys
import tempfile


def packed_kib(mode, versions, size):
    d = tempfile.mkdtemp(prefix=f"lab03-{mode}-")
    try:
        def g(*a):
            return subprocess.run(["git", *a], cwd=d, check=True,
                                  capture_output=True, text=True).stdout
        g("init", "-q", "-b", "main")
        g("config", "user.name", "Lab"); g("config", "user.email", "lab@example.com")
        rng = random.Random(1)
        data = bytearray(rng.randbytes(size))
        for v in range(versions):
            if v and mode == "resave":
                data = bytearray(rng.randbytes(size))
            elif v:
                for _ in range(10):
                    data[rng.randrange(size)] = rng.randrange(256)
            with open(os.path.join(d, "texture.png"), "wb") as f:
                f.write(data)
            g("add", "texture.png"); g("commit", "-q", "-m", f"Save version {v + 1}")
        g("gc", "-q", "--aggressive")
        stats = dict(line.split(": ") for line in g("count-objects", "-v").splitlines())
        return int(stats["size-pack"]) + int(stats["size"])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    versions = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
    print(f"{versions} versions of a {size:,}-byte file ({size / 1024:,.0f} KiB each)")
    for mode in ("resave", "patch"):
        print(f"  {mode:6}: packed history {packed_kib(mode, versions, size):,} KiB")


if __name__ == "__main__":
    main()
