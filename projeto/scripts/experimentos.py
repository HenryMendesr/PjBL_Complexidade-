#!/usr/bin/env python3
"""Uma execução de processo por algoritmo/n; aquecimento + 7 rodadas."""
import csv, io, json, platform, statistics, subprocess, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def cmd(*a): return subprocess.check_output(a,cwd=ROOT,text=True)
def main():
    rows=[]
    env={'plataforma':platform.platform(),'maquina':platform.machine(),
         'cpu':cmd('lscpu'),'compilador':cmd('gcc','--version'),
         'flags':next(l for l in (ROOT/'Makefile').read_text().splitlines() if l.startswith('CFLAGS')),
         'python':platform.python_version(),'repeticoes':7,'aquecimentos':1,
         'relogio':'CLOCK_MONOTONIC','seed':20261108,
         'nota':'Ambiente local virtualizado; frequencia e compartilhamento nao controlados.'}
    (ROOT/'dados/ambiente.json').write_text(json.dumps(env,indent=2,ensure_ascii=False))
    for n in [1000,100000,10000000]:
        for alg in ['heap','bitmap']:
            result=cmd('./build/benchmark',alg,str(n),'7')
            part=list(csv.DictReader(io.StringIO(result)));rows.extend(part)
            times=[float(r['segundos']) for r in part]
            print(f'{alg:6s} n={n:8d} mediana={statistics.median(times):.6f}s u={part[0]["u"]}',flush=True)
    with (ROOT/'dados/resultados_empiricos.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
    fields=['algoritmo','n','mediana_s','min_s','max_s','q1_s','q3_s','u','pilha_compilador_bytes','margem_abi_bytes','extra_conservador_bytes','heap_algoritmo_bytes','entrada_bytes','rss_pico_kib']
    frames={}
    for file in [ROOT/'build/heap.su',ROOT/'build/bitmap.su']:
        for line in file.read_text().splitlines():
            loc,size,kind=line.split('\t'); assert kind=='static'
            frames[loc.split(':')[-1]]=int(size)
    (ROOT/'dados/evidencias').mkdir(exist_ok=True)
    for file in [ROOT/'build/heap.su',ROOT/'build/bitmap.su']:
        shutil.copy2(file,ROOT/'dados/evidencias'/file.name)
    # Soma de frames simultâneos, mais margem de 16 B na fronteira chamador/ABI.
    stack={'heap':frames['heap_unique']+frames['sift'],'bitmap':frames['bitmap_unique']}
    assert stack['heap']+16<=256
    # Nenhuma função externa é chamada pelos dois objetos: verifica alocação oculta.
    undefined=cmd('nm','-u','build/heap.o','build/bitmap.o')
    assert not any(l.strip() and not l.strip().endswith(':') for l in undefined.splitlines()),undefined
    (ROOT/'dados/memoria.txt').write_text('Frames GCC (-fstack-usage):\n'+json.dumps(frames,indent=2)+
        '\nHeap iterativo: soma heap_unique+sift + margem ABI 16 B.\nBitmap: frame bitmap_unique + margem ABI 16 B.\n'+
        'Heap dinamico dos algoritmos: 0 B (inspecao fonte + objetos sem simbolos externos).\n'+undefined)
    (ROOT/'dados/desmontagem.txt').write_text('\n'.join(line.rstrip() for line in cmd('objdump','-dr','build/heap.o','build/bitmap.o').splitlines())+'\n')
    summary=[]
    for n in [1000,100000,10000000]:
        for alg in ['heap','bitmap']:
            part=[r for r in rows if int(r['n'])==n and r['algoritmo']==alg]
            ts=sorted(float(r['segundos']) for r in part);q=statistics.quantiles(ts,n=4)
            summary.append(dict(zip(fields,[alg,n,statistics.median(ts),min(ts),max(ts),q[0],q[2],part[0]['u'],stack[alg],16,stack[alg]+16,0,2*n,max(int(r['rss_pico_kib']) for r in part)])))
    with (ROOT/'dados/resumo.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(summary)
if __name__=='__main__':main()
