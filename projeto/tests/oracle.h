#ifndef ORACLE_H
#define ORACLE_H
#include "dedup.h"
#include <assert.h>
#include <string.h>


static void validate(const uint16_t *input, size_t n, const uint16_t *out,
                     size_t u, int sorted) {
    size_t freq[65536] = {0};
    size_t expected = 0;
    for (size_t i=0; i<n; ++i) if (!freq[input[i]]++) ++expected;
    assert(u == expected && u <= n);
    for (size_t i=0; i<u; ++i) {
        assert(freq[out[i]] > 0); freq[out[i]]=0;
        if (sorted && i) assert(out[i-1] < out[i]);
    }
    for (size_t x=0; x<65536; ++x) assert(freq[x]==0);
    if (!sorted) {
        unsigned char first[65536]={0}; size_t k=0;
        for (size_t i=0;i<n;++i) if (!first[input[i]]) {
            first[input[i]]=1; assert(k<u && out[k++]==input[i]);
        }
        assert(k==u);
    }
}
#endif
