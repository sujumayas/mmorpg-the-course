"""AU101 Lab 14 tests. Do not edit.

    .venv/bin/python courses/AU101-audio-for-games/labs/lab14-starter/test_audio_budget.py [path/to/your_module.py]

With no argument the tests load audio_budget.py from this folder. Each test prints
PASS, FAIL or TODO. The script exits with status 1 unless every test passes.
"""
import importlib.util
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "audio_budget.py"
spec = importlib.util.spec_from_file_location("budget_under_test", target)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def close(x, y, tol=1e-6):
    return abs(x - y) <= tol * max(1.0, abs(y))


def group(codec="pcm", load="decompress", count=10, seconds=1.5, channels=2,
          rate=48000, bits=16, voices=6, name="weapons"):
    return {"name": name, "count": count, "seconds": seconds, "channels": channels,
            "rate": rate, "bits": bits, "codec": codec, "load": load, "voices": voices}


def test_pcm_bytes():
    assert close(a.pcm_bytes(44100, 16, 2, 1), 176_400), "CD audio, one second"
    assert close(a.pcm_bytes(11025, 8, 1, 1), 11_025), "Doom-era effects, one second"
    assert close(a.pcm_bytes(48000, 16, 1, 0.35), 33_600)
    assert close(a.group_pcm_bytes(group()), 2_880_000)


def test_disk_and_resident():
    assert close(a.disk_bytes(group(codec="adpcm", load="compressed")), 2_880_000 / 3.5)
    assert close(a.resident_bytes(group(codec="vorbis", load="decompress")), 2_880_000), \
        "a decompressed Vorbis clip costs full PCM memory"
    assert close(a.resident_bytes(group(codec="vorbis", load="compressed")), 288_000)
    music = group(codec="vorbis", load="stream", count=4, seconds=150, voices=2, name="music")
    assert close(a.resident_bytes(music), 400_000), "streams cost their buffers, not their length"
    assert close(a.disk_bytes(music), 11_520_000)


def test_cpu_and_streams():
    assert a.played_codec(group(codec="vorbis", load="decompress")) == "pcm"
    assert a.played_codec(group(codec="adpcm", load="compressed")) == "adpcm"
    assert close(a.cpu_percent(group(codec="adpcm", load="compressed")), 0.9)
    assert close(a.cpu_percent(group(codec="vorbis", load="compressed", voices=3)), 1.5)
    music = group(codec="vorbis", load="stream", count=4, seconds=150, voices=2, name="music")
    assert close(a.stream_read_rate(music), 38_400)
    assert a.stream_read_rate(group()) == 0
    assert [a.max_real_voices(8.0, c) for c in ("pcm", "adpcm", "vorbis")] == [80, 53, 16]


def test_evaluate_plans():
    plans = a.load_groups(HERE / "level_assets.csv")
    e = a.evaluate(plans["A all pcm decompress"], 32e6, 8.0)
    assert close(e["memory"], 188_726_400) and e["fits_memory"] is False
    e = a.evaluate(plans["B vorbis decompress"], 32e6, 8.0)
    assert close(e["memory"], 188_726_400) and close(e["disk"], 18_872_640)
    e = a.evaluate(plans["C vorbis compressed"], 32e6, 8.0)
    assert e["fits_memory"] is True and e["fits_cpu"] is False
    assert close(e["cpu"], 10.5) and e["voices"] == 21


TESTS = [test_pcm_bytes, test_disk_and_resident, test_cpu_and_streams, test_evaluate_plans]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except NotImplementedError:
            failed += 1
            print(f"TODO  {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL  {t.__name__}")
            traceback.print_exc(limit=1)
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
