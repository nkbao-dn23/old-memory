#include <stdio.h>

vuln(){
  char *v2 = malloc(96);
  puts("Enter your string:");
  fgets(v2, 96, stdin);
  printf(v2);
  exit(0);
}

int main(void) {
  vuln();
}
