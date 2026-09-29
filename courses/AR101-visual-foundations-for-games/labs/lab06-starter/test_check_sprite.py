"""Self-tests for the lab 06 checker (a finished tool). Run them if you change it:
`.venv/bin/python test_check_sprite.py`. Exit code is 0 only if all pass."""
import os
import struct
import sys
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_sprite import check, orphans, read_png, scale_problems, write_png


def _png(path, w, h, ctype, depth, lines, plte=None, trns=None):
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, depth, ctype, 0, 0, 0))
    if plte:
        out += chunk(b"PLTE", plte)
    if trns:
        out += chunk(b"tRNS", trns)
    out += chunk(b"IDAT", zlib.compress(b"".join(lines))) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(out)


def test_samples():
    p = lambda n: os.path.join(HERE, n)
    problems, notes = check(p("sample_potion.png"), p("sample.hex"), p("sample_potion_4x.png"))
    assert problems == ["off-palette colors: c33a52"], problems
    assert "2 orphan pixel(s): (4,9) (7,11)" in notes
    problems, _ = check(p("sample_potion.png"), scaled=p("sample_potion_2_5x.png"))
    assert len(problems) == 1 and "x2.5" in problems[0]


def test_rgba_round_trip_and_blur_detection():
    rows = [[(10 * x, 20 * y, 30, 255) for x in range(4)] for y in range(4)]
    with tempfile.TemporaryDirectory() as d:
        write_png(os.path.join(d, "a.png"), rows)
        assert read_png(os.path.join(d, "a.png"))[2] == rows
        big = [[rows[y // 3][x // 3] for x in range(12)] for y in range(12)]
        assert scale_problems(rows, big) == []
        big[5][5] = (1, 2, 3, 255)
        assert "differs" in scale_problems(rows, big)[0]


def test_filters_sub_and_paeth():
    # 2x2 RGB image written with filter 1 (sub) on row 0 and 4 (paeth) on row 1.
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "f.png")
        row0 = bytes([1, 10, 20, 30, 5, 5, 5])            # (10,20,30) then (15,25,35)
        row1 = bytes([4, 1, 1, 1, 0, 0, 0])               # paeth: (11,21,31), then +prev
        _png(path, 2, 2, 2, 8, [row0, row1])
        _, _, rows = read_png(path)
        assert rows[0] == [(10, 20, 30, 255), (15, 25, 35, 255)]
        assert rows[1][0] == (11, 21, 31, 255)


def test_indexed_4bit_with_transparency():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "i.png")
        plte = bytes([0, 0, 0, 255, 0, 0, 0, 255, 0])
        _png(path, 3, 1, 3, 4, [bytes([0, 0x01, 0x20])], plte, bytes([0]))
        _, _, rows = read_png(path)
        assert rows[0] == [(0, 0, 0, 0), (255, 0, 0, 255), (0, 255, 0, 255)]


def test_orphans():
    a, b, t = (1, 1, 1, 255), (2, 2, 2, 255), (0, 0, 0, 0)
    rows = [[a, a, t], [a, b, t], [t, t, b]]
    assert orphans(rows) == []                 # the two b pixels touch diagonally
    rows[2][2] = t
    assert orphans(rows) == [(1, 1)]


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print("all tests pass" if not failed else f"{failed} test(s) failing")
    sys.exit(1 if failed else 0)
