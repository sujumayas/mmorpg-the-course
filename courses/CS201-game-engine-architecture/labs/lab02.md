# CS201 · Lab 02: An owning buffer and a move-only handle

**Week:** 2 ([lecture](../lectures/w02-cpp-for-engines-memory-raii-and-move-semantics.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). `PixelBuffer` and `GpuTexture` become the core layer of your engine; the week 3 allocators and the week 7 resource cache build on them.

## Objective

Write two classes that own resources: `PixelBuffer`, which owns heap memory and can be copied and moved, and `GpuTexture`, which owns a handle from a pretend GPU API and can only be moved. Prove with counters that neither leaks, neither frees twice, and a growing `std::vector` of either never deep-copies.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). You need a C++20 compiler (clang 14+, GCC 11+ or MSVC 2022) and Python 3.10+ to run the test script.

- `pixel_buffer.h`: `PixelBuffer` with a finished constructor and destructor, and four special member functions marked TODO. The starter versions compile and are safe, but wrong in instructive ways: the copy constructor forgets the bytes, the copy assignment does nothing, and the move constructor secretly copies and is not `noexcept`. `allocate_bytes` and `free_bytes` count every allocation in `g_stats`.
- `gpu_texture.h`: a fake GPU API (`gpu_create_texture`, `gpu_destroy_texture`) that tracks live ids and counts errors such as destroying an id twice, and a `GpuTexture` class with only a constructor and destructor.
- `test_lab02.cpp`: eleven tests (A1-A7 for `PixelBuffer`, B1-B4 for `GpuTexture`). Each prints `PASS` or `FAIL` with the failing line.
- `run_tests.py`: builds the tests with UndefinedBehaviorSanitizer and runs them. Add `--asan` to also build with AddressSanitizer, which catches double frees and leaks at the moment they happen. (AddressSanitizer works on most Linux and Windows setups. On some recent macOS versions it hangs at start-up; the script stops after 60 seconds and tells you so. If that happens, run without `--asan` and rely on the counters.)

On the starter, `python run_tests.py` passes A1 only, fails the other ten, and exits with code 1.

## Steps

### Part A: `PixelBuffer` (60 min)

1. Read `pixel_buffer.h` from top to bottom. Before changing anything, write in your README which of the five special member functions this class needs to define, and why (lecture section 2, rule of five).
2. Write the copy constructor. It must allocate through `allocate_bytes`, copy the bytes, and add the size to `g_stats.bytes_copied`. Test A2 must pass.
3. Write the move constructor and mark it `noexcept`. It steals the pointer and size and leaves the source with `nullptr` and 0. It must not allocate. Tests A4 and A6 (first half) must pass.
4. Write the move assignment operator, also `noexcept`. Free your own block first, then steal. Handle `a = std::move(a)` without freeing the block you are about to keep. Tests A5 and A6 must pass.
5. Write the copy assignment operator. Two correct designs exist: check for self-assignment and copy by hand, or copy into a temporary and move-assign from it (the "copy-and-swap" idea). Pick one and write two sentences in your README on why. Test A3 must pass.
6. Test A7 should now pass without further changes. Explain in your README which function made it pass, and what `g_stats.bytes_copied` would be if you removed `noexcept` from that function. Then remove it, run the tests, and check your prediction. Put `noexcept` back.

### Part B: `GpuTexture` (30 min)

7. Delete the copy constructor and copy assignment. Test B1 must pass.
8. Write the `noexcept` move constructor and move assignment. A moved-from texture holds id 0 and its destructor does nothing. Move assignment must destroy the texture it held before taking the new one. Tests B2, B3 and B4 must pass.
9. Before step 7, test B4 failed with `errors` above zero. In your README, explain exactly what sequence of calls produced those errors in the starter, and why the compiler never warned you. (Hint: lecture section 3, "the second way to lose moves.")

### Part C: measure it (30 min)

10. Copy the `grow.cpp` program from lecture section 3 into a new file. Replace its `Texture` with your `PixelBuffer(65536)` and push 1,000 of them. Print `g_stats.allocations`, `g_stats.frees` and `g_stats.bytes_copied`. Build with `-O2`.
11. Run it three ways: as written, with `noexcept` removed from your move constructor, and as written with `v.reserve(1000)` added. Record the three triples and the wall-clock time of each run (use `std::chrono::steady_clock` around the loop, best of five runs). Put the table in your README and compare it with the lecture's table. Your byte counts must match the lecture exactly on libc++ or libstdc++; on Microsoft STL they follow the ×1.5 row.

## Deliverable

A zip of your `lab02-starter/` folder containing:

- `pixel_buffer.h` and `gpu_texture.h` with all eleven tests passing under `python run_tests.py` (and under `--asan` if it runs on your machine).
- `grow_buffers.cpp` from Part C.
- `README.md` (one page at most): the answers to steps 1, 5, 6 and 9, and the Part C table with your machine, compiler and flags.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| `PixelBuffer` copy operations (A2, A3) | Both pass; self-assignment handled; no duplicated cleanup code | Both pass but copy assignment duplicates destructor logic | Either fails | 20 |
| `PixelBuffer` move operations (A4-A7) | All pass; both moves `noexcept`; moved-from state documented in a comment | All pass, no comment | Any fails | 25 |
| `GpuTexture` (B1-B4) | All pass; copy deleted, moves `noexcept` | All pass but moves not marked `noexcept` explicitly (relying on defaults) | Any fails | 20 |
| Part C measurements | Three runs, counts match the lecture's model exactly, timings with machine and flags | Counts present but one run missing or unexplained mismatch | Missing | 20 |
| README answers (steps 1, 5, 6, 9) | Correct and specific; step 9 names the implicit copy constructor and the double `gpu_destroy_texture` | Mostly correct but vague | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

A reference solution passes all eleven tests with UBSan and, on Linux, with ASan. Part C expected counts on libc++/libstdc++: with `noexcept`, 1,000 allocations, 1,000 frees at exit, 0 bytes copied; without `noexcept`, 2,023 allocations and 1,023 × 65,536 = 67,043,328 bytes copied; with `reserve`, the same as the first row. Step 9: the starter's user-declared destructor suppresses the implicit move constructor, so `std::vector<GpuTexture>` copies on growth using the implicitly generated copy constructor (deprecated but still generated), then destroys the old elements, so each id is destroyed once by the old copy and again later by the new one. The compiler does not warn because generating that copy constructor is legal; clang flags it with `-Wdeprecated-copy-with-dtor` (reported as `-Wdeprecated-copy-with-user-provided-dtor` in clang 17), which is not part of `-Wall -Wextra`. Common mistakes: forgetting to null the source in the move constructor (ASan reports a double free; without ASan, A4 fails), freeing before the self-move check in move assignment, and marking only the move constructor `noexcept`.

</details>
