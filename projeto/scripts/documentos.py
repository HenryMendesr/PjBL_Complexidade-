#!/usr/bin/env python3

import csv, json, math, re, statistics, hashlib
from pathlib import Path
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1]
from modelos import models, names, lg
rows=list(csv.DictReader((R/'dados/resumo.csv').open()))
ns=np.unique(np.rint(np.logspace(3,7,101)).astype(int))
mt=np.array([models(int(n))[0] for n in ns]);mm=np.array([models(int(n))[1] for n in ns])
with (R/'dados/previsoes_log10.csv').open('w') as f:
    w=csv.writer(f,lineterminator="\n");w.writerow(['n','estrategia','log10_segundos_previstos','log10_ram_extra_bytes_previstos'])
    for i,n in enumerate(ns):
        for j,name in enumerate(names):w.writerow([int(n),name,mt[i,j],mm[i,j]])
plt.rcParams.update({'font.size':9,'figure.dpi':150})
styles=['--',':','-.','--',':','-.','--',':'];cols=plt.cm.tab10.colors
fig,axs=plt.subplots(1,2,figsize=(12,6))
for j,name in enumerate(names):
    axs[0].plot(ns,10**np.clip(mt[:,j],-15,8),styles[j],color=cols[j+2 if j<8 else j],label=name+' — previsão')
    axs[1].plot(ns,mt[:,j],styles[j],color=cols[j+2],label=name)
for k,alg in enumerate(['heap','bitmap']):
    rr=[r for r in rows if r['algoritmo']==alg];xx=[int(r['n']) for r in rr];yy=[float(r['mediana_s']) for r in rr]
    for ax,ys in [(axs[0],yy),(axs[1],[lg(t) for t in yy])]:
        ax.plot(xx,ys,'o-',color=cols[k],linewidth=2,label=alg+' — medido')
    axs[0].errorbar(xx,yy,yerr=[[float(r['mediana_s'])-float(r['min_s']) for r in rr],[float(r['max_s'])-float(r['mediana_s']) for r in rr]],fmt='none',color=cols[k])
axs[0].set(yscale='log',ylim=(1e-8,1e6),ylabel='Tempo (s), escala log',title='Faixa prática; curvas superiores continuam no painel ao lado')
axs[0].axhline(2,color='black',alpha=.4);axs[0].text(1200,3,'2 s (meta da referência)')
axs[1].set(yscale='symlog',ylabel='log10(tempo em s), eixo symlog',title='Todas as ordens de grandeza, sem overflow')
for ax in axs:ax.set_xscale('log');ax.set_xlabel('n (leituras)');ax.grid(True,alpha=.2)
handles,labels=axs[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,fontsize=8)
fig.suptitle('Duas medições e oito modelos hipotéticos — constantes em docs/modelos.md')
fig.tight_layout(rect=(0,.18,1,.94));fig.savefig(R/'graficos/tempo.png');fig.savefig(R/'graficos/tempo.pdf');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(12,5.8))
for j,name in enumerate(names):axs[0].plot(ns,mm[:,j],styles[j],color=cols[j+2],label=name+' — cálculo')
for k,alg in enumerate(['heap','bitmap']):
    rr=[r for r in rows if r['algoritmo']==alg]
    axs[0].plot([int(r['n']) for r in rr],[lg(float(r['extra_conservador_bytes'])) for r in rr],'o-',color=cols[k],linewidth=2,label=alg+' — GCC + margem')
axs[0].axhline(lg(256),color='black',alpha=.4,label='256 B')
axs[0].set(yscale='symlog',ylim=(0,None),ylabel='log10(RAM extra em bytes), eixo symlog',title='RAM: pilha + heap; subconjuntos materializados')
axs[1].plot(ns,ns*2,label='Vetor de entrada (calculado)')
axs[1].plot(ns,ns*32768.5,'--',label='Disco unário esperado (calculado)')
for alg in ['heap','bitmap']:
    rr=[r for r in rows if r['algoritmo']==alg]
    axs[1].plot([int(r['n']) for r in rr],[int(r['rss_pico_kib'])*1024 for r in rr],'o-',label='RSS processo '+alg+' (medido)')
axs[1].set(yscale='log',ylabel='Bytes, escala log',title='Recursos separados: entrada, processo e disco')
axs[1].legend(fontsize=8)
for ax in axs:ax.set_xscale('log');ax.set_xlabel('n (leituras)');ax.grid(True,alpha=.2)
h,l=axs[0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',ncol=3,fontsize=8)
fig.tight_layout(rect=(0,.21,1,.96));fig.savefig(R/'graficos/memoria.png');fig.savefig(R/'graficos/memoria.pdf');plt.close(fig)
manifest={
    'entradas_sha256':{path:hashlib.sha256((R/path).read_bytes()).hexdigest() for path in ['dados/resumo.csv','scripts/modelos.py','scripts/documentos.py']},
    'saidas_sha256':{path:hashlib.sha256((R/path).read_bytes()).hexdigest() for path in ['graficos/tempo.png','graficos/tempo.pdf','graficos/memoria.png','graficos/memoria.pdf','dados/previsoes_log10.csv']},
    'pontos_medidos':[{'algoritmo':row['algoritmo'],'n':int(row['n']),'mediana_s':float(row['mediana_s']),'min_s':float(row['min_s']),'max_s':float(row['max_s']),'extra_conservador_bytes':int(row['extra_conservador_bytes']),'rss_pico_kib':int(row['rss_pico_kib'])} for row in rows],
    'estrategias_extrapoladas':names,'grade_n':[int(n) for n in ns],
    'painel_completo':'log10 da grandeza sobre eixo symlog; nenhuma curva descartada'}
(R/'dados/manifesto_graficos.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))


env=json.loads((R/'dados/ambiente.json').read_text())
cpu=next((l.split(':',1)[1].strip() for l in env['cpu'].splitlines() if l.startswith('Model name:')),'ver ambiente.json')
result='## Resultados locais efetivamente medidos\n\n'
result+='CPU informada ao ambiente: '+cpu+'. Sistema: '+env['plataforma']+'. Compilador: '+env['compilador'].splitlines()[0]+'.\n\n'
result+='| Algoritmo | n | u | Mediana (s) | Mín–máx (s) | Q1–Q3 (s) | Extra conservador (B) | RSS pico (KiB) |\n|---|---|---|---|---|---|---|---|\n'
for r in rows:
    result+=f"| {r['algoritmo']} | {r['n']} | {r['u']} | {float(r['mediana_s']):.9f} | {float(r['min_s']):.9f}–{float(r['max_s']):.9f} | {float(r['q1_s']):.9f}–{float(r['q3_s']):.9f} | {r['extra_conservador_bytes']} | {r['rss_pico_kib']} |\n"
result+='\nO RSS é o máximo residente de cada processo Linux, inclui dois vetores, oráculo, runtime e páginas tocadas. Não é memória extra do algoritmo e não deve ser subtraído do vetor para inferir a pilha. A inicialização do bitmap está dentro do cronômetro.\n'
(R/'docs/resultados.md').write_text(result)
parts=['# PjBL: Duas empresas, duas restrições\n\nDeduplicação de leituras de sensores — relatório técnico.\n\nIntegrantes: Henry Rodrigues, Rafael Maluf e Matheus.\n\n',
(R/'docs/fundamentacao_matematica.md').read_text(),(R/'docs/analise_teorica.md').read_text(),(R/'docs/metodologia.md').read_text(),result,
(R/'docs/modelos.md').read_text(),'\n![Tempo](graficos/tempo.png)\n\n![Memória](graficos/memoria.png)\n\n',
(R/'docs/discussao.md').read_text(),(R/'docs/auditoria.md').read_text(),(R/'docs/checklist.md').read_text(),(R/'docs/apresentacao.md').read_text()]
source='\n\n'.join(parts);(R/'docs/relatorio.md').write_text(source)

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
        path=re.search(r'\]\((.+)\)',line).group(1);story.extend([PageBreak(),Image(str(R/path),width=490,height=265),Spacer(1,10)]);i+=1;continue
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
