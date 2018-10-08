---
date: '2018-09-26'
layout: article
tags:
    - micropython
    - c
title: 'FuPy: MicroPython for FPGAs'
summary: "FuPy is a port of MicroPython which runs inside an FPGA.  I take a look at it and try to get my head around how to program for it ..."
---

*Thanks to [Tim 'mithro' Ansell](https://mithis.com/) and
[Ewen McNeill](https://ewen.mcneill.gen.nz/blog/)
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
to FuPy at [PyConAU 2018](../pycon-2018-sydney/)
and provide a [Digilent Arty A7](https://store.digilentinc.com/arty-a7-artix-7-fpga-development-board-for-makers-and-hobbyists/)
board to play with, so let's go from there:

# Building

Summary of steps from [Ewen's instructions for Artix 7](https://ewen.mcneill.gen.nz/blog/entry/2018-01-17-fupy-fpga-micropython-on-mimas-v2-and-arty-a7/) and the
[HowTo FuPy Arty A7](https://github.com/timvideos/litex-buildenv/wiki/HowTo-FuPy-Arty-A7) doc on the litex-buildenv Wiki:

* [Download Xilinx Vivado HLx 2018.2 WebPACK Installer](https://www.xilinx.com/support/download.html)
  * Install to `/opt/Xilinx/`
  * Vivado is the tool you need to program the Artix 7.
  * WebPACK is the name for the zero-cost version.  
  * The 100MB download is just the installer, the whole bundle is 17GB.
  * I am greatly looking forward to using a platform with a compact, free toolchain.
* set up environment (I use [direnv](https://direnv.net/)):
  * CPU=lm32
  * PLATFORM=arty
  * TARGET=base
  * FIRMWARE=micropython
* git clone https://github.com/timvideos/litex-buildenv.git
* cd litex-buildenv
* scripts/download-env.sh
  * This step downloads another couple of GB.
* sudo scripts/download-env-root.sh
  * This just installs the timvideos PPA and various packages
* source scripts/enter-env.sh
* make gateware
* scripts/build-micropython.sh
* make gateware-load
* make firmware-load

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

Following these instructions gets us as far as a serial REPL running on the Arty, 
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
under the 'CAS' ("Control and Status", or sometimes "Configuration and Status") module.

The `gateware/` directory contains implementations for the hardware. For example, 
`gateware/cas.py` includes code to enumerate all the LEDs defined in the `platforms/*.py` file,
and turn them into constructs which can be compiled into the FPGA.

I'm still finding my way around this code ...

When you `make gateware`, it is compiled into a binary description of the configuration of the
gates on the FPGA, sometimes known as a "bitstream".  This is a very slow step because the
compilation process involves finding an optimal way to arrange the logic you've asked for onto the 
available logical units ... careful arrangement leads to higher clock speeds.

## CSR

The compilation step also produces a mapping of "Control Status Registers" aka CSR.
The gateware defined above is mapped into the softcore's memory, and accessed by memory reads
and writes, just like on a lot of microcontrollers.

The CSR map is written out as:

* C header file format: `build/arty_base_lm32/software/include/generated/csr.h` ...
  macro defines and wrapper functions for each register to make them available from C functions
* CSV tabular format: `build/arty_base_lm32/test/csr.csv` ... the same information in
  tabular form.

For example, the LEDs above end up being written out as something like this in `csr.h`:

```C
#define CSR_CAS_BASE 0xe0006800
#define CSR_CAS_LEDS_OUT_ADDR 0xe0006800
#define CSR_CAS_LEDS_OUT_SIZE 1
static inline unsigned char cas_leds_out_read(void) {
        unsigned char r = MMPTR(0xe0006800);
        return r;
}
static inline void cas_leds_out_write(unsigned char value) {
        MMPTR(0xe0006800) = value;
}
```

## MicroPython

Finally, we can build micropython.  It is downloaded into 
`third_party/micropython/` and the FuPy port is at `ports/fupy`.

The module `litex_leds.c` includes `csr.h` (see above) and uses that to find the
registers corresponding to the LEDs.  These are then wrapped up into Python calls:

```C
STATIC mp_obj_t litex_led_on(mp_obj_t self_in) {
        litex_led_obj_t *led = self_in;
        char value = cas_leds_out_read();

        cas_leds_out_write(value | (1 << (led->num - 1)));

        return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(litex_led_on_obj, litex_led_on);
```

... and this gets exposed as the `LED.on()` method called in our REPL code above.


# Further Work

My first step is going to be to get the hang of how all this works by adding in
support for PWM channels and the RGB LEDs.  I'd like all 16 channels
(4 x mono LEDs plus 4 x RGB LEDs) to support 8 bit PWM, and all work from the same
PWM timer.

Next, I'd like to look at automating the wrapping process, so that instead of
having to write individual C functions like `litex_led_on` above, we could have a
module `_csr` (or some name like that) which automatically makes available the 
CSR registers to Python with appropriate wrappers, and then more specific
driver behaviour can be implemented in Python.

Eventually, I'd like to look at how
[LiteX could generate a DeviceTree](https://github.com/timvideos/litex-buildenv/wiki/DeviceTree)
and MicroPython could read that to discover the register mappings.
This would greatly decouple the gateware compilation process from the MicroPython compilation
process.  Also, it should allow MicroPython to discover the hardware properties of 
DeviceTree-compatible SPI devices through the use of 
[Device Tree Overlays](https://www.kernel.org/doc/Documentation/devicetree/overlay-notes.txt)

I'd also like to work with the [TinyFPGA BX](https://tinyfpga.com/bx/guide.html) which
shows a lot of promise as a smaller, cheaper board with an open source toolchain available.
[MicroPython is a work in progress!](https://twitter.com/cr1901/status/1043145532779253760)
