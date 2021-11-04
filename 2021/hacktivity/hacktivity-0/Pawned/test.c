main(){
	int *x = malloc(0x68);
	int *y = malloc(0x68);
	free(x);
	free(y);
	int *a = malloc(0x68);
	int *b = malloc(0x68);
	int *c = malloc(0x68);
}