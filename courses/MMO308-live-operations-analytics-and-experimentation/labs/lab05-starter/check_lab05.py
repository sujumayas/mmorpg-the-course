"""MMO308 Lab 05 checker. Run after gen_servers.py:  python check_lab05.py"""
import sys

import design as d

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


TESTS = {
    "bucket": lambda: all(close(d.bucket(i, "lab05-test"), v) for i, v in (
        (1, 0.18216529007352786), (2, 0.3826000687251366), (3, 0.5839944101367013))),
    "variant": lambda: (
        sum(d.variant(i, "lab05-test") == "B" for i in range(50_000)) == 24_993
        and d.variant(1, "lab05-test", share_b=0.1) == "A"
        and d.variant(1, "lab05-test", share_b=0.2) == "B"),
    "design_effect": lambda: close(d.design_effect(5000, 0.01), 50.99)
        and close(d.design_effect(1, 0.3), 1.0),
    "effective_n": lambda: close(d.effective_n(100_000, 20, 0.05), 100_000 / 1.95),
    "mde": lambda: close(d.mde(0.3, 1961), 0.04100076662011361),
    "icc_from_clusters": lambda: close(
        d.icc_from_clusters(*d.load_history()), 0.007437825450626649)
        and d.icc_from_clusters([1000, 1000], [300, 300]) == 0.0,
}


def main():
    ok = True
    for name, test in TESTS.items():
        try:
            passed = bool(test())
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
