#include <stdio.h>
#include <unistd.h>

int main() {
	char buf[64];
    
    puts("Return to vuln");
    
    printf("Input: ");
    read(0, buf, 256);
    
    return 0;
}

