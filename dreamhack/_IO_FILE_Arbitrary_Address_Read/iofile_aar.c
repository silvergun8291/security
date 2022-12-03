// Name: iofile_aar
// gcc -o iofile_aar iofile_aar.c -no-pie 

#include <stdio.h>
#include <unistd.h>
#include <string.h>

char account_buf[1024];
FILE *fp;
void init() {
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
}

int read_account() {
	FILE *fp;
	fp = fopen("/etc/passwd", "r");
	fread(account_buf, sizeof(char), sizeof(account_buf), fp);
	fclose(fp);
}

int main() {
  const char *data = "TEST FILE!";
  
  init();
  read_account();
  
  fp = fopen("testfile", "w");
  
  printf("Data: ");
  
  read(0, fp, 300);
  
  fwrite(data, sizeof(char), sizeof(account_buf), fp);
  fclose(fp);
}

