"""AU101 Lab 07: distance attenuation and equal-power panning.

Run:   python spatial.py            (prints the curve table and your sound list)
Test:  python -m unittest test_spatial -v

Fill in every function marked TODO. The docstrings define what each returns.
Distances are in metres (or any unit, as long as you are consistent).
Gains are amplitude multipliers: 1.0 is unchanged, 0.5 is -6.02 dB, 0.0 is silence.
"""
import math

# Part B: your attenuation design. (name, curve, ref, max_d)
# curve is "inverse", "linear" or "tapered". Edit these rows for your game.
SOUNDS = [
    ("footstep_enemy", "linear", 2.0, 30.0),
    ("gunshot", "tapered", 5.0, 150.0),
    ("campfire_loop", "inverse", 1.0, 15.0),
]


def to_db(gain):
    """Amplitude gain to decibels: 20 * log10(gain). Returns -inf for gain <= 0."""
    if gain <= 0:
        return float("-inf")
    return 20 * math.log10(gain)


def inverse_gain(d, ref=1.0, rolloff=1.0):
    """Web Audio "inverse" model: ref / (ref + rolloff * (max(d, ref) - ref)).
    With rolloff = 1 this is ref / d outside the reference distance."""
    return ref / (ref + rolloff * (max(d, ref) - ref))


def linear_gain(d, ref, max_d, rolloff=1.0):
    """Web Audio "linear" model: 1 - rolloff * (clamp(d, ref, max_d) - ref) / (max_d - ref).
    Never returns less than 0. Assume max_d > ref."""
    # TODO (Part A, step 3)
    raise NotImplementedError


def tapered_gain(d, ref, max_d):
    """Our inverse-tapered model: the smaller of inverse_gain(d, ref) and
    linear_gain(d, ref, max_d) squared. Realistic near the source, silent at max_d."""
    # TODO (Part A, step 4)
    raise NotImplementedError


def gain_for(curve, d, ref, max_d):
    """Dispatch on the curve name used in SOUNDS."""
    if curve == "inverse":
        return inverse_gain(d, ref)
    if curve == "linear":
        return linear_gain(d, ref, max_d)
    if curve == "tapered":
        return tapered_gain(d, ref, max_d)
    raise ValueError(curve)


def audible_radius(gain_fn, threshold_db, far=100000.0):
    """Smallest distance d at which to_db(gain_fn(d)) <= threshold_db, found by
    bisection to within 0.001. gain_fn takes one argument (distance) and must
    not increase with distance. Return math.inf if even gain_fn(far) is above
    the threshold."""
    # TODO (Part A, step 5)
    raise NotImplementedError


def pan_gains(listener, right, source):
    """Equal-power stereo gains (left, right) for a source heard by a listener.
    listener, right and source are (x, y) tuples; right is the listener's
    right-hand direction (any length). Pan p is the dot product of the unit
    vector from listener to source with the unit right vector, so p = 1 is hard
    right and p = -1 hard left. Then a = (p + 1) / 2, left = cos(a * pi / 2),
    right = sin(a * pi / 2). A source exactly at the listener is centred."""
    # TODO (Part C, step 9)
    raise NotImplementedError


def main():
    try:
        _report()
    except NotImplementedError:
        print("Some functions are still TODO. Run the tests to see which.")


def _report():
    print("Curves with ref = 1, max_d = 32 (dB)")
    print(f"{'d':>5} {'inverse':>9} {'linear':>9} {'tapered':>9}")
    for d in (1, 2, 4, 8, 16, 24, 28, 31, 32):
        row = [to_db(g(d)) for g in (lambda d: inverse_gain(d, 1),
                                       lambda d: linear_gain(d, 1, 32),
                                       lambda d: tapered_gain(d, 1, 32))]
        print(f"{d:>5} " + " ".join(f"{v:>9.1f}" for v in row))
    print()
    print("Your sounds: distance where each falls to -20 dB and -40 dB")
    for name, curve, ref, max_d in SOUNDS:
        fn = lambda d, c=curve, r=ref, m=max_d: gain_for(c, d, r, m)
        r20, r40 = audible_radius(fn, -20), audible_radius(fn, -40)
        print(f"{name:<16} {curve:<8} ref {ref:>5} max {max_d:>6}  "
              f"-20 dB at {r20:8.1f}  -40 dB at {r40:8.1f}")


if __name__ == "__main__":
    main()
