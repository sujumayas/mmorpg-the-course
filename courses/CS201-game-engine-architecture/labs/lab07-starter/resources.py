"""CS201 Lab 07: a resource manager with handles, reference counts and hot reload.

Fill in every function marked TODO. Each docstring says exactly what
check_lab07.py expects. Standard library only, Python 3.10 or later.
"""
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Part A: the load-time model from lecture section 2
# ---------------------------------------------------------------------------

def load_time(reads, megabytes, access_ms, rate_mb_s):
    """Seconds to read `megabytes` in `reads` separate reads.

    T = reads * access_ms / 1000 + megabytes / rate_mb_s
    """
    raise NotImplementedError("TODO A1: load_time")


def knee_mb(access_ms, rate_mb_s):
    """Read size in MB at which the effective rate is half of rate_mb_s."""
    raise NotImplementedError("TODO A2: knee_mb")


def pack_or_loose(file_sizes_mb, access_ms, rate_mb_s):
    """Compare loading every file separately against one packed read.

    Returns a tuple (loose_seconds, packed_seconds, speedup) where
    speedup = loose_seconds / packed_seconds. Packed means one read of the
    total size.
    """
    raise NotImplementedError("TODO A3: pack_or_loose")


# ---------------------------------------------------------------------------
# Part B: handles and the reference-counted cache
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Handle:
    index: int
    generation: int


def parse_texture(text):
    """The 'loader' for this lab's fake texture format.

    A texture file holds one line 'WIDTHxHEIGHT COLOR', for example
    '64x32 red'. Width and height must be powers of two between 1 and 4096.
    Returns a dict {'w': 64, 'h': 32, 'color': 'red'}. Raises ValueError with a
    readable message for anything else. Provided, do not change.
    """
    parts = text.strip().split()
    if len(parts) != 2 or "x" not in parts[0]:
        raise ValueError(f"expected 'WxH color', got {text.strip()!r}")
    w_text, h_text = parts[0].split("x", 1)
    if not (w_text.isdigit() and h_text.isdigit()):
        raise ValueError(f"size must be two integers, got {parts[0]!r}")
    w, h = int(w_text), int(h_text)
    for n in (w, h):
        if n < 1 or n > 4096 or n & (n - 1):
            raise ValueError(f"size {n} is not a power of two in 1..4096")
    return {"w": w, "h": h, "color": parts[1]}


class ResourceManager:
    """Loads each path once, hands out generational handles, counts references.

    `read_file` is a function path -> str (the tests pass a dict lookup, the
    demo passes a real file read). `parse` turns that text into data and may
    raise ValueError.

    Suggested fields (you may change them):
      self.slots      list of dicts {'generation', 'path', 'data', 'refs'}
                      or None data for a free slot
      self.free       list of free slot indices
      self.by_path    dict path -> slot index for resident resources
      self.disk_reads number of times read_file has been called
    """

    def __init__(self, read_file, parse=parse_texture):
        self.read_file = read_file
        self.parse = parse
        self.slots = []
        self.free = []
        self.by_path = {}
        self.disk_reads = 0

    def acquire(self, path):
        """Return a Handle for `path`, loading it only if it is not resident.

        - If the path is resident, add one reference and return a handle equal
          to the one handed out before (same index, same generation).
        - Otherwise read and parse it, put it in a free slot if one exists
          (lowest index is NOT required; reuse the most recently freed slot)
          or in a new slot, with refs = 1.
        - If parse raises ValueError, let it propagate and leave the manager
          unchanged except for disk_reads.
        """
        raise NotImplementedError("TODO B1: acquire")

    def get(self, handle):
        """Return the data for `handle`, or None if the handle is stale."""
        raise NotImplementedError("TODO B2: get")

    def release(self, handle):
        """Drop one reference. At zero, free the slot: bump its generation,
        clear its data, forget the path, add the index to the free list.
        Releasing a stale handle raises ValueError('stale handle')."""
        raise NotImplementedError("TODO B3: release")

    def refs(self, path):
        """Reference count for a resident path, 0 if not resident."""
        raise NotImplementedError("TODO B4: refs")

    # -----------------------------------------------------------------------
    # Part C: hot reload
    # -----------------------------------------------------------------------

    def reload(self, path):
        """Re-read and re-parse a resident path and swap the data in place.

        Returns True if the new data was swapped in. If parse raises
        ValueError, keep the old data, and return False. Every existing handle
        to the path must stay valid and see the new data. Reloading a path that
        is not resident returns False and reads nothing.
        """
        raise NotImplementedError("TODO C1: reload")


def rebuild_order(changed, uses):
    """Everything that must be rebuilt after `changed` changes, in a safe order.

    `uses` maps an asset to the list of assets it uses directly. Return the
    list of assets that use `changed` directly or indirectly (not `changed`
    itself) such that every asset comes after all the other assets in the
    list that it uses. Break ties alphabetically so the answer is unique.
    Raise ValueError('cycle: ...') if the affected part of the graph has a
    cycle.

    Hint: lecture section 5's breadth-first order is NOT enough. Collect the
    affected set first, then do a topological sort (Kahn's algorithm) over
    it, always taking the alphabetically smallest ready asset.
    """
    raise NotImplementedError("TODO C2: rebuild_order")
