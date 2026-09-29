"""Checks for MMO306 Lab 07. Run from this folder:  python test_lab07.py
Each check prints PASS or FAIL. A NotImplementedError counts as FAIL."""
import os
import tempfile
import traceback

import tuning as t

TINY = """pull,t,event,source,target,ability,amount
1,0.0,ENCOUNTER_START,,Warden,,0
1,20,CAST,Warden,,Cinder Wave,5
1,20.5,DEATH,Warden,P03,Cinder Wave,0
1,40,DAMAGE,raid,Warden,all,30000000
1,50,CAST,Warden,,Cinder Wave,5
1,60,CAST,Warden,,Falling Glass,3
1,60.5,DEATH,Warden,P07,Falling Glass,0
1,60.5,DEATH,Warden,P09,Falling Glass,0
1,80,DAMAGE,raid,Warden,all,34000000
1,80,ENCOUNTER_END,,Warden,,0
2,0.0,ENCOUNTER_START,,Warden,,0
2,200,DAMAGE,raid,Warden,all,190000000
2,400,DAMAGE,raid,Warden,all,190000000
2,400,DEATH,Warden,P01,Enrage,0
2,400,ENCOUNTER_END,,Warden,,0
3,0.0,ENCOUNTER_START,,Warden,,0
3,20,CAST,Warden,,Cinder Wave,5
3,200,DAMAGE,raid,Warden,all,230000000
3,385,DAMAGE,raid,Warden,all,210000000
3,385,ENCOUNTER_END,,Warden,,1
"""


def tiny_path():
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w") as f:
        f.write(TINY)
    return path


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_read_pulls():
    ps = t.read_pulls(tiny_path())
    assert [p["pull"] for p in ps] == [1, 2, 3]
    assert close(ps[0]["length"], 80) and ps[0]["damage"] == 64_000_000
    assert close(ps[0]["dps"], 800_000)
    assert ps[0]["first_death"] == "Cinder Wave" and ps[0]["deaths"]["Falling Glass"] == 2
    assert ps[1]["kill"] is False and close(ps[1]["dps"], 950_000)
    assert ps[2]["kill"] is True and ps[2]["first_death"] is None


def test_wipe_causes():
    causes = t.wipe_causes(t.read_pulls(tiny_path()))
    assert set(causes) == {"Cinder Wave", "Enrage"}
    assert close(causes["Cinder Wave"], 0.5) and close(causes["Enrage"], 0.5)


def test_deaths_per_100():
    rates = t.deaths_per_100(tiny_path())
    assert close(rates["Cinder Wave"], 100 / 15)       # 1 death in 15 exposures
    assert close(rates["Falling Glass"], 200 / 3)      # 2 deaths in 3 exposures


def test_survival():
    ps = t.read_pulls(tiny_path())
    assert close(t.survival(ps, 0), 1.0)
    assert close(t.survival(ps, 100), 2 / 3)
    assert close(t.survival(ps, 390), 1 / 3)


def test_kill_rate_lecture_sample():
    sample = [1380, 1290, 1210, 1160, 1120, 1080, 1060, 1050, 1020, 990,
              970, 940, 910, 890, 860, 830, 800, 760, 720, 650]
    sample = [d * 1000 for d in sample]
    assert close(t.kill_rate(sample, 440_000_000), 0.25)
    assert close(t.kill_rate(sample, 418_000_000), 0.40)
    assert close(t.kill_rate(sample, 396_000_000), 0.50)


def test_model_matches_lecture():
    assert abs(t.model_kill_rate(440e6, 1e6, 0.15) - 0.263) < 0.001
    assert abs(t.model_kill_rate(418e6, 1e6, 0.15) - 0.385) < 0.001
    assert abs(t.health_for_target(0.35, 1e6, 0.15) - 423.8e6) < 0.1e6


def test_fit_lognormal():
    m, s = t.fit_lognormal([1e6, 1e6 * 2.718281828459045])
    assert abs(m - 1e6 * 2.718281828459045 ** 0.5) < 1
    assert abs(s - 0.5) < 1e-6


def test_weighted_kill_rate():
    rows = [(1_200_000, 1), (1_100_000, 1), (900_000, 1), (800_000, 0), (1_300_000, 0)]
    rate = lambda d: 0.8 if d >= 1_000_000 else 0.2
    # weights: 1.25, 1.25, 5 -> share clearing 1,000,000 = 2.5 / 7.5
    assert close(t.weighted_kill_rate(rows, 400_000_000, rate), 1 / 3)


def test_dataset_numbers():
    ps = t.read_pulls("encounter_log.csv")
    assert len(ps) == 60 and sum(p["kill"] for p in ps) == 1
    causes = t.wipe_causes(ps)
    assert abs(causes["Enrage"] - 0.271) < 0.001
    rows = t.load_best_pulls("best_pulls.csv")
    assert abs(t.kill_rate([d for d, _ in rows], t.BOSS_H) - 0.230) < 0.001


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL {fn.__name__} (not implemented yet)")
        except Exception:
            print(f"FAIL {fn.__name__}")
            traceback.print_exc(limit=1)
    print(f"{passed}/{len(TESTS)} checks passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
