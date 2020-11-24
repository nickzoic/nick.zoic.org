#!/usr/bin/env python
import sys

# DOS 3.3 stores its sectors interleaved *BUT* the track 0 loader routine
# knows nothing about this so the track zero is stored in a funny order.
# this reshuffles sectors to match the DOS3.3 emulator behaviour.
# See Beneath Apple DOS p 3-23.  This might not be necessary if saving in
# WOZ format.

# Also pads file out to full floppy size

n_tracks = 35
sectors = [0, 0xD, 0xB, 9, 7, 5, 3, 1, 0xE, 0xC, 0xA, 8, 6, 4, 2, 0xF]

with open(sys.argv[1], "rb") as rfh:
    rdata = rfh.read().ljust(n_tracks*len(sectors)*256, b'\0')

with open(sys.argv[2], "wb") as wfh:
    for track in range(0,n_tracks):
        for sector in sectors:
            offset = (track*len(sectors)+sector)*256
            wfh.write(rdata[offset:offset+256])




