# CS201 · Week 01 — Engine Anatomy and Runtime Layers

**Why this matters:** An engine is tens of thousands of lines, sometimes millions, and nobody holds all of it in their head. What makes it workable is a rule about who may call whom. Get that rule right and you can port the game to a new console by rewriting a few percent of it. Get it wrong and every change to the window code breaks the inventory screen.

**You will be able to:**
- Sort an engine's modules into runtime layers and state the dependency rule the layers enforce.
- Compute the port size of a code base (the lines a porter must read and rewrite) and its port share from file sizes and include lists.
- Derive a subsystem start-up and shut-down order from a dependency list, and detect when no valid order exists.
- Redesign an upward dependency as a callback or queue so a lower layer no longer names a higher one.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), sections 1.3 "What Is a Game Engine?" and 1.6 "Runtime Engine Architecture", and section 6.1 "Subsystem Start-Up and Shut-Down". Skim the file list of the Doom source release on GitHub (`id-Software/DOOM`, folder `linuxdoom-1.10`) for five minutes. You don't need to read any C yet, just the file names.

**Prerequisites from earlier courses:** [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (inversion of control: the engine calls your code). [CS101 week 3, the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md). [CS102 week 9, the Component pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w09-pattern-component.md) (systems that run in a fixed order). [CS102 week 10, Observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (announcing without knowing who listens).

**Interactive:** [`examples/w01-port-size.html`](../examples/w01-port-size.html). Keep it open during section 2.

---

## 1. An engine is a stack of promises

In CS101 you used Godot. You wrote small scripts and the engine called them from inside its loop. This course opens the box. By week 14 you will have built a small engine in C++ that does the same job: it owns the loop, the memory, the entities, the hooks into rendering, the resources and a few tools.

Start with vocabulary. A **game engine** is the reusable part of a game: the code you would keep if you threw away this game's rules, levels and art and started the next one. Here is a practical test. If the code knows about "the player's double jump" or "the Goblin King," it is game code. If it knows about "meshes," "sounds" and "collision shapes" but not about what they mean in this game, it is engine code. Gregory points out that the line is blurry in real projects, and every studio draws it a little differently.

An engine has two halves. The **runtime** is what ships inside the game executable and runs on the player's machine. The **tools** are what the team runs at the studio: level editors, asset converters, profilers. This lecture is about the runtime. Week 14 covers tools.

### The layers

Gregory's runtime architecture diagram stacks an engine into layers. Simplified, from the bottom up:

| Layer | What lives there | Examples |
|---|---|---|
| Hardware, drivers, OS | Things you don't write | GPU driver, Windows, Linux, a console OS |
| Third-party SDKs | Libraries you link | a graphics API, a physics library, an audio library |
| Platform independence layer | Thin wrappers that hide the OS | open a window, read a file, get the time, create a thread |
| Core systems | Tools every other layer uses | memory allocators, containers, math, logging, assertions |
| Resources | Loading and caching assets | textures, meshes, sound banks, level files |
| Engine systems | The big subsystems | rendering, audio, physics, animation, input, networking |
| Gameplay foundations | The object model and scripting | entities and components, events, the script VM |
| Game-specific code | This game's rules | quests, classes, the Goblin King |

A **layer** is a group of modules at the same distance from the hardware. A **module** here means a group of source files that do one job, like "the renderer" or "the file system."

### The dependency rule

The layers exist to enforce one rule:

> Code in a layer may use code in its own layer or any layer below it. It may never name code in a layer above it.

"Use" and "name" mean concrete things in C++. If `renderer.cpp` includes `quest_log.h`, or calls `QuestLog::refresh()`, the renderer depends on the quest system. A **dependency** is any such compile-time or link-time reference. An **upward dependency** is one that points from a lower layer to a higher one. The rule bans them.

Why bother? Each benefit is a thing you can measure.

- **Portability.** If only the platform layer touches the OS, a port to a new OS rewrites only that layer. Section 2 puts a number on this.
- **Build time.** When you change a header, every file that includes it recompiles. Changing a gameplay header should never rebuild the renderer.
- **Testing.** You can test the memory allocator without a window, and the physics without a GPU, because they don't depend on those things.
- **Ownership.** On a team of 50, the audio programmer can change the audio module without reading the quest code, because the quest code can't reach into audio's internals, only through the audio API.

The rule is simple. Keeping it is hard, because breaking it is always the quickest fix on the day. The next section measures what a few quick fixes cost one of the most ported games ever made.

## 2. Worked example: how much of Doom do you rewrite to port it?

### The hook

Doom (id Software, 1993) was written on NeXT workstations and shipped on MS-DOS. In December 1997 id released the source of the Linux version. Since then, fan-made source ports have taken it to many operating systems id never supported. The README that came with the release says the code only runs on Linux, and in the same breath says it should be straightforward to bring it up on nearly any platform.

How can both be true? Code that runs on one OS, yet is easy to move to any OS? The answer is layering, and you can check it by counting.

### The model

Define the **port size** of a code base as the code a porter must read and rewrite to move it to a new platform:

```
port size = lines in files that touch the OS directly
port share   = port size / total lines
```

A file **touches the OS directly** if it includes an OS-specific header (`<unistd.h>`, `<X11/Xlib.h>`, `<windows.h>`, `<sys/socket.h>` and so on) or calls an OS function. If the dependency rule holds perfectly, the port size is exactly the platform layer. Every OS-specific include that leaks into a higher layer adds that whole file to the port size.

Doom's authors named files by module with a prefix, which makes the layers easy to see:

| Prefix | Module | Layer in the table above |
|---|---|---|
| `i_` | implementation: video, sound, network, timer, entry point | platform |
| `z_`, `w_`, `m_` | zone memory, WAD (data file) access, misc utilities | core and resources |
| `r_`, `v_`, `s_` | renderer, video buffers, sound mixing | engine systems |
| `p_` | "play": monsters, doors, lifts, collision | gameplay |
| `g_`, `d_` | game flow, the main loop and event handling | game-specific |

### Numbers you can check

I counted the lines in every `.c` and `.h` file in `linuxdoom-1.10`. You can repeat it with `wc -l *.c *.h` in that folder.

| Group | Files | Lines | Share of total |
|---|---|---|---|
| All source | 124 | 54,640 | 100% |
| `p_` gameplay | 27 | 15,170 | 27.8% |
| `r_` renderer | 19 | 6,811 | 12.5% |
| `i_` platform layer | 9 | 2,938 | 5.4% |

If the dependency rule held perfectly, a port would rewrite 5.4% of Doom. That is the promise of layering, and it is why the README can call the code portable.

Now search for OS headers outside the `i_` files. Run `grep -l "unistd\|fcntl\|sys/" *.c` and four non-platform files turn up, all including POSIX file headers (`<unistd.h>`, `<fcntl.h>`, `<sys/stat.h>`):

| File | Module | Lines | Why it touches the OS |
|---|---|---|---|
| `d_main.c` | main loop | 1,171 | checks which WAD files exist |
| `m_misc.c` | misc utilities | 534 | reads and writes files |
| `m_menu.c` | menus | 1,893 | checks for save game files |
| `w_wad.c` | WAD access | 577 | opens and reads the data file |

Add them up in Python:

```python
total = 54_640                 # lines in all .c and .h files, linuxdoom-1.10
platform = 2_938               # the nine i_*.c / i_*.h files
leaks = {"d_main.c": 1_171, "m_misc.c": 534, "m_menu.c": 1_893, "w_wad.c": 577}

size = platform + sum(leaks.values())
print(f"platform layer only: {platform / total:.1%}")
print(f"real port size:   {size:,} lines = {size / total:.1%}")
print(f"leaks multiply the port size by {size / platform:.1f}x")
```

```
platform layer only: 5.4%
real port size:   7,113 lines = 13.0%
leaks multiply the port size by 2.4x
```

Four files that each "just needed to open a file" multiply the port size by 2.4. Anyone porting it to Windows had to read the menu code to port the game. That is the cost of a leak, and it grows with every file that takes the shortcut.

Be fair to id. The leaked calls are ordinary POSIX file functions, and in 1997 every target they cared about offered something close to them. A porter often only renames a few calls. Still, the porter can't know that without reading all 4,175 lines. Port size measures what you must *inspect*, which is where the time goes.

### Open the interactive

The left view draws Doom as a layer stack, one block per module, sized by lines. The right view is a single bar: the port size as a share of the whole game. Toggle "Show OS leaks" and watch four blocks outside the platform row turn orange while the bar grows from 5.4% to 13.0%. Then click each leaked file and choose "move its OS calls into `i_system`." Each click shrinks the bar by that file's lines and adds a few lines to the platform row. The picture makes the point that the percentages hide: a leak costs the size of the *file it lands in*, not the size of the call.

### Upward dependencies in the platform layer

Leaks are one kind of violation: OS code escaping upward. The other kind is the platform layer naming something above it. Three of Doom's `i_` files include headers from higher layers:

| Platform file | Includes | Uses it to |
|---|---|---|
| `i_video.c` | `d_main.h` (main loop) | call `D_PostEvent` with each key press and mouse move |
| `i_system.c` | `g_game.h` (game flow) | call `G_CheckDemoStatus` from `I_Error` before quitting |
| `i_sound.c` | `w_wad.h` (resources) | load sound effects out of the WAD file |

The first one is the interesting case. The platform layer must hand input to the game somehow. Doom does it by calling a game-flow function by name. Look inside `D_PostEvent` and you find it only copies the event into a 64-slot ring buffer (a queue that wraps around, from [CS102 week 6](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md)). The idea is sound: a queue between the layers. The only problem is where the queue lives. Section 4 moves it.

### Cross-game recognition

**Quake (id Software, 1996; source released under the GPL in December 1999).** The `WinQuake` folder splits every OS-facing job into an interface header and one file per platform: `sys_win.c`, `sys_linux.c`, `sys_dos.c`, `sys_sun.c` for system calls, and likewise `vid_*`, `snd_*`, `in_*`, `cd_*` and `net_*`. For each job there is also a stub file that does nothing (`*_null.c`, plus `net_none.c` for networking). The header comment of `vid_null.c` says it is a null driver meant to help porting. The six stub files add up to 555 lines. A Linux build with X11 video uses `sys_linux.c`, `vid_x.c`, `snd_linux.c`, `cd_linux.c` and `net_udp.c`: 2,755 lines, 2.8% of the 98,377 lines in the folder. Same model, stricter discipline. To start a port you copy the null files, get a black window, then fill them in one at a time.

**Godot (4.7.2, 2026).** Godot's own documentation describes the engine in layers: Scene on top, then Servers (rendering, audio, physics as singletons), then Drivers and Platform Interface, then Core, with Main managing start-up and the loop. The source tree mirrors it, with `platform/` holding one folder per target (Android, iOS, Linux/BSD, macOS, visionOS, web, Windows) and `drivers/` holding graphics and audio back ends. By file size, `platform/` plus `drivers/` is about 31% of the runtime source (core, servers, scene, main, platform and drivers; about 37.7 MB). That share is far larger than Doom's, and the reason is instructive. A modern engine talks to three or four graphics APIs, touch screens, app stores and browser sandboxes. The platform layer grew because the world under it grew. The rule did not change.

Three engines, three decades, one idea. When you open an unfamiliar engine, find the folder that holds the OS code and ask two questions. How big is it compared with the whole? And what outside it includes an OS header?

### Design judgment

Strict layering has costs, and you should pay them deliberately.

- **Indirection costs a little speed and a lot of reading.** Every OS call goes through a wrapper. Usually the cost is one function call, which is nothing. The real cost is that a new programmer has to learn your wrapper API instead of the OS API they already know.
- **Wrappers can hide capabilities.** A lowest-common-denominator file API can't expose a console's fast asynchronous reads. Good platform layers let a platform offer extras behind a query ("does this platform support X?") instead of pretending all platforms are equal.
- **Some leaks are cheap.** Doom's POSIX calls were close to what every target offered. Leaking `<stdio.h>` everywhere is normal because every platform has it. The dangerous leaks are the ones specific to one vendor: window handles, GPU objects, console SDK calls.
- **Measure, don't argue.** "Our platform layer is clean" is an opinion. "Port size is 6.1% and two files outside `platform/` include OS headers" is a fact your lead can act on. Lab 1 builds the tool that produces that sentence.

## 3. Dependencies decide the start-up order

Layers also tell you in what order to start the engine. If the renderer uses the file system to load shaders, the file system must be running before the renderer starts. If the file system allocates buffers through the memory system, memory must start first.

Write each "A needs B" as an edge. Any order where every module comes after everything it needs is a valid **start-up order**. Computer scientists call such an order a **topological sort** of the dependency graph. You met graphs in [CS102 week 8](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md). Shut-down runs in exactly the reverse order, so nothing is stopped while something above it still uses it.

Doom's `D_DoomMain` prints each step as it starts, which gives you a real order to read: `V_Init` (screens), `M_LoadDefaults` (config), `Z_Init` (zone memory), `W_Init` (WAD files), `M_Init`, `R_Init` (renderer), `P_Init` (play), `I_Init` (machine state), `D_CheckNetGame`, `S_Init` (sound), `HU_Init` (heads-up display), `ST_Init` (status bar). Notice that `V_Init` runs before `Z_Init`. It can, because it grabs its screen buffers straight from the OS instead of from the zone. The order encodes the dependencies, including the exceptions.

### Why not let constructors do it?

In C++ it is tempting to write each subsystem as a global object whose constructor starts it and whose destructor stops it. The problem is that C++ does not define the order in which global objects in *different* source files are constructed. If `g_renderer` in `renderer.cpp` is built before `g_files` in `files.cpp`, the renderer's constructor loads shaders through a file system that doesn't exist yet. This is known as the **static initialization order problem**. Gregory's section 6.1 recommends the plain fix most engines use: constructors do nothing, and explicit `start` and `stop` functions run in an order you write down.

```cpp
#include <cstdio>

// Each subsystem has explicit start and stop functions.
// Constructors and destructors do nothing, so global order cannot bite.
struct MemorySystem   { void start() { std::puts("start memory");   } void stop() { std::puts("stop memory");   } };
struct FileSystem     { void start() { std::puts("start files");    } void stop() { std::puts("stop files");    } };
struct RenderSystem   { void start() { std::puts("start renderer"); } void stop() { std::puts("stop renderer"); } };
struct AudioSystem    { void start() { std::puts("start audio");    } void stop() { std::puts("stop audio");    } };

MemorySystem g_memory;
FileSystem   g_files;
RenderSystem g_renderer;
AudioSystem  g_audio;

int main() {
    // Start in dependency order: nothing starts before what it uses.
    g_memory.start();
    g_files.start();      // needs memory
    g_renderer.start();   // needs memory and files (shaders, textures)
    g_audio.start();      // needs memory and files (sound banks)

    // ... the game loop runs here ...

    // Stop in exactly the reverse order.
    g_audio.stop();
    g_renderer.stop();
    g_files.stop();
    g_memory.stop();
}
```

Build and run it with `c++ -std=c++20 -Wall startup.cpp -o startup && ./startup`. It prints the four starts, then the four stops in reverse.

It looks almost too plain. That is the point. The order is visible in one function, a code reviewer can check it against the dependency list, and a crash during start-up points at one line.

### When no order exists

If A needs B and B needs A, no topological order exists. That is a **dependency cycle**, and it always means a design problem, not a sorting problem. Lab 1 asks you to detect cycles automatically. The usual fix is to find the small piece that both modules share and move it one layer down, or to replace one direction of the dependency with a callback, which is the next section.

## 4. Talking upward without depending upward

Lower layers often need to tell higher layers something. The OS reports a key press, and the game must hear it. The physics engine finds a collision, and gameplay must apply damage. The rule says the lower layer can't name the higher one. So how does the message get up?

The answer is the one you learned in [CS102 week 10](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md): the lower layer defines a slot, and the higher layer plugs itself in. In C++ the simplest slot is a function pointer. The platform layer declares the *type* of function it will call. The game passes one in at start-up. At compile time, the platform file mentions only its own types.

```cpp
#include <cstdio>

// ---- platform layer (layer 0): knows nothing about the game ----
struct Event { int type; int key; };
using EventSink = void (*)(const Event&);

static EventSink g_sink = nullptr;
void platform_set_event_sink(EventSink sink) { g_sink = sink; }

void platform_poll() {              // pretend the OS reported two keys
    Event pressed{1, 'W'}, released{2, 'W'};
    if (g_sink) { g_sink(pressed); g_sink(released); }
}

// ---- game layer (layer 4): knows about the platform, not the reverse ----
void game_on_event(const Event& e) {
    std::printf("game got event type=%d key=%c\n", e.type, e.key);
}

int main() {
    platform_set_event_sink(game_on_event);   // the game plugs itself in
    platform_poll();
}
```

Output:

```
game got event type=1 key=W
game got event type=2 key=W
```

At run time the call still goes upward. At compile time the arrow now points only down: `game` includes `platform`, never the reverse. That is the only direction the dependency rule cares about, because compile-time dependencies are what force rebuilds and what a porter must read.

This is how you would fix Doom's `i_video.c`. Move the 64-slot event queue down into the platform layer, have `i_video.c` push into it, and have `d_main.c` drain it each frame. Or keep the queue in `d_main.c` and hand `i_video.c` a function pointer at start-up. Either way `i_video.c` stops including `d_main.h`. The first option has a bonus you will use in [week 9 on input](w09-input-and-event-systems.md): a queue of timestamped events can be recorded and replayed.

A function pointer is not the only slot. A virtual interface (`class IEventSink { virtual void on_event(const Event&) = 0; }`), a `std::function`, or a message bus all work. The trade-off is familiar from CS102: the more general the slot, the easier it is to plug in, and the harder it is to see from the code who is listening.

## 5. The engine you will build

Here is the plan for the semester, laid out in the layers from section 1. Each week adds one piece and keeps the dependency rule.

| Layer | Weeks | What you build |
|---|---|---|
| Platform | 1, 9 | a window, a clock, file reads, an input event queue |
| Core | 2, 3, 13 | ownership rules, allocators, a profiler |
| Resources | 7, 12 | a resource cache with hot reload, save files |
| Engine systems | 4, 8, 11 | the frame, a rendering hook, a physics step |
| Gameplay foundations | 5, 6, 10 | an entity-component-system, cache-friendly storage, a scripting hook |
| Tools | 14 | an in-game inspector |

The [syllabus](../syllabus.md) has the full schedule. Week 2 starts at the bottom, with the C++ rules for owning memory, because every layer above it allocates something.

## In-class activity (25 minutes)

Work in pairs. You get a printout of Kiln, a made-up mini engine of 13 headers and a `main.cpp`, 170 lines in all, with every `#include` line visible. It is the same code as the fixture in Lab 1 (`lab01-starter/mini_engine/`), and the folders name the layers: `platform`, `core`, `resources`, `engine`, `gameplay`, `game`.

1. Write the layer number (0 for platform up to 5 for game, 6 for `main.cpp`) next to each file. (5 min)
2. Draw every include as an arrow. Circle every arrow that points upward. (5 min)
3. Mark every file that includes an OS header. Compute Kiln's port size and port share. (5 min)
4. Pick one upward arrow and redesign it as a function-pointer slot. Write the new header in five lines or fewer. (5 min)
5. Swap with the pair next to you and check their port share. (5 min)

Expected output: one sheet with the layered drawing, the port share as a percentage with the arithmetic shown, and the five-line header.

## Common misconceptions

- **"Layers are about folders."** Folders are a convention. Layers are about which files include which. You can have a tidy `platform/` folder and still leak `<windows.h>` into gameplay, which is exactly what Doom did with POSIX headers.
- **"A callback is an upward dependency."** At run time control flows up. At compile time the lower layer names only its own function type. The rule is about compile-time names, so a callback respects it.
- **"The platform layer is small, so porting is cheap."** Port cost is the platform layer *plus* every file with a leak. Doom's layer is 5.4% of the code, but its real port size is 13.0%.
- **"Global objects with constructors are a clean way to start subsystems."** Their construction order across source files is not defined by C++. Use explicit start and stop calls in a written order.

## Check yourself

1. An engine has 80,000 lines. Its platform layer is 3,200 lines. Five files outside it include `<windows.h>`: 900, 1,400, 600, 2,100 and 300 lines. What is the port share? By what factor do the leaks multiply the port size?
2. Subsystems and their needs: Audio needs Files and Memory. Files needs Memory. Renderer needs Files, Memory and Window. Window needs Memory. Give a valid start-up order and the shut-down order. Is the start-up order unique?
3. Someone adds "Memory needs Log" and "Log needs Files" to question 2. What happens to your order, and what would you change in the design?
4. In the Quake Linux build from section 2, suppose `vid_x.c` is replaced by a 2,000-line Wayland driver. What is the new port share, if the folder's total grows by the difference?

<details>
<summary>Answers</summary>

1. Port size is 3,200 + 900 + 1,400 + 600 + 2,100 + 300 = 8,500 lines. Port share = 8,500 / 80,000 = 10.6%. The leaks multiply the port size by 8,500 / 3,200 = 2.7.
2. One valid order is Memory, Files, Window, Audio, Renderer. Shut-down is the reverse: Renderer, Audio, Window, Files, Memory. It is not unique. Window can go anywhere after Memory and before Renderer, and Audio and Renderer can swap.
3. Now Memory needs Log, Log needs Files, Files needs Memory. That is a cycle, so no order exists. The usual fix is to make Log depend on nothing above it: write early log lines to a fixed static buffer or straight to the console, and only attach the file sink after Files starts (a callback plugged in later, as in section 4).
4. The platform set grows from 2,755 to 2,755 − 1,199 + 2,000 = 3,556 lines, and the total grows from 98,377 to 99,178. Port share = 3,556 / 99,178 = 3.6%.

</details>

## Lab / assignment hook

[Lab 01, a layer checker](../labs/lab01.md). You write a Python tool that reads `#include` lines from a C++ source tree, assigns files to layers, and reports upward dependencies, OS leaks, the port share and a start-up order. You run it on the Kiln mini engine, fix one violation in the C++ with a callback, and show the checker reporting zero.

## Sources

- id Software, *DOOM* source code, `linuxdoom-1.10` (released December 23, 1997; re-released under the GPL in 1999). GitHub `id-Software/DOOM`. File list, line counts (`wc -l *.c *.h`, 124 files, 54,640 lines), includes in `d_main.c`, `m_misc.c`, `m_menu.c`, `w_wad.c`, `i_video.c`, `i_system.c`, `i_sound.c`; `D_PostEvent` and `MAXEVENTS` = 64; the start-up sequence in `D_DoomMain`. The README's remarks on Linux-only code and portability are paraphrased.
- Wikipedia, "Doom (1993 video game)" and "Doom engine" (accessed September 2026). Development on NeXT, MS-DOS release, source release dates (December 23, 1997, and the GPL re-release on October 3, 1999).
- id Software, *Quake* source code, `WinQuake` folder (source released under the GPL on December 21, 1999). GitHub `id-Software/Quake`. Platform file names, the "null driver to aid porting" comment in `vid_null.c`, the five `*_null.c` files and `net_none.c`, and line counts (195 files, 98,377 lines; null set 555 lines; Linux X11 set 2,755 lines).
- Wikipedia, "Quake engine" (accessed September 2026). GPL release date.
- Godot Engine documentation (stable, 4.7), "Godot's architecture overview" (Engine details, Architecture). Scene, Server, Drivers/Platform Interface, Core and Main layers, with their source folders.
- Godot Engine source, tag `4.7.2-stable`, GitHub `godotengine/godot`. Folders under `platform/`; sizes of `.cpp`, `.h`, `.c`, `.mm`, `.m`, `.java`, `.kt` files per top-level folder from the GitHub tree API (platform 7.03 MB, drivers 4.76 MB, runtime total 37.74 MB).
- Gregory, J. (2018). *Game Engine Architecture* (3rd ed.). CRC Press. Sections 1.3, 1.6 (runtime architecture layers) and 6.1 (start-up and shut-down, static initialization order).

## Interactive spec: examples/w01-port-size.html

**The one insight:** a code base's port cost is the platform layer plus every whole file that leaks an OS call, so a handful of small leaks can more than double it.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view first).

- **Left view, "Layer stack".** Five horizontal rows, top to bottom: Game flow, Gameplay, Engine systems, Core and resources, Platform. Each row holds blocks, one per module group, with width proportional to its lines (a treemap strip per row; the widest row fills the view width). Label each block with its prefix and line count. Colors from the shared palette: neutral for normal blocks, accent for platform blocks, warning (orange) for leaking blocks when leaks are shown.
- **Right view, "Port size".** One vertical bar from 0% to 100% of total lines, filled to the current port share. Beside it, three numbers in large type: port size lines, port share (one decimal), and multiplier versus the platform layer alone (one decimal, "×"). Under it, a small table listing every file in the port size with its lines.

**Data sets** (dropdown "Engine"; default Doom).

Doom, linuxdoom-1.10, total 54,640 lines. Rows and blocks:
- Game flow: `d_` 3,999; `g_` 1,769; `doomstat`/`dstrings`/`doomdef` 856; front end (`hu_` 1,375, `st_` 2,076, `am_` 1,401, `wi_` 1,904, `f_` 1,164) shown as one block "UI 7,920".
- Gameplay: `p_` 15,170; `info` 6,010; `doomdata` 222.
- Engine systems: `r_` 6,811; `v_` 612; `s_` 988; `sounds` 525.
- Core and resources: `m_` 3,305; `z_` 553; `w_` 666; `tables` 2,230; `doomtype` 66.
- Platform: `i_` 2,938.
(These sum to 54,640.)
Leak files (belong to the blocks shown in parentheses): `d_main.c` 1,171 (`d_`), `m_misc.c` 534 (`m_`), `m_menu.c` 1,893 (`m_`), `w_wad.c` 577 (`w_`).
Upward arrows to draw when "Show upward includes" is on: `i_video.c → d_main.h`, `i_system.c → g_game.h`, `i_sound.c → w_wad.h`.

Quake, WinQuake, total 98,377 lines. Show two rows only: "Platform files used by a Linux X11 build" (`sys_linux.c` 457, `vid_x.c` 1,199, `snd_linux.c` 269, `cd_linux.c` 416, `net_udp.c` 414; total 2,755) and "Everything else" (95,622). No leaks. A note under the bar: "Null driver set to start a port: 555 lines."

Godot 4.7.2 (source bytes, not lines; label the unit clearly). Rows: Scene 12.31 MB, Servers 7.51 MB, Core 5.85 MB, Main 0.28 MB, Platform 7.03 MB, Drivers 4.76 MB (Platform and Drivers both in the Platform row). Total 37.74 MB. No leak toggles for Godot.

**Controls.**
- "Engine" dropdown: Doom, Quake, Godot.
- Checkbox "Show OS leaks" (Doom only; default off). On: the four leak files are drawn as orange sub-blocks inside their parent blocks and added to the port size.
- For each leak file, a button "Move OS calls into i_system". Clicking it removes the file from the port size, turns its sub-block neutral, and grows the `i_` block by 40 lines (a stand-in for the wrapper functions). A "Reset" button restores the 1997 state.
- Checkbox "Show upward includes" (Doom only): draws the three arrows from the Platform row to their target blocks.
- All controls keyboard reachable; the bar and numbers update immediately.

**Formulas.** `size = platform_lines + Σ lines of files with leaks shown and not yet moved + 40 × moved_count`. `share = size / (total + 40 × moved_count)`. `multiplier = size / (platform_lines + 40 × moved_count)`.

**Test values (Doom).**
- Leaks off: size 2,938, share 5.4%, multiplier 1.0×.
- Leaks on, none moved: size 7,113, share 13.0%, multiplier 2.4×.
- Leaks on, `m_menu.c` moved: size 2,938 + 1,171 + 534 + 577 + 40 = 5,260; total 54,680; share 9.6%; multiplier 5,260 / 2,978 = 1.8×.
- Leaks on, all four moved: size 3,098, share 3,098 / 54,800 = 5.7%, multiplier 1.0×.
- Quake: share 2.8%. Godot: share 31.2% (Platform 18.6%, Drivers 12.6%, shown as two segments of the bar).

**First screen.** Doom with leaks on and nothing moved, so the student sees the 13.0% bar and the four orange blocks immediately, with the caption "The platform layer is 5.4% of Doom. The real port size is 13.0%."
