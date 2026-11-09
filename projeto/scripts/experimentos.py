import argparse
import csv
import ctypes
import gc
import hashlib
import json
import platform
import random
import re
import resource
import statistics
import sys
import sysconfig
import tracemalloc
from array import array
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter, perf_counter_ns
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'src'))
from heap import heap_unique
from bitmap import bitmap_unique


def validate(original, result, u, ordered):
    expected = set(original)
    prefix = result[:u]
    assert u == len(expected) == len(set(prefix)) and set(prefix) == expected
    if ordered:
        assert all(prefix[i-1] < prefix[i] for i in range(1,u))
    else:
        assert list(prefix) == list(dict.fromkeys(original))


def main():
    assert array('H').itemsize == 2
    env = {'python': sys.version, 'sistema': platform.platform(), 'cpu': platform.processor(),
           'coleta_utc': datetime.now(timezone.utc).isoformat(), 'seed': 20261108,
           'gerador': 'random.Random(seed).getrandbits(16)', 'repeticoes': 3, 'aquecimentos': 1,
           'cpu_info': next((line.strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')), ''),
           'fontes_sha256': {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'src').glob('*.py')}}
    rows = []
    for n in [1000,100000,10000000]:
        rng = random.Random(20261108)
        original = array('H', (rng.getrandbits(16) for _ in range(n)))
        for name, run in [('heap',heap_unique),('bitmap',bitmap_unique)]:
            times = []
            for repetition in range(-1,3):
                a = array('H', original)
                start = perf_counter_ns()
                u = run(a)
                seconds = (perf_counter_ns()-start)/1e9
                validate(original,a,u,name=='heap')
                print(f'{name} n={n} rodada={repetition} tempo={seconds:.6f}s u={u}',flush=True)
                if repetition >= 0:
                    times.append(seconds)
                    rows.append({'algoritmo':name,'n':n,'rodada':repetition,'segundos':seconds,'u':u,'entrada_bytes':2*n})
            with (R/'dados/resultados_empiricos.csv').open('w') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    summary=[]
    for n in [1000,100000,10000000]:
        for name in ['heap','bitmap']:
            group=[r for r in rows if r['n']==n and r['algoritmo']==name]
            ts=[r['segundos'] for r in group]
            summary.append({'algoritmo':name,'n':n,'u':group[0]['u'],'mediana_s':statistics.median(ts),'min_s':min(ts),'max_s':max(ts),'entrada_bytes':2*n})
    (R/'dados/resumo.json').write_text(json.dumps(summary,indent=2))
    env['memoria_arquivo']='memoria.json'
    env['rss_pico_processo_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (R/'dados/ambiente.json').write_text(json.dumps(env,indent=2,ensure_ascii=False))


def frame_capacity():
    if sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12):
        return {'estado':'não verificável automaticamente nesta versão do interpretador'}
    path=Path(sysconfig.get_path('include'))/'internal/pycore_frame.h'
    if not path.exists():
        return {'estado':'cabeçalho interno do CPython não disponível'}
    source=path.read_text()
    block=source.split('typedef struct _PyInterpreterFrame {',1)[1].split('} _PyInterpreterFrame;',1)[0]
    clean=re.sub(r'/\*.*?\*/|//[^\n]*','',block,flags=re.S)
    pointers=['f_code','previous','f_funcobj','f_globals','f_builtins','f_locals','frame_obj','prev_instr']
    expected=pointers+['stacktop','return_offset','owner','localsplus']
    names=re.findall(r'\b(\w+)(?:\[\d+\])?\s*;',clean)
    if names!=expected:
        return {'estado':'layout do cabeçalho difere do modelo suportado'}
    class Layout(ctypes.Structure):
        _fields_=[(name,ctypes.c_void_p) for name in pointers]+[('stacktop',ctypes.c_int),('return_offset',ctypes.c_uint16),('owner',ctypes.c_char),('localsplus',ctypes.c_void_p*1)]
    from heap import sift
    frames={}
    word=ctypes.sizeof(ctypes.c_void_p)
    header=Layout.localsplus.offset
    for run in [heap_unique,sift]:
        code=run.__code__
        if code.co_cellvars or code.co_freevars:
            return {'estado':'layout com closures não suportado por este cálculo'}
        frames[run.__name__]={'locais_slots':code.co_nlocals,'pilha_avaliacao_slots':code.co_stacksize,
                             'capacidade_bytes_calculada':header+word*(code.co_nlocals+code.co_stacksize)}
    return {'estado':'calculado para o CPython instalado, não medido por tracemalloc',
            'cabecalho_fonte':str(path),'cabecalho_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'ponteiro_bytes':word,'cabecalho_frame_bytes':header,'frames':frames,
            'caminho_heap_unique_sift_bytes':sum(f['capacidade_bytes_calculada'] for f in frames.values()),
            'limite':'capacidade simultânea dos frames, possivelmente servida de arena já reservada; não inclui objetos referenciados nem toda a pilha nativa; não somar diretamente ao pico de alocações'}


def collect_memory():
    assert array('H').itemsize == 2
    results = []
    data = {'pilha_cpython':frame_capacity(),'python':sys.version,'sistema':platform.platform(),
            'coleta_utc':datetime.now(timezone.utc).isoformat(),'seed':20261108,
            'gerador':'random.Random(seed).getrandbits(16)',
            'repeticoes_por_combinacao':1,
            'aquecimento':'mesma função em entrada pequena; gc.collect antes de cada rastreamento',
            'metodo':'tracemalloc; execução completa separada dos tempos; entrada, relógio e validação preparados fora do rastreamento; não inclui toda a memória interna do interpretador',
            'fontes_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'src').glob('*.py')},
            'resultados':results}
    for n in [1000,100000,10000000]:
        rng=random.Random(20261108)
        original=array('H',(rng.getrandbits(16) for _ in range(n)))
        for name,run in [('bitmap',bitmap_unique),('heap',heap_unique)]:
            warm=array('H',[3,1,3,0,65535]);run(warm);del warm
            a=array('H',original)
            print(f'Iniciando memória: {name} n={n}; a execução rastreada pode demorar.',flush=True)
            gc.collect()
            started=perf_counter()
            tracemalloc.start()
            baseline=tracemalloc.get_traced_memory()[0]
            tracemalloc.reset_peak()
            u=run(a)
            current,peak=tracemalloc.get_traced_memory()
            tracemalloc.stop()
            elapsed=perf_counter()-started
            validate(original,a,u,name=='heap')
            results.append({'algoritmo':name,'n':n,'u':u,
                            'pico_alocacoes_rastreadas_bytes':peak-baseline,
                            'retido_apos_chamada_bytes':current-baseline,
                            'segundos_rodada_instrumentada':elapsed,
                            'entrada_bytes':2*n,
                            'rss_pico_processo_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
            (R/'dados/memoria.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
            print(f"memória: {name} n={n} pico={peak-baseline} B u={u}; {elapsed:.3f} s instrumentados",flush=True)
    oldenv=json.loads((R/'dados/ambiente.json').read_text())
    oldenv.pop('memoria',None)
    oldenv['memoria_arquivo']='memoria.json'
    (R/'dados/ambiente.json').write_text(json.dumps(oldenv,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Mede tempo sem rastreamento e memória em execuções separadas.')
    parser.add_argument('--somente-memoria',action='store_true',help='executa só a coleta de memória nas três escalas e preserva os tempos existentes')
    args=parser.parse_args()
    if not args.somente_memoria:
        main()
    collect_memory()
