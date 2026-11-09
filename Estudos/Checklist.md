# Checklist da entrega Python

| Item | Situação |
|---|---|
| Dez estratégias analisadas e quatro contas de inviabilidade | Presente na análise e no relatório |
| Exatamente duas estratégias implementadas | heap.py e bitmap.py |
| Domínio 0–65535, vetor vazio, extremos, distintos e repetições | Testes com referência independente |
| n=1000,100000,10000000 | Coleta real com validação após cada rodada |
| Tempo separado de geração, cópia e validação | perf_counter_ns em torno da função |
| Oito extrapolações comparadas às duas medidas | Figuras individuais com legenda explícita |
| Memória do algoritmo e entrada separadas | Amostra tracemalloc em n=1000; 2n bytes de payload de entrada |
| Embarca: garantia de no máximo 256 B extras | NÃO atendida na amostra: Heap Sort teve 380 B rastreados; não usar evidência antiga de C |
| Memória medida nas três escalas | Parcial: amostra somente em n=1000; não há curva empírica completa de memória |
| Datacenter: menos de 2 s na máquina da disciplina | Pendente; a medição disponível é local |
| Linguagem Python e par aprovados pelo professor | Pendente de confirmação |
| Relatório PDF, fonte editável e instruções | Presentes em projeto/ e no README da raiz |

Todos os programas são Python. Estudos contém apenas apoio; a pasta projeto contém os itens da entrega. A migração privilegia a linguagem conhecida pela equipe e não declara satisfeitas as restrições que não foram comprovadas.
