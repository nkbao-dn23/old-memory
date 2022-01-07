main(){
	int size = 0x20;
	int *a = malloc(0x410);
	int *b = malloc(size);

	free(a);
	free(b);

	
}