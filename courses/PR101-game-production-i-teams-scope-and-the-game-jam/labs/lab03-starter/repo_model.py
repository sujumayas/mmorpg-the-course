"""PR101 Lab 03, part A: the clone-size model from lecture 3, section 2.

Fill in every function marked TODO, then run:
    python test_repo_model.py

An asset is a dict: {"path": "art/hero.png", "size": 4_000_000, "versions": 9}
  path      path inside the repository
  size      average size of one version, in bytes
  versions  how many versions have been committed (1 = committed once)

Model assumptions (the lecture's):
  - Without LFS, history stores every version at full size (binaries do not
    delta-compress after a re-save). Treat text files the same way; they are
    small, so the error does not matter here.
  - With LFS, history stores one pointer per version, and the LFS server
    stores every version at full size.
  - A clone downloads the whole Git history plus, for LFS files, only the
    current version of each file.
"""
from fnmatch import fnmatchcase
import posixpath

POINTER_TEMPLATE = (
    "version https://git-lfs.github.com/spec/v1\n"
    "oid sha256:{oid}\n"
    "size {size}\n"
)


def pointer_size(size_bytes):
    """Bytes in the LFS pointer file for a file of size_bytes.
    The oid is always 64 hex characters. Example: 3_000_000 -> 132."""
    raise NotImplementedError("TODO")


def is_lfs(path, patterns):
    """True if the file name (the last part of path) matches any pattern,
    for example "*.png". Case-sensitive, like Git on Linux."""
    raise NotImplementedError("TODO")


def history_bytes(assets, patterns):
    """Bytes stored in Git history (not counting the LFS server)."""
    raise NotImplementedError("TODO")


def lfs_server_bytes(assets, patterns):
    """Bytes stored on the LFS server: every version of every LFS file."""
    raise NotImplementedError("TODO")


def clone_bytes(assets, patterns):
    """Bytes a fresh clone downloads: all of Git history plus the current
    version of each LFS file."""
    raise NotImplementedError("TODO")


def clone_minutes(n_bytes, mbps):
    """Download time in minutes at mbps megabits per second (1 MB = 1e6 bytes)."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    semester = [{"path": f"art/a{i}.png", "size": 4_000_000, "versions": 9} for i in range(200)]
    for pats in ([], ["*.png"]):
        b = clone_bytes(semester, pats)
        print(f"patterns={pats}: clone {b / 1e6:,.1f} MB, {clone_minutes(b, 50):.1f} min at 50 Mbps")
