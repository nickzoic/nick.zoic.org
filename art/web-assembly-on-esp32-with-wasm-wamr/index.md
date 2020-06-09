---
date: '2020-02-05'
layout: article
tags:
  - esp32
  - www
title: 'Web Assembly (WASM) on ESP32 with WAMR'
summary: porting WAMR to run WebAssembly on an $5 ESP32 CPU
---

I happened to notice the recent release of 
[WAMR](https://github.com/bytecodealliance/wasm-micro-runtime),
"a standalone WebAssembly (WASM) runtime" with interpreter plus
AoT and JIT compilers.  And I happened to notice it has support
for [XTENSA](https://en.wikipedia.org/wiki/Tensilica) chips ...

So naturally I figured I should try and work out how to
[port WAMR to ESP32](https://github.com/nickzoic/wasm-micro-runtime/tree/wamr-for-esp-idf)
so we can run WASM on super cheap silicon!

This article exists as a list of resources which I used along the way.

## Compiling ESP-IDF for ESP32

I've been working with [ESP-IDF v4.0-rc](https://github.com/espressif/esp-idf/tree/v4.0-rc)
which hopefully is not far off becoming the official 4.0 release.  Version 4 uses
[CMake](https://cmake.org/) as its primary build tool, and while I'm not that keen on it
I figured I'd better bite the bullet and get used to it.

There's some advice in the documentation on
[Using ESP-IDF in Custom CMake Projects](https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/build-system.html#using-esp-idf-in-custom-cmake-projects)
which proved quite useful ... the first step was to get this building with CMake and 
printing "Hello, World!", from the `product-mini/platforms.esp-idf/` directory.

I wasted a lot of time starting from the 'normal' esp-idf CMake file, which wasn't the
right choice at all for this kind of project.
Thanks [Seon](https://unexpectedmaker.com/) for sending a MicroPython-with-CMake example
and Gus for helping get unstuck.

This also involved updating to a newer `xtensa-esp32-elf-gcc`, via the weird
installer script.  If you don't want to run the install script, you can work out the
[xtensa esp32 toolchain URLs here](https://github.com/espressif/esp-idf/blob/master/tools/tools.json)
[Version 8.2.0](https://dl.espressif.com/dl/xtensa-esp32s2-elf-gcc8_2_0-esp-2019r2-linux-amd64.tar.gz)
worked for me.

## Mashing up WAMR

WAMR is also build with CMake, which means to build the two together you have to
[mash up](http://www.djbc.net/index.html#)
the ESP-IDF `CMakeLists.txt` with the WAMR `CMakeLists.txt`.  I mostly worked
from the linux and zephyr WAMR platforms and tried to work out what was needed as I 
went along ...

As always, I spent a maddening amount of time running in circles before finding 
something which worked well enough:  well, it compiles and I can always clean it up later.

One very good hint I got along the way (thanks [Jimmo](https://github.com/jimmo/))
is to quarantine CMake off into its own `build` directory by doing something like

```
mkdir build
cd build
cmake ..
make 
```

which made a huge difference as now I could repeatably blow away the builds and start
over when CMake got confused.  It's a little thing, but it makes a big difference.

## Building a platform

The main entry point `product-mini/platforms/esp-idf/main.c` is responsible for starting
up the WASM subsystem and passing it some code to run.  For now, this code is just compiled
in from a byte array in `test_wasm.h`, but eventually I'll add file system support so it can
live separately.  It's closely based on the other platforms with a little bit of input
from [MicroPython](https://micropython.org/)'s ESP32 port.

There's a whole bunch of platform specific implementation in `core/shared/platform/esp-idf/`
(Yeah, I'm not a big fan of the directory naming and layout either.)
First I just stubbed these in with a bunch of `return 0` type code and then I'll come back
through to add implementations for time function and threading and so on.

For very basic programs, the VM is quite tolerant of missing features, so if you're porting
to some other platform don't get too stressed about gettime semaphores right before you
say hello ...

```
I (259) cpu_start: Compile time:     Feb  5 2020 16:00:36
I (271) cpu_start: ESP-IDF:          v4.0-rc
I (344) cpu_start: Starting scheduler on PRO CPU.
wasm_runtime_load
wasm_runtime_instantiate
wasm_application_execute_main
Hello world!
CORRUPT HEAP: multi_heap.c:431 detected at 0x3ffd4610
abort() was called at PC 0x4008969d on core 0
```

There are also apis to native functions in `product-mini/platforms/esp-idf/ext_lib_export.c`.
More on those later.

## Compiling Code

There's an example `test_wasm.h` which prints `Hello world!`, and getting that to execute was
a very exciting moment.  But really understanding how this platform works requires a lot more!

Webassembly can be generated in a few different ways:

* [Compiling Rust to WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly/Rust_to_wasm)
* [Compiling C to WebAssembly without Emscripten](https://dassur.ma/things/c-to-webassembly/)
* [WASI SDK](https://github.com/CraneStation/wasi-sdk)

... and [very many others](https://github.com/appcypher/awesome-wasm-langs)

For the moment all I want to do is produce something *slightly* nicer than Hello World ...
that's right, I want to blink an LED!  So the next step is to work out how to compile my
own code and pass it to WAMR for execution.

This is where WASM gets a little ... confusing.
It's surprisingly low-level, with things like `__stack_pointer` exposed.
But the code in `product_mini/app_samples/hello_world/build.sh` turned
out to be revealing, and what eventually worked for me was:

```
clang-8 --target=wasm32 -O3 -z stack-size=4096 -Wl,--initial-memory=65536 --sysroot=../../../../wamr-sdk/app/libc-builtin-sysroot -Wl,--allow-undefined -Wl,--export=main, -Wl,--no-threads,--strip-all,--no-entry -nostdlib -o test.wasm test.c
xxd -i test.wasm > test.h
```

`xxd` is a very useful file transforming utility, which in this case is used to spit out a header-file formatted version of the wasm bytecode.

`clang` I just installed from the ubuntu package, but I found that
the `wasm2wat` utility was too out of date so I installed that from
source.

There's a couple of open problems at this point:

* `printf("string!")` works fine, but `printf("hello %d", n)`
  crashes the port.
  The same WASM works okay in the linux port, so I'm not sure why.
* The port crashes & restarts when `main` returns.


## JIT and AOT with LLVM

Much of the point of this little effort was to get JIT working,
and it turns out that that might be harder than I thought.
The JIT code uses LLVM, and mainline LLVM doesn't yet support Xtensa.
There's a [LLVM for Xtensa](https://github.com/espressif/llvm-project)
under development so I'm building that, which on my laptop is
*not* a fast process.

To actually run this code it's got to target Xtensa but also the
libraries themselves have to be compiled for Xtensa.
Something like this might work:

```
cmake -DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD="Xtensa" -DLLVM_TARGET_ARCH="Xtensa" -DLLVM_BUILD_LLVM_DYLIB="ON" ~/Work/llvm-project-xtensa/llvm/
```

After a bit more research and advice, it looks like the JIT option won't really 
be practical as it'll have to build a lot of LLVM in to the runtime ... and LLVM
is not small.  However AoT is still on the agenda!

# WORK IN PROGRESS

This article is a work in progress, and now you're up to where I'm up to!

Check back later, or [follow me on twitter](https://twitter.com/nickzoic/) for updates.

There's also an open [XTensa / FreeRTOS support](https://github.com/bytecodealliance/wasm-micro-runtime/issues/134) issue on WAMR.

See also work done in [Wasm3](https://github.com/wasm3/wasm3) to support ESP32,
for example [this repo](https://github.com/vshymanskyy/Wasm3_RGB_Lamp)
and [this tweet](https://twitter.com/alvaroviebrantz/status/1221618910803513344)

## UPDATES

* Fixed up attributions for the `cmake ..` hint 
* Added some refs to other projects
