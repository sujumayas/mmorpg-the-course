"""CS101 lab 14 tests. Run: python test_lab14.py"""
import random

import juice as J


def seconds_until_calm(fps, amount=0.5):
    tr = J.Trauma(decay=0.8)
    tr.add(amount)
    frames = 0
    while tr.value > 0 and frames < 10_000:
        tr.update(1 / fps)
        frames += 1
    return frames / fps


def test_trauma_clamps_high():
    tr = J.Trauma()
    tr.add(0.7)
    tr.add(0.7)
    assert tr.value == 1.0, f"trauma is {tr.value}, should clamp at 1.0"


def test_trauma_clamps_low():
    tr = J.Trauma()
    tr.add(0.1)
    for _ in range(100):
        tr.update(1 / 60)
    assert tr.value == 0.0, f"trauma is {tr.value}, should stop at 0.0"


def test_decay_is_frame_rate_independent():
    t30, t60, t144 = (seconds_until_calm(f) for f in (30, 60, 144))
    # Model: 0.5 / 0.8 = 0.625 s, plus at most one frame of rounding.
    for fps, t in ((30, t30), (60, t60), (144, t144)):
        assert 0.62 <= t <= 0.625 + 1 / fps + 1e-9, f"{fps} fps calmed after {t:.3f} s"


def test_shake_is_squared():
    tr = J.Trauma(power=2)
    tr.add(0.5)
    assert abs(tr.shake() - 0.25) < 1e-12, tr.shake()


def test_noise_is_smooth_and_repeatable():
    a = [J.value_noise(3, i / 100) for i in range(300)]
    b = [J.value_noise(3, i / 100) for i in range(300)]
    assert a == b, "same seed and x must give the same noise"
    biggest_step = max(abs(a[i] - a[i - 1]) for i in range(1, len(a)))
    assert biggest_step < 0.1, f"noise jumped {biggest_step:.3f} between close x values"


def test_emitter_rate_matches_model():
    rng = random.Random(8)
    em = J.Emitter(rate=40, lifetime=0.5)
    for _ in range(144 * 2):  # 2 seconds at 144 fps
        em.update(1 / 144, rng)
    alive = len(em.particles)
    assert 18 <= alive <= 22, f"{alive} alive, model says 40 x 0.5 = 20"


def test_emitter_same_at_30_and_144_fps():
    counts = []
    for fps in (30, 144):
        rng = random.Random(8)
        em = J.Emitter(rate=60, lifetime=1.5)
        for _ in range(fps * 5):
            em.update(1 / fps, rng)
        counts.append(len(em.particles))
    assert abs(counts[0] - counts[1]) <= 3, f"30 fps: {counts[0]}, 144 fps: {counts[1]}"


def test_dead_particles_removed():
    rng = random.Random(1)
    em = J.Emitter(rate=0, lifetime=0.3)
    em.burst(rng, 25)
    for _ in range(30):  # 0.5 s at 60 fps
        em.update(1 / 60, rng)
    assert len(em.particles) == 0, f"{len(em.particles)} particles outlived their lifetime"


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
    print(f"{passed}/{len(TESTS)} tests passed")
