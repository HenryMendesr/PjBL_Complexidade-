#!/usr/bin/env python3

import math
from itertools import permutations, product
from collections import Counter
from modelos import models
checks=0
def check(ok):
    global checks
    assert ok
    checks+=1

for values in [(0,1,2,3),(1,1,2),(0,0,1,1),(5,5,5),(0,1,1,2,2)]:
    ordered=tuple(sorted(values));n=len(values)
    successes=sum(tuple(values[i] for i in order)==ordered for order in permutations(range(n)))
    multiplicities=math.prod(math.factorial(c) for c in Counter(values).values())
    check(successes==multiplicities)
    check(math.factorial(n)//successes==len(set(permutations(values))))

for n in range(1,13):
    count=sum(mask.bit_count() for mask in range(1<<n))
    check(count==n*2**(n-1))
    check(2*count==n*2**n)

for d in [2,3,4]:
    for n in range(1,6):
        empirical=sum(len(set(s)) for s in product(range(d),repeat=n))/d**n
        formula=d*(1-(1-1/d)**n)
        check(math.isclose(empirical,formula,rel_tol=1e-12))

for lengths in [(1,2,3),(65536,1,65536),(1,1,1,1),(17,)]:
    n=len(lengths)
    traffic=sum(lengths)+sum(sum(lengths[:i]) for i in range(n))
    weighted=sum((n-j)*length for j,length in enumerate(lengths))
    check(traffic==weighted)
for n in range(1,30):
    check(sum(range(1,n+1))==n*(n+1)//2)

u=65536;k=7;p=.01
byte_count=math.ceil((-k*u/math.log(1-p**(1/k)))/8)
rate=(1-math.exp(-k*u/(8*byte_count)))**k
oldrate=(1-math.exp(-k*u/(8*78521)))**k
check(byte_count==78586);check(rate<=p);check(oldrate>p)

logfact=sum(math.log10(j) for j in range(1,1001))
check(math.isclose(logfact,math.lgamma(1001)/math.log(10),abs_tol=1e-9))
check(math.isclose(logfact,2567.604644222133,abs_tol=1e-9))

for n in [1,2,10,1000,100000,10000000]:
    time,ram=models(n)
    check(math.isclose(time[5],math.log10(n)+n*math.log10(2)-9,abs_tol=1e-10))
    check(math.isclose(time[6],math.log10(32768.5*n*(n+1)/2/1e9),abs_tol=1e-10))
    check(math.isclose(ram[5],math.log10(n)+n*math.log10(2),abs_tol=1e-10))
print(f'OK: {checks} verificações matemáticas independentes.')
print(f'log10(1000!) = {logfact:.12f}')
print(f'Bloom: {byte_count} B, k={k}, p aproximado={rate:.12f}; 78521 B dariam {oldrate:.12f}.')
print(f'Unário, n=10^7: E[V]={327685*10_000_000*10_000_001//20} B.')
print('Subconjuntos, n=1000: log10(payload B) =',math.log10(1000)+1000*math.log10(2))
