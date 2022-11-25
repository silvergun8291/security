// gcc -o source source.c -fno-stack-protector -z now -no-pie

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int loop = 0;

int main(void)
{
	char buf[0x30];

	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);

	if (loop)
	{
		puts("bye");
		exit(-1);
	}
	loop = 1;

	read(0, buf, 0x70);

	return 0;
}

