"""Modelos teóricos; nenhuma implementação de deduplicação."""
import math
D=65536; L10=math.log(10); C=1e-9
def lg(x):return math.log10(max(x,1e-300))
def models(n):
    u=D*(-math.expm1(n*math.log1p(-1/D)))
    # Bogosort: todos distintos quando possível; multiplicidades balanceadas depois.
    q,r=divmod(n,D)
    logattempt=(math.lgamma(n+1)-(D-r)*math.lgamma(q+1)-r*math.lgamma(q+2))/L10
    time=[lg(C*n*max(1,u/2)),lg(5*C*n),lg(5*C*n*math.log2(u+1)),
          lg(7*C*n+78586*C),lg(C*n)+logattempt,
          lg(n)+n*math.log10(2)-9,lg((n*32768.5)*((n+1)/2)/1e9),lg(C*n*n)]
    ram=[lg(128),lg(16*u+128),lg(32*u+128),lg(math.ceil(-7*u/math.log(1-.01**(1/7))/8)+128),
         lg(128),lg(n)+n*math.log10(2),lg(128),lg(math.ceil(n*n/8)+128)]
    return time,ram
names=['Força bruta','Hash','Árvore balanceada','Bloom (1%)','Bogosort','Subconjuntos','Unário (I/O)','Matriz (bits)']
