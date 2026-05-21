initrd: init
	echo 'init' | cpio -o -H newc | gzip -c > initrd
	
init: init.c
	gcc -static -O0 init.c -o init -lm

run: vmlinuz initrd
	kvm -m 1G -kernel vmlinuz -initrd initrd

bootx64.efi: vmlinuz initrd
	ukify build --linux=vmlinuz --initrd=initrd --output bootx64.efi
