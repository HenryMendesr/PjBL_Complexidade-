import argparse
import csv
import gc
import hashlib
import json
import platform
import random
import resource
import statistics
import subprocess
import sys
import tracemalloc
from array import array
from datetime import datetime,timezone
from functools import partial
from pathlib import Path
from time import perf_counter_ns,perf_counter
from compilar import compile_native,FLAGS
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from heap import prepare_heap
from bitmap import bitmap_unique


def sources():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'src').iterdir()) if p.is_file()}


def validate(original,result,u,ordered):
    expected=set(original)
    prefix=result[:u]
    assert u==len(expected)==len(set(prefix)) and set(prefix)==expected
    assert list(prefix)==(sorted(expected) if ordered else list(dict.fromkeys(original)))


def native_evidence():
    frames={}
    report=(R/'build/heap.su').read_text()
    for line in report.splitlines():
        location,size,kind=line.split('\t')
        assert kind=='static'
        frames[location.split(':')[-1]]=int(size)
    assert set(frames)=={'sift','heap_unique'}
    undefined=subprocess.check_output(['nm','-u','build/heap.o'],cwd=R,text=True)
    assert not undefined.strip(),undefined
    stack=frames['sift']+frames['heap_unique']
    conservative=stack+16
    assert conservative<=256,conservative
    return {'metodo':'limite estático GCC -fstack-usage dos mesmos objetos usados no teste nativo e na biblioteca; inspeção de fonte e desmontagem',
            'frames_bytes':frames,'pilha_caminho_maximo_bytes':stack,'margem_abi_bytes':16,
            'limite_extra_conservador_bytes':conservative,'heap_dinamico_bytes':0,
            'relatorio_stack_usage':report,'simbolos_externos_nm_u':undefined,
            'desmontagem':subprocess.check_output(['objdump','-dr','build/heap.o'],cwd=R,text=True),
            'objeto_sha256':hashlib.sha256((R/'build/heap.o').read_bytes()).hexdigest(),
            'biblioteca_sha256':hashlib.sha256((R/'build/libheap.so').read_bytes()).hexdigest(),
            'compilador':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
            'flags':FLAGS,
            'escopo':'somente heap_unique e sift em C; independe de n; exclui chamador de testes, ctypes e Python; refazer para outra ABI/compilador/flags'}


def prepare(a,name):
    return prepare_heap(a) if name=='heap' else partial(bitmap_unique,a)


def main(memory_only=False):
    assert array('H').itemsize==2
    compile_native()
    native=native_evidence()
    env={'python':sys.version,'sistema':platform.platform(),
         'coleta_utc':datetime.now(timezone.utc).isoformat(),'seed':20261108,
         'gerador':'random.Random(seed).getrandbits(16)','repeticoes':3,'aquecimentos':1,
         'cpu_info':next((line.strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')),''),
         'fontes_sha256':sources(),'linguagens':{'heap':'C','bitmap':'Python'},
         'compilador_c':native['compilador'],'flags_c':FLAGS,
         'biblioteca_sha256':native['biblioteca_sha256'],'memoria_arquivo':'memoria.json'}
    if memory_only:
        old=json.loads((R/'dados/ambiente.json').read_text())
        assert old['fontes_sha256']==sources() and old['biblioteca_sha256']==native['biblioteca_sha256'],'Refaça os tempos após alterar fontes ou binário.'
    rows=[]
    memory=[]
    for n in [1000,100000,10000000]:
        rng=random.Random(20261108)
        original=array('H',(rng.getrandbits(16) for _ in range(n)))
        for name in ['heap','bitmap']:
            if not memory_only:
                for repetition in range(-1,3):
                    a=array('H',original)
                    run=prepare(a,name)
                    start=perf_counter_ns()
                    u=run()
                    seconds=(perf_counter_ns()-start)/1e9
                    validate(original,a,u,name=='heap')
                    print(f'{name} ({env["linguagens"][name]}) n={n} rodada={repetition} tempo={seconds:.6f}s u={u}',flush=True)
                    if repetition>=0:
                        rows.append({'algoritmo':name,'linguagem':env['linguagens'][name],'n':n,'rodada':repetition,'segundos':seconds,'u':u,'entrada_bytes':2*n})
            a=array('H',original)
            run=prepare(a,name)
            if name=='heap':
                u=run()
                entry={'algoritmo':name,'linguagem':'C','n':n,'u':u,'entrada_bytes':2*n,
                       'extra_bytes':native['limite_extra_conservador_bytes'],'tipo':'limite_pilha_gcc_com_margem',
                       'heap_dinamico_bytes':0,'metodo':'GCC estático + fonte/objeto auditados; execução C completa validada neste n'}
            else:
                bitmap_unique(array('H',[3,1,3,0,65535]))
                gc.collect()
                started=perf_counter()
                tracemalloc.start()
                baseline=tracemalloc.get_traced_memory()[0]
                tracemalloc.reset_peak()
                u=run()
                _,peak=tracemalloc.get_traced_memory()
                tracemalloc.stop()
                elapsed=perf_counter()-started
                entry={'algoritmo':name,'linguagem':'Python','n':n,'u':u,'entrada_bytes':2*n,
                       'extra_bytes':peak-baseline,'tipo':'pico_tracemalloc',
                       'segundos_rodada_instrumentada':elapsed,
                       'metodo':'uma execução completa rastreada; entrada/relógio/validação fora; não é RAM total do interpretador'}
            validate(original,a,u,name=='heap')
            memory.append(entry)
            print(f'memória {name} n={n}: {entry["extra_bytes"]} B ({entry["tipo"]})',flush=True)
    if not memory_only:
        with (R/'dados/resultados_empiricos.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
        summary=[]
        for n in [1000,100000,10000000]:
            for name in ['heap','bitmap']:
                group=[r for r in rows if r['n']==n and r['algoritmo']==name]
                times=[r['segundos'] for r in group]
                summary.append({'algoritmo':name,'linguagem':env['linguagens'][name],'n':n,'u':group[0]['u'],
                                'mediana_s':statistics.median(times),'min_s':min(times),'max_s':max(times),'entrada_bytes':2*n})
        (R/'dados/resumo.json').write_text(json.dumps(summary,indent=2))
        env['rss_pico_processo_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (R/'dados/ambiente.json').write_text(json.dumps(env,indent=2,ensure_ascii=False))
    data={'coleta_utc':datetime.now(timezone.utc).isoformat(),'fontes_sha256':sources(),
          'seed':20261108,'gerador':env['gerador'],'resultados':memory,'evidencia_c':native,
          'nota':'C: limite de pilha do compilador, não pico de tracemalloc. Python: pico de alocações rastreadas. Não somar com RSS nem contar infraestrutura como firmware.'}
    (R/'dados/memoria.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Coleta híbrida: Heap Sort em C e bitmap em Python.')
    parser.add_argument('--somente-memoria',action='store_true')
    args=parser.parse_args()
    main(args.somente_memoria)
