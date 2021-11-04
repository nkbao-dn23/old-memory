// gcc magic.c -no-pie -fno-stack-protector

main(){
	char a[0x10];
	gets(&a);
	printf("Hello %s\n", &a);
	close(0);
}