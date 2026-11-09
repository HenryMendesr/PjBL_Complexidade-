def sift(a, root, end):
    while root < end // 2:
        child = 2 * root + 1
        if child + 1 < end and a[child] < a[child + 1]:
            child += 1
        if a[root] >= a[child]:
            break
        temp = a[root]
        a[root] = a[child]
        a[child] = temp
        root = child


def heap_unique(a):
    n = len(a)
    if n < 2:
        return n
    for i in range(n // 2 - 1, -1, -1):
        sift(a, i, n)
    for end in range(n - 1, 0, -1):
        temp = a[0]
        a[0] = a[end]
        a[end] = temp
        sift(a, 0, end)
    u = 1
    for i in range(1, n):
        if a[i] != a[u - 1]:
            a[u] = a[i]
            u += 1
    return u
