#ifndef DEDUP_H
#define DEDUP_H
#include <stddef.h>
#include <stdint.h>



size_t heap_unique(uint16_t *a, size_t n);
size_t bitmap_unique(uint16_t *a, size_t n);
#endif
