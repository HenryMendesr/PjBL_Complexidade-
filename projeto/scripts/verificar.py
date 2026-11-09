#!/usr/bin/env python3
import csv, hashlib, json, math, re, statistics, subprocess
from pathlib import Path
from modelos import models,names
R=Path(__file__).resolve().parents[1]
def read(p):return list(csv.DictReader((R/p).open()))
def digest(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def main():
    required=['src/heap.c','src/bitmap.c','src/main.c','tests/test.c','docs/analise_teorica.md','docs/relatorio.md','dados/ambiente.json','dados/memoria.txt','relatorio.pdf','README.md','Makefile','requirements.txt','graficos/tempo.png','graficos/memoria.png','dados/evidencias/heap.su','dados/evidencias/bitmap.su','docs/fundamentacao_matematica.md','docs/auditoria.md','dados/revisao_matematica.txt','dados/calculos_quantitativos.csv','dados/manifesto_graficos.json']
    subprocess.run(['python3',str(R/'scripts/validar_matematica.py')],check=True)
    for p in required:assert (R/p).is_file() and (R/p).stat().st_size>0,p
    raw=read('dados/resultados_empiricos.csv');summary=read('dados/resumo.csv')
    keys={(alg,str(n)) for alg in ['heap','bitmap'] for n in [1000,100000,10000000]}
    assert len(raw)==42 and len(summary)==6
    assert {(r['algoritmo'],r['n']) for r in summary}==keys
    assert {(r['algoritmo'],r['n']) for r in raw}==keys
    env=json.loads((R/'dados/ambiente.json').read_text())
    for path,h in env['fontes_sha256'].items():assert digest(path)==h,('fonte mudou após coleta',path)
    assert env['flags']==next(line for line in (R/'Makefile').read_text().splitlines() if line.startswith('CFLAGS'))
    if (R/'build/benchmark').exists():assert digest('build/benchmark')==env['binario_sha256'],'binário difere do medido'
    frames={}
    for filename in ['heap','bitmap']:
        for line in (R/f'dados/evidencias/{filename}.su').read_text().splitlines():
            loc,size,kind=line.split('\t');assert kind=='static'
            frames[loc.split(':')[-1]]=int(size)
    stack={'heap':frames['heap_unique']+frames['sift'],'bitmap':frames['bitmap_unique']}
    report=(R/'docs/relatorio.md').read_text()
    for s in summary:
        group=[r for r in raw if (r['n'],r['algoritmo'])==(s['n'],s['algoritmo'])]
        assert len(group)==7 and sorted(int(r['rodada']) for r in group)==list(range(7))
        t=[float(r['segundos']) for r in group];assert all(math.isfinite(v) and v>0 for v in t)
        q=statistics.quantiles(t,n=4)
        for field,expected in [('mediana_s',statistics.median(t)),('min_s',min(t)),('max_s',max(t)),('q1_s',q[0]),('q3_s',q[2])]:
            assert math.isclose(float(s[field]),expected,rel_tol=1e-12,abs_tol=1e-15),field
        assert {r['u'] for r in group}=={s['u']}
        assert all(r['seed']==str(env['seed']) and r['distribuicao']=='xorshift32_low16' and int(r['entrada_bytes'])==2*int(r['n']) for r in group)
        assert 0<int(s['u'])<=min(int(s['n']),65536)
        assert int(s['entrada_bytes'])==2*int(s['n'])
        assert int(s['rss_pico_kib'])==max(int(r['rss_pico_kib']) for r in group)
        assert int(s['pilha_compilador_bytes'])==stack[s['algoritmo']]
        assert int(s['margem_abi_bytes'])==16 and int(s['extra_conservador_bytes'])==stack[s['algoritmo']]+16
        assert int(s['heap_algoritmo_bytes'])==0
        if s['algoritmo']=='heap':assert int(s['extra_conservador_bytes'])<=256
        expected=f"| {s['algoritmo']} | {s['n']} | {s['u']} | {float(s['mediana_s']):.9f} | {float(s['min_s']):.9f}–{float(s['max_s']):.9f} | {float(s['q1_s']):.9f}–{float(s['q3_s']):.9f} | {s['extra_conservador_bytes']} | {s['rss_pico_kib']} |"
        assert expected in report,'tabela desatualizada'
    for n in ['1000','100000','10000000']:assert len({s['u'] for s in summary if s['n']==n})==1
    manifest=json.loads((R/'dados/manifesto_graficos.json').read_text())
    for field in ['entradas_sha256','saidas_sha256']:
        for path,h in manifest[field].items():assert digest(path)==h,('gráfico desatualizado',path)
    assert manifest['estrategias_extrapoladas']==names
    for point,s in zip(manifest['pontos_medidos'],summary):
        for key,value in point.items():assert str(value)==s[key] if key in ['algoritmo'] else float(value)==float(s[key])
    assert len(manifest['pontos_medidos'])==6
    predicted=read('dados/previsoes_log10.csv')
    assert len(predicted)==len(names)*len(manifest['grade_n'])==808
    assert {(int(r['n']),r['estrategia']) for r in predicted}=={(n,name) for n in manifest['grade_n'] for name in names}
    for r in predicted:
        n=int(r['n']);i=names.index(r['estrategia']);t,m=models(n)
        for field,expected in [('log10_segundos_previstos',t[i]),('log10_ram_extra_bytes_previstos',m[i])]:
            assert math.isfinite(float(r[field])) and math.isclose(float(r[field]),expected,rel_tol=1e-12,abs_tol=1e-12)
    calc=read('dados/calculos_quantitativos.csv');assert {r['n'] for r in calc}=={'1000','100000','10000000'} and len(calc)==3
    for r in calc:
        n=int(r['n'])
        assert int(r['unario_bytes_esperados'])==65537*n//2
        assert int(r['unario_trafego_esperado_bytes'])==65537*n*(n+1)//4
        assert int(r['matriz_celulas'])==int(r['matriz_bytes'])==n*n
        assert int(r['matriz_bits_empacotados_bytes'])==(n*n+7)//8
    for logfile in ['dados/testes.txt','dados/sanitizers.txt']:
        text=(R/logfile).read_text();assert 'OK: 3502 casos x 2 algoritmos' in text
        assert 'ERROR: AddressSanitizer' not in text and 'runtime error:' not in text
    for p in ['fundamentacao_matematica','analise_teorica','metodologia','modelos','discussao','checklist','apresentacao','auditoria']:
        assert (R/f'docs/{p}.md').read_text() in report,('fonte do relatório desatualizada',p)
    text=subprocess.check_output(['pdftotext',str(R/'relatorio.pdf'),'-'],text=True)
    for term in ['Força bruta','Hash','Árvore','Bloom','Bogosort','Subconjuntos','Unário','Matriz','Resultados locais','Metodologia','256','96','Henry Rodrigues','Rafael Maluf','Matheus']:
        assert term in text,term
    for s in summary:assert f"{float(s['mediana_s']):.9f}" in text
    for p in (R/'scripts').glob('*.py'):
        import io,tokenize
        assert not any(t.type==tokenize.COMMENT and not t.string.startswith('#!') for t in tokenize.generate_tokens(io.StringIO(p.read_text()).readline)),p
    if (R/'build/benchmark').exists():
        for alg in ['heap','bitmap']:
            for n,reps in [(' -18446744073709551615','1'),('','1'),('0','1'),('18446744073709551615','1'),('1',''),('1','1001'),('1','9999999999999999999999999999999999')]:
                result=subprocess.run([str(R/'build/benchmark'),alg,n,reps],capture_output=True,text=True)
                assert result.returncode!=0 and not result.stdout,(alg,n,reps)
    print(f'OK: {len(raw)} medições, {len(summary)} resumos, {len(predicted)} previsões; quartis, frames, fontes, manifesto gráfico, tabelas e PDF coerentes.')
if __name__=='__main__':main()
