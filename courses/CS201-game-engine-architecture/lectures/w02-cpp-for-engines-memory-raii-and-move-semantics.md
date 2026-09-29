# CS201 · Week 02 — C++ for Engines: Memory, RAII and Move Semantics

**Why this matters:** Python cleaned up after you. C++ does exactly what you write, including copying 64 MiB of pixels because a function was missing one keyword. Engine code lives or dies on knowing, for every object, who owns it, when it is destroyed and what a line like `v.push_back(x)` really does to memory.

**You will be able to:**
- Write a class that owns a resource with RAII and state which of the five special member functions it needs.
- Compute how many elements a growing `std::vector` relocates for a given growth factor, and the bytes moved when each relocation is a copy versus a move.
- Predict, from a class definition alone, whether a container will move or copy it when it grows.
- Compare three engine strategies for cheap relocation (noexcept moves, trivial relocation, copy-on-write) and choose one for a given element type.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), section 3.1 "C++ Review and Best Practices" and section 3.3 "Data, Code and Memory Layout". cppreference.com, the pages "RAII" and "The rule of three/five/zero" (about 15 minutes together). Reread your notes on amortized `append` from CS102 week 4.

**Prerequisites from earlier courses:** [CS102 week 1, classes and encapsulation](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w01-classes-objects-encapsulation.md) (an object that protects an invariant). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md), section 4 (why a doubling array makes `append` O(1) on average). [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (contiguous storage). [CS201 week 1, runtime layers](w01-engine-anatomy-and-runtime-layers.md) (this week's code sits in the core layer).

**Interactive:** [`examples/w02-vector-growth.html`](../examples/w02-vector-growth.html). Keep it open during section 3.

---

## 1. Where an object's bytes live

In Python every value is an object on a heap, every variable is a reference to one, and a garbage collector frees objects when nothing refers to them. You never chose where anything lived, and you never freed anything.

C++ gives you three places to put an object, and each has its own **lifetime**, the span of time during which the object exists and its memory is valid.

- **Automatic storage (the stack).** A local variable like `int hp = 100;` or `Texture t(128, 128);` lives until the closing brace of its scope. Creating it costs almost nothing: the compiler reserves space by moving the stack pointer. Destroying it is automatic.
- **Static storage.** Globals and `static` variables live for the whole program. Week 1 showed why their start-up order across files is a trap.
- **Dynamic storage (the heap, or free store).** `new` or `std::malloc` asks the allocator for memory that lives until someone calls `delete` or `std::free`. The heap is the only place whose size you choose at run time, which is why containers put their elements there.

A `std::vector<int>` shows all this at once. The vector object itself is small (24 bytes on the 64-bit compilers used in this course: a pointer to the first element, one to the end of the elements, one to the end of the capacity). It lives wherever you declared it, often the stack. The elements live in a heap block that the vector owns. When the vector's lifetime ends, its destructor frees that block.

That last sentence is the whole idea of this lecture. The vector *owns* the heap block, and the end of the vector's lifetime is what releases it. The next section gives the idea its name.

## 2. Ownership and RAII

A **resource** is anything you acquire and must give back: heap memory, a GPU texture, a file handle, a network socket, a lock. Engines hold thousands of them. The platform layer from week 1 hands most of them out through C-style functions like `gpu_create_texture` and `gpu_destroy_texture`, and every create must be matched by exactly one destroy.

Matching them by hand fails in a predictable place: the early return. Here is a pretend graphics API and a loader that forgets one path.

```cpp
#include <cstdio>

// A pretend C graphics API, like the ones a platform layer wraps.
static int live_textures = 0;
int  gpu_create_texture(int w, int h) { ++live_textures; return w * 10000 + h; }
void gpu_destroy_texture(int)         { --live_textures; }

// Version 1: the caller must remember to destroy on every path.
bool load_icon_raw(bool file_is_corrupt) {
    int tex = gpu_create_texture(128, 128);
    if (file_is_corrupt) {
        return false;                 // forgot gpu_destroy_texture: leak
    }
    gpu_destroy_texture(tex);
    return true;
}

// Version 2: RAII. The destructor runs on every path out of the scope.
class Texture {
public:
    Texture(int w, int h) : id_(gpu_create_texture(w, h)) {}
    ~Texture() { if (id_ != 0) gpu_destroy_texture(id_); }

    Texture(const Texture&) = delete;             // two owners would destroy twice
    Texture& operator=(const Texture&) = delete;

    Texture(Texture&& other) noexcept : id_(other.id_) { other.id_ = 0; }
    Texture& operator=(Texture&& other) noexcept {
        if (this != &other) {
            if (id_ != 0) gpu_destroy_texture(id_);
            id_ = other.id_;
            other.id_ = 0;
        }
        return *this;
    }

private:
    int id_;
};

bool load_icon_raii(bool file_is_corrupt) {
    Texture tex(128, 128);
    if (file_is_corrupt) {
        return false;                 // ~Texture runs here
    }
    return true;                      // and here
}

int main() {
    for (int i = 0; i < 100; ++i) load_icon_raw(i % 10 == 0);
    std::printf("raw:  %d textures leaked\n", live_textures);

    live_textures = 0;
    for (int i = 0; i < 100; ++i) load_icon_raii(i % 10 == 0);
    std::printf("RAII: %d textures leaked\n", live_textures);
}
```

```
raw:  10 textures leaked
RAII: 0 textures leaked
```

One file in ten is corrupt, so the raw version leaks ten textures per hundred loads. In an MMO that streams item icons as players open bags and trade windows, that leak runs for hours. The RAII version cannot leak, because C++ guarantees that a local object's destructor runs when control leaves its scope, whether by `return`, by reaching the brace, or by an exception.

**RAII** stands for "resource acquisition is initialization." The name is clumsy. The rule is simple: acquire a resource in a constructor, release it in the destructor, and let the object's lifetime decide when. The class becomes the resource's single **owner**.

### Copying an owner is a question, not a default

Look again at the `Texture` class. It deletes its copy constructor and copy assignment. Why?

If C++ copied a `Texture` the default way, it would copy the integer `id_`. Now two objects hold the same GPU id, both destructors call `gpu_destroy_texture` on it, and the second call destroys a texture that no longer exists, or worse, one that the driver has since handed to someone else. That is a **double free**, and it is one of the classic crashes in C++ code.

So an owning class must answer: what does copying mean for me? There are three honest answers.

1. **Copying makes a second resource.** A pixel buffer can do this: allocate a new block and copy the bytes. That is a **deep copy**. It is correct and it can be expensive.
2. **Copying is forbidden.** A GPU texture or a file handle usually can't be cloned cheaply, so you `= delete` the copy operations. The type becomes **move-only**.
3. **Copying shares the resource.** Both copies point at one resource and a counter tracks how many owners remain. This is **shared ownership**, what `std::shared_ptr` does, and it has costs section 3 will show.

### Moving: handing over ownership

A move-only type still needs to travel. You want to return a `Texture` from a loader function, or store it in a vector. **Moving** transfers the resource from one object to another and leaves the source empty. Look at the move constructor above. It copies the integer, then sets the source's `id_` to 0, so the source's destructor does nothing. Exactly one owner remains, and no GPU call happened.

The five functions that control copying, moving and destruction (copy constructor, copy assignment, move constructor, move assignment, destructor) are called the **special member functions**. Two rules of thumb organize them.

- **Rule of zero.** If your class holds only members that already manage themselves (`std::vector`, `std::string`, `std::unique_ptr`, a `Texture`), write none of the five. The compiler generates correct ones member by member. Most game classes should look like this.
- **Rule of five.** If your class directly manages a raw resource (it calls `gpu_destroy_texture`, `std::free` or `delete` in its destructor), write or delete all five. If you write one, the others the compiler generates are probably wrong.

The standard library already has a ready-made owner for a single heap object, `std::unique_ptr<T>`. It is move-only, frees its object in its destructor, and on the compilers used in this course it is exactly 8 bytes, the same as a raw pointer. Reach for it before you write your own.

## 3. Worked example: 1,000 item icons, one keyword

### The hook

In 2007, Paul Pedriana of Electronic Arts published a paper for the C++ standards committee describing EASTL, EA's in-house replacement for the standard containers. Among the reasons it gives: when a vector of reference-counted objects grows, every element gets copied and every copy bumps a counter up and then down. EA's programmers called these "ref count storms." They were slow, and they made debugging harder. So EA wrote its own containers, partly to stop them copying things they only needed to move.

C++ has since added move semantics, which fixes this. Almost. The fix depends on one keyword that most students never write. Here is the experiment.

### The setup

An MMO client keeps its bag and bank icons in a `std::vector<Icon>`. Each `Icon` owns its pixels, a 128 × 128 RGBA image, which is 65,536 bytes (64 KiB). At login the client loads 1,000 of them with `emplace_back`, without calling `reserve` first.

```cpp
#include <cstdio>
#include <vector>

// A texture that owns a pixel buffer. The counters record
// how the vector treats it when it has to grow.
static int copies = 0;
static int moves = 0;

template <bool NoexceptMove>
struct Texture {
    std::vector<unsigned char> pixels;

    explicit Texture(std::size_t bytes) : pixels(bytes) {}
    Texture(const Texture& other) : pixels(other.pixels) { ++copies; }
    Texture(Texture&& other) noexcept(NoexceptMove)
        : pixels(std::move(other.pixels)) { ++moves; }
};

template <bool NoexceptMove>
void grow(int n) {
    copies = moves = 0;
    std::vector<Texture<NoexceptMove>> textures;
    for (int i = 0; i < n; ++i) {
        textures.emplace_back(16);  // 16 bytes keeps the demo small
    }
    std::printf("noexcept=%d  n=%d  copies=%d  moves=%d  capacity=%zu\n",
                NoexceptMove, n, copies, moves, textures.capacity());
}

int main() {
    grow<false>(1000);
    grow<true>(1000);
}
```

Compiled with Apple clang 17 (libc++), `c++ -std=c++20 -O2 grow.cpp`:

```
noexcept=0  n=1000  copies=1023  moves=0  capacity=1024
noexcept=1  n=1000  copies=0  moves=1023  capacity=1024
```

The two types are identical except for `noexcept` on the move constructor. Both have a move constructor. Without `noexcept`, the vector never calls it.

### The model

Two separate things decide the cost of growth. Keep them apart.

**How many elements get relocated** depends only on the container's growth policy. When a vector is full and you push one more element, it allocates a bigger block, **relocates** every existing element into it (constructs it at the new address and destroys the old one), and frees the old block. With growth factor `g`, the capacity goes 1, then roughly `g` times larger each time. You showed in CS102 week 4 that with doubling the total work is O(n). Here we need the exact count:

```
R(n) = sum of the sizes at which the vector was full, for all reallocations before n
     = 1 + 2 + 4 + ... + 512 = 1,023      for n = 1,000 and g = 2
```

**What each relocation costs** depends on the element type:

```
bytes moved = R(n) × c
c = size of the whole payload   if the element is copied   (65,536 bytes here)
c = size of the object itself   if it is moved             (24 bytes: three pointers)
```

And the rule that decides copy or move is in the standard. `push_back` and `emplace_back` promise that if an exception is thrown during growth, the vector is left unchanged. That is the **strong exception guarantee**. A copy never damages the old elements, so a throwing copy is safe to abandon. A move empties the old element, so a move that throws halfway would leave the old block half-empty with no way back. So the library moves only when the move constructor is declared `noexcept`, or when the type can't be copied at all. Otherwise it copies. The helper that makes this choice is `std::move_if_noexcept`.

### Numbers you can check

The real growth policies, read from the library sources: libc++ (clang) and libstdc++ (GCC) double the capacity, and Microsoft's STL grows by half (`capacity + capacity / 2`). This script counts relocations for both.

```python
def relocations(n, grow):
    """Count element relocations while push_back-ing n items."""
    size = capacity = moved = reallocs = 0
    for _ in range(n):
        if size == capacity:
            capacity = max(grow(capacity), size + 1)
            moved += size          # every existing element changes address
            reallocs += 1
        size += 1
    return reallocs, moved, capacity

libcxx = lambda cap: 2 * cap            # libc++ and libstdc++
msvc = lambda cap: cap + cap // 2       # Microsoft STL

for n in (10, 100, 1000, 10000):
    print(n, relocations(n, libcxx), relocations(n, msvc))
```

```
10 (5, 15, 16) (7, 25, 13)
100 (8, 127, 128) (13, 284, 141)
1000 (11, 1023, 1024) (18, 2137, 1066)
10000 (15, 16383, 16384) (24, 24284, 12138)
```

Each tuple is (reallocations, relocations, final capacity). Now price the 1,000 icons:

| Library | Relocations | Bytes moved, copy (64 KiB each) | Bytes moved, `noexcept` move (24 B each) | Extra heap allocations, copy |
|---|---|---|---|---|
| libc++ / libstdc++ (×2) | 1,023 | 67,043,328 (63.9 MiB) | 24,552 (24 KiB) | 1,023 |
| Microsoft STL (×1.5) | 2,137 | 140,050,432 (133.6 MiB) | 51,288 (50 KiB) | 2,137 |
| any, after `reserve(1000)` | 0 | 0 | 0 | 0 |

Missing `noexcept` makes growth about 2,700 times more expensive in bytes, and adds one heap allocation and one free per relocation. On the reference machine (Apple M4 Pro, clang 17, `-O2`), the whole loading loop, including allocating and filling the 1,000 icons themselves, took about 2.2 ms with the copying type and 0.8 ms with the moving one. The difference, 1.4 ms, is 8% of a 16.7 ms frame. At login you might not notice. In a system that rebuilds a list like this every frame, you would.

### Open the interactive

The left view plots size and capacity as you push elements: a staircase, with a marker at each reallocation. The right view plots cumulative bytes relocated, with two lines, copy and move. Drag the element-count slider and watch the staircase. It looks the same whether or not you tick `noexcept`. Now watch the right view. The move line hugs the axis while the copy line climbs to 64 MiB. Same container, same staircase, 2,700 times the bytes. Switch the growth factor to 1.5 and the staircase gets more steps (18 instead of 11) while the final capacity sits closer to 1,000. Then tick `reserve` and both lines drop to zero.

### The second way to lose moves

You don't have to write a copy constructor to get copies. Add a destructor, any destructor, and C++ stops generating the move constructor for you. The copy constructor is still generated, so containers copy.

```cpp
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

struct Quiet  { std::string name = std::string(40, 'x'); };
struct Logged { std::string name = std::string(40, 'x'); ~Logged() {} };  // "just add a destructor"

static int allocations = 0;
void* operator new(std::size_t n) { ++allocations; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

template <class T> int count(int n) {
    std::vector<T> v;
    for (int i = 0; i < n; ++i) v.emplace_back();
    allocations = 0;
    v.emplace_back();            // v is full at n = 1024: this push reallocates
    return allocations;
}

int main() {
    std::printf("Quiet:  %d allocations for one push\n", count<Quiet>(1024));
    std::printf("Logged: %d allocations for one push\n", count<Logged>(1024));
}
```

```
Quiet:  2 allocations for one push
Logged: 1026 allocations for one push
```

`Quiet` needs two allocations: the new element block and the new element's string. `Logged` needs 1,024 more, one per copied string. A programmer who added `~Logged() {}` to set a breakpoint just made every reallocation copy every name. The rule of zero protects you here. If you must write a destructor, also write `Logged(Logged&&) noexcept = default;` and the copy and move assignments.

### Cross-engine recognition

Engines that ship their own containers solve the same problem, relocating elements cheaply, in three different ways.

**EASTL (Electronic Arts, 2007 paper; on GitHub under a BSD licence since December 2015).** EASTL added a type trait, `has_trivial_relocate`, that a programmer can declare for a class. It says: this object can be moved to a new address by copying its raw bytes (`memcpy`) and forgetting the old ones. The paper's own example is a reference-counted handle. Copying it properly bumps a counter; relocating it by `memcpy` doesn't need to, because the number of owners hasn't changed. The paper notes that this idea is closely related to move semantics, which were still being designed at the time.

**Unreal Engine (5.x documentation).** Unreal's `TArray` documentation states that it, like many Unreal containers, assumes its element type is **trivially relocatable**: elements can be moved to a new address by copying raw bytes. So `TArray` growth is a byte copy of each object's own bytes (the 24-byte equivalent above), never a deep copy, and it doesn't depend on a keyword. The price is a rule you must follow: don't put in a `TArray` a type that stores a pointer to itself.

**Godot (4.7).** Godot's core-types documentation says the same thing about its containers: they assume elements are trivially relocatable so they can relocate with `memcpy` or `realloc`, and a type that points into itself may crash. Godot adds a second trick for its default `Vector`: **copy-on-write**. Copying a `Vector` copies only a pointer and bumps a reference count, so passing it around is almost free. The first write to a shared copy triggers the real deep copy. The docs recommend `LocalVector`, which has no copy-on-write, where speed matters and cheap copying doesn't.

Rewrite all three into this lecture's model and you get the same equation, `bytes moved = R(n) × c`. Each engine attacks `c`. The standard library shrinks `c` to the object's own size through `noexcept` moves. Unreal and Godot shrink it the same way through a relocation assumption. Godot's `Vector` also delays the deep copy until a write. `reserve` attacks `R(n)` instead.

### Design judgment

- **Declare moves `noexcept`, always, and check.** Moving an owner is pointer swapping; it has no reason to throw. Add `static_assert(std::is_nothrow_move_constructible_v<Icon>);` next to any type you store in a container, and the build fails the day someone adds a destructor.
- **`reserve` when you know the count.** At login you know how many icons are in the bag. One call makes `R(n) = 0`. Don't sprinkle `reserve` inside loops, though: `reserve(size() + 1)` on every push can defeat geometric growth and make it O(n²).
- **Trivial relocation is faster and more dangerous.** It skips even the move constructor, but a type that stores a pointer to its own member (a small-buffer string, an intrusive list node) breaks silently. Unreal and Godot chose it for speed and wrote the rule down. If you adopt it, write it down too.
- **Copy-on-write moves the cost, it doesn't remove it.** The deep copy still happens, at the first write, possibly in the middle of a frame and far from the code that made the copy. The shared counter also needs atomic updates if two threads can touch it, which is exactly the "ref count storm" EA complained about.
- **Store handles, not heavy objects.** Often the best `c` is a 4-byte index into a pool that never moves. Week 3 builds that pool, and section 4 shows the second reason to want it.

## 4. What `std::move` actually does

`std::move` doesn't move anything. It is a cast. It turns its argument into an **rvalue reference**, a way of saying "you may steal from this object; I'm done with it." Overload resolution then picks the move constructor or move assignment if the type has one. If it doesn't, the copy runs, silently.

```cpp
#include <cstdio>
#include <string>
#include <utility>

int main() {
    std::string a = "a very long item name that will not fit in the small buffer";
    std::string b = std::move(a);     // std::move only casts; the move constructor does the work
    std::printf("b has %zu chars, a has %zu chars\n", b.size(), a.size());
}
```

```
b has 59 chars, a has 0 chars
```

On libc++ the moved-from string is empty. The standard promises less: a moved-from standard library object is in a **valid but unspecified state**. You may destroy it or assign a new value to it. You shouldn't read it. For your own types, like `Texture`, define the moved-from state yourself (id 0, "owns nothing"), because your destructor has to handle it.

Three patterns cover most engine code:

- **Return by value.** `Texture load(const char* path)` returning a local `Texture` is fine. The compiler either builds the result directly in the caller's variable (copy elision) or moves it. Don't write `return std::move(local);`. It can block the elision and is never faster.
- **Sink parameters.** A function that stores its argument (`void Inventory::add(Icon icon) { icons_.push_back(std::move(icon)); }`) takes it by value and moves it in. Callers with a temporary pay one move; callers who want to keep theirs pay one copy, and they can see it.
- **Don't use after move.** Most static analyzers flag reading a variable after `std::move`. Treat that warning as an error.

### Shared ownership, briefly

`std::shared_ptr<T>` keeps a reference count next to the object. Copying it increments the count, destroying a copy decrements it, and the last one frees the object. On this course's compilers it is 16 bytes (two pointers), and the count updates are atomic so that threads can share it. Atomic operations are far slower than plain ones. That's the modern form of EA's ref count storm: a `std::vector<std::shared_ptr<Mesh>>` passed by value to a function performs one atomic increment and one atomic decrement per element per call.

Use shared ownership when a resource genuinely has several owners with unrelated lifetimes, like a texture used by many materials that load and unload independently. [Week 7](w07-resource-management-and-hot-reload.md)'s resource cache is that case. Use `std::unique_ptr` or a plain owning member everywhere else.

### Relocation leaves pointers dangling

Section 3 counted what relocation costs. It also has a consequence that no counter shows. When a vector relocates, every pointer, reference and iterator into its old block now points at freed memory. Such a pointer is **dangling**: it still holds an address, but no live object is there.

```cpp
#include <cstdint>
#include <cstdio>
#include <vector>

struct Monster { int hp = 100; };

int main() {
    std::vector<Monster> monsters(4);             // size 4, capacity 4
    Monster* target = &monsters[0];               // the player's current target
    auto old_address = reinterpret_cast<std::uintptr_t>(target);

    monsters.push_back(Monster{});                // full: the vector relocates
    auto new_address = reinterpret_cast<std::uintptr_t>(&monsters[0]);

    std::printf("capacity now %zu, element 0 moved: %s\n",
                monsters.capacity(), old_address != new_address ? "yes" : "no");
    // target still holds old_address. Reading target->hp now is undefined behavior.
}
```

```
capacity now 8, element 0 moved: yes
```

The answer is always "yes", because the vector allocates the new block before it frees the old one. Reading `target->hp` afterwards is **undefined behavior**: the program may print 100, print garbage, or crash an hour later in unrelated code. This is the bug behind many "the target frame shows the wrong monster" reports. Ownership rules don't prevent it, because `target` never owned anything. The usual engine fix is to stop storing addresses and store a **handle** instead, a small index that the owner translates to an address at the moment of use. Week 3's pool allocator hands out blocks that never move, and [week 5](w05-entity-component-system-design.md) turns indices into safe entity handles.

## In-class activity (25 minutes)

Work in pairs on paper, then check with the compiler.

1. Your instructor gives you six short class definitions (a struct of floats, one with a `std::string`, one with a user-written destructor, one with a deleted copy constructor, one holding a `std::unique_ptr`, one holding a raw `char*` with a destructor that frees it). For each, predict: copyable? movable? Will `std::vector` move or copy it on growth? Is it safe? (10 min)
2. For each, write the `static_assert` line that would enforce your prediction (`std::is_nothrow_move_constructible_v`, `std::is_copy_constructible_v`). (5 min)
3. Paste all six into one file and compile. Every assert that fails is a wrong prediction. Fix the class, not the assert, where the class is unsafe. (10 min)

Expected output: a table of six predictions with the ones you got wrong marked, and the corrected raw-pointer class following the rule of five.

## Common misconceptions

- **"`std::move` moves the object."** It is only a cast. If the type has no usable move constructor, the copy constructor runs and nothing warns you.
- **"If I wrote a move constructor, vector uses it."** Only if it is `noexcept` (or the type can't be copied). Otherwise growth copies, as the 1,023 copies in section 3 show.
- **"Adding an empty destructor is harmless."** A user-declared destructor stops the compiler from generating move operations, so every move becomes a copy. `Logged` paid 1,024 extra allocations for one push.
- **"A moved-from object is empty."** For your own types, it is whatever you define. For standard library types it is valid but unspecified. Don't read it; assign to it or let it die.

## Check yourself

1. With libc++ (doubling), you push 5,000 textures of 256 KiB each into an empty vector with no `reserve`. How many relocations happen? How many bytes are copied if the move constructor is not `noexcept`? How many if it is (24-byte objects)?
2. A class holds `std::vector<float> weights;` and `std::string name;` and nothing else. How many of the five special member functions should you write? Will `std::vector` of this class move on growth?
3. You add `~Brain() { log("brain destroyed"); }` to the class in question 2. What changes when the vector grows, and what is the smallest fix?
4. A Godot `Vector<int>` of 1,000 elements is copied into 10 functions, and only the last function writes one element. Using this lecture's model, how many element copies happen in total? What would the count be with `LocalVector` passed by value?

<details>
<summary>Answers</summary>

1. Reallocations happen when the vector is full at sizes 1, 2, 4, ..., 4,096, so R = 8,191. Copies: 8,191 × 262,144 bytes = 2,147,221,504 bytes, about 2.0 GiB (2,047.75 MiB). Moves: 8,191 × 24 = 196,584 bytes, about 192 KiB.
2. None (rule of zero). Both members have `noexcept` move constructors, so the generated move constructor is `noexcept` and the vector moves.
3. The user-declared destructor suppresses the implicit move constructor, so growth copies both members of every element. Fix: add `Brain(Brain&&) noexcept = default;` and, to keep the class complete, `Brain& operator=(Brain&&) noexcept = default;` plus defaulted copy operations if you still want copying.
4. Copy-on-write: the ten copies cost no element copies, and the first write to a shared buffer copies all 1,000 elements once, so 1,000 in total. `LocalVector` passed by value deep-copies on each call: 10 × 1,000 = 10,000.

</details>

## Lab / assignment hook

[Lab 02, an owning buffer](../labs/lab02.md). You implement `PixelBuffer`, a class that owns heap memory, with all five special member functions, and `GpuTexture`, a move-only handle. The tests count allocations and copies, run under UndefinedBehaviorSanitizer (AddressSanitizer too, where it works on your machine), and fail if a vector of your buffers copies when it grows.

## Sources

- Pedriana, P. (2007). "EASTL: Electronic Arts Standard Template Library." WG21 paper N2271, open-std.org. Repository `electronicarts/EASTL` on GitHub (created December 2015, BSD 3-Clause). Motivation for a game-specific STL; "ref count storms" when containers of reference-counted objects are copied; the `has_trivial_relocate` trait and its relation to move semantics. Paraphrased; one short phrase quoted.
- cppreference.com, "std::vector::push_back" and "std::move_if_noexcept" (C++11 and later). The strong exception guarantee and the rule that a non-`noexcept` move is used only when the type is not copy-insertable.
- cppreference.com, "The rule of three/five/zero" and "Move constructors" (implicitly-declared move constructor not generated when a destructor is user-declared).
- LLVM libc++ source, `libcxx/include/__vector/vector.h`, `__recommend` (main branch, September 2026): new capacity is `max(2 × capacity, new size)`.
- GNU libstdc++ source, `bits/stl_vector.h`, `_M_check_len` (master, September 2026): grows by at least doubling.
- Microsoft STL source, `stl/inc/vector`, `_Calculate_growth` (main, September 2026): `capacity + capacity / 2`.
- Epic Games, Unreal Engine 5.8 documentation, "Array Containers in Unreal Engine." `TArray` is a value type and assumes elements are trivially relocatable.
- Godot Engine documentation (stable, 4.7), "Core types": `Vector` uses copy-on-write, `LocalVector` does not, and containers assume trivially relocatable elements.
- Gregory, J. (2018). *Game Engine Architecture* (3rd ed.). CRC Press. Sections 3.1 and 3.3.
- Measurements in section 3 (copy and move counts, allocation counts, 2.2 ms vs 0.8 ms) were produced by the code shown, compiled with Apple clang 17 (libc++) at `-O2` on an Apple M4 Pro, September 2026. Your timings will differ; your counts should not, except on Microsoft STL, where the relocation counts follow the ×1.5 row of the table.

## Interactive spec: examples/w02-vector-growth.html

**The one insight:** the container decides *how many* elements move when it grows; the element type decides *how many bytes* each move costs, and one missing `noexcept` turns 24 bytes into the whole payload.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **Left view, "Size and capacity".** x axis: elements pushed, 0 to `n`. y axis: element slots. Draw size as a diagonal line and capacity as a staircase. Mark each reallocation with a dot on the staircase and a thin vertical tick. Under the plot: "Reallocations: X   Relocations R(n): Y   Final capacity: Z".
- **Right view, "Bytes relocated".** x axis: elements pushed, same range. y axis: cumulative bytes relocated, with a toggle between linear and log scale (default linear). Two lines: "copy" (warning color) and "move" (accent color). Only the active line is solid; the inactive one is drawn dashed and faded, so both are always visible for comparison. Under the plot: exact totals for both, in bytes and in MiB/KiB (two decimals), plus "ratio copy/move".

**Controls.**
- Slider "Elements `n`": 1 to 10,000, default 1,000; with a number input beside it.
- Radio "Growth policy": "×2 (libc++, libstdc++)" (default) and "×1.5 (Microsoft STL)".
- Select "Payload per element": 1 KiB, 16 KiB, 64 KiB (default, "128×128 RGBA icon"), 256 KiB, 4 MiB ("1024×1024 RGBA").
- Checkbox "Move constructor is `noexcept`" (default off, so the first screen shows the copy line climbing).
- Checkbox "`reserve(n)` first" (default off).
- Text line that updates with the controls: "This vector will COPY / MOVE when it grows", with the reason ("move constructor not noexcept, type is copyable" or "noexcept move").

**Exact model.**
```
size = capacity = relocated = reallocs = 0
if reserve: capacity = n
for i in 0..n-1:
  if size == capacity:
    capacity = max(grow(capacity), size + 1)    # grow(c) = 2c or c + floor(c/2)
    relocated += size; reallocs += 1
  size += 1
bytes_copy = relocated × payload_bytes
bytes_move = relocated × 24
```

**Test values** (payload 64 KiB = 65,536 bytes).
- ×2, n = 1,000: reallocs 11, R 1,023, capacity 1,024, copy 67,043,328 B (63.94 MiB), move 24,552 B (23.98 KiB), ratio 2,730.7.
- ×1.5, n = 1,000: reallocs 18, R 2,137, capacity 1,066, copy 140,050,432 B (133.56 MiB), move 51,288 B.
- ×2, n = 10: reallocs 5, R 15, capacity 16. ×1.5, n = 10: reallocs 7, R 25, capacity 13.
- ×2, n = 10,000: R 16,383. ×1.5, n = 10,000: R 24,284, capacity 12,138.
- ×2, n = 5,000, payload 256 KiB: R 8,191, copy 2,147,221,504 B (2,047.75 MiB).
- Any policy with `reserve` ticked: reallocs 0 (the reserve itself is not counted), R 0, both totals 0.

**First screen.** n = 1,000, ×2, 64 KiB, `noexcept` off: the copy line has reached 63.94 MiB and the caption reads "1,023 relocations × 64 KiB. Tick noexcept to make each one 24 bytes."
