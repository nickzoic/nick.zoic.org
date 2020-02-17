---
date: '2020-02-10'
layout: draft
tags:
  - systems
  - linux
title: 'Experimenting with an Nvidia Jetson Nano'
---

I grabbed an [Nvidia Jetson Nano Dev Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) board from
[Seeed](https://www.seeedstudio.com/NVIDIA-Jetson-Nano-Development-Kit-p-2916.html) ...
well, I was ordering some other stuff and it just kinda happened ... 
anyway, they're rather a cool little unit and I wanted to see how it'd go as a PC for my office.

I do do a bit of development, but the idea is to 

# Disk Image

There's a 5.2GB image file to download, which contains a ~12GB disk image.
This seems a little excessive to me.
Sure, it's actually a Linux distro but [Alpine](https://www.alpinelinux.org/)
for ARM manages to fit a lot into under 85MB compressed.

How exactly is the Jetson Nano image 60 times this big?

# SD Card

64GB Sandisk Extreme A2, claiming *UP TO* 160MB/s read and 60MB/s write.

Writing the initial image onto this from my laptop started promisingly at 100 MB/s or so and
then slowly dwindled away to 15MB/s, but I think that has more to do with the shonky USB 
adaptor I was using.   Still, it go there fast enough.

Looking at this card from my laptop, it appears to have 14 partitions of various sizes,
which seems odd.  There's also an ominous warning:

```
GPT PMBR size mismatch (25165823 != 124735487) will be corrected by write.
The backup GPT table is not on the end of the device. This problem will be corrected by write.

Device     Start      End  Sectors  Size Type
/dev/sda1  28672 25165790 25137119   12G Linux filesystem
/dev/sda2   2048     2303      256  128K Linux filesystem
/dev/sda3   4096     4991      896  448K Linux filesystem
/dev/sda4   6144     7295     1152  576K Linux filesystem
/dev/sda5   8192     8319      128   64K Linux filesystem
/dev/sda6  10240    10623      384  192K Linux filesystem
/dev/sda7  12288    13055      768  384K Linux filesystem
/dev/sda8  14336    14463      128   64K Linux filesystem
/dev/sda9  16384    17279      896  448K Linux filesystem
/dev/sda10 18432    19327      896  448K Linux filesystem
/dev/sda11 20480    22015     1536  768K Linux filesystem
/dev/sda12 22528    22655      128   64K Linux filesystem
/dev/sda13 24576    24735      160   80K Linux filesystem
/dev/sda14 26624    26879      256  128K Linux filesystem
```

Saving the partition table back to disk fixes the ominous warning, but there's still 47.5GB
of unallocated space on the card. Perhaps we'll get to reallocate that later.

# First Boot

So I finally found my 5V 4A power supply and booted the device.
On first boot it does indeed give you the option to resize that first partition,
although I'm still not sure what all the other ones are for.
If you've got it networked you can then upgrade Ubuntu packages.

Disappointingly, the DisplayPort on board is *only* a DisplayPort ...
it [won't work with the normal DisplayPort to HDMI converter cables](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#troubleshooting).
Apparently [it will with some 'active' adaptors though](https://devtalk.nvidia.com/default/topic/1049356/jetson-nano/dual-simultaneous-monitors/2)
so I'll try to get hold of one of those.

The distro includes LibreOffice, which seems odd, and doesn't seem to
include the "Nsight Eclipse Edition" any more ... there's a `/usr/local/bin/nvcc`
but no `/usr/local/bin/nsight` on this disk, and
[the usual download link](https://developer.nvidia.com/cuda-downloads?target_os=Linux)
doesn't offer a ARM8 architecture.
I saw a release note somewhere indicating that it was maybe no longer included due
to a transition to
[Nsight Visual Studio Edition](https://developer.nvidia.com/nsight-visual-studio-edition)
but I'm not clear on this yet.



