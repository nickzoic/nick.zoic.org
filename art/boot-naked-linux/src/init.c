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
        uint32_t buffer[2];
        read(fd, buffer, sizeof(buffer));

        fprintf(stderr, "Read %08x %08x\n", ntohl(buffer[0]), ntohl(buffer[1]));

	sleep(5);

        reboot(RB_POWER_OFF);
}

