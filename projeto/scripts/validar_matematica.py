#!/usr/bin/env python3

import math, csv
from pathlib import Path
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
    exact=((n+16)<<n)+16*(n+1)+128
    check(math.isclose(ram[5],math.log10(exact),abs_tol=1e-9))
    check(math.isclose(ram[3],math.log10(78586+128),abs_tol=1e-12))
for n in [65535,65536,65537,100000,10000000]:
    q,r=divmod(n,65536)
    independent=math.fsum(math.log10(i) for i in range(1,n+1))
    independent-=(65536-r)*math.fsum(math.log10(i) for i in range(1,q+1))
    independent-=r*math.fsum(math.log10(i) for i in range(1,q+2))
    check(math.isclose(models(n)[0][4],independent+math.log10(n)-9,rel_tol=0,abs_tol=2e-7))
for n in range(1,33):
    heights=[]
    for node in range(n):
        h=0;j=node
        while 2*j+1<n:j=2*j+1;h+=1
        heights.append(h)
    for h in range(1,max(heights)+1):check(sum(v>=h for v in heights)<=n//2**h)
for n in range(1,100):
    for u in range(1,min(n,65536)+1):
        explicit=sum(range(u))+(n-u)*u
        check(explicit==u*(u-1)//2+(n-u)*u)
for cells in [1000**2,100000**2,10000000**2]:
    check((cells+7)//8==math.ceil(cells/8))
root=Path(__file__).resolve().parents[1]
with (root/'dados/calculos_quantitativos.csv').open('w') as f:
    w=csv.writer(f,lineterminator="\n")
    w.writerow(['n','bogo_log10_tentativas_balanceadas','bogo_log10_segundos_modelo','power_log10_subconjuntos','power_log10_payload_bytes','power_pilha_nominal_bytes','unario_bytes_esperados','unario_trafego_esperado_bytes','unario_segundos_io_modelo','matriz_celulas','matriz_bytes','matriz_bits_empacotados_bytes','matriz_segundos_modelo'])
    for n in [1000,100000,10000000]:
        q,r=divmod(n,65536)
        logb=math.fsum(math.log10(i) for i in range(1,n+1))-(65536-r)*math.fsum(math.log10(i) for i in range(1,q+1))-r*math.fsum(math.log10(i) for i in range(1,q+2))
        storage=65537*n//2;traffic=65537*n*(n+1)//4
        w.writerow([n,logb,logb+math.log10(n)-9,math.log10(1<<n),math.log10(n<<n),16*(n+1),storage,traffic,traffic/1e9,n*n,n*n,(n*n+7)//8,n*n/1e9])
print(f'OK: {checks} verificações matemáticas; incluem grades de parâmetros e contagens independentes.')
print(f'log10(1000!) = {logfact:.12f}')
print(f'Bloom: {byte_count} B, k={k}, p aproximado={rate:.12f}; 78521 B dariam {oldrate:.12f}.')
print(f'Unário, n=10^7: E[V]={327685*10_000_000*10_000_001//20} B.')
print('Subconjuntos, n=1000: log10(payload B) =',math.log10(1000)+1000*math.log10(2))
