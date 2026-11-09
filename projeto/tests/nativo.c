#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

size_t heap_unique(uint16_t *a, size_t n);

static size_t cases;

static void check(const uint16_t *a, size_t n) {
    uint16_t *storage=malloc((n+2)*sizeof(*storage));
    unsigned char *expected=calloc(65536,1);
    assert(storage && expected);
    uint16_t *b=storage+1;
    storage[0]=12345;storage[n+1]=54321;
    if(n) memcpy(b,a,n*sizeof(*a));
    size_t count=0;
    for(size_t i=0;i<n;++i) if(!expected[a[i]]) {expected[a[i]]=1;++count;}
    size_t u=heap_unique(b,n);
    assert(u==count && u<=n);
    assert(storage[0]==12345 && storage[n+1]==54321);
    for(size_t i=0;i<u;++i) {
        assert(expected[b[i]]);
        expected[b[i]]=0;
        if(i) assert(b[i-1]<b[i]);
    }
    for(size_t x=0;x<65536;++x) assert(!expected[x]);
    free(storage);free(expected);++cases;
}

int main(void) {
    assert(heap_unique(NULL,0)==0);
    uint16_t values[7];
    size_t combinations=1;
    const uint16_t alphabet[]={0,64,65535};
    for(size_t n=0;n<=7;++n) {
        for(size_t code=0;code<combinations;++code) {
            size_t digits=code;
            for(size_t i=0;i<n;++i) {values[i]=alphabet[digits%3];digits/=3;}
            check(values,n);
        }
        combinations*=3;
    }
    const uint16_t example[]={3,1,3,0,65535};
    const uint16_t answer[]={0,1,3,65535};
    uint16_t copied[5];memcpy(copied,example,sizeof example);
    assert(heap_unique(copied,5)==4 && !memcmp(copied,answer,sizeof answer));
    uint16_t *a=malloc(10000000*sizeof(*a));assert(a);
    const size_t scales[]={1000,100000,10000000};
    uint32_t seed=20261108;
    for(size_t k=0;k<3;++k) {
        size_t n=scales[k];
        for(size_t i=0;i<n;++i) a[i]=99;
        check(a,n);
        for(size_t i=0;i<n;++i) a[i]=(uint16_t)(i*UINT64_C(65536)/n);
        check(a,n);
        for(size_t i=0;i<n;++i) a[i]=(uint16_t)(65535-i*UINT64_C(65536)/n);
        check(a,n);
        for(size_t i=0;i<n;++i) {seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;a[i]=(uint16_t)seed;}
        check(a,n);
    }
    for(size_t i=0;i<65536;++i) a[i]=(uint16_t)i;
    check(a,65536);
    for(size_t i=0;i<65536;++i) a[i]=(uint16_t)(65535-i);
    check(a,65536);
    free(a);
    printf("OK C: %zu casos, NULL/0, resposta conhecida e sentinelas.\n",cases);
    return 0;
}
