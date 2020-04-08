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

## Microarchitecture

[RISC](https://en.wikipedia.org/wiki/Reduced_instruction_set_computer)
[Pentium Pro](https://en.wikipedia.org/wiki/Pentium_Pro#Summary)

### Multi-CPU machines

[160 ARMs](https://www.servethehome.com/ampere-altra-80-arm-cores-for-cloud/)

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

## VLIW and OISC and ...

[MISC](https://en.wikipedia.org/wiki/Minimal_instruction_set_computer)
[VLIW](https://en.wikipedia.org/wiki/Very_long_instruction_word)
[OISC](https://en.wikipedia.org/wiki/Single_instruction_computer)

[FPGAs](/tag/fpga/)

## ... CUDA, oh my!

[CUDA](https://en.wikipedia.org/wiki/CUDA)
[programming in CUDA](/art/nvidia-jetson-nano-experiments/#my-first-cuda)
