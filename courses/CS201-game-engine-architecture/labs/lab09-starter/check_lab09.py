"""Checks for CS201 Lab 09. Run from this folder:  python check_lab09.py
Each check prints PASS, FAIL (with the reason) or TODO. Exit code 0 only if all pass."""
import sys

import input_layer as il
from input_layer import Event

results = []


def check(name):
    def wrap(fn):
        try:
            fn()
            results.append(("PASS", name, ""))
        except NotImplementedError as e:
            results.append(("TODO", name, str(e)))
        except AssertionError as e:
            results.append(("FAIL", name, str(e)))
        except Exception as e:  # a crash is a failure too
            results.append(("FAIL", name, f"{type(e).__name__}: {e}"))
        return fn
    return wrap


def downs(events):
    out = {}
    for e in events:
        if e.kind == "down":
            out[e.key] = out.get(e.key, 0) + 1
    return out


@check("A1 a tap inside one frame is seen")
def _():
    f = il.InputFrame()
    f.begin_frame()
    for e in [Event(1_000, "move", dx=4), Event(12_000, "down", "space"),
              Event(15_000, "move", dx=6, dy=-1), Event(22_000, "up", "space"),
              Event(30_000, "move", dx=5, dy=1)]:
        f.apply(e)
    assert not f.held("space"), "space is up at the end of the frame"
    assert f.just_pressed("space") and f.presses("space") == 1 and f.releases("space") == 1
    assert f.mouse == (15, 0), f"mouse motion must be summed, got {f.mouse}"


@check("A2 begin_frame keeps held keys and clears counts")
def _():
    f = il.InputFrame()
    f.begin_frame()
    f.apply(Event(0, "down", "w"))
    f.apply(Event(5, "move", dx=3, dy=3))
    f.begin_frame()
    assert f.held("w"), "w is still held in the next frame"
    assert f.presses("w") == 0 and not f.just_pressed("w"), "presses are per frame"
    assert f.mouse == (0, 0), "mouse motion is per frame"


@check("A3 press, release, press in one frame")
def _():
    f = il.InputFrame()
    f.begin_frame()
    for e in [Event(1, "down", "a"), Event(2, "up", "a"), Event(3, "down", "a")]:
        f.apply(e)
    assert (f.held("a"), f.presses("a"), f.releases("a")) == (True, 2, 1)


@check("A4 focus_lost releases everything")
def _():
    f = il.InputFrame()
    f.begin_frame()
    f.apply(Event(1, "down", "w"))
    f.apply(Event(2, "down", "shift"))
    f.begin_frame()
    f.apply(Event(3, "focus_lost"))
    assert not f.held("w") and not f.held("shift"), "no key may stay held after focus loss"
    assert f.releases("w") == 1 and f.releases("shift") == 1


@check("A5 event_presses loses nothing at any frame rate")
def _():
    events = il.load_session("session.csv")
    truth = downs(events)
    for frame_us in (100_000, 33_333, 16_667, 6_944):
        got = il.event_presses(events, frame_us)
        assert got == truth, f"at frame {frame_us} us: {got} != {truth}"
    s30 = il.sampled_presses(events, 33_333)
    assert sum(s30.values()) < sum(truth.values()), "sanity: sampling should lose taps at 30 fps"


@check("B1 action_for and ambiguity")
def _():
    m = il.ActionMap({"jump": ["space", "j"], "attack": ["k"]})
    assert m.action_for("j") == "jump" and m.action_for("k") == "attack"
    assert m.action_for("x") is None
    bad = il.ActionMap({"jump": ["space"], "dodge": ["space"]})
    try:
        bad.action_for("space")
    except ValueError as e:
        assert "jump" in str(e) and "dodge" in str(e), "name both actions"
    else:
        raise AssertionError("two actions on one key must raise ValueError")


@check("B2 rebind moves a key and reports the loser")
def _():
    m = il.ActionMap({"jump": ["space"], "attack": ["k"], "interact": ["e"]})
    assert m.rebind("jump", "space", "j") is None
    assert m.action_for("j") == "jump" and m.action_for("space") is None
    lost = m.rebind("attack", "k", "e")
    assert lost == "interact", f"interact lost 'e', got {lost}"
    assert m.action_for("e") == "attack" and m.bindings["interact"] == []
    try:
        m.rebind("fly", "f", "g")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown action must raise ValueError")


def make_stack():
    game = il.Context("gameplay", il.ActionMap({"move_forward": ["w"], "open_chat": ["enter"]}))
    chat = il.Context("chat", il.ActionMap({"send": ["enter"], "close": ["escape"]}), eats_everything=True)
    r = il.Router()
    r.push(game)
    return r, game, chat


@check("C1 the stuck-key scenario")
def _():
    r, game, chat = make_stack()
    r.route("down", "w")
    r.route("down", "enter")
    r.push(chat)
    r.route("up", "enter")
    r.route("up", "w")
    assert game.held == set(), f"gameplay still holds {sorted(game.held)}"
    r.route("down", "w")
    assert chat.log[-1] == ("down", "w"), "with chat on top, a new W press is text for chat"


@check("C2 pop releases what the popped context owns")
def _():
    r, game, chat = make_stack()
    r.push(chat)
    r.route("down", "a")
    r.route("down", "b")
    r.pop()
    assert r.stack == [game], "chat must be removed"
    assert chat.log[-2:] == [("up", "a"), ("up", "b")], f"chat must get ups for a, b; log {chat.log}"
    r.route("up", "a")
    assert game.log == [], "the real up for a has no owner any more and is dropped"


@check("C3 focus_lost releases every owned key")
def _():
    r, game, chat = make_stack()
    r.route("down", "w")
    r.push(chat)
    r.route("down", "x")
    r.focus_lost()
    assert game.held == set() and chat.held == set()
    assert game.log[-1] == ("up", "move_forward") and chat.log[-1] == ("up", "x")
    assert r.owner == {}


if __name__ == "__main__":
    width = max(len(n) for _, n, _ in results)
    for status, name, why in results:
        print(f"{status:4}  {name:<{width}}  {why}")
    passed = sum(s == "PASS" for s, _, _ in results)
    print(f"\n{passed}/{len(results)} checks pass")
    sys.exit(0 if passed == len(results) else 1)
