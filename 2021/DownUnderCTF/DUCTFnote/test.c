main(){
	int *a = malloc(0x500);
	int *b = malloc(0x500);
	free(a);
}