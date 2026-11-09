
import math
D=65536; L10=math.log(10); C=1e-9; BLOOM_BYTES=78586
def lg(x):return math.log10(max(x,1e-300))
def logsum10(*values):
    largest=max(values)
    return largest+math.log10(sum(10**(value-largest) for value in values))
def models(n):
    if not isinstance(n,int) or n<1:raise ValueError("n deve ser inteiro positivo")
    u=D*(-math.expm1(n*math.log1p(-1/D)))

    q,r=divmod(n,D)
    logattempt=(math.lgamma(n+1)-(D-r)*math.lgamma(q+1)-r*math.lgamma(q+2))/L10
    time=[lg(C*n*max(1,u/2)),lg(5*C*n),lg(5*C*n*math.log2(u+1)),
          lg(7*C*n+BLOOM_BYTES*C),lg(C*n)+logattempt,
          lg(n)+n*math.log10(2)-9,lg((n*32768.5)*((n+1)/2)/1e9),lg(C*n*n)]
    ram=[lg(128),lg(16*u+128),lg(32*u+128),lg(BLOOM_BYTES+128),
         lg(128),logsum10(lg(n+16)+n*math.log10(2),lg(16*(n+1)+128)),lg(128),lg(math.ceil(n*n/8)+128)]
    return time,ram
names=['Força bruta','Hash','Árvore balanceada','Bloom (1%)','Bogosort','Subconjuntos','Unário (I/O)','Matriz (bits)']
