main(){
	char distionary[62] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	char s[32];
	for(int i=0; i<= 0xffff; i++){
		srand(i);
		for(int j=0; j<32; j++){
			s[j] = distionary[rand()%62];
		}
		printf("%d: %32s\n", i, s);
	}
}