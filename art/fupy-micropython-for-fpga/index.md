---
date: '2018-09-01'
layout: draft
tags:
    - micropython
    - c
title: 'FuPy: MicroPython for FPGAs'
summary: "FuPy is a port of MicroPython which runs inside an FPGA.  I take a look at it and try to get my head around how to program for it ..."
---

*Thanks to [Tim Ansell](https://mithis.com/) and [Ewen McNeill](https://ewen.mcneill.gen.nz/blog/)
for their help getting my head around FuPy and correcting my misunderstandings.
Remaining mistakes are all my own!*

[FuPy](https://fupy.github.io/) is a port of [MicroPython](https://micropython.org/)
which runs on a [Soft Microprocessor](https://en.wikipedia.org/wiki/Soft_microprocessor) core
implemented on an [FPGA](https://en.wikipedia.org/wiki/Field-programmable_gate_array).

It builds on four other projects:

* [Migen](https://m-labs.hk/migen/), a Python tool for VLSI design.
  It provides an alternative to designing chips in VHDL or Verilog.
  Migen includes a system-on-a-chip library called MiSoC.
* [LiteX](https://github.com/enjoy-digital/litex), a fork of MiSoC which includes lots
  of peripherals implemented in Migen and a choice of CPU cores such as
  [LatticeMico32](https://en.wikipedia.org/wiki/LatticeMico32),
  [OpenRISC](https://openrisc.io/) and [RISC-V](https://en.wikipedia.org/wiki/RISC-V),
  mostly written in Verilog.
* [LiteX Buld Env](https://github.com/timvideos/litex-buildenv), a build system for LiteX SoC
  designs.
* [MicroPython](https://micropython.org/) a Python 3 implementation for resource-limited
  systems. The [FuPy MicroPython fork](https://github.com/fupy/micropython/) adds support
  for FPGA-based systems.
 
I don't know a lot about FPGAs, but I was fortunate enough to have Tim and Ewen introduce me
to FuPy at [PyConAU 2018](../pycon-2018-sydney/).
Ewen has documented the process of
[building FuPy for Mimas V2 and Artix A7 FPGAs](https://ewen.mcneill.gen.nz/blog/entry/2018-01-17-fupy-fpga-micropython-on-mimas-v2-and-arty-a7/) and there's a
[HowTo FuPy Arty A7](https://github.com/timvideos/litex-buildenv/wiki/HowTo-FuPy-Arty-A7) doc on the litex-buildenv Wiki,
so this post starts up where those ones leaves off: we have a build toolchain, and an 
[Arty A7](https://store.digilentinc.com/arty-a7-artix-7-fpga-development-board-for-makers-and-hobbyists/)
board flashed with FuPy MicroPython, so let's go from there.

# Building

Summary of steps from Ewen's instructions for Artix 7:

* Install Xilinx toolchain to /opt/Xilinx.
  * see [Ewen's instructions to get Xilinx ISE WebPack](https://ewen.mcneill.gen.nz/blog/entry/2017-03-06-numato-mimas-v2-from-linux/)
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

The Xilinx tools are about 16GB (!) and the `scripts/download-env.sh`
step downloads another couple of GB.
The `make gateware` step is pretty CPU intensive as it tries to work out how to 
arrange all the stuff you asked for onto the FPGA efficiently.
It's a good way to get the dust out of your laptop's CPU fan.
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

* C header file format: `build/arty_base_lm32/software/include/generated/csr.h` ...
  macro defines and wrapper functions for each register to make them available from C functions
* CSV tabular format: `build/arty_base_lm32/test/csr.csv` ... the same information in
  tabular form.
* Possibly, in the future,
  [LiteX could generate a DeviceTree](https://github.com/timvideos/litex-buildenv/wiki/DeviceTree)
  and MicroPython could read that to discover the register mappings.

## MicroPython

Finally, we can build micropython.  It is downloaded into 
`third_party/micropython/` and the FuPy port is at `ports/fupy`.

The module `litex_leds.c` includes `csr.h` (see above) and uses that to find the
registers corresponding to the LEDs.







