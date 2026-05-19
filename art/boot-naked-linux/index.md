---
title: Boot Naked Linux
date: '2026-05-19'
layout: draft
tags:
  - c
  - linux
---

When I was [a kid](../ultima-iv-reflections/), computers weren't coddled and 
left running 24/7, when you were done with them you switched them off, and
when you wanted them again you just switched them on and within a second or
so they'd be loading whatever was in their disk drive.

There was a brief moment in the early 2000s where the newly introduced
SSDs made booting quick but as always the tech industry has taken up the
slack until even a 16 core monster with a fast SSD still takes a minute
to get its feet under it.

So I wanted to try an alternative.
Keep the Linux kernel but strip away everything else I could.
Here goes ... well not quite nothing, but a lot less.

## Hello, World!

The first thing a Linux system does is run an "init" program of one sort
or another which loads all the other processes and configurations and stuff.
There's nothing too special about this program, it's just a regular 
executable.
So we can write a new one in C `init.c`:

    #include <stdio.h>
    #include <stdlib.h>
    #include <sys/reboot.h>

    int main(int argc, char **argv) {
        fprintf(stderr, "Hello from init.c!");
        reboot(RB_AUTOBOOT);
    }

All it does is print a message.
If the process exits the kernel panics, so instead of busy waiting or sleeping
forever or whatever, we use `reboot(RB_AUTOBOOT)` to trigger a reboot.

## Making initrd

To boot Linux you need two things: a kernel and a filesystem.
Modern Linux supports quite a complex multi-stage process, but all we 
want for now is to get our one program running:

    gcc -static init.c -o init
    echo 'init' | cpio -o --format=newc | gzip -c > initrd

`cpio` is a very weird program which makes `tar` look user-friendly.
But let's not worry about it for now.
I will note that, later, if you get a kernel message:

    Initramfs unpacking failed: no cpio magic

... it means that either the cpio format or the compression or something
similar isn't compatible with your kernel, and likewise an error message like:

    check access for rdinit=/init failed: -2, ignoring

... means that either the initramfs didn't happen or your binary is otherwise
not usable.
This message happens pretty early in the boot process, which attempts to 
continue anyway, so you'll have to look back carefully.

## Virtualized

Getting this going on real hardware would be pretty irritating,
so I'm using [QEMU](https://qemu.org/) to make a virtual system
to experiment with.

For now, I'm using `kvm` to run a virtualized system rather than
go for full emulation with `qemu-system-x86_64`, but we'll return
to the question of emulation later, and we'll get to real hardware
eventually.

First we need a kernel, I'm just using the current kernel
from my machine but the file is root-only so make a copy
of it in our working directory and change its ownership:

    sudo cp /boot/vmlinuz .
    sudo chown $USER:$GROUP vmlinuz

We now have our two binary files, the kernel `vmlinuz` and 
the init file system `initrd` which contains only our program
`init`.
So we can boot our system with:

    kvm -m 1G -nographic -kernel vmlinuz \
        -initrd initrd -append "console=ttyS0 panic=-1" \
        -no-reboot

The `-nographic` and `console=ttyS0` options give us a terminal console
to monitor stderr on, and `panic=-1` and `-no-reboot` mean that kernel
panics or reboots will let qemu exit neatly instead of hanging.

when the kernel starts up, it unpacks our `initrd` into a ram disk, and
runs our `init` binary:

    [    0.000000] Linux version 6.8.0-111-generic (buildd@lcy02-amd64-088)
    [    0.000000] Command line: console=ttyS0 panic=-1
    [    0.489390] Trying to unpack rootfs image as initramfs...
    [    0.805419] Run /init as init process
    Hello from init.c!
    [    0.807535] reboot: machine restart

## Devices

Even if we don't want any filesystems, we might want some permanent 
storage.
Let's make some:

    dd if=/dev/random of=disk bs=1K count=1K

But we haven't mounted a root filesystem yet, so there's no devices available!
Devices are made available using a kernel mechanism called "devtmpfs" which
normally isn't loaded until *after* the real root filesystem is mounted, but we
don't have one of those ... thankfully there's an easy workaround, we can mount
devtmpfs from our C program using `mount("devtmpfs", "/dev", "devtmpfs", 0, NULL)`.

QEMU can present a host file as a block device on the guest using 
the `-hda` option, it'll appear to the guest as `/dev/sda`, so let's 
modify our code from before to mount the `devtmpfs` and read the 
first few bytes from that file:

    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <sys/mount.h>
    #include <sys/reboot.h>
    #include <arpa/inet.h>

    int main(int argc, char **argv) {
        fprintf(stderr, "Hello from init.c!\n");
        mount("devtmpfs", "/dev", "devtmpfs", 0, NULL);

        int fd = open("/dev/sda", O_RDWR);
        uint32_t buffer;
        read(fd, &buffer, sizeof(buffer));
        close(fd);

        fprintf(stderr, "Read %08x\n", ntohl(buffer));
        reboot(RB_AUTOBOOT);
    }

*(yeah, I know, proper C code needs to be scattered with return
value checks and sensible reports of errno.
I've left these out for clarity.)*

We can run this as:

    kvm -m 1G -nographic -kernel vmlinuz \
        -initrd initrd -append "console=ttyS0 panic=-1" \
        -no-reboot -hda disk

... and end up with output something like (edited for brevity):

    [    0.000000] Linux version 6.8.0-111-generic (buildd@lcy02-amd64-088)
    [    0.000000] Command line: console=ttyS0 panic=-1
    [    0.010975] Memory: 975024K/1048056K available (22528K kernel code, 4438K rwdata,
                   14412K rodata, 4924K init, 4788K bss, 72772K reserved, 0K cma-reserved)
    [    0.493923] Trying to unpack rootfs image as initramfs...
    [    0.712522] ata1.00: ATA-7: QEMU HARDDISK, 2.5+, max UDMA/100
    [    0.713091] ata1.00: 2048 sectors, multi 16: LBA48 
    [    0.816634] Run /init as init process
    Hello from init.c!
    Read 4463823c
    [    0.818128] sd 0:0:0:0: [sda] Synchronizing SCSI cache
    [    0.819849] reboot: machine restart

So there we go, less than a second from power-on to running a program and reading from disk,
and a trimmed back kernel could probably improve that a bit.
