---
date: '2021-02-04'
layout: article
tags:
  - fpga
  - microcontrollers
title: 'QuickLogic / QORC Quickfeather Devkit'
summary: 'An MCU + FPGA development board with an Open Source toolchain'
---

This year at [LinuxConfAU](https://linux.conf.au/) I got to see 
Tim Saxe and Brian Faith's talk on the new
[QORC](https://www.quicklogic.com/QORC/) (QuickLogin Open Reconfigurable Computing)
SoC, and how they came to develop an open source toolchain.

I got in touch with them to request some sample hardware, and a couple of weeks
later, here it is!

# QuickFeather Dev Kit

The [QuickFeather](https://www.quicklogic.com/products/eos-s3/quickfeather-development-kit/)
devkit is quite interesting: the footprint is mostly compatible with the 
[Adafruit Feather](https://www.adafruit.com/feather) series of devices, but double-sided 
rather than stacking headers and some extra header pins on the top.
Like the Feather boards, there's a LiPo controller build in, but on this board there's also
[a bunch of sensors](https://github.com/QuickLogic-Corp/quick-feather-dev-board#key-features)
(accelerometer, pressure sensor, MEMS mic).

[![20210211_125904](img/20210211_125904-thumb.jpg)](img/20210211_125904.jpg)
*QuickLogic QuickFeather next to an Adafruit Feather nRF52832*

The board is a bit longer than a regular feather,
with another 16 pin I/O connector on the end.
It's advertised as "compatible with 0.1" breadboards" but with those extra
pins populated it will no longer fit in a normal breadboard unless you hang
those off the end of the board.

[![20210211_125839](img/20210211_125839-thumb.jpg)](img/20210211_125839.jpg)
*QuickLogic QuickFeather in a breadboard*

Without stacking headers you can't put [FeatherWings](https://www.adafruit.com/category/814)
on top of it but it'd potentially work well on top or with
[FeatherWing Doubler](https://www.adafruit.com/product/2890).

For better Feather compatibility, I'd suggest using stackable headers in the
'standard' feather pins positions, and moving the extra 16 pins to be in line with
those but leave them unpopulated. Possibly even add some little holes to make
it easy to snap the extra bit off for 100% feather compatibility, a bit like the 
[ESPea32](https://blog.aprbrother.com/product/espea32).

(or like the [QOMU](https://www.electronics-lab.com/quicklogic-launches-qomu-an-open-source-soc-dev-kit-that-fits-in-your-usb-port/) for that matter)

The chip runs at 3.3V (or at least, that's the supply voltage on this board,
it'll run down to 1.8V).
You can see from the
[schematic](https://github.com/QuickLogic-Corp/quick-feather-dev-board/blob/master/doc/quickfeather-board.pdf)
that all the dev kit I/O pins have 22 ohm series resistors on them, which is nice to
limit the chaos if you accidentally connect 5V logic to any of these pins.

## IO, GPIO, FBIO

It's kind of confusing just how many kinds of I/O there are. The
[QuickLogic EOS S3 datasheet](https://www.quicklogic.com/wp-content/uploads/2020/12/QL-EOS-S3-Ultra-Low-Power-multicore-MCU-Datasheet-2020.pdf)
includes a table (Table 31, Page 98) of how the pins are related.

* IO_*N* : One of the 46 physical pins (or pad) on the chip.   
* GPIO(*N*) : One of the 8 logical I/O addresses on the ARM core
* FBIO_*N* : An interface to the FPGA.

The I/O Multiplexor (see the
QuickLogic EOS S3 Multiplexor User Guide](https://www.quicklogic.com/wp-content/uploads/2020/06/QL-EOS-S3-Sensor-Processing-Platform-IOMUX-User-Guide.pdf)
) switches each IO Pin between GPIO, FBIO and various special purpose
peripherals.

There's a lot I haven't worked out yet.

# Plugging in In

(See also [QuickFeather Development Kit User Guide](https://github.com/QuickLogic-Corp/quick-feather-dev-board/blob/master/doc/QuickFeather_UserGuide.pdf))

## USB

On plugging it in with USB to a Linux machine and resetting the board with the "reset" button,
the LED flashes blue and then it appears as `1d50:6140 OpenMoko, Inc.`.
It's a standard `cdc_acm` device so it appears in Linux as `/dev/ttyACM0`.
It doesn't stick around for long though, after
a few seconds without connecting the board seems to disconnect.

As shipped there's a little diagnostic tool on the flash which lets you turn the LEDs
on and off, but to actually do much with this board you need a SWD programmer such
as a [Segger J-link](https://www.segger.com/products/debug-probes/j-link/) with a 
teeny 0.05" pitch connector.  Something like [this](https://www.adafruit.com/product/3571).

## SWD / J-Link

There's a 0.05" SWD header on the top, so we might as well try that out too.

Two shorting headers need to be installed (`J1` and `J7`), the SWD cable attached
to `J6` and power provided by battery or USB.

The drivers for the J-link device are available in the Ubuntu `jlink` package.
Try to remember they have weird capitalized names like `JLinkExe`.

At this point we can have a little conversation:

```
$ JLinkExe
SEGGER J-Link Commander V6.40 (Compiled Oct 26 2018 15:08:38)
DLL version V6.40, compiled Oct 26 2018 15:08:28

Connecting to J-Link via USB...O.K.
Firmware: J-Link EDU Mini V1 compiled Jan  7 2019 14:01:42
Hardware version: V1.00
S/N: 801001970
License(s): GDB, FlashBP
VTref=3.294V


Type "connect" to establish a target connection, '?' for help
J-Link>device cortex-m4
J-Link>si swd
Selecting SWD as current target interface.
J-Link>speed 4000
Selecting 4000 kHz as target interface speed
J-Link>connect
Device "CORTEX-M4" selected.


Connecting to target via SWD
Found SW-DP with ID 0x2BA01477
Scanning AP map to find all available APs
AP[1]: Stopped AP scan as end of AP map has been reached
AP[0]: AHB-AP (IDR: 0x24770011)
Iterating through AP map to find AHB-AP to use
AP[0]: Core found
AP[0]: AHB-AP ROM base: 0xE00FF000
CPUID register: 0x410FC241. Implementer code: 0x41 (ARM)
Found Cortex-M4 r0p1, Little endian.
FPUnit: 6 code (BP) slots and 2 literal slots
CoreSight components:
ROMTbl[0] @ E00FF000
ROMTbl[0][0]: E000E000, CID: B105E00D, PID: 000BB00C SCS-M7
ROMTbl[0][1]: E0001000, CID: B105E00D, PID: 003BB002 DWT
ROMTbl[0][2]: E0002000, CID: B105E00D, PID: 002BB003 FPB
ROMTbl[0][3]: E0000000, CID: B105E00D, PID: 003BB001 ITM
ROMTbl[0][4]: E0040000, CID: B105900D, PID: 000BB9A1 TPIU
Cortex-M4 identified.
J-Link>i
JTAG Id: 0x2BA01477  Version: 0x2 Part no: 0xba01 Man. Id: 023B 
J-Link>qc
```

This interface can be used to load software onto both the Cortex M4
CPU and the FPGA.

# Symbiflow

[Symbiflow](https://symbiflow.github.io/) is an Open Source FPGA toolchain
which supports many FPGA families including the QuickLogic EOS used by this board.
It's not available as a Ubuntu package yet so we're in "clone and build" territory.

Maybe don't try this on a limited bandwidth link, there's a lot of submodules to load.

When I was messing around with Symbiflow [last time](https://nick.zoic.org/art/migen-gigatron/)
I didn't achieve much on my stated aims but I did work out a much (subjectively)
nicer way to build stuff, without conda or apio or litex-buildenv, so I might have to
work that out again.

# TO BE CONTINUED

