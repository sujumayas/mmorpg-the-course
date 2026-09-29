"""AR101 Lab 14 starter: a tiny sprite atlas packer and texture memory calculator.

Run:   python atlas.py sprites.json
Test:  python test_atlas.py        (or: pytest test_atlas.py)

Every function marked TODO raises NotImplementedError until you write it.
Coordinates are in pixels with the origin at the top-left of the atlas.
"""
import json
import math
import sys

# Bytes per pixel for uncompressed formats, bytes per 4x4 block for block-compressed ones.
BYTES_PER_PIXEL = {"RGBA8": 4}
BYTES_PER_BLOCK = {"BC1": 8, "BC7": 16}


def next_pow2(n):
    """Smallest power of two that is >= n, for n >= 1. next_pow2(33) == 64."""
    raise NotImplementedError("TODO: next_pow2")


def texture_bytes(w, h, fmt="RGBA8", mips=False):
    """GPU memory for one w x h texture in bytes.

    RGBA8 costs 4 bytes per pixel. BC1 and BC7 store 4x4 blocks (8 and 16 bytes);
    a level whose side is not a multiple of 4 still pays for whole blocks.
    With mips=True, add every level down to 1x1, halving each side (never below 1).
    """
    raise NotImplementedError("TODO: texture_bytes")


def safe_mip_level(gutter):
    """Highest mip level that cannot bleed under bilinear filtering, given an
    extruded gutter of `gutter` pixels on every side of every sprite (and sprites
    aligned to 2**level). Return None when gutter == 0 (only point filtering is safe)."""
    raise NotImplementedError("TODO: safe_mip_level")


def pack_shelves(sprites, atlas_width, gutter=0, align=1):
    """Shelf-pack sprites into a strip `atlas_width` pixels wide.

    sprites: list of (name, w, h).
    Each sprite occupies a cell of (w + 2*gutter) x (h + 2*gutter).
    Sort by height (tallest first), then by name. Fill a shelf left to right; when the next
    cell does not fit, start a new shelf under the tallest cell of the current one.
    Round every cell's x and y up to a multiple of `align`.
    Return (placements, used_height) where placements maps name -> (x, y, w, h) of the
    sprite content (inside its gutter). Raise ValueError if a cell is wider than the atlas.
    """
    raise NotImplementedError("TODO: pack_shelves")


def choose_atlas(sprites, gutter=0, align=1, max_side=4096):
    """Smallest square power-of-two side that holds every sprite.
    Return (side, placements). Raise ValueError if nothing up to max_side fits."""
    raise NotImplementedError("TODO: choose_atlas")


def uv_rect(rect, side):
    """Convert a content rect (x, y, w, h) to normalized (u0, v0, u1, v1) in a square atlas."""
    raise NotImplementedError("TODO: uv_rect")


def main(path):
    with open(path) as fh:
        sprites = [(s["name"], s["w"], s["h"]) for s in json.load(fh)["sprites"]]
    print(f"{len(sprites)} sprites, {sum(w * h for _, w, h in sprites)} content pixels")
    for gutter in (0, 2, 4):
        try:
            side, placed = choose_atlas(sprites, gutter, align=max(1, gutter))
        except NotImplementedError as exc:
            print(f"gutter {gutter}: not implemented yet ({exc})")
            continue
        fill = sum(w * h for _, w, h in sprites) / side ** 2
        mem = {f: texture_bytes(side, side, f, mips=True) / 1024 for f in ("RGBA8", "BC7", "BC1")}
        print(f"gutter {gutter}: {side}x{side}, fill {fill:.0%}, safe mip {safe_mip_level(gutter)}, "
              + ", ".join(f"{f} {k:.0f} KiB" for f, k in mem.items()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sprites.json")
