// gcc -o fsb_got fsb_got.c -no -pie

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void alarm_handler() {
    puts("TIME OUT");
    exit(-1);
}


void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGALRM, alarm_handler);
    alarm(30);
}

int main() {
        char buf[256];

        read(0, buf, 256);
        printf(buf);
        exit(0);

        return 0;
}

