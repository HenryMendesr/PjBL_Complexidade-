import csv
import gc
import hashlib
import json
import platform
import random
import resource
import statistics
import sys
import tracemalloc
from array import array
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter_ns
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
    memory = {}
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
            if n == 1000:
                a = array('H',original)
                gc.collect()
                tracemalloc.start()
                baseline = tracemalloc.get_traced_memory()[0]
                tracemalloc.reset_peak()
                run(a)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                memory[name] = {'pico_alocacoes_rastreadas_bytes':peak-baseline,'n_medido':n,
                                'metodo':'tracemalloc; rodada separada dos tempos; entrada criada antes; não inclui toda a memória interna do interpretador'}
            with (R/'dados/resultados_empiricos.csv').open('w') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    summary=[]
    for n in [1000,100000,10000000]:
        for name in ['heap','bitmap']:
            group=[r for r in rows if r['n']==n and r['algoritmo']==name]
            ts=[r['segundos'] for r in group]
            summary.append({'algoritmo':name,'n':n,'u':group[0]['u'],'mediana_s':statistics.median(ts),'min_s':min(ts),'max_s':max(ts),'entrada_bytes':2*n})
    (R/'dados/resumo.json').write_text(json.dumps(summary,indent=2))
    env['memoria']=memory
    env['rss_pico_processo_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (R/'dados/ambiente.json').write_text(json.dumps(env,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
