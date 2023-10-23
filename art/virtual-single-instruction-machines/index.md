---
date: '2022-03-29'
layout: article
tags:
    - languages
    - speculation
title: 'Virtual Single Instruction Machines'
summary: "A different way of looking at Virtual Machine design to avoid a big if/elsif selector"
---

## Background

I've become a bit fascinated by Virtual Machines.

I started writing this article on 29 February 2020 ... oh, what a couple of years it has been!
But it's still an interesting topic, so over two years later I'm revisiting it ...

### Virtual Machines

I'd always thought of them as [quite silly things](https://en.wikipedia.org/wiki/Esoteric_programming_language), a 
[means to a commercial end](https://en.wikipedia.org/wiki/Java_virtual_machine), or maybe
just a thing you did when you had more
[MIPS](https://en.wikipedia.org/wiki/Instructions_per_second#Millions_of_instructions_per_second_(MIPS))
than [Real](https://www.xkcd.com/378/)
[Programmers](https://en.wikipedia.org/wiki/Real_Programmers_Don%27t_Use_Pascal) available.

But then I read about the [Apollo Guidance Computer Software](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer#Software):

    The AGC also had a sophisticated software interpreter [...]
    that implemented a virtual machine with more complex and
    capable pseudo-instructions than the native AGC. These
    instructions simplified the navigational programs.
    Interpreted code [...] could be mixed with native AGC code.

    While the execution time of the pseudo-instructions was
    increased [...] the interpreter provided many more instructions
    than AGC natively supported and the memory requirements were
    much lower than [...] the AGC native language

So, this very early computer, with its programs stored in only a few kilobytes of
[woven memory](https://en.wikipedia.org/wiki/Core_rope_memory), somehow benefited from
these effete modern techniques?  Hmmm ...

Similarly working on [implenting the Gigatron on FPGA](/art/migen-gigatron/) revealed
a really interesting thing: the virtual machine implementation can be *tiny*, so small
that the space saved by using bytecodes compared to native code exceeds the size of the 
virtual machine itself.

### Microarchitecture

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

### MicroPython Virtual Machine

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
instead of the giant switch/case if they're available) 

Modern CPUs are [superscalar](https://en.wikipedia.org/wiki/Superscalar_processor) though, 
with each instruction sequenced through a long "pipeline" of execution units. Having jumps every
few instructions reduces the ability of the CPU to optimize the pipelining of instructions.
So bytecode is quite inefficient, but it is convenient because you can interpret the 
same bytecodes on x86 or ARM or Tensilica or whatever platform is convenient.

An alternative is to take the bytecode and translate it into native machine code either 
"ahead of time" (AoT) or "just in time" (JIT).  JIT compilation is particularly interesting
because it is possible to only compile functions which are run many times, and/or to 
track the conditions under which a function is run and specialize the compiled code to run
faster under those conditions.

For example, Web Assembly with [WASM](../web-assembly-on-esp32-with-wasm-wamr/) can do AoT or JIT compilation
but unfortunately uses [LLVM](https://llvm.org/) to do so, which is a bit too heavy to be interesting to me.


### OISC and VLIW and ...

Okay, back to hardware architectures.  We already mentioned *reduced* instruction sets but
how big is a [Minimal Instruction Set](https://en.wikipedia.org/wiki/Minimal_instruction_set_computer)?
It turns out that if you push the definition of "instruction set" hard enough, you can get 
down to *[one instruction](https://en.wikipedia.org/wiki/Single_instruction_computer)* and still have 
a turing-complete machine.

This is possible because the instruction does several things all in one go: for example in the
["Subtract and branch if less than or equal to zero"](https://en.wikipedia.org/wiki/One-instruction_set_computer#Subtract_and_branch_if_less_than_or_equal_to_zero) OISC, every single instruction is just a tuple of addresses (`a`, `b`, `c`)
and to evaluate the tuple, the processor subtracts the value at `a` from the value at `b`, stores the 
result in `b` and then jumps to address `c` if the result was less than or equal to zero.
Other, more conventional instructions can then be defined in terms of multiple subtract-and-branch instructions.

This may seem all a bit like a hand-waving thought experiment, a turing tarpit for silicon instead
of tape, but supercomputing has found a use for a related idea,
[Very Long Instruction Words (VLIW)](https://en.wikipedia.org/wiki/Very_long_instruction_word).

CPUs have multiple "execution units" which can operate in parallel, and usually in CISC systems the CPU
is expected to coordinate the work of execution between these execution units.  In a VLIW architecture,
each instruction explicitly tells each execution unit what to do, and the compiler is expected to work
out the details.
(The name comes about because there's a lot of details, so the instructions get pretty wide)

Of course that means the compiler has to know a lot of very specific stuff about the exact
disposition of capabilities of the CPU, and therefore you can't upgrade the CPU without compiling everything,
etc, etc, and that's why it probably isn't practical except as a target for a JIT compiler or
[binary translator](https://en.wikipedia.org/wiki/Binary_translation).

## Virtual Single Instruction Machines

OK, so we've seen that one cause of inefficiency in bytecode execution is the execution of
a big switch/case or a big computed goto at the core of the virtual machine, and I've talked
a bit about CPU architectures some similar problems.

What I'm proposing here is replacing the CISC-like bytecode with a VLIW-like code, where each instruction word 
modifies the behaviour but not the control flow of a very small virtual processor loop.

For example, a line of Python code like:

    d = a * 107 + 42

might be assembled by cpython to a series of bytecodes like:

              0 LOAD_GLOBAL              0 (a)
              3 LOAD_CONST               1 (107)
              6 BINARY_MULTIPLY     
              7 LOAD_CONST               2 (42)
             10 BINARY_ADD          
             11 STORE_FAST               1 (d)

This would mean several passes around the big process-an-opcode loop, one per instruction.
How about if we instead had a single opcode which did several things, for example we could
have a `LOAD_MULTIPLY_ADD_STORE` instruction which would do everything in that bit of code
in one go, with no branches. It seems like a contrived example, but a lot of numeric code
is very repetitive in this way.

If you don't need to multiply?  Multiply by one.  If you don't need to add?  Add zero.
If you don't need to load a value, load 0 from a constant location
(like [MIPS R0](https://en.wikipedia.org/wiki/MIPS_architecture#Registers))

Maybe we can take this a bit further, like OISC, and have a single execution block which
does *everything all at once*, with no pipeline-stalling branches. This seems ridiculous,
but if you consider [MicroPython ByteCode](https://github.com/micropython/micropython/blob/master/py/bc0.h)
there's really not that many kinds of bytecode ops:

* Constant Loads
* Heap Loads
* Unary / Binary Operators
* External Calls
* Heap Stores
* Stack Manipulation
* Structure Manipulation
* Branches.

Operators are already just C function calls (eg: something like `top = mp_binary_op(op, lhs, rhs)` so that's easy.

So, our "single instruction" turns out something like `load-operate-store-pushpop-branch`.  It's fewer instructions,
and even though those instructions are longer, that's less laps around the VM loop.  If we pick our operations
carefully, it's possibly more efficient!






