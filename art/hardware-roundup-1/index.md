---
date: '2019-01-28'
layout: draft
tags:
    - micropython
    - esp32
title: Hardware Roundup
summary: Some hardware on my workbench ...
---

In addition to [the Espressif meshkit button](/art/esp32-meshkit-button-micropython)
I have some other cool hardware on the workbench at the moment ...

![Adafruit Metro M4 Express and Feather NRF52840 Express](adafruit.jpg)
*Adafruit Metro M4 Express and Feather NRF52840 Express*

The [Metro M4 Express](https://www.adafruit.com/product/3382)
is a nice development board with an Arduino-compatible footprint but a lot faster CPU.  

The [Feather NRF52840 Express](https://www.adafruit.com/product/4062) is a nifty little unit with a NRF42840 on board with good
Bluetooth support. I'm working on [touchio support](https://github.com/adafruit/circuitpython/issues/1048)
for this board at the moment.

![Air602 dev board and module](air602.jpg)
*Air602 dev board and module*

Could this be the successor to the [ESP8266](/tag/esp8266/) ... it's even smaller and 
looks quite capable!  There's an [Air602 SDK compatible with GCC](https://yoursunny.com/t/2018/Air602-blink/)
Could be quite handy as a "wifi coprocessor" at the very least.

![ESP32 with Lorawan](lorawan.jpg)
*ESP32 with Lorawan*

This is a neat little board integrating an [ESP32](/tag/esp32/) and a
[SX1276 LoRa transceiver](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276) 
which I bought from [Ebay](https://www.ebay.com.au/sch/i.html?_nkw=esp32+sx1276).

Quite a few people have put work into [MicroPython drivers for SX1276](https://www.google.com/search?client=ubuntu&channel=fs&q=micropython+sx1276)
and I hope to get this into mainstream MicroPython at some point ...

![Sipeed Maix](sipeed-maix.jpg)
*Sipeed Maix*

An cheap and interesting [RISC-V](https://riscv.org/) with addition "neural network coprocessor".

* [Sipeed MAIX github repo](https://github.com/sipeed/MaixPy)
* [Sipeed MAIX at Indiegogo](https://www.indiegogo.com/projects/sipeed-maix-the-world-first-risc-v-64-ai-module#/)

![Sonoff Basic](sonoff-basic.jpg)
*Sonoff Basic*

These are neat little mains-powered switches which embed an [ESP8266](/tag/esp8266/) and
[can easily be reflashed to run MicroPython](https://medium.com/cloud4rpi/getting-micropython-on-a-sonoff-smart-switch-1df6c071720a)
[Sonoff S20 schematics](https://www.itead.cc/wiki/S20_Smart_Socket) are available which makes these
a great choice if you're considering switching mains from a hobbyist project and
[don't want to get locked into someone else's IoT solution](/art/the-internet-of-not-shit-things/).

![TinyFPGA BX](tinyfpga-bx.jpg)
*TinyFPGA BX*

Suitable for running [FuPy](https://nick.zoic.org/art/fupy-micropython-for-fpga/), I've soldered 
headers all over this one, and now I need to get back to it and try to actually make some progress ...

![Espruino Pico](espruino-pico.jpg)
*Espruino Pico*

Just to prove that MicroPython isn't the *only* high level language I'm interested in for
microcontrollers ... the [Espruino Pico](http://www.espruino.com/Pico) embeds Javascript instead,
on an ARM Cortex M4.

