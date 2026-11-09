#include "dedup.h"
#include "oracle.h"
#include <stdio.h>
#include <stdlib.h>
static size_t cases;
static void check(const uint16_t *a, size_t n) {
    uint16_t *storage=malloc((n+2)*sizeof(*storage)); assert(storage);
    uint16_t *b=storage+1;
    for (int k=0;k<2;++k) {
        storage[0]=12345;storage[n+1]=54321;
        if(n) memcpy(b,a,n*sizeof(*b));
        size_t u=k?bitmap_unique(b,n):heap_unique(b,n);
        assert(storage[0]==12345 && storage[n+1]==54321);
        validate(a,n,b,u,!k);
    }
    free(storage); ++cases;
}
int main(void) {
    assert(heap_unique(NULL,0)==0); assert(bitmap_unique(NULL,0)==0);
    check(NULL,0);
    const uint16_t examples[][10]={{42},{7,7,7,7},{0,1,2,3,65535},
      {65535,3,2,1,0},{2,1,2,0,1,65535,0,65535}, {0,65535},
      {3,1,4,1,5,9,2,6,5,3}};
    size_t ns[]={1,4,5,5,8,2,10};
    for(size_t j=0;j<7;++j) check(examples[j],ns[j]);
    const uint16_t alphabet[]={0,64,65535};
    uint16_t small[7];
    size_t combinations=1;
    for(size_t n=0;n<=7;++n) {
        for(size_t code=0;code<combinations;++code) {
            size_t value=code;
            for(size_t i=0;i<n;++i) {small[i]=alphabet[value%3];value/=3;}
            check(small,n);
        }
        combinations*=3;
    }
    uint16_t *a=malloc(10000000*sizeof(*a)); assert(a);
    for(size_t i=0;i<65536;++i) a[i]=(uint16_t)i;
    check(a,65536);
    for(size_t i=0;i<65536;++i) a[i]=(uint16_t)(65535-i);
    check(a,65536);
    uint32_t s=20261108;
    for(size_t trial=0;trial<200;++trial) {
        size_t n=trial*7;
        for(size_t i=0;i<n;++i) {s^=s<<13;s^=s>>17;s^=s<<5;a[i]=(uint16_t)s;}
        check(a,n);
    }
    const size_t scales[]={1000,100000,10000000};
    for(size_t j=0;j<3;++j) {
        size_t n=scales[j];
        for(size_t i=0;i<n;++i) a[i]=99;
        check(a,n);
        for(size_t i=0;i<n;++i) a[i]=(uint16_t)(i*UINT64_C(65536)/n);
        check(a,n);
        for(size_t i=0;i<n;++i) a[i]=(uint16_t)(65535-i*UINT64_C(65536)/n);
        check(a,n);
        for(size_t i=0;i<n;++i) {s^=s<<13;s^=s>>17;s^=s<<5;a[i]=(uint16_t)s;}
        check(a,n);
    }
    free(a); printf("OK: %zu casos x 2 algoritmos; NULL vazio também validado.\n",cases);
}
