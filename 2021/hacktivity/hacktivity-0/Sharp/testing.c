main(){
	int *a = malloc(0x10);
	int *b = malloc(0x500);
	int *c = malloc(0x500);
	int *d = malloc(0x10);

	free(b);
	free(c);

	malloc(0x20);

}