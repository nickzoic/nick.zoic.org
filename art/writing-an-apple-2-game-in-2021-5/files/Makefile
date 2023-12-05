MAKEFLAGS += r
TARGET = apple2
TARGET_LIB = ${TARGET}.lib
START_ADDR = 2000  # hex

%.s: %.c
	cc65 -Oi -o $@ -t ${TARGET} $<

%.o: %.s
	ca65 -o $@ $<

%.bin: %.o
	ld65 -o $@ -t ${TARGET} -D __EXEHDR__=0 -S 0x${START_ADDR} $< ${TARGET_LIB}

%.dsk: %.bin
	cp dos33_loader.dsk $@
	a2in B.${START_ADDR} $@ PROGRAM $<

run_%: %.dsk
	mame apple2p -volume -24 -uimodekey DEL -flop1 $<
