"""Run with:  python test_lab07.py   (from inside lab07-starter/)"""
import scene_tree as s


def names(nodes):
    return [n.name for n in nodes]


def tree():
    return s.build_lecture_tree()


def test_pre_order():
    assert names(s.pre_order(tree())) == ["Main", "Player", "Sprite", "HealthBar", "Enemy"]


def test_post_order():
    assert names(s.post_order(tree())) == ["Sprite", "HealthBar", "Player", "Enemy", "Main"]


def test_check_yourself_tree():
    level = s.Node("Level")
    level.add(s.Node("HUD"))
    world = level.add(s.Node("World"))
    world.add(s.Node("Player"))
    coins = world.add(s.Node("Coins"))
    coins.add(s.Node("Coin1")); coins.add(s.Node("Coin2"))
    assert names(s.post_order(level)) == ["HUD", "Player", "Coin1", "Coin2", "Coins", "World", "Level"]
    assert names(s.pre_order(level)) == ["Level", "HUD", "World", "Player", "Coins", "Coin1", "Coin2"]


def test_priority_order():
    t = tree()
    t.children[0].children[1].priority = 10      # HealthBar runs last
    t.children[1].priority = -1                  # Enemy runs first
    assert names(s.process_order(t)) == ["Enemy", "Main", "Player", "Sprite", "HealthBar"]


def _pair(bar_first, fps=60, speed=300):
    enemy = s.Mover("Enemy", speed)
    bar = s.Follower("Bar", enemy)
    main = s.Node("Main", [bar, enemy] if bar_first else [enemy, bar])
    return main, enemy, bar


def test_gap_wrong_order():
    main, enemy, bar = _pair(True)
    s.run_frames(main, 3, 60)
    assert abs(enemy.x - 15.0) < 1e-9, enemy.x
    assert abs((enemy.x - bar.x) - 5.0) < 1e-9


def test_gap_right_order():
    main, enemy, bar = _pair(False)
    s.run_frames(main, 3, 60)
    assert abs(enemy.x - bar.x) < 1e-9


def test_priority_fixes_gap():
    main, enemy, bar = _pair(True)
    bar.priority = 1
    s.run_frames(main, 5, 144)
    assert abs(enemy.x - bar.x) < 1e-9


def test_lag_chain():
    enemy = s.Mover("Enemy", 300)
    bar = s.Follower("Bar", enemy)
    label = s.Follower("Label", bar)
    worst = s.Node("Main", [label, bar, enemy])
    assert s.lag_frames(worst, label) == 2
    assert s.lag_frames(worst, bar) == 1
    mixed = s.Node("Main", [label, enemy, bar])
    assert s.lag_frames(mixed, label) == 1
    best = s.Node("Main", [enemy, bar, label])
    assert s.lag_frames(best, label) == 0


def test_predicted_gap_table():
    assert abs(s.predicted_gap(1, 300, 30) - 10.0) < 1e-9
    assert abs(s.predicted_gap(1, 300, 144) - 2.0833) < 1e-3
    assert abs(s.predicted_gap(2, 300, 144) - 4.1667) < 1e-3


def test_measured_matches_predicted():
    enemy = s.Mover("Enemy", 450)
    bar = s.Follower("Bar", enemy)
    label = s.Follower("Label", bar)
    main = s.Node("Main", [label, bar, enemy])
    s.run_frames(main, 10, 90)
    assert abs((enemy.x - label.x) - s.predicted_gap(s.lag_frames(main, label), 450, 90)) < 1e-9


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL  {t.__name__}: not implemented yet")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e or 'assertion failed'}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
