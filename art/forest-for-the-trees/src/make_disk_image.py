magic = bytes((0xc0, 0xd1, 0xf1, 0xed, 0xed, 0x1f, 0x1c, 0xe5))

with open("diskimage.bin", "wb") as fh:
    fh.write(magic);
    fh.write(bytes(1024*1024-len(magic)))
