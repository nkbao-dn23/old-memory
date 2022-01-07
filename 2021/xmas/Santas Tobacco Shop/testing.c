#include <sys/mman.h>
#include <errno.h>

main(){
	printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n", EACCES, EAGAIN, EBADF, EEXIST, EINVAL, EINVAL, EINVAL, ENFILE, ENODEV, ENOMEM, EOVERFLOW, EPERM, EPERM, ETXTBSY);
}