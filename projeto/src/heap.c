#include "dedup.h"


static void sift(uint16_t *a, size_t root, size_t end) {
    while (root < end / 2) {
        size_t child = 2 * root + 1;
        if (child + 1 < end && a[child] < a[child + 1]) ++child;
        if (a[root] >= a[child]) break;
        uint16_t tmp = a[root]; a[root] = a[child]; a[child] = tmp;
        root = child;
    }
}
size_t heap_unique(uint16_t *a, size_t n) {
    if (n < 2) return n;
    for (size_t i = n / 2; i > 0; --i) sift(a, i - 1, n);
    for (size_t end = n; end > 1;) {
        --end;
        uint16_t tmp = a[0]; a[0] = a[end]; a[end] = tmp;
        sift(a, 0, end);
    }
    size_t u = 1;
    for (size_t i = 1; i < n; ++i)
        if (a[i] != a[u - 1]) a[u++] = a[i];
    return u;
}
