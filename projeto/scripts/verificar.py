#!/usr/bin/env python3
"""Checagens de integridade da entrega e de coerência CSV/modelos."""
import csv, math, statistics, subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return list(csv.DictReader((R/p).open()))
def main():
    required=['src/heap.c','src/bitmap.c','src/main.c','tests/test.c','docs/analise_teorica.md','docs/relatorio.md','dados/ambiente.json','dados/memoria.txt','relatorio.pdf','README.md','Makefile','requirements.txt','graficos/tempo.png','graficos/memoria.png','dados/evidencias/heap.su','dados/evidencias/bitmap.su']
    required += ['docs/fundamentacao_matematica.md','dados/revisao_matematica.txt']
    subprocess.run(['python3',str(R/'scripts/validar_matematica.py')],check=True)
    for p in required:assert (R/p).is_file() and (R/p).stat().st_size>0,p
    raw=read('dados/resultados_empiricos.csv');summary=read('dados/resumo.csv')
    assert len(raw)==42 and len(summary)==6
    for s in summary:
        group=[r for r in raw if r['n']==s['n'] and r['algoritmo']==s['algoritmo']]
        assert len(group)==7
        t=[float(r['segundos']) for r in group];assert all(math.isfinite(v) and v>0 for v in t)
        assert math.isclose(statistics.median(t),float(s['mediana_s']),rel_tol=1e-12)
        assert min(t)==float(s['min_s']) and max(t)==float(s['max_s'])
        assert len({r['u'] for r in group})==1
        assert int(s['u'])<=min(int(s['n']),65536)
        assert int(s['entrada_bytes'])==2*int(s['n'])
        assert int(s['heap_algoritmo_bytes'])==0
        if s['algoritmo']=='heap':assert int(s['extra_conservador_bytes'])<=256
    for n in ['1000','100000','10000000']:
        assert len({s['u'] for s in summary if s['n']==n})==1
    predicted=read('dados/previsoes_log10.csv');assert len({r['estrategia'] for r in predicted})==8
    from modelos import models,names
    for r in predicted:
        n=int(r['n']);i=names.index(r['estrategia']);t,m=models(n)
        assert math.isclose(float(r['log10_segundos_previstos']),t[i],rel_tol=1e-12,abs_tol=1e-12)
        assert math.isclose(float(r['log10_ram_extra_bytes_previstos']),m[i],rel_tol=1e-12,abs_tol=1e-12)
    for logfile in ['dados/testes.txt','dados/sanitizers.txt']:
        text=(R/logfile).read_text();assert 'OK: 222 casos x 2 algoritmos' in text
        assert 'ERROR: AddressSanitizer' not in text and 'runtime error:' not in text
    text=subprocess.check_output(['pdftotext',str(R/'relatorio.pdf'),'-'],text=True)
    for term in ['Bogosort','Resultados locais','PENDENTE','Metodologia','Extrapolações','256','96']:
        assert term in text,term
    print(f'OK: {len(raw)} medições, {len(summary)} resumos, {len(predicted)} previsões; PDF, fontes e evidências presentes e coerentes.')
if __name__=='__main__':main()
