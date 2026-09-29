"""Checker for GD201 Lab 04. Do not edit. Run: python check_lab04.py"""
import sys

import landmark as lm

V90 = 58.715507  # vertical FOV for 90 deg horizontal at 16:9


def zone_matrix(h_fov, fog=None):
    landmarks, starts = lm.load_zone()
    return lm.legibility_matrix(landmarks, starts, lm.vertical_fov(h_fov), 0.02, fog)


CHECKS = [
    ("vertical_fov(90) == 58.72", lambda: lm.vertical_fov(90), 58.72, 0.01),
    ("vertical_fov(60) == 35.98", lambda: lm.vertical_fov(60), 35.98, 0.01),
    ("screen_fraction(50, 2000, V90) == 0.02222", lambda: lm.screen_fraction(50, 2000, V90), 0.022222, 1e-5),
    ("screen_fraction(50, 100, V90) * 1080 == 480", lambda: lm.screen_fraction(50, 100, V90) * 1080, 480.0, 0.01),
    ("max_distance(50, 0.02, V90) == 2222.2", lambda: lm.max_distance(50, 0.02, V90), 2222.2, 0.1),
    ("max_distance(100, 0.02, V90, fog=2000) == 2000", lambda: lm.max_distance(100, 0.02, V90, fog=2000), 2000.0, 1e-6),
    ("required_height(3600, 0.02, V90) == 81", lambda: lm.required_height(3600, 0.02, V90), 81.0, 0.01),
    ("relative_luminance((235, 200, 140)) == 0.6086", lambda: lm.relative_luminance((235, 200, 140)), 0.6086, 1e-4),
    ("relative_luminance((0, 0, 0)) == 0", lambda: lm.relative_luminance((0, 0, 0)), 0.0, 1e-9),
    ("contrast_ratio(lit door, wall) == 7.02", lambda: lm.contrast_ratio((235, 200, 140), (60, 58, 66)), 7.02, 0.01),
    ("contrast_ratio is symmetric", lambda: lm.contrast_ratio((60, 58, 66), (235, 200, 140)), 7.02, 0.01),
    ("contrast_ratio(white, black) == 21", lambda: lm.contrast_ratio((255, 255, 255), (0, 0, 0)), 21.0, 1e-6),
    ("sample zone, 90 deg: West camp sees nothing",
     lambda: zone_matrix(90)["West camp"], [], None),
    ("sample zone, 90 deg: North ridge sees Weenie spire, Mill tower",
     lambda: zone_matrix(90)["North ridge"], ["Weenie spire", "Mill tower"], None),
    ("sample zone, 90 deg: Harbor gate sees Lighthouse only",
     lambda: zone_matrix(90)["Harbor gate"], ["Lighthouse"], None),
    ("sample zone, 60 deg: Harbor gate sees Weenie spire, Lighthouse",
     lambda: zone_matrix(60)["Harbor gate"], ["Weenie spire", "Lighthouse"], None),
    ("sample zone, 90 deg, fog 1000: Bridge sees Mill tower only",
     lambda: zone_matrix(90, fog=1000)["Bridge"], ["Mill tower"], None),
    ("sample zone, 60 deg: West camp sees Weenie spire, Mill tower",
     lambda: zone_matrix(60)["West camp"], ["Weenie spire", "Mill tower"], None),
]


def main():
    passed = 0
    for label, fn, want, tol in CHECKS:
        try:
            got = fn()
            ok = got == want if tol is None else abs(got - want) <= tol
        except NotImplementedError as e:
            got, ok = f"not implemented ({e})", False
        except Exception as e:  # show the student what broke
            got, ok = f"{type(e).__name__}: {e}", False
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + ("" if ok else f"   got {got}"))
    print(f"{passed}/{len(CHECKS)} checks pass")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
