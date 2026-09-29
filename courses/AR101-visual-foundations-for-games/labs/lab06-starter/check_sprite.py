"""AR101 Lab 06: sprite checker. Standard library only; a finished tool, not a TODO.

Usage (from the repository root):

    .venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab06-starter/check_sprite.py \
        sprite.png --palette zone.hex --scaled sprite_4x.png

It checks the rules of the lab 06 brief:
  - the sprite is square and 16, 24 or 32 pixels on a side;
  - every opaque pixel uses a color from the palette file (if given);
  - it uses at most --max-colors opaque colors (default 8);
  - orphan pixels: opaque pixels whose color matches none of their 8 neighbors
    (listed; the brief allows at most 4, each one justified);
  - the scaled copy (if given) is an exact integer nearest-neighbor enlargement:
    same scale on both axes, every block one flat color. Anything else means
    blurred or mixed-size pixels (mixels).

Exit code 0 when every rule passes, 1 otherwise. Reads 8-bit RGB/RGBA/gray PNGs
and indexed PNGs of any bit depth, non-interlaced (what Aseprite, Pyxel Edit,
LibreSprite, GIMP and Krita export by default).
"""
import argparse
import struct
import sys
import zlib

SIZES = (16, 24, 32)


# ---- PNG reading and writing -------------------------------------------------

def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def read_png(path):
    """Return (width, height, rows) where rows[y][x] is (r, g, b, a)."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG file")
    pos, idat, palette, trns = 8, b"", None, None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
    if interlace:
        raise ValueError(f"{path}: interlaced PNGs are not supported; re-export without interlace")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    if ctype != 3 and depth != 8 and not (ctype == 0 and depth < 8):
        raise ValueError(f"{path}: use 8 bits per channel")
    bits = channels * depth
    stride = (w * bits + 7) // 8
    bpp = max(1, bits // 8)
    raw = zlib.decompress(idat)
    rows, prev = [], bytearray(stride)
    for y in range(h):
        ftype = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if ftype == 1:
                line[i] = (line[i] + a) & 255
            elif ftype == 2:
                line[i] = (line[i] + b) & 255
            elif ftype == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif ftype == 4:
                line[i] = (line[i] + _paeth(a, b, c)) & 255
        prev = line
        if depth < 8:
            per = 8 // depth
            vals = [(line[x // per] >> (8 - depth * (x % per + 1))) & ((1 << depth) - 1) for x in range(w)]
        else:
            vals = None
        row = []
        for x in range(w):
            if ctype == 3:
                idx = vals[x] if vals else line[x]
                r, g, b = palette[idx]
                a = trns[idx] if trns and idx < len(trns) else 255
            elif ctype == 0:
                v = vals[x] * 255 // ((1 << depth) - 1) if vals else line[x]
                r = g = b = v
                a = 255
            elif ctype == 4:
                r = g = b = line[2 * x]
                a = line[2 * x + 1]
            elif ctype == 2:
                r, g, b = line[3 * x:3 * x + 3]
                a = 255
            else:
                r, g, b, a = line[4 * x:4 * x + 4]
            row.append((r, g, b, a))
        rows.append(row)
    return w, h, rows


def write_png(path, rows):
    """Write rows of (r, g, b, a) as an 8-bit RGBA PNG."""
    h, w = len(rows), len(rows[0])
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in rows)

    def chunk(kind, body):
        return (struct.pack(">I", len(body)) + kind + body
                + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))


# ---- checks ------------------------------------------------------------------

def load_palette(path):
    out = set()
    with open(path) as f:
        for line in f:
            s = line.strip().lstrip("#")
            if s and not s.startswith(";"):
                out.add(tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)))
    return out


def opaque_colors(rows):
    return {px[:3] for row in rows for px in row if px[3] >= 128}


def orphans(rows):
    """Opaque pixels whose color appears in none of their 8 neighbors."""
    h, w = len(rows), len(rows[0])
    found = []
    for y in range(h):
        for x in range(w):
            px = rows[y][x]
            if px[3] < 128:
                continue
            same = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h:
                        q = rows[y + dy][x + dx]
                        if q[3] >= 128 and q[:3] == px[:3]:
                            same = True
            if not same:
                found.append((x, y))
    return found


def scale_problems(small, big):
    """Empty list if big is an exact integer nearest-neighbor enlargement of small."""
    h, w = len(small), len(small[0])
    bh, bw = len(big), len(big[0])
    if bw % w or bh % h or bw // w != bh // h:
        return [f"scaled copy is {bw}x{bh}: not the same whole-number multiple of {w}x{h} "
                f"on both axes (x{bw / w:g} by x{bh / h:g})"]
    k = bw // w
    bad = 0
    for y in range(bh):
        for x in range(bw):
            s, b = small[y // k][x // k], big[y][x]
            if (s[3] < 128) != (b[3] < 128) or (s[3] >= 128 and s[:3] != b[:3]):
                bad += 1
    if bad:
        return [f"scaled copy (x{k}) differs from a nearest-neighbor enlargement in {bad} "
                f"screen pixels: blurred or mixed-size pixels"]
    return []


def check(sprite, palette=None, scaled=None, max_colors=8, max_orphans=4):
    w, h, rows = read_png(sprite)
    problems, notes = [], []
    if w != h or w not in SIZES:
        problems.append(f"sprite is {w}x{h}; the brief asks for 16x16, 24x24 or 32x32")
    colors = opaque_colors(rows)
    notes.append(f"{len(colors)} opaque colors")
    if len(colors) > max_colors:
        problems.append(f"{len(colors)} opaque colors (limit {max_colors})")
    if palette:
        off = sorted(colors - load_palette(palette))
        if off:
            problems.append("off-palette colors: " + ", ".join("{:02x}{:02x}{:02x}".format(*c) for c in off))
    orph = orphans(rows)
    notes.append(f"{len(orph)} orphan pixel(s)" + (": " + " ".join(f"({x},{y})" for x, y in orph) if orph else ""))
    if len(orph) > max_orphans:
        problems.append(f"{len(orph)} orphan pixels (limit {max_orphans}, each justified)")
    if scaled:
        problems += scale_problems(rows, read_png(scaled)[2])
    return problems, notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sprite")
    ap.add_argument("--palette")
    ap.add_argument("--scaled")
    ap.add_argument("--max-colors", type=int, default=8)
    args = ap.parse_args(argv)
    problems, notes = check(args.sprite, args.palette, args.scaled, args.max_colors)
    for n in notes:
        print("  " + n)
    if problems:
        for p in problems:
            print("- " + p)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
