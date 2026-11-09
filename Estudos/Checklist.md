# Checklist da entrega Python

## Como usar a pasta Estudos

1. Ler [Matematica.md](Matematica.md) para entender os símbolos, somatórios, probabilidades e conversões. Refazer os exemplos pequenos antes de estudar números astronômicos.
2. Ensaiar [apresentacao.md](apresentacao.md), acompanhando os algoritmos na entrada [3,1,3,0,65535]. O roteiro separa falas principais, cálculos e respostas de reserva.
3. Conferir abaixo quais itens têm evidência e quais permanecem parciais ou pendentes.

Os documentos desta pasta são material de apoio. Eles não alteram as medições nem substituem o relatório da entrega.

## Situação dos requisitos

| Item | Situação |
|---|---|
| Dez estratégias analisadas e quatro contas de inviabilidade | Presente na análise e no relatório |
| Exatamente duas estratégias implementadas | heap.py e bitmap.py |
| Domínio 0–65535, vetor vazio, extremos, distintos e repetições | Testes com referência independente |
| n=1000,100000,10000000 | Coleta real com validação após cada rodada |
| Tempo separado de geração, cópia e validação | perf_counter_ns em torno da função |
| Oito extrapolações comparadas às duas medidas | Figuras individuais com legenda explícita |
| Memória rastreada, frames e entrada separados | Seis amostras tracemalloc em memoria.json, capacidade dos frames calculada separadamente e 2n bytes de payload de entrada |
| Embarca: garantia de no máximo 256 B extras | NÃO atendida na amostra: Heap Sort teve 380 B rastreados; não usar evidência antiga de C |
| Memória rastreada nas três escalas | Uma execução completa por algoritmo/n; não é contagem de toda a memória do interpretador ou garantia universal |
| Datacenter: menos de 2 s na máquina da disciplina | Pendente; a medição disponível é local |
| Linguagem Python e par aprovados pelo professor | Pendente de confirmação |
| Relatório PDF, fonte editável e instruções | Presentes em projeto/ e no README da raiz |

Todos os programas são Python. Estudos contém apenas apoio; a pasta projeto contém os itens da entrega. A migração privilegia a linguagem conhecida pela equipe e não declara satisfeitas as restrições que não foram comprovadas.

## Conferência antes da apresentação

- Abrir os seis gráficos individuais e identificar corretamente os dois algoritmos medidos e as oito alternativas modeladas.
- Mostrar as três escalas no resumo de dados, sem misturar os tempos atuais de Python com os da versão antiga.
- Mostrar as três escalas de memória e explicar por que picos rastreados e capacidade dos frames são evidências separadas. Os 380 B em n=1000 já excedem 256 B.
- Conferir o contrato de prefixo: só a[0:u] é a resposta.
- Testar a demonstração pequena no computador da apresentação; preparar os gráficos se não houver tempo para rodar o benchmark inteiro.
- Usar a tabela atual de dados caso uma nova coleta tenha sido realizada.
- Tratar aprovação do professor e prazo na referência como pendências, não como fatos presumidos.

## Análise da revisão recebida

A revisão externa apontou corretamente que a entrega não podia ser considerada 100% conforme: o limite Embarca já havia falhado e a memória estava medida apenas em n=1000. A medição foi ampliada para as três escalas. O ponto dos 256 B continua sendo uma restrição não atendida pela versão Python atual; ele não vira «resolvido» por medir mais entradas.

| Sugestão da revisão | Encaminhamento |
|---|---|
| Resolver 256 B, possivelmente usando C | A equipe confirmou manter tudo em Python. A versão atual não é certificada; a capacidade calculada dos frames já excede 256 B no CPython instalado. Qualquer futura solução deve medir também a pilha, não apenas tentar reduzir o indicador de tracemalloc |
| Medir memória nos três tamanhos | Coleta separada dos tempos, com a função completa e validação independente após o rastreamento |
| Confirmar linguagem e aprovação do par | Dependem do professor. Aceitar Python como linguagem não significa dispensar os 256 B |
| Testar na máquina de referência | Pendente. A mediana de 1,04 s é evidência local do bitmap, não certificação externa |

Heap Sort é uma técnica de baixo espaço auxiliar no modelo de palavras, mas isso não torna automaticamente uma implementação CPython adequada a uma restrição física de 256 B. A recomendação Datacenter permanece baseada no domínio e nas medições locais. A implementação Embarca permanece demonstrativa enquanto não cumprir a restrição.
