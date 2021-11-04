// gcc testing.c -no-pie -fno-stack-protector

char global_var[0x1000];

void vuln(){
	char buf[0x10];
	read(0, &buf, 0x20);
}


main(){
	read(0, &global_var, 0x1000);  // safe
	puts("hello everyone"); // leak dia chi
	vuln();
}