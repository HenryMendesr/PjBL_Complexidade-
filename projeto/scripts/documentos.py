import csv
import json
import math
import re
from pathlib import Path
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from modelos import models, names, lg
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'dados/resumo.json').read_text())
env=json.loads((R/'dados/ambiente.json').read_text())
memory_env=json.loads((R/'dados/memoria.json').read_text())
memory=memory_env['resultados']
assert len(memory)==6 and {(m['algoritmo'],m['n']) for m in memory}=={(alg,n) for alg in ['heap','bitmap'] for n in [1000,100000,10000000]}
assert memory_env['fontes_sha256']==env['fontes_sha256']
assert memory_env['seed']==env['seed'] and memory_env['gerador']==env['gerador']
for m in memory:
    expected=next(r for r in rows if r['algoritmo']==m['algoritmo'] and r['n']==m['n'])
    assert m['u']==expected['u'] and m['entrada_bytes']==expected['entrada_bytes']
ns=np.unique(np.rint(np.logspace(3,7,101)).astype(int))
mt=np.array([models(int(n))[0] for n in ns])
mm=np.array([models(int(n))[1] for n in ns])
with (R/'dados/previsoes.csv').open('w') as f:
    w=csv.writer(f,lineterminator='\n')
    w.writerow(['n','estrategia','log10_segundos_modelo','log10_ram_bytes_modelo'])
    for i,n in enumerate(ns):
        for j,name in enumerate(names):w.writerow([int(n),name,mt[i,j],mm[i,j]])
plt.rcParams.update({'font.size':14,'axes.titlesize':19,'axes.labelsize':15,'legend.fontsize':12,'lines.linewidth':2.4,'savefig.dpi':200})
colorset=plt.cm.tab10.colors
styles=['--',':','-.','--',':','-.','--',':']
def new(title,ylabel):
    fig,ax=plt.subplots(figsize=(15,9))
    ax.set_title(title,pad=20)
    ax.set_xscale('log');ax.set_xlabel('Quantidade de leituras (n)');ax.set_ylabel(ylabel)
    ax.grid(True,which='major',alpha=.28)
    return fig,ax

def finish(fig,ax,name,note):
    ax.set_xlim(800,14000000)
    ax.legend(loc='center left',bbox_to_anchor=(1.02,.5),frameon=False)
    fig.text(.07,.035,note,fontsize=12)
    fig.subplots_adjust(left=.09,right=.72,bottom=.13,top=.89)
    fig.savefig(R/f'graficos/{name}.png',facecolor='white')
    plt.close(fig)

def measured(ax,expo=False):
    for k,alg in enumerate(['heap','bitmap']):
        group=[r for r in rows if r['algoritmo']==alg]
        x=[r['n'] for r in group];y=[r['mediana_s'] for r in group]
        ax.plot(x,[lg(t) for t in y] if expo else y,'o-',color=colorset[k],markersize=9,linewidth=3.3,label=alg+' — medido em Python',zorder=5)
        if not expo:
            ax.errorbar(x,y,yerr=[[r['mediana_s']-r['min_s'] for r in group],[r['max_s']-r['mediana_s'] for r in group]],fmt='none',capsize=5,color=colorset[k])

fig,ax=new('Tempo real das duas implementações Python','Tempo (segundos)')
ax.set_yscale('log');measured(ax)
ax.axhline(2,color='#555555',linewidth=1.4,label='Meta na referência: 2 s')
finish(fig,ax,'tempo_medido','Pontos: medianas de 3 rodadas; barras: mínimo e máximo. Medições locais.')
fig,ax=new('Tempo comparativo — faixa prática','Tempo (segundos)')
ax.set_yscale('log');ax.set_ylim(1e-6,1e6)
for j,name in enumerate(names):ax.plot(ns,10**np.clip(mt[:,j],-15,8),styles[j],color=colorset[j+2],label=name+' — modelo')
measured(ax)
finish(fig,ax,'tempo_comparativo','Modelos: custos nominais de baixo nível, não calibrados para Python. Curvas fora da faixa em tempo_completo.png.')
fig,ax=new('Tempo comparativo — todas as ordens de grandeza','Expoente E: tempo = 10^E segundos')
for j,name in enumerate(names):ax.plot(ns,mt[:,j],styles[j],color=colorset[j+2],label=name+' — modelo')
measured(ax,True);ax.set_yscale('symlog',linthresh=10)
ax.set_yticks([-6,0,6,100,10000,1000000,100000000],['−6','0','6','100','10 000','1 000 000','100 000 000'])
finish(fig,ax,'tempo_completo','E é um expoente, não uma duração. Eixo comprimido para manter as oito curvas, inclusive fatoriais e exponenciais.')
fig,ax=new('Memória das duas implementações Python','Pico de alocações rastreadas (bytes)')
ax.set_yscale('log')
for k,alg in enumerate(['heap','bitmap']):
    group=sorted((m for m in memory if m['algoritmo']==alg),key=lambda m:m['n'])
    ax.plot([m['n'] for m in group],[m['pico_alocacoes_rastreadas_bytes'] for m in group],'o-',color=colorset[k],markersize=9,label=alg+' — pico rastreado')
    for m in group:
        ax.annotate(str(m['pico_alocacoes_rastreadas_bytes'])+' B',(m['n'],m['pico_alocacoes_rastreadas_bytes']),xytext=(0,12),textcoords='offset points',ha='center',fontsize=12)
ax.axhline(256,color='#555555',linestyle='--',label='Limite Embarca: 256 B')
ax.set_ylim(bottom=128,top=max(m['pico_alocacoes_rastreadas_bytes'] for m in memory)*1.6)
finish(fig,ax,'memoria_algoritmos','Uma execução completa rastreada por combinação. Entrada e validação fora do rastreamento; não é RAM total.')
fig,ax=new('Memória comparativa — modelos e Python medido','Expoente E: memória = 10^E bytes')
for j,name in enumerate(names):ax.plot(ns,mm[:,j],styles[j],color=colorset[j+2],label=name+' — modelo compacto')
for k,alg in enumerate(['heap','bitmap']):
    group=sorted((m for m in memory if m['algoritmo']==alg),key=lambda m:m['n'])
    ax.plot([m['n'] for m in group],[lg(m['pico_alocacoes_rastreadas_bytes']) for m in group],'o-',color=colorset[k],label=alg+' — tracemalloc',zorder=5)
ax.axhline(lg(256),color='#555555',label='Limite Embarca: 256 B')
ax.set_yscale('symlog',linthresh=10);ax.set_ylim(bottom=0)
ax.set_yticks([0,2,4,10,1000,1000000],['0','2','4','10','1000','1 000 000'])
finish(fig,ax,'memoria_comparativa','Seis amostras Python reais. Modelos compactos não representam objetos do interpretador; não são memória medida.')
fig,ax=new('Entrada, armazenamento em disco e processo','Bytes')
ax.set_yscale('log')
ax.plot(ns,ns*2,label='Entrada array: 2n B')
ax.plot(ns,ns*32768.5,'--',label='Unário: disco esperado')
ax.scatter([10000000],[env['rss_pico_processo_kib']*1024],s=100,label='RSS máximo: coleta de tempo')
finish(fig,ax,'armazenamento','RSS: processo completo, incluindo infraestrutura. Não é memória extra de uma função.')
result='# Metodologia e resultados Python\n\n'
result+='Um aquecimento e três rodadas por combinação. perf_counter_ns mede apenas a chamada ao algoritmo; geração, cópia, validação e impressão ficam fora. Inicializar o bitmap fica dentro. Mesmos dados para ambos: random.Random(20261108).getrandbits(16), reiniciado por escala. Não é geração criptográfica. Validação independente por set, contagem, unicidade e ordem ocorre depois de toda rodada.\n\n'
result+='Ambiente: '+env['python'].splitlines()[0]+'. '+env['sistema']+'. '+env['cpu_info']+'.\n\n'
result+='| Algoritmo | n | u | Mediana (s) | Mínimo (s) | Máximo (s) |\n|---|---|---|---|---|---|\n'
for r in rows:result+=f"| {r['algoritmo']} | {r['n']} | {r['u']} | {r['mediana_s']:.6f} | {r['min_s']:.6f} | {r['max_s']:.6f} |\n"
result+='\nA memória foi medida em uma execução completa separada por algoritmo e tamanho, nas três escalas, usando as mesmas entradas da coleta de tempo (mesmo gerador e semente). Cada combinação recebeu aquecimento pequeno e gc.collect antes do rastreamento. A entrada e o relógio foram preparados antes de iniciar tracemalloc; validar e escrever o registro ocorreu após encerrá-lo. Nenhum tempo rastreado substitui as medianas de desempenho acima. São seis amostras de pico, não intervalos de confiança nem prova de pior caso para qualquer distribuição.\n\n'
result+='| Algoritmo | n | u | Pico rastreado (B) | Payload entrada (B) |\n|---|---|---|---|---|\n'
for m in sorted(memory,key=lambda m:(m['n'],m['algoritmo'])):
    result+=f"| {m['algoritmo']} | {m['n']} | {m['u']} | {m['pico_alocacoes_rastreadas_bytes']} | {m['entrada_bytes']} |\n"
result+='\ntracemalloc rastreia alocações Python, mas não toda a memória interna ou a pilha nativa. Os frames do interpretador podem usar uma arena já reservada; pico de novas alocações não é uma medição completa desse espaço de execução. O vetor tem 2n B de payload, com cabeçalho e eventual folga separados. O RSS do gráfico de armazenamento é o máximo do processo da coleta de tempo, não o consumo isolado de uma função.\n\n'
layout=memory_env.get('pilha_cpython',{})
if 'frames' in layout:
    result+='## Verificação separada da pilha do interpretador\n\n'
    result+=f"No CPython 3.12 instalado, o layout foi calculado com base no cabeçalho interno pycore_frame.h, cujo hash está em memoria.json. O cabeçalho de cada frame ocupa {layout['cabecalho_frame_bytes']} B e cada slot ocupa {layout['ponteiro_bytes']} B. As funções não usam closures.\n\n"
    result+='| Função | Slots locais | Slots de avaliação | Capacidade do frame calculada (B) |\n|---|---|---|---|\n'
    for name,f in layout['frames'].items():
        result+=f"| {name} | {f['locais_slots']} | {f['pilha_avaliacao_slots']} | {f['capacidade_bytes_calculada']} |\n"
    result+=f"\nOs frames de heap_unique e sift coexistem durante a descida: a capacidade calculada é {layout['caminho_heap_unique_sift_bytes']} B, já acima de 256 B, antes dos objetos referenciados. Essa capacidade pode ser atendida por arena já reservada; não significa a mesma quantidade de novas alocações por chamada. Não se soma diretamente esse valor aos picos de tracemalloc. O cálculo vale para o layout e fontes registrados, não para qualquer versão de Python.\n\n"
else:
    result+='A capacidade dos frames não foi calculada automaticamente neste interpretador. Não há certificação de memória extra completa por tracemalloc.\n\n'
heap_peaks=[m['pico_alocacoes_rastreadas_bytes'] for m in memory if m['algoritmo']=='heap']
result+=('O Heap Sort excedeu os 256 B nas amostras rastreadas, portanto não atende à restrição Embarca nesta versão. ' if max(heap_peaks)>256 else 'As amostras rastreadas não comprovam a memória extra total nem certificam o limite Embarca. ')
result+='A equipe confirmou manter todos os códigos em Python. A técnica de Heap Sort continua com pouco espaço auxiliar no modelo teórico, mas essa propriedade não dá a esta implementação CPython uma garantia física de 256 B. A confirmação do professor sobre a linguagem não altera automaticamente o limite de memória do enunciado.\n\n'
big=next(r for r in rows if r['n']==10000000 and r['algoritmo']=='bitmap')
result+=f"O bitmap levou {big['mediana_s']:.6f} s de mediana local em n=10⁷. "+('A mediana ficou abaixo de 2 s localmente; isso não certifica a máquina da disciplina.' if big['mediana_s']<2 else 'A mediana local excedeu 2 s: o alvo temporal também não foi atingido nesta coleta. Não se substitui a medição por estimativa.')+'\n\n'
result+='Recomendação: bitmap para Datacenter pelo domínio conhecido e custo linear, sujeito ao hardware da disciplina. Heap Sort demonstra ordenação/compactação sem vetor auxiliar, mas esta versão Python não é certificada para a Embarca. Permanecem necessárias confirmação da linguagem e aprovação do par.\n'
source=(R/'docs/analise_teorica.md').read_text()+'\n\n'+result
for name in ['tempo_medido','tempo_comparativo','tempo_completo','memoria_algoritmos','memoria_comparativa','armazenamento']:source+=f'\n\n![{name}](graficos/{name}.png)\n'
(R/'docs/relatorio.md').write_text(source)

font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
pdfmetrics.registerFont(TTFont('DV',font));pdfmetrics.registerFont(TTFont('DVB',font.replace('.ttf','-Bold.ttf')))
ss=getSampleStyleSheet()
for sty in ss.byName.values():sty.fontName='DV'
ss['Normal'].fontSize=9;ss['Normal'].leading=14;ss['Normal'].spaceAfter=7
for h in ['Heading1','Heading2','Heading3']:ss[h].fontName='DVB';ss[h].spaceBefore=14
ss['Heading1'].fontSize=17;ss['Heading2'].fontSize=13;ss['Heading3'].fontSize=11
ss['Code'].fontSize=7
story=[];lines=source.splitlines();i=0

def inline(s):
    s=escape(s);s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);s=re.sub(r'`([^`]+)`',r'<font name="DV">\1</font>',s);return s
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('!['):
        path=re.search(r'\]\((.+)\)',line).group(1);story.extend([PageBreak(),Image(str(R/path),width=490,height=294),Spacer(1,10)]);i+=1;continue
    if line.startswith('```'):
        buf=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):buf.append(lines[i]);i+=1
        story.append(Preformatted('\n'.join(buf),ss['Code']));i+=1;continue
    if line.startswith('|'):
        table=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[x.strip() for x in lines[i].strip('|').split('|')]
            if not all(re.fullmatch('[-: ]+',c) for c in cells): table.append(cells)
            i+=1
        width=490/len(table[0]);small=ss['Normal'].clone('Small');small.fontSize=6.3;small.leading=9
        tbl=Table([[Paragraph(inline(c),small) for c in row] for row in table],colWidths=[width]*len(table[0]),repeatRows=1)
        tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1ebf5')),('GRID',(0,0),(-1,-1),.3,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.extend([tbl,Spacer(1,10)]);continue
    if line.startswith('#'):
        level=min(len(line)-len(line.lstrip('#')),3)
        story.append(Paragraph(inline(line.lstrip('#').strip()),ss['Heading'+str(level)]));i+=1;continue
    buf=[line];i+=1
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![','```','- ')):buf.append(lines[i]);i+=1
    story.append(Paragraph(inline(' '.join(buf)),ss['Normal']))
def footer(canvas,doc):
    canvas.setFont('DV',8);canvas.drawString(42,24,'PjBL — Complexidade de Algoritmos');canvas.drawRightString(552,24,str(doc.page))
SimpleDocTemplate(str(R/'relatorio.pdf'),pagesize=(595,842),rightMargin=52,leftMargin=42,topMargin=40,bottomMargin=42,title='PjBL — Deduplicação de leituras de sensores',author='Henry Rodrigues; Rafael Maluf; Matheus').build(story,onFirstPage=footer,onLaterPages=footer)
print('Gráficos, modelos em CSV, fonte Markdown e relatório PDF gerados.')
