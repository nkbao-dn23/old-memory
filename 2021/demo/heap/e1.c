#include<stdio.h>
#include<stdlib.h>
#include<inttypes.h>
int main(int argc,char **argv)
{
    //this is tcache
    /*
    *typedef struct tcache_entry
    {
        struct tcache_entry *next;
   //This field exists to detect double frees.  
        struct tcache_perthread_struct *key;
    } tcache_entry;
     */
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    printf("tcache_dup can help you achieve \"arbitrary address writes\"\n");
    void *p,*q,*r,*d;
    p = malloc(0x10);
    q = malloc(0x10);
    free(p);
    printf("now , we have a tcache which is already free\n");
    printf("We can modify its next pointer!\n");
    *(uint64_t *)p = (uint64_t)q;
    printf("now p's next pointer = q\n");
    printf("p's next = %p ,q = %p\n",*(uint64_t *)p,q);
    printf("so,We can malloc twice to get a pointer to q,sure you can change this to what you want!\n");
    r = malloc(0x10);
    d = malloc(0x10);
    printf("OK!, we get we want!\n");
    
}