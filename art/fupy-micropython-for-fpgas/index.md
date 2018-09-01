---
date: '2018-09-01'
layout: draft
tags:
    - micropython
    - c
title: 'FuPy: MicroPython for FPGAs'
summary: "FuPy is a port of MicroPython which runs inside an FPGA.  I take a look at it and try to get my head around how to program for it ..."
---

[FuPy](https://fupy.github.io/) is a port of [MicroPython](https://micropython.org/)
which runs on a [Soft Microprocessor](https://en.wikipedia.org/wiki/Soft_microprocessor) core
implemented on an [FPGA](https://en.wikipedia.org/wiki/Field-programmable_gate_array).

It builds on three other projects:

* [Migen](https://m-labs.hk/migen/), a Python tool for VLSI design, an alternative to VHDL and Verilog.
* MiSoC, a system-on-chip library for Migen with lots of peripherals in Migen
  and LM32 and OpenRISC cores (written in Verilog)
* [Litex](https://github.com/enjoy-digital/litex), a build system for Migen designs
  (not to be confused with the swimwear company, ballistic armour company or the football team)
 
I don't know a lot about FPGAs, but I was fortunate enough to have Tim and Ewen introduce me
to FuPy at [PyConAU 2018](../pycon-2018-sydney/).
Ewen has documented the process of
[building FuPy for Mimas V2 and Artix A7 FPGAs](https://ewen.mcneill.gen.nz/blog/entry/2018-01-17-fupy-fpga-micropython-on-mimas-v2-and-arty-a7/)
so this post starts up where that one leaves off: we have a build toolchain, and an Artix A7
board flashed with MicroPython, so let's go from there.

# Building

Summary of steps from Ewen's instructions for Artix 7:

* Install Xilinx toolchain to /opt/Xilinx
* set up environment (I use [direnv](https://direnv.net/)):
  * CPU=lm32
  * PLATFORM=arty
  * TARGET=base
  * FIRMWARE=micropython
* git clone https://github.com/timvideos/litex-buildenv.git
* cd litex-buildenv
* scripts/download-env.sh
* sudo scripts/download-env-root.sh
* source scripts/enter-env.sh
* make gateware
* scripts/build-micropython.sh
* make gateware-load
* make firmware-load

The Xilinx tools are almost 6GB and the `scripts/download-env.sh` step downloads
another couple of GB.
The `make gateware` step is pretty CPU intensive as it tries to work out how to 
fit all the stuff you asked for onto the FPGA.
This may not be the best project to try out on the aeroplane.

On Ubuntu 18.04, the `scripts/build-micropython.sh` step (or even just
running `lm32-elf-newlib-gcc`) crashes out with a message:

```
lm32-elf-newlib-gcc: loadlocale.c:130: _nl_intern_locale_data:
Assertion `cnt < (sizeof (_nl_value_type_LC_TIME) /
sizeof (_nl_value_type_LC_TIME[0]))' failed.
```

This seems to be some kind of glibc error loading locales.  Thanks to the hint in
[this stack exchange](https://unix.stackexchange.com/questions/444102/loadlocale-c-nl-intern-locale-data-assertion-error)
post I found that either setting `LANG=/usr/locale/C.UTF-8/` (just for this command)
or installing the Ubuntu `locales-all` package would fix this problem.

If it gets stuck at the `[FLTERM] Starting...` message try pressing the hardware reset button, 

Folllowing these instructions gets us as far as a serial REPL running on the Arty, 
from which we can flash an LED:

```
>>> import litex
>>> led1 = litex.LED(1)
>>> led1.on()
>>> led1.off()
```

Okay, so that's not the most exciting thing in the world, but its something!

# Files & Repositories

Before we change anything we've got to work out what's where.

The [Litex Buildenv](https://github.com/timvideos/litex-buildenv.git) repository pulls in 
a whole bunch of toolchain stuff as submodules, and also the build scripts pull in other
modules including [FuPy](https://github.com/fupy/micropython.git).  All up there's about
2.5GB of stuff in this build directory now.

## Platforms

The `platforms/` directory contains descriptions of the pin assignments for various
development platforms, for example `platforms/arty.py` contains (in part):

```python
_io = [
    ("user_led", 0, Pins("H5"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("J5"), IOStandard("LVCMOS33")),
    # ...
    ("user_sw", 0, Pins("A8"), IOStandard("LVCMOS33")),
    # ...
    ("user_btn", 0, Pins("D9"), IOStandard("LVCMOS33")),
    # ...
    ("serial", 0,
        Subsignal("tx", Pins("D10")),
        Subsignal("rx", Pins("A9")),
        IOStandard("LVCMOS33")),
    # ...
]
```

These definitions map the [ridiculous number of I/O pins](https://www.xilinx.com/products/boards-and-kits/arty.html#hardware)
to the [development board hardware](https://reference.digilentinc.com/reference/programmable-logic/arty/reference-manual?redirect=1#basic_io).
User LED 0 is connected on pin H5, and expects CMOS 3.3V voltages.  Etc.

## Targets / Gateware

The `targets/` directory contains descriptions of the SoC used on the target boards,
pulling in submodules which implement individual bits of hardware.  A lot of stuff is
under the 'CAS' ("Control and Status") module.

The `gateware/` directory contains implementations for the hardware. For example, 
`gateware/cas.py` includes code to enumerate all the LEDs defined in the `platforms/*.py` file,
and turn them into constructs which can be compiled into the FPGA.

I'm still finding my way around this code ...

When you `make gateware`, it is compiled into a binary description of the configuration of the
gates on the FPGA, sometimes known as a "bitstream". 

## CSR

The compilation step also produces a mapping of "Control Status Registers" aka CSR.
The gateware defined above is mapped into the softcore's memory, and accessed by memory reads
and writes, just like on a lot of microcontrollers.

The CSR map is written out as:

* C header file format: `build/arty_base_lm32/software/include/generated/csr.h`
* CSV tabular format: `build/arty_base_lm32/test/csr.csv`
* [devicetree](https://elinux.org/Device_Tree_Reference) (?)

## MicroPython

Finally, we can build micropython.  It is downloaded into 
`third_party/micropython/` and the FuPy port is at `ports/fupy`.
`modlitex.c` includes `csr.h` (see above) and uses that to find registers.






