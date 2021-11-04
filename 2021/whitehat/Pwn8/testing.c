main(){
	int *a = malloc(120);
	int *b = malloc(120);

	free(a);
	free(b);
	free(a);
}