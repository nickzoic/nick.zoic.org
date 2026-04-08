---
layout: draft
title: Micropython on ESP32 with the OV5640 camera
date: '2025-03-01'
---

## Board

"Waveshare ESP32-S3-ETH" purchased on Aliexpress.

Came with a sticker linking [here](https://spotpear.com/wiki/ESP32-S3R8-PoE-ETH-RJ45-Camera-Micro-SD-Pico-W5500-OV2640-OV5640.html)

[schematic](https://files.waveshare.com/wiki/ESP32-S3-ETH/ESP32-S3-ETH-Schematic.pdf)

It's an [ESP32-S3](https://www.espressif.com/en/products/socs/esp32-s3) board with a USB-C interface,
a [Wiznet W5500](https://wiznet.io/products/ethernet-chips/w5500)-based ethernet interface and 
a little flat [camera connector](https://en.wikipedia.org/wiki/Camera_Serial_Interface), whatever those are called.

## Camera

I also got an [OV5640 camera module](https://cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV5640_datasheet.pdf)
with it.

Note there's a "powerdown pin" is on GPIO8 and the camera won't start up until this is 
pulled low (see schematic section 摄像头降压电路 (A11)) where Q3 turns off the
step-down regulators which power the camera module.

According to [this](https://github.com/cnadler86/micropython-camera-API?tab=readme-ov-file#notes):

> The OV5640 pinout is compatible with boards designed for the OV2640 but the voltage supply
> is too high for the internal 1.5V regulator, so the camera overheats unless a heat sink is applied.

... but this board does include 2.8 and 1.5 volt regulators so I'm not
sure if this applies.  The camera does seem to run pretty warm,
but for my application I'm only interested in sporadic snapshots
so hopefully I can just power the camera down between uses.

Unfortunately the module I bought has a very short cable and is kind of tricky to place sensibly when
the PoE module is also installed.  So I've ordered some camera modules with longer cables.

# PoE 

I'm planning on powering this project from [PoE](https://en.wikipedia.org/wiki/Power_over_Ethernet), which 
thanks to the Waveshare PoE Module should provide enough 5V peripheral power on the VBUS pin.
I can't find any documentation for the module but I suspect just from the look of the board
it'll be good for 5V / 1A at the most.  Which should be enough.

I've bought a [TP-Link TL-SG1005P PoE+ switch](https://www.tp-link.com/au/business-networking/soho-switch-unmanaged/tl-sg1005p/)
to provide power, it can apparently provide up to 30W power per port up to a total of 65W for all ports.
There's also a nice Auto Recovery mode which power cycles any PoE device which hasn't sent packets
["for a long period"](https://www.tp-link.com/us/support/faq/2944/) although I haven't found any documentation of
how long that is ... seconds? minutes? weeks?

# Servos

RC Servos are simple to drive, they need a constant 5V (or thereabouts) supply plus a 
[PWM signal](https://learn.sparkfun.com/tutorials/hobby-servo-tutorial/servo-motor-background)
to position them.  This is easily generated from a PWM capable GPIO.
For most servos, the required PWM signal is 50Hz (20ms) with duty cycle varying from 5% to 10% (1 - 2 ms) ...
and 3.3V logic works fine, no driver circuitry necessary.

## Demo App

The board comes with a demo app called [`ETH_Web_Cam`](https://spotpear.com/wiki/ESP32-S3R8-PoE-ETH-RJ45-Camera-Micro-SD-Pico-W5500-OV2640-OV5640.html#ETH_Web_CAM)
which does what it sounds like: DHCPs onto the ethernet network and exposes a web
server which displays stills or streams from the camera, with lots of configuration
buttons and stuff.  So at least I know the hardware works.

Incidentally, while the W5500 on this module has a default MAC address in the range "a4:3c:d7",
the demo always overrides the MAC address to `DE:AD:BE:EF:FE:ED` ...


## Micropython

```
MicroPython v1.27.0-dirty on 2026-02-22; Generic ESP32S3 module with ESP32S3
Type "help()" for more information.
>>> from machine import I2C
>>> i2c = I2C(1,scl=47,sda=48)
>>> import camera
>>> c = camera.Camera(data_pins=[41,45,46,42,40,38,15,18],vsync_pin=1,href_pin=2,xclk_pin=3,pclk_pin=39,i2c=i2c,frame_size=camera.FrameSize.QVGA,pixel_format=camera.PixelFormat.RGB565,fb_count=2, powerdown_pin=8)
>>> len(c.capture())
153600
>>> c.reconfigure(frame_size=camera.FrameSize.SVGA)
>>> len(c.capture())
960000
```

For some reason it isn't capturing JPEGs on the OV5640 though.
It works fine with the OV2640.

## control pins

between USB-C, Ethernet, UART0, the SD card, the camera 
interface and power, a boot button and an LED there aren't
that many free GPIOs on this board!

Looks like I've still got 7 completely free: 16, 17 and 33 .. 37 

The I2C bus on GPIO47 and GPIO48 is used by the camera but can be shared
with external hardware too.

## code

```
Obtain unique identifier
Configure LAN w/ random MAC
Setup output pins
Connect to MQTT & subscribe to control topic with callback:
    update outputs 
    set counter = 10
set up a 30 second timer with callback:
    mq.ping()
while True:
    if counter > 0:
        take picture and publish to img topic
        decrement counter
        mq.check_msg()
    else:
        mq.wait_msg()
```
