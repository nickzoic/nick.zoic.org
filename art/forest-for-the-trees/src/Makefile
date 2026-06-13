initrd.bin: init
	echo 'init' | cpio -ov --format=newc | gzip -c -9 > initrd.bin
	
init: init.c
	gcc -static init.c -o init

diskimage.bin:
	python make_disk_image.py

run: initrd.bin vmlinuz
	kvm -m 1G -nographic -kernel vmlinuz -initrd initrd.bin -append "console=ttyS0 panic=-1" -no-reboot -drive file=diskimage.bin,index=0,media=disk,format=raw
