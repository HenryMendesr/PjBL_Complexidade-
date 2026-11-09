# PjBL — Complexidade de Algoritmos

Trabalho sobre deduplicação de leituras de sensores para Embarca e Datacenter. A prioridade da exposição é a **lógica matemática**: especificação da saída, provas de corretude, somatórios, complexidade de tempo/espaço e limites das hipóteses probabilísticas.

## Leitura recomendada

1. [Fundamentação matemática](projeto/docs/fundamentacao_matematica.md): demonstrações e contagens verificáveis.
2. [Análise das dez estratégias](projeto/docs/analise_teorica.md): deduções, restrições e comparação dos clientes.
3. [Relatório completo em PDF](projeto/relatorio.pdf): fundamentação, metodologia, resultados e recomendações.
4. [Modelos das oito extrapolações](projeto/docs/modelos.md): custos assumidos e leitura dos gráficos.
5. [Roteiro de apresentação e defesa oral](projeto/docs/apresentacao.md).

A entrega implementa exatamente duas estratégias em C: Heap Sort iterativo in-place e bitmap de 65536 bits. As outras oito são analisadas e modeladas, sem benchmarks fictícios. Python automatiza experimentos, verificações matemáticas e documentos.

## Verificação

```sh
cd projeto
make math        # 105 verificações independentes de contas e identidades
make test        # corretude das duas implementações nas três escalas
make sanitize    # AddressSanitizer e UndefinedBehaviorSanitizer
make bench       # nova coleta real: substitui os CSV locais
make docs        # regenera relatório e gráficos a partir dos dados
python3 scripts/verificar.py
```

Consulte [instruções completas](projeto/README.md), [checklist da rubrica](projeto/docs/checklist.md) e [medições reais](projeto/dados/resumo.csv). Dependências Python em projeto/requirements.txt. O ZIP de entrega está na raiz; fontes editáveis, gráficos e evidências estão em projeto/.

**Pendências externas:** aprovação do par pelo professor, confirmação de C diante das menções a Pascal e teste na máquina de referência. Os tempos registrados são locais; não certificam o prazo de dois segundos na máquina da disciplina. Dados acadêmicos dos autores não foram informados no pedido e não foram inventados no relatório.
