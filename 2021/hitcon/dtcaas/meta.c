#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>


main(){
	FILE *f = fopen("/proc/self/fd/1", "r");
	char buf[4096];
	fread(buf, 1, 4096, f);
	write(1, buf, 4096);
}