"""AR101 Lab 14 tests. Run with `python test_atlas.py` or `pytest test_atlas.py`.
Every test fails on the starter and passes once atlas.py is complete."""
from atlas import next_pow2, texture_bytes, safe_mip_level, pack_shelves, choose_atlas, uv_rect


def squares(n, size):
    return [(f"s{i:02d}", size, size) for i in range(n)]


def test_next_pow2():
    assert [next_pow2(n) for n in (1, 2, 3, 32, 33, 255, 256, 257)] == [1, 2, 4, 32, 64, 256, 256, 512]


def test_texture_bytes():
    assert texture_bytes(256, 256) == 262144                       # 256 KiB
    assert texture_bytes(2048, 2048, "RGBA8", mips=True) == 22369620   # about 4/3 of 16 MiB
    assert texture_bytes(2048, 2048, "BC7") == 4 * 1024 * 1024
    assert texture_bytes(2048, 2048, "BC1") == 2 * 1024 * 1024
    assert texture_bytes(4, 4, "BC1", mips=True) == 24               # 4x4, 2x2, 1x1 each pay one block


def test_safe_mip_level():
    assert [safe_mip_level(g) for g in (0, 1, 2, 3, 4, 8)] == [None, 0, 1, 1, 2, 3]


def check_layout(sprites, placed, width, height, gutter, align):
    assert set(placed) == {n for n, _, _ in sprites}
    cells = []
    for name, w, h in sprites:
        x, y, pw, ph = placed[name]
        assert (pw, ph) == (w, h)
        assert x % align == 0 and y % align == 0, f"{name} not aligned"
        cx, cy, cw, ch = x - gutter, y - gutter, w + 2 * gutter, h + 2 * gutter
        assert cx >= 0 and cy >= 0 and cx + cw <= width and cy + ch <= height, f"{name} out of bounds"
        cells.append((cx, cy, cw, ch))
    for i, a in enumerate(cells):
        for b in cells[i + 1:]:
            apart = a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1]
            assert apart, f"cells overlap: {a} {b}"


def test_pack_shelves_mixed():
    sprites = [("tall", 20, 40), ("wide", 60, 10), ("a", 16, 16), ("b", 16, 16), ("c", 30, 20)]
    placed, used = pack_shelves(sprites, 64, gutter=2, align=2)
    check_layout(sprites, placed, 64, used, 2, 2)
    assert placed["tall"] == (2, 2, 20, 40)          # tallest goes first, top-left
    assert placed["c"] == (26, 2, 30, 20)            # second on the first shelf
    assert used == 78                                 # shelves 44, 20 and 14 px tall
    try:
        pack_shelves([("huge", 70, 5)], 64)
        assert False, "a 70 px sprite cannot fit a 64 px atlas"
    except ValueError:
        pass


def test_choose_atlas_padding_cliff():
    assert choose_atlas(squares(64, 32), gutter=0)[0] == 256
    assert choose_atlas(squares(64, 32), gutter=2, align=2)[0] == 512
    side, placed = choose_atlas(squares(64, 28), gutter=2, align=2)
    assert side == 256
    check_layout(squares(64, 28), placed, side, side, 2, 2)


def test_uv_rect():
    assert uv_rect((64, 32, 32, 32), 256) == (0.25, 0.125, 0.375, 0.25)


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:  # NotImplementedError counts as a failure
                failed += 1
                print(f"FAIL {name}: {type(exc).__name__} {exc}")
    raise SystemExit(1 if failed else 0)
