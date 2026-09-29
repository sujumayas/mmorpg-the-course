"""AR101 Lab 05 starter: ramps, harmony and a palette checker. Standard library only.

Fill in the four TODO functions, then run the tests from the repository root:

    .venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab05-starter/test_palette.py

Check a palette file you designed:

    .venv/bin/python .../palette.py my_zone.hex

Palette files use the Lospec .hex format (one color per line) with comment
lines that group the colors:  "; ramp <name>" (dark to light), "; reserved",
and "; neutral". Conventions follow the week 5 lecture: hue in degrees,
S and V in percent, lightness as CIE L* (week 1).
"""
import sys

# ---- provided: color helpers from weeks 1 and 4 (lab 04 solutions) ---------


def lightness(r, g, b):
    """CIE L* (0-100) of an sRGB color with 0-255 channels, as in week 1."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    y = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y


def hex_to_rgb(text):
    s = text.strip().lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "{:02x}{:02x}{:02x}".format(*rgb)


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    hi, lo = max(r, g, b), min(r, g, b)
    c = hi - lo
    if c == 0:
        h = 0.0
    elif hi == r:
        h = 60 * (((g - b) / c) % 6)
    elif hi == g:
        h = 60 * ((b - r) / c + 2)
    else:
        h = 60 * ((r - g) / c + 4)
    return h, (0.0 if hi == 0 else 100 * c / hi), 100 * hi


def hsv_to_rgb(h, s, v):
    h = h % 360
    s, v = s / 100, v / 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60)]
    return tuple(int((u + m) * 255 + 0.5) for u in (r, g, b))


def lerp(a, b, t):
    return a + (b - a) * t


def value_at(h, s, v):
    return lightness(*hsv_to_rgb(h, s, v))


def solve_v(target, h, s):
    """Smallest V (0-100) with L* >= target at this h and s, or None if even
    V = 100 is too dark (then the caller must lower s; see week 4)."""
    if value_at(h, s, 100) < target:
        return None
    lo, hi = 0.0, 100.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if value_at(h, s, mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi


# ---- your work --------------------------------------------------------------

def lerp_hue(a, b, t):
    """Move from hue a toward hue b the short way round; result in [0, 360)."""
    raise NotImplementedError("lerp_hue")


def ramp(h_shadow, h_light, s_mid, s_end, v_dark, v_light, n):
    """The week 5 ramp model. Return n lowercase hex strings, dark to light.

    t = i / (n - 1); H = lerp_hue(h_shadow, h_light, t);
    S = s_mid - (s_mid - s_end) * |2t - 1|;  V = lerp(v_dark, v_light, t).
    Convert with hsv_to_rgb above.
    """
    raise NotImplementedError("ramp")


def harmony(base, scheme):
    """Hues for a harmony scheme, each in [0, 360), in the order of the
    lecture's table. scheme is one of: "monochromatic", "analogous",
    "complementary", "split", "triadic", "tetradic"."""
    raise NotImplementedError("harmony")


def even_ramp(h_shadow, h_light, s_mid, s_end, l_dark, l_light, n):
    """Like ramp(), but choose each step's V so that its L* is exactly
    lerp(l_dark, l_light, t): an even value staircase. Use solve_v. If a step
    cannot reach its L* at V = 100, lower that step's S in steps of 1 until
    it can. Return n lowercase hex strings."""
    raise NotImplementedError("even_ramp")


# ---- provided: palette file checker -----------------------------------------

def load_groups(path):
    """Return a list of (kind, name, [hex, ...]) in file order."""
    groups, current = [], None
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(";"):
                words = line[1:].split()
                if words and words[0] in ("ramp", "reserved", "neutral"):
                    current = (words[0], " ".join(words[1:]) or words[0], [])
                    groups.append(current)
                continue
            if current is None:
                current = ("neutral", "ungrouped", [])
                groups.append(current)
            current[2].append(line.lower().lstrip("#"))
    return groups


def hue_gap(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def check_palette(path, max_colors=16, min_step=8, reserve_hue=60, reserve_gap=20):
    """Return a list of problems (empty means the palette passes)."""
    groups = load_groups(path)
    problems = []
    colors = {h for _, _, hs in groups for h in hs}
    if len(colors) > max_colors:
        problems.append(f"{len(colors)} unique colors (limit {max_colors})")
    ramps = [(name, hs) for kind, name, hs in groups if kind == "ramp"]
    if len(ramps) < 3:
        problems.append(f"only {len(ramps)} ramp(s) (need at least 3)")
    for name, hs in ramps:
        if len(hs) < 3:
            problems.append(f"ramp {name}: {len(hs)} steps (need at least 3)")
        ls = [lightness(*hex_to_rgb(h)) for h in hs]
        for i in range(1, len(ls)):
            if ls[i] - ls[i - 1] < min_step:
                problems.append(f"ramp {name}: step {i} rises {ls[i] - ls[i - 1]:.1f} L* "
                                f"(need {min_step})")
    reserved = [h for kind, _, hs in groups if kind == "reserved" for h in hs]
    if not reserved:
        problems.append("no reserved color")
    for r in reserved:
        hr, sr, _ = rgb_to_hsv(*hex_to_rgb(r))
        lr = lightness(*hex_to_rgb(r))
        for name, hs in ramps:
            for h in hs:
                hh, sh, _ = rgb_to_hsv(*hex_to_rgb(h))
                if sh >= 15 and hue_gap(hr, hh) < reserve_hue:
                    problems.append(f"reserved {r}: hue within {reserve_hue} deg of {h} "
                                    f"in ramp {name}")
            mid = hs[len(hs) // 2]
            gap = abs(lr - lightness(*hex_to_rgb(mid)))
            if gap < reserve_gap:
                problems.append(f"reserved {r}: dV {gap:.1f} to the middle of ramp {name} "
                                f"(need {reserve_gap})")
    return problems


def report(path):
    for kind, name, hs in load_groups(path):
        print(f"{kind} {name}")
        for h in hs:
            hh, s, v = rgb_to_hsv(*hex_to_rgb(h))
            print(f"  {h}  H {hh:5.1f}  S {s:5.1f}  V {v:5.1f}  L* {lightness(*hex_to_rgb(h)):5.1f}")
    problems = check_palette(path)
    print("\nPASS" if not problems else "\n" + "\n".join("- " + p for p in problems))
    return not problems


if __name__ == "__main__":
    sys.exit(0 if report(sys.argv[1]) else 1)
