#ifndef DEDUP_H
#define DEDUP_H
#include <stddef.h>
#include <stdint.h>
/* a aponta para n uint16_t válidos (ou NULL se n=0).
 * Modificam a; retornam u. Apenas a[0..u) é saída válida.
 * heap_unique ordena; bitmap_unique preserva primeiras ocorrências. */
size_t heap_unique(uint16_t *a, size_t n);
size_t bitmap_unique(uint16_t *a, size_t n);
#endif
