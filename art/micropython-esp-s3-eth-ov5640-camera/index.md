---
layout: draft
title: Micropython on ESP32 with the OV5640 camera
---

# board

"Waveshare ESP32-S3-ETH" purchased on Aliexpress.

Came with a sticker linking [here](https://spotpear.com/wiki/ESP32-S3R8-PoE-ETH-RJ45-Camera-Micro-SD-Pico-W5500-OV2640-OV5640.html)

[schematic](https://files.waveshare.com/wiki/ESP32-S3-ETH/ESP32-S3-ETH-Schematic.pdf)

Should be an ESP32-S3 with a W5500 ethernet adaptor and a POEE daughterboard,
plus an OV5640 camera module.

There's a "powerdown pin" is on GPIO8 and the camera won't start up until this is 
pulled low (see schematic section 摄像头降压电路 (A11)) where Q3 turns off the
step-down regulators which power the camera module.

According to [this](https://github.com/cnadler86/micropython-camera-API?tab=readme-ov-file#notes):

> The OV5640 pinout is compatible with boards designed for the OV2640 but the voltage supply
> is too high for the internal 1.5V regulator, so the camera overheats unless a heat sink is applied.

... but this board does include 2.8 and 1.5 volt regulators so I'm not
sure if this applies.  The camera does seem to run pretty warm,
but for my application I'm only interested in sporadic snapshots
so hopefully I can just power the camera down between uses.

I'm planning on powering it from USB-C or [PoE](https://en.wikipedia.org/wiki/Power_over_Ethernet) and in either case 
peripherals can get limited 5V power from VBUS pin or 3.3V power
from the 3V3 pin.

# circuitpython

```
Adafruit CircuitPython 10.1.3 on 2026-02-21; Waveshare ESP32-S3-ETH with ESP32S3

>>> from microcontroller.pin import *
>>> import digitalio
>>> digitalio.DigitalInOut(GPIO8).switch_to_output(False)
>>> import espcamera
>>> import busio
>>> bus = busio.I2C(sda=GPIO48,scl=GPIO47)
>>> c = espcamera.Camera(data_pins=[GPIO41,GPIO45,GPIO46,GPIO42,GPIO40,GPIO38,GPIO15,GPIO18],pixel_clock_pin=GPIO39,vsync_pin=GPIO1,href_pin=GPIO2,external_clock_pin=GPIO3,i2c=bus)
>>> b = c.take()
>>> b.height
120
>>> b.width
160
>>> b.bits_per_value
16
```

# micropython

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

For some reason it isn't capturing JPEGS though.

## control pins

between USB-C, Ethernet, UART0, the SD card, the camera 
interface and power, a boot button and an LED there aren't
that many completely free GPIOs on this board!

Looks like I've still got 7: 16, 17 and 33 .. 37 
