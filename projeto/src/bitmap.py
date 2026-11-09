def bitmap_unique(a):
    seen = bytearray(8192)
    u = 0
    for i in range(len(a)):
        x = a[i]
        index = x >> 3
        mask = 1 << (x & 7)
        if not seen[index] & mask:
            seen[index] |= mask
            a[u] = x
            u += 1
    return u
