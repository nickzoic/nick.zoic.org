---
date: '2020-02-29'
layout: draft
tags:
    - languages
    - speculation
title: 'Virtual Single Instruction Machines'
summary: "A different way of looking at Virtual Machine design to avoid a big if/elsif selector"
---

## Background

I've become a bit fascinated by Virtual Machines.

I'd always thought of them as [quite silly things](https://en.wikipedia.org/wiki/Esoteric_programming_language), a 
[means to a commercial end](https://en.wikipedia.org/wiki/Java_virtual_machine), or maybe
just a thing you did when you had more
[MIPS](https://en.wikipedia.org/wiki/Instructions_per_second#Millions_of_instructions_per_second_(MIPS))
than [Real](https://www.xkcd.com/378/)
[Programmers](https://en.wikipedia.org/wiki/Real_Programmers_Don%27t_Use_Pascal) available.

But then I read about the [Apollo Guidance Computer Software](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer#Software):

    The AGC also had a sophisticated software interpreter [...]
    that implemented a virtual machine with more complex and capable pseudo-instructions
    than the native AGC. These instructions simplified the navigational programs.
    Interpreted code [...] could be mixed with native AGC code.

    While the execution time of the pseudo-instructions was increased [...]
    the interpreter provided many more instructions than AGC natively supported
    and the memory requirements were much lower than [...] the AGC native language

so this very early computer, with its programs stored in only a few kilobytes of
[woven memory](https://en.wikipedia.org/wiki/Core_rope_memory), somehow benefited from
these effete modern techniques?  Hmmm ...

Similarly working on [implenting the Gigatron on FPGA](/art/migen-gigatron/) revealed
a really interesting thing: the virtual machine implementation can be *tiny*, so small
that the space saved by using bytecodes compared to native code exceeds the size of the 
virtual machine itself.

## Interpreters, JIT and AoT


## Microarchitecture

Back in the early days of CPU architecture, a lot of programming was done in 
assembly code, and CPU designers included lots and lots of 
[complexity](https://en.wikipedia.org/wiki/Complex_instruction_set_computer)
to make life easier for assembly language programmers.
As compilers became the 'normal' way to program, 
[RISC](https://en.wikipedia.org/wiki/Reduced_instruction_set_computer) architectures
became more popular, shifting the complexity from CPU to compiler.

The wildly popular [Intel x86](https://en.wikipedia.org/wiki/X86) family, however,
were anything but RISCy, with baroque instructions such as
[REPNE SCASB](https://stackoverflow.com/questions/26783797/repnz-scas-assembly-instruction-specifics)
(repeat while non-zero scan string byte, basically the C `strlen()` function in a
single instruction).

The [Windows/Intel](https://www.wired.com/2017/03/wintel-going-not-dead-yet/) alliance
made it almost impossible to migrate away from x86, but also demanded continuing
increase in CPU performance. And so, starting with the
[Pentium Pro](https://en.wikipedia.org/wiki/Pentium_Pro#Summary)
Intel shifted to running a
[RISC-like microarchitecture](https://en.wikipedia.org/wiki/P6_(microarchitecture))
with microinstructions decoded on the fly from regular x86 instructions.

Translating complex instructions into sequences of simple microinstructions?
Sounds suspiciously like a virtual machine.


## MicroPython Virtual Machine

I've been [doing a bit with MicroPython](/tag/micropython/) lately, and one of the
curious things about it is once you strip away all the clever interfaces to the
rest of the universe, you're left with a tiny
[MicroPython Virtual Machine](https://github.com/micropython/micropython/blob/master/py/vm.c)

At it's core lies an enormous switch/case which looks something like:

```C
dispatch_loop:
    switch (*ip++) {
        case MP_BC_LOAD_CONST_FALSE:
            ++sp = mp_const_false;
            goto dispatch_loop;
        case MP_BC_LOAD_CONST_NONE:
            ++sp = mp_const_none;
            goto dispatch_loop;
/* ... */
```

... and so on and so forth for all 81 of the Micropython Bytecodes.

It isn't especially exciting, there's probably lots of things we could do to
speed it up for one architecture or another (there's already some C-macro complexity
to use
[computed gotos](https://eli.thegreenplace.net/2012/07/12/computed-goto-for-efficient-dispatch-tables)
instead of thw switch/case if they're available) 

## VLIW and OISC and ...

[MISC](https://en.wikipedia.org/wiki/Minimal_instruction_set_computer)
[VLIW](https://en.wikipedia.org/wiki/Very_long_instruction_word)
[OISC](https://en.wikipedia.org/wiki/Single_instruction_computer)

[FPGAs](/tag/fpga/)

## ... CUDA, oh my!

[CUDA](https://en.wikipedia.org/wiki/CUDA)
[programming in CUDA](/art/nvidia-jetson-nano-experiments/#my-first-cuda)

### Multi-CPU machines

[160 ARMs](https://www.servethehome.com/ampere-altra-80-arm-cores-for-cloud/)
