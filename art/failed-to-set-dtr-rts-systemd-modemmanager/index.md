---
category: etc
date: '2019-03-28'
layout: article
summary: |
    Having trouble with /dev/ttyACM* devices?  Think you've disabled
    SystemD ModemManager?  Think again ...
tags:
    - microcontrollers
    - linux
title: 'SystemD ModemManager: failed to set dtr/rts'
---

If you're working with embedded devices which present themselves as UARTS, you've
probably already noticed an annoying thing called ModemManager which tries to 
talk to anything called `/dev/ttyACM*`.  This can cause 'device in use' errors when
you first configure the device, or mysterious hangs while using the device.

This is particularly a problem with [esptool](https://github.com/espressif/esptool) 
and [tinyprog](https://github.com/tinyfpga/TinyFPGA-Bootloader/tree/master/programmer)
and similar programs which try to send high-speed binary data over the UART.

After ages trying to work out what was going on, I found this article on
Ask Ubuntu: [udev rules seem ignored; can not prevent modem manager from grabbing device](https://askubuntu.com/questions/399263/udev-rules-seem-ignored-can-not-prevent-modem-manager-from-grabbing-device)
and everything became horribly clear.  The udev rules mechanism you're used to using to prevent
this happening no longer works.

Assuming you don't actually have any modems the easiest thing is just to tell ModemManager to leave `/dev/ttyACM*` alone:

* Edit `/lib/systemd/system/ModemManager.service` and add to the `[Service]` section:
```
Environment="MM_FILTER_RULE_TTY_ACM_INTERFACE=0"
```

Otherwise you can add specific udev rules for this device and then remind systemd ModemManager to actually respect those rules:

* Create `/etc/udev/rules.d/99-tinyfpga.rules` and add rule 

```
ATTR{idProduct}=="6130", ATTR{idVendor}=="1d50", ENV{ID_MM_DEVICE_IGNORE}="1", MODE="666"
```

* sudo udevadm control --reload
* Edit `/lib/systemd/system/ModemManager.service` and change `ExecStart=/usr/sbin/ModemManager --filter-policy=strict` to `ExecStart=/usr/sbin/ModemManager --filter-policy=default`

This policy tells ModemManager to actually respect the `ID_MM_DEVICE_IGNORE` flag.
Frustratingly, the default policy is not "default" but "strict".

Either way, reload the ModemManager configuration:

```
sudo systemctl daemon-reload
sudo systemctl restart ModemManager
```

... and you should be working again!
