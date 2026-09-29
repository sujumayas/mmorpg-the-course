"""PR101 Lab 03, part B checker.

Usage:
    python check_lab03.py lab03-repo

Prints PASS or FAIL per check; exits 0 only when all pass.
"""
import re
import subprocess
import sys
from fnmatch import fnmatchcase
from pathlib import Path

BINARY = ["*.png", "*.wav", "*.ogg", "*.psd"]
POINTER_START = b"version https://git-lfs.github.com/spec/v1\n"


def git(repo, *args, raw=False):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=not raw)
    return r.returncode, r.stdout


def attr_lines(text):
    """Map pattern -> set of attributes from a .gitattributes text."""
    out = {}
    for line in text.splitlines():
        parts = line.split()
        if parts and not parts[0].startswith("#"):
            out.setdefault(parts[0], set()).update(parts[1:])
    return out


def checks(repo):
    results = []

    def add(name, ok, hint=""):
        results.append((name, bool(ok), hint))

    _, status = git(repo, "status", "--porcelain")
    add("working tree clean", status.strip() == "", "commit or discard your changes")

    code, text = git(repo, "show", "HEAD:.gitattributes")
    attrs = attr_lines(text if code == 0 else "")
    for pat in BINARY:
        a = attrs.get(pat, set())
        add(f".gitattributes sends {pat} to LFS", {"filter=lfs", "diff=lfs", "merge=lfs", "-text"} <= a,
            f"git lfs track \"{pat}\"")
    add("*.psd is lockable", "lockable" in attrs.get("*.psd", set()),
        "git lfs track --lockable \"*.psd\"")
    add("*.gd is not in LFS", not any(fnmatchcase("enemy.gd", p) and "filter=lfs" in a
                                      for p, a in attrs.items()))

    # Every binary blob reachable from any branch or tag must be an LFS pointer.
    _, objs = git(repo, "rev-list", "--objects", "--all")
    raw_blobs = []
    for line in objs.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2 and any(fnmatchcase(Path(parts[1]).name, p) for p in BINARY):
            _, body = git(repo, "cat-file", "-p", parts[0], raw=True)
            if not body.startswith(POINTER_START):
                raw_blobs.append(parts[1])
    add("no raw binaries anywhere in history", not raw_blobs,
        f"{len(set(raw_blobs))} path(s) still raw; see step 6 (git lfs migrate import --everything)")

    _, counts = git(repo, "count-objects", "-v")
    stats = dict(l.split(": ") for l in counts.splitlines())
    kib = int(stats.get("size-pack", 0)) + int(stats.get("size", 0))
    add("Git object store under 1,024 KiB after cleanup", kib < 1024,
        f"{kib:,} KiB now; expire the reflog and gc --prune=now (step 7)")

    _, files = git(repo, "lfs", "ls-files", "--name-only")
    add("git lfs ls-files lists all 11 binaries", len(files.split()) == 11,
        f"lists {len(files.split())}")

    _, log = git(repo, "log", "--format=%ae", "main")
    add("you committed at least once", any(e != "setup@lab03.invalid" for e in log.split()),
        "commit your .gitattributes change")
    return results


def main(argv):
    if len(argv) != 2 or not (Path(argv[1]) / ".git").exists():
        print(__doc__)
        return 2
    results = checks(argv[1])
    for name, ok, hint in results:
        print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not hint else f"  ({hint})"))
    passed = sum(ok for _, ok, _ in results)
    print(f"{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
