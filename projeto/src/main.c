#define _POSIX_C_SOURCE 200809L
#include "dedup.h"
#include "oracle.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
#include <errno.h>
static double now(void) {
    struct timespec t;
    if(clock_gettime(CLOCK_MONOTONIC,&t)) {perror("clock_gettime");exit(1);}
    return t.tv_sec+t.tv_nsec*1e-9;
}
int main(int argc,char **argv) {
    if(argc!=4) {fprintf(stderr,"Uso: %s heap|bitmap n repeticoes\n",argv[0]);return 1;}
    int bitmap=!strcmp(argv[1],"bitmap");
    if(!bitmap && strcmp(argv[1],"heap")) return 1;
    if(!*argv[2] || strspn(argv[2],"0123456789")!=strlen(argv[2]) ||
       !*argv[3] || strspn(argv[3],"0123456789")!=strlen(argv[3])) return 1;
    char *end; errno=0; unsigned long long parsed=strtoull(argv[2],&end,10);
    if(errno || *end || !parsed || parsed>SIZE_MAX/sizeof(uint16_t) || argv[2][0]=='-') return 1;
    size_t n=(size_t)parsed;
    errno=0; long reps=strtol(argv[3],&end,10); if(errno || *end || reps<1 || reps>1000) return 1;
    uint16_t *a=malloc(n*sizeof(*a)),*b=malloc(n*sizeof(*b));
    if(!a||!b) {fprintf(stderr,"Sem memoria\n");free(a);free(b);return 1;}
    uint32_t s=20261108;
    for(size_t i=0;i<n;++i) {s^=s<<13;s^=s>>17;s^=s<<5;a[i]=(uint16_t)s;}
    size_t (*run)(uint16_t*,size_t)=bitmap?bitmap_unique:heap_unique;
    puts("algoritmo,n,rodada,segundos,u,seed,distribuicao,entrada_bytes,rss_pico_kib");
    for(long r=-1;r<reps;++r) {
        memcpy(b,a,n*sizeof(*a));
        double t=now(); size_t u=run(b,n); double elapsed=now()-t;
        validate(a,n,b,u,!bitmap);
        struct rusage usage; if(getrusage(RUSAGE_SELF,&usage)) return 1;
        if(r>=0) printf("%s,%zu,%ld,%.9f,%zu,20261108,xorshift32_low16,%zu,%ld\n",
            argv[1],n,r,elapsed,u,n*sizeof(*a),usage.ru_maxrss);
    }
    free(a);free(b);return 0;
}
