# Checklist de entrega e validação

Legenda: CONCLUÍDO significa produzido e/ou verificado localmente; PENDENTE é uma exigência externa ainda não demonstrada. A checklist não equivale a nota atribuída.

| Requisito | Situação e evidência |
|---|---|
| Leitura integral e interpretação do PDF | CONCLUÍDO; docs/analise_teorica.md documenta divergências |
| Domínio 0–65535 e n=10³,10⁵,10⁷ | CONCLUÍDO; uint16_t, CSV real e casos nas três escalas |
| Provas, somatórios e probabilidades auditadas | CONCLUÍDO; fundamentacao_matematica.md e 105 verificações independentes em revisao_matematica.txt |
| Dez análises com tempo, espaço e hipóteses | CONCLUÍDO; dez seções em analise_teorica.md |
| Exatamente duas estratégias implementadas | CONCLUÍDO; src/heap.c e src/bitmap.c; oráculo apenas em tests |
| Contratos, ordem e compactação | CONCLUÍDO; dedup.h, código e testes |
| Heap iterativo sem heap dinâmico ou recursão | CONCLUÍDO; fonte, nm, desmontagem e frames static |
| Embarca ≤256 B extras independente de n | CONCLUÍDO no build local: 96 B conservadores; refazer em novo alvo |
| Datacenter <2 s em n=10⁷ | CONCLUÍDO localmente; PENDENTE na máquina de referência |
| Casos vazios, unitário, iguais, distintos, ordenados, reversos, intercalados, extremos, pequenos | CONCLUÍDO; tests/test.c e dados/testes.txt |
| Corretude nas três escalas e comparação exata de conjuntos/ordem | CONCLUÍDO; 222 casos/algoritmo e validação em cada rodada |
| Compilação e análise de erros de memória | CONCLUÍDO; GCC sem avisos, ASan/UBSan em dados/sanitizers.txt |
| Benchmark com aquecimento, sete rodadas e dispersão | CONCLUÍDO; CSV bruto 42 linhas e resumo seis linhas |
| Hardware, SO, compilador, flags, semente e distribuição | CONCLUÍDO; ambiente.json e CSV |
| Separar algoritmo, entrada e processo; pilha, heap e disco | CONCLUÍDO; metodologia, memória e dois painéis gráficos |
| Oito extrapolações no gráfico com duas medições | CONCLUÍDO; tempo.png e previsoes_log10.csv |
| Constantes, hipóteses e incerteza explícitas | CONCLUÍDO; modelos.md |
| Fatoriais/exponenciais sem overflow ou sumiço | CONCLUÍDO; lgamma e CSV log₁₀, painel de faixa completa |
| Cálculos das quatro estratégias exageradas | CONCLUÍDO; exemplos numéricos e cenários especiais |
| Corrigir unário, power set, Bogosort repetido e Bloom | CONCLUÍDO; análise e modelos |
| Relatório PDF e fonte editável | CONCLUÍDO; relatorio.pdf e docs/relatorio.md |
| Código, automação, dependências, README, gráficos e ZIP | CONCLUÍDO na entrega; roteiro de reprodução no README |
| Aprovação prévia do par pelo professor | PENDENTE; não foi informada |
| Confirmação de linguagem C | PENDENTE; divergência textual com Pascal |
| Dados dos integrantes/instituição/professor | PENDENTE; não inventados |
| Bloom empírico ≤1% | NÃO SE APLICA; Bloom só analisado, soluções exatas |

## Revisão pelos seis critérios da rubrica

| Critério | Peso | Material para revisão e limite |
|---|---|---|
| Análise das dez estratégias | 25% | analise_teorica.md; inclui deduções, hipóteses, domínio limitado e recursos separados |
| Justificativa do par | 10% | seção Escolha e contrato, comparação com as outras oito; aprovação pendente |
| Implementação e instrumentação em Pascal | 20% | fontes C, testes, frames, desmontagem e sanitizadores; C precisa ser aceito pelo professor |
| Dados e coerência teoria/prática | 20% | 42 medições, seis resumos, gráficos e discussão; máquina da referência pendente |
| Estratégias exageradas e extrapolação | 15% | quatro cálculos explícitos, oito curvas e custos hipotéticos auditáveis |
| Relatório, recomendação e comunicação | 10% | PDF completo, fontes editáveis, recomendações por cliente e roteiro oral |

A soma dos pesos é 100%. Não se estima nota: ela depende do professor e das pendências acima, especialmente linguagem e máquina de referência.
