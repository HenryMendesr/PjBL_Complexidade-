#include "dedup.h"
size_t bitmap_unique(uint16_t *a, size_t n) {
    uint64_t seen[1024]; /* exatamente 65536 bits; memória automática */
    for (size_t j = 0; j < 1024; ++j) seen[j] = 0;
    size_t u = 0;
    for (size_t i = 0; i < n; ++i) {
        uint16_t x = a[i];
        uint64_t mask = UINT64_C(1) << (x & 63);
        if (!(seen[x >> 6] & mask)) {
            seen[x >> 6] |= mask;
            a[u++] = x; /* u nunca supera i+1: escrita não destrói o futuro */
        }
    }
    return u;
}
