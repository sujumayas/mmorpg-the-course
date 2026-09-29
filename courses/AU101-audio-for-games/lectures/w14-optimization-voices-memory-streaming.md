# AU101 · Week 14 — Optimization: Voices, Memory, Streaming

**Why this matters:** Every sound you made this term has a price in memory, disk and CPU, and the platform gives audio a fixed share of each. Go over and the game stutters, crashes on a console with less RAM, or drops the one sound the player needed. The choices that decide the bill (codec, load type, sample rate, voice count) are yours, and they are made per sound, not per project.

**You will be able to:**
- Compute the uncompressed, on-disk and in-memory size of a sound or a group of sounds from its sample rate, bit depth, channels, length and codec.
- Choose a load type (decompress on load, compressed in memory, stream) for each group and justify it with memory and CPU numbers.
- Compute a CPU budget for real voices and the number of voices of each codec it allows.
- Build and defend an audio budget for a level that fits a memory limit and a CPU limit at the same time.

**Before class:** Unity Manual (Unity 6), "Audio Clip" import settings, the Load Type and Compression Format sections (15 minutes). Godot Engine documentation (4.x stable), "Importing audio samples", the first section on formats (10 minutes). Skim Rodrigo Copetti, "Super Nintendo Architecture: A Practical Analysis", the audio section.

**Prerequisites from earlier courses:** [AU101 week 1, what sound does in games](w01-what-sound-does-feedback-space-emotion.md) (a sound as frequency, amplitude, duration and position). [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (playing sounds from code). AU101 [week 4](w04-layering-and-variation.md) (variation), [week 6](w06-middleware-events-and-parameters.md) (middleware banks) and [week 10](w10-mixing-ducking-and-priority.md) (voice priority). Every variant you added in week 4 is now a line on the memory bill, and week 10's priority rules decide which voices survive a voice limit.

**Interactive:** [examples/w14-audio-budget.html](../examples/w14-audio-budget.html). Keep it open during section 2. It has a listening panel, so headphones help.

---

## 1. Three budgets, one mixer

When your game plays a sound, three resources get spent.

- **Memory.** The sound's sample data has to be somewhere the mixer can read it every few milliseconds. On a console or phone, audio gets a fixed slice of RAM that you agree on with the rest of the team early in production.
- **Disk.** The sound ships in the game's package and sits on the player's drive. Some of it is also read from disk while the game runs, if it streams.
- **CPU.** Every sound that is audible right now is a **voice**. Each voice costs CPU time in every audio block: the mixer resamples it to the output rate, applies volume, filters and 3D panning, and adds it into the mix. If the data is compressed, the mixer also has to decode it first.

The three trade against each other. Compressing a sound saves memory and disk and costs CPU every time it plays. Streaming a sound saves memory and costs disk reads and start-up delay. Limiting voices saves CPU and costs sounds the player never hears. There is no setting that is cheapest on all three. That is why this is a design topic and not a checkbox.

Three terms you will need.

- **Sample rate** `f_s` is how many samples per second the sound stores. A sound sampled at `f_s` can hold frequencies up to `f_s / 2`, the Nyquist limit. 48,000 Hz holds everything up to 24 kHz, above human hearing. 22,050 Hz holds up to about 11 kHz. That is fine for a footstep's thud and loses the sizzle of a cymbal.
- **Bit depth** `b` is how many bits each sample uses. 16-bit is standard. Each bit adds about 6 dB of range between the loudest sound and the noise floor, so 8-bit audio has an audible hiss under quiet sounds.
- **Codec** is how the samples are stored. **PCM** is raw samples, no compression. **ADPCM** stores each sample as a small difference from a prediction, about 3.5 times smaller than PCM in Unity, and cheap to decode. **Vorbis** is a perceptual codec, like MP3, that throws away what the ear is unlikely to notice. Unity puts it at about 10 times smaller, and it is the most expensive of the three to decode.

## 2. Worked example: the whole soundtrack in one second of audio

### The hook

Think of a Super Nintendo game you know, or look one up and listen. It has a full soundtrack with drums, strings and brass, plus jumps, coins, hits and menu sounds. The console's sound system had 64 KB of its own RAM for all of it: every instrument sample, every sound effect, and the sound driver program that played them. It mixed eight voices at 32 kHz.

64 KB here means 65,536 bytes. One second of CD-quality stereo audio is 176,400 bytes. The SNES had room for about a third of a second of CD audio, and every game on it had to fit its soundtrack and effects into that. How?

### The model

The size of any sound follows from four numbers and a codec.

```
PCM bytes      P = f_s × (b / 8) × c × t
stored bytes   S = P / r
```

- `f_s` is the sample rate in Hz, `b` the bit depth, `c` the number of channels (1 mono, 2 stereo), `t` the length in seconds.
- `r` is the codec's compression ratio: 1 for PCM, about 3.5 for ADPCM, about 10 for Vorbis (Unity's figures; Vorbis varies with the quality setting).

Where the bytes live depends on the **load type**. Unity names the three options Decompress On Load, Compressed In Memory and Streaming, and other engines and middleware offer similar choices under their own names.

```
decompress on load   memory = P        (decoded once, when the level loads)
compressed in memory memory = P / r    (decoded every time it plays)
stream               memory = voices × buffer    (read from disk while it plays)
```

And the CPU at the busiest moment is a sum over the voices that are playing:

```
CPU = Σ voices × (mix + decode[codec played])
```

A sound that was decompressed on load plays as PCM, whatever format it shipped in. That one line is the trap in this lecture. Keep it in mind.

### Numbers you can check: the hook

| Format | f_s (Hz) | b | c | Bytes per second | Seconds that fit in 65,536 bytes |
|---|---|---|---|---|---|
| CD audio | 44,100 | 16 | 2 | 176,400 | 0.37 |
| A modern 48 kHz stereo source | 48,000 | 16 | 2 | 192,000 | 0.34 |
| SNES native, uncompressed | 32,000 | 16 | 1 | 64,000 | 1.02 |
| SNES with BRR (9 bytes per 16 samples) | 32,000 | 16 | 1 | 18,000 | 3.64 |
| Doom effects (1993) | 11,025 | 8 | 1 | 11,025 | 5.94 |

Check the BRR row. BRR (bit rate reduction), the SNES's ADPCM format, packs 16 samples, which would be 32 bytes as 16-bit PCM, into 9 bytes. That is a ratio of `32 / 9 = 3.56`, almost exactly Unity's "about 3.5" for ADPCM thirty years later. At 32,000 samples per second, that is `32,000 × 9 / 16 = 18,000` bytes per second. So 64 KB holds about 3.6 seconds of sample material, before the driver program and the echo buffer take their share.

Three and a half seconds is still not a soundtrack. The rest of the answer is the fourth variable, `t`. SNES composers didn't store music. They stored a fraction of a second of each instrument, looped the sustained part, and played the notes from a sequence at different pitches, like a MIDI file driving a tiny sampler. A 0.2-second string sample, looped and pitched, can play a whole melody. The soundtrack was a program, not a recording.

### Numbers you can check: a level today

Now a level from an invented action game targeting a mid-range phone. The audio lead has agreed a budget: **32 MB of resident audio memory** and **8% of one CPU core** for the audio thread at the busiest moment. All sources are 48 kHz, 16-bit. In this lecture 1 MB is 1,000,000 bytes.

| Group | Count | Length each (s) | Channels | PCM size P | Peak voices |
|---|---|---|---|---|---|
| Footsteps (week 4 variants) | 24 | 0.35 | 1 | 0.81 MB | 6 |
| Weapons | 10 | 1.5 | 2 | 2.88 MB | 6 |
| UI | 30 | 0.25 | 1 | 0.72 MB | 2 |
| Ambience loops | 3 | 45 | 2 | 25.92 MB | 3 |
| Music tracks | 4 | 150 | 2 | 115.20 MB | 2 |
| Voice-over lines | 180 | 2.5 | 1 | 43.20 MB | 2 |
| **Total** | | | | **188.73 MB** | **21** |

Check weapons: `48,000 × 2 × 2 × 1.5 × 10 = 2,880,000` bytes. Music has 2 peak voices because a crossfade (week 9) plays the old and new track at once.

The CPU costs per voice are **invented** for this imaginary phone: mixing costs 0.10% of a core per voice, and decoding adds 0 for PCM, 0.05% for ADPCM and 0.40% for Vorbis. Only their order comes from the engines' documentation. Unity says PCM is light on the CPU and ADPCM is much lighter than Vorbis, and Godot says Vorbis needs much more processing power than its WAV formats. The real numbers depend on the platform, and you measure them with a profiler.

Four plans:

| Plan | Memory | Disk | CPU at peak | Verdict |
|---|---|---|---|---|
| A: everything PCM, decompress on load | 188.73 MB | 188.73 MB | 2.10% | over on memory |
| B: everything Vorbis, decompress on load | 188.73 MB | 18.87 MB | 2.10% | over on memory |
| C: everything Vorbis, compressed in memory | 18.87 MB | 18.87 MB | 10.50% | over on CPU |
| D: mixed, see below | 5.74 MB | 20.78 MB | 5.20% | fits both |

Plan B is the trap. Someone sets every file to Vorbis, sees the package drop from 189 MB to 19 MB, and assumes the memory problem is solved. It is not. Decompress on load turns every Vorbis file back into PCM when the level loads. Unity's manual warns that a decompressed Vorbis clip uses about ten times the memory of the compressed one. The disk shrank. The RAM didn't.

Plan C fixes memory and breaks CPU. All 21 peak voices now decode Vorbis in real time: `21 × (0.10 + 0.40) = 10.5%`. The frame where the player fires six shots while walking through a crossfade is the frame that stutters.

Plan D chooses per group:

| Group | Codec, load | Memory | CPU at peak | Why |
|---|---|---|---|---|
| Footsteps | PCM, decompress | 0.81 MB | 0.60% | Short, frequent, many at once. Cheap in memory whatever you do, so pay nothing in CPU. |
| Weapons | ADPCM, compressed | 0.82 MB | 0.90% | Noisy transients hide ADPCM's small errors. Unity recommends ADPCM for exactly this kind of sound. |
| UI | PCM, decompress | 0.72 MB | 0.20% | Tiny and must start instantly. |
| Ambience | Vorbis, compressed | 2.59 MB | 1.50% | Long loops, few voices. |
| Music | Vorbis, stream | 0.40 MB | 1.00% | Huge and only two at once. Two stream buffers of about 200 KB each, Unity's figure. |
| Voice-over | Vorbis, stream | 0.40 MB | 1.00% | 180 lines, but at most two play at once. |

Total memory `0.81 + 0.82 + 0.72 + 2.59 + 0.40 + 0.40 = 5.74 MB`. Total CPU `0.6 + 0.9 + 0.2 + 1.5 + 1.0 + 1.0 = 5.2%`. Both fit, with room left for the next feature someone adds in the last month.

This program reproduces the plan table's memory and CPU columns:

```python
RATIO = {"pcm": 1.0, "adpcm": 3.5, "vorbis": 10.0}
DECODE = {"pcm": 0.0, "adpcm": 0.05, "vorbis": 0.40}   # % of a core per voice (invented)
MIX, STREAM_BUF = 0.10, 200_000                        # % per voice (invented), bytes

# group: (count, seconds, channels, peak voices), all 48 kHz 16-bit sources
groups = {"footsteps": (24, 0.35, 1, 6), "weapons": (10, 1.5, 2, 6),
          "ui": (30, 0.25, 1, 2), "ambience": (3, 45, 2, 3),
          "music": (4, 150, 2, 2), "vo": (180, 2.5, 1, 2)}

def cost(plan):
    mem = cpu = 0.0
    for name, (count, secs, ch, voices) in groups.items():
        codec, load = plan[name]
        pcm = count * 48_000 * 2 * ch * secs
        mem += {"decompress": pcm, "compressed": pcm / RATIO[codec],
                "stream": voices * STREAM_BUF}[load]
        played = "pcm" if load == "decompress" else codec
        cpu += voices * (MIX + DECODE[played])
    return mem / 1e6, cpu

every = lambda codec, load: {g: (codec, load) for g in groups}
plans = {"A: PCM, decompress": every("pcm", "decompress"),
         "B: Vorbis, decompress": every("vorbis", "decompress"),
         "C: Vorbis, compressed": every("vorbis", "compressed"),
         "D: mixed": {"footsteps": ("pcm", "decompress"), "weapons": ("adpcm", "compressed"),
                      "ui": ("pcm", "decompress"), "ambience": ("vorbis", "compressed"),
                      "music": ("vorbis", "stream"), "vo": ("vorbis", "stream")}}
for name, plan in plans.items():
    mem, cpu = cost(plan)
    ok = "fits" if mem <= 32 and cpu <= 8 else "OVER"
    print(f"{name:<22} memory {mem:7.2f} MB   cpu {cpu:5.2f}%   {ok}")
```

It prints:

```
A: PCM, decompress     memory  188.73 MB   cpu  2.10%   OVER
B: Vorbis, decompress  memory  188.73 MB   cpu  2.10%   OVER
C: Vorbis, compressed  memory   18.87 MB   cpu 10.50%   OVER
D: mixed               memory    5.74 MB   cpu  5.20%   fits
```

### A visual you can move

Open `examples/w14-audio-budget.html`. The top view is the memory bill: one stacked bar, one segment per group, against a dashed line at the budget. The bottom view is the CPU bill at the peak moment, drawn the same way. Each group has a codec menu, a load-type menu and a mono switch.

Start on preset B. The memory bar is far past the line and the CPU bar is short. Press preset C. The memory bar drops under the line, and the CPU bar shoots past its own. The two views pull in opposite directions, and no setting shared by every group satisfies both. Now build plan D one group at a time and watch each bar respond. Music is the fun one. Switching it from "compressed" to "stream" cuts its memory from 11.52 MB to 0.40 MB of buffers, about 11.1 MB freed, and costs nothing extra in CPU, because it decodes Vorbis either way.

Then open the listening panel. It plays a procedural test sound, a noise burst with a falling tone, rendered at 48,000, 32,000, 22,050 and 11,025 Hz and at 16 or 8 bits. Listen for what goes first. At 11,025 Hz the top of the noise burst is gone. At 8 bits there is hiss in the tail. That is Doom's format, and now you know what the numbers in the table cost your ears.

### Cross-game recognition

**Super Nintendo (1990s).** 64 KB of audio RAM, eight voices, 32 kHz, BRR at 3.56:1. In our terms the memory budget was tiny and fixed, `r` was fixed by the hardware, so composers cut `t`, with short looped instrument samples driven by a sequence. The voice budget was eight, fixed in silicon.

**Doom (id Software, 1993; linuxdoom 1.10 source release).** Sound effects are 8-bit samples at 11,025 Hz, so each second costs 11,025 bytes, a sixteenth of CD audio. The mixer has 8 internal channels, and the default config plays 3 effects at once. Each sound source gets one channel, so a new sound from a monster cuts off that monster's previous sound. When all channels are busy, a new sound takes the channel of a sound with equal or lower priority, or doesn't play at all. That is a voice budget with a priority rule, the same logic as week 10, in one short C function.

**Unity (Unity 6).** Exposes the whole model as import settings. Load Type is Decompress On Load, Compressed In Memory or Streaming. The manual gives the ratios (Vorbis about 10x, ADPCM about 3.5x) and the roughly 200 KB overhead per streaming clip. It also recommends ADPCM for noisy, frequent sounds like footsteps, impacts and weapons. The Audio settings then split voices into Max Real Voices, the ones actually mixed, and Max Virtual Voices, the ones tracked but silent. Each frame, the loudest voices are the real ones.

**Godot (4.x stable).** Same model, different words. WAV imports can stay raw or use IMA ADPCM or Quite OK Audio. The docs say hundreds of simultaneous WAV voices are fine, while Ogg Vorbis needs much more CPU to play back. The WAV import options include Force Mono, which the docs say halves the file, and Force Max Rate for lowering the sample rate.

Four systems across thirty years, one equation: bytes from `f_s × b/8 × c × t / r`, CPU from voices times per-voice cost.

## 3. Voices: real, virtual and how many

A game can ask for far more sounds than it can mix. An MMO town square (week 12) might have 200 players' footsteps, spells and emotes in range. The audio engine keeps a list of every sound that *should* be playing and splits it in two.

- **Real voices** are mixed this block. They cost the full per-voice CPU.
- **Virtual voices** are tracked but not mixed. The engine keeps their position and playback time, which costs almost nothing, so a sound that becomes audible again can come back at the right point in its timeline instead of starting over.

The number of real voices is a CPU budget in disguise. With a budget `B` and a per-voice cost of `mix + decode`, the most real voices you can afford is

```
N_real = floor(B / (mix + decode))
```

With this lecture's invented costs and an 8% budget, that is 80 PCM voices, 53 ADPCM voices or 16 Vorbis voices. This is why the codec choice for short, frequent sounds matters more than for music. Music has two voices. Footsteps in a crowd can have twenty.

Who gets to be real? Unity promotes the loudest voices each frame. Doom used priority alone. In your middleware project, the priorities and per-event instance limits from weeks 6 and 10 shape the same decision. Whatever the rule, test the busiest moment of your game with the voice counter visible. That is the moment when the rule decides what the player hears.

One more cost hides here. Every real voice that is 3D-positioned gets its own panning and filtering (week 7). A stereo file on a 3D source is usually wasted, because the engine positions it as a point anyway, and it doubles memory. Force 3D sounds to mono unless you have a specific reason.

## 4. Streaming: memory for disk

Streaming keeps only a small buffer in memory and reads the rest from disk while the sound plays. It is the right choice for long sounds with few voices: music, long ambience, voice-over, cinematics.

Its cost has three parts.

- **Read rate.** Each stream reads `f_s × b/8 × c / r` bytes per second. A 48 kHz stereo Vorbis stream at ratio 10 reads 19.2 KB per second. Plan D reads 57.6 KB per second at the peak. That is tiny for any modern drive, but it competes with textures and level data loading at the same time. On a spinning hard drive, every extra stream also adds seeks.
- **Buffer memory.** A fixed amount per playing stream, about 200 KB in Unity whether or not audio is loaded. Ten streams are 2 MB. That is why streaming is wrong for short sounds. A 0.35-second footstep is 33.6 KB as PCM, far smaller than one stream buffer.
- **Start delay.** The buffer has to fill from disk before the first sample plays. Music can wait for that. A gunshot tied to a button press can't. Anything that must start on the exact frame of an input should be in memory.

A rule of thumb that plan D follows: **stream if the sound is long and rare, keep it in memory if it is short or frequent, and decode it at load time only if it is also small.**

Week 6's banks add a level above this. You load and unload a bank of sounds with a level or a zone, so memory is a budget per area, not per game. The town bank and the dungeon bank don't need to be resident together. Loading a bank is a disk read too. Do it during a transition, not in the middle of combat.

## 5. Eyes-open design judgment

Three decisions to make on purpose.

**Where the quality goes.** Lowering the sample rate or bit depth saves memory without costing any CPU, but the loss is audible. A deep impact loses nothing at 24 kHz. A cymbal, glass, or anything with sizzle loses a lot. Use the listening panel as a guide. Cut the rate on sounds whose energy is low and keep it on sounds whose character is high. Unity and Godot both offer a sample-rate override for this.

**Where the variety goes.** Week 4 fixed the machine-gun effect by adding variants. Every variant is memory. Twenty-four footsteps at 0.35 seconds are cheap. Forty variants of a 3-second spell are 11.5 MB as mono PCM. Often the better answer is fewer recorded variants plus runtime pitch and volume randomization, which costs nothing in memory.

**When to measure.** Everything in this lecture's CPU columns was invented. Real costs depend on the platform's CPU, the codec implementation and the effects on each voice. The model tells you *which* numbers to measure: per-voice cost by codec, peak voice count, resident memory by group. The profiler gives you the values. Set the budget in the first month, measure the busiest scene every milestone, and treat going over the same way the graphics team treats frame time.

A final warning. It is easy to optimize the wrong thing. Plan A, all PCM, is the fastest possible plan on the CPU. On a PC with 16 GB of RAM and a small game, it might even be fine. Optimization means fitting the budget you have, not reaching the smallest number.

## In-class activity (25 minutes)

Pairs. Use the interactive and a spreadsheet.

1. **Tighter target (10 min).** Your game is ported to a handheld with **8 MB** of audio memory and **4.5%** CPU. Start from plan D. It still fits the memory, but its 5.20% CPU is over the new limit. Find a plan that fits both, changing only codecs, load types, sample rates and mono switches. Peak voice counts are fixed.
2. **Name the loss (5 min).** For each change you made, write what the player could hear or notice. "Ambience at 24 kHz mono: the rain loses some air, and the stereo width goes."
3. **One more feature (5 min).** The designer adds a 16-player emote party with 10 extra peak voices of 1-second stereo sounds. Price it in both budgets under your plan and say what you would cut.
4. **Swap (5 min).** Trade plans with another pair and find the change you would reverse first.

Expected output: a filled budget table, one list of audible costs, and the price of the emote party. There is more than one plan that fits without cutting any peak voices.

## Common misconceptions

- **"Vorbis makes the game use less memory."** Only if it stays compressed in memory or streams. Decompress on load turns it back into PCM. The package shrinks, the RAM doesn't.
- **"Streaming is always cheaper."** It saves memory for long sounds and costs a buffer, disk reads and start delay per voice. For short or frequent sounds it costs more than it saves.
- **"More voices is always better."** Past the point where the mix is clear, extra voices add CPU and mud. Week 10's priority and this week's voice budget work together.
- **"Uncompressed means best quality, so ship everything as PCM."** PCM is best for CPU and start time. At 48 kHz and 16 bits, a well-set Vorbis file is transparent for most listeners, and memory is often the budget you run out of first.

## Check yourself

1. A 2-second stereo explosion at 48 kHz, 16-bit. What is its PCM size? Its ADPCM size? What does it occupy in memory as Vorbis set to decompress on load?
2. You have 4 MB for voice-over and 600 lines averaging 3 seconds, mono. Can you keep them compressed in memory as Vorbis at 48 kHz? At 24 kHz? Or must they stream?
3. With this lecture's invented costs, a game has a 6% CPU budget and wants 30 real footstep voices. Which codecs make that possible?
4. A teammate streams all 30 UI sounds "to save memory." Compute the memory before (PCM, decompress, 0.25 s mono at 48 kHz each, 2 peak voices) and after (streaming, 2 peak voices). Give two more reasons it is a bad idea.
5. Why did SNES soundtracks sound like sequenced instruments rather than recordings? Answer with the model's variables.

<details>
<summary>Answers</summary>

1. `P = 48,000 × 2 × 2 × 2 = 384,000` bytes, 384 KB. ADPCM `384,000 / 3.5 ≈ 110 KB`. Vorbis decompress on load occupies the full PCM size, 384 KB, whatever the file size on disk.
2. At 48 kHz, PCM is `48,000 × 2 × 1 × 3 × 600 = 172.8 MB`, and Vorbis in memory is about 17.3 MB, too big. At 24 kHz it halves to about 8.6 MB, still too big. Stream them: two peak voices cost about 0.4 MB of buffers.
3. Per-voice costs are 0.10% (PCM), 0.15% (ADPCM), 0.50% (Vorbis). `30 × 0.10 = 3.0%` and `30 × 0.15 = 4.5%` fit in 6%. `30 × 0.50 = 15%` doesn't. PCM or ADPCM.
4. Before: `30 × 48,000 × 2 × 0.25 = 720,000` bytes, 0.72 MB. After: `2 × 200 KB = 0.4 MB`. It saves 0.32 MB, but each UI sound now waits for a buffer to fill before it plays, which makes the menu feel laggy (week 11). It also adds disk reads during menus that may be loading other data. Keep UI in memory.
5. Memory was fixed at 64 KB and `r` was fixed at 3.56 by BRR, so the only variable left was `t`. Composers stored a fraction of a second of each instrument, looped it, and let a sequence play the notes at different pitches. A recording has a large `t`. A sequence reuses a small `t` many times.

</details>

## Lab / assignment hook

[Lab 14, an audio budget you can defend](../labs/lab14.md). You implement this lecture's memory, disk, CPU and streaming model in Python, check the three trap plans against it, build a plan that fits the handheld target from the in-class activity, and write the budget sheet for your own week 15 game slice. The sheet is a required appendix to the final sound pass.

## Sources

- Wikipedia, "Super Nintendo Entertainment System", section on audio (accessed September 2026). S-SMP audio subsystem with a DSP, an 8-bit SPC700 CPU and 64 KB of dedicated RAM; eight voices of BRR-compressed 16-bit samples with echo; the article uses binary kilobytes. Wikipedia, "Bit Rate Reduction": sixteen 16-bit samples into 9 bytes, 3.56:1, a form of ADPCM.
- Copetti, R. (2019), "Super Nintendo Architecture: A Practical Analysis" (copetti.org). The S-DSP plays ADPCM samples on eight channels at 16 bits and 32 kHz; 64 KB of PSRAM holds audio data and programs; echo uses part of that memory.
- id Software, DOOM source code, `linuxdoom-1.10` (source release, 1997, of the 1993 game), GitHub id-Software/DOOM. `i_sound.c`: `SAMPLERATE 11025`, `NUM_CHANNELS 8`, 8-bit unsigned samples padded with value 128. `m_misc.c`: default `snd_channels` of 3. `s_sound.c`, `S_getChannel`: one channel per origin, and a new sound displaces an equal-or-lower-priority one or is dropped.
- Unity Technologies, Unity Manual (Unity 6), "Audio Clip" (accessed September 2026). Load types; Vorbis decompressed on load uses about ten times the memory of compressed, ADPCM about 3.5 times; streaming clips have about 200 KB overhead; ADPCM recommended for noisy, frequent sounds; PCM light on CPU; sample rate override. Unity Manual, "Audio" project settings: Max Virtual Voices and Max Real Voices, with the loudest voices picked each frame.
- Godot Engine documentation (4.x stable), "Importing audio samples" (accessed September 2026). WAV with IMA ADPCM or Quite OK Audio, hundreds of simultaneous WAV voices fine; Ogg Vorbis smaller and much more CPU to play back; MP3 between them; Force Mono halves size; Force Max Rate.
- Collins, K. (2008). *Game Sound*. MIT Press. Chapters 2 and 3 on the technical history of game audio.

## Interactive spec: examples/w14-audio-budget.html

**Purpose.** Show that memory and CPU pull in opposite directions when you choose a codec and load type, that no single setting for every group fits both budgets, and that a per-group plan does. Let the student hear what sample rate and bit depth reductions cost.

**The one insight the visual must make obvious.** Pressing preset B, then preset C, makes the memory bar and the CPU bar swap which one is over budget. B shows 188.73 MB against a 32 MB line with CPU at 2.10%. C shows 18.87 MB with CPU at 10.50% against an 8% line. Preset D brings both under their lines (5.74 MB, 5.20%).

**Layout.** Two linked views stacked on phones (390px), side by side at 1024px and wider, with the group table below and the listening panel last.

- **Top, "Memory".** One horizontal stacked bar, one segment per group in six distinguishable colours with a text label in or beside each segment, scaled so that the axis reaches max(200 MB, total × 1.1). A vertical dashed line at the memory budget, labelled "budget 32 MB". A readout above: "Resident memory 5.74 MB of 32 MB · package 20.78 MB". If over, the readout says "OVER by X MB" in text, not colour alone.
- **Bottom, "CPU at peak".** Same design for CPU percent: segments per group, dashed line at the CPU budget, axis to max(12%, total × 1.1). Readout "CPU 5.20% of 8% · 21 real voices · stream reads 57.6 KB/s".
- **Group table.** One row per group: name, count, length, channels (with a "mono" switch that sets channels to 1), sample rate menu (48,000 / 32,000 / 24,000 / 22,050 / 11,025), codec menu (PCM / ADPCM / Vorbis), load menu (Decompress on load / Compressed in memory / Stream), peak voices (number input, 0 to 40), and computed columns for PCM MB, resident MB and CPU %. Changing anything updates both bars immediately.
- **Presets.** Buttons A, B, C, D, and "Handheld" (sets budgets to 8 MB and 4.5% without changing the plan). Budgets are also editable number inputs.
- **Listening panel.** Buttons for 48,000 / 32,000 / 22,050 / 11,025 Hz and a 16-bit / 8-bit toggle, plus "Play". Beside it, a small spectrum drawn from an AnalyserNode during playback, so the missing top end is visible as well as audible.

**Data and defaults.** Groups, all 48,000 Hz, 16-bit sources: footsteps (24, 0.35 s, 1 ch, 6 voices), weapons (10, 1.5 s, 2 ch, 6), ui (30, 0.25 s, 1 ch, 2), ambience (3, 45 s, 2 ch, 3), music (4, 150 s, 2 ch, 2), vo (180, 2.5 s, 1 ch, 2). Default state is preset B with budgets 32 MB and 8%.

**Formulas.** P = count × f_s × 2 × c × t bytes (b = 16 throughout the budget view). Ratio r: PCM 1, ADPCM 3.5, Vorbis 10. Package = P / r. Resident: decompress P; compressed P / r; stream voices × 200,000. Played codec = PCM if load is decompress, else codec. CPU = voices × (0.10 + decode), decode PCM 0, ADPCM 0.05, Vorbis 0.40. Stream read rate = voices × f_s × 2 × c / r for stream groups. 1 MB = 1,000,000 bytes. Show MB to two decimals and CPU to two decimals. Label the CPU costs on screen as "invented for this example; measure your platform".

**Test values.**
- A: 188.73 MB, package 188.73 MB, CPU 2.10%.
- B: 188.73 MB, package 18.87 MB, CPU 2.10%.
- C: 18.87 MB, package 18.87 MB, CPU 10.50%.
- D (footsteps PCM decompress, weapons ADPCM compressed, ui PCM decompress, ambience Vorbis compressed, music Vorbis stream, vo Vorbis stream): 5.74 MB, package 20.78 MB, CPU 5.20%, stream reads 57.6 KB/s.
- D with ambience changed to ADPCM compressed, mono, 24,000 Hz: 5.00 MB, CPU 4.15%, which fits the Handheld budgets.
- Weapons group alone, 10 × 1.5 s stereo at 48 kHz: P = 2.88 MB.

**Listening panel audio (Web Audio, procedural only).** Build the test sound once at 48,000 Hz as a Float32Array, 1.2 s long: white noise with an exponential decay (time constant 0.15 s) plus a sine sweep from 6,000 Hz down to 200 Hz over 1.0 s at amplitude 0.3, with a 5 ms fade in and 50 ms fade out. For a chosen rate, create an AudioBuffer at that sample rate (the Web Audio API accepts rates from 8,000 Hz up) and fill it by averaging the 48 kHz samples that fall in each output sample's window, a simple low-pass before decimation. For 8-bit, quantize each sample to 256 levels, `round((x + 1) × 127.5) / 127.5 − 1`. Play at gain 0.5. The AudioContext starts only on the first press. Under prefers-reduced-motion the spectrum is drawn once, not animated.

**Accessibility of the example itself.** Native selects and inputs with labels. Bars have text readouts, and over-budget states are written in words. Keyboard order: presets, budgets, table rows, listening panel.
