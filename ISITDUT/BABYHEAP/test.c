main(){
	int *a = malloc(0x20);
	free(a);
	free(a);
	int *b = malloc(0x20);

}